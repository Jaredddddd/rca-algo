# RUN

```bash
sudo juicefs mount redis://10.10.10.119:6379/1 /mnt/jfs -d --cache-size=1024

mkdir data
cd data
ln -s /mnt/jfs/rcabench_dataset ./
ln -s /mnt/jfs/rcabench-platform-v2 ./

./main.py eval single simplerca rcabench ts3-ts-route-plan-service-request-delay-59s2q4
```

**其他 dataset 见 report branch**

```sh
export RCABENCH_BASE_URL=http://10.10.10.220:32080
export RCABENCH_USERNAME=admin
export RCABENCH_PASSWORD=admin123
sudo -E .venv/bin/python run.py batch-test


docker build -t 10.10.10.240/library/rca-algo-baro:820c2d7 .
docker push 10.10.10.240/library/rca-algo-baro:820c2d7
rca upload-algorithm-harbor ./
```

# 说明

## 两个实现的对比

`main.py`（`SimpleRCA`）和 `nezha_rca.py`（`NezhaRCA`）是同一算法的两种独立实现，核心差异如下。

### 数据输入

| | main.py | nezha_rca.py |
|---|---------|-------------|
| 入参格式 | `[log_df, metric_df, trace_df]` + 可选 `normal_dfs` 列表 | 显式区分 normal/abnormal 共六个 DataFrame |
| Polars 兼容 | 自动 `.to_pandas()` 转换 | 纯 Pandas |
| Adapter | `DataAdapter` | `NezhaDataAdapter` |

### 日志分析

- **main.py**：基于 `message` 列关键词匹配（error/fail/exception/timeout/refused），比较 normal vs 异常期的频率比。
- **nezha_rca.py**：基于 `level` 列判断（`level != "INFO"` 即为异常），检测错误率升高、日志量下降，有三级 fallback（error ratio → count reduction → simple error）。

### 指标分析

- **main.py**：用 6-sigma（mean + 6σ）做阈值，normal 优先、fallback 到自身数据；分 CPU（权重 100）、Network_Latency（50）、其他 Latency（20）三级。
- **nezha_rca.py**：用 quantile(0.95) 做阈值，异常值需超过 `1.19 × 阈值` 且 CPU/内存 > 80；按 CPU → 内存 → 其他排序。

### Trace 分析

- **main.py**：duration ns → μs，P90 > 100 为异常；frontend 固定返回 10。
- **nezha_rca.py**：duration ns → ms，P90 > 100ms 为异常；跳过 frontend；有 parent-child span fallback。

### 结果融合

- **main.py**：**条件加权**——按异常类型分层组合（CPU 异常时 log×0.3、其他 metric 异常时 log×0.5、trace 异常时 log×0.7、仅 log 时直接用 log 分）。
- **nezha_rca.py**：**投票机制**——各模态 top-5 按排名给分（5/4/3/2/1），metrics 权重 1.2，其余 1.0，按总分排序。

### 其他差异

- **nezha_rca.py** 为 Nezha 数据集定制（columns 如 `CpuUsageRate(%)`、`MemoryUsageRate(%)`、`level`），CPU 4 核，有 `@timeit()`。
- **main.py** 更通用，兼容 Polars 输入，CPU 1 核，有 `clean_node_name()` 去除 pod 后缀。

