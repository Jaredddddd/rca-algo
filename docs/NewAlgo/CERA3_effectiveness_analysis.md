# CERA3 有效性与冗余代码分析报告

- 日期：2026-06-05
- 分析对象：`algorithms/evidencerank/src/evidencerank/cera.py`
- 当前版本：`CERA3`
- 运行边界：运行时算法不读取 label、injection、历史 output、perf report、`conclusion.parquet`，也不硬编码 datapack / service / fault。

## 1. 总结

CERA3 当前是一个有效的独立 RCA 算法。full eval 结果为：

| total | error | AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1422 | 0 | 0.850211 | 0.904032 | 0.950774 | 0.976090 |

它有效的核心不是某个单独特征，而是三层机制的组合：

1. **保留 raw log-normalized incident energy**：不把每个 case 内的强异常全部压成 rank / p95 相对值，因此能保留运维上很重要的“绝对异常量级”和“流量/日志规模突变”。
2. **用 ordinal causal evidence tier 替代手写数值权重**：特征只被赋予语义角色，例如 background、baseline、support、local、high、critical；数值 energy ladder 由 tier 顺序和 tier 数量自动合成，而不是对每个 feature 手工给浮点权重。
3. **用当前 incident 自身推导拓扑和 endpoint 支撑**：endpoint gate 来自 endpoint/status/rise 的 rank agreement；parent-context 强度来自 trace graph 的 sink share，而不是固定 blend constant。

离线消融显示，CERA3 最关键的有效部分是：

- ordinal evidence tier：去掉 tier、改成 uniform energy 后，AC@1 从 `0.850211` 降到 `0.670886` 或 `0.650492`；
- raw log-normalized matrix：改成 p95 scale 或 rank feature 后，AC@1 分别降到 `0.483826` 和 `0.459212`；
- trace/status/endpoint/local/log 关键信号：删除 trace signal family 后 AC@1 降到 `0.460619`，删除 status shift 降到 `0.728551`；
- sink-share parent context：删除后 AC@1 降到 `0.798875`；
- ARC endpoint support gate：删除后 AC@1 小幅降到 `0.845288`，但 AC@3/AC@5 同时下降，说明它不是主力涨点，却能改善候选保留和少量 top-1。

当前文件中没有明显“已定义但完全不被调用”的死函数。此前 CERA2 的 family burden / counterfactual explain-away 旧代码已经删除。剩余冗余主要是**低贡献或当前被 disabled 的 feature 计算路径**，而不是完全孤立的死代码。

最明确的可删除候选是：

- `trace_duration_z`：tier 为 `DISABLED`，当前 score 中 energy 为 0；删除该列的离线结果与 CERA3 完全相同。
- `topology_out_degree`：tier 为 `DISABLED`，当前 score 中 energy 为 0；删除该列的离线结果与 CERA3 完全相同。
- `trace_error_rate`：tier 不是 disabled，但当前 cache 中非零覆盖为 0，逐 feature 删除后指标完全不变；可作为当前 RCABench 运行路径的冗余特征处理，但若要兼容其他 trace schema，可保留为 fallback。

需要谨慎处理的低边际收益项：

- `metric_value_delta`：删除后 AC@1 小幅升至 `0.853024`，但 AC@3/AC@5 略降；它可能是 top-1 噪声源，不是无风险删除项。
- `trace_count_rise_shift`：删除后 AC@1/MRR/AC@3 小幅提升但 AC@5 降低；它作为 endpoint gate 的支撑候选仍有方法意义，不建议未经额外 ablation 直接删除。
- `metric_count_drop_shift`、`log_error_rate`、`log_template_delta`、`abnormal_metric_rows`、`abnormal_trace_rows`：单项边际较弱，但有些承担 support / fallback / candidate preservation 作用，适合后续做“简化版 CERA”ablation，而不是立即删。

## 2. 算法流水线

