# EvidenceRank CREST8_REJECTED Summary

- Created: 2026-06-07T19:15:19+08:00
- Source: `CREST8_REJECTED`
- Algorithm: `crest`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.340366 |
| AC@3 | 0.447257 |
| AC@5 | 0.530942 |
| MRR | 0.439628 |
| avg_rank | 9.619550 |
| top1_miss | 938 |
| top5_miss | 667 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | response-delay | 89 | 0.000000 | 0.011236 | 0.044944 | 0.069193 | 85 |
| fault_type | delay | 21 | 0.000000 | 0.142857 | 0.142857 | 0.106349 | 18 |
| case_service | ts-ui-dashboard | 165 | 0.018182 | 0.096970 | 0.181818 | 0.120783 | 135 |
| fault_type | request-delay | 88 | 0.022727 | 0.102273 | 0.159091 | 0.114075 | 74 |
| fault_type | loss | 48 | 0.062500 | 0.166667 | 0.270833 | 0.179287 | 35 |
| fault_type | partition | 97 | 0.072165 | 0.123711 | 0.195876 | 0.168239 | 78 |
| fault_type | corrupt | 46 | 0.130435 | 0.173913 | 0.260870 | 0.216550 | 34 |
| time_bucket | ts9 | 23 | 0.173913 | 0.304348 | 0.434783 | 0.302925 | 13 |
| time_bucket | ts6 | 28 | 0.178571 | 0.250000 | 0.428571 | 0.290060 | 16 |
| fault_type | response-abort | 44 | 0.181818 | 0.386364 | 0.545455 | 0.342036 | 20 |
| fault_type | request-replace-method | 190 | 0.184211 | 0.326316 | 0.505263 | 0.324852 | 94 |
| case_service | ts-seat-service | 79 | 0.189873 | 0.265823 | 0.379747 | 0.293176 | 49 |
| fault_type | response-replace-code | 231 | 0.207792 | 0.337662 | 0.463203 | 0.336910 | 124 |
| case_service | ts-route-plan-service | 138 | 0.224638 | 0.347826 | 0.478261 | 0.351557 | 72 |
| fault_type | request-abort | 60 | 0.233333 | 0.316667 | 0.450000 | 0.342173 | 33 |
| case_service | ts-travel2-service | 68 | 0.235294 | 0.264706 | 0.294118 | 0.308544 | 48 |
| time_bucket | ts7 | 34 | 0.235294 | 0.411765 | 0.500000 | 0.372506 | 17 |
| case_service | mysql | 72 | 0.236111 | 0.333333 | 0.458333 | 0.355384 | 39 |
| case_service | ts-basic-service | 201 | 0.248756 | 0.378109 | 0.482587 | 0.371363 | 104 |
| fault_type | request-replace-path | 39 | 0.256410 | 0.564103 | 0.615385 | 0.441473 | 15 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts5-ts-ui-dashboard-corrupt-x6ghbz | ts-travel-service;ts-ui-dashboard | 46 | loadgenerator|ts-assurance-service|ts-consign-service|ts-auth-service|ts-station-service | corrupt | ts-ui-dashboard |
| ts4-ts-travel-service-response-delay-lnpdxn | ts-basic-service;ts-travel-service | 44 | ts-assurance-service|ts-consign-service|ts-config-service|ts-security-service|ts-auth-service | response-delay | ts-travel-service |
| ts8-ts-ui-dashboard-corrupt-5wlgpm | ts-food-service;ts-ui-dashboard | 44 | loadgenerator|ts-voucher-service|ts-user-service|ts-consign-service|rabbitmq | corrupt | ts-ui-dashboard |
| ts4-ts-basic-service-corrupt-trd2kh | ts-basic-service;ts-preserve-service | 43 | loadgenerator|ts-user-service|ts-contacts-service|ts-verification-code-service|ts-food-service | corrupt | ts-basic-service |
| ts4-ts-seat-service-corrupt-d8skmr | ts-preserve-service;ts-seat-service | 43 | loadgenerator|ts-assurance-service|ts-consign-service|ts-auth-service|ts-travel-plan-service | corrupt | ts-seat-service |
| ts5-ts-route-service-partition-rn9lhb | ts-route-service;ts-ui-dashboard | 43 | loadgenerator|ts-delivery-service|ts-assurance-service|ts-station-food-service|ts-contacts-service | partition | ts-route-service |
| ts5-ts-travel-service-partition-vr6f55 | ts-travel-service;ts-ui-dashboard | 43 | loadgenerator|ts-config-service|ts-route-service|ts-consign-price-service|ts-contacts-service | partition | ts-travel-service |
| ts5-ts-travel2-service-response-delay-b7zvcf | ts-route-service;ts-travel2-service | 43 | ts-voucher-service|ts-assurance-service|ts-contacts-service|loadgenerator|ts-food-service | response-delay | ts-travel2-service |
| ts8-ts-travel-service-corrupt-fsmp6c | ts-seat-service;ts-travel-service | 43 | loadgenerator|ts-user-service|ts-consign-service|mysql|ts-train-food-service | corrupt | ts-travel-service |
| ts4-ts-basic-service-request-delay-xhctbw | ts-basic-service;ts-train-service | 42 | ts-notification-service|ts-delivery-service|ts-train-food-service|ts-contacts-service|ts-user-service | request-delay | ts-basic-service |
| ts5-ts-travel-service-request-delay-f7bp9x | ts-seat-service;ts-travel-service | 42 | ts-consign-service|ts-train-food-service|ts-assurance-service|ts-route-plan-service|loadgenerator | request-delay | ts-travel-service |
| ts5-ts-ui-dashboard-response-replace-code-fsnppw | ts-ui-dashboard;ts-verification-code-service | 42 | ts-security-service|loadgenerator|ts-assurance-service|ts-auth-service|ts-train-service | response-replace-code | ts-ui-dashboard |
| ts6-ts-travel2-service-request-delay-bnhhtc | ts-seat-service;ts-travel2-service | 42 | loadgenerator|ts-inside-payment-service|ts-travel-plan-service|ts-price-service|ts-consign-service | request-delay | ts-travel2-service |
| ts4-ts-seat-service-request-delay-xfh49m | ts-order-other-service;ts-seat-service | 41 | ts-consign-service|ts-config-service|ts-route-plan-service|ts-ticket-office-service|ts-user-service | request-delay | ts-seat-service |
| ts4-ts-travel-service-response-delay-bwdbxp | ts-seat-service;ts-travel-service | 41 | loadgenerator|ts-consign-service|ts-assurance-service|ts-price-service|ts-avatar-service | response-delay | ts-travel-service |
| ts5-ts-preserve-service-partition-dkhqzh | ts-preserve-service;ts-seat-service | 41 | loadgenerator|ts-assurance-service|ts-inside-payment-service|ts-train-food-service|ts-contacts-service | partition | ts-preserve-service |
| ts9-ts-travel-service-partition-9b45sj | ts-seat-service;ts-travel-service | 41 | ts-consign-service|ts-user-service|loadgenerator|ts-station-food-service|ts-avatar-service | partition | ts-travel-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 40 | loadgenerator|ts-consign-price-service|ts-inside-payment-service|ts-price-service|ts-assurance-service | partition | ts-seat-service |
| ts4-ts-order-service-bandwidth-kqnvn7 | ts-order-service;ts-ui-dashboard | 40 | ts-assurance-service|loadgenerator|ts-user-service|ts-cancel-service|ts-config-service | bandwidth | ts-order-service |
| ts4-ts-travel-service-response-delay-k2kgdb | ts-seat-service;ts-travel-service | 40 | ts-consign-price-service|loadgenerator|ts-inside-payment-service|ts-travel2-service|ts-station-service | response-delay | ts-travel-service |
| ts5-ts-travel-plan-service-delay-v5ptlf | ts-seat-service;ts-travel-plan-service | 40 | loadgenerator|ts-admin-travel-service|ts-inside-payment-service|ts-assurance-service|ts-user-service | delay | ts-travel-plan-service |
| ts5-ts-ui-dashboard-request-delay-55ksmg | ts-food-service;ts-ui-dashboard | 40 | ts-consign-service|loadgenerator|ts-cancel-service|ts-contacts-service|ts-avatar-service | request-delay | ts-ui-dashboard |
| ts5-ts-ui-dashboard-response-delay-5lz6hf | ts-travel-service;ts-ui-dashboard | 40 | loadgenerator|ts-assurance-service|ts-ticket-office-service|ts-cancel-service|ts-inside-payment-service | response-delay | ts-ui-dashboard |
| ts4-ts-route-plan-service-request-delay-rqmwn4 | ts-route-plan-service;ts-travel-service | 39 | ts-consign-price-service|loadgenerator|ts-cancel-service|ts-consign-service|ts-config-service | request-delay | ts-route-plan-service |
| ts4-ts-route-service-partition-xw4bwj | ts-basic-service;ts-route-service | 39 | ts-station-service|ts-order-service|loadgenerator|ts-admin-basic-info-service|ts-notification-service | partition | ts-route-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 39 | ts-payment-service|loadgenerator|ts-travel-plan-service|ts-assurance-service|ts-train-food-service | response-replace-code | ts-basic-service |
| ts5-ts-ui-dashboard-response-delay-9rx4cf | ts-order-other-service;ts-ui-dashboard | 39 | ts-ticket-office-service|ts-consign-service|loadgenerator|ts-contacts-service|ts-travel-plan-service | response-delay | ts-ui-dashboard |
| ts5-ts-basic-service-response-delay-m48s7x | ts-basic-service;ts-train-service | 38 | loadgenerator|ts-cancel-service|ts-station-service|ts-assurance-service|ts-consign-service | response-delay | ts-basic-service |
| ts5-ts-travel-service-bandwidth-z684lr | ts-basic-service;ts-travel-service | 38 | loadgenerator|ts-assurance-service|ts-auth-service|ts-news-service|ts-admin-user-service | bandwidth | ts-travel-service |
| ts5-ts-ui-dashboard-response-replace-code-9xg52l | ts-route-service;ts-ui-dashboard | 38 | loadgenerator|ts-assurance-service|ts-notification-service|ts-auth-service|ts-station-food-service | response-replace-code | ts-ui-dashboard |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
