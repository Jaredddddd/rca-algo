# PV_CREST1 Iteration

## Goal

Improve default `crest` on `aiopschallenge2025_rcabench_service`, targeting or
approaching `AC@1 >= 0.70` and higher MRR, while preserving RCABench full
multimodal performance. If RCABench drops, the candidate must remain at
`AC@1 >= 0.77`, be recorded as a trade-off, and not be automatically accepted.

## Constraints

- Runtime code must not read labels, injection metadata, previous outputs,
  perf reports, historical rankings, or `conclusion.parquet`.
- Runtime code must not branch on dataset names, datapack ids, service names,
  fault names, random suffixes, or dataset splits.
- Do not globally lower trace weight, switch to metric+log, or sacrifice
  trace-root-aligned RCABench cases.
- Do not tune fixed numeric cutoffs for exposure/root roles. Any accepted
  mechanism must be explainable as unsupervised or self-supervised structure
  inside the incident, such as rank stability, Pareto dominance, feature-family
  dropout consistency, topology consistency, or cross-modal agreement.
- Offline labels may be used only for false-case analysis, summaries, compares,
  and documentation.

## Fresh Baseline Requirement

The current `crest.py` only exposes the base CREST path and modality ablations;
it does not contain the previously documented AIOPS2 modality-confidence gate.
Therefore this iteration will first run fresh full evaluations with the current
source instead of relying on old reports.

Fresh baseline snapshots:

| dataset | version | algorithm |
| --- | --- | --- |
| `aiopschallenge2025_rcabench_service` | `PV_CREST1_BASE_AIOPS25_SERVICE` | `crest` |
| `rcabench` | `PV_CREST1_BASE_RCABENCH_FRESH` | `crest` |

Fresh baseline result:

| dataset | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aiopschallenge2025_rcabench_service` | 230 | 0 | 0.334783 | 0.503603 | 0.600000 | 0.669565 |
| `rcabench` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

The AIOps25 target `AC@1 >= 0.70` requires 161 top-1 hits. Current source has
77, so the gap is 84 additional top-1 hits.

## Hypothesis

AIOps25 service-level misses are not solved by treating trace as harmful. A
safer partial-view mechanism should infer whether the current top trace surface
is root-local or exposure/propagation-biased. A challenger may alter the top
rank only when it has local metric/log/resource-style root atoms and the current
winner lacks selective trace-mutation ownership.

This iteration will validate one minimal partial-view causal mechanism after
fresh baselines are established.

## Mechanism Revision

An initial threshold-style gate was rejected during implementation because
constants such as fixed exposure/root cutoffs would be benchmark tuning rather
than an unsupervised mechanism. The current ablation therefore uses only
incident-local ordinal/Pareto dominance:

- root role is formed from metric shift, log shift, and trace mutation residual
  atoms;
- exposure role is formed from trace propagation, observability volume, and
  topology context atoms;
- trace mutation residual is computed incident-locally as trace mutation not
  explained by trace propagation burden, so endpoint/status/path shifts on an
  exposure surface are not automatically treated as root-local trace ownership;
- a challenger can move above the current winner only if it strictly dominates
  the winner on root-local role while the winner strictly dominates it on
  exposure/propagation role;
- a trace-mutation-owned winner is protected by the same relative comparisons,
  not by a fixed trace threshold.

No numeric role cutoff, dataset branch, service name, fault name, label,
injection metadata, historical output, or `conclusion.parquet` is used by the
runtime path.

## Partial-View Ablation Result

`crest_partial_view` was evaluated as an ablation and must be rejected as a
default candidate.

| dataset | version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aiopschallenge2025_rcabench_service` | `PV_CREST1_PARTIAL_AIOPS25_SERVICE` | 230 | 0 | 0.430435 | 0.608491 | 0.739130 | 0.791304 |
| `rcabench` | `PV_CREST1_PARTIAL_RCABENCH` | 1422 | 0 | 0.492264 | 0.714684 | 0.938115 | 0.972574 |

Cross-algorithm offline compare against fresh base `crest` snapshots:

| dataset | AC@1 delta | MRR delta | AC@3 delta | AC@5 delta | improved_to_hit1 | regressed_from_hit1 | rank_regressed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `aiopschallenge2025_rcabench_service` | +0.095652 | +0.104888 | +0.139130 | +0.121739 | 54 | 32 | 9 |
| `rcabench` | -0.308017 | -0.160641 | -0.006329 | +0.000703 | 35 | 473 | 105 |

Generated artifacts:

- `output/rcabench-platform-v2/evolve_snapshots/PV_CREST1_PARTIAL_AIOPS25_SERVICE/`
- `output/rcabench-platform-v2/evolve_snapshots/PV_CREST1_PARTIAL_RCABENCH/`
- `docs/EvidRank_evolve/PV_CREST1_PARTIAL_AIOPS25_SERVICE_summary.md`
- `docs/EvidRank_evolve/PV_CREST1_PARTIAL_RCABENCH_summary.md`
- `output/rcabench-platform-v2/evolve_reports/cross_compare_PV_CREST1_BASE_AIOPS25_SERVICE_vs_PV_CREST1_PARTIAL_AIOPS25_SERVICE/case_deltas.csv`
- `output/rcabench-platform-v2/evolve_reports/cross_compare_PV_CREST1_BASE_RCABENCH_FRESH_vs_PV_CREST1_PARTIAL_RCABENCH/case_deltas.csv`

Decision: reject `crest_partial_view` as default. The mechanism is label-free
and improves AIOps25 over the current base, but it is too broad. It treats many
RCABench trace-root-aligned winners as exposure surfaces and produces 473
RCABench `regressed_from_hit1` cases, far below the required `AC@1 >= 0.77`
guardrail.

The useful lesson is that root/exposure role contrast cannot be a free top-1
override, even when implemented without fixed cutoffs. A future candidate must
first prove that the winner is unstable under unsupervised evidence perturbation
or that the challenger is stable across independent views; otherwise metric/log
or residual ownership is just another symptom surface.

## Initial Plan

1. Snapshot current outputs before any `--clear` run.
2. Re-evaluate current `crest` on AIOps25 service-level and RCABench.
3. Analyze AIOps25 false cases using offline labels and raw telemetry only.
4. Implement a small CREST-owned partial-view arbitration or ablation.
5. Run `guard`, compile checks, AIOps25 full eval, and RCABench full eval.
6. Accept only if AIOps25 improves and RCABench satisfies the stated guardrail.
