可以。你可以把 **MEO（Mechanism-grounded Evidence Operator Synthesis）** 设计成一个“离线知识构建 + 在线确定性执行”的模块。它的核心目标不是让 LLM 直接做 RCA，而是让 LLM 从 **源码、插桩点、telemetry schema、运维语义** 中生成一套可验证、可编译、可复现的 **evidence operator library**。在线阶段 CREST 仍然只跑确定性特征计算和 counterfactual ranking。

这个设计可以直接借鉴 MetaRCA 的思路：MetaRCA 把 LLM 放在离线阶段，用 metadata ontology 和 structured prompt bootstrapping 一个 Meta Causal Graph，在线阶段再做轻量化实例化、加权和剪枝；你这里不是构建 causal graph，而是构建 **Meta Evidence Operator Library**。

CREST 现在的固定 feature families、mutation features 和 propagation features 可以被 MEO 替代成“由 DSL 生成、verifier 过滤、compiler 编译”的 operator library，而不是手工列表。

---

# 1. MEO 的定位

MEO 的输入是：

```
source code + deployment files + telemetry schema + instrumentation points + docs + optional generic fault mechanism catalog
```

MEO 的输出是：

```
Meta Evidence Operator Library, MEOL
```

MEOL 里面每一项是一个 feature spec，比如：

```json
{
  "name": "trace_status_code_shift",
  "source": "trace",
  "entity": "service",
  "signal": "status_code",
  "operator": "distribution_shift",
  "normal_window": "pre_anomaly",
  "abnormal_window": "post_anomaly",
  "aggregation": "service_level",
  "role_prior": {
    "mutation": 1.0,
    "propagation": 0.0,
    "observability_bias": 0.0,
    "topology_context": 0.00
  },
  "mechanism": "interface failure",
  "required_fields": ["timestamp", "service_name", "status_code"],
  "rationale": "A service-level status-code distribution shift indicates an interface-level failure mode."
}
```

运行时 CREST 不再依赖：

```python
CREST_COUNTERFACTUAL_MUTATION_FEATURES = {...}
CREST_COUNTERFACTUAL_PROPAGATION_FEATURES = {...}
```

而是从 MEOL 读出：

```python
is_mutation_feature[f]
is_propagation_feature[f]
```

然后把这些 membership 传给当前 CREST 的 counterfactual explain-away。默认
CREST-MEO 不使用连续 4 维 role weight 重新投影分数；MEOL 只替代 feature/operator
配置来源，local abnormality、parent context、denoised support、final score 都复刻
CREST。

---

# 2. 总体流程

MEO 可以分成七个阶段：

```
[1] Artifact Mining
        ↓
[2] Operational Semantic Extraction
        ↓
[3] Mechanism Card Construction
        ↓
[4] DSL-constrained LLM Operator Synthesis
        ↓
[5] Deterministic Verification
        ↓
[6] DSL Compiler
        ↓
[7] MEOL Runtime Instantiation for CREST
```

关键是：**LLM 只在离线阶段生成 operator spec；真正计算 feature 和 RCA ranking 的部分都是 deterministic。**

这和 TORAI 的 normal/abnormal window 思路兼容。TORAI 也是先把 metrics、logs、traces 转成 time series，再用 normal period 学 expected behavior，用 abnormal period 衡量 deviation。

MEO 只是进一步回答：**这些 time-series 应该如何被组合成 mutation evidence、propagation evidence、bias evidence？**

---

# 3. Stage 1: Artifact Mining

这个阶段不需要 LLM，先用静态解析器把系统可观测对象抽出来。

## 3.1 输入 artifacts

建议支持这些：

```
source/
  *.py, *.go, *.java, *.js
deploy/
  k8s yaml, docker-compose, helm charts
observability/
  prometheus rules, otel config, jaeger schema, log parser config
docs/
  README, architecture docs, runbooks, postmortems
telemetry_schema/
  metric columns, trace columns, log columns
```

## 3.2 抽取对象

你要把所有 artifact 统一成一个 ontology：

```python
@dataclass
class ServiceEntity:
    name: str
    language: str | None
    source_files: list[str]
    endpoints: list[str]
    log_templates: list[str]
    metrics: list[str]
    trace_spans: list[str]
    dependencies: list[str]

@dataclass
class TelemetrySignal:
    name: str
    modality: Literal["metric", "log", "trace", "topology"]
    entity_type: Literal["service", "endpoint", "edge", "log_template", "status_code"]
    semantic_type: Literal[
        "resource", "latency", "error", "traffic",
        "duration", "count", "distribution", "event"
    ]
    required_fields: list[str]
    source_artifacts: list[str]
```

## 3.3 怎么从代码里抽

可以先做轻量版本，不需要完整 program analysis：

### 对 HTTP endpoint

找：

```
@app.route(...)
router.get(...)
@PostMapping(...)
http.HandleFunc(...)
```

输出：

```json
{
  "service": "checkout",
  "endpoint": "/checkout",
  "artifact": "src/checkout/app.py:42",
  "semantic": "user-facing request entry"
}
```

