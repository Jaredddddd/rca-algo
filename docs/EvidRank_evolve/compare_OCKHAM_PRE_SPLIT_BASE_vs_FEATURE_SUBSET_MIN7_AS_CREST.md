# EvidenceRank Compare OCKHAM_PRE_SPLIT_BASE vs FEATURE_SUBSET_MIN7_AS_CREST

- Created: 2026-06-14T23:10:53+08:00
- Old: `OCKHAM_PRE_SPLIT_BASE`
- New: `FEATURE_SUBSET_MIN7_AS_CREST`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.800281 | 0.000000 |
| AC@3 | 0.944444 | 0.946554 | 0.002110 |
| AC@5 | 0.971871 | 0.971167 | -0.000703 |
| MRR | 0.875326 | 0.877743 | 0.002418 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 107 |
| rank_improved | 59 |
| rank_regressed | 45 |
| regressed_from_hit1 | 107 |
| unchanged | 1104 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-route-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-r727qm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-station-service|ts-travel2-service|ts-route-service | response-replace-code | ts-basic-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-basic-service|ts-config-service | response-replace-code | ts-seat-service |
| ts0-ts-station-service-loss-hs8vrm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-service | loss | ts-station-service |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-price-service|ts-station-service|ts-route-service | request-replace-method | ts-basic-service |
| ts1-ts-order-service-exception-b25hld | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-assurance-service|ts-ui-dashboard|loadgenerator|ts-consign-service | exception | ts-order-service |
| ts1-ts-order-service-exception-m9vqmq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-consign-service|ts-ui-dashboard|ts-food-service|ts-route-service | exception | ts-order-service |
| ts1-ts-payment-service-stress-k7stf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-order-service|ts-route-service|ts-train-service | stress | ts-payment-service |
| ts1-ts-route-plan-service-request-replace-method-qtbhzt | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-train-service|ts-travel2-service|ts-travel-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-body-5s6gc9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-travel2-service|ts-travel-service | response-replace-body | ts-route-plan-service |
| ts1-ts-seat-service-request-replace-path-jmcntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-order-other-service|ts-inside-payment-service|ts-basic-service | request-replace-path | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-basic-service|ts-config-service | response-replace-code | ts-seat-service |
| ts1-ts-travel-service-response-replace-code-qzmhjf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-route-service|ts-basic-service|ts-train-service | response-replace-code | ts-travel-service |
| ts2-mysql-corrupt-lt5n6d | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-auth-service|ts-basic-service|ts-ui-dashboard|ts-station-service | corrupt | mysql |
| ts2-mysql-delay-d427wn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-verification-code-service | delay | mysql |
| ts2-ts-basic-service-request-replace-path-flkd7v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-price-service|ts-travel-service|ts-station-service | request-replace-path | ts-basic-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-station-service|ts-train-service | response-replace-code | ts-basic-service |
| ts2-ts-route-plan-service-request-replace-method-dq56rf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-station-service|ts-travel2-service | request-replace-method | ts-route-plan-service |
| ts2-ts-route-plan-service-response-replace-body-dghfbk | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-travel-service|ts-basic-service | response-replace-body | ts-route-plan-service |
| ts2-ts-seat-service-request-delay-775n8q | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|loadgenerator|ts-travel-plan-service|ts-ui-dashboard|ts-travel-service | request-delay | ts-seat-service |
| ts2-ts-security-service-request-replace-method-vdvkxf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-route-service|ts-basic-service | request-replace-method | ts-security-service |
| ts2-ts-security-service-response-replace-code-zvh8k2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-route-service|ts-food-service | response-replace-code | ts-security-service |
| ts2-ts-station-service-dns-nn49s2 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-consign-service|ts-seat-service|ts-order-service|ts-ui-dashboard | unknown | unknown |
| ts2-ts-travel-service-bandwidth-f9fkg7 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-order-service | bandwidth | ts-travel-service |
| ts2-ts-travel-service-request-replace-method-5snzk5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-station-service|ts-route-service|ts-basic-service | request-replace-method | ts-travel-service |
| ts2-ts-travel-service-response-abort-jd66zv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-contacts-service|ts-route-service|ts-route-plan-service | response-abort | ts-travel-service |
| ts3-mysql-corrupt-4kplqx | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-basic-service | corrupt | mysql |
| ts3-ts-basic-service-request-replace-method-pjwm42 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-station-service|ts-travel-service|ts-price-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-response-replace-body-6lk5wq | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-price-service|ts-train-service | response-replace-body | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-bvqv9z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service|ts-route-service | response-replace-code | ts-basic-service |
| ts3-ts-route-plan-service-request-replace-path-m56fgf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-verification-code-service|ts-basic-service | request-replace-path | ts-route-plan-service |
| ts3-ts-seat-service-request-replace-method-b56nqd | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-config-service | request-replace-method | ts-seat-service |
| ts3-ts-travel-service-request-replace-path-vktk7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-service|ts-route-plan-service|ts-basic-service | request-replace-path | ts-travel-service |
| ts3-ts-travel2-service-request-replace-method-ggdqhg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-seat-service|ts-route-service|ts-travel-plan-service | request-replace-method | ts-travel2-service |
| ts3-ts-ui-dashboard-request-replace-method-rp5xrr | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-user-service|ts-route-service|ts-order-other-service|ts-auth-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts4-mysql-corrupt-kgjmhg | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-travel-service | corrupt | mysql |
| ts4-ts-basic-service-request-abort-jr6f2j | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-price-service|ts-order-service | request-abort | ts-basic-service |
| ts4-ts-basic-service-response-abort-94gfnl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-order-service|ts-food-service | response-abort | ts-basic-service |
| ts4-ts-config-service-stress-wfgt8h | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-seat-service|ts-route-plan-service|ts-travel2-service|ts-travel-service | stress | ts-config-service |
| ts4-ts-inside-payment-service-stress-gc2kcm | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-payment-service|ts-food-service|ts-order-other-service|ts-ui-dashboard | stress | ts-inside-payment-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
