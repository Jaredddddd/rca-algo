# Compare CREST15_DEFAULT vs CREST15_CLUSTER_ARBITRATION

## Metrics

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST15_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 9.113438s |
| CREST15_CLUSTER_ARBITRATION / `crest_cluster_arbitration` | 1422 | 0 | 0.812940 | 0.882065 | 0.945148 | 0.971871 | 9.134214s |

## Delta Summary

- `improved_to_hit1`: 18
- `regressed_from_hit1`: 0
- `top1_changed`: 22
- `rank_improved`: 18
- `rank_regressed`: 0
- `AC@1` delta: +0.012658
- `MRR` delta: +0.006739

## Top-1 Switches

| datapack | fault_type | gt | old top1 | new top1 | old rank | new rank | hit@1 delta |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| ts2-ts-order-other-service-container-kill-48rlds | container-kill | ts-order-other-service | ts-seat-service | ts-order-other-service | 4 | 1 | improved |
| ts2-ts-basic-service-response-replace-code-qf2qml | response-replace-code | ts-basic-service;ts-price-service | ts-travel-service | ts-basic-service | 3 | 1 | improved |
| ts3-ts-seat-service-response-replace-code-cfcfbf | response-replace-code | ts-config-service;ts-seat-service | ts-travel-service | ts-seat-service | 3 | 1 | improved |
| ts0-ts-basic-service-request-replace-method-99j798 | request-replace-method | ts-basic-service;ts-route-service | ts-preserve-service | ts-basic-service | 2 | 1 | improved |
| ts0-ts-basic-service-response-replace-code-r727qm | response-replace-code | ts-basic-service;ts-route-service | ts-travel-service | ts-basic-service | 2 | 1 | improved |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | response-replace-code | ts-order-service;ts-seat-service | ts-travel-service | ts-seat-service | 2 | 1 | improved |
| ts1-ts-basic-service-request-replace-method-2b57wf | request-replace-method | ts-basic-service;ts-price-service | ts-travel-service | ts-basic-service | 2 | 1 | improved |
| ts1-ts-seat-service-request-replace-path-jmcntt | request-replace-path | ts-order-other-service;ts-seat-service | ts-travel2-service | ts-seat-service | 2 | 1 | improved |
| ts1-ts-seat-service-response-replace-code-dk84t5 | response-replace-code | ts-order-service;ts-seat-service | ts-travel-service | ts-seat-service | 2 | 1 | improved |
| ts1-ts-travel-service-response-replace-code-qzmhjf | response-replace-code | ts-basic-service;ts-travel-service | ts-route-plan-service | ts-travel-service | 2 | 1 | improved |
| ts2-ts-basic-service-response-replace-code-92j5cs | response-replace-code | ts-basic-service;ts-train-service | ts-travel2-service | ts-basic-service | 2 | 1 | improved |
| ts2-ts-travel-service-response-abort-jd66zv | response-abort | ts-route-service;ts-travel-service | ts-food-service | ts-travel-service | 2 | 1 | improved |
| ts2-ts-travel2-service-response-replace-code-ttpn92 | response-replace-code | ts-basic-service;ts-travel2-service | ts-route-plan-service | ts-travel2-service | 2 | 1 | improved |
| ts3-ts-basic-service-response-replace-code-bvqv9z | response-replace-code | ts-basic-service;ts-station-service | ts-travel2-service | ts-basic-service | 2 | 1 | improved |
| ts3-ts-route-plan-service-request-replace-path-m56fgf | request-replace-path | ts-route-plan-service;ts-travel-service | ts-travel-plan-service | ts-route-plan-service | 2 | 1 | improved |
| ts3-ts-seat-service-response-replace-code-xdw4c7 | response-replace-code | ts-order-service;ts-seat-service | ts-travel-service | ts-seat-service | 2 | 1 | improved |
| ts3-ts-travel-service-request-replace-path-vktk7x | request-replace-path | ts-route-service;ts-travel-service | ts-food-service | ts-travel-service | 2 | 1 | improved |
| ts9-ts-route-plan-service-request-replace-path-9dg8qf | request-replace-path | ts-route-plan-service;ts-travel-service | ts-payment-service | ts-route-plan-service | 2 | 1 | improved |
| ts2-ts-basic-service-request-replace-method-t7fncf | request-replace-method | ts-basic-service;ts-price-service | ts-price-service | ts-basic-service | 1 | 1 | unchanged miss |
| ts4-ts-basic-service-response-replace-code-7tlb8z | response-replace-code | ts-basic-service;ts-price-service | ts-inside-payment-service | ts-route-plan-service | 5 | 5 | unchanged miss |
| ts5-ts-basic-service-request-replace-method-m559vq | request-replace-method | ts-basic-service;ts-route-service | ts-route-plan-service | ts-travel-service | 6 | 6 | unchanged miss |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | request-replace-method | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service | ts-consign-service | 8 | 8 | unchanged miss |

## Fault-Type Switch Summary

| fault_type | switches | improved_to_hit1 | regressed_from_hit1 | avg_mrr_delta |
| --- | ---: | ---: | ---: | ---: |
| response-replace-code | 11 | 10 | 0 | +0.484848 |
| request-replace-path | 4 | 4 | 0 | +0.500000 |
| request-replace-method | 5 | 2 | 0 | +0.200000 |
| container-kill | 1 | 1 | 0 | +0.750000 |
| response-abort | 1 | 1 | 0 | +0.500000 |

## Decision

CREST15 cluster arbitration is an accepted intermediate improvement. It improves AC@1, MRR, and AC@3 with no hit@1 or rank regressions relative to the current default. It still does not reach `AC@1 >= 0.85`, so the overall goal remains active.

## Artifacts

- `output/rcabench-platform-v2/evolve_reports/compare_CREST15_DEFAULT_vs_CREST15_CLUSTER_ARBITRATION/case_deltas.csv`
- `docs/crest_evolve/compare_CREST15_DEFAULT_vs_CREST15_CLUSTER_ARBITRATION.md`
