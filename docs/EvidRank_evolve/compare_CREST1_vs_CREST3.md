# EvidenceRank Compare CREST1 vs CREST3

- Created: 2026-06-06T03:49:22+08:00
- Old: `CREST1`
- New: `CREST3`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.699719 | 0.800281 | 0.100563 |
| AC@3 | 0.916315 | 0.945851 | 0.029536 |
| AC@5 | 0.952180 | 0.972574 | 0.020394 |
| MRR | 0.811469 | 0.875744 | 0.064274 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 188 |
| rank_improved | 83 |
| rank_regressed | 47 |
| regressed_from_hit1 | 45 |
| unchanged | 1059 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-mysql-partition-jh4jkt | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-travel-plan-service|ts-route-plan-service|ts-travel-service|ts-ui-dashboard | partition | mysql |
| ts0-ts-auth-service-stress-nlpsfx | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-consign-service|ts-preserve-service|ts-travel-plan-service | stress | ts-auth-service |
| ts0-ts-basic-service-response-replace-body-85cnwx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-station-service|ts-train-service | response-replace-body | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-4vn4gg | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-station-service|ts-price-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-5djll8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-price-service|ts-station-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-lq4ncj | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-travel-plan-service|ts-station-service | response-replace-code | ts-basic-service |
| ts0-ts-config-service-stress-g6rpl9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-consign-price-service|ts-seat-service|ts-basic-service|ts-food-service | stress | ts-config-service |
| ts0-ts-food-service-stress-xfwkgh | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|ts-preserve-service|ts-auth-service|ts-consign-service | stress | ts-food-service |
| ts0-ts-inside-payment-service-stress-5qd9rl | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-payment-service|ts-consign-service|ts-auth-service | stress | ts-inside-payment-service |
| ts0-ts-order-other-service-corrupt-wkdp68 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-ui-dashboard|ts-seat-service|ts-preserve-service|ts-travel-plan-service | corrupt | ts-order-other-service |
| ts0-ts-order-service-exception-hdgpgm | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-security-service|ts-preserve-service|ts-food-service|ts-auth-service | exception | ts-order-service |
| ts0-ts-order-service-stress-cklk2p | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-travel-service|ts-consign-service|ts-food-service | stress | ts-order-service |
| ts0-ts-order-service-stress-rb76lq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-consign-service|ts-travel-service|ts-ui-dashboard | stress | ts-order-service |
| ts0-ts-order-service-stress-xt9wfq | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-preserve-service | stress | ts-order-service |
| ts0-ts-price-service-stress-n787pd | improved_to_hit1 | 2 | 1 | 1.0 | ts-price-service | ts-price-service|ts-basic-service|ts-station-service|ts-travel2-service|ts-travel-service | stress | ts-price-service |
| ts0-ts-route-service-container-kill-tsqgmn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service | ts-route-service|ts-ui-dashboard|ts-verification-code-service|ts-auth-service|ts-travel-plan-service | container-kill | ts-route-service |
| ts0-ts-route-service-exception-5hzgms | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service | ts-route-service|ts-ui-dashboard|ts-order-service|ts-auth-service|ts-travel-plan-service | exception | ts-route-service |
| ts0-ts-seat-service-request-delay-wvvjgm | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|ts-consign-service | request-delay | ts-seat-service |
| ts0-ts-seat-service-response-abort-fddpcv | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-order-other-service|ts-travel-plan-service | response-abort | ts-seat-service |
| ts0-ts-station-food-service-stress-j5qdln | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-food-service | ts-station-food-service|ts-food-service|ts-order-service|ts-ui-dashboard|ts-preserve-service | stress | ts-station-food-service |
| ts0-ts-user-service-stress-mww4jr | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-travel-plan-service | stress | ts-user-service |
| ts1-mysql-bandwidth-s7srkn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-basic-service | bandwidth | mysql |
| ts1-ts-basic-service-response-replace-code-b2ftxt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-station-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-consign-service-container-kill-r8lmsx | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-preserve-service|ts-food-service|ts-travel-plan-service | container-kill | ts-consign-service |
| ts1-ts-inside-payment-service-stress-n6mttx | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-cancel-service|ts-consign-service|ts-preserve-service | stress | ts-inside-payment-service |
| ts1-ts-order-other-service-exception-twstdp | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-security-service|ts-preserve-service|ts-order-service|ts-seat-service | exception | ts-order-other-service |
| ts1-ts-order-service-stress-9mnw5v | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-consign-service|ts-config-service|ts-travel-plan-service | stress | ts-order-service |
| ts1-ts-preserve-service-stress-lbwbnm | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-food-service|ts-travel-plan-service|ts-security-service | stress | ts-preserve-service |
| ts1-ts-station-service-stress-jzbbjv | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-basic-service|ts-preserve-service|ts-travel-service|ts-travel2-service | stress | ts-station-service |
| ts1-ts-train-food-service-container-kill-nrmptr | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-food-service | ts-train-food-service|ts-food-service|ts-ui-dashboard|ts-auth-service|ts-travel-service | container-kill | ts-train-food-service |
| ts1-ts-train-service-stress-jfr96k | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service | ts-train-service|ts-ui-dashboard|ts-inside-payment-service|ts-consign-service|ts-preserve-service | stress | ts-train-service |
| ts1-ts-travel-plan-service-response-delay-zhj7r7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-auth-service|ts-travel-service|ts-route-plan-service | response-delay | ts-travel-plan-service |
| ts1-ts-travel-service-response-replace-body-vzcxrp | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-preserve-service | response-replace-body | ts-travel-service |
| ts1-ts-travel-service-response-replace-code-589p77 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-basic-service | response-replace-code | ts-travel-service |
| ts1-ts-travel-service-stress-9rhgns | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-seat-service|ts-travel-plan-service|ts-order-service | stress | ts-travel-service |
| ts1-ts-travel2-service-latency-bxgxm9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|loadgenerator|ts-basic-service | unknown | unknown |
| ts1-ts-user-service-container-kill-vnjsgg | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|ts-preserve-service|ts-consign-service|ts-auth-service | container-kill | ts-user-service |
| ts2-mysql-bandwidth-2zxrzh | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-basic-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service | bandwidth | mysql |
| ts2-ts-assurance-service-stress-ds6qwb | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-auth-service | stress | ts-assurance-service |
| ts2-ts-assurance-service-stress-hb5xt4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service | ts-assurance-service|ts-ui-dashboard|ts-travel-plan-service|ts-preserve-service|ts-auth-service | stress | ts-assurance-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
