# Eval Pipeline 详解

本文档介绍 `rcabench_platform` 提供的本地评估流水线，涵盖 CLI 命令、执行逻辑和评估指标。

> 源码位置：`.venv/lib/python3.13/site-packages/rcabench_platform/v2/`

---

## 整体架构

```
CLI 入口 (Typer)
├── eval single       → 单次执行：一个算法 × 一个 datapack
├── eval batch        → 批量执行：多算法 × 多数据集 × 多 datapack，并行
├── eval perf-report  → 性能报告：汇总所有 output.parquet，计算指标
├── eval show-algorithms  → 列出已注册算法
└── eval show-datasets    → 列出可用数据集
```

核心数据流：

```
算法执行 → output.parquet (原始结果 + hit/rank/runtime/error)
                ↓
        perf-report 汇总所有 output.parquet
                ↓
        calc_all_perf() 计算评估指标
                ↓
        *.perf.parquet + 终端摘要表
```

---

## 目录约定

路径由 `config.py` 控制，默认值：

| 变量 | 默认路径 | 说明 |
|------|----------|------|
| `DATA_ROOT` | `data/rcabench-platform-v2` | 数据集根目录 |
| `OUTPUT_ROOT` | `output/rcabench-platform-v2` | 输出根目录 |

关键路径模式：

```
{DATA_ROOT}/
├── meta/{dataset}/
│   ├── index.parquet          # datapack 列表
│   ├── labels.parquet         # 根因标签 (gt.level, gt.name)
│   └── attributes.parquet     # 故障属性 (fault_type 等)
└── data/{dataset}/{datapack}/ # 原始 datapack 数据

{OUTPUT_ROOT}/
├── data/{dataset}/{datapack}/{algorithm}/
│   ├── .finished              # 完成标记（用于 skip_finished）
│   ├── output.parquet         # 单次执行结果
│   └── perf.parquet           # 单次执行指标
└── meta/{dataset}/
    ├── output.parquet          # 全量输出汇总
    ├── datapack.perf.parquet   # 按 datapack 聚合指标
    ├── dataset.perf.parquet    # 按 dataset 聚合指标
    └── fault_types.perf.parquet # 按故障类型聚合指标
```

---

## 算法注册

入口文件（如 `algorithms/evidencerank/main.py`）负责将算法类注册到全局 registry：

```python
from rcabench_platform.v2.cli.main import main
from rcabench_platform.v2.algorithms.spec import global_algorithm_registry

registry = global_algorithm_registry()
registry["evidencerank"] = EvidenceRank
# ...

main(enable_builtin_algorithms=False)
```

算法类需实现 `Algorithm` 抽象基类：

```python
class Algorithm(ABC):
    def needs_cpu_count(self) -> int | None:
        """返回算法所需 CPU 核心数，用于并行调度。None 表示独占全部核心。"""

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        """执行算法，返回排序后的根因候选列表。"""
```

`AlgorithmArgs` 提供 `dataset`、`datapack`、`input_folder`、`output_folder`。
`AlgorithmAnswer` 包含 `level`（如 "service"）、`name`（服务名）、`rank`（排名）。

---

## eval single

**命令**：
```bash
uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval single -a evidencerank -d rcabench -p <datapack>
```

**执行流程**：

1. 从 registry 实例化算法
2. 确定输入路径（普通数据或采样数据）
3. `running_mark()` 做并发控制；若 `.finished` 存在且 `skip_finished=True` 则跳过
4. 调用 `alg(AlgorithmArgs(...))` 执行算法，计时
5. 异常处理：捕获异常但不终止，记录 `exception.type` 和 `exception.message`
6. 将算法答案排序，与 ground truth labels 比对，生成 `hit` 列
7. 保存 `output.parquet`（含 algorithm/dataset/datapack/hit/rank/runtime/exception 信息）
8. 调用 `calc_all_perf()` 生成 `perf.parquet`
9. 创建 `.finished` 标记

**output.parquet schema**：

| 列 | 类型 | 说明 |
|----|------|------|
| `level` | String | 根因层级 |
| `name` | String | 根因名称 |
| `rank` | UInt32 | 排名 |
| `algorithm` | String | 算法名 |
| `dataset` | String | 数据集名 |
| `datapack` | String | 数据包名 |
| `hit` | Boolean | 是否命中真实根因 |
| `runtime.seconds` | Float64 | 执行耗时（秒） |
| `exception.type` | String | 异常类型（无异常为 null） |
| `exception.message` | String | 异常堆栈（无异常为 null） |
| `sampler.name` | String | 采样器名（仅采样模式） |
| `sampler.rate` | Float64 | 采样率（仅采样模式） |
| `sampler.mode` | String | 采样模式（仅采样模式） |

---

## eval batch

**命令**：
```bash
uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a evidencerank -d rcabench --clear --use-cpus 32
```

**参数**：

| 参数 | 说明 |
|------|------|
| `-a / --algorithms` | 算法名列表（可多个） |
| `-d / --datasets` | 数据集名列表（可多个） |
| `--sample N` | 随机抽取 N 个 datapack |
| `--clear` | 清除已有结果重新执行 |
| `--skip-finished` | 跳过已完成（默认 true） |
| `--use-cpus N` | 限制使用的 CPU 核心数 |
| `--include-sampled` | 同时运行采样版本 |
| `-s / --sampler` | 指定采样器 |
| `-r / --sampling-rate` | 指定采样率 |
| `-m / --sampling-mode` | 指定采样模式 |

**执行流程**：