`cera.py` 当前分成四段。

### 2.0 什么是 raw log-normalized matrix

报告中的 **raw log-normalized matrix** 不是指直接使用 parquet 文件里的原始字段，也不是指完全不做归一化。它指的是：

```text
先从 raw metric / trace / log 中抽取服务级非负异常证据
再对每个 feature value 做 log1p(x) 压缩
但不做 case 内 p95 scaling、rank fusion、softmax 或其他相对排名归一化
```

因此 CERA 的输入矩阵可以理解为：

```text
行 = service
列 = BASE_FEATURE_NAMES 中的 feature
值 = log1p(该服务在该 feature 上的异常证据)
```

举例，假设某个 incident 中 `trace_count_delta` 的原始服务级证据是：

| service | 原始 `trace_count_delta` | `log1p` 后 |
| --- | ---: | ---: |
| service A | 1000 | 6.91 |
| service B | 100 | 4.62 |
| service C | 0 | 0.00 |

`log1p` 的作用是压缩极端大值，避免单个超大计数完全支配排序；但它仍保留了 “service A 的异常量级显著高于 service B” 这个运维语义。

如果改成 rank feature，这个例子可能会被压成：

| service | rank view |
| --- | ---: |
| service A | 1.00 |
| service B | 0.50 |
| service C | 0.00 |

这样会丢掉 `1000` 与 `100` 之间的真实量级差异。CERA3 的消融结果也支持这一点：把 raw log-normalized matrix 改成 p95-scaled 或 rank-features 后，AC@1 分别从 `0.850211` 降到 `0.483826` 和 `0.459212`。

所以这里的 **raw** 更准确地说是：

> raw extracted evidence after `log1p` compression, before per-case rank / p95 / distribution rescaling.

它是 CERA3 有效的基础之一：既降低极端值风险，又保留绝对异常强度、日志量突变、trace 量级变化等运维上有意义的信号。

### 2.1 自包含输入与特征抽取

相关函数：

- `_load_input_frames`
- `_collect_services_from_frames`
- `_metric_features`
- `_trace_features`
- `_log_features`
- `_build_feature_matrix`

输入是正常窗口和异常窗口的 metric / trace / log parquet。输出是：

```text
service x BASE_FEATURE_NAMES feature matrix
trace parent-child edges
```

这段代码的作用是把异构可观测数据转换成服务级非负证据：

- metric：z-score、均值偏移、异常指标数、指标行数、metric row drop；
- trace：duration/count/endpoint/status/self-duration、trace row 数、parent-child edge；
- log：日志行数变化、错误关键词率、template 数变化；
- topology：trace in/out degree。

这些 helper 是自包含运行所必需的，不属于冗余代码。即使有些输出 feature 目前被 disabled，通用解析逻辑仍支撑 CERA 的跨 schema 运行能力。

### 2.2 Ordinal evidence energy

相关结构：

- `CERAEvidenceTier`
- `CERA_FEATURE_TIERS`
- `_synthesize_ordinal_energy_ladder`
- `_ordinal_evidence_energy`

CERA3 不再使用手工 feature weight table，而是把 feature 映射到语义 tier：

| tier | 作用 |
| --- | --- |
| `BACKGROUND` | 普通背景异常，提供弱支持 |
| `BASELINE` | 基础异常信号 |
| `SUPPORT` | 证据量 / topology support |
| `LOCAL` | local mutation 或局部运行时证据 |
| `HIGH` | 更接近根因的协议/流量/可用性突变 |
| `CRITICAL` | 最强根因特异信号，目前主要是 status mutation |
| `DISABLED` | 当前不参与 scoring |

能量梯子由 tier 顺序生成：

```text
BACKGROUND = 0.75
BASELINE   = 1.00
SUPPORT    = 1.25
LOCAL      = 1.50
HIGH       = 6.00
ROOT       = 10.00
CRITICAL   = 16.00
```

