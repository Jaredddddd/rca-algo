# EvidRank-ARC ARC9 Iteration

- Created: 2026-06-03T21:50:16+08:00
- Hypothesis: 隔离 ARC8 退化来源：保留自监督 family consensus，但端点支持暂回 legacy gate，验证 family 视图投票是否可独立替代固定融合比例
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files changed: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: isolate ARC8 by keeping self-supervised family consensus but restoring the legacy endpoint gate in ARC, to determine whether the family view replacement was the main regression source.
- Why this should transfer beyond RCABench: the family consensus candidate used only current-case active/family/local-contrast score views, not labels or dataset-specific identifiers.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC7/`.
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC7_summary.md`.
- Baseline metrics: AC@1 `0.728551`, MRR `0.836843`, AC@3 `0.943741`, AC@5 `0.973277`, error `0`.
- Representative concern: ARC8 regressed heavily, and the source needed isolation before designing a safer learned replacement.

## Planned Change

- Minimal algorithm change:
  - leave the ARC8 self-supervised family view averaging in place;
  - switch ARC endpoint scoring and weighted matrices back to `_apply_trace_endpoint_support_gate`;
  - keep default `evidencerank` unchanged.
- Expected metric movement: if endpoint gate was the main problem, ARC9 should recover near ARC7.
- Known regression risk: if family view averaging is the main problem, ARC9 should remain far below ARC7.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC9/`.
- New summary: `docs/EvidRank-ARC-Evolve/ARC9_summary.md`.
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC7_vs_current.md` for the current output and later `compare_ARC7_vs_ARC10.md` for the equivalent ARC10 candidate.
- AC@1: `0.675809` (`-0.052742` vs ARC7).
- AC@3: `0.918425` (`-0.025316` vs ARC7).
- AC@5: `0.964838` (`-0.008439` vs ARC7).
- MRR: `0.801007` (`-0.035836` vs ARC7).
- Error: `0`.

## Case Deltas

- Improved/regressed details are materially similar to ARC10 because ARC10 produced the same headline metrics.
- Failure mechanism: family view averaging, not endpoint gate, is the dominant regression source. It removes the original active-score anchor and turns family/contrast into an averaging problem, which is too weak for root-vs-victim ordering.

## Decision

- Accept / reject / keep for later: reject.
- Reason: restoring the endpoint gate did not recover accuracy; the family consensus replacement itself is unsafe.
- Next smallest general step: keep active score as an anchor and learn only the family/contrast correction magnitude.
