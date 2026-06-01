# EvidenceRank Compare V4 vs V5

- Created: 2026-06-01T21:02:12+08:00
- Old: `V4`
- New: `V5`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.571730 | 0.699015 | 0.127286 |
| AC@3 | 0.791139 | 0.902954 | 0.111814 |
| AC@5 | 0.888889 | 0.963432 | 0.074543 |
| MRR | 0.706323 | 0.810334 | 0.104011 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 218 |
| rank_improved | 159 |
| rank_regressed | 28 |
| regressed_from_hit1 | 37 |
| unchanged | 980 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-abort-5dlq8r | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts0-ts-basic-service-request-abort-924pr2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-payment-service|ts-travel-service|ts-preserve-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts0-ts-basic-service-request-replace-path-8q599t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-train-service | request-replace-path | ts-basic-service |
| ts0-ts-basic-service-response-replace-body-pwrcvx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard | response-replace-body | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-mh6sjz | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-preserve-service-request-replace-method-48zkx2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-basic-service|ts-ui-dashboard|ts-security-service|ts-travel-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-request-replace-method-mbmqzz | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-seat-service|ts-security-service | request-replace-method | ts-preserve-service |
| ts0-ts-preserve-service-response-abort-mj9pbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-security-service | response-abort | ts-preserve-service |
| ts0-ts-route-plan-service-request-abort-7rfdzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-basic-service|ts-travel2-service | request-abort | ts-route-plan-service |
| ts0-ts-route-plan-service-request-replace-path-7v499h | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-payment-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service | request-replace-path | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-lnggrn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts0-ts-seat-service-response-abort-nggfmq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-payment-service|ts-route-plan-service|ts-travel-plan-service | response-abort | ts-seat-service |
| ts0-ts-travel-plan-service-request-replace-path-dnlz4g | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-payment-service|ts-route-plan-service|ts-travel-service|ts-seat-service | request-replace-path | ts-travel-plan-service |
| ts0-ts-travel-plan-service-response-replace-code-7ps8tm | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-travel-service|ts-route-plan-service|ts-basic-service|ts-travel2-service | response-replace-code | ts-travel-plan-service |
| ts0-ts-travel2-service-response-replace-code-9ntz74 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-seat-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service | response-replace-code | ts-travel2-service |
| ts1-ts-auth-service-request-replace-method-mqrzv4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-order-service | request-replace-method | ts-auth-service |
| ts1-ts-basic-service-request-replace-method-kqkjgj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-request-replace-path-z65h6q | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-path | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-2vvxvm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-preserve-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-order-other-service-loss-hrc6n6 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | loss | ts-order-other-service |
| ts1-ts-preserve-service-request-abort-x7w9vv | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-security-service|ts-ui-dashboard|ts-contacts-service|ts-station-food-service | request-abort | ts-preserve-service |
| ts1-ts-preserve-service-response-replace-code-bndht9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-travel-service|ts-basic-service | response-replace-code | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-contacts-service|ts-travel2-service|ts-travel-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-code-lmr4bp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts1-ts-seat-service-response-replace-body-hvd8x2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | response-replace-body | ts-seat-service |
| ts1-ts-travel-plan-service-response-abort-5s79p6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-seat-service|ts-travel2-service|ts-travel-service | response-abort | ts-travel-plan-service |
| ts1-ts-travel-service-request-replace-method-zmxkt6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-preserve-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-travel-service |
| ts1-ts-travel2-service-request-replace-method-qrl8t2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-ui-dashboard | request-replace-method | ts-travel2-service |
| ts1-ts-travel2-service-response-replace-code-swdpv2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service | response-replace-code | ts-travel2-service |
| ts1-ts-ui-dashboard-response-replace-code-pkkx65 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-price-service|loadgenerator|ts-seat-service|ts-basic-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-xstkwf | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|ts-travel-service|ts-auth-service|ts-travel2-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-auth-service-response-replace-code-dfhzs7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-seat-service | response-replace-code | ts-auth-service |
| ts2-ts-basic-service-request-replace-method-xqcmcx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel2-service|ts-preserve-service|ts-travel-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts2-ts-basic-service-response-replace-body-4xzdq7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-cancel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | response-replace-body | ts-basic-service |
| ts2-ts-consign-service-delay-k5d7zl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-verification-code-service|ts-seat-service|ts-inside-payment-service | delay | ts-consign-service |
| ts2-ts-food-service-request-abort-29w9xm | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|ts-order-other-service|ts-seat-service|ts-travel-service | request-abort | ts-food-service |
| ts2-ts-food-service-request-replace-method-nfkxm7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-train-food-service | request-replace-method | ts-food-service |
| ts2-ts-food-service-request-replace-method-z2sbdz | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|ts-seat-service|ts-travel-plan-service|ts-basic-service | request-replace-method | ts-food-service |
| ts2-ts-food-service-response-abort-5k6q44 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-seat-service | response-abort | ts-food-service |
| ts2-ts-preserve-service-request-abort-g2z7bt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-travel2-service|ts-basic-service|ts-seat-service|ts-verification-code-service | request-abort | ts-preserve-service |

## Decision Notes

- Accept V5. It improves AC@1 by `+0.127286`, MRR by `+0.104011`, AC@3 by `+0.111814`, and AC@5 by `+0.074543`, with zero eval errors.
- General mechanism: raw trace endpoint/status distribution residuals provide local, high-confidence evidence when service-level count/duration/log evidence is dominated by propagated traffic. The feature is computed from raw traces only and does not use labels, injection metadata, `conclusion.parquet`, datapack IDs, service-name branches, or fault-name branches.
- `improved_to_hit1` has 218 cases, led by response-code, request-method, response-abort, request-path, request-abort, response-body, partition, bandwidth, and delay-like cases.
- `regressed_from_hit1` has 37 cases. All remain within Top-5, with max new best rank 4. The regressions are mostly pod-failure, request-replace-method, partition, and response-replace-body cases where another endpoint/status-heavy service overtakes the prior root.
- Residual risk: 28 additional rank-regressed cases, 10 of which move outside Top-5. The next iteration should inspect those before increasing status weight or adding another dominant HTTP feature.
