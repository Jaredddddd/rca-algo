# CERA3 与 EvidenceRank 对比报告

- 日期：2026-06-06
- CERA 实现：`algorithms/evidencerank/src/evidencerank/cera.py`
- EvidenceRank 实现：`algorithms/evidencerank/src/evidencerank/algorithm.py`
- 对比范围：主算法 `CERA` 与主算法 `EvidenceRank`。`algorithm.py` 中的 `EvidenceRankARC` 也会作为相关背景说明，但不是本报告的主对比对象。

## 1. 一句话结论

CERA3 和 EvidenceRank **共享同一类通用观测特征抽取能力**，但它们的根因排序层不同：

```text
EvidenceRank = raw log-normalized feature matrix
             -> ordinal feature weights
             -> legacy fixed endpoint gate
             -> sum
             -> fixed 0.05 parent context

CERA3       = raw log-normalized feature matrix
             -> ordinal causal evidence energy
             -> incident-derived ARC endpoint support gate
             -> sum
             -> trace sink-share parent context
```

所以两者的核心差异不是“用了哪些 parquet”或“抽了哪些基础 feature”，而是：

1. EvidenceRank 仍保留 legacy endpoint gate 的固定数值常数；
2. EvidenceRank 使用固定 `PARENT_CONTEXT_WEIGHT = 0.05`；
3. CERA3 把 endpoint 支撑和 topology context 都改成从当前 incident 结构中推导；
4. CERA3 删除了 `algorithm.py` 中大量 ARC / reliability / pairwise contrast 辅助逻辑，主排序路径更短、更容易解释；
5. CERA3 的 paper-facing 叙事是 causal evidence role alignment，而不是 heuristic weighted sum。

在当前 RCABench 输出上，CERA3 比 EvidenceRank 主线更强：

| algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cera` | 1422 | 0 | 0.850211 | 0.904032 | 0.950774 | 0.976090 |
| `evidencerank` | 1422 | 0 | 0.827707 | 0.891195 | 0.947257 | 0.974684 |
| delta |  |  | +0.022504 | +0.012838 | +0.003516 | +0.001406 |

换成 case count 来看，CERA3 的 top-1 命中为 `1209`，EvidenceRank 为 `1177`，CERA3 多命中 `32` 个 top-1 case。

## 2. 相同点

### 2.1 输入边界相同

两者运行时都只读取：

```text
normal_metrics.parquet
abnormal_metrics.parquet
normal_traces.parquet
abnormal_traces.parquet
normal_logs.parquet
abnormal_logs.parquet
```

两者运行时都不应该读取：

- label；
- injection metadata；
- previous output；
- perf report；
- `conclusion.parquet`；
- datapack / service / fault hardcode。

### 2.2 基础 feature schema 基本相同

两者都有同一组 `BASE_FEATURE_NAMES`：

```text
metric_max_z
metric_mean_z
metric_anomaly_count
metric_value_delta
metric_count_drop_shift
trace_duration_z
trace_duration_delta
trace_count_delta
trace_count_rise_shift
trace_count_drop_shift
trace_endpoint_shift
trace_error_rate
trace_status_code_shift
trace_self_duration_relative_shift
log_count_delta
log_error_rate
log_template_delta
topology_in_degree
topology_out_degree
abnormal_metric_rows
abnormal_trace_rows
```

这些 feature 的抽取逻辑也基本一致：

- metric：z-score、mean z、metric value delta、metric count/drop；
- trace：duration/count/endpoint/status/self-duration；
- log：count delta、error keyword rate、template delta；
- topology：从 trace parent-child edge 得到 in/out degree。

CERA3 现在是自包含文件，不再从 `algorithm.py` import helper；但这代表工程边界独立，不代表 feature extraction 思路完全不同。

### 2.3 都使用 raw log-normalized feature matrix

两者的 `_build_feature_matrix` 都会把服务级非负证据做：

```python
math.log1p(value)
```

因此两者主线输入都不是 per-case rank feature，也不是 p95-scaled feature，而是保留绝对异常量级的 raw log-normalized matrix。

这一点很重要：CERA3 的性能提升不是因为换了 feature normalization，而是因为后续 scoring / topology alignment 变了。

### 2.4 feature-to-tier 语义映射基本相同

EvidenceRank 使用：

```text
FeaturePriority
FEATURE_PRIORITIES
FEATURE_PRIORITY_LADDER
FEATURE_WEIGHTS
```

CERA 使用：

```text
CERAEvidenceTier
CERA_FEATURE_TIERS
CERA_ORDINAL_ENERGY_LADDER
_ordinal_evidence_energy
```

当前两者的 feature 到 tier 映射基本一致，能量梯子也同构：

| role / priority | energy |
| --- | ---: |
| `DISABLED` | 0.00 |
| `BACKGROUND` | 0.75 |
| `BASELINE` | 1.00 |
| `SUPPORT` | 1.25 |
| `LOCAL` | 1.50 |
| `HIGH` | 6.00 |
| `ROOT` | 10.00 |
| `CRITICAL` | 16.00 |

因此不能把 CERA3 描述为“完全换了一套 feature prior”。更准确的说法是：

> EvidenceRank 暴露了有效的 RCA feature-priority 能力图；CERA3 将其重构为 causal evidence roles，并把原来固定常数控制的 endpoint / topology alignment 改成 incident-derived inference。

## 3. 核心差异

### 3.1 命名和方法定位不同

EvidenceRank 的主类是：

```text
class EvidenceRank(Algorithm)
```

其语义更接近：

```text
weighted evidence sum + heuristic gates
```

CERA 的主类是：

```text
class CERA(Algorithm)
```

其语义是：

```text
causal evidence role alignment
```

CERA3 想表达的是：不同观测 feature 不只是数值权重不同，而是扮演不同的因果证据角色。比如：

- status mutation 更接近 root-specific mutation；
- self-duration 更接近 local execution evidence；
- abnormal row count 更像 support；
- topology edge 用于解释传播关系，而不是简单 centrality feature。

### 3.2 Endpoint gate 不同

EvidenceRank 主线使用 legacy endpoint gate：

```text
TRACE_ENDPOINT_SUPPORT_STATUS_FACTOR = 2.0
TRACE_ENDPOINT_SUPPORT_RISE_FACTOR   = 1.5
TRACE_ENDPOINT_UNSUPPORTED_PENALTY   = 0.5
TRACE_ENDPOINT_POST_GATE_FACTOR      = 1.75
```

逻辑大致是：

```text
status/rise 对 endpoint 提供固定倍数支撑
unsupported endpoint 被固定比例惩罚
最后 endpoint 再乘固定 post-gate factor
```

这套逻辑有效，但很像 hand-crafted heuristic constants。

CERA3 使用 ARC-style endpoint support gate：

```text
endpoint_view = positive rank view(endpoint)
status_view   = positive rank view(status)
rise_view     = positive rank view(rise)
candidate weight = cosine(endpoint_view, candidate_view)
endpoint_factor = endpoint_view + support_view
```

区别是：

| 维度 | EvidenceRank legacy gate | CERA3 ARC gate |
| --- | --- | --- |
| 支撑来源 | status/rise 固定倍数 | 当前 incident 的 rank agreement |
| 数值常数 | 有 `2.0/1.5/0.5/1.75` | 无固定支撑倍数 |
| endpoint 放大 | 固定 post-gate factor | endpoint rank + support rank |
| 论文叙事 | heuristic gate | incident-derived evidence alignment |

CERA3 的 endpoint gate 不是最大涨点，但比 EvidenceRank 的 legacy gate 更符合“无手工数值权重”的目标。

### 3.3 Topology parent context 不同

EvidenceRank 主线使用固定 parent context：

```text
PARENT_CONTEXT_WEIGHT = 0.05
```

即只要 trace modality 启用，就按固定比例把 child score 与 parent score 均值混合。

CERA3 使用 sink-share parent context：

```text
context_weight = sink_nodes / service_count
sink_nodes = trace children that are not trace parents
```

这意味着：

- 如果当前 trace graph 中 terminal downstream service 很多，CERA3 会更强地用 parent evidence 校准 child；
- 如果当前 graph 没有明显 sink 结构，context weight 接近 0，CERA3 更保留 local evidence；
- topology strength 来自当前 incident，而不是固定常数。

对比：

| 维度 | EvidenceRank | CERA3 |
| --- | --- | --- |
| parent context 强度 | 固定 `0.05` | `sink_nodes / service_count` |
| 是否 case-adaptive | 否 | 是 |
| 机制含义 | 轻微 parent smoothing | sink-heavy graph 中抑制 downstream victim |
| 手工 blend constant | 有 | 无固定 blend constant |

CERA3 的消融显示，去掉 sink-share parent context 后 AC@1 从 `0.850211` 降到 `0.798875`。这说明动态 topology context 是 CERA3 相对 EvidenceRank 的核心差异之一。

### 3.4 主 scoring 公式不同

EvidenceRank 主线：

```text
matrix
* FEATURE_WEIGHTS
-> legacy endpoint gate
-> row sum
-> fixed parent context
-> rank
```

CERA3：

```text
matrix
* ordinal evidence energy
-> ARC endpoint support gate
-> evidence burden sum
-> sink-share parent context
-> rank
```

两者看起来都包含“乘 feature energy + sum”，但 CERA3 的关键变化在后两步：

- endpoint gate 从固定常数变成 rank agreement；
- parent context 从固定 `0.05` 变成 trace graph sink share。

### 3.5 CERA3 不包含 EvidenceRankARC 的复杂 reliability / pairwise contrast

`algorithm.py` 里还有 `EvidenceRankARC`，它会额外执行：

- `_robust_case_feature_matrix`
- `_arc_unsupervised_feature_weights`
- `_arc_active_feature_weights`
- `_apply_arc_top_neighbor_pairwise_contrast`

这条 ARC 线不是 EvidenceRank 主线，但它在同一个文件里。

CERA3 没有继承这整套 ARC reliability / pairwise contrast。CERA3 只复用了 ARC-style endpoint support gate 的思想，并把 topology 处理改成 sink-share parent context。

因此 CERA3 比 EvidenceRankARC 更简单：

| 维度 | EvidenceRankARC | CERA3 |
| --- | --- | --- |
| case p95 scaling | 用于 reliability / contrast | 不用于主 scoring |
| feature reliability | 有 | 无 |
| family contrast | 有 | 无 |
| top-neighbor pairwise transfer | 有 | 无 |
| endpoint support | ARC-style | ARC-style |
| topology context | fixed parent weight + pairwise contrast | sink-share parent context |

从结果看，CERA3 也高于 EvidenceRankARC：

| algorithm | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| `cera` | 0.850211 | 0.904032 | 0.950774 | 0.976090 |
| `evidencerank_arc` | 0.831224 | 0.893267 | 0.947961 | 0.975387 |

## 4. 行为差异

基于当前输出 parquet，对 `cera` 和 `evidencerank` 的 1422 个 case 做离线 rank 对比：

| category | cases |
| --- | ---: |
| both hit@1 | 1143 |
| CERA-only hit@1 | 66 |
| EvidenceRank-only hit@1 | 34 |
| both miss@1 | 179 |

rank 层面的比较：

| category | cases |
| --- | ---: |
| CERA rank better | 109 |
| EvidenceRank rank better | 77 |
| same rank | 1236 |

解释：

- 两者大多数 case 排名相同或非常接近，因为共享 feature extraction 和 feature-tier prior；
- CERA3 的差异集中在少量 topology / endpoint / propagation ambiguous case；
- CERA3 比 EvidenceRank 多 `66 - 34 = 32` 个 top-1 净改善，正好对应 AC@1 count 的差异；
- rank delta 均值为 `+0.037975`，正号表示 CERA 更好；中位数为 0，说明大多数 case 不变，提升来自局部关键 case 的 rerank。

这符合代码差异：CERA3 没有重写整个观测模型，而是把 EvidenceRank 已经有效的能力图重新组织成更稳的 endpoint/topology alignment。

## 5. 多模态 ablation 类的区别

EvidenceRank 在 `algorithm.py` 中注册：

```text
evidencerank_metric
evidencerank_log
evidencerank_trace
evidencerank_metric_log
evidencerank_metric_trace
evidencerank_log_trace
```

CERA 在 `cera.py` 中也注册了对应的 thin subclasses：

```text
cera_metric
cera_log
cera_trace
cera_metric_log
cera_metric_trace
cera_log_trace
```

两者的 variant 思路相同：只覆盖 `_modalities`，复用主算法 pipeline。

差异是：

- EvidenceRank variants 复用 `EvidenceRank` 的 legacy endpoint gate 和固定 parent context；
- CERA variants 复用 CERA3 的 ordinal role scoring、ARC endpoint gate 和 sink-share parent context；
- 非 trace variant 中，trace edge 为空，因此 parent context 和 endpoint gate 自然不生效。

## 6. 工程边界差异

### 6.1 EvidenceRank 是默认强基线

`algorithm.py` 是默认 `evidencerank` 的主实现，里面还包含：

- EvidenceRank 主线；
- EvidenceRankARC；
- metric/log/trace 多模态 variants；
- ARC reliability helper；
- legacy endpoint gate helper；
- parent context helper。

它是一个“研究累积型文件”，保留了多条算法线的支撑代码。

### 6.2 CERA 是独立新算法文件

`cera.py` 当前是 self-contained：

- 不 import `evidencerank.algorithm` 的 runtime helper；
- 保留 CERA3 所需 feature extraction；
- 保留 CERA3 所需 endpoint gate；
- 保留 CERA3 所需 sink-share parent context；
- 不包含 EvidenceRankARC 的 reliability / family consensus / pairwise contrast 逻辑。

这让 CERA 更适合作为 paper-facing algorithm artifact：主路径短，机制清楚，依赖边界明确。

## 7. 方法学意义上的区别

### 7.1 EvidenceRank 更像能力探针

EvidenceRank 的价值在于证明了哪些信号组合对 RCABench RCA 有用：

- status mutation；
- endpoint shift；
- count rise/drop；
- self-duration；
- log count；
- metric z-score；
- parent-child topology。

但 EvidenceRank 主线仍有两个论文叙事弱点：

1. legacy endpoint gate 有固定常数；
2. parent context 是固定 `0.05` smoothing。

这些让它更像高性能 heuristic ranker。

### 7.2 CERA 更像可发表算法

CERA3 继承 EvidenceRank 发现的能力图，但将其组织为：

- ordinal causal evidence roles；
- incident-derived endpoint support；
- incident-derived topology context；
- no fixed endpoint support multipliers；
- no fixed parent-context blend constant。

因此 CERA3 的论文叙事可以从“调 feature 权重”转向：

```text
heterogeneous observability evidence
-> causal evidence roles
-> incident-level role alignment
-> topology-aware root energy
```

## 8. 不能夸大的地方

为了避免论文表述被审稿人抓住，建议明确承认：

1. CERA3 不是从零发明 feature extraction。
   - 它复用了 EvidenceRank 已验证的通用 metric / trace / log 抽取能力。

2. CERA3 不是完全无先验学习。
   - feature-to-tier 的语义映射仍是专家语义 prior。
   - 它消除的是 per-feature numeric weight table 和固定 endpoint/topology blend constants。

3. CERA3 不是 Counterfactual RCA。
   - 当前 `cera.py` 没有显式 counterfactual explain-away。
   - topology 机制应称为 sink-share parent context 或 topology-aware evidence alignment。

4. CERA3 与 EvidenceRank 的最大差异是 inference layer。
   - 不要把它写成“完全不同的数据处理 pipeline”。

## 9. 推荐论文表述

可以这样写 EvidenceRank 与 CERA 的关系：

> EvidenceRank serves as a diagnostic capability probe that identifies robust observability signals for microservice RCA. CERA keeps these generic signal transformations but replaces heuristic fixed-gate scoring with causal evidence-role alignment. It synthesizes role energy from ordinal evidence tiers, derives endpoint support from incident-level rank agreement, and calibrates parent-child topology influence using the trace graph's sink share.

中文版本：

> EvidenceRank 是一个强能力探针，用于发现哪些多模态观测信号对微服务 RCA 有效。CERA 保留这些通用信号转换，但把固定常数控制的 heuristic scoring 改造成因果证据角色对齐：它由有序证据角色合成能量，用当前 incident 内 endpoint/status/traffic 的排序一致性推导 endpoint support，并用 trace graph sink share 自适应决定 parent-child topology 的影响强度。

## 10. 最终判断

CERA3 和 EvidenceRank 的关系可以概括为：

```text
共享：输入边界、feature schema、raw log-normalized matrix、feature-to-tier 语义能力图
不同：endpoint support gate、topology context strength、主 scoring 叙事、代码边界和复杂度
结果：CERA3 在当前 full eval 中 AC@1/MRR/AC@3/AC@5 均高于 EvidenceRank 主线
```

如果目标是工程稳定性，EvidenceRank 仍是一个强基线；如果目标是 ICSE 论文叙事，CERA3 更适合作为主算法，因为它把有效经验从“heuristic weighted ranker”提升成了“incident-derived causal evidence-role alignment”。
