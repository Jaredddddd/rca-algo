# labels.parquet 构建方法分析

本文档详细分析 `rca-algo-contrib/scripts/build_local_rcabench_meta.py` 构建 `labels.parquet` 的完整流程，与 `rcabench-platform` 原始逻辑的一致性对比，以及多 service ground truth 的处理机制。

## 1. 背景与问题

### 1.1 为什么需要单独构建 labels.parquet

`rcabench-platform` v2 的 eval CLI 需要以下元数据文件才能运行：

```
data/rcabench-platform-v2/
├── data/<dataset>/<datapack>/     # 转换后的 datapack 数据
│   ├── normal_traces.parquet
│   ├── abnormal_traces.parquet
│   ├── injection.json
│   ├── .finished
│   └── ...
└── meta/<dataset>/
    ├── index.parquet              # datapack 索引
    └── labels.parquet             # ground truth 标签
```

用户下载的 RCABench-Dataset 已包含转换后的 datapack 数据（traces、metrics、logs 等），但缺少 `index.parquet` 和 `labels.parquet`。`build_local_rcabench_meta.py` 的职责是为已转换的数据集补齐这两个文件。

### 1.2 为什么不能直接使用平台原始 Loader

`rcabench-platform` 原始的 `RCABenchDatapackLoader` 面向**未转换**的原始数据：

- 假设每个 datapack 中存在 `conclusion.csv`（原始结论文件）
- 会重新转换数据文件（traces → parquet 等）
- 0.4.1 版的 `get_service_names()` 按旧的 list-of-dicts schema 实现

当前下载目录的特点：

- 数据已经过转换，存在 `conclusion.parquet` 而非 `conclusion.csv`
- `ground_truth` 字段是新版 dict schema（见下文分析）
- 已有 `.finished` 标记，不应重新转换

因此脚本提供了 `PreconvertedRCABenchDatapackLoader`，复用 `convert_dataset()` 的元数据写入逻辑（`index.parquet` / `labels.parquet` 的列名、排序和格式），跳过数据重转换步骤。

## 2. 数据流全链路

### 2.1 从 injection.json 到 labels.parquet

完整的数据流如下：

```
injection.json
    │
    │  _service_names()  ← 提取 ground_truth.service
    ▼
list[str]  (去重排序后的 service name 列表)
    │
    │  labels()  ← 每个 service 生成一个 Label
    ▼
list[Label]  (Label(level="service", name=<svc>))
    │
    │  convert_dataset()  ← 展开为 parquet 行
    ▼
labels.parquet
    列: dataset | datapack | gt.level | gt.name
```

### 2.2 从 labels.parquet 到评估命中

```
labels.parquet
    │
    │  get_datapack_labels()  ← 按 dataset+datapack 过滤
    ▼
list[Label]  (该 datapack 的所有 ground truth 标签)
    │
    │  构建 labels_set = {(level, name), ...}
    ▼
labels_set: set[tuple[str, str]]
    │
    │  对比 (ans.level, ans.name) in labels_set
    ▼
hits: list[bool]  (每个算法预测是否命中任一 ground truth)
    │
    │  下游计算 MRR、AC@k、MAP@k 等指标
    ▼
性能报告
```

关键点：命中判定使用 **集合 membership** (`in`)，即算法预测的 `(level, name)` 只要出现在 `labels_set` 中的**任意一个**，就算命中。

## 3. injection.json 中 ground_truth 的 Schema 分析

### 3.1 当前数据集的实际分布

对 1422 个 datapack 的 `injection.json` 进行全量统计：

| Schema 类型 | 数量 | 占比 |
|-------------|------|------|
| `ground_truth` 为 dict，`service` 为 list | 1422 | 100% |

**所有 datapack 的 `ground_truth` 均为 dict 类型**，`service` 字段均为 list。

### 3.2 Service 数量分布

| Service 数量 | Datapack 数量 | 占比 |
|-------------|---------------|------|
| 1 | 369 | 26.0% |
| 2 | 1053 | 74.0% |

**74% 的 datapack 包含 2 个 ground truth service**。

### 3.3 多 Service 的成因

多 service 出现的典型场景：

**场景 A：网络类故障（corrupt、delay、loss 等）**

故障同时影响 source_service 和 target_service 两个端点。例如 `ts0-mysql-corrupt-jkgn5j`：

