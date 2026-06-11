"""CREST: Counterfactual Ranking of Evidence via Structural Topology.

The runtime path is intentionally label-free and model-free. It consumes only
the normal/abnormal telemetry frames exposed by the benchmark adapter.
"""

from __future__ import annotations

import math
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import timeit

from .cera import (
    ALL_MODALITIES,
    BASE_FEATURE_NAMES,
    MODALITY_FEATURES,
    _apply_arc_trace_endpoint_support_gate,
    _apply_parent_context,
    _build_feature_matrix,
    _clean_service,
    _collect_services_from_frames,
    _load_input_frames,
    _series_service,
)
from .meo.dsl.schema import EvidenceOperatorSpec
from .meo.runtime.instantiate import ROLE_ORDER, instantiate_meol_features
from .meo.runtime.load_meol import DEFAULT_MEOL_PATH, load_operator_specs


CREST_ROLE_FAMILIES: dict[str, tuple[str, ...]] = {
    "metric_shift": (
        "metric_max_z",
        "metric_mean_z",
        "metric_anomaly_count",
        "metric_value_delta",
        "metric_count_drop_shift",
    ),
    "trace_mutation": (
        "trace_endpoint_shift",
        "trace_error_rate",
        "trace_status_code_shift",
    ),
    "trace_propagation": (
        "trace_duration_z",
        "trace_duration_delta",
        "trace_count_delta",
        "trace_count_rise_shift",
        "trace_count_drop_shift",
        "trace_self_duration_relative_shift",
    ),
    "log_shift": (
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

CREST_COUNTERFACTUAL_MUTATION_FEATURES = frozenset({
    "metric_count_drop_shift",
    "trace_count_drop_shift",
    "trace_endpoint_shift",
    "trace_error_rate",
    "trace_status_code_shift",
})

CREST_COUNTERFACTUAL_PROPAGATION_FEATURES = frozenset({
    "trace_duration_z",
    "trace_duration_delta",
    "trace_self_duration_relative_shift",
    "trace_count_delta",
    "trace_count_rise_shift",
    "abnormal_trace_rows",
    "log_count_delta",
    "log_template_delta",
})

CREST_COUNTERFACTUAL_ITERATION_FAMILIES = tuple(
    family
    for family in CREST_ROLE_FAMILIES
    if family not in {"observability_volume", "topology_context"}
)

CREST_CASE_SCALE_CLIP = 3.0
CREST_DENOISED_CHANNEL_EXCLUDES = frozenset({"trace_duration_z"})
ROLE_MUTATION = ROLE_ORDER.index("mutation")
ROLE_PROPAGATION = ROLE_ORDER.index("propagation")
ROLE_OBSERVABILITY_BIAS = ROLE_ORDER.index("observability_bias")
ROLE_TOPOLOGY_CONTEXT = ROLE_ORDER.index("topology_context")


@lru_cache(maxsize=8)
def _cached_meo_specs(meol_path: str) -> tuple[EvidenceOperatorSpec, ...]:
    return tuple(load_operator_specs(Path(meol_path)))


def _finite_nonnegative_array(values: np.ndarray) -> np.ndarray:
    clean = np.nan_to_num(
        values.astype(np.float64, copy=False),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    return np.maximum(clean, 0.0)


def _saturating_incident_scale(values: np.ndarray) -> np.ndarray:
    """Map one incident-local evidence vector into [0, 1].

    The scale is the median positive value inside the current incident. This is
    a nonparametric density-drift view: a service is large only relative to the
    normality shifts observed in the same case.
    """
    clean = _finite_nonnegative_array(values)
    positive = clean[clean > 0.0]
    if positive.size == 0:
        return np.zeros_like(clean, dtype=np.float64)

    scale = float(np.median(positive))
    if scale <= 1e-12:
        scale = float(np.max(positive))
    if scale <= 1e-12:
        return np.zeros_like(clean, dtype=np.float64)

    scaled = 1.0 - np.exp(-clean / scale)
    peak = float(np.max(scaled))
    if peak > 1e-12:
        scaled = scaled / peak
    return np.clip(scaled, 0.0, 1.0)


def _robust_case_feature_matrix(matrix: np.ndarray) -> np.ndarray:
    clean_matrix = np.nan_to_num(matrix, nan=0.0, posinf=0.0, neginf=0.0)
    clean_matrix = np.maximum(clean_matrix, 0.0)
    scaled = np.zeros_like(clean_matrix, dtype=np.float64)
    for column_idx in range(clean_matrix.shape[1]):
        column = clean_matrix[:, column_idx]
        positive = column[column > 0.0]
        if positive.size == 0:
            continue
        scale = (
            float(np.percentile(positive, 95))
            if positive.size > 1
            else float(positive[0])
        )
        if not math.isfinite(scale) or scale <= 0.0:
            scale = float(np.max(positive))
        if not math.isfinite(scale) or scale <= 0.0:
            continue
        scaled[:, column_idx] = np.clip(column / scale, 0.0, CREST_CASE_SCALE_CLIP)
    return scaled


def _family_burdens(
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
) -> dict[str, np.ndarray]:
    burdens: dict[str, np.ndarray] = {}
    for family, feature_names in CREST_ROLE_FAMILIES.items():
        indices = [
            idx
            for idx, feature_name in enumerate(enabled_features)
            if feature_name in feature_names
        ]
        burdens[family] = (
            matrix[:, indices].sum(axis=1).astype(np.float64)
            if indices
            else np.zeros(matrix.shape[0], dtype=np.float64)
        )
    return burdens


def _local_family_energy(
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    include_topology: bool,
) -> np.ndarray:
    families = _family_burdens(matrix, enabled_features)
    excluded = set() if include_topology else {"topology_context"}
    energy = np.zeros(matrix.shape[0], dtype=np.float64)
    for family, values in families.items():
        if family not in excluded:
            energy += values
    return np.maximum(energy, 0.0)


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
    scale = (
        float(np.percentile(positive, 95))
        if positive.size > 1
        else float(positive[0])
    )
    if not math.isfinite(scale) or scale <= 0.0:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    return np.clip(
        values / scale,
        0.0,
        CREST_CASE_SCALE_CLIP * float(len(indices)),
    )


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


def _meo_role_vectors(
    feature_matrix: np.ndarray,
    role_weight_matrix: np.ndarray,
) -> dict[str, np.ndarray]:
    """Project MEOL feature columns into CREST role vectors."""

    row_count = int(feature_matrix.shape[0]) if feature_matrix.ndim == 2 else 0
    zeros = np.zeros(row_count, dtype=np.float64)
    if (
        feature_matrix.ndim != 2
        or role_weight_matrix.ndim != 2
        or feature_matrix.shape[1] == 0
        or role_weight_matrix.shape[0] != feature_matrix.shape[1]
        or role_weight_matrix.shape[1] < len(ROLE_ORDER)
    ):
        return {
            "mutation": zeros.copy(),
            "propagation": zeros.copy(),
            "observability_bias": zeros.copy(),
            "topology_context": zeros.copy(),
        }

    clean_features = _finite_nonnegative_array(feature_matrix)
    clean_weights = np.nan_to_num(
        role_weight_matrix.astype(np.float64, copy=False),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    clean_weights = np.maximum(clean_weights, 0.0)
    return {
        "mutation": _finite_nonnegative_array(clean_features @ clean_weights[:, ROLE_MUTATION]),
        "propagation": _finite_nonnegative_array(clean_features @ clean_weights[:, ROLE_PROPAGATION]),
        "observability_bias": _finite_nonnegative_array(
            clean_features @ clean_weights[:, ROLE_OBSERVABILITY_BIAS]
        ),
        "topology_context": _finite_nonnegative_array(
            clean_features @ clean_weights[:, ROLE_TOPOLOGY_CONTEXT]
        ),
    }


def _filter_meo_specs_for_modalities(
    specs: list[EvidenceOperatorSpec],
    enabled_modalities: frozenset[str],
) -> list[EvidenceOperatorSpec]:
    return [
        spec
        for spec in specs
        if spec.source in enabled_modalities or spec.source == "topology"
    ]


def _meo_role_weight_matrix(specs: list[EvidenceOperatorSpec]) -> np.ndarray:
    weights: list[list[float]] = []
    for spec in specs:
        raw = [float(spec.role_prior.get(role, 0.0)) for role in ROLE_ORDER]
        clean = [value if math.isfinite(value) and value > 0.0 else 0.0 for value in raw]
        total = sum(clean)
        weights.append(
            [value / total for value in clean]
            if total > 1e-12
            else [0.0 for _role in ROLE_ORDER]
        )
    return np.asarray(weights, dtype=np.float64)


def _meo_counterfactual_feature_sets(
    specs: list[EvidenceOperatorSpec],
) -> tuple[frozenset[str], frozenset[str]]:
    """Read CREST counterfactual role membership from MEOL specs."""

    mutation_features = frozenset(
        spec.name
        for spec in specs
        if float(spec.role_prior.get("mutation", 0.0)) > 0.0
    )
    propagation_features = frozenset(
        spec.name
        for spec in specs
        if float(spec.role_prior.get("propagation", 0.0)) > 0.0
    )
    return mutation_features, propagation_features


def _local_meo_energy(
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
) -> np.ndarray:
    """Compute CREST local energy for MEOL features.

    Built-in CREST feature names use the exact CREST role-family aggregation.
    Custom MEOL operators that are not part of CREST_ROLE_FAMILIES are included
    as local evidence so they can still affect ranking.
    """

    energy = _local_family_energy(matrix, enabled_features, include_topology=True)
    known_features = frozenset().union(*CREST_ROLE_FAMILIES.values())
    extra_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name not in known_features
    ]
    if extra_indices:
        energy += matrix[:, extra_indices].sum(axis=1).astype(np.float64)
    return np.maximum(energy, 0.0)


def _instantiate_meol_from_crest_features(
    frames: dict[str, pd.DataFrame],
    services: list[str],
    specs: list[EvidenceOperatorSpec],
    enabled_modalities: frozenset[str],
) -> tuple[np.ndarray, tuple[str, ...], list[tuple[str, str]]] | None:
    """Fast path for MEOL operators that are aliases of built-in CREST features."""

    if not specs:
        return None
    enabled_feature_set = frozenset().union(
        *(MODALITY_FEATURES[modality] for modality in enabled_modalities)
    )
    feature_names = tuple(spec.name for spec in specs)
    if any(name not in enabled_feature_set for name in feature_names):
        return None
    if len(set(feature_names)) != len(feature_names):
        return None

    matrix, trace_edges = _build_feature_matrix(
        frames,
        services,
        feature_names,
        enabled_modalities,
        normalize=True,
    )
    return matrix, feature_names, trace_edges


def _apply_counterfactual_explain_away_once(
    services: list[str],
    structural_energy: np.ndarray,
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
    mutation_features: frozenset[str] = CREST_COUNTERFACTUAL_MUTATION_FEATURES,
    propagation_features: frozenset[str] = CREST_COUNTERFACTUAL_PROPAGATION_FEATURES,
) -> np.ndarray:
    if not trace_edges or structural_energy.size == 0:
        return structural_energy

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    adjusted = structural_energy.astype(np.float64, copy=True)
    mutation_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name in mutation_features
    ]
    propagation_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name in propagation_features
    ]
    if not mutation_indices or not propagation_indices:
        return structural_energy

    mutation = _positive_p95_scaled_sum(role_matrix, mutation_indices)
    propagation = _positive_p95_scaled_sum(role_matrix, propagation_indices)
    best_by_victim: dict[int, tuple[int, int, float]] = {}

    def add_pair(root_idx: int, victim_idx: int) -> None:
        if root_idx == victim_idx or adjusted[victim_idx] <= adjusted[root_idx]:
            return

        mutation_excess = max(0.0, float(mutation[root_idx] - mutation[victim_idx]))
        propagation_excess = max(
            0.0,
            float(propagation[victim_idx] - propagation[root_idx]),
        )
        if mutation_excess <= 0.0 or propagation_excess <= 0.0:
            return

        mutation_share = mutation_excess / (
            float(mutation[root_idx] + mutation[victim_idx]) + 1e-12
        )
        propagation_share = propagation_excess / (
            float(propagation[victim_idx] + propagation[root_idx]) + 1e-12
        )
        transfer = (
            float(adjusted[victim_idx] - adjusted[root_idx])
            * mutation_share
            * propagation_share
        )
        if not math.isfinite(transfer) or transfer <= 0.0:
            return

        current = best_by_victim.get(victim_idx)
        if current is None or transfer > current[2]:
            best_by_victim[victim_idx] = (root_idx, victim_idx, transfer)

    for parent, child in trace_edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)
        if parent_idx is None or child_idx is None:
            continue
        add_pair(parent_idx, child_idx)
        add_pair(child_idx, parent_idx)

    for root_idx, victim_idx, transfer in best_by_victim.values():
        adjusted[root_idx] += transfer
        adjusted[victim_idx] -= transfer
    return np.maximum(adjusted, 0.0)


