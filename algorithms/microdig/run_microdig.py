#!/usr/bin/env python3
"""
Main entry point for MicroDig CLI application.

This script provides the command-line interface for running MicroDig
analysis on the new data format.
"""

import sys
from pathlib import Path

# Add src directory to path for development
src_dir = Path(__file__).parent.parent / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))

if __name__ == "__main__":
    from microdig.cli import app

    app()