这些数值不是对 feature 手工调出来的常数，而是由“低 tier 数量、tier 顺序、dyadic ceiling”自动合成。需要注意的是：**feature 到 tier 的语义分配仍然是专家语义先验**。论文表述上应强调 CERA3 消除了 per-feature numeric weights，但并不是完全无先验的黑盒自学习。

### 2.3 Endpoint support gate

相关函数：

- `_arc_positive_rank_view`
- `_cosine_similarity`
- `_apply_arc_trace_endpoint_support_gate`

endpoint shift 容易同时出现在真实根因和受害者上。CERA3 的做法是：

1. 对 `trace_endpoint_shift`、`trace_status_code_shift`、`trace_count_rise_shift` 分别构造正值 rank view；
2. 用 endpoint view 与 status/rise view 的 cosine similarity 生成支撑候选权重；
3. 用当前 case 的 support rank 放大 endpoint evidence。

这段 gate 的有效性不是来自固定权重，而是来自当前 incident 内的 rank agreement。它的单独涨点不大，但会改善高阶候选保留：

| variant | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| CERA3 current | 0.850211 | 0.904032 | 0.950774 | 0.976090 |
| no endpoint support gate | 0.845288 | 0.899151 | 0.942335 | 0.968354 |

结论：endpoint support gate 是有效的轻量校准，不是最大主因；删除它会让 AC@1 下降 `0.004923`，AC@5 下降 `0.007736`。

### 2.4 Sink-share parent context

相关函数：

- `_trace_sink_context_weight`
- `_apply_parent_context`

CERA3 没有使用固定 topology blend constant，而是用：

```text
context_weight = sink_nodes / service_count
sink_nodes = trace children that are not trace parents
```

直觉是：当 trace graph 中终端 downstream service 很多时，叶子节点更可能是传播受害者；此时把 child 的分数向 parent evidence 对齐，可以减少 downstream victim 抢 top-1。当 graph sink 很少时，CERA 保留 local evidence ranking。

消融结果：

| variant | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| CERA3 current | 0.850211 | 0.904032 | 0.950774 | 0.976090 |
| no parent context | 0.798875 | 0.876335 | 0.944444 | 0.976793 |

结论：parent context 是 CERA3 第二关键的结构组件。它让 AC@1 提升约 `0.051336`，主要解决传播受害者和 terminal downstream service 抢第一的问题。AC@5 略高于 current，说明 parent context 会牺牲极少数候选保留，但换来明显 top-1 排序质量。

## 3. 结构级消融

以下消融使用缓存 feature matrix 和 trace edges；label 只用于离线评分，不进入运行时算法。

| variant | AC@1 | MRR | AC@3 | AC@5 | 相对 CERA3 的 AC@1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| CERA3 current | 0.850211 | 0.904032 | 0.950774 | 0.976090 | 0.000000 |
| no parent context | 0.798875 | 0.876335 | 0.944444 | 0.976793 | -0.051336 |
| no endpoint support gate | 0.845288 | 0.899151 | 0.942335 | 0.968354 | -0.004923 |
| ordinal energy only, no gate, no parent | 0.804501 | 0.876950 | 0.941632 | 0.974684 | -0.045710 |
| uniform non-disabled with gate+parent | 0.670886 | 0.772650 | 0.841069 | 0.912799 | -0.179325 |
| uniform all features with gate+parent | 0.650492 | 0.764281 | 0.845992 | 0.924754 | -0.199719 |
| ordinal p95-scaled with gate+parent | 0.483826 | 0.656504 | 0.796765 | 0.895921 | -0.366385 |
| ordinal rank-features with gate+parent | 0.459212 | 0.640869 | 0.786920 | 0.895218 | -0.390999 |

关键结论：

