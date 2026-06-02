# EvidenceRank V20 Summary

- Created: 2026-06-02T23:38:55+08:00
- Source: `V20`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.789030 |
| AC@3 | 0.940225 |
| AC@5 | 0.976793 |
| MRR | 0.869097 |
| avg_rank | 1.560478 |
| top1_miss | 300 |
| top5_miss | 33 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.333333 | 0.750000 | 0.875000 | 0.555115 | 3 |
| time_bucket | ts8 | 25 | 0.360000 | 0.880000 | 0.960000 | 0.631111 | 1 |
| time_bucket | ts6 | 28 | 0.500000 | 0.714286 | 0.964286 | 0.664286 | 1 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.750000 | 0.571429 | 1 |
| time_bucket | ts7 | 34 | 0.558824 | 0.794118 | 0.852941 | 0.702696 | 5 |
| time_bucket | ts9 | 23 | 0.565217 | 0.913043 | 0.956522 | 0.732609 | 1 |
| fault_type | request-abort | 60 | 0.616667 | 0.916667 | 0.933333 | 0.764282 | 4 |
| fault_type | response-replace-body | 51 | 0.627451 | 0.862745 | 0.960784 | 0.749673 | 2 |
| case_service | ts-basic-service | 201 | 0.641791 | 0.900498 | 0.980100 | 0.774413 | 4 |
| fault_type | bandwidth | 42 | 0.642857 | 0.833333 | 0.857143 | 0.748554 | 6 |
| case_service | ts-ui-dashboard | 165 | 0.666667 | 0.860606 | 0.945455 | 0.786473 | 9 |
| case_service | ts-order-other-service | 27 | 0.666667 | 1.000000 | 1.000000 | 0.820988 | 0 |
| case_service | unknown | 26 | 0.692308 | 0.846154 | 0.884615 | 0.781197 | 3 |
| fault_type | unknown | 26 | 0.692308 | 0.846154 | 0.884615 | 0.781197 | 3 |
| case_service | ts-station-service | 20 | 0.700000 | 0.900000 | 0.900000 | 0.805060 | 2 |
| fault_type | request-replace-method | 190 | 0.710526 | 0.884211 | 0.973684 | 0.814985 | 5 |
| case_service | ts-travel2-service | 68 | 0.720588 | 0.926471 | 1.000000 | 0.827451 | 0 |
| fault_type | response-replace-code | 231 | 0.727273 | 0.909091 | 0.982684 | 0.829208 | 4 |
| case_service | ts-route-plan-service | 138 | 0.746377 | 0.920290 | 0.963768 | 0.840795 | 5 |
| time_bucket | ts4 | 274 | 0.748175 | 0.934307 | 0.970803 | 0.847085 | 8 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-travel-service|ts-order-other-service|ts-seat-service|ts-food-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 28 | ts-inside-payment-service|ts-order-service|ts-travel-service|ts-station-service|ts-ui-dashboard | return | ts-cancel-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 28 | ts-auth-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-route-plan-service | pod-failure | mysql |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 27 | ts-ui-dashboard|ts-auth-service|ts-train-food-service|ts-station-food-service|ts-security-service | pod-failure | ts-travel-plan-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 27 | ts-food-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-seat-service | container-kill | ts-food-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 16 | ts-order-service|ts-seat-service|ts-food-service|loadgenerator|ts-basic-service | request-abort | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 16 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-preserve-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 14 | ts-ui-dashboard|loadgenerator|ts-order-service|ts-seat-service|ts-auth-service | bandwidth | ts-route-plan-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 12 | ts-consign-service|ts-payment-service|ts-order-service|ts-verification-code-service|ts-travel-service | unknown | unknown |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-body | ts-basic-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 10 | ts-ui-dashboard|loadgenerator|ts-order-service|ts-contacts-service|ts-seat-service | bandwidth | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 10 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|loadgenerator|ts-verification-code-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-auth-service|ts-travel-service|ts-security-service|ts-order-service|ts-preserve-service | unknown | unknown |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 9 | ts-payment-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-consign-price-service | request-replace-method | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 9 | loadgenerator|ts-station-food-service|ts-travel2-service|ts-seat-service|ts-travel-plan-service | request-abort | ts-ui-dashboard |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-payment-service|ts-consign-price-service|ts-consign-service|ts-station-food-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 8 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service | bandwidth | ts-station-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 8 | ts-order-service|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service|ts-inside-payment-service | partition | ts-seat-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | ts-food-service;ts-ui-dashboard | 8 | ts-order-service|loadgenerator|ts-seat-service|ts-basic-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-basic-service|ts-verification-code-service|ts-food-service | bandwidth | ts-route-plan-service |
| ts4-ts-seat-service-bandwidth-k2bwt2 | ts-config-service;ts-seat-service | 8 | ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | bandwidth | ts-seat-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-station-food-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 7 | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|loadgenerator | bandwidth | ts-station-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 7 | ts-ui-dashboard|ts-consign-price-service|loadgenerator|ts-travel2-service|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 6 | ts-train-service|ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts1-ts-route-service-corrupt-5z9zfl | mysql;ts-route-service | 6 | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|loadgenerator | corrupt | ts-route-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 6 | ts-basic-service|ts-consign-service|ts-seat-service|ts-train-service|ts-order-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-ui-dashboard-request-replace-method-dxffln | ts-travel-plan-service;ts-ui-dashboard | 6 | ts-payment-service|ts-consign-service|ts-contacts-service|loadgenerator|ts-security-service | request-replace-method | ts-ui-dashboard |
| ts6-ts-route-plan-service-response-replace-code-9pfgvr | ts-route-plan-service;ts-route-service | 6 | ts-payment-service|ts-ui-dashboard|ts-consign-service|ts-consign-price-service|ts-security-service | response-replace-code | ts-route-plan-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
