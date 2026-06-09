# RCABench / RCAEval / AIOps25 多模态 RCA 效果分析

本文分析同一类多模态 RCA 算法在三个数据集上的表现差异，重点解释：

- 为什么在 RCAEval 上，CERA 和 EvidenceRank 往往表现为“多模态不如 metric-only”；
- 为什么 CREST 在 RCAEval 上可以做到多模态超过 metric-only 或至少持平；
- 为什么同样的 CREST 在 RCABench 上多模态很强，但在 AIOps25 上 full multimodal 反而不如 metric+log。

数据来源：

- RCABench: `results.md`
- AIOps25: `results_aiops2025.md`
- RCAEval: `/home/ljw/paper/DDS-DL-AIOPS/RCAEval/output/添加了 torai 论文中实验结果.md`
- 既有分析: `docs/evidrank_dataset_characteristics_rcabench_vs_rcaeval.md`

## 总结结论

三个数据集不是简单的“谁更真实、谁不真实”的关系，而是强调了不同的 observability regime。

| 数据集 | 主导证据形态 | 多模态是否天然有利 | 典型现象 |
| --- | --- | --- | --- |
| RCABench | trace / log / topology 对 request、response、network、protocol 故障高度有用 | 是 | CERA、CREST、EvidenceRank full multimodal 都远超 metric-only |
| RCAEval RE2 | metric 与 label 几乎同构，尤其 CPU/MEM/DISK/SOCKET/DELAY/LOSS 都有直接或近似 metric proxy | 通常否 | CERA、EvidenceRank full multimodal 多数低于 metric-only；CREST 能持平或小幅超过 |
| AIOps25 service-level | metric+log 更接近 resource/JVM/pod/code root；trace 常是入口或传播症状 | full multimodal 不稳定 | metric+log 明显强于 full CREST/CERA；trace 会拖低 top-1 |

核心解释是：多模态 RCA 不应该问“是否使用所有模态”，而应该问“本 incident 中每个模态是否有资格解释 root cause”。RCABench 中 trace/topology 多数有 root-aligned 价值；RCAEval 中 metric 已经接近答案空间；AIOps25 中 trace 经常是 symptom surface，而 metric/log 才更接近 root ownership。

CREST 在 RCAEval 上比 CERA/EvidenceRank 更稳，是因为它不是简单把所有模态证据相加，而是使用 `A * F + S`：

- `A`: 服务本地 abnormality；
- `F`: counterfactual / structural explanatory power；
- `S`: denoised structural support。

这个结构让弱 log/trace evidence 不容易直接推翻强 metric root；当 trace 确实有结构解释力时，又能通过 `F/S` 提供补充。因此 CREST 在 RCAEval 上可以保住 metric-only 的上界，并在 OB/TT 上小幅超过 metric-only。

## 1. RCABench：多模态真正互补

RCABench 的故障空间很宽，包含 resource/app 故障，也包含 request-delay、response-delay、abort、replace-method、replace-path、replace-code、partition、loss 等大量 request/response/network/protocol 类故障。后者并不一定产生唯一的 service-local metric anomaly，反而常出现在 span duration、span count、status/path、调用边、日志模板或日志错误率中。

### 1.1 CERA 与 CREST 在 RCABench 上的结果

| algorithm | total | AC@1 | MRR | AC@3 | AC@5 | 相对 metric-only AC@1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CERA(metric) | 1422 | 0.400844 | 0.531751 | 0.599156 | 0.685654 | baseline |
| CERA(metric+log) | 1422 | 0.452180 | 0.596157 | 0.668073 | 0.778481 | +0.051336 |
| CERA(metric+trace) | 1422 | 0.701125 | 0.820948 | 0.938115 | 0.970464 | +0.300281 |
| CERA(all) | 1422 | 0.850211 | 0.904032 | 0.950774 | 0.976090 | +0.449367 |
| CREST(metric) | 1422 | 0.381857 | 0.517921 | 0.584388 | 0.673699 | baseline |
| CREST(metric+log) | 1422 | 0.440928 | 0.601020 | 0.702532 | 0.811533 | +0.059071 |
| CREST(metric+trace) | 1422 | 0.703235 | 0.818233 | 0.932489 | 0.969761 | +0.321378 |
| CREST(all) | 1422 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | +0.418424 |

