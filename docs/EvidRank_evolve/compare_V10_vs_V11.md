# EvidenceRank Compare V10 vs V11

- Created: 2026-06-02T14:37:14+08:00
- Old: `V10`
- New: `V11`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.802391 | 0.000000 |
| AC@3 | 0.943741 | 0.943741 | 0.000000 |
| AC@5 | 0.975387 | 0.975387 | 0.000000 |
| MRR | 0.875103 | 0.875337 | 0.000234 |

## Status Counts

| status | cases |
| --- | ---: |
| rank_improved | 2 |
| unchanged | 1420 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | rank_improved | 3 | 2 | 1.0 | ts-order-service;ts-ui-dashboard | ts-cancel-service|ts-ui-dashboard|loadgenerator|ts-consign-price-service|ts-travel-plan-service | response-replace-code | ts-ui-dashboard |
| ts5-ts-order-other-service-stress-6wvd48 | rank_improved | 3 | 2 | 1.0 | ts-order-other-service | ts-execute-service|ts-order-other-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | stress | ts-order-other-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
