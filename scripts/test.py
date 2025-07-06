import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    from typing import Generator, List, Union
    from datetime import datetime, timezone
    from rcabench.const import EventType
    from rcabench.model.error import ModelHTTPError
    from rcabench.model.trace import StreamEvent
    from rcabench.openapi.api import AlgorithmApi, InjectionApi
    from rcabench.openapi.api_client import ApiClient, Configuration
    from rcabench.openapi.models import DtoAlgorithmExecutionPayload, DtoTrace
    from rcabench.rcabench import RCABenchSDK
    import json
    import marimo as mo
    import os
    import pandas as pd
    import sqlalchemy

    return (
        AlgorithmApi,
        ApiClient,
        Configuration,
        DtoAlgorithmExecutionPayload,
        DtoTrace,
        EventType,
        Generator,
        InjectionApi,
        List,
        ModelHTTPError,
        RCABenchSDK,
        StreamEvent,
        Union,
        mo,
        os,
        pd,
        sqlalchemy,
    )


@app.cell
def _(mo):
    algorithm_input = mo.ui.text_area(
        placeholder="输入要构建的算法名称，用逗号分隔", label="指定算法（可选）"
    )
    return (algorithm_input,)


@app.cell
def _(os, sqlalchemy):
    _password = os.environ.get("POSTGRES_PASSWORD", "yourpassword")
    DATABASE_URL = f"postgresql://postgres:{_password}@10.10.10.220:32432/rcabench"
    engine = sqlalchemy.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _(engine, pd):
    container_df = None
    container_query = "SELECT * FROM containers"

    try:
        container_df = pd.read_sql(container_query, engine)
        print(f"查询返回 {len(container_df)} 条记录")
    except Exception as e:
        print(f"查询执行错误: {e}")
        container_df = pd.DataFrame()

    algorithm_df = container_df[container_df["type"] == "algorithm"]
    algorithm_df = algorithm_df[algorithm_df["name"] != "detector"]
    algorithm_df
    return (algorithm_df,)


@app.cell
def _(algorithm_df, algorithm_input):
    input_text = algorithm_input.value

    if not input_text or input_text.strip() == "":
        # 如果没有指定算法，从数据库中随机选择一个
        if not algorithm_df.empty:
            random_algorithm = algorithm_df.sample(n=1)
            algorithms = [random_algorithm.iloc[0]["name"]]
            print(f"未指定算法，随机选择: {algorithms[0]}")
        else:
            algorithms = []
            print("数据库中没有找到算法容器")
    else:
        # 处理输入的算法名称（去除空格并分割）
        algorithms = [algo.strip() for algo in input_text.split(",") if algo.strip()]
        print(f"指定的算法: {algorithms}")
    return (algorithms,)


@app.cell
def _(ApiClient, Configuration, InjectionApi, pd):
    host = "http://10.10.10.220:32080"
    configuration = Configuration(host=host)
    configuration.datetime_format = "%Y-%m-%dT%H:%M:%SZ"
    client = ApiClient(configuration)

    injector = InjectionApi(api_client=client)
    injection_list_resp = injector.api_v1_injections_get(env="prod", batch="bootstrap")
    assert injection_list_resp is not None
    injection_data = [injection.to_dict() for injection in injection_list_resp.data]

    injection_df = pd.DataFrame(injection_data)
    injection_df
    return client, host, injection_df


@app.cell
def _(injection_df):
    datasets = injection_df["injection_name"][:1]
    datasets
    return (datasets,)


@app.cell
def _(Generator, ModelHTTPError, RCABenchSDK, StreamEvent, Union, host):
    def trace_execution(
        trace_id: str, timeout: int = 300
    ) -> Generator[Union[StreamEvent, ModelHTTPError], None, None]:
        sdk = RCABenchSDK(host)
        return sdk.trace.stream_trace_events(trace_id, timeout=timeout)

    return (trace_execution,)


@app.cell
def _(DtoAlgorithmExecutionPayload, algorithms, datasets):
    payload = []
    for algorithm in algorithms:
        for dataset in datasets:
            payload.append(
                DtoAlgorithmExecutionPayload.from_dict(
                    {"algorithm": algorithm, "dataset": dataset}
                )
            )

    payload
    return (payload,)


@app.cell
def _(AlgorithmApi, DtoTrace, List, client, payload):
    algorithmer = AlgorithmApi(api_client=client)
    algorithm_submit_resp = algorithmer.api_v1_algorithms_post(body=payload)
    traces: List[DtoTrace] = algorithm_submit_resp.data.traces
    traces
    return (traces,)


@app.cell
def _(EventType, pd, trace_execution, traces: "List[DtoTrace]"):
    results = {}
    errors = []

    for trace in traces:
        trace_id = trace.trace_id
        event_list = trace_execution(trace_id)
        if event_list is not None:
            for e in event_list:
                print(e.model_dump_json())
                if e.event_name == EventType.EventAlgoRunFailed:
                    errors.append(e.payload)
                if e.event_name == EventType.EventAlgoResultCollection:
                    results[trace_id] = pd.DataFrame(e.payload)
    return errors, results


@app.cell
def _(results):
    results
    return


@app.cell
def _(errors):
    errors
    return


if __name__ == "__main__":
    app.run()
