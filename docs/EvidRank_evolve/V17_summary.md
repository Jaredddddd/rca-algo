# EvidenceRank V17 Summary

- Created: 2026-06-02T18:54:41+08:00
- Source: `V17`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.563291 |
| AC@3 | 0.868495 |
| AC@5 | 0.939522 |
| MRR | 0.724849 |
| avg_rank | 2.185654 |
| top1_miss | 621 |
| top5_miss | 86 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | ts-ui-dashboard | 165 | 0.072727 | 0.672727 | 0.824242 | 0.401134 | 29 |
| fault_type | response-replace-code | 231 | 0.242424 | 0.722944 | 0.883117 | 0.503971 | 27 |
| case_service | ts-basic-service | 201 | 0.318408 | 0.711443 | 0.880597 | 0.540726 | 24 |
| time_bucket | ts8 | 25 | 0.320000 | 0.760000 | 0.960000 | 0.574889 | 1 |
| fault_type | response-replace-body | 51 | 0.333333 | 0.705882 | 0.843137 | 0.549081 | 8 |
| fault_type | request-replace-path | 39 | 0.333333 | 0.769231 | 0.923077 | 0.575427 | 3 |
| fault_type | pod-failure | 24 | 0.333333 | 0.750000 | 0.916667 | 0.563194 | 2 |
| time_bucket | ts9 | 23 | 0.347826 | 0.608696 | 0.826087 | 0.545290 | 4 |
| case_service | ts-travel2-service | 68 | 0.352941 | 0.794118 | 0.897059 | 0.574744 | 7 |
| fault_type | response-abort | 44 | 0.409091 | 0.840909 | 0.954545 | 0.628598 | 2 |
| fault_type | request-replace-method | 190 | 0.421053 | 0.768421 | 0.905263 | 0.614563 | 18 |
| fault_type | request-abort | 60 | 0.433333 | 0.766667 | 0.866667 | 0.626687 | 8 |
| time_bucket | ts7 | 34 | 0.441176 | 0.676471 | 0.794118 | 0.603303 | 7 |
| time_bucket | ts6 | 28 | 0.464286 | 0.678571 | 0.821429 | 0.623272 | 5 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.750000 | 0.571429 | 1 |
| time_bucket | ts3 | 210 | 0.542857 | 0.890476 | 0.961905 | 0.720489 | 8 |
| time_bucket | ts2 | 221 | 0.542986 | 0.923077 | 0.959276 | 0.721443 | 9 |
| case_service | ts-security-service | 33 | 0.545455 | 1.000000 | 1.000000 | 0.757576 | 0 |
| time_bucket | ts1 | 179 | 0.547486 | 0.927374 | 0.972067 | 0.728480 | 5 |
| case_service | ts-station-service | 20 | 0.550000 | 0.950000 | 0.950000 | 0.738333 | 1 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 30 | ts-ui-dashboard|ts-verification-code-service|ts-ticket-office-service|ts-auth-service|ts-consign-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | ts-auth-service|loadgenerator|ts-travel-service|ts-ui-dashboard|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-config-service|ts-train-food-service|ts-food-service|ts-travel-service|ts-train-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|loadgenerator|ts-seat-service|ts-consign-service|ts-assurance-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 28 | ts-inside-payment-service|ts-ui-dashboard|loadgenerator|ts-station-service|ts-assurance-service | return | ts-cancel-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 26 | ts-train-food-service|loadgenerator|ts-food-service|ts-order-service|ts-contacts-service | request-abort | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 24 | ts-payment-service|ts-train-food-service|loadgenerator|ts-consign-price-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 18 | ts-payment-service|ts-consign-price-service|ts-consign-service|loadgenerator|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | ts-travel-plan-service;ts-ui-dashboard | 15 | ts-inside-payment-service|ts-station-service|ts-payment-service|loadgenerator|ts-train-food-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 14 | ts-contacts-service|loadgenerator|ts-preserve-service|ts-route-plan-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 13 | ts-order-service|loadgenerator|ts-consign-price-service|ts-ui-dashboard|ts-travel-plan-service | partition | ts-seat-service |
| ts1-ts-ui-dashboard-response-replace-code-prqgf5 | ts-route-service;ts-ui-dashboard | 13 | ts-assurance-service|ts-consign-price-service|ts-travel-service|ts-order-service|ts-food-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-g7zr28 | ts-travel-service;ts-ui-dashboard | 13 | ts-travel-plan-service|loadgenerator|ts-seat-service|ts-config-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-7lstrz | ts-assurance-service;ts-ui-dashboard | 13 | loadgenerator|ts-price-service|ts-config-service|ts-contacts-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 13 | ts-preserve-service|ts-route-plan-service|loadgenerator|ts-travel-plan-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 13 | ts-route-plan-service|ts-security-service|loadgenerator|ts-travel-plan-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 13 | ts-cancel-service|ts-preserve-service|ts-station-service|ts-order-service|loadgenerator | request-replace-method | ts-basic-service |
| ts5-ts-ui-dashboard-response-replace-code-fsnppw | ts-ui-dashboard;ts-verification-code-service | 13 | ts-security-service|loadgenerator|ts-station-food-service|ts-food-service|ts-auth-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-ms2qf9 | ts-travel-plan-service;ts-ui-dashboard | 12 | loadgenerator|ts-config-service|ts-payment-service|ts-seat-service|ts-basic-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 12 | loadgenerator|ts-ui-dashboard|ts-user-service|ts-contacts-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-consign-price-service|ts-inside-payment-service|ts-station-food-service|loadgenerator | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-consign-price-service|ts-cancel-service|ts-route-plan-service|ts-travel-plan-service | request-replace-path | ts-basic-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 11 | loadgenerator|ts-travel2-service|ts-route-plan-service|ts-consign-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 11 | ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-preserve-service|ts-security-service | response-replace-code | ts-travel2-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 11 | loadgenerator|ts-station-food-service|ts-contacts-service|ts-route-service|ts-travel2-service | request-abort | ts-ui-dashboard |
| ts6-ts-preserve-service-partition-jvzrwx | ts-preserve-service;ts-ui-dashboard | 11 | ts-payment-service|loadgenerator|ts-assurance-service|ts-basic-service|ts-food-service | partition | ts-preserve-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 10 | ts-security-service|ts-preserve-service|ts-travel-service|ts-auth-service|ts-order-service | unknown | unknown |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 10 | ts-travel-service|ts-route-plan-service|loadgenerator|ts-travel-plan-service|ts-ui-dashboard | bandwidth | ts-station-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 10 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-consign-price-service|loadgenerator | response-abort | ts-basic-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|ts-station-food-service|ts-preserve-service|ts-consign-price-service | response-replace-code | ts-ui-dashboard |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
