# EvidenceRank Feature Priority Weight Study

This document records the full feature-priority / feature-weight sensitivity study around default `evidencerank`.

The short conclusion:

- Directly replacing the accepted ladder with clean-looking values such as `0,1,1,1,2,5,10,15` does not preserve AC@1.
- The scorer is sensitive because raw feature scales differ strongly: root-specific evidence such as `metric_count_drop_shift` is numerically small, while propagation/count/duration symptoms can be much larger.
- Scale compensation and rank fusion can reduce the gap, and some variants improve MRR or AC@3/AC@5, but they did not recover the accepted AC@1.
- The accepted implementation change is to remove the explicit `FEATURE_PRIORITY_WEIGHTS` float table and synthesize the nonlinear diagnostic severity ladder from ordinal `FeaturePriority` tiers.

Current accepted full-eval metrics for `FW_PRIORITY_SYNTH_LADDER`:

| total | error | AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1422 | 0 | 0.800985 | 0.874517 | 0.942335 | 0.975387 |

## Safety Boundary

All experiments below are offline analysis. They may read `labels.csv` only to compute metrics. The runtime algorithm under `algorithms/evidencerank` must not read labels, injections, previous output, perf reports, or any ground truth.

The feature cache stores raw EvidenceRank service-feature matrices generated from metrics, traces, logs, and topology. It does not store labels in the cached feature matrix.

## Current Code State

The current algorithm uses feature priorities, not a hand-maintained feature-weight table.

Code location: `algorithms/evidencerank/src/evidencerank/algorithm.py`

The per-feature declaration is ordinal:

```python
FEATURE_PRIORITIES = {
    "metric_max_z": FeaturePriority.BACKGROUND,
    "metric_mean_z": FeaturePriority.BACKGROUND,
    ...
    "metric_count_drop_shift": FeaturePriority.ROOT,
    "trace_status_code_shift": FeaturePriority.CRITICAL,
}
```

The numeric severity curve is synthesized by `_synthesize_feature_priority_ladder()`:

```text
low_tiers = BACKGROUND, BASELINE, SUPPORT, LOCAL
low_step = 1 / len(low_tiers)
BACKGROUND = 1 - low_step = 0.75
BASELINE = 1
SUPPORT = 1 + low_step = 1.25
LOCAL = 1 + 2 * low_step = 1.5
HIGH = LOCAL * len(low_tiers) = 6
ROOT = HIGH + len(low_tiers) = 10
CRITICAL = next_power_of_two(ROOT) = 16
```

Generated ladder:

```text
[0.0, 0.75, 1.0, 1.25, 1.5, 6.0, 10.0, 16.0]
```

The important paper wording is:

```text
EvidenceRank uses an ordinal SRE feature-priority prior and synthesizes a nonlinear diagnostic severity ladder.
The exact numeric entries are not the exposed algorithm interface; they are generated from the priority-tier topology.
```

Do not claim that arbitrary direct linear weights are interchangeable. The experiments below show that they are not.

## Reproduction Environment

Run commands from the repository root:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
```

Use the EvidenceRank uv environment:

```bash
uv run --package evidencerank python ...
```

Main files:

```text
algorithms/evidencerank/src/evidencerank/algorithm.py
VibeResearchTools/evidrank_feature_cache.py
docs/EvidRank_evolve/FW_PRIORITY_LADDER_ABLATION_iteration.md
docs/EvidRank_evolve/FW_PRIORITY_SYNTH_LADDER_iteration.md
```

Main generated artifacts:

```text
output/rcabench-platform-v2/evolve_feature_cache/FW_FEATURE_CACHE_BASE/
output/rcabench-platform-v2/evolve_reweights/
output/rcabench-platform-v2/evolve_snapshots/FW_PRIORITY_SYNTH_LADDER/
output/rcabench-platform-v2/evolve_reports/FW_PRIORITY_SYNTH_LADDER/
```

## Feature Cache Workflow

The feature cache lets us save pre-fusion service-feature matrices once, then replay different priority ladders without running full batch eval every time.

Dump raw feature matrices:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py dump \
  --version FW_FEATURE_CACHE_BASE \
  --dataset rcabench \
  --workers 48
```

Observed cache:

| artifact | value |
| --- | ---: |
| cases | 1422 |
| service-feature rows | 69684 |
| errors | 0 |

Offline reweight using a preset:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_CURRENT \
  --preset current \
  --dataset rcabench
```

Offline reweight using explicit ladder values:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_DECIMAL_1_2_5_10_15 \
  --weights 0,1,1,1,2,5,10,15 \
  --dataset rcabench
```

The offline scorer replays:

- `_heuristic_scores`;
- legacy endpoint support gate;
- adaptive modality reweighting if it preserves the top-ranked service;
- parent context smoothing.

Therefore it reproduced full-eval metrics exactly for the accepted ladder.

## Baseline And Direct Ladder Results

Baseline:

| version | ladder | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: |
| `FW_PRIORITY_PRIOR` | `0,0.75,1,1.25,1.5,6,10,16` | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| `FW_NUMERIC_BASELINE` | older direct numeric table | 0.802391 | 0.875337 | 0.943741 | 0.975387 |

Direct clean-looking ladders:

| version / preset | ladder | AC@1 | MRR | AC@3 | AC@5 | result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `FW_REWEIGHT_CURRENT` | `0,0.75,1,1.25,1.5,6,10,16` | 0.800985 | 0.874517 | 0.942335 | 0.975387 | accepted behavior |
| `FW_REWEIGHT_LINEAR_0_7` | `0,1,2,3,4,5,6,7` | 0.671589 | 0.789295 | 0.886076 | 0.945148 | reject |
| `FW_REWEIGHT_POWER2_TIER` | `0,1,1,1,2,4,8,16` | 0.756681 | 0.851812 | 0.941632 | 0.973980 | reject |
| `FW_REWEIGHT_DECIMAL_1_2_5_10_15` | `0,1,1,1,2,5,10,15` | 0.768636 | 0.858448 | 0.942335 | 0.975387 | reject |

Command examples:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_LINEAR_0_7 \
  --preset linear_0_7 \
  --dataset rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_POWER2_TIER \
  --preset power2_tier \
  --dataset rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_DECIMAL_1_2_5_10_15 \
  --preset decimal_1_2_5_10_15 \
  --dataset rcabench
