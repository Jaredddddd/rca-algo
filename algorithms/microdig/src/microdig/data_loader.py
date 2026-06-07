"""
Data loading utilities for MicroDig with Polars support.

This module provides data loading capabilities for the new data format
using Polars for efficient data processing.
"""

import datetime
import json
import math
import time
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Optional

import polars as pl
from rcabench_platform.v2.logging import logger


def timeit():
    """Simple timing decorator"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logger.info(f"{func.__name__} took {end - start:.2f} seconds")
            return result

        return wrapper

    return decorator


def load_json(path: Path) -> dict:
    """Load JSON file"""
    with open(path, "r") as f:
        return json.load(f)


def parse_utc_datetime(value: str) -> datetime.datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)


def tt_add_op_name(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Add operation name for Train Ticket traces"""
    return lf.with_columns(pl.col("span_name").alias("operation_name"))


def replace_enum_values(column: str, enum_values: list, start: int = 0) -> pl.Expr:
    """Replace enum string values with integers"""
    mapping_expr = pl.col(column)
    for i, value in enumerate(enum_values):
        mapping_expr = mapping_expr.str.replace(value, str(start + i))
    return mapping_expr.cast(pl.Int32)


def load_inject_time(input_folder: Path) -> datetime.datetime:
    """Load injection time from environment configuration"""
    env = load_json(path=input_folder / "env.json")

    if "abnormal_start_time" in env:
        return parse_utc_datetime(str(env["abnormal_start_time"]))

    if "ABNORMAL_START" not in env and (input_folder / "injection.json").exists():
        injection = load_json(path=input_folder / "injection.json")
        if "start_time" in injection:
            return parse_utc_datetime(str(injection["start_time"]))

    normal_start = int(env["NORMAL_START"])
    normal_end = int(env["NORMAL_END"])
    abnormal_start = int(env["ABNORMAL_START"])
    abnormal_end = int(env["ABNORMAL_END"])

    assert normal_start < normal_end <= abnormal_start < abnormal_end

    if normal_end < abnormal_start:
        inject_time = int(math.ceil(normal_end + abnormal_start) / 2)
    else:
        inject_time = abnormal_start

    inject_time = datetime.datetime.fromtimestamp(inject_time, tz=datetime.timezone.utc)
    logger.debug(f"inject_time=`{inject_time}`")

    return inject_time


def merge_two_time_ranges(normal: pl.LazyFrame, anomal: pl.LazyFrame) -> pl.LazyFrame:
    """Merge normal and anomalous time ranges with anomaly flag"""
    assert "anomal" not in normal.collect_schema().names()
    assert "anomal" not in anomal.collect_schema().names()
    normal = normal.with_columns(anomal=pl.lit(0, dtype=pl.UInt8))
    anomal = anomal.with_columns(anomal=pl.lit(1, dtype=pl.UInt8))
    merged = pl.concat([normal, anomal])
    return merged


@timeit()
def load_metrics(input_folder: Path) -> pl.LazyFrame:
    """Load metrics data from parquet files"""
    normal_metrics = pl.scan_parquet(input_folder / "normal_metrics.parquet")
    anomal_metrics = pl.scan_parquet(input_folder / "abnormal_metrics.parquet")
    lf = merge_two_time_ranges(normal_metrics, anomal_metrics)
    return lf


def is_special_constant_metric(metric: str) -> bool:
    """Check if metric is a special constant metric"""
    return metric in (
        "k8s.container.cpu_request",
        "k8s.container.memory_request",
        "k8s.container.cpu_limit",
        "k8s.container.memory_limit",
    )


@timeit()
def load_metrics_histogram(input_folder: Path) -> pl.LazyFrame:
    """Load histogram metrics data"""
    normal_histogram = pl.scan_parquet(
        input_folder / "normal_metrics_histogram.parquet"
    )
    anomal_histogram = pl.scan_parquet(
        input_folder / "abnormal_metrics_histogram.parquet"
    )
    lf = merge_two_time_ranges(normal_histogram, anomal_histogram)

    lf = lf.with_columns(
        pl.when(pl.col("metric") == "jvm.gc.duration")
        .then(
            pl.concat_str("metric", "attr.jvm.gc.name", separator=":").alias("metric")
        )
        .otherwise(pl.col("metric"))
    )
    return lf


