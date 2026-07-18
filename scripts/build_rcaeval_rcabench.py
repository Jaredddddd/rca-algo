#!/usr/bin/env python3
"""Convert RCAEval V1 RE2 datasets into RCABench-platform v2 datapacks.

The source RCAEval cases contain one unsplit CSV per telemetry modality and an
``inject_time.txt`` file. The converter applies RCAEval main.py public metric
protocol, splits all modalities at injection time, and writes the RCABench v2
contract consumed by the repository algorithm entrypoints.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


_NATIVE_LIMIT_DEFAULTS = {
    "POLARS_MAX_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "MALLOC_ARENA_MAX": "2",
}
for _name, _value in _NATIVE_LIMIT_DEFAULTS.items():
    os.environ.setdefault(_name, _value)

import polars as pl  # noqa: E402
from rcabench_platform.v2.sources.rcaeval import (  # noqa: E402
    convert_logs,
    convert_traces,
)


DEFAULT_SOURCE_ROOT = Path("/home/ljw/paper/DDS-DL-AIOPS/RCAEval-V1-Data")
DEFAULT_DATA_ROOT = Path("data/rcabench-platform-v2")
DEFAULT_DATASET_PREFIX = "rcabench_rcaeval_re2"
CONVERSION_VERSION = 3
METRIC_PREPROCESSING = "rcaeval-main-length20-v1"
RCAEVAL_METRIC_WINDOW_ROWS = 20 * 60 // 2

SUBSET_DIRECTORIES = {
    "ob": Path("RE2-OB/RE2-OB"),
    "ss": Path("RE2-SS/RE2-SS"),
    "tt": Path("RE2-TT/RE2-TT"),
}

TRACE_SCHEMA: dict[str, pl.DataType] = {
    "time": pl.Datetime("ns", "UTC"),
    "trace_id": pl.String,
    "span_id": pl.String,
    "service_name": pl.String,
    "span_name": pl.String,
    "parent_span_id": pl.String,
    "duration": pl.UInt64,
    "attr.status_code": pl.String,
}

LOG_SCHEMA: dict[str, pl.DataType] = {
    "time": pl.Datetime("ns", "UTC"),
    "service_name": pl.String,
    "trace_id": pl.String,
    "span_id": pl.String,
    "message": pl.String,
    "level": pl.String,
    "attr.req_path": pl.String,
    "attr.cluster_id": pl.UInt8,
    "attr.log_template": pl.String,
    "attr.has_error": pl.Boolean,
    "attr.k8s.container.name": pl.String,
}

METRIC_SCHEMA: dict[str, pl.DataType] = {
    "time": pl.Datetime("ns", "UTC"),
    "metric": pl.String,
    "value": pl.Float64,
    "service_name": pl.String,
    "attr.k8s.container.name": pl.String,
    "attr.k8s.deployment.name": pl.String,
    "attr.k8s.statefulset.name": pl.String,
    "attr.k8s.pod.name": pl.String,
}

HISTOGRAM_SCHEMA: dict[str, pl.DataType] = {
    "time": pl.Datetime("ns", "UTC"),
    "metric": pl.String,
    "service_name": pl.String,
    "count": pl.Float64,
    "sum": pl.Float64,
    "min": pl.Float64,
    "max": pl.Float64,
}


CONCLUSION_SCHEMA: dict[str, pl.DataType] = {
    "SpanName": pl.String,
    "Issues": pl.String,
    "AbnormalAvgDuration": pl.Float64,
    "NormalAvgDuration": pl.Float64,
    "AbnormalSuccRate": pl.Float64,
    "NormalSuccRate": pl.Float64,
    "AbnormalP90": pl.Float64,
    "NormalP90": pl.Float64,
    "AbnormalP95": pl.Float64,
    "NormalP95": pl.Float64,
    "AbnormalP99": pl.Float64,
    "NormalP99": pl.Float64,
}


@dataclass(frozen=True)
class CaseRef:
    subset: str
    source: Path
    datapack: str
    service: str
    fault: str


@dataclass(frozen=True)
class CaseResult:
    subset: str
    dataset: str
    datapack: str
    service: str
    source: str
    inject_time: int
    rows: dict[str, int]
    skipped: bool = False


def safe_name(value: str) -> str:
    text = "".join(
        char.lower() if char.isalnum() or char in "-_" else "-"
        for char in value.strip()
    )
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-_") or "case"


def split_fault_directory(name: str) -> tuple[str, str]:
    if "_" not in name:
        raise ValueError(f"RCAEval fault directory must end in _<fault>: {name}")
    service, fault = name.rsplit("_", maxsplit=1)
    if not service or not fault:
        raise ValueError(f"Invalid RCAEval fault directory: {name}")
    return service, fault


def discover_cases(source_root: Path, subset: str) -> list[CaseRef]:
    subset_root = source_root / SUBSET_DIRECTORIES[subset]
    if not subset_root.is_dir():
        raise FileNotFoundError(f"RCAEval subset directory not found: {subset_root}")

    cases: list[CaseRef] = []
    for fault_dir in sorted(path for path in subset_root.iterdir() if path.is_dir()):
        try:
            service, fault = split_fault_directory(fault_dir.name)
        except ValueError:
            continue
        for run_dir in sorted(
            (
                path
                for path in fault_dir.iterdir()
                if path.is_dir() and path.name.isdigit()
            ),
            key=lambda path: int(path.name),
        ):
            required = (run_dir / "simple_metrics.csv", run_dir / "inject_time.txt")
            if not all(path.is_file() for path in required):
                continue
            datapack = safe_name(f"{fault_dir.name}_{run_dir.name}")
            cases.append(
                CaseRef(
                    subset=subset,
                    source=run_dir,
                    datapack=datapack,
                    service=service,
                    fault=fault,
                )
            )
    if not cases:
        raise RuntimeError(f"No RCAEval cases found under {subset_root}")
    return cases


def _normalise_metrics(path: Path, inject_time: int) -> pl.LazyFrame:
    """Apply RCAEval main.py metric protocol and emit RCABench long rows."""

    raw = pl.scan_csv(path, infer_schema_length=50000)
    source_columns = [
        column
        for column in raw.collect_schema().names()
        if column != "time" and not column.endswith("_latency-50")
    ]
    renamed_columns = {
        column: column[:-3] if column.endswith("latency-90") else column
        for column in source_columns
    }
    metric_columns = list(renamed_columns.values())
    if len(set(metric_columns)) != len(metric_columns):
        raise ValueError(f"Metric rename collision in {path}")

    filled = raw.select(
        pl.col("time")
        .cast(pl.Float64, strict=False)
        .fill_nan(None)
        .forward_fill()
        .fill_null(0.0)
        .alias("time"),
        *(
            pl.col(source)
            .cast(pl.Float64, strict=False)
            .fill_nan(None)
            .replace([float("inf"), float("-inf")], None)
            .forward_fill()
            .fill_null(0.0)
            .alias(target)
            for source, target in renamed_columns.items()
        ),
    ).with_columns(
        pl.from_epoch(pl.col("time").cast(pl.Int64), time_unit="s")
        .dt.replace_time_zone("UTC")
        .alias("time")
    )
    inject_at = datetime.fromtimestamp(inject_time, tz=UTC)
    windowed = pl.concat(
        [
            filled.filter(pl.col("time") < inject_at).tail(RCAEVAL_METRIC_WINDOW_ROWS),
            filled.filter(pl.col("time") >= inject_at).head(RCAEVAL_METRIC_WINDOW_ROWS),
        ]
    )
    metrics = (
        windowed.unpivot(
            on=metric_columns,
            index="time",
            variable_name="metric",
            value_name="value",
        )
        .with_columns(pl.col("metric").str.split("_").alias("_split"))
        .with_columns(
            pl.col("_split").list.get(0).alias("service_name"),
            pl.col("_split").list.get(1).alias("metric"),
        )
        .drop("_split")
    )
    return (
        metrics.with_columns(
            pl.col("time").dt.cast_time_unit("ns"),
            pl.col("metric").cast(pl.String),
            pl.col("value").cast(pl.Float64, strict=False),
            pl.col("service_name").cast(pl.String),
        )
        .with_columns(
            pl.col("service_name").alias("attr.k8s.container.name"),
            pl.lit(None).cast(pl.String).alias("attr.k8s.deployment.name"),
            pl.lit(None).cast(pl.String).alias("attr.k8s.statefulset.name"),
            pl.col("service_name").alias("attr.k8s.pod.name"),
        )
        .select(*METRIC_SCHEMA)
    )


def _normalise_traces(path: Path) -> pl.LazyFrame:
    status = pl.col("attr.status_code").cast(pl.String).str.strip_chars()
    numeric_status = status.cast(pl.Float64, strict=False)
    normalized_status = status.str.to_lowercase()
    return (
        convert_traces(path)
        .with_columns(
            pl.col("time").dt.cast_time_unit("ns"),
            pl.when(status.is_null() | (status == ""))
            .then(pl.lit("Unset"))
            .when(normalized_status == "unset")
            .then(pl.lit("Unset"))
            .when((normalized_status == "ok") | (numeric_status == 0.0))
            .then(pl.lit("Ok"))
            .when((normalized_status == "error") | numeric_status.is_not_null())
            .then(pl.lit("Error"))
            .otherwise(status)
            .alias("attr.status_code"),
        )
        .select(*TRACE_SCHEMA)
    )


def _normalise_logs(path: Path) -> pl.LazyFrame:
    logs = convert_logs(path)
    schema = logs.collect_schema()
    for column, dtype in LOG_SCHEMA.items():
        if column not in schema:
            logs = logs.with_columns(pl.lit(None).cast(dtype).alias(column))
    return logs.with_columns(
        pl.col("time").dt.cast_time_unit("ns"),
        pl.col("level")
        .cast(pl.String)
        .fill_null("")
        .str.to_uppercase()
        .str.replace("WARNING", "WARN", literal=True),
        pl.col("service_name").alias("attr.k8s.container.name"),
    ).select(*LOG_SCHEMA)


def _empty_frame(schema: dict[str, pl.DataType]) -> pl.DataFrame:
    return pl.DataFrame(schema=schema)


def _trace_stats(path: Path, prefix: str) -> pl.LazyFrame:
    return (
        pl.scan_parquet(path)
        .with_columns(
            (pl.col("duration").cast(pl.Float64) / 1_000_000_000.0).alias(
                "_duration_s"
            ),
            (pl.col("attr.status_code") != "Error").cast(pl.Float64).alias("_success"),
        )
        .group_by("span_name")
        .agg(
            pl.col("_duration_s").mean().alias(f"{prefix}AvgDuration"),
            pl.col("_success").mean().alias(f"{prefix}SuccRate"),
            pl.col("_duration_s").quantile(0.90).alias(f"{prefix}P90"),
            pl.col("_duration_s").quantile(0.95).alias(f"{prefix}P95"),
            pl.col("_duration_s").quantile(0.99).alias(f"{prefix}P99"),
        )
        .rename({"span_name": "SpanName"})
    )


def _issue_json(row: dict[str, Any]) -> str:
    issues: dict[str, dict[str, float | bool]] = {}
    normal_p90 = float(row.get("NormalP90") or 0.0)
    abnormal_p90 = float(row.get("AbnormalP90") or 0.0)
    normal_success = float(row.get("NormalSuccRate") or 1.0)
    abnormal_success = float(row.get("AbnormalSuccRate") or 1.0)
    if normal_p90 > 0.0 and abnormal_p90 > normal_p90 * 2.0:
        issues["latency"] = {
            "change_rate": abnormal_p90 / normal_p90,
            "slo_violated": True,
        }
    if normal_success - abnormal_success > 0.2:
        issues["success_rate"] = {
            "change_rate": normal_success - abnormal_success,
            "slo_violated": True,
        }
    return json.dumps(issues, sort_keys=True)


def _build_conclusion(normal_path: Path, abnormal_path: Path) -> pl.DataFrame:
    stats = (
        _trace_stats(abnormal_path, "Abnormal")
        .join(
            _trace_stats(normal_path, "Normal"),
            on="SpanName",
            how="full",
            coalesce=True,
        )
        .fill_null(0.0)
        .collect(engine="streaming")
    )
    if stats.is_empty():
        return _empty_frame(CONCLUSION_SCHEMA)
    return (
        stats.with_columns(
            pl.struct(stats.columns)
            .map_elements(_issue_json, return_dtype=pl.String)
            .alias("Issues")
        )
        .select(*CONCLUSION_SCHEMA)
        .sort("SpanName")
    )


def _write_parquet(frame: pl.LazyFrame | pl.DataFrame, path: Path) -> int:
    if isinstance(frame, pl.LazyFrame):
        frame.sink_parquet(path, compression="zstd")
    else:
        frame.write_parquet(path, compression="zstd")
    return int(pl.scan_parquet(path).select(pl.len()).collect().item())


def _write_split(
    frame: pl.LazyFrame,
    inject_at: datetime,
    normal_path: Path,
    abnormal_path: Path,
) -> tuple[int, int]:
    normal_rows = _write_parquet(frame.filter(pl.col("time") < inject_at), normal_path)
    abnormal_rows = _write_parquet(
        frame.filter(pl.col("time") >= inject_at), abnormal_path
    )
    return normal_rows, abnormal_rows


def _metric_time_bounds(path: Path, inject_time: int) -> tuple[int, int]:
    bounds = (
        pl.scan_csv(path, infer_schema_length=50000)
        .select(
            pl.col("time").cast(pl.Int64, strict=False).min().alias("start"),
            pl.col("time").cast(pl.Int64, strict=False).max().alias("end"),
        )
        .collect()
        .row(0, named=True)
    )
    start = int(bounds["start"] or inject_time - 1)
    end = int(bounds["end"] or inject_time + 1)
    return min(start, inject_time - 1), max(end, inject_time + 1)


def _iso_utc(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=UTC).isoformat().replace("+00:00", "Z")


def _write_case_metadata(
    case: CaseRef, folder: Path, inject_time: int, start: int, end: int
) -> None:
    env = {
        "NORMAL_START": start,
        "NORMAL_END": inject_time,
        "ABNORMAL_START": inject_time,
        "ABNORMAL_END": end,
        "abnormal_start_time": _iso_utc(inject_time),
    }
    injection = {
        "start_time": _iso_utc(inject_time),
        "end_time": _iso_utc(end),
        "fault_type": case.fault,
        "ground_truth": {"service": [case.service]},
        "source_dataset": f"RE2-{case.subset.upper()}",
    }
    (folder / "env.json").write_text(json.dumps(env, indent=2) + "\n", encoding="utf-8")
    (folder / "injection.json").write_text(
        json.dumps(injection, indent=2) + "\n",
        encoding="utf-8",
    )


def _required_outputs(folder: Path) -> tuple[Path, ...]:
    names = (
        "normal_metrics.parquet",
        "abnormal_metrics.parquet",
        "normal_metrics_sum.parquet",
        "abnormal_metrics_sum.parquet",
        "normal_metrics_histogram.parquet",
        "abnormal_metrics_histogram.parquet",
        "normal_traces.parquet",
        "abnormal_traces.parquet",
        "normal_logs.parquet",
        "abnormal_logs.parquet",
        "conclusion.parquet",
        "env.json",
        "injection.json",
        "conversion.json",
        ".finished",
    )
    return tuple(folder / name for name in names)


def convert_case(
    case: CaseRef,
    data_root: Path,
    dataset_prefix: str,
    overwrite: bool,
) -> CaseResult:
    dataset = f"{dataset_prefix}_{case.subset}"
    destination = data_root / "data" / dataset / case.datapack
    if not overwrite and all(path.exists() for path in _required_outputs(destination)):
        payload = json.loads(
            (destination / "conversion.json").read_text(encoding="utf-8")
        )
        if payload.get("conversion_version") == CONVERSION_VERSION:
            return CaseResult(
                subset=case.subset,
                dataset=dataset,
                datapack=case.datapack,
                service=case.service,
                source=str(case.source),
                inject_time=int(payload["inject_time"]),
                rows={str(key): int(value) for key, value in payload["rows"].items()},
                skipped=True,
            )

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.parent / f".{destination.name}.tmp-{os.getpid()}"
    if temporary.exists():
        shutil.rmtree(temporary)
    temporary.mkdir(parents=True)

    try:
        inject_time = int(
            (case.source / "inject_time.txt").read_text(encoding="utf-8").strip()
        )
        inject_at = datetime.fromtimestamp(inject_time, tz=UTC)
        start, end = _metric_time_bounds(
            case.source / "simple_metrics.csv", inject_time
        )
        rows: dict[str, int] = {}

        metrics = _normalise_metrics(case.source / "simple_metrics.csv", inject_time)
        normal_count, abnormal_count = _write_split(
            metrics,
            inject_at,
            temporary / "normal_metrics.parquet",
            temporary / "abnormal_metrics.parquet",
        )
        rows["normal_metrics"] = normal_count
        rows["abnormal_metrics"] = abnormal_count

        # RCAEval V1 has gauges only.  Keep sum/histogram files schema-valid and
        # empty so consumers do not double-count the same source metrics.
        rows["normal_metrics_sum"] = _write_parquet(
            _empty_frame(METRIC_SCHEMA), temporary / "normal_metrics_sum.parquet"
        )
        rows["abnormal_metrics_sum"] = _write_parquet(
            _empty_frame(METRIC_SCHEMA), temporary / "abnormal_metrics_sum.parquet"
        )
        rows["normal_metrics_histogram"] = _write_parquet(
            _empty_frame(HISTOGRAM_SCHEMA),
            temporary / "normal_metrics_histogram.parquet",
        )
        rows["abnormal_metrics_histogram"] = _write_parquet(
            _empty_frame(HISTOGRAM_SCHEMA),
            temporary / "abnormal_metrics_histogram.parquet",
        )

        trace_path = case.source / "traces.csv"
        if trace_path.is_file():
            normal_count, abnormal_count = _write_split(
                _normalise_traces(trace_path),
                inject_at,
                temporary / "normal_traces.parquet",
                temporary / "abnormal_traces.parquet",
            )
        else:
            normal_count = _write_parquet(
                _empty_frame(TRACE_SCHEMA), temporary / "normal_traces.parquet"
            )
            abnormal_count = _write_parquet(
                _empty_frame(TRACE_SCHEMA), temporary / "abnormal_traces.parquet"
            )
        rows["normal_traces"] = normal_count
        rows["abnormal_traces"] = abnormal_count

        rows["conclusion"] = _write_parquet(
            _build_conclusion(
                temporary / "normal_traces.parquet",
                temporary / "abnormal_traces.parquet",
            ),
            temporary / "conclusion.parquet",
        )

        log_path = case.source / "logs.csv"
        if log_path.is_file():
            normal_count, abnormal_count = _write_split(
                _normalise_logs(log_path),
                inject_at,
                temporary / "normal_logs.parquet",
                temporary / "abnormal_logs.parquet",
            )
        else:
            normal_count = _write_parquet(
                _empty_frame(LOG_SCHEMA), temporary / "normal_logs.parquet"
            )
            abnormal_count = _write_parquet(
                _empty_frame(LOG_SCHEMA), temporary / "abnormal_logs.parquet"
            )
        rows["normal_logs"] = normal_count
        rows["abnormal_logs"] = abnormal_count

        _write_case_metadata(case, temporary, inject_time, start, end)
        conversion = {
            "conversion_version": CONVERSION_VERSION,
            "metric_preprocessing": METRIC_PREPROCESSING,
            "metric_window_rows_per_phase": RCAEVAL_METRIC_WINDOW_ROWS,
            "trace_status_mapping": "grpc-zero-ok-nonzero-error-v1",
            "source": str(case.source),
            "source_dataset": f"RE2-{case.subset.upper()}",
            "dataset": dataset,
            "datapack": case.datapack,
            "inject_time": inject_time,
            "split_rule": "normal: time < inject_time; abnormal: time >= inject_time",
            "rows": rows,
        }
        (temporary / "conversion.json").write_text(
            json.dumps(conversion, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (temporary / ".finished").touch()

        if destination.exists() or destination.is_symlink():
            if destination.is_symlink() or destination.is_file():
                destination.unlink()
            else:
                shutil.rmtree(destination)
        temporary.replace(destination)
        return CaseResult(
            subset=case.subset,
            dataset=dataset,
            datapack=case.datapack,
            service=case.service,
            source=str(case.source),
            inject_time=inject_time,
            rows=rows,
        )
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def _convert_case_task(args: tuple[CaseRef, Path, str, bool]) -> CaseResult:
    return convert_case(*args)


def _write_meta(data_root: Path, dataset: str, results: Iterable[CaseResult]) -> None:
    ordered = sorted(results, key=lambda result: result.datapack)
    index = pl.DataFrame(
        {
            "dataset": [dataset] * len(ordered),
            "datapack": [result.datapack for result in ordered],
        },
        schema={"dataset": pl.String, "datapack": pl.String},
    )
    labels = pl.DataFrame(
        {
            "dataset": [dataset] * len(ordered),
            "datapack": [result.datapack for result in ordered],
            "gt.level": ["service"] * len(ordered),
            "gt.name": [result.service for result in ordered],
        },
        schema={
            "dataset": pl.String,
            "datapack": pl.String,
            "gt.level": pl.String,
            "gt.name": pl.String,
        },
    )
    meta = data_root / "meta" / dataset
    meta.mkdir(parents=True, exist_ok=True)
    index.write_parquet(meta / "index.parquet")
    labels.write_parquet(meta / "labels.parquet")


def _load_completed_results(
    data_root: Path,
    dataset_prefix: str,
    subset: str,
) -> list[CaseResult]:
    dataset = f"{dataset_prefix}_{subset}"
    dataset_root = data_root / "data" / dataset
    if not dataset_root.is_dir():
        return []

    results: list[CaseResult] = []
    for folder in sorted(path for path in dataset_root.iterdir() if path.is_dir()):
        if not all(path.exists() for path in _required_outputs(folder)):
            continue
        conversion = json.loads(
            (folder / "conversion.json").read_text(encoding="utf-8")
        )
        injection = json.loads((folder / "injection.json").read_text(encoding="utf-8"))
        services = injection.get("ground_truth", {}).get("service", [])
        if not services:
            raise ValueError(
                f"Missing service ground truth in {folder / 'injection.json'}"
            )
        results.append(
            CaseResult(
                subset=subset,
                dataset=dataset,
                datapack=folder.name,
                service=str(services[0]),
                source=str(conversion["source"]),
                inject_time=int(conversion["inject_time"]),
                rows={
                    str(key): int(value) for key, value in conversion["rows"].items()
                },
                skipped=True,
            )
        )
    return results


def _replace_symlink(link: Path, target: Path) -> None:
    if link.is_symlink() or link.is_file():
        link.unlink()
    elif link.exists():
        shutil.rmtree(link)
    link.symlink_to(target, target_is_directory=True)


def build_combined_dataset(
    data_root: Path,
    dataset_prefix: str,
    results_by_subset: dict[str, list[CaseResult]],
) -> list[CaseResult]:
    dataset = dataset_prefix
    combined_root = data_root / "data" / dataset
    combined_root.mkdir(parents=True, exist_ok=True)
    combined: list[CaseResult] = []
    expected_names: set[str] = set()

    for subset, results in sorted(results_by_subset.items()):
        source_dataset = f"{dataset_prefix}_{subset}"
        for result in results:
            datapack = f"re2-{subset}__{result.datapack}"
            expected_names.add(datapack)
            link = combined_root / datapack
            target = Path("..") / source_dataset / result.datapack
            _replace_symlink(link, target)
            combined.append(
                CaseResult(
                    subset=subset,
                    dataset=dataset,
                    datapack=datapack,
                    service=result.service,
                    source=result.source,
                    inject_time=result.inject_time,
                    rows=result.rows,
                    skipped=result.skipped,
                )
            )

    for path in combined_root.iterdir():
        if path.name not in expected_names and path.is_symlink():
            path.unlink()
    _write_meta(data_root, dataset, combined)
    return combined


def convert_datasets(
    source_root: Path,
    data_root: Path,
    subsets: list[str],
    dataset_prefix: str,
    workers: int,
    overwrite: bool,
    limit: int | None = None,
) -> dict[str, list[CaseResult]]:
    recent_by_subset: dict[str, list[CaseResult]] = {}
    for subset in subsets:
        cases = discover_cases(source_root, subset)
        if limit is not None:
            cases = cases[:limit]
        tasks = [(case, data_root, dataset_prefix, overwrite) for case in cases]
        if workers == 1:
            results = [_convert_case_task(task) for task in tasks]
        else:
            # Polars owns native worker threads. Spawn avoids fork-after-threads deadlocks.
            with ProcessPoolExecutor(
                max_workers=workers,
                mp_context=mp.get_context("spawn"),
            ) as executor:
                results = list(executor.map(_convert_case_task, tasks))
        recent_by_subset[subset] = results

    # Rebuild metadata from every completed datapack on disk. This keeps
    # --subset and --limit incremental runs from truncating existing datasets.
    results_by_subset: dict[str, list[CaseResult]] = {}
    for subset in SUBSET_DIRECTORIES:
        completed = _load_completed_results(data_root, dataset_prefix, subset)
        if not completed:
            continue
        recent = {
            result.datapack: result for result in recent_by_subset.get(subset, [])
        }
        merged = [recent.get(result.datapack, result) for result in completed]
        dataset = f"{dataset_prefix}_{subset}"
        _write_meta(data_root, dataset, merged)
        results_by_subset[subset] = merged

    build_combined_dataset(data_root, dataset_prefix, results_by_subset)
    return results_by_subset


def _summary(
    results_by_subset: dict[str, list[CaseResult]], dataset_prefix: str
) -> dict[str, object]:
    subsets: dict[str, object] = {}
    total = 0
    for subset, results in sorted(results_by_subset.items()):
        total += len(results)
        subsets[subset] = {
            "dataset": f"{dataset_prefix}_{subset}",
            "datapacks": len(results),
            "skipped": sum(result.skipped for result in results),
        }
    return {
        "combined_dataset": dataset_prefix,
        "total_datapacks": total,
        "subsets": subsets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--dataset-prefix", default=DEFAULT_DATASET_PREFIX)
    parser.add_argument(
        "--subset",
        action="append",
        choices=tuple(SUBSET_DIRECTORIES),
        help="Convert one subset; repeat for multiple. Defaults to ob, ss, tt.",
    )
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--limit",
        type=int,
        help="Convert at most N cases per selected subset (smoke tests).",
    )
    args = parser.parse_args()

    if args.workers < 1:
        parser.error("--workers must be >= 1")
    if args.workers > 1:
        print(
            f"warning: {args.workers} workers may exhaust memory on RCAEval traces; 1 is the tested safe value",
            file=sys.stderr,
        )
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be >= 1")
    dataset_prefix = safe_name(args.dataset_prefix)
    subsets = list(dict.fromkeys(args.subset or SUBSET_DIRECTORIES))
    results = convert_datasets(
        source_root=args.source_root.resolve(),
        data_root=args.data_root.resolve(),
        subsets=subsets,
        dataset_prefix=dataset_prefix,
        workers=args.workers,
        overwrite=args.overwrite,
        limit=args.limit,
    )
    print(json.dumps(_summary(results, dataset_prefix), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
