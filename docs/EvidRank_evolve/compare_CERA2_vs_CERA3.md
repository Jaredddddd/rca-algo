# EvidenceRank Compare CERA2 vs CERA3

- Created: 2026-06-05T14:38:09+08:00
- Old: `CERA2`
- New: `CERA3`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.752461 | 0.850211 | 0.097750 |
| AC@3 | 0.926160 | 0.950774 | 0.024613 |
| AC@5 | 0.961322 | 0.976090 | 0.014768 |
| MRR | 0.842955 | 0.904032 | 0.061077 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 191 |
| rank_improved | 69 |
| rank_regressed | 36 |
| regressed_from_hit1 | 52 |
| unchanged | 1074 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-partition-jh4jkt | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-basic-service | partition | mysql |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-station-service|ts-preserve-service|ts-travel-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-request-replace-method-gqn7nd | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-station-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-lq4ncj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-r727qm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-station-service|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-seat-service-request-replace-method-dchngw | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard | request-replace-method | ts-seat-service |
| ts0-ts-seat-service-response-replace-body-vx8tdz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-order-other-service|ts-travel-plan-service|ts-route-plan-service | response-replace-body | ts-seat-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-seat-service |
| ts0-ts-travel-service-request-abort-g9mc2t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-travel2-service | request-abort | ts-travel-service |
| ts0-ts-travel-service-request-delay-z8wzcp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-basic-service|ts-seat-service|ts-train-food-service|ts-config-service | request-delay | ts-travel-service |
| ts0-ts-travel2-service-request-replace-method-dhgqc8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-travel2-service |
| ts0-ts-travel2-service-response-replace-code-9ntz74 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-basic-service|ts-route-plan-service|ts-station-service|ts-price-service | response-replace-code | ts-travel2-service |
| ts0-ts-ui-dashboard-response-delay-nqtssr | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-assurance-service|ts-travel-plan-service | response-delay | ts-ui-dashboard |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-station-service|ts-price-service|ts-preserve-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-request-replace-method-2dz98x | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-station-service|ts-price-service|ts-travel2-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-b2ftxt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-station-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-consign-service-stress-2q7pns | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-travel-service|ts-seat-service|ts-route-plan-service|ts-consign-price-service | stress | ts-consign-service |
| ts1-ts-food-service-request-abort-5ggl5l | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-train-food-service|ts-travel-service|ts-seat-service|ts-travel2-service | request-abort | ts-food-service |
| ts1-ts-route-plan-service-response-replace-body-5s6gc9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-travel-service | response-replace-body | ts-route-plan-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-twx8qg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-order-other-service | response-replace-code | ts-seat-service |
| ts1-ts-travel-plan-service-response-replace-code-6mlrxc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-travel-service-response-replace-body-vzcxrp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-basic-service|ts-price-service|ts-travel-plan-service | response-replace-body | ts-travel-service |
| ts2-mysql-corrupt-lt5n6d | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-ui-dashboard|ts-auth-service|ts-preserve-service|ts-basic-service | corrupt | mysql |
| ts2-mysql-delay-d427wn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|ts-basic-service|ts-travel-plan-service|ts-verification-code-service | delay | mysql |
| ts2-mysql-loss-4fvjb6 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-preserve-service|ts-security-service|ts-travel2-service|ts-ui-dashboard | loss | mysql |
| ts2-ts-consign-service-container-kill-fftcrp | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-consign-price-service|ts-ui-dashboard|ts-auth-service|ts-travel-service | container-kill | ts-consign-service |
| ts2-ts-food-service-response-abort-5k6q44 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|ts-train-food-service|ts-ui-dashboard|ts-auth-service|loadgenerator | response-abort | ts-food-service |
| ts2-ts-order-service-container-kill-sr295f | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-ui-dashboard|ts-food-service|ts-inside-payment-service|ts-payment-service | container-kill | ts-order-service |
| ts2-ts-route-plan-service-request-replace-method-dq56rf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-auth-service | request-replace-method | ts-route-plan-service |
| ts2-ts-seat-service-request-abort-qk6ntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | request-abort | ts-seat-service |
| ts2-ts-seat-service-request-delay-jg97tv | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-consign-service|ts-ui-dashboard|ts-travel-service|ts-preserve-service | request-delay | ts-seat-service |
| ts2-ts-seat-service-response-delay-hxp6h6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-config-service|ts-travel2-service|ts-ui-dashboard | response-delay | ts-seat-service |
| ts2-ts-seat-service-response-replace-code-kttq2h | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service | response-replace-code | ts-seat-service |
| ts2-ts-security-service-response-replace-code-zvh8k2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-food-service | response-replace-code | ts-security-service |
| ts2-ts-travel-plan-service-response-abort-f6dgj2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-basic-service|ts-route-service|ts-train-service | response-abort | ts-travel-plan-service |
| ts2-ts-travel-service-request-replace-method-5snzk5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-basic-service|ts-food-service|ts-order-service|ts-station-service | request-replace-method | ts-travel-service |
| ts2-ts-travel-service-response-abort-jd66zv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-route-service|ts-ui-dashboard | response-abort | ts-travel-service |
| ts2-ts-travel-service-response-replace-code-8c25qw | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-basic-service|ts-route-service|ts-station-service | response-replace-code | ts-travel-service |
| ts2-ts-travel-service-response-replace-code-w4bgvh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-route-service|ts-station-service|ts-basic-service | response-replace-code | ts-travel-service |

## Decision Notes

- Accept CERA3 as the current standalone CERA version. It raises AC@1 from `0.752461` to `0.850211`, MRR from `0.842955` to `0.904032`, AC@3 from `0.926160` to `0.950774`, and AC@5 from `0.961322` to `0.976090`, with full eval `error == 0`.
- The general mechanism is ordinal causal evidence role alignment: raw incident signals are scored by semantic evidence tiers whose numeric energy is synthesized from tier ordering, then endpoint support and parent context are derived from current incident geometry rather than hand-tuned constants.
- The 52 `regressed_from_hit1` cases concentrate in `request-replace-method`, `pod-failure`, `response-replace-code`, and route-plan/dashboard/basic-service patterns. This is an acceptable trade-off because CERA3 gains 191 `improved_to_hit1` cases and improves all aggregate metrics.
- The next research target should be generic infrastructure-local evidence for `pod-failure`/`bandwidth`, not restoring legacy endpoint gate constants or adding service/fault-specific exceptions.
