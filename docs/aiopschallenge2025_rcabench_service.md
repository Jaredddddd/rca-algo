# AIOpsChallenge2025 RCABench Service Dataset

## Purpose

This document records the local conversion of
`/home/ljw/paper/aiops-challenge-data/aiopschallenge2025` into the RCABench v2 layout expected by
this repository.

Converter:

```text
scripts/build_aiopschallenge2025_rcabench.py
```

Default generated dataset:

```text
data/rcabench-platform-v2/data/aiopschallenge2025_rcabench_service
data/rcabench-platform-v2/meta/aiopschallenge2025_rcabench_service
```

## Time Zone Rule

Use UTC for `groundtruth.jsonl` and parquet row filtering. Use UTC+8 only when resolving daily
folders and hourly filenames.

Confirmed example:

```text
2025-06-06/trace-parquet/trace_jaeger-span_2025-06-06_00-00-00.parquet
  2025-06-05 16:00:00.342 UTC to 2025-06-05 16:59:59.852 UTC
```

The same pattern holds for logs and metrics. A metric file under folder `2025-06-06` spans
`2025-06-05T16:00:00Z` to `2025-06-06T15:59:00Z`.

If ground-truth dates are used directly as folder dates, the local data appears to miss
`2025-06-05`, `2025-06-16`, `2025-06-23`, and `2025-06-26`. With `utc_time + 8h`, all 400
ground-truth rows map to existing daily folders.

## Build

From the repository root:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
uv run --package evidencerank python scripts/build_aiopschallenge2025_rcabench.py --overwrite
```

Useful options:

```bash
uv run --package evidencerank python scripts/build_aiopschallenge2025_rcabench.py \
  --dataset aiopschallenge2025_rcabench_service \
  --min-window-minutes 10 \
  --overwrite

uv run --package evidencerank python scripts/build_aiopschallenge2025_rcabench.py \
  --dataset __tmp_aiopschallenge2025_rcabench_smoke \
  --limit 5 \
  --overwrite
```

By default the converter now drops service-level cases whose GT service is absent from every
converted trace/log/metric `service_name` candidate. To keep these impossible service-level cases
for diagnosis only:

```bash
uv run --package evidencerank python scripts/build_aiopschallenge2025_rcabench.py \
  --keep-unobservable-labels \
  --overwrite
