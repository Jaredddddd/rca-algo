import pandas as pd
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import timeit

from .aiops_adatper import AIOPSDataAdapter
from typing import Tuple, Dict, List
"""
service_metrics=service_metrics,
fault_type=fault_type,
fault_time=fault_time,
dataset=args.dataset,
"""


def aiops_rca(
    service_metrics: pd.DataFrame,
    fault_type: str,
    fault_time: str,
    dataset: str = "AIOPS",
) -> Tuple[Dict[str, List[str]], pd.DataFrame]:
    """
    Perform root cause analysis using AIOPS data.

    Args:
        service_metrics (pd.DataFrame): Service metrics data.
        fault_type (str): Type of fault.
        fault_time (str): Time of the fault.
        dataset (str): Name of the dataset.
    Returns:
        Dict[str, List[str]]: Dictionary with "ranks" key containing ordered service names.
    """
    normal_df = service_metrics[(service_metrics["time"] < fault_time)]
    abnormal_df = service_metrics[(service_metrics["time"] >= fault_time)]
    # use 3-sigma rule to detect anomalies, group by service_name and metric and calculate mean and std
    normal_stats = (
        normal_df.groupby(["service_name", "metric"])
        .agg(mean=("value", "mean"), std=("value", "std"))
        .reset_index()
    )
    # use 3-sigma rule to detect anomalies
    abnormal_df = abnormal_df.merge(
        normal_stats, on=["service_name", "metric"], how="left", suffixes=("", "_stats")
    )
    abnormal_df["anomaly"] = (
        abnormal_df["value"] > abnormal_df["mean"] + 3 * abnormal_df["std"]
    ) | (abnormal_df["value"] < abnormal_df["mean"] - 3 * abnormal_df["std"])

    # Group by service_name and count anomalies, then rank by anomaly count
    service_ranking = (
        abnormal_df.groupby("service_name")["anomaly"]
        .sum()
        .reset_index()
        .rename(columns={"anomaly": "anomaly_count"})
        .sort_values("anomaly_count", ascending=False)
        .reset_index(drop=True)
    )
    service_ranking["rank"] = service_ranking.index + 1

    return ({"ranks": service_ranking["service_name"].tolist()}, abnormal_df)


class AIOPSRCA(Algorithm):
    def needs_cpu_count(self) -> int | None:
        return 4

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        adapter = AIOPSDataAdapter(aiops_rca)
        return adapter(args)
