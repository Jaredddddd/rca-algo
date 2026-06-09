#!/usr/bin/env python3
"""Convert AIOpsChallenge2025 into component-preserving rcabench datapacks.

This builder intentionally keeps pod/resource identity in ``service_name`` so
existing service-rank algorithms can run as component-rank algorithms without
runtime label access. The output uses ``gt.level = service`` only for
rcabench-platform compatibility; ``gt.name`` is a component id such as
``svc:frontend`` or ``pod:frontend-0``.


cd /home/ljw/paper/aegis/rca-algo-contrib

uv run --package evidencerank python scripts/build_aiopschallenge2025_rcabench_component.py \
  --dataset aiopschallenge2025_rcabench_component \
  --jobs 4 \
  --overwrite
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any

import polars as pl
from tqdm.auto import tqdm

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.build_aiopschallenge2025_rcabench import (
    DEFAULT_DATA_ROOT,
    DEFAULT_SRC,
    LOG_SCHEMA,
    METRIC_METADATA_COLUMNS,
    METRIC_SCHEMA,
    TRACE_SCHEMA,
    UTC,
    as_list,
    build_conclusion,
    case_windows,
    canonical_service_name,
    child_of_span_expr,
    clean_deleted_suffix,
    concat_or_empty,
    empty_frame,
    env_payload,
    filter_window,
    is_numeric_dtype,
    iter_local_dates,
    iter_utc_hours,
    load_groundtruth,
    local_date_hour,
    log_level,
    metrics_histogram,
    prepare_target,
    safe_name,
    service_from_pod,
    tag_value_expr,
    utc_second_string,
    write_json,
    write_parquet,
)


DEFAULT_DATASET = "aiopschallenge2025_rcabench_component"
UNKNOWN_COMPONENT = "unknown"


def _clean_identity(value: Any) -> str:
    text = clean_deleted_suffix(str(value or "")).strip()
    if not text or text.lower() in {"nan", "none", "null"}:
        return ""
    return text


def _component(prefix: str, value: Any) -> str:
    text = _clean_identity(value)
    if not text:
        return UNKNOWN_COMPONENT
    return f"{prefix}:{text}"


def svc_component(value: Any) -> str:
    text = _clean_identity(value)
    if not text:
        return UNKNOWN_COMPONENT
    return _component("svc", canonical_service_name(text))


def pod_component(value: Any) -> str:
    return _component("pod", value)


def node_component(value: Any) -> str:
    return _component("node", value)


def object_component(object_type: Any, value: Any) -> str:
    type_text = _clean_identity(object_type).lower()
    value_text = _clean_identity(value)
    if not value_text:
        return UNKNOWN_COMPONENT
    if not type_text:
        type_text = "object"
    return f"obj:{type_text}:{value_text}"


def _parent_service_from_pod(value: Any) -> str:
    pod = _clean_identity(value)
    if not pod:
        return ""
    parent = service_from_pod(pod)
    return svc_component(parent) if parent else ""


def _looks_like_trace_pod_name(raw_service: Any, candidate: Any) -> bool:
    service = canonical_service_name(_clean_identity(raw_service))
    text = _clean_identity(candidate)
    if not service or not text:
        return False
    if text == service:
        return False
    parent = service_from_pod(text)
    return parent == service or text.startswith(f"{service}-")


def metric_component_name(
    row: dict[str, Any],
    *,
    include_node_components: bool,
    include_resource_components: bool,
) -> str:
    object_id = _clean_identity(row.get("object_id"))
    object_type = _clean_identity(row.get("object_type")).lower()
    pod = _clean_identity(row.get("pod"))
    instance = _clean_identity(row.get("instance"))
    kubernetes_node = _clean_identity(row.get("kubernetes_node"))
    metric_file = _clean_identity(row.get("_metric_file"))

    if pod:
        return pod_component(pod)
    if object_id and (
        object_type == "pod"
        or "/pod/" in metric_file
        or re.search(r"-[0-9a-f]{8,10}-[a-z0-9]{5}$", object_id)
    ):
        return pod_component(object_id)
    if object_type == "node":
        if not include_node_components:
            return UNKNOWN_COMPONENT
        return node_component(kubernetes_node or instance or object_id)
    if object_type == "service":
        return svc_component(object_id or instance)
    if object_type in {"tidb", "tikv", "pd", "pod_ns"}:
        if not include_resource_components:
            return UNKNOWN_COMPONENT
        return object_component(object_type, object_id or instance or pod)
    if object_id:
        if object_type:
            return object_component(object_type, object_id) if include_resource_components else UNKNOWN_COMPONENT
        return svc_component(object_id)
    if instance:
        if instance.startswith("aiops-k8s-"):
            return node_component(instance) if include_node_components else UNKNOWN_COMPONENT
        return object_component(object_type, instance) if object_type else svc_component(instance)
    if object_type:
        return object_component(object_type, object_type) if include_resource_components else UNKNOWN_COMPONENT
    return UNKNOWN_COMPONENT


def metric_parent_service_name(row: dict[str, Any]) -> str:
    object_id = _clean_identity(row.get("object_id"))
    object_type = _clean_identity(row.get("object_type")).lower()
    pod = _clean_identity(row.get("pod"))
    instance = _clean_identity(row.get("instance"))
    metric_file = _clean_identity(row.get("_metric_file"))

    pod_identity = ""
    if pod:
        pod_identity = pod
    elif object_id and (object_type == "pod" or "/pod/" in metric_file):
        pod_identity = object_id
    if pod_identity:
        return _parent_service_from_pod(pod_identity)
    if object_type == "service":
        return svc_component(object_id or instance)
    return ""


def metric_pod_name(row: dict[str, Any]) -> str:
    pod = _clean_identity(row.get("pod"))
    object_id = _clean_identity(row.get("object_id"))
    object_type = _clean_identity(row.get("object_type")).lower()
    metric_file = _clean_identity(row.get("_metric_file"))
    if pod:
        return pod
    if object_id and (object_type == "pod" or "/pod/" in metric_file):
        return object_id
    return ""


def metric_evidence_key(row: dict[str, Any]) -> str:
    group = _clean_identity(row.get("_metric_group"))
    metric = _clean_identity(row.get("metric"))
    kpi_key = _clean_identity(row.get("kpi_key"))
    kpi_name = _clean_identity(row.get("kpi_name"))

    parts = [part for part in (group, kpi_key or kpi_name, metric) if part]
    if not parts:
        return "value"

    deduped: list[str] = []
    for part in parts:
        if part not in deduped:
            deduped.append(part)
    return "::".join(deduped)


def process_tag_value_expr(key: str, alias: str) -> pl.Expr:
    return (
        pl.col("process")
        .struct.field("tags")
        .list.eval(
            pl.when(pl.element().struct.field("key") == key)
            .then(pl.element().struct.field("value"))
        )
        .list.drop_nulls()
        .list.first()
        .cast(pl.String)
        .fill_null("")
        .alias(alias)
    )


def trace_pod_name(row: dict[str, Any]) -> str:
    pod_name = _clean_identity(row.get("podName"))
    if pod_name:
        return pod_name
    process_name = _clean_identity(row.get("name"))
    raw_service = _clean_identity(row.get("raw_service"))
    if _looks_like_trace_pod_name(raw_service, process_name):
        return process_name
    return ""


def trace_component_name(row: dict[str, Any]) -> str:
    pod_name = trace_pod_name(row)
    if pod_name:
        return pod_component(pod_name)
    return svc_component(row.get("raw_service"))


def trace_node_name(row: dict[str, Any]) -> str:
    return _clean_identity(row.get("nodeName")) or _clean_identity(row.get("node_name"))


def component_labels(row: dict[str, Any], *, include_parent_service_labels: bool) -> list[str]:
    labels: set[str] = set()
    source = _clean_identity(row.get("source"))
    destination = _clean_identity(row.get("destination"))
    service = _clean_identity(row.get("service"))
    instance_type = _clean_identity(row.get("instance_type")).lower()

    if source and destination:
        labels.add(svc_component(source))
        labels.add(svc_component(destination))
    elif service:
        labels.add(svc_component(service))
    else:
        for item in as_list(row.get("instance")):
            item = _clean_identity(item)
            if not item:
                continue
            if instance_type == "pod":
                labels.add(pod_component(item))
                parent = service_from_pod(item)
                if include_parent_service_labels and parent and parent != item:
                    labels.add(svc_component(parent))
            elif instance_type == "node":
                labels.add(node_component(item))
            elif instance_type:
                labels.add(object_component(instance_type, item))
            else:
                labels.add(svc_component(item))

    return sorted(label for label in labels if label and label != UNKNOWN_COMPONENT)


def service_set(df: pl.DataFrame) -> set[str]:
    if df.is_empty() or "service_name" not in df.columns:
        return set()
    return {
        service
        for service in df.get_column("service_name").drop_nulls().cast(pl.String).unique().to_list()
        if service and service != UNKNOWN_COMPONENT
    }


def observable_labels(labels: list[str], *frames: pl.DataFrame) -> tuple[set[str], set[str]]:
    components: set[str] = set()
    for frame in frames:
        components.update(service_set(frame))
    return set(labels) & components, components


def expand_service_labels_to_observed_pods(labels: list[str], *frames: pl.DataFrame) -> list[str]:
    service_labels = {label for label in labels if label.startswith("svc:")}
    if not service_labels:
        return labels

    expanded = set(labels)
    for frame in frames:
        if frame.is_empty() or "attr.k8s.service.name" not in frame.columns or "attr.k8s.pod.name" not in frame.columns:
            continue
        pod_rows = (
            frame.select("attr.k8s.service.name", "attr.k8s.pod.name")
            .filter(
                pl.col("attr.k8s.service.name").is_in(service_labels),
                pl.col("attr.k8s.pod.name").is_not_null(),
                pl.col("attr.k8s.pod.name") != "",
            )
            .unique()
        )
        for pod_name in pod_rows.get_column("attr.k8s.pod.name").to_list():
            expanded.add(pod_component(pod_name))
    return sorted(label for label in expanded if label and label != UNKNOWN_COMPONENT)


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
        child_of_span_expr(),
        pl.col("operationName").cast(pl.String).alias("span_name"),
        pl.col("process").struct.field("serviceName").cast(pl.String).alias("raw.service_name"),
        pl.col("process")
        .struct.field("serviceName")
        .cast(pl.String)
        .map_elements(canonical_service_name, return_dtype=pl.String)
        .alias("_raw_canonical_service"),
        process_tag_value_expr("podName", "_process_podName"),
        process_tag_value_expr("name", "_process_name"),
        process_tag_value_expr("nodeName", "_process_nodeName"),
        process_tag_value_expr("node_name", "_process_node_name"),
        (
            pl.when(pl.col("duration") > 0)
            .then(pl.col("duration"))
            .otherwise(0)
            .cast(pl.UInt64)
            * pl.lit(1000, dtype=pl.UInt64)
        ).alias("duration"),
        tag_value_expr("span.kind", "attr.span_kind"),
        tag_value_expr("status.code", "status.code"),
        tag_value_expr("status.message", "status.message"),
        tag_value_expr("http.status_code", "http.status_code"),
        tag_value_expr("otel.status_code", "otel.status_code"),
        tag_value_expr("error", "error"),
        pl.lit("").cast(pl.String).alias("attr.k8s.namespace.name"),
        pl.col("flags").cast(pl.Float64).alias("raw.flags"),
        pl.col("startTime").cast(pl.Int64).alias("raw.start_time"),
        pl.col("startTimeMillis").cast(pl.Int64).alias("raw.start_time_millis"),
        pl.col("duration").cast(pl.Int64).alias("raw.duration"),
        pl.col("references").alias("raw.references"),
        pl.col("tags").alias("raw.tags"),
        pl.col("logs").alias("raw.logs"),
        pl.col("process").alias("raw.process"),
    ).with_columns(
        pl.struct(
            [
                pl.col("_raw_canonical_service").alias("raw_service"),
                pl.col("_process_podName").alias("podName"),
                pl.col("_process_name").alias("name"),
            ]
        )
        .map_elements(trace_pod_name, return_dtype=pl.String)
        .alias("attr.k8s.pod.name"),
        pl.struct(
            [
                pl.col("_raw_canonical_service").alias("raw_service"),
                pl.col("_process_podName").alias("podName"),
                pl.col("_process_name").alias("name"),
            ]
        )
        .map_elements(trace_component_name, return_dtype=pl.String)
        .alias("service_name"),
        pl.col("_raw_canonical_service")
        .map_elements(svc_component, return_dtype=pl.String)
        .alias("attr.k8s.service.name"),
        pl.struct(
            [
                pl.col("_process_nodeName").alias("nodeName"),
                pl.col("_process_node_name").alias("node_name"),
            ]
        )
        .map_elements(trace_node_name, return_dtype=pl.String)
        .alias("attr.k8s.node.name"),
        pl.col("http.status_code").alias("attr.http.response.status_code"),
        pl.col("error").alias("attr.error"),
        pl.col("parent_span_id").fill_null(""),
    )

    status_code_number = pl.col("status.code").cast(pl.Int64, strict=False)
    http_status_number = pl.col("http.status_code").cast(pl.Int64, strict=False)
    status_is_error = (
        pl.col("error").str.to_lowercase().is_in(["true", "1", "yes"])
        | pl.col("otel.status_code").str.to_lowercase().is_in(["error", "2"])
        | ((status_code_number.is_not_null()) & (~status_code_number.is_in([0, 1])))
        | ((http_status_number.is_not_null()) & (http_status_number >= 400))
        | pl.col("status.message")
        .str.to_lowercase()
        .str.contains(r"\b(error|fail|exception|timeout|unavailable|denied|refused)\b")
    )
    out = out.with_columns(
        pl.when(status_is_error)
        .then(pl.lit("Error"))
        .otherwise(pl.lit("Ok"))
        .alias("status_code")
    ).with_columns(
        pl.col("status_code").alias("attr.status_code"),
    )
    parent_lookup = out.select(
        pl.col("span_id").alias("_parent_span_id"),
        pl.col("service_name").alias("parent_service"),
    ).unique("_parent_span_id")
    out = out.join(
        parent_lookup,
        left_on="parent_span_id",
        right_on="_parent_span_id",
        how="left",
    ).with_columns(pl.col("parent_service").fill_null(""))

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
        pl.col("message").map_elements(log_level, return_dtype=pl.String).alias("level"),
        pl.col("message").cast(pl.String).alias("message"),
        pod_clean.alias("attr.k8s.pod.name"),
        service_expr.alias("_raw_service_name"),
        pl.col("k8_namespace").cast(pl.String).alias("attr.k8s.namespace.name"),
        pl.col("k8_node_name").cast(pl.String).alias("attr.k8s.node.name"),
        pl.col("@timestamp").cast(pl.String).alias("raw.timestamp"),
        pl.col("agent_name").cast(pl.String).alias("raw.agent_name"),
        pod_clean.alias("raw.k8_pod"),
        pl.col("k8_namespace").cast(pl.String).alias("raw.k8_namespace"),
        pl.col("k8_node_name").cast(pl.String).alias("raw.k8_node_name"),
    ).with_columns(
        pl.when(pl.col("attr.k8s.pod.name").is_not_null() & (pl.col("attr.k8s.pod.name") != ""))
        .then(pl.col("attr.k8s.pod.name").map_elements(pod_component, return_dtype=pl.String))
        .otherwise(pl.col("_raw_service_name").map_elements(svc_component, return_dtype=pl.String))
        .alias("service_name"),
        pl.col("_raw_service_name").map_elements(svc_component, return_dtype=pl.String).alias("attr.k8s.service.name"),
    ).with_columns(
        pl.col("service_name").alias("attr.k8s.container.name"),
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


def transform_metric_file(
    path: Path,
    metric_group: str,
    start: datetime | None = None,
    end: datetime | None = None,
    *,
    include_node_components: bool = False,
    include_resource_components: bool = False,
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

    metric_identity = pl.struct(
        ["object_id", "object_type", "instance", "pod", "kubernetes_node", "_metric_file"]
    )
    metric_key_identity = pl.struct(["_metric_group", "metric", "kpi_key", "kpi_name"])
    component_name = lambda row: metric_component_name(
        row,
        include_node_components=include_node_components,
        include_resource_components=include_resource_components,
    )
    long = long.with_columns(
        metric_identity.map_elements(component_name, return_dtype=pl.String).alias("service_name"),
        metric_identity.map_elements(metric_parent_service_name, return_dtype=pl.String).alias("_parent_service_name"),
        metric_identity.map_elements(metric_pod_name, return_dtype=pl.String).alias("attr.k8s.pod.name"),
        pl.col("namespace").cast(pl.String).alias("attr.k8s.namespace.name"),
        pl.coalesce([pl.col("kubernetes_node"), pl.col("instance")]).cast(pl.String).alias("attr.k8s.node.name"),
        pl.col("object_id").cast(pl.String).alias("attr.aiops.object_id"),
        pl.col("object_type").cast(pl.String).alias("attr.aiops.object_type"),
        pl.col("instance").cast(pl.String).alias("attr.aiops.instance"),
        pl.col("pod").cast(pl.String).alias("attr.aiops.pod"),
        pl.col("device").cast(pl.String).alias("attr.aiops.device"),
        pl.col("mountpoint").cast(pl.String).alias("attr.aiops.mountpoint"),
        pl.col("cf").cast(pl.String).alias("attr.aiops.cf"),
        pl.col("sql_type").cast(pl.String).alias("attr.aiops.sql_type"),
        pl.col("type").cast(pl.String).alias("attr.aiops.type"),
        pl.col("kpi_key").cast(pl.String).alias("attr.aiops.kpi_key"),
        pl.col("kpi_name").cast(pl.String).alias("attr.aiops.kpi_name"),
        pl.col("_metric_group").cast(pl.String).alias("attr.aiops.metric_group"),
        pl.col("_metric_file").cast(pl.String).alias("attr.aiops.metric_file"),
        pl.col("value").cast(pl.Float64),
        metric_key_identity.map_elements(metric_evidence_key, return_dtype=pl.String).alias("metric"),
    ).with_columns(
        pl.col("service_name").alias("attr.k8s.container.name"),
        pl.col("service_name").alias("attr.k8s.deployment.name"),
        pl.col("service_name").alias("attr.k8s.statefulset.name"),
        pl.col("_parent_service_name").alias("attr.k8s.service.name"),
    )

    return (
        long.filter(
            pl.col("time").is_not_null(),
            pl.col("service_name").is_not_null(),
            pl.col("service_name") != "",
            pl.col("service_name") != UNKNOWN_COMPONENT,
        )
        .select(list(METRIC_SCHEMA))
        .sort("time")
    )


def load_metric_day_window(
    src: Path,
    local_date: str,
    start: datetime,
    end: datetime,
    *,
    include_node_components: bool,
    include_resource_components: bool,
) -> pl.DataFrame:
    date_root = src / local_date / "metric-parquet"
    if not date_root.exists():
        return empty_frame(METRIC_SCHEMA)

    frames: list[pl.DataFrame] = []
    for path in sorted(date_root.glob("**/*.parquet")):
        rel = path.relative_to(date_root)
        metric_group = rel.parts[0] if rel.parts else "metric"
        frame = transform_metric_file(
            path,
            metric_group,
            start,
            end,
            include_node_components=include_node_components,
            include_resource_components=include_resource_components,
        )
        if not frame.is_empty():
            frames.append(frame)

    return concat_or_empty(frames, METRIC_SCHEMA)


def load_metrics(
    src: Path,
    start: datetime,
    end: datetime,
    *,
    include_node_components: bool,
    include_resource_components: bool,
) -> pl.DataFrame:
    frames: list[pl.DataFrame] = []
    for local_date in iter_local_dates(start, end):
        frames.append(
            load_metric_day_window(
                src,
                local_date,
                start,
                end,
                include_node_components=include_node_components,
                include_resource_components=include_resource_components,
            )
        )
    return filter_window(concat_or_empty(frames, METRIC_SCHEMA), start, end, METRIC_SCHEMA)


def injection_payload(
    row: dict[str, Any],
    labels: list[str],
    normal_start: datetime,
    normal_end: datetime,
    abnormal_start: datetime,
    abnormal_end: datetime,
    *,
    include_parent_service_labels: bool,
    expand_service_labels_to_pods: bool,
    include_node_components: bool,
    include_resource_components: bool,
) -> dict[str, Any]:
    instances = as_list(row.get("instance"))
    pods = instances if row.get("instance_type") == "pod" else []
    service_labels = [label for label in labels if label.startswith("svc:")]
    pod_labels = [label for label in labels if label.startswith("pod:")]
    node_labels = [label for label in labels if label.startswith("node:")]
    object_labels = [label for label in labels if label.startswith("obj:")]
    return {
        "benchmark": "aiopschallenge2025",
        "created_at": datetime.now(tz=UTC).isoformat().replace("+00:00", "Z"),
        "fault_category": row.get("fault_category"),
        "fault_type": row.get("fault_type"),
        "ground_truth": {
            "component": labels,
            "container": labels,
            "function": None,
            "metric": row.get("key_metrics") or None,
            "node": node_labels,
            "object": object_labels,
            "pod": pod_labels or pods,
            "service": service_labels,
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
            "rank_granularity": "component",
            "gt_level_compatibility": "service",
            "include_parent_service_labels": include_parent_service_labels,
            "expand_service_labels_to_pods": expand_service_labels_to_pods,
            "include_node_components": include_node_components,
            "include_resource_components": include_resource_components,
            "original_groundtruth": row,
        },
    }


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


def convert_case(
    src: Path,
    out_dir: Path,
    row: dict[str, Any],
    labels: list[str],
    min_window: timedelta,
    require_observable_label: bool,
    *,
    include_parent_service_labels: bool,
    expand_service_labels_to_pods: bool,
    include_node_components: bool,
    include_resource_components: bool,
) -> dict[str, Any]:
    normal_start, normal_end, abnormal_start, abnormal_end = case_windows(row, min_window)

    normal_traces = load_traces(src, normal_start, normal_end)
    abnormal_traces = load_traces(src, abnormal_start, abnormal_end)
    normal_metrics = load_metrics(
        src,
        normal_start,
        normal_end,
        include_node_components=include_node_components,
        include_resource_components=include_resource_components,
    )
    abnormal_metrics = load_metrics(
        src,
        abnormal_start,
        abnormal_end,
        include_node_components=include_node_components,
        include_resource_components=include_resource_components,
    )
    normal_logs = load_logs(src, normal_start, normal_end)
    abnormal_logs = load_logs(src, abnormal_start, abnormal_end)

    if normal_traces.is_empty() or abnormal_traces.is_empty() or normal_metrics.is_empty() or abnormal_metrics.is_empty():
        return {
            "status": "skipped_empty",
            "primary_labels": labels,
            "normal_traces": normal_traces.height,
            "abnormal_traces": abnormal_traces.height,
            "normal_metrics": normal_metrics.height,
            "abnormal_metrics": abnormal_metrics.height,
        }

    final_labels = (
        expand_service_labels_to_observed_pods(
            labels,
            normal_traces,
            abnormal_traces,
            normal_metrics,
            abnormal_metrics,
            normal_logs,
            abnormal_logs,
        )
        if expand_service_labels_to_pods
        else labels
    )

    matched_labels, candidate_components = observable_labels(
        final_labels,
        normal_traces,
        abnormal_traces,
        normal_metrics,
        abnormal_metrics,
        normal_logs,
        abnormal_logs,
    )
    if require_observable_label and not matched_labels:
        return {
            "status": "skipped_unobservable_label",
            "primary_labels": labels,
            "labels": final_labels,
            "candidate_component_count": len(candidate_components),
            "candidate_components": sorted(candidate_components),
            "normal_traces": normal_traces.height,
            "abnormal_traces": abnormal_traces.height,
            "normal_metrics": normal_metrics.height,
            "abnormal_metrics": abnormal_metrics.height,
            "normal_logs": normal_logs.height,
            "abnormal_logs": abnormal_logs.height,
        }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        out_dir / "injection.json",
        injection_payload(
            row,
            final_labels,
            normal_start,
            normal_end,
            abnormal_start,
            abnormal_end,
            include_parent_service_labels=include_parent_service_labels,
            expand_service_labels_to_pods=expand_service_labels_to_pods,
            include_node_components=include_node_components,
            include_resource_components=include_resource_components,
        ),
    )
    env = env_payload(row, normal_start, normal_end, abnormal_start, abnormal_end)
    env["rank_granularity"] = "component"
    env["gt_level_compatibility"] = "service"
    env["include_node_components"] = include_node_components
    env["include_resource_components"] = include_resource_components
    write_json(out_dir / "env.json", env)

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

    component_counts = {
        "normal_trace_components": len(service_set(normal_traces)),
        "abnormal_trace_components": len(service_set(abnormal_traces)),
        "normal_metric_components": len(service_set(normal_metrics)),
        "abnormal_metric_components": len(service_set(abnormal_metrics)),
        "normal_log_components": len(service_set(normal_logs)),
        "abnormal_log_components": len(service_set(abnormal_logs)),
    }
    return {
        "status": "converted",
        "primary_labels": labels,
        "labels": final_labels,
        "normal_traces": normal_traces.height,
        "abnormal_traces": abnormal_traces.height,
        "normal_metrics": normal_metrics.height,
        "abnormal_metrics": abnormal_metrics.height,
        "normal_logs": normal_logs.height,
        "abnormal_logs": abnormal_logs.height,
        "matched_labels": sorted(matched_labels),
        "candidate_component_count": len(candidate_components),
        **component_counts,
    }


def make_case_task(
    src: Path,
    data_dir: Path,
    row: dict[str, Any],
    labels: list[str],
    min_window_minutes: float,
    require_observable_label: bool,
    *,
    include_parent_service_labels: bool,
    expand_service_labels_to_pods: bool,
    include_node_components: bool,
    include_resource_components: bool,
) -> dict[str, Any]:
    datapack = safe_name(f"aiops2025-{row.get('uuid')}-{row.get('fault_type')}")
    return {
        "src": str(src),
        "out_dir": str(data_dir / datapack),
        "row": row,
        "labels": labels,
        "datapack": datapack,
        "min_window_minutes": min_window_minutes,
        "require_observable_label": require_observable_label,
        "include_parent_service_labels": include_parent_service_labels,
        "expand_service_labels_to_pods": expand_service_labels_to_pods,
        "include_node_components": include_node_components,
        "include_resource_components": include_resource_components,
    }


def run_case_task(task: dict[str, Any]) -> tuple[str, list[str], dict[str, Any]]:
    datapack = str(task["datapack"])
    labels = list(task["labels"])
    result = convert_case(
        Path(task["src"]),
        Path(task["out_dir"]),
        dict(task["row"]),
        labels,
        timedelta(minutes=float(task["min_window_minutes"])),
        bool(task["require_observable_label"]),
        include_parent_service_labels=bool(task["include_parent_service_labels"]),
        expand_service_labels_to_pods=bool(task["expand_service_labels_to_pods"]),
        include_node_components=bool(task["include_node_components"]),
        include_resource_components=bool(task["include_resource_components"]),
    )
    final_labels = result.get("labels", labels)
    result.update(
        {
            "datapack": datapack,
            "uuid": task["row"].get("uuid"),
            "primary_labels": labels,
            "labels": final_labels,
        }
    )
    return datapack, final_labels, result


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
        "rank_granularity": "component",
        "gt_level_compatibility": "service",
        "include_node": args.include_node,
        "include_node_components": args.include_node,
        "include_resource_components": args.include_resource_components,
        "include_parent_service_labels": args.include_parent_service_labels,
        "expand_service_labels_to_pods": not args.no_expand_service_labels_to_pods,
        "total_groundtruth": len(rows),
        "converted": 0,
        "skipped_node": 0,
        "skipped_no_labels": 0,
        "skipped_empty": 0,
        "skipped_unobservable_label": 0,
        "skipped_limit": 0,
        "case_results": [],
    }
    converted: list[tuple[str, list[str]]] = []
    tasks: list[dict[str, Any]] = []
    require_observable_label = not args.keep_unobservable_labels
    expand_service_labels_to_pods = not args.no_expand_service_labels_to_pods

    for row in rows:
        if row.get("instance_type") == "node" and not args.include_node:
            stats["skipped_node"] += 1
            continue

        labels = component_labels(row, include_parent_service_labels=args.include_parent_service_labels)
        if not labels:
            stats["skipped_no_labels"] += 1
            continue

        tasks.append(
            make_case_task(
                src,
                data_dir,
                row,
                labels,
                args.min_window_minutes,
                require_observable_label,
                include_parent_service_labels=args.include_parent_service_labels,
                expand_service_labels_to_pods=expand_service_labels_to_pods,
                include_node_components=args.include_node,
                include_resource_components=args.include_resource_components,
            )
        )

    def record_result(datapack: str, final_labels: list[str], result: dict[str, Any]) -> None:
        stats["case_results"].append(result)
        if result["status"] != "converted":
            if result["status"] == "skipped_empty":
                stats["skipped_empty"] += 1
            elif result["status"] == "skipped_unobservable_label":
                stats["skipped_unobservable_label"] += 1
            return

        converted.append((datapack, final_labels))
        stats["converted"] += 1

    jobs = int(args.jobs)
    if args.limit is not None and jobs > 1:
        print("--limit is set; running sequentially to preserve converted-limit semantics")
        jobs = 1

    if jobs <= 1:
        for task in tqdm(tasks, desc=f"build {args.dataset}"):
            if args.limit is not None and stats["converted"] >= args.limit:
                stats["skipped_limit"] += 1
                break
            datapack, final_labels, result = run_case_task(task)
            record_result(datapack, final_labels, result)
    else:
        with ProcessPoolExecutor(max_workers=jobs) as executor:
            future_to_task = {executor.submit(run_case_task, task): task for task in tasks}
            for future in tqdm(as_completed(future_to_task), total=len(future_to_task), desc=f"build {args.dataset}"):
                datapack, final_labels, result = future.result()
                record_result(datapack, final_labels, result)

    stats["case_results"].sort(key=lambda item: str(item.get("datapack", "")))
    converted.sort(key=lambda item: item[0])

    if not converted:
        raise SystemExit("No datapacks were converted")

    write_meta(meta_dir, args.dataset, converted)
    write_json(meta_dir / "conversion_report.json", stats)
    print(
        "wrote "
        f"dataset={args.dataset} datapacks={stats['converted']} "
        f"skipped_node={stats['skipped_node']} "
        f"skipped_empty={stats['skipped_empty']} "
        f"skipped_unobservable_label={stats['skipped_unobservable_label']} "
        f"data_root={data_root}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--min-window-minutes", type=float, default=10.0)
    parser.add_argument("--limit", type=int, default=None, help="Convert only the first N eligible cases")
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Number of case conversion workers. Keep modest because raw parquet reads are I/O-heavy.",
    )
    parser.add_argument(
        "--include-node",
        action="store_true",
        help="Include original node-level AIOps25 cases and node:<name> metric components.",
    )
    parser.add_argument(
        "--include-resource-components",
        action="store_true",
        help=(
            "Include metric-only resource objects such as obj:tikv:<id>, obj:tidb:<id>, and obj:pd:<id>. "
            "Disabled by default because current CREST has no trace/log ownership for these components."
        ),
    )
    parser.add_argument(
        "--include-parent-service-labels",
        action="store_true",
        help="For pod labels, also accept the parent svc:<service> component.",
    )
    parser.add_argument(
        "--no-expand-service-labels-to-pods",
        action="store_true",
        help=(
            "Do not add observed pod:<pod> labels for service/endpoint GT labels. "
            "By default component conversion keeps svc:<service> and accepts observed pods of that service."
        ),
    )
    parser.add_argument(
        "--keep-unobservable-labels",
        action="store_true",
        help="Keep cases whose component labels are absent from all converted component candidates.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace only the target dataset data/meta dirs")
    args = parser.parse_args()

    if args.min_window_minutes <= 0 or not math.isfinite(args.min_window_minutes):
        raise SystemExit("--min-window-minutes must be a positive finite number")
    if args.limit is not None and args.limit <= 0:
        raise SystemExit("--limit must be positive")
    if args.jobs <= 0:
        raise SystemExit("--jobs must be positive")

    build_dataset(args)


if __name__ == "__main__":
    main()
