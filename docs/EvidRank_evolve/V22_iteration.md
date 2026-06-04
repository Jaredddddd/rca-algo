# EvidenceRank V22-V26 Parameter Simplification

- Created: 2026-06-04T21:27:55+08:00
- Algorithm: `evidencerank`
- Dataset: `rcabench`
- Baseline snapshot: `V21_PARAM_BASELINE`
- Final accepted snapshot: `V26_REMOVE_ADAPTIVE`

## Hypothesis

去掉弱解释性数值门控和自适应缩放。如果 AC@1、MRR、AC@3、AC@5 基本不变，就删除对应在线参数，以降低 ICSE 投稿中“手工调参”的质疑。

## Parameter Groups

- Parent context smoothing: `PARENT_CONTEXT_WEIGHT = 0.05`
- Trace endpoint support gate: `TRACE_ENDPOINT_SUPPORT_STATUS_FACTOR = 2.0`, `TRACE_ENDPOINT_SUPPORT_RISE_FACTOR = 1.5`, `TRACE_ENDPOINT_UNSUPPORTED_PENALTY = 0.5`, `TRACE_ENDPOINT_POST_GATE_FACTOR = 1.75`
- Adaptive modality scaling: `ADAPTIVE_MODALITY_SPAN = 0.08`, `ADAPTIVE_MODALITY_MIN_FACTOR = 0.92`, `ADAPTIVE_MODALITY_MAX_FACTOR = 1.08`

## Ablation Results

| Version | Change | AC@1 | MRR | AC@3 | AC@5 | Top-1 delta | Status counts vs baseline |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `V21_PARAM_BASELINE` | original implementation | 0.827707 | 0.891195 | 0.947257 | 0.974684 | 0 | baseline |
| `V22_NEUTRAL_ALL` | neutralize all three groups | 0.804501 | 0.876950 | 0.941632 | 0.974684 | -33 | 44 regressed_from_hit1, 11 improved_to_hit1 |
| `V23_NO_PARENT` | disable parent context only | 0.817159 | 0.885126 | 0.945851 | 0.974684 | -15 | 15 regressed_from_hit1, 0 improved_to_hit1 |
| `V24_NO_ENDPOINT` | neutralize endpoint gate only | 0.812940 | 0.881532 | 0.941632 | 0.974684 | -21 | 33 regressed_from_hit1, 12 improved_to_hit1 |
| `V25_NO_ADAPTIVE` | neutralize adaptive modality scaling only | 0.827707 | 0.891195 | 0.947257 | 0.974684 | 0 | 1422 unchanged |
| `V26_REMOVE_ADAPTIVE` | delete adaptive modality scaling code | 0.827707 | 0.891195 | 0.947257 | 0.974684 | 0 | 1422 unchanged |

## Interpretation

`V22_NEUTRAL_ALL` loses 33 Top-1 hits, so deleting all listed values is not safe. The loss comes from parent context and endpoint gate, not from adaptive modality scaling.

`PARENT_CONTEXT_WEIGHT = 0.05` is useful under the current implementation. Disabling it loses 15 Top-1 hits and reduces MRR by 0.006069. It is also the easiest of the remaining constants to defend: a small topology-parent smoothing term that prevents child/propagation evidence from completely dominating local evidence.

The endpoint support gate is also useful. Neutralizing it loses 21 Top-1 hits and reduces MRR by 0.009663. It mainly changes Top-1 ordering while AC@5 stays unchanged, which suggests it is resolving competition among already-recalled candidates rather than only adding recall.

Adaptive modality scaling has no measurable value on this benchmark. Neutralizing it yields exactly the same metrics and all 1422 case rankings remain unchanged. Keeping `0.08`, `0.92`, and `1.08` therefore adds explanation burden without benefit.

## Accepted Code Change

Accepted `V26_REMOVE_ADAPTIVE`:

- Removed `ADAPTIVE_MODALITY_SPAN`, `ADAPTIVE_MODALITY_MIN_FACTOR`, and `ADAPTIVE_MODALITY_MAX_FACTOR`.
- Removed `_adaptive_feature_weights`, `_modality_reliability`, and `_top_ranked_service`.
- Simplified `EvidenceRank.__call__` to use the fixed feature weights directly.
- Kept parent context and endpoint gate constants unchanged because their ablations show non-trivial Top-1 loss.

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V21_PARAM_BASELINE --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py snapshot --version V26_REMOVE_ADAPTIVE --algorithm evidencerank --dataset rcabench
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py compare --old V21_PARAM_BASELINE --new V26_REMOVE_ADAPTIVE --algorithm evidencerank --dataset rcabench
```

## Verification

- Final full eval completed on 1422 cases with `error = 0`.
- Final metrics: `AC@1 = 0.827707`, `MRR = 0.891195`, `AC@3 = 0.947257`, `AC@5 = 0.974684`.
- `compare_V21_PARAM_BASELINE_vs_V26_REMOVE_ADAPTIVE.md`: all 1422 cases unchanged.
- guard result: no high-risk overfitting warnings. Existing medium warnings are the platform import/docstring and historical backup files.

## Decision

Accept removal of adaptive modality scaling. Do not remove parent context or endpoint support gate in this round.

For ICSE packaging, describe the accepted simplification as an ablation-driven reduction of free parameters: the online adaptive modality scaling was removed because it had zero case-level effect. The remaining parent and endpoint constants need either a stronger conceptual explanation or a future replacement with data-derived defaults, but current evidence says deleting them would materially reduce RCA accuracy.
