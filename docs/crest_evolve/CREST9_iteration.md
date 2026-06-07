# CREST9 Iteration

## Goal

Continue toward `AC@1 >= 0.85` for `crest` on `rcabench` while preserving the
CREST constraints: raw-only, label-free runtime, no CERA / EvidenceRank scoring
logic, no CERA / EvidenceRank manual priors, and no datapack/service/fault
hardcoding.

## Version

- Latest completed CREST iteration: `CREST8`.
- New version for this round: `CREST9`.
- Baseline for comparison: `CREST8_DEFAULT` / `CREST7_BASELINE`.

## Constraints

- Runtime CREST may read only raw normal/abnormal metric, trace, and log frames
  under `args.input_folder`.
- Runtime CREST must not read labels, injection metadata, previous outputs, perf
  reports, historical rankings, ground truth, or `conclusion.parquet`.
- Do not inspect or borrow CERA / EvidenceRank scoring logic or hand-written
  feature priors.
- Labels and reports may be used only offline to understand failure patterns and
  evaluate versions.
- Any accepted change must be explainable as a cross-system RCA mechanism.

## Baseline

Verified default before this round:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST8_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

CREST8 residual negative control:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST8_RESIDUAL / `crest_residual` | 1422 | 0 | 0.340366 | 0.439628 | 0.447257 | 0.530942 |

## Failure Mechanism From CREST8

CREST8 residual had rescue signal but no confidence boundary:

- It improved 45 baseline misses to hit@1.
- It regressed 699 previous hit@1 cases.
- Most catastrophic cases promoted symptom-light auxiliary services,
  load-generators, or quiet metric-drift bystanders that were not competitive in
  the default CREST ranking.

This means residual support should not be allowed to discover arbitrary deep
candidates. It should only arbitrate among candidates that default CREST already
considers plausible.

## Hypothesis

Use residual support only as a gated local reranker:

```text
R is eligible only for candidates inside the default CREST competitive set.
```

The default CREST score already captures robust evidence and counterfactual
structural support. If a residual candidate is not near the default top
candidate, the residual signal is more likely to be a quiet-bystander artifact
than a weak root. If it is already near the top, residual may safely decide
between a high-observability victim and a nearby weak root.

The first gate to test is rank-statistical and label-free:

- compute the no-residual CREST ranking;
- compute residual support from raw role matrix;
- let residual affect only the top `K` no-residual candidates, where `K` is a
  small algorithmic stability parameter;
- keep all other candidates on the no-residual score.

This does not use labels at runtime and does not use service/fault names. It
also does not copy CERA/EvidenceRank priors.

## Planned Change

Add a CREST-owned gated residual mode:

- either as `crest_gated_residual`, or as a replacement for rejected
  `crest_residual` if full eval supports it;
- default `crest` changes only if full eval improves `AC@1` or `MRR` without
  unexplained `AC@3`/`AC@5` regression.

Implementation should remain local to:

- `algorithms/evidencerank/src/evidencerank/crest.py`;
- `algorithms/evidencerank/src/evidencerank/crest_residual.py`;
- `algorithms/evidencerank/main.py`.

## Offline Analysis Plan

Before editing runtime code, use existing CREST8 snapshots/reports to estimate
how much of residual's 45 rescues and 699 regressions would survive a default
rank gate such as top-2, top-3, or top-5. This analysis may use labels only to
count rescues/regressions.

The gate is acceptable to implement only if it sharply reduces regressions while
retaining a meaningful share of residual rescues.

## Offline Findings

The first report-only gate confirmed that a default-rank window alone is too
weak:

| gate | residual switches | rescues | regressions | net |
| --- | ---: | ---: | ---: | ---: |
| default top-2 only | 139 | 30 | 80 | -50 |
| default top-3 only | 243 | 36 | 151 | -115 |
| default top-5 only | 321 | 39 | 243 | -204 |

I then reconstructed raw CREST score geometry for the 139 top-2 switch cases and
wrote the analysis table to
`output/rcabench-platform-v2/evolve_reports/CREST9_top2_switch_features.csv`.
The useful distinction was not just rank:

- Good switches are much closer default-score ties: median old score ratio
  `0.9880` versus `0.9656` for bad switches.
- Good switches usually have residual support on both the default winner and
  the residual challenger: median `R_base=1.1520` versus `0.2219` for bad
  switches.
