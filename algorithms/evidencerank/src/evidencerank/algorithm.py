"""Multi-modal evidence ranking RCA algorithm adapted for rcabench-platform v2."""

from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from enum import IntEnum
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

BASE_FEATURE_NAMES = (
    "metric_max_z",
    "metric_mean_z",
    "metric_anomaly_count",
    "metric_value_delta",
    "metric_count_drop_shift",
    "trace_duration_z",
    "trace_duration_delta",
    "trace_count_delta",
    "trace_count_rise_shift",
    "trace_count_drop_shift",
    "trace_endpoint_shift",
    "trace_error_rate",
    "trace_status_code_shift",
    "trace_self_duration_relative_shift",
    "log_count_delta",
    "log_error_rate",
    "log_template_delta",
    "topology_in_degree",
    "topology_out_degree",
    "abnormal_metric_rows",
    "abnormal_trace_rows",
)

LOG_ERROR_KEYWORDS = ["error", "exception", "fail", "timeout", "critical", "fatal"]

MODALITY_FEATURES = {
    "metric": frozenset({
        "metric_max_z", "metric_mean_z", "metric_anomaly_count",
        "metric_value_delta", "metric_count_drop_shift", "abnormal_metric_rows",
    }),
    "trace": frozenset({
        "trace_duration_z", "trace_duration_delta", "trace_count_delta",
        "trace_count_rise_shift", "trace_count_drop_shift", "trace_endpoint_shift",
        "trace_error_rate", "trace_status_code_shift", "trace_self_duration_relative_shift", "abnormal_trace_rows",
        "topology_in_degree", "topology_out_degree",
    }),
    "log": frozenset({
        "log_count_delta", "log_error_rate", "log_template_delta",
    }),
}

ALL_MODALITIES = frozenset(MODALITY_FEATURES.keys())

INPUT_FRAME_NAMES = (
    "normal_metrics",
    "abnormal_metrics",
    "normal_traces",
    "abnormal_traces",
    "normal_logs",
    "abnormal_logs",
)

class FeaturePriority(IntEnum):
    DISABLED = 0
    BACKGROUND = 1
    BASELINE = 2
    SUPPORT = 3
    LOCAL = 4
    HIGH = 5
    ROOT = 6
    CRITICAL = 7


FEATURE_PRIORITIES = {
    "metric_max_z": FeaturePriority.BACKGROUND,
    "metric_mean_z": FeaturePriority.BACKGROUND,
    "metric_anomaly_count": FeaturePriority.BACKGROUND,
    "metric_value_delta": FeaturePriority.BACKGROUND,
    "metric_count_drop_shift": FeaturePriority.HIGH,
    "trace_duration_z": FeaturePriority.DISABLED,
    "trace_duration_delta": FeaturePriority.BASELINE,
    "trace_count_delta": FeaturePriority.BASELINE,
    "trace_count_rise_shift": FeaturePriority.HIGH,
    "trace_count_drop_shift": FeaturePriority.BASELINE,
    "trace_endpoint_shift": FeaturePriority.HIGH,
    "trace_error_rate": FeaturePriority.BASELINE,
    "trace_status_code_shift": FeaturePriority.CRITICAL,
    "trace_self_duration_relative_shift": FeaturePriority.LOCAL,
    "log_count_delta": FeaturePriority.LOCAL,
    "log_error_rate": FeaturePriority.LOCAL,
    "log_template_delta": FeaturePriority.BACKGROUND,
    "topology_in_degree": FeaturePriority.SUPPORT,
    "topology_out_degree": FeaturePriority.DISABLED,
    "abnormal_metric_rows": FeaturePriority.SUPPORT,
    "abnormal_trace_rows": FeaturePriority.SUPPORT,
}


def _synthesize_feature_priority_ladder() -> dict[FeaturePriority, float]:
    """Derive a nonlinear diagnostic severity curve from ordinal priority tiers."""
    low_tiers = (
        FeaturePriority.BACKGROUND,
        FeaturePriority.BASELINE,
        FeaturePriority.SUPPORT,
        FeaturePriority.LOCAL,
    )
    low_step = 1.0 / float(len(low_tiers))
    ladder = {FeaturePriority.DISABLED: 0.0}
    for priority in low_tiers:
        offset = int(priority) - int(FeaturePriority.BASELINE)
        ladder[priority] = 1.0 + low_step * float(offset)

    local_ceiling = ladder[FeaturePriority.LOCAL]
    strong_floor = local_ceiling * float(len(low_tiers))
    ladder[FeaturePriority.HIGH] = strong_floor
    ladder[FeaturePriority.ROOT] = strong_floor + float(len(low_tiers))
    ladder[FeaturePriority.CRITICAL] = float(
        1 << math.ceil(math.log2(ladder[FeaturePriority.ROOT]))
    )
    return ladder


FEATURE_PRIORITY_LADDER = _synthesize_feature_priority_ladder()


def _feature_weights_from_priorities(
    priorities: dict[str, FeaturePriority],
) -> dict[str, float]:
    return {
        name: FEATURE_PRIORITY_LADDER[priority]
        for name, priority in priorities.items()
    }


FEATURE_WEIGHTS = _feature_weights_from_priorities(FEATURE_PRIORITIES)

PARENT_CONTEXT_WEIGHT = 0.05
TRACE_ENDPOINT_SUPPORT_STATUS_FACTOR = 2.0
TRACE_ENDPOINT_SUPPORT_RISE_FACTOR = 1.5
TRACE_ENDPOINT_UNSUPPORTED_PENALTY = 0.5
TRACE_ENDPOINT_POST_GATE_FACTOR = 1.75
ARC_CASE_SCALE_CLIP = 3.0
ARC_DIRECTIONAL_MUTATION_FEATURES = frozenset({
    "metric_count_drop_shift",
    "trace_count_drop_shift",
    "trace_endpoint_shift",
    "trace_error_rate",
    "trace_status_code_shift",
})
ARC_DIRECTIONAL_PROPAGATION_FEATURES = frozenset({
    "trace_duration_z",
    "trace_duration_delta",
    "trace_self_duration_relative_shift",
    "trace_count_delta",
    "trace_count_rise_shift",
    "abnormal_trace_rows",
    "log_count_delta",
    "log_template_delta",
})


def _safe_read_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


