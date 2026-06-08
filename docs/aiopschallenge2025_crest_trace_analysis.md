# AIOpsChallenge2025 CREST Trace Degradation Analysis

## 结论

AIOpsChallenge2025 转成 service-level RCABench 格式后，CREST 全模态明显弱于
`crest_metric_log`，主要不是 CREST 的多模态思想失效，而是 **aiops2025 的 trace 在当前转换后更像入口/关键路径流量表面，而不是稳定的根因证据**。

> 2026-06-08 更新：本文分析的是修复前的转换产物和当时的 aiops2025 结果。转换脚本
> `scripts/build_aiopschallenge2025_rcabench.py` 已经修复 trace status/error 保留、raw trace
> 字段保留、metric/log 元数据保留、`redis -> redis-cart` 标准化，以及不可观测 service-level
> case 过滤。重新生成数据集后，应以新的 `conversion_report.json` 和评估结果为准。

最关键的原因有三个：

1. 修复前的转换脚本把所有 trace status 写成 `Ok`，但原始 trace tags 中实际存在 `error=true`、`http.status_code=500/404` 和非 0 `status.code`。这会导致 CREST/CERA 中最强的 trace root 信号 `trace_status_code_shift` 基本失效。
2. aiops2025 的 raw Jaeger trace 服务空间本身明显小于 metric/log/label 空间。281 个 case 中，abnormal trace 只覆盖 GT 服务 141 个；metric 覆盖 230 个，log 覆盖 215 个。
3. CREST 全模态会用 trace 构造结构解释力 `F` 和去噪支持 `S`。当 trace 缺少 status/root mutation、且只覆盖少数高流量服务时，`F/S` 会把排序吸向 `frontend`、`checkoutservice` 这类入口或关键路径服务，压低 metric/log 本来能命中的根因。

所以 aiops2025 上出现：

```text
crest_metric_log: AC@1=0.391459, AC@3=0.672598, AC@5=0.765125
crest:            AC@1=0.323843, AC@3=0.501779, AC@5=0.555160
crest_trace:      AC@1=0.274021, AC@3=0.409253, AC@5=0.466192
```

而 RCABench 中 trace/status/path/拓扑异常更常和注入根因对齐，`crest` 全模态因此是 CREST 家族最强：

```text
crest:             AC@1=0.800281, AC@3=0.944444, AC@5=0.971871
crest_metric_trace: AC@1=0.703235, AC@3=0.932489, AC@5=0.969761
crest_trace:       AC@1=0.560478, AC@3=0.836850, AC@5=0.904360
crest_metric_log:  AC@1=0.440928, AC@3=0.702532, AC@5=0.811533
```

## 数据口径

参考结果：

- `results_aiops2025.md`
- `results.md`
- 转换说明：`docs/aiopschallenge2025_rcabench_service.md`
- CREST 实现：`algorithms/evidencerank/src/evidencerank/crest.py`
- trace/log/metric feature 构造：`algorithms/evidencerank/src/evidencerank/cera.py`
- 转换脚本：`scripts/build_aiopschallenge2025_rcabench.py`

补充分析读取的是修复前 aiops2025 输出目录：

```text
output/rcabench-platform-v2/data/aiopschallenge2025_rcabench_service
data/rcabench-platform-v2/data/aiopschallenge2025_rcabench_service
```

## 结果差异

aiops2025 上，加入 trace 对 CREST 的净效果是负的。

`crest_metric_log -> crest`：

| K | metric_log 命中 | crest 命中 | crest 修复 | crest 破坏 | 净变化 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Top1 | 110 | 91 | 31 | 50 | -19 |
| Top3 | 189 | 141 | 25 | 73 | -48 |
| Top5 | 215 | 156 | 10 | 69 | -59 |

`crest_metric -> crest_metric_trace`：