def _apply_counterfactual_explain_away(
    services: list[str],
    structural_energy: np.ndarray,
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
    mutation_features: frozenset[str] = CREST_COUNTERFACTUAL_MUTATION_FEATURES,
    propagation_features: frozenset[str] = CREST_COUNTERFACTUAL_PROPAGATION_FEATURES,
) -> np.ndarray:
    adjusted = structural_energy.astype(np.float64, copy=True)
    for _family in CREST_COUNTERFACTUAL_ITERATION_FAMILIES:
        updated = _apply_counterfactual_explain_away_once(
            services,
            adjusted,
            role_matrix,
            enabled_features,
            trace_edges,
            mutation_features,
            propagation_features,
        )
        if np.linalg.norm(updated - adjusted) <= 1e-12 * (
            np.linalg.norm(adjusted) + 1e-12
        ):
            return updated
        adjusted = updated
    return adjusted


def _apply_counterfactual_explain_away_once_soft(
    services: list[str],
    structural_energy: np.ndarray,
    mutation: np.ndarray,
    propagation: np.ndarray,
    trace_edges: list[tuple[str, str]],
) -> np.ndarray:
    if not trace_edges or structural_energy.size == 0:
        return structural_energy

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    adjusted = structural_energy.astype(np.float64, copy=True)
    clean_mutation = _finite_nonnegative_array(mutation)
    clean_propagation = _finite_nonnegative_array(propagation)
    best_by_victim: dict[int, tuple[int, int, float]] = {}

    def add_pair(root_idx: int, victim_idx: int) -> None:
        if root_idx == victim_idx or adjusted[victim_idx] <= adjusted[root_idx]:
            return

        mutation_excess = max(
            0.0,
            float(clean_mutation[root_idx] - clean_mutation[victim_idx]),
        )
        propagation_excess = max(
            0.0,
            float(clean_propagation[victim_idx] - clean_propagation[root_idx]),
        )
        if mutation_excess <= 0.0 or propagation_excess <= 0.0:
            return

        mutation_share = mutation_excess / (
            float(clean_mutation[root_idx] + clean_mutation[victim_idx]) + 1e-12
        )
        propagation_share = propagation_excess / (
            float(clean_propagation[victim_idx] + clean_propagation[root_idx]) + 1e-12
        )
        transfer = (
            float(adjusted[victim_idx] - adjusted[root_idx])
            * mutation_share
            * propagation_share
        )
        if not math.isfinite(transfer) or transfer <= 0.0:
            return

        current = best_by_victim.get(victim_idx)
        if current is None or transfer > current[2]:
            best_by_victim[victim_idx] = (root_idx, victim_idx, transfer)

    for parent, child in trace_edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)
        if parent_idx is None or child_idx is None:
            continue
        add_pair(parent_idx, child_idx)
        add_pair(child_idx, parent_idx)

    for root_idx, victim_idx, transfer in best_by_victim.values():
        adjusted[root_idx] += transfer
        adjusted[victim_idx] -= transfer
    return np.maximum(adjusted, 0.0)