def _load_input_frames(input_folder: Path) -> dict[str, pd.DataFrame]:
    return {
        name: _safe_read_parquet(input_folder / f"{name}.parquet")
        for name in INPUT_FRAME_NAMES
    }


def _clean_service(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null"}:
        return None
    return text


def _series_service(df: pd.DataFrame) -> pd.Series:
    candidates = (
        "service_name",
        "service",
        "instance",
        "attr.k8s.container.name",
        "attr.k8s.deployment.name",
        "attr.k8s.statefulset.name",
        "attr.k8s.pod.name",
    )
    for column in candidates:
        if column in df.columns:
            return df[column].map(_clean_service)
    return pd.Series([None] * len(df), index=df.index)


def _count_drop_shift(normal_count: float, abnormal_count: float) -> float:
    if normal_count < 5.0:
        return 0.0
    drop = max(0.0, normal_count - abnormal_count)
    if drop <= 0.0:
        return 0.0
    return drop / max(normal_count, 1.0) * math.log1p(normal_count)


def _collect_services_from_frames(frames: dict[str, pd.DataFrame]) -> list[str]:
    services: set[str] = set()
    for df in frames.values():
        if not df.empty:
            services.update(service for service in _series_service(df).dropna().unique())
            if "parent_service" in df.columns:
                services.update(service for service in df["parent_service"].map(_clean_service).dropna().unique())
    return sorted(services)


def _collect_services(input_folder: Path) -> list[str]:
    return _collect_services_from_frames(_load_input_frames(input_folder))


def _metric_features(
    normal_df: pd.DataFrame,
    abnormal_df: pd.DataFrame,
    services: list[str],
) -> dict[str, dict[str, float]]:
    features = {service: defaultdict(float) for service in services}
    if normal_df.empty and abnormal_df.empty:
        return features

    normal = normal_df.copy()
    abnormal = abnormal_df.copy()
    normal["service_name"] = _series_service(normal)
    abnormal["service_name"] = _series_service(abnormal)
    normal = normal.dropna(subset=["service_name"])
    abnormal = abnormal.dropna(subset=["service_name"])
    normal_counts = normal.groupby("service_name").size()
    abnormal_counts = abnormal.groupby("service_name").size()
    for service in services:
        normal_count = float(normal_counts.get(service, 0.0))
        abnormal_count = float(abnormal_counts.get(service, 0.0))
        features[service]["metric_count_drop_shift"] = _count_drop_shift(normal_count, abnormal_count)
        features[service]["abnormal_metric_rows"] = abnormal_count

    if abnormal.empty or "value" not in abnormal.columns:
        return features
    if "value" not in normal.columns:
        normal["value"] = np.nan
    if "metric" not in normal.columns:
        normal["metric"] = "value"
    if "metric" not in abnormal.columns:
        abnormal["metric"] = "value"

    normal_stats = normal.groupby(["service_name", "metric"])["value"].agg(["mean", "std"])
    abnormal_stats = abnormal.groupby(["service_name", "metric"])["value"].agg(["mean", "count"])
    for (service, metric), row in abnormal_stats.iterrows():
        if service not in features:
            continue
        baseline = normal_stats.loc[(service, metric)] if (service, metric) in normal_stats.index else None
        normal_mean = float(baseline["mean"]) if baseline is not None else 0.0
        normal_std = float(baseline["std"]) if baseline is not None and not pd.isna(baseline["std"]) else 0.0
        abnormal_mean = float(row["mean"])
        z_score = abs(abnormal_mean - normal_mean) / (normal_std + 1e-6)
        features[service]["metric_max_z"] = max(features[service]["metric_max_z"], z_score)
        features[service]["metric_mean_z_sum"] += z_score
        features[service]["metric_anomaly_count"] += 1.0 if z_score > 3.0 else 0.0
        features[service]["metric_count"] += 1.0
        features[service]["metric_value_delta"] += abs(abnormal_mean - normal_mean)
    for service in services:
        count = features[service].pop("metric_count", 0.0)
        total = features[service].pop("metric_mean_z_sum", 0.0)
        features[service]["metric_mean_z"] = total / count if count else 0.0
        features[service]["abnormal_metric_rows"] = float(abnormal_counts.get(service, 0.0))
    return features


def _trace_edges(df: pd.DataFrame) -> list[tuple[str, str]]:
    if df.empty:
        return []
    data = df.copy()
    if "parent_service" not in data.columns and {"span_id", "parent_span_id", "service_name"}.issubset(data.columns):
        span_to_service = dict(zip(data["span_id"], data["service_name"]))
        data["parent_service"] = data["parent_span_id"].map(span_to_service)
    if "parent_service" not in data.columns:
        return []
    data["service_name"] = _series_service(data)
    data["parent_service"] = data["parent_service"].map(_clean_service)
    edges = []
    for parent, child in data[["parent_service", "service_name"]].dropna().drop_duplicates().itertuples(index=False):
        if parent and child:
            edges.append((str(parent), str(child)))
    return edges


def _distribution_shift_by_service(
    normal: pd.DataFrame,
    abnormal: pd.DataFrame,
    key_columns: list[str],
) -> dict[str, float]:
    key_columns = [
        column for column in key_columns
        if column in normal.columns or column in abnormal.columns
    ]
    if not key_columns or normal.empty or abnormal.empty:
        return {}

    counts_by_phase = {}
    totals_by_phase = {}
    for phase, frame in (("normal", normal), ("abnormal", abnormal)):
        columns = ["service_name"] + [column for column in key_columns if column in frame.columns]
        data = frame[columns].copy()
        data = data.dropna(subset=["service_name"])
        if data.empty:
            return {}
        for column in key_columns:
            if column not in data.columns:
                data[column] = "<missing>"
            data[column] = data[column].astype("string").fillna("<missing>")
        counts_by_phase[phase] = data.groupby(["service_name"] + key_columns, dropna=False).size()
        totals_by_phase[phase] = data.groupby("service_name", dropna=False).size()

    counts = pd.concat(
        [
            counts_by_phase["normal"].rename("normal"),
            counts_by_phase["abnormal"].rename("abnormal"),
        ],
        axis=1,
    ).fillna(0.0)
    services = counts.index.get_level_values("service_name")
    normal_totals = services.map(totals_by_phase["normal"]).astype(float)
    abnormal_totals = services.map(totals_by_phase["abnormal"]).astype(float)
    enough_samples = (normal_totals >= 5.0) & (abnormal_totals >= 5.0)
    if not enough_samples.any():
        return {}

    counts = counts.loc[enough_samples]
    services = counts.index.get_level_values("service_name")
    normal_totals = services.map(totals_by_phase["normal"]).astype(float)
    abnormal_totals = services.map(totals_by_phase["abnormal"]).astype(float)
    normal_share = counts["normal"].to_numpy(dtype=np.float64) / normal_totals
    abnormal_share = counts["abnormal"].to_numpy(dtype=np.float64) / abnormal_totals
    diffs = pd.DataFrame({
        "service_name": services,
        "absdiff": np.abs(abnormal_share - normal_share),
    })
    shifts = diffs.groupby("service_name")["absdiff"].sum() / 2.0
    return {
        str(service): float(shift) * math.log1p(min(
            float(totals_by_phase["normal"].get(service, 0.0)),
            float(totals_by_phase["abnormal"].get(service, 0.0)),
        ))
        for service, shift in shifts.items()
    }


def _trace_self_duration_stats(df: pd.DataFrame) -> dict[str, tuple[float, float]]:
    required_columns = {"trace_id", "span_id", "parent_span_id", "service_name", "duration", "time"}
    if df.empty or not required_columns.issubset(df.columns):
        return {}

    data = df[list(required_columns)].copy()
    data["service_name"] = _series_service(data)
    data = data.dropna(subset=["trace_id", "span_id", "service_name", "duration", "time"])
    if data.empty:
        return {}

    times = pd.to_datetime(data["time"], utc=True, errors="coerce")
    data = data.loc[times.notna()].copy()
    if data.empty:
        return {}

    durations = pd.to_numeric(data["duration"], errors="coerce")
    data = data.loc[durations.notna()].copy()
    if data.empty:
        return {}

    times = times.loc[data.index]
    durations = durations.loc[data.index].astype("float64").clip(lower=0.0)
    data["_start"] = times.astype("int64").astype("float64")
    data["_duration"] = durations
    data["_end"] = data["_start"] + data["_duration"]

    parent_bounds = {
        (trace_id, span_id): (float(start), float(end))
        for trace_id, span_id, start, end in data[["trace_id", "span_id", "_start", "_end"]].itertuples(
            index=False,
            name=None,
        )
    }
    child_intervals: dict[tuple[Any, Any], list[tuple[float, float]]] = defaultdict(list)
    for trace_id, parent_span_id, child_start, child_end in data[
        ["trace_id", "parent_span_id", "_start", "_end"]
    ].itertuples(index=False, name=None):
        parent_id = _clean_service(parent_span_id)
        if parent_id is None:
            continue
        parent_key = (trace_id, parent_id)
        parent_window = parent_bounds.get(parent_key)
        if parent_window is None:
            continue
        start = max(float(child_start), parent_window[0])
        end = min(float(child_end), parent_window[1])
        if end > start:
            child_intervals[parent_key].append((start, end))

    covered_by_parent: dict[tuple[Any, Any], float] = {}
    for parent_key, intervals in child_intervals.items():
        intervals.sort()
        total = 0.0
        current_start: float | None = None
        current_end: float | None = None
        for start, end in intervals:
            if current_start is None or current_end is None:
                current_start, current_end = start, end
            elif start <= current_end:
                current_end = max(current_end, end)
            else:
                total += current_end - current_start
                current_start, current_end = start, end
        if current_start is not None and current_end is not None:
            total += current_end - current_start
        covered_by_parent[parent_key] = total

    self_durations = []
    for trace_id, span_id, duration in data[["trace_id", "span_id", "_duration"]].itertuples(
        index=False,
        name=None,
    ):
        child_covered = min(float(duration), covered_by_parent.get((trace_id, span_id), 0.0))
        self_durations.append(max(0.0, float(duration) - child_covered))

    data["_self_duration"] = self_durations
    stats = data.groupby("service_name")["_self_duration"].agg(["mean", "count"])
    return {
        str(service): (float(row["mean"]), float(row["count"]))
        for service, row in stats.iterrows()
    }


def _trace_features(
    normal_df: pd.DataFrame,
    abnormal_df: pd.DataFrame,
    services: list[str],
) -> tuple[dict[str, dict[str, float]], list[tuple[str, str]]]:
    features = {service: defaultdict(float) for service in services}
    edges = _trace_edges(abnormal_df)
    if normal_df.empty and abnormal_df.empty:
        return features, edges

    normal = normal_df.copy()
    abnormal = abnormal_df.copy()
    normal["service_name"] = _series_service(normal)
    abnormal["service_name"] = _series_service(abnormal)
    normal = normal.dropna(subset=["service_name"])
    abnormal = abnormal.dropna(subset=["service_name"])
    duration_col = "duration" if "duration" in normal.columns and "duration" in abnormal.columns else None
    if duration_col:
        normal_duration = normal.groupby("service_name")[duration_col].agg(["mean", "std", "count"])
        abnormal_duration = abnormal.groupby("service_name")[duration_col].agg(["mean", "count"])
        for service, row in abnormal_duration.iterrows():
            if service not in features:
                continue
            baseline = normal_duration.loc[service] if service in normal_duration.index else None
            normal_mean = float(baseline["mean"]) if baseline is not None else 0.0
            normal_std = float(baseline["std"]) if baseline is not None and not pd.isna(baseline["std"]) else 0.0
            abnormal_mean = float(row["mean"])
            features[service]["trace_duration_z"] = abs(abnormal_mean - normal_mean) / (normal_std + 1e-6)
            features[service]["trace_duration_delta"] = abs(abnormal_mean - normal_mean)
            features[service]["abnormal_trace_rows"] = float(row["count"])
    normal_counts = normal.groupby("service_name").size()
    abnormal_counts = abnormal.groupby("service_name").size()
    normal_self_duration = _trace_self_duration_stats(normal)
    abnormal_self_duration = _trace_self_duration_stats(abnormal)
    status_cols = [col for col in ("status_code", "http.status_code", "status") if col in abnormal.columns]
    status_error_rates = pd.Series(dtype="float64")
    if status_cols:
        status_text = abnormal[status_cols[0]].astype(str).str.lower()
        is_error = status_text.str.contains("error|fail|5\\d\\d|true", regex=True)
        status_error_rates = is_error.groupby(abnormal["service_name"]).mean()
    trace_status_cols = [
        col for col in (
            "attr.http.response.status_code",
            "http.status_code",
            "status_code",
            "attr.status_code",
            "status",
        )
        if col in normal.columns or col in abnormal.columns
    ]
    endpoint_shift = _distribution_shift_by_service(normal, abnormal, ["span_name"])
    status_shift = {}
    if trace_status_cols:
        status_key_columns = ["span_name", *trace_status_cols]
        full_status_shift = _distribution_shift_by_service(normal, abnormal, status_key_columns)
        status_shift = {
            service: max(0.0, value - endpoint_shift.get(service, 0.0))
            for service, value in full_status_shift.items()
        }
    for service in services:
        normal_count = float(normal_counts.get(service, 0.0))
        abnormal_count = float(abnormal_counts.get(service, 0.0))
        features[service]["trace_count_delta"] = abs(abnormal_count - normal_count)
        features[service]["trace_count_rise_shift"] = (
            max(0.0, abnormal_count - normal_count)
            / max(abnormal_count, 1.0)
            * math.log1p(abnormal_count)
        )
        features[service]["trace_count_drop_shift"] = _count_drop_shift(normal_count, abnormal_count)
        features[service]["abnormal_trace_rows"] = max(features[service]["abnormal_trace_rows"], abnormal_count)
        features[service]["trace_endpoint_shift"] = endpoint_shift.get(service, 0.0)
        features[service]["trace_status_code_shift"] = status_shift.get(service, 0.0)
        normal_self_mean, normal_self_count = normal_self_duration.get(service, (0.0, 0.0))
        abnormal_self_mean, abnormal_self_count = abnormal_self_duration.get(service, (0.0, 0.0))
        sample_count = min(normal_self_count, abnormal_self_count)
        if sample_count >= 5.0:
            features[service]["trace_self_duration_relative_shift"] = (
                max(0.0, abnormal_self_mean - normal_self_mean)
                / (abs(normal_self_mean) + 1.0)
                * math.log1p(sample_count)
            )
        if status_cols:
            features[service]["trace_error_rate"] = float(status_error_rates.get(service, 0.0) or 0.0)
    return features, edges


def _stable_template_id(message: str) -> str:
    normalized = " ".join("<num>" if token.replace(".", "", 1).isdigit() else token for token in str(message).split())
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:8]


