```sh
uv run --package baro python algorithms/baro/main.py eval batch -a baro  -d rcabench

uv run --package shapleyiq python algorithms/shapleyiq/main.py eval batch -a shapleyiq  -a microrank -a microhecl -a microrca  -d rcabench

uv run --package  nezha python algorithms/nezha/main.py eval batch -a nezha -d rcabench

uv run --package  microdig python algorithms/microdig/main.py eval batch -a microdig -d rcabench

uv run main.py eval perf-report rcabench
```