from rcabench_platform.v2.cli.online import app
from rcabench.rcabench import RCABenchSDK
from rcabench.model.error import ModelHTTPError
from loguru import logger


@app.command()
def trace(trace_id: str, host: str = "http://10.10.10.220:32080", timeout: int = 600):
    sdk = RCABenchSDK(host)
    res = sdk.trace.stream_trace_events(trace_id=trace_id, timeout=timeout)
    for event in res:
        if isinstance(event, ModelHTTPError):
            logger.error(f"Error in event stream: {event.detail}")
        else:
            logger.info(event.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
