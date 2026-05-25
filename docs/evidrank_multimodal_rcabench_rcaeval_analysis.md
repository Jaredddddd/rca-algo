# EvidRank Multimodal Behavior On RCABench And RCAEval

## Context

The observed phenomenon is:

- On RCABench, EvidRank improves when metric, log, and trace evidence are combined.
- On RCAEval RE2, metric-only is usually best, while adding log and especially trace can reduce accuracy.

The comparison used these local artifacts:

- RCABench implementation: `aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py`
- RCABench results: `aegis/rca-algo-contrib/algorithms/evidencerank/README.md`
- RCAEval implementation: `DDS-DL-AIOPS/RCAEval/RCAEval/e2e/evidence_rank.py`
- RCAEval results: `DDS-DL-AIOPS/RCAEval/EvidRank_abulation_results.md`
- RCAEval RE2 data: `DDS-DL-AIOPS/RCAEval-V1-Data`

## Findings

The original reversal in V1 was caused by both dataset characteristics and an RCAEval-specific trace adaptation issue. After the V3 fix, the remaining pattern where `metric` is still usually best on RCAEval RE2 is mainly a dataset/evidence-quality difference, not the repeated-edge adapter bug.

### 1. RCAEval trace score is dominated by repeated span edges

In `RCAEval/e2e/evidence_rank.py`, `_trace_parent_edges()` returns one edge per span occurrence, not one unique topology edge. `_score_traces()` then adds `0.05` to the source and target service for every returned edge occurrence.

For sampled RE2 cases:

| Case | Abnormal trace rows | Edge occurrences | Unique edges | Top trace score with edge boost | Top trace score without edge boost |
| --- | ---: | ---: | ---: | ---: | ---: |
| RE2-OB `checkoutservice_cpu/1` | 195425 | 84063 | 9 | 3764.24 | 14.48 |
| RE2-TT `ts-travel-service_loss/1` | 439563 | 89216 | 55 | 1836.71 | 16.97 |

Before V3, this made `all` effectively become trace-only:

- RE2-OB `all`: top1 evidence category was trace in 90/90 cases.
- RE2-TT `all`: top1 evidence category was trace in 72/90 cases.
- RE2-OB `all` and `trace-only` have the same aggregate service-level scores in the recorded ablation table.

RCABench does not have this problem: its trace edges are deduplicated with `drop_duplicates()` before topology features are added, and the final feature values are `log1p` normalized before summing. The RCAEval adapter now deduplicates trace parent edges as well.

### V3 recheck: remaining drop is mostly data/evidence quality()

V3 uses deduplicated trace edges and keeps raw score summation, matching the RCABench-compatible baseline rather than the intermediate per-modality normalization experiment.

Latest V3 averages:

| Dataset | Metric T1/T3/A5 | Metric+Log T1/T3/A5 | All T1/T3/A5 | Log T1 | Trace T1 |
| --- | --- | --- | --- | ---: | ---: |
| RE2-OB | 0.80 / 0.97 / 0.93 | 0.54 / 0.86 / 0.80 | 0.71 / 0.97 / 0.91 | 0.19 | 0.21 |
| RE2-SS | 0.91 / 0.99 / 0.97 | 0.81 / 0.97 / 0.94 | 0.81 / 0.97 / 0.94 | 0.12 | 0.00 |
| RE2-TT | 0.79 / 0.91 / 0.89 | 0.73 / 0.89 / 0.84 | 0.76 / 0.92 / 0.88 | 0.08 | 0.02 |

Case-level comparison against metric-only:

| Dataset | All fixes metric-only misses at Top1 | All hurts metric-only hits at Top1 | Top1 modality in `all` |
| --- | ---: | ---: | --- |
| RE2-OB | 5 | 13 | metric 49, trace 40, log 1 |
| RE2-SS | 1 | 10 | metric 75, log 15 |
| RE2-TT | 9 | 12 | trace 47, metric 36, log 7 |

