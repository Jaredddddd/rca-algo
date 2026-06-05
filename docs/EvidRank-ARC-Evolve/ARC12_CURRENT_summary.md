# EvidenceRank ARC12_CURRENT Summary

- Created: 2026-06-05T12:30:52+08:00
- Source: `ARC12_CURRENT`
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.734880 |
| AC@3 | 0.936006 |
| AC@5 | 0.971871 |
| MRR | 0.839508 |
| avg_rank | 1.652602 |
| top1_miss | 377 |
| top5_miss | 40 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.375000 | 0.833333 | 0.875000 | 0.617190 | 3 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.529221 | 2 |
| time_bucket | ts9 | 23 | 0.521739 | 0.826087 | 0.956522 | 0.687440 | 1 |
| case_service | ts-basic-service | 201 | 0.562189 | 0.850746 | 0.945274 | 0.716472 | 11 |
| time_bucket | ts6 | 28 | 0.571429 | 0.750000 | 0.964286 | 0.702976 | 1 |
| fault_type | response-replace-body | 51 | 0.588235 | 0.862745 | 0.901961 | 0.741076 | 5 |
| case_service | unknown | 26 | 0.615385 | 0.884615 | 0.884615 | 0.743313 | 3 |
| fault_type | unknown | 26 | 0.615385 | 0.884615 | 0.884615 | 0.743313 | 3 |
| time_bucket | ts7 | 34 | 0.617647 | 0.823529 | 0.911765 | 0.744514 | 3 |
| fault_type | request-replace-method | 190 | 0.626316 | 0.926316 | 0.973684 | 0.777204 | 5 |
| case_service | ts-travel2-service | 68 | 0.632353 | 0.911765 | 0.970588 | 0.773588 | 2 |
| fault_type | response-replace-code | 231 | 0.640693 | 0.913420 | 0.978355 | 0.787498 | 5 |
| fault_type | request-replace-path | 39 | 0.641026 | 0.897436 | 0.974359 | 0.779304 | 1 |
| case_service | ts-security-service | 33 | 0.666667 | 0.969697 | 1.000000 | 0.820707 | 0 |
| case_service | ts-payment-service | 12 | 0.666667 | 1.000000 | 1.000000 | 0.833333 | 0 |
| case_service | ts-consign-price-service | 9 | 0.666667 | 1.000000 | 1.000000 | 0.833333 | 0 |
| fault_type | request-abort | 60 | 0.683333 | 0.883333 | 0.933333 | 0.785668 | 4 |
| fault_type | bandwidth | 42 | 0.690476 | 0.857143 | 0.880952 | 0.787724 | 5 |
| case_service | ts-route-plan-service | 138 | 0.695652 | 0.927536 | 0.971014 | 0.816796 | 4 |
| fault_type | corrupt | 46 | 0.695652 | 0.891304 | 0.978261 | 0.810507 | 1 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-food-service|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-food-service|ts-travel-service|ts-config-service|ts-order-service|ts-order-other-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-seat-service|ts-ui-dashboard|loadgenerator|ts-consign-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 22 | ts-inside-payment-service|ts-order-service|ts-travel-service|ts-seat-service|ts-assurance-service | return | ts-cancel-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 18 | ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-order-other-service|ts-order-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 17 | ts-payment-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-seat-service | response-replace-code | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 14 | ts-consign-service|ts-food-service|ts-basic-service|ts-route-plan-service|loadgenerator | stress | ts-cancel-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 13 | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-seat-service|ts-food-service | bandwidth | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 13 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service | bandwidth | ts-station-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-route-plan-service|ts-ui-dashboard|ts-food-service|ts-travel-plan-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 11 | ts-payment-service|ts-inside-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 9 | ts-order-service|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service|loadgenerator | partition | ts-seat-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 9 | ts-seat-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-preserve-service | response-replace-code | ts-travel2-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 9 | loadgenerator|ts-seat-service|ts-station-food-service|ts-travel2-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts5-ts-ui-dashboard-request-replace-method-dxffln | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-payment-service|loadgenerator|ts-basic-service|ts-security-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 9 | ts-ui-dashboard|ts-food-service|ts-payment-service|loadgenerator|ts-basic-service | response-replace-body | ts-route-plan-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 9 | ts-payment-service|ts-inside-payment-service|ts-food-service|ts-assurance-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts2-mysql-pod-kill-xvzmxb | mysql | 8 | ts-travel-service|ts-security-service|ts-auth-service|ts-order-service|ts-preserve-service | unknown | unknown |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 8 | ts-train-food-service|ts-food-service|ts-travel-service|ts-seat-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 8 | ts-route-plan-service|ts-security-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-food-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 8 | ts-preserve-service|ts-cancel-service|ts-order-service|ts-ui-dashboard|ts-seat-service | request-replace-method | ts-basic-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-consign-service|ts-food-service|ts-cancel-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | mysql | 7 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-travel2-service | container-kill | mysql |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 7 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 7 | ts-preserve-service|ts-cancel-service|ts-consign-price-service|ts-seat-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts5-ts-travel2-service-response-replace-body-ljvb7g | ts-route-service;ts-travel2-service | 7 | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-food-service|ts-ui-dashboard | response-replace-body | ts-travel2-service |
| ts7-ts-route-plan-service-response-delay-t55rlr | ts-route-plan-service;ts-travel-service | 7 | ts-inside-payment-service|ts-station-food-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | response-delay | ts-route-plan-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
