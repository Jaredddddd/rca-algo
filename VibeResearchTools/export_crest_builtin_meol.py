"""Export CREST's built-in evidence features as a MEOL JSON library."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
EVIDENCERANK_SRC = REPO / "algorithms/evidencerank/src"
sys.path.insert(0, str(EVIDENCERANK_SRC))

from evidencerank.cera import BASE_FEATURE_NAMES, MODALITY_FEATURES  # noqa: E402
from evidencerank.crest import (  # noqa: E402
    CREST_COUNTERFACTUAL_MUTATION_FEATURES,
    CREST_COUNTERFACTUAL_PROPAGATION_FEATURES,
    CREST_DENOISED_CHANNEL_EXCLUDES,
    CREST_ROLE_FAMILIES,
)
from evidencerank.meo.runtime.instantiate import ROLE_ORDER  # noqa: E402


DEFAULT_OUTPUT = (
    EVIDENCERANK_SRC
    / "evidencerank"
    / "meo"
    / "library"
    / "crest_builtin_meol.json"
)


FEATURE_OVERRIDES: dict[str, dict[str, Any]] = {
    "metric_max_z": {
        "source": "metric",
        "signal": {"field": "*", "type": "value"},
        "contrast": "z_shift",
        "aggregation": "max",
        "mechanism": "metric magnitude shift",
        "required_fields": ["time", "service_name", "value"],
    },
    "metric_mean_z": {
        "source": "metric",
        "signal": {"field": "*", "type": "value"},
        "contrast": "z_shift",
        "aggregation": "mean",
        "mechanism": "metric average shift",
        "required_fields": ["time", "service_name", "value"],
    },
    "metric_anomaly_count": {
        "source": "metric",
        "signal": {"field": "*", "type": "count"},
        "contrast": "count_delta",
        "aggregation": "sum",
        "mechanism": "metric anomaly volume change",
        "required_fields": ["time", "service_name", "value"],
    },
    "metric_value_delta": {
        "source": "metric",
        "signal": {"field": "*", "type": "value"},
        "contrast": "mean_delta",
        "aggregation": "mean",
        "mechanism": "metric value level change",
        "required_fields": ["time", "service_name", "value"],
    },
    "metric_count_drop_shift": {
        "source": "metric",
        "signal": {"field": "__row_count__", "type": "count"},
        "contrast": "count_drop",
        "aggregation": "ratio",
        "mechanism": "metric observation disappearance",
        "required_fields": ["service_name"],
    },
    "trace_duration_z": {
        "source": "trace",
        "signal": {"field": "duration", "type": "duration"},
        "contrast": "z_shift",
        "aggregation": "max",
        "mechanism": "trace latency z shift",
        "required_fields": ["service_name", "duration"],
    },
    "trace_duration_delta": {
        "source": "trace",
        "signal": {"field": "duration", "type": "duration"},
        "contrast": "robust_z_shift",
        "aggregation": "max",
        "mechanism": "trace latency propagation",
        "required_fields": ["service_name", "duration"],
    },
    "trace_count_delta": {
        "source": "trace",
        "signal": {"field": "__row_count__", "type": "count"},
        "contrast": "count_delta",
        "aggregation": "ratio",
        "mechanism": "trace traffic volume change",
        "required_fields": ["service_name"],
    },
    "trace_count_rise_shift": {
        "source": "trace",
        "signal": {"field": "__row_count__", "type": "count"},
        "contrast": "count_rise",
        "aggregation": "ratio",
        "mechanism": "retry or fan-out traffic amplification",
        "required_fields": ["service_name"],
    },
    "trace_count_drop_shift": {
        "source": "trace",
        "signal": {"field": "__row_count__", "type": "count"},
        "contrast": "count_drop",
        "aggregation": "ratio",
        "mechanism": "request handling disappearance",
        "required_fields": ["service_name"],
    },
    "trace_endpoint_shift": {
        "source": "trace",
        "signal": {"field": "endpoint", "type": "categorical"},
        "contrast": "distribution_shift",
        "aggregation": "jsd",
        "mechanism": "endpoint behavior distribution shift",
        "required_fields": ["service_name", "endpoint"],
    },
    "trace_error_rate": {
        "source": "trace",
        "signal": {"field": "status_code", "type": "rate"},
        "contrast": "error_rate_delta",
        "aggregation": "ratio",
        "mechanism": "trace error-rate change",
        "required_fields": ["service_name", "status_code"],
    },
    "trace_status_code_shift": {
        "source": "trace",
        "signal": {"field": "status_code", "type": "categorical"},
        "contrast": "distribution_shift",
        "aggregation": "jsd",
        "mechanism": "status-code distribution shift",
        "required_fields": ["service_name", "status_code"],
    },
    "trace_self_duration_relative_shift": {
        "source": "trace",
        "signal": {"field": "duration", "type": "duration"},
        "contrast": "robust_z_shift",
        "aggregation": "ratio",
        "mechanism": "service-local span duration share shift",
        "required_fields": ["service_name", "duration"],
    },
    "log_count_delta": {
        "source": "log",
        "signal": {"field": "__row_count__", "type": "count"},
        "contrast": "count_delta",
        "aggregation": "ratio",
        "mechanism": "log volume change",
        "required_fields": ["service_name"],
    },
    "log_error_rate": {
        "source": "log",
        "signal": {"field": "message", "type": "rate"},
        "contrast": "rate_delta",
        "aggregation": "ratio",
        "mechanism": "log error keyword rate change",
        "required_fields": ["service_name", "message"],
    },
    "log_template_delta": {
        "source": "log",
        "signal": {"field": "template", "type": "categorical"},
        "contrast": "distribution_shift",
        "aggregation": "jsd",
        "mechanism": "log template distribution shift",
        "required_fields": ["service_name", "template"],
    },
    "topology_in_degree": {
        "source": "topology",
        "signal": {"field": "incoming_edges", "type": "count"},
        "contrast": "count_delta",
        "aggregation": "sum",
        "mechanism": "incoming dependency context",
        "required_fields": ["parent_service", "service_name"],
    },
    "topology_out_degree": {
        "source": "topology",
        "signal": {"field": "outgoing_edges", "type": "count"},
        "contrast": "count_delta",
        "aggregation": "sum",
        "mechanism": "outgoing dependency context",
        "required_fields": ["parent_service", "service_name"],
    },
    "abnormal_metric_rows": {
        "source": "metric",
        "signal": {"field": "__row_count__", "type": "count"},
        "contrast": "count_delta",
        "aggregation": "sum",
        "mechanism": "metric observability volume",
        "required_fields": ["service_name"],
    },
    "abnormal_trace_rows": {
        "source": "trace",
        "signal": {"field": "__row_count__", "type": "count"},
        "contrast": "count_delta",
        "aggregation": "sum",
        "mechanism": "trace observability volume",
        "required_fields": ["service_name"],
    },
}


def _family_for_feature(feature_name: str) -> str:
    for family, feature_names in CREST_ROLE_FAMILIES.items():
        if feature_name in feature_names:
            return family
    return "unknown"


def _modality_for_feature(feature_name: str) -> str:
    for modality, feature_names in MODALITY_FEATURES.items():
        if feature_name in feature_names:
            return modality
    return "unknown"


def _counterfactual_role(feature_name: str) -> str:
    if feature_name in CREST_COUNTERFACTUAL_MUTATION_FEATURES:
        return "mutation"
    if feature_name in CREST_COUNTERFACTUAL_PROPAGATION_FEATURES:
        return "propagation"
    return "neutral"


def _role_prior(feature_name: str) -> dict[str, float]:
    role = _counterfactual_role(feature_name)
    return {
        candidate: 1.0 if candidate == role else 0.0
        for candidate in ROLE_ORDER
    }


def _operator(feature_name: str) -> dict[str, Any]:
    override = FEATURE_OVERRIDES[feature_name]
    cf_role = _counterfactual_role(feature_name)
    family = _family_for_feature(feature_name)
    return {
        "name": feature_name,
        "source": override["source"],
        "entity": "service",
        "signal": override["signal"],
        "contrast": {
            "operator": override["contrast"],
            "normal_window": "pre_anomaly",
            "abnormal_window": "post_anomaly",
        },
        "aggregation": {
            "level": "service",
            "method": override["aggregation"],
        },
        "role_prior": _role_prior(feature_name),
        "mechanism": override["mechanism"],
        "required_fields": override["required_fields"],
        "rationale": (
            f"Mechanical MEOL export of CREST built-in feature {feature_name}; "
            f"original family is {family}, source modality is "
            f"{_modality_for_feature(feature_name)}, and MEO role is {cf_role}."
        ),
        "metadata": {
            "crest_builtin_feature": True,
            "crest_role_family": family,
            "crest_modality": _modality_for_feature(feature_name),
            "crest_counterfactual_role": cf_role,
        },
    }


def build_library() -> dict[str, Any]:
    missing = [name for name in BASE_FEATURE_NAMES if name not in FEATURE_OVERRIDES]
    if missing:
        raise ValueError(f"missing feature overrides: {missing}")
    return {
        "library_name": "crest-builtins-meol-v1",
        "dsl_version": "1.0",
        "generator": {
            "type": "mechanical_crest_export",
            "source_modules": [
                "evidencerank.crest",
                "evidencerank.cera",
            ],
            "deterministic_runtime": True,
        },
        "roles": ["mutation", "propagation", "neutral"],
        "compatibility": {
            "feature_binding": "crest_builtin_feature_name",
            "runtime_path": "score_crest_services(use_meo=True, meol_path=...)",
            "uses_crest_feature_fast_path": True,
            "score_equivalent_to_hardcoded_crest": True,
            "note": (
                "The MEOL selects the same CREST built-in feature columns and "
                "counterfactual mutation/propagation memberships. The online "
                "CREST-MEO scorer intentionally reuses the hard-coded CREST "
                "scoring logic for equivalence."
            ),
        },
        "denoised_channel_excludes": sorted(CREST_DENOISED_CHANNEL_EXCLUDES),
        "counterfactual_mutation_features": sorted(CREST_COUNTERFACTUAL_MUTATION_FEATURES),
        "counterfactual_propagation_features": sorted(
            CREST_COUNTERFACTUAL_PROPAGATION_FEATURES
        ),
        "operators": [_operator(feature_name) for feature_name in BASE_FEATURE_NAMES],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to write crest_builtin_meol.json.",
    )
    args = parser.parse_args(argv)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(build_library(), handle, indent=2, sort_keys=False)
        handle.write("\n")
    print(args.output)


if __name__ == "__main__":
    main()