| K | metric 命中 | metric_trace 命中 | trace 修复 | trace 破坏 | 净变化 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Top1 | 98 | 100 | 46 | 44 | +2 |
| Top3 | 177 | 140 | 25 | 62 | -37 |
| Top5 | 212 | 152 | 9 | 69 | -60 |

这个表说明 trace 不是完全没有用：它能把一些 network/dns case 拉到 Top1。但它也会显著压缩 Top3/Top5 的候选多样性，导致很多 metric/log 原本靠前的根因掉出前列。

按 fault type 看，`crest_metric_log -> crest` 的 Top1 净变化如下：

| fault type | cases | metric_log Top1 | crest Top1 | 净变化 |
| --- | ---: | ---: | ---: | ---: |
| network-delay | 23 | 6 | 17 | +11 |
| dns-error | 20 | 3 | 12 | +9 |
| network-corrupt | 25 | 13 | 18 | +5 |
| network-loss | 20 | 14 | 14 | 0 |
| code-error | 19 | 11 | 10 | -1 |
| jvm-latency | 13 | 2 | 0 | -2 |
| target-port-misconfig | 15 | 4 | 1 | -3 |
| jvm-gc | 12 | 3 | 0 | -3 |
| pod-kill | 14 | 7 | 3 | -4 |
| pod-failure | 39 | 7 | 3 | -4 |
| jvm-exception | 10 | 5 | 0 | -5 |
| memory-stress | 16 | 12 | 6 | -6 |
| jvm-cpu | 11 | 8 | 1 | -7 |
| cpu-stress | 18 | 15 | 6 | -9 |

trace 的收益集中在 network/dns；损失集中在 resource/JVM/pod。全模态平均下降，是因为 CREST 没有按 trace 置信度控制结构信号。

## Trace 转换问题

修复前转换脚本里已经定义了 status 解析函数：

```text
scripts/build_aiopschallenge2025_rcabench.py:261 normalize_status(tags)
```

但当时 `transform_trace()` 实际写出时使用了常量：

```text
scripts/build_aiopschallenge2025_rcabench.py:354 pl.lit("Ok").alias("attr.status_code")
```

原始 trace parquet 的 `tags` 中包含 `status.code`、`status.message`、`http.status_code`、`error` 等字段，而且不是全 Ok。对 390 个原始 trace parquet 做聚合，能看到：

```text
status.code:
  0      110,218,955
  13         115,127
  2           93,895
  14          65,708
  4           16,544
  5           14,710

http.status_code:
  200      4,774,129
  302        923,788
  500        100,545
  404         14,710

error:
  true       327,076
```

所以 `Ok` 不是原始数据天然如此，而是当前转换逻辑造成的。转换后的 281 个 abnormal trace 中，`attr.status_code` 的唯一值都是 `Ok`：

```text
abnormal trace status counts: Ok = 19,446,312
trace_status_unique: 281/281 case 都只有 1 个 status 值
```

这会直接影响 CREST/CERA 的 trace 特征：

- `trace_status_code_shift` 在 `cera.py` 中由 `span_name + status` 分布变化计算；
- `trace_error_rate` 只检查 `status_code`、`http.status_code`、`status`，当前转换只写 `attr.status_code`；
- 所以当前 aiops2025 trace 主要剩下 duration/count/endpoint/topology/row-volume 这类传播和流量信号。

对 281 个 converted abnormal trace parquet 的列做检查，status-like 列只有 `attr.status_code`，且每个 case 都只有 `{Ok}`：

```text
status-like column case counts: {'attr.status_code': 281}
attr.status_code all exactly {Ok}: True
attr.status_code unique-count distribution: {1: 281}
```

因此这里不是 trace status 特征“权重不够”，而是两个 root-oriented status/error 特征在当前 aiops2025 转换中几乎没有可用输入：

