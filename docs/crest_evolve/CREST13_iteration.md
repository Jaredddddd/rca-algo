# CREST13 Iteration

## Goal

Continue toward `AC@1 >= 0.85` for `crest` on `rcabench` while keeping runtime
CREST raw-only, label-free, cross-system explainable, and independent of CERA /
EvidenceRank scoring logic or hand-written priors.

## Version

- Latest completed CREST iteration: `CREST12`.
- New version for this round: `CREST13`.
- Baseline for comparison: `CREST10_DEFAULT` / current default `crest`.

## Baseline

Verified default:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST10_DEFAULT / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

CREST11 and CREST12 showed that blind fusion over compressed `A/F/S` views or
broad role families does not safely recover enough misses. The next hypothesis
therefore tested a more specific raw trace signal for protocol mutation faults.

## Hypothesis

For request/response protocol mutations, the service that owns the abnormal
server-side protocol distribution may be a better challenger than the current
CREST winner:

```text
Within the current default top-k, promote the service with the strongest
server-span protocol drift only when that raw drift clearly dominates the
default winner.
```

The signal is raw-only:

- restrict traces to server spans;
- compare normal and abnormal per-service distributions;
- use total-variation drift for span name, request method, response status, and
  status code;
- require both normal and abnormal support to avoid treating missing services
  as protocol owners.

Labels were used only offline to score the proposed rerank.

## Offline Results

Analysis artifacts:

- `output/rcabench-platform-v2/evolve_reports/CREST13_server_protocol_offline_scores.csv`
- `output/rcabench-platform-v2/evolve_reports/CREST13_server_protocol_offline_summary.csv`

Summary:

| formula | AC@1 | improved_to_hit1 | regressed_from_hit1 | switches | net_hit1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| default | 0.800281 | 0 | 0 | 0 | 0 |
| top5_status_gate125 | 0.704641 | 123 | 259 | 428 | -136 |
| top3_status_gate125 | 0.703938 | 108 | 245 | 394 | -137 |
| top3_status_protocol | 0.688467 | 125 | 284 | 469 | -159 |
| top5_status_protocol | 0.687060 | 142 | 303 | 512 | -161 |
| top3_server_protocol_gate125 | 0.578059 | 103 | 419 | 606 | -316 |
| top3_server_protocol | 0.548523 | 119 | 477 | 711 | -358 |

The protocol score contains rescue signal, but it is not ownership-specific
enough. Server-side protocol drift often appears at symptom surfaces, relays, or
entry services. Reranking by it regresses far more already-correct cases than it
fixes.

## Decision

Reject `crest_server_protocol` / protocol ownership reranking. Do not implement
runtime code for CREST13.

The useful lesson is that a new raw signal is not enough by itself. It must be
paired with a strong root-victim eligibility predicate before it can change
top-1.

## Next Step

Move to CREST14: test a much narrower top-3 arbitration rule. A challenger may
replace the default winner only when it is already a near tie, has substantially
stronger trace mutation burden, and has substantially lower propagation burden.
