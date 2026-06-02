# 直接展示已有算法结果(除了 DiagFusion 和 RUN 外都有了)

```bash
# 默认 rcabench 数据集，按 MRR 降序
./scripts/combined_report.sh

# 指定数据集
./scripts/combined_report.sh rcabench_test

# 按 AC@1 排序
uv run --package baro python scripts/combined_report.py rcabench --sort-by AC@1

# 升序
uv run --package baro python scripts/combined_report.py rcabench --asc
```

如果是希望打印output/rcabench-platform-v2/evolve_snapshots中的数据：

```bash
OUTPUT_ROOT=output/rcabench-platform-v2/evolve_snapshots/V7 \
  uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```


# How to Run RCA Algorithms Locally

This document explains how to reproduce the algorithms in this repository on a local GPU server without building Docker images.

The commands below assume this layout:

```text
/home/ljw/paper/aegis/
├── rcabench-platform/
└── rca-algo-contrib/
```

The local RCABench dataset is assumed to be:

```text
/home/ljw/paper/DDS-DL-AIOPS/RCABench-Dataset
```

All commands are intended to run from:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
```

## Current Local State

On the current server, the base local dataset has already been prepared:

```text
data/rcabench-platform-v2/data/rcabench
  -> /home/ljw/paper/DDS-DL-AIOPS/RCABench-Dataset

data/rcabench-platform-v2/meta/rcabench/index.parquet
data/rcabench-platform-v2/meta/rcabench/labels.parquet
```

The generated metadata currently contains:

```text
rcabench index:  1422 datapacks
rcabench labels: 2475 service labels
```

The train/test split for trainable algorithms has also been generated:

```text
data/rcabench-platform-v2/data/__dev__rcabench_train_r1
data/rcabench-platform-v2/data/__dev__rcabench_test_r1

data/rcabench-platform-v2/meta/rcabench_train/index.parquet
data/rcabench-platform-v2/meta/rcabench_test/index.parquet

data/rcabench-platform-v2/splits/rcabench_train_test.json
```

Current split:

```text
train = 999 datapacks
test  = 423 datapacks
```

## Why Run from rca-algo-contrib

The eval CLI from `rcabench-platform` v2 reads from these relative paths by default:

```text
DATA_ROOT   = data/rcabench-platform-v2
OUTPUT_ROOT = output/rcabench-platform-v2
TEMP_ROOT   = temp
```

So the simplest and least surprising mode is:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
export DATA_ROOT=$PWD/data/rcabench-platform-v2
export OUTPUT_ROOT=$PWD/output/rcabench-platform-v2
export TEMP_ROOT=$PWD/temp
export LOGURU_COLORIZE=0
```

如果觉得运行是 debug 日志太多，可以:

```bash
export LOGURU_LEVEL=WARNING
```


The explicit exports are optional when running from the repository root, but they make scripts safer when launched from `tmux`, `nohup`, or another working directory.

## Fresh Clone Setup

Clone both repositories:

```bash
mkdir -p /home/ljw/paper/aegis
cd /home/ljw/paper/aegis

git clone <rcabench-platform-url> rcabench-platform
git clone <rca-algo-contrib-url> rca-algo-contrib
cd rca-algo-contrib
```

Initialize algorithm submodules:

```bash
git submodule update --init --recursive
```

Install `uv` if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

Recommended Python versions:

```bash
uv python install 3.13 3.12 3.10.16
```

The lightweight v2 eval algorithms mostly use Python 3.13. The trainable or heavier algorithms use separate environments:

```text
baro, rcd, run, causalrca, microdig, shapleyiq, simplerca, evidencerank, herosas: workspace packages
diagfusion: separate uv project, Python 3.10.16
art:        separate uv project, Python >=3.12
eadro:      separate uv project, Python >=3.12, CUDA torch/dgl configured
```

## Dataset Layout

If the dataset is already downloaded elsewhere, do not copy it. Use a symlink:

```bash
mkdir -p data/rcabench-platform-v2/data
ln -sfn /home/ljw/paper/DDS-DL-AIOPS/RCABench-Dataset \
  data/rcabench-platform-v2/data/rcabench
```

If you already have the convenience link in the parent `aegis` repository:

```text
/home/ljw/paper/aegis/data/RCABench-Dataset
```

you can use it as the source:

```bash
uv run --package baro python scripts/build_local_rcabench_meta.py \
  --src /home/ljw/paper/aegis/data/RCABench-Dataset
```

Otherwise use the original dataset path:

