# EvidenceRank V18 Iteration

- Created: 2026-06-02T20:49:51+08:00
- Hypothesis: 用无标签 incident corpus 的全局特征覆盖、证据集中度和跨模态一致性离线校准 feature prior，使 EvidenceRank 的权重可复现而非手工硬编码
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files changed: `algorithms/evidencerank/calibrate_feature_weights.py`; temporary scoring experiment in `algorithms/evidencerank/src/evidencerank/algorithm.py` was reverted after rejection.
- General RCA mechanism being tested: learn a global feature prior from unlabeled incident folders by measuring each feature's service-level coverage, evidence concentration, top-rank gap, robust scale, and agreement with independent modality evidence.
- Why this should transfer beyond RCABench: the calibration objective only uses raw normal/abnormal observability frames and service-level feature matrices. It does not use labels, injection metadata, output rankings, or case/service/fault identifiers. The same script can be run on any corpus of unlabeled incidents before deploying EvidenceRank.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V11/`
- Baseline summary: `docs/EvidRank_evolve/V11_summary.md`
- Baseline metrics: AC@1 0.802391, MRR 0.875337, AC@3 0.943741, AC@5 0.975387, error 0.
- Key weak groups: V11 is still relatively weak on pod-failure, request-abort, response-replace-body, bandwidth, and some infrastructure-root cases.
- Representative false cases: only used through V11/V18 summaries and compare reports for offline analysis; none enter algorithm code.

## Planned Change

- Minimal algorithm change:
  - Add an offline calibrator that scans raw incident folders and emits `docs/EvidRank_evolve/V18_unlabeled_calibration.json` plus `.csv`.
  - Temporarily replace `FEATURE_WEIGHTS` with generated weights to test whether the learned unlabeled global prior can serve as the main online prior.
  - After full evaluation, restore the accepted V11 weights because the generated prior was rejected.
- Expected metric movement: a successful unlabeled global prior should keep AC@1 near the 0.75 robustness tolerance while improving the paper-facing weight-source argument.
- Known regression risk: the global objective can confuse "feature is sharp and agrees with broad symptoms" with "feature is causally reliable". In particular, log error and trace duration can be over-promoted, while status/endpoint/rise features can be underweighted relative to V11.

## Calibration Artifact

- Command:

```bash
uv run --package evidencerank python algorithms/evidencerank/calibrate_feature_weights.py \
  --data-root data/rcabench-platform-v2/data/rcabench \
  --workers 48 \
  --out docs/EvidRank_evolve/V18_unlabeled_calibration.json \
  --csv docs/EvidRank_evolve/V18_unlabeled_calibration.csv
```

- Output artifact: `docs/EvidRank_evolve/V18_unlabeled_calibration.json`
- CSV table: `docs/EvidRank_evolve/V18_unlabeled_calibration.csv`
- Calibrated high weights:
  - `metric_count_drop_shift=12.536544`, close to V11's strong availability/drop prior.
  - `log_error_rate=5.032783`, much higher than V11 and later shown to be unsafe.
  - `trace_status_code_shift=4.894545`, much lower than V11's 16.0.
  - `trace_endpoint_shift=2.920254` and `trace_count_rise_shift=1.372194`, both lower than V11's strong endpoint/traffic-shape priors.
- Interpretation before eval: the unlabeled objective captures "local disappearance" well, but it over-trusts log error-rate sharpness and underestimates protocol/status mutation evidence.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- Guard: no high-risk warnings; only existing platform/docstring medium notices.
- Generated-prior full eval: completed 1422 cases, error 0, batch duration 311.100284s.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V18/`
- New summary: `docs/EvidRank_evolve/V18_summary.md`
- Compare reports: `docs/EvidRank_evolve/compare_V11_vs_V18.md`, `docs/EvidRank_evolve/compare_V17_vs_V18.md`
- AC@1: 0.802391 -> 0.506329 (-0.296062 vs V11)
- AC@3: 0.943741 -> 0.833333 (-0.110408 vs V11)
- AC@5: 0.975387 -> 0.941632 (-0.033755 vs V11)
- MRR: 0.875337 -> 0.684853 (-0.190484 vs V11)
- Restore verification: after rejecting V18 generated weights, `algorithm.py` was restored to the accepted V11 weights; guard passed again; full eval rerun completed 1422 cases and perf-report returned AC@1 0.802391, MRR 0.875337, AC@3 0.943741, AC@5 0.975387, error 0.

## Case Deltas

- Improved vs V11: 46 `improved_to_hit1` and 29 additional `rank_improved` cases.
  - Improvements concentrate in pod-failure, stress/corrupt, and some local availability-like cases where the generated calibration strongly rewards count-drop or local metric/trace duration anomalies.
- Regressed vs V11: 467 `regressed_from_hit1` and 131 additional `rank_regressed` cases.
  - Regressions are broad and severe on response-replace-code/body, request-abort, dashboard-entry, and basic-service groups.
  - Weak groups in V18 include response-abort AC@1 0.159091, response-replace-code AC@1 0.186147, request-abort AC@1 0.233333, response-replace-body AC@1 0.235294.

## Decision

- Accept / reject / keep for later: reject V18 generated weights as the default EvidenceRank prior; keep the calibrator and artifacts as a negative ablation and paper-facing analysis tool.
- Reason: the method is label-free and reproducible, but the naive global reliability objective does not preserve V11's causal feature ordering. It over-promotes sharp log/duration symptoms and underweights protocol/status/endpoint features that are empirically critical for request/response mutation cases. The AC@1 drop to 0.506329 is below the robustness tolerance.
- Failure mechanism: global feature agreement measures symptom co-occurrence, not causal direction. Logs and duration often agree with propagated high-volume victims; status/endpoint changes may be lower scale but more causally specific. Pure inverse-scale reliability therefore produces a plausible-looking but wrong prior.
- Current EvidenceRank why it would be wrong if accepted: it would replace a high-accuracy, accepted V11 with a weaker prior that regresses 467 existing Top-1 hits and harms AC@3/AC@5.
- General signal learned: unsupervised offline calibration is useful, but the objective needs causality-aware constraints, such as topology direction, root-vs-victim contrast, and modality-specific false-positive penalties. It should not simply reward concentration plus agreement.
- Possible improvements: pod-failure, stress/corrupt, and local availability cases where count-drop evidence is a strong signal.
- Possible regressions: response/request mutation cases, dashboard-entry cases, and log/duration-heavy propagation cases.
- Minimal next step: keep V11 as the online default; use the new calibrator to derive diagnostics, then design a constrained calibration objective that preserves known observability semantics without using labels. Candidate constraints: cap log-only prior unless supported by trace status/endpoint evidence; learn family-level rather than individual-feature priors; use topology neighbor contrast as a self-supervised negative signal.
- Validation and ablation: V18 was validated with guard, full eval, perf-report, snapshot, summary, V11/V18 compare, V17/V18 compare, and a restore full eval.
