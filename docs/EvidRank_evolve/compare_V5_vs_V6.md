# EvidenceRank Compare V5 vs V6

- Created: 2026-06-02T01:53:47+08:00
- Old: `V5`
- New: `V6`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.699015 | 0.766526 | 0.067511 |
| AC@3 | 0.902954 | 0.922644 | 0.019691 |
| AC@5 | 0.963432 | 0.961322 | -0.002110 |
| MRR | 0.810334 | 0.849078 | 0.038744 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 142 |
| rank_improved | 68 |
| rank_regressed | 76 |
| regressed_from_hit1 | 46 |
| unchanged | 1090 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-loss-hfrvkl | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-basic-service | loss | mysql |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-travel2-service|ts-station-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-request-replace-method-rmcj6l | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts0-ts-seat-service-response-delay-fjqtmh | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-preserve-service|ts-travel-service|ts-travel2-service | response-delay | ts-seat-service |
| ts0-ts-security-service-request-replace-method-j6gpxx | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-cancel-service|ts-order-service|ts-ui-dashboard | request-replace-method | ts-security-service |
| ts0-ts-security-service-request-replace-method-m5g977 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-travel-service | request-replace-method | ts-security-service |
| ts0-ts-security-service-response-replace-code-fbsfls | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-ui-dashboard|ts-order-other-service | response-replace-code | ts-security-service |
| ts0-ts-travel-plan-service-request-delay-lf5tnb | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service | request-delay | ts-travel-plan-service |
| ts0-ts-travel-service-response-replace-body-bb9m88 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | response-replace-body | ts-travel-service |
| ts0-ts-ui-dashboard-request-delay-s2z79x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-auth-service|ts-basic-service | request-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-sfz5t9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-travel-plan-service|ts-consign-price-service|ts-route-plan-service|ts-seat-service|ts-travel2-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-basic-service-request-delay-9w85fg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-verification-code-service|ts-travel-service|ts-travel2-service | request-delay | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-lfsjf6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-travel2-service|ts-train-service | response-replace-code | ts-basic-service |
| ts1-ts-config-service-delay-vlf2nr | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel2-service | delay | ts-config-service |
| ts1-ts-security-service-response-replace-code-q2nwzg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-travel-service | response-replace-code | ts-security-service |
| ts1-ts-travel-plan-service-response-delay-zhj7r7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-travel-service|ts-auth-service | response-delay | ts-travel-plan-service |
| ts1-ts-travel-service-response-abort-mqhzdf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-route-plan-service|ts-basic-service|ts-station-service | response-abort | ts-travel-service |
| ts1-ts-travel-service-response-replace-body-vzcxrp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-preserve-service | response-replace-body | ts-travel-service |
| ts1-ts-travel-service-response-replace-code-589p77 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service | response-replace-code | ts-travel-service |
| ts1-ts-travel-service-response-replace-code-gl7qrs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service | response-replace-code | ts-travel-service |
| ts1-ts-ui-dashboard-response-replace-code-24nh7m | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-ui-dashboard|ts-assurance-service|ts-consign-price-service|loadgenerator|ts-auth-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-5cjdfh | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-station-service | response-replace-code | ts-ui-dashboard |
| ts2-mysql-bandwidth-2zxrzh | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-basic-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | bandwidth | mysql |
| ts2-mysql-corrupt-lt5n6d | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-ui-dashboard|loadgenerator|ts-seat-service|ts-order-service | corrupt | mysql |
| ts2-mysql-delay-d427wn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|ts-basic-service|ts-seat-service|ts-verification-code-service | delay | mysql |
| ts2-mysql-loss-4fvjb6 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-preserve-service|ts-travel2-service|ts-security-service|ts-ui-dashboard | loss | mysql |
| ts2-ts-route-plan-service-request-replace-method-dq56rf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-verification-code-service|ts-auth-service | request-replace-method | ts-route-plan-service |
| ts2-ts-security-service-request-replace-method-kfks5v | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-ui-dashboard|ts-verification-code-service | request-replace-method | ts-security-service |
| ts2-ts-security-service-response-replace-code-kj8mxw | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-verification-code-service|ts-ui-dashboard|ts-order-service | response-replace-code | ts-security-service |
| ts2-ts-security-service-response-replace-code-zvh8k2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-seat-service | response-replace-code | ts-security-service |
| ts2-ts-travel-service-request-delay-5hk27g | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-food-service|ts-order-service|ts-seat-service|ts-route-plan-service | request-delay | ts-travel-service |
| ts2-ts-travel-service-response-replace-code-w4bgvh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service | response-replace-code | ts-travel-service |
| ts2-ts-travel2-service-request-abort-g79sj7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-travel-service | request-abort | ts-travel2-service |
| ts2-ts-ui-dashboard-response-abort-hnvckb | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service;ts-ui-dashboard | ts-travel2-service|ts-seat-service|ts-basic-service|ts-order-other-service|ts-config-service | response-abort | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-delay-f24lmd | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|loadgenerator|ts-verification-code-service|ts-travel-service | response-delay | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-g6ls9b | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-order-service|ts-seat-service|loadgenerator|ts-ui-dashboard|ts-route-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-qzfj27 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-consign-service|ts-seat-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts3-mysql-bandwidth-5xvc22 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-travel-plan-service|ts-route-service|ts-food-service|ts-ui-dashboard | bandwidth | mysql |
| ts3-ts-basic-service-request-replace-method-crz6qj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-travel2-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-request-replace-method-pjwm42 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | request-replace-method | ts-basic-service |

## Decision Notes

- Accept V6 as the current default EvidenceRank version.
- The main improvement is broad and not case-specific: `trace_count_rise_shift` helps when the root service's abnormal request volume rises, and `trace_self_duration_relative_shift` helps separate caller-local work from child-span latency propagation. Together they add `142` new Top-1 hits while `46` cases regress from Top-1.
- The main risk is also generic: request-volume and self-duration signals can over-rank services that are busy because of propagation or fan-out. This causes `14` Top-5 losses versus `11` Top-5 gains, so `AC@5` drops slightly by `0.002110`.
- The regression pattern is acceptable for V6 because `AC@1`, `AC@3`, and `MRR` improve materially, full evaluation has `error=0`, and the Top-5 loss is small and explainable. The next round should focus on a topology/cross-modal confidence gate for traffic-rise rather than increasing raw trace weights.
