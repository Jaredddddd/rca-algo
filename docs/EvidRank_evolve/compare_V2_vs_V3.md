# EvidenceRank Compare V2 vs V3

- Created: 2026-06-01T15:31:05+08:00
- Old: `V2`
- New: `V3`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.531646 | 0.559072 | 0.027426 |
| AC@3 | 0.786920 | 0.789030 | 0.002110 |
| AC@5 | 0.886779 | 0.888186 | 0.001406 |
| MRR | 0.684448 | 0.698007 | 0.013559 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 65 |
| rank_improved | 107 |
| rank_regressed | 127 |
| regressed_from_hit1 | 26 |
| unchanged | 1097 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-response-abort-c4gjrt | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-consign-price-service|ts-route-plan-service|ts-price-service|ts-travel2-service | response-abort | ts-basic-service |
| ts0-ts-preserve-service-response-abort-7gp2mq | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-ui-dashboard|ts-security-service|ts-station-service|ts-seat-service | response-abort | ts-preserve-service |
| ts0-ts-route-plan-service-request-replace-method-lrzhl6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-seat-service|ts-travel-plan-service|ts-auth-service|ts-verification-code-service | request-replace-method | ts-route-plan-service |
| ts0-ts-security-service-request-replace-method-m5g977 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-seat-service | request-replace-method | ts-security-service |
| ts0-ts-security-service-response-replace-code-fbsfls | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-ui-dashboard|ts-preserve-service|ts-order-service|ts-seat-service | response-replace-code | ts-security-service |
| ts1-mysql-corrupt-66nt6d | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-food-service | ts-station-food-service|ts-food-service|ts-basic-service|ts-ui-dashboard|ts-seat-service | corrupt | mysql |
| ts1-mysql-delay-hx85fg | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-travel-service|ts-ui-dashboard|ts-travel2-service | delay | mysql |
| ts1-ts-preserve-service-response-replace-body-6bfbmp | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-security-service|ts-order-service | response-replace-body | ts-preserve-service |
| ts1-ts-preserve-service-response-replace-code-qnm2bw | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-travel-service | response-replace-code | ts-preserve-service |
| ts1-ts-travel-plan-service-request-abort-6cqc2h | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-consign-price-service|ts-seat-service|ts-travel2-service|ts-route-plan-service | request-abort | ts-travel-plan-service |
| ts1-ts-ui-dashboard-response-replace-code-qc5tk4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-ui-dashboard;ts-user-service | ts-ui-dashboard|ts-seat-service|ts-order-service|ts-verification-code-service|ts-route-plan-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-auth-service-partition-btjpnk | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-auth-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-news-service | partition | ts-auth-service |
| ts2-ts-preserve-service-request-replace-method-zz2gxz | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-security-service | ts-preserve-service|ts-ui-dashboard|ts-verification-code-service|ts-seat-service|ts-auth-service | request-replace-method | ts-preserve-service |
| ts2-ts-route-plan-service-response-replace-body-dghfbk | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service | response-replace-body | ts-route-plan-service |
| ts2-ts-travel-plan-service-response-replace-body-j8bt56 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-route-plan-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-basic-service | response-replace-body | ts-travel-plan-service |
| ts2-ts-travel2-service-response-delay-mxrns5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-seat-service | response-delay | ts-travel2-service |
| ts2-ts-travel2-service-response-replace-code-4xptvj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-travel-plan-service|ts-basic-service|ts-seat-service | response-replace-code | ts-travel2-service |
| ts2-ts-travel2-service-response-replace-code-tdtcrq | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-payment-service|ts-route-plan-service|ts-travel-plan-service|ts-route-service | response-replace-code | ts-travel2-service |
| ts2-ts-ui-dashboard-response-abort-rcfl6z | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service;ts-ui-dashboard | ts-travel-service|ts-inside-payment-service|ts-auth-service|ts-ui-dashboard|ts-seat-service | response-abort | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-7nldtm | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-auth-service|ts-verification-code-service|ts-seat-service|ts-travel-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts3-mysql-corrupt-4kplqx | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-basic-service | corrupt | mysql |
| ts3-ts-config-service-corrupt-rvz9sf | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service | corrupt | ts-config-service |
| ts3-ts-config-service-partition-gpznpx | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-seat-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service | partition | ts-config-service |
| ts3-ts-contacts-service-partition-g7s7mn | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-contacts-service | ts-contacts-service|ts-ui-dashboard|ts-travel-service|ts-seat-service|ts-order-service | partition | ts-contacts-service |
| ts3-ts-food-service-request-replace-method-p4xjxp | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|ts-seat-service|ts-verification-code-service|ts-auth-service | request-replace-method | ts-food-service |
| ts3-ts-preserve-service-request-replace-path-lxcwn2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-security-service|loadgenerator | request-replace-path | ts-preserve-service |
| ts3-ts-travel-service-response-delay-7c9494 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-ui-dashboard|ts-seat-service|ts-travel-plan-service|ts-route-plan-service | response-delay | ts-travel-service |
| ts4-ts-auth-service-corrupt-pldpdm | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-order-service | corrupt | ts-auth-service |
| ts4-ts-basic-service-request-delay-slc8g7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-station-food-service|ts-travel-service|ts-seat-service | request-delay | ts-basic-service |
| ts4-ts-basic-service-response-delay-hmp7h5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-preserve-service|ts-seat-service | response-delay | ts-basic-service |
| ts4-ts-food-service-corrupt-ccxs65 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|ts-seat-service|ts-travel-plan-service|ts-travel-service | corrupt | ts-food-service |
| ts4-ts-order-other-service-delay-mpwtgz | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-travel-plan-service | delay | ts-order-other-service |
| ts4-ts-order-other-service-loss-j4l4zs | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-order-other-service | ts-order-other-service|ts-seat-service|ts-ui-dashboard|ts-travel2-service|ts-preserve-service | loss | ts-order-other-service |
| ts4-ts-route-plan-service-corrupt-qgnf8n | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-seat-service|ts-order-service|ts-travel-service | corrupt | ts-route-plan-service |
| ts4-ts-route-service-partition-cclrcm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-route-service | ts-route-service|ts-ui-dashboard|ts-auth-service|ts-travel-service|ts-seat-service | partition | ts-route-service |
| ts4-ts-train-service-corrupt-vm6cjh | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-ui-dashboard | ts-ui-dashboard|ts-cancel-service|ts-order-service|ts-order-other-service|ts-seat-service | corrupt | ts-train-service |
| ts4-ts-travel-service-partition-xq25fj | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-service | ts-travel-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-seat-service | partition | ts-travel-service |
| ts4-ts-ui-dashboard-response-replace-code-lk7q57 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|ts-payment-service|ts-order-service|ts-travel2-service | response-replace-code | ts-ui-dashboard |
| ts4-ts-verification-code-service-corrupt-pl6qvv | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-verification-code-service | ts-auth-service|ts-ui-dashboard|ts-order-service|ts-seat-service|ts-basic-service | corrupt | ts-verification-code-service |
| ts5-mysql-bandwidth-mt84s2 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-train-service | ts-train-service|ts-basic-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel-service | bandwidth | mysql |

## Decision Notes

- Accept V3. It improves AC@1, MRR, AC@3, and AC@5 with zero eval errors.
- General mechanism: equal-weight summation was overusing topology degree and high-volume symptoms as positive evidence. V3 makes fusion family-aware: trace-path evidence remains baseline, metric/log magnitudes are lightly damped, row coverage is treated as support, and topology degree becomes a small propagation-risk penalty.
- `improved_to_hit1` has 65 cases, especially `partition`, `corrupt`, `loss`, `bandwidth`, and request/response cases that were rank 2 under V2.
- `regressed_from_hit1` has 26 cases. Most move only to rank 2 or 3; notable larger drops are one `pod-failure` case to rank 6 and one request method replacement case to rank 4.
- Keep this version, but the next iteration should replace the uniform topology penalty with direction-aware neighbor contrast so central true roots are not penalized as much as propagated neighbors.