- Bad switches often come from an overwhelming one-sided residual jump:
  median `R_adv=1.6316` versus `0.7208` for good switches.

This supports a narrower mechanism:

```text
Residual may arbitrate only between the default top two candidates, only for a
near-tie, and only when the challenger's residual support is comparable to the
default winner's residual support.
```

This keeps the mechanism label-free at runtime and avoids service/fault rules.
It also changes the interpretation from "let residual discover a quiet deep
candidate" to "let residual break an already plausible CREST tie when both
candidates have explainability support."

The implemented ablation should therefore be named `crest_gated_residual`, keep
default `crest` unchanged, and use only incident-local score relationships:

- default top-2 candidate set;
- near-tie ratio on the no-residual CREST score;
- two-sided residual corroboration, where the challenger residual must not
  dwarf the default winner residual.

## Verification Plan

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_gated_residual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST9 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST9 --source CREST9 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST8_DEFAULT --new CREST9 --algorithm crest --dataset rcabench
```

If the gated residual is only an ablation, snapshot/summarize it under a
distinct version such as `CREST9_GATED_RESIDUAL`.

## Implementation

Added `crest_gated_residual` as an ablation only:

- `algorithms/evidencerank/src/evidencerank/crest.py`
  - added `CRESTGatedResidual`;
  - added a top-two residual arbitration gate;
  - left default `CREST._use_residual = False`.
- `algorithms/evidencerank/main.py`
  - registered `crest_gated_residual`.

The gate is intentionally narrow:

1. Compute the normal no-residual CREST score.
2. Consider only the default top two candidates.
3. Require the runner-up to be a near-tie on no-residual score.
4. Require residual to favor the runner-up, but not by a one-sided jump that
   dwarfs the default winner's residual support.
5. If eligible, add residual support only to the default top two; all deeper
   candidates receive zero residual support.

This keeps the ablation raw-only and label-free at runtime. It does not read
labels, injection metadata, outputs, perf reports, or `conclusion.parquet`.

## Verification Results

Commands run:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_gated_residual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST9_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST9_GATED_RESIDUAL --algorithm crest_gated_residual --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST9_DEFAULT --source CREST9_DEFAULT --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST9_GATED_RESIDUAL --source CREST9_GATED_RESIDUAL --algorithm crest_gated_residual --dataset rcabench
```

Guard result: no high-risk overfitting warnings. The only guard messages were
pre-existing medium `rcabench_platform` import/literal warnings.

Compile result: passed.

Full eval result:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST9_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |
| CREST9_GATED_RESIDUAL / `crest_gated_residual` | 1422 | 0 | 0.797468 | 0.873919 | 0.944444 | 0.971871 |

Custom cross-algorithm compare:

- [compare_CREST9_DEFAULT_vs_CREST9_GATED_RESIDUAL.md](compare_CREST9_DEFAULT_vs_CREST9_GATED_RESIDUAL.md)
- `improved_to_hit1`: 11
- `regressed_from_hit1`: 15
- net AC@1 count change: -4

## Decision

Reject `crest_gated_residual` as a default change.

The gate successfully prevents the catastrophic CREST8 residual failure, but it
does not create a reliable positive ranking signal. It rescues some weak-root
and co-failure cases, yet still flips already-correct protocol mutation cases
to adjacent high-explainability services. The residual channel remains useful as
offline diagnostic evidence, but not as an additive score component.

Default `crest` remains the no-residual CREST path.

## Next Step

Do not keep tightening scalar residual thresholds. The next CREST attempt should
turn residual into a contrast or suppression signal:

```text
Use residual only to explain why a high-observability victim should be
suppressed when an adjacent candidate already has stronger raw mutation evidence.
```

That is different from adding residual support to a challenger. It should be
implemented as a local pairwise victim-suppression ablation, with the base CREST
score preserved unless a neighbor can explain the victim's propagated symptoms.

## Acceptance Criteria

- `guard` reports no high-risk overfitting warnings.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: `AC@1` or `MRR` improves over `CREST8_DEFAULT`,
  `AC@3` and `AC@5` do not show unexplained large regressions, and compare docs
  show a coherent rescue/regression mechanism.
- Reject if the gate merely hides the CREST8 failure without improving default
  CREST.
