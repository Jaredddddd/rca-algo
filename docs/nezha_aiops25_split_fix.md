# Nezha AIOps25 Split Fix

## Symptoms

- `eval batch -a nezha -d aiopschallenge2025_rcabench_service` could run, but some datapacks returned `No results from Nezha analysis`.
- The same datapack could produce output when processed with the dataset's real `normal_traces.parquet` / `abnormal_traces.parquet` split.

## Root Cause

- Nezha ignored the datapack-provided split and re-split traces by sorting `trace_id` and cutting the list in half.
- On AIOpsChallenge2025 RCABench datapacks, that collapses the normal/abnormal boundary and can erase suspiciousness signals.
- The adapter also did not return the real service mapping, so successful cases could fall back to TrainTicket service names.

## Fix

- Keep and reuse the explicit `normal_traces.parquet` / `abnormal_traces.parquet` split.
- Keep the shared event ID space, but build trace features separately for normal and abnormal sets.
- Return `service_mapping` and `service_id_to_name` from the analysis result.
- Make root-span handling generic instead of assuming `loadgenerator`.

## Verification

```bash
uv run --package nezha python -m pytest algorithms/nezha/tests/test_dataset_split.py -q
LOGURU_LEVEL=WARNING uv run --package nezha python algorithms/nezha/main.py eval single nezha aiopschallenge2025_rcabench_service aiops2025-009be6db-313-code-error --clear --no-skip-finished
```

The `aiops2025-009be6db-313-code-error` datapack now writes a non-empty Nezha `output.parquet` with the real service name `frontend`.
