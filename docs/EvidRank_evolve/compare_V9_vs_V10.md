# EvidenceRank Compare V9 vs V10

- Created: 2026-06-02T11:23:11+08:00
- Old: `V9`
- New: `V10`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.794655 | 0.802391 | 0.007736 |
| AC@3 | 0.941632 | 0.943741 | 0.002110 |
| AC@5 | 0.975387 | 0.975387 | 0.000000 |
| MRR | 0.871089 | 0.875103 | 0.004013 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 16 |
| rank_improved | 22 |
| rank_regressed | 15 |
| regressed_from_hit1 | 5 |
| unchanged | 1364 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-seat-service-response-abort-nggfmq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-order-service|ts-payment-service | response-abort | ts-seat-service |
| ts2-ts-basic-service-response-replace-body-hk6w9p | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-station-service|ts-travel2-service|ts-price-service|ts-train-service | response-replace-body | ts-basic-service |
| ts2-ts-order-service-stress-8vtw2p | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | stress | ts-order-service |
| ts2-ts-route-plan-service-return-xw84fv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-consign-service|ts-station-food-service|ts-ui-dashboard|ts-basic-service | return | ts-route-plan-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-travel-service|ts-basic-service|ts-seat-service|ts-ui-dashboard | pod-failure | ts-consign-service |
| ts4-ts-basic-service-response-replace-code-2nw8nx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-service | response-replace-code | ts-basic-service |
| ts4-ts-inside-payment-service-exception-p5mf2x | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-cancel-service|ts-seat-service|ts-order-service|ts-consign-service | exception | ts-inside-payment-service |
| ts4-ts-order-service-stress-q255tz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-cancel-service|ts-seat-service|ts-ui-dashboard|ts-route-plan-service | stress | ts-order-service |
| ts4-ts-seat-service-request-replace-method-bvdt9b | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-travel-service | request-replace-method | ts-seat-service |
| ts4-ts-security-service-request-replace-method-l8vq9b | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-seat-service | request-replace-method | ts-security-service |
| ts5-ts-preserve-service-stress-845w52 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service | ts-preserve-service|ts-consign-price-service|ts-ui-dashboard|ts-station-food-service|ts-order-service | stress | ts-preserve-service |
| ts5-ts-route-plan-service-response-delay-gsbt9h | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-cancel-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | response-delay | ts-route-plan-service |
| ts5-ts-travel-service-exception-98b2cj | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-cancel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | exception | ts-travel-service |
| ts7-ts-travel-service-response-abort-tx5942 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-consign-service | response-abort | ts-travel-service |
| ts9-ts-preserve-service-pod-failure-6w29wr | improved_to_hit1 | 3 | 1 | 2.0 | ts-preserve-service | ts-preserve-service|loadgenerator|ts-ui-dashboard|ts-verification-code-service|ts-order-service | pod-failure | ts-preserve-service |
| ts4-ts-basic-service-request-replace-method-hpv2qg | improved_to_hit1 | 4 | 1 | 3.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-order-service|ts-ui-dashboard|ts-payment-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts0-ts-seat-service-pod-failure-c87xdg | rank_improved | 5 | 4 | 1.0 | ts-seat-service | ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-seat-service|ts-travel-plan-service | pod-failure | ts-seat-service |
| ts0-ts-travel-plan-service-time-rjdx4x | rank_improved | 4 | 3 | 1.0 | ts-travel-plan-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-order-service|ts-seat-service | unknown | unknown |
| ts2-ts-assurance-service-pod-failure-fvnkqg | rank_improved | 7 | 6 | 1.0 | ts-assurance-service | ts-basic-service|ts-station-service|ts-travel-service|ts-route-plan-service|ts-seat-service | pod-failure | ts-assurance-service |
| ts2-ts-consign-price-service-stress-7r95bt | rank_improved | 4 | 3 | 1.0 | ts-consign-price-service | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-preserve-service|ts-security-service | stress | ts-consign-price-service |
| ts2-ts-order-other-service-stress-ln9mfl | rank_improved | 4 | 3 | 1.0 | ts-order-other-service | ts-security-service|ts-seat-service|ts-order-other-service|ts-execute-service|ts-travel2-service | stress | ts-order-other-service |
| ts3-ts-basic-service-partition-w5hbjw | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-travel-service | ts-delivery-service|ts-basic-service|ts-food-service|ts-verification-code-service|ts-travel-service | partition | ts-basic-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | rank_improved | 15 | 14 | 1.0 | ts-payment-service | ts-inside-payment-service|ts-order-service|ts-order-other-service|ts-seat-service|ts-basic-service | pod-failure | ts-payment-service |
| ts4-ts-basic-service-response-replace-code-7tlb8z | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-price-service | ts-route-plan-service|ts-travel2-service|ts-ui-dashboard|ts-basic-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-seat-service-response-replace-body-p2bzc7 | rank_improved | 3 | 2 | 1.0 | ts-config-service;ts-seat-service | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-ui-dashboard|ts-travel2-service | response-replace-body | ts-seat-service |
| ts6-ts-basic-service-response-replace-code-s7bcv7 | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-price-service | ts-seat-service|ts-payment-service|ts-basic-service|ts-inside-payment-service|ts-order-service | response-replace-code | ts-basic-service |
| ts6-ts-travel-service-request-replace-path-6brwd9 | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-travel-service | ts-preserve-service|ts-order-service|ts-travel-service|ts-price-service|ts-ui-dashboard | request-replace-path | ts-travel-service |
| ts6-ts-ui-dashboard-response-replace-code-tgfbsg | rank_improved | 7 | 6 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-payment-service|ts-station-food-service|ts-travel-service|ts-seat-service|ts-route-plan-service | response-replace-code | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-delay-t55rlr | rank_improved | 6 | 5 | 1.0 | ts-route-plan-service;ts-travel-service | ts-station-food-service|ts-inside-payment-service|ts-ui-dashboard|ts-order-service|ts-travel-service | response-delay | ts-route-plan-service |
| ts7-ts-route-plan-service-response-replace-code-bhpv8l | rank_improved | 4 | 3 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-ui-dashboard|ts-inside-payment-service|ts-route-plan-service|loadgenerator|ts-travel-plan-service | response-replace-code | ts-route-plan-service |
| ts8-ts-food-service-pod-failure-9swgtb | rank_improved | 3 | 2 | 1.0 | ts-food-service | ts-order-service|ts-food-service|ts-ui-dashboard|ts-basic-service|ts-station-service | pod-failure | ts-food-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | rank_improved | 10 | 9 | 1.0 | ts-train-service;ts-ui-dashboard | ts-payment-service|ts-inside-payment-service|loadgenerator|ts-verification-code-service|ts-assurance-service | request-abort | ts-ui-dashboard |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | rank_improved | 11 | 9 | 2.0 | ts-order-other-service;ts-ui-dashboard | loadgenerator|ts-station-food-service|ts-travel2-service|ts-seat-service|ts-travel-plan-service | request-abort | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | rank_improved | 12 | 10 | 2.0 | ts-route-plan-service;ts-travel-service | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | rank_improved | 9 | 7 | 2.0 | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-station-food-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts3-mysql-pod-failure-58qts5 | rank_improved | 31 | 28 | 3.0 | mysql | ts-auth-service|ts-travel-service|ts-seat-service|loadgenerator|ts-order-other-service | pod-failure | mysql |
| ts5-ts-cancel-service-stress-d8xbsn | rank_improved | 15 | 11 | 4.0 | ts-cancel-service | ts-consign-service|ts-food-service|ts-route-plan-service|ts-auth-service|ts-basic-service | stress | ts-cancel-service |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | rank_improved | 35 | 27 | 8.0 | ts-travel-plan-service | ts-auth-service|ts-ui-dashboard|ts-train-food-service|ts-station-food-service|ts-security-service | pod-failure | ts-travel-plan-service |
| ts1-ts-seat-service-partition-gtmt4k | rank_regressed | 4 | 8 | -4.0 | ts-seat-service;ts-travel2-service | ts-order-service|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service|ts-travel-service | partition | ts-seat-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | rank_regressed | 12 | 14 | -2.0 | ts-route-plan-service;ts-travel-plan-service | ts-ui-dashboard|loadgenerator|ts-order-service|ts-seat-service|ts-auth-service | bandwidth | ts-route-plan-service |

## Decision Notes

- Accept V10. It raises AC@1 from 0.794655 to 0.802391, MRR from 0.871089 to 0.875103, and AC@3 from 0.941632 to 0.943741 while keeping AC@5 unchanged at 0.975387.
- The accepted mechanism is service-local availability evidence: when trace/metric counts drop sharply from a stable normal-period baseline, the affected service may be the local root rather than only a downstream victim. This complements V9 endpoint-shift evidence without using labels, datapack IDs, service names, or fault names in the algorithm.
- There are 5 `regressed_from_hit1` cases. They are all small-margin request/response method or delay cases where count drop can over-reward a nearby high-traffic propagation service. The regressions are outweighed by 16 `improved_to_hit1` cases and no AC@5 loss, but future iterations should suppress global or neighborhood-wide traffic contraction before adding more drop weight.
- Do not further increase endpoint/drop strength in the next round. The next smallest general step is topology-aware local-vs-neighbor drop contrast for residual pod-failure, bandwidth, request-abort, and infrastructure-root misses.
