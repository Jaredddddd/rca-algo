# EvidenceRank Compare V16 vs V17

- Created: 2026-06-02T18:54:51+08:00
- Old: `V16`
- New: `V17`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.583685 | 0.563291 | -0.020394 |
| AC@3 | 0.877637 | 0.868495 | -0.009142 |
| AC@5 | 0.945851 | 0.939522 | -0.006329 |
| MRR | 0.739592 | 0.724849 | -0.014743 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 4 |
| rank_improved | 9 |
| rank_regressed | 86 |
| regressed_from_hit1 | 33 |
| unchanged | 1290 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts1-ts-preserve-service-request-replace-method-xmhsbb | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-consign-service | request-replace-method | ts-preserve-service |
| ts2-ts-preserve-service-response-replace-body-t7d296 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-security-service | response-replace-body | ts-preserve-service |
| ts3-ts-config-service-container-kill-52d5j7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-seat-service|ts-payment-service|ts-travel2-service|loadgenerator | container-kill | ts-config-service |
| ts6-ts-travel2-service-request-delay-bnhhtc | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-order-other-service|ts-travel-plan-service|ts-cancel-service | request-delay | ts-travel2-service |
| ts1-ts-station-service-pod-failure-fn44tf | rank_improved | 3 | 2 | 1.0 | ts-station-service | ts-basic-service|ts-station-service|ts-travel-service|ts-travel2-service|ts-route-plan-service | pod-failure | ts-station-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | rank_improved | 4 | 3 | 1.0 | ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard|ts-price-service | pod-failure | ts-travel2-service |
| ts3-mysql-pod-failure-58qts5 | rank_improved | 31 | 30 | 1.0 | mysql | ts-auth-service|loadgenerator|ts-travel-service|ts-ui-dashboard|ts-route-plan-service | pod-failure | mysql |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | rank_improved | 3 | 2 | 1.0 | ts-consign-price-service | ts-consign-service|ts-consign-price-service|ts-ui-dashboard|loadgenerator|ts-preserve-service | pod-failure | ts-consign-price-service |
| ts4-ts-basic-service-request-replace-method-7c9cbv | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-route-service | ts-route-plan-service|loadgenerator|ts-travel-plan-service|ts-route-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | rank_improved | 14 | 13 | 1.0 | ts-basic-service;ts-price-service | ts-cancel-service|ts-preserve-service|ts-station-service|ts-order-service|loadgenerator | request-replace-method | ts-basic-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | rank_improved | 4 | 3 | 1.0 | ts-route-plan-service;ts-travel-plan-service | loadgenerator|ts-consign-price-service|ts-travel-plan-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-travel-plan-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | rank_improved | 12 | 11 | 1.0 | ts-basic-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-preserve-service|ts-security-service | response-replace-code | ts-travel2-service |
| ts4-ts-basic-service-response-abort-d2gjmt | rank_improved | 7 | 5 | 2.0 | ts-basic-service;ts-train-service | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-basic-service | response-abort | ts-basic-service |
| ts2-ts-ui-dashboard-response-replace-code-ms2qf9 | rank_regressed | 8 | 12 | -4.0 | ts-travel-plan-service;ts-ui-dashboard | loadgenerator|ts-config-service|ts-payment-service|ts-seat-service|ts-basic-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-g7zr28 | rank_regressed | 10 | 13 | -3.0 | ts-travel-service;ts-ui-dashboard | ts-travel-plan-service|loadgenerator|ts-seat-service|ts-config-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | rank_regressed | 12 | 15 | -3.0 | ts-travel-plan-service;ts-ui-dashboard | ts-inside-payment-service|ts-station-service|ts-payment-service|loadgenerator|ts-train-food-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-475jm4 | rank_regressed | 5 | 8 | -3.0 | ts-assurance-service;ts-ui-dashboard | ts-cancel-service|ts-consign-price-service|ts-route-plan-service|ts-contacts-service|ts-order-other-service | response-replace-code | ts-ui-dashboard |
| ts5-ts-ui-dashboard-response-replace-code-fsnppw | rank_regressed | 10 | 13 | -3.0 | ts-ui-dashboard;ts-verification-code-service | ts-security-service|loadgenerator|ts-station-food-service|ts-food-service|ts-auth-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-prqgf5 | rank_regressed | 11 | 13 | -2.0 | ts-route-service;ts-ui-dashboard | ts-assurance-service|ts-consign-price-service|ts-travel-service|ts-order-service|ts-food-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-food-service-bandwidth-b5qvk5 | rank_regressed | 5 | 7 | -2.0 | ts-food-service;ts-ui-dashboard | ts-consign-service|ts-assurance-service|loadgenerator|ts-verification-code-service|ts-seat-service | bandwidth | ts-food-service |
| ts2-ts-ui-dashboard-response-replace-code-bzfxkt | rank_regressed | 4 | 6 | -2.0 | ts-travel-service;ts-ui-dashboard | loadgenerator|ts-consign-service|ts-contacts-service|ts-route-service|ts-food-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-travel-service-request-delay-qhz8pd | rank_regressed | 3 | 5 | -2.0 | ts-route-service;ts-travel-service | ts-station-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-travel-service | request-delay | ts-travel-service |
| ts3-ts-ui-dashboard-request-replace-method-7lstrz | rank_regressed | 11 | 13 | -2.0 | ts-assurance-service;ts-ui-dashboard | loadgenerator|ts-price-service|ts-config-service|ts-contacts-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-replace-code-tx624r | rank_regressed | 3 | 5 | -2.0 | ts-auth-service;ts-ui-dashboard | ts-consign-price-service|loadgenerator|ts-payment-service|ts-preserve-service|ts-ui-dashboard | response-replace-code | ts-ui-dashboard |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | rank_regressed | 9 | 11 | -2.0 | ts-travel-plan-service;ts-ui-dashboard | loadgenerator|ts-travel2-service|ts-route-plan-service|ts-consign-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-abort-sclg6k | rank_regressed | 5 | 7 | -2.0 | ts-basic-service;ts-price-service | ts-route-plan-service|ts-consign-service|ts-order-service|ts-travel2-service|loadgenerator | request-abort | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-m559vq | rank_regressed | 6 | 8 | -2.0 | ts-basic-service;ts-route-service | ts-inside-payment-service|loadgenerator|ts-route-plan-service|ts-travel2-service|ts-travel-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | rank_regressed | 22 | 24 | -2.0 | ts-basic-service;ts-price-service | ts-payment-service|ts-train-food-service|loadgenerator|ts-consign-price-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts5-ts-travel2-service-request-abort-24j7nn | rank_regressed | 6 | 8 | -2.0 | ts-basic-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-preserve-service|ts-route-service|ts-config-service | request-abort | ts-travel2-service |
| ts7-ts-ui-dashboard-request-replace-method-cgqxk7 | rank_regressed | 2 | 4 | -2.0 | ts-food-service;ts-ui-dashboard | loadgenerator|ts-cancel-service|ts-travel-service|ts-food-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | rank_regressed | 6 | 7 | -1.0 | mysql | ts-train-service|ts-auth-service|loadgenerator|ts-verification-code-service|ts-ui-dashboard | container-kill | mysql |
| ts0-ts-basic-service-response-replace-code-lq4ncj | rank_regressed | 3 | 4 | -1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-preserve-service-response-abort-mj9pbn | rank_regressed | 2 | 3 | -1.0 | ts-order-service;ts-preserve-service | ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-seat-service|ts-basic-service | response-abort | ts-preserve-service |
| ts0-ts-travel-plan-service-time-rjdx4x | rank_regressed | 2 | 3 | -1.0 | ts-travel-plan-service | loadgenerator|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service | unknown | unknown |
| ts0-ts-ui-dashboard-request-replace-method-5dxswc | rank_regressed | 4 | 5 | -1.0 | ts-travel-plan-service;ts-ui-dashboard | loadgenerator|ts-consign-price-service|ts-security-service|ts-consign-service|ts-ui-dashboard | request-replace-method | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-m8st7d | rank_regressed | 3 | 4 | -1.0 | ts-travel-plan-service;ts-ui-dashboard | loadgenerator|ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|ts-consign-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-basic-service-response-replace-code-v225t5 | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-station-service | ts-travel-service|loadgenerator|ts-basic-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | rank_regressed | 6 | 7 | -1.0 | ts-food-service;ts-train-food-service | ts-consign-service|ts-payment-service|ts-order-service|ts-price-service|ts-travel-service | unknown | unknown |
| ts1-ts-preserve-service-response-replace-code-b7m2g5 | rank_regressed | 2 | 3 | -1.0 | ts-contacts-service;ts-preserve-service | ts-order-service|loadgenerator|ts-preserve-service|ts-station-food-service|ts-contacts-service | response-replace-code | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | rank_regressed | 2 | 3 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-train-service|ts-route-plan-service|ts-contacts-service|loadgenerator | request-replace-method | ts-route-plan-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
