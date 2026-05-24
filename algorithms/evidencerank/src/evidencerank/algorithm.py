"""Multi-modal evidence ranking RCA algorithm adapted for rcabench-platform v2."""

from __future__ import annotations

import hashlib
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

BASE_FEATURE_NAMES = (
    "metric_max_z",
    "metric_mean_z",
    "metric_anomaly_count",
    "metric_value_delta",
    "trace_duration_z",
    "trace_duration_delta",
    "trace_count_delta",
    "trace_error_rate",
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
        "metric_value_delta", "abnormal_metric_rows",
    }),
    "trace": frozenset({
        "trace_duration_z", "trace_duration_delta", "trace_count_delta",
        "trace_error_rate", "abnormal_trace_rows",
        "topology_in_degree", "topology_out_degree",
    }),
    "log": frozenset({
        "log_count_delta", "log_error_rate", "log_template_delta",
    }),
}

ALL_MODALITIES = frozenset(MODALITY_FEATURES.keys())


def _safe_read_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


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


def _collect_services(input_folder: Path) -> list[str]:
    services: set[str] = set()
    for name in (
        "normal_metrics.parquet",
        "abnormal_metrics.parquet",
        "normal_traces.parquet",
        "abnormal_traces.parquet",
        "normal_logs.parquet",
        "abnormal_logs.parquet",
    ):
        df = _safe_read_parquet(input_folder / name)
        if not df.empty:
            services.update(service for service in _series_service(df).dropna().unique())
            if "parent_service" in df.columns:
                services.update(service for service in df["parent_service"].map(_clean_service).dropna().unique())
    return sorted(services)


def _metric_features(
    normal_df: pd.DataFrame,
    abnormal_df: pd.DataFrame,
    services: list[str],
) -> dict[str, dict[str, float]]:
    features = {service: defaultdict(float) for service in services}
    if abnormal_df.empty or "value" not in abnormal_df.columns:
        return features

    normal = normal_df.copy()
    abnormal = abnormal_df.copy()
    normal["service_name"] = _series_service(normal)
    abnormal["service_name"] = _series_service(abnormal)
    normal = normal.dropna(subset=["service_name"])
    abnormal = abnormal.dropna(subset=["service_name"])
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
        features[service]["abnormal_metric_rows"] = float((abnormal["service_name"] == service).sum())
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


def _trace_features(
    normal_df: pd.DataFrame,
    abnormal_df: pd.DataFrame,
    services: list[str],
) -> tuple[dict[str, dict[str, float]], list[tuple[str, str]]]:
    features = {service: defaultdict(float) for service in services}
    edges = _trace_edges(abnormal_df)
    if abnormal_df.empty:
        return features, edges

    normal = normal_df.copy()
    abnormal = abnormal_df.copy()
    normal["service_name"] = _series_service(normal)
    abnormal["service_name"] = _series_service(abnormal)
    normal = normal.dropna(subset=["service_name"])
    abnormal = abnormal.dropna(subset=["service_name"])
    duration_col = "duration" if "duration" in abnormal.columns else None
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
    status_cols = [col for col in ("status_code", "http.status_code", "status") if col in abnormal.columns]
    for service in services:
        normal_count = float(normal_counts.get(service, 0.0))
        abnormal_count = float(abnormal_counts.get(service, 0.0))
        features[service]["trace_count_delta"] = abs(abnormal_count - normal_count)
        features[service]["abnormal_trace_rows"] = max(features[service]["abnormal_trace_rows"], abnormal_count)
        if status_cols:
            status = abnormal.loc[abnormal["service_name"] == service, status_cols[0]].astype(str).str.lower()
            features[service]["trace_error_rate"] = float(status.str.contains("error|fail|5\\d\\d|true").mean() or 0.0)
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
    for service in services:
        normal_count = float(normal_counts.get(service, 0.0))
        abnormal_count = float(abnormal_counts.get(service, 0.0))
        rows = abnormal["service_name"] == service
        features[service]["log_count_delta"] = abs(abnormal_count - normal_count)
        features[service]["log_error_rate"] = float(abnormal.loc[rows, "_is_error"].mean() or 0.0)
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


def _build_feature_matrix(
    input_folder: Path,
    services: list[str],
    enabled_features: tuple[str, ...],
    normalize: bool = True,
) -> tuple[np.ndarray, list[tuple[str, str]]]:
    normal_metrics = _safe_read_parquet(input_folder / "normal_metrics.parquet")
    abnormal_metrics = _safe_read_parquet(input_folder / "abnormal_metrics.parquet")
    normal_traces = _safe_read_parquet(input_folder / "normal_traces.parquet")
    abnormal_traces = _safe_read_parquet(input_folder / "abnormal_traces.parquet")
    normal_logs = _safe_read_parquet(input_folder / "normal_logs.parquet")
    abnormal_logs = _safe_read_parquet(input_folder / "abnormal_logs.parquet")

    metric_map = _metric_features(normal_metrics, abnormal_metrics, services)
    trace_map, trace_edges = _trace_features(normal_traces, abnormal_traces, services)
    log_map = _log_features(normal_logs, abnormal_logs, services)
    features_by_service = _merge_feature_maps(metric_map, trace_map, log_map)

    for source, target_service in trace_edges:
        if source in features_by_service:
            features_by_service[source]["topology_out_degree"] += 1.0
        if target_service in features_by_service:
            features_by_service[target_service]["topology_in_degree"] += 1.0

    feature_dim = len(enabled_features)
    service_to_id = {service: idx for idx, service in enumerate(services)}
    matrix = np.zeros((len(services), feature_dim), dtype=np.float32)
    for service, row_idx in service_to_id.items():
        values = [float(features_by_service.get(service, {}).get(name, 0.0)) for name in enabled_features]
        if normalize:
            values = [math.log1p(max(value, 0.0)) for value in values]
        matrix[row_idx] = np.asarray(values, dtype=np.float32)

    return matrix, trace_edges


def _heuristic_scores(services: list[str], matrix: np.ndarray) -> dict[str, float]:
    totals = matrix.sum(axis=1)
    cleaned = [0.0 if not math.isfinite(float(total)) else max(float(total), 0.0) for total in totals]
    if max(cleaned, default=0.0) <= 0:
        return {service: 0.0 for service in services}
    return {service: cleaned[idx] for idx, service in enumerate(services)}


class EvidenceRank(Algorithm):
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
        input_folder = args.input_folder

        services = _collect_services(input_folder)
        if not services:
            return []

        matrix, _ = _build_feature_matrix(input_folder, services, self._enabled_features)
        scores = _heuristic_scores(services, matrix)
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
