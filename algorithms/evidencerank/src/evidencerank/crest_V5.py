"""CREST: Counterfactual Ranking of Evidence via Structural Topology.

The runtime path is intentionally label-free and model-free. It consumes only
the normal/abnormal telemetry frames exposed by the benchmark adapter.
"""

from __future__ import annotations

import math
from collections import defaultdict
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

CREST_RESOURCE_IDENTITY_COLUMNS = (
    "attr.aiops.pod",
    "attr.k8s.pod.name",
    "attr.aiops.instance",
    "attr.aiops.object_id",
    "attr.aiops.device",
    "attr.aiops.mountpoint",
    "attr.k8s.node.name",
    "attr.k8s.container.name",
    "attr.k8s.deployment.name",
    "attr.k8s.statefulset.name",
)

CREST_SERVICE_AGGREGATE_RESOURCE_COLUMNS = frozenset({
    "attr.aiops.object_id",
    "attr.k8s.container.name",
    "attr.k8s.deployment.name",
    "attr.k8s.statefulset.name",
})

CREST_RESOURCE_KPI_COLUMNS = (
    "attr.aiops.kpi_key",
    "metric",
)

CREST_RESOURCE_KPI_CONTEXT_COLUMNS = (
    "attr.aiops.type",
    "attr.aiops.sql_type",
    "attr.aiops.cf",
    "attr.aiops.metric_group",
)

CREST_EMPTY_TEXT_VALUES = frozenset({"", "none", "nan", "null", "<na>"})


