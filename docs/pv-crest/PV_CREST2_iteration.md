# PV_CREST2 Iteration

## Fresh Baseline

Current working-tree `crest` was freshly evaluated before this iteration:

| dataset | total | error | AC@1 | MRR | AC@3 | AC@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aiopschallenge2025_rcabench_service` | 230 | 0 | 0.334783 | 0.503603 | 0.600000 | 0.669565 |
| `rcabench` | 1422 | 0 | 0.800281 | 0.875326 | 0.944444 | 0.971871 |

AIOps25 needs 161 top-1 hits to reach `AC@1=0.70`; current `crest` has 77,
so the gap is 84 Hit@1.

`PV_CREST1_PARTIAL` is rejected: it improved AIOps25 to `AC@1=0.430435` but
dropped RCABench to `AC@1=0.492264`.

## Hypothesis

Current CREST aggregates evidence as `A * F + S`, so high-observability trace
surfaces can dominate even when root-local mutation is only visible through
metric/log/resource provenance. The new mechanism should infer latent roles
inside each incident:

- root-local mutation;
- propagation symptom;
- exposure / observability surface;
- weak/noisy evidence.

This version tests a minimal partial-view causal intervention:

1. Convert existing CREST family burdens plus generic service-level provenance
   into evidence atoms.
2. Infer per-candidate latent role vectors from incident-local robust scales.
3. In the current top-head, compare candidate root responsibility after masking
   exposure atoms.
4. Allow one challenger to pass the current winner only when its root-local
   atoms explain the winner's propagation/exposure residual through trace
   adjacency or strong default CREST support.

No label, injection, previous output, perf report, dataset name, service name,
fault name, SimpleRCA output, or `conclusion.parquet` is used by runtime code.

## Evidence Atoms

Initial atom families:

- metric root atoms: metric shift burden plus service-local provenance
  concentration from generic pod/instance/object/KPI/resource keys;
- log root atoms: log shift burden;
- trace root atoms: trace mutation not explained by trace propagation;
- trace propagation atoms: duration/count/self-duration propagation burden;
- trace exposure atoms: abnormal trace row burden, topology context, and
  propagation-heavy trace mass;
- weak/noise atoms: residual low-binding mass after root/propagation/exposure
  assignment.

Provenance is service-level evidence only. Pod, instance, object, KPI, device,
mountpoint, and metric-group keys can support their parent service, but they
are never emitted as final answers. If provenance columns are absent or
uninformative, the atom naturally has zero mass.

## Intervention Design

For candidate `c`:

- `z_root(c)` comes from metric/log/provenance root atoms and trace mutation
  residual;
- `z_prop(c)` comes from propagation trace atoms;
- `z_exposure(c)` comes from trace row volume, topology context, and
  propagation-heavy exposure mass;
- `root_responsibility(c)` estimates how much incident residual is explained
  by preserving root atoms while masking exposure atoms.

The reranker only inspects the current incident head with size derived from the
candidate count (`ceil(sqrt(N))`). This is a scale rule, not a tuned dataset
cutoff.

A challenger may replace the winner only by incident-local Pareto evidence:

- challenger has greater root responsibility than the winner;
- winner has greater exposure responsibility than challenger;
- challenger is connected to the winner through trace adjacency, or the base
  CREST head already supports the challenger;
- challenger remains above the winner when exposure atoms are masked;
- winner is not protected by stronger trace-mutation root responsibility.

This is intended to be a counterfactual intervention, not `base + bonus -
penalty`.

## Validation Plan

1. Implement as `pv_crest_role_intervention` ablation; do not promote default
   `crest` until validation.
2. Run `compileall` and `evidrank_lab.py guard`.
3. Full eval on AIOps25 service and RCABench.
4. Snapshot and summarize both outputs.
5. Compare against fresh baseline with cross-algorithm offline compare if
   needed.
6. Accept only if AIOps25 improves and RCABench does not fall below the stated
   guardrail. If `0.77 <= RCABench AC@1 < baseline`, mark as trade-off and do
   not auto-accept.
