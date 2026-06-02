# EvidenceRank V15 Summary

- Created: 2026-06-02T18:33:51+08:00
- Source: `V15`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.638537 |
| AC@3 | 0.884669 |
| AC@5 | 0.949367 |
| MRR | 0.772135 |
| avg_rank | 2.012658 |
| top1_miss | 514 |
| top5_miss | 72 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.083333 | 0.208333 | 0.458333 | 0.233382 | 13 |
| case_service | ts-cancel-service | 4 | 0.250000 | 0.500000 | 0.500000 | 0.394984 | 2 |
| fault_type | response-replace-body | 51 | 0.274510 | 0.764706 | 0.882353 | 0.532843 | 6 |
| fault_type | response-replace-code | 231 | 0.376623 | 0.796537 | 0.922078 | 0.607133 | 18 |
| case_service | ts-travel2-service | 68 | 0.382353 | 0.808824 | 0.955882 | 0.596341 | 3 |
| fault_type | request-replace-path | 39 | 0.384615 | 0.717949 | 0.948718 | 0.587424 | 2 |
| case_service | ts-basic-service | 201 | 0.422886 | 0.696517 | 0.870647 | 0.600589 | 26 |
| fault_type | response-abort | 44 | 0.454545 | 0.818182 | 0.931818 | 0.647538 | 3 |
| fault_type | request-abort | 60 | 0.466667 | 0.833333 | 0.950000 | 0.665482 | 3 |
| case_service | ts-security-service | 33 | 0.484848 | 1.000000 | 1.000000 | 0.737374 | 0 |
| fault_type | request-replace-method | 190 | 0.505263 | 0.826316 | 0.926316 | 0.681744 | 14 |
| time_bucket | ts6 | 28 | 0.535714 | 0.821429 | 0.928571 | 0.699405 | 2 |
| case_service | ts-route-plan-service | 138 | 0.536232 | 0.876812 | 0.927536 | 0.715243 | 10 |
| time_bucket | ts1 | 179 | 0.564246 | 0.860335 | 0.966480 | 0.726425 | 6 |
| time_bucket | ts9 | 23 | 0.565217 | 0.695652 | 0.913043 | 0.679004 | 2 |
| time_bucket | ts2 | 221 | 0.565611 | 0.895928 | 0.954751 | 0.735173 | 10 |
| case_service | ts-ui-dashboard | 165 | 0.581818 | 0.915152 | 0.951515 | 0.748768 | 8 |
| time_bucket | ts3 | 210 | 0.585714 | 0.890476 | 0.957143 | 0.747463 | 9 |
| case_service | ts-travel-service | 92 | 0.586957 | 0.836957 | 0.967391 | 0.731090 | 3 |
| case_service | ts-station-service | 20 | 0.600000 | 0.850000 | 0.900000 | 0.751667 | 2 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 34 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-verification-code-service|ts-order-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 34 | ts-auth-service|ts-travel-service|loadgenerator|ts-route-plan-service|ts-order-other-service | pod-failure | mysql |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 29 | ts-inside-payment-service|ts-ui-dashboard|ts-order-service|ts-station-service|loadgenerator | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-ui-dashboard|ts-consign-service|ts-assurance-service|loadgenerator | container-kill | ts-food-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 28 | ts-config-service|ts-food-service|ts-travel-service|ts-train-food-service|ts-order-other-service | unknown | unknown |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 27 | ts-inside-payment-service|ts-order-other-service|ts-order-service|ts-ui-dashboard|ts-basic-service | pod-failure | ts-payment-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 22 | ts-consign-service|ts-food-service|ts-station-service|ts-basic-service|loadgenerator | stress | ts-cancel-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 21 | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-order-other-service | pod-failure | ts-consign-service |
| ts8-ts-food-service-pod-failure-9swgtb | ts-food-service | 21 | ts-station-service|ts-order-service|ts-order-other-service|ts-basic-service|ts-price-service | pod-failure | ts-food-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 20 | ts-station-service|ts-basic-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-service | pod-failure | ts-assurance-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 18 | ts-train-service|ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service | container-kill | mysql |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 17 | ts-payment-service|ts-ui-dashboard|ts-train-food-service|ts-preserve-service|loadgenerator | response-replace-code | ts-basic-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 16 | ts-consign-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service | pod-failure | ts-price-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 15 | ts-security-service|ts-preserve-service|ts-travel-service|ts-order-service|ts-auth-service | unknown | unknown |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 15 | ts-ui-dashboard|ts-payment-service|loadgenerator|ts-assurance-service|ts-food-service | response-replace-body | ts-route-plan-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | ts-travel-service | 13 | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|loadgenerator|ts-travel2-service | pod-failure | ts-travel-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 13 | ts-train-food-service|ts-food-service|ts-order-service|ts-seat-service|ts-contacts-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-route-plan-service|ts-food-service|ts-travel-plan-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-ui-dashboard|ts-preserve-service|ts-route-plan-service|ts-seat-service|ts-contacts-service | response-replace-code | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 11 | ts-payment-service|ts-assurance-service|ts-inside-payment-service|ts-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 10 | ts-ui-dashboard|ts-order-service|loadgenerator|ts-order-other-service|ts-seat-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 10 | ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-inside-payment-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 10 | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-ui-dashboard|ts-order-service | response-replace-code | ts-travel2-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-cancel-service|ts-train-food-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-station-food-service-pod-failure-td2qj4 | ts-station-food-service | 9 | ts-food-service|ts-travel-service|ts-basic-service|ts-order-other-service|ts-ui-dashboard | pod-failure | ts-station-food-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 9 | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service|ts-security-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 9 | ts-order-service|ts-preserve-service|ts-ui-dashboard|ts-station-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 9 | ts-order-service|ts-consign-service|loadgenerator|ts-basic-service|ts-contacts-service | request-abort | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-basic-service|ts-travel-plan-service | bandwidth | ts-route-plan-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-route-plan-service|ts-travel2-service|ts-seat-service|ts-basic-service|ts-consign-service | request-replace-method | ts-ui-dashboard |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
