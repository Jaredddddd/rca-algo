"""CREST: Counterfactual Ranking of Evidence via Structural Topology.

The runtime path is intentionally label-free and model-free. It consumes only
the normal/abnormal telemetry frames exposed by the benchmark adapter.


主要改动在 crest.py：保留原 residual 仲裁，再加两段 raw-trace 结构门控：
1、incoming caller symptom cluster 仲裁；
2、server protocol/path drift + fan-in 仲裁。
没有读 label/injection/output/conclusion，也没有 hardcode service/datapack/fault。严格说，我用了 3 个命名 eligibility guard 常量，不是 feature weight；我已在文档里标成 remaining risk，后续如果你要“完全无常量”的版本，可以继续把它替换成 case-local plateau estimator。



这两个仲裁的共同思想是：**不再让 residual 作为一个自由加分项，而是把它包装成“局部解释权”的门控**。也就是说，只有当一个 near-tie 候选能解释当前 top1 为什么像“受害者/症状面”时，才允许它把 top1 翻过来。

**Incoming Caller Symptom Cluster**
对应代码：[crest.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/crest.py:684)、[crest.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/crest.py:836)

直觉是：如果某个服务是真 root，它的异常不一定表现为最高总分；但它的上游 caller 往往会同时出现传播症状，比如 duration、count、log、错误面被放大。  
所以我们问：

> 一个候选服务是否能解释多个 incoming caller 的传播症状？

具体就是：

- 候选必须已经在 top-5 附近，不能从很深位置空降；
- 候选 trace mutation 更强，例如 endpoint/status/count-drop 这类更像 root-owned mutation；
- 候选 propagation 不高于当前 winner，避免把更像受害者的节点抬上来；
- 至少有两个 incoming caller 的 propagation 比候选更重，形成“症状簇”。

这不是在奖励“中心节点”，而是在找一种局部因果形状：

```text
caller A symptom ↑
caller B symptom ↑
        \ /
     candidate mutation ↑
```

如果只有一个 caller 异常，太容易是偶然传播；两个以上 caller 同时被 candidate 解释，就更像 root 改变了接口/行为，导致多个调用方受影响。

**Server Protocol/Path Drift + Fan-in**
对应代码：[crest.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/crest.py:733)、[crest.py](/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/crest.py:894)

这个机制针对 request/response mutation 类 case。单看 protocol/path drift 很危险，因为入口服务、下游症状面也会出现 path/status/method 分布变化。所以这里加了结构绑定：

- 候选也必须是 near-tie；
- 候选 server-side span/method/status 分布漂移更强；
- 候选 fan-in 更高，也就是有更多 incoming caller；
- 候选 observability volume 更高，说明这个漂移有足够样本支撑；
- 候选 propagation 不能比 winner 高太多，防止抬传播受害者。

它的思想是：

```text
不是“谁 path drift 大谁是 root”
而是“谁在服务端拥有 path/protocol drift，并且被更多 caller 共同指向”
```

所以它更像“协议所有权仲裁”。当当前 winner 只是一个被影响的高分症状面，而 near-tie candidate 才是 server-side API/path/status 变化的拥有者时，才翻转 top1。

一句话总结：  
**cluster 仲裁看“这个候选能不能解释多个 caller 的传播症状”；path/fanin 仲裁看“这个候选是不是协议/路径漂移的服务端拥有者”。** 两者都只做局部 top1 仲裁，不做全局重排。


"""

from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from rcabench_platform.v2.algorithms.spec import (
    Algorithm,
    AlgorithmAnswer,
    AlgorithmArgs,
)
from rcabench_platform.v2.logging import timeit

from .cera import (
    ALL_MODALITIES,
    BASE_FEATURE_NAMES,
    MODALITY_FEATURES,
    _apply_arc_trace_endpoint_support_gate,
    _apply_parent_context,
    _build_feature_matrix,
    _clean_service,
    _collect_services_from_frames,
    _distribution_shift_by_service,
    _load_input_frames,
    _series_service,
)


CREST_ROLE_FAMILIES: dict[str, tuple[str, ...]] = {
    "metric_shift": (
        "metric_max_z",
        "metric_mean_z",
        "metric_anomaly_count",
        "metric_value_delta",
        "metric_count_drop_shift",
    ),
    "trace_mutation": (
        "trace_endpoint_shift",
        "trace_error_rate",
        "trace_status_code_shift",
    ),
    "trace_propagation": (
        "trace_duration_z",
        "trace_duration_delta",
        "trace_count_delta",
        "trace_count_rise_shift",
        "trace_count_drop_shift",
        "trace_self_duration_relative_shift",
    ),
    "log_shift": (
        "log_count_delta",
        "log_error_rate",
        "log_template_delta",
    ),
    "observability_volume": (
        "abnormal_metric_rows",
        "abnormal_trace_rows",
    ),
    "topology_context": (
        "topology_in_degree",
        "topology_out_degree",
    ),
}

CREST_COUNTERFACTUAL_MUTATION_FEATURES = frozenset({
    "metric_count_drop_shift",
    "trace_count_drop_shift",
    "trace_endpoint_shift",
    "trace_error_rate",
    "trace_status_code_shift",
})

CREST_COUNTERFACTUAL_PROPAGATION_FEATURES = frozenset({
    "trace_duration_z",
    "trace_duration_delta",
    "trace_self_duration_relative_shift",
    "trace_count_delta",
    "trace_count_rise_shift",
    "abnormal_trace_rows",
    "log_count_delta",
    "log_template_delta",
})

