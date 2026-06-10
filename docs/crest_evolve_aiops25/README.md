# CREST AIOps25 Cross-Dataset Evolution

This directory is the durable home for CREST optimization work whose primary
goal is to improve AIOpsChallenge2025 while preserving RCABench performance.

## Scope

- Target algorithm family: `crest`
- Main implementation: `algorithms/evidencerank/src/evidencerank/crest.py`
- AIOps25 dataset name: `aiopschallenge2025_rcabench_service`
- AIOps25 data root:
  `data/rcabench-platform-v2/data/aiopschallenge2025_rcabench_service`
- AIOps25 meta root:
  `data/rcabench-platform-v2/meta/aiopschallenge2025_rcabench_service`
- RCABench reference dataset: `rcabench`

The goal is to raise CREST on AIOps25, ideally to `AC@1 >= 0.70`, without
lowering the current verified `crest` metrics on RCABench. The algorithmic
mechanism must be general to operations RCA, not a dataset, service, datapack,
or fault-name patch.

## Current Known Baselines

The active baseline must be re-verified in a fresh iteration before claiming
improvement.

Known AIOps25 result after the rebuilt 230-case service-level conversion:

| algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `crest` | 230 | 0 | 0.334783 | 0.503603 | 0.600000 | 0.669565 |
| `crest_metric_log` | 230 | 0 | 0.478261 | 0.668761 | 0.821739 | 0.934783 |

Known RCABench reference for the repository baseline:

| algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

If the working tree contains a later accepted CREST variant, use the freshly
verified current `crest` output as the no-regression baseline instead of these
reference numbers.

## Current Working-Tree Status

The resumed PV-CREST direction is now retained as historical analysis only.
Per the user request after the cleanup review, all runtime CREST code changes
from the AIOps25 optimization attempt were reverted to the pre-AIOps25
optimization source state. The `AC@1 >= 0.70` target was not reached.

Last verified PV-CREST experimental outputs before rollback:

| dataset | version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aiopschallenge2025_rcabench_service` | `PV_CREST3_REPRESENTATIVE_AIOPS25_SERVICE` | 230 | 0 | 0.526087 | 0.672613 | 0.782609 | 0.865217 |
| `rcabench` | `PV_CREST3_REPRESENTATIVE_RCABENCH` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

PV_CREST2 introduced DyMo-style dynamic evidence selection and was the main
safe gain in this resumed direction: AIOps25 AC@1 improved from `0.334783` to
`0.526087` while RCABench stayed unchanged. PV_CREST3 added incident-local
service representativeness for provenance atoms; it kept AIOps25 AC@1 unchanged
but improved MRR, AC@3, and AC@5. These mechanisms were not retained in the
default runtime code because they added too many hand-designed traces without
reaching the AIOps25 target.

Key PV-CREST documents:

- [../pv-crest/PV_CREST1_iteration.md](../pv-crest/PV_CREST1_iteration.md)
- [../pv-crest/PV_CREST2_iteration.md](../pv-crest/PV_CREST2_iteration.md)
- [../pv-crest/PV_CREST3_analysis.md](../pv-crest/PV_CREST3_analysis.md)
- [PV_CREST3_REPRESENTATIVE_AIOPS25_SERVICE_summary.md](../EvidRank_evolve/PV_CREST3_REPRESENTATIVE_AIOPS25_SERVICE_summary.md)
- [PV_CREST3_REPRESENTATIVE_RCABENCH_summary.md](../EvidRank_evolve/PV_CREST3_REPRESENTATIVE_RCABENCH_summary.md)

Historical code cleanup note before rollback:

- A cleanup split had separated default CREST code from experimental variants,
  but that code change was also reverted with the rest of the AIOps25 runtime
  modifications.
- The retained lesson is that default CREST should not import CERA/EvidenceRank
  ordinal evidence energy, feature ladders, calibrated priors, or similar
  hand-designed scorer traces.

## Historical AIOPS Status

This task is stopped after the user-defined three-round limit for the resumed
adaptive-modality direction. The target `AC@1 >= 0.70` on
`aiopschallenge2025_rcabench_service` was not reached without RCABench
regression.

Before the PV-CREST resumed direction, the accepted default was `CREST_AIOPS2`.
Later AIOPS ablations are documented but not promoted:

| version | registry | AIOps25 AC@1 | RCABench AC@1 | decision |
| --- | --- | ---: | ---: | --- |
| `CREST_AIOPS3` | `crest_resource_provenance` | 0.469565 | 0.798172 | rejected: RCABench regression |
| `CREST_AIOPS4` | `crest_trace_root_eligibility` | 0.465217 | 0.803797 | rejected: no AIOps25 gain |
| `CREST_AIOPS5` | `crest_adaptive_modality` | 0.465217 | 0.803094 | rejected: no ranking change |
| `CREST_AIOPS6` | `crest_surface_competition` | 0.530435 | 0.789733 | rejected: RCABench regression |

The strongest rejected AIOps25 ablation is `CREST_AIOPS6`: it confirms the
telemetry-reliability hypothesis by raising AIOps25 AC@1 from `0.465217` to
`0.530435`, but it is too broad and damages RCABench trace-root cases.

Key final documents:

- [CREST_AIOPS6_iteration.md](CREST_AIOPS6_iteration.md)
- [CREST_AIOPS6_surface_competition_compare.md](CREST_AIOPS6_surface_competition_compare.md)
- [CREST_AIOPS6_SURFACE_AIOPS25_summary.md](../EvidRank_evolve/CREST_AIOPS6_SURFACE_AIOPS25_summary.md)
- [CREST_AIOPS6_SURFACE_RCABENCH_summary.md](../EvidRank_evolve/CREST_AIOPS6_SURFACE_RCABENCH_summary.md)

The lesson is that CREST needs incident-local modality reliability, but a safe
online selector must prove trace is not root-aligned before demoting a trace
surface. Metric/log ownership alone is an insufficient proof because propagated
symptoms can also create strong non-trace ownership.

## Historical Accepted Default

`CREST_AIOPS2` was the accepted default `crest` for the older AIOPS series. It keeps the
incident-local trace structural confidence gate and adds a narrow unsupervised
modality ownership arbitration step. Under weak trace reliability, a metric/log
candidate can overtake a trace-surface winner only when it has joint metric and
log local ownership, and trace-mutation-owned winners are protected.

Freshly verified final result:

| dataset | version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aiopschallenge2025_rcabench_service` | `CREST_AIOPS2_FINAL_AIOPS25` | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| `rcabench` | `CREST_AIOPS2_FINAL_RCABENCH` | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |

