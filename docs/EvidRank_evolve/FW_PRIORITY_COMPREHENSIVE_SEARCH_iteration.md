# EvidenceRank FW_PRIORITY_COMPREHENSIVE_SEARCH Iteration

- Created: 2026-06-04T03:31:04+08:00
- Algorithm line: `evidencerank`
- Dataset: `rcabench`
- Baseline: `FW_PRIORITY_SYNTH_LADDER`
- Hypothesis: 在不改变 EvidenceRank scoring 逻辑的前提下，只搜索 `FEATURE_PRIORITIES` 的 ordinal assignment 和 `FEATURE_PRIORITY_LADDER` 的层级数值，可以估计当前 feature prior 的性能上限、敏感区间和最小可解释候选。

## Safety Boundary

This is an offline label-guided search over cached raw feature matrices. It is not an accepted default algorithm change.

The experiment reads labels only to compute AC@1/MRR/AC@3/AC@5 and case movement. No labels, injections, output rankings, perf reports, historical leaderboard files, datapack-specific rules, service names, or fault names are read by `algorithms/evidencerank`.

Because the search objective uses RCABench labels, the best candidate below must be treated as an upper-bound and sensitivity study. It should not be copied into `algorithm.py` as a default without a separate mechanism-level justification, guard, full eval, snapshot, summary, compare, and regression analysis.

## Artifacts

Output directory:

```text
output/rcabench-platform-v2/evolve_reweights/FW_PRIORITY_COMPREHENSIVE_SEARCH/
```

Core files:

```text
candidate_summary.csv
single_feature_priority_scan.csv
greedy_priority_search.csv
ladder_coordinate_search.csv
targeted_combinations.csv
```

Post-analysis files:

```text
single_feature_priority_ac1_pivot.csv
single_feature_priority_summary.csv
assignment_ladder_preset_results.csv
one_level_ladder_range_scan.csv
one_level_ladder_plateaus.csv
key_candidate_cases.csv
key_candidate_case_deltas.csv
key_candidate_delta_summary.csv
manifest.json
```

Input feature cache:

```text
output/rcabench-platform-v2/evolve_feature_cache/FW_FEATURE_CACHE_BASE/
```

The manifest records `eval_count=1105` for the first comprehensive search and `post_analysis_eval_count=170` for the follow-up preset/range scans.

## Method

The search replays the same cached service-feature matrices used by the accepted synthesized-ladder experiment. The offline scorer preserves the current scoring logic:

- `_heuristic_scores`;
- endpoint support gate;
- adaptive modality reweighting only when it preserves the top-ranked service;
- parent context smoothing.

The baseline priority ladder is:

```text
DISABLED=0, BACKGROUND=0.75, BASELINE=1, SUPPORT=1.25, LOCAL=1.5, HIGH=6, ROOT=10, CRITICAL=16
```

Experiments:

1. Baseline replay of current `FEATURE_PRIORITIES` and synthesized ladder.
2. Single-feature priority reassignment: for each feature, assign it to every `FeaturePriority` tier and replay all cases.
3. Greedy priority coordinate search: repeatedly accept the one priority reassignment that most improves AC@1/MRR.
4. Ladder coordinate search: starting from the best greedy priority assignment, adjust one ladder tier at a time.
5. Targeted combinations around previously observed weak points.
6. Post-analysis preset scan: combine current/modified priority assignments with common ladders such as `0,1,1,1,2,5,10,15`.
7. Post-analysis one-level ladder range scan: fix all but one ladder tier and report AC@1 plateaus.
8. Key candidate case movement: compare baseline hit@1/rank movement against the main candidates.

## Baseline

| config | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| current priorities + synthesized ladder | 0.800985 | 0.874517 | 0.942335 | 0.975387 |

This reproduces the accepted `FW_PRIORITY_SYNTH_LADDER` behavior exactly.

## Best Offline Candidate

The best label-guided replay candidate is:

```text
Priority assignment changes:
trace_duration_z: BASELINE -> DISABLED
topology_in_degree: DISABLED -> SUPPORT
log_count_delta: BACKGROUND -> LOCAL
trace_count_delta: BASELINE -> BACKGROUND
log_error_rate: BACKGROUND -> LOCAL
metric_count_drop_shift: ROOT -> HIGH

Ladder changes:
LOCAL: 1.5 -> 2.0
CRITICAL: 16 -> 20
```

Metrics:

| config | AC@1 | MRR | AC@3 | AC@5 | top5 miss |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.800985 | 0.874517 | 0.942335 | 0.975387 | 35 |
| greedy priorities, current ladder | 0.830520 | 0.892995 | 0.947961 | 0.976793 | 33 |
| greedy priorities, LOCAL=2 and CRITICAL=20 | 0.839662 | 0.898061 | 0.950070 | 0.974684 | 36 |

Headline deltas for the best candidate:

```text
AC@1 +0.038678
MRR  +0.023544
AC@3 +0.007736
AC@5 -0.000703
```

The AC@5 drop is one case and therefore small, but it must still be explained before any accepted default change.

## Greedy Search Path

| step | change | AC@1 | MRR | step delta AC@1 |
| ---: | --- | ---: | ---: | ---: |
| 1 | `trace_duration_z: BASELINE -> DISABLED` | 0.816456 | 0.884112 | +0.015471 |
| 2 | `topology_in_degree: DISABLED -> SUPPORT` | 0.821378 | 0.887160 | +0.004923 |
| 3 | `log_count_delta: BACKGROUND -> LOCAL` | 0.826301 | 0.890430 | +0.004923 |
| 4 | `trace_count_delta: BASELINE -> BACKGROUND` | 0.828411 | 0.891963 | +0.002110 |
| 5 | `log_error_rate: BACKGROUND -> LOCAL` | 0.829817 | 0.892886 | +0.001406 |
| 6 | `metric_count_drop_shift: ROOT -> HIGH` | 0.830520 | 0.892995 | +0.000703 |
| ladder 1 | `LOCAL: 1.5 -> 2.0` | 0.836850 | 0.896024 | +0.006329 |
| ladder 2 | `CRITICAL: 16 -> 20` | 0.839662 | 0.898061 | +0.002813 |

Interpretation:

- The dominant improvement is disabling `trace_duration_z`.
- The next meaningful increments come from adding topology support and increasing log-count/log-error from background to local corroboration.
- The `metric_count_drop_shift: ROOT -> HIGH` change is only one top-1 case and should be considered fragile.
- The ladder step is not independent from the priority assignment: `LOCAL=2` helps after log features are promoted to `LOCAL`.

## Single-Feature Priority Scan

Only a few single reassignments improve AC@1 over baseline:

| feature | old priority | best priority | best AC@1 | best MRR | delta AC@1 |
| --- | --- | --- | ---: | ---: | ---: |
| `trace_duration_z` | BASELINE | DISABLED | 0.816456 | 0.884112 | +0.015471 |
| `log_count_delta` | BACKGROUND | LOCAL | 0.803094 | 0.878003 | +0.002110 |
| `topology_in_degree` | DISABLED | LOCAL | 0.803094 | 0.875939 | +0.002110 |
| `log_error_rate` | BACKGROUND | LOCAL | 0.801688 | 0.875590 | +0.000703 |

Many feature priority changes are strongly harmful. For example, assigning high-scale context features to `CRITICAL` collapses AC@1:

| feature | worst priority | worst AC@1 | sensitivity range |
| --- | --- | ---: | ---: |
| `log_template_delta` | CRITICAL | 0.360056 | 0.440928 |
| `trace_duration_delta` | CRITICAL | 0.400844 | 0.400141 |
| `metric_max_z` | CRITICAL | 0.440225 | 0.360759 |
| `metric_mean_z` | CRITICAL | 0.511955 | 0.289030 |
| `abnormal_trace_rows` | CRITICAL | 0.526020 | 0.274965 |
| `trace_self_duration_relative_shift` | CRITICAL | 0.537271 | 0.263713 |
| `log_count_delta` | CRITICAL | 0.544304 | 0.258790 |

