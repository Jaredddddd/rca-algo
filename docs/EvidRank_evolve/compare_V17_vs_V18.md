# EvidenceRank Compare V17 vs V18

- Created: 2026-06-02T21:15:32+08:00
- Old: `V17`
- New: `V18`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.563291 | 0.506329 | -0.056962 |
| AC@3 | 0.868495 | 0.833333 | -0.035162 |
| AC@5 | 0.939522 | 0.941632 | 0.002110 |
| MRR | 0.724849 | 0.684853 | -0.039996 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 131 |
| rank_improved | 124 |
| rank_regressed | 181 |
| regressed_from_hit1 | 212 |
| unchanged | 774 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-partition-mphlhs | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-security-service | ts-security-service|ts-preserve-service|ts-voucher-service|ts-ui-dashboard|loadgenerator | partition | mysql |
| ts0-ts-basic-service-request-replace-method-88h72r | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-price-service|ts-station-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-delay-cg24jn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-ui-dashboard|ts-travel2-service|ts-travel-service | response-delay | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-5djll8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-price-service|ts-station-service | response-replace-code | ts-basic-service |
| ts0-ts-config-service-stress-g6rpl9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-consign-price-service|ts-seat-service|ts-verification-code-service|ts-food-service | stress | ts-config-service |
| ts0-ts-consign-price-service-stress-t67vtg | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-payment-service|ts-voucher-service|ts-travel-service | stress | ts-consign-price-service |
| ts0-ts-order-service-exception-hdgpgm | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service | exception | ts-order-service |
| ts0-ts-route-plan-service-exception-tcmvg6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-travel-service | exception | ts-route-plan-service |
| ts0-ts-seat-service-pod-failure-c87xdg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-travel2-service | pod-failure | ts-seat-service |
| ts0-ts-seat-service-request-replace-method-h4rcm9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-method | ts-seat-service |
| ts0-ts-travel-service-mysql-28wmss | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|rabbitmq|ts-consign-service|ts-consign-price-service|ts-ui-dashboard | unknown | unknown |
| ts0-ts-ui-dashboard-response-delay-rlz7sk | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-verification-code-service | ts-ui-dashboard|loadgenerator|ts-route-service|ts-basic-service|ts-order-service | response-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-delay-zd6lz6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|loadgenerator|ts-food-service|ts-verification-code-service|ts-seat-service | response-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-mlxmpf | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-service|ts-auth-service|ts-travel-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-auth-service-response-replace-code-xn6gk2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-order-service | response-replace-code | ts-auth-service |
| ts1-ts-config-service-latency-5kkcrc | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-consign-service|ts-ui-dashboard|ts-auth-service|ts-basic-service | unknown | unknown |
| ts1-ts-food-service-stress-cm6h5v | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-inside-payment-service|ts-payment-service|ts-consign-service|ts-ui-dashboard | stress | ts-food-service |
| ts1-ts-order-service-exception-m9vqmq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-voucher-service|ts-consign-service|ts-ui-dashboard|ts-auth-service | exception | ts-order-service |
| ts1-ts-payment-service-stress-5778hg | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|ts-consign-price-service|ts-basic-service | stress | ts-payment-service |
| ts1-ts-payment-service-stress-k7stf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-cancel-service|ts-ui-dashboard|ts-order-other-service | stress | ts-payment-service |
| ts1-ts-preserve-service-response-replace-body-6bfbmp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-price-service|ts-station-service|ts-basic-service | response-replace-body | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-p6bkb6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-travel2-service|ts-travel-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-request-replace-method-w9xvjp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel-service|ts-route-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-code-44s4p6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel-service|ts-travel2-service | response-replace-code | ts-route-plan-service |
| ts1-ts-security-service-request-replace-method-xv2ncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-delivery-service|ts-ui-dashboard|ts-order-service | request-replace-method | ts-security-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-food-service | ts-station-food-service|ts-food-service|ts-travel-service|ts-basic-service|ts-order-other-service | pod-failure | ts-station-food-service |
| ts1-ts-station-service-pod-failure-fn44tf | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-travel-service|ts-basic-service|ts-travel2-service|ts-route-plan-service | pod-failure | ts-station-service |
| ts1-ts-station-service-stress-jzbbjv | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-basic-service|ts-ui-dashboard|ts-travel2-service|ts-travel-service | stress | ts-station-service |
| ts1-ts-travel-service-exception-h5t4v2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | exception | ts-travel-service |
| ts1-ts-travel-service-stress-9rhgns | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-payment-service|ts-verification-code-service|ts-user-service | stress | ts-travel-service |
| ts1-ts-ui-dashboard-request-delay-d56qn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-user-service|ts-inside-payment-service|ts-security-service | request-delay | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-qc5tk4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|loadgenerator|ts-price-service|ts-seat-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts2-mysql-bandwidth-fws9rx | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|loadgenerator | bandwidth | mysql |
| ts2-ts-basic-service-response-delay-8d8blx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-contacts-service | response-delay | ts-basic-service |
| ts2-ts-food-service-response-delay-drcx9w | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-station-service|ts-basic-service | response-delay | ts-food-service |
| ts2-ts-route-plan-service-request-abort-rnjzzl | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-order-service|ts-seat-service|ts-order-other-service | request-abort | ts-route-plan-service |
| ts2-ts-route-plan-service-response-replace-code-q8jrhd | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-config-service|ts-basic-service | response-replace-code | ts-route-plan-service |
| ts2-ts-seat-service-container-kill-pt6tdw | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel2-service|ts-travel-service|ts-ui-dashboard | container-kill | ts-seat-service |
| ts2-ts-seat-service-request-delay-775n8q | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service | request-delay | ts-seat-service |
| ts2-ts-security-service-request-abort-55q6h2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-basic-service | request-abort | ts-security-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
