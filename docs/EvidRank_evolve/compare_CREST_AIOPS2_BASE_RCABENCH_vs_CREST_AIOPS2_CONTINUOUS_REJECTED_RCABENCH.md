# EvidenceRank Compare CREST_AIOPS2_BASE_RCABENCH vs CREST_AIOPS2_CONTINUOUS_REJECTED_RCABENCH

- Created: 2026-06-08T21:29:43+08:00
- Old: `CREST_AIOPS2_BASE_RCABENCH`
- New: `CREST_AIOPS2_CONTINUOUS_REJECTED_RCABENCH`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.801688 | 0.797468 | -0.004219 |
| AC@3 | 0.944444 | 0.943741 | -0.000703 |
| AC@5 | 0.971871 | 0.972574 | 0.000703 |
| MRR | 0.876029 | 0.873281 | -0.002747 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 3 |
| rank_improved | 9 |
| rank_regressed | 14 |
| regressed_from_hit1 | 9 |
| unchanged | 1387 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-auth-service | pod-failure | ts-user-service |
| ts4-ts-config-service-stress-wfgt8h | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-route-plan-service|ts-travel2-service|ts-seat-service|ts-basic-service | stress | ts-config-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-payment-service|ts-travel2-service | pod-failure | ts-route-plan-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | rank_improved | 3 | 2 | 1.0 | ts-station-food-service | ts-food-service|ts-station-food-service|ts-travel-service|ts-basic-service|ts-order-other-service | pod-failure | ts-station-food-service |
| ts3-ts-basic-service-partition-w5hbjw | rank_improved | 10 | 9 | 1.0 | ts-basic-service;ts-travel-service | ts-ui-dashboard|ts-food-service|loadgenerator|ts-consign-service|ts-preserve-service | partition | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | rank_improved | 9 | 8 | 1.0 | ts-route-plan-service;ts-travel-service | ts-ui-dashboard|loadgenerator|ts-food-service|ts-travel-plan-service|ts-seat-service | bandwidth | ts-route-plan-service |
| ts4-ts-station-service-bandwidth-nfljv5 | rank_improved | 17 | 16 | 1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-ui-dashboard | bandwidth | ts-station-service |
| ts5-ts-basic-service-request-replace-method-m559vq | rank_improved | 6 | 5 | 1.0 | ts-basic-service;ts-route-service | ts-route-plan-service|ts-travel2-service|ts-travel-service|ts-inside-payment-service|ts-basic-service | request-replace-method | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | rank_improved | 20 | 18 | 2.0 | ts-cancel-service | ts-consign-service|ts-food-service|ts-basic-service|loadgenerator|ts-station-service | stress | ts-cancel-service |
| ts2-mysql-pod-kill-xvzmxb | rank_improved | 15 | 11 | 4.0 | mysql | ts-order-service|ts-auth-service|ts-security-service|ts-preserve-service|ts-travel-service | unknown | unknown |
| ts3-ts-consign-service-pod-failure-8cb7mp | rank_improved | 17 | 12 | 5.0 | ts-consign-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-food-service|ts-seat-service | pod-failure | ts-consign-service |
| ts0-mysql-container-kill-9t6n24 | rank_improved | 15 | 6 | 9.0 | mysql | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|ts-food-service | container-kill | mysql |
| ts3-ts-basic-service-response-replace-code-ws6vpb | rank_regressed | 7 | 9 | -2.0 | ts-basic-service;ts-station-service | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts4-ts-ui-dashboard-response-replace-code-wdt6z5 | rank_regressed | 2 | 4 | -2.0 | ts-preserve-service;ts-ui-dashboard | ts-consign-service|ts-seat-service|ts-food-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-ui-dashboard |
| ts2-mysql-corrupt-lt5n6d | rank_regressed | 2 | 3 | -1.0 | mysql;ts-contacts-service | ts-auth-service|ts-ui-dashboard|ts-contacts-service|ts-preserve-service|ts-basic-service | corrupt | mysql |
| ts4-mysql-corrupt-kgjmhg | rank_regressed | 2 | 3 | -1.0 | mysql;ts-train-service | ts-route-plan-service|ts-travel-plan-service|ts-train-service|ts-travel-service|ts-basic-service | corrupt | mysql |
| ts4-ts-basic-service-request-replace-method-hpv2qg | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-price-service | ts-route-plan-service|ts-payment-service|ts-basic-service|ts-consign-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | rank_regressed | 9 | 10 | -1.0 | ts-basic-service;ts-price-service | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-hvsqnm | rank_regressed | 6 | 7 | -1.0 | ts-basic-service;ts-route-service | ts-preserve-service|ts-travel2-service|ts-security-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | rank_regressed | 14 | 15 | -1.0 | ts-route-plan-service;ts-travel-plan-service | ts-auth-service|ts-ui-dashboard|ts-seat-service|ts-preserve-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-order-service-partition-z2d6nw | rank_regressed | 2 | 3 | -1.0 | ts-order-service;ts-ui-dashboard | ts-order-other-service|ts-security-service|ts-ui-dashboard|ts-food-service|ts-seat-service | partition | ts-order-service |
| ts5-ts-route-plan-service-response-delay-vjgk5j | rank_regressed | 2 | 3 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-consign-price-service|ts-route-plan-service|ts-contacts-service|ts-order-service | response-delay | ts-route-plan-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | rank_regressed | 4 | 5 | -1.0 | ts-route-plan-service;ts-travel-plan-service | ts-preserve-service|ts-ui-dashboard|ts-consign-price-service|ts-travel2-service|ts-travel-plan-service | response-replace-code | ts-travel-plan-service |
| ts5-ts-travel-service-response-patch-body-nt8z6r | rank_regressed | 4 | 5 | -1.0 | ts-basic-service;ts-travel-service | ts-assurance-service|ts-route-plan-service|ts-travel-plan-service|ts-order-service|ts-travel-service | unknown | unknown |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | rank_regressed | 9 | 10 | -1.0 | ts-basic-service;ts-travel2-service | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-preserve-service|ts-ui-dashboard | response-replace-code | ts-travel2-service |
| ts6-ts-preserve-service-partition-jvzrwx | rank_regressed | 6 | 7 | -1.0 | ts-preserve-service;ts-ui-dashboard | ts-food-service|ts-basic-service|ts-assurance-service|ts-seat-service|ts-order-service | partition | ts-preserve-service |
| ts0-mysql-partition-mphlhs | regressed_from_hit1 | 1 | 2 | -1.0 | mysql;ts-security-service | ts-preserve-service|ts-security-service|ts-ui-dashboard|ts-travel2-service|ts-assurance-service | partition | mysql |
| ts0-ts-basic-service-request-replace-method-z2nlcm | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-basic-service|ts-station-service|ts-travel2-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-pqlzs2 | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-station-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts2-mysql-loss-4fvjb6 | regressed_from_hit1 | 1 | 2 | -1.0 | mysql;ts-order-other-service | ts-preserve-service|ts-order-other-service|ts-security-service|ts-travel2-service|ts-seat-service | loss | mysql |
| ts3-mysql-corrupt-wgvhdb | regressed_from_hit1 | 1 | 2 | -1.0 | mysql;ts-config-service | ts-seat-service|ts-config-service|ts-travel2-service|ts-route-service|ts-travel-service | corrupt | mysql |
| ts3-ts-user-service-partition-vt7q2n | regressed_from_hit1 | 1 | 2 | -1.0 | mysql;ts-user-service | ts-verification-code-service|ts-user-service|ts-auth-service|ts-ui-dashboard|ts-order-other-service | partition | ts-user-service |
| ts4-ts-basic-service-response-delay-slw7f4 | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-station-service | ts-seat-service|ts-basic-service|ts-route-plan-service|ts-travel-service|ts-preserve-service | response-delay | ts-basic-service |
| ts4-ts-route-plan-service-request-replace-path-fmj8lq | regressed_from_hit1 | 1 | 2 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-seat-service|ts-order-service|ts-travel2-service | request-replace-path | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-7dhcgm | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-train-service | ts-consign-service|ts-basic-service|ts-seat-service|ts-travel-service|ts-train-service | request-replace-method | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