| feature | 当前状态 | 影响 |
| --- | --- | --- |
| `trace_error_rate` | 代码不读取 `attr.status_code`，而转换未生成 `status_code/http.status_code/status` | 结构性缺席 |
| `trace_status_code_shift` | 能看到 `attr.status_code`，但 normal/abnormal 全是 `Ok` | 结构性为 0 |
| `trace_endpoint_shift` | 仍可计算 | 更像 path/span 分布漂移，缺少 status/error 支持 |
| `trace_duration/count/rows/topology` | 仍可计算且数据量大 | 容易代表传播和入口流量 |

这和 RCABench 很不同。RCABench 中很多故障是 request/response/status/path 类异常，trace status/path mutation 能提供根因特异性；aiops2025 当前转换后这部分信息被削弱了。

## Trace 覆盖问题

281 个 aiops2025 case 中，各模态 abnormal 数据对 GT 服务的覆盖率是：

| modality | GT covered | rate | median rows | median services |
| --- | ---: | ---: | ---: | ---: |
| metric | 230 / 281 | 0.819 | 18,304 | 15 |
| log | 215 / 281 | 0.765 | 58,796 | 10 |
| trace | 141 / 281 | 0.502 | 54,614 | 8 |

trace 对 JVM 类和部分 infra/pod 类故障覆盖很差。这里的“覆盖低”不是指 trace 文件为空；281 个 converted case 都有 abnormal trace，median 还有 54,614 行。问题是 raw Jaeger trace 只包含 8 个服务：

```text
frontend
productcatalogservice
recommendationservice
redis
cartservice
checkoutservice
shippingservice
emailservice
```

而 service-level label 中有 14 个服务名：

```text
adservice
cartservice
checkoutservice
currencyservice
emailservice
frontend
paymentservice
productcatalogservice
recommendationservice
redis-cart
shippingservice
tidb-pd
tidb-tidb
tidb-tikv
```

因此 `adservice`、`currencyservice`、`paymentservice`、`tidb-*` 等根因服务在 raw trace 服务空间中本来就不存在；这主要是原始 trace instrumentation / benchmark observability coverage 的问题，不是转换脚本把这些服务漏掉。一个小的转换/标准化问题是 raw trace 里叫 `redis`，label 里叫 `redis-cart`，这会影响少量 Redis case。

按 fault type 展开：

| fault type | trace GT coverage |
| --- | ---: |
| io-fault | 0 / 26 |
| jvm-gc | 0 / 12 |
| jvm-exception | 0 / 10 |
| jvm-cpu | 0 / 11 |
| jvm-latency | 0 / 13 |
| target-port-misconfig | 2 / 15 |
| pod-failure | 9 / 39 |
| cpu-stress | 10 / 18 |
| pod-kill | 8 / 14 |
| memory-stress | 10 / 16 |
| code-error | 15 / 19 |
| dns-error | 19 / 20 |
| network-loss | 20 / 20 |
| network-delay | 23 / 23 |
| network-corrupt | 25 / 25 |

这解释了为什么 trace 对 network/dns 有帮助，但会破坏 resource/JVM/pod case。

一个典型例子是 `aiops2025-fb327034-184-jvm-exception`，GT 是 `adservice`：

- `crest_metric_log` 中 `adservice` 排第 1，score=2.0；
- trace-only 中 `adservice` 的 `A/F/S/score` 全部是 0；
- full `crest` 中 `frontend/cart/checkout/recommendation/...` 都被 trace 结构抬到 `adservice` 前面。

另一个例子是 `aiops2025-4e221a94-277-memory-stress`，GT 是 `paymentservice`：

- `crest_metric_log` 中 `paymentservice` 排第 1；
- trace-only 中 `paymentservice` 没有 trace 支持；
- full `crest` 排第 1 变成 `checkoutservice`，`paymentservice` 掉到第 9。

相反，`aiops2025-178aa45f-353-dns-error` 和 `aiops2025-342d4820-100-network-corrupt` 中，trace 覆盖并强化了 `checkoutservice` 相关路径，全模态可以修复 `crest_metric_log` 的错误。

