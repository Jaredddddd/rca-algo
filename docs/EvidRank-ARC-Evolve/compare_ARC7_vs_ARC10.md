# EvidenceRank Compare ARC7 vs ARC10

- Created: 2026-06-03T22:33:35+08:00
- Old: `ARC7`
- New: `ARC10`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.728551 | 0.675809 | -0.052743 |
| AC@3 | 0.943741 | 0.918425 | -0.025316 |
| AC@5 | 0.973277 | 0.964838 | -0.008439 |
| MRR | 0.836843 | 0.801007 | -0.035835 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 58 |
| rank_improved | 50 |
| rank_regressed | 95 |
| regressed_from_hit1 | 133 |
| unchanged | 1086 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-response-replace-body-85cnwx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-ui-dashboard|ts-travel2-service|ts-travel-service|ts-route-plan-service | response-replace-body | ts-basic-service |
| ts0-ts-basic-service-response-replace-body-pwrcvx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-food-service | response-replace-body | ts-basic-service |
| ts0-ts-route-plan-service-request-replace-method-lrzhl6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-route-service | request-replace-method | ts-route-plan-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-order-service | response-replace-code | ts-seat-service |
| ts0-ts-travel2-service-request-replace-method-dhgqc8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-travel2-service |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-preserve-service | pod-failure | ts-user-service |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-station-food-service|ts-preserve-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-request-replace-method-v627xx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-price-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-request-replace-path-z65h6q | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | request-replace-path | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-b2ftxt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-route-plan-service-response-replace-body-5s6gc9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-travel-service | response-replace-body | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-code-lmr4bp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts1-ts-seat-service-response-replace-body-hvd8x2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service | response-replace-body | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-seat-service |
| ts1-ts-train-service-pod-failure-5qwqdz | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service | ts-train-service|ts-basic-service|ts-travel-plan-service|ts-travel-service|ts-route-plan-service | pod-failure | ts-train-service |
| ts1-ts-travel-plan-service-response-replace-code-6mlrxc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-inside-payment-service|ts-ui-dashboard|ts-travel-service|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-travel-plan-service-response-replace-code-cwn86t | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-price-service|ts-basic-service|ts-travel2-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-travel-service-request-replace-method-mgw6hv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-ui-dashboard|ts-route-plan-service|ts-route-service | request-replace-method | ts-travel-service |
| ts1-ts-travel-service-response-abort-mqhzdf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-route-plan-service|ts-basic-service|ts-verification-code-service | response-abort | ts-travel-service |
| ts1-ts-travel-service-response-replace-code-w6jftp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | response-replace-code | ts-travel-service |
| ts2-ts-basic-service-response-replace-body-zrxcjp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-preserve-service | response-replace-body | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-pqkdss | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts2-ts-consign-service-bandwidth-x9qdzm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-payment-service|ts-preserve-service | bandwidth | ts-consign-service |
| ts2-ts-preserve-service-response-replace-body-t7d296 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-contacts-service|ts-basic-service | response-replace-body | ts-preserve-service |
| ts2-ts-route-plan-service-request-replace-method-j9lggd | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-ui-dashboard|ts-seat-service | request-replace-method | ts-route-plan-service |
| ts2-ts-travel-service-request-replace-method-5snzk5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-ui-dashboard|ts-basic-service|ts-seat-service | request-replace-method | ts-travel-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-price-service|ts-travel-plan-service | pod-failure | ts-travel2-service |
| ts2-ts-travel2-service-request-replace-method-mh6crg | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-order-other-service | request-replace-method | ts-travel2-service |
| ts2-ts-ui-dashboard-response-abort-rcfl6z | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|ts-inside-payment-service|ts-travel-service|loadgenerator|ts-basic-service | response-abort | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-bzfxkt | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|loadgenerator|ts-route-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-auth-service-request-replace-path-zrc7rt | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-food-service | request-replace-path | ts-auth-service |
| ts3-ts-auth-service-response-replace-code-9cstpf | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-seat-service | response-replace-code | ts-auth-service |
| ts3-ts-basic-service-request-replace-method-ljqz6g | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-response-replace-body-6lk5wq | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service | response-replace-body | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-bvqv9z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-vm557j | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-station-service | response-replace-code | ts-basic-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-ui-dashboard|ts-preserve-service|ts-seat-service | pod-failure | ts-consign-price-service |
| ts3-ts-food-service-response-replace-code-2bmlvb | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|ts-ui-dashboard|ts-order-other-service|ts-seat-service|ts-train-food-service | response-replace-code | ts-food-service |
| ts3-ts-route-plan-service-response-replace-code-xr5ths | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts3-ts-travel-plan-service-response-replace-code-x6bzr8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-route-plan-service|ts-basic-service | response-replace-code | ts-travel-plan-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
