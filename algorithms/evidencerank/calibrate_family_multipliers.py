#!/usr/bin/env python3
"""Learn family-level EvidenceRank weight multipliers without labels.

This calibrator keeps the accepted EvidenceRank semantic prior as the center and
learns only coarse feature-family multipliers from self-supervised causal pairs.
The objective is intentionally label-free: synthetic pseudo-roots should outrank
topology-propagated victims and high-background services, while multipliers are
regularized toward 1.0.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCERANK_SRC = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(EVIDENCERANK_SRC))

from calibrate_causal_feature_weights import (  # noqa: E402
    DEFAULT_BACKGROUND_FACTOR,
    DEFAULT_EPOCHS,
    DEFAULT_LEARNING_RATE,
    DEFAULT_PROPAGATION_DECAY,
    DEFAULT_SAMPLES_PER_CASE,
    DEFAULT_SEED,
    _feature_scales,
    _incident_dirs,
    _load_case_packs,
    _relative,
    _repo_path,
    _sigmoid_negative_margin,
    _synthetic_diffs,
)
from evidencerank.algorithm import BASE_FEATURE_NAMES, FEATURE_WEIGHTS  # noqa: E402


FAMILY_FEATURES: dict[str, tuple[str, ...]] = {
    "metric_magnitude": (
        "metric_max_z",
        "metric_mean_z",
        "metric_anomaly_count",
        "metric_value_delta",
    ),
    "availability_drop": (
        "metric_count_drop_shift",
        "trace_count_drop_shift",
    ),
    "trace_latency": (
        "trace_duration_z",
        "trace_duration_delta",
        "trace_self_duration_relative_shift",
    ),
    "trace_traffic": (
        "trace_count_delta",
        "trace_count_rise_shift",
    ),
    "trace_protocol": (
        "trace_endpoint_shift",
        "trace_error_rate",
        "trace_status_code_shift",
    ),
    "log_evidence": (
        "log_count_delta",
        "log_error_rate",
        "log_template_delta",
    ),
    "observability_volume": (
        "abnormal_metric_rows",
        "abnormal_trace_rows",
    ),
    "topology_context": (
        "topology_in_degree",
        "topology_out_degree",
    ),
}

DEFAULT_CENTER_L2 = 1.5
DEFAULT_MIN_MULTIPLIER = 0.72
DEFAULT_MAX_MULTIPLIER = 1.28


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _family_names() -> tuple[str, ...]:
    return tuple(FAMILY_FEATURES.keys())


def _family_assignment() -> np.ndarray:
    families = _family_names()
    assignment = np.zeros((len(BASE_FEATURE_NAMES), len(families)), dtype=np.float64)
    seen: set[str] = set()
    for family_idx, family in enumerate(families):
        for feature in FAMILY_FEATURES[family]:
            if feature not in BASE_FEATURE_NAMES:
                raise SystemExit(f"Unknown feature in family {family}: {feature}")
            if feature in seen:
                raise SystemExit(f"Feature assigned to multiple families: {feature}")
            seen.add(feature)
            assignment[BASE_FEATURE_NAMES.index(feature), family_idx] = 1.0
    missing = set(BASE_FEATURE_NAMES) - seen
    if missing:
        raise SystemExit(f"Missing family assignments: {sorted(missing)}")
    return assignment


def _base_weight_vector() -> np.ndarray:
    return np.asarray(
        [float(FEATURE_WEIGHTS.get(feature, 1.0)) for feature in BASE_FEATURE_NAMES],
        dtype=np.float64,
    )


def _family_contributions(
    diffs: list[np.ndarray],
    base_weights: np.ndarray,
    assignment: np.ndarray,
) -> np.ndarray:
    batch = np.vstack(diffs).astype(np.float64, copy=False)
    return batch @ (base_weights[:, None] * assignment)


def _fit_multipliers(
    packs: list[Any],
    scales: np.ndarray,
    samples_per_case: int,
    epochs: int,
    learning_rate: float,
    center_l2: float,
    min_multiplier: float,
    max_multiplier: float,
    background_factor: float,
    propagation_decay: float,
    seed: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    rng = np.random.default_rng(seed)
    families = _family_names()
    assignment = _family_assignment()
    base_weights = _base_weight_vector()
    multipliers = np.ones(len(families), dtype=np.float64)
    trace: list[dict[str, float]] = []
    total_pairs = 0

    for epoch in range(epochs):
        order = rng.permutation(len(packs))
        epoch_pairs = 0
        epoch_loss = 0.0
        epoch_accuracy = 0.0
        epoch_base_accuracy = 0.0
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
            contributions = _family_contributions(diffs, base_weights, assignment)
            margins = contributions @ multipliers
            base_margins = contributions.sum(axis=1)
            factors = _sigmoid_negative_margin(margins)
            gradient = -(factors[:, None] * contributions).mean(axis=0)
            gradient += center_l2 * (multipliers - 1.0)
            multipliers -= learning_rate * gradient
            multipliers = np.clip(multipliers, min_multiplier, max_multiplier)

            epoch_pairs += int(contributions.shape[0])
            epoch_loss += float(np.log1p(np.exp(-np.clip(margins, -50.0, 50.0))).mean())
            epoch_accuracy += float((margins > 0.0).mean())
            epoch_base_accuracy += float((base_margins > 0.0).mean())
            epoch_batches += 1

        total_pairs += epoch_pairs
        trace.append({
            "epoch": float(epoch + 1),
            "pairs": float(epoch_pairs),
            "mean_loss": epoch_loss / max(epoch_batches, 1),
            "pair_accuracy": epoch_accuracy / max(epoch_batches, 1),
            "base_pair_accuracy": epoch_base_accuracy / max(epoch_batches, 1),
            "max_abs_multiplier_delta": float(np.max(np.abs(multipliers - 1.0))),
        })

    diagnostics = {
        "total_pairs": total_pairs,
        "epoch_trace": trace,
    }
    return multipliers, diagnostics


def _weight_table(multipliers: np.ndarray) -> pd.DataFrame:
    families = _family_names()
    feature_to_family = {
        feature: family
        for family, features in FAMILY_FEATURES.items()
        for feature in features
    }
    rows = []
    for feature in BASE_FEATURE_NAMES:
        family = feature_to_family[feature]
        multiplier = float(multipliers[families.index(family)])
        base_weight = float(FEATURE_WEIGHTS.get(feature, 1.0))
        rows.append({
            "feature": feature,
            "family": family,
            "base_weight": base_weight,
            "multiplier": multiplier,
            "calibrated_weight": base_weight * multiplier,
        })
    return pd.DataFrame(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Label-free family-level calibration for EvidenceRank weights."
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
    parser.add_argument("--center-l2", type=float, default=DEFAULT_CENTER_L2)
    parser.add_argument("--min-multiplier", type=float, default=DEFAULT_MIN_MULTIPLIER)
    parser.add_argument("--max-multiplier", type=float, default=DEFAULT_MAX_MULTIPLIER)
    parser.add_argument("--background-factor", type=float, default=DEFAULT_BACKGROUND_FACTOR)
    parser.add_argument("--propagation-decay", type=float, default=DEFAULT_PROPAGATION_DECAY)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.min_multiplier <= 0.0 or args.max_multiplier < args.min_multiplier:
        raise SystemExit("Multiplier bounds must be positive and ordered.")

    data_root = _repo_path(args.data_root)
    case_dirs = _incident_dirs(data_root)
    if not case_dirs:
        raise SystemExit(f"No incident folders found under {data_root}")

    packs = _load_case_packs(case_dirs, args.workers)
    if not packs:
        raise SystemExit("No usable incident feature matrices were produced.")

    scales = _feature_scales(packs)
    multipliers, diagnostics = _fit_multipliers(
        packs,
        scales,
        samples_per_case=args.samples_per_case,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        center_l2=args.center_l2,
        min_multiplier=args.min_multiplier,
        max_multiplier=args.max_multiplier,
        background_factor=args.background_factor,
        propagation_decay=args.propagation_decay,
        seed=args.seed,
    )
    table = _weight_table(multipliers)
    families = _family_names()
    family_payload = {
        family: float(multipliers[idx])
        for idx, family in enumerate(families)
    }
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
            "name": "self_supervised_causal_family_multiplier_calibration",
            "labels_used": False,
            "ground_truth_used": False,
            "base_prior": "EvidenceRank semantic feature weights",
            "objective": "learn bounded family multipliers so synthetic pseudo-roots outrank topology-propagated victims while staying close to the base prior",
            "family_features": FAMILY_FEATURES,
        },
        "parameters": {
            "seed": args.seed,
            "samples_per_case": args.samples_per_case,
            "epochs": args.epochs,
            "learning_rate": args.learning_rate,
            "center_l2": args.center_l2,
            "min_multiplier": args.min_multiplier,
            "max_multiplier": args.max_multiplier,
            "background_factor": args.background_factor,
            "propagation_decay": args.propagation_decay,
        },
        "diagnostics": diagnostics,
        "family_multipliers": family_payload,
        "weights": weights,
        "feature_stats": table.to_dict(orient="records"),
    }

    if args.out:
        _write_json(_repo_path(args.out), payload)
    if args.csv:
        csv_path = _repo_path(args.csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(csv_path, index=False)

    print(table.to_string(index=False, float_format=lambda value: f"{value:.6f}"))
    print(json.dumps(diagnostics["epoch_trace"][-1], sort_keys=True), file=sys.stderr)


if __name__ == "__main__":
    main()
