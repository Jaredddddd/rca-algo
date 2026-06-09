# AIOps25 Component-Level 数据集重构可行性判断

本文回答一个具体问题：是否可以把 pod 也当成 service 一样进入排序空间，统一视为 `component` 排序，从而避免当前 `aiopschallenge2025_rcabench_service` 把 pod / KPI / instance 证据聚合到 service 后造成的稀释。

结论先行：

**可以重构，而且技术上比较可行；但它应该是一个新的 component-level 数据集，而不是静默替换当前 service-level 数据集。** 当前 230-case service 数据集适合评估“根因所属 service 是否排前”；component 数据集评估的是“根因组件 pod / service / node / edge endpoint 是否排前”。两者问题不同，指标不能直接混称。

补充目标边界：这里的目标不是单纯“更贴近 AIOps25 原始任务”，而是让转换后的输入粒度更符合 CREST 的证据建模方式。换句话说，数据构造应尽量保留 raw telemetry 中的 pod / object / KPI evidence atom，避免 service-level 投影让 CREST 的 `A * F + S` 在进入算法前就被削弱。这是 converter-to-algorithm input compatibility，不是 runtime 读取标签或 oracle 的算法特化。

RCAEval 适配中已经出现过类似问题：RCAEval wide metric 的列名本身是 `service + metric + anomaly` evidence atom；如果直接 melt 成 long table 再做 service-level summary，会改变 scoring unit 并导致性能下降。AIOps25 的对应教训是：pod / object / KPI provenance 本身就是 evidence atom，不应在转换阶段无条件压成 service aggregate。

## 1. 为什么这个方向是合理的

当前转换脚本 `scripts/build_aiopschallenge2025_rcabench.py` 做了 service-level 投影：

- `service_labels()` 会把 `instance_type == "pod"` 的原始实例名用 `service_from_pod()` 压成 service；
- `metric_service_name()` 会把 pod object id / pod name 也压成 service；
- `transform_log()` 从 `k8_pod` 得到 `service_name` 时同样去掉 pod suffix；
- `transform_trace()` 当前只把 Jaeger process serviceName 写入 `service_name`，没有把 process tags 里的 pod identity 提取出来。

这导致一类明显损失：真实异常集中在某个 pod / object / KPI family，但算法看到的是 service 聚合后的均值、计数和 trace 结构。对 `score = A * F + S` 来说，service 聚合会削弱 metric/log 的 `A`，而 trace 的 service-level propagation surface 仍然可能抬高入口或传播节点的 `F/S`。

已有 converted 230 case 的 telemetry 也支持 component 化：

| item | 当前 converted 230 case 统计 |
| --- | ---: |
| abnormal metric service 数 / case | median 15 |
| abnormal metric pod 数 / case | median 34 |
| abnormal log service 数 / case | median 10 |
| abnormal log pod 数 / case | median 23 |
| abnormal trace service 数 / case | median 8 |
| 从 `raw.process.tags` 可恢复的 abnormal trace pod 数 / case | median 17 |
| converted pod case 数 | 62 |
| converted pod case 中 GT pod 在 metric provenance 精确出现 | 62 / 62 |
| converted pod case 中 GT pod 在 log provenance 精确出现 | 51 / 62 |
| converted pod case 中 GT pod 在 trace process tags 精确出现 | 19 / 62 |

一个被当前 service-level 转换跳过的例子是 `io fault`，原始 instance 包含 `tidb-tikv-0` / `tidb-tikv`，但当前候选 service 只有 HipsterShop service 和少量泛化名，因此被归为 `skipped_unobservable_label`。这说明当前 51 个 `skipped_unobservable_label` 不是简单“无证据”，而是至少有一部分属于 component identity 被 service 投影丢失。

## 2. 技术上怎么重构

建议新增数据集，例如：

```text
aiopschallenge2025_rcabench_component
```

不要覆盖：

```text
aiopschallenge2025_rcabench_service
```

为了兼容当前 rcabench-platform 评估器和 CREST/CERA/EvidenceRank 的输出接口，可以继续让算法输出：

```text
AlgorithmAnswer(level="service", name="<component-id>", rank=...)
```

同时在 `labels.parquet` 里继续写：

```text
gt.level = "service"
gt.name = "<component-id>"
```

