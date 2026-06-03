# EvidenceRank Compare FW_NUMERIC_BASELINE vs FW_PRIORITY_PRIOR

- Created: 2026-06-03T23:18:30+08:00
- Old: `FW_NUMERIC_BASELINE`
- New: `FW_PRIORITY_PRIOR`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.802391 | 0.800985 | -0.001406 |
| AC@3 | 0.943741 | 0.942335 | -0.001406 |
| AC@5 | 0.975387 | 0.975387 | 0.000000 |
| MRR | 0.875337 | 0.874517 | -0.000820 |

## Status Counts

| status | cases |
| --- | ---: |
| rank_regressed | 2 |
| regressed_from_hit1 | 2 |
| unchanged | 1418 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts6-ts-basic-service-response-replace-code-s7bcv7 | rank_regressed | 3 | 4 | -1.0 | ts-basic-service;ts-price-service | ts-seat-service|ts-payment-service|ts-inside-payment-service|ts-basic-service|ts-order-service | response-replace-code | ts-basic-service |
| ts7-ts-ui-dashboard-response-replace-code-t7vsbl | rank_regressed | 3 | 4 | -1.0 | ts-travel-service;ts-ui-dashboard | ts-cancel-service|ts-payment-service|ts-inside-payment-service|ts-ui-dashboard|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts2-ts-basic-service-response-replace-code-rmprwq | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-route-service | ts-travel-service|ts-basic-service|ts-route-plan-service|ts-travel2-service|ts-station-service | response-replace-code | ts-basic-service |
| ts4-ts-basic-service-request-replace-method-hpv2qg | regressed_from_hit1 | 1 | 2 | -1.0 | ts-basic-service;ts-price-service | ts-order-service|ts-basic-service|ts-ui-dashboard|ts-payment-service|ts-travel2-service | request-replace-method | ts-basic-service |

## Decision Notes

- Decision: accept as an optional SRE-priority representation of the existing prior, not as an accuracy-improving ranking change.
- Validation result: the priority prior is nearly behavior-preserving. It loses 2 top-1 hits and 2 top-3 hits out of 1422 cases; AC@5 is unchanged and MRR drops only `0.000820`.
- The two `regressed_from_hit1` cases are both one-rank drops in protocol mutation scenarios. The likely generic mechanism is not a new failure mode, but the removal of the old feature-specific near-baseline value for `trace_count_drop_shift`; mapping that feature to `BASELINE` makes the prior cleaner while slightly changing close score margins.
- General mechanism supported: EvidenceRank can describe its feature prior as ordinal SRE evidence types and use a shared priority-to-weight calibration ladder. This avoids a feature-by-feature numeric table while preserving almost all ranking behavior.
- Caveat: if the default line must maximize AC@1/MRR with no tolerance for a tiny loss, keep the numeric baseline or introduce a near-baseline priority level. The latter would recover more exact behavior but weakens the simplicity of the SRE-priority story.
