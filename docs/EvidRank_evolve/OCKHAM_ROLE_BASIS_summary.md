# EvidenceRank OCKHAM_ROLE_BASIS Summary

- Created: 2026-06-14T20:55:00+08:00
- Source: `OCKHAM_ROLE_BASIS`
- Algorithm: `crest_ockham_role_basis`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.623769 |
| AC@3 | 0.884669 |
| AC@5 | 0.939522 |
| MRR | 0.757144 |
| avg_rank | 2.286217 |
| top1_miss | 535 |
| top5_miss | 86 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.000000 | 0.125000 | 0.375000 | 0.139340 | 15 |
| case_service | ts-cancel-service | 4 | 0.000000 | 0.250000 | 0.500000 | 0.192241 | 2 |
| case_service | ts-station-service | 20 | 0.250000 | 0.700000 | 0.750000 | 0.490739 | 5 |
| case_service | ts-verification-code-service | 4 | 0.250000 | 1.000000 | 1.000000 | 0.583333 | 0 |
| case_service | ts-order-service | 45 | 0.266667 | 0.822222 | 0.977778 | 0.543545 | 1 |
| fault_type | container-kill | 89 | 0.269663 | 0.831461 | 0.910112 | 0.538812 | 8 |
| fault_type | stress | 173 | 0.317919 | 0.768786 | 0.872832 | 0.559473 | 22 |
| case_service | ts-user-service | 15 | 0.333333 | 0.533333 | 0.666667 | 0.485444 | 5 |
| case_service | ts-payment-service | 12 | 0.333333 | 0.833333 | 0.833333 | 0.544540 | 2 |
| case_service | ts-station-food-service | 9 | 0.333333 | 0.666667 | 0.777778 | 0.522037 | 2 |
| case_service | unknown | 26 | 0.346154 | 0.653846 | 0.730769 | 0.502611 | 7 |
| fault_type | unknown | 26 | 0.346154 | 0.653846 | 0.730769 | 0.502611 | 7 |
| case_service | ts-route-service | 23 | 0.347826 | 0.695652 | 0.913043 | 0.544203 | 2 |
| case_service | ts-order-other-service | 27 | 0.407407 | 0.703704 | 0.851852 | 0.582942 | 4 |
| case_service | ts-seat-service | 79 | 0.417722 | 0.860759 | 0.962025 | 0.629315 | 3 |
| case_service | ts-inside-payment-service | 28 | 0.428571 | 0.857143 | 0.928571 | 0.660714 | 2 |
| fault_type | delay | 21 | 0.428571 | 0.952381 | 1.000000 | 0.612698 | 0 |
| case_service | ts-config-service | 13 | 0.461538 | 0.769231 | 0.846154 | 0.638462 | 2 |
| case_service | ts-train-service | 17 | 0.470588 | 0.823529 | 0.941176 | 0.653922 | 1 |
| fault_type | return | 21 | 0.476190 | 0.619048 | 0.666667 | 0.591685 | 7 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts3-mysql-pod-failure-58qts5 | mysql | 32 | ts-auth-service|loadgenerator|ts-travel-service|ts-seat-service|ts-order-other-service | pod-failure | mysql |
| ts2-mysql-pod-kill-xvzmxb | mysql | 31 | ts-auth-service|ts-order-service|ts-security-service|ts-preserve-service|ts-travel-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 29 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-route-plan-service|ts-travel-service | return | ts-cancel-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 29 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-basic-service|ts-order-other-service | pod-failure | ts-payment-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-ui-dashboard|loadgenerator|ts-consign-service|ts-assurance-service | container-kill | ts-food-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 29 | loadgenerator|ts-station-service|ts-basic-service|ts-consign-service|ts-route-service | stress | ts-cancel-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 28 | ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-seat-service|ts-verification-code-service | pod-failure | ts-consign-service |
| ts5-ts-train-food-service-mysql-rswcbh | mysql;ts-train-food-service | 28 | loadgenerator|ts-basic-service|ts-ui-dashboard|ts-order-service|ts-station-service | unknown | unknown |
| ts0-mysql-container-kill-9t6n24 | mysql | 27 | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|ts-order-service | container-kill | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 27 | ts-travel-service|ts-food-service|ts-order-service|ts-config-service|ts-seat-service | unknown | unknown |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 26 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-user-service|ts-verification-code-service | pod-failure | ts-travel-plan-service |
| ts0-ts-user-service-pod-failure-b44c7f | ts-user-service | 25 | loadgenerator|ts-ui-dashboard|ts-preserve-service|ts-basic-service|ts-order-service | pod-failure | ts-user-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | ts-station-food-service | 25 | ts-food-service|ts-travel-service|ts-basic-service|ts-seat-service|ts-train-food-service | pod-failure | ts-station-food-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 24 | ts-basic-service|ts-station-service|ts-seat-service|ts-travel-service|ts-price-service | pod-failure | ts-assurance-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | ts-travel2-service | 24 | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-ui-dashboard|ts-basic-service | pod-failure | ts-travel2-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 24 | ts-basic-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-travel-service | pod-failure | ts-price-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | ts-route-plan-service | 22 | ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-order-other-service|ts-train-service | pod-failure | ts-route-plan-service |
| ts8-ts-food-service-pod-failure-9swgtb | ts-food-service | 22 | ts-ui-dashboard|loadgenerator|ts-basic-service|ts-order-service|ts-contacts-service | pod-failure | ts-food-service |
| ts1-ts-config-service-latency-5kkcrc | ts-config-service | 20 | ts-consign-service|ts-ui-dashboard|ts-travel2-service|ts-preserve-service|ts-order-service | unknown | unknown |
| ts2-ts-travel-service-pod-failure-jqk2bj | ts-travel-service | 20 | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-order-service|ts-travel2-service | pod-failure | ts-travel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 20 | ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-travel-plan-service|ts-verification-code-service | response-replace-code | ts-basic-service |
| ts2-ts-station-service-dns-nn49s2 | mysql;ts-station-service | 19 | ts-consign-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel2-service|ts-seat-service | unknown | unknown |
| ts4-ts-travel-service-stress-fz5lbn | ts-travel-service | 18 | ts-ui-dashboard|ts-travel-plan-service|loadgenerator|ts-route-plan-service|ts-preserve-service | stress | ts-travel-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 17 | ts-travel-plan-service|ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-route-service | bandwidth | ts-station-service |
| ts2-ts-order-other-service-container-kill-48rlds | ts-order-other-service | 16 | ts-seat-service|ts-ui-dashboard|ts-preserve-service|ts-consign-service|ts-travel2-service | container-kill | ts-order-other-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | ts-consign-price-service | 16 | ts-consign-service|ts-ui-dashboard|ts-travel-plan-service|ts-preserve-service|ts-auth-service | pod-failure | ts-consign-price-service |
| ts9-ts-preserve-service-pod-failure-6w29wr | ts-preserve-service | 16 | loadgenerator|ts-order-service|ts-inside-payment-service|ts-ui-dashboard|ts-verification-code-service | pod-failure | ts-preserve-service |
| ts4-ts-order-other-service-stress-h7rsps | ts-order-other-service | 15 | ts-route-plan-service|ts-travel2-service|ts-security-service|ts-basic-service|ts-consign-service | stress | ts-order-other-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 15 | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-assurance-service|ts-travel-plan-service | response-replace-body | ts-travel-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 14 | ts-consign-service|ts-ui-dashboard|ts-verification-code-service|ts-travel-plan-service|ts-food-service | bandwidth | ts-station-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
