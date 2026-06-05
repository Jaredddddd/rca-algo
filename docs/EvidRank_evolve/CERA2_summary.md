# EvidenceRank CERA2 Summary

- Created: 2026-06-05T11:09:39+08:00
- Source: `CERA2`
- Algorithm: `cera`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.752461 |
| AC@3 | 0.926160 |
| AC@5 | 0.961322 |
| MRR | 0.842955 |
| avg_rank | 1.759494 |
| top1_miss | 352 |
| top5_miss | 55 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| time_bucket | ts6 | 28 | 0.428571 | 0.821429 | 0.928571 | 0.641342 | 2 |
| fault_type | pod-failure | 24 | 0.500000 | 0.791667 | 0.833333 | 0.625946 | 4 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.522321 | 2 |
| case_service | ts-seat-service | 79 | 0.531646 | 0.898734 | 0.987342 | 0.722996 | 1 |
| time_bucket | ts7 | 34 | 0.558824 | 0.794118 | 0.911765 | 0.701552 | 3 |
| case_service | ts-ui-dashboard | 165 | 0.593939 | 0.872727 | 0.939394 | 0.740200 | 10 |
| case_service | ts-travel2-service | 68 | 0.617647 | 0.926471 | 0.985294 | 0.775875 | 1 |
| case_service | ts-travel-service | 92 | 0.619565 | 0.934783 | 0.978261 | 0.770471 | 2 |
| case_service | ts-basic-service | 201 | 0.631841 | 0.855721 | 0.910448 | 0.755500 | 18 |
| time_bucket | ts9 | 23 | 0.652174 | 0.869565 | 0.913043 | 0.758454 | 2 |
| fault_type | response-abort | 44 | 0.659091 | 0.954545 | 0.977273 | 0.811959 | 1 |
| fault_type | response-replace-code | 231 | 0.666667 | 0.900433 | 0.948052 | 0.785496 | 12 |
| fault_type | response-replace-body | 51 | 0.666667 | 0.784314 | 0.921569 | 0.762169 | 4 |
| fault_type | partition | 97 | 0.670103 | 0.876289 | 0.938144 | 0.782495 | 6 |
| time_bucket | ts5 | 258 | 0.678295 | 0.883721 | 0.934109 | 0.789102 | 17 |
| fault_type | request-replace-method | 190 | 0.678947 | 0.921053 | 0.963158 | 0.804568 | 7 |
| fault_type | request-abort | 60 | 0.683333 | 0.933333 | 0.950000 | 0.809722 | 3 |
| fault_type | bandwidth | 42 | 0.690476 | 0.785714 | 0.857143 | 0.756390 | 6 |
| case_service | unknown | 26 | 0.692308 | 0.846154 | 0.884615 | 0.769830 | 3 |
| fault_type | unknown | 26 | 0.692308 | 0.846154 | 0.884615 | 0.769830 | 3 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-execute-service|ts-cancel-service | pod-failure | ts-travel-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 31 | ts-train-food-service|ts-travel-service|ts-config-service|ts-food-service|ts-station-food-service | unknown | unknown |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-verification-code-service|ts-seat-service|ts-route-plan-service | pod-failure | mysql |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 24 | ts-consign-service|ts-station-service|loadgenerator|ts-food-service|ts-basic-service | stress | ts-cancel-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 23 | ts-basic-service|ts-travel-service|ts-food-service|ts-ui-dashboard|ts-travel-plan-service | pod-failure | ts-consign-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 23 | ts-food-service|ts-train-food-service|ts-station-food-service|ts-travel-service|ts-preserve-service | container-kill | ts-food-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 23 | ts-preserve-service|ts-payment-service|ts-user-service|ts-food-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 21 | ts-inside-payment-service|ts-order-service|ts-preserve-service|ts-seat-service|ts-travel-service | return | ts-cancel-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 18 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-auth-service | bandwidth | ts-station-service |
| ts5-ts-preserve-service-partition-kfrmzn | ts-preserve-service;ts-ui-dashboard | 18 | ts-contacts-service|ts-food-service|ts-order-service|ts-consign-service|ts-travel-plan-service | partition | ts-preserve-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 17 | ts-auth-service|ts-ui-dashboard|ts-food-service|ts-travel-plan-service|loadgenerator | bandwidth | ts-basic-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 15 | ts-auth-service|ts-train-service|ts-verification-code-service|ts-food-service|ts-ui-dashboard | container-kill | mysql |
| ts2-mysql-pod-kill-xvzmxb | mysql | 15 | ts-security-service|ts-order-service|ts-auth-service|ts-preserve-service|ts-route-service | unknown | unknown |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 14 | ts-consign-service|ts-preserve-service|ts-food-service|ts-assurance-service|ts-security-service | bandwidth | ts-station-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 12 | ts-order-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-auth-service | partition | ts-seat-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 12 | ts-train-food-service|ts-food-service|ts-order-service|ts-station-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-route-plan-service|ts-food-service|ts-travel2-service|ts-travel-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-inside-payment-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 12 | ts-payment-service|ts-inside-payment-service|ts-assurance-service|ts-food-service|ts-price-service | request-abort | ts-ui-dashboard |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 11 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 11 | ts-route-plan-service|ts-travel-plan-service|ts-security-service|ts-travel2-service|ts-travel-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 11 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-travel-plan-service|ts-auth-service | bandwidth | ts-route-plan-service |
| ts6-ts-preserve-service-partition-jvzrwx | ts-preserve-service;ts-ui-dashboard | 11 | ts-food-service|ts-assurance-service|ts-basic-service|ts-seat-service|ts-order-other-service | partition | ts-preserve-service |
| ts1-ts-route-service-corrupt-qlt7gn | mysql;ts-route-service | 10 | ts-auth-service|ts-train-service|ts-consign-service|ts-inside-payment-service|ts-order-other-service | corrupt | ts-route-service |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 10 | ts-ui-dashboard|ts-food-service|ts-consign-service|ts-preserve-service|ts-travel-plan-service | partition | ts-basic-service |
| ts3-ts-route-service-corrupt-rplmkr | mysql;ts-route-service | 10 | ts-auth-service|ts-order-service|ts-user-service|ts-food-service|ts-basic-service | corrupt | ts-route-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-contacts-service|ts-travel2-service|ts-seat-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 10 | ts-preserve-service|ts-travel2-service|ts-seat-service|ts-consign-service|ts-security-service | response-replace-body | ts-travel-service |
| ts4-ts-ui-dashboard-partition-lvfxl6 | ts-food-service;ts-ui-dashboard | 9 | ts-travel-plan-service|ts-route-plan-service|ts-auth-service|ts-train-service|ts-consign-service | partition | ts-ui-dashboard |
| ts4-ts-verification-code-service-partition-nlbl25 | ts-ui-dashboard;ts-verification-code-service | 9 | ts-travel2-service|ts-auth-service|ts-order-service|ts-travel-service|ts-food-service | partition | ts-verification-code-service |

## Research Notes

- CERA2 crosses the strong CERA milestone by removing fixed role-blend constants and using only incident-derived topology density plus mutation/propagation counterfactual shares for reranking.
- The weak groups suggest a remaining generic failure mode: when propagation-heavy victims and topology-central services both carry strong symptoms, the counterfactual transfer can sharpen top-1 but may push alternate true roots out of top-3/top-5.
- Future work should add uncertainty-aware candidate preservation or multi-root posterior smoothing derived from incident geometry, without introducing service/fault/case-specific rules or hand-crafted family weights.
