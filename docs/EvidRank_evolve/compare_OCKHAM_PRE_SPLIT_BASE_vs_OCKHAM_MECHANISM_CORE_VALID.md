# EvidenceRank Compare OCKHAM_PRE_SPLIT_BASE vs OCKHAM_MECHANISM_CORE_AS_CREST

- Created: 2026-06-14T21:01:17+08:00
- Old: `OCKHAM_PRE_SPLIT_BASE`
- New: `OCKHAM_MECHANISM_CORE_AS_CREST`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.754571 | -0.045710 |
| AC@3 | 0.944444 | 0.939522 | -0.004923 |
| AC@5 | 0.971871 | 0.973277 | 0.001406 |
| MRR | 0.875326 | 0.847589 | -0.027737 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 65 |
| rank_improved | 49 |
| rank_regressed | 64 |
| regressed_from_hit1 | 130 |
| unchanged | 1114 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-station-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-r727qm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-station-service|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-station-service-loss-hs8vrm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-travel-plan-service|ts-travel2-service | loss | ts-station-service |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-station-service|ts-price-service|ts-preserve-service | request-replace-method | ts-basic-service |
| ts1-ts-preserve-service-request-abort-x7w9vv | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-security-service|ts-contacts-service|ts-ui-dashboard|ts-order-other-service | request-abort | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-train-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-body-5s6gc9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-route-service|ts-travel-service | response-replace-body | ts-route-plan-service |
| ts1-ts-seat-service-request-replace-path-jmcntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-order-other-service|ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | request-replace-path | ts-seat-service |
| ts1-ts-travel-plan-service-response-replace-code-6mlrxc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-inside-payment-service|ts-travel-service|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts1-ts-ui-dashboard-response-replace-code-prqgf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|ts-order-service|ts-travel-service|ts-assurance-service|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts2-mysql-corrupt-lt5n6d | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-ui-dashboard|ts-auth-service|ts-preserve-service|ts-basic-service | corrupt | mysql |
| ts2-ts-basic-service-request-replace-method-v6gzn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-station-service|ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts2-ts-basic-service-request-replace-path-flkd7v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-price-service|ts-basic-service|ts-travel2-service|ts-station-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts2-ts-consign-price-service-stress-7r95bt | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-ui-dashboard|ts-auth-service|ts-verification-code-service | stress | ts-consign-price-service |
| ts2-ts-route-plan-service-response-replace-body-dghfbk | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-basic-service|ts-ui-dashboard | response-replace-body | ts-route-plan-service |
| ts2-ts-security-service-request-replace-method-vdvkxf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-auth-service|ts-assurance-service|ts-travel2-service | request-replace-method | ts-security-service |
| ts2-ts-security-service-response-replace-code-zvh8k2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-food-service | response-replace-code | ts-security-service |
| ts2-ts-travel-service-request-delay-5hk27g | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-food-service|ts-order-service|ts-basic-service|ts-seat-service | request-delay | ts-travel-service |
| ts2-ts-travel-service-response-abort-jd66zv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-route-service|ts-seat-service | response-abort | ts-travel-service |
| ts2-ts-travel2-service-response-replace-code-ttpn92 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-price-service|ts-travel-plan-service|ts-station-service | response-replace-code | ts-travel2-service |
| ts3-ts-basic-service-request-replace-method-pjwm42 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-station-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-bvqv9z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-travel-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-route-plan-service-request-replace-path-m56fgf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-verification-code-service|ts-basic-service | request-replace-path | ts-route-plan-service |
| ts3-ts-travel-service-request-replace-path-vktk7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service | request-replace-path | ts-travel-service |
| ts3-ts-ui-dashboard-request-replace-method-rp5xrr | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-verification-code-service|ts-user-service | request-replace-method | ts-ui-dashboard |
| ts3-ts-ui-dashboard-response-abort-zd59tz | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-assurance-service|loadgenerator|ts-order-service|ts-ui-dashboard|ts-order-other-service | response-abort | ts-ui-dashboard |
| ts4-ts-basic-service-request-abort-jr6f2j | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-seat-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts4-ts-basic-service-response-abort-94gfnl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-route-plan-service|ts-preserve-service|ts-travel-service|ts-travel-plan-service | response-abort | ts-basic-service |
| ts4-ts-consign-service-partition-ncb5l8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-payment-service|ts-travel2-service|ts-order-other-service | partition | ts-consign-service |
| ts4-ts-inside-payment-service-stress-gc2kcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-payment-service|ts-ui-dashboard|ts-consign-service|loadgenerator | stress | ts-inside-payment-service |
| ts4-ts-order-service-bandwidth-kqnvn7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-auth-service|ts-food-service|ts-preserve-service|ts-verification-code-service | bandwidth | ts-order-service |
| ts4-ts-route-plan-service-request-delay-6kgcnn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-consign-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard | request-delay | ts-route-plan-service |
| ts4-ts-route-service-partition-xw4bwj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-station-service|ts-travel-service|ts-order-service|ts-order-other-service | partition | ts-route-service |
| ts4-ts-seat-service-delay-ddn72q | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|loadgenerator|ts-ui-dashboard|ts-consign-service|ts-seat-service | delay | ts-seat-service |
| ts4-ts-train-service-corrupt-vm6cjh | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-cancel-service|ts-auth-service|ts-order-other-service | corrupt | ts-train-service |
| ts4-ts-travel-service-partition-xq25fj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-auth-service | partition | ts-travel-service |
| ts4-ts-travel-service-request-replace-method-s2wfxf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-consign-service|ts-route-plan-service|ts-order-service | request-replace-method | ts-travel-service |
| ts4-ts-travel-service-response-delay-d9w5bf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-food-service|ts-travel-plan-service|ts-basic-service | response-delay | ts-travel-service |
| ts4-ts-ui-dashboard-loss-gvqmxw | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-assurance-service|ts-auth-service|ts-preserve-service | loss | ts-ui-dashboard |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
