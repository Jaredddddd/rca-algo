# EvidenceRank Compare OCKHAM_PRE_SPLIT_BASE vs OCKHAM_PROTOCOL_CORE_AS_CREST

- Created: 2026-06-14T21:02:25+08:00
- Old: `OCKHAM_PRE_SPLIT_BASE`
- New: `OCKHAM_PROTOCOL_CORE_AS_CREST`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.483826 | -0.316456 |
| AC@3 | 0.944444 | 0.757384 | -0.187060 |
| AC@5 | 0.971871 | 0.857947 | -0.113924 |
| MRR | 0.875326 | 0.641656 | -0.233669 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 72 |
| rank_improved | 45 |
| rank_regressed | 105 |
| regressed_from_hit1 | 522 |
| unchanged | 678 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-station-service|ts-preserve-service|ts-price-service|ts-travel-service | request-replace-method | ts-basic-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-order-service|ts-travel-service|ts-travel-plan-service|ts-order-other-service | response-replace-code | ts-seat-service |
| ts0-ts-station-service-loss-hs8vrm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-route-plan-service|ts-travel-plan-service|ts-travel-service | loss | ts-station-service |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-station-service|ts-price-service|ts-travel-service|ts-route-service | request-replace-method | ts-basic-service |
| ts1-ts-preserve-service-request-abort-x7w9vv | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-security-service|ts-contacts-service|ts-auth-service|ts-ui-dashboard | request-abort | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-station-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-body-5s6gc9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-travel-service|ts-route-plan-service|ts-auth-service | response-replace-body | ts-route-plan-service |
| ts1-ts-seat-service-request-replace-path-jmcntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-order-other-service|ts-seat-service|loadgenerator|ts-travel2-service|ts-travel-plan-service | request-replace-path | ts-seat-service |
| ts1-ts-seat-service-response-replace-body-hvd8x2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-order-service | response-replace-body | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-order-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-seat-service |
| ts1-ts-travel-plan-service-response-replace-code-6mlrxc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-travel-service|ts-travel2-service|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-travel-service-response-replace-code-qzmhjf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-basic-service|ts-station-service|ts-travel-plan-service | response-replace-code | ts-travel-service |
| ts1-ts-ui-dashboard-request-abort-sksx9s | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-inside-payment-service|ts-consign-service|ts-auth-service | request-abort | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-prqgf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-food-service|ts-inside-payment-service|ts-consign-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-basic-service-request-replace-path-flkd7v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-price-service|ts-basic-service|ts-station-service|ts-travel2-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-station-service|ts-travel2-service|ts-travel-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts2-ts-consign-price-service-stress-7r95bt | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-ui-dashboard|ts-travel2-service|ts-auth-service | stress | ts-consign-price-service |
| ts2-ts-route-plan-service-response-replace-body-dghfbk | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-travel-service | response-replace-body | ts-route-plan-service |
| ts2-ts-security-service-request-replace-method-vdvkxf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-assurance-service|ts-auth-service|ts-travel2-service | request-replace-method | ts-security-service |
| ts2-ts-security-service-response-replace-code-zvh8k2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-inside-payment-service|ts-order-service|ts-ui-dashboard | response-replace-code | ts-security-service |
| ts2-ts-travel-service-request-replace-method-5snzk5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-basic-service|ts-food-service|ts-seat-service|ts-order-service | request-replace-method | ts-travel-service |
| ts2-ts-travel-service-response-abort-jd66zv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-route-service|ts-travel-plan-service | response-abort | ts-travel-service |
| ts2-ts-travel2-service-response-replace-code-ttpn92 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-train-service|ts-route-service|ts-route-plan-service|ts-ui-dashboard | response-replace-code | ts-travel2-service |
| ts2-ts-ui-dashboard-request-abort-djrhxq | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-order-other-service|ts-travel-plan-service | request-abort | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-abort-rcfl6z | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-travel-service|ts-basic-service|ts-ui-dashboard|loadgenerator|ts-consign-service | response-abort | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-bzfxkt | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-consign-service|ts-cancel-service|ts-assurance-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-basic-service-response-replace-body-6lk5wq | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-price-service|ts-train-service | response-replace-body | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-bvqv9z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-station-service|ts-travel2-service|ts-travel-service|ts-price-service | response-replace-code | ts-basic-service |
| ts3-ts-route-plan-service-request-replace-path-m56fgf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-service|ts-basic-service|ts-travel-plan-service|ts-price-service | request-replace-path | ts-route-plan-service |
| ts3-ts-seat-service-response-replace-code-xdw4c7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-route-plan-service|ts-basic-service | response-replace-code | ts-seat-service |
| ts3-ts-travel-service-request-replace-path-vktk7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-basic-service|ts-food-service|ts-ui-dashboard|loadgenerator | request-replace-path | ts-travel-service |
| ts3-ts-ui-dashboard-response-abort-zd59tz | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-assurance-service|ts-order-service|ts-ui-dashboard|ts-preserve-service|ts-travel-plan-service | response-abort | ts-ui-dashboard |
| ts4-ts-inside-payment-service-stress-gc2kcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-cancel-service|ts-consign-service|ts-ui-dashboard|loadgenerator | stress | ts-inside-payment-service |
| ts4-ts-order-service-bandwidth-kqnvn7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|ts-assurance-service|ts-food-service|ts-order-service | bandwidth | ts-order-service |
| ts4-ts-route-plan-service-response-replace-code-7d5bnz | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard|ts-order-other-service | response-replace-code | ts-route-plan-service |
| ts4-ts-route-service-partition-xw4bwj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-order-service|ts-order-other-service|ts-travel2-service | partition | ts-route-service |
| ts4-ts-travel-service-request-replace-method-s2wfxf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-order-service|ts-basic-service | request-replace-method | ts-travel-service |
| ts4-ts-ui-dashboard-response-replace-code-5s6j28 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-inside-payment-service|ts-preserve-service|ts-food-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-ui-dashboard-response-replace-code-wdt6z5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|loadgenerator|ts-assurance-service|ts-consign-price-service | response-replace-code | ts-ui-dashboard |
| ts5-ts-food-service-response-replace-code-bgr2hd | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-ui-dashboard|ts-consign-service|loadgenerator|ts-travel-service | response-replace-code | ts-food-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
