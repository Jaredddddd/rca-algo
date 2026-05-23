from rcabench_platform.v2.cli.main import main
from rcabench_platform.v2.algorithms.spec import (
    global_algorithm_registry,
    Algorithm,
    AlgorithmArgs,
    AlgorithmAnswer,
)
import os
from client import inference_single

class ART(Algorithm):
    def needs_cpu_count(self) -> int | None:
        return 4

    def __call__(self, args: AlgorithmArgs) -> list[AlgorithmAnswer]:
        model_path = "model.pkl"
        results = inference_single(
            datapack_path=args.input_folder,
            model_path=model_path,
        )
        answers = [
            AlgorithmAnswer(level="service", name=name, rank=i + 1)
            for i, name in enumerate(results)
        ]
        return answers



if __name__ == "__main__":
    registry = global_algorithm_registry()
    registry["art"] = ART
    main(enable_builtin_algorithms=False)