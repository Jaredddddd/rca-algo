You are working in an RCABench-style repository that already contains the CREST root cause analysis algorithm.

Your task is to add and evaluate a new CREST variant called CREST-Residual, or `crest_residual`, based on Counterfactual Evidence Residual Ranking.

The goal is to test whether incident-level residual explanatory power can improve service-level root cause ranking over the existing CREST algorithm, while keeping the method nearly parameter-free and avoiding benchmark-specific tuning. 如果已有方法不行，你可以进行小幅调整，目前是 AC@1不变甚至提高。

我的建议是：实现 CREST-Residual 做实验，但主论文仍以原 CREST 为主；只有当它稳定提升 AC@1/MRR 且不过度增加复杂度时，再把它升级为主算法。

# Core idea

Existing CREST uses approximately:

score = A * F + S

where:

* A = incident-local abnormality
* F = structural explanatory power
* S = denoised structural support

CREST already has pairwise counterfactual explain-away over service topology.

The new CREST-Residual module should add an incident-level counterfactual residual signal:

For each candidate root service r, estimate how much observed abnormal evidence across the incident can be explained if r is assumed to be the root mutation. A better root cause should leave less unexplained residual abnormality.

This is not Sage-style generated counterfactual latency prediction. Do not train a model. Do not generate hypothetical telemetry. Use only observed telemetry evidence, existing CREST feature matrices, mutation evidence, propagation evidence, and trace-derived topology.

# Important design constraint

Do not introduce many tunable hyperparameters.

The default algorithm should be nearly parameter-free. The only optional sensitivity parameter allowed is:

eta, default 1.0

Do not tune eta silently. If sensitivity is run, report it separately as exploratory.

# Step 1: Inspect the repository

First inspect the repository and locate:

* existing CREST implementation
* helper functions used by CREST
* algorithm registration mechanism
* benchmark execution scripts
* result aggregation scripts
* existing output/result format
* existing per-case ranking format, if available

Do not assume file names. Search and read the code.

Do not hardcode absolute paths.

# Step 2: Add a new algorithm variant

Add a new algorithm variant named preferably:

* class name: CRESTResidual
* algorithm name: crest_residual

Keep the original `crest` behavior unchanged.

Do not modify the semantics of existing algorithms.

Prefer adding a new scoring mode or small helper functions rather than copying the entire CREST implementation.

# Step 3: Reuse existing CREST internals

Reuse the existing CREST logic wherever possible:

* input loading
* service collection
* enabled modalities
* feature matrix construction
* incident-local robust calibration
* role/evidence matrix
* mutation feature set
* propagation feature set
* weighted trace graph construction
* graph decay
* parent context
* counterfactual explain-away if needed
* denoised structural support
* final DataFrame sorting and ranking

The new module should reuse the same A, F, and S values as CREST when available.

If A, F, and S are not currently exposed cleanly, refactor minimally so both CREST and CRESTResidual can share a diagnostic scoring function.

# Step 4: Compute mutation and propagation evidence

For each service v, compute:

M[v] = normalized mutation-like evidence
P[v] = normalized propagation-like evidence

Use the existing CREST mutation feature set for M if available, including features such as:

* metric_count_drop_shift
* trace_count_drop_shift
* trace_endpoint_shift
* trace_error_rate
* trace_status_code_shift

Use the existing CREST propagation feature set for P if available, including features such as:

* trace_duration_z
* trace_duration_delta
* trace_self_duration_relative_shift
* trace_count_delta
* trace_count_rise_shift
* abnormal_trace_rows
* log_count_delta
* log_template_delta

Normalize M and P using the existing positive p95 scaling helper if available.

Clip M and P to nonnegative finite values.

# Step 5: Build topology influence K

Use the existing trace-derived weighted graph if available.

Define K[r, v] as the maximum decayed topology influence from candidate root r to target service v.

Use a directed trace graph by default.

Use the existing incident graph decay function if available. Do not add a new custom decay parameter.

