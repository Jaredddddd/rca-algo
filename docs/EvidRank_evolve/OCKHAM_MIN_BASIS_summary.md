# EvidenceRank OCKHAM_MIN_BASIS Summary

- Created: 2026-06-14T20:55:26+08:00
- Source: `OCKHAM_MIN_BASIS`
- Algorithm: `crest_ockham_min_basis`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.457103 |
| AC@3 | 0.756681 |
| AC@5 | 0.845992 |
| MRR | 0.624685 |
| avg_rank | 3.289733 |
| top1_miss | 772 |
| top5_miss | 219 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | ts-config-service | 13 | 0.000000 | 0.538462 | 0.615385 | 0.248385 | 5 |
| case_service | ts-cancel-service | 4 | 0.000000 | 0.250000 | 0.250000 | 0.152949 | 3 |
| fault_type | pod-failure | 24 | 0.041667 | 0.125000 | 0.333333 | 0.166479 | 16 |
| fault_type | delay | 21 | 0.047619 | 0.285714 | 0.428571 | 0.223663 | 12 |
| fault_type | container-kill | 89 | 0.089888 | 0.573034 | 0.764045 | 0.350564 | 21 |
| case_service | ts-assurance-service | 18 | 0.111111 | 0.833333 | 0.833333 | 0.416336 | 3 |
| case_service | ts-route-service | 23 | 0.130435 | 0.434783 | 0.652174 | 0.347809 | 8 |
| case_service | ts-user-service | 15 | 0.133333 | 0.333333 | 0.533333 | 0.317517 | 7 |
| fault_type | stress | 173 | 0.144509 | 0.485549 | 0.647399 | 0.357508 | 61 |
| case_service | unknown | 26 | 0.153846 | 0.461538 | 0.461538 | 0.324893 | 14 |
| fault_type | unknown | 26 | 0.153846 | 0.461538 | 0.461538 | 0.324893 | 14 |
| case_service | ts-order-service | 45 | 0.155556 | 0.466667 | 0.600000 | 0.357216 | 18 |
| case_service | ts-inside-payment-service | 28 | 0.214286 | 0.535714 | 0.714286 | 0.419884 | 8 |
| fault_type | corrupt | 46 | 0.217391 | 0.630435 | 0.717391 | 0.428226 | 13 |
| time_bucket | ts9 | 23 | 0.217391 | 0.695652 | 0.782609 | 0.472547 | 5 |
| case_service | ts-order-other-service | 27 | 0.222222 | 0.333333 | 0.407407 | 0.358316 | 16 |
| case_service | ts-station-food-service | 9 | 0.222222 | 0.444444 | 0.555556 | 0.409206 | 4 |
| fault_type | request-delay | 88 | 0.227273 | 0.670455 | 0.875000 | 0.482553 | 11 |
| fault_type | response-delay | 89 | 0.235955 | 0.651685 | 0.808989 | 0.472253 | 17 |
| time_bucket | ts6 | 28 | 0.250000 | 0.714286 | 0.785714 | 0.498937 | 6 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-food-service|ts-travel-service|ts-assurance-service|ts-order-service|ts-travel-plan-service | unknown | unknown |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | loadgenerator|ts-auth-service|ts-ui-dashboard|ts-route-plan-service|ts-travel2-service | pod-failure | mysql |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 30 | loadgenerator|ts-station-service|ts-consign-service|ts-basic-service|ts-ui-dashboard | stress | ts-cancel-service |
| ts5-ts-train-food-service-mysql-rswcbh | mysql;ts-train-food-service | 30 | loadgenerator|ts-basic-service|ts-ui-dashboard|ts-station-service|ts-consign-service | unknown | unknown |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 29 | ts-inside-payment-service|ts-order-service|ts-basic-service|ts-seat-service|ts-route-plan-service | pod-failure | ts-payment-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 28 | ts-ui-dashboard|loadgenerator|ts-travel-service|ts-basic-service|ts-food-service | pod-failure | ts-consign-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | ts-route-plan-service | 28 | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-travel2-service | pod-failure | ts-route-plan-service |
| ts0-ts-cancel-service-stress-s7tf69 | ts-cancel-service | 26 | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-service|ts-seat-service | stress | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 26 | loadgenerator|ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-food-service | container-kill | ts-food-service |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 25 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-user-service|ts-execute-service | pod-failure | ts-travel-plan-service |
| ts0-ts-user-service-pod-failure-b44c7f | ts-user-service | 25 | loadgenerator|ts-ui-dashboard|ts-preserve-service|ts-basic-service|ts-auth-service | pod-failure | ts-user-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | ts-station-food-service | 25 | ts-food-service|ts-travel-service|ts-basic-service|ts-train-food-service|ts-station-service | pod-failure | ts-station-food-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 25 | ts-auth-service|ts-verification-code-service|ts-ui-dashboard|ts-order-service|ts-preserve-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 25 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-route-plan-service|ts-travel2-service | return | ts-cancel-service |
| ts2-ts-station-service-dns-nn49s2 | mysql;ts-station-service | 25 | ts-consign-service|ts-ui-dashboard|ts-travel-plan-service|ts-consign-price-service|loadgenerator | unknown | unknown |
| ts9-ts-preserve-service-pod-failure-6w29wr | ts-preserve-service | 25 | loadgenerator|ts-ui-dashboard|ts-verification-code-service|ts-order-service|ts-auth-service | pod-failure | ts-preserve-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 24 | loadgenerator|ts-basic-service|ts-station-service|ts-ui-dashboard|ts-price-service | pod-failure | ts-assurance-service |
| ts2-ts-inside-payment-service-stress-9vnqwf | ts-inside-payment-service | 24 | ts-order-service|ts-seat-service|ts-cancel-service|ts-basic-service|ts-travel-service | stress | ts-inside-payment-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | ts-travel2-service | 24 | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-ui-dashboard|ts-basic-service | pod-failure | ts-travel2-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 24 | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-travel2-service|ts-travel-service | pod-failure | ts-price-service |
| ts1-ts-config-service-latency-5kkcrc | ts-config-service | 23 | ts-consign-service|ts-ui-dashboard|ts-preserve-service|ts-order-service|ts-travel2-service | unknown | unknown |
| ts5-ts-order-other-service-stress-6wvd48 | ts-order-other-service | 23 | ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service | stress | ts-order-other-service |
| ts8-ts-food-service-pod-failure-9swgtb | ts-food-service | 23 | loadgenerator|ts-ui-dashboard|ts-consign-service|ts-contacts-service|ts-basic-service | pod-failure | ts-food-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 22 | ts-auth-service|ts-verification-code-service|ts-ui-dashboard|ts-train-service|loadgenerator | container-kill | mysql |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 22 | ts-consign-service|ts-ui-dashboard|ts-food-service|ts-consign-price-service|ts-auth-service | bandwidth | ts-station-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | ts-travel-service | 20 | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-order-service|ts-ui-dashboard | pod-failure | ts-travel-service |
| ts3-ts-config-service-corrupt-7r594z | mysql;ts-config-service | 20 | loadgenerator|ts-ui-dashboard|ts-travel-plan-service|ts-food-service|ts-route-plan-service | corrupt | ts-config-service |
| ts4-ts-travel-service-stress-fz5lbn | ts-travel-service | 20 | ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-route-plan-service|ts-auth-service | stress | ts-travel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 20 | ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-travel-plan-service|ts-auth-service | response-replace-code | ts-basic-service |
| ts2-ts-route-plan-service-return-xw84fv | ts-route-plan-service | 19 | ts-consign-service|ts-ui-dashboard|ts-auth-service|ts-food-service|ts-travel2-service | return | ts-route-plan-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