这个结果说明，在 RCABench 上 metric-only 不是一个高上界。trace 是非常关键的增量模态：CERA(metric+trace) 比 CERA(metric) AC@1 高约 `+0.30`，CREST(metric+trace) 比 CREST(metric) 高约 `+0.32`。full multimodal 继续从 log/trace/topology 的组合中获益。

### 1.2 RCABench 对算法融合的含义

在 RCABench 上，CERA 和 CREST 都能显著受益于多模态，原因不是“多模态一定更好”，而是该数据集的 fault taxonomy 与 trace/log 观测语义高度匹配。对于很多 request/response 类故障，metric 只能看到弱副作用；trace/log 才是 root-local mutation 或传播路径的直接证据。

因此 RCABench 更适合评价：

- trace status/path/duration/count mutation；
- 调用图传播和上游/下游解释；
- log template / error-rate shift；
- 多模态共同定位 root，而不是只靠 resource metric。

## 2. RCAEval RE2：metric 与答案空间高度对齐

RCAEval RE2 的核心特点是 service-level metric 与 label 接近同构。CPU/MEM/DISK/SOCKET 直接对应 `{service}_cpu`、`{service}_mem`、`{service}_diskio`、`{service}_socket` 等 metric；DELAY/LOSS 也常有 latency percentile 或 error/latency proxy。因此 metric-only 已经接近 ceiling。

在这种数据分布下，log/trace 不是没有信息，而是经常表现为高流量服务、入口服务、公共链路或 downstream symptom。对于简单加性或半加性的多模态融合，额外模态更容易把原本正确的 metric root 拉偏。

### 2.1 RCAEval 上 CERA / EvidenceRank / CREST 的平均表现

下面只取 service-level report 的平均列。

| dataset | algorithm | all T1/T3/A5 | metric T1/T3/A5 | metric+log T1/T3/A5 | trace T1/T3/A5 | all vs metric T1 |
| --- | --- | --- | --- | --- | --- | ---: |
| re2-ob | CERA | 0.71 / 0.98 / 0.93 | 0.80 / 0.97 / 0.93 | 0.59 / 0.78 / 0.78 | 0.33 / 0.72 / 0.70 | -0.09 |
| re2-ob | EvidenceRank | 0.71 / 0.97 / 0.92 | 0.80 / 0.97 / 0.93 | 0.54 / 0.86 / 0.80 | 0.21 / 0.54 / 0.54 | -0.09 |
| re2-ob | CREST | 0.81 / 1.00 / 0.95 | 0.80 / 0.97 / 0.93 | 0.74 / 0.97 / 0.92 | 0.41 / 0.68 / 0.73 | +0.01 |
| re2-ss | CERA | 0.76 / 0.97 / 0.92 | 0.91 / 0.99 / 0.97 | 0.76 / 0.97 / 0.92 | 0.00 / 0.00 / 0.00 | -0.15 |
| re2-ss | EvidenceRank | 0.81 / 0.97 / 0.94 | 0.91 / 0.99 / 0.97 | 0.81 / 0.97 / 0.94 | 0.00 / 0.00 / 0.00 | -0.10 |
| re2-ss | CREST | 0.91 / 0.99 / 0.97 | 0.91 / 0.99 / 0.97 | 0.91 / 0.99 / 0.97 | 0.00 / 0.00 / 0.00 | 0.00 |
| re2-tt | CERA | 0.80 / 0.89 / 0.89 | 0.79 / 0.91 / 0.89 | 0.71 / 0.82 / 0.80 | 0.54 / 0.98 / 0.90 | +0.01 |
| re2-tt | EvidenceRank | 0.78 / 0.91 / 0.89 | 0.79 / 0.91 / 0.89 | 0.73 / 0.89 / 0.84 | 0.02 / 0.72 / 0.58 | -0.01 |
| re2-tt | CREST | 0.82 / 0.92 / 0.91 | 0.79 / 0.91 / 0.89 | 0.82 / 0.91 / 0.90 | 0.48 / 0.92 / 0.84 | +0.03 |

跨三个 RE2 subset 粗略平均：

