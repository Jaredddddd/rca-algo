# CREST Evolution

This directory is the durable home for CREST optimization records from now on.
All future CREST plans, hypotheses, iteration notes, summaries, comparisons,
ablations, decisions, and lessons should be written here.

## Scope

- Target algorithm registry name: `crest`
- Main implementation: `algorithms/evidencerank/src/evidencerank/crest.py`
- Goal: improve CREST from the current `AC@1 ~= 0.80` prototype to
  `AC@1 >= 0.85` on `rcabench` while preserving label-free, raw-telemetry
  deployability.
- Current known baseline: CREST has reached `AC@1 = 0.800281`, `MRR ~= 0.875`,
  `AC@3 ~= 0.945`, `AC@5 ~= 0.972`, `error = 0`. A fresh iteration must verify
  the current working-tree baseline before claiming improvement.

## Hard Rules

- Do not use CERA or EvidenceRank as algorithmic sources for CREST optimization.
- Do not copy or reuse CERA / EvidenceRank manual prior weights, feature-weight
  ladders, ordinal tiers, calibrated multipliers, or optimization records.
- Runtime CREST must not read labels, injection metadata, previous outputs,
  perf reports, historical rankings, ground truth, or `conclusion.parquet`.
- Offline labels and injection metadata may be used only for false-case analysis,
  summarize, compare, and documentation.
- New logic must be expressible as a general microservice RCA mechanism, not as
  a datapack, service-name, fault-name, or RCABench-specific patch.

## File Convention

Use the next unused CREST version number.

- Prompt: `CodingAgentPrompt.md`
- Iteration note: `CREST<N>_iteration.md`
- Summary mirror: `CREST<N>_summary.md`
- Compare mirror: `compare_CREST<OLD>_vs_CREST<NEW>.md`
- Ablation or analysis note: `CREST<N>_<short_name>.md`

`VibeResearchTools/evidrank_lab.py summarize` and `compare` may still emit
markdown under `docs/EvidRank_evolve/`. For CREST work, mirror the generated
CREST markdown into this directory and treat this directory as the source of
truth for future CREST research.

## Current Entry

Start new CREST optimization sessions from:

- [CodingAgentPrompt.md](CodingAgentPrompt.md)

## Current Status

- Latest completed positive-but-reverted iteration: [CREST17_iteration.md](CREST17_iteration.md)
- Current working-tree runtime default: CREST algorithm code has been reverted
  to the repository baseline after the no-magic-number review. The CREST14,
  CREST15, and CREST17 arbitration modules are retained only as research
  records, not as default runtime logic.
- Revert and lesson summary: [CREST_revert_and_lessons.md](CREST_revert_and_lessons.md)
- Baseline metrics to beat on `rcabench`: `AC@1=0.800281`,
  `MRR=0.875326`, `AC@3=0.944444`, `AC@5=0.971871`, `error=0`.
- The `AC@1 >= 0.85` goal is not complete.
- Accepted CREST17 default: `crest` improved 18 cases to hit@1 with 0
  `regressed_from_hit1` cases relative to `CREST15_ACCEPTED`. It had one
  non-top1 `rank_regressed` case, where the GT moved from rank 2 to rank 3.
- Accepted CREST15 default: `crest` improved 18 cases to hit@1 with 0
  `regressed_from_hit1` cases relative to the old default.
- Positive CREST14 ablation: `crest_mutation_arbitration` reached
  `AC@1=0.803094`, `MRR=0.876849`, `AC@3=0.944444`, `AC@5=0.971871`,
  `error=0`. It improved 4 cases to hit@1, regressed 0 previous hit@1 cases,
  and changed top-1 in only 6 cases. Keep it as an intermediate CREST-family
  variant, not as proof that the `AC@1 >= 0.85` goal is solved.
- Rejected CREST8 residual ablation: `crest_residual` reached only
  `AC@1=0.340366` and caused 699 `regressed_from_hit1` cases.
- Rejected CREST9 gated residual ablation: `crest_gated_residual` reached
  `AC@1=0.797468`, `MRR=0.873919`, `AC@3=0.944444`, `AC@5=0.971871`.
  It improved 11 cases to hit@1 but regressed 15 previous hit@1 cases, so the
  default must not switch.
