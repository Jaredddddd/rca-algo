# EvidenceRank V2 Summary

- Created: 2026-06-01T14:41:10+08:00
- Source: `V2`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.531646 |
| AC@3 | 0.786920 |
| AC@5 | 0.886779 |
| MRR | 0.684448 |
| avg_rank | 2.664557 |
| top1_miss | 666 |
| top5_miss | 161 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | bandwidth | 42 | 0.238095 | 0.523810 | 0.714286 | 0.418679 | 12 |
| fault_type | response-replace-code | 231 | 0.259740 | 0.606061 | 0.818182 | 0.484906 | 42 |
| fault_type | response-abort | 44 | 0.295455 | 0.681818 | 0.863636 | 0.532107 | 6 |
| time_bucket | ts8 | 25 | 0.320000 | 0.600000 | 0.800000 | 0.524017 | 5 |
| time_bucket | ts6 | 28 | 0.321429 | 0.678571 | 0.928571 | 0.545833 | 2 |
| time_bucket | ts7 | 34 | 0.352941 | 0.735294 | 0.823529 | 0.571161 | 6 |
| case_service | ts-travel-plan-service | 72 | 0.361111 | 0.763889 | 0.888889 | 0.588589 | 8 |
| case_service | mysql | 72 | 0.375000 | 0.625000 | 0.694444 | 0.530882 | 22 |
| case_service | ts-route-plan-service | 138 | 0.376812 | 0.601449 | 0.789855 | 0.547551 | 29 |
| case_service | ts-ui-dashboard | 165 | 0.381818 | 0.684848 | 0.836364 | 0.575197 | 27 |
| fault_type | request-replace-path | 39 | 0.384615 | 0.743590 | 0.871795 | 0.590232 | 5 |
| case_service | ts-basic-service | 201 | 0.407960 | 0.706468 | 0.850746 | 0.594309 | 30 |
| time_bucket | ts5 | 258 | 0.410853 | 0.720930 | 0.841085 | 0.599537 | 41 |
| fault_type | corrupt | 46 | 0.413043 | 0.760870 | 0.826087 | 0.613044 | 8 |
| case_service | ts-security-service | 33 | 0.424242 | 0.727273 | 0.939394 | 0.603260 | 2 |
| fault_type | response-replace-body | 51 | 0.431373 | 0.784314 | 0.901961 | 0.635520 | 5 |
| time_bucket | ts9 | 23 | 0.434783 | 0.695652 | 0.826087 | 0.593047 | 4 |
| fault_type | request-replace-method | 190 | 0.457895 | 0.715789 | 0.821053 | 0.624616 | 34 |
| fault_type | loss | 48 | 0.458333 | 0.812500 | 0.854167 | 0.647098 | 7 |
| fault_type | request-abort | 60 | 0.466667 | 0.800000 | 0.883333 | 0.657279 | 7 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 35 | ts-auth-service|ts-train-food-service|ts-verification-code-service|ts-station-food-service|ts-security-service | pod-failure | ts-travel-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-seat-service|ts-travel-service|ts-order-other-service|ts-basic-service | unknown | unknown |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | ts-auth-service|ts-seat-service|ts-travel-service|ts-route-plan-service|ts-basic-service | pod-failure | mysql |
| ts2-ts-consign-price-service-stress-7r95bt | ts-consign-price-service | 27 | ts-payment-service|ts-preserve-service|ts-security-service|ts-seat-service|ts-ui-dashboard | stress | ts-consign-price-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 26 | ts-food-service|ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-order-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 25 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-basic-service|ts-auth-service | return | ts-cancel-service |
| ts2-mysql-partition-5zrq5z | mysql;ts-contacts-service | 20 | ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-travel-service|ts-order-service | partition | mysql |
| ts2-ts-consign-service-partition-xbv84t | mysql;ts-consign-service | 20 | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-order-service|ts-route-plan-service | partition | ts-consign-service |
| ts4-ts-inside-payment-service-return-x4gr5r | ts-inside-payment-service | 20 | ts-assurance-service|ts-station-food-service|ts-seat-service|ts-verification-code-service|ts-travel-service | return | ts-inside-payment-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 19 | ts-seat-service|ts-order-service|ts-travel-service|ts-basic-service|ts-food-service | request-abort | ts-ui-dashboard |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 19 | ts-consign-price-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-preserve-service | response-replace-code | ts-travel-plan-service |
| ts2-ts-consign-price-service-container-kill-lj9llf | ts-consign-price-service | 18 | ts-seat-service|ts-basic-service|ts-ui-dashboard|ts-verification-code-service|ts-order-service | container-kill | ts-consign-price-service |
| ts3-ts-consign-service-bandwidth-pmdbk7 | mysql;ts-consign-service | 18 | ts-ui-dashboard|ts-seat-service|ts-verification-code-service|ts-travel2-service|ts-basic-service | bandwidth | ts-consign-service |
| ts3-ts-contacts-service-loss-6lcnb9 | mysql;ts-contacts-service | 18 | ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-basic-service|ts-auth-service | loss | ts-contacts-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 18 | ts-payment-service|ts-inside-payment-service|ts-basic-service|ts-verification-code-service|ts-seat-service | request-abort | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-475jm4 | ts-assurance-service;ts-ui-dashboard | 16 | ts-consign-price-service|ts-route-plan-service|ts-station-food-service|ts-travel2-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts1-mysql-bandwidth-2xj2mq | mysql;ts-consign-service | 15 | ts-order-service|ts-food-service|ts-preserve-service|ts-route-service|ts-ui-dashboard | bandwidth | mysql |
| ts3-mysql-bandwidth-5xvc22 | mysql;ts-consign-service | 15 | ts-travel-plan-service|ts-food-service|ts-route-service|ts-ui-dashboard|ts-travel-service | bandwidth | mysql |
| ts6-ts-route-plan-service-response-replace-code-9pfgvr | ts-route-plan-service;ts-route-service | 15 | ts-payment-service|ts-consign-price-service|ts-security-service|ts-consign-service|ts-ui-dashboard | response-replace-code | ts-route-plan-service |
| ts0-mysql-partition-cfvlsw | mysql;ts-travel2-service | 14 | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-verification-code-service|ts-travel-service | partition | mysql |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 14 | ts-payment-service|ts-verification-code-service|ts-seat-service|ts-travel-service|ts-order-service | unknown | unknown |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 14 | ts-seat-service|ts-basic-service|ts-order-service|ts-travel-service|ts-auth-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 13 | ts-preserve-service|ts-seat-service|ts-order-service|ts-ui-dashboard|ts-basic-service | bandwidth | ts-station-service |
| ts0-ts-station-service-loss-hs8vrm | mysql;ts-station-service | 13 | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | loss | ts-station-service |
| ts2-mysql-corrupt-lt5n6d | mysql;ts-contacts-service | 13 | ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-basic-service|ts-travel2-service | corrupt | mysql |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 13 | ts-consign-service|ts-route-plan-service|ts-seat-service|ts-verification-code-service|ts-travel-service | response-abort | ts-basic-service |
| ts5-ts-preserve-service-request-replace-method-gvn4ls | ts-contacts-service;ts-preserve-service | 13 | ts-security-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-verification-code-service | request-replace-method | ts-preserve-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 13 | ts-station-food-service|ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts1-mysql-bandwidth-s7srkn | mysql;ts-travel-service | 12 | ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-food-service|ts-seat-service | bandwidth | mysql |
| ts2-mysql-bandwidth-bbk2d4 | mysql;ts-station-service | 12 | ts-basic-service|ts-travel-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service | bandwidth | mysql |

## Research Notes

- V2 failure mechanism fixed: feature fusion should be robust to sparse observability. A missing or undefined modality is feature-level no-evidence, not service-level negative evidence.
- Remaining weak groups still point to propagation and endpoint-symptom ambiguity: `bandwidth`, request/response mutation faults, and infrastructure plus business-service multi-GT cases still often rank high-volume neighbors above roots.
- Do not read `conclusion.parquet`. If endpoint-level evidence is revisited, reconstruct it only from raw traces and require confidence gating plus topology-aware suppression before rank fusion.
- Next reusable direction: neighbor contrast or topology-aware rerank that distinguishes a service's own anomaly from anomalies inherited from upstream/downstream traffic.
