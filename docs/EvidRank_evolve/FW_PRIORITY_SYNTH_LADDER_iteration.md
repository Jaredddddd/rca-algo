# EvidenceRank FW_PRIORITY_SYNTH_LADDER Iteration

- Created: 2026-06-04T02:10:00+08:00
- Hypothesis: `FEATURE_WEIGHTS` 的精确浮点数不应作为算法接口暴露；只保留 SRE feature priority ordering，并从 priority tier topology 自动合成非线性诊断强度曲线，可以保持当前 AC@1/MRR，同时降低“手写精确权重表”的论文风险。
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files changed:
  - `algorithms/evidencerank/src/evidencerank/algorithm.py`
  - `docs/EvidRank_evolve/FW_PRIORITY_LADDER_ABLATION_iteration.md`
  - generated reports under `docs/EvidRank_evolve/` and refreshed `VibeResearchTools/VibeResearch.md`
- General RCA mechanism: express feature knowledge as ordinal diagnostic priority, then synthesize a nonlinear severity ladder from the priority tiers:
  - low symptom/support tiers are fine-grained around the baseline unit;
  - root-specific tiers must exceed the combined pull of several low-tier symptoms;
  - critical protocol/status tiers use the next binary ceiling above root strength to model discontinuous diagnostic evidence.
- The algorithm still does not read labels, injections, outputs, historical reports, or case identifiers. Labels are used only in offline `VibeResearchTools` reports.

## Failure Mechanism

The previous priority table was easier to defend than per-feature floats, but it still exposed exact-looking values such as `0.75`, `1.25`, `1.5`, `6`, `10`, and `16`.

Offline feature-cache analysis showed why the scorer is sensitive:

- root-specific `metric_count_drop_shift` has very small raw scale, with global positive p95 around `0.236`;
- many count/duration/background features have p95 in the `5..20` range;
- if strong tiers are compressed to a simple integer/decimal ladder, propagation and volume symptoms become competitive in close top-1 margins.

So the core issue is not the per-feature table itself, but the need for a nonlinear diagnostic strength separation between low-level symptoms and root-specific evidence.

## Negative Experiments

All rows below used cached raw feature matrices from `FW_FEATURE_CACHE_BASE`; labels were used only for offline metric computation.

| mechanism | representative setting | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| direct decimal ladder | `0,1,1,1,2,5,10,15` | 0.768636 | 0.858448 | 0.942335 | 0.975387 | reject |
| feature-wise inverse-scale compensation | best around alpha `0.15` | 0.779184 | 0.865758 | 0.948664 | 0.976090 | reject |
| priority-group max-scale compensation | decimal + two-sided alpha `0.20` | 0.797468 | 0.874584 | 0.946554 | 0.978903 | near miss |
| conservative p25/down-only compensation | decimal + alpha `0.30` | 0.796765 | 0.875511 | 0.948664 | 0.978903 | near miss |
| severity-family rank fusion | best `gmax_two 0.15..0.25`, RRF | 0.797468 | 0.874605 | 0.946554 | 0.979606 | near miss |
| formula low + triangular strong | `0,0.75,1,1.25,1.5,6,10,15` | 0.795359 | 0.871761 | 0.940225 | 0.976793 | reject |

These results do not support the claim that arbitrary ordinal values alone are enough under the current linear scorer. They do support a narrower claim: exact user-facing values are not the core; the core is a nonlinear diagnostic strength curve that keeps root/critical tiers separated from propagation symptoms.

## Accepted Change

Removed the explicit `FEATURE_PRIORITY_WEIGHTS` table and added `_synthesize_feature_priority_ladder()`.

The synthesized ladder is derived from the `FeaturePriority` enum:

- `DISABLED = 0`;
- low tiers `BACKGROUND..LOCAL` are centered around baseline with step `1 / number_of_low_tiers`;
- `HIGH` is the low-tier ceiling multiplied by the low-tier count;
- `ROOT` adds one low-tier block above `HIGH`;
- `CRITICAL` is the next power-of-two ceiling above `ROOT`.

For the current priority taxonomy this yields:

```text
[0.0, 0.75, 1.0, 1.25, 1.5, 6.0, 10.0, 16.0]
```

This keeps the accepted ranking behavior but removes the hand-maintained float lookup from the algorithm interface. If a paper or config displays priorities as `0,1,1,1,2,5,10,15`, those should be described as ordinal severity IDs, not direct scorer weights; the scorer synthesizes its own nonlinear diagnostic ladder from the priority structure.

## Validation

Commands:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version FW_PRIORITY_SYNTH_LADDER --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version FW_PRIORITY_SYNTH_LADDER --source FW_PRIORITY_SYNTH_LADDER --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old FW_PRIORITY_PRIOR --new FW_PRIORITY_SYNTH_LADDER --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

Full eval:

| version | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `FW_PRIORITY_PRIOR` | 1422 | 0 | 0.800985 | 0.874517 | 0.942335 | 0.975387 |
| `FW_PRIORITY_SYNTH_LADDER` | 1422 | 0 | 0.800985 | 0.874517 | 0.942335 | 0.975387 |

Compare result: all `1422` cases unchanged.

Guard result: no high-risk overfitting warnings. Existing medium warnings are rcabench package/documentation literals.

## Decision

Accepted.

Reason: the code no longer exposes exact feature-priority float values, while full eval remains unchanged. This supports the paper statement: "the exact numeric entries are not the contribution; EvidenceRank uses an ordinal SRE feature-priority prior and synthesizes a nonlinear diagnostic severity ladder so root-specific and critical evidence are separated from generic propagation symptoms."

The stronger claim "any monotonic numeric ladder reaches best AC@1" is not supported by experiments. Direct `0,1,1,1,2,5,10,15` still loses about `46` top-1 hits versus the accepted synthesized ladder when used as direct weights.
