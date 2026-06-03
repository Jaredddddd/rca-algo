# EvidenceRank Compare ARC7 vs ARC12

- Created: 2026-06-03T22:49:20+08:00
- Old: `ARC7`
- New: `ARC12`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.728551 | 0.734880 | 0.006329 |
| AC@3 | 0.943741 | 0.936006 | -0.007736 |
| AC@5 | 0.973277 | 0.971871 | -0.001406 |
| MRR | 0.836843 | 0.839508 | 0.002665 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 35 |
| rank_improved | 29 |
| rank_regressed | 37 |
| regressed_from_hit1 | 26 |
| unchanged | 1295 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-response-replace-body-pwrcvx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-station-service | response-replace-body | ts-basic-service |
| ts0-ts-seat-service-response-replace-code-gqm7pj | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service | response-replace-code | ts-seat-service |
| ts0-ts-travel2-service-request-replace-method-dhgqc8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-travel2-service |
| ts1-ts-basic-service-request-replace-path-z65h6q | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | request-replace-path | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-2vvxvm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-b2ftxt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-route-plan-service-response-replace-code-lmr4bp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts1-ts-travel-plan-service-response-replace-code-6mlrxc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-inside-payment-service|ts-ui-dashboard|ts-travel-service|ts-train-food-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-travel-service-request-replace-method-mgw6hv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-ui-dashboard|ts-route-service | request-replace-method | ts-travel-service |
| ts1-ts-travel-service-response-abort-mqhzdf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-route-plan-service|ts-basic-service|ts-verification-code-service | response-abort | ts-travel-service |
| ts1-ts-travel-service-response-replace-body-vzcxrp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-preserve-service|ts-ui-dashboard | response-replace-body | ts-travel-service |
| ts1-ts-travel-service-response-replace-code-w6jftp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | response-replace-code | ts-travel-service |
| ts2-mysql-loss-4fvjb6 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-preserve-service|ts-security-service|ts-travel2-service|ts-ui-dashboard | loss | mysql |
| ts2-ts-basic-service-response-replace-body-zrxcjp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-preserve-service|ts-ui-dashboard | response-replace-body | ts-basic-service |
| ts2-ts-consign-service-bandwidth-x9qdzm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-payment-service|ts-basic-service | bandwidth | ts-consign-service |
| ts2-ts-preserve-service-response-replace-body-t7d296 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-order-service|ts-security-service | response-replace-body | ts-preserve-service |
| ts2-ts-route-plan-service-request-replace-method-j9lggd | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service|ts-seat-service | request-replace-method | ts-route-plan-service |
| ts2-ts-travel-service-response-replace-code-w4bgvh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-basic-service | response-replace-code | ts-travel-service |
| ts2-ts-travel2-service-response-replace-code-4xptvj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-basic-service | response-replace-code | ts-travel2-service |
| ts2-ts-ui-dashboard-response-abort-rcfl6z | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-travel-service|loadgenerator|ts-ui-dashboard|ts-inside-payment-service|ts-basic-service | response-abort | ts-ui-dashboard |
| ts3-mysql-bandwidth-kpqsfl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-ui-dashboard|ts-order-service|ts-travel-service|loadgenerator | bandwidth | mysql |
| ts3-ts-basic-service-request-replace-method-ljqz6g | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-request-replace-method-xk7cgd | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-station-service|ts-travel2-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-bvqv9z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-vm557j | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-station-service | response-replace-code | ts-basic-service |
| ts3-ts-route-plan-service-response-abort-mwz8b5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel2-service | response-abort | ts-route-plan-service |
| ts3-ts-travel-service-request-replace-method-64dgzx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service | request-replace-method | ts-travel-service |
| ts5-ts-food-service-request-replace-path-c4fd88 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-preserve-service|ts-basic-service|ts-seat-service|ts-order-service | request-replace-path | ts-food-service |
| ts5-ts-food-service-response-replace-code-bgr2hd | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-consign-service|ts-ui-dashboard|ts-order-service|ts-travel-service | response-replace-code | ts-food-service |
| ts7-ts-route-plan-service-partition-g88vxv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-consign-service | partition | ts-route-plan-service |
| ts9-ts-preserve-service-response-replace-code-jxdnlj | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-payment-service|ts-ui-dashboard|ts-assurance-service|ts-food-service | response-replace-code | ts-preserve-service |
| ts2-ts-basic-service-request-replace-method-t7fncf | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-price-service|ts-security-service | request-replace-method | ts-basic-service |
| ts3-ts-route-plan-service-response-replace-code-vqsdbr | improved_to_hit1 | 3 | 1 | 2.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-basic-service|ts-auth-service | response-replace-code | ts-route-plan-service |
| ts3-ts-travel-service-response-replace-code-l22vcj | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-basic-service | response-replace-code | ts-travel-service |
| ts3-ts-travel2-service-response-replace-code-fm72m6 | improved_to_hit1 | 3 | 1 | 2.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-basic-service | response-replace-code | ts-travel2-service |
| ts0-mysql-container-kill-9t6n24 | rank_improved | 8 | 7 | 1.0 | mysql | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-travel2-service | container-kill | mysql |
| ts0-ts-basic-service-request-replace-method-gqn7nd | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts1-mysql-loss-dfzrxw | rank_improved | 3 | 2 | 1.0 | mysql;ts-travel-service | ts-route-plan-service|ts-travel-service|ts-travel-plan-service|ts-ui-dashboard|ts-order-service | loss | mysql |
| ts1-ts-basic-service-response-replace-code-6d6shc | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-travel2-service|ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-lfsjf6 | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-train-service | ts-preserve-service|ts-basic-service|ts-travel2-service|ts-security-service|ts-travel-service | response-replace-code | ts-basic-service |

## Decision Notes

- Accept ARC12 as the current EvidRank-ARC candidate.
- The gain comes from endpoint/status/rise rank-alignment support replacing the legacy endpoint factors in the ARC path, combined with ARC11's effective family participation. This sharper endpoint gate improves protocol mutation head ranking: response-replace-code and request-replace-method dominate the `improved_to_hit1` set.
- The main regression is explainable: endpoint-focused support can over-promote protocol/entry-like neighbors in delay, partition, loss, and a few pod/container cases where propagation-shaped evidence is causal rather than merely symptomatic.
- AC@3 drops by 11 net cases and AC@5 by 2 net cases, so the next step should add a case-local propagation-sensitivity guard instead of weakening the endpoint gate globally.
