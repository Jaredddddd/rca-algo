import polars as pl

from shapleyiq.platform.data_loader import load_traces


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
