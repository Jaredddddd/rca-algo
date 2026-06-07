# CREST8 Iteration

## Goal

Move CREST beyond the current verified `AC@1 ~= 0.80` plateau toward
`AC@1 >= 0.85` without using CERA / EvidenceRank scoring logic, manual feature
priors, labels, injection metadata, historical rankings, or processed
conclusions in the runtime path.

## Version

- Latest CREST number observed in project docs: `CREST7`.
- New version for this round: `CREST8`.
- Target registry name: `crest`.
- Planned ablation registry: `crest_noresidual`.

## Constraints

- Runtime CREST reads only raw normal/abnormal metric, trace, and log frames
  under `args.input_folder`.
- Runtime CREST must not read labels, injection metadata, previous outputs, perf
  reports, historical rankings, ground truth, or `conclusion.parquet`.
- Do not inspect, copy, or adapt CERA / EvidenceRank scoring logic or hand-made
  feature weights. Existing CREST imports from `cera.py` are treated only as raw
  I/O / feature-matrix helper technical debt.
- Do not hardcode datapack ids, service names, fault names, dataset splits, or
  case-specific rules.
- Any new mechanism must be explainable as a cross-system RCA operation.

## Baseline Status

Baseline must be verified before accepting CREST8.

Planned baseline procedure:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST7_BASELINE --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST7_BASELINE --source CREST7_BASELINE --algorithm crest --dataset rcabench
```

If the current output is not a reliable `crest` baseline, rerun:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

Verified baseline snapshot:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST7_BASELINE --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST7_BASELINE --source CREST7_BASELINE --algorithm crest --dataset rcabench
```

Baseline metrics:

| version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CREST7_BASELINE | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

Baseline summary mirrored to
`docs/crest_evolve/CREST7_BASELINE_summary.md`.

## Failure Mechanism

Current CREST already separates local abnormality, topology-conditioned
counterfactual support, and a denoised support channel. The remaining hard
misses are expected to include weakly observable roots, local pod or
infrastructure failures, and low-traffic/drop roots whose own telemetry is
smaller than the downstream services accumulating duration, count, or log
symptoms.

The suspected failure is that the current explain-away step transfers score
between directly adjacent services but still scores the final candidate mostly
from its own adjusted structural energy. A high-observability victim can remain
dominant when it is only partially explainable by several weaker neighbors, or
when a root explains a broad local neighborhood without having the largest
single pairwise transfer.

Offline case inspection supports this mechanism:

- Pod/local failures can have strong metric-shift evidence but no trace/log
  presence, leaving `F` and `S` much lower than high-traffic victims.
- High-observability entry or downstream services often saturate all current
  channels (`A`, `F`, and `S`), even when their evidence is propagation-heavy.
- Multi-root bandwidth and response-mutation cases still expose business roots
  in top-20, but propagation services dominate top-5 through trace/log mass.

## Hypothesis

Add a CREST-owned residual explainability channel:

```text
R(r) = incident-local reduction in neighborhood residual symptom mass if r is
       treated as the local root explanation.
```

For each candidate service, estimate how much propagation-heavy neighbor
symptom mass is explainable from the candidate's root-like local mutation,
drop, or API-change evidence and directed trace proximity. Rank support should
increase when removing that explainable mass leaves less residual anomaly in
the local graph. Victim services are not given a fixed penalty; they are only
suppressed when another structurally connected candidate can explain their
propagation symptoms better.

## Implemented Module

Added `algorithms/evidencerank/src/evidencerank/crest_residual.py` with helper
functions owned by CREST:

- build incident-local root evidence and propagation symptom vectors from the
  already normalized CREST role matrix;
- construct directed/undirected trace neighborhoods from raw trace edges;
- compute residual-reduction support by bounded explainable mass transfer;
- return a saturated incident-local `R` vector.

It was first integrated into `crest.py` as:

```text
score(v) = A(v) * F(v) + S(v) + R(v)
```

The addition is intentionally rank-statistical and incident-local rather than a
manual feature-weight table. Feature sets may use CREST role semantics already
present in `crest.py`, but not EvidenceRank/CERA priority ladders.

After full eval, this integration was rejected and default `crest` was restored
to:

```text
score(v) = A(v) * F(v) + S(v)
```

The residual module is retained only as explicit ablation `crest_residual`.
`crest_noresidual` is also registered as a default-path alias for verification.

## Validation Plan

1. Snapshot and summarize current baseline output, or rerun full baseline if
   current output is stale.
2. Use false-case summaries and a small number of case reports only for offline
   failure analysis; convert observations into general mechanisms.
3. Run guard and compile:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py
```

4. Run full eval for default and ablation:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_noresidual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

5. Snapshot, summarize, compare:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST8 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST8 --source CREST8 --algorithm crest --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST7_BASELINE --new CREST8 --algorithm crest --dataset rcabench
```