1. **ordinal tier 是最大贡献之一**：uniform non-disabled 比 current 低 `0.179325`，说明“只保留特征但不区分语义角色”远远不够。
2. **raw log-normalized 值比 rank/p95 更适合当前 RCA**：rank/p95 看似更鲁棒，但它们抹掉了绝对异常量级，导致 top-1 大幅下降。
3. **parent context 是强结构增益**：仅去掉 parent context 降 `0.051336`。
4. **endpoint gate 是小而稳定的增益**：主要改善 AC@3/AC@5 和少量 top-1。

## 4. 特征族消融

| variant | AC@1 | MRR | AC@3 | AC@5 | 相对 CERA3 的 AC@1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| CERA3 current | 0.850211 | 0.904032 | 0.950774 | 0.976090 | 0.000000 |
| drop trace signal family | 0.460619 | 0.589465 | 0.654008 | 0.736287 | -0.389592 |
| drop metric family | 0.665963 | 0.752574 | 0.795359 | 0.855134 | -0.184248 |
| drop log family | 0.701125 | 0.820948 | 0.938115 | 0.970464 | -0.149086 |
| drop endpoint/status/rise triad | 0.625879 | 0.734920 | 0.809423 | 0.883263 | -0.224332 |
| drop topology degree features | 0.842475 | 0.899888 | 0.948664 | 0.978200 | -0.007736 |
| drop abnormal row support | 0.843179 | 0.901538 | 0.952883 | 0.981013 | -0.007032 |

关键结论：

1. **trace signal family 是主干**。删除 trace signal 后 AC@1 下降接近 `0.39`，说明 CERA 的根因定位主要依赖 trace 中的 endpoint/status/count/self-duration/duration 信号。
2. **metric family 仍然必要**。删除后 AC@1 下降 `0.184248`，说明 metric 异常为 infrastructure / resource / availability 类故障提供重要证据。
3. **log family 对 top-1 重要，但对 top-3/top-5 影响小**。删除 log 后 AC@1 降 `0.149086`，AC@5 只降 `0.005626`，说明日志主要用于把候选中的真实根因顶到第一，而不是决定是否进入 top-5。
4. **topology degree 作为 feature 的贡献很弱**。删除 topology in/out degree 只降 AC@1 `0.007736`，甚至 AC@5 上升。注意这不代表 topology 无效；真正有效的是 trace edge 上的 parent context，而不是 degree 作为独立分数列。

## 5. 逐 feature 消融