Suggested propagation:

* K[r, r] = 1.0
* initialize frontier[r] = 1.0
* repeatedly propagate:
  message = frontier[parent] * edge_weight * decay
* update each child using max influence:
  next_frontier[child] = max(next_frontier[child], message)
* update:
  K[r, child] = max(K[r, child], message)
* stop after at most node_count steps or when the frontier becomes negligible
* clip K to [0, 1]

This avoids introducing a max_hops hyperparameter while still preventing infinite loops.

# Step 6: Compute residual explanatory power R

For each candidate root r and each service v:

Explain[r, v] = M[r] * K[r, v] * P[v]

Then cap explanation by observed abnormality:

Explain[r, v] = min(A[v], Explain[r, v])

Compute residual abnormality:

Residual[r] = sum_v max(0, A[v] - Explain[r, v])

Compute null residual:

Residual_null = sum_v A[v] + epsilon

Compute residual explanatory power:

R[r] = 1 - Residual[r] / Residual_null

Clip R to [0, 1].

Interpretation:

* R is high if candidate root r can explain a large fraction of observed abnormal evidence.
* R is low if r cannot explain the incident-level abnormality pattern.
* R should not boost unrelated topology-central services unless they also have mutation evidence M.

# Step 7: Integrate residual power into CREST

Do not add R as an arbitrary weighted score term.

Instead, use R as an alternative estimate of structural explanatory power and gate it by mutation evidence.

Default formula:

F_residual[r] = F[r] + M[r] * max(0, R[r] - F[r])

score_residual[r] = A[r] * F_residual[r] + S[r]

This means:

* residual explanatory power can only improve a service if it has mutation evidence;
* R cannot reduce the original CREST structural power;
* R cannot arbitrarily boost topology-central services without mutation evidence;
* the final formula remains close to CREST’s original score = A * F + S.

Optional sensitivity formula:

F_residual[r] = F[r] + eta * M[r] * max(0, R[r] - F[r])

score_residual[r] = A[r] * F_residual[r] + S[r]

Default eta = 1.0.

Only run eta sensitivity as exploratory analysis with:

eta in {0.25, 0.5, 1.0, 2.0}

Do not tune eta silently. The main reported result must use eta = 1.0.

# Step 8: Fallback behavior

The new variant must be robust to missing telemetry.

If graph is unavailable:

* fall back to original CREST score if available;
* otherwise fall back to A.

If mutation evidence is unavailable or all zero:

* fall back to original CREST score if available;
* otherwise fall back to A.

If propagation evidence is unavailable or all zero:

* fall back to original CREST score if available;
* otherwise fall back to A.

The new algorithm must not crash due to missing metrics, logs, traces, or topology.

# Step 9: Diagnostics export

Add an optional diagnostic export for CRESTResidual.

When an output path is provided, export per-case per-service diagnostics with columns such as:

* case_id, if available
* service
* A
* F
* S
* M
* P
* R
* residual
* F_residual
* original_crest_score
* residual_score
* final_score
* final_rank

Prefer CSV or Parquet, matching the repository’s existing style.

Do not change the default benchmark output format unless necessary.

# Step 10: Register the new algorithm

Register `crest_residual` in the same way existing algorithms are registered.

The existing algorithms must still run unchanged, especially:

* crest
* crest_local
* crest_nocf
* crest_metric
* crest_trace
* crest_log
* crest_metric_trace
* crest_metric_log
* crest_log_trace

# Step 11: Run benchmark comparison

Run CRESTResidual on the same RCABench cases used by existing CREST results.

Compare at least:

* crest
* crest_residual
* crest_local
* crest_nocf
* crest_metric_trace
* crest_trace
* strongest non-CREST baseline if available

Report:

* total cases
* error count
* runtime mean
* runtime median, if available
* runtime p95, if available
* MRR
* AC@1
* AC@3
* AC@5
* Avg@3 and Avg@5 only if already defined by the benchmark

Use paired cases whenever possible.