```

Interpretation:

- `0..7` compresses `CRITICAL / BASELINE` from `16` to `3.5`.
- `0..7` compresses `ROOT / BASELINE` from `10` to `3`.
- It also raises background/support/local symptoms relative to strong root evidence.
- The result is that victims, entry services, and high-volume propagation symptoms steal top-1.

## Raw Feature Scale Diagnosis

The key reason direct ordinal values are unstable is feature scale mismatch.

Reproduce:

```bash
uv run --package evidencerank python - <<'PY'
from pathlib import Path
import sys, math
import numpy as np
import pandas as pd

repo = Path("/home/ljw/paper/aegis/rca-algo-contrib")
sys.path.insert(0, str(repo / "algorithms/evidencerank/src"))

from evidencerank.algorithm import BASE_FEATURE_NAMES, FEATURE_PRIORITIES

features = pd.read_parquet(
    repo / "output/rcabench-platform-v2/evolve_feature_cache/FW_FEATURE_CACHE_BASE/features.parquet"
)

rows = []
for name in BASE_FEATURE_NAMES:
    vals = pd.to_numeric(features[name], errors="coerce").fillna(0).to_numpy(float)
    pos = vals[vals > 0]
    rows.append({
        "feature": name,
        "priority": FEATURE_PRIORITIES[name].name,
        "nonzero_rate": len(pos) / len(vals),
        "median_pos": float(np.median(pos)) if len(pos) else 0.0,
        "p95_pos": float(np.percentile(pos, 95)) if len(pos) > 1 else (float(pos[0]) if len(pos) == 1 else 0.0),
        "p99_pos": float(np.percentile(pos, 99)) if len(pos) > 1 else (float(pos[0]) if len(pos) == 1 else 0.0),
    })

print(pd.DataFrame(rows).to_string(index=False, float_format=lambda value: f"{value:.4f}"))
PY
```

Observed key scales:

| feature | priority | nonzero_rate | median_pos | p95_pos | p99_pos |
| --- | --- | ---: | ---: | ---: | ---: |
| `metric_value_delta` | BACKGROUND | 0.8055 | 19.0463 | 21.2317 | 22.7031 |
| `log_count_delta` | BACKGROUND | 0.6070 | 6.2710 | 8.7273 | 9.3490 |
| `trace_duration_delta` | BASELINE | 0.5649 | 14.8121 | 20.8001 | 23.7316 |
| `trace_count_delta` | BASELINE | 0.6114 | 7.0901 | 9.2137 | 9.9949 |
| `abnormal_trace_rows` | SUPPORT | 0.5649 | 6.7754 | 9.2988 | 10.2085 |
| `trace_self_duration_relative_shift` | LOCAL | 0.2615 | 1.3193 | 5.2466 | 7.9970 |
| `trace_count_rise_shift` | HIGH | 0.0911 | 1.0042 | 2.0874 | 2.2782 |
| `trace_endpoint_shift` | HIGH | 0.4529 | 0.2909 | 1.2325 | 1.6640 |
| `metric_count_drop_shift` | ROOT | 0.2411 | 0.1256 | 0.2360 | 0.4292 |
| `trace_status_code_shift` | CRITICAL | 0.0708 | 0.2323 | 1.2016 | 1.4747 |

Most important observation:

```text
ROOT metric_count_drop_shift p95 ~= 0.236
BACKGROUND / BASELINE count-duration p95 often ~= 5..21
```

So a simple linear ordinal ladder gives too much room to large-scale propagation symptoms.

## Weight Range Scans

### Strong-Layer Range With Current Low Layers

Fixed low layers:

```text
BACKGROUND=0.75, BASELINE=1, SUPPORT=1.25, LOCAL=1.5
```

Command:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py scan \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_SCAN_CURRENT_LOW_STRONG_RANGE \
  --dataset rcabench \
  --background 0.75 \
  --baseline 1 \
  --support 1.25 \
  --local 1.5 \
  --high-values 4,5,6,7,8 \
  --root-values 8,9,10,11,12 \
  --critical-values 12,14,15,16,18,20
```

Results:

| varied level | value | best AC@1 | best MRR |
| --- | ---: | ---: | ---: |
| HIGH | 4 | 0.784107 | 0.866192 |
| HIGH | 5 | 0.792546 | 0.870965 |
| HIGH | 6 | 0.800985 | 0.874517 |
| HIGH | 7 | 0.797468 | 0.872793 |
| HIGH | 8 | 0.790436 | 0.868981 |
| ROOT | 8 | 0.800985 | 0.874507 |
| ROOT | 9 | 0.800985 | 0.874392 |
| ROOT | 10 | 0.800985 | 0.874517 |
| ROOT | 11 | 0.800985 | 0.874378 |
| ROOT | 12 | 0.800281 | 0.874112 |
| CRITICAL | 12 | 0.792546 | 0.870069 |
| CRITICAL | 14 | 0.796062 | 0.871984 |
| CRITICAL | 15 | 0.797468 | 0.872793 |
| CRITICAL | 16 | 0.800985 | 0.874517 |
| CRITICAL | 18 | 0.799578 | 0.874341 |
| CRITICAL | 20 | 0.798875 | 0.874235 |

Conclusion:

- `ROOT` is relatively tolerant around `8..11`.
- `HIGH` and `CRITICAL` are sensitive.
- `CRITICAL=16` is the only tested value that preserved full AC@1 in this grid.

### Integer Low-Layer Scan

Fixed integer low layers:

```text
BACKGROUND=1, BASELINE=1, SUPPORT=1, LOCAL=2
```

Best full ladder in this grid:

```text
0,1,1,1,2,8,10,20
```

Metrics:

| AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: |
| 0.791139 | 0.871603 | 0.949367 | 0.981013 |

This improved AC@3/AC@5 but lost 14 top-1 hits versus current.

### Low-Layer Range With Current Strong Layers

Fixed strong layers:

```text
HIGH=6, ROOT=10, CRITICAL=16, BASELINE=1
```

