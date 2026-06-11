"""Static checks for EvidenceOperatorSpec objects."""

from __future__ import annotations

import math

from ..dsl.schema import EvidenceOperatorSpec
from ..runtime.instantiate import ROLE_ORDER


ALLOWED_OPERATORS = {
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
}
ALLOWED_SOURCES = {"metric", "log", "trace", "topology"}
ALLOWED_ROLES = set(ROLE_ORDER)


def static_verify(spec: EvidenceOperatorSpec) -> tuple[bool, list[str]]:
    """Validate source, operator, role membership, and mechanism metadata."""

    errors: list[str] = []
    if spec.source not in ALLOWED_SOURCES:
        errors.append(f"invalid_source:{spec.source}")
    if spec.contrast.operator not in ALLOWED_OPERATORS:
        errors.append(f"invalid_operator:{spec.contrast.operator}")

    unknown_roles = sorted(set(spec.role_prior) - ALLOWED_ROLES)
    if unknown_roles:
        errors.append(f"unknown_roles:{unknown_roles}")

    for role, value in spec.role_prior.items():
        numeric = float(value)
        if not math.isfinite(numeric) or numeric < 0.0 or numeric > 1.0:
            errors.append(f"role_prior_out_of_range:{role}:{value}")

    mutation = float(spec.role_prior.get("mutation", 0.0))
    propagation = float(spec.role_prior.get("propagation", 0.0))
    if mutation not in {0.0, 1.0}:
        errors.append(f"role_prior_not_binary:mutation:{mutation}")
    if propagation not in {0.0, 1.0}:
        errors.append(f"role_prior_not_binary:propagation:{propagation}")
    if mutation > 0.0 and propagation > 0.0:
        errors.append("role_prior_ambiguous:mutation_and_propagation")

    if not spec.rationale.strip():
        errors.append("missing_rationale")
    if not spec.mechanism.strip():
        errors.append("missing_mechanism")
    return len(errors) == 0, errors