Important implications:

- RE2-SS has no usable trace file in the sampled V3 run, so `all == metric+log`; the drop below `metric` is caused by log evidence, not trace adaptation.
- `metric+log` in V3 matches the V1 aggregate numbers, which means the metric/log path was not changed by the trace fix.
- Trace-only on RE2-OB and RE2-TT has low Top1 but much better Top3/Top5, so trace often points to a symptom neighborhood rather than the injected root service.
- RCAEval RE2 metric-only is already near ceiling at Top3/Top5, leaving little room for noisy log/trace evidence to improve ranking.

### 2. RCAEval metric is unusually strong

RCAEval RE2 `simple_metrics.csv` contains service-suffixed, reduced metric features. The root service signal is often directly visible in the metric columns.

Recorded RCAEval RE2 metric-only service-level top1:

- RE2-OB: 0.80
- RE2-SS: 0.91
- RE2-TT: 0.79

This leaves little room for noisy modalities to help. Any uncalibrated log/trace score can easily displace a correct metric top1.

### 3. RCAEval log evidence is noisy and propagation-heavy

Log-only is much weaker than metric-only:

- RE2-OB: top1 0.19
- RE2-SS: top1 0.12
- RE2-TT: top1 0.08

Adding logs to metrics still changes top1 often:

- RE2-OB `metric+log`: top1 evidence category was log in 17/90 cases, reducing exact top1 hits from 72 to 49 in the inspected result files.
- RE2-TT `metric+log`: top1 evidence category was log in 39/90 cases, reducing exact top1 hits from 71 to 66.

This is consistent with logs reflecting downstream request volume and propagated symptoms, not only the injected root service.

### 4. RCAEval uses raw logs/traces even though pre-aggregated time series exist

RE2 case directories include `logts.csv`, `tracets_lat.csv`, and `tracets_err.csv`. TORAI uses those time-series style sources, but the current RCAEval EvidRank adapter reads raw `logs.csv` and `traces.csv`. The current parser uses generic count, template, duration, and edge heuristics rather than dataset-native time-series evidence.

This makes the adapter sensitive to raw event volume and service naming differences such as `frontend` vs `frontendservice`.

### 5. RCABench multimodal evidence is better calibrated

In sampled RCABench cases, modality scores stay in comparable ranges:

- Metric top scores: tens to around 75.
- Log top scores: around 14-18.
- Trace top scores: around 30-40.

The full RCABench results show net gain from multimodal evidence:

- Metric-only top1: 558/1422
- Metric+log top1: 671/1422
- Metric+trace top1: 728/1422
- Metric+log+trace top1: 754/1422

Case-level comparison of RCABench metric-only vs full:

- Top1: full fixes 300 metric-only misses, while hurting 104 metric-only hits.
- Top3: full fixes 341 metric-only misses, while hurting 88 metric-only hits.
- Top5: full fixes 345 metric-only misses, while hurting 67 metric-only hits.

## Conclusion

The phenomenon should not be interpreted as evidence that multimodal RCA is inherently useful on RCABench but harmful on RCAEval.

The best interpretation is:

1. RCAEval RE2 has much stronger metric-only signal than RCABench.
2. RCAEval raw logs/traces are noisier and more propagation-heavy.
3. The V1 RCAEval EvidRank adapter had a trace topology scoring bug: repeated span edges were added directly to service scores, causing trace to dominate the fused ranking. This is fixed in the V3 baseline.

So the severe V1 `all` collapse was primarily an adapter/scoring issue amplified by benchmark data differences. After the V3 trace dedup fix, the remaining `metric > all` result is best interpreted as a benchmark/data evidence difference: RCAEval RE2 metrics are strong, while raw logs/traces are weak or propagation-heavy under the RCABench-compatible EvidRank scoring logic.

## Compatibility Guidance

