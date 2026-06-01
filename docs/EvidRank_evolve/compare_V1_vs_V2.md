# EvidenceRank Compare V1 vs V2

- Created: 2026-06-01T14:41:41+08:00
- Old: `V1`
- New: `V2`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.530239 | 0.531646 | 0.001406 |
| AC@3 | 0.778481 | 0.786920 | 0.008439 |
| AC@5 | 0.877637 | 0.886779 | 0.009142 |
| MRR | 0.679202 | 0.684448 | 0.005246 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 11 |
| rank_improved | 32 |
| rank_regressed | 27 |
| regressed_from_hit1 | 9 |
| unchanged | 1343 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts2-ts-assurance-service-pod-failure-fvnkqg | improved_to_hit1 | 31 | 1 | 30.0 | ts-assurance-service | ts-assurance-service|ts-route-plan-service|ts-seat-service|ts-basic-service|ts-travel-service | pod-failure | ts-assurance-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | improved_to_hit1 | 37 | 1 | 36.0 | ts-consign-service | ts-consign-service|ts-travel-service|ts-seat-service|ts-basic-service|ts-order-other-service | pod-failure | ts-consign-service |
| ts8-ts-food-service-pod-failure-9swgtb | improved_to_hit1 | 37 | 1 | 36.0 | ts-food-service | ts-food-service|ts-seat-service|ts-order-service|ts-ui-dashboard|ts-travel-service | pod-failure | ts-food-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | improved_to_hit1 | 38 | 1 | 37.0 | ts-consign-price-service | ts-consign-price-service|ts-preserve-service|ts-consign-service|ts-ui-dashboard|ts-seat-service | pod-failure | ts-consign-price-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | improved_to_hit1 | 43 | 1 | 42.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-order-other-service|ts-seat-service|ts-route-plan-service | pod-failure | ts-payment-service |
| ts9-ts-preserve-service-pod-failure-6w29wr | improved_to_hit1 | 44 | 1 | 43.0 | ts-preserve-service | ts-preserve-service|ts-seat-service|ts-basic-service|ts-ui-dashboard|ts-verification-code-service | pod-failure | ts-preserve-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | improved_to_hit1 | 45 | 1 | 44.0 | ts-station-food-service | ts-station-food-service|ts-travel-service|ts-food-service|ts-order-other-service|ts-basic-service | pod-failure | ts-station-food-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | improved_to_hit1 | 45 | 1 | 44.0 | ts-price-service | ts-price-service|ts-seat-service|ts-travel-service|ts-basic-service|ts-order-other-service | pod-failure | ts-price-service |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 47 | 1 | 46.0 | ts-user-service | ts-user-service|ts-ui-dashboard|ts-auth-service|ts-verification-code-service|loadgenerator | pod-failure | ts-user-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | improved_to_hit1 | 47 | 1 | 46.0 | ts-travel-service | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-seat-service | pod-failure | ts-travel-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | improved_to_hit1 | 47 | 1 | 46.0 | ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-price-service|ts-travel-plan-service|ts-seat-service | pod-failure | ts-travel2-service |
| ts0-ts-station-service-loss-hs8vrm | rank_improved | 14 | 13 | 1.0 | mysql;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | loss | ts-station-service |
| ts1-ts-route-service-corrupt-5z9zfl | rank_improved | 12 | 11 | 1.0 | mysql;ts-route-service | ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-basic-service | corrupt | ts-route-service |
| ts3-ts-route-service-corrupt-rplmkr | rank_improved | 10 | 9 | 1.0 | mysql;ts-route-service | ts-basic-service|ts-ui-dashboard|ts-auth-service|ts-verification-code-service|ts-order-service | corrupt | ts-route-service |
| ts3-ts-user-service-partition-vt7q2n | rank_improved | 6 | 5 | 1.0 | mysql;ts-user-service | ts-verification-code-service|ts-ui-dashboard|ts-auth-service|loadgenerator|ts-user-service | partition | ts-user-service |
| ts1-ts-route-service-corrupt-qlt7gn | rank_improved | 11 | 9 | 2.0 | mysql;ts-route-service | ts-ui-dashboard|ts-auth-service|ts-verification-code-service|ts-preserve-service|ts-order-other-service | corrupt | ts-route-service |
| ts2-mysql-bandwidth-2zxrzh | rank_improved | 11 | 9 | 2.0 | mysql;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | bandwidth | mysql |
| ts1-mysql-corrupt-hft465 | rank_improved | 8 | 5 | 3.0 | mysql;ts-route-service | ts-ui-dashboard|ts-auth-service|ts-verification-code-service|ts-order-service|ts-route-service | corrupt | mysql |
| ts1-mysql-loss-dfzrxw | rank_improved | 15 | 11 | 4.0 | mysql;ts-travel-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-order-service|ts-verification-code-service | loss | mysql |
| ts2-mysql-corrupt-lt5n6d | rank_improved | 17 | 13 | 4.0 | mysql;ts-contacts-service | ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-basic-service|ts-travel2-service | corrupt | mysql |
| ts0-mysql-partition-cfvlsw | rank_improved | 19 | 14 | 5.0 | mysql;ts-travel2-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-verification-code-service|ts-travel-service | partition | mysql |
| ts0-mysql-partition-fl747g | rank_improved | 16 | 11 | 5.0 | mysql;ts-price-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-verification-code-service|ts-ui-dashboard | partition | mysql |
| ts0-mysql-partition-jh4jkt | rank_improved | 14 | 9 | 5.0 | mysql;ts-train-service | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-seat-service | partition | mysql |
| ts2-mysql-bandwidth-68t494 | rank_improved | 11 | 6 | 5.0 | mysql;ts-order-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service | bandwidth | mysql |
| ts3-ts-train-service-partition-r58pxm | rank_improved | 15 | 10 | 5.0 | mysql;ts-train-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-verification-code-service | partition | ts-train-service |
| ts2-mysql-bandwidth-fws9rx | rank_improved | 18 | 12 | 6.0 | mysql;ts-travel2-service | ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-verification-code-service|ts-travel-service | bandwidth | mysql |
| ts3-mysql-partition-xgmtkl | rank_improved | 15 | 9 | 6.0 | mysql;ts-station-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | partition | mysql |
| ts3-ts-contacts-service-loss-cdzjg5 | rank_improved | 18 | 12 | 6.0 | mysql;ts-contacts-service | ts-ui-dashboard|ts-news-service|ts-seat-service|ts-basic-service|ts-travel-service | loss | ts-contacts-service |
| ts0-mysql-partition-k9q6lq | rank_improved | 16 | 9 | 7.0 | mysql;ts-train-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel2-service | partition | mysql |
| ts2-ts-consign-service-partition-xbv84t | rank_improved | 27 | 20 | 7.0 | mysql;ts-consign-service | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-order-service|ts-route-plan-service | partition | ts-consign-service |
| ts3-mysql-corrupt-wgvhdb | rank_improved | 18 | 11 | 7.0 | mysql;ts-config-service | ts-seat-service|ts-travel-service|ts-travel2-service|ts-route-service|ts-ui-dashboard | corrupt | mysql |
| ts3-mysql-partition-4hh8bj | rank_improved | 19 | 12 | 7.0 | mysql;ts-travel-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service|ts-order-service | partition | mysql |
| ts1-ts-consign-service-time-hslmgs | rank_improved | 38 | 30 | 8.0 | ts-consign-service | ts-config-service|ts-seat-service|ts-travel-service|ts-order-other-service|ts-basic-service | unknown | unknown |
| ts2-ts-train-service-loss-j2w694 | rank_improved | 17 | 9 | 8.0 | mysql;ts-train-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-preserve-service|ts-travel-plan-service | loss | ts-train-service |
| ts1-mysql-partition-gcgbzp | rank_improved | 22 | 11 | 11.0 | mysql;ts-order-service | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | partition | mysql |
| ts2-ts-consign-price-service-stress-7r95bt | rank_improved | 38 | 27 | 11.0 | ts-consign-price-service | ts-payment-service|ts-preserve-service|ts-security-service|ts-seat-service|ts-ui-dashboard | stress | ts-consign-price-service |
| ts3-ts-auth-service-return-9tmvzg | rank_improved | 13 | 2 | 11.0 | ts-auth-service | ts-verification-code-service|ts-auth-service|ts-ui-dashboard|loadgenerator|ts-travel-service | return | ts-auth-service |
| ts2-mysql-loss-4fvjb6 | rank_improved | 19 | 7 | 12.0 | mysql;ts-order-other-service | ts-preserve-service|ts-travel2-service|ts-security-service|ts-ui-dashboard|ts-travel-service | loss | mysql |
| ts2-ts-cancel-service-return-7qlbbz | rank_improved | 37 | 25 | 12.0 | ts-cancel-service | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-basic-service|ts-auth-service | return | ts-cancel-service |
| ts2-ts-order-service-loss-lp8wln | rank_improved | 20 | 6 | 14.0 | mysql;ts-order-service | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | loss | ts-order-service |

## Decision Notes

- Accept V2. The only algorithmic change is feature-level non-finite sanitization before normalization and final fusion, which is a generic observability robustness rule rather than a dataset-specific branch.
- Metric movement supports the hypothesis: AC@1, AC@3, AC@5, and MRR all improved, with no eval errors.
- `improved_to_hit1` is concentrated in `pod-failure`: 11 cases moved from deep ranks to rank 1 because valid non-NaN feature evidence was no longer discarded with the whole service row.
- `regressed_from_hit1` has 9 cases, all rank `1 -> 2`; they remain Top-3/Top-5. These are mostly request/response mutation cases where a newly restored propagated service can slightly outrank the previous root.
- Next iteration should not add a direct endpoint boost. Raw-trace endpoint symptoms need confidence gating and topology-aware propagation suppression, and `conclusion.parquet` must remain unused as evidence.
