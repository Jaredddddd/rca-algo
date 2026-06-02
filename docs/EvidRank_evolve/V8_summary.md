# EvidenceRank V8 Summary

- Created: 2026-06-02T03:53:28+08:00
- Source: `V8`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.788326 |
| AC@3 | 0.939522 |
| AC@5 | 0.973980 |
| MRR | 0.866904 |
| avg_rank | 1.604782 |
| top1_miss | 301 |
| top5_miss | 37 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.166667 | 0.541667 | 0.791667 | 0.408785 | 5 |
| time_bucket | ts8 | 25 | 0.360000 | 0.920000 | 0.960000 | 0.641667 | 1 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.527116 | 2 |
| time_bucket | ts6 | 28 | 0.535714 | 0.714286 | 0.857143 | 0.676871 | 4 |
| fault_type | response-replace-body | 51 | 0.549020 | 0.862745 | 0.960784 | 0.706754 | 2 |
| time_bucket | ts7 | 34 | 0.558824 | 0.794118 | 0.882353 | 0.705882 | 4 |
| time_bucket | ts9 | 23 | 0.565217 | 0.913043 | 0.956522 | 0.731605 | 1 |
| fault_type | request-abort | 60 | 0.600000 | 0.916667 | 0.933333 | 0.754603 | 4 |
| case_service | ts-basic-service | 201 | 0.626866 | 0.905473 | 0.975124 | 0.763512 | 5 |
| case_service | ts-ui-dashboard | 165 | 0.654545 | 0.872727 | 0.933333 | 0.775738 | 11 |
| fault_type | bandwidth | 42 | 0.666667 | 0.833333 | 0.857143 | 0.763370 | 6 |
| case_service | ts-order-other-service | 27 | 0.666667 | 0.962963 | 1.000000 | 0.817901 | 0 |
| case_service | unknown | 26 | 0.692308 | 0.807692 | 0.884615 | 0.771335 | 3 |
| fault_type | unknown | 26 | 0.692308 | 0.807692 | 0.884615 | 0.771335 | 3 |
| fault_type | request-replace-method | 190 | 0.694737 | 0.900000 | 0.957895 | 0.806067 | 8 |
| case_service | ts-station-service | 20 | 0.700000 | 0.850000 | 0.900000 | 0.797698 | 2 |
| fault_type | response-replace-code | 231 | 0.718615 | 0.917749 | 0.978355 | 0.821568 | 5 |
| case_service | ts-travel2-service | 68 | 0.720588 | 0.941176 | 1.000000 | 0.831127 | 0 |
| case_service | ts-route-plan-service | 138 | 0.753623 | 0.927536 | 0.971014 | 0.845293 | 4 |
| time_bucket | ts5 | 258 | 0.763566 | 0.941860 | 0.980620 | 0.855170 | 5 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 35 | ts-auth-service|ts-train-food-service|ts-station-food-service|ts-security-service|ts-payment-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-order-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 27 | ts-inside-payment-service|ts-travel-service|ts-order-service|ts-ui-dashboard|ts-station-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 27 | ts-food-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-seat-service | container-kill | ts-food-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 15 | ts-inside-payment-service|ts-order-other-service|ts-order-service|ts-seat-service|ts-basic-service | pod-failure | ts-payment-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 15 | ts-order-service|ts-seat-service|loadgenerator|ts-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 14 | ts-payment-service|ts-ui-dashboard|ts-train-food-service|ts-preserve-service|loadgenerator | response-replace-code | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 14 | ts-consign-service|ts-food-service|ts-route-plan-service|ts-auth-service|ts-basic-service | stress | ts-cancel-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 13 | ts-consign-service|ts-verification-code-service|ts-payment-service|ts-seat-service|ts-travel-service | unknown | unknown |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 13 | ts-payment-service|ts-inside-payment-service|loadgenerator|ts-verification-code-service|ts-auth-service | request-abort | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 12 | ts-ui-dashboard|ts-seat-service|ts-order-service|loadgenerator|ts-auth-service | bandwidth | ts-route-plan-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 11 | ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-basic-service|ts-seat-service | bandwidth | ts-route-plan-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 11 | loadgenerator|ts-station-food-service|ts-travel2-service|ts-seat-service|ts-route-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 10 | ts-ui-dashboard|loadgenerator|ts-order-service|ts-contacts-service|ts-seat-service | bandwidth | ts-basic-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 10 | ts-basic-service|ts-consign-service|ts-seat-service|ts-auth-service|ts-train-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 10 | ts-ui-dashboard|ts-consign-price-service|ts-travel2-service|loadgenerator|ts-auth-service | response-replace-code | ts-travel-plan-service |
| ts6-ts-basic-service-request-replace-method-4qzglm | ts-basic-service;ts-train-service | 10 | ts-cancel-service|ts-verification-code-service|ts-consign-service|ts-route-service|ts-travel-service | request-replace-method | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 10 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel-plan-service | response-replace-body | ts-route-plan-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 9 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service | bandwidth | ts-station-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-auth-service|ts-travel-service|ts-security-service|ts-preserve-service|ts-order-service | unknown | unknown |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | ts-food-service;ts-ui-dashboard | 9 | ts-order-service|ts-seat-service|loadgenerator|ts-basic-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 9 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | response-replace-body | ts-basic-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 8 | ts-order-service|loadgenerator|ts-basic-service|ts-verification-code-service|ts-consign-service | request-abort | ts-ui-dashboard |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-station-food-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-station-food-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | mysql | 7 | ts-train-service|ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 7 | ts-travel-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|loadgenerator | bandwidth | ts-station-service |
| ts6-ts-route-plan-service-response-replace-code-9pfgvr | ts-route-plan-service;ts-route-service | 7 | ts-payment-service|ts-ui-dashboard|ts-consign-service|ts-security-service|ts-consign-price-service | response-replace-code | ts-route-plan-service |
| ts6-ts-ui-dashboard-response-replace-code-tgfbsg | ts-consign-service;ts-ui-dashboard | 7 | ts-payment-service|ts-station-food-service|ts-travel-service|ts-seat-service|ts-route-plan-service | response-replace-code | ts-ui-dashboard |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
