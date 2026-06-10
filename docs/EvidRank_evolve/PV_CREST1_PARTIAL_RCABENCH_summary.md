# EvidenceRank PV_CREST1_PARTIAL_RCABENCH Summary

- Created: 2026-06-10T17:15:01+08:00
- Source: `PV_CREST1_PARTIAL_RCABENCH`
- Algorithm: `crest_partial_view`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.492264 |
| AC@3 | 0.938115 |
| AC@5 | 0.972574 |
| MRR | 0.714684 |
| avg_rank | 1.918425 |
| top1_miss | 722 |
| top5_miss | 39 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | partition | 97 | 0.154639 | 0.938144 | 0.958763 | 0.540726 | 4 |
| fault_type | request-delay | 88 | 0.159091 | 0.988636 | 1.000000 | 0.566667 | 0 |
| fault_type | loss | 48 | 0.187500 | 0.958333 | 1.000000 | 0.576389 | 0 |
| fault_type | response-delay | 89 | 0.191011 | 0.966292 | 1.000000 | 0.565918 | 0 |
| case_service | ts-ui-dashboard | 165 | 0.206061 | 0.903030 | 0.963636 | 0.555587 | 6 |
| time_bucket | ts6 | 28 | 0.214286 | 0.750000 | 0.964286 | 0.525340 | 1 |
| fault_type | corrupt | 46 | 0.239130 | 0.891304 | 0.956522 | 0.576294 | 2 |
| fault_type | response-abort | 44 | 0.250000 | 0.954545 | 0.977273 | 0.580898 | 1 |
| fault_type | delay | 21 | 0.285714 | 1.000000 | 1.000000 | 0.626984 | 0 |
| time_bucket | ts7 | 34 | 0.294118 | 0.764706 | 0.941176 | 0.572562 | 2 |
| case_service | ts-travel2-service | 68 | 0.352941 | 0.897059 | 0.970588 | 0.634477 | 2 |
| case_service | ts-route-plan-service | 138 | 0.369565 | 0.949275 | 0.978261 | 0.657336 | 3 |
| fault_type | response-replace-code | 231 | 0.372294 | 0.913420 | 0.965368 | 0.642776 | 8 |
| time_bucket | ts5 | 258 | 0.379845 | 0.895349 | 0.949612 | 0.640799 | 13 |
| time_bucket | ts4 | 274 | 0.383212 | 0.930657 | 0.959854 | 0.650484 | 11 |
| case_service | ts-basic-service | 201 | 0.398010 | 0.860697 | 0.930348 | 0.632782 | 14 |
| case_service | ts-travel-plan-service | 72 | 0.416667 | 0.972222 | 0.986111 | 0.691393 | 1 |
| fault_type | request-replace-method | 190 | 0.421053 | 0.915789 | 0.978947 | 0.667989 | 4 |
| case_service | mysql | 72 | 0.430556 | 0.930556 | 0.986111 | 0.690263 | 1 |
| time_bucket | ts8 | 25 | 0.440000 | 0.960000 | 0.960000 | 0.678333 | 1 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-verification-code-service|ts-execute-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-voucher-service|ts-auth-service|ts-travel-service|ts-seat-service|ts-basic-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-voucher-service|ts-travel-service|ts-food-service|ts-config-service|ts-train-food-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 26 | ts-food-service|ts-train-food-service|ts-seat-service|ts-ui-dashboard|ts-preserve-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 22 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-travel-service|ts-assurance-service | return | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 19 | ts-payment-service|ts-preserve-service|ts-ui-dashboard|ts-food-service|ts-user-service | response-replace-code | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 18 | ts-admin-order-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service | bandwidth | ts-station-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 15 | ts-ui-dashboard|ts-auth-service|loadgenerator|ts-food-service|ts-travel-plan-service | bandwidth | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 14 | ts-ui-dashboard|ts-auth-service|ts-preserve-service|ts-seat-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-inside-payment-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 12 | ts-voucher-service|ts-payment-service|ts-inside-payment-service|ts-food-service|ts-assurance-service | request-abort | ts-ui-dashboard |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 11 | ts-consign-price-service|ts-order-service|ts-ui-dashboard|ts-travel-plan-service|loadgenerator | partition | ts-seat-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 11 | ts-notification-service|ts-route-plan-service|ts-security-service|ts-travel-plan-service|ts-travel2-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-seat-service|ts-travel2-service|ts-contacts-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 11 | ts-verification-code-service|ts-ui-dashboard|ts-food-service|ts-preserve-service|loadgenerator | response-replace-body | ts-route-plan-service |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 10 | ts-ui-dashboard|ts-food-service|loadgenerator|ts-consign-service|ts-preserve-service | partition | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 10 | ts-notification-service|ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service | response-replace-body | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 10 | ts-ticket-office-service|ts-ui-dashboard|loadgenerator|ts-food-service|ts-travel-plan-service | bandwidth | ts-route-plan-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 9 | ts-train-food-service|ts-food-service|ts-order-service|ts-seat-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 9 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-preserve-service|ts-ui-dashboard | response-replace-code | ts-travel2-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 8 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-food-service|ts-seat-service | bandwidth | ts-station-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-consign-service|ts-cancel-service|ts-food-service|ts-consign-price-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-route-service-corrupt-qlt7gn | mysql;ts-route-service | 7 | ts-auth-service|ts-ui-dashboard|ts-train-service|ts-consign-service|ts-inside-payment-service | corrupt | ts-route-service |
| ts4-ts-basic-service-response-replace-code-hvsqnm | ts-basic-service;ts-route-service | 7 | ts-notification-service|ts-preserve-service|ts-travel2-service|ts-security-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 7 | ts-cancel-service|ts-preserve-service|ts-order-service|ts-food-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 7 | ts-cancel-service|ts-seat-service|ts-preserve-service|ts-travel-service|ts-route-plan-service | request-replace-path | ts-basic-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 7 | ts-consign-service|ts-route-plan-service|ts-consign-price-service|ts-travel-plan-service|ts-travel2-service | response-abort | ts-basic-service |
| ts5-ts-travel-service-response-replace-body-kbclt4 | ts-basic-service;ts-travel-service | 7 | ts-preserve-service|ts-seat-service|ts-travel2-service|ts-ui-dashboard|ts-order-service | response-replace-body | ts-travel-service |
| ts6-ts-preserve-service-partition-jvzrwx | ts-preserve-service;ts-ui-dashboard | 7 | ts-payment-service|ts-food-service|ts-basic-service|ts-assurance-service|ts-seat-service | partition | ts-preserve-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 7 | ts-ticket-office-service|ts-order-service|ts-consign-service|ts-contacts-service|loadgenerator | request-abort | ts-ui-dashboard |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
