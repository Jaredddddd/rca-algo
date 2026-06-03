#!/usr/bin/env python3
"""Dump EvidenceRank feature matrices and reweight them offline.

This is an evaluation-side research tool. It may read labels when computing
metrics, but the EvidenceRank algorithm path remains label-free.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCERANK_SRC = REPO_ROOT / "algorithms" / "evidencerank" / "src"
sys.path.insert(0, str(EVIDENCERANK_SRC))

from evidencerank.algorithm import (  # noqa: E402
    ALL_MODALITIES,
    BASE_FEATURE_NAMES,
    FEATURE_PRIORITIES,
    PARENT_CONTEXT_WEIGHT,
    FeaturePriority,
    _adaptive_feature_weights,
    _build_feature_matrix,
    _collect_services_from_frames,
    _heuristic_scores,
    _load_input_frames,
    _top_ranked_service,
)


DEFAULT_DATA_ROOT = REPO_ROOT / "data" / "rcabench-platform-v2" / "data"
DEFAULT_LABELS = (
    REPO_ROOT / "data" / "rcabench-platform-v2" / "meta" / "rcabench-csv" / "labels.csv"
)
OUTPUT_ROOT = REPO_ROOT / "output" / "rcabench-platform-v2"
FEATURE_CACHE_ROOT = OUTPUT_ROOT / "evolve_feature_cache"
REWEIGHT_ROOT = OUTPUT_ROOT / "evolve_reweights"

PRIORITY_ORDER = tuple(FeaturePriority)
LADDER_PRESETS: dict[str, tuple[float, ...]] = {
    "current": (0.0, 0.75, 1.0, 1.25, 1.5, 6.0, 10.0, 16.0),
    "linear_0_7": (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0),
    "power2_tier": (0.0, 1.0, 1.0, 1.0, 2.0, 4.0, 8.0, 16.0),
    "decimal_1_2_5_10_15": (0.0, 1.0, 1.0, 1.0, 2.0, 5.0, 10.0, 15.0),
}


@dataclass(frozen=True)
class Metrics:
    total: int
    missing_outputs: int
    ac1: float
    ac3: float
    ac5: float
    mrr: float
    avg_rank: float | None
    top5_miss: int


@dataclass(frozen=True)
class CaseFeaturePack:
    datapack: str
    feature_rows: list[dict[str, Any]]
    edge_rows: list[dict[str, Any]]
    error: str = ""


@dataclass(frozen=True)
class CachedCase:
    datapack: str
    services: list[str]
    matrix: np.ndarray
    trace_edges: list[tuple[str, str]]


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def _cache_dir(cache: str | Path) -> Path:
    path = Path(cache)
    if path.exists() or path.is_absolute() or "/" in str(cache):
        return _repo_path(path)
    return FEATURE_CACHE_ROOT / str(cache)


def _parse_ladder(value: str | None, preset: str | None) -> tuple[float, ...]:
    if value:
        parts = [part.strip() for part in value.split(",") if part.strip()]
        if len(parts) != len(PRIORITY_ORDER):
            raise SystemExit(
                f"--weights must contain {len(PRIORITY_ORDER)} comma-separated values"
            )
        ladder = tuple(float(part) for part in parts)
    else:
        name = preset or "current"
        if name not in LADDER_PRESETS:
            raise SystemExit(
                f"Unknown preset {name!r}; choose one of {sorted(LADDER_PRESETS)}"
            )
        ladder = LADDER_PRESETS[name]

    if ladder[FeaturePriority.DISABLED] != 0.0:
        raise SystemExit("DISABLED priority weight must be 0.0")
    for left, right in zip(ladder, ladder[1:]):
        if right < left:
            raise SystemExit("Priority ladder must be monotonic nondecreasing")
    return ladder


def _feature_weights_from_ladder(ladder: tuple[float, ...]) -> np.ndarray:
    values = {
        priority: float(ladder[int(priority)])
        for priority in PRIORITY_ORDER
    }
    return np.asarray(
        [values[FEATURE_PRIORITIES[name]] for name in BASE_FEATURE_NAMES],
        dtype=np.float32,
    )


def _score_case(
    services: list[str],
    matrix: np.ndarray,
    edges: list[tuple[str, str]],
    base_weights: np.ndarray,
) -> dict[str, float]:
    scores = _heuristic_scores(
        services,
        matrix,
        BASE_FEATURE_NAMES,
        base_weights,
        edges,
        PARENT_CONTEXT_WEIGHT,
    )
    adaptive_weights = _adaptive_feature_weights(
        matrix,
        BASE_FEATURE_NAMES,
        base_weights,
    )
    if not np.array_equal(adaptive_weights, base_weights):
        adaptive_scores = _heuristic_scores(
            services,
            matrix,
            BASE_FEATURE_NAMES,
            adaptive_weights,
            edges,
            PARENT_CONTEXT_WEIGHT,
        )
        if _top_ranked_service(adaptive_scores) == _top_ranked_service(scores):
            scores = adaptive_scores
    return scores


def _load_labels(labels_path: Path, dataset: str) -> dict[str, set[str]]:
    labels = pd.read_csv(labels_path)
    required = {"dataset", "datapack", "gt.level", "gt.name"}
    missing = required - set(labels.columns)
    if missing:
        raise SystemExit(f"Label file is missing columns: {sorted(missing)}")
    labels = labels[(labels["dataset"] == dataset) & (labels["gt.level"] == "service")]
    result: dict[str, set[str]] = {}
    for datapack, group in labels.groupby("datapack"):
        result[str(datapack)] = {str(name) for name in group["gt.name"].dropna()}
    return result


def _metrics(cases: pd.DataFrame) -> Metrics:
    if cases.empty:
        return Metrics(0, 0, 0.0, 0.0, 0.0, 0.0, None, 0)
    ranks = pd.to_numeric(cases["best_rank"], errors="coerce")
    return Metrics(
        total=int(len(cases)),
        missing_outputs=int(cases["missing_output"].fillna(False).sum()),
        ac1=float(cases["hit@1"].mean()),
        ac3=float(cases["hit@3"].mean()),
        ac5=float(cases["hit@5"].mean()),
        mrr=float(cases["mrr"].mean()),
        avg_rank=float(ranks.dropna().mean()) if ranks.notna().any() else None,
        top5_miss=int((~cases["hit@5"]).sum()),
    )


def _case_dirs(data_root: Path, dataset: str) -> list[Path]:
    dataset_root = data_root / dataset
    if not dataset_root.exists():
        raise SystemExit(f"Dataset root not found: {dataset_root}")
    return sorted({path.parent for path in dataset_root.glob("*/normal_metrics.parquet")})


def _dump_case(case_dir: Path, dataset: str) -> CaseFeaturePack:
    datapack = case_dir.name
    try:
        frames = _load_input_frames(case_dir)
        services = _collect_services_from_frames(frames)
        if not services:
            return CaseFeaturePack(datapack, [], [])
        matrix, edges = _build_feature_matrix(
            frames,
            services,
            BASE_FEATURE_NAMES,
            ALL_MODALITIES,
        )
        feature_rows: list[dict[str, Any]] = []
        for service_idx, service in enumerate(services):
            row: dict[str, Any] = {
                "dataset": dataset,
                "datapack": datapack,
                "service_index": service_idx,
                "service": service,
            }
            row.update(
                {
                    feature: float(matrix[service_idx, feature_idx])
                    for feature_idx, feature in enumerate(BASE_FEATURE_NAMES)
                }
            )
            feature_rows.append(row)
        edge_rows = [
            {
                "dataset": dataset,
                "datapack": datapack,
                "edge_index": edge_idx,
                "source": source,
                "target": target,
            }
            for edge_idx, (source, target) in enumerate(edges)
        ]
        return CaseFeaturePack(datapack, feature_rows, edge_rows)
    except Exception as exc:  # noqa: BLE001 - research report should keep going.
        return CaseFeaturePack(datapack, [], [], repr(exc))


def cmd_dump(args: argparse.Namespace) -> None:
    data_root = _repo_path(args.data_root)
    out_dir = FEATURE_CACHE_ROOT / args.version
    if out_dir.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite feature cache: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    cases = _case_dirs(data_root, args.dataset)
    feature_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    errors: dict[str, str] = {}
    workers = max(1, int(args.workers))

    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_dump_case, case_dir, args.dataset) for case_dir in cases]
        for future in as_completed(futures):
            pack = future.result()
            if pack.error:
                errors[pack.datapack] = pack.error
            feature_rows.extend(pack.feature_rows)
            edge_rows.extend(pack.edge_rows)

    features = pd.DataFrame(feature_rows).sort_values(
        ["datapack", "service_index"], kind="stable"
    )
    edges = pd.DataFrame(edge_rows)
    if not edges.empty:
        edges = edges.sort_values(["datapack", "edge_index"], kind="stable")

    features.to_parquet(out_dir / "features.parquet", index=False)
    edges.to_parquet(out_dir / "trace_edges.parquet", index=False)
    manifest = {
        "version": args.version,
        "created": _now(),
        "dataset": args.dataset,
        "data_root": str(data_root),
        "case_count": len(cases),
        "feature_rows": len(features),
        "edge_rows": len(edges),
        "feature_names": list(BASE_FEATURE_NAMES),
        "errors": errors,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(
        f"Feature cache saved: {out_dir} "
        f"({len(cases)} cases, {len(features)} service rows, {len(errors)} errors)"
    )


def _load_cache(cache: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    root = _cache_dir(cache)
    features_path = root / "features.parquet"
    edges_path = root / "trace_edges.parquet"
    if not features_path.exists():
        raise SystemExit(f"Feature cache not found: {features_path}")
    features = pd.read_parquet(features_path)
    edges = pd.read_parquet(edges_path) if edges_path.exists() else pd.DataFrame()
    return features, edges


def _prepare_cached_cases(
    features: pd.DataFrame,
    edges: pd.DataFrame,
) -> list[CachedCase]:
    edge_groups = {
        str(datapack): group
        for datapack, group in edges.groupby("datapack")
    } if not edges.empty else {}

    cases: list[CachedCase] = []
    for datapack, group in features.groupby("datapack", sort=True):
        datapack = str(datapack)
        group = group.sort_values("service_index", kind="stable")
        services = [str(service) for service in group["service"].tolist()]
        matrix = group[list(BASE_FEATURE_NAMES)].to_numpy(dtype=np.float32, copy=True)
        edge_group = edge_groups.get(datapack)
        if edge_group is None:
            trace_edges: list[tuple[str, str]] = []
        else:
            edge_group = edge_group.sort_values("edge_index", kind="stable")
            trace_edges = [
                (str(item["source"]), str(item["target"]))
                for item in edge_group.to_dict("records")
            ]
        cases.append(CachedCase(datapack, services, matrix, trace_edges))
    return cases


def _rank_prepared_cases(
    cached_cases: list[CachedCase],
    labels: dict[str, set[str]],
    dataset: str,
    ladder: tuple[float, ...],
    top_k: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    base_weights = _feature_weights_from_ladder(ladder)
    ranking_rows: list[dict[str, Any]] = []
    case_rows: list[dict[str, Any]] = []
    for cached in cached_cases:
        scores = _score_case(
            cached.services,
            cached.matrix,
            cached.trace_edges,
            base_weights,
        )
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        gt = labels.get(cached.datapack, set())
        best_rank: int | None = None
        for rank, (service, score) in enumerate(ranked, start=1):
            hit = service in gt
            if hit and best_rank is None:
                best_rank = rank
            ranking_rows.append(
                {
                    "dataset": dataset,
                    "datapack": cached.datapack,
                    "level": "service",
                    "name": service,
                    "rank": rank,
                    "score": float(score),
                    "hit": hit,
                }
            )
        names = [service for service, _score in ranked]
        case_rows.append(
                {
                    "dataset": dataset,
                    "datapack": cached.datapack,
                    "gt": ";".join(sorted(gt)),
                    "gt_count": len(gt),
                    "missing_output": False,
                "best_rank": best_rank if best_rank is not None else pd.NA,
                "mrr": (1.0 / best_rank) if best_rank else 0.0,
                "hit@1": bool(best_rank == 1),
                "hit@3": bool(best_rank is not None and best_rank <= 3),
                "hit@5": bool(best_rank is not None and best_rank <= 5),
                "top1": names[0] if names else "",
                "top3": "|".join(names[:3]),
                "top5": "|".join(names[:5]),
                f"top{top_k}": "|".join(names[:top_k]),
            }
        )

    seen = {case.datapack for case in cached_cases}
    for datapack, gt in labels.items():
        if datapack in seen:
            continue
        case_rows.append(
            {
                "dataset": dataset,
                "datapack": datapack,
                "gt": ";".join(sorted(gt)),
                "gt_count": len(gt),
                "missing_output": True,
                "best_rank": pd.NA,
                "mrr": 0.0,
                "hit@1": False,
                "hit@3": False,
                "hit@5": False,
                "top1": "",
                "top3": "",
                "top5": "",
                f"top{top_k}": "",
            }
        )

    rankings = pd.DataFrame(ranking_rows).sort_values(
        ["datapack", "rank"], kind="stable"
    )
    cases = pd.DataFrame(case_rows).sort_values("datapack", kind="stable")
    return rankings, cases


def _rank_from_cache(
    features: pd.DataFrame,
    edges: pd.DataFrame,
    labels: dict[str, set[str]],
    dataset: str,
    ladder: tuple[float, ...],
    top_k: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cached_cases = _prepare_cached_cases(features, edges)
    return _rank_prepared_cases(cached_cases, labels, dataset, ladder, top_k)


def cmd_reweight(args: argparse.Namespace) -> None:
    ladder = _parse_ladder(args.weights, args.preset)
    features, edges = _load_cache(args.cache)
    labels = _load_labels(_repo_path(args.labels), args.dataset)
    cached_cases = _prepare_cached_cases(features, edges)
    rankings, cases = _rank_from_cache(
        features,
        edges,
        labels,
        args.dataset,
        ladder,
        args.top_k,
    )
    metrics = _metrics(cases)

    out_dir = REWEIGHT_ROOT / args.version
    if out_dir.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite reweight output: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    rankings.to_parquet(out_dir / "rankings.parquet", index=False)
    cases.to_csv(out_dir / "all_cases.csv", index=False)
    manifest = {
        "version": args.version,
        "created": _now(),
        "dataset": args.dataset,
        "cache": str(_cache_dir(args.cache)),
        "preset": args.preset,
        "ladder": list(ladder),
        "metrics": asdict(metrics),
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(
        " ".join(
            [
                f"Reweight saved: {out_dir}",
                f"AC@1={metrics.ac1:.6f}",
                f"AC@3={metrics.ac3:.6f}",
                f"AC@5={metrics.ac5:.6f}",
                f"MRR={metrics.mrr:.6f}",
            ]
        )
    )


def _float_list(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def cmd_scan(args: argparse.Namespace) -> None:
    features, edges = _load_cache(args.cache)
    labels = _load_labels(_repo_path(args.labels), args.dataset)
    cached_cases = _prepare_cached_cases(features, edges)
    background_values = (
        _float_list(args.background_values)
        if args.background_values
        else [float(args.background)]
    )
    baseline_values = (
        _float_list(args.baseline_values)
        if args.baseline_values
        else [float(args.baseline)]
    )
    support_values = (
        _float_list(args.support_values)
        if args.support_values
        else [float(args.support)]
    )
    local_values = (
        _float_list(args.local_values)
        if args.local_values
        else [float(args.local)]
    )
    rows: list[dict[str, Any]] = []

    for background in background_values:
        for baseline in baseline_values:
            for support in support_values:
                for local in local_values:
                    for high in _float_list(args.high_values):
                        for root in _float_list(args.root_values):
                            for critical in _float_list(args.critical_values):
                                ladder = (
                                    0.0,
                                    background,
                                    baseline,
                                    support,
                                    local,
                                    high,
                                    root,
                                    critical,
                                )
                                if any(right < left for left, right in zip(ladder, ladder[1:])):
                                    continue
                                _rankings, cases = _rank_prepared_cases(
                                    cached_cases,
                                    labels,
                                    args.dataset,
                                    ladder,
                                    args.top_k,
                                )
                                metrics = _metrics(cases)
                                rows.append(
                                    {
                                        "background": background,
                                        "baseline": baseline,
                                        "support": support,
                                        "local": local,
                                        "high": high,
                                        "root": root,
                                        "critical": critical,
                                        **asdict(metrics),
                                    }
                                )

    result = pd.DataFrame(rows).sort_values(
        ["ac1", "mrr", "ac3", "ac5"],
        ascending=[False, False, False, False],
        kind="stable",
    )
    out_dir = REWEIGHT_ROOT / args.version
    if out_dir.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite scan output: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(out_dir / "scan.csv", index=False)
    manifest = {
        "version": args.version,
        "created": _now(),
        "dataset": args.dataset,
        "cache": str(_cache_dir(args.cache)),
        "fixed": {
            "background": background_values,
            "baseline": baseline_values,
            "support": support_values,
            "local": local_values,
        },
        "high_values": _float_list(args.high_values),
        "root_values": _float_list(args.root_values),
        "critical_values": _float_list(args.critical_values),
        "rows": len(result),
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    best = result.iloc[0] if not result.empty else None
    if best is None:
        print(f"Scan saved: {out_dir} (no valid ladders)")
    else:
        print(
            f"Scan saved: {out_dir} rows={len(result)} "
            f"best=({best['background']},{best['baseline']},{best['support']},"
            f"{best['local']},{best['high']},{best['root']},{best['critical']}) "
            f"AC@1={best['ac1']:.6f} MRR={best['mrr']:.6f}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    dump = subparsers.add_parser("dump", help="Dump raw EvidenceRank feature matrices")
    dump.add_argument("--version", required=True)
    dump.add_argument("--dataset", default="rcabench")
    dump.add_argument("--data-root", default=str(DEFAULT_DATA_ROOT.relative_to(REPO_ROOT)))
    dump.add_argument("--workers", type=int, default=48)
    dump.add_argument("--force", action="store_true")
    dump.set_defaults(func=cmd_dump)

    reweight = subparsers.add_parser("reweight", help="Re-rank a feature cache")
    reweight.add_argument("--cache", required=True)
    reweight.add_argument("--version", required=True)
    reweight.add_argument("--dataset", default="rcabench")
    reweight.add_argument("--labels", default=str(DEFAULT_LABELS.relative_to(REPO_ROOT)))
    reweight.add_argument("--preset", choices=sorted(LADDER_PRESETS), default="current")
    reweight.add_argument("--weights", help="Eight comma-separated priority weights")
    reweight.add_argument("--top-k", type=int, default=10)
    reweight.add_argument("--force", action="store_true")
    reweight.set_defaults(func=cmd_reweight)

    scan = subparsers.add_parser("scan", help="Grid-scan high/root/critical weights")
    scan.add_argument("--cache", required=True)
    scan.add_argument("--version", required=True)
    scan.add_argument("--dataset", default="rcabench")
    scan.add_argument("--labels", default=str(DEFAULT_LABELS.relative_to(REPO_ROOT)))
    scan.add_argument("--background", type=float, default=1.0)
    scan.add_argument("--baseline", type=float, default=1.0)
    scan.add_argument("--support", type=float, default=1.0)
    scan.add_argument("--local", type=float, default=2.0)
    scan.add_argument("--background-values")
    scan.add_argument("--baseline-values")
    scan.add_argument("--support-values")
    scan.add_argument("--local-values")
    scan.add_argument("--high-values", default="4,5,6,7,8")
    scan.add_argument("--root-values", default="8,10,12")
    scan.add_argument("--critical-values", default="12,15,16,18,20")
    scan.add_argument("--top-k", type=int, default=10)
    scan.add_argument("--force", action="store_true")
    scan.set_defaults(func=cmd_scan)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
