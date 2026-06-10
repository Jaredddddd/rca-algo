# PV_CREST3 Analysis

## Evaluation Stop Point

Per the user request, optimization is paused after the PV_CREST3 evaluation.
No further selector or scoring experiments are opened in this round.

Freshly evaluated current `crest`:

| dataset | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aiopschallenge2025_rcabench_service` | 230 | 0 | 0.526087 | 0.672613 | 0.782609 | 0.865217 |
| `rcabench` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

Against `PV_CREST2_DYNAMIC_AIOPS25_SERVICE`, PV_CREST3 keeps AIOps25 AC@1
unchanged, improves MRR by `+0.009901`, improves AC@3 by `+0.026087`, and
improves AC@5 by `+0.039130`. It has 5 `improved_to_hit1`, 5
`regressed_from_hit1`, 16 `rank_improved`, and 3 `rank_regressed`. RCABench is
unchanged on all reported metrics.

PV_CREST3 adds a service-level representativeness factor to metric provenance
atoms. The factor is unsupervised: it uses incident-local raw row support to
downweight provenance candidates that look like isolated metric entities rather
than service-level RCA candidates. It helps MRR/top-k, but does not solve the
top-1 gap.

## Useful Optimizations

| mechanism | evidence | decision |
| --- | --- | --- |
| Incident-local trace structural confidence / AIOPS1 | AIOps25 AC@1 `0.334783 -> 0.413043`; RCABench stayed near baseline | Useful safe intermediate |
| Narrow modality ownership / AIOPS2 | AIOps25 AC@1 `0.413043 -> 0.465217`; RCABench slightly improved | Useful accepted mechanism |
| DyMo-style dynamic evidence selection / PV_CREST2 | AIOps25 AC@1 `0.334783 -> 0.526087`, MRR `0.503603 -> 0.662711`; RCABench unchanged | Most useful safe PV-CREST mechanism so far |
| Service representativeness for provenance / PV_CREST3 | AIOps25 MRR `0.662711 -> 0.672613`, AC@3/AC@5 improve; RCABench unchanged | Useful for ranking depth, not top-1 |
| Broad surface competition / AIOPS6 | AIOps25 AC@1 reached `0.530435`, showing the failure mode is real | Useful diagnostic, rejected as default because RCABench dropped to `0.789733` |

## Unhelpful Or Unsafe Optimizations

| mechanism | evidence | decision |
| --- | --- | --- |
| Broad partial-view root/exposure override / PV_CREST1 | AIOps25 AC@1 improved to `0.430435`, but RCABench collapsed to `0.492264` | Unsafe |
| Provenance as broad direct arbitration / AIOPS3 | AIOps25 barely improved, RCABench regressed | Unsafe as default |
| Trace-root eligibility only / AIOPS4 | No AIOps25 gain | Not useful |
| Adaptive modality gate that required strict ownership dominance / AIOPS5 | No ranking change | Too conservative |
| `pv_crest_role_intervention` | AIOps25 AC@1 `0.404348`, below current dynamic `crest` | Not useful |
| Simple `metric+log` switch | AIOps25 `crest_metric_log` AC@1 `0.478261`; RCABench `crest_metric_log` AC@1 `0.440928` | Not acceptable; sacrifices trace-root cases |

## High-AC@1 Feasibility Analysis

It is not mathematically impossible for an oracle to reach AIOps25 AC@1 near
`0.70`, but it looks very unlikely for the current CREST representation to do
so with a purely incident-local unsupervised selector while also preserving
RCABench.

Empirical upper-bound signals:

| oracle view set on AIOps25 | hit@1 | AC@1 |
| --- | ---: | ---: |
| current `crest` | 121 / 230 | 0.526087 |
| `crest` OR `crest_metric_log` | 155 / 230 | 0.673913 |
| `crest` OR `evidencerank_metric_log` | 165 / 230 | 0.717391 |
| `crest` OR metric/log variants from CREST/CERA/EvidenceRank | 167 / 230 | 0.726087 |
| `crest` OR CREST single-modality variants | 177 / 230 | 0.769565 |

These are oracle unions, not valid runtime algorithms. To reach `AC@1 >= 0.70`
from current `crest`, a selector needs at least 40 net additional top-1 hits.
The `crest + evidencerank_metric_log` oracle has only 44 extra hits available
over current `crest`, so a label-free selector would need to recover almost all
of those cases while preserving almost all current trace/base hits. Previous
unsupervised broad selectors show why that is hard: they recover many AIOps25
service-level cases but also demote valid trace/root-aligned cases.

The core identifiability issue:

- RCABench full multimodal often rewards trace-root-aligned reasoning:
  protocol mutation, request/response behavior, and topology explain-away.
- AIOps25 service-level often hides the service root from trace and exposes it
  through metric/log/resource provenance; trace then becomes an entry or
  propagation surface.
- Metric/log ownership is not proof of root locality. Propagated victims can
  also own strong metric/log anomalies.
- Trace dominance is not proof of exposure. Some trace-dominant services are
  true roots.
- In single-incident, label-free inference, these two regimes can be
  observationally equivalent unless there is extra causal evidence such as
  stronger resource provenance, repeated incidents, service-role priors, or a
  self-supervised history model.

Conclusion: with only current raw per-incident CREST features and no learned
history, simultaneously achieving very high AIOps25 service-level AC@1 and
preserving RCABench appears close to an identifiability limit rather than just a
missing threshold. The current best safe direction is to keep PV_CREST2/PV_CREST3
as evidence-qualified mechanisms and treat further jumps toward `0.70` as
requiring additional unsupervised information, for example historical incident
prototypes, repeated service-role calibration, or richer resource/provenance
atoms rather than broader online trace demotion.

## Code Hygiene Cleanup

After the analysis pause, the CREST implementation was cleaned up without
opening a new optimization round.

Rollback note: after a follow-up review, the user requested reverting all CREST
runtime modifications from the AIOps25 optimization attempt. The cleanup
changes and PV-CREST runtime mechanisms are therefore historical notes only;
the default code was restored to the pre-AIOps25 optimization source state.

- Default runtime path now lives in
  `algorithms/evidencerank/src/evidencerank/crest.py`.
- Experimental and rejected variants now live in
  `algorithms/evidencerank/src/evidencerank/crest_experiments.py`.
- Removed unused dynamic-selection draft helpers:
  `_active_dynamic_families`, `_score_dynamic_evidence_view`,
  `_dynamic_selection_quality`, and their private support helpers.
- Removed unused `_counterfactual_explanatory_power` from the default file.
- Moved `crest_partial_view` and `pv_crest_role_intervention` implementation
  into the experiment file.
- Moved local/PageRank NoCF ablation support into the experiment file.
- Removed the CERA/ARC `_ordinal_evidence_energy` dependency from default
  `crest`; dynamic evidence selection now uses CREST's own incident-local
  `role_matrix`.
- Removed the duplicate `pv_crest_dynamic_selection` registry entry because
  current default `crest` already uses dynamic selection.
- Renamed the counterfactual iteration control from a family tuple to an
  explicit max-iteration count, preserving behavior while fixing the misleading
  loop semantics.

Verification after cleanup:

- `python -m compileall -q algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_experiments.py algorithms/evidencerank/main.py`
- `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard`
- import smoke for `CREST`, `CRESTMetricLog`, `CRESTPartialView`, and
  `PV_CRESTRoleIntervention`
- direct `score_crest_services` smoke on
  `aiops2025-009be6db-313-code-error`

## Artifacts

- `PV_CREST3_REPRESENTATIVE_AIOPS25_SERVICE`
- `PV_CREST3_REPRESENTATIVE_RCABENCH`
- `docs/EvidRank_evolve/PV_CREST3_REPRESENTATIVE_AIOPS25_SERVICE_summary.md`
- `docs/EvidRank_evolve/PV_CREST3_REPRESENTATIVE_RCABENCH_summary.md`
- `docs/EvidRank_evolve/cross_compare_PV_CREST2_DYNAMIC_AIOPS25_SERVICE_vs_PV_CREST3_REPRESENTATIVE_AIOPS25_SERVICE.md`
- `docs/EvidRank_evolve/cross_compare_PV_CREST2_DYNAMIC_RCABENCH_vs_PV_CREST3_REPRESENTATIVE_RCABENCH.md`
