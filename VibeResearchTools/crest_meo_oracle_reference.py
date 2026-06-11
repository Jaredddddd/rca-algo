"""Write benchmark-style reference outputs from a case-indicator Oracle artifact.

The input artifact is intentionally leaky and contains per-case GT indicators.
This script is research-only and must not be imported from runtime algorithms.
For the benchmark-level universal Oracle, use ``crest_meo_universal_oracle.py``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = (
    REPO
    / "output/rcabench-platform-v2/crest_meo_oracle/case_indicator_oracle.json"
)
DEFAULT_OUTPUT_ROOT = REPO / "output/rcabench-platform-v2/data"
DEFAULT_SUMMARY = (
    REPO
    / "output/rcabench-platform-v2/crest_meo_oracle/case_indicator_reference_summary.json"
)


def _repo_path(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else REPO / path


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def _load_artifact(path: Path) -> dict[str, Any]:
    artifact = json.loads(path.read_text(encoding="utf-8"))
    if artifact.get("artifact_type") != "oracle_upper_bound":
        raise SystemExit(f"Not an oracle artifact: {path}")
    if artifact.get("oracle_matrix_encoding") != "broadcast_oracle_indicator_to_all_operators":
        raise SystemExit(
            "Unsupported oracle_matrix_encoding: "
            f"{artifact.get('oracle_matrix_encoding')}"
        )
    return artifact


def _rank_case(
    case: dict[str, Any],
    dataset: str,
    algorithm: str,
    operator_count: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    services = [str(service) for service in case["services"]]
    gt_services = {str(service) for service in case["gt_services"]}
    indicator = np.asarray(case["oracle_indicator"], dtype=np.float64)
    if len(services) != indicator.size:
        raise ValueError(f"indicator length mismatch for {case['datapack']}")

    scores = indicator * float(operator_count)
    order = np.lexsort((np.asarray(services, dtype=object), -scores))
    ordered_services = [services[int(idx)] for idx in order]
    hits = [service in gt_services for service in ordered_services]
    ranks = np.arange(1, len(ordered_services) + 1, dtype=np.uint32)
    best_rank = next(
        (int(rank) for rank, hit in zip(ranks, hits, strict=False) if hit),
        10**9,
    )

    output = pd.DataFrame(
        {
            "level": ["service"] * len(ordered_services),
            "name": ordered_services,
            "rank": ranks,
            "algorithm": [algorithm] * len(ordered_services),
            "dataset": [dataset] * len(ordered_services),
            "datapack": [case["datapack"]] * len(ordered_services),
            "hit": hits,
            "runtime.seconds": [0.0] * len(ordered_services),
            "exception.type": [None] * len(ordered_services),
            "exception.message": [None] * len(ordered_services),
        }
    )

    precision_at: dict[int, float] = {}
    hit_seen_at: dict[int, float] = {}
    for k in range(1, 6):
        top_hits = hits[:k]
        precision_at[k] = float(sum(top_hits)) / float(k)
        hit_seen_at[k] = 1.0 if best_rank <= k else 0.0

    mrr = 1.0 / float(best_rank) if best_rank < 10**9 else 0.0
    perf = pd.DataFrame(
        {
            "algorithm": [algorithm],
            "dataset": [dataset],
            "datapack": [case["datapack"]],
            "total": np.asarray([1], dtype=np.uint32),
            "error": np.asarray([0], dtype=np.uint32),
            "runtime.seconds:avg": [0.0],
            "rank": np.asarray([best_rank], dtype=np.uint32),
            "MRR": [mrr],
            "AC@1.count": [hit_seen_at[1]],
            "AC@2.count": [hit_seen_at[2]],
            "AC@3.count": [hit_seen_at[3]],
            "AC@4.count": [hit_seen_at[4]],
            "AC@5.count": [hit_seen_at[5]],
            "AC@1": [hit_seen_at[1]],
            "AC@2": [hit_seen_at[2]],
            "AC@3": [hit_seen_at[3]],
            "AC@4": [hit_seen_at[4]],
            "AC@5": [hit_seen_at[5]],
            "Avg@1": [hit_seen_at[1]],
            "Avg@2": [hit_seen_at[2]],
            "Avg@3": [hit_seen_at[3]],
            "Avg@4": [hit_seen_at[4]],
            "Avg@5": [hit_seen_at[5]],
            "P@1": [precision_at[1]],
            "P@2": [precision_at[2]],
            "P@3": [precision_at[3]],
            "P@4": [precision_at[4]],
            "P@5": [precision_at[5]],
            "AP@1": [hit_seen_at[1]],
            "AP@2": [hit_seen_at[2]],
            "AP@3": [hit_seen_at[3]],
            "AP@4": [hit_seen_at[4]],
            "AP@5": [hit_seen_at[5]],
        }
    )
    summary = {
        "datapack": case["datapack"],
        "best_rank": best_rank,
        "top1": ordered_services[0] if ordered_services else None,
        "hit1": bool(best_rank == 1),
        "service_count": len(services),
        "gt_count": len(gt_services),
    }
    return output, perf, summary


def _aggregate(case_summaries: list[dict[str, Any]]) -> dict[str, float | int]:
    ranks = [float(item["best_rank"]) for item in case_summaries]
    if not ranks:
        return {
            "total": 0,
            "error": 0,
            "AC@1": 0.0,
            "MRR": 0.0,
            "AC@3": 0.0,
            "AC@5": 0.0,
        }
    return {
        "total": len(ranks),
        "error": 0,
        "AC@1": sum(1 for rank in ranks if rank <= 1.0) / len(ranks),
        "MRR": sum(1.0 / rank for rank in ranks) / len(ranks),
        "AC@3": sum(1 for rank in ranks if rank <= 3.0) / len(ranks),
        "AC@5": sum(1 for rank in ranks if rank <= 5.0) / len(ranks),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Write CREST-MEO Oracle reference predictions from an oracle artifact."
    )
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--algorithm", default="crest_meo_oracle")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--limit", type=int, default=None)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    artifact_path = _repo_path(args.artifact)
    output_root = _repo_path(args.output_root)
    summary_path = _repo_path(args.summary)

    artifact = _load_artifact(artifact_path)
    dataset = args.dataset or str(artifact["dataset"])
    cases = list(artifact["cases"])
    if args.limit is not None:
        cases = cases[: max(0, args.limit)]
    operator_count = int(artifact["operator_count"])

    case_summaries: list[dict[str, Any]] = []
    for idx, case in enumerate(cases, start=1):
        output, perf, case_summary = _rank_case(
            case,
            dataset,
            args.algorithm,
            operator_count,
        )
        target = output_root / dataset / str(case["datapack"]) / args.algorithm
        target.mkdir(parents=True, exist_ok=True)
        output.to_parquet(target / "output.parquet", index=False)
        perf.to_parquet(target / "perf.parquet", index=False)
        case_summaries.append(case_summary)
        if idx % 100 == 0:
            print(f"wrote {idx}/{len(cases)}", flush=True)

    summary = {
        "algorithm": args.algorithm,
        "dataset": dataset,
        "artifact": _relative(artifact_path),
        "output_root": _relative(output_root),
        "operator_count": operator_count,
        "oracle_matrix_encoding": artifact["oracle_matrix_encoding"],
        "metrics": _aggregate(case_summaries),
        "case_summaries": case_summaries,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"saved {summary_path.relative_to(REPO) if summary_path.is_relative_to(REPO) else summary_path}")
    print(json.dumps(summary["metrics"], sort_keys=True))


if __name__ == "__main__":
    main()
