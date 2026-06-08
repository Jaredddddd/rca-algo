# CREST AIOps25 Coding Agent Prompt

Copy the prompt below into a fresh coding-agent session.

````text
你是一个微服务 / 云原生运维 RCA 算法研究员兼谨慎的 coding agent。你当前在仓库 /home/ljw/paper/aegis/rca-algo-contrib 中工作。

目标：优化 `crest` ，使它在 `aiopschallenge2025_rcabench_service` 上明显升高，最好 `AC@1 >= 0.70`；同时当前 `crest` 在 `rcabench` 上不能降低。所有算法和优化方案必须来自通用运维领域特点，例如观测覆盖、模态可靠性、trace 根因对齐度、资源/实例 provenance、传播受害者识别、跨模态一致性，而不是 AIOps25 或 RCABench 的特化规则。

背景：
- 主实现是 `algorithms/evidencerank/src/evidencerank/crest.py`。
- 主要 registry 是 `crest`，允许新增 ablation registry，例如 `crest_modality_confidence`、`crest_trace_confidence`、`crest_resource_provenance`，但最终接受版本必须能作为通用 `crest` 机制解释。
- AIOps25 数据集名是 `aiopschallenge2025_rcabench_service`，当前默认是过滤不可观测 label 后的 230 个 service-level case。
- AIOps25 当前已知结果：
  - `crest`: `total=230`, `error=0`, `AC@1=0.334783`, `MRR=0.503603`, `AC@3=0.600000`, `AC@5=0.669565`
  - `crest_metric_log`: `total=230`, `error=0`, `AC@1=0.478261`, `MRR=0.668761`, `AC@3=0.821739`, `AC@5=0.934783`
- RCABench 当前参考结果：
  - `crest`: `total=1422`, `error=0`, `AC@1=0.800281`, `MRR=0.875326`, `AC@3=0.944444`, `AC@5=0.971871`
- 如果当前工作树的 `crest` 已经不是上述 baseline，必须先重新验证当前 `crest` 在两个数据集上的指标，并把 freshly verified baseline 写入本轮 iteration 文档。不要用旧数字声称不降。

必须先阅读：
1. `AGENTS.md`
2. `docs/crest_evolve_aiops25/README.md`
3. `docs/crest_evolve_aiops25/CodingAgentPrompt.md`
4. `docs/aiopschallenge2025_rcabench_service.md`
5. `docs/aiopschallenge2025_crest_after_rebuild_analysis.md`
6. `docs/aiopschallenge2025_crest_trace_analysis.md`，注意其中 281-case 数字多为修复前历史，只能作为机制参考
7. `docs/crest_evolve/README.md`
8. `docs/crest_evolve/CodingAgentPrompt.md`
9. `algorithms/evidencerank/src/evidencerank/crest.py`
10. `algorithms/evidencerank/main.py` 中 CREST registry 相关部分

明确禁止：
1. 禁止在 runtime 算法中读取 labels、injection、output、perf report、历史排行榜、ground truth 或 `conclusion.parquet`。
2. 禁止 hardcode dataset name、datapack id、case id、随机后缀、服务名、故障名、fault type、dataset split。
3. 禁止写 `if dataset == "aiopschallenge2025_rcabench_service"`、`if service == "frontend"`、`if "jvm" in datapack` 这类分支。
4. 禁止为了涨 AIOps25 改转换器过滤策略、减少评估 case、跳过 hard cases，除非用户明确把任务改成 dataset conversion。
5. 禁止把 `crest_metric_log`、CERA、EvidenceRank 或其他算法作为 runtime teacher、fallback、ensemble oracle、tie breaker。
6. 禁止复制 CERA / EvidenceRank 的手工先验权重、feature ladder、ordinal tier、family multiplier 或调参结论。
7. 禁止把 `attr.aiops.*` 当成 AIOps25 特权标签。可以把它作为通用 resource / instance / pod provenance 元数据使用，但代码必须在这些列不存在时自然退化。
8. 禁止因为 full eval 慢而跳过验证。没有 AIOps25 和 RCABench 的 full eval / perf-report，不允许声称版本有效。

补充边界：
- `conclusion.parquet` 不要作为算法实现或离线 false-case 证据读取；如果研究它的生成思路，只能把思路转化为 raw traces / logs / metrics 上的通用信号。

