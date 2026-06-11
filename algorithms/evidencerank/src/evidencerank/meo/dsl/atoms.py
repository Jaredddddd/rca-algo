"""Robust primitive contrast atoms for CREST-MEO operators."""

from __future__ import annotations

import math
from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


EPS = 1e-9


def finite_series(values: pd.Series | np.ndarray | Iterable[Any]) -> np.ndarray:
    """Return a finite float64 array, coercing invalid numeric values to zero."""

    if values is None:
        return np.asarray([], dtype=np.float64)
    try:
        series = pd.Series(values)
        numeric = pd.to_numeric(series, errors="coerce")
        arr = numeric.to_numpy(dtype=np.float64, copy=False)
    except (TypeError, ValueError):
        return np.asarray([], dtype=np.float64)
    return np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)


def _finite_nonnegative(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(numeric) or numeric <= 0.0:
        return 0.0
    return numeric


def _safe_max(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    return _finite_nonnegative(np.max(values))


def z_shift(
    normal: pd.Series | np.ndarray | Iterable[Any],
    abnormal: pd.Series | np.ndarray | Iterable[Any],
) -> float:
    """Maximum absolute z shift of abnormal values against normal values."""

    normal_arr = finite_series(normal)
    abnormal_arr = finite_series(abnormal)
    if normal_arr.size == 0 or abnormal_arr.size == 0:
        return 0.0

    sigma = float(np.std(normal_arr))
    if not math.isfinite(sigma) or sigma <= EPS:
        return 0.0
    mu = float(np.mean(normal_arr))
    return _safe_max(np.abs((abnormal_arr - mu) / (sigma + EPS)))


def robust_z_shift(
    normal: pd.Series | np.ndarray | Iterable[Any],
    abnormal: pd.Series | np.ndarray | Iterable[Any],
) -> float:
    """Maximum robust z shift using the normal median and IQR."""

    normal_arr = finite_series(normal)
    abnormal_arr = finite_series(abnormal)
    if normal_arr.size == 0 or abnormal_arr.size == 0:
        return 0.0

    median = float(np.median(normal_arr))
    q75 = float(np.percentile(normal_arr, 75))
    q25 = float(np.percentile(normal_arr, 25))
    iqr = q75 - q25
    if not math.isfinite(iqr) or iqr <= EPS:
        return 0.0
    return _safe_max(np.abs((abnormal_arr - median) / (iqr + EPS)))


def mean_delta(
    normal: pd.Series | np.ndarray | Iterable[Any],
    abnormal: pd.Series | np.ndarray | Iterable[Any],
) -> float:
    """Absolute relative mean shift."""

    normal_arr = finite_series(normal)
    abnormal_arr = finite_series(abnormal)
    if normal_arr.size == 0 or abnormal_arr.size == 0:
        return 0.0

    normal_mean = float(np.mean(normal_arr))
    abnormal_mean = float(np.mean(abnormal_arr))
    delta = abs(abnormal_mean - normal_mean) / (abs(normal_mean) + EPS)
    return _finite_nonnegative(delta)


def _clean_count(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(numeric) or numeric <= 0.0:
        return 0.0
    return numeric


def count_delta(normal_count: float, abnormal_count: float) -> float:
    """Absolute relative count change."""

    normal_clean = _clean_count(normal_count)
    abnormal_clean = _clean_count(abnormal_count)
    return _finite_nonnegative(abs(abnormal_clean - normal_clean) / (normal_clean + EPS))


def count_rise(normal_count: float, abnormal_count: float) -> float:
    """Relative count increase."""

    normal_clean = _clean_count(normal_count)
    abnormal_clean = _clean_count(abnormal_count)
    return _finite_nonnegative(max(0.0, abnormal_clean - normal_clean) / (normal_clean + EPS))


def count_drop(normal_count: float, abnormal_count: float) -> float:
    """Relative count decrease."""

    normal_clean = _clean_count(normal_count)
    abnormal_clean = _clean_count(abnormal_count)
    return _finite_nonnegative(max(0.0, normal_clean - abnormal_clean) / (normal_clean + EPS))


def js_divergence(p: np.ndarray | Iterable[Any], q: np.ndarray | Iterable[Any]) -> float:
    """Jensen-Shannon divergence for two non-negative count vectors."""

    p_arr = np.maximum(finite_series(p), 0.0)
    q_arr = np.maximum(finite_series(q), 0.0)
    size = max(p_arr.size, q_arr.size)
    if size == 0:
        return 0.0
    if p_arr.size < size:
        p_arr = np.pad(p_arr, (0, size - p_arr.size))
    if q_arr.size < size:
        q_arr = np.pad(q_arr, (0, size - q_arr.size))
    if float(np.sum(p_arr)) <= EPS and float(np.sum(q_arr)) <= EPS:
        return 0.0

    p_prob = p_arr / (float(np.sum(p_arr)) + EPS)
    q_prob = q_arr / (float(np.sum(q_arr)) + EPS)
    midpoint = 0.5 * (p_prob + q_prob)

    def kl_divergence(left: np.ndarray, right: np.ndarray) -> float:
        mask = left > EPS
        if not bool(np.any(mask)):
            return 0.0
        value = float(np.sum(left[mask] * np.log((left[mask] + EPS) / (right[mask] + EPS))))
        return value if math.isfinite(value) else 0.0

    score = 0.5 * kl_divergence(p_prob, midpoint) + 0.5 * kl_divergence(q_prob, midpoint)
    return _finite_nonnegative(score)


def is_error_status(value: Any) -> bool:
    """Return whether a status-like value represents an error."""

    try:
        return int(float(value)) >= 400
    except (TypeError, ValueError):
        text = str(value).strip().lower()
        if not text or text in {"nan", "none", "null"}:
            return False
        return (
            "error" in text
            or "fail" in text
            or "timeout" in text
            or text.startswith("4")
            or text.startswith("5")
            or text == "true"
        )


def error_rate(values: pd.Series | np.ndarray | Iterable[Any]) -> float:
    """Fraction of status-like values that are errors."""

    if values is None:
        return 0.0
    items = list(values)
    if not items:
        return 0.0
    errors = sum(1 for value in items if is_error_status(value))
    return _finite_nonnegative(float(errors) / float(len(items)))


def error_rate_delta(
    normal_values: pd.Series | np.ndarray | Iterable[Any],
    abnormal_values: pd.Series | np.ndarray | Iterable[Any],
) -> float:
    """Absolute change in error status rate."""

    return _finite_nonnegative(abs(error_rate(abnormal_values) - error_rate(normal_values)))

