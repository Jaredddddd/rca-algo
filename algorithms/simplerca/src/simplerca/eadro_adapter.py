from pathlib import Path
from typing import Any, Callable, Dict

import pandas as pd
import polars as pl
from rcabench_platform.v2.algorithms.spec import AlgorithmAnswer, AlgorithmArgs
from rcabench_platform.v2.datasets.spec import get_datapack_labels
from rcabench_platform.v2.utils.env import debug
from rcabench_platform.v2.utils.serde import load_json, save_parquet


class EadroDataAdapter:
    """Data adapter for Eadro dataset format"""

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        """
        Adapt Eadro dataset format to algorithm function

        Args:
            args: AlgorithmArgs containing input folder and other parameters

        Returns:
            List of AlgorithmAnswer objects with ranked service names
        """
        # Load fault information if available
        fault_info = {}
        fault_info_path = args.input_folder / "fault_info.json"
        if fault_info_path.exists():
            fault_info = load_json(path=fault_info_path)

        # Get labels from dataset
        labels = get_datapack_labels(args.dataset, args.input_folder.name)
        fault_type = ""
        for label in labels:
            if label.level == "type":
                fault_type = label.name

        # Load metric data from parquet files (Eadro format)
        pod_metrics = self._load_pod_metrics_from_parquet(args.input_folder)

        # Call the algorithm function
        output = self.func(
            pod_metrics=pod_metrics,
            fault_type=fault_type,
            dataset=args.dataset,
        )

        ranks: list[str] = output["ranks"]

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

    def _load_pod_metrics_from_parquet(
        self, data_folder: Path
    ) -> Dict[str, pd.DataFrame]:
        """
        Load pod metrics from parquet files in Eadro format using polars for efficiency

        Args:
            data_folder: Path to the data folder

        Returns:
            Dictionary mapping service_name -> DataFrame with metrics in long format
        """
        service_metric_dict = {}

        # Look for parquet files in the metrics folder or data folder
        metrics_folder = data_folder / "metrics"
        if not metrics_folder.exists():
            metrics_folder = data_folder

        print(f"Loading metrics from: {metrics_folder}")

        # Load single metric.parquet file
        metric_file = metrics_folder / "metric.parquet"
        if not metric_file.exists():
            print(f"metric.parquet not found in {metrics_folder}")
            return service_metric_dict

        try:
            print(f"Loading single metric file: {metric_file}")

            # Use polars to scan and filter data efficiently - keep long format
            df_lazy = (
                pl.scan_parquet(metric_file)
                .filter(
                    pl.col("metric").is_in(["cpu_usage_total", "rx_bytes", "tx_bytes"])
                )
                .with_columns(
                    [
                        pl.from_epoch(pl.col("time"), time_unit="s").alias(
                            "parsed_time"
                        )
                    ]
                )
            )

            # Group by service_name and collect each service data
            for service_name in (
                df_lazy.select("service_name").unique().collect()["service_name"]
            ):
                if service_name is None:
                    continue

                # Filter for this service and collect
                service_df = df_lazy.filter(
                    pl.col("service_name") == service_name
                ).collect()

                if service_df.is_empty():
                    continue

                # Convert to pandas for compatibility with existing algorithm
                pandas_df = service_df.to_pandas()

                service_metric_dict[str(service_name)] = pandas_df
                print(
                    f"Loaded metrics for service: {service_name} ({len(pandas_df)} rows)"
                )

        except Exception as e:
            print(f"Failed to load {metric_file}: {e}")

        print(f"Total services loaded: {len(service_metric_dict)}")
        return service_metric_dict
