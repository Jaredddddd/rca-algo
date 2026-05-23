from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import timeit

from .nezha_adapter import NezhaDataAdapter


def nezha_rca(
    normal_logs: pd.DataFrame,
    abnormal_logs: pd.DataFrame,
    normal_metrics: pd.DataFrame,
    abnormal_metrics: pd.DataFrame,
    normal_traces: pd.DataFrame,
    abnormal_traces: pd.DataFrame,
    dataset: str = "NEZHA",
) -> Dict[str, List[str]]:
    """
    Perform root cause analysis using Nezha-style data with voting mechanism.

    Args:
        normal_logs: Normal log data
        abnormal_logs: Abnormal log data
        normal_metrics: Normal metrics data
        abnormal_metrics: Abnormal metrics data
        normal_traces: Normal trace data
        abnormal_traces: Abnormal trace data
        dataset: Name of the dataset

    Returns:
        Tuple of (dict with "ranks" key, debug DataFrame)
    """

    # Collect results from all three modalities
    metric_pods = _detect_metric_anomalies(normal_metrics, abnormal_metrics)
    trace_pods = _detect_trace_anomalies(normal_traces, abnormal_traces)
    log_pods = _detect_log_anomalies(normal_logs, abnormal_logs)

    # Use voting mechanism to combine results
    final_ranks = _vote_combine_results(metric_pods, trace_pods, log_pods)

    # Choose debug DataFrame based on which method contributed most

    return {"ranks": final_ranks}


def _vote_combine_results(
    metric_pods: List[str], trace_pods: List[str], log_pods: List[str]
) -> List[str]:
    """
    Combine results from different modalities using voting mechanism.

    Args:
        metric_pods: List of pods detected by metric analysis
        trace_pods: List of pods detected by trace analysis
        log_pods: List of pods detected by log analysis

    Returns:
        Combined ranked list of pods
    """
    from collections import defaultdict

    # Count votes for each pod with position-based scoring
    pod_scores = defaultdict(float)

    # Score pods based on their rank in each method (higher rank = higher score)
    def add_scores(pods, method_weight=1.0):
        for i, pod in enumerate(pods[:5]):  # Only consider top 5 from each method
            # Score decreases with rank: rank 1 gets 5 points, rank 2 gets 4 points, etc.
            score = (5 - i) * method_weight
            pod_scores[pod] += score

    # Add scores from each method with equal weight
    if metric_pods:
        add_scores(metric_pods, method_weight=1.2)  # Slightly higher weight for metrics
    if trace_pods:
        add_scores(trace_pods, method_weight=1.0)
    if log_pods:
        add_scores(log_pods, method_weight=1.0)

    # If no results from any method, return empty list
    if not pod_scores:
        return []

    # Sort by combined score (descending) and return top 5
    sorted_pods = sorted(pod_scores.items(), key=lambda x: x[1], reverse=True)
    return [pod for pod, _ in sorted_pods[:5]]


def _detect_metric_anomalies(
    normal_metrics: pd.DataFrame, abnormal_metrics: pd.DataFrame
) -> List[str]:
    """Detect anomalies using metric data (adapted from demo_pair metric RCA)"""
    if normal_metrics.empty or abnormal_metrics.empty:
        return []

    anomalies = []

    # Define available metrics
    cpu_metric = (
        "CpuUsageRate(%)" if "CpuUsageRate(%)" in abnormal_metrics.columns else None
    )
    memory_metric = (
        "MemoryUsageRate(%)"
        if "MemoryUsageRate(%)" in abnormal_metrics.columns
        else None
    )
    latency_metrics = [
        col for col in abnormal_metrics.columns if "Latency" in col and "P9" in col
    ]

    if "service_name" not in abnormal_metrics.columns:
        print("Warning: service_name column not found in metrics")
        return []

    # Group by service_name and calculate thresholds from normal data
    for pod_name in abnormal_metrics["service_name"].unique():
        if pod_name not in normal_metrics["service_name"].values:
            continue

        normal_pod_data = normal_metrics[normal_metrics["service_name"] == pod_name]
        abnormal_pod_data = abnormal_metrics[
            abnormal_metrics["service_name"] == pod_name
        ]

        if normal_pod_data.empty or abnormal_pod_data.empty:
            continue

        matched_metrics = []
        metric_values = {}
        thresholds = {}

        # Check CPU metric
        if cpu_metric and cpu_metric in normal_pod_data.columns:
            threshold = normal_pod_data[cpu_metric].quantile(0.95)
            max_value = abnormal_pod_data[cpu_metric].max()
            if max_value > 1.19 * threshold and max_value > 80:
                matched_metrics.append(cpu_metric)
                metric_values[cpu_metric] = max_value
                thresholds[cpu_metric] = threshold

        # Check memory metric
        if memory_metric and memory_metric in normal_pod_data.columns:
            threshold = normal_pod_data[memory_metric].quantile(0.95)
            max_value = abnormal_pod_data[memory_metric].max()
            if max_value > 1.19 * threshold and max_value > 80:
                matched_metrics.append(memory_metric)
                metric_values[memory_metric] = max_value
                thresholds[memory_metric] = threshold

        # Check latency metrics (if available)
        for metric in latency_metrics:
            if metric in normal_pod_data.columns:
                threshold = normal_pod_data[metric].quantile(0.95)
                max_value = abnormal_pod_data[metric].max()
                if max_value > 1.19 * threshold:
                    matched_metrics.append(metric)
                    metric_values[metric] = max_value
                    thresholds[metric] = threshold

        if matched_metrics:
            anomalies.append(
                {
                    "pod": pod_name,
                    "metrics": matched_metrics,
                    "values": metric_values,
                    "thresholds": thresholds,
                }
            )

    if anomalies:
        # Sort by anomaly score (prioritize CPU, then memory, then highest ratio)
        def get_anomaly_score(anomaly):
            # Prioritize CPU metric
            if cpu_metric and cpu_metric in anomaly["metrics"]:
                v = anomaly["values"].get(cpu_metric, 0)
                t = anomaly["thresholds"].get(cpu_metric, 1e-8)
                return v / t if t != 0 else 0
            # Then memory metric
            elif memory_metric and memory_metric in anomaly["metrics"]:
                v = anomaly["values"].get(memory_metric, 0)
                t = anomaly["thresholds"].get(memory_metric, 1e-8)
                return v / t if t != 0 else 0
            # Finally other metrics
            elif anomaly["metrics"]:
                metric = anomaly["metrics"][0]
                v = anomaly["values"].get(metric, 0)
                t = anomaly["thresholds"].get(metric, 1e-8)
                return v / t if t != 0 else 0
            return 0

        anomalies.sort(key=get_anomaly_score, reverse=True)
        return [anomaly["pod"] for anomaly in anomalies[:5]]

    return []


