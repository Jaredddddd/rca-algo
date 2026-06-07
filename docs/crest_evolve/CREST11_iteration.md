# CREST11 Iteration

## Goal

Continue toward `AC@1 >= 0.85` for `crest` on `rcabench` while keeping runtime
CREST raw-only, label-free, cross-system explainable, and independent of CERA /
EvidenceRank scoring logic or hand-written priors.

## Version

- Latest completed CREST iteration: `CREST10`.
- New version for this round: `CREST11`.
- Baseline for comparison: `CREST10_DEFAULT` / `CREST9_DEFAULT`.

## Baseline

Verified default before this round:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST10_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

Recent rejected ablations:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST9_GATED_RESIDUAL / `crest_gated_residual` | 1422 | 0 | 0.797468 | 0.873919 | 0.944444 | 0.971871 |
| CREST10_VICTIM_SUPPRESSION / `crest_victim_suppression` | 1422 | 0 | 0.757384 | 0.841618 | 0.917018 | 0.950070 |

## Failure Mechanism

CREST8-CREST10 show that direct score mutation is fragile:

- additive residual is too easy to turn into a quiet-node bonus;
- gated residual is safer but still regresses more hit@1 cases than it rescues;
- broad pairwise victim suppression removes score from too many already-correct
  roots.

The shared weakness is insufficient eligibility before changing top-1. CREST
needs a label-free confidence model that says when an alternative candidate is
stable across raw evidence views, not just when one extra signal likes it.

## Hypothesis

Use bootstrap/rank-stability fusion over CREST-owned evidence views:

```text
A candidate is eligible to challenge the default winner only when it is stable
across multiple raw CREST views of the same incident.
```

The views are not CERA/EvidenceRank priors. They are CREST's existing runtime
signals:

- `A`: local abnormality;
- `F`: counterfactual explanatory power;
- `S`: denoised structural support;
- simple unweighted combinations such as `A*F`, `A+S`, `F+S`, and `A+F+S`.

The candidate ranking can use rank statistics such as median rank, reciprocal
rank sum, or Pareto front depth rather than feature weights. This is a
manual-weight-free eligibility layer: it asks whether a candidate is repeatedly
near the top under perturbations of the same raw evidence, and it avoids
changing scores via residual bonus or broad suppression.

## Offline Analysis Plan

Before editing runtime code, reconstruct `score_crest_services` for all
`CREST10_DEFAULT` cases and evaluate label-free rank-stability formulas against
offline labels:

1. Keep labels only in the analysis script to count hit@1/MRR.
2. Compare default `A*F+S` with unweighted rank-fusion variants.
3. Measure especially:
   - total AC@1/MRR;
   - `improved_to_hit1`;
   - `regressed_from_hit1`;
   - whether gains come from top-3/top-5 default misses.
4. Implement a `crest_stability_fusion` ablation only if one simple mechanism
   improves AC@1 or MRR in offline reconstruction without relying on
   case/service/fault names.

## Offline Results

Reconstructed `score_crest_services` for all 1422 `CREST10_DEFAULT` cases and
evaluated unweighted rank-stability formulas. Analysis artifacts:

- `output/rcabench-platform-v2/evolve_reports/CREST11_stability_offline_scores.csv`
- `output/rcabench-platform-v2/evolve_reports/CREST11_stability_offline_summary.csv`

Summary:

| formula | AC@1 | MRR | AC@3 | AC@5 | improved_to_hit1 | regressed_from_hit1 | net_hit1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| default_score | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 0 | 0 | 0 |
| A_plus_F_plus_S | 0.800281 | 0.875208 | 0.944444 | 0.971871 | 0 | 0 | 0 |
| top5_rrf_views7 | 0.798875 | 0.874058 | 0.945148 | 0.971871 | 3 | 5 | -2 |
| rrf_views7 | 0.798875 | 0.873869 | 0.945148 | 0.971871 | 3 | 5 | -2 |
| A_plus_S | 0.795359 | 0.873126 | 0.946554 | 0.975387 | 19 | 26 | -7 |
| rrf_default_AFS | 0.792546 | 0.869898 | 0.943741 | 0.970464 | 9 | 20 | -11 |
| AF | 0.774262 | 0.861558 | 0.940928 | 0.974684 | 20 | 57 | -37 |
| rrf_AFS | 0.768636 | 0.856783 | 0.940225 | 0.969761 | 24 | 69 | -45 |

None of the simple rank-stability variants improved AC@1 or MRR. Some variants
improved AC@3/AC@5 slightly, especially `A_plus_S`, but they lost too many
hit@1 cases to justify a runtime ablation.

## Decision

Do not implement `crest_stability_fusion`.

The negative result is useful: the remaining improvement is not recoverable by
blindly re-aggregating the already-compressed `A`, `F`, and `S` views. CREST
needs a more granular eligibility signal before aggregation, likely at the
role-family or feature-family level.

## Next Step

Move to a CREST12 hypothesis: analyze CREST role-family burdens
(`metric_shift`, `trace_mutation`, `trace_propagation`, `log_shift`, and
topology/observability context) before they are compressed into `A`, `F`, and
`S`. The key question is whether a label-free family-level root evidence
profile can distinguish roots from high-observability victims better than
post-hoc rank fusion.

## Planned Implementation

If supported, add `crest_stability_fusion` as an ablation only. Default `crest`
must remain unchanged unless full eval proves improvement.

Likely local files:

- `algorithms/evidencerank/src/evidencerank/crest.py`
- `algorithms/evidencerank/main.py`

The runtime path must not read labels, injection metadata, previous outputs,
perf reports, historical rankings, or `conclusion.parquet`.

## Verification Plan

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_stability_fusion -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST11_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST11_STABILITY_FUSION --algorithm crest_stability_fusion --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST11_DEFAULT --source CREST11_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST11_STABILITY_FUSION --source CREST11_STABILITY_FUSION --algorithm crest_stability_fusion --dataset rcabench
```

Use a custom cross-algorithm compare if needed.

## Acceptance Criteria

- `guard` reports no high-risk overfitting warnings.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: `AC@1` or `MRR` improves over `CREST10_DEFAULT`,
  `AC@3` and `AC@5` do not show unexplained large regressions, and compare docs
  show a coherent rescue/regression mechanism.
- Reject if the fusion is just a label-tuned formula or if it reduces CREST to a
  generic anomaly-rank ensemble without explanatory semantics.
