# Run Equivalence And Benchmark Acceptance

Status: ready-for-agent
Type: AFK

## Parent

.scratch/crest-meo-online-runtime/PRD.md

## What to build

Run the focused and benchmark validation needed to accept the strict generic CREST-MEO online runtime. This issue should confirm that the compiler migration preserves deployable feature values, online ranking behavior, full-evaluation correctness, and expected runtime characteristics.

This slice is complete when the migration has focused test evidence and full RCABench perf evidence showing no large accuracy/runtime regression.

## Acceptance criteria

- [ ] Focused CREST-MEO tests pass.
- [ ] CREST source compile check passes.
- [ ] Full RCABench evaluation for `crest_meo` completes with `error == 0`.
- [ ] Perf report shows AC@1, MRR, AC@3, AC@5, and runtime are consistent with the verified CREST-MEO baseline within expected noise.
- [ ] Any metric or runtime regression is either fixed or documented as a blocker before accepting the migration.

## Blocked by

- .scratch/crest-meo-online-runtime/issues/03-implement-generic-compiler-equivalence.md
- .scratch/crest-meo-online-runtime/issues/04-switch-online-instantiation-to-strict-generic-path.md
- .scratch/crest-meo-online-runtime/issues/06-lock-runtime-and-registry-smoke-tests.md
