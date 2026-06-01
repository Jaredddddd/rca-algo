#!/usr/bin/env python3
"""EvidenceRank evolution helper CLI.

The tools in this file are intentionally evaluation-side utilities. They may
read labels and injection metadata for analysis, but algorithm code must not.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
PLATFORM_OUTPUT = REPO_ROOT / "output" / "rcabench-platform-v2"
CURRENT_DATA_ROOT = PLATFORM_OUTPUT / "data"
SNAPSHOT_ROOT = PLATFORM_OUTPUT / "evolve_snapshots"
REPORT_ROOT = PLATFORM_OUTPUT / "evolve_reports"
DOC_ROOT = REPO_ROOT / "docs" / "EvidRank_evolve"
VIBE_RESEARCH_PAGE = REPO_ROOT / "VibeResearchTools" / "VibeResearch.md"
DEFAULT_LABELS = (
    REPO_ROOT / "data" / "rcabench-platform-v2" / "meta" / "rcabench-csv" / "labels.csv"
)
DEFAULT_CASE_DATA_ROOT = REPO_ROOT / "data" / "rcabench-platform-v2" / "data"
EVIDENCERANK_SRC = REPO_ROOT / "algorithms" / "evidencerank" / "src" / "evidencerank"

FAULT_PATTERNS = [
    "request-replace-method",
    "request-replace-path",
    "request-replace-body",
    "response-replace-body",
    "response-replace-code",
    "container-kill",
    "pod-failure",
    "request-abort",
    "request-delay",
    "response-abort",
    "response-delay",
    "partition",
    "corrupt",
    "exception",
    "bandwidth",
    "stress",
    "delay",
    "loss",
    "return",
]

SERVICE_COLUMNS = (
    "service_name",
    "service",
    "instance",
    "attr.k8s.container.name",
    "attr.k8s.deployment.name",
    "attr.k8s.statefulset.name",
    "attr.k8s.pod.name",
    "parent_service",
)


@dataclass(frozen=True)
class Metrics:
    total: int
    missing_outputs: int
    ac1: float
    ac3: float
    ac5: float
    mrr: float
    avg_rank: float | None
    top5_miss: int


def _repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")


def _write_text_once(path: Path, text: str) -> None:
    if path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_csv_once(path: Path, df: pd.DataFrame) -> None:
    if path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _relative_to_repo(path: Path) -> Path:
    try:
        return path.relative_to(REPO_ROOT)
    except ValueError:
        return path


def _link_from_vibe_page(path: Path) -> str:
    rel = _relative_to_repo(path)
    target = Path("..") / rel
    return f"[{rel.as_posix()}]({target.as_posix()})"


def _mtime(path: Path) -> str:
    return (
        datetime.fromtimestamp(path.stat().st_mtime)
        .astimezone()
        .isoformat(timespec="seconds")
    )


def _doc_type(path: Path) -> str:
    name = path.name
    if name == "README.md":
        return "guide"
    if name.endswith("_iteration.md"):
        return "iteration"
    if name.endswith("_summary.md"):
        return "summary"
    if name.startswith("compare_"):
        return "compare"
    return "note"


def _initial_vibe_research_page() -> str:
    return """# Vibe Research

This is the main page for EvidenceRank vibe research. Keep long-lived research context, launch prompts, decisions, and links here. Detailed iteration notes can stay in `docs/EvidRank_evolve/`.

## LLM Launch Prompt

Use the prompt in `AGENTS.md` as the source of truth for analysis agents. Keep this page as the lightweight operating dashboard and document index.

