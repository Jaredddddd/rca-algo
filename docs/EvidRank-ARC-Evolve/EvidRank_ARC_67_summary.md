# EvidRank-ARC 67 Summary

- Created: 2026-06-03T12:41:14+08:00
- Source: `ARC_67` (stored in the pre-rename snapshot `V13_SELF_LEARNED_67`)
- Algorithm: `evidencerank_arc` (equivalent pre-rename run: `evidencerank_v13`)
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.670886 |
| AC@3 | 0.925457 |
| AC@5 | 0.973980 |
| MRR | 0.801983 |
| avg_rank | 1.746132 |
| top1_miss | 468 |
| top5_miss | 37 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | request-replace-path | 39 | 0.358974 | 0.846154 | 0.974359 | 0.618162 | 1 |
| fault_type | response-replace-code | 231 | 0.372294 | 0.865801 | 0.974026 | 0.626442 | 6 |
| fault_type | response-replace-body | 51 | 0.431373 | 0.803922 | 0.941176 | 0.630906 | 3 |
| case_service | ts-basic-service | 201 | 0.442786 | 0.825871 | 0.950249 | 0.640096 | 10 |
| fault_type | response-abort | 44 | 0.477273 | 0.909091 | 0.977273 | 0.688474 | 1 |
| case_service | ts-travel2-service | 68 | 0.500000 | 0.808824 | 0.970588 | 0.674323 | 2 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.544408 | 2 |
| case_service | ts-security-service | 33 | 0.515152 | 1.000000 | 1.000000 | 0.747475 | 0 |
| fault_type | request-abort | 60 | 0.516667 | 0.850000 | 0.933333 | 0.693665 | 4 |
| time_bucket | ts9 | 23 | 0.521739 | 0.826087 | 0.956522 | 0.687440 | 1 |
| fault_type | request-replace-method | 190 | 0.531579 | 0.889474 | 0.978947 | 0.714810 | 4 |
| time_bucket | ts6 | 28 | 0.535714 | 0.785714 | 0.928571 | 0.692857 | 2 |
| fault_type | pod-failure | 24 | 0.541667 | 0.833333 | 0.875000 | 0.699658 | 3 |
| time_bucket | ts7 | 34 | 0.558824 | 0.852941 | 0.911765 | 0.711555 | 3 |
| case_service | ts-route-plan-service | 138 | 0.565217 | 0.898551 | 0.971014 | 0.736970 | 4 |
| case_service | ts-ui-dashboard | 165 | 0.581818 | 0.915152 | 0.957576 | 0.752663 | 7 |
| case_service | unknown | 26 | 0.615385 | 0.807692 | 0.923077 | 0.738797 | 2 |
| fault_type | unknown | 26 | 0.615385 | 0.807692 | 0.923077 | 0.738797 | 2 |
| time_bucket | ts1 | 179 | 0.625698 | 0.960894 | 0.983240 | 0.788523 | 3 |
| time_bucket | ts2 | 221 | 0.628959 | 0.968326 | 0.990950 | 0.788131 | 2 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-route-plan-service|ts-seat-service|loadgenerator | pod-failure | mysql |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 30 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-order-service | pod-failure | ts-travel-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-food-service|ts-travel-service|ts-config-service|ts-train-food-service|ts-order-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-seat-service|ts-ui-dashboard|loadgenerator|ts-preserve-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 19 | ts-inside-payment-service|ts-ui-dashboard|ts-order-service|ts-travel-service|ts-seat-service | return | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 16 | ts-payment-service|ts-ui-dashboard|ts-preserve-service|ts-train-food-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 13 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-order-other-service|ts-order-service | bandwidth | ts-route-plan-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 12 | ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-auth-service|ts-travel2-service | bandwidth | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-inside-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 11 | ts-travel-service|ts-security-service|ts-preserve-service|ts-order-service|ts-auth-service | unknown | unknown |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 11 | loadgenerator|ts-station-food-service|ts-seat-service|ts-travel2-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | mysql | 10 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-travel2-service | container-kill | mysql |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-food-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-route-plan-service|ts-contacts-service | response-replace-code | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 10 | ts-payment-service|ts-ui-dashboard|ts-food-service|loadgenerator|ts-basic-service | response-replace-body | ts-route-plan-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 9 | ts-order-service|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service|loadgenerator | partition | ts-seat-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 9 | ts-cancel-service|ts-preserve-service|ts-order-service|ts-food-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 9 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-travel2-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-payment-service|ts-consign-service|ts-cancel-service|ts-consign-price-service|ts-food-service | request-replace-method | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 9 | ts-payment-service|ts-inside-payment-service|ts-assurance-service|ts-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 8 | ts-train-food-service|ts-food-service|ts-seat-service|ts-order-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 8 | ts-route-plan-service|ts-security-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-seat-service|ts-travel-plan-service | bandwidth | ts-route-plan-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 8 | ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | bandwidth | ts-station-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 8 | ts-preserve-service|ts-seat-service|ts-cancel-service|ts-consign-price-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 8 | ts-consign-service|ts-food-service|ts-basic-service|loadgenerator|ts-route-plan-service | stress | ts-cancel-service |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 7 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 7 | ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-food-service|ts-seat-service | pod-failure | ts-consign-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 7 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-consign-price-service|ts-travel2-service | response-abort | ts-basic-service |

## Research Notes

- This final EvidRank-ARC baseline reaches the requested AC@1 >= 0.67 threshold without fixed per-feature prior weights.
- Remaining weak groups are mostly protocol mutation faults and cases where endpoint or infrastructure symptoms propagate to high-traffic services.
- The accepted mechanism is p95 case-local scaling with clip 3.0, self-learned feature reliability, cross-modal agreement, and retained topology degree features.
- Future no-label variants should add causality-aware constraints before trying to exceed the fixed-prior default.