### 对 log statement

找：

```
logger.error(...)
logger.warn(...)
log.Printf(...)
```

用 Drain 或简单模板化生成 log template：

```json
{
  "service": "payment",
  "log_template": "failed to charge card: <*>",
  "severity_hint": "error",
  "artifact": "src/payment/payment.go:91"
}
```

### 对 trace span

找 OpenTelemetry / Jaeger instrumentation：

```
tracer.start_span(...)
with tracer.start_as_current_span(...)
span.set_attribute(...)
```

输出：

```json
{
  "service": "frontend",
  "span": "POST /cart",
  "attributes": ["http.status_code", "http.route", "duration"],
  "artifact": "src/frontend/trace.py:18"
}
```

### 对 metrics

找：

```
Counter(...)
Gauge(...)
Histogram(...)
Summary(...)
prometheus_client
```

输出：

```json
{
  "service": "recommendation",
  "metric": "request_latency_seconds",
  "metric_type": "histogram",
  "semantic": "latency",
  "artifact": "src/recommendation/metrics.py:23"
}
```

---

# 4. Stage 2: Operational Semantic Extraction

这一步可以用 LLM，但它不生成 feature，只给 artifact 做语义标注。

输入给 LLM 的不是全部源码，而是压缩后的 artifact cards：

```json
{
  "service": "payment",
  "endpoints": ["/charge"],
  "logs": [
    {"template": "failed to charge card: <*>", "level": "error"}
  ],
  "metrics": [
    {"name": "payment_request_total", "type": "counter"},
    {"name": "payment_latency_seconds", "type": "histogram"}
  ],
  "traces": [
    {"span": "POST /charge", "attributes": ["status_code", "duration"]}
  ],
  "dependencies": ["currency", "checkout"]
}
```

LLM 输出：

```json
{
  "service": "payment",
  "semantic_summary": "Payment is a downstream dependency of checkout and exposes charge-related interface behavior.",
  "candidate_mechanisms": [
    "interface failure",
    "dependency slowdown",
    "error propagation"
  ],
  "telemetry_semantics": [
    {
      "signal": "payment_latency_seconds",
      "semantic_type": "latency",
      "likely_role": "propagation_or_local_shift"
    },
    {
      "signal": "failed to charge card: <*>",
      "semantic_type": "error_event",
      "likely_role": "mutation"
    }
  ]
}
```

这一步的目的不是准确决定 root cause，而是把“源码里的东西”翻译成“运维语义”。

---

# 5. Stage 3: Mechanism Card Construction

这是 MEO 的核心之一。你不要直接让 LLM 从 feature list 开始，而是先构建 **mechanism cards**。

一个 mechanism card 描述：

```
故障机制 → 可观测后果 → 适合的 DSL atoms → evidence role
```

例如：

```json
{
  "mechanism": "interface failure",
  "description": "A service interface returns abnormal status codes or errors.",
  "observable_consequences": [
    "status code distribution changes",
    "error rate increases",
    "error log templates appear more frequently"
  ],
  "allowed_atoms": [
    "rate_delta",
    "distribution_shift",
    "count_rise"
  ],
  "role_prior": {
    "mutation": 1.0,
    "propagation": 0.0,
    "observability_bias": 0.0,
    "topology_context": 0.0
  }
}
```

另一个例子：

```json
{
  "mechanism": "dependency slowdown",
  "description": "A downstream dependency becomes slow, causing latency inflation in callers.",
  "observable_consequences": [
    "trace duration increases",
    "self duration ratio changes",
    "request queue or retry count increases"
  ],
  "allowed_atoms": [
    "duration_shift",
    "count_rise",
    "delta"
  ],
  "role_prior": {
    "mutation": 0.0,
    "propagation": 1.0,
    "observability_bias": 0.0,
    "topology_context": 0.0
  }
}
```

你可以先手写 8–10 个通用 mechanism cards，然后再让 LLM 根据代码和文档扩展。这会比“完全让 LLM 想 feature”安全得多。

建议第一版机制表：

| Mechanism | 可观测后果 | 主要 role |
| --- | --- | --- |
| resource saturation | CPU/memory/IO/network shift | mutation/local |
| service hang/crash | count drop, no response, missing traces | mutation |
| interface failure | error rate/status code shift | mutation |
| endpoint behavior change | endpoint distribution shift | mutation |
| dependency slowdown | duration/latency inflation | propagation |
| retry/backpressure | trace count rise, log burst | propagation |
| traffic surge | request count rise, upstream fan-out | propagation/local |
| software event shift | log template distribution change | mutation/propagation |
| observability skew | abnormal rows/count volume high | neutral/local |
| topology exposure | high in/out degree | neutral/local |

---

# 6. Stage 4: DSL 设计

DSL 的作用是限制 LLM 的创造空间。LLM 不能随便说“计算一个复杂语义分数”，它只能在 DSL 里组合。

## 6.1 DSL 的核心抽象

一个 evidence operator 可以写成：

