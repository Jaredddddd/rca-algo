# rca-algo-contrib 本地复现记录

日期：2026-05-21

## 结论

`rca-algo-contrib` 更像独立仓库，而不是当前 `aegis` 仓库内的正式子目录。

证据：

- `rca-algo-contrib` 自己是 Git 仓库，远端是 `https://github.com/OperationsPAI/rca-algo-contrib.git`。
- 在主仓库 `/home/ljw/paper/aegis` 视角下，`rca-algo-contrib/` 是未跟踪目录；主仓库没有把它登记到 `workspace.yaml`，也没有主仓库级 `.gitmodules` 指向它。
- `rca-algo-contrib/.gitmodules` 管理的是 `algorithms/*` 下的算法子模块，例如 `baro`、`rcd`、`nezha`、`shapleyiq` 等。
- `rca-algo-contrib/pyproject.toml` 明确依赖 `rcabench-platform>=0.4.1`，不是通过相对路径 import 主仓库代码。
- 当前 `aegis/rcabench-platform` 是主仓库内的 Python 子树，`pyproject.toml` 名称为 `rcabench-platform`，版本为 `0.4.46`；主仓库 CI 也说明它是 `rcabench-platform` subtree。
- 本地验证 `uv run --package baro ...` 安装并使用的是 PyPI/lock 中的 `rcabench-platform==0.4.1`，路径在 `rca-algo-contrib/.venv/lib/python3.13/site-packages/rcabench_platform/`，不是 `../rcabench-platform/src`。

因此推荐保留情况 B：`rca-algo-contrib` 独立维护，通过 PyPI 包或显式 editable path 依赖 `rcabench-platform`。若要和 `aegis` 联动开发，可在本地临时使用 path source，但不建议把它直接移动进主仓库，除非组织层面决定把该仓库纳入 `workspace.yaml` 和主仓库 Git 管理。

## 结构与依赖证据

`rca-algo-contrib` 根目录：

- `pyproject.toml`: uv workspace，`members = ["algorithms/*"]`，排除了 `random`、`traceback`、`diagfusion`、`eadro`、`art`；根项目依赖 `rcabench-platform>=0.4.1`。
- `.gitmodules`: 算法目录来自 `LGU-SE-Internal/*` 私有/内部仓库；当前本地还存在用户已有改动：删除 `padirca`，`nezha` 指针变更。
- `Makefile`: `build` 目标调用 `uv run build_local.py batch`，但仓库实际只有 `build.py`，没有 `build_local.py`。
- `README.local.md`: 给出的本地入口是 `uv run --package <algo> python algorithms/<algo>/main.py eval ...`。
- `random` / `traceback`: 没有独立 pyproject，Dockerfile 依赖 `10.10.10.240/library/rcabench-platform:latest` base image。

算法 Python 版本和主要依赖：

- `baro`: Python `>=3.13`，依赖 `rcabench`, `rcabench-platform`。
- `nezha`: Python `>=3.10`，依赖 `polars`, `pyarrow`, `rcabench-platform==0.4.1`。
- `rcd`: Python `>=3.13`，依赖本地 editable `causal-learn` 和 `rcabench-platform`。
- `shapleyiq`: Python `>=3.13`，依赖 `numpy/scipy/pandas/scikit-learn/matplotlib/rcabench-platform`。
- `simplerca`: Python `>=3.13`，依赖 `polars`, `rcabench-platform`。
- `causalrca` / `run`: 依赖 `torch>=2.7.1`，会拉 CUDA 12 相关 PyTorch wheel。
- `eadro`: Python `>=3.12`，`torch==2.4.0`，显式使用 CUDA 12.4 的 `torch` / `dgl` wheel；需要 `CHECKPOINT_PATH`。
- `diagfusion`: Python `==3.10.16`，依赖 `torch==2.4.0`, `dgl==0.9.1`, `fasttext`, `py2neo` 等；需要 checkpoint / metadata 环境变量。
- `art`: Python `>=3.12`，声明 `dgl` 和 `torch`，但当前 `tool.uv.sources.torch` 指向 CPU wheel，不是 GPU wheel。

## 本地数据准备

平台 v2 eval CLI 默认读取：

