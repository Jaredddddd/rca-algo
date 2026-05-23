#!/usr/bin/env bash
# 合并所有算法的 perf-report 到同一张表格。
# 用法: ./scripts/combined_report.sh [dataset] [--sort-by COLUMN] [--asc]
#   dataset    — 数据集名称 (默认: rcabench)
#   --sort-by  — 排序依据列 (默认: MRR)
#   --asc      — 升序排列 (默认降序)
set -euo pipefail

DATASET="${1:-rcabench}"
shift || true

cd "$(dirname "$0")/.."

# 使用 workspace 的 Python 环境（通过任意一个 workspace package 启动）
uv run --package baro python scripts/combined_report.py "$DATASET" "$@"