[

E = Aggregate_{entity}(Compare(Transform(Signal), normal, abnormal))

]

也就是：

```
signal → transform → normal/abnormal contrast → aggregation → role
```

## 6.2 JSON DSL schema

建议定义成这样：

```json
{
  "name": "string",
  "version": "string",
  "source": "metric | log | trace | topology",
  "entity": "service | endpoint | edge | log_template | status_code",
  "selector": {
    "field": "string",
    "op": "exists | eq | contains | regex | in",
    "value": "string | list | null"
  },
  "signal": {
    "field": "string",
    "type": "value | count | rate | duration | distribution | categorical"
  },
  "transform": "none | abs | log1p | templateize | normalize_by_count",
  "contrast": {
    "operator": "z_shift | robust_z_shift | mean_delta | count_delta | count_rise | count_drop | rate_delta | distribution_shift | novelty",
    "normal_window": "pre_anomaly",
    "abnormal_window": "post_anomaly"
  },
  "aggregation": {
    "level": "service | endpoint | edge",
    "method": "max | mean | sum | p95 | ratio | jsd"
  },
  "role_prior": {
    "mutation": 0.0,
    "propagation": 0.0,
    "observability_bias": 0.0,
    "topology_context": 0.0
  },
  "guards": {
    "min_normal_points": 5,
    "min_abnormal_points": 1,
    "zero_division": "return_zero",
    "clip": 3.0
  },
  "required_fields": ["timestamp", "service_name"],
  "mechanism": "string",
  "rationale": "string"
}
```

## 6.3 DSL atoms

第一版只需要这些 atoms：

### Magnitude shift

```
z_shift
robust_z_shift
mean_delta
value_delta
```

用于 metric value、duration、latency。

### Frequency shift

```
count_delta
count_rise
count_drop
```

用于 trace count、log count、metric rows。

### Rate shift

```
rate_delta
error_rate_delta
timeout_rate_delta
```

用于 error logs、status code、failed spans。

### Distribution shift

```
distribution_shift
endpoint_shift
status_code_shift
template_shift
```

用 Jensen-Shannon divergence、total variation distance 或 chi-square distance。

### Novelty

```
novelty
new_template_rate
new_status_code_rate
```

用于 abnormal window 出现 normal window 没有的模板、状态码、endpoint。

### Topology context

```
in_degree
out_degree
edge_activity
parent_context
```

用于结构上下文，不直接当 root cause。

---

# 7. 关键 operator 具体怎么实现

下面是最小实现版本。

## 7.1 `z_shift`

适合 metrics 或 latency。

```python
def z_shift(normal: pd.Series, abnormal: pd.Series, eps: float = 1e-9) -> float:
    mu = normal.mean()
    sigma = normal.std()
    if not np.isfinite(sigma) or sigma < eps:
        return 0.0
    z = np.abs((abnormal - mu) / (sigma + eps))
    return float(np.nanmax(z)) if len(z) else 0.0
```

## 7.2 `robust_z_shift`

适合异常检测时间不准的场景。

```python
def robust_z_shift(normal: pd.Series, abnormal: pd.Series, eps: float = 1e-9) -> float:
    med = normal.median()
    iqr = normal.quantile(0.75) - normal.quantile(0.25)
    if not np.isfinite(iqr) or iqr < eps:
        return 0.0
    score = np.abs((abnormal - med) / (iqr + eps))
    return float(np.nanmax(score)) if len(score) else 0.0
```

## 7.3 `count_delta`

适合 logs、traces、metric rows。

```python
def count_delta(normal_count: float, abnormal_count: float, eps: float = 1e-9) -> float:
    return abs(abnormal_count - normal_count) / (normal_count + eps)
```

## 7.4 `count_rise`

```python
def count_rise(normal_count: float, abnormal_count: float, eps: float = 1e-9) -> float:
    return max(0.0, abnormal_count - normal_count) / (normal_count + eps)
```

## 7.5 `count_drop`

```python
def count_drop(normal_count: float, abnormal_count: float, eps: float = 1e-9) -> float:
    return max(0.0, normal_count - abnormal_count) / (normal_count + eps)
```

## 7.6 `rate_delta`

适合 error rate、status code rate。

```python
def rate_delta(normal_num, normal_den, abnormal_num, abnormal_den, eps=1e-9) -> float:
    r0 = normal_num / (normal_den + eps)
    r1 = abnormal_num / (abnormal_den + eps)
    return abs(r1 - r0)
```

## 7.7 `distribution_shift`

适合 endpoint/status/log-template 分布。

```python
def js_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    p = p.astype(float)
    q = q.astype(float)
    p = p / (p.sum() + eps)
    q = q / (q.sum() + eps)
    m = 0.5 * (p + q)

    def kl(a, b):
        mask = a > eps
        return float(np.sum(a[mask] * np.log((a[mask] + eps) / (b[mask] + eps))))

    return 0.5 * kl(p, m) + 0.5 * kl(q, m)
```

---

