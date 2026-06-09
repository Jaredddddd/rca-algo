# AIOps25 Component 数据集上 CREST 仍然较差的原因分析

本文分析 `aiopschallenge2025_rcabench_component` 上 `crest` 指标仍然较低的原因，并对照之前 RCAEval 适配中的“转换不能破坏 evidence atom 粒度”经验。

当前结果：

```text
dataset = aiopschallenge2025_rcabench_component
algorithm = crest
total = 230
error = 0
AC@1 = 0.356522
MRR = 0.477889
AC@3 = 0.495652
AC@5 = 0.617391
runtime.avg = 149.618032s
```

## 1. 先区分两种可能

component 数据集变差可能有两类原因：

1. 算法预测到了正确 service，但预测的是错误 pod；
2. 算法 top1 仍然是错误 service，只是现在名字变成了 pod。

把 component 输出折回 parent service 后重新计算 relaxed service 指标：

| view | AC@1 | AC@3 | AC@5 | MRR |
| --- | ---: | ---: | ---: | ---: |
| exact component | 0.356522 | 0.495652 | 0.617391 | 0.477889 |
| mapped-to-service relaxed | 0.356522 | 0.608696 | 0.704348 | 0.535687 |

关键结论：

**AC@1 完全没有变化，说明 top1 不是“正确 service 的错误 pod”，而是大量 case 仍然预测到了错误 service。**

mapped-to-service 后 AC@3/AC@5 明显提升，说明 component 拆分确实带来了 top-k crowding：同一个错误高流量 service 的多个 pod 会占住前几名。但 top1 失败的本质仍然是 service-level root 判断错。

## 2. Top1 极度集中在入口/高流量 pod

component top1 分布：

| top1 component | cases |
| --- | ---: |
| `pod:frontend-2` | 57 |
| `pod:frontend-1` | 54 |
| `pod:frontend-0` | 48 |
| `pod:checkoutservice-2` | 23 |
| `pod:checkoutservice-1` | 11 |
| `pod:checkoutservice-0` | 9 |

折回 service 后：

| top1 service | cases |
| --- | ---: |
| `frontend` | 159 |
| `checkoutservice` | 43 |
| `cartservice` | 14 |
| `shippingservice` | 6 |

这说明 component 化后，CREST 不是更稳定地找到 root-owned pod，而是把原本 service-level 的入口/高流量面进一步拆成多个高分 pod。frontend / checkoutservice 仍然主导 top1。

## 3. 按 GT service 看，入口服务天然吃满

按 service label row 统计 top1 是否命中：

| GT service | labels | hit | rate |
| --- | ---: | ---: | ---: |
| `frontend` | 36 | 36 | 1.000 |
| `checkoutservice` | 60 | 36 | 0.600 |
| `shippingservice` | 18 | 10 | 0.556 |
| `paymentservice` | 19 | 8 | 0.421 |
| `cartservice` | 29 | 12 | 0.414 |
| `recommendationservice` | 20 | 8 | 0.400 |
| `emailservice` | 10 | 4 | 0.400 |
| `productcatalogservice` | 23 | 8 | 0.348 |
| `currencyservice` | 18 | 3 | 0.167 |
| `adservice` | 60 | 6 | 0.100 |
| `redis-cart` | 5 | 0 | 0.000 |

最常见的错法是：GT 是其他服务，但 top1 是 frontend。

| wrong pattern | cases |
| --- | ---: |
| `adservice -> frontend` | 46 |
| `checkoutservice -> frontend` | 21 |
| `cartservice -> frontend` | 17 |
| `currencyservice -> frontend` | 13 |
| `productcatalogservice -> frontend` | 13 |
| `recommendationservice -> frontend` | 12 |

这说明 component 粒度没有自动解决“入口/传播受害者识别”。CREST 的 structural support 仍然把高入口、高 trace row、高路径覆盖的 pod 看成最能解释 incident 的 component。

## 4. 按 fault type 看，metric/root-local 类仍然弱

按 case 统计 top1 命中率：

| fault_type | cases | hit | rate |
| --- | ---: | ---: | ---: |
| `jvm latency` | 13 | 0 | 0.000 |
| `target port misconfig` | 15 | 0 | 0.000 |
| `jvm gc` | 12 | 0 | 0.000 |
| `jvm exception` | 10 | 0 | 0.000 |
| `jvm cpu` | 11 | 1 | 0.091 |
| `pod kill` | 14 | 2 | 0.143 |
| `pod failure` | 14 | 3 | 0.214 |
| `cpu stress` | 18 | 4 | 0.222 |
| `memory stress` | 16 | 4 | 0.250 |
| `code error` | 19 | 7 | 0.368 |
| `network delay` | 23 | 12 | 0.522 |
| `dns error` | 20 | 12 | 0.600 |
| `network loss` | 20 | 16 | 0.800 |
| `network corrupt` | 25 | 21 | 0.840 |

