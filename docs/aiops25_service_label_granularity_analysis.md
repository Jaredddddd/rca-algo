# AIOps25 Service-Level 转换与标签粒度分析

本文检查 `scripts/build_aiopschallenge2025_rcabench.py` 对 AIOpsChallenge2025 的筛选和构建逻辑，并分析当前 `aiopschallenge2025_rcabench_service` 230 个 case 的 GT service、reason/fault 类型和 provenance 分布。

结论先行：

**AIOps25 转成 service-rank 数据集后存在明显粒度压缩：原始 root cause 经常在 pod / instance / KPI / edge 上，但评估标签被压成 service。这个数据集可以作为“service-level observable subset”使用，但不适合作为唯一标准来评价一个只输出 service rank 的 RCA 算法是否真正解决了 AIOps25 原题。**

## 1. 转换脚本做了什么

主脚本：

```text
scripts/build_aiopschallenge2025_rcabench.py
```

关键转换逻辑如下。

### 1.1 Label 压缩逻辑

`service_labels(row)` 把原始 groundtruth 转为 service 级标签：

- 网络类故障如果有 `source` 和 `destination`，标签变成 `[source, destination]`；
- 否则如果有 `service` 字段，直接使用 `service`；
- 否则如果 `instance_type == "pod"`，从 pod 名去掉 replica/hash 后推导 service；
- 最终只写入 `gt.level = service` 和 `gt.name = label`。

这意味着：

- pod-level 故障不再评估具体 pod；
- node-level 故障默认被跳过；
- network edge 故障被变成两个 endpoint service；
- `reason` 不进入 `labels.parquet`，只在原始 groundtruth / `injection.json` 中保留。

### 1.2 数据窗口

`case_windows()` 使用：

- normal window: `[start - max(duration, min_window), start]`
- abnormal window: `[start, start + max(duration, min_window)]`
- 默认 `min_window_minutes = 10`

这对持续时间很短的故障会强制扩展到 10 分钟窗口。

### 1.3 过滤逻辑

默认转换会跳过：

- `instance_type == "node"` 的全部 case；
- 无 service label 的 case；
- normal/abnormal traces 或 normal/abnormal metrics 任一为空的 case；
- service-level label 在 metrics/logs/traces 候选服务集合中完全不可观测的 case。

当前转换报告：

| item | count |
| --- | ---: |
| original groundtruth | 400 |
| converted | 230 |
| skipped_node | 82 |
| skipped_empty | 37 |
| skipped_unobservable_label | 51 |
| skipped_no_labels | 0 |

其中非 node case 共 318 个，最终只保留 230 个。51 个 `skipped_unobservable_label` 全部来自 pod-level case，主要是：

| skipped_unobservable fault_type | count |
| --- | ---: |
| io fault | 26 |
| pod failure | 25 |

这说明当前 230-case 数据集已经不是完整 AIOps25，而是“service/pod 且 trace/metric 不空且 service label 可观测”的子集。

## 2. 当前 230 个 case 的 GT 粒度

原始 400 个 groundtruth 的 `instance_type` 分布：

| instance_type | count |
| --- | ---: |
| service | 195 |
| pod | 123 |
| node | 82 |

转换后 230 个 case：

| instance_type | count |
| --- | ---: |
| service | 168 |
| pod | 62 |

这 62 个 pod case 在 `labels.parquet` 中全部被压成 service label。例如：

| datapack | original instance_type | original instance | converted label |
| --- | --- | --- | --- |
| `aiops2025-31392fda-93-memory-stress` | pod | `shippingservice-0` | `shippingservice` |
| `aiops2025-6ef260df-97-jvm-gc` | pod | `adservice-1` | `adservice` |
| `aiops2025-0efb9550-160-memory-stress` | pod | `productcatalogservice-2` | `productcatalogservice` |
| `aiops2025-cebb47f5-165-pod-kill` | pod | `paymentservice-1` | `paymentservice` |

这就是粒度压缩：真实注入对象是 pod，但评估只问 service。

## 3. GT service 分布

当前 `labels.parquet` 有 298 行标签，对应 230 个 datapack。差异来自 68 个 network case 有两个 service 标签。

每个 case 的 GT label 数：

| labels per case | count |
| --- | ---: |
| 1 | 162 |
| 2 | 68 |

GT service label 行分布：

| gt.name | label rows |
| --- | ---: |
| adservice | 60 |
| checkoutservice | 60 |
| frontend | 36 |
| cartservice | 29 |
| productcatalogservice | 23 |
| recommendationservice | 20 |
| paymentservice | 19 |
| currencyservice | 18 |
| shippingservice | 18 |
| emailservice | 10 |
| redis-cart | 5 |