def ui_span_name_parser(df: pl.DataFrame) -> pl.DataFrame:
    """Parse UI dashboard span names by replacing with child span names"""
    # Create a mapping from parent span ID to child span name
    child_mapping = df.select(["parent_span_id", "span_name"]).rename(
        {"parent_span_id": "span_id", "span_name": "child_span_name"}
    )

    # Join with original dataframe
    merged_df = df.join(child_mapping, on="span_id", how="left")

    # Replace span names for ts-ui-dashboard service with child span names
    processed_df = merged_df.with_columns(
        pl.when(pl.col("service_name") == "ts-ui-dashboard")
        .then(pl.col("child_span_name"))
        .otherwise(pl.col("span_name"))
        .alias("span_name")
    ).drop("child_span_name")

    return processed_df


@timeit()
def load_traces(input_folder: Path) -> pl.LazyFrame:
    """Load trace data from parquet files"""
    normal_traces = pl.scan_parquet(input_folder / "normal_traces.parquet")
    anomal_traces = pl.scan_parquet(input_folder / "abnormal_traces.parquet")
    lf = merge_two_time_ranges(normal_traces, anomal_traces)

    optional_float_columns = [
        "attr.http.response.status_code",
        "attr.http.request.content_length",
        "attr.http.response.content_length",
    ]
    schema_names = lf.collect_schema().names()
    missing_columns = [name for name in optional_float_columns if name not in schema_names]
    if missing_columns:
        lf = lf.with_columns(
            [pl.lit(None).cast(pl.Float64).alias(name) for name in missing_columns]
        )

    status_code_values = ["Unset", "Ok", "Error"]
    lf = lf.with_columns(
        replace_enum_values("attr.status_code", status_code_values, start=0),
    )

    lf = lf.with_columns(
        pl.col("duration").cast(pl.Float64),
        pl.col("attr.http.response.status_code").cast(pl.Float64),
        pl.col("attr.http.request.content_length").cast(pl.Float64),
        pl.col("attr.http.response.content_length").cast(pl.Float64),
    )

    # Apply UI span name parsing
    df = lf.collect()
    df = ui_span_name_parser(df)

    lf = df.lazy()
    lf = tt_add_op_name(lf)

    return lf


@timeit()
def load_logs(input_folder: Path) -> pl.LazyFrame:
    """Load log data from parquet files"""
    normal_logs = pl.scan_parquet(input_folder / "normal_logs.parquet")
    anomal_logs = pl.scan_parquet(input_folder / "abnormal_logs.parquet")
    lf = merge_two_time_ranges(normal_logs, anomal_logs)

    level_values = ["", "TRACE", "DEBUG", "INFO", "WARN", "ERROR", "SEVERE"]
    lf = lf.with_columns(pl.col("level").str.replace("WARNING", "WARN", literal=True))
    lf = lf.with_columns(
        replace_enum_values("level", level_values, start=0).alias("level_number")
    )

    return lf


@timeit()
def load_metrics_sli(input_folder: Path) -> Optional[pl.LazyFrame]:
    """Load SLI metrics data from parquet file"""
    sli_path = input_folder / "metrics_sli.parquet"
    if not sli_path.exists():
        logger.warning("metrics_sli.parquet not found, skipping SLI data loading")
        return None

    try:
        lf = pl.scan_parquet(sli_path)
        logger.info("Loaded SLI metrics data")
        return lf
    except Exception as e:
        logger.error(f"Failed to load SLI metrics: {e}")
        return None


