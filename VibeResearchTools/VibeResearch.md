# Vibe Research

This is the main page for EvidenceRank vibe research. Keep long-lived research context, launch prompts, decisions, and links here. Detailed iteration notes can stay in `docs/EvidRank_evolve/`; EvidRank-ARC notes live in `docs/EvidRank-ARC-Evolve/`.

## Research Entry

- Target algorithm: `algorithms/evidencerank`
- Default dataset for current evolution: `rcabench`
- Iteration docs: `docs/EvidRank_evolve/`
- EvidRank-ARC docs: `docs/EvidRank-ARC-Evolve/`
- Tool CLI: `VibeResearchTools/evidrank_lab.py`
- Labels for offline analysis only: `data/rcabench-platform-v2/meta/rcabench-csv/labels.csv`
- Case metadata for offline analysis only: `data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json`
- Do not read `data/rcabench-platform-v2/data/rcabench/<datapack>/conclusion.parquet` in algorithm code or false-case evidence. It is acceptable to study, at a design level, how comparable endpoint symptoms could be reconstructed from raw traces.

## LLM Launch Prompt

Use the following prompt to start an analysis-focused LLM or coding agent for EvidenceRank evolution.

### 第一次迭代 evolve：V1 到 V4 的 prompt

```text
你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作，目标是基于 RCABench 当前 false cases 迭代优化 EvidenceRank，但必须保持算法跨系统通用，严禁把 RCABench label、case id、服务名或故障名写进算法逻辑。

背景：
- EvidenceRank 是当前研究算法，路径为 algorithms/evidencerank。
- 主实现为 algorithms/evidencerank/src/evidencerank/algorithm.py。
- 当前评估结果已在 results.md 和 output/rcabench-platform-v2 中。
- RCABench label 位于 data/rcabench-platform-v2/meta/rcabench-csv/labels.csv。
- 单 case 注入和 GT 元信息位于 data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json。
- label 和 injection 只能用于离线分析、报告和验证，不能被 algorithms/evidencerank 的运行逻辑读取。

总体目标：
从 EvidenceRank 的 false cases 中归纳可迁移的 RCA 机制，提出并实现最小充分的通用算法改动，提升 AC@1 / MRR / AC@3 / AC@5，同时控制退化。

强约束：
1. 禁止硬编码 datapack、case id、随机后缀、服务名、故障名、dataset split。
2. 禁止在算法实现中读取 labels.csv、injection.json、output、perf report 或任何 ground truth。
3. 禁止为了当前数据集堆叠不可解释的 if/else、黑名单、白名单或查表逻辑。
4. 任何进入算法的改动必须能解释为跨微服务系统通用的 RCA 信号、归一化、证据融合或拓扑推理。
5. 每轮实验必须保留版本化输出，不覆盖旧结果。
6. 所有研究计划、假设、结果、经验和索引都要同步到文档；Vibe Research 主页面是 VibeResearchTools/VibeResearch.md，详细迭代文档在 docs/EvidRank_evolve/。

推荐工作流：
1. 先阅读 AGENTS.md、VibeResearchTools/VibeResearch.md、results.md、algorithms/evidencerank/src/evidencerank/algorithm.py。
2. 如果还没有 baseline snapshot，先运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
3. 研究 false cases：
   - 阅读 docs/EvidRank_evolve/<VERSION>_summary.md。
   - 对代表性 case 运行 VibeResearchTools/evidrank_lab.py case。
   - 聚合 fault_type、case_service、GT rank、top5、输入数据概况，寻找通用失败机制。
4. 在改代码前创建迭代笔记：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V<N> --hypothesis "<一句话通用算法假设>"
5. 只修改 algorithms/evidencerank 中与通用 RCA 排序有关的逻辑，例如：
   - robust scaling / rank fusion；
   - modality confidence；
   - evidence concentration；
   - topology-aware rerank；
   - neighbor contrast；
   - 多 ground truth 排序友好性。
6. 修改后运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
   uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
   uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
7. 评估后保存新版本：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V<N> --source V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V<N-1> --new V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index

每个改进建议必须输出：
1. 失败机制；
2. 当前 EvidenceRank 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式；
8. 是否接受该版本以及理由。

接受标准：
- VibeResearchTools guard 无 high-risk 告警；
- full eval error == 0；
- AC@1 或 MRR 至少一个提升；
- AC@3 / AC@5 没有不可解释的大幅退化；
- improved / regressed case 已在 docs/EvidRank_evolve 中记录；
- VibeResearchTools/VibeResearch.md 索引已刷新。

现在初始evidencerank的结果如下，我希望最终evidencerank的AC@1能至少达到 65-70%


┌───────────────────────────┬───────┬───────┬─────────────────────┬──────────┬────────────┬────────────┬────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ algorithm                 ┆ total ┆ error ┆ runtime.seconds:avg ┆      MRR ┆ AC@1.count ┆ AC@3.count ┆ AC@5.count ┆     AC@1 ┆     AC@3 ┆     AC@5 ┆    Avg@3 ┆    Avg@5 │
│ evidencerank              ┆ 1,422 ┆     0 ┆            8.669303 ┆ 0.679202 ┆      754.0 ┆    1,107.0 ┆    1,248.0 ┆ 0.530239 ┆ 0.778481 ┆ 0.877637 ┆ 0.673465 ┆ 0.746835 │
│ microrca                  ┆ 1,422 ┆     0 ┆           24.493223 ┆ 0.674339 ┆      750.0 ┆      853.0 ┆    1,011.0 ┆ 0.527426 ┆ 0.599859 ┆  0.71097 ┆ 0.566104 ┆ 0.619831 │

```




### 第二次迭代 evolve：V4到 V5 时的 prompt

```text
你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作，目标是基于 RCABench 当前 false cases 迭代优化 EvidenceRank，但必须保持算法跨系统通用，严禁把 RCABench label、case id、服务名或故障名写进算法逻辑。

背景：
- EvidenceRank 是当前研究算法，路径为 algorithms/evidencerank。
- 主实现为 algorithms/evidencerank/src/evidencerank/algorithm.py。
- 当前评估结果已在 results.md 和 output/rcabench-platform-v2 中。
- RCABench label 位于 data/rcabench-platform-v2/meta/rcabench-csv/labels.csv。
- 单 case 注入和 GT 元信息位于 data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json。
- label 和 injection 只能用于离线分析、报告和验证，不能被 algorithms/evidencerank 的运行逻辑读取。
- conclusion.parquet 属于已加工诊断结论，不要用于算法实现，也不要用于离线 false case 归因；可以研究其生成思路，并只从 raw traces 反向构造通用端点异常信号。

总体目标：
从 EvidenceRank 的 false cases 中归纳可迁移的 RCA 机制，提出并实现最小充分的通用算法改动，提升 AC@1 / MRR / AC@3 / AC@5，同时控制退化。

强约束：
1. 禁止硬编码 datapack、case id、随机后缀、服务名、故障名、dataset split。
2. 禁止在算法实现中读取 labels.csv、injection.json、output、perf report 或任何 ground truth。
3. 禁止读取 conclusion.parquet 参与算法实现或离线 false case 证据；允许研究生成思路，并只从 raw traces 构造可迁移信号。
4. 禁止为了当前数据集堆叠不可解释的 if/else、黑名单、白名单或查表逻辑。
5. 任何进入算法的改动必须能解释为跨微服务系统通用的 RCA 信号、归一化、证据融合或拓扑推理。
6. 每轮实验必须保留版本化输出，不覆盖旧结果。
7. 所有研究计划、假设、结果、经验和索引都要同步到文档；Vibe Research 主页面是 VibeResearchTools/VibeResearch.md，详细迭代文档在 docs/EvidRank_evolve/。
8. 验证算法需要较长时间是完全可以接受的。目标是通过最终 ACC 提升算法质量，而非缩短开发验证周期。不要因为全量 eval 运行慢就中止实验、跳过验证或改用已有输出做"快速分析"——这种做法可能导致真正能涨点的优化方向没有得到充分验证。例如，以下行为是被禁止的："这次离线脚本是顺序读全量 parquet，速度太慢，不适合拿来做快速研究。我会停掉这个当前启动的实验，改用已有 V2 输出和更小的抽样/并行分析来收敛候选信号。"

推荐工作流：
1. 先阅读 AGENTS.md、VibeResearchTools/VibeResearch.md、results.md、algorithms/evidencerank/src/evidencerank/algorithm.py。
2. 如果还没有 baseline snapshot，先运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
3. 研究 false cases：
   - 阅读 docs/EvidRank_evolve/<VERSION>_summary.md。
   - 对代表性 case 运行 VibeResearchTools/evidrank_lab.py case。
   - 聚合 fault_type、case_service、GT rank、top5、输入数据概况，寻找通用失败机制；不要读取 conclusion.parquet，可研究如何从 raw traces 构造类似端点异常信号。
4. 在改代码前创建迭代笔记：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V<N> --hypothesis "<一句话通用算法假设>"
5. 只修改 algorithms/evidencerank 中与通用 RCA 排序有关的逻辑，例如：
   - robust scaling / rank fusion；
   - modality confidence；
   - evidence concentration；
   - topology-aware rerank；
   - neighbor contrast；
   - 多 ground truth 排序友好性。
6. 修改后运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
   uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
   uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
7. 评估后保存新版本：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V<N> --source V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V<N-1> --new V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index

每个改进建议必须输出：
1. 失败机制；
2. 当前 EvidenceRank 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式；
8. 是否接受该版本以及理由。

接受标准：
- VibeResearchTools guard 无 high-risk 告警；
- full eval error == 0；
- AC@1 或 MRR 至少一个提升；
- AC@3 / AC@5 没有不可解释的大幅退化；
- improved / regressed case 已在 docs/EvidRank_evolve 中记录；
- VibeResearchTools/VibeResearch.md 索引已刷新。

现在经过之前优化到 V4 的结果如下，我希望最终evidencerank的AC@1能至少达到 65-70%

│ algorithm                 ┆ total ┆ error ┆ runtime.seconds:avg ┆      MRR ┆ AC@1.count ┆ AC@3.count ┆ AC@5.count ┆     AC@1 ┆     AC@3 ┆     AC@5 ┆    Avg@3 ┆    Avg@5 │
│ evidencerank              ┆ 1,422 ┆     0 ┆            7.365646 ┆ 0.706323 ┆      813.0 ┆    1,125.0 ┆    1,264.0 ┆  0.57173 ┆ 0.791139 ┆ 0.888889 ┆ 0.696906 ┆ 0.764135 │
│ microrca                  ┆ 1,422 ┆     0 ┆           24.493223 ┆ 0.609371 ┆      750.0 ┆      853.0 ┆    1,011.0 ┆ 0.527426 ┆ 0.599859 ┆  0.71097 ┆ 0.566104 ┆ 0.619831 │

我的小建议：其实可以集各家之所长，来把优点融合到 EvidRank 中，例如分析为什么现在 MircoHECL对的都在 AC@1 ，从而看有什么事可以应用到 EvidRank的

V4 之后给出的建议：

下一步最有希望继续冲 AC@1 的方向是：从 raw traces/logs 重构 endpoint-level 的 path/method/status/body/error shift 信号，做 confidence gating 和拓扑抑制；仍然不直接使用 conclusion.parquet。

已完成一轮到 V4 的迭代，当前接受版本是 **V4**。

核心代码改动在 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:57)：

- V2: 非有限/缺失特征按“该特征无证据”处理，避免一个 NaN 抹掉整个服务分数。
- V3: 加入通用 feature-family weights，降低 metric/log 量纲支配，提高 row coverage 支持。
- V4: 不再把 topology degree 作为正/负硬证据，改成 trace 方向上的 `5%` 上游调用方上下文传递，见 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:340) 和 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:359)。

没有在算法里读取 `labels.csv`、`injection.json`、`output`、perf report 或 `conclusion.parquet`；也没有加入 datapack/service/fault hardcode。`rg` 检查算法文件没有 `conclusion/labels/injection/ground/datapack` 命中。

**指标进展**

| version | AC@1 | MRR | AC@3 | AC@5 | error |
| --- | ---: | ---: | ---: | ---: | ---: |
| V1 baseline | 0.530239 | 0.679202 | 0.778481 | 0.877637 | 0 |
| V2 | 0.531646 | 0.684448 | 0.786920 | 0.886779 | 0 |
| V3 | 0.559072 | 0.698007 | 0.789030 | 0.888186 | 0 |
| V4 accepted | 0.571730 | 0.706323 | 0.791139 | 0.888889 | 0 |

V4 相比 V1：AC@1 从 `754/1422` 到 `813/1422`，净增 59 个 Hit@1。还没达到你希望的 65-70%，但已经是一个干净、可解释、全指标正向的版本。

**验证完成**

- `python -m compileall algorithms/evidencerank/src/evidencerank`
- `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard`
  - 无 high-risk，仅有原有 medium 提示。
- full eval：1422/1422，`error=0`
- snapshot/summary/compare 已生成：
  - [V4_iteration.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V4_iteration.md)
  - [V4_summary.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V4_summary.md)
  - [compare_V3_vs_V4.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/compare_V3_vs_V4.md)
- VibeResearch 索引已刷新。

```

