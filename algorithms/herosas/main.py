#!/usr/bin/env -S uv run -s
from rcabench_platform.v2.algorithms.spec import global_algorithm_registry
from rcabench_platform.v2.cli.main import main

from herosas import HeroSAS

if __name__ == "__main__":
    registry = global_algorithm_registry()
    registry["herosas"] = HeroSAS

    main(enable_builtin_algorithms=False)
