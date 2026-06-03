# EvidRank-ARC Compare ARC_BASELINE vs ARC_67

- Created: 2026-06-03T12:41:23+08:00
- Old: `ARC_BASELINE`
- New: `ARC_67`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.670886 | 0.670886 | 0.000000 |
| AC@3 | 0.925457 | 0.925457 | 0.000000 |
| AC@5 | 0.973980 | 0.973980 | 0.000000 |
| MRR | 0.801983 | 0.801983 | 0.000000 |

## Status Counts

| status | cases |
| --- | ---: |
| unchanged | 1422 |

## Important Case Deltas

No important case deltas.

## Decision Notes

- Accept `ARC_67` as the final named ARC baseline behavior.
- There are no metric deltas and no case-level deltas versus the equivalent pre-rename baseline; all 1422 cases are unchanged.
- This confirms the current output did not drift after the rejected no-topology ablation.
