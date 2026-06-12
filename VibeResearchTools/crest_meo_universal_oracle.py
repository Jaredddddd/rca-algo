"""Synthesize raw-telemetry Oracle operators for CREST-MEO.

This is an intentionally leaky, research-only upper-bound tool. It may read
service-level GT labels offline to select one global set of telemetry-derived
evidence operators, role assignments, and counterfactual mutation/propagation
sets. It must never be imported from the online algorithm path.

The key constraint is that GT is not used to construct feature values. Feature
values are computed only from raw normal/abnormal telemetry with universal
rules shared across every benchmark case.
"""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import re
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
import pyarrow.parquet as pq


REPO = Path(__file__).resolve().parents[1]
EVIDENCERANK_SRC = REPO / "algorithms/evidencerank/src"
sys.path.insert(0, str(EVIDENCERANK_SRC))

from evidencerank.cera import (  # noqa: E402
    ALL_MODALITIES,
    BASE_FEATURE_NAMES,
    MODALITY_FEATURES,
    _apply_arc_trace_endpoint_support_gate,
    _build_feature_matrix,
    _clean_service,
    _collect_services_from_frames,
    _load_input_frames,
    _series_service,
    _stable_template_id,
)
from evidencerank.crest import (  # noqa: E402
    CREST_DENOISED_CHANNEL_EXCLUDES,
    CREST_COUNTERFACTUAL_MUTATION_FEATURES,
    CREST_COUNTERFACTUAL_PROPAGATION_FEATURES,
    CREST_ROLE_FAMILIES,
    _apply_counterfactual_explain_away,
    _apply_counterfactual_explain_away_soft,
    _apply_parent_context,
    _robust_case_feature_matrix,
    _saturating_incident_scale,
    _trace_density_context_weight,
)
from evidencerank.meo.dsl.schema import EvidenceOperatorSpec  # noqa: E402
from evidencerank.meo.runtime.instantiate import ROLE_ORDER  # noqa: E402
from evidencerank.meo.runtime.load_meol import DEFAULT_MEOL_PATH, load_operator_specs  # noqa: E402


DEFAULT_DATA_ROOT = REPO / "data/rcabench-platform-v2/data"
DEFAULT_LABELS = REPO / "data/rcabench-platform-v2/meta/rcabench-csv/labels.csv"
DEFAULT_ARTIFACT = (
    REPO / "output/rcabench-platform-v2/crest_meo_oracle/oracle_evidence_operators.json"
)
DEFAULT_OUTPUT_ROOT = REPO / "output/rcabench-platform-v2/data"
DEFAULT_SUMMARY = (
    REPO
    / "output/rcabench-platform-v2/crest_meo_oracle/role_synthesis_reference_result_summary.json"
)
DEFAULT_CREST_EQUIVALENT_ARTIFACT = (
    REPO
    / "output/rcabench-platform-v2/crest_meo_oracle/crest_equivalent_evidence_operators.json"
)
DEFAULT_CREST_EQUIVALENT_SUMMARY = (
    REPO
    / "output/rcabench-platform-v2/crest_meo_oracle/crest_equivalent_reference_result_summary.json"
)

FEATURES = tuple(
    feature
    for feature in BASE_FEATURE_NAMES
    if feature
    in frozenset().union(*(MODALITY_FEATURES[modality] for modality in ALL_MODALITIES))
)
EPS = 1e-12
ROLE_DISABLED = -1
ROLE_NEUTRAL = len(ROLE_ORDER)
ROLE_TO_INDEX = {role: idx for idx, role in enumerate(ROLE_ORDER)}
INDEX_TO_ROLE = {idx: role for role, idx in ROLE_TO_INDEX.items()}
ROLE_VECTOR_CHOICES = (
    ROLE_DISABLED,
    ROLE_TO_INDEX["mutation"],
    ROLE_TO_INDEX["propagation"],
    ROLE_TO_INDEX["observability_bias"],
    ROLE_TO_INDEX["topology_context"],
)
CREST_EQUIVALENT_ROLE_CHOICES = (
    ROLE_DISABLED,
    ROLE_TO_INDEX["mutation"],
    ROLE_TO_INDEX["propagation"],
    ROLE_NEUTRAL,
)
SCORING_MODES = ("crest_equivalent", "role_vector")
_EVAL_RECORD_CHUNKS: list[list["CaseFeatures"]] = []
_EVAL_SCORING_MODE = "crest_equivalent"

TRACE_CATEGORICAL_ALIASES = (
    "span_name",
    "operation",
    "operation_name",
    "endpoint",
    "http_route",
    "route",
    "attr.status_code",
    "status_code",
    "status",
    "code",
    "http_status_code",
    "attr.http.response.status_code",
    "http.status_code",
    "attr.http.request.method",
    "http.method",
    "method",
    "attr.span_kind",
)
TRACE_STATUS_ALIASES = (
    "attr.http.response.status_code",
    "http.status_code",
    "status_code",
    "http_status_code",
    "attr.status_code",
    "status",
    "code",
)
TRACE_NUMERIC_ALIASES = (
    "duration",
    "duration_ms",
    "latency",
    "elapsed",
    "elapsed_ms",
    "attr.http.request.content_length",
    "attr.http.response.content_length",
)
LOG_CATEGORICAL_ALIASES = (
    "level",
    "severity",
    "log_level",
    "template",
    "log_template",
    "message_template",
    "event_template",
    "__message_template__",
)
LOG_MESSAGE_ALIASES = ("message", "msg", "body", "content", "log")


@dataclass(frozen=True)
class CandidateSpec:
    """One universal evidence operator candidate."""

    name: str
    source: str
    family: str
    signal_field: str
    signal_type: str
    contrast_operator: str
    aggregation_method: str
    seed_role: int
    initially_enabled: bool
    mechanism: str
    rationale: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class CaseFeatures:
    datapack: str
    services: tuple[str, ...]
    gt_mask: np.ndarray
    matrix: np.ndarray
    candidate_names: tuple[str, ...]
    runtime_feature_names: tuple[str, ...]
    trace_edges: tuple[tuple[str, str], ...]
    explain_edges: tuple[tuple[str, str], ...]
    context_weight: float


