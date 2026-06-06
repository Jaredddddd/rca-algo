# EvidenceRank Compare CREST2 vs CREST3

- Created: 2026-06-06T03:49:21+08:00
- Old: `CREST2`
- New: `CREST3`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.800281 | 0.000000 |
| AC@3 | 0.944444 | 0.945851 | 0.001406 |
| AC@5 | 0.971871 | 0.972574 | 0.000703 |
| MRR | 0.875326 | 0.875744 | 0.000418 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 12 |
| rank_improved | 18 |
| rank_regressed | 10 |
| regressed_from_hit1 | 12 |
| unchanged | 1370 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-ui-dashboard-response-delay-nqtssr | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-assurance-service|ts-preserve-service|ts-auth-service | response-delay | ts-ui-dashboard |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-auth-service | pod-failure | ts-user-service |
| ts2-ts-ui-dashboard-request-abort-djrhxq | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-auth-service|ts-travel2-service | request-abort | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-abort-rcfl6z | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-inside-payment-service|ts-travel-service|ts-auth-service | response-abort | ts-ui-dashboard |
| ts3-ts-basic-service-response-delay-qh7j7v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-consign-service | response-delay | ts-basic-service |
| ts3-ts-travel-service-request-replace-path-vktk7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-path | ts-travel-service |
| ts3-ts-ui-dashboard-response-abort-zd59tz | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-assurance-service|loadgenerator|ts-ui-dashboard|ts-order-service|ts-verification-code-service | response-abort | ts-ui-dashboard |
| ts4-ts-route-service-partition-xw4bwj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-station-service|ts-travel-service|ts-train-service|ts-order-service | partition | ts-route-service |
| ts7-ts-ui-dashboard-response-replace-code-t7vsbl | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|ts-cancel-service|ts-consign-service|ts-inside-payment-service|ts-security-service | response-replace-code | ts-ui-dashboard |
| ts8-ts-route-plan-service-request-replace-path-xxpxdq | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-cancel-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | request-replace-path | ts-route-plan-service |
| ts9-ts-route-plan-service-request-replace-path-9dg8qf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-payment-service|ts-travel-plan-service|ts-consign-service|ts-seat-service | request-replace-path | ts-route-plan-service |
| ts0-ts-ui-dashboard-request-replace-method-fl9jln | improved_to_hit1 | 3 | 1 | 2.0 | ts-ui-dashboard;ts-user-service | ts-user-service|ts-route-plan-service|ts-assurance-service|ts-travel-plan-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-seat-service-request-replace-method-h4rcm9 | rank_improved | 3 | 2 | 1.0 | ts-order-service;ts-seat-service | ts-travel-service|ts-seat-service|ts-route-plan-service|ts-travel-plan-service|ts-order-service | request-replace-method | ts-seat-service |
| ts3-ts-basic-service-partition-w5hbjw | rank_improved | 10 | 9 | 1.0 | ts-basic-service;ts-travel-service | ts-ui-dashboard|ts-food-service|ts-consign-service|ts-preserve-service|ts-verification-code-service | partition | ts-basic-service |
| ts3-ts-ui-dashboard-request-replace-method-wkh6t7 | rank_improved | 3 | 2 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-basic-service|ts-travel-plan-service|ts-seat-service|ts-travel2-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-7tlb8z | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-price-service | ts-inside-payment-service|ts-route-plan-service|ts-travel2-service|ts-basic-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-sjpbd8 | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-train-service | ts-ui-dashboard|ts-payment-service|ts-travel2-service|ts-basic-service|loadgenerator | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | rank_improved | 9 | 8 | 1.0 | ts-route-plan-service;ts-travel-service | ts-ui-dashboard|loadgenerator|ts-food-service|ts-travel-plan-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts4-ts-ui-dashboard-request-delay-6b6bd5 | rank_improved | 3 | 2 | 1.0 | ts-train-service;ts-ui-dashboard | ts-assurance-service|ts-ui-dashboard|ts-seat-service|ts-preserve-service|ts-food-service | request-delay | ts-ui-dashboard |
| ts5-ts-basic-service-request-delay-4cwcs6 | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-price-service | ts-travel-plan-service|ts-route-plan-service|ts-basic-service|ts-travel2-service|ts-travel-service | request-delay | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | rank_improved | 12 | 11 | 1.0 | ts-basic-service;ts-price-service | ts-payment-service|ts-inside-payment-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | rank_improved | 7 | 6 | 1.0 | ts-basic-service;ts-price-service | ts-seat-service|ts-preserve-service|ts-cancel-service|ts-travel-service|ts-route-plan-service | request-replace-path | ts-basic-service |
| ts5-ts-route-plan-service-request-replace-method-v76qjz | rank_improved | 4 | 3 | 1.0 | ts-route-plan-service;ts-route-service | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-travel-service|ts-basic-service | request-replace-method | ts-route-plan-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | rank_improved | 4 | 3 | 1.0 | ts-order-other-service;ts-ui-dashboard | loadgenerator|ts-seat-service|ts-ui-dashboard|ts-station-food-service|ts-travel2-service | request-abort | ts-ui-dashboard |
| ts5-ts-ui-dashboard-request-replace-method-dxffln | rank_improved | 4 | 3 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service|loadgenerator|ts-ui-dashboard|ts-basic-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts7-mysql-loss-dxzvbj | rank_improved | 3 | 2 | 1.0 | mysql;ts-user-service | ts-ui-dashboard|ts-user-service|loadgenerator|ts-travel-service|ts-auth-service | loss | mysql |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | rank_improved | 6 | 5 | 1.0 | ts-food-service;ts-ui-dashboard | ts-order-service|ts-consign-service|ts-contacts-service|ts-seat-service|ts-ui-dashboard | request-abort | ts-ui-dashboard |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | rank_improved | 8 | 7 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service|ts-consign-service|ts-food-service|ts-cancel-service|ts-consign-price-service | request-replace-method | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | rank_improved | 11 | 10 | 1.0 | ts-train-service;ts-ui-dashboard | ts-payment-service|ts-inside-payment-service|ts-food-service|ts-assurance-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts9-ts-ui-dashboard-response-replace-code-4bfgrj | rank_improved | 7 | 6 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-payment-service|ts-inside-payment-service|ts-seat-service|ts-food-service|ts-basic-service | response-replace-code | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | rank_regressed | 15 | 17 | -2.0 | mysql | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|ts-food-service | container-kill | mysql |
| ts0-ts-seat-service-pod-failure-c87xdg | rank_regressed | 2 | 4 | -2.0 | ts-seat-service | ts-route-plan-service|ts-travel-service|ts-travel2-service|ts-seat-service|ts-travel-plan-service | pod-failure | ts-seat-service |
| ts2-ts-order-other-service-container-kill-48rlds | rank_regressed | 4 | 5 | -1.0 | ts-order-other-service | ts-seat-service|ts-preserve-service|ts-travel2-service|ts-basic-service|ts-order-other-service | container-kill | ts-order-other-service |
| ts2-ts-travel-service-bandwidth-f9fkg7 | rank_regressed | 2 | 3 | -1.0 | mysql;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-ui-dashboard|ts-auth-service | bandwidth | ts-travel-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | rank_regressed | 17 | 18 | -1.0 | ts-consign-service | ts-basic-service|ts-travel-service|ts-food-service|ts-ui-dashboard|ts-seat-service | pod-failure | ts-consign-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | rank_regressed | 3 | 4 | -1.0 | ts-payment-service | ts-inside-payment-service|ts-order-service|ts-order-other-service|ts-payment-service|ts-basic-service | pod-failure | ts-payment-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | rank_regressed | 9 | 10 | -1.0 | ts-preserve-service;ts-ui-dashboard | ts-train-food-service|ts-food-service|ts-order-service|ts-seat-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-mysql-corrupt-kgjmhg | rank_regressed | 2 | 3 | -1.0 | mysql;ts-train-service | ts-route-plan-service|ts-travel-plan-service|ts-train-service|ts-travel-service|ts-basic-service | corrupt | mysql |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | rank_regressed | 6 | 7 | -1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | rank_regressed | 4 | 5 | -1.0 | ts-route-plan-service;ts-travel-plan-service | ts-preserve-service|ts-ui-dashboard|ts-consign-price-service|ts-travel2-service|ts-travel-plan-service | response-replace-code | ts-travel-plan-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
