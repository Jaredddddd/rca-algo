# RCA 算法对比报告：EvidenceRank vs HeroSAS vs SimpleRCA

## 1. 总览

| 维度 | EvidenceRank | HeroSAS | SimpleRCA |
|------|-------------|---------|-----------|
| 数据模态 | 指标 + 链路 + 日志（三模态） | 仅指标（单模态） | 指标 + 链路 + 日志（三模态） |
| 核心方法论 | 多模态异常特征求和排序 | 稳态-异常-恢复时序模式检测 | 投票融合 / 加权评分（含多策略） |
| 是否有学习组件 | 无 | 无 | 无 |
| 可配参数 | 无（全部硬编码） | 12 个可调参数（HeroSASConfig） | 硬编码阈值散布于各策略中 |
| 活跃策略 | 单一策略 | 单一策略 | 4 种策略，当前激活 NezhaRCA |
| 依赖核心库 | pandas, numpy | pandas, numpy | polars, pandas, numpy |
| 平台 SDK | rcabench-platform >=0.3.30 | rcabench-platform >=0.4.1 | rcabench-platform >=0.3.30 |

---

## 2. 输入数据对比

### 2.1 数据源

| 数据源 | EvidenceRank | HeroSAS | SimpleRCA (NezhaRCA) |
|--------|-------------|---------|---------------------|
| normal_metrics.parquet | 必须 | 必须 | 必须 |
| abnormal_metrics.parquet | 必须 | 必须 | 必须 |
| normal_traces.parquet | 可选 | 不使用 | 必须 |
| abnormal_traces.parquet | 可选 | 不使用 | 必须 |
| normal_logs.parquet | 可选 | 不使用 | 必须 |
| abnormal_logs.parquet | 可选 | 不使用 | 必须 |
| metrics_sum.parquet | 不使用 | 可选 | 不使用 |
| metrics_histogram.parquet | 不使用 | 可选 | 不使用 |

### 2.2 服务名解析

三个算法均尝试多列回退策略来解析服务名，但优先列不同：

- **EvidenceRank**: `service_name` → `service` → `instance` → `attr.k8s.container.name` → `attr.k8s.deployment.name` → `attr.k8s.statefulset.name` → `attr.k8s.pod.name`
- **HeroSAS**: `service_name` → `attr.k8s.service.name` → `attr.k8s.deployment.name` → `attr.destination`（还会用正则剥离 Pod 后缀，并过滤基础设施服务如 cilium-agent、kube-proxy 等）
- **SimpleRCA**: 各 adapter 有独立逻辑；Nezha adapter 使用 `service_name` 列，并对 Pod 名做 `clean_node_name` 清洗

---

## 3. 核心算法逻辑对比

### 3.1 EvidenceRank — 多模态特征向量求和

**特征提取**（共 15 维）：

| 类别 | 特征 | 计算方式 |
|------|------|---------|
| 指标 | metric_max_z | z-score 最大值 |
| 指标 | metric_mean_z | z-score 均值 |
| 指标 | metric_anomaly_count | z > 3.0 的指标数 |
| 指标 | metric_value_delta | 均值绝对差累计 |
| 指标 | abnormal_metric_rows | 异常期指标行数 |
| 链路 | trace_duration_z | 延迟 z-score |
| 链路 | trace_duration_delta | 延迟差值 |
| 链路 | trace_count_delta | 调用量变化 |
| 链路 | trace_error_rate | 错误率 |
| 日志 | log_error_rate | 错误关键词占比 |
| 日志 | log_count_delta | 日志量变化 |
| 日志 | log_template_delta | 新增日志模板数 |
| 拓扑 | topology_in_degree | 被调用次数 |
| 拓扑 | topology_out_degree | 调用他人次数 |

**评分**：`score = Σ log1p(max(feature, 0))`，所有特征等权求和。

**排序**：按总分降序，得分最高者为 rank 1。

### 3.2 HeroSAS — 时序异常检测 + 降噪 + 聚合

**检测流程**：

1. **稳定基线验证**：取正常期尾部 N 个点，要求标准差低于阈值
2. **跳变检测**：异常期峰值与基线的差值需超过 `jump_threshold_factor * max(stable_std, min_jump_floor)`
3. **恢复验证**（可选）：峰值后数据需恢复平稳
4. **鲁棒 z-score**：使用 IQR 代替标准差，降低异常值干扰
5. **事件评分**：`score = delta × (1 + min(log1p(robust_z), 5) / 5)`
6. **降噪**：逐指标去除低分事件；逐指标去除产生过多时间簇的噪声指标
7. **全局过滤**：去除低于全局最高分 × 阈值的事件

**服务聚合**：

```
service_score = max(event_score) + 0.25 × Σ(event_scores) + 2.0 × log1p(distinct_metric_count)
```

三项分别捕捉：最严重异常、累积证据、影响面广度。

### 3.3 SimpleRCA (NezhaRCA) — 三路投票融合

**三路独立检测**：

| 检测器 | 核心逻辑 | 异常判定 |
|--------|---------|---------|
| 指标检测 | 正常期 P95 作为基线，乘以 1.19x 系数 | 异常值 > 阈值 且 CPU/内存 > 80 |
| 链路检测 | P90 延迟（ms） | P90 > 100ms（排除前端服务） |
| 日志检测 | 错误率增加 / 日志量下降 / 简单错误计数 | 错误率增幅 > 1.5x / 日志量下降 > 40% |

