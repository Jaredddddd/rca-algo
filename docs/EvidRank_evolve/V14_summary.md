# EvidenceRank V14 Summary

- Created: 2026-06-02T18:21:49+08:00
- Source: `V14`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.657525 |
| AC@3 | 0.914205 |
| AC@5 | 0.962025 |
| MRR | 0.791101 |
| avg_rank | 1.827707 |
| top1_miss | 487 |
| top5_miss | 54 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | response-replace-body | 51 | 0.392157 | 0.784314 | 0.882353 | 0.610627 | 6 |
| fault_type | response-replace-code | 231 | 0.398268 | 0.826840 | 0.943723 | 0.627146 | 13 |
| case_service | ts-basic-service | 201 | 0.402985 | 0.786070 | 0.890547 | 0.611417 | 22 |
| fault_type | request-replace-path | 39 | 0.410256 | 0.820513 | 0.948718 | 0.639174 | 2 |
| case_service | ts-travel2-service | 68 | 0.426471 | 0.794118 | 0.970588 | 0.630801 | 2 |
| fault_type | pod-failure | 24 | 0.458333 | 0.833333 | 0.916667 | 0.634821 | 2 |
| fault_type | response-abort | 44 | 0.477273 | 0.840909 | 0.909091 | 0.670455 | 4 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.750000 | 0.750000 | 0.594697 | 1 |
| fault_type | request-replace-method | 190 | 0.510526 | 0.873684 | 0.947368 | 0.697350 | 10 |
| case_service | ts-security-service | 33 | 0.515152 | 1.000000 | 1.000000 | 0.747475 | 0 |
| fault_type | request-abort | 60 | 0.550000 | 0.833333 | 0.933333 | 0.709094 | 4 |
| time_bucket | ts9 | 23 | 0.565217 | 0.782609 | 0.913043 | 0.693478 | 2 |
| time_bucket | ts6 | 28 | 0.571429 | 0.750000 | 0.857143 | 0.694983 | 4 |
| case_service | ts-route-plan-service | 138 | 0.579710 | 0.876812 | 0.942029 | 0.738207 | 8 |
| case_service | ts-travel-service | 92 | 0.586957 | 0.880435 | 0.967391 | 0.748249 | 3 |
| time_bucket | ts7 | 34 | 0.588235 | 0.794118 | 0.852941 | 0.714354 | 5 |
| time_bucket | ts3 | 210 | 0.590476 | 0.923810 | 0.985714 | 0.761924 | 3 |
| case_service | ts-ui-dashboard | 165 | 0.593939 | 0.903030 | 0.951515 | 0.753458 | 8 |
| time_bucket | ts8 | 25 | 0.600000 | 0.800000 | 0.920000 | 0.733714 | 2 |
| case_service | ts-station-service | 20 | 0.600000 | 0.900000 | 0.950000 | 0.758810 | 1 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | ts-auth-service|ts-travel-service|loadgenerator|ts-seat-service|ts-route-plan-service | pod-failure | mysql |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 30 | ts-food-service|ts-ui-dashboard|ts-seat-service|loadgenerator|ts-consign-service | container-kill | ts-food-service |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 28 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-ticket-office-service | pod-failure | ts-travel-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 24 | ts-config-service|ts-food-service|ts-travel-service|ts-train-food-service|ts-order-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 22 | ts-inside-payment-service|ts-ui-dashboard|ts-assurance-service|ts-order-service|ts-station-service | return | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 20 | ts-payment-service|ts-ui-dashboard|ts-train-food-service|ts-seat-service|ts-preserve-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 15 | ts-preserve-service|ts-route-plan-service|ts-food-service|ts-travel-plan-service|ts-seat-service | response-replace-body | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 13 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-food-service|ts-verification-code-service | response-replace-body | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|ts-consign-price-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 12 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-travel2-service | response-abort | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 12 | ts-payment-service|ts-assurance-service|ts-inside-payment-service|ts-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jrv8dx | ts-basic-service;ts-price-service | 10 | ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-cancel-service|ts-train-food-service | response-replace-body | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 10 | ts-route-plan-service|ts-security-service|ts-ui-dashboard|ts-seat-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-seat-service|ts-route-plan-service|ts-travel2-service|ts-consign-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-cancel-service|ts-order-service|ts-seat-service|ts-food-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 10 | ts-ui-dashboard|ts-preserve-service|ts-seat-service|ts-route-plan-service|ts-contacts-service | response-replace-code | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 10 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-order-service | response-replace-code | ts-travel2-service |
| ts7-ts-route-plan-service-response-delay-t55rlr | ts-route-plan-service;ts-travel-service | 10 | ts-station-food-service|ts-consign-price-service|ts-inside-payment-service|ts-ui-dashboard|ts-seat-service | response-delay | ts-route-plan-service |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 9 | ts-ui-dashboard|ts-food-service|loadgenerator|ts-order-service|ts-verification-code-service | partition | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 9 | ts-ui-dashboard|ts-order-other-service|loadgenerator|ts-seat-service|ts-order-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 9 | ts-seat-service|ts-preserve-service|ts-food-service|ts-route-plan-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 9 | ts-preserve-service|ts-seat-service|ts-travel2-service|ts-ui-dashboard|ts-order-service | response-replace-body | ts-travel-service |
| ts5-ts-travel-service-response-replace-code-m9pmws | ts-basic-service;ts-travel-service | 9 | ts-preserve-service|ts-order-service|ts-route-plan-service|ts-seat-service|ts-ui-dashboard | response-replace-code | ts-travel-service |
| ts5-ts-travel2-service-response-replace-body-ljvb7g | ts-route-service;ts-travel2-service | 9 | ts-travel-plan-service|ts-seat-service|ts-ui-dashboard|ts-route-plan-service|ts-food-service | response-replace-body | ts-travel2-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 9 | ts-order-service|loadgenerator|ts-consign-service|ts-seat-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 8 | ts-ui-dashboard|ts-order-service|ts-consign-price-service|ts-travel-plan-service|loadgenerator | partition | ts-seat-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 8 | ts-security-service|ts-travel-service|ts-preserve-service|ts-order-service|ts-auth-service | unknown | unknown |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 8 | ts-ui-dashboard|loadgenerator|ts-config-service|ts-contacts-service|ts-auth-service | bandwidth | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-verification-code-service|ts-food-service | bandwidth | ts-route-plan-service |
| ts5-ts-travel-service-response-patch-body-nt8z6r | ts-basic-service;ts-travel-service | 8 | ts-travel-plan-service|ts-assurance-service|ts-order-service|ts-route-plan-service|ts-inside-payment-service | unknown | unknown |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
