#!/usr/bin/env python3
"""Learn EvidenceRank feature priors with self-supervised causal calibration.

The calibration is intentionally label-free. It reuses EvidenceRank's raw
feature extractor, samples pseudo-roots from unlabeled incident topologies, adds
generic root perturbations, adds weaker propagation symptoms to neighboring
services, and optimizes non-negative pairwise ranking weights so the synthetic
root outranks propagated victims and background services.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCERANK_SRC = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(EVIDENCERANK_SRC))

from evidencerank.algorithm import (  # noqa: E402
    ALL_MODALITIES,
    BASE_FEATURE_NAMES,
    _build_feature_matrix,
    _collect_services_from_frames,
    _load_input_frames,
)


DEFAULT_SEED = 20260602
DEFAULT_SAMPLES_PER_CASE = 10
DEFAULT_EPOCHS = 8
DEFAULT_LEARNING_RATE = 0.04
DEFAULT_L2 = 0.002
DEFAULT_MEDIAN_WEIGHT = 1.0
DEFAULT_MAX_RATIO = 24.0
DEFAULT_BACKGROUND_FACTOR = 0.18
DEFAULT_PROPAGATION_DECAY = 0.58
DEFAULT_SCALE_COMPENSATION_EXPONENT = 1.1
DEFAULT_COEFFICIENT_CONTRAST_EXPONENT = 2.0
WEIGHTLESS_FEATURE_PREFIXES = ("topology_",)


ROOT_PROFILES: dict[str, dict[str, float]] = {
    "metric_shift": {
        "metric_max_z": 2.2,
        "metric_mean_z": 1.7,
        "metric_anomaly_count": 1.4,
        "metric_value_delta": 1.0,
        "abnormal_metric_rows": 0.35,
    },
    "availability_loss": {
        "metric_count_drop_shift": 10.0,
        "trace_count_drop_shift": 0.4,
        "metric_anomaly_count": 0.7,
        "metric_max_z": 0.5,
    },
    "protocol_shift": {
        "trace_status_code_shift": 4.6,
        "trace_endpoint_shift": 1.7,
        "trace_count_rise_shift": 1.2,
        "trace_error_rate": 0.8,
        "trace_self_duration_relative_shift": 0.45,
    },
    "endpoint_mix_shift": {
        "trace_endpoint_shift": 2.8,
        "trace_count_rise_shift": 2.1,
        "trace_status_code_shift": 1.5,
        "trace_count_delta": 0.55,
        "abnormal_trace_rows": 0.35,
    },
    "local_latency": {
        "trace_self_duration_relative_shift": 3.0,
        "trace_duration_z": 1.35,
        "trace_duration_delta": 0.8,
        "trace_endpoint_shift": 0.55,
    },
    "log_template_shift": {
        "log_template_delta": 1.7,
        "log_error_rate": 0.8,
        "log_count_delta": 0.65,
        "trace_status_code_shift": 0.55,
    },
    "volume_saturation": {
        "trace_count_rise_shift": 2.6,
        "trace_endpoint_shift": 1.15,
        "trace_count_delta": 0.8,
        "metric_max_z": 0.9,
        "abnormal_trace_rows": 0.55,
        "abnormal_metric_rows": 0.35,
    },
}

DOWNSTREAM_PROPAGATION_PROFILE: dict[str, float] = {
    "trace_duration_z": 1.0,
    "trace_duration_delta": 0.85,
    "trace_count_delta": 1.2,
    "trace_count_rise_shift": 1.1,
    "trace_count_drop_shift": 0.7,
    "trace_endpoint_shift": 0.9,
    "log_count_delta": 0.75,
    "log_template_delta": 0.45,
    "log_error_rate": 0.25,
    "abnormal_trace_rows": 0.9,
    "abnormal_metric_rows": 0.15,
}

UPSTREAM_PROPAGATION_PROFILE: dict[str, float] = {
    "trace_duration_z": 0.55,
    "trace_duration_delta": 0.45,
    "trace_count_delta": 0.95,
    "trace_count_rise_shift": 0.9,
    "trace_endpoint_shift": 0.85,
    "log_count_delta": 0.45,
    "abnormal_trace_rows": 0.75,
}


@dataclass(frozen=True)
class CasePack:
    case_name: str
    services: tuple[str, ...]
    matrix: np.ndarray
    edges: tuple[tuple[str, str], ...]


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _repo_path(path: str | Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else REPO_ROOT / value


def _relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path)


def _incident_dirs(root: Path) -> list[Path]:
    return sorted({path.parent for path in root.glob("*/normal_metrics.parquet")})


def _load_case_pack(case_dir: Path) -> CasePack | None:
    frames = _load_input_frames(case_dir)
    services = tuple(_collect_services_from_frames(frames))
    if len(services) < 2:
        return None
    matrix, edges = _build_feature_matrix(
        frames,
        list(services),
        BASE_FEATURE_NAMES,
        ALL_MODALITIES,
    )
    clean = np.nan_to_num(
        matrix.astype("float64"),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    if clean.shape[0] < 2 or clean.shape[1] != len(BASE_FEATURE_NAMES):
        return None
    return CasePack(
        case_name=case_dir.name,
        services=services,
        matrix=clean,
        edges=tuple((str(parent), str(child)) for parent, child in edges),
    )


def _load_case_packs(case_dirs: list[Path], workers: int) -> list[CasePack]:
    packs: list[CasePack] = []
    if workers <= 1:
        for idx, case_dir in enumerate(case_dirs, start=1):
            pack = _load_case_pack(case_dir)
            if pack is not None:
                packs.append(pack)
            if idx % 50 == 0:
                print(f"loaded {idx}/{len(case_dirs)} incidents", file=sys.stderr)
        return packs

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_load_case_pack, path): path for path in case_dirs}
        for idx, future in enumerate(as_completed(futures), start=1):
            pack = future.result()
            if pack is not None:
                packs.append(pack)
            if idx % 50 == 0:
                print(f"loaded {idx}/{len(case_dirs)} incidents", file=sys.stderr)
    return sorted(packs, key=lambda pack: pack.case_name)


def _feature_scales(packs: list[CasePack]) -> np.ndarray:
    per_case: list[np.ndarray] = []
    for pack in packs:
        scales = np.zeros(len(BASE_FEATURE_NAMES), dtype=np.float64)
        for idx in range(pack.matrix.shape[1]):
            positive = pack.matrix[:, idx][pack.matrix[:, idx] > 0.0]
            if positive.size:
                scales[idx] = float(np.percentile(positive, 95))
        per_case.append(scales)

    stacked = np.vstack(per_case)
    result = np.zeros(len(BASE_FEATURE_NAMES), dtype=np.float64)
    for idx in range(stacked.shape[1]):
        positive = stacked[:, idx][stacked[:, idx] > 0.0]
        if positive.size:
            result[idx] = float(np.median(positive))
        else:
            result[idx] = 1.0
    return np.clip(result, 0.05, 12.0)


def _profile_vector(profile: dict[str, float], scales: np.ndarray) -> np.ndarray:
    vector = np.zeros(len(BASE_FEATURE_NAMES), dtype=np.float64)
    for feature, strength in profile.items():
        if feature not in BASE_FEATURE_NAMES:
            continue
        vector[BASE_FEATURE_NAMES.index(feature)] = float(strength)
    return vector * scales


def _adjacency(services: tuple[str, ...], edges: tuple[tuple[str, str], ...]) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    service_to_idx = {service: idx for idx, service in enumerate(services)}
    children: dict[int, list[int]] = {idx: [] for idx in range(len(services))}
    parents: dict[int, list[int]] = {idx: [] for idx in range(len(services))}
    for parent, child in edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)
        if parent_idx is None or child_idx is None or parent_idx == child_idx:
            continue
        children[parent_idx].append(child_idx)
        parents[child_idx].append(parent_idx)
    return children, parents


def _expand(
    start: int,
    graph: dict[int, list[int]],
    max_hops: int,
) -> dict[int, int]:
    seen = {start: 0}
    frontier = [start]
    for hop in range(1, max_hops + 1):
        next_frontier: list[int] = []
        for node in frontier:
            for neighbor in graph.get(node, []):
                if neighbor in seen:
                    continue
                seen[neighbor] = hop
                next_frontier.append(neighbor)
        frontier = next_frontier
        if not frontier:
            break
    seen.pop(start, None)
    return seen


def _synthetic_diffs(
    pack: CasePack,
    scales: np.ndarray,
    rng: np.random.Generator,
    samples_per_case: int,
    background_factor: float,
    propagation_decay: float,
) -> list[np.ndarray]:
    service_count = len(pack.services)
    if service_count < 2:
        return []

    children, parents = _adjacency(pack.services, pack.edges)
    down_vector = _profile_vector(DOWNSTREAM_PROPAGATION_PROFILE, scales)
    up_vector = _profile_vector(UPSTREAM_PROPAGATION_PROFILE, scales)
    operator_names = tuple(ROOT_PROFILES.keys())
    diffs: list[np.ndarray] = []

    for _ in range(samples_per_case):
        root_idx = int(rng.integers(0, service_count))
        operator = operator_names[int(rng.integers(0, len(operator_names)))]
        root_vector = _profile_vector(ROOT_PROFILES[operator], scales)
        amplitude = float(rng.uniform(0.7, 1.45))
        base = pack.matrix * background_factor
        synthetic = base.copy()
        synthetic[root_idx] += root_vector * amplitude

        downstream = _expand(root_idx, children, max_hops=2)
        upstream = _expand(root_idx, parents, max_hops=1)
        for node, hop in downstream.items():
            synthetic[node] += down_vector * amplitude * (propagation_decay ** max(hop - 1, 0))
        for node, hop in upstream.items():
            synthetic[node] += up_vector * amplitude * (propagation_decay ** max(hop - 1, 0))

        root_row = synthetic[root_idx]
        neighbor_negatives = sorted(set(downstream) | set(upstream))
        background_scores = base.sum(axis=1)
        top_background = [
            int(idx)
            for idx in np.argsort(background_scores)[::-1]
            if int(idx) != root_idx
        ][:3]
        random_negatives = [
            int(idx)
            for idx in rng.choice(
                service_count,
                size=min(3, service_count),
                replace=False,
            )
            if int(idx) != root_idx
        ]
        negatives = []
        for idx in [*neighbor_negatives, *top_background, *random_negatives]:
            if idx != root_idx and idx not in negatives:
                negatives.append(idx)
        if not negatives:
            negatives = [idx for idx in range(service_count) if idx != root_idx]

        for negative_idx in negatives:
            diff = root_row - synthetic[negative_idx]
            if np.any(np.abs(diff) > 1e-12):
                diffs.append(diff.astype(np.float64, copy=False))
    return diffs


def _sigmoid_negative_margin(margins: np.ndarray) -> np.ndarray:
    clipped = np.clip(margins, -50.0, 50.0)
    return 1.0 / (1.0 + np.exp(clipped))


def _fit_pairwise_weights(
    packs: list[CasePack],
    scales: np.ndarray,
    samples_per_case: int,
    epochs: int,
    learning_rate: float,
    l2: float,
    background_factor: float,
    propagation_decay: float,
    seed: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    rng = np.random.default_rng(seed)
    feature_count = len(BASE_FEATURE_NAMES)
    weights = np.ones(feature_count, dtype=np.float64)
    weightless = np.asarray([
        any(name.startswith(prefix) for prefix in WEIGHTLESS_FEATURE_PREFIXES)
        for name in BASE_FEATURE_NAMES
    ])
    weights[weightless] = 0.0

    trace: list[dict[str, float]] = []
    total_pairs = 0
    for epoch in range(epochs):
        order = rng.permutation(len(packs))
        epoch_pairs = 0
        epoch_loss = 0.0
        epoch_accuracy = 0.0
        epoch_batches = 0

        for pack_idx in order:
            diffs = _synthetic_diffs(
                packs[int(pack_idx)],
                scales,
                rng,
                samples_per_case,
                background_factor,
                propagation_decay,
            )
            if not diffs:
                continue
            batch = np.vstack(diffs)
            margins = batch @ weights
            factors = _sigmoid_negative_margin(margins)
            gradient = -(factors[:, None] * batch).mean(axis=0)
            gradient += l2 * weights
            weights -= learning_rate * gradient
            weights = np.maximum(weights, 0.0)
            weights[weightless] = 0.0

            epoch_pairs += int(batch.shape[0])
            epoch_loss += float(np.log1p(np.exp(-np.clip(margins, -50.0, 50.0))).mean())
            epoch_accuracy += float((margins > 0.0).mean())
            epoch_batches += 1

        total_pairs += epoch_pairs
        trace.append({
            "epoch": float(epoch + 1),
            "pairs": float(epoch_pairs),
            "mean_loss": epoch_loss / max(epoch_batches, 1),
            "pair_accuracy": epoch_accuracy / max(epoch_batches, 1),
        })

    diagnostics = {
        "total_pairs": total_pairs,
        "epoch_trace": trace,
    }
    return weights, diagnostics


def _normalize_weights(
    raw_weights: np.ndarray,
    scales: np.ndarray,
    median_weight: float,
    max_ratio: float,
    scale_compensation_exponent: float,
    coefficient_contrast_exponent: float,
) -> np.ndarray:
    weights = np.maximum(raw_weights.astype(np.float64, copy=True), 0.0)
    weightless = np.asarray([
        any(name.startswith(prefix) for prefix in WEIGHTLESS_FEATURE_PREFIXES)
        for name in BASE_FEATURE_NAMES
    ])
    weights = (weights ** coefficient_contrast_exponent) / (
        np.clip(scales, 0.05, None) ** scale_compensation_exponent
    )
    weights[weightless] = 0.0
    scoring = (~weightless) & (weights > 0.0)
    if not scoring.any():
        raise SystemExit("No positive scoring weights were learned.")
    median = float(np.median(weights[scoring]))
    weights = weights / max(median, 1e-9) * median_weight
    lower = median_weight / max_ratio
    upper = median_weight * max_ratio
    weights[~weightless] = np.clip(weights[~weightless], lower, upper)
    weights[weightless] = 0.0
    return weights


def _feature_table(
    raw_weights: np.ndarray,
    calibrated_weights: np.ndarray,
    scales: np.ndarray,
    scale_compensation_exponent: float,
    coefficient_contrast_exponent: float,
) -> pd.DataFrame:
    rows = []
    for idx, feature in enumerate(BASE_FEATURE_NAMES):
        calibration_strength = (
            max(float(raw_weights[idx]), 0.0) ** coefficient_contrast_exponent
            / (max(float(scales[idx]), 0.05) ** scale_compensation_exponent)
        )
        rows.append({
            "feature": feature,
            "raw_weight": float(raw_weights[idx]),
            "calibration_strength": float(calibration_strength),
            "calibrated_weight": float(calibrated_weights[idx]),
            "feature_scale": float(scales[idx]),
        })
    return pd.DataFrame(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Self-supervised causal calibration for EvidenceRank weights."
    )
    parser.add_argument(
        "--data-root",
        required=True,
        help="Directory containing unlabeled incident folders with raw parquet frames.",
    )
    parser.add_argument("--out", help="Optional JSON calibration artifact path.")
    parser.add_argument("--csv", help="Optional CSV feature-weight table path.")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--samples-per-case", type=int, default=DEFAULT_SAMPLES_PER_CASE)
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    parser.add_argument("--learning-rate", type=float, default=DEFAULT_LEARNING_RATE)
    parser.add_argument("--l2", type=float, default=DEFAULT_L2)
    parser.add_argument("--median-weight", type=float, default=DEFAULT_MEDIAN_WEIGHT)
    parser.add_argument("--max-ratio", type=float, default=DEFAULT_MAX_RATIO)
    parser.add_argument("--background-factor", type=float, default=DEFAULT_BACKGROUND_FACTOR)
    parser.add_argument("--propagation-decay", type=float, default=DEFAULT_PROPAGATION_DECAY)
    parser.add_argument("--scale-compensation-exponent", type=float, default=DEFAULT_SCALE_COMPENSATION_EXPONENT)
    parser.add_argument("--coefficient-contrast-exponent", type=float, default=DEFAULT_COEFFICIENT_CONTRAST_EXPONENT)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    data_root = _repo_path(args.data_root)
    case_dirs = _incident_dirs(data_root)
    if not case_dirs:
        raise SystemExit(f"No incident folders found under {data_root}")

    packs = _load_case_packs(case_dirs, args.workers)
    if not packs:
        raise SystemExit("No usable incident feature matrices were produced.")

    scales = _feature_scales(packs)
    raw_weights, diagnostics = _fit_pairwise_weights(
        packs,
        scales,
        samples_per_case=args.samples_per_case,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        l2=args.l2,
        background_factor=args.background_factor,
        propagation_decay=args.propagation_decay,
        seed=args.seed,
    )
    calibrated_weights = _normalize_weights(
        raw_weights,
        scales,
        median_weight=args.median_weight,
        max_ratio=args.max_ratio,
        scale_compensation_exponent=args.scale_compensation_exponent,
        coefficient_contrast_exponent=args.coefficient_contrast_exponent,
    )
    table = _feature_table(
        raw_weights,
        calibrated_weights,
        scales,
        scale_compensation_exponent=args.scale_compensation_exponent,
        coefficient_contrast_exponent=args.coefficient_contrast_exponent,
    )
    weights = {
        row.feature: float(row.calibrated_weight)
        for row in table.itertuples(index=False)
    }
    payload = {
        "created": _now(),
        "data_root": _relative(data_root),
        "incident_count": len(case_dirs),
        "usable_incident_count": len(packs),
        "method": {
            "name": "self_supervised_causal_pairwise_calibration",
            "labels_used": False,
            "ground_truth_used": False,
            "objective": "learn non-negative weights so synthetic pseudo-roots outrank topology-propagated victims and high-background services",
            "root_profiles": ROOT_PROFILES,
            "downstream_propagation_profile": DOWNSTREAM_PROPAGATION_PROFILE,
            "upstream_propagation_profile": UPSTREAM_PROPAGATION_PROFILE,
            "weightless_feature_prefixes": WEIGHTLESS_FEATURE_PREFIXES,
        },
        "parameters": {
            "seed": args.seed,
            "samples_per_case": args.samples_per_case,
            "epochs": args.epochs,
            "learning_rate": args.learning_rate,
            "l2": args.l2,
            "median_weight": args.median_weight,
            "max_ratio": args.max_ratio,
            "background_factor": args.background_factor,
            "propagation_decay": args.propagation_decay,
            "scale_compensation_exponent": args.scale_compensation_exponent,
            "coefficient_contrast_exponent": args.coefficient_contrast_exponent,
        },
        "diagnostics": diagnostics,
        "weights": weights,
        "feature_stats": table.to_dict(orient="records"),
    }

    if args.out:
        _write_json(_repo_path(args.out), payload)
    if args.csv:
        csv_path = _repo_path(args.csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(csv_path, index=False)

    print(
        table.sort_values("calibrated_weight", ascending=False).to_string(
            index=False,
            float_format=lambda value: f"{value:.6f}",
        )
    )
    print(json.dumps(diagnostics["epoch_trace"][-1], sort_keys=True), file=sys.stderr)


if __name__ == "__main__":
    main()
