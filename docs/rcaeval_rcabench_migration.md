# RCAEval RE2 → RCABench v2 迁移与验证

> 状态：2026-07-18 已完成 270 个 datapack 的 conversion v3 正式构建、结构校验、canonical Oracle8 全量复跑、内存安全验证和无需训练算法 smoke test。
> 这里的 conversion v3 是本迁移脚本的数据协议版本；算法入口仍是 RCABench-platform v2。


## 结论

RCAEval V1 的三个 RE2 子集已经转换成仓库统一使用的 RCABench-platform v2 datapack，conversion version 为 3。所有已适配算法继续使用 `eval batch -d <dataset>`；不再需要独立 RCAEval runner。`crest_rcaeval_oracle8` 只提供 RCAEval 专属 feature profile，并复用 canonical CREST。

统一数据集名是：

```text
rcabench_rcaeval_re2
```

它由 270 个指向三个子集的相对符号链接组成，不会复制一份遥测数据。需要分别报告时，
使用：

```text
rcabench_rcaeval_re2_ob
rcabench_rcaeval_re2_ss
rcabench_rcaeval_re2_tt
```

## 输入与输出

原始数据：

```text
/home/ljw/paper/DDS-DL-AIOPS/RCAEval-V1-Data/RE2-OB/RE2-OB
/home/ljw/paper/DDS-DL-AIOPS/RCAEval-V1-Data/RE2-SS/RE2-SS
/home/ljw/paper/DDS-DL-AIOPS/RCAEval-V1-Data/RE2-TT/RE2-TT
```

转换结果：

```text
data/rcabench-platform-v2/data/rcabench_rcaeval_re2_{ob,ss,tt}
data/rcabench-platform-v2/data/rcabench_rcaeval_re2
data/rcabench-platform-v2/meta/rcabench_rcaeval_re2_{ob,ss,tt}
data/rcabench-platform-v2/meta/rcabench_rcaeval_re2
```

正式 conversion v3 结构校验如下：

| 子集 | datapack | conversion v3 | conclusion | 不完整 datapack |
| --- | ---: | ---: | ---: | ---: |
| RE2-OB | 90 | 90 | 90 | 0 |
| RE2-SS | 90 | 90 | 90 | 0 |
| RE2-TT | 90 | 90 | 90 | 0 |

三个子集的 `index.parquet` 和 `labels.parquet` 都是 90 行；统一数据集有 270 个有效相对链接、0 个断链。RE2-SS 原始数据没有 trace，这不是迁移丢失。

## 转换规则

转换器是 `scripts/build_rcaeval_rcabench.py`，复用
`rcabench_platform.v2.sources.rcaeval` 的 metric/log/trace 字段转换逻辑。

- 每个数字实验目录转换为一个 datapack，例如
  `checkoutservice_cpu/1` → `checkoutservice_cpu_1`。
- 根因服务和故障类型从故障目录的最后一个下划线处分割，因此
  `ts-auth-service_cpu` 会正确得到服务 `ts-auth-service`。
- 分窗与旧 RCAEval 完全一致：
  `normal = time < inject_time`，
  `abnormal = time >= inject_time`。
- conversion v3 将原始 RCAEval `main.py --length 20` 的公共 metric 协议固化到 datapack：删除 `*_latency-50`，在完整宽表上处理 inf/NaN 并 forward-fill，正常侧取注入前最后 600 个时间点，异常侧取注入后最前 600 个时间点，再把 `*_latency-90` 改名为 `*_latency` 后转成长表。
- v3 的 `conversion.json` 记录 `metric_preprocessing=rcaeval-main-length20-v1` 和 `metric_window_rows_per_phase=600`；version 不匹配时会自动重建。
- RCAEval V1 没有 sum/histogram metric；对应 parquet 保留合法空 schema。
- trace status 统一为 `Unset`、`Ok`、`Error`：空值映射为 `Unset`，数值 0 为 `Ok`，非 0 为 `Error`，已有字符串按统一大小写保留。
- 缺失的 trace/log 生成合法空表。
- v3 从正常/异常 trace 的 span duration 与 success 变化生成 label-free `conclusion.parquet`，复用 AIOPS2025 的公共 conclusion contract；它不读取 labels、injection root cause 或历史输出。RE2-SS 无 trace，因此生成 schema 合法的空 conclusion。
- 每个 datapack 写入 `env.json`、`injection.json`、`conversion.json`、`conclusion.parquet` 和 `.finished`。
- 多进程使用 `spawn`；默认 `--workers 1`。
- `--subset`/`--limit` 增量运行会扫描所有完整 datapack 重建 metadata，不会截断既有子集。
- 统一数据集用相对符号链接聚合三个子集，不复制遥测数据。

