# Compare CREST9_DEFAULT vs CREST9_GATED_RESIDUAL

## Overall Metrics

| metric | old `crest` | new `crest_gated_residual` | delta |
| --- | ---: | ---: | ---: |
| total | 1422 | 1422 | 0 |
| error | 0 | 0 | 0 |
| AC@1 | 0.800281 | 0.797468 | -0.002813 |
| MRR | 0.875326 | 0.873919 | -0.001406 |
| AC@3 | 0.944444 | 0.944444 | +0.000000 |
| AC@5 | 0.971871 | 0.971871 | +0.000000 |

## Change Counts

- `improved_to_hit1`: 11
- `regressed_from_hit1`: 15
- `rank_improved`: 0
- `rank_regressed`: 0
- `unchanged`: 1396

## Hit@1 Changes By Fault Type

| change_type | fault_type | count |
| --- | --- | --- |
| improved_to_hit1 | pod-failure | 2 |
| improved_to_hit1 | response-replace-code | 2 |
| improved_to_hit1 | stress | 2 |
| improved_to_hit1 | loss | 1 |
| improved_to_hit1 | request-replace-path | 1 |
| improved_to_hit1 | response-abort | 1 |
| improved_to_hit1 | response-replace-body | 1 |
| improved_to_hit1 | return | 1 |
| regressed_from_hit1 | request-replace-method | 6 |
| regressed_from_hit1 | response-replace-code | 5 |
| regressed_from_hit1 | bandwidth | 1 |
| regressed_from_hit1 | partition | 1 |
| regressed_from_hit1 | response-abort | 1 |
| regressed_from_hit1 | response-replace-body | 1 |

## Improved To Hit@1

| datapack | gt | fault_type | top1_old | top1_new | best_rank_old | best_rank_new | rank_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ts0-ts-station-service-loss-hs8vrm | mysql;ts-station-service | loss | ts-basic-service | ts-station-service | 2 | 1 | -1 |
| ts0-ts-user-service-pod-failure-b44c7f | ts-user-service | pod-failure | ts-ui-dashboard | ts-user-service | 2 | 1 | -1 |
| ts1-ts-payment-service-stress-k7stf5 | ts-payment-service | stress | ts-inside-payment-service | ts-payment-service | 2 | 1 | -1 |
| ts1-ts-seat-service-response-replace-body-hvd8x2 | ts-order-service;ts-seat-service | response-replace-body | ts-travel-service | ts-seat-service | 2 | 1 | -1 |
| ts1-ts-seat-service-response-replace-code-dk84t5 | ts-order-service;ts-seat-service | response-replace-code | ts-travel-service | ts-seat-service | 2 | 1 | -1 |
| ts3-ts-basic-service-response-replace-code-bvqv9z | ts-basic-service;ts-station-service | response-replace-code | ts-travel2-service | ts-basic-service | 2 | 1 | -1 |
| ts3-ts-travel-service-return-p696jn | ts-travel-service | return | ts-consign-service | ts-travel-service | 2 | 1 | -1 |
| ts3-ts-ui-dashboard-response-abort-zd59tz | ts-assurance-service;ts-ui-dashboard | response-abort | loadgenerator | ts-assurance-service | 2 | 1 | -1 |
| ts4-ts-inside-payment-service-stress-gc2kcm | ts-inside-payment-service | stress | ts-payment-service | ts-inside-payment-service | 2 | 1 | -1 |
| ts6-ts-route-plan-service-pod-failure-n576ft | ts-route-plan-service | pod-failure | ts-travel-plan-service | ts-route-plan-service | 2 | 1 | -1 |
| ts9-ts-travel2-service-request-replace-path-nbzx5n | ts-basic-service;ts-travel2-service | request-replace-path | ts-travel-plan-service | ts-travel2-service | 2 | 1 | -1 |

## Regressed From Hit@1

| datapack | gt | fault_type | top1_old | top1_new | best_rank_old | best_rank_new | rank_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-z2nlcm | ts-basic-service;ts-station-service | request-replace-method | ts-basic-service | ts-travel-service | 1 | 2 | 1 |
| ts0-ts-seat-service-response-replace-code-gqm7pj | ts-order-service;ts-seat-service | response-replace-code | ts-seat-service | ts-travel-service | 1 | 2 | 1 |
| ts0-ts-travel2-service-request-replace-method-dhgqc8 | ts-basic-service;ts-travel2-service | request-replace-method | ts-travel2-service | ts-route-plan-service | 1 | 2 | 1 |
| ts1-ts-travel-service-response-replace-body-vzcxrp | ts-seat-service;ts-travel-service | response-replace-body | ts-travel-service | ts-route-plan-service | 1 | 2 | 1 |
| ts2-mysql-bandwidth-2zxrzh | mysql;ts-train-service | bandwidth | ts-train-service | ts-basic-service | 1 | 2 | 1 |
| ts2-ts-travel-service-response-replace-code-w4bgvh | ts-basic-service;ts-travel-service | response-replace-code | ts-travel-service | ts-route-plan-service | 1 | 2 | 1 |
| ts3-mysql-partition-xgmtkl | mysql;ts-station-service | partition | ts-station-service | ts-basic-service | 1 | 2 | 1 |
| ts3-ts-seat-service-response-abort-csvk8f | ts-config-service;ts-seat-service | response-abort | ts-seat-service | ts-travel-service | 1 | 2 | 1 |
| ts3-ts-travel-plan-service-response-replace-code-79hbwm | ts-route-plan-service;ts-travel-plan-service | response-replace-code | ts-travel-plan-service | ts-preserve-service | 1 | 2 | 1 |
| ts4-ts-route-plan-service-response-replace-code-cq5j9f | ts-route-plan-service;ts-travel2-service | response-replace-code | ts-route-plan-service | ts-travel-plan-service | 1 | 2 | 1 |
| ts5-ts-preserve-service-request-replace-method-gvn4ls | ts-contacts-service;ts-preserve-service | request-replace-method | ts-preserve-service | ts-security-service | 1 | 2 | 1 |
| ts5-ts-route-plan-service-request-replace-method-7msq7k | ts-route-plan-service;ts-route-service | request-replace-method | ts-route-plan-service | ts-travel-plan-service | 1 | 2 | 1 |
| ts5-ts-route-plan-service-request-replace-method-cthlsk | ts-route-plan-service;ts-route-service | request-replace-method | ts-route-plan-service | ts-travel-plan-service | 1 | 2 | 1 |
| ts5-ts-seat-service-response-replace-code-q8j5cp | ts-config-service;ts-seat-service | response-replace-code | ts-seat-service | ts-route-plan-service | 1 | 2 | 1 |
| ts5-ts-ui-dashboard-request-replace-method-wlvx9d | ts-travel2-service;ts-ui-dashboard | request-replace-method | ts-ui-dashboard | ts-cancel-service | 1 | 2 | 1 |

## Decision

Reject `crest_gated_residual` as a default change. The gated residual ablation keeps AC@3 and AC@5 unchanged but loses four AC@1 hits and lowers MRR. The residual confidence boundary is still not reliable enough; future work should use residual as a diagnostic/contrast signal rather than an additive ranking channel.