网络类 `network loss/corrupt` 较好，说明当 trace/path/edge 症状和 endpoint root 对齐时，CREST 的结构机制仍然有效。

JVM、pod、stress、misconfig 类很弱，说明它们的 root evidence 更偏 metric/log/provenance，而 trace 多数时候只是入口或传播症状。component 化保留了 pod 粒度，但没有改变 CREST 对 trace structural support 的信任方式。

## 5. 为什么 component 化没有带来预期提升

### 5.1 它修的是输入粒度，不是 trace root eligibility

component 数据集已经把：

```text
service_name -> component_name
metric -> metric_evidence_key
```

因此 CREST 的 metric 聚合键实际变成：

```text
component_name, metric_evidence_key
```

这符合 RCAEval 适配中的核心经验：转换层应保留 evidence atom，不应提前聚合成 service-level summary。

但 CREST 的主排序仍然是：

```text
score = A * F + S
```

其中 `F/S` 依赖 trace graph / parent context / counterfactual structural support。AIOps25 的许多 incident 中，trace 不是 root evidence，而是传播面或入口流量面。component 化会把 frontend 拆成 `frontend-0/1/2`，但这三个 pod 仍然拥有大量 trace rows、path distribution shift、parent-child context，因此继续占据 top1/top3。

### 5.2 component 拆分会放大错误高流量 service 的 top-k crowding

service-level 时，错误的 frontend 只占一个名次。component-level 时，错误的 frontend 可能占三个名次：

```text
pod:frontend-0
pod:frontend-1
pod:frontend-2
```

这解释了 mapped-to-service relaxed AC@3/AC@5 明显高于 exact component AC@3/AC@5：不是 root 信号不存在，而是错误入口 service 的多个 pod 把 top-k 挤满了。

### 5.3 Metric evidence 仍不等于 root ownership

component 转换保留了 `metric_group/kpi_key/kpi_name` 到 `metric` evidence key，但 CREST 的 metric feature 仍是 z-score、count、delta 等 summary：

```text
metric_max_z
metric_mean_z
metric_anomaly_count
metric_value_delta
metric_count_drop_shift
abnormal_metric_rows
```

这些信号能表示“某个 component 的 metric 变化强”，但不能充分判断：

- 这个 pod 是 root 还是受害者；
- 这个 KPI 是资源根因 KPI 还是请求/响应传播 KPI；
- metric/log 与 trace 是否时间对齐；
- trace top pod 是否只是入口/高流量 surface。

因此 metric 粒度修正后，CREST 仍可能把 request/response/error 传播指标和 trace volume 一起解释成入口 pod root。

### 5.4 默认 component scope 没有恢复 51 个 TiDB/TiKV/PD case

当前默认 component 数据集仍然是 230 个 case。原因是上一版 51 个 `skipped_unobservable_label` 实际是：

| instance | count |
| --- | ---: |
| `tidb-tikv-0`, `tidb-tikv` | 41 |
| `tidb-pd-0`, `tidb-pd` | 5 |
| `tidb-tidb-0`, `tidb-tidb` | 5 |

这些属于 TiDB/TiKV/PD resource object。当前 CREST 对它们缺少 trace/log ownership 和结构边，因此默认没有纳入 `obj:*` 候选。也就是说，这次 component 化主要修正了 230 个 service/pod observable case 的输入粒度，并没有扩充评估 case 数。

## 6. 结论

component 数据集不是无效；它确实修正了 service-level 投影的一个问题：

- pod identity 保留了；
- trace pod graph 恢复了；
- metric evidence key 保留了 `metric_group/kpi_key` 粒度；
- CREST 实际按 `(component_name, metric_evidence_key)` 聚合。

但 CREST 在 AIOps25 上差的主因不只是“service 聚合稀释”，而是：

```text
trace structural support 在大量 AIOps25 incident 中仍然更像传播/入口症状，
而不是 root cause evidence。
```

因此仅靠数据转换不能把 CREST 拉高。下一步如果继续优化 CREST，最优先仍应是无监督 trace root eligibility / modality confidence：

- 判断 trace 是否有资格解释 root cause；
- 限制 frontend/checkout 这类高入口 pod 的 structural dominance；
- 在 trace 低可信时让 metric/log/provenance ownership 更强；
- 对同一错误 service 的多个 pod 做 top-k 去拥挤或 service-cluster competition。

换句话说：component 数据集修掉了“输入粒度错配”，但没有修掉“trace 被当作 root 解释器”的算法问题。