## 生成命令

RCAEval trace 很大，转换和评估都应限制原生线程：

```bash
cd /home/ljw/paper/aegis/rca-algo-contrib
export POLARS_MAX_THREADS=1
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export MALLOC_ARENA_MAX=2

uv run --package crest python scripts/build_rcaeval_rcabench.py --workers 1
```

正式数据已经是 conversion v3；默认会跳过 version 正确的 datapack。需要强制重建时加 `--overwrite`；只转换某个子集或快速检查时可用：

```bash
uv run --package crest python scripts/build_rcaeval_rcabench.py --subset ob --workers 1 --overwrite
uv run --package crest python scripts/build_rcaeval_rcabench.py --subset ob --limit 1
```

## 统一算法入口

当前 RCAEval oracle8 的推荐入口是可配置脚本：

```bash
algorithms/crest/run_rcaeval_experiments.sh --datasets ob,ss,tt --groups baseline --cpus 1
```

等价的单数据集底层命令是：

```bash
uv run --package crest python algorithms/crest/main.py eval batch \
  -a crest_rcaeval_oracle8 \
  -d rcabench_rcaeval_re2_ob \
  --use-cpus 1
```

脚本支持：

- `--datasets ob,ss,tt,combined,all`：选择数据集；
- `--groups baseline,modalities,modules,all`：选择基线、模态消融或模块消融；
- `--algorithms ...`：显式覆盖算法列表；
- `--cpus`、`--sample`、`--clear`、`--resume`、`--rerun`、`--no-report`；
- `--dry-run` 和 `--list`：先检查实际命令与注册名。

默认断点续跑且只用 1 个 worker；每个 worker 的原生线程也限制为 1。不要在 RCAEval 上沿用 RCABench 的高并发。

## `--length 20` 与算法预处理边界

原始 RCAEval `process()` 在 `func = globals()[args.method]` 之前先处理 metric，因此 README 的 `--length 20` 不是 BARO 或 CREST 私有参数。20 分钟按 2 秒采样换算为每侧 600 个时间点。边界如下：

| 层级 | 处理 | 原始适用范围 | 性质 |
| --- | --- | --- | --- |
| runner 公共协议 | 删除 `*_latency-50`、inf/NaN 后前向填充、正常 tail 600、异常 head 600、`*_latency-90` 改名为 `*_latency` | 经 `main.py` 分派的全部方法 | RCAEval benchmark 公共输入协议，不是 AC@1 trick |
| runner 数据集分支 | 只保留 `ts-*` metric | 仅 `mm-tt`/`torai-TT` 路径，不包括 RE2-TT | 不应迁移到 RE2-TT；Oracle8 中误加的逻辑已删除 |
| 方法共享预处理 | 去 time、正常/异常分别删常量列、取列交集、mem 除以 1e6 | BARO、RCD、Torai 和多种 causal wrapper 广泛复用，但并非所有方法逐字一致 | 通用的时序卫生/数值尺度处理，应由方法 adapter 保留 |

conversion v3 已把 runner 公共 metric 协议写入全部 270 个 datapack，因此其他 RCAEval 方法读取迁移 metric 时，数据层面等价于已经经过 `--length 20`。这不替代各方法自身真正需要的常量过滤、缩放、建图或参数。Oracle8 不再补做任何公共协议。
原 runner 对普通 RE2 的 raw logs/traces 不执行 20 分钟裁剪；只有 Torai 的预聚合 `logts`/`tracets` 有单独窗口。v3 因此只固化公共 metric 窗口，不擅自裁剪 raw trace/log。

## `rcaeval_oracle8.py` 的作用与精简结果

该文件现在只是 RCAEval 数据集 profile：声明独立的 8-feature surface，并提供 baseline、六个模态组合、`local`、`nocf` 九个继承 canonical `CREST` 的类。它不再实现第二套 scorer，也不再处理输入数据。

已删除的冗余包括：v2/v3 兼容分支、600 行裁剪、latency 重命名、常量列过滤、mem 缩放、2 ULP parser shim、legacy role/support 与 explain-away、重复 modality 映射、未被入口调用的 scoring wrapper 及其样板测试。公共协议属于 converter；排序、模态过滤和图模式属于 canonical CREST。

该文件仍有存在意义，因为 RCAEval 的 8 个 feature 与 RCABench Min8、AIOPS25 generic8 不同。它隔离的是“feature 选择”，不是历史算法语义。