```

## Generated Shape

Each datapack contains the RCABench v2 files used by the local eval pipeline:

```text
.finished
env.json
injection.json
normal_traces.parquet
abnormal_traces.parquet
normal_logs.parquet
abnormal_logs.parquet
normal_metrics.parquet
abnormal_metrics.parquet
normal_metrics_sum.parquet
abnormal_metrics_sum.parquet
normal_metrics_histogram.parquet
abnormal_metrics_histogram.parquet
conclusion.parquet
```

Metadata:

```text
meta/aiopschallenge2025_rcabench_service/index.parquet
meta/aiopschallenge2025_rcabench_service/labels.parquet
meta/aiopschallenge2025_rcabench_service/conversion_report.json
```

## Label Policy

The default dataset is service-only:

- skip `instance_type == "node"`
- write only `gt.level = service`
- service faults use `service`
- network faults label both `source` and `destination`
- pod faults map pod names to their owning service
- map raw trace service `redis` to label-compatible `redis-cart`
- skip cases whose labels are not observable in any converted trace/log/metric service candidates
  unless `--keep-unobservable-labels` is set

## Preserved Source Features

The converter intentionally keeps more source information than the first conversion did:

- trace: keeps raw `references`, `tags`, `logs`, `process`, `flags`, source start/duration fields,
  raw service name, derived `parent_span_id`, and derived `parent_service`
- trace status: derives `status_code` / `attr.status_code` from raw `error`, `status.code`,
  `otel.status_code`, `http.status_code`, and error-like `status.message`; it no longer writes every
  span as `Ok`
- trace compatibility: also writes `status.code`, `status.message`, `http.status_code`,
  `otel.status_code`, `error`, `attr.http.response.status_code`, and `attr.error`
- log: preserves raw timestamp, agent, pod, namespace, node, and infers `level` from message text
  instead of writing all logs as `INFO`
- metric: preserves source metadata under `attr.aiops.*`, including `object_id`, `object_type`,
  `instance`, `pod`, `device`, `mountpoint`, `cf`, `sql_type`, `type`, `kpi_key`, `kpi_name`,
  metric group, and metric file

This makes the RCABench-shaped parquet files larger, but keeps the raw evidence needed by algorithms
that can use status/error tags, trace topology, pod metadata, or metric provenance.

## Previous Conversion Result

The following numbers are from the earlier conversion before trace-status preservation and
unobservable-label filtering:

```text
total groundtruth rows: 400
converted datapacks:   281
skipped node cases:    82
skipped empty cases:   37
metadata labels:       349, all gt.level=service
dataset size:          1.7G
meta size:             136K
```

`skipped_empty` means at least one required normal/abnormal trace or metric window was empty. The
details are stored in `conversion_report.json`.

## Current Converter Validation

Validated on 2026-06-08:

- `py_compile` passes for `scripts/build_aiopschallenge2025_rcabench.py`
- smoke conversion with `--limit 2` writes trace/log/metric parquet with the expanded schemas
- a `network corrupt` smoke case contains both `Ok` and `Error` trace statuses after conversion
- old converted data contains 230 observable service-level cases and 51 unobservable service-level
  cases
- sampled unobservable cases such as `tidb-tikv` `io fault` and `tidb-pd` / `tidb-tidb`
  `pod failure` are now returned as `skipped_unobservable_label`

The 51 unobservable cases are not hard-coded as TiDB. They are skipped because their service-level
GT label does not appear in any converted trace/log/metric `service_name` candidate, so a service
ranking algorithm cannot hit them under the current RCABench service-level interface.

## Output / Perf Report Pitfall

`--overwrite` only replaces the generated dataset data/meta directories. It does not remove old
algorithm outputs under:

```text
output/rcabench-platform-v2/data/aiopschallenge2025_rcabench_service
```

After the observable-label filter was enabled, the current dataset has 230 datapacks, while a
workspace that evaluated the earlier 281-case conversion may still have 281 output datapack
directories. Re-run the target algorithms with `eval batch ... --clear` after rebuilding the
dataset, and use `eval perf-report ... --warn-missing` when intentionally aggregating partial
algorithm runs.

Current conversion summary:

```text
total_groundtruth=400
converted=230
skipped_node=82
skipped_empty=37
skipped_unobservable_label=51
```

## CREST Smoke Test

Commands:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -d aiopschallenge2025_rcabench_service --clear --use-cpus 16

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval perf-report aiopschallenge2025_rcabench_service
```

Observed current `perf-report` row after filtering to the 230 current datapacks:

```text
total:       230
error:       0
runtime avg: 20.902668 seconds
MRR:         0.503603
AC@1:        0.334783
AC@3:        0.600000
AC@5:        0.669565
Avg@3:       0.475362
Avg@5:       0.545217
```

## Follow-up Analysis

CREST trace degradation analysis:

```text
docs/aiopschallenge2025_crest_trace_analysis.md
docs/aiopschallenge2025_crest_after_rebuild_analysis.md
```

Key finding before the rebuild: raw aiops2025 trace tags contain non-OK status/error evidence, but
the pre-fix conversion wrote all `attr.status_code` values as `Ok`.

Key finding after the rebuild: status/error preservation and unobservable-label filtering are fixed,
but aiops2025 trace is still much less root-aligned than RCABench trace. Full CREST remains weaker
than `crest_metric_log` because trace/topology support often promotes `frontend` or other propagation
services on resource, JVM, pod, and port-misconfig cases.
