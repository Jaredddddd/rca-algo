# CREST 0.85 Coding Agent Prompt

Copy the prompt below into a fresh coding-agent session.

````text
你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作。

目标：在不参考 CERA 和 EvidenceRank 算法逻辑、不使用 CERA / EvidenceRank 手工先验权重的前提下，继续优化已有 CREST 原型，把 `crest` 在 `rcabench` 上从当前约 `AC@1 = 0.80` 推进到 `AC@1 >= 0.85`。允许大刀阔斧新增模块、重构 CREST 内部结构，甚至设计新的 CREST-family ranking/inference 算法，但必须保持 raw-only、label-free、跨系统可解释。

背景：
- 当前 CREST 注册名是 `crest`。
- 主实现是 `algorithms/evidencerank/src/evidencerank/crest.py`。
- CREST 当前已证明可达到约：
  - `AC@1 = 0.800281`
  - `MRR ~= 0.875`
  - `AC@3 ~= 0.945`
  - `AC@5 ~= 0.972`
  - `error = 0`
- 当前已知剩余失败模式主要是：弱可观测根因、基础设施/局部 pod failure、低流量或掉量根因，被高可观测入口服务、下游传播服务、日志/延迟/流量放大的受害者压过。

必须先阅读：
1. `AGENTS.md`
2. `docs/crest_evolve/README.md`
3. `docs/crest_evolve/CodingAgentPrompt.md`
4. `docs/crest_icse_paper_draft.md`
5. `algorithms/evidencerank/src/evidencerank/crest.py`
6. `algorithms/evidencerank/main.py` 中与 `crest` registry 相关的部分

可选阅读：
- `docs/crest_evolve/*.md`
- 如果 `docs/crest_evolve/` 还没有足够的历史上下文，只允许阅读 `docs/EvidRank_evolve/CREST*_*.md` 这些 CREST-only 历史文档。不要阅读其中的 EvidenceRank `V*.md`、feature-weight 文档、CERA 文档或 CERA/EvidenceRank compare 文档作为算法来源。

明确禁止：
1. 禁止参考、复制或改写 CERA / EvidenceRank 的 scoring 逻辑。
2. 禁止使用 CERA / EvidenceRank 的手工 prior weights、feature-priority ladder、ordinal tier、family multiplier、校准权重或任何历史调参结论。
3. 禁止把 EvidenceRank、EvidenceRankARC 或 CERA 当 runtime teacher、fallback、ensemble member、tie breaker 或 oracle。
4. 禁止读取或利用 labels.csv、injection.json、output、perf report、历史排行榜、ground truth 或 `conclusion.parquet` 进入算法运行路径。
5. 禁止 hardcode datapack id、case id、随机后缀、服务名、故障名、dataset split。
6. 禁止为了涨当前数据集分数堆叠不可解释的 if/else、黑名单、白名单、case/service/fault 特化规则。
7. 禁止因为 full eval 慢而跳过验证；没有 full eval 和 perf-report，不允许声称版本有效。

关于 CERA 依赖的特殊约束：
- 当前 CREST 代码可能仍从 `cera.py` import 一些 raw frame loading / feature matrix helper。这是历史技术债，不代表允许参考 CERA 算法。
- 如果需要维护接口，最多只确认当前 CREST 已 import 的 helper 函数签名和 raw data shape；不要阅读、复制或借鉴 CERA scoring、权重、role energy、iteration docs。
- 推荐优先把 CREST 需要的 raw I/O 和 feature construction 迁移到 CREST-owned helper，例如 `crest_features.py`，使 CREST 后续演化在代码结构上也不依赖 CERA。

允许并鼓励：
1. 新增 CREST 专属模块，例如：
   - `crest_features.py`
   - `crest_graph.py`
   - `crest_residual.py`
   - `crest_inference.py`
   - `crest_ablation.py`
2. 改写 CREST 的核心排序公式，不局限于当前 `A * F + S`。
3. 使用完全无标签的通用机制，例如：
   - counterfactual residual minimization；
   - topology-conditioned symptom explainability；
   - root-victim bipartite assignment；
   - incident-local Pareto / rank aggregation；
   - robust graph cut or flow attribution；
   - minimum description length / residual anomaly mass；
   - self-supervised contrastive objectives built only from raw normal/abnormal frames；
   - modality-specific confidence learned inside one incident without labels；
   - candidate cluster ranking for multi-root or infra+business co-failure cases。
4. 新增 ablation registry，例如 `crest_residual`, `crest_flow`, `crest_cluster`, `crest_victim_suppression`，只要不破坏现有 `crest`。
5. 使用离线 label / injection 做 false-case analysis、summarize、compare 和文档归因，但不得把这些信息写入算法运行路径。

优先研究方向：

1. Counterfactual residual minimization
   - 对每个候选根因 `r`，估计如果 `r` 是 root，它能解释多少邻域异常质量。
   - 排名依据不是候选自身异常有多大，而是移除其可解释传播后，全图剩余异常质量是否最小。
   - 目标是压制高可观测 victim，同时救回弱可观测 root。