```bash
uv run --package baro python scripts/build_local_rcabench_meta.py \
  --src /home/ljw/paper/DDS-DL-AIOPS/RCABench-Dataset
```

This script creates:

```text
data/rcabench-platform-v2/data/rcabench
data/rcabench-platform-v2/meta/rcabench/index.parquet
data/rcabench-platform-v2/meta/rcabench/labels.parquet
```

It reuses `rcabench_platform.v2.sources.convert.convert_dataset()` for the parquet metadata generation. The raw data is not rewritten because the downloaded RCABench dataset is already converted and each datapack has `.finished`.

Verify:

```bash
uv run --package baro python - <<'PY'
from pathlib import Path
import polars as pl

root = Path("data/rcabench-platform-v2/meta/rcabench")
index = pl.read_parquet(root / "index.parquet")
labels = pl.read_parquet(root / "labels.parquet")

print("index", index.shape, index.columns)
print("labels", labels.shape, labels.columns)
PY
```

Expected:

```text
index (1422, 2) ['dataset', 'datapack']
labels (2475, 4) ['dataset', 'datapack', 'gt.level', 'gt.name']
```

## Train/Test Split

Trainable algorithms need a train/test split. The split helper is:

```text
scripts/build_rcabench_train_test_split.py
```

### V2 vs V3 Split Decision

Both platform functions were compared:

```text
rcabench_platform.v2.datasets.rcabench.rcabench_split_train_test
rcabench_platform.v3.sdk.datasets.rcabench.rcabench_split_train_test
```

Their split algorithm is the same:

1. Remove `previous_datapacks`.
2. Group datapacks by the ground-truth service set from `injection.json`.
3. Take approximately `train_ratio` from every service group.
4. Cap per-group train size with a threshold so the global ratio is close to the target.
5. Return `train_datapacks, test_datapacks`.

For this repository, the default should be v2 because all local eval commands in `rca-algo-contrib` use `rcabench-platform` v2.

Both v2 and v3 were adapted to the current dataset schema:

```text
ground_truth: dict
ground_truth.service: list[str]
```

Older code expected:

```text
ground_truth: list[dict]
```

Both versions were also made deterministic by sorting datapacks and using a stable service key instead of Python's process-randomized `hash()`.

Generate the default split:

```bash
uv run --package baro python scripts/build_rcabench_train_test_split.py \
  --splitter-version v2 \
  --train-ratio 0.7 \
  --seed 42
```

Outputs:

```text
data/rcabench-platform-v2/data/__dev__rcabench_train_r1
data/rcabench-platform-v2/data/__dev__rcabench_test_r1
data/rcabench-platform-v2/meta/rcabench_train/index.parquet
data/rcabench-platform-v2/meta/rcabench_test/index.parquet
data/rcabench-platform-v2/splits/rcabench_train_test.json
```

Verify:

```bash
uv run --package baro python - <<'PY'
from pathlib import Path
import json
import polars as pl

root = Path("data/rcabench-platform-v2")
manifest = json.loads((root / "splits/rcabench_train_test.json").read_text())
print(manifest["source"])
print(manifest["splitter_version"], manifest["train_count"], manifest["test_count"])

for dataset in ["rcabench_train", "rcabench_test"]:
    index = pl.read_parquet(root / "meta" / dataset / "index.parquet")
    labels = pl.read_parquet(root / "meta" / dataset / "labels.parquet")
    print(dataset, index.shape, labels.shape)
PY
```

Expected:

```text
rcabench_platform.v2.datasets.rcabench.rcabench_split_train_test
v2 999 423
rcabench_train (999, 2) (1724, 4)
rcabench_test (423, 2) (751, 4)
```

You can compare with v3 if needed:

```bash
uv run --package baro python scripts/build_rcabench_train_test_split.py \
  --splitter-version v3 \
  --train-ratio 0.7 \
  --seed 42 \
  --manifest data/rcabench-platform-v2/splits/rcabench_train_test_v3.json \
  --no-data-dirs \
  --no-meta
```

## Offline Operation

Offline operation is possible only if all required artifacts already exist locally:

```text
1. repository files and submodules
2. uv.lock files
3. uv cache or wheelhouse for every dependency
4. Python interpreters required by uv
5. RCABench dataset
6. generated index.parquet / labels.parquet
7. trained checkpoints for trainable algorithms
```

On an online machine, prefill the UV cache:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib

