# ICSE Packaging Plan for EvidenceRank

## Target Framing

Package EvidenceRank as a software-engineering research contribution on microservice incident diagnosis, not as a benchmark-specific leaderboard entry.

Suggested paper theme:

> EvidenceRank: Evidence-consistent multimodal root-cause localization for microservice incidents.

Core claim:

> Given an incident window, root causes can be localized more accurately by ranking services whose metric, trace, log, and topology evidence is both concentrated and causally specific, while suppressing high-volume propagation symptoms.

## Contribution Shape

1. Evidence taxonomy for microservice RCA:
   - metric deviations;
   - trace distribution shifts;
   - protocol/status mutations;
   - log anomaly concentration;
   - topology root-victim contrast.
2. A label-free RCA ranking algorithm:
   - raw normal/abnormal incident frames only;
   - no labels, injection metadata, historical outputs, or `conclusion.parquet`;
   - semantic evidence priors plus bounded per-case reliability adjustment.
3. Fair evaluation protocol:
   - RCA conditioned on a known incident window;
   - raw-only baselines separated from baselines that consume processed alarm-service hints;
   - multimodal and feature-level ablations.
4. Reusable artifact:
   - containerized runner;
   - one-command evaluation;
   - scripts to regenerate tables, figures, and false-case reports.

## Recommended RQs

- RQ1 Accuracy: How does EvidenceRank compare with existing RCA methods under the same known incident-window protocol?
- RQ2 Ablation: Which evidence families are necessary for the improvement?
- RQ3 Robustness: How stable is the method under missing modalities, shifted diagnosis windows, and noisy/low-volume evidence?
- RQ4 Fairness: How do results change when baselines using `conclusion.parquet` hints are separated or disabled?
- RQ5 Efficiency and usability: What is the runtime overhead, and can the ranking be explained through feature contributions?

## Empirical Requirements

- Report `AC@1`, `MRR`, `AC@3`, `AC@5`, `error`, and runtime.
- Use paired comparisons by case, not only aggregate leaderboard numbers.
- Add confidence intervals via bootstrap and effect sizes for the main claims.
- Include ablations:
  - modality-only variants;
  - no topology;
  - no status/endpoint mutation;
  - no adaptive reliability;
  - uniform feature weights;
  - raw-only baseline set vs hint-assisted baseline set.
- Stress-test fairness by documenting that EvidenceRank does not read labels, `injection.json`, output history, or `conclusion.parquet`.

## Code Packaging

Refactor `algorithm.py` for readability before artifact release:

- `io.py`: load raw input frames;
- `features/metric.py`, `features/trace.py`, `features/log.py`, `features/topology.py`;
- `ranking.py`: score aggregation and reranking;
- `config.py`: frozen `EvidenceRankConfig`;
- `explain.py`: per-service feature contribution export;
- `cli.py`: reproduce paper tables and run single-case diagnosis.

Keep the current platform `Algorithm` interface compatible.

## ICSE Submission Notes

As of 2026-06-04, the ICSE 2027 Research Track lists:

- mandatory abstract deadline: 2026-06-23 AoE;
- paper deadline: 2026-06-30 AoE;
- double-anonymous review;
- Open Science policy where artifact sharing is expected by default but not mandatory.

The artifact track expects clean documentation and strongly encourages containers or VMs. The artifact should be executable on a clean machine and ideally install within a reasonable time.

Official sources:

- Research Track: https://conf.researchr.org/track/icse-2027/icse-2027-research-track
- Open Science Policies: https://conf.researchr.org/track/icse-2027/icse-2027-icse-2027-open-science-policies
- Artifact Evaluation: https://conf.researchr.org/track/icse-2027/icse-2027-artifact-evaluation

## Biggest Review Risks

- Single-benchmark overfitting concern if evaluation only uses RCABench.
- Hand-tuned weight concern unless weights are explained as semantic evidence priors and supported by ablations.
- Unfair baseline concern if `conclusion.parquet`-assisted methods are mixed with raw-only methods.
- Generality concern if examples sound TrainTicket-specific.

## Defensive Story

EvidenceRank should be presented as a general incident-window RCA method whose design rules are:

- compare normal vs abnormal behavior;
- prefer causal mutation evidence over victim-side propagation symptoms;
- fuse multiple observability modalities only when they provide reliable support;
- use topology to distinguish root-victim pairs;
- keep all algorithm inputs raw and label-free.
