# EvidenceRank FW_PRIORITY_LADDER_ABLATION Iteration

- Created: 2026-06-03T23:40:28+08:00
- Hypothesis: 比较线性序数、二进制层级和十进制 SRE severity ladder，分析 FEATURE_PRIORITY_WEIGHTS 数值区间对默认 EvidenceRank 排名稳定性的影响
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files changed:
  - `VibeResearchTools/evidrank_feature_cache.py`
  - `VibeResearchTools/README.md`
  - temporary algorithm ladder edits were used for full-eval ablations, then restored to the current priority ladder.
- General RCA mechanism being tested: whether an ordinal SRE priority prior can use cleaner-looking ladder values without materially changing root-cause ranking, and whether raw pre-fusion feature matrices can be cached for fast offline reweighting.
- Why this should transfer beyond RCABench: the feature cache stores only raw service-level RCA evidence generated from metrics/traces/logs/topology. Labels are used only by offline `reweight` / `scan` reports to evaluate candidate ladders.

## Baseline

- Baseline snapshot: `FW_PRIORITY_PRIOR`
- Baseline metrics: AC@1 `0.800985`, MRR `0.874517`, AC@3 `0.942335`, AC@5 `0.975387`, error `0`.
- Numeric baseline reference: `FW_NUMERIC_BASELINE`, AC@1 `0.802391`, MRR `0.875337`.
- Key weak groups are unchanged from the default EvidenceRank reports; this iteration is about prior-ladder sensitivity, not a new RCA signal.

## Planned Change

- Minimal algorithm change: none accepted into ranking logic. Add an offline feature-cache tool that dumps one raw feature matrix and replays `_heuristic_scores`, adaptive modality weights, endpoint gate, and parent context for arbitrary ladders.
- Expected metric movement: candidate ladders may change rankings substantially because the scorer is a weighted sum before endpoint gating and parent-context smoothing. Compressing strong causal evidence makes propagation/volume/background features competitive in close cases.
- Known regression risk: any ladder that raises background/support/local evidence or lowers `HIGH`/`ROOT`/`CRITICAL` relative to `BASELINE` can promote victim or high-traffic services over true roots.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py dump --version FW_FEATURE_CACHE_BASE --dataset rcabench --workers 48
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py reweight --cache FW_FEATURE_CACHE_BASE --version FW_REWEIGHT_CURRENT --preset current --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_feature_cache.py scan --cache FW_FEATURE_CACHE_BASE --version FW_SCAN_CURRENT_LOW_STRONG_RANGE --dataset rcabench --background 0.75 --baseline 1 --support 1.25 --local 1.5 --high-values 4,5,6,7,8 --root-values 8,9,10,11,12 --critical-values 12,14,15,16,18,20
```

## Results

- Feature cache: `output/rcabench-platform-v2/evolve_feature_cache/FW_FEATURE_CACHE_BASE/`, `1422` cases, `69684` service rows, `0` errors.
- Offline reweight reproduced full-eval metrics exactly for known ladders:

| ladder | weights | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: |
| current | `0,0.75,1,1.25,1.5,6,10,16` | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| linear_0_7 | `0,1,2,3,4,5,6,7` | 0.671589 | 0.789295 | 0.886076 | 0.945148 |
| power2_tier | `0,1,1,1,2,4,8,16` | 0.756681 | 0.851812 | 0.941632 | 0.973980 |
| decimal_1_2_5_10_15 | `0,1,1,1,2,5,10,15` | 0.768636 | 0.858448 | 0.942335 | 0.975387 |

### Strong-Layer Range With Current Low Layers

Fixed `BACKGROUND=0.75`, `BASELINE=1`, `SUPPORT=1.25`, `LOCAL=1.5`.

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

No-top1-loss region in this grid: `HIGH=6`, `CRITICAL=16`, and `ROOT` approximately `8..11`. `ROOT=12` loses one top-1 case. `CRITICAL=18` loses two top-1 cases but improves AC@3.

### Integer Low-Layer Scan

Fixed `BACKGROUND=1`, `BASELINE=1`, `SUPPORT=1`, `LOCAL=2`.

| varied level | best value in grid | best AC@1 | best MRR |
| --- | ---: | ---: | ---: |
| HIGH | 8 | 0.791139 | 0.871603 |
| ROOT | 10/11/12 | 0.791139 | 0.871603 |
| CRITICAL | 20 | 0.791139 | 0.871603 |

Best full ladder in this grid: `0,1,1,1,2,8,10,20`, AC@1 `0.791139`, MRR `0.871603`, AC@3 `0.949367`, AC@5 `0.981013`. This is 14 fewer top-1 hits than current, despite better AC@3/AC@5.

### Low-Layer Range With Current Strong Layers

Fixed `HIGH=6`, `ROOT=10`, `CRITICAL=16`, `BASELINE=1`.

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

Only `BACKGROUND=0.75`, `SUPPORT=1.25`, `LOCAL=1.5` preserved the current AC@1 in this coarse grid.

## Case Deltas

- Linear `0..7`: large regression, `227` cases regressed from hit@1 and `43` improved to hit@1 versus `FW_PRIORITY_PRIOR`.
- Power-of-two tier: moderate regression, `90` cases regressed from hit@1 and `27` improved to hit@1 versus `FW_PRIORITY_PRIOR`.
- Generic integer low-layer scan shows a tradeoff: fewer top-1 hits but slightly higher AC@3/AC@5 for the best high-layer settings.

## Decision

- Accept / reject / keep for later: accept the feature-cache/reweight tooling; reject replacing current ladder with linear, power-of-two, or decimal integer ladders as default.
- Reason: the current ladder is not arbitrary-looking by accident; it defines narrow ranking margins between root-specific evidence and propagation symptoms. `0..7` compresses `CRITICAL/BASELINE` from `16` to `3.5`, `ROOT/BASELINE` from `10` to `3`, and raises support/background evidence, causing large top-1 loss.
- Answer to the interval question: yes, the new cache can analyze candidate intervals without full eval. In the tested grid, `ROOT` is relatively tolerant (`8..11` with current low/critical/high), while `HIGH`, `CRITICAL`, `BACKGROUND`, and `LOCAL` are sensitive.
- Presentation implication: a cleaner paper story should not claim these values are interchangeable ordinal IDs. A defensible wording is "SRE feature-priority prior with a calibrated severity ladder"; the ladder can be justified by offline sensitivity analysis or learned from unlabeled incidents.
- Next smallest general step: run a narrower continuous/offline search around the current ladder, then either report stability intervals or learn the ladder with a label-free objective constrained by these no-regression bands.
