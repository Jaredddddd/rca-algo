"""
Main MicroDig algorithm implementation.

This module provides the main MicroDig algorithm that combines
data preprocessing, graph generation, anomaly detection, and ranking
to identify root causes in microservice failures.
"""

import time
from typing import Any, Dict, List, Optional

import pandas as pd
from rcabench_platform.v2.logging import logger

from .anomaly import AnomalyDetector
from .data_structures import AlgorithmInput, AlgorithmOutput
from .evaluator import Evaluator
from .graph import GraphGenerator
from .ranker import Ranker


class MicroDigAlgorithm:
    """Main MicroDig algorithm for microservice failure root cause analysis."""

    def __init__(self, hyper_params: Optional[Dict[str, Any]] = None):
        """
        Initialize MicroDig algorithm.

        Args:
            hyper_params: Optional hyperparameters override
        """
        # Default hyperparameters
        self.hyper_params = {
            "test_length_before": 10,
            "test_length_after": 10,
            "train_length": 60,
            "search_method": "all",
            "rank_method": "random walk",
            "level": "method",
            "rev_weight": 0.2,
            "server_data": False,
            "beta": 0.1,
            "new_col": "final_score",
        }

        if hyper_params:
            self.hyper_params.update(hyper_params)

        # Initialize components
        self.anomaly_detector = AnomalyDetector(self.hyper_params)

        logger.info("MicroDig algorithm initialized")
        logger.debug(f"Hyperparameters: {self.hyper_params}")

    def _extract_service_name(self, name: str, algorithm_name: str) -> Optional[str]:
        """
        Extract service name from result name based on algorithm type.

        Args:
            name: Result name from algorithm
            algorithm_name: Name of the algorithm that produced this result

        Returns:
            Service name or None if extraction fails
        """
        if not name:
            return None

        # If the name already looks like a Train Ticket service, return it directly
        if name.startswith("ts-") and "|" not in name:
            return name

        # Extract service name from API paths like "/api/v1/travelplanservice/..."
        if "/api/v1/" in name:
            import re

            # Extract service name from path
            match = re.search(r"/api/v1/([a-zA-Z0-9_]+)(?:service)?(?:/|$)", name)
            if match:
                service_base = match.group(1)
                # Complete mapping based on Caddy configuration
                service_mapping = {
                    "adminbasicservice": "ts-admin-basic-info-service",
                    "adminorderservice": "ts-admin-order-service",
                    "adminrouteservice": "ts-admin-route-service",
                    "admintravelservice": "ts-admin-travel-service",
                    "adminuserservice": "ts-admin-user-service",
                    "assuranceservice": "ts-assurance-service",
                    "auth": "ts-auth-service",
                    "users": "ts-auth-service",
                    "avatar": "ts-avatar-service",
                    "basicservice": "ts-basic-service",
                    "cancelservice": "ts-cancel-service",
                    "configservice": "ts-config-service",
                    "consignpriceservice": "ts-consign-price-service",
                    "consignservice": "ts-consign-service",
                    "contactservice": "ts-contacts-service",
                    "executeservice": "ts-execute-service",
                    "foodservice": "ts-food-service",
                    "inside_pay_service": "ts-inside-payment-service",
                    "notifyservice": "ts-notification-service",
                    "orderOtherService": "ts-order-other-service",
                    "orderservice": "ts-order-service",
                    "paymentservice": "ts-payment-service",
                    "preserveotherservice": "ts-preserve-other-service",
                    "preserveservice": "ts-preserve-service",
                    "priceservice": "ts-price-service",
                    "rebookservice": "ts-rebook-service",
                    "routeplanservice": "ts-route-plan-service",
                    "routeservice": "ts-route-service",
                    "seatservice": "ts-seat-service",
                    "securityservice": "ts-security-service",
                    "stationfoodservice": "ts-station-food-service",
                    "stationservice": "ts-station-service",
                    "trainfoodservice": "ts-train-food-service",
                    "trainservice": "ts-train-service",
                    "travel2service": "ts-travel2-service",
                    "travelplanservice": "ts-travel-plan-service",
                    "travelservice": "ts-travel-service",
                    "userservice": "ts-user-service",
                    "verifycode": "ts-verification-code-service",
                    "waitorderservice": "ts-wait-order-service",
                    "fooddeliveryservice": "ts-food-delivery-service",
                    # Legacy mappings for backward compatibility
                    "travelplan": "ts-travel-plan-service",
                    "route": "ts-route-service",
                    "order": "ts-order-service",
                    "user": "ts-user-service",
                    "seat": "ts-seat-service",
                    "train": "ts-train-service",
                }

                if service_base in service_mapping:
                    return service_mapping[service_base]
                else:
                    # Generic conversion for unknown services: add ts- prefix and -service suffix
                    return f"ts-{service_base}-service"

        # Extract from controller names like "TravelPlanController.method"
        if "Controller." in name:
            controller_name = name.split("Controller.")[0]
            # Controller to service mapping
            controller_mapping = {
                "TravelPlan": "ts-travel-plan-service",
                "RoutePlan": "ts-route-plan-service",
                "Route": "ts-route-service",
                "Order": "ts-order-service",
                "OrderOther": "ts-order-other-service",
                "User": "ts-user-service",
                "Seat": "ts-seat-service",
                "Train": "ts-train-service",
                "Travel": "ts-travel-service",
                "Travel2": "ts-travel2-service",
                "Basic": "ts-basic-service",
                "Auth": "ts-auth-service",
                "Payment": "ts-payment-service",
                "Preserve": "ts-preserve-service",
                "PreserveOther": "ts-preserve-other-service",
                "Cancel": "ts-cancel-service",
                "Config": "ts-config-service",
                "Contact": "ts-contacts-service",
                "Consign": "ts-consign-service",
                "ConsignPrice": "ts-consign-price-service",
                "Execute": "ts-execute-service",
                "Food": "ts-food-service",
                "FoodDelivery": "ts-food-delivery-service",
                "TrainFood": "ts-train-food-service",
                "StationFood": "ts-station-food-service",
                "Notification": "ts-notification-service",
                "Price": "ts-price-service",
                "Rebook": "ts-rebook-service",
                "Security": "ts-security-service",
                "Station": "ts-station-service",
                "Assurance": "ts-assurance-service",
                "Avatar": "ts-avatar-service",
                "VerificationCode": "ts-verification-code-service",
                "WaitOrder": "ts-wait-order-service",
                "InsidePayment": "ts-inside-payment-service",
                "AdminBasic": "ts-admin-basic-info-service",
                "AdminOrder": "ts-admin-order-service",
                "AdminRoute": "ts-admin-route-service",
                "AdminTravel": "ts-admin-travel-service",
                "AdminUser": "ts-admin-user-service",
            }

            if controller_name in controller_mapping:
                return controller_mapping[controller_name]

        # Skip obvious non-service patterns
        non_service_patterns = [
            "BasicErrorController",
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "HEAD",
            "OPTIONS",
            "PATCH",
        ]

        for pattern in non_service_patterns:
            if pattern == name.strip():  # Exact match for HTTP methods
                return None

        # Handle different algorithm result formats
        if "|" in name:
            parts = name.split("|")

            # Look for Train Ticket service names in the parts
            for part in parts:
                if part.startswith("ts-"):
                    return part

            # Fallback to position-based extraction, but still filter
            potential_service = None
            if algorithm_name.startswith("alg1"):
                # Algorithm 1 method format: server|service|method or caller|callee format
                if len(parts) >= 3:
                    # Method level: server|service|method
                    potential_service = parts[1]  # Service name
                elif len(parts) == 2:
                    # Could be server|service
                    potential_service = parts[1]
                else:
                    potential_service = parts[0]

            elif algorithm_name in ["alg4", "alg5"]:
                # Server-level algorithms, but may contain service info
                if len(parts) >= 2:
                    potential_service = parts[1]  # Try service position
                else:
                    potential_service = parts[0]
            else:
                # Default: try service position first
                if len(parts) >= 2:
                    potential_service = parts[1]
                else:
                    potential_service = parts[0]

            # Apply same extraction logic to potential service
            if potential_service and potential_service.startswith("ts-"):
                return potential_service
        else:
            # No separators, treat as direct service/server name
            # But still check if it's a valid service name
            if name.startswith("ts-"):
                return name

        return None

    def analyze_case(self, algorithm_input: AlgorithmInput) -> AlgorithmOutput:
        """
        Analyze a single failure case.

        Args:
            algorithm_input: Input data and parameters

        Returns:
            Algorithm output with rankings and evaluation results
        """
        start_time = time.time()

        try:
            logger.info(
                f"Starting analysis for case {algorithm_input.case.alarm_start_time}"
            )

            # Update hyperparameters from input
            if hasattr(algorithm_input, "to_dict"):
                self.hyper_params.update(algorithm_input.to_dict())

            # Initialize components for this case
            graph_gen = GraphGenerator(
                self.anomaly_detector, self.hyper_params, algorithm_input.case
            )

            ranker = Ranker(self.hyper_params, algorithm_input.case, graph_gen)

            # Run ranking algorithms based on level
            logger.info(
                f"Running {self.hyper_params['level']}-level ranking algorithms..."
            )

            try:
                if self.hyper_params["level"] == "service":
                    # For service level, use the service node graph
                    graph_gen = GraphGenerator(
                        self.anomaly_detector, self.hyper_params, algorithm_input.case
                    )
                    G_service = graph_gen.get_asso_service_node_ano_graph()[0]

                    if len(G_service) == 0:
                        logger.warning("Empty service graph")
                        alg5_result = pd.DataFrame()
                    else:
                        # Create rankings for service-level nodes
                        rankings = ranker._do_rank(G_service, "score")
                        alg5_result = pd.DataFrame(
                            [(name, score) for name, score in rankings.items()],
                            columns=["name", "final_score"],
                        )
                else:
                    # For method level, use server node ranking
                    alg5_result = ranker.server_node_rank()

                results = {"alg5": alg5_result}
                logger.info(
                    f"{self.hyper_params['level'].capitalize()} ranking algorithm completed"
                )
            except Exception as e:
                logger.error(f"Ranking failed: {e}")
                results = {}

            # Create output
            output = AlgorithmOutput(
                case_name=algorithm_input.case.alarm_start_time,
                processing_time=time.time() - start_time,
                success=True,
            )

            # Extract and aggregate service rankings
            service_scores = {}  # service_name -> max_score

            # Process Algorithm 5 results and aggregate by service
            if (
                "alg5" in results
                and results["alg5"] is not None
                and not results["alg5"].empty
            ):
                result_df = results["alg5"]
                logger.debug(f"Processing server ranking with {len(result_df)} results")

                for _, row in result_df.iterrows():
                    name = str(row["name"])
                    score = float(row["final_score"])

                    logger.debug(f"Processing result: {name} (score: {score:.4f})")

                    # Extract service name from method-level result
                    service_name = None

                    # If it's already a service name (ts-service format)
                    if name.startswith("ts-") and "|" not in name:
                        service_name = name
                        logger.debug(f"  -> Direct service name: {service_name}")
                    # If it's a method-level name (ts-service|method format)
                    elif "|" in name and name.startswith("ts-"):
                        service_name = name.split("|")[0]
                        logger.debug(f"  -> Extracted from method: {service_name}")
                    # Try other extraction patterns for non-ts names
                    else:
                        # For non-ts names, be more lenient to get more results
                        if "|" in name:
                            parts = name.split("|")
                            # Look for any part that looks like a service
                            for part in parts:
                                if part.startswith("ts-"):
                                    service_name = part
                                    logger.debug(
                                        f"  -> Found ts- service in parts: {service_name}"
                                    )
                                    break

                        # If still no service found, try the extraction function
                        if not service_name:
                            extracted = self._extract_service_name(name, "alg5")
                            if extracted:
                                service_name = extracted
                                logger.debug(
                                    f"  -> Extracted via function: {service_name}"
                                )
                            else:
                                logger.debug(
                                    f"  -> No service name found, skipping: {name}"
                                )

                    if service_name:
                        # Aggregate scores by service (take maximum score)
                        if (
                            service_name not in service_scores
                            or score > service_scores[service_name]
                        ):
                            service_scores[service_name] = score
                        logger.debug(
                            f"  -> Final aggregated service: {service_name} (score: {score:.4f})"
                        )
                    else:
                        logger.debug(f"  -> Filtered out: {name}")

            # Sort services by score
            sorted_services = sorted(
                service_scores.items(), key=lambda x: x[1], reverse=True
            )
            unique_ranking = [service_name for service_name, _ in sorted_services]

            output.service_ranking = unique_ranking

            logger.info(
                f"Analysis completed for case {algorithm_input.case.alarm_start_time} "
                f"in {output.processing_time:.2f}s"
            )

            return output

        except Exception as e:
            error_msg = f"Error analyzing case {algorithm_input.case.alarm_start_time}: {str(e)}"
            logger.error(error_msg)

            return AlgorithmOutput(
                case_name=algorithm_input.case.alarm_start_time,
                processing_time=time.time() - start_time,
                success=False,
                error_message=error_msg,
            )

    def analyze_multiple_cases(
        self, cases: List[AlgorithmInput], output_dir: str = "./results"
    ) -> Dict[str, Any]:
        """
        Analyze multiple failure cases.

        Args:
            cases: List of algorithm inputs
            output_dir: Directory to save results

        Returns:
            Dictionary with aggregated results and evaluation metrics
        """
        logger.info(f"Starting analysis of {len(cases)} cases")

        # Initialize evaluators for different algorithms
        evaluator1 = Evaluator(f"{output_dir}/results-alg1")
        evaluator4 = Evaluator(f"{output_dir}/results-alg4")
        evaluator5 = Evaluator(f"{output_dir}/results-alg5")

        successful_cases = 0
        failed_cases = 0
        all_results = []

        for i, case_input in enumerate(cases):
            logger.info(
                f"Processing case {i + 1}/{len(cases)}: {case_input.case.alarm_start_time}"
            )

            # Analyze single case
            output = self.analyze_case(case_input)
            all_results.append(output)

            if output.success:
                successful_cases += 1

                # Evaluate service-level results
                try:
                    if output.service_ranking:
                        # Create DataFrame for evaluation
                        service_df = pd.DataFrame(
                            {
                                "name": output.service_ranking,
                                "final_score": [
                                    1.0 / (i + 1)
                                    for i in range(len(output.service_ranking))
                                ],  # Simple scoring
                            }
                        )
                        evaluator1.process_result_server(service_df, case_input.case)

                except Exception as e:
                    logger.error(
                        f"Error evaluating case {case_input.case.alarm_start_time}: {e}"
                    )

            else:
                failed_cases += 1
                logger.warning(f"Case analysis failed: {output.error_message}")

        # Save final evaluation results
        logger.info("Saving evaluation results...")

        evaluator1.save_final_result("server")
        evaluator1.save_final_result("method")
        evaluator4.save_final_result("server")
        evaluator5.save_final_result("server")

        # Get final metrics
        metrics1_server, _ = evaluator1.get_final_result("server")
        metrics1_method, _ = evaluator1.get_final_result("method")
        metrics4, _ = evaluator4.get_final_result("server")
        metrics5, _ = evaluator5.get_final_result("server")

        # Aggregate results
        summary = {
            "total_cases": len(cases),
            "successful_cases": successful_cases,
            "failed_cases": failed_cases,
            "success_rate": successful_cases / len(cases) if cases else 0,
            "avg_processing_time": sum(r.processing_time for r in all_results)
            / len(all_results)
            if all_results
            else 0,
            "metrics": {
                "algorithm1_server": metrics1_server,
                "algorithm1_method": metrics1_method,
                "algorithm4": metrics4,
                "algorithm5": metrics5,
            },
        }

        logger.info(
            f"Analysis summary: {successful_cases}/{len(cases)} cases successful"
        )
        logger.info(f"Average processing time: {summary['avg_processing_time']:.2f}s")

        return summary
