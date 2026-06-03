# EvidenceRank V14 Iteration

- Created: 2026-06-02T18:12:29+08:00
- Hypothesis: 用无监督自一致性同时学习 feature 权重和 modality-view 权重，通过可靠视图的 rank fusion 替代手工固定先验，在保持可迁移性的同时恢复 Top-1 稳定性
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: V13 removed the fixed feature table but over-equalized all evidence. V14 keeps the no-label/no-service/no-feature-table constraint while learning two levels of weights: feature weights from iterative self-consistency, and modality-view weights from score-distribution reliability.
- Why this should transfer beyond RCABench: microservice RCA systems often have uneven observability. A robust unsupervised ranker should prefer the view whose evidence is concentrated, contrasted, and self-consistent for the current incident rather than relying on hand-picked metric/trace/log weights.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V13/`
- Baseline summary: `docs/EvidRank_evolve/V13_summary.md`
- Baseline metrics: AC@1 0.679325, MRR 0.804981, AC@3 0.926864, AC@5 0.966245, error 0.
- Reference accepted version: V11 has AC@1 0.802391, MRR 0.875337, AC@3 0.943741, AC@5 0.975387.
- Key weak groups: V13 regressed many V11 Top-1 cases, especially response/request replacement and body/code cases, because globally equalized features diluted previously strong trace/status/count evidence.
- Representative false cases: V13 compare shows 238 `regressed_from_hit1` but also 63 `improved_to_hit1`, so the next mechanism should preserve no-prior gains without making every feature family equally trusted.

## Planned Change

- Minimal algorithm change:
  - Replace one-pass feature agreement with iterative self-consistency: feature weights are repeatedly updated from intrinsic reliability and agreement with the current consensus score vector.
  - Add modality-view candidates for the enabled modalities, including single modalities, pairs, and the full view.
  - Score each view independently with the same unsupervised feature learner, estimate view reliability from the service score distribution, and fuse views by reliability-weighted reciprocal-rank / normalized-score fusion.
- Expected metric movement: recover V13's AC@1 toward at least the user's robustness target around 75%, while keeping the no fixed per-feature prior table.
- Known regression risk: view fusion can over-promote a sharp but victim-side modality view; the parent-context and endpoint-support gates remain as generic propagation controls.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V14/`
- New summary: `docs/EvidRank_evolve/V14_summary.md`
- Compare reports: `docs/EvidRank_evolve/compare_V11_vs_V14.md`, `docs/EvidRank_evolve/compare_V13_vs_V14.md`
- Full eval: 1422 cases, error 0, batch wall time 309.796673s with `--use-cpus 48`.
- Runtime avg: 10.051229s.
- AC@1: 0.657525
- AC@3: 0.914205
- AC@5: 0.962025
- MRR: 0.791101
- V11 -> V14 delta: AC@1 -0.144866, MRR -0.084236, AC@3 -0.029536, AC@5 -0.013361.
- V13 -> V14 delta: AC@1 -0.021800, MRR -0.013880, AC@3 -0.012658, AC@5 -0.004219.

## Case Deltas

- Improved: 66 `improved_to_hit1` vs V11; 32 `improved_to_hit1` vs V13. These are mostly cases where a single local modality view makes the GT service sharply visible.
- Regressed: 272 `regressed_from_hit1` vs V11; 63 additional `regressed_from_hit1` vs V13. This indicates the view-level reliability estimate over-trusts sharp but victim-side or entry-side views.

## Decision

- Accept / reject / keep for later: reject as default; keep as a no-fixed-prior view-fusion ablation.
- Reason: guard and full eval are clean, but the main model falls to AC@1 0.657525, below the user's robustness target around 0.75 and below V13. The failure mechanism is general: score-distribution sharpness alone is not sufficient evidence of causality because propagated victim nodes and entry nodes can also produce concentrated modality views.
- Next smallest general step: remove view fusion and learn a single feature weighting over all evidence using raw effect size, locality, distribution contrast, and cross-feature self-consistency. The goal is to preserve the no-label/no-feature-table property without letting isolated sharp views dominate Top-1.
