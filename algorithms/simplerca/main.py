#!/usr/bin/env -S uv run -s
from rcabench_platform.v2.cli.main import main
from rcabench_platform.v2.algorithms.spec import global_algorithm_registry
from rcabench_platform.v2.datasets.spec import get_datapack_list, get_datapack_folder
from src.simplerca.main import SimpleRCA
from src.simplerca.eadro_rca import EadroRCA
from src.simplerca.aiops_rca import AIOPSRCA
from src.simplerca.nezha_rca import NezhaRCA
if __name__ == "__main__":
    registry = global_algorithm_registry()
    registry["simplerca"] = NezhaRCA

    main(enable_builtin_algorithms=False)
    #print(get_datapack_list("nezha_tt"))
    #print(get_datapack_folder("nezha_tt","2023-01-29_08-43_return"))
