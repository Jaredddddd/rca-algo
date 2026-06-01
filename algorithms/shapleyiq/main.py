#!/usr/bin/env -S uv run -s
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from patches.rcabench_cli import main
from rcabench_platform.v2.algorithms.spec import global_algorithm_registry
from src.shapleyiq.platform.algorithms import TON, MicroRank, MicroHECL, MicroRCA, ShapleyRCA

if __name__ == "__main__":
    registry = global_algorithm_registry()
    registry["shapleyiq"] = ShapleyRCA
    registry["ton"] = TON
    registry["microrank"] = MicroRank
    registry["microhecl"] = MicroHECL
    registry["microrca"] = MicroRCA

    main(enable_builtin_algorithms=False)
