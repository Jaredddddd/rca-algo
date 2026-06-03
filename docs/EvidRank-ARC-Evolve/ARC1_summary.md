# EvidenceRank ARC1 Summary

- Created: 2026-06-03T15:10:59+08:00
- Source: `ARC1`
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.705345 |
| AC@3 | 0.940225 |
| AC@5 | 0.971167 |
| MRR | 0.823675 |
| avg_rank | 1.702532 |
| top1_miss | 419 |
| top5_miss | 41 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.291667 | 0.750000 | 0.875000 | 0.527607 | 3 |
| fault_type | response-replace-body | 51 | 0.431373 | 0.862745 | 0.921569 | 0.656941 | 4 |
| time_bucket | ts9 | 23 | 0.434783 | 0.782609 | 0.956522 | 0.654348 | 1 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.524027 | 2 |
| fault_type | response-replace-code | 231 | 0.506494 | 0.913420 | 0.965368 | 0.710244 | 8 |
| case_service | ts-basic-service | 201 | 0.512438 | 0.880597 | 0.940299 | 0.689219 | 12 |
| fault_type | request-replace-path | 39 | 0.512821 | 0.871795 | 0.974359 | 0.710043 | 1 |
| fault_type | request-replace-method | 190 | 0.521053 | 0.921053 | 0.973684 | 0.718231 | 5 |
| time_bucket | ts6 | 28 | 0.535714 | 0.821429 | 0.928571 | 0.695833 | 2 |
| fault_type | response-abort | 44 | 0.545455 | 0.909091 | 0.977273 | 0.734470 | 1 |
| case_service | ts-security-service | 33 | 0.575758 | 0.969697 | 1.000000 | 0.775253 | 0 |
| case_service | ts-travel2-service | 68 | 0.588235 | 0.897059 | 0.970588 | 0.747852 | 2 |
| time_bucket | ts7 | 34 | 0.588235 | 0.852941 | 0.911765 | 0.727358 | 3 |
| time_bucket | ts8 | 25 | 0.600000 | 0.960000 | 0.960000 | 0.764444 | 1 |
| case_service | ts-route-plan-service | 138 | 0.644928 | 0.920290 | 0.971014 | 0.784429 | 4 |
| case_service | unknown | 26 | 0.653846 | 0.807692 | 0.923077 | 0.755813 | 2 |
| fault_type | unknown | 26 | 0.653846 | 0.807692 | 0.923077 | 0.755813 | 2 |
| fault_type | request-abort | 60 | 0.666667 | 0.883333 | 0.933333 | 0.776687 | 4 |
| case_service | ts-payment-service | 12 | 0.666667 | 0.916667 | 1.000000 | 0.808333 | 0 |
| case_service | ts-consign-price-service | 9 | 0.666667 | 1.000000 | 1.000000 | 0.814815 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-food-service|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-food-service|ts-travel-service|ts-config-service|ts-order-service|ts-train-food-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-seat-service|ts-ui-dashboard|ts-preserve-service|loadgenerator | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 23 | ts-inside-payment-service|ts-travel-service|ts-ui-dashboard|ts-seat-service|ts-order-service | return | ts-cancel-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 19 | ts-consign-service|ts-food-service|ts-basic-service|ts-route-plan-service|loadgenerator | stress | ts-cancel-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 18 | ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-order-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 15 | ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-food-service|ts-seat-service | pod-failure | ts-consign-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 14 | ts-payment-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-train-food-service | response-replace-code | ts-basic-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 12 | ts-travel-service|ts-security-service|ts-order-service|ts-preserve-service|ts-auth-service | unknown | unknown |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 12 | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-seat-service|ts-travel2-service | bandwidth | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-inside-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 12 | loadgenerator|ts-seat-service|ts-station-food-service|ts-travel2-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-contacts-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 10 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-travel2-service | container-kill | mysql |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | response-replace-body | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|ts-assurance-service|ts-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 9 | ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | bandwidth | ts-station-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 9 | ts-preserve-service|ts-order-service|ts-cancel-service|ts-seat-service|ts-food-service | request-replace-method | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 9 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-travel2-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 9 | ts-ui-dashboard|ts-payment-service|ts-food-service|ts-basic-service|loadgenerator | response-replace-body | ts-route-plan-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-payment-service|ts-consign-service|ts-food-service|ts-cancel-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 8 | ts-train-food-service|ts-food-service|ts-seat-service|ts-order-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 8 | ts-route-plan-service|ts-security-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-food-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 8 | ts-cancel-service|ts-seat-service|ts-preserve-service|ts-consign-price-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 8 | ts-ui-dashboard|ts-consign-price-service|ts-preserve-service|ts-travel2-service|ts-seat-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 7 | ts-order-service|ts-ui-dashboard|ts-travel-plan-service|ts-consign-price-service|ts-inside-payment-service | partition | ts-seat-service |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 7 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