允许使用：
- 离线 labels / injection 只能用于 false-case analysis、summary、compare 和文档归因。
- AIOps25 的 `labels.parquet` 可临时转换成 `/tmp` 下的 CSV 供 `evidrank_lab.py summarize/compare/case` 使用；不要提交生成的 label CSV。
- 可以新增 CREST 专属模块，例如：
  - `crest_modality.py`
  - `crest_resource.py`
  - `crest_trace_confidence.py`
  - `crest_observability.py`
  - `crest_inference.py`
- 可以新增 ablation registry，但不要破坏现有 `crest_metric`、`crest_log`、`crest_trace`、`crest_metric_log`、`crest_metric_trace`、`crest_local`、`crest_nocf` 的可运行性。

核心研究假设：

AIOps25 与 RCABench 的关键差异不是某个服务或故障名，而是每个 incident 内 telemetry reliability 的结构不同。RCABench 中 trace 覆盖广、status/path/topology 常与根因对齐，因此 full CREST 的 `A * F + S` 有用；AIOps25 中许多 resource/JVM/pod/infra 类 incident 的根因证据在 metric/log，trace 往往是入口或关键路径传播表面。通用解法不是对 AIOps25 关掉 trace，而是从 raw telemetry 自动估计每个 incident、每个候选、每个模态的根因可信度，并让 trace 结构只在“trace 看起来像根因证据”时增强排序，在“trace 看起来像传播/入口表面”时被约束。

优先研究方向：

1. Case-local modality confidence
   - 从 normal/abnormal raw frames 估计 metric、log、trace 的可靠性。
   - 信号可以包括：服务覆盖率、候选空间重叠、top-volume share、服务分布熵、normal-vs-abnormal shift、status/error/path mutation 是否集中且选择性强、跨模态 top-k 一致性。
   - 输出应是 incident-local 的 confidence / cap / gate，而不是 dataset-specific 权重表。

2. Trace structural confidence gate
   - 当 trace 服务覆盖显著窄于 metric/log，且 top-volume share 极高，且 status/error/path mutation 不够选择性时，限制 graph `F/S` 和 `abnormal_trace_rows` 对最终排序的支配。
   - 当 trace 有强 status/error/path/duration mutation、覆盖目标候选、并且不是单一入口流量面时，保留甚至增强 trace topology 的解释力。
   - 不能简单全局降低 trace，因为 RCABench 依赖 trace，AIOps25 的 network/DNS/path 类 case 也依赖 trace。

3. Metric/log root ownership under weak trace
   - 如果某服务有强 metric/log local abnormality 或 metric-log agreement，但 trace 中缺席或只显示邻居传播，不应被 trace graph 大幅压低。
   - 这应通过 evidence ownership、candidate coverage 和 confidence cap 实现，而不是固定 fallback 到 `crest_metric_log`。

4. Resource / instance / pod provenance
   - AIOps25 转换保留了 `attr.aiops.*` metric provenance，例如 pod、instance、object、device、mountpoint、kpi_key、kpi_name 等。
   - 通用做法：把 provenance 看作 resource identity，检测“某个 service 的少数 resource identity / KPI family 出现集中异常”，并把它作为 service root-local evidence。
   - 若 RCABench 或其他数据集没有这些列，代码必须无损退化；不得因为列名缺失报错或改变 unrelated behavior。

5. Entry-path victim control
   - 不要按服务名惩罚入口服务。
   - 可以用通用结构识别高入口/高流量/高 fan-in 或 high centrality symptom surface：异常 trace row share 极高、许多 downstream symptoms、metric/log root evidence 弱、trace mutation 不选择性。
   - 只有在存在更强的 root-owned metric/log/provenance/trace mutation 解释者时，才约束这类 victim 的 structural support。

6. Coverage-aware candidate union
   - trace 缺少某个服务并不代表该服务不是根因，尤其在 resource/JVM/pod/infra-like observability 下。
   - 保证 metric/log 强候选不会因为 trace coverage 缺失被隐式归零。
   - 反过来，metric/log 弱但 trace status/path/root mutation 强的候选仍应可胜出。

7. Manual-weight-free or bounded calibration
   - 如果融合多个 objective，优先使用 rank statistics、confidence gating、Pareto dominance、bounded calibration、bootstrap stability、coverage-aware caps，而不是大表式手工权重。
   - 少量数学阈值可以存在，但必须解释为稳定性参数，并通过 ablation 证明不是只为 AIOps25 调参。

每轮迭代流程：

