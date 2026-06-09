# EvidenceRank Compare CREST_AIOPS2_MAJORITY_OWNERSHIP_RCABENCH vs CREST_AIOPS2_FINAL_RCABENCH

- Created: 2026-06-09T00:32:23+08:00
- Old: `CREST_AIOPS2_MAJORITY_OWNERSHIP_RCABENCH`
- New: `CREST_AIOPS2_FINAL_RCABENCH`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.803094 | 0.000703 |
| AC@3 | 0.944444 | 0.945148 | 0.000703 |
| AC@5 | 0.971871 | 0.972574 | 0.000703 |
| MRR | 0.876368 | 0.876983 | 0.000615 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 1 |
| unchanged | 1421 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts3-ts-basic-service-response-replace-code-ws6vpb | improved_to_hit1 | 8 | 1 | 7.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard | response-replace-code | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
