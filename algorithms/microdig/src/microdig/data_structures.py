"""
Data structures for MicroDig algorithm.

This module defines the core data structures used throughout the MicroDig
microservice failure root cause analysis algorithm.
"""

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TraceData:
    """Represents processed trace data for a single trace."""

    trace_id: str
    span_id: str
    parent_span_id: str
    service_name: str
    operation_name: str
    start_time: str
    duration: float
    span_kind: str
    status: int
    http_status: int
    error: bool
    method: str
    service: str


@dataclass
class CaseModel:
    """Represents a failure case with all related metrics and metadata."""

    # Basic case information
    alarm_start_time: str
    alarm_end_time: str
    alarm_start_minute: int
    alarm_end_minute: int
    monitor_id: int
    alarm_item: str
    sli_type: str
    where_info: Dict[str, Any]

    # Analysis results
    callings: Dict[str, Any] = field(default_factory=dict)
    alarm_callings: Dict[str, Any] = field(default_factory=dict)
    rc: List[str] = field(default_factory=list)  # root causes
    changed: bool = False
    server_num: int = 0

    @classmethod
    def from_datetime(
        cls,
        alarm_start_time: datetime.datetime,
        alarm_end_time: datetime.datetime,
        monitor_id: int,
        alarm_item: str,
        sli_type: str,
        where_info: Dict[str, Any],
    ) -> "CaseModel":
        """Create CaseModel from datetime objects."""
        return cls(
            alarm_start_time=str(alarm_start_time),
            alarm_end_time=str(alarm_end_time),
            alarm_start_minute=alarm_start_time.hour * 60 + alarm_start_time.minute,
            alarm_end_minute=alarm_end_time.hour * 60 + alarm_end_time.minute,
            monitor_id=monitor_id,
            alarm_item=alarm_item,
            sli_type=sli_type,
            where_info=where_info,
        )


@dataclass
class AlgorithmInput:
    """Input structure for the MicroDig algorithm."""

    # Configuration parameters
    test_length_before: int = 10
    test_length_after: int = 10
    train_length: int = 60
    search_method: str = "all"  # ['all', 'deepest2', 'last2']
    rank_method: str = "random walk"  # ['pagerank', 'random walk']
    level: str = "service"  # Always use service level
    rev_weight: float = 0.2
    server_data: bool = False
    beta: float = 0.1
    new_col: str = "final_score"

    # Data (required)
    case: CaseModel = field(
        default_factory=lambda: CaseModel("", "", 0, 0, 0, "", "", {})
    )
    trace_data: List[TraceData] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return {
            "test_length_before": self.test_length_before,
            "test_length_after": self.test_length_after,
            "train_length": self.train_length,
            "search_method": self.search_method,
            "rank_method": self.rank_method,
            "level": self.level,
            "rev_weight": self.rev_weight,
            "server_data": self.server_data,
            "beta": self.beta,
            "new_col": self.new_col,
        }


@dataclass
class AlgorithmOutput:
    """Output structure for the MicroDig algorithm."""

    # Service-level rankings (simplified)
    service_ranking: List[str] = field(
        default_factory=list
    )  # Just service names in order

    # Evaluation metrics
    evaluation_results: Dict[str, Any] = field(default_factory=dict)

    # Additional information
    case_name: str = ""
    processing_time: float = 0.0
    success: bool = True
    error_message: str = ""
