# EvidenceRank Compare CREST1_RAW vs CREST2

- Created: 2026-06-06T03:20:11+08:00
- Old: `CREST1_RAW`
- New: `CREST2`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.234177 | 0.800281 | 0.566104 |
| AC@3 | 0.511252 | 0.944444 | 0.433193 |
| AC@5 | 0.640647 | 0.971871 | 0.331224 |
| MRR | 0.419913 | 0.875326 | 0.455413 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 845 |
| rank_improved | 156 |
| rank_regressed | 41 |
| regressed_from_hit1 | 40 |
| unchanged | 340 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-auth-service-exception-scvnk9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-consign-service|ts-preserve-service | exception | ts-auth-service |
| ts0-ts-basic-service-response-abort-c4gjrt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-price-service|ts-station-service|ts-travel2-service|ts-train-service | response-abort | ts-basic-service |
| ts0-ts-food-service-container-kill-fc4sjw | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-consign-service|ts-preserve-service|ts-travel-plan-service | container-kill | ts-food-service |
| ts0-ts-food-service-stress-dq7mwn | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-station-food-service|ts-consign-service|ts-travel-service | stress | ts-food-service |
| ts0-ts-food-service-stress-xfwkgh | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-preserve-service|ts-auth-service|ts-train-food-service | stress | ts-food-service |
| ts0-ts-preserve-service-request-replace-method-2hbvml | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-basic-service|ts-travel-service|ts-contacts-service|ts-security-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-48zkx2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-basic-service|ts-ui-dashboard|ts-security-service|ts-contacts-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-cw7ndj | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-contacts-service|ts-security-service|ts-ui-dashboard|ts-auth-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-mbmqzz | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-security-service|ts-ui-dashboard|ts-order-service|ts-auth-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-response-abort-mj9pbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-travel-plan-service|ts-food-service|ts-basic-service | response-abort | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-body-644lf4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-security-service|ts-ui-dashboard|ts-food-service|ts-order-other-service | response-replace-body | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-8h9brj | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-security-service|ts-contacts-service|ts-order-service|ts-basic-service | response-replace-code | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-8lnlwd | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-contacts-service|ts-security-service|ts-assurance-service|ts-ui-dashboard | response-replace-code | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-ghpf5j | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-security-service|ts-auth-service|ts-ui-dashboard|ts-order-other-service | response-replace-code | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-kvkzkr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-food-service|ts-basic-service | response-replace-code | ts-preserve-service |
| ts0-ts-route-plan-service-exception-tcmvg6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-travel-service|ts-basic-service | exception | ts-route-plan-service |
| ts0-ts-route-plan-service-request-abort-7rfdzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-travel-service|ts-seat-service | request-abort | ts-route-plan-service |
| ts0-ts-route-plan-service-request-abort-x2bhww | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service|ts-travel-service | request-abort | ts-route-plan-service |
| ts0-ts-route-plan-service-request-replace-path-7v499h | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard|ts-route-service | request-replace-path | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-body-xqldsl | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel2-service|ts-travel-plan-service|ts-basic-service|ts-travel-service | response-replace-body | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-lnggrn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service | response-replace-code | ts-route-plan-service |
| ts0-ts-travel-plan-service-request-delay-lf5tnb | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service | request-delay | ts-travel-plan-service |
| ts0-ts-travel-plan-service-response-replace-body-mns47j | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard|ts-route-service | response-replace-body | ts-travel-plan-service |
| ts0-ts-travel-service-pod-failure-cvrncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-ui-dashboard | pod-failure | ts-travel-service |
| ts0-ts-travel-service-request-abort-6nm66v | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-food-service|ts-basic-service|ts-seat-service | request-abort | ts-travel-service |
| ts0-ts-travel-service-request-abort-c6glmz | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service | request-abort | ts-travel-service |
| ts0-ts-travel2-service-request-abort-nnvxn4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-basic-service | request-abort | ts-travel2-service |
| ts0-ts-travel2-service-request-replace-method-2pjf4g | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-travel2-service |
| ts0-ts-travel2-service-request-replace-method-dhgqc8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-travel2-service |
| ts0-ts-ui-dashboard-request-replace-method-5dxswc | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-travel-plan-service|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-ui-dashboard-request-replace-method-7bx8qb | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-auth-service|loadgenerator|ts-ui-dashboard|ts-verification-code-service|ts-food-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-price-service|ts-cancel-service|loadgenerator|ts-travel-plan-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-basic-service-request-replace-method-nhgsjg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-price-service|ts-station-service|ts-train-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-body-bt9qt4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-station-service|ts-travel-service|ts-price-service|ts-preserve-service | response-replace-body | ts-basic-service |
| ts1-ts-food-service-request-replace-method-rq29d8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-station-food-service|ts-travel-service|ts-ui-dashboard|ts-train-food-service | request-replace-method | ts-food-service |
| ts1-ts-food-service-response-replace-code-j6ld4p | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|ts-train-food-service|ts-auth-service|ts-verification-code-service | response-replace-code | ts-food-service |
| ts1-ts-inside-payment-service-container-kill-2c99w6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-cancel-service|ts-preserve-service|ts-ui-dashboard|ts-consign-service | container-kill | ts-inside-payment-service |
| ts1-ts-inside-payment-service-stress-lp6wwg | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-payment-service|ts-preserve-service|ts-food-service|ts-travel-service | stress | ts-inside-payment-service |
| ts1-ts-preserve-service-request-replace-method-9m4wvr | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-food-service | request-replace-method | ts-preserve-service |
| ts1-ts-preserve-service-request-replace-method-xmhsbb | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-basic-service|ts-ui-dashboard|ts-contacts-service|ts-security-service | request-replace-method | ts-preserve-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
