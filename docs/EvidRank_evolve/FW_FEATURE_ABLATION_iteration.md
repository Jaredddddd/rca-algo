# EvidenceRank FW_FEATURE_ABLATION Iteration

- Created: 2026-06-04T02:35:00+08:00
- Hypothesis: 对 `BASE_FEATURE_NAMES` 做系统离线消融，可以区分当前默认 EvidenceRank scorer 中真正有边际贡献的信号、只在单独排序中有诊断能力但组合中冗余的信号、以及会把传播/受害者症状误推到 top-1 的有害信号。
- Algorithm: `evidencerank`
- Dataset: `rcabench`
- Baseline: `FW_PRIORITY_SYNTH_LADDER`

## Safety Boundary

This is offline analysis over the cached raw feature matrix `FW_FEATURE_CACHE_BASE`.

Labels are used only to compute offline AC@1/MRR/AC@3/AC@5. No labels, injections, outputs, historical rankings, or case ids are read by `algorithms/evidencerank`.

The conclusions below are about the current default `evidencerank` scorer. They should not be directly generalized to `evidencerank_arc`, where topology and reliability logic are different.

## Artifacts

Output directory:

```text
output/rcabench-platform-v2/evolve_reweights/FW_FEATURE_ABLATION_SYNTH_LADDER/
```

Important files:

```text
manifest.json
ablation_summary.csv
leave_one_out.csv
single_feature_only.csv
leave_priority_out.csv
priority_only.csv
leave_modality_out.csv
modality_only.csv
leave_family_out.csv
family_only.csv
combined_ablation.csv
greedy_backward_elimination.csv
*_case_delta.csv
```

## Method

Base weights are the synthesized priority ladder from `FW_PRIORITY_SYNTH_LADDER`:

| feature | priority | weight |
| --- | --- | ---: |
| `metric_max_z` | BACKGROUND | 0.75 |
| `metric_mean_z` | BACKGROUND | 0.75 |
| `metric_anomaly_count` | BACKGROUND | 0.75 |
| `metric_value_delta` | BACKGROUND | 0.75 |
| `metric_count_drop_shift` | ROOT | 10.0 |
| `trace_duration_z` | BASELINE | 1.0 |
| `trace_duration_delta` | BASELINE | 1.0 |
| `trace_count_delta` | BASELINE | 1.0 |
| `trace_count_rise_shift` | HIGH | 6.0 |
| `trace_count_drop_shift` | BASELINE | 1.0 |
| `trace_endpoint_shift` | HIGH | 6.0 |
| `trace_error_rate` | BASELINE | 1.0 |
| `trace_status_code_shift` | CRITICAL | 16.0 |
| `trace_self_duration_relative_shift` | LOCAL | 1.5 |
| `log_count_delta` | BACKGROUND | 0.75 |
| `log_error_rate` | BACKGROUND | 0.75 |
| `log_template_delta` | BACKGROUND | 0.75 |
| `topology_in_degree` | DISABLED | 0.0 |
| `topology_out_degree` | DISABLED | 0.0 |
| `abnormal_metric_rows` | SUPPORT | 1.25 |
| `abnormal_trace_rows` | SUPPORT | 1.25 |

Experiments:

- `leave_one_out`: set exactly one feature's weight to zero.
- `single_feature_only`: keep exactly one feature active.
- `leave_priority_out` / `priority_only`: remove or isolate one `FeaturePriority` tier.
- `leave_modality_out` / `modality_only`: remove or isolate metric, trace, or log modality.
- `leave_family_out` / `family_only`: remove or isolate manually defined diagnostic families.
- `combined_ablation`: test targeted combinations suggested by the first pass.
- `greedy_backward_elimination`: label-guided offline diagnostic; repeatedly remove the one active feature that improves AC@1/MRR most.

## Baseline

| total | error | AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1422 | 0 | 0.800985 | 0.874517 | 0.942335 | 0.975387 |

## Leave-One-Out Results

Positive `delta_ac1` means removing the feature improved AC@1, so the feature is harmful in the current combination. Negative `delta_ac1` means the feature contributes useful signal.

