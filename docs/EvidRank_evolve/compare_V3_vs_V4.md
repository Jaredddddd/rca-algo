# EvidenceRank Compare V3 vs V4

- Created: 2026-06-01T15:42:07+08:00
- Old: `V3`
- New: `V4`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.559072 | 0.571730 | 0.012658 |
| AC@3 | 0.789030 | 0.791139 | 0.002110 |
| AC@5 | 0.888186 | 0.888889 | 0.000703 |
| MRR | 0.698007 | 0.706323 | 0.008316 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 19 |
| rank_improved | 60 |
| rank_regressed | 31 |
| regressed_from_hit1 | 1 |
| unchanged | 1311 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-preserve-service-response-replace-code-kvkzkr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-security-service|ts-travel-service | response-replace-code | ts-preserve-service |
| ts1-ts-basic-service-response-replace-code-ft59pl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-travel-plan-service-request-replace-method-5vh2md | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-travel2-service|ts-seat-service | request-replace-method | ts-travel-plan-service |
| ts1-ts-ui-dashboard-response-delay-mhcfcl | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-verification-code-service | ts-ui-dashboard|ts-order-service|ts-travel-service|ts-basic-service|ts-seat-service | response-delay | ts-ui-dashboard |
| ts2-ts-auth-service-response-replace-code-zb5np6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-voucher-service | response-replace-code | ts-auth-service |
| ts2-ts-basic-service-response-replace-code-fmb55x | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-station-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts2-ts-preserve-service-request-replace-method-nsz4x4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-verification-code-service|ts-seat-service | request-replace-method | ts-preserve-service |
| ts3-ts-basic-service-request-replace-method-4css6n | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-preserve-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts3-ts-food-service-response-replace-body-mn5pkz | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-auth-service | response-replace-body | ts-food-service |
| ts3-ts-travel-plan-service-request-delay-b8pn5w | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-travel-service|ts-basic-service | request-delay | ts-travel-plan-service |
| ts4-ts-basic-service-corrupt-trd2kh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service|ts-travel2-service | corrupt | ts-basic-service |
| ts4-ts-travel-plan-service-response-replace-code-cts4xg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-seat-service|ts-order-service|ts-ui-dashboard|ts-route-plan-service|ts-verification-code-service | response-replace-code | ts-travel-plan-service |
| ts4-ts-travel-service-partition-w7gd8j | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service|ts-consign-service | partition | ts-travel-service |
| ts5-mysql-corrupt-k6788t | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-service | ts-order-service|ts-station-service|ts-seat-service|ts-ui-dashboard|ts-preserve-service | corrupt | mysql |
| ts5-ts-basic-service-request-delay-4cwcs6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-order-service|ts-seat-service | request-delay | ts-basic-service |
| ts5-ts-basic-service-response-delay-m48s7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-travel-service|ts-travel-plan-service | response-delay | ts-basic-service |
| ts5-ts-preserve-service-response-replace-code-qww8tw | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-order-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-preserve-service |
| ts5-ts-train-food-service-bandwidth-wbjdkv | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|ts-ui-dashboard|ts-seat-service|ts-order-service|ts-travel-service | bandwidth | ts-train-food-service |
| ts5-ts-travel-plan-service-request-replace-method-hkczvz | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-order-service|ts-basic-service | request-replace-method | ts-travel-plan-service |
| ts0-mysql-loss-hfrvkl | rank_improved | 4 | 3 | 1.0 | mysql;ts-security-service | ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-seat-service|ts-basic-service | loss | mysql |
| ts0-ts-basic-service-request-replace-method-z2nlcm | rank_improved | 7 | 6 | 1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-lmnjw7 | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-route-service | ts-travel-service|ts-basic-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-r727qm | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-route-service | ts-travel-service|ts-ui-dashboard|ts-basic-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-station-service-loss-hs8vrm | rank_improved | 9 | 8 | 1.0 | mysql;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service | loss | ts-station-service |
| ts0-ts-travel-plan-service-request-delay-lf5tnb | rank_improved | 3 | 2 | 1.0 | ts-train-service;ts-travel-plan-service | ts-preserve-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-order-service | request-delay | ts-travel-plan-service |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | rank_improved | 6 | 5 | 1.0 | ts-order-service;ts-ui-dashboard | ts-cancel-service|ts-consign-price-service|ts-seat-service|ts-travel-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts1-mysql-bandwidth-s7srkn | rank_improved | 8 | 7 | 1.0 | mysql;ts-travel-service | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-food-service|ts-seat-service | bandwidth | mysql |
| ts1-ts-basic-service-request-replace-method-2b57wf | rank_improved | 12 | 11 | 1.0 | ts-basic-service;ts-price-service | ts-travel-service|ts-ui-dashboard|ts-preserve-service|ts-station-food-service|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-5pdcrx | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-basic-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-security-service-response-replace-code-q2nwzg | rank_improved | 3 | 2 | 1.0 | ts-order-other-service;ts-security-service | ts-preserve-service|ts-security-service|ts-ui-dashboard|ts-seat-service|ts-travel-service | response-replace-code | ts-security-service |
| ts1-ts-travel2-service-request-replace-method-s99vbn | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard|ts-order-service | request-replace-method | ts-travel2-service |
| ts2-mysql-partition-5zrq5z | rank_improved | 16 | 15 | 1.0 | mysql;ts-contacts-service | ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-travel-service|ts-order-service | partition | mysql |
| ts2-ts-basic-service-response-abort-jl47fg | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-route-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-travel-plan-service|ts-route-service | response-abort | ts-basic-service |
| ts2-ts-order-other-service-stress-ln9mfl | rank_improved | 5 | 4 | 1.0 | ts-order-other-service | ts-seat-service|ts-security-service|ts-travel2-service|ts-order-other-service|ts-execute-service | stress | ts-order-other-service |
| ts2-ts-preserve-service-response-replace-code-pbnw6x | rank_improved | 3 | 2 | 1.0 | ts-order-service;ts-preserve-service | ts-ui-dashboard|ts-preserve-service|ts-consign-service|ts-basic-service|ts-verification-code-service | response-replace-code | ts-preserve-service |
| ts2-ts-route-plan-service-request-replace-method-dq56rf | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-verification-code-service|ts-auth-service | request-replace-method | ts-route-plan-service |
| ts2-ts-security-service-response-replace-code-kj8mxw | rank_improved | 4 | 3 | 1.0 | ts-order-service;ts-security-service | ts-preserve-service|ts-verification-code-service|ts-security-service|ts-ui-dashboard|ts-seat-service | response-replace-code | ts-security-service |
| ts2-ts-travel-service-bandwidth-f9fkg7 | rank_improved | 11 | 10 | 1.0 | mysql;ts-travel-service | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-auth-service|ts-order-service | bandwidth | ts-travel-service |
| ts3-ts-basic-service-request-abort-j5qblh | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-travel-service|ts-basic-service|ts-seat-service|ts-preserve-service|ts-travel2-service | request-abort | ts-basic-service |
| ts3-ts-basic-service-request-replace-method-ljqz6g | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-preserve-service|ts-basic-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-basic-service |

## Decision Notes

- Accept V4. It improves AC@1, MRR, AC@3, and AC@5 with zero eval errors.
- General mechanism: replacing the uniform topology degree penalty with a weak upstream-to-callee context term is a more direction-aware topology rule. It lets caller-observed symptoms provide small support to the callee without making topology dominate service-local evidence.
- `improved_to_hit1` has 19 cases and `rank_improved` has 60 cases, mostly request/response mutation cases plus a few corrupt/partition/bandwidth cases.
- `regressed_from_hit1` has only one case, `ts4-ts-ui-dashboard-response-replace-code-lk7q57`, which moves from rank 1 to rank 2 and remains within Top-5.
- Next iteration should look beyond scalar topology and reconstruct endpoint-level symptoms from raw traces/logs; `conclusion.parquet` remains prohibited as an input.