## CREST 机制如何放大这个问题

CREST 的 trace 不是普通加权项。它会进入三个位置：

1. `CREST_ROLE_FAMILIES` 把 trace 分成 mutation、propagation、observability volume 和 topology context。
2. `score_crest_services()` 中，trace 被用于构建 graph，生成 structural `F` 和 denoised `S`。
3. 最终分数是：

```text
score = A * F + S
```

对应实现：

```text
algorithms/evidencerank/src/evidencerank/crest.py:515 构造 trace graph
algorithms/evidencerank/src/evidencerank/crest.py:522-557 生成 F/S
algorithms/evidencerank/src/evidencerank/crest.py:559-561 score = A * F + S
```

当 trace root mutation 足够可靠时，这个结构解释能把传播受害者压下去，是 RCABench 上 CREST 有效的关键。但在 aiops2025 当前转换中，status root signal 缺失，trace 服务覆盖又窄，结构解释就主要由高流量入口和关键路径服务驱动。

Top1 集中度很直观：

| algorithm | Top1 最集中服务 | Top2 服务占比 |
| --- | --- | ---: |
| crest_metric_log | `frontend` 88, `adservice` 45 | 133 / 281 |
| crest | `frontend` 199, `checkoutservice` 48 | 247 / 281 |
| crest_trace | `frontend` 194, `checkoutservice` 79 | 273 / 281 |
| crest_metric_trace | `frontend` 167, `checkoutservice` 75 | 242 / 281 |
| crest_log_trace | `frontend` 219, `checkoutservice` 55 | 274 / 281 |

这说明 trace 加入后，排序空间被压到少数入口/关键路径服务，而不是更细地定位根因。

## 为什么 RCABench 中全模态更好

RCABench 的 fault taxonomy 和 aiops2025 service 转换后的数据形态不同。

RCABench 有大量 request/response/network/path/status 类故障：request/response delay、abort、replace code/body/method/path、partition、loss、corrupt 等。这些故障的根因证据常常不在单一 resource metric 上，而是在 trace duration/count/status/endpoint、log template/error 或拓扑传播中。因此全模态 CREST 能修复 metric/log 无法定位的 case。

aiops2025 当前 service 转换后的数据更像混合了两类任务：

- network/dns 类：trace 覆盖高，trace 可以帮助；
- JVM/resource/pod/infra 类：metric/log 更接近根因，trace 缺失根因服务或只记录入口流量，trace 会伤害排序。

因此同一个 CREST 结构融合在 RCABench 上是补充证据，在 aiops2025 上经常变成强传播噪声。

## RCAEval 中 CREST 为什么更稳

RCAEval RE2 的现象要分算法看。它并不是“所有算法全模态都最好”：

| Method | RE2-OB Top1 | RE2-SS Top1 | RE2-TT Top1 | 三子集均值 |
| --- | ---: | ---: | ---: | ---: |
| CREST(all) | 0.811 | 0.911 | 0.822 | 0.848 |
| CREST(metric-only) | 0.800 | 0.911 | 0.789 | 0.833 |
| CREST(metric+log) | 0.744 | 0.911 | 0.822 | 0.826 |
| CREST(trace-only) | 0.411 | 0.000 | 0.478 | 0.296 |
| EvidenceRank(all) | 0.711 | 0.811 | 0.778 | 0.767 |
| EvidenceRank(metric-only) | 0.800 | 0.911 | 0.789 | 0.833 |
| EvidenceRank(metric+log) | 0.544 | 0.811 | 0.733 | 0.696 |
| EvidenceRank(trace-only) | 0.211 | 0.000 | 0.022 | 0.078 |

CREST 的鲁棒性主要来自两个机制：

