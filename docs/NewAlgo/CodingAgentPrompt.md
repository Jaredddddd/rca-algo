# Coding Agent Prompt For New Unsupervised RCA Algorithm

Copy the prompt below into a fresh coding-agent session.

```text
你是一个微服务根因定位 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作。目标是基于当前 EvidenceRank 代码已经证明有效的能力，设计并实现一个新的、可发表叙事更强的无监督 RCA 算法。新算法必须真的 work：第一阶段 full eval 后 AC@1 至少达到 0.60，error 必须为 0；之后逐轮迭代到接近当前 EvidenceRank 的 0.80 水平。

背景：
- 当前强基线 / 探针算法是 EvidenceRank，路径为 algorithms/evidencerank。
- 主实现是 algorithms/evidencerank/src/evidencerank/algorithm.py。
- EvidenceRank 已经展示出一个高分 RCA 算法所需的能力：多模态证据、robust per-case normalization、endpoint/status mutation、log local evidence、trace topology、root-victim propagation separation、evidence-family reliability。
- 但 EvidenceRank 的核心表达仍接近 feature-priority weighted sum，作为 ICSE/FSE 顶会新方法不够 novel。
- 你要把 EvidenceRank 暴露出的能力重新组织成一个更 fancy 且有强 motivation 的无监督方法，而不是简单改名复制 EvidenceRank。

必须先阅读：
1. AGENTS.md
2. VibeResearchTools/DesignNewAlgo.md
3. docs/NewAlgo/README.md
4. docs/NewAlgo/CERA_design_brief.md
5. VibeResearchTools/VibeResearch.md
6. results.md
7. algorithms/evidencerank/src/evidencerank/algorithm.py（可以忽略其中 ARC 算法）
8. docs/feature_weight.md
9. docs/EvidRank-ARC-Evolve/EvidRank_ARC_baseline.md
10. docs/EvidRank_evolve/V11_summary.md
11. docs/EvidRank_evolve/V20_iteration.md

强约束：
1. 运行时算法禁止读取 labels.csv、injection.json、output、perf report、历史排行榜、ground truth 或 conclusion.parquet。
2. 禁止 hardcode datapack id、case id、随机后缀、服务名、故障名、dataset split。
3. 禁止把新算法实现成直接调用 EvidenceRank / EvidenceRankARC，然后返回它的 ranking。
4. 禁止复制 FEATURE_WEIGHTS 或 feature-priority weighted sum 作为新算法的最终核心。
5. 可以复用 EvidenceRank 的 raw feature extraction，因为这些是从 metrics/traces/logs/topology 得到的通用 observability transformation。
6. label 和 injection 只能用于离线 summarize / compare / false-case analysis，不能进入 algorithms/evidencerank 的运行路径。
7. 每次算法设计、计划、假设、实验结果、失败机制和下一步都必须写入 docs/NewAlgo/。
8. 验证可以慢，但不能因为慢就跳过 full eval。没有 full eval 和 perf-report，不允许声称算法 work。

建议方法名：
- 初始使用 CERA，Counterfactual Evidence Role Alignment。
- 代码 registry name 优先用 cera；如果换名，必须同步更新 docs/NewAlgo 和 VibeResearchTools/DesignNewAlgo.md。

新方法核心要求：
1. 将每个 service 建模为 latent role：root / propagation victim / background。
2. 将 EvidenceRank 的 raw features 聚合成 evidence families，而不是直接按原始 FEATURE_WEIGHTS 求和。
3. 在每个 incident 内自监督学习 family reliability：support、concentration、peak contrast、top gap、cross-view rank agreement。
4. 用 role energy 或 EM-style inference 更新 q(root)、q(victim)、q(background)。
5. 用 trace topology 做 counterfactual explain-away：相邻服务中 root-like mutation/local evidence 更强的一方应该解释 propagation-heavy victim，而不是让 victim 靠高流量/高延迟偷走 top-1。
6. 用 EvidenceRank 作为能力探针和对照，不作为运行时 teacher。可以离线比较 CERA 与 EvidenceRank 的 improved/regressed cases，用来找缺失机制。

推荐 implementation plan：
1. 不要修改默认 evidencerank 行为。先新增一个 candidate algorithm，例如 class CERA 或 LatentRoleRCA，并在 algorithms/evidencerank/main.py 注册为 cera。
2. 优先复用 algorithm.py 中的输入读取、服务收集、metric/trace/log feature extraction、trace_edges、robust cleanup helper。必要时可以小心重构成共享 helper，但保持 EvidenceRank 和 EvidenceRankARC 可运行。
3. 第一版 CERA1 做最小可运行 role-energy：
   - build feature matrix；
   - positive p95 per-case scaling，clip 到合理范围；
   - family aggregation；
   - root_energy = mutation/local/log evidence - propagation dominance + simple topology explain-away；
   - rank by root_energy；
   - 目标 AC@1 >= 0.60。
4. 第二版 CERA2 加入 family reliability：
   - support；
   - entropy concentration；
   - p95-vs-median contrast；
   - top1/top2 gap；
   - 与当前 root posterior 的 rank/cosine agreement；
   - 3 到 8 轮 EM-style update；
   - 目标 AC@1 >= 0.70。
5. 第三版 CERA3 加强 topology counterfactual explain-away：
   - 对每条 parent-child edge 测试 parent-root/child-victim 和 child-root/parent-victim 两种解释；
   - 根据 mutation excess、propagation excess、score gap 做 transfer 或 suppression；
   - 避免固定服务名或故障类型；
   - 目标 AC@1 >= 0.75。
6. CERA4+ 才考虑更复杂的离线无标签校准：
   - bootstrap family reliability；
   - synthetic root-victim pair objective；
   - bounded family-level multiplier；
   - 不能使用 labels、injection、output ranking 或 conclusion。

每轮必须生成或更新：
- docs/NewAlgo/CERA<N>_iteration.md
- 若有 compare，记录 improved_to_hit1、regressed_from_hit1、rank_improved、rank_regressed。
- VibeResearchTools/DesignNewAlgo.md 的 index 或当前状态。

每轮命令模板：

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/algorithm.py algorithms/evidencerank/main.py
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a cera -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CERA<N> --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CERA<N> --source CERA<N> --algorithm cera --dataset rcabench

从 CERA2 开始，每轮还要 compare：

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CERA<N-1> --new CERA<N> --algorithm cera --dataset rcabench

最后刷新索引：

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index

接受标准：
- guard 无 high-risk 过拟合告警；
- full eval total=1422 且 error=0；
- CERA1 AC@1 >= 0.60，否则不能叫 work；
- AC@3 / AC@5 不能出现无法解释的大幅退化；
- 文档中必须解释本轮机制、代码变化、指标、改善 case、退化 case、是否接受；
- 新算法不能破坏 evidencerank、evidencerank_arc 和多模态 variants 的可运行性。

论文叙事目标：
把 CERA 写成“latent causal-role inference + self-supervised evidence reliability + counterfactual topology explain-away”的无监督 RCA 方法。EvidenceRank 只作为探针：它证明了哪些能力必要；CERA 把这些能力系统化为新的 inference framework。

每个候选改进必须回答：
1. 失败机制是什么？
2. EvidenceRank/当前 CERA 为什么会错？
3. 新机制为什么是跨系统可迁移的？
4. 可能改善哪些 case 类型？
5. 可能退化哪些 case 类型？
6. 最小代码改动位置在哪里？
7. 用什么 ablation 验证？
8. 是否接受该版本？

现在开始：先读上述文件，写 docs/NewAlgo/CERA1_iteration.md 的假设和计划，然后实现 CERA1。不要停留在设计；必须跑 guard、compile、full eval、perf-report、snapshot、summary，并根据 AC@1 判断是否达到 work 标准。
```