- `DATA_ROOT` 默认 `data/rcabench-platform-v2`
- 输入数据：`data/rcabench-platform-v2/data/<dataset>/<datapack>`
- 元数据：`data/rcabench-platform-v2/meta/<dataset>/index.parquet`
- 标签：`data/rcabench-platform-v2/meta/<dataset>/labels.parquet`
- 输出：`output/rcabench-platform-v2/...`

用户已下载数据在：

`/home/ljw/paper/DDS-DL-AIOPS/RCABench-Dataset`

该目录已经是转换后的 datapack 集合，包含 `normal_metrics.parquet`、`abnormal_metrics.parquet`、`normal_traces.parquet`、`abnormal_traces.parquet`、`env.json`、`injection.json`、`.finished` 等。它缺少 eval CLI 必需的 `meta/index.parquet` 和 `meta/labels.parquet`。我新增了：

`rca-algo-contrib/scripts/build_local_rcabench_meta.py`

它会创建 `data/rcabench-platform-v2/data/rcabench` symlink，然后用一个 preconverted dataset loader 调用 `rcabench_platform.v2.sources.convert.convert_dataset()` 生成 `index.parquet` 和 `labels.parquet`。这样 parquet 的列名、排序和写入方式复用平台转换阶段的同一条路径。没有直接使用平台原始 `RCABenchDatapackLoader`，因为该 loader 面向未转换原始数据，要求每个 datapack 中存在 `conclusion.csv` 并会重新转换数据文件；当前下载目录只有转换后的 `conclusion.parquet`。

服务标签仍从 `injection.json` 的 `ground_truth.service` 读取。当前数据里的 `ground_truth` 是 dict；`rcabench_platform.v2.datasets.rcabench.get_service_names()` 在 0.4.1 版里按旧的 list-of-dicts schema 实现，不能直接复用到这份数据。

已执行：

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
uv run --package baro python scripts/build_local_rcabench_meta.py \
  --src /home/ljw/paper/DDS-DL-AIOPS/RCABench-Dataset
```

结果：

- `datapacks=1422`
- `labels=2475`

## 已验证命令

环境：

- `uv 0.11.13`
- 系统 Python `3.12.3`
- UV 为 `baro` 创建了 CPython `3.13.13`
- GPU: NVIDIA A100-SXM4-40GB，Driver `550.163.01`，CUDA `12.4`

可识别数据集：

```bash
uv run --package baro python algorithms/baro/main.py eval show-datasets
```

输出确认 `rcabench (1422 datapacks)`。

已跑通 `baro`：

```bash
uv run --package baro python algorithms/baro/main.py \
  eval single baro rcabench ts7-mysql-partition-wk622l --clear
```

输出：

- `output/rcabench-platform-v2/data/rcabench/ts7-mysql-partition-wk622l/baro/output.parquet`
- `output/rcabench-platform-v2/data/rcabench/ts7-mysql-partition-wk622l/baro/perf.parquet`
- 该 datapack 上 Baro 命中 `ts-route-service`，单样本 perf `MRR=1.0`。

已跑通 `nezha`：

```bash
uv run --package nezha python algorithms/nezha/main.py \
  eval single nezha rcabench ts7-mysql-partition-wk622l --clear
```

输出：

- 读取 78743 条 trace、42184 条 log。
- 输出 3 条 service ranking 到 `output/.../nezha/output.parquet`。
- 该样本未命中 ground truth。
- `metrics_sli.parquet not found` 是 warning，不阻断运行。

已跑通 `rcd`：

```bash
uv run --package rcaeval-rcd python algorithms/rcd/main.py \
  eval single rcd rcabench ts7-mysql-partition-wk622l --clear
