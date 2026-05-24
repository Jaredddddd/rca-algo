from __future__ import annotations

import math
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import logger, timeit


GENERIC_SERVICE_NAMES = {
    "cilium-agent",
    "kube-apiserver",
    "kube-controller-manager",
    "kube-dns",
    "kube-proxy",
    "kube-scheduler",
    "kubernetes",
    "kubernetes-endpoints",
    "loadgenerator",
    "prometheus",
}

SERVICE_COLUMNS = (
    "service_name",
    "attr.k8s.service.name",
    "attr.k8s.deployment.name",
    "attr.k8s.statefulset.name",
    "attr.k8s.container.name",
    "attr.k8s.pod.name",
)

ENDPOINT_COLUMNS = ("attr.destination", "attr.source")
REPLICASET_POD_RE = re.compile(r"^(.+)-[0-9a-f]{6,10}-[a-z0-9]{5}$")
STATEFULSET_POD_RE = re.compile(r"^(.+)-[0-9]+$")


@dataclass(frozen=True)
class HeroSASConfig:
    stable_window_size: int = 5
    min_stable_window_size: int = 3
    recovery_window_size: int = 0
    stable_std_threshold: float = 10.0
    recovery_std_threshold: float = 25.0
    jump_threshold_factor: float = 3.0
    min_jump_floor: float = 1.0
    min_robust_z: float = 1.0
    noise_reduction_w: float = 0.4
    cluster_minutes_k: int = 3
    max_clusters_nc: int = 3
    final_filter_x: float = 0.2


@dataclass(frozen=True)
class MetricEvent:
    service: str
    metric: str
    timestamp: pd.Timestamp
    score: float
    delta: float
    robust_z: float
    peak_value: float
    baseline_value: float
    direction: str


def _safe_read_parquet(path: Path, columns: Iterable[str] | None = None) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    requested = list(columns) if columns is not None else None
    try:
        data = pd.read_parquet(path)
    except Exception as exc:
        logger.warning(f"failed to read {path.name}: {exc}")
        return pd.DataFrame()
    if requested is None:
        return data
    existing = [column for column in requested if column in data.columns]
    return data[existing]


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null", "<na>"}:
        return None
    return text


def _workload_from_endpoint(value: Any) -> str | None:
    text = _clean_text(value)
    if text is None:
        return None
    if "/" in text:
        text = text.rsplit("/", 1)[-1]
    match = REPLICASET_POD_RE.match(text)
    if match:
        return match.group(1)
    match = STATEFULSET_POD_RE.match(text)
    if match:
        return match.group(1)
    return text


def _normalize_service(value: Any) -> str | None:
    service = _workload_from_endpoint(value)
    if service is None or service in GENERIC_SERVICE_NAMES:
        return None
    if service.endswith("-istio-proxy"):
        return None
    return service


def _service_series(df: pd.DataFrame) -> pd.Series:
    service = pd.Series([None] * len(df), index=df.index, dtype="object")
    for column in SERVICE_COLUMNS:
        if column not in df.columns:
            continue
        candidate = df[column].map(_normalize_service)
        service = service.where(service.notna(), candidate)

    generic_or_missing = service.isna()
    for column in ENDPOINT_COLUMNS:
        if column not in df.columns:
            continue
        candidate = df[column].map(_normalize_service)
        service = service.where(~generic_or_missing, candidate)
        generic_or_missing = service.isna()
    return service


def _metric_frame(input_folder: Path, phase: str) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    specs = (
        (f"{phase}_metrics.parquet", "gauge"),
        (f"{phase}_metrics_sum.parquet", "sum"),
    )
    base_columns = set(("time", "metric", "value", *SERVICE_COLUMNS, *ENDPOINT_COLUMNS))
    for filename, source in specs:
        df = _safe_read_parquet(input_folder / filename, base_columns)
        if df.empty or not {"time", "metric", "value"}.issubset(df.columns):
            continue
        frame = df[["time", "metric", "value"]].copy()
        frame["service"] = _service_series(df)
        frame["metric"] = source + ":" + frame["metric"].astype(str)
        frames.append(frame)

    hist_columns = set(("time", "metric", "sum", "count", *SERVICE_COLUMNS, *ENDPOINT_COLUMNS))
    hist = _safe_read_parquet(input_folder / f"{phase}_metrics_histogram.parquet", hist_columns)
    if not hist.empty and {"time", "metric", "sum", "count"}.issubset(hist.columns):
        service = _service_series(hist)
        count = pd.to_numeric(hist["count"], errors="coerce")
        total = pd.to_numeric(hist["sum"], errors="coerce")

        mean_frame = hist[["time", "metric"]].copy()
        mean_frame["value"] = total / count.replace(0, np.nan)
        mean_frame["service"] = service
        mean_frame["metric"] = "hist_mean:" + mean_frame["metric"].astype(str)
        frames.append(mean_frame)

        count_frame = hist[["time", "metric"]].copy()
        count_frame["value"] = count
        count_frame["service"] = service
        count_frame["metric"] = "hist_count:" + count_frame["metric"].astype(str)
        frames.append(count_frame)

    if not frames:
        return pd.DataFrame(columns=["time", "metric", "value", "service"])

    data = pd.concat(frames, ignore_index=True)
    data["time"] = pd.to_datetime(data["time"], utc=True, errors="coerce")
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["time", "metric", "service", "value"])
    return data