def _apply_counterfactual_explain_away_soft(
    services: list[str],
    structural_energy: np.ndarray,
    mutation: np.ndarray,
    propagation: np.ndarray,
    trace_edges: list[tuple[str, str]],
    max_iter: int = len(CREST_COUNTERFACTUAL_ITERATION_FAMILIES),
) -> np.ndarray:
    adjusted = structural_energy.astype(np.float64, copy=True)
    for _step in range(max_iter):
        updated = _apply_counterfactual_explain_away_once_soft(
            services,
            adjusted,
            mutation,
            propagation,
            trace_edges,
        )
        if np.linalg.norm(updated - adjusted) <= 1e-12 * (
            np.linalg.norm(adjusted) + 1e-12
        ):
            return updated
        adjusted = updated
    return adjusted


def _denoised_channel_energy(
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    excluded_features: frozenset[str] = CREST_DENOISED_CHANNEL_EXCLUDES,
) -> np.ndarray:
    indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name not in excluded_features
    ]
    if not indices:
        return np.zeros(role_matrix.shape[0], dtype=np.float64)
    return role_matrix[:, indices].sum(axis=1).astype(np.float64)


def _derive_parent_service(data: pd.DataFrame) -> pd.DataFrame:
    if "parent_service" in data.columns:
        return data
    required = {"span_id", "parent_span_id", "service_name"}
    if not required.issubset(data.columns):
        return data
    span_to_service = {
        span_id: service
        for span_id, service in data[["span_id", "service_name"]].itertuples(
            index=False,
            name=None,
        )
        if _clean_service(span_id) is not None and _clean_service(service) is not None
    }
    data = data.copy()
    data["parent_service"] = data["parent_span_id"].map(span_to_service)
    return data