### 第三次迭代：


```text
你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作，目标是基于 RCABench 当前 false cases 迭代优化 EvidenceRank，但必须保持算法跨系统通用，严禁把 RCABench label、case id、服务名或故障名写进算法逻辑。

背景：
- EvidenceRank 是当前研究算法，路径为 algorithms/evidencerank。
- 主实现为 algorithms/evidencerank/src/evidencerank/algorithm.py。
- 当前评估结果已在 results.md 和 output/rcabench-platform-v2 中。
- RCABench label 位于 data/rcabench-platform-v2/meta/rcabench-csv/labels.csv。
- 单 case 注入和 GT 元信息位于 data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json。
- label 和 injection 只能用于离线分析、报告和验证，不能被 algorithms/evidencerank 的运行逻辑读取。
- conclusion.parquet 属于已加工诊断结论，不要用于算法实现，也不要用于离线 false case 归因；可以研究其生成思路，并只从 raw traces 反向构造通用端点异常信号。

总体目标：
从 EvidenceRank 的 false cases 中归纳可迁移的 RCA 机制，提出并实现最小充分的通用算法改动，提升 AC@1 / MRR / AC@3 / AC@5，同时控制退化。

强约束：
1. 禁止硬编码 datapack、case id、随机后缀、服务名、故障名、dataset split。
2. 禁止在算法实现中读取 labels.csv、injection.json、output、perf report 或任何 ground truth。
3. 禁止读取 conclusion.parquet 参与算法实现或离线 false case 证据；允许研究生成思路，并只从 raw traces 构造可迁移信号。
4. 禁止为了当前数据集堆叠不可解释的 if/else、黑名单、白名单或查表逻辑。
5. 任何进入算法的改动必须能解释为跨微服务系统通用的 RCA 信号、归一化、证据融合或拓扑推理。
6. 每轮实验必须保留版本化输出，不覆盖旧结果。
7. 所有研究计划、假设、结果、经验和索引都要同步到文档；Vibe Research 主页面是 VibeResearchTools/VibeResearch.md，详细迭代文档在 docs/EvidRank_evolve/。
8. 验证算法需要较长时间是完全可以接受的。目标是通过最终 ACC 提升算法质量，而非缩短开发验证周期。不要因为全量 eval 运行慢就中止实验、跳过验证或改用已有输出做"快速分析"——这种做法可能导致真正能涨点的优化方向没有得到充分验证。例如，以下行为是被禁止的："这次离线脚本是顺序读全量 parquet，速度太慢，不适合拿来做快速研究。我会停掉这个当前启动的实验，改用已有 V2 输出和更小的抽样/并行分析来收敛候选信号。"

推荐工作流：
1. 先阅读 AGENTS.md、VibeResearchTools/VibeResearch.md、results.md、algorithms/evidencerank/src/evidencerank/algorithm.py。
2. 如果还没有 baseline snapshot，先运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
3. 研究 false cases：
   - 阅读 docs/EvidRank_evolve/<VERSION>_summary.md。
   - 对代表性 case 运行 VibeResearchTools/evidrank_lab.py case。
   - 聚合 fault_type、case_service、GT rank、top5、输入数据概况，寻找通用失败机制；不要读取 conclusion.parquet，可研究如何从 raw traces 构造类似端点异常信号。
4. 在改代码前创建迭代笔记：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V<N> --hypothesis "<一句话通用算法假设>"
5. 只修改 algorithms/evidencerank 中与通用 RCA 排序有关的逻辑，例如：
   - robust scaling / rank fusion；
   - modality confidence；
   - evidence concentration；
   - topology-aware rerank；
   - neighbor contrast；
   - 多 ground truth 排序友好性。
6. 修改后运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
   uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
   uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
7. 评估后保存新版本：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V<N> --source V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V<N-1> --new V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index

每个改进建议必须输出：
1. 失败机制；
2. 当前 EvidenceRank 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式；
8. 是否接受该版本以及理由。

接受标准：
- VibeResearchTools guard 无 high-risk 告警；
- full eval error == 0；
- AC@1 或 MRR 至少一个提升；
- AC@3 / AC@5 没有不可解释的大幅退化；
- improved / regressed case 已在 docs/EvidRank_evolve 中记录；
- VibeResearchTools/VibeResearch.md 索引已刷新。

现在经过之前优化到 V5 的结果如下，我希望最终evidencerank的AC@1能至少达到 75%-80%

│ algorithm                 ┆ total ┆ error ┆ runtime.seconds:avg ┆      MRR ┆ AC@1.count ┆ AC@3.count ┆ AC@5.count ┆     AC@1 ┆     AC@3 ┆     AC@5 ┆    Avg@3 ┆    Avg@5 │
│ evidencerank              ┆ 1,422 ┆     0 ┆            8.349568 ┆ 0.810334 ┆      994.0 ┆    1,284.0 ┆    1,370.0 ┆ 0.699015 ┆ 0.902954 ┆ 0.963432 ┆ 0.816925 ┆ 0.872152 │
│ microrca                  ┆ 1,422 ┆     0 ┆           24.493223 ┆ 0.609371 ┆      750.0 ┆      853.0 ┆    1,011.0 ┆ 0.527426 ┆ 0.599859 ┆  0.71097 ┆ 0.566104 ┆ 0.619831 │

我的小建议：其实可以集各家之所长，来把优点融合到 EvidRank 中，例如在V4优化到 V5 的过程中我们就分析了为什么现在 MircoHECL 对的都在 AC@1 ，从而看有什么事可以应用到 EvidRank的。
那么从V5 开始更新的时候，可不可以参考microrca或者microdig呢？此外，shapleyiq似乎对网络问题的解决特别准确:"Interestingly, Shapleyiq shows exceptional performance on delay-based faults (HTTPRequestDelay and HTTPResponseDelay), achieving near-perfect scores (MRR > 0.97), indicating its specialized capability in handling latency-induced issues." 如果核心阻塞点为latency-induced issues可以参考shapleyiq的设计思想。

V5 之后给出的建议：退化也记录了：`improved_to_hit1=218`，`regressed_from_hit1=37`，且这 37 个都还在 Top-5。下一轮最值得看的是剩余 `ts-ui-dashboard`、`pod-failure`、bandwidth 弱组，优先做 confidence gate 或非 HTTP/infrastructure 信号，而不是继续盲目加大 status 权重。


V5 做完并接受了。核心改动在 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:29)：新增 `trace_status_code_shift`，用 raw traces 比较每个服务内 `span_name + status` 的异常/正常分布变化，并减去 endpoint-only 的流量形状变化，避免只是奖励流量漂移。实现位置主要在 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:192)。

正式 full eval 结果达到目标区间：

| version | AC@1 | MRR | AC@3 | AC@5 | error |
| --- | ---: | ---: | ---: | ---: | ---: |
| V4 | 0.571730 | 0.706323 | 0.791139 | 0.888889 | 0 |
| V5 | 0.699015 | 0.810334 | 0.902954 | 0.963432 | 0 |

也就是 AC@1 从 `813/1422` 提到 `994/1422`，净增 181 个 Hit@1。验证完成：`compileall`、`guard` 无 high-risk、full eval `1422/1422 error=0`、`perf-report`、V5 snapshot、summary、compare、index 都已跑完。

文档已更新：
- [V5_iteration.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V5_iteration.md:53)
- [V5_summary.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V5_summary.md:1)
- [compare_V4_vs_V5.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/compare_V4_vs_V5.md:1)
- `VibeResearchTools/VibeResearch.md` index 已刷新

退化也记录了：`improved_to_hit1=218`，`regressed_from_hit1=37`，且这 37 个都还在 Top-5。下一轮最值得看的是剩余 `ts-ui-dashboard`、`pod-failure`、bandwidth 弱组，优先做 confidence gate 或非 HTTP/infrastructure 信号，而不是继续盲目加大 status 权重。

```