# 8. Stage 5: LLM Operator Synthesizer

LLM 的任务不是输出代码，而是输出 DSL spec。

当前实现把这一阶段做成 config-driven offline pipeline。默认配置使用 mock client，
因此不会调用真实 LLM；真实 provider 只在用户显式修改 config 并传入
`--allow-real-llm` 后启用。

配置文件：

```text
algorithms/evidencerank/src/evidencerank/meo/llm/config.yaml
```

默认：

```yaml
synthesis:
  mode: mock
  allow_real_llm: false
llm:
  provider: mock
```

mock 输出和 mock prompt context 统一放在：

```text
algorithms/evidencerank/src/evidencerank/meo/llm/mock_outputs.py
```

离线 synthesis CLI：

```bash
uv run --package evidencerank python -m meo.llm.synthesize \
  --mock \
  --output /tmp/default_meol.json
```

该命令仍然会构建真实 prompt 形状，并执行 static / leakage verifier，只是 LLM
response 由固定的 `mock_meol()` 代替。这样 Phase-1 可以先把整体流程跑通，后续只需
替换 config 中的 provider/model，就可以进入真实 LLM synthesis 实验。

## 8.1 Prompt 输入

给 LLM 四类信息：

```
1. Artifact summary
2. Mechanism cards
3. DSL grammar
4. Safety rules
```

示例 prompt：

```
You are an expert SRE and telemetry feature designer.

Your task is to synthesize candidate evidence operators for microservice RCA.
You must only use the allowed DSL atoms. You must not use root-cause labels,
fault injection labels, case IDs, or baseline outcomes.

Input:
- Service artifact summary:
{artifact_summary}

- Available telemetry schema:
{telemetry_schema}

- Mechanism cards:
{mechanism_cards}

- Allowed DSL atoms:
{dsl_atoms}

Rules:
1. Each operator must be computable from normal and abnormal telemetry windows.
2. Each operator must be service-level or edge-level aggregatable.
3. Do not create operators that depend on a specific service name.
4. Do not use ground-truth root cause labels or fault types.
5. Assign role_prior as counterfactual membership: mutation, propagation, or neutral.
6. Output valid JSON only.

Output:
{
  "operators": [
    {
      "name": "...",
      "source": "...",
      "entity": "...",
      "signal": {...},
      "contrast": {...},
      "aggregation": {...},
      "role_prior": {...},
      "mechanism": "...",
      "rationale": "...",
      "required_fields": [...]
    }
  ]
}
```

## 8.2 LLM 输出例子

```json
{
  "operators": [
    {
      "name": "trace_endpoint_distribution_shift",
      "source": "trace",
      "entity": "service",
      "signal": {
        "field": "endpoint",
        "type": "categorical"
      },
      "contrast": {
        "operator": "distribution_shift",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      },
      "aggregation": {
        "level": "service",
        "method": "jsd"
      },
      "role_prior": {
        "mutation": 1.0,
        "propagation": 0.0,
        "observability_bias": 0.0,
        "topology_context": 0.0
      },
      "mechanism": "endpoint behavior change",
      "required_fields": ["timestamp", "service_name", "endpoint"],
      "rationale": "A service whose endpoint mix changes after anomaly onset may have changed behavior at its interface."
    }
  ]
}
```

---

# 9. Stage 6: Verifier

Verifier 是防止 LLM 胡编和数据泄露的关键。

## 9.1 Static verifier

检查：

```
JSON schema 是否合法
operator 是否在 DSL allowlist
required_fields 是否存在
role_prior 是否是 mutation / propagation / neutral 的互斥 membership
是否包含 forbidden fields
是否包含 service-specific literal
是否依赖 root cause label / fault type / case id
是否有 rationale 和 mechanism
```

示例：

```python
FORBIDDEN_FIELDS = {
    "root_cause",
    "root_service",
    "fault_type",
    "injection_type",
    "label",
    "rank",
    "answer",
    "ground_truth",
}

ALLOWED_OPERATORS = {
    "z_shift",
    "robust_z_shift",
    "mean_delta",
    "count_delta",
    "count_rise",
    "count_drop",
    "rate_delta",
    "distribution_shift",
    "novelty",
    "in_degree",
    "out_degree",
}
```

```python
def static_verify(spec: dict, telemetry_columns: set[str]) -> tuple[bool, list[str]]:
    errors = []

    if spec["contrast"]["operator"] not in ALLOWED_OPERATORS:
        errors.append("operator_not_allowed")

    for field in spec.get("required_fields", []):
        if field not in telemetry_columns:
            errors.append(f"missing_field:{field}")

    serialized = json.dumps(spec).lower()
    for forbidden in FORBIDDEN_FIELDS:
        if forbidden in serialized:
            errors.append(f"forbidden_token:{forbidden}")

    role = spec.get("role_prior", {})
    mutation = float(role.get("mutation", 0.0))
    propagation = float(role.get("propagation", 0.0))
    if mutation not in {0.0, 1.0} or propagation not in {0.0, 1.0}:
        errors.append("role_prior_not_binary")
    if mutation > 0.0 and propagation > 0.0:
        errors.append("role_prior_ambiguous")
    if any(float(v) < 0 or float(v) > 1 for v in role.values()):
        errors.append("role_prior_out_of_range")

    return len(errors) == 0, errors
```

