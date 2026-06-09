# CREST_AIOPS1 Iteration

## General Hypothesis

AIOps25 and RCABench differ mainly in incident-local telemetry reliability,
not in a dataset-specific service or fault identity. Full CREST should keep
trace/topology support when trace looks root-aligned, but cap structural trace
support when trace has narrow service coverage, high traffic concentration, and
weak selective mutation while metric/log evidence names a stronger local root
candidate.

The first implementation target is a label-free telemetry reliability gate:
estimate case-local trace structural confidence from raw normal/abnormal trace
coverage, trace volume concentration, selective trace mutation, and overlap
with metric/log candidate evidence. Use that confidence to bound graph
counterfactual support instead of switching to a fixed metric-log fallback.

## Fresh Baseline

Fresh verification completed on 2026-06-08 against the current working tree.

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.334783 | 0.503603 | 0.600000 | 0.669565 |
| rcabench | crest | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

Baseline snapshots and summaries:

- `CREST_AIOPS1_BASE_AIOPS25`: `total=230`, `error=0`,
  `AC@1=0.334783`, `MRR=0.503603`, `AC@3=0.600000`, `AC@5=0.669565`.
- `CREST_AIOPS1_BASE_RCABENCH`: `total=1422`, `error=0`,
  `AC@1=0.800281`, `MRR=0.875326`, `AC@3=0.944444`, `AC@5=0.971871`.

The previous AIOps25 `crest_metric_log` reference remains useful as offline
evidence of weak trace reliability in many incidents, but it is not a runtime
fallback or teacher.

## Failure Mechanism

Current full CREST computes local abnormality `A`, structural explanatory power
`F`, denoised support `S`, then ranks by `A * F + S`. This works on RCABench
when trace coverage and status/path/topology mutation are broad and frequently
root-owned. In AIOps25, many service-level resource, JVM, pod, or infrastructure
incidents have stronger root evidence in metric/log, while trace is often an
entry-path or key-path propagation surface with narrower candidate coverage.
Then graph `F/S` and trace row-volume evidence can promote a high-observability
victim above a metric/log-owned root.

## Offline Failcase Comparison

The following comparison used baseline outputs plus offline GT labels only for
analysis. No runtime logic reads `simplerca`, labels, output, perf, or GT.

Against `simplerca` on the 230 AIOps25 service cases:

| group | cases | GT trace covered | median trace top share | dominant CREST top1 |
| --- | ---: | ---: | ---: | --- |
| both hit@1 | 45 | 1.000 | 0.561 | checkoutservice/frontend |
| CREST-only hit@1 | 32 | 1.000 | 0.550 | frontend |
| SimpleRCA-only hit@1 | 105 | 0.343 | 0.549 | frontend |
| both miss hit@1 | 48 | 0.583 | 0.549 | frontend |
| `crest_metric_log` hit and CREST miss | 65 | 0.354 | 0.549 | frontend |

Mechanism extracted from this comparison:

- SimpleRCA wins many cases where the GT service is not covered by abnormal
  trace, while CREST is pulled to a high-volume trace service.
- CREST-only wins all have GT trace coverage, so a safe fix must not globally
  disable trace or topology.
- The reusable signal is not a service name. It is a telemetry reliability
  pattern: strong metric/log evidence outside trace coverage plus concentrated
  trace traffic implies trace is likely a symptom surface; selective trace
  mutation/propagation with candidate coverage implies trace remains useful.

Why SimpleRCA is strong on AIOps25:

- The current `simplerca` registry runs the Nezha-style implementation, which
  detects metric, log, and trace anomalies independently and combines each
  modality's top-5 by position voting. This caps any single modality's
  continuous score dominance.
- Its metric detector uses normal-window quantile thresholds and gives metric
  votes slightly higher weight. This is well aligned with AIOps25 resource,
  JVM, pod, CPU, and memory cases where local metric/log evidence often owns
  the root better than trace topology.
- Its trace and log fallback logic explicitly suppresses an entry service by
  name. That explains many AIOps25 gains, because baseline CREST often ranked
  the entry/high-volume trace surface first. This cannot be copied into CREST;
  the generalizable lesson is to identify entry-path victims from telemetry
  structure: dominant trace row share, broad downstream symptoms, weak
  root-owned metric/log evidence, and non-selective trace mutation.
- On RCABench, SimpleRCA is much weaker than CREST, so it should not be used as
  a runtime teacher or fallback. Its value is as offline evidence that
  rank-bounded modality fusion can be robust when trace reliability is weak.

## Planned Code Change

- Keep existing CREST registries runnable.
- Add a CREST-owned incident-local trace confidence calculation in
  `algorithms/evidencerank/src/evidencerank/crest.py`.
- Use only raw frames and feature matrix values already available to CREST.
- Cap or interpolate structural support when trace confidence is weak; preserve
  full structural support when trace coverage, mutation selectivity, and
  modality overlap indicate root alignment.
- Do not read labels, injection metadata, prior outputs, perf reports,
  historical rankings, ground truth, or `conclusion.parquet`.
- Do not hardcode dataset names, datapack ids, service names, fault names, or
  dataset splits.

## Validation Plan

1. Generate temporary AIOps25 labels CSV under `/tmp` for offline summaries only.
2. Run current `crest` full eval and perf-report on
   `aiopschallenge2025_rcabench_service`; confirm `total=230`, `error=0`.
3. Run current `crest` full eval and perf-report on `rcabench`; confirm
   `total=1422`, `error=0`.