def _log_features(
    normal_df: pd.DataFrame,
    abnormal_df: pd.DataFrame,
    services: list[str],
) -> dict[str, dict[str, float]]:
    features = {service: defaultdict(float) for service in services}
    if abnormal_df.empty:
        return features
    normal = normal_df.copy()
    abnormal = abnormal_df.copy()
    normal["service_name"] = _series_service(normal)
    abnormal["service_name"] = _series_service(abnormal)
    normal = normal.dropna(subset=["service_name"])
    abnormal = abnormal.dropna(subset=["service_name"])

    message_col = next((col for col in ("message", "body", "content", "log") if col in abnormal.columns), None)
    if message_col:
        pattern = "|".join(LOG_ERROR_KEYWORDS)
        abnormal["_is_error"] = abnormal[message_col].astype(str).str.lower().str.contains(pattern, regex=True)
        abnormal["_template"] = abnormal[message_col].map(_stable_template_id)
        normal["_template"] = normal[message_col].map(_stable_template_id) if message_col in normal.columns else ""
    else:
        abnormal["_is_error"] = False
        abnormal["_template"] = ""
        normal["_template"] = ""

    normal_counts = normal.groupby("service_name").size()
    abnormal_counts = abnormal.groupby("service_name").size()
    normal_templates = normal.groupby("service_name")["_template"].nunique()
    abnormal_templates = abnormal.groupby("service_name")["_template"].nunique()
    log_error_rates = abnormal.groupby("service_name")["_is_error"].mean()
    for service in services:
        normal_count = float(normal_counts.get(service, 0.0))
        abnormal_count = float(abnormal_counts.get(service, 0.0))
        features[service]["log_count_delta"] = abs(abnormal_count - normal_count)
        features[service]["log_error_rate"] = float(log_error_rates.get(service, 0.0) or 0.0)
        features[service]["log_template_delta"] = abs(
            float(abnormal_templates.get(service, 0.0)) - float(normal_templates.get(service, 0.0))
        )
    return features


