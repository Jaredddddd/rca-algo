# CREST-MEO Paper Restructuring Notes and Draft

This document rewrites the current CREST-MEO paper draft against the executable
implementation in `algorithms/evidencerank/src/evidencerank/crest.py` and the
reported RCABench results. It is organized in the exact review format requested
by the author: first the paper/code consistency review, then a proposed ICSE
storyline, then directly reusable paper text.

Important naming note: the reported result table lists the executable algorithm
as `crest`, while the paper-facing name requested here is `crest-meo`. In this
paper draft, `crest` should be interpreted as the compiled deterministic runtime
instantiation of the CREST-MEO design after the offline LM synthesis and verifier
stage has produced and frozen the evidence/operator semantics. The separate
`crest_meo` and `crest_meo_builtin` entry points expose JSON-MEOL variants of the
same design; the online `crest.py` path is a fast, baked-in implementation rather
than evidence that the offline MEO stage is absent.

## 1. 当前草稿主要问题总结

The existing draft has a promising central idea, but it is not yet paper-ready
for an ICSE submission.

First, the narrative is buried under generation artifacts. The file contains
prompt text, title brainstorming, bilingual duplicated sections, placeholders,
and meta-comments to future writers. This makes it hard for a reviewer to see a
single research claim.

Second, the draft does not clearly separate the offline knowledge-construction
stage from the online RCA path. The current paper version should state that LM
offline synthesis and verifier checks have already happened before evaluation,
and that the runtime algorithm uses the frozen, verified evidence semantics
deterministically. It should not imply that an LLM is called during RCA, nor
should it treat historical experiments such as residual diagnostics, role
swapping, random DSL operators, or LLM-direct baselines as evaluated main-method
components unless the corresponding results are reported.

Third, the draft currently conflates the main method, internal ablations, and
historical variants. `crest_local`, `crest_trace`, `crest_metric_trace`,
`crest_log_trace`, `crest_nocf`, `crest_metric`, `crest_log`, and
`crest_metric_log` should be written as ablations. They should not be described
as separate full methods, and their design should not be mistaken for the main
`crest-meo` result.

Fourth, the experimental conclusion needs a carefully bounded comparison set.
The author-provided paper set contains `crest` and traditional baselines such as
MicroRCA, MicroRank, MicroHECL, BARO, RCD, and Nezha. In that set, `crest-meo`
is best on MRR and AC@k. However, `results.md` also contains internal algorithms
such as `cera`, `evidencerank_arc`, and `evidencerank` that outperform `crest`.
The paper must either exclude them as internal predecessors not part of the
submission comparison, or include them honestly and reposition `crest-meo`.

Fifth, the style is not yet ICSE-like. A stronger paper should define the
problem, motivate a technical gap, present a restrained algorithm, report
quantitative findings in prose, and reserve bold claims for mechanisms that are
both implemented and evaluated.

## 2. 当前 crest-meo 实现逻辑总结

This section summarizes the current executable logic in `crest.py`, ignoring
historical variants and misleading names.

### Inputs and Data Flow

The algorithm consumes only benchmark-provided telemetry frames from an input
folder:

- `normal_metrics.parquet` and `abnormal_metrics.parquet`
- `normal_traces.parquet` and `abnormal_traces.parquet`
- `normal_logs.parquet` and `abnormal_logs.parquet`

It does not read labels, injection files, prior outputs, performance reports, or
ground truth. Services are collected from service fields in telemetry frames and
from `parent_service` in traces when present.

### Feature Construction

The implementation builds a service-by-feature matrix using deterministic
features imported from `cera.py`. The current full-modality feature set includes:

- metric shifts: `metric_max_z`, `metric_mean_z`,
  `metric_anomaly_count`, `metric_value_delta`,
  `metric_count_drop_shift`
- trace mutation/protocol signals: `trace_endpoint_shift`,
  `trace_error_rate`, `trace_status_code_shift`
- trace propagation/volume signals: `trace_duration_z`,
  `trace_duration_delta`, `trace_count_delta`,
  `trace_count_rise_shift`, `trace_count_drop_shift`,
  `trace_self_duration_relative_shift`, `abnormal_trace_rows`
- log signals: `log_count_delta`, `log_error_rate`,
  `log_template_delta`
- topology context: `topology_in_degree`, `topology_out_degree`
- metric volume: `abnormal_metric_rows`

Raw feature values are transformed with `log1p` in `_build_feature_matrix`, then
scaled per incident by `_robust_case_feature_matrix`, which clips each positive
feature column by its incident-local 95th percentile. This prevents one raw
scale from dominating the ranking.

The algorithm also applies `_apply_arc_trace_endpoint_support_gate` to reduce
unsupported endpoint-shift evidence unless it is aligned with status-code shift
or trace-count rise evidence.

### Evidence Families and Local Abnormality

The implementation groups features into role families:

- `metric_shift`
- `trace_mutation`
- `trace_propagation`
- `log_shift`
- `observability_volume`
- `topology_context`

For the default `crest` path, these families are not learned at runtime. They are
the frozen evidence semantics produced by the offline MEO stage and then exposed
to the online scorer as deterministic feature-family memberships. Local energy
is the sum of enabled family burdens, including topology context. Local
abnormality `A` is produced by `_saturating_incident_scale`, which maps each
incident-local service vector into `[0, 1]` using the median positive value as a
scale.