def _weighted_trace_graph(
    frames: dict[str, pd.DataFrame],
    services: list[str],
) -> dict[int, list[tuple[int, float]]]:
    service_to_idx = {service: idx for idx, service in enumerate(services)}
    abnormal = frames.get("abnormal_traces", pd.DataFrame())
    normal = frames.get("normal_traces", pd.DataFrame())
    data = abnormal if abnormal is not None and not abnormal.empty else normal
    if data is None or data.empty:
        return {}

    data = _derive_parent_service(data.copy())
    if "parent_service" not in data.columns:
        return {}

    data["service_name"] = _series_service(data)
    data["parent_service"] = data["parent_service"].map(_clean_service)
    edge_counts: dict[tuple[int, int], float] = defaultdict(float)
    for parent, child in data[["parent_service", "service_name"]].dropna().itertuples(
        index=False,
        name=None,
    ):
        parent_idx = service_to_idx.get(str(parent))
        child_idx = service_to_idx.get(str(child))
        if parent_idx is None or child_idx is None or parent_idx == child_idx:
            continue
        edge_counts[(parent_idx, child_idx)] += 1.0

    out_totals: dict[int, float] = defaultdict(float)
    for (parent_idx, _child_idx), count in edge_counts.items():
        out_totals[parent_idx] += count

    graph: dict[int, list[tuple[int, float]]] = defaultdict(list)
    for (parent_idx, child_idx), count in edge_counts.items():
        total = out_totals[parent_idx]
        if total > 0.0:
            graph[parent_idx].append((child_idx, count / total))
    return dict(graph)


