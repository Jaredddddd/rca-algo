# EvidenceRank Compare CERA1_RAW vs CERA1

- Created: 2026-06-05T01:27:54+08:00
- Old: `CERA1_RAW`
- New: `CERA1`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.510549 | 0.691280 | 0.180731 |
| AC@3 | 0.893108 | 0.933193 | 0.040084 |
| AC@5 | 0.961322 | 0.966245 | 0.004923 |
| MRR | 0.700399 | 0.814367 | 0.113968 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 342 |
| rank_improved | 134 |
| rank_regressed | 80 |
| regressed_from_hit1 | 85 |
| unchanged | 781 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-loss-k9xrkf | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-payment-service|ts-preserve-service|ts-ui-dashboard|loadgenerator | loss | mysql |
| ts0-ts-auth-service-stress-nlpsfx | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-consign-service|loadgenerator|ts-seat-service | stress | ts-auth-service |
| ts0-ts-basic-service-request-abort-62vtm2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-station-service | request-abort | ts-basic-service |
| ts0-ts-basic-service-request-abort-924pr2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-preserve-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts0-ts-basic-service-request-replace-method-88h72r | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-price-service|ts-preserve-service|ts-station-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-request-replace-method-brs246 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-price-service|ts-travel-service|ts-preserve-service|ts-station-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-request-replace-path-5888sf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-station-service | request-replace-path | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-4vn4gg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-station-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-5djll8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-price-service | response-replace-code | ts-basic-service |
| ts0-ts-config-service-stress-g6rpl9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-consign-price-service|ts-seat-service|ts-verification-code-service|ts-assurance-service | stress | ts-config-service |
| ts0-ts-consign-price-service-exception-8b6tng | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-ui-dashboard|ts-order-service|ts-seat-service | exception | ts-consign-price-service |
| ts0-ts-food-service-container-kill-fc4sjw | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-consign-service|loadgenerator|ts-seat-service | container-kill | ts-food-service |
| ts0-ts-food-service-stress-dq7mwn | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-assurance-service|ts-order-service|ts-consign-service | stress | ts-food-service |
| ts0-ts-food-service-stress-xfwkgh | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-payment-service | stress | ts-food-service |
| ts0-ts-inside-payment-service-stress-5qd9rl | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-payment-service|loadgenerator|ts-assurance-service | stress | ts-inside-payment-service |
| ts0-ts-order-other-service-corrupt-wkdp68 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-ui-dashboard|loadgenerator|ts-seat-service|ts-security-service | corrupt | ts-order-other-service |
| ts0-ts-order-service-exception-hdgpgm | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service | exception | ts-order-service |
| ts0-ts-order-service-stress-64c8cv | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-ui-dashboard|ts-seat-service|ts-travel-service|ts-route-plan-service | stress | ts-order-service |
| ts0-ts-order-service-stress-cklk2p | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-consign-service|ts-travel-service|ts-travel-plan-service | stress | ts-order-service |
| ts0-ts-order-service-stress-xt9wfq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-ui-dashboard|ts-seat-service|ts-consign-price-service|ts-inside-payment-service | stress | ts-order-service |
| ts0-ts-preserve-service-request-replace-method-2hbvml | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-basic-service|ts-seat-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-48zkx2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-auth-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-cw7ndj | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|loadgenerator|ts-security-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-mbmqzz | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-order-service|ts-price-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-response-abort-7gp2mq | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-ui-dashboard|ts-station-service|ts-contacts-service|ts-price-service | response-abort | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-8h9brj | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-security-service|ts-contacts-service | response-replace-code | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-8lnlwd | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-assurance-service|ts-travel-service|ts-contacts-service | response-replace-code | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-ghpf5j | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-basic-service|ts-auth-service | response-replace-code | ts-preserve-service |
| ts0-ts-price-service-stress-n787pd | improved_to_hit1 | 2 | 1 | 1.0 | ts-price-service | ts-price-service|ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service | stress | ts-price-service |
| ts0-ts-route-plan-service-exception-tcmvg6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-basic-service | exception | ts-route-plan-service |
| ts0-ts-route-plan-service-request-abort-7rfdzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-seat-service|ts-travel-service | request-abort | ts-route-plan-service |
| ts0-ts-route-plan-service-request-replace-method-8ks5m4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel-service|ts-route-service | request-replace-method | ts-route-plan-service |
| ts0-ts-route-plan-service-request-replace-method-gl2rrc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard | request-replace-method | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-lpnvvp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service|ts-seat-service | response-replace-code | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-s6v7mm | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-station-food-service|ts-route-service | response-replace-code | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-vh2bnx | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-train-food-service|ts-travel-plan-service|ts-travel2-service|ts-station-service | response-replace-code | ts-route-plan-service |
| ts0-ts-route-service-container-kill-tsqgmn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service | ts-route-service|ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-order-service | container-kill | ts-route-service |
| ts0-ts-route-service-exception-5hzgms | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service | ts-route-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-verification-code-service | exception | ts-route-service |
| ts0-ts-seat-service-request-delay-wvvjgm | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-basic-service | request-delay | ts-seat-service |
| ts0-ts-seat-service-response-abort-fddpcv | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-order-other-service | response-abort | ts-seat-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