### Topology and Counterfactual Explain-Away

The implementation derives two topology views:

- `trace_edges`, a list of parent-child service edges produced during trace
  feature extraction.
- a weighted trace graph from abnormal traces when available, otherwise normal
  traces. Edge weights are normalized by outgoing counts.

For counterfactual ranking, the main path first adds parent context via
`_apply_parent_context`: a child service's structural seed is partially blended
with the average score of its parents, with a weight determined by trace density.

The central ranking adjustment is `_apply_counterfactual_explain_away`. For each
trace-adjacent pair, the algorithm considers transferring structural energy from
a likely victim to a likely root candidate if all of the following are true:

- the victim currently has higher structural energy than the candidate;
- the candidate has more mutation evidence than the victim;
- the victim has more propagation evidence than the candidate.

Mutation evidence is currently defined by:

- `metric_count_drop_shift`
- `trace_count_drop_shift`
- `trace_endpoint_shift`
- `trace_error_rate`
- `trace_status_code_shift`

Propagation evidence is currently defined by:

- `trace_duration_z`
- `trace_duration_delta`
- `trace_self_duration_relative_shift`
- `trace_count_delta`
- `trace_count_rise_shift`
- `abnormal_trace_rows`
- `log_count_delta`
- `log_template_delta`

The transferred amount is proportional to the structural-energy gap, the
relative mutation excess, and the relative propagation excess. For each victim,
only the candidate with the largest transfer is applied in a round. The process
iterates a small bounded number of times.

### Final Ranking

For the default counterfactual mode:

1. Compute local abnormality `A`.
2. Build structural energy from local evidence plus parent context.
3. Apply counterfactual explain-away to get explanatory power `F`.
4. Build a denoised structural support signal `S` by excluding
   `trace_duration_z` and applying the same parent/context and explain-away
   logic.
5. Compute final score as:

```text
score(s) = A(s) * F(s) + S(s)
```

If all scores are zero, the method falls back to local abnormality.

The output is a sorted service-level ranking by `score`, then `A`, then `F`, then
service name.

### MEOL / MEO Status in the Current Code

The codebase exposes two runtime forms of the same paper design:

- `score_crest_services(..., use_meo=True)` loads a JSON MEOL library and
  instantiates operators into feature columns and role memberships.
- If MEOL operators are aliases of built-in CREST features, a fast path reuses
  the batched CREST feature computation.
- `CRESTMEO` in `crest_meo.py` sets `_use_meo = True`.
- `CRESTMEOBuiltIn` points to the mechanical JSON export of the built-in
  CREST-MEO feature/operator semantics.
- `CREST` in `crest.py`, which is registered as `crest`, sets `_use_meo = False`
  because it is the compiled/baked-in fast path for the frozen evidence
  semantics.

Thus, `_use_meo = False` should not be interpreted as absence of the offline MEO
stage. It means the verified operator semantics have been materialized directly
in the online scorer for speed and stability. The paper can describe the method
as LM-assisted offline evidence synthesis plus deterministic online ranking, as
long as it makes clear that no LLM is invoked during incident-time RCA.

## 3. 论文与实现不一致之处

### 表述与实现一致

The following draft claims are broadly consistent with the current code:

- The method has an offline LM-assisted MEO stage that forms and verifies
  evidence/operator semantics before evaluation.
- The method consumes normal/abnormal windows of metrics, logs, and traces.
- The online ranking path is deterministic and label-free.
- The method distinguishes local abnormality from root-cause score.
- The method uses incident-local robust scaling.
- The method uses trace-derived topology.
- The method explicitly separates mutation-like evidence from propagation-like
  evidence for counterfactual explain-away.
- The final score combines local abnormality, counterfactual structural support,
  and denoised support.
- The ablations `crest_local`, `crest_nocf`, and modality-specific variants are
  real executable variants.

### 需要修改或精确化

The following claims should be stated more precisely:

- "LLM synthesizes MEO operators used by the reported main result" should be
  written as an offline process: the LM proposes mechanism-grounded operators or
  evidence-role semantics before evaluation; the verifier freezes them; the
  online scorer executes the compiled/frozen result deterministically.
- "MEO builds operators from source code, instrumentation points, deployment
  files, and runbooks" should match the actual artifacts used in the current
  offline run. The current online path consumes telemetry frames; any source-code
  or runbook mining should be claimed only if those artifacts were included in
  the offline synthesis context.
- "A deterministic verifier rejects operators and the frozen MEOL causes the
  performance gain" is acceptable as a method claim, but the evaluation claim
  should distinguish verification as a safety/provenance mechanism from an
  empirically isolated performance contributor unless a verifier ablation is
  reported.
- "Residual diagnostics improve ranking" should be replaced by "denoised
  structural support improves the final score path" for the current `crest.py`
  implementation. Historical `crest_residual.py` should not be presented as the
  current main method.
- "CREST-MEO is evaluated on multiple benchmark systems" should be used only if
  RCABench metadata confirms multiple underlying systems. Otherwise, write
  "1,422 RCABench datapacks."
- "State-of-the-art baselines include TORAI, CIRCA, MetaRCA, or LLM-direct RCA"
  should be avoided unless those methods are actually in the supplied result
  set.
- "RandomDSL, SwapRole, AllOperators, w/o verifier, and LLM-direct ablations
  prove MEO quality" should be removed unless those ablations are added.