def _incident_graph_decay(graph: dict[int, list[tuple[int, float]]]) -> float:
    if not graph:
        return 0.0
    branching = np.asarray([len(children) for children in graph.values()], dtype=np.float64)
    mean_branching = float(np.mean(branching)) if branching.size else 0.0
    if mean_branching <= 0.0:
        return 0.0
    return 1.0 / math.sqrt(1.0 + mean_branching)


def _counterfactual_explanatory_power(
    local_abnormality: np.ndarray,
    graph: dict[int, list[tuple[int, float]]],
) -> np.ndarray:
    total_energy = float(np.sum(local_abnormality))
    if total_energy <= 1e-12:
        return np.zeros_like(local_abnormality, dtype=np.float64)
    if not graph:
        return local_abnormality / total_energy

    node_count = local_abnormality.shape[0]
    decay = _incident_graph_decay(graph)
    if decay <= 0.0:
        return local_abnormality / total_energy

    explanatory = np.zeros(node_count, dtype=np.float64)
    for source_idx in range(node_count):
        impact = np.zeros(node_count, dtype=np.float64)
        frontier = np.zeros(node_count, dtype=np.float64)
        impact[source_idx] = 1.0
        frontier[source_idx] = 1.0

        for _step in range(node_count):
            next_frontier = np.zeros(node_count, dtype=np.float64)
            active = np.flatnonzero(frontier > 1e-9)
            if active.size == 0:
                break
            for parent_idx in active:
                for child_idx, edge_weight in graph.get(int(parent_idx), ()):
                    message = float(frontier[parent_idx]) * float(edge_weight) * decay
                    if message > next_frontier[child_idx]:
                        next_frontier[child_idx] = message
            if not np.any(next_frontier > 1e-9):
                break
            impact = 1.0 - (1.0 - impact) * (1.0 - np.clip(next_frontier, 0.0, 1.0))
            frontier = next_frontier

        explanatory[source_idx] = float(np.dot(local_abnormality, impact) / total_energy)

    return np.clip(explanatory, 0.0, 1.0)


