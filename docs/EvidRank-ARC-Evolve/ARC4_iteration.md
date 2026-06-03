# EvidRank-ARC ARC4 Iteration

- Created: 2026-06-03T18:42:42+08:00
- Hypothesis: 用当前 case 的 local family 证据与 propagation/topology 证据构造 pseudo-root/pseudo-victim，对 feature 做自监督 causal alignment，从而合成接近 RCA 语义先验的无标签 adaptive prior
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: synthesize a case-local feature prior by aligning each feature with pseudo-root and pseudo-victim service vectors. Pseudo-root is derived from local family evidence (`metric + mutation + log`) that exceeds propagation evidence; pseudo-victim is derived from propagation/topology evidence that exceeds local evidence. A feature gets more weight when it aligns with pseudo-root and less when it aligns with pseudo-victim.
- Why this should transfer beyond RCABench: the mechanism depends on feature distributions, evidence families, and raw trace topology inside the current incident. It does not read labels, injection metadata, historical outputs, service names, fault names, or `FEATURE_WEIGHTS`.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC3/`
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC3_summary.md`
- Baseline metrics: AC@1 `0.720113`, MRR `0.832050`, AC@3 `0.940928`, AC@5 `0.973277`, error `0`.
- Key weak groups: remaining weak groups include `pod-failure`, protocol mutation cases with deep rank misses, `bandwidth`, and delay/partition/loss cases where propagation-shaped evidence can be causal.
- Representative false cases: ARC3 still has 398 top-1 misses and 38 top-5 misses; the goal is to recover more of the fixed-prior behavior without inserting fixed per-feature weights.

## Planned Change

- Minimal algorithm change:
  - reuse ARC3 p95 case scaling, active-feature mask, family reliability, family local-vs-propagation contrast, and directional contrast;
  - create pseudo-root and pseudo-victim service vectors from current-case family evidence only;
  - score every enabled feature by cosine alignment to pseudo-root versus pseudo-victim, gated by existing single-case feature reliability;
  - use the synthesized prior as an additional no-label score view only if offline full-case testing shows it improves AC@1/MRR without harming AC@3/AC@5.
- Expected metric movement: target is to exceed ARC3's AC@1 `0.720113`; a useful candidate should improve AC@1 or MRR and avoid AC@3/AC@5 regression.
- Known regression risk: pseudo-root construction may over-favor local metric/log noise, while pseudo-victim construction may wrongly suppress true delay/partition roots.

## Offline Candidate Results

All candidates were evaluated over the full 1422-case dataset by reading raw frames and using labels only at the final metric calculation step. No candidate was written into the algorithm.

| candidate | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | ---: | ---: | ---: | ---: | --- |
| `ARC3` baseline | 0.720113 | 0.832050 | 0.940928 | 0.973277 | keep |
| `ratio_structural_consensus` | 0.705345 | 0.823704 | 0.939522 | 0.974684 | reject |
| `rank_structural_consensus` | 0.703235 | 0.821802 | 0.936709 | 0.973980 | reject |
| `arc3_plus_synth_ratio_equal` | 0.694093 | 0.816899 | 0.938115 | 0.973980 | reject |
| `synth_ratio_direct` | 0.663854 | 0.797325 | 0.925457 | 0.973277 | reject |
| `synth_diff_direct` | 0.523910 | 0.665250 | 0.763010 | 0.843882 | reject |

Conservative arbitration also failed to beat ARC3:

| candidate | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | ---: | ---: | ---: | ---: | --- |
| `gap_weighted_arc3_cons` | 0.709564 | 0.826269 | 0.940225 | 0.973980 | reject |
| `switch_to_cons_if_gap_better` | 0.709564 | 0.825376 | 0.938819 | 0.974684 | reject |
| `rank_gap_weighted_arc3_cons` | 0.709564 | 0.825333 | 0.939522 | 0.973980 | reject |
| `switch_to_synth_if_gap_better` | 0.694093 | 0.814893 | 0.932489 | 0.974684 | reject |

## Failure Mechanism

- The pseudo-root vector `max(metric + mutation + log - propagation, 0)` is too broad: it often marks local metric/log co-movement on victim services as root-specific.
- The pseudo-victim vector `max(propagation + topology - local, 0)` is too aggressive for delay, partition, and loss cases, where propagation-shaped evidence may be the causal symptom rather than only a downstream effect.
- Feature alignment by cosine similarity is too global across services. It rewards features that share the overall service-distribution shape, but root-cause ranking depends on subtle top-1/top-2 contrasts.
- The synthesized prior improves some top5 behavior, but it consistently loses head accuracy and MRR, which are the priority metrics.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: not created; no candidate accepted into algorithm output.
- New summary: not created; no full eval run because no code candidate beat ARC3 offline.
- Compare report: not created; ARC3 remains current accepted output.
- AC@1: best ARC4 candidate `0.709564`, below ARC3 `0.720113`.
- AC@3: best conservative candidate `0.940225`, slightly below ARC3 `0.940928`.
- AC@5: some candidates reached `0.974684`, above ARC3 `0.973277`, but at unacceptable AC@1/MRR cost.
- MRR: best ARC4 candidate `0.826269`, below ARC3 `0.832050`.

## Case Deltas

- Improved: not materialized into versioned output because no candidate was accepted.
- Regressed: synthesized prior candidates consistently regress AC@1/MRR; direct `diff` prior is especially harmful.

## Decision

- Accept / reject / keep for later: reject ARC4 candidate set; keep ARC3 as current EvidRank-ARC line.
- Reason: the self-supervised prior synthesis mechanism is directionally aligned with the desired story, but the current pseudo-root/pseudo-victim construction is not accurate enough for head ranking.
- Next smallest general step: improve pseudo-vector construction before retrying. A better version should use pairwise top-neighbor contrast and trace direction, not only global service-vector cosine alignment.
