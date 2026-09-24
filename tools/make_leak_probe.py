"""生成"渲染泄漏检测"用的自检副本：复制交互图 HTML，并在末尾注入检测脚本。

用法：
    ..\\.venv\\Scripts\\python.exe tools\\make_leak_probe.py figure-2-10-11
输出：tmp/probe/<figure-id>.leak.html

检测内容：
- 连续触发滑块 input、开关 change、标签页切换、重置等高频渲染路径；
- 每次记录 .fk-grid 数量、SVG 总节点数、根层 line/path 数、各命名图层节点数；
- 额外报告每个 .fk-grid 的父元素（用于确认它究竟挂在哪一层）；
- 结论写进页面里的 <pre id="leak-report">，配合 chrome --dump-dom 读回。
"""

from __future__ import annotations

import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "tmp" / "probe"

INJECT = r"""
<pre id="leak-report" style="position:fixed;left:0;bottom:0;z-index:99;background:#0f172a;color:#e2e8f0;font:11px/1.4 Consolas,monospace;margin:0;padding:6px 8px;white-space:pre-wrap;max-width:100%">probing…</pre>
<script>
(function () {
  var lines = [];
  function log(s) {
    lines.push(String(s));
    var box = document.getElementById("leak-report");
    if (box) box.textContent = lines.join("\n");
  }
  function describe(node) {
    if (!node) return "null";
    if (node.nodeType === 1) {
      return node.tagName.toLowerCase()
        + (node.id ? "#" + node.id : "")
        + (node.getAttribute && node.getAttribute("class") ? "." + node.getAttribute("class") : "");
    }
    return "nodeType" + node.nodeType;
  }
  function snap(tag) {
    var svg = document.getElementById("viewport");
    if (!svg) { log(tag + " | 找不到 #viewport"); return; }
    var grids = document.querySelectorAll(".fk-grid");
    var parents = [];
    for (var i = 0; i < Math.min(grids.length, 3); i += 1) parents.push(describe(grids[i].parentNode));
    var root = svg;
    var named = svg.querySelectorAll(":scope > g").length;
    log(tag
      + " | fk-grid=" + grids.length
      + " 总节点=" + svg.querySelectorAll("*").length
      + " 根g=" + named
      + " 根line=" + root.querySelectorAll(":scope > line").length
      + " 根text=" + root.querySelectorAll(":scope > text").length
      + " | 前3个grid的父=" + parents.join("/"));
  }
  function fire(id, times) {
    var input = document.getElementById(id);
    if (!input) { log("  ! 缺少输入 " + id); return; }
    var lo = Number(input.min), hi = Number(input.max);
    for (var i = 0; i < times; i += 1) {
      input.value = String(lo + (hi - lo) * ((i % 13) / 12));
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }
  }
  function flip(id, times) {
    var el = document.getElementById(id);
    if (!el) { log("  ! 缺少开关 " + id); return; }
    for (var i = 0; i < times; i += 1) {
      el.checked = !el.checked;
      el.dispatchEvent(new Event("change", { bubbles: true }));
    }
  }
  function fireAll(times) {
    var controls = document.querySelectorAll('input[type="range"]');
    var toggles = document.querySelectorAll('input[type="checkbox"]');
    var used = 0;
    Array.prototype.forEach.call(controls, function (el) {
      var lo = Number(el.min || 0), hi = Number(el.max || 100);
      for (var i = 0; i < times; i += 1) {
        el.value = String(lo + (hi - lo) * ((i % 13) / 12));
        el.dispatchEvent(new Event("input", { bubbles: true }));
      }
      used += 1;
    });
    Array.prototype.forEach.call(toggles, function (el) {
      if (el.id === "auto") return;
      for (var i = 0; i < 2; i += 1) {
        el.checked = !el.checked;
        el.dispatchEvent(new Event("change", { bubbles: true }));
      }
      used += 1;
    });
    return { sliders: controls.length, toggles: toggles.length, used: used };
  }
  function run() {
    try {
      snap("A 初始");
      var info = fireAll(12);
      log("   （滑块 " + info.sliders + " 个、复选框 " + info.toggles + " 个，各触发 12 次）");
      snap("B 高频操作后");
      var auto = document.getElementById("auto");
      if (auto) { auto.checked = true; auto.dispatchEvent(new Event("change", { bubbles: true })); snap("C 自动旋转开"); auto.checked = false; auto.dispatchEvent(new Event("change", { bubbles: true })); }
      var tabs = document.querySelectorAll(".tabs button, [role=tab]");
      Array.prototype.forEach.call(tabs, function (t) { t.click(); t.click(); });
      snap("D 标签页切换后");
      var reset = document.getElementById("reset");
      if (reset) reset.click();
      snap("E 重置后");
      log("判据：fk-grid 恒为 1；根line/根text 恒为 0；总节点数不随操作次数增长");
    } catch (error) {
      log("! 执行异常：" + error.message);
    }
  }
  run();
}());
</script>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="生成渲染泄漏自检副本")
    parser.add_argument("figure_id", help="交互图 id，如 figure-2-10-11")
    parser.add_argument("--book", default="craig-introduction-to-robotics", help="书籍 slug")
    args = parser.parse_args()

    source = REPO / "content" / "books" / args.book / "docs" / "interactive" / f"{args.figure_id}.html"
    if not source.is_file():
        raise SystemExit(f"找不到 {source}")
    html = source.read_text(encoding="utf-8")
    if "</body>" in html:
        html = html.replace("</body>", INJECT + "\n</body>", 1)
    else:
        html += INJECT
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{args.figure_id}.leak.html"
    target.write_text(html, encoding="utf-8")
    print(f"写入 {target.relative_to(REPO)}（{len(html)} 字节）")


if __name__ == "__main__":
    main()
