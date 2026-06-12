# Domain Docs

This is a multi-context algorithm repository. Engineering skills should read the context that matches the algorithm area being changed.

## Before exploring, read these

- `AGENTS.md` at the repo root for global repository rules.
- `CONTEXT-MAP.md` at the repo root if it exists. It points to per-context `CONTEXT.md` files.
- The relevant per-context `CONTEXT.md` for the algorithm or subsystem being changed.
- `docs/adr/` for system-wide architectural decisions, if it exists.
- Context-scoped ADRs under the relevant algorithm directory, if they exist.

If any of these files do not exist, proceed silently. Do not suggest creating them upfront; producer skills such as `/grill-with-docs` can create them lazily when terminology or decisions are clarified.

## Known contexts

### EvidenceRank / CREST

Primary current development area:

- `algorithms/evidencerank/src/evidencerank/crest.py`
- `algorithms/evidencerank/src/evidencerank/`
- `docs/EvidRank_evolve/`
- `docs/crest_evolve/`
- `VibeResearchTools/VibeResearch.md`

The user intends to continue CREST-related development and may later extract this algorithm into a separate directory under `algorithms/`.

## Use the glossary's vocabulary

When output names a domain concept in an issue title, refactor proposal, hypothesis, or test name, use the term defined in the relevant `CONTEXT.md`.

If the concept is not in the glossary yet, either reconsider the wording or note it as a gap for `/grill-with-docs`.

## Flag ADR conflicts

If output contradicts an existing ADR, surface it explicitly rather than silently overriding it.