**投票融合**：

```
vote_score = Σ(position_score × weight)
```

- 每路检测器贡献 top-5 服务
- 位置评分：rank 1 = 5 分，rank 2 = 4 分，...，rank 5 = 1 分
- 指标权重 1.2，链路和日志权重 1.0

---

## 4. 方法论差异分析

### 4.1 根因定位思路

| 算法 | 思路 | 优势 | 劣势 |
|------|------|------|------|
| EvidenceRank | 多模态异常证据累加 | 信息利用充分，能捕捉跨模态异常关联 | 各模态等权，无法区分信号强弱 |
| HeroSAS | 指标时序突变检测 | 对指标异常检测精度高，降噪机制完善 | 不使用链路和日志信息，对非指标类故障盲区大 |
| SimpleRCA | 多检测器投票 | 鲁棒性好，单路检测失败不影响整体 | 投票机制较粗糙，各路检测器权重固定 |

### 4.2 统计方法对比

| 统计方法 | EvidenceRank | HeroSAS | SimpleRCA |
|----------|-------------|---------|-----------|
| z-score | 指标和链路 | 鲁棒 z-score（IQR） | 不使用 |
| 分位数基线 | 不使用 | 不使用 | P95（指标）、P90（链路） |
| 固定阈值 | z > 3.0 判异常 | jump_threshold 等 | CPU/内存 > 80、延迟 > 100ms |
| 时序模式 | 不使用 | 稳态-跳变-恢复 | 不使用 |
| log 变换 | log1p 归一化 | log1p 评分调制 | log1p 评分调制 |

### 4.3 拓扑利用

| 算法 | 拓扑信息 | 用途 |
|------|---------|------|
| EvidenceRank | 从 trace 的 parent-child span 中提取有向边 | 作为入度/出度两个特征维度参与评分 |
| HeroSAS | 不使用 | — |
| SimpleRCA | 不使用 | — |

---

## 5. 评分与排序机制对比

```
EvidenceRank:  score = Σ log1p(features)           → 等权求和，信息全面但无重点
HeroSAS:       score = max + 0.25×sum + 2×log1p(n) → 强调最严重异常，兼顾广度
SimpleRCA:     score = Σ(position × weight)         → 投票制，鲁棒但精度受限于位置量化
```

| 特性 | EvidenceRank | HeroSAS | SimpleRCA |
|------|-------------|---------|-----------|
| 评分连续性 | 连续实数 | 连续实数 | 离散整数（5/4/3/2/1） |
| 对多异常场景的区分 | 各异常加权累加，区分度好 | max+sum 联合，区分度好 | 投票分有限，区分度一般 |
| 对单点强异常的敏感度 | 中等（被其他特征稀释） | 高（max 主导） | 取决于检测器排名 |

---

## 6. 可扩展性与可配性对比

| 维度 | EvidenceRank | HeroSAS | SimpleRCA |
|------|-------------|---------|-----------|
| 新增数据模态 | 需修改特征矩阵和 BASE_FEATURE_NAMES | 不适用（设计为指标专用） | 需新增 adapter 和检测器 |
| 参数调优 | 无参数，无法调优 | 12 个参数，可精细调节 | 硬编码阈值，需改源码 |
| 多数据集适配 | 靠服务名多列回退兼容 | 靠服务名多列回退 + 正则清洗 | 4 套 adapter 分别适配不同数据集格式 |
| 代码组织 | 单文件 (~300 行) | 单文件 (~408 行) | 多文件，4 策略 + 4 adapter |

---

## 7. 适用场景建议

| 场景 | 推荐算法 | 原因 |
|------|---------|------|
| 指标类故障（CPU 飙升、内存泄漏等） | HeroSAS | 专门的时序突变检测，降噪完善，精度最高 |
| 需要利用多模态信息的通用场景 | EvidenceRank | 三模态 + 拓扑，信息利用最全面 |
| 多种数据集格式、需要灵活切换 | SimpleRCA | 内置 4 套 adapter，覆盖 Nezha/Eadro/AIOps 等格式 |
| 缺乏指标数据，只有日志和链路 | EvidenceRank 或 SimpleRCA | HeroSAS 无法处理 |
| 需要精细调参以适配特定环境 | HeroSAS | 唯一提供可配参数的算法 |
| 快速原型验证 | EvidenceRank | 无参数，即插即用 |

---

## 8. 总结

三个算法定位不同：

- **EvidenceRank** 是信息最全面的多模态融合方案，以"证据累加"为核心理念，适合需要综合判断的通用场景，但等权求和的策略在信号强弱差异大时可能被噪声稀释。
- **HeroSAS** 是指标异常检测的专家方案，采用稳态-跳变-恢复的时序模式匹配，降噪机制最完善，是唯一提供丰富可配参数的算法，但在非指标类故障上完全无效。
- **SimpleRCA** 是最灵活的工程方案，内置多策略和多数据集适配器，投票融合保证了鲁棒性，但评分粒度较粗，定位精度受限于离散的位置分。
