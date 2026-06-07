# CREST ICSE Paper Draft

Status: initial paper-facing draft.

Scope note: the main baseline comparison deliberately excludes CERA and
EvidenceRank because they are internal methods from the same research line. They
can be mentioned, if needed, only as internal prototypes or appendix ablations,
not as prior work.

## Packaging Memo

### One-sentence pitch

CREST reframes microservice RCA from "ranking the most abnormal component" to
"ranking the component whose local evidence and architectural position can
counterfactually explain away the incident symptoms."

### Plain-language idea

Existing RCA algorithms often pick the service with the loudest telemetry
change. In microservices, the loudest service is frequently a downstream victim,
an entry service, or a high-traffic relay. CREST asks a different question: if
this service were the root, would its local mutation evidence and trace-topology
position explain the symptoms observed in its neighbors?

### ICSE-friendly framing

The paper should not sell CREST as a fancy model. The software-engineering angle
is incident triage under realistic observability constraints:

- Production microservices expose heterogeneous telemetry, but incident labels
  and fault-specific training data are scarce.
- Operators need a ranked service list that is auditable from raw metrics,
  traces, logs, and call topology.
- The central failure mode in existing methods is an observability-causality
  mismatch: telemetry salience is treated as diagnostic responsibility.
- CREST contributes a lightweight, label-free ranking semantics that separates
  local mutation evidence from propagated victim symptoms.

### The "fatal blind spot" phrased politely

Many prior approaches assume that the same signal used to detect an incident can
also localize its cause. This conflates anomaly salience with explanatory
sufficiency. In distributed systems, however, an incident changes the telemetry
of both the faulty component and its dependents. A root-cause localizer must
therefore reason about whether a candidate can explain other anomalies, not only
whether it is anomalous itself.

### Terms to use consistently

- Observability-causality gap
- Explanatory sufficiency
- Counterfactual explain-away
- Topology-conditioned evidence roles
- Local mutation evidence versus propagated victim symptoms
- Denoised structural support
- Modality ablation
- Raw-only, label-free incident-window diagnosis

### Terms to avoid overusing

- "AI" or "deep learning": CREST is intentionally not positioned there.
- "Benchmark winner": ICSE reviewers will read that as overfitting unless the
  design argument and ablations are strong.
- "Causal discovery": CREST uses counterfactual ranking semantics over observed
  topology, not full causal graph identification.

## Draft Paper

# CREST: Counterfactual Evidence Ranking for Microservice Root Cause Localization

## Abstract

Root-cause localization for microservice incidents is commonly formulated as a
ranking problem over services. Existing methods detect deviations in metrics,
traces, or logs and then rank the components with the strongest abnormality,
correlation, graph centrality, or learned representation shift. This design is
attractive because the same telemetry used for incident detection can be reused
for diagnosis. However, it hides a critical mismatch: in a microservice system,
the most observable symptoms are often produced by downstream victims, entry
services, or high-traffic relays rather than by the faulty component itself.
Consequently, ranking anomaly salience is not equivalent to ranking diagnostic
responsibility.

We present CREST, a label-free root-cause localization method that ranks
services by counterfactual explanatory power over raw incident telemetry. CREST
first extracts local evidence families from metrics, traces, logs, and service
topology, distinguishing root-like mutation evidence from propagated victim
symptoms. It then applies a topology-conditioned explain-away operation: when a
candidate has stronger local mutation evidence and a neighboring service has
stronger propagation evidence, CREST transfers only the explainable victim
symptom mass back to the candidate. Finally, a denoised structural support
channel preserves multi-feature explanatory evidence while excluding standalone
latency spikes that often indicate propagation. CREST requires no incident
labels, no fault-type classifier, no pretrained model, and no benchmark-specific
metadata.

On 1,422 RCABench incidents, CREST achieves AC@1 of 0.800, MRR of 0.875, AC@3 of
0.944, and AC@5 of 0.972 using only raw normal and abnormal telemetry frames.
Among external baselines in the local evaluation inventory, the strongest
non-internal methods reach AC@1 between 0.527 and 0.515. Ablations show that
CREST's improvement is not due to generic graph centrality: replacing its
counterfactual propagation with a PageRank-style graph prior reduces AC@1 from
0.800 to 0.492. These results suggest that microservice RCA benefits from
ranking explanatory sufficiency rather than anomaly magnitude alone.

