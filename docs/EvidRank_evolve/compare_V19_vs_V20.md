# EvidenceRank Compare V19 vs V20

- Created: 2026-06-02T23:39:26+08:00
- Old: `V19`
- New: `V20`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.658931 | 0.789030 | 0.130098 |
| AC@3 | 0.877637 | 0.940225 | 0.062588 |
| AC@5 | 0.927567 | 0.976793 | 0.049226 |
| MRR | 0.776972 | 0.869097 | 0.092124 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 267 |
| rank_improved | 97 |
| rank_regressed | 47 |
| regressed_from_hit1 | 82 |
| unchanged | 929 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-order-other-service-corrupt-wkdp68 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-travel-plan-service | corrupt | ts-order-other-service |
| ts0-ts-order-service-exception-hdgpgm | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service | exception | ts-order-service |
| ts0-ts-seat-service-request-replace-method-dchngw | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-seat-service |
| ts0-ts-seat-service-response-delay-s2jg62 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-inside-payment-service|ts-travel-service|ts-travel2-service | response-delay | ts-seat-service |
| ts0-ts-security-service-request-replace-method-m5g977 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-basic-service | request-replace-method | ts-security-service |
| ts0-ts-travel-service-mysql-28wmss | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-consign-service|ts-consign-price-service|ts-food-service|ts-assurance-service | unknown | unknown |
| ts0-ts-travel-service-request-abort-g9mc2t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | request-abort | ts-travel-service |
| ts0-ts-travel-service-request-delay-z8wzcp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-train-food-service|ts-food-service|ts-basic-service|ts-travel2-service | request-delay | ts-travel-service |
| ts0-ts-travel2-service-request-delay-lzpl9v | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-consign-service|ts-travel-plan-service|ts-travel-service | request-delay | ts-travel2-service |
| ts0-ts-ui-dashboard-request-delay-s2z79x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-basic-service|ts-auth-service | request-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-delay-n5c9hs | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-service|ts-travel-service|ts-contacts-service | response-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-m8st7d | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-inside-payment-service|loadgenerator|ts-payment-service|ts-consign-service | response-replace-code | ts-ui-dashboard |
| ts1-mysql-corrupt-hft465 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|loadgenerator|ts-ui-dashboard|ts-order-service|ts-auth-service | corrupt | mysql |
| ts1-ts-basic-service-request-delay-4tqskz | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-preserve-service|ts-travel-plan-service | request-delay | ts-basic-service |
| ts1-ts-config-service-latency-5kkcrc | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-consign-service|ts-ui-dashboard|ts-basic-service|ts-seat-service | unknown | unknown |
| ts1-ts-food-service-stress-cm6h5v | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-consign-service|ts-inside-payment-service|ts-ui-dashboard|ts-travel-service | stress | ts-food-service |
| ts1-ts-order-service-exception-m9vqmq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-consign-service|ts-ui-dashboard|loadgenerator|ts-basic-service | exception | ts-order-service |
| ts1-ts-payment-service-stress-5778hg | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|ts-basic-service|loadgenerator | stress | ts-payment-service |
| ts1-ts-route-plan-service-request-abort-ghmj47 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-travel-service|ts-travel2-service|ts-route-service|ts-basic-service|ts-travel-plan-service | request-abort | ts-route-plan-service |
| ts1-ts-seat-service-request-delay-7dtgj8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-travel-plan-service|ts-basic-service | request-delay | ts-seat-service |
| ts1-ts-seat-service-response-delay-28bqw8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-basic-service|loadgenerator|ts-travel-plan-service | response-delay | ts-seat-service |
| ts1-ts-travel-service-response-replace-body-vzcxrp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-preserve-service | response-replace-body | ts-travel-service |
| ts1-ts-travel-service-return-zbss2p | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-consign-service|ts-ui-dashboard|ts-order-service|ts-basic-service | return | ts-travel-service |
| ts1-ts-travel-service-stress-9rhgns | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-order-service|ts-ui-dashboard | stress | ts-travel-service |
| ts1-ts-travel2-service-request-replace-method-qrl8t2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-travel-service | request-replace-method | ts-travel2-service |
| ts1-ts-travel2-service-response-replace-body-wsbwjq | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service|ts-basic-service | response-replace-body | ts-travel2-service |
| ts1-ts-ui-dashboard-request-delay-4h5kzs | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-other-service|ts-seat-service|ts-order-service | request-delay | ts-ui-dashboard |
| ts1-ts-ui-dashboard-request-replace-method-ntbf6g | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-service|ts-order-other-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-pkkx65 | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-consign-price-service|ts-basic-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-prqgf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|ts-assurance-service|loadgenerator|ts-order-service|ts-travel-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-xstkwf | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-travel-service|ts-seat-service|ts-auth-service | response-replace-code | ts-ui-dashboard |
| ts2-mysql-delay-d427wn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-travel-service | delay | mysql |
| ts2-ts-basic-service-response-delay-8d8blx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-preserve-service|ts-seat-service | response-delay | ts-basic-service |
| ts2-ts-order-service-stress-8vtw2p | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | stress | ts-order-service |
| ts2-ts-order-service-stress-967z6d | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service | stress | ts-order-service |
| ts2-ts-route-plan-service-request-replace-method-dq56rf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-travel2-service | request-replace-method | ts-route-plan-service |
| ts2-ts-route-plan-service-return-xw84fv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-consign-service|ts-station-food-service|ts-ui-dashboard|ts-payment-service | return | ts-route-plan-service |
| ts2-ts-train-service-stress-qv9rrc | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service | ts-train-service|ts-basic-service|ts-travel-plan-service|ts-travel-service|ts-route-plan-service | stress | ts-train-service |
| ts2-ts-travel-service-delay-gbx5sb | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-ui-dashboard|ts-basic-service|ts-food-service|ts-travel-plan-service | delay | ts-travel-service |
| ts2-ts-travel-service-request-delay-5hk27g | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-food-service|ts-order-service|ts-route-plan-service|ts-seat-service | request-delay | ts-travel-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
