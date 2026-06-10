"""Aggregate CREST-Residual experiment results.

Run from the repository root:

    uv run --package evidencerank python analysis/crest_residual/analyze_residual_results.py
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_ALGORITHMS = (
    "crest_residual",
    "crest",
    "crest_local",
    "crest_nocf",
    "crest_metric_trace",
    "crest_trace",
    "cera",
)

PAIRED_BASELINES = (
    "crest",
    "crest_local",
    "crest_nocf",
    "crest_metric_trace",
)

ETA_VALUES = (0.25, 0.5, 1.0, 2.0)


@dataclass(frozen=True)
class CaseMetrics:
    datapack: str
    min_rank: float
    mrr: float
    ac1: float
    ac3: float
    ac5: float
    top1: str | None


def _load_ground_truth(labels_path: Path, dataset: str) -> dict[str, set[str]]:
    labels = pd.read_csv(labels_path)
    labels = labels[(labels["dataset"] == dataset) & (labels["gt.level"] == "service")]
    truth: dict[str, set[str]] = {}
    for datapack, group in labels.groupby("datapack"):
        truth[str(datapack)] = {str(name) for name in group["gt.name"].dropna()}
    return truth


def _read_algorithm_outputs(output_root: Path, dataset: str, algorithm: str) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted((output_root / dataset).glob(f"*/{algorithm}/output.parquet")):
        try:
            frames.append(pd.read_parquet(path))
        except Exception as exc:  # pragma: no cover - defensive reporting path.
            print(f"skip unreadable output {path}: {exc}")
    if not frames:
        return pd.DataFrame(
            columns=["dataset", "datapack", "algorithm", "level", "name", "rank", "hit"]
        )
    return pd.concat(frames, ignore_index=True)


def _read_algorithm_perf(output_root: Path, dataset: str, algorithm: str) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted((output_root / dataset).glob(f"*/{algorithm}/perf.parquet")):
        try:
            frames.append(pd.read_parquet(path))
        except Exception as exc:  # pragma: no cover - defensive reporting path.
            print(f"skip unreadable perf {path}: {exc}")
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _case_metrics(output: pd.DataFrame, truth: dict[str, set[str]]) -> pd.DataFrame:
    rows: list[CaseMetrics] = []
    for datapack, group in output.groupby("datapack"):
        group = group.sort_values("rank", kind="stable")
        gt_names = truth.get(str(datapack), set())
        hit_ranks = [
            float(rank)
            for name, rank in group[["name", "rank"]].itertuples(index=False, name=None)
            if str(name) in gt_names
        ]
        min_rank = min(hit_ranks) if hit_ranks else np.inf
        top1 = str(group.iloc[0]["name"]) if not group.empty else None
        rows.append(
            CaseMetrics(
                datapack=str(datapack),
                min_rank=min_rank,
                mrr=0.0 if not np.isfinite(min_rank) else 1.0 / min_rank,
                ac1=float(min_rank <= 1),
                ac3=float(min_rank <= 3),
                ac5=float(min_rank <= 5),
                top1=top1,
            )
        )
    return pd.DataFrame([row.__dict__ for row in rows])


def _summary_row(
    dataset: str,
    algorithm: str,
    cases: pd.DataFrame,
    perf: pd.DataFrame,
) -> dict[str, float | int | str]:
    runtime = (
        perf["runtime.seconds:avg"].astype(float)
        if "runtime.seconds:avg" in perf.columns and not perf.empty
        else pd.Series(dtype=float)
    )
    error = int(perf["error"].sum()) if "error" in perf.columns and not perf.empty else 0
    return {
        "dataset": dataset,
        "algorithm": algorithm,
        "total": int(len(cases)),
        "error": error,
        "runtime_mean": float(runtime.mean()) if not runtime.empty else np.nan,
        "runtime_median": float(runtime.median()) if not runtime.empty else np.nan,
        "runtime_p95": float(runtime.quantile(0.95)) if not runtime.empty else np.nan,
        "MRR": float(cases["mrr"].mean()) if not cases.empty else np.nan,
        "AC@1": float(cases["ac1"].mean()) if not cases.empty else np.nan,
        "AC@3": float(cases["ac3"].mean()) if not cases.empty else np.nan,
        "AC@5": float(cases["ac5"].mean()) if not cases.empty else np.nan,
    }


def _bootstrap_delta(
    residual: pd.DataFrame,
    baseline: pd.DataFrame,
    baseline_name: str,
    seed: int,
    iterations: int,
) -> list[dict[str, float | str | int]]:
    paired = residual.merge(
        baseline,
        on="datapack",
        suffixes=("_residual", "_baseline"),
    )
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | str | int]] = []
    for metric in ("mrr", "ac1", "ac3", "ac5"):
        delta = (
            paired[f"{metric}_residual"].to_numpy(dtype=np.float64)
            - paired[f"{metric}_baseline"].to_numpy(dtype=np.float64)
        )
        observed = float(np.mean(delta)) if delta.size else np.nan
        if delta.size:
            samples = rng.choice(delta, size=(iterations, delta.size), replace=True).mean(axis=1)
            ci_low, ci_high = np.quantile(samples, [0.025, 0.975])
            prob_gt0 = float(np.mean(samples > 0.0))
        else:
            ci_low = ci_high = prob_gt0 = np.nan
        rows.append(
            {
                "comparison": f"crest_residual_vs_{baseline_name}",
                "metric": metric.upper().replace("AC", "AC@"),
                "paired_cases": int(delta.size),
                "delta": observed,
                "bootstrap_ci_low": float(ci_low),
                "bootstrap_ci_high": float(ci_high),
                "prob_delta_gt_0": prob_gt0,
                "bootstrap_iterations": iterations,
                "seed": seed,
            }
        )
    return rows


def _format_markdown_value(value: object, floatfmt: str) -> str:
    if isinstance(value, (float, np.floating)):
        if not np.isfinite(float(value)):
            return ""
        return format(float(value), floatfmt)
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    return str(value)


def _markdown_table(frame: pd.DataFrame, floatfmt: str = ".6f") -> str:
    if frame.empty:
        return "_No rows._"
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        values = [_format_markdown_value(value, floatfmt) for value in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def _topk(output: pd.DataFrame, datapack: str, algorithm: str, k: int = 5) -> str:
    rows = output[
        (output["datapack"] == datapack) & (output["algorithm"] == algorithm)
    ].sort_values("rank", kind="stable")
    return ", ".join(
        f"{int(row.rank)}:{row.name}" for row in rows.head(k).itertuples(index=False)
    )


def _load_residual_diagnostics(output_root: Path, dataset: str) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted(
        (output_root / dataset).glob("*/crest_residual/crest_residual_diagnostics.parquet")
    ):
        frames.append(pd.read_parquet(path))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def _case_studies(
    outputs: dict[str, pd.DataFrame],
    cases: dict[str, pd.DataFrame],
    truth: dict[str, set[str]],
    diagnostics: pd.DataFrame,
    output_path: Path,
) -> None:
    residual = cases["crest_residual"]
    crest = cases["crest"]
    local = cases["crest_local"]
    nocf = cases["crest_nocf"]
    paired = residual.merge(crest, on="datapack", suffixes=("_residual", "_crest"))
    wins = paired[(paired["ac1_residual"] == 1.0) & (paired["ac1_crest"] == 0.0)]
    losses = paired[(paired["ac1_residual"] == 0.0) & (paired["ac1_crest"] == 1.0)]

    cf_pool = residual.merge(crest, on="datapack", suffixes=("_residual", "_crest"))
    cf_pool = cf_pool.merge(local, on="datapack")
    cf_pool = cf_pool.merge(nocf, on="datapack", suffixes=("_local", "_nocf"))
    cf_pool = cf_pool[
        ((cf_pool["ac1_residual"] == 1.0) | (cf_pool["ac1_crest"] == 1.0))
        & ((cf_pool["ac1_local"] == 0.0) | (cf_pool["ac1_nocf"] == 0.0))
    ]

    lines = [
        "# CREST-Residual Case Studies",
        "",
        f"- Residual wins over crest: {len(wins)}",
        f"- Residual losses against crest: {len(losses)}",
        f"- Counterfactual/topology wins over local or nocf pool: {len(cf_pool)}",
        "",
    ]

    def add_section(title: str, frame: pd.DataFrame, limit: int) -> None:
        lines.extend([f"## {title}", ""])
        if frame.empty:
            lines.extend(["No cases found.", ""])
            return
        for row in frame.head(limit).itertuples(index=False):
            datapack = str(row.datapack)
            gt = ", ".join(sorted(truth.get(datapack, set())))
            lines.extend(
                [
                    f"### {datapack}",
                    "",
                    f"- Ground truth: {gt}",
                    f"- crest: {_topk(outputs['crest'], datapack, 'crest')}",
                    (
                        "- crest_residual: "
                        f"{_topk(outputs['crest_residual'], datapack, 'crest_residual')}"
                    ),
                    f"- crest_local: {_topk(outputs['crest_local'], datapack, 'crest_local')}",
                    f"- crest_nocf: {_topk(outputs['crest_nocf'], datapack, 'crest_nocf')}",
                ]
            )
            if not diagnostics.empty:
                diag = diagnostics[diagnostics["case_id"] == datapack].head(5)
                keep = [
                    "service",
                    "A",
                    "F",
                    "S",
                    "M",
                    "P",
                    "R",
                    "F_residual",
                    "final_score",
                ]
                lines.extend(["", _markdown_table(diag[keep], floatfmt=".4f"), ""])
            lines.extend(
                [
                    (
                        "Interpretation: CREST-Residual changes rank only inside "
                        "a very narrow CREST near-tie when the challenger has "
                        "stronger mutation ownership, no larger propagation burden, "
                        "non-weaker F, and top residual eligibility."
                    ),
                    "",
                ]
            )

    add_section("Residual Wins", wins, 5)
    add_section("Residual Losses", losses, 5)
    add_section("Counterfactual Wins", cf_pool, 5)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def _eta_sensitivity(
    diagnostics: pd.DataFrame,
    truth: dict[str, set[str]],
    runtime_mean: float,
) -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    if diagnostics.empty:
        return pd.DataFrame()

    for eta in ETA_VALUES:
        per_case: list[CaseMetrics] = []
        for datapack, group in diagnostics.groupby("case_id"):
            group = group.copy()
            f_residual = np.clip(
                group["F"].to_numpy(dtype=np.float64)
                + eta
                * group["M"].to_numpy(dtype=np.float64)
                * np.maximum(
                    0.0,
                    group["R"].to_numpy(dtype=np.float64)
                    - group["F"].to_numpy(dtype=np.float64),
                ),
                0.0,
                1.0,
            )
            group["eta_score"] = group["A"].astype(float) * f_residual + group["S"].astype(float)
            group["eta_f_residual"] = f_residual
            group = group.sort_values(
                ["eta_score", "A", "eta_f_residual", "service"],
                ascending=[False, False, False, True],
                kind="stable",
            )
            group = _apply_eta_arbitration(group)
            group = group.sort_values(
                ["eta_score", "A", "eta_f_residual", "service"],
                ascending=[False, False, False, True],
                kind="stable",
            ).reset_index(drop=True)
            gt_names = truth.get(str(datapack), set())
            hit_ranks = [
                float(idx + 1)
                for idx, service in enumerate(group["service"])
                if str(service) in gt_names
            ]
            min_rank = min(hit_ranks) if hit_ranks else np.inf
            top1 = str(group.iloc[0]["service"]) if not group.empty else None
            per_case.append(
                CaseMetrics(
                    datapack=str(datapack),
                    min_rank=min_rank,
                    mrr=0.0 if not np.isfinite(min_rank) else 1.0 / min_rank,
                    ac1=float(min_rank <= 1),
                    ac3=float(min_rank <= 3),
                    ac5=float(min_rank <= 5),
                    top1=top1,
                )
            )
        frame = pd.DataFrame([row.__dict__ for row in per_case])
        rows.append(
            {
                "eta": eta,
                "total": int(len(frame)),
                "MRR": float(frame["mrr"].mean()),
                "AC@1": float(frame["ac1"].mean()),
                "AC@3": float(frame["ac3"].mean()),
                "AC@5": float(frame["ac5"].mean()),
                "runtime_mean": runtime_mean,
                "runtime_source": "estimated_from_eta1_diagnostics",
            }
        )
    return pd.DataFrame(rows)


def _ordinal_ranks(values: np.ndarray, higher_is_better: bool = True) -> np.ndarray:
    clean = np.nan_to_num(values.astype(np.float64, copy=False), nan=0.0)
    order = np.argsort(-clean if higher_is_better else clean, kind="stable")
    ranks = np.empty(clean.shape[0], dtype=np.int64)
    ranks[order] = np.arange(1, clean.shape[0] + 1, dtype=np.int64)
    return ranks


def _apply_eta_arbitration(group: pd.DataFrame) -> pd.DataFrame:
    if len(group) < 2:
        return group
    scores = group["eta_score"].to_numpy(dtype=np.float64)
    gaps = np.maximum(0.0, scores[:-1] - scores[1:])
    positive = gaps[gaps > 1e-12]
    if positive.size == 0:
        return group
    near_tie_gap = float(np.percentile(positive, 25))
    mutation_rank = _ordinal_ranks(group["M"].to_numpy(dtype=np.float64), True)
    residual_rank = _ordinal_ranks(group["R"].to_numpy(dtype=np.float64), True)
    propagation = group["P"].to_numpy(dtype=np.float64)
    explanatory = group["F"].to_numpy(dtype=np.float64)
    candidates: list[int] = []
    for idx in range(1, min(5, len(group))):
        if scores[0] - scores[idx] > near_tie_gap + 1e-12:
            continue
        if mutation_rank[idx] >= mutation_rank[0]:
            continue
        if propagation[idx] > propagation[0] + 1e-12:
            continue
        if explanatory[idx] + 1e-12 < explanatory[0]:
            continue
        if residual_rank[idx] > 3:
            continue
        candidates.append(idx)
    if not candidates:
        return group
    chosen = max(
        candidates,
        key=lambda idx: (
            float(group.iloc[idx]["R"]),
            float(group.iloc[idx]["eta_score"]),
            -idx,
        ),
    )
    group = group.copy()
    group.loc[group.index[chosen], "eta_score"] = float(scores[0]) + max(
        abs(float(scores[0])),
        1.0,
    ) * 1e-9
    return group


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="rcabench")
    parser.add_argument("--bootstrap-iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20250610)
    args = parser.parse_args()

    repo = Path.cwd()
    output_root = repo / "output" / "rcabench-platform-v2" / "data"
    labels_path = repo / "data" / "rcabench-platform-v2" / "meta" / "rcabench-csv" / "labels.csv"
    analysis_root = repo / "analysis" / "crest_residual"
    output_dir = analysis_root / "output"
    diagnostics_dir = analysis_root / "diagnostics"
    output_dir.mkdir(parents=True, exist_ok=True)
    diagnostics_dir.mkdir(parents=True, exist_ok=True)

    truth = _load_ground_truth(labels_path, args.dataset)
    outputs = {
        algorithm: _read_algorithm_outputs(output_root, args.dataset, algorithm)
        for algorithm in DEFAULT_ALGORITHMS
    }
    per_case = {
        algorithm: _case_metrics(output, truth)
        for algorithm, output in outputs.items()
        if not output.empty
    }
    perfs = {
        algorithm: _read_algorithm_perf(output_root, args.dataset, algorithm)
        for algorithm in per_case
    }

    summaries = pd.DataFrame(
        [
            _summary_row(args.dataset, algorithm, per_case[algorithm], perfs[algorithm])
            for algorithm in per_case
        ]
    )
    summaries.to_csv(output_dir / "residual_summary.csv", index=False)
    summary_lines = [
        "# CREST-Residual Summary",
        "",
        _markdown_table(summaries, floatfmt=".6f"),
        "",
    ]
    (output_dir / "residual_summary.md").write_text(
        "\n".join(summary_lines),
        encoding="utf-8",
    )

    residual_cases = per_case["crest_residual"]
    significance_rows: list[dict[str, float | str | int]] = []
    for baseline in PAIRED_BASELINES:
        significance_rows.extend(
            _bootstrap_delta(
                residual_cases,
                per_case[baseline],
                baseline,
                args.seed,
                args.bootstrap_iterations,
            )
        )
    significance = pd.DataFrame(significance_rows)
    significance.to_csv(output_dir / "residual_vs_crest_significance.csv", index=False)

    diagnostics = _load_residual_diagnostics(output_root, args.dataset)
    if not diagnostics.empty:
        diagnostics.to_parquet(
            diagnostics_dir / "crest_residual_scores.parquet",
            index=False,
        )
    residual_runtime = float(
        summaries.loc[
            summaries["algorithm"] == "crest_residual",
            "runtime_mean",
        ].iloc[0]
    )
    eta_sensitivity = _eta_sensitivity(diagnostics, truth, residual_runtime)
    if not eta_sensitivity.empty:
        eta_sensitivity.to_csv(output_dir / "residual_eta_sensitivity.csv", index=False)
    _case_studies(
        outputs,
        per_case,
        truth,
        diagnostics,
        output_dir / "residual_case_studies.md",
    )

    print(summaries.to_string(index=False))
    print(significance.to_string(index=False))


if __name__ == "__main__":
    main()