## 1. Introduction

Microservice architectures turn software failures into distributed diagnostic
problems. A delayed request, a killed container, a broken network link, or an
incorrect response mutation may first appear as many simultaneous symptoms:
latency shifts in downstream services, status-code changes at entry points,
volume drops near the fault, and log changes in unrelated error handlers. During
incident response, engineers must decide which service to inspect first. A
ranking that places a high-observability victim above the true faulty component
can waste the most valuable minutes of triage.

The research community has proposed many automated root-cause analysis methods
for this setting. Statistical methods compare normal and abnormal metric
distributions. Trace-centric methods construct call graphs and rank suspicious
operations by correlation, random walks, spectral formulas, or Shapley-style
credit assignment. Pattern-mining methods compare normal and abnormal event
sequences. Supervised fusion methods learn service representations from
multi-modal telemetry and labeled incidents. These approaches cover an
impressive design space, but they share a common simplifying assumption: signals
that are useful for detecting an incident are treated as directly useful for
localizing the root cause.

This assumption is fragile in microservice systems. Telemetry is not attached
only to the faulty component. A root component can become less observable after a
crash or request drop, while its callers or callees accumulate large latency,
error, or volume changes. A graph-centrality algorithm may promote a busy
service because many symptoms pass through it. A metric-only algorithm may miss
protocol or trace mutations. A supervised model may learn dataset-specific
symptom patterns that are difficult to audit in a new deployment. In all cases,
the unresolved question is not whether a service is abnormal, but whether its
abnormality can explain the other abnormalities around it.

This paper argues that microservice RCA should be formulated as explanatory
ranking under architectural propagation. CREST operationalizes this view with
three design choices.

First, CREST separates evidence roles. Local mutation signals such as count
drops, endpoint shifts, status-code shifts, and error-rate changes are treated
differently from victim-side symptoms such as duration shifts, volume rises, and
broad log/template drift. The goal is not to attach a hand-written fault rule to
each service, but to preserve the diagnostic semantics of each telemetry family.

Second, CREST performs topology-conditioned counterfactual explain-away. Given a
pair of neighboring services, if one service has stronger mutation evidence
while the other has stronger propagation evidence, CREST transfers only the
explainable symptom mass from the apparent victim back to the plausible cause.
This differs from random walk or PageRank-style scoring, which spreads
suspicion through the graph without asking whether the transferred mass has the
right diagnostic role.

Third, CREST keeps the final score compact and auditable rather than adding a
case-local calibration layer. Cross-modal agreement is useful for analysis, but
sparse root evidence is common in real incidents. CREST therefore evaluates
metric, trace, log, and pairwise modality ablations separately instead of letting
modality agreement suppress valid single-channel root signals.

The result is a practical, raw-only RCA algorithm. CREST consumes the same
incident-window data that operators already collect: normal and abnormal
metrics, traces, logs, and parent-child trace topology. It does not read labels,
injection metadata, previous outputs, processed conclusions, service-name
whitelists, or fault-type identifiers. This input discipline matters for
software-engineering evaluation because it separates deployable diagnosis from
benchmark-specific oracle access.

This paper makes the following contributions:

- We identify the observability-causality gap in microservice RCA: ranking
  anomaly salience does not necessarily rank diagnostic responsibility.
- We introduce CREST, a label-free counterfactual evidence-ranking algorithm
  that separates local mutation evidence from propagated victim symptoms.
- We provide an ablation-based evaluation showing that CREST's gains come from
  counterfactual structural explain-away rather than generic graph centrality.
- We release a reproducible artifact that runs on raw incident telemetry through
  the existing RCA benchmark interface.

## 2. Motivation

### 2.1 RCA is not anomaly detection

