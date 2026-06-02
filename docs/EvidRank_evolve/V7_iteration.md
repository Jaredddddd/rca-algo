# EvidenceRank V7 Iteration

- Created: 2026-06-02T02:53:29+08:00
- Hypothesis: raw trace endpoint 分布漂移可以补充 status residual，识别请求路径/入口形状变化强于单纯状态码变化的根因
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: add a lightweight endpoint-shape distribution shift from raw traces. V5 used `span_name + status` residuals after subtracting endpoint-only traffic mix. V7 tests whether the endpoint-only `span_name` distribution shift itself is useful as a lower-confidence companion signal when the fault changes request path, entry shape, or endpoint mix without producing a unique status residual.
- Design reference from other algorithms: MicroRCA/MicroHECL/MicroDig emphasize anomalous call paths and propagation-aware ranking. V7 does not import their random walk, service-name mapping, or alarm-item assumptions. It keeps the transferable part: anomalous behavior should be localized on raw trace endpoints before service-level fusion.
- Why this should transfer beyond RCABench: endpoint/span-name distribution drift is computed per service from `normal_traces.parquet` and `abnormal_traces.parquet`. It uses schema-level trace fields only, does not read labels, injection metadata, previous outputs, or `conclusion.parquet`, and has no datapack/service/fault branches.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V6`.
- Baseline summary: `docs/EvidRank_evolve/V6_summary.md`.
- Baseline metrics: `AC@1=0.766526`, `AC@3=0.922644`, `AC@5=0.961322`, `MRR=0.849078`, `top1_miss=332`, `top5_miss=55`.
- Key weak groups: `pod-failure`, `response-replace-body`, `request-abort`, `response-replace-code`, `bandwidth`, `request-replace-method`, and UI/front-door cases where status/volume symptoms still point to propagated services.
- Representative false cases: `ts8-ts-ui-dashboard-request-replace-method-xlwbzw`, `ts0-ts-basic-service-request-abort-62vtm2`, `ts7-ts-route-plan-service-response-replace-body-g2tfl4`, `ts0-mysql-container-kill-9t6n24`.

## Planned Change

- Minimal algorithm change: add `trace_endpoint_shift` to `BASE_FEATURE_NAMES`, `MODALITY_FEATURES`, `FEATURE_WEIGHTS`, and `_trace_features`. The feature is the existing L1 distribution shift helper over `span_name`, weighted by `log1p(min(normal_rows, abnormal_rows))`, then passed through the existing `log1p` normalization and trace parent-context smoothing.
- Expected metric movement from full offline ablation over all 1422 V6 cases: endpoint weight `6.0` gives `AC@1 0.766526 -> 0.782700`, `MRR 0.849078 -> 0.864911`, `AC@3 0.922644 -> 0.940928`, `AC@5 0.961322 -> 0.979606`, with `53` new Top-1 hits and `30` Top-1 regressions. A second weight-retuning grid was stopped after one pathological exploratory worker ran for more than 20 minutes; it is not used as evidence for the V7 decision.
- Known regression risk: endpoint-only shift can reward traffic mix changes and caller-visible propagation, especially in broad fan-out cases. The weight is intentionally lower than `trace_status_code_shift=16.0` and is treated as companion evidence rather than a dominant replacement for status residuals or self-duration.

## Commands

```bash
export LOGURU_LEVEL=WARNING
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V7 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V7 --source V7 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V6 --new V7 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- Guard: no high-risk warnings. Existing medium warnings are the pre-existing rcabench platform docstring/import literals.
- Full eval completed all `1422` datapacks with `error=0`.
- Batch walltime: `364.022205s` with `--use-cpus 48`; perf-report average `runtime.seconds=11.861259`.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V7`.
- New summary: `docs/EvidRank_evolve/V7_summary.md`.
- Compare report: `docs/EvidRank_evolve/compare_V6_vs_V7.md`.
- AC@1: `0.766526 -> 0.781997` (`+0.015471`, `1090 -> 1112`).
- AC@3: `0.922644 -> 0.940928` (`+0.018284`, `1312 -> 1338`).
- AC@5: `0.961322 -> 0.978903` (`+0.017581`, `1367 -> 1392`).
- MRR: `0.849078 -> 0.864359` (`+0.015280`).

## Case Deltas

- Improved: `52` V6 misses moved to Top-1, and `80` additional cases improved rank. Gains concentrate in `response-replace-code`, `request-replace-method`, `request-replace-path`, `response-abort`, `response-replace-body`, and UI/front-door endpoint-shape cases.
- Regressed: `30` V6 Top-1 hits regressed from Top-1, and `37` additional cases worsened rank. Main weak/regression area is generic rather than service-specific: endpoint-shape drift can over-promote caller-visible traffic mix or fan-out symptoms. `pod-failure` also regressed as a group (`AC@1 0.375000 -> 0.166667`), showing that endpoint evidence is actively unhelpful when the root is metric/infrastructure-local and HTTP symptoms are downstream.
- Top-5 improved materially despite regressions: top5 misses decreased from `55` to `30`.

## Decision

- Accept as V7.
- Reason: guard has no high-risk leakage warnings, full eval has `error=0`, and all headline metrics improve. The version is below the longer-term `80%-85%` AC@1 target, but it is a clean, documented, versioned improvement that also raises `AC@5` close to `0.98`.
- Next smallest general step: do not increase raw endpoint weight. Add a topology/cross-modal confidence gate for endpoint or traffic features, or add a metric-dominant fallback for services whose own metric anomaly is strong while endpoint evidence is weak or clearly propagated. Validate specifically against V7 `regressed_from_hit1` and pod-failure/bandwidth hard cases.