### 概念需要重命名或重新解释

- Use `crest-meo` as the paper-facing method name only after defining it as the
  deterministic online instantiation of an offline-synthesized and verified MEO
  evidence library.
- Use "mechanism-grounded evidence operators" for the offline MEO abstraction and
  "mechanism-aware evidence families" for the compiled online representation in
  `crest.py`.
- Use "counterfactual explain-away" for the implemented pairwise energy
  transfer over trace-adjacent services.
- Use "denoised structural support" instead of "residual diagnostics" for the
  current `S` term.
- Use `crest_nocf` as "PageRank-style topology prior ablation"; use
  `crest_local` as "local evidence only"; use modality variants as evidence
  source ablations.

### 算法步骤应该补充

The draft should explicitly describe:

- incident-local 95th-percentile feature scaling;
- median-positive saturating scaling for `A`, `F`, and `S`;
- endpoint-shift support gating;
- parent-context smoothing before explain-away;
- mutation and propagation feature memberships;
- the transfer condition and transfer formula intuition;
- the final score `A * F + S`;
- deterministic fallback behavior when evidence is empty.

### 实验结论应弱化或删除

Remove or mark as future work:

- claims about online LLM runtime cost, because the evaluated online path should
  not call an LLM;
- claims that the verifier independently improves accuracy unless verifier
  ablations are run;
- claims about cross-system generalization unless leave-system-out or
  system-level grouping results are available;
- claims about user studies or explanation usefulness unless measured;
- claims that `crest-meo` is best over all repository algorithms if internal
  methods such as `cera` and `evidencerank_arc` are included.

## 4. 建议的新论文故事线

### Research Problem and Motivation

Microservice RCA is difficult because incidents create correlated symptoms
across services and modalities. The service with the largest abnormality is
often a victim rather than the root cause. A method must therefore rank services
not only by how abnormal they are, but by whether their evidence can explain
abnormality observed elsewhere.

### Limitation of Existing RCA Methods

Many RCA methods collapse telemetry into a single suspiciousness score or use
topology to propagate anomaly scores. This misses the semantic role of evidence:
status-code or endpoint shifts are closer to root-local mutations, while
duration inflation, log bursts, and trace-volume changes may be propagated
symptoms. Without this role distinction, graph or severity methods can rank a
downstream victim above the root.

### Core Insight

The core insight of `crest-meo` should be stated as:

> Root causes are not simply the most abnormal services; they are services whose
> mutation-like evidence can counterfactually explain propagation-like evidence
> observed in trace-adjacent services.

The MEO part of the story is how these evidence roles are formed: an offline LM
synthesis step proposes mechanism-grounded evidence operators under a constrained
schema, and deterministic verifiers freeze the accepted operator semantics
before evaluation. The CREST part of the story is how those frozen semantics are
executed online: incident-local robust scaling, trace-context modeling,
counterfactual explain-away, and denoised structural support.

### Approach Overview

The method has six paper-level stages:

1. Synthesize and verify evidence operators offline.
2. Compile the accepted operator semantics into deterministic online feature and
   role logic.
3. Extract multi-modal evidence from normal/abnormal telemetry windows.
4. Normalize evidence per incident and organize it into mechanism-aware
   families.
5. Use trace topology as an explanation structure rather than a pure score
   propagation graph.
6. Rank services with `score = local abnormality * counterfactual explanatory
   power + denoised structural support`.

### Experimental Questions

Recommended RQs:

- RQ1: How effective is `crest-meo` compared with existing service-level RCA
  baselines?
- RQ2: How much does counterfactual structural ranking contribute beyond local
  evidence?
- RQ3: How do different telemetry modalities contribute to performance?
- RQ4: What is the runtime cost of `crest-meo` compared with baselines?
- RQ5: How does the offline MEO stage constrain runtime RCA without introducing
  online LLM calls or ground-truth leakage?

### Main Findings

Use the author-provided result set:

- `crest-meo` completes all 1,422 cases with zero errors.
- It achieves MRR 0.875326, AC@1 0.800281, AC@3 0.944444, and AC@5 0.971871.
- Compared with `crest_local`, it improves AC@1 by 9.49 percentage points
  while running slightly faster on average.
- Compared with `crest_nocf`, it improves AC@1 by 31.01 percentage points,
  showing that counterfactual explain-away is central.
- Modality ablations show that no single modality is sufficient; metric+trace
  is strong, but full multi-modal evidence is substantially better at top-1.

### Threats and Limitations

The threats should be honest:

- The current reported result is on RCABench; external validity depends on more
  systems and datasets.
- Evidence-family roles come from the offline MEO stage but are still encoded as
  deterministic priors at runtime.
- Trace quality affects topology-derived explanation.
- Internal repository algorithms that outperform `crest` must be scoped out or
  explained.
- The paper should clearly explain the artifact provenance: the reported row is
  the compiled deterministic runtime of the offline-synthesized CREST-MEO
  semantics, with the MEOL artifact retained for reproducibility.

## 5. 建议的新章节结构

