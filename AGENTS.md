# AGENTS.md

本文件是本仓库内 Codex / coding agent 的项目级工作契约。除非用户在当前对话中明确覆盖，否则所有自动化研究、代码修改、评估和文档更新都必须遵守这里的规则。

## Agent skills

### Issue tracker

Issues and PRDs are tracked as local markdown files under `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

The repo uses the default five-label triage vocabulary. See `docs/agents/triage-labels.md`.

### Domain docs

This is a multi-context algorithm repository; engineering skills should use the relevant context docs for the algorithm area being changed. See `docs/agents/domain.md`.

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
- CREST 后续迭代研究默认记录在 `algorithms/crest/docs/crest_evolve/`；prompt、iteration、summary、compare、ablation 和长期决策都以该目录为准。
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
- 当前重点开发对象：CREST，canonical implementation 位于 `algorithms/crest/`，`algorithms/evidencerank/src/evidencerank/crest.py` 仅作为兼容 adapter 保留；计划最终可由 `git@github.com:Jaredddddd/Crest.git` 作为 submodule 管理。
- CREST 结构拆分计划：`algorithms/crest/docs/crest_evolve/CREST_extraction_plan.md`
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

### 自监督 causal calibration 可学习权重但暂不足以完全替代 V11

触发信号：V19 为回应固定权重的审稿质疑，尝试用无标签 incident、拓扑伪根因、通用 root perturbation profile、上下游传播负例和非负 pairwise ranking 学习 EvidenceRank feature prior。

根因 / 约束：causal pairwise objective 比 V18 的症状一致性目标更接近 RCA，但 synthetic profile 本身仍是先验假设。它容易把 availability drop、status mutation、endpoint shift 学得过强，同时压低 duration/count/self-duration/log-template 这类 delay、高扇出和入口服务 case 仍需要的信号。

正确做法：保留 `calibrate_causal_feature_weights.py` 作为无标签离线校准和论文 ablation 工具，但不要直接用 V19 individual-feature weights 替换 V11。更稳的下一步是学习 family-level calibration multiplier 或 regularizer：以 V11 的可解释语义先验为中心，用 V19 的无标签 causal objective 自动给出校准、置信区间或偏移约束。

验证方式：V19 guard 无 high-risk；full eval 1422 case、error 0。相对 V18，AC@1 从 `0.506329` 升到 `0.658931`，MRR 从 `0.684853` 升到 `0.776972`；相对 V11，AC@1 从 `0.802391` 降到 `0.658931`，产生 277 个 `regressed_from_hit1`。恢复 V11 后 full eval/perf-report 回到 `0.802391/0.875337/0.943741/0.975387`。

适用范围：所有尝试把固定 RCA 权重解释为“可由无标签数据自动形成”的实验。结论是形成权重的算法方向可行，但作为完全替代默认权重暂不可行；论文中应把它用于校准/正则化/消融，而不是声称单独的无标签学习已经达到 V11。

### 无标签 family multiplier 是比 per-feature replacement 更稳的权重形成方式

触发信号：V20 继续回应固定权重的鲁棒性/可迁移性质疑，不再让无标签目标自由学习每个 feature weight，而是以 V11 语义先验为中心，只学习 8 个 feature-family multiplier。

根因 / 约束：完全无监督 individual-feature replacement 自由度太高，会把 synthetic objective 的偏好直接变成 per-feature 权重，导致 V19 类似的过度校准。family-level multiplier 把学习自由度降到语义组，并用窄边界和 L2 正则限制偏移，能保留 V11 的稳定语义，同时给权重来源一个可复现的无标签算法。

正确做法：将在线算法表达为 `SEMANTIC_FEATURE_PRIOR * CALIBRATED_FAMILY_MULTIPLIERS`。离线校准脚本只能读取 raw incident frames 和拓扑，不能读取 label、injection、output、perf report 或 conclusion。接受前必须比较 V11/V20 和 V19/V20，而不是只看合成 pair accuracy。

验证方式：V20 narrow calibration 使用 `center_l2=4.0`、multiplier bounds `0.92..1.08`；full eval 1422 case、error 0。相对 V11，AC@1 `0.802391 -> 0.789030`，MRR `0.875337 -> 0.869097`，AC@5 `0.975387 -> 0.976793`；相对 V19，AC@1 `0.658931 -> 0.789030`。guard 无 high-risk。

适用范围：所有需要把 RCA 权重从“手工常数”转化为“可解释语义先验 + 无标签自动校准”的算法版本。该经验不证明完全无监督权重学习已经足够，而是支持把无标签学习限制在 family-level multiplier/regularizer。

目前尝试自适应权重最好的是 V13 和 V19。

### ARC reliability 只适合局部校准，不适合替代主排序先验

触发信号：EvidRank-ARC ARC12 使用 `feature_weights = (reliability > 0)`、family consensus 和 pairwise contrast 后，AC@1 停在 `0.734880`；把 reliability 改成连续权重或 rank-fusion 的离线实验反而进一步下降。

根因 / 约束：单 case 内的无标签 reliability 会高估传播、入口流量、受害者延迟和日志尖峰。即使 reliability 不是 0/1 mask，只要让它替代根因语义先验做全局排序，就会把多个传播症状一起激活并抹平根因差异。family consensus 还会继续把分数向邻近/同族症状扩散。

正确做法：ARC 主排序应保留 raw multi-modal root evidence 和 ordinal semantic priority；数值 ladder 可以由优先级顺序自动合成，但不要让 case-local reliability 自由替代主排序权重。ARC reliability 更适合构造 robust case-scaled 的局部 trace-neighbor contrast，用于解释高分受害者和邻接根因之间的错排。

验证方式：ARC13 将主排序改为 raw ordinal semantic prior，只把 reliability-active case matrix 用于最终 neighbor pairwise contrast。full eval 1422 case、error 0；相对 ARC12_CURRENT，AC@1 `0.734880 -> 0.831224`，MRR `0.839508 -> 0.893267`，AC@3 `0.936006 -> 0.947961`，AC@5 `0.971871 -> 0.975387`。guard 无 high-risk。

适用范围：所有 EvidRank-ARC、CERA 或新 RCA 算法中试图用单 incident 的无标签 reliability、agreement、concentration、rank gap 直接生成全局 feature weights 的实验。该经验不禁止 reliability，但要求把它限制为局部校准、置信度门控或 regularizer。

### CREST residual 支持必须先有置信门控

触发信号：CREST8 将弱根因 residual explainability 作为自由加性通道接入默认 `crest`，希望救回 pod failure、低可观测根因和基础设施局部故障。

根因 / 约束：未门控的 residual 会把“安静的旁观节点”和“弱可观测根因”混在一起。低传播、低日志、低 trace 的服务可能只是辅助服务、背景低流量节点或 metric drift bystander；如果只看 symptom-light + root-like metric shift，它们会获得过高 residual 支持，压过原本正确的高置信 CREST 排名。

正确做法：residual 只能作为显式 ablation 或被强置信 gate 保护的局部校准信号，不能直接 `score = A * F + S + R`。下一步若继续做 CREST residual，必须先证明候选的 trace/log silence 与异常窗口中新出现的邻域症状存在可解释关系，而不是背景低观测。

验证方式：CREST8 full eval 1422 case、error 0。`crest_residual` / residual-as-default 为 `AC@1=0.340366, MRR=0.439628, AC@3=0.447257, AC@5=0.530942`，虽然有 45 个 `improved_to_hit1`，但产生 699 个 `regressed_from_hit1`。恢复默认 no-residual 后 `crest` 回到 `0.800281/0.875326/0.944444/0.971871`。

适用范围：CREST-family 中所有试图用 residual reduction、weak-root rescue、quiet-node bonus 或 topology explainability 作为自由加性主排序通道的实验。该经验不否定 residual 思路，但要求 residual eligibility 先由无标签置信门控约束。

### CREST additive residual 即使强门控也不宜作为默认排序通道

触发信号：CREST9 在 CREST8 的负向结果后实现 `crest_gated_residual`，只允许 residual 在默认 top-2、near-tie 且 residual 双侧可比的候选之间仲裁。

根因 / 约束：top-2 和 residual comparable gate 能阻止 CREST8 的深层旁观节点灾难，但它仍把“给 challenger 加分”作为核心动作。对于 request/response protocol mutation 这类原本 CREST 已经正确的 case，邻接服务可能也具备足够 residual explainability，于是 gate 会把正确 root 翻到相邻传播服务。也就是说，门控能降低 residual 的破坏面，但没有把 residual 从“支持候选”转化为“解释/抑制 victim”的因果对比。

正确做法：不要继续通过收紧 scalar threshold、top-K window、near-tie ratio 或 residual ratio 来寻找默认提升。下一步 residual 应改成 pairwise victim suppression / contrast：只有当高可观测 victim 的传播症状能被邻接候选的更强 raw mutation evidence 解释时，才降低 victim，而不是直接给 challenger 加分。默认 `crest` 继续保持 no-residual。

验证方式：CREST9 full eval 1422 case、error 0。`crest_gated_residual` 得到 `AC@1=0.797468, MRR=0.873919, AC@3=0.944444, AC@5=0.971871`，相对 `CREST9_DEFAULT` / `crest` 的 `0.800281/0.875326/0.944444/0.971871` 净损 4 个 hit@1；compare 显示 11 个 `improved_to_hit1`、15 个 `regressed_from_hit1`。guard 无 high-risk。

适用范围：CREST-family 中所有 residual / weak-root rescue 方案，尤其是把 residual 作为 additive score、tie breaker 或 challenger bonus 的实验。

### CREST victim suppression 必须先有强 root-victim eligibility

触发信号：CREST10 将 residual bonus 改成 pairwise victim suppression：当相邻低分候选具备更强 mutation evidence、较高分服务具备更强 propagation evidence 时，只削弱 victim 分数，不给 challenger 加分。

根因 / 约束：mutation/propagation contrast 本身仍不等于 root-victim 关系。许多正确 root 的邻居也会表现出局部 mutation/propagation 差异；如果 suppression 直接作用于所有 trace-adjacent pair，就会把已正确的 protocol mutation、response mutation 和多 GT case 翻到相邻服务。相比 additive residual，suppression 的语义更接近 explain-away，但 eligibility 仍然太宽。

正确做法：不要把最终分数级 suppression 应用于所有邻接 contrast。下一步必须先得到更强的无标签 eligibility，例如 cluster-local competition、多个独立 victim symptoms 的一致可解释性、candidate 自身默认 CREST 置信保持、或 raw feature family 的 bootstrap stability。只有 eligibility 成立时才能改变 top-1；否则 residual/contrast 只能作为诊断解释输出。

验证方式：CREST10 full eval 1422 case、error 0。`crest_victim_suppression` 得到 `AC@1=0.757384, MRR=0.841618, AC@3=0.917018, AC@5=0.950070`，相对 `CREST10_DEFAULT` / `crest` 的 `0.800281/0.875326/0.944444/0.971871` 明显下降；compare 显示 24 个 `improved_to_hit1`、85 个 `regressed_from_hit1`、41 个 `rank_improved`、46 个 `rank_regressed`。guard 无 high-risk。

适用范围：CREST-family 中所有基于邻接拓扑、mutation/propagation contrast、victim explain-away 或 final-score suppression 的实验。

### CREST root-victim contrast 只适合窄门控或局部症状簇仲裁

触发信号：CREST11-CREST13 的 `A/F/S` stability fusion、family fusion 和 server protocol ownership rerank 都含有 rescue signal，但 broad rerank 大幅回归；CREST14 将动作缩小为默认 top-3 near-tie 中的 trace mutation / propagation contrast 仲裁；CREST15 进一步要求候选解释多个 incoming caller symptom surfaces。

根因 / 约束：root-like raw signal 本身仍可能出现在 symptom surface、入口服务或相邻传播服务上。只有当候选已经接近默认 winner，且候选的 trace mutation 明显更强、trace propagation 明显更弱，或能解释多个 incoming caller 的高 propagation 症状时，这种 contrast 才足以安全改变 top-1。否则它会退化成 family rerank、protocol symptom rerank 或 two-hop topology centrality。

正确做法：把 root-victim contrast 用作严格 eligibility predicate，而不是自由加分、全局 rerank 或 broad suppression。默认安全形态是：候选位于当前 top-k、分数 near-tie、mutation/propagation 角色强对比、只做单次仲裁；若扩大范围，必须扩大“解释了多少独立邻域症状”，不要放宽为全局 feature weight 或 two-hop ranker。

验证方式：CREST15 `crest_cluster_arbitration` full eval 1422 case、error 0；相对旧 default `crest`，AC@1 `0.800281 -> 0.812940`，MRR `0.875326 -> 0.882065`，AC@3 `0.944444 -> 0.945148`，AC@5 保持 `0.971871`；compare 显示 18 个 `improved_to_hit1`、0 个 `regressed_from_hit1`、18 个 `rank_improved`、0 个 `rank_regressed`。该机制已提升为默认 `crest`，但仍未达到 `AC@1 >= 0.85`。

适用范围：CREST-family 中所有基于 role contrast、trace mutation ownership、protocol mutation rescue、cluster-local explain-away、incoming caller symptom cluster 或 top-k arbitration 的实验。

### CREST protocol/path drift 必须绑定结构 fan-in 与传播上限

触发信号：CREST13/CREST16 的 server protocol drift 作为 scalar gate 会把入口服务、下游症状面和高可观测传播节点推到 top-1；CREST17 重新审视 accepted-default top-3 miss 后发现，只有当 path/method drift 与更广 incoming caller fan-in 同时出现时才足够安全。

根因 / 约束：server span / method distribution drift 是真实异常信号，但它不天然区分 root-owned request mutation 与 symptom-surface protocol drift。入口或受害服务也会因为上游异常、重试、流量改道或错误路径集中而出现强 method/span TV。若只按 protocol drift、observability 或两者组合仲裁，AC@1 可涨但会产生大量 `regressed_from_hit1`。

正确做法：protocol/path drift 只能作为近邻仲裁的 eligibility，而不是全局 rerank。CREST17 的安全形态是：候选位于当前 top-3 near-tie；server method/span TV 高于当前 winner；observability volume 高于 winner；incoming caller 数至少比 winner 多 1；trace propagation burden 不超过 winner 的 1.4x。动作仍然只是把一个 near-tie challenger bump 到 winner 上方，不给全局 bonus、不读取 label/injection/output/perf/conclusion、不使用服务名或 fault 名。

验证方式：CREST17 `crest_path_fanin_arbitration` 和 promoted default `crest` full eval 均为 1422 case、error 0。相对 `CREST15_ACCEPTED`，AC@1 `0.812940 -> 0.825598`，MRR `0.882065 -> 0.888980`，AC@3/AC@5 保持 `0.945148/0.971871`；compare 显示 18 个 `improved_to_hit1`、0 个 `regressed_from_hit1`、1 个非 top-1 `rank_regressed`。guard 无 high-risk。运行时成本从约 `9.21s` 上升到约 `11.74s`。

适用范围：CREST-family 中所有 request path、span name、HTTP method/status、server protocol、endpoint ownership、caller-cluster path consistency 或 protocol mutation rescue 实验。未来若继续扩展该方向，应增强结构解释性或缓存 raw trace TV，而不要放宽为 scalar protocol score。

### PV-CREST 动态 evidence selection 有效但接近无监督可辨识性上限

触发信号：AIOps25 service-level 的目标要求 `crest` 接近 `AC@1 >= 0.70`，同时 RCABench full multimodal 不下降；PV_CREST1-PV_CREST3 尝试将 CREST 改造成 DyMo-style inference-time dynamic evidence selection。

根因 / 约束：两个数据集的可观测性语义冲突很强。RCABench 经常奖励 trace-root-aligned protocol / topology 证据；AIOps25 service-level 中 trace 又常常只覆盖入口或传播面，真正 service root 更可能通过 metric/log/resource provenance 出现。单 incident、label-free 的选择器很难区分“trace dominance 是真实 root”还是“trace dominance 是 exposure surface”，也很难区分“metric/log ownership 是 root-local”还是“metric/log ownership 是传播受害者”。oracle union 显示，当前 `crest` 与 `crest_metric_log` 的 AIOps25 hit@1 union 只有 `0.673913`，而引入另一套 metric-log 排序的 oracle 才能略过 `0.70`，这意味着无监督 selector 几乎必须接近 oracle 才能达标。

正确做法：保留 PV_CREST2 的动态 evidence selection 作为当前最稳的 safe gain：只在 incident-local masked-root view 的无标签质量优于 base view 时切换，不做 dataset/service/fault 分支，不全局降低 trace。PV_CREST3 的 service-level representativeness 可作为 provenance atom 的局部校准，帮助 MRR/AC@3/AC@5，但不要声称它解决 top-1。后续若要继续逼近 `0.70`，不要再放宽 broad trace demotion 或 metric+log fallback；需要新增无标签信息源，例如历史 incident 原型、服务角色稳定性、重复事件下的 self-supervised calibration，或更细的 resource/provenance atom。

验证方式：PV_CREST2 full eval：AIOps25 `AC@1=0.526087, MRR=0.662711, AC@3=0.756522, AC@5=0.826087`，RCABench `0.800281/0.875326/0.944444/0.971871` 不变。PV_CREST3 full eval：AIOps25 `AC@1=0.526087, MRR=0.672613, AC@3=0.782609, AC@5=0.865217`，RCABench 仍不变。PV_CREST1 broad partial-view override 虽提升 AIOps25 到 `0.430435`，但 RCABench 降到 `0.492264`，证明 broad role override 不安全。

适用范围：所有 AIOps25 service-level 与 RCABench 同时优化的 CREST / PV-CREST 实验，尤其是动态模态选择、trace exposure suppression、metric/log/provenance root rescue、resource ownership arbitration，以及试图用纯 incident-local 无监督机制同时获得两个数据集高 AC@1 的方案。
