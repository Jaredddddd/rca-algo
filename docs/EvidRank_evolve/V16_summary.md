# EvidenceRank V16 Summary

- Created: 2026-06-02T18:45:07+08:00
- Source: `V16`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.583685 |
| AC@3 | 0.877637 |
| AC@5 | 0.945851 |
| MRR | 0.739592 |
| avg_rank | 2.094937 |
| top1_miss | 592 |
| top5_miss | 77 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | ts-ui-dashboard | 165 | 0.109091 | 0.703030 | 0.836364 | 0.432726 | 27 |
| fault_type | response-replace-code | 231 | 0.268398 | 0.744589 | 0.904762 | 0.527181 | 22 |
| fault_type | response-replace-body | 51 | 0.313725 | 0.745098 | 0.882353 | 0.554132 | 6 |
| fault_type | pod-failure | 24 | 0.333333 | 0.708333 | 0.916667 | 0.545789 | 2 |
| time_bucket | ts9 | 23 | 0.347826 | 0.608696 | 0.869565 | 0.548913 | 3 |
| case_service | ts-travel2-service | 68 | 0.352941 | 0.808824 | 0.911765 | 0.581863 | 6 |
| fault_type | request-replace-path | 39 | 0.358974 | 0.769231 | 0.923077 | 0.593998 | 3 |
| case_service | ts-basic-service | 201 | 0.368159 | 0.726368 | 0.890547 | 0.570786 | 22 |
| fault_type | response-abort | 44 | 0.409091 | 0.840909 | 0.931818 | 0.634876 | 3 |
| fault_type | request-replace-method | 190 | 0.431579 | 0.789474 | 0.905263 | 0.625817 | 18 |
| time_bucket | ts8 | 25 | 0.440000 | 0.800000 | 0.960000 | 0.640353 | 1 |
| time_bucket | ts7 | 34 | 0.441176 | 0.705882 | 0.794118 | 0.613060 | 7 |
| fault_type | request-abort | 60 | 0.450000 | 0.783333 | 0.900000 | 0.640535 | 6 |
| time_bucket | ts6 | 28 | 0.500000 | 0.714286 | 0.821429 | 0.653019 | 5 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.750000 | 0.571429 | 1 |
| case_service | ts-security-service | 33 | 0.545455 | 1.000000 | 1.000000 | 0.757576 | 0 |
| time_bucket | ts2 | 221 | 0.547511 | 0.923077 | 0.972851 | 0.728900 | 6 |
| time_bucket | ts3 | 210 | 0.557143 | 0.900000 | 0.961905 | 0.733732 | 8 |
| time_bucket | ts1 | 179 | 0.564246 | 0.932961 | 0.972067 | 0.742507 | 5 |
| case_service | ts-route-plan-service | 138 | 0.565217 | 0.884058 | 0.956522 | 0.737276 | 6 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|loadgenerator|ts-travel-service|ts-ui-dashboard|ts-route-plan-service | pod-failure | mysql |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 30 | ts-ui-dashboard|ts-verification-code-service|ts-auth-service|ts-consign-service|ts-ticket-office-service | pod-failure | ts-travel-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-config-service|ts-train-food-service|ts-food-service|ts-travel-service|ts-train-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|loadgenerator|ts-seat-service|ts-consign-service|ts-ui-dashboard | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 28 | ts-inside-payment-service|ts-ui-dashboard|loadgenerator|ts-station-service|ts-assurance-service | return | ts-cancel-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 25 | ts-train-food-service|ts-food-service|loadgenerator|ts-order-service|ts-contacts-service | request-abort | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 22 | ts-payment-service|ts-train-food-service|loadgenerator|ts-consign-price-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 17 | ts-payment-service|ts-consign-price-service|ts-consign-service|loadgenerator|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 14 | ts-cancel-service|ts-preserve-service|ts-order-service|ts-station-service|ts-food-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 13 | ts-contacts-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 12 | ts-order-service|loadgenerator|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service | partition | ts-seat-service |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | ts-travel-plan-service;ts-ui-dashboard | 12 | ts-inside-payment-service|ts-station-service|ts-payment-service|loadgenerator|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 12 | ts-route-plan-service|ts-security-service|ts-travel-plan-service|loadgenerator|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 12 | loadgenerator|ts-ui-dashboard|ts-user-service|ts-contacts-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-consign-price-service|ts-inside-payment-service|ts-station-food-service|loadgenerator | request-replace-method | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 12 | ts-travel-plan-service|ts-route-plan-service|ts-seat-service|ts-preserve-service|ts-security-service | response-replace-code | ts-travel2-service |
| ts1-ts-ui-dashboard-response-replace-code-prqgf5 | ts-route-service;ts-ui-dashboard | 11 | ts-assurance-service|ts-consign-price-service|ts-travel-service|ts-order-service|ts-food-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-7lstrz | ts-assurance-service;ts-ui-dashboard | 11 | loadgenerator|ts-price-service|ts-config-service|ts-basic-service|ts-contacts-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-consign-price-service|ts-route-plan-service|ts-cancel-service|ts-seat-service | request-replace-path | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 11 | loadgenerator|ts-station-food-service|ts-contacts-service|ts-route-service|ts-travel2-service | request-abort | ts-ui-dashboard |
| ts2-mysql-pod-kill-xvzmxb | mysql | 10 | ts-security-service|ts-preserve-service|ts-travel-service|ts-order-service|ts-auth-service | unknown | unknown |
| ts2-ts-ui-dashboard-request-replace-method-g7zr28 | ts-travel-service;ts-ui-dashboard | 10 | ts-travel-plan-service|loadgenerator|ts-seat-service|ts-basic-service|ts-config-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 10 | ts-travel-service|ts-route-plan-service|loadgenerator|ts-ui-dashboard|ts-travel-plan-service | bandwidth | ts-station-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 10 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-consign-price-service|loadgenerator | response-abort | ts-basic-service |
| ts5-ts-ui-dashboard-response-replace-code-fsnppw | ts-ui-dashboard;ts-verification-code-service | 10 | ts-security-service|loadgenerator|ts-station-food-service|ts-food-service|ts-auth-service | response-replace-code | ts-ui-dashboard |
| ts6-ts-preserve-service-partition-jvzrwx | ts-preserve-service;ts-ui-dashboard | 10 | ts-payment-service|loadgenerator|ts-assurance-service|ts-basic-service|ts-food-service | partition | ts-preserve-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|ts-station-food-service|ts-preserve-service|ts-consign-price-service | response-replace-code | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|ts-assurance-service|loadgenerator|ts-voucher-service | request-abort | ts-ui-dashboard |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 9 | loadgenerator|ts-food-service|ts-ui-dashboard|ts-assurance-service|ts-payment-service | partition | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
