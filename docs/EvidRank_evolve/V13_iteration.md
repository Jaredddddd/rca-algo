# EvidenceRank V13 Iteration

- Created: 2026-06-02T17:59:11+08:00
- Hypothesis: 用单 case 内的特征覆盖、峰值对比、证据集中度和跨模态一致性无监督学习 feature 权重，替代手工固定先验以提升 EvidenceRank 的可迁移性论证
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: replace the fixed per-feature prior table with case-local unsupervised feature weighting. Each feature column is robustly normalized inside the current case, then weighted by its own positive support, evidence concentration, peak contrast, top-rank gap, and agreement with other feature families/modalities.
- Why this should transfer beyond RCABench: observability signals should be trusted when they are present, discriminative, localized, and corroborated by neighboring evidence in the same case. These criteria do not depend on labels, datapack IDs, service names, fault names, or RCABench-specific splits.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V11/`
- Baseline summary: `docs/EvidRank_evolve/V11_summary.md`
- Baseline metrics: AC@1 0.802391, MRR 0.875337, AC@3 0.943741, AC@5 0.975387, error 0.
- Note on versioning: `V12` is already occupied by an identical-output snapshot/report residue, so this robustness iteration uses `V13` rather than reusing the old version number.
- Key weak groups: V11 remains weak on pod-failure, request-abort, response-replace-body, bandwidth, and some infrastructure-root cases.
- Representative false cases: the V11 summary lists hard cases where high-traffic propagated services can outrank local roots. These are used only for offline validation and do not enter algorithm code.

## Planned Change

- Minimal algorithm change:
  - Remove the fixed `FEATURE_WEIGHTS` lookup from the ranking path.
  - Keep raw feature extraction, endpoint confidence gate, and parent trace context unchanged.
  - Add robust per-case column normalization so metric, trace, log, and row-count features share a comparable scale without hand tuning.
  - Learn feature weights from the current case using support, entropy concentration, p95-vs-median contrast, top1-vs-top2 gap, and cosine agreement with peer/cross-modal evidence.
- Expected metric movement: AC@1 may drop from the V11 80% level because the fixed V10/V11 priors encoded useful empirical preferences. A drop toward roughly 75% is acceptable if guard is clean, error remains 0, and AC@3/AC@5 do not collapse.
- Known regression risk: single-modality roots may be demoted if cross-modal agreement is too strict; high-volume propagation nodes may rise if row-count or traffic features appear concentrated but are not causal.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V13/`
- New summary: `docs/EvidRank_evolve/V13_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_V11_vs_V13.md`
- Full eval: 1422 cases, error 0, batch wall time 299.904091s with `--use-cpus 48`.
- Runtime avg: 9.715801s.
- AC@1: 0.802391 -> 0.679325 (-0.123066)
- AC@3: 0.943741 -> 0.926864 (-0.016878)
- AC@5: 0.975387 -> 0.966245 (-0.009142)
- MRR: 0.875337 -> 0.804981 (-0.070356)

## Case Deltas

- Improved: 63 `improved_to_hit1` and 44 additional `rank_improved` cases. Gains mostly come from rank-2 cases where a strongly localized local signal becomes visible once hand priors are removed.
- Regressed: 238 `regressed_from_hit1` and 82 additional `rank_regressed` cases. This is too large for the robustness trade-off target, even though AC@3/AC@5 only drop moderately.
- Interpretation: pure case-local column normalization plus one-pass feature reliability behaves too much like equalized feature fusion. It removes the appearance of manual tuning, but it also loses the stable high-confidence structure learned in earlier iterations.

## Decision

- Accept / reject / keep for later: reject V13 as the default EvidenceRank version.
- Reason: guard is clean and full eval has error 0, but AC@1 drops below the user's acceptable robustness target, from 80.24% to 67.93%. The mechanism is useful as an ablation showing why a naive no-prior formulation is insufficient.
- Next smallest general step: keep the no-label/no-service/no-feature-table constraint, but replace one-pass feature weighting with an unsupervised self-consistency estimator. Feature weights should be high when the feature is discriminative and agrees with an iteratively learned consensus over services/modalities, while noisy modalities such as logs should be downweighted automatically.
