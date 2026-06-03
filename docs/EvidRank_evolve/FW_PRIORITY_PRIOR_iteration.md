# EvidenceRank FW_PRIORITY_PRIOR Iteration

- Created: 2026-06-03T23:09:15+08:00
- Hypothesis: 用 SRE 可解释的 feature priority level 自动生成 FEATURE_WEIGHTS，验证能否替代逐 feature 手写浮点权重且保持默认 EvidenceRank 指标
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files changed: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: replace per-feature floating-point `FEATURE_WEIGHTS` with an ordinal SRE feature-priority prior, then derive the numeric scorer weights from a shared monotonic calibration ladder.
- Why this should transfer beyond RCABench: the code now records feature classes such as `BACKGROUND`, `BASELINE`, `SUPPORT`, `LOCAL`, `HIGH`, `ROOT`, and `CRITICAL` instead of independent feature-specific numbers. The prior can be explained as SRE/RCA evidence type ordering: protocol/status mutation and root-side count drop are more root-causal, row-count support features are supporting evidence, and high-volume metric/log symptoms are background context.

## Baseline

- Baseline snapshot: `FW_NUMERIC_BASELINE`
- Baseline summary: `docs/EvidRank_evolve/FW_NUMERIC_BASELINE_summary.md`
- Baseline metrics: AC@1 `0.802391`, MRR `0.875337`, AC@3 `0.943741`, AC@5 `0.975387`, error `0`.
- Key weak groups: `pod-failure`, `request-abort`, `response-replace-body`, `bandwidth`, and cases centered on high-fanout or UI/basic-service propagation paths remain the main weak areas.
- Representative false cases: unchanged hard misses include pod failure and bandwidth cases where propagation/entry symptoms dominate raw evidence. These cases are not directly targeted by this refactor.

## Planned Change

- Minimal algorithm change: introduce `FeaturePriority`, replace the feature-to-float table with `FEATURE_PRIORITIES`, and compute `FEATURE_WEIGHTS` from priorities in one helper. No labels, injections, outputs, historical rankings, or case identifiers are read by the algorithm.
- Expected metric movement: near-neutral. The change is intended to test whether numeric feature weights can be presented as ordinal type priors without materially changing ranking behavior.
- Known regression risk: collapsing the old near-baseline `trace_count_drop_shift=0.85` into `FeaturePriority.BASELINE` removes one small tuned-looking distinction. Cases that rely on a narrow balance between trace drop and protocol/status mutation evidence may move by one rank.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `FW_PRIORITY_PRIOR`
- New summary: `docs/EvidRank_evolve/FW_PRIORITY_PRIOR_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_PRIOR.md`
- AC@1: `0.802391 -> 0.800985` (`-0.001406`, 2 fewer top-1 hits)
- MRR: `0.875337 -> 0.874517` (`-0.000820`)
- AC@3: `0.943741 -> 0.942335` (`-0.001406`, 2 fewer top-3 hits)
- AC@5: `0.975387 -> 0.975387` (unchanged)
- Full eval: total `1422`, error `0`.

## Case Deltas

- Improved: none. This was a representation/maintainability refactor, not a new RCA signal.
- Regressed from hit@1:
  - `ts2-ts-basic-service-response-replace-code-rmprwq`: best GT rank `1 -> 2`.
  - `ts4-ts-basic-service-request-replace-method-hpv2qg`: best GT rank `1 -> 2`.
- Rank-regressed inside top-5:
  - `ts6-ts-basic-service-response-replace-code-s7bcv7`: best GT rank `3 -> 4`.
  - `ts7-ts-ui-dashboard-response-replace-code-t7vsbl`: best GT rank `3 -> 4`.
- Interpretation: all observed regressions are one-rank movements. The meaningful behavioral difference is the removal of the old feature-specific `trace_count_drop_shift=0.85` micro-weight; assigning it to `BASELINE` makes the prior cleaner but slightly changes close contests in protocol mutation cases.

## Decision

- Accept / reject / keep for later: accept as an optional presentation and maintainability refactor; do not claim it improves accuracy.
- Reason: the experiment validates that `FEATURE_WEIGHTS` can be expressed as an ordinal SRE feature-priority prior with only a tiny metric cost: 2 top-1 regressions out of 1422 cases, MRR down by `0.000820`, and AC@5 unchanged. This makes the method easier to describe as a type prior rather than a feature-by-feature hand-tuned numeric table.
- Paper wording supported by this run: "EvidenceRank uses an ordinal SRE feature-priority prior; the implementation maps priority levels to a shared monotonic calibration ladder before score aggregation." This is more defensible than listing independent per-feature constants.
- Caveat: the scorer still ultimately needs numeric multipliers. The important difference is that numbers are no longer assigned independently per feature. If strict no-regression default accuracy is required, the numeric baseline remains slightly better; adding a separate near-baseline priority for `trace_count_drop_shift` would recover the old behavior but would also reintroduce a micro-priority that looks more tuned.
- Next smallest general step: if continuing this line, learn or synthesize the priority-to-weight ladder from unlabeled incidents while keeping `FEATURE_PRIORITIES` ordinal. That would keep the SRE prior readable and move the remaining calibration away from hand-picked level weights.
