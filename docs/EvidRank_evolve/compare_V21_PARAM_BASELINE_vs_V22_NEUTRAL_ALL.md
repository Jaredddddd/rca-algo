# EvidenceRank Compare V21_PARAM_BASELINE vs V22_NEUTRAL_ALL

- Created: 2026-06-04T21:36:12+08:00
- Old: `V21_PARAM_BASELINE`
- New: `V22_NEUTRAL_ALL`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.827707 | 0.804501 | -0.023207 |
| AC@3 | 0.947257 | 0.941632 | -0.005626 |
| AC@5 | 0.974684 | 0.974684 | 0.000000 |
| MRR | 0.891195 | 0.876950 | -0.014245 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 11 |
| rank_improved | 26 |
| rank_regressed | 39 |
| regressed_from_hit1 | 44 |
| unchanged | 1302 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-seat-service-pod-failure-c87xdg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service | ts-seat-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-seat-service |
| ts0-ts-travel-service-pod-failure-cvrncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-food-service|ts-travel-plan-service|ts-ui-dashboard | pod-failure | ts-travel-service |
| ts1-ts-payment-service-stress-k7stf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|ts-seat-service|ts-order-service | stress | ts-payment-service |
| ts2-ts-route-plan-service-return-xw84fv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-consign-service|ts-ui-dashboard|ts-station-food-service|ts-basic-service | return | ts-route-plan-service |
| ts4-ts-seat-service-request-replace-method-9wfmmb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service | request-replace-method | ts-seat-service |
| ts4-ts-seat-service-response-replace-code-h5lfx8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | response-replace-code | ts-seat-service |
| ts4-ts-travel2-service-request-abort-ttlcpg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-order-other-service|ts-order-service | request-abort | ts-travel2-service |
| ts5-ts-seat-service-loss-5kglkt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-payment-service | loss | ts-seat-service |
| ts5-ts-ui-dashboard-request-replace-method-dd2fll | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-ui-dashboard | ts-contacts-service|ts-ui-dashboard|ts-travel2-service|ts-verification-code-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts7-ts-ui-dashboard-request-replace-method-cgqxk7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-food-service|ts-basic-service|ts-order-service|ts-travel-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts8-ts-seat-service-request-replace-method-mx5nvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-seat-service |
| ts0-mysql-container-kill-9t6n24 | rank_improved | 9 | 8 | 1.0 | mysql | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts0-ts-basic-service-pod-failure-94xplz | rank_improved | 3 | 2 | 1.0 | ts-basic-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-basic-service |
| ts0-ts-user-service-pod-failure-b44c7f | rank_improved | 3 | 2 | 1.0 | ts-user-service | ts-ui-dashboard|ts-user-service|loadgenerator|ts-auth-service|ts-verification-code-service | pod-failure | ts-user-service |
| ts2-ts-food-service-bandwidth-b5qvk5 | rank_improved | 4 | 3 | 1.0 | ts-food-service;ts-ui-dashboard | ts-consign-service|ts-verification-code-service|ts-ui-dashboard|ts-seat-service|ts-assurance-service | bandwidth | ts-food-service |
| ts2-ts-ui-dashboard-request-replace-method-jrt2mv | rank_improved | 4 | 3 | 1.0 | ts-train-service;ts-ui-dashboard | ts-seat-service|ts-order-service|ts-ui-dashboard|ts-train-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | rank_improved | 6 | 5 | 1.0 | ts-food-service;ts-ui-dashboard | ts-order-service|ts-seat-service|ts-basic-service|ts-travel-service|ts-food-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | rank_improved | 14 | 13 | 1.0 | ts-preserve-service;ts-ui-dashboard | ts-order-service|ts-seat-service|ts-basic-service|ts-food-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | rank_improved | 5 | 4 | 1.0 | ts-route-plan-service;ts-travel-service | ts-ui-dashboard|ts-basic-service|ts-seat-service|ts-travel-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | rank_improved | 16 | 15 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-ui-dashboard|ts-seat-service|ts-order-service|ts-basic-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-m559vq | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-route-service | ts-route-plan-service|ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-seat-service-response-replace-body-cjm68r | rank_improved | 4 | 3 | 1.0 | ts-order-other-service;ts-seat-service | ts-travel-plan-service|ts-route-plan-service|ts-seat-service|ts-travel2-service|ts-consign-price-service | response-replace-body | ts-seat-service |
| ts5-ts-travel2-service-request-replace-method-zfpch6 | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard|ts-seat-service | request-replace-method | ts-travel2-service |
| ts5-ts-ui-dashboard-response-replace-code-fsnppw | rank_improved | 3 | 2 | 1.0 | ts-ui-dashboard;ts-verification-code-service | ts-security-service|ts-ui-dashboard|ts-order-service|ts-basic-service|ts-food-service | response-replace-code | ts-ui-dashboard |
| ts8-ts-basic-service-response-replace-code-vpbr92 | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-price-service | ts-route-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | rank_improved | 15 | 14 | 1.0 | ts-train-service;ts-ui-dashboard | ts-payment-service|ts-inside-payment-service|ts-verification-code-service|ts-basic-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts0-ts-ui-dashboard-request-replace-method-fl9jln | rank_improved | 5 | 3 | 2.0 | ts-ui-dashboard;ts-user-service | ts-route-plan-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-train-service-pod-failure-5qwqdz | rank_improved | 4 | 2 | 2.0 | ts-train-service | ts-basic-service|ts-train-service|ts-route-plan-service|ts-travel-service|ts-travel-plan-service | pod-failure | ts-train-service |
| ts4-ts-seat-service-bandwidth-k2bwt2 | rank_improved | 6 | 4 | 2.0 | ts-config-service;ts-seat-service | ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|ts-seat-service|ts-basic-service | bandwidth | ts-seat-service |
| ts4-ts-station-service-bandwidth-nfljv5 | rank_improved | 9 | 7 | 2.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-route-service | bandwidth | ts-station-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | rank_improved | 12 | 10 | 2.0 | ts-basic-service;ts-price-service | ts-payment-service|ts-ui-dashboard|ts-seat-service|ts-train-food-service|ts-order-service | response-replace-code | ts-basic-service |
| ts6-ts-basic-service-request-replace-method-4qzglm | rank_improved | 9 | 7 | 2.0 | ts-basic-service;ts-train-service | ts-cancel-service|ts-consign-service|ts-order-service|ts-travel-service|ts-verification-code-service | request-replace-method | ts-basic-service |
| ts6-ts-basic-service-request-replace-method-kmmr8k | rank_improved | 4 | 2 | 2.0 | ts-basic-service;ts-route-service | ts-travel-service|ts-basic-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts6-ts-food-service-request-replace-method-n59f6p | rank_improved | 6 | 4 | 2.0 | ts-food-service;ts-travel-service | ts-route-plan-service|ts-basic-service|ts-order-service|ts-travel-service|ts-food-service | request-replace-method | ts-food-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | rank_improved | 8 | 5 | 3.0 | ts-assurance-service;ts-ui-dashboard | ts-basic-service|ts-consign-service|ts-seat-service|ts-order-service|ts-assurance-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | rank_improved | 8 | 5 | 3.0 | ts-order-other-service;ts-ui-dashboard | ts-seat-service|ts-travel2-service|loadgenerator|ts-route-service|ts-order-other-service | request-abort | ts-ui-dashboard |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | rank_improved | 11 | 7 | 4.0 | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-basic-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-route-plan-service-request-replace-method-v76qjz | rank_regressed | 2 | 6 | -4.0 | ts-route-plan-service;ts-route-service | ts-travel-plan-service|ts-basic-service|ts-travel-service|ts-seat-service|ts-ui-dashboard | request-replace-method | ts-route-plan-service |
| ts5-ts-travel-plan-service-response-replace-code-k8hf8v | rank_regressed | 6 | 10 | -4.0 | ts-route-plan-service;ts-travel-plan-service | ts-consign-price-service|ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-travel-service | response-replace-code | ts-travel-plan-service |
| ts2-ts-consign-price-service-stress-7r95bt | rank_regressed | 3 | 6 | -3.0 | ts-consign-price-service | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-seat-service | stress | ts-consign-price-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
