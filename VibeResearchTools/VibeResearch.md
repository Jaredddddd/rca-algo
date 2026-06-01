# Vibe Research

This is the main page for EvidenceRank vibe research. Keep long-lived research context, launch prompts, decisions, and links here. Detailed iteration notes can stay in `docs/EvidRank_evolve/`.

## Research Entry

- Target algorithm: `algorithms/evidencerank`
- Default dataset for current evolution: `rcabench`
- Iteration docs: `docs/EvidRank_evolve/`
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

现在经过之前优化到 V5 的结果如下，我希望最终evidencerank的AC@1能至少达到 75%%

│ algorithm                 ┆ total ┆ error ┆ runtime.seconds:avg ┆      MRR ┆ AC@1.count ┆ AC@3.count ┆ AC@5.count ┆     AC@1 ┆     AC@3 ┆     AC@5 ┆    Avg@3 ┆    Avg@5 │
│ evidencerank              ┆ 1,422 ┆     0 ┆            8.349568 ┆ 0.810334 ┆      994.0 ┆    1,284.0 ┆    1,370.0 ┆ 0.699015 ┆ 0.902954 ┆ 0.963432 ┆ 0.816925 ┆ 0.872152 │
│ microrca                  ┆ 1,422 ┆     0 ┆           24.493223 ┆ 0.609371 ┆      750.0 ┆      853.0 ┆    1,011.0 ┆ 0.527426 ┆ 0.599859 ┆  0.71097 ┆ 0.566104 ┆ 0.619831 │

我的小建议：其实可以集各家之所长，来把优点融合到 EvidRank 中，例如在V4优化到 V5 的过程中我们就分析了为什么现在 MircoHECL对的都在 AC@1 ，从而看有什么事可以应用到 EvidRank的。
那么从V5 开始更新的时候，可不可以参考第二好的microrca呢？

V5 之后给出的建议：

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



## Operating Notes

- `VibeResearchTools/VibeResearch.md` is the dashboard and index. Prefer linking detailed notes instead of duplicating long analyses here.
- `docs/EvidRank_evolve/` is the durable archive for iteration summaries, comparisons, and detailed case studies.
- `VibeResearchTools/evidrank_lab.py index` refreshes the generated index below.
- The generated index is bounded by `VIBE-INDEX` comments. Edit outside those comments for persistent notes.

<!-- VIBE-INDEX:START -->
_Last refreshed: 2026-06-01T21:03:58+08:00_

## EvidenceRank Document Index

| type | document | updated |
| --- | --- | --- |
| guide | [docs/EvidRank_evolve/README.md](../docs/EvidRank_evolve/README.md) | 2026-06-01T18:29:32+08:00 |
| summary | [docs/EvidRank_evolve/V1_summary.md](../docs/EvidRank_evolve/V1_summary.md) | 2026-06-01T18:29:32+08:00 |
| iteration | [docs/EvidRank_evolve/V2_iteration.md](../docs/EvidRank_evolve/V2_iteration.md) | 2026-06-01T18:29:32+08:00 |
| summary | [docs/EvidRank_evolve/V2_summary.md](../docs/EvidRank_evolve/V2_summary.md) | 2026-06-01T18:29:32+08:00 |
| iteration | [docs/EvidRank_evolve/V3_iteration.md](../docs/EvidRank_evolve/V3_iteration.md) | 2026-06-01T18:29:32+08:00 |
| summary | [docs/EvidRank_evolve/V3_summary.md](../docs/EvidRank_evolve/V3_summary.md) | 2026-06-01T18:29:32+08:00 |
| iteration | [docs/EvidRank_evolve/V4_iteration.md](../docs/EvidRank_evolve/V4_iteration.md) | 2026-06-01T18:29:32+08:00 |
| summary | [docs/EvidRank_evolve/V4_summary.md](../docs/EvidRank_evolve/V4_summary.md) | 2026-06-01T18:29:32+08:00 |
| iteration | [docs/EvidRank_evolve/V5_iteration.md](../docs/EvidRank_evolve/V5_iteration.md) | 2026-06-01T21:03:28+08:00 |
| summary | [docs/EvidRank_evolve/V5_summary.md](../docs/EvidRank_evolve/V5_summary.md) | 2026-06-01T21:03:40+08:00 |
| compare | [docs/EvidRank_evolve/compare_V1_vs_V2.md](../docs/EvidRank_evolve/compare_V1_vs_V2.md) | 2026-06-01T18:29:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V2_vs_V3.md](../docs/EvidRank_evolve/compare_V2_vs_V3.md) | 2026-06-01T18:29:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V3_vs_V4.md](../docs/EvidRank_evolve/compare_V3_vs_V4.md) | 2026-06-01T18:29:32+08:00 |
| compare | [docs/EvidRank_evolve/compare_V4_vs_V5.md](../docs/EvidRank_evolve/compare_V4_vs_V5.md) | 2026-06-01T21:03:50+08:00 |

## Versioned Artifacts

| kind | path |
| --- | --- |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V1` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V2` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V3` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V4` |
| snapshot | `output/rcabench-platform-v2/evolve_snapshots/V5` |
| report | `output/rcabench-platform-v2/evolve_reports/V1` |
| report | `output/rcabench-platform-v2/evolve_reports/V2` |
| report | `output/rcabench-platform-v2/evolve_reports/V3` |
| report | `output/rcabench-platform-v2/evolve_reports/V3_research` |
| report | `output/rcabench-platform-v2/evolve_reports/V4` |
| report | `output/rcabench-platform-v2/evolve_reports/V4_research` |
| report | `output/rcabench-platform-v2/evolve_reports/V5` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V1_vs_V2` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V2_vs_V3` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V3_vs_V4` |
| report | `output/rcabench-platform-v2/evolve_reports/compare_V4_vs_V5` |

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