uv sync --frozen --package baro
uv sync --frozen --package shapleyiq
uv sync --frozen --package nezha
uv sync --frozen --package MicroDig
uv sync --frozen --package rcaeval-rcd
uv sync --frozen --package rcaeval_causalrca
uv sync --frozen --package rcaeval_run
uv sync --frozen --package SimpleRCA
uv sync --frozen --package evidencerank
uv sync --frozen --package herosas

uv sync --frozen --directory algorithms/art
uv sync --frozen --directory algorithms/eadro
uv sync --frozen --directory algorithms/diagfusion
```

Then copy these to the offline server:

```text
~/.cache/uv
~/.local/share/uv/python
rca-algo-contrib/
rcabench-platform/
RCABench-Dataset/
```

On the offline server, run with:

```bash
export UV_OFFLINE=1

uv sync --offline --frozen --package baro
uv run --offline --frozen --package baro python algorithms/baro/main.py eval show-datasets
```

If `uv` says a wheel or Python version is missing, the offline cache is incomplete. Run the failing `uv sync` once on an online machine, then copy the updated UV cache again.

## Local Eval Command Pattern

All local eval commands have the same shape:

```bash
uv run --package <uv-package> python algorithms/<algorithm>/main.py \
  eval batch \
  -a <algorithm-name> \
  -d rcabench \
  --clear \
  --use-cpus 32
```

Use `rcabench` to evaluate on the whole dataset.

Use `rcabench_test` to evaluate only on the held-out split:

```bash
uv run --package <uv-package> python algorithms/<algorithm>/main.py \
  eval batch \
  -a <algorithm-name> \
  -d rcabench_test \
  --clear \
  --use-cpus 32
```

`--clear` deletes and rewrites that algorithm's output folder. Omit it to resume and skip finished datapacks.

Outputs go to:

```text
output/rcabench-platform-v2/<dataset>/<datapack>/<algorithm>/
├── output.parquet
├── perf.parquet
└── .finished
```

## Full Dataset Commands

### Baro

```bash
uv run --package baro python algorithms/baro/main.py \
  eval batch -a baro -d rcabench --clear --use-cpus 32
```

Report:

```bash
uv run --package baro python algorithms/baro/main.py \
  eval perf-report rcabench
```

### Nezha

```bash
uv run --package nezha python algorithms/nezha/main.py \
  eval batch -a nezha -d rcabench --clear --use-cpus 32
```

Report:

```bash
uv run --package nezha python algorithms/nezha/main.py \
  eval perf-report rcabench
```

### MicroDig

```bash
uv run --package MicroDig python algorithms/microdig/main.py \
  eval batch -a microdig -d rcabench --clear --use-cpus 32
```

Report:

```bash
uv run --package MicroDig python algorithms/microdig/main.py \
  eval perf-report rcabench
```

### ShapleyIQ Family

The `shapleyiq` package registers five algorithms:

```text
shapleyiq
ton
microrank
microhecl
microrca
```

Run all five:

```bash
uv run --package shapleyiq python algorithms/shapleyiq/main.py \
  eval batch \
  -a shapleyiq \
  -a ton \
  -a microrank \
  -a microhecl \
  -a microrca \
  -d rcabench \
  --clear \
  --use-cpus 32
```

Report:

```bash
uv run --package shapleyiq python algorithms/shapleyiq/main.py \
  eval perf-report rcabench
```

### RCD

```bash
uv run --package rcaeval-rcd python algorithms/rcd/main.py \
  eval batch -a rcd -d rcabench --clear --use-cpus 32
```

Report:

```bash
uv run --package rcaeval-rcd python algorithms/rcd/main.py \
  eval perf-report rcabench
```

### CausalRCA

This package depends on `torch>=2.7.1`, so first install it in a controlled window:

```bash
uv sync --frozen --package rcaeval_causalrca
```

Then evaluate:

```bash
uv run --package rcaeval_causalrca python algorithms/causalrca/main.py \
  eval batch -a causalrca -d rcabench --clear --use-cpus 32
```

### RUN

This package also depends on torch:

```bash
uv sync --frozen --package rcaeval_run
```

RUN 中日志太多，运行前可以：

```bash
export LOGURU_LEVEL=WARNING
```

Run:

```bash
uv run --package rcaeval_run python algorithms/run/main.py \
  eval batch -a RUN -d rcabench --clear --use-cpus 32
```

The algorithm name is uppercase `RUN`.

### SimpleRCA

```bash
uv run --package SimpleRCA python algorithms/simplerca/main.py \
  eval batch -a simplerca -d rcabench --clear --use-cpus 32
