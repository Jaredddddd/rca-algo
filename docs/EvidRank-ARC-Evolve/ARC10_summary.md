# EvidenceRank ARC10 Summary

- Created: 2026-06-03T22:32:51+08:00
- Source: `current`
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.675809 |
| AC@3 | 0.918425 |
| AC@5 | 0.964838 |
| MRR | 0.801007 |
| avg_rank | 1.784810 |
| top1_miss | 461 |
| top5_miss | 50 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | delay | 21 | 0.333333 | 0.809524 | 0.904762 | 0.584921 | 2 |
| fault_type | request-delay | 88 | 0.443182 | 0.897727 | 0.943182 | 0.668782 | 5 |
| fault_type | loss | 48 | 0.458333 | 0.833333 | 0.958333 | 0.682986 | 2 |
| fault_type | response-delay | 89 | 0.494382 | 0.842697 | 0.966292 | 0.678745 | 3 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.553571 | 2 |
| case_service | ts-basic-service | 201 | 0.502488 | 0.796020 | 0.905473 | 0.666105 | 19 |
| time_bucket | ts9 | 23 | 0.521739 | 0.913043 | 0.956522 | 0.702899 | 1 |
| fault_type | bandwidth | 42 | 0.523810 | 0.833333 | 0.880952 | 0.694444 | 5 |
| time_bucket | ts6 | 28 | 0.535714 | 0.821429 | 0.892857 | 0.691369 | 3 |
| fault_type | corrupt | 46 | 0.543478 | 0.782609 | 0.956522 | 0.693901 | 2 |
| case_service | ts-order-other-service | 27 | 0.555556 | 0.925926 | 0.962963 | 0.743827 | 1 |
| case_service | mysql | 72 | 0.569444 | 0.847222 | 0.972222 | 0.730093 | 2 |
| case_service | ts-travel-service | 92 | 0.586957 | 0.956522 | 0.989130 | 0.758618 | 1 |
| case_service | ts-travel2-service | 68 | 0.588235 | 0.882353 | 0.970588 | 0.735294 | 2 |
| time_bucket | ts7 | 34 | 0.588235 | 0.852941 | 0.941176 | 0.743382 | 2 |
| time_bucket | ts8 | 25 | 0.600000 | 0.920000 | 0.960000 | 0.761333 | 1 |
| case_service | ts-route-plan-service | 138 | 0.601449 | 0.927536 | 0.971014 | 0.765036 | 4 |
| case_service | ts-security-service | 33 | 0.606061 | 0.969697 | 1.000000 | 0.778788 | 0 |
| case_service | unknown | 26 | 0.615385 | 0.884615 | 0.884615 | 0.736715 | 3 |
| fault_type | unknown | 26 | 0.615385 | 0.884615 | 0.884615 | 0.736715 | 3 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 31 | ts-food-service|ts-seat-service|ts-ui-dashboard|loadgenerator|ts-consign-service | container-kill | ts-food-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 30 | ts-auth-service|ts-travel-service|ts-food-service|ts-route-plan-service|ts-order-other-service | pod-failure | mysql |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 26 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-order-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 23 | ts-food-service|ts-travel-service|ts-order-service|ts-config-service|ts-inside-payment-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 21 | ts-inside-payment-service|ts-travel-service|ts-assurance-service|ts-order-service|ts-seat-service | return | ts-cancel-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 20 | ts-auth-service|ts-ui-dashboard|ts-seat-service|ts-preserve-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 17 | ts-payment-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 13 | ts-preserve-service|ts-food-service|ts-notification-service|ts-ui-dashboard|ts-route-plan-service | response-replace-body | ts-basic-service |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 12 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-ui-dashboard | bandwidth | ts-station-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 12 | ts-payment-service|ts-inside-payment-service|ts-food-service|ts-basic-service|ts-seat-service | request-abort | ts-ui-dashboard |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 11 | ts-ui-dashboard|ts-order-service|ts-consign-price-service|loadgenerator|ts-inside-payment-service | partition | ts-seat-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 11 | ts-payment-service|ts-consign-price-service|ts-inside-payment-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-route-service-corrupt-5z9zfl | mysql;ts-route-service | 9 | ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel-service | corrupt | ts-route-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-travel-service|ts-order-service|ts-auth-service|ts-security-service|ts-preserve-service | unknown | unknown |
| ts5-ts-basic-service-request-delay-xjt5h5 | ts-basic-service;ts-train-service | 9 | ts-preserve-service|ts-route-plan-service|ts-ui-dashboard|ts-seat-service|ts-payment-service | request-delay | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 9 | loadgenerator|ts-seat-service|ts-station-food-service|ts-order-service|ts-food-service | request-abort | ts-ui-dashboard |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 8 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 8 | ts-travel-service|ts-seat-service|ts-food-service|ts-order-service|ts-station-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 8 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-seat-service|ts-auth-service | bandwidth | ts-basic-service |
| ts4-ts-basic-service-corrupt-trd2kh | ts-basic-service;ts-preserve-service | 8 | ts-ui-dashboard|ts-seat-service|ts-verification-code-service|ts-food-service|ts-security-service | corrupt | ts-basic-service |
| ts4-ts-basic-service-request-delay-xhctbw | ts-basic-service;ts-train-service | 8 | ts-route-plan-service|ts-preserve-service|ts-travel2-service|ts-travel-service|ts-seat-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 8 | ts-route-plan-service|ts-security-service|ts-travel-plan-service|ts-travel-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | loadgenerator|ts-ui-dashboard|ts-food-service|ts-seat-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 8 | ts-preserve-service|ts-cancel-service|ts-seat-service|ts-food-service|ts-order-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 8 | ts-preserve-service|ts-cancel-service|ts-consign-price-service|ts-seat-service|ts-food-service | request-replace-path | ts-basic-service |
| ts5-ts-basic-service-response-abort-7f8qrl | ts-basic-service;ts-price-service | 8 | ts-consign-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-seat-service | response-abort | ts-basic-service |
| ts5-ts-basic-service-response-delay-m48s7x | ts-basic-service;ts-train-service | 8 | ts-ui-dashboard|ts-preserve-service|ts-travel2-service|ts-travel-service|ts-route-plan-service | response-delay | ts-basic-service |
| ts5-ts-travel2-service-response-replace-body-ljvb7g | ts-route-service;ts-travel2-service | 8 | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-food-service|ts-ui-dashboard | response-replace-body | ts-travel2-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 8 | ts-seat-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-preserve-service | response-replace-code | ts-travel2-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
