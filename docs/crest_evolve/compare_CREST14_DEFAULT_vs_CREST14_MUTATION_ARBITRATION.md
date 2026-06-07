# Compare CREST14_DEFAULT vs CREST14_MUTATION_ARBITRATION

## Metrics

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST14_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 8.903303s |
| CREST14_MUTATION_ARBITRATION / `crest_mutation_arbitration` | 1422 | 0 | 0.803094 | 0.876849 | 0.944444 | 0.971871 | 8.928790s |

## Delta Summary

- `improved_to_hit1`: 4
- `regressed_from_hit1`: 0
- `top1_changed`: 6
- `rank_improved`: 4
- `rank_regressed`: 0
- `AC@1` delta: +0.002813
- `MRR` delta: +0.001524

## Top-1 Switches

| datapack | fault_type | gt | old top1 | new top1 | old rank | new rank | hit@1 delta |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| ts2-ts-basic-service-response-replace-code-qf2qml | response-replace-code | ts-basic-service;ts-price-service | ts-travel-service | ts-basic-service | 3 | 1 | improved |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | response-replace-code | ts-order-service;ts-seat-service | ts-travel-service | ts-seat-service | 2 | 1 | improved |
| ts3-ts-route-plan-service-request-replace-path-m56fgf | request-replace-path | ts-route-plan-service;ts-travel-service | ts-travel-plan-service | ts-route-plan-service | 2 | 1 | improved |
| ts9-ts-route-plan-service-request-replace-path-9dg8qf | request-replace-path | ts-route-plan-service;ts-travel-service | ts-payment-service | ts-route-plan-service | 2 | 1 | improved |
| ts4-ts-basic-service-response-replace-code-7tlb8z | response-replace-code | ts-basic-service;ts-price-service | ts-inside-payment-service | ts-route-plan-service | 5 | 5 | unchanged miss |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | request-replace-method | ts-travel-plan-service;ts-ui-dashboard | ts-payment-service | ts-consign-service | 8 | 8 | unchanged miss |

## Fault-Type Switch Summary

| fault_type | switches | improved_to_hit1 | regressed_from_hit1 | avg_mrr_delta |
| --- | ---: | ---: | ---: | ---: |
| response-replace-code | 3 | 2 | 0 | +0.388889 |
| request-replace-path | 2 | 2 | 0 | +0.500000 |
| request-replace-method | 1 | 0 | 0 | +0.000000 |

## Decision

CREST14 mutation arbitration is a small positive ablation. It improves AC@1 and MRR without changing AC@3/AC@5 and without regressing any previous hit@1 case in the full evaluation. It still falls far short of the target `AC@1 >= 0.85`, so it should be treated as an intermediate CREST-family variant rather than proof that the goal is solved.

## Artifacts

- `output/rcabench-platform-v2/evolve_reports/compare_CREST14_DEFAULT_vs_CREST14_MUTATION_ARBITRATION/case_deltas.csv`
- `docs/crest_evolve/compare_CREST14_DEFAULT_vs_CREST14_MUTATION_ARBITRATION.md`
