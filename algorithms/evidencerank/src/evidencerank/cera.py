"""Counterfactual Evidence Role Alignment RCA algorithm."""

from __future__ import annotations

import math

import numpy as np
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import timeit

from .algorithm import (
    ALL_MODALITIES,
    BASE_FEATURE_NAMES,
    MODALITY_FEATURES,
    _apply_arc_trace_endpoint_support_gate,
    _build_feature_matrix,
    _collect_services_from_frames,
    _load_input_frames,
    _robust_case_feature_matrix,
)

CERA_ROLE_FAMILIES = {
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
    "trace_protocol_mutation": (
        "trace_endpoint_shift",
        "trace_error_rate",
        "trace_status_code_shift",
    ),
    "trace_latency": (
        "trace_duration_z",
        "trace_duration_delta",
    ),
    "trace_traffic": (
        "trace_count_delta",
        "trace_count_rise_shift",
    ),
    "trace_local_latency": (
        "trace_self_duration_relative_shift",
    ),
    "log_locality": (
        "log_count_delta",
        "log_error_rate",
        "log_template_delta",
    ),
    "observability_volume": (
        "abnormal_metric_rows",
        "abnormal_trace_rows",
    ),
}


def _family_indices(enabled_features: tuple[str, ...]) -> dict[str, list[int]]:
    return {
        family: [
            idx
            for idx, name in enumerate(enabled_features)
            if name in feature_names
        ]
        for family, feature_names in CERA_ROLE_FAMILIES.items()
    }


def _family_burdens(
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
) -> dict[str, np.ndarray]:
    return {
        family: matrix[:, indices].sum(axis=1).astype(np.float64)
        if indices
        else np.zeros(matrix.shape[0], dtype=np.float64)
        for family, indices in _family_indices(enabled_features).items()
    }


def _apply_counterfactual_explain_away(
    services: list[str],
    root_energy: np.ndarray,
    root_anchor: np.ndarray,
    victim_energy: np.ndarray,
    trace_edges: list[tuple[str, str]],
) -> np.ndarray:
    if not trace_edges or root_energy.size == 0:
        return root_energy

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    adjusted = root_energy.astype(np.float64, copy=True)
    anchor = np.nan_to_num(
        root_anchor.astype(np.float64, copy=False),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    victim = np.nan_to_num(
        victim_energy.astype(np.float64, copy=False),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    candidate_pairs: list[tuple[int, int, float]] = []

    def add_pair(root_idx: int, victim_idx: int) -> None:
        if root_idx == victim_idx:
            return

        anchor_excess = max(0.0, float(anchor[root_idx] - anchor[victim_idx]))
        victim_excess = max(0.0, float(victim[victim_idx] - victim[root_idx]))
        if anchor_excess <= 0.0 or victim_excess <= 0.0:
            return

        anchor_share = anchor_excess / (
            float(anchor[root_idx] + anchor[victim_idx]) + 1e-6
        )
        victim_share = victim_excess / (
            float(victim[victim_idx] + victim[root_idx]) + 1e-6
        )
        score_excess = max(0.0, float(adjusted[victim_idx] - adjusted[root_idx]))
        pair_strength = anchor_share * victim_share
        if not math.isfinite(pair_strength) or pair_strength <= 0.0:
            return

        transfer_base = score_excess
        if transfer_base <= 0.0:
            transfer_base = 0.05 * min(
                float(anchor[root_idx]),
                float(victim[victim_idx]),
            )
        transfer = transfer_base * pair_strength
        if math.isfinite(transfer) and transfer > 0.0:
            candidate_pairs.append((root_idx, victim_idx, transfer))

    for parent, child in trace_edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)
        if parent_idx is None or child_idx is None:
            continue
        add_pair(parent_idx, child_idx)
        add_pair(child_idx, parent_idx)

    best_by_victim: dict[int, tuple[int, int, float]] = {}
    for pair in candidate_pairs:
        victim_idx = pair[1]
        current = best_by_victim.get(victim_idx)
        if current is None or pair[2] > current[2]:
            best_by_victim[victim_idx] = pair

    for root_idx, victim_idx, transfer in best_by_victim.values():
        adjusted[root_idx] += transfer
        adjusted[victim_idx] -= 0.75 * transfer

    return np.maximum(adjusted, 0.0)


def _role_scores(
    services: list[str],
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
) -> dict[str, float]:
    case_matrix = _robust_case_feature_matrix(matrix)
    role_matrix = _apply_arc_trace_endpoint_support_gate(enabled_features, case_matrix)
    families = _family_burdens(role_matrix, enabled_features)

    metric = families["metric_magnitude"]
    availability = families["availability_drop"]
    protocol = families["trace_protocol_mutation"]
    latency = families["trace_latency"]
    traffic = families["trace_traffic"]
    local_latency = families["trace_local_latency"]
    log = families["log_locality"]
    volume = families["observability_volume"]

    evidence_burden = (
        metric
        + availability
        + protocol
        + latency
        + traffic
        + local_latency
        + log
        + volume
    )
    root_anchor = (
        availability
        + protocol
        + log
        + local_latency
        + 0.5 * metric
    )
    victim_energy = latency + traffic + 0.5 * volume
    propagation_dominance = np.maximum(0.0, victim_energy - root_anchor)
    root_energy = (
        evidence_burden
        + 0.10 * root_anchor
        - 0.05 * propagation_dominance
    )
    root_energy = np.maximum(root_energy, 0.0)
    root_energy = _apply_counterfactual_explain_away(
        services,
        root_energy,
        root_anchor,
        victim_energy,
        trace_edges,
    )

    return {
        service: float(score) if math.isfinite(float(score)) else 0.0
        for service, score in zip(services, root_energy)
    }


class CERA(Algorithm):
    """Counterfactual Evidence Role Alignment."""

    _modalities: frozenset[str] = ALL_MODALITIES

    def __init__(self):
        all_enabled = frozenset().union(*(MODALITY_FEATURES[m] for m in self._modalities))
        self._enabled_features = tuple(
            name for name in BASE_FEATURE_NAMES if name in all_enabled
        )

    def needs_cpu_count(self) -> int | None:
        return 1

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        frames = _load_input_frames(args.input_folder)
        services = _collect_services_from_frames(frames)
        if not services:
            return []

        matrix, trace_edges = _build_feature_matrix(
            frames,
            services,
            self._enabled_features,
            self._modalities,
        )
        scores = _role_scores(
            services,
            matrix,
            self._enabled_features,
            trace_edges,
        )
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        return [
            AlgorithmAnswer(level="service", name=name, rank=rank)
            for rank, (name, _score) in enumerate(sorted_scores, start=1)
        ]
