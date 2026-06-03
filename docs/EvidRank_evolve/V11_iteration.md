# EvidenceRank V11 Iteration

- Created: 2026-06-02T14:19:25+08:00
- Hypothesis: 单 case 内按模态证据覆盖、集中度和跨模态一致性自适应缩放固定先验权重，同时消除重复输入读取以降低运行时间
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: 在保留 V10 固定 feature prior 的前提下，用单 case 内的模态覆盖、证据集中度、峰值对比度估计无监督可靠度，对 metric/trace/log 做小幅动态缩放；同时去除同一 case 内重复读取 raw parquet 的纯工程开销。
- Why this should transfer beyond RCABench: 模态是否有足够正证据、证据是否集中、是否能形成相对峰值，是微服务 RCA 中跨系统适用的证据质量判断；性能优化只改变数据加载路径，不改变任何 RCABench 特有逻辑。

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V10/`
- Baseline summary: `docs/EvidRank_evolve/V10_summary.md`
- Baseline metrics: AC@1 0.802391, MRR 0.875103, AC@3 0.943741, AC@5 0.975387, runtime avg 11.737922s, error 0.
- Key weak groups: pod-failure, request-abort, response-replace-body, bandwidth and infrastructure-root cases remain weaker; V10 also warns that stronger drop weights can regress small-margin request/response cases.
- Representative false cases: V10 hard cases include pod-failure and bandwidth cases where high-traffic propagation nodes outrank the local root; V11 does not target case names in code and uses these only for offline validation.

## Planned Change

- Minimal algorithm change:
  - Load the six raw input parquet files once per case and reuse the DataFrames for service collection and feature construction.
  - Skip disabled modality feature extraction for metric/log/trace variants while preserving the all-raw-input service candidate set.
  - Add `_adaptive_feature_weights`, which keeps V10 `FEATURE_WEIGHTS` as priors and applies bounded per-case modality factors based on unsupervised evidence reliability.
- Expected metric movement: AC@1/AC@3/AC@5 should stay at V10 level; runtime avg should decrease from 11.737922s because duplicate parquet reads are removed.
- Known regression risk: even bounded adaptive scaling can move small-margin top-1 ties between metric/trace/log evidence; if AC@1 or MRR drops materially, keep the performance refactor and reject or damp the adaptive scaling.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V11/`
- New summary: `docs/EvidRank_evolve/V11_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_V10_vs_V11.md`
- Full eval: 1422 cases, error 0, batch wall time 297.697896s with `--use-cpus 48`.
- Runtime avg: 9.635375s, down from V10 11.737922s (-2.102547s, -17.91%).
- Variant smoke: `EvidenceRank`, `EvidenceRankMetric`, `EvidenceRankLog`, `EvidenceRankTrace`, `EvidenceRankMetricLog`, `EvidenceRankMetricTrace`, and `EvidenceRankLogTrace` all returned 49 ranked services on one raw-input case without writing formal eval output.
- AC@1: 0.802391 -> 0.802391 (+0.000000)
- AC@3: 0.943741 -> 0.943741 (+0.000000)
- AC@5: 0.975387 -> 0.975387 (+0.000000)
- MRR: 0.875103 -> 0.875337 (+0.000234)
- Avg@3: 0.880450 -> 0.880919 (+0.000469)
- Avg@5: 0.916315 -> 0.916596 (+0.000281)

## Adaptive Weight Ablation

- Trial snapshot: `output/rcabench-platform-v2/evolve_snapshots/V11_trial_span008/`
- Trial compare: `docs/EvidRank_evolve/compare_V10_vs_V11_trial_span008.md`
- Direct bounded adaptive scaling without a stability gate produced AC@1 0.801688 and MRR 0.874985. It improved 2 ranks but introduced 1 `regressed_from_hit1` case, so it was rejected as the default V11 behavior.
- Final V11 keeps the same unsupervised modality reliability estimate, but applies the adaptive score only when the top-1 service is unchanged relative to the V10 prior-weight score. This keeps top-1 stability while allowing lower-rank ordering to benefit from case-local evidence reliability.

## Case Deltas

- Improved: 2 `rank_improved` cases, both rank 3 -> rank 2.
- Regressed: 0; no `regressed_from_hit1`, no `rank_regressed`, and no top-5 loss.
- Unchanged: 1420 cases.
- Improved examples from compare:
  - `ts0-ts-ui-dashboard-response-replace-code-lflx8j`: GT rank 3 -> 2.
  - `ts5-ts-order-other-service-stress-6wvd48`: GT rank 3 -> 2.

## Proposal Checklist

- Failure mechanism: the V10 scoring path repeatedly read the same raw parquet files per case and used fixed modality priors even when a case-local modality had weak coverage or diffuse evidence.
- Why current EvidenceRank can be wrong: fixed weights cannot distinguish a sharply concentrated, well-supported modality from a noisy but present modality; repeated I/O and per-service filtering add runtime without adding evidence.
- General signal or fusion: estimate each modality's unsupervised reliability from positive evidence support, concentration and p95-vs-median contrast, then apply a small bounded scaling around the V10 prior.
- Likely improved case types: small-margin cases where a reliable secondary modality should move the GT higher inside top-3/top-5 without changing the primary root candidate.
- Likely regressed case types: small-margin top-1 cases where the fixed prior already protects the root from a high-traffic propagation node; this was observed in the rejected direct-scaling trial.
- Minimal code location: `algorithms/evidencerank/src/evidencerank/algorithm.py`, limited to input frame reuse, feature extraction loops, and `_adaptive_feature_weights`.
- Validation and ablation: run `guard`, full batch eval, perf-report, V10 vs V11 compare, plus the direct-scaling ablation `V11_trial_span008`.
- Acceptance: accept V11 because guard has no high-risk alerts, full eval has error 0, AC@1/AC@3/AC@5 are unchanged, MRR improves slightly, and runtime avg drops 17.91%.

## Decision

- Accept / reject / keep for later: accept V11.
- Reason: V11 satisfies the user's constraint that AC@1 and other headline accuracy metrics remain unchanged, while removing duplicate raw parquet reads and adding a conservative unsupervised adaptive-weight path. The accepted path is label-free, does not read `labels.csv`, `injection.json`, output, perf reports or `conclusion.parquet`, and does not hardcode dataset, datapack, service or fault names.
- Next smallest general step: profile the remaining per-case time inside trace feature construction and replace more per-service DataFrame scans with grouped/vectorized statistics, while keeping the V11 scoring output stable as the regression target.
