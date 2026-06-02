# EvidenceRank V13 Summary

- Created: 2026-06-02T18:10:49+08:00
- Source: `V13`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.679325 |
| AC@3 | 0.926864 |
| AC@5 | 0.966245 |
| MRR | 0.804981 |
| avg_rank | 1.786217 |
| top1_miss | 456 |
| top5_miss | 48 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.166667 | 0.583333 | 0.875000 | 0.412726 | 3 |
| fault_type | response-replace-body | 51 | 0.431373 | 0.843137 | 0.901961 | 0.641914 | 5 |
| fault_type | response-replace-code | 231 | 0.432900 | 0.883117 | 0.969697 | 0.662365 | 7 |
| fault_type | request-replace-path | 39 | 0.461538 | 0.846154 | 0.948718 | 0.668234 | 2 |
| time_bucket | ts9 | 23 | 0.478261 | 0.739130 | 0.956522 | 0.640909 | 1 |
| case_service | ts-basic-service | 201 | 0.482587 | 0.830846 | 0.920398 | 0.659405 | 16 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.540179 | 2 |
| case_service | ts-travel2-service | 68 | 0.514706 | 0.926471 | 0.970588 | 0.706624 | 2 |
| case_service | ts-security-service | 33 | 0.515152 | 1.000000 | 1.000000 | 0.752525 | 0 |
| case_service | ts-ui-dashboard | 165 | 0.551515 | 0.903030 | 0.951515 | 0.728059 | 8 |
| fault_type | request-replace-method | 190 | 0.552632 | 0.905263 | 0.963158 | 0.726936 | 7 |
| fault_type | request-abort | 60 | 0.566667 | 0.850000 | 0.900000 | 0.720774 | 6 |
| time_bucket | ts6 | 28 | 0.571429 | 0.785714 | 0.892857 | 0.709821 | 3 |
| fault_type | response-abort | 44 | 0.590909 | 0.909091 | 0.954545 | 0.754356 | 2 |
| case_service | unknown | 26 | 0.615385 | 0.846154 | 0.884615 | 0.731241 | 3 |
| fault_type | unknown | 26 | 0.615385 | 0.846154 | 0.884615 | 0.731241 | 3 |
| time_bucket | ts7 | 34 | 0.617647 | 0.794118 | 0.911765 | 0.730065 | 3 |
| case_service | ts-travel-service | 92 | 0.619565 | 0.945652 | 0.967391 | 0.780344 | 3 |
| time_bucket | ts3 | 210 | 0.638095 | 0.942857 | 0.971429 | 0.788340 | 6 |
| case_service | ts-station-service | 20 | 0.650000 | 0.900000 | 0.950000 | 0.772879 | 1 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|loadgenerator|ts-route-plan-service|ts-order-other-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-config-service|ts-food-service|ts-travel-service|ts-train-food-service|ts-order-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|loadgenerator|ts-ui-dashboard|ts-seat-service|ts-consign-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 28 | ts-inside-payment-service|ts-ui-dashboard|ts-station-service|ts-order-service|ts-assurance-service | return | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 21 | ts-payment-service|ts-preserve-service|ts-ui-dashboard|ts-train-food-service|loadgenerator | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 15 | ts-train-food-service|ts-food-service|ts-order-service|ts-seat-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 14 | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-order-other-service|ts-seat-service | bandwidth | ts-route-plan-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 13 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-food-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 13 | ts-inside-payment-service|ts-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 13 | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-route-plan-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 11 | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-security-service|ts-travel2-service | response-replace-code | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 11 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | bandwidth | ts-station-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-order-service|ts-station-service|ts-food-service|ts-cancel-service | request-replace-method | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 11 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-travel2-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 11 | ts-payment-service|ts-inside-payment-service|ts-assurance-service|ts-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 10 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-food-service|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-cancel-service|ts-food-service | request-replace-method | ts-ui-dashboard |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-travel-service|ts-security-service|ts-order-service|ts-preserve-service|ts-auth-service | unknown | unknown |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 9 | ts-seat-service|ts-preserve-service|ts-route-plan-service|ts-travel-service|ts-food-service | request-replace-path | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 9 | loadgenerator|ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-contacts-service | request-abort | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-delay-t55rlr | ts-route-plan-service;ts-travel-service | 9 | ts-inside-payment-service|ts-station-food-service|ts-consign-price-service|ts-ui-dashboard|ts-seat-service | response-delay | ts-route-plan-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 9 | ts-order-service|loadgenerator|ts-consign-service|ts-contacts-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | mysql | 8 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|loadgenerator | container-kill | mysql |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 8 | ts-order-service|ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-consign-price-service | partition | ts-seat-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 8 | ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-auth-service|ts-config-service | bandwidth | ts-basic-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-seat-service|ts-route-plan-service|ts-travel2-service|ts-consign-service|loadgenerator | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 8 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | response-abort | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 8 | ts-consign-service|loadgenerator|ts-food-service|ts-route-plan-service|ts-basic-service | stress | ts-cancel-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 8 | ts-preserve-service|ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-order-service | response-replace-body | ts-travel-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