## 9.2 Dynamic verifier

在无标签 telemetry 上跑 smoke test：

```
是否能正常计算
是否全 NaN
是否全 0
是否全常数
是否极端稀疏
是否和已有 operator 完全重复
是否只在某一个服务名上有值
是否 runtime 太慢
```

示例：

```python
def dynamic_verify(
    spec: dict,
    compiler,
    sample_frames: dict[str, pd.DataFrame],
    services: list[str],
) -> tuple[bool, dict]:
    fn = compiler.compile(spec)
    values = fn(sample_frames, services)

    stats = {
        "nan_rate": float(np.isnan(values).mean()),
        "nonzero_rate": float((values > 0).mean()),
        "variance": float(np.nanvar(values)),
        "max": float(np.nanmax(values)) if len(values) else 0.0,
    }

    ok = True
    if stats["nan_rate"] > 0.1:
        ok = False
    if stats["nonzero_rate"] == 0.0:
        ok = False
    if stats["variance"] <= 1e-12:
        ok = False

    return ok, stats
```

## 9.3 Leakage verifier

这个非常重要。你可以单独写一个 verifier：

```python
def leakage_verify(spec: dict) -> tuple[bool, list[str]]:
    text = json.dumps(spec).lower()
    forbidden = [
        "root", "ground_truth", "fault_type", "injection",
        "cpu_hog", "memory_leak", "packet_loss", "answer",
        "rank", "torai_wrong", "baseline"
    ]
    hits = [w for w in forbidden if w in text]
    return len(hits) == 0, hits
```

注意：如果你确实想让 LLM 知道 benchmark 的 fault type list，例如 CPU、MEM、DELAY、LOSS，要把它放在 **generic mechanism catalog**，不要作为某个 case 的输入。更保险的做法是主实验不用 fault type list，附录做 “with fault-type catalog” 的对比。

---

# 10. Stage 7: DSL Compiler

Compiler 的作用是把 DSL spec 编译成一个 Python callable：

```python
feature_fn(frames, services) -> np.ndarray
```

其中：

```python
frames = {
    "normal_metrics": pd.DataFrame,
    "abnormal_metrics": pd.DataFrame,
    "normal_logs": pd.DataFrame,
    "abnormal_logs": pd.DataFrame,
    "normal_traces": pd.DataFrame,
    "abnormal_traces": pd.DataFrame,
}
```

输出：

```python
np.ndarray shape = [num_services]
```

## 10.1 Compiler 架构

```python
class EvidenceCompiler:
    def __init__(self, operator_registry):
        self.registry = operator_registry

    def compile(self, spec: dict):
        source = spec["source"]
        op = spec["contrast"]["operator"]

        if source == "metric":
            return self._compile_metric(spec)
        if source == "log":
            return self._compile_log(spec)
        if source == "trace":
            return self._compile_trace(spec)
        if source == "topology":
            return self._compile_topology(spec)

        raise ValueError(f"Unsupported source: {source}")
```

## 10.2 Trace compiler example

```python
def compile_trace_distribution_shift(spec):
    field = spec["signal"]["field"]

    def feature(frames, services):
        normal = frames.get("normal_traces", pd.DataFrame())
        abnormal = frames.get("abnormal_traces", pd.DataFrame())
        out = []

        for svc in services:
            n = normal[normal["service_name"] == svc]
            a = abnormal[abnormal["service_name"] == svc]

            cats = sorted(set(n[field].dropna()) | set(a[field].dropna()))
            if not cats:
                out.append(0.0)
                continue

            p = np.array([(n[field] == c).sum() for c in cats], dtype=float)
            q = np.array([(a[field] == c).sum() for c in cats], dtype=float)
            out.append(js_divergence(p, q))

        return np.asarray(out, dtype=float)

    return feature
```

## 10.3 Metric compiler example

```python
def compile_metric_z_shift(spec):
    metric_name = spec["signal"]["field"]

    def feature(frames, services):
        normal = frames.get("normal_metrics", pd.DataFrame())
        abnormal = frames.get("abnormal_metrics", pd.DataFrame())
        out = []

        for svc in services:
            col = f"{svc}_{metric_name}"
            if col not in normal.columns or col not in abnormal.columns:
                out.append(0.0)
                continue

            out.append(z_shift(normal[col].dropna(), abnormal[col].dropna()))

        return np.asarray(out, dtype=float)

    return feature
```

## 10.4 Log compiler example