Anomaly detection answers whether observed behavior deviates from a reference.
RCA asks which component should be changed, restarted, rolled back, or inspected
to make the incident disappear. These are related but not identical questions.
For example, a database partition can produce low request counts at the database
service, high latency at business services, and error logs at entry services.
The entry service may be the loudest telemetry source, but repairing it would
not remove the incident. In diagnostic terms, it is a symptom-bearing node, not
an explanatory node.

Many RCA systems collapse this distinction because abnormality provides an
available ranking signal. A service with a high z-score, high correlation with
an alert, high PageRank in an abnormal subgraph, or high learned anomaly score is
placed near the top. This works when root causes are locally loud. It fails when
the root is low-observability and its dependents amplify the symptoms.

### 2.2 Microservice topology creates role ambiguity

The same telemetry feature can have different meanings depending on topology.
High duration in a callee may indicate local work inflation. High duration in a
caller may indicate waiting on a downstream dependency. Count drops can indicate
a failing component, but count rises can indicate traffic concentration around a
victim path. Log bursts can indicate local failure handling, but they can also
reflect propagated retries. A useful RCA method must therefore model telemetry
features as role-conditioned evidence rather than as dimensionless anomaly
magnitudes.

### 2.3 Why not simply learn the mapping?

Supervised multi-modal RCA models can learn symptom-to-root mappings when
labeled incidents are available. This is valuable in controlled environments,
but it creates three obstacles for general incident response research. First,
incident labels are scarce and expensive. Second, learned mappings can encode
architecture-specific fault patterns that do not transfer across systems. Third,
operators often need to audit why a service was ranked first. CREST targets the
complementary setting: no labels, no pretrained model, and an explanation that
can be traced back to raw evidence families and topology.

## 3. Existing Algorithms and the Missing Diagnostic Step

We organize the existing algorithms in the repository into families. This table
excludes CERA and EvidenceRank because they are internal methods from the same
research line as CREST.

| Family | Examples in `algorithms/` | Typical mechanism | Missing diagnostic step |
| --- | --- | --- | --- |
| Metric deviation | Baro, HeroSAS, RCD, CausalRCA, RUN | Compare normal and abnormal metric series, then aggregate metric-level anomalies or learned metric graphs to services. | Non-resource failures often manifest first in traces or logs; metric abnormality is not separated into root mutation versus propagated load. |
| Trace graph ranking | MicroDig, MicroRCA, MicroRank, TON, MicroHECL | Build abnormal trace graphs and rank operations or services using correlation, random walk, PageRank, spectral suspiciousness, or propagation heuristics. | Graph centrality and trace salience can promote high-traffic victims; the graph move does not ask whether the source has root-like local evidence. |
| Statistical credit assignment | ShapleyIQ | Attribute abnormal trace latency to operations with cooperative-game credit assignment. | Credit assignment over observed timelines can still assign cost to operations that suffer from upstream/downstream delays rather than cause them. |
| Event-pattern mining | Nezha | Encode traces/logs as events and compare normal versus abnormal sequence patterns. | Event motif shifts are instrumentation-dependent and do not by themselves distinguish causal mutations from propagated error handling. |
| Rule/vote fusion | SimpleRCA | Run independent metric, trace, and log detectors and combine top-k rankings by fixed voting. | Voting improves robustness but loses feature semantics and cannot explain away a strong victim when it appears in several detectors. |
| Supervised deep fusion | ART, DiagFusion, Eadro | Train representation or graph neural models over multi-modal telemetry. | Labeled training can be powerful, but deployability depends on label availability, architecture transfer, and explanation of learned symptom priors. |

The common pattern is not that these algorithms are poorly designed. Rather,
they solve a slightly different problem: they find components that are abnormal,
central, correlated, or representationally surprising. CREST adds the missing
diagnostic step: a candidate should be ranked highly when its local evidence and
topological position make it an explanation for neighboring symptoms.

## 4. CREST

CREST stands for Counterfactual Ranking of Evidence via Structural Topology. It
is a service-level ranking algorithm for a known incident window. CREST receives
normal and abnormal telemetry frames and returns a ranked list of services.

