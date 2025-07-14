#!/bin/bash -ex
export ALGORITHM=${ALGORITHM:-traceback-A8}
LOGURU_COLORIZE=0 .venv/bin/python main.py container run
