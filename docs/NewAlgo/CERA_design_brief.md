# CERA Design Brief

CERA stands for Causal Evidence Role Alignment. It is a proposed unsupervised RCA algorithm intended to fit the capability envelope discovered by EvidenceRank while looking and behaving like a genuinely new method.

## Motivation

Current EvidenceRank is valuable as a probe because its performance shows that high-quality RCA needs multimodal evidence, robust normalization, endpoint mutation signals, topology context, and root-victim separation. But a feature-priority weighted sum is difficult to position as a new ICSE/FSE-level method.

CERA reframes the same empirical lessons as causal evidence-role inference:

- a root service should exhibit local mutation evidence;
- a victim service often exhibits propagation evidence such as latency, traffic, and high observability volume;
- topology should not simply boost central services, but should suppress downstream victims when the trace graph contains many terminal sink nodes;
- numeric evidence strength should be synthesized from ordinal causal evidence tiers, not manually assigned as feature-specific weights.

## Core Variables

For each service `s`, infer a root-causal evidence energy:

```text
E_s(root)
```

For each feature `x_j`, define an ordinal causal evidence tier:

```text
tier_j in {disabled, background, baseline, support, local, high, root, critical}
```

Recommended evidence families:

| family | example raw features |
| --- | --- |
| metric_magnitude | metric z-score, metric value delta |
| availability_drop | metric count drop, trace count drop |
| trace_protocol_mutation | endpoint shift, status-code shift, trace error rate |
| trace_latency | duration delta, self-duration shift |
| trace_traffic | count delta, count rise, abnormal trace rows |
| log_locality | log error rate, template delta, count delta |
| observability_volume | abnormal metric rows, abnormal trace rows |
| topology_context | parent-child edge role consistency |

## Inference Sketch

1. Load raw frames and collect services exactly as EvidenceRank does.
2. Build a nonnegative service-feature matrix from raw metrics, traces, logs, and trace edges.
3. Preserve raw log-normalized incident feature scale because magnitude and volume are operational evidence.
4. Synthesize the numeric energy ladder from ordinal tier ordering and tier count, not from per-feature constants.
5. Apply endpoint support using current incident agreement between endpoint, status, and traffic-rise rank views.
6. Apply parent-context smoothing with a strength derived from trace graph sink share:

```text
context_weight = sink_nodes / service_count
sink_nodes = trace children that are not trace parents
```

7. Rank services with an energy function:

```text
E_root(s) =
  sum_j ordinal_energy(tier_j) * raw_feature_j(s)
  aligned by endpoint support and sink-share topology context
```

8. Rank services by monotonic root energy.

## Topology Role Alignment

Earlier CERA variants tested counterfactual transfer on each trace edge:

```text
parent root explains child victim
child root explains parent victim
```

CERA3 found a more robust mechanism: derive parent-context strength from the current graph's sink share. When many nodes are terminal downstream children, leaf symptoms are more likely to be propagation victims, so parent context is stronger. When the graph has few sinks, CERA preserves the local evidence ranking. This keeps topology incident-derived rather than a centrality prior or a fixed blend constant.

## How To Fit EvidenceRank Without Copying It

EvidenceRank may be used as:

- a capability probe;
- an offline weak teacher for analyzing which unsupervised mechanisms are missing;
- a baseline to compare against;
- a source of reusable raw feature extraction.

EvidenceRank must not be used as:

- a runtime subroutine that directly supplies final rankings;
- a copied feature-weight table;
- a target that is optimized using labels, datapack names, or service/fault-specific patches;
- the only reason for a hyperparameter.

The desired fit is behavioral: CERA should learn the same kind of RCA competence EvidenceRank exposed, then improve or approach its metrics through a more novel unsupervised inference model.

## Version Plan

| version | target |
| --- | --- |
| `CERA0` | implementation scaffold, registry, smoke test |
| `CERA1` | robust scaled role-energy model, AC@1 >= 0.60 |
| `CERA2` | no-handcrafted-weight robust burden, AC@1 >= 0.75 |
| `CERA3` | ordinal causal evidence + sink-share topology, AC@1 >= 0.80 |
| `CERA4+` | robustness ablations and infrastructure-local evidence |

## Paper Framing

Possible paper contribution claim:

```text
We propose Causal Evidence Role Alignment, an unsupervised RCA framework that turns heterogeneous observability signals into ordinal causal evidence roles and uses incident-derived topology context rather than fixed feature weights. CERA synthesizes evidence energy from role ordering and derives parent-context strength from trace graph sink share to distinguish root causes from downstream propagation victims.
```

Key experiments:

- compare against EvidenceRank, EvidRank-ARC, MicroRCA, MicroHECL, MicroRank, BARO, and other existing outputs;
- ablate ordinal tiers, synthesized energy ladder, endpoint/status mutation support, sink-share topology, and raw-vs-robust scaling;
- evaluate CERA1/CERA2/CERA3 progression through AC@1 >= 0.60, 0.75, and 0.80;
- report false-case groups and regressions, not just aggregate metrics.
