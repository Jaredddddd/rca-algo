# EvidenceRank Compare V11 vs V20

- Created: 2026-06-02T23:39:26+08:00
- Old: `V11`
- New: `V20`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.789030 | -0.013361 |
| AC@3 | 0.943741 | 0.940225 | -0.003516 |
| AC@5 | 0.975387 | 0.976793 | 0.001406 |
| MRR | 0.875337 | 0.869097 | -0.006240 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 5 |
| rank_improved | 16 |
| rank_regressed | 27 |
| regressed_from_hit1 | 24 |
| unchanged | 1350 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts5-ts-order-service-partition-x8xglz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | partition | ts-order-service |
| ts6-ts-basic-service-corrupt-zg68ql | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-travel2-service|loadgenerator|ts-travel-plan-service | corrupt | ts-basic-service |
| ts8-ts-food-service-pod-failure-9swgtb | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-order-service|ts-ui-dashboard|ts-basic-service|ts-station-service | pod-failure | ts-food-service |
| ts0-ts-seat-service-pod-failure-c87xdg | improved_to_hit1 | 4 | 1 | 3.0 | ts-seat-service | ts-seat-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-seat-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | improved_to_hit1 | 6 | 1 | 5.0 | ts-assurance-service | ts-assurance-service|ts-basic-service|ts-station-service|ts-route-plan-service|ts-travel-service | pod-failure | ts-assurance-service |
| ts0-ts-basic-service-request-abort-62vtm2 | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-station-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts0-ts-station-service-bandwidth-bp5k94 | rank_improved | 9 | 8 | 1.0 | mysql;ts-station-service | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service | bandwidth | ts-station-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | rank_improved | 3 | 2 | 1.0 | ts-station-food-service | ts-food-service|ts-station-food-service|ts-travel-service|ts-basic-service|ts-order-other-service | pod-failure | ts-station-food-service |
| ts2-ts-auth-service-response-patch-body-9bcpvv | rank_improved | 3 | 2 | 1.0 | ts-auth-service;ts-verification-code-service | ts-ui-dashboard|ts-auth-service|loadgenerator|ts-verification-code-service|ts-basic-service | unknown | unknown |
| ts2-ts-travel-service-pod-failure-jqk2bj | rank_improved | 4 | 3 | 1.0 | ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-ui-dashboard|loadgenerator | pod-failure | ts-travel-service |
| ts3-ts-auth-service-return-9tmvzg | rank_improved | 4 | 3 | 1.0 | ts-auth-service | ts-verification-code-service|ts-ui-dashboard|ts-auth-service|loadgenerator|ts-travel-service | return | ts-auth-service |
| ts4-ts-route-plan-service-response-delay-vxcl8q | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-payment-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-auth-service | response-delay | ts-route-plan-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | rank_improved | 5 | 4 | 1.0 | ts-route-plan-service | ts-payment-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|loadgenerator | pod-failure | ts-route-plan-service |
| ts6-ts-ui-dashboard-response-replace-code-tgfbsg | rank_improved | 6 | 5 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-payment-service|ts-station-food-service|ts-travel-service|ts-seat-service|ts-consign-service | response-replace-code | ts-ui-dashboard |
| ts7-ts-price-service-pod-failure-vg4fh6 | rank_improved | 7 | 6 | 1.0 | ts-price-service | ts-travel-plan-service|ts-basic-service|ts-route-plan-service|ts-travel2-service|ts-travel-service | pod-failure | ts-price-service |
| ts0-mysql-container-kill-9t6n24 | rank_improved | 8 | 6 | 2.0 | mysql | ts-train-service|ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | rank_improved | 4 | 2 | 2.0 | ts-consign-price-service | ts-consign-service|ts-consign-price-service|ts-ui-dashboard|ts-preserve-service|ts-seat-service | pod-failure | ts-consign-price-service |
| ts1-ts-station-service-pod-failure-fn44tf | rank_improved | 6 | 3 | 3.0 | ts-station-service | ts-basic-service|ts-travel-service|ts-station-service|ts-travel2-service|ts-route-plan-service | pod-failure | ts-station-service |
| ts1-ts-train-service-pod-failure-5qwqdz | rank_improved | 6 | 2 | 4.0 | ts-train-service | ts-basic-service|ts-train-service|ts-route-plan-service|ts-travel-service|ts-travel-plan-service | pod-failure | ts-train-service |
| ts5-ts-cancel-service-stress-d8xbsn | rank_improved | 11 | 4 | 7.0 | ts-cancel-service | ts-consign-service|ts-food-service|ts-route-plan-service|ts-cancel-service|ts-auth-service | stress | ts-cancel-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | rank_improved | 14 | 4 | 10.0 | ts-payment-service | ts-inside-payment-service|ts-order-service|ts-order-other-service|ts-payment-service|ts-seat-service | pod-failure | ts-payment-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | rank_regressed | 13 | 16 | -3.0 | ts-preserve-service;ts-ui-dashboard | ts-order-service|ts-seat-service|ts-food-service|loadgenerator|ts-basic-service | request-abort | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | rank_regressed | 2 | 4 | -2.0 | ts-order-service;ts-ui-dashboard | ts-cancel-service|ts-consign-price-service|loadgenerator|ts-ui-dashboard|ts-travel-plan-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-consign-price-service-stress-7r95bt | rank_regressed | 3 | 5 | -2.0 | ts-consign-price-service | ts-payment-service|ts-consign-service|ts-preserve-service|ts-security-service|ts-consign-price-service | stress | ts-consign-price-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | rank_regressed | 6 | 8 | -2.0 | ts-food-service;ts-ui-dashboard | ts-order-service|loadgenerator|ts-seat-service|ts-basic-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-method-c7p9qz | rank_regressed | 7 | 9 | -2.0 | ts-basic-service;ts-price-service | ts-payment-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-consign-price-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | rank_regressed | 14 | 16 | -2.0 | ts-basic-service;ts-price-service | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-preserve-service | response-replace-code | ts-basic-service |
| ts6-ts-route-plan-service-response-replace-code-9pfgvr | rank_regressed | 4 | 6 | -2.0 | ts-route-plan-service;ts-route-service | ts-payment-service|ts-ui-dashboard|ts-consign-service|ts-consign-price-service|ts-security-service | response-replace-code | ts-route-plan-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | rank_regressed | 7 | 9 | -2.0 | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service|ts-consign-price-service|ts-consign-service|ts-station-food-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-travel-plan-service-time-rjdx4x | rank_regressed | 3 | 4 | -1.0 | ts-travel-plan-service | ts-route-plan-service|ts-ui-dashboard|ts-order-service|ts-travel-plan-service|ts-route-service | unknown | unknown |
| ts1-ts-route-service-corrupt-5z9zfl | rank_regressed | 5 | 6 | -1.0 | mysql;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|loadgenerator | corrupt | ts-route-service |
| ts2-ts-food-service-bandwidth-b5qvk5 | rank_regressed | 3 | 4 | -1.0 | ts-food-service;ts-ui-dashboard | ts-consign-service|ts-assurance-service|ts-verification-code-service|ts-ui-dashboard|ts-seat-service | bandwidth | ts-food-service |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | rank_regressed | 3 | 4 | -1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-inside-payment-service|loadgenerator|ts-travel-service|ts-ui-dashboard|ts-payment-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-475jm4 | rank_regressed | 3 | 4 | -1.0 | ts-assurance-service;ts-ui-dashboard | ts-consign-price-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard|ts-station-food-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-wpxp9b | rank_regressed | 4 | 5 | -1.0 | ts-basic-service;ts-station-service | ts-preserve-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-service|ts-basic-service | response-replace-body | ts-basic-service |
| ts4-ts-route-plan-service-response-abort-h48vtr | rank_regressed | 4 | 5 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-payment-service|ts-cancel-service|ts-travel-plan-service|ts-consign-price-service|ts-route-plan-service | response-abort | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-j4nzcx | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-price-service | ts-consign-price-service|ts-ui-dashboard|ts-basic-service|ts-route-plan-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-abort-7f8qrl | rank_regressed | 3 | 4 | -1.0 | ts-basic-service;ts-price-service | ts-route-plan-service|ts-travel-plan-service|ts-consign-service|ts-basic-service|ts-travel2-service | response-abort | ts-basic-service |
| ts5-ts-route-plan-service-request-replace-method-hvvmmj | rank_regressed | 3 | 4 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-station-service|ts-ui-dashboard|ts-route-plan-service|loadgenerator | request-replace-method | ts-route-plan-service |
| ts5-ts-seat-service-response-replace-body-cjm68r | rank_regressed | 4 | 5 | -1.0 | ts-order-other-service;ts-seat-service | ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-consign-price-service|ts-seat-service | response-replace-body | ts-seat-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
