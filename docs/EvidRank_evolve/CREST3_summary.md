# EvidenceRank CREST3 Summary

- Created: 2026-06-06T03:49:11+08:00
- Source: `CREST3`
- Algorithm: `crest`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.800281 |
| AC@3 | 0.945851 |
| AC@5 | 0.972574 |
| MRR | 0.875744 |
| avg_rank | 1.586498 |
| top1_miss | 284 |
| top5_miss | 39 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.458333 | 0.791667 | 0.875000 | 0.636866 | 3 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.523864 | 2 |
| time_bucket | ts6 | 28 | 0.607143 | 0.821429 | 0.964286 | 0.736310 | 1 |
| time_bucket | ts9 | 23 | 0.652174 | 0.913043 | 0.913043 | 0.786957 | 2 |
| fault_type | response-replace-body | 51 | 0.666667 | 0.843137 | 0.941176 | 0.776697 | 3 |
| time_bucket | ts7 | 34 | 0.676471 | 0.794118 | 0.970588 | 0.779144 | 1 |
| case_service | ts-seat-service | 79 | 0.683544 | 0.962025 | 0.987342 | 0.816974 | 1 |
| case_service | ts-basic-service | 201 | 0.686567 | 0.875622 | 0.930348 | 0.789562 | 14 |
| fault_type | bandwidth | 42 | 0.690476 | 0.857143 | 0.880952 | 0.774530 | 5 |
| case_service | unknown | 26 | 0.692308 | 0.884615 | 0.923077 | 0.789103 | 2 |
| fault_type | unknown | 26 | 0.692308 | 0.884615 | 0.923077 | 0.789103 | 2 |
| case_service | ts-travel-service | 92 | 0.706522 | 0.956522 | 0.989130 | 0.830357 | 1 |
| time_bucket | ts5 | 258 | 0.732558 | 0.903101 | 0.953488 | 0.825998 | 12 |
| fault_type | request-replace-method | 190 | 0.736842 | 0.942105 | 0.973684 | 0.841067 | 5 |
| fault_type | corrupt | 46 | 0.739130 | 0.913043 | 0.956522 | 0.835352 | 2 |
| case_service | ts-ui-dashboard | 165 | 0.739394 | 0.933333 | 0.969697 | 0.840014 | 5 |
| fault_type | response-replace-code | 231 | 0.740260 | 0.926407 | 0.965368 | 0.837074 | 8 |
| case_service | ts-order-other-service | 27 | 0.740741 | 0.925926 | 1.000000 | 0.841975 | 0 |
| case_service | ts-travel2-service | 68 | 0.750000 | 0.911765 | 0.985294 | 0.842810 | 1 |
| fault_type | request-abort | 60 | 0.750000 | 0.933333 | 0.966667 | 0.841389 | 2 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-verification-code-service|ts-execute-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-basic-service|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-travel-service|ts-food-service|ts-config-service|ts-train-food-service|ts-order-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 26 | ts-food-service|ts-train-food-service|ts-ui-dashboard|ts-seat-service|ts-preserve-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 22 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-travel-service|ts-assurance-service | return | ts-cancel-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 20 | ts-consign-service|ts-food-service|ts-basic-service|ts-station-service|ts-route-plan-service | stress | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 19 | ts-preserve-service|ts-payment-service|ts-ui-dashboard|ts-food-service|ts-user-service | response-replace-code | ts-basic-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 18 | ts-basic-service|ts-travel-service|ts-food-service|ts-ui-dashboard|ts-seat-service | pod-failure | ts-consign-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 17 | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|ts-food-service | container-kill | mysql |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 17 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-ui-dashboard | bandwidth | ts-station-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 15 | ts-security-service|ts-order-service|ts-auth-service|ts-preserve-service|ts-travel-service | unknown | unknown |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 15 | ts-ui-dashboard|ts-auth-service|ts-food-service|loadgenerator|ts-travel-plan-service | bandwidth | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 14 | ts-ui-dashboard|ts-auth-service|ts-preserve-service|ts-seat-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 11 | ts-order-service|ts-ui-dashboard|ts-travel-plan-service|ts-inside-payment-service|loadgenerator | partition | ts-seat-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 11 | ts-payment-service|ts-inside-payment-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-seat-service|ts-travel2-service|ts-contacts-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 11 | ts-ui-dashboard|ts-food-service|ts-preserve-service|ts-travel2-service|ts-travel-plan-service | response-replace-body | ts-route-plan-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 10 | ts-train-food-service|ts-food-service|ts-order-service|ts-seat-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 10 | ts-route-plan-service|ts-security-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|ts-food-service|ts-assurance-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 9 | ts-ui-dashboard|ts-food-service|ts-consign-service|ts-preserve-service|ts-verification-code-service | partition | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 9 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 9 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-preserve-service|ts-ui-dashboard | response-replace-code | ts-travel2-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 8 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-food-service|ts-seat-service | bandwidth | ts-station-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-travel-plan-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts1-ts-route-service-corrupt-qlt7gn | mysql;ts-route-service | 7 | ts-auth-service|ts-ui-dashboard|ts-consign-service|ts-train-service|ts-order-other-service | corrupt | ts-route-service |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 7 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 7 | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 7 | ts-preserve-service|ts-cancel-service|ts-order-service|ts-food-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 7 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-consign-price-service|ts-travel2-service | response-abort | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
