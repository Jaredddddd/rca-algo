"""Dynamic execution checks for EvidenceOperatorSpec objects."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from ..dsl.compiler import EvidenceCompiler
from ..dsl.schema import EvidenceOperatorSpec


def dynamic_verify(
    spec: EvidenceOperatorSpec,
    frames: dict[str, pd.DataFrame],
    services: list[str],
    compiler: EvidenceCompiler | None = None,
) -> tuple[bool, dict[str, float]]:
    """Execute one operator and report basic feature quality statistics."""

    compiler = compiler or EvidenceCompiler()
    try:
        feature_fn = compiler.compile(spec)
        values = np.asarray(feature_fn(frames, services), dtype=np.float64)
    except Exception:
        return False, {
            "compile_or_runtime_error": 1.0,
            "nan_rate": 1.0,
            "nonzero_rate": 0.0,
            "variance": 0.0,
            "max": 0.0,
        }

    if values.size == 0:
        return False, {
            "nan_rate": 1.0,
            "nonzero_rate": 0.0,
            "variance": 0.0,
            "max": 0.0,
        }

    finite_values = np.nan_to_num(values, nan=0.0, posinf=0.0, neginf=0.0)
    stats = {
        "nan_rate": float(np.isnan(values).mean()),
        "nonzero_rate": float((finite_values > 0.0).mean()),
        "variance": float(np.var(finite_values)),
        "max": float(np.max(finite_values)),
    }
    stats = {
        key: value if math.isfinite(value) else 0.0
        for key, value in stats.items()
    }
    ok = stats["nan_rate"] <= 0.1 and stats["variance"] > 1e-12
    return ok, stats

