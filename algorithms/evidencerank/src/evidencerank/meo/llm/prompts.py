"""Prompt templates for offline CREST-MEO operator synthesis."""

from __future__ import annotations

import json
from typing import Any


MEO_OPERATOR_SYNTHESIS_PROMPT = """
You are an expert SRE and telemetry feature designer.

Your task is to synthesize a Meta Evidence Operator Library (MEOL) for
microservice root cause analysis. You must only output JSON. Do not output
Python code. Operators must be computable from normal and abnormal telemetry
windows by the CREST-MEO DSL compiler.

Rules:
1. Use only allowed DSL atoms.
2. Do not depend on a specific service name, incident id, datapack id,
   evaluation outcome metadata, injected-fault metadata, or prior method output.
3. Assign counterfactual role membership through role_prior: mutation,
   propagation, or neutral. Use mutation=1 only for root-local mechanism-change
   evidence, propagation=1 only for propagated symptom evidence, and all-zero
   mutation/propagation for neutral local evidence. Do not set mutation and
   propagation at the same time.
4. Include mechanism, rationale, and required_fields for every operator.
5. The online RCA path must remain deterministic over the frozen JSON library.
""".strip()


DSL_ALLOWED_ATOMS = {
    "sources": ["metric", "log", "trace", "topology"],
    "entities": ["service", "endpoint", "edge", "log_template", "status_code"],
    "signal_types": ["value", "count", "rate", "duration", "categorical"],
    "contrast_operators": [
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
    ],
    "aggregation_methods": ["max", "mean", "sum", "p95", "ratio", "jsd"],
}


DEFAULT_MECHANISM_CATALOG = [
    {
        "mechanism": "service hang or disappearance",
        "observable_consequences": [
            "request count drops",
            "trace count drops",
            "metric rows may disappear",
        ],
        "typical_roles": ["mutation"],
    },
    {
        "mechanism": "interface failure",
        "observable_consequences": [
            "status code distribution changes",
            "error rate increases",
            "error logs increase",
        ],
        "typical_roles": ["mutation"],
    },
    {
        "mechanism": "dependency slowdown",
        "observable_consequences": [
            "trace duration increases",
            "latency propagates across service calls",
            "log volume can increase due to retries",
        ],
        "typical_roles": ["propagation"],
    },
    {
        "mechanism": "retry or backpressure",
        "observable_consequences": [
            "trace count rises",
            "log count rises",
            "latency increases in connected services",
        ],
        "typical_roles": ["propagation"],
    },
    {
        "mechanism": "neutral local evidence",
        "observable_consequences": [
            "metric magnitude shifts or volume signals can support local energy",
            "the signal is not specific enough for counterfactual explain-away",
        ],
        "typical_roles": ["neutral"],
    },
]


def build_operator_synthesis_prompt(
    *,
    artifact_summary: dict[str, Any] | None = None,
    telemetry_schema: dict[str, Any] | None = None,
    mechanism_catalog: list[dict[str, Any]] | None = None,
    extra_context: dict[str, Any] | None = None,
) -> str:
    """Build a DSL-constrained prompt from mined offline artifacts."""

    payload = {
        "artifact_summary": artifact_summary or {},
        "telemetry_schema": telemetry_schema or {},
        "mechanism_catalog": mechanism_catalog or DEFAULT_MECHANISM_CATALOG,
        "dsl_allowed_atoms": DSL_ALLOWED_ATOMS,
        "extra_context": extra_context or {},
        "expected_output_schema": {
            "library_name": "string",
            "dsl_version": "string",
            "generator": "object",
            "roles": [
                "mutation",
                "propagation",
                "neutral",
            ],
            "operators": [
                {
                    "name": "string",
                    "source": "metric|log|trace|topology",
                    "entity": "service|endpoint|edge|log_template|status_code",
                    "signal": {"field": "string", "type": "value|count|rate|duration|categorical"},
                    "contrast": {
                        "operator": "allowed contrast operator",
                        "normal_window": "pre_anomaly",
                        "abnormal_window": "post_anomaly",
                    },
                    "aggregation": {"level": "service", "method": "allowed aggregation method"},
                    "role_prior": {
                        "mutation": 0.0,
                        "propagation": 0.0,
                        "observability_bias": 0.0,
                        "topology_context": 0.0,
                    },
                    "mechanism": "string",
                    "required_fields": ["string"],
                    "rationale": "string",
                }
            ],
        },
    }
    return (
        MEO_OPERATOR_SYNTHESIS_PROMPT
        + "\n\nInput JSON:\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n\nReturn the MEOL JSON object only."
    )
