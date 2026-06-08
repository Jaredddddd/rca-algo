# CREST Method Section Draft

This document rewrites the current implementation in
`algorithms/evidencerank/src/evidencerank/crest.py` as an ICSE-style method
section. It describes the algorithm as implemented: a label-free service ranking
procedure over normal and abnormal telemetry windows. It does not claim that
CREST learns a model, discovers a complete causal graph, or uses any benchmark
oracle at runtime.

## Method

### Problem Formulation

We consider root-cause localization for a microservice incident after an
incident window has already been identified. Let `V` be the set of services
observed in the telemetry. For each incident, the algorithm receives telemetry
from a normal reference window and an abnormal window. The task is to return an
ordered list of services:

```text
rank: V -> {1, ..., |V|}
```

where lower rank means that the service should be inspected earlier as a
possible root cause.

CREST treats root-cause localization as a ranking problem rather than as binary
classification. The method does not require training labels. Instead, it uses
three types of information that can be computed from the current incident:

- local evidence: how much each service changed between the normal and abnormal
  windows;
- evidence role: whether a feature is more consistent with a local mutation or
  with a propagated symptom;
- topology context: which services are adjacent in the trace-derived call graph.

Here, a local mutation means an observed change that can plausibly originate at
the service itself, such as a count drop, endpoint distribution change,
status-code distribution change, or error-rate increase. A propagated symptom
means an observed change that can be caused by another service, such as a
duration increase, request-volume shift, or broad log/template change. These
roles are fixed feature groups in the implementation; they are not learned from
labels.

### Input and Output

CREST consumes only raw telemetry frames under an incident input folder. The
default implementation uses all available modalities:

```text
normal_metrics.parquet
abnormal_metrics.parquet
normal_traces.parquet
abnormal_traces.parquet
normal_logs.parquet
abnormal_logs.parquet
```

The method extracts a service set from common service columns such as
`service_name`, `service`, `instance`, and Kubernetes deployment/container/pod
fields. Trace edges are extracted from `parent_service` when present. If
`parent_service` is absent, CREST derives it from `span_id`, `parent_span_id`,
and `service_name` when those columns are available.

The output is a service-level ranking. The implementation also exposes a
diagnostic table with the following columns:

```text
service, A, F, S, score
```

`A` is local abnormality, `F` is counterfactual structural factor, `S` is
denoised structural support, and `score` is the value used for final ranking.

The runtime path does not read labels, injection metadata, historical outputs,
evaluation reports, processed conclusions, datapack identifiers, service-name
rules, or fault-name rules.

### Assumptions

CREST relies on the following assumptions:

1. The incident window and a normal reference window are available.
2. Telemetry records can be mapped to services with reasonable coverage.
3. At least one enabled modality exposes evidence related to the root cause or
   its propagation.
4. Trace-derived parent-child edges approximate relevant service interactions
   during the incident. They need not form a complete causal graph.
5. Normal and abnormal windows are comparable enough that distribution shifts
   are meaningful.
6. The root cause may be quieter than downstream symptoms, so raw abnormality
   alone is insufficient.

If these assumptions are violated, CREST can still return a ranking, but the
ranking may degrade to local abnormality or become ambiguous.

### Algorithm Overview

CREST has four main stages.

First, it builds a service-feature matrix. For each service, the implementation
extracts metric, trace, log, volume, and topology features. Examples include
metric z-scores, metric count drops, trace duration shifts, trace count changes,
endpoint shifts, status-code shifts, trace error rates, self-duration shifts,
log count changes, log error rates, log template changes, abnormal row counts,
and trace in/out degrees.

Second, it normalizes evidence within the incident. Each raw feature is first
mapped through `log1p` by the shared feature builder. CREST then rescales each
feature column by its positive 95th percentile within the incident and clips the
result to a fixed upper bound. This makes features comparable across services
inside the same incident and reduces the effect of large row-count differences.

Third, CREST groups features by evidence role. The implementation uses six
families:

```text
metric_shift
trace_mutation
trace_propagation
log_shift
observability_volume
topology_context
```

