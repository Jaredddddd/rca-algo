"""
Example script showing how to use the MicroDig algorithm.

This script demonstrates how to use the refactored MicroDig algorithm
for microservice failure root cause analysis.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from rcabench_platform.v2.logging import logger

from microdig import AlgorithmInput, CaseModel, MicroDigAlgorithm


def main():
    """Main execution function."""
    logger.info("Starting MicroDig example")

    # Initialize the algorithm
    hyper_params = {
        "test_length_before": 10,
        "test_length_after": 10,
        "train_length": 60,
        "search_method": "all",
        "rank_method": "random walk",
        "level": "method",
        "rev_weight": 0.2,
        "server_data": False,
        "beta": 0.1,
    }

    algorithm = MicroDigAlgorithm(hyper_params)

    # Example 1: Preprocess traces (if you have raw pickle files)
    # algorithm.preprocess_traces(
    #     input_dir='./raw_traces',
    #     output_dir='./processed_traces'
    # )

    # Example 2: Process trace statistics
    # algorithm.process_trace_statistics(
    #     input_pattern='./processed_traces/*.csv',
    #     output_file='./output.csv'
    # )

    # Example 3: Run full pipeline with existing case data
    case_info_file = "./MicroDig/dataset/cases_testbed.csv"
    case_data_dir = "./MicroDig/cases"
    output_dir = "./results"

    if os.path.exists(case_info_file) and os.path.exists(case_data_dir):
        logger.info("Running full pipeline")
        results = algorithm.run_full_pipeline(
            case_info_file=case_info_file,
            case_data_dir=case_data_dir,
            output_dir=output_dir,
        )

        logger.info("Pipeline results:")
        logger.info(f"Total cases: {results.get('total_cases', 0)}")
        logger.info(f"Success rate: {results.get('success_rate', 0):.2%}")
        logger.info(
            f"Average processing time: {results.get('avg_processing_time', 0):.2f}s"
        )

        # Print evaluation metrics
        metrics = results.get("metrics", {})
        for alg_name, alg_metrics in metrics.items():
            logger.info(f"\n{alg_name} metrics:")
            for metric_name, metric_value in alg_metrics.items():
                logger.info(f"  {metric_name}: {metric_value}")

    else:
        logger.warning("Case data files not found, creating example case")

        # Example 4: Create and analyze a single case
        example_case = CaseModel(
            alarm_start_time="2022-02-23 07:00:00",
            alarm_end_time="2022-02-23 07:05:00",
            alarm_start_minute=420,  # 7:00 AM in minutes
            alarm_end_minute=425,  # 7:05 AM in minutes
            monitor_id=1,
            alarm_item="ts-preserve-other-service",
            sli_type="error_rate",
            where_info={"service": "ts-preserve-other-service"},
            rc=["ts-basic-service"],  # Ground truth root cause
            server_num=10,
        )

        # Create algorithm input
        algorithm_input = AlgorithmInput(case=example_case, **hyper_params)

        # Analyze the case
        logger.info("Analyzing example case")
        output = algorithm.analyze_case(algorithm_input)

        if output.success:
            logger.info(f"Analysis completed in {output.processing_time:.2f}s")
            logger.info(
                f"Algorithm 1 server rankings: {len(output.alg1_server_ranking)} results"
            )
            logger.info(f"Algorithm 4 rankings: {len(output.alg4_ranking)} results")
            logger.info(f"Algorithm 5 rankings: {len(output.alg5_ranking)} results")
        else:
            logger.error(f"Analysis failed: {output.error_message}")

    logger.info("MicroDig example completed")


if __name__ == "__main__":
    main()