4. Snapshot and summarize baselines as `CREST_AIOPS1_BASE_AIOPS25` and
   `CREST_AIOPS1_BASE_RCABENCH`.
5. Implement the telemetry reliability change.
6. Run guard and compile.
7. Run full eval and perf-report on both datasets.
8. Snapshot, summarize, and compare `CREST_AIOPS1_AIOPS25` and
   `CREST_AIOPS1_RCABENCH` against their fresh baselines.
9. Mirror generated summaries/compare documents into this directory and update
   `docs/crest_evolve_aiops25/README.md`.

## Acceptance Criteria

- Guard has no high-risk overfitting findings.
- Compile passes.
- AIOps25 full eval completes with `total=230`, `error=0`.
- RCABench full eval completes with `total=1422`, `error=0`.
- RCABench AC@1, MRR, AC@3, and AC@5 are not lower than the fresh baseline.
- AIOps25 AC@1 or MRR improves clearly; target AC@1 is at least 0.70.
- AIOps25 AC@3/AC@5 do not have unexplained large regressions.
- Compare documents list top-1 improvements, top-1 regressions, rank
  improvements, and rank regressions for both datasets.
- Any retained mechanism is explained as telemetry reliability, trace
  root-alignment, candidate coverage, or metric/log root ownership, not as
  dataset-specific selection.

## Implemented Change

Implemented an incident-local trace structural confidence gate in
`algorithms/evidencerank/src/evidencerank/crest.py`.

Runtime inputs are only raw telemetry frames and CREST's own feature matrix.
The gate estimates whether trace should be treated as root-aligned structural
evidence from:

- abnormal trace service coverage;
- abnormal trace row concentration and spread;
- trace mutation / propagation family selectivity;
- overlap between trace-covered candidates and metric/log evidence mass.

If abnormal trace traffic is not dominated by a single service surface, CREST
keeps full trace structural support. If trace rows are dominant and concentrated
while metric/log evidence points outside trace coverage, CREST scales trace
feature families and graph context support for this incident. This is a bounded
confidence cap, not a fallback to `crest_metric_log`.

`crest_no_reliability` was added as a CREST-owned ablation registry. Existing
modal ablations keep `_reliability_mode = "none"` so their historical behavior
remains isolated from the new default `crest` mechanism.

## Rejected Intermediate

The first trace-confidence gate improved AIOps25 but regressed RCABench:

| dataset | version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | `CREST_AIOPS1_AIOPS25` | 230 | 0 | 0.413043 | 0.580494 | 0.678261 | 0.786957 |
| rcabench | `CREST_AIOPS1_RCABENCH_REJECTED` | 1422 | 0 | 0.793952 | 0.872228 | 0.945148 | 0.971871 |

RCABench regressions occurred in cases where trace was broad enough to remain
useful but the earlier confidence formula still reduced it. The refinement was
to only enter the cap path when abnormal trace row share is dominated by one
service surface. This keeps the mechanism tied to entry-path / symptom-surface
identification rather than arbitrary trace down-weighting.

## Final Validation

The accepted CREST_AIOPS1 dominant trace gate was fully re-evaluated after the
refinement.

| dataset | version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | `CREST_AIOPS1_DOMINANT_AIOPS25` | 230 | 0 | 0.413043 | 0.580494 | 0.678261 | 0.786957 |
| rcabench | `CREST_AIOPS1_DOMINANT_RCABENCH` | 1422 | 0 | 0.801688 | 0.876029 | 0.944444 | 0.971871 |

Metric deltas against the freshly verified no-reliability baseline:

| dataset | AC@1 delta | MRR delta | AC@3 delta | AC@5 delta |
| --- | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | +0.078261 | +0.076891 | +0.078261 | +0.117391 |
| rcabench | +0.001406 | +0.000703 | 0.000000 | 0.000000 |

Compare status counts:

| dataset | improved_to_hit1 | regressed_from_hit1 | rank_improved | rank_regressed | unchanged |
| --- | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | 18 | 0 | 62 | 4 | 146 |
| rcabench | 2 | 0 | 0 | 0 | 1420 |

Generated artifacts:

- `CREST_AIOPS1_BASE_AIOPS25`
- `CREST_AIOPS1_BASE_RCABENCH`
- `CREST_AIOPS1_DOMINANT_AIOPS25`
- `CREST_AIOPS1_DOMINANT_RCABENCH`
- `docs/EvidRank_evolve/compare_CREST_AIOPS1_BASE_AIOPS25_vs_CREST_AIOPS1_DOMINANT_AIOPS25.md`
- `docs/EvidRank_evolve/compare_CREST_AIOPS1_BASE_RCABENCH_vs_CREST_AIOPS1_DOMINANT_RCABENCH.md`

## Decision

Accept CREST_AIOPS1 as an intermediate default `crest` improvement.

The improvement is explained by a general operations RCA mechanism: when an
incident's trace telemetry is concentrated on a dominant high-observability
service and lacks enough root-aligned candidate overlap, trace is more likely
to be an entry-path or propagation symptom surface. The gate protects
metric/log-owned root candidates from being suppressed by structural trace
support, while leaving RCABench-style broad trace/topology evidence untouched.

This does not reach the target `AC@1 >= 0.70` on AIOps25. Remaining hard cases
are still dominated by weakly trace-covered resource/JVM/pod forms where the
root service's local evidence is present but not strongly enough owned by a
resource or instance identity. The next minimal generic change should be
resource / instance / KPI provenance concentration as root-local evidence, with
natural no-op behavior when provenance columns are absent.
