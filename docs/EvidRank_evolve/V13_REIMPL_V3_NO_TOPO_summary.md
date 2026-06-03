# EvidenceRank V13_REIMPL_V3_NO_TOPO Summary

- Created: 2026-06-03T12:32:27+08:00
- Source: `V13_REIMPL_V3_NO_TOPO`
- Algorithm: `evidencerank_v13`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.649086 |
| AC@3 | 0.914909 |
| AC@5 | 0.966245 |
| MRR | 0.786477 |
| avg_rank | 1.833333 |
| top1_miss | 499 |
| top5_miss | 48 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | response-replace-code | 231 | 0.324675 | 0.835498 | 0.965368 | 0.590296 | 8 |
| fault_type | response-replace-body | 51 | 0.392157 | 0.803922 | 0.882353 | 0.601844 | 6 |
| fault_type | response-abort | 44 | 0.409091 | 0.863636 | 0.954545 | 0.650631 | 2 |
| case_service | ts-basic-service | 201 | 0.427861 | 0.771144 | 0.905473 | 0.618702 | 19 |
| case_service | ts-ui-dashboard | 165 | 0.430303 | 0.896970 | 0.951515 | 0.659216 | 8 |
| fault_type | request-replace-path | 39 | 0.435897 | 0.846154 | 0.948718 | 0.651140 | 2 |
| fault_type | request-abort | 60 | 0.450000 | 0.800000 | 0.900000 | 0.649722 | 6 |
| case_service | ts-travel2-service | 68 | 0.470588 | 0.838235 | 0.970588 | 0.662640 | 2 |
| time_bucket | ts9 | 23 | 0.478261 | 0.739130 | 0.956522 | 0.642754 | 1 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.750000 | 0.575658 | 1 |
| fault_type | request-replace-method | 190 | 0.510526 | 0.873684 | 0.963158 | 0.695992 | 7 |
| time_bucket | ts8 | 25 | 0.520000 | 0.840000 | 0.960000 | 0.700667 | 1 |
| time_bucket | ts7 | 34 | 0.529412 | 0.823529 | 0.911765 | 0.687745 | 3 |
| time_bucket | ts6 | 28 | 0.535714 | 0.750000 | 0.892857 | 0.681888 | 3 |
| case_service | ts-security-service | 33 | 0.545455 | 1.000000 | 1.000000 | 0.762626 | 0 |
| case_service | ts-route-plan-service | 138 | 0.550725 | 0.905797 | 0.971014 | 0.737388 | 4 |
| case_service | unknown | 26 | 0.576923 | 0.807692 | 0.884615 | 0.721625 | 3 |
| fault_type | unknown | 26 | 0.576923 | 0.807692 | 0.884615 | 0.721625 | 3 |
| fault_type | pod-failure | 24 | 0.583333 | 0.916667 | 0.916667 | 0.745833 | 2 |
| case_service | ts-travel-service | 92 | 0.597826 | 0.891304 | 0.956522 | 0.752083 | 4 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 30 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | ts-auth-service|loadgenerator|ts-travel-service|ts-route-plan-service|ts-order-other-service | pod-failure | mysql |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 30 | ts-food-service|loadgenerator|ts-seat-service|ts-ui-dashboard|ts-consign-service | container-kill | ts-food-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-config-service|ts-food-service|ts-travel-service|ts-train-food-service|ts-voucher-service | unknown | unknown |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 21 | ts-payment-service|ts-ui-dashboard|ts-train-food-service|ts-preserve-service|loadgenerator | response-replace-code | ts-basic-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 19 | ts-inside-payment-service|ts-ui-dashboard|ts-station-service|ts-order-service|loadgenerator | return | ts-cancel-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 15 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-notification-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 13 | ts-payment-service|ts-consign-price-service|ts-inside-payment-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 13 | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-route-plan-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 12 | ts-train-food-service|ts-food-service|ts-order-service|loadgenerator|ts-seat-service | request-abort | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 12 | ts-payment-service|ts-assurance-service|ts-inside-payment-service|ts-food-service|loadgenerator | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 11 | ts-security-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 11 | ts-cancel-service|ts-preserve-service|ts-order-service|ts-station-service|ts-food-service | request-replace-method | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 10 | ts-ui-dashboard|loadgenerator|ts-order-other-service|ts-auth-service|ts-order-service | bandwidth | ts-route-plan-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 10 | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-travel2-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 10 | loadgenerator|ts-station-food-service|ts-travel2-service|ts-seat-service|ts-contacts-service | request-abort | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-delay-t55rlr | ts-route-plan-service;ts-travel-service | 10 | ts-consign-price-service|ts-inside-payment-service|ts-station-food-service|ts-ui-dashboard|ts-contacts-service | response-delay | ts-route-plan-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 10 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-food-service|ts-assurance-service | response-replace-body | ts-route-plan-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 10 | ts-order-service|loadgenerator|ts-consign-service|ts-basic-service|ts-contacts-service | request-abort | ts-ui-dashboard |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-cancel-service|loadgenerator | request-replace-method | ts-ui-dashboard |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 9 | ts-order-service|ts-ui-dashboard|ts-consign-price-service|loadgenerator|ts-travel-plan-service | partition | ts-seat-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-travel-service|ts-security-service|ts-preserve-service|ts-order-service|ts-auth-service | unknown | unknown |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 9 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | bandwidth | ts-station-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-route-plan-service|ts-seat-service|ts-travel2-service|loadgenerator|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 9 | ts-consign-price-service|ts-cancel-service|ts-preserve-service|ts-seat-service|ts-route-plan-service | request-replace-path | ts-basic-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 9 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-consign-price-service|ts-voucher-service | response-abort | ts-basic-service |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-assurance-service|ts-order-service | partition | ts-basic-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 8 | ts-preserve-service|ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-order-service | response-replace-body | ts-travel-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 7 | ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-auth-service|ts-order-service | bandwidth | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-wpxp9b | ts-basic-service;ts-station-service | 7 | ts-route-plan-service|ts-preserve-service|ts-ui-dashboard|ts-verification-code-service|ts-travel-service | response-replace-body | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