```

```bash
uv run --package SimpleRCA python algorithms/simplerca/main.py eval perf-report rcabench
```

### EvidenceRank

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a evidencerank -d rcabench --clear --use-cpus 32
```

Report:

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

#### EvidenceRank Ablation (消融实验)

EvidenceRank 默认融合三模态（metric + trace + log）的 15 维特征。以下 6 个变体用于消融实验，覆盖所有单模态和双模态组合：

| 变体名 | 使用模态 | 特征维度 |
|--------|---------|---------|
| `evidencerank_metric` | metric only | 5 |
| `evidencerank_log` | log only | 3 |
| `evidencerank_trace` | trace + topology | 7 |
| `evidencerank_metric_log` | metric + log | 8 |
| `evidencerank_metric_trace` | metric + trace + topology | 12 |
| `evidencerank_log_trace` | log + trace + topology | 10 |

一次运行全部消融变体：

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch \
  -a evidencerank_metric \
  -a evidencerank_log \
  -a evidencerank_trace \
  -a evidencerank_metric_log \
  -a evidencerank_metric_trace \
  -a evidencerank_log_trace \
  -d rcabench --clear --use-cpus 32
```

Report：

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

也可以与完整 EvidenceRank 一起运行对比：

```bash
uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch \
  -a evidencerank \
  -a evidencerank_metric \
  -a evidencerank_log \
  -a evidencerank_trace \
  -a evidencerank_metric_log \
  -a evidencerank_metric_trace \
  -a evidencerank_log_trace \
  -d rcabench --clear --use-cpus 45
```

### HeroSAS

HeroSAS is adapted from the original Bank metric tool in `algorithms/herosas/metric_tools.py`.
The RCABench version reads `normal_metrics*.parquet` and `abnormal_metrics*.parquet`,
detects stable-to-anomalous metric shifts per service, applies the original per-metric
noise reduction and time-cluster filtering, then returns service-level rankings.

```bash
uv run --package herosas python algorithms/herosas/main.py \
  eval batch -a herosas -d rcabench --clear --use-cpus 32
```

Report:

```bash
uv run --package herosas python algorithms/herosas/main.py eval perf-report rcabench
```

## Trainable Algorithms

The trainable algorithms are not part of the root workspace sync because their environments conflict with the lightweight eval packages.

Always use the split generated above:

```text
data/rcabench-platform-v2/data/__dev__rcabench_train_r1
data/rcabench-platform-v2/data/__dev__rcabench_test_r1
```

For fair evaluation:

```text
train on __dev__rcabench_train_r1
evaluate on rcabench_test
```

### ART

Environment:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib/algorithms/art
uv sync --frozen
```

Current `algorithms/art/pyproject.toml` pins CPU torch and DGL wheels:

```text
torch = torch-2.4.0+cpu.cxx11.abi
dgl   = dgl-2.4.0 for torch 2.4
```

If GPU training is required, replace those wheel URLs with CUDA-compatible torch/DGL wheels before `uv sync`.

Preprocess the RCABench split:

```bash
uv run python client.py preprocess \
  --data-root ../../data/rcabench-platform-v2/data \
  --output-dir data/RCABENCH \
  --dataset-type RCABENCH_r1
```

Train:

```bash
uv run python client.py train \
  --dataset RCABENCH \
  --output-dir res/RCABENCH
```

Expose the trained model where `main.py` expects it:

```bash
ln -sfn res/RCABENCH/model.pkl model.pkl
```

Evaluate on held-out test split:

```bash
DATA_ROOT=../../data/rcabench-platform-v2 \
OUTPUT_ROOT=../../output/rcabench-platform-v2 \
TEMP_ROOT=../../temp \
uv run python main.py eval batch \
  -a art \
  -d rcabench_test \
  --clear \
  --use-cpus 32
```

### Eadro

Environment:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib/algorithms/eadro
uv sync --frozen
```

Current `algorithms/eadro/pyproject.toml` already points to CUDA 12.4 wheels:

```text
torch 2.4.0+cu124
dgl   2.4.0+cu124
```

Create a local settings file:

```bash
cp settings.toml settings.local.toml
```

Edit these paths in `settings.local.toml`:

```toml
[datasets.rcabench]
root_path = "../../data/rcabench-platform-v2/data"

[training]
gpu = true
device = "cuda"

