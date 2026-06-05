# EvidenceRank ARC13 Summary

- Created: 2026-06-05T12:54:34+08:00
- Source: `ARC13`
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.831224 |
| AC@3 | 0.947961 |
| AC@5 | 0.975387 |
| MRR | 0.893267 |
| avg_rank | 1.517581 |
| top1_miss | 240 |
| top5_miss | 35 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.166667 | 0.500000 | 0.791667 | 0.390317 | 5 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.523634 | 2 |
| time_bucket | ts8 | 25 | 0.560000 | 0.880000 | 0.960000 | 0.736410 | 1 |
| time_bucket | ts6 | 28 | 0.571429 | 0.857143 | 0.892857 | 0.715774 | 3 |
| fault_type | response-replace-body | 51 | 0.666667 | 0.882353 | 0.960784 | 0.793682 | 2 |
| fault_type | bandwidth | 42 | 0.666667 | 0.833333 | 0.880952 | 0.770981 | 5 |
| fault_type | request-abort | 60 | 0.683333 | 0.916667 | 0.933333 | 0.805548 | 4 |
| fault_type | corrupt | 46 | 0.695652 | 0.978261 | 1.000000 | 0.830435 | 0 |
| time_bucket | ts7 | 34 | 0.705882 | 0.823529 | 0.882353 | 0.781734 | 4 |
| case_service | ts-basic-service | 201 | 0.711443 | 0.935323 | 0.980100 | 0.825802 | 4 |
| case_service | unknown | 26 | 0.730769 | 0.807692 | 0.884615 | 0.795591 | 3 |
| fault_type | unknown | 26 | 0.730769 | 0.807692 | 0.884615 | 0.795591 | 3 |
| fault_type | request-replace-method | 190 | 0.736842 | 0.921053 | 0.968421 | 0.836069 | 6 |
| time_bucket | ts9 | 23 | 0.739130 | 0.956522 | 0.956522 | 0.843924 | 1 |
| case_service | ts-verification-code-service | 4 | 0.750000 | 1.000000 | 1.000000 | 0.875000 | 0 |
| case_service | ts-ui-dashboard | 165 | 0.757576 | 0.884848 | 0.939394 | 0.835184 | 10 |
| case_service | ts-security-service | 33 | 0.757576 | 1.000000 | 1.000000 | 0.873737 | 0 |
| case_service | ts-route-plan-service | 138 | 0.760870 | 0.949275 | 0.978261 | 0.855405 | 3 |
| case_service | ts-consign-price-service | 9 | 0.777778 | 0.888889 | 1.000000 | 0.837037 | 0 |
| time_bucket | ts4 | 274 | 0.791971 | 0.952555 | 0.970803 | 0.876969 | 8 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-order-service | unknown | unknown |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | ts-auth-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-basic-service | pod-failure | mysql |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 29 | ts-ui-dashboard|ts-verification-code-service|ts-user-service|ts-consign-service|ts-order-other-service | pod-failure | ts-travel-plan-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 28 | ts-inside-payment-service|ts-order-service|ts-travel-service|ts-seat-service|ts-basic-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 27 | ts-food-service|ts-ui-dashboard|ts-order-service|loadgenerator|ts-travel-service | container-kill | ts-food-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 17 | ts-consign-service|ts-basic-service|ts-food-service|ts-route-plan-service|ts-auth-service | stress | ts-cancel-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 16 | ts-inside-payment-service|ts-order-service|ts-order-other-service|ts-seat-service|ts-basic-service | pod-failure | ts-payment-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 16 | ts-ui-dashboard|ts-seat-service|ts-order-service|ts-order-other-service|ts-auth-service | bandwidth | ts-route-plan-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 14 | ts-order-service|ts-seat-service|ts-basic-service|ts-travel-service|ts-food-service | request-abort | ts-ui-dashboard |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 13 | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-inside-payment-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 13 | ts-payment-service|ts-inside-payment-service|ts-verification-code-service|loadgenerator|ts-basic-service | request-abort | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 12 | ts-payment-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-travel2-service | response-replace-body | ts-route-plan-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 11 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service | bandwidth | ts-station-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 11 | ts-consign-service|ts-order-service|ts-seat-service|ts-travel-service|ts-verification-code-service | unknown | unknown |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 11 | ts-ui-dashboard|ts-travel2-service|ts-basic-service|ts-consign-price-service|ts-route-service | response-replace-code | ts-travel-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 10 | ts-payment-service|ts-ui-dashboard|ts-preserve-service|ts-train-food-service|ts-order-service | response-replace-code | ts-basic-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 9 | ts-auth-service|ts-train-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-auth-service|ts-travel-service|ts-security-service|ts-order-service|ts-preserve-service | unknown | unknown |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 9 | ts-basic-service|ts-travel-service|ts-seat-service|ts-station-service|ts-route-service | pod-failure | ts-assurance-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 9 | ts-preserve-service|ts-route-plan-service|ts-order-service|ts-seat-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 9 | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-route-service | bandwidth | ts-station-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-seat-service|ts-station-food-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 8 | ts-basic-service|ts-consign-service|ts-seat-service|ts-order-service|ts-train-service | request-replace-method | ts-ui-dashboard |
| ts6-ts-basic-service-request-replace-method-4qzglm | ts-basic-service;ts-train-service | 8 | ts-cancel-service|ts-consign-service|ts-order-service|ts-travel-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 8 | ts-order-service|ts-basic-service|ts-consign-service|loadgenerator|ts-verification-code-service | request-abort | ts-ui-dashboard |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 7 | ts-basic-service|ts-travel2-service|ts-seat-service|ts-travel-service|ts-order-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 7 | loadgenerator|ts-seat-service|ts-travel2-service|ts-route-service|ts-station-food-service | request-abort | ts-ui-dashboard |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 7 | ts-travel-plan-service|ts-basic-service|ts-travel2-service|ts-route-plan-service|ts-travel-service | pod-failure | ts-price-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 6 | ts-order-service|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service|ts-travel-service | partition | ts-seat-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | ts-food-service;ts-ui-dashboard | 6 | ts-order-service|ts-seat-service|ts-basic-service|ts-travel-service|ts-route-service | request-replace-method | ts-ui-dashboard |

## Research Notes

- ARC13 confirms that ARC12's main failure was not merely the `reliability > 0` mask. Offline continuous reliability and rank-fusion variants performed worse, indicating that single-case reliability still overvalues propagation, volume, and victim symptoms.
- Accepted mechanism: keep raw root-specific multi-modal evidence as the primary ranking signal through an ordinal semantic priority ladder, and restrict ARC reliability to a local trace-neighbor contrast. This prevents family consensus from smoothing the root below propagated neighbors.
- Remaining weak area: sparse pod-failure and some entry-service protocol cases. The next reusable signal should detect sparse infrastructure/root-local failures without service names, labels, fault names, or processed conclusions.
