# EvidenceRank CREST1_RAW Summary

- Created: 2026-06-06T01:33:36+08:00
- Source: `CREST1_RAW`
- Algorithm: `crest`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.234177 |
| AC@3 | 0.511252 |
| AC@5 | 0.640647 |
| MRR | 0.419913 |
| avg_rank | 5.626582 |
| top1_miss | 1089 |
| top5_miss | 511 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | ts-security-service | 33 | 0.000000 | 0.454545 | 0.818182 | 0.275049 | 6 |
| case_service | ts-order-other-service | 27 | 0.000000 | 0.037037 | 0.148148 | 0.097158 | 23 |
| fault_type | pod-failure | 24 | 0.000000 | 0.083333 | 0.166667 | 0.123501 | 20 |
| case_service | ts-station-service | 20 | 0.000000 | 0.000000 | 0.000000 | 0.071692 | 20 |
| case_service | ts-assurance-service | 18 | 0.000000 | 0.166667 | 0.166667 | 0.109347 | 15 |
| case_service | ts-user-service | 15 | 0.000000 | 0.000000 | 0.000000 | 0.071853 | 15 |
| case_service | ts-config-service | 13 | 0.000000 | 0.000000 | 0.076923 | 0.080257 | 12 |
| case_service | ts-payment-service | 12 | 0.000000 | 0.000000 | 0.000000 | 0.061609 | 12 |
| case_service | ts-consign-price-service | 9 | 0.000000 | 0.000000 | 0.000000 | 0.062963 | 9 |
| case_service | ts-station-food-service | 9 | 0.000000 | 0.000000 | 0.000000 | 0.063943 | 9 |
| case_service | ts-price-service | 8 | 0.000000 | 0.000000 | 0.000000 | 0.079714 | 8 |
| case_service | ts-train-food-service | 7 | 0.000000 | 0.142857 | 0.142857 | 0.118607 | 6 |
| case_service | ts-cancel-service | 4 | 0.000000 | 0.250000 | 0.500000 | 0.160000 | 2 |
| case_service | ts-seat-service | 79 | 0.012658 | 0.189873 | 0.797468 | 0.249126 | 16 |
| case_service | ts-basic-service | 201 | 0.014925 | 0.089552 | 0.313433 | 0.188184 | 138 |
| case_service | ts-auth-service | 26 | 0.038462 | 0.730769 | 0.884615 | 0.343056 | 3 |
| case_service | ts-order-service | 45 | 0.044444 | 0.111111 | 0.177778 | 0.151072 | 37 |
| case_service | mysql | 72 | 0.055556 | 0.194444 | 0.263889 | 0.189408 | 53 |
| case_service | ts-contacts-service | 15 | 0.066667 | 0.266667 | 0.266667 | 0.197836 | 11 |
| case_service | ts-inside-payment-service | 28 | 0.071429 | 0.321429 | 0.642857 | 0.283291 | 10 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-travel-service|ts-auth-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | pod-failure | mysql |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 30 | ts-food-service|ts-travel-service|ts-travel2-service|ts-preserve-service|ts-ui-dashboard | container-kill | ts-food-service |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 29 | ts-ui-dashboard|ts-auth-service|ts-travel-service|ts-inside-payment-service|ts-basic-service | pod-failure | ts-travel-plan-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 25 | ts-route-plan-service|ts-travel2-service|loadgenerator|ts-food-service|ts-travel-plan-service | stress | ts-cancel-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 23 | ts-inside-payment-service|ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-payment-service |
| ts5-ts-train-food-service-mysql-rswcbh | mysql;ts-train-food-service | 23 | ts-travel-service|ts-preserve-service|loadgenerator|ts-travel2-service|ts-basic-service | unknown | unknown |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 22 | ts-travel-service|ts-food-service|ts-travel-plan-service|ts-preserve-service|ts-travel2-service | unknown | unknown |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | ts-consign-price-service | 20 | ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|loadgenerator|ts-travel-service | pod-failure | ts-consign-price-service |
| ts2-ts-order-other-service-container-kill-48rlds | ts-order-other-service | 19 | ts-travel2-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-seat-service | container-kill | ts-order-other-service |
| ts3-ts-station-service-return-4z45w8 | ts-station-service | 19 | ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-preserve-service|ts-route-plan-service | return | ts-station-service |
| ts4-ts-assurance-service-return-x28fwz | ts-assurance-service | 19 | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-preserve-service|ts-food-service | return | ts-assurance-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 18 | ts-ui-dashboard|ts-travel-service|ts-preserve-service|loadgenerator|ts-consign-service | bandwidth | ts-station-service |
| ts1-ts-config-service-latency-5kkcrc | ts-config-service | 18 | ts-ui-dashboard|ts-travel2-service|ts-travel-service|ts-preserve-service|ts-travel-plan-service | unknown | unknown |
| ts2-ts-station-service-dns-nn49s2 | mysql;ts-station-service | 18 | ts-ui-dashboard|ts-travel2-service|ts-travel-service|ts-travel-plan-service|loadgenerator | unknown | unknown |
| ts5-ts-order-other-service-stress-kv9nfz | ts-order-other-service | 18 | ts-travel2-service|ts-preserve-service|ts-travel-plan-service|ts-route-plan-service|ts-food-service | stress | ts-order-other-service |
| ts0-ts-config-service-stress-g6rpl9 | ts-config-service | 17 | ts-preserve-service|ts-travel2-service|ts-food-service|ts-seat-service|ts-travel-service | stress | ts-config-service |
| ts0-ts-station-food-service-stress-j5qdln | ts-station-food-service | 17 | ts-ui-dashboard|ts-food-service|ts-travel2-service|ts-travel-plan-service|ts-preserve-service | stress | ts-station-food-service |
| ts2-ts-order-other-service-stress-sv9xq6 | ts-order-other-service | 17 | ts-seat-service|ts-travel2-service|ts-preserve-service|ts-travel-service|ts-security-service | stress | ts-order-other-service |
| ts3-ts-train-food-service-stress-dqsrx2 | ts-train-food-service | 17 | ts-ui-dashboard|ts-food-service|loadgenerator|ts-travel2-service|ts-travel-service | stress | ts-train-food-service |
| ts4-ts-order-other-service-stress-h7rsps | ts-order-other-service | 17 | ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-travel-service|ts-seat-service | stress | ts-order-other-service |
| ts4-ts-order-other-service-stress-tm48k8 | ts-order-other-service | 17 | ts-travel2-service|ts-preserve-service|ts-seat-service|ts-route-plan-service|ts-travel-plan-service | stress | ts-order-other-service |
| ts5-ts-order-other-service-container-kill-p8t6kq | ts-order-other-service | 17 | ts-travel-plan-service|ts-travel2-service|ts-seat-service|ts-food-service|ts-ui-dashboard | container-kill | ts-order-other-service |
| ts5-ts-order-other-service-stress-6wvd48 | ts-order-other-service | 17 | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | stress | ts-order-other-service |
| ts6-ts-order-other-service-container-kill-8gfz95 | ts-order-other-service | 17 | ts-travel-plan-service|ts-preserve-service|ts-travel2-service|ts-ui-dashboard|ts-seat-service | container-kill | ts-order-other-service |
| ts7-mysql-loss-dxzvbj | mysql;ts-user-service | 17 | ts-travel-service|ts-ui-dashboard|ts-travel2-service|loadgenerator|ts-travel-plan-service | loss | mysql |
| ts0-mysql-loss-67k278 | mysql;ts-train-service | 16 | ts-ui-dashboard|ts-travel-service|ts-travel-plan-service|ts-travel2-service|loadgenerator | loss | mysql |
| ts0-ts-order-other-service-stress-4d76fr | ts-order-other-service | 16 | ts-preserve-service|ts-travel2-service|ts-seat-service|ts-travel-plan-service|ts-route-plan-service | stress | ts-order-other-service |
| ts0-ts-order-service-stress-xt9wfq | ts-order-service | 16 | ts-ui-dashboard|ts-seat-service|ts-travel-service|ts-travel2-service|ts-food-service | stress | ts-order-service |
| ts0-ts-payment-service-stress-56jvjc | ts-payment-service | 16 | ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|ts-travel-service|ts-inside-payment-service | stress | ts-payment-service |
| ts0-ts-route-service-stress-kstvv2 | ts-route-service | 16 | ts-travel-service|ts-ui-dashboard|ts-basic-service|ts-food-service|ts-travel2-service | stress | ts-route-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