### 第四次迭代：

```

你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作，目标是基于 RCABench 当前 false cases 迭代优化 EvidenceRank，但必须保持算法跨系统通用，严禁把 RCABench label、case id、服务名或故障名写进算法逻辑。

背景：
- EvidenceRank 是当前研究算法，路径为 algorithms/evidencerank。
- 主实现为 algorithms/evidencerank/src/evidencerank/algorithm.py。
- 当前评估结果已在 results.md 和 output/rcabench-platform-v2 中。
- RCABench label 位于 data/rcabench-platform-v2/meta/rcabench-csv/labels.csv。
- 单 case 注入和 GT 元信息位于 data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json。
- label 和 injection 只能用于离线分析、报告和验证，不能被 algorithms/evidencerank 的运行逻辑读取。
- conclusion.parquet 属于已加工诊断结论，不要用于算法实现，也不要用于离线 false case 归因；可以研究其生成思路，并只从 raw traces 反向构造通用端点异常信号。

总体目标：
从 EvidenceRank 的 false cases 中归纳可迁移的 RCA 机制，提出并实现最小充分的通用算法改动，提升 AC@1 / MRR / AC@3 / AC@5，同时控制退化。

强约束：
1. 禁止硬编码 datapack、case id、随机后缀、服务名、故障名、dataset split。
2. 禁止在算法实现中读取 labels.csv、injection.json、output、perf report 或任何 ground truth。
3. 禁止读取 conclusion.parquet 参与算法实现或离线 false case 证据；允许研究生成思路，并只从 raw traces 构造可迁移信号。
4. 禁止为了当前数据集堆叠不可解释的 if/else、黑名单、白名单或查表逻辑。
5. 任何进入算法的改动必须能解释为跨微服务系统通用的 RCA 信号、归一化、证据融合或拓扑推理。
6. 每轮实验必须保留版本化输出，不覆盖旧结果。
7. 所有研究计划、假设、结果、经验和索引都要同步到文档；Vibe Research 主页面是 VibeResearchTools/VibeResearch.md，详细迭代文档在 docs/EvidRank_evolve/。
8. 验证算法需要较长时间是完全可以接受的。目标是通过最终 ACC 提升算法质量，而非缩短开发验证周期。不要因为全量 eval 运行慢就中止实验、跳过验证或改用已有输出做"快速分析"——这种做法可能导致真正能涨点的优化方向没有得到充分验证。例如，以下行为是被禁止的："这次离线脚本是顺序读全量 parquet，速度太慢，不适合拿来做快速研究。我会停掉这个当前启动的实验，改用已有 V2 输出和更小的抽样/并行分析来收敛候选信号。"

推荐工作流：
1. 先阅读 AGENTS.md、VibeResearchTools/VibeResearch.md、results.md、algorithms/evidencerank/src/evidencerank/algorithm.py。
2. 如果还没有 baseline snapshot，先运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
3. 研究 false cases：
   - 阅读 docs/EvidRank_evolve/<VERSION>_summary.md。
   - 对代表性 case 运行 VibeResearchTools/evidrank_lab.py case。
   - 聚合 fault_type、case_service、GT rank、top5、输入数据概况，寻找通用失败机制；不要读取 conclusion.parquet，可研究如何从 raw traces 构造类似端点异常信号。
4. 在改代码前创建迭代笔记：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V<N> --hypothesis "<一句话通用算法假设>"
5. 只修改 algorithms/evidencerank 中与通用 RCA 排序有关的逻辑，例如：
   - robust scaling / rank fusion；
   - modality confidence；
   - evidence concentration；
   - topology-aware rerank；
   - neighbor contrast；
   - 多 ground truth 排序友好性。
1. 修改后运行以下指令：
    注意，默认输出 debug 信息，为了减少无用输出，最好提前使用export LOGURU_LEVEL=INFO限制输出log 的打印
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
   uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
   uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
2. 评估后保存新版本：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V<N> --source V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V<N-1> --new V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index

每个改进建议必须输出：
1. 失败机制；
2. 当前 EvidenceRank 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式；
8. 是否接受该版本以及理由。

接受标准：
- VibeResearchTools guard 无 high-risk 告警；
- full eval error == 0；
- AC@1 或 MRR 至少一个提升；
- AC@3 / AC@5 没有不可解释的大幅退化；
- improved / regressed case 已在 docs/EvidRank_evolve 中记录；
- VibeResearchTools/VibeResearch.md 索引已刷新。

现在经过之前优化到 V6 的结果如下，我希望最终evidencerank的AC@1能至少达到 80%-85%

┌──────────┬─────────────┬───────┬───────┬────────────┬──────────┬────────────┬────────────┬────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ dataset  ┆ algorithm   ┆ total ┆ error ┆ runtime.se ┆      MRR ┆ AC@1.count ┆ AC@3.count ┆ AC@5.count ┆     AC@1 ┆     AC@3 ┆     AC@5 ┆    Avg@3 ┆    Avg@5 │
│ evidencerank            ┆  1422 ┆     0 ┆  11.807853 ┆ 0.849078 ┆     1090.0 ┆     1312.0 ┆     1367.0 ┆ 0.766526 ┆ 0.922644 ┆ 0.961322 ┆ 0.853493 ┆  0.89339 │
│ microrca                ┆ 1,422 ┆     0 ┆           24.493223 ┆ 0.609371 ┆      750.0 ┆      853.0 ┆    1,011.0 ┆ 0.527426 ┆ 0.599859 ┆  0.71097 ┆ 0.566104 ┆ 0.619831 │

我的小建议：其实可以集各家之所长，来把优点融合到 EvidRank 中，例如在V4优化到 V5 的过程中我们就分析了为什么现在 MircoHECL 对的都在 AC@1 ，从而看有什么是可以应用到 EvidRank的。V5到 V6 的过程中我们参考了shapleyiq对网络问题的解决。

那么从V6 开始更新的时候，可不可以参考microrca或者microdig呢？或者查看剩下的所有算法中有没有值得参考设计，并且要注意，不要为了一点点性能的提升而大幅提升算法运行时间：

RUN, baro, causalrca, herosas, microdig, microhecl, microrank, microrca, nezha, rcd, shapleyiq, simplerca, ton


```

### 第五次迭代：V8-V10