def _finite_nonnegative_array(values: np.ndarray) -> np.ndarray:
    clean = np.nan_to_num(
        values.astype(np.float64, copy=False),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    return np.maximum(clean, 0.0)


def _clean_text_series(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.strip()
    return text.mask(text.str.lower().isin(CREST_EMPTY_TEXT_VALUES))


def _first_valid_text_column(
    data: pd.DataFrame,
    columns: tuple[str, ...],
    service_series: pd.Series | None = None,
) -> pd.Series:
    result = pd.Series(pd.NA, index=data.index, dtype="string")
    for column in columns:
        if column not in data.columns:
            continue
        values = _clean_text_series(data[column])
        if (
            service_series is not None
            and column in CREST_SERVICE_AGGREGATE_RESOURCE_COLUMNS
        ):
            values = values.mask(values == service_series)
        result = result.fillna(values)
    return result


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


def _unit_geometric_mean(values: list[float]) -> float:
    clean = [float(np.clip(value, 0.0, 1.0)) for value in values]
    if not clean:
        return 0.0
    product = math.prod(clean)
    return float(np.clip(product ** (1.0 / float(len(clean))), 0.0, 1.0))


def _trace_service_mask_and_spread(
    frames: dict[str, pd.DataFrame],
    services: list[str],
) -> tuple[np.ndarray, float, float, bool, int | None]:
    mask = np.zeros(len(services), dtype=bool)
    abnormal = frames.get("abnormal_traces", pd.DataFrame())
    if abnormal is None or abnormal.empty or not services:
        return mask, 0.0, 0.0, False, None

    series = _series_service(abnormal).dropna()
    if series.empty:
        return mask, 0.0, 0.0, False, None

    service_set = set(services)
    series = series[series.isin(service_set)]
    if series.empty:
        return mask, 0.0, 0.0, False, None

    counts = series.value_counts()
    service_to_idx = {service: idx for idx, service in enumerate(services)}
    for service in counts.index:
        idx = service_to_idx.get(str(service))
        if idx is not None:
            mask[idx] = True
    top_idx = service_to_idx.get(str(counts.index[0]))

    total = float(counts.sum())
    top_share = float(counts.iloc[0]) / total if total > 0.0 else 0.0
    rest_share = max(0.0, 1.0 - top_share)
    trace_service_count = int(mask.sum())
    coverage = float(trace_service_count) / float(len(services)) if services else 0.0
    if trace_service_count <= 1:
        spread = 0.0
    else:
        uniform_share = 1.0 / float(trace_service_count)
        spread = (1.0 - top_share) / max(1e-12, 1.0 - uniform_share)
    return (
        mask,
        float(np.clip(coverage, 0.0, 1.0)),
        float(np.clip(spread, 0.0, 1.0)),
        bool(top_share > rest_share),
        top_idx,
    )


def _family_selectivity(values: np.ndarray) -> float:
    clean = _finite_nonnegative_array(values)
    positive = clean[clean > 0.0]
    if positive.size == 0:
        return 0.0

    ordered = np.sort(positive)
    top = float(ordered[-1])
    second = float(ordered[-2]) if ordered.size > 1 else 0.0
    total = float(np.sum(positive))
    if top <= 1e-12 or total <= 1e-12:
        return 0.0

    top_share = top / total
    gap = (top - second) / (top + second + 1e-12)
    selectivity = math.sqrt(max(0.0, top_share) * max(0.0, gap))
    return float(np.clip(selectivity, 0.0, 1.0))


def _positive_rank_view(values: np.ndarray) -> np.ndarray:
    clean = _finite_nonnegative_array(values)
    view = np.zeros(clean.shape[0], dtype=np.float64)
    positive_idx = np.flatnonzero(clean > 0.0)
    if positive_idx.size == 0:
        return view

    ordered_idx = positive_idx[np.argsort(clean[positive_idx], kind="mergesort")]
    view[ordered_idx] = np.arange(1, positive_idx.size + 1, dtype=np.float64) / float(
        positive_idx.size
    )
    return view


def _modality_energy_confidence(values: np.ndarray) -> float:
    clean = _finite_nonnegative_array(values)
    if clean.size == 0:
        return 0.0
    positive = clean[clean > 0.0]
    if positive.size == 0:
        return 0.0

    coverage = float(positive.size) / float(clean.size)
    selectivity = _family_selectivity(clean)
    coverage_or_selectivity = max(coverage, selectivity)
    return _unit_geometric_mean([coverage_or_selectivity, selectivity])


def _rank_agreement(left: np.ndarray, right: np.ndarray) -> float:
    left_view = _positive_rank_view(left)
    right_view = _positive_rank_view(right)
    left_norm = float(np.linalg.norm(left_view))
    right_norm = float(np.linalg.norm(right_view))
    if left_norm <= 1e-12 or right_norm <= 1e-12:
        return 0.0
    similarity = float(np.dot(left_view, right_view) / (left_norm * right_norm))
    if not math.isfinite(similarity):
        return 0.0
    return float(np.clip(similarity, 0.0, 1.0))


def _nontrace_evidence_trace_overlap(
    families: dict[str, np.ndarray],
    trace_mask: np.ndarray,
) -> float:
    metric = _finite_nonnegative_array(
        families.get("metric_shift", np.zeros_like(trace_mask, dtype=np.float64))
    )
    log = _finite_nonnegative_array(
        families.get("log_shift", np.zeros_like(metric, dtype=np.float64))
    )
    evidence = metric + log
    if evidence.size == 0 or trace_mask.size == 0:
        return 1.0

    positive_idx = np.flatnonzero(evidence > 0.0)
    if positive_idx.size == 0:
        return 1.0

    total = float(np.sum(evidence[positive_idx]))
    if total <= 1e-12:
        return 1.0

    mass_overlap = float(np.sum(evidence[trace_mask])) / total
    top_k = max(1, min(int(positive_idx.size), math.ceil(math.sqrt(positive_idx.size))))
    ranked = positive_idx[np.argsort(evidence[positive_idx], kind="mergesort")][::-1]
    top_overlap = float(np.mean(trace_mask[ranked[:top_k]])) if top_k > 0 else 1.0
    return float(np.clip(math.sqrt(max(0.0, mass_overlap) * max(0.0, top_overlap)), 0.0, 1.0))


def _nontrace_top_surface_ownership(
    families: dict[str, np.ndarray],
    top_idx: int | None,
) -> float:
    if top_idx is None:
        return 0.0
    metric = _finite_nonnegative_array(
        families.get("metric_shift", np.asarray([], dtype=np.float64))
    )
    log = _finite_nonnegative_array(
        families.get("log_shift", np.zeros_like(metric, dtype=np.float64))
    )
    evidence = metric + log
    if evidence.size == 0 or top_idx >= evidence.size:
        return 0.0

    positive = evidence[evidence > 0.0]
    if positive.size == 0:
        return 0.0
    top_value = float(evidence[top_idx])
    if top_value <= 0.0:
        return 0.0

    mass_share = top_value / max(float(np.sum(positive)), 1e-12)
    peak_share = top_value / max(float(np.max(positive)), 1e-12)
    return _unit_geometric_mean([mass_share, peak_share])


def _incident_trace_structural_reliability(
    frames: dict[str, pd.DataFrame],
    services: list[str],
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
) -> tuple[float, float]:
    trace_mask, trace_coverage, trace_spread, has_majority_surface, top_trace_idx = _trace_service_mask_and_spread(
        frames,
        services,
    )
    if not np.any(trace_mask):
        return 0.0, 0.0
    if not has_majority_surface:
        return 1.0, 1.0

    families = _family_burdens(role_matrix, enabled_features)
    mutation_selectivity = _family_selectivity(
        families.get("trace_mutation", np.asarray([], dtype=np.float64))
    )
    propagation_selectivity = _family_selectivity(
        families.get("trace_propagation", np.asarray([], dtype=np.float64))
    )
    nontrace_overlap = _nontrace_evidence_trace_overlap(families, trace_mask)
    top_surface_ownership = _nontrace_top_surface_ownership(families, top_trace_idx)

    candidate_coverage = max(math.sqrt(trace_coverage), nontrace_overlap)
    trace_role_selectivity = max(mutation_selectivity, propagation_selectivity)
    root_alignment = max(
        nontrace_overlap,
        trace_role_selectivity,
        top_surface_ownership,
    )
    confidence = _unit_geometric_mean(
        [trace_spread, candidate_coverage, root_alignment]
    )
    return confidence, confidence


def _apply_trace_confidence_gate(
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_scale: float,
) -> np.ndarray:
    if trace_scale >= 1.0:
        return role_matrix
    adjusted = role_matrix.copy()
    for idx, feature_name in enumerate(enabled_features):
        if feature_name in MODALITY_FEATURES["trace"]:
            adjusted[:, idx] *= trace_scale
    return adjusted


def _modality_weighted_rank_fusion(
    score: np.ndarray,
    families: dict[str, np.ndarray],
    enabled_modalities: frozenset[str],
    trace_scale: float,
    trace_mask: np.ndarray | None = None,
    trace_surface_idx: int | None = None,
) -> tuple[np.ndarray, dict[str, float]]:
    metric = _finite_nonnegative_array(
        families.get("metric_shift", np.zeros_like(score, dtype=np.float64))
    )
    log = _finite_nonnegative_array(
        families.get("log_shift", np.zeros_like(score, dtype=np.float64))
    )
    trace = _finite_nonnegative_array(
        families.get("trace_mutation", np.zeros_like(score, dtype=np.float64))
    ) + _finite_nonnegative_array(
        families.get("trace_propagation", np.zeros_like(score, dtype=np.float64))
    )

    metric_confidence = (
        _modality_energy_confidence(metric) if "metric" in enabled_modalities else 0.0
    )
    log_confidence = (
        _modality_energy_confidence(log) if "log" in enabled_modalities else 0.0
    )
    trace_energy_confidence = (
        _modality_energy_confidence(trace) if "trace" in enabled_modalities else 0.0
    )
    trace_modality_confidence = _unit_geometric_mean(
        [trace_scale, max(trace_energy_confidence, _rank_agreement(trace, metric + log))]
    )
    confidences = {
        "metric_confidence": metric_confidence,
        "log_confidence": log_confidence,
        "trace_modality_confidence": trace_modality_confidence,
    }
    if trace_scale >= 1.0 or score.size == 0:
        return score, confidences

    nontrace = metric + log
    if not np.any(nontrace > 0.0) or not np.any(score > 0.0):
        return score, confidences

    winner_idx = int(np.argmax(score))
    candidate_idx = int(np.argmax(nontrace))
    if candidate_idx == winner_idx:
        return score, confidences

    score_view = _positive_rank_view(score)
    positive_score_view = score_view[score_view > 0.0]
    if positive_score_view.size == 0:
        return score, confidences
    if float(score_view[candidate_idx]) < float(np.median(positive_score_view)):
        return score, confidences

    nontrace_view = _positive_rank_view(nontrace)
    trace_view = _positive_rank_view(trace)
    nontrace_confidence = max(
        metric_confidence,
        log_confidence,
        _rank_agreement(metric, log),
    )
    if nontrace_confidence <= trace_modality_confidence:
        return score, confidences
    if nontrace_view[candidate_idx] <= nontrace_view[winner_idx]:
        return score, confidences

    metric_view = _positive_rank_view(metric)
    log_view = _positive_rank_view(log)
    if metric[candidate_idx] <= 0.0 or log[candidate_idx] <= 0.0:
        return score, confidences
    if metric_view[candidate_idx] < metric_view[winner_idx]:
        return score, confidences
    if log_view[candidate_idx] < log_view[winner_idx]:
        return score, confidences

    mutation_view = _positive_rank_view(
        _finite_nonnegative_array(
            families.get("trace_mutation", np.zeros_like(score, dtype=np.float64))
        )
    )
    propagation_view = _positive_rank_view(
        _finite_nonnegative_array(
            families.get("trace_propagation", np.zeros_like(score, dtype=np.float64))
        )
    )
    if trace_surface_idx is not None and 0 <= trace_surface_idx < score.size:
        winner_mutation_owned_surface = (
            winner_idx == trace_surface_idx
            and mutation_view[winner_idx] > propagation_view[winner_idx]
            and mutation_view[winner_idx] > mutation_view[candidate_idx]
        )
        if winner_mutation_owned_surface:
            return score, confidences

        candidate_is_trace_covered = (
            trace_mask is not None
            and candidate_idx < trace_mask.size
            and bool(trace_mask[candidate_idx])
        )
        winner_mutation_owned_non_surface = (
            winner_idx != trace_surface_idx
            and candidate_is_trace_covered
            and mutation_view[winner_idx] > mutation_view[candidate_idx]
        )
        if winner_mutation_owned_non_surface:
            return score, confidences

    if trace_view[winner_idx] <= trace_view[candidate_idx]:
        return score, confidences

    adjusted = score.astype(np.float64, copy=True)
    peak = float(np.max(adjusted))
    if not math.isfinite(peak) or peak <= 0.0:
        return score, confidences
    adjusted[candidate_idx] = np.nextafter(peak, math.inf)
    return adjusted, confidences


def _trace_root_eligibility_vectors(
    families: dict[str, np.ndarray],
    trace_coverage: float,
    trace_spread: float,
    score_shape: tuple[int, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    metric = _finite_nonnegative_array(
        families.get("metric_shift", np.zeros(score_shape, dtype=np.float64))
    )
    log = _finite_nonnegative_array(
        families.get("log_shift", np.zeros_like(metric, dtype=np.float64))
    )
    trace_mutation = _finite_nonnegative_array(
        families.get("trace_mutation", np.zeros_like(metric, dtype=np.float64))
    )
    trace_propagation = _finite_nonnegative_array(
        families.get("trace_propagation", np.zeros_like(metric, dtype=np.float64))
    )

    metric_view = _positive_rank_view(metric)
    log_view = _positive_rank_view(log)
    nontrace_view = _positive_rank_view(metric + log)
    mutation_view = _positive_rank_view(trace_mutation)
    propagation_view = _positive_rank_view(trace_propagation)
    trace_view = _positive_rank_view(trace_mutation + trace_propagation)

    structural_context = math.sqrt(
        max(0.0, float(trace_coverage)) * max(0.0, float(trace_spread))
    )
    nontrace_support = np.maximum(metric_view, log_view)
    trace_root = np.maximum(
        np.sqrt(mutation_view * nontrace_view),
        np.sqrt(mutation_view * structural_context),
    )
    trace_symptom = np.sqrt(
        trace_view
        * propagation_view
        * np.maximum(0.0, 1.0 - nontrace_view)
        * max(0.0, 1.0 - float(trace_spread))
    )
    nontrace_root = np.sqrt(nontrace_view * nontrace_support)
    return trace_root, trace_symptom, nontrace_root


def _apply_trace_root_eligibility_arbitration(
    score: np.ndarray,
    families: dict[str, np.ndarray],
    trace_coverage: float,
    trace_spread: float,
    trace_mask: np.ndarray | None = None,
    trace_surface_idx: int | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    trace_root, trace_symptom, nontrace_root = _trace_root_eligibility_vectors(
        families,
        trace_coverage,
        trace_spread,
        score.shape,
    )
    if score.size == 0 or not np.any(nontrace_root > 0.0):
        return score, trace_root, trace_symptom, nontrace_root
    if not np.any(trace_symptom > 0.0):
        return score, trace_root, trace_symptom, nontrace_root

    winner_idx = int(np.argmax(score))
    candidate_idx = int(np.argmax(nontrace_root))
    if candidate_idx == winner_idx:
        return score, trace_root, trace_symptom, nontrace_root
    if nontrace_root[candidate_idx] <= nontrace_root[winner_idx]:
        return score, trace_root, trace_symptom, nontrace_root
    if trace_symptom[winner_idx] <= trace_root[winner_idx]:
        return score, trace_root, trace_symptom, nontrace_root
    if nontrace_root[candidate_idx] <= trace_root[winner_idx]:
        return score, trace_root, trace_symptom, nontrace_root

    trace_total = _finite_nonnegative_array(
        families.get("trace_mutation", np.zeros_like(score, dtype=np.float64))
    ) + _finite_nonnegative_array(
        families.get("trace_propagation", np.zeros_like(score, dtype=np.float64))
    )
    trace_view = _positive_rank_view(trace_total)
    if trace_view[winner_idx] <= trace_view[candidate_idx]:
        return score, trace_root, trace_symptom, nontrace_root

    candidate_is_trace_surface = (
        trace_surface_idx is not None and candidate_idx == trace_surface_idx
    )
    candidate_is_trace_covered = (
        trace_mask is not None
        and candidate_idx < trace_mask.size
        and bool(trace_mask[candidate_idx])
    )
    if candidate_is_trace_surface and candidate_is_trace_covered:
        return score, trace_root, trace_symptom, nontrace_root

    adjusted = score.astype(np.float64, copy=True)
    peak = float(np.max(adjusted))
    if not math.isfinite(peak) or peak <= 0.0:
        return score, trace_root, trace_symptom, nontrace_root
    adjusted[candidate_idx] = np.nextafter(peak, math.inf)
    return adjusted, trace_root, trace_symptom, nontrace_root


def _apply_adaptive_modality_surface_competition(
    score: np.ndarray,
    families: dict[str, np.ndarray],
    trace_spread: float,
    has_majority_surface: bool,
    trace_surface_idx: int | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    surface_pressure = np.zeros_like(score, dtype=np.float64)
    nontrace_root = np.zeros_like(score, dtype=np.float64)
    if (
        score.size == 0
        or not has_majority_surface
        or trace_surface_idx is None
        or trace_surface_idx < 0
        or trace_surface_idx >= score.size
    ):
        return score, surface_pressure, nontrace_root

    metric = _finite_nonnegative_array(
        families.get("metric_shift", np.zeros_like(score, dtype=np.float64))
    )
    log = _finite_nonnegative_array(
        families.get("log_shift", np.zeros_like(score, dtype=np.float64))
    )
    trace_mutation = _finite_nonnegative_array(
        families.get("trace_mutation", np.zeros_like(score, dtype=np.float64))
    )
    trace_propagation = _finite_nonnegative_array(
        families.get("trace_propagation", np.zeros_like(score, dtype=np.float64))
    )
    trace_volume = _finite_nonnegative_array(
        families.get("observability_volume", np.zeros_like(score, dtype=np.float64))
    )

    nontrace = metric + log
    if not np.any(nontrace > 0.0) or not np.any(score > 0.0):
        return score, surface_pressure, nontrace_root

    metric_view = _positive_rank_view(metric)
    log_view = _positive_rank_view(log)
    nontrace_view = _positive_rank_view(nontrace)
    mutation_view = _positive_rank_view(trace_mutation)
    propagation_view = _positive_rank_view(trace_propagation)
    trace_view = _positive_rank_view(trace_mutation + trace_propagation + trace_volume)
    score_view = _positive_rank_view(score)

    nontrace_support = np.maximum(metric_view, log_view)
    nontrace_root = np.sqrt(nontrace_view * nontrace_support)
    cross_modal_alignment = _rank_agreement(trace_mutation, nontrace)
    trace_root = np.sqrt(
        mutation_view
        * np.maximum(nontrace_view, np.full_like(nontrace_view, cross_modal_alignment))
    )
    trace_surface_pressure = np.sqrt(
        trace_view
        * np.maximum(propagation_view, np.maximum(0.0, trace_view - mutation_view))
        * max(0.0, 1.0 - float(trace_spread))
    )
    surface_pressure = trace_surface_pressure

    winner_idx = int(np.argmax(score))
    surface_idx = int(trace_surface_idx)
    if winner_idx != surface_idx:
        return score, surface_pressure, nontrace_root

    candidate_idx = int(np.argmax(nontrace_root))
    if candidate_idx == surface_idx:
        return score, surface_pressure, nontrace_root
    if nontrace_root[candidate_idx] <= nontrace_root[surface_idx]:
        return score, surface_pressure, nontrace_root
    if nontrace_root[candidate_idx] <= trace_root[surface_idx]:
        return score, surface_pressure, nontrace_root
    if surface_pressure[surface_idx] <= trace_root[surface_idx]:
        return score, surface_pressure, nontrace_root
    if trace_view[surface_idx] <= trace_view[candidate_idx]:
        return score, surface_pressure, nontrace_root

    positive_score_view = score_view[score_view > 0.0]
    if positive_score_view.size == 0 or score_view[candidate_idx] <= 0.0:
        return score, surface_pressure, nontrace_root
    if score_view[candidate_idx] < float(np.median(positive_score_view)):
        return score, surface_pressure, nontrace_root

    adjusted = score.astype(np.float64, copy=True)
    peak = float(np.max(adjusted))
    if not math.isfinite(peak) or peak <= 0.0:
        return score, surface_pressure, nontrace_root
    adjusted[candidate_idx] = np.nextafter(peak, math.inf)
    return adjusted, surface_pressure, nontrace_root


def _apply_broad_trace_surface_competition(
    score: np.ndarray,
    families: dict[str, np.ndarray],
    has_majority_surface: bool,
    trace_surface_idx: int | None,
) -> tuple[np.ndarray, np.ndarray]:
    nontrace_root = np.zeros_like(score, dtype=np.float64)
    if (
        score.size == 0
        or not has_majority_surface
        or trace_surface_idx is None
        or trace_surface_idx < 0
        or trace_surface_idx >= score.size
    ):
        return score, nontrace_root

    winner_idx = int(np.argmax(score))
    surface_idx = int(trace_surface_idx)
    if winner_idx != surface_idx:
        return score, nontrace_root

    metric = _finite_nonnegative_array(
        families.get("metric_shift", np.zeros_like(score, dtype=np.float64))
    )
    log = _finite_nonnegative_array(
        families.get("log_shift", np.zeros_like(score, dtype=np.float64))
    )
    nontrace = metric + log
    if not np.any(nontrace > 0.0):
        return score, nontrace_root

    metric_view = _positive_rank_view(metric)
    log_view = _positive_rank_view(log)
    nontrace_view = _positive_rank_view(nontrace)
    nontrace_root = np.sqrt(nontrace_view * np.maximum(metric_view, log_view))

    candidates = np.arange(score.size)
    candidates = candidates[candidates != surface_idx]
    if candidates.size == 0:
        return score, nontrace_root

    candidate_idx = int(candidates[np.argmax(nontrace_root[candidates])])
    if nontrace_root[candidate_idx] <= 0.0:
        return score, nontrace_root

    positive_nontrace = nontrace_root[nontrace_root > 0.0]
    if positive_nontrace.size == 0:
        return score, nontrace_root
    if nontrace_root[candidate_idx] < float(np.median(positive_nontrace)):
        return score, nontrace_root

    score_view = _positive_rank_view(score)
    positive_score_view = score_view[score_view > 0.0]
    if positive_score_view.size == 0:
        return score, nontrace_root
    if score_view[candidate_idx] < float(np.median(positive_score_view)):
        return score, nontrace_root

    adjusted = score.astype(np.float64, copy=True)
    peak = float(np.max(adjusted))
    if not math.isfinite(peak) or peak <= 0.0:
        return score, nontrace_root
    adjusted[candidate_idx] = np.nextafter(peak, math.inf)
    return adjusted, nontrace_root


def _prepare_metric_provenance_frame(data: pd.DataFrame) -> pd.DataFrame:
    if data is None or data.empty:
        return pd.DataFrame(columns=["service_name", "_resource", "_kpi", "_value"])
    if "service_name" not in data.columns or "value" not in data.columns:
        return pd.DataFrame(columns=["service_name", "_resource", "_kpi", "_value"])

    service = _clean_text_series(data["service_name"])
    resource = _first_valid_text_column(
        data,
        CREST_RESOURCE_IDENTITY_COLUMNS,
        service_series=service,
    )
    if resource.isna().all():
        return pd.DataFrame(columns=["service_name", "_resource", "_kpi", "_value"])

    kpi = _first_valid_text_column(data, CREST_RESOURCE_KPI_COLUMNS)
    context = _first_valid_text_column(data, CREST_RESOURCE_KPI_CONTEXT_COLUMNS)
    kpi = kpi.fillna("metric")
    context = context.fillna("")
    kpi_key = _clean_text_series(kpi + "|" + context).fillna("metric")

    prepared = pd.DataFrame(
        {
            "service_name": service,
            "_resource": resource,
            "_kpi": kpi_key,
            "_value": pd.to_numeric(data["value"], errors="coerce"),
        }
    )
    return prepared.dropna(subset=["service_name", "_resource", "_value"])


def _second_largest(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    ordered = np.sort(np.asarray(values, dtype=np.float64))
    return float(ordered[-2])


def _resource_provenance_ownership(
    frames: dict[str, pd.DataFrame],
    services: list[str],
) -> np.ndarray:
    ownership = np.zeros(len(services), dtype=np.float64)
    if not services:
        return ownership

    normal = _prepare_metric_provenance_frame(
        frames.get("normal_metrics", pd.DataFrame())
    )
    abnormal = _prepare_metric_provenance_frame(
        frames.get("abnormal_metrics", pd.DataFrame())
    )
    if normal.empty and abnormal.empty:
        return ownership

    keys = ["service_name", "_resource", "_kpi"]
    grouped_frames = []
    if not normal.empty:
        grouped = normal.groupby(keys, dropna=False)["_value"].agg(
            n_mean="mean",
            n_std="std",
            n_count="count",
        )
        grouped_frames.append(grouped)
    if not abnormal.empty:
        grouped = abnormal.groupby(keys, dropna=False)["_value"].agg(
            a_mean="mean",
            a_count="count",
        )
        grouped_frames.append(grouped)
    if not grouped_frames:
        return ownership

    stats = pd.concat(grouped_frames, axis=1)
    for column in ("n_mean", "n_std", "a_mean"):
        if column not in stats.columns:
            stats[column] = 0.0
        stats[column] = stats[column].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    for column in ("n_count", "a_count"):
        if column not in stats.columns:
            stats[column] = 0.0
        stats[column] = stats[column].fillna(0.0).astype(np.float64)

    n_count = stats["n_count"].to_numpy(dtype=np.float64)
    a_count = stats["a_count"].to_numpy(dtype=np.float64)
    min_count = np.minimum(n_count, a_count)
    max_count = np.maximum(n_count, a_count)
    value_delta = np.abs(
        stats["a_mean"].to_numpy(dtype=np.float64)
        - stats["n_mean"].to_numpy(dtype=np.float64)
    )
    scale = np.abs(stats["n_std"].to_numpy(dtype=np.float64)) + 1e-6
    value_signal = np.log1p(value_delta / scale) * np.log1p(min_count)
    count_signal = (
        np.abs(a_count - n_count) / (max_count + 1e-12) * np.log1p(max_count)
    )
    evidence = np.maximum(value_signal + count_signal, 0.0)
    if not np.any(evidence > 0.0):
        return ownership

    service_to_group_values: dict[str, list[float]] = defaultdict(list)
    service_to_resource_values: dict[str, dict[str, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    for (service, resource, _kpi), value in zip(stats.index, evidence):
        evidence_value = float(value)
        if not math.isfinite(evidence_value) or evidence_value <= 0.0:
            continue
        service_name = str(service)
        resource_name = str(resource)
        service_to_group_values[service_name].append(evidence_value)
        service_to_resource_values[service_name][resource_name] += evidence_value

    raw = np.zeros(len(services), dtype=np.float64)
    service_to_idx = {service: idx for idx, service in enumerate(services)}
    for service, group_values in service_to_group_values.items():
        service_idx = service_to_idx.get(service)
        if service_idx is None:
            continue
        group_array = np.asarray(group_values, dtype=np.float64)
        total = float(np.sum(group_array))
        top = float(np.max(group_array)) if group_array.size else 0.0
        second = _second_largest(group_values)
        group_share = top / (total + 1e-12)
        group_gap = (top - second) / (top + second + 1e-12)

        resource_values = list(service_to_resource_values[service].values())
        resource_total = float(np.sum(resource_values))
        resource_top = float(np.max(resource_values)) if resource_values else 0.0
        resource_second = _second_largest(resource_values)
        resource_share = resource_top / (resource_total + 1e-12)
        resource_gap = (resource_top - resource_second) / (
            resource_top + resource_second + 1e-12
        )
        concentration = math.sqrt(
            max(0.0, max(group_share * group_gap, resource_share * resource_gap))
        )
        raw[service_idx] = total * math.sqrt(max(0.0, concentration))

    return _saturating_incident_scale(raw)


def _resource_provenance_confidence(resource_ownership: np.ndarray) -> float:
    return _family_selectivity(resource_ownership)


def _apply_resource_provenance_arbitration(
    score: np.ndarray,
    families: dict[str, np.ndarray],
    resource_ownership: np.ndarray,
    trace_scale: float,
    trace_mask: np.ndarray | None = None,
    trace_surface_idx: int | None = None,
) -> np.ndarray:
    if trace_scale >= 1.0 or score.size == 0:
        return score

    resource = _finite_nonnegative_array(resource_ownership)
    if resource.size != score.size or not np.any(resource > 0.0):
        return score

    metric = _finite_nonnegative_array(
        families.get("metric_shift", np.zeros_like(score, dtype=np.float64))
    )
    log = _finite_nonnegative_array(
        families.get("log_shift", np.zeros_like(score, dtype=np.float64))
    )
    trace_mutation = _finite_nonnegative_array(
        families.get("trace_mutation", np.zeros_like(score, dtype=np.float64))
    )
    trace_propagation = _finite_nonnegative_array(
        families.get("trace_propagation", np.zeros_like(score, dtype=np.float64))
    )
    if not np.any(metric > 0.0):
        return score

    resource_view = _positive_rank_view(resource)
    metric_view = _positive_rank_view(metric)
    nontrace_view = _positive_rank_view(metric + log)
    support_view = np.maximum(metric_view, nontrace_view)
    ownership_view = np.sqrt(resource_view * support_view)
    if not np.any(ownership_view > 0.0):
        return score

    winner_idx = int(np.argmax(score))
    candidate_idx = int(np.argmax(ownership_view))
    if candidate_idx == winner_idx:
        return score
    if ownership_view[candidate_idx] <= ownership_view[winner_idx]:
        return score
    if resource_view[candidate_idx] <= resource_view[winner_idx]:
        return score
    if support_view[candidate_idx] <= support_view[winner_idx]:
        return score

    trace_view = _positive_rank_view(trace_mutation + trace_propagation)
    if trace_view[winner_idx] <= trace_view[candidate_idx]:
        return score

    mutation_view = _positive_rank_view(trace_mutation)
    propagation_view = _positive_rank_view(trace_propagation)
    if trace_surface_idx is not None and 0 <= trace_surface_idx < score.size:
        candidate_is_trace_covered = (
            trace_mask is not None
            and candidate_idx < trace_mask.size
            and bool(trace_mask[candidate_idx])
        )
        covered_mutation_owned = (
            winner_idx != trace_surface_idx
            and candidate_is_trace_covered
            and mutation_view[winner_idx] > mutation_view[candidate_idx]
            and mutation_view[winner_idx] > propagation_view[winner_idx]
        )
        if covered_mutation_owned:
            return score

    adjusted = score.astype(np.float64, copy=True)
    peak = float(np.max(adjusted))
    if not math.isfinite(peak) or peak <= 0.0:
        return score
    adjusted[candidate_idx] = np.nextafter(peak, math.inf)
    return adjusted


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


def score_crest_services(
    input_folder: Path,
    enabled_modalities: frozenset[str] = ALL_MODALITIES,
    graph_mode: str = "counterfactual",
    reliability_mode: str = "none",
    resource_mode: str = "none",
) -> pd.DataFrame:
    frames = _load_input_frames(input_folder)
    services = _collect_services_from_frames(frames)
    if not services:
        return pd.DataFrame(columns=["service", "A", "F", "S", "score"])

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
    trace_confidence = 1.0
    trace_scale = 1.0
    if (
        reliability_mode
        in {
            "trace_confidence",
            "modality_confidence",
            "trace_root_eligibility",
            "adaptive_modality",
            "surface_competition",
            "resource_provenance",
        }
        and "trace" in enabled_modalities
        and any(modality in enabled_modalities for modality in ("metric", "log"))
    ):
        trace_confidence, trace_scale = _incident_trace_structural_reliability(
            frames,
            services,
            role_matrix,
            enabled_features,
        )
        role_matrix = _apply_trace_confidence_gate(
            role_matrix,
            enabled_features,
            trace_scale,
        )
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
        structural_seed = _local_family_energy(
            role_matrix,
            enabled_features,
            include_topology=True,
        )
        context_weight = _trace_density_context_weight(services, trace_edges) * trace_scale
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

    score = local_abnormality * explanatory_power
    if graph_mode == "counterfactual":
        score = score + denoised_support
    if not np.any(score > 0.0) and np.any(local_abnormality > 0.0):
        score = local_abnormality.copy()
    families = _family_burdens(role_matrix, enabled_features)
    modality_confidences = {
        "metric_confidence": 0.0,
        "log_confidence": 0.0,
        "trace_modality_confidence": trace_scale,
    }
    trace_root_eligibility = np.zeros(len(services), dtype=np.float64)
    trace_symptom_pressure = np.zeros(len(services), dtype=np.float64)
    nontrace_root_ownership = np.zeros(len(services), dtype=np.float64)
    if reliability_mode in {
        "modality_confidence",
        "trace_root_eligibility",
        "adaptive_modality",
        "surface_competition",
    }:
        trace_mask, _trace_coverage, _trace_spread, _has_majority, trace_surface_idx = (
            _trace_service_mask_and_spread(frames, services)
        )
        score, modality_confidences = _modality_weighted_rank_fusion(
            score,
            families,
            enabled_modalities,
            trace_scale,
            trace_mask,
            trace_surface_idx,
        )
    adaptive_surface_pressure = np.zeros(len(services), dtype=np.float64)
    adaptive_nontrace_ownership = np.zeros(len(services), dtype=np.float64)
    surface_competition_ownership = np.zeros(len(services), dtype=np.float64)
    if (
        reliability_mode == "trace_root_eligibility"
        and "trace" in enabled_modalities
        and any(modality in enabled_modalities for modality in ("metric", "log"))
    ):
        trace_mask, trace_coverage, trace_spread, _has_majority, trace_surface_idx = (
            _trace_service_mask_and_spread(frames, services)
        )
        (
            score,
            trace_root_eligibility,
            trace_symptom_pressure,
            nontrace_root_ownership,
        ) = _apply_trace_root_eligibility_arbitration(
            score,
            families,
            trace_coverage,
            trace_spread,
            trace_mask,
            trace_surface_idx,
        )
    if (
        reliability_mode == "adaptive_modality"
        and "trace" in enabled_modalities
        and any(modality in enabled_modalities for modality in ("metric", "log"))
    ):
        _trace_mask, _trace_coverage, trace_spread, has_majority, trace_surface_idx = (
            _trace_service_mask_and_spread(frames, services)
        )
        (
            score,
            adaptive_surface_pressure,
            adaptive_nontrace_ownership,
        ) = _apply_adaptive_modality_surface_competition(
            score,
            families,
            trace_spread,
            has_majority,
            trace_surface_idx,
        )
    if (
        reliability_mode == "surface_competition"
        and "trace" in enabled_modalities
        and any(modality in enabled_modalities for modality in ("metric", "log"))
    ):
        _trace_mask, _trace_coverage, _trace_spread, has_majority, trace_surface_idx = (
            _trace_service_mask_and_spread(frames, services)
        )
        score, surface_competition_ownership = (
            _apply_broad_trace_surface_competition(
                score,
                families,
                has_majority,
                trace_surface_idx,
            )
        )
    resource_ownership = np.zeros(len(services), dtype=np.float64)
    resource_confidence = 0.0
    if resource_mode == "provenance" and "metric" in enabled_modalities:
        resource_ownership = _resource_provenance_ownership(frames, services)
        resource_confidence = _resource_provenance_confidence(resource_ownership)
        if resource_confidence > 0.0:
            trace_mask, _trace_coverage, _trace_spread, _has_majority, trace_surface_idx = (
                _trace_service_mask_and_spread(frames, services)
            )
            score = _apply_resource_provenance_arbitration(
                score,
                families,
                resource_ownership,
                trace_scale,
                trace_mask,
                trace_surface_idx,
            )

    result = pd.DataFrame(
        {
            "service": services,
            "A": local_abnormality,
            "F": explanatory_power,
            "S": denoised_support,
            "score": score,
            "trace_confidence": np.full(len(services), trace_confidence),
            "trace_scale": np.full(len(services), trace_scale),
            "metric_confidence": np.full(
                len(services), modality_confidences["metric_confidence"]
            ),
            "log_confidence": np.full(
                len(services), modality_confidences["log_confidence"]
            ),
            "trace_modality_confidence": np.full(
                len(services), modality_confidences["trace_modality_confidence"]
            ),
            "trace_root_eligibility": trace_root_eligibility,
            "trace_symptom_pressure": trace_symptom_pressure,
            "nontrace_root_ownership": nontrace_root_ownership,
            "adaptive_surface_pressure": adaptive_surface_pressure,
            "adaptive_nontrace_ownership": adaptive_nontrace_ownership,
            "surface_competition_ownership": surface_competition_ownership,
            "resource_provenance": resource_ownership,
            "resource_provenance_confidence": np.full(
                len(services),
                resource_confidence,
            ),
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
    _reliability_mode = "modality_confidence"
    _resource_mode = "none"

    def needs_cpu_count(self) -> int | None:
        return 1

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        ranking = score_crest_services(
            args.input_folder,
            enabled_modalities=self._modalities,
            graph_mode=self._graph_mode,
            reliability_mode=self._reliability_mode,
            resource_mode=self._resource_mode,
        )
        return [
            AlgorithmAnswer(level="service", name=str(row.service), rank=rank)
            for rank, row in enumerate(ranking.itertuples(index=False), start=1)
        ]


class CRESTLocal(CREST):
    """CREST-Local ablation: Module 1 only."""

    _graph_mode = "local"
    _reliability_mode = "none"


class CRESTNoCF(CREST):
    """CREST-NoCF ablation: local abnormality plus PageRank-style graph prior."""

    _graph_mode = "pagerank"
    _reliability_mode = "none"


class CRESTNoReliability(CREST):
    """CREST ablation without telemetry reliability gating."""

    _reliability_mode = "none"


class CRESTModalityConfidence(CREST):
    """CREST ablation with incident-local bounded modality confidence fusion."""

    _reliability_mode = "modality_confidence"


class CRESTResourceProvenance(CREST):
    """CREST ablation with metric resource provenance ownership arbitration."""

    _reliability_mode = "modality_confidence"
    _resource_mode = "provenance"


class CRESTTraceRootEligibility(CREST):
    """CREST ablation with trace root-eligibility arbitration."""

    _reliability_mode = "trace_root_eligibility"


class CRESTAdaptiveModality(CREST):
    """CREST ablation with incident-local adaptive modality selection."""

    _reliability_mode = "adaptive_modality"


class CRESTSurfaceCompetition(CREST):
    """CREST ablation with broad dominant trace-surface competition."""

    _reliability_mode = "surface_competition"


class CRESTMetric(CREST):
    """CREST ablation using only metric evidence."""

    _modalities = frozenset({"metric"})
    _reliability_mode = "none"


class CRESTTrace(CREST):
    """CREST ablation using only trace evidence."""

    _modalities = frozenset({"trace"})
    _reliability_mode = "none"


class CRESTLog(CREST):
    """CREST ablation using only log evidence."""

    _modalities = frozenset({"log"})
    _reliability_mode = "none"


class CRESTMetricTrace(CREST):
    """CREST ablation using metric and trace evidence."""

    _modalities = frozenset({"metric", "trace"})
    _reliability_mode = "none"


class CRESTMetricLog(CREST):
    """CREST ablation using metric and log evidence."""

    _modalities = frozenset({"metric", "log"})
    _reliability_mode = "none"


class CRESTLogTrace(CREST):
    """CREST ablation using log and trace evidence."""

    _modalities = frozenset({"log", "trace"})
    _reliability_mode = "none"
