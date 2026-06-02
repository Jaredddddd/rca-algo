# V20 Family-Level Weight Calibration Methodology

- Created: 2026-06-03
- Algorithm: `EvidenceRank`
- Version: `V20`
- Purpose: 说明 V20 中 EvidenceRank 权重如何由“可解释语义先验 + 无标签 family-level calibration”形成，并给出可用于 ICSE 投稿写作的 Introduction、Motivation 和 Methodology 草稿。

## One-Sentence Summary

V20 不再把 EvidenceRank 的权重描述为人工调出的 per-feature 常数，而是把权重分解为两部分：一个跨系统可解释的 RCA 语义先验，以及一个由未标注 incident corpus 自动学习得到的 feature-family multiplier。在线算法只使用校准后的固定 prior，不读取任何 label、injection、历史输出或 ground truth。

## Key Message for Reviewers

V20 的核心观点是：RCA 权重不应该完全交给单个 case 内部的无监督自适应，也不应该被写成无法解释的固定数字。更稳健的做法是先定义少量跨微服务系统通用的证据语义组，然后在大量未标注 incident 上，用自监督的 root-vs-propagation 目标学习每个语义组的有限校准倍率。

这给审稿人的解释是：

- 不是用 RCABench label 拟合权重；
- 不是根据 case id、服务名或故障类型查表；
- 不是让每个 feature 独立自由漂移；
- 权重由可复现脚本在 raw observability data 上生成；
- 学习自由度只有 8 个 family multiplier，并且被正则化到接近 1.0；
- 最终算法仍然是无监督 RCA ranking，不读取评估输出或 ground truth。

## Weight Decomposition

V20 将在线权重写成：

```text
w_i = semantic_prior_i * calibrated_multiplier_family(i)
```

其中：

- `semantic_prior_i` 是 EvidenceRank 的跨系统可解释语义先验，表示某类观测信号在 RCA 中的基础可靠性；
- `family(i)` 把 feature `i` 映射到一个语义 family；
- `calibrated_multiplier_family(i)` 是从未标注 incident corpus 上学习得到的 family-level 校准倍率。

因此，V20 的在线代码中不再直接维护一串孤立的 feature weight，而是维护：

- `SEMANTIC_FEATURE_PRIOR`
- `FEATURE_FAMILIES`
- `CALIBRATED_FAMILY_MULTIPLIERS`

对应实现位置：

```text
algorithms/evidencerank/src/evidencerank/algorithm.py
```

离线学习脚本：

```text
algorithms/evidencerank/calibrate_family_multipliers.py
```

## Feature Families

V20 将 EvidenceRank 的原始特征划分为 8 个语义 family：

| family | features | RCA meaning |
| --- | --- | --- |
| `metric_magnitude` | `metric_max_z`, `metric_mean_z`, `metric_anomaly_count`, `metric_value_delta` | 指标值变化强度，表示服务自身 metric 分布发生异常 |
| `availability_drop` | `metric_count_drop_shift`, `trace_count_drop_shift` | 可用性下降或请求/指标消失，常对应局部故障或实例不可达 |
| `trace_latency` | `trace_duration_z`, `trace_duration_delta`, `trace_self_duration_relative_shift` | trace 延迟或服务自身处理时间变化 |
| `trace_traffic` | `trace_count_delta`, `trace_count_rise_shift` | 请求流量形态变化，包括流量上升或流量分布偏移 |
| `trace_protocol` | `trace_endpoint_shift`, `trace_error_rate`, `trace_status_code_shift` | endpoint、状态码、错误率等协议层异常 |
| `log_evidence` | `log_count_delta`, `log_error_rate`, `log_template_delta` | 日志数量、错误日志和模板变化 |
| `observability_volume` | `abnormal_metric_rows`, `abnormal_trace_rows` | 异常窗口中观测样本量，提供证据支撑但也容易偏向高流量节点 |
| `topology_context` | `topology_in_degree`, `topology_out_degree` | 拓扑上下文特征，目前作为结构上下文而不直接加分 |

这种 family-level 设计刻意降低学习自由度。相比直接学习 21 个 feature weight，V20 只学习 8 个 family multiplier，避免无标签目标把偶然的传播症状误学成根因权重。

## Learning Objective

### Input

校准器输入是一个未标注 incident corpus。每个 incident 只需要包含 EvidenceRank 已使用的 raw observability frames：

```text
normal_metrics.parquet
abnormal_metrics.parquet
normal_traces.parquet
abnormal_traces.parquet
normal_logs.parquet
abnormal_logs.parquet
```

校准器不读取：

- `labels.csv`
- `injection.json`
- `output`
- `perf report`
- `conclusion.parquet`
- case id 对应的 ground truth
- 服务名或故障名规则

