"""
共享 CLI 入口：在调用 rcabench_platform CLI 前自动应用所有补丁。

各 algorithm 的 main.py 应使用如下模式导入：

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from patches.rcabench_cli import main

这样可以确保 uv run --package <algo> 的子环境中也能找到 patches 包。
"""

import patches.rcabench_mrr_fix  # noqa: F401 — 应用 MRR 计算修复

from rcabench_platform.v2.cli.main import main

__all__ = ["main"]