def _merge_feature_maps(*maps: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    merged: dict[str, dict[str, float]] = {}
    for feature_map in maps:
        for service, values in feature_map.items():
            target = merged.setdefault(service, defaultdict(float))
            for key, value in values.items():
                target[key] += float(value)
    return merged


def _finite_nonnegative(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(numeric) or numeric <= 0.0:
        return 0.0
    return numeric


def _build_feature_matrix(
    frames: dict[str, pd.DataFrame],
    services: list[str],
    enabled_features: tuple[str, ...],
    enabled_modalities: frozenset[str] = ALL_MODALITIES,
    normalize: bool = True,
) -> tuple[np.ndarray, list[tuple[str, str]]]:
    feature_maps: list[dict[str, dict[str, float]]] = []
    trace_edges: list[tuple[str, str]] = []
    empty = pd.DataFrame()

    if "metric" in enabled_modalities:
        feature_maps.append(
            _metric_features(
                frames.get("normal_metrics", empty),
                frames.get("abnormal_metrics", empty),
                services,
            )
        )
    if "trace" in enabled_modalities:
        trace_map, trace_edges = _trace_features(
            frames.get("normal_traces", empty),
            frames.get("abnormal_traces", empty),
            services,
        )
        feature_maps.append(trace_map)
    if "log" in enabled_modalities:
        feature_maps.append(
            _log_features(
                frames.get("normal_logs", empty),
                frames.get("abnormal_logs", empty),
                services,
            )
        )

    features_by_service = _merge_feature_maps(*feature_maps)

    for source, target_service in trace_edges:
        if source in features_by_service:
            features_by_service[source]["topology_out_degree"] += 1.0
        if target_service in features_by_service:
            features_by_service[target_service]["topology_in_degree"] += 1.0

    feature_dim = len(enabled_features)
    service_to_id = {service: idx for idx, service in enumerate(services)}
    matrix = np.zeros((len(services), feature_dim), dtype=np.float32)
    for service, row_idx in service_to_id.items():
        values = [
            _finite_nonnegative(features_by_service.get(service, {}).get(name, 0.0))
            for name in enabled_features
        ]
        if normalize:
            values = [math.log1p(value) for value in values]
        matrix[row_idx] = np.asarray(values, dtype=np.float32)

    return matrix, trace_edges


def _feature_modality(feature_name: str) -> str | None:
    for modality, feature_names in MODALITY_FEATURES.items():
        if feature_name in feature_names:
            return modality
    return None


def _robust_case_feature_matrix(matrix: np.ndarray) -> np.ndarray:
    clean_matrix = np.nan_to_num(matrix, nan=0.0, posinf=0.0, neginf=0.0)
    clean_matrix = np.maximum(clean_matrix, 0.0)
    scaled = np.zeros_like(clean_matrix, dtype=np.float32)
    for idx in range(clean_matrix.shape[1]):
        column = clean_matrix[:, idx]
        positive = column[column > 0.0]
        if positive.size == 0:
            continue
        scale = float(np.percentile(positive, 95)) if positive.size > 1 else float(positive[0])
        if not math.isfinite(scale) or scale <= 0.0:
            scale = float(np.max(positive))
        if not math.isfinite(scale) or scale <= 0.0:
            continue
        scaled[:, idx] = np.clip(column / scale, 0.0, ARC_CASE_SCALE_CLIP)
    return scaled


def _cosine_similarity(left: np.ndarray, right: np.ndarray) -> float | None:
    left_norm = float(np.linalg.norm(left))
    right_norm = float(np.linalg.norm(right))
    if left_norm <= 1e-12 or right_norm <= 1e-12:
        return None
    similarity = float(np.dot(left, right) / (left_norm * right_norm))
    if not math.isfinite(similarity):
        return None
    return min(1.0, max(0.0, similarity))


def _arc_positive_rank_view(values: np.ndarray) -> np.ndarray:
    clean = np.nan_to_num(values.astype(np.float64, copy=False), nan=0.0, posinf=0.0, neginf=0.0)
    clean = np.maximum(clean, 0.0)
    view = np.zeros(clean.shape[0], dtype=np.float64)
    positive_idx = np.flatnonzero(clean > 0.0)
    if positive_idx.size == 0:
        return view

    ordered_idx = positive_idx[np.argsort(clean[positive_idx], kind="mergesort")]
    view[ordered_idx] = np.arange(1, positive_idx.size + 1, dtype=np.float64) / float(positive_idx.size)
    return view


def _feature_agreement(
    matrix: np.ndarray,
    feature_idx: int,
    enabled_features: tuple[str, ...],
    modality_indices: dict[str, list[int]],
) -> float:
    feature_vector = matrix[:, feature_idx]
    if not np.any(feature_vector > 0.0):
        return 0.0

    modality = _feature_modality(enabled_features[feature_idx])
    agreement_scores: list[float] = []

    peer_indices = [
        idx
        for idx in modality_indices.get(modality or "", [])
        if idx != feature_idx and np.any(matrix[:, idx] > 0.0)
    ]
    if peer_indices:
        peer_vector = matrix[:, peer_indices].mean(axis=1)
        similarity = _cosine_similarity(feature_vector, peer_vector)
        if similarity is not None:
            agreement_scores.append(similarity)

    cross_indices = [
        idx
        for other_modality, indices in modality_indices.items()
        if other_modality != modality
        for idx in indices
        if np.any(matrix[:, idx] > 0.0)
    ]
    if cross_indices:
        cross_vector = matrix[:, cross_indices].mean(axis=1)
        similarity = _cosine_similarity(feature_vector, cross_vector)
        if similarity is not None:
            agreement_scores.append(similarity)

    if not agreement_scores:
        return 0.5
    return float(np.mean(agreement_scores))


def _feature_reliability_components(column: np.ndarray, agreement: float) -> np.ndarray:
    positive = column[np.isfinite(column) & (column > 0.0)]
    if positive.size == 0:
        return np.zeros(5, dtype=np.float64)

    support = min(1.0, math.sqrt(float(positive.size) / 3.0))

    if positive.size == 1:
        concentration = 1.0
        top_gap = 1.0
    else:
        total = float(positive.sum())
        if not math.isfinite(total) or total <= 0.0:
            return 0.0
        probabilities = positive / total
        entropy = -float(np.sum(probabilities * np.log(probabilities + 1e-12)))
        concentration = 1.0 - entropy / math.log(float(positive.size))
        concentration = min(1.0, max(0.0, concentration))

        ordered = np.sort(positive)[::-1]
        top_gap = float((ordered[0] - ordered[1]) / (ordered[0] + ordered[1] + 1e-6))
        top_gap = min(1.0, max(0.0, top_gap))

    p95 = float(np.percentile(positive, 95))
    median = float(np.median(positive))
    contrast = (p95 - median) / (p95 + median + 1e-6)
    contrast = min(1.0, max(0.0, contrast))

    agreement = min(1.0, max(0.0, agreement))
    return np.asarray(
        [support, concentration, contrast, top_gap, agreement],
        dtype=np.float64,
    )


def _arc_reliability_component_weights(components: np.ndarray) -> np.ndarray:
    """Learn reliability meta-weights from the current case diagnostics."""
    if components.size == 0 or components.shape[1] == 0:
        return np.asarray([], dtype=np.float64)

    clean = np.nan_to_num(components, nan=0.0, posinf=0.0, neginf=0.0)
    if not np.any(clean > 0.0):
        return np.zeros(clean.shape[1], dtype=np.float64)

    centered = clean - np.mean(clean, axis=0, keepdims=True)
    scale = np.std(centered, axis=0)
    standardized = centered / (scale + 1e-12)
    covariance = standardized.T @ standardized / max(1, standardized.shape[0] - 1)
    try:
        eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    except np.linalg.LinAlgError:
        return np.ones(clean.shape[1], dtype=np.float64) / float(clean.shape[1])

    component = eigenvectors[:, int(np.argmax(eigenvalues))]
    feature_mean = np.mean(clean, axis=1)
    if float(np.dot(clean @ component, feature_mean)) < 0.0:
        component = -component

    weights = np.maximum(component, 0.0)
    if float(np.sum(weights)) <= 1e-12:
        weights = np.abs(component)
    if float(np.sum(weights)) <= 1e-12:
        return np.ones(clean.shape[1], dtype=np.float64) / float(clean.shape[1])
    return weights / float(np.sum(weights))


def _arc_unsupervised_feature_weights(
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
) -> np.ndarray:
    modality_indices: dict[str, list[int]] = {}
    for idx, feature_name in enumerate(enabled_features):
        modality = _feature_modality(feature_name) or "other"
        modality_indices.setdefault(modality, []).append(idx)

    components = np.zeros((len(enabled_features), 5), dtype=np.float64)
    for idx in range(len(enabled_features)):
        agreement = _feature_agreement(matrix, idx, enabled_features, modality_indices)
        components[idx] = _feature_reliability_components(matrix[:, idx], agreement)

    component_weights = _arc_reliability_component_weights(components)
    if component_weights.size == 0:
        return np.zeros(len(enabled_features), dtype=np.float32)

    weights = components @ component_weights
    weights = np.nan_to_num(weights, nan=0.0, posinf=0.0, neginf=0.0)
    weights = np.maximum(weights, 0.0).astype(np.float32)
    positive = weights[weights > 0.0]
    if positive.size == 0:
        return weights
    weights = weights / float(np.mean(positive))
    return weights.astype(np.float32)


def _arc_active_feature_weights(feature_reliability: np.ndarray) -> np.ndarray:
    """Use single-case reliability as an active evidence mask, not a sharp prior."""
    clean = np.nan_to_num(feature_reliability, nan=0.0, posinf=0.0, neginf=0.0)
    return (clean > 0.0).astype(np.float32)


def _arc_family_indices(enabled_features: tuple[str, ...]) -> dict[str, list[int]]:
    return {
        "metric": [
            idx
            for idx, name in enumerate(enabled_features)
            if name in MODALITY_FEATURES["metric"] and not name.startswith("topology_")
        ],
        "mutation": [
            idx
            for idx, name in enumerate(enabled_features)
            if name in ARC_DIRECTIONAL_MUTATION_FEATURES
        ],
        "propagation": [
            idx
            for idx, name in enumerate(enabled_features)
            if name in ARC_DIRECTIONAL_PROPAGATION_FEATURES
        ],
        "log": [
            idx
            for idx, name in enumerate(enabled_features)
            if name in MODALITY_FEATURES["log"]
        ],
    }


def _arc_family_reliability_weights(
    feature_reliability: np.ndarray,
    enabled_features: tuple[str, ...],
) -> tuple[np.ndarray, float]:
    """Collapse noisy feature reliability into bounded family-level calibration."""
    clean = np.nan_to_num(feature_reliability, nan=0.0, posinf=0.0, neginf=0.0)
    family_indices = _arc_family_indices(enabled_features)
    family_reliability: dict[str, float] = {}
    for family, indices in family_indices.items():
        positive = clean[indices][clean[indices] > 0.0]
        if positive.size == 0:
            continue
        reliability = float(np.median(positive))
        if math.isfinite(reliability) and reliability > 0.0:
            family_reliability[family] = reliability

    positive_reliability = [
        reliability for reliability in family_reliability.values()
        if reliability > 0.0
    ]
    if not positive_reliability:
        return np.ones(len(enabled_features), dtype=np.float32), 1.0

    center = float(np.mean(positive_reliability))
    if not math.isfinite(center) or center <= 0.0:
        return np.ones(len(enabled_features), dtype=np.float32), 1.0

    weights = np.ones(len(enabled_features), dtype=np.float32)
    for family, reliability in family_reliability.items():
        family_weight = reliability / center
        if not math.isfinite(family_weight) or family_weight <= 0.0:
            continue
        weights[family_indices[family]] = float(family_weight)

    reliability_values = np.asarray(positive_reliability, dtype=np.float64)
    reliability_mass = float(np.sum(reliability_values))
    reliability_energy = float(np.sum(reliability_values * reliability_values))
    if reliability_mass <= 0.0 or reliability_energy <= 0.0:
        return weights, 1.0
    effective_family_count = reliability_mass * reliability_mass / reliability_energy
    if not math.isfinite(effective_family_count) or effective_family_count <= 0.0:
        effective_family_count = 1.0
    return weights, effective_family_count


def _arc_normalized_family_sum(
    weighted_matrix: np.ndarray,
    indices: list[int],
) -> np.ndarray:
    if not indices:
        return np.zeros(weighted_matrix.shape[0], dtype=np.float64)
    values = weighted_matrix[:, indices].sum(axis=1).astype(np.float64)
    positive = values[np.isfinite(values) & (values > 0.0)]
    if positive.size == 0:
        return np.zeros(weighted_matrix.shape[0], dtype=np.float64)
    scale = float(np.percentile(positive, 95)) if positive.size > 1 else float(positive[0])
    if not math.isfinite(scale) or scale <= 0.0:
        return np.zeros(weighted_matrix.shape[0], dtype=np.float64)
    return np.clip(values / scale, 0.0, ARC_CASE_SCALE_CLIP)


def _arc_family_local_contrast(
    weighted_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
) -> np.ndarray:
    family_indices = _arc_family_indices(enabled_features)
    metric = _arc_normalized_family_sum(weighted_matrix, family_indices["metric"])
    mutation = _arc_normalized_family_sum(weighted_matrix, family_indices["mutation"])
    propagation = _arc_normalized_family_sum(weighted_matrix, family_indices["propagation"])
    log = _arc_normalized_family_sum(weighted_matrix, family_indices["log"])
    return metric + mutation + log - propagation


def _apply_arc_family_consensus(
    services: list[str],
    active_scores: dict[str, float],
    family_scores: dict[str, float],
    family_weighted_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    effective_family_count: float,
) -> dict[str, float]:
    if not active_scores:
        return active_scores

    active_vector = np.asarray(
        [active_scores.get(service, 0.0) for service in services],
        dtype=np.float64,
    )
    family_vector = np.asarray(
        [family_scores.get(service, 0.0) for service in services],
        dtype=np.float64,
    )
    family_delta = _arc_family_local_contrast(family_weighted_matrix, enabled_features)
    family_count = max(1.0, float(effective_family_count))
    reliability_blend = 1.0 / family_count
    contrast_blend = 1.0 / math.sqrt(family_count)
    adjusted = (
        (1.0 - reliability_blend) * active_vector
        + reliability_blend * family_vector
        + contrast_blend * family_delta
    )
    adjusted = np.maximum(adjusted, 0.0)
    return {service: float(adjusted[idx]) for idx, service in enumerate(services)}


def _apply_arc_top_neighbor_pairwise_contrast(
    services: list[str],
    scores: dict[str, float],
    weighted_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
) -> dict[str, float]:
    """Use trace-neighbor root/victim pairs as a final ARC correction."""
    if not trace_edges or not scores:
        return scores

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    base_scores = np.asarray(
        [scores.get(service, 0.0) for service in services],
        dtype=np.float64,
    )
    adjusted = base_scores.copy()

    mutation_indices = [
        idx
        for idx, name in enumerate(enabled_features)
        if name in ARC_DIRECTIONAL_MUTATION_FEATURES
    ]
    propagation_indices = [
        idx
        for idx, name in enumerate(enabled_features)
        if name in ARC_DIRECTIONAL_PROPAGATION_FEATURES
    ]
    if not mutation_indices or not propagation_indices:
        return scores

    mutation = _arc_normalized_family_sum(weighted_matrix, mutation_indices)
    propagation = _arc_normalized_family_sum(weighted_matrix, propagation_indices)

    candidate_pairs: list[tuple[int, int, float, float, float, float]] = []

    def add_pair(root_idx: int, victim_idx: int) -> None:
        if root_idx == victim_idx or base_scores[victim_idx] <= base_scores[root_idx]:
            return

        mutation_excess = max(0.0, float(mutation[root_idx] - mutation[victim_idx]))
        propagation_excess = max(
            0.0,
            float(propagation[victim_idx] - propagation[root_idx]),
        )
        if mutation_excess <= 0.0 or propagation_excess <= 0.0:
            return

        mutation_share = mutation_excess / (
            float(mutation[root_idx] + mutation[victim_idx]) + 1e-6
        )
        propagation_share = propagation_excess / (
            float(propagation[victim_idx] + propagation[root_idx]) + 1e-6
        )
        score_excess = float(base_scores[victim_idx] - base_scores[root_idx])
        score_share = score_excess / (
            float(base_scores[victim_idx] + base_scores[root_idx]) + 1e-6
        )
        strength = mutation_share * propagation_share * score_share
        if not math.isfinite(strength) or strength <= 0.0:
            return

        candidate_pairs.append(
            (
                root_idx,
                victim_idx,
                mutation_share,
                propagation_share,
                strength,
                score_excess,
            )
        )

    for parent, child in trace_edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)
        if parent_idx is None or child_idx is None or parent_idx == child_idx:
            continue

        add_pair(child_idx, parent_idx)
        add_pair(parent_idx, child_idx)

    if not candidate_pairs:
        return scores

    best_by_victim: dict[int, tuple[int, int, float, float, float, float]] = {}
    for pair in candidate_pairs:
        victim_idx = pair[1]
        current = best_by_victim.get(victim_idx)
        if current is None or pair[4] > current[4]:
            best_by_victim[victim_idx] = pair

    pair_counts = np.zeros(len(services), dtype=np.float64)
    for _root_idx, victim_idx, *_rest in best_by_victim.values():
        pair_counts[victim_idx] += 1.0

    for (
        root_idx,
        victim_idx,
        mutation_share,
        propagation_share,
        _strength,
        score_excess,
    ) in best_by_victim.values():
        transfer = (
            score_excess
            * mutation_share
            * propagation_share
            / max(1.0, pair_counts[victim_idx])
        )
        adjusted[victim_idx] -= transfer
        adjusted[root_idx] += transfer

    adjusted = np.maximum(adjusted, 0.0)
    return {service: float(adjusted[idx]) for idx, service in enumerate(services)}


def _heuristic_scores(
    services: list[str],
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    feature_weights: np.ndarray | None = None,
    trace_edges: list[tuple[str, str]] | None = None,
    parent_context_weight: float = 0.0,
    endpoint_gate: str = "legacy",
) -> dict[str, float]:
    clean_matrix = np.nan_to_num(matrix, nan=0.0, posinf=0.0, neginf=0.0)
    if feature_weights is not None:
        clean_matrix = clean_matrix * feature_weights
    if endpoint_gate == "legacy":
        clean_matrix = _apply_trace_endpoint_support_gate(enabled_features, clean_matrix)
    elif endpoint_gate == "arc":
        clean_matrix = _apply_arc_trace_endpoint_support_gate(enabled_features, clean_matrix)
    totals = clean_matrix.sum(axis=1)
    if trace_edges and parent_context_weight > 0.0:
        totals = _apply_parent_context(services, totals, trace_edges, parent_context_weight)
    cleaned = [0.0 if not math.isfinite(float(total)) else max(float(total), 0.0) for total in totals]
    if max(cleaned, default=0.0) <= 0:
        return {service: 0.0 for service in services}
    return {service: cleaned[idx] for idx, service in enumerate(services)}


def _apply_trace_endpoint_support_gate(
    enabled_features: tuple[str, ...],
    weighted_matrix: np.ndarray,
) -> np.ndarray:
    required = (
        "trace_endpoint_shift",
        "trace_status_code_shift",
        "trace_count_rise_shift",
    )
    if not all(name in enabled_features for name in required):
        return weighted_matrix

    endpoint_idx = enabled_features.index("trace_endpoint_shift")
    status_idx = enabled_features.index("trace_status_code_shift")
    rise_idx = enabled_features.index("trace_count_rise_shift")

    endpoint = weighted_matrix[:, endpoint_idx]
    supported_by_status = TRACE_ENDPOINT_SUPPORT_STATUS_FACTOR * weighted_matrix[:, status_idx]
    supported_by_rise = TRACE_ENDPOINT_SUPPORT_RISE_FACTOR * weighted_matrix[:, rise_idx]
    unsupported_endpoint = np.maximum(0.0, endpoint - supported_by_status - supported_by_rise)

    adjusted = weighted_matrix.copy()
    adjusted[:, endpoint_idx] = np.maximum(
        0.0,
        endpoint - TRACE_ENDPOINT_UNSUPPORTED_PENALTY * unsupported_endpoint,
    ) * TRACE_ENDPOINT_POST_GATE_FACTOR
    return adjusted


def _apply_arc_trace_endpoint_support_gate(
    enabled_features: tuple[str, ...],
    weighted_matrix: np.ndarray,
) -> np.ndarray:
    required = (
        "trace_endpoint_shift",
        "trace_status_code_shift",
        "trace_count_rise_shift",
    )
    if not all(name in enabled_features for name in required):
        return weighted_matrix

    endpoint_idx = enabled_features.index("trace_endpoint_shift")
    status_idx = enabled_features.index("trace_status_code_shift")
    rise_idx = enabled_features.index("trace_count_rise_shift")

    endpoint = weighted_matrix[:, endpoint_idx].astype(np.float64, copy=False)
    if not np.any(endpoint > 0.0):
        return weighted_matrix

    support_candidates = [
        weighted_matrix[:, status_idx].astype(np.float64, copy=False),
        weighted_matrix[:, rise_idx].astype(np.float64, copy=False),
    ]
    endpoint_view = _arc_positive_rank_view(endpoint)
    candidate_views = [_arc_positive_rank_view(candidate) for candidate in support_candidates]
    candidate_weights = np.asarray(
        [
            _cosine_similarity(endpoint_view, candidate_view) or 0.0
            for candidate_view in candidate_views
        ],
        dtype=np.float64,
    )
    if not np.any(candidate_weights > 0.0):
        active_candidates = np.asarray(
            [np.any(candidate > 0.0) for candidate in support_candidates],
            dtype=np.float64,
        )
        if not np.any(active_candidates > 0.0):
            return weighted_matrix
        candidate_weights = active_candidates
    candidate_weights = candidate_weights / float(np.sum(candidate_weights))

    support = np.zeros_like(endpoint, dtype=np.float64)
    for weight, candidate in zip(candidate_weights, support_candidates):
        support += float(weight) * candidate

    support_view = _arc_positive_rank_view(support)
    endpoint_factor = endpoint_view + support_view

    adjusted = weighted_matrix.copy()
    adjusted[:, endpoint_idx] = np.maximum(0.0, endpoint * endpoint_factor)
    return adjusted


def _apply_parent_context(
    services: list[str],
    scores: np.ndarray,
    trace_edges: list[tuple[str, str]],
    weight: float,
) -> np.ndarray:
    service_to_idx = {service: idx for idx, service in enumerate(services)}
    parent_totals = np.zeros(len(services), dtype=np.float64)
    parent_counts = np.zeros(len(services), dtype=np.float64)

    for parent, child in trace_edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)
        if parent_idx is None or child_idx is None or parent_idx == child_idx:
            continue
        parent_totals[child_idx] += float(scores[parent_idx])
        parent_counts[child_idx] += 1.0

    adjusted = scores.astype(np.float64, copy=True)
    has_parent = parent_counts > 0.0
    adjusted[has_parent] = (
        (1.0 - weight) * adjusted[has_parent]
        + weight * (parent_totals[has_parent] / parent_counts[has_parent])
    )
    return adjusted


