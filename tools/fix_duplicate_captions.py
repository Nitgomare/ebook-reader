"""清理图题重复：删除因「补充图题」而遗留的旧纯文本图题行。

背景：部分教材正文把图题写在图片下方的几行之外（中间夹着公式行），
`apply_figure_containers.py` 会在容器后立即补一个居中图题段落，
于是原来的纯文本图题行就成了重复内容。本脚本负责删除这些遗留行。

判定规则（保守）：
1. 只处理 `figure_containers.json` 中已嵌入交互容器的条目。
2. 只检查容器与图题段落前后各 12 行范围内、以「图<号>」开头的独立行。
3. 该行必须与图题段落不同、且不含「如/见/所示/中/为」等正文指代词，避免误删正文。
4. 同一图号只删一处，删完打印报告。

用法：
    ..\\.venv\\Scripts\\python.exe tools\\fix_duplicate_captions.py --check   # 只报告
    ..\\.venv\\Scripts\\python.exe tools\\fix_duplicate_captions.py           # 执行
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS_ROOT = REPO / "content" / "books"
PLAN_FILE = REPO / "tools" / "figure_containers.json"

CONTEXT_LINES = 12
FORBIDDEN = ("如", "见", "所示", "其中", "表明", "说明", "中为", "时为")


def main() -> None:
    parser = argparse.ArgumentParser(description="清理重复的旧图题行")
    parser.add_argument("--check", action="store_true", help="只报告，不写入")
    args = parser.parse_args()

    plans = json.loads(PLAN_FILE.read_text(encoding="utf-8"))["plans"]
    removed_total = 0

    for plan in plans:
        path = BOOKS_ROOT / plan["book"] / "docs" / plan["doc"]
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        caption = f'<p class="figure-caption">{plan["title"]}（原图与交互示例）</p>'
        if caption not in lines:
            continue
        caption_index = lines.index(caption)
        number = plan["number"]
        # 允许图号内部出现空格，例如「图 3.11」
        number_re = re.compile("^" + r"\s*".join(re.escape(ch) for ch in number) + r"(?![\d.])\s")
        targets: list[int] = []
        for offset in range(1, CONTEXT_LINES + 1):
            for index in (caption_index - offset, caption_index + offset):
                if not (0 <= index < len(lines)):
                    continue
                line = lines[index].strip()
                if not number_re.match(line):
                    continue
                if any(word in line for word in FORBIDDEN):
                    continue
                if "interactive-figure" in line or "<p" in line:
                    continue
                targets.append(index)
        if not targets:
            print(f"[保留] {number} {plan['doc']}：未发现重复图题行")
            continue
        for index in sorted(set(targets), reverse=True):
            print(f"[{'检查' if args.check else '删除'}] {number} {plan['doc']} 第 {index + 1} 行：{lines[index].strip()[:60]}")
            if not args.check:
                del lines[index]
                removed_total += 1
        if not args.check:
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"完成：{'将删除' if args.check else '共删除'} {removed_total} 行重复图题")


if __name__ == "__main__":
    main()
