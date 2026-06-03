# EvidenceRank V20 Iteration

- Created: 2026-06-02T23:13:47+08:00
- Hypothesis: 用无标签 causal pairwise objective 学 feature-family multiplier，并以 V11 语义权重为中心做正则化，得到可复现且更稳的全局 prior
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files changed:
  - `algorithms/evidencerank/calibrate_family_multipliers.py`
  - `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: keep V11's interpretable semantic feature prior, learn only coarse feature-family multipliers from unlabeled root-vs-propagation synthetic pairs, and regularize multipliers toward 1.0.
- Why this should transfer beyond RCABench: the learned variables are semantic RCA families rather than individual services, faults, case ids, or datapacks. The calibrator uses only raw incident observability frames and trace topology; it does not read labels, injection metadata, output rankings, perf reports, or conclusion parquet.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/V11/`
- Baseline summary: `docs/EvidRank_evolve/V11_summary.md`
- Baseline metrics: AC@1 0.802391, MRR 0.875337, AC@3 0.943741, AC@5 0.975387, error 0.
- Prior negative/partial experiments:
  - V18 naive unlabeled feature calibration: AC@1 0.506329.
  - V19 individual-feature causal calibration: AC@1 0.658931.
- Key V11 weakness retained as risk: pod-failure, request-abort, bandwidth, response-replace-body, and some dashboard/high-fanout cases.

## Planned Change

- Minimal algorithm change:
  - Add `calibrate_family_multipliers.py`, reusing V19's label-free synthetic causal pairs.
  - Partition V11 features into semantic families: `metric_magnitude`, `availability_drop`, `trace_latency`, `trace_traffic`, `trace_protocol`, `log_evidence`, `observability_volume`, `topology_context`.
  - Learn bounded family multipliers by pairwise logistic ranking: synthetic pseudo-roots should outrank topology-propagated victims and high-background services.
  - In `algorithm.py`, replace opaque per-feature V20 numbers with `SEMANTIC_FEATURE_PRIOR * CALIBRATED_FAMILY_MULTIPLIERS`.
- Expected metric movement: keep AC@1 near V11 and above 0.75, with small acceptable loss if the calibration story is stronger and AC@3/AC@5 do not materially degrade.
- Known regression risk: the unlabeled causal objective tends to upweight metric/availability and downweight trace/log/volume families. This can help pod-failure/local availability cases but may hurt request/response mutation, dashboard, traffic-shape, and delay cases if the bounds are too loose.

## Calibration Artifacts

- Wide exploratory command:

```bash
uv run --package evidencerank python algorithms/evidencerank/calibrate_family_multipliers.py \
  --data-root data/rcabench-platform-v2/data/rcabench \
  --workers 48 \
  --out docs/EvidRank_evolve/V20_family_calibration.json \
  --csv docs/EvidRank_evolve/V20_family_calibration.csv
```

- Wide result: multipliers clipped to the default wide bounds, e.g. metric/availability `1.28`, traffic/log/volume `0.72`; this was too aggressive for a robustness default.
- Final narrow command:

```bash
uv run --package evidencerank python algorithms/evidencerank/calibrate_family_multipliers.py \
  --data-root data/rcabench-platform-v2/data/rcabench \
  --workers 48 \
  --center-l2 4.0 \
  --min-multiplier 0.92 \
  --max-multiplier 1.08 \
  --out docs/EvidRank_evolve/V20_family_calibration_narrow.json \
  --csv docs/EvidRank_evolve/V20_family_calibration_narrow.csv
```

- Final narrow multipliers:
  - `metric_magnitude=1.08`
  - `availability_drop=1.08`
  - `trace_latency=0.92`
  - `trace_traffic=0.92`
  - `trace_protocol=0.92`
  - `log_evidence=0.92`
  - `observability_volume=0.92`
  - `topology_context=1.0`
- Training diagnostics from final artifact: final epoch 115410 pairs, base synthetic pair accuracy 0.775252, calibrated pair accuracy 0.777930, max absolute multiplier delta 0.08.
- Interpretation: the unlabeled objective gives a reproducible direction, but the meaningful mechanism is the bounded family-level regularizer, not free per-feature replacement.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V20 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V20 --source V20 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V11 --new V20 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V19 --new V20 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