| removed feature | AC@1 | MRR | AC@3 | AC@5 | delta AC@1 | delta MRR | regressed_from_hit1 | improved_to_hit1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `trace_duration_z` | 0.816456 | 0.884112 | 0.945851 | 0.976793 | +0.015471 | +0.009595 | 15 | 37 |
| `abnormal_metric_rows` | 0.800985 | 0.874670 | 0.942335 | 0.976090 | +0.000000 | +0.000153 | 0 | 0 |
| `trace_error_rate` | 0.800985 | 0.874517 | 0.942335 | 0.975387 | +0.000000 | +0.000000 | 0 | 0 |
| `topology_in_degree` | 0.800985 | 0.874517 | 0.942335 | 0.975387 | +0.000000 | +0.000000 | 0 | 0 |
| `topology_out_degree` | 0.800985 | 0.874517 | 0.942335 | 0.975387 | +0.000000 | +0.000000 | 0 | 0 |
| `log_error_rate` | 0.800985 | 0.874211 | 0.940928 | 0.976090 | +0.000000 | -0.000305 | 0 | 0 |
| `trace_count_drop_shift` | 0.798172 | 0.873207 | 0.944444 | 0.974684 | -0.002813 | -0.001310 | 8 | 4 |
| `metric_count_drop_shift` | 0.797468 | 0.872750 | 0.940225 | 0.976090 | -0.003516 | -0.001767 | 7 | 2 |
| `metric_anomaly_count` | 0.796062 | 0.872795 | 0.943038 | 0.976090 | -0.004923 | -0.001722 | 13 | 6 |
| `trace_count_delta` | 0.789733 | 0.869857 | 0.946554 | 0.978903 | -0.011252 | -0.004660 | 24 | 8 |
| `trace_duration_delta` | 0.789030 | 0.871386 | 0.952180 | 0.973277 | -0.011955 | -0.003131 | 39 | 22 |
| `metric_value_delta` | 0.789030 | 0.867898 | 0.937412 | 0.974684 | -0.011955 | -0.006619 | 31 | 14 |
| `abnormal_trace_rows` | 0.779887 | 0.863428 | 0.942335 | 0.976090 | -0.021097 | -0.011089 | 40 | 10 |
| `log_template_delta` | 0.769339 | 0.856781 | 0.940225 | 0.970464 | -0.031646 | -0.017736 | 58 | 13 |
| `metric_mean_z` | 0.767932 | 0.855161 | 0.937412 | 0.969761 | -0.033052 | -0.019356 | 65 | 18 |
| `metric_max_z` | 0.764416 | 0.853272 | 0.939522 | 0.968354 | -0.036568 | -0.021244 | 72 | 20 |
| `trace_endpoint_shift` | 0.760197 | 0.845533 | 0.920534 | 0.956399 | -0.040788 | -0.028984 | 85 | 27 |
| `log_count_delta` | 0.759494 | 0.850702 | 0.936006 | 0.976090 | -0.041491 | -0.023814 | 63 | 4 |
| `trace_count_rise_shift` | 0.745429 | 0.847589 | 0.947961 | 0.973980 | -0.055556 | -0.026927 | 89 | 10 |
| `trace_self_duration_relative_shift` | 0.719409 | 0.827396 | 0.929677 | 0.973980 | -0.081575 | -0.047121 | 145 | 29 |
| `trace_status_code_shift` | 0.715893 | 0.813851 | 0.886076 | 0.945148 | -0.085091 | -0.060665 | 158 | 37 |

## Feature Utility Tiers

### Harmful In Current Combination

| feature | evidence |
| --- | --- |
| `trace_duration_z` | Removing it improves AC@1 by `+0.015471` and MRR by `+0.009595`; 37 cases improve to hit@1 while 15 regress from hit@1. |

Interpretation: z-scored trace latency appears to over-promote propagated latency victims. The duration family is not entirely bad, because `trace_duration_delta` and `trace_self_duration_relative_shift` are useful; the harmful part is specifically `trace_duration_z`.

### Strong Positive Marginal Contribution

Removing these drops AC@1 by at least about `0.04`.

| feature | delta AC@1 when removed | likely role |
| --- | ---: | --- |
| `trace_status_code_shift` | -0.085091 | critical protocol/status mutation signal |
| `trace_self_duration_relative_shift` | -0.081575 | local service-side latency mutation |
| `trace_count_rise_shift` | -0.055556 | traffic/entry rise signal, important with endpoint gate |
| `log_count_delta` | -0.041491 | log-volume corroboration, strong interaction signal |
| `trace_endpoint_shift` | -0.040788 | endpoint distribution mutation |

### Medium Positive Marginal Contribution

| feature | delta AC@1 when removed | likely role |
| --- | ---: | --- |
| `metric_max_z` | -0.036568 | metric spike evidence |
| `metric_mean_z` | -0.033052 | sustained metric shift |
| `log_template_delta` | -0.031646 | log pattern distribution shift |
| `abnormal_trace_rows` | -0.021097 | trace support / row-count confidence |
| `metric_value_delta` | -0.011955 | metric value shift |
| `trace_duration_delta` | -0.011955 | raw duration shift, useful despite `trace_duration_z` being harmful |
| `trace_count_delta` | -0.011252 | trace count shift |

### Weak Positive Marginal Contribution

