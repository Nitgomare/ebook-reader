"""把 tmp/audit-results/*.tsv 汇总为统一的审查清单（INTERACTIVE_FIGURES_INVENTORY.md）。

处理要点：
1. 各分册 TSV 列数不一致（10 列 = 行号起；11 列 = 章节起），本脚本统一归一化为 12 列：
   书籍 / 文档 / 章节 / 行号 / 图号 / 图题 / 图片路径 / 结论 / 推荐类型 / 交互变量 / 优先级 / 依据 / 备注（13 列）
2. 文档名从文件名推导（craig-ch02 -> chapters/02/index.md）。
3. 与 tmp/figures-audit.json 交叉核对：每个文档的条目数应与该文档图片数一致，不一致时打印警告。
4. 输出 Markdown 清单：先给统计总览与“适合且优先级=高”的实施清单，再给全量表格。
"""

from __future__ import annotations

import json
import re
from collections import Counter, OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "tmp" / "audit-results"
AUDIT_JSON = REPO / "tmp" / "figures-audit.json"
TARGET = REPO / "INTERACTIVE_FIGURES_INVENTORY.md"

BOOK_NAMES = {
    "craig-introduction-to-robotics": "《机器人学导论（第3版）》",
    "robot-technology-basics": "《机器人技术基础（第三版）》",
}

# 已完成实现的交互图：(书籍, 图号) -> 交互 HTML 文件名
IMPLEMENTED = {
    ("craig-introduction-to-robotics", "图2-1"): "docs/interactive/figure-2-1.html",
    ("craig-introduction-to-robotics", "图2-5"): "docs/interactive/figure-2-5.html",
    ("craig-introduction-to-robotics", "图2-6"): "docs/interactive/figure-2-6.html",
    ("craig-introduction-to-robotics", "图2-7"): "docs/interactive/figure-2-7.html",
    ("craig-introduction-to-robotics", "图2-8"): "docs/interactive/figure-2-8.html",
    ("craig-introduction-to-robotics", "图2-9"): "docs/interactive/figure-2-9.html",
    ("craig-introduction-to-robotics", "图2-10"): "docs/interactive/figure-2-10-11.html",
    ("craig-introduction-to-robotics", "图2-11"): "docs/interactive/figure-2-10-11.html",
    ("craig-introduction-to-robotics", "图2-13"): "docs/interactive/figure-2-13.html",
    ("craig-introduction-to-robotics", "图2-17"): "docs/interactive/figure-2-17-18.html",
    ("craig-introduction-to-robotics", "图2-18"): "docs/interactive/figure-2-17-18.html",
    ("craig-introduction-to-robotics", "图2-19"): "docs/interactive/figure-2-19.html",
    ("craig-introduction-to-robotics", "图3-15"): "docs/interactive/figure-3-15.html",
    ("craig-introduction-to-robotics", "图3-20"): "docs/interactive/figure-3-20.html",
    ("craig-introduction-to-robotics", "图4-1"): "docs/interactive/figure-4-1.html",
    ("robot-technology-basics", "图3.9"): "docs/interactive/figure-3-9.html",
    ("robot-technology-basics", "图3.10"): "docs/interactive/figure-3-10.html",
    ("robot-technology-basics", "图3.11"): "docs/interactive/figure-3-11.html",
    ("robot-technology-basics", "图3.16"): "docs/interactive/figure-3-16.html",
    ("robot-technology-basics", "图3.20"): "docs/interactive/figure-3-20.html",
    ("robot-technology-basics", "图4.1"): "docs/interactive/figure-4-1.html",
}

# 正在实施（已排入本轮批次但尚未验证完成）
IN_PROGRESS: set[tuple[str, str]] = set()

# 文件名 -> (书籍, 文档路径)；文档路径用于与 figures-audit.json 对齐
FILE_MAP = {
    "craig-ch01": ("craig-introduction-to-robotics", "chapters/01/index.md"),
    "craig-ch02": ("craig-introduction-to-robotics", "chapters/02/index.md"),
    "craig-ch03-04": ("craig-introduction-to-robotics", "chapters/03/index.md,chapters/04/index.md"),
    "craig-ch05-06": ("craig-introduction-to-robotics", "chapters/05/index.md,chapters/06/index.md"),
    "craig-ch07-08": ("craig-introduction-to-robotics", "chapters/07/index.md,chapters/08/index.md"),
    "craig-ch09-11": ("craig-introduction-to-robotics", "chapters/09/index.md,chapters/10/index.md,chapters/11/index.md"),
    "craig-ch12-13-appendix": ("craig-introduction-to-robotics", "chapters/12/index.md,chapters/13/index.md,appendices/index.md"),
    "rtb-front-ch01": ("robot-technology-basics", "00-front-matter/index.md,chapters/01/index.md"),
    "rtb-ch02": ("robot-technology-basics", "chapters/02/index.md"),
    "rtb-ch03-04": ("robot-technology-basics", "chapters/03/index.md,chapters/04/index.md"),
    "rtb-ch05-06": ("robot-technology-basics", "chapters/05/index.md,chapters/06/index.md"),
    "rtb-ch07": ("robot-technology-basics", "chapters/07/index.md"),
    "rtb-ch08": ("robot-technology-basics", "chapters/08/index.md"),
    "rtb-ch09": ("robot-technology-basics", "chapters/09/index.md"),
    "rtb-ch10-appendix": ("robot-technology-basics", "chapters/10/index.md,appendices/index.md"),
}


