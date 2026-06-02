# EvidenceRank Compare V11 vs V15

- Created: 2026-06-02T18:34:01+08:00
- Old: `V11`
- New: `V15`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.638537 | -0.163854 |
| AC@3 | 0.943741 | 0.884669 | -0.059072 |
| AC@5 | 0.975387 | 0.949367 | -0.026020 |
| MRR | 0.875337 | 0.772135 | -0.103202 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 71 |
| rank_improved | 37 |
| rank_regressed | 102 |
| regressed_from_hit1 | 304 |
| unchanged | 908 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-ui-dashboard-response-replace-code-69j7gg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-order-service|ts-travel-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-route-service-corrupt-qlt7gn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|loadgenerator|ts-train-service|ts-auth-service | corrupt | ts-route-service |
| ts2-mysql-bandwidth-bbk2d4 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | bandwidth | mysql |
| ts2-ts-ui-dashboard-request-replace-method-h27hzq | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-food-service|loadgenerator|ts-order-service|ts-ui-dashboard|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts3-mysql-corrupt-wgvhdb | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-route-plan-service|ts-travel2-service|ts-travel-plan-service | corrupt | mysql |
| ts3-ts-ui-dashboard-request-replace-method-hh8qpt | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|ts-order-service|ts-consign-service|ts-cancel-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-rp5xrr | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|ts-auth-service|ts-travel-service|ts-order-other-service|ts-route-plan-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-replace-code-p9767j | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-consign-service|ts-payment-service|ts-ui-dashboard|ts-seat-service|ts-inside-payment-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-assurance-service-container-kill-bsv8nk | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-payment-service|ts-station-food-service|ts-ui-dashboard|loadgenerator | container-kill | ts-assurance-service |
| ts4-ts-basic-service-corrupt-trd2kh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-security-service|ts-order-service | corrupt | ts-basic-service |
| ts4-ts-basic-service-request-delay-jkxt8v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-route-plan-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-request-delay-jshmsn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-route-plan-service|ts-preserve-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-response-delay-76ksjc | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-route-plan-service|ts-travel-service|ts-travel-plan-service|ts-order-other-service | response-delay | ts-basic-service |
| ts4-ts-consign-service-partition-ncb5l8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|ts-order-other-service|ts-payment-service|ts-price-service|ts-travel2-service | partition | ts-consign-service |
| ts4-ts-consign-service-stress-rw9qhw | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|ts-ui-dashboard|ts-station-food-service|ts-seat-service | stress | ts-consign-service |
| ts4-ts-inside-payment-service-stress-gc2kcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-payment-service|ts-food-service|ts-consign-service|ts-ui-dashboard | stress | ts-inside-payment-service |
| ts4-ts-order-other-service-stress-h7rsps | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-travel-service|ts-execute-service|ts-security-service|ts-route-plan-service | stress | ts-order-other-service |
| ts4-ts-order-other-service-stress-tm48k8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-ui-dashboard|ts-travel2-service|ts-order-service | stress | ts-order-other-service |
| ts4-ts-route-plan-service-corrupt-kw4rss | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-order-service | corrupt | ts-route-plan-service |
| ts4-ts-seat-service-request-replace-method-9wfmmb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-seat-service |
| ts4-ts-travel-plan-service-request-abort-2gtm6s | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-payment-service|ts-preserve-service|ts-assurance-service|ts-inside-payment-service | request-abort | ts-travel-plan-service |
| ts4-ts-travel-service-stress-d9bz8l | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-order-service | stress | ts-travel-service |
| ts4-ts-travel-service-stress-fz5lbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-ui-dashboard|ts-cancel-service|ts-route-plan-service|ts-seat-service | stress | ts-travel-service |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-basic-service | corrupt | ts-verification-code-service |
| ts5-mysql-loss-q42phw | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-auth-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-travel-plan-service | loss | mysql |
| ts5-ts-basic-service-request-replace-method-j4nzcx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-route-plan-service|ts-travel2-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-fqg54d | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-order-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-n7djz7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-food-service|ts-order-service | response-replace-code | ts-basic-service |
| ts5-ts-consign-service-stress-g9c5n7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-cancel-service|ts-contacts-service|ts-order-other-service|ts-route-plan-service | stress | ts-consign-service |
| ts5-ts-inside-payment-service-container-kill-bzhplc | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-cancel-service|ts-ui-dashboard|ts-consign-price-service|loadgenerator | container-kill | ts-inside-payment-service |
| ts5-ts-order-other-service-stress-b7fkzf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-security-service|ts-seat-service|ts-order-service | stress | ts-order-other-service |
| ts5-ts-order-other-service-stress-kv9nfz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-travel2-service|ts-rebook-service|ts-preserve-service | stress | ts-order-other-service |
| ts5-ts-order-service-corrupt-bd4p5g | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-assurance-service|ts-order-service|ts-order-other-service|loadgenerator | corrupt | ts-order-service |
| ts5-ts-order-service-partition-x8xglz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | partition | ts-order-service |
| ts5-ts-route-service-corrupt-vvvjts | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-travel-plan-service | corrupt | ts-route-service |
| ts5-ts-station-service-container-kill-c99ccx | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-cancel-service|ts-ui-dashboard|ts-inside-payment-service|ts-consign-price-service | container-kill | ts-station-service |
| ts5-ts-ui-dashboard-request-replace-method-dd2fll | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-ui-dashboard | ts-contacts-service|loadgenerator|ts-verification-code-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-ui-dashboard-response-replace-code-fvp5cd | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-preserve-service|ts-order-service|ts-seat-service|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts6-mysql-partition-dlhc27 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-payment-service|ts-ui-dashboard|ts-route-service|ts-travel-service | partition | mysql |
| ts6-ts-basic-service-corrupt-zg68ql | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | corrupt | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