| feature | delta AC@1 when removed | note |
| --- | ---: | --- |
| `metric_anomaly_count` | -0.004923 | weak support |
| `metric_count_drop_shift` | -0.003516 | small but positive root/drop signal under current scorer |
| `trace_count_drop_shift` | -0.002813 | weak but positive |

These are not useless; they have small marginal contribution because stronger correlated features already carry much of the signal.

### Neutral Or Currently Unused

| feature | delta AC@1 when removed | note |
| --- | ---: | --- |
| `trace_error_rate` | 0.000000 | feature is effectively inactive in this dataset/cache; single-feature-only AC@1 is `0`. |
| `log_error_rate` | 0.000000 | no top-1 marginal effect, slight MRR decrease when removed. |
| `abnormal_metric_rows` | 0.000000 | no top-1 marginal effect, tiny MRR increase when removed. |
| `topology_in_degree` | 0.000000 | default weight is `0`; no conclusion about ARC topology utility. |
| `topology_out_degree` | 0.000000 | default weight is `0`; no conclusion about ARC topology utility. |

## Single-Feature-Only Results

Single-feature-only measures standalone diagnostic power. It is not the same as marginal utility because EvidenceRank is a multimodal fusion method.

Top standalone features:

| feature | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| `trace_status_code_shift` | 0.389592 | 0.569878 | 0.711674 | 0.789030 |
| `metric_anomaly_count` | 0.376231 | 0.504773 | 0.554149 | 0.651195 |
| `trace_self_duration_relative_shift` | 0.373418 | 0.503993 | 0.540788 | 0.640647 |
| `metric_mean_z` | 0.364979 | 0.507271 | 0.568917 | 0.684248 |
| `metric_max_z` | 0.343179 | 0.470194 | 0.514065 | 0.618143 |
| `trace_endpoint_shift` | 0.331927 | 0.472015 | 0.510549 | 0.623066 |
| `trace_duration_z` | 0.271449 | 0.411357 | 0.433896 | 0.558368 |

Important nuance: `trace_duration_z` has nontrivial standalone diagnostic power but is harmful in the full combination. That is a classic victim-propagation symptom: it can identify anomalous services, but when fused with root-specific signals it over-ranks affected downstream/entry services.

## Priority-Tier Ablation

| removed priority | AC@1 | MRR | delta AC@1 | interpretation |
| --- | ---: | ---: | ---: | --- |
| DISABLED | 0.800985 | 0.874517 | 0.000000 | no current effect |
| ROOT | 0.797468 | 0.872750 | -0.003516 | weak marginal under current scorer |
| BASELINE | 0.792546 | 0.872847 | -0.008439 | many baseline features are redundant/noisy |
| SUPPORT | 0.779184 | 0.863369 | -0.021800 | row-count confidence matters |
| LOCAL | 0.719409 | 0.827396 | -0.081575 | local self-duration shift matters |
| CRITICAL | 0.715893 | 0.813851 | -0.085091 | status mutation is critical |
| HIGH | 0.689873 | 0.806708 | -0.111111 | endpoint/count rise are very important |
| BACKGROUND | 0.534459 | 0.682764 | -0.266526 | background metric/log evidence is collectively essential |

Priority-only best tier:

| priority only | AC@1 | MRR |
| --- | ---: | ---: |
| BACKGROUND | 0.439522 | 0.588986 |
| CRITICAL | 0.389592 | 0.569878 |
| LOCAL | 0.373418 | 0.503993 |
| HIGH | 0.317159 | 0.456380 |
| BASELINE | 0.301688 | 0.443608 |

Interpretation: "BACKGROUND" sounds weak, but it contains several broad metric/log signals and is collectively important. The priority name means "low per-feature diagnostic specificity", not "safe to remove".

## Modality Ablation

| experiment | AC@1 | MRR | delta AC@1 | interpretation |
| --- | ---: | ---: | ---: | --- |
| leave log out | 0.704641 | 0.818491 | -0.096343 | log is auxiliary but useful |
| leave metric out | 0.617440 | 0.722785 | -0.183544 | metric is important |
| leave trace out | 0.443741 | 0.590651 | -0.357243 | trace is most important |
| trace only | 0.535162 | 0.676815 | -0.265823 | trace is strongest standalone modality |
| metric only | 0.400844 | 0.530948 | -0.400141 | metric alone is weaker than trace |
| log only | 0.123066 | 0.297466 | -0.677918 | log alone is weak |

## Family Ablation

