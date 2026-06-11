"""Load Meta Evidence Operator libraries from JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..dsl.schema import EvidenceOperatorSpec, parse_operator_spec


DEFAULT_MEOL_PATH = Path(__file__).resolve().parents[1] / "library" / "default_meol.json"
CREST_BUILTIN_MEOL_PATH = (
    Path(__file__).resolve().parents[1] / "library" / "crest_builtin_meol.json"
)


def load_meol(path: str | Path) -> dict[str, Any]:
    """Load a MEOL JSON document."""

    with Path(path).open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    if not isinstance(raw, dict):
        raise ValueError("MEOL root must be a JSON object")
    return raw


def load_operator_specs(path: str | Path) -> list[EvidenceOperatorSpec]:
    """Load and parse all operator specs from a MEOL JSON document."""

    raw = load_meol(path)
    operators = raw.get("operators", [])
    if not isinstance(operators, list):
        raise ValueError("MEOL operators must be a list")
    return [parse_operator_spec(item) for item in operators]