```

你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作，目标是基于 RCABench 当前 false cases 迭代优化 EvidenceRank，但必须保持算法跨系统通用，严禁把 RCABench label、case id、服务名或故障名写进算法逻辑。

背景：
- EvidenceRank 是当前研究算法，路径为 algorithms/evidencerank。
- 主实现为 algorithms/evidencerank/src/evidencerank/algorithm.py。
- 当前评估结果已在 results.md 和 output/rcabench-platform-v2 中。
- RCABench label 位于 data/rcabench-platform-v2/meta/rcabench-csv/labels.csv。
- 单 case 注入和 GT 元信息位于 data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json。
- label 和 injection 只能用于离线分析、报告和验证，不能被 algorithms/evidencerank 的运行逻辑读取。
- conclusion.parquet 属于已加工诊断结论，不要用于算法实现，也不要用于离线 false case 归因；可以研究其生成思路，并只从 raw traces 反向构造通用端点异常信号。

总体目标：
从 EvidenceRank 的 false cases 中归纳可迁移的 RCA 机制，提出并实现最小充分的通用算法改动，提升 AC@1 / MRR / AC@3 / AC@5，同时控制退化。

强约束：
1. 禁止硬编码 datapack、case id、随机后缀、服务名、故障名、dataset split。
2. 禁止在算法实现中读取 labels.csv、injection.json、output、perf report 或任何 ground truth。
3. 禁止读取 conclusion.parquet 参与算法实现或离线 false case 证据；允许研究生成思路，并只从 raw traces 构造可迁移信号。
4. 禁止为了当前数据集堆叠不可解释的 if/else、黑名单、白名单或查表逻辑。
5. 任何进入算法的改动必须能解释为跨微服务系统通用的 RCA 信号、归一化、证据融合或拓扑推理。
6. 每轮实验必须保留版本化输出，不覆盖旧结果。
7. 所有研究计划、假设、结果、经验和索引都要同步到文档；Vibe Research 主页面是 VibeResearchTools/VibeResearch.md，详细迭代文档在 docs/EvidRank_evolve/。
8. 验证算法需要较长时间是完全可以接受的。目标是通过最终 ACC 提升算法质量，而非缩短开发验证周期。不要因为全量 eval 运行慢就中止实验、跳过验证或改用已有输出做"快速分析"——这种做法可能导致真正能涨点的优化方向没有得到充分验证。例如，以下行为是被禁止的："这次离线脚本是顺序读全量 parquet，速度太慢，不适合拿来做快速研究。我会停掉这个当前启动的实验，改用已有 V2 输出和更小的抽样/并行分析来收敛候选信号。"

推荐工作流：
1. 先阅读 AGENTS.md、VibeResearchTools/VibeResearch.md、results.md、algorithms/evidencerank/src/evidencerank/algorithm.py。
2. 如果还没有 baseline snapshot，先运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
3. 研究 false cases：
   - 阅读 docs/EvidRank_evolve/<VERSION>_summary.md。
   - 对代表性 case 运行 VibeResearchTools/evidrank_lab.py case。
   - 聚合 fault_type、case_service、GT rank、top5、输入数据概况，寻找通用失败机制；不要读取 conclusion.parquet，可研究如何从 raw traces 构造类似端点异常信号。
4. 在改代码前创建迭代笔记：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V<N> --hypothesis "<一句话通用算法假设>"
5. 只修改 algorithms/evidencerank 中与通用 RCA 排序有关的逻辑，例如：
   - robust scaling / rank fusion；
   - modality confidence；
   - evidence concentration；
   - topology-aware rerank；
   - neighbor contrast；
   - 多 ground truth 排序友好性。
1. 修改后运行以下指令：
    注意，默认输出 debug 信息，为了减少无用输出，最好提前使用export LOGURU_LEVEL=INFO限制输出log 的打印
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
   uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
   uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
2. 评估后保存新版本：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V<N> --source V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V<N-1> --new V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index

每个改进建议必须输出：
1. 失败机制；
2. 当前 EvidenceRank 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式；
8. 是否接受该版本以及理由。

接受标准：
- VibeResearchTools guard 无 high-risk 告警；
- full eval error == 0；
- AC@1 或 MRR 至少一个提升；
- AC@3 / AC@5 没有不可解释的大幅退化；
- improved / regressed case 已在 docs/EvidRank_evolve 中记录；
- VibeResearchTools/VibeResearch.md 索引已刷新。

现在经过之前优化到 V8 的结果如下，我希望最终evidencerank的AC@1能至少达到 80%-85%，且最好runtime.seconds:avg保持在 13 秒以内。你有 2 个可以参考的优化方向：
1.首先是优化准确率
1.1 这是 V8 优化后给出的意见：下一步最有希望的方向不是继续压 endpoint，而是给 true endpoint-only 请求形状故障加一个选择性补偿信号：从 raw traces 里做 method/path/span-name novelty 的本地性判断，区分“根服务自己的请求形状突变”和“邻域传播出来的流量形状变化”。
1.2 是分析 V8 版本的 fail case 之后做针对性设计，做出新的创新。



│ algorithm                 ┆ total ┆ error ┆ runtime.seconds:avg ┆      MRR ┆ AC@1.count ┆ AC@3.count ┆ AC@5.count ┆     AC@1 ┆     AC@3 ┆     AC@5 ┆    Avg@3 ┆    Avg@5 │
│ evidencerank              ┆ 1,422 ┆     0 ┆           11.721153 ┆ 0.866904 ┆    1,121.0 ┆    1,336.0 ┆    1,385.0 ┆ 0.788326 ┆ 0.939522 ┆  0.97398 ┆ 0.873887 ┆  0.91083 │

完成了从 V6 到 V8 的一轮完整迭代，当前最佳是 **V8：AC@1 = 0.788326**，还没到你希望的 80%-85%，但已经从 V6 的 0.766526 稳定推进到 0.788326。

V7 做了 `trace_endpoint_shift`，把 raw trace 的 endpoint/span-name 分布漂移纳入 EvidenceRank；V8 在此基础上加了一个低成本的 endpoint confidence gate：当 endpoint 漂移缺少 status residual 或 trace count rise 支撑时，部分降权，避免把传播型流量形状误排到根因前面。代码在 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:29)、[algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:392)、[algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:555)。

文档和产物已更新：

- [V8_iteration.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V8_iteration.md:43)
- [V8_summary.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V8_summary.md:1)
- [compare_V7_vs_V8.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/compare_V7_vs_V8.md:7)
- `output/rcabench-platform-v2/evolve_snapshots/V8`
- `VibeResearchTools/VibeResearch.md` index 已刷新

```

### 第六次迭代：

```

你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作，目标是基于 RCABench 当前 false cases 迭代优化 EvidenceRank，但必须保持算法跨系统通用，严禁把 RCABench label、case id、服务名或故障名写进算法逻辑。

背景：
- EvidenceRank 是当前研究算法，路径为 algorithms/evidencerank。
- 主实现为 algorithms/evidencerank/src/evidencerank/algorithm.py。
- 当前评估结果已在 results.md 和 output/rcabench-platform-v2 中。
- RCABench label 位于 data/rcabench-platform-v2/meta/rcabench-csv/labels.csv。
- 单 case 注入和 GT 元信息位于 data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json。
- label 和 injection 只能用于离线分析、报告和验证，不能被 algorithms/evidencerank 的运行逻辑读取。
- conclusion.parquet 属于已加工诊断结论，不要用于算法实现，也不要用于离线 false case 归因；可以研究其生成思路，并只从 raw traces 反向构造通用端点异常信号。

总体目标：
从 EvidenceRank 的 false cases 中归纳可迁移的 RCA 机制，提出并实现最小充分的通用算法改动，提升 AC@1 / MRR / AC@3 / AC@5，同时控制退化。

强约束：
1. 禁止硬编码 datapack、case id、随机后缀、服务名、故障名、dataset split。
2. 禁止在算法实现中读取 labels.csv、injection.json、output、perf report 或任何 ground truth。
3. 禁止读取 conclusion.parquet 参与算法实现或离线 false case 证据；允许研究生成思路，并只从 raw traces 构造可迁移信号。
4. 禁止为了当前数据集堆叠不可解释的 if/else、黑名单、白名单或查表逻辑。
5. 任何进入算法的改动必须能解释为跨微服务系统通用的 RCA 信号、归一化、证据融合或拓扑推理。
6. 每轮实验必须保留版本化输出，不覆盖旧结果。
7. 所有研究计划、假设、结果、经验和索引都要同步到文档；Vibe Research 主页面是 VibeResearchTools/VibeResearch.md，详细迭代文档在 docs/EvidRank_evolve/。
8. 验证算法需要较长时间是完全可以接受的。目标是通过最终 ACC 提升算法质量，而非缩短开发验证周期。不要因为全量 eval 运行慢就中止实验、跳过验证或改用已有输出做"快速分析"——这种做法可能导致真正能涨点的优化方向没有得到充分验证。例如，以下行为是被禁止的："这次离线脚本是顺序读全量 parquet，速度太慢，不适合拿来做快速研究。我会停掉这个当前启动的实验，改用已有 V2 输出和更小的抽样/并行分析来收敛候选信号。"

推荐工作流：
1. 先阅读 AGENTS.md、VibeResearchTools/VibeResearch.md、results.md、algorithms/evidencerank/src/evidencerank/algorithm.py。
2. 如果还没有 baseline snapshot，先运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
3. 研究 false cases：
   - 阅读 docs/EvidRank_evolve/<VERSION>_summary.md。
   - 对代表性 case 运行 VibeResearchTools/evidrank_lab.py case。
   - 聚合 fault_type、case_service、GT rank、top5、输入数据概况，寻找通用失败机制；不要读取 conclusion.parquet，可研究如何从 raw traces 构造类似端点异常信号。
4. 在改代码前创建迭代笔记：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V<N> --hypothesis "<一句话通用算法假设>"
5. 只修改 algorithms/evidencerank 中与通用 RCA 排序有关的逻辑，例如：
   - robust scaling / rank fusion；
   - modality confidence；
   - evidence concentration；
   - topology-aware rerank；
   - neighbor contrast；
   - 多 ground truth 排序友好性。
1. 修改后运行以下指令：
    注意，默认输出 debug 信息，为了减少无用输出，最好提前使用export LOGURU_LEVEL=INFO限制输出log 的打印
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
   uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
   uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
2. 评估后保存新版本：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V<N> --source V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V<N-1> --new V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index

每个改进建议必须输出：
1. 失败机制；
2. 当前 EvidenceRank 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式；
8. 是否接受该版本以及理由。

接受标准：
- VibeResearchTools guard 无 high-risk 告警；
- full eval error == 0；
- AC@1 或 MRR 至少一个提升，或者运行时间下降或达到用户要求的优化方向；
- 如果是优化效率和鲁棒性，要求 AC@1 / AC@3 / AC@5 没有不可解释的大幅退化，可以有小幅下降；
- improved / regressed case 已在 docs/EvidRank_evolve 中记录；
- VibeResearchTools/VibeResearch.md 索引已刷新。

现在经过之前优化到 V11 的结果的AC@1能已经基本达到我的预期0.8，接下来优化方向是鲁棒性和可迁移性，前提是 AC@1等指标不变，或者为了鲁棒性运行 AC@1小幅下降（例如下降到 75% 左右）：
现在算法中使用先验权重的方法会让人质疑是针对数据集特化的，能不能保持无监督的方法来自适应权重，权重现在是 fix 的，可不可以自学习？不然有点针对数据集优化的感觉。我的目的是让审稿人不要认为我的固定权重是通过过拟合数据集得出来的结果，所以即使性能数据 AC@1 有所下降也是可以接受的，我更希望这是一个通用鲁棒的算法。或者至少需要一种方法，可以自动化无监督的得出这些权重，而不是手工硬编码。

```

### 第七次迭代：

