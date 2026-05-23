"""
Utility functions for MicroDig.

This module contains helper functions used throughout the MicroDig package.
"""

import datetime
import json
import os
import time
from typing import Any, Dict, Optional

import pandas as pd
from rcabench_platform.v2.logging import logger

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"  # 默认的时间格式


def ts2date(ts: float) -> datetime.datetime:
    """Convert timestamp to datetime object."""
    return datetime.datetime.fromtimestamp(ts)


def date2datetime(date_str: str, time_format: str = TIME_FORMAT) -> datetime.datetime:
    """Convert date string to datetime object."""
    return datetime.datetime.strptime(date_str, time_format)


def date2ts(date_str: str, time_format: str = TIME_FORMAT) -> int:
    """Convert date string to timestamp."""
    return int(time.mktime(time.strptime(date_str, time_format)))


def ts2date_for_df(df: pd.DataFrame, time_col: str, date_col: str) -> None:
    """Convert timestamp column to datetime column in DataFrame."""
    df[date_col] = df[time_col].map(datetime.datetime.fromtimestamp)


def load_json(json_file: str) -> Optional[Dict[str, Any]]:
    """Load JSON file safely."""
    if os.path.exists(json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON file {json_file}: {str(e)}")
            return None
    else:
        logger.warning(f"No such file: {json_file}")
        return None


def cut_df(df: pd.DataFrame, start: int, end: int, at: str) -> pd.DataFrame:
    """Cut DataFrame by time range."""
    return df[(df[at] >= start) & (df[at] <= end)]


def normalization(data):
    """Normalize data to [0, 1] range."""
    if len(data) == 0:
        return data

    import numpy as np

    if isinstance(data, list):
        data = np.array(data)

    data_range = np.max(data) - np.min(data)
    if data_range == 0:
        logger.warning(f"Data range is zero: {data}")
        return data

    result = (data - np.min(data)) / data_range
    return list(result) if isinstance(data, list) else result


def merge_callings(df: pd.DataFrame, gb_cols: list) -> Dict[str, Any]:
    """
    Merge callings by grouping columns.

    Args:
        df: DataFrame with calling data
        gb_cols: Columns to group by

    Returns:
        Dictionary with merged calling data
    """
    from collections import Counter

    if df.shape[0] == 0:
        return {}

    min_cols = ["duration", "error_min", "error_rate", "request_min"]
    new_data = {}

    if len(gb_cols):
        groups = df.groupby(gb_cols)
    else:
        groups = [(["all"], df)]

    for group_key, group_df in groups:
        key = "|".join(str(k) for k in group_key)
        temp = [Counter() for _ in min_cols]

        for _, row in group_df.iterrows():
            for j, col in enumerate(min_cols):
                if hasattr(row[col], "items"):  # Check if it's dict-like
                    temp[j].update(Counter(row[col]))
                else:
                    # Handle single values
                    temp[j].update({0: row[col]})

        new_data[key] = {
            col: dict(sorted(counter.items(), key=lambda x: x[0]))
            for col, counter in zip(min_cols, temp)
        }
        new_data[key]["name"] = key

    return new_data
