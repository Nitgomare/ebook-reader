#!/usr/bin/env python
"""Small local entry point for building and previewing the learning site."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description="管理 Python 与数据分析学习站")
    parser.add_argument("command", choices=("build", "check", "preview"))
    parser.add_argument("--book", action="append", dest="books")
    parser.add_argument("--port", type=int, default=8010)
    args = parser.parse_args()

    build_command = [sys.executable, str(ROOT / "build.py")]
    for book in args.books or []:
        build_command.extend(("--book", book))
    result = subprocess.run(build_command, cwd=ROOT, check=False)
    if result.returncode:
        return result.returncode

    check_result = subprocess.run(
        [sys.executable, str(ROOT / "verify.py")], cwd=ROOT, check=False
    )
    if check_result.returncode or args.command in {"build", "check"}:
        return check_result.returncode

    print(f"\n预览地址：http://127.0.0.1:{args.port}")
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "http.server",
            str(args.port),
            "--bind",
            "127.0.0.1",
            "--directory",
            str(ROOT / "dist"),
        ],
        cwd=ROOT,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
