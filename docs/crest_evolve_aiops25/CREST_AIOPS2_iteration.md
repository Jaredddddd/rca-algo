# CREST_AIOPS2 Iteration

## General Hypothesis

CREST_AIOPS1 proved that trace structural support should be capped when an
incident's trace telemetry looks like a dominant symptom surface. The next
general step is to estimate metric, log, and trace reliability jointly inside
each incident, then use those unsupervised confidence values for bounded
modality fusion.

The mechanism should capture a common operations RCA pattern: resource/JVM/pod
incidents often have root-owned metric/log evidence while trace mainly shows
entry-path propagation, but protocol/path/network incidents can still be
trace-owned. The algorithm must decide from telemetry reliability, not from
dataset, service, or fault identity.

## Fresh Baseline

Current baseline for this iteration is the accepted CREST_AIOPS1 default
`crest`, freshly evaluated on 2026-06-08:

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.413043 | 0.580494 | 0.678261 | 0.786957 |
| rcabench | crest | 1422 | 0 | 0.801688 | 0.876029 | 0.944444 | 0.971871 |

Before accepting any AIOPS2 result, snapshot the current outputs as
`CREST_AIOPS2_BASE_AIOPS25` and `CREST_AIOPS2_BASE_RCABENCH`, then compare the
candidate against those snapshots.

## Failure Mechanism

CREST_AIOPS1 removes a large class of high-volume trace victim errors, but many
AIOps25 misses remain where the root is weakly covered by trace and only appears
as local metric/log/resource evidence. A trace-only gate cannot promote these
roots when metric/log evidence is present but does not dominate CREST's final
`A * F + S` score.

SimpleRCA's AIOps25 strength suggests a reusable mechanism: independent
modality top-k evidence and rank-bounded voting can be robust when trace
reliability is weak. CREST should borrow the bounded fusion idea, not
SimpleRCA's service-name suppression, fixed dataset adapter behavior, or output
as a runtime teacher.

## Planned Code Change

- Add `crest_modality_confidence` as an ablation registry.
- Keep default `crest` unchanged until the ablation is verified on both
  datasets.
- Compute metric, log, and trace confidence from raw telemetry and CREST
  feature families:
  service coverage, sample volume, score selectivity, normal-vs-abnormal shift,
  trace row concentration, trace mutation selectivity, and cross-modal top-k
  agreement.
- Fuse modality-local ranks with bounded confidence weights, while preserving
  CREST_AIOPS1's trace structural cap.
- Do not read labels, injection metadata, previous output, perf reports,
  historical rankings, ground truth, SimpleRCA output, or `conclusion.parquet`.
- Do not hardcode dataset names, datapack ids, service names, fault names, or
  splits.

## Parallel Validation Plan

AIOps25 and RCABench full evaluations are independent and should be launched in
parallel for this iteration. Use two concurrent batch commands or parallel tool
calls:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_modality_confidence \
  -d "$AIOPS_DATASET" --clear --use-cpus 16
```

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_modality_confidence \
  -d "$RCABENCH_DATASET" --clear --use-cpus 32
```

After both finish, run perf-report, snapshot, summarize, and compare for both
datasets. If the ablation is accepted, promote the mechanism to default
`crest`, then rerun full eval and compare again under the `crest` name.

## Acceptance Criteria

- Guard has no high-risk overfitting findings.
- Compile passes.
- AIOps25 full eval completes with `total=230`, `error=0`.
- RCABench full eval completes with `total=1422`, `error=0`.
- Relative to `CREST_AIOPS2_BASE_*`, AIOps25 AC@1 or MRR improves clearly.
- RCABench AC@1, MRR, AC@3, and AC@5 do not drop below baseline if promoted to
  default `crest`.
- AIOps25 AC@3 and AC@5 do not suffer unexplained large regressions.
- Compare reports list `improved_to_hit1`, `regressed_from_hit1`,
  `rank_improved`, and `rank_regressed` for both datasets.
- Any accepted improvement is explained as unsupervised modality reliability,
  metric/log root ownership, trace root alignment, resource provenance, or
  propagation victim control.

## SimpleRCA Analysis

