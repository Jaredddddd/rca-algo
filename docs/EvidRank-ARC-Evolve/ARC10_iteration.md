# EvidRank-ARC ARC10 Iteration

- Created: 2026-06-03T22:25:56+08:00
- Hypothesis: 用 active-score anchored self-supervised reliability 学习 family 与 local-contrast 校正幅度，替代固定 family_count blend 且避免 ARC9 视图平均稀释根因锚点
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files changed: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: keep active score as the base ranking and learn only the family and local-contrast correction magnitude from case-local view reliability.
- Why this should transfer beyond RCABench: view reliability is computed from support, concentration, top-gap, and peer agreement within the current incident.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC7/`.
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC7_summary.md`.
- Baseline metrics: AC@1 `0.728551`, MRR `0.836843`, AC@3 `0.943741`, AC@5 `0.973277`, error `0`.
- Representative concern: ARC9 showed that averaging complete score views destroys the useful active-score anchor.

## Planned Change

- Minimal algorithm change:
  - replace pure view averaging with `active + learned_family_delta + learned_contrast_delta`;
  - learn view weights from the same reliability component diagnostics already used by ARC feature reliability;
  - keep endpoint gate legacy to isolate family behavior.
- Expected metric movement: recover ARC7 metrics if the active anchor is sufficient.
- Known regression risk: view reliability may still underweight or misweight the contrast correction, failing to reproduce ARC7's correction strength.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC10/`.
- New summary: `docs/EvidRank-ARC-Evolve/ARC10_summary.md`.
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC10.md`.
- AC@1: `0.675809` (`-0.052742` vs ARC7).
- AC@3: `0.918425` (`-0.025316` vs ARC7).
- AC@5: `0.964838` (`-0.008439` vs ARC7).
- MRR: `0.801007` (`-0.035836` vs ARC7).
- Error: `0`.

## Case Deltas

- Improved/regressed pattern remained essentially ARC9-like.
- Failure mechanism: learning free view correction magnitudes from agreement/reliability still fails because the useful family correction is a structural RCA transform, not just a reliable peer view. The contrast term must remain tied to local-vs-propagation role structure.

## Decision

- Accept / reject / keep for later: reject.
- Reason: no recovery relative to ARC9; active anchoring alone is not enough if the correction magnitude is learned from generic view reliability.
- Next smallest general step: preserve the ARC7 correction shape but replace integer active-family count with a smoother case-local effective participation estimate.
