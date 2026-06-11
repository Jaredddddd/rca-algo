"""Compiler from MEOL operator specs to deterministic feature functions."""

from __future__ import annotations

import math
from collections.abc import Iterable
from typing import Callable, Any

import numpy as np
import pandas as pd

from .atoms import (
    count_delta,
    count_drop,
    count_rise,
    error_rate_delta,
    js_divergence,
    mean_delta,
    robust_z_shift,
    z_shift,
)
from .schema import EvidenceOperatorSpec


FeatureFn = Callable[[dict[str, pd.DataFrame], list[str]], np.ndarray]

ROW_COUNT_FIELDS = {"__row_count__", "**row_count**", "row_count"}
TIME_COLUMNS = {"time", "timestamp", "datetime", "date"}
SERVICE_ALIASES = (
    "service_name",
    "service",
    "svc",
    "instance",
    "attr.k8s.container.name",
    "attr.k8s.deployment.name",
    "attr.k8s.statefulset.name",
    "attr.k8s.pod.name",
)
TRACE_ENDPOINT_ALIASES = (
    "endpoint",
    "operation",
    "operation_name",
    "span_name",
    "http_route",
    "route",
    "attr.http.route",
)
TRACE_STATUS_ALIASES = (
    "status_code",
    "http_status_code",
    "http.status_code",
    "attr.http.response.status_code",
    "attr.status_code",
    "status",
    "code",
)
TRACE_DURATION_ALIASES = (
    "duration",
    "duration_ms",
    "latency",
    "elapsed",
    "elapsed_ms",
)
LOG_TEMPLATE_ALIASES = (
    "template",
    "log_template",
    "message_template",
    "event_template",
)
LOG_LEVEL_ALIASES = ("level", "severity", "log_level")
LOG_MESSAGE_ALIASES = ("message", "msg", "body", "content", "log")


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null"}:
        return None
    return text


def _finite_nonnegative_array(values: Iterable[Any], length: int) -> np.ndarray:
    try:
        arr = np.asarray(list(values), dtype=np.float64)
    except (TypeError, ValueError):
        arr = np.zeros(length, dtype=np.float64)
    if arr.shape != (length,):
        clean = np.zeros(length, dtype=np.float64)
        copy_len = min(length, int(arr.size))
        if copy_len:
            clean[:copy_len] = arr.reshape(-1)[:copy_len]
        arr = clean
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    return np.maximum(arr, 0.0)


