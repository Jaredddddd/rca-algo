# EvidenceRank Compare V11 vs V19

- Created: 2026-06-02T22:25:39+08:00
- Old: `V11`
- New: `V19`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.658931 | -0.143460 |
| AC@3 | 0.943741 | 0.877637 | -0.066104 |
| AC@5 | 0.975387 | 0.927567 | -0.047820 |
| MRR | 0.875337 | 0.776972 | -0.098365 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 73 |
| rank_improved | 53 |
| rank_regressed | 97 |
| regressed_from_hit1 | 277 |
| unchanged | 922 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-gqn7nd | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service|ts-train-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-replace-body-85cnwx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-station-service|ts-train-service|ts-route-plan-service | response-replace-body | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-lmnjw7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|loadgenerator | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-station-service|ts-price-service|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-5pdcrx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-station-service | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-pqlzs2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-station-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-order-service-exception-b25hld | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|loadgenerator|ts-ui-dashboard|ts-assurance-service|ts-travel-service | exception | ts-order-service |
| ts1-ts-seat-service-response-replace-body-hvd8x2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|loadgenerator | response-replace-body | ts-seat-service |
| ts2-mysql-bandwidth-bbk2d4 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-travel-plan-service|ts-route-plan-service|ts-travel-service | bandwidth | mysql |
| ts2-ts-basic-service-request-replace-method-hjnzfp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-price-service|ts-travel2-service|ts-station-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-qf2qml | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-station-service|ts-price-service | response-replace-code | ts-basic-service |
| ts2-ts-travel2-service-response-replace-code-ttpn92 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-price-service|ts-basic-service|ts-travel-plan-service | response-replace-code | ts-travel2-service |
| ts3-ts-seat-service-response-replace-code-xdw4c7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|loadgenerator | response-replace-code | ts-seat-service |
| ts4-ts-assurance-service-container-kill-bsv8nk | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|loadgenerator|ts-station-food-service|ts-travel-plan-service | container-kill | ts-assurance-service |
| ts4-ts-consign-service-stress-rw9qhw | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|loadgenerator|ts-station-food-service|ts-ui-dashboard | stress | ts-consign-service |
| ts4-ts-inside-payment-service-stress-gc2kcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-payment-service|loadgenerator|ts-consign-service|ts-food-service | stress | ts-inside-payment-service |
| ts4-ts-order-other-service-stress-h7rsps | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-security-service|ts-payment-service|ts-travel-plan-service | stress | ts-order-other-service |
| ts4-ts-order-other-service-stress-tm48k8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-travel2-service|ts-security-service|ts-preserve-service | stress | ts-order-other-service |
| ts4-ts-route-plan-service-request-abort-nhkd5p | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-travel2-service|ts-voucher-service | request-abort | ts-route-plan-service |
| ts4-ts-route-plan-service-request-delay-dp6npb | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-payment-service|ts-travel-plan-service|loadgenerator|ts-food-service | request-delay | ts-route-plan-service |
| ts4-ts-route-plan-service-response-replace-body-bfsdhx | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-consign-service|ts-route-service | response-replace-body | ts-route-plan-service |
| ts4-ts-route-plan-service-response-replace-code-fszhvp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-ui-dashboard|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts4-ts-travel-plan-service-request-abort-2gtm6s | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-payment-service|loadgenerator|ts-ui-dashboard|ts-route-service | request-abort | ts-travel-plan-service |
| ts4-ts-travel-service-stress-d9bz8l | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-payment-service|ts-travel-plan-service|loadgenerator|ts-route-plan-service | stress | ts-travel-service |
| ts5-ts-consign-service-stress-g9c5n7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|ts-user-service|ts-train-food-service|ts-assurance-service | stress | ts-consign-service |
| ts5-ts-inside-payment-service-container-kill-bzhplc | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-cancel-service|loadgenerator|ts-order-other-service|ts-assurance-service | container-kill | ts-inside-payment-service |
| ts5-ts-inside-payment-service-stress-tbb7h6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-payment-service|loadgenerator|ts-contacts-service|ts-price-service | stress | ts-inside-payment-service |
| ts5-ts-order-other-service-stress-b7fkzf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-route-plan-service|loadgenerator|ts-execute-service|ts-travel-plan-service | stress | ts-order-other-service |
| ts5-ts-order-other-service-stress-kv9nfz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-route-plan-service|ts-travel-plan-service|loadgenerator | stress | ts-order-other-service |
| ts5-ts-seat-service-response-replace-code-q8j5cp | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|loadgenerator | response-replace-code | ts-seat-service |
| ts5-ts-station-service-container-kill-c99ccx | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-cancel-service|loadgenerator|ts-ui-dashboard|ts-route-plan-service | container-kill | ts-station-service |
| ts5-ts-travel-plan-service-container-kill-76w568 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service | ts-travel-plan-service|ts-payment-service|loadgenerator|ts-consign-service|ts-ui-dashboard | container-kill | ts-travel-plan-service |
| ts5-ts-ui-dashboard-response-replace-code-w4qsj2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-service|ts-preserve-service|ts-route-plan-service | response-replace-code | ts-ui-dashboard |
| ts6-mysql-partition-dlhc27 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-payment-service|ts-food-service|ts-cancel-service|ts-route-service | partition | mysql |
| ts6-ts-order-other-service-container-kill-8gfz95 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|loadgenerator|ts-travel-plan-service|ts-preserve-service | container-kill | ts-order-other-service |
| ts6-ts-station-service-stress-wl6rqj | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-payment-service|ts-route-plan-service|loadgenerator|ts-travel-plan-service | stress | ts-station-service |
| ts7-ts-assurance-service-stress-lth6xq | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|ts-voucher-service|loadgenerator|ts-station-food-service | stress | ts-assurance-service |
| ts7-ts-basic-service-request-replace-method-6c2n7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-preserve-service|ts-travel-plan-service|ts-payment-service|loadgenerator | request-replace-method | ts-basic-service |
| ts8-ts-assurance-service-stress-pknkfc | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|ts-price-service|loadgenerator|ts-train-service | stress | ts-assurance-service |
| ts8-ts-food-service-pod-failure-9swgtb | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-contacts-service|ts-order-service|ts-station-service|loadgenerator | pod-failure | ts-food-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
