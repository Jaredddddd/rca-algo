"""Compatibility wrapper for the standalone CREST tool."""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    repo = Path(__file__).resolve().parents[1]
    runpy.run_path(str(repo / "algorithms/crest/tools/crest_meo_oracle.py"), run_name="__main__")