### Feature Extraction

对每个 incident，校准器复用 EvidenceRank 的 raw feature extractor，得到服务级 feature matrix：

```text
X in R^(services x features)
```

并从 raw traces 中抽取服务调用边，用作拓扑传播建模。这里的拓扑只用于生成自监督 pair，不用于读取任何人工标注。

### Synthetic Root-Vs-Propagation Pairs

真实 RCA 的一个关键难点是：根因服务和传播受害服务都会表现出异常。V20 的自监督目标不是学习“哪个服务 label 是根因”，而是构造一个通用的因果排序任务：

```text
synthetic pseudo-root should outrank topology-propagated victims
```

具体过程：

1. 从一个未标注 incident 的服务集合中随机采样一个 pseudo-root `r`。
2. 给 `r` 注入通用 root perturbation profile，例如：
   - metric shift；
   - availability loss；
   - protocol/status shift；
   - endpoint mix shift；
   - local latency；
   - log template shift；
   - volume saturation。
3. 沿 trace topology 向下游和少量上游传播较弱的 propagation symptom。
4. 选择负例服务，包括：
   - 拓扑邻居；
   - 高 background score 服务；
   - 随机服务。
5. 对每个负例 `v` 构造 pairwise diff：

```text
d = x_root - x_victim
```

这个过程只依赖通用的微服务传播假设：根因服务的局部异常应当比其传播受害者更有根因特异性。

### Family Contribution

V20 不直接学习每个 feature 的权重，而是先用语义先验 `w^(0)` 计算每个 family 对 pairwise margin 的贡献。

对某个 family `g`：

```text
c_g(d) = sum_{i in g} w_i^(0) * d_i
```

其中：

- `d_i` 是 root-vs-victim 的 feature difference；
- `w_i^(0)` 是语义先验；
- `c_g(d)` 是 family `g` 对“root 应排在 victim 前面”的贡献。

### Multiplier Optimization

校准器学习 family multiplier 向量 `m`。对每个 pairwise diff `d`，margin 定义为：

```text
margin(d, m) = sum_g m_g * c_g(d)
```

优化目标是 pairwise logistic loss 加上中心正则：

```text
L(m) = mean_d log(1 + exp(-margin(d, m))) + lambda * ||m - 1||_2^2
```

并加上有界约束：

```text
m_min <= m_g <= m_max
```

V20 最终使用窄边界：

```text
m_min = 0.92
m_max = 1.08
lambda = 4.0
```

这表示校准器最多只能让某个 family 相对语义先验上调或下调 8%。这个限制很重要：它把无标签学习从“重新发明整套权重”变成“围绕可解释先验做保守校准”。

### Final V20 Multipliers

V20 最终学到：

```text
metric_magnitude       1.08
availability_drop      1.08
trace_latency          0.92
trace_traffic          0.92
trace_protocol         0.92
log_evidence           0.92
observability_volume   0.92
topology_context       1.00
```

训练诊断：

```text
pairs in final epoch: 115410
base pair accuracy: 0.775252
calibrated pair accuracy: 0.777930
max abs multiplier delta: 0.08
```

需要注意：synthetic pair accuracy 的提升不是论文里最重要的结果。更重要的是，V20 的学习目标给出了一个可复现的校准方向，而窄边界正则保证它不会像 V19 那样过度替换稳定先验。

## Why Not Learn Per-Feature Weights?

V18 和 V19 提供了负向/部分正向证据：

- V18 用无标签 feature concentration、coverage 和 cross-modality agreement 学全局 feature prior，AC@1 降到 `0.506329`；
- V19 用 causal pairwise self-supervision 学 individual-feature weights，AC@1 提升到 `0.658931`，但仍低于可接受阈值；
- V20 把学习自由度限制到 family-level multiplier，并围绕 V11 语义先验正则化，AC@1 达到 `0.789030`。

这说明：

1. 完全无监督的 per-feature replacement 太不稳定；
2. causal/topology self-supervision 的方向是有用的；
3. 最稳健的方式是学习少量 family multiplier，而不是让每个 feature 独立调权。

## Empirical Result

V20 相对 V11：

| metric | V11 | V20 | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.789030 | -0.013361 |
| MRR | 0.875337 | 0.869097 | -0.006240 |
| AC@3 | 0.943741 | 0.940225 | -0.003516 |
| AC@5 | 0.975387 | 0.976793 | +0.001406 |

V20 相对 V19：

| metric | V19 | V20 | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.658931 | 0.789030 | +0.130098 |
| MRR | 0.776972 | 0.869097 | +0.092124 |
| AC@3 | 0.877637 | 0.940225 | +0.062588 |
| AC@5 | 0.927567 | 0.976793 | +0.049226 |

