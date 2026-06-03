# EvidenceRank FW_PRIORITY_LADDER_ABLATION Iteration

- Created: 2026-06-03T23:40:28+08:00
- Hypothesis: 比较线性序数、二进制层级和十进制 SRE severity ladder，分析 FEATURE_PRIORITY_WEIGHTS 数值区间对默认 EvidenceRank 排名稳定性的影响
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
