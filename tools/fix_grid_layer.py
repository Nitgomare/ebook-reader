"""批量修正交互图规格里 scene.grid(...) 缺少父图层的问题。

背景（2026-09-24 定位的渲染泄漏）：
    规格的 render() 只会清理自己声明的命名图层（如 #grid），
    但 scene.grid(half, step) 默认把 <g class="fk-grid"> 挂在 scene.layer（根 SVG）上，
    于是每次重绘都往根层堆一套网格 → 拖动/缩放/自动旋转时出现大量拖影。

本脚本把 `scene.grid(args...)` 统一改成 `scene.grid(args..., null, gridLayer)`。
只处理确实声明了 gridLayer 的规格；改完请用
    ..\\.venv\\Scripts\\python.exe tools\\check_svg_layer_leaks.py
复验（要求根层 g.fk-grid = 0、裸 line = 0）。

用法：
    ..\\.venv\\Scripts\\python.exe tools\\fix_grid_layer.py --check    # 只报告
    ..\\.venv\\Scripts\\python.exe tools\\fix_grid_layer.py            # 执行
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPEC_DIRS = [
    REPO / "content" / "books" / "craig-introduction-to-robotics" / "docs" / "interactive" / "specs",
    REPO / "content" / "books" / "robot-technology-basics" / "docs" / "interactive" / "specs",
]

CALL_RE = re.compile(r"scene\.grid\((?P<args>[^;]*?)\)(?P<tail>\s*;)")


def already_fixed(args: str) -> bool:
    return "gridLayer" in args


def fix_source(text: str) -> tuple[str, int]:
    if 'getElementById("grid")' not in text:
        return text, 0
    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        args = match.group("args").strip()
        if already_fixed(args):
            return match.group(0)
        changed += 1
        return f"scene.grid({args}, null, gridLayer){match.group('tail')}"

    return CALL_RE.sub(repl, text), changed


def main() -> None:
    parser = argparse.ArgumentParser(description="修正 scene.grid 的父图层")
    parser.add_argument("--check", action="store_true", help="只报告不写盘")
    args = parser.parse_args()

    total = 0
    for folder in SPEC_DIRS:
        if not folder.is_dir():
            continue
        for spec in sorted(folder.glob("figure_*.py")):
            text = spec.read_text(encoding="utf-8")
            new_text, changed = fix_source(text)
            if not changed:
                continue
            total += changed
            print(f"[{'检查' if args.check else '写入'}] {spec.name}：修正 {changed} 处 scene.grid 调用")
            if not args.check:
                spec.write_text(new_text, encoding="utf-8")
    if not total:
        print("没有需要修正的规格（可能已全部修好）")
    else:
        print(f"合计 {total} 处；" + ("未写盘" if args.check else "请重新生成并跑 check_svg_layer_leaks.py 复验"))


if __name__ == "__main__":
    main()