<!-- VIBE-INDEX:START -->
<!-- VIBE-INDEX:END -->
"""


def _render_vibe_index() -> str:
    docs = sorted(DOC_ROOT.glob("*.md")) if DOC_ROOT.exists() else []
    snapshots = sorted(SNAPSHOT_ROOT.glob("*")) if SNAPSHOT_ROOT.exists() else []
    reports = sorted(REPORT_ROOT.glob("*")) if REPORT_ROOT.exists() else []

    lines = [
        "<!-- VIBE-INDEX:START -->",
        f"_Last refreshed: {_now()}_",
        "",
        "## EvidenceRank Document Index",
        "",
    ]
    if docs:
        lines += [
            "| type | document | updated |",
            "| --- | --- | --- |",
        ]
        for doc in docs:
            lines.append(
                f"| {_doc_type(doc)} | {_link_from_vibe_page(doc)} | {_mtime(doc)} |"
            )
    else:
        lines.append("No `docs/EvidRank_evolve/*.md` documents found yet.")

    lines += [
        "",
        "## Versioned Artifacts",
        "",
        "| kind | path |",
        "| --- | --- |",
    ]
    artifact_count = 0
    for snapshot in snapshots:
        if snapshot.is_dir():
            lines.append(f"| snapshot | `{_relative_to_repo(snapshot).as_posix()}` |")
            artifact_count += 1
    for report in reports:
        if report.is_dir():
            lines.append(f"| report | `{_relative_to_repo(report).as_posix()}` |")
            artifact_count += 1
    if artifact_count == 0:
        lines.append("| none | No snapshots or reports generated yet. |")

    lines += [
        "",
        "<!-- VIBE-INDEX:END -->",
    ]
    return "\n".join(lines)


def _refresh_vibe_research_index() -> None:
    VIBE_RESEARCH_PAGE.parent.mkdir(parents=True, exist_ok=True)
    if VIBE_RESEARCH_PAGE.exists():
        text = VIBE_RESEARCH_PAGE.read_text(encoding="utf-8")
    else:
        text = _initial_vibe_research_page()

    start = "<!-- VIBE-INDEX:START -->"
    end = "<!-- VIBE-INDEX:END -->"
    index = _render_vibe_index()
    if start in text and end in text:
        before = text.split(start, 1)[0].rstrip()
        after = text.split(end, 1)[1].lstrip()
        text = f"{before}\n\n{index}\n"
        if after:
            text += f"\n{after}"
    else:
        text = f"{text.rstrip()}\n\n{index}\n"
    VIBE_RESEARCH_PAGE.write_text(text, encoding="utf-8")


def _run_git(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return ""
    return completed.stdout.strip()


def _load_labels(labels_path: Path, dataset: str) -> dict[str, set[str]]:
    if not labels_path.exists():
        raise SystemExit(f"Label file not found: {labels_path}")
    labels = pd.read_csv(labels_path)
    required = {"dataset", "datapack", "gt.level", "gt.name"}
    missing = required - set(labels.columns)
    if missing:
        raise SystemExit(f"Label file is missing columns: {sorted(missing)}")
    labels = labels[(labels["dataset"] == dataset) & (labels["gt.level"] == "service")]
    result: dict[str, set[str]] = {}
    for datapack, group in labels.groupby("datapack"):
        result[str(datapack)] = {str(name) for name in group["gt.name"].dropna()}
    return result


def _resolve_data_root(source: str) -> Path:
    if source == "current":
        return CURRENT_DATA_ROOT
    snapshot_data = SNAPSHOT_ROOT / source / "data"
    if snapshot_data.exists():
        return snapshot_data
    path = _repo_path(source)
    if (path / "data").exists():
        return path / "data"
    return path


def _prediction_file(
    data_root: Path, dataset: str, datapack: str, algorithm: str
) -> Path:
    return data_root / dataset / datapack / algorithm / "output.parquet"


def _prediction_files(data_root: Path, dataset: str, algorithm: str) -> list[Path]:
    dataset_root = data_root / dataset
    if not dataset_root.exists():
        return []
    return sorted(dataset_root.glob(f"*/{algorithm}/output.parquet"))


def _parse_datapack(datapack: str) -> dict[str, str]:
    parts = datapack.split("-")
    time_bucket = parts[0] if parts else ""
    rest = parts[1:]
    for fault in FAULT_PATTERNS:
        tokens = fault.split("-")
        for idx in range(0, max(len(rest) - len(tokens) + 1, 0)):
            if rest[idx : idx + len(tokens)] == tokens:
                suffix = "-".join(rest[idx + len(tokens) :])
                return {
                    "time_bucket": time_bucket,
                    "case_service": "-".join(rest[:idx]) or "unknown",
                    "fault_type": fault,
                    "case_suffix": suffix,
                }
    return {
        "time_bucket": time_bucket,
        "case_service": "unknown",
        "fault_type": "unknown",
        "case_suffix": "",
    }


def _read_prediction_rows(
    data_root: Path,
    dataset: str,
    algorithm: str,
    labels: dict[str, set[str]],
    top_k: int = 10,
) -> pd.DataFrame:
    files = _prediction_files(data_root, dataset, algorithm)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    for path in files:
        datapack = path.parents[1].name
        seen.add(datapack)
        gt = labels.get(datapack, set())
        parsed = _parse_datapack(datapack)
        row: dict[str, Any] = {
            "dataset": dataset,
            "datapack": datapack,
            "algorithm": algorithm,
            "gt": ";".join(sorted(gt)),
            "gt_count": len(gt),
            **parsed,
        }
        try:
            pred = pd.read_parquet(path)
        except Exception as exc:  # noqa: BLE001 - report bad output files.
            row.update(
                {
                    "missing_output": False,
                    "read_error": repr(exc),
                    "best_rank": pd.NA,
                    "mrr": 0.0,
                    "hit@1": False,
                    "hit@3": False,
                    "hit@5": False,
                    "top1": "",
                    "top3": "",
                    "top5": "",
                    "top10": "",
                    "runtime.seconds": pd.NA,
                }
            )
            rows.append(row)
            continue

        if "level" in pred.columns:
            pred = pred[pred["level"] == "service"]
        if "rank" in pred.columns:
            pred = pred.sort_values("rank", kind="stable")
        names = [
            str(name)
            for name in pred.get("name", pd.Series(dtype=object)).dropna().tolist()
        ]
        ranks: list[int] = []
        if gt and {"name", "rank"}.issubset(pred.columns):
            for _, item in pred.iterrows():
                if str(item["name"]) in gt:
                    ranks.append(int(item["rank"]))
        best_rank = min(ranks) if ranks else None
        runtime = None
        if "runtime.seconds" in pred.columns and not pred.empty:
            runtime = float(pred["runtime.seconds"].iloc[0])
        row.update(
            {
                "missing_output": False,
                "read_error": "",
                "best_rank": best_rank if best_rank is not None else pd.NA,
                "mrr": (1.0 / best_rank) if best_rank else 0.0,
                "hit@1": bool(best_rank == 1),
                "hit@3": bool(best_rank is not None and best_rank <= 3),
                "hit@5": bool(best_rank is not None and best_rank <= 5),
                "top1": names[0] if names else "",
                "top3": "|".join(names[:3]),
                "top5": "|".join(names[:5]),
                f"top{top_k}": "|".join(names[:top_k]),
                "runtime.seconds": runtime if runtime is not None else pd.NA,
            }
        )
        rows.append(row)

    for datapack, gt in labels.items():
        if datapack in seen:
            continue
        parsed = _parse_datapack(datapack)
        rows.append(
            {
                "dataset": dataset,
                "datapack": datapack,
                "algorithm": algorithm,
                "gt": ";".join(sorted(gt)),
                "gt_count": len(gt),
                **parsed,
                "missing_output": True,
                "read_error": "",
                "best_rank": pd.NA,
                "mrr": 0.0,
                "hit@1": False,
                "hit@3": False,
                "hit@5": False,
                "top1": "",
                "top3": "",
                "top5": "",
                f"top{top_k}": "",
                "runtime.seconds": pd.NA,
            }
        )

    if not rows:
        return pd.DataFrame()
    return (
        pd.DataFrame(rows).sort_values("datapack", kind="stable").reset_index(drop=True)
    )


def _metrics(cases: pd.DataFrame) -> Metrics:
    if cases.empty:
        return Metrics(0, 0, 0.0, 0.0, 0.0, 0.0, None, 0)
    total = len(cases)
    ranks = pd.to_numeric(cases["best_rank"], errors="coerce")
    return Metrics(
        total=total,
        missing_outputs=int(cases["missing_output"].fillna(False).sum()),
        ac1=float(cases["hit@1"].mean()),
        ac3=float(cases["hit@3"].mean()),
        ac5=float(cases["hit@5"].mean()),
        mrr=float(cases["mrr"].mean()),
        avg_rank=float(ranks.dropna().mean()) if ranks.notna().any() else None,
        top5_miss=int((~cases["hit@5"]).sum()),
    )


def _fmt(value: float | None) -> str:
    if value is None:
        return "NA"
    return f"{value:.6f}"


def _group_summary(cases: pd.DataFrame) -> pd.DataFrame:
    if cases.empty:
        return pd.DataFrame()
    frames: list[pd.DataFrame] = []
    for column in ("fault_type", "case_service", "time_bucket"):
        grouped = (
            cases.groupby(column, dropna=False)
            .agg(
                cases=("datapack", "count"),
                ac1=("hit@1", "mean"),
                ac3=("hit@3", "mean"),
                ac5=("hit@5", "mean"),
                mrr=("mrr", "mean"),
                top5_miss=("hit@5", lambda s: int((~s).sum())),
            )
            .reset_index()
            .rename(columns={column: "group"})
        )
        grouped.insert(0, "group_type", column)
        frames.append(grouped)
    return pd.concat(frames, ignore_index=True).sort_values(
        ["group_type", "ac1", "cases"], ascending=[True, True, False], kind="stable"
    )


def _markdown_summary(
    version: str, source: str, cases: pd.DataFrame, groups: pd.DataFrame
) -> str:
    metrics = _metrics(cases)
    false_cases = cases[~cases["hit@1"]].copy()
    top5_miss = cases[~cases["hit@5"]].copy()
    hard = false_cases.copy()
    hard["_rank_for_sort"] = pd.to_numeric(hard["best_rank"], errors="coerce").fillna(
        10**9
    )
    hard = hard.sort_values(
        ["_rank_for_sort", "datapack"], ascending=[False, True]
    ).head(30)

    lines = [
        f"# EvidenceRank {version} Summary",
        "",
        f"- Created: {_now()}",
        f"- Source: `{source}`",
        "- Algorithm: `evidencerank`",
        "- Dataset: `rcabench`",
        "",
        "## Metrics",
        "",
        "| metric | value |",
        "| --- | ---: |",
        f"| total | {metrics.total} |",
        f"| missing_outputs | {metrics.missing_outputs} |",
        f"| AC@1 | {_fmt(metrics.ac1)} |",
        f"| AC@3 | {_fmt(metrics.ac3)} |",
        f"| AC@5 | {_fmt(metrics.ac5)} |",
        f"| MRR | {_fmt(metrics.mrr)} |",
        f"| avg_rank | {_fmt(metrics.avg_rank)} |",
        f"| top1_miss | {len(false_cases)} |",
        f"| top5_miss | {len(top5_miss)} |",
        "",
        "## Weak Groups",
        "",
    ]
    weak_groups = groups.sort_values(["ac1", "cases"], ascending=[True, False]).head(20)
    if weak_groups.empty:
        lines.append("No group summary available.")
    else:
        lines += [
            "| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for item in weak_groups.to_dict("records"):
            lines.append(
                "| {group_type} | {group} | {cases} | {ac1:.6f} | {ac3:.6f} | "
                "{ac5:.6f} | {mrr:.6f} | {top5_miss} |".format(**item)
            )

    lines += [
        "",
        "## Hard False Cases",
        "",
    ]
    if hard.empty:
        lines.append("No Top-1 false cases.")
    else:
        lines += [
            "| datapack | gt | best_rank | top5 | fault_type | case_service |",
            "| --- | --- | ---: | --- | --- | --- |",
        ]
        for item in hard.to_dict("records"):
            lines.append(
                f"| {item['datapack']} | {item['gt']} | {item['best_rank']} | "
                f"{item['top5']} | {item['fault_type']} | {item['case_service']} |"
            )

    lines += [
        "",
        "## Research Notes",
        "",
        "- Write the suspected general failure mechanism here.",
        "- Do not add case/service/fault hardcoding to the algorithm.",
        "- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.",
        "",
    ]
    return "\n".join(lines)


def _read_combined_metrics(dataset: str, algorithm: str) -> dict[str, Any]:
    path = PLATFORM_OUTPUT / "meta" / dataset / "dataset.perf.combined.parquet"
    if not path.exists():
        return {}
    df = pd.read_parquet(path)
    if "algorithm" not in df.columns:
        return {}
    row = df[df["algorithm"] == algorithm]
    if row.empty:
        return {}
    result: dict[str, Any] = {}
    for key, value in row.iloc[0].to_dict().items():
        if pd.isna(value):
            result[key] = None
        elif hasattr(value, "item"):
            result[key] = value.item()
        else:
            result[key] = value
    return result


def cmd_snapshot(args: argparse.Namespace) -> None:
    version = _safe_name(args.version)
    destination = SNAPSHOT_ROOT / version
    if destination.exists():
        raise SystemExit(
            f"Snapshot already exists, choose a new version: {destination}"
        )

    source_dataset_root = CURRENT_DATA_ROOT / args.dataset
    if not source_dataset_root.exists():
        raise SystemExit(
            f"Current output dataset root not found: {source_dataset_root}"
        )

    algorithm_dirs = sorted(source_dataset_root.glob(f"*/{args.algorithm}"))
    if not algorithm_dirs:
        raise SystemExit(
            f"No current outputs found for algorithm={args.algorithm} dataset={args.dataset}"
        )

    copied = 0
    for src in algorithm_dirs:
        datapack = src.parent.name
        dst = destination / "data" / args.dataset / datapack / args.algorithm
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)
        copied += 1

    manifest = {
        "version": version,
        "created_at": _now(),
        "algorithm": args.algorithm,
        "dataset": args.dataset,
        "source": str(CURRENT_DATA_ROOT.relative_to(REPO_ROOT)),
        "copied_datapacks": copied,
        "git_head": _run_git(["rev-parse", "HEAD"]),
        "git_status_short": _run_git(["status", "--short"]),
        "combined_metrics": _read_combined_metrics(args.dataset, args.algorithm),
        "notes": args.notes or "",
    }
    manifest_path = destination / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Snapshot saved: {destination.relative_to(REPO_ROOT)} ({copied} datapacks)")


def cmd_summarize(args: argparse.Namespace) -> None:
    source = args.source
    version = _safe_name(args.version or source)
    data_root = _resolve_data_root(source)
    labels = _load_labels(_repo_path(args.labels), args.dataset)
    cases = _read_prediction_rows(
        data_root, args.dataset, args.algorithm, labels, top_k=args.top_k
    )
    if cases.empty:
        raise SystemExit(
            f"No predictions found under {data_root} for {args.dataset}/{args.algorithm}"
        )

    report_dir = REPORT_ROOT / version
    all_cases_path = report_dir / "all_cases.csv"
    false_cases_path = report_dir / "false_cases.csv"
    group_path = report_dir / "group_summary.csv"
    doc_path = DOC_ROOT / f"{version}_summary.md"
    for path in (all_cases_path, false_cases_path, group_path, doc_path):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite existing report file: {path}")

    false_cases = cases[~cases["hit@1"]].copy()
    groups = _group_summary(cases)
    _write_csv_once(all_cases_path, cases)
    _write_csv_once(false_cases_path, false_cases)
    _write_csv_once(group_path, groups)
    _write_text_once(doc_path, _markdown_summary(version, source, cases, groups))
    _refresh_vibe_research_index()
    metrics = _metrics(cases)
    print(f"Summary saved: {doc_path.relative_to(REPO_ROOT)}")
    print(
        f"AC@1={metrics.ac1:.6f} AC@3={metrics.ac3:.6f} AC@5={metrics.ac5:.6f} MRR={metrics.mrr:.6f}"
    )


def _status_for_delta(old_rank: float | None, new_rank: float | None) -> str:
    old_hit = old_rank == 1
    new_hit = new_rank == 1
    if old_hit and not new_hit:
        return "regressed_from_hit1"
    if not old_hit and new_hit:
        return "improved_to_hit1"
    if old_rank is None and new_rank is None:
        return "unchanged_missing"
    if old_rank is None:
        return "rank_improved"
    if new_rank is None:
        return "rank_regressed"
    if new_rank < old_rank:
        return "rank_improved"
    if new_rank > old_rank:
        return "rank_regressed"
    return "unchanged"


def _rank_or_none(value: Any) -> float | None:
    if pd.isna(value):
        return None
    return float(value)


def _markdown_compare(
    old: str,
    new: str,
    old_cases: pd.DataFrame,
    new_cases: pd.DataFrame,
    deltas: pd.DataFrame,
) -> str:
    old_metrics = _metrics(old_cases)
    new_metrics = _metrics(new_cases)
    status_counts = deltas["status"].value_counts().to_dict()
    important = deltas[
        deltas["status"].isin(
            [
                "regressed_from_hit1",
                "improved_to_hit1",
                "rank_regressed",
                "rank_improved",
            ]
        )
    ].copy()
    important = important.sort_values(
        ["status", "rank_delta"], ascending=[True, True]
    ).head(40)

    lines = [
        f"# EvidenceRank Compare {old} vs {new}",
        "",
        f"- Created: {_now()}",
        f"- Old: `{old}`",
        f"- New: `{new}`",
        "",
        "## Metric Delta",
        "",
        "| metric | old | new | delta |",
        "| --- | ---: | ---: | ---: |",
        f"| AC@1 | {_fmt(old_metrics.ac1)} | {_fmt(new_metrics.ac1)} | {_fmt(new_metrics.ac1 - old_metrics.ac1)} |",
        f"| AC@3 | {_fmt(old_metrics.ac3)} | {_fmt(new_metrics.ac3)} | {_fmt(new_metrics.ac3 - old_metrics.ac3)} |",
        f"| AC@5 | {_fmt(old_metrics.ac5)} | {_fmt(new_metrics.ac5)} | {_fmt(new_metrics.ac5 - old_metrics.ac5)} |",
        f"| MRR | {_fmt(old_metrics.mrr)} | {_fmt(new_metrics.mrr)} | {_fmt(new_metrics.mrr - old_metrics.mrr)} |",
        "",
        "## Status Counts",
        "",
        "| status | cases |",
        "| --- | ---: |",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")

    lines += [
        "",
        "## Important Case Deltas",
        "",
    ]
    if important.empty:
        lines.append("No important case deltas.")
    else:
        lines += [
            "| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |",
            "| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |",
        ]
        for item in important.to_dict("records"):
            lines.append(
                f"| {item['datapack']} | {item['status']} | {item['old_best_rank']} | "
                f"{item['new_best_rank']} | {item['rank_delta']} | {item['gt']} | "
                f"{item['new_top5']} | {item['fault_type']} | {item['case_service']} |"
            )

    lines += [
        "",
        "## Decision Notes",
        "",
        "- Explain whether the new version should be accepted.",
        "- Pay special attention to `regressed_from_hit1` cases.",
        "- If accepted, record the general mechanism that improved the ranking.",
        "",
    ]
    return "\n".join(lines)


def cmd_compare(args: argparse.Namespace) -> None:
    labels = _load_labels(_repo_path(args.labels), args.dataset)
    old_cases = _read_prediction_rows(
        _resolve_data_root(args.old),
        args.dataset,
        args.algorithm,
        labels,
        top_k=args.top_k,
    )
    new_cases = _read_prediction_rows(
        _resolve_data_root(args.new),
        args.dataset,
        args.algorithm,
        labels,
        top_k=args.top_k,
    )
    if old_cases.empty or new_cases.empty:
        raise SystemExit("Both old and new sources must contain predictions.")

    old_cols = [
        "datapack",
        "best_rank",
        "mrr",
        "hit@1",
        "hit@3",
        "hit@5",
        "top5",
    ]
    new_cols = [
        "datapack",
        "gt",
        "time_bucket",
        "case_service",
        "fault_type",
        "best_rank",
        "mrr",
        "hit@1",
        "hit@3",
        "hit@5",
        "top5",
    ]
    deltas = old_cases[old_cols].merge(
        new_cases[new_cols], on="datapack", suffixes=("_old", "_new")
    )
    deltas = deltas.rename(
        columns={
            "best_rank_old": "old_best_rank",
            "best_rank_new": "new_best_rank",
            "mrr_old": "old_mrr",
            "mrr_new": "new_mrr",
            "top5_old": "old_top5",
            "top5_new": "new_top5",
        }
    )
    old_ranks = deltas["old_best_rank"].map(_rank_or_none)
    new_ranks = deltas["new_best_rank"].map(_rank_or_none)
    deltas["rank_delta"] = [
        (old if old is not None else 10**9) - (new if new is not None else 10**9)
        for old, new in zip(old_ranks, new_ranks, strict=True)
    ]
    deltas["mrr_delta"] = deltas["new_mrr"] - deltas["old_mrr"]
    deltas["status"] = [
        _status_for_delta(old, new)
        for old, new in zip(old_ranks, new_ranks, strict=True)
    ]
    deltas = deltas.sort_values(
        ["status", "rank_delta", "datapack"], ascending=[True, True, True]
    )

    compare_name = _safe_name(args.version or f"compare_{args.old}_vs_{args.new}")
    report_dir = REPORT_ROOT / compare_name
    csv_path = report_dir / "case_deltas.csv"
    doc_path = DOC_ROOT / f"{compare_name}.md"
    _write_csv_once(csv_path, deltas)
    _write_text_once(
        doc_path, _markdown_compare(args.old, args.new, old_cases, new_cases, deltas)
    )
    _refresh_vibe_research_index()
    print(f"Compare saved: {doc_path.relative_to(REPO_ROOT)}")


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _service_counts(df: pd.DataFrame) -> str:
    for column in SERVICE_COLUMNS:
        if column in df.columns:
            counts = df[column].dropna().astype(str).value_counts().head(10)
            if not counts.empty:
                return ", ".join(f"{name}:{count}" for name, count in counts.items())
    return ""


def _input_file_summary(case_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(case_dir.glob("*.parquet")):
        if path.name == "conclusion.parquet":
            continue
        try:
            df = pd.read_parquet(path)
        except Exception as exc:  # noqa: BLE001 - report bad input files.
            rows.append(
                {
                    "file": path.name,
                    "rows": "ERR",
                    "columns": repr(exc),
                    "top_services": "",
                }
            )
            continue
        rows.append(
            {
                "file": path.name,
                "rows": len(df),
                "columns": ", ".join(map(str, df.columns[:20])),
                "top_services": _service_counts(df),
            }
        )
    return rows


def _markdown_case(args: argparse.Namespace) -> str:
    labels = _load_labels(_repo_path(args.labels), args.dataset)
    gt = labels.get(args.datapack, set())
    data_root = _resolve_data_root(args.source)
    pred_path = _prediction_file(data_root, args.dataset, args.datapack, args.algorithm)
    case_dir = _repo_path(args.case_data_root) / args.dataset / args.datapack
    injection_path = case_dir / "injection.json"

    lines = [
        f"# Case {args.datapack}",
        "",
        f"- Created: {_now()}",
        f"- Source: `{args.source}`",
        f"- Algorithm: `{args.algorithm}`",
        f"- Dataset: `{args.dataset}`",
        f"- GT: `{';'.join(sorted(gt))}`",
        "",
        "## Prediction",
        "",
    ]
    if pred_path.exists():
        pred = pd.read_parquet(pred_path)
        if "level" in pred.columns:
            pred = pred[pred["level"] == "service"]
        if "rank" in pred.columns:
            pred = pred.sort_values("rank", kind="stable")
        lines += [
            "| rank | name | hit |",
            "| ---: | --- | --- |",
        ]
        for item in pred.head(args.top_k).to_dict("records"):
            lines.append(
                f"| {item.get('rank', '')} | {item.get('name', '')} | {item.get('hit', '')} |"
            )
    else:
        lines.append(f"Prediction not found: `{pred_path}`")

    lines += [
        "",
        "## Injection",
        "",
    ]
    if injection_path.exists():
        injection = _read_json(injection_path)
        lines.append("```json")
        lines.append(json.dumps(injection, ensure_ascii=False, indent=2)[:8000])
        lines.append("```")
    else:
        lines.append(f"Injection file not found: `{injection_path}`")

    lines += [
        "",
        "## Input Files",
        "",
    ]
    summaries = _input_file_summary(case_dir) if case_dir.exists() else []
    if summaries:
        lines += [
            "| file | rows | top_services | columns |",
            "| --- | ---: | --- | --- |",
        ]
        for item in summaries:
            lines.append(
                f"| {item['file']} | {item['rows']} | {item['top_services']} | {item['columns']} |"
            )
    else:
        lines.append(
            f"Input case directory not found or has no parquet files: `{case_dir}`"
        )

    lines += [
        "",
        "## Analysis Notes",
        "",
        "- Describe why current scoring ranks the GT here.",
        "- Convert observations into a general algorithm idea before editing code.",
        "",
    ]
    return "\n".join(lines)


def cmd_case(args: argparse.Namespace) -> None:
    text = _markdown_case(args)
    if args.out:
        out = _repo_path(args.out)
        _write_text_once(out, text)
        if out.suffix == ".md":
            _refresh_vibe_research_index()
        print(f"Case report saved: {out.relative_to(REPO_ROOT)}")
    else:
        print(text)


def cmd_guard(args: argparse.Namespace) -> None:
    source_root = _repo_path(args.source_root)
    patterns = [
        (
            "HIGH",
            re.compile(r"\bts\d+-[a-z0-9-]+-[a-z0-9]{5,}\b"),
            "datapack id literal",
        ),
        (
            "HIGH",
            re.compile(
                r"labels\.csv|injection\.json|conclusion\.parquet|ground[_ -]?truth|gt\.name",
                re.I,
            ),
            "label leakage",
        ),
        (
            "HIGH",
            re.compile(
                r"['\"](?:mysql|rabbitmq|loadgenerator|ts-[a-z0-9-]+-service|ts-ui-dashboard)['\"]"
            ),
            "service name literal",
        ),
        ("MEDIUM", re.compile(r"rcabench", re.I), "dataset name literal"),
    ]
    warnings: list[tuple[str, Path, int, str, str]] = []
    for path in sorted(source_root.rglob("*.py")):
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for severity, pattern, message in patterns:
                if pattern.search(line):
                    warnings.append((severity, path, lineno, message, line.strip()))

    high_count = sum(1 for item in warnings if item[0] == "HIGH")
    if warnings:
        for severity, path, lineno, message, line in warnings:
            rel = path.relative_to(REPO_ROOT)
            print(f"{severity}: {rel}:{lineno}: {message}: {line}")
    else:
        print("No overfitting guard warnings.")

    if high_count:
        raise SystemExit(f"Found {high_count} high-risk overfitting warning(s).")
    print("No high-risk overfitting warnings.")


def cmd_new_note(args: argparse.Namespace) -> None:
    version = _safe_name(args.version)
    path = DOC_ROOT / f"{version}_iteration.md"
    text = f"""# EvidenceRank {version} Iteration

