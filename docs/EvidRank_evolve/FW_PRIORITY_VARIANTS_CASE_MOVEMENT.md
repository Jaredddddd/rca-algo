# EvidenceRank Priority Variants And Case Movement

- Created: 2026-06-04
- Related experiment: `FW_PRIORITY_COMPREHENSIVE_SEARCH`
- Artifact directory: `output/rcabench-platform-v2/evolve_reweights/FW_PRIORITY_COMPREHENSIVE_SEARCH/`
- Main CSVs:
  - `assignment_ladder_preset_results.csv`
  - `key_candidate_cases.csv`
  - `key_candidate_case_deltas.csv`
  - `key_candidate_delta_summary.csv`

## Purpose

This note explains what "case movement versus baseline" means, what each priority/ladder variant represents, and whether `greedy priorities + clean ladder` should become the default EvidenceRank configuration.

Short answer:

```text
`greedy priorities + clean ladder` has fewer special-looking numeric constants,
but it has stronger label-guided priority-fitting traces.
It should not replace the default algorithm as-is.
```

## Baseline

The baseline in the movement table is:

```text
current FEATURE_PRIORITIES
+ current synthesized priority ladder
0,0.75,1,1.25,1.5,6,10,16
```

Metrics:

| AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: |
| 0.800985 | 0.874517 | 0.942335 | 0.975387 |

This is the accepted `FW_PRIORITY_SYNTH_LADDER` behavior.

## Movement Types

For each case, the offline report compares the best ground-truth service rank under the old baseline and under a candidate variant.

Let:

```text
old_rank = best rank of any GT service under baseline
new_rank = best rank of any GT service under candidate
```

Then each case is assigned exactly one movement type.

| movement type | meaning | example |
| --- | --- | --- |
| `improved_to_hit1` | Baseline was not top-1, candidate becomes top-1. | old_rank=3, new_rank=1 |
| `regressed_from_hit1` | Baseline was top-1, candidate is no longer top-1. | old_rank=1, new_rank=2 |
| `rank_improved` | Candidate improves GT rank but does not newly become hit@1. | old_rank=7, new_rank=3 |
| `rank_regressed` | Candidate worsens GT rank but does not fall from hit@1. | old_rank=3, new_rank=6 |
| `unchanged` | No meaningful rank category change in this comparison. | old_rank=2, new_rank=2 |

Important:

```text
AC@1 delta is controlled by improved_to_hit1 - regressed_from_hit1.
MRR/AC@3/AC@5 also depend on rank_improved and rank_regressed.
```

For 1422 cases, one top-1 case is:

```text
1 / 1422 = 0.000703 AC@1
```

So a net gain of 22 top-1 cases corresponds to:

```text
22 / 1422 = 0.015471 AC@1
```

## Compared Variants

### `disable_trace_duration_z`

Definition:

```text
trace_duration_z: BASELINE -> DISABLED
ladder: 0,0.75,1,1.25,1.5,6,10,16
```

Interpretation:

```text
Remove raw global trace-duration extremeness as a direct root-cause feature.
Keep other latency signals such as trace_duration_delta and trace_self_duration_relative_shift.
```

Metrics:

| AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: |
| 0.816456 | 0.884112 | 0.945851 | 0.976793 |

Movement:

| improved_to_hit1 | regressed_from_hit1 | net top-1 | rank_improved | rank_regressed | unchanged |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 37 | 15 | +22 | 23 | 7 | 1340 |

This is the cleanest mechanism-level candidate because it changes one feature and has a clear RCA explanation: global latency z-score often marks propagation victims.

### `greedy priorities + current ladder`

Definition:

```text
trace_duration_z: BASELINE -> DISABLED
topology_in_degree: DISABLED -> SUPPORT
log_count_delta: BACKGROUND -> LOCAL
trace_count_delta: BASELINE -> BACKGROUND
log_error_rate: BACKGROUND -> LOCAL
metric_count_drop_shift: ROOT -> HIGH

ladder: 0,0.75,1,1.25,1.5,6,10,16
```

Metrics:

| AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: |
| 0.830520 | 0.892995 | 0.947961 | 0.976793 |

Movement:

| improved_to_hit1 | regressed_from_hit1 | net top-1 | rank_improved | rank_regressed | unchanged |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 61 | 19 | +42 | 54 | 31 | 1257 |

This has strong offline performance but the priority assignment is label-guided. It is useful as an upper-bound and hypothesis generator, not as an immediate default.

### `greedy priorities + best ladder`