class EvidenceCompiler:
    """Compile verified EvidenceOperatorSpec objects into feature functions."""

    def __init__(self) -> None:
        self._service_group_cache: dict[
            tuple[int, int, tuple[str, ...], str],
            tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]] | None,
        ] = {}

    def compile(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        if spec.source == "metric":
            return self._compile_metric(spec)
        if spec.source == "trace":
            return self._compile_trace(spec)
        if spec.source == "log":
            return self._compile_log(spec)
        if spec.source == "topology":
            return self._compile_topology(spec)
        raise ValueError(f"Unsupported source: {spec.source}")

    def _compile_metric(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        op = spec.contrast.operator
        field = spec.signal.field

        def feature(frames: dict[str, pd.DataFrame], services: list[str]) -> np.ndarray:
            normal = frames.get("normal_metrics", pd.DataFrame())
            abnormal = frames.get("abnormal_metrics", pd.DataFrame())
            grouped = self._service_frame_groups(normal, abnormal, services, source="metric")
            out: list[float] = []
            for service in services:
                if grouped is not None:
                    normal_groups, abnormal_groups = grouped
                    n_service = normal_groups.get(service, pd.DataFrame(columns=normal.columns))
                    a_service = abnormal_groups.get(service, pd.DataFrame(columns=abnormal.columns))
                    if field in ROW_COUNT_FIELDS:
                        out.append(self._apply_count_op(op, float(len(n_service)), float(len(a_service))))
                        continue
                    out.append(
                        self._metric_numeric_score_from_service_frames(
                            n_service,
                            a_service,
                            field,
                            op,
                            spec,
                        )
                    )
                    continue
                if field in ROW_COUNT_FIELDS:
                    out.append(
                        self._apply_count_op(
                            op,
                            self._service_metric_row_count(normal, service),
                            self._service_metric_row_count(abnormal, service),
                        )
                    )
                    continue
                out.append(self._metric_numeric_score(normal, abnormal, service, field, op, spec))
            return _finite_nonnegative_array(out, len(services))

        return feature

    def _metric_numeric_score_from_service_frames(
        self,
        normal_service: pd.DataFrame,
        abnormal_service: pd.DataFrame,
        field: str,
        op: str,
        spec: EvidenceOperatorSpec,
    ) -> float:
        value_col_n = self._find_col(normal_service, ("value", "metric_value", "val"))
        value_col_a = self._find_col(abnormal_service, ("value", "metric_value", "val"))
        if value_col_n is None or value_col_a is None:
            return 0.0

        metric_col_n = self._find_col(normal_service, ("metric", "metric_name", "name"))
        metric_col_a = self._find_col(abnormal_service, ("metric", "metric_name", "name"))
        if field == "*" or metric_col_n is None or metric_col_a is None:
            return self._apply_field_op(op, normal_service[value_col_n], abnormal_service[value_col_a])

        n_names = normal_service[metric_col_n].map(_clean_text)
        a_names = abnormal_service[metric_col_a].map(_clean_text)
        names = sorted((set(n_names.dropna()) | set(a_names.dropna())) & {field})
        if not names:
            names = sorted(
                name
                for name in (set(n_names.dropna()) | set(a_names.dropna()))
                if field in str(name)
            )
        return self._aggregate_scores(
            [
                self._apply_field_op(
                    op,
                    normal_service.loc[n_names == name, value_col_n],
                    abnormal_service.loc[a_names == name, value_col_a],
                )
                for name in names
            ],
            spec.aggregation.method,
        )

    def _metric_numeric_score(
        self,
        normal: pd.DataFrame,
        abnormal: pd.DataFrame,
        service: str,
        field: str,
        op: str,
        spec: EvidenceOperatorSpec,
    ) -> float:
        long_scores = self._long_metric_scores(normal, abnormal, service, field, op)
        wide_scores = [
            self._apply_field_op(
                op,
                normal[column] if column in normal.columns else pd.Series(dtype="float64"),
                abnormal[column] if column in abnormal.columns else pd.Series(dtype="float64"),
            )
            for column in self._metric_columns_for_service(normal, abnormal, service, field)
        ]
        return self._aggregate_scores([*long_scores, *wide_scores], spec.aggregation.method)

    def _long_metric_scores(
        self,
        normal: pd.DataFrame,
        abnormal: pd.DataFrame,
        service: str,
        field: str,
        op: str,
    ) -> list[float]:
        service_col_n = self._find_col(normal, SERVICE_ALIASES)
        service_col_a = self._find_col(abnormal, SERVICE_ALIASES)
        value_col_n = self._find_col(normal, ("value", "metric_value", "val"))
        value_col_a = self._find_col(abnormal, ("value", "metric_value", "val"))
        if (
            service_col_n is None
            or service_col_a is None
            or value_col_n is None
            or value_col_a is None
        ):
            return []

        n_service = self._filter_service(normal, service_col_n, service)
        a_service = self._filter_service(abnormal, service_col_a, service)
        metric_col_n = self._find_col(n_service, ("metric", "metric_name", "name"))
        metric_col_a = self._find_col(a_service, ("metric", "metric_name", "name"))
        if field == "*" or metric_col_n is None or metric_col_a is None:
            return [self._apply_field_op(op, n_service[value_col_n], a_service[value_col_a])]

        n_names = n_service[metric_col_n].map(_clean_text)
        a_names = a_service[metric_col_a].map(_clean_text)
        exact_names = sorted((set(n_names.dropna()) | set(a_names.dropna())) & {field})
        names = exact_names or sorted(
            name
            for name in (set(n_names.dropna()) | set(a_names.dropna()))
            if field in str(name)
        )
        return [
            self._apply_field_op(
                op,
                n_service.loc[n_names == name, value_col_n],
                a_service.loc[a_names == name, value_col_a],
            )
            for name in names
        ]

    def _metric_columns_for_service(
        self,
        normal: pd.DataFrame,
        abnormal: pd.DataFrame,
        service: str,
        field: str,
    ) -> list[str]:
        cols = {
            str(column)
            for column in [*normal.columns, *abnormal.columns]
            if str(column).lower() not in TIME_COLUMNS
        }
        prefixes = (f"{service}_", f"{service}.", f"{service}/")
        if field == "*":
            return sorted(column for column in cols if column.startswith(prefixes))
        direct_candidates = {f"{service}_{field}", f"{service}.{field}", f"{service}/{field}"}
        direct = sorted(column for column in cols if column in direct_candidates)
        if direct:
            return direct
        return sorted(
            column
            for column in cols
            if column.startswith(prefixes) and field in column
        )

    def _service_metric_row_count(self, frame: pd.DataFrame, service: str) -> float:
        if frame is None or frame.empty:
            return 0.0
        service_col = self._find_col(frame, SERVICE_ALIASES)
        if service_col is not None:
            return float(len(self._filter_service(frame, service_col, service)))
        cols = self._metric_columns_for_service(frame, frame, service, "*")
        if not cols:
            return 0.0
        return float(frame[cols].dropna(how="all").shape[0])

    def _compile_trace(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        op = spec.contrast.operator
        field = spec.signal.field

        def feature(frames: dict[str, pd.DataFrame], services: list[str]) -> np.ndarray:
            normal = frames.get("normal_traces", pd.DataFrame())
            abnormal = frames.get("abnormal_traces", pd.DataFrame())
            grouped = self._service_frame_groups(normal, abnormal, services, source="trace")
            if grouped is None:
                return np.zeros(len(services), dtype=np.float64)
            normal_groups, abnormal_groups = grouped

            out: list[float] = []
            for service in services:
                n_service = normal_groups.get(service, pd.DataFrame(columns=normal.columns))
                a_service = abnormal_groups.get(service, pd.DataFrame(columns=abnormal.columns))
                if field in ROW_COUNT_FIELDS:
                    out.append(self._apply_count_op(op, float(len(n_service)), float(len(a_service))))
                    continue

                n_field = self._resolve_trace_field(n_service, field)
                a_field = self._resolve_trace_field(a_service, field)
                if n_field is None or a_field is None:
                    out.append(0.0)
                elif op == "distribution_shift":
                    out.append(self._categorical_distribution_shift(n_service[n_field], a_service[a_field]))
                elif op == "error_rate_delta":
                    out.append(error_rate_delta(n_service[n_field], a_service[a_field]))
                else:
                    out.append(self._apply_field_op(op, n_service[n_field], a_service[a_field]))
            return _finite_nonnegative_array(out, len(services))

        return feature

    def _compile_log(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        op = spec.contrast.operator
        field = spec.signal.field

        def feature(frames: dict[str, pd.DataFrame], services: list[str]) -> np.ndarray:
            normal = frames.get("normal_logs", pd.DataFrame())
            abnormal = frames.get("abnormal_logs", pd.DataFrame())
            grouped = self._service_frame_groups(normal, abnormal, services, source="log")
            if grouped is None:
                return np.zeros(len(services), dtype=np.float64)
            normal_groups, abnormal_groups = grouped

            out: list[float] = []
            for service in services:
                n_service = normal_groups.get(service, pd.DataFrame(columns=normal.columns))
                a_service = abnormal_groups.get(service, pd.DataFrame(columns=abnormal.columns))
                if field in ROW_COUNT_FIELDS:
                    out.append(self._apply_count_op(op, float(len(n_service)), float(len(a_service))))
                    continue

                n_field = self._resolve_log_field(n_service, field)
                a_field = self._resolve_log_field(a_service, field)
                if n_field is None or a_field is None or op != "distribution_shift":
                    out.append(0.0)
                else:
                    out.append(self._categorical_distribution_shift(n_service[n_field], a_service[a_field]))
            return _finite_nonnegative_array(out, len(services))

        return feature

    def _compile_topology(self, _spec: EvidenceOperatorSpec) -> FeatureFn:
        def feature(_frames: dict[str, pd.DataFrame], services: list[str]) -> np.ndarray:
            return np.zeros(len(services), dtype=np.float64)

        return feature

    def _find_col(self, frame: pd.DataFrame, candidates: Iterable[str]) -> str | None:
        if frame is None:
            return None
        lower_to_original = {str(column).lower(): str(column) for column in frame.columns}
        for candidate in candidates:
            column = lower_to_original.get(str(candidate).lower())
            if column is not None:
                return column
        return None

    def _filter_service(self, frame: pd.DataFrame, service_col: str, service: str) -> pd.DataFrame:
        if frame is None or frame.empty or service_col not in frame.columns:
            return pd.DataFrame(columns=[] if frame is None else frame.columns)
        normalized = frame[service_col].map(_clean_text)
        return frame.loc[normalized == str(service)]

    def _service_frame_groups(
        self,
        normal: pd.DataFrame,
        abnormal: pd.DataFrame,
        services: list[str],
        *,
        source: str,
    ) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]] | None:
        service_col_n = self._find_col(normal, SERVICE_ALIASES)
        service_col_a = self._find_col(abnormal, SERVICE_ALIASES)
        if service_col_n is None or service_col_a is None:
            return None

        key = (id(normal), id(abnormal), tuple(services), source)
        cached = self._service_group_cache.get(key)
        if cached is not None:
            return cached

        service_set = set(services)

        def build(frame: pd.DataFrame, service_col: str) -> dict[str, pd.DataFrame]:
            if frame is None or frame.empty or service_col not in frame.columns:
                return {}
            working = frame.copy()
            working["_meo_service_name"] = working[service_col].map(_clean_text)
            working = working.loc[working["_meo_service_name"].isin(service_set)]
            if working.empty:
                return {}
            return {
                str(service): group.drop(columns=["_meo_service_name"])
                for service, group in working.groupby("_meo_service_name", sort=False)
            }

        grouped = (build(normal, service_col_n), build(abnormal, service_col_a))
        self._service_group_cache[key] = grouped
        return grouped

    def _resolve_trace_field(self, frame: pd.DataFrame, field: str) -> str | None:
        aliases = {
            "endpoint": TRACE_ENDPOINT_ALIASES,
            "status_code": TRACE_STATUS_ALIASES,
            "duration": TRACE_DURATION_ALIASES,
        }
        return self._find_col(frame, aliases.get(field, (field,)))

    def _resolve_log_field(self, frame: pd.DataFrame, field: str) -> str | None:
        aliases = {
            "template": LOG_TEMPLATE_ALIASES,
            "level": LOG_LEVEL_ALIASES,
            "message": LOG_MESSAGE_ALIASES,
        }
        return self._find_col(frame, aliases.get(field, (field,)))

    def _categorical_distribution_shift(self, normal_values: pd.Series, abnormal_values: pd.Series) -> float:
        normal = pd.Series(normal_values).dropna().map(str)
        abnormal = pd.Series(abnormal_values).dropna().map(str)
        categories = sorted(set(normal.unique()) | set(abnormal.unique()))
        if not categories:
            return 0.0
        p = np.asarray([(normal == category).sum() for category in categories], dtype=np.float64)
        q = np.asarray([(abnormal == category).sum() for category in categories], dtype=np.float64)
        return js_divergence(p, q)

    def _apply_field_op(self, op: str, normal_values: pd.Series, abnormal_values: pd.Series) -> float:
        if op == "z_shift":
            return z_shift(normal_values, abnormal_values)
        if op == "robust_z_shift":
            return robust_z_shift(normal_values, abnormal_values)
        if op == "mean_delta":
            return mean_delta(normal_values, abnormal_values)
        if op == "count_delta":
            return count_delta(pd.Series(normal_values).dropna().shape[0], pd.Series(abnormal_values).dropna().shape[0])
        if op == "count_rise":
            return count_rise(pd.Series(normal_values).dropna().shape[0], pd.Series(abnormal_values).dropna().shape[0])
        if op == "count_drop":
            return count_drop(pd.Series(normal_values).dropna().shape[0], pd.Series(abnormal_values).dropna().shape[0])
        raise ValueError(f"Unsupported field operator: {op}")

    def _apply_count_op(self, op: str, normal_count: float, abnormal_count: float) -> float:
        if op == "count_delta":
            return count_delta(normal_count, abnormal_count)
        if op == "count_rise":
            return count_rise(normal_count, abnormal_count)
        if op == "count_drop":
            return count_drop(normal_count, abnormal_count)
        raise ValueError(f"Unsupported count operator: {op}")

    def _aggregate_scores(self, scores: list[float], method: str) -> float:
        clean = np.asarray(
            [score for score in scores if math.isfinite(float(score)) and float(score) > 0.0],
            dtype=np.float64,
        )
        if clean.size == 0:
            return 0.0
        if method == "mean":
            return float(np.mean(clean))
        if method == "sum":
            return float(np.sum(clean))
        if method == "p95":
            return float(np.percentile(clean, 95))
        return float(np.max(clean))