### 4.1 Inputs and evidence extraction

CREST uses only raw incident-window frames:

- `normal_metrics.parquet` and `abnormal_metrics.parquet`
- `normal_traces.parquet` and `abnormal_traces.parquet`
- `normal_logs.parquet` and `abnormal_logs.parquet`

From these frames, CREST extracts service-level feature families:

- metric shifts: z-score, mean/value deviations, anomaly count, count drop
- trace mutations: endpoint shift, error rate, status-code shift
- trace propagation symptoms: duration shift, count change, count rise/drop,
  self-duration relative shift
- log shifts: count change, error keyword rate, template change
- observability volume: abnormal metric and trace row counts
- topology context: trace-derived parent-child service relations

Each feature is scaled within the current incident using robust positive
percentile normalization and saturating transforms. This prevents raw row counts
or high-volume services from dominating solely due to scale.

### 4.2 Local abnormality `A`

CREST first computes a local abnormality score:

```text
A(v) = saturated_case_scale(sum_role_families(v))
```

`A` is not intended to be the final RCA score. It is a local evidence substrate:
how much service `v` changed relative to the incident. This preserves useful
symptom information while deferring causal interpretation to the structural
stage.

### 4.3 Counterfactual structural factor `F`

CREST then evaluates whether a service can explain symptoms around it. For a
neighboring pair `(u, v)`, CREST compares root-like mutation evidence and
victim-like propagation evidence:

```text
mutation_excess(u, v) = max(0, mutation(u) - mutation(v))
propagation_excess(v, u) = max(0, propagation(v) - propagation(u))
```

If `u` has stronger mutation evidence and `v` has stronger propagation evidence,
CREST transfers only the explainable score gap from `v` to `u`:

```text
transfer(u <- v) =
    score_gap(v, u)
    * mutation_share(u, v)
    * propagation_share(v, u)
```

This is the core explain-away operation. It says: the victim's suspiciousness
should be reduced only to the extent that a neighbor has the right kind of local
evidence to explain it. CREST applies this operation over trace-derived
neighbor pairs and converts the resulting structural energy into `F`.

### 4.4 Denoised structural support `S`

Some roots have moderate local abnormality but broad structural support.
CREST therefore adds a denoised support channel `S`, computed from the same
structural operations but excluding standalone trace duration z-score, which is
often a propagated latency symptom. The accepted score is:

```text
score(v) = A(v) * F(v) + S(v)
```

`S` helps retain multi-feature structural evidence without letting a single
latency spike dominate the rank.

### 4.5 Implementation discipline

The runtime implementation does not read labels, injection metadata, previous
rankings, evaluation outputs, or processed conclusion files. It also does not
hard-code datapack IDs, service names, fault names, or dataset splits. This
discipline is important for the paper: the method is an incident-window RCA
algorithm, not a benchmark oracle.

## 5. Research Questions

RQ1. Accuracy: How accurately does CREST localize root-cause services compared
with external RCA baselines under the same incident-window evaluation protocol?

RQ2. Diagnostic mechanism: Does CREST's counterfactual explain-away outperform
generic graph centrality or local abnormality alone?

RQ3. Evidence roles: Which telemetry families contribute to root-victim
separation across metric, trace, log, and topology evidence?

RQ4. Robustness: How does CREST behave under missing modalities, sparse root
evidence, and high-observability victim services?

RQ5. Practicality: What runtime overhead and explanation artifacts does CREST
provide for incident triage?

## 6. Evaluation Design

### 6.1 Dataset and protocol

The current evaluation uses RCABench with 1,422 incidents. Each algorithm
receives the incident's raw telemetry folder and returns a service-level ranking.
We report AC@1, MRR, AC@3, AC@5, error count, and average runtime.

The paper should emphasize fairness:

- Methods are evaluated at the service level.
- The incident window is assumed known for all methods.
- The main raw-only comparison should disclose whether any baseline consumes
  processed alarm or conclusion hints.
- Internal methods from the same research line, including CERA and EvidenceRank,
  are not counted as external prior work.

