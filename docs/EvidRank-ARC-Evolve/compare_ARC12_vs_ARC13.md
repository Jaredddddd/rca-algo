# EvidenceRank Compare ARC12 vs ARC13

- Created: 2026-06-05T12:54:46+08:00
- Old: `ARC12`
- New: `ARC13`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.734880 | 0.831224 | 0.096343 |
| AC@3 | 0.936006 | 0.947961 | 0.011955 |
| AC@5 | 0.971871 | 0.975387 | 0.003516 |
| MRR | 0.839508 | 0.893267 | 0.053760 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 180 |
| rank_improved | 80 |
| rank_regressed | 48 |
| regressed_from_hit1 | 43 |
| unchanged | 1071 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-loss-hfrvkl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-seat-service | loss | mysql |
| ts0-mysql-partition-mphlhs | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-basic-service | partition | mysql |
| ts0-ts-basic-service-request-delay-d5jvr6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-travel2-service|ts-seat-service | request-delay | ts-basic-service |
| ts0-ts-basic-service-request-replace-method-z2nlcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-station-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-request-replace-path-8q599t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-train-service|ts-station-service | request-replace-path | ts-basic-service |
| ts0-ts-basic-service-response-delay-cg24jn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-travel2-service | response-delay | ts-basic-service |
| ts0-ts-consign-price-service-stress-t67vtg | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-basic-service|ts-travel-service|ts-payment-service | stress | ts-consign-price-service |
| ts0-ts-preserve-service-response-abort-mj9pbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-basic-service|ts-ui-dashboard|ts-contacts-service|ts-station-service | response-abort | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-kvkzkr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-basic-service|ts-station-service|ts-contacts-service|ts-ui-dashboard | response-replace-code | ts-preserve-service |
| ts0-ts-route-plan-service-request-replace-method-lrzhl6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-order-service | request-replace-method | ts-route-plan-service |
| ts0-ts-seat-service-response-replace-body-vx8tdz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-order-other-service|ts-travel-plan-service | response-replace-body | ts-seat-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-order-service|ts-travel-plan-service | response-replace-code | ts-seat-service |
| ts0-ts-security-service-request-replace-method-j6gpxx | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-ui-dashboard|ts-order-other-service | request-replace-method | ts-security-service |
| ts0-ts-security-service-request-replace-method-m5g977 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-travel-service | request-replace-method | ts-security-service |
| ts0-ts-security-service-response-replace-code-47m5nd | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-order-other-service | response-replace-code | ts-security-service |
| ts0-ts-security-service-response-replace-code-fbsfls | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-order-other-service|ts-ui-dashboard | response-replace-code | ts-security-service |
| ts0-ts-travel-service-mysql-28wmss | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-consign-service|ts-seat-service|ts-food-service|ts-order-service | unknown | unknown |
| ts0-ts-travel-service-request-delay-z8wzcp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-basic-service|ts-seat-service|ts-order-service|ts-food-service | request-delay | ts-travel-service |
| ts0-ts-ui-dashboard-response-delay-nqtssr | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-assurance-service|ts-travel-service | response-delay | ts-ui-dashboard |
| ts0-ts-user-service-partition-77jfkk | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-verification-code-service | partition | ts-user-service |
| ts1-ts-auth-service-request-replace-method-mrrl9f | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator|ts-travel-service | request-replace-method | ts-auth-service |
| ts1-ts-basic-service-request-replace-method-hz96t6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-station-service|ts-train-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-request-replace-method-kqkjgj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-lfsjf6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-preserve-service|ts-train-service | response-replace-code | ts-basic-service |
| ts1-ts-food-service-stress-cm6h5v | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-consign-service|ts-inside-payment-service|ts-ui-dashboard|ts-travel-service | stress | ts-food-service |
| ts1-ts-inside-payment-service-stress-6qq6f6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-travel-service | stress | ts-inside-payment-service |
| ts1-ts-inside-payment-service-stress-n6mttx | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-basic-service|ts-order-service|ts-seat-service | stress | ts-inside-payment-service |
| ts1-ts-payment-service-stress-5778hg | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-ui-dashboard|ts-basic-service|ts-inside-payment-service|ts-seat-service | stress | ts-payment-service |
| ts1-ts-preserve-service-response-replace-body-6bfbmp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-basic-service|ts-station-service|ts-contacts-service|ts-price-service | response-replace-body | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-delay-6q57t2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-ui-dashboard|ts-assurance-service|ts-travel-service|ts-consign-price-service | response-delay | ts-route-plan-service |
| ts1-ts-seat-service-request-replace-method-4m5zmq | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | request-replace-method | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-route-plan-service|ts-ui-dashboard | response-replace-code | ts-seat-service |
| ts1-ts-security-service-response-replace-code-q2nwzg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-travel-service | response-replace-code | ts-security-service |
| ts1-ts-travel-plan-service-response-delay-zhj7r7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-travel-service|ts-basic-service | response-delay | ts-travel-plan-service |
| ts1-ts-travel-plan-service-response-replace-code-cwn86t | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-price-service|ts-travel2-service|ts-basic-service|ts-route-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-travel-service-request-replace-method-zmxkt6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-preserve-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-travel-service |
| ts1-ts-travel-service-response-replace-code-589p77 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-station-service | response-replace-code | ts-travel-service |
| ts1-ts-travel-service-response-replace-code-qzmhjf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-ui-dashboard | response-replace-code | ts-travel-service |
| ts1-ts-travel2-service-request-replace-method-qrl8t2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-travel2-service |

## Decision Notes

- Accept ARC13 over ARC12.
- ARC13 improves all headline metrics: AC@1 `+0.096343`, MRR `+0.053760`, AC@3 `+0.011955`, and AC@5 `+0.003516`, with `error=0`.
- The improvement set is broad: `180` improved_to_hit1 cases, led by response-replace-code, request-replace-method, response/request delay, partition, stress, response-abort, and request-replace-path.
- The `43` regressed_from_hit1 cases are concentrated in request-replace-method, response-replace-code, pod-failure, corrupt, and a few UI/dashboard or route-plan entry-service patterns. This is acceptable for ARC13 because top-k metrics still improve and the regression mechanism is clear: ARC13 removes ARC12's aggressive global reliability/family smoothing and endpoint boost, which helped some sparse or entry-local cases.
- General mechanism: root-specific raw evidence with ordinal semantic priorities should be the primary score; ARC reliability should act as a local topology contrast, not a global replacement weight.
