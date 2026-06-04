# EvidenceRank V22_NEUTRAL_ALL Summary

- Created: 2026-06-04T21:35:51+08:00
- Source: `V22_NEUTRAL_ALL`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 1383 |
| AC@1 | 0.022504 |
| AC@3 | 0.026723 |
| AC@5 | 0.026723 |
| MRR | 0.024584 |
| avg_rank | 1.358974 |
| top1_miss | 1390 |
| top5_miss | 1384 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| time_bucket | ts4 | 274 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 274 |
| time_bucket | ts5 | 258 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 258 |
| time_bucket | ts2 | 221 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 221 |
| time_bucket | ts3 | 210 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 210 |
| time_bucket | ts1 | 179 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 179 |
| case_service | ts-ui-dashboard | 165 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 165 |
| case_service | ts-route-plan-service | 138 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 138 |
| case_service | ts-preserve-service | 95 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 95 |
| case_service | ts-travel-service | 92 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 92 |
| fault_type | container-kill | 89 | 0.000000 | 0.000000 | 0.000000 | 0.001404 | 89 |
| case_service | ts-seat-service | 79 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 79 |
| case_service | ts-travel-plan-service | 72 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 72 |
| case_service | ts-travel2-service | 68 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 68 |
| case_service | ts-food-service | 54 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 54 |
| case_service | ts-order-service | 45 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 45 |
| fault_type | bandwidth | 42 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 42 |
| time_bucket | ts7 | 34 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 34 |
| case_service | ts-security-service | 33 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 33 |
| case_service | ts-inside-payment-service | 28 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 28 |
| time_bucket | ts6 | 28 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 28 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-basic-service-response-replace-code-lmnjw7 | ts-basic-service;ts-route-service | None |  | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-lq4ncj | ts-basic-service;ts-station-service | None |  | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-mh6sjz | ts-basic-service;ts-price-service | None |  | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-r727qm | ts-basic-service;ts-route-service | None |  | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-v9z47n | ts-basic-service;ts-price-service | None |  | response-replace-code | ts-basic-service |
| ts0-ts-cancel-service-stress-s7tf69 | ts-cancel-service | None |  | stress | ts-cancel-service |
| ts0-ts-config-service-corrupt-qjwhfb | mysql;ts-config-service | None |  | corrupt | ts-config-service |
| ts0-ts-config-service-stress-g6rpl9 | ts-config-service | None |  | stress | ts-config-service |
| ts0-ts-consign-price-service-exception-8b6tng | ts-consign-price-service | None |  | exception | ts-consign-price-service |
| ts0-ts-consign-price-service-stress-nwzn4t | ts-consign-price-service | None |  | stress | ts-consign-price-service |
| ts0-ts-consign-price-service-stress-t67vtg | ts-consign-price-service | None |  | stress | ts-consign-price-service |
| ts0-ts-consign-service-stress-7f878v | ts-consign-service | None |  | stress | ts-consign-service |
| ts0-ts-consign-service-stress-psgrfn | ts-consign-service | None |  | stress | ts-consign-service |
| ts0-ts-contacts-service-pod-failure-j42hd8 | ts-contacts-service | None |  | pod-failure | ts-contacts-service |
| ts0-ts-food-service-container-kill-fc4sjw | ts-food-service | None |  | container-kill | ts-food-service |
| ts0-ts-food-service-stress-dq7mwn | ts-food-service | None |  | stress | ts-food-service |
| ts0-ts-food-service-stress-skmh42 | ts-food-service | None |  | stress | ts-food-service |
| ts0-ts-food-service-stress-xfwkgh | ts-food-service | None |  | stress | ts-food-service |
| ts0-ts-inside-payment-service-container-kill-cxt5lv | ts-inside-payment-service | None |  | container-kill | ts-inside-payment-service |
| ts0-ts-inside-payment-service-return-7pjv29 | ts-inside-payment-service | None |  | return | ts-inside-payment-service |
| ts0-ts-inside-payment-service-stress-5qd9rl | ts-inside-payment-service | None |  | stress | ts-inside-payment-service |
| ts0-ts-inside-payment-service-stress-jpg9xm | ts-inside-payment-service | None |  | stress | ts-inside-payment-service |
| ts0-ts-order-other-service-corrupt-wkdp68 | mysql;ts-order-other-service | None |  | corrupt | ts-order-other-service |
| ts0-ts-order-other-service-stress-4d76fr | ts-order-other-service | None |  | stress | ts-order-other-service |
| ts0-ts-order-service-delay-5hms4x | mysql;ts-order-service | None |  | delay | ts-order-service |
| ts0-ts-order-service-delay-jwmltg | mysql;ts-order-service | None |  | delay | ts-order-service |
| ts0-ts-order-service-exception-hdgpgm | ts-order-service | None |  | exception | ts-order-service |
| ts0-ts-order-service-exception-l2bqm5 | ts-order-service | None |  | exception | ts-order-service |
| ts0-ts-order-service-stress-64c8cv | ts-order-service | None |  | stress | ts-order-service |
| ts0-ts-order-service-stress-cklk2p | ts-order-service | None |  | stress | ts-order-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
