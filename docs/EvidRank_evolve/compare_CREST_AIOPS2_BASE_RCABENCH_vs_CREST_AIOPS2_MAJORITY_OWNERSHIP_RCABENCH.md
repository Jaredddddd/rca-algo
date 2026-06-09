# EvidenceRank Compare CREST_AIOPS2_BASE_RCABENCH vs CREST_AIOPS2_MAJORITY_OWNERSHIP_RCABENCH

- Created: 2026-06-08T22:13:57+08:00
- Old: `CREST_AIOPS2_BASE_RCABENCH`
- New: `CREST_AIOPS2_MAJORITY_OWNERSHIP_RCABENCH`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.801688 | 0.802391 | 0.000703 |
| AC@3 | 0.944444 | 0.944444 | 0.000000 |
| AC@5 | 0.971871 | 0.971871 | 0.000000 |
| MRR | 0.876029 | 0.876368 | 0.000339 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 1 |
| rank_regressed | 2 |
| unchanged | 1419 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts1-ts-basic-service-request-replace-method-v627xx | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-service|ts-price-service | request-replace-method | ts-basic-service |
| ts2-ts-ui-dashboard-request-abort-djrhxq | rank_regressed | 2 | 3 | -1.0 | ts-auth-service;ts-ui-dashboard | ts-verification-code-service|loadgenerator|ts-ui-dashboard|ts-auth-service|ts-travel2-service | request-abort | ts-ui-dashboard |
| ts3-ts-basic-service-response-replace-code-ws6vpb | rank_regressed | 7 | 8 | -1.0 | ts-basic-service;ts-station-service | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-verification-code-service | response-replace-code | ts-basic-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
