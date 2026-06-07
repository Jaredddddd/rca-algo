# CREST16 Iteration

## Goal

Continue from accepted CREST15 default toward `AC@1 >= 0.85` for `crest` on
`rcabench`, while preserving raw-only, label-free, cross-system deployability
and avoiding CERA / EvidenceRank scoring logic or manual priors.

## Version

- Latest completed CREST iteration: `CREST15`.
- New version for this round: `CREST16`.
- Baseline for comparison: `CREST15_ACCEPTED`.

## Baseline

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST15_ACCEPTED / `crest` | 1422 | 0 | 0.812940 | 0.882065 | 0.945148 | 0.971871 |

## Failure Mechanism

CREST13 showed that server-side protocol drift alone is too broad: it often
marks symptom surfaces and regresses many correct cases. CREST15 showed that
incoming caller symptom clusters are a safe eligibility gate, but many protocol
mutation misses remain below top-1.

## Hypothesis

Use server-side protocol ownership only inside strict CREST15-style eligibility:

```text
A protocol-drift challenger may alter top-1 only if it is already near the
default ranking and is supported by local caller-symptom explainability.
```

This differs from CREST13:

- no standalone protocol rerank;
- no two-hop topology expansion;
- no service, datapack, or fault-name rules;
- labels only for offline scoring;
- runtime, if implemented, uses raw traces and CREST-owned ranking state only.

## Offline Analysis Plan

Compute per-service server-span protocol drift from raw normal/abnormal traces:

- server span name drift;
- request method drift;
- response status drift;
- span status drift.

Evaluate only gated variants that combine protocol drift with current top-k
near-tie and incoming caller symptom evidence. Implement a runtime ablation only
if the offline mechanism improves over `CREST15_ACCEPTED` with small,
explainable regressions.

## Acceptance Criteria

- `guard` reports no high-risk overfitting warnings.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: improves AC@1 or MRR over CREST15 without
  unexplained AC@3/AC@5 regression and with a coherent mechanism.
- Reject if the protocol signal behaves like CREST13's broad symptom-surface
  rerank.

## Offline Results

Analysis artifacts:

- `output/rcabench-platform-v2/evolve_reports/CREST16_protocol_cluster_offline_candidates.csv`
- `output/rcabench-platform-v2/evolve_reports/CREST16_protocol_cluster_offline_summary.csv`

Top offline variants:

| formula | AC@1 | improved_to_hit1 | regressed_from_hit1 | switches | net_hit1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| CREST15_ACCEPTED baseline | 0.812940 | 0 | 0 | 0 | 0 |
| top5_score0.95_server_status_protocol_r1.05_in1 | 0.820675 | 18 | 7 | 37 | +11 |
| top5_score0.95_server_protocol_r1.05_in1 | 0.819972 | 17 | 7 | 33 | +10 |
| top3_score0.98_server_protocol_r1.05_in1 | 0.818565 | 10 | 2 | 17 | +8 |
| top5_score0.93_server_status_protocol_r1.05_in2 | 0.815049 | 3 | 0 | 3 | +3 |

The protocol signal remains noisy even when gated by incoming caller symptom
evidence. The high-gain formulas still regress multiple accepted hit@1 cases.
The zero-regression formulas add only 3 hit@1 cases, which is too small to
justify a new runtime protocol-drift module at this stage.

## Decision

Reject CREST16 as a runtime change. Keep CREST15 as the accepted default.

The negative result refines the CREST13 lesson: protocol drift should not be
introduced as another arbitration signal unless the eligibility predicate can
distinguish root-owned protocol mutation from symptom-surface protocol drift
more sharply than incoming caller count alone.

## Next Step

CREST17 should avoid adding another scalar protocol gate. A better direction is
to inspect remaining accepted-default misses by structural pattern and look for
one new raw mechanism that can recover more than a handful of cases without
regressing accepted hit@1 cases, such as request-path-consistent caller clusters
or multi-root preservation.