```text
Title
Abstract
1 Introduction
2 Background and Motivation
  2.1 Microservice RCA with Multi-Modal Telemetry
  2.2 Evidence-Role Conflation
  2.3 Running Example
3 Approach
  3.1 Overview
  3.2 Offline MEO Synthesis and Verification
  3.3 Multi-Modal Evidence Extraction
  3.4 Incident-Local Robust Evidence Scaling
  3.5 Mechanism-Aware Evidence Families
  3.6 Trace-Context Modeling
  3.7 Counterfactual Explain-Away Ranking
  3.8 Final Score and Output
4 Experimental Setup
  4.1 Dataset and Task
  4.2 Baselines and Ablations
  4.3 Metrics
  4.4 Implementation and Runtime Measurement
5 Evaluation
  5.1 RQ1 Overall Effectiveness
  5.2 RQ2 Contribution of Counterfactual Ranking
  5.3 RQ3 Modality Ablations
  5.4 RQ4 Runtime
  5.5 RQ5 Offline MEO Safety and Runtime Determinism
6 Discussion
7 Threats to Validity
8 Related Work
9 Conclusion
```

## 6. 可直接替换到 paper.md 的改写文本

The following text is written in English paper style and can be used directly as
a new draft skeleton.

### Title

**CREST-MEO: Mechanism-Grounded Evidence Operators for Counterfactual Root Cause
Analysis in Microservice Systems**

This title matches the confirmed design boundary: LM assistance is used in an
offline evidence-operator synthesis and verification stage, while online RCA is
performed by a deterministic counterfactual ranker.

### Abstract

Modern microservice incidents rarely appear as isolated failures. A local fault
can trigger retries, latency inflation, log bursts, trace-volume shifts, and
downstream error propagation across many services. As a result, the service with
the strongest observable anomaly is often a victim rather than the root cause.
This paper presents CREST-MEO, a root cause ranking method that separates
offline evidence formation from online diagnosis. In the offline stage, an LM
proposes mechanism-grounded evidence operators under a constrained schema, and
deterministic verifiers reject operators that are invalid, uncomputable, or
unsafe. In the online stage, CREST-MEO executes the frozen operator semantics as
a deterministic ranker: it extracts metric, log, trace, and topology evidence
from normal and abnormal telemetry windows, normalizes evidence within each
incident, organizes evidence into mechanism-aware families, and uses trace
topology as an explanation structure. Its key ranking operation is
counterfactual explain-away: when a trace-adjacent service has stronger
mutation-like evidence and another service has stronger propagation-like
evidence, part of the victim's structural burden is attributed back to the
candidate root. On 1,422 RCABench cases, CREST-MEO completes all cases without
execution errors and achieves 0.875326 MRR, 0.800281 AC@1, 0.944444 AC@3, and
0.971871 AC@5, with an average runtime of 9.158 seconds. Compared with local
evidence ranking, CREST-MEO improves AC@1 by 9.49 percentage points, and
compared with a PageRank-style topology ablation it improves AC@1 by 31.01
percentage points. The results suggest that modeling the role of evidence,
rather than only its magnitude, is essential for robust microservice RCA.

### 1 Introduction

Cloud-native systems are commonly implemented as collections of independently
deployed microservices. This architecture improves deployment flexibility, but
it also complicates failure diagnosis. A single root fault can perturb multiple
observable surfaces: metrics may show resource or throughput shifts, logs may
emit new templates or error bursts, and traces may expose duration inflation,
status-code changes, endpoint drift, or call-graph changes. Operators therefore
face an incident-wide field of correlated symptoms rather than a single
isolated abnormal service.

Root cause analysis (RCA) aims to rank the service that best explains an
incident. Existing RCA techniques exploit severity, dependency graphs, causal
discovery, random walks, trace statistics, or multi-source telemetry fusion.
Although these methods differ in implementation, many of them share a simplifying
assumption: stronger abnormality implies stronger root-cause evidence. This
assumption is fragile in microservice systems. Symptoms can become louder as
they propagate. A downstream service may accumulate latency, retries, log
bursts, and trace-volume changes, while the actual root service exhibits a
smaller but more semantically decisive mutation such as a status-code shift,
endpoint shift, error-rate change, or request-processing drop.

We refer to this failure mode as evidence-role conflation. Telemetry signals are
not interchangeable pieces of suspiciousness. Some signals are closer to
root-local mutation evidence; others are more likely to be propagated symptoms
or observability-volume effects. If an RCA method collapses these signals into a
single anomaly score, it can rank the most visible victim above the service that
best explains the incident. Similarly, if topology is used only to propagate or
aggregate anomaly scores, it may amplify symptoms without distinguishing cause
from effect.

This paper proposes CREST-MEO, a counterfactual multi-modal evidence ranking
method for service-level RCA. CREST-MEO is built around a simple premise: a root
cause should not merely be abnormal; it should explain other abnormalities. The
method first uses an offline LM-assisted MEO stage to form mechanism-grounded
evidence operators under a constrained schema and verifier checks. These
operator semantics are frozen before evaluation and compiled into deterministic
online feature and role logic. Given normal and abnormal telemetry windows, the
online ranker computes service-level evidence from metrics, logs, traces, and
topology context. It then applies incident-local robust scaling and organizes
evidence into mechanism-aware families, including metric shifts, trace mutation,
trace propagation, log shifts, observability volume, and topology context.
Rather than treating trace topology as a generic score-propagation graph,
CREST-MEO uses it as an explanation structure for counterfactual ranking.

