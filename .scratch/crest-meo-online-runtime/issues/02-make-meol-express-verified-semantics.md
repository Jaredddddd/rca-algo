# Make MEOL Express Verified Semantics Explicitly

Status: ready-for-agent
Type: AFK

## Parent

.scratch/crest-meo-online-runtime/PRD.md

## What to build

Update the frozen CREST-MEO library and any required schema vocabulary so the current deployable operators express their verified AtomicOperator semantics directly. The MEOL should remain the online source of truth for operator selection and role membership, without relying on feature-name special cases or redundant runtime binding metadata.

This slice is complete when the deployable MEOL can be read as an ordinary frozen operator library whose specs contain enough semantic information for the generic compiler to execute the verified behavior.

## Acceptance criteria

- [ ] The deployable MEOL contains no `runtime_binding`, `feature_column`, `extracted_feature_column`, or equivalent duplicate column-binding metadata.
- [ ] Operators whose current JSON semantics are incomplete are updated to explicit generic semantics, including metric anomaly count, abnormal row volume, trace duration mean delta, joint operation/status residual shift, and trace self-duration relative increase.
- [ ] Role priors remain binary and continue to define mutation / propagation / neutral membership from the MEOL itself.
- [ ] Static and schema verification vocabulary accepts the explicit semantics needed by the deployable MEOL.
- [ ] Existing tests for MEOL loading, role membership, and no redundant runtime binding are updated and pass.

## Blocked by

- .scratch/crest-meo-online-runtime/issues/01-define-atomic-operator-inventory.md
