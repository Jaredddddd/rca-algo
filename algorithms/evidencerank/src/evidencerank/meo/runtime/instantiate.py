"""Runtime instantiation of MEOL operators into feature and role matrices."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from ..dsl.compiler import EvidenceCompiler
from ..dsl.schema import EvidenceOperatorSpec


ROLE_ORDER = ["mutation", "propagation", "observability_bias", "topology_context"]


def _clean_feature_values(values: np.ndarray, size: int) -> np.ndarray:
    try:
        arr = np.asarray(values, dtype=np.float64).reshape(-1)
    except (TypeError, ValueError):
        arr = np.zeros(size, dtype=np.float64)
    if arr.size != size:
        resized = np.zeros(size, dtype=np.float64)
        copy_len = min(size, arr.size)
        if copy_len:
            resized[:copy_len] = arr[:copy_len]
        arr = resized
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    return np.maximum(arr, 0.0)


def _role_weights(spec: EvidenceOperatorSpec) -> list[float]:
    raw = [float(spec.role_prior.get(role, 0.0)) for role in ROLE_ORDER]
    clean = [value if math.isfinite(value) and value > 0.0 else 0.0 for value in raw]
    total = sum(clean)
    if total <= 1e-12:
        return [0.0 for _role in ROLE_ORDER]
    return [value / total for value in clean]


def instantiate_meol_features(
    frames: dict[str, pd.DataFrame],
    services: list[str],
    specs: list[EvidenceOperatorSpec],
    compiler: EvidenceCompiler | None = None,
) -> tuple[np.ndarray, tuple[str, ...], np.ndarray]:
    """Compile and execute MEOL operators against one incident's telemetry."""

    compiler = compiler or EvidenceCompiler()
    feature_values: list[np.ndarray] = []
    feature_names: list[str] = []
    role_weights: list[list[float]] = []

    for spec in specs:
        try:
            feature_fn = compiler.compile(spec)
            values = feature_fn(frames, services)
        except Exception:
            values = np.zeros(len(services), dtype=np.float64)
        feature_values.append(_clean_feature_values(values, len(services)))
        feature_names.append(spec.name)
        role_weights.append(_role_weights(spec))

    if feature_values:
        feature_matrix = np.stack(feature_values, axis=1).astype(np.float64, copy=False)
        role_weight_matrix = np.asarray(role_weights, dtype=np.float64)
    else:
        feature_matrix = np.zeros((len(services), 0), dtype=np.float64)
        role_weight_matrix = np.zeros((0, len(ROLE_ORDER)), dtype=np.float64)

    return feature_matrix, tuple(feature_names), role_weight_matrix

