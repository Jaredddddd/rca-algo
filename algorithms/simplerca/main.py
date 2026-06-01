#!/usr/bin/env -S uv run -s
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from patches.rcabench_cli import main
from rcabench_platform.v2.algorithms.spec import global_algorithm_registry
from rcabench_platform.v2.datasets.spec import get_datapack_list, get_datapack_folder
from src.simplerca.main import SimpleRCA
from src.simplerca.eadro_rca import EadroRCA
from src.simplerca.aiops_rca import AIOPSRCA
from src.simplerca.nezha_rca import NezhaRCA

if __name__ == "__main__":
    registry = global_algorithm_registry()
    # # 这里的Nezha意思是数据集类型，而不是算法选的是NezhaRCA，算法依旧选的是SimpleRCA，具体对比可见Readme
    registry["simplerca"] = NezhaRCA

    main(enable_builtin_algorithms=False)
    #print(get_datapack_list("nezha_tt"))
    #print(get_datapack_folder("nezha_tt","2023-01-29_08-43_return"))