def _repo_path(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else REPO / path


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def _safe_name(value: str) -> str:
    text = re.sub(r"[^0-9A-Za-z_.]+", "_", str(value).strip())
    text = text.strip("._")
    return text or "field"


def _load_labels(labels_path: Path, dataset: str) -> dict[str, set[str]]:
    labels = pd.read_csv(labels_path)
    required = {"dataset", "datapack", "gt.level", "gt.name"}
    missing = required - set(labels.columns)
    if missing:
        raise SystemExit(f"Label file is missing columns: {sorted(missing)}")
    labels = labels[(labels["dataset"] == dataset) & (labels["gt.level"] == "service")]
    return {
        str(datapack): {str(name) for name in group["gt.name"].dropna()}
        for datapack, group in labels.groupby("datapack")
    }


def _feature_source(feature_name: str) -> str:
    for modality, feature_names in MODALITY_FEATURES.items():
        if feature_name in feature_names:
            return modality
    return "crest"


def _seed_role_for_crest_feature(feature_name: str) -> int:
    if feature_name in CREST_COUNTERFACTUAL_MUTATION_FEATURES:
        return ROLE_TO_INDEX["mutation"]
    if feature_name in CREST_COUNTERFACTUAL_PROPAGATION_FEATURES:
        return ROLE_TO_INDEX["propagation"]
    if feature_name in CREST_ROLE_FAMILIES["observability_volume"]:
        return ROLE_TO_INDEX["observability_bias"]
    if feature_name in CREST_ROLE_FAMILIES["topology_context"]:
        return ROLE_TO_INDEX["topology_context"]
    if feature_name in CREST_ROLE_FAMILIES["trace_propagation"]:
        return ROLE_TO_INDEX["propagation"]
    return ROLE_TO_INDEX["mutation"]


def _seed_role_from_prior(role_prior: dict[str, float]) -> int:
    clean = {
        role: float(value)
        for role, value in role_prior.items()
        if role in ROLE_TO_INDEX and math.isfinite(float(value))
    }
    if not clean or max(clean.values()) <= 0.0:
        return ROLE_DISABLED
    return ROLE_TO_INDEX[max(clean.items(), key=lambda item: (item[1], item[0]))[0]]


def _raw_seed_role(source: str, signal_field: str, contrast_operator: str) -> int:
    field = signal_field.lower()
    op = contrast_operator.lower()
    if source == "topology":
        return ROLE_TO_INDEX["topology_context"]
    if "count_drop" in op or "error_rate" in op or "status" in field or "endpoint" in field or "route" in field or "span_name" in field:
        return ROLE_TO_INDEX["mutation"]
    if "duration" in field or "latency" in field or "elapsed" in field or "count_rise" in op:
        return ROLE_TO_INDEX["propagation"]
    if source == "metric":
        return ROLE_TO_INDEX["mutation"]
    if source == "log":
        return ROLE_TO_INDEX["propagation"]
    return ROLE_TO_INDEX["mutation"]


def _role_name(role_idx: int) -> str:
    if int(role_idx) == ROLE_DISABLED:
        return "disabled"
    if int(role_idx) == ROLE_NEUTRAL:
        return "neutral"
    return INDEX_TO_ROLE.get(int(role_idx), "disabled")


def _role_choices(scoring_mode: str) -> tuple[int, ...]:
    if scoring_mode == "crest_equivalent":
        return CREST_EQUIVALENT_ROLE_CHOICES
    return ROLE_VECTOR_CHOICES


def _coerce_role_for_scoring(role_idx: int, scoring_mode: str) -> int:
    role_idx = int(role_idx)
    if role_idx < 0:
        return ROLE_DISABLED
    if scoring_mode != "crest_equivalent":
        return role_idx
    if role_idx in (ROLE_TO_INDEX["mutation"], ROLE_TO_INDEX["propagation"]):
        return role_idx
    return ROLE_NEUTRAL


def _initial_role_for_scoring(spec: CandidateSpec, scoring_mode: str) -> int:
    if not spec.initially_enabled:
        return ROLE_DISABLED
    if scoring_mode == "crest_equivalent" and spec.seed_role < 0:
        return ROLE_NEUTRAL
    return _coerce_role_for_scoring(spec.seed_role, scoring_mode)


def _runtime_feature_name(spec: CandidateSpec) -> str:
    if spec.family in {"crest_feature", "meol_operator"}:
        base_operator = str(spec.metadata.get("base_operator", ""))
        if base_operator in FEATURES:
            return base_operator
    return spec.name


def _candidate(
    *,
    name: str,
    source: str,
    family: str,
    signal_field: str,
    signal_type: str,
    contrast_operator: str,
    aggregation_method: str,
    seed_role: int | None = None,
    initially_enabled: bool = False,
    mechanism: str,
    rationale: str,
    metadata: dict[str, Any] | None = None,
) -> CandidateSpec:
    return CandidateSpec(
        name=name,
        source=source,
        family=family,
        signal_field=signal_field,
        signal_type=signal_type,
        contrast_operator=contrast_operator,
        aggregation_method=aggregation_method,
        seed_role=(
            _raw_seed_role(source, signal_field, contrast_operator)
            if seed_role is None
            else seed_role
        ),
        initially_enabled=initially_enabled,
        mechanism=mechanism,
        rationale=rationale,
        metadata=metadata or {},
    )


def _discover_metric_names(
    data_root: Path,
    dataset: str,
    datapacks: list[str],
    *,
    max_scan_cases: int,
    max_metric_names: int,
    min_case_coverage: int,
) -> list[str]:
    counts: dict[str, int] = {}
    for datapack in datapacks[: max(0, max_scan_cases)]:
        seen: set[str] = set()
        case_dir = data_root / dataset / datapack
        for frame_name in ("normal_metrics", "abnormal_metrics"):
            path = case_dir / f"{frame_name}.parquet"
            if not path.exists():
                continue
            try:
                frame = pd.read_parquet(path, columns=["metric"])
            except Exception:
                continue
            seen.update(str(value) for value in frame["metric"].dropna().unique())
        for metric_name in seen:
            counts[metric_name] = counts.get(metric_name, 0) + 1
    filtered = [
        (metric_name, count)
        for metric_name, count in counts.items()
        if count >= max(1, min_case_coverage)
    ]
    filtered.sort(key=lambda item: (-item[1], item[0]))
    return [metric_name for metric_name, _count in filtered[:max_metric_names]]


def _discover_columns(
    data_root: Path,
    dataset: str,
    datapacks: list[str],
    frame_name: str,
    aliases: tuple[str, ...],
    *,
    max_scan_cases: int,
    min_case_coverage: int,
) -> list[str]:
    counts: dict[str, int] = {}
    alias_set = set(aliases)
    for datapack in datapacks[: max(0, max_scan_cases)]:
        path = data_root / dataset / datapack / f"{frame_name}.parquet"
        if not path.exists():
            continue
        try:
            columns = set(pq.read_schema(path).names)
        except Exception:
            continue
        for column in sorted(alias_set & columns):
            counts[column] = counts.get(column, 0) + 1
    filtered = [
        (column, count)
        for column, count in counts.items()
        if count >= max(1, min_case_coverage)
    ]
    filtered.sort(key=lambda item: (-item[1], item[0]))
    return [column for column, _count in filtered]


def _build_candidate_specs(
    data_root: Path,
    dataset: str,
    datapacks: list[str],
    meol_path: Path,
    *,
    max_scan_cases: int,
    max_metric_names: int,
    min_case_coverage: int,
) -> tuple[list[CandidateSpec], list[EvidenceOperatorSpec]]:
    specs: list[CandidateSpec] = []

    for feature_name in FEATURES:
        source = _feature_source(feature_name)
        specs.append(
            _candidate(
                name=f"crest::{feature_name}",
                source=source,
                family="crest_feature",
                signal_field=feature_name,
                signal_type="derived",
                contrast_operator="crest_builtin",
                aggregation_method="crest_builtin",
                seed_role=_seed_role_for_crest_feature(feature_name),
                initially_enabled=True,
                mechanism="current CREST telemetry feature",
                rationale="Existing deterministic CREST evidence feature used as a synthesis candidate.",
                metadata={"base_operator": feature_name},
            )
        )

    meo_specs = load_operator_specs(meol_path)
    for spec in meo_specs:
        specs.append(
            _candidate(
                name=f"meol::{spec.name}",
                source=spec.source,
                family="meol_operator",
                signal_field=spec.signal.field,
                signal_type=spec.signal.type,
                contrast_operator=spec.contrast.operator,
                aggregation_method=spec.aggregation.method,
                seed_role=_seed_role_from_prior(spec.role_prior),
                initially_enabled=True,
                mechanism=spec.mechanism,
                rationale=spec.rationale,
                metadata={
                    "base_operator": spec.name,
                    "entity": spec.entity,
                    "required_fields": list(spec.required_fields),
                    "original_role_prior": spec.role_prior,
                },
            )
        )

    metric_names = _discover_metric_names(
        data_root,
        dataset,
        datapacks,
        max_scan_cases=max_scan_cases,
        max_metric_names=max_metric_names,
        min_case_coverage=min_case_coverage,
    )
    for metric_name in metric_names:
        safe_metric = _safe_name(metric_name)
        for op in ("z_shift", "robust_z_shift", "mean_delta"):
            specs.append(
                _candidate(
                    name=f"raw_metric::{safe_metric}::{op}",
                    source="metric",
                    family="raw_metric_value",
                    signal_field=metric_name,
                    signal_type="value",
                    contrast_operator=op,
                    aggregation_method="service_metric",
                    mechanism="metric-specific normality shift",
                    rationale="Metric-name-specific value shift synthesized from raw telemetry schema.",
                    metadata={"metric_name": metric_name},
                )
            )

    for source in ("metric", "trace", "log"):
        for op in ("count_delta", "count_rise", "count_drop"):
            specs.append(
                _candidate(
                    name=f"raw_{source}::row_count::{op}",
                    source=source,
                    family=f"raw_{source}_row_count",
                    signal_field="__row_count__",
                    signal_type="count",
                    contrast_operator=op,
                    aggregation_method="service_count",
                    mechanism=f"{source} observation-volume shift",
                    rationale=f"Service-level {source} row-count shift from raw telemetry.",
                )
            )

    trace_categorical = _discover_columns(
        data_root,
        dataset,
        datapacks,
        "normal_traces",
        TRACE_CATEGORICAL_ALIASES,
        max_scan_cases=max_scan_cases,
        min_case_coverage=min_case_coverage,
    )
    for column in trace_categorical:
        safe_column = _safe_name(column)
        specs.append(
            _candidate(
                name=f"raw_trace::{safe_column}::distribution_shift",
                source="trace",
                family="raw_trace_categorical",
                signal_field=column,
                signal_type="categorical",
                contrast_operator="distribution_shift",
                aggregation_method="jsd",
                mechanism="trace categorical distribution shift",
                rationale="Service-level categorical trace-field shift synthesized from raw telemetry.",
                metadata={"column": column},
            )
        )
        if column in TRACE_STATUS_ALIASES:
            specs.append(
                _candidate(
                    name=f"raw_trace::{safe_column}::error_rate_delta",
                    source="trace",
                    family="raw_trace_error_rate",
                    signal_field=column,
                    signal_type="rate",
                    contrast_operator="error_rate_delta",
                    aggregation_method="ratio",
                    mechanism="trace status error-rate shift",
                    rationale="Service-level error-rate delta synthesized from status-like trace fields.",
                    metadata={"column": column},
                )
            )

    trace_numeric = _discover_columns(
        data_root,
        dataset,
        datapacks,
        "normal_traces",
        TRACE_NUMERIC_ALIASES,
        max_scan_cases=max_scan_cases,
        min_case_coverage=min_case_coverage,
    )
    for column in trace_numeric:
        safe_column = _safe_name(column)
        for op in ("z_shift", "robust_z_shift", "mean_delta"):
            specs.append(
                _candidate(
                    name=f"raw_trace::{safe_column}::{op}",
                    source="trace",
                    family="raw_trace_numeric",
                    signal_field=column,
                    signal_type="value",
                    contrast_operator=op,
                    aggregation_method="service_numeric",
                    mechanism="trace numeric value shift",
                    rationale="Service-level numeric trace-field shift synthesized from raw telemetry.",
                    metadata={"column": column},
                )
            )

    log_categorical = _discover_columns(
        data_root,
        dataset,
        datapacks,
        "normal_logs",
        LOG_CATEGORICAL_ALIASES + LOG_MESSAGE_ALIASES,
        max_scan_cases=max_scan_cases,
        min_case_coverage=min_case_coverage,
    )
    if any(column in LOG_MESSAGE_ALIASES for column in log_categorical):
        log_categorical.append("__message_template__")
    for column in sorted(set(log_categorical)):
        safe_column = _safe_name(column)
        specs.append(
            _candidate(
                name=f"raw_log::{safe_column}::distribution_shift",
                source="log",
                family="raw_log_categorical",
                signal_field=column,
                signal_type="categorical",
                contrast_operator="distribution_shift",
                aggregation_method="jsd",
                mechanism="log categorical distribution shift",
                rationale="Service-level log categorical/template shift synthesized from raw telemetry.",
                metadata={"column": column},
            )
        )

    for op in ("count_delta", "count_rise", "count_drop"):
        specs.append(
            _candidate(
                name=f"raw_topology::edge_count::{op}",
                source="topology",
                family="raw_topology_edge_count",
                signal_field="edge_count",
                signal_type="count",
                contrast_operator=op,
                aggregation_method="service_edge_count",
                mechanism="trace topology edge-volume shift",
                rationale="Service-level raw trace edge-count shift.",
            )
        )
    for column in ("caller_distribution", "callee_distribution"):
        specs.append(
            _candidate(
                name=f"raw_topology::{column}::distribution_shift",
                source="topology",
                family="raw_topology_distribution",
                signal_field=column,
                signal_type="categorical",
                contrast_operator="distribution_shift",
                aggregation_method="jsd",
                mechanism="trace topology neighbor distribution shift",
                rationale="Service-level caller/callee distribution shift from raw trace edges.",
            )
        )

    deduped: dict[str, CandidateSpec] = {}
    for spec in specs:
        deduped.setdefault(spec.name, spec)
    return list(deduped.values()), meo_specs


def _finite_nonnegative(values: np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    return np.maximum(arr, 0.0)


def _count_op(normal_count: float, abnormal_count: float, op: str) -> float:
    normal_count = max(float(normal_count), 0.0)
    abnormal_count = max(float(abnormal_count), 0.0)
    if op == "count_delta":
        return abs(abnormal_count - normal_count) / (normal_count + EPS)
    if op == "count_rise":
        return max(0.0, abnormal_count - normal_count) / (normal_count + EPS)
    if op == "count_drop":
        return max(0.0, normal_count - abnormal_count) / (normal_count + EPS)
    return 0.0


def _js_divergence_from_counts(left: pd.Series, right: pd.Series) -> float:
    categories = sorted(set(left.index.astype(str)) | set(right.index.astype(str)))
    if not categories:
        return 0.0
    p = np.asarray([float(left.get(category, 0.0)) for category in categories])
    q = np.asarray([float(right.get(category, 0.0)) for category in categories])
    if p.sum() <= EPS and q.sum() <= EPS:
        return 0.0
    p = p / (p.sum() + EPS)
    q = q / (q.sum() + EPS)
    m = 0.5 * (p + q)

    def kl(a: np.ndarray, b: np.ndarray) -> float:
        mask = a > EPS
        if not np.any(mask):
            return 0.0
        return float(np.sum(a[mask] * np.log((a[mask] + EPS) / (b[mask] + EPS))))

    value = 0.5 * kl(p, m) + 0.5 * kl(q, m)
    return value if math.isfinite(value) and value > 0.0 else 0.0


def _is_error_status(value: Any) -> bool:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return False
    try:
        code = int(float(value))
        return code >= 400
    except Exception:
        text = str(value).lower()
        return (
            "error" in text
            or "fail" in text
            or "timeout" in text
            or text.startswith("5")
            or text.startswith("4")
        )


def _prepare_service_frame(frame: pd.DataFrame) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame()
    data = frame.copy()
    data["service_name"] = _series_service(data)
    return data.dropna(subset=["service_name"])


def _prepare_frames(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {
        "normal_metrics": _prepare_service_frame(frames.get("normal_metrics", pd.DataFrame())),
        "abnormal_metrics": _prepare_service_frame(frames.get("abnormal_metrics", pd.DataFrame())),
        "normal_traces": _prepare_service_frame(frames.get("normal_traces", pd.DataFrame())),
        "abnormal_traces": _prepare_service_frame(frames.get("abnormal_traces", pd.DataFrame())),
        "normal_logs": _prepare_service_frame(frames.get("normal_logs", pd.DataFrame())),
        "abnormal_logs": _prepare_service_frame(frames.get("abnormal_logs", pd.DataFrame())),
    }


def _numeric_shift_feature(
    normal: pd.DataFrame,
    abnormal: pd.DataFrame,
    services: list[str],
    column: str,
    op: str,
) -> np.ndarray:
    if normal.empty or abnormal.empty or column not in normal.columns or column not in abnormal.columns:
        return np.zeros(len(services), dtype=np.float64)
    normal_values = normal[["service_name", column]].copy()
    abnormal_values = abnormal[["service_name", column]].copy()
    normal_values[column] = pd.to_numeric(normal_values[column], errors="coerce")
    abnormal_values[column] = pd.to_numeric(abnormal_values[column], errors="coerce")
    normal_values = normal_values.dropna(subset=[column])
    abnormal_values = abnormal_values.dropna(subset=[column])
    if normal_values.empty or abnormal_values.empty:
        return np.zeros(len(services), dtype=np.float64)

    n_group = normal_values.groupby("service_name")[column]
    a_group = abnormal_values.groupby("service_name")[column]
    n_mean = n_group.mean()
    n_std = n_group.std().fillna(0.0)
    n_median = n_group.median()
    n_q25 = n_group.quantile(0.25)
    n_q75 = n_group.quantile(0.75)
    a_mean = a_group.mean()

    out = np.zeros(len(services), dtype=np.float64)
    for idx, service in enumerate(services):
        if service not in a_mean.index or service not in n_mean.index:
            continue
        if op == "z_shift":
            denom = float(n_std.get(service, 0.0))
            if denom <= EPS:
                continue
            value = abs(float(a_mean[service]) - float(n_mean[service])) / (denom + EPS)
        elif op == "robust_z_shift":
            iqr = float(n_q75.get(service, 0.0)) - float(n_q25.get(service, 0.0))
            if iqr <= EPS:
                continue
            value = abs(float(a_mean[service]) - float(n_median[service])) / (iqr + EPS)
        elif op == "mean_delta":
            value = abs(float(a_mean[service]) - float(n_mean[service])) / (
                abs(float(n_mean[service])) + 1.0
            )
        else:
            value = 0.0
        out[idx] = value if math.isfinite(value) and value > 0.0 else 0.0
    return out


def _metric_name_feature(
    normal_metrics: pd.DataFrame,
    abnormal_metrics: pd.DataFrame,
    services: list[str],
    metric_name: str,
    op: str,
) -> np.ndarray:
    if normal_metrics.empty or abnormal_metrics.empty or "metric" not in normal_metrics.columns or "metric" not in abnormal_metrics.columns:
        return np.zeros(len(services), dtype=np.float64)
    normal = normal_metrics[normal_metrics["metric"].astype(str) == str(metric_name)]
    abnormal = abnormal_metrics[abnormal_metrics["metric"].astype(str) == str(metric_name)]
    return _numeric_shift_feature(normal, abnormal, services, "value", op)


def _row_count_feature(
    normal: pd.DataFrame,
    abnormal: pd.DataFrame,
    services: list[str],
    op: str,
) -> np.ndarray:
    normal_counts = normal.groupby("service_name").size() if not normal.empty else pd.Series(dtype="float64")
    abnormal_counts = abnormal.groupby("service_name").size() if not abnormal.empty else pd.Series(dtype="float64")
    return np.asarray(
        [
            _count_op(
                float(normal_counts.get(service, 0.0)),
                float(abnormal_counts.get(service, 0.0)),
                op,
            )
            for service in services
        ],
        dtype=np.float64,
    )


def _categorical_shift_feature(
    normal: pd.DataFrame,
    abnormal: pd.DataFrame,
    services: list[str],
    column: str,
) -> np.ndarray:
    if normal.empty or abnormal.empty:
        return np.zeros(len(services), dtype=np.float64)
    if column == "__message_template__":
        message_col = next((col for col in LOG_MESSAGE_ALIASES if col in normal.columns or col in abnormal.columns), None)
        if message_col is None:
            return np.zeros(len(services), dtype=np.float64)
        normal = normal.copy()
        abnormal = abnormal.copy()
        normal[column] = normal[message_col].map(_stable_template_id) if message_col in normal.columns else ""
        abnormal[column] = abnormal[message_col].map(_stable_template_id) if message_col in abnormal.columns else ""
    elif column not in normal.columns or column not in abnormal.columns:
        return np.zeros(len(services), dtype=np.float64)

    normal_data = normal[["service_name", column]].dropna()
    abnormal_data = abnormal[["service_name", column]].dropna()
    if normal_data.empty or abnormal_data.empty:
        return np.zeros(len(services), dtype=np.float64)
    normal_data[column] = normal_data[column].astype(str)
    abnormal_data[column] = abnormal_data[column].astype(str)
    normal_counts = normal_data.groupby(["service_name", column]).size()
    abnormal_counts = abnormal_data.groupby(["service_name", column]).size()
    normal_service_counts = normal_data.groupby("service_name").size()
    abnormal_service_counts = abnormal_data.groupby("service_name").size()

    out = np.zeros(len(services), dtype=np.float64)
    for idx, service in enumerate(services):
        if normal_service_counts.get(service, 0) < 5 or abnormal_service_counts.get(service, 0) < 5:
            continue
        try:
            n_counts = normal_counts.xs(service, level="service_name")
        except KeyError:
            n_counts = pd.Series(dtype="float64")
        try:
            a_counts = abnormal_counts.xs(service, level="service_name")
        except KeyError:
            a_counts = pd.Series(dtype="float64")
        out[idx] = _js_divergence_from_counts(n_counts, a_counts)
    return out


def _error_rate_feature(
    normal: pd.DataFrame,
    abnormal: pd.DataFrame,
    services: list[str],
    column: str,
) -> np.ndarray:
    if normal.empty or abnormal.empty or column not in normal.columns or column not in abnormal.columns:
        return np.zeros(len(services), dtype=np.float64)
    normal_data = normal[["service_name", column]].dropna().copy()
    abnormal_data = abnormal[["service_name", column]].dropna().copy()
    if normal_data.empty or abnormal_data.empty:
        return np.zeros(len(services), dtype=np.float64)
    normal_data["_is_error"] = normal_data[column].map(_is_error_status)
    abnormal_data["_is_error"] = abnormal_data[column].map(_is_error_status)
    normal_rates = normal_data.groupby("service_name")["_is_error"].mean()
    abnormal_rates = abnormal_data.groupby("service_name")["_is_error"].mean()
    out = np.zeros(len(services), dtype=np.float64)
    for idx, service in enumerate(services):
        if service not in normal_rates.index or service not in abnormal_rates.index:
            continue
        n_rate = float(normal_rates[service])
        a_rate = float(abnormal_rates[service])
        value = abs(a_rate - n_rate)
        out[idx] = value if math.isfinite(value) and value > 0.0 else 0.0
    return out


def _derive_trace_edges(frame: pd.DataFrame) -> list[tuple[str, str]]:
    if frame.empty:
        return []
    data = frame.copy()
    data["service_name"] = _series_service(data)
    if "parent_service" not in data.columns and {"span_id", "parent_span_id", "service_name"}.issubset(data.columns):
        span_to_service = {
            span_id: service
            for span_id, service in data[["span_id", "service_name"]].itertuples(index=False, name=None)
            if _clean_service(span_id) is not None and _clean_service(service) is not None
        }
        data["parent_service"] = data["parent_span_id"].map(span_to_service)
    if "parent_service" not in data.columns:
        return []
    data["parent_service"] = data["parent_service"].map(_clean_service)
    return [
        (str(parent), str(child))
        for parent, child in data[["parent_service", "service_name"]].dropna().itertuples(index=False, name=None)
        if parent and child and str(parent) != str(child)
    ]


def _topology_edge_count_feature(
    normal_traces: pd.DataFrame,
    abnormal_traces: pd.DataFrame,
    services: list[str],
    op: str,
) -> np.ndarray:
    normal_edges = _derive_trace_edges(normal_traces)
    abnormal_edges = _derive_trace_edges(abnormal_traces)

    def counts(edges: list[tuple[str, str]]) -> dict[str, float]:
        result: dict[str, float] = {}
        for parent, child in edges:
            result[parent] = result.get(parent, 0.0) + 1.0
            result[child] = result.get(child, 0.0) + 1.0
        return result

    n_counts = counts(normal_edges)
    a_counts = counts(abnormal_edges)
    return np.asarray(
        [
            _count_op(n_counts.get(service, 0.0), a_counts.get(service, 0.0), op)
            for service in services
        ],
        dtype=np.float64,
    )


def _topology_distribution_feature(
    normal_traces: pd.DataFrame,
    abnormal_traces: pd.DataFrame,
    services: list[str],
    field: str,
) -> np.ndarray:
    normal_edges = _derive_trace_edges(normal_traces)
    abnormal_edges = _derive_trace_edges(abnormal_traces)
    out = np.zeros(len(services), dtype=np.float64)
    for idx, service in enumerate(services):
        if field == "caller_distribution":
            n_values = [parent for parent, child in normal_edges if child == service]
            a_values = [parent for parent, child in abnormal_edges if child == service]
        else:
            n_values = [child for parent, child in normal_edges if parent == service]
            a_values = [child for parent, child in abnormal_edges if parent == service]
        if len(n_values) < 5 or len(a_values) < 5:
            continue
        out[idx] = _js_divergence_from_counts(
            pd.Series(n_values).value_counts(),
            pd.Series(a_values).value_counts(),
        )
    return out


def _raw_feature_values(
    spec: CandidateSpec,
    prepared_frames: dict[str, pd.DataFrame],
    services: list[str],
) -> np.ndarray:
    normal_metrics = prepared_frames["normal_metrics"]
    abnormal_metrics = prepared_frames["abnormal_metrics"]
    normal_traces = prepared_frames["normal_traces"]
    abnormal_traces = prepared_frames["abnormal_traces"]
    normal_logs = prepared_frames["normal_logs"]
    abnormal_logs = prepared_frames["abnormal_logs"]

    if spec.family == "raw_metric_value":
        return _metric_name_feature(
            normal_metrics,
            abnormal_metrics,
            services,
            str(spec.metadata["metric_name"]),
            spec.contrast_operator,
        )
    if spec.family == "raw_metric_row_count":
        return _row_count_feature(normal_metrics, abnormal_metrics, services, spec.contrast_operator)
    if spec.family == "raw_trace_row_count":
        return _row_count_feature(normal_traces, abnormal_traces, services, spec.contrast_operator)
    if spec.family == "raw_log_row_count":
        return _row_count_feature(normal_logs, abnormal_logs, services, spec.contrast_operator)
    if spec.family == "raw_trace_categorical":
        return _categorical_shift_feature(
            normal_traces,
            abnormal_traces,
            services,
            str(spec.metadata["column"]),
        )
    if spec.family == "raw_trace_error_rate":
        return _error_rate_feature(
            normal_traces,
            abnormal_traces,
            services,
            str(spec.metadata["column"]),
        )
    if spec.family == "raw_trace_numeric":
        return _numeric_shift_feature(
            normal_traces,
            abnormal_traces,
            services,
            str(spec.metadata["column"]),
            spec.contrast_operator,
        )
    if spec.family == "raw_log_categorical":
        return _categorical_shift_feature(
            normal_logs,
            abnormal_logs,
            services,
            str(spec.metadata["column"]),
        )
    if spec.family == "raw_topology_edge_count":
        return _topology_edge_count_feature(
            normal_traces,
            abnormal_traces,
            services,
            spec.contrast_operator,
        )
    if spec.family == "raw_topology_distribution":
        return _topology_distribution_feature(
            normal_traces,
            abnormal_traces,
            services,
            spec.signal_field,
        )
    return np.zeros(len(services), dtype=np.float64)


def _extract_case_features(
    data_root: Path,
    dataset: str,
    datapack: str,
    gt_services: set[str],
    specs: list[CandidateSpec],
    meo_specs: list[EvidenceOperatorSpec],
    scoring_mode: str,
) -> CaseFeatures:
    case_dir = data_root / dataset / datapack
    if not case_dir.exists():
        raise FileNotFoundError(_relative(case_dir))
    frames = _load_input_frames(case_dir)
    prepared_frames = _prepare_frames(frames)
    services = _collect_services_from_frames(frames)
    if not services:
        raise ValueError("no_services")
    gt_mask = np.asarray([service in gt_services for service in services], dtype=bool)

    crest_matrix, trace_edges = _build_feature_matrix(
        frames,
        services,
        FEATURES,
        ALL_MODALITIES,
        normalize=True,
    )

    historical_gated_crest = (
        _apply_arc_trace_endpoint_support_gate(
            FEATURES,
            _robust_case_feature_matrix(crest_matrix),
        )
        if scoring_mode == "role_vector"
        else None
    )

    columns: list[np.ndarray] = []
    candidate_names: list[str] = []
    runtime_feature_names: list[str] = []
    for spec in specs:
        try:
            if spec.family == "crest_feature":
                feature_name = str(spec.metadata["base_operator"])
                values = (
                    historical_gated_crest[:, FEATURES.index(feature_name)]
                    if historical_gated_crest is not None
                    else crest_matrix[:, FEATURES.index(feature_name)]
                )
            elif spec.family == "meol_operator":
                feature_name = str(spec.metadata["base_operator"])
                values = (
                    (
                        historical_gated_crest[:, FEATURES.index(feature_name)]
                        if historical_gated_crest is not None
                        else crest_matrix[:, FEATURES.index(feature_name)]
                    )
                    if feature_name in FEATURES
                    else np.zeros(len(services), dtype=np.float64)
                )
            else:
                values = _raw_feature_values(spec, prepared_frames, services)
        except Exception:
            values = np.zeros(len(services), dtype=np.float64)
        columns.append(_finite_nonnegative(values))
        candidate_names.append(spec.name)
        runtime_feature_names.append(_runtime_feature_name(spec))

    matrix = (
        np.stack(columns, axis=1).astype(np.float32, copy=False)
        if columns
        else np.zeros((len(services), 0), dtype=np.float32)
    )
    matrix = _robust_case_feature_matrix(matrix)
    if scoring_mode == "crest_equivalent":
        matrix = _apply_arc_trace_endpoint_support_gate(
            tuple(runtime_feature_names),
            matrix,
        )
    matrix = matrix.astype(np.float32, copy=False)
    services_tuple = tuple(services)
    trace_edges_tuple = tuple(trace_edges)
    explain_edges = tuple(sorted(set(trace_edges_tuple)))
    return CaseFeatures(
        datapack=datapack,
        services=services_tuple,
        gt_mask=gt_mask,
        matrix=matrix,
        candidate_names=tuple(candidate_names),
        runtime_feature_names=tuple(runtime_feature_names),
        trace_edges=trace_edges_tuple,
        explain_edges=explain_edges,
        context_weight=_trace_density_context_weight(services, list(trace_edges_tuple)),
    )


def _worker(
    args: tuple[
        Path,
        str,
        str,
        set[str],
        list[CandidateSpec],
        list[EvidenceOperatorSpec],
        str,
    ],
) -> CaseFeatures | dict[str, Any]:
    data_root, dataset, datapack, gt_services, specs, meo_specs, scoring_mode = args
    try:
        return _extract_case_features(
            data_root,
            dataset,
            datapack,
            gt_services,
            specs,
            meo_specs,
            scoring_mode,
        )
    except Exception as exc:
        return {
            "datapack": datapack,
            "error": f"{type(exc).__name__}:{exc}",
        }


def _role_vectors(record: CaseFeatures, roles: np.ndarray) -> dict[str, np.ndarray]:
    row_count = int(record.matrix.shape[0]) if record.matrix.ndim == 2 else 0
    zeros = np.zeros(row_count, dtype=np.float64)
    if record.matrix.ndim != 2 or record.matrix.shape[1] == 0:
        return {role: zeros.copy() for role in ROLE_ORDER}

    vectors: dict[str, np.ndarray] = {}
    for role_name, role_idx in ROLE_TO_INDEX.items():
        mask = roles == role_idx
        if not np.any(mask):
            vectors[role_name] = zeros.copy()
            continue
        vectors[role_name] = _finite_nonnegative(
            np.sum(record.matrix[:, mask], axis=1, dtype=np.float64)
        )
    return vectors


def _score_record_role_vector(record: CaseFeatures, roles: np.ndarray) -> np.ndarray:
    vectors = _role_vectors(record, roles)
    mutation = vectors["mutation"]
    propagation = vectors["propagation"]
    observability_bias = vectors["observability_bias"]
    topology_context = vectors["topology_context"]
    local_energy = _finite_nonnegative(mutation + propagation + observability_bias + topology_context)
    local_abnormality = _saturating_incident_scale(local_energy)
    if not np.any(local_abnormality > 0.0):
        return local_abnormality

    structural_energy = _apply_parent_context(
        record.services,
        local_energy,
        record.trace_edges,
        record.context_weight,
    )
    structural_energy = _apply_counterfactual_explain_away_soft(
        record.services,
        np.maximum(structural_energy, 0.0),
        mutation,
        propagation,
        record.explain_edges,
    )
    explanatory_power = _saturating_incident_scale(structural_energy)
    denoised_support = _saturating_incident_scale(_finite_nonnegative(mutation + propagation))
    score = local_abnormality * explanatory_power + denoised_support
    if not np.any(score > 0.0):
        score = local_abnormality
    return _finite_nonnegative(score)


def _score_record_crest_equivalent(record: CaseFeatures, roles: np.ndarray) -> np.ndarray:
    if record.matrix.ndim != 2 or record.matrix.shape[1] == 0:
        return np.zeros(len(record.services), dtype=np.float64)

    enabled_indices = [
        idx
        for idx, role_idx in enumerate(roles)
        if int(role_idx) >= 0 and idx < record.matrix.shape[1]
    ]
    if not enabled_indices:
        return np.zeros(len(record.services), dtype=np.float64)

    role_matrix = _finite_nonnegative(record.matrix[:, enabled_indices])
    enabled_features = tuple(record.candidate_names[idx] for idx in enabled_indices)
    runtime_features = tuple(record.runtime_feature_names[idx] for idx in enabled_indices)
    local_energy = _finite_nonnegative(np.sum(role_matrix, axis=1, dtype=np.float64))
    local_abnormality = _saturating_incident_scale(local_energy)
    if not np.any(local_abnormality > 0.0):
        return local_abnormality

    mutation_features = frozenset(
        record.candidate_names[idx]
        for idx in enabled_indices
        if int(roles[idx]) == ROLE_TO_INDEX["mutation"]
    )
    propagation_features = frozenset(
        record.candidate_names[idx]
        for idx in enabled_indices
        if int(roles[idx]) == ROLE_TO_INDEX["propagation"]
    )

    structural_energy = _apply_parent_context(
        record.services,
        local_energy,
        record.trace_edges,
        record.context_weight,
    )
    structural_energy = _apply_counterfactual_explain_away(
        record.services,
        np.maximum(structural_energy, 0.0),
        role_matrix,
        enabled_features,
        record.explain_edges,
        mutation_features,
        propagation_features,
    )
    explanatory_power = _saturating_incident_scale(structural_energy)

    denoised_indices = [
        idx
        for idx, feature_name in enumerate(runtime_features)
        if feature_name not in CREST_DENOISED_CHANNEL_EXCLUDES
    ]
    denoised_energy = (
        role_matrix[:, denoised_indices].sum(axis=1).astype(np.float64)
        if denoised_indices
        else np.zeros(role_matrix.shape[0], dtype=np.float64)
    )
    denoised_structural = _apply_parent_context(
        record.services,
        denoised_energy,
        record.trace_edges,
        record.context_weight,
    )
    denoised_structural = _apply_counterfactual_explain_away(
        record.services,
        np.maximum(denoised_structural, 0.0),
        role_matrix,
        enabled_features,
        record.explain_edges,
        mutation_features,
        propagation_features,
    )
    denoised_support = _saturating_incident_scale(denoised_structural)

    score = local_abnormality * explanatory_power + denoised_support
    if not np.any(score > 0.0):
        score = local_abnormality
    return _finite_nonnegative(score)


def _score_record(
    record: CaseFeatures,
    roles: np.ndarray,
    scoring_mode: str,
) -> np.ndarray:
    if scoring_mode == "crest_equivalent":
        return _score_record_crest_equivalent(record, roles)
    return _score_record_role_vector(record, roles)


def _rank_order(services: tuple[str, ...], scores: np.ndarray) -> list[int]:
    clean_scores = _finite_nonnegative(scores)
    return sorted(range(len(services)), key=lambda idx: (-float(clean_scores[idx]), services[idx]))


def _case_rank(
    record: CaseFeatures,
    roles: np.ndarray,
    scoring_mode: str,
) -> tuple[int, str | None]:
    if record.matrix.size == 0 or not np.any(record.gt_mask):
        return 10**9, None
    ordered = _rank_order(record.services, _score_record(record, roles, scoring_mode))
    for rank, row_idx in enumerate(ordered, start=1):
        if bool(record.gt_mask[row_idx]):
            return rank, record.services[row_idx]
    return 10**9, None


def _evaluate_records(
    records: list[CaseFeatures],
    roles: np.ndarray,
    scoring_mode: str,
) -> dict[str, float | int]:
    return _metrics_from_stats(_rank_stats(records, roles, scoring_mode))


def _rank_stats(
    records: list[CaseFeatures],
    roles: np.ndarray,
    scoring_mode: str,
) -> tuple[int, int, float, int, int, int]:
    ranks = [float(_case_rank(record, roles, scoring_mode)[0]) for record in records]
    return _stats_from_ranks(ranks)


def _stats_from_ranks(ranks: list[float]) -> tuple[int, int, float, int, int, int]:
    if not ranks:
        return (0, 0, 0.0, 0, 0, 0)
    total = len(ranks)
    hit1 = sum(1 for rank in ranks if rank <= 1.0)
    hit3 = sum(1 for rank in ranks if rank <= 3.0)
    hit5 = sum(1 for rank in ranks if rank <= 5.0)
    reciprocal = sum(1.0 / rank for rank in ranks)
    return (total, 0, reciprocal, hit1, hit3, hit5)


def _metrics_from_stats(stats: tuple[int, int, float, int, int, int]) -> dict[str, float | int]:
    total, error, reciprocal, hit1, hit3, hit5 = stats
    if total <= 0:
        return {"total": 0, "error": 0, "AC@1": 0.0, "MRR": 0.0, "AC@3": 0.0, "AC@5": 0.0}
    return {
        "total": total,
        "error": error,
        "AC@1": float(hit1) / float(total),
        "MRR": float(reciprocal) / float(total),
        "AC@3": float(hit3) / float(total),
        "AC@5": float(hit5) / float(total),
    }


def _merge_stats(
    stats: list[tuple[int, int, float, int, int, int]],
) -> tuple[int, int, float, int, int, int]:
    total = sum(item[0] for item in stats)
    error = sum(item[1] for item in stats)
    reciprocal = sum(item[2] for item in stats)
    hit1 = sum(item[3] for item in stats)
    hit3 = sum(item[4] for item in stats)
    hit5 = sum(item[5] for item in stats)
    return (total, error, reciprocal, hit1, hit3, hit5)


def _chunk_records(records: list[CaseFeatures], worker_count: int) -> list[list[CaseFeatures]]:
    worker_count = max(1, min(worker_count, len(records)))
    chunks = [[] for _idx in range(worker_count)]
    for idx, record in enumerate(records):
        chunks[idx % worker_count].append(record)
    return [chunk for chunk in chunks if chunk]


def _init_eval_pool(chunks: list[list[CaseFeatures]], scoring_mode: str) -> None:
    global _EVAL_RECORD_CHUNKS, _EVAL_SCORING_MODE
    _EVAL_RECORD_CHUNKS = chunks
    _EVAL_SCORING_MODE = scoring_mode


def _eval_chunk_worker(payload: tuple[int, list[int]]) -> tuple[int, int, float, int, int, int]:
    chunk_idx, role_values = payload
    roles = np.asarray(role_values, dtype=np.int16)
    return _rank_stats(_EVAL_RECORD_CHUNKS[chunk_idx], roles, _EVAL_SCORING_MODE)


def _evaluate_records_parallel(
    executor: ProcessPoolExecutor,
    chunk_count: int,
    roles: np.ndarray,
) -> dict[str, float | int]:
    role_values = [int(value) for value in roles]
    stats = list(
        executor.map(
            _eval_chunk_worker,
            ((chunk_idx, role_values) for chunk_idx in range(chunk_count)),
        )
    )
    return _metrics_from_stats(_merge_stats(stats))


def _single_feature_proxy_metrics(records: list[CaseFeatures], column_idx: int) -> dict[str, float | int]:
    ranks: list[float] = []
    for record in records:
        if record.matrix.shape[1] <= column_idx or not np.any(record.gt_mask):
            ranks.append(float(10**9))
            continue
        scores = record.matrix[:, column_idx].astype(np.float64, copy=False)
        ordered = _rank_order(record.services, scores)
        rank = next(
            (position for position, row_idx in enumerate(ordered, start=1) if bool(record.gt_mask[row_idx])),
            10**9,
        )
        ranks.append(float(rank))
    if not ranks:
        return {"total": 0, "error": 0, "AC@1": 0.0, "MRR": 0.0, "AC@3": 0.0, "AC@5": 0.0}
    return {
        "total": len(ranks),
        "error": 0,
        "AC@1": sum(1 for rank in ranks if rank <= 1.0) / len(ranks),
        "MRR": sum(1.0 / rank for rank in ranks) / len(ranks),
        "AC@3": sum(1 for rank in ranks if rank <= 3.0) / len(ranks),
        "AC@5": sum(1 for rank in ranks if rank <= 5.0) / len(ranks),
    }


def _objective_key(metrics: dict[str, float | int], enabled_count: int) -> tuple[float, float, float, float, float]:
    return (
        float(metrics["AC@1"]),
        float(metrics["MRR"]),
        float(metrics["AC@3"]),
        float(metrics["AC@5"]),
        -float(enabled_count),
    )


def _enabled_count(roles: np.ndarray) -> int:
    return int(np.sum(roles >= 0))


def _try_best_role(
    evaluate: Callable[[np.ndarray], dict[str, float | int]],
    roles: np.ndarray,
    idx: int,
    current_key: tuple[float, float, float, float, float],
    scoring_mode: str,
) -> tuple[np.ndarray, dict[str, float | int], tuple[float, float, float, float, float], bool]:
    best_roles = roles
    best_metrics = evaluate(roles)
    best_key = current_key
    improved = False
    for role in _role_choices(scoring_mode):
        if int(roles[idx]) == int(role):
            continue
        candidate = roles.copy()
        candidate[idx] = int(role)
        metrics = evaluate(candidate)
        key = _objective_key(metrics, _enabled_count(candidate))
        if key > best_key:
            best_roles = candidate
            best_metrics = metrics
            best_key = key
            improved = True
    return best_roles, best_metrics, best_key, improved


def _synthesize_roles(
    records: list[CaseFeatures],
    specs: list[CandidateSpec],
    *,
    scoring_mode: str,
    search_workers: int,
    max_candidates: int,
    coordinate_passes: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    search_executor: ProcessPoolExecutor | None = None
    search_chunk_count = 0
    if search_workers > 1 and records:
        chunks = _chunk_records(records, search_workers)
        search_chunk_count = len(chunks)
        search_executor = ProcessPoolExecutor(
            max_workers=search_chunk_count,
            mp_context=mp.get_context("fork"),
            initializer=_init_eval_pool,
            initargs=(chunks, scoring_mode),
        )

    def evaluate(candidate_roles: np.ndarray) -> dict[str, float | int]:
        if search_executor is None:
            return _evaluate_records(records, candidate_roles, scoring_mode)
        return _evaluate_records_parallel(search_executor, search_chunk_count, candidate_roles)

    seed_roles = np.asarray(
        [
            _initial_role_for_scoring(spec, scoring_mode)
            for spec in specs
        ],
        dtype=np.int16,
    )
    seed_metrics = evaluate(seed_roles)
    seed_key = _objective_key(seed_metrics, _enabled_count(seed_roles))
    print(
        "synthesis seed "
        + json.dumps(
            {
                "enabled": _enabled_count(seed_roles),
                "AC@1": seed_metrics["AC@1"],
                "MRR": seed_metrics["MRR"],
            },
            sort_keys=True,
        ),
        flush=True,
    )

    proxy_scores: list[dict[str, Any]] = []
    for idx, spec in enumerate(specs):
        metrics = _single_feature_proxy_metrics(records, idx)
        key = _objective_key(metrics, 1)
        proxy_scores.append(
            {
                "idx": idx,
                "name": spec.name,
                "seed_role": _role_name(_initial_role_for_scoring(spec, scoring_mode)),
                "metrics": metrics,
                "key": key,
            }
        )

    proxy_scores.sort(key=lambda item: item["key"], reverse=True)
    screened_indices = [int(item["idx"]) for item in proxy_scores[: max(0, max_candidates)]]
    seeded_indices = [idx for idx, role in enumerate(seed_roles) if int(role) >= 0]
    candidate_indices = list(dict.fromkeys([*seeded_indices, *screened_indices]))
    print(
        f"synthesis screened {len(screened_indices)} operators; "
        f"coordinate candidates={len(candidate_indices)}",
        flush=True,
    )

    roles = seed_roles.copy()
    metrics = seed_metrics
    key = seed_key
    history: list[dict[str, Any]] = [
        {
            "stage": "seed",
            "metrics": metrics,
            "enabled_count": _enabled_count(roles),
        }
    ]

    for screen_pos, idx in enumerate(screened_indices, start=1):
        if int(roles[idx]) >= 0:
            continue
        best_roles, best_metrics, best_key, improved = _try_best_role(
            evaluate,
            roles,
            idx,
            key,
            scoring_mode,
        )
        if improved:
            roles, metrics, key = best_roles, best_metrics, best_key
            history.append(
                {
                    "stage": "greedy_add",
                    "operator": specs[idx].name,
                    "role": _role_name(int(roles[idx])),
                    "metrics": metrics,
                    "enabled_count": _enabled_count(roles),
                }
            )
        if screen_pos % 10 == 0 or screen_pos == len(screened_indices):
            print(
                f"synthesis greedy {screen_pos}/{len(screened_indices)} "
                f"AC@1={metrics['AC@1']:.6f} selected={_enabled_count(roles)}",
                flush=True,
            )

    for pass_idx in range(max(0, coordinate_passes)):
        pass_improved = False
        for coord_pos, idx in enumerate(candidate_indices, start=1):
            best_roles, best_metrics, best_key, improved = _try_best_role(
                evaluate,
                roles,
                idx,
                key,
                scoring_mode,
            )
            if improved:
                roles, metrics, key = best_roles, best_metrics, best_key
                pass_improved = True
                history.append(
                    {
                        "stage": f"coordinate_pass_{pass_idx + 1}",
                        "operator": specs[idx].name,
                        "role": _role_name(int(roles[idx])),
                        "metrics": metrics,
                        "enabled_count": _enabled_count(roles),
                    }
                )
            if coord_pos % 20 == 0 or coord_pos == len(candidate_indices):
                print(
                    f"synthesis coordinate pass={pass_idx + 1} "
                    f"{coord_pos}/{len(candidate_indices)} "
                    f"AC@1={metrics['AC@1']:.6f} selected={_enabled_count(roles)}",
                    flush=True,
                )
        if not pass_improved:
            break

    selected_before_prune = [idx for idx, role in enumerate(roles) if int(role) >= 0]
    for prune_pos, idx in enumerate(selected_before_prune, start=1):
        candidate = roles.copy()
        candidate[idx] = ROLE_DISABLED
        prune_metrics = evaluate(candidate)
        prune_key = _objective_key(prune_metrics, _enabled_count(candidate))
        if prune_key >= key:
            roles, metrics, key = candidate, prune_metrics, prune_key
            history.append(
                {
                    "stage": "prune",
                    "operator": specs[idx].name,
                    "metrics": metrics,
                    "enabled_count": _enabled_count(roles),
                }
            )
        if prune_pos % 20 == 0 or prune_pos == len(selected_before_prune):
            print(
                f"synthesis prune {prune_pos}/{len(selected_before_prune)} "
                f"AC@1={metrics['AC@1']:.6f} selected={_enabled_count(roles)}",
                flush=True,
            )

    summary = {
        "seed_metrics": seed_metrics,
        "selected_metrics": metrics,
        "selected_key": list(key),
        "screened_operator_count": len(screened_indices),
        "scoring_mode": scoring_mode,
        "search_workers": search_chunk_count or 1,
        "history": history,
        "screening_method": "single_feature_rank_proxy",
        "top_proxy_operators": proxy_scores[:25],
    }
    if search_executor is not None:
        search_executor.shutdown()
    return roles, summary


def _role_prior(role_idx: int) -> dict[str, float]:
    if int(role_idx) < 0:
        return {role: 0.0 for role in ROLE_ORDER}
    return {role: 1.0 if ROLE_TO_INDEX[role] == int(role_idx) else 0.0 for role in ROLE_ORDER}


def _operator_record(spec: CandidateSpec, role_idx: int) -> dict[str, Any]:
    role_name = _role_name(int(role_idx))
    return {
        "name": spec.name,
        "source": spec.source,
        "operator_family": spec.family,
        "signal": {
            "field": spec.signal_field,
            "type": spec.signal_type,
        },
        "contrast": {
            "operator": spec.contrast_operator,
            "normal_window": "pre_anomaly",
            "abnormal_window": "post_anomaly",
        },
        "aggregation": {
            "level": "service",
            "method": spec.aggregation_method,
        },
        "selected": bool(int(role_idx) >= 0),
        "synthesized_role": role_name,
        "role_prior": _role_prior(int(role_idx)),
        "mechanism": spec.mechanism,
        "rationale": spec.rationale,
        "metadata": spec.metadata,
    }


def _role_families(specs: list[CandidateSpec], roles: np.ndarray) -> dict[str, list[str]]:
    families = {role: [] for role in (*ROLE_ORDER, "neutral")}
    for spec, role_idx in zip(specs, roles, strict=True):
        role_name = _role_name(int(role_idx))
        if role_name != "disabled":
            families[role_name].append(spec.name)
    return families


def _write_case_output(
    record: CaseFeatures,
    roles: np.ndarray,
    scoring_mode: str,
    dataset: str,
    algorithm: str,
    target: Path,
) -> dict[str, Any]:
    scores = _score_record(record, roles, scoring_mode)
    order = _rank_order(record.services, scores)
    ordered_services = [record.services[idx] for idx in order]
    hits = [bool(record.gt_mask[idx]) for idx in order]
    ranks = np.arange(1, len(ordered_services) + 1, dtype=np.uint32)
    best_rank = next(
        (int(rank) for rank, hit in zip(ranks, hits, strict=False) if hit),
        10**9,
    )

    output = pd.DataFrame(
        {
            "level": ["service"] * len(ordered_services),
            "name": ordered_services,
            "rank": ranks,
            "algorithm": [algorithm] * len(ordered_services),
            "dataset": [dataset] * len(ordered_services),
            "datapack": [record.datapack] * len(ordered_services),
            "hit": hits,
            "runtime.seconds": [0.0] * len(ordered_services),
            "exception.type": [None] * len(ordered_services),
            "exception.message": [None] * len(ordered_services),
        }
    )

    hit_seen_at = {k: 1.0 if best_rank <= k else 0.0 for k in range(1, 6)}
    precision_at = {k: float(sum(hits[:k])) / float(k) for k in range(1, 6)}
    mrr = 1.0 / float(best_rank) if best_rank < 10**9 else 0.0
    perf = pd.DataFrame(
        {
            "algorithm": [algorithm],
            "dataset": [dataset],
            "datapack": [record.datapack],
            "total": np.asarray([1], dtype=np.uint32),
            "error": np.asarray([0], dtype=np.uint32),
            "runtime.seconds:avg": [0.0],
            "rank": np.asarray([best_rank], dtype=np.uint32),
            "MRR": [mrr],
            "AC@1.count": [hit_seen_at[1]],
            "AC@2.count": [hit_seen_at[2]],
            "AC@3.count": [hit_seen_at[3]],
            "AC@4.count": [hit_seen_at[4]],
            "AC@5.count": [hit_seen_at[5]],
            "AC@1": [hit_seen_at[1]],
            "AC@2": [hit_seen_at[2]],
            "AC@3": [hit_seen_at[3]],
            "AC@4": [hit_seen_at[4]],
            "AC@5": [hit_seen_at[5]],
            "Avg@1": [hit_seen_at[1]],
            "Avg@2": [hit_seen_at[2]],
            "Avg@3": [hit_seen_at[3]],
            "Avg@4": [hit_seen_at[4]],
            "Avg@5": [hit_seen_at[5]],
            "P@1": [precision_at[1]],
            "P@2": [precision_at[2]],
            "P@3": [precision_at[3]],
            "P@4": [precision_at[4]],
            "P@5": [precision_at[5]],
            "AP@1": [hit_seen_at[1]],
            "AP@2": [hit_seen_at[2]],
            "AP@3": [hit_seen_at[3]],
            "AP@4": [hit_seen_at[4]],
            "AP@5": [hit_seen_at[5]],
        }
    )
    target.mkdir(parents=True, exist_ok=True)
    output.to_parquet(target / "output.parquet", index=False)
    perf.to_parquet(target / "perf.parquet", index=False)
    return {
        "datapack": record.datapack,
        "best_rank": best_rank,
        "top1": ordered_services[0] if ordered_services else None,
        "hit1": bool(best_rank == 1),
        "service_count": len(ordered_services),
        "gt_count": int(np.sum(record.gt_mask)),
    }


def _aggregate(case_summaries: list[dict[str, Any]]) -> dict[str, float | int]:
    ranks = [float(item["best_rank"]) for item in case_summaries]
    if not ranks:
        return {"total": 0, "error": 0, "AC@1": 0.0, "MRR": 0.0, "AC@3": 0.0, "AC@5": 0.0}
    return {
        "total": len(ranks),
        "error": 0,
        "AC@1": sum(1 for rank in ranks if rank <= 1.0) / len(ranks),
        "MRR": sum(1.0 / rank for rank in ranks) / len(ranks),
        "AC@3": sum(1 for rank in ranks if rank <= 3.0) / len(ranks),
        "AC@5": sum(1 for rank in ranks if rank <= 5.0) / len(ranks),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate raw-telemetry Oracle role/operator synthesis for CREST-MEO."
    )
    parser.add_argument("--dataset", default="rcabench")
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--labels", type=Path, default=DEFAULT_LABELS)
    parser.add_argument("--meol-path", type=Path, default=DEFAULT_MEOL_PATH)
    parser.add_argument(
        "--scoring-mode",
        choices=SCORING_MODES,
        default="crest_equivalent",
        help=(
            "crest_equivalent uses the deployable CREST-MEO scoring semantics; "
            "role_vector preserves the historical soft role-vector Oracle ablation."
        ),
    )
    parser.add_argument("--artifact", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path, default=None)
    parser.add_argument("--algorithm", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-scan-cases", type=int, default=120)
    parser.add_argument("--max-metric-names", type=int, default=60)
    parser.add_argument("--min-case-coverage", type=int, default=3)
    parser.add_argument("--max-candidates", type=int, default=80)
    parser.add_argument("--coordinate-passes", type=int, default=3)
    parser.add_argument(
        "--search-workers",
        type=int,
        default=None,
        help=(
            "Workers for offline objective evaluation. Defaults to --workers "
            "for crest_equivalent scoring and 1 for the historical role_vector ablation."
        ),
    )
    parser.add_argument(
        "--exclude-raw-metric",
        action="store_true",
        help=(
            "Exclude all raw_metric::* candidates. This is a conservative "
            "generic-operator ablation for reviewers who treat metric-name "
            "operators as schema- or benchmark-specific."
        ),
    )
    parser.add_argument(
        "--exclude-raw-metric-values",
        action="store_true",
        help=(
            "Exclude only raw_metric::<metric-name>::* candidates while keeping "
            "generic raw_metric::row_count::* operators."
        ),
    )
    parser.add_argument("--no-reference", action="store_true")
    parser.add_argument("--indent", type=int, default=2)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    data_root = _repo_path(args.data_root)
    labels_path = _repo_path(args.labels)
    meol_path = _repo_path(args.meol_path)
    output_root = _repo_path(args.output_root)
    scoring_mode = str(args.scoring_mode)
    artifact_path = _repo_path(
        args.artifact
        or (
            DEFAULT_CREST_EQUIVALENT_ARTIFACT
            if scoring_mode == "crest_equivalent"
            else DEFAULT_ARTIFACT
        )
    )
    summary_path = _repo_path(
        args.summary
        or (
            DEFAULT_CREST_EQUIVALENT_SUMMARY
            if scoring_mode == "crest_equivalent"
            else DEFAULT_SUMMARY
        )
    )
    algorithm = args.algorithm or (
        "crest_meo_oracle_crest_equivalent"
        if scoring_mode == "crest_equivalent"
        else "crest_meo_oracle_role_synthesis"
    )

    gt_by_datapack = _load_labels(labels_path, args.dataset)
    datapacks = sorted(gt_by_datapack)
    if args.limit is not None:
        datapacks = datapacks[: max(0, args.limit)]

    specs, meo_specs = _build_candidate_specs(
        data_root,
        args.dataset,
        datapacks,
        meol_path,
        max_scan_cases=int(args.max_scan_cases),
        max_metric_names=int(args.max_metric_names),
        min_case_coverage=int(args.min_case_coverage),
    )
    excluded_prefixes: list[str] = []
    excluded_families: list[str] = []
    if args.exclude_raw_metric_values:
        excluded_families.append("raw_metric_value")
        specs = [spec for spec in specs if spec.family != "raw_metric_value"]
    if args.exclude_raw_metric:
        excluded_prefixes.append("raw_metric::")
        specs = [spec for spec in specs if not spec.name.startswith("raw_metric::")]

    worker_args = [
        (
            data_root,
            args.dataset,
            datapack,
            gt_by_datapack[datapack],
            specs,
            meo_specs,
            scoring_mode,
        )
        for datapack in datapacks
    ]

    records: list[CaseFeatures] = []
    errors: list[dict[str, Any]] = []
    workers = max(1, int(args.workers))
    search_workers = (
        max(1, int(args.search_workers))
        if args.search_workers is not None
        else (workers if scoring_mode == "crest_equivalent" else 1)
    )
    if workers == 1:
        for idx, item in enumerate(worker_args, start=1):
            result = _worker(item)
            if isinstance(result, CaseFeatures):
                records.append(result)
            else:
                errors.append(result)
            if idx % 100 == 0:
                print(f"processed {idx}/{len(worker_args)}", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_worker, item): item[2] for item in worker_args}
            for idx, future in enumerate(as_completed(futures), start=1):
                result = future.result()
                if isinstance(result, CaseFeatures):
                    records.append(result)
                else:
                    errors.append(result)
                if idx % 100 == 0:
                    print(f"processed {idx}/{len(worker_args)}", flush=True)

    records.sort(key=lambda item: item.datapack)
    errors.sort(key=lambda item: str(item["datapack"]))
    if not records:
        raise SystemExit(f"No valid cases extracted. sample_errors={errors[:5]}")

    roles, synthesis_summary = _synthesize_roles(
        records,
        specs,
        scoring_mode=scoring_mode,
        search_workers=search_workers,
        max_candidates=int(args.max_candidates),
        coordinate_passes=int(args.coordinate_passes),
    )
    operators = [_operator_record(spec, int(role)) for spec, role in zip(specs, roles, strict=True)]
    role_families = _role_families(specs, roles)
    mutation_features = role_families["mutation"]
    propagation_features = role_families["propagation"]

    case_summaries: list[dict[str, Any]] = []
    if args.no_reference:
        for record in records:
            rank, _top_gt = _case_rank(record, roles, scoring_mode)
            scores = _score_record(record, roles, scoring_mode)
            top1_idx = _rank_order(record.services, scores)[0]
            case_summaries.append(
                {
                    "datapack": record.datapack,
                    "best_rank": rank,
                    "top1": record.services[top1_idx],
                    "hit1": bool(rank == 1),
                    "service_count": len(record.services),
                    "gt_count": int(np.sum(record.gt_mask)),
                }
            )
    else:
        for idx, record in enumerate(records, start=1):
            target = output_root / args.dataset / record.datapack / algorithm
            case_summaries.append(
                _write_case_output(
                    record,
                    roles,
                    scoring_mode,
                    args.dataset,
                    algorithm,
                    target,
                )
            )
            if idx % 100 == 0:
                print(f"wrote {idx}/{len(records)}", flush=True)

    metrics = _aggregate(case_summaries)
    artifact = {
        "artifact_name": "crest-meo-oracle-raw-telemetry-role-synthesis-rcabench-v1",
        "artifact_type": "oracle_raw_telemetry_operator_synthesis",
        "scoring_mode": scoring_mode,
        "dataset": args.dataset,
        "created_at": datetime.now(UTC).isoformat(),
        "policy": {
            "uses_gt_labels": True,
            "uses_gt_for_feature_values": False,
            "uses_per_incident_gt_signal": False,
            "uses_service_identity_weight": False,
            "uses_gt_feature_bank": False,
            "uses_fault_labels": False,
            "uses_prior_run_results": False,
            "uses_conclusion_parquet": False,
            "not_for_online_ranking": True,
            "intentionally_leaky": True,
            "purpose": (
                "Offline upper-bound synthesis of global raw-telemetry evidence "
                "operators, role assignments, and counterfactual role sets."
            ),
        },
        "inputs": {
            "labels": _relative(labels_path),
            "data_root": _relative(data_root),
            "meol_path": _relative(meol_path),
        },
        "oracle_scope": "global_raw_telemetry_operator_and_role_synthesis",
        "objective": "maximize AC@1, then MRR, AC@3, AC@5, and fewer enabled operators",
        "scoring_semantics": (
            "CREST-equivalent MEOL membership path: selected operators contribute "
            "to local/denoised CREST energy; mutation and propagation memberships "
            "only choose dynamic counterfactual explain-away sets."
            if scoring_mode == "crest_equivalent"
            else "Historical soft role-vector Oracle ablation."
        ),
        "candidate_space": {
            "crest_feature_count": len(FEATURES),
            "meol_operator_count": len(meo_specs),
            "total_operator_count": len(specs),
            "raw_operator_count": sum(1 for spec in specs if spec.family.startswith("raw_")),
            "max_scan_incidents": int(args.max_scan_cases),
            "max_metric_names": int(args.max_metric_names),
            "min_case_coverage": int(args.min_case_coverage),
            "excluded_operator_prefixes": excluded_prefixes,
            "excluded_operator_families": excluded_families,
        },
        "role_families": role_families,
        "counterfactual_mutation_features": mutation_features,
        "counterfactual_propagation_features": propagation_features,
        "operators": operators,
        "operator_count": len(operators),
        "selected_operator_count": int(np.sum(roles >= 0)),
        "metrics": metrics,
        "synthesis": {
            "incident_count": len(records),
            "error_count": len(errors),
            "service_rows": int(sum(len(record.services) for record in records)),
            "max_candidates": int(args.max_candidates),
            "coordinate_passes": int(args.coordinate_passes),
            "search_workers": int(search_workers),
            **synthesis_summary,
        },
        "errors": errors,
    }

    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=args.indent) + "\n",
        encoding="utf-8",
    )

    summary = {
        "algorithm": algorithm,
        "dataset": args.dataset,
        "scoring_mode": scoring_mode,
        "artifact": _relative(artifact_path),
        "output_root": _relative(output_root),
        "metrics": metrics,
        "operator_count": len(operators),
        "selected_operator_count": int(np.sum(roles >= 0)),
        "case_summaries": case_summaries,
        "errors": errors,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"saved {artifact_path.relative_to(REPO) if artifact_path.is_relative_to(REPO) else artifact_path}"
    )
    print(
        f"saved {summary_path.relative_to(REPO) if summary_path.is_relative_to(REPO) else summary_path}"
    )
    print(json.dumps(metrics, sort_keys=True))
    if errors:
        print(f"sample_errors={json.dumps(errors[:5], ensure_ascii=False)[:2000]}")


if __name__ == "__main__":
    main()
