# CERA Design Brief

CERA stands for Counterfactual Evidence Role Alignment. It is a proposed unsupervised RCA algorithm intended to fit the capability envelope discovered by EvidenceRank while looking and behaving like a genuinely new method.

## Motivation

Current EvidenceRank is valuable as a probe because its performance shows that high-quality RCA needs multimodal evidence, robust normalization, endpoint mutation signals, topology context, and root-victim separation. But a feature-priority weighted sum is difficult to position as a new ICSE/FSE-level method.

CERA reframes the same empirical lessons as latent causal-role inference:

- a root service should exhibit local mutation evidence;
- a victim service often exhibits propagation evidence such as latency, traffic, and high observability volume;
- topology should not simply boost central services, but should explain away propagation-heavy neighbors;
- modality weights should be learned from the current incident's evidence geometry, not fixed by labels.

## Core Variables

For each service `s`, infer a latent role distribution:

```text
q_s(root), q_s(victim), q_s(background)
```

For each evidence family `f`, infer a case-local reliability:

```text
r_f in [0, 1]
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
3. Apply robust per-case scaling: positive p95 scaling, clipping, and finite-value cleanup.
4. Aggregate features into role views:
   - root mutation view: availability drop + protocol mutation + log locality + local metric magnitude;
   - victim propagation view: latency + traffic + observability volume;
   - background view: low evidence or diffuse evidence.
5. Initialize `q(root)` from mutation and local evidence after subtracting propagation dominance.
6. Estimate family reliability from support, evidence concentration, peak contrast, top gap, and rank agreement with the current root posterior.
7. Update role posteriors with an energy function:

```text
E_root(s) =
  reliable_mutation(s)
  + reliable_local_log_metric(s)
  - propagation_dominance(s)
  + topology_explain_away_gain(s)
  + multimodal_redundancy(s)
```

8. Run a small fixed number of EM-style updates, for example 3 to 8 iterations.
9. Rank services by `q_s(root)` or by a monotonic root energy.

## Counterfactual Explain-Away

For each trace edge `(parent, child)`, CERA should test both possible explanations:

```text
parent root explains child victim
child root explains parent victim
```

The better explanation is the one where the root candidate has stronger mutation/local evidence and the victim candidate has stronger propagation evidence. Transfer or suppress score accordingly. This is the publishable step: topology is used as counterfactual role alignment, not as centrality.

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
| `CERA2` | family reliability and EM-style updates, AC@1 >= 0.70 |
| `CERA3` | topology counterfactual explain-away, AC@1 >= 0.75 |
| `CERA4+` | teacher-probe analysis and ablations toward 0.80 |

## Paper Framing

Possible paper contribution claim:

```text
We propose Counterfactual Evidence Role Alignment, an unsupervised RCA framework that turns heterogeneous observability signals into latent causal roles and uses topology as an explain-away constraint rather than a centrality prior. CERA learns incident-specific evidence reliability from internal agreement and uses counterfactual neighbor role assignments to distinguish root causes from propagation victims.
```

Key experiments:

- compare against EvidenceRank, EvidRank-ARC, MicroRCA, MicroHECL, MicroRank, BARO, and other existing outputs;
- ablate latent roles, reliability learning, explain-away, endpoint/status mutation, and log evidence;
- evaluate whether CERA reaches AC@1 >= 0.60 first, then iterates toward 0.80;
- report false-case groups and regressions, not just aggregate metrics.

