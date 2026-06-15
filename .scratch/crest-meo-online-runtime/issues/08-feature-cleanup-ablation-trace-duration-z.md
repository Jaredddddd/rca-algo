# Feature Cleanup Ablation For Redundant Signals

Status: ready-for-agent
Type: AFK

## Parent

.scratch/crest-meo-online-runtime/PRD.md

## What to build

Evaluate whether apparently redundant or low-value deployable features can be removed after the strict generic runtime migration. Start with `trace_duration_z` because it has been identified as a possible redundant propagation signal, but treat deletion as an evidence-backed ablation rather than a cleanup assumption.

This slice is complete when there is a documented ablation result showing whether the feature should stay or be removed from the deployable MEOL.

## Acceptance criteria

- [ ] A variant MEOL or controlled ablation disables the candidate feature without changing unrelated scoring logic.
- [ ] Full evaluation and perf report compare the ablation against the accepted strict generic CREST-MEO baseline.
- [ ] The result documents AC@1, MRR, AC@3, AC@5, runtime, improved cases, and regressed cases when available.
- [ ] The feature is removed from deployable MEOL only if the ablation shows no unacceptable regression.
- [ ] Documentation records the decision so future cleanup does not repeat the same ablation.

## Blocked by

- .scratch/crest-meo-online-runtime/issues/07-run-equivalence-and-benchmark-acceptance.md