def _detect_trace_anomalies(
    normal_traces: pd.DataFrame, abnormal_traces: pd.DataFrame
) -> List[str]:
    """Detect anomalies using trace data (adapted from demo_pair trace RCA)"""
    if normal_traces.empty or abnormal_traces.empty:
        return []

    try:
        # Calculate latency metrics for each pod
        latency_results = {}

        for pod_name in abnormal_traces["service_name"].unique():
            if "frontend" in str(pod_name).lower():
                continue  # Skip frontend pods

            p90_latency = _get_latency_metric(abnormal_traces, pod_name)
            if p90_latency > 100:  # Threshold for anomaly
                latency_results[pod_name] = p90_latency

        if latency_results:
            # Sort by latency and return top 5
            sorted_pods = sorted(
                latency_results.items(), key=lambda x: x[1], reverse=True
            )
            return [pod for pod, _ in sorted_pods[:5]]

    except Exception as e:
        print(f"Error in trace anomaly detection: {e}")

    return []


def _get_latency_metric(trace_df: pd.DataFrame, pod_name: str) -> float:
    """Calculate P90 latency for a pod (adapted for new trace format)"""
    try:
        latency_list = []

        # Filter traces for this pod
        pod_spans = trace_df[trace_df["service_name"] == pod_name]

        if (
            pod_spans.empty
            or "parent_span_id" not in pod_spans.columns
            or "duration" not in pod_spans.columns
        ):
            return 0.0

        # For the new format, we can use duration directly or calculate parent-child latencies
        # Method 1: Use duration field directly (convert from nanoseconds to milliseconds)
        if "duration" in pod_spans.columns:
            durations_ms = (
                pod_spans["duration"] / 1000000
            )  # Convert nanoseconds to milliseconds
            if len(durations_ms) > 2:
                return np.percentile(durations_ms, 90)

        # Method 2: Calculate parent-child latencies (fallback)
        if "span_id" in trace_df.columns and "parent_span_id" in pod_spans.columns:
            # Create lookup for parent spans
            parent_lookup = trace_df.set_index("span_id")[
                ["service_name", "duration"]
            ].to_dict("index")

            for _, span in pod_spans.iterrows():
                parent_id = span.get("parent_span_id")
                if pd.isna(parent_id) or parent_id not in parent_lookup:
                    continue

                parent_info = parent_lookup[parent_id]
                parent_pod_name = parent_info.get("service_name")
                parent_duration = parent_info.get("duration", 0)

                if parent_pod_name != pod_name and parent_duration > 0:
                    latency_ms = parent_duration / 1000000  # Convert to ms
                    latency_list.append(latency_ms)

            if len(latency_list) > 2:
                return np.percentile(latency_list, 90)

    except Exception as e:
        print(f"Error calculating latency for {pod_name}: {e}")

    return 0.0


