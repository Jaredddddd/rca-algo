# EvidenceRank Compare V11 vs V14

- Created: 2026-06-02T18:22:01+08:00
- Old: `V11`
- New: `V14`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.657525 | -0.144866 |
| AC@3 | 0.943741 | 0.914205 | -0.029536 |
| AC@5 | 0.975387 | 0.962025 | -0.013361 |
| MRR | 0.875337 | 0.791101 | -0.084236 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 66 |
| rank_improved | 46 |
| rank_regressed | 89 |
| regressed_from_hit1 | 272 |
| unchanged | 949 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-travel-service-pod-failure-cvrncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-food-service | pod-failure | ts-travel-service |
| ts0-ts-ui-dashboard-response-replace-code-69j7gg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-security-service|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts1-ts-ui-dashboard-request-abort-cr4wzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-station-service|ts-auth-service|ts-price-service | request-abort | ts-ui-dashboard |
| ts2-mysql-bandwidth-bbk2d4 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service | bandwidth | mysql |
| ts2-ts-route-plan-service-request-abort-l264j8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service|ts-order-service | request-abort | ts-route-plan-service |
| ts3-ts-ui-dashboard-request-replace-method-hh8qpt | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|ts-cancel-service|ts-order-service|loadgenerator|ts-consign-price-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-rp5xrr | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|ts-auth-service|loadgenerator|ts-travel-service|ts-verification-code-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-wkh6t7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-order-service|ts-verification-code-service|ts-seat-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-replace-code-p9767j | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-consign-service|ts-ui-dashboard|ts-payment-service|ts-seat-service|ts-inside-payment-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-assurance-service-container-kill-bsv8nk | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|ts-station-food-service|ts-ui-dashboard|ts-travel-plan-service | container-kill | ts-assurance-service |
| ts4-ts-basic-service-request-delay-jshmsn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service | request-delay | ts-basic-service |
| ts4-ts-consign-service-stress-rw9qhw | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|ts-ui-dashboard|ts-seat-service|ts-station-food-service | stress | ts-consign-service |
| ts4-ts-order-other-service-stress-h7rsps | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-security-service|ts-travel-service|ts-route-plan-service | stress | ts-order-other-service |
| ts4-ts-order-other-service-stress-tm48k8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-seat-service|ts-order-service|ts-travel2-service | stress | ts-order-other-service |
| ts4-ts-route-plan-service-corrupt-kw4rss | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-basic-service|loadgenerator | corrupt | ts-route-plan-service |
| ts4-ts-route-plan-service-response-replace-body-bfsdhx | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|loadgenerator|ts-consign-service | response-replace-body | ts-route-plan-service |
| ts4-ts-route-plan-service-response-replace-code-fszhvp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-verification-code-service|ts-order-service | response-replace-code | ts-route-plan-service |
| ts4-ts-seat-service-corrupt-d8skmr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-order-service|ts-auth-service | corrupt | ts-seat-service |
| ts4-ts-seat-service-request-replace-method-9wfmmb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-seat-service |
| ts4-ts-travel-plan-service-request-abort-2gtm6s | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-payment-service|ts-preserve-service|ts-inside-payment-service|ts-assurance-service | request-abort | ts-travel-plan-service |
| ts4-ts-travel-plan-service-request-replace-method-cl8lsl | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|loadgenerator|ts-inside-payment-service | request-replace-method | ts-travel-plan-service |
| ts4-ts-travel-service-stress-d9bz8l | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-order-service | stress | ts-travel-service |
| ts4-ts-travel-service-stress-fz5lbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-cancel-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service | stress | ts-travel-service |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-seat-service|ts-basic-service | corrupt | ts-verification-code-service |
| ts5-ts-basic-service-container-kill-hmkst8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service | ts-basic-service|ts-payment-service|ts-route-plan-service|ts-ui-dashboard|ts-seat-service | container-kill | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-j4nzcx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-seat-service|ts-consign-price-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-fqg54d | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-order-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-n7djz7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-seat-service|ts-route-plan-service|ts-food-service | response-replace-code | ts-basic-service |
| ts5-ts-consign-service-stress-g9c5n7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|ts-seat-service|ts-contacts-service|ts-travel2-service | stress | ts-consign-service |
| ts5-ts-inside-payment-service-container-kill-bzhplc | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-cancel-service|ts-ui-dashboard|ts-seat-service|loadgenerator | container-kill | ts-inside-payment-service |
| ts5-ts-order-other-service-stress-6wvd48 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-execute-service | stress | ts-order-other-service |
| ts5-ts-order-other-service-stress-b7fkzf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-seat-service|ts-security-service|ts-order-service | stress | ts-order-other-service |
| ts5-ts-order-other-service-stress-kv9nfz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-rebook-service|ts-travel2-service|ts-preserve-service | stress | ts-order-other-service |
| ts5-ts-order-service-partition-x8xglz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | partition | ts-order-service |
| ts5-ts-station-service-container-kill-c99ccx | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-cancel-service|ts-ui-dashboard|ts-consign-price-service|ts-inside-payment-service | container-kill | ts-station-service |
| ts5-ts-ui-dashboard-request-replace-method-dd2fll | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-ui-dashboard | ts-contacts-service|loadgenerator|ts-verification-code-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-ui-dashboard-response-replace-code-fvp5cd | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|ts-seat-service|ts-preserve-service|ts-verification-code-service | response-replace-code | ts-ui-dashboard |
| ts6-mysql-partition-dlhc27 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-payment-service|ts-ui-dashboard|ts-route-service|ts-travel-service | partition | mysql |
| ts6-ts-basic-service-corrupt-zg68ql | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-travel-plan-service | corrupt | ts-basic-service |
| ts6-ts-order-other-service-container-kill-8gfz95 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-preserve-service|ts-seat-service|ts-security-service | container-kill | ts-order-other-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
