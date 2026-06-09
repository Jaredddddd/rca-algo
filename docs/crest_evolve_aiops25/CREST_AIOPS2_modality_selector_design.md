# CREST_AIOPS2 Modality Selector Design

## Goal

Design a general, unsupervised modality-adaptive CREST mechanism that can run
on AIOps25 and RCABench without labels, dataset identity, service-name rules,
or runtime teachers.

The mechanism should generalize the accepted CREST_AIOPS1 trace-confidence gate:
instead of only deciding when trace structural support is weak, estimate
incident-local reliability for metric, log, and trace, then use those
confidence values to blend or cap modality contributions.

## Motivation From SimpleRCA

SimpleRCA is strong on AIOps25 because its current Nezha-style implementation
uses independent metric/log/trace detectors and bounded top-5 voting. This
prevents a single unreliable trace surface from dominating the final rank and
slightly favors metric evidence in resource-like incidents.

The parts that can transfer to CREST:

- rank-bounded modality fusion;
- metric/log ownership under weak trace;
- incident-local confidence instead of fixed global modality weights;
- entry-path victim control from telemetry structure.

The parts that must not transfer:

- service-name suppression such as skipping a named entry service;
- dataset adapter branches as algorithmic behavior;
- fixed fallback from `crest` to `crest_metric_log`;
- using SimpleRCA output as a runtime teacher or tie breaker.

## Runtime Signals

All signals are computed from normal/abnormal raw telemetry frames and CREST's
own case-local feature matrix.

Metric reliability:

- service coverage and sample count;
- normal-vs-abnormal shift strength using robust quantiles or MAD;
- top candidate selectivity and top-vs-second gap;
- concentration by resource / instance / KPI identity when provenance columns
  exist, with no-op fallback when they do not;
- agreement with log top-k or root-local trace mutation.

Log reliability:

- service coverage and abnormal log volume;
- error/template/level shift selectivity;
- normal-vs-abnormal count or ratio shift;
- top candidate concentration without allowing a single noisy log burst to
  dominate;
- agreement with metric top-k or trace mutation top-k.

Trace reliability:

- abnormal trace service coverage;
- top row share and service distribution entropy;
- status/path/method/duration mutation selectivity;
- candidate overlap between trace-covered services and metric/log evidence;
- propagation-victim risk from high traffic share, high fan-in/fan-out,
  downstream symptom breadth, and weak root-owned local evidence.

Cross-modal reliability:

- top-k overlap among modalities;
- rank stability under simple bootstrap or feature-family dropout;
- Pareto support: a candidate supported by two moderately reliable modalities
  should not be suppressed by a single low-confidence modality.

## Fusion Design

1. Build per-modality CREST family scores for every service:
   metric-local, log-local, trace-mutation, trace-propagation, and trace-graph
   support.
2. Convert each modality score to a within-case robust rank statistic, such as
   percentile rank or winsorized z-score. This keeps one modality's raw scale
   from dominating another.
3. Compute unsupervised modality confidence values in `[0, 1]` from coverage,
   selectivity, normal-abnormal shift, and cross-modal agreement.
4. Use bounded confidence weights:
   keep a small floor so absent/noisy modalities do not implicitly erase strong
   candidates; cap trace structural support when trace confidence is weak; keep
   full trace support when coverage and mutation selectivity are strong.
5. Fuse using rank-bounded addition or a confidence-weighted Borda score, then
   retain CREST's existing structural arbitration only when the trace confidence
   gate permits it.

Candidate absence is not negative evidence. If a service is absent from trace
but has strong metric/log local ownership, it should remain competitive under
weak trace confidence. Conversely, when metric/log are weak but trace mutation
is selective and broad enough, trace should still win.

## Suggested Registries

- `crest`: accepted default after validation.
- `crest_modality_confidence`: candidate ablation with full metric/log/trace
  confidence fusion.
- `crest_no_reliability`: no-confidence ablation, already added in
  CREST_AIOPS1.
- Optional narrow ablations:
  `crest_trace_confidence`, `crest_metric_log_confidence`,
  `crest_resource_provenance`.

## Parallel Validation Plan

AIOps25 and RCABench evaluations are independent and should be launched in
parallel. At the agent/tool level, use parallel tool calls. In shell form, the
same idea is:

```bash
export LOGURU_LEVEL=WARNING
export AIOPS_DATASET=aiopschallenge2025_rcabench_service
export RCABENCH_DATASET=rcabench

uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_modality_confidence \
  -d "$AIOPS_DATASET" --clear --use-cpus 16 &
pid_aiops=$!

uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_modality_confidence \
  -d "$RCABENCH_DATASET" --clear --use-cpus 32 &
pid_rcabench=$!

wait "$pid_aiops" "$pid_rcabench"
```

After both complete, run perf-report, snapshot, summarize, and compare for both
datasets. Do not claim an accepted version unless AIOps25 has `total=230`,
RCABench has `total=1422`, both have `error=0`, and RCABench does not regress
relative to a freshly verified baseline.

## Acceptance Standard

- No labels, injection metadata, previous output, perf report, historical
  ranking, ground truth, or `conclusion.parquet` in runtime logic.
- No dataset, datapack, service, fault, or split hardcoding.
- AIOps25 AC@1 and/or MRR improves over CREST_AIOPS1.
- RCABench AC@1, MRR, AC@3, and AC@5 do not drop below the fresh baseline.
- Compare documents show `improved_to_hit1`, `regressed_from_hit1`,
  `rank_improved`, and `rank_regressed` for both datasets.
- Ablations demonstrate that the modality selector adds value beyond the
  trace-only CREST_AIOPS1 gate.
