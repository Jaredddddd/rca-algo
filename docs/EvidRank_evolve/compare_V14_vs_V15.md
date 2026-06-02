# EvidenceRank Compare V14 vs V15

- Created: 2026-06-02T18:34:03+08:00
- Old: `V14`
- New: `V15`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.657525 | 0.638537 | -0.018987 |
| AC@3 | 0.914205 | 0.884669 | -0.029536 |
| AC@5 | 0.962025 | 0.949367 | -0.012658 |
| MRR | 0.791101 | 0.772135 | -0.018966 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 71 |
| rank_improved | 73 |
| rank_regressed | 111 |
| regressed_from_hit1 | 98 |
| unchanged | 1069 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-loss-hfrvkl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-basic-service|loadgenerator | loss | mysql |
| ts0-mysql-partition-mphlhs | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-assurance-service|loadgenerator | partition | mysql |
| ts0-ts-basic-service-response-delay-cg24jn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-travel-service | response-delay | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-5djll8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-price-service | response-replace-code | ts-basic-service |
| ts0-ts-config-service-stress-g6rpl9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-seat-service|ts-consign-price-service|ts-travel2-service|ts-verification-code-service | stress | ts-config-service |
| ts0-ts-seat-service-request-replace-method-h4rcm9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-seat-service |
| ts0-ts-seat-service-response-delay-fjqtmh | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-preserve-service|ts-travel-service|ts-travel2-service | response-delay | ts-seat-service |
| ts1-mysql-loss-dfzrxw | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-order-service | loss | mysql |
| ts1-ts-basic-service-request-delay-4tqskz | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-ui-dashboard|ts-preserve-service|ts-travel-service|ts-route-plan-service | request-delay | ts-basic-service |
| ts1-ts-preserve-service-response-replace-code-bndht9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-security-service|ts-verification-code-service | response-replace-code | ts-preserve-service |
| ts1-ts-preserve-service-stress-lbwbnm | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-food-service|ts-route-plan-service|ts-assurance-service | stress | ts-preserve-service |
| ts1-ts-route-service-corrupt-qlt7gn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|loadgenerator|ts-train-service|ts-auth-service | corrupt | ts-route-service |
| ts1-ts-travel-plan-service-response-delay-zhj7r7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-route-plan-service | response-delay | ts-travel-plan-service |
| ts2-mysql-bandwidth-fws9rx | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|loadgenerator | bandwidth | mysql |
| ts2-mysql-delay-d427wn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-travel-service | delay | mysql |
| ts2-ts-auth-service-stress-lq54b9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-assurance-service|ts-consign-service|ts-verification-code-service | stress | ts-auth-service |
| ts2-ts-basic-service-response-delay-8d8blx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-contacts-service | response-delay | ts-basic-service |
| ts2-ts-config-service-stress-j8gm95 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-seat-service|ts-route-plan-service|ts-ui-dashboard|ts-verification-code-service | stress | ts-config-service |
| ts2-ts-consign-price-service-stress-7r95bt | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-payment-service|ts-ui-dashboard|ts-preserve-service | stress | ts-consign-price-service |
| ts2-ts-consign-service-delay-k5d7zl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-seat-service | delay | ts-consign-service |
| ts2-ts-food-service-bandwidth-b5qvk5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|ts-assurance-service|ts-verification-code-service|ts-seat-service|ts-consign-service | bandwidth | ts-food-service |
| ts2-ts-food-service-request-replace-method-z2sbdz | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-config-service|ts-travel-plan-service | request-replace-method | ts-food-service |
| ts2-ts-route-plan-service-response-replace-code-7z5jgz | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard|ts-travel-service | response-replace-code | ts-route-plan-service |
| ts2-ts-travel-service-delay-gbx5sb | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-ui-dashboard|ts-food-service|ts-route-plan-service|ts-travel-plan-service | delay | ts-travel-service |
| ts2-ts-ui-dashboard-request-replace-method-cqn54z | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-route-service|ts-order-service|ts-auth-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-h27hzq | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-food-service|loadgenerator|ts-order-service|ts-ui-dashboard|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-abort-hnvckb | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service;ts-ui-dashboard | ts-travel2-service|ts-basic-service|ts-order-other-service|ts-price-service|loadgenerator | response-abort | ts-ui-dashboard |
| ts3-mysql-bandwidth-kpqsfl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-route-plan-service | bandwidth | mysql |
| ts3-mysql-corrupt-4kplqx | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-route-plan-service | corrupt | mysql |
| ts3-mysql-corrupt-wgvhdb | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-route-plan-service|ts-travel2-service|ts-travel-plan-service | corrupt | mysql |
| ts3-mysql-partition-4hh8bj | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | partition | mysql |
| ts3-ts-basic-service-response-delay-qh7j7v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-ui-dashboard|ts-consign-service | response-delay | ts-basic-service |
| ts3-ts-travel-plan-service-request-delay-b8pn5w | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-user-service|ts-basic-service | request-delay | ts-travel-plan-service |
| ts3-ts-travel-service-response-delay-4rdh8b | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-ui-dashboard|loadgenerator|ts-order-other-service|ts-route-plan-service | response-delay | ts-travel-service |
| ts3-ts-travel-service-response-delay-7c9494 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-route-plan-service | response-delay | ts-travel-service |
| ts3-ts-travel2-service-response-delay-hf7kl4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-seat-service | response-delay | ts-travel2-service |
| ts4-ts-basic-service-corrupt-trd2kh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-security-service|ts-order-service | corrupt | ts-basic-service |
| ts4-ts-basic-service-request-delay-jkxt8v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-route-plan-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-request-delay-xhctbw | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-assurance-service|ts-preserve-service|ts-travel-service|ts-route-plan-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-response-delay-76ksjc | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-route-plan-service|ts-travel-service|ts-travel-plan-service|ts-order-other-service | response-delay | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
