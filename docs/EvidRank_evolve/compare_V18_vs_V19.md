# EvidenceRank Compare V18 vs V19

- Created: 2026-06-02T22:31:32+08:00
- Old: `V18`
- New: `V19`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.506329 | 0.658931 | 0.152602 |
| AC@3 | 0.833333 | 0.877637 | 0.044304 |
| AC@5 | 0.941632 | 0.927567 | -0.014065 |
| MRR | 0.684853 | 0.776972 | 0.092119 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 393 |
| rank_improved | 110 |
| rank_regressed | 124 |
| regressed_from_hit1 | 176 |
| unchanged | 619 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-loss-k9xrkf | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-price-service|ts-user-service|ts-preserve-service|loadgenerator | loss | mysql |
| ts0-mysql-partition-cfvlsw | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|loadgenerator|ts-ui-dashboard | partition | mysql |
| ts0-ts-basic-service-response-abort-c4gjrt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-train-service|ts-price-service|ts-station-service|ts-consign-price-service | response-abort | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-hl8qdr | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-route-service|ts-price-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-v9z47n | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-train-service|ts-price-service | response-replace-code | ts-basic-service |
| ts0-ts-order-other-service-stress-4d76fr | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-security-service|ts-execute-service|ts-seat-service|ts-route-plan-service | stress | ts-order-other-service |
| ts0-ts-preserve-service-response-abort-7gp2mq | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-contacts-service|ts-price-service|ts-basic-service|ts-station-service | response-abort | ts-preserve-service |
| ts0-ts-preserve-service-response-abort-mj9pbn | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-basic-service|ts-contacts-service|ts-ui-dashboard|ts-station-service | response-abort | ts-preserve-service |
| ts0-ts-route-plan-service-request-abort-x2bhww | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ticket-office-service|ts-train-service|ts-train-food-service | request-abort | ts-route-plan-service |
| ts0-ts-route-plan-service-request-replace-method-lrzhl6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-seat-service|loadgenerator|ts-ui-dashboard | request-replace-method | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-body-xqldsl | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-price-service|ts-basic-service | response-replace-body | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-lpnvvp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-ticket-office-service|ts-ui-dashboard | response-replace-code | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-nsmpv4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-ui-dashboard|ts-payment-service | response-replace-code | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-vh2bnx | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel2-service|ts-station-service|ts-price-service|ts-train-service | response-replace-code | ts-route-plan-service |
| ts0-ts-route-service-container-kill-tsqgmn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service | ts-route-service|ts-payment-service|loadgenerator|ts-ui-dashboard|ts-contacts-service | container-kill | ts-route-service |
| ts0-ts-seat-service-response-delay-fjqtmh | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-preserve-service | response-delay | ts-seat-service |
| ts0-ts-security-service-response-replace-code-fbsfls | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|ts-order-other-service|ts-ui-dashboard | response-replace-code | ts-security-service |
| ts0-ts-travel-plan-service-request-replace-path-dnlz4g | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-travel-service|loadgenerator|ts-consign-service | request-replace-path | ts-travel-plan-service |
| ts0-ts-travel-plan-service-response-replace-body-mns47j | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-travel2-service|ts-train-service|ts-route-plan-service|ts-order-service | response-replace-body | ts-travel-plan-service |
| ts0-ts-travel-service-request-abort-6nm66v | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-food-service|ts-train-food-service|ts-travel-plan-service | request-abort | ts-travel-service |
| ts0-ts-travel2-service-request-replace-method-dhgqc8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-travel2-service |
| ts0-ts-ui-dashboard-request-replace-method-2lnwn5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-verification-code-service | ts-verification-code-service|loadgenerator|ts-news-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-delay-nqtssr | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-consign-service|ts-basic-service | response-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-sfz5t9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-travel-plan-service|ts-basic-service|ts-order-service|ts-route-plan-service|ts-travel-service | response-replace-code | ts-ui-dashboard |
| ts0-ts-user-service-partition-77jfkk | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-user-service | ts-user-service|loadgenerator|ts-ui-dashboard|ts-voucher-service|ts-auth-service | partition | ts-user-service |
| ts0-ts-user-service-stress-mww4jr | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-cancel-service|ts-ui-dashboard|ts-preserve-service|loadgenerator | stress | ts-user-service |
| ts1-ts-auth-service-request-replace-method-mqrzv4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-verification-code-service|ts-ui-dashboard|loadgenerator|ts-basic-service | request-replace-method | ts-auth-service |
| ts1-ts-auth-service-request-replace-method-mrrl9f | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-verification-code-service|loadgenerator|ts-ui-dashboard|ts-order-service | request-replace-method | ts-auth-service |
| ts1-ts-basic-service-request-replace-method-2dz98x | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-station-service|ts-price-service|ts-travel2-service|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts1-ts-food-service-request-replace-method-rq29d8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-station-food-service|ts-travel-service|ts-train-food-service|ts-ui-dashboard | request-replace-method | ts-food-service |
| ts1-ts-order-service-exception-b25hld | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|loadgenerator|ts-ui-dashboard|ts-assurance-service|ts-travel-service | exception | ts-order-service |
| ts1-ts-preserve-service-request-abort-x7w9vv | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-contacts-service|ts-security-service|ts-order-other-service|loadgenerator | request-abort | ts-preserve-service |
| ts1-ts-preserve-service-request-replace-method-9m4wvr | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|loadgenerator|ts-voucher-service|ts-ui-dashboard|ts-gateway-service | request-replace-method | ts-preserve-service |
| ts1-ts-preserve-service-response-abort-fxjfws | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-contacts-service|ts-security-service|ts-order-service|ts-voucher-service | response-abort | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-method-bn6rxm | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|loadgenerator|ts-station-food-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-request-replace-method-hv2klv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-route-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-request-replace-path-8b97qc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|loadgenerator|ts-route-service|ts-travel-service | request-replace-path | ts-route-plan-service |
| ts1-ts-route-plan-service-response-abort-5l599d | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-travel-service|ts-ui-dashboard | response-abort | ts-route-plan-service |
| ts1-ts-security-service-response-replace-code-q2nwzg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-order-service|loadgenerator|ts-travel-service | response-replace-code | ts-security-service |
| ts1-ts-station-food-service-stress-zvn4hb | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-food-service | ts-station-food-service|ts-food-service|loadgenerator|ts-cancel-service|ts-ui-dashboard | stress | ts-station-food-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
