# EvidenceRank Compare V13_REIMPL_V2 vs V13_REIMPL_V3_NO_TOPO

- Created: 2026-06-03T12:32:37+08:00
- Old: `V13_REIMPL_V2`
- New: `V13_REIMPL_V3_NO_TOPO`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.670886 | 0.649086 | -0.021800 |
| AC@3 | 0.925457 | 0.914909 | -0.010549 |
| AC@5 | 0.973980 | 0.966245 | -0.007736 |
| MRR | 0.801983 | 0.786477 | -0.015506 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 21 |
| rank_improved | 32 |
| rank_regressed | 89 |
| regressed_from_hit1 | 52 |
| unchanged | 1228 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts1-ts-auth-service-request-replace-method-mrrl9f | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-verification-code-service|ts-ui-dashboard|ts-auth-service|loadgenerator|ts-order-other-service | request-replace-method | ts-auth-service |
| ts1-ts-preserve-service-response-replace-code-b7m2g5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|loadgenerator|ts-food-service | response-replace-code | ts-preserve-service |
| ts1-ts-security-service-request-replace-method-xv2ncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-delivery-service|ts-order-service | request-replace-method | ts-security-service |
| ts1-ts-station-service-stress-jzbbjv | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-travel-service | stress | ts-station-service |
| ts1-ts-travel-plan-service-request-replace-method-d2pqdm | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-station-service|ts-travel2-service|loadgenerator | request-replace-method | ts-travel-plan-service |
| ts1-ts-travel-plan-service-request-replace-path-zdh4tb | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-price-service|ts-travel2-service|ts-assurance-service | request-replace-path | ts-travel-plan-service |
| ts1-ts-travel-plan-service-response-delay-zhj7r7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-service|ts-basic-service | response-delay | ts-travel-plan-service |
| ts2-mysql-corrupt-lt5n6d | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-ui-dashboard|ts-preserve-service|ts-auth-service|ts-seat-service | corrupt | mysql |
| ts2-mysql-delay-d427wn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel-service | delay | mysql |
| ts2-ts-auth-service-loss-5k6gqr | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-auth-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-order-service | loss | ts-auth-service |
| ts2-ts-basic-service-request-replace-method-v6gzn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-station-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts2-ts-station-service-stress-mzxgqn | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-travel-plan-service | stress | ts-station-service |
| ts3-ts-food-service-response-abort-9tjsld | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-travel-service | response-abort | ts-food-service |
| ts3-ts-preserve-service-request-replace-path-9f8dtp | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-security-service | request-replace-path | ts-preserve-service |
| ts3-ts-preserve-service-response-replace-code-dtlxgb | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-security-service|ts-basic-service | response-replace-code | ts-preserve-service |
| ts3-ts-seat-service-request-replace-path-749bws | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-travel-plan-service|ts-route-plan-service | request-replace-path | ts-seat-service |
| ts3-ts-travel-plan-service-response-delay-5nq8mq | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-basic-service | response-delay | ts-travel-plan-service |
| ts4-ts-auth-service-corrupt-pldpdm | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-order-service | corrupt | ts-auth-service |
| ts5-ts-station-service-container-kill-c99ccx | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-cancel-service|ts-ui-dashboard|ts-consign-price-service|ts-inside-payment-service | container-kill | ts-station-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | improved_to_hit1 | 3 | 1 | 2.0 | ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-price-service | pod-failure | ts-travel2-service |
| ts5-ts-order-other-service-stress-6wvd48 | improved_to_hit1 | 3 | 1 | 2.0 | ts-order-other-service | ts-order-other-service|ts-execute-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | stress | ts-order-other-service |
| ts0-ts-station-service-bandwidth-bp5k94 | rank_improved | 6 | 5 | 1.0 | mysql;ts-station-service | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-station-service | bandwidth | ts-station-service |
| ts1-ts-config-service-latency-5kkcrc | rank_improved | 3 | 2 | 1.0 | ts-config-service | ts-consign-service|ts-config-service|ts-ui-dashboard|ts-food-service|ts-basic-service | unknown | unknown |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-contacts-service|ts-train-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-service-corrupt-5z9zfl | rank_improved | 6 | 5 | 1.0 | mysql;ts-route-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-basic-service|ts-route-service | corrupt | ts-route-service |
| ts1-ts-travel2-service-request-replace-method-s99vbn | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard|loadgenerator | request-replace-method | ts-travel2-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-train-service | ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-basic-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts2-ts-route-plan-service-response-replace-body-dghfbk | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|loadgenerator|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | rank_improved | 4 | 3 | 1.0 | ts-travel-service | ts-travel-plan-service|ts-route-plan-service|ts-travel-service|ts-ui-dashboard|loadgenerator | pod-failure | ts-travel-service |
| ts2-ts-travel2-service-response-replace-code-ttpn92 | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard|ts-price-service | response-replace-code | ts-travel2-service |
| ts3-mysql-pod-failure-58qts5 | rank_improved | 31 | 30 | 1.0 | mysql | ts-auth-service|loadgenerator|ts-travel-service|ts-route-plan-service|ts-order-other-service | pod-failure | mysql |
| ts3-ts-basic-service-response-replace-code-ws6vpb | rank_improved | 7 | 6 | 1.0 | ts-basic-service;ts-station-service | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts3-ts-route-plan-service-response-abort-mwz8b5 | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-basic-service|ts-payment-service | response-abort | ts-route-plan-service |
| ts3-ts-route-plan-service-response-replace-code-vqsdbr | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|loadgenerator|ts-basic-service | response-replace-code | ts-route-plan-service |
| ts3-ts-ui-dashboard-request-replace-method-pgl9hb | rank_improved | 4 | 3 | 1.0 | ts-contacts-service;ts-ui-dashboard | ts-station-service|loadgenerator|ts-contacts-service|ts-basic-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-abort-zd59tz | rank_improved | 3 | 2 | 1.0 | ts-assurance-service;ts-ui-dashboard | loadgenerator|ts-assurance-service|ts-order-service|ts-verification-code-service|ts-ui-dashboard | response-abort | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | rank_improved | 8 | 7 | 1.0 | ts-route-plan-service;ts-travel-service | ts-ui-dashboard|loadgenerator|ts-food-service|ts-seat-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts4-ts-route-plan-service-request-replace-method-fd9l64 | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel-service | ts-cancel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|loadgenerator | request-replace-method | ts-route-plan-service |
| ts4-ts-travel-plan-service-request-replace-method-cl8lsl | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-inside-payment-service|ts-travel-plan-service|ts-ui-dashboard|ts-consign-price-service|ts-route-plan-service | request-replace-method | ts-travel-plan-service |
| ts4-ts-travel2-service-response-replace-body-lsqg4p | rank_improved | 5 | 4 | 1.0 | ts-seat-service;ts-travel2-service | ts-cancel-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-body | ts-travel2-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