| algorithm | all AC@1 avg | metric AC@1 avg | all - metric |
| --- | ---: | ---: | ---: |
| CERA | 0.757 | 0.833 | -0.077 |
| EvidenceRank | 0.767 | 0.833 | -0.067 |
| CREST | 0.847 | 0.833 | +0.014 |

### 2.2 为什么 CERA / EvidenceRank 在 RCAEval 上多模态不如 metric-only

CERA 的基本流程是构造 metric/log/trace/topology feature matrix，给不同 feature 赋予 ordinal evidence tier，然后将 enabled modalities 的 evidence burden 合并，并通过 trace parent context 得到 root score。EvidenceRank 的多模态融合也类似：多种 feature family 一旦启用，就会进入同一个排序空间。

这类方法在 RCABench 上很有效，因为 trace/log 经常是 root evidence。但在 RCAEval 上，metric 已经强到接近答案，log/trace 多数是 symptom 或 traffic surface。于是融合会出现两个问题：

1. **额外模态主要增加噪声而不是补充 root evidence。**  
   re2-ss 中 trace 不可用或近似无效，CERA/EvidenceRank 的 all 基本等价于 metric+log，仍从 metric-only 的 `0.91` 降到 `0.76/0.81`，说明 log 本身就足以拖低 metric root。

2. **trace/log 的高 coverage 服务容易获得正证据。**  
   RCAEval 的 log/trace 经常集中到公共服务或高流量路径。若算法没有 incident-local modality reliability gate，这些服务会被当作 root candidate，而不是 downstream/entry symptom。

因此，RCAEval 上的“多模态不如 metric-only”不是实现 bug 的充分证据，更像数据集特征与融合策略的交互结果：metric isomorphic label space + noisy auxiliary modalities。

### 2.3 为什么 CREST 能在 RCAEval 上持平或超过 metric

CREST 的关键优势是 full score 不是简单加法，而是：

```text
score = A * F + S
```

其中：

- `A` 是服务本地异常强度；
- `F` 是结构解释力，即该服务的异常是否能解释 incident 中的结构上下文；
- `S` 是去噪后的结构支持。

这个结构带来两个效果：

1. **metric root 不容易被弱 log/trace 直接挤掉。**  
   RCAEval 的 metric candidate 通常有非常强的 local abnormality。log/trace 如果只是公共流量面，只有局部 row count 或弱 symptom，没有足够的 explanatory power，就不容易通过 `A * F + S` 超过 metric root。

2. **trace 仍能作为结构补充，而不是全局噪声。**  
   re2-tt 中 CREST(trace) 的 T3/A5 很高，但 T1 不高，说明 trace 可以帮助把 root 放进候选前列，却不总能单独确定 top-1。CREST(all) 能把 trace 的结构支持与 metric local root 合在一起，所以 re2-tt 从 metric `0.79/0.91/0.89` 到 all `0.82/0.92/0.91`。

因此，CREST 在 RCAEval 上的意义不是“所有模态都可靠”，而是它的融合机制比较接近“metric 保底 + trace/log 有资格时再增强”。这也是后续设计 adaptive modality selector 的主要方向。

## 3. AIOps25：metric+log 强，trace 容易成为传播/入口症状

AIOps25 的结果与 RCAEval 有相似点：full multimodal 不如 metric-only 或 metric+log。但原因不完全相同。

RCAEval 是 metric 与 label 高度同构，metric-only 本身接近 ceiling；AIOps25 则是许多 service-level incident 的 root evidence 在 metric/log/resource/provenance 中，而 trace 经常表现为入口链路或传播表面。也就是说，AIOps25 的问题不是“只有 metric 有用”，而是“trace 是否有资格解释 root cause”需要更强判断。

### 3.1 AIOps25 上 CERA 与 CREST 的结果

