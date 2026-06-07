# EvidenceRank Compare CREST15_DEFAULT vs CREST15_ACCEPTED

- Created: 2026-06-07T23:07:05+08:00
- Old: `CREST15_DEFAULT`
- New: `CREST15_ACCEPTED`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800281 | 0.812940 | 0.012658 |
| AC@3 | 0.944444 | 0.945148 | 0.000703 |
| AC@5 | 0.971871 | 0.971871 | 0.000000 |
| MRR | 0.875326 | 0.882065 | 0.006739 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 18 |
| unchanged | 1404 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-method-99j798 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-preserve-service|ts-travel-service|ts-travel2-service|ts-route-service | request-replace-method | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-r727qm | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-station-service|ts-travel2-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-seat-service-response-replace-code-4mpcv7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-seat-service |
| ts1-ts-basic-service-request-replace-method-2b57wf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-travel-plan-service|ts-station-food-service | request-replace-method | ts-basic-service |
| ts1-ts-seat-service-request-replace-path-jmcntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-inside-payment-service|ts-order-other-service|ts-travel-plan-service | request-replace-path | ts-seat-service |
| ts1-ts-seat-service-response-replace-code-dk84t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-order-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-seat-service |
| ts1-ts-travel-service-response-replace-code-qzmhjf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-station-service | response-replace-code | ts-travel-service |
| ts2-ts-basic-service-response-replace-code-92j5cs | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts2-ts-travel-service-response-abort-jd66zv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-contacts-service|ts-route-plan-service|ts-travel-plan-service | response-abort | ts-travel-service |
| ts2-ts-travel2-service-response-replace-code-ttpn92 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-price-service|ts-basic-service | response-replace-code | ts-travel2-service |
| ts3-ts-basic-service-response-replace-code-bvqv9z | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel2-service|ts-travel-service|ts-route-plan-service|ts-station-service | response-replace-code | ts-basic-service |
| ts3-ts-route-plan-service-request-replace-path-m56fgf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-verification-code-service|ts-travel-service|ts-ui-dashboard | request-replace-path | ts-route-plan-service |
| ts3-ts-seat-service-response-replace-code-xdw4c7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service | response-replace-code | ts-seat-service |
| ts3-ts-travel-service-request-replace-path-vktk7x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel-service | ts-travel-service|ts-food-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard | request-replace-path | ts-travel-service |
| ts9-ts-route-plan-service-request-replace-path-9dg8qf | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-payment-service|ts-consign-service|ts-travel-plan-service|ts-seat-service | request-replace-path | ts-route-plan-service |
| ts2-ts-basic-service-response-replace-code-qf2qml | improved_to_hit1 | 3 | 1 | 2.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-station-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts3-ts-seat-service-response-replace-code-cfcfbf | improved_to_hit1 | 3 | 1 | 2.0 | ts-config-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service | response-replace-code | ts-seat-service |
| ts2-ts-order-other-service-container-kill-48rlds | improved_to_hit1 | 4 | 1 | 3.0 | ts-order-other-service | ts-order-other-service|ts-seat-service|ts-preserve-service|ts-travel2-service|ts-basic-service | container-kill | ts-order-other-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
