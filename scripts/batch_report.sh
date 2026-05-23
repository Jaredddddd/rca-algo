#!/usr/bin/env bash
# Batch perf-report for all algorithms.
# Usage: ./scripts/batch_report.sh [dataset] [output_dir]
#   dataset    — dataset name passed to perf-report (default: rcabench)
#   output_dir — where to collect merged reports (default: output/rcabench-platform-v2/meta/<dataset>)
set -euo pipefail

DATASET="${1:-rcabench}"
cd "$(dirname "$0")/.."

# Workspace algorithms (share the same Python/dependency environment)
# Each entry: "uv-package-name::algorithm-main.py-path"
WORKSPACE_ALGOS=(
  "baro::algorithms/baro/main.py"
  "nezha::algorithms/nezha/main.py"
  "shapleyiq::algorithms/shapleyiq/main.py"
  "MicroDig::algorithms/microdig/main.py"
  "rcaeval-rcd::algorithms/rcd/main.py"
  "rcaeval_causalrca::algorithms/causalrca/main.py"
  "rcaeval_run::algorithms/run/main.py"
  "SimpleRCA::algorithms/simplerca/main.py"
)

# Standalone algorithms (separate Python environments, run from their own directory)
STANDALONE_ALGOS=(
  "algorithms/art"
  "algorithms/eadro"
  "algorithms/diagfusion"
)

echo "=== Workspace algorithms ==="
for entry in "${WORKSPACE_ALGOS[@]}"; do
  pkg="${entry%%::*}"
  path="${entry##*::}"
  echo "--- $pkg ($path) ---"
  uv run --package "$pkg" python "$path" eval perf-report "$DATASET"
done

echo ""
echo "=== Standalone algorithms ==="
for dir in "${STANDALONE_ALGOS[@]}"; do
  if [ -f "$dir/main.py" ]; then
    echo "--- $dir ---"
    (
      cd "$dir"
      uv run python main.py eval perf-report "$DATASET"
    )
  else
    echo "--- $dir: main.py not found, skipping ---"
  fi
done

echo ""
echo "=== Done. Reports per algorithm are under output/rcabench-platform-v2/meta/$DATASET/ ==="
