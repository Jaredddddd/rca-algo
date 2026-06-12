"""Compatibility wrapper for the standalone CREST tool."""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    repo = Path(__file__).resolve().parents[1]
    runpy.run_path(
        str(repo / "algorithms/crest/tools/export_crest_builtin_meol.py"),
        run_name="__main__",
    )