Definition:

```text
same greedy priorities as above

ladder: 0,0.75,1,1.25,2,6,10,20
LOCAL: 1.5 -> 2
CRITICAL: 16 -> 20
```

Metrics:

| AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: |
| 0.839662 | 0.898061 | 0.950070 | 0.974684 |

Movement:

| improved_to_hit1 | regressed_from_hit1 | net top-1 | rank_improved | rank_regressed | unchanged |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 68 | 13 | +55 | 55 | 30 | 1256 |

This is the best offline replay result, but it has the most label-guided calibration traces because both priorities and ladder values were selected by metric feedback.

### `greedy priorities + clean ladder`

Definition:

```text
same greedy priorities as above

ladder: 0,1,1,1,2,5,10,15
```

Metrics:

| AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: |
| 0.816456 | 0.884331 | 0.944444 | 0.974684 |

Movement:

| improved_to_hit1 | regressed_from_hit1 | net top-1 | rank_improved | rank_regressed | unchanged |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 67 | 45 | +22 | 43 | 47 | 1220 |

This variant has the same net top-1 gain as `disable_trace_duration_z`, but much higher churn:

```text
disable_trace_duration_z:
  improved_to_hit1=37, regressed_from_hit1=15

greedy priorities + clean ladder:
  improved_to_hit1=67, regressed_from_hit1=45
```

So it gets to the same AC@1 gain by moving many more cases around. That is a warning sign for transferability.

## Is `greedy priorities + clean ladder` Least Hand-Designed?

It depends on what "hand-designed" means.

### Fewer explicit numeric constants

Yes.

The clean ladder:

```text
0,1,1,1,2,5,10,15
```

looks less special than:

```text
0,0.75,1,1.25,1.5,6,10,16
```

or:

```text
0,0.75,1,1.25,2,6,10,20
```

If the only concern is "do the numeric constants look hand-tuned?", then `greedy priorities + clean ladder` looks better.

### Fewer data-fitting traces

No.

The priorities in this variant are:

```text
trace_duration_z -> DISABLED
topology_in_degree -> SUPPORT
log_count_delta -> LOCAL
trace_count_delta -> BACKGROUND
log_error_rate -> LOCAL
metric_count_drop_shift -> HIGH
```

These were not derived from an unsupervised mechanism in this experiment. They were selected by label-guided greedy search on RCABench. That is a stronger data-fitting trace than the current synthesized ladder formula.

### More stable case movement

No.

Compared with `disable_trace_duration_z`, it has the same net top-1 gain but three times as many regressions from hit@1:

```text
15 regressions for disable_trace_duration_z
45 regressions for greedy priorities + clean ladder
```

It also has worse AC@3 and AC@5 than `disable_trace_duration_z`:

| variant | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| disable `trace_duration_z` | 0.816456 | 0.884112 | 0.945851 | 0.976793 |
| greedy priorities + clean ladder | 0.816456 | 0.884331 | 0.944444 | 0.974684 |

The clean ladder variant has slightly higher MRR, but it loses on AC@3/AC@5 and has much more churn.

## Recommendation

Do not change the default algorithm to `greedy priorities + clean ladder` as-is.

Reason:

```text
It reduces visible numeric calibration, but increases hidden label-guided priority fitting.
It is less stable than the one-feature `trace_duration_z` removal candidate.
```

If we want a lower-handcraft next step, the better direction is not to paste the greedy priorities into code. It is to convert the strongest discovered mechanism into an unsupervised rule:

```text
Gate or suppress trace_duration_z unless it agrees with local self-duration,
endpoint/status mutation, log corroboration, or topology-direction contrast.
```

If a minimal priority-only candidate must be full-evaluated next, the safer one is:

```text
trace_duration_z: BASELINE -> DISABLED
keep the current synthesized ladder
```

because it is simpler, has the same net AC@1 gain as `greedy priorities + clean ladder`, has fewer hit@1 regressions, and has a clearer RCA mechanism.

## Paper Wording

Defensible:

```text
We use ordinal diagnostic priorities and synthesize a nonlinear severity ladder.
The comprehensive search shows that priority ordering contains useful diagnostic information,
but direct clean monotonic numeric ladders are not equivalent under a linear evidence sum.
```

Not defensible:

```text
The exact numbers do not matter at all.
```

More precise:

```text
The exact numbers are not the public prior interface, but the scorer still needs nonlinear tier separation
or an alternative normalization/fusion mechanism to avoid propagation features dominating root-specific evidence.
```