The `trace_mutation` family contains endpoint, error-rate, and status-code
shift features. The `trace_propagation` family contains duration, count, volume,
and self-duration shift features. The `observability_volume` and
`topology_context` families provide context but are not treated as root-like
mutation by themselves.

Fourth, CREST computes a final score from local abnormality, structural
explanation, and denoised support. It then sorts services by `score`, with
`A`, `F`, and service name used as deterministic tie breakers.

### Core Scoring Function

Let `X[v, j]` be the incident-normalized value of feature `j` for service `v`.
After normalization and endpoint support adjustment, the resulting matrix is
called `R`. The endpoint support adjustment only affects `trace_endpoint_shift`:
when endpoint shift is present, it is multiplied by a factor derived from its
incident-local rank and supporting ranks from status-code shift and trace count
rise. If the required trace features are absent, this adjustment is skipped.

For a feature family `g`, define the family burden:

```text
B_g(v) = sum_{j in g} R[v, j]
```

The local energy is the sum over enabled family burdens:

```text
E_local(v) = sum_g B_g(v)
```

CREST maps non-negative incident-local vectors into `[0, 1]` with a saturating
scale:

```text
sat(z_v) = (1 - exp(-z_v / median_positive(z))) / max_u(1 - exp(-z_u / median_positive(z)))
```

where `median_positive(z)` is the median of the positive entries in vector `z`.
If the vector has no positive entries, the result is the all-zero vector.

Local abnormality is:

```text
A(v) = sat(E_local(v))
```

`A` measures how strongly a service changed in the current incident. It is not
used alone as the default RCA score.

CREST next computes structural energy. It starts from `E_local` and blends each
child service with the mean score of its trace parents:

```text
E_parent(v) =
    (1 - w) * E_local(v) + w * mean_{u in parents(v)} E_local(u)
```

for services with at least one parent. Services without parents keep
`E_local(v)`. The incident-specific context weight is:

```text
w = 1 / (1 + |E_trace| / |V|)
```

where `E_trace` is the set of valid trace edges between observed services.

CREST then applies a pairwise explain-away operation over trace-neighbor pairs.
For each ordered pair `(u, v)` derived from an undirected view of a trace edge,
`u` can explain away part of `v` only when three conditions hold:

```text
E(v) > E(u)
mutation(u) > mutation(v)
propagation(v) > propagation(u)
```

The mutation and propagation vectors are robust positive-95th-percentile scaled
sums of their respective feature sets. The mutation set is:

```text
metric_count_drop_shift
trace_count_drop_shift
trace_endpoint_shift
trace_error_rate
trace_status_code_shift
```

The propagation set is:

```text
trace_duration_z
trace_duration_delta
trace_self_duration_relative_shift
trace_count_delta
trace_count_rise_shift
abnormal_trace_rows
log_count_delta
log_template_delta
```

For a qualifying pair, CREST transfers only the explainable portion of the
energy gap:

```text
mutation_share(u, v) =
    (mutation(u) - mutation(v)) / (mutation(u) + mutation(v) + eps)

propagation_share(v, u) =
    (propagation(v) - propagation(u)) / (propagation(v) + propagation(u) + eps)

transfer(u <- v) =
    (E(v) - E(u)) * mutation_share(u, v) * propagation_share(v, u)
```

Within one iteration, each victim service `v` keeps only its largest incoming
transfer. CREST then adds the transfer to the candidate explainer and subtracts
it from the victim:

```text
E'(u) = E(u) + transfer(u <- v)
E'(v) = E(v) - transfer(u <- v)
```

The implementation repeats this operation for at most the number of non-context
role families, stopping early when the structural energy no longer changes.
The structural factor is:

```text
F(v) = sat(E_struct(v))
```

Finally, CREST computes a denoised support channel. This channel repeats the
same parent-context and explain-away steps, but its seed excludes
`trace_duration_z`, because a standalone duration z-score is often a propagated
latency symptom. Let the resulting energy be `E_denoised`. Then:

```text
S(v) = sat(E_denoised(v))
```

The default CREST score is:

```text
score(v) = A(v) * F(v) + S(v)
```

If all final scores are zero but some local abnormality is positive, CREST falls
back to ranking by `A`.

The implementation includes ablation variants. `crest_local` sets the
structural factor to one and uses only local abnormality. `crest_nocf` replaces
the explain-away operation with a PageRank-style graph prior. Modality ablations
enable only metric, trace, log, or pairwise modality subsets.

### Pseudocode

```text
Algorithm 1: CREST service ranking

Input:
  folder containing normal and abnormal metric, trace, and log frames
  enabled_modalities, default = {metric, trace, log}
Output:
  ranked list of services

1: frames <- load raw telemetry frames from folder
2: V <- collect services from metric, trace, and log frames
3: if V is empty:
4:     return empty ranking
5:
6: feature_names <- enabled features for enabled_modalities
7: X, trace_edges <- build service-feature matrix from frames
8: X <- log1p-normalized non-negative feature matrix
9: R <- positive-p95-scale each feature column of X and clip large values
10: R <- apply endpoint support adjustment when trace support features exist
11:
12: E_local <- sum family burdens in R
13: A <- saturating_incident_scale(E_local)
14:
15: w <- 1 / (1 + number_of_valid_trace_edges / number_of_services)
16: E_struct <- blend each child with mean parent energy using weight w
17: E_struct <- EXPLAIN_AWAY(V, E_struct, R, feature_names, trace_edges)
18: F <- saturating_incident_scale(E_struct)
19:
20: E_denoised <- sum all enabled feature values except trace_duration_z
21: E_denoised <- blend each child with mean parent energy using weight w
22: E_denoised <- EXPLAIN_AWAY(V, E_denoised, R, feature_names, trace_edges)
23: S <- saturating_incident_scale(E_denoised)
24:
25: for each service v in V:
26:     score[v] <- A[v] * F[v] + S[v]
27: if all score values are zero and any A value is positive:
28:     score <- A
29: return services sorted by score descending, then A descending,
        then F descending, then service name ascending


Procedure EXPLAIN_AWAY(V, E, R, feature_names, trace_edges)

1: mutation <- positive-p95-scaled sum of mutation features in R
2: propagation <- positive-p95-scaled sum of propagation features in R
3: repeat up to the number of non-context role families:
4:     best_transfer_by_victim <- empty map
5:     for each trace edge {u, v}, considered in both directions:
6:         if E[v] <= E[u]:
7:             continue
8:         mutation_excess <- mutation[u] - mutation[v]
9:         propagation_excess <- propagation[v] - propagation[u]
10:        if mutation_excess <= 0 or propagation_excess <= 0:
11:            continue
12:        mutation_share <- mutation_excess / (mutation[u] + mutation[v] + eps)
13:        propagation_share <- propagation_excess /
                              (propagation[v] + propagation[u] + eps)
14:        transfer <- (E[v] - E[u]) * mutation_share * propagation_share
15:        keep transfer if it is the largest candidate for victim v
16:    E_old <- E
17:    for each kept transfer u <- v:
18:        E[u] <- E[u] + transfer
19:        E[v] <- E[v] - transfer
20:    E <- max(E, 0)
21:    if norm(E - E_old) is negligible:
22:        break
23: return E
```

### Toy Example

Consider three services: `frontend`, `checkout`, and `payment`. The trace graph
contains two edges:

```text
frontend -> checkout -> payment
```

Assume the incident-normalized evidence after feature extraction is as follows.
The numbers are illustrative and are not tied to any benchmark case.

| service | local energy | mutation | propagation | denoised seed |
| --- | ---: | ---: | ---: | ---: |
| frontend | 0.30 | 0.10 | 0.40 | 0.25 |
| checkout | 0.85 | 0.90 | 0.20 | 0.80 |
| payment | 1.00 | 0.10 | 0.80 | 0.20 |

