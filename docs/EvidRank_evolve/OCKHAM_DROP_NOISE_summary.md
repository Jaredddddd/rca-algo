# EvidenceRank OCKHAM_DROP_NOISE Summary

- Created: 2026-06-14T20:54:08+08:00
- Source: `OCKHAM_DROP_NOISE`
- Algorithm: `crest_ockham_drop_noise`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.750352 |
| AC@3 | 0.924754 |
| AC@5 | 0.970464 |
| MRR | 0.840446 |
| avg_rank | 1.718706 |
| top1_miss | 355 |
| top5_miss | 42 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| time_bucket | ts9 | 23 | 0.478261 | 0.826087 | 0.956522 | 0.677536 | 1 |
| case_service | ts-ui-dashboard | 165 | 0.478788 | 0.903030 | 0.957576 | 0.687357 | 7 |
| fault_type | corrupt | 46 | 0.500000 | 0.782609 | 0.934783 | 0.659481 | 3 |
| time_bucket | ts6 | 28 | 0.500000 | 0.750000 | 0.964286 | 0.649405 | 1 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.750000 | 0.572500 | 1 |
| case_service | ts-seat-service | 79 | 0.569620 | 0.949367 | 0.974684 | 0.746875 | 2 |
| fault_type | response-delay | 89 | 0.606742 | 0.921348 | 0.988764 | 0.762360 | 1 |
| case_service | ts-route-service | 23 | 0.608696 | 0.782609 | 0.913043 | 0.726449 | 2 |
| fault_type | delay | 21 | 0.619048 | 0.904762 | 1.000000 | 0.753968 | 0 |
| time_bucket | ts7 | 34 | 0.647059 | 0.764706 | 0.941176 | 0.742927 | 2 |
| fault_type | request-delay | 88 | 0.647727 | 0.977273 | 1.000000 | 0.808712 | 0 |
| time_bucket | ts5 | 258 | 0.651163 | 0.860465 | 0.953488 | 0.767717 | 12 |
| time_bucket | ts4 | 274 | 0.660584 | 0.912409 | 0.956204 | 0.784761 | 12 |
| fault_type | bandwidth | 42 | 0.666667 | 0.785714 | 0.880952 | 0.745134 | 5 |
| time_bucket | ts8 | 25 | 0.680000 | 0.960000 | 0.960000 | 0.799048 | 1 |
| case_service | ts-basic-service | 201 | 0.681592 | 0.840796 | 0.930348 | 0.773874 | 14 |
| fault_type | request-replace-method | 190 | 0.684211 | 0.868421 | 0.957895 | 0.791080 | 8 |
| fault_type | loss | 48 | 0.687500 | 0.958333 | 0.979167 | 0.803323 | 1 |
| case_service | unknown | 26 | 0.692308 | 0.846154 | 0.884615 | 0.782095 | 3 |
| fault_type | unknown | 26 | 0.692308 | 0.846154 | 0.884615 | 0.782095 | 3 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 32 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-verification-code-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|loadgenerator|ts-travel-service|ts-seat-service|ts-order-other-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-config-service|ts-travel-service|ts-order-service|ts-food-service|ts-order-other-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 25 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-assurance-service|ts-travel-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 25 | ts-food-service|ts-train-food-service|loadgenerator|ts-ui-dashboard|ts-station-food-service | container-kill | ts-food-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 22 | ts-preserve-service|ts-payment-service|ts-ui-dashboard|loadgenerator|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 18 | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-order-other-service|ts-user-service | bandwidth | ts-route-plan-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 18 | ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-auth-service | bandwidth | ts-station-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 17 | ts-train-food-service|ts-station-service|ts-order-service|ts-seat-service|loadgenerator | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 15 | ts-route-plan-service|ts-security-service|ts-auth-service|ts-travel-plan-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 13 | ts-ui-dashboard|ts-order-service|loadgenerator|ts-travel-plan-service|ts-inside-payment-service | partition | ts-seat-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 12 | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-food-service|ts-travel-plan-service | bandwidth | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-consign-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-ui-dashboard|ts-travel-plan-service|ts-consign-price-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-contacts-service | response-replace-code | ts-basic-service |
| ts1-ts-route-service-corrupt-qlt7gn | mysql;ts-route-service | 10 | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-consign-service|ts-train-service | corrupt | ts-route-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 10 | ts-auth-service|ts-order-service|ts-security-service|ts-preserve-service|ts-verification-code-service | unknown | unknown |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-cancel-service|ts-order-service|ts-ui-dashboard|ts-food-service | request-replace-method | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 10 | ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-food-service|ts-travel-plan-service | response-replace-body | ts-route-plan-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|ts-verification-code-service|ts-food-service|loadgenerator | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-corrupt-trd2kh | ts-basic-service;ts-preserve-service | 9 | ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-contacts-service|ts-food-service | corrupt | ts-basic-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 9 | ts-verification-code-service|ts-consign-service|ts-basic-service|ts-config-service|ts-order-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-route-service-corrupt-rplmkr | mysql;ts-route-service | 8 | ts-ui-dashboard|ts-basic-service|ts-auth-service|ts-order-service|loadgenerator | corrupt | ts-route-service |
| ts3-ts-ui-dashboard-request-replace-method-7lstrz | ts-assurance-service;ts-ui-dashboard | 8 | loadgenerator|ts-price-service|ts-verification-code-service|ts-basic-service|ts-config-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | loadgenerator|ts-ui-dashboard|ts-food-service|ts-verification-code-service|ts-travel-plan-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 8 | ts-consign-service|ts-route-plan-service|ts-voucher-service|ts-travel2-service|ts-travel-plan-service | response-abort | ts-basic-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 8 | ts-preserve-service|ts-ui-dashboard|ts-travel2-service|ts-order-service|loadgenerator | response-replace-body | ts-travel-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 8 | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-ui-dashboard|ts-config-service | response-replace-code | ts-travel2-service |
| ts3-ts-ui-dashboard-request-replace-method-wkh6t7 | ts-travel-plan-service;ts-ui-dashboard | 7 | ts-seat-service|loadgenerator|ts-order-service|ts-basic-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-seat-service-bandwidth-k2bwt2 | ts-config-service;ts-seat-service | 7 | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-route-plan-service | bandwidth | ts-seat-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
