#!/usr/bin/env python3
"""Build rcabench-platform v2 metadata for an already-converted RCABench tree."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from rcabench_platform.v2.datasets.spec import Label
from rcabench_platform.v2.logging import logger
from rcabench_platform.v2.sources.convert import DatapackLoader, DatasetLoader, convert_dataset


class _CallableName(str):
    def __call__(self) -> str:
        return str(self)


class PreconvertedRCABenchDatapackLoader(DatapackLoader):
    def __init__(self, src_folder: Path) -> None:
        self._src_folder = src_folder
        _validate_datapack_name(self.name)

    @property
    def name(self) -> _CallableName:
        return _CallableName(self._src_folder.name)

    def labels(self) -> list[Label]:
        injection = json.loads((self._src_folder / "injection.json").read_text())
        return [Label(level="service", name=service) for service in _service_names(injection)]

    def data(self) -> dict[str, Any]:
        raise RuntimeError(
            f"{self.name} is expected to be preconverted and marked with .finished; "
            "this helper only reuses convert_dataset() to build index.parquet and labels.parquet."
        )


class PreconvertedRCABenchDatasetLoader(DatasetLoader):
    def __init__(self, src: Path, dataset: str) -> None:
        self._src = src
        self._dataset = dataset
        self._datapacks = _scan_preconverted_datapacks(src)

    def name(self) -> str:
        return self._dataset

    def __len__(self) -> int:
        return len(self._datapacks)

    def __getitem__(self, index: int) -> DatapackLoader:
        return PreconvertedRCABenchDatapackLoader(self._src / self._datapacks[index])


def _validate_datapack_name(name: str) -> None:
    if not re.match(r"^[A-Za-z0-9_-]+$", name):
        raise ValueError(f"Invalid datapack name: {name}")


def _service_names(injection: dict[str, Any]) -> list[str]:
    ground_truth = injection.get("ground_truth")
    names: list[str] = []

    if isinstance(ground_truth, dict):
        services = ground_truth.get("service", [])
        if isinstance(services, str):
            names.append(services)
        elif isinstance(services, list):
            names.extend(str(item) for item in services if item)
    elif isinstance(ground_truth, list):
        for item in ground_truth:
            if not isinstance(item, dict):
                continue
            services = item.get("service", [])
            if isinstance(services, str):
                names.append(services)
            elif isinstance(services, list):
                names.extend(str(service) for service in services if service)

    return sorted(set(names))


def _scan_preconverted_datapacks(src: Path) -> list[str]:
    datapacks: list[str] = []
    missing_finished: list[str] = []

    for datapack_dir in sorted(path for path in src.iterdir() if path.is_dir()):
        injection_path = datapack_dir / "injection.json"
        if not injection_path.exists():
            continue

        injection = json.loads(injection_path.read_text())
        if not _service_names(injection):
            print(f"skip {datapack_dir.name}: no service labels in injection.json")
            continue

        if not (datapack_dir / ".finished").exists():
            missing_finished.append(datapack_dir.name)
            continue

        datapacks.append(datapack_dir.name)

    if missing_finished:
        examples = ", ".join(missing_finished[:5])
        raise SystemExit(
            "Found datapacks without .finished marker. "
            "This helper expects an already-converted RCABench tree so convert_dataset() "
            f"does not rewrite datapack data. Examples: {examples}"
        )

    if not datapacks:
        raise SystemExit(f"No valid datapacks found under {src}")

    return datapacks


def configure_logging(verbose: bool) -> None:
    logger.remove()
    logger.add(sys.stderr, level="DEBUG" if verbose else "INFO", colorize=False)


def build_meta(src: Path, data_root: Path, dataset: str) -> tuple[int, int]:
    src = src.resolve()
    data_root = data_root.resolve()
    dataset_data = data_root / "data" / dataset

    dataset_data.parent.mkdir(parents=True, exist_ok=True)

    if dataset_data.exists() or dataset_data.is_symlink():
        if dataset_data.resolve() != src:
            raise SystemExit(f"{dataset_data} already exists and does not point to {src}")
    else:
        dataset_data.symlink_to(src, target_is_directory=True)

    loader = PreconvertedRCABenchDatasetLoader(src, dataset)
    convert_dataset(loader, root=data_root, skip_finished=True, parallel=1)
    labels = sum(len(loader[index].labels()) for index in range(len(loader)))
    return len(loader), labels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=Path, required=True, help="Downloaded RCABench-Dataset directory")
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("data") / "rcabench-platform-v2",
        help="rcabench-platform data root used by DATA_ROOT",
    )
    parser.add_argument("--dataset", default="rcabench")
    parser.add_argument("--verbose", action="store_true", help="Show rcabench-platform debug logs")
    args = parser.parse_args()

    configure_logging(args.verbose)
    datapacks, labels = build_meta(args.src, args.data_root, args.dataset)
    print(f"wrote dataset={args.dataset} datapacks={datapacks} labels={labels} data_root={args.data_root}")


if __name__ == "__main__":
    main()
