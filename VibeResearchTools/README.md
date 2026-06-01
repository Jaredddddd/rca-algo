# VibeResearchTools

This directory contains evaluation-side tools for EvidenceRank evolution. Run them with the EvidenceRank uv environment so pandas and rcabench dependencies are available:

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py --help
```

Main commands:

- `snapshot`: preserve current `output/rcabench-platform-v2/data/<dataset>/<datapack>/<algorithm>/` results under `output/rcabench-platform-v2/evolve_snapshots/<VERSION>/`.
- `summarize`: combine predictions with `labels.csv` and write false-case reports.
- `compare`: compare two snapshots or output sources.
- `case`: inspect one datapack with prediction top-k, GT, injection metadata and input file summaries. It skips `conclusion.parquet`.
- `guard`: scan EvidenceRank source for obvious label leakage or hardcoded case/service literals.
- `new-note`: create a versioned iteration-note template in `docs/EvidRank_evolve/`.
- `index`: refresh `VibeResearchTools/VibeResearch.md` so it links the current `docs/EvidRank_evolve/*.md` documents and generated artifacts.

These tools may read labels and injection metadata for offline analysis. Algorithm code under `algorithms/evidencerank` must not read those files. Do not use `conclusion.parquet` in either tooling-driven analysis or algorithm code.

`VibeResearchTools/VibeResearch.md` is the main page for Vibe Research context, launch prompts, and the generated document index.
