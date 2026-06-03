# EvidenceRank FW_PRIORITY_PRIOR Summary

- Created: 2026-06-03T23:17:48+08:00
- Source: `current`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.800985 |
| AC@3 | 0.942335 |
| AC@5 | 0.975387 |
| MRR | 0.874517 |
| avg_rank | 1.554852 |
| top1_miss | 283 |
| top5_miss | 35 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.208333 | 0.500000 | 0.708333 | 0.416127 | 7 |
| time_bucket | ts8 | 25 | 0.360000 | 0.880000 | 0.960000 | 0.632381 | 1 |
| time_bucket | ts6 | 28 | 0.500000 | 0.750000 | 0.964286 | 0.667262 | 1 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.531656 | 2 |
| time_bucket | ts7 | 34 | 0.588235 | 0.823529 | 0.882353 | 0.720658 | 4 |
| time_bucket | ts9 | 23 | 0.608696 | 0.913043 | 0.956522 | 0.754831 | 1 |
| fault_type | request-abort | 60 | 0.616667 | 0.916667 | 0.933333 | 0.761930 | 4 |
| fault_type | response-replace-body | 51 | 0.627451 | 0.862745 | 0.960784 | 0.751634 | 2 |
| case_service | ts-basic-service | 201 | 0.636816 | 0.905473 | 0.980100 | 0.772791 | 4 |
| fault_type | bandwidth | 42 | 0.690476 | 0.857143 | 0.857143 | 0.774017 | 6 |
| case_service | unknown | 26 | 0.692308 | 0.884615 | 0.884615 | 0.777991 | 3 |
| fault_type | unknown | 26 | 0.692308 | 0.884615 | 0.884615 | 0.777991 | 3 |
| case_service | ts-station-service | 20 | 0.700000 | 0.850000 | 0.850000 | 0.796032 | 3 |
| case_service | ts-ui-dashboard | 165 | 0.703030 | 0.884848 | 0.945455 | 0.808393 | 9 |
| case_service | ts-order-other-service | 27 | 0.703704 | 1.000000 | 1.000000 | 0.839506 | 0 |
| fault_type | request-replace-method | 190 | 0.715789 | 0.894737 | 0.978947 | 0.820100 | 4 |
| case_service | ts-travel2-service | 68 | 0.720588 | 0.926471 | 1.000000 | 0.827451 | 0 |
| fault_type | response-replace-code | 231 | 0.744589 | 0.922078 | 0.982684 | 0.840002 | 4 |
| case_service | ts-verification-code-service | 4 | 0.750000 | 1.000000 | 1.000000 | 0.875000 | 0 |
| fault_type | corrupt | 46 | 0.760870 | 0.978261 | 1.000000 | 0.870290 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-travel-service|ts-order-other-service|ts-seat-service|ts-food-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 28 | ts-inside-payment-service|ts-order-service|ts-travel-service|ts-station-service|ts-ui-dashboard | return | ts-cancel-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 28 | ts-auth-service|ts-travel-service|ts-seat-service|ts-order-other-service|loadgenerator | pod-failure | mysql |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 27 | ts-auth-service|ts-ui-dashboard|ts-train-food-service|ts-station-food-service|ts-security-service | pod-failure | ts-travel-plan-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 27 | ts-food-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-order-service | container-kill | ts-food-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 14 | ts-inside-payment-service|ts-order-service|ts-order-other-service|ts-seat-service|ts-basic-service | pod-failure | ts-payment-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 14 | ts-ui-dashboard|loadgenerator|ts-order-service|ts-seat-service|ts-auth-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 14 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-preserve-service | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 13 | ts-order-service|ts-seat-service|ts-food-service|loadgenerator|ts-basic-service | request-abort | ts-ui-dashboard |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 12 | ts-consign-service|ts-order-service|ts-payment-service|ts-verification-code-service|ts-travel-service | unknown | unknown |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 11 | ts-consign-service|ts-food-service|ts-route-plan-service|ts-auth-service|ts-basic-service | stress | ts-cancel-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 10 | ts-ui-dashboard|loadgenerator|ts-order-service|ts-contacts-service|ts-seat-service | bandwidth | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 10 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 9 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service | bandwidth | ts-station-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-auth-service|ts-travel-service|ts-security-service|ts-order-service|ts-preserve-service | unknown | unknown |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 9 | loadgenerator|ts-station-food-service|ts-travel2-service|ts-seat-service|ts-travel-plan-service | request-abort | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 9 | ts-payment-service|ts-inside-payment-service|loadgenerator|ts-verification-code-service|ts-assurance-service | request-abort | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | mysql | 8 | ts-train-service|ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 8 | ts-order-service|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service|ts-inside-payment-service | partition | ts-seat-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-basic-service|ts-verification-code-service|ts-travel-plan-service | bandwidth | ts-route-plan-service |
| ts4-ts-seat-service-bandwidth-k2bwt2 | ts-config-service;ts-seat-service | 8 | ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | bandwidth | ts-seat-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 7 | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|loadgenerator | bandwidth | ts-station-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 7 | ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-payment-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 7 | ts-ui-dashboard|loadgenerator|ts-consign-price-service|ts-travel2-service|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 7 | ts-travel-plan-service|ts-basic-service|ts-route-plan-service|ts-travel2-service|ts-travel-service | pod-failure | ts-price-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 7 | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-station-food-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 7 | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-station-food-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-station-service-pod-failure-fn44tf | ts-station-service | 6 | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-station-service |
| ts1-ts-train-service-pod-failure-5qwqdz | ts-train-service | 6 | ts-basic-service|ts-route-plan-service|ts-travel-service|ts-travel-plan-service|ts-travel2-service | pod-failure | ts-train-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
