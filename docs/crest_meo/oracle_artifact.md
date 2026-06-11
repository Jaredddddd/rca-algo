# CREST-MEO Oracle Evidence Operators

## Definition

The primary Oracle artifact is a research-only raw-telemetry synthesis upper
bound. It uses RCABench service-level GT labels offline to select one global set
of evidence operators, role assignments, and counterfactual mutation /
propagation feature sets.

The selected operators are universal across the benchmark. Their feature values
are computed only from raw normal/abnormal telemetry. The artifact is not a
deployable MEOL and must never be loaded by the online CREST-MEO path.

## Artifact

Generated file:

```text
output/rcabench-platform-v2/crest_meo_oracle/oracle_evidence_operators.json
```

Artifact type:

```text
oracle_raw_telemetry_operator_synthesis
```

Scope:

```text
global_raw_telemetry_operator_and_role_synthesis
```

The artifact contains:

- global operator specs
- selected/disabled flags
- learned `role_prior`
- `role_families`
- `counterfactual_mutation_features`
- `counterfactual_propagation_features`
- candidate-space metadata
- synthesis metrics and search history

The artifact does not contain `cases`, per-incident GT vectors, service-name
weights, GT telemetry feature banks, historical output/rank references, or
datapack-specific lookup tables.

## 如何查看和理解 `oracle_evidence_operators.json`

`oracle_evidence_operators.json` 不是某个 incident 的 ranking 输出，也不是在线
CREST-MEO 会加载的 deployable MEOL。它是一次离线 synthesis 的完整研究记录：

```text
1. 这次 synthesis 用了哪些输入；
2. 一共枚举了哪些候选 evidence operators；
3. 哪些 operators 被最终选中；
4. 每个 selected operator 被分配到哪个 CREST-MEO role；
5. counterfactual mutation / propagation sets 最终是什么；
6. 离线搜索过程和最终 upper-bound 指标是多少。
```

因此阅读这个 JSON 时，应把它理解为“全 benchmark 共用的 operator library + role
assignment + synthesis log”，而不是“每个 case 的答案表”。

### 推荐查看方式

文件比较大，不建议直接在编辑器里从头读到尾。推荐先看 top-level keys：

```bash
python - <<'PY'
import json
from pathlib import Path

p = Path("output/rcabench-platform-v2/crest_meo_oracle/oracle_evidence_operators.json")
data = json.loads(p.read_text())
print(sorted(data))
PY
```

当前 top-level keys 是：

```text
artifact_name
artifact_type
candidate_space
counterfactual_mutation_features
counterfactual_propagation_features
created_at
dataset
errors
inputs
metrics
objective
operator_count
operators
oracle_scope
policy
role_families
selected_operator_count
synthesis
```

最常看的不是全部 `operators`，而是 selected operators：

```bash
python - <<'PY'
import json
from pathlib import Path

p = Path("output/rcabench-platform-v2/crest_meo_oracle/oracle_evidence_operators.json")
data = json.loads(p.read_text())
for op in data["operators"]:
    if op["selected"]:
        print(f"{op['synthesized_role']:18s} {op['source']:6s} {op['operator_family']:20s} {op['name']}")
PY
```

也可以按 role 查看最终 role families：

```bash
python - <<'PY'
import json
from pathlib import Path

p = Path("output/rcabench-platform-v2/crest_meo_oracle/oracle_evidence_operators.json")
data = json.loads(p.read_text())
for role, names in data["role_families"].items():
    print(f"\n[{role}]")
    for name in names:
        print(" ", name)
PY
```

```
[mutation]
  crest::metric_mean_z
  crest::log_error_rate
  crest::abnormal_trace_rows
  meol::metric_max_z
  meol::trace_status_code_shift
  meol::trace_endpoint_shift
  raw_metric::k8s.pod.filesystem.usage::z_shift
  raw_log::level::distribution_shift

[propagation]
  crest::trace_status_code_shift
  crest::trace_self_duration_relative_shift
  meol::log_count_delta
  raw_metric::k8s.pod.cpu.usage::mean_delta
  raw_metric::k8s.pod.memory.page_faults::mean_delta
  raw_trace::duration::mean_delta

[observability_bias]
  crest::trace_count_delta
  crest::trace_endpoint_shift
  crest::log_count_delta
  crest::log_template_delta
  raw_metric::container.cpu.usage::mean_delta
  raw_metric::k8s.pod.filesystem.usage::robust_z_shift
  raw_metric::k8s.pod.filesystem.usage::mean_delta
  raw_trace::duration::robust_z_shift

[topology_context]
  crest::topology_in_degree
  crest::topology_out_degree
```


