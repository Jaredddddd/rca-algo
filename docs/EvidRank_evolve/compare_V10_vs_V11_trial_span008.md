# EvidenceRank Compare V10 vs V11_trial_span008

- Created: 2026-06-02T14:29:32+08:00
- Old: `V10`
- New: `V11_trial_span008`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.801688 | -0.000703 |
| AC@3 | 0.943741 | 0.943741 | 0.000000 |
| AC@5 | 0.975387 | 0.975387 | 0.000000 |
| MRR | 0.875103 | 0.874985 | -0.000117 |

## Status Counts

| status | cases |
| --- | ---: |
| rank_improved | 2 |
| regressed_from_hit1 | 1 |
| unchanged | 1419 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | rank_improved | 3 | 2 | 1.0 | ts-order-service;ts-ui-dashboard | ts-cancel-service|ts-ui-dashboard|loadgenerator|ts-consign-price-service|ts-travel-plan-service | response-replace-code | ts-ui-dashboard |
| ts5-ts-order-other-service-stress-6wvd48 | rank_improved | 3 | 2 | 1.0 | ts-order-other-service | ts-execute-service|ts-order-other-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | stress | ts-order-other-service |
| ts4-ts-basic-service-request-replace-method-hpv2qg | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-price-service | ts-order-service|ts-basic-service|ts-ui-dashboard|ts-travel2-service|ts-payment-service | request-replace-method | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