```

输出：

- 读入 simple metrics 后剩余 584 列。
- 输出 3 条 service ranking 到 `output/.../rcd/output.parquet`。
- 该样本未命中 ground truth。

可生成 `baro` 最小报告：

```bash
uv run --package baro python algorithms/baro/main.py eval perf-report rcabench
```

该命令只按当前入口注册的算法聚合。若要跨算法合并，需要一个统一注册 `baro/nezha/rcd/...` 的 runner，或分别读取各自 `output.parquet` 汇总。

## 入口 import 验证

已验证可启动：

- `baro`: `uv run --package baro python algorithms/baro/main.py eval show-algorithms`
- `nezha`: `uv run --package nezha python algorithms/nezha/main.py eval show-algorithms`
- `microdig`: `uv run --package microdig python algorithms/microdig/main.py eval show-algorithms`
- `rcd`: `uv run --package rcaeval-rcd python algorithms/rcd/main.py eval show-algorithms`
- `shapleyiq`: `uv run --package shapleyiq python algorithms/shapleyiq/main.py eval show-algorithms`
- `simplerca`: `uv run --package SimpleRCA python algorithms/simplerca/main.py eval show-algorithms`

未完成：

- `causalrca` 和 `run` 入口验证触发 `torch>=2.7.1` 的 CUDA 12 依赖下载，包含 `torch`、`nvidia-cudnn-cu12`、`nvidia-cublas-cu12`、`nvidia-nccl-cu12` 等多个大包；为避免长时间占用，本轮已停止。正式跑它们应串行执行，并设置更长 UV lock timeout。
- `eadro` / `diagfusion` / `art` 属于独立或排除 workspace 的重型环境，且 `eadro`、`diagfusion` 需要 checkpoint/metadata。本轮没有完成这些模型的可复现训练或推理。

## 推荐复现步骤

轻量算法：

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
git submodule update --init --recursive

uv run --package baro python scripts/build_local_rcabench_meta.py \
  --src /home/ljw/paper/DDS-DL-AIOPS/RCABench-Dataset

uv run --package baro python algorithms/baro/main.py eval show-datasets
uv run --package baro python algorithms/baro/main.py eval single baro rcabench ts7-mysql-partition-wk622l --clear
uv run --package nezha python algorithms/nezha/main.py eval single nezha rcabench ts7-mysql-partition-wk622l --clear
uv run --package rcaeval-rcd python algorithms/rcd/main.py eval single rcd rcabench ts7-mysql-partition-wk622l --clear
```

批量示例：

```bash
uv run --package baro python algorithms/baro/main.py \
  eval batch -a baro -d rcabench --sample 5 --clear
```

PyTorch/CUDA 类算法应串行创建或补全环境：

```bash
UV_LOCK_TIMEOUT=1800 uv run --package rcaeval_causalrca \
  python algorithms/causalrca/main.py eval show-algorithms

UV_LOCK_TIMEOUT=1800 uv run --package rcaeval_run \
  python algorithms/run/main.py eval show-algorithms
```

`eadro` 需要额外提供：

```bash
export CHECKPOINT_PATH=/path/to/best_model.ckpt
uv run --directory algorithms/eadro python main.py ...
```

`diagfusion` 需要额外提供：

```bash
export CHECKPOINT_PATH=./data/middle/checkpoints/service_model.pt
export DYNACONF_PATHS__METADATA=./data/middle/metadata
export DYNACONF_PATHS__CKPT=./data/middle/checkpoints
uv run --directory algorithms/diagfusion python main.py ...
```

## 常见问题

- `index.parquet` / `labels.parquet` 不存在：运行 `scripts/build_local_rcabench_meta.py`。
- `No package metadata was found for rcabench-platform`：没有在 UV 环境内运行；用 `uv run --package <package> ...`。
- `.venv/.lock Timeout`：不要并行启动多个 `uv run` 安装；串行执行，或设置 `UV_LOCK_TIMEOUT=1800`。
- `CHECKPOINT_PATH` 缺失：`eadro`、`diagfusion` 需要训练好的模型或官方 checkpoint。
- `metrics_sli.parquet not found`：Nezha warning，当前单样本不阻断。
- `Makefile build` 失败：`Makefile` 引用不存在的 `build_local.py`，当前实际文件是 `build.py`。
- 平台原始 `RCABenchDatapackLoader` 不适配当前下载目录：下载数据已有 `conclusion.parquet`，且 `ground_truth` 是 dict；该 loader 假定 `conclusion.csv` 和旧版 list 形态 ground truth。当前 helper 只跳过原始数据重转换，仍复用 `convert_dataset()` 生成 meta parquet。

