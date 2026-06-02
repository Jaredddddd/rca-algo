# EvidenceRank V7 Summary

- Created: 2026-06-02T03:01:44+08:00
- Source: `V7`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.781997 |
| AC@3 | 0.940928 |
| AC@5 | 0.978903 |
| MRR | 0.864359 |
| avg_rank | 1.586498 |
| top1_miss | 310 |
| top5_miss | 30 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.166667 | 0.541667 | 0.791667 | 0.386959 | 5 |
| time_bucket | ts8 | 25 | 0.360000 | 0.880000 | 0.960000 | 0.631333 | 1 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.525926 | 2 |
| time_bucket | ts6 | 28 | 0.535714 | 0.750000 | 0.964286 | 0.690221 | 1 |
| fault_type | response-replace-body | 51 | 0.549020 | 0.862745 | 0.960784 | 0.706031 | 2 |
| time_bucket | ts9 | 23 | 0.565217 | 0.913043 | 0.956522 | 0.732609 | 1 |
| time_bucket | ts7 | 34 | 0.588235 | 0.794118 | 0.911765 | 0.722527 | 3 |
| fault_type | request-abort | 60 | 0.600000 | 0.916667 | 0.950000 | 0.759754 | 3 |
| case_service | ts-basic-service | 201 | 0.616915 | 0.890547 | 0.980100 | 0.756823 | 4 |
| fault_type | bandwidth | 42 | 0.642857 | 0.857143 | 0.857143 | 0.758853 | 6 |
| case_service | ts-order-other-service | 27 | 0.666667 | 0.962963 | 1.000000 | 0.817901 | 0 |
| case_service | ts-consign-price-service | 9 | 0.666667 | 0.777778 | 0.888889 | 0.768519 | 1 |
| case_service | ts-ui-dashboard | 165 | 0.678788 | 0.903030 | 0.969697 | 0.800264 | 5 |
| case_service | unknown | 26 | 0.692308 | 0.807692 | 0.884615 | 0.771581 | 3 |
| fault_type | unknown | 26 | 0.692308 | 0.807692 | 0.884615 | 0.771581 | 3 |
| case_service | ts-station-service | 20 | 0.700000 | 0.900000 | 0.900000 | 0.804365 | 2 |
| case_service | ts-travel2-service | 68 | 0.705882 | 0.941176 | 1.000000 | 0.823775 | 0 |
| fault_type | request-replace-method | 190 | 0.715789 | 0.921053 | 0.989474 | 0.825088 | 2 |
| fault_type | corrupt | 46 | 0.717391 | 0.978261 | 1.000000 | 0.848551 | 0 |
| fault_type | response-replace-code | 231 | 0.718615 | 0.913420 | 0.982684 | 0.821454 | 4 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 35 | ts-auth-service|ts-train-food-service|ts-station-food-service|ts-security-service|ts-payment-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-food-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 27 | ts-inside-payment-service|ts-order-service|ts-travel-service|ts-ui-dashboard|ts-station-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 27 | ts-food-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-consign-service | container-kill | ts-food-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 15 | ts-inside-payment-service|ts-order-service|ts-order-other-service|ts-seat-service|ts-basic-service | pod-failure | ts-payment-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 15 | ts-consign-service|ts-food-service|ts-route-plan-service|ts-basic-service|ts-auth-service | stress | ts-cancel-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 14 | ts-payment-service|ts-ui-dashboard|ts-train-food-service|ts-preserve-service|loadgenerator | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 13 | ts-order-service|ts-seat-service|ts-food-service|ts-basic-service|ts-contacts-service | request-abort | ts-ui-dashboard |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 12 | ts-consign-service|ts-verification-code-service|ts-payment-service|ts-travel-service|ts-seat-service | unknown | unknown |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 12 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-order-service | response-replace-body | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 12 | ts-ui-dashboard|ts-order-service|ts-seat-service|ts-order-other-service|loadgenerator | bandwidth | ts-route-plan-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 11 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-travel-plan-service | response-replace-body | ts-route-plan-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 10 | ts-ui-dashboard|loadgenerator|ts-order-service|ts-contacts-service|ts-seat-service | bandwidth | ts-basic-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 10 | ts-ui-dashboard|ts-consign-price-service|ts-travel2-service|loadgenerator|ts-auth-service | response-replace-code | ts-travel-plan-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|loadgenerator|ts-verification-code-service|ts-auth-service | request-abort | ts-ui-dashboard |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 9 | ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-order-service | bandwidth | ts-station-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-auth-service|ts-travel-service|ts-security-service|ts-preserve-service|ts-order-service | unknown | unknown |
| ts0-mysql-container-kill-9t6n24 | mysql | 8 | ts-train-service|ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator | container-kill | mysql |
| ts4-ts-seat-service-bandwidth-k2bwt2 | ts-config-service;ts-seat-service | 8 | ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|loadgenerator|ts-route-plan-service | bandwidth | ts-seat-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 8 | loadgenerator|ts-station-food-service|ts-travel2-service|ts-seat-service|ts-travel-plan-service | request-abort | ts-ui-dashboard |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-station-food-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 7 | ts-basic-service|ts-station-service|ts-travel-service|ts-route-plan-service|ts-seat-service | pod-failure | ts-assurance-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 7 | ts-ui-dashboard|ts-basic-service|loadgenerator|ts-verification-code-service|ts-travel-plan-service | bandwidth | ts-route-plan-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 7 | ts-travel-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-route-service | bandwidth | ts-station-service |
| ts6-ts-route-plan-service-response-replace-code-9pfgvr | ts-route-plan-service;ts-route-service | 7 | ts-payment-service|ts-ui-dashboard|ts-consign-service|ts-security-service|ts-consign-price-service | response-replace-code | ts-route-plan-service |
| ts2-ts-consign-price-service-stress-7r95bt | ts-consign-price-service | 6 | ts-payment-service|ts-consign-service|ts-preserve-service|ts-security-service|ts-ui-dashboard | stress | ts-consign-price-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 6 | ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-payment-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 6 | ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service | pod-failure | ts-price-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 6 | ts-payment-service|ts-consign-service|ts-consign-price-service|ts-station-food-service|ts-basic-service | request-replace-method | ts-ui-dashboard |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
