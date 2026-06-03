# EvidenceRank Compare FW_PRIORITY_PRIOR vs FW_PRIORITY_SYNTH_LADDER

- Created: 2026-06-04T02:03:28+08:00
- Old: `FW_PRIORITY_PRIOR`
- New: `FW_PRIORITY_SYNTH_LADDER`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.800985 | 0.800985 | 0.000000 |
| AC@3 | 0.942335 | 0.942335 | 0.000000 |
| AC@5 | 0.975387 | 0.975387 | 0.000000 |
| MRR | 0.874517 | 0.874517 | 0.000000 |

## Status Counts

| status | cases |
| --- | ---: |
| unchanged | 1422 |

## Important Case Deltas

No important case deltas.

## Decision Notes

- Accept `FW_PRIORITY_SYNTH_LADDER`.
- There are no `regressed_from_hit1`, `improved_to_hit1`, or rank-delta cases; all `1422` cases are unchanged.
- The accepted mechanism is an implementation/presentation improvement rather than a ranking improvement: feature-level knowledge is now an ordinal `FeaturePriority` prior, and the nonlinear diagnostic severity ladder is synthesized from priority-tier structure instead of maintained as an explicit float table.