CREST_COUNTERFACTUAL_ITERATION_FAMILIES = tuple(
    family
    for family in CREST_ROLE_FAMILIES
    if family not in {"observability_volume", "topology_context"}
)

CREST_CASE_SCALE_CLIP = 3.0
CREST_DENOISED_CHANNEL_EXCLUDES = frozenset({"trace_duration_z"})
CREST_RESIDUAL_CLUSTER_SCORE_FLOOR = 0.98
CREST_RESIDUAL_PATH_SCORE_FLOOR = 0.985
CREST_RESIDUAL_PROPAGATION_SLACK = 1.4


def _finite_nonnegative_array(values: np.ndarray) -> np.ndarray:
    clean = np.nan_to_num(
        values.astype(np.float64, copy=False),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    return np.maximum(clean, 0.0)


def _saturating_incident_scale(values: np.ndarray) -> np.ndarray:
    """Map one incident-local evidence vector into [0, 1].

    The scale is the median positive value inside the current incident. This is
    a nonparametric density-drift view: a service is large only relative to the
    normality shifts observed in the same case.
    """
    clean = _finite_nonnegative_array(values)
    positive = clean[clean > 0.0]
    if positive.size == 0:
        return np.zeros_like(clean, dtype=np.float64)

    scale = float(np.median(positive))
    if scale <= 1e-12:
        scale = float(np.max(positive))
    if scale <= 1e-12:
        return np.zeros_like(clean, dtype=np.float64)

    scaled = 1.0 - np.exp(-clean / scale)
    peak = float(np.max(scaled))
    if peak > 1e-12:
        scaled = scaled / peak
    return np.clip(scaled, 0.0, 1.0)


def _robust_case_feature_matrix(matrix: np.ndarray) -> np.ndarray:
    clean_matrix = np.nan_to_num(matrix, nan=0.0, posinf=0.0, neginf=0.0)
    clean_matrix = np.maximum(clean_matrix, 0.0)
    scaled = np.zeros_like(clean_matrix, dtype=np.float64)
    for column_idx in range(clean_matrix.shape[1]):
        column = clean_matrix[:, column_idx]
        positive = column[column > 0.0]
        if positive.size == 0:
            continue
        scale = (
            float(np.percentile(positive, 95))
            if positive.size > 1
            else float(positive[0])
        )
        if not math.isfinite(scale) or scale <= 0.0:
            scale = float(np.max(positive))
        if not math.isfinite(scale) or scale <= 0.0:
            continue
        scaled[:, column_idx] = np.clip(column / scale, 0.0, CREST_CASE_SCALE_CLIP)
    return scaled


def _family_burdens(
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
) -> dict[str, np.ndarray]:
    burdens: dict[str, np.ndarray] = {}
    for family, feature_names in CREST_ROLE_FAMILIES.items():
        indices = [
            idx
            for idx, feature_name in enumerate(enabled_features)
            if feature_name in feature_names
        ]
        burdens[family] = (
            matrix[:, indices].sum(axis=1).astype(np.float64)
            if indices
            else np.zeros(matrix.shape[0], dtype=np.float64)
        )
    return burdens


def _local_family_energy(
    matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    include_topology: bool,
) -> np.ndarray:
    families = _family_burdens(matrix, enabled_features)
    excluded = set() if include_topology else {"topology_context"}
    energy = np.zeros(matrix.shape[0], dtype=np.float64)
    for family, values in families.items():
        if family not in excluded:
            energy += values
    return np.maximum(energy, 0.0)


def _positive_p95_scaled_sum(
    matrix: np.ndarray,
    indices: list[int],
) -> np.ndarray:
    if not indices:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    values = matrix[:, indices].sum(axis=1).astype(np.float64)
    positive = values[np.isfinite(values) & (values > 0.0)]
    if positive.size == 0:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    scale = (
        float(np.percentile(positive, 95))
        if positive.size > 1
        else float(positive[0])
    )
    if not math.isfinite(scale) or scale <= 0.0:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    return np.clip(
        values / scale,
        0.0,
        CREST_CASE_SCALE_CLIP * float(len(indices)),
    )


def _trace_density_context_weight(
    services: list[str],
    trace_edges: list[tuple[str, str]],
) -> float:
    if not services:
        return 0.0
    service_set = set(services)
    valid_edges = {
        (parent, child)
        for parent, child in trace_edges
        if parent in service_set and child in service_set and parent != child
    }
    average_edge_degree = float(len(valid_edges)) / float(len(services))
    return 1.0 / (1.0 + average_edge_degree)


def _apply_counterfactual_explain_away_once(
    services: list[str],
    structural_energy: np.ndarray,
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
) -> np.ndarray:
    if not trace_edges or structural_energy.size == 0:
        return structural_energy

    service_to_idx = {service: idx for idx, service in enumerate(services)}
    adjusted = structural_energy.astype(np.float64, copy=True)
    mutation_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name in CREST_COUNTERFACTUAL_MUTATION_FEATURES
    ]
    propagation_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name in CREST_COUNTERFACTUAL_PROPAGATION_FEATURES
    ]
    if not mutation_indices or not propagation_indices:
        return structural_energy

    mutation = _positive_p95_scaled_sum(role_matrix, mutation_indices)
    propagation = _positive_p95_scaled_sum(role_matrix, propagation_indices)
    best_by_victim: dict[int, tuple[int, int, float]] = {}

    def add_pair(root_idx: int, victim_idx: int) -> None:
        if root_idx == victim_idx or adjusted[victim_idx] <= adjusted[root_idx]:
            return

        mutation_excess = max(0.0, float(mutation[root_idx] - mutation[victim_idx]))
        propagation_excess = max(
            0.0,
            float(propagation[victim_idx] - propagation[root_idx]),
        )
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
        if not math.isfinite(transfer) or transfer <= 0.0:
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