A local-abnormality-only method would rank `payment` first because its local
energy is highest. CREST compares `checkout` and `payment`, which are trace
neighbors. `checkout` has stronger mutation evidence, while `payment` has
stronger propagation evidence. Therefore, `checkout` can explain away part of
`payment`'s energy gap.

For this pair:

```text
mutation_share(checkout, payment)
  = (0.90 - 0.10) / (0.90 + 0.10) = 0.80

propagation_share(payment, checkout)
  = (0.80 - 0.20) / (0.80 + 0.20) = 0.60

transfer(checkout <- payment)
  = (1.00 - 0.85) * 0.80 * 0.60 = 0.072
```

After this local update, the structural energies become:

```text
checkout: 0.85 + 0.072 = 0.922
payment:  1.00 - 0.072 = 0.928
```

The update does not simply move all suspicion from the victim to the candidate.
It moves only the part supported by the mutation-propagation contrast. The
final ranking also uses `A` and `S`. In this example, `checkout` has a much
larger denoised seed because its evidence is not dominated by a standalone
duration spike. After saturation, `checkout` can outrank `payment` even though
`payment` remains locally abnormal. This behavior is intended: the downstream
victim still appears suspicious, but the service with stronger local mutation
and structural support is inspected first.

### Complexity Analysis

Let:

- `n = |V|`, the number of observed services;
- `d`, the number of enabled service-level features;
- `m`, the number of valid trace edges between observed services;
- `r`, the number of non-context role families used as the iteration cap;
- `N`, the total number of metric, trace, and log records read from the input
  folder.

Feature extraction is dominated by grouping and distribution-shift computation
over the raw frames. In a typical dataframe implementation, this cost is
approximately `O(N log N)` or `O(N)` depending on grouping internals and key
cardinality. The scoring stage after feature extraction has the following cost:

- robust feature scaling: `O(n d)`;
- family burden computation: `O(n d)`;
- parent-context blending: `O(n + m)`;
- one explain-away iteration: `O(n d + m)`;
- full explain-away stage: `O(r (n d + m))`;
- final sorting: `O(n log n)`.

Thus the default scoring complexity after feature extraction is:

```text
O(n d + r (n d + m) + n log n)
```

In the current implementation, `d` and `r` are small fixed constants, so runtime
is usually dominated by reading parquet files and constructing grouped telemetry
features. The memory used by the scoring stage is `O(n d + m)`, excluding the
raw input frames held by the dataframe library.

The `crest_nocf` ablation uses a PageRank-style graph prior. Its graph
propagation loop runs for up to `n` steps and has scoring cost
`O(n (n + m))` after feature extraction.

### Failure Modes

CREST is designed as a lightweight, label-free ranking method. It has several
known limitations.

Incorrect incident windows. If the abnormal window does not contain the failure
or the normal window is not representative, the feature shifts can be
misleading.

Missing service attribution. If records cannot be mapped to services, the
affected services may be absent from the ranking or have near-zero evidence.

Missing trace topology. If trace parent-child information is unavailable,
CREST loses the structural explain-away signal and behaves closer to local
abnormality ranking.

No observable root evidence. If the root service has no local mutation, no log
shift, no metric shift, and no structural support in the available data, CREST
has little basis to rank it above visible victims.

Ambiguous root-victim roles. A downstream service can have real local mutation
evidence, and a root service can also have propagation-like evidence. In such
cases, the fixed mutation and propagation feature groups may not cleanly
separate candidates.

Multiple independent roots. CREST returns a single ordered list and applies
pairwise local transfers. Independent simultaneous faults can produce multiple
high-scoring regions that are difficult to order.

Unmodeled infrastructure components. If the true faulty component is not
represented as a service in the telemetry, CREST can only rank the services
whose symptoms are observable.

Global traffic shifts. When many services change similarly, incident-local
scaling can compress differences between candidates. This can reduce the
usefulness of both local abnormality and explain-away.

No causal discovery guarantee. The trace graph is used as observed structural
context. CREST does not infer a complete causal graph and does not prove that a
ranked service caused the incident. The output is a triage ranking, not a formal
causal certificate.
