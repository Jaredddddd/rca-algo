# EvidenceRank Compare CREST1_RAW vs CREST1

- Created: 2026-06-06T02:12:48+08:00
- Old: `CREST1_RAW`
- New: `CREST1`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.234177 | 0.699719 | 0.465541 |
| AC@3 | 0.511252 | 0.916315 | 0.405063 |
| AC@5 | 0.640647 | 0.952180 | 0.311533 |
| MRR | 0.419913 | 0.811469 | 0.391556 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 701 |
| rank_improved | 271 |
| rank_regressed | 62 |
| regressed_from_hit1 | 39 |
| unchanged | 349 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-auth-service-exception-scvnk9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-order-service|loadgenerator | exception | ts-auth-service |
| ts0-ts-basic-service-response-abort-c4gjrt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-price-service|ts-station-service|ts-travel2-service|ts-route-plan-service | response-abort | ts-basic-service |
| ts0-ts-food-service-container-kill-fc4sjw | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-consign-service|ts-seat-service|loadgenerator | container-kill | ts-food-service |
| ts0-ts-food-service-stress-dq7mwn | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-assurance-service|ts-consign-service|ts-order-other-service | stress | ts-food-service |
| ts0-ts-preserve-service-request-replace-method-2hbvml | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-basic-service|ts-travel-service|ts-security-service|ts-contacts-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-48zkx2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-basic-service|ts-ui-dashboard|ts-security-service|ts-travel-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-cw7ndj | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-security-service|loadgenerator | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-mbmqzz | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-security-service|ts-ui-dashboard|ts-order-service|ts-verification-code-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-response-abort-mj9pbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-seat-service|ts-order-service | response-abort | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-body-644lf4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-order-service|ts-order-other-service | response-replace-body | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-8h9brj | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-security-service|ts-contacts-service|ts-order-service|ts-basic-service | response-replace-code | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-8lnlwd | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-contacts-service|ts-assurance-service|ts-travel-service|ts-security-service | response-replace-code | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-ghpf5j | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-auth-service|ts-security-service | response-replace-code | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-kvkzkr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-order-service|ts-contacts-service | response-replace-code | ts-preserve-service |
| ts0-ts-route-plan-service-exception-tcmvg6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service | exception | ts-route-plan-service |
| ts0-ts-route-plan-service-request-abort-7rfdzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-basic-service|ts-travel-service|ts-travel-plan-service|ts-seat-service | request-abort | ts-route-plan-service |
| ts0-ts-route-plan-service-request-abort-x2bhww | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-food-service|ts-order-service | request-abort | ts-route-plan-service |
| ts0-ts-route-plan-service-request-replace-path-7v499h | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard|ts-travel-service | request-replace-path | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-body-xqldsl | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-travel-service|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-lnggrn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-travel-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts0-ts-travel-plan-service-request-delay-lf5tnb | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-preserve-service|ts-travel2-service|ts-order-service | request-delay | ts-travel-plan-service |
| ts0-ts-travel-plan-service-response-replace-body-mns47j | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-service | response-replace-body | ts-travel-plan-service |
| ts0-ts-travel-service-request-abort-6nm66v | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-food-service|ts-travel-plan-service|ts-basic-service | request-abort | ts-travel-service |
| ts0-ts-travel-service-request-abort-c6glmz | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service | request-abort | ts-travel-service |
| ts0-ts-travel2-service-request-abort-nnvxn4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-seat-service | request-abort | ts-travel2-service |
| ts0-ts-travel2-service-request-replace-method-2pjf4g | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-travel2-service |
| ts0-ts-travel2-service-request-replace-method-dhgqc8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-travel2-service |
| ts0-ts-ui-dashboard-request-replace-method-5dxswc | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-security-service|ts-basic-service|ts-preserve-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-ui-dashboard-request-replace-method-7bx8qb | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-auth-service|loadgenerator|ts-ui-dashboard|ts-verification-code-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-consign-service|ts-train-food-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-basic-service-request-replace-method-nhgsjg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-price-service|ts-travel2-service|ts-station-service|ts-train-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-body-bt9qt4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-station-service|ts-preserve-service|ts-price-service | response-replace-body | ts-basic-service |
| ts1-ts-food-service-request-replace-method-rq29d8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-station-food-service|ts-travel-service|ts-ui-dashboard|ts-train-food-service | request-replace-method | ts-food-service |
| ts1-ts-food-service-response-replace-code-j6ld4p | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|ts-verification-code-service|ts-auth-service|ts-travel-service | response-replace-code | ts-food-service |
| ts1-ts-inside-payment-service-container-kill-2c99w6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-consign-service|ts-preserve-service|ts-food-service | container-kill | ts-inside-payment-service |
| ts1-ts-inside-payment-service-stress-lp6wwg | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-preserve-service|ts-travel-plan-service|ts-food-service|ts-travel-service | stress | ts-inside-payment-service |
| ts1-ts-preserve-service-request-abort-x7w9vv | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-security-service|ts-contacts-service|ts-ui-dashboard|ts-food-service | request-abort | ts-preserve-service |
| ts1-ts-preserve-service-request-replace-method-9m4wvr | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-route-plan-service|ts-auth-service | request-replace-method | ts-preserve-service |
| ts1-ts-preserve-service-request-replace-method-xmhsbb | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-basic-service|ts-contacts-service|ts-ui-dashboard|ts-consign-service | request-replace-method | ts-preserve-service |
| ts1-ts-preserve-service-response-replace-body-6bfbmp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-price-service|ts-contacts-service|ts-basic-service|ts-station-service | response-replace-body | ts-preserve-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
