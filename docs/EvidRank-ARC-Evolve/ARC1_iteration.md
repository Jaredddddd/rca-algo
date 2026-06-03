# EvidRank-ARC ARC1 Iteration

- Created: 2026-06-03T15:00:27+08:00
- Hypothesis: 单 case feature reliability 估计会过度放大传播型尖峰；将 reliability 退化为 active-feature mask 并加入 trace 方向的 caller-victim contrast 可在无固定先验下改善 ARC 头部排序
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: single-case feature reliability can be too noisy to use as a sharp per-feature multiplier; use it as an active evidence mask, then apply trace-direction root-vs-victim contrast between caller propagation symptoms and callee mutation evidence.
- Why this should transfer beyond RCABench: the mechanism depends only on per-incident feature distributions and raw trace parent-child edges. It does not use dataset names, service names, fault names, labels, injection metadata, or historical outputs.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC_BASELINE/`
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC_BASELINE_summary.md`
- Baseline metrics: AC@1 `0.670886`, MRR `0.801983`, AC@3 `0.925457`, AC@5 `0.973980`, error `0`.
- Key weak groups: protocol mutation faults, especially `response-replace-code`, `request-replace-method`, `request-replace-path`, `response-replace-body`, and `response-abort`.
- Representative false cases: many ARC top1 misses have GT at rank 2 and are hit@1 by the fixed-prior default line, suggesting that ARC sees the root evidence but over-amplifies neighboring propagation symptoms.

## Planned Change

- Minimal algorithm change:
  - keep ARC p95 case-local feature scaling and endpoint support gate;
  - convert learned feature reliability into an active-feature mask instead of multiplying scores by noisy single-case reliability;
  - add a trace-edge directional contrast that transfers score from a higher-scored caller to a callee only when the caller has stronger propagation evidence and the callee has stronger mutation evidence.
- Offline candidate metrics before code change:
  - baseline ARC: AC@1 `0.670886`, MRR `0.801983`, AC@3 `0.925457`, AC@5 `0.973980`;
  - reliability power `p=0.5`: AC@1 `0.685654`, MRR `0.811940`, AC@3 `0.938115`, AC@5 `0.971871`;
  - active mask / equal reliability: AC@1 `0.702532`, MRR `0.822233`, AC@3 `0.940225`, AC@5 `0.971167`;
  - active mask plus directional contrast: AC@1 `0.705345`, MRR `0.823675`, AC@3 `0.940225`, AC@5 `0.971167`.
- Expected metric movement: AC@1 and MRR should improve; AC@3 should improve; AC@5 may drop slightly but should remain close to baseline.
- Known regression risk: infrastructure and hard pod/container cases may lose some top5 stability if neutralizing reliability removes useful concentrated signals.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC1/`
- New summary: `docs/EvidRank-ARC-Evolve/ARC1_summary.md`
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC_BASELINE_vs_ARC1.md`
- AC@1: `0.705345` (`954 -> 1003` Hit@1, +49)
- AC@3: `0.940225` (`1316 -> 1337`, +21)
- AC@5: `0.971167` (`1385 -> 1381`, -4)
- MRR: `0.823675` (`+0.021692`)
- Error: `0`

## Case Deltas

- Improved:
  - `improved_to_hit1`: 87 cases.
  - Largest fault groups: `response-replace-code` 36, `request-abort` 9, `request-delay` 8, `stress` 7, `request-replace-path` 6, `response-delay` 5, `request-replace-method` 5.
  - Typical pattern: old rank 2 root cases where a neighboring caller or high-traffic service was rank 1; active-mask scoring plus directional contrast lets the root service reclaim first place without fixed feature priors.
- Regressed:
  - `regressed_from_hit1`: 38 cases.
  - Largest fault groups: `request-replace-method` 7, `pod-failure` 6, `response-replace-code` 5, `partition` 5, `stress` 3, `bandwidth` 3.
  - `hit@5` regressions: 5 cases, with 1 `hit@5` improvement; net AC@5 delta is -4 cases.
  - Typical risk: infrastructure and hard topology cases sometimes needed a sharp concentrated reliability signal; active-mask neutralization flattens that signal and can let nearby high-traffic services move ahead.

## Decision

- Accept / reject / keep for later: accept ARC1 as the current EvidRank-ARC line.
- Reason: guard has no high-risk warnings, full eval completes with `error=0`, AC@1/MRR/AC@3 all improve materially, and AC@5 drops only 4 cases with an understood mechanism.
- Next smallest general step: recover some infrastructure/pod-failure stability without reintroducing fixed feature priors, likely by making active-mask neutralization conditional on cross-feature/topology disagreement or by adding a reliability confidence interval rather than a point multiplier.
