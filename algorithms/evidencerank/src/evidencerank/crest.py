"""CREST: Counterfactual Ranking of Evidence via Structural Topology.

The runtime path is intentionally label-free and model-free. It consumes only
the normal/abnormal telemetry frames exposed by the benchmark adapter.
"""

from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import Any

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


CREST_LOCAL_MODALITY_FEATURES: dict[str, tuple[str, ...]] = {
    modality: tuple(
        feature
        for feature in BASE_FEATURE_NAMES
        if feature in features
        and feature not in {"topology_in_degree", "topology_out_degree"}
    )
    for modality, features in MODALITY_FEATURES.items()
}

CREST_LOCAL_FEATURES = tuple(
    feature
    for feature in BASE_FEATURE_NAMES
    if any(feature in features for features in CREST_LOCAL_MODALITY_FEATURES.values())
)

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
CREST_CALIBRATION_FLOOR = 0.96


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


def _feature_probability_matrix(matrix: np.ndarray) -> np.ndarray:
    if matrix.size == 0:
        return matrix.astype(np.float64, copy=True)

    result = np.zeros(matrix.shape, dtype=np.float64)
    for column_idx in range(matrix.shape[1]):
        result[:, column_idx] = _saturating_incident_scale(matrix[:, column_idx])
    return result


def _rms(values: np.ndarray, axis: int) -> np.ndarray:
    if values.size == 0:
        return np.asarray([], dtype=np.float64)
    return np.sqrt(np.mean(np.square(values), axis=axis))


def _modality_scores(
    feature_scores: np.ndarray,
    enabled_features: tuple[str, ...],
    enabled_modalities: frozenset[str],
) -> tuple[np.ndarray, tuple[str, ...]]:
    columns: list[np.ndarray] = []
    names: list[str] = []
    feature_to_idx = {feature: idx for idx, feature in enumerate(enabled_features)}

    for modality in ("metric", "trace", "log"):
        if modality not in enabled_modalities:
            continue
        indices = [
            feature_to_idx[feature]
            for feature in CREST_LOCAL_MODALITY_FEATURES[modality]
            if feature in feature_to_idx
        ]
        if not indices:
            continue
        block = feature_scores[:, indices]
        if not np.any(block > 0.0):
            continue
        columns.append(_rms(block, axis=1))
        names.append(modality)

    if not columns:
        return np.zeros((feature_scores.shape[0], 0), dtype=np.float64), tuple()
    return np.vstack(columns).T, tuple(names)


def _local_abnormality(modality_matrix: np.ndarray) -> np.ndarray:
    if modality_matrix.size == 0 or modality_matrix.shape[1] == 0:
        return np.zeros(modality_matrix.shape[0], dtype=np.float64)
    energy = _rms(modality_matrix, axis=1)
    return _saturating_incident_scale(energy)


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


def _apply_counterfactual_explain_away_once(
    services: list[str],
    structural_energy: np.ndarray,
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
) -> np.ndarray:
    if not trace_edges or structural_energy.size == 0:
        return structural_energy

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    adjusted = structural_energy.astype(np.float64, copy=True)
    mutation_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name in CREST_COUNTERFACTUAL_MUTATION_FEATURES
    ]
    propagation_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name in CREST_COUNTERFACTUAL_PROPAGATION_FEATURES
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
) -> np.ndarray:
    adjusted = structural_energy.astype(np.float64, copy=True)
    for _family in CREST_COUNTERFACTUAL_ITERATION_FAMILIES:
        updated = _apply_counterfactual_explain_away_once(
            services,
            adjusted,
            role_matrix,
            enabled_features,
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
) -> np.ndarray:
    indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name not in CREST_DENOISED_CHANNEL_EXCLUDES
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


def _cross_modal_consistency(modality_matrix: np.ndarray) -> np.ndarray:
    if modality_matrix.size == 0 or modality_matrix.shape[1] <= 1:
        return np.ones(modality_matrix.shape[0], dtype=np.float64)
    mean = np.mean(modality_matrix, axis=1)
    std = np.std(modality_matrix, axis=1)
    coefficient = np.divide(std, mean + 1e-9)
    agreement = 1.0 / (1.0 + coefficient)
    coverage = np.mean(modality_matrix > 0.0, axis=1)
    raw_consistency = np.clip(np.sqrt(coverage) * agreement, 0.0, 1.0)
    calibrated = CREST_CALIBRATION_FLOOR + (
        1.0 - CREST_CALIBRATION_FLOOR
    ) * raw_consistency
    return np.clip(calibrated, CREST_CALIBRATION_FLOOR, 1.0)


def score_crest_services(
    input_folder: Path,
    enabled_modalities: frozenset[str] = ALL_MODALITIES,
    graph_mode: str = "counterfactual",
    use_calibration: bool = False,
) -> pd.DataFrame:
    frames = _load_input_frames(input_folder)
    services = _collect_services_from_frames(frames)
    if not services:
        return pd.DataFrame(columns=["service", "A", "F", "C", "score"])

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

    feature_scores = _feature_probability_matrix(role_matrix)
    modality_matrix, _modality_names = _modality_scores(
        feature_scores,
        enabled_features,
        enabled_modalities,
    )

    graph = _weighted_trace_graph(frames, services) if "trace" in enabled_modalities else {}
    denoised_support = np.zeros_like(local_abnormality, dtype=np.float64)
    if graph_mode == "local":
        explanatory_power = np.ones_like(local_abnormality, dtype=np.float64)
    elif graph_mode == "pagerank":
        explanatory_power = _pagerank_explanatory_power(local_abnormality, graph)
    else:
        structural_seed = _local_family_energy(
            role_matrix,
            enabled_features,
            include_topology=True,
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
        )
        denoised_support = _saturating_incident_scale(denoised_structural)

    calibration = (
        _cross_modal_consistency(modality_matrix)
        if use_calibration
        else np.ones_like(local_abnormality, dtype=np.float64)
    )
    score = local_abnormality * explanatory_power * calibration
    if graph_mode == "counterfactual":
        score = score + denoised_support * calibration
    if not np.any(score > 0.0) and np.any(local_abnormality > 0.0):
        score = local_abnormality.copy()

    result = pd.DataFrame(
        {
            "service": services,
            "A": local_abnormality,
            "F": explanatory_power,
            "C": calibration,
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
    """CREST ranking with counterfactual structural support and mild calibration."""

    _modalities: frozenset[str] = ALL_MODALITIES
    _graph_mode = "counterfactual"
    _use_calibration = True

    def needs_cpu_count(self) -> int | None:
        return 1

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        ranking = score_crest_services(
            args.input_folder,
            enabled_modalities=self._modalities,
            graph_mode=self._graph_mode,
            use_calibration=self._use_calibration,
        )
        return [
            AlgorithmAnswer(level="service", name=str(row.service), rank=rank)
            for rank, row in enumerate(ranking.itertuples(index=False), start=1)
        ]


class CRESTLocal(CREST):
    """CREST-Local ablation: Module 1 only."""

    _graph_mode = "local"
    _use_calibration = False


class CRESTNoCF(CREST):
    """CREST-NoCF ablation: local abnormality plus PageRank-style graph prior."""

    _graph_mode = "pagerank"


class CRESTNoCalib(CREST):
    """CREST-NoCalib ablation entrypoint.

    This keeps the counterfactual structural support term but removes the
    cross-modal uncertainty calibration factor.
    """

    _use_calibration = False