def _apply_counterfactual_explain_away(
    services: list[str],
    structural_energy: np.ndarray,
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    trace_edges: list[tuple[str, str]],
) -> np.ndarray:
    adjusted = structural_energy.astype(np.float64, copy=True)
    for _family in CREST_COUNTERFACTUAL_ITERATION_FAMILIES:
        updated = _apply_counterfactual_explain_away_once(
            services,
            adjusted,
            role_matrix,
            enabled_features,
            trace_edges,
        )
        if np.linalg.norm(updated - adjusted) <= 1e-12 * (
            np.linalg.norm(adjusted) + 1e-12
        ):
            return updated
        adjusted = updated
    return adjusted


def _denoised_channel_energy(
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
) -> np.ndarray:
    indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name not in CREST_DENOISED_CHANNEL_EXCLUDES
    ]
    if not indices:
        return np.zeros(role_matrix.shape[0], dtype=np.float64)
    return role_matrix[:, indices].sum(axis=1).astype(np.float64)


def _derive_parent_service(data: pd.DataFrame) -> pd.DataFrame:
    if "parent_service" in data.columns:
        return data
    required = {"span_id", "parent_span_id", "service_name"}
    if not required.issubset(data.columns):
        return data
    span_to_service = {
        span_id: service
        for span_id, service in data[["span_id", "service_name"]].itertuples(
            index=False,
            name=None,
        )
        if _clean_service(span_id) is not None and _clean_service(service) is not None
    }
    data = data.copy()
    data["parent_service"] = data["parent_span_id"].map(span_to_service)
    return data


def _weighted_trace_graph(
    frames: dict[str, pd.DataFrame],
    services: list[str],
) -> dict[int, list[tuple[int, float]]]:
    service_to_idx = {service: idx for idx, service in enumerate(services)}
    abnormal = frames.get("abnormal_traces", pd.DataFrame())
    normal = frames.get("normal_traces", pd.DataFrame())
    data = abnormal if abnormal is not None and not abnormal.empty else normal
    if data is None or data.empty:
        return {}

    data = _derive_parent_service(data.copy())
    if "parent_service" not in data.columns:
        return {}

    data["service_name"] = _series_service(data)
    data["parent_service"] = data["parent_service"].map(_clean_service)
    edge_counts: dict[tuple[int, int], float] = defaultdict(float)
    for parent, child in data[["parent_service", "service_name"]].dropna().itertuples(
        index=False,
        name=None,
    ):
        parent_idx = service_to_idx.get(str(parent))
        child_idx = service_to_idx.get(str(child))
        if parent_idx is None or child_idx is None or parent_idx == child_idx:
            continue
        edge_counts[(parent_idx, child_idx)] += 1.0

    out_totals: dict[int, float] = defaultdict(float)
    for (parent_idx, _child_idx), count in edge_counts.items():
        out_totals[parent_idx] += count

    graph: dict[int, list[tuple[int, float]]] = defaultdict(list)
    for (parent_idx, child_idx), count in edge_counts.items():
        total = out_totals[parent_idx]
        if total > 0.0:
            graph[parent_idx].append((child_idx, count / total))
    return dict(graph)


def _incident_graph_decay(graph: dict[int, list[tuple[int, float]]]) -> float:
    if not graph:
        return 0.0
    branching = np.asarray([len(children) for children in graph.values()], dtype=np.float64)
    mean_branching = float(np.mean(branching)) if branching.size else 0.0
    if mean_branching <= 0.0:
        return 0.0
    return 1.0 / math.sqrt(1.0 + mean_branching)


def _counterfactual_explanatory_power(
    local_abnormality: np.ndarray,
    graph: dict[int, list[tuple[int, float]]],
) -> np.ndarray:
    total_energy = float(np.sum(local_abnormality))
    if total_energy <= 1e-12:
        return np.zeros_like(local_abnormality, dtype=np.float64)
    if not graph:
        return local_abnormality / total_energy

    node_count = local_abnormality.shape[0]
    decay = _incident_graph_decay(graph)
    if decay <= 0.0:
        return local_abnormality / total_energy

    explanatory = np.zeros(node_count, dtype=np.float64)
    for source_idx in range(node_count):
        impact = np.zeros(node_count, dtype=np.float64)
        frontier = np.zeros(node_count, dtype=np.float64)
        impact[source_idx] = 1.0
        frontier[source_idx] = 1.0

        for _step in range(node_count):
            next_frontier = np.zeros(node_count, dtype=np.float64)
            active = np.flatnonzero(frontier > 1e-9)
            if active.size == 0:
                break
            for parent_idx in active:
                for child_idx, edge_weight in graph.get(int(parent_idx), ()):
                    message = float(frontier[parent_idx]) * float(edge_weight) * decay
                    if message > next_frontier[child_idx]:
                        next_frontier[child_idx] = message
            if not np.any(next_frontier > 1e-9):
                break
            impact = 1.0 - (1.0 - impact) * (1.0 - np.clip(next_frontier, 0.0, 1.0))
            frontier = next_frontier

        explanatory[source_idx] = float(np.dot(local_abnormality, impact) / total_energy)

    return np.clip(explanatory, 0.0, 1.0)


