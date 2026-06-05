# CERA1 Iteration

- Created: 2026-06-05
- Algorithm registry name: `cera`
- Dataset: `rcabench`
- Goal: first standalone CERA implementation with full eval `error == 0` and `AC@1 >= 0.60`

## Hypothesis

If each service is scored by latent role evidence rather than by a direct feature-priority weighted sum, then robustly scaled observability families can separate root-like mutation/local evidence from propagation-heavy victim symptoms well enough for a first working unsupervised RCA algorithm.

## Scope

- Add a new standalone algorithm class, `CERA`, without changing default `evidencerank` or `evidencerank_arc` behavior.
- Reuse only generic raw observability transformations from `algorithm.py`: frame loading, service collection, metric/trace/log feature extraction, trace edges, and robust case scaling.
- Do not read labels, injection metadata, previous outputs, perf reports, historical rankings, ground truth, or `conclusion.parquet` in the runtime algorithm.
- Do not hardcode datapack ids, service names, fault names, random suffixes, or dataset splits.
- Do not call `EvidenceRank` or `EvidenceRankARC` as a teacher or return their rankings.

## Planned Mechanism

1. Build the existing raw service-feature matrix from metrics, traces, logs, and topology.
2. Apply per-case positive-p95 scaling and clip each feature to a bounded nonnegative range.
3. Aggregate features into semantic evidence families:
   - metric magnitude;
   - availability drop;
   - trace protocol mutation;
   - trace latency;
   - trace traffic;
   - local trace duration;
   - log locality;
   - observability volume.
4. Infer role energies:
   - `root` is supported by availability/protocol/log/local metric evidence and multimodal redundancy;
   - `victim` is supported by latency, traffic, and observability volume;
   - `background` is represented implicitly by low family evidence.
5. Apply trace-topology counterfactual explain-away: for each adjacent pair, transfer part of a propagation-heavy neighbor's root score to the stronger mutation/local candidate when the role assignment is more consistent.
6. Rank services by final nonnegative root energy.

## Implementation

- Main implementation: `algorithms/evidencerank/src/evidencerank/cera.py`
- Registry hook: `algorithms/evidencerank/main.py` registers `cera -> CERA`
- `algorithms/evidencerank/src/evidencerank/algorithm.py` is unchanged by CERA1.
- Runtime data boundary: CERA reads only the normal/abnormal metric, trace, and log frames through existing raw extraction helpers. It does not read labels, injection metadata, previous outputs, perf reports, historical rankings, or `conclusion.parquet`.

The first implementation, snapshotted as `CERA1_RAW`, used p95-normalized family views directly:

```text
root_energy = mutation/local/log/metric evidence
              + small propagation support
              - propagation dominance
              + topology explain-away
```

That version completed full eval with `error=0` but failed the work bar:

| version | AC@1 | MRR | AC@3 | AC@5 | decision |
| --- | ---: | ---: | ---: | ---: | --- |
| `CERA1_RAW` | 0.510549 | 0.700399 | 0.893108 | 0.961322 | reject as too soft for top-1 |

The failure mechanism was not missing candidates: `AC@3` and `AC@5` were already high. The issue was that per-family p95 normalization flattened strong individual evidence, so propagation or adjacent services often stayed above the true root at rank 1.

The accepted CERA1 keeps family aggregation but changes the role posterior initialization:

```text
evidence_burden =
  metric_magnitude
  + availability_drop
  + trace_protocol_mutation
  + trace_latency
  + trace_traffic
  + trace_local_latency
  + log_locality
  + observability_volume

root_anchor =
  availability_drop
  + trace_protocol_mutation
  + log_locality
  + trace_local_latency
  + 0.5 * metric_magnitude

victim_energy =
  trace_latency
  + trace_traffic
  + 0.5 * observability_volume

root_energy =
  evidence_burden
  + 0.10 * root_anchor
  - 0.05 * max(victim_energy - root_anchor, 0)
```

