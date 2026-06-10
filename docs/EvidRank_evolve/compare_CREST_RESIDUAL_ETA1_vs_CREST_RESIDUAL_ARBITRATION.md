# EvidenceRank Compare CREST_RESIDUAL_ETA1 vs CREST_RESIDUAL_ARBITRATION

- Created: 2026-06-11T00:44:05+08:00
- Old: `CREST_RESIDUAL_ETA1`
- New: `CREST_RESIDUAL_ARBITRATION`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.803094 | 0.002813 |
| AC@3 | 0.944444 | 0.944444 | 0.000000 |
| AC@5 | 0.971871 | 0.971871 | 0.000000 |
| MRR | 0.875326 | 0.876849 | 0.001524 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 4 |
| unchanged | 1418 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts3-ts-travel-service-request-replace-path-vktk7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-path | ts-travel-service |
| ts8-ts-route-plan-service-request-replace-path-xxpxdq | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-cancel-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | request-replace-path | ts-route-plan-service |
| ts9-ts-route-plan-service-request-replace-path-9dg8qf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-payment-service|ts-consign-service|ts-travel-plan-service|ts-seat-service | request-replace-path | ts-route-plan-service |
| ts3-ts-ui-dashboard-request-replace-method-wkh6t7 | improved_to_hit1 | 3 | 1 | 2.0 | ts-travel-plan-service;ts-ui-dashboard | ts-travel-plan-service|ts-basic-service|ts-seat-service|ts-travel2-service|ts-travel-service | request-replace-method | ts-ui-dashboard |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