def _topology_influence_matrix(
    graph: dict[int, list[tuple[int, float]]],
    node_count: int,
) -> np.ndarray:
    """Return max decayed directed influence from each candidate to each node."""
    influence = np.zeros((node_count, node_count), dtype=np.float64)
    if node_count <= 0 or not graph:
        return influence

    decay = _incident_graph_decay(graph)
    if decay <= 0.0:
        return influence

    for source_idx in range(node_count):
        frontier = np.zeros(node_count, dtype=np.float64)
        frontier[source_idx] = 1.0
        influence[source_idx, source_idx] = 1.0

        for _step in range(node_count):
            next_frontier = np.zeros(node_count, dtype=np.float64)
            active = np.flatnonzero(frontier > 1e-9)
            if active.size == 0:
                break
            for parent_idx in active:
                for child_idx, edge_weight in graph.get(int(parent_idx), ()):
                    if child_idx < 0 or child_idx >= node_count:
                        continue
                    message = float(frontier[parent_idx]) * float(edge_weight) * decay
                    if message > next_frontier[child_idx]:
                        next_frontier[child_idx] = message
            if not np.any(next_frontier > 1e-9):
                break
            influence[source_idx] = np.maximum(
                influence[source_idx],
                np.clip(next_frontier, 0.0, 1.0),
            )
            frontier = next_frontier

    return np.clip(influence, 0.0, 1.0)


def _crest_residual_diagnostics(
    local_abnormality: np.ndarray,
    explanatory_power: np.ndarray,
    denoised_support: np.ndarray,
    original_score: np.ndarray,
    role_matrix: np.ndarray,
    enabled_features: tuple[str, ...],
    graph: dict[int, list[tuple[int, float]]],
    eta: float,
) -> dict[str, np.ndarray]:
    """Compute parameter-light residual explanatory power for CREST-Residual."""
    node_count = local_abnormality.shape[0]
    zeros = np.zeros(node_count, dtype=np.float64)
    total_abnormality = float(np.sum(local_abnormality))
    fallback = {
        "M": zeros.copy(),
        "P": zeros.copy(),
        "R": zeros.copy(),
        "residual": np.full(node_count, max(total_abnormality, 0.0), dtype=np.float64),
        "F_residual": explanatory_power.astype(np.float64, copy=True),
        "original_crest_score": original_score.astype(np.float64, copy=True),
        "residual_score": original_score.astype(np.float64, copy=True),
        "final_score": original_score.astype(np.float64, copy=True),
    }
    if node_count == 0 or total_abnormality <= 1e-12 or not graph:
        return fallback

    mutation_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name in CREST_COUNTERFACTUAL_MUTATION_FEATURES
    ]
    propagation_indices = [
        idx
        for idx, feature_name in enumerate(enabled_features)
        if feature_name in CREST_COUNTERFACTUAL_PROPAGATION_FEATURES
    ]
    if not mutation_indices or not propagation_indices:
        return fallback

    mutation = np.clip(
        _positive_p95_scaled_sum(role_matrix, mutation_indices),
        0.0,
        1.0,
    )
    propagation = np.clip(
        _positive_p95_scaled_sum(role_matrix, propagation_indices),
        0.0,
        1.0,
    )
    fallback["M"] = mutation
    fallback["P"] = propagation
    if not np.any(mutation > 0.0) or not np.any(propagation > 0.0):
        return fallback

    influence = _topology_influence_matrix(graph, node_count)
    if not np.any(influence > 0.0):
        return fallback

    explainable = mutation[:, None] * influence * propagation[None, :]
    explainable = np.minimum(local_abnormality[None, :], explainable)
    residual = np.maximum(0.0, local_abnormality[None, :] - explainable).sum(axis=1)
    residual_power = np.clip(1.0 - residual / (total_abnormality + 1e-12), 0.0, 1.0)

    try:
        eta_value = float(eta)
    except (TypeError, ValueError):
        eta_value = 1.0
    if not math.isfinite(eta_value):
        eta_value = 1.0
    eta_value = max(0.0, eta_value)

    # R is an alternative structural estimate: it can only fill missing F
    # when the candidate itself has mutation evidence.
    residual_gain = eta_value * mutation * np.maximum(
        0.0,
        residual_power - explanatory_power,
    )
    residual_explanatory_power = np.clip(
        explanatory_power + residual_gain,
        0.0,
        1.0,
    )
    residual_score = local_abnormality * residual_explanatory_power + denoised_support
    return {
        "M": mutation,
        "P": propagation,
        "R": residual_power,
        "residual": residual,
        "F_residual": residual_explanatory_power,
        "original_crest_score": original_score.astype(np.float64, copy=True),
        "residual_score": residual_score,
        "final_score": residual_score,
    }


def _case_ordinal_ranks(values: np.ndarray, higher_is_better: bool = True) -> np.ndarray:
    clean = np.nan_to_num(
        values.astype(np.float64, copy=False),
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )
    order = np.argsort(-clean if higher_is_better else clean, kind="stable")
    ranks = np.empty(clean.shape[0], dtype=np.int64)
    ranks[order] = np.arange(1, clean.shape[0] + 1, dtype=np.int64)
    return ranks


