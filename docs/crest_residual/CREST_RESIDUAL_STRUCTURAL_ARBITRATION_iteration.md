# CREST-Residual Structural Arbitration Iteration

## Goal

Raise `crest_residual` to `AC@1 >= 0.82` while keeping the runtime path
label-free, raw-telemetry based, and free of service/datapack/fault hardcoding.

## Baseline

Previous accepted residual package:

| version | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: |
| CREST_RESIDUAL_ARBITRATION_PRE_STRUCTURAL | 0.803094 | 0.876849 | 0.944444 | 0.971871 |

Residual-only offline search over `A/F/S/M/P/R` could not reach the target.
The best broad scalar/rank variants stayed near `AC@1 ~= 0.8066` and introduced
many hit@1 regressions, confirming that residual must be paired with raw
trace-structure eligibility rather than used as a free reranker.

## Mechanism

`crest_residual` now keeps the original conservative residual gate and adds two
structural arbitration stages:

1. Incoming symptom-cluster arbitration:
   - candidate remains in the top-5 score plateau;
   - candidate has stronger trace mutation and no higher propagation than the
     current winner;
   - candidate explains at least two incoming caller symptom surfaces.
2. Protocol/fan-in arbitration:
   - candidate remains in a stricter top-5 score plateau;
   - candidate has stronger server-side protocol/path drift, higher fan-in, and
     higher observability volume than the current winner;
   - candidate's propagation burden is bounded relative to the winner.

Both stages only bump one near-tie challenger above the current winner. They do
not add a global residual score, feature-weight replacement, service-specific
branch, or fault-specific branch.

## Code Change

Changed `algorithms/evidencerank/src/evidencerank/crest.py`:

- export role-family burdens and residual arbitration markers in diagnostics;
- compute raw trace server protocol/path distribution drift from normal vs
  abnormal traces;
- compute incoming/outgoing trace neighbor counts and incoming caller symptom
  explainability from raw trace edges;
- replace the single residual arbitration call with three staged arbitrators:
  residual mutation ownership, incoming symptom cluster, and protocol/fan-in.

`crest` default behavior remains unchanged; the new logic is opt-in through
`CRESTResidual`.

## Verification

Commands run:

```bash
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py analysis/crest_residual/analyze_residual_results.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest_residual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python analysis/crest_residual/analyze_residual_results.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST_RESIDUAL_STRUCTURAL_ARBITRATION --algorithm crest_residual --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST_RESIDUAL_STRUCTURAL_ARBITRATION --source CREST_RESIDUAL_STRUCTURAL_ARBITRATION --algorithm crest_residual --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST_RESIDUAL_ARBITRATION_PRE_STRUCTURAL --new CREST_RESIDUAL_STRUCTURAL_ARBITRATION --algorithm crest_residual --dataset rcabench
```

`guard` reported no high-risk overfitting warnings.

## Results

| version / algorithm | total | error | AC@1 | MRR | AC@3 | AC@5 | runtime.avg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| previous `crest_residual` | 1422 | 0 | 0.803094 | 0.876849 | 0.944444 | 0.971871 | 8.688498s |
| structural `crest_residual` | 1422 | 0 | 0.822785 | 0.887046 | 0.944444 | 0.971871 | 11.053631s |
| `crest` baseline | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 | 9.973219s |

Against the previous residual snapshot:

| status | cases |
| --- | ---: |
| improved_to_hit1 | 28 |
| regressed_from_hit1 | 0 |
| rank_regressed | 3 |
| unchanged | 1391 |

Arbitration diagnostics in the accepted run:

| marker | cases |
| --- | ---: |
| residual_arbitrated | 6 |
| residual_cluster_arbitrated | 22 |
| residual_path_fanin_arbitrated | 14 |

Paired bootstrap from `analysis/crest_residual/analyze_residual_results.py`
against `crest`:

- AC@1 delta: `+0.022504`, 95% CI `[+0.014768, +0.030257]`,
  `prob_delta_gt_0=1.000`.
- MRR delta: `+0.011721`, 95% CI `[+0.007793, +0.015706]`,
  `prob_delta_gt_0=1.000`.

## Decision

Accept `CREST_RESIDUAL_STRUCTURAL_ARBITRATION` as the current `crest_residual`
package. It reaches the requested `AC@1 >= 0.82`, improves MRR, preserves
AC@3/AC@5, has no hit@1 regressions against the previous residual snapshot, and
keeps runtime evidence restricted to raw telemetry.

## Remaining Risk

The path/fan-in stage uses strict named eligibility constants for score plateau
and propagation slack. They are not feature weights, but they should be
presented as safety guards rather than learned causal parameters. Future work
can replace them with a fully case-local plateau estimator if it can preserve
the same zero hit@1 regression profile.