如果只想看最终指标：

```bash
python - <<'PY'
import json
from pathlib import Path

p = Path("output/rcabench-platform-v2/crest_meo_oracle/oracle_evidence_operators.json")
data = json.loads(p.read_text())
print(data["metrics"])
PY
```

### Top-level 字段含义

`artifact_type`
: 必须是 `oracle_raw_telemetry_operator_synthesis`。这表示该文件是 raw telemetry
  Oracle synthesis artifact，而不是旧的 case-indicator 或 prototype-bank artifact。

`oracle_scope`
: 当前为 `global_raw_telemetry_operator_and_role_synthesis`。含义是：一个全局
  operator library 作用于整个 benchmark。

`policy`
: 最重要的隔离声明。这里会标明 `uses_gt_labels=true`，同时也标明
  `uses_gt_for_feature_values=false`、`uses_per_incident_gt_signal=false`、
  `uses_service_identity_weight=false`、`uses_gt_feature_bank=false`、
  `uses_prior_run_results=false`、`not_for_online_ranking=true`。读论文或复现实验时，
  应优先检查这个字段，确认它仍然只是离线 upper-bound artifact。

`inputs`
: 记录 synthesis 使用的 label 文件、raw telemetry root 和 default MEOL path。
  它是复现实验用的输入路径说明，不代表在线算法会读取这些文件。

`candidate_space`
: 描述候选池大小和 schema scanning 参数。本次为：

```text
crest_feature_count=21
meol_operator_count=10
raw_operator_count=177
total_operator_count=208
max_scan_incidents=120
max_metric_names=60
min_case_coverage=3
```

`operators`
: 最核心的列表，长度为 `operator_count=208`。它保存所有候选 operator，不只是最终
  选中的 24 个。每个元素都是一个 operator spec + synthesis result。

`selected_operator_count`
: 最终启用的 operator 数量。本次为 `24`。判断某个 operator 是否进入最终 Oracle
  library，应看 operator 内部的 `selected` 字段，而不是只看它是否出现在
  `operators` 列表中。

`role_families`
: 按最终 role 分组后的 selected operator names。它是从 `operators` 中
  `selected=true` 且 `synthesized_role != disabled` 的项派生出来的，方便直接理解
  哪些 evidence 进入 mutation、propagation、observability_bias、topology_context。

`counterfactual_mutation_features`
: 最终用于 MEO soft counterfactual explain-away 的 mutation feature names。
  当前等价于 `role_families["mutation"]`。

`counterfactual_propagation_features`
: 最终用于 MEO soft counterfactual explain-away 的 propagation feature names。
  当前等价于 `role_families["propagation"]`。

`metrics`
: 使用最终 selected operators 和 CREST-MEO scoring path 对全量 benchmark 生成
  reference output 后得到的 upper-bound 指标。

`synthesis`
: 离线搜索过程记录。它包含 seed 指标、最终指标、筛选方法、top proxy operators、
  greedy/coordinate/prune history 等。若想解释“为什么某个 operator 被加进来或删掉”，
  应查看这里的 `history`。

`errors`
: feature extraction 期间失败的 incident 列表。本次为空，表示 1422 个 incident
  都成功提取并写出 reference output。

### 单个 Operator 怎么读

`operators` 中每个元素的结构类似：

```json
{
  "name": "raw_metric::k8s.pod.filesystem.usage::z_shift",
  "source": "metric",
  "operator_family": "raw_metric_value",
  "signal": {
    "field": "k8s.pod.filesystem.usage",
    "type": "value"
  },
  "contrast": {
    "operator": "z_shift",
    "normal_window": "pre_anomaly",
    "abnormal_window": "post_anomaly"
  },
  "aggregation": {
    "level": "service",
    "method": "service_metric"
  },
  "selected": true,
  "synthesized_role": "mutation",
  "role_prior": {
    "mutation": 1.0,
    "propagation": 0.0,
    "observability_bias": 0.0,
    "topology_context": 0.0
  },
  "mechanism": "metric-specific normality shift",
  "rationale": "Metric-name-specific value shift synthesized from raw telemetry schema.",
  "metadata": {
    "metric_name": "k8s.pod.filesystem.usage"
  }
}
```