Command:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py scan \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_SCAN_LOW_RANGE_STRONG_CURRENT \
  --dataset rcabench \
  --background-values 0.5,0.75,1 \
  --baseline-values 1 \
  --support-values 1,1.25,1.5 \
  --local-values 1,1.5,2 \
  --high-values 6 \
  --root-values 10 \
  --critical-values 16
```

Results:

| level | value | best AC@1 | best MRR |
| --- | ---: | ---: | ---: |
| BACKGROUND | 0.50 | 0.779887 | 0.861955 |
| BACKGROUND | 0.75 | 0.800985 | 0.874517 |
| BACKGROUND | 1.00 | 0.786920 | 0.869020 |
| SUPPORT | 1.00 | 0.795359 | 0.872322 |
| SUPPORT | 1.25 | 0.800985 | 0.874517 |
| SUPPORT | 1.50 | 0.797468 | 0.872704 |
| LOCAL | 1.00 | 0.779887 | 0.864244 |
| LOCAL | 1.50 | 0.800985 | 0.874517 |
| LOCAL | 2.00 | 0.789733 | 0.869020 |

Conclusion:

The low layers are also sensitive. In this coarse grid, only the current low-layer values preserved AC@1.

## What Is Scale Compensation?

Scale compensation tries to correct the fact that different features have different numeric ranges.

Without compensation:

```text
score(service) = sum_j feature_value(service, j) * priority_weight(j)
```

If feature `A` has p95 scale `20` and feature `B` has p95 scale `0.2`, then `B` needs a much larger priority weight to compete. Direct ordinal weights ignore this.

### Feature-Wise Scale Compensation

For each feature `j`:

```text
scale_j = p95_positive(feature_j over all cached service rows)
multiplier_j = (reference_scale / scale_j) ** alpha
effective_weight_j = ladder[priority_j] * multiplier_j
```

`alpha` controls compensation strength:

- `alpha=0`: no compensation;
- `alpha=1`: full inverse-scale compensation;
- `0 < alpha < 1`: partial compensation.

Feature-wise compensation gives each feature its own multiplier. This is powerful but can overfit feature idiosyncrasies and over-amplify tiny-scale features.

Observed decimal-ladder feature-wise scan:

| method | alpha | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| feature p95 | 0.00 | 0.768636 | 0.858448 | 0.942335 | 0.975387 |
| feature p95 | 0.05 | 0.774262 | 0.862332 | 0.945851 | 0.975387 |
| feature p95 | 0.10 | 0.775668 | 0.863744 | 0.946554 | 0.976090 |
| feature p95 | 0.15 | 0.779184 | 0.865758 | 0.948664 | 0.976090 |
| feature p95 | 0.20 | 0.777075 | 0.864729 | 0.947961 | 0.978200 |
| feature p95 | 0.25 | 0.777075 | 0.865100 | 0.952883 | 0.979606 |
| feature p95 | 0.30 | 0.777778 | 0.865784 | 0.953586 | 0.980309 |
| feature p95 | 0.40 | 0.767932 | 0.860994 | 0.950070 | 0.980309 |
| feature p95 | 0.60 | 0.740506 | 0.845477 | 0.942335 | 0.978903 |
| feature p95 | 1.00 | 0.657525 | 0.786963 | 0.902954 | 0.957806 |

Best AC@1 was only `0.779184`, so feature-wise inverse scale does not recover the accepted ranking.

### Priority-Group Scale Compensation

To reduce freedom, we can share one scale per priority tier:

```text
group_scale_l = aggregate(scale_j for all features with priority l)
multiplier_l = (reference_scale / group_scale_l) ** alpha
effective_weight_j = ladder[priority_j] * multiplier_priority_j
```

Aggregates tested:

- `median`: median feature scale inside a priority tier;
- `mean`: mean feature scale inside a priority tier;
- `max`: max feature scale inside a priority tier.

Modes tested:

- `two_sided`: allow both upweighting small-scale groups and downweighting large-scale groups;
- `down_only`: only downweight groups above the reference scale, never upweight small-scale groups;
- `sqrt_up_cap`: downweight fully, but take square-root for upweighting to limit amplification;
- `q75_up_cap`: cap multipliers at the 75th percentile of active multipliers.

Best group-level results:

| mechanism | setting | AC@1 | MRR | AC@3 | AC@5 | interpretation |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| group median | alpha `0.30` | 0.791139 | 0.870225 | 0.945851 | 0.974684 | better than direct decimal |
| group mean | alpha `0.30` | 0.793249 | 0.873202 | 0.951477 | 0.981716 | improves MRR/AC@5 |
| group max | two-sided alpha `0.20` | 0.797468 | 0.874584 | 0.946554 | 0.978903 | best AC@1 near miss |
| group max | two-sided alpha `0.25` | 0.796062 | 0.874992 | 0.951477 | 0.979606 | better MRR |
| group max | p25 down-only alpha `0.30` | 0.796765 | 0.875511 | 0.948664 | 0.978903 | best MRR near miss |

The `group_max + two_sided alpha=0.20` candidate transformed the visible decimal ladder into approximate effective weights:

| priority | visible decimal | effective weight |
| --- | ---: | ---: |
| BACKGROUND | 1 | 0.7097 |
| BASELINE | 1 | 0.7126 |
| SUPPORT | 1 | 0.8371 |
| LOCAL | 2 | 1.8772 |
| HIGH | 5 | 5.6430 |
| ROOT | 10 | 17.4534 |
| CRITICAL | 15 | 18.9062 |

This got close, but not enough. Compared with current, it had:

| delta type | cases |
| --- | ---: |
| regressed_from_hit1 | 23 |
| improved_to_hit1 | 18 |
| net top-1 loss | 5 |

Regressed contribution summary for candidate top1 minus GT:

| priority | mean diff | median diff | interpretation |
| --- | ---: | ---: | --- |
| CRITICAL | 13.6641 | 16.8210 | status/code evidence often boosted wrong top1 |
| LOCAL | 5.4265 | 8.3433 | local trace self-duration victim symptoms too strong |
| SUPPORT | -1.4338 | -2.0621 | GT often had more support than wrong top1 |
| ROOT | -0.0404 | 0.0000 | root signal did not explain most remaining regressions |

Interpretation:

Scale compensation helps because it corrects raw magnitude mismatch. It still fails to recover all top-1 cases because unrestricted compensation can over-amplify small-scale high/critical/local propagation symptoms.

## What Is Rank Fusion?

Rank fusion combines multiple ranked lists instead of trusting one numeric weight setting.

The motivation was robustness:

```text
If no single priority ladder is fully reliable, rank services by consensus across several plausible ladders.
```

Variants tested:

- `zscore`: per-case z-score normalize each variant's service scores, then sum;
- `minmax`: per-case min-max normalize scores, then sum;
- `rank_rrf`: reciprocal rank fusion, `1 / (rank + k)`, with `k=5`;
- `rank_borda`: Borda-style score from rank position.

Severity variants used for the main rank-fusion experiment:

```text
gmax_two_0.15
gmax_two_0.20
gmax_two_0.25
gmax_two_0.30
gmax_down_p25_0.20
gmax_down_p25_0.25
gmax_down_p25_0.30
gmax_down_p25_0.35
gmax_sqrt_mean_0.20
gmax_sqrt_mean_0.25
gmax_sqrt_mean_0.30
gmax_sqrt_mean_0.35
gmax_sqrt_mean_0.40
gmean_two_0.25
gmean_two_0.30
gmean_two_0.35
gmean_two_0.40
```

Best rank fusion results:

| set | method | variants | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `two_015_025` | `rank_rrf` | 3 | 0.797468 | 0.874605 | 0.946554 | 0.979606 |
| `two_015_025` | `rank_borda` | 3 | 0.797468 | 0.874596 | 0.946554 | 0.979606 |
| `two_015_030` | `zscore` | 4 | 0.796765 | 0.874480 | 0.949367 | 0.978903 |
| `top_near` | `rank_borda` | 4 | 0.796062 | 0.875300 | 0.951477 | 0.978903 |
| `all_gmax_two_down` | `rank_borda` | 8 | 0.796062 | 0.874787 | 0.950070 | 0.978903 |

Conclusion:

Rank fusion improved robustness and MRR/AC@3/AC@5 in some settings, but did not recover accepted AC@1. The remaining AC@1 boundary cases need the nonlinear diagnostic severity separation, not only consensus.

## Other Robustness Mechanisms Tested

| mechanism | representative setting | AC@1 | MRR | interpretation |
| --- | --- | ---: | ---: | --- |
| case feature p95 normalization | decimal ladder, per-feature case p95 | 0.523910 | 0.706148 | Removes useful magnitude information. |
| feature rank normalization | decimal ladder, per-feature rank | 0.434599 | 0.655407 | Priority order cannot rescue rank-only feature evidence. |
| global unlabeled scale compensation | decimal + max-scale alpha `0.25` | 0.796062 | 0.874992 | Close on MRR, still lower AC@1. |
| case priority-group calibration | decimal + mean-scale alpha `0.1` | 0.793249 | 0.873004 | Helps but does not recover accepted AC@1. |
| context cap / low-priority cap | cap context by strong evidence | 0.414909 | 0.575017 | Too harsh; context evidence is necessary. |
| generic ladder ensemble | decimal + power2 + linear + integer-best | 0.767932 | 0.856877 | Generic-only consensus remains below current. |
| current-neighbor ensemble | `HIGH=6`, `CRITICAL=16`, `ROOT in 8..11` | 0.800985 | 0.874399 | Stable for ROOT only; still relies on calibrated low/high/critical. |
| mixed small interval ensemble | current + generic nearby ladders | 0.793952 | 0.872855 | Robust but loses top-1. |
| lexicographic priority-only | priority tuple, no numeric ladder | 0.394515 | 0.584970 | Pure priority ordering is insufficient. |

## Formula Ladder Experiments

The accepted code synthesizes a nonlinear curve from priority-tier topology.

Reweight commands:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_FORMULA_TRIANGULAR \
  --weights 0,0.75,1,1.25,1.5,6,10,15 \
  --dataset rcabench \
  --force

uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_FORMULA_TRIANGULAR16 \
  --weights 0,0.75,1,1.25,1.5,6,10,16 \
  --dataset rcabench \
  --force

uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight \
  --cache FW_FEATURE_CACHE_BASE \
  --version FW_REWEIGHT_FORMULA_DECIMAL_LOW_TRI \
  --weights 0,1,1,1,2,6,10,15 \
  --dataset rcabench \
  --force
```

