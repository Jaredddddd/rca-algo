from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import polars as pl


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_rcaeval_rcabench.py"
SPEC = importlib.util.spec_from_file_location("build_rcaeval_rcabench", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def _write_case(
    root: Path,
    subset_dir: str,
    *,
    with_traces: bool = True,
    run: str = "1",
) -> Path:
    case = root / subset_dir / "checkoutservice_cpu" / run
    case.mkdir(parents=True)
    (case / "inject_time.txt").write_text("101\n", encoding="utf-8")
    pl.DataFrame(
        {
            "time": [100, 101, 102],
            "checkoutservice_cpu": [1.0, 8.0, 9.0],
            "frontend_latency-90": [0.1, 0.8, 0.9],
        }
    ).write_csv(case / "simple_metrics.csv")
    pl.DataFrame(
        {
            "time": ["00:01", "00:01"],
            "timestamp": [100_000_000_000, 101_000_000_000],
            "container_name": ["checkoutservice", "checkoutservice"],
            "message": ["ok", "error happened"],
            "level": ["info", "warning"],
        }
    ).write_csv(case / "logs.csv")
    if with_traces:
        pl.DataFrame(
            {
                "time": ["00:01", "00:01"],
                "traceID": ["t1", "t2"],
                "spanID": ["s1", "s2"],
                "serviceName": ["frontend", "checkoutservice"],
                "methodName": ["GET", "POST"],
                "operationName": ["/", "/checkout"],
                "startTimeMillis": [100_000, 101_000],
                "startTime": [100_000_000, 101_000_000],
                "duration": [5, 10],
                "statusCode": [0.0, 2.0],
                "parentSpanID": ["", "s1"],
            }
        ).write_csv(case / "traces.csv")
    return case


def test_split_fault_directory_preserves_hyphenated_service() -> None:
    assert module.split_fault_directory("ts-auth-service_cpu") == (
        "ts-auth-service",
        "cpu",
    )


def test_convert_dataset_writes_rcabench_contract_and_combined_links(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "source"
    _write_case(source_root, "RE2-OB/RE2-OB")
    data_root = tmp_path / "data-root"

    results = module.convert_datasets(
        source_root=source_root,
        data_root=data_root,
        subsets=["ob"],
        dataset_prefix="rcabench_rcaeval_re2",
        workers=1,
        overwrite=False,
    )

    assert len(results["ob"]) == 1
    datapack = data_root / "data/rcabench_rcaeval_re2_ob/checkoutservice_cpu_1"
    assert (datapack / ".finished").exists()
    for phase in ("normal", "abnormal"):
        for modality in ("metrics", "traces", "logs"):
            assert (datapack / f"{phase}_{modality}.parquet").exists()

    normal_metrics = pl.read_parquet(datapack / "normal_metrics.parquet")
    abnormal_metrics = pl.read_parquet(datapack / "abnormal_metrics.parquet")
    assert int(normal_metrics["time"].max().timestamp()) == 100
    assert int(abnormal_metrics["time"].min().timestamp()) == 101
    assert set(normal_metrics["service_name"]) == {"checkoutservice", "frontend"}
    assert "attr.k8s.container.name" in normal_metrics.columns

    abnormal_logs = pl.read_parquet(datapack / "abnormal_logs.parquet")
    assert abnormal_logs["level"].to_list() == ["WARN"]
    abnormal_traces = pl.read_parquet(datapack / "abnormal_traces.parquet")
    assert abnormal_traces["attr.status_code"].to_list() == ["Error"]
    normal_traces = pl.read_parquet(datapack / "normal_traces.parquet")
    assert normal_traces["attr.status_code"].to_list() == ["Ok"]
    conclusion = pl.read_parquet(datapack / "conclusion.parquet")
    assert conclusion.schema == module.CONCLUSION_SCHEMA

    conversion = json.loads((datapack / "conversion.json").read_text(encoding="utf-8"))
    assert conversion["conversion_version"] == module.CONVERSION_VERSION
    assert conversion["metric_preprocessing"] == module.METRIC_PREPROCESSING
    assert (
        conversion["metric_window_rows_per_phase"] == module.RCAEVAL_METRIC_WINDOW_ROWS
    )

    injection = json.loads((datapack / "injection.json").read_text(encoding="utf-8"))
    assert injection["ground_truth"]["service"] == ["checkoutservice"]
    labels = pl.read_parquet(data_root / "meta/rcabench_rcaeval_re2_ob/labels.parquet")
    assert labels.row(0, named=True)["gt.name"] == "checkoutservice"

    combined = data_root / "data/rcabench_rcaeval_re2/re2-ob__checkoutservice_cpu_1"
    assert combined.is_symlink()
    assert combined.resolve() == datapack.resolve()
    combined_labels = pl.read_parquet(
        data_root / "meta/rcabench_rcaeval_re2/labels.parquet"
    )
    assert combined_labels.row(0, named=True)["datapack"].startswith("re2-ob__")


def test_missing_trace_source_produces_schema_valid_empty_frames(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "source"
    _write_case(source_root, "RE2-SS/RE2-SS", with_traces=False)
    data_root = tmp_path / "data-root"

    module.convert_datasets(
        source_root=source_root,
        data_root=data_root,
        subsets=["ss"],
        dataset_prefix="rcabench_rcaeval_re2",
        workers=1,
        overwrite=False,
    )

    trace_path = (
        data_root
        / "data/rcabench_rcaeval_re2_ss/checkoutservice_cpu_1/normal_traces.parquet"
    )
    traces = pl.read_parquet(trace_path)
    assert traces.is_empty()
    assert traces.schema == module.TRACE_SCHEMA
    conclusion = pl.read_parquet(trace_path.parent / "conclusion.parquet")
    assert conclusion.is_empty()
    assert conclusion.schema == module.CONCLUSION_SCHEMA


def test_incremental_subset_run_preserves_existing_metadata(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    _write_case(source_root, "RE2-OB/RE2-OB", run="1")
    _write_case(source_root, "RE2-OB/RE2-OB", run="2")
    _write_case(source_root, "RE2-SS/RE2-SS", run="1", with_traces=False)
    data_root = tmp_path / "data-root"

    module.convert_datasets(
        source_root=source_root,
        data_root=data_root,
        subsets=["ob", "ss"],
        dataset_prefix="rcabench_rcaeval_re2",
        workers=1,
        overwrite=False,
    )
    results = module.convert_datasets(
        source_root=source_root,
        data_root=data_root,
        subsets=["ob"],
        dataset_prefix="rcabench_rcaeval_re2",
        workers=1,
        overwrite=False,
        limit=1,
    )

    assert len(results["ob"]) == 2
    assert len(results["ss"]) == 1
    ob_index = pl.read_parquet(data_root / "meta/rcabench_rcaeval_re2_ob/index.parquet")
    ss_index = pl.read_parquet(data_root / "meta/rcabench_rcaeval_re2_ss/index.parquet")
    combined_index = pl.read_parquet(
        data_root / "meta/rcabench_rcaeval_re2/index.parquet"
    )
    assert ob_index.height == 2
    assert ss_index.height == 1
    assert combined_index.height == 3


def test_metric_normalization_preserves_ffilled_missing_time_rows(
    tmp_path: Path,
) -> None:
    source = tmp_path / "simple_metrics.csv"
    pl.DataFrame(
        {
            "time": [100.0, 101.0, None],
            "checkoutservice_cpu": [1.0, None, 3.0],
            "frontend_latency-90": [None, 2.0, None],
        }
    ).write_csv(source)

    metrics = module._normalise_metrics(source, inject_time=101).collect()
    trailing = metrics.filter(pl.col("time").dt.epoch("s") == 101)

    assert metrics.height == 6
    assert trailing.height == 4
    assert trailing.filter(
        (pl.col("service_name") == "checkoutservice") & (pl.col("metric") == "cpu")
    )["value"].to_list() == [1.0, 3.0]
    assert trailing.filter(
        (pl.col("service_name") == "frontend") & (pl.col("metric") == "latency")
    )["value"].to_list() == [2.0, 2.0]


def test_metric_normalization_applies_public_length20_protocol(
    tmp_path: Path,
) -> None:
    source = tmp_path / "simple_metrics.csv"
    inject_time = 1_000
    normal_times = list(range(inject_time - 603, inject_time))
    abnormal_times = list(range(inject_time, inject_time + 604))
    times = normal_times + abnormal_times
    pl.DataFrame(
        {
            "time": times,
            "checkoutservice_cpu": list(map(float, range(len(times)))),
            "frontend_latency-50": [1.0] * len(times),
            "frontend_latency-90": list(map(float, range(len(times)))),
        }
    ).write_csv(source)

    metrics = module._normalise_metrics(source, inject_time=inject_time).collect()
    seconds = metrics.get_column("time").dt.epoch("s")

    assert set(metrics.get_column("metric")) == {"cpu", "latency"}
    assert metrics.height == 600 * 2 * 2
    assert seconds.filter(seconds < inject_time).min() == inject_time - 600
    assert seconds.filter(seconds >= inject_time).max() == inject_time + 599
