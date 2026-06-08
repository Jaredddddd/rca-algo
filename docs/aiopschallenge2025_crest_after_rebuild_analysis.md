# AIOpsChallenge2025 CREST Analysis After Rebuild

Date: 2026-06-08

## Conclusion

After rebuilding `aiopschallenge2025_rcabench_service`, the low CREST score is now mainly caused by
the dataset's observability and fault-type characteristics, not by the earlier trace-status
conversion bug.

The converter fixes did work:

- trace `status_code` / `attr.status_code` is no longer all `Ok`;
- raw trace/log/metric metadata is preserved more completely;
- `redis` is normalized to `redis-cart`;
- service-level impossible cases are filtered by default.

However, aiops2025 trace still behaves very differently from RCABench trace. In aiops2025, trace is
mostly an entry/key-path traffic surface dominated by `frontend`, while many root causes are
resource/JVM/pod/service faults whose strongest root evidence is in metrics or logs. CREST's full
mode uses trace topology and counterfactual propagation (`score = A * F + S`), so it often promotes
entry/propagation services over the metric/log root.

## Current Data And Result Snapshot

Conversion report:

```text
total groundtruth rows:        400
converted service datapacks:   230
skipped node cases:             82
skipped empty cases:            37
skipped unobservable labels:    51
```

The 51 unobservable service-level cases are mostly:

```text
io fault:     26
pod failure: 25
```

These are no longer contaminating the default evaluation.

Current aiops2025 CREST-family results on 230 converted cases:

| algorithm | AC@1 | AC@3 | AC@5 | MRR |
| --- | ---: | ---: | ---: | ---: |
| `crest_metric_log` | 0.478261 | 0.821739 | 0.934783 | 0.668761 |
| `crest_metric` | 0.426087 | 0.769565 | 0.921739 | 0.621815 |
| `crest_metric_trace` | 0.369565 | 0.604348 | 0.660870 | 0.520278 |
| `crest` | 0.334783 | 0.600000 | 0.669565 | 0.503603 |
| `crest_trace` | 0.308696 | 0.495652 | 0.569565 | 0.451532 |

RCABench reference from `results.md` / saved combined report:

| algorithm | AC@1 | AC@3 | AC@5 | MRR |
| --- | ---: | ---: | ---: | ---: |
| `crest` | 0.800281 | 0.944444 | 0.971871 | 0.875326 |
| `crest_metric_trace` | 0.703235 | 0.932489 | 0.969761 | 0.818233 |
| `crest_trace` | 0.560478 | 0.836850 | 0.904360 | 0.709243 |
| `crest_metric_log` | 0.440928 | 0.702532 | 0.811533 | 0.601020 |

So the key reversal is:

```text
RCABench:   crest full > metric_trace > trace > metric_log
aiops2025: metric_log > metric > metric_trace > crest full > trace
```

This is the strongest evidence that the remaining issue is not generic "CREST is bad", but
aiops2025 trace is not serving the same role as RCABench trace.

## Modality Coverage

Service-level GT coverage in abnormal data:

| dataset | metric GT covered | log GT covered | trace GT covered |
| --- | ---: | ---: | ---: |
| aiops2025 | 230 / 230 = 1.000 | 215 / 230 = 0.935 | 141 / 230 = 0.613 |
| RCABench | 1422 / 1422 = 1.000 | 1407 / 1422 = 0.989 | 1404 / 1422 = 0.987 |

Median rows and service counts:

| dataset | modality | median rows | median services |
| --- | --- | ---: | ---: |
| aiops2025 | metric | 19,036.5 | 15 |
| aiops2025 | log | 61,042.5 | 10 |
| aiops2025 | trace | 60,457.0 | 8 |
| RCABench | metric | 71,853.5 | 49 |
| RCABench | log | 29,622.5 | 30 |
| RCABench | trace | 58,477.0 | 29 |

Interpretation:

- aiops2025 metric/log have enough service coverage for the converted 230 cases.
- aiops2025 trace has many rows, but covers a much smaller service space.
- RCABench trace covers nearly every GT service and has a broader service graph.

## Trace Error And Status Signal

After the converter fix, aiops2025 trace status is no longer all `Ok`. A sampled `network corrupt`
case has:

```text
Error: 388
Ok:    49839
```

But the fixed status signal still often does not land on the root service:

| dataset | cases with any trace error | cases with GT trace error | cases where top error service is GT |
| --- | ---: | ---: | ---: |
| aiops2025 | 145 / 230 | 59 / 230 | 38 / 230 |
| RCABench | 1419 / 1422 | 978 / 1422 | 729 / 1422 |

By fault type in aiops2025:

| fault type | cases | trace GT covered | any trace error | GT trace error |
| --- | ---: | ---: | ---: | ---: |
| network corrupt | 25 | 25 | 25 | 23 |
| network delay | 23 | 23 | 2 | 1 |
| dns error | 20 | 19 | 12 | 12 |
| network loss | 20 | 20 | 20 | 17 |
| code error | 19 | 15 | 19 | 6 |
| cpu stress | 18 | 10 | 0 | 0 |
| memory stress | 16 | 10 | 6 | 0 |
| target port misconfig | 15 | 2 | 15 | 0 |
| pod failure | 14 | 9 | 13 | 0 |
| pod kill | 14 | 8 | 8 | 0 |
| jvm latency | 13 | 0 | 7 | 0 |
| jvm gc | 12 | 0 | 8 | 0 |
| jvm cpu | 11 | 0 | 1 | 0 |
| jvm exception | 10 | 0 | 9 | 0 |

This explains why trace helps network/DNS cases but hurts many resource/JVM/pod cases. The trace
contains symptoms, but the symptoms are not root-owned.

