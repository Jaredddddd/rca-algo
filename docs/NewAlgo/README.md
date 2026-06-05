# NewAlgo Research

This directory records the design and iteration trail for a new unsupervised RCA algorithm derived from the capabilities exposed by EvidenceRank, not from RCABench labels or case-specific patches.

## Goal

Use the current EvidenceRank implementation as a strong probe: it reveals which multimodal and topology-aware capabilities are necessary for high RCABench performance. The new algorithm should transform those capabilities into a publishable unsupervised method with a clear motivation, a novel inference mechanism, and robust empirical behavior.

The first acceptance bar is deliberately lower than the current EvidenceRank score:

| milestone | requirement | meaning |
| --- | ---: | --- |
| Work | AC@1 >= 0.60 | standalone new algorithm is viable |
| Competitive | AC@1 >= 0.70 | close to ARC-style no-fixed-prior baselines |
| Strong | AC@1 >= 0.75 | worth serious ablation and paper framing |
| Target | AC@1 near 0.80 | approaches current EvidenceRank probe |

Every version must complete full eval with `error == 0` before it is called working.

## Boundaries

- Do not read labels, injection metadata, evaluation outputs, previous rankings, perf reports, or `conclusion.parquet` in the runtime algorithm.
- Do not hardcode datapack ids, service names, fault names, random suffixes, or dataset splits.
- Do not implement the new algorithm as a direct call to `EvidenceRank`, `EvidenceRankARC`, or a copied `FEATURE_WEIGHTS` weighted sum.
- It is acceptable to reuse raw feature extraction from EvidenceRank, because those are generic observability transformations from metrics, traces, logs, and topology.
- Labels and injection metadata may be used only in offline summaries, comparisons, and research documents.

## Starting Point

Read these files before designing or coding:

```text
AGENTS.md
VibeResearchTools/DesignNewAlgo.md
VibeResearchTools/VibeResearch.md
results.md
algorithms/evidencerank/src/evidencerank/algorithm.py
docs/feature_weight.md
docs/EvidRank-ARC-Evolve/EvidRank_ARC_baseline.md
docs/EvidRank_evolve/V11_summary.md
docs/EvidRank_evolve/V20_iteration.md
```

## Current Version

`CERA1` is accepted as the first working standalone version:

| version | AC@1 | MRR | AC@3 | AC@5 | error | note |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `CERA1` | 0.691280 | 0.814367 | 0.933193 | 0.966245 | 0 | Work milestone passed |

Implementation: `algorithms/evidencerank/src/evidencerank/cera.py`

Iteration note: `docs/NewAlgo/CERA1_iteration.md`

## Suggested Method Line

The initial proposed method is CERA, Counterfactual Evidence Role Alignment. It is described in `CERA_design_brief.md`, and the full prompt for the next coding agent is in `CodingAgentPrompt.md`.

The short version:

- infer latent roles for services: root, propagation victim, background;
- learn evidence-family reliability inside each incident;
- distinguish mutation/local evidence from propagation evidence;
- use trace topology to explain away victim symptoms through adjacent root-like services;
- iterate from a simple working version to a stronger EM-style or energy-based model.
