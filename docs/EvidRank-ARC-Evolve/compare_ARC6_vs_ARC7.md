# EvidenceRank Compare ARC6 vs ARC7

- Created: 2026-06-03T21:13:31+08:00
- Old: `ARC6`
- New: `ARC7`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.728551 | 0.728551 | 0.000000 |
| AC@3 | 0.943741 | 0.943741 | 0.000000 |
| AC@5 | 0.973277 | 0.973277 | 0.000000 |
| MRR | 0.836841 | 0.836843 | 0.000002 |

## Status Counts

| status | cases |
| --- | ---: |
| rank_improved | 1 |
| unchanged | 1421 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | rank_improved | 19 | 18 | 1.0 | ts-route-plan-service;ts-travel-plan-service | ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-order-other-service|ts-order-service | bandwidth | ts-route-plan-service |

## Decision Notes

- Accept ARC7. It removes the older directional reranking layer while keeping AC@1, AC@3, and AC@5 unchanged and improving MRR by `+0.000002`.
- There are no regressions relative to ARC6; only one case improves by one rank.
- The result supports the interpretation that final top-neighbor pairwise contrast has absorbed the useful part of the old directional transfer.
