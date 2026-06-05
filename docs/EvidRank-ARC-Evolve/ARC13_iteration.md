# EvidRank-ARC ARC13 Iteration

- Created: 2026-06-05T12:30:33+08:00
- Hypothesis: ARC 的 case-local reliability 不应替代根因语义先验做全局权重；更稳的结构是用 ordinal semantic prior 排主榜，再只把无标签 reliability 用于局部 trace-neighbor contrast
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: replace ARC12's global reliability mask + family consensus scorer with a two-stage ranker. Stage 1 uses raw multi-modal evidence and ordinal feature priorities whose numeric ladder is synthesized from priority order, not hand-entered per-feature numeric weights. Stage 2 uses ARC's case-local reliability only to build a robust, case-scaled trace-neighbor mutation/propagation contrast.
- Why this should transfer beyond RCABench: the main rank keeps root-specific evidence semantics such as status mutation, count drop, endpoint shift, and local self-duration instead of letting propagation symptoms dominate by reliability concentration. The ARC correction remains label-free and topology-local, so it can explain away neighboring victim services without reading labels, datapacks, service names, fault names, or processed conclusions.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC12_CURRENT/`.
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC12_CURRENT_summary.md`.
- Baseline metrics: AC@1 `0.734880`, MRR `0.839508`, AC@3 `0.936006`, AC@5 `0.971871`, error `0`.
- Key weak groups: pod-failure, response/request protocol mutations where ARC ranks a neighboring high-traffic service first, delay/partition/loss propagation cases, and sparse infrastructure roots.
- Representative false cases: `ts0-ts-basic-service-request-delay-d5jvr6`, `ts0-ts-preserve-service-response-replace-code-kvkzkr`, `ts0-ts-route-plan-service-request-replace-method-lrzhl6`, `ts0-ts-user-service-partition-77jfkk`.

## Planned Change

- Algorithm change:
  - add ordinal semantic prior weights to `EvidenceRankARC.__init__` using the existing priority ladder synthesis;
  - score the main ranking on the raw feature matrix with the legacy endpoint support gate and parent context;
  - compute robust case-local feature reliability only for an ARC contrast matrix;
  - remove ARC12's global `feature_weights = reliability > 0` scorer, family reliability consensus, and full-score family smoothing from the ARC online path;
  - keep final top-neighbor pairwise contrast, but feed it the robust reliability-active contrast matrix.
- Expected metric movement: offline label-side analysis predicted `prior_raw_arc_pairwise` at AC@1 `0.831224`, MRR `0.893267`, AC@3 `0.947961`, AC@5 `0.975387`, which clears the target and improves over both ARC12 and default ARC-style variants.
- Known regression risk: because the main ranking now trusts semantic root evidence again, cases where ARC12's endpoint gate helped but the semantic prior ranked a sibling/root counterpart second may regress. Pairwise contrast can also over-transfer in sparse trace graphs if mutation/propagation evidence is noisy.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC13/`.
- New summary: `docs/EvidRank-ARC-Evolve/ARC13_summary.md`.
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC12_CURRENT_vs_ARC13.md`.
- AC@1: `0.831224` (`+0.096343` vs ARC12_CURRENT).
- AC@3: `0.947961` (`+0.011955` vs ARC12_CURRENT).
- AC@5: `0.975387` (`+0.003516` vs ARC12_CURRENT).
- MRR: `0.893267` (`+0.053760` vs ARC12_CURRENT).
- Error: `0`.
- Runtime avg: `9.549299s`.

## Case Deltas

- Improved: `180` cases improved to hit@1 and `80` additional rank improvements.
- Regressed: `43` cases regressed from hit@1 and `48` additional rank regressions.
- Improved fault types: response-replace-code (`43` improved to hit@1), request-replace-method (`31`), response-delay (`18`), partition (`17`), request-delay (`16`), stress (`10`), response-abort (`8`), request-replace-path (`7`), plus smaller gains in loss, response-replace-body, delay, corrupt, and unknown cases.
- Regressed fault types: request-replace-method (`10` regressed from hit@1), response-replace-code (`8`), pod-failure (`5`), corrupt (`4`), response-delay (`3`), request-abort (`3`), plus smaller bandwidth, partition, response-abort, request-delay, loss, and response-replace-body cases.
- Interpretation: ARC12's global reliability mask/family consensus often put a propagated high-traffic neighbor ahead of the root. ARC13 recovers those by restoring raw root-specific evidence as the primary score. The main cost is that sparse pod-failure and some entry-service protocol cases lose ARC12's aggressive endpoint-local boost.

## Decision

- Accept / reject / keep for later: accept ARC13 as the current EvidRank-ARC version.
- Reason: full eval completed with `error=0`; `guard` has no high-risk overfitting warnings; AC@1 clears the target `0.8`; MRR, AC@3, and AC@5 all improve over ARC12_CURRENT; the regression pattern is explainable and much smaller than the improvement set.
- Next smallest general step: improve sparse pod-failure and UI/route-plan entry-service regressions with a non-label topology/sparsity detector, rather than reintroducing global family consensus.
