# EvidenceRank FW_PRIORITY_POWER2_TIER Summary

- Created: 2026-06-03T23:47:04+08:00
- Source: `current`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.756681 |
| AC@3 | 0.941632 |
| AC@5 | 0.973980 |
| MRR | 0.851812 |
| avg_rank | 1.616034 |
| top1_miss | 346 |
| top5_miss | 37 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| time_bucket | ts8 | 25 | 0.400000 | 0.920000 | 0.960000 | 0.653636 | 1 |
| fault_type | response-replace-body | 51 | 0.470588 | 0.823529 | 0.960784 | 0.672589 | 2 |
| time_bucket | ts6 | 28 | 0.500000 | 0.785714 | 0.892857 | 0.669189 | 3 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.750000 | 0.750000 | 0.634259 | 1 |
| fault_type | pod-failure | 24 | 0.541667 | 0.916667 | 0.916667 | 0.704365 | 2 |
| case_service | ts-basic-service | 201 | 0.542289 | 0.885572 | 0.970149 | 0.718286 | 6 |
| time_bucket | ts7 | 34 | 0.558824 | 0.823529 | 0.882353 | 0.709537 | 4 |
| time_bucket | ts9 | 23 | 0.565217 | 0.869565 | 0.956522 | 0.725808 | 1 |
| fault_type | request-abort | 60 | 0.583333 | 0.916667 | 0.933333 | 0.749014 | 4 |
| case_service | ts-ui-dashboard | 165 | 0.593939 | 0.860606 | 0.927273 | 0.740224 | 12 |
| fault_type | response-replace-code | 231 | 0.614719 | 0.913420 | 0.974026 | 0.766463 | 6 |
| fault_type | bandwidth | 42 | 0.642857 | 0.833333 | 0.857143 | 0.747978 | 6 |
| fault_type | request-replace-method | 190 | 0.657895 | 0.878947 | 0.957895 | 0.782333 | 8 |
| case_service | ts-consign-price-service | 9 | 0.666667 | 0.888889 | 0.888889 | 0.796296 | 1 |
| case_service | ts-travel2-service | 68 | 0.676471 | 0.941176 | 1.000000 | 0.809069 | 0 |
| fault_type | request-replace-path | 39 | 0.692308 | 0.923077 | 0.974359 | 0.810684 | 1 |
| case_service | ts-station-service | 20 | 0.700000 | 0.900000 | 0.900000 | 0.804365 | 2 |
| case_service | ts-route-plan-service | 138 | 0.702899 | 0.920290 | 0.963768 | 0.817958 | 5 |
| case_service | ts-order-other-service | 27 | 0.703704 | 1.000000 | 1.000000 | 0.839506 | 0 |
| fault_type | response-abort | 44 | 0.727273 | 0.954545 | 1.000000 | 0.834848 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-travel-service|ts-order-other-service|ts-seat-service|ts-order-service | unknown | unknown |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 28 | ts-ui-dashboard|ts-auth-service|ts-train-food-service|ts-verification-code-service|ts-station-food-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 28 | ts-auth-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-route-plan-service | pod-failure | mysql |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 27 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-station-service|ts-order-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 27 | ts-food-service|ts-ui-dashboard|ts-seat-service|loadgenerator|ts-travel-service | container-kill | ts-food-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 18 | ts-order-service|ts-seat-service|ts-food-service|ts-train-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 17 | ts-payment-service|ts-ui-dashboard|ts-train-food-service|ts-preserve-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 13 | ts-consign-service|ts-payment-service|ts-verification-code-service|ts-order-service|ts-seat-service | unknown | unknown |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 13 | ts-payment-service|ts-inside-payment-service|ts-verification-code-service|loadgenerator|ts-assurance-service | request-abort | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 12 | ts-ui-dashboard|ts-seat-service|ts-order-service|ts-auth-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 11 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-consign-price-service|ts-basic-service | response-replace-body | ts-route-plan-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 11 | ts-payment-service|ts-consign-price-service|ts-consign-service|ts-station-food-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | ts-food-service;ts-ui-dashboard | 10 | ts-order-service|ts-seat-service|ts-basic-service|ts-travel-service|loadgenerator | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 10 | ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-order-service|ts-seat-service | bandwidth | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 10 | loadgenerator|ts-station-food-service|ts-travel2-service|ts-seat-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 9 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service | bandwidth | ts-station-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 9 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-order-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 9 | ts-ui-dashboard|ts-verification-code-service|ts-basic-service|ts-seat-service|ts-travel-plan-service | bandwidth | ts-route-plan-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 9 | ts-basic-service|ts-consign-service|ts-seat-service|ts-order-service|ts-train-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 9 | ts-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts6-ts-basic-service-request-replace-method-4qzglm | ts-basic-service;ts-train-service | 9 | ts-cancel-service|ts-consign-service|ts-verification-code-service|ts-seat-service|ts-order-service | request-replace-method | ts-basic-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 8 | ts-consign-price-service|ts-order-service|ts-ui-dashboard|ts-travel-plan-service|ts-inside-payment-service | partition | ts-seat-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 8 | ts-auth-service|ts-travel-service|ts-security-service|ts-preserve-service|ts-order-service | unknown | unknown |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 8 | ts-order-service|ts-basic-service|ts-consign-service|loadgenerator|ts-verification-code-service | request-abort | ts-ui-dashboard |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-station-food-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | ts-travel-plan-service;ts-ui-dashboard | 7 | ts-inside-payment-service|ts-travel-service|ts-payment-service|ts-seat-service|ts-order-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 7 | ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-route-service | bandwidth | ts-station-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 7 | ts-travel2-service|ts-seat-service|ts-basic-service|ts-travel-service|ts-order-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 7 | ts-consign-price-service|ts-ui-dashboard|ts-travel2-service|ts-seat-service|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts6-ts-route-plan-service-response-replace-code-9pfgvr | ts-route-plan-service;ts-route-service | 7 | ts-payment-service|ts-consign-price-service|ts-consign-service|ts-security-service|ts-ui-dashboard | response-replace-code | ts-route-plan-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
