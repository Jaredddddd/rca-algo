"""将 output/rcabench-platform-v2/data 中的 parquet 文件转为 CSV。

用法:
  # 转换全部
  python parquet_to_csv.py

  # 只转换指定算法
  python parquet_to_csv.py evidencerank

  # 指定多个算法
  python parquet_to_csv.py evidencerank eadro

输出目录结构: data_csv/{algorithmName}/{caseName}/*.csv
"""

import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path("output/rcabench-platform-v2/data")
DST_DIR = Path("output/rcabench-platform-v2/data_csv")


def convert(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(src)
    df.to_csv(dst, index=False)


def main() -> None:
    if not SRC_DIR.exists():
        print(f"源目录不存在: {SRC_DIR}")
        sys.exit(1)

    algorithms = [a.lower() for a in sys.argv[1:]] if len(sys.argv) > 1 else None

    parquets = list(SRC_DIR.rglob("*.parquet"))
    if not parquets:
        print("未找到 parquet 文件")
        sys.exit(1)

    converted = 0
    for p in parquets:
        # 路径结构: data/{dataset}/{caseName}/{algorithmName}/{file}.parquet
        parts = p.relative_to(SRC_DIR).parts
        if len(parts) < 4:
            print(f"  跳过（路径层级不足）: {p}")
            continue

        algorithm_name = parts[-2]
        case_name = parts[-3]

        if algorithms and algorithm_name.lower() not in algorithms:
            continue

        dst = DST_DIR / algorithm_name / case_name / p.with_suffix(".csv").name
        print(f"  {p} -> {dst}")
        convert(p, dst)
        converted += 1

    print(f"\n完成，共转换 {converted} 个文件")


if __name__ == "__main__":
    main()