| algorithm | total | AC@1 | MRR | AC@3 | AC@5 | 相对 metric-only AC@1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CERA(metric) | 230 | 0.456522 | 0.653622 | 0.839130 | 0.952174 | baseline |
| CERA(metric+log) | 230 | 0.517391 | 0.686796 | 0.830435 | 0.939130 | +0.060869 |
| CERA(metric+trace) | 230 | 0.413043 | 0.534171 | 0.565217 | 0.600000 | -0.043479 |
| CERA(all) | 230 | 0.369565 | 0.517597 | 0.565217 | 0.652174 | -0.086957 |
| CREST(metric) | 230 | 0.426087 | 0.621815 | 0.769565 | 0.921739 | baseline |
| CREST(metric+log) | 230 | 0.478261 | 0.668761 | 0.821739 | 0.934783 | +0.052174 |
| CREST(metric+trace) | 230 | 0.369565 | 0.520278 | 0.604348 | 0.660870 | -0.056522 |
| CREST(all) | 230 | 0.334783 | 0.503603 | 0.600000 | 0.669565 | -0.091304 |

这个表非常清楚：

- metric+log 是 AIOps25 上 CERA/CREST 家族中更好的组合；
- trace 一加入 metric，就显著拉低 AC@1、AC@3、AC@5；
- full multimodal 比 metric-only 更差，说明 trace/log/topology 的融合没有正确识别 propagation victim。

### 3.2 AIOps25 与 RCAEval 的差别

AIOps25 和 RCAEval 都会惩罚 naive full multimodal，但机制不同。

| 对比项 | RCAEval RE2 | AIOps25 |
| --- | --- | --- |
| metric 为什么强 | service-level metric 与故障类型/label 几乎同构 | resource/JVM/pod/code 类 incident 的 root evidence 常在 metric/provenance |
| log 的作用 | 经常是 traffic/common-service symptom，可能拖低 metric | 与 metric 互补，metric+log 通常最强 |
| trace 的作用 | 在部分 subset 可提供 top-k 支持，但 top-1 常不稳 | 经常是入口/传播表面，full CREST 被 trace graph 拉偏 |
| 适合的机制 | metric floor + 有资格的 trace/log support | trace root eligibility + metric/log ownership + resource provenance |

因此不能简单说 AIOps25 “不符合生产”。它更像一种常见生产形态：资源、实例、pod、JVM 或代码错误的 root-local 证据在 metric/log，而 trace 主要记录用户请求路径上的受害者和传播面。真实生产里这种形态很常见；同时 RCABench 里的 request/protocol/network fault 也很常见。两个数据集代表的是不同 incident mix。

## 4. CERA 与 CREST 的机制差异

### 4.1 CERA：多模态证据 burden 更直接，适合 root-aligned trace/log

CERA 使用 ordinal evidence tier，把 metric/log/trace/topology feature 变成 evidence energy，再聚合为服务分数并通过 trace parent context 调整。它的优点是简单、可解释，在 RCABench 这种 trace/log 与 root 高度相关的数据集上非常强：

- RCABench CERA(all) AC@1 `0.850211`，高于 CERA(metric) `0.400844`；
- CERA(metric+trace) 已经达到 `0.701125`，说明 trace 是主要增益来源。

但 CERA 的弱点也正是这个正向聚合：当 log/trace 是传播症状时，它们仍会贡献正 evidence burden。RCAEval 和 AIOps25 里，这会把强 metric root 推开：

- RCAEval re2-ob: CERA(all) `0.71` < CERA(metric) `0.80`；
- RCAEval re2-ss: CERA(all) `0.76` < CERA(metric) `0.91`；
- AIOps25: CERA(all) `0.369565` < CERA(metric) `0.456522` < CERA(metric+log) `0.517391`。

### 4.2 CREST：结构解释门控更强，能保护 metric ceiling

CREST 把本地异常、结构解释力、去噪结构支持拆开。直观上，服务不是“有异常就高分”，而是“有本地异常，并且能解释 incident 结构”才高分。

这使 CREST 在 RCAEval 上更像一种自适应融合：

- re2-ob: CREST(all) `0.81`，略高于 CREST(metric) `0.80`；
- re2-ss: CREST(all) `0.91`，与 CREST(metric) `0.91` 持平；
- re2-tt: CREST(all) `0.82`，高于 CREST(metric) `0.79`。

CREST 没有让多模态在 RCAEval 上大幅伤害 metric root，说明 `A * F + S` 在“metric 已强、trace/log 不稳定”的 regime 下有保护作用。

