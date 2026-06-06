# CREST1 Iteration

- Created: 2026-06-06
- Algorithm registry name: `crest`
- Dataset: `rcabench`
- Gate: Gate 0 + Gate 1
- Goal: integrate CREST as a standalone pure traditional RCA algorithm and pass Gate 1 `AC@1 >= 0.60`

## Constraints

- Runtime CREST reads only normal/abnormal metric, trace, and log parquet frames from `args.input_folder`.
- Runtime CREST does not read labels, injection metadata, previous outputs, perf reports, historical rankings, ground truth, or `conclusion.parquet`.
- No LLM, external API, pretrained neural network, or label-trained model is used.
- No datapack id, service name, fault name, random suffix, or dataset split is hardcoded.
- CERA's ordinal tier / ladder expert weights are not used.

## Gate 0 Implementation

Code changes:

- Added `algorithms/evidencerank/src/evidencerank/crest.py`.
- Registered:
  - `crest`
  - `crest_local`
  - `crest_nocf`
  - `crest_nocalib`
- Exposed `score_crest_services(...)` for diagnostics with per-service `A`, `F`, `C`, and final `score`.

The first `CREST1_RAW` implementation used:

```text
A = modality RMS over incident-scaled feature probabilities
F = downstream counterfactual energy removal by message passing
C = 1
score = A * F
```

It was stable but failed Gate 1:

| version | AC@1 | MRR | AC@3 | AC@5 | error | decision |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| CREST1_RAW | 0.234177 | 0.419913 | 0.511252 | 0.640647 | 0 | reject |

Failure mechanism:

- No NaN, missing output, numeric underflow, or graph traversal loop was observed.
- `A` was inflated by high-volume propagation services.
- `F` over-penalized low-outdegree or infrastructure roots because many true roots have weak observable downstream repair reach in trace data.

## Gate 1 Fix

CREST1 replaces the raw modality RMS with a normality-regularized family burden:

```text
A(v) = incident-scaled sum of robust metric / trace / log drift families
```

Topology is deliberately excluded from `A` and moved to `F`.

The simplified structural factor is:

```text
structural_seed = local_family_energy + topology_context
context_weight = 1 / (1 + valid_trace_edges / service_count)
structural_energy = parent_context(structural_seed, context_weight)
structural_energy = counterfactual_explain_away(structural_energy)
F(v) = clip(scale(structural_energy(v)) / (A(v) + eps), 0, 1)
score(v) = A(v) * F(v)
```

The counterfactual explain-away transfer is data-derived:

```text
transfer = score_excess * mutation_share * propagation_share
```

where mutation and propagation shares are computed from current incident feature families, not labels or fixed feature weights.

## Validation Commands

```bash
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST1 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST1 --source CREST1 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST1_RAW --new CREST1 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

Guard result:

- No high-risk overfitting warnings.
- Existing medium notices are `rcabench_platform` import/docstring literals.

## Results

| version | AC@1 | MRR | AC@3 | AC@5 | error | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST1_RAW | 0.234177 | 0.419913 | 0.511252 | 0.640647 | 0 | 8.868140s |
| CREST1 | 0.699719 | 0.811469 | 0.916315 | 0.952180 | 0 | 8.799600s |

CREST1 passes Gate 1.

Compared with `CREST1_RAW`, CREST1 improves:

| metric | delta |
| --- | ---: |
| AC@1 | +0.465542 |
| MRR | +0.391556 |
| AC@3 | +0.405063 |
| AC@5 | +0.311533 |

Artifacts:

- Snapshot: `output/rcabench-platform-v2/evolve_snapshots/CREST1/`
- Summary: `docs/EvidRank_evolve/CREST1_summary.md`
- Compare: `docs/EvidRank_evolve/compare_CREST1_RAW_vs_CREST1.md`

## Failure Analysis

Weak groups after CREST1:

| fault_type | cases | AC@1 | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| pod-failure | 24 | 0.000000 | 0.166667 | 0.291667 |
| return | 21 | 0.476190 | 0.761905 | 0.809524 |
| unknown | 26 | 0.576923 | 0.807692 | 0.807692 |
| stress | 173 | 0.601156 | 0.930636 | 0.988439 |
| corrupt | 46 | 0.608696 | 0.913043 | 0.934783 |

Representative Top-1 miss components:

| datapack | GT | top1 | GT rank | node | A | F | C | score |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | ts-ui-dashboard | 33 | ts-ui-dashboard | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | ts-ui-dashboard | 33 | ts-travel-plan-service | 0.614222 | 0.983858 | 1.000000 | 0.604307 |
| ts3-mysql-pod-failure-58qts5 | mysql | ts-auth-service | 31 | ts-auth-service | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| ts3-mysql-pod-failure-58qts5 | mysql | ts-auth-service | 31 | mysql | 0.580047 | 0.915105 | 1.000000 | 0.530804 |

Interpretation:

- CREST1 fixed the catastrophic graph over-penalty from CREST1_RAW.
- Remaining hard misses are not mainly caused by `F`; they are caused by `A` assigning stronger telemetry drift to propagated or entry services than to infrastructure-local roots.
- Module 3 is still disabled, so `C=1` for all services.

## Decision

Accept CREST1 as the Gate 1 baseline because it:

- integrates as a standalone `Algorithm`;
- completes full eval with `error == 0`;
- passes `AC@1 >= 0.60`;
- has no high-risk guard warnings;
- avoids CERA3 expert feature tiers and any label/runtime leakage.

## Next Step

Proceed to Gate 2.

The next minimal hypothesis is:

```text
Cross-modal consistency should penalize entry/propagation services whose high A is driven by broad trace or volume drift, while preserving roots whose metric/log/trace evidence is concentrated and locally unusual.
```

Gate 2 should add Module 3 carefully and compare:

- `crest` vs `crest_nocalib`;
- `crest_local` vs `crest`;
- `crest_nocf` vs `crest`;
- CREST1 failure groups, especially `pod-failure`, `return`, and infrastructure-local cases.