```

你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作，目标是基于 RCABench 当前 false cases 迭代优化 EvidenceRank，但必须保持算法跨系统通用，严禁把 RCABench label、case id、服务名或故障名写进算法逻辑。

背景：
- EvidenceRank 是当前研究算法，路径为 algorithms/evidencerank。
- 主实现为 algorithms/evidencerank/src/evidencerank/algorithm.py。
- 当前评估结果已在 results.md 和 output/rcabench-platform-v2 中。
- RCABench label 位于 data/rcabench-platform-v2/meta/rcabench-csv/labels.csv。
- 单 case 注入和 GT 元信息位于 data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json。
- label 和 injection 只能用于离线分析、报告和验证，不能被 algorithms/evidencerank 的运行逻辑读取。
- conclusion.parquet 属于已加工诊断结论，不要用于算法实现，也不要用于离线 false case 归因；可以研究其生成思路，并只从 raw traces 反向构造通用端点异常信号。

总体目标：
从 EvidenceRank 的 false cases 中归纳可迁移的 RCA 机制，提出并实现最小充分的通用算法改动，提升 AC@1 / MRR / AC@3 / AC@5，同时控制退化。

强约束：
1. 禁止硬编码 datapack、case id、随机后缀、服务名、故障名、dataset split。
2. 禁止在算法实现中读取 labels.csv、injection.json、output、perf report 或任何 ground truth。
3. 禁止读取 conclusion.parquet 参与算法实现或离线 false case 证据；允许研究生成思路，并只从 raw traces 构造可迁移信号。
4. 禁止为了当前数据集堆叠不可解释的 if/else、黑名单、白名单或查表逻辑。
5. 任何进入算法的改动必须能解释为跨微服务系统通用的 RCA 信号、归一化、证据融合或拓扑推理。
6. 每轮实验必须保留版本化输出，不覆盖旧结果。
7. 所有研究计划、假设、结果、经验和索引都要同步到文档；Vibe Research 主页面是 VibeResearchTools/VibeResearch.md，详细迭代文档在 docs/EvidRank_evolve/。
8. 验证算法需要较长时间是完全可以接受的。目标是通过最终 ACC 提升算法质量，而非缩短开发验证周期。不要因为全量 eval 运行慢就中止实验、跳过验证或改用已有输出做"快速分析"——这种做法可能导致真正能涨点的优化方向没有得到充分验证。例如，以下行为是被禁止的："这次离线脚本是顺序读全量 parquet，速度太慢，不适合拿来做快速研究。我会停掉这个当前启动的实验，改用已有 V2 输出和更小的抽样/并行分析来收敛候选信号。"

推荐工作流：
1. 先阅读 AGENTS.md、VibeResearchTools/VibeResearch.md、results.md、algorithms/evidencerank/src/evidencerank/algorithm.py。
2. 如果还没有 baseline snapshot，先运行：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V1 --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V1 --source V1 --algorithm evidencerank --dataset rcabench
3. 研究 false cases：
   - 阅读 docs/EvidRank_evolve/<VERSION>_summary.md。
   - 对代表性 case 运行 VibeResearchTools/evidrank_lab.py case。
   - 聚合 fault_type、case_service、GT rank、top5、输入数据概况，寻找通用失败机制；不要读取 conclusion.parquet，可研究如何从 raw traces 构造类似端点异常信号。
4. 在改代码前创建迭代笔记：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version V<N> --hypothesis "<一句话通用算法假设>"
5. 只修改 algorithms/evidencerank 中与通用 RCA 排序有关的逻辑，例如：
   - robust scaling / rank fusion；
   - modality confidence；
   - evidence concentration；
   - topology-aware rerank；
   - neighbor contrast；
   - 多 ground truth 排序友好性。
1. 修改后运行以下指令：
    注意，默认输出 debug 信息，为了减少无用输出，最好提前使用export LOGURU_LEVEL=INFO限制输出log 的打印
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
   uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
   uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
2. 评估后保存新版本：
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version V<N> --source V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V<N-1> --new V<N> --algorithm evidencerank --dataset rcabench
   uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index

每个改进建议必须输出：
1. 失败机制；
2. 当前 EvidenceRank 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式；
8. 是否接受该版本以及理由。

接受标准：
- VibeResearchTools guard 无 high-risk 告警；
- full eval error == 0；
- AC@1 或 MRR 至少一个提升，或者运行时间下降或达到用户要求的优化方向；
- 如果是优化效率和鲁棒性，要求 AC@1 / AC@3 / AC@5 没有不可解释的大幅退化，可以有小幅下降；
- improved / regressed case 已在 docs/EvidRank_evolve 中记录；
- VibeResearchTools/VibeResearch.md 索引已刷新。

现在经过之前优化到 V11 的结果的AC@1能已经基本达到我的预期0.8，接下来优化方向是鲁棒性和可迁移性，前提是 AC@1等指标不变，或者为了鲁棒性运行 AC@1小幅下降（例如下降到 75% 左右）：
现在算法中使用先验权重的方法会让人质疑是针对数据集特化的，能不能保持无监督的方法来自适应权重，权重现在是 fix 的，可不可以自学习？不然有点针对数据集优化的感觉。我的目的是让审稿人不要认为我的固定权重是通过过拟合数据集得出来的结果，所以即使性能数据 AC@1 有所下降也是可以接受的，我更希望这是一个通用鲁棒的算法。或者至少需要一种方法，可以自动化无监督的得出这些权重，而不是手工硬编码。

之前已经尝试了很多次修改，不要是 fix weight，可见V13-V17，之前是尝试 case by case 的自适应权重，经验如下：对论文/审稿的建议结论是：单 case 内部的完全无监督权重学习目前不够稳，容易把传播节点、入口流量或局部日志尖峰当成根因。更 defensible 的下一步不是继续手调 per-case 权重，而是做“无标签离线全局校准”：用大量未标注 incident 的特征分布、跨模态一致性和拓扑稳定性学习全局 prior，再在单 case 内做轻量自适应。这样可以避免“RCABench label 拟合”的质疑，同时保留 V11 这类 domain prior 的稳定性。

接下来帮我尝试从“无标签离线全局校准“角度，看看怎么获得这份已有的固定阈值，或者有什么办法得到这份阈值，总之我的目的就是让这份算法看起来并不是只是在这份数据集上经过紧密的微调后才有用的，而是一种鲁棒的通用方法。


```


### 第八次迭代：开始转向优化 EvidRank-ARC

```text
你是一个微服务 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作，目标是继续优化 EvidRank-ARC（Adaptive Reliability Calibration）的算法准确率，同时保持无监督、自适应、可迁移的研究定位。

当前研究对象：
- 正式算法名：EvidRank-ARC, Adaptive Reliability Calibration。
- CLI registry：`evidencerank_arc`。
- 主实现：`algorithms/evidencerank/src/evidencerank/algorithm.py` 中的 `EvidenceRankARC`。
- 默认 `evidencerank` 不要被替换；EvidRank-ARC 是一个独立 baseline / ablation line。可以通过和evidencerank的输出对比，发现可以优化的点和逻辑，在EvidenceRankARC最好不能出现手工固定的参数或者权重，以免无法迁移。
- ARC 的核心机制：单 case 内对 feature matrix 做 positive-p95 scaling，clip 到 `[0, 3.0]`；再根据特征覆盖、证据集中度、峰值对比、top gap、同模态/跨模态一致性学习 feature reliability weight；保留 topology degree 作为无监督结构特征。
- 也可以大幅修改目前的核心机制，我的唯一目标就是无监督、自适应、可迁移且准确率足够高。例如也不一定clip 到 `[0, 3.0]`，也可以是其他。

当前 ARC baseline：
- 历史重命名前等价输出：`output/rcabench-platform-v2/evolve_snapshots/V13_SELF_LEARNED_67/`。
- 记录文档：`docs/EvidRank-ARC-Evolve/EvidRank_ARC_baseline.md`。
- 指标：total 1422, error 0, AC@1 0.705345, MRR 0.823675, AC@3 0.940225, AC@5 0.971167。
- 已知负向 ablation：去掉 topology degree 后 AC@1 降到 0.649086，因此不要轻易移除结构特征。
- 已经经过了第一轮的优化：ARC1_iteration.md

本轮目标：
1. 从 EvidRank-ARC 当前 70.53% AC@1 继续提升准确率，优先提升 AC@1 和 MRR。
2. 第一目标是稳定超过 0.75 AC@1；进一步目标是接近或超过 0.8。
3. AC@3 / AC@5 不应出现不可解释的大幅退化。
4. 仍然保持无监督 baseline：不要回退到手工固定 `FEATURE_WEIGHTS`，不要把 V11/V20 的固定 prior 直接塞回 ARC。

强约束：
1. 禁止硬编码 datapack、case id、随机后缀、服务名、故障名、dataset split。
2. 禁止在算法实现中读取 labels.csv、injection.json、output、perf report、历史排行榜或任何 ground truth。
3. 禁止读取 conclusion.parquet 作为算法证据或离线 false case 证据；端点类想法必须从 raw traces 重建。
4. label / injection 只允许用于离线报告、错误归因和文档，不允许进入 `algorithms/evidencerank` 运行路径。
5. 任何改动必须能解释为跨微服务系统通用的 RCA 信号、归一化、证据融合、拓扑推理或无标签校准。
6. 每轮实验必须保留版本化输出，不覆盖旧结果；ARC 文档必须同步到 `docs/EvidRank-ARC-Evolve/` 并刷新 VibeResearch index。
7. full eval 慢是可以接受的，不要因为耗时而跳过验证或停止实验。

优先研究方向：
- Root-vs-victim contrast：区分根因节点的局部突变和受害者/入口节点的传播型尖峰。
- Topology-aware reliability：利用 trace edge 方向、父子异常差异、邻域对比来抑制高流量传播节点。
- Modality confidence：当 log-only、trace-only 或 endpoint-only 信号与其他模态冲突时自动降权，而不是固定降权。
- Feature-family reliability：不要自由学习每个 feature 到失控；可以学习 family-level 或 constrained reliability multiplier。
- Iterative consensus：先形成服务级异常共识，再反过来重估 feature reliability，避免单一尖峰主导。
- Rank fusion / robust scaling：用 feature family rank、分位数、MAD 或 winsorized effect size 降低量纲和极端 row count 支配。

推荐工作流：
1. 先阅读：
   - `AGENTS.md`
   - `VibeResearchTools/VibeResearch.md`
   - `docs/EvidRank-ARC-Evolve/EvidRank_ARC_baseline.md`
   - `docs/EvidRank-ARC-Evolve/EvidRank_ARC_67_summary.md`
   - `algorithms/evidencerank/src/evidencerank/algorithm.py`
2. 如果当前还没有 `evidencerank_arc` 的新输出，先跑一遍重命名后的 baseline：
   `LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48`
   `uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench`
   `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version ARC_BASELINE --algorithm evidencerank_arc --dataset rcabench`
   `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version ARC_BASELINE --source ARC_BASELINE --algorithm evidencerank_arc --dataset rcabench`
3. 从 ARC false cases 出发，聚合 weak groups、hard cases、rank deltas，提出一个最小通用假设。
4. 改代码前创建迭代记录，例如：
   `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py new-note --version ARC1 --hypothesis "<一句话描述本轮 ARC 通用改进假设>"`
5. 只修改 `algorithms/evidencerank` 中与 ARC 排序相关的通用逻辑，保持 Algorithm 接口兼容。
6. 修改后至少运行：
   `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard`
   `LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48`
   `uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench`
7. 评估后保存和比较：
   `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version ARC<N> --algorithm evidencerank_arc --dataset rcabench`
   `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version ARC<N> --source ARC<N> --algorithm evidencerank_arc --dataset rcabench`
   `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old ARC<N-1> --new ARC<N> --algorithm evidencerank_arc --dataset rcabench`
   `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index`

每个候选改动必须记录：
1. 失败机制；
2. 当前 ARC 为什么会错；
3. 可泛化的新信号或组合方式；
4. 可能改善的 case 类型；
5. 可能退化的 case 类型；
6. 最小代码改动位置；
7. 验证指标和 ablation 方式；
8. 是否接受该版本以及理由。

接受标准：
- guard 无 high-risk 过拟合告警；
- full eval error == 0；
- AC@1 或 MRR 至少一个提升；
- AC@3 / AC@5 没有不可解释的大幅退化；
- 退化 case 已被解释；
- docs 和 VibeResearch index 已刷新；
- 算法仍保持 EvidRank-ARC 的无监督自适应权重定位。
```



