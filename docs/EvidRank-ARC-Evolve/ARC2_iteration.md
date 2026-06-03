# EvidRank-ARC ARC2 Iteration

- Created: 2026-06-03T17:04:05+08:00
- Hypothesis: 服务级 family-local 证据与 propagation 证据的无标签对比可以修正 ARC1 的高流量传播型 rank-2 互换，同时用 family-level reliability 做保守校准而不恢复固定 feature prior
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: ARC1's active-feature mask avoids noisy per-feature reliability, but its final service sum still lets high-traffic propagation families beat a nearby service whose local metric/mutation/log evidence is more coherent. Add a bounded, case-local family correction: compare normalized local evidence families against propagation evidence, and let family-level reliability provide only a conservative group correction.
- Why this should transfer beyond RCABench: the mechanism uses only the current incident's feature matrix, raw trace topology, and feature family structure (`metric`, `trace mutation`, `trace propagation`, `log`). It does not use dataset names, service names, fault names, labels, injection metadata, historical outputs, or fixed per-feature priors.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC1/`
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC1_summary.md`
- Baseline metrics: AC@1 `0.705345`, MRR `0.823675`, AC@3 `0.940225`, AC@5 `0.971167`, error `0`.
- Key weak groups: `pod-failure` AC@1 `0.291667`, `response-replace-body` `0.431373`, `response-replace-code` `0.506494`, `request-replace-path` `0.512821`, `request-replace-method` `0.521053`.
- Representative false cases: ARC1 has `419` top-1 misses; `254` of them are rank-2 misses, and `373` misses have two GT services. Common rank-2 misses show the wrong top service with stronger propagation evidence, while the GT service has similar total score and stronger local metric/mutation/log evidence.

## Planned Change

- Minimal algorithm change:
  - keep ARC p95 case-local feature scaling, active-feature mask, endpoint support gate, parent context, and directional contrast;
  - aggregate the existing single-case feature reliability to family-level median reliability instead of using it as free per-feature weights;
  - compute a family-local contrast from p95-normalized family sums: `metric + mutation + log - propagation`;
  - combine `0.75 * ARC1 active base + 0.25 * family-reliability base + 0.5 * family-local contrast` as a bounded service-level correction.
- Offline candidate metrics before code change:
  - ARC1: AC@1 `0.705345`, MRR `0.823675`, AC@3 `0.940225`, AC@5 `0.971167`;
  - simple `base + 0.5 * family_delta`: AC@1 `0.714487`, MRR `0.829598`, AC@3 `0.940928`, AC@5 `0.972574`;
  - bounded family-reliability correction (`0.75/0.25` base blend plus `0.5` family delta): AC@1 `0.720113`, MRR `0.832050`, AC@3 `0.940928`, AC@5 `0.973277`.
- Expected metric movement: AC@1 and MRR should improve; AC@3 should stay flat or slightly improve; AC@5 should not regress and may recover some ARC1 top5 loss.
- Known regression risk: services whose real root evidence is mostly propagation-shaped, or infrastructure cases where the root has sparse local evidence, may be pushed down by the local-vs-propagation contrast.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC2/`
- New summary: `docs/EvidRank-ARC-Evolve/ARC2_summary.md`
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC1_vs_ARC2.md`
- AC@1: `0.720113` (`1003 -> 1024` Hit@1, +21)
- AC@3: `0.940928` (`1337 -> 1338`, +1)
- AC@5: `0.973277` (`1381 -> 1384`, +3)
- MRR: `0.832050` (`+0.008375`)
- Error: `0`

## Case Deltas

- Improved:
  - `improved_to_hit1`: 54 cases.
  - Largest fault groups: `response-replace-code` 17, `request-replace-method` 12, `pod-failure` 5, `response-abort` 5, `response-replace-body` 5.
  - Typical pattern: old rank-2 roots where the wrong top service had stronger propagation evidence, while the GT service had similar total score plus stronger local family evidence. ARC2 flips 52 rank-2 misses directly to rank 1.
  - Hard group improvement: `pod-failure` AC@1 improves from ARC1 `0.291667` to ARC2 `0.500000`, though it remains the weakest large fault group.
- Regressed:
  - `regressed_from_hit1`: 33 cases; all moved from rank 1 to rank 2.
  - Largest fault groups: `response-delay` 6, `request-delay` 6, `partition` 6, `delay` 4, plus smaller `bandwidth`, `corrupt`, `loss`, and `stress` groups.
  - Typical risk: delay/partition/loss style incidents can make the true root look propagation-shaped; the local-vs-propagation contrast may favor a nearby service with more local family evidence.
  - `rank_regressed`: 31 cases, mostly `request-replace-method`, `bandwidth`, `corrupt`, `response-delay`, `loss`, `request-abort`, and `response-replace-code`.

## Decision

- Accept / reject / keep for later: accept ARC2 as the current EvidRank-ARC line.
- Reason: guard has no high-risk warnings, full eval completes with `error=0`, and AC@1/MRR/AC@3/AC@5 all improve. The improvement is broad enough to offset the 33 rank-1 regressions, and the regression mechanism is interpretable rather than dataset-specific.
- Next smallest general step: make the local-vs-propagation correction self-dampen when delay/partition-like propagation evidence is internally consistent across trace families, without using fault labels or fixed feature priors.
