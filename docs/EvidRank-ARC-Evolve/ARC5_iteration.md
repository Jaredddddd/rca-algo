# EvidRank-ARC ARC5 Iteration

- Created: 2026-06-03T18:58:37+08:00
- Hypothesis: 用 trace 邻接上的 top-neighbor pairwise root-vs-victim contrast 替代全局 pseudo-vector cosine，对 feature prior 做自监督合成
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`, only if an offline full-case candidate beats ARC3 safely.
- General RCA mechanism being tested: replace ARC4's global pseudo-root / pseudo-victim cosine alignment with self-supervised pair construction on raw trace adjacency. For each directed trace edge, the candidate treats a neighbor as root-like only when it has stronger mutation evidence than its adjacent service while the adjacent service has stronger propagation evidence. The accepted version uses this pairwise root-vs-victim target as a final score transfer, not as a full replacement feature prior.
- Why this should transfer beyond RCABench: the mechanism uses only current-case feature distributions and raw trace parent-child direction. It does not read labels, injection metadata, historical outputs, service names, fault names, or `FEATURE_WEIGHTS`.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC3/`
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC3_summary.md`
- Baseline metrics: AC@1 `0.720113`, MRR `0.832050`, AC@3 `0.940928`, AC@5 `0.973277`, error `0`.
- Key weak groups: pod-failure, response/request protocol mutation cases, bandwidth, and sparse infrastructure roots remain difficult for ARC3.
- Representative false cases: ARC3 has `398` top-1 misses and `38` top-5 misses; ARC4 showed that a broad local-vs-propagation pseudo-vector regresses head accuracy.

## Planned Change

- Minimal algorithm change:
  - compute ARC3 scores unchanged;
  - construct trace-directed neighbor pairs from current-case mutation and propagation family evidence;
  - for each victim service, keep only the strongest neighbor explanation, which makes "top-neighbor" a structural selection instead of a fixed top-k;
  - transfer score from a propagation-heavy higher-scored victim to a mutation-heavier adjacent root candidate in proportion to the current score gap and pairwise evidence shares;
  - avoid any fixed feature weights, dataset identifiers, labels, injection metadata, historical outputs, or service-name rules.
- Expected metric movement: target is to exceed ARC3's AC@1 `0.720113` or MRR `0.832050`; AC@3 and AC@5 should remain close to ARC3 without unexplained large regression.
- Known regression risk: pairwise trace contrast may over-promote downstream services with localized symptoms, or suppress true delay / partition roots where propagation-shaped evidence is causal rather than victim-only.

## Offline Candidate Results

All candidates were evaluated on the full 1422-case dataset by reading raw frames and using labels only for final metrics.

| candidate family | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | ---: | ---: | ---: | ---: | --- |
| ARC3 baseline | 0.720113 | 0.832050 | 0.940928 | 0.973277 | baseline |
| pairwise feature-prior / score-view variants | best 0.677918 | best 0.798604 | best 0.921941 | best 0.962025 | reject |
| final childroot-only transfer | 0.724332 | 0.834198 | 0.942335 | 0.973277 | safe but lower AC@1 |
| final bidirectional top-neighbor transfer | 0.728551 | 0.836412 | 0.940225 | 0.973277 | accept |
| final bidirectional transfer with upstream in-degree gate | 0.725035 | 0.834829 | 0.940928 | 0.973277 | keep as fallback |

The key finding is that pairwise pseudo targets are useful as a local score correction, but still too unstable as a direct feature-prior replacement.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC5/`
- New summary: `docs/EvidRank-ARC-Evolve/ARC5_summary.md`
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC3_vs_ARC5.md`
- AC@1: `0.728551` (`+0.008439` vs ARC3)
- AC@3: `0.940225` (`-0.000703` vs ARC3)
- AC@5: `0.973277` (unchanged vs ARC3)
- MRR: `0.836412` (`+0.004362` vs ARC3)
- Error: `0`

## Case Deltas

- Improved: `15` improved to hit@1 and `14` additional rank improvements.
- Regressed: `3` regressed from hit@1 and `9` additional rank regressions.
- Improved modes: response/request protocol mutation, request/response delay, pod-failure, container-kill, corrupt, and request-replace-path cases where ARC3 ranked a propagation-heavy neighbor just above a mutation-heavier adjacent root.
- Regressed modes: loss, corrupt, request-delay, bandwidth, partition, and request-replace-method cases where propagation-shaped evidence can be causal or an upstream/entry-like service can look mutation-heavier than the labeled root.

## Decision

- Accept / reject / keep for later: accept ARC5 as the current EvidRank-ARC line.
- Reason: guard has no high-risk warnings, full eval has `error=0`, AC@1 and MRR improve, AC@5 is unchanged, and the tiny AC@3 regression is explained by the expected propagation-as-root risk.
- Next smallest general step: study a no-constant topology confidence gate for upstream-root transfer, such as damping reverse-direction transfer by trace in-degree support, because it reduces hit@1 regressions but currently gives up part of ARC5's AC@1 gain.