class EvidenceRank(Algorithm):
    _modalities: frozenset[str] = ALL_MODALITIES

    def __init__(self):
        all_enabled = frozenset().union(*(MODALITY_FEATURES[m] for m in self._modalities))
        self._enabled_features = tuple(
            name for name in BASE_FEATURE_NAMES if name in all_enabled
        )
        self._feature_weights = np.asarray(
            [FEATURE_WEIGHTS.get(name, 1.0) for name in self._enabled_features],
            dtype=np.float32,
        )
        self._parent_context_weight = PARENT_CONTEXT_WEIGHT if "trace" in self._modalities else 0.0

    def needs_cpu_count(self) -> int | None:
        return 1

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        input_folder = args.input_folder

        frames = _load_input_frames(input_folder)
        services = _collect_services_from_frames(frames)
        if not services:
            return []

        matrix, trace_edges = _build_feature_matrix(
            frames,
            services,
            self._enabled_features,
            self._modalities,
        )
        scores = _heuristic_scores(
            services,
            matrix,
            self._enabled_features,
            self._feature_weights,
            trace_edges,
            self._parent_context_weight,
        )
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        answers = [
            AlgorithmAnswer(level="service", name=name, rank=rank)
            for rank, (name, _score) in enumerate(sorted_scores, start=1)
        ]
        return answers


