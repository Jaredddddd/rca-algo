#!/usr/bin/env python3
"""Build local RCABench train/test split using rcabench-platform helpers."""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path
from typing import Any

import polars as pl


def _default_platform_src() -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root.parent / "rcabench-platform" / "src"


def _load_previous_datapacks(path: Path | None) -> list[str]:
    if path is None:
        return []

    data = json.loads(path.read_text())
    if isinstance(data, list):
        return [str(item) for item in data]
    if isinstance(data, dict):
        values: list[str] = []
        for key in ("train", "test", "datapacks", "previous_datapacks"):
            items = data.get(key)
            if isinstance(items, list):
                values.extend(str(item) for item in items)
        return values
    raise SystemExit(f"Unsupported previous datapacks manifest: {path}")


def _import_splitter(platform_src: Path | None, data_root: Path, splitter_version: str):
    if platform_src is not None:
        platform_src = platform_src.resolve()
        if not platform_src.exists():
            raise SystemExit(f"rcabench-platform src does not exist: {platform_src}")
        sys.path.insert(0, str(platform_src))

    os.environ.setdefault("DATA_ROOT", str(data_root))

    try:
        if splitter_version == "v2":
            from rcabench_platform.v2.logging import logger
            from rcabench_platform.v2.datasets.rcabench import rcabench_split_train_test

            source = "rcabench_platform.v2.datasets.rcabench.rcabench_split_train_test"
        elif splitter_version == "v3":
            from rcabench_platform.v3.sdk.logging import logger
            from rcabench_platform.v3.sdk.datasets.rcabench import rcabench_split_train_test

            source = "rcabench_platform.v3.sdk.datasets.rcabench.rcabench_split_train_test"
        else:
            raise SystemExit(f"Unsupported splitter version: {splitter_version}")
    except ModuleNotFoundError as exc:
        raise SystemExit(
            f"Cannot import rcabench_platform.{splitter_version}. Clone rcabench-platform next to "
            "rca-algo-contrib or pass --platform-src /path/to/rcabench-platform/src."
        ) from exc

    logger.remove()
    logger.add(sys.stderr, level="INFO", colorize=False)
    return rcabench_split_train_test, source


def _read_dataset_datapacks(data_root: Path, dataset: str) -> list[str]:
    index_path = data_root / "meta" / dataset / "index.parquet"
    if not index_path.exists():
        raise SystemExit(f"Dataset index not found: {index_path}")
    return pl.read_parquet(index_path).select("datapack")["datapack"].to_list()


def _ensure_datapack_symlink(src: Path, dst: Path) -> None:
    if not src.exists():
        raise SystemExit(f"Source datapack does not exist: {src}")

    if dst.exists() or dst.is_symlink():
        if dst.resolve() != src.resolve():
            raise SystemExit(f"{dst} already exists and does not point to {src}")
        return

    dst.symlink_to(src, target_is_directory=True)


def _write_split_data_dir(data_root: Path, source_dataset: str, split_dir_name: str, datapacks: list[str]) -> Path:
    source_dir = data_root / "data" / source_dataset
    split_dir = data_root / "data" / split_dir_name
    split_dir.mkdir(parents=True, exist_ok=True)

    for datapack in datapacks:
        _ensure_datapack_symlink(source_dir / datapack, split_dir / datapack)

    return split_dir


def _write_split_meta(data_root: Path, source_dataset: str, split_dataset: str, datapacks: list[str]) -> None:
    meta_dir = data_root / "meta" / split_dataset
    meta_dir.mkdir(parents=True, exist_ok=True)

    index_df = pl.DataFrame(
        [{"dataset": split_dataset, "datapack": datapack} for datapack in datapacks]
    ).sort(by=pl.all())

    source_labels_path = data_root / "meta" / source_dataset / "labels.parquet"
    if not source_labels_path.exists():
        raise SystemExit(f"Source labels not found: {source_labels_path}")

    labels_df = (
        pl.read_parquet(source_labels_path)
        .filter(pl.col("datapack").is_in(datapacks))
        .with_columns(pl.lit(split_dataset).alias("dataset"))
        .sort(by=pl.all())
    )

    index_df.write_parquet(meta_dir / "index.parquet")
    labels_df.write_parquet(meta_dir / "labels.parquet")


