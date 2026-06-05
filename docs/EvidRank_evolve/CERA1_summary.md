# EvidenceRank CERA1 Summary

- Created: 2026-06-05T01:27:32+08:00
- Source: `CERA1`
- Algorithm: `cera`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.691280 |
| AC@3 | 0.933193 |
| AC@5 | 0.966245 |
| MRR | 0.814367 |
| avg_rank | 1.741913 |
| top1_miss | 439 |
| top5_miss | 48 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| time_bucket | ts9 | 23 | 0.434783 | 0.782609 | 0.913043 | 0.636232 | 2 |
| fault_type | response-replace-body | 51 | 0.490196 | 0.803922 | 0.901961 | 0.671538 | 5 |
| fault_type | response-replace-code | 231 | 0.493506 | 0.909091 | 0.965368 | 0.703286 | 8 |
| fault_type | pod-failure | 24 | 0.500000 | 0.833333 | 0.916667 | 0.674179 | 2 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.540865 | 2 |
| time_bucket | ts6 | 28 | 0.535714 | 0.821429 | 0.928571 | 0.690816 | 2 |
| case_service | ts-basic-service | 201 | 0.537313 | 0.845771 | 0.915423 | 0.697755 | 17 |
| fault_type | request-replace-method | 190 | 0.542105 | 0.905263 | 0.957895 | 0.725071 | 8 |
| case_service | ts-security-service | 33 | 0.545455 | 1.000000 | 1.000000 | 0.757576 | 0 |
| case_service | ts-ui-dashboard | 165 | 0.557576 | 0.921212 | 0.957576 | 0.734572 | 7 |
| fault_type | request-replace-path | 39 | 0.564103 | 0.897436 | 0.974359 | 0.733547 | 1 |
| fault_type | response-abort | 44 | 0.568182 | 0.909091 | 0.954545 | 0.744129 | 2 |
| case_service | ts-travel-service | 92 | 0.597826 | 0.934783 | 0.978261 | 0.771601 | 2 |
| case_service | unknown | 26 | 0.615385 | 0.884615 | 0.884615 | 0.743313 | 3 |
| fault_type | unknown | 26 | 0.615385 | 0.884615 | 0.884615 | 0.743313 | 3 |
| time_bucket | ts7 | 34 | 0.617647 | 0.823529 | 0.911765 | 0.738562 | 3 |
| case_service | ts-travel2-service | 68 | 0.632353 | 0.897059 | 0.955882 | 0.776477 | 3 |
| time_bucket | ts8 | 25 | 0.640000 | 0.960000 | 0.960000 | 0.777778 | 1 |
| fault_type | request-abort | 60 | 0.650000 | 0.850000 | 0.900000 | 0.757348 | 6 |
| case_service | ts-route-plan-service | 138 | 0.666667 | 0.913043 | 0.971014 | 0.793511 | 4 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | ts-auth-service|ts-travel-service|loadgenerator|ts-order-other-service|ts-seat-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-food-service|ts-config-service|ts-travel-service|ts-order-service|ts-train-food-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-seat-service|loadgenerator|ts-ui-dashboard|ts-consign-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 26 | ts-inside-payment-service|ts-station-service|ts-order-service|ts-assurance-service|ts-travel-service | return | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 21 | ts-payment-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-train-food-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 17 | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-seat-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 15 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-notification-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 14 | ts-train-food-service|ts-food-service|ts-order-service|ts-seat-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 12 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | bandwidth | ts-station-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-inside-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-contacts-service|ts-route-plan-service|ts-ui-dashboard|ts-seat-service | response-replace-code | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 11 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-travel2-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 10 | ts-route-plan-service|ts-security-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-order-service|ts-cancel-service|ts-ui-dashboard|ts-seat-service | request-replace-method | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|ts-assurance-service|ts-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 9 | ts-consign-price-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-travel2-service | response-replace-code | ts-travel-plan-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 9 | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-order-service | response-replace-body | ts-travel-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 9 | loadgenerator|ts-station-food-service|ts-seat-service|ts-travel2-service|ts-consign-service | request-abort | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 9 | ts-ui-dashboard|ts-payment-service|loadgenerator|ts-food-service|ts-verification-code-service | response-replace-body | ts-route-plan-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-payment-service|ts-consign-service|ts-food-service|ts-cancel-service|ts-price-service | request-replace-method | ts-ui-dashboard |
| ts2-mysql-pod-kill-xvzmxb | mysql | 8 | ts-travel-service|ts-security-service|ts-auth-service|ts-order-service|ts-preserve-service | unknown | unknown |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-verification-code-service|ts-assurance-service | partition | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 8 | ts-consign-price-service|ts-cancel-service|ts-preserve-service|ts-seat-service|ts-route-plan-service | request-replace-path | ts-basic-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 8 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | response-abort | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 8 | ts-consign-service|ts-food-service|loadgenerator|ts-basic-service|ts-route-plan-service | stress | ts-cancel-service |
| ts7-ts-route-plan-service-response-delay-t55rlr | ts-route-plan-service;ts-travel-service | 8 | ts-inside-payment-service|ts-station-food-service|ts-consign-price-service|ts-ui-dashboard|ts-seat-service | response-delay | ts-route-plan-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 8 | ts-order-service|ts-consign-service|loadgenerator|ts-contacts-service|ts-seat-service | request-abort | ts-ui-dashboard |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 7 | ts-order-service|ts-ui-dashboard|loadgenerator|ts-consign-price-service|ts-travel-plan-service | partition | ts-seat-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 7 | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-config-service|ts-order-service | bandwidth | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