def _near_tie_gap(scores: np.ndarray) -> float | None:
    gaps = np.maximum(0.0, scores[:-1] - scores[1:])
    positive_gaps = gaps[gaps > 1e-12]
    if positive_gaps.size == 0:
        return None
    return float(np.percentile(positive_gaps, 25))


def _bump_above_winner(
    adjusted: pd.DataFrame,
    candidate_idx: int,
    scores: np.ndarray,
    marker_column: str,
) -> pd.DataFrame:
    bump = max(abs(float(scores[0])), 1.0) * 1e-9
    adjusted.loc[adjusted.index[candidate_idx], "score"] = float(scores[0]) + bump
    if "final_score" in adjusted.columns:
        adjusted.loc[adjusted.index[candidate_idx], "final_score"] = (
            float(scores[0]) + bump
        )
    adjusted.loc[adjusted.index[candidate_idx], marker_column] = True
    return adjusted


def _apply_residual_arbitration(result: pd.DataFrame) -> pd.DataFrame:
    """Use residual evidence as a narrow near-tie ownership arbitrator."""
    required = {"score", "A", "F", "M", "P", "R", "service"}
    if len(result) < 2 or not required.issubset(result.columns):
        return result

    adjusted = result.copy()
    if "residual_arbitrated" not in adjusted.columns:
        adjusted["residual_arbitrated"] = False
    scores = adjusted["score"].to_numpy(dtype=np.float64)
    near_tie_gap = _near_tie_gap(scores)
    if near_tie_gap is None:
        return adjusted

    mutation_rank = _case_ordinal_ranks(
        adjusted["M"].to_numpy(dtype=np.float64),
        higher_is_better=True,
    )
    residual_rank = _case_ordinal_ranks(
        adjusted["R"].to_numpy(dtype=np.float64),
        higher_is_better=True,
    )
    propagation = adjusted["P"].to_numpy(dtype=np.float64)
    explanatory = adjusted["F"].to_numpy(dtype=np.float64)

    candidates: list[int] = []
    for idx in range(1, min(5, len(adjusted))):
        if scores[0] - scores[idx] > near_tie_gap + 1e-12:
            continue
        if mutation_rank[idx] >= mutation_rank[0]:
            continue
        if propagation[idx] > propagation[0] + 1e-12:
            continue
        if explanatory[idx] + 1e-12 < explanatory[0]:
            continue
        if residual_rank[idx] > 3:
            continue
        candidates.append(idx)

    if not candidates:
        return adjusted

    chosen = max(
        candidates,
        key=lambda idx: (
            float(adjusted.iloc[idx]["R"]),
            float(adjusted.iloc[idx]["score"]),
            -idx,
        ),
    )
    return _bump_above_winner(adjusted, chosen, scores, "residual_arbitrated")


def _trace_neighbor_context(
    services: list[str],
    trace_edges: list[tuple[str, str]],
    mutation: np.ndarray,
    propagation: np.ndarray,
) -> dict[str, np.ndarray]:
    service_to_idx = {service: idx for idx, service in enumerate(services)}
    node_count = len(services)
    in_neighbors: list[set[int]] = [set() for _ in services]
    out_neighbors: list[set[int]] = [set() for _ in services]
    incoming_explain_count = np.zeros(node_count, dtype=np.float64)
    incoming_winner_explainable = np.zeros(node_count, dtype=np.float64)

    for parent, child in trace_edges:
        parent_idx = service_to_idx.get(parent)
        child_idx = service_to_idx.get(child)
        if parent_idx is None or child_idx is None or parent_idx == child_idx:
            continue
        out_neighbors[parent_idx].add(child_idx)
        in_neighbors[child_idx].add(parent_idx)

    if node_count:
        winner_idx = 0
        for child_idx, parents in enumerate(in_neighbors):
            for parent_idx in parents:
                explains_parent = (
                    mutation[child_idx] > mutation[parent_idx] + 1e-12
                    and propagation[parent_idx] > propagation[child_idx] + 1e-12
                )
                if not explains_parent:
                    continue
                incoming_explain_count[child_idx] += 1.0
                if parent_idx == winner_idx:
                    incoming_winner_explainable[child_idx] = 1.0

    return {
        "in_neighbor_count": np.asarray(
            [len(neighbors) for neighbors in in_neighbors],
            dtype=np.float64,
        ),
        "out_neighbor_count": np.asarray(
            [len(neighbors) for neighbors in out_neighbors],
            dtype=np.float64,
        ),
        "incoming_explain_count": incoming_explain_count,
        "incoming_winner_explainable": incoming_winner_explainable,
    }


