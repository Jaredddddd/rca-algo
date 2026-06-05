# Design New Algorithm

This is the main page for designing a new unsupervised RCA algorithm that learns from the current EvidenceRank codebase without becoming a renamed copy of EvidenceRank.

## Research Entry

- Existing probe / teacher baseline: `algorithms/evidencerank`
- Current default implementation: `algorithms/evidencerank/src/evidencerank/algorithm.py`
- New-algorithm iteration docs: `docs/NewAlgo/`
- Main coding-agent prompt: `docs/NewAlgo/CodingAgentPrompt.md`
- Design brief: `docs/NewAlgo/CERA_design_brief.md`
- Existing EvidenceRank evolution docs: `docs/EvidRank_evolve/`
- Existing no-fixed-prior ARC line: `docs/EvidRank-ARC-Evolve/`
- Labels for offline evaluation only: `data/rcabench-platform-v2/meta/rcabench-csv/labels.csv`
- Case metadata for offline analysis only: `data/rcabench-platform-v2/data/rcabench/<datapack>/injection.json`

## Current Position

EvidenceRank has become a strong dataset probe. It demonstrates that an unsupervised RCA algorithm needs at least these capabilities to perform well on RCABench:

- robust per-case normalization over heterogeneous metric, trace, and log scales;
- endpoint / status / traffic mutation signals reconstructed from raw traces;
- separation between root-like mutation evidence and propagation-like victim symptoms;
- conservative topology reasoning over trace parent-child edges;
- evidence-family reliability rather than free per-feature self-weighting;
- safeguards against high-volume entry services and downstream victims stealing top-1.

The simple EvidenceRank scoring form is not enough as a top-conference method because it is still largely an interpretable feature-priority ranker. The new research goal is to turn the same empirical capability map into a more novel unsupervised method with latent causal roles, self-supervised evidence reliability, and topology-aware explain-away inference.

## Current Status

- `CERA3` is the current accepted standalone CERA version.
- Implementation module: `algorithms/evidencerank/src/evidencerank/cera.py`
- Registry name: `cera`
- Default EvidenceRank implementation remains unchanged.
- CERA3 full eval on `rcabench`: `total=1422`, `error=0`, `AC@1=0.850211`, `MRR=0.904032`, `AC@3=0.950774`, `AC@5=0.976090`.
- CERA3 mechanism: raw log-normalized incident features are mapped to ordinal causal evidence tiers; the numeric energy ladder is synthesized from tier ordering and tier count; ARC endpoint support is derived from current rank agreement; parent-context strength is derived from trace graph sink share.
- Key CERA3 lesson: the route to a publishable no-handcrafted-numeric-weight algorithm is not free rank fusion. It is a semantic ordinal evidence taxonomy plus incident-derived topology support. Remaining weaknesses are mainly pod-failure, bandwidth, and other low-mutation infrastructure cases.

## Proposed Method Line

Working name: **CERA**, Causal Evidence Role Alignment.

Alternative paper-facing names may be chosen later, but the coding agent should initially use `cera` or `latent_role_rca` as the registry name so it is evaluated separately from `evidencerank`.

Core idea:

1. Treat observability features as ordinal causal evidence roles rather than per-feature numeric weights.
2. Convert raw metrics, traces, logs, and topology into incident evidence energy, reusing EvidenceRank's raw extraction logic where appropriate.
3. Derive endpoint support from current endpoint/status/traffic-rank agreement.
4. Derive topology parent-context strength from the current trace graph's sink share.
5. Rank services by root-causal evidence energy after incident-derived endpoint and topology alignment.
6. Use EvidenceRank as a probe and behavioral target during research, but do not call EvidenceRank or copy its final weighted-sum scoring as the new algorithm.

## Work Standard

The new algorithm must first become a working standalone method:

- `guard` has no high-risk overfitting warnings;
- full eval completes with `error == 0`;
- AC@1 is at least `0.60`;
- iteration documentation exists in `docs/NewAlgo/`;
- outputs are snapshotted and compared.

After that, iterate toward the current EvidenceRank level:

- milestone A: AC@1 >= `0.60`, method works;
- milestone B: AC@1 >= `0.70`, method is competitive with unsupervised ARC-style baselines;
- milestone C: AC@1 >= `0.75`, method is strong enough for serious ablation;
- milestone D: AC@1 near `0.80`, method approaches the current EvidenceRank probe.

## Required Commands

Use these from the repository root:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a cera -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CERA<N> --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CERA<N> --source CERA<N> --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old CERA<N-1> --new CERA<N> --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

If the final registry name is not `cera`, replace `cera` consistently in all commands and docs.

## Index

- [NewAlgo README](../docs/NewAlgo/README.md)
- [CERA Design Brief](../docs/NewAlgo/CERA_design_brief.md)
- [Coding Agent Prompt](../docs/NewAlgo/CodingAgentPrompt.md)
- [CERA1 Iteration](../docs/NewAlgo/CERA1_iteration.md)
- [CERA1 Summary](../docs/EvidRank_evolve/CERA1_summary.md)
- [CERA1 RAW vs CERA1 Compare](../docs/EvidRank_evolve/compare_CERA1_RAW_vs_CERA1.md)
- [CERA2 Iteration](../docs/NewAlgo/CERA2_iteration.md)
- [CERA2 Summary](../docs/EvidRank_evolve/CERA2_summary.md)
- [CERA1 vs CERA2 Compare](../docs/EvidRank_evolve/compare_CERA1_vs_CERA2.md)
- [CERA3 Iteration](../docs/NewAlgo/CERA3_iteration.md)
- [CERA3 Summary](../docs/EvidRank_evolve/CERA3_summary.md)
- [CERA2 vs CERA3 Compare](../docs/EvidRank_evolve/compare_CERA2_vs_CERA3.md)
