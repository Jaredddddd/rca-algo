# EvidenceRank Compare V6 vs V7

- Created: 2026-06-02T03:02:06+08:00
- Old: `V6`
- New: `V7`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.766526 | 0.781997 | 0.015471 |
| AC@3 | 0.922644 | 0.940928 | 0.018284 |
| AC@5 | 0.961322 | 0.978903 | 0.017581 |
| MRR | 0.849078 | 0.864359 | 0.015280 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 52 |
| rank_improved | 80 |
| rank_regressed | 37 |
| regressed_from_hit1 | 30 |
| unchanged | 1223 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-response-replace-body-2ntz4z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-price-service|ts-station-service | response-replace-body | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-4vn4gg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-price-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-consign-price-service-stress-t67vtg | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-payment-service|ts-travel-service|ts-basic-service | stress | ts-consign-price-service |
| ts0-ts-security-service-response-replace-code-47m5nd | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-order-other-service | response-replace-code | ts-security-service |
| ts0-ts-travel2-service-response-abort-bvl7cs | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-ui-dashboard | response-abort | ts-travel2-service |
| ts0-ts-ui-dashboard-request-replace-method-kpdcrm | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-travel-service|ts-auth-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-m8st7d | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-inside-payment-service|loadgenerator|ts-payment-service|ts-travel2-service | response-replace-code | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-mlxmpf | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-order-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-basic-service-request-replace-path-qbdgjj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-travel2-service|ts-route-plan-service | request-replace-path | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-ft59pl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-station-service|ts-price-service|ts-preserve-service | response-replace-code | ts-basic-service |
| ts1-ts-travel-service-response-replace-code-qzmhjf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-ui-dashboard | response-replace-code | ts-travel-service |
| ts1-ts-ui-dashboard-response-replace-code-b2g9ss | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-service|ts-travel-service|ts-basic-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-f8wvld | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-assurance-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-auth-service-response-replace-code-zb5np6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-voucher-service | response-replace-code | ts-auth-service |
| ts2-ts-train-service-loss-j2w694 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-basic-service|ts-travel-plan-service|ts-route-plan-service|ts-travel-service | loss | ts-train-service |
| ts2-ts-travel-service-response-abort-jd66zv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-ui-dashboard|ts-route-service | response-abort | ts-travel-service |
| ts2-ts-travel2-service-request-replace-method-x7fqwg | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service | request-replace-method | ts-travel2-service |
| ts2-ts-ui-dashboard-response-replace-code-478bgk | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|ts-contacts-service|loadgenerator|ts-seat-service|ts-route-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-mk44qn | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-travel-plan-service|ts-preserve-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-auth-service-response-replace-code-9cstpf | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-travel-service | response-replace-code | ts-auth-service |
| ts3-ts-basic-service-request-abort-hb7rsg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-route-plan-service|ts-travel-plan-service | request-abort | ts-basic-service |
| ts3-ts-basic-service-request-replace-path-r6c626 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-price-service|ts-station-service|ts-route-service | request-replace-path | ts-basic-service |
| ts3-ts-route-plan-service-response-replace-body-fzz87f | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-service|ts-route-plan-service|ts-ui-dashboard | response-replace-body | ts-route-plan-service |
| ts3-ts-train-service-partition-r58pxm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-basic-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | partition | ts-train-service |
| ts3-ts-travel-plan-service-response-replace-code-x6bzr8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-payment-service|ts-ui-dashboard|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts3-ts-travel-service-request-replace-path-vktk7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | request-replace-path | ts-travel-service |
| ts3-ts-ui-dashboard-response-abort-zd59tz | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-assurance-service|ts-order-service|loadgenerator|ts-ui-dashboard|ts-seat-service | response-abort | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-replace-code-5drrkc | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|ts-seat-service|ts-route-plan-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-ui-dashboard-partition-lvfxl6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|ts-travel-plan-service|ts-basic-service|ts-seat-service|loadgenerator | partition | ts-ui-dashboard |
| ts4-ts-ui-dashboard-request-delay-6b6bd5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|ts-order-service|ts-assurance-service|ts-travel-service | request-delay | ts-ui-dashboard |
| ts5-ts-food-service-response-replace-code-bgr2hd | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-order-service|ts-consign-service|ts-ui-dashboard|ts-basic-service | response-replace-code | ts-food-service |
| ts5-ts-route-plan-service-response-replace-code-fps9dk | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-payment-service|loadgenerator | response-replace-code | ts-route-plan-service |
| ts5-ts-travel-service-request-abort-jsgpm6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-order-service|ts-travel-plan-service|ts-basic-service | request-abort | ts-travel-service |
| ts5-ts-ui-dashboard-request-replace-method-km4wzw | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-ui-dashboard | ts-preserve-service|ts-order-service|ts-basic-service|ts-ui-dashboard|ts-food-service | request-replace-method | ts-ui-dashboard |
| ts6-ts-basic-service-corrupt-zg68ql | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | corrupt | ts-basic-service |
| ts6-ts-security-service-response-replace-code-nj74q4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-consign-service|ts-ui-dashboard|loadgenerator | response-replace-code | ts-security-service |
| ts6-ts-travel-plan-service-response-replace-code-xwj6fw | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard|ts-travel-service|ts-route-plan-service | response-replace-code | ts-travel-plan-service |
| ts7-ts-ui-dashboard-loss-sz9kk8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-ui-dashboard|ts-preserve-service|ts-travel2-service|ts-route-service|ts-route-plan-service | loss | ts-ui-dashboard |
| ts7-ts-ui-dashboard-response-replace-code-9rd4mj | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-service|ts-travel-service|ts-auth-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-basic-service-response-replace-code-pqkdss | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
