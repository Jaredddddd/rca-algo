# EvidenceRank Compare ARC7 vs ARC11

- Created: 2026-06-03T22:41:58+08:00
- Old: `ARC7`
- New: `ARC11`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.728551 | 0.728551 | 0.000000 |
| AC@3 | 0.943741 | 0.943741 | 0.000000 |
| AC@5 | 0.973277 | 0.973277 | 0.000000 |
| MRR | 0.836843 | 0.836637 | -0.000206 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 1 |
| rank_improved | 1 |
| rank_regressed | 2 |
| regressed_from_hit1 | 1 |
| unchanged | 1417 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts9-ts-preserve-service-response-replace-code-jxdnlj | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-payment-service|ts-ui-dashboard|ts-assurance-service|ts-food-service | response-replace-code | ts-preserve-service |
| ts9-ts-preserve-service-request-replace-method-dw9h5j | rank_improved | 5 | 4 | 1.0 | ts-preserve-service;ts-travel-service | ts-food-service|ts-verification-code-service|ts-ui-dashboard|ts-preserve-service|ts-basic-service | request-replace-method | ts-preserve-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | rank_regressed | 10 | 11 | -1.0 | ts-basic-service;ts-price-service | ts-preserve-service|ts-route-plan-service|ts-ui-dashboard|ts-food-service|ts-travel-plan-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-request-delay-4cwcs6 | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-price-service | ts-travel-plan-service|ts-route-plan-service|ts-basic-service|ts-travel2-service|ts-order-service | request-delay | ts-basic-service |
| ts0-ts-travel2-service-request-delay-lzpl9v | regressed_from_hit1 | 1 | 3 | -2.0 | ts-seat-service;ts-travel2-service | ts-consign-service|ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|ts-travel-service | request-delay | ts-travel2-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
