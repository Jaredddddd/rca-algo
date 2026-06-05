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
    _apply_parent_context,
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
    "topology_context": (
        "topology_in_degree",
        "topology_out_degree",
    ),
}

CERA_COUNTERFACTUAL_MUTATION_FEATURES = frozenset({
    "metric_count_drop_shift",
    "trace_count_drop_shift",
    "trace_endpoint_shift",
    "trace_error_rate",
    "trace_status_code_shift",
})

CERA_COUNTERFACTUAL_PROPAGATION_FEATURES = frozenset({
    "trace_duration_z",
    "trace_duration_delta",
    "trace_self_duration_relative_shift",
    "trace_count_delta",
    "trace_count_rise_shift",
    "abnormal_trace_rows",
    "log_count_delta",
    "log_template_delta",
})

CERA_COUNTERFACTUAL_ROLE_FAMILIES = tuple(
    family
    for family in CERA_ROLE_FAMILIES
    if family not in {"observability_volume", "topology_context"}
)


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


def _positive_p95_scaled_sum(
    matrix: np.ndarray,
    indices: list[int],
) -> np.ndarray:
    if not indices:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    values = matrix[:, indices].sum(axis=1).astype(np.float64)
    positive = values[np.isfinite(values) & (values > 0.0)]
    if positive.size == 0:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    scale = float(np.percentile(positive, 95)) if positive.size > 1 else float(positive[0])
    if not math.isfinite(scale) or scale <= 0.0:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    return np.clip(values / scale, 0.0, float(len(indices)))


def _trace_density_context_weight(
    services: list[str],
    trace_edges: list[tuple[str, str]],
) -> float:
    if not services:
        return 0.0
    service_set = set(services)
    valid_edges = {
        (parent, child)
        for parent, child in trace_edges
        if parent in service_set and child in service_set and parent != child
    }
    average_edge_degree = float(len(valid_edges)) / float(len(services))
    return 1.0 / (1.0 + average_edge_degree)


def _apply_counterfactual_explain_away_once(
    services: list[str],
    root_energy: np.ndarray,
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
) -> np.ndarray:
    if not trace_edges or root_energy.size == 0:
        return root_energy

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    adjusted = root_energy.astype(np.float64, copy=True)
    mutation_indices = [
        idx
        for idx, name in enumerate(enabled_features)
        if name in CERA_COUNTERFACTUAL_MUTATION_FEATURES
    ]
    propagation_indices = [
        idx
        for idx, name in enumerate(enabled_features)
        if name in CERA_COUNTERFACTUAL_PROPAGATION_FEATURES
    ]
    if not mutation_indices or not propagation_indices:
        return root_energy

    mutation = _positive_p95_scaled_sum(role_matrix, mutation_indices)
    propagation = _positive_p95_scaled_sum(role_matrix, propagation_indices)
    candidate_pairs: list[tuple[int, int, float]] = []

    def add_pair(root_idx: int, victim_idx: int) -> None:
        if root_idx == victim_idx or adjusted[victim_idx] <= adjusted[root_idx]:
            return

        mutation_excess = max(0.0, float(mutation[root_idx] - mutation[victim_idx]))
        propagation_excess = max(0.0, float(propagation[victim_idx] - propagation[root_idx]))
        if mutation_excess <= 0.0 or propagation_excess <= 0.0:
            return

        mutation_share = mutation_excess / (
            float(mutation[root_idx] + mutation[victim_idx]) + 1e-12
        )
        propagation_share = propagation_excess / (
            float(propagation[victim_idx] + propagation[root_idx]) + 1e-12
        )
        pair_strength = mutation_share * propagation_share
        if not math.isfinite(pair_strength) or pair_strength <= 0.0:
            return

        score_excess = float(adjusted[victim_idx] - adjusted[root_idx])
        transfer = score_excess * pair_strength
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
        adjusted[victim_idx] -= transfer

    return np.maximum(adjusted, 0.0)


def _apply_counterfactual_explain_away(
    services: list[str],
    root_energy: np.ndarray,
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
) -> np.ndarray:
    adjusted = root_energy.astype(np.float64, copy=True)
    for _family in CERA_COUNTERFACTUAL_ROLE_FAMILIES:
        updated = _apply_counterfactual_explain_away_once(
            services,
            adjusted,
            role_matrix,
            enabled_features,
            trace_edges,
        )
        if np.linalg.norm(updated - adjusted) <= 1e-12 * (np.linalg.norm(adjusted) + 1e-12):
            return updated
        adjusted = updated
    return adjusted


def _role_scores(
    services: list[str],
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
) -> dict[str, float]:
    case_matrix = _robust_case_feature_matrix(matrix)
    role_matrix = _apply_arc_trace_endpoint_support_gate(enabled_features, case_matrix)
    families = _family_burdens(role_matrix, enabled_features)

    evidence_burden = sum(
        family_values
        for family_values in families.values()
    )
    context_weight = _trace_density_context_weight(services, trace_edges)
    root_energy = _apply_parent_context(
        services,
        evidence_burden
        if isinstance(evidence_burden, np.ndarray)
        else np.zeros(len(services), dtype=np.float64),
        trace_edges,
        context_weight,
    )
    root_energy = np.maximum(root_energy, 0.0)
    root_energy = _apply_counterfactual_explain_away(
        services,
        root_energy,
        role_matrix,
        enabled_features,
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