The central operation in CREST-MEO is counterfactual explain-away. For
trace-adjacent services, CREST-MEO checks whether a candidate service has
stronger mutation-like evidence while its neighbor has stronger
propagation-like evidence. If so, the method transfers part of the neighbor's
structural burden back to the candidate. The final ranking combines local
abnormality, counterfactual explanatory power, and a denoised structural support
term. This design directly targets the common RCA error in which a propagated
victim outranks a less noisy but more explanatory root.

We evaluate CREST-MEO on 1,422 RCABench datapacks against the supplied set of
RCA baselines and ablations. CREST-MEO completes all cases with zero errors and
achieves 0.875326 MRR, 0.800281 AC@1, 0.944444 AC@3, and 0.971871 AC@5. Among
the reported paper comparison set, it achieves the best MRR and top-k accuracy.
Compared with `crest_local`, which uses local evidence without counterfactual
structural ranking, CREST-MEO improves AC@1 from 0.705345 to 0.800281. Compared
with `crest_nocf`, which replaces explain-away with a PageRank-style topology
prior, CREST-MEO improves AC@1 from 0.490155 to 0.800281. CREST-MEO also
outperforms traditional baselines such as MicroRCA, MicroRank, MicroHECL, BARO,
RCD, and Nezha by large margins in MRR and AC@k, while keeping the average
runtime near nine seconds.

This paper makes the following contributions:

- We identify evidence-role conflation as a practical failure mode in
  telemetry-based microservice RCA.
- We design MEO, an offline LM-assisted evidence-operator synthesis and
  verification stage that converts operational mechanism knowledge into frozen,
  deterministic evidence semantics for RCA.
- We present CREST, the online counterfactual ranker in CREST-MEO, which combines
  incident-local robust evidence scaling, mechanism-aware evidence families,
  trace-context modeling, and denoised structural support.
- We design a counterfactual explain-away procedure that uses topology to test
  whether mutation-like evidence can explain propagation-like symptoms.
- We evaluate CREST-MEO on 1,422 RCABench cases and show that its full
  multi-modal counterfactual ranking outperforms local, topology-only, and
  modality-restricted ablations, as well as traditional RCA baselines in the
  reported comparison set.

### 2 Motivation and Problem Statement

Consider an incident in which a service starts returning abnormal status codes
for a subset of requests. Its upstream callers experience longer waits, its
downstream services may observe changed traffic patterns, and the system may
generate new log templates or repeated traces. A severity-based method may rank
the service with the largest latency or log burst first. A graph-based method
may further amplify that service if many anomalous calls reach it. Neither
reasoning path is sufficient unless the method also asks what role each signal
plays in the incident.

CREST-MEO is motivated by three observations.

First, multi-modal telemetry contains role-specific evidence. Status-code
shifts, endpoint-distribution shifts, error-rate changes, and count drops often
indicate root-local mutation or request-handling failure. Duration inflation,
trace-count rises, log bursts, and template changes can be symptoms of
propagation. Metric shifts may indicate local resource pressure but can also be
background context. Observability-volume features are useful but can reflect
measurement bias. A robust RCA method should preserve these distinctions.

Second, topology is useful only when paired with evidence roles. A trace edge
shows that a symptom could propagate between two services, but it does not by
itself reveal which service is the root. CREST-MEO therefore avoids using
topology as a pure centrality or score-propagation prior. Instead, it uses
topology to identify pairs where a mutation-like candidate can explain a
propagation-like neighbor.

Third, evidence must be normalized inside each incident. Different features have
different units, row counts, and dynamic ranges. CREST-MEO uses incident-local
robust scaling so that ranking is based on relative evidence within the current
case rather than raw feature magnitude.

Formally, let `S = {s_1, ..., s_n}` be the services observed in an incident. For
each service, the algorithm receives telemetry before and after the detected
anomaly time. The output is a ranked list of services. The objective is not to
rank services by local abnormality alone, but to rank them by a score that
combines local evidence and counterfactual explanatory power over structurally
related symptoms.

### 3 Approach Overview

CREST-MEO has an offline stage and an online stage. Figure 1 should present
these stages as a pipeline: LM-assisted evidence-operator synthesis,
deterministic verification, compiled online evidence extraction,
incident-local scaling, counterfactual structural ranking, and final service
ranking.

In the offline stage, the LM proposes mechanism-grounded evidence operators
under a constrained operator schema. Verifiers check schema validity, required
fields, leakage risks, and runtime computability. Accepted operators are frozen
before evaluation. In the current implementation, the frozen semantics are
available both as MEOL JSON artifacts and as compiled/built-in feature and role
logic in the online scorer.

In the first online stage, CREST-MEO extracts deterministic service-level evidence from
metrics, logs, traces, and topology. Metric features capture value shifts,
anomaly counts, and observation-count drops. Trace features capture duration
shifts, count changes, endpoint shifts, error-rate changes, status-code shifts,
self-duration shifts, and topology degrees. Log features capture count changes,
error-rate changes, and template-distribution changes.

In the second online stage, CREST-MEO normalizes evidence within the current incident.
Each feature column is clipped by an incident-local positive 95th percentile,
and service-level vectors are mapped into a bounded scale using a median-positive
saturating transform. This scaling makes the ranking robust to feature units and
case-specific volume differences.

In the third online stage, CREST-MEO builds structural evidence. It first adjusts local
structural energy with parent context from trace edges. Then it applies
counterfactual explain-away over trace-adjacent pairs. A service is treated as a
candidate root for a neighboring victim when it has stronger mutation evidence,
the victim has stronger propagation evidence, and the victim currently carries
more structural energy. The victim's excess burden is partially transferred to
the candidate in proportion to mutation excess, propagation excess, and the
energy gap.