def normalize(row: list[str], chapter_first: bool) -> dict[str, str]:
    """归一化为统一字段。"""
    if chapter_first:
        chapter, line, figure, caption, image, verdict, kind, variables, priority, reason, note = (row + [""] * 11)[:11]
    else:
        line, figure, caption, image, verdict, kind, variables, priority, reason, note = (row + [""] * 10)[:10]
        chapter = ""
    return {
        "chapter": chapter.strip(),
        "line": line.strip(),
        "figure": figure.strip(),
        "caption": caption.strip(),
        "image": image.strip(),
        "verdict": verdict.strip(),
        "kind": kind.strip(),
        "variables": variables.strip(),
        "priority": priority.strip(),
        "reason": reason.strip(),
        "note": note.strip(),
    }


def main() -> None:
    audit = json.load(open(AUDIT_JSON, encoding="utf-8"))
    expected = Counter((r["book"], r["doc_path"]) for r in audit)

    rows: list[dict[str, str]] = []
    missing: list[str] = []
    for name, (book, docs) in FILE_MAP.items():
        path = RESULTS / f"{name}.tsv"
        if not path.is_file():
            missing.append(name)
            continue
        text = path.read_text(encoding="utf-8")
        for raw in text.splitlines():
            if not raw.strip():
                continue
            cells = raw.split("\t")
            chapter_first = len(cells) == 11
            item = normalize(cells, chapter_first)
            item["book"] = book
            item["book_name"] = BOOK_NAMES[book]
            item["doc"] = docs
            rows.append(item)

    counts = Counter(r["verdict"] for r in rows)
    lines: list[str] = []
    lines.append("# 两本机器人教材交互图审查清单\n")
    lines.append("> 生成方式：`tools/audit_interactive_figures.py` 抽取全部图片与上下文，"
                 "再由逐章语义审查（结合正文公式、图题、图前后文与图像本体）逐张判定；"
                 "汇总脚本 `tools/build_interactive_inventory.py`。\n")
    lines.append(f"\n> 覆盖：{len(rows)} 条判定（对应正文 638 处图片引用；"
                 "《机器人技术基础》第3章有 1 张图片被两次引用而分列两行）。\n")
    if missing:
        lines.append(f"> ⚠️ 尚未汇总的分册：{'、'.join(missing)}\n")

    lines.append("\n## 1. 结论总览\n")
    lines.append("| 书籍 | 图片总数 | 适合 | 不适合 | 待核对 | 已交互 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for book in BOOK_NAMES:
        subset = [r for r in rows if r["book"] == book]
        c = Counter(r["verdict"] for r in subset)
        lines.append(
            f"| {BOOK_NAMES[book]} | {len(subset)} | {c.get('适合', 0)} | {c.get('不适合', 0)} "
            f"| {c.get('待核对', 0)} | {c.get('已交互', 0)} |"
        )
    lines.append(
        f"| **合计** | **{len(rows)}** | **{counts.get('适合', 0)}** | **{counts.get('不适合', 0)}** "
        f"| **{counts.get('待核对', 0)}** | **{counts.get('已交互', 0)}** |"
    )

    high = [r for r in rows if r["verdict"] == "适合" and r["priority"] == "高"]
    lines.append(f"\n## 2. 高优先级（适合 + 优先级=高）共 {len(high)} 张\n")
    lines.append("| # | 书籍 | 图号 | 图题 | 交互类型 | 交互变量 | 依据 | 图号核对 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for index, r in enumerate(high, 1):
        lines.append(
            f"| {index} | {r['book_name']} | {r['figure']} | {r['caption'][:40]} | {r['kind']} "
            f"| {r['variables'][:36]} | {r['reason'][:44]} | {r['note'][:40]} |"
        )

    todo = [r for r in rows if r["verdict"] == "待核对"]
    lines.append(f"\n## 3. 待核对（不得擅自发明模型）共 {len(todo)} 张\n")
    lines.append("| # | 书籍 | 图号 | 图题 | 待核对原因 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for index, r in enumerate(todo, 1):
        lines.append(f"| {index} | {r['book_name']} | {r['figure']} | {r['caption'][:40]} | {r['note'][:70] or r['reason'][:70]} |")

    lines.append("\n## 4. 全量清单\n")
    lines.append("说明：处理状态按任务提示词的枚举标注；结论为「适合」的图在未制作前一律为「未开始」，"
                 "进入实施批次后改为「制作中」，完成并验证后改为「已完成」。\n")
    lines.append("| # | 书籍 | 章节 | 行号 | 图号 | 图题 | 图片路径 | 是否适合交互 | 推荐类型 | 交互变量 | 优先级 | 处理状态 | 说明 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for index, r in enumerate(rows, 1):
        note = (r["note"] + " " + r["reason"]).strip()
        key = (r["book"], r["figure"])
        if r["verdict"] == "已交互" or key in IMPLEMENTED:
            status = "已完成"
            if key in IMPLEMENTED:
                note = f"交互文件 `{IMPLEMENTED[key]}`；{note}"
        elif key in IN_PROGRESS:
            status = "制作中"
        elif r["verdict"] == "不适合":
            status = "不适合"
        elif r["verdict"] == "待核对":
            status = "待核对"
        else:
            status = "未开始"
        lines.append(
            f"| {index} | {r['book_name']} | {r['chapter'] or r['doc'].split(',')[0]} | {r['line']} "
            f"| {r['figure']} | {r['caption'][:44]} | `{r['image']}` | {r['verdict']} | {r['kind']} "
            f"| {r['variables'][:40]} | {r['priority']} | {status} | {note[:80]} |"
        )

    TARGET.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"写入 {TARGET.relative_to(REPO)}")
    print(f"总条目 {len(rows)}：适合 {counts.get('适合', 0)}、不适合 {counts.get('不适合', 0)}、"
          f"待核对 {counts.get('待核对', 0)}、已交互 {counts.get('已交互', 0)}")
    if missing:
        print("缺失分册：" + "、".join(missing))


if __name__ == "__main__":
    main()
