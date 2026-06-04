# RCABench Evaluation Fairness Note

## Question

Whether the algorithms in `results.md` are evaluated under pure RCA conditions with the fault time/window provided, or whether some baselines perform or consume AD+RCA style inputs.

## Findings

- The platform `AlgorithmArgs` only exposes `dataset`, `datapack`, `input_folder`, and `output_folder`; it does not pass an explicit fault timestamp field.
- RCABench datapacks are already split into `normal_*` and `abnormal_*` parquet files. This means the benchmark is mainly RCA conditioned on a known incident window, not end-to-end anomaly detection from a long unlabeled stream.
- Several baseline adapters derive an injection/alarm time from `env.json` or platform helpers and use it to split or define normal/abnormal windows. This is equivalent to assuming the failure window is known.
- EvidenceRank uses only raw `normal_*` and `abnormal_*` frames and does not read labels, `injection.json`, historical outputs, or `conclusion.parquet`.
- Some baselines consume stronger processed hints:
  - MicroDig auto-detects `alarm_item` from `conclusion.parquet` when no alarm service is passed.
  - ShapleyIQ's MicroHECL, MicroRCA, and TON variants call `detect_anomalous_services`, which reads `conclusion.parquet`; ShapleyRCA and MicroRank disable this in their current adapters.
- `simplerca` in the current registry uses `NezhaRCA` with `NezhaDataAdapter`, which reads normal/abnormal parquet files directly. Other unused SimpleRCA adapters contain label-reading code, but they are not the path used by the current `simplerca` result in `results.md`.

## Interpretation

The fair headline protocol is: **RCA accuracy given a known incident window**. It should not be described as end-to-end AD+RCA unless the experiment is changed to hide the normal/abnormal split and require algorithms to discover the anomaly time.

EvidenceRank's high score is not explained by extra access to fault time or labels. It uses the same pre-split incident-window assumption as the main baseline group, and some lower-scoring baselines actually receive additional processed alarm-service hints from `conclusion.parquet`.

## Reporting Recommendation

When reporting results, separate baselines into:

- Raw incident-window RCA: EvidenceRank, HeroSAS, Baro, RCD, CausalRCA, RUN, Nezha, SimpleRCA/NezhaRCA, ShapleyRCA, MicroRank.
- Incident-window RCA with processed alarm-service hints: MicroDig, MicroHECL, MicroRCA, TON.

For a stricter raw-only comparison, rerun or mark the `conclusion.parquet`-dependent baselines with that hint disabled.