1. Deduplicate trace edges before applying topology boosts, matching the RCABench implementation's unique-edge behavior.
2. Keep raw score summation so the RCAEval adapter remains comparable with the RCABench implementation.
3. Use any per-modality normalization or weighting only as a separate algorithm variant, not as the EvidRank compatibility baseline.
4. Consider using RCAEval's `logts.csv`, `tracets_lat.csv`, and `tracets_err.csv` only in a clearly labeled RCAEval-specific variant; the compatibility baseline reads raw `logs.csv` and `traces.csv`.
5. Align service names across modalities when evaluating or explaining failures, especially Online Boutique names such as `frontend` and `frontendservice`.
6. Treat the V3 ablation as the current RCABench-compatible baseline for dataset-difference analysis.

## Applied Fix

The RCAEval EvidRank adapter now:

- deduplicates `_trace_parent_edges()` before adding topology boost, so repeated span occurrences no longer multiply service scores;
- keeps the original raw score summation fusion, matching the RCABench EvidRank implementation's sum-based ranking behavior.

An intermediate experiment tried per-modality normalization, but that changed the algorithm semantics and made weak log/trace modalities too influential on RCAEval. That experiment should not be used to judge dataset differences.


# 中文

# EvidRank多模态行为在RCABench与RCAEval上的表现

## 背景

观察到的现象如下：

- 在RCABench上，将指标、日志和追踪证据结合后，EvidRank的表现有所提升。
- 在RCAEval RE2上，仅使用指标通常效果最佳，加入日志尤其是追踪数据反而会降低准确率。

对比所用的本地文件：

- RCABench实现：`aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/algorithm.py`
- RCABench结果：`aegis/rca-algo-contrib/algorithms/evidencerank/README.md`
- RCAEval实现：`DDS-DL-AIOPS/RCAEval/RCAEval/e2e/evidence_rank.py`
- RCAEval结果：`DDS-DL-AIOPS/RCAEval/EvidRank_abulation_results.md`
- RCAEval RE2数据：`DDS-DL-AIOPS/RCAEval-V1-Data`

## 发现

这一反转现象同时源于数据集特征与RCAEval特有的适配问题。RE2-OB和RE2-TT上`all`模式严重退化的主要原因，是RCAEval适配器中的一个实现缺陷。

### 1. RCAEval追踪得分被重复的Span边主导

在`RCAEval/e2e/evidence_rank.py`中，`_trace_parent_edges()`为每次Span出现返回一条边，而非唯一的拓扑边。`_score_traces()`随后对每条返回的边，向源服务和目标服务各加`0.05`分。

采样RE2案例数据如下：

| 案例 | 异常追踪行数 | 边出现次数 | 唯一边数 | 有边增益的最高追踪得分 | 无边增益的最高追踪得分 |
|---|---:|---:|---:|---:|---:|
| RE2-OB `checkoutservice_cpu/1` | 195425 | 84063 | 9 | 3764.24 | 14.48 |
| RE2-TT `ts-travel-service_loss/1` | 439563 | 89216 | 55 | 1836.71 | 16.97 |

这导致`all`模式实际上退化为仅追踪模式：

- RE2-OB `all`：90个案例中，90个的最高证据类别均为追踪。
- RE2-TT `all`：90个案例中，72个的最高证据类别为追踪。
- RE2-OB的`all`与`仅追踪`在消融表中的聚合服务级得分完全相同。

RCABench不存在此问题：其追踪边在加入拓扑特征之前已通过`drop_duplicates()`去重，且最终特征值经`log1p`归一化后再求和。

### 2. RCAEval指标信号异常强劲

RCAEval RE2的`simple_metrics.csv`包含带服务后缀的精简指标特征，根因服务的信号往往在指标列中直接可见。

RCAEval RE2仅指标模式的服务级Top1记录结果：

- RE2-OB：0.80
- RE2-SS：0.91
- RE2-TT：0.79

