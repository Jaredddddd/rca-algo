# EvidenceRank FW_PRIORITY_LINEAR_0_7 Iteration

- Created: 2026-06-03T23:25:58+08:00
- Hypothesis: 把 SRE feature priority ladder 从当前分段倍率替换为 0-7 线性序数，验证压缩根因特异信号倍率后默认 EvidenceRank 的排名稳定性
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change:
- General RCA mechanism being tested:
- Why this should transfer beyond RCABench:

## Baseline

- Baseline snapshot:
- Baseline summary:
- Key weak groups:
- Representative false cases:

## Planned Change

- Minimal algorithm change:
- Expected metric movement:
- Known regression risk:

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot:
- New summary:
- Compare report:
- AC@1:
- AC@3:
- AC@5:
- MRR:

## Case Deltas

- Improved:
- Regressed:

## Decision

- Accept / reject / keep for later:
- Reason:
- Next smallest general step:
