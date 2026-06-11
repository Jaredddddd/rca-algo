"""CREST-MEO algorithm entry points."""

from __future__ import annotations

from pathlib import Path

from .crest import CREST
from .meo.runtime.load_meol import CREST_BUILTIN_MEOL_PATH


class CRESTMEO(CREST):
    """CREST-MEO ranking with the default JSON Meta Evidence Operator Library."""

    _use_meo = True
    _meol_path: Path | None = None


class CRESTMEOBuiltIn(CRESTMEO):
    """CREST-MEO using the mechanical JSON export of CREST built-in features."""

    _meol_path: Path | None = CREST_BUILTIN_MEOL_PATH