### 6.2 External baseline inventory

The table below summarizes local results from `results.md`, excluding internal
CERA and EvidenceRank variants.

| Algorithm | Main evidence | AC@1 | MRR | AC@3 | AC@5 | Runtime avg |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| CREST | metrics/traces/logs/topology | 0.800 | 0.875 | 0.944 | 0.972 | 8.78s |
| MicroRCA | traces/conclusion-style graph ranking | 0.527 | 0.609 | 0.600 | 0.711 | 24.49s |
| MicroDig | trace graph random walk | 0.515 | 0.636 | 0.749 | 0.785 | 55.96s |
| MicroHECL | trace propagation heuristics | 0.515 | 0.515 | 0.515 | 0.515 | 24.34s |
| HeroSAS | metrics | 0.487 | 0.611 | 0.676 | 0.766 | 14.04s |
| Baro | metrics | 0.412 | 0.538 | 0.596 | 0.698 | 1.05s |
| SimpleRCA | rules over metrics/traces/logs | 0.332 | 0.541 | 0.713 | 0.895 | 1.88s |
| ShapleyIQ | traces | 0.313 | 0.461 | 0.502 | 0.668 | 55.68s |
| CausalRCA | metrics/causal graph | 0.164 | 0.294 | 0.357 | 0.390 | 134.40s |
| TON | traces | 0.152 | 0.285 | 0.282 | 0.409 | 23.40s |
| MicroRank | traces | 0.135 | 0.299 | 0.321 | 0.454 | 24.85s |
| RCD | metrics/causal discovery | 0.057 | 0.092 | 0.125 | 0.141 | 30.47s |
| Nezha | traces/log event patterns | 0.044 | 0.071 | 0.101 | 0.108 | 35.37s |

Interpretation: the strongest external baselines are trace-centric methods, but
they still lag CREST at top-1 localization. This supports the paper's central
claim: topology is useful only when paired with evidence-role semantics.

### 6.3 Ablation study

CREST includes explicit ablation entry points:

| Variant | Removed or replaced module | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: |
| CREST | Full method without calibration | 0.800 | 0.875 | 0.944 | 0.972 |
| CREST-NoCF | Replace counterfactual explain-away with PageRank-style graph prior | 0.492 | 0.666 | 0.814 | 0.937 |
| CREST-Local | Use local abnormality only | 0.705 | 0.824 | 0.940 | 0.968 |
| CREST-Metric | Metric-only modality ablation | TBD | TBD | TBD | TBD |
| CREST-Trace | Trace-only modality ablation | TBD | TBD | TBD | TBD |
| CREST-Log | Log-only modality ablation | TBD | TBD | TBD | TBD |
| CREST-MetricTrace | Metric + trace modality ablation | TBD | TBD | TBD | TBD |
| CREST-MetricLog | Metric + log modality ablation | TBD | TBD | TBD | TBD |
| CREST-LogTrace | Log + trace modality ablation | TBD | TBD | TBD | TBD |

This ablation is the strongest evidence for the method section. Local
abnormality alone is already useful, but it does not reach the full method.
Replacing counterfactual explain-away with generic graph propagation causes the
largest regression. Therefore, CREST's contribution is not "use topology" in the
abstract; it is using topology to apply role-aware counterfactual symptom
redistribution.

### 6.4 Additional experiments to add before submission

The current draft should be strengthened with the following experiments:

- Bootstrap confidence intervals for AC@1 and MRR.
- Per-fault and per-service-group deltas for CREST versus the strongest external
  baselines.
- Missing-modality stress tests: metric-only, trace-only, log-only,
  metric+trace, trace+log.
- Raw-only fairness split that separates baselines using processed conclusion
  hints from baselines using only raw telemetry.
- Case studies with feature-level explanations for one successful explain-away
  case and one remaining failure case.

## 7. Discussion

### 7.1 Why CREST is a software-engineering contribution

CREST is not primarily a new statistical anomaly detector. Its contribution is a
diagnostic semantics for software architecture telemetry. The method encodes a
practical insight used by experienced on-call engineers: a service that screams
in telemetry is not necessarily the service that should be fixed. By making this
insight explicit and reproducible, CREST turns an operational debugging pattern
into an algorithmic ranking procedure.

