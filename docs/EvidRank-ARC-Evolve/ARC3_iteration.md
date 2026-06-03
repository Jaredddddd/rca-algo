# EvidRank-ARC ARC3 Iteration

- Created: 2026-06-03T17:57:13+08:00
- Hypothesis: ARC2 的固定 blending 常量应替换为由当前 case 可用 evidence family 数自动确定的结构化融合，以保持 ARC 的无显式超参数自适应定位
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: ARC2 improved accuracy, but `ARC_FAMILY_RELIABILITY_BLEND = 0.25` and `ARC_FAMILY_CONTRAST_BLEND = 0.5` are explicit global blend hyperparameters. Replace them with structural, case-derived coefficients based on the number of active evidence families.
- Why this should transfer beyond RCABench: the coefficients should come from available evidence-family count rather than dataset tuning. The algorithm still uses only current-case feature distributions and raw trace-derived family structure, with no label, service, fault, or datapack information.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC2/`
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC2_summary.md`
- Baseline metrics: AC@1 `0.720113`, MRR `0.832050`, AC@3 `0.940928`, AC@5 `0.973277`, error `0`.
- Key weak groups: remaining hard cases are sparse infrastructure roots plus delay/partition/loss cases where propagation-shaped evidence can be a true root signature.
- Representative concern: ARC2's improvement is real, but the explicit blend constants weaken the no-explicit-hyperparameter story for EvidRank-ARC.

## Planned Change

- Minimal algorithm change:
  - remove `ARC_FAMILY_RELIABILITY_BLEND` and `ARC_FAMILY_CONTRAST_BLEND`;
  - return the active family count from family-level reliability calibration;
  - derive reliability blend as `1 / active_family_count`;
  - derive contrast blend as `1 / sqrt(active_family_count)`, treating local-vs-propagation contrast as a variance-normalized family correction rather than a tuned constant.
- Offline candidate metrics before code change:
  - ARC1: AC@1 `0.705345`, MRR `0.823675`, AC@3 `0.940225`, AC@5 `0.971167`;
  - ARC2 structural-count replacement: AC@1 `0.720113`, MRR `0.832050`, AC@3 `0.940928`, AC@5 `0.973277`;
  - equal-view `base + family + familyplusdelta`: AC@1 `0.718003`, MRR `0.830437`, AC@3 `0.941632`, AC@5 `0.973277`;
  - rank equal-view variants were lower, so structural-count replacement is the best no-explicit-blend candidate.
- Expected metric movement: should match ARC2 on the current dataset while removing explicit blend constants.
- Known regression risk: if a future case has fewer active evidence families, the derived correction will become stronger than ARC2's fixed coefficients. That is intended self-adaptation but should be watched in non-RCABench validation.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC3/`
- New summary: `docs/EvidRank-ARC-Evolve/ARC3_summary.md`
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC2_vs_ARC3.md`
- AC@1: `0.720113`
- AC@3: `0.940928`
- AC@5: `0.973277`
- MRR: `0.832050`
- Error: `0`

## Case Deltas

- Improved relative to ARC2: none; all `1422` cases are unchanged.
- Regressed relative to ARC2: none; all `1422` cases are unchanged.
- Effective improvement relative to ARC1 remains ARC2's gain: AC@1 `0.705345 -> 0.720113`, MRR `0.823675 -> 0.832050`, AC@3 `0.940225 -> 0.940928`, AC@5 `0.971167 -> 0.973277`.

## Decision

- Accept / reject / keep for later: accept ARC3 as the current EvidRank-ARC line, superseding ARC2.
- Reason: ARC3 removes the explicit `0.25` and `0.5` blend constants, keeps guard clean, completes full eval with `error=0`, and is output-equivalent to ARC2 on all 1422 cases.
- Next smallest general step: continue from ARC3, not ARC2; make the local-vs-propagation correction self-dampen when propagation evidence is internally consistent, using only current-case family statistics.
