# EvidenceRank ARC5 Summary

- Created: 2026-06-03T19:33:55+08:00
- Source: `ARC5`
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.728551 |
| AC@3 | 0.940225 |
| AC@5 | 0.973277 |
| MRR | 0.836412 |
| avg_rank | 1.661041 |
| top1_miss | 386 |
| top5_miss | 38 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.527536 | 2 |
| time_bucket | ts9 | 23 | 0.521739 | 0.826087 | 0.956522 | 0.701932 | 1 |
| case_service | ts-basic-service | 201 | 0.527363 | 0.875622 | 0.950249 | 0.700647 | 10 |
| fault_type | response-replace-body | 51 | 0.529412 | 0.862745 | 0.921569 | 0.715858 | 4 |
| fault_type | pod-failure | 24 | 0.541667 | 0.833333 | 0.875000 | 0.707468 | 3 |
| time_bucket | ts6 | 28 | 0.571429 | 0.785714 | 0.964286 | 0.711905 | 1 |
| time_bucket | ts7 | 34 | 0.588235 | 0.823529 | 0.911765 | 0.735294 | 3 |
| fault_type | response-replace-code | 231 | 0.588745 | 0.922078 | 0.978355 | 0.757427 | 5 |
| fault_type | request-replace-path | 39 | 0.589744 | 0.897436 | 0.974359 | 0.750641 | 1 |
| fault_type | request-replace-method | 190 | 0.594737 | 0.926316 | 0.973684 | 0.758461 | 5 |
| case_service | unknown | 26 | 0.615385 | 0.807692 | 0.923077 | 0.737651 | 2 |
| fault_type | unknown | 26 | 0.615385 | 0.807692 | 0.923077 | 0.737651 | 2 |
| fault_type | response-abort | 44 | 0.659091 | 0.909091 | 0.977273 | 0.792424 | 1 |
| case_service | ts-travel2-service | 68 | 0.661765 | 0.911765 | 0.970588 | 0.788294 | 2 |
| case_service | ts-travel-service | 92 | 0.663043 | 0.945652 | 0.989130 | 0.809239 | 1 |
| fault_type | bandwidth | 42 | 0.666667 | 0.857143 | 0.880952 | 0.775902 | 5 |
| case_service | ts-security-service | 33 | 0.666667 | 0.969697 | 1.000000 | 0.820707 | 0 |
| case_service | ts-payment-service | 12 | 0.666667 | 1.000000 | 1.000000 | 0.833333 | 0 |
| case_service | ts-consign-price-service | 9 | 0.666667 | 1.000000 | 1.000000 | 0.833333 | 0 |
| case_service | ts-route-plan-service | 138 | 0.681159 | 0.934783 | 0.971014 | 0.810406 | 4 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-food-service|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-food-service|ts-travel-service|ts-config-service|ts-order-service|ts-order-other-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-seat-service|ts-ui-dashboard|loadgenerator|ts-preserve-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 23 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-order-service|ts-assurance-service | return | ts-cancel-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 19 | ts-ui-dashboard|ts-auth-service|ts-seat-service|ts-order-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 16 | ts-payment-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-seat-service | response-replace-code | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 15 | ts-consign-service|ts-food-service|ts-basic-service|ts-route-plan-service|loadgenerator | stress | ts-cancel-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 13 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-food-service|ts-auth-service | bandwidth | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 12 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service | bandwidth | ts-station-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-food-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 11 | ts-payment-service|ts-inside-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 11 | loadgenerator|ts-seat-service|ts-station-food-service|ts-travel2-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | mysql | 10 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-travel2-service | container-kill | mysql |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-payment-service|ts-food-service|ts-consign-service|ts-seat-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 9 | ts-order-service|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service|loadgenerator | partition | ts-seat-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-travel-service|ts-security-service|ts-order-service|ts-auth-service|ts-preserve-service | unknown | unknown |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 9 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-travel2-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 9 | ts-payment-service|ts-inside-payment-service|ts-food-service|ts-assurance-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 8 | ts-train-food-service|ts-food-service|ts-travel-service|ts-seat-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 8 | ts-route-plan-service|ts-security-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-seat-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 8 | ts-preserve-service|ts-cancel-service|ts-order-service|ts-seat-service|ts-food-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 8 | ts-cancel-service|ts-preserve-service|ts-consign-price-service|ts-seat-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts5-ts-ui-dashboard-request-replace-method-dxffln | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-basic-service|loadgenerator|ts-security-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|ts-food-service|ts-payment-service|ts-basic-service|loadgenerator | response-replace-body | ts-route-plan-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 8 | ts-order-service|ts-seat-service|ts-basic-service|ts-contacts-service|ts-consign-service | request-abort | ts-ui-dashboard |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 7 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-travel2-service-response-replace-body-ljvb7g | ts-route-service;ts-travel2-service | 7 | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-food-service|ts-ui-dashboard | response-replace-body | ts-travel2-service |

## Research Notes

- ARC5 adds a final top-neighbor pairwise contrast after ARC3 family consensus. A trace-adjacent service can receive score from a higher-scored neighbor only when it has stronger mutation-family evidence and that neighbor has stronger propagation-family evidence.
- The mechanism is self-supervised and case-local: pair strength comes from current score gap, mutation excess, propagation excess, and raw trace direction; no labels, injection metadata, historical outputs, service names, fault names, or `FEATURE_WEIGHTS` are used.
- The main gain is in top-1 disambiguation when ARC3 places a propagation-heavy neighbor just above a mutation-heavier adjacent service.
- The main remaining risk is propagation-shaped true roots: loss, corrupt, request-delay, bandwidth, and partition-like cases can be hurt when propagation evidence is causal rather than victim-only.
