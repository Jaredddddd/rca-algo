# CREST-MEO Phase 1 Implementation

## Goal

Phase 1 adds a deterministic CREST-MEO path that turns a frozen JSON Meta
Evidence Operator Library (MEOL) into service-level evidence features and role
vectors for CREST ranking.

Implemented scope:

- JSON MEOL schema parsing.
- Robust DSL atoms for numeric, count, categorical, and error-rate contrasts.
- Deterministic compiler for metric, trace, log, and placeholder topology
  sources.
- Runtime instantiation into `feature_matrix`, `feature_names`, and
  `role_weight_matrix`.
- Static, leakage, and dynamic verifier helpers.
- Config-driven offline LLM synthesis scaffold. The default config uses mock
  output; no real LLM call is made unless config and CLI both opt in.
- Optional `use_meo=True` path in `score_crest_services`.
- New `CRESTMEO` class and `crest_meo` registry name.

## Key Files

- `algorithms/evidencerank/src/evidencerank/meo/dsl/schema.py`
- `algorithms/evidencerank/src/evidencerank/meo/dsl/atoms.py`
- `algorithms/evidencerank/src/evidencerank/meo/dsl/compiler.py`
- `algorithms/evidencerank/src/evidencerank/meo/runtime/load_meol.py`
- `algorithms/evidencerank/src/evidencerank/meo/runtime/instantiate.py`
- `algorithms/evidencerank/src/evidencerank/meo/verify/`
- `algorithms/evidencerank/src/evidencerank/meo/llm/`
- `algorithms/evidencerank/src/evidencerank/meo/llm/config.yaml`
- `algorithms/evidencerank/src/evidencerank/meo/artifacts/telemetry_schema.py`
- `algorithms/evidencerank/src/evidencerank/meo/library/default_meol.json`
- `algorithms/evidencerank/src/evidencerank/crest.py`

## Runtime Behavior

`use_meo=False` keeps the existing CREST path. `use_meo=True` loads
`default_meol.json` unless an explicit `meol_path` is provided, compiles each
operator, executes operators against the current incident frames, scales the
result with `_robust_case_feature_matrix`, and computes:

- `mutation`
- `propagation`
- `observability_bias`
- `topology_context`

The counterfactual mode then uses parent context plus the new soft explain-away
routine over MEO `mutation` and `propagation` role vectors.

If an individual operator fails, its feature column is zeroed. If the whole
MEOL path produces no positive local abnormality, the function falls back to
the original CREST path rather than crashing.

## Offline LLM Synthesis Flow

The offline synthesis CLI is now config-driven:

```bash
uv run --package evidencerank python -m meo.llm.synthesize \
  --config algorithms/evidencerank/src/evidencerank/meo/llm/config.yaml \
  --mock \
  --output /tmp/default_meol.json
```

Default behavior:

- `config.yaml` sets `synthesis.mode=mock` and `llm.provider=mock`.
- All mock content is centralized in
  `algorithms/evidencerank/src/evidencerank/meo/llm/mock_outputs.py`.
- The CLI still builds the same prompt shape that a real LLM will receive:
  artifact summary, telemetry schema, mechanism catalog, DSL atoms, and safety
  rules.
- The mock client returns `mock_meol()`.
- Static and leakage verifiers run before writing the MEOL file.

Prompt inspection:

```bash
uv run --package evidencerank python -m meo.llm.synthesize --mock --print-prompt
```

Real LLM path:

1. Edit `config.yaml`: set `synthesis.mode=real`,
   `synthesis.allow_real_llm=true`, `llm.provider=openai`, and `llm.model`.
2. Set the API key environment variable named by `llm.api_key_env`.
3. Run with the additional CLI guard:

```bash
uv run --package evidencerank python -m meo.llm.synthesize \
  --config algorithms/evidencerank/src/evidencerank/meo/llm/config.yaml \
  --allow-real-llm \
  --output /tmp/llm_meol.json
```

The double opt-in is deliberate: online CREST-MEO must remain deterministic,
and accidental external calls during tests or benchmark evaluation are not
allowed.

## Verification Results

Completed smoke verification:

```bash
uv run --package evidencerank pytest algorithms/evidencerank/tests/test_meo_phase1.py
uv run --package evidencerank python -m meo.llm.synthesize --mock --output /tmp/default_meol.json
uv run --package evidencerank python -m meo.llm.synthesize --mock --print-prompt
uv run --package evidencerank python -m compileall -q algorithms/evidencerank/src/evidencerank/meo algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py
uv run --package evidencerank ruff check algorithms/evidencerank/src/evidencerank/meo algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py algorithms/evidencerank/tests/test_meo_phase1.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
```

Results:

- `pytest`: 6 passed.
- `compileall`: passed.
- config-driven mock synthesis CLI: passed and wrote non-empty JSON.
- prompt construction: passed.
- `ruff check`: passed.
- default MEOL static/leakage verifier check: 10 operators, no errors.
- guard: no high-risk overfitting warnings; only pre-existing medium
  `rcabench_platform` import/name warnings were reported.

Full benchmark evaluation is not part of Phase 1 acceptance; this phase is
about getting JSON MEOL -> compiler -> feature matrix -> CRESTMEO ranking
running without introducing online LLM calls or answer-metadata leakage.
