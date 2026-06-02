# EvidenceRank V9 Iteration

- Created: 2026-06-02T10:13:56+08:00
- Hypothesis: 保留 V8 endpoint confidence gate，但对 gate 后仍幸存的本地 endpoint 分布漂移做温和补偿，可抵消传播型大数值特征对请求形状根因的淹没
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: V8 correctly discounts endpoint drift that lacks status/count support, but several true request-shape roots still lose to broad metric, duration, and row-count evidence from propagated traffic. V9 tests a small post-gate compensation for endpoint evidence that survives the V8 confidence gate.
- Why this should transfer beyond RCABench: the rule uses only per-service raw trace endpoint distribution drift already computed from `normal_traces.parquet` and `abnormal_traces.parquet`. It does not branch on datapack, service, fault type, dataset split, label, injection metadata, or historical outputs.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V8`.
- Baseline summary: `docs/EvidRank_evolve/V8_summary.md`.
- Baseline metrics: `AC@1=0.788326`, `AC@3=0.939522`, `AC@5=0.973980`, `MRR=0.866904`, `top1_miss=301`, `top5_miss=37`.
- Key weak groups: `request-replace-method`, `response-replace-code`, `request-abort`, `response-replace-body`, `pod-failure`, and `bandwidth`.
- Representative false cases: `ts4-ts-ui-dashboard-request-replace-method-gbwc6b`, `ts6-ts-basic-service-request-replace-method-4qzglm`, `ts0-ts-travel-plan-service-pod-failure-sxz5ll`, `ts0-ts-station-service-bandwidth-bp5k94`.

## Planned Change

- Minimal algorithm change: keep `_apply_trace_endpoint_support_gate` unchanged in structure, but multiply the endpoint contribution that remains after the V8 unsupported-endpoint penalty by `TRACE_ENDPOINT_POST_GATE_FACTOR=1.75`.
- Offline ablation: a raw trace `span_name + HTTP method` residual signal produced no ranking change, because `span_name` already contains method/path in the available trace schema. A small endpoint post-gate multiplier gave the best full-case offline replay among tested candidates.
- Expected metric movement from offline replay over all `1422` V8 cases: `AC@1=0.794655` (`1121 -> 1130`), `MRR=0.871089`, `AC@3=0.941632`, `AC@5=0.975387`.
- Known regression risk: multiplying endpoint evidence can revive some propagation-visible endpoint drift that V8 intentionally suppressed. The multiplier is applied after the V8 gate, so unsupported endpoint-only evidence is still partially discounted before compensation.

## Commands

```bash
export LOGURU_LEVEL=WARNING
python -m compileall algorithms/evidencerank/src/evidencerank
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V9 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V9 --source V9 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V8 --new V9 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- Guard: no high-risk warnings. Existing medium warnings are the pre-existing rcabench platform docstring/import literals.
- Full eval completed all `1422` datapacks with `error=0`.
- Batch walltime: `363.991289s` with `--use-cpus 48`; perf-report average `runtime.seconds=11.879449`, still below the requested 13 second target.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V9`.
- New summary: `docs/EvidRank_evolve/V9_summary.md`.
- Compare report: `docs/EvidRank_evolve/compare_V8_vs_V9.md`.
- AC@1: `0.788326 -> 0.794655` (`+0.006329`, `1121 -> 1130`).
- AC@3: `0.939522 -> 0.941632` (`+0.002110`, `1336 -> 1339`).
- AC@5: `0.973980 -> 0.975387` (`+0.001406`, `1385 -> 1387`).
- MRR: `0.866904 -> 0.871089` (`+0.004185`).

## Case Deltas

- Improved: `25` V8 misses moved to Top-1 and `43` additional cases improved rank. Gains concentrate in request/response shape cases where endpoint evidence should remain visible after V8's confidence gate: `request-replace-method` on `ts-ui-dashboard`, `response-replace-code` on `ts-ui-dashboard`/`ts-basic-service`, and `response-replace-body` on `ts-basic-service`.
- Regressed: `16` V8 Top-1 hits regressed from Top-1 and `30` additional cases worsened rank. Regressions are scattered across `corrupt`, `request-delay`, `request-replace-method`, `pod-failure`, `partition`, `request-abort`, `response-*`, `return`, and `stress`; `pod-failure` weak-group metrics fell from `AC@1=0.166667` to `0.125000`.
- Top-5 tradeoff: net Top-5 improves by `2` cases overall, but `pod-failure` top5 misses increase (`5 -> 7`). This suggests the endpoint compensation is acceptable globally but should not be pushed further.

## Decision

- Accept as V9, with caution.
- Reason: guard has no high-risk leakage warnings, full eval has `error=0`, `AC@1`, `MRR`, `AC@3`, and `AC@5` all improve, and average runtime remains under 13 seconds. The change is a single generic post-gate endpoint compensation and does not read labels, injections, conclusions, outputs, service names, or fault names in the algorithm path.
- Next smallest general step: do not further increase endpoint strength. Focus on the remaining deep `pod-failure` and `bandwidth` hard cases with a separate topology/availability signal, likely detecting services whose own trace/log/metric presence drops or disappears while neighbors show propagated rises.
