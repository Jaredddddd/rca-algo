# EvidenceRank V16 Iteration

- Created: 2026-06-02T18:35:41+08:00
- Hypothesis: 以 metric+trace 作为无监督主干视图，log 只在与主干排序一致时按一致性自适应加入，从而用 case-local modality agreement 替代固定模态权重并降低噪声模态拖累
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: V13-V15 show that removing fixed priors is feasible but noisy modalities, especially logs, can drag Top-1 below the robustness target. V16 learns modality participation from case-local agreement: metric+trace form the primary structural/symptom backbone, and log evidence is only blended when its ranking agrees with that backbone.
- Why this should transfer beyond RCABench: metric and trace usually provide continuous symptoms plus causal call structure; logs are valuable but bursty and instrumentation-dependent. Requiring log agreement with non-log evidence is a general observability reliability rule, not a dataset-specific service or fault rule.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V15/`
- Baseline summary: `docs/EvidRank_evolve/V15_summary.md`
- Reference accepted version: V11 has AC@1 0.802391, MRR 0.875337, AC@3 0.943741, AC@5 0.975387.
- Key weak groups: V15 is especially weak on pod-failure, response-replace-body/code, and request replacement groups; many failures are high-volume victim or entry services outranking the root.
- Representative false cases: V15 hard cases include availability-like pod/container failures and response replacement cases where log/traffic bursts dominate. These are used only for offline validation and do not enter algorithm logic.

## Planned Change

- Minimal algorithm change:
  - Restore the simpler self-consistency feature learner that uses robust scaled columns only, because V15's raw-effect locality term over-penalized availability evidence.
  - Score a metric+trace backbone when both modalities are available.
  - Score the full enabled modality set and the log-only view separately.
  - Blend the full score into the backbone only in proportion to log/backbone cosine agreement and top-k overlap; otherwise return the backbone score.
- Expected metric movement: recover above V15 and V14 toward the best no-fixed-prior metric+trace behavior, while keeping no fixed per-feature weight table.
- Known regression risk: log-only root cases may be underweighted if metric/trace evidence is sparse; metric+trace victim nodes can still outrank infrastructure roots without the earlier fixed priors.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=INFO uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V16/`
- New summary: `docs/EvidRank_evolve/V16_summary.md`
- Compare reports: `docs/EvidRank_evolve/compare_V15_vs_V16.md`, `docs/EvidRank_evolve/compare_V11_vs_V16.md`
- `evidencerank` full eval: error 0, runtime.avg 9.866908s, AC@1 0.583685, MRR 0.739592, AC@3 0.877637, AC@5 0.945851.
- Delta vs V15: AC@1 -0.054852, MRR -0.032542, AC@3 -0.007032, AC@5 -0.003516.
- Delta vs V11: AC@1 -0.218706, MRR -0.135745, AC@3 -0.066104, AC@5 -0.029536.
- Perf-report also listed existing variant outputs such as `evidencerank_metric_trace`, but the V16 batch command only reran `-a evidencerank`. Those variant rows are not valid V16 ablation evidence. They were treated only as a hypothesis signal and were explicitly tested in V17's main path.

## Case Deltas

- Improved vs V15: 82 cases moved to hit@1 and 108 additional cases improved in rank. These improvements are mostly cases where metric/trace self-consistency promotes a local service symptom without relying on fixed feature priors.
- Regressed vs V15: 160 cases regressed from hit@1 and 118 additional cases regressed in rank. V16 remains weak on dashboard-entry, response replacement, request replacement, and some pod-failure cases.
- Improved vs V11: 50 cases moved to hit@1.
- Regressed vs V11: 361 cases regressed from hit@1.

## Decision

- Accept / reject / keep for later: reject as the default version; keep as an ablation and failure record.
- Reason: removing the fixed feature-weight table is robust in principle, but V16's log agreement gate is too permissive. Even bounded blending with the full log view pulls the main algorithm below V15. The apparent metric+trace side signal in perf-report was not a same-version ablation because variants were not rerun by the batch command.
- Failure mechanism: log evidence is bursty and broad in many incidents. When blended into a full score, it can promote entry, high-volume, or victim services that share logs with the true root but are not the root.
- Current EvidenceRank error mode: the case-local agreement gate measures distribution similarity between log and backbone rankings, but a small full-score blend can still flip Top-1 in close cases.
- General signal to keep: unsupervised feature self-consistency and modality-level reliability should be learned from the current incident, but noisy modalities should be allowed to participate only under a stricter acceptance rule.
- Possible improvements: cases where metrics and traces jointly expose the faulty component, especially local service/resource anomalies.
- Possible regressions: log-only failures or incidents with sparse metric/trace evidence.
- Minimal next code change: make the full `evidencerank` main path use the metric+trace backbone when both modalities exist, and only fall back to log/full evidence if the backbone is unavailable.
- Verification: run `guard`, full eval, snapshot V17, summarize V17, compare V16/V17 and V11/V17. The target is to validate whether the metric+trace backbone hypothesis holds when implemented in the main algorithm, not to rely on stale variant output.
