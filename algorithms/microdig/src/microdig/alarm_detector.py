"""
Alarm Item Detector

This module automatically detects the alarm service from conclusion.parquet
based on the severity of issues detected in different services.
"""

import json
import math
import re
from pathlib import Path
from typing import Dict, Optional

import polars as pl
from rcabench_platform.v2.logging import logger


class AlarmDetector:
    """Detects alarm services from conclusion data"""

    def __init__(self, input_folder: Path):
        """
        Initialize the alarm detector.

        Args:
            input_folder: Path to the data folder containing conclusion.parquet
        """
        self.input_folder = Path(input_folder)
        self.conclusion_file = self.input_folder / "conclusion.parquet"
        self.service_mapping = self._build_service_mapping()

    def _build_service_mapping(self) -> Dict[str, str]:
        """
        Build mapping from URL paths to service names based on common patterns.
        This is derived from the Caddyfile routing rules.
        """
        # Complete mapping based on the Caddyfile routing rules provided
        url_to_service = {
            "/api/v1/adminbasicservice": "ts-admin-basic-info-service",
            "/api/v1/adminorderservice": "ts-admin-order-service",
            "/api/v1/adminrouteservice": "ts-admin-route-service",
            "/api/v1/admintravelservice": "ts-admin-travel-service",
            "/api/v1/adminuserservice": "ts-admin-user-service",
            "/api/v1/assuranceservice": "ts-assurance-service",
            "/api/v1/auth": "ts-auth-service",
            "/api/v1/users": "ts-auth-service",
            "/api/v1/avatar": "ts-avatar-service",
            "/api/v1/basicservice": "ts-basic-service",
            "/api/v1/cancelservice": "ts-cancel-service",
            "/api/v1/configservice": "ts-config-service",
            "/api/v1/consignpriceservice": "ts-consign-price-service",
            "/api/v1/consignservice": "ts-consign-service",
            "/api/v1/contactservice": "ts-contacts-service",
            "/api/v1/executeservice": "ts-execute-service",
            "/api/v1/foodservice": "ts-food-service",
            "/api/v1/inside_pay_service": "ts-inside-payment-service",
            "/api/v1/notifyservice": "ts-notification-service",
            "/api/v1/orderOtherService": "ts-order-other-service",
            "/api/v1/orderservice": "ts-order-service",
            "/api/v1/paymentservice": "ts-payment-service",
            "/api/v1/preserveotherservice": "ts-preserve-other-service",
            "/api/v1/preserveservice": "ts-preserve-service",
            "/api/v1/priceservice": "ts-price-service",
            "/api/v1/rebookservice": "ts-rebook-service",
            "/api/v1/routeplanservice": "ts-route-plan-service",
            "/api/v1/routeservice": "ts-route-service",
            "/api/v1/seatservice": "ts-seat-service",
            "/api/v1/securityservice": "ts-security-service",
            "/api/v1/stationfoodservice": "ts-station-food-service",
            "/api/v1/stationservice": "ts-station-service",
            "/api/v1/trainfoodservice": "ts-train-food-service",
            "/api/v1/trainservice": "ts-train-service",
            "/api/v1/travel2service": "ts-travel2-service",
            "/api/v1/travelplanservice": "ts-travel-plan-service",
            "/api/v1/travelservice": "ts-travel-service",
            "/api/v1/userservice": "ts-user-service",
            "/api/v1/verifycode": "ts-verification-code-service",
            "/api/v1/waitorderservice": "ts-wait-order-service",
            "/api/v1/fooddeliveryservice": "ts-food-delivery-service",
        }
        return url_to_service

    @staticmethod
    def _normalize_service_name(service_name: str) -> Optional[str]:
        """Normalize service identifiers to the RCABench service label style."""
        if not service_name:
            return None

        normalized = service_name.strip().strip("/")
        if not normalized:
            return None

        normalized = normalized.split(":", 1)[0]
        normalized = normalized.replace("_", "-")
        normalized = normalized.lower()
        if normalized.startswith("hipstershop."):
            normalized = normalized.rsplit(".", 1)[-1]

        if normalized == "redis":
            return "redis-cart"

        return normalized

    def _extract_service_from_span(self, span_name: str) -> Optional[str]:
        """
        Extract service name from span name using URL mapping.

        Args:
            span_name: The span name like "HTTP POST http://ts-ui-dashboard:8080/api/v1/preserveservice/preserve"

        Returns:
            Service name or None if not found
        """
        if not span_name:
            return None

        text = span_name.strip()

        # Extract URL path from Train Ticket span names.
        # Pattern: "HTTP METHOD http://host:port/path"
        url_pattern = r"HTTP\s+\w+\s+http://[^:]+:\d+(/api/v1/[^/]+)"
        match = re.search(url_pattern, text)

        if match:
            api_path = match.group(1)
            service_name = self.service_mapping.get(api_path)
            if service_name:
                logger.debug(f"Mapped {api_path} -> {service_name}")
                return service_name
            else:
                logger.warning(f"No service mapping found for {api_path}")

        # Extract service names from AIOps/HipsterShop gRPC-style names, such as:
        # "hipstershop.CartService/AddItem", "/hipstershop.CartService/GetCart",
        # "hipstershop.Frontend/Recv.", or "POST /hipstershop.CartService/AddItem".
        service_match = re.search(
            r"(?:^|\s|/)(?:[A-Za-z0-9_-]+\.)?([A-Za-z0-9_-]+Service|Frontend)(?:/|$)",
            text,
            flags=re.IGNORECASE,
        )
        if service_match:
            return self._normalize_service_name(service_match.group(1))

        logger.debug(f"Could not extract service from span: {span_name}")

        return None

    def _calculate_row_fallback_score(self, row: Dict) -> float:
        """Score a conclusion row when explicit issue JSON is absent."""
        score = 0.0

        normal_success = row.get("NormalSuccRate")
        abnormal_success = row.get("AbnormalSuccRate")
        if isinstance(normal_success, (int, float)) and isinstance(
            abnormal_success, (int, float)
        ):
            score += max(0.0, float(normal_success) - float(abnormal_success)) * 1000

        normal_duration = row.get("NormalAvgDuration")
        abnormal_duration = row.get("AbnormalAvgDuration")
        if (
            isinstance(normal_duration, (int, float))
            and isinstance(abnormal_duration, (int, float))
            and math.isfinite(float(normal_duration))
            and math.isfinite(float(abnormal_duration))
        ):
            if float(normal_duration) > 0:
                score += max(
                    0.0,
                    (float(abnormal_duration) - float(normal_duration))
                    / float(normal_duration),
                ) * 10
            elif float(abnormal_duration) > 0:
                score += float(abnormal_duration) * 10

        return score

    def _parse_issues(self, issues_str: str) -> Dict[str, dict]:
        """
        Parse the issues JSON string.

        Args:
            issues_str: JSON string containing issue information

        Returns:
            Dictionary of parsed issues
        """
        if not issues_str or issues_str.strip() == "{}":
            return {}

        try:
            return json.loads(issues_str)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse issues JSON: {e}")
            return {}

    def _calculate_severity_score(self, issues: Dict[str, dict]) -> float:
        """
        Calculate severity score for issues.

        Priority:
        1. Number of issues (more issues = higher severity)
        2. Change rate (higher change rate = higher severity)
        3. SLO violation status

        Args:
            issues: Dictionary of issues

        Returns:
            Severity score (higher = more severe)
        """
        if not issues:
            return 0.0

        num_issues = len(issues)
        total_change_rate = 0.0
        slo_violations = 0

        for issue_type, issue_data in issues.items():
            if isinstance(issue_data, dict):
                # Get change rate
                change_rate = issue_data.get("change_rate", 0.0)
                if isinstance(change_rate, (int, float)):
                    total_change_rate += float(change_rate)

                # Count SLO violations
                if issue_data.get("slo_violated", False):
                    slo_violations += 1

        # Calculate composite score
        # Primary: number of issues
        # Secondary: average change rate
        # Tertiary: SLO violations
        avg_change_rate = total_change_rate / num_issues if num_issues > 0 else 0.0

        severity_score = (
            num_issues * 1000  # Primary factor
            + avg_change_rate * 10  # Secondary factor
            + slo_violations * 1
        )  # Tertiary factor

        logger.debug(
            f"Calculated severity: {num_issues} issues, "
            f"avg change rate {avg_change_rate:.2f}, "
            f"{slo_violations} SLO violations, "
            f"score {severity_score:.2f}"
        )

        return severity_score

    def detect_alarm_service(self) -> Optional[str]:
        """
        Detect the alarm service from conclusion.parquet.

        Returns:
            Service name with the highest severity issues, or None if no issues found
        """
        if not self.conclusion_file.exists():
            logger.error(f"Conclusion file not found: {self.conclusion_file}")
            return None

        try:
            # Load conclusion data
            logger.info(f"Loading conclusion data from {self.conclusion_file}")
            df = pl.read_parquet(self.conclusion_file)

            if df.is_empty():
                logger.warning("Conclusion data is empty")
                return None

            if "SpanName" not in df.columns or "Issues" not in df.columns:
                logger.error(
                    "Required columns (SpanName, Issues) not found in conclusion data"
                )
                return None

            service_severity_map = {}

            # Process each row
            for row in df.iter_rows(named=True):
                span_name = row.get("SpanName", "")
                issues_str = row.get("Issues", "{}")  # Note: capital 'I'

                # Extract service name
                service_name = self._extract_service_from_span(span_name)
                if not service_name:
                    continue

                # Parse issues
                issues = self._parse_issues(issues_str)
                severity = (
                    self._calculate_severity_score(issues)
                    if issues
                    else self._calculate_row_fallback_score(row)
                )
                if severity > 0:
                    current = service_severity_map.get(
                        service_name, (0.0, 0, {})
                    )
                    service_severity_map[service_name] = (
                        current[0] + severity,
                        current[1] + len(issues),
                        issues or current[2],
                    )
                    logger.info(
                        f"Service {service_name}: severity {severity:.2f}, {len(issues)} issues"
                    )

            service_severities = [
                (service, severity, num_issues, issues)
                for service, (severity, num_issues, issues) in service_severity_map.items()
            ]

            if not service_severities:
                logger.warning("No services with issues found")
                return None

            # Sort by severity (descending) and pick the most severe
            service_severities.sort(key=lambda x: x[1], reverse=True)

            most_severe_service = service_severities[0][0]
            most_severe_score = service_severities[0][1]
            most_severe_issues = service_severities[0][2]

            logger.info(
                f"Selected alarm service: {most_severe_service} "
                f"(severity: {most_severe_score:.2f}, {most_severe_issues} issues)"
            )

            # Log all services for reference
            logger.info("All services with issues (ranked by severity):")
            for i, (service, severity, num_issues, issues) in enumerate(
                service_severities[:5]
            ):
                logger.info(
                    f"  {i + 1}. {service}: {severity:.2f} ({num_issues} issues)"
                )

            return most_severe_service

        except Exception as e:
            logger.error(f"Failed to detect alarm service: {e}")
            return None

    def get_issue_summary(self, service_name: str) -> Dict:
        """
        Get detailed issue summary for a specific service.

        Args:
            service_name: Name of the service to get issues for

        Returns:
            Dictionary containing issue details
        """
        try:
            df = pl.read_parquet(self.conclusion_file)

            for row in df.iter_rows(named=True):
                span_name = row.get("SpanName", "")
                issues_str = row.get("Issues", "{}")  # Note: capital 'I'

                extracted_service = self._extract_service_from_span(span_name)
                if extracted_service == service_name:
                    issues = self._parse_issues(issues_str)
                    return {
                        "service": service_name,
                        "span_name": span_name,
                        "issues": issues,
                        "severity": self._calculate_severity_score(issues),
                    }

            return {}

        except Exception as e:
            logger.error(f"Failed to get issue summary for {service_name}: {e}")
            return {}
