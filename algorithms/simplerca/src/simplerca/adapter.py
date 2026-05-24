from collections.abc import Callable
from typing import Any

import pandas as pd
from rcabench_platform.v2.algorithms.spec import AlgorithmAnswer, AlgorithmArgs
from rcabench_platform.v2.datasets.spec import get_datapack_labels
from rcabench_platform.v2.utils.env import debug
from rcabench_platform.v2.utils.serde import save_parquet


class DataAdapter:
    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        folder = args.input_folder

        labels = get_datapack_labels(args.dataset, args.input_folder.name)
        fault_type = ""
        for label in labels:
            if label.level == "type":
                fault_type = label.name

        log = pd.read_parquet(folder / "abnormal_logs.parquet")
        trace = pd.read_parquet(folder / "abnormal_traces.parquet")
        metric = pd.read_parquet(folder / "abnormal_metrics.parquet")

        normal_log = pd.read_parquet(folder / "normal_logs.parquet")
        normal_trace = pd.read_parquet(folder / "normal_traces.parquet")
        normal_metric = pd.read_parquet(folder / "normal_metrics.parquet")

        for df in [log, normal_log]:
            if "time" in df.columns and "timestamp" not in df.columns:
                df.rename(columns={"time": "timestamp"}, inplace=True)

        output = self.func(
            data=[log, metric, trace],
            normal_dfs=[normal_log, normal_metric, normal_trace],
            dataset=args.dataset,
            fault_type=fault_type,
        )
        ranks: list[str] = output["ranks"]

        answers: list[AlgorithmAnswer] = []
        for rank, node_name in enumerate(ranks, start=1):
            answers.append(AlgorithmAnswer(level="service", name=node_name, rank=rank))

        if debug():
            rows = [{"rank": rank, "service_name": name} for rank, name in enumerate(ranks, start=1)]
            save_parquet(pd.DataFrame(rows), path=args.output_folder / "ranks.parquet")

        return answers