每个字段可以这样理解：

`name`
: 全局唯一 operator 名。命名空间通常是 `crest::...`、`meol::...`、
  `raw_metric::...`、`raw_trace::...`、`raw_log::...` 或 `raw_topology::...`。

`source`
: operator 读取哪类 telemetry：`metric`、`trace`、`log` 或 `topology`。

`operator_family`
: 这个 operator 是从哪种枚举规则来的，例如 `crest_feature`、`meol_operator`、
  `raw_metric_value`、`raw_trace_numeric`、`raw_log_categorical`。

`signal`
: 读取的字段和字段类型。对 raw metric operator，`field` 通常是 metric name；
  对 trace/log operator，`field` 通常是列名或 alias；对 CREST feature，`field`
  是已有 feature name。

`contrast`
: normal window 与 abnormal window 如何比较。常见值包括 `z_shift`、
  `robust_z_shift`、`mean_delta`、`count_delta`、`distribution_shift`、
  `error_rate_delta`。

`aggregation`
: 如何聚合到 service level。Oracle 当前只做 service-level RCA，所以
  `level` 基本都是 `service`。

`selected`
: 是否进入最终 24 个 selected operators。`false` 表示它只是候选，最终被禁用。

`synthesized_role`
: 离线搜索学到的最终 role。`disabled` 表示未启用；其他值会进入 CREST-MEO
  role-vector scoring。

`role_prior`
: 与 `synthesized_role` 对应的 one-hot 权重。selected operator 的 role prior
  加和为 1；disabled operator 的 role prior 全为 0。

`mechanism` / `rationale`
: 给论文和人工检查看的机制解释。它们不是 scoring 输入，只说明为什么这个 operator
  在机制上合理。

`metadata`
: 保留枚举时的辅助信息，例如原始 metric name、原始 MEOL operator name、
  required fields 等。

### 如何判断一个 Operator 是否重要

判断顺序建议是：

1. 先看 `selected=true`；
2. 再看 `synthesized_role`，判断它在 mutation、propagation、observability_bias、
   topology_context 中扮演什么角色；
3. 看 `source` 和 `operator_family`，判断它来自 CREST、MEOL 还是 raw telemetry；
4. 看 `signal.field` 和 `contrast.operator`，理解它具体计算什么；
5. 如果要解释搜索过程，再去 `synthesis.history` 中找它何时被 `greedy_add`、
   `coordinate_pass_1` 或 `prune` 修改。

例如：

```text
raw_metric::k8s.pod.filesystem.usage::z_shift
```

应理解为：从 raw metric schema 中发现 `k8s.pod.filesystem.usage` 这个跨 incident
覆盖足够高的 metric name；对每个 service 计算 abnormal 相对 normal 的 z-shift；
离线搜索发现它作为 `mutation` role 可以提升全局 AC@1，因此最终 selected。

再如：

```text
raw_trace::duration::robust_z_shift
```

应理解为：从 trace schema 中发现 duration 类 numeric 字段；计算 robust z-shift；
最终它不是 mutation，而是 `observability_bias`，说明搜索认为它更像高可观测症状面
或强暴露信号，而不是直接根因突变。

### 这个 JSON 不保存什么

为了避免误解，需要特别强调：这个 JSON 不保存每个 incident 的 feature matrix，
也不保存每个服务的分数。它只保存“如何重新计算这些 features 和如何组合它们”的
全局规则。

如果要看最终 reference ranking，应查看：

```text
output/rcabench-platform-v2/data/rcabench/<datapack>/crest_meo_oracle_role_synthesis/output.parquet
output/rcabench-platform-v2/data/rcabench/<datapack>/crest_meo_oracle_role_synthesis/perf.parquet
```

如果要看全局汇总和每个 incident 的 best-rank summary，应查看：

```text
output/rcabench-platform-v2/crest_meo_oracle/role_synthesis_reference_result_summary.json
```

## Candidate Pool

The candidate pool includes:

- current CREST base features
- default MEOL operators
- raw metric value shifts
- metric/trace/log row-count shifts
- trace categorical distribution shifts
- trace status error-rate deltas
- trace duration/latency numeric shifts
- log categorical/template shifts
- raw trace topology edge-count and caller/callee distribution shifts

Field selection is based on schema, dtype, aliases, and minimum coverage only.
It does not use service-name, datapack-name, or fault-name rules.

## 这些 Operators 是如何找到的

