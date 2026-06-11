from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

import evidencerank.crest as crest_module
from evidencerank.cera import BASE_FEATURE_NAMES
from evidencerank.crest import (
    CREST_COUNTERFACTUAL_MUTATION_FEATURES,
    CREST_COUNTERFACTUAL_PROPAGATION_FEATURES,
    score_crest_services,
)
from evidencerank.crest_meo import CRESTMEO, CRESTMEOBuiltIn
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
from evidencerank.meo.runtime.load_meol import (
    CREST_BUILTIN_MEOL_PATH,
    DEFAULT_MEOL_PATH,
    load_operator_specs,
)
from evidencerank.meo.verify.static_verifier import static_verify
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
    assert set(np.round(role_weights.sum(axis=1), 8)) <= {0.0, 1.0}


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


def test_score_crest_services_default_meol_uses_crest_feature_fast_path(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frames = _trace_frames()
    for name, frame in frames.items():
        frame.to_parquet(tmp_path / f"{name}.parquet")

    def fail_interpreter(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("default MEOL should use the CREST feature fast path")

    monkeypatch.setattr(crest_module, "instantiate_meol_features", fail_interpreter)
    ranking = score_crest_services(tmp_path, use_meo=True)

    assert ranking.iloc[0]["service"] == "a"
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


def test_static_verifier_accepts_neutral_and_rejects_ambiguous_roles() -> None:
    spec = load_operator_specs(DEFAULT_MEOL_PATH)[0]
    neutral = replace(
        spec,
        role_prior={
            "mutation": 0.0,
            "propagation": 0.0,
            "observability_bias": 0.0,
            "topology_context": 0.0,
        },
    )
    ambiguous = replace(
        spec,
        role_prior={
            "mutation": 1.0,
            "propagation": 1.0,
            "observability_bias": 0.0,
            "topology_context": 0.0,
        },
    )

    ok, errors = static_verify(neutral)
    assert ok, errors
    ok, errors = static_verify(ambiguous)
    assert not ok
    assert "role_prior_ambiguous:mutation_and_propagation" in errors


def test_crest_meo_has_separate_canonical_module_with_compat_import() -> None:
    assert CRESTMEO.__module__ == "evidencerank.crest_meo"
    assert crest_module.CRESTMEO is CRESTMEO
    assert CRESTMEOBuiltIn._meol_path == CREST_BUILTIN_MEOL_PATH


def test_crest_builtin_meol_mirrors_hardcoded_feature_sets() -> None:
    specs = load_operator_specs(CREST_BUILTIN_MEOL_PATH)
    names = tuple(spec.name for spec in specs)
    mutation_names = {
        spec.name for spec in specs if spec.role_prior.get("mutation", 0.0) > 0.0
    }
    propagation_names = {
        spec.name for spec in specs if spec.role_prior.get("propagation", 0.0) > 0.0
    }

    assert names == BASE_FEATURE_NAMES
    assert mutation_names == set(CREST_COUNTERFACTUAL_MUTATION_FEATURES)
    assert propagation_names == set(CREST_COUNTERFACTUAL_PROPAGATION_FEATURES)
    for spec in specs:
        assert set(spec.role_prior) == {
            "mutation",
            "propagation",
            "observability_bias",
            "topology_context",
        }
        assert spec.role_prior["mutation"] in {0.0, 1.0}
        assert spec.role_prior["propagation"] in {0.0, 1.0}
        assert not (
            spec.role_prior["mutation"] > 0.0
            and spec.role_prior["propagation"] > 0.0
        )


def test_score_crest_services_crest_builtin_meol_uses_fast_path(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frames = _trace_frames()
    for name, frame in frames.items():
        frame.to_parquet(tmp_path / f"{name}.parquet")

    def fail_interpreter(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("CREST built-in MEOL should use the CREST feature fast path")

    monkeypatch.setattr(crest_module, "instantiate_meol_features", fail_interpreter)
    ranking = score_crest_services(
        tmp_path,
        use_meo=True,
        meol_path=CREST_BUILTIN_MEOL_PATH,
    )

    assert ranking.iloc[0]["service"] == "a"
    assert float(ranking.iloc[0]["score"]) > 0.0


def test_score_crest_services_crest_builtin_meol_matches_crest(tmp_path) -> None:
    frames = _trace_frames()
    for name, frame in frames.items():
        frame.to_parquet(tmp_path / f"{name}.parquet")

    crest_ranking = score_crest_services(tmp_path)
    meo_ranking = score_crest_services(
        tmp_path,
        use_meo=True,
        meol_path=CREST_BUILTIN_MEOL_PATH,
    )

    pd.testing.assert_frame_equal(
        crest_ranking,
        meo_ranking,
        check_exact=False,
        rtol=1e-12,
        atol=1e-12,
    )
