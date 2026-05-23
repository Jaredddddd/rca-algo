"""
MicroDig algorithm adapter for the new platform interface.

This module provides the Algorithm interface implementation for MicroDig
that works with the new data format and rcabench platform.
"""

import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import logger

from .alarm_detector import AlarmDetector
from .algorithm import MicroDigAlgorithm
from .data_loader import DataLoader
from .data_structures import AlgorithmInput, CaseModel


class MicroDigAdapter:
    """Adapter to convert new data format to MicroDig format"""

    def __init__(self):
        self.microdig_algorithm = MicroDigAlgorithm()

    def convert_data_to_microdig_format(
        self, data_loader: DataLoader, inject_time: datetime.datetime
    ) -> Dict[str, Any]:
        """Convert new data format to MicroDig calling patterns"""

        # Load all data including SLI
        all_data = data_loader.load_all_data()

        # Use enhanced calling pattern extraction with SLI data
        calling_patterns = data_loader.extract_calling_patterns_with_sli(
            all_data.get("traces"), all_data.get("metrics_sli")
        )

        if not calling_patterns:
            logger.warning("No calling patterns extracted")
            # Fallback to trace-only if SLI enhancement fails
            if all_data.get("traces") is not None:
                calling_patterns = data_loader.extract_calling_patterns(
                    all_data["traces"]
                )

        return calling_patterns

    def create_case_model(
        self,
        inject_time: datetime.datetime,
        alarm_item: Optional[str] = None,
        root_cause: Optional[str] = None,
    ) -> CaseModel:
        """Create a CaseModel from inject time and other parameters"""

        # Convert inject_time to required format
        alarm_start_time = inject_time.strftime("%Y-%m-%d %H:%M:%S")
        alarm_end_time = (inject_time + datetime.timedelta(minutes=5)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Calculate minutes from start of day
        start_of_day = inject_time.replace(hour=0, minute=0, second=0, microsecond=0)
        alarm_start_minute = int((inject_time - start_of_day).total_seconds() // 60)
        alarm_end_minute = alarm_start_minute + 5

        # Create case model
        case_model = CaseModel(
            alarm_start_time=alarm_start_time,
            alarm_end_time=alarm_end_time,
            alarm_start_minute=alarm_start_minute,
            alarm_end_minute=alarm_end_minute,
            monitor_id=1,
            alarm_item=alarm_item or "unknown-service",
            sli_type="error_rate",
            where_info={"service": alarm_item or "unknown-service"},
        )

        # Set root cause if provided
        if root_cause:
            case_model.rc = [root_cause]

        return case_model

    def run_microdig_analysis(
        self,
        input_folder: Path,
        alarm_item: Optional[str] = None,
        root_cause: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Run MicroDig analysis on new data format"""

        try:
            # Initialize data loader
            data_loader = DataLoader(input_folder)
            inject_time = data_loader.get_inject_time()

            logger.info(f"Running MicroDig analysis for inject_time: {inject_time}")

            # Convert data to MicroDig format
            calling_patterns = self.convert_data_to_microdig_format(
                data_loader, inject_time
            )

            if not calling_patterns:
                logger.warning("No calling patterns extracted")
                return {
                    "node_names": [],
                    "ranks": [],
                    "error": "No calling patterns found",
                }

            # Create case model
            case_model = self.create_case_model(inject_time, alarm_item, root_cause)
            case_model.callings = calling_patterns

            # Create algorithm input
            algorithm_input = AlgorithmInput(case=case_model, **kwargs)

            # Run analysis
            output = self.microdig_algorithm.analyze_case(algorithm_input)

            if not output.success:
                return {"node_names": [], "ranks": [], "error": output.error_message}

            # Extract results from simplified service ranking
            service_ranking = output.service_ranking if output.service_ranking else []

            logger.info(
                f"MicroDig analysis completed. Found {len(service_ranking)} ranked services"
            )

            return {
                "node_names": service_ranking,  # For backward compatibility
                "ranks": service_ranking,
                "processing_time": output.processing_time,
                "algorithms_results": output,  # Pass the full output
            }

        except Exception as e:
            error_msg = f"MicroDig analysis failed: {str(e)}"
            logger.error(error_msg)
            return {"node_names": [], "ranks": [], "error": error_msg}


def microdig_analysis(
    input_folder: Path,
    alarm_item: Optional[str] = None,
    root_cause: Optional[str] = None,
    test_length_before: int = 10,
    test_length_after: int = 10,
    train_length: int = 60,
    search_method: str = "all",
    rank_method: str = "random walk",
    level: str = "service",
    rev_weight: float = 0.2,
    beta: float = 0.1,
) -> Dict[str, Any]:
    """
    Main MicroDig analysis function with new data format.

    Args:
        input_folder: Path to folder containing parquet files
        alarm_item: Name of the alarmed service/component (auto-detected if None)
        root_cause: Ground truth root cause (for evaluation)
        test_length_before: Time window before alarm for testing
        test_length_after: Time window after alarm for testing
        train_length: Historical data window for training
        search_method: Strategy for finding candidates ('all', 'deepest2', 'last2')
        rank_method: Ranking algorithm ('pagerank', 'random walk')
        level: Analysis level ('method', 'service')
        rev_weight: Weight for reverse edges in graph
        beta: Weight factor for mixed node ranking

    Returns:
        Dictionary containing analysis results
    """
    import time

    start_time = time.time()

    try:
        # Auto-detect alarm_item if not provided using enhanced detection
        if alarm_item is None:
            logger.info("Auto-detecting alarm service from available data sources")
            alarm_detector = AlarmDetector(input_folder)
            detected_alarm = alarm_detector.detect_alarm_service()

            if detected_alarm:
                alarm_item = detected_alarm
                logger.info(f"Auto-detected alarm service: {alarm_item}")

                # Get detailed issue summary if available
                issue_summary = alarm_detector.get_issue_summary(alarm_item)
                if issue_summary:
                    logger.info(f"Issue summary for {alarm_item}:")
                    logger.info(f"  Span: {issue_summary.get('span_name', 'N/A')}")
                    logger.info(f"  Severity: {issue_summary.get('severity', 0):.2f}")
                    logger.info(f"  Issues: {issue_summary.get('issues', {})}")
            else:
                logger.warning(
                    "Could not auto-detect alarm service, analysis may be less effective"
                )

        # Create adapter and run analysis
        adapter = MicroDigAdapter()
        result = adapter.run_microdig_analysis(
            input_folder=input_folder,
            alarm_item=alarm_item,
            root_cause=root_cause,
            test_length_before=test_length_before,
            test_length_after=test_length_after,
            train_length=train_length,
            search_method=search_method,
            rank_method=rank_method,
            level=level,
            rev_weight=rev_weight,
            beta=beta,
        )

        # Add processing time
        processing_time = time.time() - start_time
        result["processing_time"] = processing_time
        result["auto_detected_alarm"] = (
            alarm_item if alarm_item != root_cause else False
        )

        return result

    except Exception as e:
        processing_time = time.time() - start_time
        error_msg = f"MicroDig analysis failed: {str(e)}"
        logger.error(error_msg)
        return {
            "node_names": [],
            "ranks": [],
            "error": error_msg,
            "processing_time": processing_time,
        }


class MicroDig(Algorithm):
    """MicroDig algorithm implementation for rcabench platform"""

    def needs_cpu_count(self) -> Optional[int]:
        return 4

    def __call__(self, args: AlgorithmArgs) -> List[AlgorithmAnswer]:
        """Execute MicroDig algorithm"""

        logger.info("Starting MicroDig algorithm execution")

        try:
            # Extract parameters from args
            input_folder = Path(args.input_folder)

            # Get algorithm parameters (with defaults)

            # Run analysis
            result = microdig_analysis(
                input_folder=input_folder,
            )

            # Create algorithm answers for each ranked service
            answers = []

            # Get service ranking from the simplified output
            if "algorithms_results" in result:
                algorithm_output = result["algorithms_results"]
                if hasattr(algorithm_output, "service_ranking"):
                    service_ranking = algorithm_output.service_ranking
                elif (
                    isinstance(algorithm_output, dict)
                    and "service_ranking" in algorithm_output
                ):
                    service_ranking = algorithm_output["service_ranking"]
                else:
                    # Fallback to node_names for backward compatibility
                    service_ranking = result.get("node_names", [])
            else:
                service_ranking = result.get("node_names", [])

            for i, service_name in enumerate(service_ranking[:10]):  # Top 10 results
                answer = AlgorithmAnswer(
                    level="service",  # We only do service level RCA
                    name=service_name,
                    rank=i + 1,
                )
                answers.append(answer)

            # If no results, return empty list
            if not answers:
                logger.warning("No ranked services found in analysis result")

            return answers

        except Exception as e:
            error_msg = f"MicroDig algorithm execution failed: {str(e)}"
            logger.error(error_msg)

            # Return empty list for error case
            return []