class EvidenceRankARC(Algorithm):
    """EvidRank-ARC: ordinal root evidence with local reliability contrast."""

    _modalities: frozenset[str] = ALL_MODALITIES

    def __init__(self):
        all_enabled = frozenset().union(*(MODALITY_FEATURES[m] for m in self._modalities))
        self._enabled_features = tuple(
            name for name in BASE_FEATURE_NAMES if name in all_enabled
        )
        self._feature_weights = np.asarray(
            [FEATURE_WEIGHTS.get(name, 1.0) for name in self._enabled_features],
            dtype=np.float32,
        )
        self._parent_context_weight = PARENT_CONTEXT_WEIGHT if "trace" in self._modalities else 0.0

    def needs_cpu_count(self) -> int | None:
        return 1

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        input_folder = args.input_folder

        frames = _load_input_frames(input_folder)
        services = _collect_services_from_frames(frames)
        if not services:
            return []

        matrix, trace_edges = _build_feature_matrix(
            frames,
            services,
            self._enabled_features,
            self._modalities,
        )
        case_matrix = _robust_case_feature_matrix(matrix)
        feature_reliability = _arc_unsupervised_feature_weights(
            case_matrix,
            self._enabled_features,
        )
        active_feature_weights = _arc_active_feature_weights(feature_reliability)
        scores = _heuristic_scores(
            services,
            matrix,
            self._enabled_features,
            self._feature_weights,
            trace_edges,
            self._parent_context_weight,
            endpoint_gate="legacy",
        )
        contrast_matrix = _apply_arc_trace_endpoint_support_gate(
            self._enabled_features,
            case_matrix * active_feature_weights,
        )
        scores = _apply_arc_top_neighbor_pairwise_contrast(
            services,
            scores,
            contrast_matrix,
            self._enabled_features,
            trace_edges,
        )
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        answers = [
            AlgorithmAnswer(level="service", name=name, rank=rank)
            for rank, (name, _score) in enumerate(sorted_scores, start=1)
        ]
        return answers


class EvidenceRankMetric(EvidenceRank):
    _modalities = frozenset({"metric"})


class EvidenceRankLog(EvidenceRank):
    _modalities = frozenset({"log"})


class EvidenceRankTrace(EvidenceRank):
    _modalities = frozenset({"trace"})


class EvidenceRankMetricLog(EvidenceRank):
    _modalities = frozenset({"metric", "log"})


class EvidenceRankMetricTrace(EvidenceRank):
    _modalities = frozenset({"metric", "trace"})


class EvidenceRankLogTrace(EvidenceRank):
    _modalities = frozenset({"log", "trace"})
