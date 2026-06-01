# EvidenceRank V4 Iteration

- Created: 2026-06-01T15:35:29+08:00
- Hypothesis: 根因服务的异常常被上游调用方观测到，少量上游上下文传播比统一拓扑度惩罚更稳
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: caller-side symptoms should provide weak directional support to the callee, because downstream root causes are often observed by upstream services.
- Why this should transfer beyond RCABench: distributed traces encode generic parent-child call direction; a small upstream-to-callee context term can reduce propagated caller false positives without naming any service or fault.
- Constraint reminder: V4 reads only raw traces already used by EvidenceRank. It does not read `conclusion.parquet`, labels, injection metadata, or previous outputs in algorithm logic.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V3`
- Baseline summary: `docs/EvidRank_evolve/V3_summary.md`
- Baseline metrics: `AC@1=0.559072`, `AC@3=0.789030`, `AC@5=0.888186`, `MRR=0.698007`.
- Key weak groups: `response-replace-code`, `response-abort`, `bandwidth`, `request-replace-path`, and user-facing or route-planning paths where endpoint symptoms and topology direction are ambiguous.
- Representative false cases: V3 regressions show that a uniform topology degree penalty can demote central true roots, while remaining false cases still show upstream callers outranking likely downstream causes.

## Planned Change

- Minimal algorithm change: set topology degree feature weights to `0.0` and add `_apply_parent_context`, which blends each service score with `5%` of the mean score of its trace parents.
- Expected metric movement from offline replay on V3 feature/edge caches: `AC@1 0.559072 -> 0.570323`, `AC@3 0.789030 -> 0.790436`, `AC@5 0.888186 -> 0.889592`, `MRR 0.698007 -> 0.705336`.
- Known regression risk: true caller-side roots can be slightly demoted if their downstream callees receive parent context; the low `5%` weight is intended to make this a tie-breaker rather than a new dominant signal.

## Improvement Proposal Record

1. Failure mechanism: propagated symptoms often appear at callers, while the callee root remains just below the caller in rank.
2. Why current EvidenceRank is wrong: V3 replaced positive topology evidence with a uniform degree penalty, but degree alone cannot distinguish true central roots from propagated callers.
3. General signal or combination: use trace direction to pass a small amount of parent/caller anomaly context to each child/callee before sorting.
4. Case types likely to improve: cases where upstream entry or orchestration services observe downstream root symptoms and the root is already near the top ranks.
5. Case types likely to regress: caller-side injected faults where the caller is the true root and downstream services inherit its high context.
6. Minimal code location: `FEATURE_WEIGHTS`, `_heuristic_scores`, `_apply_parent_context`, and `EvidenceRank.__call__`.
7. Validation and ablation: V3 is the uniform topology-penalty ablation; V4 full eval validates parent-context smoothing.
8. Acceptance criterion: accept only if full eval has zero errors, guard has no high-risk warning, AC@1/MRR improve, and AC@3/AC@5 do not materially regress.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V4 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V4 --source V4 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V3 --new V4 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- Guard: no high-risk warnings. Existing medium warnings are pre-existing dataset-name literals in module/import context.
- Full eval: `total=1422`, `error=0`, average runtime `7.365646s`.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V4`
- New summary: `docs/EvidRank_evolve/V4_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_V3_vs_V4.md`
- AC@1: `0.559072 -> 0.571730` (`+0.012658`, `795 -> 813`)
- AC@3: `0.789030 -> 0.791139` (`+0.002110`, `1122 -> 1125`)
- AC@5: `0.888186 -> 0.888889` (`+0.000703`, `1263 -> 1264`)
- MRR: `0.698007 -> 0.706323` (`+0.008316`)

## Case Deltas

- Status counts: `improved_to_hit1=19`, `rank_improved=60`, `rank_regressed=31`, `regressed_from_hit1=1`, `unchanged=1311`.
- Improved to Hit@1: mostly `response-replace-code` 6, `request-replace-method` 4, plus `corrupt`, `response-delay`, `request-delay`, `partition`, `bandwidth`, and `response-replace-body`.
- Regressed from Hit@1: only `ts4-ts-ui-dashboard-response-replace-code-lk7q57`, rank `1 -> 2`; GT remains in Top-2 and Top-5.
- Net effect: parent-context smoothing improves all primary metrics and reduces V3's broad topology-penalty regressions.

## Decision

- Accept / reject / keep for later: accept V4 as the current default.
- Reason: full eval has `error=0`; guard has no high-risk warning; AC@1/MRR/AC@3/AC@5 all improve over V3; regression from Hit@1 is a single rank `1 -> 2` case.
- Next smallest general step: reconstruct endpoint-level request/error/body/status shift signals from raw traces and logs, with confidence gating, without reading `conclusion.parquet`.
