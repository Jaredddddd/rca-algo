"""Generate the legacy case-indicator CREST-MEO Oracle sanity-check artifact.

This script is intentionally leaky and research-only: it reads service-level
GT labels to construct a per-case perfect oracle evidence matrix. It must never
be imported from the runtime algorithm path. For the benchmark-level universal
operator library, use ``crest_meo_universal_oracle.py``.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


REPO = Path(__file__).resolve().parents[1]
EVIDENCERANK_SRC = REPO / "algorithms/evidencerank/src"
sys.path.insert(0, str(EVIDENCERANK_SRC))

from evidencerank.cera import (  # noqa: E402
    ALL_MODALITIES,
    BASE_FEATURE_NAMES,
    MODALITY_FEATURES,
)
from evidencerank.meo.runtime.load_meol import DEFAULT_MEOL_PATH, load_operator_specs  # noqa: E402


DEFAULT_DATA_ROOT = REPO / "data/rcabench-platform-v2/data"
DEFAULT_LABELS = REPO / "data/rcabench-platform-v2/meta/rcabench-csv/labels.csv"
DEFAULT_OUTPUT = (
    REPO
    / "output/rcabench-platform-v2/crest_meo_oracle/case_indicator_oracle.json"
)
FEATURES = tuple(
    feature
    for feature in BASE_FEATURE_NAMES
    if feature in frozenset().union(
        *(MODALITY_FEATURES[modality] for modality in ALL_MODALITIES)
    )
)
INPUT_FRAME_NAMES = (
    "normal_metrics",
    "abnormal_metrics",
    "normal_traces",
    "abnormal_traces",
    "normal_logs",
    "abnormal_logs",
)
SERVICE_COLUMNS = (
    "service_name",
    "service",
    "svc",
    "parent_service",
    "attr.k8s.service.name",
)


def _repo_path(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else REPO / path


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def _feature_source(feature_name: str) -> str:
    for modality, feature_names in MODALITY_FEATURES.items():
        if feature_name in feature_names:
            return modality
    return "unknown"


def _load_labels(labels_path: Path, dataset: str) -> dict[str, set[str]]:
    labels = pd.read_csv(labels_path)
    required = {"dataset", "datapack", "gt.level", "gt.name"}
    missing = required - set(labels.columns)
    if missing:
        raise SystemExit(f"Label file is missing columns: {sorted(missing)}")
    labels = labels[
        (labels["dataset"] == dataset)
        & (labels["gt.level"] == "service")
    ]
    return {
        str(datapack): {str(name) for name in group["gt.name"].dropna()}
        for datapack, group in labels.groupby("datapack")
    }


def _operator_catalog(meol_path: Path) -> tuple[list[dict[str, Any]], tuple[str, ...], tuple[str, ...]]:
    meo_specs = load_operator_specs(meol_path)
    operators: list[dict[str, Any]] = [
        {
            "name": "oracle_gt_indicator",
            "operator_family": "oracle_label",
            "base_operator": "gt_indicator",
            "source": "oracle_label",
            "oracle_transform": "gt_indicator",
            "intentionally_leaky": True,
            "role_prior": {
                "mutation": 1.0,
                "propagation": 0.0,
                "observability_bias": 0.0,
                "topology_context": 0.0,
            },
            "rationale": "Perfect service-level GT indicator used only as an upper bound.",
        }
    ]

    for feature_name in FEATURES:
        operators.append(
            {
                "name": f"oracle_crest_{feature_name}",
                "operator_family": "crest_feature",
                "base_operator": feature_name,
                "source": _feature_source(feature_name),
                "oracle_transform": "gt_indicator_broadcast",
                "intentionally_leaky": True,
                "rationale": (
                    "Oracle upper-bound column for this CREST feature name. "
                    "The value is the service-level GT indicator broadcast "
                    "to this operator column."
                ),
            }
        )

    meo_feature_names = tuple(spec.name for spec in meo_specs)
    for spec in meo_specs:
        operators.append(
            {
                "name": f"oracle_meol_{spec.name}",
                "operator_family": "meol_operator",
                "base_operator": spec.name,
                "source": spec.source,
                "entity": spec.entity,
                "signal": {
                    "field": spec.signal.field,
                    "type": spec.signal.type,
                },
                "contrast": {
                    "operator": spec.contrast.operator,
                    "normal_window": spec.contrast.normal_window,
                    "abnormal_window": spec.contrast.abnormal_window,
                },
                "aggregation": {
                    "level": spec.aggregation.level,
                    "method": spec.aggregation.method,
                },
                "role_prior": spec.role_prior,
                "oracle_transform": "gt_indicator_broadcast",
                "intentionally_leaky": True,
                "rationale": (
                    "Oracle upper-bound column for this MEOL operator. The "
                    "value is the service-level GT indicator broadcast to "
                    "this operator column."
                ),
            }
        )
    return operators, FEATURES, meo_feature_names


def _clean_service(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null"}:
        return None
    return text


def _read_services_from_parquet(path: Path) -> set[str]:
    if not path.exists():
        return set()
    services: set[str] = set()
    for column in SERVICE_COLUMNS:
        try:
            frame = pd.read_parquet(path, columns=[column])
        except Exception:
            continue
        if column not in frame.columns:
            continue
        services.update(
            service
            for service in frame[column].map(_clean_service).dropna().unique()
            if service
        )
    return services


def _collect_services_fast(case_dir: Path, gt_services: set[str]) -> list[str]:
    services = set(gt_services)
    for frame_name in INPUT_FRAME_NAMES:
        services.update(_read_services_from_parquet(case_dir / f"{frame_name}.parquet"))
    return sorted(services)


def _process_case(
    data_root: Path,
    dataset: str,
    datapack: str,
    gt_services: set[str],
    operator_count: int,
) -> dict[str, Any]:
    case_dir = data_root / dataset / datapack
    if not case_dir.exists():
        return {
            "datapack": datapack,
            "gt_services": sorted(gt_services),
            "error": f"missing_case_dir:{_relative(case_dir)}",
        }

    services = _collect_services_fast(case_dir, gt_services)
    if not services:
        return {
            "datapack": datapack,
            "gt_services": sorted(gt_services),
            "error": "no_services",
        }

    indicator = [1 if service in gt_services else 0 for service in services]
    best_rank = 1 if any(indicator) and operator_count > 0 else 10**9

    return {
        "datapack": datapack,
        "gt_services": sorted(gt_services),
        "services": services,
        "best_rank": int(best_rank),
        "top1_hit": bool(best_rank == 1),
        "oracle_indicator": indicator,
    }


def _worker(args: tuple[Path, str, str, set[str], int]) -> dict[str, Any]:
    data_root, dataset, datapack, gt_services, operator_count = args
    try:
        return _process_case(data_root, dataset, datapack, gt_services, operator_count)
    except Exception as exc:
        return {
            "datapack": datapack,
            "gt_services": sorted(gt_services),
            "error": f"{type(exc).__name__}:{exc}",
        }


def _metrics(cases: list[dict[str, Any]]) -> dict[str, float | int]:
    valid_cases = [case for case in cases if "error" not in case]
    ranks = [float(case.get("best_rank", 10**9)) for case in valid_cases]
    if not ranks:
        return {
            "case_count": len(cases),
            "valid_case_count": 0,
            "error_count": len(cases),
            "service_rows": 0,
            "AC@1": 0.0,
            "MRR": 0.0,
            "AC@3": 0.0,
            "AC@5": 0.0,
        }
    return {
        "case_count": len(cases),
        "valid_case_count": len(valid_cases),
        "error_count": len(cases) - len(valid_cases),
        "service_rows": int(sum(len(case["services"]) for case in valid_cases)),
        "AC@1": sum(1 for rank in ranks if rank <= 1.0) / len(ranks),
        "MRR": sum(1.0 / rank for rank in ranks) / len(ranks),
        "AC@3": sum(1 for rank in ranks if rank <= 3.0) / len(ranks),
        "AC@5": sum(1 for rank in ranks if rank <= 5.0) / len(ranks),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an intentionally leaky per-case GT-indicator CREST-MEO "
            "Oracle sanity-check artifact."
        )
    )
    parser.add_argument("--dataset", default="rcabench")
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--labels", type=Path, default=DEFAULT_LABELS)
    parser.add_argument("--meol-path", type=Path, default=DEFAULT_MEOL_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    parser.add_argument("--indent", type=int, default=None)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    data_root = _repo_path(args.data_root)
    labels_path = _repo_path(args.labels)
    meol_path = _repo_path(args.meol_path)
    output = _repo_path(args.output)

    gt_by_datapack = _load_labels(labels_path, args.dataset)
    datapacks = sorted(gt_by_datapack)
    if args.limit is not None:
        datapacks = datapacks[: max(0, args.limit)]

    operators, crest_feature_names, meo_feature_names = _operator_catalog(meol_path)
    worker_args = [
        (data_root, args.dataset, datapack, gt_by_datapack[datapack], len(operators))
        for datapack in datapacks
    ]

    cases: list[dict[str, Any]] = []
    workers = max(1, int(args.workers))
    if workers == 1:
        for idx, item in enumerate(worker_args, start=1):
            cases.append(_worker(item))
            if idx % 100 == 0:
                print(f"processed {idx}/{len(worker_args)}", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_worker, item): item[2] for item in worker_args}
            for idx, future in enumerate(as_completed(futures), start=1):
                cases.append(future.result())
                if idx % 100 == 0:
                    print(f"processed {idx}/{len(worker_args)}", flush=True)

    cases.sort(key=lambda item: str(item["datapack"]))
    metrics = _metrics(cases)
    artifact = {
        "artifact_name": "crest-meo-case-indicator-oracle-rcabench-v1",
        "artifact_type": "oracle_upper_bound",
        "dataset": args.dataset,
        "created_at": datetime.now(UTC).isoformat(),
        "policy": {
            "uses_gt_labels": True,
            "uses_fault_labels": False,
            "uses_baseline_outputs": False,
            "uses_conclusion_parquet": False,
            "not_for_online_ranking": True,
            "intentionally_leaky": True,
            "purpose": "Upper-bound evidence operator artifact for offline research only.",
        },
        "inputs": {
            "labels": _relative(labels_path),
            "data_root": _relative(data_root),
            "meol_path": _relative(meol_path),
        },
        "oracle_semantics": (
            "Each operator column is encoded as the service-level GT indicator. "
            "The case-level oracle_indicator vector is broadcast to every "
            "operator in the operators list, giving perfect evidence for each "
            "CREST/MEOL operator family name."
        ),
        "oracle_matrix_encoding": "broadcast_oracle_indicator_to_all_operators",
        "crest_feature_names": list(crest_feature_names),
        "meol_feature_names": list(meo_feature_names),
        "operators": operators,
        "operator_count": len(operators),
        "metrics": metrics,
        "cases": cases,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(
            artifact,
            handle,
            ensure_ascii=False,
            indent=args.indent,
            separators=None if args.indent is not None else (",", ":"),
        )
        handle.write("\n")

    print(f"saved {output.relative_to(REPO) if output.is_relative_to(REPO) else output}")
    print(json.dumps(metrics, sort_keys=True))
    if metrics["error_count"]:
        errors = [case for case in cases if "error" in case][:5]
        print(f"sample_errors={json.dumps(errors, ensure_ascii=False)[:2000]}")


if __name__ == "__main__":
    main()
