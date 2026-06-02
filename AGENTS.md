# AGENTS.md

本文件是本仓库内 Codex / coding agent 的项目级工作契约。除非用户在当前对话中明确覆盖，否则所有自动化研究、代码修改、评估和文档更新都必须遵守这里的规则。

## 基础约束

- 除非用户明确要求，不要使用 SuperPower 相关 skill。
- 不要运行破坏性命令，例如 `git reset --hard`、`git checkout -- <path>`、不受控的 `rm -rf`。
- 不要使用非 Git 工具操作 `.git`。
- 不要终止非当前任务启动的进程。
- 不要用不可信输入拼接 shell 命令、SQL 或文件路径；数据库访问必须使用参数化查询。
- 优先局部修改和最小充分实现，避免把研究任务扩张成无关重构。
- 如果任务复杂度上升，升级为显式研究流程；如果任务已经收敛为局部改动，降级为局部修复流程。

## 文档维护

- 计划、目标、约束、关键决策、经验教训、步骤或进度变化时，必须同步更新项目内 `docs/`。
- EvidenceRank 迭代研究默认记录在 `docs/EvidRank_evolve/`。
- Vibe Research 主页面为 `VibeResearchTools/VibeResearch.md`。所有 Vibe Research 相关入口信息、启动 prompt、长期决策、索引和导航都可以写入该文件。
- `docs/EvidRank_evolve/` 中的详细文档必须能在 `VibeResearchTools/VibeResearch.md` 的 index 中被发现。生成或修改研究文档后运行：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

- 每轮算法优化至少沉淀一篇迭代记录，建议命名为 `V<N>_iteration.md` 或 `V<N>_summary.md`。
- 反复证明有价值的经验应沉淀回本文件或 `CLAUDE.md`。经验模板最小包含：标题、触发信号、根因 / 约束、正确做法、验证方式、适用范围。

## 当前研究对象

- 目标算法：`algorithms/evidencerank`
- 主实现：`algorithms/evidencerank/src/evidencerank/algorithm.py`
- 运行命令：

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 32
```

- 评估命令：

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

- Parquet 转 CSV：

```bash
uv run --package evidencerank python scripts/parquet_to_csv.py evidencerank
```

- RCABench label：

```text
data/rcabench-platform-v2/meta/rcabench-csv/labels.csv
```

- 单 case ground truth / 注入信息：

```text
data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json
```

- 当前算法输出：

```text
output/rcabench-platform-v2/data/rcabench/<datapack>/evidencerank/
```

## 研究目标

使用 RCABench 当前数据集对 EvidenceRank 做迭代优化，提升 `AC@1`、`MRR`、`AC@3`、`AC@5` 等指标，同时保持算法跨系统通用性。

核心目标不是“记住 RCABench”，而是从 false case 中归纳可迁移 RCA 机制，例如：

- 多模态证据的可靠性估计；
- 指标、trace、log 的鲁棒归一化；
- 拓扑上的异常传播与抑制；
- 上游/下游故障影响的方向性建模；
- 异常强度、异常稀疏度和证据一致性的通用组合；
- 多 ground truth case 中对基础设施组件和业务服务共同异常的排序策略。

## 严禁的数据集特化

以下行为禁止进入算法实现：

- 硬编码 datapack 名称，例如 `ts0-mysql-container-kill-9t6n24`。
- 硬编码 label、case id、随机后缀、RCABench 专属 split。
- 在算法运行路径中读取 `labels.csv`、`injection.json`、评估输出、历史排行榜或任何 ground truth。
- 不要读取 `conclusion.parquet` 作为算法实现或离线 false case 证据。该文件属于已加工诊断结论；只允许研究其生成思路，并从 raw traces 反向构造通用端点异常信号。
- 针对具体服务名写分支，例如 `if service == "mysql"`、`if name.startswith("ts-order")`。
- 针对具体故障名写分支，例如 `if "container-kill" in datapack`。
- 为了提升当前数据集分数而堆叠不可解释的 if/else、查表、黑名单、白名单。

允许在离线研究工具和文档中使用 label，只能用于分析错误模式、生成报告、比较版本和提出通用假设。`conclusion.parquet` 不得被读取为证据或特征；若研究其生成机制，只能把思路转化为 raw traces 上的通用信号。任何进入 `algorithms/evidencerank` 的逻辑必须能解释为跨微服务系统通用的 RCA 方法。

## 推荐迭代流程

每一轮 EvidenceRank 优化按以下顺序执行：

1. 明确版本号，例如 `V1`、`V2`、`V3`。不要复用旧版本号。
2. 在修改前快照当前输出：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
```