注意：这是 label row 统计，network edge case 会同时给 source 和 destination 记一次。

按 case 的 label 组合看，单 service 中 `adservice` 最多：

| label combination | cases |
| --- | ---: |
| adservice | 55 |
| checkoutservice | 29 |
| currencyservice | 13 |
| shippingservice | 13 |
| paymentservice | 12 |
| cartservice | 11 |
| productcatalogservice | 9 |
| recommendationservice | 8 |
| checkoutservice+paymentservice | 7 |
| cartservice+frontend | 7 |
| emailservice | 6 |
| frontend+recommendationservice | 6 |
| productcatalogservice+recommendationservice | 6 |
| cartservice+checkoutservice | 6 |
| frontend | 6 |

这说明当前 service-level 评估中，GT 服务分布并不均匀，`adservice` 和 `checkoutservice` 权重很大。

## 4. Reason / fault 分布

原始 `groundtruth.jsonl` 没有单独的 `reason` 字段。README 说明：

- `key_metrics` 用于 reason 字段关键词评分；
- `fault_description` 用于 reason 字段语义评分；
- `fault_category` / `fault_type` 是结构化故障类型。

因此这里用 `fault_category`、`fault_type`、`key_metrics` 共同描述 reason 分布。

### 4.1 fault_category

| fault_category | cases |
| --- | ---: |
| network attack | 68 |
| jvm fault | 46 |
| stress test | 34 |
| pod fault | 28 |
| dns fault | 20 |
| erroneous change | 19 |
| misconfiguration | 15 |

### 4.2 fault_type

| fault_type | cases |
| --- | ---: |
| network corrupt | 25 |
| network delay | 23 |
| network loss | 20 |
| dns error | 20 |
| code error | 19 |
| cpu stress | 18 |
| memory stress | 16 |
| target port misconfig | 15 |
| pod failure | 14 |
| pod kill | 14 |
| jvm latency | 13 |
| jvm gc | 12 |
| jvm cpu | 11 |
| jvm exception | 10 |

### 4.3 key_observations 模态集合

| key_observation type set | cases |
| --- | ---: |
| log+metric+trace | 105 |
| log+metric | 43 |
| metric | 34 |
| metric+trace | 25 |
| log | 21 |
| none | 2 |

单独按 observation type 计数：

| type | cases |
| --- | ---: |
| metric | 207 |
| log | 169 |
| trace | 130 |

这个分布支持一个重要判断：AIOps25 并不是纯 trace 数据集，metric/log 在 groundtruth reason 中更常出现。trace 只在 130/230 个 converted case 的 key observations 中出现，而 metric 在 207/230 个 case 中出现。

### 4.4 key_metrics 高频项

| key_metric | cases |
| --- | ---: |
| request | 109 |
| response | 109 |
| rrt | 77 |
| rrt_max | 77 |
| pod_network_receive_bytes | 67 |
| pod_network_receive_packets | 67 |
| pod_network_transmit_bytes | 67 |
| pod_network_transmit_packets | 67 |
| error | 43 |
| pod_processes | 33 |
| pod_cpu_usage | 29 |
| error_ratio | 29 |
| client_error | 28 |
| client_error_ratio | 28 |
| dns | 20 |
| http.resp.status | 20 |
| 302 | 20 |
| pod_memory_working_set_bytes | 15 |
| port | 15 |

这里大量 reason keyword 本身就是 KPI / metric 名称，尤其是 `pod_*`、`rrt`、`request/response`、`error_ratio`。

## 5. Metric provenance 证明：证据确实在 pod / instance / KPI

转换脚本没有丢弃 metric provenance。`METRIC_SCHEMA` 保留了：

- `attr.aiops.object_id`
- `attr.aiops.object_type`
- `attr.aiops.instance`
- `attr.aiops.pod`
- `attr.aiops.device`
- `attr.aiops.mountpoint`
- `attr.aiops.kpi_key`
- `attr.aiops.kpi_name`
- `attr.aiops.metric_group`
- `attr.aiops.metric_file`
- `attr.k8s.pod.name`

在 230 个 converted case 的 abnormal metrics 中，共有 4,413,494 行 metric。provenance 覆盖情况：

