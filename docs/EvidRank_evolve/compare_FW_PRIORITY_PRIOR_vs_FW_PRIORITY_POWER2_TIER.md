# EvidenceRank Compare FW_PRIORITY_PRIOR vs FW_PRIORITY_POWER2_TIER

- Created: 2026-06-03T23:47:36+08:00
- Old: `FW_PRIORITY_PRIOR`
- New: `FW_PRIORITY_POWER2_TIER`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800985 | 0.756681 | -0.044304 |
| AC@3 | 0.942335 | 0.941632 | -0.000703 |
| AC@5 | 0.975387 | 0.973980 | -0.001406 |
| MRR | 0.874517 | 0.851812 | -0.022705 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 27 |
| rank_improved | 37 |
| rank_regressed | 61 |
| regressed_from_hit1 | 90 |
| unchanged | 1207 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-contacts-service-pod-failure-j42hd8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service | ts-contacts-service|ts-ui-dashboard|loadgenerator|ts-order-other-service|ts-basic-service | pod-failure | ts-contacts-service |
| ts0-ts-travel-service-pod-failure-cvrncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-food-service|ts-ui-dashboard | pod-failure | ts-travel-service |
| ts1-ts-payment-service-stress-k7stf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-seat-service|ts-ui-dashboard|ts-order-service | stress | ts-payment-service |
| ts2-ts-basic-service-response-replace-code-rmprwq | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts2-ts-station-service-dns-nn49s2 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-consign-service|ts-seat-service|ts-ui-dashboard|ts-basic-service | unknown | unknown |
| ts3-ts-travel-plan-service-request-delay-kxhn5n | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-order-service | request-delay | ts-travel-plan-service |
| ts4-ts-basic-service-corrupt-trd2kh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-travel2-service|ts-seat-service | corrupt | ts-basic-service |
| ts4-ts-basic-service-request-delay-jshmsn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-order-service | request-delay | ts-basic-service |
| ts4-ts-route-plan-service-response-replace-body-bfsdhx | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|loadgenerator|ts-verification-code-service | response-replace-body | ts-route-plan-service |
| ts4-ts-seat-service-request-replace-method-9wfmmb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-seat-service |
| ts4-ts-travel2-service-request-abort-ttlcpg | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-cancel-service|ts-order-other-service | request-abort | ts-travel2-service |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-basic-service | corrupt | ts-verification-code-service |
| ts5-ts-basic-service-response-replace-code-fqg54d | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-plan-service|ts-travel2-service|ts-route-plan-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts5-ts-order-service-partition-x8xglz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | partition | ts-order-service |
| ts5-ts-seat-service-loss-5kglkt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-ui-dashboard|ts-payment-service|ts-travel-plan-service | loss | ts-seat-service |
| ts5-ts-seat-service-response-replace-body-p2bzc7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-body | ts-seat-service |
| ts5-ts-seat-service-response-replace-code-q8j5cp | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-seat-service |
| ts6-ts-travel2-service-request-delay-bnhhtc | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-seat-service | request-delay | ts-travel2-service |
| ts8-ts-food-service-pod-failure-9swgtb | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-order-service|ts-seat-service|ts-ui-dashboard|ts-basic-service | pod-failure | ts-food-service |
| ts0-ts-basic-service-pod-failure-94xplz | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-basic-service |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 3 | 1 | 2.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-auth-service|ts-verification-code-service | pod-failure | ts-user-service |
| ts2-ts-auth-service-response-patch-body-9bcpvv | improved_to_hit1 | 3 | 1 | 2.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|loadgenerator|ts-ui-dashboard|ts-verification-code-service|ts-basic-service | unknown | unknown |
| ts8-ts-seat-service-request-replace-method-mx5nvv | improved_to_hit1 | 3 | 1 | 2.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-travel2-service|ts-ui-dashboard | request-replace-method | ts-seat-service |
| ts0-ts-seat-service-pod-failure-c87xdg | improved_to_hit1 | 4 | 1 | 3.0 | ts-seat-service | ts-seat-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | pod-failure | ts-seat-service |
| ts4-ts-seat-service-response-replace-code-h5lfx8 | improved_to_hit1 | 4 | 1 | 3.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-seat-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | improved_to_hit1 | 6 | 1 | 5.0 | ts-assurance-service | ts-assurance-service|ts-route-plan-service|ts-basic-service|ts-travel-service|ts-seat-service | pod-failure | ts-assurance-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | improved_to_hit1 | 7 | 1 | 6.0 | ts-price-service | ts-price-service|ts-travel-plan-service|ts-basic-service|ts-travel2-service|ts-route-plan-service | pod-failure | ts-price-service |
| ts0-ts-basic-service-request-abort-62vtm2 | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-train-service | ts-travel-service|ts-basic-service|ts-travel2-service|ts-route-plan-service|ts-station-service | request-abort | ts-basic-service |
| ts1-ts-basic-service-request-abort-snb6ck | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-travel2-service|ts-basic-service|ts-station-service|ts-train-service|ts-route-service | request-abort | ts-basic-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | rank_improved | 3 | 2 | 1.0 | ts-station-food-service | ts-food-service|ts-station-food-service|ts-travel-service|ts-basic-service|ts-order-other-service | pod-failure | ts-station-food-service |
| ts2-mysql-pod-kill-xvzmxb | rank_improved | 9 | 8 | 1.0 | mysql | ts-auth-service|ts-travel-service|ts-security-service|ts-preserve-service|ts-order-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | rank_improved | 28 | 27 | 1.0 | ts-cancel-service | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-station-service|ts-order-service | return | ts-cancel-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | rank_improved | 4 | 3 | 1.0 | ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-ui-dashboard|loadgenerator | pod-failure | ts-travel-service |
| ts3-ts-auth-service-return-9tmvzg | rank_improved | 4 | 3 | 1.0 | ts-auth-service | ts-verification-code-service|ts-ui-dashboard|ts-auth-service|loadgenerator|ts-travel-service | return | ts-auth-service |
| ts4-ts-basic-service-request-replace-method-7c9cbv | rank_improved | 5 | 4 | 1.0 | ts-basic-service;ts-route-service | ts-route-plan-service|ts-travel-service|ts-travel-plan-service|ts-basic-service|ts-ui-dashboard | request-replace-method | ts-basic-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-train-service | ts-route-plan-service|ts-ui-dashboard|ts-basic-service|ts-travel-plan-service|ts-travel-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-response-delay-vxcl8q | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-payment-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel2-service | response-delay | ts-route-plan-service |
| ts4-ts-travel-service-response-replace-body-vhbkq2 | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-plan-service|ts-travel-service|ts-route-plan-service|ts-security-service|ts-ui-dashboard | response-replace-body | ts-travel-service |
| ts4-ts-travel2-service-response-abort-5svkhq | rank_improved | 3 | 2 | 1.0 | ts-seat-service;ts-travel2-service | ts-route-plan-service|ts-travel2-service|ts-travel-plan-service|ts-consign-service|ts-seat-service | response-abort | ts-travel2-service |
| ts4-ts-travel2-service-response-replace-body-lsqg4p | rank_improved | 5 | 4 | 1.0 | ts-seat-service;ts-travel2-service | ts-cancel-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-body | ts-travel2-service |

## Decision Notes

- Decision: reject `0,1,1,1,2,4,8,16` as default, but keep it as a useful ablation.
- Reason: it is much better than `0..7`, but still loses `0.044304` AC@1 and `0.022705` MRR versus `FW_PRIORITY_PRIOR`.
- Mechanism: keeping `CRITICAL=16` preserves top-3/top-5 fairly well, but lowering `HIGH` from `6` to `4` and `ROOT` from `10` to `8` still loses many close top-1 contests.
- Interpretation: the strong end of the ladder needs calibrated spacing; a visually clean power-of-two ladder is not enough for the current feature distributions.
