# CREST17 Iteration

## Goal

Continue from accepted CREST15 default toward `AC@1 >= 0.85` for `crest` on
`rcabench`, preserving raw-only, label-free, cross-system deployability and
avoiding CERA / EvidenceRank scoring logic or manual priors.

## Version

- Latest completed CREST iteration: `CREST16`.
- New version for this round: `CREST17`.
- Baseline for comparison: `CREST15_ACCEPTED`.

## Baseline

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST15_ACCEPTED / `crest` | 1422 | 0 | 0.812940 | 0.882065 | 0.945148 | 0.971871 |

## Hypothesis Space

CREST16 rejected another scalar protocol gate. CREST17 will first profile the
remaining accepted-default misses and only then pick one mechanism. Candidate
directions:

- request-path-consistent caller clusters;
- multi-root preservation when one GT-like infrastructure/business partner is
  already high in the ranking;
- local missing/availability evidence for low-observability roots;
- stricter root-victim assignment within accepted top-3/top-5.

## Offline Analysis Plan

Use labels only to profile misses and score offline variants. Do not read
labels, injection metadata, previous outputs, perf reports, or
`conclusion.parquet` in runtime code. Evaluate only raw-trace/metric/log
mechanisms that can be expressed without service, datapack, or fault-name rules.

## Acceptance Criteria

- `guard` reports no high-risk overfitting warnings.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred: `AC@1 >= 0.85`.
- Intermediate acceptance: improves AC@1 or MRR over CREST15 with no
  unexplained AC@3/AC@5 regression and a coherent general mechanism.
- Reject if the candidate is just a label-shaped top-k rerank.

## Offline Profiling Results

Accepted-default candidate features were rebuilt by merging the raw-derived
CREST15/CREST16 offline role table with the verified `CREST15_ACCEPTED`
snapshot ranks:

- `output/rcabench-platform-v2/evolve_reports/CREST17_accepted_candidate_features.csv`
- `output/rcabench-platform-v2/evolve_reports/CREST17_top1_bestgt_pairs.csv`
- `output/rcabench-platform-v2/evolve_reports/CREST17_simple_rule_search.csv`

The current accepted baseline had 266 top-1 misses. Among them, the best GT was
rank 2 in 135 cases, rank 3 in 53 cases, rank 4 in 27 cases, and rank 5 in 11
cases.

Simple broad gates were unsafe. The best observability-only family reached
offline `AC@1 ~= 0.833333` but regressed 30 accepted hit@1 cases. The usable
mechanism was narrower:

```text
top-3 near-tie challenger
+ higher server method/span distribution drift
+ higher observability volume
+ at least one more incoming caller than the current winner
+ propagation burden no more than 1.4x the winner
```

This is a structural path/fan-in arbitration gate, not a scalar protocol rerank.
It only fires when protocol/path drift is accompanied by broader incoming
request exposure and does not look substantially more propagation-heavy than
the current winner.

## Code Change

Implemented `crest_path_fanin_arbitration` in
`algorithms/evidencerank/src/evidencerank/crest.py` and registered it in
`algorithms/evidencerank/main.py`.

Runtime additions:

- raw server-span method/span total-variation drift from normal vs abnormal
  traces;
- top-3 near-tie path/fan-in arbitration after CREST15 cluster arbitration and
  CREST14 mutation arbitration;
- diagnostic output column `P` for the path/fan-in arbitration bump.

No runtime path reads labels, injection metadata, previous output, perf report,
historical ranking, or `conclusion.parquet`. The new signal uses only raw trace
frames plus the CREST role matrix already built from raw telemetry.

## Verification

Commands run:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_path_fanin_arbitration -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST17_ACCEPTED --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST17_ACCEPTED --source CREST17_ACCEPTED --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST15_ACCEPTED --new CREST17_ACCEPTED --algorithm crest --dataset rcabench
```

`guard` reported no high-risk overfitting warnings. Compile passed.

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST15_ACCEPTED / old `crest` | 1422 | 0 | 0.812940 | 0.882065 | 0.945148 | 0.971871 | 9.211219s |
| CREST17_PATH_FANIN / `crest_path_fanin_arbitration` | 1422 | 0 | 0.825598 | 0.888980 | 0.945148 | 0.971871 | 11.869161s |
| CREST17_ACCEPTED / promoted `crest` | 1422 | 0 | 0.825598 | 0.888980 | 0.945148 | 0.971871 | 11.735005s |

Compare against `CREST15_ACCEPTED`:

| status | cases |
| --- | ---: |
| improved_to_hit1 | 18 |
| rank_regressed | 1 |
| unchanged | 1403 |

There were no `regressed_from_hit1` cases. The single `rank_regressed` case was
`ts0-ts-seat-service-pod-failure-c87xdg`, whose GT moved from rank 2 to rank 3;
top-1 was already false before and remains false after.

Artifacts:

- [CREST17_ACCEPTED_summary.md](CREST17_ACCEPTED_summary.md)
- [CREST17_PATH_FANIN_summary.md](CREST17_PATH_FANIN_summary.md)
- [compare_CREST15_ACCEPTED_vs_CREST17_ACCEPTED.md](compare_CREST15_ACCEPTED_vs_CREST17_ACCEPTED.md)
- [compare_CREST15_ACCEPTED_vs_CREST17_PATH_FANIN.md](compare_CREST15_ACCEPTED_vs_CREST17_PATH_FANIN.md)

## Decision

Accept CREST17 and promote the path/fan-in arbitration into default `crest`.
The goal is still not complete because verified `AC@1=0.825598` is below
`0.85`.

The accepted mechanism preserves the CREST13/CREST16 lesson: protocol/path
drift is unsafe as a standalone ranking signal, but becomes useful when it is
restricted to a near-tie candidate with broader incoming request exposure and
bounded propagation burden.

## Next Step

The remaining weak groups are still pod-failure, low-observability roots, and
some top-5 misses where the root is not a near-tie path owner. CREST18 should
avoid broad protocol gates and instead target weak availability/drop roots with
a structural mechanism that can distinguish missing local root evidence from
high-observability victims.
