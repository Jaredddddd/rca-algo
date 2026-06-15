# Switch Online Instantiation To Strict Generic Path

Status: ready-for-agent
Type: AFK

## Parent

.scratch/crest-meo-online-runtime/PRD.md

## What to build

Change online CREST-MEO feature materialization so every frozen MEOL operator is compiled and executed through the generic compiler path in MEOL order. Remove the online extracted special path and make ordinary compile/runtime failures surface by default.

This slice is complete when `score_crest_services()` consumes frozen MEOL strictly and cannot silently fall back to old hard-coded feature construction or zero a failed online operator.

## Acceptance criteria

- [ ] Default online feature materialization calls the compiler for each deployable MEOL operator and stacks columns in MEOL order.
- [ ] The extracted fast path is removed from the online runtime.
- [ ] A compile/runtime failure raises by default through online instantiation instead of producing a zero column.
- [ ] `score_crest_services()` continues to load MEOL, read role priors, compute ranking columns, and support modality / graph ablations.
- [ ] Tests prove the default deployable MEOL uses the generic compiler path.

## Blocked by

- .scratch/crest-meo-online-runtime/issues/02-make-meol-express-verified-semantics.md
- .scratch/crest-meo-online-runtime/issues/03-implement-generic-compiler-equivalence.md