Results:

| version | ladder | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: |
| `FW_REWEIGHT_FORMULA_TRIANGULAR` | `0,0.75,1,1.25,1.5,6,10,15` | 0.795359 | 0.871761 | 0.940225 | 0.976793 |
| `FW_REWEIGHT_FORMULA_TRIANGULAR16` | `0,0.75,1,1.25,1.5,6,10,16` | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| `FW_REWEIGHT_FORMULA_DECIMAL_LOW_TRI` | `0,1,1,1,2,6,10,15` | 0.779887 | 0.865499 | 0.945851 | 0.977496 |

The `next_power_of_two(ROOT)` critical tier is necessary for exact accepted AC@1 under the current scorer.

## Accepted Final Experiment

Implementation change:

```text
Remove FEATURE_PRIORITY_WEIGHTS.
Add _synthesize_feature_priority_ladder().
FEATURE_WEIGHTS = _feature_weights_from_priorities(FEATURE_PRIORITIES)
```

Validation commands:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version FW_PRIORITY_SYNTH_LADDER --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version FW_PRIORITY_SYNTH_LADDER --source FW_PRIORITY_SYNTH_LADDER --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old FW_PRIORITY_PRIOR --new FW_PRIORITY_SYNTH_LADDER --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

Results:

| version | total | error | AC@1 | MRR | AC@3 | AC@5 | case delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `FW_PRIORITY_PRIOR` | 1422 | 0 | 0.800985 | 0.874517 | 0.942335 | 0.975387 | baseline |
| `FW_PRIORITY_SYNTH_LADDER` | 1422 | 0 | 0.800985 | 0.874517 | 0.942335 | 0.975387 | all 1422 unchanged |

Guard:

```text
No high-risk overfitting warnings.
```

Medium guard warnings are existing package/documentation literals related to `rcabench_platform`, not label leakage or case/service hardcoding.