In the fourth online stage, CREST-MEO computes the final score. Let `A(s)` be local
abnormality, `F(s)` be counterfactual explanatory power after structural
explain-away, and `S(s)` be denoised structural support computed after excluding
a high-noise trace-duration channel. The final score is:

```text
score(s) = A(s) * F(s) + S(s)
```

Services are ranked by this score with deterministic tie-breaking.

### 4 Algorithm Design

#### 4.1 Offline MEO Synthesis and Verification

CREST-MEO separates evidence formation from incident-time diagnosis. Before
evaluation, the offline MEO stage uses an LM to propose evidence operators that
encode operational mechanisms such as request mutation, service disappearance,
latency propagation, log-event shifts, and observability-volume effects. The LM
does not output root causes and is not called during online RCA. Its output is a
candidate operator library.

Each operator must declare its telemetry source, required fields, contrast over
normal and abnormal windows, aggregation level, and evidence-role prior. Static
and leakage verifiers reject operators that violate the schema, depend on
answer metadata, use unavailable fields, or cannot be executed on unlabeled
telemetry. The accepted library is frozen before benchmark evaluation.

The current runtime exposes the frozen MEO semantics in two equivalent forms.
The JSON-MEOL path can instantiate operators explicitly. The compiled `crest.py`
path materializes the accepted feature and role semantics directly as built-in
feature families and counterfactual mutation/propagation memberships. This
compiled path is used for efficient deterministic evaluation.

#### 4.2 Multi-Modal Evidence Extraction

CREST-MEO reads normal and abnormal telemetry frames and constructs a
service-by-feature matrix. The implementation supports three telemetry
modalities. Metric evidence captures value changes and observation-count drops.
Trace evidence captures request duration, count, endpoint, status, error-rate,
self-duration, and topology information. Log evidence captures count, error, and
template-distribution changes.

The algorithm includes all services observed in telemetry frames and trace
parent-service fields. Missing modalities do not stop execution; unavailable
features simply contribute zero evidence. This behavior is important for RCA
benchmarks where not every service exposes every modality.

#### 4.3 Robust Incident-Local Scaling

Raw telemetry features have incompatible scales. CREST-MEO first applies a
non-negative log transform during feature construction. It then scales each
feature column by the incident-local positive 95th percentile and clips extreme
values. Finally, aggregate vectors such as local abnormality and structural
support are mapped into `[0, 1]` with a saturating transform based on the median
positive value in the same incident.

This normalization is deliberately local to the incident. It avoids requiring a
training set, avoids label information, and reduces the risk that services with
large telemetry volume dominate the ranking simply because of scale.

#### 4.4 Mechanism-Aware Evidence Families

CREST-MEO groups evidence into mechanism-aware families. Metric-shift features
capture local resource or performance changes. Trace-mutation features capture
interface or protocol changes such as endpoint shifts, status-code shifts, and
trace error-rate changes. Trace-propagation features capture latency, count, and
self-duration changes that may reflect downstream or upstream symptom spread.
Log-shift features capture event and template changes. Observability-volume and
topology-context features provide supporting context but are not treated as
standalone proof of causality.

The implementation uses explicit mutation and propagation feature sets for
counterfactual explain-away. These sets are not learned at runtime; they are the
compiled representation of the offline MEO evidence semantics.

#### 4.5 Trace Context as Explanation Structure

CREST-MEO derives trace edges from parent-child service relationships. It uses
these edges in two ways. First, parent context smooths structural seed evidence:
when a service has parents in the trace graph, its structural energy is blended
with the average energy of its parents using a density-dependent weight.
Second, trace adjacency defines the candidate-victim pairs considered by
counterfactual explain-away.

The important design choice is that topology does not directly make a service a
root cause. Topology only creates an opportunity for explanation. A candidate
must still have stronger mutation-like evidence than its neighbor, and the
neighbor must have stronger propagation-like evidence.

#### 4.6 Counterfactual Explain-Away

For each trace-adjacent pair, CREST-MEO considers both directions. Suppose
service `i` is a candidate root and service `j` is a candidate victim. Energy is
transferred from `j` to `i` only if:

```text
structural_energy(j) > structural_energy(i)
mutation(i) > mutation(j)
propagation(j) > propagation(i)
```

The transfer is proportional to three factors: the structural energy gap, the
relative mutation excess of `i`, and the relative propagation excess of `j`.
Only the strongest candidate root is used for each victim in one iteration. The
procedure repeats for a small bounded number of iterations or until convergence.

This operation implements the paper's core counterfactual question: if service
`i` were the root, how much of service `j`'s symptom burden would become
explainable as propagation rather than independent root evidence?

#### 4.7 Denoised Structural Support and Final Ranking

The final ranking also uses a denoised structural support term. The current
implementation removes `trace_duration_z` from this support path, then applies
the same parent-context and counterfactual explain-away logic. This term helps
retain structurally supported evidence while reducing reliance on a noisy
duration channel.

The final score is `A * F + S`. Local abnormality alone is insufficient because
it can favor victims. Explanatory power alone is insufficient because a service
with little local evidence should not dominate. Denoised support helps preserve
robust structural evidence. The product-and-support form reflects these
constraints.