## Operating Notes

- `VibeResearchTools/VibeResearch.md` is the dashboard and index. Prefer linking detailed notes instead of duplicating long analyses here.
- `docs/EvidRank_evolve/` is the durable archive for legacy EvidenceRank iterations; `docs/EvidRank-ARC-Evolve/` is the archive for EvidRank-ARC iterations.
- `VibeResearchTools/evidrank_lab.py index` refreshes the generated index below.
- The generated index is bounded by `VIBE-INDEX` comments. Edit outside those comments for persistent notes.

<!-- VIBE-INDEX:START -->
_Last refreshed: 2026-06-03T23:47:37+08:00_

## EvidenceRank Document Index

| type | document | updated |
| --- | --- | --- |
| iteration | [docs/EvidRank-ARC-Evolve/ARC10_iteration.md](../docs/EvidRank-ARC-Evolve/ARC10_iteration.md) | 2026-06-03T22:52:30+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC10_summary.md](../docs/EvidRank-ARC-Evolve/ARC10_summary.md) | 2026-06-03T22:32:51+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC11_iteration.md](../docs/EvidRank-ARC-Evolve/ARC11_iteration.md) | 2026-06-03T22:52:30+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC11_summary.md](../docs/EvidRank-ARC-Evolve/ARC11_summary.md) | 2026-06-03T22:41:19+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC12_iteration.md](../docs/EvidRank-ARC-Evolve/ARC12_iteration.md) | 2026-06-03T22:52:30+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC12_summary.md](../docs/EvidRank-ARC-Evolve/ARC12_summary.md) | 2026-06-03T22:48:40+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC1_iteration.md](../docs/EvidRank-ARC-Evolve/ARC1_iteration.md) | 2026-06-03T15:12:37+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC1_summary.md](../docs/EvidRank-ARC-Evolve/ARC1_summary.md) | 2026-06-03T15:10:59+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC2_iteration.md](../docs/EvidRank-ARC-Evolve/ARC2_iteration.md) | 2026-06-03T17:14:15+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC2_summary.md](../docs/EvidRank-ARC-Evolve/ARC2_summary.md) | 2026-06-03T17:15:27+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC3_iteration.md](../docs/EvidRank-ARC-Evolve/ARC3_iteration.md) | 2026-06-03T18:05:43+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC3_summary.md](../docs/EvidRank-ARC-Evolve/ARC3_summary.md) | 2026-06-03T18:05:53+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC4_iteration.md](../docs/EvidRank-ARC-Evolve/ARC4_iteration.md) | 2026-06-03T18:55:30+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC5_iteration.md](../docs/EvidRank-ARC-Evolve/ARC5_iteration.md) | 2026-06-03T19:35:12+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC5_summary.md](../docs/EvidRank-ARC-Evolve/ARC5_summary.md) | 2026-06-03T19:35:22+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC6_iteration.md](../docs/EvidRank-ARC-Evolve/ARC6_iteration.md) | 2026-06-03T20:29:38+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC6_summary.md](../docs/EvidRank-ARC-Evolve/ARC6_summary.md) | 2026-06-03T20:29:50+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC7_iteration.md](../docs/EvidRank-ARC-Evolve/ARC7_iteration.md) | 2026-06-03T21:14:12+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC7_summary.md](../docs/EvidRank-ARC-Evolve/ARC7_summary.md) | 2026-06-03T21:14:25+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC8_RECHECK_summary.md](../docs/EvidRank-ARC-Evolve/ARC8_RECHECK_summary.md) | 2026-06-03T21:49:32+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC8_iteration.md](../docs/EvidRank-ARC-Evolve/ARC8_iteration.md) | 2026-06-03T22:52:30+08:00 |
| iteration | [docs/EvidRank-ARC-Evolve/ARC9_iteration.md](../docs/EvidRank-ARC-Evolve/ARC9_iteration.md) | 2026-06-03T22:52:30+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC9_summary.md](../docs/EvidRank-ARC-Evolve/ARC9_summary.md) | 2026-06-03T22:25:33+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/ARC_BASELINE_summary.md](../docs/EvidRank-ARC-Evolve/ARC_BASELINE_summary.md) | 2026-06-03T14:04:27+08:00 |
| summary | [docs/EvidRank-ARC-Evolve/EvidRank_ARC_67_summary.md](../docs/EvidRank-ARC-Evolve/EvidRank_ARC_67_summary.md) | 2026-06-03T13:52:23+08:00 |
| note | [docs/EvidRank-ARC-Evolve/EvidRank_ARC_baseline.md](../docs/EvidRank-ARC-Evolve/EvidRank_ARC_baseline.md) | 2026-06-03T22:55:09+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC11_vs_ARC12.md](../docs/EvidRank-ARC-Evolve/compare_ARC11_vs_ARC12.md) | 2026-06-03T22:54:10+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC1_vs_ARC2.md](../docs/EvidRank-ARC-Evolve/compare_ARC1_vs_ARC2.md) | 2026-06-03T17:15:44+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC2_vs_ARC3.md](../docs/EvidRank-ARC-Evolve/compare_ARC2_vs_ARC3.md) | 2026-06-03T18:06:02+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC3_vs_ARC5.md](../docs/EvidRank-ARC-Evolve/compare_ARC3_vs_ARC5.md) | 2026-06-03T19:35:32+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC5_vs_ARC6.md](../docs/EvidRank-ARC-Evolve/compare_ARC5_vs_ARC6.md) | 2026-06-03T20:30:03+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC6_vs_ARC7.md](../docs/EvidRank-ARC-Evolve/compare_ARC6_vs_ARC7.md) | 2026-06-03T21:14:40+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC10.md](../docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC10.md) | 2026-06-03T22:33:35+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC11.md](../docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC11.md) | 2026-06-03T22:41:58+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC12.md](../docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC12.md) | 2026-06-03T22:54:10+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC8.md](../docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC8.md) | 2026-06-03T21:48:46+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC_BASELINE_vs_ARC1.md](../docs/EvidRank-ARC-Evolve/compare_ARC_BASELINE_vs_ARC1.md) | 2026-06-03T15:14:00+08:00 |
| compare | [docs/EvidRank-ARC-Evolve/compare_ARC_BASELINE_vs_ARC_67.md](../docs/EvidRank-ARC-Evolve/compare_ARC_BASELINE_vs_ARC_67.md) | 2026-06-03T13:52:33+08:00 |
| summary | [docs/EvidRank_evolve/FW_NUMERIC_BASELINE_summary.md](../docs/EvidRank_evolve/FW_NUMERIC_BASELINE_summary.md) | 2026-06-03T23:08:56+08:00 |
| iteration | [docs/EvidRank_evolve/FW_PRIORITY_LADDER_ABLATION_iteration.md](../docs/EvidRank_evolve/FW_PRIORITY_LADDER_ABLATION_iteration.md) | 2026-06-03T23:40:28+08:00 |
| iteration | [docs/EvidRank_evolve/FW_PRIORITY_LINEAR_0_7_iteration.md](../docs/EvidRank_evolve/FW_PRIORITY_LINEAR_0_7_iteration.md) | 2026-06-03T23:25:58+08:00 |
| summary | [docs/EvidRank_evolve/FW_PRIORITY_LINEAR_0_7_summary.md](../docs/EvidRank_evolve/FW_PRIORITY_LINEAR_0_7_summary.md) | 2026-06-03T23:32:35+08:00 |
| summary | [docs/EvidRank_evolve/FW_PRIORITY_POWER2_TIER_summary.md](../docs/EvidRank_evolve/FW_PRIORITY_POWER2_TIER_summary.md) | 2026-06-03T23:47:04+08:00 |
| iteration | [docs/EvidRank_evolve/FW_PRIORITY_PRIOR_iteration.md](../docs/EvidRank_evolve/FW_PRIORITY_PRIOR_iteration.md) | 2026-06-03T23:21:26+08:00 |
| summary | [docs/EvidRank_evolve/FW_PRIORITY_PRIOR_summary.md](../docs/EvidRank_evolve/FW_PRIORITY_PRIOR_summary.md) | 2026-06-03T23:17:48+08:00 |
| guide | [docs/EvidRank_evolve/README.md](../docs/EvidRank_evolve/README.md) | 2026-06-01T18:29:32+08:00 |
| iteration | [docs/EvidRank_evolve/V10_iteration.md](../docs/EvidRank_evolve/V10_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V10_summary.md](../docs/EvidRank_evolve/V10_summary.md) | 2026-06-02T11:24:53+08:00 |
| iteration | [docs/EvidRank_evolve/V11_iteration.md](../docs/EvidRank_evolve/V11_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V11_summary.md](../docs/EvidRank_evolve/V11_summary.md) | 2026-06-02T14:36:46+08:00 |
| summary | [docs/EvidRank_evolve/V11_trial_span008_summary.md](../docs/EvidRank_evolve/V11_trial_span008_summary.md) | 2026-06-02T14:29:11+08:00 |
| summary | [docs/EvidRank_evolve/V13_REIMPL_V2_summary.md](../docs/EvidRank_evolve/V13_REIMPL_V2_summary.md) | 2026-06-03T12:23:58+08:00 |
| summary | [docs/EvidRank_evolve/V13_REIMPL_V3_NO_TOPO_summary.md](../docs/EvidRank_evolve/V13_REIMPL_V3_NO_TOPO_summary.md) | 2026-06-03T12:32:27+08:00 |
| summary | [docs/EvidRank_evolve/V13_REIMPL_summary.md](../docs/EvidRank_evolve/V13_REIMPL_summary.md) | 2026-06-03T12:06:14+08:00 |
| iteration | [docs/EvidRank_evolve/V13_iteration.md](../docs/EvidRank_evolve/V13_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V13_summary.md](../docs/EvidRank_evolve/V13_summary.md) | 2026-06-02T18:10:49+08:00 |
| iteration | [docs/EvidRank_evolve/V14_iteration.md](../docs/EvidRank_evolve/V14_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V14_summary.md](../docs/EvidRank_evolve/V14_summary.md) | 2026-06-02T18:21:49+08:00 |
| iteration | [docs/EvidRank_evolve/V15_iteration.md](../docs/EvidRank_evolve/V15_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V15_summary.md](../docs/EvidRank_evolve/V15_summary.md) | 2026-06-02T18:33:51+08:00 |
| iteration | [docs/EvidRank_evolve/V16_iteration.md](../docs/EvidRank_evolve/V16_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V16_summary.md](../docs/EvidRank_evolve/V16_summary.md) | 2026-06-02T18:45:07+08:00 |
| iteration | [docs/EvidRank_evolve/V17_iteration.md](../docs/EvidRank_evolve/V17_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V17_summary.md](../docs/EvidRank_evolve/V17_summary.md) | 2026-06-02T18:54:41+08:00 |
| iteration | [docs/EvidRank_evolve/V18_iteration.md](../docs/EvidRank_evolve/V18_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V18_summary.md](../docs/EvidRank_evolve/V18_summary.md) | 2026-06-02T21:15:00+08:00 |
| iteration | [docs/EvidRank_evolve/V19_iteration.md](../docs/EvidRank_evolve/V19_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V19_summary.md](../docs/EvidRank_evolve/V19_summary.md) | 2026-06-02T22:25:28+08:00 |
| summary | [docs/EvidRank_evolve/V1_summary.md](../docs/EvidRank_evolve/V1_summary.md) | 2026-06-01T18:29:32+08:00 |
| note | [docs/EvidRank_evolve/V20_family_calibration_methodology.md](../docs/EvidRank_evolve/V20_family_calibration_methodology.md) | 2026-06-03T00:31:00+08:00 |
| iteration | [docs/EvidRank_evolve/V20_iteration.md](../docs/EvidRank_evolve/V20_iteration.md) | 2026-06-03T13:14:42+08:00 |
| summary | [docs/EvidRank_evolve/V20_summary.md](../docs/EvidRank_evolve/V20_summary.md) | 2026-06-02T23:38:55+08:00 |
| iteration | [docs/EvidRank_evolve/V2_iteration.md](../docs/EvidRank_evolve/V2_iteration.md) | 2026-06-01T18:29:32+08:00 |
| summary | [docs/EvidRank_evolve/V2_summary.md](../docs/EvidRank_evolve/V2_summary.md) | 2026-06-01T18:29:32+08:00 |
| iteration | [docs/EvidRank_evolve/V3_iteration.md](../docs/EvidRank_evolve/V3_iteration.md) | 2026-06-01T18:29:32+08:00 |
| summary | [docs/EvidRank_evolve/V3_summary.md](../docs/EvidRank_evolve/V3_summary.md) | 2026-06-01T18:29:32+08:00 |
| iteration | [docs/EvidRank_evolve/V4_iteration.md](../docs/EvidRank_evolve/V4_iteration.md) | 2026-06-01T18:29:32+08:00 |
| summary | [docs/EvidRank_evolve/V4_summary.md](../docs/EvidRank_evolve/V4_summary.md) | 2026-06-01T18:29:32+08:00 |
| iteration | [docs/EvidRank_evolve/V5_iteration.md](../docs/EvidRank_evolve/V5_iteration.md) | 2026-06-01T21:03:28+08:00 |
| summary | [docs/EvidRank_evolve/V5_summary.md](../docs/EvidRank_evolve/V5_summary.md) | 2026-06-01T21:03:40+08:00 |
| iteration | [docs/EvidRank_evolve/V6_iteration.md](../docs/EvidRank_evolve/V6_iteration.md) | 2026-06-02T01:55:06+08:00 |
| summary | [docs/EvidRank_evolve/V6_summary.md](../docs/EvidRank_evolve/V6_summary.md) | 2026-06-02T01:55:14+08:00 |
| iteration | [docs/EvidRank_evolve/V7_iteration.md](../docs/EvidRank_evolve/V7_iteration.md) | 2026-06-02T23:35:33+08:00 |
| summary | [docs/EvidRank_evolve/V7_summary.md](../docs/EvidRank_evolve/V7_summary.md) | 2026-06-02T03:01:44+08:00 |
| iteration | [docs/EvidRank_evolve/V8_iteration.md](../docs/EvidRank_evolve/V8_iteration.md) | 2026-06-02T23:35:33+08:00 |
| summary | [docs/EvidRank_evolve/V8_summary.md](../docs/EvidRank_evolve/V8_summary.md) | 2026-06-02T03:53:28+08:00 |
| iteration | [docs/EvidRank_evolve/V9_iteration.md](../docs/EvidRank_evolve/V9_iteration.md) | 2026-06-02T23:35:33+08:00 |
| summary | [docs/EvidRank_evolve/V9_summary.md](../docs/EvidRank_evolve/V9_summary.md) | 2026-06-02T10:22:26+08:00 |
| compare | [docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_LINEAR_0_7.md](../docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_LINEAR_0_7.md) | 2026-06-03T23:33:06+08:00 |
| compare | [docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_POWER2_TIER.md](../docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_POWER2_TIER.md) | 2026-06-03T23:47:37+08:00 |
| compare | [docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_PRIOR.md](../docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_PRIOR.md) | 2026-06-03T23:21:38+08:00 |
| compare | [docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_current.md](../docs/EvidRank_evolve/compare_FW_NUMERIC_BASELINE_vs_current.md) | 2026-06-03T23:22:21+08:00 |
| compare | [docs/EvidRank_evolve/compare_FW_PRIORITY_PRIOR_vs_FW_PRIORITY_LINEAR_0_7.md](../docs/EvidRank_evolve/compare_FW_PRIORITY_PRIOR_vs_FW_PRIORITY_LINEAR_0_7.md) | 2026-06-03T23:33:06+08:00 |
| compare | [docs/EvidRank_evolve/compare_FW_PRIORITY_PRIOR_vs_FW_PRIORITY_POWER2_TIER.md](../docs/EvidRank_evolve/compare_FW_PRIORITY_PRIOR_vs_FW_PRIORITY_POWER2_TIER.md) | 2026-06-03T23:47:36+08:00 |
| compare | [docs/EvidRank_evolve/compare_V10_vs_V11.md](../docs/EvidRank_evolve/compare_V10_vs_V11.md) | 2026-06-02T14:37:14+08:00 |
| compare | [docs/EvidRank_evolve/compare_V10_vs_V11_trial_span008.md](../docs/EvidRank_evolve/compare_V10_vs_V11_trial_span008.md) | 2026-06-02T14:29:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V11_vs_V13.md](../docs/EvidRank_evolve/compare_V11_vs_V13.md) | 2026-06-02T18:11:00+08:00 |
| compare | [docs/EvidRank_evolve/compare_V11_vs_V14.md](../docs/EvidRank_evolve/compare_V11_vs_V14.md) | 2026-06-02T18:22:01+08:00 |
| compare | [docs/EvidRank_evolve/compare_V11_vs_V15.md](../docs/EvidRank_evolve/compare_V11_vs_V15.md) | 2026-06-02T18:34:01+08:00 |
| compare | [docs/EvidRank_evolve/compare_V11_vs_V16.md](../docs/EvidRank_evolve/compare_V11_vs_V16.md) | 2026-06-02T18:45:17+08:00 |
| compare | [docs/EvidRank_evolve/compare_V11_vs_V17.md](../docs/EvidRank_evolve/compare_V11_vs_V17.md) | 2026-06-02T18:54:52+08:00 |
| compare | [docs/EvidRank_evolve/compare_V11_vs_V18.md](../docs/EvidRank_evolve/compare_V11_vs_V18.md) | 2026-06-02T21:15:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V11_vs_V19.md](../docs/EvidRank_evolve/compare_V11_vs_V19.md) | 2026-06-02T22:25:39+08:00 |
| compare | [docs/EvidRank_evolve/compare_V11_vs_V20.md](../docs/EvidRank_evolve/compare_V11_vs_V20.md) | 2026-06-02T23:39:26+08:00 |
| compare | [docs/EvidRank_evolve/compare_V13_REIMPL_V2_vs_V13_REIMPL_V3_NO_TOPO.md](../docs/EvidRank_evolve/compare_V13_REIMPL_V2_vs_V13_REIMPL_V3_NO_TOPO.md) | 2026-06-03T12:32:37+08:00 |
| compare | [docs/EvidRank_evolve/compare_V13_REIMPL_vs_V13_REIMPL_V2.md](../docs/EvidRank_evolve/compare_V13_REIMPL_vs_V13_REIMPL_V2.md) | 2026-06-03T12:24:08+08:00 |
| compare | [docs/EvidRank_evolve/compare_V13_vs_V14.md](../docs/EvidRank_evolve/compare_V13_vs_V14.md) | 2026-06-02T18:22:01+08:00 |
| compare | [docs/EvidRank_evolve/compare_V14_vs_V15.md](../docs/EvidRank_evolve/compare_V14_vs_V15.md) | 2026-06-02T18:34:03+08:00 |
| compare | [docs/EvidRank_evolve/compare_V15_vs_V16.md](../docs/EvidRank_evolve/compare_V15_vs_V16.md) | 2026-06-02T18:45:17+08:00 |
| compare | [docs/EvidRank_evolve/compare_V16_vs_V17.md](../docs/EvidRank_evolve/compare_V16_vs_V17.md) | 2026-06-02T18:54:51+08:00 |
| compare | [docs/EvidRank_evolve/compare_V17_vs_V18.md](../docs/EvidRank_evolve/compare_V17_vs_V18.md) | 2026-06-02T21:15:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V18_vs_V19.md](../docs/EvidRank_evolve/compare_V18_vs_V19.md) | 2026-06-02T22:31:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V19_vs_V20.md](../docs/EvidRank_evolve/compare_V19_vs_V20.md) | 2026-06-02T23:39:26+08:00 |
| compare | [docs/EvidRank_evolve/compare_V1_vs_V2.md](../docs/EvidRank_evolve/compare_V1_vs_V2.md) | 2026-06-01T18:29:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V2_vs_V3.md](../docs/EvidRank_evolve/compare_V2_vs_V3.md) | 2026-06-01T18:29:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V3_vs_V4.md](../docs/EvidRank_evolve/compare_V3_vs_V4.md) | 2026-06-01T18:29:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V4_vs_V5.md](../docs/EvidRank_evolve/compare_V4_vs_V5.md) | 2026-06-01T21:03:50+08:00 |
| compare | [docs/EvidRank_evolve/compare_V5_vs_V6.md](../docs/EvidRank_evolve/compare_V5_vs_V6.md) | 2026-06-02T01:55:22+08:00 |
| compare | [docs/EvidRank_evolve/compare_V6_vs_V7.md](../docs/EvidRank_evolve/compare_V6_vs_V7.md) | 2026-06-02T03:02:06+08:00 |
| compare | [docs/EvidRank_evolve/compare_V7_vs_V8.md](../docs/EvidRank_evolve/compare_V7_vs_V8.md) | 2026-06-02T03:53:57+08:00 |
| compare | [docs/EvidRank_evolve/compare_V8_vs_V9.md](../docs/EvidRank_evolve/compare_V8_vs_V9.md) | 2026-06-02T10:23:35+08:00 |
| compare | [docs/EvidRank_evolve/compare_V9_vs_V10.md](../docs/EvidRank_evolve/compare_V9_vs_V10.md) | 2026-06-02T11:24:43+08:00 |

