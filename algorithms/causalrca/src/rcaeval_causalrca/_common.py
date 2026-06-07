from collections.abc import Callable
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

import pandas as pd
import polars as pl
from rcabench_platform.v2.algorithms.spec import AlgorithmAnswer, AlgorithmArgs
from rcabench_platform.v2.graphs.sdg.build_.rcabench import (
    load_inject_time as rcabench_load_inject_time,
)
from rcabench_platform.v2.graphs.sdg.build_.rcaeval import (
    load_inject_time as rcaeval_load_inject_time,
)
from rcabench_platform.v2.logging import timeit
from rcabench_platform.v2.utils.env import debug
from rcabench_platform.v2.utils.serde import save_parquet
from rcabench_platform.vendor.RCAEval.time_series import preprocess

RENAME_METRICS = {
    "hubble_http_request_duration_p50_seconds": "lat50",
    "hubble_http_request_duration_p90_seconds": "lat90",
    "k8s.pod.cpu.usage": "cpu",
    "k8s.pod.memory.usage": "mem",
    "k8s.pod.memory.available": "avail_mem",
}


class SimpleMetricsAdapter:
    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        if not (
            args.dataset == "rcaeval_re2_tt"
            or is_rcabench_like_dataset(args.dataset, args.input_folder)
        ):
            raise NotImplementedError(f"unsupported dataset for simple metrics adapter: {args.dataset}")

        inject_time = load_inject_time(args.dataset, args.input_folder)
        df = preprocess(load_simple_metrics(args.dataset, args.input_folder))
        #df.to_csv(args.output_folder / "simple_metrics.csv", index=False)
        output = (self.func)(data=df, inject_time=inject_time, dataset="train-ticket")
        ranks: list[str] = output["ranks"]

        answers: list[AlgorithmAnswer] = []
        for rank, node_name in enumerate(ranks, start=1):
            service, metric = node_name.split("_", maxsplit=1)
            answers.append(AlgorithmAnswer(level="service", name=service, rank=rank))
            # answers.append(AlgorithmAnswer(level="metric", name=metric, rank=rank))

        if debug():
            rows = []
            for rank, node_name in enumerate(ranks, start=1):
                rows.append({"rank": rank, "node_name": node_name})
            df = pd.DataFrame(rows)
            save_parquet(df, path=args.output_folder / "ranks.parquet")

        return answers


def is_rcabench_like_dataset(dataset: str, input_folder: Path) -> bool:
    return dataset.startswith("rcabench") or (input_folder / "normal_metrics.parquet").exists()


def parse_utc_datetime(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def load_rcabench_like_inject_time(input_folder: Path) -> datetime:
    try:
        return rcabench_load_inject_time(input_folder)
    except (AssertionError, KeyError, FileNotFoundError, TypeError, ValueError):
        pass

    env_path = input_folder / "env.json"
    if env_path.exists():
        env = json.loads(env_path.read_text())
        if "abnormal_start_time" in env:
            return parse_utc_datetime(str(env["abnormal_start_time"]))

    injection_path = input_folder / "injection.json"
    if injection_path.exists():
        injection = json.loads(injection_path.read_text())
        if "start_time" in injection:
            return parse_utc_datetime(str(injection["start_time"]))

    raise KeyError(f"cannot infer injection time from {input_folder}")


@timeit()
def load_simple_metrics(dataset: str, input_folder: Path) -> pd.DataFrame:
    if dataset.startswith("rcaeval"):
        metrics = pl.scan_parquet(input_folder / "simple_metrics.parquet")

        df = convert_simple_metrics(metrics)
        return df.to_pandas()

    if is_rcabench_like_dataset(dataset, input_folder):
        normal_metrics = pl.scan_parquet(input_folder / "normal_metrics.parquet")
        abnormal_metrics = pl.scan_parquet(input_folder / "abnormal_metrics.parquet")
        metrics = pl.concat([normal_metrics, abnormal_metrics])

        metrics = metrics.with_columns(
            pl.coalesce(
                [
                    "attr.k8s.container.name",
                    "attr.k8s.deployment.name",
                    "attr.k8s.statefulset.name",
                ]
            ).alias("service_name")
        )

        metrics = metrics.select(
            pl.col("time"),
            pl.col("service_name"),
            pl.col("metric"),
            pl.col("value"),
        )

        # normal_metrics_histogram = pl.scan_parquet(input_folder / "normal_metrics_histogram.parquet")
        # abnormal_metrics_histogram = pl.scan_parquet(input_folder / "abnormal_metrics_histogram.parquet")
        # metrics_histogram = pl.concat([normal_metrics_histogram, abnormal_metrics_histogram])
        #
        # metrics_histogram = metrics_histogram.select(
        #    pl.col("time"),
        #    pl.col("service_name"),
        #    pl.col("metric"),
        #    pl.col("sum").alias("value"),  # `sum` as `value` (?)
        # )
        #
        # lf = pl.concat([metrics, metrics_histogram])
        lf = metrics
        df = convert_simple_metrics(lf)

        return df.to_pandas()

    raise NotImplementedError


def convert_simple_metrics(lf: pl.LazyFrame) -> pl.DataFrame:
    lf = lf.drop_nulls(subset=["service_name"])

    lf = lf.with_columns(pl.col("time").dt.timestamp(time_unit="ns"))
    # rename metric use RENAME_METRICS dict
    lf = lf.with_columns(
        pl.col("metric").replace(
            list(RENAME_METRICS.keys()),
            list(RENAME_METRICS.values()),
            default=pl.col("metric"),
        )
    )

    lf = lf.with_columns(
        pl.concat_str(pl.col("service_name"), pl.col("metric"), separator="_").alias(
            "metric"
        )
    )

    lf = lf.select("time", "metric", "value")

    df = lf.collect()

    df = df.pivot("metric", index="time", values="value", aggregate_function="mean")

    assert df.columns[0] == "time"
    df = df.select("time", *sorted(df.columns[1:]))

    df = (
        df.fill_nan(value=None)
        .fill_null(strategy="backward")
        .fill_null(strategy="forward")
    )

    return df


@timeit()
def load_inject_time(dataset: str, input_folder: Path) -> int:
    if dataset.startswith("rcaeval"):
        inject_time = rcaeval_load_inject_time(input_folder)
    elif is_rcabench_like_dataset(dataset, input_folder):
        inject_time = load_rcabench_like_inject_time(input_folder)
    else:
        raise NotImplementedError

    return int(inject_time.timestamp() * 1e9)