[paths]
data_root = "../../data/rcabench-platform-v2/data"
metadata = "data/local/eadro/metadata"
ckpt = "data/local/eadro/checkpoints"
result_dir = "result"
```

Create train and test samples:

```bash
uv run python client.py create-dataset \
  --config settings.local.toml \
  --dataset-folder __dev__rcabench_train_r1 \
  --label train \
  --workers 16

uv run python client.py create-dataset \
  --config settings.local.toml \
  --dataset-folder __dev__rcabench_test_r1 \
  --label test \
  --workers 16
```

Train:

```bash
uv run python client.py train \
  --config settings.local.toml \
  --dataset-folder __dev__rcabench_train_r1 \
  --test-dataset-folder __dev__rcabench_test_r1 \
  --experiment-name rcabench-local
```

The expected checkpoint is:

```text
data/local/eadro/checkpoints/rcabench-local/best_model.ckpt
```

Create symlink so the eval CLI can find the test dataset:

> The `rcabench_platform` framework resolves `-d rcabench_test` to
> `DATA_ROOT/data/rcabench_test/`, but the actual directory on disk is
> `__dev__rcabench_test_r1`. A symlink bridges this gap.

```bash
ln -sfn __dev__rcabench_test_r1 ../../data/rcabench-platform-v2/data/rcabench_test
```

Evaluate:

```bash
CHECKPOINT_PATH=data/local/eadro/checkpoints/rcabench-local/best_model.ckpt \
DATA_ROOT=../../data/rcabench-platform-v2 \
OUTPUT_ROOT=../../output/rcabench-platform-v2 \
TEMP_ROOT=../../temp \
uv run python main.py eval batch \
  -a eadro \
  -d rcabench_test \
  --clear
```

Eadro's `main.py` is wired to the local v2 eval CLI, so `eval batch` is available.

### DiagFusion

Environment:

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib/algorithms/diagfusion
uv sync --frozen
```

DiagFusion requires Python 3.10.16 and has older pinned dependencies:

```text
torch==2.4.0
dgl==0.9.1
fasttext==0.9.3
py2neo==2021.2.4
```

The current training code still has several hardcoded paths under:

```text
data/rcabench/demo/demo2
data/middle/metadata
data/middle/checkpoints
```

Before training, make sure the RCABench split exists. Then run preprocessing/training from `algorithms/diagfusion` after adapting `src/config/gaia_config2.yaml` to the local split directories:

```text
../../data/rcabench-platform-v2/data/__dev__rcabench_train_r1
../../data/rcabench-platform-v2/data/__dev__rcabench_test_r1
```

The original training entry is:

```bash
uv run python client.py --config gaia_config2.yaml
```

The trained inference artifacts expected by `main.py` are:

```text
data/middle/checkpoints/service_model.pt
data/middle/metadata/topology.pkl
data/middle/metadata/service_instance_mapping.json
```

Set environment variables:

```bash
export CHECKPOINT_PATH=./data/middle/checkpoints/service_model.pt
export DYNACONF_PATHS__METADATA=./data/middle/metadata
export DYNACONF_PATHS__CKPT=./data/middle/checkpoints
```

Evaluate on held-out test split:

```bash
DATA_ROOT=../../data/rcabench-platform-v2 \
OUTPUT_ROOT=../../output/rcabench-platform-v2 \
TEMP_ROOT=../../temp \
uv run python main.py eval batch \
  -a diagfusion \
  -d rcabench_test \
  --clear
```

DiagFusion is the least plug-and-play of the three trainable algorithms. If the checkpoint or metadata files do not exist, local eval will fail before producing RCA output.

## Reporting

After a batch run, generate a report using the same algorithm entrypoint that registered the algorithm:

```bash
uv run --package baro python algorithms/baro/main.py eval perf-report rcabench
uv run --package nezha python algorithms/nezha/main.py eval perf-report rcabench
uv run --package shapleyiq python algorithms/shapleyiq/main.py eval perf-report rcabench
```

For train/test evaluation:

```bash
uv run --package baro python algorithms/baro/main.py eval perf-report rcabench_test
```

### Batch report all algorithms

To generate perf-report for every algorithm at once:

```bash
./scripts/batch_report.sh              # default dataset: rcabench
./scripts/batch_report.sh rcabench_test  # specify dataset
```

The script iterates over all workspace algorithms (baro, nezha, shapleyiq, microdig, rcd, causalrca, run, simplerca, evidencerank) and standalone algorithms (art, eadro, diagfusion) in sequence.