Against the AIOPS2 fresh baseline, AIOps25 improved by `+0.052174` AC@1 and
`+0.037359` MRR; RCABench improved by `+0.001406` AC@1 and `+0.000954` MRR.
Against the later magic-free majority-ownership intermediate, AIOps25 improved
by `+0.043478` AC@1 and RCABench improved by `+0.000703` AC@1.

Key documents:

- [CREST_AIOPS2_iteration.md](CREST_AIOPS2_iteration.md)
- [CREST_AIOPS2_modality_selector_design.md](CREST_AIOPS2_modality_selector_design.md)
- [CREST_AIOPS2_FINAL_AIOPS25_summary.md](../EvidRank_evolve/CREST_AIOPS2_FINAL_AIOPS25_summary.md)
- [CREST_AIOPS2_FINAL_RCABENCH_summary.md](../EvidRank_evolve/CREST_AIOPS2_FINAL_RCABENCH_summary.md)

The target `AC@1 >= 0.70` is still not reached. Further optimization is not
continued in this task because three additional adaptive-modality rounds were
completed without a promotable solution.

## Previous Accepted Intermediate

`CREST_AIOPS1` adds an incident-local trace structural confidence gate to the
default `crest`. The mechanism is unsupervised and uses only raw telemetry plus
CREST feature values. It caps trace structural support when abnormal trace rows
are dominated by a single high-observability service surface, trace root
alignment is weak, and metric/log evidence points outside trace coverage.

Freshly verified result:

| dataset | version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aiopschallenge2025_rcabench_service` | `CREST_AIOPS1_DOMINANT_AIOPS25` | 230 | 0 | 0.413043 | 0.580494 | 0.678261 | 0.786957 |
| `rcabench` | `CREST_AIOPS1_DOMINANT_RCABENCH` | 1422 | 0 | 0.801688 | 0.876029 | 0.944444 | 0.971871 |

Against the fresh no-reliability baseline, AIOps25 improved by `+0.078261`
AC@1 and RCABench did not regress. This is accepted only as an intermediate
version; AIOps25 remains far below the target `AC@1 >= 0.70`.

## Hard Rules

- Do not use SuperPower skills unless the user explicitly asks.
- Runtime algorithm code must not read labels, injection metadata, previous
  outputs, perf reports, historical rankings, ground truth, or
  `conclusion.parquet`.
- Offline labels may be used only for analysis, summaries, comparisons, and
  documentation.
- Do not hardcode `aiopschallenge2025_rcabench_service`, `rcabench`, datapack
  names, case ids, random suffixes, service names, fault names, or dataset
  splits in runtime logic.
- Do not improve AIOps25 by changing the evaluation population, filtering hard
  cases, or rebuilding the dataset with a different label policy unless the
  user explicitly asks for dataset work.
- Do not copy CERA or EvidenceRank scoring logic, manual prior weights,
  ladders, calibrated multipliers, or runtime fallback behavior into CREST.
- Any accepted change must be expressible as a general operations RCA mechanism:
  telemetry coverage, modality reliability, trace root-alignment, resource
  provenance, graph propagation, candidate observability, or cross-modal
  agreement.

## Current Entry

Start new AIOps25-focused CREST optimization sessions from:

- [CodingAgentPrompt.md](CodingAgentPrompt.md)

## Recommended Version Convention

Use the next unused version number with this pattern:

- Iteration note: `CREST_AIOPS<N>_iteration.md`
- AIOps25 baseline snapshot: `CREST_AIOPS<N>_BASE_AIOPS25`
- RCABench baseline snapshot: `CREST_AIOPS<N>_BASE_RCABENCH`
- AIOps25 snapshot: `CREST_AIOPS<N>_AIOPS25`
- RCABench snapshot: `CREST_AIOPS<N>_RCABENCH`
- AIOps25 baseline summary mirror: `CREST_AIOPS<N>_BASE_AIOPS25_summary.md`
- RCABench baseline summary mirror: `CREST_AIOPS<N>_BASE_RCABENCH_summary.md`
- AIOps25 summary mirror: `CREST_AIOPS<N>_AIOPS25_summary.md`
- RCABench summary mirror: `CREST_AIOPS<N>_RCABENCH_summary.md`
- Compare mirror:
  `compare_CREST_AIOPS<OLD>_vs_CREST_AIOPS<N>_<DATASET>.md`

`VibeResearchTools/evidrank_lab.py summarize` and `compare` currently expect a
CSV labels file. For AIOps25, generate an offline-only temporary CSV from
`labels.parquet` under `/tmp` when needed; do not commit generated labels.
