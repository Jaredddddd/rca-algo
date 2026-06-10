You are Codex. Implement the CREST-MEO extension described below.
详细的设计文档在/home/ljw/paper/aegis/rca-algo-contrib/docs/crest_meo/design.md中，目前实现的 crest 在/home/ljw/paper/aegis/rca-algo-contrib/algorithms/evidencerank/src/evidencerank/crest.py中，请忽略其他变体，专注于 crest。

我将把你设置为 goal 模式，每次 compact 之后，都要回顾/home/ljw/paper/aegis/rca-algo-contrib/docs/crest_meo/design.md，保证设计不偏离。

Goal:
Add an optional MEO path to the existing CREST algorithm. MEO stands for Mechanism-grounded Evidence Operator Synthesis. It replaces hard-coded feature role sets with a JSON-based Meta Evidence Operator Library, MEOL. The LLM part should be mocked for now. Do not call any real LLM. The online RCA path must remain deterministic.

先让完成 Phase 1 最小可用版本，也就是 JSON MEOL → compiler → feature matrix → CRESTMEO ranking 跑通。真实 LLM、源码 mining、prompt 工程可以后置；现在最重要的是把 hard-coded feature roles 抽象成 MEOL 机制，这样你的论文叙事和代码结构就对齐了。

Current context:
The existing CREST implementation already has:

* score_crest_services(...)
* CREST, CRESTResidual, CRESTLocal, CRESTNoCF, CRESTMetric, CRESTTrace, CRESTLog, etc.
* _build_feature_matrix(...)
* _robust_case_feature_matrix(...)
* _saturating_incident_scale(...)
* _apply_parent_context(...)
* _apply_counterfactual_explain_away(...)
* _crest_residual_diagnostics(...)
* _weighted_trace_graph(...)
* _trace_density_context_weight(...)

Implement the following:

1. Add a new package or module path named meo/ under the same algorithm package.

Required files:

* meo/dsl/schema.py
* meo/dsl/atoms.py
* meo/dsl/compiler.py
* meo/runtime/load_meol.py
* meo/runtime/instantiate.py
* meo/verify/static_verifier.py
* meo/verify/leakage_verifier.py
* meo/verify/dynamic_verifier.py
* meo/llm/prompts.py
* meo/llm/mock_outputs.py
* meo/llm/synthesize.py
* meo/library/default_meol.json

2. Implement DSL schema.

Create dataclasses:

* SignalSpec
* ContrastSpec
* AggregationSpec
* EvidenceOperatorSpec

Fields:
EvidenceOperatorSpec:

* name: str
* source: metric | log | trace | topology
* entity: service | endpoint | edge | log_template | status_code
* signal: SignalSpec
* contrast: ContrastSpec
* aggregation: AggregationSpec
* role_prior: dict[str, float]
* mechanism: str
* required_fields: list[str]
* rationale: str

Implement parse_operator_spec(raw: dict) -> EvidenceOperatorSpec.

3. Implement atoms in meo/dsl/atoms.py.

Functions:

* finite_series
* z_shift
* robust_z_shift
* mean_delta
* count_delta
* count_rise
* count_drop
* js_divergence
* is_error_status
* error_rate
* error_rate_delta

All functions must be robust to NaN, inf, empty arrays, zero denominators, and return finite non-negative floats.

4. Implement EvidenceCompiler in meo/dsl/compiler.py.

Interface:
FeatureFn = Callable[[dict[str, pd.DataFrame], list[str]], np.ndarray]

class EvidenceCompiler:
def compile(self, spec: EvidenceOperatorSpec) -> FeatureFn

Support source types:

* metric
* trace
* log
* topology

For metric:

* support field "*": all metric columns prefixed with service name.
* support field "**row_count**": service-level row count.
* support contrast operators z_shift, robust_z_shift, mean_delta, count_delta, count_rise, count_drop.

For trace:

* service column aliases: service_name, service, svc
* endpoint aliases: endpoint, operation, operation_name, span_name, http_route, route
* status aliases: status_code, http_status_code, status, code
* duration aliases: duration, duration_ms, latency, elapsed, elapsed_ms
* support distribution_shift, error_rate_delta, z_shift, robust_z_shift, mean_delta, count_delta, count_rise, count_drop.

For log:

* service column aliases: service_name, service, svc
* template aliases: template, log_template, message_template, event_template
* level aliases: level, severity, log_level
* message aliases: message, msg, body, content
* support distribution_shift and count_delta/count_rise/count_drop on "**row_count**".

For topology:

* first version can return zeros.

5. Implement MEOL loading.

meo/runtime/load_meol.py:

* load_meol(path) -> dict
* load_operator_specs(path) -> list[EvidenceOperatorSpec]

6. Implement MEOL runtime instantiation.

meo/runtime/instantiate.py:

* ROLE_ORDER = ["mutation", "propagation", "observability_bias", "topology_context"]
* instantiate_meol_features(frames, services, specs, compiler=None)
  returns:

  * feature_matrix: np.ndarray shape [num_services, num_operators]
  * feature_names: tuple[str, ...]
  * role_weight_matrix: np.ndarray shape [num_operators, 4]

Each operator should be compiled and executed. If one operator fails, it should return zeros instead of crashing. All feature values must be finite and non-negative.

7. Create meo/library/default_meol.json.

Use a mock MEOL with at least these operators:

* metric_max_z
* metric_count_drop_shift
* trace_status_code_shift
* trace_error_rate
* trace_endpoint_shift
* trace_duration_delta
* trace_count_rise_shift
* trace_count_drop_shift
* log_count_delta
* log_template_delta

Each operator must include:

* source
* entity
* signal
* contrast
* aggregation
* role_prior
* mechanism
* required_fields
* rationale

Do not include any ground truth, fault labels, root cause labels, or baseline outputs.

8. Implement verifiers.

static_verifier.py:

* static_verify(spec) -> tuple[bool, list[str]]
  Check source, operator allowlist, role names, role prior normalization, rationale, mechanism.

leakage_verifier.py:

* leakage_verify(spec) -> tuple[bool, list[str]]
  Reject forbidden tokens:
  ground_truth, root_cause, root_service, root_metric, answer, label, rank, torai_wrong, baseline_output.

dynamic_verifier.py:

* dynamic_verify(spec, frames, services, compiler=None) -> tuple[bool, dict[str, float]]
  Compile and execute spec. Report nan_rate, nonzero_rate, variance, max. Reject high NaN rate or zero variance.

9. Implement mock LLM.

meo/llm/prompts.py:

* MEO_OPERATOR_SYNTHESIS_PROMPT string
* DEFAULT_MECHANISM_CATALOG list

meo/llm/mock_outputs.py:

* mock_meol() -> dict
  Return the same structure as default_meol.json.

meo/llm/synthesize.py:
A CLI:
python -m meo.llm.synthesize --mock --output meo/library/default_meol.json

No real LLM calls.

10. Modify existing CREST code.

Add to score_crest_services:
new parameters:

* use_meo: bool = False
* meol_path: Path | None = None

When use_meo=False:

* preserve existing behavior exactly.

When use_meo=True:

* load operator specs from meol_path or default meo/library/default_meol.json
* instantiate MEOL features using current frames and services
* scale feature matrix using existing _robust_case_feature_matrix
* compute role vectors:
  mutation = feature_matrix @ role_weight_matrix[:, 0]
  propagation = feature_matrix @ role_weight_matrix[:, 1]
  observability_bias = feature_matrix @ role_weight_matrix[:, 2]
  topology_context = feature_matrix @ role_weight_matrix[:, 3]
* local_energy = mutation + propagation + observability_bias + topology_context
* local_abnormality = _saturating_incident_scale(local_energy)

Add helper:
_meo_role_vectors(feature_matrix, role_weight_matrix) -> dict[str, np.ndarray]

Add soft explain-away:
_apply_counterfactual_explain_away_once_soft(...)
_apply_counterfactual_explain_away_soft(...)

The soft explain-away should use mutation and propagation vectors directly. Keep the same logic as the existing hard-coded explain-away:

* if candidate root has higher mutation than victim
* and victim has higher propagation than root
* and victim structural energy is higher than root
* transfer part of victim energy to root.

In graph_mode == "counterfactual" and use_meo=True:

* use _apply_parent_context
* then _apply_counterfactual_explain_away_soft
* explanatory_power = _saturating_incident_scale(structural_energy)
* denoised_support can be _saturating_incident_scale(mutation + propagation)
* score = local_abnormality * explanatory_power + denoised_support

If no score is positive but local_abnormality is positive, fallback to local_abnormality.

11. Add a new algorithm class:

class CRESTMEO(CREST):
_use_meo = True
_meol_path = None

It should call score_crest_services(..., use_meo=True, meol_path=self._meol_path).

Do not break existing CREST classes.

12. Add smoke tests if possible:

* atoms return expected finite values.
* compiler can compile trace_status_code_shift and detect a service with changed status code.
* instantiate_meol_features returns matrix and role weights.
* CRESTMEO can be constructed and run on a minimal or existing test input if test fixtures exist.

13. Acceptance criteria:

* Existing CREST path unchanged.
* CRESTMEO path works with default_meol.json.
* No LLM call is made.
* No GT/fault label/baseline output is used.
* All feature values are finite and non-negative.
* role_prior values sum to 1.
* Operator failure does not crash the entire algorithm.
* New modules are type-hinted and reasonably documented.
