#!/usr/bin/env -S uv run -s
from rcabench_platform.v2.cli.main import main
from rcabench_platform.v2.algorithms.spec import global_algorithm_registry

from src.evidencerank.algorithm import (
    EvidenceRank,
    EvidenceRankLog,
    EvidenceRankLogTrace,
    EvidenceRankMetric,
    EvidenceRankMetricLog,
    EvidenceRankMetricTrace,
    EvidenceRankTrace,
)

if __name__ == "__main__":
    registry = global_algorithm_registry()
    registry["evidencerank"] = EvidenceRank
    registry["evidencerank_metric"] = EvidenceRankMetric
    registry["evidencerank_log"] = EvidenceRankLog
    registry["evidencerank_trace"] = EvidenceRankTrace
    registry["evidencerank_metric_log"] = EvidenceRankMetricLog
    registry["evidencerank_metric_trace"] = EvidenceRankMetricTrace
    registry["evidencerank_log_trace"] = EvidenceRankLogTrace

    main(enable_builtin_algorithms=False)
