# EvidenceRank FEATURE_SUBSET_MIN7_FULL Summary

- Created: 2026-06-14T23:10:10+08:00
- Source: `FEATURE_SUBSET_MIN7_FULL`
- Algorithm: `crest_feature_min7`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.800281 |
| AC@3 | 0.946554 |
| AC@5 | 0.971167 |
| MRR | 0.877743 |
| avg_rank | 1.609705 |
| top1_miss | 284 |
| top5_miss | 41 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.250000 | 0.458333 | 0.541667 | 0.395320 | 11 |
| case_service | ts-cancel-service | 4 | 0.250000 | 0.500000 | 0.500000 | 0.393621 | 2 |
| case_service | ts-ui-dashboard | 165 | 0.533333 | 0.884848 | 0.963636 | 0.724947 | 6 |
| time_bucket | ts7 | 34 | 0.647059 | 0.852941 | 0.911765 | 0.770378 | 3 |
| case_service | unknown | 26 | 0.653846 | 0.846154 | 0.846154 | 0.746051 | 4 |
| fault_type | unknown | 26 | 0.653846 | 0.846154 | 0.846154 | 0.746051 | 4 |
| case_service | ts-consign-price-service | 9 | 0.666667 | 1.000000 | 1.000000 | 0.796296 | 0 |
| case_service | ts-travel2-service | 68 | 0.676471 | 0.955882 | 1.000000 | 0.812500 | 0 |
| case_service | ts-route-service | 23 | 0.695652 | 0.869565 | 0.913043 | 0.791408 | 2 |
| time_bucket | ts9 | 23 | 0.695652 | 0.913043 | 0.956522 | 0.814182 | 1 |
| fault_type | request-abort | 60 | 0.700000 | 0.900000 | 0.950000 | 0.818849 | 3 |
| fault_type | request-replace-method | 190 | 0.710526 | 0.910526 | 0.973684 | 0.820362 | 5 |
| case_service | ts-seat-service | 79 | 0.721519 | 0.936709 | 0.987342 | 0.840506 | 1 |
| time_bucket | ts6 | 28 | 0.750000 | 0.928571 | 1.000000 | 0.847619 | 0 |
| case_service | ts-verification-code-service | 4 | 0.750000 | 1.000000 | 1.000000 | 0.875000 | 0 |
| time_bucket | ts5 | 258 | 0.759690 | 0.949612 | 0.980620 | 0.857567 | 5 |
| time_bucket | ts8 | 25 | 0.760000 | 0.920000 | 0.960000 | 0.852667 | 1 |
| fault_type | bandwidth | 42 | 0.761905 | 0.833333 | 0.880952 | 0.816185 | 5 |
| fault_type | response-abort | 44 | 0.772727 | 0.931818 | 1.000000 | 0.856818 | 0 |
| fault_type | response-replace-code | 231 | 0.774892 | 0.978355 | 0.991342 | 0.876641 | 2 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 34 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-user-service|ts-auth-service | pod-failure | ts-travel-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 31 | ts-config-service|ts-travel-service|ts-station-service|ts-basic-service|ts-order-service | unknown | unknown |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | ts-auth-service|ts-travel-service|ts-order-other-service|ts-order-service|ts-basic-service | pod-failure | mysql |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 29 | ts-inside-payment-service|ts-order-service|ts-station-service|ts-travel-service|ts-basic-service | return | ts-cancel-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 28 | ts-basic-service|ts-travel-service|ts-train-service|ts-ui-dashboard|ts-food-service | pod-failure | ts-consign-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 25 | ts-consign-service|ts-station-service|ts-basic-service|ts-route-service|ts-order-other-service | stress | ts-cancel-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 22 | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|ts-order-service | container-kill | mysql |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 22 | ts-ui-dashboard|ts-order-other-service|ts-order-service|ts-train-service|ts-user-service | bandwidth | ts-route-plan-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 18 | ts-auth-service|ts-order-service|ts-security-service|ts-travel-service|ts-preserve-service | unknown | unknown |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 17 | ts-ui-dashboard|ts-assurance-service|ts-consign-service|ts-food-service|ts-order-service | bandwidth | ts-basic-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 17 | ts-food-service|ts-seat-service|ts-train-food-service|ts-travel-service|ts-order-other-service | container-kill | ts-food-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 17 | ts-travel-service|ts-route-service|ts-travel-plan-service|ts-route-plan-service|ts-train-service | bandwidth | ts-station-service |
| ts0-ts-user-service-pod-failure-b44c7f | ts-user-service | 16 | ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-basic-service|ts-order-service | pod-failure | ts-user-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 16 | ts-station-service|ts-route-service|ts-basic-service|ts-price-service|ts-train-service | pod-failure | ts-assurance-service |
| ts8-ts-food-service-pod-failure-9swgtb | ts-food-service | 15 | ts-station-service|ts-route-service|ts-order-service|ts-basic-service|ts-contacts-service | pod-failure | ts-food-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 14 | loadgenerator|ts-train-food-service|ts-order-service|ts-basic-service|ts-station-service | request-abort | ts-ui-dashboard |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 13 | ts-inside-payment-service|ts-order-service|ts-order-other-service|ts-station-service|ts-basic-service | pod-failure | ts-payment-service |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 12 | loadgenerator|ts-assurance-service|ts-order-other-service|ts-station-service|ts-order-service | partition | ts-basic-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | ts-food-service;ts-ui-dashboard | 11 | ts-price-service|ts-route-service|ts-station-service|loadgenerator|ts-order-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-station-food-service-pod-failure-td2qj4 | ts-station-food-service | 10 | ts-food-service|ts-travel-service|ts-basic-service|ts-train-food-service|ts-route-service | pod-failure | ts-station-food-service |
| ts3-ts-ui-dashboard-request-replace-method-7lstrz | ts-assurance-service;ts-ui-dashboard | 10 | ts-route-service|ts-basic-service|ts-price-service|ts-station-service|ts-contacts-service | request-replace-method | ts-ui-dashboard |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 10 | ts-basic-service|ts-travel2-service|ts-travel-plan-service|ts-route-service|ts-travel-service | pod-failure | ts-price-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | ts-travel-service | 9 | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-travel2-service|ts-order-service | pod-failure | ts-travel-service |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-inside-payment-service|ts-payment-service|ts-travel-service|ts-order-service|ts-station-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 9 | ts-preserve-service|ts-food-service|ts-payment-service|ts-train-food-service|ts-contacts-service | response-replace-code | ts-basic-service |
| ts5-ts-preserve-service-partition-kfrmzn | ts-preserve-service;ts-ui-dashboard | 8 | ts-contacts-service|ts-order-service|ts-price-service|ts-route-service|ts-basic-service | partition | ts-preserve-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 7 | ts-consign-service|ts-order-service|ts-travel-service|ts-price-service|ts-basic-service | unknown | unknown |
| ts1-ts-route-service-corrupt-qlt7gn | mysql;ts-route-service | 7 | ts-order-other-service|ts-train-service|ts-ui-dashboard|ts-auth-service|ts-user-service | corrupt | ts-route-service |
| ts3-ts-auth-service-return-9tmvzg | ts-auth-service | 7 | ts-verification-code-service|ts-ui-dashboard|ts-user-service|loadgenerator|ts-order-service | return | ts-auth-service |
| ts3-ts-route-service-corrupt-rplmkr | mysql;ts-route-service | 7 | ts-order-service|ts-auth-service|ts-basic-service|ts-train-service|ts-ui-dashboard | corrupt | ts-route-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