- Created: {_now()}
- Hypothesis: {args.hypothesis}
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Scope

- Files planned for change:
- General RCA mechanism being tested:
- Why this should transfer beyond RCABench:

## Baseline

- Baseline snapshot:
- Baseline summary:
- Key weak groups:
- Representative false cases:

## Planned Change

- Minimal algorithm change:
- Expected metric movement:
- Known regression risk:

## Commands

```bash
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch -a evidencerank -d rcabench --clear --use-cpus 32
uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
```

## Results

- New snapshot:
- New summary:
- Compare report:
- AC@1:
- AC@3:
- AC@5:
- MRR:

## Case Deltas

- Improved:
- Regressed:

## Decision

- Accept / reject / keep for later:
- Reason:
- Next smallest general step:
"""
    _write_text_once(path, text)
    _refresh_vibe_research_index()
    print(f"Iteration note saved: {path.relative_to(REPO_ROOT)}")


def cmd_index(args: argparse.Namespace) -> None:
    _refresh_vibe_research_index()
    print(f"VibeResearch index refreshed: {VIBE_RESEARCH_PAGE.relative_to(REPO_ROOT)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="EvidenceRank evolution research tools"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser(
        "snapshot", help="Copy current algorithm outputs into a versioned snapshot"
    )
    snapshot.add_argument(
        "--version", required=True, help="Unique version name, for example V1"
    )
    snapshot.add_argument("--algorithm", default="evidencerank")
    snapshot.add_argument("--dataset", default="rcabench")
    snapshot.add_argument("--notes", default="")
    snapshot.set_defaults(func=cmd_snapshot)

    summarize = subparsers.add_parser(
        "summarize", help="Create false-case summary for current output or a snapshot"
    )
    summarize.add_argument(
        "--version", help="Report version name; defaults to --source"
    )
    summarize.add_argument(
        "--source", default="current", help="current, snapshot version, or path"
    )
    summarize.add_argument("--algorithm", default="evidencerank")
    summarize.add_argument("--dataset", default="rcabench")
    summarize.add_argument(
        "--labels", default=str(DEFAULT_LABELS.relative_to(REPO_ROOT))
    )
    summarize.add_argument("--top-k", type=int, default=10)
    summarize.set_defaults(func=cmd_summarize)

    compare = subparsers.add_parser("compare", help="Compare two output sources")
    compare.add_argument(
        "--old", required=True, help="Old snapshot/source, for example V1"
    )
    compare.add_argument(
        "--new", required=True, help="New snapshot/source, for example V2 or current"
    )
    compare.add_argument("--version", help="Report version name")
    compare.add_argument("--algorithm", default="evidencerank")
    compare.add_argument("--dataset", default="rcabench")
    compare.add_argument("--labels", default=str(DEFAULT_LABELS.relative_to(REPO_ROOT)))
    compare.add_argument("--top-k", type=int, default=10)
    compare.set_defaults(func=cmd_compare)

    case = subparsers.add_parser("case", help="Inspect one datapack")
    case.add_argument("--datapack", required=True)
    case.add_argument("--source", default="current")
    case.add_argument("--algorithm", default="evidencerank")
    case.add_argument("--dataset", default="rcabench")
    case.add_argument("--labels", default=str(DEFAULT_LABELS.relative_to(REPO_ROOT)))
    case.add_argument(
        "--case-data-root", default=str(DEFAULT_CASE_DATA_ROOT.relative_to(REPO_ROOT))
    )
    case.add_argument("--top-k", type=int, default=20)
    case.add_argument("--out", help="Optional markdown output path")
    case.set_defaults(func=cmd_case)

    guard = subparsers.add_parser(
        "guard", help="Scan EvidenceRank source for obvious overfitting signals"
    )
    guard.add_argument(
        "--source-root", default=str(EVIDENCERANK_SRC.relative_to(REPO_ROOT))
    )
    guard.set_defaults(func=cmd_guard)

    note = subparsers.add_parser("new-note", help="Create an iteration note template")
    note.add_argument("--version", required=True)
    note.add_argument("--hypothesis", required=True)
    note.set_defaults(func=cmd_new_note)

    index = subparsers.add_parser(
        "index", help="Refresh VibeResearchTools/VibeResearch.md document index"
    )
    index.set_defaults(func=cmd_index)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
