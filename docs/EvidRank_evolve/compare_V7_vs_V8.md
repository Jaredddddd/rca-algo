# EvidenceRank Compare V7 vs V8

- Created: 2026-06-02T03:53:57+08:00
- Old: `V7`
- New: `V8`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.781997 | 0.788326 | 0.006329 |
| AC@3 | 0.940928 | 0.939522 | -0.001406 |
| AC@5 | 0.978903 | 0.973980 | -0.004923 |
| MRR | 0.864359 | 0.866904 | 0.002546 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 16 |
| rank_improved | 20 |
| rank_regressed | 25 |
| regressed_from_hit1 | 7 |
| unchanged | 1354 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts2-ts-consign-price-service-container-kill-lj9llf | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-seat-service|ts-ui-dashboard|ts-order-service | container-kill | ts-consign-price-service |
| ts2-ts-ui-dashboard-response-replace-code-bzfxkt | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|loadgenerator|ts-basic-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts3-mysql-bandwidth-kpqsfl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-ui-dashboard|loadgenerator|ts-route-plan-service|ts-order-service | bandwidth | mysql |
| ts3-ts-travel-plan-service-request-delay-kxhn5n | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-order-service | request-delay | ts-travel-plan-service |
| ts4-ts-basic-service-corrupt-trd2kh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-travel2-service|ts-seat-service | corrupt | ts-basic-service |
| ts4-ts-basic-service-request-delay-jshmsn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-order-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-response-delay-hmp7h5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-preserve-service|ts-seat-service | response-delay | ts-basic-service |
| ts4-ts-seat-service-corrupt-d8skmr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-basic-service|ts-auth-service | corrupt | ts-seat-service |
| ts4-ts-seat-service-response-delay-46hcdn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel2-service|ts-consign-price-service | response-delay | ts-seat-service |
| ts4-ts-security-service-corrupt-9lndmd | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-seat-service | corrupt | ts-security-service |
| ts4-ts-security-service-corrupt-rq5cgb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-ui-dashboard|ts-preserve-service|ts-seat-service|ts-travel-service | corrupt | ts-security-service |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-basic-service | corrupt | ts-verification-code-service |
| ts5-mysql-loss-q42phw | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-order-service|ts-travel-plan-service|ts-travel-service | loss | mysql |
| ts5-ts-contacts-service-corrupt-jwgz8t | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service|ts-basic-service | corrupt | ts-contacts-service |
| ts5-ts-travel-service-loss-bcmp2f | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel-service|ts-order-service | loss | ts-travel-service |
| ts6-ts-travel2-service-request-delay-bnhhtc | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-basic-service|ts-seat-service|ts-travel-service | request-delay | ts-travel2-service |
| ts0-mysql-container-kill-9t6n24 | rank_improved | 8 | 7 | 1.0 | mysql | ts-train-service|ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts1-ts-station-food-service-pod-failure-td2qj4 | rank_improved | 3 | 2 | 1.0 | ts-station-food-service | ts-food-service|ts-station-food-service|ts-travel-service|ts-basic-service|ts-order-other-service | pod-failure | ts-station-food-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | rank_improved | 7 | 6 | 1.0 | ts-assurance-service | ts-basic-service|ts-route-plan-service|ts-travel-service|ts-seat-service|ts-station-service | pod-failure | ts-assurance-service |
| ts2-ts-consign-price-service-stress-7r95bt | rank_improved | 6 | 5 | 1.0 | ts-consign-price-service | ts-payment-service|ts-consign-service|ts-preserve-service|ts-security-service|ts-consign-price-service | stress | ts-consign-price-service |
| ts3-ts-auth-service-return-9tmvzg | rank_improved | 4 | 3 | 1.0 | ts-auth-service | ts-verification-code-service|ts-ui-dashboard|ts-auth-service|loadgenerator|ts-travel-service | return | ts-auth-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | rank_improved | 3 | 2 | 1.0 | ts-consign-service | ts-travel-service|ts-consign-service|ts-basic-service|ts-seat-service|ts-order-other-service | pod-failure | ts-consign-service |
| ts4-ts-basic-service-request-delay-jkxt8v | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-route-service | ts-preserve-service|ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-seat-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-7tlb8z | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-price-service | ts-route-plan-service|ts-travel2-service|ts-basic-service|ts-travel-plan-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-response-delay-vxcl8q | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-payment-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-order-service | response-delay | ts-route-plan-service |
| ts5-ts-basic-service-response-abort-7f8qrl | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-price-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-consign-service|ts-travel2-service | response-abort | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | rank_improved | 15 | 14 | 1.0 | ts-cancel-service | ts-consign-service|ts-food-service|ts-route-plan-service|ts-auth-service|ts-basic-service | stress | ts-cancel-service |
| ts5-ts-route-plan-service-request-replace-method-hvvmmj | rank_improved | 4 | 3 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-station-service|loadgenerator | request-replace-method | ts-route-plan-service |
| ts5-ts-route-plan-service-request-replace-method-v76qjz | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-route-service | ts-travel-plan-service|ts-route-plan-service|ts-basic-service|ts-ui-dashboard|ts-seat-service | request-replace-method | ts-route-plan-service |
| ts5-ts-route-plan-service-response-delay-vjgk5j | rank_improved | 5 | 4 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-consign-price-service|ts-contacts-service|ts-order-service|ts-route-plan-service|ts-travel-plan-service | response-delay | ts-route-plan-service |
| ts5-ts-travel-service-response-delay-9x42gg | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-travel-service | ts-payment-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service | response-delay | ts-travel-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | rank_improved | 11 | 10 | 1.0 | ts-route-plan-service;ts-travel-service | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel-plan-service | response-replace-body | ts-route-plan-service |
| ts4-ts-basic-service-request-replace-method-hpv2qg | rank_improved | 5 | 3 | 2.0 | ts-basic-service;ts-price-service | ts-seat-service|ts-travel2-service|ts-basic-service|ts-order-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts4-ts-seat-service-bandwidth-k2bwt2 | rank_improved | 8 | 6 | 2.0 | ts-config-service;ts-seat-service | ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|loadgenerator|ts-route-plan-service | bandwidth | ts-seat-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | rank_improved | 12 | 9 | 3.0 | ts-basic-service;ts-price-service | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | response-replace-body | ts-basic-service |
| ts8-ts-food-service-pod-failure-9swgtb | rank_improved | 5 | 2 | 3.0 | ts-food-service | ts-order-service|ts-food-service|ts-seat-service|ts-ui-dashboard|ts-basic-service | pod-failure | ts-food-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | rank_regressed | 3 | 10 | -7.0 | ts-assurance-service;ts-ui-dashboard | ts-basic-service|ts-consign-service|ts-seat-service|ts-auth-service|ts-train-service | request-replace-method | ts-ui-dashboard |
| ts6-ts-basic-service-request-replace-method-4qzglm | rank_regressed | 4 | 10 | -6.0 | ts-basic-service;ts-train-service | ts-cancel-service|ts-verification-code-service|ts-consign-service|ts-route-service|ts-travel-service | request-replace-method | ts-basic-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | rank_regressed | 5 | 9 | -4.0 | ts-food-service;ts-ui-dashboard | ts-order-service|ts-seat-service|loadgenerator|ts-basic-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | rank_regressed | 7 | 11 | -4.0 | ts-route-plan-service;ts-travel-service | ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-basic-service|ts-seat-service | bandwidth | ts-route-plan-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
