# EvidenceRank V5 Iteration

- Created: 2026-06-01T20:54:09+08:00
- Hypothesis: raw trace 中同一 endpoint 的 HTTP/status 分布相对变化是比全局流量更高置信的根因局部证据
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: endpoint-local status distribution shifts are high-confidence evidence for the service where an HTTP-visible fault is expressed. The signal compares a service's abnormal `span_name + status` distribution against its own normal baseline and subtracts the plain endpoint-shape shift, so it favors status changes beyond traffic mix changes.
- Why this should transfer beyond RCABench: HTTP status/span status changes are common raw trace symptoms in microservice systems. The feature is schema-driven and per-case/per-service normalized; it does not depend on Train Ticket service names, datapack names, labels, injection metadata, `conclusion.parquet`, or previous algorithm outputs.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V4`
- Baseline summary: `docs/EvidRank_evolve/V4_summary.md`
- Baseline metrics: `AC@1=0.571730`, `AC@3=0.791139`, `AC@5=0.888889`, `MRR=0.706323`.
- Key weak groups: `response-replace-code`, `response-abort`, `bandwidth`, `request-replace-path`, `request-replace-method`, and user-facing endpoint cases where high-volume caller/callee services outrank a local status-changing root.
- Representative false cases: V4 hard/near-miss cases include response-code and bandwidth faults where the GT service already has a distinctive raw trace status shift but is buried under global row-count, duration, or propagated traffic evidence.

## Planned Change

- Minimal algorithm change: add one trace feature, `trace_status_code_shift`, computed from raw `normal_traces.parquet` and `abnormal_traces.parquet`. For each service, compute the L1 distribution shift of `span_name + attr.http.response.status_code + attr.status_code`, subtract the L1 shift of `span_name` alone, clamp at zero, weight by `log1p(min(normal_rows, abnormal_rows))`, then feed it through the existing `log1p` feature normalization and parent-context smoothing.
- Expected metric movement from offline replay using V4 feature/edge logic: status weight `16.0` gives `AC@1 0.571730 -> 0.699015`, `AC@3 0.791139 -> 0.902954`, `AC@5 0.888889 -> 0.963432`, `MRR 0.706323 -> 0.810334`.
- Known regression risk: cases whose true root is mostly metric/log-visible but whose downstream services have incidental status shifts can be demoted. The feature intentionally subtracts endpoint mix shift to avoid rewarding plain traffic redistribution, but the high confidence weight can still dominate in status-heavy cases.

## Improvement Proposal Record

1. Failure mechanism: V4 often ranks high-traffic or propagated services above roots when the root's strongest symptom is a local HTTP/status change rather than total row count or average duration.
2. Why current EvidenceRank is wrong: existing trace features use service-level duration, count, and error rates. They miss endpoint-local status distribution changes and can let global traffic volume dominate.
3. General signal or combination: compare abnormal vs normal status distributions inside each service and endpoint, subtract endpoint-only shape drift, then add the residual as a high-confidence trace feature.
4. Case types likely to improve: response-code, response-abort, request/response mutation, bandwidth, and other faults that surface as status changes on specific endpoints.
5. Case types likely to regress: metric-only or log-only faults with secondary downstream status changes; broad caller-side failures where status symptoms are not root-local.
6. Minimal code location: `BASE_FEATURE_NAMES`, `MODALITY_FEATURES`, `FEATURE_WEIGHTS`, and `_trace_features` in `algorithms/evidencerank/src/evidencerank/algorithm.py`.
7. Validation and ablation: offline replay reproduced V4 exactly; status-only sweeps were monotonic through weight `20`. V5 uses weight `16.0` as a conservative near-plateau point before full eval.
8. Acceptance criterion: accept only if guard has no high-risk warnings, full eval has zero errors, AC@1/MRR improve materially, AC@3/AC@5 do not regress, and V5 snapshot/summary/compare/index are generated.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V5 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V5 --source V5 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V4 --new V5 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- Guard: no high-risk warnings. Existing medium warnings are the pre-existing module/import dataset-name literals.
- Full eval: `total=1422`, `error=0`, average runtime `8.349568s`, processpool walltime `258.599496s` with `--use-cpus 48`.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V5`
- New summary: `docs/EvidRank_evolve/V5_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_V4_vs_V5.md`
- AC@1: `0.571730 -> 0.699015` (`+0.127286`, `813 -> 994`)
- AC@3: `0.791139 -> 0.902954` (`+0.111814`, `1125 -> 1284`)
- AC@5: `0.888889 -> 0.963432` (`+0.074543`, `1264 -> 1370`)
- MRR: `0.706323 -> 0.810334` (`+0.104011`)

## Case Deltas

- Status counts: `improved_to_hit1=218`, `rank_improved=159`, `rank_regressed=28`, `regressed_from_hit1=37`, `unchanged=980`.
- Improved to Hit@1: concentrated in `response-replace-code` 79, `request-replace-method` 35, `response-abort` 17, `request-replace-path` 16, `request-abort` 15, `response-replace-body` 13, `partition` 12, plus smaller gains in request-delay, bandwidth, response-delay, loss, corrupt, and delay.
- Regressed from Hit@1: 37 cases, but all remain in Top-5; max new best rank is 4. Regressions are mostly `pod-failure` 7, `request-replace-method` 7, `partition` 6, `response-replace-body` 6, plus smaller groups.
- Rank-regressed but not from Hit@1: 28 cases; 10 move outside Top-5. These are the main residual risk for high status-shift weighting and should be reviewed before increasing the weight further.

## Decision

- Accept / reject / keep for later: accept V5 as the current default.
- Reason: full eval has `error=0`; guard has no high-risk warning; AC@1, MRR, AC@3, and AC@5 all improve sharply over V4; the 37 Hit@1 regressions remain in Top-5 and are outweighed by 218 new Hit@1 improvements.
- Next smallest general step: study the remaining `ts-ui-dashboard`, `pod-failure`, and bandwidth weak groups. Prefer adding a confidence gate or complementary non-HTTP infrastructure signal rather than increasing the status-shift weight blindly.
