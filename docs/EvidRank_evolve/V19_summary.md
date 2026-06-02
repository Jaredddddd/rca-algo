# EvidenceRank V19 Summary

- Created: 2026-06-02T22:25:28+08:00
- Source: `V19`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.658931 |
| AC@3 | 0.877637 |
| AC@5 | 0.927567 |
| MRR | 0.776972 |
| avg_rank | 2.179325 |
| top1_miss | 485 |
| top5_miss | 103 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | ts-ui-dashboard | 165 | 0.193939 | 0.733333 | 0.830303 | 0.478942 | 28 |
| fault_type | pod-failure | 24 | 0.250000 | 0.666667 | 0.916667 | 0.523611 | 2 |
| time_bucket | ts9 | 23 | 0.391304 | 0.782609 | 0.869565 | 0.618478 | 3 |
| fault_type | response-delay | 89 | 0.404494 | 0.707865 | 0.786517 | 0.588710 | 19 |
| fault_type | request-delay | 88 | 0.409091 | 0.727273 | 0.818182 | 0.594367 | 16 |
| time_bucket | ts6 | 28 | 0.428571 | 0.678571 | 0.821429 | 0.582681 | 5 |
| fault_type | corrupt | 46 | 0.434783 | 0.717391 | 0.804348 | 0.594180 | 9 |
| time_bucket | ts7 | 34 | 0.441176 | 0.705882 | 0.882353 | 0.618640 | 4 |
| fault_type | delay | 21 | 0.476190 | 0.904762 | 0.952381 | 0.682143 | 1 |
| case_service | ts-travel-service | 92 | 0.478261 | 0.836957 | 0.913043 | 0.667167 | 8 |
| case_service | ts-route-service | 23 | 0.478261 | 0.782609 | 0.913043 | 0.638043 | 2 |
| time_bucket | ts8 | 25 | 0.480000 | 0.800000 | 0.880000 | 0.668067 | 3 |
| time_bucket | ts4 | 274 | 0.543796 | 0.817518 | 0.901460 | 0.690591 | 27 |
| time_bucket | ts5 | 258 | 0.558140 | 0.790698 | 0.852713 | 0.689902 | 38 |
| case_service | ts-travel2-service | 68 | 0.573529 | 0.882353 | 0.911765 | 0.728904 | 6 |
| case_service | ts-seat-service | 79 | 0.594937 | 0.860759 | 0.949367 | 0.734474 | 4 |
| case_service | ts-basic-service | 201 | 0.601990 | 0.771144 | 0.870647 | 0.708942 | 26 |
| case_service | ts-auth-service | 26 | 0.615385 | 0.961538 | 0.961538 | 0.794872 | 1 |
| fault_type | request-abort | 60 | 0.616667 | 0.833333 | 0.916667 | 0.741917 | 5 |
| fault_type | bandwidth | 42 | 0.619048 | 0.809524 | 0.880952 | 0.731660 | 5 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 35 | ts-food-service|loadgenerator|ts-train-service|ts-seat-service|ts-train-food-service | container-kill | ts-food-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 33 | ts-auth-service|ts-contacts-service|ts-order-service|ts-user-service|ts-config-service | bandwidth | ts-route-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-voucher-service|ts-consign-price-service|ts-travel-service|ts-train-service|ts-config-service | unknown | unknown |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 27 | ts-order-service|ts-price-service|ts-inside-payment-service|ts-notification-service|ts-travel-plan-service | partition | ts-seat-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 25 | loadgenerator|ts-train-food-service|ts-train-service|ts-station-service|ts-seat-service | request-abort | ts-ui-dashboard |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 23 | ts-route-plan-service|ts-travel-service|loadgenerator|ts-travel-plan-service|ts-consign-service | bandwidth | ts-station-service |
| ts5-ts-basic-service-request-delay-xjt5h5 | ts-basic-service;ts-train-service | 22 | ts-preserve-service|ts-cancel-service|ts-route-plan-service|loadgenerator|ts-travel-plan-service | request-delay | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 22 | ts-route-plan-service|loadgenerator|ts-travel-plan-service|ts-payment-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts4-ts-basic-service-request-delay-xhctbw | ts-basic-service;ts-train-service | 21 | ts-route-plan-service|ts-travel2-service|ts-assurance-service|ts-travel-plan-service|ts-notification-service | request-delay | ts-basic-service |
| ts5-ts-travel2-service-response-delay-b7zvcf | ts-route-service;ts-travel2-service | 21 | ts-voucher-service|loadgenerator|ts-assurance-service|ts-travel-service|ts-route-plan-service | response-delay | ts-travel2-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 19 | loadgenerator|ts-travel2-service|ts-contacts-service|ts-ui-dashboard|ts-route-service | response-replace-code | ts-basic-service |
| ts5-ts-ui-dashboard-response-replace-code-fvp5cd | ts-travel-plan-service;ts-ui-dashboard | 18 | ts-consign-service|ts-news-service|ts-verification-code-service|ts-ticket-office-service|ts-price-service | response-replace-code | ts-ui-dashboard |
| ts6-ts-preserve-service-partition-jvzrwx | ts-preserve-service;ts-ui-dashboard | 18 | ts-food-service|ts-payment-service|ts-basic-service|loadgenerator|ts-price-service | partition | ts-preserve-service |
| ts4-ts-basic-service-request-delay-jshmsn | ts-basic-service;ts-station-service | 17 | ts-route-plan-service|ts-travel-service|ts-order-service|ts-travel2-service|ts-security-service | request-delay | ts-basic-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 17 | ts-payment-service|ts-station-food-service|loadgenerator|ts-price-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 16 | loadgenerator|ts-payment-service|ts-preserve-service|ts-station-food-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts5-ts-order-service-corrupt-bd4p5g | ts-order-service;ts-ui-dashboard | 16 | ts-assurance-service|ts-security-service|ts-station-food-service|ts-consign-price-service|ts-consign-service | corrupt | ts-order-service |
| ts4-ts-ui-dashboard-request-delay-pqkrj8 | ts-travel-plan-service;ts-ui-dashboard | 15 | ts-voucher-service|loadgenerator|ts-order-service|ts-assurance-service|ts-consign-service | request-delay | ts-ui-dashboard |
| ts5-ts-basic-service-response-delay-wwd22h | ts-basic-service;ts-station-service | 15 | ts-ticket-office-service|ts-preserve-service|ts-route-plan-service|ts-travel-service|ts-config-service | response-delay | ts-basic-service |
| ts5-ts-route-service-corrupt-vvvjts | ts-route-plan-service;ts-route-service | 15 | ts-basic-service|loadgenerator|ts-travel2-service|ts-ui-dashboard|ts-station-food-service | corrupt | ts-route-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 15 | ts-payment-service|loadgenerator|ts-inside-payment-service|ts-station-food-service|ts-consign-price-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-food-service-bandwidth-b5qvk5 | ts-food-service;ts-ui-dashboard | 14 | ts-consign-service|loadgenerator|ts-order-service|ts-config-service|ts-seat-service | bandwidth | ts-food-service |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 14 | ts-preserve-service|loadgenerator|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 13 | ts-consign-service|ts-order-service|ts-travel-service|ts-cancel-service|ts-route-plan-service | unknown | unknown |
| ts4-ts-basic-service-corrupt-trd2kh | ts-basic-service;ts-preserve-service | 13 | ts-contacts-service|ts-verification-code-service|ts-food-service|ts-price-service|ts-security-service | corrupt | ts-basic-service |
| ts4-ts-seat-service-response-delay-46hcdn | ts-order-other-service;ts-seat-service | 13 | ts-ticket-office-service|ts-ui-dashboard|ts-verification-code-service|ts-contacts-service|ts-security-service | response-delay | ts-seat-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 13 | ts-preserve-service|loadgenerator|ts-order-service|ts-travel2-service|ts-food-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-delay-m48s7x | ts-basic-service;ts-train-service | 13 | ts-travel2-service|ts-preserve-service|ts-ui-dashboard|ts-station-service|ts-route-plan-service | response-delay | ts-basic-service |
| ts1-ts-basic-service-request-delay-9w85fg | ts-basic-service;ts-station-service | 12 | ts-voucher-service|ts-user-service|ts-train-food-service|ts-consign-service|ts-preserve-service | request-delay | ts-basic-service |
| ts5-ts-travel2-service-partition-2zcnc7 | ts-travel2-service;ts-ui-dashboard | 12 | ts-ticket-office-service|ts-basic-service|ts-seat-service|ts-travel-service|ts-preserve-service | partition | ts-travel2-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
