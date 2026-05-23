#!/usr/bin/env -S uv run -s
from rcabench_platform.v2.algorithms.spec import (
    AlgorithmArgs,
    global_algorithm_registry,
)

from src.microdig import MicroDig
from pathlib import Path
if __name__ == "__main__":
    registry = global_algorithm_registry()
    registry["microdig"] = MicroDig

    # This block is for testing the adapter directly
    from rcabench_platform.v2.logging import logger

    logger.info("Testing MicroDigAdapter...")
    args = AlgorithmArgs(
        dataset="rcabench",
        datapack="ts1-ts-route-plan-service-request-replace-method-qtbhzt",
        input_folder=Path(
            "test/ts1-ts-route-plan-service-request-replace-method-qtbhzt"
        ),
        output_folder=Path("."),
    )
    MicroDig()(args)
