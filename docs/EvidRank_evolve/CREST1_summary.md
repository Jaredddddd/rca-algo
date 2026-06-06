# EvidenceRank CREST1 Summary

- Created: 2026-06-06T02:12:25+08:00
- Source: `CREST1`
- Algorithm: `crest`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.699719 |
| AC@3 | 0.916315 |
| AC@5 | 0.952180 |
| MRR | 0.811469 |
| avg_rank | 1.923347 |
| top1_miss | 427 |
| top5_miss | 68 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.000000 | 0.166667 | 0.291667 | 0.141647 | 17 |
| case_service | ts-cancel-service | 4 | 0.250000 | 0.500000 | 0.500000 | 0.392549 | 2 |
| case_service | ts-route-service | 23 | 0.434783 | 0.826087 | 0.913043 | 0.633696 | 2 |
| fault_type | return | 21 | 0.476190 | 0.761905 | 0.809524 | 0.646200 | 4 |
| case_service | ts-order-other-service | 27 | 0.481481 | 0.851852 | 0.925926 | 0.676279 | 2 |
| case_service | ts-station-service | 20 | 0.500000 | 0.750000 | 0.750000 | 0.643452 | 5 |
| case_service | ts-payment-service | 12 | 0.500000 | 0.833333 | 0.916667 | 0.676944 | 1 |
| case_service | ts-verification-code-service | 4 | 0.500000 | 1.000000 | 1.000000 | 0.750000 | 0 |
| time_bucket | ts9 | 23 | 0.521739 | 0.826087 | 0.869565 | 0.696223 | 3 |
| case_service | ts-train-service | 17 | 0.529412 | 0.941176 | 0.941176 | 0.725490 | 1 |
| time_bucket | ts6 | 28 | 0.571429 | 0.857143 | 0.928571 | 0.738706 | 2 |
| case_service | unknown | 26 | 0.576923 | 0.807692 | 0.807692 | 0.699946 | 5 |
| fault_type | unknown | 26 | 0.576923 | 0.807692 | 0.807692 | 0.699946 | 5 |
| case_service | ts-order-service | 45 | 0.577778 | 0.977778 | 1.000000 | 0.768519 | 0 |
| time_bucket | ts7 | 34 | 0.588235 | 0.794118 | 0.911765 | 0.708088 | 3 |
| case_service | ts-travel-service | 92 | 0.597826 | 0.902174 | 0.967391 | 0.758424 | 3 |
| fault_type | stress | 173 | 0.601156 | 0.930636 | 0.988439 | 0.768126 | 2 |
| fault_type | corrupt | 46 | 0.608696 | 0.913043 | 0.934783 | 0.756703 | 3 |
| case_service | ts-config-service | 13 | 0.615385 | 1.000000 | 1.000000 | 0.782051 | 0 |
| fault_type | bandwidth | 42 | 0.619048 | 0.833333 | 0.880952 | 0.735754 | 5 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|loadgenerator|ts-order-other-service|ts-seat-service | pod-failure | mysql |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 29 | ts-inside-payment-service|ts-station-service|ts-assurance-service|ts-travel-service|ts-seat-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|loadgenerator|ts-ui-dashboard|ts-consign-service|ts-assurance-service | container-kill | ts-food-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 28 | ts-config-service|ts-food-service|ts-travel-service|ts-order-service|ts-order-other-service | unknown | unknown |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 28 | ts-consign-service|loadgenerator|ts-food-service|ts-basic-service|ts-route-plan-service | stress | ts-cancel-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | ts-consign-price-service | 25 | ts-consign-service|ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-seat-service | pod-failure | ts-consign-price-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 25 | ts-inside-payment-service|ts-order-other-service|ts-order-service|ts-basic-service|ts-travel2-service | pod-failure | ts-payment-service |
| ts8-ts-food-service-pod-failure-9swgtb | ts-food-service | 21 | ts-order-service|ts-station-service|ts-seat-service|ts-basic-service|ts-contacts-service | pod-failure | ts-food-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 20 | ts-station-service|ts-basic-service|ts-route-plan-service|ts-travel-service|ts-route-service | pod-failure | ts-assurance-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 19 | ts-security-service|ts-order-service|ts-auth-service|ts-travel-service|ts-preserve-service | unknown | unknown |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 19 | ts-basic-service|ts-travel-service|ts-food-service|ts-ui-dashboard|ts-seat-service | pod-failure | ts-consign-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 19 | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-user-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 18 | ts-travel2-service|ts-travel-plan-service|ts-basic-service|ts-travel-service|ts-route-plan-service | pod-failure | ts-price-service |
| ts9-ts-preserve-service-pod-failure-6w29wr | ts-preserve-service | 18 | loadgenerator|ts-verification-code-service|ts-inside-payment-service|ts-food-service|ts-order-service | pod-failure | ts-preserve-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 17 | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-seat-service|ts-order-service | bandwidth | ts-route-plan-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 15 | ts-order-service|ts-food-service|ts-seat-service|ts-travel-service|ts-station-service | request-abort | ts-ui-dashboard |
| ts0-mysql-container-kill-9t6n24 | mysql | 14 | ts-auth-service|ts-train-service|ts-ui-dashboard|ts-verification-code-service|loadgenerator | container-kill | mysql |
| ts1-ts-config-service-latency-5kkcrc | ts-config-service | 13 | ts-consign-service|ts-ui-dashboard|ts-basic-service|ts-travel2-service|ts-food-service | unknown | unknown |
| ts1-ts-station-food-service-pod-failure-td2qj4 | ts-station-food-service | 13 | ts-food-service|ts-travel-service|ts-basic-service|ts-order-other-service|ts-auth-service | pod-failure | ts-station-food-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | ts-travel-service | 12 | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service | pod-failure | ts-travel-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 12 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | bandwidth | ts-station-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-contacts-service|ts-seat-service|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | ts-route-plan-service | 11 | ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-order-other-service|ts-travel2-service | pod-failure | ts-route-plan-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 11 | ts-food-service|ts-assurance-service|ts-inside-payment-service|ts-basic-service|ts-payment-service | request-abort | ts-ui-dashboard |
| ts0-ts-user-service-pod-failure-b44c7f | ts-user-service | 10 | ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-travel-service|ts-auth-service | pod-failure | ts-user-service |
| ts2-ts-station-service-dns-nn49s2 | mysql;ts-station-service | 10 | ts-consign-service|ts-seat-service|ts-ui-dashboard|ts-food-service|ts-basic-service | unknown | unknown |
| ts4-ts-basic-service-corrupt-trd2kh | ts-basic-service;ts-preserve-service | 10 | ts-ui-dashboard|ts-seat-service|loadgenerator|ts-verification-code-service|ts-contacts-service | corrupt | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 10 | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service | response-replace-code | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
