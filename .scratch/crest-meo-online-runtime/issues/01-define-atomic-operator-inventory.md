# Define AtomicOperator Inventory

Status: ready-for-agent
Type: HITL

## Parent

.scratch/crest-meo-online-runtime/PRD.md

## What to build

Create a reviewed AtomicOperator inventory for the current CREST-MEO verified feature semantics. The inventory should translate the existing deployable feature set into generic operational evidence semantics, including each operator's source, signal, derived signal if any, contrast, aggregation, support gate, scaling rule, and mutation / propagation / neutral role prior.

This slice is complete when future implementation agents can update MEOL JSON and the compiler without inferring hidden semantics from feature names or old column bindings.

## Acceptance criteria

- [ ] The inventory covers every currently deployable CREST-MEO feature, including metric, trace, log, topology, and abnormal row volume signals.
- [ ] Ambiguous semantics are explicitly resolved, including operation/span endpoint shift, joint operation/status residual shift, trace self-duration relative increase, log keyword error-rate, and template fallback behavior.
- [ ] The inventory distinguishes generic operational semantics from old feature-column names and avoids `runtime_binding`, `feature_column`, and `extracted_feature_column` terminology.
- [ ] The inventory records whether each feature contributes mutation, propagation, or neutral role membership.
- [ ] The PRD or current design document links to the approved inventory so later issues can treat it as the semantic contract.

## Blocked by

None - can start immediately