```python
def compile_log_template_delta(spec):
    template_field = spec["signal"].get("field", "template")

    def feature(frames, services):
        normal = frames.get("normal_logs", pd.DataFrame())
        abnormal = frames.get("abnormal_logs", pd.DataFrame())
        out = []

        for svc in services:
            n = normal[normal["service_name"] == svc]
            a = abnormal[abnormal["service_name"] == svc]

            n_counts = n[template_field].value_counts()
            a_counts = a[template_field].value_counts()

            templates = sorted(set(n_counts.index) | set(a_counts.index))
            if not templates:
                out.append(0.0)
                continue

            p = np.array([n_counts.get(t, 0) for t in templates], dtype=float)
            q = np.array([a_counts.get(t, 0) for t in templates], dtype=float)
            out.append(js_divergence(p, q))

        return np.asarray(out, dtype=float)

    return feature
```

---

# 11. MEOL 文件格式

MEO 最终产出一个 `meol.json` 或 `meol.yaml`。

```json
{
  "library_name": "MEOL-online-boutique-v1",
  "created_at": "2026-06-10",
  "generator": {
    "llm": "gpt-...",
    "prompt_version": "meo_prompt_v1",
    "dsl_version": "dsl_v1"
  },
  "artifact_hashes": {
    "source": "sha256:...",
    "telemetry_schema": "sha256:...",
    "docs": "sha256:..."
  },
  "leakage_policy": {
    "uses_ground_truth": false,
    "uses_case_fault_type": false,
    "uses_baseline_outputs": false
  },
  "operators": [
    {
      "name": "trace_status_code_shift",
      "source": "trace",
      "entity": "service",
      "signal": {"field": "status_code", "type": "categorical"},
      "contrast": {"operator": "distribution_shift"},
      "aggregation": {"level": "service", "method": "jsd"},
      "role_prior": {
        "mutation": 0.85,
        "propagation": 0.10,
        "observability_bias": 0.05,
        "topology_context": 0.0
      },
      "mechanism": "interface failure",
      "required_fields": ["timestamp", "service_name", "status_code"],
      "rationale": "..."
    }
  ]
}
```

一定要保存：

```
artifact hashes
prompt version
DSL version
LLM model version
accepted/rejected specs
verifier logs
```

这样你论文里可以说：

> The operator library is frozen before evaluation and fully reproducible from the released artifacts.
> 

---

# 12. Runtime: 如何接到 CREST

你现在的 CREST pipeline 大概是：

```python
matrix, trace_edges = _build_feature_matrix(...)
case_matrix = _robust_case_feature_matrix(matrix)
role_matrix = _apply_arc_trace_endpoint_support_gate(...)
local_energy = _local_family_energy(...)
...
score = local_abnormality * explanatory_power + denoised_support
```

现在改成：

```python
meol = load_meol("meol.json")
compiled_ops = [compiler.compile(spec) for spec in meol.operators]

E = []
for op in compiled_ops:
    E.append(op(frames, services))

feature_matrix = np.stack(E, axis=1)
mutation_features, propagation_features = read_counterfactual_membership(meol)
```

其中：

```python
mutation_features = {op.name for op in meol.operators if op.role_prior["mutation"] > 0}
propagation_features = {op.name for op in meol.operators if op.role_prior["propagation"] > 0}
```

然后：

```python
local_energy = crest_local_family_energy(feature_matrix, feature_names)
structural_energy = apply_parent_context(local_energy, trace_edges)
structural_energy = apply_counterfactual_explain_away(
    structural_energy,
    feature_matrix,
    feature_names,
    mutation_features=mutation_features,
    propagation_features=propagation_features,
)
```

你的 `_apply_counterfactual_explain_away_once` 里现在是通过 feature name 找 mutation / propagation indices。

改成 soft role 后，可以直接传入 `mutation` 和 `propagation`：

```python
def apply_counterfactual_explain_away_soft(
    services,
    structural_energy,
    mutation,
    propagation,
    trace_edges,
):
    ...
```

核心逻辑保持不变：

```python
mutation_excess = max(0.0, mutation[root] - mutation[victim])
propagation_excess = max(0.0, propagation[victim] - propagation[root])
transfer = (adjusted[victim] - adjusted[root]) * mutation_share * propagation_share
```

你当前实现已经有这个思想：当 candidate root 的 mutation evidence 更强、victim 的 propagation evidence 更强时，把 victim 的部分能量转回 root。

---

# 13. 一个完整的最小实现目录

建议工程结构：

```
crest_meo/
  artifacts/
    miner.py
    source_parser.py
    schema_parser.py
    trace_parser.py
    log_parser.py

  dsl/
    schema.py
    atoms.py
    registry.py
    compiler.py

  llm/
    prompts/
      operator_synthesis_v1.txt
      semantic_extraction_v1.txt
    synthesize.py
    parse_output.py

  verify/
    static_verifier.py
    dynamic_verifier.py
    leakage_verifier.py
    redundancy_verifier.py

  library/
    meol.online_boutique.v1.json
    meol.sock_shop.v1.json
    meol.train_ticket.v1.json

  runtime/
    instantiate.py
    crest_adapter.py
```

---

# 14. 伪代码：离线构建 MEOL

