# Context Map

This repository is a multi-context RCA algorithm workspace. Read the context that
matches the algorithm area being changed.

## Contexts

### EvidenceRank

- Current path: `algorithms/evidencerank/`
- Current context file: `algorithms/evidencerank/CONTEXT.md` if present
- Research docs: `docs/EvidRank_evolve/`, `docs/EvidRank-ARC-Evolve/`

### CREST

- Canonical implementation path: `algorithms/crest/`
- Compatibility adapter path: `algorithms/evidencerank/src/evidencerank/crest.py`
- Current support modules:
  - `algorithms/crest/src/crest/features.py`
  - `algorithms/crest/src/crest/meo_algorithm.py`
  - `algorithms/crest/src/crest/residual.py`
  - `algorithms/crest/src/crest/meo/`
- Planned upstream repository: `git@github.com:Jaredddddd/Crest.git`
- Current research docs:
  - `algorithms/crest/docs/crest_meo/`
  - `algorithms/crest/docs/root_notes/`

CREST has already been extracted from EvidenceRank. For new structural changes,
use `algorithms/crest/` as the source of truth and keep compatibility adapters
under `algorithms/evidencerank/` thin.
