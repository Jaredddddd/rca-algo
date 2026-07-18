import polars as pl

from shapleyiq.platform.data_loader import load_traces
from shapleyiq.platform.alarm_detector import detect_anomalous_services
from shapleyiq.platform.adapters import _match_service_to_node
from shapleyiq.platform.algorithms import (
    MicroHECL,
    MicroRCA,
    MicroRank,
    ShapleyRCA,
    TON,
)


def test_shapley_family_disables_parallel_batch_execution():
    algorithms = [ShapleyRCA(), MicroHECL(), MicroRCA(), TON(), MicroRank()]

    assert all(algorithm.needs_cpu_count() is None for algorithm in algorithms)


def test_load_traces_treats_empty_optional_http_numbers_as_null(tmp_path):
    base_rows = {
        "trace_id": ["trace-1", "trace-2"],
        "span_id": ["span-1", "span-2"],
        "parent_span_id": ["", "span-1"],
        "service_name": ["frontend", "backend"],
        "span_name": ["GET /api", "POST /work"],
        "duration": [100, 200],
        "attr.status_code": ["Ok", "Error"],
        "attr.http.response.status_code": ["", "200"],
    }
    pl.DataFrame(base_rows).write_parquet(tmp_path / "normal_traces.parquet")
    pl.DataFrame(
        {
            **base_rows,
            "trace_id": ["trace-3", "trace-4"],
            "attr.http.response.status_code": ["302", ""],
        }
    ).write_parquet(tmp_path / "abnormal_traces.parquet")

    traces = load_traces(tmp_path).collect()

    assert traces.schema["attr.http.response.status_code"] == pl.Float64
    assert traces.schema["attr.http.request.content_length"] == pl.Float64
    assert traces.schema["attr.http.response.content_length"] == pl.Float64
    assert traces.get_column("attr.http.response.status_code").to_list() == [
        None,
        200.0,
        302.0,
        None,
    ]
    assert traces.get_column("attr.http.request.content_length").null_count() == 4
    assert traces.get_column("attr.http.response.content_length").null_count() == 4


def test_alarm_detection_uses_common_conclusion_contract(tmp_path):
    pl.DataFrame(
        {
            "SpanName": ["GET /api/v1/auth/login"],
            "Issues": ['{"latency": {"change_rate": 3.0, "slo_violated": true}}'],
        }
    ).write_parquet(tmp_path / "conclusion.parquet")

    assert detect_anomalous_services(tmp_path) == ["ts-auth-service"]


def test_alarm_detection_has_no_metric_fallback(tmp_path):
    assert detect_anomalous_services(tmp_path) == []


def test_alarm_service_is_mapped_to_operation_node():
    nodes = ["frontend:GET /", "checkoutservice:POST /checkout"]

    assert (
        _match_service_to_node("checkoutservice", nodes)
        == "checkoutservice:POST /checkout"
    )
    assert _match_service_to_node(nodes[0], nodes) == nodes[0]
