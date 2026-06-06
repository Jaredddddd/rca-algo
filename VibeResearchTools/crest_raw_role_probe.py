"""Offline CREST raw-feature role probe.

This script is research-only. It reads labels only to compute metrics and must
not be imported from the runtime algorithm path.
"""

from __future__ import annotations

import math
import os
import sys
from collections import defaultdict
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


def _positive_rank_view(matrix: np.ndarray) -> np.ndarray:
    ranks = np.zeros_like(matrix, dtype=np.float64)
    for column_idx in range(matrix.shape[1]):
        column = matrix[:, column_idx]
        positive_idx = np.flatnonzero(column > 0.0)
        if positive_idx.size == 0:
            continue
        ordered = positive_idx[np.argsort(column[positive_idx], kind="mergesort")]
        ranks[ordered, column_idx] = (
            np.arange(1, positive_idx.size + 1, dtype=np.float64)
            / float(positive_idx.size)
        )
    return ranks


def _feature_stats(
    matrix: np.ndarray,
    services: list[str],
    trace_edges: list[tuple[str, str]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    service_to_idx = {service: idx for idx, service in enumerate(services)}
    concentration = np.zeros(matrix.shape[1], dtype=np.float64)
    gap = np.zeros(matrix.shape[1], dtype=np.float64)
    upstream_ratio = np.full(matrix.shape[1], 0.5, dtype=np.float64)
    sink_ratio = np.zeros(matrix.shape[1], dtype=np.float64)

    parent_nodes = {parent for parent, child in trace_edges if parent != child}
    child_nodes = {child for parent, child in trace_edges if parent != child}
    sink_indices = [
        service_to_idx[service]
        for service in sorted(child_nodes - parent_nodes)
        if service in service_to_idx
    ]
    source_indices = [
        service_to_idx[service]
        for service in sorted(parent_nodes)
        if service in service_to_idx
    ]

    for column_idx in range(matrix.shape[1]):
        column = matrix[:, column_idx]
        positive = column[column > 0.0]
        if positive.size == 0:
            continue

        max_value = float(np.max(positive))
        concentration[column_idx] = max_value / (float(np.mean(positive)) + 1e-9)
        if positive.size > 1:
            sorted_positive = np.sort(positive)
            gap[column_idx] = max(
                0.0,
                (float(sorted_positive[-1]) - float(sorted_positive[-2]))
                / (max_value + 1e-9),
            )
        else:
            gap[column_idx] = 1.0

        upstream = 0.0
        downstream = 0.0
        for parent, child in trace_edges:
            parent_idx = service_to_idx.get(parent)
            child_idx = service_to_idx.get(child)
            if parent_idx is None or child_idx is None or parent_idx == child_idx:
                continue
            delta = float(column[parent_idx] - column[child_idx])
            if delta >= 0.0:
                upstream += delta
            else:
                downstream -= delta
        if upstream > 0.0 or downstream > 0.0:
            upstream_ratio[column_idx] = upstream / (upstream + downstream + 1e-9)

        sink_mean = float(np.mean(column[sink_indices])) if sink_indices else 0.0
        source_mean = float(np.mean(column[source_indices])) if source_indices else 0.0
        sink_ratio[column_idx] = sink_mean / (sink_mean + source_mean + 1e-9)

    def normalize(values: np.ndarray, default: float = 0.0) -> np.ndarray:
        finite = np.nan_to_num(values, nan=default, posinf=default, neginf=default)
        positive = finite[finite > 0.0]
        if positive.size == 0:
            return np.zeros_like(finite)
        scale = float(np.median(positive))
        if scale <= 1e-12:
            scale = float(np.max(positive))
        return np.clip(finite / (scale + 1e-9), 0.0, 6.0)

    return normalize(concentration), np.clip(gap, 0.0, 1.0), upstream_ratio, sink_ratio


def _best_rank(services: list[str], scores: np.ndarray, gt: set[str]) -> int:
    order = np.lexsort((np.asarray(services, dtype=object), -scores))
    for rank, service_idx in enumerate(order, start=1):
        if services[int(service_idx)] in gt:
            return rank
    return 10**9


def _role_scores(
    matrix: np.ndarray,
    services: list[str],
    trace_edges: list[tuple[str, str]],
    concentration_power: float,
    upstream_power: float,
    gap_power: float,
    transfer_weight: float,
    victim_penalty: float,
) -> np.ndarray:
    concentration, gap, upstream_ratio, sink_ratio = _feature_stats(
        matrix,
        services,
        trace_edges,
    )
    root_weight = (
        np.power(0.25 + concentration, concentration_power)
        * np.power(0.25 + gap, gap_power)
        * np.power(0.25 + upstream_ratio, upstream_power)
    )
    victim_weight = (
        np.power(0.25 + concentration, concentration_power)
        * np.power(0.25 + (1.0 - upstream_ratio), upstream_power)
        * (0.5 + sink_ratio)
    )
    positive_root = root_weight[root_weight > 0.0]
    positive_victim = victim_weight[victim_weight > 0.0]
    if positive_root.size:
        root_weight = root_weight / (float(np.median(positive_root)) + 1e-9)
    if positive_victim.size:
        victim_weight = victim_weight / (float(np.median(positive_victim)) + 1e-9)

    root = matrix @ np.clip(root_weight, 0.0, 12.0)
    victim = matrix @ np.clip(victim_weight, 0.0, 12.0)

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    transfer = np.zeros(len(services), dtype=np.float64)
    for parent, child in trace_edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)
        if parent_idx is None or child_idx is None or parent_idx == child_idx:
            continue
        parent_root = float(root[parent_idx])
        child_root = float(root[child_idx])
        child_victim_excess = max(0.0, float(victim[child_idx] - victim[parent_idx]))
        if parent_root <= 0.0 or child_victim_excess <= 0.0:
            continue
        root_share = parent_root / (parent_root + child_root + 1e-9)
        transfer[parent_idx] += child_victim_excess * root_share

    root_positive = root[root > 0.0]
    victim_positive = victim[victim > 0.0]
    if root_positive.size:
        root_scaled = root / (float(np.percentile(root_positive, 95)) + 1e-9)
    else:
        root_scaled = root
    if victim_positive.size:
        victim_scaled = victim / (float(np.percentile(victim_positive, 95)) + 1e-9)
    else:
        victim_scaled = victim
    victim_only = np.maximum(victim_scaled - root_scaled, 0.0)
    return root + transfer_weight * transfer - victim_penalty * victim_only


def process_case(datapack: str, gt: set[str]) -> dict[str, int | str]:
    frames = _load_input_frames(DATA / datapack)
    services = _collect_services_from_frames(frames)
    if not services:
        return {"datapack": datapack}

    matrix, trace_edges = _build_feature_matrix(
        frames,
        services,
        FEATURES,
        ALL_MODALITIES,
        normalize=True,
    )
    matrix = _clean_matrix(matrix)
    rank_matrix = _positive_rank_view(matrix)
    context_weight = _trace_sink_context_weight(services, trace_edges)

    variants: dict[str, np.ndarray] = {
        "raw_equal": matrix.sum(axis=1),
        "rank_equal": rank_matrix.sum(axis=1),
    }
    for concentration_power in (0.0, 0.5, 1.0):
        for upstream_power in (0.5, 1.0, 2.0):
            for gap_power in (0.0, 0.5, 1.0):
                for transfer_weight in (0.0, 0.25, 0.5, 1.0):
                    for victim_penalty in (0.0, 0.1, 0.25, 0.5):
                        name = (
                            f"role_c{concentration_power}_u{upstream_power}"
                            f"_g{gap_power}_t{transfer_weight}_p{victim_penalty}"
                        )
                        variants[name] = _role_scores(
                            matrix,
                            services,
                            trace_edges,
                            concentration_power,
                            upstream_power,
                            gap_power,
                            transfer_weight,
                            victim_penalty,
                        )

    result: dict[str, int | str] = {"datapack": datapack}
    for name, scores in variants.items():
        result[name] = _best_rank(services, scores, gt)
        result[f"{name}_parent"] = _best_rank(
            services,
            _apply_parent_context(services, scores, trace_edges, context_weight),
            gt,
        )
    return result


def main() -> None:
    labels = pd.read_csv(LABELS)
    labels = labels[labels["gt.level"] == "service"]
    gt_by_datapack = labels.groupby("datapack")["gt.name"].apply(
        lambda values: set(map(str, values))
    )
    datapacks = sorted(gt_by_datapack.index)

    rows: list[dict[str, int | str]] = []
    workers = min(32, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(process_case, datapack, gt_by_datapack[datapack]): datapack
            for datapack in datapacks
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            rows.append(future.result())
            if completed % 100 == 0:
                print(f"done {completed}", flush=True)

    frame = pd.DataFrame(rows).set_index("datapack").reindex(datapacks)
    output = Path("/tmp/crest_raw_role_probe.parquet")
    frame.to_parquet(output)
    print(f"saved {output}")

    results: list[tuple[float, float, float, float, str]] = []
    for column in sorted(frame.columns):
        best = frame[column].astype(float)
        results.append(
            (
                float((best == 1).mean()),
                float((1.0 / best).mean()),
                float((best <= 3).mean()),
                float((best <= 5).mean()),
                column,
            )
        )
    for ac1, mrr, ac3, ac5, column in sorted(results, reverse=True)[:80]:
        print(
            f"{column:52s} AC@1={ac1:.6f} "
            f"MRR={mrr:.6f} AC@3={ac3:.6f} AC@5={ac5:.6f}"
        )


if __name__ == "__main__":
    main()

