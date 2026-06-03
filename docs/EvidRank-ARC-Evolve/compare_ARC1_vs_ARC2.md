# EvidenceRank Compare ARC1 vs ARC2

- Created: 2026-06-03T17:13:23+08:00
- Old: `ARC1`
- New: `ARC2`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.705345 | 0.720113 | 0.014768 |
| AC@3 | 0.940225 | 0.940928 | 0.000703 |
| AC@5 | 0.971167 | 0.973277 | 0.002110 |
| MRR | 0.823675 | 0.832050 | 0.008375 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 54 |
| rank_improved | 38 |
| rank_regressed | 31 |
| regressed_from_hit1 | 33 |
| unchanged | 1266 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-pod-failure-94xplz | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | pod-failure | ts-basic-service |
| ts0-ts-basic-service-request-abort-5dlq8r | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service | request-abort | ts-basic-service |
| ts0-ts-basic-service-response-replace-body-2ntz4z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-route-plan-service | response-replace-body | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-5djll8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-price-service | response-replace-code | ts-basic-service |
| ts0-ts-route-plan-service-response-replace-code-lnggrn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel-service | response-replace-code | ts-route-plan-service |
| ts0-ts-seat-service-response-abort-fddpcv | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-order-other-service | response-abort | ts-seat-service |
| ts0-ts-security-service-response-replace-code-f2529z | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-order-service | response-replace-code | ts-security-service |
| ts0-ts-travel2-service-response-replace-body-rmn797 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service | response-replace-body | ts-travel2-service |
| ts0-ts-ui-dashboard-request-replace-method-fl9jln | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|ts-route-plan-service|ts-assurance-service|ts-user-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-basic-service-request-replace-method-wnm8xl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-food-service-stress-cm6h5v | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-consign-service|ts-ui-dashboard|ts-inside-payment-service|ts-route-plan-service | stress | ts-food-service |
| ts1-ts-inside-payment-service-stress-6qq6f6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-food-service|ts-route-plan-service|loadgenerator | stress | ts-inside-payment-service |
| ts1-ts-preserve-service-response-replace-code-b7m2g5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-food-service|ts-contacts-service | response-replace-code | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-p6bkb6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-travel2-service|ts-travel-service | request-replace-method | ts-route-plan-service |
| ts1-ts-station-service-pod-failure-fn44tf | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service | pod-failure | ts-station-service |
| ts1-ts-train-service-pod-failure-5qwqdz | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service | ts-train-service|ts-basic-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-train-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-basic-service|ts-station-service|ts-travel-service|ts-route-plan-service | pod-failure | ts-assurance-service |
| ts2-ts-basic-service-request-replace-method-hjnzfp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-price-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts2-ts-basic-service-response-abort-kqlbzw | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-travel2-service|ts-route-plan-service | response-abort | ts-basic-service |
| ts2-ts-consign-service-bandwidth-x9qdzm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-payment-service|ts-preserve-service | bandwidth | ts-consign-service |
| ts2-ts-food-service-response-abort-5k6q44 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-config-service | response-abort | ts-food-service |
| ts2-ts-route-plan-service-response-replace-code-q8jrhd | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel-service | response-replace-code | ts-route-plan-service |
| ts2-ts-seat-service-response-replace-code-kttq2h | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | response-replace-code | ts-seat-service |
| ts2-ts-security-service-request-replace-method-kfks5v | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-ui-dashboard|ts-order-other-service | request-replace-method | ts-security-service |
| ts2-ts-travel2-service-response-replace-code-dh8ncq | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-ui-dashboard|ts-travel-plan-service | response-replace-code | ts-travel2-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-food-service|ts-order-service|ts-seat-service|ts-travel-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-49hvp5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-travel-service|ts-basic-service|ts-verification-code-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-auth-service-response-replace-body-d2pnfg | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-seat-service|ts-verification-code-service | response-replace-body | ts-auth-service |
| ts3-ts-basic-service-response-replace-body-w5fj79 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-route-service|ts-ui-dashboard|ts-preserve-service | response-replace-body | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-qklc4n | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-verification-code-service | response-replace-code | ts-basic-service |
| ts3-ts-food-service-request-replace-method-p4xjxp | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|ts-verification-code-service|ts-route-service|ts-auth-service | request-replace-method | ts-food-service |
| ts3-ts-food-service-response-abort-9tjsld | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-ui-dashboard|ts-travel-service|ts-order-service|ts-train-food-service | response-abort | ts-food-service |
| ts3-ts-order-service-pod-failure-7xsmwd | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-ui-dashboard|ts-travel-service|loadgenerator | pod-failure | ts-order-service |
| ts3-ts-preserve-service-request-replace-path-9f8dtp | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-security-service|loadgenerator | request-replace-path | ts-preserve-service |
| ts3-ts-security-service-response-replace-code-2cnwvh | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-order-other-service | response-replace-code | ts-security-service |
| ts3-ts-travel-plan-service-response-replace-code-79hbwm | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-preserve-service|ts-basic-service|ts-travel2-service | response-replace-code | ts-travel-plan-service |
| ts3-ts-travel-plan-service-response-replace-code-cl7m5g | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-contacts-service|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-travel-plan-service |
| ts3-ts-ui-dashboard-request-replace-method-hh8qpt | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|ts-cancel-service|ts-order-service|ts-inside-payment-service|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-replace-code-fjll2p | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-seat-service|ts-consign-price-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-replace-code-kxp2f4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-order-service|ts-verification-code-service | response-replace-code | ts-ui-dashboard |

## Decision Notes

- Accept ARC2 as the current EvidRank-ARC line.
- Metrics are all positive relative to ARC1: AC@1 `+0.014768`, MRR `+0.008375`, AC@3 `+0.000703`, AC@5 `+0.002110`.
- `improved_to_hit1` has 54 cases, mostly `response-replace-code`, `request-replace-method`, pod-failure, response-abort, and response-replace-body; 52 of these were old rank-2 misses.
- `regressed_from_hit1` has 33 cases, all moving from rank 1 to rank 2. These cluster in delay, request-delay, response-delay, partition, and a few bandwidth/corrupt/loss cases, matching the expected risk that true roots can sometimes look propagation-shaped.
- General mechanism: family-level median reliability provides a conservative calibration signal, and local family contrast (`metric + mutation + log - propagation`) suppresses high-traffic victim nodes without using labels, service names, fault names, or fixed per-feature priors.