def _trace_server_protocol_context(
    frames: dict[str, pd.DataFrame],
    services: list[str],
) -> dict[str, np.ndarray]:
    zeros = np.zeros(len(services), dtype=np.float64)
    empty_context = {
        "server_protocol": zeros.copy(),
        "server_status_protocol": zeros.copy(),
        "server_method_span": zeros.copy(),
        "server_normal_count": zeros.copy(),
        "server_abnormal_count": zeros.copy(),
    }
    normal = frames.get("normal_traces", pd.DataFrame())
    abnormal = frames.get("abnormal_traces", pd.DataFrame())
    if normal is None or abnormal is None or normal.empty or abnormal.empty:
        return empty_context

    normal = normal.copy()
    abnormal = abnormal.copy()
    normal["service_name"] = _series_service(normal)
    abnormal["service_name"] = _series_service(abnormal)
    normal = normal.dropna(subset=["service_name"])
    abnormal = abnormal.dropna(subset=["service_name"])
    if normal.empty or abnormal.empty:
        return empty_context

    method_columns = [
        column
        for column in (
            "attr.http.request.method",
            "http.method",
            "method",
            "request_method",
        )
        if column in normal.columns or column in abnormal.columns
    ]
    status_columns = [
        column
        for column in (
            "attr.http.response.status_code",
            "http.status_code",
            "status_code",
            "attr.status_code",
            "status",
        )
        if column in normal.columns or column in abnormal.columns
    ]
    response_status_columns = [
        column
        for column in (
            "attr.http.response.status_code",
            "http.status_code",
            "status_code",
        )
        if column in normal.columns or column in abnormal.columns
    ]

    span_shift = _distribution_shift_by_service(normal, abnormal, ["span_name"])
    method_shift = _distribution_shift_by_service(normal, abnormal, method_columns)
    method_span_shift = _distribution_shift_by_service(
        normal,
        abnormal,
        ["span_name", *method_columns],
    )
    status_shift = _distribution_shift_by_service(normal, abnormal, status_columns)
    response_status_shift = _distribution_shift_by_service(
        normal,
        abnormal,
        response_status_columns,
    )
    normal_counts = normal.groupby("service_name").size()
    abnormal_counts = abnormal.groupby("service_name").size()

    server_protocol = zeros.copy()
    status_protocol = zeros.copy()
    method_span = zeros.copy()
    normal_count = zeros.copy()
    abnormal_count = zeros.copy()
    for idx, service in enumerate(services):
        status_value = max(
            status_shift.get(service, 0.0),
            response_status_shift.get(service, 0.0),
        )
        method_span_value = max(
            span_shift.get(service, 0.0),
            method_shift.get(service, 0.0),
            method_span_shift.get(service, 0.0),
        )
        status_protocol[idx] = status_value
        method_span[idx] = method_span_value
        server_protocol[idx] = max(status_value, method_span_value)
        normal_count[idx] = float(normal_counts.get(service, 0.0))
        abnormal_count[idx] = float(abnormal_counts.get(service, 0.0))

    return {
        "server_protocol": server_protocol,
        "server_status_protocol": status_protocol,
        "server_method_span": method_span,
        "server_normal_count": normal_count,
        "server_abnormal_count": abnormal_count,
    }


def _apply_incoming_cluster_arbitration(result: pd.DataFrame) -> pd.DataFrame:
    """Promote a near-tie service that explains multiple incoming symptoms."""
    required = {
        "score",
        "service",
        "trace_mutation",
        "trace_propagation",
        "incoming_explain_count",
    }
    if len(result) < 2 or not required.issubset(result.columns):
        return result

    adjusted = result.copy()
    if "residual_cluster_arbitrated" not in adjusted.columns:
        adjusted["residual_cluster_arbitrated"] = False
    scores = adjusted["score"].to_numpy(dtype=np.float64)
    top_score = float(scores[0])
    if top_score <= 0.0:
        return adjusted

    mutation_rank = _case_ordinal_ranks(
        adjusted["trace_mutation"].to_numpy(dtype=np.float64),
        higher_is_better=True,
    )
    propagation = adjusted["trace_propagation"].to_numpy(dtype=np.float64)
    cluster_count = adjusted["incoming_explain_count"].to_numpy(dtype=np.float64)
    candidates: list[int] = []
    for idx in range(1, min(5, len(adjusted))):
        if scores[idx] + 1e-12 < CREST_RESIDUAL_CLUSTER_SCORE_FLOOR * top_score:
            continue
        if cluster_count[idx] < 2.0:
            continue
        if mutation_rank[idx] >= mutation_rank[0]:
            continue
        if propagation[idx] > propagation[0] + 1e-12:
            continue
        candidates.append(idx)

    if not candidates:
        return adjusted

    chosen = max(
        candidates,
        key=lambda idx: (
            float(cluster_count[idx]),
            float(adjusted.iloc[idx]["trace_mutation"]),
            float(adjusted.iloc[idx]["score"]),
            -idx,
        ),
    )
    return _bump_above_winner(
        adjusted,
        chosen,
        scores,
        "residual_cluster_arbitrated",
    )