这一版 Oracle 的核心思想不是手写一个能直接命中 GT 的特征，而是把“离线 LLM/MEO
可能生成的 evidence operator library”具体化为一个可复现的搜索问题：

```text
raw telemetry schema + existing CREST/MEOL definitions
  -> 自动枚举通用候选 operators
  -> 对每个 incident 计算 feature matrix
  -> 用 GT 只评价全局配置好坏
  -> 选择一套全 benchmark 共用的 operators / roles / counterfactual sets
```

换句话说，GT 只回答“哪一套全局 operator library 更好”，不参与任何 operator
在某个 incident 内的取值计算。最终选中的 24 个 operators 对 1422 个 incident
完全共用同一个定义、同一个 role assignment。

### 输入数据

离线 synthesis 工具读取三类输入：

1. `labels.csv`
   只用于构造 service-level GT mask，并在离线搜索时计算 `AC@1`、`MRR`、
   `AC@3`、`AC@5`。它不参与 feature value 计算，也不会写入主 artifact。

2. raw telemetry parquet
   每个 incident 的 `normal_metrics`、`abnormal_metrics`、`normal_traces`、
   `abnormal_traces`、`normal_logs`、`abnormal_logs`。所有候选 operator 的
   数值都只从这些 normal/abnormal telemetry frame 计算。

3. 当前 CREST / default MEOL definitions
   CREST 的 21 个基础 feature 作为已有机制先验；default MEOL 的 10 个
   operators 作为 Phase-1 MEO seed。它们只提供候选 evidence 形状和初始 role
   prior，不提供 GT 信息。

工具不读取 `conclusion.parquet`，不读取历史 `output.parquet` / `perf.parquet`，
不读取 `injection.json`，也不使用 datapack 名称、fault 名称或服务名规则。

### 候选 Operator 枚举

候选池由 `VibeResearchTools/crest_meo_universal_oracle.py` 中的
`_build_candidate_specs(...)` 生成。本次全量 run 的 candidate-space metadata 是：

```text
crest_feature_count=21
meol_operator_count=10
raw_operator_count=177
total_operator_count=208
max_scan_incidents=120
max_metric_names=60
min_case_coverage=3
```

具体枚举规则如下。

1. CREST 基础 features

   将当前 CREST 的 21 个基础 telemetry feature 全部放入候选池，命名为
   `crest::<feature_name>`。这些 feature 是现有 CREST 已经证明有效的机制性
   evidence，例如 metric shift、trace status shift、trace endpoint shift、
   log count/template shift、topology in/out degree 等。

2. default MEOL operators

   将 `default_meol.json` 中 10 个 operators 放入候选池，命名为
   `meol::<operator_name>`。当前工具为了保持全量 synthesis 可运行，会优先复用
   与 CREST 基础 feature 同名的列；如果某个 MEOL operator 暂时不能映射到已计算
   列，则返回全零列而不是报错。这保持了“operator failure 不影响整体 synthesis”
   的 Phase-1 约束。

3. raw metric value shifts

   从前 `max_scan_incidents=120` 个 incident 的 raw metric frame 中扫描
   `metric` 字段，保留至少出现在 `min_case_coverage=3` 个 incident 的 metric
   name，再按覆盖率排序取前 `max_metric_names=60` 个。实际本次去重后生成了
   144 个 raw metric value operators，即 48 个 metric names × 3 个 contrast：

   ```text
   z_shift
   robust_z_shift
   mean_delta
   ```

   这里的 metric name 是 telemetry schema 层面的字段，例如
   `k8s.pod.filesystem.usage`、`k8s.pod.cpu.usage`、`container.cpu.usage`。
   它不是服务名，也不是 datapack/fault 名称。Oracle 允许使用这些 schema-level
   metric semantics，因为离线 LLM/MEO 理论上也可以从 telemetry schema 中识别这些
   运维机制。

4. row-count shifts

   对 metric、trace、log 三种 source 都枚举 service-level row count shift：

   ```text
   count_delta
   count_rise
   count_drop
   ```

   这类 operator 捕获“观测量变化”本身，例如 trace volume 上升、log volume 下降、
   metric report count 改变等。

5. trace categorical shifts

   从 trace schema 中按 alias 发现 status/code/endpoint/route/span/method 等
   categorical 字段，计算 normal 与 abnormal 的 Jensen-Shannon distribution
   shift。字段选择只看列名 alias 和 coverage，不看具体服务或 fault。

