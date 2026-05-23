from pathlib import Path
from typing import Any, Callable, Dict

import pandas as pd
import polars as pl
from rcabench_platform.v2.algorithms.spec import AlgorithmAnswer, AlgorithmArgs
from rcabench_platform.v2.utils.env import debug
from rcabench_platform.v2.utils.serde import load_json, save_parquet


class AIOPSDataAdapter:
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
        fault_info_path = args.input_folder / "metadata.json"
        if fault_info_path.exists():
            fault_info = load_json(path=fault_info_path)

        # Get labels from dataset
        injection_name = fault_info.get("injection_name", "")
        fault_time = fault_info.get("fault_time", "")
        fault_type = fault_info.get("fault_type", "")

        # Load metric data from parquet files (Eadro format)
        service_metrics = self._load_service_metrics_from_parquet(
            args.input_folder, injection_name
        )

        # Call the algorithm function
        output,df = self.func(
            service_metrics=service_metrics,
            fault_type=fault_type,
            fault_time=fault_time,
            dataset=args.dataset,
        )
        ranks = output["ranks"]
        save_parquet(df, path=args.output_folder/"abdf_output.parquet")

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

    def _load_service_metrics_from_parquet(
        self, data_folder: Path, injection_name: str = ""
    ) ->  pd.DataFrame:
        """
        Load pod metrics from parquet files in Eadro format using polars for efficiency

        Args:
            data_folder: Path to the data folder

        Returns:
            Dictionary mapping service_name -> DataFrame with metrics in long format
        """

        # Load single metric.parquet file
        metric_file = data_folder / "metrics.parquet"


        print(f"Loading single metric file: {metric_file}")

        # Use polars to scan and filter data efficiently - keep long format
        df = pd.read_parquet(metric_file).dropna(subset=["value"])

        return df
