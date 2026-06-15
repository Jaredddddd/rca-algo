# Move Failure Collection To Offline Verification Tools

Status: ready-for-agent
Type: AFK

## Parent

.scratch/crest-meo-online-runtime/PRD.md

## What to build

Preserve candidate-operator failure collection for offline verification and research tools without letting that behavior leak into online CREST-MEO runtime. Candidate MEOL verification may continue collecting runtime-error statistics, but frozen online MEOL execution must remain strict.

This slice is complete when verifier tools can still report operator failures for candidate libraries, while `score_crest_services()` and default online instantiation do not mask frozen MEOL errors.

## Acceptance criteria

- [ ] Offline dynamic verification can still report compile/runtime error counts for candidate operators.
- [ ] Any non-strict behavior is explicit to verifier or research utilities and is not the default online instantiation mode.
- [ ] Tests cover verifier failure reporting separately from online strict runtime behavior.
- [ ] Documentation states that offline verification filters ordinary runtime errors before a MEOL is frozen.

## Blocked by

- .scratch/crest-meo-online-runtime/issues/04-switch-online-instantiation-to-strict-generic-path.md
