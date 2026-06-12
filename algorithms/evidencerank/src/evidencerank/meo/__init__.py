"""Compatibility adapter for :mod:`crest.meo`.

The CREST-MEO implementation now lives in the standalone ``crest`` package.
This package keeps historic ``evidencerank.meo.*`` imports working by pointing
Python's submodule search path at ``crest.meo``.
"""

from crest import meo as _crest_meo

__path__ = list(_crest_meo.__path__)
