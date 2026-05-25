# Why EvidRank Multimodal Helps RCABench But Metric-Only Wins On RCAEval RE2

## Conclusion

The concrete dataset-level reason is:

**RCAEval RE2 turns RCA into a mostly metric-aligned service ranking problem, while RCABench contains many request/response/network faults whose strongest evidence is in traces and logs.**

In RCAEval RE2, every evaluated case has a target-service metric column or close metric proxy in `simple_metrics.csv`: examples include `checkoutservice_cpu`, `carts_diskio`, `ts-travel-service_socket`, and latency percentile columns such as `*_latency-50` / `*_latency-90` for delay/loss-like faults. The metric table is therefore almost isomorphic to the service-level answer space.

In RCABench, many faults are not resource-metric faults. They are request aborts, request/response delays, response code/body replacements, partitions, loss, corruptions, and method/path rewrites. Those failures often first appear as span duration/count/status changes or log/template changes rather than as a uniquely identifying CPU/mem/disk-style metric on the injected service.

This difference explains the phenomenon:

- On RCABench, metric-only misses many request/trace/log-oriented failures, so log/trace evidence adds real complementary signal.
- On RCAEval RE2, metric-only already has a near-direct signal, so adding noisy log/trace evidence more often displaces a correct metric ranking than fixes it.

## Key Evidence

### 1. RCAEval RE2 metrics are label-aligned

For the selected RE2 cases, each service/fault case has a corresponding service-level metric proxy in `simple_metrics.csv`.

| Dataset | Cases with target metric proxy | Rate |
| --- | ---: | ---: |
| RE2-OB | 90 / 90 | 1.00 |
| RE2-SS | 90 / 90 | 1.00 |
| RE2-TT | 90 / 90 | 1.00 |

Fault-to-metric mapping used by the data itself:

| Fault | Metric proxy in `simple_metrics.csv` |
| --- | --- |
| cpu | `{service}_cpu` |
| mem | `{service}_mem` |
| disk | `{service}_diskio` |
| socket | `{service}_socket` |
| delay | `{service}_latency-50`, `{service}_latency-90` |
| loss | latency/error-related service metrics, especially latency percentile proxies |

This makes metric-only very strong:

| RCAEval RE2 subset | Metric Top1 | Metric Top3 | Metric Avg@5 |
| --- | ---: | ---: | ---: |
| RE2-OB | 0.80 | 0.97 | 0.93 |
| RE2-SS | 0.91 | 0.99 | 0.97 |
| RE2-TT | 0.79 | 0.91 | 0.89 |

Once metric-only is already this close to the ceiling, multimodal fusion has little room to improve.

### 2. RCAEval logs/traces are mostly propagation and high-traffic symptoms

RCAEval RE2 raw logs and traces often rank common traffic services rather than the injected root service.

Examples from the V3 runs:

| Dataset | Log-only Top1 concentration | Trace-only Top1 concentration |
| --- | --- | --- |
| RE2-OB | `recommendationservice` is Top1 in 81/90 log-only cases | `productcatalogservice` is Top1 in 68/90 trace-only cases |
| RE2-SS | `front-end` is Top1 in 56/90 log-only cases | no usable trace file in this subset |
| RE2-TT | `ts-travel-service` and `ts-consign-service` dominate log-only Top1 | `ts-station-service` is Top1 in 77/90 trace-only cases |

This explains why adding modalities hurts top1:

| Dataset | ALL fixes metric-only Top1 misses | ALL hurts metric-only Top1 hits | Net |
| --- | ---: | ---: | ---: |
| RE2-OB | 5 | 13 | -8 |
| RE2-SS | 1 | 10 | -9 |
| RE2-TT | 9 | 12 | -3 |

RE2-SS is especially diagnostic: it has no usable trace data in the V3 run, so `ALL == metric+log`. The drop from metric-only is therefore caused by logs alone, not by trace adaptation.

### 3. RCABench contains many non-metric-aligned faults

RCABench has a much broader fault taxonomy than RCAEval RE2. Many cases are request/response/network faults whose symptoms are naturally multimodal.

Grouped by fault type:

| RCABench fault group | Cases | Metric Top1 | ALL Top1 | Net fixes from ALL |
| --- | ---: | ---: | ---: | ---: |
| Resource/app metric-aligned faults | 372 | 0.965 | 0.863 | -38 |
| Request/trace/log-oriented faults | 1050 | 0.190 | 0.412 | +234 |

The resource/app metric-aligned group includes cases such as `stress`, `container-kill`, `pod-failure`, `exception`, and similar failures. In those cases, metric-only is already very strong, and adding other modalities can hurt.

The request/trace/log-oriented group includes `request-delay`, `response-delay`, `request-abort`, `response-abort`, `request-replace-method`, `request-replace-path`, `response-replace-code`, `response-replace-body`, `partition`, `loss`, and similar failures. In these cases, metric-only is weak, while traces/logs supply the missing evidence.

This is exactly the opposite mixture from RCAEval RE2: RCABench has enough non-metric-aligned cases that the average benefits from multimodal evidence.

### 4. RCABench shows real complementarity across modalities

RCABench aggregate results:

| Method | Top1 | Top3 | Top5 |
| --- | ---: | ---: | ---: |
| Metric only | 558 / 1422 | 854 / 1422 | 970 / 1422 |
| Metric + Log | 671 / 1422 | 974 / 1422 | 1119 / 1422 |
| Metric + Trace | 728 / 1422 | 1077 / 1422 | 1188 / 1422 |
| All | 754 / 1422 | 1107 / 1422 | 1248 / 1422 |

Case-level comparison of RCABench metric-only vs all:

| K | Metric-only correct, ALL wrong | Metric-only wrong, ALL correct | Net |
| --- | ---: | ---: | ---: |
| Top1 | 104 | 300 | +196 |
| Top3 | 88 | 341 | +253 |
| Top5 | 67 | 345 | +278 |

This is not just score calibration. The additional modalities correct many cases that metric-only cannot solve.

## Why The Two Benchmarks Diverge

The divergence comes from the interaction between fault taxonomy and data representation.

RCAEval RE2 uses a compact `simple_metrics.csv` table where each service has a small fixed set of semantically obvious metric columns. The benchmark faults are also named in those same metric terms: cpu, mem, disk, socket, delay, loss. Even delay/loss cases have service-local latency percentile columns. So metric-only can often rank the right service without needing logs or traces.

RCABench uses standardized normal/abnormal OpenTelemetry-style datapacks. Its metric table is a long table of generic resource and telemetry metrics, while many injected faults are HTTP or RPC behavior changes. A response code replacement or request method rewrite does not necessarily create a unique resource metric anomaly on the injected service. It may instead appear as changed span duration, span count, status code, call topology, log count, or log template distribution.

So the same EvidRank fusion behaves differently:

- In RCAEval RE2, log/trace evidence is mostly redundant or noisy relative to a strong metric signal.
- In RCABench, log/trace evidence is complementary because many faults are not directly encoded by metric columns.

## Practical Interpretation

V3 should be interpreted as follows:

1. The previous trace repeated-edge issue was an adapter bug and has been fixed.
2. The remaining `metric-only > ALL` result on RCAEval RE2 is a dataset characteristic, not evidence that the RCABench-compatible EvidRank logic is wrong.
3. The most precise explanation is that RCAEval RE2's metric modality is unusually label-aligned, while RCABench's fault taxonomy has enough request/trace/log-oriented failures for multimodal evidence to win on average.

