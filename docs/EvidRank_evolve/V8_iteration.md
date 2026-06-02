# EvidenceRank V8 Iteration

- Created: 2026-06-02T03:44:55+08:00
- Hypothesis: endpoint 分布漂移需要由状态码残差或调用量上升提供支撑，缺少支撑的 endpoint-only 信号更可能是传播症状
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: V7 added raw trace endpoint distribution drift and improved request/response path-shape cases, but it also over-promoted some caller-visible or fan-out symptoms. V8 tests a lightweight confidence gate: endpoint drift is strongest when supported by a status-code residual or abnormal trace-count rise; unsupported endpoint-only drift is partially discounted as possible propagation.
- Design reference from other algorithms: MicroRCA, MicroHECL, and MicroDig emphasize anomalous call paths and propagation direction. V8 keeps the transferable part as a trace-evidence confidence rule, without importing random walk outputs, service mappings, labels, injections, or algorithm-specific result files.
- Why this should transfer beyond RCABench: the gate uses only per-service raw trace feature contributions already computed by EvidenceRank (`trace_endpoint_shift`, `trace_status_code_shift`, `trace_count_rise_shift`). It is schema-level and does not branch on datapack, service, fault, dataset split, or ground truth.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V7`.
- Baseline summary: `docs/EvidRank_evolve/V7_summary.md`.
- Baseline metrics: `AC@1=0.781997`, `AC@3=0.940928`, `AC@5=0.978903`, `MRR=0.864359`, `top1_miss=310`, `top5_miss=30`.
- Key weak groups: `pod-failure`, `response-replace-body`, `request-abort`, `bandwidth`, `request-replace-method`, and cases where V7 endpoint evidence ranks propagated traffic shape above the root service.
- Representative false cases: `ts0-ts-travel-plan-service-pod-failure-sxz5ll`, `ts3-mysql-pod-failure-58qts5`, `ts4-ts-route-plan-service-bandwidth-z6g6ng`, `ts8-ts-ui-dashboard-request-replace-method-xlwbzw`.

## Planned Change

- Minimal algorithm change: after log-normalization and feature weighting, apply `_apply_trace_endpoint_support_gate`. The gate computes `unsupported_endpoint = max(0, endpoint - 2.0 * status_residual - 1.5 * count_rise)` and subtracts `0.5 * unsupported_endpoint` from the endpoint contribution. All constants are feature-confidence weights, not case-specific branches.
- Expected metric movement from full offline replay over all `1422` V7 cases: best candidate reached `AC@1=0.788326`, `MRR=0.866845`, `AC@3=0.939522`, `AC@5=0.974684`, with `16` V7 misses moved to Top-1 and `7` V7 Top-1 hits regressed. This remains below the long-term `80%-85%` AC@1 target, but is a low-runtime general gate worth full validation.
- Rejected exploratory candidates: a topology neighbor endpoint penalty gave only `+4` Top-1 with AC@5 loss; metric-dominant fallback hurt AC@1; a broader cross-modal grid was interrupted because the exploratory script followed an inefficient raw self-duration recomputation path and produced no usable result.
- Known regression risk: the gate can suppress true endpoint-only failures such as request path/method/body mutations that do not produce clear status residuals or count rise. The penalty is partial rather than hard-zeroing endpoint evidence to preserve those cases.

## Commands

```bash
export LOGURU_LEVEL=WARNING
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V8 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V8 --source V8 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V7 --new V8 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- Guard: no high-risk warnings. Existing medium warnings are the pre-existing rcabench platform docstring/import literals.
- Full eval completed all `1422` datapacks with `error=0`.
- Batch walltime: `360.756970s` with `--use-cpus 48`; perf-report average `runtime.seconds=11.721153`.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V8`.
- New summary: `docs/EvidRank_evolve/V8_summary.md`.
- Compare report: `docs/EvidRank_evolve/compare_V7_vs_V8.md`.
- AC@1: `0.781997 -> 0.788326` (`+0.006329`, `1112 -> 1121`).
- AC@3: `0.940928 -> 0.939522` (`-0.001406`, `1338 -> 1336`).
- AC@5: `0.978903 -> 0.973980` (`-0.004923`, `1392 -> 1385`).
- MRR: `0.864359 -> 0.866904` (`+0.002546`).

## Case Deltas

- Improved: `16` V7 misses moved to Top-1 and `20` additional cases improved rank. Gains concentrate in cases where V7 endpoint drift over-promoted caller-visible symptoms and V8 let status/count-supported services win: `corrupt`, `request-delay`, `response-delay`, `loss`, and a small number of bandwidth/container-kill cases.
- Regressed: `7` V7 Top-1 hits regressed from Top-1 and `25` additional cases worsened rank. The main regression pattern is `request-replace-method` (`4` Top-1 regressions and most Top-5 losses), where endpoint-only drift is a true root signal even when status residual and count rise are weak.
- Top-5 tradeoff: `8` cases that were V7 Top-5 hits moved out of Top-5. This is an expected risk of endpoint gating and is not a runtime or leakage issue, but it shows V8 should not be followed by stronger endpoint penalties.

## Decision

- Accept as V8, with caution.
- Reason: guard has no high-risk leakage warnings, full eval has `error=0`, and both `AC@1` and `MRR` improve without a large or unexplained `AC@3`/`AC@5` collapse. The change is a low-cost generic confidence gate, and V8 remains better than V6 on all headline metrics. However, it is still below the long-term `80%-85%` AC@1 target and loses some request-method endpoint-only cases, so the mechanism is accepted only as a moderate refinement rather than a final direction.
- Next smallest general step: do not increase endpoint penalties. Focus on a selective exemption or companion signal for true endpoint-only request-shape faults, ideally from raw traces only: method/path/span-name novelty that is local to the service and not broadly repeated across neighbors. Validate first against the V8 request-replace-method regressions and against the remaining `pod-failure`/`bandwidth` hard cases.
