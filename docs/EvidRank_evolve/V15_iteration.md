# EvidenceRank V15 Iteration

- Created: 2026-06-02T18:24:36+08:00
- Hypothesis: 用单 case 内的效应量、局部性、分布对比和跨特征一致性无监督学习 feature 权重，替代固定 feature prior，并避免多视图融合把尖锐但不一致的受害侧异常推到 Top-1
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: V13/V14 removed the fixed prior table, but robust column equalization erased useful effect-size structure and V14 view fusion over-promoted sharp but non-causal modality views. V15 learns feature weights inside each case from raw effect size, locality, distribution contrast, and agreement with a consensus over all evidence.
- Why this should transfer beyond RCABench: a root-cause signal should be present, localized, contrasted against peers, and consistent with other evidence in the same incident. These criteria are independent of labels, datapack IDs, service names, fault names, and dataset-specific splits.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V14/`
- Baseline summary: `docs/EvidRank_evolve/V14_summary.md`
- Reference accepted version: V11 has AC@1 0.802391, MRR 0.875337, AC@3 0.943741, AC@5 0.975387.
- Key weak groups: V14 is weak on response-replace-body/code, request-replace-path/method, pod-failure, and broad entry-side/service-chain cases because view fusion trusts concentrated victim-side scores.
- Representative false cases: V14 compare shows 272 `regressed_from_hit1` vs V11. These are used only for offline validation and do not enter algorithm logic.

## Planned Change

- Minimal algorithm change:
  - Keep the fixed `FEATURE_WEIGHTS` table removed from the ranking path.
  - Keep robust per-case feature scaling for comparable evidence addition.
  - Learn feature weights from raw feature effect size, locality, p95-vs-median contrast, support, and scaled-column reliability.
  - Iterate the weights against a single all-feature consensus instead of fusing multiple modality views.
- Expected metric movement: recover from V13/V14 toward the user's robustness target around 0.75 AC@1 while keeping no fixed feature prior table and error 0.
- Known regression risk: locality can underweight broad but real system-wide metric anomalies; consensus can suppress a valid single-modality root if other modalities are sparse or missing.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=INFO uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V15/`
- New summary: `docs/EvidRank_evolve/V15_summary.md`
- Compare reports: `docs/EvidRank_evolve/compare_V14_vs_V15.md`, `docs/EvidRank_evolve/compare_V11_vs_V15.md`
- Full eval: 1422 cases, error 0, batch wall time 304.126028s with `--use-cpus 48`.
- Runtime avg: 9.890354s.
- AC@1: 0.638537
- AC@3: 0.884669
- AC@5: 0.949367
- MRR: 0.772135
- V14 -> V15 delta: AC@1 -0.018987, MRR -0.018966, AC@3 -0.029536, AC@5 -0.012658.
- V11 -> V15 delta: AC@1 -0.163854, MRR -0.103202, AC@3 -0.059072, AC@5 -0.026020.

## Case Deltas

- Improved: 71 `improved_to_hit1` vs V14. These are mainly cases where localized delay/stress/corrupt evidence becomes visible under the raw-effect-aware weighting.
- Regressed: 98 `regressed_from_hit1` vs V14 and 304 vs V11. Pod-failure, response-replace-body/code, and request replacement groups regress materially.

## Decision

- Accept / reject / keep for later: reject as default; keep as an ablation.
- Reason: V15 remains label-free and guard-clean, but AC@1 drops to 0.638537 and AC@3/AC@5 also fall more than acceptable. The locality term over-penalizes broad availability and endpoint symptoms, while logs and high-volume victim services still pull many cases away from the root.
- Next smallest general step: learn modality participation before feature participation. Use metric+trace as an unlabeled backbone and let log evidence join only when its service ranking agrees with that backbone, so noisy log bursts cannot dominate Top-1.
