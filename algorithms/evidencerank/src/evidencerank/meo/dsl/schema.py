"""Typed schema for CREST Meta Evidence Operators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RoleName = Literal[
    "mutation",
    "propagation",
    "observability_bias",
    "topology_context",
]
SourceName = Literal["metric", "log", "trace", "topology"]
EntityName = Literal["service", "endpoint", "edge", "log_template", "status_code"]
SignalType = Literal["value", "count", "rate", "duration", "categorical"]
ContrastOperator = Literal[
    "z_shift",
    "robust_z_shift",
    "mean_delta",
    "count_delta",
    "count_rise",
    "count_drop",
    "rate_delta",
    "error_rate_delta",
    "distribution_shift",
    "novelty",
]
AggregationMethod = Literal["max", "mean", "sum", "p95", "ratio", "jsd"]


@dataclass(frozen=True)
class SignalSpec:
    """Input telemetry signal selected by an evidence operator."""

    field: str
    type: SignalType


@dataclass(frozen=True)
class ContrastSpec:
    """Normal-vs-abnormal contrast atom for an evidence operator."""

    operator: ContrastOperator
    normal_window: str = "pre_anomaly"
    abnormal_window: str = "post_anomaly"


@dataclass(frozen=True)
class AggregationSpec:
    """Service-level aggregation metadata for an evidence operator."""

    level: str = "service"
    method: AggregationMethod = "max"


@dataclass(frozen=True)
class EvidenceOperatorSpec:
    """Serializable specification for a deterministic evidence feature."""

    name: str
    source: SourceName
    entity: EntityName
    signal: SignalSpec
    contrast: ContrastSpec
    aggregation: AggregationSpec
    role_prior: dict[str, float]
    mechanism: str
    required_fields: list[str]
    rationale: str


def parse_operator_spec(raw: dict) -> EvidenceOperatorSpec:
    """Parse a JSON dictionary into an EvidenceOperatorSpec."""

    signal = raw.get("signal", {})
    contrast = raw.get("contrast", {})
    aggregation = raw.get("aggregation", {})
    return EvidenceOperatorSpec(
        name=str(raw["name"]),
        source=raw["source"],
        entity=raw["entity"],
        signal=SignalSpec(
            field=str(signal["field"]),
            type=signal["type"],
        ),
        contrast=ContrastSpec(
            operator=contrast["operator"],
            normal_window=str(contrast.get("normal_window", "pre_anomaly")),
            abnormal_window=str(contrast.get("abnormal_window", "post_anomaly")),
        ),
        aggregation=AggregationSpec(
            level=str(aggregation.get("level", "service")),
            method=aggregation.get("method", "max"),
        ),
        role_prior={str(key): float(value) for key, value in raw["role_prior"].items()},
        mechanism=str(raw.get("mechanism", "")),
        required_fields=[str(field) for field in raw.get("required_fields", [])],
        rationale=str(raw.get("rationale", "")),
    )

