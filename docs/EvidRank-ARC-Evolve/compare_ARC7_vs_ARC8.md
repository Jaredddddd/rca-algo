# EvidenceRank Compare ARC7 vs ARC8

- Created: 2026-06-03T21:48:46+08:00
- Old: `ARC7`
- New: `ARC8`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.728551 | 0.677918 | -0.050633 |
| AC@3 | 0.943741 | 0.917722 | -0.026020 |
| AC@5 | 0.973277 | 0.963432 | -0.009845 |
| MRR | 0.836843 | 0.802414 | -0.034429 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 77 |
| rank_improved | 55 |
| rank_regressed | 93 |
| regressed_from_hit1 | 149 |
| unchanged | 1048 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-response-replace-body-85cnwx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-travel2-service|ts-route-plan-service | response-replace-body | ts-basic-service |
| ts0-ts-basic-service-response-replace-body-pwrcvx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-food-service | response-replace-body | ts-basic-service |
| ts0-ts-route-plan-service-request-replace-method-lrzhl6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-route-service | request-replace-method | ts-route-plan-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-order-service|ts-route-plan-service | response-replace-code | ts-seat-service |
| ts0-ts-seat-service-response-replace-code-gqm7pj | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-order-service|ts-travel-plan-service | response-replace-code | ts-seat-service |
| ts0-ts-travel2-service-request-replace-method-dhgqc8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-travel2-service |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-preserve-service | pod-failure | ts-user-service |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-station-food-service|ts-preserve-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-request-replace-method-v627xx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-price-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-request-replace-path-z65h6q | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | request-replace-path | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-2vvxvm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-5pdcrx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-b2ftxt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-payment-service-stress-5778hg | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|ts-basic-service|ts-assurance-service | stress | ts-payment-service |
| ts1-ts-route-plan-service-response-replace-code-lmr4bp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts1-ts-seat-service-response-replace-body-hvd8x2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service | response-replace-body | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-order-service | response-replace-code | ts-seat-service |
| ts1-ts-security-service-response-replace-code-q2nwzg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-travel-service | response-replace-code | ts-security-service |
| ts1-ts-train-service-pod-failure-5qwqdz | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service | ts-train-service|ts-basic-service|ts-travel-plan-service|ts-travel2-service|ts-travel-service | pod-failure | ts-train-service |
| ts1-ts-travel-plan-service-response-replace-code-6mlrxc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-inside-payment-service|ts-ui-dashboard|ts-travel-service|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-travel-plan-service-response-replace-code-cwn86t | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-price-service|ts-basic-service|ts-travel2-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-travel-service-request-replace-method-mgw6hv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-ui-dashboard|ts-route-plan-service|ts-route-service | request-replace-method | ts-travel-service |
| ts1-ts-travel-service-response-abort-mqhzdf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-route-plan-service|ts-verification-code-service|ts-basic-service | response-abort | ts-travel-service |
| ts1-ts-travel-service-response-replace-body-vzcxrp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-preserve-service | response-replace-body | ts-travel-service |
| ts1-ts-travel-service-response-replace-code-w6jftp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-travel-service |
| ts1-ts-ui-dashboard-request-abort-sksx9s | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel2-service|ts-food-service | request-abort | ts-ui-dashboard |
| ts2-ts-auth-service-response-replace-code-zb5np6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-voucher-service | response-replace-code | ts-auth-service |
| ts2-ts-basic-service-response-replace-body-zrxcjp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-preserve-service | response-replace-body | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-pqkdss | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts2-ts-consign-service-bandwidth-x9qdzm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-payment-service|ts-preserve-service | bandwidth | ts-consign-service |
| ts2-ts-preserve-service-response-replace-body-t7d296 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-contacts-service|ts-basic-service | response-replace-body | ts-preserve-service |
| ts2-ts-route-plan-service-request-replace-method-j9lggd | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-ui-dashboard|ts-seat-service | request-replace-method | ts-route-plan-service |
| ts2-ts-route-plan-service-request-replace-method-jw9nkv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-seat-service | request-replace-method | ts-route-plan-service |
| ts2-ts-route-plan-service-request-replace-method-r6ktcx | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-preserve-service|ts-travel2-service|ts-ui-dashboard | request-replace-method | ts-route-plan-service |
| ts2-ts-travel-service-request-replace-method-5snzk5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-basic-service|ts-ui-dashboard|ts-seat-service | request-replace-method | ts-travel-service |
| ts2-ts-travel-service-response-replace-code-w4bgvh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel-plan-service | response-replace-code | ts-travel-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-price-service|ts-travel-plan-service | pod-failure | ts-travel2-service |
| ts2-ts-travel2-service-request-replace-method-mh6crg | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-service | request-replace-method | ts-travel2-service |
| ts2-ts-travel2-service-response-replace-code-4xptvj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-basic-service | response-replace-code | ts-travel2-service |
| ts2-ts-ui-dashboard-response-abort-rcfl6z | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|ts-inside-payment-service|ts-travel-service|loadgenerator|ts-basic-service | response-abort | ts-ui-dashboard |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
