# EvidenceRank V6 Summary

- Created: 2026-06-02T01:53:21+08:00
- Source: `V6`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.766526 |
| AC@3 | 0.922644 |
| AC@5 | 0.961322 |
| MRR | 0.849078 |
| avg_rank | 1.736990 |
| top1_miss | 332 |
| top5_miss | 55 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.375000 | 0.708333 | 0.875000 | 0.552267 | 3 |
| time_bucket | ts8 | 25 | 0.440000 | 0.880000 | 0.920000 | 0.657111 | 2 |
| time_bucket | ts6 | 28 | 0.464286 | 0.750000 | 0.857143 | 0.641511 | 4 |
| time_bucket | ts7 | 34 | 0.500000 | 0.764706 | 0.911765 | 0.661252 | 3 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.527116 | 2 |
| fault_type | response-replace-body | 51 | 0.529412 | 0.823529 | 0.941176 | 0.690998 | 3 |
| case_service | ts-ui-dashboard | 165 | 0.539394 | 0.769697 | 0.848485 | 0.674963 | 25 |
| case_service | ts-consign-price-service | 9 | 0.555556 | 0.777778 | 0.888889 | 0.688272 | 1 |
| time_bucket | ts9 | 23 | 0.565217 | 0.826087 | 0.913043 | 0.717633 | 2 |
| fault_type | request-abort | 60 | 0.583333 | 0.866667 | 0.933333 | 0.723412 | 4 |
| case_service | ts-basic-service | 201 | 0.592040 | 0.860697 | 0.965174 | 0.734206 | 7 |
| fault_type | response-replace-code | 231 | 0.623377 | 0.870130 | 0.948052 | 0.757404 | 12 |
| fault_type | bandwidth | 42 | 0.642857 | 0.833333 | 0.833333 | 0.747667 | 7 |
| case_service | ts-order-other-service | 27 | 0.666667 | 0.962963 | 1.000000 | 0.817901 | 0 |
| fault_type | request-replace-method | 190 | 0.673684 | 0.852632 | 0.905263 | 0.770069 | 18 |
| case_service | ts-travel2-service | 68 | 0.691176 | 0.911765 | 1.000000 | 0.809804 | 0 |
| fault_type | request-replace-path | 39 | 0.692308 | 0.923077 | 1.000000 | 0.811538 | 0 |
| case_service | ts-station-service | 20 | 0.700000 | 0.900000 | 0.900000 | 0.805000 | 2 |
| fault_type | response-abort | 44 | 0.750000 | 0.931818 | 1.000000 | 0.853030 | 0 |
| time_bucket | ts5 | 258 | 0.751938 | 0.918605 | 0.961240 | 0.840980 | 10 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 35 | ts-auth-service|ts-train-food-service|ts-station-food-service|ts-security-service|ts-payment-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-seat-service|ts-travel-service|ts-order-other-service|ts-order-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 27 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-ui-dashboard|ts-station-service | return | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 25 | ts-food-service|ts-ui-dashboard|ts-seat-service|ts-verification-code-service|ts-travel-service | container-kill | ts-food-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 18 | ts-seat-service|ts-order-service|ts-train-food-service|ts-food-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 18 | ts-payment-service|ts-inside-payment-service|ts-verification-code-service|ts-auth-service|ts-travel-plan-service | request-abort | ts-ui-dashboard |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 16 | ts-consign-service|ts-verification-code-service|ts-payment-service|ts-seat-service|ts-travel-service | unknown | unknown |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 15 | ts-payment-service|ts-consign-price-service|ts-consign-service|ts-station-food-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 14 | ts-consign-service|ts-food-service|ts-route-plan-service|ts-auth-service|ts-basic-service | stress | ts-cancel-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 13 | ts-inside-payment-service|ts-order-other-service|ts-seat-service|ts-order-service|ts-basic-service | pod-failure | ts-payment-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 13 | ts-seat-service|ts-basic-service|ts-auth-service|ts-verification-code-service|ts-consign-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 13 | ts-payment-service|ts-train-food-service|ts-ui-dashboard|ts-seat-service|ts-preserve-service | response-replace-code | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 13 | ts-station-food-service|loadgenerator|ts-travel2-service|ts-seat-service|ts-route-service | request-abort | ts-ui-dashboard |
| ts0-ts-ui-dashboard-request-replace-method-fl9jln | ts-ui-dashboard;ts-user-service | 12 | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | ts-food-service;ts-ui-dashboard | 11 | ts-seat-service|ts-order-service|ts-config-service|ts-travel-service|ts-route-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 11 | ts-ui-dashboard|ts-seat-service|ts-order-service|ts-auth-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 11 | ts-consign-price-service|ts-ui-dashboard|ts-travel2-service|ts-auth-service|ts-seat-service | response-replace-code | ts-travel-plan-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 11 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-consign-price-service | response-replace-body | ts-route-plan-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 10 | ts-consign-service|ts-preserve-service|ts-seat-service|ts-ui-dashboard|ts-order-service | bandwidth | ts-station-service |
| ts0-ts-ui-dashboard-request-replace-method-z9kbl2 | ts-train-service;ts-ui-dashboard | 10 | ts-payment-service|ts-train-food-service|ts-consign-price-service|ts-auth-service|ts-inside-payment-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 10 | ts-ui-dashboard|ts-verification-code-service|ts-seat-service|ts-travel-plan-service|ts-auth-service | bandwidth | ts-route-plan-service |
| ts6-ts-basic-service-request-replace-method-4qzglm | ts-basic-service;ts-train-service | 10 | ts-cancel-service|ts-verification-code-service|ts-consign-service|ts-auth-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 10 | ts-order-service|ts-verification-code-service|ts-basic-service|ts-auth-service|ts-seat-service | request-abort | ts-ui-dashboard |
| ts2-ts-consign-price-service-stress-7r95bt | ts-consign-price-service | 9 | ts-payment-service|ts-preserve-service|ts-consign-service|ts-security-service|ts-ui-dashboard | stress | ts-consign-price-service |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-order-service|ts-payment-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 9 | ts-ui-dashboard|ts-auth-service|ts-seat-service|ts-contacts-service|ts-order-service | bandwidth | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 9 | ts-route-plan-service|ts-payment-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-ui-dashboard-request-replace-method-dd2fll | ts-contacts-service;ts-ui-dashboard | 9 | ts-travel2-service|ts-verification-code-service|ts-travel-plan-service|ts-auth-service|ts-route-plan-service | request-replace-method | ts-ui-dashboard |
| ts6-ts-ui-dashboard-response-replace-code-tgfbsg | ts-consign-service;ts-ui-dashboard | 9 | ts-payment-service|ts-station-food-service|ts-travel-service|ts-seat-service|ts-order-service | response-replace-code | ts-ui-dashboard |

## Research Notes

- V6 supports the hypothesis that abnormal trace request-volume rise and caller self-duration growth are useful generic complements to status/latency evidence. They convert many V5 near misses into Top-1 hits, especially when the true component was already in Top-5 but lost to propagated high-traffic services.
- Remaining weak groups still include pod failures, UI/front-door request manipulation, bandwidth, and some response body/code mutations. These failures suggest that strong trace volume can still be an effect of fan-out or downstream propagation rather than a causal-local anomaly.
- Next reusable direction: gate or normalize `trace_count_rise_shift` using cross-modal agreement and topology neighbor contrast, instead of adding service-specific or fault-specific rules.
