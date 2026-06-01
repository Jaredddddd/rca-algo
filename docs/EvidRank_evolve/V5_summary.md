# EvidenceRank V5 Summary

- Created: 2026-06-01T21:02:02+08:00
- Source: `V5`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.699015 |
| AC@3 | 0.902954 |
| AC@5 | 0.963432 |
| MRR | 0.810334 |
| avg_rank | 1.838959 |
| top1_miss | 428 |
| top5_miss | 52 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| time_bucket | ts6 | 28 | 0.392857 | 0.750000 | 0.928571 | 0.598810 | 2 |
| time_bucket | ts8 | 25 | 0.400000 | 0.880000 | 0.960000 | 0.650303 | 1 |
| case_service | ts-ui-dashboard | 165 | 0.448485 | 0.739394 | 0.872727 | 0.628019 | 21 |
| case_service | ts-security-service | 33 | 0.484848 | 0.939394 | 1.000000 | 0.727273 | 0 |
| time_bucket | ts7 | 34 | 0.500000 | 0.735294 | 0.882353 | 0.659104 | 4 |
| fault_type | pod-failure | 24 | 0.500000 | 0.833333 | 0.875000 | 0.663993 | 3 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.550926 | 2 |
| time_bucket | ts9 | 23 | 0.521739 | 0.826087 | 0.956522 | 0.701691 | 1 |
| fault_type | bandwidth | 42 | 0.523810 | 0.738095 | 0.880952 | 0.655460 | 5 |
| case_service | ts-travel2-service | 68 | 0.573529 | 0.882353 | 1.000000 | 0.731373 | 0 |
| fault_type | response-delay | 89 | 0.584270 | 0.865169 | 0.977528 | 0.745176 | 2 |
| fault_type | response-replace-body | 51 | 0.588235 | 0.843137 | 0.960784 | 0.736298 | 2 |
| fault_type | response-replace-code | 231 | 0.601732 | 0.887446 | 0.969697 | 0.757394 | 7 |
| case_service | ts-basic-service | 201 | 0.601990 | 0.885572 | 0.965174 | 0.751976 | 7 |
| case_service | ts-travel-service | 92 | 0.608696 | 0.978261 | 1.000000 | 0.784420 | 0 |
| time_bucket | ts5 | 258 | 0.624031 | 0.872093 | 0.968992 | 0.763683 | 8 |
| case_service | ts-order-other-service | 27 | 0.629630 | 0.962963 | 1.000000 | 0.793210 | 0 |
| case_service | ts-route-plan-service | 138 | 0.630435 | 0.869565 | 0.956522 | 0.763616 | 6 |
| time_bucket | ts4 | 274 | 0.638686 | 0.883212 | 0.974453 | 0.771456 | 7 |
| fault_type | request-replace-method | 190 | 0.642105 | 0.852632 | 0.915789 | 0.762860 | 16 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 35 | ts-auth-service|ts-train-food-service|ts-station-food-service|ts-security-service|ts-payment-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-seat-service|ts-travel-service|ts-route-plan-service|ts-order-other-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-seat-service|ts-travel-service|ts-order-other-service|ts-basic-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 27 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-basic-service|ts-auth-service | return | ts-cancel-service |
| ts2-ts-consign-price-service-stress-7r95bt | ts-consign-price-service | 27 | ts-payment-service|ts-preserve-service|ts-security-service|ts-seat-service|ts-consign-service | stress | ts-consign-price-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 25 | ts-food-service|ts-ui-dashboard|ts-seat-service|ts-travel-service|ts-order-service | container-kill | ts-food-service |
| ts2-ts-consign-price-service-container-kill-lj9llf | ts-consign-price-service | 19 | ts-seat-service|ts-basic-service|ts-ui-dashboard|ts-auth-service|ts-route-service | container-kill | ts-consign-price-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 19 | ts-seat-service|ts-order-service|ts-travel-service|ts-train-food-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 18 | ts-payment-service|ts-inside-payment-service|ts-verification-code-service|ts-basic-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 17 | ts-seat-service|ts-basic-service|ts-order-service|ts-auth-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 16 | ts-consign-service|ts-payment-service|ts-verification-code-service|ts-seat-service|ts-travel-service | unknown | unknown |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 13 | ts-preserve-service|ts-consign-service|ts-seat-service|ts-order-service|ts-ui-dashboard | bandwidth | ts-station-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 12 | ts-station-food-service|loadgenerator|ts-seat-service|ts-travel-plan-service|ts-travel2-service | request-abort | ts-ui-dashboard |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 12 | ts-payment-service|ts-inside-payment-service|ts-preserve-service|ts-station-food-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts0-ts-ui-dashboard-request-replace-method-z9kbl2 | ts-train-service;ts-ui-dashboard | 11 | ts-payment-service|ts-consign-price-service|ts-train-food-service|ts-inside-payment-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-475jm4 | ts-assurance-service;ts-ui-dashboard | 11 | ts-consign-price-service|ts-route-plan-service|ts-station-food-service|ts-travel2-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 11 | ts-payment-service|ts-train-food-service|ts-ui-dashboard|ts-seat-service|ts-order-service | response-replace-code | ts-basic-service |
| ts5-ts-ui-dashboard-request-replace-method-dd2fll | ts-contacts-service;ts-ui-dashboard | 11 | ts-travel2-service|ts-auth-service|ts-basic-service|ts-verification-code-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 11 | ts-payment-service|ts-consign-price-service|ts-consign-service|ts-station-food-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 10 | ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-order-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | ts-food-service;ts-ui-dashboard | 9 | ts-seat-service|ts-order-service|ts-config-service|ts-route-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-seat-service|ts-order-service|ts-travel2-service|ts-travel-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 9 | ts-payment-service|ts-consign-price-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service | request-replace-method | ts-basic-service |
| ts5-ts-route-plan-service-response-delay-vjgk5j | ts-route-plan-service;ts-travel2-service | 9 | ts-consign-price-service|ts-contacts-service|ts-order-service|ts-travel-plan-service|ts-ui-dashboard | response-delay | ts-route-plan-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 8 | ts-auth-service|ts-travel-service|ts-preserve-service|ts-security-service|ts-order-service | unknown | unknown |
| ts2-ts-ui-dashboard-request-replace-method-jrt2mv | ts-train-service;ts-ui-dashboard | 8 | ts-seat-service|ts-order-service|ts-travel-service|ts-order-other-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-inside-payment-service|ts-payment-service|ts-travel-service|ts-seat-service|ts-order-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 8 | ts-inside-payment-service|ts-order-other-service|ts-seat-service|ts-route-plan-service|ts-basic-service | pod-failure | ts-payment-service |
| ts3-ts-ui-dashboard-request-replace-method-7lstrz | ts-assurance-service;ts-ui-dashboard | 8 | ts-seat-service|ts-basic-service|ts-verification-code-service|ts-order-service|ts-config-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-hh8qpt | ts-consign-service;ts-ui-dashboard | 8 | ts-cancel-service|ts-auth-service|ts-order-service|ts-seat-service|ts-travel-service | request-replace-method | ts-ui-dashboard |

## Research Notes

- V5 strongly supports the endpoint-local status shift hypothesis. A residual `span_name + status` distribution shift, after subtracting endpoint-only traffic mix drift, separates many true roots from high-volume propagated services.
- The largest remaining weak group is still `ts-ui-dashboard`, plus pod-failure and bandwidth cases where HTTP status evidence is weak, absent, or points to caller-visible symptoms rather than the infrastructure/root service.
- Do not increase the status weight further without reviewing the 37 `regressed_from_hit1` cases and the 10 rank-regressed cases that moved outside Top-5. The next reusable improvement should add confidence gating or a non-HTTP infrastructure signal, not a case/service/fault branch.