### 7.2 Why the method is not just another graph ranker

Graph rankers propagate suspicion along edges. CREST conditions propagation on
evidence roles. A victim symptom can be explained away only when a neighbor has
stronger root-like mutation evidence. This is why the CREST-NoCF ablation is
important: replacing the counterfactual operation with PageRank-style graph
propagation collapses top-1 accuracy.

### 7.3 Why the method is not just another fusion heuristic

CREST does fuse metrics, traces, and logs, but the fusion is not a flat vote.
Feature families are assigned diagnostic roles before aggregation. Duration,
count, endpoint, status, log, and topology evidence are not interchangeable
votes; they are different kinds of evidence in a root-victim explanation.

## 8. Threats to Validity

Single-benchmark evaluation. The current evidence is strongest on RCABench.
Before submission, the paper should either add another benchmark or clearly
frame RCABench as the primary controlled incident corpus and strengthen
case-level analysis.

Incident-window assumption. CREST assumes the normal and abnormal windows are
provided. This matches many benchmark protocols and post-alert triage workflows,
but it does not solve alert detection or incident-window discovery.

Telemetry schema dependence. CREST uses common metric, trace, and log fields,
but production schemas vary. The artifact should document required columns and
fallback service-name resolution.

Baseline fairness. Some historical RCA baselines may rely on processed
conclusion or alarm hints. The final paper must separate raw-only and
hint-assisted settings to avoid overstating comparisons.

Interpretability limits. CREST exposes `A`, `F`, `S`, and feature families,
but a full operator-facing explanation UI is future work.

## 9. Related Work

Metric-based RCA. Metric methods identify deviations between normal and
abnormal time series and aggregate suspicious metrics to services. Examples in
the local artifact include Baro, RCD, CausalRCA, and RUN. They are effective
when resource metrics directly expose the fault, but they underrepresent
protocol, trace, and log-only failures.

Trace-based RCA. Trace methods exploit call graphs and operation timelines.
MicroRCA, MicroRank, MicroDig, MicroHECL, TON, and ShapleyIQ represent different
forms of graph ranking, correlation analysis, spectral suspiciousness, and
credit assignment. CREST builds on the insight that topology is essential, but
adds role-conditioned counterfactual explain-away instead of generic graph
propagation.

Log and event-pattern RCA. Methods such as Nezha compare event patterns across
normal and abnormal windows. CREST uses logs as one evidence family, but avoids
making event-pattern shifts the sole localization mechanism.

Supervised multi-modal RCA. ART, DiagFusion, and Eadro learn representations
from multi-modal telemetry. CREST targets the complementary deployment regime in
which labels, checkpoints, or architecture-specific retraining are unavailable
or undesirable during incident response.

TODO: replace these placeholder references with verified bibliographic entries
before submission.

## 10. Conclusion

Microservice RCA requires more than finding the most abnormal service. Because
faults propagate through service topology, high-observability symptoms often
appear at victims rather than roots. CREST addresses this observability-causality
gap by ranking services according to counterfactual explanatory power: local
mutation evidence, denoised structural support, and topology-conditioned
explain-away of propagated symptoms. The result is a label-free, raw-only, and
auditable RCA method that substantially improves top-1 localization over the
external baselines in the current artifact. More broadly, CREST suggests that
future RCA tools should treat telemetry features as diagnostic roles in an
architectural explanation, not merely as anomaly magnitudes to be summed,
walked, or learned.

## Reviewer-facing Claim Checklist

- Do not claim CREST discovers a complete causal graph.
- Do not claim CREST is supervised or trained.
- Do not compare against CERA/EvidenceRank as prior work.
- Do claim CREST closes the observability-causality gap by moving from anomaly
  salience to explanatory sufficiency.
- Do support the mechanism with the CREST-Local and CREST-NoCF ablations.
- Do disclose raw-only input discipline and any baseline that consumes processed
  conclusion hints.