如此强的基准几乎没有空间让噪声模态发挥作用，任何未经校准的日志/追踪得分都可能轻易取代正确的指标Top1。

### 3. RCAEval日志证据噪声大且传播效应明显

仅日志模式远弱于仅指标模式：

- RE2-OB：Top1 0.19
- RE2-SS：Top1 0.12
- RE2-TT：Top1 0.08

即便将日志加入指标，Top1仍会频繁改变：

- RE2-OB `指标+日志`：90个案例中17个的最高证据类别为日志，使精确Top1命中从72降至49。
- RE2-TT `指标+日志`：90个案例中39个的最高证据类别为日志，使精确Top1命中从71降至66。

这与日志反映下游请求量和传播症状而非注入根因服务的特性相吻合。

### 4. RCAEval使用原始日志/追踪，而非已有的预聚合时间序列

RE2案例目录包含`logts.csv`、`tracets_lat.csv`和`tracets_err.csv`，TORAI会使用这些时间序列风格的数据源，但当前RCAEval的EvidRank适配器读取的是原始`logs.csv`和`traces.csv`，并使用通用的计数、模板、时延和边启发式方法，而非数据集原生的时间序列证据。

这使适配器对原始事件量和服务命名差异（如`frontend`与`frontendservice`）十分敏感。

### 5. RCABench多模态证据校准更好

在采样的RCABench案例中，各模态得分保持在可比范围内：

- 指标最高分：数十至约75。
- 日志最高分：约14至18。
- 追踪最高分：约30至40。

RCABench完整结果显示多模态证据带来净收益：

- 仅指标 Top1：558/1422
- 指标+日志 Top1：671/1422
- 指标+追踪 Top1：728/1422
- 指标+日志+追踪 Top1：754/1422

RCABench仅指标与完整模式的案例级对比：

- Top1：完整模式修复了300个仅指标的错误，同时使104个正确命中变错。
- Top3：完整模式修复了341个错误，同时使88个正确命中变错。
- Top5：完整模式修复了345个错误，同时使67个正确命中变错。

## 结论

此现象不应被解读为"多模态RCA在RCABench上本质有益，而在RCAEval上本质有害"的证据。

最合理的解释是：

1. RCAEval RE2的仅指标信号远强于RCABench。
2. RCAEval原始日志/追踪噪声更大，传播效应更重。
3. 当前RCAEval EvidRank适配器存在追踪拓扑评分缺陷：重复的Span边被直接累加至服务得分，导致追踪主导融合排名。

因此，RCAEval的退化主要是适配器/评分问题，并被基准数据集差异进一步放大。

## 建议修复措施

1. 在应用拓扑增益前对追踪边去重，或移除每条边直接加`0.05`的服务增益机制。
2. 保留原始得分求和方式，使RCAEval适配器与RCABench实现保持一致。
3. 仅在独立的算法变体中使用各模态归一化或加权，不将其作为EvidRank兼容性基线。
4. 考虑仅在明确标注的RCAEval专用变体中使用`logts.csv`、`tracets_lat.csv`和`tracets_err.csv`；兼容性基线读取原始`logs.csv`和`traces.csv`。
5. 在评估或分析失败案例时，对齐各模态的服务名称，尤其是Online Boutique中`frontend`与`frontendservice`等差异。
6. 修复追踪评分后重新运行消融实验，分别报告`指标`、`指标+日志`、`指标+追踪`和`全部`的结果。

## 已应用的修复

RCAEval EvidRank适配器现已：

- 在添加拓扑增益前对`_trace_parent_edges()`去重，使重复的Span出现不再成倍累加服务得分；
- 保留原始得分求和融合方式，与RCABench EvidRank实现的基于求和的排名行为保持一致。

中间实验曾尝试各模态归一化，但这改变了算法语义，使弱日志/追踪模态在RCAEval上影响力过大。该实验结果不应用于判断数据集间的差异。