- Rejected CREST10 victim suppression ablation: `crest_victim_suppression`
  reached `AC@1=0.757384`, `MRR=0.841618`, `AC@3=0.917018`,
  `AC@5=0.950070`. It improved 24 cases to hit@1 but regressed 85 previous
  hit@1 cases, so the suppression predicate is too broad.
- Rejected CREST11 compressed stability fusion: no runtime ablation was
  implemented because no `A/F/S` rank-fusion formula improved AC@1 or MRR.
- Rejected CREST12 family fusion: no runtime ablation was implemented because
  family-level root evidence was too noisy and regressed many default hit@1
  cases offline.
- Rejected CREST13 server protocol ownership reranking: no runtime ablation was
  implemented because server-span protocol drift produced many symptom-surface
  false positives.

Key CREST8 artifacts:

- [CREST7_BASELINE_summary.md](CREST7_BASELINE_summary.md)
- [CREST8_DEFAULT_summary.md](CREST8_DEFAULT_summary.md)
- [CREST8_RESIDUAL_summary.md](CREST8_RESIDUAL_summary.md)
- [compare_CREST7_BASELINE_vs_CREST8_REJECTED.md](compare_CREST7_BASELINE_vs_CREST8_REJECTED.md)
- [compare_CREST7_BASELINE_vs_CREST8_DEFAULT.md](compare_CREST7_BASELINE_vs_CREST8_DEFAULT.md)

Key CREST9 artifacts:

- [CREST9_iteration.md](CREST9_iteration.md)
- [CREST9_DEFAULT_summary.md](CREST9_DEFAULT_summary.md)
- [CREST9_GATED_RESIDUAL_summary.md](CREST9_GATED_RESIDUAL_summary.md)
- [compare_CREST9_DEFAULT_vs_CREST9_GATED_RESIDUAL.md](compare_CREST9_DEFAULT_vs_CREST9_GATED_RESIDUAL.md)

Key CREST10 artifacts:

- [CREST10_iteration.md](CREST10_iteration.md)
- [CREST10_DEFAULT_summary.md](CREST10_DEFAULT_summary.md)
- [CREST10_VICTIM_SUPPRESSION_summary.md](CREST10_VICTIM_SUPPRESSION_summary.md)
- [compare_CREST10_DEFAULT_vs_CREST10_VICTIM_SUPPRESSION.md](compare_CREST10_DEFAULT_vs_CREST10_VICTIM_SUPPRESSION.md)

Key CREST11-CREST14 artifacts:

- [CREST11_iteration.md](CREST11_iteration.md)
- [CREST12_iteration.md](CREST12_iteration.md)
- [CREST13_iteration.md](CREST13_iteration.md)
- [CREST14_iteration.md](CREST14_iteration.md)
- [CREST14_DEFAULT_summary.md](CREST14_DEFAULT_summary.md)
- [CREST14_MUTATION_ARBITRATION_summary.md](CREST14_MUTATION_ARBITRATION_summary.md)
- [compare_CREST14_DEFAULT_vs_CREST14_MUTATION_ARBITRATION.md](compare_CREST14_DEFAULT_vs_CREST14_MUTATION_ARBITRATION.md)
- [CREST15_iteration.md](CREST15_iteration.md)
- [CREST15_ACCEPTED_summary.md](CREST15_ACCEPTED_summary.md)
- [compare_CREST15_DEFAULT_vs_CREST15_ACCEPTED.md](compare_CREST15_DEFAULT_vs_CREST15_ACCEPTED.md)
- [CREST16_iteration.md](CREST16_iteration.md)
- [CREST17_iteration.md](CREST17_iteration.md)
- [CREST17_ACCEPTED_summary.md](CREST17_ACCEPTED_summary.md)
- [CREST17_PATH_FANIN_summary.md](CREST17_PATH_FANIN_summary.md)
- [compare_CREST15_ACCEPTED_vs_CREST17_ACCEPTED.md](compare_CREST15_ACCEPTED_vs_CREST17_ACCEPTED.md)
- [compare_CREST15_ACCEPTED_vs_CREST17_PATH_FANIN.md](compare_CREST15_ACCEPTED_vs_CREST17_PATH_FANIN.md)

Next recommended focus: do not add protocol drift as a scalar arbitration gate.
CREST17 showed that path/protocol drift becomes useful only when tied to
near-tie structural fan-in and bounded propagation. CREST18 should target the
remaining pod-failure, low-observability, and top-5 miss cases with a weak-root
availability/drop mechanism rather than broadening path drift further.
