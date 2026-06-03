# EvidenceRank Compare V13_REIMPL vs V13_REIMPL_V2

- Created: 2026-06-03T12:24:08+08:00
- Old: `V13_REIMPL`
- New: `V13_REIMPL_V2`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.583685 | 0.670886 | 0.087201 |
| AC@3 | 0.910689 | 0.925457 | 0.014768 |
| AC@5 | 0.955696 | 0.973980 | 0.018284 |
| MRR | 0.747704 | 0.801983 | 0.054279 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 256 |
| rank_improved | 62 |
| rank_regressed | 89 |
| regressed_from_hit1 | 132 |
| unchanged | 883 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-loss-67k278 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-travel-plan-service | loss | mysql |
| ts0-mysql-partition-k9q6lq | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-basic-service|ts-travel-plan-service|ts-travel-service|ts-ui-dashboard | partition | mysql |
| ts0-ts-auth-service-stress-nlpsfx | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-consign-service|ts-preserve-service|ts-seat-service | stress | ts-auth-service |
| ts0-ts-basic-service-request-replace-path-5888sf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-station-service | request-replace-path | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-4vn4gg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-hl8qdr | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-mh6sjz | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-price-service | response-replace-code | ts-basic-service |
| ts0-ts-config-service-corrupt-qjwhfb | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-travel2-service|ts-travel-service|ts-travel-plan-service | corrupt | ts-config-service |
| ts0-ts-config-service-stress-g6rpl9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-consign-price-service|ts-seat-service|ts-travel2-service|ts-basic-service | stress | ts-config-service |
| ts0-ts-food-service-stress-xfwkgh | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-payment-service | stress | ts-food-service |
| ts0-ts-inside-payment-service-stress-5qd9rl | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-payment-service|ts-assurance-service|ts-verification-code-service | stress | ts-inside-payment-service |
| ts0-ts-order-other-service-corrupt-wkdp68 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-ui-dashboard|ts-seat-service|loadgenerator|ts-security-service | corrupt | ts-order-other-service |
| ts0-ts-order-service-exception-l2bqm5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-route-plan-service | exception | ts-order-service |
| ts0-ts-order-service-stress-cklk2p | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-consign-service|ts-travel-service|ts-travel-plan-service | stress | ts-order-service |
| ts0-ts-order-service-stress-xt9wfq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-ui-dashboard|ts-seat-service|ts-consign-price-service|ts-cancel-service | stress | ts-order-service |
| ts0-ts-payment-service-stress-56jvjc | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|ts-consign-price-service|ts-seat-service | stress | ts-payment-service |
| ts0-ts-price-service-stress-n787pd | improved_to_hit1 | 2 | 1 | 1.0 | ts-price-service | ts-price-service|ts-basic-service|ts-travel2-service|ts-travel-service|ts-route-plan-service | stress | ts-price-service |
| ts0-ts-route-plan-service-exception-tcmvg6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-travel-service | exception | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-body-xqldsl | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-cancel-service|ts-ui-dashboard|ts-basic-service | response-replace-body | ts-route-plan-service |
| ts0-ts-route-service-container-kill-tsqgmn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service | ts-route-service|ts-ui-dashboard|ts-payment-service|ts-verification-code-service|ts-basic-service | container-kill | ts-route-service |
| ts0-ts-seat-service-request-delay-wvvjgm | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | request-delay | ts-seat-service |
| ts0-ts-security-service-request-replace-method-m5g977 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-basic-service | request-replace-method | ts-security-service |
| ts0-ts-station-food-service-stress-j5qdln | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-food-service | ts-station-food-service|ts-food-service|ts-ui-dashboard|ts-order-service|ts-preserve-service | stress | ts-station-food-service |
| ts0-ts-travel-plan-service-request-delay-lf5tnb | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-preserve-service|ts-travel2-service|ts-seat-service | request-delay | ts-travel-plan-service |
| ts0-ts-travel-service-response-replace-body-bb9m88 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | response-replace-body | ts-travel-service |
| ts0-ts-travel2-service-request-delay-lzpl9v | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-consign-service|ts-travel-plan-service|ts-route-plan-service | request-delay | ts-travel2-service |
| ts0-ts-ui-dashboard-request-replace-method-fl9jln | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|ts-route-plan-service|ts-assurance-service|ts-travel2-service|ts-travel-plan-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-user-service-loss-tfz45k | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-basic-service | loss | ts-user-service |
| ts0-ts-user-service-partition-77jfkk | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-auth-service | partition | ts-user-service |
| ts0-ts-user-service-stress-mww4jr | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-cancel-service | stress | ts-user-service |
| ts1-mysql-bandwidth-2xj2mq | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-order-service|ts-seat-service|ts-travel-service | bandwidth | mysql |
| ts1-ts-auth-service-request-replace-method-mqrzv4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-order-service | request-replace-method | ts-auth-service |
| ts1-ts-auth-service-response-replace-code-xn6gk2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-basic-service | response-replace-code | ts-auth-service |
| ts1-ts-basic-service-request-abort-snb6ck | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-route-plan-service|ts-route-service | request-abort | ts-basic-service |
| ts1-ts-consign-service-container-kill-r8lmsx | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-food-service|loadgenerator|ts-preserve-service | container-kill | ts-consign-service |
| ts1-ts-inside-payment-service-stress-4qc7k8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-consign-service|ts-ui-dashboard|ts-cancel-service|ts-travel-service | stress | ts-inside-payment-service |
| ts1-ts-inside-payment-service-stress-6qq6f6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-consign-price-service|ts-food-service|ts-route-plan-service | stress | ts-inside-payment-service |
| ts1-ts-inside-payment-service-stress-n6mttx | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-travel-service|ts-consign-price-service|ts-basic-service | stress | ts-inside-payment-service |
| ts1-ts-order-other-service-exception-twstdp | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-security-service|ts-preserve-service|ts-order-service|ts-seat-service | exception | ts-order-other-service |
| ts1-ts-order-service-exception-fvcrfk | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-travel-service | exception | ts-order-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