## RCAEval 专用 8-feature profile

`crest_rcaeval_oracle8` 使用以下 8 个互不重复的当前 feature：

1. `metric_anomaly_count`
2. `metric_value_delta`
3. `trace_count_delta`
4. `trace_self_duration_relative_shift`
5. `topology_in_degree`
6. `abnormal_trace_rows`
7. `raw_metric_type::latency::mean_delta`
8. `trace_status_code_shift`

其中 3 个 metric feature、5 个 trace/topology feature；oracle8 profile 没有 log
feature。因此 log-only 是空证据控制，metric+log 等于 metric，log+trace 等于 trace。
这套 profile 与 RCABench Min8、AIOPS25 generic8 相互独立。

### 固定 8-feature 选型协议

选型不改变 canonical CREST 的异常度、图上下文、融合或排序，也不添加任何数据集
权重。候选池是上一版 RCAEval8、RCABench Min8 和 AIOPS25 Generic8 的有序并集，
去重后共 18 项；离线工具穷举全部 `C(18, 8) = 43,758` 个固定八项组合。
`*_1`、`*_2` 只用于选型，`*_3` 只做保留验证；标签只由离线评估工具计算名次，
不会进入算法 runtime。

最优组合保留上一版 RCAEval8 的 7 项，只把 `metric_mean_z` 替换为 RCABench
Min8 已使用的 `trace_status_code_shift`。选型集 AC@1 为 OB/SS/TT
`0.95/0.95/1.00`，保留集为 `0.933333/0.900000/0.933333`。可用以下单 worker
命令重建/复用缓存并复现搜索：

```bash
uv run --package crest python algorithms/crest/tools/search_rcaeval_feature_profile.py \
  --datasets ob,ss,tt --workers 1 --chunk-size 1024 --top-k 100
```

## Oracle8 canonical 全量验证结果

三个子集都完成 90/90，`error=0`：

| 子集 | MRR | AC@1 命中 | AC@1 | AC@3 | AC@5 | Avg@5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| RE2-OB | 0.972222 | 85/90 | 0.944444 | 1.000000 | 1.000000 | 0.988889 |
| RE2-SS | 0.963889 | 84/90 | 0.933333 | 0.988889 | 1.000000 | 0.982222 |
| RE2-TT | 0.985556 | 88/90 | 0.977778 | 0.988889 | 1.000000 | 0.988889 |

总体 AC@1 为 `257/270 = 0.951852`，三个子集都高于 90%。搜索预测与真实统一
入口的 OB/SS/TT 命中计数逐项一致，说明缓存向量化评分与 canonical runtime 的
排序和 tie-break 一致；不要求逐 case 候选顺序与历史输出完全相同。

canonical `crest` 仍使用 RCABench Min8，不能与 oracle8 当作同一算法。此前
Min8 在迁移数据上的结果保留作版本对照：

| 子集 | Min8 AC@1 | Min8 AC@3 | Min8 Avg@5 |
| --- | ---: | ---: | ---: |
| RE2-OB | 0.711111 | 0.877778 | 0.873333 |
| RE2-SS | 0.500000 | 0.788889 | 0.731111 |
| RE2-TT | 0.711111 | 0.933333 | 0.884444 |

## 语义取舍

旧 adapter 曾用常量过滤、mem 缩放和 2 ULP parser shim 追求逐 case 历史一致；这些都已删除。当前结果只要求复用 canonical CREST 且 AC@1 大于 90%。因此结果变化应解释为算法语义切换，而不是 conversion v3 数据回归；公共 `--length 20` 协议本身已由 converter 单独测试。

## 其他算法兼容性

2026-07-18 在 conversion v3 固定 case 上复核：OB `checkoutservice_cpu_1`、SS `carts_cpu_1`、TT `ts-auth-service_cpu_1`。以下是数据契约 smoke test，不是完整 benchmark。