This confirms that the priority assignment is not freely interchangeable. Large-scale propagation or context features become destructive if promoted into root/critical tiers.

## Common Ladder Presets

The user asked whether simpler-looking ladders such as `0,1,1,1,2,5,10,15` can preserve or reach the best AC@1.

| assignment | ladder | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: |
| greedy step 6 | `0,0.75,1,1.25,2,6,10,20` | 0.839662 | 0.898061 | 0.950070 | 0.974684 |
| greedy step 6 | `0,0.75,1,1.25,1.5,6,10,16` | 0.830520 | 0.892995 | 0.947961 | 0.976793 |
| disable `trace_duration_z` only | `0,0.75,1,1.25,2,6,10,20` | 0.820675 | 0.886394 | 0.945851 | 0.975387 |
| greedy step 6 | `0,1,1,1,2,5,10,15` | 0.816456 | 0.884331 | 0.944444 | 0.974684 |
| disable `trace_duration_z` only | `0,0.75,1,1.25,1.5,6,10,16` | 0.816456 | 0.884112 | 0.945851 | 0.976793 |
| current priorities | `0,0.75,1,1.25,1.5,6,10,16` | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| disable `trace_duration_z` only | `0,1,1,1,2,5,10,15` | 0.796062 | 0.874065 | 0.943741 | 0.976090 |
| current priorities | `0,1,1,1,2,5,10,15` | 0.768636 | 0.858448 | 0.942335 | 0.975387 |
| greedy step 6 | `0,1,2,3,4,5,6,7` | 0.751055 | 0.836820 | 0.909986 | 0.948664 |
| current priorities | `0,1,2,3,4,5,6,7` | 0.671589 | 0.789295 | 0.886076 | 0.945148 |

Conclusion:

```text
Priority ordering alone helps, but direct clean-looking numeric ladders do not match the best candidate.
The optimized assignment makes the clean ladder less bad, raising it from 0.768636 to 0.816456,
but the best nonlinear ladder still adds another 0.023206 AC@1.
```

Therefore the defensible paper wording is:

```text
The exposed prior is ordinal diagnostic strength. A nonlinear severity ladder is synthesized to compensate feature-scale and diagnostic-specificity gaps.
```

The unsafe wording would be:

```text
Only the ordering matters and arbitrary monotonic values are equivalent.
```

## Ladder Range Sensitivity

The one-level scan fixes all other tiers and varies one tier at a time.

### Current Priorities + Current Ladder

| tier | best value | best AC@1 | exact best values | within one-case values | AC@1 range |
| --- | ---: | ---: | --- | --- | ---: |
| BACKGROUND | 0.75 | 0.800985 | 0.75 | 0.75 | 0.266526 |
| BASELINE | 1.00 | 0.800985 | 1 | 1 | 0.013361 |
| SUPPORT | 1.25 | 0.800985 | 1.25 | 1.25 | 0.005626 |
| LOCAL | 1.50 | 0.800985 | 1.5 | 1.5 | 0.029536 |
| HIGH | 6.00 | 0.800985 | 6 | 6 | 0.026020 |
| ROOT | 10.00 | 0.800985 | 8, 10 | 8, 10, 12, 14, 16 | 0.001406 |
| CRITICAL | 16.00 | 0.800985 | 16 | 16 | 0.018284 |

The default scorer is sensitive to `BACKGROUND`, `LOCAL`, `HIGH`, and `CRITICAL`. `ROOT` is tolerant in this one-level scan.

### Disable `trace_duration_z` + Current Ladder

| tier | best value | best AC@1 | exact best values | within one-case values | AC@1 range |
| --- | ---: | ---: | --- | --- | ---: |
| BACKGROUND | 0.75 | 0.816456 | 0.75 | 0.75 | 0.265120 |
| BASELINE | 1.00 | 0.816456 | 1 | 1 | 0.006329 |
| SUPPORT | 1.50 | 0.816456 | 1.25, 1.5 | 1.25, 1.5 | 0.002813 |
| LOCAL | 1.75 | 0.820675 | 1.75 | 1.75 | 0.018987 |
| HIGH | 6.00 | 0.816456 | 6 | 6 | 0.035162 |
| ROOT | 10.00 | 0.816456 | 8, 10 | 6, 8, 10 | 0.002110 |
| CRITICAL | 16.00 | 0.816456 | 16 | 16, 18, 20 | 0.014065 |

