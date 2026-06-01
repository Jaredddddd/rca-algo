# EvidenceRank V6 Iteration

- Created: 2026-06-02T01:43:49+08:00
- Hypothesis: 异常期 trace 请求数上升与调用者自耗时相对增长可以互补识别高流量传播下的真实根因
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: combine a trace traffic-rise signal with a ShapleyIQ-inspired self-duration signal. Traffic rise captures services whose local request volume increases sharply in the abnormal window; self-duration subtracts direct child span time from each caller span, then scores services whose own execution time grows relative to their normal baseline.
- Why this should transfer beyond RCABench: both signals are computed from raw distributed traces using schema-level fields (`trace_id`, `span_id`, `parent_span_id`, `time`, `duration`, `service_name`). They do not depend on Train Ticket service names, datapack IDs, fault names, labels, injection metadata, `conclusion.parquet`, or previous algorithm outputs.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V5`.
- Baseline summary: `docs/EvidRank_evolve/V5_summary.md`.
- Baseline metrics: `AC@1=0.699015`, `AC@3=0.902954`, `AC@5=0.963432`, `MRR=0.810334`.
- Key weak groups: `ts-ui-dashboard`, `pod-failure`, `bandwidth`, `response-delay`, `request-replace-method`, and V5 Top-1 misses where the ground truth is already in Top-5 but high-traffic propagated services lead the ranking.
- Representative false cases: `ts5-ts-route-plan-service-response-delay-vjgk5j`, `ts0-ts-station-service-bandwidth-bp5k94`, and `ts3-ts-payment-service-pod-failure-fnlgp6`.

## Planned Change

- Minimal algorithm change: add `trace_count_rise_shift` and `trace_self_duration_relative_shift` to trace feature extraction and weighted rank fusion. `trace_count_rise_shift` is a sample-confident relative request-count increase. `trace_self_duration_relative_shift` computes span self time by subtracting direct child span interval union from each span duration, then compares abnormal vs normal service-level mean self time.
- Expected metric movement from offline replay of V5 scoring: weight `(trace_count_rise_shift=6.0, trace_self_duration_relative_shift=1.5)` gives `AC@1 0.699015 -> 0.765120`, `MRR 0.810334 -> 0.850565`, `AC@3 0.902954 -> 0.929677`, and keeps `AC@5=0.963432`.
- Known regression risk: count-rise can over-reward high-volume propagated services; self-duration can over-reward leaf/internal work that is slow but not causal. The chosen weights are below the highest-AC@1 sweep point because they preserve V5 Top-5 count in offline replay.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V6 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V6 --source V6 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V5 --new V6 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V6`.
- New summary: `docs/EvidRank_evolve/V6_summary.md`.
- Compare report: `docs/EvidRank_evolve/compare_V5_vs_V6.md`.
- Full evaluation completed 1422 datapacks with `error=0`.
- AC@1: `0.699015 -> 0.766526` (`+0.067511`, +96 Top-1 hits).
- AC@3: `0.902954 -> 0.922644` (`+0.019691`).
- AC@5: `0.963432 -> 0.961322` (`-0.002110`, -3 net Top-5 hits).
- MRR: `0.810334 -> 0.849078` (`+0.038744`).
- V6 false cases: `top1_miss=332`, `top5_miss=55`.

## Case Deltas

- Improved: `142` cases moved to Top-1 and `68` additional cases improved rank. The largest improved groups are `response-delay`, `request-delay`, `response-replace-code`, `partition`, and `request-replace-method`; common case services include `ts-basic-service`, `ts-ui-dashboard`, `ts-route-plan-service`, `ts-travel-service`, and `mysql`.
- Regressed: `46` cases regressed from Top-1 and `76` additional cases worsened rank. Top-5 gained `11` cases and lost `14` cases, for a net `AC@5` loss of `3`.
- Main regression pattern: the traffic-rise/self-duration signals can over-promote services with broad request-volume or local-work growth in `response-replace-code`, `request-replace-method`, `response-replace-body`, and `request-abort` cases. These regressions are concentrated around `ts-basic-service` and `ts-ui-dashboard`, but the failure mechanism is generic: strong local trace volume can be an effect of propagated or fan-out behavior rather than the cause.
- Representative Top-5 gains: `ts2-ts-consign-price-service-container-kill-lj9llf` (`19 -> 3`), `ts5-ts-route-plan-service-response-delay-vjgk5j` (`9 -> 4`), `ts0-ts-station-service-loss-hs8vrm` (`6 -> 2`).
- Representative Top-5 losses: `ts5-ts-travel-plan-service-response-replace-code-7626tx` (`4 -> 11`), `ts8-ts-food-service-response-replace-code-lsl65n` (`2 -> 9`), `ts6-ts-ui-dashboard-response-replace-code-tgfbsg` (`5 -> 9`).

## Decision

- Accept as V6.
- Reason: guard has no high-risk leakage warnings, full eval completed with `error=0`, `AC@1`, `AC@3`, and `MRR` all improve materially, and the `AC@5` decline is small (`3` net cases) with an interpretable mechanism.
- Next smallest general step: add a generic confidence gate or neighbor-contrast term for `trace_count_rise_shift`, so traffic-rise only receives full weight when it agrees with local endpoint/status/latency evidence or when the service's anomaly is stronger than its immediate trace neighbors. Validate with an ablation focused on recovering the V6 Top-5 losses without giving back the delay/request-volume gains.
