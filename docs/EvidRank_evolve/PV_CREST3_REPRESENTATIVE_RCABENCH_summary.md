# EvidenceRank PV_CREST3_REPRESENTATIVE_RCABENCH Summary

- Created: 2026-06-10T20:45:33+08:00
- Source: `PV_CREST3_REPRESENTATIVE_RCABENCH`
- Algorithm: `crest`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.800281 |
| AC@3 | 0.944444 |
| AC@5 | 0.971871 |
| MRR | 0.875326 |
| avg_rank | 1.591421 |
| top1_miss | 284 |
| top5_miss | 40 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.523864 | 2 |
| fault_type | pod-failure | 24 | 0.541667 | 0.875000 | 0.875000 | 0.692558 | 3 |
| time_bucket | ts6 | 28 | 0.607143 | 0.821429 | 0.964286 | 0.736310 | 1 |
| time_bucket | ts9 | 23 | 0.608696 | 0.913043 | 0.913043 | 0.763787 | 2 |
| time_bucket | ts7 | 34 | 0.647059 | 0.794118 | 0.941176 | 0.758556 | 2 |
| fault_type | response-replace-body | 51 | 0.666667 | 0.843137 | 0.941176 | 0.776697 | 3 |
| case_service | ts-basic-service | 201 | 0.681592 | 0.870647 | 0.930348 | 0.785951 | 14 |
| fault_type | request-replace-path | 39 | 0.692308 | 0.897436 | 0.974359 | 0.816484 | 1 |
| case_service | unknown | 26 | 0.692308 | 0.884615 | 0.923077 | 0.789103 | 2 |
| fault_type | unknown | 26 | 0.692308 | 0.884615 | 0.923077 | 0.789103 | 2 |
| case_service | ts-ui-dashboard | 165 | 0.703030 | 0.921212 | 0.963636 | 0.817494 | 6 |
| case_service | ts-travel-service | 92 | 0.706522 | 0.956522 | 0.989130 | 0.832169 | 1 |
| case_service | ts-seat-service | 79 | 0.708861 | 0.974684 | 0.987342 | 0.830687 | 1 |
| time_bucket | ts8 | 25 | 0.720000 | 0.960000 | 0.960000 | 0.831667 | 1 |
| fault_type | request-replace-method | 190 | 0.731579 | 0.931579 | 0.973684 | 0.834919 | 5 |
| fault_type | request-abort | 60 | 0.733333 | 0.916667 | 0.950000 | 0.831145 | 3 |
| fault_type | bandwidth | 42 | 0.738095 | 0.857143 | 0.880952 | 0.801977 | 5 |
| case_service | ts-route-service | 23 | 0.739130 | 0.826087 | 0.913043 | 0.815631 | 2 |
| time_bucket | ts5 | 258 | 0.740310 | 0.887597 | 0.953488 | 0.828654 | 12 |
| fault_type | response-replace-code | 231 | 0.744589 | 0.926407 | 0.965368 | 0.838919 | 8 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-auth-service|ts-verification-code-service|ts-execute-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-basic-service|ts-food-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-travel-service|ts-food-service|ts-config-service|ts-train-food-service|ts-order-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 26 | ts-food-service|ts-train-food-service|ts-seat-service|ts-ui-dashboard|ts-preserve-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 22 | ts-inside-payment-service|ts-order-service|ts-seat-service|ts-travel-service|ts-assurance-service | return | ts-cancel-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 20 | ts-consign-service|ts-food-service|ts-basic-service|loadgenerator|ts-station-service | stress | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 19 | ts-preserve-service|ts-payment-service|ts-ui-dashboard|ts-food-service|ts-user-service | response-replace-code | ts-basic-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 17 | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-food-service|ts-seat-service | pod-failure | ts-consign-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 17 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-ui-dashboard | bandwidth | ts-station-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 15 | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|ts-food-service | container-kill | mysql |
| ts2-mysql-pod-kill-xvzmxb | mysql | 15 | ts-security-service|ts-order-service|ts-auth-service|ts-preserve-service|ts-travel-service | unknown | unknown |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 15 | ts-ui-dashboard|ts-auth-service|loadgenerator|ts-food-service|ts-travel-plan-service | bandwidth | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 14 | ts-ui-dashboard|ts-auth-service|ts-preserve-service|ts-seat-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 12 | ts-payment-service|ts-inside-payment-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 11 | ts-order-service|ts-ui-dashboard|ts-travel-plan-service|loadgenerator|ts-inside-payment-service | partition | ts-seat-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-seat-service|ts-travel2-service|ts-contacts-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 11 | ts-ui-dashboard|ts-food-service|ts-preserve-service|loadgenerator|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 11 | ts-payment-service|ts-inside-payment-service|ts-food-service|ts-assurance-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 10 | ts-ui-dashboard|ts-food-service|loadgenerator|ts-consign-service|ts-preserve-service | partition | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 10 | ts-route-plan-service|ts-security-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 9 | ts-train-food-service|ts-food-service|ts-order-service|ts-seat-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 9 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 9 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-travel-plan-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 9 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-preserve-service|ts-ui-dashboard | response-replace-code | ts-travel2-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 8 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-food-service|ts-seat-service | bandwidth | ts-station-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-consign-service|ts-cancel-service|ts-food-service|ts-consign-price-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-route-service-corrupt-qlt7gn | mysql;ts-route-service | 7 | ts-auth-service|ts-ui-dashboard|ts-train-service|ts-consign-service|ts-inside-payment-service | corrupt | ts-route-service |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 7 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 7 | ts-preserve-service|ts-cancel-service|ts-order-service|ts-food-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 7 | ts-seat-service|ts-preserve-service|ts-cancel-service|ts-travel-service|ts-route-plan-service | request-replace-path | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
