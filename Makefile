
init:
	git submodule update --init --recursive

upgrade:
	git submodule update --remote --merge

build:
	uv run build_local.py batch