但 AIOps25 暴露了 CREST 的边界：如果 trace surface 本身拥有很强结构位置、异常 row share 或传播支持，`F/S` 仍可能把入口/受害服务推到 top-1。也就是说，CREST 的结构解释比 CERA 更稳，但还不是完整的 incident-local modality reliability estimator。

## 5. 三个数据集的统一解释框架

可以把三个数据集放到一个二维平面上：

1. **root evidence modality**：root 证据主要在 metric、log、trace，还是跨模态；
2. **symptom surface strength**：非 root 服务在 log/trace/topology 中是否有高流量、高覆盖、高传播症状。

| 数据集 | root evidence modality | symptom surface strength | 对算法的要求 |
| --- | --- | --- | --- |
| RCABench | 大量 trace/log/topology root evidence | 有，但 root-aligned trace 也强 | 利用 trace graph 和 endpoint/status/path mutation |
| RCAEval RE2 | metric root evidence 极强 | log/trace 常是公共路径或不可用 | 保护 metric floor，只接受有资格的 trace/log 增益 |
| AIOps25 | metric+log/resource root evidence 强 | trace entry/propagation surface 很强 | trace root eligibility + resource/log ownership + victim control |

这个框架解释了为什么同一个算法会跨数据集表现不同：

- **CERA / EvidenceRank**：当 root evidence 与多模态一致时很强；当 metric 已经足够、其他模态噪声多时会被拖低。
- **CREST**：用结构解释门控降低噪声模态的破坏，因此 RCAEval 上能持平或超过 metric；但当 trace surface 本身结构强时，仍会在 AIOps25 被拉偏。

## 6. 对论文和算法设计的启示

### 6.1 不能用“多模态是否超过 metric-only”单独判断算法好坏

在 RCAEval RE2 上，metric-only 很强不是因为真实生产只需要 metric，而是因为该 benchmark 的 service-level metric proxy 与 label 高度对齐。多模态低于 metric-only，在这里更多说明辅助模态未被可靠性过滤，而不是说明 trace/log 没有 RCA 价值。

在 RCABench 上，metric-only 弱也不是 metric 算法差，而是因为很多故障根本不是 resource-metric-first 的问题。trace/log/topology 是必要证据。

### 6.2 CREST 的价值在于“融合方式”，不是简单多模态堆叠

CREST 在 RCAEval 上的结果特别重要：它说明多模态算法不必在 metric-aligned 数据集上必然输给 metric-only。只要融合机制能判断结构解释力，full multimodal 可以做到：

- metric 强时不破坏 metric root；
- trace/log 有结构资格时提供增益；
- 弱模态作为 support，而不是直接作为 top-1 root evidence。

这比“手动选择 metric-only”更通用，也更接近生产 RCA。

### 6.3 AIOps25 提醒还需要更强的 incident-local modality reliability

AIOps25 上 CREST full multimodal 仍低于 metric+log，说明 `A * F + S` 还不够。下一类机制应当显式判断：

- trace 覆盖服务数与候选空间比例；
- trace 异常是否被单一入口/高流量服务支配；
- trace status/path/duration mutation 是否选择性强；
- metric/log root ownership 是否集中到非 trace-surface 服务；
- trace top 服务是否只有 downstream symptom，而缺少 root-local evidence；
- resource / instance / pod provenance 是否支持某个 service 的 root-local anomaly。

这类机制不是数据集特化，而是通用的 telemetry reliability estimation。

## 7. 最终判断

RCAEval、RCABench、AIOps25 都有研究价值，但它们代表的生产 incident mix 不同：

- RCABench 更强调 request/response/network/protocol 以及 trace/log/topology 的 RCA 价值；
- RCAEval RE2 更强调 metric-aligned service ranking，适合检验算法是否会被弱 log/trace 模态破坏；
- AIOps25 更强调 resource/log/root ownership 与 trace propagation surface 的冲突。

从这三个数据集一起看，最合理的结论不是“忽略哪个数据集”，而是：

**真正通用的多模态 RCA 算法必须做 incident-local 模态可信度选择。CREST 已经比 CERA/EvidenceRank 更接近这个方向，因为它能在 RCAEval 上保住 metric-only 的强信号；但 AIOps25 说明它还需要更强的 trace root eligibility、metric/log ownership 和 resource provenance 机制。**