```json
{
  "fault_type": 20,
  "display_config": "{
    \"injection_point\": {
      \"source_service\": \"mysql\",
      \"target_service\": \"ts-order-service\"
    },
    \"corrupt\": 85,
    \"direction\": \"both\"
  }",
  "ground_truth": {
    "service": ["mysql", "ts-order-service"],
    "container": ["mysql", "ts-order-service"],
    "pod": ["mysql-0", "ts-order-service-56b9db98d8-2c52p"],
    "span": ["mysql", "ts-order-service"]
  }
}
```

此处 `mysql` 是故障注入的 source，`ts-order-service` 是 target。网络故障对双向（`direction: "both"`）都有影响，因此两端都被标记为 root cause。

**场景 B：HTTP 请求级故障（abort、delay 等）**

故障影响请求的发起方和接收方。例如 `ts0-ts-basic-service-request-abort-5dlq8r`：

```json
{
  "fault_type": 5,
  "display_config": "{
    \"injection_point\": {
      \"app_name\": \"ts-basic-service\",
      \"server_address\": \"ts-station-service\",
      \"method\": \"POST\",
      \"route\": \"/api/v1/stationservice/stations/idlist\"
    }
  }",
  "ground_truth": {
    "service": ["ts-basic-service", "ts-station-service"],
    "container": ["ts-basic-service", "ts-station-service"],
    "pod": ["ts-basic-service-59885fb497-sdvtt", "ts-station-service-6d584c8ff5-z9zjh"],
    "span": ["ts-basic-service", "ts-station-service"]
  }
}
```

### 3.4 最常见的 Service 对

| Service 对 | 频次 |
|------------|------|
| ts-basic-service, ts-price-service | 79 |
| ts-route-plan-service, ts-travel2-service | 50 |
| ts-route-plan-service, ts-travel-service | 43 |
| ts-basic-service, ts-station-service | 40 |
| ts-basic-service, ts-route-service | 38 |

这些 service 对反映了 TrainTicket 系统中高频的调用关系。

### 3.5 单 Service 场景

单 service 出现在容器级故障（ContainerKill、PodKill 等），故障仅影响一个容器/pod：

```json
{
  "fault_type": 2,
  "ground_truth": {
    "service": ["mysql"],
    "container": ["mysql"],
    "pod": ["mysql-0"]
  }
}
```

## 4. 代码逐行对比：脚本 vs 平台原始实现

### 4.1 平台原始实现

位于 `rcabench-platform/src/rcabench_platform/v2/datasets/rcabench.py`，`get_service_names()` 函数：

```python
def get_service_names(injection: dict[str, Any]) -> list[str]:
    """Extract service names from injection.json for batch fault injections"""
    ground_truth = injection.get("ground_truth", [])      # [1] 默认值为空列表
    assert ground_truth, "No groundtruths found in injection.json"  # [2] 硬断言

    if isinstance(ground_truth, dict):                     # [3] dict → 包裹为单元素列表
        groundtruths = [ground_truth]
    elif isinstance(ground_truth, list):                   # [4] list → 直接使用
        groundtruths = ground_truth
    else:
        raise TypeError(f"Unsupported ground_truth type: {type(ground_truth)}")  # [5] 类型异常

    svc_names: list[str] = []
    for gt in groundtruths:
        assert isinstance(gt, dict), f"Invalid groundtruth entry: {gt}"  # [6] 断言每项为 dict
        services = gt.get("service", [])
        if isinstance(services, str):                      # [7] str → 包裹为列表
            services = [services]
        assert len(services) > 0, "No services found in groundtruth"  # [8] 断言非空
        svc_names.extend(str(service) for service in services if service)  # [9] 提取并过滤

    return sorted(set(svc_names))                          # [10] 去重排序
```

### 4.2 脚本实现

位于 `rca-algo-contrib/scripts/build_local_rcabench_meta.py`，`_service_names()` 函数：

```python
def _service_names(injection: dict[str, Any]) -> list[str]:
    ground_truth = injection.get("ground_truth)             # [1] 默认值为 None
    names: list[str] = []

    if isinstance(ground_truth, dict):                      # [2] dict → 直接处理
        services = ground_truth.get("service", [])
        if isinstance(services, str):                       # [3] str → 单个 append
            names.append(services)
        elif isinstance(services, list):                    # [4] list → extend
            names.extend(str(item) for item in services if item)

    elif isinstance(ground_truth, list):                    # [5] list → 遍历每项
        for item in ground_truth:
            if not isinstance(item, dict):                  # [6] 跳过非 dict
                continue
            services = item.get("service", [])
            if isinstance(services, str):
                names.append(services)
            elif isinstance(services, list):
                names.extend(str(service) for service in services if service)

    return sorted(set(names))                               # [7] 去重排序
```

