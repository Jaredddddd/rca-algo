import json
import re
import statistics
from collections import Counter

import numpy as np
import pandas as pd


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


class NotebookRCA:
    def __init__(self):
        # Define error keywords
        self.ERROR_KWS = ["error", "fail", "exception", "timeout", "refused"]
        # Compile regex pattern, case insensitive
        self.error_pattern = re.compile(r"|".join(self.ERROR_KWS), re.IGNORECASE)


    def process_log_data(self, log_df, ns="hipster"):
        """Process log data like notebook's process_log_csv"""
        log_df = log_df.copy()
        log_df["log_event"] = log_df["message"]
        return log_df

    def detect_root_pod(self, ab_df, ns):
        """Detect root pod exactly like notebook"""

        def has_kw(msg):
            return bool(self.error_pattern.search(str(msg)))  # Match any keyword

        ab_df["has_kw"] = ab_df["log_event"].apply(has_kw)
        pod_count = (
            ab_df[ab_df["has_kw"]]
            .groupby("service_name")
            .size()
            .sort_values(ascending=False)
        )

        if not pod_count.empty:
            # Remove frontend pod if there are multiple pods with errors
            if len(pod_count) >= 2 and ns == "hipster":
                frontend_pods = [idx for idx in pod_count.index if "frontend" in idx]
                for frontend_pod in frontend_pods:
                    if frontend_pod in pod_count.index:
                        pod_count = pod_count.drop(frontend_pod)

            if not pod_count.empty:
                return pod_count.index[0]
        return None

    def get_top_fail_event(self, df, root_pod, ns):
        """Find root cause event (most common fail msg) exactly like notebook"""
        pod_df = df[(df["service_name"] == root_pod)]
        fail_msgs = [
            msg
            for msg in pod_df["log_event"]
            if any(kw in str(msg).lower() for kw in self.ERROR_KWS)
        ]
        counter = Counter(fail_msgs)
        if len(counter) >= 2 and ns == "hipster":
            if "Request error" in counter:
                del counter["Request error"]

        return counter.most_common(1)[0][0] if counter else "unknown"

    def rca_on_logs(self, log_df, ns="hipster"):
        """Main log RCA function exactly like notebook"""
        ab_df = self.process_log_data(log_df, ns)

        root_pod = self.detect_root_pod(ab_df, ns)
        if root_pod is None:
            return None, None

        root_event = self.get_top_fail_event(ab_df, root_pod, ns)
        root_event_lower = root_event.lower()

        if ns == "hipster":
            if "fail" in root_event_lower:
                root_type = "exception"
            elif "error" in root_event_lower:
                root_type = "return"
            else:
                root_type = "unknown"
        elif ns == "ts":
            if "exception" in root_event_lower:
                root_type = "exception"
            elif "error" in root_event_lower:
                root_type = "return"
            else:
                root_type = "unknown"

        return root_pod, root_type

    def get_latency_metric(self, trace_df, pod_name):
        """Get latency metric exactly like notebook"""
        if "front" in pod_name.lower():
            return 10, 10

        try:
            # Filter traces for this pod
            pod_traces = trace_df[trace_df["service_name"] == pod_name]
            if pod_traces.empty:
                return 10, 10

            latency_list = []

            # Use duration if available (convert from nanoseconds to microseconds)
            if "duration" in pod_traces.columns:
                latencies = pod_traces["duration"] / 1000  # Convert to microseconds
                latencies = latencies.dropna()
                if len(latencies) > 2:
                    return np.percentile(latencies, 90), statistics.stdev(
                        latencies
                    ) if len(latencies) > 1 else 1
                else:
                    return 1, 1
            else:
                return 1, 1

        except Exception:
            return 1, 1

    def rca_on_trace(self, trace_df):
        """Main trace RCA function exactly like notebook"""
        latency_results = {}

        if trace_df.empty or "service_name" not in trace_df.columns:
            return None, None

        unique_pods = trace_df["service_name"].unique()

        for pod_name in unique_pods:
            p90_latency, _ = self.get_latency_metric(trace_df, pod_name)
            latency_results[pod_name] = p90_latency

        # Create result dataframe
        result_data = [(pod, latency) for pod, latency in latency_results.items()]
        result_df = pd.DataFrame(result_data, columns=["PodName", "P90_Latency"])

        # Filter pods with P90_Latency > 100
        result_df = result_df[result_df["P90_Latency"] > 100].sort_values(
            "P90_Latency", ascending=False
        )

        if len(result_df) == 0:
            return None, None

        root_pod = result_df["PodName"].iloc[0]
        root_cause = "network_delay"
        return root_pod, root_cause

    def detect_anomalies_p95(self, metric_df, normal_metric_df=None, metrics=None):
        """Detect metric anomalies exactly like notebook using normal phase thresholds"""
        if metrics is None:
            metrics = ["CpuUsageRate(%)"]

        anomalies = []

        if metric_df.empty or "service_name" not in metric_df.columns:
            return anomalies

        # Group by service
        for service_name in metric_df["service_name"].unique():
            service_data = metric_df[metric_df["service_name"] == service_name]

            matched_metrics = []
            metric_values = {}
            thresholds = {}

            for metric in metrics:
                if metric in service_data.columns:
                    metric_values_series = service_data[metric].dropna()
                    if len(metric_values_series) > 0:
                        # Calculate threshold from normal data if available
                        threshold = self.get_normal_threshold(
                            normal_metric_df, service_name, metric, metric_values_series
                        )
                        current_value = metric_values_series.iloc[
                            -1
                        ]  # Use latest value

                        if current_value > 1.19 * threshold and current_value > 80:
                            matched_metrics.append(metric)
                            metric_values[metric] = current_value
                            thresholds[metric] = threshold

            if matched_metrics:
                anomalies.append(
                    {
                        "pod": service_name,
                        "metrics": matched_metrics,
                        "values": metric_values,
                        "thresholds": thresholds,
                    }
                )

        return anomalies

    def get_normal_threshold(
        self, normal_metric_df, service_name, metric, fallback_values
    ):
        """Get threshold from normal data or fallback to current data"""
        if (
            normal_metric_df is not None
            and not normal_metric_df.empty
            and "service_name" in normal_metric_df.columns
        ):
            # Filter normal data for this service and metric
            normal_service_data = normal_metric_df[
                (normal_metric_df["service_name"] == service_name)
                & (normal_metric_df["metric"] == metric)
            ]

            if not normal_service_data.empty and "value" in normal_service_data.columns:
                normal_values = normal_service_data["value"].dropna()
                if len(normal_values) > 0:
                    return normal_values.quantile(0.95)

        # Fallback to current data
        return fallback_values.quantile(0.95)

    def filter_top_root_cause_by_priority(self, root_causes):
        """Filter root causes by priority exactly like notebook"""
        if len(root_causes) < 2:
            return root_causes

        cpu_metric = "CpuUsageRate(%)"

        # Step 1: Filter root causes with CPU
        cpu_causes = [cause for cause in root_causes if cpu_metric in cause["metrics"]]

        # Step 2: If CPU exists, compare only these; otherwise compare latency
        if cpu_causes:
            key_metric = cpu_metric
            candidates = cpu_causes
        else:
            # Try to compare latency (pick first latency metric)
            if not root_causes[0]["metrics"]:
                return []
            key_metric = root_causes[0]["metrics"][
                0
            ]  # Assume at least one latency metric
            candidates = root_causes

        # Step 3: Compare value / threshold
        def ratio(cause):
            v = cause["values"].get(key_metric, 0)
            t = cause["thresholds"].get(key_metric, 1e-8)
            return v / t if t != 0 else 0

        best_cause = max(candidates, key=ratio)
        return [best_cause]

    def rca_on_metrics(self, metric_df, normal_metric_df=None):
        """Main metric RCA function"""
        # Check for CPU anomalies first
        cpu_metrics = ["CpuUsageRate(%)"]
        cpu_anomalies = self.detect_anomalies_p95(
            metric_df, normal_metric_df, cpu_metrics
        )

        if cpu_anomalies:
            if len(cpu_anomalies) == 1:
                return clean_node_name(cpu_anomalies[0]["pod"]), "cpu"
            else:
                top_cause = self.filter_top_root_cause_by_priority(cpu_anomalies)
                if top_cause:
                    return clean_node_name(top_cause[0]["pod"]), "cpu"

        # Check for network latency anomalies
        network_metrics = ["Network_Latency"]
        network_anomalies = self.detect_anomalies_p95(
            metric_df, normal_metric_df, network_metrics
        )

        if network_anomalies:
            if len(network_anomalies) == 1:
                return clean_node_name(network_anomalies[0]["pod"]), "network_delay"
            else:
                top_cause = self.filter_top_root_cause_by_priority(network_anomalies)
                if top_cause:
                    return clean_node_name(top_cause[0]["pod"]), "network_delay"

        # Check for other latency anomalies
        latency_metrics = [
            "PodClientLatencyP90(s)",
            "PodServerLatencyP90(s)",
            "PodClientLatencyP99(s)",
            "PodServerLatencyP99(s)",
        ]
        latency_anomalies = self.detect_anomalies_p95(
            metric_df, normal_metric_df, latency_metrics
        )

        if latency_anomalies:
            if len(latency_anomalies) == 1:
                return clean_node_name(latency_anomalies[0]["pod"]), "network_delay"
            else:
                top_cause = self.filter_top_root_cause_by_priority(latency_anomalies)
                if top_cause:
                    return clean_node_name(top_cause[0]["pod"]), "network_delay"

        return None, None

    def run_rca(self, data, normal_dfs=None, dataset="", fault_type=""):
        """Main RCA function that combines all approaches exactly like notebook"""
        log_df, metric_df, trace_df = data

        # Convert to pandas if needed
        if hasattr(log_df, "to_pandas"):
            log_df = log_df.to_pandas()
        if hasattr(metric_df, "to_pandas"):
            metric_df = metric_df.to_pandas()
        if hasattr(trace_df, "to_pandas"):
            trace_df = trace_df.to_pandas()

        # Get normal metric data if available
        normal_metric_df = None
        if normal_dfs is not None and len(normal_dfs) > 1:
            normal_metric_df = normal_dfs[1]
            if hasattr(normal_metric_df, "to_pandas"):
                normal_metric_df = normal_metric_df.to_pandas()

        # Determine namespace based on dataset
        ns = "hipster" if "2022" in dataset else "ts"

        # Try metric RCA first (highest priority for CPU)
        metric_rc_pod, metric_rc_type = self.rca_on_metrics(metric_df, normal_metric_df)

        if metric_rc_pod is not None:
            # Check if fault type matches
            if fault_type and "cpu" in fault_type and metric_rc_type == "cpu":
                return {"ranks": [metric_rc_pod]}
            elif (
                fault_type
                and "network" in fault_type
                and metric_rc_type == "network_delay"
            ):
                return {"ranks": [metric_rc_pod]}
            elif not fault_type:  # No specific fault type required
                return {"ranks": [metric_rc_pod]}

        # Try trace RCA
        trace_rc_pod, trace_rc_type = self.rca_on_trace(trace_df)

        if trace_rc_pod is not None:
            cleaned_trace_pod = clean_node_name(trace_rc_pod)
            if fault_type and trace_rc_type == fault_type:
                return {"ranks": [cleaned_trace_pod]}
            elif not fault_type:
                return {"ranks": [cleaned_trace_pod]}

        # Try log RCA
        log_rc_pod, log_rc_type = self.rca_on_logs(log_df, ns)

        if log_rc_pod is not None:
            cleaned_log_pod = clean_node_name(log_rc_pod)
            if fault_type and log_rc_type == fault_type:
                return {"ranks": [cleaned_log_pod]}
            elif not fault_type:
                return {"ranks": [cleaned_log_pod]}

        # If no root cause found, return empty list
        return {"ranks": []}


def notebook_rca(data, normal_dfs=None, dataset="", fault_type=""):
    """Wrapper function for NotebookRCA"""
    rca = NotebookRCA()
    return rca.run_rca(data, normal_dfs, dataset, fault_type)
