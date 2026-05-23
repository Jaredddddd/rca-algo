"""
Anomaly detection module for MicroDig.

This module provides anomaly detection capabilities using statistical methods
to identify unusual patterns in microservice calling behavior.
"""

from typing import Any, Dict, List

import numpy as np
import pandas as pd
from rcabench_platform.v2.logging import logger


class AnomalyDetector:
    """Detects anomalies in microservice calling patterns."""

    def __init__(self, hyper_params: Dict[str, Any]):
        """
        Initialize anomaly detector.

        Args:
            hyper_params: Hyperparameters for anomaly detection
        """
        self.hyper_params = hyper_params
        self.anomaly_score_func = self.ksigma
        logger.debug("AnomalyDetector initialized with k-sigma method")

    @staticmethod
    def ksigma(train: np.ndarray, test: np.ndarray, is_alarm: bool) -> float:
        """
        K-sigma anomaly detection method.

        Args:
            train: Training data array
            test: Test data array
            is_alarm: Whether this is for an alarm condition

        Returns:
            Anomaly score between 0 and 1
        """
        eps = 1e-3
        mean = train.mean()
        std = train.std()
        mmax = test.max()
        mmin = test.min()

        # Check if test data shows significant change
        if (mmax - mmin < 0.0005) or (mmax <= train.max()):
            return 0.01 if is_alarm else 0

        temp_scores = []
        for x in test:
            # Check if value is outside 3-sigma range with minimum threshold
            if ((x > mean + 3 * std) or (x < mean - 3 * std)) and (
                abs(x - mean) >= 0.0005
            ):
                temp_scores.append(1)
                break
            else:
                temp_scores.append(0.01 if is_alarm else 0)

        return max(temp_scores) if temp_scores else 0

    def edge_score(
        self, alarm_minute: int, data_list: List[Dict], is_alarm: bool
    ) -> List[float]:
        """
        Calculate anomaly scores for edge data.

        Args:
            alarm_minute: Minute when alarm occurred
            data_list: List of time-series data dictionaries
            is_alarm: Whether this is for an alarm condition

        Returns:
            List of anomaly scores for each data series
        """
        train_length = self.hyper_params["train_length"]
        test_length_before = self.hyper_params["test_length_before"]
        test_length_after = self.hyper_params["test_length_after"]

        scores = []

        for data_dict in data_list:
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(
                {"min": list(data_dict.keys()), "value": list(data_dict.values())}
            )

            # Extract training data (before alarm)
            train_data = df[
                (df["min"] > alarm_minute - test_length_before - train_length)
                & (df["min"] <= alarm_minute - test_length_before)
            ]["value"].values

            # Extract test data (around alarm time)
            test_data = df[
                (df["min"] > alarm_minute - test_length_before)
                & (df["min"] <= alarm_minute + test_length_after)
            ]["value"].values

            # Check if we have sufficient data
            if len(train_data) < 5 or len(test_data) == 0:
                logger.debug(
                    f"Insufficient data: train={len(train_data)}, test={len(test_data)}"
                )
                return [0] * len(data_list)

            # Calculate anomaly score
            score = self.anomaly_score_func(train_data, test_data, is_alarm)
            scores.append(score)

            logger.debug(f"Calculated anomaly score: {score:.4f}")

        return scores

    def detect_anomalous_edges(
        self, callings: Dict[str, Any], alarm_minute: int
    ) -> Dict[str, float]:
        """
        Detect anomalous calling edges.

        Args:
            callings: Dictionary of calling data
            alarm_minute: Minute when alarm occurred

        Returns:
            Dictionary mapping edge names to anomaly scores
        """
        logger.info(f"Detecting anomalous edges for alarm at minute {alarm_minute}")

        anomalous_edges = {}

        for edge_name, edge_data in callings.items():
            # Extract time series data for different metrics
            metrics = ["duration", "error_rate", "request_min"]
            metric_data = []

            for metric in metrics:
                if metric in edge_data:
                    metric_data.append(edge_data[metric])
                else:
                    logger.warning(f"Missing metric {metric} for edge {edge_name}")
                    metric_data.append({})

            # Calculate anomaly scores for each metric
            scores = self.edge_score(alarm_minute, metric_data, is_alarm=True)

            # Combine scores (could use different aggregation methods)
            combined_score = np.mean(scores) if scores else 0.0
            anomalous_edges[edge_name] = combined_score

            logger.debug(
                f"Edge {edge_name}: scores={scores}, combined={combined_score:.4f}"
            )

        # Filter edges with significant anomaly scores
        significant_threshold = 0.1
        anomalous_edges = {
            name: score
            for name, score in anomalous_edges.items()
            if score >= significant_threshold
        }

        logger.info(f"Found {len(anomalous_edges)} anomalous edges")
        return anomalous_edges

    def get_anomaly_threshold(
        self, scores: List[float], percentile: float = 0.9
    ) -> float:
        """
        Get anomaly threshold based on score distribution.

        Args:
            scores: List of anomaly scores
            percentile: Percentile for threshold

        Returns:
            Threshold value
        """
        if not scores:
            return 0.0

        threshold = np.percentile(scores, percentile * 100)
        logger.debug(f"Anomaly threshold at {percentile * 100}%: {threshold:.4f}")
        return threshold