## Final Interpretation

What we can claim:

```text
The method does not depend on exposing hand-written per-feature float weights.
Feature knowledge is represented as ordinal SRE diagnostic priority.
A deterministic nonlinear severity ladder is synthesized from the priority-tier topology.
The nonlinear separation is what matters, not manually assigning a precise float to each feature.
```

What we should not claim:

```text
Any monotonic numeric values work if used directly as linear weights.
```

The direct `0,1,1,1,2,5,10,15` ladder lost about `46` top-1 hits versus the accepted synthesized ladder. It is acceptable as a displayed ordinal severity ID, but not as the direct scorer weight.

## BASE_FEATURE_NAMES Ablation Summary

Detailed record: `docs/EvidRank_evolve/FW_FEATURE_ABLATION_iteration.md`

Artifacts:

```text
output/rcabench-platform-v2/evolve_reweights/FW_FEATURE_ABLATION_SYNTH_LADDER/
```

The ablation used the same `FW_FEATURE_CACHE_BASE` raw feature cache and the accepted synthesized ladder. It evaluated:

- leave-one-feature-out;
- single-feature-only;
- priority tier ablations;
- modality ablations;
- feature-family ablations;
- targeted combined removals;
- label-guided offline greedy backward elimination.

### Most Useful Features In Current Scorer

These features have the largest positive marginal contribution. Removing them causes the largest AC@1 drop:

| feature removed | AC@1 after removal | delta AC@1 | interpretation |
| --- | ---: | ---: | --- |
| `trace_status_code_shift` | 0.715893 | -0.085091 | critical status/protocol mutation |
| `trace_self_duration_relative_shift` | 0.719409 | -0.081575 | local service-side latency mutation |
| `trace_count_rise_shift` | 0.745429 | -0.055556 | traffic/entry rise and endpoint support |
| `log_count_delta` | 0.759494 | -0.041491 | log-volume corroboration |
| `trace_endpoint_shift` | 0.760197 | -0.040788 | endpoint distribution mutation |
| `metric_max_z` | 0.764416 | -0.036568 | metric spike evidence |
| `metric_mean_z` | 0.767932 | -0.033052 | sustained metric shift |
| `log_template_delta` | 0.769339 | -0.031646 | log pattern distribution shift |
| `abnormal_trace_rows` | 0.779887 | -0.021097 | trace support / sample confidence |

Medium/weak but still positive:

```text
trace_duration_delta
trace_count_delta
metric_value_delta
metric_anomaly_count
metric_count_drop_shift
trace_count_drop_shift
```

### Harmful Feature Candidate

`trace_duration_z` is the only feature whose removal improved all headline metrics in the cache replay:

| experiment | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| all features | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| remove `trace_duration_z` | 0.816456 | 0.884112 | 0.945851 | 0.976793 |

Case movement:

| regressed_from_hit1 | improved_to_hit1 |
| ---: | ---: |
| 15 | 37 |

Interpretation: `trace_duration_z` has standalone anomaly-detection power, but in the fused RCA scorer it behaves like a propagation/victim latency symptom. `trace_duration_delta` and `trace_self_duration_relative_shift` preserve more useful latency information.

### Currently Neutral Or Unused

| feature | reason |
| --- | --- |
| `trace_error_rate` | no top-1 or MRR effect in this cache replay; single-feature-only AC@1 is `0`. |
| `log_error_rate` | no top-1 marginal effect, tiny negative MRR effect when removed. |
| `abnormal_metric_rows` | no top-1 marginal effect, tiny positive MRR when removed. |
| `topology_in_degree` | default `evidencerank` weight is `0`; no conclusion about ARC. |
| `topology_out_degree` | default `evidencerank` weight is `0`; no conclusion about ARC. |

### Group-Level Findings

| ablation | AC@1 after removal | delta AC@1 | interpretation |
| --- | ---: | ---: | --- |
| remove trace modality | 0.443741 | -0.357243 | trace is the most important modality |
| remove metric modality | 0.617440 | -0.183544 | metric is important |
| remove log modality | 0.704641 | -0.096343 | log is auxiliary but useful |
| remove BACKGROUND priority | 0.534459 | -0.266526 | background metric/log signals are collectively essential |
| remove HIGH priority | 0.689873 | -0.111111 | endpoint/count rise signals are very important |
| remove CRITICAL priority | 0.715893 | -0.085091 | status mutation is critical |
| remove LOCAL priority | 0.719409 | -0.081575 | self-duration/local latency is important |

### Greedy Backward Result

The offline greedy elimination selected exactly one improving removal:

```text
remove trace_duration_z
```

No additional single feature removal improved AC@1/MRR after that step.

No default algorithm change was made in the ablation turn. If this candidate is accepted later, it should be run as a normal versioned algorithm iteration with full eval, snapshot, summary, compare, and guard.

## Comprehensive Priority And Ladder Search

Detailed record: `docs/EvidRank_evolve/FW_PRIORITY_COMPREHENSIVE_SEARCH_iteration.md`

Dedicated case-movement and variant interpretation: `docs/EvidRank_evolve/FW_PRIORITY_VARIANTS_CASE_MOVEMENT.md`

Artifacts:

```text
output/rcabench-platform-v2/evolve_reweights/FW_PRIORITY_COMPREHENSIVE_SEARCH/
```

This experiment asked a broader question:

```text
Without changing EvidenceRank scoring logic, how far can offline label-guided search push performance
by changing only FEATURE_PRIORITIES assignments and FEATURE_PRIORITY_LADDER values?
```

Safety boundary:

- This is an offline label-guided upper-bound and sensitivity study.
- It used labels only to compute metrics and case movement.
- No default `algorithm.py` change was made.
- The best candidate should not be copied into runtime as-is without mechanism-level justification and full eval.

### Search Space

The search evaluated:

- single-feature priority reassignment across all `FeaturePriority` tiers;
- greedy coordinate search over priority assignments;
- ladder coordinate search after the greedy assignment;
- targeted combinations around previously observed weak points;
- post-analysis preset scans with clean ladders such as `0,1,1,1,2,5,10,15`;
- one-level ladder range scans to estimate AC@1 plateaus;
- key candidate case movement versus baseline.

