"""Compatibility adapter for the standalone :mod:`crest` package."""

from crest.algorithm import *  # noqa: F401,F403


def __getattr__(name: str) -> object:
    """Preserve historic lazy CREST-MEO imports from ``evidencerank.crest``."""

    if name == "CRESTMEO":
        from crest.meo_algorithm import CRESTMEO

        return CRESTMEO
    if name == "CRESTMEOBuiltIn":
        from crest.meo_algorithm import CRESTMEOBuiltIn

        return CRESTMEOBuiltIn
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
