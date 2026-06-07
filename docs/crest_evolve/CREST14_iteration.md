# CREST14 Iteration

## Goal

Continue toward `AC@1 >= 0.85` for `crest` on `rcabench` while preserving
raw-only, label-free, cross-system deployability and avoiding CERA /
EvidenceRank scoring logic or manual priors.

## Version

- Latest completed CREST iteration: `CREST13`.
- New version for this round: `CREST14`.
- Baseline for comparison: `CREST10_DEFAULT` / current default `crest`.

## Baseline

Verified default:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST10_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

## Failure Mechanism

CREST's remaining misses are frequently already present in the default top-3:
284 top-1 misses, but only 79 top-3 misses. This means many failures are not
candidate-generation failures; they are arbitration failures between a loud
victim/relay and a nearby root-like candidate.

Rejected CREST11-CREST13 attempts show that broad reranking is unsafe:

- compressed view fusion barely changes rankings;
- family-level fusion is too noisy;
- server protocol drift often marks symptom surfaces rather than roots.

## Hypothesis

Use a narrow, label-free root-victim arbitration rule:

```text
A top-3 challenger may replace the current winner only when it is a near tie,
has much stronger trace mutation burden, and has much lower propagation burden.
```

This is not a feature-weight prior. It is an eligibility predicate for a single
near-tie swap:

- near tie: challenger score is at least 98% of the current winner's score;
- mutation dominance: challenger trace-mutation burden is at least 1.5x the
  current winner's burden;
- propagation contrast: challenger trace-propagation burden is at most 0.5x the
  current winner's burden;
- selection is restricted to the current default top-3.

The constants are stability gates rather than feature weights: they define when
two already-near candidates have a clear role contrast.

## Offline Analysis

Analysis artifacts:

- `output/rcabench-platform-v2/evolve_reports/CREST14_root_victim_offline_candidates.csv`
- `output/rcabench-platform-v2/evolve_reports/CREST14_root_victim_offline_summary.csv`

Best safe offline variant:

| formula | AC@1 | improved_to_hit1 | regressed_from_hit1 | switches | net_hit1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| default | 0.800281 | 0 | 0 | 0 | 0 |
| top3_score0.98_mut1.50_prop0.50 | 0.803094 | 4 | 0 | 6 | +4 |

The larger net variant `top3_score0.97_mut1.50_prop0.50` reached
`AC@1=0.803797`, but it introduced one previous hit@1 regression. CREST14 will
implement the stricter zero-regression offline variant first.

## Planned Implementation

Add a `crest_mutation_arbitration` ablation only. Default `crest` remains
unchanged unless full eval proves the ablation is a safe improvement.

Likely local files:

- `algorithms/evidencerank/src/evidencerank/crest.py`
- `algorithms/evidencerank/main.py`

Runtime must not read labels, injection metadata, previous outputs, perf
reports, historical rankings, or `conclusion.parquet`.

## Verification Plan

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_mutation_arbitration -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST14_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST14_MUTATION_ARBITRATION --algorithm crest_mutation_arbitration --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST14_DEFAULT --source CREST14_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST14_MUTATION_ARBITRATION --source CREST14_MUTATION_ARBITRATION --algorithm crest_mutation_arbitration --dataset rcabench
```

Use a custom cross-algorithm compare if needed because `evidrank_lab.py compare`
assumes one algorithm name.

## Acceptance Criteria

- `guard` reports no high-risk overfitting warnings.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: `AC@1` or `MRR` improves over baseline, no previous
  hit@1 regressions appear in compare, and AC@3/AC@5 do not show unexplained
  large regression.
- Reject if the rule behaves like a broad family reranker rather than a narrow
  role-contrast arbitration.

## Full Eval Results

Commands run:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_mutation_arbitration -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST14_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST14_MUTATION_ARBITRATION --algorithm crest_mutation_arbitration --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST14_DEFAULT --source CREST14_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST14_MUTATION_ARBITRATION --source CREST14_MUTATION_ARBITRATION --algorithm crest_mutation_arbitration --dataset rcabench
```

`guard` reported no high-risk overfitting warnings. Compile passed.

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST14_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 8.903303s |
| CREST14_MUTATION_ARBITRATION / `crest_mutation_arbitration` | 1422 | 0 | 0.803094 | 0.876849 | 0.944444 | 0.971871 | 8.928790s |

Custom compare artifacts:

- `output/rcabench-platform-v2/evolve_reports/compare_CREST14_DEFAULT_vs_CREST14_MUTATION_ARBITRATION/case_deltas.csv`
- `docs/crest_evolve/compare_CREST14_DEFAULT_vs_CREST14_MUTATION_ARBITRATION.md`

Delta summary:

| metric | value |
| --- | ---: |
| improved_to_hit1 | 4 |
| regressed_from_hit1 | 0 |
| top1_changed | 6 |
| rank_improved | 4 |
| rank_regressed | 0 |
| AC@1 delta | +0.002813 |
| MRR delta | +0.001524 |

## Decision

Keep `crest_mutation_arbitration` as a positive CREST-family ablation. Do not
switch default `crest` yet and do not mark the `AC@1 >= 0.85` goal complete.

The result supports a narrower lesson than CREST10: root-victim contrast can be
safe when it is only used to arbitrate already-near top-3 candidates and when
the challenger has a strong trace mutation / low propagation role contrast. The
gain is too small to be the final mechanism, but it is the first safe positive
CREST iteration after several broad negative rerank attempts.

## Next Step

CREST15 should preserve this narrow arbitration discipline but seek a larger
raw-only signal. The best next target is a cluster-local explanation model:
instead of one pairwise top-3 swap, estimate whether a candidate explains
multiple neighboring symptom surfaces with consistent mutation-to-propagation
direction. The candidate should still be near the default top-k and should not
receive a free additive bonus.