The first search pass recorded `eval_count=1105`; the post-analysis pass added `170` replay evaluations.

### Best Offline Candidate

Best label-guided replay candidate:

```text
Priority changes:
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

| config | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| current priorities + current synthesized ladder | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| greedy priorities + current ladder | 0.830520 | 0.892995 | 0.947961 | 0.976793 |
| greedy priorities + `LOCAL=2, CRITICAL=20` | 0.839662 | 0.898061 | 0.950070 | 0.974684 |

Case movement versus baseline:

| candidate | improved_to_hit1 | regressed_from_hit1 | rank_improved | rank_regressed | unchanged |
| --- | ---: | ---: | ---: | ---: | ---: |
| disable `trace_duration_z` | 37 | 15 | 23 | 7 | 1340 |
| greedy priorities + current ladder | 61 | 19 | 54 | 31 | 1257 |
| greedy priorities + best ladder | 68 | 13 | 55 | 30 | 1256 |
| greedy priorities + clean ladder | 67 | 45 | 43 | 47 | 1220 |

### Greedy Path

| step | change | AC@1 | MRR |
| ---: | --- | ---: | ---: |
| 1 | `trace_duration_z: BASELINE -> DISABLED` | 0.816456 | 0.884112 |
| 2 | `topology_in_degree: DISABLED -> SUPPORT` | 0.821378 | 0.887160 |
| 3 | `log_count_delta: BACKGROUND -> LOCAL` | 0.826301 | 0.890430 |
| 4 | `trace_count_delta: BASELINE -> BACKGROUND` | 0.828411 | 0.891963 |
| 5 | `log_error_rate: BACKGROUND -> LOCAL` | 0.829817 | 0.892886 |
| 6 | `metric_count_drop_shift: ROOT -> HIGH` | 0.830520 | 0.892995 |
| ladder 1 | `LOCAL: 1.5 -> 2.0` | 0.836850 | 0.896024 |
| ladder 2 | `CRITICAL: 16 -> 20` | 0.839662 | 0.898061 |

The dominant single change is still disabling `trace_duration_z`. The next changes are plausible, but more label-guided: weak topology support, local log corroboration, demotion of raw trace count, and a very small one-case gain from demoting metric count drop.

### Clean Ladder Check

| assignment | ladder | AC@1 | MRR | result |
| --- | --- | ---: | ---: | --- |
| current priorities | `0,1,1,1,2,5,10,15` | 0.768636 | 0.858448 | loses many top-1 hits |
| disable `trace_duration_z` only | `0,1,1,1,2,5,10,15` | 0.796062 | 0.874065 | still below current |
| greedy priorities | `0,1,1,1,2,5,10,15` | 0.816456 | 0.884331 | better, but below best |
| greedy priorities | `0,0.75,1,1.25,2,6,10,20` | 0.839662 | 0.898061 | best offline candidate |

This answers the priority-only question:

```text
FeaturePriority ordering carries real diagnostic information,
but ordering alone is not sufficient under the current linear scorer.
The nonlinear spacing between tiers still decides many boundary cases.
```

### Ladder Plateau Findings

For current priorities and the accepted ladder:

| tier | exact best values | within one-case values | interpretation |
| --- | --- | --- | --- |
| BACKGROUND | 0.75 | 0.75 | highly sensitive |
| BASELINE | 1 | 1 | moderately sensitive |
| SUPPORT | 1.25 | 1.25 | mildly sensitive |
| LOCAL | 1.5 | 1.5 | sensitive |
| HIGH | 6 | 6 | sensitive |
| ROOT | 8, 10 | 8, 10, 12, 14, 16 | tolerant |
| CRITICAL | 16 | 16 | sensitive |

For greedy priorities and the best ladder:

| tier | exact best values | within one-case values | interpretation |
| --- | --- | --- | --- |
| BACKGROUND | 0.75 | 0.75 | still sensitive |
| BASELINE | 1 | 1 | stable but exact |
| SUPPORT | 1.25 | 1.25 | stable but exact |
| LOCAL | 2 | 2, 2.25 | modest plateau |
| HIGH | 6 | 6 | still sensitive |
| ROOT | 6, 8, 10, 12, 14, 16, 20 | same | irrelevant after demoting the only root feature |
| CRITICAL | 20 | 20 | still sensitive |

So the search did not prove that exact numeric values are irrelevant. It showed a narrower claim:

```text
Some tiers, especially ROOT after the greedy reassignment, become insensitive.
But BACKGROUND/HIGH/CRITICAL remain sensitive because large-scale context features and small-scale root-specific features compete in one linear sum.
```

### Mechanism Takeaways

Most defensible mechanism:

```text
Raw global trace-duration extremeness behaves like a propagation/victim latency symptom.
It should be gated, downweighted, or replaced by a local/self-duration and topology-contrast latency signal.
```

Secondary mechanisms:

- Raw trace count deltas are propagation-prone and benefit from demotion.
- Logs can be useful local corroboration after victim-latency evidence is controlled.
- Weak topology support can help default `evidencerank`, but ARC has separate topology/reliability logic, so this should not be generalized blindly.
- `metric_count_drop_shift: ROOT -> HIGH` is too small a gain to trust as a standalone conclusion.

Recommended next accepted-code experiment:

```text
Do not directly paste the best label-guided assignment into algorithm.py.
Instead, test a mechanism version that suppresses or gates `trace_duration_z` using unsupervised agreement:
self-duration, endpoint/status mutation, log corroboration, or trace-direction neighbor contrast.
```

## Appendix A: Reproduce Scale Compensation Scans

This script reproduces the main scale compensation variants from the cached feature matrix. It is intentionally offline and reads labels only for metric reporting.

```bash
uv run --package evidencerank python - <<'PY'
from pathlib import Path
import sys, math
import numpy as np
import pandas as pd

repo = Path("/home/ljw/paper/aegis/rca-algo-contrib")
sys.path.insert(0, str(repo / "VibeResearchTools"))

import evidrank_feature_cache as fc
from evidencerank.algorithm import BASE_FEATURE_NAMES, FEATURE_PRIORITIES

