# EvidenceRank Compare OCKHAM_PRE_SPLIT_BASE vs OCKHAM_DROP_NOISE_AS_CREST

- Created: 2026-06-14T21:00:55+08:00
- Old: `OCKHAM_PRE_SPLIT_BASE`
- New: `OCKHAM_DROP_NOISE_AS_CREST`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.750352 | -0.049930 |
| AC@3 | 0.944444 | 0.924754 | -0.019691 |
| AC@5 | 0.971871 | 0.970464 | -0.001406 |
| MRR | 0.875326 | 0.840446 | -0.034879 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 47 |
| rank_improved | 38 |
| rank_regressed | 88 |
| regressed_from_hit1 | 118 |
| unchanged | 1131 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-station-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts0-ts-contacts-service-pod-failure-j42hd8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service | ts-contacts-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-order-other-service | pod-failure | ts-contacts-service |
| ts0-ts-seat-service-pod-failure-c87xdg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service | pod-failure | ts-seat-service |
| ts0-ts-travel-service-request-abort-g9mc2t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-voucher-service|ts-seat-service | request-abort | ts-travel-service |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-preserve-service | pod-failure | ts-user-service |
| ts1-ts-payment-service-stress-k7stf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|ts-order-service|loadgenerator | stress | ts-payment-service |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-contacts-service|ts-basic-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-body-5s6gc9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-route-service|ts-travel-service | response-replace-body | ts-route-plan-service |
| ts1-ts-seat-service-request-replace-path-jmcntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-inside-payment-service|ts-order-other-service|ts-travel-plan-service | request-replace-path | ts-seat-service |
| ts1-ts-travel-service-response-replace-code-qzmhjf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-basic-service|ts-station-service|ts-travel-plan-service | response-replace-code | ts-travel-service |
| ts2-ts-basic-service-request-replace-method-v6gzn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-station-service|ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts2-ts-basic-service-request-replace-path-flkd7v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-price-service|ts-basic-service|ts-travel2-service|ts-station-service|ts-train-service | request-replace-path | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts2-ts-consign-price-service-stress-7r95bt | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-ui-dashboard|ts-auth-service|ts-preserve-service | stress | ts-consign-price-service |
| ts2-ts-order-service-container-kill-sr295f | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-ui-dashboard|ts-food-service|ts-auth-service|ts-inside-payment-service | container-kill | ts-order-service |
| ts2-ts-route-plan-service-response-replace-body-dghfbk | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-ui-dashboard | response-replace-body | ts-route-plan-service |
| ts2-ts-security-service-request-replace-method-vdvkxf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-auth-service|ts-verification-code-service|ts-route-service | request-replace-method | ts-security-service |
| ts2-ts-travel2-service-response-replace-code-ttpn92 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-price-service|ts-travel-plan-service|ts-station-service | response-replace-code | ts-travel2-service |
| ts3-ts-basic-service-request-replace-method-pjwm42 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-station-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-response-replace-body-6lk5wq | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-price-service|ts-station-service|ts-train-service | response-replace-body | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-bvqv9z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-travel-plan-service | pod-failure | ts-consign-price-service |
| ts3-ts-route-plan-service-request-replace-path-m56fgf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-verification-code-service|ts-travel-plan-service|ts-travel-service|ts-basic-service | request-replace-path | ts-route-plan-service |
| ts3-ts-seat-service-request-replace-method-b56nqd | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-config-service | request-replace-method | ts-seat-service |
| ts3-ts-travel-service-request-replace-path-vktk7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-basic-service|ts-ui-dashboard | request-replace-path | ts-travel-service |
| ts3-ts-travel2-service-request-replace-method-ggdqhg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-seat-service | request-replace-method | ts-travel2-service |
| ts4-ts-basic-service-request-abort-jr6f2j | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-route-plan-service|ts-seat-service|ts-travel-service | request-abort | ts-basic-service |
| ts4-ts-basic-service-response-abort-94gfnl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-route-plan-service|ts-preserve-service|ts-travel-service|loadgenerator | response-abort | ts-basic-service |
| ts4-ts-config-service-stress-wfgt8h | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-route-plan-service|ts-travel2-service|ts-seat-service|ts-basic-service | stress | ts-config-service |
| ts4-ts-consign-service-partition-ncb5l8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-payment-service|ts-order-other-service|ts-travel2-service | partition | ts-consign-service |
| ts4-ts-order-service-bandwidth-kqnvn7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-auth-service|ts-food-service|ts-travel-service|ts-verification-code-service | bandwidth | ts-order-service |
| ts4-ts-travel-service-partition-xq25fj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-cancel-service | partition | ts-travel-service |
| ts4-ts-travel-service-response-delay-d9w5bf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-basic-service | response-delay | ts-travel-service |
| ts4-ts-travel-service-stress-fz5lbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-ui-dashboard|loadgenerator|ts-cancel-service|ts-travel-plan-service | stress | ts-travel-service |
| ts5-ts-basic-service-request-delay-4qpvfj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-security-service|ts-route-plan-service | request-delay | ts-basic-service |
| ts5-ts-preserve-service-request-replace-method-v2qhvn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-seat-service|ts-config-service|ts-order-service|ts-order-other-service | request-replace-method | ts-preserve-service |
| ts5-ts-ui-dashboard-response-replace-code-9xg52l | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-consign-service|ts-auth-service|ts-assurance-service | response-replace-code | ts-ui-dashboard |
| ts6-ts-route-plan-service-pod-failure-n576ft | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-payment-service | pod-failure | ts-route-plan-service |
| ts7-ts-ui-dashboard-response-replace-code-mdhj8g | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-food-service|ts-assurance-service|ts-verification-code-service | response-replace-code | ts-ui-dashboard |
| ts7-ts-ui-dashboard-response-replace-code-t7vsbl | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|loadgenerator|ts-cancel-service|ts-inside-payment-service | response-replace-code | ts-ui-dashboard |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
