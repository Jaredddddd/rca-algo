# CREST3 Iteration

- Created: 2026-06-06
- Algorithm registry name: `crest`
- Dataset: `rcabench`
- Gate: Gate 2 + Gate 3 ablation verification
- Goal: make the accepted CREST implementation satisfy the full `A * F * C` design while keeping `AC@1 >= 0.80`.

## Constraints

- Runtime CREST reads only normal/abnormal metric, trace, and log parquet frames under `args.input_folder`.
- Runtime CREST does not read labels, injection metadata, previous outputs, perf reports, historical rankings, ground truth, or `conclusion.parquet`.
- No LLM, external API, pretrained neural network, or label-trained model is used.
- No datapack id, service name, fault name, random suffix, or dataset split is hardcoded.
- CERA's ordinal tier / ladder expert feature weights are not used.
- Labels are used only in offline summary, compare, ablation, and diagnostic scripts.

## Hypothesis

CREST2 reached `AC@1 >= 0.80`, but it kept Module 3 disabled in the accepted default because the raw cross-modal consistency factor was too aggressive.

CREST3 tests a milder uncertainty calibration:

```text
C(v) = 0.96 + 0.04 * raw_consistency(v)
```

where `raw_consistency` is derived from normalized metric/trace/log modality agreement and coverage. The floor keeps calibration in the CREST scoring path while preventing sparse but valid root evidence from being suppressed.

## Code Changes

Updated `algorithms/evidencerank/src/evidencerank/crest.py`:

- Added `CREST_CALIBRATION_FLOOR = 0.96`.
- Changed `_cross_modal_consistency(...)` from a direct penalty to a trust-region calibration in `[0.96, 1.0]`.
- Enabled calibration in primary `CREST`.
- Kept `crest_nocalib` as the direct no-calibration ablation.
- Kept `crest_nocf` as the PageRank / Random Walk replacement for counterfactual propagation.
- Kept `crest_local` as Module 1 only.

Accepted score:

```text
score(v) = A(v) * F(v) * C(v) + S(v) * C(v)
```

where:

- `A`: normality-regularized local abnormality.
- `F`: counterfactual structural explanatory power.
- `C`: mild cross-modal uncertainty calibration.
- `S`: denoised structural support excluding standalone `trace_duration_z`.

## Validation Commands

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST3 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST3 --source CREST3 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST2 --new CREST3 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST1 --new CREST3 --algorithm crest --dataset rcabench
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest_nocalib -d rcabench --clear --use-cpus 32
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest_nocf -d rcabench --clear --use-cpus 32
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest_local -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

| version | AC@1 | MRR | AC@3 | AC@5 | error | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST1 | 0.699719 | 0.811469 | 0.916315 | 0.952180 | 0 | 8.799600s |
| CREST2 / NoCalib | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 0 | 8.783818s |
| CREST3 | 0.800281 | 0.875744 | 0.945851 | 0.972574 | 0 | 8.769954s |

Compared with `CREST2`, CREST3 changes only a small number of cases:

| status | cases |
| --- | ---: |
| improved_to_hit1 | 12 |
| rank_improved | 18 |
| rank_regressed | 10 |
| regressed_from_hit1 | 12 |
| unchanged | 1370 |

Metric delta versus `CREST2`:

| metric | delta |
| --- | ---: |
| AC@1 | +0.000000 |
| MRR | +0.000418 |
| AC@3 | +0.001406 |
| AC@5 | +0.000703 |

Artifacts:

- Snapshot: `output/rcabench-platform-v2/evolve_snapshots/CREST3/`
- Summary: `docs/EvidRank_evolve/CREST3_summary.md`
- Compare with CREST2: `docs/EvidRank_evolve/compare_CREST2_vs_CREST3.md`
- Compare with CREST1: `docs/EvidRank_evolve/compare_CREST1_vs_CREST3.md`

Final checks:

- `guard`: no high-risk overfitting warnings. Existing medium notices are limited to `rcabench_platform` import/docstring literals.
- `compileall`: `crest.py` and `main.py` compile successfully.
- `index`: `VibeResearchTools/VibeResearch.md` refreshed and includes the CREST3 documents.

## Gate 3 Ablation

Official ablation metrics:

| variant | module removed / replaced | AC@1 | MRR | AC@3 | AC@5 | error |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `crest` | none | 0.800281 | 0.875744 | 0.945851 | 0.972574 | 0 |
| `crest_nocalib` | remove Module 3 calibration | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 0 |
| `crest_nocf` | replace counterfactual propagation with PageRank-style graph prior | 0.492264 | 0.665531 | 0.813643 | 0.936709 | 0 |
| `crest_local` | use Module 1 only | 0.705345 | 0.824138 | 0.939522 | 0.967651 | 0 |

Interpretation:

- Module 1 alone is usable but not sufficient for the 0.8 target.
- Replacing counterfactual propagation with PageRank collapses AC@1, supporting that CREST's counterfactual structural operation is not just graph centrality.
- Mild Module 3 calibration is a small but positive ranking stabilizer: AC@1 stays unchanged while MRR, AC@3, and AC@5 improve over NoCalib.

## Failure Analysis

Representative hard misses after CREST3:

| datapack | GT | top1 | GT rank | node | A | F | C | S | score |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | ts-ui-dashboard | 33 | ts-ui-dashboard | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 2.000000 |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | ts-ui-dashboard | 33 | ts-travel-plan-service | 0.571964 | 0.571964 | 1.000000 | 0.581723 | 0.908866 |
| ts3-mysql-pod-failure-58qts5 | mysql | ts-auth-service | 31 | ts-auth-service | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 2.000000 |
| ts3-mysql-pod-failure-58qts5 | mysql | ts-auth-service | 31 | mysql | 0.552236 | 0.544249 | 1.000000 | 0.577797 | 0.878351 |

Failure mechanism:

- Hard pod-failure and infrastructure-local cases remain dominated by high-observability entry or propagation services.
- In representative cases, both the mistaken top1 and the GT have high consistency, so Module 3 cannot separate them.
- The missing signal is not cross-modal consistency; it is topology-role contrast for weak roots and strong downstream victims.

## Decision

Accept CREST3 as the current CREST implementation because:

- It uses the full CREST score with an enabled `C` factor.
- It reaches the requested `AC@1 >= 0.8` target under full eval.
- It improves MRR, AC@3, and AC@5 over the no-calibration CREST2 baseline.
- Gate 3 ablations are implemented and officially evaluated.
- Guard and compile checks pass; no runtime leakage is introduced by the calibration change.

## Next Step

The next minimal hypothesis is:

```text
Add topology-role contrast for low-observability roots: when a candidate has moderate mutation/drop evidence and its neighbors have saturated duration or volume victim symptoms, transfer only the victim-symptom portion of S instead of globally amplifying high-observability services.
```

This should target the remaining pod-failure and infrastructure-local misses without sacrificing the broad request/response mutation cases that CREST3 already ranks well.
