from __future__ import annotations

import math

import numpy as np
import pandas as pd

from evidencerank.crest import score_crest_services
from evidencerank.meo.dsl.atoms import (
    count_drop,
    count_rise,
    finite_series,
    js_divergence,
    robust_z_shift,
    z_shift,
)
from evidencerank.meo.dsl.compiler import EvidenceCompiler
from evidencerank.meo.runtime.instantiate import instantiate_meol_features
from evidencerank.meo.runtime.load_meol import DEFAULT_MEOL_PATH, load_operator_specs
from meo.llm.synthesize import main as synthesize_main


def _trace_frames() -> dict[str, pd.DataFrame]:
    return {
        "normal_traces": pd.DataFrame(
            {
                "service_name": ["a", "a", "b", "b"],
                "status_code": [200, 200, 200, 200],
                "endpoint": ["/x", "/x", "/y", "/y"],
                "duration": [10.0, 11.0, 9.0, 10.0],
            }
        ),
        "abnormal_traces": pd.DataFrame(
            {
                "service_name": ["a", "a", "b", "b"],
                "status_code": [500, 500, 200, 200],
                "endpoint": ["/x", "/z", "/y", "/y"],
                "duration": [80.0, 90.0, 9.0, 10.0],
            }
        ),
        "normal_metrics": pd.DataFrame(),
        "abnormal_metrics": pd.DataFrame(),
        "normal_logs": pd.DataFrame(),
        "abnormal_logs": pd.DataFrame(),
    }


def test_atoms_return_finite_nonnegative_values() -> None:
    arr = finite_series(np.asarray([1.0, np.nan, np.inf, -np.inf]))
    assert np.all(np.isfinite(arr))
    assert z_shift([1.0, 2.0, 3.0], [7.0]) >= 0.0
    assert robust_z_shift([1.0, 2.0, 3.0, 4.0], [10.0]) >= 0.0
    assert count_drop(100.0, 50.0) > 0.0
    assert count_drop(50.0, 100.0) == 0.0
    assert count_rise(50.0, 100.0) > 0.0
    assert count_rise(100.0, 50.0) == 0.0
    assert js_divergence(np.asarray([1.0, 2.0]), np.asarray([1.0, 2.0])) < 1e-6


def test_compiler_trace_status_shift_detects_changed_service() -> None:
    spec = next(
        spec
        for spec in load_operator_specs(DEFAULT_MEOL_PATH)
        if spec.name == "trace_status_code_shift"
    )
    values = EvidenceCompiler().compile(spec)(_trace_frames(), ["a", "b"])
    assert values.shape == (2,)
    assert np.all(np.isfinite(values))
    assert np.all(values >= 0.0)
    assert values[0] > values[1]


def test_instantiate_default_meol_returns_finite_matrix_and_roles() -> None:
    specs = load_operator_specs(DEFAULT_MEOL_PATH)
    matrix, names, role_weights = instantiate_meol_features(
        _trace_frames(),
        ["a", "b"],
        specs,
    )
    assert matrix.shape == (2, len(specs))
    assert role_weights.shape == (len(specs), 4)
    assert "trace_status_code_shift" in names
    assert np.all(np.isfinite(matrix))
    assert np.all(matrix >= 0.0)
    assert np.all(np.isfinite(role_weights))
    assert np.all(role_weights >= 0.0)
    assert np.allclose(role_weights.sum(axis=1), 1.0)


def test_operator_failure_returns_zero_column() -> None:
    class FailingCompiler(EvidenceCompiler):
        def compile(self, spec):  # type: ignore[no-untyped-def]
            raise RuntimeError(spec.name)

    specs = load_operator_specs(DEFAULT_MEOL_PATH)[:1]
    matrix, names, role_weights = instantiate_meol_features(
        _trace_frames(),
        ["a", "b"],
        specs,
        compiler=FailingCompiler(),
    )
    assert names == (specs[0].name,)
    assert matrix.tolist() == [[0.0], [0.0]]
    assert role_weights.shape == (1, 4)


def test_score_crest_services_with_meo_smoke(tmp_path) -> None:
    frames = _trace_frames()
    for name, frame in frames.items():
        frame.to_parquet(tmp_path / f"{name}.parquet")

    ranking = score_crest_services(tmp_path, use_meo=True)
    assert list(ranking.columns) == ["service", "A", "F", "S", "score"]
    assert ranking.iloc[0]["service"] == "a"
    assert math.isfinite(float(ranking.iloc[0]["score"]))
    assert float(ranking.iloc[0]["score"]) > 0.0


def test_config_driven_mock_synthesis_cli(tmp_path) -> None:
    output = tmp_path / "mock_meol.json"
    synthesize_main(["--mock", "--output", str(output)])
    specs = load_operator_specs(output)
    assert len(specs) == 10
    assert {spec.name for spec in specs} >= {
        "metric_max_z",
        "trace_status_code_shift",
        "log_template_delta",
    }
