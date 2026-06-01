# EvidenceRank V2 Iteration

- Created: 2026-06-01T14:33:52+08:00
- Hypothesis: 未定义或缺失的单个模态特征应作为无证据处理，而不应让服务已有的其他异常证据整体失效
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: feature-level missingness should mean "no evidence" for that feature, not "discard this service's whole evidence vector".
- Why this should transfer beyond RCABench: real observability data often has sparse modality coverage, empty log/error-rate groups, or undefined statistical moments. A service with one undefined modality can still carry valid metric or trace evidence.
- Constraint update: do not read `conclusion.parquet` in algorithm code. It can only inspire raw-trace feature design by studying how endpoint-level symptoms might be derived; the file itself must not be consumed for ranking or false-case evidence.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V1`
- Baseline summary: `docs/EvidRank_evolve/V1_summary.md`
- Key weak groups: `bandwidth`, `response-replace-code`, `response-abort`, `pod-failure`, and multi-GT request/response cases.
- Representative false cases reviewed:
  - `ts0-mysql-container-kill-9t6n24`: GT rank 4, high-volume log/trace services outrank infrastructure root.
  - `ts0-mysql-partition-cfvlsw`: GT services rank outside Top-5; endpoint/path-level symptoms appear in raw traces but need better propagation control.
  - `ts2-ts-travel-service-pod-failure-jqk2bj`: root service is deeply ranked while gateway/plan services dominate observed symptoms.
  - `ts3-ts-ui-dashboard-request-abort-7z5bcm`: raw trace endpoint errors identify a relevant path, but naive endpoint boosting over-promotes propagated symptoms.

## Planned Change

- Minimal algorithm change: sanitize non-finite feature values before `log1p` normalization and before final summation in `_heuristic_scores`.
- Expected metric movement: small AC@1/MRR/AC@3/AC@5 lift. Offline replay using the same current features estimated `AC@1 0.530239 -> 0.531646`, `AC@3 0.778481 -> 0.786920`, `AC@5 0.877637 -> 0.886779`, `MRR 0.679202 -> 0.684448`.
- Known regression risk: low but non-zero. Services previously suppressed by a NaN can move upward, which may displace a true Top-1 in a small number of cases.
- Rejected for this version: naive endpoint rank-fusion from raw traces. It did not read `conclusion.parquet`, but offline rank fusion hurt AC@1, indicating endpoint symptoms need confidence gating and topology-aware propagation suppression before entering the algorithm.

## Improvement Proposal Record

1. Failure mechanism: sparse or undefined modality values can create `NaN` in a service feature vector.
2. Why current EvidenceRank is wrong: a single non-finite feature made the row sum non-finite, and `_heuristic_scores` converted the whole service score to zero, discarding valid evidence from other features.
3. General signal or combination: treat non-finite, negative, or undefined feature values as feature-level no-evidence before normalization and fusion.
4. Case types likely to improve: cases where the root has a strong metric, trace, log, or topology signal plus one missing/undefined modality; V2 evidence shows many `pod-failure` roots moved from deep ranks to rank 1.
5. Case types likely to regress: cases where a high-traffic propagated service was previously suppressed by a non-finite value and can now move above a true root; V2 regressions are mostly one-rank shifts in request/response mutation cases.
6. Minimal code location: `algorithms/evidencerank/src/evidencerank/algorithm.py`, `_build_feature_matrix` and `_heuristic_scores`.
7. Validation and ablation: compare V1 vs V2 full RCABench metrics; ablation is the V1 behavior without feature-level non-finite sanitization.
8. Acceptance criterion: accept only if guard has no high-risk warning, full eval has zero errors, at least one of AC@1/MRR improves, and AC@3/AC@5 do not materially regress.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V2 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V2 --source V2 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V1 --new V2 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- Guard: no high-risk warnings. Existing medium warnings are dataset-name literals in documentation/import context, not ranking logic.
- Full eval: `total=1422`, `error=0`, average runtime `7.406487s`.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V2`
- New summary: `docs/EvidRank_evolve/V2_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_V1_vs_V2.md`
- AC@1: `0.530239 -> 0.531646` (`+0.001406`, `754 -> 756`)
- AC@3: `0.778481 -> 0.786920` (`+0.008439`, `1107 -> 1119`)
- AC@5: `0.877637 -> 0.886779` (`+0.009142`, `1248 -> 1261`)
- MRR: `0.679202 -> 0.684448` (`+0.005246`)

## Case Deltas

- Status counts: `improved_to_hit1=11`, `rank_improved=32`, `rank_regressed=27`, `regressed_from_hit1=9`, `unchanged=1343`.
- Improved to Hit@1: all 11 cases are `pod-failure`, typically moving from ranks `31-47` to rank `1`. This supports the hypothesis that non-finite feature suppression was hiding otherwise valid root evidence.
- Other rank improvements: mostly `partition`, `corrupt`, `loss`, and `bandwidth` multi-GT cases; gains are smaller but broad enough to improve AC@3 and AC@5.
- Regressed from Hit@1: 9 cases, all from rank `1` to rank `2`. Fault groups are `request-abort`, `response-replace-body`, `request-replace-method`, `request-replace-path`, `response-abort`, and `response-replace-code`.
- Notable deep regression: `ts0-ts-travel-plan-service-pod-failure-sxz5ll` moved from rank `15` to `35`, so the next round should avoid globally boosting newly unsuppressed services without topology or confidence control.

## Decision

- Accept / reject / keep for later: accept V2 as a small, generic improvement.
- Reason: full eval completed with `error=0`; guard has no high-risk warning; AC@1, MRR, AC@3, and AC@5 all improved; Top-1 regressions are mild rank `1 -> 2` shifts and remain within Top-3/Top-5.
- Next smallest general step: design a confidence-gated raw-trace endpoint symptom feature that does not read `conclusion.parquet`, then suppress propagated endpoint symptoms with topology or neighbor contrast before fusing with service-level evidence.
