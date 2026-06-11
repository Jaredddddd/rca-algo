# CREST-MEO 设计修改文档：在现有 CREST 中加入 Mechanism-grounded Evidence Operator Synthesis

## 0. 目标

当前 CREST 的核心逻辑已经具备较强的 RCA 排序能力：它从 telemetry 中构建 feature matrix，将特征划分为 metric shift、trace mutation、trace propagation、log shift、observability volume、topology context 等 role families，然后基于 local abnormality、structural support、counterfactual explain-away 和 residual explanatory power 进行服务级 RCA 排名。

但当前实现存在一个明显研究风险：`CREST_ROLE_FAMILIES`、`CREST_COUNTERFACTUAL_MUTATION_FEATURES` 和 `CREST_COUNTERFACTUAL_PROPAGATION_FEATURES` 是硬编码的。审稿人可能质疑这些特征集合是否是人工调参、benchmark hacking、或者依赖特定数据集命名习惯。

本次修改目标是引入一个离线模块：

**MEO: Mechanism-grounded Evidence Operator Synthesis**

MEO 的作用不是让 LLM 在线做 RCA，也不是让 LLM 直接输出 root cause，而是让 LLM 在离线阶段基于源码、插桩点、telemetry schema、部署文件、运维语义和一个受限 DSL，生成一套可验证、可编译、可复现的 evidence operators。然后 CREST 在线阶段使用这些 operators 计算 feature matrix，并继续执行确定性的 counterfactual ranking。

最终系统名称建议为：

**CREST-MEO: Counterfactual Ranking with Mechanism-grounded Evidence Operators**

---

## 1. 当前代码问题与修改方向

### 1.1 当前代码中的核心硬编码点

当前 CREST 中存在如下设计：

```python
CREST_ROLE_FAMILIES = {
    "metric_shift": (...),
    "trace_mutation": (...),
    "trace_propagation": (...),
    "log_shift": (...),
    "observability_volume": (...),
    "topology_context": (...),
}

CREST_COUNTERFACTUAL_MUTATION_FEATURES = frozenset({...})

CREST_COUNTERFACTUAL_PROPAGATION_FEATURES = frozenset({...})
```

这些集合之后被 `_family_burdens`、`_local_family_energy`、`_apply_counterfactual_explain_away_once`、`_crest_residual_diagnostics` 等模块使用。

当前逻辑等价于：

1. 先由 `_build_feature_matrix` 构建固定 feature matrix。
2. 再用硬编码 feature names 找到 mutation / propagation features。
3. 再根据 mutation excess 和 propagation excess 做 explain-away。
4. 最后输出服务级排名。

### 1.2 修改后的目标逻辑

修改后，不再把 feature role 写死在 Python 常量中，而是引入一个外部可冻结的 operator library：

```text
MEOL: Meta Evidence Operator Library
```

MEOL 是一个 JSON 文件，里面每个 operator 都描述：

1. 这个 operator 从哪种 telemetry 中计算。
2. 使用哪个字段。
3. 使用哪个 normal-vs-abnormal contrast atom。
4. 如何按 service 聚合。
5. 它更像 mutation、propagation、observability bias，还是 topology context。
6. 其运维机制和 rationale 是什么。
7. 需要哪些字段。
8. 是否通过 verifier。

运行时流程变成：

```text
MEOL JSON
  ↓
DSL Compiler
  ↓
compiled feature functions
  ↓
run on existing normal/abnormal telemetry
  ↓
feature_matrix: services × operators
  ↓
role_weight_matrix: operators × roles
  ↓
mutation / propagation / bias / topology vectors
  ↓
CREST counterfactual ranking
```

---

## 2. 核心概念解释

### 2.1 Evidence Operator 是什么

Evidence operator 是一条“如何从已有 telemetry 中计算 RCA 证据分数”的规则。

例如：

```text
trace_status_code_shift
```

它并不是原始 telemetry 里已有的字段，而是一个计算规则：

```text
对每个 service：
    读取 normal traces 中的 status_code 分布
    读取 abnormal traces 中的 status_code 分布
    计算两个分布的变化程度
    输出一个 service-level score
```

数学上：

```text
E_f(s_i) = Operator_f(Telemetry_normal, Telemetry_abnormal, s_i)
```

其中：

* `f` 是 operator 名称；
* `s_i` 是服务；
* `E_f(s_i)` 是服务在该证据维度上的分数。

如果系统有 N 个服务、K 个 evidence operators，则输出矩阵为：

```text
N × K feature matrix
```

这个矩阵就是 CREST 后续 ranking 的输入。

### 2.2 DSL 是什么

DSL 是用于描述 evidence operator 的结构化语言。它的作用是限制 LLM 的自由度，让 LLM 不能直接写 Python，也不能自由发明不可计算的特征。

LLM 只能输出类似下面的 JSON spec：

```json
{
  "name": "trace_status_code_shift",
  "source": "trace",
  "entity": "service",
  "signal": {
    "field": "status_code",
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
    "mutation": 0.85,
    "propagation": 0.10,
    "observability_bias": 0.05,
    "topology_context": 0.00
  },
  "mechanism": "interface failure",
  "required_fields": ["timestamp", "service_name", "status_code"],
  "rationale": "A status-code distribution shift indicates a service-level interface failure mode."
}
```

这个 JSON 本身不执行计算。它只是一个 operator specification。之后由 compiler 将其编译成 Python 函数。

### 2.3 Compiler 是什么

Compiler 的作用是把 DSL spec 变成一个可执行函数：

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

即每个服务一个分数。

---

## 3. 新增目录结构

建议在现有算法目录下新增如下结构：

```text
crest_meo/
  dsl/
    __init__.py
    schema.py
    atoms.py
    compiler.py
    registry.py

  verify/
    __init__.py
    static_verifier.py
    dynamic_verifier.py
    leakage_verifier.py
    redundancy_verifier.py

  llm/
    __init__.py
    prompts.py
    mock_outputs.py
    synthesize.py

  library/
    default_meol.json
    meol_schema.json

  runtime/
    __init__.py
    load_meol.py
    instantiate.py
    crest_adapter.py

  artifacts/
    __init__.py
    schema_miner.py
    code_miner.py
    telemetry_schema.py
```

如果目前项目结构不适合单独建 `crest_meo/`，也可以放在现有算法包内部，例如：

```text
algorithms/
  crest.py
  cera.py
  meo/
    dsl/
    verify/
    llm/
    library/
    runtime/
```

优先保持最少侵入。第一版可以只实现：

```text
meo/dsl/schema.py
meo/dsl/atoms.py
meo/dsl/compiler.py
meo/runtime/load_meol.py
meo/runtime/instantiate.py
meo/library/default_meol.json
```

LLM 生成先 mock。

---

## 4. MEOL 文件格式

新增一个默认 library 文件：

```text
meo/library/default_meol.json
```

第一版可以直接写入 mock LLM 生成的 operators。

示例：

