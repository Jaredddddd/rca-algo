#!/usr/bin/env bash
# Run local non-trainable/non-excluded algorithms on AIOpsChallenge2025 RCABench data.
#
# Excluded by design: art, eadro, diagfusion, RUN.

set -uo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/run_aiopschallenge2025_algorithms.sh [dataset]

Default dataset:
  aiopschallenge2025_rcabench_service

Environment variables:
  CPUS=16                         Number of workers passed to eval batch.
  CLEAR=1                         Use --clear before each algorithm run. Set CLEAR=0 to resume.
  SAMPLE=                         Optional sample size passed to eval batch.
  FAIL_FAST=0                     Set to 1 to stop at the first failed group.
  INCLUDE_CAUSALRCA=1             Set to 0 to skip CausalRCA.
  SYNC_CAUSALRCA=0                Set to 1 to run uv sync --frozen for CausalRCA first.
  RUN_COMBINED_REPORT=1           Set to 0 to skip the final combined report.
  SORT_BY=MRR                     Sort column for scripts/combined_report.py.
  LOGURU_LEVEL=WARNING            Default log level.
  DRY_RUN=0                       Set to 1 to print commands without executing them.

Examples:
  scripts/run_aiopschallenge2025_algorithms.sh
  CPUS=32 CLEAR=0 scripts/run_aiopschallenge2025_algorithms.sh
  INCLUDE_CAUSALRCA=0 SAMPLE=10 scripts/run_aiopschallenge2025_algorithms.sh
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DATASET="${1:-${DATASET:-aiopschallenge2025_rcabench_service}}"
CPUS="${CPUS:-16}"
CLEAR="${CLEAR:-1}"
SAMPLE="${SAMPLE:-}"
FAIL_FAST="${FAIL_FAST:-0}"
INCLUDE_CAUSALRCA="${INCLUDE_CAUSALRCA:-1}"
SYNC_CAUSALRCA="${SYNC_CAUSALRCA:-0}"
RUN_COMBINED_REPORT="${RUN_COMBINED_REPORT:-1}"
SORT_BY="${SORT_BY:-MRR}"
DRY_RUN="${DRY_RUN:-0}"

export DATA_ROOT="${DATA_ROOT:-$ROOT_DIR/data/rcabench-platform-v2}"
export OUTPUT_ROOT="${OUTPUT_ROOT:-$ROOT_DIR/output/rcabench-platform-v2}"
export TEMP_ROOT="${TEMP_ROOT:-$ROOT_DIR/temp}"
export LOGURU_COLORIZE="${LOGURU_COLORIZE:-0}"
export LOGURU_LEVEL="${LOGURU_LEVEL:-WARNING}"

if [[ ! -f "$DATA_ROOT/meta/$DATASET/index.parquet" || ! -f "$DATA_ROOT/meta/$DATASET/labels.parquet" ]]; then
  echo "Dataset metadata not found for '$DATASET' under $DATA_ROOT/meta/$DATASET" >&2
  echo "Build it first with:" >&2
  echo "  uv run --package evidencerank python scripts/build_aiopschallenge2025_rcabench.py --overwrite" >&2
  exit 2
fi

CLEAR_ARGS=()
if [[ "$CLEAR" != "0" ]]; then
  CLEAR_ARGS=(--clear)
fi

SAMPLE_ARGS=()
if [[ -n "$SAMPLE" ]]; then
  SAMPLE_ARGS=(--sample "$SAMPLE")
fi

FAILURES=()

run_step() {
  local name="$1"
  shift

  echo
  echo "=== $name ==="
  printf '+'
  printf ' %q' "$@"
  echo

  if [[ "$DRY_RUN" == "1" ]]; then
    echo "=== $name: dry run ==="
    return 0
  fi

  if "$@"; then
    echo "=== $name: done ==="
    return 0
  fi

  local rc=$?
  echo "=== $name: failed with exit code $rc ===" >&2
  FAILURES+=("$name:$rc")

  if [[ "$FAIL_FAST" == "1" ]]; then
    exit "$rc"
  fi

  return 0
}

run_eval_batch() {
  local name="$1"
  local package="$2"
  local main_py="$3"
  shift 3

  local cmd=(uv run --package "$package" python "$main_py" eval batch)
  local algorithm
  for algorithm in "$@"; do
    cmd+=(-a "$algorithm")
  done
  cmd+=(-d "$DATASET")
  cmd+=("${CLEAR_ARGS[@]}")
  cmd+=(--use-cpus "$CPUS")
  cmd+=("${SAMPLE_ARGS[@]}")

  run_step "$name" "${cmd[@]}"
}

echo "Dataset: $DATASET"
echo "DATA_ROOT: $DATA_ROOT"
echo "OUTPUT_ROOT: $OUTPUT_ROOT"
echo "TEMP_ROOT: $TEMP_ROOT"
echo "CPUS: $CPUS"
echo "CLEAR: $CLEAR"
echo "DRY_RUN: $DRY_RUN"
echo "Excluded: art, eadro, diagfusion, RUN"

run_eval_batch "baro" "baro" "algorithms/baro/main.py" \
  baro

run_eval_batch "nezha" "nezha" "algorithms/nezha/main.py" \
  nezha

run_eval_batch "microdig" "MicroDig" "algorithms/microdig/main.py" \
  microdig

run_eval_batch "shapleyiq family" "shapleyiq" "algorithms/shapleyiq/main.py" \
  shapleyiq \
  ton \
  microrank \
  microhecl \
  microrca

run_eval_batch "rcd" "rcaeval-rcd" "algorithms/rcd/main.py" \
  rcd

run_eval_batch "simplerca" "SimpleRCA" "algorithms/simplerca/main.py" \
  simplerca

run_eval_batch "herosas" "herosas" "algorithms/herosas/main.py" \
  herosas

if [[ "$INCLUDE_CAUSALRCA" != "0" ]]; then
  if [[ "$SYNC_CAUSALRCA" == "1" ]]; then
    run_step "sync causalrca" \
      uv sync --frozen --package rcaeval_causalrca
  fi
  run_eval_batch "causalrca" "rcaeval_causalrca" "algorithms/causalrca/main.py" \
    causalrca
else
  echo
  echo "=== causalrca: skipped because INCLUDE_CAUSALRCA=0 ==="
fi

run_eval_batch "evidencerank family" "evidencerank" "algorithms/evidencerank/main.py" \
  evidencerank \
  evidencerank_metric \
  evidencerank_log \
  evidencerank_trace \
  evidencerank_metric_log \
  evidencerank_metric_trace \
  evidencerank_log_trace \
  evidencerank_arc

run_eval_batch "cera family" "evidencerank" "algorithms/evidencerank/main.py" \
  cera \
  cera_metric \
  cera_log \
  cera_trace \
  cera_metric_log \
  cera_metric_trace \
  cera_log_trace

run_eval_batch "crest family" "evidencerank" "algorithms/evidencerank/main.py" \
  crest \
  crest_local \
  crest_nocf \
  crest_metric \
  crest_trace \
  crest_log \
  crest_metric_trace \
  crest_metric_log \
  crest_log_trace \
  crest_noresidual \
  crest_residual \
  crest_gated_residual

if [[ "$RUN_COMBINED_REPORT" != "0" ]]; then
  run_step "combined report" \
    uv run --package baro python scripts/combined_report.py "$DATASET" --sort-by "$SORT_BY"
fi

echo
if (( ${#FAILURES[@]} > 0 )); then
  echo "Completed with failures:" >&2
  printf '  %s\n' "${FAILURES[@]}" >&2
  exit 1
fi

echo "All requested algorithm groups completed successfully."
