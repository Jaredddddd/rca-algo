import re

import numpy as np
import pandas as pd
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)

from .adapter import DataAdapter

def clean_node_name(node_name):
    """Clean node name by removing pod suffix (e.g., -b5ccf8557-j4txs)"""
    if not node_name:
        return node_name

    # Split by '-' and remove the last two parts if they look like pod suffixes
    parts = node_name.split("-")
    if len(parts) >= 3:
        # Check if last two parts look like pod suffixes (alphanumeric)
        last_part = parts[-1]
        second_last_part = parts[-2]

        # If both parts are alphanumeric and reasonably short, assume they're pod suffixes
        if (
            len(last_part) <= 10
            and last_part.isalnum()
            and len(second_last_part) <= 10
            and second_last_part.isalnum()
        ):
            return "-".join(parts[:-2])

    return node_name


def simplerca(data, normal_dfs=None, dataset="", fault_type=""):
    """
    Root Cause Analysis function based on logs, traces, and metrics
    Args:
        data: list containing [log_df, metric_df, trace_df]
        normal_dfs: list containing normal data (not used in current implementation)
        dataset: dataset name
    Returns:
        dict with 'ranks' key containing list of ranked node names
    """
    log_df, metric_df, trace_df = data

    # Convert Polars to Pandas if needed
    if hasattr(log_df, "to_pandas"):
        log_df = log_df.to_pandas()
    if hasattr(metric_df, "to_pandas"):
        metric_df = metric_df.to_pandas()
    if hasattr(trace_df, "to_pandas"):
        trace_df = trace_df.to_pandas()

    # Convert normal data if provided
    normal_metric_df = None
    normal_log_df = None
    if normal_dfs is not None:
        if len(normal_dfs) > 0:
            normal_log_df = normal_dfs[0]  # log_df is at index 0
            if hasattr(normal_log_df, "to_pandas"):
                normal_log_df = normal_log_df.to_pandas()
        if len(normal_dfs) > 1:
            normal_metric_df = normal_dfs[1]  # metric_df is at index 1
            if hasattr(normal_metric_df, "to_pandas"):
                normal_metric_df = normal_metric_df.to_pandas()

    # Define error keywords
    ERROR_KWS = ["error", "fail", "exception", "timeout", "refused"]
    error_pattern = re.compile(r"|".join(ERROR_KWS), re.IGNORECASE)

    # Get unique service names from all data sources
    node_names = set()
    if "service_name" in log_df.columns:
        node_names.update(log_df["service_name"].dropna().unique())
    if "service_name" in metric_df.columns:
        node_names.update(metric_df["service_name"].dropna().unique())
    if "service_name" in trace_df.columns:
        node_names.update(trace_df["service_name"].dropna().unique())

    node_names = list(node_names)

    # Root cause analysis on logs
    log_scores = analyze_logs(log_df, error_pattern, ERROR_KWS, normal_log_df)

    # Root cause analysis on traces
    trace_scores = analyze_traces(trace_df)

    # Root cause analysis on metrics
    metric_scores = analyze_metrics(metric_df, normal_metric_df)

    # Combine scores and rank nodes
    combined_scores = combine_scores(
        log_scores, trace_scores, metric_scores, node_names
    )

    # Sort by score (descending) and return ranked list
    ranked_nodes = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Clean node names before returning
    cleaned_ranks = [clean_node_name(node) for node, score in ranked_nodes]

    return {"ranks": cleaned_ranks}