6. trace error-rate deltas

   对 status-like trace 字段额外枚举 error-rate delta。状态码 `>=400` 或文本中
   包含 error/fail/timeout 等模式会被视为 error。该 operator 捕获接口错误率变化。

7. trace numeric shifts

   对 duration/latency/elapsed 等 numeric trace 字段枚举
   `z_shift`、`robust_z_shift`、`mean_delta`。该类 operator 捕获延迟、耗时、
   payload size 等连续值漂移。

8. log categorical shifts

   对 level/severity/log template/message template 等 log 字段计算 distribution
   shift。message 类字段会先映射为稳定 template id，避免直接依赖原始长文本。

9. raw trace topology shifts

   从 raw trace spans 中恢复 parent-child service edges，然后枚举 edge count
   rise/drop/delta，以及 caller/callee distribution shift。这类 operator 是
   topology evidence，但它仍然只来自 raw trace，不来自 GT 或历史输出。

### Feature Matrix 计算

候选池确定后，工具对每个 incident 独立构造 feature matrix：

```text
services × candidate_operators
```

计算流程是：

1. 加载 normal/abnormal telemetry frames；
2. 使用与 CREST 相同的 service normalization 逻辑收集服务列表；
3. 对 CREST candidates 调用现有 `_build_feature_matrix(...)`，再做
   `_robust_case_feature_matrix(...)`；
4. 对 MEOL candidates 复用可映射的 CREST 列，无法映射则返回零列；
5. 对 raw candidates 按 source 执行对应的 groupby / distribution / delta 计算；
6. 每个 operator 失败时返回零列，不让单个 operator crash 整个 synthesis；
7. 所有值都经过 finite、non-negative 清洗；
8. 最终整个 candidate matrix 再做一次 CREST robust case scaling。

这里最重要的约束是：`gt_mask` 只在之后评价 rank 时使用，不进入上述任何 feature
calculation。

### Role Seed

每个 operator 初始有一个 role：

```text
disabled | mutation | propagation | observability_bias | topology_context
```

初始 role 的来源是：

1. `crest::<feature>` 使用当前 CREST 的 hard-coded role families 和
   counterfactual mutation/propagation sets；
2. `meol::<operator>` 使用 `default_meol.json` 中的 `role_prior` 最大项；
3. raw operators 使用 source、field 和 contrast 的机制性 heuristic：
   status/error/endpoint/count-drop 更偏 mutation，duration/count-rise 更偏
   propagation，row-count/volume 类可能作为 observability bias，topology 类作为
   topology context。

这一步只是 seed，不是最终答案。后续 coordinate search 可以把 operator 改到其他
role，也可以禁用它。

本次全量 run 的 seed 配置启用了 31 个 operators，初始指标为：

```text
AC@1=0.739100
MRR=0.840164
AC@3=0.934599
AC@5=0.967651
```

### Screening

直接对 208 个候选逐一做完整 CREST-MEO role search 太慢，所以先用一个确定性的
single-feature rank proxy 做筛选：

1. 对每个候选 operator 单独用其 feature value 排序；
2. 用 GT 计算该单 feature 的 `AC@1/MRR/AC@3/AC@5`；
3. 按同一个 objective 排序；
4. 保留 top `max_candidates=40` 个候选进入 greedy/coordinate search；
5. seed 中已经启用的 operator 即使不在 top 40 里，也会保留进 coordinate
   candidate set。

本次 top proxy 的前几个 operator 是：

```text
raw_metric::k8s.pod.filesystem.usage::z_shift
raw_metric::k8s.pod.filesystem.usage::mean_delta
raw_metric::k8s.pod.filesystem.usage::robust_z_shift
raw_log::level::distribution_shift
raw_trace::attr.http.response.status_code::distribution_shift
raw_metric::k8s.pod.cpu.usage::mean_delta
raw_metric::container.cpu.usage::mean_delta
raw_trace::attr.http.response.status_code::error_rate_delta
raw_metric::k8s.pod.cpu_limit_utilization::mean_delta
crest::metric_anomaly_count
```

proxy 只用于减少搜索空间；最终是否选中、选中后放哪个 role，仍由完整 CREST-MEO
scoring 决定。

### Greedy Add

Greedy 阶段从 seed 配置开始，按 proxy 排名遍历 top 40 候选。对每个当前未启用的
operator，尝试五种状态：

```text
disabled
mutation
propagation
observability_bias
topology_context
```

