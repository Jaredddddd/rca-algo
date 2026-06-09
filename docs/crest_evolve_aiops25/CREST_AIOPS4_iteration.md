# CREST_AIOPS4 Iteration

## Round Budget

The user updated the objective: from this resumed trace-root-eligibility
direction, run at most three optimization rounds. AIOPS4 is round 1/3. If the
target is still not reached after AIOPS6, stop the optimization task and record
the evidence-backed limitation.

## General Hypothesis

CREST should not ask "is trace globally useful?" It should ask, for each
incident, "does trace have enough root-cause eligibility to explain the current
root?" The useful mechanism is a fully unsupervised trace root-eligibility gate:
trace topology and trace row volume should strengthen ranking only when trace
coverage, mutation selectivity, candidate support, and cross-modal consistency
look root-owned. When trace mostly describes an entry path or propagation
surface, metric/log evidence should dominate the final arbitration.

The same structure should later apply to metric and log: each modality provides
root evidence only when it has selective, candidate-owned, cross-modal or
normal-vs-abnormal support inside the current incident.

## Fresh Baseline

Current default `crest` is still CREST_AIOPS2. AIOPS3 was rejected and not
promoted.

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| rcabench | crest | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |

These freshly verified AIOPS3 baseline outputs are the no-regression reference
for AIOPS4.

## Failure Mechanism

The AIOps25 gap is still dominated by incidents where trace is observable but
not root-explanatory. Trace often covers a high-volume entry chain or downstream
symptom surface, while the true root candidate has stronger metric/log local
evidence. CREST_AIOPS2 already helps by capping dominant trace surfaces, but its
metric/log arbitration is intentionally narrow and still protects some trace
mutation surfaces that can be propagation symptoms in AIOps25.

SimpleRCA's high AIOps25 AC@1 is consistent with this diagnosis: it uses
bounded modality-local top candidates and does not let trace graph support
dominate every incident. CREST should adopt the root-eligibility principle, not
SimpleRCA's fixed thresholds, service-name behavior, or output as a teacher.

## Planned Code Change

- Add `crest_trace_root_eligibility` as an ablation registry.
- Keep default `crest` unchanged until the ablation is verified on both
  datasets.
- Compute incident-local trace root eligibility from raw telemetry and CREST
  feature families:
  - trace service coverage over candidate services;
  - abnormal trace concentration and spread;
  - trace mutation selectivity versus propagation burden;
  - metric/log support for the trace top candidate;
  - metric/log support for the strongest non-trace candidate;
  - whether the trace top candidate looks like high-volume downstream or entry
    symptom surface.
- If trace root eligibility is weaker than non-trace root ownership, cap trace
  structural dominance and allow metric/log candidate arbitration.
- Preserve trace-owned RCABench behavior by retaining trace when mutation
  selectivity and cross-modal support agree, or when no stronger non-trace root
  owner exists.

## Execution Constraints

- Runtime code must not read labels, injection metadata, previous output,
  perf reports, historical rankings, ground truth, SimpleRCA output, or
  `conclusion.parquet`.
- Do not hardcode dataset names, datapack ids, services, fault names, random
  suffixes, or splits.
- Do not use banned trace magic constants such as
  `CREST_TRACE_CONFIDENCE_FULL`, `CREST_TRACE_CONFIDENCE_FLOOR`,
  `CREST_TRACE_MIN_SCALE`, `CREST_TRACE_DOMINANT_ROW_SHARE`, or their exact
  numeric values.
- Do not change converters, filters, evaluation case population, or non-CREST
  algorithms.

## Validation Plan

Run guard and compile:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall \
  algorithms/evidencerank/src/evidencerank/crest.py \
  algorithms/evidencerank/main.py
```

Run AIOps25 and RCABench full evals in parallel:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_trace_root_eligibility \
  -d "$AIOPS_DATASET" --clear --use-cpus 16
```

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_trace_root_eligibility \
  -d "$RCABENCH_DATASET" --clear --use-cpus 32
```

Then run perf-report, snapshot, summary, and compare. Promote to default only
if AIOps25 improves and RCABench does not regress.

## Acceptance Criteria

- `guard` has no high-risk overfitting warning.
- Compile passes.
- AIOps25 full eval: `total=230`, `error=0`.
- RCABench full eval: `total=1422`, `error=0`.
- AIOps25 AC@1 or MRR clearly improves.
- RCABench AC@1, MRR, AC@3, and AC@5 do not drop below the fresh AIOPS3
  default baseline if promoted.
- Compare reports explain improved and regressed cases.
- The accepted mechanism is trace root eligibility / modality reliability, not
  dataset-specific selection.

## Result

Implemented `crest_trace_root_eligibility` as an ablation. It compiles, guard
has no high-risk warning, and the banned trace-confidence constants are absent.

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| aiopschallenge2025_rcabench_service | crest_trace_root_eligibility | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| rcabench | crest | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |
| rcabench | crest_trace_root_eligibility | 1422 | 0 | 0.803797 | 0.877095 | 0.945148 | 0.972574 |

Offline top-1 comparison:

- AIOps25: `top1_changed=0`, `improved=0`, `regressed=0`.
- RCABench: `top1_changed=7`, `improved=2`, `regressed=1`.

Decision: reject AIOPS4 as a default promotion. It is safe for RCABench but too
narrow for AIOps25: the `trace_symptom > trace_root` predicate almost never
fires on the target false cases. The next round should change from rare top
bump to explicit unsupervised modality selection for high trace-surface
incidents.