| removed family | AC@1 | MRR | delta AC@1 | interpretation |
| --- | ---: | ---: | ---: | --- |
| topology | 0.800985 | 0.874517 | 0.000000 | default weight is zero |
| metric_root | 0.797468 | 0.872750 | -0.003516 | `metric_count_drop_shift` is weak but positive |
| support_rows | 0.779184 | 0.863369 | -0.021800 | support rows help |
| log | 0.704641 | 0.818491 | -0.096343 | log corroboration helps |
| trace_volume | 0.700422 | 0.818889 | -0.100563 | trace count/rise/drop/support is important |
| trace_latency | 0.693390 | 0.792640 | -0.107595 | latency family is useful overall despite `trace_duration_z` harm |
| trace_endpoint_status | 0.665260 | 0.766012 | -0.135724 | endpoint/status family is critical |
| metric_core | 0.619550 | 0.730162 | -0.181435 | metric z/value/count evidence is important |
| nonzero_trace_strong | 0.558368 | 0.694486 | -0.242616 | trace strong mutation signals are critical |
| high_root_critical | 0.556962 | 0.694190 | -0.244023 | high/root/critical tiers are collectively critical |
| background_all | 0.534459 | 0.682764 | -0.266526 | background metric/log evidence is collectively critical |

## Combined Ablation

Targeted combinations were tested after the leave-one-out pass.

| experiment | removed features | AC@1 | MRR | AC@3 | AC@5 | delta AC@1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `drop_trace_duration_z` | `trace_duration_z` | 0.816456 | 0.884112 | 0.945851 | 0.976793 | +0.015471 |
| `drop_trace_duration_z_no_current_weight` | `trace_duration_z,topology_in_degree,topology_out_degree` | 0.816456 | 0.884112 | 0.945851 | 0.976793 | +0.015471 |
| `drop_trace_duration_z_abnormal_metric_rows` | `trace_duration_z,abnormal_metric_rows` | 0.816456 | 0.884053 | 0.945148 | 0.976793 | +0.015471 |
| `drop_trace_duration_z_trace_count_drop_shift` | `trace_duration_z,trace_count_drop_shift` | 0.815049 | 0.883653 | 0.947257 | 0.976090 | +0.014065 |
| `drop_trace_duration_z_trace_error_log_error` | `trace_duration_z,trace_error_rate,log_error_rate` | 0.815049 | 0.883132 | 0.943741 | 0.976090 | +0.014065 |
| `drop_zero_marginal` | `trace_error_rate,log_error_rate,abnormal_metric_rows` | 0.800985 | 0.874224 | 0.940928 | 0.976090 | +0.000000 |

Best combination: remove only `trace_duration_z`.

## Greedy Backward Elimination

Label-guided offline greedy search selected only one improving removal:

| step | removed feature | AC@1 | MRR | AC@3 | AC@5 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `trace_duration_z` | 0.816456 | 0.884112 | 0.945851 | 0.976793 |

After removing `trace_duration_z`, no additional single removal improved the AC@1/MRR objective.

## Interpretation

### Features to Keep

These have clear positive contribution and should not be removed casually:

```text
trace_status_code_shift
trace_self_duration_relative_shift
trace_count_rise_shift
trace_endpoint_shift
log_count_delta
metric_max_z
metric_mean_z
log_template_delta
abnormal_trace_rows
trace_duration_delta
trace_count_delta
metric_value_delta
metric_anomaly_count
metric_count_drop_shift
trace_count_drop_shift
```

### Features to Reconsider

```text
trace_duration_z
```

This is the only feature whose removal improved every headline metric in the offline cache replay:

| baseline | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| all features | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| without `trace_duration_z` | 0.816456 | 0.884112 | 0.945851 | 0.976793 |

Hypothesis: `trace_duration_z` is a propagation-sensitive victim signal. It points to anomalous latency but not necessarily root cause. `trace_duration_delta` and `trace_self_duration_relative_shift` preserve more useful latency information, so dropping z-score latency removes noise while keeping better latency variants.

### Features with Little Current Effect

```text
trace_error_rate
log_error_rate
abnormal_metric_rows
topology_in_degree
topology_out_degree
```

Notes:

- `topology_in_degree` and `topology_out_degree` have weight `0` in default `evidencerank`; this says nothing about ARC, where topology has proven useful.
- `trace_error_rate` appears inactive in the current cache.
- `log_error_rate` has no top-1 marginal effect but a tiny MRR effect; it should be treated as weak, not necessarily harmful.
- `abnormal_metric_rows` has no top-1 marginal effect and tiny positive MRR when removed, but combining its removal with `trace_duration_z` slightly reduces MRR compared with removing `trace_duration_z` alone.

## Decision

No algorithm default was changed in this ablation turn.

Recommended next candidate if we decide to optimize default `evidencerank`: remove or strongly downweight `trace_duration_z`, then run the normal full-eval/snapshot/summary/compare cycle as a new accepted-or-rejected version.

This ablation is label-guided offline analysis. It is useful evidence, but should not be described as an unsupervised online selection mechanism.
