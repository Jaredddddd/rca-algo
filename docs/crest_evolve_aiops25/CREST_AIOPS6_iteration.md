# CREST_AIOPS6 Iteration

## Round Budget

AIOPS6 is round 3/3 of the resumed adaptive-modality direction. If it does not
reach the target, stop this optimization task and document the limitation
instead of continuing more optimization rounds.

## General Hypothesis

AIOPS4 and AIOPS5 were safe but too narrow. The remaining general hypothesis is
that a dominant trace surface should not be allowed to keep top-1 merely because
it also has propagated metric/log evidence. When trace concentration identifies
a high-volume surface and a different service has strong non-trace ownership
inside the same incident, CREST should run a bounded competition between the
surface and that non-trace owner.

This is an unsupervised modality selector, not a dataset fallback. It uses raw
telemetry only: abnormal trace concentration, per-service metric/log ownership,
default CREST rank support, and incident-local distribution statistics.

## Fresh Baseline

The current accepted default remains CREST_AIOPS2.

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| rcabench | crest | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |

## Failure Mechanism

Representative AIOps25 false cases show:

- default `crest` top-1 is a dominant trace surface;
- the correct service is often rank 2 or 3 under default CREST;
- metric/log ownership for the correct service is high, but the trace surface
  also has propagated metric/log evidence, so strict ownership dominance never
  fires.

The general mechanism is propagation contamination of non-trace evidence on the
trace surface. AIOPS6 should use case-local rank competitiveness rather than
strict surface domination.

## Planned Code Change

- Add `crest_surface_competition` as the final ablation registry.
- Keep default `crest` unchanged until validation.
- Reuse the AIOPS2 modality confidence gate.
- When the current winner is the dominant abnormal trace surface:
  - compute metric/log ownership rank view;
  - choose the strongest non-surface non-trace owner;
  - require the candidate to be in the incident's supported default-score
    region rather than deep tail;
  - move the candidate just above the surface.

No fixed trace confidence constants, service names, dataset names, labels,
injection data, previous outputs, SimpleRCA outputs, or `conclusion.parquet`
are used at runtime.

## Validation Plan

Run compile, guard, banned-constant scan, full AIOps25/RCABench evals,
perf-report, snapshots, summaries, and top-1 change analysis. If AIOps25 still
does not improve enough, stop after documenting the evidence.

## Acceptance Criteria

- `guard` has no high-risk overfitting warning.
- Compile passes.
- AIOps25 full eval: `total=230`, `error=0`.
- RCABench full eval: `total=1422`, `error=0`.
- AIOps25 AC@1 or MRR clearly improves.
- RCABench AC@1, MRR, AC@3, and AC@5 do not drop below the fresh baseline if
  promoted.
- If AIOps25 remains far below `AC@1 >= 0.70`, stop the task and record that
  this family of online unsupervised trace-surface gates is insufficient under
  the current service-level representation.

## Result

Implemented `crest_surface_competition` as an ablation registry and kept the
default `crest` unchanged.

Static checks:

- `compileall` passed for `crest.py` and `main.py`.
- `guard` had no high-risk overfitting warnings; only the existing medium
  `rcabench_platform` import/docstring literals were reported.
- Banned trace-confidence constant/name scan was empty for `crest.py` and
  `main.py`.

Full eval and perf-report:

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| aiopschallenge2025_rcabench_service | crest_surface_competition | 230 | 0 | 0.530435 | 0.660161 | 0.734783 | 0.813043 |
| rcabench | crest | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |
| rcabench | crest_surface_competition | 1422 | 0 | 0.789733 | 0.870302 | 0.945148 | 0.972574 |

Snapshots and summaries:

- `CREST_AIOPS6_BASE_AIOPS25`
- `CREST_AIOPS6_SURFACE_AIOPS25`
- `CREST_AIOPS6_BASE_RCABENCH`
- `CREST_AIOPS6_SURFACE_RCABENCH`
- Summary files were written under `docs/EvidRank_evolve/`.

Offline top-1 change analysis:

| dataset | improved_to_hit1 | regressed_from_hit1 | rank_improved | rank_regressed | unchanged | top1_changed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | 36 | 21 | 0 | 13 | 160 | 113 / 230 |
| rcabench | 0 | 19 | 0 | 0 | 1403 | 21 / 1422 |

Detailed compare note:

- [CREST_AIOPS6_surface_competition_compare.md](CREST_AIOPS6_surface_competition_compare.md)

## Decision

Reject AIOPS6 and do not promote it to default `crest`.

The mechanism is directionally useful on AIOps25: it confirms that a dominant
trace surface can be a propagation or entry symptom, and that non-trace
ownership can rescue many service-level cases. However, the gate is too broad.
It also demotes legitimate trace/root-aligned winners, especially cases where
trace topology and request/response symptoms are the real root evidence. That
failure appears clearly on RCABench: there are 19 `regressed_from_hit1` and no
offsetting `improved_to_hit1`.

The accepted default remains CREST_AIOPS2. AIOPS4 was too narrow, AIOPS5 made
no ranking changes, and AIOPS6 was strong enough to move AIOps25 but unsafe for
RCABench. Per the round budget, this optimization task stops here instead of
opening AIOPS7.

## Lesson

Online unsupervised modality selection is necessary but not sufficient in the
current service-level representation. A safe selector cannot ask only whether a
non-trace candidate has strong metric/log ownership; it must also prove that the
current trace surface lacks root-owned trace mutation or that the challenger
explains the surface through a stronger causal path. Without that second proof,
the selector becomes a broad demotion rule and damages trace-topology cases.
