# EvidenceRank Compare V8 vs V9

- Created: 2026-06-02T10:22:36+08:00
- Old: `V8`
- New: `V9`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.788326 | 0.794655 | 0.006329 |
| AC@3 | 0.939522 | 0.941632 | 0.002110 |
| AC@5 | 0.973980 | 0.975387 | 0.001406 |
| MRR | 0.866904 | 0.871089 | 0.004185 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 25 |
| rank_improved | 43 |
| rank_regressed | 30 |
| regressed_from_hit1 | 16 |
| unchanged | 1308 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-partition-k9q6lq | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-basic-service|ts-travel-plan-service|ts-travel-service|ts-route-plan-service | partition | mysql |
| ts0-ts-basic-service-request-abort-bgq9qs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-route-service|ts-train-service | request-abort | ts-basic-service |
| ts0-ts-basic-service-request-replace-path-5888sf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-station-service|ts-route-plan-service | request-replace-path | ts-basic-service |
| ts0-ts-route-plan-service-request-replace-method-gl2rrc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service | request-replace-method | ts-route-plan-service |
| ts0-ts-ui-dashboard-request-replace-method-5dxswc | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-security-service|loadgenerator|ts-consign-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts1-mysql-bandwidth-s7srkn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | bandwidth | mysql |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-station-service|ts-preserve-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts1-ts-basic-service-response-replace-body-bt9qt4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-station-service|ts-travel-service|ts-price-service|ts-train-service | response-replace-body | ts-basic-service |
| ts1-ts-route-plan-service-request-abort-ghmj47 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-travel-service|ts-travel2-service|ts-route-service|ts-basic-service|ts-travel-plan-service | request-abort | ts-route-plan-service |
| ts1-ts-travel2-service-response-replace-body-wsbwjq | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-ui-dashboard | response-replace-body | ts-travel2-service |
| ts2-ts-basic-service-response-replace-body-4xzdq7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-price-service|ts-cancel-service | response-replace-body | ts-basic-service |
| ts2-ts-travel2-service-response-replace-code-tdtcrq | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-route-service|ts-travel-plan-service|ts-payment-service | response-replace-code | ts-travel2-service |
| ts3-ts-basic-service-response-replace-body-w5fj79 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-station-service|ts-route-service|ts-train-service | response-replace-body | ts-basic-service |
| ts3-ts-ui-dashboard-request-replace-method-wkh6t7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-order-service|ts-route-plan-service|ts-seat-service|ts-travel-plan-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-replace-code-kxp2f4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-service|ts-basic-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-order-other-service-loss-mvcrfm | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-payment-service|ts-preserve-service|ts-ui-dashboard|ts-basic-service | loss | ts-order-other-service |
| ts4-ts-route-plan-service-response-delay-vxcl8q | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-ui-dashboard|ts-payment-service|ts-travel-plan-service|ts-basic-service | response-delay | ts-route-plan-service |
| ts4-ts-ui-dashboard-response-replace-code-w7z7vm | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|ts-travel-service|ts-order-service|loadgenerator|ts-food-service | response-replace-code | ts-ui-dashboard |
| ts5-ts-ui-dashboard-request-replace-method-km4wzw | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-ui-dashboard | ts-preserve-service|ts-order-service|ts-ui-dashboard|loadgenerator|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-ui-dashboard-response-replace-code-dww7g8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-price-service|loadgenerator|ts-order-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts7-ts-ui-dashboard-request-replace-method-cgqxk7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-food-service|ts-basic-service|loadgenerator|ts-order-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts9-ts-ui-dashboard-response-replace-code-92vp2k | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-price-service|loadgenerator|ts-payment-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts0-mysql-partition-cfvlsw | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-basic-service | partition | mysql |
| ts2-ts-basic-service-response-replace-code-kd7f9n | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-preserve-service|ts-station-service | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-response-replace-code-fjll2p | improved_to_hit1 | 3 | 1 | 2.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-basic-service|ts-seat-service|ts-travel-service|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts0-ts-basic-service-request-replace-method-gqn7nd | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-station-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-replace-body-85cnwx | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-basic-service|ts-station-service|ts-train-service|ts-route-plan-service | response-replace-body | ts-basic-service |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | rank_improved | 3 | 2 | 1.0 | ts-order-service;ts-ui-dashboard | ts-cancel-service|ts-ui-dashboard|loadgenerator|ts-consign-price-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-food-service-response-patch-body-qjhx5h | rank_improved | 13 | 12 | 1.0 | ts-food-service;ts-train-food-service | ts-consign-service|ts-verification-code-service|ts-payment-service|ts-travel-service|ts-seat-service | unknown | unknown |
| ts2-ts-basic-service-response-replace-body-hk6w9p | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-station-service|ts-basic-service|ts-travel2-service|ts-price-service|ts-train-service | response-replace-body | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-qf2qml | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-travel-service|ts-basic-service|ts-preserve-service|ts-station-service|ts-price-service | response-replace-code | ts-basic-service |
| ts2-ts-consign-price-service-stress-7r95bt | rank_improved | 5 | 4 | 1.0 | ts-consign-price-service | ts-payment-service|ts-consign-service|ts-preserve-service|ts-consign-price-service|ts-security-service | stress | ts-consign-price-service |
| ts2-ts-ui-dashboard-request-replace-method-k4pkfg | rank_improved | 3 | 2 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-inside-payment-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-basic-service-response-replace-code-ws6vpb | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-preserve-service|ts-travel2-service|ts-station-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-zn4kzg | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-travel2-service|ts-basic-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-ui-dashboard-request-replace-method-7lstrz | rank_improved | 4 | 3 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-basic-service|loadgenerator|ts-ui-dashboard|ts-order-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-hh8qpt | rank_improved | 3 | 2 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-cancel-service|ts-ui-dashboard|ts-order-service|loadgenerator|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-replace-method-pgl9hb | rank_improved | 4 | 3 | 1.0 | ts-contacts-service;ts-ui-dashboard | loadgenerator|ts-station-service|ts-ui-dashboard|ts-basic-service|ts-contacts-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jrv8dx | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-price-service | ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-basic-service|ts-auth-service | response-replace-body | ts-basic-service |
| ts4-ts-basic-service-response-replace-body-wpxp9b | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-station-service | ts-preserve-service|ts-ui-dashboard|ts-route-plan-service|ts-basic-service|ts-travel-service | response-replace-body | ts-basic-service |

## Decision Notes

- Accept V9 with caution. All headline metrics improve: `AC@1 +0.006329`, `MRR +0.004185`, `AC@3 +0.002110`, and `AC@5 +0.001406`.
- The accepted mechanism is a post-gate endpoint compensation: V8 still discounts unsupported endpoint drift, while V9 lets endpoint evidence that survives that gate compete with broad metric/duration/row-count propagation.
- `25` cases improve to Hit@1 versus `16` regress from Hit@1. Improvements concentrate in request/response shape cases, especially `request-replace-method` and `response-replace-code` around UI/basic-service paths.
- Regression risk remains in `pod-failure`: the weak group falls to `AC@1=0.125000` and top5 misses rise to `7`. Do not further increase endpoint weight; the next iteration should target availability/topology-drop evidence separately.
