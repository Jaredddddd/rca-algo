# EvidenceRank V18 Summary

- Created: 2026-06-02T21:15:00+08:00
- Source: `current`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.506329 |
| AC@3 | 0.833333 |
| AC@5 | 0.941632 |
| MRR | 0.684853 |
| avg_rank | 2.246132 |
| top1_miss | 702 |
| top5_miss | 83 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | response-abort | 44 | 0.159091 | 0.704545 | 0.931818 | 0.463474 | 3 |
| fault_type | response-replace-code | 231 | 0.186147 | 0.636364 | 0.874459 | 0.443364 | 29 |
| case_service | ts-ui-dashboard | 165 | 0.224242 | 0.715152 | 0.878788 | 0.493832 | 20 |
| fault_type | request-abort | 60 | 0.233333 | 0.733333 | 0.916667 | 0.514738 | 5 |
| fault_type | response-replace-body | 51 | 0.235294 | 0.647059 | 0.882353 | 0.471880 | 6 |
| case_service | ts-basic-service | 201 | 0.253731 | 0.597015 | 0.845771 | 0.472624 | 31 |
| case_service | ts-travel2-service | 68 | 0.294118 | 0.602941 | 0.911765 | 0.511210 | 6 |
| time_bucket | ts7 | 34 | 0.294118 | 0.705882 | 0.823529 | 0.525117 | 6 |
| fault_type | request-replace-path | 39 | 0.307692 | 0.666667 | 0.871795 | 0.536111 | 5 |
| time_bucket | ts8 | 25 | 0.320000 | 0.760000 | 0.920000 | 0.553714 | 2 |
| time_bucket | ts6 | 28 | 0.321429 | 0.750000 | 0.892857 | 0.563690 | 3 |
| fault_type | request-replace-method | 190 | 0.342105 | 0.721053 | 0.905263 | 0.572806 | 18 |
| case_service | ts-route-plan-service | 138 | 0.376812 | 0.847826 | 0.942029 | 0.616546 | 8 |
| fault_type | response-delay | 89 | 0.426966 | 0.921348 | 0.966292 | 0.662297 | 3 |
| fault_type | request-delay | 88 | 0.431818 | 0.943182 | 1.000000 | 0.675947 | 0 |
| time_bucket | ts9 | 23 | 0.434783 | 0.739130 | 0.869565 | 0.604710 | 3 |
| case_service | ts-travel-plan-service | 72 | 0.458333 | 0.875000 | 0.972222 | 0.675860 | 2 |
| case_service | ts-travel-service | 92 | 0.478261 | 0.891304 | 0.978261 | 0.683152 | 2 |
| case_service | ts-seat-service | 79 | 0.481013 | 0.759494 | 0.911392 | 0.652854 | 7 |
| case_service | ts-order-other-service | 27 | 0.481481 | 0.925926 | 1.000000 | 0.695679 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-voucher-service|ts-config-service|ts-train-food-service|ts-consign-price-service|ts-travel-service | unknown | unknown |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 28 | ts-auth-service|ts-basic-service|ts-train-food-service|ts-route-service|ts-travel-service | pod-failure | ts-travel-plan-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 26 | ts-food-service|ts-seat-service|ts-train-food-service|ts-ui-dashboard|ts-consign-service | container-kill | ts-food-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 24 | ts-payment-service|ts-train-food-service|ts-consign-price-service|ts-preserve-service|ts-seat-service | response-replace-code | ts-basic-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 17 | ts-consign-price-service|ts-ticket-office-service|ts-order-service|ts-ui-dashboard|ts-inside-payment-service | partition | ts-seat-service |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 17 | ts-train-food-service|ts-food-service|ts-order-service|ts-seat-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 16 | ts-payment-service|ts-consign-price-service|ts-station-food-service|ts-inside-payment-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-partition-w5hbjw | ts-basic-service;ts-travel-service | 15 | ts-delivery-service|ts-preserve-other-service|ts-admin-basic-info-service|ts-admin-order-service|ts-admin-route-service | partition | ts-basic-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 15 | ts-payment-service|ts-consign-price-service|ts-station-food-service|ts-consign-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 14 | ts-notification-service|ts-delivery-service|ts-route-plan-service|ts-preserve-service|ts-consign-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 12 | ts-ui-dashboard|ts-preserve-service|ts-travel2-service|ts-seat-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 12 | ts-payment-service|ts-delivery-service|ts-notification-service|ts-consign-price-service|ts-ui-dashboard | response-replace-body | ts-route-plan-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 12 | ts-payment-service|ts-voucher-service|ts-inside-payment-service|ts-assurance-service|loadgenerator | request-abort | ts-ui-dashboard |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 11 | ts-payment-service|ts-delivery-service|ts-consign-service|ts-verification-code-service|ts-price-service | unknown | unknown |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 11 | ts-cancel-service|ts-order-service|ts-preserve-service|ts-travel2-service|ts-food-service | request-replace-method | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 11 | ts-station-food-service|loadgenerator|ts-travel2-service|ts-contacts-service|ts-seat-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 10 | ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-auth-service|ts-order-service | bandwidth | ts-basic-service |
| ts7-ts-ui-dashboard-response-replace-code-jv845c | ts-travel-plan-service;ts-ui-dashboard | 10 | ts-payment-service|ts-inside-payment-service|ts-station-food-service|ts-preserve-service|ts-consign-price-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 9 | ts-ticket-office-service|ts-news-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 9 | ts-ui-dashboard|ts-order-other-service|ts-contacts-service|ts-order-service|ts-auth-service | bandwidth | ts-route-plan-service |
| ts5-ts-travel2-service-response-replace-body-ljvb7g | ts-route-service;ts-travel2-service | 9 | rabbitmq|ts-delivery-service|ts-travel-plan-service|ts-seat-service|ts-route-plan-service | response-replace-body | ts-travel2-service |
| ts5-ts-ui-dashboard-response-replace-code-fvp5cd | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-news-service|ts-ticket-office-service|ts-consign-service|ts-inside-payment-service|ts-verification-code-service | response-replace-code | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-delay-t55rlr | ts-route-plan-service;ts-travel-service | 9 | ts-station-food-service|ts-inside-payment-service|ts-consign-price-service|ts-assurance-service|ts-ui-dashboard | response-delay | ts-route-plan-service |
| ts0-ts-travel-plan-service-time-rjdx4x | ts-travel-plan-service | 8 | ts-route-plan-service|ts-train-food-service|ts-security-service|ts-station-food-service|ts-assurance-service | unknown | unknown |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 8 | ts-security-service|ts-notification-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 8 | ts-cancel-service|ts-consign-price-service|ts-seat-service|ts-preserve-service|ts-route-plan-service | request-replace-path | ts-basic-service |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 8 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-order-service | response-replace-code | ts-travel2-service |
| ts5-ts-ui-dashboard-request-replace-method-dxffln | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-contacts-service|ts-security-service|ts-consign-service|loadgenerator | request-replace-method | ts-ui-dashboard |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 8 | ts-ticket-office-service|ts-order-service|loadgenerator|ts-consign-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts7-ts-ui-dashboard-response-replace-code-t7vsbl | ts-travel-service;ts-ui-dashboard | 8 | ts-cancel-service|ts-inside-payment-service|ts-payment-service|ts-station-food-service|ts-notification-service | response-replace-code | ts-ui-dashboard |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
