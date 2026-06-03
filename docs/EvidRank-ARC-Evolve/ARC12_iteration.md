# EvidRank-ARC ARC12 Iteration

- Created: 2026-06-03T22:42:07+08:00
- Hypothesis: 在 ARC11 family effective participation 基础上，用 endpoint-status/rise rank alignment 学习 endpoint support gate，替代 legacy endpoint 固定 factor/penalty
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Scope

- Files changed: `algorithms/evidencerank/src/evidencerank/algorithm.py`.
- General RCA mechanism being tested: combine ARC11 family effective participation with an ARC-only endpoint support gate learned from endpoint/status/rise rank alignment. Default `evidencerank` remains unchanged.
- Why this should transfer beyond RCABench: endpoint shift is trusted when it aligns with protocol status mutation or request-volume rise in the current case. The support mixture uses current-case rank vectors and cosine alignment, not fixed status/rise multipliers, labels, services, or fault names.

## Baseline

- Baseline snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC7/`.
- Baseline summary: `docs/EvidRank-ARC-Evolve/ARC7_summary.md`.
- Baseline metrics: AC@1 `0.728551`, MRR `0.836843`, AC@3 `0.943741`, AC@5 `0.973277`, error `0`.
- Intermediate baseline: ARC11 matched ARC7 AC@1/AC@3/AC@5 and had MRR `0.836637`, but kept legacy endpoint gate.
- Representative concern: legacy endpoint gate still used fixed factors `2.0`, `1.5`, `0.5`, and `1.75` in the ARC path.

## Planned Change

- Minimal algorithm change:
  - keep ARC11 effective family participation;
  - route ARC scoring and weighted matrices through `_apply_arc_trace_endpoint_support_gate`;
  - compute status/rise support weights by cosine alignment between endpoint rank view and candidate support rank views;
  - adjust endpoint evidence by endpoint rank plus learned support rank.
- Expected metric movement: improve AC@1/MRR by sharpening protocol mutation cases where endpoint, status, and rise co-localize.
- Known regression risk: delay, partition, loss, pod/container, and other propagation-shaped roots may rely less on endpoint/status alignment and can drop in top3.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank_arc -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `output/rcabench-platform-v2/evolve_snapshots/ARC12/`.
- New summary: `docs/EvidRank-ARC-Evolve/ARC12_summary.md`.
- Compare report: `docs/EvidRank-ARC-Evolve/compare_ARC7_vs_ARC12.md`.
- AC@1: `0.734880` (`+0.006329` vs ARC7).
- AC@3: `0.936006` (`-0.007736` vs ARC7).
- AC@5: `0.971871` (`-0.001406` vs ARC7).
- MRR: `0.839508` (`+0.002665` vs ARC7).
- Error: `0`.

## Case Deltas

- Improved: `35` improved to hit@1 and `29` additional rank improvements.
- Regressed: `26` regressed from hit@1 and `37` additional rank regressions.
- Improved fault types: response-replace-code (`15` improved to hit@1), request-replace-method (`7`), response-replace-body (`4`), response-abort (`3`), plus smaller gains in bandwidth, request-replace-path, partition, and loss.
- Regressed fault types: response-delay (`4` regressed from hit@1), request-delay (`3`), partition (`3`), response-replace-code (`3`), loss (`2`), pod-failure (`2`), and scattered single-case regressions.
- Top-k movement: `13` cases lost top3 while `2` gained top3; `2` cases lost top5 and no cases gained top5. The AC@3 drop is concentrated in delay/propagation-like cases plus a few protocol cases where the endpoint gate over-promoted a neighboring endpoint-supported service.

## Decision

- Accept / reject / keep for later: accept ARC12 as the current EvidRank-ARC candidate.
- Reason: guard has no high-risk warnings; full eval has `error=0`; AC@1 and MRR both improve over ARC7; AC@5 has only a small two-case net drop; AC@3 drops by 11 net cases but the mechanism is explainable as a sharper endpoint/protocol mutation gate trading off some propagation-shaped delay/partition cases.
- Next smallest general step: add a case-local propagation-sensitivity guard for the endpoint gate, learned from delay/propagation family dominance, to recover AC@3 without giving up the ARC12 AC@1 gain.