3. 生成当前 false case 报告：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
```

4. 用报告抽样查看 case 证据，而不是直接猜：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py case --datapack <case-name> --source V1 --algorithm evidencerank --dataset rcabench --top-k 20
```

5. 在 `docs/EvidRank_evolve/` 记录假设、证据和计划：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V2 --hypothesis "一句话描述本轮通用算法假设"
```

6. 修改算法。优先改通用 feature、score、normalization、rank aggregation、topology propagation，不要改 dataset adapter 或评估代码。
7. 运行反过拟合守卫：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
```

8. 运行必要的 smoke test 或 full eval。full eval 会覆盖当前 `output/.../evidencerank`，因此运行前必须已经做过快照。
9. 评估后把新输出快照为新版本，例如：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V2 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V2 --source V2 --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V1 --new V2 --algorithm evidencerank --dataset rcabench
```

10. 在迭代文档中写清楚：本轮假设、代码变化、指标变化、改善 case、退化 case、是否接受、下一步。

## VibeResearchTools 工具说明

工具实现放在 `VibeResearchTools/`。默认通过下面形式运行：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py <subcommand> ...
```

### `snapshot`

功能：把当前算法输出复制到不可复用版本目录，避免 full eval 的 `--clear` 覆盖历史结果。

默认输出：

```text
output/rcabench-platform-v2/evolve_snapshots/<VERSION>/
```

包含：

- `data/<dataset>/<datapack>/<algorithm>/output.parquet`
- `data/<dataset>/<datapack>/<algorithm>/perf.parquet`
- `.finished` 等算法输出侧文件
- `manifest.json`，记录版本、算法、数据集、git commit、dirty 状态和总体指标

### `summarize`

功能：读取某个版本或当前输出，结合 `labels.csv` 生成 false case 报告。

输出：

- `output/rcabench-platform-v2/evolve_reports/<VERSION>/all_cases.csv`
- `output/rcabench-platform-v2/evolve_reports/<VERSION>/false_cases.csv`
- `output/rcabench-platform-v2/evolve_reports/<VERSION>/group_summary.csv`
- `docs/EvidRank_evolve/<VERSION>_summary.md`

报告重点看：

- Top-1 miss；
- Top-5 miss；
- 按 fault type、case service、GT service 聚合的退化模式；
- rank 很深或缺失的 hard cases；
- 可迁移算法假设，而不是 case-specific patch。

### `compare`

功能：比较两个版本的输出，定位改善和退化。

示例：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V1 --new V2 --algorithm evidencerank --dataset rcabench
```

输出：

- `output/rcabench-platform-v2/evolve_reports/compare_<OLD>_vs_<NEW>/case_deltas.csv`
- `docs/EvidRank_evolve/compare_<OLD>_vs_<NEW>.md`

必须重点阅读：

- `regressed_from_hit1`
- `improved_to_hit1`
- `rank_regressed`
- `rank_improved`

如果总体提升来自少量 case，而大类明显退化，不应直接接受。

### `case`

功能：查看一个 datapack 的 GT、预测 top-k、注入信息和输入数据概况，用于人工归因。输入数据概况会跳过 `conclusion.parquet`。

示例：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py case --datapack ts0-mysql-container-kill-9t6n24 --source V1 --algorithm evidencerank --dataset rcabench --top-k 20
```

注意：`case` 可以读取 `injection.json`，但这只允许用于离线分析和文档。算法实现不能读取它。`case` 不读取 `conclusion.parquet`；端点类想法必须从 raw traces 重建。

### `guard`

功能：扫描 EvidenceRank 源码中的高风险过拟合信号。

会提示：