### EvidRank-ARC

- [ARC evolve docs](../docs/EvidRank-ARC-Evolve)

## Versioned Artifacts

| kind | path |
| --- | --- |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC1` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC10` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC11` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC12` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC2` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC3` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC5` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC6` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC7` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC8` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC9` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/ARC_BASELINE` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/FW_NUMERIC_BASELINE` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/FW_PRIORITY_LINEAR_0_7` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/FW_PRIORITY_POWER2_TIER` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/FW_PRIORITY_PRIOR` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V1` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V10` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V11` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V11_trial_span008` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V12` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V13` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V13_REIMPL` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V13_REIMPL_V2` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V13_REIMPL_V3_NO_TOPO` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V13_SELF_LEARNED_67` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V14` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V15` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V16` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V17` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V18` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V19` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V2` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V20` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V3` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V4` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V5` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V6` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V7` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V8` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V9` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC1` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC10` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC11` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC12` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC2` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC3` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC5` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC6` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC7` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC8_RECHECK` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC9` |
| report | `output/rcabench-platform-v2/evolve_reports/ARC_BASELINE` |
| report | `output/rcabench-platform-v2/evolve_reports/FW_NUMERIC_BASELINE` |
| report | `output/rcabench-platform-v2/evolve_reports/FW_PRIORITY_LINEAR_0_7` |
| report | `output/rcabench-platform-v2/evolve_reports/FW_PRIORITY_POWER2_TIER` |
| report | `output/rcabench-platform-v2/evolve_reports/FW_PRIORITY_PRIOR` |
| report | `output/rcabench-platform-v2/evolve_reports/V1` |
| report | `output/rcabench-platform-v2/evolve_reports/V10` |
| report | `output/rcabench-platform-v2/evolve_reports/V11` |
| report | `output/rcabench-platform-v2/evolve_reports/V11_trial_span008` |
| report | `output/rcabench-platform-v2/evolve_reports/V12` |
| report | `output/rcabench-platform-v2/evolve_reports/V13` |
| report | `output/rcabench-platform-v2/evolve_reports/V13_REIMPL` |
| report | `output/rcabench-platform-v2/evolve_reports/V13_REIMPL_V2` |
| report | `output/rcabench-platform-v2/evolve_reports/V13_REIMPL_V3_NO_TOPO` |
| report | `output/rcabench-platform-v2/evolve_reports/V13_SELF_LEARNED_67` |
| report | `output/rcabench-platform-v2/evolve_reports/V14` |
| report | `output/rcabench-platform-v2/evolve_reports/V15` |
| report | `output/rcabench-platform-v2/evolve_reports/V16` |
| report | `output/rcabench-platform-v2/evolve_reports/V17` |
| report | `output/rcabench-platform-v2/evolve_reports/V18` |
| report | `output/rcabench-platform-v2/evolve_reports/V19` |
| report | `output/rcabench-platform-v2/evolve_reports/V2` |
| report | `output/rcabench-platform-v2/evolve_reports/V20` |
| report | `output/rcabench-platform-v2/evolve_reports/V3` |
| report | `output/rcabench-platform-v2/evolve_reports/V3_research` |
| report | `output/rcabench-platform-v2/evolve_reports/V4` |
| report | `output/rcabench-platform-v2/evolve_reports/V4_research` |
| report | `output/rcabench-platform-v2/evolve_reports/V5` |
| report | `output/rcabench-platform-v2/evolve_reports/V6` |
| report | `output/rcabench-platform-v2/evolve_reports/V7` |
| report | `output/rcabench-platform-v2/evolve_reports/V8` |
| report | `output/rcabench-platform-v2/evolve_reports/V9` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC11_vs_ARC12` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC1_vs_ARC2` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC2_vs_ARC3` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC3_vs_ARC5` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC5_vs_ARC6` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC6_vs_ARC7` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC7_vs_ARC10` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC7_vs_ARC11` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC7_vs_ARC12` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC7_vs_ARC8` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_ARC_BASELINE_vs_ARC1` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_LINEAR_0_7` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_POWER2_TIER` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_PRIOR` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_FW_NUMERIC_BASELINE_vs_current` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_FW_PRIORITY_PRIOR_vs_FW_PRIORITY_LINEAR_0_7` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_FW_PRIORITY_PRIOR_vs_FW_PRIORITY_POWER2_TIER` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V10_vs_V11` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V10_vs_V11_trial_span008` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V12` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V13` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V14` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V15` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V16` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V17` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V18` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V19` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V11_vs_V20` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V13_REIMPL_V2_vs_V13_REIMPL_V3_NO_TOPO` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V13_REIMPL_V2_vs_V13_SELF_LEARNED_67` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V13_REIMPL_vs_V13_REIMPL_V2` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V13_vs_V14` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V14_vs_V15` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V15_vs_V16` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V16_vs_V17` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V17_vs_V18` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V18_vs_V19` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V19_vs_V20` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V1_vs_V2` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V2_vs_V3` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V3_vs_V4` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V4_vs_V5` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V5_vs_V6` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V6_vs_V7` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V7_vs_V8` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V8_vs_V9` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V9_vs_V10` |

<!-- VIBE-INDEX:END -->

# Next Step

我的小建议：其实可以集各家之所长，来把优点融合到 EvidRank 中，例如分析为什么现在 MircoHECL对的都在 AC@1 ，从而看有什么事可以应用到 EvidRank的

V4 之后给出的建议：

下一步最有希望继续冲 AC@1 的方向是：从 raw traces/logs 重构 endpoint-level 的 path/method/status/body/error shift 信号，做 confidence gating 和拓扑抑制；仍然不直接使用 conclusion.parquet。

已完成一轮到 V4 的迭代，当前接受版本是 **V4**。

核心代码改动在 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:57)：

- V2: 非有限/缺失特征按“该特征无证据”处理，避免一个 NaN 抹掉整个服务分数。
- V3: 加入通用 feature-family weights，降低 metric/log 量纲支配，提高 row coverage 支持。
- V4: 不再把 topology degree 作为正/负硬证据，改成 trace 方向上的 `5%` 上游调用方上下文传递，见 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:340) 和 [algorithm.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py:359)。

没有在算法里读取 `labels.csv`、`injection.json`、`output`、perf report 或 `conclusion.parquet`；也没有加入 datapack/service/fault hardcode。`rg` 检查算法文件没有 `conclusion/labels/injection/ground/datapack` 命中。

**指标进展**

| version | AC@1 | MRR | AC@3 | AC@5 | error |
| --- | ---: | ---: | ---: | ---: | ---: |
| V1 baseline | 0.530239 | 0.679202 | 0.778481 | 0.877637 | 0 |
| V2 | 0.531646 | 0.684448 | 0.786920 | 0.886779 | 0 |
| V3 | 0.559072 | 0.698007 | 0.789030 | 0.888186 | 0 |
| V4 accepted | 0.571730 | 0.706323 | 0.791139 | 0.888889 | 0 |

V4 相比 V1：AC@1 从 `754/1422` 到 `813/1422`，净增 59 个 Hit@1。还没达到你希望的 65-70%，但已经是一个干净、可解释、全指标正向的版本。

**验证完成**

- `python -m compileall algorithms/evidencerank/src/evidencerank`
- `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard`
  - 无 high-risk，仅有原有 medium 提示。
- full eval：1422/1422，`error=0`
- snapshot/summary/compare 已生成：
  - [V4_iteration.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V4_iteration.md)
  - [V4_summary.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/V4_summary.md)
  - [compare_V3_vs_V4.md](/home/ljw/paper/aegis/rca-algo-contrib/docs/EvidRank_evolve/compare_V3_vs_V4.md)
- VibeResearch 索引已刷新。

下一步最有希望继续冲 AC@1 的方向是：从 raw traces/logs 重构 endpoint-level 的 path/method/status/body/error shift 信号，做 confidence gating 和拓扑抑制；仍然不直接使用 `conclusion.parquet`。
