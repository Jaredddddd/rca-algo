#!/bin/bash -ex
export ALGORITHM=${ALGORITHM:-traceback-A8}
LOGURU_COLORIZE=0 .venv/bin/python -m rcabench_platform.v2.online.run_exp_platform run