1. **没有 trace 时自动退化得比较干净。** RE2-SS 中 trace-only 为 0，CREST(all)、CREST(metric-only)、CREST(metric+log) 的 Top1 都是 0.911；也就是说 trace 缺失时 CREST 基本没有被空 trace 拖坏。
2. **trace 可用时作为结构支持，而不是单独替代 metric。** RE2-OB/TT 中 trace-only 的 Top1 不高，但 Top3/A5 有一定结构信息；CREST 的 `score = A * F + S` 让 metric local abnormality 先形成 `A`，trace graph 主要提供 `F/S`，所以可以小幅提升 metric-only。EvidenceRank/CERA 这类更直接的 feature/role 融合在 RCAEval 上更容易被 log/trace 噪声稀释，表现为 all 低于 metric-only。

所以 RCAEval 上 CREST 的“全模态强”不是因为 trace 独立很准，而是因为它的结构通道在 trace 弱或缺失时相对不破坏 metric 主信号，在 trace 有用时提供少量结构补益。aiops2025 当前转换则相反：trace 不只是弱，它还以高行数、高入口集中度、低服务覆盖的形式强力进入 `F/S`，并且 status/error 根因特异信号被转换丢失，所以会产生更大的负迁移。

## 为什么其他算法也普遍低

aiops2025 上不只是 CREST 低，很多算法都低，主要是数据表示和算法假设整体错位。

### 1. 一部分 case 在 service 候选空间里不可命中

把 normal+abnormal 的 metric/log/trace 服务名合并后，GT 服务出现在候选空间的 case 只有 230/281：

| candidate source | GT covered | rate |
| --- | ---: | ---: |
| metric candidate services | 230 / 281 | 0.819 |
| log candidate services | 226 / 281 | 0.804 |
| trace candidate services | 150 / 281 | 0.534 |
| all modality candidate services | 230 / 281 | 0.819 |

缺失的 51 个 case 集中在：

```text
io-fault:    26 / 26 missing
pod-failure: 25 / 39 missing
```

这些缺失 case 的 GT 多是 `tidb-tikv`、`tidb-pd`、`tidb-tidb`。也就是说，很多算法即使排序完全正确地在当前候选服务中找异常，也无法命中这些 label；这会把理论 AC@1 上限先压到约 0.819。

但最好算法只有 `AC@1=0.423`，说明低分不只来自不可命中 case，还来自下面的模态错配。

### 2. 不同故障类型依赖不同模态，单一算法容易顾此失彼

`cera_metric_log` / `evidencerank_metric_log` 是 aiops2025 当前最强，但它们也有明显盲区：

| fault type | cera_metric_log Top1 |
| --- | ---: |
| io-fault | 0 / 26 |
| dns-error | 0 / 20 |
| jvm-latency | 2 / 13 |
| pod-failure | 10 / 39 |
| network-delay | 6 / 23 |
| cpu-stress | 14 / 18 |
| jvm-exception | 9 / 10 |

metric/log 对 JVM/resource 类更好，对 DNS、IO、部分 network/path 类弱。trace/graph 类算法正好相反：`crest`、`microrca`、`microrank`、`shapleyiq` 在 network/dns 上相对更好，但 JVM/resource/pod 类大量为 0 或接近 0。

这意味着 aiops2025 当前数据集不是一个统一的“service RCA”分布，而是混合了：

- resource/JVM/pod 类：metric/log 更接近根因；
- network/dns/path 类：trace/topology 更有用；
- TiDB/infra 类：service label 与可观测 service 候选不一致；
- entry-path 传播类：trace 容易把入口服务排高。

没有模态置信度和候选覆盖修正时，大多数算法都会在某些 fault type 上大面积失效。

### 3. 很多 trace/topology 算法发生 Top1 塌缩

aiops2025 raw trace 只有 8 个服务，且流量高度集中在 `frontend` 等入口路径。很多依赖 trace/topology/调用图的算法 Top1 会塌缩到少数服务：

