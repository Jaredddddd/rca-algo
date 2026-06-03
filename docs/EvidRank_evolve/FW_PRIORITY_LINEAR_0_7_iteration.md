# EvidenceRank FW_PRIORITY_LINEAR_0_7 Iteration

- Created: 2026-06-03T23:25:58+08:00
- Hypothesis: 把 SRE feature priority ladder 从当前分段倍率替换为 0-7 线性序数，验证压缩根因特异信号倍率后默认 EvidenceRank 的排名稳定性
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files temporarily changed: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- General RCA mechanism being tested: use the ordinal priority enum value itself as the feature weight, i.e. `DISABLED=0 ... CRITICAL=7`.
- Why this should transfer beyond RCABench: if successful, this would make the SRE priority prior purely ordinal and remove the need for a calibrated severity ladder.

## Baseline

- Baseline snapshot: `FW_PRIORITY_PRIOR`
- Baseline metrics: AC@1 `0.800985`, MRR `0.874517`, AC@3 `0.942335`, AC@5 `0.975387`.
- Broader ladder analysis: `docs/EvidRank_evolve/FW_PRIORITY_LADDER_ABLATION_iteration.md`

## Planned Change

- Minimal algorithm change: replace the shared priority ladder with `float(priority)`.
- Expected metric movement: unknown; this tests whether ordinal priority spacing is enough.
- Known regression risk: strong RCA evidence is compressed too much: `CRITICAL/BASELINE` changes from `16` to `3.5`, and `ROOT/BASELINE` from `10` to `3`.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot: `FW_PRIORITY_LINEAR_0_7`
- New summary: `docs/EvidRank_evolve/FW_PRIORITY_LINEAR_0_7_summary.md`
- Compare report: `docs/EvidRank_evolve/compare_FW_PRIORITY_PRIOR_vs_FW_PRIORITY_LINEAR_0_7.md`
- AC@1: `0.800985 -> 0.671589`
- MRR: `0.874517 -> 0.789295`
- AC@3: `0.942335 -> 0.886076`
- AC@5: `0.975387 -> 0.945148`

## Case Deltas

- Improved to hit@1: `43`
- Regressed from hit@1: `227`
- Interpretation: linear ordinal values over-promote background/support/propagation evidence and under-promote protocol/status/root-side evidence.

## Decision

- Accept / reject / keep for later: reject as default.
- Reason: the loss is too large across AC@1, MRR, AC@3, and AC@5.
- Next smallest general step: use feature-cache reweighting to scan calibrated priority ladders instead of rerunning full eval for each candidate.
