# CREST-MEO Phase 1 Implementation

## Goal

Phase 1 adds a deterministic CREST-MEO path that turns a frozen JSON Meta
Evidence Operator Library (MEOL) into service-level evidence features and
counterfactual role membership for CREST ranking.

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
- `algorithms/evidencerank/src/evidencerank/meo/library/crest_builtin_meol.json`
- `algorithms/evidencerank/src/evidencerank/crest.py`
- `algorithms/evidencerank/src/evidencerank/crest_meo.py`
- `VibeResearchTools/export_crest_builtin_meol.py`

## MEOL Library Provenance

当前有两个用途不同的 MEOL 文件：

`default_meol.json` 是 Phase-1 的 mock LLM 输出。它由
`algorithms/evidencerank/src/evidencerank/meo/llm/mock_outputs.py` 中的
`mock_meol()` 提供，包含 10 个机制化 seed operators，例如
`metric_max_z`、`trace_status_code_shift`、`trace_error_rate`、
`trace_duration_delta` 和 `log_template_delta`。它的作用是跑通
“prompt/context -> mock LLM response -> verifier -> compiler -> CREST-MEO
ranking” 这条链路，不是从当前 CREST 的 hard-coded constants 自动生成的。

`crest_builtin_meol.json` 是一个对照/消融库，由
`VibeResearchTools/export_crest_builtin_meol.py` 从当前 CREST/CERA 源码机械导出：

- operator 顺序严格等于 `BASE_FEATURE_NAMES`，共 21 个；
- operator 名字严格等于原 CREST feature 名字，因此 CREST-MEO 可以走
  `_build_feature_matrix` fast path；
- `CREST_COUNTERFACTUAL_MUTATION_FEATURES` 中的 feature 被转换为
  `role_prior.mutation = 1.0`；
- `CREST_COUNTERFACTUAL_PROPAGATION_FEATURES` 中的 feature 被转换为
  `role_prior.propagation = 1.0`；
- 其余 CREST feature 被转换为 neutral，也就是
  `role_prior.mutation = 0.0` 且 `role_prior.propagation = 0.0`；这些 feature
  仍参与 CREST local evidence energy 和 denoised support，但不参与
  counterfactual mutation/propagation 对比。

这个转换的目标是让你能直接查看“当前 CREST hard-coded feature/role set 的
JSON MEOL 表达”。当前 `crest_meo_builtin` 的在线 scoring 已经刻意复刻原
hard-coded CREST：同一批 feature columns、同一个 endpoint support gate、同一个
parent context、同一个 hard counterfactual explain-away、同一个 denoised support。
因此它应理解为“CREST scorer 的 MEOL 配置化入口”。

重新生成命令：

```bash
uv run --package evidencerank python VibeResearchTools/export_crest_builtin_meol.py
```

直接用该库跑 CREST-MEO：

```python
from pathlib import Path
from evidencerank.crest import score_crest_services

ranking = score_crest_services(
    input_folder,
    use_meo=True,
    meol_path=Path(
        "algorithms/evidencerank/src/evidencerank/meo/library/crest_builtin_meol.json"
    ),
)
```

Benchmark CLI 中也注册了一个显式算法名：

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch \
  -a crest_meo_builtin \
  -d rcabench \
  --clear \
  --use-cpus 48
```

对应关系是：

- `-a crest_meo`：使用 `default_meol.json`，也就是 mock LLM seed library；
- `-a crest_meo_builtin`：使用 `crest_builtin_meol.json`，也就是当前 CREST 21 个
  built-in feature 的机械 MEOL 导出库。

## Runtime Behavior

`use_meo=False` keeps the existing CREST path. `use_meo=True` loads
`default_meol.json` unless an explicit `meol_path` is provided. MEOL controls
which operators become feature columns and which columns enter the
counterfactual mutation / propagation sets. The online scoring logic then
reuses CREST exactly:

- `_build_feature_matrix(..., normalize=True)` for built-in feature aliases;
- `_robust_case_feature_matrix`;
- `_apply_arc_trace_endpoint_support_gate`;
- CREST local family energy;
- parent context;
- hard counterfactual explain-away;
- CREST denoised structural support;
- final `score = A * F + S`.

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

- `pytest`: 12 passed.
- `compileall`: passed.
- config-driven mock synthesis CLI: passed and wrote non-empty JSON.
- prompt construction: passed.
- `ruff check`: passed.
- default MEOL static/leakage verifier check: 10 operators, no errors.
- CREST built-in MEOL equivalence check: 21 operators, mutation/propagation sets
  match the current hard-coded CREST constants, and a smoke input has identical
  `A/F/S/score` to `crest`.
- guard: no high-risk overfitting warnings; only pre-existing medium
  `rcabench_platform` import/name warnings were reported.

Full benchmark evaluation is not part of Phase 1 acceptance; this phase is
about getting JSON MEOL -> compiler -> feature matrix -> CRESTMEO ranking
running without introducing online LLM calls or answer-metadata leakage.

## Runtime Optimization

CREST-MEO now has a general grouped execution path rather than a purely
operator-by-operator interpreter. For each incident, the MEOL is loaded once,
operators are filtered by enabled modality, and the `EvidenceCompiler` caches
normal/abnormal telemetry slices grouped by source and service. Metric, trace,
and log operators that share the same source therefore reuse the same
service-level frame groups instead of repeatedly filtering the full DataFrame
for every operator.

The default MEOL also has a compatibility fast path: when every enabled
operator name maps directly to an existing CREST/CERA feature name, CREST-MEO
uses the existing batched `_build_feature_matrix(..., normalize=True)`
implementation. Custom operators that do not map to built-in CREST features
still fall back to the general grouped compiler path, preserving DSL
compatibility.

Validation on one RCABench case after the optimization:

```text
case=ts7-mysql-partition-wk622l
crest avg     3.6187s over 5 runs
crest_meo avg 3.5271s over 5 runs
```

Verification commands:

```bash
uv run --package evidencerank pytest algorithms/evidencerank/tests/test_meo_phase1.py -q
uv run --package evidencerank python -m compileall -q algorithms/evidencerank/src/evidencerank/meo algorithms/evidencerank/src/evidencerank/crest.py
uv run --package evidencerank ruff check algorithms/evidencerank/src/evidencerank/meo/dsl/compiler.py algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/tests/test_meo_phase1.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
```

## CREST Built-In MEOL Equivalence

`crest_builtin_meol.json` 现在是原 CREST scorer 的配置化入口，而不是 soft role-vector
ablation。它通过 MEOL 提供：

- 21 个 `BASE_FEATURE_NAMES`；
- counterfactual mutation membership；
- counterfactual propagation membership；
- `denoised_channel_excludes = ["trace_duration_z"]`。

在线路径不再使用 `mutation + propagation` 的 soft denoised support，而是复用原 CREST
的 hard explain-away 和 denoised structural support。当前真实 case smoke 已确认：

```text
ts0-ts-basic-service-response-replace-code-lmnjw7 equal
ts0-ts-auth-service-stress-nlpsfx equal
ts0-ts-food-service-container-kill-fc4sjw equal
ts7-mysql-partition-wk622l equal
```

最终验收要求是 full benchmark 中 `crest_meo_builtin` 的 `AC@1/MRR/AC@3/AC@5`
与 `crest` 完全一致。