```json
{
  "library_name": "crest-meol-default-v1",
  "dsl_version": "1.0",
  "generator": {
    "type": "mock_llm",
    "prompt_version": "meo_operator_synthesis_v1",
    "uses_ground_truth": false,
    "uses_case_fault_type": false,
    "uses_baseline_outputs": false
  },
  "roles": [
    "mutation",
    "propagation",
    "observability_bias",
    "topology_context"
  ],
  "operators": [
    {
      "name": "metric_max_z",
      "source": "metric",
      "entity": "service",
      "signal": {
        "field": "*",
        "type": "value"
      },
      "contrast": {
        "operator": "z_shift",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      },
      "aggregation": {
        "level": "service",
        "method": "max"
      },
      "role_prior": {
        "mutation": 0.45,
        "propagation": 0.30,
        "observability_bias": 0.15,
        "topology_context": 0.10
      },
      "mechanism": "resource or performance magnitude shift",
      "required_fields": ["time"],
      "rationale": "A large metric z-score indicates a service-local state deviation, but can also be affected by propagated symptoms."
    },
    {
      "name": "metric_count_drop_shift",
      "source": "metric",
      "entity": "service",
      "signal": {
        "field": "__row_count__",
        "type": "count"
      },
      "contrast": {
        "operator": "count_drop",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      },
      "aggregation": {
        "level": "service",
        "method": "ratio"
      },
      "role_prior": {
        "mutation": 0.75,
        "propagation": 0.10,
        "observability_bias": 0.15,
        "topology_context": 0.00
      },
      "mechanism": "service hang or telemetry disappearance",
      "required_fields": ["time"],
      "rationale": "A sharp drop in service-level metric observations may indicate that the service stopped processing or reporting."
    },
    {
      "name": "trace_status_code_shift",
      "source": "trace",
      "entity": "service",
      "signal": {
        "field": "status_code",
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
        "mutation": 0.85,
        "propagation": 0.10,
        "observability_bias": 0.05,
        "topology_context": 0.00
      },
      "mechanism": "interface failure",
      "required_fields": ["service_name", "status_code"],
      "rationale": "A status-code distribution shift indicates a service-level interface failure mode."
    },
    {
      "name": "trace_error_rate",
      "source": "trace",
      "entity": "service",
      "signal": {
        "field": "status_code",
        "type": "rate"
      },
      "contrast": {
        "operator": "error_rate_delta",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      },
      "aggregation": {
        "level": "service",
        "method": "ratio"
      },
      "role_prior": {
        "mutation": 0.80,
        "propagation": 0.15,
        "observability_bias": 0.05,
        "topology_context": 0.00
      },
      "mechanism": "interface failure",
      "required_fields": ["service_name", "status_code"],
      "rationale": "An increase in error status rate often reflects service-level failure behavior."
    },
    {
      "name": "trace_endpoint_shift",
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
        "mutation": 0.75,
        "propagation": 0.20,
        "observability_bias": 0.05,
        "topology_context": 0.00
      },
      "mechanism": "endpoint behavior change",
      "required_fields": ["service_name", "endpoint"],
      "rationale": "A service whose endpoint mix changes after anomaly onset may have changed behavior at its interface."
    },
    {
      "name": "trace_duration_delta",
      "source": "trace",
      "entity": "service",
      "signal": {
        "field": "duration",
        "type": "duration"
      },
      "contrast": {
        "operator": "robust_z_shift",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      },
      "aggregation": {
        "level": "service",
        "method": "max"
      },
      "role_prior": {
        "mutation": 0.20,
        "propagation": 0.75,
        "observability_bias": 0.05,
        "topology_context": 0.00
      },
      "mechanism": "latency propagation",
      "required_fields": ["service_name", "duration"],
      "rationale": "Latency is often amplified along service dependencies and is a typical propagated symptom."
    },
    {
      "name": "trace_count_rise_shift",
      "source": "trace",
      "entity": "service",
      "signal": {
        "field": "__row_count__",
        "type": "count"
      },
      "contrast": {
        "operator": "count_rise",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      },
      "aggregation": {
        "level": "service",
        "method": "ratio"
      },
      "role_prior": {
        "mutation": 0.20,
        "propagation": 0.70,
        "observability_bias": 0.10,
        "topology_context": 0.00
      },
      "mechanism": "retry or traffic amplification",
      "required_fields": ["service_name"],
      "rationale": "A rise in trace count can reflect retries, fan-out, or propagated pressure."
    },
    {
      "name": "trace_count_drop_shift",
      "source": "trace",
      "entity": "service",
      "signal": {
        "field": "__row_count__",
        "type": "count"
      },
      "contrast": {
        "operator": "count_drop",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      },
      "aggregation": {
        "level": "service",
        "method": "ratio"
      },
      "role_prior": {
        "mutation": 0.75,
        "propagation": 0.15,
        "observability_bias": 0.10,
        "topology_context": 0.00
      },
      "mechanism": "service hang or request handling failure",
      "required_fields": ["service_name"],
      "rationale": "A sharp drop in trace activity can indicate a service stopped receiving or processing requests."
    },
    {
      "name": "log_count_delta",
      "source": "log",
      "entity": "service",
      "signal": {
        "field": "__row_count__",
        "type": "count"
      },
      "contrast": {
        "operator": "count_delta",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      },
      "aggregation": {
        "level": "service",
        "method": "ratio"
      },
      "role_prior": {
        "mutation": 0.35,
        "propagation": 0.55,
        "observability_bias": 0.10,
        "topology_context": 0.00
      },
      "mechanism": "software event volume shift",
      "required_fields": ["service_name"],
      "rationale": "Log volume changes can indicate local software events or propagated error handling."
    },
    {
      "name": "log_template_delta",
      "source": "log",
      "entity": "service",
      "signal": {
        "field": "template",
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
        "mutation": 0.45,
        "propagation": 0.45,
        "observability_bias": 0.10,
        "topology_context": 0.00
      },
      "mechanism": "software event distribution shift",
      "required_fields": ["service_name", "template"],
      "rationale": "A log-template distribution shift indicates changed software event behavior, which may be root-local or propagated."
    }
  ]
}
```

注意：第一版可以只支持这些 operator，先保证能跑通和替代硬编码。

---

## 5. DSL Schema 实现

新增文件：

```text
meo/dsl/schema.py
```

建议定义 dataclass 或 Pydantic model。如果不想引入 Pydantic，则用 dataclass + 手动校验。

### 5.1 数据结构

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RoleName = Literal[
    "mutation",
    "propagation",
    "observability_bias",
    "topology_context",
]

SourceName = Literal["metric", "log", "trace", "topology"]

EntityName = Literal["service", "endpoint", "edge", "log_template", "status_code"]

SignalType = Literal[
    "value",
    "count",
    "rate",
    "duration",
    "categorical",
]

ContrastOperator = Literal[
    "z_shift",
    "robust_z_shift",
    "mean_delta",
    "count_delta",
    "count_rise",
    "count_drop",
    "rate_delta",
    "error_rate_delta",
    "distribution_shift",
    "novelty",
]

AggregationMethod = Literal[
    "max",
    "mean",
    "sum",
    "p95",
    "ratio",
    "jsd",
]


@dataclass(frozen=True)
class SignalSpec:
    field: str
    type: SignalType


@dataclass(frozen=True)
class ContrastSpec:
    operator: ContrastOperator
    normal_window: str = "pre_anomaly"
    abnormal_window: str = "post_anomaly"


@dataclass(frozen=True)
class AggregationSpec:
    level: str = "service"
    method: AggregationMethod = "max"


@dataclass(frozen=True)
class EvidenceOperatorSpec:
    name: str
    source: SourceName
    entity: EntityName
    signal: SignalSpec
    contrast: ContrastSpec
    aggregation: AggregationSpec
    role_prior: dict[str, float]
    mechanism: str
    required_fields: list[str]
    rationale: str
```

### 5.2 加载 JSON 到 spec

```python
def parse_operator_spec(raw: dict) -> EvidenceOperatorSpec:
    return EvidenceOperatorSpec(
        name=str(raw["name"]),
        source=raw["source"],
        entity=raw["entity"],
        signal=SignalSpec(**raw["signal"]),
        contrast=ContrastSpec(**raw["contrast"]),
        aggregation=AggregationSpec(**raw["aggregation"]),
        role_prior={k: float(v) for k, v in raw["role_prior"].items()},
        mechanism=str(raw.get("mechanism", "")),
        required_fields=list(raw.get("required_fields", [])),
        rationale=str(raw.get("rationale", "")),
    )
```

---

## 6. DSL Atoms 实现

新增文件：

```text
meo/dsl/atoms.py
```

这些 atoms 是真正的底层计算函数。

### 6.1 数值清理工具

```python
import math
import numpy as np
import pandas as pd


EPS = 1e-9