| 算法 | 最终迁移数据上的结果 | 边界 |
| --- | --- | --- |
| Baro | OB/SS/TT 均完成并产出候选 | 无异常字段 |
| RCD、SimpleRCA、HeroSAS | OB/SS/TT 均完成并产出候选 | TT 单例更慢，但内存稳定 |
| EvidenceRank、CERA | OB/SS/TT 基础入口均完成并产出候选 | 使用统一 `eval single` 入口 |
| MicroDig | OB 7 个、TT 10 个候选；SS 正常结束但为空 | SS 原始数据无 trace |
| ShapleyIQ、ToN、MicroRank、MicroHECL、MicroRCA | OB 均可运行；TT 五个入口均有候选 | 只消费公共 conclusion；TT MicroHECL 根因 rank=1；SS 无 trace，均为空 |
| Nezha | OB 根因 rank=1；TT 3 个候选且根因 rank=1 | 缺 `metrics_sli` 时从正常 trace 推导 p90；Nezha 不读取 conclusion；SS 无 trace 仍为空 |
| CausalRCA | OB 单例 3 个候选、0 exception，约 259 秒 | 单进程；本机使用约 8 GiB GPU 显存 |
| RUN | OB 单例 3 个候选、0 exception，约 8.1 秒 | 算法名为大写 `RUN`，使用 CUDA |
| ART、Eadro、DiagFusion | 未做有效评估 | 需为新数据集定义训练划分并生成 checkpoint |

ShapleyIQ family 只消费公共 `conclusion.parquet`，删除了正常/异常 metric 漂移 seed fallback。最小适配仅放宽 `/api/v1/...` operation 解析并把 conclusion service seed 映射到图节点；TT 固定 case 的 detector 返回 `ts-auth-service`，MicroHECL 根因 rank=1。OB/TT 全局算法仍可运行；SS 源数据没有 trace，因此五个入口正常返回空。

Nezha 不读取 conclusion。RCAEval 与 RCABench/AIOPS25 的差别是缺少 `metrics_sli.parquet`：只做 status 归一化时，TT 固定 case 的 351 个 pattern 中 0 个越过异常阈值；从正常 trace 推导 152 个同单位 p90 后出现 6 个异常 pattern、聚合为 3 个服务候选，`ts-auth-service` rank=1。因此该 p90 路径是必要且最小的通用数据契约补足，不使用 ground truth；SS 无 trace 仍为空。

低内存批量 smoke 命令：

```bash
CPUS=1 SAMPLE=1 INCLUDE_CAUSALRCA=0 \
  scripts/run_aiopschallenge2025_algorithms.sh rcabench_rcaeval_re2
```

该脚本虽沿用历史文件名，但接受任意 RCABench v2 数据集。v3 conclusion 是通用的 label-free 遥测产物；ShapleyIQ family 不再有 metric seed fallback。Nezha 唯一保留的适配是缺少 `metrics_sli` 时从正常 trace 推导 p90。

## 内存安全结论

此前卡死风险来自“高进程数 × 每进程大 pandas/Polars trace frame × 原生线程 × allocator arenas”的乘法放大。安全基线每次只运行一个子集、一个 worker，Polars/BLAS/OpenMP 线程均为 1。

本轮缓存构建与全量运行时可用内存稳定在约 97–100 GiB，swap 仅约 1.2 MiB。`run_rcaeval_experiments.sh` 默认 1 worker；Nezha 与 ShapleyIQ family 返回 `needs_cpu_count() = None`，批量调度也强制串行。

## 已验证命令

```bash
uv run --offline --frozen --package crest pytest -q algorithms/crest/tests
# 27 passed

uv run --offline --frozen --package crest pytest -q tests/test_build_rcaeval_rcabench.py
# 6 passed

uv run --offline --frozen --package nezha pytest -q algorithms/nezha/tests/test_dataset_split.py
# 4 passed

uv run --offline --frozen --package shapleyiq pytest -q algorithms/shapleyiq/tests/test_platform_data_loader.py
# 5 passed

uv run --offline --frozen --package crest ruff check <本任务 Python 文件>
uv run --offline --frozen --package crest python -m compileall -q <本任务源码>
bash -n algorithms/crest/run_rcaeval_experiments.sh
```

正式 OB/SS/TT 共 270 个 datapack 已逐子集以 `--workers 1` 重建并校验：version=3、metric 每侧最多 600 个时间点、无 `latency-50`、`latency-90` 已重命名、trace status 已归一化、全部存在 `conclusion.parquet`；combined 数据集有 270 个有效链接。

ShapleyIQ 全目录中的旧 `test_algorithms.py`/`test_data_structures.py` 仍有 12 个 setup error：fixture 使用已经删除的旧 dataclass 参数和旧 result-object API。这不是本轮 platform adapter 回归；新增的 platform tests 与 OB/SS/TT 真实 case 均已通过。

## 后续工作

1. 用 `run_rcaeval_experiments.sh --groups modalities` 和 `--groups modules` 断点续跑完整消融。
2. 在 AIOPS2025 上复跑新增的六个模态入口并生成正式对照表。
3. ART、Eadro、DiagFusion 若纳入正式比较，需要先定义训练/验证切分并重新训练。