```python
def build_meol(
    source_dir,
    deploy_dir,
    docs_dir,
    telemetry_schema,
    mechanism_catalog,
    dsl_grammar,
    sample_unlabeled_frames,
):
    artifacts = mine_artifacts(
        source_dir=source_dir,
        deploy_dir=deploy_dir,
        docs_dir=docs_dir,
        telemetry_schema=telemetry_schema,
    )

    semantic_cards = llm_extract_operational_semantics(
        artifacts=artifacts,
        mechanism_catalog=mechanism_catalog,
    )

    raw_specs = llm_synthesize_operator_specs(
        semantic_cards=semantic_cards,
        telemetry_schema=telemetry_schema,
        mechanism_catalog=mechanism_catalog,
        dsl_grammar=dsl_grammar,
    )

    accepted = []
    rejected = []

    for spec in raw_specs:
        ok, errors = static_verify(spec, telemetry_schema.columns)
        if not ok:
            rejected.append((spec, errors))
            continue

        ok, errors = leakage_verify(spec)
        if not ok:
            rejected.append((spec, errors))
            continue

        fn = compiler.compile(spec)

        ok, stats = dynamic_verify(
            spec=spec,
            compiler=compiler,
            sample_frames=sample_unlabeled_frames,
            services=artifacts.services,
        )
        if not ok:
            rejected.append((spec, stats))
            continue

        accepted.append(spec)

    accepted = deduplicate_specs(accepted)
    accepted = validate_role_membership(accepted)

    meol = freeze_library(
        specs=accepted,
        artifacts=artifacts,
        prompt_version="meo_v1",
        dsl_version="dsl_v1",
    )

    return meol, rejected
```

---

# 15. 伪代码：在线使用 MEOL

```python
def compute_meo_feature_matrix(frames, services, meol):
    compiled = [compiler.compile(spec) for spec in meol["operators"]]

    values = []
    names = []
    mutation_features = set()
    propagation_features = set()

    for spec, fn in zip(meol["operators"], compiled):
        v = fn(frames, services)
        values.append(v)
        names.append(spec["name"])
        if spec["role_prior"].get("mutation", 0.0) > 0:
            mutation_features.add(spec["name"])
        if spec["role_prior"].get("propagation", 0.0) > 0:
            propagation_features.add(spec["name"])

    feature_matrix = np.stack(values, axis=1)

    return feature_matrix, names, mutation_features, propagation_features
```

然后接 CREST：

```python
feature_matrix, feature_names, mutation_features, propagation_features = compute_meo_feature_matrix(
    frames,
    services,
    meol,
)

feature_matrix = robust_case_scale(feature_matrix)
local_abnormality = crest_local_family_energy(feature_matrix, feature_names)

structural_energy = crest_parent_context(local_abnormality, trace_edges)
structural_energy = crest_counterfactual_explain_away(
    structural_energy,
    feature_matrix,
    feature_names,
    mutation_features=mutation_features,
    propagation_features=propagation_features,
)
propagation = feature_matrix @ W[:, 1]
bias = feature_matrix @ W[:, 2]
topology = feature_matrix @ W[:, 3]

local_abnormality = saturating_scale(
    mutation + propagation + bias + topology
)

explanatory_power = compute_counterfactual_explanatory_power(
    local_abnormality=local_abnormality,
    mutation=mutation,
    propagation=propagation,
    graph=trace_graph,
)

score = local_abnormality * explanatory_power
```

---

# 16. 如何避免“benchmark hacking”质疑

你需要在 paper 里明确四条规则。

## Rule 1: LLM 只看部署前可见的信息

允许：

```
source code
instrumentation code
telemetry schema
deployment topology
README/docs/runbooks
generic mechanism catalog
```

不允许：

```
test case root cause
test case fault type
test case rank result
baseline output
which case TORAI fails
```

## Rule 2: Operator library 在评估前冻结

你要保存：

```
meol.json
prompt
artifact hash
verifier logs
generation timestamp
```

## Rule 3: 主结果用 label-free MEOL

GT 只能用于最终 evaluation。不能用 GT 调 role weight。

## Rule 4: 做 leave-system-out

例如：

```
用 Online Boutique + Sock Shop 的 artifacts 构建通用 MEOL；
在 Train Ticket 上测试。
```

或者：

```
只给 Train Ticket 的 schema，不给 Train Ticket 的 incidents。
```

这能证明 MEO 不是看 test results 调出来的。

---

# 17. 实验设计

你至少要有一个专门 RQ：

## RQ-MEO: Does MEO produce useful evidence operators?

比较这些版本：

| Variant | 说明 |
| --- | --- |
| CREST-Hand | 你现在手写 features |
| CREST-MEO | LLM + DSL + verifier |
| CREST-MEO w/o code | 不给源码，只给 telemetry schema |
| CREST-MEO w/o instrumentation | 不给插桩点 |
| CREST-MEO w/o verifier | LLM spec 直接用 |
| CREST-DSL-All | DSL 所有可组合 operators 全用 |
| CREST-DSL-Random | 随机生成同等数量 operators |
| CREST-SwapRole | mutation / propagation role 对调 |
| LLM-direct RCA | LLM 直接输出 root cause |