| 删除 feature | AC@1 | MRR | AC@3 | AC@5 | AC@1 变化 | 解释 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `trace_status_code_shift` | 0.728551 | 0.818768 | 0.884669 | 0.937412 | -0.121660 | 最强单项根因特异信号，不能删 |
| `trace_self_duration_relative_shift` | 0.766526 | 0.851965 | 0.925457 | 0.966948 | -0.083685 | 对 local execution delay / self work 很关键 |
| `log_count_delta` | 0.776371 | 0.863218 | 0.943741 | 0.974684 | -0.073840 | 日志量突变是强 top-1 区分信号 |
| `trace_endpoint_shift` | 0.804501 | 0.867147 | 0.918425 | 0.950070 | -0.045710 | endpoint mutation 关键，且参与 gate |
| `metric_max_z` | 0.825598 | 0.887395 | 0.940928 | 0.969761 | -0.024613 | metric 强异常上限有效 |
| `metric_mean_z` | 0.829817 | 0.890666 | 0.945851 | 0.969761 | -0.020394 | metric 平均偏移有效 |
| `trace_duration_delta` | 0.834740 | 0.893710 | 0.945851 | 0.971167 | -0.015471 | duration delta 有效，不能用 disabled 的 z 版替代 |
| `log_template_delta` | 0.841069 | 0.899308 | 0.950774 | 0.973980 | -0.009142 | 弱有效，更多是日志结构变化 support |
| `topology_in_degree` | 0.842475 | 0.899888 | 0.948664 | 0.978200 | -0.007736 | 弱有效；degree 不是核心 topology 机制 |
| `trace_count_delta` | 0.842475 | 0.901154 | 0.952883 | 0.980309 | -0.007736 | 弱有效，候选保留更明显 |
| `abnormal_trace_rows` | 0.843179 | 0.901552 | 0.952883 | 0.981013 | -0.007032 | 弱 support，有助于 top-1 但 AC@5 可上升 |
| `trace_count_drop_shift` | 0.844585 | 0.901646 | 0.953586 | 0.977496 | -0.005626 | 弱有效 |
| `log_error_rate` | 0.846695 | 0.902194 | 0.951477 | 0.975387 | -0.003516 | 当前弱有效 |
| `metric_count_drop_shift` | 0.847398 | 0.901993 | 0.947961 | 0.976090 | -0.002813 | 边际弱，但可支持 count-drop 类故障 |
| `metric_anomaly_count` | 0.848101 | 0.902416 | 0.946554 | 0.977496 | -0.002110 | 边际弱 |
| `abnormal_metric_rows` | 0.849508 | 0.903686 | 0.950774 | 0.976090 | -0.000703 | 接近中性 |
| `trace_duration_z` | 0.850211 | 0.904032 | 0.950774 | 0.976090 | 0.000000 | 当前 disabled，删除不影响 |
| `trace_error_rate` | 0.850211 | 0.904032 | 0.950774 | 0.976090 | 0.000000 | 当前数据中非零覆盖为 0 |
| `topology_out_degree` | 0.850211 | 0.904032 | 0.950774 | 0.976090 | 0.000000 | 当前 disabled，删除不影响 |
| `trace_count_rise_shift` | 0.850914 | 0.906380 | 0.957103 | 0.974684 | +0.000703 | 直接 scoring 边际可疑，但仍是 endpoint gate 支撑候选 |
| `metric_value_delta` | 0.853024 | 0.905378 | 0.947257 | 0.975387 | +0.002813 | top-1 上可能有噪声；删除会损伤 AC@3/AC@5 |

## 6. Feature 覆盖率与冗余解释

| feature | tier | energy | 非零 service rows | 非零 case 数 |
| --- | --- | ---: | ---: | ---: |
| `trace_duration_z` | `DISABLED` | 0.00 | 39362 | 1422 |
| `topology_out_degree` | `DISABLED` | 0.00 | 39355 | 1422 |
| `trace_error_rate` | `BASELINE` | 1.00 | 0 | 0 |

这三个 feature 的冗余原因不同：

- `trace_duration_z` 和 `topology_out_degree` 有大量非零值，但 tier energy 为 0，因此当前 CERA3 完全不使用它们。它们是**显式 disabled 的 scoring 冗余**。
- `trace_error_rate` tier 不为 0，但当前 schema 下没有产生非零值，因此是**数据覆盖导致的当前冗余**。如果未来 trace 中有 `status_code` / `http.status_code` / `status` 且无法通过 `trace_status_code_shift` 捕获，它仍可能作为 fallback 有用。

## 7. 有效部分

### 7.1 必须保留

- `CERA_FEATURE_TIERS` 和 `_synthesize_ordinal_energy_ladder`：这是 CERA3 区别于手写 feature weight table 的核心。
- `_build_feature_matrix` 中的 `math.log1p` normalization：当前证据表明 raw log-normalized matrix 比 p95/rank 更强。
- `trace_status_code_shift`：最强单项 feature，删除后 AC@1 降 `0.121660`。
- `trace_self_duration_relative_shift`：local execution root 关键证据。
- `log_count_delta`：日志突变对 top-1 很有效。
- `trace_endpoint_shift`：endpoint mutation 与 gate 的基础。
- `_trace_sink_context_weight` + `_apply_parent_context`：CERA3 的关键 topology mechanism。
- trace edge 抽取与 parent-child fallback：parent context 依赖它，不应因为 degree feature 弱就删 trace edge。

