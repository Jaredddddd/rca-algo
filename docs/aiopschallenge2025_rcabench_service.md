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

## Current Conversion Result

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

## CREST Smoke Test

Commands:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a crest -d aiopschallenge2025_rcabench_service --clear --use-cpus 16

LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval perf-report aiopschallenge2025_rcabench_service
```

Observed result:

```text
crest/.finished:      281
crest/output.parquet: 281
crest/perf.parquet:   281
error:                0
runtime avg:          7.11812 seconds
MRR:                  0.445155
AC@1:                 0.323843
AC@3:                 0.501779
AC@5:                 0.555160
Avg@3:                0.418742
Avg@5:                0.469751
```
