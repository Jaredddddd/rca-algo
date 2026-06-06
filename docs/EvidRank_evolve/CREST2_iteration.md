# CREST2 Iteration

- Created: 2026-06-06
- Algorithm registry name: `crest`
- Dataset: `rcabench`
- Gate: Gate 2 target check
- Goal: push CREST from the Gate 1 baseline to `AC@1 >= 0.80` without labels, LLMs, pretrained models, or CERA ordinal feature tiers.

## Constraints

- Runtime CREST reads only the normal/abnormal metric, trace, and log parquet frames under `args.input_folder`.
- Runtime CREST does not read labels, injection metadata, previous outputs, perf reports, historical rankings, ground truth, or `conclusion.parquet`.
- No datapack id, service name, fault name, random suffix, or dataset split is hardcoded.
- CERA's ordinal tier / ladder expert weights are not used.
- Labels are used only in offline summary, compare, and diagnostic scripts.

## Hypothesis

CREST1 passed Gate 1, but its `score = A * F` form still lost many cases where a true root has moderate local evidence and several downstream or entry services show maximum trace-duration and volume drift.

The Gate 2 hypothesis is:

```text
Counterfactual explanatory power should be paired with a denoised structural support channel. The extra channel should keep broad multi-feature structural evidence while excluding standalone trace duration, which is often a propagated symptom rather than root evidence.
```

## Code Changes

Updated `algorithms/evidencerank/src/evidencerank/crest.py`:

- Increased incident-local robust feature clipping from `1.0` to `3.0` so strong but not top-ranked root evidence is not compressed too early.
- Added `_denoised_channel_energy(...)`, which sums the case-scaled feature matrix except `trace_duration_z`.
- Added a denoised structural support term `S` by applying the same parent-context and counterfactual explain-away operators to the denoised channel.
- Changed the accepted counterfactual score to:

```text
score(v) = A(v) * F(v) * C(v) + S(v) * C(v)
```

For CREST2, `C(v)=1` in the accepted default because the current incident-local cross-modal consistency factor is too aggressive for sparse root evidence.

The registered ablation entrypoints are present:

- `crest_local`: Module 1 only.
- `crest_nocf`: Module 1 plus PageRank-style graph prior.
- `crest_nocalib`: accepted CREST2 with calibration disabled.

## Validation Commands

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST2 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST2 --source CREST2 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST1 --new CREST2 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST1_RAW --new CREST2 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

| version | AC@1 | MRR | AC@3 | AC@5 | error | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST1_RAW | 0.234177 | 0.419913 | 0.511252 | 0.640647 | 0 | 8.868140s |
| CREST1 | 0.699719 | 0.811469 | 0.916315 | 0.952180 | 0 | 8.799600s |
| CREST2 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 0 | 8.744964s |

Compared with `CREST1`, CREST2 improves:

| metric | delta |
| --- | ---: |
| AC@1 | +0.100563 |
| MRR | +0.063856 |
| AC@3 | +0.028129 |
| AC@5 | +0.019691 |

Case status delta versus `CREST1`:

| status | cases |
| --- | ---: |
| improved_to_hit1 | 193 |
| rank_improved | 78 |
| rank_regressed | 48 |
| regressed_from_hit1 | 50 |
| unchanged | 1053 |

Artifacts:

- Snapshot: `output/rcabench-platform-v2/evolve_snapshots/CREST2/`
- Summary: `docs/EvidRank_evolve/CREST2_summary.md`
- Compare with CREST1: `docs/EvidRank_evolve/compare_CREST1_vs_CREST2.md`
- Compare with CREST1_RAW: `docs/EvidRank_evolve/compare_CREST1_RAW_vs_CREST2.md`

Final checks:

- `guard`: no high-risk overfitting warnings. Existing medium notices are limited to `rcabench_platform` import/docstring literals.
- `compileall`: `crest.py` and `main.py` compile successfully.
- Smoke check: `local`, `pagerank`, default `counterfactual`, and `counterfactual + calibration` scoring modes all produce service rankings on a representative case.

## Calibration Check

The Module 3 consistency factor is implemented as `_cross_modal_consistency(...)`, but enabling it in the accepted score is rejected for now.

Offline diagnostic run:

| variant | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | ---: | ---: | ---: | ---: | --- |
| CREST2 default, `C=1` | 0.800281 | 0.875326 | 0.944444 | 0.971871 | accept |
| CREST2 with `use_calibration=True` | 0.632208 | 0.764479 | 0.882560 | 0.938115 | reject |

Interpretation:

- Cross-modal variance currently penalizes true roots when the root is weakly observable in one or two modalities.
- The accepted algorithm keeps calibration as a diagnostic and ablation switch, not as the primary ranking factor.
- A future calibration term should be uncertainty-aware by modality availability and root-victim topology role, not just variance across normalized modality scores.

## Failure Analysis

Representative Top-1 misses after CREST2:

| datapack | GT | top1 | GT rank | node | A | F | C | S | score |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | ts-ui-dashboard | 33 | ts-ui-dashboard | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 2.000000 |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | ts-ui-dashboard | 33 | ts-travel-plan-service | 0.571964 | 0.571964 | 1.000000 | 0.581723 | 0.908866 |
| ts3-mysql-pod-failure-58qts5 | mysql | ts-auth-service | 31 | ts-auth-service | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 2.000000 |
| ts3-mysql-pod-failure-58qts5 | mysql | ts-auth-service | 31 | mysql | 0.552236 | 0.544249 | 1.000000 | 0.577797 | 0.878351 |

Failure mechanism:

- CREST2 reaches the target by improving many rank-2 cases, but the hardest pod-failure and infrastructure-local cases remain weak.
- In these cases, the true root has moderate `A` and `S`; the mistaken top1 service saturates both channels.
- The issue is not a NaN, graph loop, or missing output. It is a root-victim separation problem when a low-observability root causes high-observability entry or propagation services to dominate all incident-local scales.

## Decision

Accept CREST2 as the current CREST target version because:

- full eval completes with `error == 0`;
- AC@1 reaches the requested `0.8` target;
- MRR, AC@3, and AC@5 all improve over CREST1;
- runtime remains comparable to CREST1;
- the mechanism is data-derived and label-free at runtime;
- calibration was tested and rejected rather than silently enabled.

## Next Step

The next minimal research hypothesis is:

```text
Add a topology-role contrast for low-observability roots: if a candidate has moderate local mutation/drop evidence and its high-scoring neighbors look like broad trace-duration or volume victims, transfer only the victim-symptom portion of S rather than adding a global denoised channel.
```

This should target pod-failure and infrastructure-local misses without increasing the already-saturated entry-service scores.