def finite_series(values: pd.Series | np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    return arr


def safe_max(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    value = float(np.max(values))
    return value if math.isfinite(value) else 0.0
```

### 6.2 z_shift

```python
def z_shift(normal: pd.Series | np.ndarray, abnormal: pd.Series | np.ndarray) -> float:
    normal_arr = finite_series(normal)
    abnormal_arr = finite_series(abnormal)

    if normal_arr.size == 0 or abnormal_arr.size == 0:
        return 0.0

    mu = float(np.mean(normal_arr))
    sigma = float(np.std(normal_arr))

    if not math.isfinite(sigma) or sigma <= EPS:
        return 0.0

    z = np.abs((abnormal_arr - mu) / (sigma + EPS))
    return safe_max(z)
```

### 6.3 robust_z_shift

```python
def robust_z_shift(normal: pd.Series | np.ndarray, abnormal: pd.Series | np.ndarray) -> float:
    normal_arr = finite_series(normal)
    abnormal_arr = finite_series(abnormal)

    if normal_arr.size == 0 or abnormal_arr.size == 0:
        return 0.0

    med = float(np.median(normal_arr))
    q75 = float(np.percentile(normal_arr, 75))
    q25 = float(np.percentile(normal_arr, 25))
    iqr = q75 - q25

    if not math.isfinite(iqr) or iqr <= EPS:
        return 0.0

    score = np.abs((abnormal_arr - med) / (iqr + EPS))
    return safe_max(score)
```

### 6.4 mean_delta

```python
def mean_delta(normal: pd.Series | np.ndarray, abnormal: pd.Series | np.ndarray) -> float:
    normal_arr = finite_series(normal)
    abnormal_arr = finite_series(abnormal)

    if normal_arr.size == 0 or abnormal_arr.size == 0:
        return 0.0

    base = abs(float(np.mean(normal_arr))) + EPS
    delta = abs(float(np.mean(abnormal_arr)) - float(np.mean(normal_arr)))
    return delta / base
```

### 6.5 count_delta / count_rise / count_drop

```python
def count_delta(normal_count: float, abnormal_count: float) -> float:
    normal_count = max(float(normal_count), 0.0)
    abnormal_count = max(float(abnormal_count), 0.0)
    return abs(abnormal_count - normal_count) / (normal_count + EPS)


def count_rise(normal_count: float, abnormal_count: float) -> float:
    normal_count = max(float(normal_count), 0.0)
    abnormal_count = max(float(abnormal_count), 0.0)
    return max(0.0, abnormal_count - normal_count) / (normal_count + EPS)


def count_drop(normal_count: float, abnormal_count: float) -> float:
    normal_count = max(float(normal_count), 0.0)
    abnormal_count = max(float(abnormal_count), 0.0)
    return max(0.0, normal_count - abnormal_count) / (normal_count + EPS)
```

### 6.6 distribution_shift

使用 Jensen-Shannon divergence。

```python
def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)

    p = np.maximum(np.nan_to_num(p, nan=0.0), 0.0)
    q = np.maximum(np.nan_to_num(q, nan=0.0), 0.0)

    if p.sum() <= EPS and q.sum() <= EPS:
        return 0.0

    p = p / (p.sum() + EPS)
    q = q / (q.sum() + EPS)
    m = 0.5 * (p + q)

    def kl(a: np.ndarray, b: np.ndarray) -> float:
        mask = a > EPS
        if not np.any(mask):
            return 0.0
        return float(np.sum(a[mask] * np.log((a[mask] + EPS) / (b[mask] + EPS))))

    score = 0.5 * kl(p, m) + 0.5 * kl(q, m)
    return score if math.isfinite(score) else 0.0
```

### 6.7 error_rate_delta

```python
def is_error_status(value) -> bool:
    try:
        code = int(value)
        return code >= 400
    except Exception:
        text = str(value).lower()
        return (
            "error" in text
            or "fail" in text
            or "timeout" in text
            or text.startswith("5")
            or text.startswith("4")
        )


def error_rate(values: pd.Series | np.ndarray) -> float:
    arr = list(values)
    if len(arr) == 0:
        return 0.0
    errors = sum(1 for v in arr if is_error_status(v))
    return float(errors) / float(len(arr))


def error_rate_delta(normal_values, abnormal_values) -> float:
    return abs(error_rate(abnormal_values) - error_rate(normal_values))
```

---

## 7. Compiler 实现

新增文件：

```text
meo/dsl/compiler.py
```

### 7.1 Compiler 类接口

```python
from __future__ import annotations

from typing import Callable
import numpy as np
import pandas as pd

from .schema import EvidenceOperatorSpec
from .atoms import (
    z_shift,
    robust_z_shift,
    mean_delta,
    count_delta,
    count_rise,
    count_drop,
    js_divergence,
    error_rate_delta,
)


FeatureFn = Callable[[dict[str, pd.DataFrame], list[str]], np.ndarray]


class EvidenceCompiler:
    def compile(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        if spec.source == "metric":
            return self._compile_metric(spec)
        if spec.source == "trace":
            return self._compile_trace(spec)
        if spec.source == "log":
            return self._compile_log(spec)
        if spec.source == "topology":
            return self._compile_topology(spec)
        raise ValueError(f"Unsupported source: {spec.source}")
```

### 7.2 Metric 编译

第一版假设 metric frame 可能是 wide format，即列名形如：

```text
service_metricName
```

如果已有 `cera._build_feature_matrix` 里有服务名解析工具，优先复用 `_series_service`、`_clean_service` 或你已有的 service collection 逻辑。

```python
    def _compile_metric(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        op = spec.contrast.operator
        field = spec.signal.field

        def feature(frames: dict[str, pd.DataFrame], services: list[str]) -> np.ndarray:
            normal = frames.get("normal_metrics", pd.DataFrame())
            abnormal = frames.get("abnormal_metrics", pd.DataFrame())
            out: list[float] = []

            for svc in services:
                if field == "__row_count__":
                    n_count = self._service_metric_row_count(normal, svc)
                    a_count = self._service_metric_row_count(abnormal, svc)
                    out.append(self._apply_count_op(op, n_count, a_count))
                    continue

                candidate_cols = self._metric_columns_for_service(normal, abnormal, svc, field)
                if not candidate_cols:
                    out.append(0.0)
                    continue

                scores = []
                for col in candidate_cols:
                    if col not in normal.columns or col not in abnormal.columns:
                        continue
                    scores.append(self._apply_numeric_op(op, normal[col], abnormal[col]))

                out.append(max(scores) if scores else 0.0)

            return np.asarray(out, dtype=np.float64)

        return feature
```

辅助函数：

```python
    def _metric_columns_for_service(
        self,
        normal: pd.DataFrame,
        abnormal: pd.DataFrame,
        service: str,
        field: str,
    ) -> list[str]:
        cols = set(normal.columns) | set(abnormal.columns)
        cols = [c for c in cols if c != "time"]

        if field == "*":
            return [c for c in cols if str(c).startswith(f"{service}_")]

        direct = f"{service}_{field}"
        if direct in cols:
            return [direct]

        return [
            c for c in cols
            if str(c).startswith(f"{service}_") and field in str(c)
        ]

    def _service_metric_row_count(self, frame: pd.DataFrame, service: str) -> float:
        cols = [c for c in frame.columns if c != "time" and str(c).startswith(f"{service}_")]
        if not cols:
            return 0.0
        return float(frame[cols].dropna(how="all").shape[0])

    def _apply_numeric_op(self, op: str, normal_values, abnormal_values) -> float:
        if op == "z_shift":
            return z_shift(normal_values, abnormal_values)
        if op == "robust_z_shift":
            return robust_z_shift(normal_values, abnormal_values)
        if op == "mean_delta":
            return mean_delta(normal_values, abnormal_values)
        raise ValueError(f"Unsupported numeric operator: {op}")

    def _apply_count_op(self, op: str, normal_count: float, abnormal_count: float) -> float:
        if op == "count_delta":
            return count_delta(normal_count, abnormal_count)
        if op == "count_rise":
            return count_rise(normal_count, abnormal_count)
        if op == "count_drop":
            return count_drop(normal_count, abnormal_count)
        raise ValueError(f"Unsupported count operator: {op}")
```

### 7.3 Trace 编译

支持字段名兼容：

* service: `service_name`, `service`, `svc`
* endpoint: `endpoint`, `operation`, `operation_name`, `span_name`, `http_route`
* status: `status_code`, `http_status_code`, `status`
* duration: `duration`, `duration_ms`, `latency`, `elapsed`

```python
    def _compile_trace(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        op = spec.contrast.operator
        field = spec.signal.field

        def feature(frames: dict[str, pd.DataFrame], services: list[str]) -> np.ndarray:
            normal = frames.get("normal_traces", pd.DataFrame())
            abnormal = frames.get("abnormal_traces", pd.DataFrame())

            service_col_n = self._find_col(normal, ["service_name", "service", "svc"])
            service_col_a = self._find_col(abnormal, ["service_name", "service", "svc"])

            if service_col_n is None or service_col_a is None:
                return np.zeros(len(services), dtype=np.float64)

            out: list[float] = []

            for svc in services:
                n = normal[normal[service_col_n].astype(str) == str(svc)]
                a = abnormal[abnormal[service_col_a].astype(str) == str(svc)]

                if field == "__row_count__":
                    out.append(self._apply_count_op(op, float(len(n)), float(len(a))))
                    continue

                actual_field_n = self._resolve_trace_field(n, field)
                actual_field_a = self._resolve_trace_field(a, field)
                if actual_field_n is None or actual_field_a is None:
                    out.append(0.0)
                    continue

                if op == "distribution_shift":
                    out.append(self._categorical_distribution_shift(n[actual_field_n], a[actual_field_a]))
                elif op == "error_rate_delta":
                    out.append(error_rate_delta(n[actual_field_n], a[actual_field_a]))
                else:
                    out.append(self._apply_numeric_op(op, n[actual_field_n], a[actual_field_a]))

            return np.asarray(out, dtype=np.float64)

        return feature
```

辅助：

```python
    def _find_col(self, frame: pd.DataFrame, candidates: list[str]) -> str | None:
        lower_to_original = {str(c).lower(): c for c in frame.columns}
        for c in candidates:
            if c.lower() in lower_to_original:
                return lower_to_original[c.lower()]
        return None

    def _resolve_trace_field(self, frame: pd.DataFrame, field: str) -> str | None:
        aliases = {
            "endpoint": ["endpoint", "operation", "operation_name", "span_name", "http_route", "route"],
            "status_code": ["status_code", "http_status_code", "status", "code"],
            "duration": ["duration", "duration_ms", "latency", "elapsed", "elapsed_ms"],
        }
        candidates = aliases.get(field, [field])
        return self._find_col(frame, candidates)

    def _categorical_distribution_shift(self, normal_values, abnormal_values) -> float:
        n = pd.Series(normal_values).dropna().astype(str)
        a = pd.Series(abnormal_values).dropna().astype(str)

        categories = sorted(set(n.unique()) | set(a.unique()))
        if not categories:
            return 0.0

        p = np.asarray([(n == cat).sum() for cat in categories], dtype=np.float64)
        q = np.asarray([(a == cat).sum() for cat in categories], dtype=np.float64)
        return js_divergence(p, q)
```

### 7.4 Log 编译

支持：

* service: `service_name`, `service`, `svc`
* template: `template`, `log_template`, `message_template`
* level: `level`, `severity`

```python
    def _compile_log(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        op = spec.contrast.operator
        field = spec.signal.field

        def feature(frames: dict[str, pd.DataFrame], services: list[str]) -> np.ndarray:
            normal = frames.get("normal_logs", pd.DataFrame())
            abnormal = frames.get("abnormal_logs", pd.DataFrame())

            service_col_n = self._find_col(normal, ["service_name", "service", "svc"])
            service_col_a = self._find_col(abnormal, ["service_name", "service", "svc"])

            if service_col_n is None or service_col_a is None:
                return np.zeros(len(services), dtype=np.float64)

            out: list[float] = []

            for svc in services:
                n = normal[normal[service_col_n].astype(str) == str(svc)]
                a = abnormal[abnormal[service_col_a].astype(str) == str(svc)]

                if field == "__row_count__":
                    out.append(self._apply_count_op(op, float(len(n)), float(len(a))))
                    continue

                actual_field_n = self._resolve_log_field(n, field)
                actual_field_a = self._resolve_log_field(a, field)

                if actual_field_n is None or actual_field_a is None:
                    out.append(0.0)
                    continue

                if op == "distribution_shift":
                    out.append(self._categorical_distribution_shift(n[actual_field_n], a[actual_field_a]))
                else:
                    out.append(0.0)

            return np.asarray(out, dtype=np.float64)

        return feature
```

辅助：

```python
    def _resolve_log_field(self, frame: pd.DataFrame, field: str) -> str | None:
        aliases = {
            "template": ["template", "log_template", "message_template", "event_template"],
            "level": ["level", "severity", "log_level"],
            "message": ["message", "msg", "body", "content"],
        }
        candidates = aliases.get(field, [field])
        return self._find_col(frame, candidates)
```

### 7.5 Topology 编译

第一版可以跳过 topology operators，因为你当前 CREST 已经从 `_build_feature_matrix` 或 trace_edges 中处理 topology context。若要实现：

```python
    def _compile_topology(self, spec: EvidenceOperatorSpec) -> FeatureFn:
        def feature(frames: dict[str, pd.DataFrame], services: list[str]) -> np.ndarray:
            return np.zeros(len(services), dtype=np.float64)
        return feature
```

---

## 8. MEOL 加载与实例化

新增文件：

```text
meo/runtime/load_meol.py
```

```python
from __future__ import annotations

import json
from pathlib import Path

from meo.dsl.schema import EvidenceOperatorSpec, parse_operator_spec


def load_meol(path: str | Path) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_operator_specs(path: str | Path) -> list[EvidenceOperatorSpec]:
    raw = load_meol(path)
    return [parse_operator_spec(item) for item in raw.get("operators", [])]
```

新增文件：

```text
meo/runtime/instantiate.py
```

```python
from __future__ import annotations

import numpy as np
import pandas as pd

from meo.dsl.compiler import EvidenceCompiler
from meo.dsl.schema import EvidenceOperatorSpec


ROLE_ORDER = [
    "mutation",
    "propagation",
    "observability_bias",
    "topology_context",
]


def instantiate_meol_features(
    frames: dict[str, pd.DataFrame],
    services: list[str],
    specs: list[EvidenceOperatorSpec],
    compiler: EvidenceCompiler | None = None,
) -> tuple[np.ndarray, tuple[str, ...], np.ndarray]:
    compiler = compiler or EvidenceCompiler()

    feature_values: list[np.ndarray] = []
    feature_names: list[str] = []
    role_weights: list[list[float]] = []

    for spec in specs:
        try:
            fn = compiler.compile(spec)
            values = fn(frames, services)
        except Exception:
            values = np.zeros(len(services), dtype=np.float64)

        values = np.nan_to_num(values, nan=0.0, posinf=0.0, neginf=0.0)
        values = np.maximum(values, 0.0)

        feature_values.append(values)
        feature_names.append(spec.name)

        role = spec.role_prior
        role_weights.append([float(role.get(r, 0.0)) for r in ROLE_ORDER])

    if feature_values:
        feature_matrix = np.stack(feature_values, axis=1)
        role_weight_matrix = np.asarray(role_weights, dtype=np.float64)
    else:
        feature_matrix = np.zeros((len(services), 0), dtype=np.float64)
        role_weight_matrix = np.zeros((0, len(ROLE_ORDER)), dtype=np.float64)

    return feature_matrix, tuple(feature_names), role_weight_matrix
```

---

## 9. Verifier 设计

第一版可以先不接入主流程，但要实现基本校验，便于后续论文复现。

新增：

```text
meo/verify/static_verifier.py
```

```python
from __future__ import annotations

from meo.dsl.schema import EvidenceOperatorSpec


ALLOWED_OPERATORS = {
    "z_shift",
    "robust_z_shift",
    "mean_delta",
    "count_delta",
    "count_rise",
    "count_drop",
    "rate_delta",
    "error_rate_delta",
    "distribution_shift",
    "novelty",
}

ALLOWED_SOURCES = {"metric", "log", "trace", "topology"}

ALLOWED_ROLES = {
    "mutation",
    "propagation",
    "observability_bias",
    "topology_context",
}


def static_verify(spec: EvidenceOperatorSpec) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if spec.source not in ALLOWED_SOURCES:
        errors.append(f"invalid_source:{spec.source}")

    if spec.contrast.operator not in ALLOWED_OPERATORS:
        errors.append(f"invalid_operator:{spec.contrast.operator}")

    role_keys = set(spec.role_prior)
    unknown_roles = role_keys - ALLOWED_ROLES
    if unknown_roles:
        errors.append(f"unknown_roles:{sorted(unknown_roles)}")

    total = sum(float(v) for v in spec.role_prior.values())
    if abs(total - 1.0) > 1e-3:
        errors.append(f"role_prior_not_normalized:{total}")

    for role, value in spec.role_prior.items():
        if value < 0.0 or value > 1.0:
            errors.append(f"role_prior_out_of_range:{role}:{value}")

    if not spec.rationale:
        errors.append("missing_rationale")

    if not spec.mechanism:
        errors.append("missing_mechanism")

    return len(errors) == 0, errors
```

新增：

```text
meo/verify/leakage_verifier.py
```

```python
from __future__ import annotations

import json

from meo.dsl.schema import EvidenceOperatorSpec


FORBIDDEN_TOKENS = {
    "ground_truth",
    "root_cause",
    "root_service",
    "root_metric",
    "answer",
    "label",
    "rank",
    "torai_wrong",
    "baseline_output",
}


def leakage_verify(spec: EvidenceOperatorSpec) -> tuple[bool, list[str]]:
    text = json.dumps(spec, default=lambda o: getattr(o, "__dict__", str(o))).lower()
    hits = sorted(token for token in FORBIDDEN_TOKENS if token in text)
    return len(hits) == 0, hits
```

新增：

```text
meo/verify/dynamic_verifier.py
```

```python
from __future__ import annotations

import numpy as np
import pandas as pd

from meo.dsl.compiler import EvidenceCompiler
from meo.dsl.schema import EvidenceOperatorSpec


def dynamic_verify(
    spec: EvidenceOperatorSpec,
    frames: dict[str, pd.DataFrame],
    services: list[str],
    compiler: EvidenceCompiler | None = None,
) -> tuple[bool, dict[str, float]]:
    compiler = compiler or EvidenceCompiler()

    try:
        fn = compiler.compile(spec)
        values = fn(frames, services)
    except Exception:
        return False, {"compile_or_runtime_error": 1.0}

    values = np.asarray(values, dtype=np.float64)
    stats = {
        "nan_rate": float(np.isnan(values).mean()) if values.size else 1.0,
        "nonzero_rate": float((np.nan_to_num(values) > 0.0).mean()) if values.size else 0.0,
        "variance": float(np.nanvar(values)) if values.size else 0.0,
        "max": float(np.nanmax(values)) if values.size else 0.0,
    }

    ok = True
    if stats["nan_rate"] > 0.1:
        ok = False
    if stats["variance"] <= 1e-12:
        ok = False

    return ok, stats
```

---

## 10. 将 MEO 接入 CREST

当前 `score_crest_services` 中的流程是：

```python
frames = _load_input_frames(input_folder)
services = _collect_services_from_frames(frames)
enabled_feature_set = ...
enabled_features = ...
matrix, trace_edges = _build_feature_matrix(...)
case_matrix = _robust_case_feature_matrix(matrix)
role_matrix = _apply_arc_trace_endpoint_support_gate(enabled_features, case_matrix)
local_energy = _local_family_energy(...)
...
```

现在建议增加一个可选参数：

```python
use_meo: bool = False
meol_path: Path | None = None
```

或者通过 class 设置：

```python
class CRESTMEO(CREST):
    _use_meo = True
    _meol_path = Path("meo/library/default_meol.json")
```

### 10.1 新增 role vector 计算函数

在 CREST 文件中新增：

```python
ROLE_MUTATION = 0
ROLE_PROPAGATION = 1
ROLE_OBSERVABILITY_BIAS = 2
ROLE_TOPOLOGY_CONTEXT = 3


def _meo_role_vectors(
    feature_matrix: np.ndarray,
    role_weight_matrix: np.ndarray,
) -> dict[str, np.ndarray]:
    if feature_matrix.size == 0 or role_weight_matrix.size == 0:
        zeros = np.zeros(feature_matrix.shape[0], dtype=np.float64)
        return {
            "mutation": zeros.copy(),
            "propagation": zeros.copy(),
            "observability_bias": zeros.copy(),
            "topology_context": zeros.copy(),
        }

    return {
        "mutation": feature_matrix @ role_weight_matrix[:, ROLE_MUTATION],
        "propagation": feature_matrix @ role_weight_matrix[:, ROLE_PROPAGATION],
        "observability_bias": feature_matrix @ role_weight_matrix[:, ROLE_OBSERVABILITY_BIAS],
        "topology_context": feature_matrix @ role_weight_matrix[:, ROLE_TOPOLOGY_CONTEXT],
    }
```

### 10.2 新增 soft explain-away

当前 `_apply_counterfactual_explain_away_once` 通过 feature index 从 role_matrix 中重新计算 mutation / propagation。MEO 模式下直接传入 `mutation` 和 `propagation` vectors。

新增：

```python
def _apply_counterfactual_explain_away_once_soft(
    services: list[str],
    structural_energy: np.ndarray,
    mutation: np.ndarray,
    propagation: np.ndarray,
    trace_edges: list[tuple[str, str]],
) -> np.ndarray:
    if not trace_edges or structural_energy.size == 0:
        return structural_energy

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    adjusted = structural_energy.astype(np.float64, copy=True)
    best_by_victim: dict[int, tuple[int, int, float]] = {}

    def add_pair(root_idx: int, victim_idx: int) -> None:
        if root_idx == victim_idx or adjusted[victim_idx] <= adjusted[root_idx]:
            return

        mutation_excess = max(0.0, float(mutation[root_idx] - mutation[victim_idx]))
        propagation_excess = max(0.0, float(propagation[victim_idx] - propagation[root_idx]))

        if mutation_excess <= 0.0 or propagation_excess <= 0.0:
            return

        mutation_share = mutation_excess / (
            float(mutation[root_idx] + mutation[victim_idx]) + 1e-12
        )
        propagation_share = propagation_excess / (
            float(propagation[victim_idx] + propagation[root_idx]) + 1e-12
        )

        transfer = (
            float(adjusted[victim_idx] - adjusted[root_idx])
            * mutation_share
            * propagation_share
        )

        if not np.isfinite(transfer) or transfer <= 0.0:
            return

        current = best_by_victim.get(victim_idx)
        if current is None or transfer > current[2]:
            best_by_victim[victim_idx] = (root_idx, victim_idx, transfer)

    for parent, child in trace_edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)

        if parent_idx is None or child_idx is None:
            continue

        add_pair(parent_idx, child_idx)
        add_pair(child_idx, parent_idx)

    for root_idx, victim_idx, transfer in best_by_victim.values():
        adjusted[root_idx] += transfer
        adjusted[victim_idx] -= transfer

    return np.maximum(adjusted, 0.0)
```

新增多轮版本：

```python
def _apply_counterfactual_explain_away_soft(
    services: list[str],
    structural_energy: np.ndarray,
    mutation: np.ndarray,
    propagation: np.ndarray,
    trace_edges: list[tuple[str, str]],
    max_iter: int = 4,
) -> np.ndarray:
    adjusted = structural_energy.astype(np.float64, copy=True)

    for _ in range(max_iter):
        updated = _apply_counterfactual_explain_away_once_soft(
            services=services,
            structural_energy=adjusted,
            mutation=mutation,
            propagation=propagation,
            trace_edges=trace_edges,
        )

        if np.linalg.norm(updated - adjusted) <= 1e-12 * (np.linalg.norm(adjusted) + 1e-12):
            return updated

        adjusted = updated

    return adjusted
```

### 10.3 修改 score_crest_services

新增参数：

```python
def score_crest_services(
    input_folder: Path,
    enabled_modalities: frozenset[str] = ALL_MODALITIES,
    graph_mode: str = "counterfactual",
    residual_eta: float | None = None,
    use_meo: bool = False,
    meol_path: Path | None = None,
) -> pd.DataFrame:
```

在函数内部，加载 frames 和 services 后：

```python
if use_meo:
    from meo.runtime.load_meol import load_operator_specs
    from meo.runtime.instantiate import instantiate_meol_features

    specs = load_operator_specs(meol_path or Path("meo/library/default_meol.json"))

    meo_matrix, meo_features, role_weight_matrix = instantiate_meol_features(
        frames=frames,
        services=services,
        specs=specs,
    )

    case_matrix = _robust_case_feature_matrix(meo_matrix)
    role_vectors = _meo_role_vectors(case_matrix, role_weight_matrix)

    mutation = role_vectors["mutation"]
    propagation = role_vectors["propagation"]
    observability_bias = role_vectors["observability_bias"]
    topology_context = role_vectors["topology_context"]

    local_energy = np.maximum(
        mutation + propagation + observability_bias + topology_context,
        0.0,
    )
    local_abnormality = _saturating_incident_scale(local_energy)

    matrix = meo_matrix
    enabled_features = meo_features
    role_matrix = case_matrix

else:
    existing original path
```

之后 graph 逻辑复用现有代码。但在 `graph_mode == "counterfactual"` 分支中，如果 `use_meo=True`，用 soft explain-away：

```python
if use_meo:
    structural_seed = local_energy.copy()
    context_weight = _trace_density_context_weight(services, trace_edges)
    structural_energy = _apply_parent_context(
        services,
        structural_seed,
        trace_edges,
        context_weight,
    )
    structural_energy = _apply_counterfactual_explain_away_soft(
        services=services,
        structural_energy=np.maximum(structural_energy, 0.0),
        mutation=mutation,
        propagation=propagation,
        trace_edges=trace_edges,
    )
    explanatory_power = _saturating_incident_scale(structural_energy)

    denoised_support = _saturating_incident_scale(
        np.maximum(mutation + propagation, 0.0)
    )
else:
    existing original counterfactual branch
```

最终：

```python
score = local_abnormality * explanatory_power
if graph_mode == "counterfactual":
    score = score + denoised_support
```

保持原有排序。

### 10.4 新增算法类

在 CREST 文件底部新增：

```python
class CRESTMEO(CREST):
    """CREST-MEO: CREST with Meta Evidence Operator Library."""

    _use_meo = True
    _meol_path: Path | None = None

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        ranking = score_crest_services(
            args.input_folder,
            enabled_modalities=self._modalities,
            graph_mode=self._graph_mode,
            residual_eta=self._residual_eta,
            use_meo=True,
            meol_path=self._meol_path,
        )

        if self._export_residual_diagnostics:
            _export_crest_residual_diagnostics(ranking, args)

        return [
            AlgorithmAnswer(level="service", name=str(row.service), rank=rank)
            for rank, row in enumerate(ranking.itertuples(index=False), start=1)
        ]
```

如果 `Path` 未导入，复用文件顶部已有 `from pathlib import Path`。

---

## 11. LLM mock 输出

第一版不接真实 LLM，新增：

```text
meo/llm/mock_outputs.py
```

```python
def mock_meol() -> dict:
    return {
        "library_name": "crest-meol-mock-v1",
        "dsl_version": "1.0",
        "generator": {
            "type": "mock_llm",
            "prompt_version": "meo_operator_synthesis_v1",
            "uses_ground_truth": False,
            "uses_case_fault_type": False,
            "uses_baseline_outputs": False,
        },
        "roles": [
            "mutation",
            "propagation",
            "observability_bias",
            "topology_context",
        ],
        "operators": [
            # copy the default_meol operators here or load from json
        ],
    }
```

也可以提供 CLI 生成 default file：

```text
python -m meo.llm.synthesize --mock --output meo/library/default_meol.json
```

新增：

```text
meo/llm/synthesize.py
```

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .mock_outputs import mock_meol


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    if not args.mock:
        raise NotImplementedError("Real LLM synthesis is not implemented yet.")

    meol = mock_meol()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(meol, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
```

---

## 11.1 Config-driven LLM Synthesis 当前实现

当前实现已经把 LLM synthesis 从简单 `--mock` 脚本升级为 config-driven offline
pipeline。配置文件位置：

```text
algorithms/evidencerank/src/evidencerank/meo/llm/config.yaml
```

默认配置：

```yaml
synthesis:
  mode: mock
  allow_real_llm: false
llm:
  provider: mock
```

因此默认运行不会调用任何真实 LLM。mock 内容统一放在：

```text
algorithms/evidencerank/src/evidencerank/meo/llm/mock_outputs.py
```

包括：

- `mock_meol()`
- mock artifact summary
- mock telemetry schema
- mock mechanism catalog

CLI：

```bash
uv run --package evidencerank python -m meo.llm.synthesize \
  --config algorithms/evidencerank/src/evidencerank/meo/llm/config.yaml \
  --mock \
  --output /tmp/default_meol.json
```

这个 CLI 会执行完整离线流程：

```text
config.yaml
  -> artifact / telemetry / mechanism prompt context
  -> DSL-constrained prompt
  -> mock or real LLM client
  -> MEOL JSON
  -> static verifier
  -> leakage verifier
  -> frozen output JSON
```

真实 LLM 路径已经预留，但需要双重显式开启：

1. config 中设置 `synthesis.mode=real`、`synthesis.allow_real_llm=true`、
   `llm.provider=openai`、`llm.model=<your model>`；
2. CLI 传入 `--allow-real-llm`。

这样可以防止测试、benchmark eval 或在线 CREST-MEO 路径误触发外部调用。

如果需要把某个 incident 的 telemetry schema 喂给 prompt，可使用：

```bash
uv run --package evidencerank python -m meo.llm.synthesize \
  --mock \
  --input-folder data/rcabench-platform-v2/data/rcabench/<datapack> \
  --output /tmp/default_meol.json
```

`--input-folder` 只做 schema summary，不把 row-level telemetry 或 GT 写入 prompt。

---

## 12. Artifact Mining 第一版

第一版可以只实现 telemetry schema mining，不做完整 source code parser。

新增：

```text
meo/artifacts/telemetry_schema.py
```

```python
from __future__ import annotations

import pandas as pd


def summarize_frames(frames: dict[str, pd.DataFrame]) -> dict:
    summary = {}
    for name, frame in frames.items():
        if frame is None or frame.empty:
            summary[name] = {
                "columns": [],
                "num_rows": 0,
            }
        else:
            summary[name] = {
                "columns": [str(c) for c in frame.columns],
                "num_rows": int(len(frame)),
            }
    return summary
```

后续真实 LLM prompt 可以把这个 summary 喂给 LLM。

---

## 13. Prompt 设计

新增：

```text
meo/llm/prompts.py
```

```python
MEO_OPERATOR_SYNTHESIS_PROMPT = """
You are an expert SRE and telemetry feature designer.

Your task is to synthesize candidate evidence operators for microservice root cause analysis.

Important constraints:
1. You must not use ground-truth root cause labels.
2. You must not use case-specific fault type labels.
3. You must not use baseline outputs or information about which method succeeds or fails.
4. You must only use the allowed DSL atoms.
5. Each operator must be computable from normal and abnormal telemetry windows.
6. Each operator must be service-level or edge-level aggregatable.
7. Each operator must include a role_prior over:
   - mutation
   - propagation
   - observability_bias
   - topology_context
8. Output valid JSON only.

Telemetry schema:
{telemetry_schema}

Mechanism catalog:
{mechanism_catalog}

Allowed DSL atoms:
{dsl_atoms}

Return JSON in this format:
{{
  "operators": [
    {{
      "name": "...",
      "source": "metric|log|trace|topology",
      "entity": "service|endpoint|edge|log_template|status_code",
      "signal": {{
        "field": "...",
        "type": "value|count|rate|duration|categorical"
      }},
      "contrast": {{
        "operator": "z_shift|robust_z_shift|mean_delta|count_delta|count_rise|count_drop|rate_delta|error_rate_delta|distribution_shift|novelty",
        "normal_window": "pre_anomaly",
        "abnormal_window": "post_anomaly"
      }},
      "aggregation": {{
        "level": "service",
        "method": "max|mean|sum|p95|ratio|jsd"
      }},
      "role_prior": {{
        "mutation": 0.0,
        "propagation": 0.0,
        "observability_bias": 0.0,
        "topology_context": 0.0
      }},
      "mechanism": "...",
      "required_fields": ["..."],
      "rationale": "..."
    }}
  ]
}}
"""
```

Mechanism catalog 第一版：

```python
DEFAULT_MECHANISM_CATALOG = [
    {
        "mechanism": "resource saturation",
        "observable_consequences": [
            "resource metrics shift",
            "latency may increase",
            "error rate may increase"
        ],
        "typical_roles": ["mutation", "propagation"]
    },
    {
        "mechanism": "service hang or crash",
        "observable_consequences": [
            "request count drops",
            "trace count drops",
            "metric rows may disappear"
        ],
        "typical_roles": ["mutation"]
    },
    {
        "mechanism": "interface failure",
        "observable_consequences": [
            "status code distribution changes",
            "error rate increases",
            "error logs increase"
        ],
        "typical_roles": ["mutation"]
    },
    {
        "mechanism": "dependency slowdown",
        "observable_consequences": [
            "trace duration increases",
            "latency propagates upstream",
            "log volume can increase due to retries"
        ],
        "typical_roles": ["propagation"]
    },
    {
        "mechanism": "retry or backpressure",
        "observable_consequences": [
            "trace count rises",
            "log count rises",
            "latency increases in downstream or upstream services"
        ],
        "typical_roles": ["propagation"]
    },
    {
        "mechanism": "observability skew",
        "observable_consequences": [
            "services with more telemetry rows may receive higher raw scores"
        ],
        "typical_roles": ["observability_bias"]
    }
]
```

---

## 14. 兼容性要求

必须保证：

1. 原始 `CREST`、`CRESTResidual`、`CRESTLocal`、`CRESTNoCF`、`CRESTMetric` 等类保持不变。
2. 新增 `CRESTMEO`，不要破坏原有实验结果。
3. `use_meo=False` 时完全走旧路径。
4. `use_meo=True` 时走新路径。
5. 如果 MEOL 加载失败或 operators 全部不可用，应 fallback 到原始 CREST 或 local abnormality，不能崩溃。
6. 所有 feature 输出必须非负、finite。
7. 所有 role_prior 必须归一化。
8. MEOL 不允许使用 GT、fault label、baseline output。

---

## 15. 单元测试建议

新增测试：

```text
tests/test_meo_atoms.py
tests/test_meo_compiler.py
tests/test_meo_instantiate.py
tests/test_crest_meo_smoke.py
```

### 15.1 atoms 测试

```python
def test_count_drop():
    assert count_drop(100, 50) > 0
    assert count_drop(50, 100) == 0

def test_count_rise():
    assert count_rise(50, 100) > 0
    assert count_rise(100, 50) == 0

def test_js_divergence_zero_for_same_distribution():
    p = np.array([1, 2, 3])
    assert js_divergence(p, p) < 1e-9
```

### 15.2 compiler 测试

构造简单 frames：

```python
frames = {
    "normal_traces": pd.DataFrame({
        "service_name": ["a", "a", "b"],
        "status_code": [200, 200, 200],
        "duration": [10, 11, 9],
    }),
    "abnormal_traces": pd.DataFrame({
        "service_name": ["a", "a", "b"],
        "status_code": [500, 500, 200],
        "duration": [100, 120, 10],
    }),
}
```

测试 `trace_status_code_shift` 中 service `a` 分数高于 `b`。

### 15.3 CRESTMEO smoke test

用一个小 input_folder 跑 `CRESTMEO`，确保返回 `AlgorithmAnswer` list。

---

## 16. 论文叙事对应

实现完成后，论文里可以这样描述：

1. **MEO 离线生成 evidence operators**
   不直接做 RCA，不看 GT，不看 test labels。

2. **DSL-constrained synthesis**
   LLM 只能在允许的 operator atoms 中组合，输出 JSON spec。

3. **Deterministic compiler**
   spec 被编译成确定性 Python feature functions。

4. **MEOL frozen before evaluation**
   评估前冻结 operator library。

5. **CREST online ranking remains deterministic**
   在线阶段只计算 telemetry feature matrix 和 counterfactual ranking。

6. **Ablation**
   比较 CREST-Hand、CREST-MEO、CREST-MEO w/o verifier、CREST-DSL-Random、CREST-SwapRole、LLM-direct RCA。

---

## 17. 实现优先级

### Phase 1: 最小可用版本

1. 新建 `meo/dsl/atoms.py`
2. 新建 `meo/dsl/schema.py`
3. 新建 `meo/dsl/compiler.py`
4. 新建 `meo/runtime/load_meol.py`
5. 新建 `meo/runtime/instantiate.py`
6. 新建 `meo/library/default_meol.json`
7. 在 CREST 中增加 `use_meo` 路径
8. 新增 `CRESTMEO` 类
9. 跑通一个 smoke test

### Phase 2: Verifier

1. static verifier
2. leakage verifier
3. dynamic verifier
4. 生成 verifier report

### Phase 3: Mock LLM

1. 加 `meo/llm/prompts.py`
2. 加 `meo/llm/mock_outputs.py`
3. 加 `meo/llm/synthesize.py`
4. 支持 mock 生成 MEOL

### Phase 4: 真实 LLM 接入

1. 输入 telemetry schema summary
2. 输入 mechanism catalog
3. 输入 DSL grammar
4. LLM 生成 JSON
5. verifier 过滤
6. MEOL 冻结

### Phase 5: 实验

1. CREST vs CRESTMEO
2. Hand vs MEO
3. SwapRole
4. DSL-Random
5. w/o verifier
6. w/o trace / metric / log
7. runtime comparison

---

## 18. 最终验收标准

完成后应满足：

1. 原有 CREST 不受影响。
2. 新增 CRESTMEO 可以在相同 benchmark adapter 上运行。
3. `default_meol.json` 可以被加载并编译。
4. 每个 operator 都能输出每个 service 的非负分数。
5. CRESTMEO 输出 service-level ranking。
6. feature names 和 role weights 可导出用于诊断。
7. mock LLM 版本可以复现固定 MEOL。
8. 没有任何 GT label、fault type、baseline output 进入 MEOL。
9. 支持后续替换为真实 LLM 生成。

---

## 19. 关键实现注意事项

1. 不要让 LLM 输出 Python 代码。
2. 不要在 online ranking 时调用 LLM。
3. DSL spec 必须是 JSON。
4. compiler 必须只使用已有 telemetry frames。
5. verifier 必须防止 GT leakage。
6. MEO 模式失败时要 graceful fallback。
7. role_prior 先用 soft weight，不要硬编码 mutation / propagation set。
8. 第一版不要追求覆盖所有字段，先跑通核心 operators。
9. 所有输出必须 finite、non-negative。
10. 保留原始 hard-coded CREST 作为 baseline 和 ablation。

---

## 20. Oracle Evidence Operators / Raw-Telemetry Upper Bound

Oracle evidence operators 是专门用于离线研究和论文上限分析的泄漏型
artifact。它们可以读取 RCABench 的 service-level GT label，但读取只发生在
`VibeResearchTools/` 的离线 synthesis 阶段，不允许进入 `default_meol.json`、
`CRESTMEO` 在线路径、benchmark 正式提交路径或任何无标签/可部署算法路径。

当前主 Oracle 的语义是：

```text
从 raw telemetry 自动生成一批全 benchmark 通用 evidence operators，
再用 GT 离线选择最能提升 AC@1 的全局 operator + role + counterfactual 配置。
```

它模拟的是“离线 MEO/LLM 如果能从 telemetry schema 和机制语义中生成最好的通用
operator library，会得到什么上限”，而不是“每个 incident 直接查 GT”。

### 20.1 目的

Raw-telemetry Oracle artifact 用于回答：

```text
如果允许用整个 benchmark 的 GT label 离线选择通用 evidence operators 和角色，
但每个 operator 的取值仍只能来自 raw normal/abnormal telemetry，
CREST-MEO role-vector + counterfactual ranking 可以达到什么上限？
```

它用于：

1. 给 CREST、默认 CREST-MEO 和 future LLM-MEO 做 upper-bound 对照；
2. 检查当前 telemetry schema 能否表达更强的 RCA evidence；
3. 验证 MEOL/feature-matrix/role-vector/counterfactual pipeline 是否能消费全局 operator library；
4. 为论文叙事区分“在线无标签算法”与“离线 Oracle 角色合成上限”。

### 20.2 严格隔离规则

Oracle artifact 必须满足：

1. 只由 `VibeResearchTools/crest_meo_universal_oracle.py` 生成；
2. 可以读取 `labels.csv`，但只能用于离线 operator/role selection objective；
3. feature values 只由 raw telemetry 计算，不能由 GT、fault type 或历史排名计算；
4. 不读取 `conclusion.parquet`；
5. 不读取历史 `output.parquet` / `perf.parquet` 作为候选 evidence；
6. 不写入 `algorithms/evidencerank/src/evidencerank/meo/library/default_meol.json`；
7. 不被 `score_crest_services(..., use_meo=True)` 默认加载；
8. JSON metadata 中必须显式标注 `uses_gt_labels=true`、
   `not_for_online_ranking=true` 和 `intentionally_leaky=true`；
9. 任何基于 Oracle 的分数不能作为正式算法结果汇报，只能作为 upper bound。

明确禁止：

```text
per-incident GT signal
service-name weight
GT telemetry feature bank
historical run result feature
datapack / fault / service name rule
```

### 20.3 Candidate Operator Pool

候选 operator pool 是全局的，由 schema / dtype / alias / coverage 规则自动枚举：

1. `crest_feature`
   当前 CREST 的 21 个基础 telemetry features。

2. `meol_operator`
   default MEOL 中的 10 个机制化 operators。当前离线工具为了速度复用与 CREST
   feature 同名的列；无法映射的 operator 返回零列，不会 crash。

3. `raw_metric_value`
   从 raw metrics 中扫描覆盖足够多 incident 的 metric name，并枚举
   `z_shift`、`robust_z_shift`、`mean_delta`。

4. `raw_metric_row_count` / `raw_trace_row_count` / `raw_log_row_count`
   对 metric、trace、log 的 service-level row count 枚举
   `count_delta`、`count_rise`、`count_drop`。

5. `raw_trace_categorical`
   对 status/code/endpoint/route/span/method 等 trace categorical 字段计算
   distribution shift。

6. `raw_trace_error_rate`
   对 status-like trace 字段计算 error-rate delta。

7. `raw_trace_numeric`
   对 duration/latency/elapsed 等 trace numeric 字段计算
   `z_shift`、`robust_z_shift`、`mean_delta`。

8. `raw_log_categorical`
   对 template/level/severity/message-template 等 log 字段计算 distribution shift。

9. `raw_topology_edge_count` / `raw_topology_distribution`
   从 raw trace edges 计算 edge count rise/drop/delta 和 caller/callee distribution shift。

字段选择只依赖 schema、dtype、alias 和最小覆盖率，不使用服务名、datapack 名、
fault 名或任何 per-incident GT 规则。

### 20.4 Offline Optimization

离线合成流程：

1. 对所有 incident 一次性提取候选 feature matrices；
2. 每个 incident 内使用 CREST 的 `_robust_case_feature_matrix` 做 case scaling；
3. seed 配置来自当前 CREST role families 和 default MEOL role priors；
4. 用单 feature rank proxy 筛选候选；
5. 用 deterministic greedy 加入能提升目标的 operator/role；
6. 用 coordinate search 优化 selected operators 的 role assignment；
7. prune 删除不伤 objective 的 operator。

目标函数严格按下面顺序比较：

```text
AC@1 -> MRR -> AC@3 -> AC@5 -> fewer selected operators
```

评分路径使用 CREST-MEO role-vector 语义：

```text
mutation = feature_matrix @ role_weight_matrix[:, mutation]
propagation = feature_matrix @ role_weight_matrix[:, propagation]
observability_bias = feature_matrix @ role_weight_matrix[:, observability_bias]
topology_context = feature_matrix @ role_weight_matrix[:, topology_context]
local_abnormality = saturating(mutation + propagation + observability_bias + topology_context)
score = local_abnormality * explanatory_power + denoised_support
```

其中 `explanatory_power` 使用当前 CREST parent-context 和 MEO soft counterfactual
explain-away 逻辑。GT 只用于比较不同全局配置的 hit@k，不参与任何 incident 的
feature value 计算。

### 20.5 主 Artifact 语义

默认输出：

```text
output/rcabench-platform-v2/crest_meo_oracle/oracle_evidence_operators.json
```

文件类型：

```text
artifact_type = oracle_raw_telemetry_operator_synthesis
oracle_scope = global_raw_telemetry_operator_and_role_synthesis
```

主 artifact 包含：

- 全局 operator specs；
- 每个 operator 的 `selected` 标记；
- learned `role_prior`；
- `role_families`；
- `counterfactual_mutation_features`；
- `counterfactual_propagation_features`；
- candidate-space metadata；
- synthesis metrics 和 search history；
- policy flags，标明 GT 只用于离线 synthesis。

主 artifact 不包含：

- `cases`；
- per-incident GT vector；
- service-name weight；
- telemetry feature bank keyed by GT；
- historical output/rank references；
- datapack-specific lookup table。

### 20.6 生成命令与当前结果

当前全量生成命令：

```bash
uv run --package evidencerank python VibeResearchTools/crest_meo_universal_oracle.py \
  --dataset rcabench \
  --workers 32 \
  --max-candidates 40 \
  --coordinate-passes 1
```

实际运行耗时：

```text
elapsed=55:30.40
```

当前结果：

```text
total=1422
error=0
operator_count=208
selected_operator_count=24
AC@1=0.890999
MRR=0.931160
AC@3=0.969058
AC@5=0.988748
```

Selected operator 分布：

```text
operator_family:
  crest_feature=11
  meol_operator=4
  raw_metric_value=6
  raw_trace_numeric=2
  raw_log_categorical=1

source:
  metric=8
  trace=11
  log=5

role:
  mutation=8
  propagation=6
  observability_bias=8
  topology_context=2
```

Reference 输出：

```text
output/rcabench-platform-v2/data/rcabench/<datapack>/crest_meo_oracle_role_synthesis/output.parquet
output/rcabench-platform-v2/data/rcabench/<datapack>/crest_meo_oracle_role_synthesis/perf.parquet
output/rcabench-platform-v2/crest_meo_oracle/role_synthesis_reference_result_summary.json
```

### 20.7 Deprecated Oracle Variants

之前的 case-indicator artifact 只保留为 pipeline sanity check，不是论文主 Oracle。
它直接把 service-level GT signal 写入 per-incident artifact，因此不能代表
MEO 能生成的 operator library。

之前的 service-name calibration / GT telemetry prototype-bank 版本也作废。它们虽然
可以被描述为 benchmark-level shared features，但仍然把 GT 服务身份或 GT telemetry
样本库编码进 feature space，不符合当前 Oracle 定义。后续论文和实验默认只使用
`artifact_type=oracle_raw_telemetry_operator_synthesis` 的 raw-telemetry synthesis
artifact。

旧脚本和输出路径只用于 sanity check：

```text
VibeResearchTools/crest_meo_oracle.py
VibeResearchTools/crest_meo_oracle_reference.py
output/rcabench-platform-v2/crest_meo_oracle/case_indicator_oracle.json
```
