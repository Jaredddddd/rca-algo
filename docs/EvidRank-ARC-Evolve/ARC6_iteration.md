# EvidRank-ARC ARC6 Iteration

- Created: 2026-06-03T20:04:22+08:00
- Hypothesis: 用 case-local 自监督 meta-calibration 和 trace pairwise role discovery 替代 ARC 中固定 reliability 权重、固定 endpoint gate 与人工 mutation/propagation 分组
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: replace ARC's remaining fixed calibration choices with case-local self-supervision. The target is to remove fixed reliability meta-weights, fixed case-scale clipping, fixed endpoint gate factors, and fixed mutation/propagation feature groups from the ARC ranking path.
- Why this should transfer beyond RCABench: the candidate should learn calibration strength and root/victim feature roles from the current case's feature distributions and raw trace pairwise contrasts, not from labels, service names, fault names, dataset identifiers, or manually assigned feature weights.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC5/`
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC5_summary.md`
- Baseline metrics: AC@1 `0.728551`, MRR `0.836412`, AC@3 `0.940225`, AC@5 `0.973277`, error `0`.
- Key weak groups: remaining weak groups include sparse infrastructure roots, bandwidth, response/request body/path/code cases, and propagation-shaped roots where ARC5 can over-interpret a neighbor as victim.
- Representative false cases: ARC5 still has `386` top-1 misses and `38` top-5 misses.

## Planned Change

- Minimal algorithm change candidates:
  - derive reliability meta-weights from the current case's reliability-diagnostic matrix instead of using fixed coefficients;
  - scale features by positive p95 without a fixed global clip, or derive any cap from the column's own positive distribution;
  - bypass the fixed endpoint support gate in ARC scoring;
  - discover root-side and victim-side feature roles from trace-neighbor pairwise contrasts instead of using `ARC_DIRECTIONAL_MUTATION_FEATURES` and `ARC_DIRECTIONAL_PROPAGATION_FEATURES`.
- Expected metric movement: a candidate should at least preserve ARC5's AC@1/MRR trend; if it regresses materially, it should be recorded as evidence that some RCA inductive bias is still necessary.
- Known regression risk: removing semantic role priors may let high-volume propagation features, row-count effects, or entry-service traffic dominate again.

## Offline Candidate Results

All offline candidates read only raw case frames. Labels were used only for final metric calculation.

| candidate | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | ---: | ---: | ---: | ---: | --- |
| ARC5 baseline | 0.728551 | 0.836412 | 0.940225 | 0.973277 | baseline |
| full no-fixed calibration, best candidate | 0.652602 | 0.786702 | 0.910689 | 0.957806 | reject |
| remove endpoint gate only, best candidate | 0.680731 | 0.806767 | 0.923347 | 0.967651 | reject |
| remove fixed clip only, best candidate | 0.585091 | 0.749176 | 0.913502 | 0.969761 | reject |
| replace fixed reliability meta-weight with case-local PCA | 0.728551 | 0.836841 | 0.943741 | 0.973277 | accept |

The negative result is important: removing all remaining ARC design at once is not a safe unsupervised baseline. The acceptable step is narrower: remove the fixed reliability coefficient vector and let the current case's reliability-diagnostic matrix determine the meta-weights.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC6/`
- New summary: `docs/EvidRank-ARC-Evolve/ARC6_summary.md`
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC5_vs_ARC6.md`
- AC@1: `0.728551` (unchanged vs ARC5)
- AC@3: `0.943741` (`+0.003516` vs ARC5)
- AC@5: `0.973277` (unchanged vs ARC5)
- MRR: `0.836841` (`+0.000429` vs ARC5)
- Error: `0`

## Case Deltas

- Improved: `5` improved to hit@1 and `16` additional rank improvements.
- Regressed: `5` regressed from hit@1 and `9` additional rank regressions.
- Improved modes include response-delay, request-replace-path, stress, bandwidth, loss, partition, request-delay, request-abort, corrupt, and infrastructure-like cases where PCA reliability gives more useful evidence-family separation.
- Regressed modes include pod-failure, bandwidth, stress, return, response-replace-code/body, request-abort, and request-replace-method where the changed reliability meta-weight shifts sparse local evidence behind high-traffic neighbors.

## Decision

- Accept / reject / keep for later: accept ARC6 as the current EvidRank-ARC line.
- Reason: ARC6 removes the fixed reliability meta-weight constants from the ARC path, keeps full eval `error=0`, improves MRR and AC@3, and does not reduce AC@1 or AC@5.
- What remains intentionally not removed: fixed case-scale clipping, endpoint support gate, and semantic mutation/propagation role groups. Full-case ablations show that removing them causes large AC@1/MRR regressions, so they should be reframed as explicit RCA inductive biases or replaced only by stronger self-supervised mechanisms.
- Next smallest general step: learn endpoint support and mutation/propagation role grouping from unlabeled trace-pair objectives, but keep the current versions as guarded fallbacks until the learned alternatives beat ARC6.
