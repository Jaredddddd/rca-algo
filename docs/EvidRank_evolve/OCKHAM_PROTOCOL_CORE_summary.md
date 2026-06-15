# EvidenceRank OCKHAM_PROTOCOL_CORE Summary

- Created: 2026-06-14T20:55:52+08:00
- Source: `OCKHAM_PROTOCOL_CORE`
- Algorithm: `crest_ockham_protocol_core`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.483826 |
| AC@3 | 0.757384 |
| AC@5 | 0.857947 |
| MRR | 0.641656 |
| avg_rank | 3.226442 |
| top1_miss | 734 |
| top5_miss | 202 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | ts-cancel-service | 4 | 0.000000 | 0.250000 | 0.250000 | 0.172801 | 3 |
| case_service | ts-verification-code-service | 4 | 0.000000 | 1.000000 | 1.000000 | 0.375000 | 0 |
| fault_type | delay | 21 | 0.047619 | 0.095238 | 0.285714 | 0.175723 | 15 |
| case_service | ts-config-service | 13 | 0.076923 | 0.461538 | 0.538462 | 0.284360 | 6 |
| fault_type | pod-failure | 24 | 0.125000 | 0.583333 | 0.833333 | 0.383420 | 4 |
| case_service | ts-route-service | 23 | 0.130435 | 0.391304 | 0.521739 | 0.330382 | 11 |
| case_service | ts-user-service | 15 | 0.133333 | 0.400000 | 0.600000 | 0.334940 | 6 |
| fault_type | corrupt | 46 | 0.152174 | 0.521739 | 0.673913 | 0.368396 | 15 |
| fault_type | container-kill | 89 | 0.168539 | 0.595506 | 0.831461 | 0.412989 | 15 |
| fault_type | request-delay | 88 | 0.181818 | 0.590909 | 0.818182 | 0.427948 | 16 |
| case_service | ts-order-other-service | 27 | 0.185185 | 0.333333 | 0.444444 | 0.335994 | 15 |
| fault_type | stress | 173 | 0.196532 | 0.549133 | 0.705202 | 0.416963 | 51 |
| case_service | ts-order-service | 45 | 0.200000 | 0.444444 | 0.711111 | 0.392649 | 13 |
| fault_type | response-delay | 89 | 0.202247 | 0.539326 | 0.719101 | 0.426499 | 25 |
| case_service | ts-station-food-service | 9 | 0.222222 | 0.444444 | 0.666667 | 0.425309 | 3 |
| time_bucket | ts6 | 28 | 0.250000 | 0.642857 | 0.821429 | 0.501935 | 5 |
| case_service | ts-station-service | 20 | 0.250000 | 0.400000 | 0.500000 | 0.389097 | 10 |
| case_service | ts-price-service | 8 | 0.250000 | 0.750000 | 0.750000 | 0.515625 | 2 |
| time_bucket | ts9 | 23 | 0.260870 | 0.695652 | 0.869565 | 0.511284 | 3 |
| case_service | ts-seat-service | 79 | 0.265823 | 0.518987 | 0.784810 | 0.449693 | 17 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 44 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-route-plan-service|ts-travel2-service | return | ts-cancel-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 32 | ts-auth-service|ts-order-service|ts-travel-service|ts-security-service|ts-preserve-service | unknown | unknown |
| ts3-mysql-pod-failure-58qts5 | mysql | 32 | loadgenerator|ts-auth-service|ts-ui-dashboard|ts-assurance-service|ts-verification-code-service | pod-failure | mysql |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 31 | loadgenerator|ts-ui-dashboard|ts-food-service|ts-consign-service|ts-assurance-service | container-kill | ts-food-service |
| ts5-ts-train-food-service-mysql-rswcbh | mysql;ts-train-food-service | 28 | loadgenerator|ts-basic-service|ts-ui-dashboard|ts-consign-service|ts-station-service | unknown | unknown |
| ts4-ts-travel-service-stress-fz5lbn | ts-travel-service | 27 | ts-ui-dashboard|ts-travel-plan-service|loadgenerator|ts-route-plan-service|ts-cancel-service | stress | ts-travel-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 26 | ts-auth-service|ts-train-service|ts-ui-dashboard|ts-order-service|ts-verification-code-service | container-kill | mysql |
| ts1-mysql-delay-hx85fg | mysql;ts-config-service | 26 | loadgenerator|ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-verification-code-service | delay | mysql |
| ts2-ts-station-service-dns-nn49s2 | mysql;ts-station-service | 26 | ts-consign-service|ts-ui-dashboard|ts-consign-price-service|ts-assurance-service|ts-verification-code-service | unknown | unknown |
| ts3-ts-config-service-corrupt-7r594z | mysql;ts-config-service | 25 | loadgenerator|ts-ui-dashboard|ts-food-service|ts-travel-plan-service|ts-consign-service | corrupt | ts-config-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 23 | ts-consign-service|ts-ui-dashboard|ts-consign-price-service|ts-assurance-service|ts-food-service | bandwidth | ts-station-service |
| ts1-ts-station-service-delay-hwcd55 | mysql;ts-station-service | 23 | loadgenerator|ts-ui-dashboard|ts-consign-service|ts-assurance-service|ts-auth-service | delay | ts-station-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 23 | loadgenerator|ts-consign-service|ts-station-service|ts-basic-service|ts-ui-dashboard | stress | ts-cancel-service |
| ts5-ts-order-other-service-stress-6wvd48 | ts-order-other-service | 23 | ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service | stress | ts-order-other-service |
| ts1-ts-config-service-latency-5kkcrc | ts-config-service | 22 | ts-consign-service|ts-ui-dashboard|ts-order-service|ts-preserve-service|ts-travel2-service | unknown | unknown |
| ts7-mysql-loss-dxzvbj | mysql;ts-user-service | 22 | loadgenerator|ts-ui-dashboard|ts-consign-service|ts-food-service|ts-order-service | loss | mysql |
| ts4-ts-order-other-service-exception-x566nt | ts-order-other-service | 21 | ts-consign-service|ts-inside-payment-service|ts-assurance-service|ts-cancel-service|ts-consign-price-service | exception | ts-order-other-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 21 | ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-travel-plan-service|ts-cancel-service | response-replace-code | ts-basic-service |
| ts1-ts-config-service-delay-vlf2nr | mysql;ts-config-service | 20 | ts-ui-dashboard|loadgenerator|ts-consign-service|ts-auth-service|ts-food-service | delay | ts-config-service |
| ts1-ts-route-service-latency-vhk7dz | ts-route-service | 20 | ts-ui-dashboard|ts-route-plan-service|ts-train-service|ts-travel2-service|ts-travel-plan-service | unknown | unknown |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 20 | loadgenerator|ts-ui-dashboard|ts-inside-payment-service|ts-order-service|ts-cancel-service | partition | ts-seat-service |
| ts4-ts-train-service-latency-5gvbsq | ts-train-service | 20 | loadgenerator|ts-ui-dashboard|ts-travel-plan-service|ts-travel2-service|ts-seat-service | unknown | unknown |
| ts1-ts-travel-service-return-zbss2p | ts-travel-service | 18 | ts-consign-service|ts-food-service|ts-assurance-service|ts-preserve-service|ts-ui-dashboard | return | ts-travel-service |
| ts2-mysql-delay-d427wn | mysql;ts-route-service | 18 | loadgenerator|ts-ui-dashboard|ts-consign-service|ts-food-service|ts-order-service | delay | mysql |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 18 | loadgenerator|ts-ui-dashboard|ts-consign-price-service|ts-consign-service|ts-travel-plan-service | partition | ts-basic-service |
| ts4-ts-order-other-service-stress-h7rsps | ts-order-other-service | 18 | ts-route-plan-service|ts-travel2-service|ts-security-service|ts-travel-plan-service|ts-consign-service | stress | ts-order-other-service |
| ts1-ts-order-service-delay-mxmrwz | mysql;ts-order-service | 17 | loadgenerator|ts-ui-dashboard|ts-consign-service|ts-assurance-service|ts-travel-service | delay | ts-order-service |
| ts2-ts-food-service-response-delay-drcx9w | ts-food-service;ts-train-food-service | 17 | loadgenerator|ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-basic-service | response-delay | ts-food-service |
| ts3-mysql-corrupt-5h87jc | mysql;ts-train-service | 17 | ts-ui-dashboard|ts-consign-service|ts-assurance-service|ts-food-service|ts-travel2-service | corrupt | mysql |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 17 | ts-preserve-service|ts-assurance-service|ts-ui-dashboard|ts-consign-service|ts-travel-plan-service | response-replace-body | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
