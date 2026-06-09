# EvidenceRank Compare CREST_AIOPS1_BASE_RCABENCH vs CREST_AIOPS1_RCABENCH_REJECTED

- Created: 2026-06-08T20:40:07+08:00
- Old: `CREST_AIOPS1_BASE_RCABENCH`
- New: `CREST_AIOPS1_RCABENCH_REJECTED`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.793952 | -0.006329 |
| AC@3 | 0.944444 | 0.945148 | 0.000703 |
| AC@5 | 0.971871 | 0.971871 | 0.000000 |
| MRR | 0.875326 | 0.872228 | -0.003098 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 2 |
| rank_improved | 8 |
| rank_regressed | 4 |
| regressed_from_hit1 | 11 |
| unchanged | 1397 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-travel-service-request-abort-g9mc2t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-voucher-service|ts-route-plan-service|ts-delivery-service|ts-travel-plan-service | request-abort | ts-travel-service |
| ts2-ts-basic-service-request-replace-method-v6gzn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | rank_improved | 9 | 8 | 1.0 | ts-route-plan-service;ts-travel-service | ts-ui-dashboard|loadgenerator|ts-food-service|ts-seat-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts4-ts-seat-service-bandwidth-k2bwt2 | rank_improved | 3 | 2 | 1.0 | ts-config-service;ts-seat-service | ts-travel-plan-service|ts-seat-service|ts-route-plan-service|ts-ui-dashboard|ts-travel2-service | bandwidth | ts-seat-service |
| ts4-ts-station-service-bandwidth-nfljv5 | rank_improved | 17 | 16 | 1.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-ui-dashboard | bandwidth | ts-station-service |
| ts7-mysql-loss-dxzvbj | rank_improved | 3 | 2 | 1.0 | mysql;ts-user-service | ts-ui-dashboard|ts-user-service|loadgenerator|ts-travel-service|ts-voucher-service | loss | mysql |
| ts2-mysql-pod-kill-xvzmxb | rank_improved | 15 | 8 | 7.0 | mysql | ts-order-service|ts-auth-service|ts-travel-service|ts-security-service|ts-preserve-service | unknown | unknown |
| ts3-ts-consign-service-pod-failure-8cb7mp | rank_improved | 17 | 10 | 7.0 | ts-consign-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-food-service|ts-seat-service | pod-failure | ts-consign-service |
| ts5-ts-cancel-service-stress-d8xbsn | rank_improved | 20 | 12 | 8.0 | ts-cancel-service | ts-consign-service|ts-food-service|ts-basic-service|ts-route-plan-service|ts-station-service | stress | ts-cancel-service |
| ts0-mysql-container-kill-9t6n24 | rank_improved | 15 | 3 | 12.0 | mysql | ts-train-service|ts-auth-service|mysql|ts-ui-dashboard|ts-verification-code-service | container-kill | mysql |
| ts5-ts-preserve-service-partition-kfrmzn | rank_regressed | 5 | 9 | -4.0 | ts-preserve-service;ts-ui-dashboard | ts-seat-service|ts-contacts-service|ts-order-service|ts-notification-service|ts-food-service | partition | ts-preserve-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | rank_regressed | 6 | 9 | -3.0 | ts-food-service;ts-ui-dashboard | ts-order-service|ts-seat-service|ts-consign-service|ts-contacts-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | rank_regressed | 9 | 10 | -1.0 | ts-basic-service;ts-price-service | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-travel2-service | response-replace-body | ts-basic-service |
| ts5-ts-contacts-service-loss-bdtvgn | rank_regressed | 2 | 3 | -1.0 | ts-contacts-service;ts-ui-dashboard | ts-travel2-service|ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-basic-service | loss | ts-contacts-service |
| ts4-mysql-partition-bbrxlg | regressed_from_hit1 | 1 | 3 | -2.0 | mysql;ts-auth-service | ts-notification-service|ts-delivery-service|ts-auth-service|ts-ui-dashboard|ts-order-other-service | partition | mysql |
| ts5-ts-price-service-corrupt-pdk7dj | regressed_from_hit1 | 1 | 3 | -2.0 | mysql;ts-price-service | ts-travel-plan-service|ts-voucher-service|ts-price-service|ts-ui-dashboard|ts-travel-service | corrupt | ts-price-service |
| ts0-ts-basic-service-request-replace-method-gqn7nd | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-station-service|ts-travel-plan-service | request-replace-method | ts-basic-service |
| ts3-ts-user-service-partition-vt7q2n | regressed_from_hit1 | 1 | 2 | -1.0 | mysql;ts-user-service | ts-verification-code-service|ts-user-service|ts-auth-service|ts-ui-dashboard|ts-food-service | partition | ts-user-service |
| ts4-ts-auth-service-corrupt-pldpdm | regressed_from_hit1 | 1 | 2 | -1.0 | ts-auth-service;ts-verification-code-service | ts-basic-service|ts-auth-service|ts-order-service|ts-ui-dashboard|ts-verification-code-service | corrupt | ts-auth-service |
| ts4-ts-basic-service-response-delay-slw7f4 | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-station-service | ts-seat-service|ts-basic-service|ts-route-plan-service|ts-travel-service|ts-preserve-service | response-delay | ts-basic-service |
| ts4-ts-order-other-service-loss-mvcrfm | regressed_from_hit1 | 1 | 2 | -1.0 | ts-order-other-service;ts-security-service | ts-preserve-service|ts-security-service|ts-consign-service|ts-food-service|ts-seat-service | loss | ts-order-other-service |
| ts5-ts-basic-service-response-replace-code-n7djz7 | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-route-service | ts-preserve-service|ts-basic-service|ts-route-plan-service|ts-seat-service|ts-travel-service | response-replace-code | ts-basic-service |
| ts5-ts-travel-service-bandwidth-vf7jtc | regressed_from_hit1 | 1 | 2 | -1.0 | mysql;ts-travel-service | ts-travel-plan-service|ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel2-service | bandwidth | ts-travel-service |
| ts6-ts-auth-service-partition-pk27vh | regressed_from_hit1 | 1 | 2 | -1.0 | mysql;ts-auth-service | ts-ui-dashboard|ts-auth-service|ts-route-service|ts-travel2-service|ts-payment-service | partition | ts-auth-service |
| ts7-ts-ui-dashboard-loss-sz9kk8 | regressed_from_hit1 | 1 | 2 | -1.0 | ts-assurance-service;ts-ui-dashboard | ts-preserve-service|ts-ui-dashboard|ts-food-service|ts-travel2-service|ts-basic-service | loss | ts-ui-dashboard |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
