# EvidenceRank CREST10_VICTIM_SUPPRESSION Summary

- Created: 2026-06-07T20:41:22+08:00
- Source: `CREST10_VICTIM_SUPPRESSION`
- Algorithm: `crest_victim_suppression`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.757384 |
| AC@3 | 0.917018 |
| AC@5 | 0.950070 |
| MRR | 0.841618 |
| avg_rank | 1.851617 |
| top1_miss | 345 |
| top5_miss | 71 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| time_bucket | ts9 | 23 | 0.478261 | 0.739130 | 0.913043 | 0.655518 | 2 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.525253 | 2 |
| time_bucket | ts6 | 28 | 0.535714 | 0.785714 | 0.857143 | 0.667543 | 4 |
| fault_type | pod-failure | 24 | 0.541667 | 0.875000 | 0.875000 | 0.692558 | 3 |
| case_service | ts-seat-service | 79 | 0.556962 | 0.886076 | 0.949367 | 0.725437 | 4 |
| case_service | ts-ui-dashboard | 165 | 0.557576 | 0.818182 | 0.866667 | 0.701666 | 22 |
| time_bucket | ts7 | 34 | 0.588235 | 0.852941 | 0.911765 | 0.725000 | 3 |
| fault_type | loss | 48 | 0.604167 | 0.833333 | 0.854167 | 0.731242 | 7 |
| fault_type | corrupt | 46 | 0.608696 | 0.782609 | 0.869565 | 0.730430 | 6 |
| case_service | ts-travel-service | 92 | 0.652174 | 0.934783 | 0.978261 | 0.790955 | 2 |
| time_bucket | ts4 | 274 | 0.656934 | 0.875912 | 0.919708 | 0.770889 | 22 |
| fault_type | response-delay | 89 | 0.662921 | 0.910112 | 0.955056 | 0.787293 | 4 |
| fault_type | response-replace-body | 51 | 0.666667 | 0.862745 | 0.941176 | 0.774556 | 3 |
| fault_type | bandwidth | 42 | 0.666667 | 0.833333 | 0.880952 | 0.752513 | 5 |
| case_service | ts-order-other-service | 27 | 0.666667 | 0.851852 | 1.000000 | 0.788272 | 0 |
| time_bucket | ts5 | 258 | 0.670543 | 0.833333 | 0.914729 | 0.769672 | 22 |
| case_service | ts-basic-service | 201 | 0.676617 | 0.870647 | 0.925373 | 0.778179 | 15 |
| time_bucket | ts8 | 25 | 0.680000 | 0.880000 | 0.880000 | 0.785714 | 3 |
| fault_type | partition | 97 | 0.680412 | 0.804124 | 0.835052 | 0.757307 | 16 |
| case_service | unknown | 26 | 0.692308 | 0.884615 | 0.923077 | 0.789103 | 2 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-verification-code-service|ts-execute-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-seat-service|ts-travel-service|ts-route-plan-service|ts-food-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-travel-service|ts-food-service|ts-config-service|ts-train-food-service|ts-order-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 26 | ts-food-service|ts-train-food-service|ts-seat-service|ts-preserve-service|ts-station-food-service | container-kill | ts-food-service |
| ts6-ts-preserve-service-partition-jvzrwx | ts-preserve-service;ts-ui-dashboard | 25 | ts-food-service|ts-basic-service|ts-assurance-service|ts-seat-service|ts-order-service | partition | ts-preserve-service |
| ts5-ts-preserve-service-partition-kfrmzn | ts-preserve-service;ts-ui-dashboard | 24 | ts-contacts-service|ts-order-service|ts-food-service|ts-seat-service|ts-consign-service | partition | ts-preserve-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 22 | ts-inside-payment-service|ts-order-service|ts-travel-service|ts-seat-service|ts-assurance-service | return | ts-cancel-service |
| ts4-ts-ui-dashboard-partition-lvfxl6 | ts-food-service;ts-ui-dashboard | 21 | ts-travel-plan-service|ts-seat-service|ts-auth-service|ts-route-plan-service|ts-train-service | partition | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 19 | ts-train-food-service|ts-order-service|ts-food-service|ts-travel-service|ts-station-service | request-abort | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 19 | ts-preserve-service|ts-payment-service|ts-ui-dashboard|ts-food-service|ts-user-service | response-replace-code | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 18 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-auth-service | bandwidth | ts-station-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 18 | ts-consign-service|ts-basic-service|loadgenerator|ts-food-service|ts-station-service | stress | ts-cancel-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 17 | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-food-service|ts-travel-plan-service | pod-failure | ts-consign-service |
| ts4-ts-assurance-service-partition-m4gbzn | ts-assurance-service;ts-ui-dashboard | 17 | ts-consign-service|ts-travel-plan-service|loadgenerator|ts-food-service|ts-basic-service | partition | ts-assurance-service |
| ts4-ts-basic-service-corrupt-trd2kh | ts-basic-service;ts-preserve-service | 16 | ts-food-service|ts-contacts-service|ts-seat-service|ts-ui-dashboard|ts-verification-code-service | corrupt | ts-basic-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 15 | ts-auth-service|ts-train-service|ts-ui-dashboard|ts-food-service|ts-travel-plan-service | container-kill | mysql |
| ts2-mysql-pod-kill-xvzmxb | mysql | 15 | ts-security-service|ts-order-service|ts-auth-service|ts-preserve-service|ts-travel-service | unknown | unknown |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 15 | ts-auth-service|loadgenerator|ts-food-service|ts-travel-plan-service|ts-travel2-service | bandwidth | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 15 | ts-auth-service|ts-preserve-service|ts-order-other-service|ts-order-service|ts-user-service | bandwidth | ts-route-plan-service |
| ts5-ts-contacts-service-loss-bdtvgn | ts-contacts-service;ts-ui-dashboard | 14 | ts-travel2-service|ts-travel-service|ts-seat-service|ts-basic-service|ts-route-service | loss | ts-contacts-service |
| ts5-ts-ui-dashboard-response-replace-code-fsnppw | ts-ui-dashboard;ts-verification-code-service | 14 | ts-security-service|ts-food-service|ts-auth-service|ts-travel-plan-service|ts-station-food-service | response-replace-code | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 13 | ts-inside-payment-service|ts-food-service|ts-assurance-service|ts-basic-service|ts-seat-service | request-abort | ts-ui-dashboard |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 12 | ts-order-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-inside-payment-service | partition | ts-seat-service |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | ts-travel-plan-service;ts-ui-dashboard | 12 | ts-inside-payment-service|ts-payment-service|ts-travel-service|ts-order-service|ts-food-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-order-service-partition-z2d6nw | ts-order-service;ts-ui-dashboard | 12 | ts-order-other-service|ts-security-service|ts-food-service|loadgenerator|ts-basic-service | partition | ts-order-service |
| ts4-ts-assurance-service-loss-5nnml6 | ts-assurance-service;ts-ui-dashboard | 11 | ts-seat-service|ts-food-service|ts-basic-service|ts-travel2-service|ts-travel-plan-service | loss | ts-assurance-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 11 | ts-payment-service|ts-inside-payment-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-travel2-service|ts-contacts-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-ui-dashboard-partition-czfh8c | ts-assurance-service;ts-ui-dashboard | 11 | ts-order-other-service|ts-order-service|ts-contacts-service|ts-consign-service|loadgenerator | partition | ts-ui-dashboard |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 10 | ts-ui-dashboard|ts-food-service|loadgenerator|ts-consign-service|ts-preserve-service | partition | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
