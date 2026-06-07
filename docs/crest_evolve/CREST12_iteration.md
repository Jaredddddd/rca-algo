# CREST12 Iteration

## Goal

Continue toward `AC@1 >= 0.85` for `crest` on `rcabench` while preserving
raw-only, label-free, cross-system deployability and avoiding CERA /
EvidenceRank scoring logic or manual priors.

## Version

- Latest completed CREST iteration: `CREST11`.
- New version for this round: `CREST12`.
- Baseline for comparison: `CREST10_DEFAULT` / `CREST11 offline default`.

## Baseline

Verified default:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST10_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

CREST11 offline stability fusion over `A`, `F`, and `S` did not improve AC@1
or MRR, so no `crest_stability_fusion` runtime ablation was implemented.

## Hypothesis

The current `A/F/S` compression may hide useful root-victim distinctions. A
root and a victim can both look strong after aggregation, but their family
profiles differ:

- roots should retain local mutation or local fault evidence;
- victims often have strong trace propagation, observability volume, or broad
  structural support;
- logs can be root-local in some incidents and propagated in others, so they
  should be treated as an independent family rather than a fixed bonus.

CREST12 tests whether a manual-weight-free family-level rank aggregation can
improve top-1:

```text
Rank candidates by stability across root-evidence families and default CREST
confidence, while avoiding direct residual bonuses or broad victim penalties.
```

This differs from CREST11 because it uses role-family burdens before `A/F/S`
compression rather than re-ranking only the compressed outputs.

## Offline Analysis Plan

Reconstruct CREST raw feature matrices for all `CREST10_DEFAULT` cases and
compute incident-local family signals:

- `metric_shift`
- `trace_mutation`
- `trace_propagation`
- `log_shift`
- `observability_volume`
- `topology_context`
- derived root families such as mutation/root-purity/cross-family support

Evaluate unweighted, label-free formulas such as:

- root-family reciprocal-rank fusion;
- root-family median rank;
- default-top-k reranking by family stability;
- root-purity gated family rank fusion.

Labels may be used only offline to count hit@1/MRR and compare regressions.
Implement a runtime ablation only if a simple family-level mechanism improves
AC@1 or MRR in offline reconstruction.

## Offline Results

Reconstructed CREST role-family burdens for all 1422 `CREST10_DEFAULT` cases.
Analysis artifacts:

- `output/rcabench-platform-v2/evolve_reports/CREST12_family_offline_scores.csv`
- `output/rcabench-platform-v2/evolve_reports/CREST12_family_offline_summary.csv`

Summary:

| formula | AC@1 | MRR | AC@3 | AC@5 | improved_to_hit1 | regressed_from_hit1 | net_hit1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| default_score | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 0 | 0 | 0 |
| default_rootS_rrf | 0.774262 | 0.853941 | 0.924051 | 0.954993 | 28 | 65 | -37 |
| default_root_rrf | 0.715893 | 0.821714 | 0.909283 | 0.954993 | 40 | 160 | -120 |
| top3_root_sum_purity | 0.617440 | 0.762319 | 0.944444 | 0.967651 | 64 | 324 | -260 |
| root_sum | 0.613221 | 0.739171 | 0.829817 | 0.924754 | 56 | 322 | -266 |
| root_family_rrf | 0.502813 | 0.666082 | 0.767932 | 0.905767 | 69 | 492 | -423 |
| mutation_sum | 0.494374 | 0.646378 | 0.741913 | 0.870605 | 38 | 473 | -435 |
| root_purity | 0.047117 | 0.138446 | 0.086498 | 0.137131 | 13 | 1084 | -1071 |

Family-level root evidence alone is far too noisy. It does contain rescue
signal, but it destroys many already-correct rankings. This supports the CREST10
lesson: eligibility cannot be derived from broad family aggregation alone.

## Decision

Do not implement `crest_family_fusion`.

The next useful direction should stop trying to re-aggregate existing service
scores and instead create a more specific raw signal for one large failure
class. The strongest candidate is trace protocol mutation ownership: identify
which service first introduces new or shifted status/path/method/endpoint
behavior in abnormal traces, using only raw trace structure.

## Planned Implementation

If supported, add a `crest_family_fusion` ablation only. Default `crest` must
remain unchanged unless full eval proves improvement.

Likely local files:

- `algorithms/evidencerank/src/evidencerank/crest.py`
- `algorithms/evidencerank/main.py`

The runtime path must not read labels, injection metadata, previous outputs,
perf reports, historical rankings, or `conclusion.parquet`.

## Acceptance Criteria

- Offline reconstruction shows a simple, explainable family-level mechanism with
  positive AC@1 or MRR delta versus default.
- `guard` reports no high-risk overfitting warnings before full eval.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: `AC@1` or `MRR` improves over baseline and AC@3/AC@5
  do not show unexplained large regression.
