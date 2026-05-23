"""
Evaluation module for MicroDig.

This module provides evaluation metrics and functions to assess
the performance of root cause analysis results.
"""

import os
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from rcabench_platform.v2.logging import logger

from .data_structures import AlgorithmOutput, CaseModel


class Evaluator:
    """Evaluates root cause analysis results."""

    def __init__(self, result_dir: str):
        """
        Initialize evaluator.

        Args:
            result_dir: Directory to save evaluation results
        """
        self.result_dir = result_dir
        self.result_mar: List[List[Any]] = []
        self.result_mar_method: List[List[Any]] = []

        os.makedirs(result_dir, exist_ok=True)

        # Initialize temporary result file
        self.tmp_output_path = os.path.join(result_dir, "tmp_result.csv")
        try:
            self.tmp_output = open(self.tmp_output_path, "w", encoding="utf-8")
            self.tmp_output.write("alarm_start_time,mar\n")
            self.tmp_output.flush()
        except Exception as e:
            logger.error(f"Error initializing tmp output file: {e}")
            self.tmp_output = None

        logger.info(f"Evaluator initialized with result directory: {result_dir}")

    def __del__(self):
        """Cleanup file handles."""
        if hasattr(self, "tmp_output") and self.tmp_output:
            try:
                self.tmp_output.close()
            except Exception:
                pass

    def save_tmp_mar(self, case: CaseModel, mar: List[float]) -> None:
        """Save temporary MAR result."""
        if self.tmp_output:
            try:
                mar_str = ",".join(map(str, mar))
                self.tmp_output.write(f"{case.alarm_start_time},{mar_str}\n")
                self.tmp_output.flush()
            except Exception as e:
                logger.error(f"Error saving tmp MAR: {e}")

    def process_result_method(
        self, res_df: pd.DataFrame, case: CaseModel, score_col: str = "final_score"
    ) -> List[float]:
        """
        Process method-level results.

        Args:
            res_df: Results DataFrame with method rankings
            case: Case model with ground truth
            score_col: Column name for scores

        Returns:
            List of MAR values for each root cause
        """
        if res_df.empty:
            logger.warning(f"Empty results for case {case.alarm_start_time}")
            return [float("inf")] * len(case.rc)

        # Adjust scores to be non-negative
        min_score = res_df[score_col].min()
        res_df = res_df.copy()
        res_df["final_score_adjusted"] = res_df[score_col] - min_score

        # Save detailed results
        result_file = os.path.join(
            self.result_dir, f"method-{case.alarm_start_time}.csv"
        )
        res_df.sort_values("final_score_adjusted", ascending=False).to_csv(
            result_file, index=False
        )

        # Group by server and calculate server-level scores
        if "server" not in res_df.columns:
            # Extract server from node name (assume format: server|service|method)
            res_df["server"] = res_df["name"].apply(
                lambda x: x.split("|")[0] if "|" in x else x
            )

        server_scores = res_df.groupby("server")["final_score_adjusted"].sum().to_dict()
        ranked_servers = sorted(
            server_scores.keys(), key=lambda x: server_scores[x], reverse=True
        )

        # Calculate MAR for each root cause
        mar_values = []
        for rc in case.rc:
            if rc in ranked_servers:
                mar = ranked_servers.index(rc) + 1
            else:
                # Assign average rank for missing servers
                missing_servers = case.server_num - len(ranked_servers)
                mar = len(ranked_servers) + (missing_servers + 1) / 2
            mar_values.append(mar)

        self.result_mar_method.append([case.alarm_start_time, case.rc, mar_values])
        logger.debug(f"Method-level MAR for {case.alarm_start_time}: {mar_values}")

        return mar_values

    def process_result_server(
        self, res_df: pd.DataFrame, case: CaseModel, score_col: str = "final_score"
    ) -> List[float]:
        """
        Process server-level results.

        Args:
            res_df: Results DataFrame with server rankings
            case: Case model with ground truth
            score_col: Column name for scores

        Returns:
            List of MAR values for each root cause
        """
        if res_df.empty:
            logger.warning(f"Empty results for case {case.alarm_start_time}")
            return [float("inf")] * len(case.rc)

        # Adjust scores to be non-negative
        min_score = res_df[score_col].min() if len(res_df) > 0 else 0
        res_df = res_df.copy()
        res_df["final_score_adjusted"] = res_df[score_col] - min_score

        # Save detailed results
        result_file = os.path.join(
            self.result_dir, f"server-{case.alarm_start_time}.csv"
        )
        res_df.sort_values("final_score_adjusted", ascending=False).to_csv(
            result_file, index=False
        )

        # Create server ranking
        server_scores = {
            row.name: row.final_score_adjusted for row in res_df.itertuples()
        }
        ranked_servers = sorted(
            server_scores.keys(), key=lambda x: server_scores[x], reverse=True
        )

        # Calculate MAR for each root cause
        mar_values = []
        for rc in case.rc:
            if rc in ranked_servers:
                mar = ranked_servers.index(rc) + 1
            else:
                # Assign average rank for missing servers
                missing_servers = case.server_num - len(ranked_servers)
                mar = len(ranked_servers) + (missing_servers + 1) / 2
            mar_values.append(mar)

        self.result_mar.append([case.alarm_start_time, case.rc, mar_values])
        self.save_tmp_mar(case, mar_values)

        logger.debug(f"Server-level MAR for {case.alarm_start_time}: {mar_values}")
        return mar_values

    def calculate_metrics(self, mar_results: List[List[Any]]) -> Dict[str, float]:
        """
        Calculate evaluation metrics from MAR results.

        Args:
            mar_results: List of [case_name, root_causes, mar_values]

        Returns:
            Dictionary of evaluation metrics
        """
        if not mar_results:
            logger.warning("No results to evaluate")
            return {}

        # Convert to DataFrame
        df = pd.DataFrame(
            mar_results, columns=["alarm_start_time", "root_cause", "mar"]
        )

        # Flatten all MAR values
        all_mars = []
        for _, row in df.iterrows():
            mar_list = row["mar"]
            if isinstance(mar_list, str):
                mar_list = eval(mar_list)  # Handle string representation
            if isinstance(mar_list, list):
                all_mars.extend([m for m in mar_list if m > 0 and not np.isinf(m)])
            else:
                if mar_list > 0 and not np.isinf(mar_list):
                    all_mars.append(mar_list)

        if not all_mars:
            logger.warning("No valid MAR values found")
            return {}

        metrics = {}

        # Calculate AC@k (Accuracy at k)
        topk_values = [1, 2, 3, 4, 5]
        for k in topk_values:
            accuracy_scores = []

            for _, row in df.iterrows():
                mar_list = row["mar"]
                root_causes = row["root_cause"]

                if isinstance(mar_list, str):
                    mar_list = eval(mar_list)
                if isinstance(root_causes, str):
                    root_causes = eval(root_causes)

                if isinstance(mar_list, list) and isinstance(root_causes, list):
                    # Count how many root causes are in top-k
                    hits = len([m for m in mar_list if 1 <= m <= k])
                    total = min(k, len(root_causes))
                    accuracy_scores.append(hits / total if total > 0 else 0)

            metrics[f"AC@{k}"] = round(np.mean(accuracy_scores), 3)

        # Calculate Avg@k (Average AC@1 to AC@k)
        avg_topk = [5]
        for k in avg_topk:
            avg_score = np.mean([metrics[f"AC@{i}"] for i in range(1, k + 1)])
            metrics[f"Avg@{k}"] = round(avg_score, 3)

        # Calculate MAR (Mean Average Rank)
        metrics["MAR"] = round(np.mean(all_mars), 3)

        # Calculate MRR (Mean Reciprocal Rank)
        reciprocals = [1.0 / mar for mar in all_mars if mar > 0]
        metrics["MRR"] = round(np.mean(reciprocals), 3) if reciprocals else 0.0

        logger.info(f"Calculated metrics: {metrics}")
        return metrics

    def save_final_result(self, result_type: str = "server") -> None:
        """
        Save final evaluation results.

        Args:
            result_type: Type of results ('server' or 'method')
        """
        results_data = (
            self.result_mar if result_type == "server" else self.result_mar_method
        )

        if not results_data:
            logger.warning(f"No {result_type} results to save")
            return

        # Calculate metrics and create DataFrame
        metrics = self.calculate_metrics(results_data)
        df = pd.DataFrame(
            results_data,
            columns=[
                "alarm_start_time",
                "root_cause",
                f"mar_{os.path.basename(self.result_dir)}",
            ],
        )

        # Save results
        save_path = f"result_mar_{result_type}.csv"
        if os.path.exists(save_path):
            try:
                df_old = pd.read_csv(save_path)
                df_merged = df.merge(df_old, on="alarm_start_time", how="outer")
                df_merged.to_csv(save_path, index=False)
            except Exception as e:
                logger.error(f"Error merging with existing results: {e}")
                df.to_csv(save_path, index=False)
        else:
            df.to_csv(save_path, index=False)

        logger.info(f"Saved {result_type} results to {save_path}")
        logger.info(f"Final {result_type} metrics: {metrics}")

    def get_final_result(
        self, result_type: str = "server"
    ) -> Tuple[Dict[str, float], pd.DataFrame]:
        """
        Get final evaluation results.

        Args:
            result_type: Type of results ('server' or 'method')

        Returns:
            Tuple of (metrics_dict, results_dataframe)
        """
        results_data = (
            self.result_mar if result_type == "server" else self.result_mar_method
        )

        if not results_data:
            return {}, pd.DataFrame()

        metrics = self.calculate_metrics(results_data)
        df = pd.DataFrame(
            results_data,
            columns=[
                "alarm_start_time",
                "root_cause",
                f"mar_{os.path.basename(self.result_dir)}",
            ],
        )

        return metrics, df

    def evaluate_algorithm_output(
        self, output: AlgorithmOutput, case: CaseModel
    ) -> Dict[str, Any]:
        """
        Evaluate algorithm output against ground truth.

        Args:
            output: Algorithm output with rankings
            case: Case model with ground truth

        Returns:
            Dictionary with evaluation results
        """
        eval_results = {}

        try:
            # Evaluate different algorithm results
            if output.alg1_server_ranking:
                server_df = pd.DataFrame(
                    output.alg1_server_ranking, columns=["name", "final_score"]
                )
                mar_alg1_server = self.process_result_server(server_df, case)
                eval_results["alg1_server_mar"] = mar_alg1_server

            if output.alg1_method_ranking:
                method_df = pd.DataFrame(
                    output.alg1_method_ranking, columns=["name", "final_score"]
                )
                # Add server column for method evaluation
                method_df["server"] = method_df["name"].apply(
                    lambda x: x.split("|")[0] if "|" in x else x
                )
                mar_alg1_method = self.process_result_method(method_df, case)
                eval_results["alg1_method_mar"] = mar_alg1_method

            if output.alg4_ranking:
                alg4_df = pd.DataFrame(
                    output.alg4_ranking, columns=["name", "final_score"]
                )
                mar_alg4 = self.process_result_server(alg4_df, case)
                eval_results["alg4_mar"] = mar_alg4

            if output.alg5_ranking:
                alg5_df = pd.DataFrame(
                    output.alg5_ranking, columns=["name", "final_score"]
                )
                mar_alg5 = self.process_result_server(alg5_df, case)
                eval_results["alg5_mar"] = mar_alg5

            logger.info(f"Evaluation completed for case {case.alarm_start_time}")

        except Exception as e:
            logger.error(f"Error evaluating algorithm output: {e}")
            eval_results["error"] = str(e)

        return eval_results