这里的 `level="service"` 只是平台兼容壳，语义应在文档中明确为 component rank。

推荐 component namespace 使用前缀避免重名：

| 原始对象 | component id |
| --- | --- |
| service `frontend` | `svc:frontend` |
| pod `frontend-0` | `pod:frontend-0` |
| node `aiops-k8s-06` | `node:aiops-k8s-06` |
| TiDB/TiKV/PD object | `obj:<object_type>:<object_id>` |
| network edge 可选表达 | `edge:<source>-><destination>` |

如果暂时只做 node ranking 算法不支持 edge，则 network case 可以先保留两个 endpoint label：

```text
svc:<source>
svc:<destination>
```

## 3. 三个模态的转换建议

### 3.1 Metric

metric 应使用最具体可观测 identity 作为 `service_name`：

1. 如果 `attr.k8s.pod.name` / `attr.aiops.pod` / `object_type == "pod"` 存在，写 `pod:<pod>`;
2. 如果是 node metric，写 `node:<node>`;
3. 如果是 TiDB/TiKV/PD 或其他 resource object，写 `obj:<object_type>:<object_id>`;
4. 如果只有 service，写 `svc:<service>`;
5. 原始 service parent 不应丢弃，可以保留在 `attr.k8s.service.name` 或新增 `attr.aiops.parent_service`。

默认不建议把同一条 pod metric 同时复制成 service aggregate 行，否则会重新引入 service 聚合稀释，并且让 service aggregate 与 pod component 互相竞争。若需要 parent-level relaxed evaluation，应另建 rollup 或离线映射，不混进主 component 排序输入。

### 3.2 Log

log 可从 `k8_pod` / `attr.k8s.pod.name` 得到 pod component：

```text
service_name = pod:<pod>
attr.k8s.service.name = svc:<service_from_pod(pod)>
```

没有 pod 的日志再 fallback 到 `svc:<service>`。

### 3.3 Trace

trace 当前没有把 pod 写入 `attr.k8s.pod.name`，但 `raw.process.tags` 中存在 `podName` / `name` / `nodeName` / `ip` 等字段。重构时应：

1. 从 process tags 提取 pod：
   - 优先 `podName`;
   - fallback 到看起来像 pod name 的 `name`;
2. `service_name` 写成 `pod:<pod>`，没有 pod 时 fallback 到 `svc:<raw.service_name>`;
3. 用 span 的 `parent_span_id` 重新 join 出 `parent_service`，此时 parent/child 都是 component id；
4. 同时保留 `attr.k8s.service.name = svc:<raw.service_name>`，用于解释和 parent rollup。

这一步很关键。若 trace 仍停在 service 级，而 metric/log 变成 pod 级，CREST 的 trace graph 会变成 service 节点和 pod 节点混合的弱连接图；虽然 metric pod 的 local `A` 不会消失，但 `F/S` 的解释力会变得不稳定。

## 4. Label 设计建议

建议把 component 数据集分成 primary 和 relaxed 两层文档语义，但主评估只用 primary。

Primary labels：

- `instance_type == "pod"`：标精确 pod，例如 `pod:adservice-1`;
- `instance_type == "service"`：标 service component，例如 `svc:adservice`;
- `instance_type == "node"`：如果纳入 component 数据集，标 `node:<node>`;
- network source/destination：先标 `svc:<source>` 和 `svc:<destination>`；若未来算法支持 edge rank，再标 `edge:<source>-><destination>`。

Relaxed labels 或 offline report：

- pod label 可以映射到 parent service；
- service label 可以映射到观测窗口内该 service 的 pod 集合；
- edge label 可以映射到两个 endpoint。

这样可以同时回答两个问题：

1. exact component rank 是否正确；
2. component 预测映射回 service 后是否覆盖当前 service-level 评价。

## 5. 预期 case 数

当前 service 数据集转换报告是：

| status | count |
| --- | ---: |
| original groundtruth | 400 |
| converted | 230 |
| skipped_node | 82 |
| skipped_empty | 37 |
| skipped_unobservable_label | 51 |

若只把 service/pod case 改成 component-level，理论上上限是：

```text
400 - 82 node - 37 empty = 281
```

