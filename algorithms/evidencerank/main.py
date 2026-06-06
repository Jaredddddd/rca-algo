#!/usr/bin/env -S uv run -s
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from patches.rcabench_cli import main
from rcabench_platform.v2.algorithms.spec import global_algorithm_registry

from src.evidencerank.algorithm import (
    EvidenceRank,
    EvidenceRankLog,
    EvidenceRankLogTrace,
    EvidenceRankMetric,
    EvidenceRankMetricLog,
    EvidenceRankMetricTrace,
    EvidenceRankTrace,
    EvidenceRankARC,
)
from src.evidencerank.cera import (
    CERA,
    CERALog,
    CERALogTrace,
    CERAMetric,
    CERAMetricLog,
    CERAMetricTrace,
    CERATrace,
)
from src.evidencerank.crest import (
    CREST,
    CRESTLocal,
    CRESTNoCF,
    CRESTNoCalib,
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
    registry["evidencerank_arc"] = EvidenceRankARC
    registry["cera"] = CERA
    registry["cera_metric"] = CERAMetric
    registry["cera_log"] = CERALog
    registry["cera_trace"] = CERATrace
    registry["cera_metric_log"] = CERAMetricLog
    registry["cera_metric_trace"] = CERAMetricTrace
    registry["cera_log_trace"] = CERALogTrace
    registry["crest"] = CREST
    registry["crest_local"] = CRESTLocal
    registry["crest_nocf"] = CRESTNoCF
    registry["crest_nocalib"] = CRESTNoCalib

    main(enable_builtin_algorithms=False)