Do not compare algorithms on different case sets without clearly reporting that limitation.

# Step 12: Statistical analysis

If per-case ranks are available, compute paired comparisons:

* crest_residual vs crest
* crest_residual vs crest_local
* crest_residual vs crest_nocf
* crest_residual vs crest_metric_trace

For each comparison, compute:

* paired MRR difference
* paired AC@1 difference
* paired AC@3 difference
* paired AC@5 difference
* bootstrap 95% confidence interval
* empirical probability that the difference is greater than 0

Use fixed random seed.

Default bootstrap iterations: 1000.

Allow 10000 through CLI if feasible.

# Step 13: Optional eta sensitivity

If time allows, run eta sensitivity:

eta in {0.25, 0.5, 1.0, 2.0}

Output:

* MRR
* AC@1
* AC@3
* AC@5
* runtime

Save as:

analysis/crest_residual/output/residual_eta_sensitivity.csv

Clearly state that eta sensitivity is exploratory and should not be treated as tuned test performance unless a separate validation split exists.

# Step 14: Case study extraction

If per-case rankings and diagnostics are available, extract:

1. residual wins:
   crest_residual Top-1 correct, crest Top-1 wrong

2. residual losses:
   crest Top-1 correct, crest_residual Top-1 wrong

3. counterfactual wins:
   crest_residual or crest Top-1 correct, but crest_local or crest_nocf Top-1 wrong

For each case, report:

* case id
* ground truth root service
* top-5 ranking for crest
* top-5 ranking for crest_residual
* top-5 ranking for crest_local or crest_nocf if relevant
* A / F / S / M / P / R / F_residual / final score for top services
* short explanation of why residual ranking helped or hurt

Save as:

analysis/crest_residual/output/residual_case_studies.md

# Step 15: Output structure

Create or update:

analysis/crest_residual/
README.md
analyze_residual_results.py, if needed
run_residual_experiment.py, if needed
output/
residual_summary.csv
residual_summary.md
residual_vs_crest_significance.csv
residual_eta_sensitivity.csv, if run
residual_case_studies.md, if available
diagnostics/
crest_residual_scores.csv or .parquet, if diagnostic export is enabled

# Step 16: README requirements

The README should explain:

1. What CREST-Residual adds.
2. How CREST-Residual differs from original CREST.
3. Why the design is nearly parameter-free.
4. How to run the benchmark.
5. How to aggregate results.
6. How to reproduce the comparison with original CREST.
7. What output files are generated.
8. Which input files are required.
9. Known limitations.

# Step 17: Important constraints

* Do not delete original benchmark results.
* Do not overwrite original result files unless explicitly requested.
* Do not break existing algorithm names.
* Do not change original `crest` behavior.
* Do not use ground truth during scoring.
* Do not train any model.
* Keep changes minimal and easy to review.
* Add docstrings to new functions.
* Add comments explaining the residual formula.
* Handle missing telemetry gracefully.
* Fix random seeds for statistical analysis.
* Avoid hardcoded absolute paths.
* Make scripts runnable from the repository root.

# Step 18: Final response expected

After implementation and experiments, report:

1. Files changed.
2. New algorithm names added.
3. Exact commands used.
4. Whether the benchmark ran successfully.
5. Overall table comparing crest_residual, crest, crest_local, crest_nocf, and crest_metric_trace.
6. Whether crest_residual improves MRR, AC@1, AC@3, or AC@5 over crest.
7. Runtime overhead compared with crest.
8. Eta sensitivity results, if run.
9. Win/loss case study findings, if available.
10. Any failures, missing files, or assumptions.

Be honest if CRESTResidual does not improve performance. If it does not improve, analyze likely causes, such as:

* original CREST is already saturated;
* residual signal duplicates existing F or S;
* mutation evidence is too sparse;
* propagation evidence is too noisy;
* topology influence is too diffuse;
* residual gate is too conservative;
* benchmark does not contain enough cases where incident-level residual helps.
