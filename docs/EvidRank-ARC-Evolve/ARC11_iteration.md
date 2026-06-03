# EvidRank-ARC ARC11 Iteration

- Created: 2026-06-03T22:33:55+08:00
- Hypothesis: 用 family reliability 的 effective participation number 学习 ARC family correction 强度，替代整数 active_family_count，同时保留 active-anchor RCA 校正结构
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files changed: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: keep the ARC7 active/family/local-contrast correction shape, but replace integer `active_family_count` with the effective participation number of the current case's learned family reliability distribution.
- Why this should transfer beyond RCABench: the participation number is computed from feature reliability inside the current incident; it does not use labels, service names, fault names, or historical results.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC7/`.
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC7_summary.md`.
- Baseline metrics: AC@1 `0.728551`, MRR `0.836843`, AC@3 `0.943741`, AC@5 `0.973277`, error `0`.
- Representative concern: ARC9/ARC10 proved generic view reliability is not a safe replacement for the structured family correction.

## Planned Change

- Minimal algorithm change:
  - compute family reliabilities from feature reliability as before;
  - compute `effective_family_count = (sum reliability)^2 / sum(reliability^2)`;
  - use that effective count in the existing family reliability and contrast blend formulas;
  - keep endpoint gate legacy for isolation.
- Expected metric movement: match ARC7 while making the correction strength depend on the current case's reliability distribution rather than an integer count.
- Known regression risk: if effective count differs from integer count in sensitive cases, MRR can move without changing hit@1.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC11/`.
- New summary: `docs/EvidRank-ARC-Evolve/ARC11_summary.md`.
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC11.md`.
- AC@1: `0.728551` (unchanged vs ARC7).
- AC@3: `0.943741` (unchanged vs ARC7).
- AC@5: `0.973277` (unchanged vs ARC7).
- MRR: `0.836637` (`-0.000206` vs ARC7).
- Error: `0`.

## Case Deltas

- Hit@1 unchanged overall. MRR falls slightly, indicating small within-top ranks moved unfavorably even though top-k counts were stable.
- Mechanism supported: effective family participation is a safe near-drop-in replacement for integer active family count, but by itself does not improve metrics.

## Decision

- Accept / reject / keep for later: keep as foundation for ARC12, not accepted alone.
- Reason: it removes one artificial counting choice with negligible metric movement, but acceptance requires AC@1 or MRR improvement.
- Next smallest general step: combine ARC11 with a learned endpoint support gate to test whether endpoint fixed factors can be replaced without losing head accuracy.