### 5 Evaluation Results

#### RQ1: Overall Effectiveness

CREST-MEO completes all 1,422 RCABench cases without execution errors. It
achieves 0.875326 MRR, 0.800281 AC@1, 0.944444 AC@3, 0.971871 AC@5, 0.883497
Avg@3, and 0.917300 Avg@5. These results mean that CREST-MEO ranks a ground
truth service first in 1,138 cases, within the top three in 1,343 cases, and
within the top five in 1,382 cases.

Within the supplied paper comparison set, CREST-MEO is the strongest method
across MRR, AC@1, AC@3, and AC@5. The nearest reported ablation,
`crest_local`, reaches 0.824138 MRR and 0.705345 AC@1. CREST-MEO therefore
improves MRR by 0.051188 and AC@1 by 0.094936 absolute, while also improving
AC@3 from 0.939522 to 0.944444 and AC@5 from 0.967651 to 0.971871.

Compared with traditional RCA baselines, the gap is larger. MicroRCA achieves
0.609371 MRR and 0.527426 AC@1; MicroRank achieves 0.298642 MRR and 0.135021
AC@1; MicroHECL achieves 0.514768 MRR and 0.514768 AC@1; BARO achieves 0.537925
MRR and 0.412096 AC@1; RCD and Nezha obtain below 0.10 MRR in the reported
results. CREST-MEO's advantage is not limited to top-1 accuracy: it also
maintains 94.44% AC@3 and 97.19% AC@5, indicating that even when it misses the
first position, it usually places the root cause near the top of the ranking.

#### RQ2: Contribution of Counterfactual Ranking

The strongest evidence for CREST-MEO's design comes from the contrast with
`crest_nocf`. This ablation replaces the counterfactual explain-away path with a
PageRank-style topology prior. It achieves 0.664688 MRR and 0.490155 AC@1.
CREST-MEO improves AC@1 by 31.01 percentage points and MRR by 0.210638. The
large drop shows that topology alone is not enough; the method needs the
mutation-versus-propagation condition that decides when a neighbor's abnormality
should be explained away.

The comparison with `crest_local` is also informative. Local evidence alone is
already strong, with 0.705345 AC@1 and 0.939522 AC@3. However, CREST-MEO raises
AC@1 to 0.800281. This indicates that local evidence can often place the root
near the top, but counterfactual structural ranking is needed to resolve the
hard top-1 competition between a root and a propagated victim.

#### RQ3: Contribution of Telemetry Modalities

The modality ablations show that no single evidence source is sufficient.
`crest_trace` achieves 0.709243 MRR and 0.560478 AC@1. `crest_log` is much
weaker, with 0.393698 MRR and 0.171589 AC@1. `crest_metric` reaches 0.517921
MRR and 0.381857 AC@1. Combining modalities improves results:
`crest_metric_trace` obtains 0.818233 MRR and 0.703235 AC@1, while
`crest_log_trace` obtains 0.743158 MRR and 0.617440 AC@1. The full method still
outperforms these variants, achieving 0.875326 MRR and 0.800281 AC@1.

These results support the multi-modal design. Trace evidence is important for
topology and protocol changes, metric evidence helps capture local shifts and
count drops, and logs contribute event and template changes. The full method's
top-1 advantage suggests that CREST-MEO benefits from combining these signals
rather than relying on a single modality.

#### RQ4: Runtime

CREST-MEO has an average runtime of 9.158382 seconds per case and completes all
cases without errors. This cost is comparable to or better than the strongest
reported ablations. `crest_local` averages 10.557463 seconds, and `crest_nocf`
averages 11.304127 seconds. CREST-MEO is slower than lightweight baselines such
as BARO, but it is substantially faster than several traditional methods:
MicroRCA averages 24.493223 seconds, MicroRank averages 24.852426 seconds,
MicroDIG averages 55.964886 seconds, RCD averages 30.470458 seconds, and Nezha
averages 35.374271 seconds.

The runtime profile is consistent with the algorithm design. CREST-MEO performs
deterministic feature extraction, incident-local scaling, bounded topology
passes, and sorting. It does not require online model training, online LLM
reasoning, or expensive causal discovery in the reported path.

#### RQ5: Offline MEO Safety and Runtime Determinism

CREST-MEO uses LM assistance only before evaluation. The offline MEO stage
generates candidate evidence operators under a constrained schema, and verifier
checks reject operators that are malformed, depend on answer metadata, or cannot
be computed from unlabeled telemetry. The accepted semantics are frozen before
benchmark execution.

This design makes the online RCA path deterministic. During evaluation, the
ranker reads only normal and abnormal telemetry frames, computes the compiled
evidence features, applies counterfactual ranking, and emits a service-level
ordering. It does not read labels, injection metadata, previous outputs, or
ground-truth files, and it does not call an LLM at incident time. This separation
is central to the paper's claim: CREST-MEO uses LM synthesis to construct
mechanism-grounded evidence semantics, but it preserves the reproducibility and
latency profile of a deterministic RCA algorithm.

### 6 Ablation Study

The ablation results clarify which parts of CREST-MEO matter most.

The `crest_local` ablation removes counterfactual structural ranking and ranks
services using local evidence. Its high AC@3 but lower AC@1 suggests that local
evidence often identifies a small candidate set but struggles to choose the root
over nearby victims.