def analyze_logs(log_df, error_pattern, error_kws, normal_log_df=None):
    """Analyze logs for error indicators and frequency changes using notebook logic"""
    scores = {}

    if log_df.empty or "service_name" not in log_df.columns:
        return scores

    # Parse log events if needed (similar to notebook's parse_log_line)
    if "message" in log_df.columns:
        log_df = log_df.copy()
        # Extract log events from messages (simplified version of notebook logic)
        log_df["log_event"] = log_df["message"]

        # Calculate time windows in minutes
        anomalous_duration_minutes = get_time_window_minutes(log_df)

        # Calculate normal log frequencies if normal data available
        normal_frequencies = {}
        normal_error_frequencies = {}
        normal_duration_minutes = 1  # Default fallback

        if (
            normal_log_df is not None
            and not normal_log_df.empty
            and "service_name" in normal_log_df.columns
        ):
            normal_log_df = normal_log_df.copy()
            normal_log_df["log_event"] = normal_log_df["message"]
            normal_duration_minutes = get_time_window_minutes(normal_log_df)

            # Calculate normal phase frequencies per service (per minute)
            for service in normal_log_df["service_name"].unique():
                service_normal_logs = normal_log_df[
                    normal_log_df["service_name"] == service
                ]
                total_logs = len(service_normal_logs)
                normal_frequencies[service] = (
                    total_logs / normal_duration_minutes
                    if normal_duration_minutes > 0
                    else 0
                )

                # Count normal phase error logs (per minute)
                normal_error_count = sum(
                    bool(error_pattern.search(str(msg)))
                    for msg in service_normal_logs["log_event"]
                )
                normal_error_frequencies[service] = (
                    normal_error_count / normal_duration_minutes
                    if normal_duration_minutes > 0
                    else 0
                )

        # Analyze anomalous phase logs
        for service in log_df["service_name"].unique():
            service_logs = log_df[log_df["service_name"] == service]

            # Count error occurrences per service (notebook's has_kw logic)
            error_count = sum(
                bool(error_pattern.search(str(msg)))
                for msg in service_logs["log_event"]
            )

            # Calculate frequency ratios as scores
            score = 0

            # Add frequency analysis if normal data available
            if service in normal_frequencies:
                current_total_logs = len(service_logs)
                current_frequency_per_min = (
                    current_total_logs / anomalous_duration_minutes
                    if anomalous_duration_minutes > 0
                    else 0
                )
                current_error_frequency_per_min = (
                    error_count / anomalous_duration_minutes
                    if anomalous_duration_minutes > 0
                    else 0
                )

                normal_frequency_per_min = normal_frequencies[service]
                normal_error_frequency_per_min = normal_error_frequencies.get(
                    service, 0
                )

                # Error frequency ratio
                if (
                    normal_error_frequency_per_min == 0
                    and current_error_frequency_per_min > 0
                ):
                    # New errors appeared where there were none before
                    score += 100
                elif normal_error_frequency_per_min > 0:
                    # Calculate error frequency ratio
                    error_ratio = (
                        current_error_frequency_per_min / normal_error_frequency_per_min
                    )
                    score += error_ratio * 50  # Scale the ratio

                # Normal log frequency decrease ratio
                if normal_frequency_per_min == 0 and current_frequency_per_min == 0:
                    # Both are 0, no change
                    pass
                elif normal_frequency_per_min == 0 and current_frequency_per_min > 0:
                    # Logs appeared where there were none
                    score += 20
                elif normal_frequency_per_min > 0:
                    # Calculate frequency decrease (inverted ratio)
                    frequency_ratio = (
                        current_frequency_per_min / normal_frequency_per_min
                    )
                    if frequency_ratio < 1.0:  # Frequency decreased
                        decrease_score = (
                            1.0 - frequency_ratio
                        ) * 30  # Scale inverted ratio
                        score += decrease_score
            else:
                # No normal data, just use error count
                score = error_count * 10

            scores[service] = score

    return scores


def get_time_window_minutes(df):
    """Calculate time window duration in minutes from dataframe timestamps"""
    if df.empty or "timestamp" not in df.columns:
        return 1  # Default fallback

    try:
        # Convert timestamp to datetime if it's not already
        if df["timestamp"].dtype == "object":
            timestamps = pd.to_datetime(df["timestamp"])
        else:
            timestamps = df["timestamp"]

        # Calculate duration in minutes
        min_time = timestamps.min()
        max_time = timestamps.max()
        duration_seconds = (max_time - min_time).total_seconds()
        duration_minutes = max(duration_seconds / 60, 1)  # At least 1 minute

        return duration_minutes
    except:
        return 1  # Default fallback


def analyze_traces(trace_df):
    """Analyze traces for latency anomalies using notebook logic"""
    scores = {}

    if trace_df.empty or "service_name" not in trace_df.columns:
        return scores

    # Calculate latency metrics for each service using notebook's method
    for service in trace_df["service_name"].unique():
        try:
            latency_score = get_latency_metric(trace_df, service)
            # Only consider high latency scores (>100 like in notebook)
            if latency_score > 100:
                scores[service] = latency_score
            else:
                scores[service] = 0
        except:
            scores[service] = 0

    return scores