Disabling `trace_duration_z` reduces sensitivity for `BASELINE/SUPPORT/ROOT`, but `BACKGROUND/HIGH/LOCAL/CRITICAL` still matter.

### Greedy Step 6 + Current Ladder

| tier | best value | best AC@1 | exact best values | within one-case values | AC@1 range |
| --- | ---: | ---: | --- | --- | ---: |
| BACKGROUND | 0.75 | 0.830520 | 0.75 | 0.75 | 0.172293 |
| BASELINE | 1.00 | 0.830520 | 1 | 1 | 0.004219 |
| SUPPORT | 1.25 | 0.830520 | 1.25 | 1.25 | 0.001406 |
| LOCAL | 2.25 | 0.838959 | 2.25 | 2.25 | 0.017581 |
| HIGH | 6.00 | 0.830520 | 6 | 6 | 0.036568 |
| ROOT | 6.00 | 0.830520 | 6, 8, 10, 12, 14, 16 | 6, 8, 10, 12, 14, 16 | 0.000000 |
| CRITICAL | 16.00 | 0.830520 | 16 | 14, 16 | 0.010549 |

After the greedy priority changes, `ROOT` becomes fully insensitive in the tested range because the only root-assigned feature was demoted to `HIGH`. This is a clue that the original `ROOT` tier may be unnecessary for the current default scorer, but that conclusion is label-guided and does not automatically transfer to ARC.

### Greedy Step 6 + Best Ladder

| tier | best value | best AC@1 | exact best values | within one-case values | AC@1 range |
| --- | ---: | ---: | --- | --- | ---: |
| BACKGROUND | 0.75 | 0.839662 | 0.75 | 0.75 | 0.187060 |
| BASELINE | 1.00 | 0.839662 | 1 | 1 | 0.004923 |
| SUPPORT | 1.25 | 0.839662 | 1.25 | 1.25 | 0.004923 |
| LOCAL | 2.00 | 0.839662 | 2 | 2, 2.25 | 0.019691 |
| HIGH | 6.00 | 0.839662 | 6 | 6 | 0.019691 |
| ROOT | 6.00 | 0.839662 | 6, 8, 10, 12, 14, 16, 20 | 6, 8, 10, 12, 14, 16, 20 | 0.000000 |
| CRITICAL | 20.00 | 0.839662 | 20 | 20 | 0.011252 |

The best candidate is still sensitive to `BACKGROUND`, `LOCAL`, `HIGH`, and `CRITICAL`. The exact values are not arbitrary.

## Case Movement

Case movement versus baseline:

| candidate | improved_to_hit1 | regressed_from_hit1 | rank_improved | rank_regressed | unchanged |
| --- | ---: | ---: | ---: | ---: | ---: |
| disable `trace_duration_z` | 37 | 15 | 23 | 7 | 1340 |
| greedy step 6 + current ladder | 61 | 19 | 54 | 31 | 1257 |
| greedy step 6 + best ladder | 68 | 13 | 55 | 30 | 1256 |
| greedy step 6 + clean ladder | 67 | 45 | 43 | 47 | 1220 |

The best candidate improves many more top-1 cases than it regresses, but the clean ladder version has a much worse regression profile. This is the strongest evidence that the optimized priority ordering alone is not enough.

## Mechanism-Level Interpretation

### `trace_duration_z: BASELINE -> DISABLED`

Failure mechanism:

```text
Global trace duration z-score often identifies latency victims or propagation hotspots rather than the causal service.
```

Why current scorer can be wrong:

```text
The scorer already has `trace_duration_delta` and `trace_self_duration_relative_shift`.
Keeping `trace_duration_z` adds a third latency channel that can over-reward high-latency downstream services.
```

