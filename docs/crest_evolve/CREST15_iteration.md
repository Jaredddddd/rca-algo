# CREST15 Iteration

## Goal

Continue toward `AC@1 >= 0.85` for `crest` on `rcabench` while preserving
raw-only, label-free, cross-system deployability and avoiding CERA /
EvidenceRank scoring logic or manual priors.

## Version

- Latest completed CREST iteration: `CREST14`.
- New version for this round: `CREST15`.
- Baseline for comparison: `CREST14_DEFAULT` and the positive
  `CREST14_MUTATION_ARBITRATION` ablation.

## Baseline

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST14_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |
| CREST14_MUTATION_ARBITRATION / `crest_mutation_arbitration` | 1422 | 0 | 0.803094 | 0.876849 | 0.944444 | 0.971871 |

## Failure Mechanism

CREST14 proves that strict top-3 arbitration can be safe, but it only fixes 4
top-1 misses. The gate is too local: it asks whether one challenger has stronger
trace mutation and lower propagation than the current winner, but it does not
ask whether the challenger explains a broader cluster of symptoms.

The remaining opportunity is large because default `crest` still has 205
top-1 misses whose ground truth appears in top-3.

## Hypothesis

Use cluster-local explanation eligibility:

```text
A candidate can challenge the top-1 only if it is already in the default top-k
and its mutation evidence can explain multiple nearby high-propagation symptom
surfaces with consistent direction.
```

This preserves the CREST14 discipline:

- no global rerank;
- no additive free bonus for quiet nodes;
- no service, datapack, or fault-name rule;
- labels only for offline scoring;
- runtime, if implemented, uses raw trace topology and CREST-owned role-family
  burdens only.

## Offline Analysis Plan

Reconstruct candidate-level CREST role-family burdens and trace topology for
all default cases. Evaluate label-free cluster signals such as:

- number of adjacent or reachable neighbors whose propagation burden exceeds
  the candidate's propagation burden;
- aggregate explainable propagation mass around the candidate;
- whether the current winner is one of those high-propagation symptom surfaces;
- near-tie gating against the default top-1;
- top-k restriction before any top-1 swap.

Implement a runtime ablation only if the offline mechanism improves AC@1 or MRR
over CREST14 while keeping regressions small and explainable.

## Verification Plan

If an offline formula is positive:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a <crest15_ablation> -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

Then snapshot, summarize, compare, mirror docs into `docs/crest_evolve/`, and
refresh the VibeResearch index.

## Acceptance Criteria

- `guard` reports no high-risk overfitting warnings.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: improves AC@1 or MRR over CREST14 without
  unexplained AC@3/AC@5 regression and with a coherent root-victim explanation.
- Reject if the cluster signal becomes a broad topology centrality score or a
  disguised service/fault-specific rule.

## Offline Results

Analysis artifacts:

- `output/rcabench-platform-v2/evolve_reports/CREST15_cluster_offline_candidates.csv`
- `output/rcabench-platform-v2/evolve_reports/CREST15_cluster_offline_summary.csv`

Best high-gain offline variants:

| formula | AC@1 | improved_to_hit1 | regressed_from_hit1 | switches | net_hit1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| default | 0.800281 | 0 | 0 | 0 | 0 |
| top5_score0.98_n2_15_12_count2 | 0.818565 | 46 | 20 | 94 | +26 |
| top5_score0.97_in_12_12_count2 | 0.811533 | 16 | 0 | 18 | +16 |
| cluster_then_mutation | 0.812940 | 18 | 0 | 22 | +18 |

The highest net formulas used two-hop neighborhoods and regressed many default
hit@1 cases. The accepted candidate is stricter:

```text
top-5 near-tie challenger + at least two incoming caller symptoms explained +
CREST14 mutation arbitration as fallback
```

The accepted mechanism is not a graph centrality score. It only promotes a
candidate that is already near the default winner and has stronger trace
mutation than at least two incoming callers whose propagation burden is higher.

## Full Eval Results

Commands run:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_cluster_arbitration -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST15_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST15_CLUSTER_ARBITRATION --algorithm crest_cluster_arbitration --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST15_DEFAULT --source CREST15_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST15_CLUSTER_ARBITRATION --source CREST15_CLUSTER_ARBITRATION --algorithm crest_cluster_arbitration --dataset rcabench
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST15_ACCEPTED --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST15_ACCEPTED --source CREST15_ACCEPTED --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST15_DEFAULT --new CREST15_ACCEPTED --algorithm crest --dataset rcabench
```

`guard` reported no high-risk overfitting warnings. Compile passed.

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST15_DEFAULT / old `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 9.113438s |
| CREST15_CLUSTER_ARBITRATION / ablation | 1422 | 0 | 0.812940 | 0.882065 | 0.945148 | 0.971871 | 9.134214s |
| CREST15_ACCEPTED / promoted `crest` | 1422 | 0 | 0.812940 | 0.882065 | 0.945148 | 0.971871 | 9.211219s |

Compare against the old default:

| status | cases |
| --- | ---: |
| improved_to_hit1 | 18 |
| regressed_from_hit1 | 0 |
| rank_improved | 18 |
| rank_regressed | 0 |

## Decision

Accept CREST15 and promote the cluster arbitration mechanism into default
`crest`. The goal is still not complete because the verified default is
`AC@1=0.812940`, below the target `AC@1 >= 0.85`.

The accepted mechanism is:

- top-5 near-tie gating against the current winner;
- incoming caller symptom cluster: at least two callers have higher propagation
  burden while the candidate has stronger trace mutation;
- CREST14 mutation arbitration fallback for the small set of single-pair
  protocol mutation rescues.

This preserves the lesson from CREST8-CREST14: do not globally rerank by raw
symptom strength; only change top-1 when a near candidate explains local symptom
surfaces with role-consistent evidence.

## Next Step

CREST16 should target the remaining top-3 misses without broadening into
two-hop rerank. A promising direction is endpoint/protocol mutation ownership
inside the same incoming-caller cluster: require the candidate's server-side
protocol drift to coincide with multiple caller propagation symptoms, instead
of using protocol drift as a standalone rerank signal.