1. 确定下一个版本号，例如 `CREST_AIOPS1`、`CREST_AIOPS2`。不要复用旧版本号。
2. 修改代码前创建 `docs/crest_evolve_aiops25/CREST_AIOPS<N>_iteration.md`，至少包含：
   - 本轮通用假设；
   - 当前 AIOps25 与 RCABench baseline；
   - 失败机制；
   - 计划新增模块或改动点；
   - 禁止数据集特化的执行约束；
   - AIOps25 验证计划；
   - RCABench 不降验证计划；
   - 接受 / 拒绝标准。
3. 先验证 baseline：
   - 如果当前 output 已可靠且与当前工作树一致，先 snapshot 为 `CREST_AIOPS<N>_BASE_AIOPS25` 和 `CREST_AIOPS<N>_BASE_RCABENCH`；
   - 否则先跑当前 `crest` 在 AIOps25 和 RCABench 的 full eval；
   - AIOps25 必须确认是当前 230-case observable service dataset，而不是旧 281-case 输出。
4. 做 false-case analysis：
   - AIOps25 labels / injection 只用于离线分析和文档；
   - 每个观察必须转化为“运维通用机制”，例如 coverage、modality reliability、resource provenance、entry-path propagation；
   - 不得转化为 service/fault/datapack 分支。
5. 修改 CREST：
   - 优先改 `algorithms/evidencerank/src/evidencerank/crest.py` 或新增 CREST-owned helper；
   - 不改 EvidenceRank / CERA 默认算法；
   - 不改 eval pipeline 来涨分；
   - 不读取 `conclusion.parquet`。
6. 运行 guard、compile、AIOps25 full eval、RCABench full eval、perf-report、snapshot、summary、compare。
7. 将本轮文档、summary、compare 镜像或直接写到 `docs/crest_evolve_aiops25/`，并更新该目录 README 当前状态。
8. 如果 AIOps25 未达到 `AC@1 >= 0.70`，但较 baseline 明显提升且 RCABench 不降，可以保留为中间研究版本；下一轮只提出一个最小但有力度的通用改动。

命令模板：

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
export LOGURU_LEVEL=WARNING
export AIOPS_DATASET=aiopschallenge2025_rcabench_service
export RCABENCH_DATASET=rcabench
```

如果需要用 `evidrank_lab.py` 对 AIOps25 做 summarize / compare，先生成离线临时 labels CSV：

```bash
uv run --package evidencerank python - <<'PY'
from pathlib import Path
import polars as pl

src = Path("data/rcabench-platform-v2/meta/aiopschallenge2025_rcabench_service/labels.parquet")
dst = Path("/tmp/aiopschallenge2025_rcabench_service_labels.csv")
pl.read_parquet(src).write_csv(dst)
print(dst)
PY
```

Baseline / eval:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -d "$AIOPS_DATASET" --clear --use-cpus 16

uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval perf-report "$AIOPS_DATASET"

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -d "$RCABENCH_DATASET" --clear --use-cpus 32

uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval perf-report "$RCABENCH_DATASET"
```

Baseline snapshot / summary:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot \
  --version CREST_AIOPS<N>_BASE_AIOPS25 --algorithm crest --dataset "$AIOPS_DATASET"

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize \
  --version CREST_AIOPS<N>_BASE_AIOPS25 \
  --source CREST_AIOPS<N>_BASE_AIOPS25 \
  --algorithm crest \
  --dataset "$AIOPS_DATASET" \
  --labels /tmp/aiopschallenge2025_rcabench_service_labels.csv

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot \
  --version CREST_AIOPS<N>_BASE_RCABENCH --algorithm crest --dataset "$RCABENCH_DATASET"

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize \
  --version CREST_AIOPS<N>_BASE_RCABENCH \
  --source CREST_AIOPS<N>_BASE_RCABENCH \
  --algorithm crest \
  --dataset "$RCABENCH_DATASET"
```

Guard / compile:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard

uv run --package evidencerank python -m compileall \
  algorithms/evidencerank/src/evidencerank/crest.py \
  algorithms/evidencerank/main.py
```

如果新增 ablation，例如 `crest_modality_confidence`，先和 `crest` 同跑两个数据集：

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_modality_confidence -d "$AIOPS_DATASET" --clear --use-cpus 16

uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval perf-report "$AIOPS_DATASET"

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -a crest_modality_confidence -d "$RCABENCH_DATASET" --clear --use-cpus 32

uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval perf-report "$RCABENCH_DATASET"
```

注意：`evidrank_lab.py compare` 当前按同一个 algorithm 名称比较 old/new。如果候选逻辑仍是 ablation registry，先用 perf-report 和 summary 看总体效果；最终接受前要把候选逻辑提升到 `crest`，重跑两个数据集，再比较 `crest` 的 baseline/result snapshots。

Result snapshot / compare 示例：

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot \
  --version CREST_AIOPS<N>_AIOPS25 --algorithm crest --dataset "$AIOPS_DATASET"

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize \
  --version CREST_AIOPS<N>_AIOPS25 \
  --source CREST_AIOPS<N>_AIOPS25 \
  --algorithm crest \
  --dataset "$AIOPS_DATASET" \
  --labels /tmp/aiopschallenge2025_rcabench_service_labels.csv

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot \
  --version CREST_AIOPS<N>_RCABENCH --algorithm crest --dataset "$RCABENCH_DATASET"

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize \
  --version CREST_AIOPS<N>_RCABENCH \
  --source CREST_AIOPS<N>_RCABENCH \
  --algorithm crest \
  --dataset "$RCABENCH_DATASET"
```

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare \
  --old CREST_AIOPS<N>_BASE_AIOPS25 \
  --new CREST_AIOPS<N>_AIOPS25 \
  --algorithm crest \
  --dataset "$AIOPS_DATASET" \
  --labels /tmp/aiopschallenge2025_rcabench_service_labels.csv

uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare \
  --old CREST_AIOPS<N>_BASE_RCABENCH \
  --new CREST_AIOPS<N>_RCABENCH \
  --algorithm crest \
  --dataset "$RCABENCH_DATASET"
```

也可以生成 AIOps25 combined report，但注意它会扫描现有输出；必须确保输出来自当前 230-case dataset 且目标算法已经 `--clear` 重跑：

```bash
uv run --package baro python scripts/combined_report.py "$AIOPS_DATASET" --sort-by AC@1
```

接受标准：

1. `guard` 无 high-risk 过拟合告警。
2. compile 通过。
3. AIOps25 full eval 完成，`total=230`、`error=0`。
4. RCABench full eval 完成，`total=1422`、`error=0`。
5. RCABench `AC@1`、`MRR`、`AC@3`、`AC@5` 不低于 freshly verified baseline；若出现极小数值差异，必须复跑确认，不能把真实退化称为噪声。
6. AIOps25 `AC@1` 和 `MRR` 至少一个明确提升，目标是 `AC@1 >= 0.70`。
7. AIOps25 `AC@3`、`AC@5` 不应出现不可解释的大幅退化。
8. 必须有 compare 文档，列出 improved_to_hit1、regressed_from_hit1、rank_improved、rank_regressed，两个数据集都要看。
9. 必须有 ablation 证明新增模块有效，例如 with/without trace-confidence gate、with/without resource provenance、with/without candidate coverage cap。
10. 必须解释改善来自哪个通用运维 RCA 机制，而不是权重试凑或数据集特化。

每个候选改进必须回答：
1. 当前失败机制是什么？
2. 为什么当前 CREST 会错？
3. 新机制为什么对运维 RCA 通用？
4. 它如何避免 AIOps25 / RCABench 特化？
5. 它如何保护 RCABench 上 trace/topology 的有效性？
6. 它可能改善哪些 incident 形态？
7. 它可能退化哪些 incident 形态？
8. 最小代码改动位置在哪里？
9. 用什么 ablation 验证？
10. 如果 AIOps25 没到 70%，下一轮只做哪一个最小通用改动？

重要判断边界：
- 如果最强方案只是“在 AIOps25 上选择 `crest_metric_log`，在 RCABench 上选择 full `crest`”，这是 dataset-specific，不可接受。
- 如果方案能在每个 incident 内根据 trace coverage、status/path selectivity、top-volume concentration、metric/log agreement 自动决定 trace structural support 强度，这是通用机制，可以接受。
- 如果方案使用 `attr.aiops.*`，必须把它解释为通用 resource provenance；在没有这些列时退化为原 CREST 行为。
- 如果目标 `AC@1 >= 0.70` 在当前 service-level 表示下达不到，必须诚实记录瓶颈和上界，不要通过过滤 case、改 label、读 GT 或 hardcode 来制造结果。

现在开始：先确定最新 `CREST_AIOPS<N>` 版本号，创建 `docs/crest_evolve_aiops25/CREST_AIOPS<N>_iteration.md`，写清楚本轮假设和双数据集验证计划；然后验证当前 baseline，再实现第一个通用的 telemetry reliability / modality confidence 改动。不要停在设计。
````
