"""Causal Evidence Role Alignment RCA algorithm."""

from __future__ import annotations

import math
from enum import IntEnum

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
)


class CERAEvidenceTier(IntEnum):
    """Ordinal causal evidence roles, not feature-specific numeric weights."""

    DISABLED = 0
    BACKGROUND = 1
    BASELINE = 2
    SUPPORT = 3
    LOCAL = 4
    HIGH = 5
    ROOT = 6
    CRITICAL = 7


CERA_FEATURE_TIERS = {
    "metric_max_z": CERAEvidenceTier.BACKGROUND,
    "metric_mean_z": CERAEvidenceTier.BACKGROUND,
    "metric_anomaly_count": CERAEvidenceTier.BACKGROUND,
    "metric_value_delta": CERAEvidenceTier.BACKGROUND,
    "metric_count_drop_shift": CERAEvidenceTier.HIGH,
    "trace_duration_z": CERAEvidenceTier.DISABLED,
    "trace_duration_delta": CERAEvidenceTier.BASELINE,
    "trace_count_delta": CERAEvidenceTier.BASELINE,
    "trace_count_rise_shift": CERAEvidenceTier.HIGH,
    "trace_count_drop_shift": CERAEvidenceTier.BASELINE,
    "trace_endpoint_shift": CERAEvidenceTier.HIGH,
    "trace_error_rate": CERAEvidenceTier.BASELINE,
    "trace_status_code_shift": CERAEvidenceTier.CRITICAL,
    "trace_self_duration_relative_shift": CERAEvidenceTier.LOCAL,
    "log_count_delta": CERAEvidenceTier.LOCAL,
    "log_error_rate": CERAEvidenceTier.LOCAL,
    "log_template_delta": CERAEvidenceTier.BACKGROUND,
    "topology_in_degree": CERAEvidenceTier.SUPPORT,
    "topology_out_degree": CERAEvidenceTier.DISABLED,
    "abnormal_metric_rows": CERAEvidenceTier.SUPPORT,
    "abnormal_trace_rows": CERAEvidenceTier.SUPPORT,
}


def _synthesize_ordinal_energy_ladder() -> dict[CERAEvidenceTier, float]:
    """Build evidence energies from tier ordering and tier count.

    The ladder avoids per-feature numeric tuning. Low tiers form a small ordinal
    band around the baseline tier; causal-root tiers are separated by the number
    of low tiers, and the critical tier is the next dyadic ceiling.
    """
    low_tiers = (
        CERAEvidenceTier.BACKGROUND,
        CERAEvidenceTier.BASELINE,
        CERAEvidenceTier.SUPPORT,
        CERAEvidenceTier.LOCAL,
    )
    low_step = 1.0 / float(len(low_tiers))
    ladder = {CERAEvidenceTier.DISABLED: 0.0}
    for tier in low_tiers:
        offset = int(tier) - int(CERAEvidenceTier.BASELINE)
        ladder[tier] = 1.0 + low_step * float(offset)

    local_ceiling = ladder[CERAEvidenceTier.LOCAL]
    root_floor = local_ceiling * float(len(low_tiers))
    ladder[CERAEvidenceTier.HIGH] = root_floor
    ladder[CERAEvidenceTier.ROOT] = root_floor + float(len(low_tiers))
    ladder[CERAEvidenceTier.CRITICAL] = float(
        1 << math.ceil(math.log2(ladder[CERAEvidenceTier.ROOT]))
    )
    return ladder


CERA_ORDINAL_ENERGY_LADDER = _synthesize_ordinal_energy_ladder()

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


def _trace_sink_context_weight(
    services: list[str],
    trace_edges: list[tuple[str, str]],
) -> float:
    if not services or not trace_edges:
        return 0.0
    service_set = set(services)
    valid_edges = {
        (parent, child)
        for parent, child in trace_edges
        if parent in service_set and child in service_set and parent != child
    }
    if not valid_edges:
        return 0.0
    parent_nodes = {parent for parent, _child in valid_edges}
    child_nodes = {child for _parent, child in valid_edges}
    sink_nodes = child_nodes - parent_nodes
    return float(len(sink_nodes)) / float(len(services))


def _ordinal_evidence_energy(enabled_features: tuple[str, ...]) -> np.ndarray:
    return np.asarray(
        [
            CERA_ORDINAL_ENERGY_LADDER[
                CERA_FEATURE_TIERS.get(feature_name, CERAEvidenceTier.BASELINE)
            ]
            for feature_name in enabled_features
        ],
        dtype=np.float32,
    )


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
    evidence_energy = _ordinal_evidence_energy(enabled_features)
    role_matrix = _apply_arc_trace_endpoint_support_gate(
        enabled_features,
        matrix * evidence_energy,
    )
    evidence_burden = role_matrix.sum(axis=1).astype(np.float64)
    context_weight = _trace_sink_context_weight(services, trace_edges)
    root_energy = _apply_parent_context(
        services,
        evidence_burden,
        trace_edges,
        context_weight,
    )
    root_energy = np.maximum(root_energy, 0.0)

    return {
        service: float(score) if math.isfinite(float(score)) else 0.0
        for service, score in zip(services, root_energy)
    }


class CERA(Algorithm):
    """Causal Evidence Role Alignment."""

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
