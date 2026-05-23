#!/bin/bash -ex
export ALGORITHM=${ALGORITHM:-simplerca}
LOGURU_COLORIZE=0 .venv/bin/python main.py container run
