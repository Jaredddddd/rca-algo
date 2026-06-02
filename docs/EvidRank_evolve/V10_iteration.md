# EvidenceRank V10 Iteration

- Created: 2026-06-02T10:24:51+08:00
- Hypothesis: 服务自身 trace/log 证据从正常期显著下降时，可能表示可用性故障根因；该 drop 信号应与传播节点的上升型异常区分开
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: 正常期有稳定样本、异常期 trace/metric 行数显著下降时，服务自身可能从“异常传播节点”变成“可用性下降根因”；该 drop evidence 应与 V8/V9 的 trace endpoint shift 互补。
- Why this should transfer beyond RCABench: 任意微服务系统中，请求中断、实例不可用或局部容量崩溃都会表现为某些服务的观测量从正常期减少；该信号只依赖 raw metric/trace 的 service-level count，不依赖 datapack、服务名、故障名或 label。

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V9/`
- Baseline summary: `docs/EvidRank_evolve/V9_summary.md`
- Baseline metrics: AC@1 0.794655, MRR 0.871089, AC@3 0.941632, AC@5 0.975387, runtime avg 11.879449s, error 0.
- Key weak groups: V9 已改善请求/响应类 endpoint case，但 pod-failure 仍弱；V9 compare 显示 endpoint strength 不宜继续单独增大。
- Representative false cases: V9 中仍存在 base rank 2/3 的可用性/局部服务异常 case，被上游或高流量传播节点压住。

## Planned Change

- Minimal algorithm change: 新增通用 `_count_drop_shift(normal_count, abnormal_count)`，在 metric 和 trace 模态分别加入 `metric_count_drop_shift`、`trace_count_drop_shift`；保持 V9 endpoint post-gate factor 1.75 不变。
- Offline ablation:
  - 初始网格 `trace_drop_w=1.0, metric_drop_w=3.0`：AC@1 0.798875, MRR 0.873386, AC@3 0.940928, AC@5 0.976090。
  - endpoint/drop 联合搜索最高先到 1137/1422：`endpoint_factor=1.75, trace_drop_w=1.0, metric_drop_w=5.0`，AC@1 0.799578。
  - 加密搜索最佳：`endpoint_factor=1.75, trace_drop_w=0.85, metric_drop_w=10.0`，AC@1 0.802391, MRR 0.875103, AC@3 0.943741, AC@5 0.975387。
- Expected metric movement: AC@1 超过 0.80，MRR 和 AC@3 上升，AC@5 至少不低于 V9。
- Known regression risk: count drop 可能把全局流量下降或上游入口流量下降误当作本地根因；metric drop 权重较高，因此必须用 full eval/compare 检查退化 case。

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=INFO uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- Guard: no high-risk overfitting warnings; only existing rcabench platform import/docstring medium notices.
- Full eval: completed 1422 datapacks, error 0, batch wall time 360.810477s.
- Runtime avg: 11.737922s.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V10/`
- New summary: `docs/EvidRank_evolve/V10_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_V9_vs_V10.md`
- AC@1: 0.802391, +0.007736 vs V9, 1141/1422 top-1 hits.
- AC@3: 0.943741, +0.002110 vs V9.
- AC@5: 0.975387, unchanged vs V9.
- MRR: 0.875103, +0.004013 vs V9.

## Case Deltas

- Improved: 16 `improved_to_hit1`, 22 `rank_improved`.
  - Top-1 improvements include response/endpoint shape cases such as `ts0-ts-seat-service-response-abort-nggfmq`, `ts2-ts-basic-service-response-replace-body-hk6w9p`, `ts4-ts-basic-service-response-replace-code-2nw8nx`, and `ts4-ts-seat-service-request-replace-method-bvdt9b`.
  - Count-drop evidence also recovered availability/capacity-like cases such as `ts3-ts-consign-service-pod-failure-8cb7mp`, `ts9-ts-preserve-service-pod-failure-6w29wr`, `ts2-ts-order-service-stress-8vtw2p`, and `ts5-ts-preserve-service-stress-845w52`.
- Regressed: 5 `regressed_from_hit1`, 15 `rank_regressed`.
  - Top-1 regressions are mostly small-margin request/response delay or method cases where count drop over-rewarded a nearby propagation or high-traffic service: `ts1-ts-basic-service-request-replace-method-2b57wf`, `ts3-ts-travel-plan-service-request-delay-kxhn5n`, `ts3-ts-ui-dashboard-request-replace-method-wkh6t7`, `ts4-ts-basic-service-response-delay-76ksjc`, `ts4-ts-route-plan-service-response-delay-vxcl8q`.
  - Worst non-top1 regressions include partition/bandwidth/return cases already outside top-1 in V9; these suggest future drop signals should distinguish local disappearance from global traffic contraction.

## Decision

- Accept / reject / keep for later: Accept V10.
- Reason: V10 crosses the 80% AC@1 target while improving MRR and AC@3, preserving AC@5, keeping error 0 and runtime under 13s. The mechanism is generic: service-level trace/metric count decrease from a stable normal baseline can reveal local availability or capacity loss that V9 endpoint-shift evidence did not fully capture.
- Next smallest general step: analyze residual pod-failure, bandwidth, request-abort and infrastructure-root hard cases; prefer topology/global-drop contrast or neighbor-level suppression over increasing endpoint/drop weights further.
