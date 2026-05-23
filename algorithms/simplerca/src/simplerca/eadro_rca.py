from typing import Dict, List, Tuple

import pandas as pd
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import timeit

from .eadro_adapter import EadroDataAdapter


def eadro_rca(
    pod_metrics: Dict[str, pd.DataFrame],
    fault_type: str = "",
    dataset: str = "",
) -> Dict[str, List[str]]:
    """
    Eadro-based Root Cause Analysis algorithm

    Args:
        pod_metrics: Dictionary mapping service_name -> DataFrame with metrics
        fault_type: Type of fault (for future enhancement)
        dataset: Dataset name (for future enhancement)

    Returns:
        Dictionary with 'ranks' key containing list of ranked service names
    """
    print(f"EadroRCA: Processing {len(pod_metrics)} services for dataset {dataset}")

    # If no service metrics, return empty list
    if not pod_metrics:
        print("No service metrics available")
        return {"ranks": []}

    # Detect anomalies using rule-based approach
    anomalies, all_anomalies = detect_anomalies_rules(pod_metrics, dataset)

    print(
        f"Detected {len(anomalies)} top anomalies, {len(all_anomalies)} total anomalies"
    )

    # Rank services by anomaly severity - match demo logic
    if not anomalies:
        return {"ranks": []}

    # Use the top anomaly (like demo_eadro rc logic)
    top_service = anomalies[0]["pod"]  # Keep "pod" key for compatibility

    # Sort all anomalies by total events (descending) for ranking
    ranked_anomalies = sorted(
        all_anomalies, key=lambda x: x["total_events"], reverse=True
    )

    # Extract service names from ranked anomalies
    ranked_services = [
        anomaly["pod"] for anomaly in ranked_anomalies
    ]  # Keep "pod" key for compatibility

    # Add any remaining services that weren't detected as anomalous
    all_services = set(pod_metrics.keys())
    detected_services = set(ranked_services)
    remaining_services = sorted(all_services - detected_services)

    final_ranks = ranked_services + remaining_services

    print(f"Top detected service: {top_service}")
    print(f"Final ranking: {final_ranks[:5]}{'...' if len(final_ranks) > 5 else ''}")

    return {"ranks": final_ranks}


def detect_anomalies_rules(
    pod_metrics: Dict[str, pd.DataFrame],
    dataset: str = "",
) -> Tuple[List[Dict], List[Dict]]:
    """
    Detect anomalies using rule-based approach on long format data

    Args:
        pod_metrics: Dictionary of service metrics DataFrames in long format
        dataset: Dataset name to determine rules

    Returns:
        Tuple of (top_anomalies, all_anomalies)
    """
    anomalies = []

    # Define detection rules based on dataset type - match demo_eadro exactly
    if "SN" in dataset.upper():
        METRIC_RULES = {
            "cpu_usage_total": lambda x: x > 8,  # CPU total usage > 8
        }
        # For rx/tx we need to calculate the ratio first
        rx_tx_range = (5, 30)
    elif "TT" in dataset.upper():
        METRIC_RULES = {
            "cpu_usage_total": lambda x: x > 8,  # CPU total usage > 8
        }
        rx_tx_range = (8, 30)
    else:
        METRIC_RULES = {
            "cpu_usage_total": lambda x: x > 80,  # CPU usage > 80%
        }
        rx_tx_range = None

    print(f"Applying anomaly detection rules to {len(pod_metrics)} services")

    for service_name, df in pod_metrics.items():
        if df.empty:
            continue

        print(f"Processing service {service_name} with {len(df)} data points")

        # Initialize event counts
        event_counts = {"cpu_usage_total": 0, "rx/tx": 0}

        # Process CPU usage
        cpu_data = df[df["metric"] == "cpu_usage_total"]
        for _, row in cpu_data.iterrows():
            if not pd.isna(row["value"]) and METRIC_RULES["cpu_usage_total"](
                row["value"]
            ):
                event_counts["cpu_usage_total"] += 1

        # Process rx/tx ratio if we have the range defined
        if rx_tx_range:
            # Get rx and tx data by timestamp
            rx_data = df[df["metric"] == "rx_bytes"].set_index("parsed_time")["value"]
            tx_data = df[df["metric"] == "tx_bytes"].set_index("parsed_time")["value"]

            # Calculate rx/tx ratio for each timestamp
            for timestamp in rx_data.index:
                if timestamp in tx_data.index:
                    rx_val = rx_data[timestamp]
                    tx_val = tx_data[timestamp]
                    if not pd.isna(rx_val) and not pd.isna(tx_val) and tx_val != 0:
                        ratio = rx_val / tx_val
                        if rx_tx_range[0] < ratio < rx_tx_range[1]:
                            event_counts["rx/tx"] += 1

        # Calculate total anomaly events
        total_events = sum(event_counts.values())

        print(
            f"Service {service_name}: event_counts={event_counts}, total_events={total_events}"
        )

        # Record anomaly if any events detected
        if total_events > 0:
            anomalies.append(
                {
                    "pod": service_name,  # Keep "pod" key for compatibility
                    "event_counts": event_counts,
                    "total_events": total_events,
                }
            )

    print(f"Total anomalies detected: {len(anomalies)}")

    # Return logic should match demo_eadro exactly
    rc = anomalies
    if len(anomalies) > 1:
        rc = [max(anomalies, key=lambda x: x["total_events"])]

    return rc, anomalies


def sli_filter(
    pod_metric_dict: Dict[str, pd.DataFrame],
    pod_name: str,
    start_time: str,
    duration: int,
) -> bool:
    """
    Filter invalid fault injections based on network activity

    Args:
        pod_metric_dict: Dictionary of pod metrics
        pod_name: Name of pod to check
        start_time: Start time of fault injection
        duration: Duration in seconds

    Returns:
        True if should be filtered (invalid), False otherwise
    """
    try:
        if pod_name not in pod_metric_dict:
            return True  # Filter if pod not found

        # Parse time window
        try:
            # Try parsing as ISO format first
            start_dt = pd.to_datetime(start_time, utc=True)
        except:
            # Fallback to unix timestamp
            start_dt = pd.to_datetime(start_time, unit="s", utc=True)

        end_dt = start_dt + pd.Timedelta(seconds=duration)

        target_pod_df = pod_metric_dict[pod_name]

        if "parsed_time" not in target_pod_df.columns:
            return True

        # Filter to time window
        time_window_df = target_pod_df[
            (target_pod_df["parsed_time"] >= start_dt)
            & (target_pod_df["parsed_time"] <= end_dt)
        ]

        if time_window_df.empty:
            return True

        # Check for network activity
        if (
            "rx_bytes" in time_window_df.columns
            and "tx_bytes" in time_window_df.columns
        ):
            rx_zero_ratio = (time_window_df["rx_bytes"] == 0).mean()
            tx_zero_ratio = (time_window_df["tx_bytes"] == 0).mean()

            # Filter if both rx and tx are 90% zeros (no network activity)
            if rx_zero_ratio >= 0.9 and tx_zero_ratio >= 0.9:
                return True

        return False

    except Exception as e:
        print(f"Error in SLI filter for pod {pod_name}: {e}")
        return True


class EadroRCA(Algorithm):
    """Eadro-based Root Cause Analysis Algorithm"""

    def needs_cpu_count(self) -> int | None:
        return 4

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        adapter = EadroDataAdapter(eadro_rca)
        return adapter(args)
