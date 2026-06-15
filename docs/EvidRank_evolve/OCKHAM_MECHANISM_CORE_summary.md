# EvidenceRank OCKHAM_MECHANISM_CORE Summary

- Created: 2026-06-14T20:54:34+08:00
- Source: `OCKHAM_MECHANISM_CORE`
- Algorithm: `crest_ockham_mechanism_core`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.754571 |
| AC@3 | 0.939522 |
| AC@5 | 0.973277 |
| MRR | 0.847589 |
| avg_rank | 1.650492 |
| top1_miss | 349 |
| top5_miss | 38 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.291667 | 0.833333 | 0.916667 | 0.556360 | 2 |
| time_bucket | ts6 | 28 | 0.464286 | 0.785714 | 1.000000 | 0.658929 | 0 |
| case_service | ts-route-service | 23 | 0.478261 | 0.826087 | 0.913043 | 0.662077 | 2 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.525794 | 2 |
| case_service | ts-seat-service | 79 | 0.518987 | 0.924051 | 0.974684 | 0.713351 | 2 |
| time_bucket | ts9 | 23 | 0.565217 | 0.913043 | 0.956522 | 0.732298 | 1 |
| fault_type | corrupt | 46 | 0.586957 | 0.826087 | 0.934783 | 0.711680 | 3 |
| case_service | ts-ui-dashboard | 165 | 0.593939 | 0.939394 | 0.987879 | 0.773150 | 2 |
| case_service | ts-user-service | 15 | 0.600000 | 1.000000 | 1.000000 | 0.777778 | 0 |
| fault_type | response-delay | 89 | 0.606742 | 0.977528 | 0.988764 | 0.770037 | 1 |
| fault_type | delay | 21 | 0.619048 | 1.000000 | 1.000000 | 0.746032 | 0 |
| case_service | ts-price-service | 8 | 0.625000 | 1.000000 | 1.000000 | 0.770833 | 0 |
| time_bucket | ts8 | 25 | 0.640000 | 0.960000 | 1.000000 | 0.788000 | 0 |
| case_service | unknown | 26 | 0.653846 | 0.846154 | 0.884615 | 0.751099 | 3 |
| fault_type | unknown | 26 | 0.653846 | 0.846154 | 0.884615 | 0.751099 | 3 |
| fault_type | bandwidth | 42 | 0.666667 | 0.809524 | 0.857143 | 0.751808 | 6 |
| case_service | ts-order-other-service | 27 | 0.666667 | 0.851852 | 0.925926 | 0.783069 | 2 |
| time_bucket | ts5 | 258 | 0.670543 | 0.895349 | 0.945736 | 0.787606 | 14 |
| fault_type | request-replace-method | 190 | 0.694737 | 0.921053 | 0.984211 | 0.811487 | 3 |
| case_service | ts-basic-service | 201 | 0.696517 | 0.855721 | 0.945274 | 0.788379 | 11 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|loadgenerator|ts-travel-service|ts-seat-service|ts-order-other-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 28 | ts-travel-service|ts-config-service|ts-order-service|ts-food-service|ts-order-other-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 28 | ts-food-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-consign-service | container-kill | ts-food-service |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 27 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-verification-code-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 22 | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-verification-code-service | response-replace-code | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 21 | loadgenerator|ts-consign-service|ts-station-service|ts-route-plan-service|ts-basic-service | stress | ts-cancel-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 18 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-assurance-service|ts-travel-service | return | ts-cancel-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 18 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-auth-service | bandwidth | ts-station-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 17 | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 13 | ts-ui-dashboard|loadgenerator|ts-order-service|ts-travel-plan-service|ts-inside-payment-service | partition | ts-seat-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 13 | loadgenerator|ts-station-service|ts-order-service|ts-basic-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 12 | ts-preserve-service|ts-ui-dashboard|ts-travel2-service|ts-order-service|ts-consign-service | response-replace-body | ts-travel-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 11 | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-food-service|ts-travel-plan-service | bandwidth | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 11 | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-auth-service|ts-travel2-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 11 | ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-inside-payment-service|ts-payment-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-travel-plan-service|ts-travel2-service|ts-preserve-service|ts-route-plan-service|ts-contacts-service | response-replace-code | ts-basic-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 10 | ts-auth-service|ts-order-service|ts-security-service|ts-preserve-service|ts-verification-code-service | unknown | unknown |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-body | ts-basic-service |
| ts1-ts-route-service-corrupt-qlt7gn | mysql;ts-route-service | 9 | ts-auth-service|ts-ui-dashboard|ts-consign-service|ts-train-service|loadgenerator | corrupt | ts-route-service |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 9 | loadgenerator|ts-ui-dashboard|ts-verification-code-service|ts-food-service|ts-assurance-service | partition | ts-basic-service |
| ts4-ts-seat-service-bandwidth-k2bwt2 | ts-config-service;ts-seat-service | 9 | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-route-plan-service|ts-auth-service | bandwidth | ts-seat-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 8 | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-verification-code-service|ts-food-service | request-replace-method | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-travel-plan-service|ts-food-service | response-replace-body | ts-route-plan-service |
| ts4-ts-basic-service-corrupt-trd2kh | ts-basic-service;ts-preserve-service | 7 | ts-ui-dashboard|ts-verification-code-service|loadgenerator|ts-food-service|ts-contacts-service | corrupt | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jrv8dx | ts-basic-service;ts-price-service | 7 | ts-ui-dashboard|ts-auth-service|ts-travel2-service|ts-consign-service|loadgenerator | response-replace-body | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 7 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-travel-plan-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts5-ts-order-other-service-stress-6wvd48 | ts-order-other-service | 7 | ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|loadgenerator | stress | ts-order-other-service |
| ts5-ts-train-food-service-mysql-rswcbh | mysql;ts-train-food-service | 7 | loadgenerator|ts-basic-service|ts-ui-dashboard|ts-price-service|ts-order-service | unknown | unknown |
| ts7-mysql-loss-dxzvbj | mysql;ts-user-service | 7 | ts-ui-dashboard|loadgenerator|ts-travel-service|ts-auth-service|ts-consign-service | loss | mysql |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 7 | ts-payment-service|ts-verification-code-service|loadgenerator|ts-inside-payment-service|ts-food-service | request-abort | ts-ui-dashboard |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
