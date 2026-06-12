from __future__ import annotations

import evidencerank.crest as evidencerank_crest
from evidencerank.crest import CREST, score_crest_services
from evidencerank.crest_meo import CRESTMEO, CRESTMEOBuiltIn
from evidencerank.crest_residual import CRESTResidual
from evidencerank.meo.runtime.load_meol import CREST_BUILTIN_MEOL_PATH

from crest.algorithm import CREST as CanonicalCREST
from crest.algorithm import score_crest_services as canonical_score_crest_services
from crest.meo_algorithm import CRESTMEO as CanonicalCRESTMEO
from crest.meo_algorithm import CRESTMEOBuiltIn as CanonicalCRESTMEOBuiltIn
from crest.residual import CRESTResidual as CanonicalCRESTResidual


def test_evidencerank_crest_imports_forward_to_standalone_package() -> None:
    assert CREST is CanonicalCREST
    assert score_crest_services is canonical_score_crest_services
    assert evidencerank_crest.CRESTMEO is CanonicalCRESTMEO
    assert CRESTMEO is CanonicalCRESTMEO
    assert CRESTMEOBuiltIn is CanonicalCRESTMEOBuiltIn
    assert CRESTResidual is CanonicalCRESTResidual
    assert CRESTMEOBuiltIn._meol_path == CREST_BUILTIN_MEOL_PATH
