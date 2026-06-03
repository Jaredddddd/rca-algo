# EvidRank-ARC ARC8 Iteration

- Created: 2026-06-03T21:34:10+08:00
- Hypothesis: 用单 case 内视图一致性和端点邻近支持自监督学习 family consensus 与 endpoint gate 强度，替代固定人工 gate 常数
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files changed: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: replace both ARC family consensus and endpoint support gate with case-local self-supervised view agreement. Family consensus used active/family/local-contrast score views and learned their weights from rank-view agreement. Endpoint gate used endpoint/status/rise rank alignment instead of fixed status/rise/penalty factors.
- Why this should transfer beyond RCABench: all diagnostics are computed from the current incident's feature matrix and raw trace-derived evidence. No labels, injection metadata, service names, fault names, historical outputs, or dataset-specific priors are read.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC7/`.
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC7_summary.md`.
- Baseline metrics: AC@1 `0.728551`, MRR `0.836843`, AC@3 `0.943741`, AC@5 `0.973277`, error `0`.
- Key weak groups: pod-failure, bandwidth, sparse infrastructure roots, and some propagation-shaped delay/loss cases.
- Representative concern: endpoint support and family consensus were still implemented as hand-designed correction layers rather than learned from current-case structure.

## Planned Change

- Minimal algorithm change:
  - add case-local rank-view helpers;
  - replace family blend with active/family/contrast consensus weights learned by view agreement;
  - replace ARC endpoint gate with endpoint/status/rise rank-alignment support;
  - keep default `evidencerank` path unchanged.
- Expected metric movement: preserve ARC7 AC@1/MRR while reducing manual calibration.
- Known regression risk: pure view agreement may over-favor broad propagation/entry views and dilute the root-like active score anchor; endpoint rank alignment may under-boost supported endpoint shifts compared with the legacy gate.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC8/`.
- New summary: `docs/EvidRank-ARC-Evolve/ARC8_RECHECK_summary.md`. Note: `ARC8_summary.md` was generated concurrently with snapshot creation and has `missing_outputs=998`; treat it as an invalid race artifact.
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC8.md`.
- AC@1: `0.677918` (`-0.050633` vs ARC7).
- AC@3: `0.917722` (`-0.026020` vs ARC7).
- AC@5: `0.963432` (`-0.009845` vs ARC7).
- MRR: `0.802414` (`-0.034429` vs ARC7).
- Error: `0`.

## Case Deltas

- Improved: `77` improved to hit@1 and `55` additional rank improvements.
- Regressed: `149` regressed from hit@1 and `93` additional rank regressions.
- Failure mechanism: the family view averaging diluted ARC7's active root-score anchor. Endpoint rank alignment helped some protocol mutation cases but could not compensate for the loss of family local-vs-propagation contrast.
- Likely improved case type: protocol mutation cases where endpoint/status/rise align around the true service.
- Likely regressed case type: delay, partition, loss, and propagation-shaped symptoms where broad victim/entry views look highly consistent.

## Decision

- Accept / reject / keep for later: reject.
- Reason: all headline metrics regress; AC@3 and AC@5 also fall. The result shows that removing fixed correction shape outright is too destructive.
- Next smallest general step: isolate whether the regression comes from family consensus or endpoint gate, then preserve active-score anchoring while learning only the correction strength.