def _robust_scale(values: pd.Series) -> float:
    quantiles = values.quantile([0.25, 0.75])
    iqr = float(quantiles.iloc[1] - quantiles.iloc[0])
    if math.isfinite(iqr) and iqr > 0:
        return iqr
    std = float(values.std(ddof=0))
    if math.isfinite(std) and std > 0:
        return std
    return 1.0


def _normalized(values: pd.Series, min_value: float, max_value: float) -> pd.Series:
    if not math.isfinite(min_value) or not math.isfinite(max_value) or max_value == min_value:
        return pd.Series([0.0] * len(values), index=values.index)
    return (values - min_value) / (max_value - min_value) * 100.0


def _detect_service_metric_event(
    metric: str,
    service: str,
    normal: pd.DataFrame,
    abnormal: pd.DataFrame,
    config: HeroSASConfig,
) -> MetricEvent | None:
    if len(normal) < config.min_stable_window_size or abnormal.empty:
        return None

    normal = normal.sort_values("time")
    abnormal = abnormal.sort_values("time")
    stable_size = min(config.stable_window_size, len(normal))
    if stable_size < config.min_stable_window_size:
        return None

    normal_values = normal["value"].astype(float)
    abnormal_values = abnormal["value"].astype(float)
    combined = pd.concat([normal_values, abnormal_values], ignore_index=True)
    min_value = float(combined.min())
    max_value = float(combined.max())
    if not math.isfinite(min_value) or not math.isfinite(max_value) or max_value == min_value:
        return None

    normal_norm = _normalized(normal_values, min_value, max_value)
    abnormal_norm = _normalized(abnormal_values, min_value, max_value)
    stable_norm = normal_norm.tail(stable_size)
    stable_std = float(stable_norm.std(ddof=0))
    if not math.isfinite(stable_std) or stable_std > config.stable_std_threshold:
        return None

    baseline_norm = float(stable_norm.mean())
    diff = abnormal_norm - baseline_norm
    peak_pos = int(diff.abs().to_numpy().argmax())
    delta = float(abs(diff.iloc[peak_pos]))
    jump = float(abs(abnormal_norm.iloc[peak_pos] - stable_norm.iloc[-1]))
    if jump <= config.jump_threshold_factor * max(stable_std, config.min_jump_floor):
        return None

    if config.recovery_window_size > 0:
        recovery = abnormal_norm.iloc[peak_pos + 1 : peak_pos + 1 + config.recovery_window_size]
        if len(recovery) == config.recovery_window_size:
            recovery_std = float(recovery.std(ddof=0))
            if recovery_std > config.recovery_std_threshold:
                return None

    stable_raw = normal_values.tail(stable_size)
    baseline_value = float(stable_raw.mean())
    peak_value = float(abnormal_values.iloc[peak_pos])
    robust_z = abs(peak_value - baseline_value) / (_robust_scale(normal_values) + 1e-9)
    if robust_z < config.min_robust_z:
        return None

    direction = "up" if peak_value >= baseline_value else "down"
    score = delta * (1.0 + min(math.log1p(robust_z), 5.0) / 5.0)
    return MetricEvent(
        service=service,
        metric=metric,
        timestamp=abnormal["time"].iloc[peak_pos],
        score=score,
        delta=delta,
        robust_z=robust_z,
        peak_value=peak_value,
        baseline_value=baseline_value,
        direction=direction,
    )


