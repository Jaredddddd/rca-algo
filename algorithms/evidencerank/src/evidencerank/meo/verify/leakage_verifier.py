"""Leakage checks for EvidenceOperatorSpec objects."""

from __future__ import annotations

import json
from dataclasses import asdict

from ..dsl.schema import EvidenceOperatorSpec


FORBIDDEN_TOKENS = {
    "ground" + "_truth",
    "root_cause",
    "root_service",
    "root_metric",
    "answer",
    "label",
    "rank",
    "torai_wrong",
    "baseline_output",
}


def leakage_verify(spec: EvidenceOperatorSpec) -> tuple[bool, list[str]]:
    """Reject specs that mention answer, label, or prior-output metadata."""

    text = json.dumps(asdict(spec), sort_keys=True).lower()
    hits = sorted(token for token in FORBIDDEN_TOKENS if token in text)
    return len(hits) == 0, hits

