# EvidRank-ARC Baseline

- Created: 2026-06-03
- Final evaluated behavior: `ARC_67`
- Stored pre-rename snapshot: `output/rcabench-platform-v2/evolve_snapshots/V13_SELF_LEARNED_67/`
- Algorithm registry name: `evidencerank_arc`
- Full name: EvidRank-ARC, Adaptive Reliability Calibration
- Purpose: provide a runnable self-learned reliability-calibration baseline without replacing the accepted default `evidencerank` implementation.

## Hypothesis

Use only the current incident's feature matrix to learn feature weights. A feature should be trusted when it has enough positive coverage, produces a localized evidence distribution, separates peaks from the background, has a clear top-rank gap, and agrees with peer or cross-modal evidence.

This is a no-label baseline for the "remove fixed per-feature prior" question. It was first explored under the V13 experimental line, but the formal method name is now EvidRank-ARC. It must not read labels, injection metadata, evaluation outputs, historical rankings, or `conclusion.parquet`.

## Final Mechanism

- Default `evidencerank` is unchanged; the new code path is registered as `evidencerank_arc`.
- `EvidenceRankARC` reuses the existing raw metric, trace, log, endpoint-support, trace-edge, and parent-context feature extraction.
- It does not use `FEATURE_WEIGHTS` in its ranking path.
- It scales every feature column inside the current case by the positive p95 value, then clips to `[0, 3.0]`.
- It learns one case-local weight per enabled feature from positive support, entropy-based evidence concentration, p95-vs-median peak contrast, top1-vs-top2 gap, and cosine agreement with same-modality peer features plus other modalities.
- Learned weights are normalized to mean 1 over active features before service scores are summed.
- EvidRank-ARC keeps `topology_in_degree` and `topology_out_degree` as unsupervised structural tie-break features. Removing them lowered AC@1, so they are part of the accepted baseline.

## Iterations

| version | key change | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `V13_REIMPL` | p95 scaling clipped to `[0, 1]` | 0.583685 | 0.747704 | 0.910689 | 0.955696 | reject |
| `ARC_BASELINE` | p95 scaling clipped to `[0, 3.0]`, topology retained | 0.670886 | 0.801983 | 0.925457 | 0.973980 | accept as EvidRank-ARC |
| `V13_REIMPL_V3_NO_TOPO` | removed topology degree features | 0.649086 | 0.786477 | 0.914909 | 0.966245 | reject |
| `ARC_67` | final named ARC behavior | 0.670886 | 0.801983 | 0.925457 | 0.973980 | final |

The important optimization was allowing strong peak evidence to remain above 1 after per-case p95 scaling. The `[0, 1]` version over-flattened localized roots and behaved too much like equalized feature fusion. The topology ablation showed that degree features, even without a hand-coded prior, help stabilize this no-prior baseline.

## Current Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version EvidRank_ARC_67 --algorithm evidencerank_arc --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version EvidRank_ARC_67 --source EvidRank_ARC_67 --algorithm evidencerank_arc --dataset rcabench
```

## Verification

- `uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/algorithm.py algorithms/evidencerank/main.py`
  - Result: compile succeeded.
- `uv run --package evidencerank python -c "from evidencerank.algorithm import EvidenceRankARC; alg=EvidenceRankARC(); print(type(alg).__name__, len(alg._enabled_features), alg.needs_cpu_count())"`
  - Result: `EvidenceRankARC 21 1`.
- `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard`
  - Result: no high-risk overfitting warnings.
- `LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_v13 -d rcabench --clear --use-cpus 48`
  - Result for the equivalent pre-rename implementation: full eval completed, 1422 cases, error 0, batch wall time 298.997433s.
- `uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench`
  - Result for the equivalent pre-rename `evidencerank_v13` run: total 1422, error 0, runtime.avg 9.733532s, AC@1 0.670886, MRR 0.801983, AC@3 0.925457, AC@5 0.973980.
- Final summary: `docs/EvidRank-ARC-Evolve/EvidRank_ARC_67_summary.md`.
- Drift check: `docs/EvidRank-ARC-Evolve/compare_ARC_BASELINE_vs_ARC_67.md` shows all 1422 cases unchanged.

## Decision

Accept `evidencerank_arc` / EvidRank-ARC as the self-learning feature-weight baseline because it reaches the requested AC@1 >= 0.67 threshold with a clean guard and error 0 full eval. It should remain a comparison baseline rather than the default EvidenceRank implementation, because it still trails the accepted fixed-prior line on AC@1 and MRR.