def _write_manifest(
    path: Path,
    *,
    source_dataset: str,
    train_dataset: str,
    test_dataset: str,
    train_dir_name: str,
    test_dir_name: str,
    train_ratio: float,
    seed: int,
    splitter_version: str,
    splitter_source: str,
    train: list[str],
    test: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "source": splitter_source,
        "splitter_version": splitter_version,
        "source_dataset": source_dataset,
        "train_dataset": train_dataset,
        "test_dataset": test_dataset,
        "train_dir_name": train_dir_name,
        "test_dir_name": test_dir_name,
        "train_ratio": train_ratio,
        "seed": seed,
        "train_count": len(train),
        "test_count": len(test),
        "train": train,
        "test": test,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path("data") / "rcabench-platform-v2")
    parser.add_argument("--dataset", default="rcabench", help="Source v2 dataset name")
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--datapack-limit", type=int, default=0, help="0 means no limit")
    parser.add_argument("--previous-datapacks", type=Path)
    parser.add_argument("--platform-src", type=Path, default=_default_platform_src())
    parser.add_argument("--splitter-version", choices=["v2", "v3"], default="v2")
    parser.add_argument("--train-dir-name", default="__dev__rcabench_train_r1")
    parser.add_argument("--test-dir-name", default="__dev__rcabench_test_r1")
    parser.add_argument("--train-dataset", default="rcabench_train")
    parser.add_argument("--test-dataset", default="rcabench_test")
    parser.add_argument("--manifest", type=Path, default=Path("data") / "rcabench-platform-v2" / "splits" / "rcabench_train_test.json")
    parser.add_argument("--no-data-dirs", action="store_true", help="Only write manifest and meta parquet")
    parser.add_argument("--no-meta", action="store_true", help="Only write manifest and split data dirs")
    args = parser.parse_args()

    data_root = args.data_root.resolve()
    splitter, splitter_source = _import_splitter(args.platform_src, data_root, args.splitter_version)
    datapacks = _read_dataset_datapacks(data_root, args.dataset)
    previous_datapacks = _load_previous_datapacks(args.previous_datapacks)
    datapack_limit = args.datapack_limit if args.datapack_limit > 0 else len(datapacks)

    random.seed(args.seed)
    train, test = splitter(
        args.dataset,
        datapacks,
        args.train_ratio,
        previous_datapacks,
        datapack_limit,
    )

    if not args.no_data_dirs:
        train_dir = _write_split_data_dir(data_root, args.dataset, args.train_dir_name, train)
        test_dir = _write_split_data_dir(data_root, args.dataset, args.test_dir_name, test)
        print(f"wrote train dir: {train_dir}")
        print(f"wrote test dir:  {test_dir}")

    if not args.no_meta:
        _write_split_meta(data_root, args.dataset, args.train_dataset, train)
        _write_split_meta(data_root, args.dataset, args.test_dataset, test)
        print(f"wrote train meta dataset: {args.train_dataset}")
        print(f"wrote test meta dataset:  {args.test_dataset}")

    _write_manifest(
        args.manifest,
        source_dataset=args.dataset,
        train_dataset=args.train_dataset,
        test_dataset=args.test_dataset,
        train_dir_name=args.train_dir_name,
        test_dir_name=args.test_dir_name,
        train_ratio=args.train_ratio,
        seed=args.seed,
        splitter_version=args.splitter_version,
        splitter_source=splitter_source,
        train=train,
        test=test,
    )
    print(f"wrote manifest: {args.manifest}")
    print(f"train={len(train)} test={len(test)} total={len(train) + len(test)}")


if __name__ == "__main__":
    main()
