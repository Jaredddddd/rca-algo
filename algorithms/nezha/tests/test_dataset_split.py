from __future__ import annotations

from pathlib import Path

import polars as pl

from nezha.integration import NezhaIntegrator
from nezha.rcabench_adapter import NezhaAlgorithm


def test_nezha_disables_parallel_batch_execution():
    assert NezhaAlgorithm().needs_cpu_count() is None


def _write_trace_pack(root: Path) -> None:
    normal_traces = pl.DataFrame(
        [
            {
                "time": "2025-06-16T17:56:05Z",
                "trace_id": "normal-1",
                "span_id": "n1",
                "parent_span_id": "",
                "span_name": "HTTP",
                "attr.span_kind": "SERVER",
                "service_name": "frontend",
                "duration": 10_000_000,
                "attr.status_code": "Ok",
            },
            {
                "time": "2025-06-16T17:56:06Z",
                "trace_id": "normal-2",
                "span_id": "n2",
                "parent_span_id": "",
                "span_name": "HTTP",
                "attr.span_kind": "SERVER",
                "service_name": "frontend",
                "duration": 11_000_000,
                "attr.status_code": "Ok",
            },
        ]
    )
    abnormal_traces = pl.DataFrame(
        [
            {
                "time": "2025-06-16T18:10:05Z",
                "trace_id": "abnormal-1",
                "span_id": "a1",
                "parent_span_id": "",
                "span_name": "HTTP",
                "attr.span_kind": "SERVER",
                "service_name": "frontend",
                "duration": 12_000_000,
                "attr.status_code": "Error",
            },
            {
                "time": "2025-06-16T18:10:06Z",
                "trace_id": "abnormal-2",
                "span_id": "a2",
                "parent_span_id": "",
                "span_name": "HTTP",
                "attr.span_kind": "SERVER",
                "service_name": "frontend",
                "duration": 13_000_000,
                "attr.status_code": "Error",
            },
        ]
    )

    normal_traces.write_parquet(root / "normal_traces.parquet")
    abnormal_traces.write_parquet(root / "abnormal_traces.parquet")
    (root / "env.json").write_text(
        """{
  "NORMAL_START": "1",
  "NORMAL_END": "2",
  "ABNORMAL_START": "3",
  "ABNORMAL_END": "4"
}""",
        encoding="utf-8",
    )


def test_integrator_uses_explicit_dataset_split(tmp_path: Path):
    _write_trace_pack(tmp_path)

    integrator = NezhaIntegrator(tmp_path)
    integrator.load_and_preprocess(need_logs=False)

    assert [t.trace_id for t in integrator.normal_traces] == ["normal-1", "normal-2"]
    assert [t.trace_id for t in integrator.abnormal_traces] == [
        "abnormal-1",
        "abnormal-2",
    ]


def test_run_analysis_returns_service_mapping(tmp_path: Path):
    _write_trace_pack(tmp_path)

    integrator = NezhaIntegrator(tmp_path)
    integrator.load_and_preprocess(need_logs=False)
    integrator.separate_normal_abnormal_traces()

    results = integrator.run_analysis(min_support=1, min_score=0.0, top_k=5)

    assert "service_mapping" in results
    assert "service_id_to_name" in results
    assert results["service_mapping"]["frontend"] == 0
    assert results["service_id_to_name"][0] == "frontend"


def test_missing_metrics_sli_derives_thresholds_from_normal_traces(
    tmp_path: Path,
):
    _write_trace_pack(tmp_path)

    integrator = NezhaIntegrator(tmp_path)
    integrator.load_and_preprocess(need_logs=False)

    thresholds = integrator.preprocessor.performance_thresholds
    assert thresholds["frontend_HTTP"] >= 11_000_000
    assert thresholds["frontend_HTTP"] < 12_000_000
