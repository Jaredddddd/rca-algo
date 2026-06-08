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
