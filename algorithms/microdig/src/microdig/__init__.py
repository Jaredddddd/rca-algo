"""
MicroDig: Microservice Failure Root Cause Analysis

This package provides tools for analyzing microservice failure patterns
and identifying root causes using graph-based anomaly detection.
"""

__version__ = "1.0.0"
__author__ = "MicroDig Team"

# Import main components
from .alarm_detector import AlarmDetector
from .algorithm import MicroDigAlgorithm
from .anomaly import AnomalyDetector
from .cli import app as cli_app
from .data_loader import DataLoader
from .data_structures import AlgorithmInput, AlgorithmOutput, CaseModel, TraceData
from .evaluator import Evaluator
from .graph import GraphGenerator
from .platform_adapter import MicroDig, MicroDigAdapter, microdig_analysis
from .ranker import Ranker

__all__ = [
    "MicroDigAlgorithm",
    "CaseModel",
    "TraceData",
    "AlgorithmInput",
    "AlgorithmOutput",
    "AnomalyDetector",
    "GraphGenerator",
    "Ranker",
    "Evaluator",
    "DataLoader",
    "MicroDig",
    "microdig_analysis",
    "MicroDigAdapter",
    "cli_app",
    "AlarmDetector",
]
