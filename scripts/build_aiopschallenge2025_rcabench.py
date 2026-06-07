#!/usr/bin/env python3
"""Convert AIOpsChallenge2025 into rcabench-platform v2 datapacks.

The source dataset names daily folders and hourly files by UTC+8 clock time,
while timestamps inside groundtruth.jsonl and parquet rows are UTC.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
from collections.abc import Iterable
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

import polars as pl
from tqdm.auto import tqdm


UTC = timezone.utc
LOCAL_OFFSET = timedelta(hours=8)

DEFAULT_SRC = Path("/home/ljw/paper/aiops-challenge-data/aiopschallenge2025")
DEFAULT_DATA_ROOT = Path("data") / "rcabench-platform-v2"
DEFAULT_DATASET = "aiopschallenge2025_rcabench_service"


TRACE_SCHEMA: dict[str, pl.DataType] = {
    "time": pl.Datetime("ns", "UTC"),
    "trace_id": pl.String,
    "span_id": pl.String,
    "parent_span_id": pl.String,
    "span_name": pl.String,
    "attr.span_kind": pl.String,
    "service_name": pl.String,
    "duration": pl.UInt64,
    "attr.status_code": pl.String,
    "attr.k8s.pod.name": pl.String,
    "attr.k8s.service.name": pl.String,
    "attr.k8s.namespace.name": pl.String,
    "attr.k8s.node.name": pl.String,
}

LOG_SCHEMA: dict[str, pl.DataType] = {
    "time": pl.Datetime("ns", "UTC"),
    "trace_id": pl.String,
    "span_id": pl.String,
    "level": pl.String,
    "service_name": pl.String,
    "message": pl.String,
    "attr.k8s.pod.name": pl.String,
    "attr.k8s.service.name": pl.String,
    "attr.k8s.namespace.name": pl.String,
    "attr.k8s.node.name": pl.String,
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
    "attr.k8s.service.name": pl.String,
    "attr.k8s.namespace.name": pl.String,
    "attr.k8s.node.name": pl.String,
    "attr.aiops.object_id": pl.String,
    "attr.aiops.object_type": pl.String,
    "attr.aiops.instance": pl.String,
    "attr.aiops.metric_group": pl.String,
    "attr.aiops.metric_file": pl.String,
}

HISTOGRAM_SCHEMA: dict[str, pl.DataType] = {
    "time": pl.Datetime("ns", "UTC"),
    "metric": pl.String,
    "service_name": pl.String,
    "count": pl.Float64,
    "sum": pl.Float64,
    "min": pl.Float64,
    "max": pl.Float64,
    "attr.k8s.pod.name": pl.String,
    "attr.k8s.service.name": pl.String,
    "attr.k8s.namespace.name": pl.String,
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

METRIC_METADATA_COLUMNS = [
    "object_id",
    "object_type",
    "instance",
    "pod",
    "kubernetes_node",
    "namespace",
    "device",
    "mountpoint",
    "cf",
    "sql_type",
    "type",
    "kpi_key",
    "kpi_name",
]


def empty_frame(schema: dict[str, pl.DataType]) -> pl.DataFrame:
    return pl.DataFrame(schema=schema)


def parse_utc(value: str) -> datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def floor_hour(dt: datetime) -> datetime:
    return dt.replace(minute=0, second=0, microsecond=0)


def iter_utc_hours(start: datetime, end: datetime) -> Iterable[datetime]:
    current = floor_hour(start)
    while current <= end:
        yield current
        current += timedelta(hours=1)


def iter_local_dates(start: datetime, end: datetime) -> Iterable[str]:
    current = (start + LOCAL_OFFSET).date()
    last = (end + LOCAL_OFFSET).date()
    while current <= last:
        yield current.isoformat()
        current += timedelta(days=1)


def local_date_hour(utc_hour: datetime) -> tuple[str, str]:
    local = utc_hour + LOCAL_OFFSET
    return local.strftime("%Y-%m-%d"), local.strftime("%H")


def safe_name(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9_-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-_")
    return value or "case"


def clean_deleted_suffix(value: str) -> str:
    return re.sub(r"\s+\(deleted\)\s*$", "", value.strip())


def service_from_pod(value: Any) -> str:
    text = clean_deleted_suffix(str(value or ""))
    if not text:
        return ""
    hash_match = re.match(r"^(.+)-[0-9a-f]{8,10}-[a-z0-9]{5}$", text)
    if hash_match:
        return hash_match.group(1)
    ordinal_match = re.match(r"^(.+)-\d+$", text)
    if ordinal_match:
        return ordinal_match.group(1)
    return text


def as_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)]


def service_labels(row: dict[str, Any]) -> list[str]:
    labels: list[str] = []
    source = str(row.get("source") or "")
    destination = str(row.get("destination") or "")
    service = str(row.get("service") or "")

    if source and destination:
        labels.extend([source, destination])
    elif service:
        labels.append(service)
    else:
        for item in as_list(row.get("instance")):
            labels.append(service_from_pod(item) if row.get("instance_type") == "pod" else item)

    return sorted({label for label in labels if label})


def case_windows(row: dict[str, Any], min_window: timedelta) -> tuple[datetime, datetime, datetime, datetime]:
    start = parse_utc(str(row["start_time"]))
    end = parse_utc(str(row["end_time"]))
    duration = max(end - start, timedelta(seconds=1))
    window = max(duration, min_window)
    normal_start = start - window
    normal_end = start
    abnormal_start = start
    abnormal_end = start + window
    return normal_start, normal_end, abnormal_start, abnormal_end


def get_tag(tags: Any, key: str) -> str | None:
    if tags is None:
        return None
    if isinstance(tags, pl.Series):
        tags = tags.to_list()
    if not tags:
        return None
    for item in tags:
        try:
            if item.get("key") == key:
                value = item.get("value")
                return None if value is None else str(value)
        except AttributeError:
            continue
    return None


def parent_span_id(refs: Any) -> str:
    if refs is None:
        return ""
    if isinstance(refs, pl.Series):
        refs = refs.to_list()
    if not refs:
        return ""
    for ref in refs:
        try:
            if ref.get("refType") == "CHILD_OF":
                return str(ref.get("spanID") or "")
        except AttributeError:
            continue
    try:
        return str(refs[0].get("spanID") or "")
    except Exception:
        return ""


def normalize_status(tags: Any) -> str:
    code = (get_tag(tags, "status.code") or "").strip()
    message = (get_tag(tags, "status.message") or "").strip()
    if code.lower() in {"error", "2"}:
        return "Error"
    if message and message.lower() not in {"ok", "unset"}:
        return "Error"
    return "Ok"


def log_level(message: Any) -> str:
    text = str(message or "")
    match = re.search(r"\b(FATAL|ERROR|ERR|WARN|WARNING|DEBUG|TRACE|INFO)\b", text, re.IGNORECASE)
    if not match:
        return "INFO"
    level = match.group(1).upper()
    if level == "ERR":
        return "ERROR"
    if level == "WARNING":
        return "WARN"
    return level


def metric_service_name(row: dict[str, Any]) -> str:
    object_id = str(row.get("object_id") or "")
    object_type = str(row.get("object_type") or "")
    pod = str(row.get("pod") or "")
    instance = str(row.get("instance") or "")
    metric_file = str(row.get("_metric_file") or "")

    if object_id:
        if object_type == "pod" or "/pod/" in metric_file or re.search(r"-\d+(?:\s+\(deleted\))?$", object_id):
            return service_from_pod(object_id)
        return object_id
    if pod:
        return service_from_pod(pod)
    if instance:
        return clean_deleted_suffix(instance)
    if object_type:
        return object_type
    return "unknown"


def metric_pod_name(row: dict[str, Any]) -> str:
    pod = str(row.get("pod") or "")
    object_id = str(row.get("object_id") or "")
    object_type = str(row.get("object_type") or "")
    metric_file = str(row.get("_metric_file") or "")
    if pod:
        return clean_deleted_suffix(pod)
    if object_id and (object_type == "pod" or "/pod/" in metric_file):
        return clean_deleted_suffix(object_id)
    return ""


def filter_window(df: pl.DataFrame, start: datetime, end: datetime, schema: dict[str, pl.DataType]) -> pl.DataFrame:
    if df.is_empty():
        return empty_frame(schema)
    out = df.filter((pl.col("time") >= start) & (pl.col("time") <= end))
    if out.is_empty():
        return empty_frame(schema)
    return out


def concat_or_empty(frames: list[pl.DataFrame], schema: dict[str, pl.DataType]) -> pl.DataFrame:
    frames = [frame for frame in frames if not frame.is_empty()]
    if not frames:
        return empty_frame(schema)
    return pl.concat(frames, how="diagonal_relaxed").select(list(schema))


def transform_trace(df: pl.DataFrame) -> pl.DataFrame:
    if df.is_empty():
        return empty_frame(TRACE_SCHEMA)

    out = df.with_columns(
        pl.from_epoch(pl.col("startTimeMillis"), time_unit="ms")
        .dt.replace_time_zone("UTC")
        .dt.cast_time_unit("ns")
        .alias("time"),
        pl.col("traceID").cast(pl.String).alias("trace_id"),
        pl.col("spanID").cast(pl.String).alias("span_id"),
        pl.col("references").list.first().struct.field("spanID").cast(pl.String).alias("parent_span_id"),
        pl.col("operationName").cast(pl.String).alias("span_name"),
        pl.col("process").struct.field("serviceName").cast(pl.String).alias("service_name"),
        (
            pl.when(pl.col("duration") > 0)
            .then(pl.col("duration"))
            .otherwise(0)
            .cast(pl.UInt64)
            * pl.lit(1000, dtype=pl.UInt64)
        ).alias("duration"),
        pl.lit("").cast(pl.String).alias("attr.span_kind"),
        pl.lit("Ok").cast(pl.String).alias("attr.status_code"),
        pl.lit("").cast(pl.String).alias("attr.k8s.pod.name"),
        pl.lit("").cast(pl.String).alias("attr.k8s.namespace.name"),
        pl.lit("").cast(pl.String).alias("attr.k8s.node.name"),
    ).with_columns(
        pl.col("service_name").alias("attr.k8s.service.name"),
        pl.col("parent_span_id").fill_null(""),
    )

    return out.select(list(TRACE_SCHEMA)).sort("time")


@lru_cache(maxsize=16)
def load_trace_hour(src: str, local_date: str, local_hour: str) -> pl.DataFrame:
    root = Path(src)
    path = root / local_date / "trace-parquet" / f"trace_jaeger-span_{local_date}_{local_hour}-00-00.parquet"
    if not path.exists():
        return empty_frame(TRACE_SCHEMA)
    return transform_trace(pl.read_parquet(path))


def load_traces(src: Path, start: datetime, end: datetime) -> pl.DataFrame:
    frames: list[pl.DataFrame] = []
    for hour in iter_utc_hours(start, end):
        local_date, local_hour = local_date_hour(hour)
        frames.append(load_trace_hour(str(src), local_date, local_hour))
    return filter_window(concat_or_empty(frames, TRACE_SCHEMA), start, end, TRACE_SCHEMA)


def transform_log(df: pl.DataFrame) -> pl.DataFrame:
    if df.is_empty():
        return empty_frame(LOG_SCHEMA)

    pod_clean = pl.col("k8_pod").cast(pl.String).str.replace(r"\s+\(deleted\)\s*$", "")
    service_expr = pod_clean.str.replace(r"-[0-9a-f]{8,10}-[a-z0-9]{5}$", "").str.replace(r"-\d+$", "")
    out = df.with_columns(
        pl.col("@timestamp")
        .str.strptime(pl.Datetime("ns", "UTC"), "%Y-%m-%dT%H:%M:%S%.fZ", strict=False)
        .alias("time"),
        pl.lit("").cast(pl.String).alias("trace_id"),
        pl.lit("").cast(pl.String).alias("span_id"),
        pl.lit("INFO").cast(pl.String).alias("level"),
        service_expr.alias("service_name"),
        pl.col("message").cast(pl.String).alias("message"),
        pod_clean.alias("attr.k8s.pod.name"),
        pl.col("k8_namespace").cast(pl.String).alias("attr.k8s.namespace.name"),
        pl.col("k8_node_name").cast(pl.String).alias("attr.k8s.node.name"),
    ).with_columns(
        pl.col("service_name").alias("attr.k8s.service.name"),
    )

    return out.select(list(LOG_SCHEMA)).sort("time")


@lru_cache(maxsize=16)
def load_log_hour(src: str, local_date: str, local_hour: str) -> pl.DataFrame:
    root = Path(src)
    path = root / local_date / "log-parquet" / f"log_filebeat-server_{local_date}_{local_hour}-00-00.parquet"
    if not path.exists():
        return empty_frame(LOG_SCHEMA)
    return transform_log(pl.read_parquet(path))


def load_logs(src: Path, start: datetime, end: datetime) -> pl.DataFrame:
    frames: list[pl.DataFrame] = []
    for hour in iter_utc_hours(start, end):
        local_date, local_hour = local_date_hour(hour)
        frames.append(load_log_hour(str(src), local_date, local_hour))
    return filter_window(concat_or_empty(frames, LOG_SCHEMA), start, end, LOG_SCHEMA)


def is_numeric_dtype(dtype: pl.DataType) -> bool:
    try:
        return bool(dtype.is_numeric())
    except AttributeError:
        return dtype in {
            pl.Int8,
            pl.Int16,
            pl.Int32,
            pl.Int64,
            pl.UInt8,
            pl.UInt16,
            pl.UInt32,
            pl.UInt64,
            pl.Float32,
            pl.Float64,
        }


def utc_second_string(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def transform_metric_file(
    path: Path,
    metric_group: str,
    start: datetime | None = None,
    end: datetime | None = None,
) -> pl.DataFrame:
    lf = pl.scan_parquet(path)
    if start is not None and end is not None:
        lf = lf.filter(
            pl.col("time") >= utc_second_string(start),
            pl.col("time") <= utc_second_string(end),
        )
    df = lf.collect()
    if df.is_empty() or "time" not in df.columns:
        return empty_frame(METRIC_SCHEMA)

    value_columns = [
        name
        for name, dtype in df.schema.items()
        if name != "time" and name not in METRIC_METADATA_COLUMNS and is_numeric_dtype(dtype)
    ]
    if not value_columns:
        return empty_frame(METRIC_SCHEMA)

    for column in METRIC_METADATA_COLUMNS:
        if column not in df.columns:
            df = df.with_columns(pl.lit(None).cast(pl.String).alias(column))

    df = df.with_columns(
        pl.col("time")
        .str.strptime(pl.Datetime("ns", "UTC"), "%Y-%m-%dT%H:%M:%SZ", strict=False)
        .alias("time"),
        pl.lit(metric_group).cast(pl.String).alias("_metric_group"),
        pl.lit(str(path.name)).cast(pl.String).alias("_metric_file"),
    )

    index_columns = ["time", *METRIC_METADATA_COLUMNS, "_metric_group", "_metric_file"]
    long = df.unpivot(
        index=index_columns,
        on=value_columns,
        variable_name="metric",
        value_name="value",
    )

    long = long.with_columns(
        pl.struct(["object_id", "object_type", "instance", "pod", "_metric_file"])
        .map_elements(metric_service_name, return_dtype=pl.String)
        .alias("service_name"),
        pl.struct(["object_id", "object_type", "pod", "_metric_file"])
        .map_elements(metric_pod_name, return_dtype=pl.String)
        .alias("attr.k8s.pod.name"),
        pl.col("namespace").cast(pl.String).alias("attr.k8s.namespace.name"),
        pl.coalesce([pl.col("kubernetes_node"), pl.col("instance")]).cast(pl.String).alias("attr.k8s.node.name"),
        pl.col("object_id").cast(pl.String).alias("attr.aiops.object_id"),
        pl.col("object_type").cast(pl.String).alias("attr.aiops.object_type"),
        pl.col("instance").cast(pl.String).alias("attr.aiops.instance"),
        pl.col("_metric_group").cast(pl.String).alias("attr.aiops.metric_group"),
        pl.col("_metric_file").cast(pl.String).alias("attr.aiops.metric_file"),
        pl.col("value").cast(pl.Float64),
        pl.col("metric").cast(pl.String),
    ).with_columns(
        pl.col("service_name").alias("attr.k8s.container.name"),
        pl.col("service_name").alias("attr.k8s.deployment.name"),
        pl.col("service_name").alias("attr.k8s.statefulset.name"),
        pl.col("service_name").alias("attr.k8s.service.name"),
    )

    return (
        long.filter(pl.col("time").is_not_null(), pl.col("service_name").is_not_null(), pl.col("service_name") != "")
        .select(list(METRIC_SCHEMA))
        .sort("time")
    )


def load_metric_day_window(src: Path, local_date: str, start: datetime, end: datetime) -> pl.DataFrame:
    date_root = src / local_date / "metric-parquet"
    if not date_root.exists():
        return empty_frame(METRIC_SCHEMA)

    frames: list[pl.DataFrame] = []
    for path in sorted(date_root.glob("**/*.parquet")):
        rel = path.relative_to(date_root)
        metric_group = rel.parts[0] if rel.parts else "metric"
        frame = transform_metric_file(path, metric_group, start, end)
        if not frame.is_empty():
            frames.append(frame)

    return concat_or_empty(frames, METRIC_SCHEMA)


def load_metrics(src: Path, start: datetime, end: datetime) -> pl.DataFrame:
    frames: list[pl.DataFrame] = []
    for local_date in iter_local_dates(start, end):
        frames.append(load_metric_day_window(src, local_date, start, end))
    return filter_window(concat_or_empty(frames, METRIC_SCHEMA), start, end, METRIC_SCHEMA)


def metrics_histogram(metrics: pl.DataFrame) -> pl.DataFrame:
    if metrics.is_empty():
        return empty_frame(HISTOGRAM_SCHEMA)
    return metrics.select(
        "time",
        "metric",
        "service_name",
        pl.lit(1.0).alias("count"),
        pl.col("value").alias("sum"),
        pl.col("value").alias("min"),
        pl.col("value").alias("max"),
        "attr.k8s.pod.name",
        "attr.k8s.service.name",
        "attr.k8s.namespace.name",
    ).select(list(HISTOGRAM_SCHEMA))


def trace_stats(traces: pl.DataFrame, prefix: str) -> pl.DataFrame:
    if traces.is_empty():
        return pl.DataFrame(
            schema={
                "SpanName": pl.String,
                f"{prefix}AvgDuration": pl.Float64,
                f"{prefix}SuccRate": pl.Float64,
                f"{prefix}P90": pl.Float64,
                f"{prefix}P95": pl.Float64,
                f"{prefix}P99": pl.Float64,
            }
        )

    return (
        traces.with_columns(
            (pl.col("duration").cast(pl.Float64) / 1_000_000_000.0).alias("_duration_s"),
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


def issue_json(row: dict[str, Any]) -> str:
    issues: dict[str, dict[str, float | bool]] = {}
    normal_p90 = float(row.get("NormalP90") or 0.0)
    abnormal_p90 = float(row.get("AbnormalP90") or 0.0)
    normal_succ = float(row.get("NormalSuccRate") or 1.0)
    abnormal_succ = float(row.get("AbnormalSuccRate") or 1.0)

    if normal_p90 > 0.0 and abnormal_p90 > normal_p90 * 2.0:
        issues["latency"] = {
            "change_rate": abnormal_p90 / normal_p90,
            "slo_violated": True,
        }
    if normal_succ - abnormal_succ > 0.2:
        issues["success_rate"] = {
            "change_rate": normal_succ - abnormal_succ,
            "slo_violated": True,
        }
    return json.dumps(issues, sort_keys=True)


def build_conclusion(normal_traces: pl.DataFrame, abnormal_traces: pl.DataFrame) -> pl.DataFrame:
    normal = trace_stats(normal_traces, "Normal")
    abnormal = trace_stats(abnormal_traces, "Abnormal")
    if normal.is_empty() and abnormal.is_empty():
        return empty_frame(CONCLUSION_SCHEMA)

    df = abnormal.join(normal, on="SpanName", how="full", coalesce=True).fill_null(0.0)
    df = df.with_columns(
        pl.struct(df.columns).map_elements(issue_json, return_dtype=pl.String).alias("Issues")
    )
    return df.select(list(CONCLUSION_SCHEMA)).sort("SpanName")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_parquet(path: Path, df: pl.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path)


def injection_payload(
    row: dict[str, Any],
    labels: list[str],
    normal_start: datetime,
    normal_end: datetime,
    abnormal_start: datetime,
    abnormal_end: datetime,
) -> dict[str, Any]:
    instances = as_list(row.get("instance"))
    pods = instances if row.get("instance_type") == "pod" else []
    return {
        "benchmark": "aiopschallenge2025",
        "created_at": datetime.now(tz=UTC).isoformat().replace("+00:00", "Z"),
        "fault_category": row.get("fault_category"),
        "fault_type": row.get("fault_type"),
        "ground_truth": {
            "container": labels,
            "function": None,
            "metric": row.get("key_metrics") or None,
            "node": [],
            "pod": pods,
            "service": labels,
            "span": labels,
            "additional_properties": {},
        },
        "injection_name": f"{row.get('uuid')}-{safe_name(str(row.get('fault_type') or 'fault'))}",
        "start_time": row.get("start_time"),
        "end_time": row.get("end_time"),
        "normal_start_time": normal_start.isoformat().replace("+00:00", "Z"),
        "normal_end_time": normal_end.isoformat().replace("+00:00", "Z"),
        "abnormal_start_time": abnormal_start.isoformat().replace("+00:00", "Z"),
        "abnormal_end_time": abnormal_end.isoformat().replace("+00:00", "Z"),
        "additional_properties": {
            "original_groundtruth": row,
        },
    }


def env_payload(
    row: dict[str, Any],
    normal_start: datetime,
    normal_end: datetime,
    abnormal_start: datetime,
    abnormal_end: datetime,
) -> dict[str, Any]:
    return {
        "dataset": "aiopschallenge2025",
        "namespace": "hipstershop",
        "uuid": row.get("uuid"),
        "normal_start_time": normal_start.isoformat().replace("+00:00", "Z"),
        "normal_end_time": normal_end.isoformat().replace("+00:00", "Z"),
        "abnormal_start_time": abnormal_start.isoformat().replace("+00:00", "Z"),
        "abnormal_end_time": abnormal_end.isoformat().replace("+00:00", "Z"),
        "time_mapping": {
            "folder_timezone": "UTC+08:00",
            "parquet_timestamp_timezone": "UTC",
            "groundtruth_timezone": "UTC",
        },
    }


def convert_case(
    src: Path,
    out_dir: Path,
    row: dict[str, Any],
    labels: list[str],
    min_window: timedelta,
) -> dict[str, Any]:
    normal_start, normal_end, abnormal_start, abnormal_end = case_windows(row, min_window)

    normal_traces = load_traces(src, normal_start, normal_end)
    abnormal_traces = load_traces(src, abnormal_start, abnormal_end)
    normal_metrics = load_metrics(src, normal_start, normal_end)
    abnormal_metrics = load_metrics(src, abnormal_start, abnormal_end)
    normal_logs = load_logs(src, normal_start, normal_end)
    abnormal_logs = load_logs(src, abnormal_start, abnormal_end)

    if normal_traces.is_empty() or abnormal_traces.is_empty() or normal_metrics.is_empty() or abnormal_metrics.is_empty():
        return {
            "status": "skipped_empty",
            "normal_traces": normal_traces.height,
            "abnormal_traces": abnormal_traces.height,
            "normal_metrics": normal_metrics.height,
            "abnormal_metrics": abnormal_metrics.height,
        }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "injection.json", injection_payload(row, labels, normal_start, normal_end, abnormal_start, abnormal_end))
    write_json(out_dir / "env.json", env_payload(row, normal_start, normal_end, abnormal_start, abnormal_end))

    write_parquet(out_dir / "normal_traces.parquet", normal_traces)
    write_parquet(out_dir / "abnormal_traces.parquet", abnormal_traces)
    write_parquet(out_dir / "normal_logs.parquet", normal_logs)
    write_parquet(out_dir / "abnormal_logs.parquet", abnormal_logs)
    write_parquet(out_dir / "normal_metrics.parquet", normal_metrics)
    write_parquet(out_dir / "abnormal_metrics.parquet", abnormal_metrics)
    write_parquet(out_dir / "normal_metrics_sum.parquet", normal_metrics)
    write_parquet(out_dir / "abnormal_metrics_sum.parquet", abnormal_metrics)
    write_parquet(out_dir / "normal_metrics_histogram.parquet", metrics_histogram(normal_metrics))
    write_parquet(out_dir / "abnormal_metrics_histogram.parquet", metrics_histogram(abnormal_metrics))
    write_parquet(out_dir / "conclusion.parquet", build_conclusion(normal_traces, abnormal_traces))
    (out_dir / ".finished").touch()

    return {
        "status": "converted",
        "normal_traces": normal_traces.height,
        "abnormal_traces": abnormal_traces.height,
        "normal_metrics": normal_metrics.height,
        "abnormal_metrics": abnormal_metrics.height,
        "normal_logs": normal_logs.height,
        "abnormal_logs": abnormal_logs.height,
    }


def load_groundtruth(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def prepare_target(data_root: Path, dataset: str, overwrite: bool) -> tuple[Path, Path]:
    data_dir = data_root / "data" / dataset
    meta_dir = data_root / "meta" / dataset
    if data_dir.exists() or meta_dir.exists():
        if not overwrite:
            raise SystemExit(
                f"Target dataset already exists: {data_dir} or {meta_dir}. "
                "Use --overwrite to replace only this target dataset."
            )
        if data_dir.exists():
            shutil.rmtree(data_dir)
        if meta_dir.exists():
            shutil.rmtree(meta_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)
    return data_dir, meta_dir


def write_meta(meta_dir: Path, dataset: str, converted: list[tuple[str, list[str]]]) -> None:
    index_rows = [{"dataset": dataset, "datapack": datapack} for datapack, _ in converted]
    label_rows = [
        {"dataset": dataset, "datapack": datapack, "gt.level": "service", "gt.name": label}
        for datapack, labels in converted
        for label in labels
    ]
    pl.DataFrame(index_rows, schema={"dataset": pl.String, "datapack": pl.String}).sort("datapack").write_parquet(
        meta_dir / "index.parquet"
    )
    pl.DataFrame(
        label_rows,
        schema={"dataset": pl.String, "datapack": pl.String, "gt.level": pl.String, "gt.name": pl.String},
    ).sort(["datapack", "gt.name"]).write_parquet(meta_dir / "labels.parquet")


def build_dataset(args: argparse.Namespace) -> None:
    src = args.src.resolve()
    data_root = args.data_root.resolve()
    if not (src / "groundtruth.jsonl").exists():
        raise SystemExit(f"Missing groundtruth.jsonl under {src}")

    rows = load_groundtruth(src / "groundtruth.jsonl")
    data_dir, meta_dir = prepare_target(data_root, args.dataset, args.overwrite)

    stats: dict[str, Any] = {
        "source": str(src),
        "dataset": args.dataset,
        "total_groundtruth": len(rows),
        "converted": 0,
        "skipped_node": 0,
        "skipped_no_labels": 0,
        "skipped_empty": 0,
        "skipped_limit": 0,
        "case_results": [],
    }
    converted: list[tuple[str, list[str]]] = []
    min_window = timedelta(minutes=args.min_window_minutes)

    for row in tqdm(rows, desc=f"build {args.dataset}"):
        if args.limit is not None and stats["converted"] >= args.limit:
            break

        if row.get("instance_type") == "node":
            stats["skipped_node"] += 1
            continue

        labels = service_labels(row)
        if not labels:
            stats["skipped_no_labels"] += 1
            continue

        datapack = safe_name(f"aiops2025-{row.get('uuid')}-{row.get('fault_type')}")
        result = convert_case(src, data_dir / datapack, row, labels, min_window)
        result.update({"datapack": datapack, "uuid": row.get("uuid"), "labels": labels})
        stats["case_results"].append(result)

        if result["status"] != "converted":
            stats["skipped_empty"] += 1
            if (data_dir / datapack).exists():
                shutil.rmtree(data_dir / datapack)
            continue

        converted.append((datapack, labels))
        stats["converted"] += 1

    if not converted:
        raise SystemExit("No datapacks were converted")

    write_meta(meta_dir, args.dataset, converted)
    write_json(meta_dir / "conversion_report.json", stats)
    print(
        "wrote "
        f"dataset={args.dataset} datapacks={stats['converted']} "
        f"skipped_node={stats['skipped_node']} "
        f"skipped_empty={stats['skipped_empty']} "
        f"data_root={data_root}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--min-window-minutes", type=float, default=10.0)
    parser.add_argument("--limit", type=int, default=None, help="Convert only the first N service/pod cases")
    parser.add_argument("--overwrite", action="store_true", help="Replace only the target dataset data/meta dirs")
    args = parser.parse_args()

    if args.min_window_minutes <= 0 or not math.isfinite(args.min_window_minutes):
        raise SystemExit("--min-window-minutes must be a positive finite number")
    if args.limit is not None and args.limit <= 0:
        raise SystemExit("--limit must be positive")

    build_dataset(args)


if __name__ == "__main__":
    main()
