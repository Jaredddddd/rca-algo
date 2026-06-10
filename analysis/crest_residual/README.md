# CREST-Residual Experiment

CREST-Residual adds a conservative incident-level residual explanatory signal to
CREST. For each candidate root service, it estimates how much abnormal evidence
could be explained by the candidate's mutation evidence flowing over the
directed trace topology.

The default algorithm name is `crest_residual`. The original `crest` algorithm
is unchanged.

## Method

CREST uses `score = A * F + S`, where `A` is incident-local abnormality, `F` is
structural explanatory power, and `S` is denoised structural support.

CREST-Residual computes normalized mutation evidence `M`, propagation evidence
`P`, directed topology influence `K`, and residual explanatory power `R`. It
then only fills missing structural power:

```text
F_residual = F + eta * M * max(0, R - F)
score_residual = A * F_residual + S
```

The default `eta` is `1.0`. No ground truth, injection metadata, trained model,
or generated counterfactual telemetry is used by the scoring path.

The accepted variant also adds a narrow residual-qualified arbitration step. It
only acts inside the current CREST top-5 when a challenger is in a very tight
score near-tie, has better mutation rank than the current winner, has no larger
propagation burden, has non-weaker `F`, and is top-3 by residual explanatory
eligibility. This keeps residual evidence as a gate for mutation ownership
rather than a broad additive bonus.

## Reproduction

Run the benchmark from the repository root:

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a crest_residual -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python analysis/crest_residual/analyze_residual_results.py
```

The analysis script uses existing paired outputs for:

- `crest`
- `crest_residual`
- `crest_local`
- `crest_nocf`
- `crest_metric_trace`
- `crest_trace`
- `cera`

## Outputs

- `analysis/crest_residual/output/residual_summary.csv`
- `analysis/crest_residual/output/residual_summary.md`
- `analysis/crest_residual/output/residual_vs_crest_significance.csv`
- `analysis/crest_residual/output/residual_eta_sensitivity.csv`
- `analysis/crest_residual/output/residual_case_studies.md`
- `analysis/crest_residual/diagnostics/crest_residual_scores.parquet`

Per-case diagnostics are also written under each benchmark output directory as:

```text
output/rcabench-platform-v2/data/rcabench/<datapack>/crest_residual/crest_residual_diagnostics.parquet
```

## Limitations

The residual signal is deliberately conservative. Raw `R` is usually smaller
than existing CREST `F`, so direct residual score addition is ineffective. The
arbitration step protects against the older failure mode where residual support
became a broad bonus for quiet bystanders or topology-central victims, but the
observed gain is intentionally small.
