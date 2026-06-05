# EvidenceRank Compare CERA1 vs CERA2

- Created: 2026-06-05T11:09:49+08:00
- Old: `CERA1`
- New: `CERA2`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.691280 | 0.752461 | 0.061181 |
| AC@3 | 0.933193 | 0.926160 | -0.007032 |
| AC@5 | 0.966245 | 0.961322 | -0.004923 |
| MRR | 0.814367 | 0.842955 | 0.028588 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 188 |
| rank_improved | 74 |
| rank_regressed | 87 |
| regressed_from_hit1 | 101 |
| unchanged | 972 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-loss-hfrvkl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-security-service | ts-security-service|ts-preserve-service|ts-contacts-service|ts-user-service|ts-basic-service | loss | mysql |
| ts0-mysql-partition-mphlhs | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-security-service | ts-security-service|ts-preserve-service|ts-assurance-service|ts-food-service|ts-travel-plan-service | partition | mysql |
| ts0-ts-basic-service-request-delay-d5jvr6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-preserve-service | request-delay | ts-basic-service |
| ts0-ts-basic-service-request-replace-method-z2nlcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-request-replace-path-8q599t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-station-service|ts-travel2-service|ts-route-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts0-ts-consign-price-service-stress-t67vtg | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-basic-service|ts-travel-service|ts-price-service | stress | ts-consign-price-service |
| ts0-ts-contacts-service-pod-failure-j42hd8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service | ts-contacts-service|ts-ui-dashboard|ts-auth-service|loadgenerator|ts-consign-service | pod-failure | ts-contacts-service |
| ts0-ts-preserve-service-response-abort-mj9pbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-travel-plan-service|ts-food-service|ts-auth-service|ts-ui-dashboard | response-abort | ts-preserve-service |
| ts0-ts-preserve-service-response-replace-code-kvkzkr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-food-service|ts-contacts-service|ts-travel-plan-service|ts-auth-service | response-replace-code | ts-preserve-service |
| ts0-ts-route-plan-service-request-replace-method-lrzhl6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-auth-service|ts-travel2-service|ts-seat-service | request-replace-method | ts-route-plan-service |
| ts0-ts-seat-service-response-replace-code-gqm7pj | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-travel-plan-service|ts-basic-service | response-replace-code | ts-seat-service |
| ts0-ts-security-service-request-replace-method-j6gpxx | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-cancel-service|ts-order-other-service | request-replace-method | ts-security-service |
| ts0-ts-security-service-request-replace-method-m5g977 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-food-service|ts-assurance-service | request-replace-method | ts-security-service |
| ts0-ts-security-service-response-replace-code-47m5nd | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-auth-service|ts-order-service|ts-food-service | response-replace-code | ts-security-service |
| ts0-ts-security-service-response-replace-code-f2529z | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-auth-service|ts-food-service|ts-assurance-service | response-replace-code | ts-security-service |
| ts0-ts-security-service-response-replace-code-fbsfls | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-contacts-service|ts-food-service | response-replace-code | ts-security-service |
| ts0-ts-travel-plan-service-time-rjdx4x | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard|ts-auth-service | unknown | unknown |
| ts0-ts-travel2-service-response-replace-body-rmn797 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-auth-service | response-replace-body | ts-travel2-service |
| ts0-ts-ui-dashboard-request-replace-method-7bx8qb | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-auth-service|loadgenerator|ts-ui-dashboard|ts-verification-code-service|ts-food-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-delay-n5c9hs | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-travel-plan-service|ts-preserve-service | response-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-user-service|ts-travel-plan-service|ts-consign-service|ts-consign-price-service | response-replace-code | ts-ui-dashboard |
| ts0-ts-user-service-partition-77jfkk | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-user-service | ts-user-service|ts-ui-dashboard|ts-auth-service|ts-preserve-service|ts-travel-plan-service | partition | ts-user-service |
| ts1-ts-auth-service-request-replace-method-mrrl9f | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-verification-code-service|ts-travel-service|ts-order-other-service|ts-order-service | request-replace-method | ts-auth-service |
| ts1-ts-basic-service-request-replace-method-hz96t6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-preserve-service|ts-station-service|ts-travel-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-request-replace-method-kqkjgj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-2vvxvm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-station-service|ts-travel-service|ts-travel2-service|ts-preserve-service | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-lfsjf6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-security-service|ts-preserve-service|ts-station-service|ts-travel2-service | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-pqlzs2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-inside-payment-service-stress-6qq6f6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-travel-plan-service|ts-consign-service|ts-auth-service | stress | ts-inside-payment-service |
| ts1-ts-inside-payment-service-stress-n6mttx | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-cancel-service|ts-consign-service|ts-auth-service | stress | ts-inside-payment-service |
| ts1-ts-payment-service-stress-5778hg | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-basic-service|ts-ui-dashboard|ts-auth-service | stress | ts-payment-service |
| ts1-ts-payment-service-stress-k7stf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-cancel-service|ts-ui-dashboard|ts-travel-plan-service | stress | ts-payment-service |
| ts1-ts-preserve-service-request-replace-method-xmhsbb | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-contacts-service|ts-consign-service|ts-auth-service|ts-security-service | request-replace-method | ts-preserve-service |
| ts1-ts-preserve-service-response-replace-body-6bfbmp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-contacts-service|ts-food-service|ts-assurance-service|ts-auth-service | response-replace-body | ts-preserve-service |
| ts1-ts-preserve-service-response-replace-code-bndht9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-food-service|ts-travel-plan-service|ts-contacts-service|ts-auth-service | response-replace-code | ts-preserve-service |
| ts1-ts-preserve-service-response-replace-code-wpdr2x | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-basic-service|ts-contacts-service | response-replace-code | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-train-service|ts-contacts-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-code-lmr4bp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-preserve-service | response-replace-code | ts-route-plan-service |
| ts1-ts-security-service-response-replace-code-q2nwzg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-auth-service|ts-order-service|ts-food-service | response-replace-code | ts-security-service |
| ts1-ts-station-service-pod-failure-fn44tf | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-basic-service|ts-route-plan-service|ts-travel2-service|ts-travel-service | pod-failure | ts-station-service |

## Decision Notes

- Accept CERA2 as the current standalone CERA version. It raises AC@1 from `0.691280` to `0.752461` and MRR from `0.814367` to `0.842955`, with full eval `error == 0`.
- The accepted mechanism is not a hand-crafted weighted sum: CERA2 uses unweighted robust family burden, derives parent-context strength from trace graph density, and derives explain-away transfer from current score excess multiplied by relative mutation and propagation shares.
- The trade-off is a small AC@3/AC@5 regression: `AC@3 -0.007032`, `AC@5 -0.004923`. The `regressed_from_hit1` cases concentrate in `partition`, `loss`, dashboard, seat, and basic-service patterns, consistent with over-sharpening in propagation-ambiguous incidents.
- Next iteration should preserve CERA2's no-handcrafted-weight constraint and add an incident-derived uncertainty or multi-root preservation mechanism to recover candidate recall.
