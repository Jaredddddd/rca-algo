# EvidenceRank V13_REIMPL Summary

- Created: 2026-06-03T12:06:14+08:00
- Source: `V13_REIMPL`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.583685 |
| AC@3 | 0.910689 |
| AC@5 | 0.955696 |
| MRR | 0.747704 |
| avg_rank | 2.077356 |
| top1_miss | 592 |
| top5_miss | 63 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.041667 | 0.125000 | 0.250000 | 0.159286 | 18 |
| case_service | ts-config-service | 13 | 0.076923 | 0.769231 | 1.000000 | 0.447436 | 0 |
| case_service | ts-cancel-service | 4 | 0.250000 | 0.500000 | 0.500000 | 0.392549 | 2 |
| case_service | ts-station-service | 20 | 0.300000 | 0.700000 | 0.750000 | 0.546925 | 5 |
| case_service | ts-auth-service | 26 | 0.307692 | 0.923077 | 1.000000 | 0.600641 | 0 |
| fault_type | return | 21 | 0.333333 | 0.761905 | 0.809524 | 0.549450 | 4 |
| case_service | ts-payment-service | 12 | 0.333333 | 0.750000 | 0.916667 | 0.564087 | 1 |
| fault_type | response-replace-body | 51 | 0.372549 | 0.862745 | 0.941176 | 0.623856 | 3 |
| case_service | ts-basic-service | 201 | 0.378109 | 0.850746 | 0.945274 | 0.611447 | 11 |
| case_service | ts-travel2-service | 68 | 0.411765 | 0.926471 | 0.955882 | 0.644690 | 3 |
| case_service | ts-train-service | 17 | 0.411765 | 0.882353 | 0.941176 | 0.642157 | 1 |
| case_service | ts-security-service | 33 | 0.424242 | 1.000000 | 1.000000 | 0.702020 | 0 |
| case_service | ts-consign-price-service | 9 | 0.444444 | 0.888889 | 0.888889 | 0.671717 | 1 |
| fault_type | stress | 173 | 0.473988 | 0.924855 | 0.988439 | 0.701234 | 2 |
| case_service | ts-route-service | 23 | 0.478261 | 0.695652 | 0.956522 | 0.657246 | 1 |
| fault_type | corrupt | 46 | 0.500000 | 0.869565 | 0.978261 | 0.693841 | 1 |
| case_service | unknown | 26 | 0.500000 | 0.769231 | 0.807692 | 0.650097 | 5 |
| fault_type | unknown | 26 | 0.500000 | 0.769231 | 0.807692 | 0.650097 | 5 |
| case_service | ts-verification-code-service | 4 | 0.500000 | 1.000000 | 1.000000 | 0.750000 | 0 |
| time_bucket | ts2 | 221 | 0.506787 | 0.936652 | 0.963801 | 0.711784 | 8 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 32 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 32 | ts-auth-service|ts-travel-service|ts-seat-service|ts-route-plan-service|ts-food-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-food-service|ts-travel-service|ts-config-service|ts-order-service|ts-order-other-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 29 | ts-inside-payment-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-station-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-consign-service | container-kill | ts-food-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 28 | ts-inside-payment-service|ts-order-other-service|ts-basic-service|ts-order-service|ts-travel2-service | pod-failure | ts-payment-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 28 | ts-consign-service|ts-food-service|ts-basic-service|loadgenerator|ts-route-plan-service | stress | ts-cancel-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | ts-station-food-service | 22 | ts-food-service|ts-travel-service|ts-basic-service|ts-order-other-service|ts-ui-dashboard | pod-failure | ts-station-food-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 22 | ts-travel-service|ts-security-service|ts-order-service|ts-preserve-service|ts-auth-service | unknown | unknown |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 22 | ts-basic-service|ts-travel-service|ts-route-plan-service|ts-station-service|ts-seat-service | pod-failure | ts-assurance-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | ts-consign-price-service | 22 | ts-consign-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-seat-service | pod-failure | ts-consign-price-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 21 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-travel2-service | container-kill | mysql |
| ts8-ts-food-service-pod-failure-9swgtb | ts-food-service | 21 | ts-order-service|ts-seat-service|ts-basic-service|ts-station-service|ts-ui-dashboard | pod-failure | ts-food-service |
| ts9-ts-preserve-service-pod-failure-6w29wr | ts-preserve-service | 19 | ts-verification-code-service|loadgenerator|ts-inside-payment-service|ts-order-service|ts-seat-service | pod-failure | ts-preserve-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | ts-route-plan-service | 16 | ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-order-other-service|ts-payment-service | pod-failure | ts-route-plan-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 16 | ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service|ts-route-plan-service | pod-failure | ts-price-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 15 | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-food-service|ts-seat-service | pod-failure | ts-consign-service |
| ts1-ts-config-service-latency-5kkcrc | ts-config-service | 14 | ts-consign-service|ts-ui-dashboard|ts-food-service|ts-basic-service|ts-preserve-service | unknown | unknown |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 14 | ts-preserve-service|ts-ui-dashboard|ts-payment-service|ts-seat-service|ts-food-service | response-replace-code | ts-basic-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | ts-travel-service | 13 | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-basic-service | pod-failure | ts-travel-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 13 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-order-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-train-food-service-mysql-rswcbh | mysql;ts-train-food-service | 13 | ts-basic-service|loadgenerator|ts-preserve-service|ts-travel-service|ts-ui-dashboard | unknown | unknown |
| ts2-ts-station-service-dns-nn49s2 | mysql;ts-station-service | 11 | ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-food-service|ts-basic-service | unknown | unknown |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 11 | ts-food-service|ts-seat-service|ts-order-service|ts-travel-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 11 | ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-travel2-service|ts-auth-service | bandwidth | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 11 | ts-inside-payment-service|ts-food-service|ts-assurance-service|ts-payment-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 10 | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-route-plan-service|ts-travel2-service | response-replace-code | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 10 | ts-ui-dashboard|ts-food-service|ts-payment-service|ts-basic-service|loadgenerator | response-replace-body | ts-route-plan-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