- datapack id；
- label / injection / ground truth 读取；
- 读取 `conclusion.parquet` 作为证据或特征；
- service name 字面量；
- dataset name 字面量。

`guard` 不能证明算法一定通用，但它能拦截明显泄漏和硬编码。每次提交算法改动前必须运行。

### `new-note`

功能：为下一轮创建迭代记录模板，强制先写假设再改代码。

示例：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V3 --hypothesis "拓扑邻域的一致异常比单点异常更能区分根因与传播影响"
```

## 推荐分析 prompt

### LLM 启动 Prompt

完整启动 prompt 放在 `VibeResearchTools/VibeResearch.md` 的 `LLM Launch Prompt` 小节。启动新的分析型 LLM / coding agent 时，优先复制该 prompt，并要求它先阅读：

- `AGENTS.md`
- `VibeResearchTools/VibeResearch.md`
- `results.md`
- `algorithms/evidencerank/src/evidencerank/algorithm.py`
- 当前版本的 `docs/EvidRank_evolve/<VERSION>_summary.md`

启动 prompt 的核心要求是：只允许用 label / injection 做离线 false case 分析，不允许把它们读入算法；任何算法改动都必须能解释为跨微服务系统通用的 RCA 机制。

额外要求：验证算法需要较长时间是完全可以接受的。目标是通过最终 ACC 提升算法质量，而非缩短开发验证周期。不要因为全量 eval 运行慢就中止实验、跳过验证或改用已有输出做"快速分析"——这种做法可能导致真正能涨点的优化方向没有得到充分验证。例如，以下行为是被禁止的："这次离线脚本是顺序读全量 parquet，速度太慢，不适合拿来做快速研究。我会停掉这个当前启动的实验，改用已有 V2 输出和更小的抽样/并行分析来收敛候选信号。"

### False Case 研究 Prompt

```text
你是微服务 RCA 算法研究员。请根据 EvidenceRank 当前算法逻辑、false case 排名、GT 和输入数据概况，找出可以跨系统迁移的失败模式。

禁止提出 hardcode case/service/fault 的方案。
每个改进建议必须包含：
1. 失败机制；
2. 当前特征或 scoring 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式。
```

### 算法修改 Prompt

```text
请只修改 algorithms/evidencerank 中与通用 RCA 排序有关的逻辑。

要求：
- 不读取 label、injection、output、result；
- 不硬编码数据集、datapack、服务名、故障名；
- 保持 Algorithm 接口兼容；
- 保留多模态 variant 的可运行性；
- 修改前后都能通过 VibeResearchTools guard；
- 在 docs/EvidRank_evolve/<VERSION>_iteration.md 记录假设、改动和验证。
```

### 回归分析 Prompt

```text
请比较 V<OLD> 和 V<NEW> 的 case_deltas.csv。

