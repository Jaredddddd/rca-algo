# CREST_AIOPS6 Surface Competition Compare

This is an offline compare between default `crest` and the AIOPS6 ablation
`crest_surface_competition`. It reads only evaluation outputs after full eval;
no part of this analysis is used by runtime CREST.

## Metrics

| dataset | algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | crest | 230 | 0 | 0.465217 | 0.617852 | 0.695652 | 0.786957 |
| aiopschallenge2025_rcabench_service | crest_surface_competition | 230 | 0 | 0.530435 | 0.660161 | 0.734783 | 0.813043 |
| rcabench | crest | 1422 | 0 | 0.803094 | 0.876983 | 0.945148 | 0.972574 |
| rcabench | crest_surface_competition | 1422 | 0 | 0.789733 | 0.870302 | 0.945148 | 0.972574 |

## Case Deltas

| dataset | improved_to_hit1 | regressed_from_hit1 | rank_improved | rank_regressed | unchanged | top1_changed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aiopschallenge2025_rcabench_service | 36 | 21 | 0 | 13 | 160 | 113 / 230 |
| rcabench | 0 | 19 | 0 | 0 | 1403 | 21 / 1422 |

## Interpretation

AIOPS6 validates the broad direction: many AIOps25 misses are caused by a
dominant abnormal trace surface holding top-1 while a different service owns
stronger metric/log evidence. Letting the non-trace owner compete improves
AIOps25 AC@1 by `+0.065218` and MRR by `+0.042309`.

The same broad action is not safe enough. On AIOps25 it flips 113 of 230 top-1
predictions, causing 21 hit@1 regressions and 13 non-top-1 rank regressions. On
RCABench it causes 19 hit@1 regressions and no improvements. The harmed
RCABench cases are exactly the regime where CREST's trace topology is valuable:
trace/root-aligned request, response, exception, and service interaction
symptoms.

The general failure mechanism is over-demotion. Metric/log ownership is not
itself proof that trace is only propagation. A service can look like a
non-trace owner because propagated symptoms accumulate there, while the current
trace winner is still the root-aligned service. A safe future mechanism would
need a stronger causal eligibility proof before changing top-1.

## Decision

Reject `crest_surface_competition` as default. Keep it only as an ablation
showing that trace-surface suppression can help AIOps25 but needs stricter
root-eligibility protection to preserve RCABench.
