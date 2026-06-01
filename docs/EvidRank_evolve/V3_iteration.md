# EvidenceRank V3 Iteration

- Created: 2026-06-01T15:24:22+08:00
- Hypothesis: 多模态证据应按通用可靠性加权，并将拓扑度视为传播风险而非根因正证据
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: EvidenceRank should fuse feature families by generic confidence instead of treating every log-scaled feature as equally reliable positive evidence.
- Why this should transfer beyond RCABench: in microservice RCA, high-volume metric/log symptoms and high graph degree often reflect propagation or observation density, while trace-path deviations and sustained row coverage usually provide stronger causal support.
- Constraint reminder: do not read `conclusion.parquet`; V3 uses only the existing raw metric, trace, and log feature matrix.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V2`
- Baseline summary: `docs/EvidRank_evolve/V2_summary.md`
- Baseline metrics: `AC@1=0.531646`, `AC@3=0.786920`, `AC@5=0.886779`, `MRR=0.684448`.
- Key weak groups: `bandwidth`, `response-replace-code`, `response-abort`, infrastructure plus business-service multi-GT cases, and request/response mutation cases with endpoint-symptom propagation.
- Representative false cases: V2 hard cases show central/high-traffic services outranking roots; V2 regressions also show newly unsuppressed propagated services can displace a true Top-1.

## Planned Change

- Minimal algorithm change: add a global `FEATURE_WEIGHTS` vector and apply it in `_heuristic_scores` after feature sanitization.
- Weighting rule: metric core `0.75`, trace core `1.0`, log core `0.75`, row coverage `1.25`, topology degree `-0.25`.
- Expected metric movement from offline replay on V2 feature matrices: `AC@1 0.531646 -> 0.559072`, `AC@3 0.786920 -> 0.789030`, `AC@5 0.886779 -> 0.888186`, `MRR 0.684448 -> 0.697890`.
- Known regression risk: high-degree true roots or request/response mutation roots can be demoted by the topology penalty; offline replay shows 26 `regressed_from_hit1` cases, mostly rank `1 -> 2/3` with two pod-failure exceptions.

## Improvement Proposal Record

1. Failure mechanism: equal positive summation lets high-volume row counts and topology centrality dominate even when they are propagation symptoms.
2. Why current EvidenceRank is wrong: `topology_in_degree` and `topology_out_degree` are treated as root evidence, so fan-in/fan-out services can outrank services with more direct anomaly evidence.
3. General signal or combination: apply family-level confidence weights and use topology degree as a light propagation penalty instead of a positive signal.
4. Case types likely to improve: network/resource faults, partition/loss/corrupt/bandwidth cases, and request/response cases where the root is near but slightly below a propagated service.
5. Case types likely to regress: central true roots and pod-failure roots whose main signal is graph position or row volume.
6. Minimal code location: `FEATURE_WEIGHTS`, `EvidenceRank.__init__`, and `_heuristic_scores` in `algorithms/evidencerank/src/evidencerank/algorithm.py`.
7. Validation and ablation: V2 is the equal-weight ablation; V3 full eval plus `compare V2 vs V3` validates the weighted fusion.
8. Acceptance criterion: accept only if full eval has zero errors, guard has no high-risk warning, AC@1/MRR improve, and AC@3/AC@5 do not materially regress.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V3 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V3 --source V3 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V2 --new V3 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- Guard: no high-risk warnings. Existing medium warnings are pre-existing dataset-name literals in module/import context.
- Full eval: `total=1422`, `error=0`, average runtime `7.499614s`.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V3`
- New summary: `docs/EvidRank_evolve/V3_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_V2_vs_V3.md`
- AC@1: `0.531646 -> 0.559072` (`+0.027426`, `756 -> 795`)
- AC@3: `0.786920 -> 0.789030` (`+0.002110`, `1119 -> 1122`)
- AC@5: `0.886779 -> 0.888186` (`+0.001406`, `1261 -> 1263`)
- MRR: `0.684448 -> 0.698007` (`+0.013559`)

## Case Deltas

- Status counts: `improved_to_hit1=65`, `rank_improved=107`, `rank_regressed=127`, `regressed_from_hit1=26`, `unchanged=1097`.
- Improved to Hit@1: strongest counts come from `partition` 14, `corrupt` 9, `response-replace-code` 7, `request-replace-method` 6, `loss` 6, `response-delay` 5, and `bandwidth` 4. This supports the hypothesis that equal positive topology/volume evidence was over-promoting propagated nodes.
- Regressed from Hit@1: 26 cases. Most are rank `1 -> 2/3`; the largest drops are `ts3-ts-payment-service-pod-failure-fnlgp6` rank `1 -> 6`, `ts2-ts-basic-service-request-replace-method-hjnzfp` rank `1 -> 4`, and six cases rank `1 -> 3`.
- Regressed groups: mostly `response-replace-code`, `request-replace-method`, `response-replace-body`, `request-abort`, `response-abort`, and two `pod-failure` cases. These are consistent with the topology penalty demoting true roots that sit at central request/response positions.
- Net effect: AC@1, MRR, AC@3, and AC@5 all improve, so the regression set is acceptable but should guide the next topology refinement.

## Decision

- Accept / reject / keep for later: accept V3 as the current default.
- Reason: full eval has `error=0`; guard has no high-risk warning; all primary metrics improve; the algorithm change is a global, explainable feature-fusion rule with no label, datapack, service, or fault branching.
- Next smallest general step: split topology into direction-aware neighbor contrast rather than a uniform degree penalty, so central true roots can retain self-anomaly evidence while propagated high-degree neighbors are suppressed.