输出：
1. 总体指标变化；
2. 改善最多的 fault/service 模式；
3. 退化最多的 fault/service 模式；
4. 本轮假设是否被证据支持；
5. 是否接受该版本；
6. 下一轮只做一个最小、通用的改动建议。
```

## 可考虑的通用优化方向

- Robust scaling：用分位数、MAD、winsorization 或 per-case relative rank 降低极端 row count 对 score 的支配。
- Modality confidence：根据某一模态是否有足够样本、是否与其他模态一致来调整权重。
- Evidence concentration：根因通常在多个异常信号上集中，传播节点可能是单一大流量异常；可建模证据分布熵或 top feature concentration。
- Topology-aware rerank：用 trace edge 方向区分上游触发、下游受害和中心节点高流量假阳性。
- Neighbor contrast：比较服务自身异常与邻居异常，识别“自身突变强于邻域”的节点。
- Multi-GT handling：RCABench 有些 case 同时标注基础设施组件和业务服务；排序策略应能保留共同根因，而不是只偏向数据库或业务服务。
- Rank fusion：用 feature family 的名次融合替代原始值求和，降低不同量纲对结果的影响。

## 接受标准

一次优化被接受前至少满足：

- `guard` 无高风险告警；
- full eval 可完成且 `error == 0`；
- `AC@1` 或 `MRR` 至少一个提升；
- `AC@3`、`AC@5` 没有不可解释的大幅退化；
- 退化 case 已在文档中列出并解释；
- 文档包含复现实验命令和版本号；
- 当前输出已 snapshot，历史输出未被覆盖。

如果指标下降但发现了清晰失败机制，也可以保留为研究记录，但不要把算法改动作为默认版本接受。

## 经验沉淀

### 尝试 case by case 的无监督自适应权重

完成了这一轮“去固定权重 / 无监督自适应权重”的实验闭环。

核心结论：我实现并完整评估了 V13-V17 多个无标签自学习权重方案，但都没有达到可接受的鲁棒性-性能折中。最好的无固定权重版本是 V13，`AC@1=0.679325, MRR=0.804981`，低于你希望的约 `0.75` 容忍线；V17 进一步降到 `AC@1=0.563291`。因此这些版本都已记录为负向实验，没有接受进默认算法。

当前默认实现已恢复到已接受的 V11。恢复后重新跑了 full eval 和 perf-report，主行指标回到：

```text
total=1422, error=0
AC@1=0.802391
MRR=0.875337
AC@3=0.943741
AC@5=0.975387
runtime.avg=9.753871s
```

guard 已通过：无 high-risk 过拟合告警；`algorithm.py` 没有残留实验 diff。VibeResearch 索引也已刷新。

这轮研究沉淀在V13-V17：
- [V13_iteration.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V13_iteration.md)
- [V17_iteration.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V17_iteration.md)
- [VibeResearch.md](/home/ljw/paper/aegis/rca-algo-contrib/VibeResearchTools/VibeResearch.md)

对论文/审稿的建议结论是：单 case 内部的完全无监督权重学习目前不够稳，容易把传播节点、入口流量或局部日志尖峰当成根因。更 defensible 的下一步不是继续手调 per-case 权重，而是做“无标签离线全局校准”：用大量未标注 incident 的特征分布、跨模态一致性和拓扑稳定性学习全局 prior，再在单 case 内做轻量自适应。这样可以避免“RCABench label 拟合”的质疑，同时保留 V11 这类 domain prior 的稳定性。

工作区目前留下了研究文档、compare 文档、`AGENTS.md` 经验补充和评估输出 parquet；默认算法源码没有被改成被拒绝版本。

### 无标签离线全局校准不能只优化症状一致性

触发信号：为了回应固定 feature weight 可能被质疑为数据集特化，V18 尝试用无标签 incident corpus 的 feature 覆盖、集中度、top gap、逆尺度和跨模态一致性生成全局 prior。

根因 / 约束：无标签统计能发现“哪些症状尖锐且经常和其他症状共现”，但这不等价于“哪些症状更接近根因”。日志错误率和 trace duration 这类传播/受害者症状可能同时具备高集中度和高一致性；status/endpoint 这类协议级 mutation 信号虽然数值尺度较小，却更有因果特异性。朴素全局校准会高估前者、低估后者。

正确做法：保留 `calibrate_feature_weights.py` 这类离线工具作为论文中的无标签 prior 生成和诊断流程，但不要直接用“集中度 + 一致性 + 逆尺度”替换 V11 默认权重。下一步若继续做无标签校准，应加入 causality-aware 约束，例如拓扑方向、root-vs-victim neighbor contrast、log-only cap、status/endpoint 支持门控、family-level 而非 individual-feature 的先验学习。

验证方式：V18 generated prior 完整跑了 guard、full eval、perf-report、snapshot、summary、V11/V18 compare、V17/V18 compare。结果 AC@1 从 V11 的 `0.802391` 降到 `0.506329`，MRR 从 `0.875337` 降到 `0.684853`，并产生 467 个 `regressed_from_hit1`，因此拒绝；恢复 V11 后重新 full eval，AC@1/MRR/AC@3/AC@5 回到 `0.802391/0.875337/0.943741/0.975387`。

适用范围：所有试图用无标签统计、self-supervised agreement 或 global calibration 替代 RCA feature prior 的实验。该经验不禁止无标签校准，但要求 calibration objective 显式区分根因特异信号和传播症状。