只有当完整 objective 变好时才接受。完整 scoring 使用 CREST-MEO 的 role-vector
路径：

```text
mutation / propagation / observability_bias / topology_context
  -> local_abnormality
  -> parent context
  -> soft counterfactual explain-away
  -> final service ranking
```

Greedy 阶段的关键改善包括：

```text
raw_metric::k8s.pod.filesystem.usage::z_shift
raw_metric::k8s.pod.filesystem.usage::mean_delta
raw_log::level::distribution_shift
raw_metric::k8s.pod.cpu.usage::mean_delta
raw_metric::container.cpu.usage::mean_delta
raw_metric::k8s.pod.memory.page_faults::mean_delta
```

Greedy 结束时：

```text
AC@1=0.864276
selected_operator_count=39
```

这说明 raw telemetry schema 中确实存在 CREST 21 个基础 feature 之外的额外 RCA
evidence，尤其是 filesystem/cpu/page-fault/duration/log-level 这类机制性信号。

### Coordinate Search

Greedy 只负责“加入”候选，可能把 operator 放在局部最优 role。Coordinate search
随后遍历 seed + screened 的 62 个 candidate operators，对每个 operator 再次尝试
五种状态，并接受能提升 objective 的 role reassignment 或 disable。

这个阶段做了两类重要事情：

1. 禁用不再有帮助的 seed / MEOL operators，例如若某些 trace count/duration MEOL
   列在当前组合下增加传播噪声，就会被设为 disabled；
2. 重新解释 raw metric operator 的 role，例如 filesystem usage 的 robust/mean
   shift 最终更适合作为 observability bias，而不是纯 mutation。

Coordinate 结束时：

```text
AC@1=0.886779
selected_operator_count=27
```

### Prune

最后 prune 阶段逐个尝试删除已选 operator。若删除后 objective 不下降，或者
`AC@1/MRR/AC@3/AC@5` 更好，则接受删除。Prune 的意义是把 Oracle library 从
“所有有帮助的候选”压缩成“最小充分的全局 operator set”。

本次 prune 删除了几个冗余项，并且指标还略有提升：

```text
crest::metric_value_delta
crest::abnormal_metric_rows
meol::metric_count_drop_shift
```

最终配置为：

```text
AC@1=0.890999
MRR=0.931160
AC@3=0.969058
AC@5=0.988748
selected_operator_count=24
```

### 为什么会选中这些 Operators

最终 24 个 selected operators 可以分成四类机制。

1. Root-local mutation evidence

   这类 operator 更像“根因服务自身发生机制突变”：

   ```text
   crest::metric_mean_z
   crest::log_error_rate
   crest::abnormal_trace_rows
   meol::metric_max_z
   meol::trace_status_code_shift
   meol::trace_endpoint_shift
   raw_metric::k8s.pod.filesystem.usage::z_shift
   raw_log::level::distribution_shift
   ```

   它们强调 metric 异常、错误日志、状态码/endpoint 分布变化、trace 行数异常等。
   在 CREST-MEO scoring 中，这些 operator 进入 mutation role，用于 counterfactual
   explain-away：如果某个邻接服务有更强 mutation，而当前高分服务主要是传播症状，
   能把部分 victim energy 转移回 candidate root。

2. Propagation evidence

   这类 operator 更像“症状传播、延迟扩散、下游受害面”：

   ```text
   crest::trace_status_code_shift
   crest::trace_self_duration_relative_shift
   meol::log_count_delta
   raw_metric::k8s.pod.cpu.usage::mean_delta
   raw_metric::k8s.pod.memory.page_faults::mean_delta
   raw_trace::duration::mean_delta
   ```

   它们不一定直接表示 root，但能帮助识别 victim surface。与 mutation role 结合后，
   propagation role 可以支持 soft counterfactual explain-away。

3. Observability-bias / volume evidence

   这类 operator 捕获“某个服务是否因为观测量、流量或资源暴露而更容易高分”：

   ```text
   crest::trace_count_delta
   crest::trace_endpoint_shift
   crest::log_count_delta
   crest::log_template_delta
   raw_metric::container.cpu.usage::mean_delta
   raw_metric::k8s.pod.filesystem.usage::robust_z_shift
   raw_metric::k8s.pod.filesystem.usage::mean_delta
   raw_trace::duration::robust_z_shift
   ```

   Oracle 把其中一部分放入 observability_bias，而不是全部当作 mutation。这个结果
   很重要：它说明强异常值有时是根因证据，有时只是“可观测性更强的症状面”，需要
   与 mutation/propagation/topology 一起解释。

