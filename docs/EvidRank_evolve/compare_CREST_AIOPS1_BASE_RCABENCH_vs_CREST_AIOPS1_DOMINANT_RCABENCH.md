# EvidenceRank Compare CREST_AIOPS1_BASE_RCABENCH vs CREST_AIOPS1_DOMINANT_RCABENCH

- Created: 2026-06-08T21:05:43+08:00
- Old: `CREST_AIOPS1_BASE_RCABENCH`
- New: `CREST_AIOPS1_DOMINANT_RCABENCH`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.801688 | 0.001406 |
| AC@3 | 0.944444 | 0.944444 | 0.000000 |
| AC@5 | 0.971871 | 0.971871 | 0.000000 |
| MRR | 0.875326 | 0.876029 | 0.000703 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 2 |
| unchanged | 1420 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-travel-service-request-abort-g9mc2t | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-voucher-service|ts-route-plan-service|ts-delivery-service|ts-travel-plan-service | request-abort | ts-travel-service |
| ts2-ts-basic-service-request-replace-method-v6gzn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-station-service|ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-travel2-service | request-replace-method | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
