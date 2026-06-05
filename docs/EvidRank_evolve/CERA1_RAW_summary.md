# EvidenceRank CERA1_RAW Summary

- Created: 2026-06-05T01:09:06+08:00
- Source: `CERA1_RAW`
- Algorithm: `cera`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.510549 |
| AC@3 | 0.893108 |
| AC@5 | 0.961322 |
| MRR | 0.700399 |
| avg_rank | 2.134318 |
| top1_miss | 696 |
| top5_miss | 55 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.083333 | 0.625000 | 0.791667 | 0.353520 | 5 |
| fault_type | request-replace-path | 39 | 0.205128 | 0.846154 | 0.974359 | 0.512607 | 1 |
| case_service | ts-cancel-service | 4 | 0.250000 | 0.500000 | 0.500000 | 0.394490 | 2 |
| case_service | ts-verification-code-service | 4 | 0.250000 | 1.000000 | 1.000000 | 0.583333 | 0 |
| fault_type | response-replace-body | 51 | 0.274510 | 0.686275 | 0.882353 | 0.508061 | 6 |
| fault_type | response-replace-code | 231 | 0.316017 | 0.809524 | 0.956710 | 0.573892 | 10 |
| fault_type | request-abort | 60 | 0.316667 | 0.866667 | 0.916667 | 0.584901 | 5 |
| fault_type | response-abort | 44 | 0.318182 | 0.886364 | 0.954545 | 0.582235 | 2 |
| case_service | ts-basic-service | 201 | 0.318408 | 0.701493 | 0.905473 | 0.540125 | 19 |
| fault_type | request-replace-method | 190 | 0.342105 | 0.842105 | 0.957895 | 0.598053 | 8 |
| case_service | ts-travel2-service | 68 | 0.352941 | 0.779412 | 0.955882 | 0.565809 | 3 |
| case_service | ts-route-plan-service | 138 | 0.355072 | 0.891304 | 0.971014 | 0.602916 | 4 |
| time_bucket | ts1 | 179 | 0.357542 | 0.860335 | 0.955307 | 0.609275 | 8 |
| case_service | ts-auth-service | 26 | 0.384615 | 0.961538 | 1.000000 | 0.663462 | 0 |
| time_bucket | ts0 | 170 | 0.388235 | 0.917647 | 0.976471 | 0.640354 | 4 |
| time_bucket | ts3 | 210 | 0.395238 | 0.885714 | 0.971429 | 0.634476 | 6 |
| case_service | ts-payment-service | 12 | 0.416667 | 0.916667 | 0.916667 | 0.652778 | 1 |
| time_bucket | ts2 | 221 | 0.420814 | 0.900452 | 0.986425 | 0.653589 | 3 |
| time_bucket | ts7 | 34 | 0.441176 | 0.823529 | 0.941176 | 0.640196 | 2 |
| case_service | ts-consign-price-service | 9 | 0.444444 | 1.000000 | 1.000000 | 0.703704 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 32 | ts-food-service|ts-assurance-service|ts-ui-dashboard|loadgenerator|ts-consign-service | container-kill | ts-food-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 29 | ts-travel-service|ts-security-service|ts-order-service|ts-auth-service|ts-preserve-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 29 | ts-inside-payment-service|ts-order-service|ts-station-service|ts-travel-plan-service|ts-ui-dashboard | return | ts-cancel-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 29 | ts-auth-service|ts-travel-service|loadgenerator|ts-food-service|ts-order-other-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 23 | ts-food-service|ts-travel-service|ts-inside-payment-service|ts-order-service|ts-config-service | unknown | unknown |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 23 | ts-consign-service|loadgenerator|ts-food-service|ts-basic-service|ts-station-service | stress | ts-cancel-service |
| ts5-ts-train-food-service-mysql-rswcbh | mysql;ts-train-food-service | 22 | loadgenerator|ts-basic-service|ts-order-service|ts-preserve-service|ts-food-service | unknown | unknown |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 21 | ts-preserve-service|ts-payment-service|ts-ui-dashboard|ts-food-service|loadgenerator | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 20 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-train-service|ts-order-service | bandwidth | ts-route-plan-service |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 18 | loadgenerator|ts-ui-dashboard|ts-consign-price-service|ts-payment-service|ts-food-service | partition | ts-basic-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 17 | ts-consign-service|ts-travel-plan-service|ts-seat-service|ts-order-other-service|ts-route-plan-service | response-abort | ts-basic-service |
| ts1-ts-config-service-latency-5kkcrc | ts-config-service | 15 | ts-ui-dashboard|ts-consign-service|ts-order-service|ts-travel2-service|ts-food-service | unknown | unknown |
| ts0-mysql-container-kill-9t6n24 | mysql | 13 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-travel-service|ts-seat-service | container-kill | mysql |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 13 | ts-route-plan-service|ts-food-service|ts-assurance-service|ts-order-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-seat-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 12 | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-route-service | bandwidth | ts-station-service |
| ts5-ts-basic-service-request-replace-method-m559vq | ts-basic-service;ts-route-service | 12 | ts-inside-payment-service|ts-food-service|ts-travel2-service|ts-travel-service|ts-contacts-service | request-replace-method | ts-basic-service |
| ts2-ts-order-other-service-container-kill-48rlds | ts-order-other-service | 11 | ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-basic-service|ts-preserve-service | container-kill | ts-order-other-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-contacts-service|ts-travel-plan-service|ts-seat-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 10 | ts-ui-dashboard|ts-consign-service|ts-order-service|ts-user-service|ts-train-service | pod-failure | ts-travel-plan-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 10 | ts-preserve-service|ts-ui-dashboard|ts-assurance-service|ts-consign-price-service|ts-consign-service | response-replace-code | ts-travel-plan-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 10 | ts-order-service|ts-contacts-service|ts-consign-service|loadgenerator|ts-basic-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jrv8dx | ts-basic-service;ts-price-service | 9 | ts-ui-dashboard|ts-consign-service|ts-assurance-service|ts-inside-payment-service|ts-seat-service | response-replace-body | ts-basic-service |
| ts4-ts-travel-service-stress-fz5lbn | ts-travel-service | 9 | ts-ui-dashboard|ts-route-plan-service|ts-preserve-service|ts-security-service|loadgenerator | stress | ts-travel-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 9 | ts-inside-payment-service|ts-ui-dashboard|ts-payment-service|ts-route-plan-service|ts-food-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 8 | ts-travel-service|ts-preserve-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 8 | loadgenerator|ts-food-service|ts-assurance-service|ts-order-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts4-ts-station-service-return-qrsdpz | ts-station-service | 8 | ts-consign-service|ts-food-service|ts-basic-service|ts-travel2-service|ts-travel-service | return | ts-station-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 8 | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-seat-service|ts-food-service | response-replace-body | ts-travel-service |
| ts5-ts-travel2-service-response-replace-body-ljvb7g | ts-route-service;ts-travel2-service | 8 | ts-ui-dashboard|ts-food-service|ts-travel-plan-service|ts-route-plan-service|ts-order-service | response-replace-body | ts-travel2-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
