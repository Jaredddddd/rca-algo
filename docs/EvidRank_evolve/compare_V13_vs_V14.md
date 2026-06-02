# EvidenceRank Compare V13 vs V14

- Created: 2026-06-02T18:22:01+08:00
- Old: `V13`
- New: `V14`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.679325 | 0.657525 | -0.021800 |
| AC@3 | 0.926864 | 0.914205 | -0.012658 |
| AC@5 | 0.966245 | 0.962025 | -0.004219 |
| MRR | 0.804981 | 0.791101 | -0.013880 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 32 |
| rank_improved | 56 |
| rank_regressed | 100 |
| regressed_from_hit1 | 63 |
| unchanged | 1171 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-travel-service-pod-failure-cvrncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-food-service | pod-failure | ts-travel-service |
| ts0-ts-ui-dashboard-response-delay-n5c9hs | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-order-service|ts-travel-service | response-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-delay-nqtssr | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-assurance-service|ts-verification-code-service|ts-preserve-service | response-delay | ts-ui-dashboard |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-order-other-service|ts-travel-service | pod-failure | ts-user-service |
| ts1-ts-preserve-service-request-abort-x7w9vv | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-station-food-service|ts-contacts-service | request-abort | ts-preserve-service |
| ts1-ts-ui-dashboard-request-abort-cr4wzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-station-service|ts-auth-service|ts-price-service | request-abort | ts-ui-dashboard |
| ts1-ts-ui-dashboard-request-delay-d56qn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-user-service|ts-security-service|ts-food-service | request-delay | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-delay-mhcfcl | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-verification-code-service | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-station-service|ts-order-service | response-delay | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-b2g9ss | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-consign-service|ts-travel-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts2-mysql-bandwidth-bbk2d4 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service | bandwidth | mysql |
| ts2-ts-food-service-response-abort-5k6q44 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-config-service | response-abort | ts-food-service |
| ts2-ts-route-plan-service-return-xw84fv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-consign-service|ts-ui-dashboard|ts-station-food-service|ts-payment-service | return | ts-route-plan-service |
| ts2-ts-ui-dashboard-response-delay-kzbf4x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-travel-service|ts-basic-service|ts-price-service | response-delay | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-mk44qn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-travel-plan-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-qzfj27 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|loadgenerator|ts-route-plan-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-delay-fhl2lp | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | request-delay | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-wkh6t7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-order-service|ts-verification-code-service|ts-seat-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-assurance-service-partition-nj8rh5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-travel-service|ts-consign-price-service | partition | ts-assurance-service |
| ts4-ts-route-plan-service-response-replace-code-fszhvp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-verification-code-service|ts-order-service | response-replace-code | ts-route-plan-service |
| ts4-ts-seat-service-response-delay-46hcdn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-ui-dashboard|ts-food-service|ts-travel2-service | response-delay | ts-seat-service |
| ts4-ts-travel-plan-service-request-replace-method-cl8lsl | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|loadgenerator|ts-inside-payment-service | request-replace-method | ts-travel-plan-service |
| ts5-ts-order-other-service-stress-6wvd48 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-execute-service | stress | ts-order-other-service |
| ts5-ts-preserve-service-request-replace-method-v2qhvn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-seat-service|ts-ui-dashboard|ts-order-service|ts-route-plan-service | request-replace-method | ts-preserve-service |
| ts5-ts-travel-service-stress-p5h56b | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-payment-service|ts-ui-dashboard|ts-travel-plan-service | stress | ts-travel-service |
| ts9-ts-basic-service-response-delay-hfvbg6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-verification-code-service | response-delay | ts-basic-service |
| ts9-ts-preserve-service-pod-failure-6w29wr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service | ts-preserve-service|ts-verification-code-service|loadgenerator|ts-inside-payment-service|ts-order-service | pod-failure | ts-preserve-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | improved_to_hit1 | 3 | 1 | 2.0 | ts-assurance-service | ts-assurance-service|ts-station-service|ts-basic-service|ts-route-plan-service|ts-seat-service | pod-failure | ts-assurance-service |
| ts2-ts-order-other-service-container-kill-48rlds | improved_to_hit1 | 3 | 1 | 2.0 | ts-order-other-service | ts-order-other-service|ts-seat-service|ts-travel2-service|ts-ui-dashboard|ts-basic-service | container-kill | ts-order-other-service |
| ts5-ts-train-food-service-mysql-rswcbh | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-train-food-service | ts-train-food-service|loadgenerator|ts-basic-service|ts-payment-service|ts-cancel-service | unknown | unknown |
| ts3-ts-consign-service-pod-failure-8cb7mp | improved_to_hit1 | 4 | 1 | 3.0 | ts-consign-service | ts-consign-service|ts-basic-service|ts-ui-dashboard|ts-seat-service|ts-travel-service | pod-failure | ts-consign-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | improved_to_hit1 | 4 | 1 | 3.0 | ts-price-service | ts-price-service|ts-consign-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service | pod-failure | ts-price-service |
| ts0-ts-seat-service-pod-failure-c87xdg | improved_to_hit1 | 5 | 1 | 4.0 | ts-seat-service | ts-seat-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service | pod-failure | ts-seat-service |
| ts0-ts-basic-service-pod-failure-94xplz | rank_improved | 4 | 3 | 1.0 | ts-basic-service | ts-travel-service|ts-travel2-service|ts-basic-service|ts-route-plan-service|ts-ui-dashboard | pod-failure | ts-basic-service |
| ts0-ts-basic-service-response-replace-body-2ntz4z | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-preserve-service|ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service | response-replace-body | ts-basic-service |
| ts0-ts-ui-dashboard-request-replace-method-fl9jln | rank_improved | 3 | 2 | 1.0 | ts-ui-dashboard;ts-user-service | ts-assurance-service|ts-ui-dashboard|ts-route-plan-service|ts-user-service|ts-travel-plan-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-basic-service-request-replace-method-v627xx | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | rank_improved | 5 | 4 | 1.0 | ts-food-service;ts-train-food-service | ts-consign-service|ts-order-service|ts-payment-service|ts-food-service|ts-travel-service | unknown | unknown |
| ts1-ts-route-service-corrupt-5z9zfl | rank_improved | 6 | 5 | 1.0 | mysql;ts-route-service | ts-route-plan-service|ts-basic-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-service | corrupt | ts-route-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | rank_improved | 3 | 2 | 1.0 | ts-station-food-service | ts-food-service|ts-station-food-service|ts-travel-service|ts-basic-service|ts-order-other-service | pod-failure | ts-station-food-service |
| ts1-ts-station-service-pod-failure-fn44tf | rank_improved | 3 | 2 | 1.0 | ts-station-service | ts-basic-service|ts-station-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service | pod-failure | ts-station-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
