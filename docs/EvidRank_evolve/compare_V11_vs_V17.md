# EvidenceRank Compare V11 vs V17

- Created: 2026-06-02T18:54:52+08:00
- Old: `V11`
- New: `V17`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.563291 | -0.239100 |
| AC@3 | 0.943741 | 0.868495 | -0.075246 |
| AC@5 | 0.975387 | 0.939522 | -0.035865 |
| MRR | 0.875337 | 0.724849 | -0.150488 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 45 |
| rank_improved | 38 |
| rank_regressed | 139 |
| regressed_from_hit1 | 385 |
| unchanged | 815 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-travel-service-pod-failure-cvrncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-ui-dashboard | pod-failure | ts-travel-service |
| ts2-mysql-bandwidth-bbk2d4 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-travel-plan-service|loadgenerator | bandwidth | mysql |
| ts2-ts-route-plan-service-request-abort-l264j8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service|loadgenerator | request-abort | ts-route-plan-service |
| ts3-ts-travel-plan-service-request-delay-kxhn5n | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|loadgenerator|ts-ui-dashboard|ts-route-service|ts-route-plan-service | request-delay | ts-travel-plan-service |
| ts4-ts-assurance-service-container-kill-bsv8nk | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|ts-station-food-service|loadgenerator|ts-ui-dashboard | container-kill | ts-assurance-service |
| ts4-ts-basic-service-request-delay-jshmsn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | request-delay | ts-basic-service |
| ts4-ts-consign-service-stress-rw9qhw | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|loadgenerator|ts-station-food-service|ts-ui-dashboard | stress | ts-consign-service |
| ts4-ts-order-other-service-stress-tm48k8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-ui-dashboard|ts-security-service|ts-travel2-service | stress | ts-order-other-service |
| ts4-ts-route-plan-service-corrupt-kw4rss | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel2-service | corrupt | ts-route-plan-service |
| ts4-ts-route-plan-service-request-abort-nhkd5p | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-station-service|ts-security-service | request-abort | ts-route-plan-service |
| ts4-ts-route-plan-service-response-replace-code-fszhvp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-contacts-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts4-ts-seat-service-corrupt-d8skmr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-auth-service | corrupt | ts-seat-service |
| ts4-ts-seat-service-request-replace-method-9wfmmb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | request-replace-method | ts-seat-service |
| ts4-ts-travel-service-stress-d9bz8l | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-payment-service|ts-consign-price-service|ts-order-other-service|ts-inside-payment-service | stress | ts-travel-service |
| ts4-ts-travel-service-stress-fz5lbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-cancel-service|loadgenerator|ts-route-plan-service|rabbitmq | stress | ts-travel-service |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|loadgenerator|ts-ui-dashboard|ts-basic-service|ts-order-service | corrupt | ts-verification-code-service |
| ts5-ts-basic-service-request-replace-method-j4nzcx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-consign-price-service|loadgenerator|ts-route-plan-service|ts-price-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-fqg54d | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-station-service|ts-order-service|ts-travel2-service|loadgenerator | response-replace-code | ts-basic-service |
| ts5-ts-consign-service-stress-g9c5n7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|ts-contacts-service|loadgenerator|ts-route-plan-service | stress | ts-consign-service |
| ts5-ts-inside-payment-service-container-kill-bzhplc | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-cancel-service|loadgenerator|ts-consign-price-service|ts-ui-dashboard | container-kill | ts-inside-payment-service |
| ts5-ts-order-other-service-stress-6wvd48 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-travel2-service|loadgenerator|ts-consign-price-service | stress | ts-order-other-service |
| ts5-ts-order-other-service-stress-b7fkzf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-security-service|ts-config-service|ts-seat-service | stress | ts-order-other-service |
| ts5-ts-order-other-service-stress-kv9nfz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-rebook-service|ts-ticket-office-service|ts-ui-dashboard | stress | ts-order-other-service |
| ts5-ts-order-service-partition-x8xglz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel-service|ts-travel-plan-service|loadgenerator | partition | ts-order-service |
| ts5-ts-station-service-container-kill-c99ccx | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-cancel-service|ts-consign-price-service|ts-inside-payment-service|loadgenerator | container-kill | ts-station-service |
| ts6-mysql-partition-dlhc27 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-payment-service|ts-route-service|ts-travel-service|ts-food-service | partition | mysql |
| ts6-ts-order-other-service-container-kill-8gfz95 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-preserve-service|ts-security-service|ts-inside-payment-service | container-kill | ts-order-other-service |
| ts6-ts-travel2-service-request-delay-bnhhtc | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-order-other-service|ts-travel-plan-service|ts-cancel-service | request-delay | ts-travel2-service |
| ts7-ts-assurance-service-stress-lth6xq | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|loadgenerator|ts-station-food-service|ts-order-other-service | stress | ts-assurance-service |
| ts7-ts-basic-service-request-delay-pgvrbg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-cancel-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service | request-delay | ts-basic-service |
| ts8-ts-assurance-service-stress-pknkfc | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|ts-price-service|ts-cancel-service|ts-inside-payment-service | stress | ts-assurance-service |
| ts8-ts-food-service-pod-failure-9swgtb | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-station-service|ts-order-service|loadgenerator|ts-price-service | pod-failure | ts-food-service |
| ts8-ts-food-service-response-replace-code-lsl65n | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-order-service | response-replace-code | ts-food-service |
| ts0-ts-basic-service-request-abort-62vtm2 | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-station-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 3 | 1 | 2.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-preserve-service | pod-failure | ts-user-service |
| ts1-ts-basic-service-request-abort-snb6ck | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-route-plan-service|ts-train-service | request-abort | ts-basic-service |
| ts2-ts-basic-service-response-abort-jl47fg | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-travel-plan-service|ts-route-service | response-abort | ts-basic-service |
| ts2-ts-travel-service-bandwidth-f9fkg7 | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-ui-dashboard | bandwidth | ts-travel-service |
| ts4-ts-route-plan-service-response-delay-vxcl8q | improved_to_hit1 | 3 | 1 | 2.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-assurance-service|ts-payment-service|ts-preserve-service|loadgenerator | response-delay | ts-route-plan-service |
| ts5-ts-order-other-service-container-kill-p8t6kq | improved_to_hit1 | 3 | 1 | 2.0 | ts-order-other-service | ts-order-other-service|ts-payment-service|ts-execute-service|ts-cancel-service|ts-travel-plan-service | container-kill | ts-order-other-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