也就是当前 230 个加上 51 个因为 service label 不可观测而被跳过的 case。这个数也与历史 281-case 版本的规模吻合，但需要用新的 component builder 重新验证，而不能复用旧输出。

若进一步把 node 也作为 component 纳入，理论上上限接近：

```text
400 - 37 empty = 363
```

但 node case 是否全部可评估，需要单独验证 node metric provenance、trace/log 是否为空、以及算法是否允许 metric-only/component-only 候选。

## 6. 对 CREST 的影响

component 化有可能改善 CREST 在 AIOps25 上的核心问题：

- pod / KPI 异常不再被 service 聚合稀释，metric/log local abnormality `A` 更集中；
- trace 如果只显示入口传播面，pod root candidate 至少不会被强行合并进入口 service；
- 若 trace process tags 成功恢复 pod，`F/S` 的结构解释可以从 service graph 细化到 pod/component graph；
- `crest_metric_log` 在 AIOps25 强，说明 metric/log ownership 本来就有信息；component 化会让这类 ownership 更干净。

但它也有风险：

- candidate 数从约 15 个 service 扩到每 case 30+ pod/resource，AC@1 会更难；
- service-level 故障如果只标 `svc:<service>`，而证据主要在 pod metric，算法可能需要 parent rollup 才公平；
- trace pod 覆盖不是满覆盖，converted 62 个 pod case 中 abnormal trace 精确出现 GT pod 只有 19/62；
- network case 本质是 edge，单 node/component rank 仍然是有损表示；
- 新数据集指标不能拿来证明原 service 数据集上的 CREST 已经优化成功。

## 7. 最小可行重构方案

第一版已经按“新增 builder，不动现有 service 数据集”的方式实现：

```text
scripts/build_aiopschallenge2025_rcabench_component.py
```

不建议第一版直接在现有 builder 里加：

```bash
--rank-granularity service|component
```

原因是当前 `build_aiopschallenge2025_rcabench.py` 已经把 service 语义写进多个位置：

- `service_labels()` 决定 label 压缩；
- `metric_service_name()` 决定 metric candidate；
- `transform_log()` 决定 log candidate；
- `transform_trace()` 决定 trace candidate 和 `parent_service`；
- `observable_labels()` 决定 case 过滤；
- `write_meta()` 固定写 service-level label。

component 化会同时改变这些位置。若只加一个参数，脚本里会出现大量 `if granularity == ...` 分支，容易误伤当前已经作为 baseline 使用的 service 数据集，也容易让后续实验不知道某次输出到底来自哪种语义。

更稳的工程形态是：

1. 新增 `scripts/build_aiopschallenge2025_rcabench_component.py`;
2. 复用原脚本中的时间窗口、schema、parquet 读写、safe name 等低风险工具；
3. 在新脚本中显式实现 component label policy、component metric/log/trace transform、component observable filter；
4. 输出独立 dataset name，例如 `aiopschallenge2025_rcabench_component`;
5. 生成独立 conversion report，明确记录它是 CREST-oriented feature-preserving component conversion。

等 component builder 验证稳定后，再考虑把两个脚本共同部分抽成 `scripts/aiopschallenge2025_rcabench_common.py`。不要第一步就为了复用而重构 service builder。

当前脚本默认策略：

- 输出数据集名：`aiopschallenge2025_rcabench_component`;
- 仍写 `gt.level = "service"`，保持平台和现有算法输出兼容；
- `gt.name` 写 component id，例如 `svc:emailservice`、`pod:emailservice-0`;
- metric/log/trace 的 `service_name` 都写 component id;
- metric 的 `metric` 字段写 evidence key，例如 `apm::request`、`pod::pod_cpu_usage`，必要时包含 `metric_group` / `kpi_key` / `kpi_name`;
- trace 从 `raw.process.tags` 恢复 pod，并用 component id 重建 `parent_service`;
- service / network endpoint 标签默认扩展到观测到的同服务 pod，例如 `svc:emailservice` 同时接受 `pod:emailservice-0/1/2`;
- 可用 `--no-expand-service-labels-to-pods` 关闭 service-to-pod label expansion;
- pod GT 默认只标 exact `pod:<pod>`，可用 `--include-parent-service-labels` 额外接受 parent `svc:<service>`;
- node case 和 node metric component 默认不纳入，可用 `--include-node` 显式打开；
- TiDB/TiKV/PD 等 metric-only resource object 默认不纳入，可用 `--include-resource-components` 显式打开。
- case 转换可用 `--jobs N` 并行；每个 worker 只写自己的 datapack，主进程统一写 meta。默认 `--jobs 1`，带 `--limit` smoke 时会回退到单进程以保持 limit 语义。

