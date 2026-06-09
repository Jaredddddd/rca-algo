# CREST_AIOPS5 Iteration

## Round Budget

AIOPS5 is round 2/3 of the resumed adaptive-modality direction. If AIOPS5 and
AIOPS6 still do not reach the target, stop this optimization task and document
the evidence-backed limitation.

## General Hypothesis

AIOPS4 showed that a rare trace-root top bump is too conservative. The next
generic mechanism is entry/trace-surface competition: trace should be allowed
to explain root cause only when the trace surface has root-owned mutation or
cross-modal ownership. If the current winner is the dominant abnormal trace
surface and another candidate has stronger metric/log root ownership, CREST
should let the non-trace candidate arbitrate.

This is still unsupervised and incident-local. It does not name entry services,
fault types, datasets, or case ids. It uses only raw telemetry structure:
abnormal trace service concentration, trace mutation versus propagation burden,
metric/log ownership, and cross-modal rank agreement.

## Fresh Baseline

The current accepted default is still CREST_AIOPS2. AIOPS4 was rejected and not
promoted.

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| rcabench | crest | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |

## Failure Mechanism

Offline false-case comparison shows 34 AIOps25 cases where default `crest`
misses top-1 while `crest_metric_log` hits top-1. In those cases, the default
winner is usually a high-volume trace surface while the ground-truth service is
ranked higher by metric/log local evidence. This does not justify using
`crest_metric_log` as a teacher; it points to a generic observability regime:
trace is present but describes propagation/entry symptoms, while root ownership
lives in metric/log.

AIOPS4 did not improve AIOps25 because it only acted when the current winner's
trace symptom pressure exceeded trace root eligibility. Many entry-surface
false winners also have trace mutation, so that predicate protected them.
AIOPS5 should instead ask whether the trace surface has enough cross-modal
ownership to keep control of final ranking.

## Planned Code Change

- Add `crest_adaptive_modality` as an ablation registry.
- Keep default `crest` unchanged until full dual-dataset validation.
- Preserve the AIOPS2 modality confidence gate.
- Add a trace-surface competition step:
  - identify the dominant abnormal trace surface without service names;
  - if the current winner is that surface, compare its trace-root ownership
    against the strongest metric/log-owned candidate;
  - if non-trace ownership is stronger and the trace surface is better explained
    as trace volume/propagation than cross-modal root ownership, move the
    non-trace candidate above the surface.
- Use rank views and incident-local relative comparisons rather than fixed
  confidence constants.

## Execution Constraints

- Runtime code must not read labels, injection metadata, previous output,
  perf reports, historical rankings, ground truth, SimpleRCA output, or
  `conclusion.parquet`.
- Do not hardcode dataset names, datapack ids, services, fault names, random
  suffixes, or splits.
- Do not copy SimpleRCA's service-name skip, thresholds, fixed top-k vote, or
  output. Only use the general principle of bounded modality-local evidence.
- Do not change converters, filters, evaluation case population, or non-CREST
  algorithms.

## Validation Plan

Run guard, compile, banned-constant scan, then full eval on both datasets:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_adaptive_modality \
  -d "$AIOPS_DATASET" --clear --use-cpus 16

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_adaptive_modality \
  -d "$RCABENCH_DATASET" --clear --use-cpus 32
```

Then run perf-report, snapshot, summary, and offline top-1 change comparison.
Promote to default only if AIOps25 improves and RCABench does not regress.

## Acceptance Criteria

- `guard` has no high-risk overfitting warning.
- Compile passes.
- AIOps25 full eval: `total=230`, `error=0`.
- RCABench full eval: `total=1422`, `error=0`.
- AIOps25 AC@1 or MRR clearly improves.
- RCABench AC@1, MRR, AC@3, and AC@5 do not drop below the fresh baseline if
  promoted.
- AIOps25 AC@3/AC@5 do not show a large unexplained collapse.
- If not accepted, record whether the mechanism was too narrow or too broad
  before moving to AIOPS6.

## Result

Implemented `crest_adaptive_modality` and ran full dual-dataset validation.

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| aiopschallenge2025_rcabench_service | crest_adaptive_modality | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| rcabench | crest | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |
| rcabench | crest_adaptive_modality | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |

Decision: reject AIOPS5. It is safe but still too narrow. Offline diagnosis on
representative AIOps25 false cases shows the current trace surface often has
non-zero metric/log ownership as a propagated symptom, so requiring the
non-surface candidate to strictly dominate the surface's non-trace ownership
prevents action.

For AIOPS6, use broader incident-local surface competition: when the current
winner is the dominant trace surface, choose a non-surface candidate with strong
metric/log ownership relative to the case distribution and allow it to compete
even if the surface also has propagated metric/log evidence.
