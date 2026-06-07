# EvidenceRank Compare CREST15_ACCEPTED vs CREST17_PATH_FANIN_AS_CREST

- Created: 2026-06-07T23:56:35+08:00
- Old: `CREST15_ACCEPTED`
- New: `CREST17_PATH_FANIN_AS_CREST`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.812940 | 0.825598 | 0.012658 |
| AC@3 | 0.945148 | 0.945148 | 0.000000 |
| AC@5 | 0.971871 | 0.971871 | 0.000000 |
| MRR | 0.882065 | 0.888980 | 0.006915 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 18 |
| rank_regressed | 1 |
| unchanged | 1403 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-travel-service-request-abort-g9mc2t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-travel2-service | request-abort | ts-travel-service |
| ts2-ts-travel-service-bandwidth-f9fkg7 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-auth-service | bandwidth | ts-travel-service |
| ts3-ts-basic-service-request-replace-method-pjwm42 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-travel-plan-service|ts-travel-service|ts-station-service | request-replace-method | ts-basic-service |
| ts3-ts-travel2-service-request-replace-method-ggdqhg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-travel-service | request-replace-method | ts-travel2-service |
| ts4-ts-basic-service-request-abort-jr6f2j | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-seat-service|ts-travel-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts4-ts-basic-service-response-abort-94gfnl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-route-plan-service|ts-travel-service|ts-seat-service | response-abort | ts-basic-service |
| ts4-ts-travel-service-partition-xq25fj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-seat-service|ts-cancel-service | partition | ts-travel-service |
| ts4-ts-travel-service-request-replace-method-s2wfxf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-consign-service|ts-travel-plan-service|ts-seat-service|ts-route-plan-service | request-replace-method | ts-travel-service |
| ts4-ts-travel2-service-request-replace-method-mn7d6d | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-auth-service | request-replace-method | ts-travel2-service |
| ts5-ts-basic-service-request-delay-4qpvfj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-seat-service|ts-security-service | request-delay | ts-basic-service |
| ts5-ts-travel2-service-request-replace-method-d4kncl | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-config-service | request-replace-method | ts-travel2-service |
| ts9-ts-travel-service-partition-9b45sj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-food-service|ts-seat-service | partition | ts-travel-service |
| ts1-mysql-loss-dfzrxw | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-order-service|ts-route-service | loss | mysql |
| ts2-mysql-bandwidth-fws9rx | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-verification-code-service|ts-ui-dashboard | bandwidth | mysql |
| ts4-ts-basic-service-response-replace-code-2nw8nx | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-plan-service|ts-route-plan-service|ts-travel-service|ts-travel2-service | response-replace-code | ts-basic-service |
| ts4-ts-travel-service-response-delay-lnpdxn | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-seat-service|ts-route-plan-service|ts-food-service | response-delay | ts-travel-service |
| ts4-ts-travel-service-response-replace-body-vhbkq2 | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-security-service|ts-travel-plan-service|ts-route-plan-service|ts-preserve-service | response-replace-body | ts-travel-service |
| ts5-ts-basic-service-partition-4wswsd | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-travel-service | partition | ts-basic-service |
| ts0-ts-seat-service-pod-failure-c87xdg | rank_regressed | 2 | 3 | -1.0 | ts-seat-service | ts-travel-service|ts-route-plan-service|ts-seat-service|ts-travel2-service|ts-travel-plan-service | pod-failure | ts-seat-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