The `crest_nocf` ablation keeps topology but replaces explain-away with a
PageRank-style graph prior. Its substantial decline shows that graph structure
should not be used as generic suspiciousness propagation. The useful signal is
not centrality itself; it is whether mutation-like evidence in one service can
explain propagation-like evidence in another.

The modality ablations show that full multi-modal evidence is necessary for the
reported top-1 performance. Metric+trace is the strongest partial variant, but
it still trails the full method by 9.70 percentage points in AC@1. Log-only and
metric-only variants are insufficient, while trace-only ranking lacks the
additional local and log evidence needed for robust root selection.

The `crest_nocalib` row is identical to CREST-MEO in the reported metrics. This
should not be framed as evidence that calibration is important. Instead, either
remove this ablation from the paper or explain that the current calibration flag
does not change the evaluated scoring path.

### 7 Discussion

CREST-MEO's empirical advantage comes from modeling evidence roles. The method
does not assume that all abnormality supports the same root-cause hypothesis.
Instead, it separates local abnormality from explanatory power and uses trace
adjacency only when the evidence roles support a root-victim interpretation.
This makes the approach especially suitable for incidents where symptoms are
amplified through service calls.

The method is also intentionally deterministic. It does not rely on labels,
ground-truth files, historical leaderboard outputs, or case-specific service
names. This is important for avoiding benchmark leakage and for making the RCA
output reproducible. The LM and verifier operate before benchmark evaluation;
the online path uses the frozen evidence semantics compiled into the CREST-MEO
ranker. This distinction is important for the paper: the method can claim
LM-assisted evidence synthesis, but the measured RCA runtime and ranking output
come from deterministic execution.

There are several limitations. First, the method uses mechanism-informed feature
roles formed offline, and incorrect accepted roles can affect ranking. Second,
trace coverage matters because counterfactual explain-away operates over
trace-adjacent pairs. Third, incidents where the root has weak mutation evidence
and victims have strong local evidence remain difficult. Fourth, the current
evaluation should be expanded beyond the supplied RCABench result set before
making broad claims about external deployment generality.

### 8 Threats to Validity

**Internal validity.** The main risk is provenance ambiguity. The paper name
`crest-meo` refers to the offline MEO plus online CREST ranker design, while the
reported result row is named `crest` in the benchmark output. The paper should
state that this row is the compiled deterministic runtime instantiation of the
offline-synthesized and verified CREST-MEO semantics, and should report the exact
command and algorithm key used for evaluation.

**Construct validity.** AC@1, AC@3, AC@5, Avg@k, and MRR measure ranking
quality, but they do not directly measure operator usefulness or diagnostic
explanation quality. Claims about explanation actionability require additional
case studies or user evaluation.

**External validity.** The reported results are based on RCABench datapacks.
Although the algorithm is label-free and avoids service-name hardcoding,
additional datasets and production incidents are needed to validate
generalization across architectures, telemetry schemas, and fault distributions.

**Ablation validity.** The current ablation set supports claims about
counterfactual ranking and modality contribution. It supports the safety and
reproducibility role of offline MEO through the method design, but it does not
isolate the accuracy contribution of each verifier rule unless additional
verifier ablations are reported.

**Baseline validity.** The paper should clearly define the comparison set. If
internal repository methods such as `cera`, `evidencerank_arc`, or
`evidencerank` are excluded, the reason should be stated. If they are included,
the current claim that CREST-MEO is the overall best algorithm must be revised.

### 9 Conclusion

This paper presented CREST-MEO, a two-stage RCA method for microservice systems.
The offline MEO stage uses LM-assisted synthesis and deterministic verification
to form mechanism-grounded evidence semantics. The online CREST ranker executes
those frozen semantics deterministically, separating local abnormality from
counterfactual explanatory power. It extracts metric, log, trace, and topology
evidence, applies incident-local robust scaling, organizes evidence into
mechanism-aware families, and uses trace topology to explain propagation-like
symptoms through mutation-like root evidence. On 1,422 RCABench cases,
CREST-MEO completes without errors and achieves 0.875326 MRR, 0.800281 AC@1,
0.944444 AC@3, and 0.971871 AC@5. Ablations show that the main gain comes from
counterfactual explain-away and full multi-modal evidence fusion. These results
support the central claim that microservice RCA should reason about what role
each telemetry signal plays, not only how abnormal it is.

## 7. 需要作者确认的问题列表

1. Which exact CLI command and registry key should be reported for the compiled
   deterministic CREST-MEO result row?
2. Should internal algorithms `cera`, `evidencerank_arc`, and `evidencerank` be
   excluded from the paper comparison set? If yes, what is the principled reason
   (e.g., internal predecessor, not part of submitted baseline pool, different
   research artifact)?
3. Are RCABench's 1,422 datapacks from one benchmark suite only, or should the
   paper name multiple underlying microservice systems? The current text avoids
   naming systems until confirmed.
4. Should `crest_nocalib` remain in the paper? Its reported metrics are
   identical to CREST-MEO, so it does not currently demonstrate a calibration
   effect.
5. Do we have per-fault-type or per-system breakdowns? They would strengthen the
   ICSE evaluation section and help explain where counterfactual explain-away is
   most useful.
6. Do we have case studies for propagated-victim corrections? One concise case
   study would make the motivation more convincing.
7. Should the final artifact include both the MEOL JSON library and the compiled
   `crest.py` fast path as reproducibility components?
