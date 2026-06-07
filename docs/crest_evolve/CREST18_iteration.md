# CREST18 Iteration

## Goal

Continue from accepted CREST17 default toward `AC@1 >= 0.85` for `crest` on
`rcabench`, preserving raw-only, label-free, cross-system deployability and
avoiding CERA / EvidenceRank scoring logic or manual priors.

## Version

- Latest completed CREST iteration: `CREST17`.
- New version for this round: `CREST18`.
- Baseline for comparison: `CREST17_ACCEPTED`.

## Baseline

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST17_ACCEPTED / `crest` | 1422 | 0 | 0.825598 | 0.888980 | 0.945148 | 0.971871 |

## Failure Mechanism

CREST17 safely recovered path/fan-in near ties, but the remaining weak groups
still include pod-failure, low-observability roots, and cases where the root is
not a near-tie path owner. These misses are likely not solved by broadening
protocol/path drift. Many involve a true root with low or missing local traffic
that is outranked by high-observability callers, entry services, or downstream
symptom surfaces.

## Hypothesis

Use weak-root availability/drop evidence only when it is structurally
explanatory:

```text
A candidate may challenge top-1 only if it is already close enough in the
ranking, has stronger local availability/drop evidence than the winner, and
its neighbors carry propagation or observability symptoms that the candidate's
drop can explain.
```

This differs from rejected residual experiments:

- no free bonus for quiet nodes;
- no global residual rerank;
- no service, datapack, or fault-name rules;
- labels only for offline scoring;
- runtime, if implemented, uses raw metrics/traces/logs and CREST-owned
  topology/evidence roles only.

## Offline Analysis Plan

Rebuild candidate-level CREST17 features and profile remaining misses by
accepted rank, fault group, and root-victim feature contrast. Evaluate only
gated variants that combine:

- top-k near-tie restriction;
- candidate drop / availability evidence;
- winner propagation or observability burden;
- local neighbor explainability or fan-in/fan-out context;
- no broad scalar protocol rerank.

Implement a runtime ablation only if the offline mechanism improves AC@1 or MRR
over CREST17 with small, explainable regressions and a coherent weak-root
mechanism.

## Acceptance Criteria

- `guard` reports no high-risk overfitting warnings.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: improves AC@1 or MRR over CREST17 with no
  unexplained AC@3/AC@5 regression and a coherent weak-root mechanism.
- Reject if the candidate becomes another residual/quiet-node bonus or a
  label-shaped top-k rerank.
