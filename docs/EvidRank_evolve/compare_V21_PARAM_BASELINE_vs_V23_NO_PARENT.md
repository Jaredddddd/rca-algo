# EvidenceRank Compare V21_PARAM_BASELINE vs V23_NO_PARENT

- Created: 2026-06-04T21:44:29+08:00
- Old: `V21_PARAM_BASELINE`
- New: `V23_NO_PARENT`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.827707 | 0.817159 | -0.010549 |
| AC@3 | 0.947257 | 0.945851 | -0.001406 |
| AC@5 | 0.974684 | 0.974684 | 0.000000 |
| MRR | 0.891195 | 0.885126 | -0.006069 |

## Status Counts

| status | cases |
| --- | ---: |
| rank_improved | 10 |
| rank_regressed | 17 |
| regressed_from_hit1 | 15 |
| unchanged | 1380 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-container-kill-9t6n24 | rank_improved | 9 | 8 | 1.0 | mysql | ts-train-service|ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts2-ts-food-service-bandwidth-b5qvk5 | rank_improved | 4 | 3 | 1.0 | ts-food-service;ts-ui-dashboard | ts-consign-service|ts-verification-code-service|ts-ui-dashboard|ts-seat-service|ts-assurance-service | bandwidth | ts-food-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | rank_improved | 6 | 5 | 1.0 | ts-food-service;ts-ui-dashboard | ts-order-service|ts-seat-service|ts-basic-service|ts-travel-service|ts-food-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-bandwidth-fn4pnv | rank_improved | 6 | 5 | 1.0 | ts-basic-service;ts-preserve-service | ts-ui-dashboard|ts-order-service|ts-seat-service|ts-travel-service|ts-basic-service | bandwidth | ts-basic-service |
| ts4-ts-food-service-container-kill-lv5htg | rank_improved | 27 | 26 | 1.0 | ts-config-service | ts-food-service|ts-ui-dashboard|ts-order-service|loadgenerator|ts-travel-service | container-kill | ts-food-service |
| ts4-ts-station-service-bandwidth-nfljv5 | rank_improved | 9 | 8 | 1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-route-service | bandwidth | ts-station-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-price-service | ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | rank_improved | 12 | 11 | 1.0 | ts-basic-service;ts-price-service | ts-payment-service|ts-ui-dashboard|ts-seat-service|ts-order-service|ts-train-food-service | response-replace-code | ts-basic-service |
| ts6-ts-basic-service-request-replace-method-kmmr8k | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-route-service | ts-travel-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts7-ts-ui-dashboard-response-replace-code-t7vsbl | rank_improved | 4 | 3 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-payment-service|ts-cancel-service|ts-ui-dashboard|ts-inside-payment-service|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts1-ts-station-service-pod-failure-fn44tf | rank_regressed | 3 | 5 | -2.0 | ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-station-service | pod-failure | ts-station-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | rank_regressed | 11 | 13 | -2.0 | ts-route-plan-service;ts-travel-plan-service | ts-ui-dashboard|ts-basic-service|ts-travel2-service|ts-consign-price-service|ts-seat-service | response-replace-code | ts-travel-plan-service |
| ts5-ts-travel-plan-service-response-replace-code-k8hf8v | rank_regressed | 6 | 8 | -2.0 | ts-route-plan-service;ts-travel-plan-service | ts-ui-dashboard|ts-consign-price-service|ts-seat-service|ts-basic-service|ts-travel-service | response-replace-code | ts-travel-plan-service |
| ts0-ts-station-service-loss-hs8vrm | rank_regressed | 2 | 3 | -1.0 | mysql;ts-station-service | ts-basic-service|ts-travel-service|ts-station-service|ts-travel2-service|ts-travel-plan-service | loss | ts-station-service |
| ts0-ts-travel-plan-service-time-rjdx4x | rank_regressed | 5 | 6 | -1.0 | ts-travel-plan-service | ts-ui-dashboard|ts-route-plan-service|ts-order-service|ts-seat-service|ts-route-service | unknown | unknown |
| ts1-ts-train-service-pod-failure-5qwqdz | rank_regressed | 4 | 5 | -1.0 | ts-train-service | ts-basic-service|ts-route-plan-service|ts-travel-service|ts-travel-plan-service|ts-train-service | pod-failure | ts-train-service |
| ts2-ts-basic-service-request-replace-method-sbrkxn | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-price-service | ts-travel2-service|ts-travel-service|ts-basic-service|ts-station-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-travel2-service|ts-basic-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts2-ts-consign-price-service-stress-7r95bt | rank_regressed | 3 | 4 | -1.0 | ts-consign-price-service | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-consign-price-service|ts-security-service | stress | ts-consign-price-service |
| ts2-ts-ui-dashboard-request-replace-method-g7zr28 | rank_regressed | 3 | 4 | -1.0 | ts-travel-service;ts-ui-dashboard | ts-travel-plan-service|ts-seat-service|ts-order-service|ts-travel-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-basic-service-response-replace-body-6lk5wq | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-price-service | ts-travel2-service|ts-travel-service|ts-basic-service|ts-travel-plan-service|ts-route-plan-service | response-replace-body | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-zn4kzg | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-travel2-service|ts-basic-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-route-plan-service-request-replace-method-hvvmmj | rank_regressed | 3 | 4 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-ui-dashboard|ts-travel-plan-service|ts-station-service|ts-route-plan-service|ts-travel-service | request-replace-method | ts-route-plan-service |
| ts5-ts-travel-plan-service-response-delay-7cc7nq | rank_regressed | 3 | 4 | -1.0 | ts-route-plan-service;ts-travel-plan-service | ts-payment-service|ts-security-service|ts-order-service|ts-travel-plan-service|ts-seat-service | response-delay | ts-travel-plan-service |
| ts5-ts-travel2-service-response-replace-body-ljvb7g | rank_regressed | 5 | 6 | -1.0 | ts-route-service;ts-travel2-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service|ts-order-service | response-replace-body | ts-travel2-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | rank_regressed | 9 | 10 | -1.0 | ts-food-service;ts-ui-dashboard | ts-order-service|ts-basic-service|ts-consign-service|loadgenerator|ts-verification-code-service | request-abort | ts-ui-dashboard |
| ts8-ts-food-service-pod-failure-9swgtb | rank_regressed | 4 | 5 | -1.0 | ts-food-service | ts-order-service|ts-seat-service|ts-basic-service|ts-ui-dashboard|ts-food-service | pod-failure | ts-food-service |
| ts2-ts-basic-service-response-replace-code-rmprwq | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-route-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-route-plan-service|ts-station-service | response-replace-code | ts-basic-service |
| ts2-ts-food-service-response-delay-drcx9w | regressed_from_hit1 | 1 | 2 | -1.0 | ts-food-service;ts-train-food-service | ts-ui-dashboard|ts-food-service|ts-order-service|ts-basic-service|ts-travel-service | response-delay | ts-food-service |
| ts2-ts-route-plan-service-request-replace-method-dq56rf | regressed_from_hit1 | 1 | 2 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-basic-service|ts-verification-code-service | request-replace-method | ts-route-plan-service |
| ts4-ts-route-plan-service-request-abort-p674pz | regressed_from_hit1 | 1 | 2 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-order-service|ts-basic-service|ts-seat-service | request-abort | ts-route-plan-service |
| ts4-ts-route-plan-service-request-delay-cmtsjp | regressed_from_hit1 | 1 | 2 | -1.0 | ts-route-plan-service;ts-travel-service | ts-consign-service|ts-route-plan-service|ts-order-service|ts-verification-code-service|ts-food-service | request-delay | ts-route-plan-service |
| ts4-ts-route-plan-service-request-replace-method-fd9l64 | regressed_from_hit1 | 1 | 2 | -1.0 | ts-route-plan-service;ts-travel-service | ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-basic-service | request-replace-method | ts-route-plan-service |
| ts4-ts-security-service-response-replace-code-szv8qk | regressed_from_hit1 | 1 | 2 | -1.0 | ts-order-service;ts-security-service | ts-preserve-service|ts-security-service|ts-ui-dashboard|ts-basic-service|ts-order-service | response-replace-code | ts-security-service |
| ts4-ts-travel-plan-service-response-delay-qjd7q4 | regressed_from_hit1 | 1 | 2 | -1.0 | ts-train-service;ts-travel-plan-service | ts-ui-dashboard|ts-travel-plan-service|ts-seat-service|ts-order-service|ts-basic-service | response-delay | ts-travel-plan-service |
| ts4-ts-travel2-service-response-abort-5svkhq | regressed_from_hit1 | 1 | 2 | -1.0 | ts-seat-service;ts-travel2-service | ts-travel-plan-service|ts-travel2-service|ts-route-plan-service|ts-consign-service|ts-seat-service | response-abort | ts-travel2-service |
| ts5-ts-order-service-corrupt-475z9v | regressed_from_hit1 | 1 | 2 | -1.0 | ts-order-service;ts-security-service | ts-ui-dashboard|ts-security-service|ts-basic-service|ts-seat-service|ts-preserve-service | corrupt | ts-order-service |
| ts5-ts-preserve-service-response-delay-g8zznv | regressed_from_hit1 | 1 | 2 | -1.0 | ts-preserve-service;ts-security-service | ts-ui-dashboard|ts-preserve-service|ts-seat-service|ts-order-service|ts-basic-service | response-delay | ts-preserve-service |
| ts5-ts-route-plan-service-request-delay-drzzdc | regressed_from_hit1 | 1 | 2 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-ui-dashboard|ts-route-plan-service|ts-seat-service|ts-order-service|ts-travel-plan-service | request-delay | ts-route-plan-service |
| ts5-ts-route-plan-service-request-delay-wbrskp | regressed_from_hit1 | 1 | 2 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-ui-dashboard|ts-route-plan-service|ts-assurance-service|ts-seat-service|ts-travel-plan-service | request-delay | ts-route-plan-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