### 4.3 逐项差异分析

| 编号 | 维度 | 平台原始 `get_service_names` | 脚本 `_service_names` | 影响评估 |
|------|------|------------------------------|----------------------|---------|
| 1 | 默认值 | `injection.get("ground_truth", [])` → 默认 `[]` | `injection.get("ground_truth")` → 默认 `None` | **无影响**。`None` 不匹配 `dict` 或 `list`，最终返回空列表 |
| 2 | 空值检查 | `assert ground_truth` 硬报错 | 无断言，静默返回空列表 | **容错差异**。脚本在上游 `_scan_preconverted_datapacks` 中用 `if not _service_names(injection): skip` 处理 |
| 3 | dict 处理 | 统一包裹为 `[ground_truth]` 后进入循环 | 直接取 `ground_truth.service` | **逻辑等效**。两种写法最终都读取 `ground_truth["service"]` |
| 4 | list 处理 | 遍历 `groundtruths` 列表 | 遍历 `ground_truth` 列表 | **逻辑等效** |
| 5 | 类型异常 | `raise TypeError` | 不处理，`None`/`str` 等类型自然不进入分支 | **容错差异**。异常类型被静默忽略而非报错 |
| 6 | 非断言每项 | `assert isinstance(gt, dict)` | `if not isinstance(item, dict): continue` | **容错差异**。脚本跳过非 dict 项而非报错 |
| 7 | service 字段 | `str` → 包裹为列表后统一处理 | `str` → 直接 append | **逻辑等效** |
| 8 | 空断言 | `assert len(services) > 0` | 无断言 | **容错差异**。无 service 的项静默跳过 |
| 9 | 提取逻辑 | `svc_names.extend(str(service) for service in services if service)` | `names.extend(str(item) for item in services if item)` | **完全一致** |
| 10 | 返回值 | `sorted(set(svc_names))` | `sorted(set(names))` | **完全一致** |

### 4.4 结论

**核心提取逻辑完全一致**：两种实现都能正确处理当前数据集中所有 1422 个 datapack 的 `injection.json`。

差异仅在于**错误处理策略**：

- 平台原始版本使用 `assert` / `raise`，遇到异常数据时硬报错（适合 pipeline 环境，确保数据质量）
- 脚本版本使用静默跳过（适合本地已转换数据集，避免少量异常数据阻断整个构建流程）

脚本的静默容错是合理的，因为：

1. 异常数据在 `_scan_preconverted_datapacks` 阶段会被跳过并打印 warning
2. 已转换数据集是静态的，不会因运行时异常导致下游数据不一致
3. 构建结果是幂等的，重新运行可修复之前跳过的问题

## 5. 多 Service 的处理机制详解

### 5.1 labels.parquet 中的多行展开

以 `ts0-mysql-corrupt-jkgn5j` 为例（`ground_truth.service = ["mysql", "ts-order-service"]`）：

**Step 1**: `_service_names()` 提取并返回 `["mysql", "ts-order-service"]`

**Step 2**: `labels()` 为每个 service 生成一个 `Label`：

```python
def labels(self) -> list[Label]:
    injection = json.loads((self._src_folder / "injection.json").read_text())
    return [Label(level="service", name=service) for service in _service_names(injection)]
```

结果：`[Label(level="service", name="mysql"), Label(level="service", name="ts-order-service")]`

**Step 3**: `convert_dataset()` 将每个 label 展开为 `labels.parquet` 中的独立行：

```python
# convert_dataset() 中的核心逻辑（convert.py:82-88）
index_rows = []
labels_rows = []
for datapack, labels in results:
    index = {"dataset": dataset, "datapack": datapack}
    index_rows.append(index)
    for label in labels:                                          # 遍历每个 label
        labels_rows.append({
            **index,                                              # dataset + datapack
            "gt.level": label.level,                              # "service"
            "gt.name": label.name,                                # "mysql" 或 "ts-order-service"
        })
```

最终 `labels.parquet` 中的行：

| dataset | datapack | gt.level | gt.name |
|---------|----------|----------|---------|
| rcabench | ts0-mysql-corrupt-jkgn5j | service | mysql |
| rcabench | ts0-mysql-corrupt-jkgn5j | service | ts-order-service |

### 5.2 评估时的命中判定

`experiments/single.py` 中的命中逻辑：

```python
# 构建 ground truth 集合
labels_set = {(label.level, label.name) for label in get_datapack_labels(dataset, datapack)}
# 例如: {("service", "mysql"), ("service", "ts-order-service")}

# 对算法的每个预测检查是否命中
hits = [(ans["level"], ans["name"]) in labels_set for ans in answers]
```

