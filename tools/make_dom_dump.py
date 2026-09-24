"""诊断探针：打印 SVG 根层的真实子元素结构。

用法：
    ..\\.venv\\Scripts\\python.exe tools\\make_dom_dump.py figure-2-10-11
输出：tmp/probe/<figure-id>.dom.html（注入脚本把结构写进 <pre id="dom-report">）
"""

from __future__ import annotations

import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "tmp" / "probe"

INJECT = r"""
<pre id="dom-report" style="position:fixed;left:0;bottom:0;z-index:99;background:#0f172a;color:#e2e8f0;font:11px/1.4 Consolas,monospace;margin:0;padding:6px 8px;white-space:pre-wrap;max-width:100%">dumping…</pre>
<script>
(function () {
  var out = [];
  function log(s) { out.push(String(s)); document.getElementById("dom-report").textContent = out.join("\n"); }
  function describe(n) {
    var cls = n.getAttribute && n.getAttribute("class") ? "." + n.getAttribute("class") : "";
    return n.tagName.toLowerCase() + (n.id ? "#" + n.id : "") + cls
      + "(" + n.childElementCount + "子)";
  }
  var svg = document.getElementById("viewport");
  log("svg#viewport 直接子元素 " + svg.childElementCount + " 个：");
  Array.prototype.forEach.call(svg.children, function (child, i) {
    log("  [" + i + "] " + describe(child));
  });
  log("");
  log("查找所有 .fk-grid：");
  var grids = document.querySelectorAll(".fk-grid");
  log("  共 " + grids.length + " 个");
  for (var i = 0; i < Math.min(grids.length, 4); i += 1) {
    var g = grids[i];
    var chain = [];
    var node = g;
    while (node && node !== document.documentElement) { chain.push(describe(node)); node = node.parentNode; }
    log("  grid[" + i + "] 祖先链：" + chain.join(" < "));
    log("     子元素数=" + g.childElementCount + "，第一个子=" + (g.firstElementChild ? describe(g.firstElementChild) : "无"));
  }
  log("");
  log("文档里 #grid 元素：" + document.querySelectorAll("#grid").length
    + "，#axes：" + document.querySelectorAll("#axes").length
    + "，#viewport：" + document.querySelectorAll("#viewport").length
    + "，#guides：" + document.querySelectorAll("#guides").length
    + "，#vectors：" + document.querySelectorAll("#vectors").length
    + "，#labels：" + document.querySelectorAll("#labels").length);
  log("document.querySelector('#grid') 的父=" + describe(document.querySelector("#grid").parentNode));
  log("document.querySelector('#grid').childElementCount=" + document.querySelector("#grid").childElementCount);
  log("document.querySelector('#viewport').querySelectorAll('.fk-grid').length="
    + document.querySelector("#viewport").querySelectorAll(".fk-grid").length);
  log("document.querySelectorAll('#viewport > g').length=" + document.querySelectorAll("#viewport > g").length);
  var direct = document.querySelectorAll("#viewport > .fk-grid");
  log("#viewport > .fk-grid 数量=" + direct.length);
}());
</script>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="生成 DOM 结构诊断副本")
    parser.add_argument("figure_id", help="交互图 id")
    parser.add_argument("--book", default="craig-introduction-to-robotics")
    args = parser.parse_args()
    source = REPO / "content" / "books" / args.book / "docs" / "interactive" / f"{args.figure_id}.html"
    html = source.read_text(encoding="utf-8")
    html = html.replace("</body>", INJECT + "\n</body>", 1) if "</body>" in html else html + INJECT
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{args.figure_id}.dom.html"
    target.write_text(html, encoding="utf-8")
    print(f"写入 {target.relative_to(REPO)}")


if __name__ == "__main__":
    main()
