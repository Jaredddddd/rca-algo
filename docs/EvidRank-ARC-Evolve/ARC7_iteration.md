# EvidRank-ARC ARC7 Iteration

- Created: 2026-06-03T21:05:58+08:00
- Hypothesis: 移除已被 top-neighbor pairwise contrast 吸收的旧 directional contrast，减少 ARC 排序路径中的人工 reranking 层
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: remove the older one-directional caller-victim score transfer because ARC5/ARC6's final top-neighbor pairwise contrast already handles the same root-vs-victim correction more locally.
- Why this should transfer beyond RCABench: removing a redundant reranking layer reduces hand-designed ordering logic. The remaining pairwise contrast still uses only current-case feature distributions and raw trace adjacency.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC6/`
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC6_summary.md`
- Baseline metrics: AC@1 `0.728551`, MRR `0.836841`, AC@3 `0.943741`, AC@5 `0.973277`, error `0`.
- Key weak groups: pod-failure, bandwidth, response/request mutation cases, and sparse infrastructure roots remain weak.
- Representative concern: ARC6 still had two reranking layers with overlapping mutation-vs-propagation assumptions: the older directional transfer and the newer top-neighbor pairwise transfer.

## Planned Change

- Minimal algorithm change:
  - remove `_apply_arc_directional_contrast`;
  - remove both calls from `EvidenceRankARC.__call__`;
  - keep family consensus and final top-neighbor pairwise contrast unchanged.
- Expected metric movement: ablation predicted AC@1/AC@3/AC@5 unchanged and a tiny MRR gain.
- Known regression risk: if some cases still need the older one-directional caller-victim transfer, removing it could regress top-1 or near-top ranks.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC7/`
- New summary: `docs/EvidRank-ARC-Evolve/ARC7_summary.md`
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC6_vs_ARC7.md`
- AC@1: `0.728551` (unchanged vs ARC6)
- AC@3: `0.943741` (unchanged vs ARC6)
- AC@5: `0.973277` (unchanged vs ARC6)
- MRR: `0.836843` (`+0.000002` vs ARC6)
- Error: `0`

## Case Deltas

- Improved: `1` rank-improved case.
- Regressed: `0`.
- The only changed case is a bandwidth case whose best GT rank improved from `19` to `18`.

## Decision

- Accept / reject / keep for later: accept ARC7 as the current EvidRank-ARC line.
- Reason: it removes an artificial reranking layer, keeps all headline accuracy metrics unchanged, slightly improves MRR, and has no case-level regression relative to ARC6.
- Next smallest general step: focus on learned replacements for endpoint support and mutation/propagation role priors, because current ablations show they still carry large accuracy value.
