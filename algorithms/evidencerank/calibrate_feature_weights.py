#!/usr/bin/env python3
"""Calibrate EvidenceRank feature priors from unlabeled incident folders.

This utility is intentionally offline. It reads the same raw observability
frames used by EvidenceRank, estimates global feature reliability without
labels, and emits a reproducible calibration artifact.
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
    FEATURE_WEIGHTS,
    MODALITY_FEATURES,
    _build_feature_matrix,
    _collect_services_from_frames,
    _load_input_frames,
)


MIN_ACTIVE_SERVICES = 1
DEFAULT_MEDIAN_WEIGHT = 1.0
DEFAULT_MAX_RATIO = 24.0
DEFAULT_SCALE_EXPONENT = 0.9
DEFAULT_ACTIVE_EXPONENT = 0.15
WEIGHTLESS_FEATURE_PREFIXES = ("topology_",)


@dataclass(frozen=True)
class FeatureObservation:
    feature: str
    positive_services: int
    peak: float
    p95: float
    median: float
    concentration: float
    contrast: float
    top_gap: float
    peak_separation: float
    support: float
    agreement: float
    top_agreement: float


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _repo_path(path: str | Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else REPO_ROOT / value


def _incident_dirs(root: Path) -> list[Path]:
    return sorted({path.parent for path in root.glob("*/normal_metrics.parquet")})


def _concentration(values: np.ndarray) -> float:
    if values.size <= 0:
        return 0.0
    if values.size == 1:
        return 1.0
    total = float(values.sum())
    if total <= 0.0 or not math.isfinite(total):
        return 0.0
    probabilities = values / total
    entropy = -float(np.sum(probabilities * np.log(probabilities + 1e-12)))
    return min(1.0, max(0.0, 1.0 - entropy / math.log(float(values.size))))


def _cosine(left: np.ndarray, right: np.ndarray) -> float | None:
    left_norm = float(np.linalg.norm(left))
    right_norm = float(np.linalg.norm(right))
    if left_norm <= 0.0 or right_norm <= 0.0:
        return None
    return float(np.dot(left, right) / (left_norm * right_norm))


def _top_agreement(vector: np.ndarray, peer: np.ndarray) -> float:
    if float(peer.sum()) <= 0.0 or float(vector.sum()) <= 0.0:
        return 0.0
    top_idx = int(np.argmax(vector))
    peer_order = np.argsort(peer)[::-1]
    rank_positions = np.where(peer_order == top_idx)[0]
    if rank_positions.size == 0:
        return 0.0
    rank = int(rank_positions[0]) + 1
    return 1.0 / min(rank, 10)


def _case_observations(case_dir: Path) -> list[dict[str, Any]]:
    frames = _load_input_frames(case_dir)
    services = _collect_services_from_frames(frames)
    if not services:
        return []

    matrix, _edges = _build_feature_matrix(
        frames,
        services,
        BASE_FEATURE_NAMES,
        ALL_MODALITIES,
    )
    clean = np.nan_to_num(
        matrix.astype("float64"),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    normalized = np.zeros_like(clean)
    active_indices: list[int] = []

    for idx in range(clean.shape[1]):
        column = clean[:, idx]
        positive = column[column > 0.0]
        if positive.size < MIN_ACTIVE_SERVICES:
            continue
        p95 = float(np.percentile(positive, 95))
        if p95 <= 0.0 or not math.isfinite(p95):
            continue
        normalized[:, idx] = np.clip(column / (p95 + 1e-9), 0.0, 1.0)
        active_indices.append(idx)

    if not active_indices:
        return []

    feature_to_modality = {
        feature: modality
        for modality, feature_names in MODALITY_FEATURES.items()
        for feature in feature_names
    }
    all_consensus = normalized[:, active_indices].sum(axis=1)
    modality_consensus: dict[str, np.ndarray] = {}
    for modality, feature_names in MODALITY_FEATURES.items():
        indices = [
            BASE_FEATURE_NAMES.index(feature)
            for feature in feature_names
            if feature in BASE_FEATURE_NAMES
        ]
        indices = [idx for idx in indices if idx in active_indices]
        if indices:
            modality_consensus[modality] = normalized[:, indices].sum(axis=1)

    observations: list[dict[str, Any]] = []
    for idx, feature in enumerate(BASE_FEATURE_NAMES):
        column = clean[:, idx]
        positive = column[column > 0.0]
        if positive.size < MIN_ACTIVE_SERVICES:
            continue

        sorted_positive = np.sort(positive)[::-1]
        peak = float(sorted_positive[0])
        second = float(sorted_positive[1]) if sorted_positive.size > 1 else 0.0
        median = float(np.median(positive))
        p75 = float(np.percentile(positive, 75))
        p95 = float(np.percentile(positive, 95))

        modality = feature_to_modality.get(feature)
        cross_consensus = all_consensus.copy()
        if modality in modality_consensus:
            cross_consensus = cross_consensus - modality_consensus[modality]
        peer_consensus = (
            cross_consensus
            if float(cross_consensus.sum()) > 0.0
            else all_consensus - normalized[:, idx]
        )
        agreement = _cosine(normalized[:, idx], peer_consensus)
        if agreement is None:
            agreement = 0.0

        observation = FeatureObservation(
            feature=feature,
            positive_services=int(positive.size),
            peak=peak,
            p95=p95,
            median=median,
            concentration=_concentration(positive),
            contrast=max(0.0, min(1.0, (p95 - median) / (p95 + median + 1e-9))),
            top_gap=max(0.0, min(1.0, (peak - second) / (peak + second + 1e-9))),
            peak_separation=max(0.0, min(1.0, (peak - p75) / (peak + p75 + 1e-9))),
            support=min(1.0, math.sqrt(float(positive.size) / 3.0)),
            agreement=max(0.0, min(1.0, agreement)),
            top_agreement=_top_agreement(normalized[:, idx], peer_consensus),
        )
        observations.append(observation.__dict__)
    return observations


def _aggregate(observations: list[dict[str, Any]], total_cases: int) -> pd.DataFrame:
    if not observations:
        raise SystemExit("No feature observations were produced.")

    data = pd.DataFrame(observations)
    rows: list[dict[str, Any]] = []
    for feature in BASE_FEATURE_NAMES:
        group = data[data["feature"] == feature]
        if group.empty:
            rows.append({
                "feature": feature,
                "active_cases": 0,
                "active_rate": 0.0,
                "quality": 0.0,
                "median_peak": 0.0,
                "median_p95": 0.0,
                "current_weight": float(FEATURE_WEIGHTS.get(feature, 1.0)),
            })
            continue

        quality = (
            0.18 * float(group["concentration"].mean())
            + 0.18 * float(group["contrast"].mean())
            + 0.16 * float(group["top_gap"].mean())
            + 0.14 * float(group["peak_separation"].mean())
            + 0.22 * float(group["agreement"].mean())
            + 0.07 * float(group["top_agreement"].mean())
            + 0.05 * float(group["support"].mean())
        )
        rows.append({
            "feature": feature,
            "active_cases": int(len(group)),
            "active_rate": float(len(group) / max(total_cases, 1)),
            "quality": quality,
            "median_peak": float(group["peak"].median()),
            "median_p95": float(group["p95"].median()),
            "mean_agreement": float(group["agreement"].mean()),
            "mean_top_agreement": float(group["top_agreement"].mean()),
            "mean_concentration": float(group["concentration"].mean()),
            "mean_contrast": float(group["contrast"].mean()),
            "mean_top_gap": float(group["top_gap"].mean()),
            "current_weight": float(FEATURE_WEIGHTS.get(feature, 1.0)),
        })
    return pd.DataFrame(rows)


def _calibrate_weights(
    stats: pd.DataFrame,
    median_weight: float,
    max_ratio: float,
    scale_exponent: float,
    active_exponent: float,
) -> pd.DataFrame:
    calibrated = stats.copy()
    signal_scale = calibrated["median_p95"].clip(lower=1e-6)
    active_factor = calibrated["active_rate"].clip(lower=1e-6) ** active_exponent
    raw_strength = calibrated["quality"] * active_factor / (signal_scale ** scale_exponent)
    raw_strength = raw_strength.replace([np.inf, -np.inf], np.nan).fillna(0.0)

    scoring_mask = ~calibrated["feature"].str.startswith(WEIGHTLESS_FEATURE_PREFIXES)
    positive = raw_strength[scoring_mask & (raw_strength > 0.0)]
    if positive.empty:
        raise SystemExit("No positive calibration strengths were produced.")

    median_strength = float(positive.median())
    weights = raw_strength / max(median_strength, 1e-9) * median_weight
    lower = median_weight / max_ratio
    upper = median_weight * max_ratio
    weights = weights.clip(lower=lower, upper=upper)

    for prefix in WEIGHTLESS_FEATURE_PREFIXES:
        weights.loc[calibrated["feature"].str.startswith(prefix)] = 0.0

    calibrated["raw_strength"] = raw_strength
    calibrated["calibrated_weight"] = weights
    calibrated["calibrated_to_current_ratio"] = (
        calibrated["calibrated_weight"]
        / calibrated["current_weight"].replace(0.0, np.nan)
    )
    return calibrated


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Learn EvidenceRank feature priors from unlabeled raw incidents."
    )
    parser.add_argument(
        "--data-root",
        default="data/rcabench-platform-v2/data/rcabench",
        help="Directory containing incident folders with raw observability parquet files.",
    )
    parser.add_argument("--out", help="Optional JSON calibration artifact path.")
    parser.add_argument("--csv", help="Optional CSV feature statistics path.")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--median-weight", type=float, default=DEFAULT_MEDIAN_WEIGHT)
    parser.add_argument("--max-ratio", type=float, default=DEFAULT_MAX_RATIO)
    parser.add_argument("--scale-exponent", type=float, default=DEFAULT_SCALE_EXPONENT)
    parser.add_argument("--active-exponent", type=float, default=DEFAULT_ACTIVE_EXPONENT)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    data_root = _repo_path(args.data_root)
    case_dirs = _incident_dirs(data_root)
    if not case_dirs:
        raise SystemExit(f"No incident folders found under {data_root}")

    observations: list[dict[str, Any]] = []
    if args.workers <= 1:
        for idx, case_dir in enumerate(case_dirs, start=1):
            observations.extend(_case_observations(case_dir))
            if idx % 50 == 0:
                print(f"processed {idx}/{len(case_dirs)} incidents", file=sys.stderr)
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(_case_observations, path): path for path in case_dirs}
            for idx, future in enumerate(as_completed(futures), start=1):
                observations.extend(future.result())
                if idx % 50 == 0:
                    print(f"processed {idx}/{len(case_dirs)} incidents", file=sys.stderr)

    stats = _aggregate(observations, len(case_dirs))
    calibrated = _calibrate_weights(
        stats,
        median_weight=args.median_weight,
        max_ratio=args.max_ratio,
        scale_exponent=args.scale_exponent,
        active_exponent=args.active_exponent,
    )
    weights = {
        str(row.feature): float(row.calibrated_weight)
        for row in calibrated.itertuples(index=False)
    }
    payload = {
        "created": _now(),
        "data_root": str(data_root.relative_to(REPO_ROOT) if data_root.is_relative_to(REPO_ROOT) else data_root),
        "incident_count": len(case_dirs),
        "observation_count": len(observations),
        "method": {
            "quality": "0.18*concentration + 0.18*contrast + 0.16*top_gap + 0.14*peak_separation + 0.22*agreement + 0.07*top_agreement + 0.05*support",
            "strength": "quality * active_rate^active_exponent / median_p95^scale_exponent",
            "normalization": "scale positive non-topology strengths to the requested median weight, then cap by max_ratio",
            "labels_used": False,
        },
        "parameters": {
            "median_weight": args.median_weight,
            "max_ratio": args.max_ratio,
            "scale_exponent": args.scale_exponent,
            "active_exponent": args.active_exponent,
        },
        "weights": weights,
        "feature_stats": calibrated.to_dict(orient="records"),
    }

    if args.out:
        _write_json(_repo_path(args.out), payload)
    if args.csv:
        csv_path = _repo_path(args.csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        calibrated.to_csv(csv_path, index=False)

    summary = calibrated[
        [
            "feature",
            "calibrated_weight",
            "current_weight",
            "quality",
            "active_rate",
            "median_p95",
            "mean_agreement",
            "mean_top_agreement",
        ]
    ].sort_values("calibrated_weight", ascending=False)
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.6f}"))


if __name__ == "__main__":
    main()