def _detect_log_anomalies(
    normal_logs: pd.DataFrame, abnormal_logs: pd.DataFrame
) -> List[str]:
    """Detect anomalies using log data with new level-based error detection"""
    if abnormal_logs.empty:
        return []

    # Method 1: Error ratio increase detection (if normal logs available)
    if not normal_logs.empty:
        error_pods = _detect_error_ratio_increase(normal_logs, abnormal_logs)
        if error_pods:
            return error_pods

        # Method 2: Log count reduction detection
        count_pods = _detect_count_reduction(normal_logs, abnormal_logs)
        if count_pods:
            return count_pods

    # Fallback: Simple error detection on abnormal logs only
    return _detect_simple_errors(abnormal_logs)


def _detect_error_ratio_increase(
    normal_logs: pd.DataFrame, abnormal_logs: pd.DataFrame
) -> List[str]:
    """Detect pods with increased error ratios using level column"""
    if "level" not in normal_logs.columns or "level" not in abnormal_logs.columns:
        return []

    if (
        "service_name" not in normal_logs.columns
        or "service_name" not in abnormal_logs.columns
    ):
        return []

    def count_error_logs(df):
        df = df.copy()
        df["has_error"] = df["level"] != "INFO"
        error_counts = df[df["has_error"]].groupby("service_name").size()
        total_counts = df.groupby("service_name").size()
        return error_counts, total_counts

    normal_error_counts, normal_total_counts = count_error_logs(normal_logs)
    abnormal_error_counts, abnormal_total_counts = count_error_logs(abnormal_logs)

    error_ratio_changes = []
    all_pods = set(normal_total_counts.index) | set(abnormal_total_counts.index)

    for pod in all_pods:
        normal_errors = normal_error_counts.get(pod, 0)
        normal_total = normal_total_counts.get(pod, 1)
        abnormal_errors = abnormal_error_counts.get(pod, 0)
        abnormal_total = abnormal_total_counts.get(pod, 1)

        normal_ratio = normal_errors / normal_total if normal_total > 0 else 0
        abnormal_ratio = abnormal_errors / abnormal_total if abnormal_total > 0 else 0

        # Detect significant error ratio increase
        if (
            abnormal_ratio > normal_ratio * 1.5
            and abnormal_errors > 0
            and abnormal_total > 10
        ):
            error_ratio_changes.append((pod, abnormal_ratio - normal_ratio))

    if error_ratio_changes:
        error_ratio_changes.sort(key=lambda x: x[1], reverse=True)
        return [pod for pod, _ in error_ratio_changes[:5]]

    return []


def _detect_count_reduction(
    normal_logs: pd.DataFrame, abnormal_logs: pd.DataFrame
) -> List[str]:
    """Detect pods with reduced log counts (filtering out error spans from normal)"""
    if (
        "service_name" not in normal_logs.columns
        or "service_name" not in abnormal_logs.columns
    ):
        return []

    # Filter out error spans from both normal and abnormal data
    normal_logs_clean = normal_logs[normal_logs["level"] == "INFO"].copy()
    abnormal_logs_clean = abnormal_logs[abnormal_logs["level"] == "INFO"].copy()

    normal_counts = normal_logs_clean.groupby("service_name").size()
    abnormal_counts = abnormal_logs_clean.groupby("service_name").size()

    count_reductions = []

    for pod in normal_counts.index:
        normal_count = normal_counts.get(pod, 0)
        abnormal_count = abnormal_counts.get(pod, 0)

        # If log count drops significantly (>40% reduction)
        if (
            normal_count > 0
            and abnormal_count < normal_count * 0.6
            and normal_count > 40
        ):
            reduction_ratio = (normal_count - abnormal_count) / normal_count
            count_reductions.append((pod, reduction_ratio))

    if count_reductions:
        count_reductions.sort(key=lambda x: x[1], reverse=True)
        return [pod for pod, _ in count_reductions[:5]]

    return []


def _detect_simple_errors(abnormal_logs: pd.DataFrame) -> List[str]:
    """Simple error detection when only abnormal logs are available"""
    if (
        "level" not in abnormal_logs.columns
        or "service_name" not in abnormal_logs.columns
    ):
        return []

    # Count error logs per pod
    abnormal_logs = abnormal_logs.copy()
    abnormal_logs["has_error"] = abnormal_logs["level"] != "INFO"

    pod_error_counts = (
        abnormal_logs[abnormal_logs["has_error"]]
        .groupby("service_name")
        .size()
        .sort_values(ascending=False)
    )

    if not pod_error_counts.empty:
        # Remove frontend pod if there are multiple pods with errors
        if len(pod_error_counts) >= 2:
            frontend_pods = [
                pod for pod in pod_error_counts.index if "frontend" in str(pod).lower()
            ]
            for frontend_pod in frontend_pods:
                if frontend_pod in pod_error_counts.index:
                    pod_error_counts = pod_error_counts.drop(frontend_pod)

        return pod_error_counts.index.tolist()[:5]

    return []


class NezhaRCA(Algorithm):
    def needs_cpu_count(self) -> int | None:
        return 4

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        adapter = NezhaDataAdapter(nezha_rca)
        return adapter(args)