4. Topology context

   ```text
   crest::topology_in_degree
   crest::topology_out_degree
   ```

   这两个 operator 不单独决定 root，而是在 parent-context 和 trace explain-away
   中提供结构先验。它们帮助区分中心节点、高 fan-in/fan-out 节点和真正局部突变服务。

### 为什么选中项里有 CREST 与 MEOL 的语义重复

最终列表里同时出现了 `crest::trace_status_code_shift` 和
`meol::trace_status_code_shift`，也同时出现了 `crest::metric_mean_z` 和
`meol::metric_max_z`。这不是 per-case trick，而是离线搜索在当前 operator
表达空间中学到的全局权重效果。

在 Phase-1 实现中，MEOL operators 被编译成与现有 CREST feature matrix 兼容的列。
当 CREST feature 与 MEOL operator 语义相近但 role seed 不完全相同时，选择二者
等价于给这个机制更高的全局权重，或允许它在不同 role 中发挥作用。这符合 Oracle
upper-bound 的目的：模拟最好的离线 MEO 可能给某类机制更高 prior。若论文中需要
更严格的“无重复 operator” ablation，可以在后续版本加入 semantic deduplication。

### 与真实 LLM-MEO 的关系

真实 LLM-MEO 不能读取 GT，因此不能执行这里的 objective search。Oracle 的作用是
给出上限：如果一个离线 MEO/LLM 足够理解 telemetry schema、源码机制和运维语义，
它理论上希望接近这套全局 operators 和 role assignments。

因此，当前 artifact 不是 deployable algorithm，而是回答：

```text
当前 raw telemetry 中是否存在可由通用 operators 表达的更强 RCA evidence？
```

结果 `AC@1=0.890999` 说明答案是肯定的：在不使用 per-incident GT signal、不使用
服务名 prior、不使用 GT telemetry feature bank、不读取历史输出的条件下，raw
telemetry schema 中仍然可以合成明显强于默认 seed 的全局 evidence operator set。

## Offline Objective

GT labels are used only to choose the global configuration. The objective order
is:

```text
AC@1 -> MRR -> AC@3 -> AC@5 -> fewer selected operators
```

Runtime scoring inside the tool follows the CREST-MEO role-vector path with
parent context and soft counterfactual explain-away. GT is not used while
scoring an incident.

## Generation Command

Current full benchmark command:

```bash
uv run --package evidencerank python VibeResearchTools/crest_meo_universal_oracle.py \
  --dataset rcabench \
  --workers 32 \
  --max-candidates 40 \
  --coordinate-passes 1
```

Runtime:

```text
elapsed=55:30.40
```

## Results

Current raw-telemetry Oracle result:

- Total: `1422`
- Errors: `0`
- Candidate operators: `208`
- Selected operators: `24`
- `AC@1`: `0.890999`
- `MRR`: `0.931160`
- `AC@3`: `0.969058`
- `AC@5`: `0.988748`

Reference outputs:

```text
output/rcabench-platform-v2/data/rcabench/<datapack>/crest_meo_oracle_role_synthesis/output.parquet
output/rcabench-platform-v2/data/rcabench/<datapack>/crest_meo_oracle_role_synthesis/perf.parquet
output/rcabench-platform-v2/crest_meo_oracle/role_synthesis_reference_result_summary.json
```

## Deprecated Variants

The earlier case-indicator artifact is only a pipeline sanity check. It writes
the GT service signal per incident and is not an Oracle-MEO result.

The earlier service-name calibration and GT telemetry prototype-bank artifact is
also deprecated. It encodes GT service identity or GT telemetry examples into
the feature space, which does not represent what an offline MEO/LLM could
generate as a universal operator library.

Legacy sanity-check paths:

```text
VibeResearchTools/crest_meo_oracle.py
VibeResearchTools/crest_meo_oracle_reference.py
output/rcabench-platform-v2/crest_meo_oracle/case_indicator_oracle.json
```

## Isolation Rule

This Oracle artifact is intentionally leaky and research-only. It may read GT
labels only in `VibeResearchTools/`. It must not be used by:

- `algorithms/evidencerank/src/evidencerank/meo/library/default_meol.json`
- `score_crest_services(..., use_meo=True)`
- benchmark submissions
- any deployable or label-free RCA algorithm path
