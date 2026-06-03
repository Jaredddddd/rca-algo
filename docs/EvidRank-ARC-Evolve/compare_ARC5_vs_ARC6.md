# EvidenceRank Compare ARC5 vs ARC6

- Created: 2026-06-03T20:28:49+08:00
- Old: `ARC5`
- New: `ARC6`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.728551 | 0.728551 | 0.000000 |
| AC@3 | 0.940225 | 0.943741 | 0.003516 |
| AC@5 | 0.973277 | 0.973277 | 0.000000 |
| MRR | 0.836412 | 0.836841 | 0.000429 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 5 |
| rank_improved | 16 |
| rank_regressed | 9 |
| regressed_from_hit1 | 5 |
| unchanged | 1387 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-ui-dashboard-response-delay-nqtssr | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-assurance-service|ts-preserve-service|ts-basic-service | response-delay | ts-ui-dashboard |
| ts1-ts-travel-plan-service-request-replace-path-zdh4tb | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-seat-service|ts-basic-service | request-replace-path | ts-travel-plan-service |
| ts2-ts-auth-service-stress-lq54b9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-assurance-service|ts-consign-service|ts-seat-service | stress | ts-auth-service |
| ts2-ts-food-service-bandwidth-b5qvk5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|ts-assurance-service|ts-seat-service|ts-verification-code-service | bandwidth | ts-food-service |
| ts4-ts-ui-dashboard-loss-gvqmxw | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|ts-assurance-service|ts-seat-service|loadgenerator|ts-basic-service | loss | ts-ui-dashboard |
| ts2-mysql-pod-kill-xvzmxb | rank_improved | 9 | 8 | 1.0 | mysql | ts-travel-service|ts-order-service|ts-security-service|ts-auth-service|ts-preserve-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | rank_improved | 23 | 22 | 1.0 | ts-cancel-service | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-order-service|ts-assurance-service | return | ts-cancel-service |
| ts3-ts-basic-service-partition-w5hbjw | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-travel-service | ts-ui-dashboard|ts-food-service|ts-basic-service|loadgenerator|ts-order-service | partition | ts-basic-service |
| ts3-ts-travel-plan-service-request-delay-b8pn5w | rank_improved | 3 | 2 | 1.0 | ts-train-service;ts-travel-plan-service | ts-ui-dashboard|ts-travel-plan-service|loadgenerator|ts-basic-service|ts-travel-service | request-delay | ts-travel-plan-service |
| ts4-ts-basic-service-request-abort-jr6f2j | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-preserve-service|ts-basic-service|ts-seat-service|ts-consign-service|ts-travel-service | request-abort | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | rank_improved | 11 | 10 | 1.0 | ts-basic-service;ts-price-service | ts-preserve-service|ts-route-plan-service|ts-ui-dashboard|ts-food-service|ts-travel-plan-service | response-replace-body | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | rank_improved | 12 | 11 | 1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service | bandwidth | ts-station-service |
| ts5-mysql-corrupt-k6788t | rank_improved | 4 | 3 | 1.0 | mysql;ts-order-service | ts-station-service|ts-seat-service|ts-order-service|ts-ui-dashboard|ts-food-service | corrupt | mysql |
| ts5-mysql-loss-q42phw | rank_improved | 3 | 2 | 1.0 | mysql;ts-auth-service | ts-ui-dashboard|ts-auth-service|loadgenerator|ts-order-service|ts-seat-service | loss | mysql |
| ts5-ts-train-food-service-mysql-rswcbh | rank_improved | 4 | 3 | 1.0 | mysql;ts-train-food-service | ts-basic-service|loadgenerator|ts-train-food-service|ts-cancel-service|ts-payment-service | unknown | unknown |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | rank_improved | 5 | 4 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-ui-dashboard|ts-consign-price-service|ts-preserve-service|ts-travel-plan-service|ts-travel2-service | response-replace-code | ts-travel-plan-service |
| ts5-ts-travel-service-partition-vr6f55 | rank_improved | 3 | 2 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-consign-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-seat-service | partition | ts-travel-service |
| ts6-ts-travel2-service-request-delay-bnhhtc | rank_improved | 3 | 2 | 1.0 | ts-seat-service;ts-travel2-service | ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-travel-service | request-delay | ts-travel2-service |
| ts6-ts-ui-dashboard-request-abort-k6bvd5 | rank_improved | 4 | 3 | 1.0 | ts-travel2-service;ts-ui-dashboard | ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|loadgenerator|ts-seat-service | request-abort | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-code-bhpv8l | rank_improved | 4 | 3 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-inside-payment-service|ts-assurance-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | response-replace-code | ts-route-plan-service |
| ts0-mysql-container-kill-9t6n24 | rank_improved | 10 | 8 | 2.0 | mysql | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-travel2-service | container-kill | mysql |
| ts3-ts-consign-service-pod-failure-8cb7mp | rank_regressed | 6 | 8 | -2.0 | ts-consign-service | ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-food-service|ts-seat-service | pod-failure | ts-consign-service |
| ts2-ts-ui-dashboard-request-replace-method-jrt2mv | rank_regressed | 2 | 3 | -1.0 | ts-train-service;ts-ui-dashboard | ts-seat-service|ts-order-service|ts-train-service|ts-ui-dashboard|loadgenerator | request-replace-method | ts-ui-dashboard |
| ts3-ts-payment-service-pod-failure-fnlgp6 | rank_regressed | 2 | 3 | -1.0 | ts-payment-service | ts-inside-payment-service|ts-order-other-service|ts-payment-service|ts-order-service|ts-basic-service | pod-failure | ts-payment-service |
| ts3-ts-route-plan-service-response-replace-code-vqsdbr | rank_regressed | 2 | 3 | -1.0 | ts-route-plan-service;ts-travel2-service | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-basic-service|ts-auth-service | response-replace-code | ts-route-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | rank_regressed | 16 | 17 | -1.0 | ts-basic-service;ts-price-service | ts-payment-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-seat-service | response-replace-code | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | rank_regressed | 11 | 12 | -1.0 | ts-order-other-service;ts-ui-dashboard | loadgenerator|ts-seat-service|ts-station-food-service|ts-travel2-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts5-ts-ui-dashboard-request-replace-method-dxffln | rank_regressed | 8 | 9 | -1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service|ts-basic-service|loadgenerator|ts-security-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts6-ts-basic-service-response-replace-code-s7bcv7 | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-price-service | ts-seat-service|ts-payment-service|ts-basic-service|ts-price-service|ts-food-service | response-replace-code | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | rank_regressed | 8 | 9 | -1.0 | ts-route-plan-service;ts-travel-service | ts-ui-dashboard|ts-food-service|ts-payment-service|loadgenerator|ts-basic-service | response-replace-body | ts-route-plan-service |
| ts1-ts-inside-payment-service-stress-6qq6f6 | regressed_from_hit1 | 1 | 2 | -1.0 | ts-inside-payment-service | ts-ui-dashboard|ts-inside-payment-service|ts-food-service|ts-route-plan-service|ts-travel2-service | stress | ts-inside-payment-service |
| ts1-ts-train-service-pod-failure-5qwqdz | regressed_from_hit1 | 1 | 2 | -1.0 | ts-train-service | ts-basic-service|ts-train-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-train-service |
| ts2-ts-consign-service-bandwidth-x9qdzm | regressed_from_hit1 | 1 | 2 | -1.0 | mysql;ts-consign-service | ts-ui-dashboard|ts-consign-service|ts-seat-service|ts-payment-service|ts-preserve-service | bandwidth | ts-consign-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | regressed_from_hit1 | 1 | 2 | -1.0 | ts-travel2-service | ts-ui-dashboard|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-price-service | pod-failure | ts-travel2-service |
| ts3-ts-route-service-return-9l76ss | regressed_from_hit1 | 1 | 2 | -1.0 | ts-route-service | ts-consign-service|ts-route-service|ts-food-service|ts-travel-service|ts-station-food-service | return | ts-route-service |

## Decision Notes

- Accept ARC6. It removes the fixed reliability meta-weight constants while preserving AC@1 and AC@5, and improves MRR by `+0.000429` and AC@3 by `+0.003516`.
- The mechanism that improved the ranking is case-local PCA calibration over reliability diagnostics: support, concentration, contrast, top gap, and agreement become diagnostic components whose combination is learned from the current case rather than fixed by constants.
- `regressed_from_hit1` cases are balanced by the same number of `improved_to_hit1` cases. The regressions cluster around sparse pod-failure, bandwidth, stress, and return cases where a small PCA shift can move traffic-heavy neighbors above localized roots.
- Full removal of all remaining hand-designed structure is rejected for now based on offline ablation; endpoint gate, robust clipping, and mutation/propagation role priors should remain explicit inductive biases until learned replacements outperform them.
