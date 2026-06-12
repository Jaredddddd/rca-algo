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
  - `algorithms/crest/docs/crest_evolve/`
  - `algorithms/crest/docs/crest_evolve_aiops25/`
  - `algorithms/crest/docs/crest_meo/`
  - `algorithms/crest/docs/crest_residual/`
  - `algorithms/crest/docs/pv-crest/`
  - `algorithms/crest/docs/root_notes/`

Read `algorithms/crest/docs/crest_evolve/CREST_extraction_plan.md` before making structural
changes around CREST extraction.
