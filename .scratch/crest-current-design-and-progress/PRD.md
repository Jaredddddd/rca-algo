# CREST 当前设计与进展梳理 PRD

Status: ready-for-agent
Created: 2026-06-12

## Problem Statement

用户需要快速理解 CREST / CREST-MEO 项目当前到底发展到哪里：默认算法是什么、MEO 和 Oracle 分别是什么、哪些部分已经实现并验证、当前指标和跨数据集风险是什么、下一步应该沿哪个方向继续。现有文档很多且分散，部分文档包含历史方案、ablation、论文草稿和 research-only upper bound，容易把可部署主线、mock MEO、Oracle 上界和历史失败实验混在一起。

## Solution

整理一份当前状态设计稿，把 CREST 项目划分为默认 deterministic runtime、CREST-MEO 配置化入口、research-only Oracle 上界、cross-system validation 四条线。设计稿以现有代码和文档为依据，明确在线路径的无标签约束、核心 scoring 公式、MEOL 当前实现状态、Phase-1 验证结果、RCABench / RCAEval 上的进展，以及下一轮最值得投入的测试 seam 和研究方向。AIOps25 只保留为历史旁证，不作为当前目标任务数据集。

## User Stories

1. As an RCA algorithm researcher, I want to know the default CREST runtime path, so that I can distinguish deployable code from research-only experiments.
2. As an RCA algorithm researcher, I want to understand the input telemetry contract, so that I can judge which datasets are compatible with CREST.
3. As an RCA algorithm researcher, I want to see the feature families and role semantics, so that I can reason about why CREST ranks one service above another.
4. As an RCA algorithm researcher, I want the final scoring formula explained, so that I can debug `A`, `F`, `S`, and final score movements.
5. As an RCA algorithm researcher, I want the counterfactual explain-away mechanism summarized, so that I can assess root-victim role contrast.
6. As an RCA algorithm researcher, I want modality ablations summarized, so that I can see which evidence channels contribute to current performance.
7. As an RCA algorithm researcher, I want to know what CREST-MEO has implemented, so that I can tell whether it is ready for real LLM synthesis.
8. As an RCA algorithm researcher, I want to distinguish `default_meol` from built-in MEOL, so that I do not misread the mock seed library as the production evidence library.
9. As an RCA algorithm researcher, I want the built-in MEOL equivalence guarantee captured, so that future MEOL work does not silently change the default baseline.
10. As an RCA algorithm researcher, I want Oracle artifacts clearly labeled as research-only, so that no GT-derived library leaks into online evaluation.
11. As an RCA algorithm researcher, I want the current RCABench metrics summarized, so that I can anchor progress against known baselines.
12. As an RCA algorithm researcher, I want the RCAEval SOTA result captured, so that I can use it as the intended cross-system validation target.
13. As an RCA algorithm researcher, I want AIOps25 findings explicitly marked as historical and out-of-target, so that I do not optimize the current project for the wrong dataset.
14. As an RCA algorithm researcher, I want known negative lessons about residual scoring captured, so that I do not repeat broad additive residual experiments.
15. As an RCA algorithm researcher, I want the highest-level testing seams identified, so that future agents can verify behavior without brittle implementation-detail tests.
16. As an RCA algorithm researcher, I want guardrail requirements listed, so that label leakage and case hardcoding remain out of the algorithm path.
17. As a paper writer, I want the online/offline separation described, so that the paper does not imply online LLM calls during incident-time RCA.
18. As a paper writer, I want Oracle upper-bound results separated from main-method results, so that the claims stay defensible.
19. As a future implementation agent, I want clear next-step candidates, so that I can pick a focused issue instead of reopening the whole design space.
20. As a future implementation agent, I want current verification commands and acceptance seams, so that I can make a change and know what must pass.
21. As a maintainer, I want project state documented inside the CREST docs, so that new work can start from the canonical module rather than legacy adapters.
22. As a maintainer, I want historical ablations summarized as context, so that rejected ideas remain useful without becoming default behavior.

## Implementation Decisions

- The design summary treats the standalone CREST module as the source of truth and treats legacy compatibility adapters as non-canonical.
- The default deployable algorithm is described as deterministic, label-free service ranking over normal and abnormal telemetry windows.
- The core algorithm is explained through local abnormality, structural explanatory power, denoised support, and final ranking score.
- Evidence roles are described as two explicit deployable memberships, mutation and propagation; neutral is represented by both memberships being zero.
- CREST-MEO is documented as an offline synthesis and online deterministic execution architecture; online LLM calls remain outside the deployable runtime.
- The mock default MEOL is documented as a Phase-1 chain validation artifact rather than a mature operator library.
- The built-in MEOL is documented as a mechanical configuration export of the default CREST feature set and role memberships.
- Oracle artifacts are documented as intentionally leaky research-only upper bounds that may use labels only for offline global operator selection.
- Current metrics are summarized by dataset and by algorithm family, with RCABench and intended RCAEval validation kept separate from historical AIOps25 notes.
- The next major documentation direction is to formalize RCAEval cross-system validation, including exact metrics, commands, comparison set, and SOTA basis.
- Residual and victim suppression variants are treated as historical ablations unless protected by narrow eligibility gates.
- The design summary is published as a human-readable CREST documentation page, while this PRD records the productized documentation goal in the local issue tracker.

## Testing Decisions

- Good tests should verify external ranking behavior, deterministic fallback behavior, MEOL equivalence, and leakage boundaries rather than private implementation details.
- The highest-value seam is the service scoring entry point, because default CREST, MEO variants, modality ablations, and graph modes all pass through it.
- The existing Phase-1 test suite should remain the primary unit/smoke suite for MEO atoms, compiler behavior, instantiation, verifier behavior, mock synthesis, and built-in MEOL equivalence.
- Full benchmark verification should use the registered algorithm CLI and perf reports for dataset-level acceptance.
- Safety verification should continue to use the repository guard for high-risk label, injection, output, and service-name hardcoding signals.
- Future MEOL work should include an equivalence test for the built-in MEOL unless the explicit goal is to change default CREST semantics.
- Future cross-dataset work should report RCABench and RCAEval results; AIOps25-family results are not part of the current default acceptance bar unless explicitly requested.

## Out of Scope

- Changing CREST scoring code.
- Promoting any Oracle artifact into the deployable MEOL library.
- Calling a real LLM during online RCA evaluation.
- Running a new full benchmark evaluation.
- Creating new implementation tickets for every future research direction.
- Rewriting the existing long design documents or paper drafts.
- Refactoring the standalone module or the EvidenceRank compatibility adapter.

## Further Notes

The produced design summary intentionally separates four concepts that are easy to conflate: default `crest` as the accepted runtime, `crest_meo` as the configurable MEOL entry point, `crest_meo_builtin` as the equivalence bridge, and Oracle synthesis as an upper-bound research tool. Future agents should preserve this separation when proposing algorithm changes or paper claims.