class DataLoader:
    """Data loader for MicroDig with Polars support"""

    def __init__(self, input_folder: Path):
        """Initialize data loader with input folder path"""
        self.input_folder = Path(input_folder)
        self.inject_time = load_inject_time(self.input_folder)
        logger.info(f"Data loader initialized for {self.input_folder}")

    def load_all_data(self) -> Dict[str, pl.LazyFrame]:
        """Load all data types (traces, metrics, logs, SLI)"""
        data = {}

        try:
            data["traces"] = load_traces(self.input_folder)
            logger.info("Loaded trace data")
        except Exception as e:
            logger.warning(f"Failed to load traces: {e}")
            data["traces"] = None

        try:
            data["metrics_sli"] = load_metrics_sli(self.input_folder)
            if data["metrics_sli"] is not None:
                logger.info("Loaded SLI metrics data")
        except Exception as e:
            logger.warning(f"Failed to load SLI metrics: {e}")
            data["metrics_sli"] = None

        return data

    def get_inject_time(self) -> datetime.datetime:
        """Get the injection time"""
        return self.inject_time

    def extract_calling_patterns(self, traces_lf: pl.LazyFrame) -> Dict[str, Any]:
        """Extract calling patterns from trace data for MicroDig"""
        logger.info("Extracting calling patterns from traces")

        # Convert to pandas for compatibility with existing MicroDig logic
        traces_df = traces_lf.collect().to_pandas()

        # Build span ID to service mapping
        span_to_service = {}
        for _, row in traces_df.iterrows():
            span_id = row.get("span_id")
            service_name = row.get("service_name", "")
            operation_name = row.get("operation_name", row.get("span_name", ""))
            if span_id:
                span_to_service[span_id] = {
                    "service": service_name,
                    "operation": operation_name,
                    "full_name": f"{service_name}|{operation_name}",
                }

        # Extract calling relationships based on parent-child span relationships
        calling_patterns = {}

        for _, row in traces_df.iterrows():
            span_id = row.get("span_id")
            parent_span_id = row.get("parent_span_id")
            service_name = row.get("service_name", "")
            operation_name = row.get("operation_name", row.get("span_name", ""))
            duration = row.get("duration", 0)
            is_abnormal = row.get("anomal", 0) == 1

            # Create calling relationship if parent exists
            if parent_span_id and parent_span_id in span_to_service:
                parent_info = span_to_service[parent_span_id]
                caller_service = parent_info["service"]
                caller_operation = parent_info["operation"]
                callee_service = service_name
                callee_operation = operation_name

                # Create calling key in format: caller_service|caller_operation|callee_service|callee_operation
                calling_key = f"{caller_service}|{caller_operation}|{callee_service}|{callee_operation}"

                # Also create a simplified service-level calling key
                service_calling_key = f"{caller_service}|{callee_service}"

                # Time-based grouping (minute level)
                timestamp = row.get("time", self.inject_time)
                if isinstance(timestamp, str):
                    timestamp = datetime.datetime.fromisoformat(
                        timestamp.replace("Z", "+00:00")
                    )
                time_minute = int(timestamp.timestamp() // 60)

                # Process method-level calling
                if calling_key not in calling_patterns:
                    calling_patterns[calling_key] = {
                        "name": calling_key,
                        "duration": {},
                        "normal_data": [],
                        "abnormal_data": [],
                        "error_min": {},
                        "request_min": {},
                        "error_rate": {},
                    }

                pattern = calling_patterns[calling_key]

                # Store data point
                data_point = {
                    "time_minute": time_minute,
                    "duration": duration / 1e6,  # Convert to milliseconds
                    "is_error": (
                        row.get("attr.status_code", 0) == 2  # Error status
                        or row.get("attr.http.response.status_code", 200) >= 400
                    ),
                }

                if is_abnormal:
                    pattern["abnormal_data"].append(data_point)
                else:
                    pattern["normal_data"].append(data_point)

                # Maintain time-based aggregation for compatibility
                if time_minute not in pattern["duration"]:
                    pattern["duration"][time_minute] = []
                pattern["duration"][time_minute].append(duration / 1e6)

                if time_minute not in pattern["request_min"]:
                    pattern["request_min"][time_minute] = 0
                pattern["request_min"][time_minute] += 1

                if time_minute not in pattern["error_min"]:
                    pattern["error_min"][time_minute] = 0
                if data_point["is_error"]:
                    pattern["error_min"][time_minute] += 1

            # Also create single-service patterns for completeness
            single_service_key = f"{service_name}|{operation_name}"
            if single_service_key not in calling_patterns:
                calling_patterns[single_service_key] = {
                    "name": single_service_key,
                    "duration": {},
                    "normal_data": [],
                    "abnormal_data": [],
                    "error_min": {},
                    "request_min": {},
                    "error_rate": {},
                }

            pattern = calling_patterns[single_service_key]

            # Time-based grouping (minute level)
            timestamp = row.get("time", self.inject_time)
            if isinstance(timestamp, str):
                timestamp = datetime.datetime.fromisoformat(
                    timestamp.replace("Z", "+00:00")
                )
            time_minute = int(timestamp.timestamp() // 60)

            # Store data point
            data_point = {
                "time_minute": time_minute,
                "duration": duration / 1e6,
                "is_error": (
                    row.get("attr.status_code", 0) == 2
                    or row.get("attr.http.response.status_code", 200) >= 400
                ),
            }

            if is_abnormal:
                pattern["abnormal_data"].append(data_point)
            else:
                pattern["normal_data"].append(data_point)

            # Maintain time-based aggregation
            if time_minute not in pattern["duration"]:
                pattern["duration"][time_minute] = []
            pattern["duration"][time_minute].append(duration / 1e6)

            if time_minute not in pattern["request_min"]:
                pattern["request_min"][time_minute] = 0
            pattern["request_min"][time_minute] += 1

            if time_minute not in pattern["error_min"]:
                pattern["error_min"][time_minute] = 0
            if data_point["is_error"]:
                pattern["error_min"][time_minute] += 1

        # Post-process: convert lists to averages and calculate statistics
        for pattern in calling_patterns.values():
            # Average durations
            for time_min in pattern["duration"]:
                durations = pattern["duration"][time_min]
                pattern["duration"][time_min] = (
                    sum(durations) / len(durations) if durations else 0
                )

            # Calculate error rates
            for time_min in pattern["error_min"]:
                error_count = pattern["error_min"][time_min]
                request_count = pattern["request_min"].get(time_min, 1)
                pattern["error_rate"][time_min] = (
                    error_count / request_count if request_count > 0 else 0
                )

            # Calculate normal vs abnormal statistics
            normal_durations = [d["duration"] for d in pattern["normal_data"]]
            abnormal_durations = [d["duration"] for d in pattern["abnormal_data"]]

            pattern["normal_avg_duration"] = (
                sum(normal_durations) / len(normal_durations) if normal_durations else 0
            )
            pattern["abnormal_avg_duration"] = (
                sum(abnormal_durations) / len(abnormal_durations)
                if abnormal_durations
                else 0
            )

            # Calculate anomaly score based on duration difference
            if pattern["normal_avg_duration"] > 0:
                pattern["duration_anomaly_score"] = (
                    abs(
                        pattern["abnormal_avg_duration"]
                        - pattern["normal_avg_duration"]
                    )
                    / pattern["normal_avg_duration"]
                )
            else:
                pattern["duration_anomaly_score"] = 0.0

        logger.info(
            f"Extracted {len(calling_patterns)} calling patterns with service relationships"
        )
        return calling_patterns

    def extract_calling_patterns_with_sli(
        self, traces_lf: Optional[pl.LazyFrame], sli_lf: Optional[pl.LazyFrame]
    ) -> Dict[str, Any]:
        """Extract calling patterns enhanced with SLI metrics data"""
        logger.info("Extracting calling patterns with SLI metrics enhancement")

        # Start with trace-based patterns if available
        if traces_lf is not None:
            calling_patterns = self.extract_calling_patterns(traces_lf)
        else:
            calling_patterns = {}

        # Enhance with SLI data if available
        if sli_lf is not None:
            sli_patterns = self._extract_sli_patterns(sli_lf)
            calling_patterns = self._merge_patterns_with_sli(
                calling_patterns, sli_patterns
            )

        return calling_patterns

    def _extract_sli_patterns(self, sli_lf: pl.LazyFrame) -> Dict[str, Any]:
        """Extract patterns from SLI metrics data"""
        logger.info("Extracting patterns from SLI metrics")

        sli_df = sli_lf.collect().to_pandas()
        sli_patterns = {}

        for _, row in sli_df.iterrows():
            service_name = row.get("service_name", "")
            span_name = row.get("span_name", "")
            timestamp = row.get("time")

            # Create pattern key (service|operation format)
            pattern_key = f"{service_name}|{span_name}"

            # Convert timestamp to minute-based key
            if isinstance(timestamp, str):
                timestamp = datetime.datetime.fromisoformat(
                    timestamp.replace("Z", "+00:00")
                )
            time_minute = int(timestamp.timestamp() // 60)

            # Initialize pattern if not exists
            if pattern_key not in sli_patterns:
                sli_patterns[pattern_key] = {
                    "name": pattern_key,
                    "service_name": service_name,
                    "span_name": span_name,
                    "duration": {},
                    "error_rate": {},
                    "request_min": {},
                    "error_min": {},
                    "sli_data": {},
                }

            pattern = sli_patterns[pattern_key]

            # Extract SLI metrics
            avg_duration = row.get("avg_duration", 0)
            total_count = row.get("total_count", 0)
            error_count = row.get("error_count", 0)

            # Store aggregated metrics
            pattern["duration"][time_minute] = avg_duration
            pattern["request_min"][time_minute] = total_count
            pattern["error_min"][time_minute] = error_count
            pattern["error_rate"][time_minute] = (
                error_count / total_count if total_count > 0 else 0
            )

            # Store detailed SLI data for advanced analysis
            pattern["sli_data"][time_minute] = {
                "min_duration": row.get("min_duration", 0),
                "max_duration": row.get("max_duration", 0),
                "avg_duration": avg_duration,
                "duration_p50": row.get("duration_p50", 0),
                "duration_p90": row.get("duration_p90", 0),
                "duration_p95": row.get("duration_p95", 0),
                "duration_p99": row.get("duration_p99", 0),
                "total_count": total_count,
                "error_count": error_count,
            }

        logger.info(f"Extracted {len(sli_patterns)} SLI-based patterns")
        return sli_patterns

    def _merge_patterns_with_sli(
        self, trace_patterns: Dict[str, Any], sli_patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge trace-based patterns with SLI patterns"""
        logger.info("Merging trace patterns with SLI patterns")

        merged_patterns = trace_patterns.copy()

        # Add SLI patterns and enhance existing ones
        for sli_key, sli_pattern in sli_patterns.items():
            service_name = sli_pattern["service_name"]
            span_name = sli_pattern["span_name"]

            # Try to find matching trace pattern
            matching_trace_key = None
            for trace_key in trace_patterns.keys():
                if service_name in trace_key and span_name in trace_key:
                    matching_trace_key = trace_key
                    break

            if matching_trace_key:
                # Enhance existing trace pattern with SLI data
                trace_pattern = merged_patterns[matching_trace_key]

                # Add SLI data to existing pattern
                trace_pattern["sli_data"] = sli_pattern["sli_data"]

                # Override with more accurate SLI metrics where available
                for time_minute, sli_metrics in sli_pattern["sli_data"].items():
                    if time_minute not in trace_pattern["duration"]:
                        trace_pattern["duration"][time_minute] = sli_metrics[
                            "avg_duration"
                        ]
                        trace_pattern["request_min"][time_minute] = sli_metrics[
                            "total_count"
                        ]
                        trace_pattern["error_min"][time_minute] = sli_metrics[
                            "error_count"
                        ]
                        trace_pattern["error_rate"][time_minute] = (
                            sli_metrics["error_count"] / sli_metrics["total_count"]
                            if sli_metrics["total_count"] > 0
                            else 0
                        )
                    else:
                        # Use SLI data as it's more accurate for aggregated metrics
                        trace_pattern["duration"][time_minute] = sli_metrics[
                            "avg_duration"
                        ]
                        trace_pattern["error_rate"][time_minute] = (
                            sli_metrics["error_count"] / sli_metrics["total_count"]
                            if sli_metrics["total_count"] > 0
                            else 0
                        )

                logger.debug(
                    f"Enhanced trace pattern {matching_trace_key} with SLI data"
                )
            else:
                # Add new SLI-only pattern
                merged_patterns[sli_key] = sli_pattern
                logger.debug(f"Added new SLI pattern {sli_key}")

        logger.info(f"Merged patterns: {len(merged_patterns)} total patterns")
        return merged_patterns