features, edges = fc._load_cache("FW_FEATURE_CACHE_BASE")
labels = fc._load_labels(
    repo / "data/rcabench-platform-v2/meta/rcabench-csv/labels.csv",
    "rcabench",
)
cached_cases = fc._prepare_cached_cases(features, edges)

levels = np.asarray([int(FEATURE_PRIORITIES[name]) for name in BASE_FEATURE_NAMES])
ladder = (0, 1, 1, 1, 2, 5, 10, 15)
raw = np.asarray(
    [ladder[int(FEATURE_PRIORITIES[name])] for name in BASE_FEATURE_NAMES],
    dtype=float,
)

scales = []
for name in BASE_FEATURE_NAMES:
    values = features[name].to_numpy(float)
    positive = values[np.isfinite(values) & (values > 0)]
    if len(positive) > 1:
        scale = float(np.percentile(positive, 95))
    elif len(positive) == 1:
        scale = float(positive[0])
    else:
        scale = 1.0
    scales.append(scale if math.isfinite(scale) and scale > 0 else 1.0)
scales = np.asarray(scales, dtype=float)

def metrics(weights: np.ndarray) -> fc.Metrics:
    rows = []
    weights = weights.astype(np.float32)
    for case in cached_cases:
        scores = fc._score_case(case.services, case.matrix, case.trace_edges, weights)
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        gt = labels.get(case.datapack, set())
        best = None
        for rank, (service, _score) in enumerate(ranked, start=1):
            if service in gt:
                best = rank
                break
        rows.append({
            "best_rank": best if best is not None else pd.NA,
            "mrr": 1 / best if best else 0,
            "hit@1": best == 1,
            "hit@3": best is not None and best <= 3,
            "hit@5": best is not None and best <= 5,
            "missing_output": False,
        })
    return fc._metrics(pd.DataFrame(rows))

rows = []

# Feature-wise p95 compensation.
reference = float(np.median(scales[scales > 0]))
for alpha in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.75, 1.0]:
    weights = raw * ((reference / scales) ** alpha)
    weights[raw <= 0] = 0
    metric = metrics(weights)
    rows.append({
        "method": "feature_p95",
        "alpha": alpha,
        "ac1": metric.ac1,
        "mrr": metric.mrr,
        "ac3": metric.ac3,
        "ac5": metric.ac5,
    })

# Priority-group compensation.
for aggregate_name, aggregate_fn in [
    ("group_median", np.median),
    ("group_mean", np.mean),
    ("group_max", np.max),
]:
    group_scale = {}
    for level in sorted(set(levels)):
        group_scale[level] = float(aggregate_fn(scales[levels == level]))
    group_vector = np.asarray(
        [group_scale[int(FEATURE_PRIORITIES[name])] for name in BASE_FEATURE_NAMES],
        dtype=float,
    )
    active_group_values = np.asarray(
        [value for level, value in group_scale.items() if level != 0 and value > 0],
        dtype=float,
    )
    for reference_name, reference in {
        "median": float(np.median(active_group_values)),
        "mean": float(np.mean(active_group_values)),
        "p25": float(np.percentile(active_group_values, 25)),
    }.items():
        for mode in ["two_sided", "down_only", "sqrt_up_cap", "q75_up_cap"]:
            for alpha in [0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]:
                multiplier = (reference / group_vector) ** alpha
                if mode == "down_only":
                    multiplier = np.minimum(1.0, multiplier)
                elif mode == "sqrt_up_cap":
                    multiplier = np.where(multiplier > 1.0, np.sqrt(multiplier), multiplier)
                elif mode == "q75_up_cap":
                    cap = float(np.percentile(multiplier[raw > 0], 75))
                    multiplier = np.minimum(multiplier, cap)
                weights = raw * multiplier
                weights[raw <= 0] = 0
                metric = metrics(weights)
                rows.append({
                    "method": f"{aggregate_name}_{reference_name}_{mode}",
                    "alpha": alpha,
                    "ac1": metric.ac1,
                    "mrr": metric.mrr,
                    "ac3": metric.ac3,
                    "ac5": metric.ac5,
                })

result = pd.DataFrame(rows).sort_values(
    ["ac1", "mrr", "ac3", "ac5"],
    ascending=[False, False, False, False],
)
print(result.head(40).to_string(index=False, float_format=lambda value: f"{value:.6f}"))
PY
```

## Appendix B: Reproduce Rank Fusion Scans

This script reproduces the main severity-family rank fusion experiment.

```bash
uv run --package evidencerank python - <<'PY'
from pathlib import Path
import sys, math
import numpy as np
import pandas as pd

repo = Path("/home/ljw/paper/aegis/rca-algo-contrib")
sys.path.insert(0, str(repo / "VibeResearchTools"))

import evidrank_feature_cache as fc
from evidencerank.algorithm import BASE_FEATURE_NAMES, FEATURE_PRIORITIES

features, edges = fc._load_cache("FW_FEATURE_CACHE_BASE")
labels = fc._load_labels(
    repo / "data/rcabench-platform-v2/meta/rcabench-csv/labels.csv",
    "rcabench",
)
cases = fc._prepare_cached_cases(features, edges)

levels = np.asarray([int(FEATURE_PRIORITIES[name]) for name in BASE_FEATURE_NAMES])
ladder = (0, 1, 1, 1, 2, 5, 10, 15)
raw = np.asarray([ladder[int(FEATURE_PRIORITIES[name])] for name in BASE_FEATURE_NAMES], dtype=float)

scales = []
for name in BASE_FEATURE_NAMES:
    values = features[name].to_numpy(float)
    positive = values[np.isfinite(values) & (values > 0)]
    if len(positive) > 1:
        scale = float(np.percentile(positive, 95))
    elif len(positive) == 1:
        scale = float(positive[0])
    else:
        scale = 1.0
    scales.append(scale if math.isfinite(scale) and scale > 0 else 1.0)
scales = np.asarray(scales, dtype=float)

group_scales = {
    "max": {level: float(np.max(scales[levels == level])) for level in sorted(set(levels))},
    "mean": {level: float(np.mean(scales[levels == level])) for level in sorted(set(levels))},
}

