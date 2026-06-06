"""Offline raw-equal top-candidate probe for CREST selector research."""

from __future__ import annotations

import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "algorithms/evidencerank"))

from src.evidencerank.cera import (  # noqa: E402
    ALL_MODALITIES,
    BASE_FEATURE_NAMES,
    MODALITY_FEATURES,
    _apply_parent_context,
    _build_feature_matrix,
    _collect_services_from_frames,
    _load_input_frames,
    _trace_sink_context_weight,
)


REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data/rcabench-platform-v2/data/rcabench"
LABELS = REPO / "data/rcabench-platform-v2/meta/rcabench-csv/labels.csv"
FEATURES = tuple(
    feature
    for feature in BASE_FEATURE_NAMES
    if feature in frozenset().union(
        *(MODALITY_FEATURES[modality] for modality in ALL_MODALITIES)
    )
)


def _clean_matrix(matrix: np.ndarray) -> np.ndarray:
    clean = np.nan_to_num(matrix.astype(np.float64), nan=0.0, posinf=0.0, neginf=0.0)
    return np.maximum(clean, 0.0)


def _top_summary(
    datapack: str,
    variant: str,
    services: list[str],
    scores: np.ndarray,
    gt: set[str],
) -> dict[str, object]:
    order = np.lexsort((np.asarray(services, dtype=object), -scores))
    top_idx = int(order[0])
    second_idx = int(order[1]) if len(order) > 1 else top_idx
    best_rank = 10**9
    for rank, idx in enumerate(order, start=1):
        if services[int(idx)] in gt:
            best_rank = rank
            break
    top_score = float(scores[top_idx])
    second_score = float(scores[second_idx])
    return {
        "datapack": datapack,
        "variant": variant,
        "raw_top1": services[top_idx],
        "raw_top1_hit": services[top_idx] in gt,
        "raw_best_rank": best_rank,
        "raw_top_score": top_score,
        "raw_second_score": second_score,
        "raw_gap": top_score - second_score,
        "raw_gap_ratio": (top_score - second_score) / (abs(top_score) + 1e-9),
    }


def process_case(datapack: str, gt: set[str]) -> list[dict[str, object]]:
    frames = _load_input_frames(DATA / datapack)
    services = _collect_services_from_frames(frames)
    if not services:
        return []
    matrix, trace_edges = _build_feature_matrix(
        frames,
        services,
        FEATURES,
        ALL_MODALITIES,
        normalize=True,
    )
    matrix = _clean_matrix(matrix)
    raw_equal = matrix.sum(axis=1)
    context_weight = _trace_sink_context_weight(services, trace_edges)
    raw_parent = _apply_parent_context(
        services,
        raw_equal,
        trace_edges,
        context_weight,
    )
    return [
        _top_summary(datapack, "raw_equal", services, raw_equal, gt),
        _top_summary(datapack, "raw_equal_parent", services, raw_parent, gt),
    ]


def main() -> None:
    labels = pd.read_csv(LABELS)
    labels = labels[labels["gt.level"] == "service"]
    gt_by_datapack = labels.groupby("datapack")["gt.name"].apply(
        lambda values: set(map(str, values))
    )
    datapacks = sorted(gt_by_datapack.index)
    rows: list[dict[str, object]] = []
    workers = min(32, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(process_case, datapack, gt_by_datapack[datapack]): datapack
            for datapack in datapacks
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            rows.extend(future.result())
            if completed % 100 == 0:
                print(f"done {completed}", flush=True)
    frame = pd.DataFrame(rows)
    output = Path("/tmp/crest_raw_equal_top_probe.parquet")
    frame.to_parquet(output)
    print(f"saved {output}")
    for variant, group in frame.groupby("variant"):
        print(
            f"{variant:18s} top1={group['raw_top1_hit'].mean():.6f} "
            f"best1={(group['raw_best_rank'] == 1).mean():.6f}"
        )


if __name__ == "__main__":
    main()

