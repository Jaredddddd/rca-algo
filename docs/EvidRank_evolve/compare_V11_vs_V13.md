# EvidenceRank Compare V11 vs V13

- Created: 2026-06-02T18:11:00+08:00
- Old: `V11`
- New: `V13`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.679325 | -0.123066 |
| AC@3 | 0.943741 | 0.926864 | -0.016878 |
| AC@5 | 0.975387 | 0.966245 | -0.009142 |
| MRR | 0.875337 | 0.804981 | -0.070356 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 63 |
| rank_improved | 44 |
| rank_regressed | 82 |
| regressed_from_hit1 | 238 |
| unchanged | 995 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-ui-dashboard-response-replace-code-69j7gg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-basic-service|loadgenerator|ts-seat-service|ts-route-plan-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-route-plan-service-request-abort-l264j8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service|loadgenerator | request-abort | ts-route-plan-service |
| ts2-ts-ui-dashboard-response-replace-code-ms2qf9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|loadgenerator|ts-config-service|ts-basic-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-hh8qpt | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|ts-cancel-service|ts-order-service|loadgenerator|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-rp5xrr | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-travel-service|ts-user-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-replace-code-p9767j | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|ts-payment-service|ts-seat-service|ts-inside-payment-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-assurance-service-container-kill-bsv8nk | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|ts-station-food-service|ts-ui-dashboard|loadgenerator | container-kill | ts-assurance-service |
| ts4-ts-basic-service-request-delay-jshmsn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-route-plan-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service | request-delay | ts-basic-service |
| ts4-ts-consign-service-stress-rw9qhw | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|ts-ui-dashboard|ts-station-food-service|ts-seat-service | stress | ts-consign-service |
| ts4-ts-inside-payment-service-stress-gc2kcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-payment-service|ts-food-service|loadgenerator|ts-ui-dashboard | stress | ts-inside-payment-service |
| ts4-ts-order-other-service-stress-h7rsps | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-security-service|ts-execute-service|ts-route-plan-service|ts-travel-service | stress | ts-order-other-service |
| ts4-ts-order-other-service-stress-tm48k8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-travel2-service|ts-ui-dashboard|ts-security-service | stress | ts-order-other-service |
| ts4-ts-route-plan-service-corrupt-kw4rss | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-seat-service|ts-basic-service | corrupt | ts-route-plan-service |
| ts4-ts-route-plan-service-request-delay-dp6npb | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-payment-service|ts-travel-plan-service|ts-assurance-service|ts-food-service | request-delay | ts-route-plan-service |
| ts4-ts-route-plan-service-response-replace-body-bfsdhx | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-ui-dashboard|ts-consign-service | response-replace-body | ts-route-plan-service |
| ts4-ts-seat-service-corrupt-d8skmr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-basic-service | corrupt | ts-seat-service |
| ts4-ts-seat-service-request-replace-method-9wfmmb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-seat-service |
| ts4-ts-travel-plan-service-request-abort-2gtm6s | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-payment-service|ts-preserve-service|ts-assurance-service|ts-inside-payment-service | request-abort | ts-travel-plan-service |
| ts4-ts-travel-service-stress-d9bz8l | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-order-other-service | stress | ts-travel-service |
| ts4-ts-travel-service-stress-fz5lbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-cancel-service|ts-ui-dashboard|ts-route-plan-service|loadgenerator | stress | ts-travel-service |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-seat-service | corrupt | ts-verification-code-service |
| ts5-ts-basic-service-container-kill-hmkst8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service | ts-basic-service|ts-payment-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard | container-kill | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-j4nzcx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-route-plan-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-fqg54d | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-travel-plan-service|ts-order-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-n7djz7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-route-plan-service|ts-preserve-service|ts-food-service|ts-travel-service | response-replace-code | ts-basic-service |
| ts5-ts-consign-service-stress-g9c5n7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|ts-contacts-service|ts-travel2-service|ts-order-other-service | stress | ts-consign-service |
| ts5-ts-inside-payment-service-container-kill-bzhplc | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-cancel-service|ts-ui-dashboard|loadgenerator|ts-seat-service | container-kill | ts-inside-payment-service |
| ts5-ts-order-other-service-stress-b7fkzf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-security-service|ts-seat-service|ts-order-service | stress | ts-order-other-service |
| ts5-ts-order-other-service-stress-kv9nfz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-travel2-service|ts-preserve-service|ts-rebook-service | stress | ts-order-other-service |
| ts5-ts-order-service-corrupt-bd4p5g | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-assurance-service|ts-consign-price-service|ts-station-food-service | corrupt | ts-order-service |
| ts5-ts-order-service-partition-x8xglz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | partition | ts-order-service |
| ts5-ts-station-service-container-kill-c99ccx | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-cancel-service|ts-ui-dashboard|ts-travel2-service|ts-consign-price-service | container-kill | ts-station-service |
| ts5-ts-ui-dashboard-request-replace-method-dd2fll | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-ui-dashboard | ts-contacts-service|loadgenerator|ts-verification-code-service|ts-travel2-service|ts-ui-dashboard | request-replace-method | ts-ui-dashboard |
| ts5-ts-ui-dashboard-response-replace-code-fvp5cd | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|loadgenerator|ts-preserve-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts6-mysql-partition-dlhc27 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-payment-service|ts-route-service|ts-travel-service|ts-food-service | partition | mysql |
| ts6-ts-basic-service-corrupt-zg68ql | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-travel-plan-service | corrupt | ts-basic-service |
| ts6-ts-order-other-service-container-kill-8gfz95 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-preserve-service|ts-security-service|ts-ui-dashboard | container-kill | ts-order-other-service |
| ts6-ts-station-service-stress-wl6rqj | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-payment-service|ts-basic-service|ts-travel-plan-service|ts-route-plan-service | stress | ts-station-service |
| ts7-ts-assurance-service-stress-lth6xq | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|loadgenerator|ts-order-service|ts-station-food-service | stress | ts-assurance-service |
| ts7-ts-basic-service-request-delay-pgvrbg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-cancel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | request-delay | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
