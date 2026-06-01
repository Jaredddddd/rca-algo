# Vibe Research

This is the main page for EvidenceRank vibe research. Keep long-lived research context, launch prompts, decisions, and links here. Detailed iteration notes can stay in `docs/EvidRank_evolve/`.

## Research Entry

- Target algorithm: `algorithms/evidencerank`
- Default dataset for current evolution: `rcabench`
- Iteration docs: `docs/EvidRank_evolve/`
- Tool CLI: `VibeResearchTools/evidrank_lab.py`
- Labels for offline analysis only: `data/rcabench-platform-v2/meta/rcabench-csv/labels.csv`
- Case metadata for offline analysis only: `data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json`

## LLM Launch Prompt

Use the following prompt to start an analysis-focused LLM or coding agent for EvidenceRank evolution.

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
   uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 32
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

## Operating Notes

- `VibeResearchTools/VibeResearch.md` is the dashboard and index. Prefer linking detailed notes instead of duplicating long analyses here.
- `docs/EvidRank_evolve/` is the durable archive for iteration summaries, comparisons, and detailed case studies.
- `VibeResearchTools/evidrank_lab.py index` refreshes the generated index below.
- The generated index is bounded by `VIBE-INDEX` comments. Edit outside those comments for persistent notes.

<!-- VIBE-INDEX:START -->
_Last refreshed: 2026-06-01T13:52:35+08:00_

## EvidenceRank Document Index

| type | document | updated |
| --- | --- | --- |
| guide | [docs/EvidRank_evolve/README.md](../docs/EvidRank_evolve/README.md) | 2026-06-01T13:52:24+08:00 |

## Versioned Artifacts

| kind | path |
| --- | --- |
| none | No snapshots or reports generated yet. |

<!-- VIBE-INDEX:END -->