def _pagerank_explanatory_power(
    local_abnormality: np.ndarray,
    graph: dict[int, list[tuple[int, float]]],
) -> np.ndarray:
    total_energy = float(np.sum(local_abnormality))
    if total_energy <= 1e-12:
        return np.zeros_like(local_abnormality, dtype=np.float64)
    if not graph:
        return local_abnormality / total_energy

    node_count = local_abnormality.shape[0]
    teleport = local_abnormality / total_energy
    rank = teleport.copy()
    linked_nodes = set(graph)
    damping = _incident_graph_decay(graph)
    for _step in range(max(1, node_count)):
        next_rank = (1.0 - damping) * teleport
        dangling_mass = float(np.sum(rank[[idx for idx in range(node_count) if idx not in linked_nodes]]))
        next_rank += damping * dangling_mass * teleport
        for parent_idx, children in graph.items():
            parent_mass = damping * float(rank[parent_idx])
            for child_idx, edge_weight in children:
                next_rank[child_idx] += parent_mass * float(edge_weight)
        rank = next_rank

    return _saturating_incident_scale(rank)


def score_crest_services(
    input_folder: Path,
    enabled_modalities: frozenset[str] = ALL_MODALITIES,
    graph_mode: str = "counterfactual",
    use_meo: bool = False,
    meol_path: Path | None = None,
) -> pd.DataFrame:
    frames = _load_input_frames(input_folder)
    services = _collect_services_from_frames(frames)
    if not services:
        return pd.DataFrame(columns=["service", "A", "F", "S", "score"])

    enabled_features: tuple[str, ...] = ()
    trace_edges: list[tuple[str, str]] = []
    role_matrix = np.zeros((len(services), 0), dtype=np.float64)
    mutation_features = CREST_COUNTERFACTUAL_MUTATION_FEATURES
    propagation_features = CREST_COUNTERFACTUAL_PROPAGATION_FEATURES
    if use_meo:
        try:
            selected_meol_path = meol_path or DEFAULT_MEOL_PATH
            specs = _filter_meo_specs_for_modalities(
                list(_cached_meo_specs(str(selected_meol_path))),
                enabled_modalities,
            )
            mutation_features, propagation_features = _meo_counterfactual_feature_sets(specs)
            fast_meo = _instantiate_meol_from_crest_features(
                frames,
                services,
                specs,
                enabled_modalities,
            )
            if fast_meo is None:
                meo_matrix, enabled_features, _role_weight_matrix = instantiate_meol_features(
                    frames,
                    services,
                    specs,
                )
                meo_matrix = np.log1p(_finite_nonnegative_array(meo_matrix))
                _empty_matrix, trace_edges = _build_feature_matrix(
                    frames,
                    services,
                    (),
                    enabled_modalities,
                    normalize=True,
                )
            else:
                meo_matrix, enabled_features, trace_edges = fast_meo
            case_matrix = _robust_case_feature_matrix(meo_matrix)
            role_matrix = _apply_arc_trace_endpoint_support_gate(
                enabled_features,
                case_matrix,
            )
            local_energy = _local_meo_energy(role_matrix, enabled_features)
            local_abnormality = _saturating_incident_scale(local_energy)
            if not np.any(local_abnormality > 0.0):
                use_meo = False
        except Exception:
            use_meo = False

    if not use_meo:
        mutation_features = CREST_COUNTERFACTUAL_MUTATION_FEATURES
        propagation_features = CREST_COUNTERFACTUAL_PROPAGATION_FEATURES
        enabled_feature_set = frozenset().union(
            *(MODALITY_FEATURES[modality] for modality in enabled_modalities)
        )
        enabled_features = tuple(
            feature
            for feature in BASE_FEATURE_NAMES
            if feature in enabled_feature_set
        )
        matrix, trace_edges = _build_feature_matrix(
            frames,
            services,
            enabled_features,
            enabled_modalities,
            normalize=True,
        )
        case_matrix = _robust_case_feature_matrix(matrix)
        role_matrix = _apply_arc_trace_endpoint_support_gate(enabled_features, case_matrix)
        local_energy = _local_family_energy(
            role_matrix,
            enabled_features,
            include_topology=True,
        )
        local_abnormality = _saturating_incident_scale(local_energy)

    graph = _weighted_trace_graph(frames, services) if "trace" in enabled_modalities else {}
    denoised_support = np.zeros_like(local_abnormality, dtype=np.float64)
    if graph_mode == "local":
        explanatory_power = np.ones_like(local_abnormality, dtype=np.float64)
    elif graph_mode == "pagerank":
        explanatory_power = _pagerank_explanatory_power(local_abnormality, graph)
    else:
        structural_seed = (
            _local_meo_energy(role_matrix, enabled_features)
            if use_meo
            else _local_family_energy(
                role_matrix,
                enabled_features,
                include_topology=True,
            )
        )
        context_weight = _trace_density_context_weight(services, trace_edges)
        structural_energy = _apply_parent_context(
            services,
            structural_seed,
            trace_edges,
            context_weight,
        )
        structural_energy = _apply_counterfactual_explain_away(
            services,
            np.maximum(structural_energy, 0.0),
            role_matrix,
            enabled_features,
            trace_edges,
            mutation_features,
            propagation_features,
        )
        explanatory_power = _saturating_incident_scale(structural_energy)

        denoised_energy = _denoised_channel_energy(role_matrix, enabled_features)
        denoised_structural = _apply_parent_context(
            services,
            denoised_energy,
            trace_edges,
            context_weight,
        )
        denoised_structural = _apply_counterfactual_explain_away(
            services,
            np.maximum(denoised_structural, 0.0),
            role_matrix,
            enabled_features,
            trace_edges,
            mutation_features,
            propagation_features,
        )
        denoised_support = _saturating_incident_scale(denoised_structural)

    score = local_abnormality * explanatory_power
    if graph_mode == "counterfactual":
        score = score + denoised_support
    if not np.any(score > 0.0) and np.any(local_abnormality > 0.0):
        score = local_abnormality.copy()

    result = pd.DataFrame(
        {
            "service": services,
            "A": local_abnormality,
            "F": explanatory_power,
            "S": denoised_support,
            "score": score,
        }
    )
    return result.sort_values(
        ["score", "A", "F", "service"],
        ascending=[False, False, False, True],
        kind="stable",
    ).reset_index(drop=True)


