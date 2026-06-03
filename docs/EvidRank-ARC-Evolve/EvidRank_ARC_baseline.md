# EvidRank-ARC Baseline

- Created: 2026-06-03
- Current accepted behavior: `ARC5`
- Initial evaluated baseline: `ARC_67`
- Stored pre-rename snapshot: `output/rcabench-platform-v2/evolve_snapshots/V13_SELF_LEARNED_67/`
- Algorithm registry name: `evidencerank_arc`
- Full name: EvidRank-ARC, Adaptive Reliability Calibration
- Purpose: provide a runnable self-learned reliability-calibration baseline without replacing the accepted default `evidencerank` implementation.

## Hypothesis

Use only the current incident's feature matrix to learn feature weights. A feature should be trusted when it has enough positive coverage, produces a localized evidence distribution, separates peaks from the background, has a clear top-rank gap, and agrees with peer or cross-modal evidence.

This is a no-label baseline for the "remove fixed per-feature prior" question. It was first explored under the V13 experimental line, but the formal method name is now EvidRank-ARC. It must not read labels, injection metadata, evaluation outputs, historical rankings, or `conclusion.parquet`.

## Current Mechanism

- Default `evidencerank` is unchanged; the new code path is registered as `evidencerank_arc`.
- `EvidenceRankARC` reuses the existing raw metric, trace, log, endpoint-support, trace-edge, and parent-context feature extraction.
- It does not use `FEATURE_WEIGHTS` in its ranking path.
- It scales every feature column inside the current case by the positive p95 value, then clips to `[0, 3.0]`.
- It learns one case-local weight per enabled feature from positive support, entropy-based evidence concentration, p95-vs-median peak contrast, top1-vs-top2 gap, and cosine agreement with same-modality peer features plus other modalities.
- ARC1 changed those learned weights into an active-feature mask, because single-case per-feature reliability was too noisy as a sharp multiplier.
- ARC2 aggregates the same single-case reliability to family-level median reliability and applies it only as a bounded group correction.
- ARC2 also computes a service-level local-vs-propagation contrast from p95-normalized family sums: `metric + mutation + log - propagation`.
- ARC3 removes ARC2's explicit blend constants and derives correction strength from active evidence-family count.
- ARC5 adds a final trace-neighbor pairwise contrast: when a higher-scored adjacent service is propagation-heavy and its neighbor is mutation-heavier, score is transferred to the strongest root-like neighbor explanation for that victim.
- EvidRank-ARC keeps `topology_in_degree` and `topology_out_degree` as unsupervised structural tie-break features. Removing them lowered AC@1, so they are part of the accepted baseline.

## Iterations

| version | key change | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `V13_REIMPL` | p95 scaling clipped to `[0, 1]` | 0.583685 | 0.747704 | 0.910689 | 0.955696 | reject |
| `ARC_BASELINE` | p95 scaling clipped to `[0, 3.0]`, topology retained | 0.670886 | 0.801983 | 0.925457 | 0.973980 | accept as EvidRank-ARC |
| `V13_REIMPL_V3_NO_TOPO` | removed topology degree features | 0.649086 | 0.786477 | 0.914909 | 0.966245 | reject |
| `ARC_67` | final named initial ARC behavior | 0.670886 | 0.801983 | 0.925457 | 0.973980 | historical baseline |
| `ARC1` | active-feature mask plus trace-direction caller-victim contrast | 0.705345 | 0.823675 | 0.940225 | 0.971167 | accept |
| `ARC2` | bounded family-reliability correction plus local-vs-propagation family contrast | 0.720113 | 0.832050 | 0.940928 | 0.973277 | superseded by ARC3 |
| `ARC3` | ARC2-equivalent structural family-count blend, no explicit blend constants | 0.720113 | 0.832050 | 0.940928 | 0.973277 | superseded by ARC5 |
| `ARC4` | global pseudo-root / pseudo-victim cosine prior synthesis, best conservative candidate | 0.709564 | 0.826269 | 0.940225 | 0.973980 | reject |
| `ARC5` | trace-directed top-neighbor pairwise mutation-vs-propagation transfer | 0.728551 | 0.836412 | 0.940225 | 0.973277 | accept current |

The important optimization was allowing strong peak evidence to remain above 1 after per-case p95 scaling. The `[0, 1]` version over-flattened localized roots and behaved too much like equalized feature fusion. The topology ablation showed that degree features, even without a hand-coded prior, help stabilize this no-prior baseline.

ARC1 showed that per-feature reliability should not be used as a sharp case-local prior. ARC2 recovers part of that signal at a safer granularity: family-level median reliability and service-level local/propagation contrast. ARC3 keeps ARC2's output while replacing explicit blend constants with family-count-derived correction strength. ARC4 showed that global pseudo-vector prior synthesis is too broad for head ranking. ARC5 keeps the self-supervised idea but applies it only as a trace-local top-neighbor pairwise correction. This keeps ARC unsupervised and adaptive while avoiding a direct return to fixed `FEATURE_WEIGHTS`.

## Current Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version ARC5 --algorithm evidencerank_arc --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version ARC5 --source ARC5 --algorithm evidencerank_arc --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old ARC3 --new ARC5 --algorithm evidencerank_arc --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Verification

- `uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/algorithm.py algorithms/evidencerank/main.py`
  - Result: compile succeeded.
- `uv run --package evidencerank python -c "from evidencerank.algorithm import EvidenceRankARC; alg=EvidenceRankARC(); print(type(alg).__name__, len(alg._enabled_features), alg.needs_cpu_count())"`
  - Result: `EvidenceRankARC 21 1`.
- `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard`
  - Result: no high-risk overfitting warnings.
- `LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48`
  - Result for ARC5: full eval completed, 1422 cases, error 0, batch wall time about 299s.
- `uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench`
  - Result for ARC5: total 1422, error 0, runtime.avg 9.752806s, AC@1 0.728551, MRR 0.836412, AC@3 0.940225, AC@5 0.973277.
- Current summary: `docs/EvidRank-ARC-Evolve/ARC5_summary.md`.
- Current compare: `docs/EvidRank-ARC-Evolve/compare_ARC3_vs_ARC5.md`.
- Main improvement compare: `docs/EvidRank-ARC-Evolve/compare_ARC1_vs_ARC2.md`.
- Initial ARC drift check: `docs/EvidRank-ARC-Evolve/compare_ARC_BASELINE_vs_ARC_67.md` shows all 1422 cases unchanged.

## Decision

Accept `ARC5` as the current `evidencerank_arc` / EvidRank-ARC line. Relative to ARC3, it improves AC@1 `0.720113 -> 0.728551` and MRR `0.832050 -> 0.836412`, keeps AC@5 unchanged, and has only a tiny AC@3 change `0.940928 -> 0.940225`. It should remain a comparison baseline rather than replacing the default EvidenceRank implementation, because it still trails the accepted fixed-prior line on AC@1 and MRR.
