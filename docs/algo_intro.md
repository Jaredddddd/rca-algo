### 核心算法介绍速览

| 算法 | 主要数据 | 学习范式 | 方法类型 | 核心思路 | 输出粒度 |
|---|---|---|---|---|---|
| `art` | metrics / traces / logs | 无监督 / 正常基线训练 | 深度学习 / 图学习 / 表示学习 | 用滑动窗口构造服务图样本，AutoRegressor 学习正常表示，再用系统级和实例级偏离相似度做 RCL 排名。 | service |
| `baro` | metrics | 无监督 | 统计方法 / 阈值偏离 | 将指标转成 `service_metric` 宽表，用正常阶段中位数/IQR 计算异常阶段 RobustScaler 偏离，并按 service 聚合。 | service |
| `causalrca` | metrics | 无监督 | 深度学习 / 因果发现 / PageRank | 用 NOTEARS/MLP 学习指标级因果图，在邻接矩阵上运行 PageRank，再把 metric 分数聚合到 service。 | service |
| `diagfusion` | metrics / traces / logs | 监督学习 | 深度学习 / 图神经网络 / 多模态融合 | 抽取服务级多模态异常特征并构造 DGL 服务图，用 TAG 图分类器预测根因服务概率。 | service |
| `eadro` | metrics / traces / logs | 监督学习 | 深度学习 / 图神经网络 / 多模态融合 | 用 TCN 编码时序特征、Drain/嵌入表示日志、GATv2 融合服务图结构，并对窗口预测做加权投票。 | service |
| `microdig` | traces | 无监督 | 统计方法 / 图方法 / 随机游走 | 基于 trace 调用图做 k-sigma 异常检测，抽取告警服务连通异常子图，用 PageRank/Random Walk 排序；`train` 可并行预热 pkl 预处理缓存，`evaluate` 支持 manifest/test/all 批量评估。 | service |
| `microhecl` | traces | 无监督 | 统计方法 / 图搜索 / 相关性分析 | 从异常入口 operation 出发，沿调用图分析 RT/EC 下游传播和 QPS 上游传播，再按相关性排名。 | service |
| `microrca` | traces / conclusion | 无监督 | 统计方法 / 图方法 / 随机游走 | 构造 operation 调用图和 RT/QPS/EC 序列，从 conclusion 检测告警服务，抽取异常子图，用相关性加权 personalized random walk 排名；`train` 可并行预热 pkl 缓存，`evaluate` 支持 manifest/test/all 和 1422 case 全量评估。 | service |
| `microrank` | traces | 无监督 | 统计方法 / 图方法 / 谱系故障定位 | 分别构建正常/异常 trace-operation 图，运行 PageRank，并用谱系故障定位比较两类图中的可疑度。 | service |
| `nezha` | traces / logs | 无监督 | 统计方法 / 事件模式挖掘 | 将 trace/log 编码为事件序列，比较 normal/abnormal 2-gram pattern 支持度，聚合到 service。 | service |
| `rcd` | metrics | 无监督 | 统计方法 / 因果发现 | 添加 F-node 区分正常/异常样本，用分块 Psi-PC 因果发现筛出与 F-node 强关联的可疑指标。 | service |
| `run` | metrics | 无监督 / 自监督预训练 | 深度学习 / 因果图 / PageRank | 对每个 metric 训练 DLinear 时序模型，提取影响权重构建因果 DAG，并用 personalized PageRank 排名。 | service |
| `shapleyiq` | traces | 无监督 | 博弈论 / 统计归因 | 将异常 trace 转成调用时间线，把 operation 视作合作博弈参与者，用 Shapley value 分摊异常贡献。 | service |
| `simplerca` | metrics / traces / logs | 无监督 | 规则方法 / 统计阈值 / 投票融合 | 分别用阈值、延迟和日志错误规则检测多模态异常，再按固定权重投票融合。 | service |