一起打印结果：
```bash
# 默认 rcabench 数据集，按 MRR 降序
./scripts/combined_report.sh

# 指定数据集
./scripts/combined_report.sh rcabench_test

# 按 AC@1 排序
uv run --package baro python scripts/combined_report.py rcabench --sort-by AC@1

# 升序
uv run --package baro python scripts/combined_report.py rcabench --asc
```
核心逻辑：直接扫描 output/rcabench-platform-v2/data/{dataset}/ 下所有算法的 output.parquet，合并后调用 calc_all_perf 计算统一指标，输出一张包含全部算法的汇总表。结果同时保存为 dataset.perf.combined.parquet。


Report outputs:

```text
output/rcabench-platform-v2/meta/<dataset>/output.parquet
output/rcabench-platform-v2/meta/<dataset>/datapack.perf.parquet
output/rcabench-platform-v2/meta/<dataset>/dataset.perf.parquet
```

## Smoke Tests

Dataset visibility:

```bash
uv run --package baro python algorithms/baro/main.py eval show-datasets
```

Expected datasets after setup:

```text
rcabench        1422 datapacks
rcabench_train   999 datapacks
rcabench_test    423 datapacks
```

Single datapack:

```bash
uv run --package baro python algorithms/baro/main.py \
  eval single baro rcabench ts7-mysql-partition-wk622l --clear
```

Small sampled batch:

```bash
uv run --package baro python algorithms/baro/main.py \
  eval batch -a baro -d rcabench --sample 5 --clear --use-cpus 8
```

## Common Errors

### `index.parquet` or `labels.parquet` missing

Run:

```bash
uv run --package baro python scripts/build_local_rcabench_meta.py \
  --src /home/ljw/paper/DDS-DL-AIOPS/RCABench-Dataset
```

### `No module named rcabench_platform.v3`

Use the default v2 splitter:

```bash
uv run --package baro python scripts/build_rcabench_train_test_split.py \
  --splitter-version v2
```

The v3 splitter requires local `rcabench-platform/src` because PyPI `rcabench-platform==0.4.1` does not expose the v3 SDK.

### `AttributeError: 'str' object has no attribute 'get'` in `get_service_names`

You are using an old platform implementation that assumes `ground_truth` is a list. The current dataset uses a dict.

Use the local patched `rcabench-platform` source or update `get_service_names()` in both v2 and v3 to support dict and list schemas.

### `Dataset folder not found`

Check `DATA_ROOT`:

```bash
echo "$DATA_ROOT"
ls -l data/rcabench-platform-v2/data
ls -l data/rcabench-platform-v2/meta
```

For commands launched from `algorithms/art`, `algorithms/eadro`, or `algorithms/diagfusion`, use:

```bash
DATA_ROOT=../../data/rcabench-platform-v2
OUTPUT_ROOT=../../output/rcabench-platform-v2
TEMP_ROOT=../../temp
```

### `CHECKPOINT_PATH` missing

The algorithm requires a trained model:

```text
eadro:      best_model.ckpt
diagfusion: service_model.pt plus metadata files
art:        model.pkl
```

Train first or point the env var/symlink to an existing checkpoint.

### UV starts downloading huge torch wheels

This is expected for `causalrca`, `run`, `eadro`, `art`, and `diagfusion`.

Use one algorithm environment at a time:

```bash
uv sync --frozen --package rcaeval_run
uv sync --frozen --directory algorithms/eadro
```

Avoid starting several heavy `uv sync` commands in parallel.

### `uv run --offline` fails

The UV cache is incomplete. Re-run the same `uv sync --frozen ...` command on an online machine and copy the UV cache back.

### `metrics_sli.parquet not found`

This warning can appear in Nezha. It did not block the verified single-datapack run.

### Batch run appears to do nothing

The default is `--skip-finished`. Add `--clear` to force a rerun:

```bash
uv run --package baro python algorithms/baro/main.py \
  eval batch -a baro -d rcabench --clear
```

## Recommended Long-Running Pattern

Use `tmux`:

```bash
tmux new -s rca-baro
cd /home/ljw/paper/aegis/rca-algo-contrib
export DATA_ROOT=$PWD/data/rcabench-platform-v2
export OUTPUT_ROOT=$PWD/output/rcabench-platform-v2
export TEMP_ROOT=$PWD/temp
export LOGURU_COLORIZE=0

uv run --package baro python algorithms/baro/main.py \
  eval batch -a baro -d rcabench --clear --use-cpus 32
```

Then detach with `Ctrl-b d`.
