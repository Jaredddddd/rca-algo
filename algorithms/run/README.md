# RUN

```bash
sudo juicefs mount redis://10.10.10.38:6379/1 /mnt/jfs -d --cache-size=1024

mkdir data
cd data
ln -s /mnt/jfs/rcabench_dataset ./
ln -s /mnt/jfs/rcabench-platform-v2 ./

./main.py eval single RUN rcabench ts3-ts-route-plan-service-request-delay-59s2q4

mkdir temp
ALGORITHM=RUN INPUT_PATH=data/rcabench_dataset/ts3-ts-route-plan-service-request-delay-59s2q4 OUTPUT_PATH=temp uv run python run_exp.py
```



# 20260524优化

优化建议（不改算法逻辑，只改工程实现）
优先级	改动	预期加速	难度
P0	关掉 set_detect_anomaly	~20-30%	改一行
P0	DataLoader 只创建一次，缓存 scaler	~10-15%	小改
P1	逐列训练改为一次性 batch 化：把 N 列的模型 forward 合并为一次 batched matmul	5-10x（GPU 利用率从极低变高）	中等
P1	降低 needs_cpu_count() 从 16 到 4，让更多 worker 并行处理不同 datapack	2-4x	改一行
P2	每列训练完后显式 del model; torch.cuda.empty_cache()	避免 OOM 风险	小改
P2	num_workers 从 0 改为 2-4	小幅提升	改一行
综合估计：P0 + P1 改完后，单个 datapack 耗时可从 ~22 分钟降到 2-5 分钟，全量 1422 个约 2-5 天（取决于并行度）。


修改总结
set_detect_anomaly 已注释 — 去掉逐 op NaN 检查开销
DLinear 模型 batched 化 — ModuleList + Python for 循环 → grouped Conv1d，一次 kernel 完成所有通道的线性变换
DataLoader 缓存 — data_provider 只在 Run() 入口调一次，60 列共享同一个 DataLoader 和 StandardScaler
forward 中 batch_size 不再硬编码 — 用实际 B 替代魔数 128
needs_cpu_count 从 16 → 2 — 同等 CPU 下可开更多并行 worker
每列训练后 torch.cuda.empty_cache() — 及时释放 GPU 显存


单 case 总耗时 1176 秒，其中 DAG 剪枝（pearson_correlation 循环）占了约 14 分钟。这部分是纯 Python 循环，也可以用 NumPy 向量化显著加速，但是还没做