def analyze_metrics(metric_df, normal_metric_df=None):
    """Analyze metrics for resource anomalies using normal data for threshold calculation"""
    scores = {}

    if metric_df.empty:
        return scores

    # Group by service_name
    if "service_name" in metric_df.columns:
        groupby_col = "service_name"
    else:
        return scores

    # Use normal data for threshold calculation if available
    for service in metric_df[groupby_col].unique():
        service_metrics = metric_df[metric_df[groupby_col] == service]
        score = 0

        # Get normal data for this service if available
        normal_service_metrics = None
        if normal_metric_df is not None and not normal_metric_df.empty:
            if groupby_col in normal_metric_df.columns:
                normal_service_metrics = normal_metric_df[
                    normal_metric_df[groupby_col] == service
                ]

        # CPU anomaly detection (highest priority like notebook)
        cpu_metrics = service_metrics[
            service_metrics["metric"].str.contains("Cpu|CPU", case=False, na=False)
        ]
        if not cpu_metrics.empty and "value" in cpu_metrics.columns:
            values = cpu_metrics["value"].dropna()
            if len(values) > 0:
                mean_val, sigma_threshold = get_six_sigma_threshold(
                    normal_service_metrics, "Cpu|CPU", values
                )
                for value in values:
                    # Use 6-sigma threshold instead of hardcoded values
                    if value > sigma_threshold:
                        score += 100  # Very high priority for CPU anomalies

        # Network latency anomaly detection (new from notebook)
        network_metrics = service_metrics[
            service_metrics["metric"] == "Network_Latency"
        ]
        if not network_metrics.empty and "value" in network_metrics.columns:
            values = network_metrics["value"].dropna()
            if len(values) > 0:
                mean_val, sigma_threshold = get_six_sigma_threshold(
                    normal_service_metrics, "Network_Latency", values, exact_match=True
                )
                for value in values:
                    if value > sigma_threshold:
                        score += 50  # High priority for network latency

        # Other latency anomaly detection
        latency_metrics = service_metrics[
            service_metrics["metric"].str.contains("Latency", case=False, na=False)
            & (service_metrics["metric"] != "Network_Latency")
        ]
        if not latency_metrics.empty and "value" in latency_metrics.columns:
            values = latency_metrics["value"].dropna()
            if len(values) > 0:
                mean_val, sigma_threshold = get_six_sigma_threshold(
                    normal_service_metrics, "Latency", values
                )
                for value in values:
                    if value > sigma_threshold:
                        score += 20  # Medium priority for other latency anomalies

        scores[service] = score

    return scores


def get_six_sigma_threshold(
    normal_service_metrics, metric_pattern, fallback_values, exact_match=False
):
    """Get 6-sigma threshold from normal data or fallback to current data"""
    if normal_service_metrics is not None and not normal_service_metrics.empty:
        if exact_match:
            normal_metrics = normal_service_metrics[
                normal_service_metrics["metric"] == metric_pattern
            ]
        else:
            normal_metrics = normal_service_metrics[
                normal_service_metrics["metric"].str.contains(
                    metric_pattern, case=False, na=False
                )
            ]

        if not normal_metrics.empty and "value" in normal_metrics.columns:
            normal_values = normal_metrics["value"].dropna()
            if len(normal_values) > 1:  # Need at least 2 values to calculate std
                mean_val = normal_values.mean()
                std_val = normal_values.std()
                sigma_threshold = mean_val + 6 * std_val
                return mean_val, sigma_threshold

    # Fallback to current data for 6-sigma calculation
    if len(fallback_values) > 1:
        mean_val = fallback_values.mean()
        std_val = fallback_values.std()
        sigma_threshold = mean_val + 6 * std_val
        return mean_val, sigma_threshold
    else:
        # If we can't calculate std, use the max value as threshold
        max_val = fallback_values.max() if len(fallback_values) > 0 else 0
        return max_val, max_val


def get_threshold(
    normal_service_metrics, metric_pattern, fallback_values, exact_match=False
):
    """Get threshold from normal data or fallback to current data"""
    # This function is kept for backward compatibility but now uses 6-sigma
    mean_val, sigma_threshold = get_six_sigma_threshold(
        normal_service_metrics, metric_pattern, fallback_values, exact_match
    )
    return sigma_threshold


def combine_scores(log_scores, trace_scores, metric_scores, all_nodes):
    """Combine scores using weighted approach instead of pure fallback"""
    combined = {}

    for node in all_nodes:
        metric_score = metric_scores.get(node, 0)
        trace_score = trace_scores.get(node, 0)
        log_score = log_scores.get(node, 0)

        # Check if this node has CPU anomalies (highest priority)
        if metric_score >= 100:
            combined[node] = (
                metric_score + log_score * 0.3
            )  # Add log boost for CPU issues
        # Check if this node has other metric anomalies
        elif metric_score > 0:
            combined[node] = metric_score + log_score * 0.5  # Medium log weight
        # Check if this node has trace anomalies
        elif trace_score > 0:
            combined[node] = trace_score + log_score * 0.7  # Higher log weight
        # Only log anomalies
        else:
            combined[node] = log_score

    return combined


def get_latency_metric(trace_df, service_name):
    if "front" in service_name.lower():
        return 10  # Frontend special case from notebook

    try:
        service_traces = trace_df[trace_df["service_name"] == service_name]
        if service_traces.empty:
            return 1

        # Notebook uses P90 latency calculation
        if "duration" in service_traces.columns:
            # Duration is in nanoseconds, convert to microseconds (notebook uses microseconds)
            latencies = service_traces["duration"] / 1000  # Convert to microseconds
            latencies = latencies.dropna()

            if len(latencies) > 2:
                return np.percentile(latencies, 90)
            else:
                return 1
        else:
            return 1
    except:
        return 1


class SimpleRCA(Algorithm):
    def needs_cpu_count(self) -> int | None:
        return 1

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        # Use notebook RCA implementation
        adapter = DataAdapter(simplerca)
        return adapter(args)