| algorithm | Top1 最常见服务 | 次数 | Top2 服务占比 |
| --- | --- | ---: | ---: |
| ton | `frontend` | 279 / 281 | 0.996 |
| microrca | `frontend` | 227 / 281 | 0.993 |
| crest_log_trace | `frontend` | 219 / 281 | 0.975 |
| cera_log_trace | `frontend` | 238 / 281 | 0.968 |
| microrank | `frontend` | 153 / 281 | 0.957 |
| shapleyiq | `frontend` | 225 / 281 | 0.904 |
| crest | `frontend` | 199 / 281 | 0.879 |

这类算法在 RCABench / RCAEval 中能利用 topology，是因为调用图覆盖的候选服务和故障服务更一致；在 aiops2025 当前转换中，调用图主要表达“谁在入口主路径上”，不一定表达“谁是根因”。

### 4. 部分 legacy 算法存在输出/命名适配问题

从输出 Top1 看，有些算法大量输出 `None` / `null`：

| algorithm | Top1 |
| --- | --- |
| microdig | `None` 281 / 281 |
| nezha | `None` 280 / 281 |
| baro | `null` 196 / 281 |
| simplerca | `None` 132 / 281 |

这说明不仅是 ranking 质量问题，还有 adapter / output name 与 service-level label 对不齐的问题。此类算法原本可能假设特定矩阵、调用图节点或 metric 命名格式；aiops2025 转成 RCABench v2 后，虽然文件齐全，但节点命名和输入结构未必满足它们的内部假设。

### 5. status 转换问题会影响所有 trace/status 类算法

当前 `conclusion.parquet` 也是从转换后的 `attr.status_code` 生成的。由于 trace status 全被写成 `Ok`，所有依赖 trace status、success rate、error span 或 conclusion success rate 的算法都会丢失一类关键异常信号。这不只影响 CREST/EvidenceRank，也会影响其他使用 trace 诊断结论或 span status 的方法。

因此，“其他算法也差”的主因不是某一个算法坏，而是当前 aiops2025 service-level 转换暴露了四个共同难点：

1. 候选服务空间和 label 空间不完全一致；
2. trace 覆盖窄、入口流量极强；
3. status/error 被转换抹平；
4. fault taxonomy 混合了 resource/JVM/network/DNS/infra，多数算法没有 per-case 模态置信度。

## 建议

优先先修转换，再考虑算法改动。

1. 修复 `transform_trace()` 的 status 转换：
   - 使用已有 `normalize_status(tags)` 生成 `attr.status_code`；
   - 同时保留或派生 `http.status_code`，让 `trace_error_rate` 能工作；
   - 重新生成 aiops2025 数据集并重跑 `crest_trace`、`crest_metric_trace`、`crest`、`crest_metric_log`。

2. 为 CREST 加 dataset-independent trace confidence gate：
   - 如果 trace 服务覆盖率显著低于 metric/log 服务覆盖率，降低 graph `F/S` 的作用；
   - 如果 case 内 `trace_status_code_shift` 和 `trace_error_rate` 全 0，且 trace Top1/Top2 过度集中在高流量服务，限制 `abnormal_trace_rows`、topology、duration/count 对最终排序的支配；
   - 如果 metric/log 对某个服务有强局部证据，但该服务没有 trace rows，不应仅凭 trace graph 把它大幅压低，除非 trace mutation evidence 很强。

3. 做最小 ablation 验证：
   - fixed-status conversion vs current conversion；
   - `crest` vs `crest_metric_log`；
   - `crest` with/without trace graph `F/S`；
   - `crest` with/without `abnormal_trace_rows` 和 topology context；
   - 按 fault type 报告 fixes/hurts，而不是只看总体 AC@1。

预期：修复 status 后，network/dns/code/path 类 case 可能继续受益；resource/JVM/pod 类仍需要 trace confidence gate，否则全模态仍可能被入口/关键路径 trace 吸走。
