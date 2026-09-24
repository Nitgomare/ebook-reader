"""按图号从审查清单里取出一批图的完整信息，生成实施简报。

用法：
    ..\\.venv\\Scripts\\python.exe tools\\figure_brief.py 图3-2 图3-6 --book craig-introduction-to-robotics
输出：tmp/brief/<book>.md（供实施 Agent 直接读取）
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "tmp" / "audit-results"
OUT = REPO / "tmp" / "brief"

FILE_MAP = {
    "craig-ch01": "craig-introduction-to-robotics",
    "craig-ch02": "craig-introduction-to-robotics",
    "craig-ch03-04": "craig-introduction-to-robotics",
    "craig-ch05-06": "craig-introduction-to-robotics",
    "craig-ch07-08": "craig-introduction-to-robotics",
    "craig-ch09-11": "craig-introduction-to-robotics",
    "craig-ch12-13-appendix": "craig-introduction-to-robotics",
    "rtb-front-ch01": "robot-technology-basics",
    "rtb-ch02": "robot-technology-basics",
    "rtb-ch03-04": "robot-technology-basics",
    "rtb-ch05-06": "robot-technology-basics",
    "rtb-ch07": "robot-technology-basics",
    "rtb-ch08": "robot-technology-basics",
    "rtb-ch09": "robot-technology-basics",
    "rtb-ch10-appendix": "robot-technology-basics",
}

AUDIT = json.loads((REPO / "tmp" / "figures-audit.json").read_text(encoding="utf-8"))


def audit_context(book: str, image: str) -> dict | None:
    for record in AUDIT:
        if record["book"] == book and image.endswith(record["image_path"].lstrip("./")):
            return record
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="生成交互图实施简报")
    parser.add_argument("figures", nargs="+", help="图号，如 图3-2")
    parser.add_argument("--book", required=True, help="书籍 slug")
    args = parser.parse_args()

    wanted = set(args.figures)
    rows: list[dict[str, str]] = []
    for name, book in FILE_MAP.items():
        if book != args.book:
            continue
        path = RESULTS / f"{name}.tsv"
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            cells = raw.split("\t")
            if len(cells) == 11:
                chapter, line, figure, caption, image, verdict, kind, variables, priority, reason, note = cells
            else:
                line, figure, caption, image, verdict, kind, variables, priority, reason, note = cells
                chapter = ""
            if figure.strip() not in wanted:
                continue
            rows.append({
                "chapter": chapter.strip(), "line": line.strip(), "figure": figure.strip(),
                "caption": caption.strip(), "image": image.strip(), "verdict": verdict.strip(),
                "kind": kind.strip(), "variables": variables.strip(), "priority": priority.strip(),
                "reason": reason.strip(), "note": note.strip(),
            })

    OUT.mkdir(parents=True, exist_ok=True)
    lines = [f"# 实施简报：{args.book}", ""]
    for row in rows:
        ctx = audit_context(args.book, row["image"])
        lines += [
            f"## {row['figure']}　{row['caption']}",
            f"- 正文：`content/books/{args.book}/docs/`（行号 {row['line']}，见下方上下文）",
            f"- 图片：`{row['image']}`",
            f"- 审查结论：{row['verdict']}；推荐交互类型：{row['kind']}；优先级：{row['priority']}",
            f"- 建议交互变量：{row['variables']}",
            f"- 教材依据：{row['reason']}",
            f"- 实施提醒：{row['note']}",
        ]
        if ctx:
            lines += [
                f"- 所在小节：{' > '.join(ctx['heading_path'][-2:])}",
                f"- 图片上文：{ctx['before_text'][:260]}",
                f"- 图片下文：{ctx['after_text'][:260]}",
            ]
        lines.append("")
    target = OUT / f"{args.book}-{'-'.join(args.figures)}.md".replace("/", "_")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"写入 {target.relative_to(REPO)}（{len(rows)} 张图）")
    for row in rows:
        print(f"  {row['figure']}\t{row['image']}\t{row['verdict']}\t{row['priority']}")


if __name__ == "__main__":
    main()