def _clusters(events: list[MetricEvent], minutes: int) -> list[list[MetricEvent]]:
    if not events:
        return []
    sorted_events = sorted(events, key=lambda event: event.timestamp)
    clusters = [[sorted_events[0]]]
    window = pd.Timedelta(minutes=minutes)
    for event in sorted_events[1:]:
        if event.timestamp - clusters[-1][-1].timestamp <= window:
            clusters[-1].append(event)
        else:
            clusters.append([event])
    return clusters


def _detect_metric_events(
    normal: pd.DataFrame,
    abnormal: pd.DataFrame,
    config: HeroSASConfig,
) -> list[MetricEvent]:
    if normal.empty or abnormal.empty:
        return []

    events: list[MetricEvent] = []
    normal_by_metric = {metric: df for metric, df in normal.groupby("metric", sort=False)}
    for metric, abnormal_metric in abnormal.groupby("metric", sort=False):
        normal_metric = normal_by_metric.get(metric)
        if normal_metric is None or normal_metric.empty:
            continue
        normal_by_service = {
            service: df for service, df in normal_metric.groupby("service", sort=False)
        }

        metric_events: list[MetricEvent] = []
        for service, abnormal_service in abnormal_metric.groupby("service", sort=False):
            normal_service = normal_by_service.get(service)
            if normal_service is None:
                continue
            event = _detect_service_metric_event(
                metric=metric,
                service=str(service),
                normal=normal_service,
                abnormal=abnormal_service,
                config=config,
            )
            if event is not None:
                metric_events.append(event)

        if not metric_events:
            continue

        max_score = max(event.score for event in metric_events)
        denoised = [
            event for event in metric_events if event.score >= config.noise_reduction_w * max_score
        ]
        if not denoised:
            continue
        metric_clusters = _clusters(denoised, config.cluster_minutes_k)
        if 1 <= len(metric_clusters) <= config.max_clusters_nc:
            events.extend(denoised)

    if not events:
        return []

    overall_max = max(event.score for event in events)
    threshold = config.final_filter_x * overall_max
    return sorted(
        [event for event in events if event.score >= threshold],
        key=lambda event: event.score,
        reverse=True,
    )


def _fallback_scores(normal: pd.DataFrame, abnormal: pd.DataFrame) -> dict[str, float]:
    if normal.empty or abnormal.empty:
        return {}

    normal_stats = normal.groupby(["service", "metric"])["value"].agg(["mean", "std"])
    abnormal_stats = abnormal.groupby(["service", "metric"])["value"].agg(["mean", "count"])
    service_scores: dict[str, float] = defaultdict(float)
    for (service, metric), row in abnormal_stats.iterrows():
        if (service, metric) not in normal_stats.index:
            continue
        baseline = normal_stats.loc[(service, metric)]
        scale = float(baseline["std"])
        if not math.isfinite(scale) or scale <= 0:
            scale = 1.0
        z_score = abs(float(row["mean"]) - float(baseline["mean"])) / scale
        if math.isfinite(z_score):
            service_scores[str(service)] += math.log1p(z_score) * math.log1p(float(row["count"]))
    return dict(service_scores)


def _aggregate_events(events: list[MetricEvent]) -> dict[str, float]:
    by_service: dict[str, list[MetricEvent]] = defaultdict(list)
    for event in events:
        by_service[event.service].append(event)

    scores: dict[str, float] = {}
    for service, service_events in by_service.items():
        max_score = max(event.score for event in service_events)
        total_score = sum(event.score for event in service_events)
        metric_count = len({event.metric for event in service_events})
        scores[service] = max_score + 0.25 * total_score + 2.0 * math.log1p(metric_count)
    return scores


class HeroSAS(Algorithm):
    def __init__(self, config: HeroSASConfig | None = None):
        self.config = config or HeroSASConfig()

    def needs_cpu_count(self) -> int | None:
        return 1

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        input_folder = Path(args.input_folder)
        normal = _metric_frame(input_folder, "normal")
        abnormal = _metric_frame(input_folder, "abnormal")
        if normal.empty or abnormal.empty:
            return []

        events = _detect_metric_events(normal, abnormal, self.config)
        scores = _aggregate_events(events)
        if not scores:
            logger.warning(
                f"HeroSAS found no stable-window events for {args.datapack}; using robust mean-shift fallback"
            )
            scores = _fallback_scores(normal, abnormal)

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [
            AlgorithmAnswer(level="service", name=service, rank=rank)
            for rank, (service, _score) in enumerate(ranked, start=1)
        ]
