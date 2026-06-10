# EvidenceRank Compare CREST_RESIDUAL_ARBITRATION_PRE_STRUCTURAL vs CREST_RESIDUAL_STRUCTURAL_ARBITRATION

- Created: 2026-06-11T01:58:11+08:00
- Old: `CREST_RESIDUAL_ARBITRATION_PRE_STRUCTURAL`
- New: `CREST_RESIDUAL_STRUCTURAL_ARBITRATION`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.803094 | 0.822785 | 0.019691 |
| AC@3 | 0.944444 | 0.944444 | 0.000000 |
| AC@5 | 0.971871 | 0.971871 | 0.000000 |
| MRR | 0.876849 | 0.887046 | 0.010197 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 28 |
| rank_regressed | 3 |
| unchanged | 1391 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-travel2-service|ts-route-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-r727qm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-station-service|ts-travel2-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-seat-service |
| ts0-ts-travel-service-request-abort-g9mc2t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-travel2-service | request-abort | ts-travel-service |
| ts1-ts-seat-service-request-replace-path-jmcntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-inside-payment-service|ts-order-other-service|ts-travel-plan-service | request-replace-path | ts-seat-service |
| ts1-ts-seat-service-response-replace-body-hvd8x2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | response-replace-body | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-seat-service |
| ts1-ts-travel-service-response-replace-code-qzmhjf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-station-service | response-replace-code | ts-travel-service |
| ts2-ts-basic-service-request-replace-path-flkd7v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-price-service|ts-travel-service|ts-station-service | request-replace-path | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts2-ts-travel-service-bandwidth-f9fkg7 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-auth-service | bandwidth | ts-travel-service |
| ts2-ts-travel-service-response-abort-jd66zv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-contacts-service|ts-route-plan-service|ts-travel-plan-service | response-abort | ts-travel-service |
| ts2-ts-travel2-service-response-replace-code-ttpn92 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-price-service|ts-basic-service | response-replace-code | ts-travel2-service |
| ts3-ts-basic-service-response-replace-body-6lk5wq | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-price-service|ts-train-service | response-replace-body | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-bvqv9z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-station-service | response-replace-code | ts-basic-service |
| ts3-ts-seat-service-response-replace-code-xdw4c7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service | response-replace-code | ts-seat-service |
| ts3-ts-travel2-service-request-replace-method-ggdqhg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-travel-service | request-replace-method | ts-travel2-service |
| ts4-ts-basic-service-request-replace-method-hpv2qg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-route-plan-service|ts-payment-service|ts-consign-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts4-ts-travel-service-partition-xq25fj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-seat-service|ts-cancel-service | partition | ts-travel-service |
| ts4-ts-travel-service-stress-fz5lbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-cancel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service | stress | ts-travel-service |
| ts5-ts-basic-service-request-delay-4qpvfj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-seat-service|ts-security-service | request-delay | ts-basic-service |
| ts8-ts-basic-service-response-abort-fwndhj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-price-service|ts-food-service|ts-preserve-service|ts-travel-service | response-abort | ts-basic-service |
| ts9-ts-travel-service-partition-9b45sj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-food-service|ts-seat-service | partition | ts-travel-service |
| ts2-mysql-bandwidth-fws9rx | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-verification-code-service|ts-ui-dashboard | bandwidth | mysql |
| ts2-ts-basic-service-response-replace-code-qf2qml | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-station-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-2nw8nx | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-plan-service|ts-route-plan-service|ts-travel-service|ts-travel2-service | response-replace-code | ts-basic-service |
| ts4-ts-travel-service-response-replace-body-vhbkq2 | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-security-service|ts-travel-plan-service|ts-route-plan-service|ts-preserve-service | response-replace-body | ts-travel-service |
| ts4-ts-basic-service-request-replace-path-n9jq9s | improved_to_hit1 | 4 | 1 | 3.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-route-plan-service|ts-seat-service|ts-preserve-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts0-ts-seat-service-pod-failure-c87xdg | rank_regressed | 2 | 3 | -1.0 | ts-seat-service | ts-travel2-service|ts-route-plan-service|ts-seat-service|ts-travel-service|ts-travel-plan-service | pod-failure | ts-seat-service |
| ts0-ts-ui-dashboard-request-replace-method-fl9jln | rank_regressed | 3 | 4 | -1.0 | ts-ui-dashboard;ts-user-service | ts-travel2-service|ts-route-plan-service|ts-assurance-service|ts-user-service|ts-travel-plan-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-corrupt-trd2kh | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-preserve-service | ts-food-service|ts-ui-dashboard|ts-preserve-service|ts-contacts-service|ts-seat-service | corrupt | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