2. Directional propagation asymmetry
   - 从 raw traces 构造 parent/child 方向上的异常流。
   - 区分 caller waiting、callee mutation、入口放大、下游受害。
   - 不用服务名，只用拓扑方向、正常/异常调用量、duration、status、endpoint、self-duration 的相对变化。

3. Weak-root rescue without service priors
   - 为低流量、掉量、pod failure、infra-local root 设计通用机制。
   - 例：candidate 自身 evidence 中等但其邻域 victim symptoms 高且可由该 candidate 的 drop/mutation/availability change 解释时，提高 candidate。
   - 不能写 `mysql`、`ts-ui-dashboard` 或任何服务名。

4. Victim suppression by explainability, not by fixed penalty
   - 不要简单惩罚高流量/高延迟服务。
   - 只有当某个邻居或结构路径上存在更强解释者时，才压制 victim 的传播型异常。

5. Multi-root / co-failure ranking
   - RCABench 中有些 case 有基础设施组件和业务服务共同标注。
   - 算法不能读 GT，但可以输出更稳定的候选簇或让同一解释簇中的 root-like 节点靠前，避免只把传播最强节点放第一。

6. Manual-weight-free fusion
   - 不要引入 CERA/EvidenceRank 式手工权重表。
   - 如果需要融合多个 objective，优先使用 incident-local rank statistics、Pareto dominance、learned unsupervised confidence、bounded automatic calibration、residual reduction、bootstrap stability，而不是人工常数表。
   - 少量数学超参数可以存在，但必须解释为算法稳定性参数，不是 feature prior。

每轮迭代流程：

1. 明确下一个版本号，例如如果最新是 `CREST7`，则使用 `CREST8`。不要复用旧版本号。
2. 在修改代码前写：
   - `docs/crest_evolve/CREST<N>_iteration.md`
   - 必须包含：假设、失败机制、拟新增模块、禁止参考 CERA/EvidenceRank 的执行约束、验证计划、接受/拒绝标准。
3. 验证当前 baseline：
   - 如果当前 output 中已有可靠 `crest` 输出，先 snapshot；
   - 如果没有，先跑当前 `crest` full eval，得到真实 baseline；
   - 记录 baseline 指标到 `docs/crest_evolve/CREST<N>_iteration.md`。
4. 用 false-case 报告和 case 查看做离线分析：
   - label / injection 只能用于离线分析；
   - 每个观察必须转化为跨系统机制，不得转化为服务名或故障名规则。
5. 修改 CREST 代码：
   - 优先改 `algorithms/evidencerank/src/evidencerank/crest.py` 或新增 CREST 专属模块；
   - 不要改 EvidenceRank / CERA 默认算法；
   - 保留现有 `crest_metric`, `crest_trace`, `crest_log`, pairwise modality ablations、`crest_local`, `crest_nocf` 的可运行性，除非文档明确说明替代方案。
6. 运行 guard、compile、full eval、perf-report、snapshot、summary、compare。
7. 将所有 CREST markdown 结果存放或镜像到 `docs/crest_evolve/`。
8. 更新 `docs/crest_evolve/README.md` 的当前状态或索引。

命令模板：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST<N> --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST<N> --source CREST<N> --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST<OLD> --new CREST<N> --algorithm crest --dataset rcabench
```

如果新增 ablation，不需要 full eval，只需要对比有无：

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch \
  -a crest \
  -a <new_ablation_name> \
  -d rcabench --clear --use-cpus 32

uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

注意：`evidrank_lab.py summarize` / `compare` 可能默认把 markdown 写到 `docs/EvidRank_evolve/`。CREST 相关 markdown 必须镜像到 `docs/crest_evolve/`，之后以 `docs/crest_evolve/` 为准。

接受标准：
- `guard` 无 high-risk 过拟合告警；
- full eval `total=1422` 且 `error=0`；
- 目标版本 `AC@1 >= 0.85`；
- 若还未达到 0.85，只有当 `AC@1` 或 `MRR` 有明确提升、`AC@3/AC@5` 没有不可解释退化，并且失败机制清楚时，才可作为中间研究版本保留；
- 任何接受版本都必须有 compare 文档，列出 `improved_to_hit1`、`regressed_from_hit1`、`rank_improved`、`rank_regressed`；
- 必须解释改善来自哪个通用 RCA 机制，而不是来自权重试凑；
- 必须有至少一个 ablation 证明新增模块不是无意义复杂度；
- 不破坏 `crest` 以外已有算法的 registry/import/compile。

每个候选改进必须回答：
1. 当前失败机制是什么？
2. 为什么当前 CREST 会错？
3. 新机制为什么跨系统可迁移？
4. 它是否完全避免 CERA/EvidenceRank 手工先验权重？
5. 可能改善哪些 case 类型？
6. 可能退化哪些 case 类型？
7. 最小代码改动位置在哪里？
8. 用什么 ablation 验证？
9. 指标未达 0.85 时，下一轮只做哪一个最小但有力度的通用改动？

现在开始：先确定最新 CREST 版本号，创建 `docs/crest_evolve/CREST<N>_iteration.md`，写清楚本轮假设和验证计划；然后验证当前 baseline，再实现第一个不依赖 CERA/EvidenceRank 先验的新 CREST 模块。不要停在设计。
````