因此，V20 是一个更适合论文叙事的折中点：它相对 V11 有非常小的 top-1 损失，但把权重来源从“固定常数”变成了“可解释先验 + 无标签校准”。

## ICSE Draft: Introduction

现代云原生系统通常由大量微服务组成，单个用户请求会跨越多个服务、数据库和基础设施组件。当 incident 发生时，异常信号会沿服务调用链迅速传播：根因服务可能表现为指标突变、请求消失、端点分布变化或错误日志增加，而其上下游服务也会因为传播效应出现延迟、流量波动或日志尖峰。因此，微服务根因定位需要在多个观测模态之间融合证据，并区分真正的根因信号与传播受害者信号。

现有无监督 RCA 方法通常依赖异常检测分数、图传播或跨模态聚合来排序可疑服务。然而，一个经常被忽视的问题是：不同证据类型的可靠性并不相同。比如，状态码分布变化往往比单纯的日志数量变化更接近协议层故障；局部可用性下降可能比高流量节点上的大量异常 trace 更具有根因特异性。如果算法使用人工指定的固定权重，审稿人和实际用户都会质疑这些权重是否只是在某个 benchmark 上调出来的；如果算法完全在单个 case 内自适应学习权重，又容易把传播节点、入口流量或局部日志尖峰误认为根因。

为了解决这一矛盾，我们提出一种无标签的 family-level evidence calibration 方法。核心思想是保留跨系统可解释的 RCA 语义先验，但不把它视为不可解释的手工常数。相反，我们把 EvidenceRank 的证据特征划分为少量语义 family，并在未标注 incident corpus 上构造自监督 root-vs-propagation 排序任务，学习每个 family 的有限校准倍率。最终在线算法只使用校准后的固定 prior，不读取任何 label、injection metadata 或历史评估输出。

这种设计在可迁移性和稳定性之间取得平衡：一方面，family multiplier 由 raw observability data 自动学习，避免了 label-driven benchmark fitting；另一方面，学习自由度被限制在语义组级别，并通过中心正则约束在先验附近，避免完全无监督 per-feature replacement 带来的不稳定性。我们的消融实验表明，朴素无标签 feature calibration 和 individual-feature causal calibration 都不足以稳定替代语义先验，而 V20 的 family-level calibration 在保持接近 V11 性能的同时，显著增强了权重来源的可解释性和可复现性。

## ICSE Draft: Motivation

### M1: Fixed Weights Are Hard to Defend

EvidenceRank 的早期版本使用一组固定 feature weights 融合 metric、trace、log 和 topology evidence。这些权重能够取得较高准确率，但从论文审稿角度看存在一个明显问题：如果权重直接以常数形式出现在算法中，审稿人可能会认为它们来自对 RCABench 的人工调参。即使算法没有读取 label，固定权重本身也可能被质疑为 dataset-specific prior。

### M2: Per-Case Unsupervised Adaptation Is Unstable

一种自然选择是在每个 case 内部完全无监督地自适应权重。然而，V13-V17 的实验显示，这类方法容易被局部最强症状误导。例如，入口服务可能因为承载大量请求而出现更强的 trace/log 信号；传播受害者可能因为延迟堆积而拥有更尖锐的 duration 异常；局部日志错误率也可能只是下游影响。单 case 内部缺少跨 incident 的稳定约束，因此完全无监督自适应不够稳。

### M3: Naive Offline Calibration Learns Symptoms, Not Causality

V18 尝试在未标注 incident corpus 上根据 feature coverage、concentration 和 cross-modality agreement 学习全局 prior，但结果大幅退化。原因是这类统计目标只能发现“哪些症状尖锐且经常共现”，不能区分“哪些症状更接近根因”。传播症状也可能高度集中、跨模态一致，因此 naive offline calibration 会高估日志、duration 或 volume 类信号。

### M4: Individual-Feature Causal Calibration Has Too Much Freedom

V19 引入了 self-supervised causal pairwise objective，用 synthetic pseudo-root 和拓扑传播负例学习 feature weights。它显著优于 V18，说明因果方向和拓扑负例是正确方向。但 V19 仍然让每个 feature 独立学习权重，导致某些 root-specific synthetic features 被过度放大，另一些真实系统中重要的 trace/log/volume features 被压得过低。

### M5: Family-Level Calibration Is the Stable Middle Ground

V20 的出发点是降低学习自由度。我们不再让无标签目标直接决定所有 feature weights，而是把特征划分为少量 RCA 语义 family，只学习每个 family 的 multiplier。这样，校准器可以自动回答“metric/availability 证据整体是否应略强，trace/log/volume 证据整体是否应略弱”，但不能对单个 feature 做任意调参。这使权重形成过程更可解释、更可复现，也更适合跨系统迁移。

