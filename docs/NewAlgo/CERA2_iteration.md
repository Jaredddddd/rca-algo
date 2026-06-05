# CERA2 Iteration

- Created: 2026-06-05
- Algorithm registry name: `cera`
- Dataset: `rcabench`
- Goal: remove hand-crafted heuristic weights from CERA1 and reach `AC@1 >= 0.75` with full eval `error == 0`

## Hypothesis

CERA1 works because robustly scaled evidence burden preserves enough raw incident signal, but it still uses fixed hand-crafted blend constants for role alignment and explain-away. CERA2 should replace those constants with self-supervised, incident-local reliability and role posterior updates derived from family support, concentration, contrast, top gap, and cross-view agreement.

## Hard Constraints

- Runtime CERA must not read labels, injection metadata, previous outputs, perf reports, historical rankings, ground truth, or `conclusion.parquet`.
- Do not hardcode datapack ids, service names, fault names, random suffixes, or dataset splits.
- Do not call `EvidenceRank` or `EvidenceRankARC` for runtime rankings.
- Do not use hand-crafted heuristic blend weights such as `0.10 * root_anchor`, `0.05 * propagation_dominance`, or manually chosen family priority multipliers.
- Uniform mathematical operations are allowed: sums, means, normalized ranks, geometric means, PCA-derived component weights, quantiles, entropy, cosine agreement, softmax, and ratios derived from current incident statistics.

## Planned Mechanism

1. Keep CERA1's robust per-case scaling and semantic family aggregation.
2. Replace fixed role-alignment blend weights with a uniform evidence burden over all active families, including a topology-context family.
3. Derive parent-context strength from the current trace graph density:

```text
context_weight = 1 / (1 + valid_non_self_edges / service_count)
```

4. Replace fixed explain-away transfer constants with counterfactual pair strengths derived from current incident statistics:

```text
transfer = score_excess * mutation_share * propagation_share
```

5. Derive explain-away iteration count from the number of causal-role families, excluding observability-volume and topology-context families.

## Expected Failure Modes

- Pure reliability replacement may repeat the CERA1_RAW problem by over-normalizing family views and losing strong raw evidence.
- Free incident-local reliability can over-trust propagation families when high-traffic victims have the clearest peaks.
- Removing every fixed blend constant may lower AC@1 unless the posterior update derives enough strength from case geometry.

## Validation Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/cera.py algorithms/evidencerank/main.py
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a cera -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CERA2 --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CERA2 --source CERA2 --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CERA1 --new CERA2 --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

Full eval completed on 2026-06-05:

| metric | value |
| --- | ---: |
| total | 1422 |
| error | 0 |
| AC@1 | 0.752461 |
| MRR | 0.842955 |
| AC@3 | 0.926160 |
| AC@5 | 0.961322 |
| runtime.avg | 9.688974s |

Compared with `CERA1`:

| metric | CERA1 | CERA2 | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.691280 | 0.752461 | +0.061181 |
| MRR | 0.814367 | 0.842955 | +0.028588 |
| AC@3 | 0.933193 | 0.926160 | -0.007032 |
| AC@5 | 0.966245 | 0.961322 | -0.004923 |

Status deltas:

| status | cases |
| --- | ---: |
| improved_to_hit1 | 188 |
| regressed_from_hit1 | 101 |
| rank_improved | 74 |
| rank_regressed | 87 |
| unchanged | 972 |

Main improvements are in protocol/request mutation and delay-like cases where CERA1 often ranked the true root second. The largest `improved_to_hit1` groups are `response-replace-code`, `request-replace-method`, `request-delay`, `request-replace-path`, and `stress`.

Main regressions are in topology-heavy or propagation-ambiguous cases such as `partition`, `loss`, and some dashboard/seat/basic-service cases. The top-3/top-5 drops are small but real, which suggests CERA2's counterfactual transfer is better for top-1 separation while slightly sharper than CERA1 for candidate preservation.

Validation artifacts:

- Snapshot: `output/rcabench-platform-v2/evolve_snapshots/CERA2/`
- Summary: `docs/EvidRank_evolve/CERA2_summary.md`
- Compare: `docs/EvidRank_evolve/compare_CERA1_vs_CERA2.md`

Guard result: no high-risk overfitting warnings. The remaining medium warnings are existing `rcabench_platform` import/docstring literals.

## Decision

CERA2 is accepted as the current CERA version because it reaches the requested `AC@1 >= 0.75` target, improves MRR, completes full eval with `error == 0`, and removes CERA1's hand-crafted role-alignment / explain-away blend constants.

The accepted interpretation is:

- semantic feature families are used only as unweighted evidence groups;
- topology context strength is derived from incident trace graph density;
- counterfactual explain-away transfer is derived from current root/victim score gaps and relative mutation/propagation shares;
- iteration count is derived from the number of causal-role families rather than a manually tuned loop count.

Next work should focus on recovering the small AC@3/AC@5 loss without adding manual family weights back into the runtime algorithm.