def make_weights(aggregate: str, alpha: float, mode: str, reference_mode: str) -> np.ndarray:
    group_scale = group_scales[aggregate]
    active_values = np.asarray(
        [value for level, value in group_scale.items() if level != 0 and value > 0],
        dtype=float,
    )
    if reference_mode == "median":
        reference = float(np.median(active_values))
    elif reference_mode == "mean":
        reference = float(np.mean(active_values))
    elif reference_mode == "p25":
        reference = float(np.percentile(active_values, 25))
    else:
        raise ValueError(reference_mode)

    group_vector = np.asarray(
        [group_scale[int(FEATURE_PRIORITIES[name])] for name in BASE_FEATURE_NAMES],
        dtype=float,
    )
    multiplier = (reference / group_vector) ** alpha
    if mode == "down":
        multiplier = np.minimum(1.0, multiplier)
    elif mode == "sqrt":
        multiplier = np.where(multiplier > 1.0, np.sqrt(multiplier), multiplier)
    elif mode != "two":
        raise ValueError(mode)

    weights = raw * multiplier
    weights[raw <= 0] = 0
    return weights.astype(np.float32)

def score_all(weights: np.ndarray) -> dict[str, dict[str, float]]:
    result = {}
    for case in cases:
        result[case.datapack] = fc._score_case(case.services, case.matrix, case.trace_edges, weights)
    return result

variants = []
for alpha in [0.15, 0.2, 0.25, 0.3]:
    variants.append((f"gmax_two_{alpha}", make_weights("max", alpha, "two", "median")))
for alpha in [0.2, 0.25, 0.3, 0.35]:
    variants.append((f"gmax_down_p25_{alpha}", make_weights("max", alpha, "down", "p25")))
for alpha in [0.2, 0.25, 0.3, 0.35, 0.4]:
    variants.append((f"gmax_sqrt_mean_{alpha}", make_weights("max", alpha, "sqrt", "mean")))
for alpha in [0.25, 0.3, 0.35, 0.4]:
    variants.append((f"gmean_two_{alpha}", make_weights("mean", alpha, "two", "median")))

score_maps = {name: score_all(weights) for name, weights in variants}

sets = {
    "two_015_025": ["gmax_two_0.15", "gmax_two_0.2", "gmax_two_0.25"],
    "two_015_030": ["gmax_two_0.15", "gmax_two_0.2", "gmax_two_0.25", "gmax_two_0.3"],
    "top_near": ["gmax_two_0.2", "gmax_two_0.25", "gmax_down_p25_0.3", "gmax_sqrt_mean_0.4"],
    "all_gmax_two_down": [name for name, _weights in variants if name.startswith("gmax_two") or name.startswith("gmax_down")],
    "all": [name for name, _weights in variants],
}

def evaluate(names: list[str], method: str) -> fc.Metrics:
    rows = []
    selected = [score_maps[name] for name in names]
    for case in cases:
        accum = {service: 0.0 for service in case.services}
        for score_map in selected:
            scores = np.asarray([score_map[case.datapack].get(service, 0.0) for service in case.services], dtype=float)
            if method == "zscore":
                std = float(np.std(scores))
                mean = float(np.mean(scores))
                normalized = (scores - mean) / (std + 1e-9) if std > 0 else scores * 0
            elif method == "minmax":
                lo = float(np.min(scores))
                hi = float(np.max(scores))
                normalized = (scores - lo) / (hi - lo + 1e-9)
            elif method == "rank_rrf":
                order = np.argsort(-scores, kind="mergesort")
                normalized = np.zeros_like(scores)
                for rank, index in enumerate(order, start=1):
                    normalized[index] = 1.0 / (rank + 5.0)
            elif method == "rank_borda":
                order = np.argsort(scores, kind="mergesort")
                normalized = np.empty_like(scores)
                normalized[order] = np.arange(1, len(scores) + 1) / len(scores)
            else:
                raise ValueError(method)
            for service, value in zip(case.services, normalized):
                accum[service] += float(value)

        ranked = sorted(accum.items(), key=lambda item: item[1], reverse=True)
        gt = labels.get(case.datapack, set())
        best = None
        for rank, (service, _score) in enumerate(ranked, start=1):
            if service in gt:
                best = rank
                break
        rows.append({
            "best_rank": best if best is not None else pd.NA,
            "mrr": 1 / best if best else 0,
            "hit@1": best == 1,
            "hit@3": best is not None and best <= 3,
            "hit@5": best is not None and best <= 5,
            "missing_output": False,
        })
    return fc._metrics(pd.DataFrame(rows))

rows = []
for set_name, names in sets.items():
    for method in ["zscore", "minmax", "rank_rrf", "rank_borda"]:
        metric = evaluate(names, method)
        rows.append({
            "set": set_name,
            "method": method,
            "n": len(names),
            "ac1": metric.ac1,
            "mrr": metric.mrr,
            "ac3": metric.ac3,
            "ac5": metric.ac5,
        })

result = pd.DataFrame(rows).sort_values(["ac1", "mrr"], ascending=[False, False])
print(result.to_string(index=False, float_format=lambda value: f"{value:.6f}"))
PY
```

## Appendix C: Full Eval And Report Artifacts

The accepted full-eval artifacts were generated with:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch \
  -a evidencerank \
  -d rcabench \
  --clear \
  --use-cpus 48

uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot \
  --version FW_PRIORITY_SYNTH_LADDER \
  --algorithm evidencerank \
  --dataset rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize \
  --version FW_PRIORITY_SYNTH_LADDER \
  --source FW_PRIORITY_SYNTH_LADDER \
  --algorithm evidencerank \
  --dataset rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare \
  --old FW_PRIORITY_PRIOR \
  --new FW_PRIORITY_SYNTH_LADDER \
  --algorithm evidencerank \
  --dataset rcabench
```

Generated docs:

```text
docs/EvidRank_evolve/FW_PRIORITY_SYNTH_LADDER_iteration.md
docs/EvidRank_evolve/FW_PRIORITY_SYNTH_LADDER_summary.md
docs/EvidRank_evolve/compare_FW_PRIORITY_PRIOR_vs_FW_PRIORITY_SYNTH_LADDER.md
docs/EvidRank_evolve/FW_PRIORITY_LADDER_ABLATION_iteration.md
```
