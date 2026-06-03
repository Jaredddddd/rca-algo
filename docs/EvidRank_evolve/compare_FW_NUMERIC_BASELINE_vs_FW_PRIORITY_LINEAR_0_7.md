# EvidenceRank Compare FW_NUMERIC_BASELINE vs FW_PRIORITY_LINEAR_0_7

- Created: 2026-06-03T23:33:06+08:00
- Old: `FW_NUMERIC_BASELINE`
- New: `FW_PRIORITY_LINEAR_0_7`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.671589 | -0.130802 |
| AC@3 | 0.943741 | 0.886076 | -0.057665 |
| AC@5 | 0.975387 | 0.945148 | -0.030239 |
| MRR | 0.875337 | 0.789295 | -0.086042 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 43 |
| rank_improved | 23 |
| rank_regressed | 118 |
| regressed_from_hit1 | 229 |
| unchanged | 1009 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts1-ts-route-service-corrupt-qlt7gn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|loadgenerator|ts-train-service|ts-auth-service | corrupt | ts-route-service |
| ts1-ts-ui-dashboard-partition-99sdlj | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|loadgenerator|ts-basic-service|ts-auth-service | partition | ts-ui-dashboard |
| ts2-mysql-bandwidth-bbk2d4 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | bandwidth | mysql |
| ts2-ts-security-service-request-replace-method-vdvkxf | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-order-service | request-replace-method | ts-security-service |
| ts2-ts-station-service-dns-nn49s2 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-travel-service | unknown | unknown |
| ts3-mysql-corrupt-wgvhdb | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-route-plan-service|ts-travel2-service|ts-travel-service | corrupt | mysql |
| ts3-ts-travel-plan-service-request-delay-kxhn5n | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-travel-service|ts-route-service|loadgenerator | request-delay | ts-travel-plan-service |
| ts3-ts-ui-dashboard-request-replace-method-rp5xrr | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|loadgenerator|ts-travel-service|ts-seat-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-corrupt-trd2kh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-travel2-service|ts-contacts-service | corrupt | ts-basic-service |
| ts4-ts-basic-service-request-abort-jr6f2j | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-consign-service|ts-order-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts4-ts-basic-service-request-delay-jkxt8v | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-seat-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-request-delay-jshmsn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-order-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-response-delay-76ksjc | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-route-plan-service | response-delay | ts-basic-service |
| ts4-ts-seat-service-corrupt-d8skmr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-basic-service|ts-auth-service | corrupt | ts-seat-service |
| ts4-ts-seat-service-request-replace-method-9wfmmb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service | request-replace-method | ts-seat-service |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-seat-service | corrupt | ts-verification-code-service |
| ts5-mysql-loss-q42phw | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-auth-service | ts-auth-service|ts-ui-dashboard|ts-order-service|ts-travel-service|ts-travel-plan-service | loss | mysql |
| ts5-ts-basic-service-request-abort-vrvjhn | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-order-service|ts-preserve-service|ts-seat-service|ts-travel-service | request-abort | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-j4nzcx | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-route-plan-service|ts-consign-price-service|ts-travel2-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-fqg54d | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-order-service|ts-travel-plan-service|ts-travel-service | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-n7djz7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-order-service|ts-seat-service|ts-ui-dashboard | response-replace-code | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-s6wgdk | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-preserve-service|ts-seat-service|ts-order-service|ts-travel-service | response-replace-code | ts-basic-service |
| ts5-ts-order-service-corrupt-bd4p5g | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-order-other-service|ts-route-service|ts-consign-price-service|ts-station-food-service | corrupt | ts-order-service |
| ts5-ts-order-service-partition-x8xglz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-ui-dashboard|loadgenerator|ts-route-plan-service | partition | ts-order-service |
| ts5-ts-route-service-corrupt-vvvjts | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-ui-dashboard|ts-basic-service|ts-seat-service|ts-travel-service | corrupt | ts-route-service |
| ts5-ts-seat-service-loss-5kglkt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service | loss | ts-seat-service |
| ts5-ts-seat-service-response-replace-body-p2bzc7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|loadgenerator | response-replace-body | ts-seat-service |
| ts5-ts-seat-service-response-replace-code-q8j5cp | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-route-plan-service|ts-travel2-service|ts-travel-plan-service | response-replace-code | ts-seat-service |
| ts5-ts-travel-service-response-patch-body-nt8z6r | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-order-service|ts-assurance-service|ts-seat-service|ts-station-service | unknown | unknown |
| ts6-ts-travel2-service-request-delay-bnhhtc | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-travel-service | request-delay | ts-travel2-service |
| ts8-ts-basic-service-response-replace-code-w8c2xr | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-order-service|ts-travel-service|ts-security-service | response-replace-code | ts-basic-service |
| ts8-ts-travel-service-request-replace-method-f6gclk | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-seat-service|ts-basic-service | request-replace-method | ts-travel-service |
| ts2-mysql-bandwidth-fws9rx | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-service | bandwidth | mysql |
| ts2-ts-travel-service-bandwidth-f9fkg7 | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-order-service | bandwidth | ts-travel-service |
| ts3-mysql-partition-4hh8bj | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator | partition | mysql |
| ts4-ts-route-plan-service-response-delay-vxcl8q | improved_to_hit1 | 3 | 1 | 2.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-ui-dashboard|ts-payment-service|ts-travel2-service|ts-route-service | response-delay | ts-route-plan-service |
| ts4-ts-travel-service-response-replace-body-vhbkq2 | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-order-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service | response-replace-body | ts-travel-service |
| ts4-ts-travel2-service-response-abort-5svkhq | improved_to_hit1 | 3 | 1 | 2.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-consign-service|ts-seat-service | response-abort | ts-travel2-service |
| ts5-ts-travel-plan-service-response-delay-7cc7nq | improved_to_hit1 | 3 | 1 | 2.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-order-service|ts-security-service|ts-payment-service|ts-seat-service | response-delay | ts-travel-plan-service |
| ts8-ts-seat-service-request-replace-method-mx5nvv | improved_to_hit1 | 3 | 1 | 2.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service|ts-travel-service | request-replace-method | ts-seat-service |

## Decision Notes

- Decision: reject `0..7` linear ordinal weights as default.
- Reason: relative to the numeric baseline, AC@1 drops by `0.130802`, MRR by `0.086042`, AC@3 by `0.057665`, and AC@5 by `0.030239`.
- Mechanism: ordinal values compress root-specific evidence and over-weight propagation/background evidence. This is too large a behavioral change for a presentation refactor.
