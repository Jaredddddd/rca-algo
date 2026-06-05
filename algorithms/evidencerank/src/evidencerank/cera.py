"""Causal Evidence Role Alignment RCA algorithm."""

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

LOG_ERROR_KEYWORDS = ("error", "exception", "fail", "timeout", "critical", "fatal")

MODALITY_FEATURES = {
    "metric": frozenset({
        "metric_max_z",
        "metric_mean_z",
        "metric_anomaly_count",
        "metric_value_delta",
        "metric_count_drop_shift",
        "abnormal_metric_rows",
    }),
    "trace": frozenset({
        "trace_duration_z",
        "trace_duration_delta",
        "trace_count_delta",
        "trace_count_rise_shift",
        "trace_count_drop_shift",
        "trace_endpoint_shift",
        "trace_error_rate",
        "trace_status_code_shift",
        "trace_self_duration_relative_shift",
        "abnormal_trace_rows",
        "topology_in_degree",
        "topology_out_degree",
    }),
    "log": frozenset({
        "log_count_delta",
        "log_error_rate",
        "log_template_delta",
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
                services.update(
                    service
                    for service in df["parent_service"].map(_clean_service).dropna().unique()
                )
    return sorted(services)


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
        features[service]["metric_count_drop_shift"] = _count_drop_shift(
            normal_count,
            abnormal_count,
        )
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
        normal_std = (
            float(baseline["std"])
            if baseline is not None and not pd.isna(baseline["std"])
            else 0.0
        )
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
    if "parent_service" not in data.columns and {
        "span_id",
        "parent_span_id",
        "service_name",
    }.issubset(data.columns):
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
        column
        for column in key_columns
        if column in normal.columns or column in abnormal.columns
    ]
    if not key_columns or normal.empty or abnormal.empty:
        return {}

    counts_by_phase = {}
    totals_by_phase = {}
    for phase, frame in (("normal", normal), ("abnormal", abnormal)):
        columns = ["service_name"] + [
            column for column in key_columns if column in frame.columns
        ]
        data = frame[columns].copy()
        data = data.dropna(subset=["service_name"])
        if data.empty:
            return {}
        for column in key_columns:
            if column not in data.columns:
                data[column] = "<missing>"
            data[column] = data[column].astype("string").fillna("<missing>")
        counts_by_phase[phase] = data.groupby(
            ["service_name"] + key_columns,
            dropna=False,
        ).size()
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
    required_columns = {
        "trace_id",
        "span_id",
        "parent_span_id",
        "service_name",
        "duration",
        "time",
    }
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
        for trace_id, span_id, start, end in data[
            ["trace_id", "span_id", "_start", "_end"]
        ].itertuples(index=False, name=None)
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
    for trace_id, span_id, duration in data[
        ["trace_id", "span_id", "_duration"]
    ].itertuples(index=False, name=None):
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
            normal_std = (
                float(baseline["std"])
                if baseline is not None and not pd.isna(baseline["std"])
                else 0.0
            )
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
        col
        for col in (
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
    normalized = " ".join(
        "<num>" if token.replace(".", "", 1).isdigit() else token
        for token in str(message).split()
    )
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

    message_col = next(
        (col for col in ("message", "body", "content", "log") if col in abnormal.columns),
        None,
    )
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
            float(abnormal_templates.get(service, 0.0))
            - float(normal_templates.get(service, 0.0))
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
    clean = np.nan_to_num(
        values.astype(np.float64, copy=False),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    clean = np.maximum(clean, 0.0)
    view = np.zeros(clean.shape[0], dtype=np.float64)
    positive_idx = np.flatnonzero(clean > 0.0)
    if positive_idx.size == 0:
        return view

    ordered_idx = positive_idx[np.argsort(clean[positive_idx], kind="mergesort")]
    view[ordered_idx] = np.arange(1, positive_idx.size + 1, dtype=np.float64) / float(
        positive_idx.size
    )
    return view


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


class CERAMetric(CERA):
    """CERA ablation using only metric evidence."""

    _modalities = frozenset({"metric"})


class CERALog(CERA):
    """CERA ablation using only log evidence."""

    _modalities = frozenset({"log"})


class CERATrace(CERA):
    """CERA ablation using only trace evidence."""

    _modalities = frozenset({"trace"})


class CERAMetricLog(CERA):
    """CERA ablation using metric and log evidence."""

    _modalities = frozenset({"metric", "log"})


class CERAMetricTrace(CERA):
    """CERA ablation using metric and trace evidence."""

    _modalities = frozenset({"metric", "trace"})


class CERALogTrace(CERA):
    """CERA ablation using log and trace evidence."""

    _modalities = frozenset({"log", "trace"})