假设算法输出排序为 `[("service", "ts-route-service"), ("service", "mysql"), ("service", "ts-order-service")]`：

| rank | 预测 service | 命中? |
|------|-------------|-------|
| 1 | ts-route-service | False |
| 2 | mysql | True |
| 3 | ts-order-service | True |

**算法只要命中任意一个 ground truth service 即算正确**。这意味着：

- 对于网络类故障，命中 source 或 target 都算正确
- 对于 HTTP 请求级故障，命中 caller 或 callee 都算正确
- MRR 计算时取最高排名的命中（`1/rank` 最小 rank）
- AC@k 计算时，top-k 中任意一个命中即为 True

### 5.3 对指标计算的影响

以 MRR（Mean Reciprocal Rank）为例，来自 `evaluation/ranking.py`：

```python
def calc_mrr(df: pl.DataFrame) -> pl.DataFrame:
    hit_df = df.filter(pl.col("hit"))               # 只保留命中的行
    min_rank = hit_df.group_by("datapack").agg(
        pl.col("rank").min().alias("min_rank")      # 取最高排名
    )
    return min_rank.with_columns(
        (1.0 / pl.col("min_rank")).alias("mrr")     # 1/rank
    )
```

对于上面的例子，`min_rank = 2`，MRR = 0.5。如果算法将 `mysql` 排在 rank 1，则 MRR = 1.0。

### 5.4 多 Service 对评估结果的实际影响

在当前数据集中：

- 369 个 datapack 只有 1 个 ground truth service（难度相对较低）
- 1053 个 datapack 有 2 个 ground truth service（算法有更多命中机会）

这意味着在 2-service 场景下，随机猜测的 baseline 命中率约为 `2/N`（N 为总 service 数），而非 `1/N`。评估时如果需要公平对比，应当注意到这一差异。

## 6. convert_dataset 调用链详解

### 6.1 脚本如何调用 convert_dataset

```python
# build_local_rcabench_meta.py:126-141
def build_meta(src: Path, data_root: Path, dataset: str) -> tuple[int, int]:
    src = src.resolve()
    data_root = data_root.resolve()
    dataset_data = data_root / "data" / dataset

    dataset_data.parent.mkdir(parents=True, exist_ok=True)

    # 创建 symlink: data/rcabench-platform-v2/data/rcabench → 实际数据目录
    if dataset_data.exists() or dataset_data.is_symlink():
        if dataset_data.resolve() != src:
            raise SystemExit(f"{dataset_data} already exists and does not point to {src}")
    else:
        dataset_data.symlink_to(src, target_is_directory=True)

    loader = PreconvertedRCABenchDatasetLoader(src, dataset)
    convert_dataset(loader, root=data_root, skip_finished=True, parallel=1)
```

关键参数：

- `skip_finished=True`：已转换的 datapack 不会重新处理数据
- `parallel=1`：单线程执行，避免多进程 symlink 问题

### 6.2 convert_dataset 内部流程

```
PreconvertedRCABenchDatasetLoader
    │
    │  __len__() → 1422
    │  __getitem__(i) → PreconvertedRCABenchDatapackLoader
    ▼
convert_dataset()
    │
    │  对每个 datapack:
    │    _convert_datapack(loader, i, data_folder, skip_finished=True)
    │        │
    │        │  PreconvertedRCABenchDatapackLoader.labels()
    │        │    → [Label(level="service", name="mysql"),
    │        │       Label(level="service", name="ts-order-service")]
    │        │
    │        │  检查 .finished → 存在 → 跳过数据写入
    │        │
    │        │  返回 (datapack_name, labels)
    │        ▼
    │  收集所有结果，构建 index_rows 和 labels_rows
    │
    │  index_df = pl.DataFrame(index_rows).sort(by=pl.all())
    │  labels_df = pl.DataFrame(labels_rows).sort(by=pl.all())
    │
    │  save_parquet(index_df, meta_folder / "index.parquet")
    │  save_parquet(labels_df, meta_folder / "labels.parquet")
    ▼
最终输出:
    data/rcabench-platform-v2/meta/rcabench/index.parquet   (1422 rows)
    data/rcabench-platform-v2/meta/rcabench/labels.parquet  (2475 rows)
```

### 6.3 为什么 labels 数量 (2475) 大于 datapacks 数量 (1422)

