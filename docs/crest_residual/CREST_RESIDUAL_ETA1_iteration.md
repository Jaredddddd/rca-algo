# CREST-Residual ETA1 Iteration

## Goal

Implement and evaluate `crest_residual`, a conservative Counterfactual Evidence
Residual Ranking variant for CREST. The original `crest` algorithm must remain
unchanged.

## Implementation

- Added residual topology influence and residual explanatory power helpers in
  `algorithms/evidencerank/src/evidencerank/crest.py`.
- Added `CRESTResidual` with registry name `crest_residual`.
- Kept `crest` default behavior unchanged by making residual scoring opt-in via
  `residual_eta`.
- Exported per-case diagnostics to
  `crest_residual_diagnostics.parquet`.
- Added `analysis/crest_residual/analyze_residual_results.py` and README.

The residual formula is:

```text
F_residual = F + eta * M * max(0, R - F)
score_residual = A * F_residual + S
```

Default `eta = 1.0`. The residual signal cannot reduce CREST's original `F`,
and it can only fill missing structural power when the candidate has mutation
evidence.

## Commands

```bash
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest_residual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python analysis/crest_residual/analyze_residual_results.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST_RESIDUAL_ETA1 --algorithm crest_residual --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST_RESIDUAL_ETA1 --source CREST_RESIDUAL_ETA1 --algorithm crest_residual --dataset rcabench
```

## Results

| algorithm | total | error | runtime_mean | runtime_median | runtime_p95 | MRR | AC@1 | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| crest_residual | 1422 | 0 | 8.697871 | 8.099498 | 14.597762 | 0.875326 | 0.800281 | 0.944444 | 0.971871 |
| crest | 1422 | 0 | 9.973219 | 9.487427 | 16.347651 | 0.875326 | 0.800281 | 0.944444 | 0.971871 |
| crest_local | 1422 | 0 | 10.557463 | 9.858251 | 19.107231 | 0.824138 | 0.705345 | 0.939522 | 0.967651 |
| crest_nocf | 1422 | 0 | 11.304127 | 10.779583 | 19.590831 | 0.664688 | 0.490155 | 0.815752 | 0.936006 |
| crest_metric_trace | 1422 | 0 | 7.449607 | 7.029971 | 12.242126 | 0.818233 | 0.703235 | 0.932489 | 0.969761 |
| crest_trace | 1422 | 0 | 7.427738 | 7.073958 | 12.719752 | 0.709243 | 0.560478 | 0.836850 | 0.904360 |
| cera | 1422 | 0 | 9.673971 | 9.334153 | 16.201761 | 0.904032 | 0.850211 | 0.950774 | 0.976090 |

The paired bootstrap comparison against `crest` is exactly zero for MRR,
AC@1, AC@3, and AC@5. There are no residual wins and no residual losses over
`crest`.

Eta sensitivity was recomputed from exported diagnostics, not by rerunning the
benchmark. All tested eta values `{0.25, 0.5, 1.0, 2.0}` produce the same
ranking and metrics.

## Interpretation

`crest_residual` is safe but too conservative to improve RCABench. Diagnostics
show that residual explanatory power `R` is usually far below the existing
CREST structural power `F`, so `max(0, R - F)` is zero and the ranking remains
unchanged.

This is preferable to the earlier rejected residual variants that caused large
regressions, but it does not provide evidence for promoting residual scoring to
the main CREST algorithm.

## Decision

Keep `crest_residual` as a reproducible ablation and diagnostic artifact.
Do not promote it as the default CREST ranking path.
