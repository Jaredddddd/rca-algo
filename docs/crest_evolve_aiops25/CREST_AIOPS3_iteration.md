# CREST_AIOPS3 Iteration

## General Hypothesis

CREST_AIOPS2 improves AIOps25 by estimating incident-local modality
reliability and allowing narrow metric/log ownership arbitration when trace is a
dominant symptom surface. The remaining gap is often service-local resource
ownership: a root service may show concentrated abnormality on a small number of
pods, instances, objects, devices, mountpoints, or KPI identities, while
service-level aggregation and trace topology are dominated by entry-path or
propagation surfaces.

The AIOPS3 hypothesis is that concentrated resource/KPI provenance shifts are
generic operations RCA evidence. They should strengthen a candidate only when
the abnormality is selective within the current incident, bound to metric
evidence, and not contradicted by strong trace-mutation ownership from the
current winner. If provenance columns are absent or uninformative, the mechanism
must naturally no-op.

## Fresh Baseline

The current working-tree default `crest` is the accepted CREST_AIOPS2 final
mechanism, freshly evaluated on 2026-06-09:

| dataset | version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | CREST_AIOPS2_FINAL_AIOPS25 | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| rcabench | CREST_AIOPS2_FINAL_RCABENCH | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |

These are the no-regression baselines for AIOPS3. Before claiming an accepted
result, rerun default `crest` and the new ablation on both datasets, then
snapshot and compare under fresh AIOPS3 names.

## Failure Mechanism

Offline comparison against labels and SimpleRCA output is used only for
analysis. It shows that SimpleRCA succeeds on many AIOps25 cases because it
produces bounded independent modality top candidates; it often emits only one
or a few candidates, so a strong metric/log signal can win even when trace is
dominated by frontend or other high-volume surfaces. This is useful as a
mechanistic clue, but CREST must not read SimpleRCA output or copy its
service-name suppression and fixed thresholds.

The transferable failure pattern is:

- CREST service-level metric aggregation sees the root service but not sharply
  enough;
- trace and graph support favor high-observability propagation surfaces;
- metric/log arbitration helps only when both modalities agree, leaving
  resource-local metric roots under-ranked;
- SimpleRCA-like top1 success suggests that a narrow, root-owned metric
  selector can be helpful, but broad replacement would regress CREST-owned
  network, DNS, code, and multi-GT cases.

## Planned Code Change

- Add `crest_resource_provenance` as an ablation registry.
- Keep default `crest` unchanged until the ablation is verified.
- Derive a service-local provenance ownership score from raw metric rows:
  resource identity columns such as pod, instance, object, device, mountpoint,
  container, deployment, statefulset, metric/KPI key, KPI name, and metric group.
- Compare normal and abnormal windows by `(service, metric family, resource
  identity)` using robust relative change and distribution concentration.
- Use the score only as bounded near-top arbitration under weak trace or weak
  current-winner nontrace ownership; do not add an unbounded global bonus.
- Protect current winners with stronger trace-mutation ownership so RCABench and
  trace-owned AIOps25 incidents keep their topology/path signal.
- If useful provenance columns are missing, constant, or too sparse, return the
  original CREST score unchanged.

## Execution Constraints

- Runtime code must not read labels, injection metadata, previous outputs,
  perf reports, historical rankings, ground truth, SimpleRCA output, or
  `conclusion.parquet`.
- Do not hardcode dataset names, datapack ids, case ids, service names, fault
  names, random suffixes, or dataset splits.
- Do not treat `attr.aiops.*` as privileged labels. They are only generic
  resource provenance metadata and the code must no-op when they are absent.
- Avoid magic-number trace confidence constants, including the banned
  `CREST_TRACE_CONFIDENCE_*` and dominant-share constants.
- Do not change converters, filters, evaluation population, or existing
  non-CREST algorithms.

## Validation Plan

Run guard and compile before full evaluation:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall \
  algorithms/evidencerank/src/evidencerank/crest.py \
  algorithms/evidencerank/main.py
```

Run AIOps25 and RCABench full evals in parallel:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_resource_provenance \
  -d "$AIOPS_DATASET" --clear --use-cpus 16
```

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_resource_provenance \
  -d "$RCABENCH_DATASET" --clear --use-cpus 32
```

Then run perf-report, snapshot, summarize, and compare for both datasets. If
the ablation is accepted, promote to default `crest` and rerun both datasets
under the `crest` name.

## Acceptance Criteria

- `guard` has no high-risk overfitting warning.
- Compile passes.
- AIOps25 full eval completes with `total=230`, `error=0`.
- RCABench full eval completes with `total=1422`, `error=0`.
- AIOps25 AC@1 or MRR improves clearly relative to CREST_AIOPS2 final.
- RCABench AC@1, MRR, AC@3, and AC@5 do not drop below CREST_AIOPS2 final if
  promoted to default.
- AIOps25 AC@3 and AC@5 do not show unexplained large regression.
- Compare reports for both datasets list improved, regressed, and rank-moved
  cases.
- The accepted explanation is resource provenance ownership and coverage-aware
  modality reliability, not dataset/fault/service-specific tuning.

## If Target Is Not Reached

If AIOps25 remains below `AC@1 >= 0.70` but improves without RCABench
regression, keep AIOPS3 as an intermediate research version. The next minimal
generic step should be a stricter pairwise competition between resource-owned
metric roots and trace/log symptom surfaces, rather than broader additive
rescoring.

## Result

The `crest_resource_provenance` ablation was implemented and fully evaluated on
both datasets. It produced a small AIOps25 improvement but violated the
RCABench no-regression criterion:

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| aiopschallenge2025_rcabench_service | crest_resource_provenance | 230 | 0 | 0.469565 | 0.634666 | 0.734783 | 0.817391 |
| rcabench | crest | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |
| rcabench | crest_resource_provenance | 1422 | 0 | 0.798172 | 0.874405 | 0.945148 | 0.972574 |

Decision: reject AIOPS3 as a default `crest` mechanism. The resource provenance
signal is useful for AIOps25 recall, but the current arbitration is too broad
for RCABench trace-owned incidents. Keep it as an ablation and research
negative result; do not promote it.

The next round should return to the stronger evidence-backed direction:
incident-local trace root eligibility. Instead of adding resource-owned metric
bonus, first decide whether trace has the right to explain root cause from
coverage, concentration, mutation-vs-propagation role, metric/log support, and
candidate consistency.
