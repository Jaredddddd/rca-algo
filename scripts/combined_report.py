#!/usr/bin/env python3
"""
合并所有算法的 perf-report 到同一张表格。

用法:
    python scripts/combined_report.py [dataset] [--sort-by COLUMN] [--desc]

读取 output/rcabench-platform-v2/data/{dataset}/*/output.parquet 下所有算法的结果，
计算统一指标，输出一张包含全部算法的汇总表。
"""
import argparse
import sys
from pathlib import Path

import polars as pl

OUTPUT_ROOT = Path("output/rcabench-platform-v2")

DISPLAY_COLUMNS = [
    "algorithm",
    "total",
    "error",
    "runtime.seconds:avg",
    "MRR",
    "AC@1.count",
    "AC@3.count",
    "AC@5.count",
    "AC@1",
    "AC@3",
    "AC@5",
    "Avg@3",
    "Avg@5",
]


def discover_output_files(dataset: str) -> list[Path]:
    """扫描 data/{dataset}/ 下所有算法的 output.parquet。"""
    data_dir = OUTPUT_ROOT / "data" / dataset
    if not data_dir.exists():
        print(f"错误: 数据目录不存在: {data_dir}", file=sys.stderr)
        sys.exit(1)

    files = sorted(data_dir.rglob("output.parquet"))
    # 过滤掉 meta 目录下的合并文件，只保留 per-algorithm 的
    files = [f for f in files if "meta" not in f.parts]
    return files


def compute_dataset_perf(output_df: pl.DataFrame) -> pl.DataFrame:
    """计算 dataset 级别的汇总指标。"""
    from rcabench_platform.v2.evaluation.ranking import calc_all_perf

    perf_df = calc_all_perf(output_df, agg_level="dataset", include_sampled=False)

    # 只保留非 sampled 行
    if "sampler.name" in perf_df.columns:
        perf_df = perf_df.filter(pl.col("sampler.name").is_null())
        perf_df = perf_df.drop(["sampler.name", "sampler.rate", "sampler.mode"])

    return perf_df


def main():
    parser = argparse.ArgumentParser(description="合并所有算法的 perf-report")
    parser.add_argument("dataset", nargs="?", default="rcabench", help="数据集名称 (默认: rcabench)")
    parser.add_argument("--sort-by", default="MRR", help="排序依据列 (默认: MRR)")
    parser.add_argument("--desc", action="store_true", default=True, help="降序排列 (默认)")
    parser.add_argument("--asc", action="store_true", help="升序排列")
    args = parser.parse_args()

    dataset = args.dataset
    sort_col = args.sort_by
    descending = not args.asc

    output_files = discover_output_files(dataset)
    if not output_files:
        print(f"未找到 {dataset} 的输出文件", file=sys.stderr)
        sys.exit(1)

    print(f"发现 {len(output_files)} 个算法输出文件\n")

    dfs = []
    for f in output_files:
        try:
            df = pl.read_parquet(f)
            if len(df) > 0:
                dfs.append(df)
        except Exception as e:
            print(f"警告: 读取 {f} 失败: {e}", file=sys.stderr)

    if not dfs:
        print("没有有效的输出数据", file=sys.stderr)
        sys.exit(1)

    combined = pl.concat(dfs, rechunk=True)

    # 统计各算法的数据量
    algorithms = combined["algorithm"].unique().sort()
    print(f"包含算法: {', '.join(algorithms.to_list())}")
    print(f"总 datapack 结果: {len(combined)} 行\n")

    perf_df = compute_dataset_perf(combined)

    # 排序
    if sort_col in perf_df.columns:
        perf_df = perf_df.sort(sort_col, descending=descending)
    else:
        print(f"警告: 排序列 '{sort_col}' 不存在，使用默认顺序", file=sys.stderr)

    # 选择显示列
    available = [c for c in DISPLAY_COLUMNS if c in perf_df.columns]
    display_df = perf_df.select(available)

    # 打印表格
    with pl.Config(
        tbl_rows=len(display_df),
        tbl_cols=len(display_df.columns),
        fmt_str_lengths=120,
        tbl_width_chars=200,
        tbl_cell_numeric_alignment="RIGHT",
        thousands_separator=True,
    ):
        print(display_df)

    # 同时保存到 meta 目录
    from rcabench_platform.v2.utils.serde import save_parquet

    meta_dir = OUTPUT_ROOT / "meta" / dataset
    meta_dir.mkdir(parents=True, exist_ok=True)
    save_parquet(perf_df, path=meta_dir / "dataset.perf.combined.parquet")
    print(f"\n合并报告已保存: {meta_dir / 'dataset.perf.combined.parquet'}")


if __name__ == "__main__":
    main()