| column | non-empty rows | row rate | non-empty cases |
| --- | ---: | ---: | ---: |
| service_name | 4,413,494 | 1.000 | 230/230 |
| metric | 4,413,494 | 1.000 | 230/230 |
| attr.aiops.metric_group | 4,413,494 | 1.000 | 230/230 |
| attr.aiops.metric_file | 4,413,494 | 1.000 | 230/230 |
| attr.aiops.object_type | 4,413,494 | 1.000 | 230/230 |
| attr.k8s.pod.name | 3,904,183 | 0.885 | 230/230 |
| attr.aiops.kpi_key | 2,766,475 | 0.627 | 230/230 |
| attr.aiops.kpi_name | 2,766,475 | 0.627 | 230/230 |
| attr.aiops.instance | 2,766,475 | 0.627 | 230/230 |
| attr.aiops.pod | 2,766,475 | 0.627 | 230/230 |
| attr.aiops.device | 2,766,475 | 0.627 | 230/230 |
| attr.aiops.mountpoint | 2,766,475 | 0.627 | 230/230 |
| attr.aiops.object_id | 1,647,019 | 0.373 | 230/230 |

更关键的是：

| check | result |
| --- | ---: |
| converted pod cases | 62 |
| GT pod exact match in metric provenance | 62 / 62 |
| pod cases with any pod provenance | 62 / 62 |
| service cases with GT instance exact match in metric provenance | 168 / 168 |

这直接坐实了你的判断：**原始 GT 的 pod / service instance 在 metric provenance 中可见，但 service-level 评估把它们压成 service label。**

每个 case 的 metric provenance 基数也很大：

| item | min | median | max |
| --- | ---: | ---: | ---: |
| services in abnormal metrics | 14 | 15 | 15 |
| KPI keys | 65 | 66 | 66 |
| object_ids | 37 | 40 | 43 |
| pod identities | 33 | 34 | 34 |

也就是说，每个 incident 的 metric 表不是“一个 service 一个 metric”，而是包含约 15 个 service、约 34 个 pod、约 66 个 KPI key 的大候选空间。对 service-rank 算法来说，如果只把这些 evidence 聚合到 service，会天然稀释“某个 pod / 某个 KPI family 的集中异常”。

## 6. 这个数据集是否适合 service-rank RCA

结论要分层说。

### 6.1 适合作为 service-level proxy，但不是原题完整评价

当前 230-case 数据集适合用来问：

> 在可观测 service label 子集上，算法能否把 root 所属 service 排到前面？

但它不适合单独用来问：

> 算法是否真正解决了 AIOps25 原始 RCA 问题？

原因是原题包含更细粒度的 root cause 和 reason：

- pod-level 故障要求知道具体 pod；
- node-level 故障被当前转换完全跳过；
- network 类故障本质是 source-destination edge，转换后变成两个 service label；
- reason 字段依赖 key_metrics / fault_description，但 service-rank 评估完全忽略 reason；
- metric evidence 中有强 KPI/provenance 信息，但 service-rank 标签无法奖励算法指出具体 KPI/pod。

### 6.2 对 service-only 算法的影响

当前转换会制造两类困难：

1. **细粒度 root 被 service 聚合稀释。**  
   例如某个 `adservice-1` 的 JVM GC 或某个 `productcatalogservice-2` 的 memory stress，metric provenance 能看到具体 pod 和 KPI，但 service-rank 算法如果只按 service 聚合，可能被同 service 其他 pod 或全局流量症状稀释。

2. **trace surface 可能压过 metric/log provenance。**  
   AIOps25 中很多 trace 异常表现为入口或传播路径，而不是 root pod/service。full CREST 在 AIOps25 上低于 `crest_metric_log`，正是这种结构的表现。

### 6.3 对算法设计的合理方向

如果继续用 service-rank 评估 AIOps25，算法需要把细粒度 provenance 转化成 service-level root evidence：

- 在 service 内检测少数 pod / instance / object_id 的集中异常；
- 在 service 内检测少数 KPI family / kpi_key 的集中异常；
- metric/log 强 ownership 的 service 不应被 trace surface 大幅压低；
- network case 应考虑 edge-level 或 pair-level evidence，而不是只看单服务；
- 最好同时输出 service + supporting pod/KPI/reason，service rank 只作为降维后的评估。

## 7. 最终判断

当前 `aiopschallenge2025_rcabench_service` 的 230 个 case 并不是无效数据集，但它是一个**有损 service-level 投影**：

- 它跳过了全部 82 个 node case；
- 跳过了 51 个 service label 不可观测的 pod case；
- 保留的 62 个 pod-level case 全部被压成 service label；
- 68 个 network edge case 被压成两个 endpoint service label；
- reason / KPI / fault_description 没有进入 service-rank label；
- metric provenance 中广泛存在 pod、instance、object、KPI 信息。

因此，如果目标是评估“服务级根因定位”，这个数据集可以使用，但必须在论文和实验中明确叫做 service-level observable subset。如果目标是评价 AIOps25 原始 RCA 能力，它不够充分，至少应该补充 instance/pod/KPI/reason 级评估，或者在 service-rank 算法中显式利用 provenance ownership。
