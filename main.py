#!/usr/bin/env -S uv run -s
from rcabench_platform.v2.algorithms.spec import Algorithm, global_algorithm_registry
from rcabench_platform.v2.cli.main import main

if __name__ == "__main__":
    registry = global_algorithm_registry()
    registry["baro"] = Algorithm
    registry["shapleyiq"] = Algorithm
    registry["ton"] = Algorithm
    registry["microrank"] = Algorithm
    registry["microhecl"] = Algorithm
    registry["microrca"] = Algorithm
    registry["nezha"] = Algorithm
    registry["microdig"] = Algorithm

    main(enable_builtin_algorithms=False)