## Frontend-Dominated Trace Topology

In aiops2025, the largest trace-volume service is always `frontend`:

```text
aiops2025 top trace-volume service:
  frontend: 230 / 230 cases
  median frontend row share: 0.549
```

In RCABench, the trace graph is still entry-heavy, but much less concentrated:

```text
RCABench median top trace-volume share: 0.196
RCABench trace top-volume service is GT: 253 / 1422
```

This matters for CREST because full CREST does not simply sum metric/log/trace anomalies. It builds:

- local abnormality `A`;
- structural explanatory power `F`;
- denoised propagation support `S`;
- final score `A * F + S`.

When trace rows and topology are dominated by an entry service, `F` and `S` can make `frontend` look
like the best explanation of the incident even when metric/log rank the true root first.

## Trace Helps And Hurts Different Fault Types

Comparing `crest_metric_log` to full `crest` on aiops2025:

| fault type | cases | full CREST Top1 | metric+log Top1 | net |
| --- | ---: | ---: | ---: | ---: |
| dns error | 20 | 12 | 3 | +9 |
| network corrupt | 25 | 21 | 13 | +8 |
| network delay | 23 | 13 | 6 | +7 |
| network loss | 20 | 16 | 14 | +2 |
| code error | 19 | 6 | 11 | -5 |
| pod failure | 14 | 1 | 7 | -6 |
| memory stress | 16 | 5 | 12 | -7 |
| pod kill | 14 | 0 | 7 | -7 |
| jvm cpu | 11 | 0 | 8 | -8 |
| cpu stress | 18 | 3 | 15 | -12 |

Top1 regressions from `crest_metric_log` to full `crest`:

```text
total regressions: 65
predicted frontend: 55
predicted checkoutservice: 8
predicted cartservice: 1
predicted redis-cart: 1
```

Top1 improvements are almost entirely network/DNS:

```text
network corrupt: 9
network delay:   9
dns error:       9
network loss:    3
```

So the trace channel is not useless. It is useful for communication/path faults, but harmful for
resource/JVM/pod faults where trace mostly observes propagation.

## Concrete CREST Failure Examples

`cpu stress`, GT `paymentservice`:

| service | A | F | S | score |
| --- | ---: | ---: | ---: | ---: |
| frontend | 1.000000 | 1.000000 | 1.000000 | 2.000000 |
| checkoutservice | 0.970759 | 0.984532 | 0.970719 | 1.926463 |
| paymentservice | 0.795758 | 0.762391 | 0.773024 | 1.379703 |

`paymentservice` is ranked 7 by full CREST, while `crest_metric_log` ranks it 1.

`code error`, GT `cartservice`:

| service | A | F | S | score |
| --- | ---: | ---: | ---: | ---: |
| frontend | 0.976992 | 1.000000 | 1.000000 | 1.976992 |
| cartservice | 1.000000 | 0.974988 | 0.957239 | 1.932227 |

The GT has the highest local abnormality, but `frontend` wins through structural support.

`jvm latency`, GT `adservice`:

| service | rank | A | F | S | score |
| --- | ---: | ---: | ---: | ---: | ---: |
| frontend | 1 | 1.000000 | 1.000000 | 1.000000 | 2.000000 |
| adservice | 9 | 0.656245 | 0.590213 | 0.600347 | 0.987671 |

Here the GT has metric/log evidence, but trace has no GT coverage for JVM fault classes, so the
structural trace channel pushes the ranking toward frontend-side symptoms.

## Is This Still A Conversion-Script Problem?

Only partially.

What the converter already fixed:

- It preserves raw trace status/error evidence.
- It preserves raw trace tags/logs/process/references and parent service.
- It preserves metric provenance metadata.
- It filters cases whose service-level GT is not rankable at all.

Evidence that the remaining problem is not primarily conversion:

- The default dataset now has 230 rankable service cases.
- Metric/log variants perform much better than full CREST on the same converted data.
- Trace status is present and non-trivial in 145 / 230 cases.
- Full CREST mostly regresses by promoting `frontend`, a real raw trace service, not a missing or
  fabricated service.
- The negative effect is fault-type dependent: trace improves network/DNS and hurts resource/JVM/pod.

Remaining conversion/interface limitations:

- AIOps2025 has pod/instance and metric-key semantics, but the RCABench service interface collapses
  them mostly into `service_name`; CREST does not currently use `attr.aiops.*` metadata.
- Some metric rows produce namespace/global candidates such as `hipstershop`, `null`, or
  `example-ant`; these are noise, but not the main full-CREST failure mode.
- The converter cannot create trace instrumentation for services missing from raw Jaeger traces.

So the accurate answer is:

```text
The earlier conversion bug was real and is now fixed.
The remaining CREST gap is mainly caused by aiops2025 data characteristics:
low trace GT coverage, frontend-dominated trace topology, and many resource/JVM/pod faults whose
root evidence is metric/log rather than trace/status/path.
```

## Implication For Future CREST Adaptation

For aiops2025-like datasets, full CREST needs modality confidence before using trace structure:

- downweight trace counterfactual support when trace service coverage is narrow and top-volume share
  is very high;
- treat trace as high-confidence only for network/protocol/path/status-aligned incidents;
- prevent `abnormal_trace_rows` and trace topology from overriding strong metric/log root evidence;
- use `attr.aiops.*` metric provenance for pod/instance-level root localization instead of only
  service-level aggregation;
- keep filtering unobservable labels, because those are evaluation-interface impossible cases.

The most defensible next experiment is not another conversion rewrite, but a CREST trace-confidence
gate or modality-confidence ablation on the rebuilt 230-case dataset.
