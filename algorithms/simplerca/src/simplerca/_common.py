from collections.abc import Callable
from typing import Any

import pandas as pd
import polars as pl
from rcabench_platform.v2.algorithms.spec import AlgorithmAnswer, AlgorithmArgs
from rcabench_platform.v2.datasets.spec import get_datapack_labels
from rcabench_platform.v2.utils.env import debug
from rcabench_platform.v2.utils.serde import load_json, save_parquet

RENAME_METRICS = {
    "hubble_http_request_duration_p50_seconds": "lat50",
    "hubble_http_request_duration_p90_seconds": "lat90",
    "k8s.pod.cpu.usage": "cpu",
    "k8s.pod.memory.usage": "mem",
    "k8s.pod.memory.available": "avail_mem",
}

NEZHA_REQUEST_METRICS = (
    "CpuUsageRate(%)",
    "MemoryUsageRate(%)",
    "PodClientLatencyP90(s)",
    "PodServerLatencyP90(s)",
    "PodClientLatencyP99(s)",
    "PodServerLatencyP99(s)",
)

NEZHA_RENAME_METRICS = {
    "PodClientLatencyP90(s)": "lat90Client",
    "PodServerLatencyP90(s)": "lat90Server",
    "CpuUsage(m)": "cpu",
    "MemoryUsage(Mi)": "mem",
}


class DataAdapter:
    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        fault_info = load_json(path=args.input_folder / "fault_info.json")
        labels = get_datapack_labels(args.dataset, args.input_folder.name)
        fault_type = ""
        for label in labels:
            if label.level == "type":
                fault_type = label.name

        # Get fault time information
        start = fault_info.get("fault_start_time", "")
        end = fault_info.get("fault_end_time", "")
        inject_time = start

        # Determine normal folder based on dataset
        if args.input_folder.name.startswith("2023-01-29"):
            normal_folder = args.input_folder.parent / "2023-01-29_08-50_normal_case"
            normal_metric_file = "/home/nuevo/workspace/SimpleRCA/normal_metric/2023-01-29/metric.parquet"
        elif args.input_folder.name.startswith("2023-01-30"):
            normal_folder = args.input_folder.parent / "2023-01-30_11-39_normal_case"
            normal_metric_file = "/home/nuevo/workspace/SimpleRCA/normal_metric/2023-01-30/metric.parquet"
        elif args.input_folder.name.startswith("2022-08-22"):
            normal_folder = args.input_folder.parent / "2022-08-22_03-51_normal_case"
            normal_metric_file = "/home/nuevo/workspace/SimpleRCA/normal_metric/2022-08-22/metric.parquet"
        elif args.input_folder.name.startswith("2022-08-23"):
            normal_folder = args.input_folder.parent / "2022-08-23_17-00_normal_case"
            normal_metric_file = "/home/nuevo/workspace/SimpleRCA/normal_metric/2022-08-23/metric.parquet"
        else:
            raise ValueError("Unsupported dataset folder name format.")

        # Load data using pandas for better compatibility
        log = pd.read_parquet(args.input_folder / "log.parquet")
        normal_log = pd.read_parquet(normal_folder / "log.parquet")

        trace = pd.read_parquet(args.input_folder / "trace.parquet")
        normal_trace = pd.read_parquet(normal_folder / "trace.parquet")

        # Filter metric data for the fault period and specific metrics
        # Convert string timestamps to datetime for comparison
        start_dt = pl.lit(start).str.to_datetime()
        end_dt = pl.lit(end).str.to_datetime()

        metric = (
            pl.scan_parquet(args.input_folder / "metric.parquet")
            .filter(
                (pl.col("time") >= start_dt)
                & (pl.col("time") <= end_dt)
                & pl.col("metric").is_in(NEZHA_REQUEST_METRICS)
            )
            .select(
                pl.col("time"),
                pl.col("service_name"),
                pl.col("metric"),
                pl.col("value"),
            )
            .collect()
            .to_pandas()
        )

        # Add network latency calculation like in notebook
        if not metric.empty:
            metric = calculate_network_latency(metric)

        # Normal metric data
        normal_metric = (
            pl.scan_parquet(normal_metric_file)
            .filter(pl.col("metric").is_in(NEZHA_REQUEST_METRICS))
            .select(
                pl.col("time"),
                pl.col("service_name"),
                pl.col("metric"),
                pl.col("value"),
            )
            .collect()
            .to_pandas()
        )

        # Add network latency calculation for normal data
        if not normal_metric.empty:
            normal_metric = calculate_network_latency(normal_metric)

        # Call the algorithm function with fault_type
        output = (self.func)(
            data=[log, metric, trace],
            normal_dfs=[normal_log, normal_metric, normal_trace],
            dataset=args.dataset,
            fault_type=fault_type,
        )
        ranks: list[str] = output["ranks"]

        answers: list[AlgorithmAnswer] = []
        for rank, node_name in enumerate(ranks, start=1):
            answers.append(AlgorithmAnswer(level="pod", name=node_name, rank=rank))

        if debug():
            rows = []
            for rank, node_name in enumerate(ranks, start=1):
                rows.append({"rank": rank, "service_name": node_name})
            df = pd.DataFrame(rows)
            save_parquet(df, path=args.output_folder / "ranks.parquet")

        return answers


def calculate_network_latency(metric_df):
    """Calculate network latency like in the notebook: |ClientP99 - ServerP99|"""
    if metric_df.empty:
        return metric_df

    # Group by service_name and time to calculate network latency
    result_rows = []

    for service in metric_df["service_name"].unique():
        service_data = metric_df[metric_df["service_name"] == service]

        # Group by time to get client and server latencies at same time
        for time_val in service_data["time"].unique():
            time_data = service_data[service_data["time"] == time_val]

            client_p99 = time_data[time_data["metric"] == "PodClientLatencyP99(s)"][
                "value"
            ]
            server_p99 = time_data[time_data["metric"] == "PodServerLatencyP99(s)"][
                "value"
            ]

            if not client_p99.empty and not server_p99.empty:
                # Calculate network latency as absolute difference
                network_latency = abs(client_p99.iloc[0] - server_p99.iloc[0])

                # Add new row for network latency metric
                result_rows.append(
                    {
                        "time": time_val,
                        "service_name": service,
                        "metric": "Network_Latency",
                        "value": network_latency,
                    }
                )

    # Add network latency rows to original dataframe
    if result_rows:
        network_df = pd.DataFrame(result_rows)
        metric_df = pd.concat([metric_df, network_df], ignore_index=True)

    return metric_df