`results_aiops2025.md` shows `simplerca` at `AC@1=0.652174` and
`MRR=0.696957` on the same 230 AIOps25 cases. The useful general lesson is not
its service-name behavior or any runtime fallback. Its strength comes from a
bounded modality selection pattern: metric, log, and trace each produce local
top candidates, and rank voting prevents a single high-volume trace surface
from dominating all incidents.

The transferable mechanism for CREST is therefore:

- keep trace when trace mutation looks root-owned;
- constrain trace when it is mostly a dominant propagation or entry surface;
- let metric/log local ownership arbitrate only under weak trace reliability;
- make the decision from incident-local telemetry ranks, not dataset, service,
  fault, SimpleRCA output, labels, or historical perf.

## Implemented Mechanism

The accepted code path keeps the AIOPS1 trace-confidence gate and adds a narrow
case-local modality arbitration step. It first estimates metric, log, and trace
confidence from CREST family burdens and rank agreement. If trace structural
support is capped, a metric/log candidate may move above the current winner only
when all of these unsupervised conditions hold:

- the candidate has both metric and log local evidence;
- its metric and log ranks are not below the current winner;
- non-trace confidence exceeds trace modality confidence;
- the current winner looks more trace-surface-heavy than the candidate;
- a trace-mutation-owned winner is protected, both when it is the dominant
  trace surface and when a trace-covered challenger tries to override it.

This is intentionally an eligibility predicate, not a broad score fusion. It
does not use fixed dataset branches, service names, fault names, labels,
injection metadata, SimpleRCA outputs, perf reports, or `conclusion.parquet`.

## Ablation Result

Before promotion, `crest_modality_confidence` was evaluated on both datasets:

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest_modality_confidence | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| rcabench | crest_modality_confidence | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |

A broader earlier ablation reached slightly higher AIOps25 AC@1 but regressed
RCABench. The accepted predicate is narrower because RCABench protocol cases
and AIOps25 DNS/network cases need trace-mutation ownership protection.

## Final Promoted Result

The accepted mechanism was promoted to default `crest` and fully re-evaluated:

| dataset | version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | CREST_AIOPS2_FINAL_AIOPS25 | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| rcabench | CREST_AIOPS2_FINAL_RCABENCH | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |

Against `CREST_AIOPS2_BASE_*`, AIOps25 improved by `+0.052174` AC@1 and
`+0.037359` MRR; RCABench improved by `+0.001406` AC@1 and `+0.000954` MRR.
Against the later magic-free majority-ownership intermediate, AIOps25 improved
by `+0.043478` AC@1 and `+0.031159` MRR; RCABench improved by `+0.000703`
AC@1 and `+0.000615` MRR.

Important compare documents:

- `docs/EvidRank_evolve/compare_CREST_AIOPS2_BASE_AIOPS25_vs_CREST_AIOPS2_FINAL_AIOPS25.md`
- `docs/EvidRank_evolve/compare_CREST_AIOPS2_BASE_RCABENCH_vs_CREST_AIOPS2_FINAL_RCABENCH.md`
- `docs/EvidRank_evolve/compare_CREST_AIOPS2_MAJORITY_OWNERSHIP_AIOPS25_vs_CREST_AIOPS2_FINAL_AIOPS25.md`
- `docs/EvidRank_evolve/compare_CREST_AIOPS2_MAJORITY_OWNERSHIP_RCABENCH_vs_CREST_AIOPS2_FINAL_RCABENCH.md`

The majority-ownership to final AIOps25 compare has 12 `improved_to_hit1` and 2
`regressed_from_hit1`; the RCABench compare has 1 `improved_to_hit1` and no
`regressed_from_hit1`.

## Decision

Accept CREST_AIOPS2 as the default `crest` mechanism. It is a general
telemetry reliability and modality ownership improvement, improves AIOps25
clearly, and does not lower RCABench.

The target `AC@1 >= 0.70` is not reached. The remaining gap is likely not solved
by broader metric/log arbitration, because that starts to damage trace-owned
DNS/network/protocol incidents. The next minimal general step should be
resource / instance / pod provenance: detect concentrated KPI/resource identity
ownership within a service, with natural no-op behavior when provenance columns
are absent.
