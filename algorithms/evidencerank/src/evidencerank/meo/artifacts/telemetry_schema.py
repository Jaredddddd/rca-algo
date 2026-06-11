"""Telemetry schema summaries for offline MEO prompt construction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


FRAME_NAMES = (
    "normal_metrics",
    "abnormal_metrics",
    "normal_traces",
    "abnormal_traces",
    "normal_logs",
    "abnormal_logs",
)


def summarize_frames(frames: dict[str, pd.DataFrame]) -> dict[str, Any]:
    """Summarize in-memory telemetry frames without including row-level data."""

    summary: dict[str, Any] = {}
    for name in FRAME_NAMES:
        frame = frames.get(name, pd.DataFrame())
        summary[name] = _summarize_frame(frame)
    return summary


def summarize_parquet_folder(path: str | Path) -> dict[str, Any]:
    """Summarize standard normal/abnormal parquet files in an incident folder."""

    folder = Path(path)
    frames: dict[str, pd.DataFrame] = {}
    for name in FRAME_NAMES:
        parquet_path = folder / f"{name}.parquet"
        if parquet_path.exists():
            frames[name] = pd.read_parquet(parquet_path)
        else:
            frames[name] = pd.DataFrame()
    return summarize_frames(frames)


def _summarize_frame(frame: pd.DataFrame) -> dict[str, Any]:
    if frame is None or frame.empty:
        return {
            "columns": [],
            "num_rows": 0,
            "dtypes": {},
            "sample_values": {},
        }
    columns = [str(column) for column in frame.columns]
    sample_values: dict[str, list[str]] = {}
    for column in frame.columns[:50]:
        values = frame[column].dropna().astype(str).unique()[:5]
        sample_values[str(column)] = [str(value) for value in values]
    return {
        "columns": columns,
        "num_rows": int(len(frame)),
        "dtypes": {str(column): str(dtype) for column, dtype in frame.dtypes.items()},
        "sample_values": sample_values,
    }