Potential general mechanism:

```text
Do not use raw global duration extremeness as a direct root-cause feature unless it passes a local/self-duration or topology contrast gate.
```

This is the most plausible candidate for a future accepted algorithm change, but disabling it solely because labels say so would be overfit-prone. A more defensible implementation would convert it into a self-supervised propagation-capped latency signal.

### `topology_in_degree: DISABLED -> SUPPORT`

Failure mechanism:

```text
When symptoms are distributed, structural position can help distinguish local service anomalies from isolated propagation artifacts.
```

Risk:

```text
High fan-in entry or aggregation services can also be victims. Topology should remain weak/supportive unless combined with direction-aware contrast.
```

### `log_count_delta` and `log_error_rate: BACKGROUND -> LOCAL`

Failure mechanism:

```text
Logs can corroborate service-local mutation after noisy trace duration evidence is removed.
```

Risk:

```text
High-volume victims and retry storms can produce large log changes. Promoting log evidence without a reliability gate may overfit RCABench logging behavior.
```

### `trace_count_delta: BASELINE -> BACKGROUND`

Failure mechanism:

```text
Raw trace count deltas are often traffic propagation or entry effects. Demoting them reduces victim/entry dominance.
```

This aligns with the user's root-vs-victim contrast direction.

### `metric_count_drop_shift: ROOT -> HIGH`

Failure mechanism:

```text
Metric count drop can be root-specific in availability failures, but as a single feature it should not dominate all other evidence.
```

Risk:

```text
The gain is only one top-1 case in greedy search, so it is likely the least stable change.
```

## Acceptance Decision

Do not accept the full best candidate into default `algorithm.py` in this turn.

Reasons:

- The search is label-guided and therefore estimates an upper bound, not an unsupervised mechanism.
- The best candidate changes both priority assignment and ladder values based on metric feedback.
- Several changes are plausible but not equally robust; `metric_count_drop_shift: ROOT -> HIGH` is especially thin.
- AC@5 drops by one case and needs a compare report if implemented.

Recommended next accepted-code candidate:

```text
Replace direct `trace_duration_z` contribution with an unsupervised propagation-capped latency signal,
or run a full eval candidate that sets `trace_duration_z` to DISABLED and document the mechanism as
victim-latency suppression.
```

Recommended next research candidate:

```text
Learn a case-local gate for global latency evidence:
use `trace_duration_z` only when it agrees with self-duration, endpoint/status mutation, or upstream/downstream contrast.
This keeps the feature available for true local latency faults while suppressing propagation victims.
```

## Reproduction

The experiment starts from the raw feature cache:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py dump \
  --version FW_FEATURE_CACHE_BASE \
  --dataset rcabench \
  --workers 48
```

The baseline can be replayed with:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_CURRENT \
  --preset current \
  --dataset rcabench
```

The comprehensive search in this iteration used an offline Python replay over:

```text
VibeResearchTools.evidrank_feature_cache._load_cache
VibeResearchTools.evidrank_feature_cache._prepare_cached_cases
VibeResearchTools.evidrank_feature_cache._score_case
VibeResearchTools.evidrank_feature_cache._metrics
```

and wrote all result tables listed in the artifact section. If this experiment is repeated, use a new version directory instead of overwriting `FW_PRIORITY_COMPREHENSIVE_SEARCH`.

## Final Conclusion

The current EvidenceRank scorer has a much higher label-guided upper bound than the accepted default: offline replay reached `AC@1=0.839662` without changing scoring logic.

The strongest robust insight is not a new numeric ladder. It is:

```text
Raw global trace-duration extremeness is harmful as a direct root-cause signal;
local/self-duration, endpoint/status mutation, topology support, and log corroboration are more root-specific.
```

For the paper, the cleanest claim remains:

```text
EvidenceRank exposes an ordinal diagnostic-priority prior, while the nonlinear ladder provides scale and specificity separation.
The exact visible constants are less important than the diagnostic tiering and the nonlinear separation,
but arbitrary monotonic ladders are not equivalent under the current linear scorer.
```