```
labels 总数 = Σ 每个 datapack 的 service 数量
            = 369 × 1 + 1053 × 2
            = 369 + 2106
            = 2475 ✓
```

这恰好验证了多 service 的展开逻辑。

## 7. PreconvertedRCABenchDatapackLoader 设计说明

### 7.1 为什么 data() 抛出异常

```python
def data(self) -> dict[str, Any]:
    raise RuntimeError(
        f"{self.name} is expected to be preconverted and marked with .finished; "
        "this helper only reuses convert_dataset() to build index.parquet and labels.parquet."
    )
```

因为 `convert_dataset()` 内部的 `convert_datapack()` 会调用 `loader.data()` 来获取数据并写入磁盘。但在 preconverted 场景下：

1. 数据已经存在于目标目录
2. `.finished` 标记已存在
3. `skip_finished=True` 使得 `convert_datapack()` 不会真正调用 `data()`

所以 `data()` 抛出异常是一个**安全网**——如果某种原因导致 `skip_finished` 逻辑失效，会立即报错而非静默覆盖数据。

### 7.2 _CallableName 的作用

```python
class _CallableName(str):
    def __call__(self) -> str:
        return str(self)
```

这是一个兼容层。`DatapackLoader.name` 是 `@property`，返回 `str`。但 `convert_datapack()` 中直接用 `datapack = loader.name` 作为字符串使用。`_CallableName` 同时满足：

- `str(datapack)` → 字符串值
- `datapack()` → 同样返回字符串值

这确保了与 `convert_dataset()` 内部所有使用方式的兼容。

## 8. 与平台原始 RCABenchDatapackLoader 的对比

平台原始的 `RCABenchDatapackLoader`（在 `cli/dataset_transform/` 中实现）完成以下工作：

| 职责 | 原始 Loader | Preconverted Loader |
|------|-------------|---------------------|
| 读取原始数据（CSV 等） | 是 | 否 |
| 转换为 parquet | 是 | 否（已转换） |
| 从 injection.json 提取 labels | 是 | 是（使用 `_service_names`） |
| 写入 .finished 标记 | 是 | 否（已存在） |
| 生成 index.parquet | 是（通过 `convert_dataset`） | 是（通过 `convert_dataset`） |
| 生成 labels.parquet | 是（通过 `convert_dataset`） | 是（通过 `convert_dataset`） |

**核心差异**：Preconverted Loader 不做数据转换，只提供 labels 信息，让 `convert_dataset()` 走完元数据写入流程。

## 9. 验证方法

### 9.1 检查 labels.parquet 内容

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
uv run --package baro python -c "
import polars as pl
df = pl.read_parquet('data/rcabench-platform-v2/meta/rcabench/labels.parquet')
print(f'总行数: {df.height}')
print(f'列名: {df.columns}')
print(f'gt.level 分布: {df[\"gt.level\"].value_counts()}')
print()
print('多 service 示例:')
multi = df.filter(pl.col('datapack') == 'ts0-mysql-corrupt-jkgn5j')
print(multi)
"
```

### 9.2 验证 label 数量

```bash
uv run --package baro python -c "
import polars as pl
df = pl.read_parquet('data/rcabench-platform-v2/meta/rcabench/labels.parquet')
per_datapack = df.group_by('datapack').len()
print(f'1 label: {(per_datapack[\"len\"] == 1).sum()}')
print(f'2 labels: {(per_datapack[\"len\"] == 2).sum()}')
print(f'总计: {df.height} labels, {per_datapack.height} datapacks')
"
```

### 9.3 运行 eval 验证 labels 可用

```bash
uv run --package baro python algorithms/baro/main.py eval show-datasets
uv run --package baro python algorithms/baro/main.py eval single baro rcabench ts0-mysql-corrupt-jkgn5j --clear
```

## 10. 总结

| 结论 | 说明 |
|------|------|
| 逻辑一致性 | 脚本 `_service_names()` 与平台原始 `get_service_names()` 核心提取逻辑完全一致，仅错误处理策略不同（静默容错 vs assert 硬报错） |
| 多 service 处理 | 每个 service 在 `labels.parquet` 中展开为独立行；评估时命中任意一个即算正确 |
| 74% 多 service | 当前数据集中 1053/1422 的 datapack 包含 2 个 ground truth service，这是网络类和 HTTP 类故障的正常特征 |
| labels 总数 | 369×1 + 1053×2 = 2475，与构建输出一致 |
| eval 兼容性 | 生成的 `labels.parquet` 列名、格式与 eval CLI 完全兼容，已通过 baro/nezha/rcd 等算法验证 |
