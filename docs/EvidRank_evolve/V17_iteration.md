# EvidenceRank V17 Iteration

- Created: 2026-06-02T18:46:14+08:00
- Hypothesis: 当 metric+trace 无监督主干可用时，将日志视为低置信辅助模态而非默认混合模态，可以用观测模态可靠性替代固定特征先验并提升迁移鲁棒性
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: V16 showed that the no-fixed-prior metric+trace backbone is much stronger than the full log-blended main path. V17 treats logs as low-confidence auxiliary evidence when both metric and trace are present, so the main ranking is driven by unsupervised feature weights over continuous symptoms and call-structure evidence.
- Why this should transfer beyond RCABench: metrics and traces are generally less sparse and less instrumentation-text-dependent than logs. A metric+trace backbone is a common observability reliability rule, not a case, service, or fault-specific rule.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V16/`
- Baseline summary: `docs/EvidRank_evolve/V16_summary.md`
- Reference accepted version: V11 has AC@1 0.802391, MRR 0.875337, AC@3 0.943741, AC@5 0.975387, but uses a fixed feature-weight table.
- V16 main metrics: AC@1 0.583685, MRR 0.739592, AC@3 0.877637, AC@5 0.945851.
- Hypothesis signal: perf-report listed an existing `evidencerank_metric_trace` output with AC@1 0.704641, but that variant was not rerun by the V16 `-a evidencerank` batch. V17 tests the same idea in the main path.
- Key weak groups: V16 is weak on dashboard-entry and request/response replacement cases where broad log or entry-side symptoms promote high-volume victim services.
- Representative false cases: V16 hard false cases listed in `docs/EvidRank_evolve/V16_summary.md`; labels and injection metadata are used only in reports, not in algorithm logic.

## Planned Change

- Minimal algorithm change: keep the V16 unsupervised feature self-consistency learner, but when the enabled modalities contain metric, trace, and log, return the metric+trace backbone score instead of blending full log scores into the backbone.
- Expected metric movement: recover the main `evidencerank` result toward the V16 `evidencerank_metric_trace` ablation while preserving no fixed per-feature weight table.
- Known regression risk: log-only or log-dominant incidents can lose Top-1 influence when metric+trace evidence exists but is weak.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V17/`
- New summary: `docs/EvidRank_evolve/V17_summary.md`
- Compare reports: `docs/EvidRank_evolve/compare_V16_vs_V17.md`, `docs/EvidRank_evolve/compare_V11_vs_V17.md`
- Full eval: error 0, runtime.avg 9.767386s, AC@1 0.563291, MRR 0.724849, AC@3 0.868495, AC@5 0.939522.
- Delta vs V16: AC@1 -0.020394, MRR -0.014743, AC@3 -0.009142, AC@5 -0.006329.
- Delta vs V11: AC@1 -0.239100, MRR -0.150488, AC@3 -0.075246, AC@5 -0.035865.

## Case Deltas

- Improved vs V16: 4 cases moved to hit@1 and 9 additional cases improved in rank.
- Regressed vs V16: 33 cases regressed from hit@1 and 86 additional cases regressed in rank.
- Regressed pattern: many regressions are dashboard-entry or request/response replacement cases where ignoring log/full evidence removed a useful symptom and allowed other high-volume services to outrank the ground-truth set.

## Decision

- Accept / reject / keep for later: reject as default; keep as a negative ablation.
- Reason: the metric+trace-only main path did not recover the apparent side-output metric; it further reduced AC@1 and MRR. The previous perf-report variant row was not a same-version ablation, so using it as a target was misleading.
- Failure mechanism: with no fixed feature priors, metric+trace evidence alone over-emphasizes broad structural and traffic symptoms in close cases. Logs are noisy, but fully suppressing them removes useful localized evidence for request/response mutation and entry-side failures.
- Current EvidenceRank why it would be wrong if accepted: it would replace a high-accuracy accepted V11 with a much weaker no-fixed-prior experiment, below the user's robustness tolerance.
- General signal learned: no-fixed feature weights need either a stronger unsupervised calibration objective or an explicit paper-facing justification for fixed priors; simple case-local self-consistency is not enough.
- Possible improvements: a small subset of local service anomalies where logs act mostly as distractors.
- Possible regressions: log-dominant, entry-side, request/response replacement, and multi-GT cases.
- Minimal next step: do not leave V17 in the default algorithm. Restore the accepted V11 implementation and document V13-V17 as no-fixed-prior ablations. A future robust path should learn global priors from unlabeled incidents through an offline calibration objective, not from labels.
- Verification: V17 guard had no high-risk warnings before eval; after rejection, `algorithm.py` was restored to the accepted implementation and recompiled.