这里特意没有默认纳入 `node:*` 和 `obj:<object_type>:<object_id>`。原因是当前 CREST 的结构解释主要来自 trace graph，而这些 infra/resource object 在 AIOps25 转换中通常只有 metric provenance，没有 trace/log ownership，也没有与 pod/service trace graph 的可靠边。CREST 可以给它们 local metric `A`，但 `F/S` 只能退化为 isolated local support，容易成为强 distractor。若研究 node/resource RCA，可以显式打开开关并作为单独实验；默认面向 CREST 的 service/pod component 数据集应先保留 k8s service/pod 这类跨 metric/log/trace 更可解的组件。

注意：CREST 源码仍然按 `service_name, metric` 聚合 metric feature。component 数据集没有修改 CREST 运行时逻辑，而是把 `service_name` 的语义改成 `component_name`。因此实际聚合键变成：

```text
component_name, metric_evidence_key
```

这和 RCAEval 适配中的经验一致：转换层应保留算法需要的 evidence atom，而不是把多个原始 atom 提前合并成 service-level summary。

smoke 验证：

```bash
uv run --package evidencerank python scripts/build_aiopschallenge2025_rcabench_component.py \
  --data-root /tmp/aegis_aiops_component_smoke \
  --dataset aiopschallenge2025_rcabench_component_smoke \
  --limit 1 --overwrite
```

完整构建可用保守并行度，例如：

```bash
uv run --package evidencerank python scripts/build_aiopschallenge2025_rcabench_component.py \
  --dataset aiopschallenge2025_rcabench_component \
  --jobs 4 \
  --overwrite
```

首个 case `aiops2025-345fbe93-80-cpu-stress` 成功生成；labels 从 primary `svc:emailservice` 扩展为：

```text
pod:emailservice-0
pod:emailservice-1
pod:emailservice-2
svc:emailservice
```

样例输出中 abnormal metric/log/trace 都进入了 component 命名空间，trace `parent_service` 也恢复为 pod-level component graph。直接调用 `score_crest_services()` 可以正常排序该 datapack。

在默认 scope 下，同一 smoke case 的 candidate component 数从包含 node/resource object 时的 83 个降为 45 个；abnormal metrics 只保留 `pod` / `svc` 前缀，`node` 和 `obj` 不进入主候选空间。该 case 的 metric 输出包含 44 个 component、20 个 metric evidence key、699 个 `(component, metric)` atom。

第一版验收标准：

1. 生成 `aiopschallenge2025_rcabench_component`，不覆盖 `aiopschallenge2025_rcabench_service`;
2. `labels.parquet` 兼容平台评估，`gt.level` 暂用 `"service"`，`gt.name` 为 component id;
3. metric/log/trace 的 `service_name` 均写 component id;
4. trace 从 `raw.process.tags` 恢复 pod，并重建 `parent_service`;
5. 写出 conversion report，包含 primary label 类型分布、component candidate 覆盖、service/pod/node/edge case 数;
6. 跑 `crest`、`crest_metric_log`、`simplerca` 或其他对照算法，报告 exact component 指标和 map-to-service 后的 relaxed 指标。

## 8. 最终判断

这个方向是可行的，也更接近 AIOps25 原始问题里的“instance / pod / KPI / resource provenance”结构。它不是为了给 CREST 特化涨分，而是在修正当前 service-level 投影带来的评价粒度损失。

不过它不能替代现有 service 数据集的结论。更严谨的论文/实验表述应是：

- `aiopschallenge2025_rcabench_service`：service-level observable subset；
- `aiopschallenge2025_rcabench_component`：component-level reconstruction，保留 pod/resource identity；
- 同时报告 exact component 指标和 component-to-service relaxed 指标。

如果 component exact 指标更能反映 SimpleRCA / CREST / CERA 的差异，就说明 AIOps25 的主要困难确实不只是算法“不适配”，而是当前 service 投影把原始 RCA 任务的根因粒度压扁了。
