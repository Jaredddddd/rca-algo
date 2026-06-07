# CREST10 Iteration

## Goal

Continue toward `AC@1 >= 0.85` for `crest` on `rcabench` while preserving
CREST's constraints: raw-only runtime, no labels or injection metadata in the
algorithm path, no CERA / EvidenceRank scoring logic, no CERA / EvidenceRank
manual priors, and no datapack/service/fault hardcoding.

## Version

- Latest completed CREST iteration: `CREST9`.
- New version for this round: `CREST10`.
- Baseline for comparison: `CREST9_DEFAULT` / `CREST8_DEFAULT`.

## Baseline

Verified default before this round:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST9_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

Rejected residual ablations:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST8_RESIDUAL / `crest_residual` | 1422 | 0 | 0.340366 | 0.439628 | 0.447257 | 0.530942 |
| CREST9_GATED_RESIDUAL / `crest_gated_residual` | 1422 | 0 | 0.797468 | 0.873919 | 0.944444 | 0.971871 |

## Failure Mechanism

CREST8 and CREST9 show that residual support has real rescue signal but is not
safe as an additive ranking channel:

- free residual creates many deep quiet-bystander false positives;
- gated residual avoids deep false positives but still flips already-correct
  protocol mutation cases to adjacent services;
- both variants treat residual as a challenger bonus.

The remaining useful mechanism is not "give residual-supported candidates more
score." It is:

```text
If a high-observability service looks like a victim and an adjacent candidate
has stronger local mutation evidence, suppress only the explainable victim
score mass.
```

## Hypothesis

Pairwise victim suppression is safer than additive residual:

1. Keep the default CREST score as the primary ranking.
2. Identify adjacent service pairs from raw trace topology.
3. For a higher-scored service `v`, compute whether it is more propagation-like
   than an adjacent lower-scored candidate `r`.
4. Compute whether `r` has stronger root-mutation evidence than `v`.
5. Only when both contrasts hold, reduce `v` by the explainable portion of its
   score advantage. Do not add that mass to `r`.

This is a CREST-native counterfactual explanation step: it removes symptom mass
from a victim when a neighbor can explain it, but does not manufacture a new
root bonus.

## Planned Change

Add `crest_victim_suppression` as an ablation only. Default `crest` must remain
unchanged unless full eval proves an improvement.

Local implementation targets:

- `algorithms/evidencerank/src/evidencerank/crest.py`
- `algorithms/evidencerank/main.py`

The ablation may reuse existing CREST role families and mutation/propagation
feature sets. It must not read labels, injection metadata, previous outputs,
perf reports, historical rankings, or `conclusion.parquet`.

## Verification Plan

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_victim_suppression -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST10_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST10_VICTIM_SUPPRESSION --algorithm crest_victim_suppression --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST10_DEFAULT --source CREST10_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST10_VICTIM_SUPPRESSION --source CREST10_VICTIM_SUPPRESSION --algorithm crest_victim_suppression --dataset rcabench
```

Use a custom cross-algorithm compare if the built-in compare command cannot
compare `crest` to the ablation registry name.

## Implementation

Added `crest_victim_suppression` as an ablation only:

- `algorithms/evidencerank/src/evidencerank/crest.py`
  - added `CRESTVictimSuppression`;
  - added pairwise final-score suppression for adjacent services when a
    lower-scored neighbor has stronger mutation evidence and the higher-scored
    service has stronger propagation evidence;
  - suppression subtracts from the victim only and does not add score to the
    candidate.
- `algorithms/evidencerank/main.py`
  - registered `crest_victim_suppression`.

Default `crest` remains unchanged.

## Verification Results

Commands run:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_victim_suppression -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST10_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST10_VICTIM_SUPPRESSION --algorithm crest_victim_suppression --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST10_DEFAULT --source CREST10_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST10_VICTIM_SUPPRESSION --source CREST10_VICTIM_SUPPRESSION --algorithm crest_victim_suppression --dataset rcabench
```

Guard result: no high-risk overfitting warnings. The only guard messages were
pre-existing medium `rcabench_platform` import/literal warnings.

Compile result: passed.

Full eval result:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST10_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |
| CREST10_VICTIM_SUPPRESSION / `crest_victim_suppression` | 1422 | 0 | 0.757384 | 0.841618 | 0.917018 | 0.950070 |

Custom cross-algorithm compare:

- [compare_CREST10_DEFAULT_vs_CREST10_VICTIM_SUPPRESSION.md](compare_CREST10_DEFAULT_vs_CREST10_VICTIM_SUPPRESSION.md)
- `improved_to_hit1`: 24
- `regressed_from_hit1`: 85
- `rank_improved`: 41
- `rank_regressed`: 46

## Decision

Reject `crest_victim_suppression` as a default change.

The mechanism was directionally plausible but too broad. It suppressed many
already-correct roots whenever an adjacent service had a mutation/propagation
contrast, which means the final-score operation did not have enough root-victim
eligibility control. The drop in AC@1, MRR, AC@3, and AC@5 is too large to keep
as an intermediate accepted version.

Default `crest` remains the no-residual, no-victim-suppression path.

## Next Step

Do not apply final-score suppression to all adjacent mutation/propagation
contrasts. The next attempt should first learn or derive a stronger
root-victim eligibility predicate without labels, for example:

- require the candidate to explain multiple independent victim symptoms while
  preserving its own default CREST confidence;
- derive incident-local candidate clusters and only rerank within a cluster
  whose members are already mutually competitive;
- use bootstrap stability over raw feature families to decide whether a
  root-victim contrast is stable enough to affect top-1.

## Acceptance Criteria

- `guard` reports no high-risk overfitting warnings.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: `AC@1` or `MRR` improves over `CREST9_DEFAULT`,
  `AC@3` and `AC@5` do not show unexplained large regressions, and compare docs
  show a coherent rescue/regression mechanism.
- Reject if suppression becomes a generic penalty against high-observability
  services rather than an adjacency-conditioned explainability operation.
