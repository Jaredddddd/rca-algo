"""Mock MEOL output used while real LLM synthesis is intentionally disabled."""

from __future__ import annotations

from typing import Any


MOCK_ARTIFACT_SUMMARY: dict[str, Any] = {
    "services": [],
    "source_artifacts": [],
    "deployment_artifacts": [],
    "notes": [
        "Phase-1 mock context intentionally contains no incident ids, labels, or service priors.",
    ],
}


MOCK_TELEMETRY_SCHEMA: dict[str, Any] = {
    "normal_metrics": {
        "columns": ["time", "service_name", "metric", "value"],
        "semantic_hints": ["resource", "availability", "performance"],
    },
    "abnormal_metrics": {
        "columns": ["time", "service_name", "metric", "value"],
        "semantic_hints": ["resource", "availability", "performance"],
    },
    "normal_traces": {
        "columns": ["service_name", "endpoint", "status_code", "duration"],
        "semantic_hints": ["interface", "latency", "traffic"],
    },
    "abnormal_traces": {
        "columns": ["service_name", "endpoint", "status_code", "duration"],
        "semantic_hints": ["interface", "latency", "traffic"],
    },
    "normal_logs": {
        "columns": ["service_name", "template", "level", "message"],
        "semantic_hints": ["software_event", "error_event"],
    },
    "abnormal_logs": {
        "columns": ["service_name", "template", "level", "message"],
        "semantic_hints": ["software_event", "error_event"],
    },
}


MOCK_MECHANISM_CATALOG: list[dict[str, Any]] = [
    {
        "mechanism": "service hang or telemetry disappearance",
        "observable_consequences": ["metric rows drop", "trace rows drop"],
        "typical_roles": ["mutation"],
    },
    {
        "mechanism": "interface failure",
        "observable_consequences": ["status-code shift", "error-rate rise"],
        "typical_roles": ["mutation"],
    },
    {
        "mechanism": "endpoint behavior change",
        "observable_consequences": ["endpoint mix changes"],
        "typical_roles": ["mutation"],
    },
    {
        "mechanism": "latency propagation",
        "observable_consequences": ["duration shift", "retry amplification"],
        "typical_roles": ["propagation"],
    },
    {
        "mechanism": "software event distribution shift",
        "observable_consequences": ["log count changes", "template mix changes"],
        "typical_roles": ["propagation"],
    },
]


def _operator(
    name: str,
    source: str,
    entity: str,
    field: str,
    signal_type: str,
    contrast_operator: str,
    aggregation_method: str,
    role_prior: dict[str, float],
    mechanism: str,
    required_fields: list[str],
    rationale: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "source": source,
        "entity": entity,
        "signal": {
            "field": field,
            "type": signal_type,
        },
        "contrast": {
            "operator": contrast_operator,
            "normal_window": "pre_anomaly",
            "abnormal_window": "post_anomaly",
        },
        "aggregation": {
            "level": "service",
            "method": aggregation_method,
        },
        "role_prior": role_prior,
        "mechanism": mechanism,
        "required_fields": required_fields,
        "rationale": rationale,
    }


def mock_meol() -> dict[str, Any]:
    """Return the frozen Phase 1 mock MEOL structure."""

    return {
        "library_name": "crest-meol-default-v1",
        "dsl_version": "1.0",
        "generator": {
            "type": "mock_llm",
            "prompt_version": "meo_operator_synthesis_v1",
            "telemetry_only": True,
            "deterministic_runtime": True,
        },
        "roles": [
            "mutation",
            "propagation",
            "neutral",
        ],
        "operators": [
            _operator(
                "metric_max_z",
                "metric",
                "service",
                "*",
                "value",
                "z_shift",
                "max",
                {
                    "mutation": 0.0,
                    "propagation": 0.0,
                    "observability_bias": 0.0,
                    "topology_context": 0.0,
                },
                "resource or performance magnitude shift",
                ["time", "service_name", "value"],
                "Large metric z shifts provide local evidence but are neutral for counterfactual mutation/propagation explain-away.",
            ),
            _operator(
                "metric_count_drop_shift",
                "metric",
                "service",
                "__row_count__",
                "count",
                "count_drop",
                "ratio",
                {
                    "mutation": 1.00,
                    "propagation": 0.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "service hang or telemetry disappearance",
                ["time", "service_name"],
                "A sharp drop in service metric observations can indicate stopped processing or reporting.",
            ),
            _operator(
                "trace_status_code_shift",
                "trace",
                "service",
                "status_code",
                "categorical",
                "distribution_shift",
                "jsd",
                {
                    "mutation": 1.00,
                    "propagation": 0.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "interface failure",
                ["service_name", "status_code"],
                "A status-code distribution shift reflects interface behavior changes at service granularity.",
            ),
            _operator(
                "trace_error_rate",
                "trace",
                "service",
                "status_code",
                "rate",
                "error_rate_delta",
                "ratio",
                {
                    "mutation": 1.00,
                    "propagation": 0.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "interface failure",
                ["service_name", "status_code"],
                "A change in error status rate is a compact interface failure signal.",
            ),
            _operator(
                "trace_endpoint_shift",
                "trace",
                "service",
                "endpoint",
                "categorical",
                "distribution_shift",
                "jsd",
                {
                    "mutation": 1.00,
                    "propagation": 0.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "endpoint behavior change",
                ["service_name", "endpoint"],
                "A changed endpoint mix suggests altered service interface behavior.",
            ),
            _operator(
                "trace_duration_delta",
                "trace",
                "service",
                "duration",
                "duration",
                "robust_z_shift",
                "max",
                {
                    "mutation": 0.00,
                    "propagation": 1.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "latency propagation",
                ["service_name", "duration"],
                "Latency shifts are often amplified along dependencies and are treated primarily as propagated symptoms.",
            ),
            _operator(
                "trace_count_rise_shift",
                "trace",
                "service",
                "__row_count__",
                "count",
                "count_rise",
                "ratio",
                {
                    "mutation": 0.00,
                    "propagation": 1.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "retry or traffic amplification",
                ["service_name"],
                "A trace count rise can reflect retries, fan-out, or propagated pressure.",
            ),
            _operator(
                "trace_count_drop_shift",
                "trace",
                "service",
                "__row_count__",
                "count",
                "count_drop",
                "ratio",
                {
                    "mutation": 1.00,
                    "propagation": 0.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "service hang or request handling failure",
                ["service_name"],
                "A sharp trace activity drop can indicate stopped request handling.",
            ),
            _operator(
                "log_count_delta",
                "log",
                "service",
                "__row_count__",
                "count",
                "count_delta",
                "ratio",
                {
                    "mutation": 0.00,
                    "propagation": 1.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "software event volume shift",
                ["service_name"],
                "Log volume changes can indicate local software events or propagated error handling.",
            ),
            _operator(
                "log_template_delta",
                "log",
                "service",
                "template",
                "categorical",
                "distribution_shift",
                "jsd",
                {
                    "mutation": 0.00,
                    "propagation": 1.00,
                    "observability_bias": 0.00,
                    "topology_context": 0.00,
                },
                "software event distribution shift",
                ["service_name", "template"],
                "A log-template distribution shift indicates changed software behavior that can be local or propagated.",
            ),
        ],
    }


def mock_synthesis_inputs() -> dict[str, Any]:
    """Return deterministic prompt inputs used by the mock path."""

    return {
        "artifact_summary": MOCK_ARTIFACT_SUMMARY,
        "telemetry_schema": MOCK_TELEMETRY_SCHEMA,
        "mechanism_catalog": MOCK_MECHANISM_CATALOG,
    }