### 7.2 有效但边际较小

- `_apply_arc_trace_endpoint_support_gate`：小幅提升，但主要改善候选质量，建议保留。
- `topology_in_degree`：单独边际弱，但对 top-1 有轻微帮助；若做轻量版可考虑删除。
- `abnormal_metric_rows` / `abnormal_trace_rows`：support 边际弱，部分高阶指标改善；适合在简化版中做 ablation。
- `log_error_rate` / `log_template_delta`：单项弱，但 log family 整体强，不能因为单项弱就删除整个 log 模态。

### 7.3 必要基础设施，不应按“冗余”删除

- `_clean_service` / `_series_service`：保证跨 schema 服务名识别。
- `_safe_read_parquet`：允许缺失模态，不让算法因某个 parquet 不存在而失败。
- `_distribution_shift_by_service`：endpoint/status shift 的基础。
- `_trace_self_duration_stats`：self-duration feature 的基础。
- `_stable_template_id`：log template delta 的基础。
- `_finite_nonnegative`：防止 NaN/inf/负值进入 score。

这些 helper 的价值不是直接涨分，而是保证算法在不同观测 schema、缺失模态、小样本和异常值下可运行。

## 8. 无效或冗余部分

### 8.1 可优先删除或移出 active scoring 的项

1. `trace_duration_z`
   - 当前 tier：`DISABLED`
   - 删除单项后指标完全不变。
   - 建议：从 active `BASE_FEATURE_NAMES` / `CERA_FEATURE_TIERS` 中移除，或者保留为未来实验 feature 但明确标注“not used by CERA3 scoring”。

2. `topology_out_degree`
   - 当前 tier：`DISABLED`
   - 删除单项后指标完全不变。
   - 建议：删除 active scoring 列。保留 trace edges 和 parent context，不要误删 topology mechanism。

3. `trace_error_rate`
   - 当前非零覆盖：0 case。
   - 删除单项后指标完全不变。
   - 建议：如果目标是压缩 RCABench 当前 CERA3，可删除；如果目标是跨系统 schema 兼容，保留为 fallback，并在代码注释中说明它当前不是主要信号。

### 8.2 可进一步 ablation 后再决定的项

1. `metric_value_delta`
   - 删除后 AC@1 升 `0.002813`，但 AC@3/AC@5 下降。
   - 解释：绝对 metric delta 可能受量纲影响，偶尔把 top-1 推错；但它仍能保留一些候选。
   - 建议：不要简单删除；更合理的是降 tier、做 family-level cap，或只在 metric z-score 支持下启用。

2. `trace_count_rise_shift`
   - 删除后 AC@1/MRR/AC@3 略升，AC@5 略降。
   - 解释：traffic rise 直接作为 HIGH evidence 可能偏传播/入口流量；但它作为 endpoint gate 的 support view 有意义。
   - 建议：测试“只作为 gate support，不作为直接 HIGH score”的版本。

3. `metric_count_drop_shift`
   - 单项边际很小。
   - 解释：对少数 availability/drop 类 case 有意义，但不是 CERA3 主力。
   - 建议：保留到 infrastructure-local evidence 进一步设计，不急删。

4. `abnormal_*_rows`
   - 删除后 AC@1 略降，但 AC@3/AC@5 可上升。
   - 解释：行数 support 能帮助 top-1，也可能偏向高流量节点。
   - 建议：可作为论文 ablation 中的 support evidence，而不是核心 root evidence。

## 9. 不应删除的内容

不要因为某些 topology feature 边际弱而删除以下内容：

- trace edge extraction；
- `_trace_sink_context_weight`；
- `_apply_parent_context`。

原因是：degree feature 弱，不代表 topology reasoning 弱。消融显示 parent context 带来 `+0.051336` AC@1 增益，是 CERA3 的关键机制之一。

