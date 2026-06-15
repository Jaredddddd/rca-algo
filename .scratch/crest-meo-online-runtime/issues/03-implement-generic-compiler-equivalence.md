# Implement Generic Compiler Equivalence

Status: ready-for-agent
Type: AFK

## Parent

.scratch/crest-meo-online-runtime/PRD.md

## What to build

Implement the AtomicOperator semantics in the generic EvidenceCompiler so the deployable MEOL produces the same raw feature matrix as the verified feature reference. The compiler should interpret operator semantics from specs, not from old feature-column names.

This slice is complete when the generic compiler can materialize the current deployable MEOL end to end and match `_build_feature_matrix(..., normalize=False)` for the verified feature set in focused tests.

## Acceptance criteria

- [ ] Metric operators match verified z shift, mean z, anomaly count, absolute mean delta, row-count drop, and abnormal row volume semantics.
- [ ] Trace operators match verified duration shift, count delta/rise/drop, operation/span distribution shift, error-rate, joint operation/status residual, self-duration relative increase, abnormal row volume, and topology semantics.
- [ ] Log operators match verified count delta, keyword error-rate, and template cardinality delta semantics, including existing-template preference and stable message fallback.
- [ ] Compiler tests compare generic compiler output against the verified feature oracle for the deployable MEOL with `normalize=False`.
- [ ] The compiler no longer needs an extracted feature matrix path to reproduce deployable MEOL values.

## Blocked by

- .scratch/crest-meo-online-runtime/issues/01-define-atomic-operator-inventory.md
- .scratch/crest-meo-online-runtime/issues/02-make-meol-express-verified-semantics.md
