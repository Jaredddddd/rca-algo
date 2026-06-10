# CREST-Residual Arbitration Iteration

## Motivation

Raw residual explanatory power `R` is usually much smaller than CREST's existing
structural power `F`, so the first `crest_residual` formula mostly tied `crest`.
Directly rank-normalizing or adding `R` caused regressions in offline search.

This iteration keeps residual as an eligibility signal and uses it only for
near-tie mutation ownership arbitration.

## Mechanism

`crest_residual` now keeps the original conservative formula:

```text
F_residual = F + eta * M * max(0, R - F)
score_residual = A * F_residual + S
```

Then it applies a narrow arbitration rule inside the already sorted CREST result:

1. only consider challengers in the current top-5;
2. require the challenger to be in a very tight near-tie, where the score gap is
   no larger than the case-local 25th percentile of positive adjacent score
   gaps;
3. require better mutation evidence rank than the current winner;
4. require no larger propagation burden than the current winner;
5. require non-weaker original `F`;
6. require top-3 case-local residual explanatory eligibility.

This turns residual from a broad additive bonus into a gate for mutation
ownership in ambiguous top-ranked clusters.

## Validation

Commands:

```bash
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py analysis/crest_residual/analyze_residual_results.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest_residual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python analysis/crest_residual/analyze_residual_results.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CREST_RESIDUAL_ARBITRATION --algorithm crest_residual --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CREST_RESIDUAL_ARBITRATION --source CREST_RESIDUAL_ARBITRATION --algorithm crest_residual --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CREST_RESIDUAL_ETA1 --new CREST_RESIDUAL_ARBITRATION --algorithm crest_residual --dataset rcabench
```

Guard result: no high-risk overfitting warnings. The remaining medium warnings
are existing platform import / dataset-name string notices.

## Results

| version | AC@1 | MRR | AC@3 | AC@5 | notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `crest` | 0.800281 | 0.875326 | 0.944444 | 0.971871 | baseline output |
| `CREST_RESIDUAL_ETA1` | 0.800281 | 0.875326 | 0.944444 | 0.971871 | residual formula only |
| `CREST_RESIDUAL_ARBITRATION` | 0.803094 | 0.876849 | 0.944444 | 0.971871 | accepted ablation |

Compared with `CREST_RESIDUAL_ETA1`, the arbitration version has:

- `improved_to_hit1`: 4
- `regressed_from_hit1`: 0
- unchanged: 1418

Paired bootstrap from `analysis/crest_residual/analyze_residual_results.py`:

- `crest_residual` vs `crest`, MRR delta: `+0.001524`, 95% CI
  `[+0.000352, +0.003165]`, empirical `P(delta > 0) = 0.979`.
- `crest_residual` vs `crest`, AC@1 delta: `+0.002813`, 95% CI
  `[+0.000703, +0.005626]`, empirical `P(delta > 0) = 0.976`.

## Improved Cases

The four top-1 improvements are all near-tie request path/method cases where
the original CREST winner had high propagated symptom support but the challenger
had stronger mutation ownership and residual eligibility:

- `ts3-ts-travel-service-request-replace-path-vktk7x`
- `ts3-ts-ui-dashboard-request-replace-method-wkh6t7`
- `ts8-ts-route-plan-service-request-replace-path-xxpxdq`
- `ts9-ts-route-plan-service-request-replace-path-9dg8qf`

## Decision

Accept `crest_residual` as a packaged residual variant, not as a replacement for
the main CREST claim. The improvement is small but clean: it raises AC@1/MRR,
does not change AC@3/AC@5, and has no observed hit@1 regressions on RCABench.

For paper wording, describe the mechanism as residual-qualified near-tie
mutation ownership arbitration, not as direct residual minimization.