也不要把 raw matrix 替换成 rank fusion / p95 scaling。它们在鲁棒性叙事上看起来诱人，但实证上明显失败：

| 替代方式 | AC@1 | 相对 CERA3 |
| --- | ---: | ---: |
| p95-scaled | 0.483826 | -0.366385 |
| rank-features | 0.459212 | -0.390999 |

这说明 CERA3 的“鲁棒”不是靠把所有 case 内数值压平，而是靠：

- `log1p` 降低极端值；
- ordinal tier 区分根因特异信号和背景症状；
- sink-share topology 抑制传播受害者；
- endpoint/status/rise agreement 校准 endpoint mutation。

## 10. 论文叙事建议

建议把 CERA3 解释为：

> CERA converts heterogeneous observability signals into ordinal causal evidence roles and performs incident-derived evidence alignment over endpoint mutation and trace topology. It avoids hand-crafted per-feature numeric weights by synthesizing role energy from the ordinal evidence taxonomy, while preserving raw log-normalized operational signal magnitudes that are essential for robust top-1 RCA.

中文表达：

> CERA 将指标、调用链和日志证据映射为有序因果证据角色，并基于当前 incident 的 endpoint/status/traffic 一致性与 trace sink-share 拓扑结构进行证据对齐。它不使用手工 per-feature 数值权重，而是由证据角色顺序自动合成能量梯子，同时保留 raw log-normalized 异常强度，以兼顾根因特异性和运维鲁棒性。

需要主动承认的限制：

- CERA3 仍使用 feature-to-tier 的语义先验；它不是完全无先验学习算法。
- 当前最弱的 case 主要是 pod-failure、bandwidth、低 mutation infrastructure 故障和小样本 cancel-service 类 case。
- `trace_duration_z` / `topology_out_degree` 这类 disabled feature 应在 camera-ready 前清理或标注，否则审稿人可能认为代码含有未解释残留。

## 11. 建议的清理路线

如果下一步要真的改 `cera.py`，建议按以下顺序做，且每一步都跑 full eval 或至少 cache scoring：

1. **安全清理 disabled active columns**
   - 从 active scoring 中移除 `trace_duration_z`、`topology_out_degree`。
   - 验证 AC/MRR 与当前完全一致。

2. **处理 `trace_error_rate`**
   - 方案 A：删除，获得更简洁实现。
   - 方案 B：保留为跨 schema fallback，并在报告/代码注释说明当前 RCABench 中非主信号。

3. **测试 support-only `trace_count_rise_shift`**
   - 不让它直接进入 HIGH energy sum；
   - 仍允许它参与 endpoint support gate。

4. **测试 metric value delta 降噪**
   - 删除、降 tier、或在 z-score 支持下启用；
   - 观察 AC@1 提升是否会牺牲 AC@3/AC@5。

5. **做简化版 CERA ablation**
   - 保留 status/self-duration/log-count/endpoint/metric-z/parent context；
   - 去除弱 support feature；
   - 比较是否能在更少特征下保持 `AC@1 >= 0.84`。

## 12. 最终判断

CERA3 的有效性有比较充分的证据支撑：

- 指标上超过目标：`AC@1=0.850211`；
- 相对 CERA2 提升明显：AC@1 从 `0.752461` 到 `0.850211`；
- 结构消融能解释涨点来源；
- 关键 feature 消融能解释哪些观测信号在发挥作用；
- 没有 runtime label leakage 或 case hardcoding；
- 没有 hand-crafted per-feature numeric weights。

当前应保留的核心是：

```text
raw log-normalized features
+ ordinal causal evidence tiers
+ ARC endpoint support gate
+ sink-share parent context
```

当前可作为冗余清理对象的是：

```text
trace_duration_z
topology_out_degree
trace_error_rate
```

其中前两个是明确 disabled feature，删除风险最低；`trace_error_rate` 当前无贡献，但是否删除取决于是否要保留跨 trace schema fallback 能力。
