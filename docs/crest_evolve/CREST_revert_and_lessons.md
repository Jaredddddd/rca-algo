# CREST 撤回与踩坑总结

## 背景

本轮 CREST 研究目标是把 `crest` 在 `rcabench` 上从初始约
`AC@1=0.800281` 推进到 `AC@1>=0.85`，同时保持 raw-only、label-free、
跨系统可解释，并且不借用 CERA / EvidenceRank 的 scoring 逻辑或手工先验。

后续复盘发现，真正带来正向指标的 CREST14、CREST15、CREST17 都依赖
top-k、near-tie ratio、mutation/propagation ratio、fan-in delta 等人工门控常数。
这些门控没有使用服务名、故障名或 ground truth，不属于数据泄漏，但仍然是
magic number 风格的超参数。根据最新要求，运行路径中的 CREST 改动已撤回到
仓库基线，相关尝试只保留为研究记录。

## 撤回范围

- 已撤回 `algorithms/evidencerank/src/evidencerank/crest.py` 中新增的 residual、
  victim suppression、mutation arbitration、cluster arbitration 和 path/fan-in
  arbitration 逻辑。
- 已撤回 `algorithms/evidencerank/main.py` 中新增的 CREST ablation registry。
- 已删除未跟踪实验模块
  `algorithms/evidencerank/src/evidencerank/crest_residual.py`。
- 保留 `docs/crest_evolve/` 下的迭代记录、summary 和 compare 文档，用作后续审阅。

撤回后，`crest.py` 和 `main.py` 相对仓库基线无 diff。历史基线指标仍以
`CREST10_DEFAULT / crest` 为准：

| total | error | AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

## 已尝试路线

| 版本 / 尝试 | 结果 | 主要问题 | 是否保留到默认 |
| --- | --- | --- | --- |
| CREST8 residual | `AC@1=0.340366`，699 个 hit@1 回归 | residual support 变成 quiet-node bonus，弱信号节点被无差别抬升 | 否 |
| CREST9 gated residual | `AC@1=0.797468`，11 个改善、15 个回归 | 门控后仍会把部分传播节点当成根因 | 否 |
| CREST10 victim suppression | `AC@1=0.757384`，24 个改善、85 个回归 | broad suppression 过度压制高可观测但本来正确的根因 | 否 |
| CREST11 A/F/S rank fusion | 离线无公式提升 AC@1 或 MRR | 压缩后的 `A/F/S` 已经丢失足够的 root-victim 区分信息 | 否 |
| CREST12 family fusion | 最好公式也明显低于基线 | family-level root evidence 噪声太大，会破坏大量已正确 top-1 | 否 |
| CREST13 protocol ownership | 拒绝运行实现 | server protocol drift 很多时候标记的是症状表面，不是根因 | 否 |
| CREST14 mutation arbitration | `AC@1=0.803094`，4 个改善、0 个 hit@1 回归 | 有正收益，但依赖 top-3、near-tie、mutation/propagation ratio | 已撤回 |
| CREST15 cluster arbitration | `AC@1=0.812940`，18 个改善、0 个 hit@1 回归 | 有正收益，但依赖 top-5、near-tie、ratio 和 min incoming | 已撤回 |
| CREST16 protocol + cluster | 高收益公式有回归，零回归公式只改善 3 个 | protocol 信号仍然不够 root-specific | 否 |
| CREST17 path/fan-in arbitration | `AC@1=0.825598`，相对 CREST15 改善 18 个、0 个 hit@1 回归 | 当前最好结果，但依赖多个 path/fan-in 门控常数 | 已撤回 |
| CREST18 weak-root sweep | 已停止 | 搜索方向继续堆阈值，不符合无 magic number 要求 | 否 |

## CERA 先验边界检查

历史记录中没有已接受的 `crest_cera` runtime ablation。与 CERA 相关的边界测试主要出现在
`docs/EvidRank_evolve/CREST4_attempt.md`：

| 检查项 | 结果 | 结论 |
| --- | ---: | --- |
| CERA ordinal shape applied to CREST-normalized matrix | `AC@1=0.464135` | 只把 CERA 的 ordinal shape 套到 CREST 特征矩阵上会严重退化 |
| best blend of CERA modality variants without full CERA | `AC@1=0.838959` | 不使用 full CERA rank channel 时没有到 0.85，更没有到 0.88 |
| crest + full CERA rank channel | `AC@1=0.850211` | 达到的是 CERA3 自身水平，不是 CREST 机制独立涨点 |
| oracle over `crest`, `crest_local`, `crest_nocf`, `crest_nocalib` | `AC@1=0.874121` | 这是 oracle variant selection 上界，不是 CERA 先验，也不是可部署无监督算法 |

因此，如果“0.88”指 `AC@1`，当前证据不支持“CREST 加入 CERA 先验可到
0.88”。最接近的是不可接受的 oracle 上界 `0.874121`，以及 full CERA rank channel
的 `0.850211`。如果“0.88”指 `MRR`，则 CREST17 已到 `MRR=0.888980`，
CERA3 到 `MRR=0.904032`，但这不是 `AC@1=0.88`。

## 关键教训

1. 宽泛重排不可靠。
   只要把 residual、family evidence、protocol drift 或 victim suppression 做成全局重排，
   就很容易把传播节点、入口服务或高可观测受害者推到根因前面。

2. 已压缩的 `A/F/S` 不足以无参数涨点。
   CREST11 说明，简单的 RRF、median rank、unweighted sum 等 rank-stability 方法没有
   带来 AC@1 或 MRR 提升。

3. family-level root evidence 有 rescue 信号，但不能单独排序。
   CREST12 中部分错误 case 被救回，但整体大量回归，说明 family profile 需要更强的
   root-victim 约束，不能直接当 ranking score。

4. protocol/path drift 不能单独代表根因。
   CREST13 和 CREST16 都表明，协议、状态码、路径或方法变化常常出现在症状表面。
   CREST17 只有把它绑定到 near-tie、fan-in 和 propagation 上限后才安全，但这正是
   magic number 的来源。

5. 目前所有已验证正收益都来自窄门控 arbitration。
   这类方法没有数据泄漏，也不是服务特化，但不是“无 magic number”的算法机制。
   如果论文或后续实现要求更干净的原则，目前不应把这些门控作为默认 CREST。

## 后续若继续 CREST 的建议

如果再次推进 CREST，建议开一个严格的 `CREST_NO_MAGIC` 分支或 ablation，约束如下：

- 不允许新增固定 top-k、ratio、delta、min-count、max-count 之类常数。
- 不允许使用服务名、故障名、datapack id、label、injection、历史 output、perf report 或
  `conclusion.parquet`。
- 排序机制只能来自 incident-local 的自洽结构，例如：
  - 全服务 Pareto dominance，而不是 top-k gate；
  - leave-one-family-out 稳定性，而不是手调权重；
  - 参数自由的 rank aggregation；
  - root-victim assignment / graph cut / MDL residual minimization，但不能引入人工阈值；
  - 数据自身的分位秩或序关系，而不是固定比例。
- 必须先离线证明超过 `AC@1=0.800281` 或 `MRR=0.875326`，再实现 runtime ablation。
- 即使离线有效，也必须 full eval、perf-report、snapshot、summary、compare 后才能接受。

## 当前结论

截至本总结，没有已验证模块能在完全不新增 magic number 的前提下稳定提升 CREST。
因此本轮撤回所有 CREST 运行路径改动，只保留研究文档作为负向实验和后续设计依据。