你希望看到：

```
CREST-MEO >= CREST-Hand
CREST-MEO > CREST-DSL-All
CREST-MEO > CREST-DSL-Random
CREST-MEO > CREST-MEO w/o verifier
CREST-SwapRole 明显下降
LLM-direct RCA 慢且不稳定
```

这就能证明：

1. MEO 不是随便生成 feature；
2. DSL 限制有用；
3. verifier 有用；
4. mutation / propagation role 真的重要；
5. LLM 不应该直接做 RCA，而应该做 evidence synthesis。

---

# 18. 论文里的包装方式

你可以把 MEO 写成 CREST 的第一个模块：

```
3.1 MEO: Mechanism-grounded Evidence Operator Synthesis
3.1.1 Code and Observability Artifact Mining
3.1.2 Mechanism Cards
3.1.3 Evidence Operator DSL
3.1.4 LLM-guided Operator Synthesis
3.1.5 Deterministic Verification and Compilation
3.2 Counterfactual Evidence Ranking
3.3 Residual Explanatory Diagnostics
```

核心 claim：

> MEO converts operational semantics into executable evidence operators. Unlike prior work that either manually defines telemetry features or asks LLMs to directly diagnose incidents, MEO uses LLMs only for offline, DSL-constrained evidence synthesis. The generated operators are verified, compiled, and frozen before evaluation.
> 

MetaRCA 可以作为非常好的相关工作对照：它证明了“LLM 离线构建可复用知识，在线轻量推理”是一个可被 FSE 接受的路线；你的差异是 MetaRCA 构建的是 metadata-level causal graph，而 MEO 构建的是 metadata-level evidence operator library。

---

# 19. 最小可实现版本

第一版不要做太复杂。你可以先实现下面 10 个 DSL operators：

```
metric_z_shift
metric_robust_z_shift
metric_count_drop
trace_duration_shift
trace_count_rise
trace_count_drop
trace_status_code_shift
trace_endpoint_shift
log_count_delta
log_template_shift
```

这 10 个已经基本覆盖你现在 CREST 的手工 features。然后让 MEO 生成这些 operator specs，并通过 compiler 计算出同样或更丰富的 feature matrix。你现在 CREST 里已经有 metric、trace、log、topology、mutation、propagation、observability volume 这些 role families；MEO 的第一步就是把这些从 hard-coded constants 升级为 MEOL。

当前实现里需要区分两个 MEOL 文件：

```text
algorithms/evidencerank/src/evidencerank/meo/library/default_meol.json
algorithms/evidencerank/src/evidencerank/meo/library/crest_builtin_meol.json
```

`default_meol.json` 是 mock LLM 生成路径的默认输出，内容来自
`meo/llm/mock_outputs.py`，用于模拟未来真实 LLM 会生成的一组机制化 operator
spec。它不是从 CREST 常量自动转换出来的。

`crest_builtin_meol.json` 则是从当前 CREST/CERA 源码机械导出的对照库：

```bash
uv run --package evidencerank python VibeResearchTools/export_crest_builtin_meol.py
```

这个文件包含完整 21 个 `BASE_FEATURE_NAMES`，并把
`CREST_COUNTERFACTUAL_MUTATION_FEATURES`、`CREST_COUNTERFACTUAL_PROPAGATION_FEATURES`
分别转换为 one-hot `mutation` / `propagation` role prior；其余 feature 转成
neutral，也就是 mutation/propagation 都为 0。neutral feature 仍参与 CREST local
energy 和 denoised support，只是不参与 counterfactual mutation/propagation 对比。
因此它适合用来检查“当前 hard-coded CREST roles 被 JSON MEOL 表达出来以后是否覆盖
同一批 feature 和 counterfactual sets”。当前 CREST-MEO 在线路径已经复刻原 CREST
scoring，所以 `crest_meo_builtin` 应与 `crest` 在 ranking、`A/F/S/score` 和 benchmark
指标上等价。

等第一版跑通后，再加：

```
edge_latency_shift
edge_error_rate_delta
new_log_template_rate
new_endpoint_rate
self_duration_ratio_shift
parent_context_shift
```

---

# 20. 最终建议

你可以把 MEO 的 novelty 定义成：

> **MEO is a code-and-observability-grounded evidence synthesis module that transforms operational knowledge into executable telemetry evidence operators through a DSL-constrained LLM and deterministic compiler.**
> 

它解决的不是“如何让 LLM 找 root cause”，而是：

> **如何系统性、可复现、无标签地构造 RCA evidence features。**
> 

这会让你的 CREST 从“一个特征打分算法”升级成：

```
MEO: 生成可解释 evidence operators
CREST: 用 counterfactual topology 排序 root cause
Residual: 处理结构解释不足的场景
```

这条路线比单纯说“我手工设计了 mutation features 和 propagation features”强很多，也比“我加了 LLM 直接做 RCA”更容易被审稿人接受。
