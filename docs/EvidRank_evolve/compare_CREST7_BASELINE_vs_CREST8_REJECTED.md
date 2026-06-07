# EvidenceRank Compare CREST7_BASELINE vs CREST8_REJECTED

- Created: 2026-06-07T19:15:31+08:00
- Old: `CREST7_BASELINE`
- New: `CREST8_REJECTED`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.340366 | -0.459916 |
| AC@3 | 0.944444 | 0.447257 | -0.497187 |
| AC@5 | 0.971871 | 0.530942 | -0.440928 |
| MRR | 0.875326 | 0.439628 | -0.435698 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 45 |
| rank_improved | 15 |
| rank_regressed | 214 |
| regressed_from_hit1 | 699 |
| unchanged | 449 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-route-service|ts-assurance-service|ts-auth-service|ts-preserve-service|ts-station-service | request-replace-method | ts-basic-service |
| ts0-ts-contacts-service-pod-failure-j42hd8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service | ts-contacts-service|loadgenerator|ts-consign-service|ts-station-service|ts-train-service | pod-failure | ts-contacts-service |
| ts0-ts-seat-service-pod-failure-c87xdg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service | ts-seat-service|ts-train-service|ts-route-service|ts-price-service|ts-order-other-service | pod-failure | ts-seat-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-contacts-service|loadgenerator|ts-price-service|ts-user-service | response-replace-code | ts-seat-service |
| ts0-ts-travel-service-mysql-28wmss | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-consign-price-service|ts-assurance-service|rabbitmq|loadgenerator | unknown | unknown |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-station-food-service|ts-order-other-service | pod-failure | ts-user-service |
| ts1-ts-basic-service-response-replace-code-6d6shc | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ticket-office-service|ts-user-service|ts-station-service|loadgenerator | response-replace-code | ts-basic-service |
| ts1-ts-config-service-latency-5kkcrc | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-consign-service|loadgenerator|ts-auth-service|ts-assurance-service | unknown | unknown |
| ts1-ts-food-service-stress-cm6h5v | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-inside-payment-service|ts-consign-service|ts-assurance-service|ts-payment-service | stress | ts-food-service |
| ts1-ts-order-service-exception-b25hld | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|loadgenerator|ts-assurance-service|ts-consign-service|ts-train-food-service | exception | ts-order-service |
| ts1-ts-order-service-exception-m9vqmq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-consign-service|ts-assurance-service|ts-voucher-service|loadgenerator | exception | ts-order-service |
| ts1-ts-payment-service-stress-k7stf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|loadgenerator|ts-assurance-service|ts-contacts-service | stress | ts-payment-service |
| ts1-ts-seat-service-response-replace-body-hvd8x2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-route-service|loadgenerator|ts-user-service|ts-travel-service | response-replace-body | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-user-service|loadgenerator|ts-contacts-service|ts-train-service | response-replace-code | ts-seat-service |
| ts2-ts-basic-service-request-replace-method-v6gzn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-station-service|ts-user-service|ts-basic-service|ts-voucher-service|ts-train-service | request-replace-method | ts-basic-service |
| ts2-ts-basic-service-request-replace-path-flkd7v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-price-service|ts-basic-service|ts-train-service|ts-station-service|ts-train-food-service | request-replace-path | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-user-service|ts-order-service|loadgenerator|ts-train-service | response-replace-code | ts-basic-service |
| ts2-ts-order-service-container-kill-sr295f | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-food-service|ts-inside-payment-service|loadgenerator|ts-contacts-service | container-kill | ts-order-service |
| ts2-ts-route-plan-service-return-xw84fv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-consign-service|ts-station-food-service|ts-assurance-service|ts-train-food-service | return | ts-route-plan-service |
| ts2-ts-station-service-dns-nn49s2 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-consign-service|loadgenerator|ts-assurance-service|ts-payment-service | unknown | unknown |
| ts3-ts-auth-service-return-9tmvzg | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|loadgenerator|ts-delivery-service|ts-verification-code-service|ts-preserve-service | return | ts-auth-service |
| ts3-ts-basic-service-response-replace-body-6lk5wq | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-train-service|loadgenerator|ts-price-service|ts-contacts-service | response-replace-body | ts-basic-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-preserve-service|ts-consign-service|loadgenerator|ts-contacts-service | pod-failure | ts-consign-price-service |
| ts3-ts-inside-payment-service-stress-tj2rtz | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-auth-service|loadgenerator|ts-user-service|ts-train-food-service | stress | ts-inside-payment-service |
| ts3-ts-travel-service-return-p696jn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-consign-price-service|loadgenerator|ts-assurance-service|ts-consign-service | return | ts-travel-service |
| ts4-ts-config-service-stress-wfgt8h | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-cancel-service|ts-assurance-service|ts-inside-payment-service|ts-voucher-service | stress | ts-config-service |
| ts4-ts-inside-payment-service-stress-gc2kcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|loadgenerator|ts-payment-service|ts-cancel-service|ts-station-food-service | stress | ts-inside-payment-service |
| ts4-ts-travel-service-stress-fz5lbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|loadgenerator|rabbitmq|ts-travel-plan-service|ts-assurance-service | stress | ts-travel-service |
| ts5-ts-inside-payment-service-stress-tbb7h6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|loadgenerator|ts-payment-service|ts-cancel-service|mysql | stress | ts-inside-payment-service |
| ts5-ts-travel-service-stress-p5h56b | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|loadgenerator|ts-inside-payment-service|ts-assurance-service|ts-travel2-service | stress | ts-travel-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-payment-service|ts-consign-service | pod-failure | ts-route-plan-service |
| ts9-ts-travel2-service-request-replace-path-nbzx5n | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|loadgenerator|ts-travel-plan-service|ts-consign-service|ts-inside-payment-service | request-replace-path | ts-travel2-service |
| ts1-ts-basic-service-request-replace-method-v627xx | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|loadgenerator|ts-train-food-service|ts-station-service|ts-user-service | request-replace-method | ts-basic-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | improved_to_hit1 | 3 | 1 | 2.0 | ts-station-food-service | ts-station-food-service|ts-user-service|ts-travel-service|ts-order-other-service|ts-price-service | pod-failure | ts-station-food-service |
| ts2-ts-basic-service-response-replace-code-qf2qml | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-assurance-service|ts-delivery-service|ts-route-service|ts-user-service | response-replace-code | ts-basic-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | improved_to_hit1 | 3 | 1 | 2.0 | ts-travel-service | ts-travel-service|ts-consign-service|ts-user-service|ts-order-service|loadgenerator | pod-failure | ts-travel-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | improved_to_hit1 | 3 | 1 | 2.0 | ts-payment-service | ts-payment-service|ts-assurance-service|ts-station-service|ts-price-service|ts-consign-service | pod-failure | ts-payment-service |
| ts3-ts-seat-service-response-replace-code-cfcfbf | improved_to_hit1 | 3 | 1 | 2.0 | ts-config-service;ts-seat-service | ts-config-service|loadgenerator|ts-user-service|ts-train-service|ts-inside-payment-service | response-replace-code | ts-seat-service |
| ts2-ts-order-other-service-container-kill-48rlds | improved_to_hit1 | 4 | 1 | 3.0 | ts-order-other-service | ts-order-other-service|loadgenerator|ts-preserve-service|ts-station-service|ts-inside-payment-service | container-kill | ts-order-other-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | improved_to_hit1 | 4 | 1 | 3.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-consign-price-service|loadgenerator|ts-consign-service|ts-security-service | response-replace-code | ts-travel-plan-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
