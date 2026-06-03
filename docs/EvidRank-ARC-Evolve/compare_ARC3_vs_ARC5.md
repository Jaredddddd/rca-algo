# EvidenceRank Compare ARC3 vs ARC5

- Created: 2026-06-03T19:34:06+08:00
- Old: `ARC3`
- New: `ARC5`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.720113 | 0.728551 | 0.008439 |
| AC@3 | 0.940928 | 0.940225 | -0.000703 |
| AC@5 | 0.973277 | 0.973277 | 0.000000 |
| MRR | 0.832050 | 0.836412 | 0.004362 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 15 |
| rank_improved | 14 |
| rank_regressed | 9 |
| regressed_from_hit1 | 3 |
| unchanged | 1381 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts1-mysql-delay-hx85fg | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-config-service | ts-config-service|ts-ui-dashboard|ts-seat-service|ts-travel-service|loadgenerator | delay | mysql |
| ts1-ts-preserve-service-request-replace-method-xmhsbb | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-contacts-service|ts-travel-service | request-replace-method | ts-preserve-service |
| ts1-ts-preserve-service-response-replace-code-bndht9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-travel-service|ts-basic-service|ts-food-service | response-replace-code | ts-preserve-service |
| ts1-ts-preserve-service-response-replace-code-wpdr2x | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-travel-service | response-replace-code | ts-preserve-service |
| ts1-ts-travel-plan-service-request-replace-method-d2pqdm | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-station-service|ts-route-service | request-replace-method | ts-travel-plan-service |
| ts2-ts-seat-service-request-delay-775n8q | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-travel-plan-service | request-delay | ts-seat-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service|ts-price-service | pod-failure | ts-travel2-service |
| ts3-ts-preserve-service-request-replace-method-msns6h | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|ts-travel-service|ts-seat-service | request-replace-method | ts-preserve-service |
| ts3-ts-preserve-service-request-replace-path-lxcwn2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-contacts-service|ts-seat-service|loadgenerator | request-replace-path | ts-preserve-service |
| ts3-ts-travel2-service-response-delay-hf7kl4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel2-service | ts-travel2-service|ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-route-service | response-delay | ts-travel2-service |
| ts4-ts-ui-dashboard-response-replace-code-czmwrk | improved_to_hit1 | 2 | 1 | 1.0 | ts-train-service;ts-ui-dashboard | ts-ui-dashboard|ts-payment-service|ts-inside-payment-service|loadgenerator|ts-train-food-service | response-replace-code | ts-ui-dashboard |
| ts5-ts-basic-service-corrupt-hvpqlr | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel-service|ts-travel2-service | corrupt | ts-basic-service |
| ts5-ts-route-plan-service-response-delay-5mjstz | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel2-service|ts-basic-service|ts-payment-service|ts-food-service | response-delay | ts-route-plan-service |
| ts5-ts-travel-plan-service-container-kill-76w568 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-payment-service|ts-basic-service|ts-travel-service | container-kill | ts-travel-plan-service |
| ts8-ts-route-plan-service-request-delay-5dmjfm | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-payment-service|ts-ui-dashboard|ts-seat-service|ts-travel-plan-service | request-delay | ts-route-plan-service |
| ts2-ts-order-other-service-container-kill-48rlds | rank_improved | 4 | 3 | 1.0 | ts-order-other-service | ts-seat-service|ts-travel2-service|ts-order-other-service|ts-ui-dashboard|ts-basic-service | container-kill | ts-order-other-service |
| ts2-ts-ui-dashboard-request-replace-method-jrt2mv | rank_improved | 3 | 2 | 1.0 | ts-train-service;ts-ui-dashboard | ts-seat-service|ts-train-service|ts-order-service|ts-ui-dashboard|loadgenerator | request-replace-method | ts-ui-dashboard |
| ts3-ts-route-plan-service-request-replace-path-m56fgf | rank_improved | 4 | 3 | 1.0 | ts-route-plan-service;ts-travel-service | ts-travel-plan-service|ts-verification-code-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-service | request-replace-path | ts-route-plan-service |
| ts4-ts-basic-service-response-replace-body-jrv8dx | rank_improved | 3 | 2 | 1.0 | ts-basic-service;ts-price-service | ts-ui-dashboard|ts-basic-service|ts-travel2-service|ts-preserve-service|ts-seat-service | response-replace-body | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | rank_improved | 16 | 15 | 1.0 | ts-cancel-service | ts-consign-service|ts-food-service|ts-basic-service|ts-route-plan-service|loadgenerator | stress | ts-cancel-service |
| ts5-ts-route-plan-service-response-replace-code-2w8c9x | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-ui-dashboard|ts-route-plan-service|ts-consign-price-service|ts-cancel-service|ts-travel-plan-service | response-replace-code | ts-route-plan-service |
| ts5-ts-travel-plan-service-response-replace-code-k8hf8v | rank_improved | 5 | 4 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-consign-price-service|ts-seat-service|ts-ui-dashboard|ts-travel-plan-service|ts-basic-service | response-replace-code | ts-travel-plan-service |
| ts5-ts-travel-service-response-delay-9x42gg | rank_improved | 4 | 3 | 1.0 | ts-basic-service;ts-travel-service | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-food-service|ts-route-plan-service | response-delay | ts-travel-service |
| ts5-ts-ui-dashboard-response-replace-code-g2v8rq | rank_improved | 3 | 2 | 1.0 | ts-ui-dashboard;ts-user-service | ts-assurance-service|ts-ui-dashboard|ts-seat-service|ts-cancel-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts6-ts-route-plan-service-pod-failure-n576ft | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service | ts-travel-plan-service|ts-route-plan-service|ts-payment-service|ts-ui-dashboard|ts-seat-service | pod-failure | ts-route-plan-service |
| ts7-ts-route-plan-service-response-delay-t55rlr | rank_improved | 7 | 6 | 1.0 | ts-route-plan-service;ts-travel-service | ts-inside-payment-service|ts-station-food-service|ts-ui-dashboard|ts-travel-plan-service|ts-seat-service | response-delay | ts-route-plan-service |
| ts8-ts-route-plan-service-response-replace-body-l4k72c | rank_improved | 3 | 2 | 1.0 | ts-route-plan-service;ts-travel-service | ts-travel-plan-service|ts-route-plan-service|ts-payment-service|ts-travel2-service|ts-order-other-service | response-replace-body | ts-route-plan-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | rank_improved | 13 | 11 | 2.0 | ts-order-other-service;ts-ui-dashboard | loadgenerator|ts-seat-service|ts-station-food-service|ts-travel2-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | rank_improved | 9 | 6 | 3.0 | ts-travel-plan-service;ts-ui-dashboard | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-consign-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts4-ts-station-service-bandwidth-nfljv5 | rank_regressed | 10 | 12 | -2.0 | ts-basic-service;ts-station-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service | bandwidth | ts-station-service |
| ts3-ts-basic-service-partition-w5hbjw | rank_regressed | 3 | 4 | -1.0 | ts-basic-service;ts-travel-service | ts-ui-dashboard|ts-food-service|loadgenerator|ts-basic-service|ts-order-service | partition | ts-basic-service |
| ts3-ts-travel-plan-service-request-delay-b8pn5w | rank_regressed | 2 | 3 | -1.0 | ts-train-service;ts-travel-plan-service | ts-ui-dashboard|loadgenerator|ts-travel-plan-service|ts-basic-service|ts-preserve-service | request-delay | ts-travel-plan-service |
| ts3-ts-ui-dashboard-request-replace-method-7lstrz | rank_regressed | 2 | 3 | -1.0 | ts-assurance-service;ts-ui-dashboard | ts-basic-service|ts-verification-code-service|ts-ui-dashboard|ts-price-service|ts-contacts-service | request-replace-method | ts-ui-dashboard |
| ts5-mysql-loss-q42phw | rank_regressed | 2 | 3 | -1.0 | mysql;ts-auth-service | ts-ui-dashboard|loadgenerator|ts-auth-service|ts-order-service|ts-seat-service | loss | mysql |
| ts5-ts-basic-service-request-delay-xjt5h5 | rank_regressed | 2 | 3 | -1.0 | ts-basic-service;ts-train-service | ts-preserve-service|ts-route-plan-service|ts-basic-service|ts-travel-service|ts-ui-dashboard | request-delay | ts-basic-service |
| ts7-ts-basic-service-bandwidth-mgb7rl | rank_regressed | 3 | 4 | -1.0 | ts-basic-service;ts-route-service | ts-ui-dashboard|ts-seat-service|loadgenerator|ts-basic-service|ts-route-service | bandwidth | ts-basic-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | rank_regressed | 9 | 10 | -1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service|ts-food-service|ts-consign-service|ts-seat-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts9-ts-ui-dashboard-response-replace-code-4bfgrj | rank_regressed | 3 | 4 | -1.0 | ts-consign-service;ts-ui-dashboard | ts-payment-service|ts-seat-service|ts-inside-payment-service|ts-ui-dashboard|ts-food-service | response-replace-code | ts-ui-dashboard |
| ts5-mysql-corrupt-k6788t | regressed_from_hit1 | 1 | 4 | -3.0 | mysql;ts-order-service | ts-seat-service|ts-station-service|ts-ui-dashboard|ts-order-service|ts-food-service | corrupt | mysql |
| ts4-ts-ui-dashboard-loss-gvqmxw | regressed_from_hit1 | 1 | 2 | -1.0 | ts-travel-service;ts-ui-dashboard | ts-assurance-service|ts-ui-dashboard|ts-seat-service|loadgenerator|ts-basic-service | loss | ts-ui-dashboard |

## Decision Notes

- Accept ARC5. It improves AC@1 by `+0.008439` and MRR by `+0.004362`, keeps AC@5 unchanged, and has only a one-case AC@3 regression.
- The accepted mechanism is a trace-directed top-neighbor pairwise score transfer: mutation-heavier adjacent root candidates can recover score from propagation-heavier victims when ARC3 currently ranks the victim higher.
- `regressed_from_hit1` cases are explainable and match the known risk: in corrupt, loss, and request-delay cases, propagation-shaped evidence or upstream/entry-like traffic can be part of the causal signature, so the pairwise victim/root assumption is occasionally too aggressive.
- The next follow-up should test a topology-confidence gate for reverse-direction transfer, but ARC5's net top-1 gain is currently better than the safer gated variants.