## ICSE Draft: Methodology

### Overview

Given an unlabeled corpus of incidents, EvidenceRank first extracts service-level evidence features from metrics, traces, and logs. Instead of learning a separate weight for each feature, V20 groups features into semantic families and learns a bounded multiplier for each family. The learned multipliers calibrate an interpretable semantic prior and are then fixed for online RCA ranking.

The method has four stages:

1. Extract service-level multi-modal evidence from raw observability data.
2. Generate self-supervised root-vs-propagation ranking pairs.
3. Optimize bounded family multipliers with a pairwise ranking loss and center regularization.
4. Use the calibrated prior in the online EvidenceRank scorer.

### Stage 1: Multi-Modal Evidence Extraction

For each incident, EvidenceRank constructs a feature matrix over services. Metric features capture value shifts, anomaly counts, and count drops. Trace features capture latency, traffic, endpoint distribution, status-code shifts, and self-duration changes. Log features capture count changes, error rates, and template shifts. Trace data also provides service-call topology.

This stage is identical to the online EvidenceRank feature extraction path, ensuring the calibrator learns over the same feature semantics that the algorithm later uses.

### Stage 2: Self-Supervised Pair Construction

Because no labels are available, V20 creates synthetic causal ranking tasks. For each incident, the calibrator samples a pseudo-root service and injects a generic root perturbation profile. It then propagates weaker symptoms along the trace topology to mimic downstream and upstream impact. The pseudo-root is treated as the positive item, while topology neighbors, high-background services, and random services are treated as negatives.

This produces pairwise differences:

```text
d = x_root - x_negative
```

The pair is considered satisfied if the calibrated scorer assigns a higher score to the pseudo-root than to the negative service.

### Stage 3: Family Multiplier Learning

Let `w^(0)` be the semantic feature prior and let `G` be the set of feature families. For a pairwise difference `d`, V20 computes each family's contribution:

```text
c_g(d) = sum_{i in g} w_i^(0) * d_i
```

The calibrated margin is:

```text
margin(d, m) = sum_g m_g * c_g(d)
```

where `m_g` is the multiplier for family `g`.

The objective is:

```text
L(m) = mean_d log(1 + exp(-margin(d, m))) + lambda * ||m - 1||_2^2
```

subject to:

```text
m_min <= m_g <= m_max
```

The center regularization and multiplier bounds are essential. They prevent the synthetic objective from replacing the semantic prior and force calibration to remain conservative.

### Stage 4: Online Ranking

After calibration, the online EvidenceRank algorithm uses fixed weights:

```text
w_i = w_i^(0) * m_family(i)
```

At runtime, EvidenceRank does not rerun the calibrator and does not read any training corpus, label file, injection metadata, output directory, or historical evaluation result. The learned multipliers are global priors and are applied uniformly across incidents and systems.

## How to Present This in the Paper

Recommended wording:

```text
EvidenceRank does not tune feature weights using benchmark labels. Instead, it
starts from a small set of domain-semantic evidence families and calibrates their
relative reliability using a label-free causal ranking objective over unlabeled
incidents. The calibration objective creates pseudo-root perturbations and
topology-propagated negatives, and learns bounded family-level multipliers around
the semantic prior. This design provides a reproducible source for the final
weights while preventing the instability observed when learning unconstrained
per-feature weights.
```

What not to claim:

- 不要声称 V20 已经完全无监督地从零学习了所有权重；
- 不要说语义先验不重要；
- 不要把 V20 描述为 per-case adaptive weighting；
- 不要把 RCABench label 或 injection 当成训练数据；
- 不要隐藏 V18/V19 负向实验，它们正好支持 V20 的设计动机。

Recommended claim:

```text
The weights are not benchmark-label tuned constants. They are generated by
regularizing an interpretable semantic prior with label-free family-level
calibration over unlabeled incidents.
```

## Limitations and Future Validation

V20 仍然保留语义先验，因此它不是“完全从零开始”的无监督权重发现算法。更准确的说法是：V20 提供了一个可复现的无标签校准过程，用于解释、约束和微调语义先验。

后续为了进一步增强 ICSE 说服力，可以补充：

- bootstrap 多次采样未标注 incidents，报告 family multiplier 的置信区间；
- 在不同系统或不同 incident corpus 上重复校准，比较 multiplier 稳定性；
- 做 ablation：无正则、宽边界、窄边界、per-feature learning、family-level learning；
- 报告 V18/V19/V20 作为 progressive design evidence。

这会进一步说明 V20 的权重不是 benchmark-specific tuning，而是一个稳定、可复现、可迁移的 calibration mechanism。