- Guard: no high-risk warnings; only existing medium platform/docstring notices.
- Full eval: completed 1422 cases, error 0, batch duration 303.906394s.
- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/V20/`
- New summary: `docs/EvidRank_evolve/V20_summary.md`
- Compare reports: `docs/EvidRank_evolve/compare_V11_vs_V20.md`, `docs/EvidRank_evolve/compare_V19_vs_V20.md`
- V11 -> V20:
  - AC@1 0.802391 -> 0.789030 (-0.013361)
  - MRR 0.875337 -> 0.869097 (-0.006240)
  - AC@3 0.943741 -> 0.940225 (-0.003516)
  - AC@5 0.975387 -> 0.976793 (+0.001406)
- V19 -> V20:
  - AC@1 0.658931 -> 0.789030 (+0.130098)
  - MRR 0.776972 -> 0.869097 (+0.092124)
  - AC@3 0.877637 -> 0.940225 (+0.062588)
  - AC@5 0.927567 -> 0.976793 (+0.049226)

## Case Deltas

- V11 -> V20 status counts: `improved_to_hit1=5`, `rank_improved=16`, `rank_regressed=27`, `regressed_from_hit1=24`, `unchanged=1350`.
- Improvements vs V11: pod-failure/local availability and a few corrupt/partition cases. The learned 1.08 multiplier for metric magnitude and availability drop helps sparse local root evidence.
- Regressions vs V11: mostly request/response mutation, dashboard-entry, and basic/route-plan cases where trace protocol, traffic, log, or volume evidence was already important and V20 scales those families down by 0.92.
- V19 -> V20 status counts: `improved_to_hit1=267`, `rank_improved=97`, `rank_regressed=47`, `regressed_from_hit1=82`, `unchanged=929`.
- Interpretation: family-level regularization recovers almost all of V11's stability while preserving a label-free calibration path; individual-feature replacement in V19 was too free.

## Required Interpretation

- 失败机制：V18/V19 这类更自由的无监督权重学习会把 synthetic objective 的偏好直接灌进 per-feature weights，容易过度偏向局部 drop/status 或压低真实系统里仍重要的 trace/log/volume 传播信号。
- 当前 EvidenceRank 为什么会错：如果继续使用完全固定的 V11 数字，论文中难以解释这些权重来源；如果直接替换成 V19 individual-feature weights，又会造成大幅准确率退化。V20 介于两者之间：固定的是可解释语义先验，学习的是无标签 family multiplier。
- 可泛化的新信号或组合方式：以 domain-semantic prior 为中心，用未标注 incident 的 root-vs-propagation pairwise objective 学 family-level multipliers，并通过强正则和窄边界限制自由度。
- 可能改善的 case 类型：pod-failure、container/local availability、metric magnitude 和 count-drop 更根因特异的 cases。
- 可能退化的 case 类型：request/response mutation、dashboard/high-fanout、traffic-shape、delay、log/template 证据较关键的 cases。
- 最小代码改动位置：`calibrate_family_multipliers.py` 负责离线无标签学习；`algorithm.py` 中 `SEMANTIC_FEATURE_PRIOR`、`CALIBRATED_FAMILY_MULTIPLIERS`、`FEATURE_FAMILIES` 负责在线固定使用校准后的通用 prior。
- 验证指标和 ablation 方式：wide vs narrow family calibration；guard；full eval；perf-report；snapshot；summary；V11/V20 compare；V19/V20 compare。
- 是否接受该版本以及理由：接受 V20 作为鲁棒性/论文叙事版本。它相对 V11 只有小幅 AC@1/MRR/AC@3 下降，AC@5 略升，且远优于 V19；它把固定权重解释为“语义先验 + 无标签 family 校准”，比手工 per-feature 常数更 defensible。

## Decision

- Accept / reject / keep for later: accept V20 as the current EvidenceRank default for robustness and paper-facing calibration.
- Reason: V20 满足目标约束：guard 无 high-risk，full eval error 0，AC@1 保持在 0.789030，明显高于 0.75 容忍线；同时给权重来源提供了可复现的无标签 family-level calibration algorithm。
- Paper-facing conclusion: 不应声称完全无监督 individual-feature learning 已经足够；更稳健的结论是 EvidenceRank 使用可解释语义先验，并通过无标签 causal family calibration 自动学习有限倍率。这个设计既避免 RCABench label 拟合，也避免 V19 那种自由度过高导致的退化。
- Next smallest general step: 若继续提升，可做跨 corpus 或 bootstrap 稳定性分析，给 family multiplier 置信区间；在线算法仍只使用固定的校准后 prior，不读取任何评估或 ground truth。
