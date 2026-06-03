# EvidenceRank Compare ARC2 vs ARC3

- Created: 2026-06-03T18:05:07+08:00
- Old: `ARC2`
- New: `ARC3`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.720113 | 0.720113 | 0.000000 |
| AC@3 | 0.940928 | 0.940928 | 0.000000 |
| AC@5 | 0.973277 | 0.973277 | 0.000000 |
| MRR | 0.832050 | 0.832050 | 0.000000 |

## Status Counts

| status | cases |
| --- | ---: |
| unchanged | 1422 |

## Important Case Deltas

No important case deltas.

## Decision Notes

- Accept ARC3 as the current EvidRank-ARC line.
- ARC3 has zero metric delta and zero case-level rank delta relative to ARC2: all 1422 cases are unchanged.
- The reason to accept ARC3 is methodological, not metric gain: it removes explicit global blend constants and derives the correction strength from active evidence-family count.
- No `regressed_from_hit1` cases were introduced relative to ARC2.
