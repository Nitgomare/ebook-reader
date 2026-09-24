"""把 Markdown 正文中的教材插图替换为「原图 / 可交互」容器。

用法：
    ..\\.venv\\Scripts\\python.exe tools\\apply_figure_containers.py            # 处理所有就绪的替换项
    ..\\.venv\\Scripts\\python.exe tools\\apply_figure_containers.py --check    # 只报告可处理项

替换计划在 `tools/figure_containers.json`，每个条目字段：
- book      : 书籍 slug
- doc       : 相对 docs/ 的 Markdown 路径
- image     : Markdown 中该图片的原始路径（相对当前 Markdown）
- figure_id : 交互文件 id（对应 docs/interactive/<figure_id>.html）
- number    : 图号，如 "图2-6"
- title     : 容器 data-interactive-title 与图题中使用的标题
- caption   : 该图在正文里原有的图题行（整行文本），用于就地把纯文本图题改成居中图题段落

规则（遵循 PROJECT_HANDOFF.md 7.1 与任务提示词第七节）：
1. 图片引用必须在该 Markdown 中唯一出现，否则报错不处理。
2. 保留原图相对路径，原图始终是默认显示的一面。
3. 图题处理：从插入的容器结尾向后找第一行非空文本；
   若它等于 caption（或以其开头），改写为居中图题段落；否则在容器结尾补一个居中图题段落。
   这样不会误改其它图的图题。
4. 幂等：已经存在同一 figure_id 容器时跳过。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS_ROOT = REPO / "content" / "books"
PLAN_FILE = REPO / "tools" / "figure_containers.json"

CONTAINER = """<div class="interactive-figure" data-interactive-src="../../interactive/{figure_id}.html" data-interactive-title="{title}">
  <div class="interactive-figure-toolbar" role="group" aria-label="{number}显示方式">
    <button type="button" class="is-active" data-figure-mode="original" aria-pressed="true">原图</button>
    <button type="button" data-figure-mode="interactive" aria-pressed="false">可交互</button>
  </div>
  <div class="interactive-figure-pane" data-figure-pane="original">
    <img src="{image}" alt="{alt}">
  </div>
  <div class="interactive-figure-pane" data-figure-pane="interactive" hidden>
    <div class="interactive-figure-loading">正在载入交互模型…</div>
  </div>
</div>"""


def image_line_pattern(image: str) -> re.Pattern[str]:
    return re.compile(r"^\!\[[^\]]*\]\(\s*" + re.escape(image) + r"\s*\)\s*$", re.M)


def number_prefix(number: str) -> str:
    """把「图2-6」「图3.11」统一为可容忍空格的匹配前缀。"""
    head = number[0]
    rest = number[1:]
    return head + r"\s*".join(re.escape(ch) for ch in rest)


def load_plans() -> list[dict[str, str]]:
    payload = json.loads(PLAN_FILE.read_text(encoding="utf-8"))
    plans = payload.get("plans", [])
    for plan in plans:
        for key in ("book", "doc", "image", "figure_id", "number", "title"):
            if key not in plan:
                raise SystemExit(f"{PLAN_FILE.name} 中的条目缺少字段 {key}：{plan}")
    return plans


def apply_plan(text: str, plan: dict[str, str]) -> tuple[str, str]:
    """返回 (新文本, 结果说明)。"""
    pattern = image_line_pattern(plan["image"])
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        return text, f"匹配到 {len(matches)} 处图片引用，跳过"

    container = CONTAINER.format(
        figure_id=plan["figure_id"],
        title=plan["title"],
        number=plan["number"],
        image=plan["image"],
        alt=plan.get("alt") or plan["title"],
    )
    cursor = matches[0].end()
    text = text[: matches[0].start()] + container + text[cursor:]
    after = matches[0].start() + len(container)
    cursor = after

    # 跳过空行，定位紧随其后的第一行非空文本
    probe = cursor
    while probe < len(text) and text[probe] in "\r\n":
        probe += 1
    line_end = text.find("\n", probe)
    if line_end == -1:
        line_end = len(text)
    candidate = text[probe:line_end].strip()
    new_caption = f'<p class="figure-caption">{plan["title"]}（原图与交互示例）</p>'

    if candidate == new_caption:
        return text, "已处理（图题已存在）"
    if candidate and re.match(r"^" + number_prefix(plan["number"]) + r"(?![\d.])", candidate):
        text = text[:probe] + new_caption + text[line_end:]
        return text, "已替换图片并改写图题"
    text = text[:cursor] + "\n\n" + new_caption + text[cursor:]
    return text, "已替换图片并补充图题"


def main() -> None:
    parser = argparse.ArgumentParser(description="把教材插图替换为原图/可交互容器")
    parser.add_argument("--check", action="store_true", help="只检查，不写入")
    args = parser.parse_args()

    total = 0
    for plan in load_plans():
        path = BOOKS_ROOT / plan["book"] / "docs" / plan["doc"]
        if not path.is_file():
            print(f"[缺失] {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if not image_line_pattern(plan["image"]).search(text):
            print(f"[跳过] {plan['number']}：{plan['doc']} 中已无该图片引用（视作已嵌入）")
            continue
        new_text, note = apply_plan(text, plan)
        if new_text == text:
            print(f"[警告] {plan['number']} {plan['doc']}：{note}", file=sys.stderr)
            continue
        if args.check:
            print(f"[检查] {plan['number']} {plan['doc']}：{note}")
            continue
        path.write_text(new_text, encoding="utf-8")
        total += 1
        print(f"[写入] {plan['number']} -> {plan['doc']}：{note}")

    if not args.check:
        print(f"完成：共处理 {total} 处")


if __name__ == "__main__":
    main()
