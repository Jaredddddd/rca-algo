# EvidenceRank Compare V11 vs V18

- Created: 2026-06-02T21:15:32+08:00
- Old: `V11`
- New: `V18`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.506329 | -0.296062 |
| AC@3 | 0.943741 | 0.833333 | -0.110408 |
| AC@5 | 0.975387 | 0.941632 | -0.033755 |
| MRR | 0.875337 | 0.684853 | -0.190484 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 46 |
| rank_improved | 29 |
| rank_regressed | 131 |
| regressed_from_hit1 | 467 |
| unchanged | 749 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-contacts-service-pod-failure-j42hd8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service | ts-contacts-service|ts-ui-dashboard|loadgenerator|ts-order-other-service|ts-route-service | pod-failure | ts-contacts-service |
| ts0-ts-travel-service-pod-failure-cvrncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-food-service|ts-ui-dashboard | pod-failure | ts-travel-service |
| ts1-ts-payment-service-stress-k7stf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-payment-service | ts-payment-service|ts-inside-payment-service|ts-cancel-service|ts-ui-dashboard|ts-order-other-service | stress | ts-payment-service |
| ts1-ts-route-service-corrupt-qlt7gn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|loadgenerator|ts-consign-service|ts-train-service | corrupt | ts-route-service |
| ts1-ts-ui-dashboard-request-abort-cr4wzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-station-service|ts-basic-service|ts-travel-service | request-abort | ts-ui-dashboard |
| ts2-mysql-bandwidth-bbk2d4 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-basic-service|mysql|ts-travel-service|ts-travel-plan-service | bandwidth | mysql |
| ts2-ts-station-service-dns-nn49s2 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-consign-service|ts-seat-service|ts-ui-dashboard|ts-payment-service | unknown | unknown |
| ts2-ts-ui-dashboard-request-replace-method-h27hzq | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-food-service|loadgenerator|ts-ui-dashboard|ts-order-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts3-mysql-corrupt-wgvhdb | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | corrupt | mysql |
| ts3-ts-order-service-pod-failure-7xsmwd | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel-plan-service | pod-failure | ts-order-service |
| ts3-ts-travel-plan-service-request-delay-kxhn5n | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-verification-code-service | request-delay | ts-travel-plan-service |
| ts3-ts-ui-dashboard-request-replace-method-rp5xrr | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|loadgenerator|ts-user-service|ts-order-other-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-corrupt-trd2kh | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-security-service|ts-travel2-service | corrupt | ts-basic-service |
| ts4-ts-route-plan-service-corrupt-kw4rss | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-seat-service | corrupt | ts-route-plan-service |
| ts4-ts-route-plan-service-response-replace-body-bfsdhx | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-consign-service | response-replace-body | ts-route-plan-service |
| ts4-ts-route-plan-service-response-replace-code-fszhvp | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|loadgenerator | response-replace-code | ts-route-plan-service |
| ts4-ts-seat-service-corrupt-d8skmr | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-basic-service|ts-auth-service | corrupt | ts-seat-service |
| ts4-ts-seat-service-request-replace-method-9wfmmb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-seat-service |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-order-service | corrupt | ts-verification-code-service |
| ts5-mysql-loss-q42phw | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-auth-service | ts-auth-service|ts-delivery-service|ts-ui-dashboard|ts-train-food-service|loadgenerator | loss | mysql |
| ts5-ts-order-service-partition-x8xglz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | partition | ts-order-service |
| ts5-ts-route-service-corrupt-vvvjts | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-basic-service|ts-train-food-service | corrupt | ts-route-service |
| ts5-ts-seat-service-response-replace-code-q8j5cp | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel-plan-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-seat-service |
| ts5-ts-ui-dashboard-request-replace-method-dd2fll | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-ui-dashboard | ts-contacts-service|loadgenerator|ts-ui-dashboard|ts-travel2-service|ts-verification-code-service | request-replace-method | ts-ui-dashboard |
| ts6-ts-basic-service-corrupt-zg68ql | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-delivery-service|ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service | corrupt | ts-basic-service |
| ts8-ts-food-service-pod-failure-9swgtb | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-station-service|ts-price-service|ts-order-service|ts-order-other-service | pod-failure | ts-food-service |
| ts8-ts-food-service-response-replace-code-lsl65n | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|ts-order-service|ts-travel-plan-service|ts-seat-service | response-replace-code | ts-food-service |
| ts0-ts-basic-service-pod-failure-94xplz | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service | ts-basic-service|ts-travel-service|ts-route-plan-service|ts-travel2-service|ts-travel-plan-service | pod-failure | ts-basic-service |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 3 | 1 | 2.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-travel-service | pod-failure | ts-user-service |
| ts1-ts-basic-service-request-abort-snb6ck | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-consign-price-service|ts-station-service|ts-route-plan-service | request-abort | ts-basic-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | improved_to_hit1 | 3 | 1 | 2.0 | ts-station-food-service | ts-station-food-service|ts-food-service|ts-travel-service|ts-basic-service|ts-order-other-service | pod-failure | ts-station-food-service |
| ts2-mysql-bandwidth-fws9rx | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel2-service | ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|loadgenerator | bandwidth | mysql |
| ts2-ts-travel-service-bandwidth-f9fkg7 | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-travel-service | mysql|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | bandwidth | ts-travel-service |
| ts3-ts-route-service-corrupt-rplmkr | improved_to_hit1 | 3 | 1 | 2.0 | mysql;ts-route-service | ts-route-service|ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-config-service | corrupt | ts-route-service |
| ts0-ts-seat-service-pod-failure-c87xdg | improved_to_hit1 | 4 | 1 | 3.0 | ts-seat-service | ts-seat-service|ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-travel2-service | pod-failure | ts-seat-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | improved_to_hit1 | 4 | 1 | 3.0 | ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|loadgenerator | pod-failure | ts-travel-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | improved_to_hit1 | 4 | 1 | 3.0 | ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-price-service | pod-failure | ts-travel2-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | improved_to_hit1 | 4 | 1 | 3.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-preserve-service|ts-ui-dashboard|ts-verification-code-service | pod-failure | ts-consign-price-service |
| ts1-ts-station-service-pod-failure-fn44tf | improved_to_hit1 | 6 | 1 | 5.0 | ts-station-service | ts-station-service|ts-travel-service|ts-basic-service|ts-travel2-service|ts-route-plan-service | pod-failure | ts-station-service |
| ts1-ts-train-service-pod-failure-5qwqdz | improved_to_hit1 | 6 | 1 | 5.0 | ts-train-service | ts-train-service|ts-basic-service|ts-travel-service|ts-route-plan-service|ts-travel2-service | pod-failure | ts-train-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
