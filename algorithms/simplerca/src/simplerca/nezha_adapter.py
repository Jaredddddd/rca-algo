from pathlib import Path
from typing import Any, Callable

import pandas as pd
from rcabench_platform.v2.algorithms.spec import AlgorithmAnswer, AlgorithmArgs
from rcabench_platform.v2.utils.env import debug
from rcabench_platform.v2.utils.serde import save_parquet


class NezhaDataAdapter:
    """Data adapter for Nezha dataset format with parquet files"""

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        """
        Adapt Nezha dataset format to algorithm function

        Args:
            args: AlgorithmArgs containing input folder and other parameters

        Returns:
            List of AlgorithmAnswer objects with ranked service names
        """
        # Load normal and abnormal data from parquet files
        normal_logs = self._load_parquet_safe(args.input_folder / "normal_logs.parquet")
        abnormal_logs = self._load_parquet_safe(
            args.input_folder / "abnormal_logs.parquet"
        )
        normal_metrics = self._load_parquet_safe(
            args.input_folder / "normal_metrics.parquet"
        )
        abnormal_metrics = self._load_parquet_safe(
            args.input_folder / "abnormal_metrics.parquet"
        )
        normal_traces = self._load_parquet_safe(
            args.input_folder / "normal_traces.parquet"
        )
        abnormal_traces = self._load_parquet_safe(
            args.input_folder / "abnormal_traces.parquet"
        )

        # Transform metrics if this is an RCABench dataset
        if args.dataset.startswith("rcabench"):
            normal_metrics = self._transform_rcabench_metrics(normal_metrics)
            abnormal_metrics = self._transform_rcabench_metrics(abnormal_metrics)

        # Call the algorithm function
        output = self.func(
            normal_logs=normal_logs,
            abnormal_logs=abnormal_logs,
            normal_metrics=normal_metrics,
            abnormal_metrics=abnormal_metrics,
            normal_traces=normal_traces,
            abnormal_traces=abnormal_traces,
            dataset=args.dataset,
        )

        ranks = output["ranks"]

        # Convert to AlgorithmAnswer format - use "service" level
        answers: list[AlgorithmAnswer] = []
        for rank, service_name in enumerate(ranks, start=1):
            answers.append(
                AlgorithmAnswer(level="service", name=service_name, rank=rank)
            )

        # Save debug information if enabled
        if debug():
            rows = []
            for rank, service_name in enumerate(ranks, start=1):
                rows.append({"rank": rank, "service_name": service_name})
            df = pd.DataFrame(rows)
            save_parquet(df, path=args.output_folder / "ranks.parquet")

        return answers

    def _transform_rcabench_metrics(self, metrics_df: pd.DataFrame) -> pd.DataFrame:
        """Transform RCABench metrics to Nezha format"""
        if metrics_df.empty:
            return metrics_df

        # Create a copy to avoid modifying the original
        df = metrics_df.copy()

        # Pivot metrics from long to wide format if needed
        if "metric" in df.columns and "value" in df.columns:
            # Pivot to wide format: each metric becomes a column
            df = df.pivot_table(
                index=["time", "service_name"],
                columns="metric",
                values="value",
                aggfunc="mean",
            ).reset_index()
            df.columns.name = None  # Remove the 'metric' name from columns

        # Transform CPU metric
        if "k8s.pod.cpu_limit_utilization" in df.columns:
            df["CpuUsageRate(%)"] = df["k8s.pod.cpu_limit_utilization"] * 100
            df = df.drop(columns=["k8s.pod.cpu_limit_utilization"])

        # Transform memory metric
        if "k8s.pod.memory_limit_utilization" in df.columns:
            df["MemoryUsageRate(%)"] = df["k8s.pod.memory_limit_utilization"] * 100
            df = df.drop(columns=["k8s.pod.memory_limit_utilization"])

        # Keep only the transformed metrics and essential columns
        keep_columns = ["time", "service_name"]
        if "CpuUsageRate(%)" in df.columns:
            keep_columns.append("CpuUsageRate(%)")
        if "MemoryUsageRate(%)" in df.columns:
            keep_columns.append("MemoryUsageRate(%)")

        # Filter to keep only the columns we want
        available_columns = [col for col in keep_columns if col in df.columns]
        df = df[available_columns]

        return df

    def _load_parquet_safe(self, file_path: Path) -> pd.DataFrame:
        """Safely load parquet file, return empty DataFrame if file doesn't exist"""
        try:
            if file_path.exists():
                return pd.read_parquet(file_path)
            else:
                print(f"Warning: {file_path} not found, returning empty DataFrame")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return pd.DataFrame()
