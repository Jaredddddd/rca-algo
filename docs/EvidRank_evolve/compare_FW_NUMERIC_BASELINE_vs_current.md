# EvidenceRank Compare FW_NUMERIC_BASELINE vs current

- Created: 2026-06-03T23:17:59+08:00
- Old: `FW_NUMERIC_BASELINE`
- New: `current`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.800985 | -0.001406 |
| AC@3 | 0.943741 | 0.942335 | -0.001406 |
| AC@5 | 0.975387 | 0.975387 | 0.000000 |
| MRR | 0.875337 | 0.874517 | -0.000820 |

## Status Counts

| status | cases |
| --- | ---: |
| rank_regressed | 2 |
| regressed_from_hit1 | 2 |
| unchanged | 1418 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts6-ts-basic-service-response-replace-code-s7bcv7 | rank_regressed | 3 | 4 | -1.0 | ts-basic-service;ts-price-service | ts-seat-service|ts-payment-service|ts-inside-payment-service|ts-basic-service|ts-order-service | response-replace-code | ts-basic-service |
| ts7-ts-ui-dashboard-response-replace-code-t7vsbl | rank_regressed | 3 | 4 | -1.0 | ts-travel-service;ts-ui-dashboard | ts-cancel-service|ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts2-ts-basic-service-response-replace-code-rmprwq | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-route-service | ts-travel-service|ts-basic-service|ts-route-plan-service|ts-travel2-service|ts-station-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-request-replace-method-hpv2qg | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-price-service | ts-order-service|ts-basic-service|ts-ui-dashboard|ts-payment-service|ts-travel2-service | request-replace-method | ts-basic-service |

## Decision Notes

- This report is equivalent to `compare_FW_NUMERIC_BASELINE_vs_FW_PRIORITY_PRIOR.md`; `current` was the priority-prior output at generation time.
- Decision: accept as an optional SRE-priority representation, not as an accuracy-improving ranking change.
- The priority prior is nearly behavior-preserving: 2 fewer top-1 hits, 2 fewer top-3 hits, unchanged AC@5, and MRR `-0.000820`.
- The observed regressions are all one-rank movements and are consistent with removing the old feature-specific near-baseline value for `trace_count_drop_shift`.