Mirror generated CREST markdown into `docs/crest_evolve/`.

## Acceptance Criteria

- `guard` has no high-risk overfitting warning.
- Full eval finishes with `total=1422` and `error=0`.
- Preferred acceptance: `AC@1 >= 0.85`.
- Intermediate acceptance: `AC@1` or `MRR` improves over baseline, `AC@3` and
  `AC@5` do not show unexplained large regressions, and the compare report
  identifies coherent improved/regressed mechanisms.
- Ablation `crest_noresidual` must show whether the residual channel adds real
  value over the previous scoring path.
- Reject or keep as a negative record if the residual channel mostly promotes
  propagation victims or degrades hard groups without a clear explanation.

## Questions Each Candidate Must Answer

1. Current failure mechanism: high-observability victims can retain top score
   when weak roots explain neighborhood symptoms only diffusely.
2. Why current CREST misses: pairwise explain-away is local and the final score
   does not directly measure remaining residual symptom mass.
3. Why transferable: residual reduction uses only raw telemetry roles and trace
   topology, not service/fault names.
4. Avoids CERA/EvidenceRank priors: no external scoring, no manual feature
   priority ladder, no label-derived selector.
5. Likely improvements: weak roots, local pod failures, drop/availability
   roots with strong downstream symptoms.
6. Likely regressions: true roots that are also high-observability victims, or
   sparse traces where neighborhood explainability is underdetermined.
7. Minimal code location: new `crest_residual.py`, small integration in
   `crest.py`, and registry import in `main.py`.
8. Ablation: `crest_noresidual`.
9. If below target: next round should improve confidence gating for when
   residual support is allowed to influence the top candidate.

## Code Changes

- Added `algorithms/evidencerank/src/evidencerank/crest_residual.py`.
- Added optional `R` residual support output to `score_crest_services(...)`.
- Added registry entries:
  - `crest_residual`: rejected residual experiment;
  - `crest_noresidual`: default no-residual path.
- Restored default `crest` to no residual after full eval showed severe
  regression.

## Verification

Commands run:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/src/evidencerank/crest_residual.py algorithms/evidencerank/main.py

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_noresidual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest -a crest_residual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

Guard result: no high-risk overfitting warnings. The only warnings were existing
medium `rcabench_platform` import / docstring literals.

Final metrics:

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| CREST7_BASELINE / `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | baseline |
| CREST8_REJECTED / residual as default | 1422 | 0 | 0.340366 | 0.439628 | 0.447257 | 0.530942 | reject |
| CREST8_NORESIDUAL / `crest_noresidual` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | confirms old path |
| CREST8_DEFAULT / restored `crest` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | keep default |
| CREST8_RESIDUAL / `crest_residual` | 1422 | 0 | 0.340366 | 0.439628 | 0.447257 | 0.530942 | rejected ablation |

Artifacts:

- `docs/crest_evolve/CREST7_BASELINE_summary.md`
- `docs/crest_evolve/CREST8_REJECTED_summary.md`
- `docs/crest_evolve/CREST8_NORESIDUAL_summary.md`
- `docs/crest_evolve/CREST8_DEFAULT_summary.md`
- `docs/crest_evolve/CREST8_RESIDUAL_summary.md`
- `docs/crest_evolve/compare_CREST7_BASELINE_vs_CREST8_REJECTED.md`
- `docs/crest_evolve/compare_CREST7_BASELINE_vs_CREST8_DEFAULT.md`

## Result Analysis

The residual channel had real rescue signal but no reliable confidence boundary:

- `CREST8_REJECTED` improved 45 cases to hit@1.
- It also regressed 699 previous hit@1 cases.
- Top-1 collapses were caused by symptom-light auxiliary services, load
  generators, and low-propagation nodes receiving high residual support without
  enough evidence that they were structurally responsible.

The failure mechanism is therefore more specific than the initial hypothesis:
residual reduction cannot be a free additive score. It must be gated by a
confidence objective that distinguishes "weak root with sparse observability"
from "quiet bystander with metric drift." The noresidual ablation exactly
matches the baseline, so the regression is isolated to `R`.

## Decision

Reject residual as part of default `crest`.

Keep `crest_residual` as a negative ablation and diagnostic artifact. Default
`crest` remains the verified no-residual implementation at `AC@1=0.800281`.

## Next Step

The next round should not add more residual mass. It should learn or derive a
label-free confidence gate for residual eligibility, using only raw incident
telemetry. A promising minimal direction is:

```text
Before any weak-root residual support can affect rank, require agreement
between the candidate's sparse root evidence and a structural absence pattern:
its trace/log silence must coincide with neighbor symptoms that are newly
introduced in the abnormal window, not with background low-traffic metric drift.
```