class CREST(Algorithm):
    """CREST ranking with counterfactual structural support."""

    _modalities: frozenset[str] = ALL_MODALITIES
    _graph_mode = "counterfactual"
    _use_meo = False
    _meol_path: Path | None = None

    def needs_cpu_count(self) -> int | None:
        return 1

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        ranking = score_crest_services(
            args.input_folder,
            enabled_modalities=self._modalities,
            graph_mode=self._graph_mode,
            use_meo=self._use_meo,
            meol_path=self._meol_path,
        )
        return [
            AlgorithmAnswer(level="service", name=str(row.service), rank=rank)
            for rank, row in enumerate(ranking.itertuples(index=False), start=1)
        ]


class CRESTLocal(CREST):
    """CREST-Local ablation: Module 1 only."""

    _graph_mode = "local"


class CRESTNoCF(CREST):
    """CREST-NoCF ablation: local abnormality plus PageRank-style graph prior."""

    _graph_mode = "pagerank"


class CRESTMetric(CREST):
    """CREST ablation using only metric evidence."""

    _modalities = frozenset({"metric"})


class CRESTTrace(CREST):
    """CREST ablation using only trace evidence."""

    _modalities = frozenset({"trace"})


class CRESTLog(CREST):
    """CREST ablation using only log evidence."""

    _modalities = frozenset({"log"})


class CRESTMetricTrace(CREST):
    """CREST ablation using metric and trace evidence."""

    _modalities = frozenset({"metric", "trace"})


class CRESTMetricLog(CREST):
    """CREST ablation using metric and log evidence."""

    _modalities = frozenset({"metric", "log"})


class CRESTLogTrace(CREST):
    """CREST ablation using log and trace evidence."""

    _modalities = frozenset({"log", "trace"})


def __getattr__(name: str) -> object:
    """Keep historic CREST-MEO import paths while defining them separately."""

    if name == "CRESTMEO":
        from .crest_meo import CRESTMEO

        return CRESTMEO
    if name == "CRESTMEOBuiltIn":
        from .crest_meo import CRESTMEOBuiltIn

        return CRESTMEOBuiltIn
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
