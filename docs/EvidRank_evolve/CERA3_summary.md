# EvidenceRank CERA3 Summary

- Created: 2026-06-05T14:38:00+08:00
- Source: `CERA3`
- Algorithm: `cera`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.850211 |
| AC@3 | 0.950774 |
| AC@5 | 0.976090 |
| MRR | 0.904032 |
| avg_rank | 1.487342 |
| top1_miss | 213 |
| top5_miss | 34 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.208333 | 0.583333 | 0.750000 | 0.446068 | 6 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.523634 | 2 |
| time_bucket | ts6 | 28 | 0.607143 | 0.750000 | 0.964286 | 0.729507 | 1 |
| time_bucket | ts8 | 25 | 0.640000 | 0.920000 | 0.960000 | 0.790000 | 1 |
| fault_type | response-replace-body | 51 | 0.647059 | 0.882353 | 0.960784 | 0.767796 | 2 |
| time_bucket | ts7 | 34 | 0.647059 | 0.794118 | 0.852941 | 0.739823 | 5 |
| fault_type | bandwidth | 42 | 0.690476 | 0.833333 | 0.857143 | 0.769007 | 6 |
| fault_type | request-abort | 60 | 0.750000 | 0.933333 | 0.966667 | 0.844722 | 2 |
| case_service | ts-ui-dashboard | 165 | 0.751515 | 0.915152 | 0.957576 | 0.843256 | 7 |
| case_service | unknown | 26 | 0.769231 | 0.884615 | 0.884615 | 0.823504 | 3 |
| fault_type | unknown | 26 | 0.769231 | 0.884615 | 0.884615 | 0.823504 | 3 |
| fault_type | request-replace-method | 190 | 0.773684 | 0.926316 | 0.978947 | 0.858383 | 4 |
| case_service | ts-basic-service | 201 | 0.776119 | 0.915423 | 0.980100 | 0.857246 | 4 |
| case_service | ts-consign-price-service | 9 | 0.777778 | 0.888889 | 0.888889 | 0.847222 | 1 |
| case_service | ts-travel2-service | 68 | 0.779412 | 0.955882 | 1.000000 | 0.868873 | 0 |
| time_bucket | ts9 | 23 | 0.782609 | 0.913043 | 1.000000 | 0.860145 | 0 |
| case_service | ts-station-service | 20 | 0.800000 | 0.900000 | 0.900000 | 0.858013 | 2 |
| fault_type | response-replace-code | 231 | 0.813853 | 0.935065 | 0.987013 | 0.880952 | 3 |
| time_bucket | ts5 | 258 | 0.817829 | 0.949612 | 0.984496 | 0.885257 | 4 |
| case_service | ts-seat-service | 79 | 0.822785 | 0.936709 | 0.974684 | 0.884016 | 2 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-basic-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-seat-service|ts-travel-service|ts-order-other-service|ts-basic-service | unknown | unknown |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 29 | ts-ui-dashboard|ts-verification-code-service|ts-consign-service|ts-user-service|ts-auth-service | pod-failure | ts-travel-plan-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 28 | ts-inside-payment-service|ts-order-service|ts-travel-service|ts-seat-service|ts-basic-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 28 | ts-food-service|ts-ui-dashboard|ts-train-food-service|ts-station-food-service|ts-travel-service | container-kill | ts-food-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 18 | ts-inside-payment-service|ts-order-service|ts-order-other-service|ts-seat-service|ts-basic-service | pod-failure | ts-payment-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 17 | ts-consign-service|ts-station-service|ts-basic-service|ts-route-plan-service|ts-food-service | stress | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 16 | ts-ui-dashboard|ts-payment-service|ts-preserve-service|ts-auth-service|ts-verification-code-service | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 15 | ts-order-service|ts-basic-service|ts-seat-service|ts-station-service|ts-food-service | request-abort | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 15 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 13 | ts-consign-service|ts-preserve-service|ts-seat-service|ts-ui-dashboard|ts-basic-service | bandwidth | ts-station-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 13 | ts-ui-dashboard|ts-auth-service|ts-travel-plan-service|ts-order-service|ts-food-service | bandwidth | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 12 | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-route-service | bandwidth | ts-station-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-route-plan-service|ts-seat-service|ts-travel-plan-service|ts-food-service | response-replace-body | ts-basic-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 10 | ts-auth-service|ts-travel-service|ts-security-service|ts-order-service|ts-preserve-service | unknown | unknown |
| ts0-mysql-container-kill-9t6n24 | mysql | 9 | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 9 | ts-consign-service|ts-seat-service|ts-travel-service|ts-basic-service|ts-order-service | unknown | unknown |
| ts4-ts-seat-service-bandwidth-k2bwt2 | ts-config-service;ts-seat-service | 9 | ts-ui-dashboard|ts-travel-plan-service|ts-travel2-service|loadgenerator|ts-route-plan-service | bandwidth | ts-seat-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-seat-service|ts-station-food-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 8 | ts-basic-service|ts-station-service|ts-seat-service|ts-travel-service|ts-route-service | pod-failure | ts-assurance-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | ts-consign-price-service | 8 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-auth-service|ts-travel-plan-service | pod-failure | ts-consign-price-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|ts-food-service|ts-travel-plan-service|ts-auth-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 8 | ts-ui-dashboard|ts-auth-service|ts-verification-code-service|ts-seat-service|ts-order-service | bandwidth | ts-route-plan-service |
| ts5-ts-route-plan-service-response-delay-5mjstz | ts-route-plan-service;ts-travel-service | 8 | ts-payment-service|ts-basic-service|ts-seat-service|ts-station-service|ts-consign-price-service | response-delay | ts-route-plan-service |
| ts0-ts-ui-dashboard-response-replace-code-rm7j85 | ts-travel-plan-service;ts-ui-dashboard | 7 | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 7 | ts-ui-dashboard|ts-order-service|ts-travel-plan-service|ts-travel-service|ts-consign-price-service | partition | ts-seat-service |
| ts6-ts-basic-service-request-replace-method-4qzglm | ts-basic-service;ts-train-service | 7 | ts-cancel-service|ts-seat-service|ts-travel-service|ts-verification-code-service|ts-order-service | request-replace-method | ts-basic-service |
| ts7-ts-route-plan-service-response-delay-t55rlr | ts-route-plan-service;ts-travel-service | 7 | ts-station-food-service|ts-inside-payment-service|ts-order-service|ts-ui-dashboard|ts-seat-service | response-delay | ts-route-plan-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 6 | ts-basic-service|ts-consign-service|ts-order-service|ts-seat-service|ts-station-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 6 | ts-basic-service|ts-seat-service|ts-travel2-service|ts-travel-service|ts-order-service | request-replace-method | ts-ui-dashboard |

## Research Notes

- CERA3 reaches the target with `AC@1=0.850211` by replacing CERA2's egalitarian robust family burden with ordinal causal evidence energy and incident-derived sink-share parent context.
- The main remaining weakness is generic infrastructure or severe disruption behavior: `pod-failure`, `bandwidth`, and a few unknown/return cases often lack strong endpoint/status mutation at the failing component while downstream traffic and latency dominate.
- Future work should investigate generic infrastructure-local evidence and uncertainty-aware multi-root preservation. Do not introduce service/fault/case-specific rules or manually tuned numeric constants.
