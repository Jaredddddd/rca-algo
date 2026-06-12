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
from crest.algorithm import (
    CREST,
    CRESTLog,
    CRESTLogTrace,
    CRESTLocal,
    CRESTMetric,
    CRESTMetricLog,
    CRESTMetricTrace,
    CRESTNoCF,
    CRESTTrace,
)
from crest.meo_algorithm import CRESTMEO, CRESTMEOBuiltIn

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
    registry["crest_metric"] = CRESTMetric
    registry["crest_log"] = CRESTLog
    registry["crest_trace"] = CRESTTrace
    registry["crest_metric_log"] = CRESTMetricLog
    registry["crest_metric_trace"] = CRESTMetricTrace
    registry["crest_log_trace"] = CRESTLogTrace
    registry["crest_local"] = CRESTLocal
    registry["crest_nocf"] = CRESTNoCF
    registry["crest_meo"] = CRESTMEO
    registry["crest_meo_builtin"] = CRESTMEOBuiltIn

    main(enable_builtin_algorithms=False)
