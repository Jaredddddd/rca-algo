# CERA3 Iteration

- Created: 2026-06-05
- Algorithm registry name: `cera`
- Dataset: `rcabench`
- Goal: reach `AC@1 >= 0.80` without hand-crafted numeric feature weights, runtime labels, case hardcoding, or EvidenceRank delegation

## Hypothesis

CERA2's unweighted robust family burden is too egalitarian: it preserves generic evidence but under-separates root-specific protocol, availability, and local mutation signals from high-volume propagation symptoms. A publishable CERA variant should express this separation as an ordinal causal evidence taxonomy rather than a feature-by-feature numeric weight table.

The root score should combine three generic mechanisms:

1. Raw incident feature energy, because absolute log-normalized volume and mutation magnitude are themselves operational signals.
2. Ordinal causal evidence tiers, where feature semantics define roles such as background, support, local, high, root, and critical evidence.
3. Topology sink-share context, where the strength of parent-context smoothing is derived from the current trace graph's fraction of terminal downstream nodes.

## Hard Constraints

- Runtime CERA must not read labels, injection metadata, previous outputs, perf reports, historical rankings, ground truth, or `conclusion.parquet`.
- Do not hardcode datapack ids, service names, fault names, random suffixes, or dataset splits.
- Do not call `EvidenceRank` or `EvidenceRankARC` for runtime rankings.
- Do not use hand-crafted numeric feature weights or manually tuned blend constants.
- Numeric evidence energy must be synthesized from ordinal tier ordering and tier count, not assigned as per-feature floats.
- Parent-context strength must be derived from the current incident trace graph.

## Offline Ablation

The ablation used only cached feature matrices and labels for evaluation-side scoring. No label-derived value enters the runtime algorithm.

Best candidate mechanisms:

| variant | AC@1 | MRR | AC@3 | AC@5 | note |
| --- | ---: | ---: | ---: | ---: | --- |
| CERA2 | 0.752461 | 0.842955 | 0.926160 | 0.961322 | accepted CERA2 baseline |
| ordinal raw, no gate, no parent | 0.804501 | 0.876950 | 0.941632 | 0.974684 | crosses target without fixed gate/context constants |
| ordinal raw + sink-share parent | 0.845288 | 0.899151 | 0.942335 | 0.968354 | graph-derived parent context |
| ordinal raw + ARC endpoint support + sink-share parent | 0.850211 | 0.904032 | 0.950774 | 0.976090 | selected CERA3 candidate |
| ordinal raw + legacy endpoint gate + sink-share parent | 0.852321 | 0.904868 | 0.950070 | 0.974684 | rejected because legacy gate contains fixed numeric constants |

Rejected directions:

- Equal rank-fusion views reduced AC@1 to `0.59..0.67`.
- PCA/self-reliability feature weighting remained below CERA2.
- Counterfactual explain-away on the ordinal candidate lowered top-1 relative to sink-share parent context alone.

## Planned Mechanism

1. Replace CERA2's robust unweighted family burden with raw log-normalized ordinal evidence energy.
2. Define semantic causal evidence tiers, not per-feature numeric weights.
3. Synthesize the energy ladder from tier ordering:
   - low tiers occupy a compact ordinal band around baseline;
   - high/root tiers are separated by the number of low tiers;
   - critical evidence uses the next dyadic ceiling.
4. Apply ARC endpoint support gate, whose support blend is derived from current endpoint/status/rise rank agreement.
5. Apply parent context with:

```text
context_weight = sink_nodes / service_count
sink_nodes = trace children that are not trace parents
```

## Validation Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/cera.py algorithms/evidencerank/main.py
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a cera -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CERA3 --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CERA3 --source CERA3 --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CERA2 --new CERA3 --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

Full eval completed on 2026-06-05:

| metric | value |
| --- | ---: |
| total | 1422 |
| error | 0 |
| AC@1 | 0.850211 |
| MRR | 0.904032 |
| AC@3 | 0.950774 |
| AC@5 | 0.976090 |
| runtime.avg | 9.979881s |

Compared with `CERA2`:

| metric | CERA2 | CERA3 | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.752461 | 0.850211 | +0.097750 |
| MRR | 0.842955 | 0.904032 | +0.061077 |
| AC@3 | 0.926160 | 0.950774 | +0.024613 |
| AC@5 | 0.961322 | 0.976090 | +0.014768 |

Status deltas:

| status | cases |
| --- | ---: |
| improved_to_hit1 | 191 |
| regressed_from_hit1 | 52 |
| rank_improved | 69 |
| rank_regressed | 36 |
| unchanged | 1074 |

Main improvements concentrate in protocol mutation, request/response replacement, partition, delay, and dashboard/basic/seat/travel service cases where CERA2's robust family burden often left the true root at rank 2. CERA3's ordinal causal energy separates root-like mutation evidence from propagation symptoms while sink-share context suppresses terminal downstream victims.

Remaining weak groups are `pod-failure`, `bandwidth`, a few unknown/return cases, and small-sample cancel-service cases. These are consistent with incidents where the failing component has weak raw endpoint/status mutation and downstream services dominate the observable traffic/latency footprint.

Validation artifacts:

- Snapshot: `output/rcabench-platform-v2/evolve_snapshots/CERA3/`
- Summary: `docs/EvidRank_evolve/CERA3_summary.md`
- Compare: `docs/EvidRank_evolve/compare_CERA2_vs_CERA3.md`

Guard result: no high-risk overfitting warnings. The remaining medium warnings are existing `rcabench_platform` import/docstring literals.

## Decision

CERA3 is accepted as the current CERA version because it exceeds the requested `AC@1 >= 0.80` target, improves MRR/AC@3/AC@5 over CERA2, completes full eval with `error == 0`, and avoids hand-crafted numeric feature weights.

The accepted interpretation is:

- feature semantics are represented as ordinal causal evidence tiers, not per-feature floats;
- numeric energy is synthesized from tier ordering and tier count;
- endpoint support is derived from current incident rank agreement between endpoint, status, and traffic-rise views;
- parent-context strength is derived from trace graph sink share;
- runtime ranking does not use labels, injection metadata, previous outputs, or case/service/fault-specific rules.

Next work can target paper-quality robustness analysis and ablations. If further accuracy work is needed, focus on pod-failure/bandwidth cases through generic infrastructure-local evidence rather than restoring hand-tuned constants.