def _apply_path_fanin_arbitration(result: pd.DataFrame) -> pd.DataFrame:
    """Use protocol/path drift only when accompanied by broader fan-in."""
    required = {
        "score",
        "service",
        "trace_propagation",
        "observability_volume",
        "in_neighbor_count",
        "server_protocol",
        "server_method_span",
    }
    if len(result) < 2 or not required.issubset(result.columns):
        return result

    adjusted = result.copy()
    if "residual_path_fanin_arbitrated" not in adjusted.columns:
        adjusted["residual_path_fanin_arbitrated"] = False
    scores = adjusted["score"].to_numpy(dtype=np.float64)
    top_score = float(scores[0])
    if top_score <= 0.0:
        return adjusted

    propagation = adjusted["trace_propagation"].to_numpy(dtype=np.float64)
    protocol = adjusted["server_protocol"].to_numpy(dtype=np.float64)
    observability = adjusted["observability_volume"].to_numpy(dtype=np.float64)
    fanin = adjusted["in_neighbor_count"].to_numpy(dtype=np.float64)

    candidates: list[int] = []
    for idx in range(1, min(5, len(adjusted))):
        if scores[idx] + 1e-12 < CREST_RESIDUAL_PATH_SCORE_FLOOR * top_score:
            continue
        if protocol[idx] <= protocol[0] + 1e-12:
            continue
        if observability[idx] <= observability[0] + 1e-12:
            continue
        if fanin[idx] <= fanin[0] + 1e-12:
            continue
        if (
            propagation[idx]
            > CREST_RESIDUAL_PROPAGATION_SLACK * propagation[0] + 1e-12
        ):
            continue
        candidates.append(idx)

    if not candidates:
        return adjusted

    chosen = max(
        candidates,
        key=lambda idx: (
            float(protocol[idx]),
            float(fanin[idx]),
            float(observability[idx]),
            float(adjusted.iloc[idx]["score"]),
            -idx,
        ),
    )
    return _bump_above_winner(
        adjusted,
        chosen,
        scores,
        "residual_path_fanin_arbitrated",
    )


def _apply_residual_structural_arbitration(result: pd.DataFrame) -> pd.DataFrame:
    result = result.copy()
    for marker in (
        "residual_arbitrated",
        "residual_cluster_arbitrated",
        "residual_path_fanin_arbitrated",
    ):
        if marker not in result.columns:
            result[marker] = False

    sort_f_column = "F_residual" if "F_residual" in result.columns else "F"
    sort_columns = ["score", "A", sort_f_column, "service"]
    result = _apply_residual_arbitration(result)
    result = result.sort_values(
        sort_columns,
        ascending=[False, False, False, True],
        kind="stable",
    ).reset_index(drop=True)
    result = _apply_incoming_cluster_arbitration(result)
    result = result.sort_values(
        sort_columns,
        ascending=[False, False, False, True],
        kind="stable",
    ).reset_index(drop=True)
    result = _apply_path_fanin_arbitration(result)
    return result.sort_values(
        sort_columns,
        ascending=[False, False, False, True],
        kind="stable",
    ).reset_index(drop=True)


def _pagerank_explanatory_power(
    local_abnormality: np.ndarray,
    graph: dict[int, list[tuple[int, float]]],
) -> np.ndarray:
    total_energy = float(np.sum(local_abnormality))
    if total_energy <= 1e-12:
        return np.zeros_like(local_abnormality, dtype=np.float64)
    if not graph:
        return local_abnormality / total_energy

    node_count = local_abnormality.shape[0]
    teleport = local_abnormality / total_energy
    rank = teleport.copy()
    linked_nodes = set(graph)
    damping = _incident_graph_decay(graph)
    for _step in range(max(1, node_count)):
        next_rank = (1.0 - damping) * teleport
        dangling_mass = float(np.sum(rank[[idx for idx in range(node_count) if idx not in linked_nodes]]))
        next_rank += damping * dangling_mass * teleport
        for parent_idx, children in graph.items():
            parent_mass = damping * float(rank[parent_idx])
            for child_idx, edge_weight in children:
                next_rank[child_idx] += parent_mass * float(edge_weight)
        rank = next_rank

    return _saturating_incident_scale(rank)


def score_crest_services(
    input_folder: Path,
    enabled_modalities: frozenset[str] = ALL_MODALITIES,
    graph_mode: str = "counterfactual",
    residual_eta: float | None = None,
    residual_arbitration: bool = False,
) -> pd.DataFrame:
    frames = _load_input_frames(input_folder)
    services = _collect_services_from_frames(frames)
    if not services:
        return pd.DataFrame(columns=["service", "A", "F", "S", "score"])

    enabled_feature_set = frozenset().union(
        *(MODALITY_FEATURES[modality] for modality in enabled_modalities)
    )
    enabled_features = tuple(
        feature
        for feature in BASE_FEATURE_NAMES
        if feature in enabled_feature_set
    )
    matrix, trace_edges = _build_feature_matrix(
        frames,
        services,
        enabled_features,
        enabled_modalities,
        normalize=True,
    )
    case_matrix = _robust_case_feature_matrix(matrix)
    role_matrix = _apply_arc_trace_endpoint_support_gate(enabled_features, case_matrix)
    local_energy = _local_family_energy(
        role_matrix,
        enabled_features,
        include_topology=True,
    )
    local_abnormality = _saturating_incident_scale(local_energy)

    graph = _weighted_trace_graph(frames, services) if "trace" in enabled_modalities else {}
    denoised_support = np.zeros_like(local_abnormality, dtype=np.float64)
    if graph_mode == "local":
        explanatory_power = np.ones_like(local_abnormality, dtype=np.float64)
    elif graph_mode == "pagerank":
        explanatory_power = _pagerank_explanatory_power(local_abnormality, graph)
    else:
        structural_seed = _local_family_energy(
            role_matrix,
            enabled_features,
            include_topology=True,
        )
        context_weight = _trace_density_context_weight(services, trace_edges)
        structural_energy = _apply_parent_context(
            services,
            structural_seed,
            trace_edges,
            context_weight,
        )
        structural_energy = _apply_counterfactual_explain_away(
            services,
            np.maximum(structural_energy, 0.0),
            role_matrix,
            enabled_features,
            trace_edges,
        )
        explanatory_power = _saturating_incident_scale(structural_energy)

        denoised_energy = _denoised_channel_energy(role_matrix, enabled_features)
        denoised_structural = _apply_parent_context(
            services,
            denoised_energy,
            trace_edges,
            context_weight,
        )
        denoised_structural = _apply_counterfactual_explain_away(
            services,
            np.maximum(denoised_structural, 0.0),
            role_matrix,
            enabled_features,
            trace_edges,
        )
        denoised_support = _saturating_incident_scale(denoised_structural)

    score = local_abnormality * explanatory_power
    if graph_mode == "counterfactual":
        score = score + denoised_support
    if not np.any(score > 0.0) and np.any(local_abnormality > 0.0):
        score = local_abnormality.copy()
    families = _family_burdens(role_matrix, enabled_features)
    neighbor_context = _trace_neighbor_context(
        services,
        trace_edges,
        _finite_nonnegative_array(families["trace_mutation"]),
        _finite_nonnegative_array(families["trace_propagation"]),
    )
    protocol_context = (
        _trace_server_protocol_context(frames, services)
        if "trace" in enabled_modalities
        else {
            "server_protocol": np.zeros(len(services), dtype=np.float64),
            "server_status_protocol": np.zeros(len(services), dtype=np.float64),
            "server_method_span": np.zeros(len(services), dtype=np.float64),
            "server_normal_count": np.zeros(len(services), dtype=np.float64),
            "server_abnormal_count": np.zeros(len(services), dtype=np.float64),
        }
    )

    columns = {
        "service": services,
        "A": local_abnormality,
        "F": explanatory_power,
        "S": denoised_support,
        "score": score,
    }
    columns.update(families)
    columns.update(neighbor_context)
    columns.update(protocol_context)
    sort_f_column = "F"
    if residual_eta is not None and graph_mode == "counterfactual":
        residual = _crest_residual_diagnostics(
            local_abnormality,
            explanatory_power,
            denoised_support,
            score,
            role_matrix,
            enabled_features,
            graph,
            residual_eta,
        )
        score = residual["final_score"]
        columns.update(residual)
        columns["score"] = score
        sort_f_column = "F_residual"

    result = pd.DataFrame(columns)
    result = result.sort_values(
        ["score", "A", sort_f_column, "service"],
        ascending=[False, False, False, True],
        kind="stable",
    ).reset_index(drop=True)
    if residual_eta is not None and residual_arbitration:
        result = _apply_residual_structural_arbitration(result)
    if residual_eta is not None:
        result["final_rank"] = np.arange(1, len(result) + 1, dtype=np.int64)
    return result


def _export_crest_residual_diagnostics(
    ranking: pd.DataFrame,
    args: AlgorithmArgs,
) -> None:
    output_folder = getattr(args, "output_folder", None)
    if output_folder is None:
        return

    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    diagnostics = ranking.copy()
    case_id = getattr(args, "datapack", None)
    if case_id is not None and "case_id" not in diagnostics.columns:
        diagnostics.insert(0, "case_id", str(case_id))

    parquet_path = output_folder / "crest_residual_diagnostics.parquet"
    try:
        diagnostics.to_parquet(parquet_path, index=False)
    except Exception:
        diagnostics.to_csv(parquet_path.with_suffix(".csv"), index=False)


class CREST(Algorithm):
    """CREST ranking with counterfactual structural support."""

    _modalities: frozenset[str] = ALL_MODALITIES
    _graph_mode = "counterfactual"
    _residual_eta: float | None = None
    _residual_arbitration = False
    _export_residual_diagnostics = False

    def needs_cpu_count(self) -> int | None:
        return 1

    @timeit()
    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        ranking = score_crest_services(
            args.input_folder,
            enabled_modalities=self._modalities,
            graph_mode=self._graph_mode,
            residual_eta=self._residual_eta,
            residual_arbitration=self._residual_arbitration,
        )
        if self._export_residual_diagnostics:
            _export_crest_residual_diagnostics(ranking, args)
        return [
            AlgorithmAnswer(level="service", name=str(row.service), rank=rank)
            for rank, row in enumerate(ranking.itertuples(index=False), start=1)
        ]


class CRESTResidual(CREST):
    """CREST-Residual with gated incident-level residual explanatory power."""

    _residual_eta = 1.0
    _residual_arbitration = True
    _export_residual_diagnostics = True


class CRESTLocal(CREST):
    """CREST-Local ablation: Module 1 only."""

    _graph_mode = "local"


class CRESTNoCF(CREST):
    """CREST-NoCF ablation: local abnormality plus PageRank-style graph prior."""

    _graph_mode = "pagerank"


class CRESTMetric(CREST):
    """CREST ablation using only metric evidence."""

    _modalities = frozenset({"metric"})


class CRESTTrace(CREST):
    """CREST ablation using only trace evidence."""

    _modalities = frozenset({"trace"})


class CRESTLog(CREST):
    """CREST ablation using only log evidence."""

    _modalities = frozenset({"log"})


class CRESTMetricTrace(CREST):
    """CREST ablation using metric and trace evidence."""

    _modalities = frozenset({"metric", "trace"})


class CRESTMetricLog(CREST):
    """CREST ablation using metric and log evidence."""

    _modalities = frozenset({"metric", "log"})


class CRESTLogTrace(CREST):
    """CREST ablation using log and trace evidence."""

    _modalities = frozenset({"log", "trace"})