1. 校验所有算法名是否在 registry 中
2. 若 `include_sampled=True`，自动扫描可用的采样器配置
3. 对每个数据集获取 datapack 列表，如指定 `--sample` 则随机抽样
4. 对每个算法，根据 `needs_cpu_count()` 和可用 CPU 计算并行度
5. 为每个 (algorithm, dataset, datapack) 组合构造 `run_single` 的 partial 任务
6. 通过 `fmap_processpool` 并行执行所有任务
7. 打印总耗时和平均耗时

**并行度计算**：

```python
usable_cpu_count = use_cpus or max(cpu_count - 4, 0)
parallel = usable_cpu_count // alg.needs_cpu_count()
```

---

## eval perf-report

**命令**：
```bash
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

**参数**：

| 参数 | 说明 |
|------|------|
| `dataset` | 数据集名（位置参数） |
| `--warn-missing` | 缺失文件时打印警告 |
| `--include-sampled` | 包含采样数据 |

**执行流程**：

1. 扫描所有 `(datapack, algorithm)` 组合对应的 `output.parquet`
2. 若 `include_sampled=True`，额外扫描含 `_sampled_` 的输出目录
3. 合并所有 output DataFrame，保存到 `{meta}/{dataset}/output.parquet`
4. 对 `rcabench`/`rcaeval`/`aiops21` 数据集，按故障类型（fault_type）生成 `fault_types.perf.parquet`
5. 生成 `datapack.perf.parquet`（按 datapack 聚合）和 `dataset.perf.parquet`（按 dataset 聚合）
6. 若有采样数据，额外生成 `sampler.detailed.perf.parquet`、`sampler.aggregated.perf.parquet`、`sampler.grouped.perf.parquet`
7. 打印摘要表到终端

**终端输出示例**：

```
dataset    algorithm      total  error  runtime.seconds:avg  MRR     AC@1  AC@3  AC@5  Avg@3  Avg@5
rcabench   evidencerank   100    0      1.234                0.850   0.80  0.90  0.95  0.850  0.883
```

---

## 评估指标详解

所有指标在 `evaluation/ranking.py` 中实现，入口函数为 `calc_all_perf()`。

### 聚合层级

| agg_level | 分组键 | 说明 |
|-----------|--------|------|
| `datapack` | algorithm + dataset + datapack | 最细粒度，保留每个 datapack 的独立指标 |
| `dataset` | algorithm + dataset | 按数据集聚合 |
| `algorithm` | algorithm | 按算法聚合 |
| `sampler` | algorithm + dataset + datapack + sampler 列 | 按采样配置聚合 |
| `sampler_dataset` | algorithm + dataset + sampler 列 | 按 dataset + 采样配置聚合 |

### 指标计算函数

`calc_all_perf()` 依次调用以下函数并 join 结果：

#### 1. calc_index — 基础统计

- **total**：去重后的总 datapack 数
- **error**：出现异常的 datapack 数（`exception.type IS NOT NULL`）

#### 2. calc_avg_runtime — 平均运行时间

- 先按 (algorithm, dataset, datapack) 取 max runtime（去重），再按聚合层级取 mean
- 结果列：`runtime.seconds:avg`

#### 3. calc_mrr — 平均倒数排名

**MRR (Mean Reciprocal Rank)**：https://en.wikipedia.org/wiki/Mean_reciprocal_rank

- 仅统计命中的结果（`hit=True`）
- 对每个 datapack，取最小 rank（最优排名）
- 计算 `1/rank` 作为 reciprocal rank
- 按聚合层级取均值

```
MRR = mean(1 / rank_best)  over all datapacks
```

#### 4. calc_accuracy — 准确率

**AC@k (Accuracy at k)**：Top-k 结果中至少包含一个真实根因的概率。

```
AC@k = count(datapacks where hit in top-k) / total_datapacks
```

- 对每个 datapack，检查是否存在 `hit=True AND rank ≤ k`
- 按聚合层级汇总：`AC@k.count`（命中数）和 `AC@k`（命中率）

**Avg@k**：AC@1 到 AC@k 的均值。

```
Avg@k = (AC@1 + AC@2 + ... + AC@k) / k
```

默认计算 k = 1, 2, 3, 4, 5。

#### 5. calc_precision — 精确率

**P@k (Precision at k)**：Top-k 中命中结果的比例。

```
P@k = count(hits in top-k) / k
```

**AP@k (Average Precision at k)**：对 P@i 按相关性加权求和后归一化。

```
AP@k = sum(P@i * rel@i for i=1..k) / count(hits in top-k)
```

其中 `rel@i = 1` 当 rank == i 且 hit 为真。

**MAP@k (Mean Average Precision at k)**：AP@k 在聚合层级上的均值（仅非 datapack 层级计算）。

### calc_all_perf_by_datapack_attr

按 datapack 属性（如故障类型）分组计算指标。将属性列重命名为 `dataset`，复用 `calc_all_perf(dataset)` 的逻辑，再还原列名。

---

## 典型使用流程

```bash
# 1. 查看可用算法和数据集
uv run --package evidencerank python algorithms/evidencerank/main.py eval show-algorithms
uv run --package evidencerank python algorithms/evidencerank/main.py eval show-datasets

# 2. 批量执行（可多次运行，已完成的会自动跳过）
uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch -a evidencerank -d rcabench --use-cpus 32

# 3. 生成性能报告
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench

# 4. 查看结果
#    output/rcabench-platform-v2/meta/rcabench/dataset.perf.parquet
```

若需重新执行所有 datapack，加 `--clear` 参数。
