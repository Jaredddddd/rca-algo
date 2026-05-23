#!/bin/bash -ex
export ALGORITHM=${ALGORITHM:-art}
LOGURU_COLORIZE=0 .venv/bin/python main.py container run