Then CERA applies trace-neighbor counterfactual explain-away. Topology degree is not used as a centrality feature in this CERA1 score; topology is used only through trace edges.

## Expected Behavior

- Should improve over simple trace-only or metric/log-only behavior by keeping multiple evidence families active.
- Should reduce high-traffic or high-latency victim top-1 errors through role contrast and trace-neighbor explain-away.
- May still miss cases where fixed semantic priorities from EvidenceRank are crucial, because CERA1 intentionally avoids per-feature priority weights and incident-level reliability learning.

## Validation Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/algorithm.py algorithms/evidencerank/main.py
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a cera -d rcabench --clear --use-cpus 48
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version CERA1 --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py summarize --version CERA1 --source CERA1 --algorithm cera --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py index
```

## Results

Validation completed:

- `uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard`
  - Result: no high-risk overfitting warnings. Only existing medium `rcabench_platform` import/docstring notices.
- `uv run --package evidencerank python -m compileall algorithms/evidencerank/src/evidencerank/algorithm.py algorithms/evidencerank/src/evidencerank/cera.py algorithms/evidencerank/main.py`
  - Result: compile succeeded.
- `LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a cera -d rcabench --clear --use-cpus 48`
  - Result: completed all 1422 cases.
- `uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench`
  - CERA1 result:

| total | error | runtime.avg | AC@1 | MRR | AC@3 | AC@5 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1422 | 0 | 9.597891s | 0.691280 | 0.814367 | 0.933193 | 0.966245 |

Artifacts:

- Snapshot: `output/rcabench-platform-v2/evolve_snapshots/CERA1/`
- Summary: `docs/EvidRank_evolve/CERA1_summary.md`
- Failed first attempt snapshot: `output/rcabench-platform-v2/evolve_snapshots/CERA1_RAW/`
- Failed first attempt summary: `docs/EvidRank_evolve/CERA1_RAW_summary.md`
- Compare: `docs/EvidRank_evolve/compare_CERA1_RAW_vs_CERA1.md`

Compared with `CERA1_RAW`:

| metric | CERA1_RAW | CERA1 | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.510549 | 0.691280 | +0.180731 |
| MRR | 0.700399 | 0.814367 | +0.113968 |
| AC@3 | 0.893108 | 0.933193 | +0.040084 |
| AC@5 | 0.961322 | 0.966245 | +0.004923 |

Status counts:

| status | cases |
| --- | ---: |
| improved_to_hit1 | 342 |
| rank_improved | 134 |
| rank_regressed | 80 |
| regressed_from_hit1 | 85 |
| unchanged | 781 |

Main improvements came from cases where true roots were already rank 2 or 3 under the over-normalized role score: response-replace-code, stress, request-replace-method, container-kill, request-abort, request-replace-path, exception, response-replace-body, response-abort, response-delay, and pod-failure.

Regressions from hit@1 were concentrated in response-replace-code, partition, request-delay, request-replace-method, response-delay, loss, corrupt, bandwidth, response-replace-body, and request-abort. The accepted CERA1 is still below EvidenceRank and EvidRank-ARC, so these regressions should drive CERA2 reliability learning rather than case-specific patches.

## Decision

Accept CERA1 as the first working standalone CERA version.

Reason:

- It is implemented as a new module rather than a renamed EvidenceRank path.
- It does not read labels, injection metadata, outputs, perf reports, historical rankings, ground truth, or `conclusion.parquet`.
- It does not hardcode datapack ids, service names, fault names, random suffixes, or dataset splits.
- It does not call `EvidenceRank` or `EvidenceRankARC` for rankings.
- Full eval completed with `error=0`.
- `AC@1=0.691280`, which exceeds the CERA1 work bar of `0.60`.

Next step for CERA2:

Add incident-local family reliability and EM-style role updates, but keep the CERA1 lesson: reliability should sharpen or calibrate the evidence-burden posterior, not replace it with over-normalized family views.
