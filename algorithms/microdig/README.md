# MicroDig

```bash
sudo juicefs mount redis://10.10.10.119:6379/1 /mnt/jfs -d --cache-size=1024

mkdir data
cd data
ln -s /mnt/jfs/rcabench_dataset ./
ln -s /mnt/jfs/rcabench-platform-v2 ./

./main.py eval single microdig rcabench ts3-ts-route-plan-service-request-delay-59s2q4

mkdir temp
ALGORITHM=microdig INPUT_PATH=data/rcabench_dataset/ts3-ts-route-plan-service-request-delay-59s2q4 OUTPUT_PATH=temp uv run python run_exp.py


export RCABENCH_BASE_URL=http://10.10.10.220:32080
export RCABENCH_USERNAME=admin
export RCABENCH_PASSWORD=admin123
# upload algorithm
docker build -t 10.10.10.240/library/rca-algo-microdig:820c2d7 .
docker push 10.10.10.240/library/rca-algo-microdig:820c2d7
rca upload-algorithm-harbor ./
# batch test
sudo -E .venv/bin/python run.py batch-test --label 8.23microdig820c2d7
```

```
┌───────────┬───────────┬─────────────────┬───────────┬───────┬───────┬───────┬───────┬─────┬─────┬─────┬────────────┬────────────────┐
│ algorithm ┆ dataset   ┆ dataset_version ┆ level     ┆  top1 ┆  top3 ┆  top5 ┆   mrr ┆ as1 ┆ as3 ┆ as5 ┆ efficiency ┆ datapack_count │
│ ---       ┆ ---       ┆ ---             ┆ ---       ┆   --- ┆   --- ┆   --- ┆   --- ┆ --- ┆ --- ┆ --- ┆        --- ┆            --- │
│ str       ┆ str       ┆ str             ┆ str       ┆   f64 ┆   f64 ┆   f64 ┆   f64 ┆ f64 ┆ f64 ┆ f64 ┆        f64 ┆            i64 │
╞═══════════╪═══════════╪═════════════════╪═══════════╪═══════╪═══════╪═══════╪═══════╪═════╪═════╪═════╪════════════╪════════════════╡
│ microdig  ┆ pair-diag ┆ all-8.23        ┆ service   ┆ 0.528 ┆ 0.756 ┆ 0.791 ┆ 0.647 ┆ 0.0 ┆ 0.0 ┆ 0.0 ┆        0.0 ┆           1129 │
└───────────┴───────────┴─────────────────┴───────────┴───────┴───────┴───────┴───────┴─────┴─────┴─────┴────────────┴────────────────┘
```
