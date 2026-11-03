"""为《机械原理（第四版）》生成交互机构图（自包含页面）。

按 anatomy 的做法画成一台真实的小试验台：底板与地脚、轴承立柱与压盖螺栓、
贯穿销轴与挡圈、带圆眼的链杆；等轴测正交投影、明暗分面、画家序。
交互沿用站点既有交互图的面板写法（滑块 + 复选项 + 重置 + 读数区）。

用法：python -X utf8 tools/mechanism_figures/build.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "content/books/mechanism-principles-4e"
OUT = BOOK / "docs/interactive"
TOOLS = Path(__file__).resolve().parent

TEMPLATE_PAGE = ROOT / "content/books/robot-technology-basics/docs/interactive/figure-3-9.html"
KIT_SRC = ROOT / "content/books/craig-introduction-to-robotics/docs/interactive/figure-kit.js"

FIGURES = [
    {
        "file": "figure-3-3.html",
        "title": "图3-3 铰链四杆机构",
        "aria": "铰链四杆机构曲柄摇杆的交互示意，曲柄整周回转，摇杆往复摆动",
        "subtitle": "曲柄 1 绕 A 整周回转，连带连杆 2 使摇杆 3 绕 D 往复摆动。"
        "最短杆为连架杆且满足格拉肖夫条件，才存在曲柄。",
        "controls": [
            ("theta", "曲柄转角 θ", 0, 360, 1, "42", "42°"),
            ("r", "曲柄 AB 长度", 0.70, 1.10, 0.01, "1.0", "1.00"),
            ("l", "连杆 BC 长度", 2.90, 3.60, 0.01, "3.2", "3.20"),
        ],
        "options": [
            ("auto", "自动运转", True),
            ("showTrace", "显示铰点轨迹", True),
            ("showLabels", "显示铰点标注", True),
        ],
        "legend": [
            ("#c08a3e", "曲柄 1（AB，整周回转）"),
            ("#3f6fae", "连杆 2（BC）"),
            ("#3f8f96", "摇杆 3（CD，往复摆动）"),
            ("#8a93a3", "机架 4（AD，固定）"),
        ],
        "readout": [
            ("θ", "曲柄转角", "thetaOut", "42°"),
            ("ψ", "摇杆摆角", "psiOut", "—"),
            ("γ", "传动角", "gammaOut", "—"),
        ],
        "note": "格拉肖夫条件：r + l ≤ d + e（1.0 + 3.2 ≤ 2.4 + 3.0），最短杆 AB 与机架相邻 ⇒ 曲柄摇杆机构。",
        "scene": "fig_3_3.js",
    },
    {
        "file": "figure-3-6.html",
        "title": "图3-6 冲床的双曲柄机构",
        "aria": "双曲柄机构交互示意，两根连架杆都能整周回转",
        "subtitle": "机架 AD 最短且与两连架杆之和满足格拉肖夫条件，AB 与 CD 均可整周回转；两曲柄转速不等，冲床由此获得空行程快、工作行程慢的运动。",
        "controls": [
            ("theta", "主动曲柄转角 θ", 0, 360, 1, "0", "0°"),
            ("bc", "连杆 BC 长度", 1.05, 1.75, 0.01, "1.4", "1.40"),
        ],
        "options": [
            ("auto", "自动运转", True),
            ("showTrace", "显示铰点轨迹", True),
            ("showLabels", "显示铰点标注", True),
        ],
        "legend": [
            ("#c08a3e", "主动曲柄 1（AB，整周回转）"),
            ("#3f6fae", "连杆 2（BC）"),
            ("#7c6aa8", "从动曲柄 3（CD，整周回转）"),
            ("#8a93a3", "机架 4（AD，固定）"),
        ],
        "readout": [
            ("θ", "主动曲柄转角", "thetaOut", "0°"),
            ("φ", "从动曲柄转角", "phiOut", "—"),
            ("i", "瞬时传动比 dφ/dθ", "ratioOut", "—"),
        ],
        "note": "格拉肖夫条件：l_min + l_max ≤ 其余两杆之和（0.9 + 1.4 ≤ 1.4 + 1.3），最短杆 AD 为机架 ⇒ 双曲柄机构；两侧曲柄转速不等，故冲床空行程快、工作行程慢。",
        "scene": "fig_3_6.js",
    },
    {
        "file": "figure-3-12.html",
        "title": "图3-12 造型机翻箱机构",
        "aria": "双摇杆机构交互示意，两根连架杆都在有限角度内摆动",
        "subtitle": "造型机翻箱用的双摇杆机构：机架 AD 最长、连杆 BC 最短，"
        "两连架杆都只能在有限角度内摆动，不能整周回转。",
        "controls": [
            ("theta", "主动摇杆转角 θ", 16, 80, 1, "60", "60°"),
            ("cd", "摇杆 CD 长度", 1.45, 1.95, 0.01, "1.70", "1.70"),
        ],
        "options": [
            ("auto", "自动运转", True),
            ("showTrace", "显示铰点轨迹", True),
            ("showLabels", "显示铰点标注", True),
        ],
        "legend": [
            ("#c08a3e", "主动摇杆 1（AB，往复摆动）"),
            ("#3f6fae", "连杆 2（BC）"),
            ("#3f8f96", "从动摇杆 3（CD，往复摆动）"),
            ("#8a93a3", "机架 4（AD，固定）"),
        ],
        "readout": [
            ("θ", "主动摇杆转角", "thetaOut", "60°"),
            ("ψ", "从动摇杆转角", "psiOut", "—"),
            ("β", "连杆方位角", "couplerOut", "—"),
        ],
        "note": "格拉肖夫条件：l_min + l_max > 其余两杆之和（1.2 + 2.6 > 1.7 + 1.7），得不到曲柄 ⇒ 双摇杆机构。摆动范围由装配条件 |BC − CD| ≤ |BD| ≤ BC + CD 限定，滑块范围会自动收在该可装配区间内。",
        "scene": "fig_3_12.js",
    },
    {
        "file": "figure-3-15.html",
        "title": "图3-15 曲柄滑块机构",
        "aria": "曲柄滑块机构交互示意，曲柄整周回转带动滑块沿导轨往复",
        "subtitle": "曲柄 AB 整周回转，经连杆 BC 推动滑块 C 沿导轨往复移动。"
        "偏距 e 不为零时为偏置曲柄滑块，行程大于 2r，并具有急回特性。",
        "controls": [
            ("theta", "曲柄转角 θ", 0, 360, 1, "30", "30°"),
            ("r", "曲柄半径 r", 0.90, 1.20, 0.01, "1.20", "1.20"),
            ("e", "偏距 e", 0, 1.00, 0.01, "0.60", "0.60"),
        ],
        "options": [
            ("auto", "自动运转", True),
            ("showTrace", "显示铰点轨迹", True),
            ("showLabels", "显示铰点标注", True),
        ],
        "legend": [
            ("#c08a3e", "曲柄 1（AB，整周回转）"),
            ("#3f6fae", "连杆 2（BC）"),
            ("#7c6aa8", "滑块 3（C，往复移动）"),
            ("#8a93a3", "机架与导轨 4"),
        ],
        "readout": [
            ("θ", "曲柄转角", "thetaOut", "30°"),
            ("s", "滑块位移", "sOut", "—"),
            ("H", "行程", "hOut", "—"),
            ("γ", "传动角", "gammaOut", "—"),
        ],
        "note": "偏置曲柄滑块：滑块位移 s = r cosθ + √(l² − (r sinθ − e)²)，行程 H > 2r；e = 0 时退化为对心曲柄滑块，H = 2r 且无急回。",
        "scene": "fig_3_15.js",
    },
    {
        "file": "figure-3-20.html",
        "title": "图3-20 牛头刨床导杆机构",
        "aria": "摆动导杆机构交互示意，曲柄整周回转带动导杆往复摆动",
        "subtitle": "曲柄 AB 整周回转，滑块 B 在导杆的槽中滑动，迫使导杆绕 C 往复摆动，"
        "再经滑枕把摆动变成刨刀的直线往复运动。导杆摆角 2arcsin(r/a) 决定行程与急回程度。",
        "controls": [
            ("theta", "曲柄转角 θ", 0, 360, 1, "0", "0°"),
            ("r", "曲柄半径 r", 0.70, 1.20, 0.01, "1.00", "1.00"),
        ],
        "options": [
            ("auto", "自动运转", True),
            ("showTrace", "显示铰点轨迹", True),
            ("showLabels", "显示铰点标注", True),
        ],
        "legend": [
            ("#c08a3e", "曲柄 1（AB，整周回转）"),
            ("#7c6aa8", "滑块 2（B，沿导杆滑动）"),
            ("#3f8f96", "导杆 3（绕 C 摆动）"),
            ("#8a93a3", "机架 4（AC，固定）"),
        ],
        "readout": [
            ("θ", "曲柄转角", "thetaOut", "0°"),
            ("φ", "导杆摆角", "phiOut", "—"),
            ("2ψ", "总摆角", "swingOut", "—"),
            ("K", "行程速比系数", "kOut", "—"),
        ],
        "note": "导杆摆角 2ψ = 2arcsin(r/a)（本机 a = 1.5）；行程速比系数 K = (180° + 2ψ)/(180° − 2ψ)，据此可反求曲柄半径 r = a·sinψ。",
        "scene": "fig_3_20.js",
    },
]



PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}
</style>
</head>
<body>
<main class="app">
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img" aria-label="{aria}">
  <g id="baseLayer"></g>
  <g id="traceLayer"></g>
  <g id="frameLayer"></g>
  <g id="linkLayer"></g>
  <g id="pinLayer"></g>
  <g id="labelLayer"></g>
</svg>

<section class="panel" aria-label="{title} 控制面板">
  <div class="panel-head">
    <div>
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>
{controls}
  <div class="options">
{options}
  </div>

  <div class="legend">
{legend}
  </div>
</section>

<div class="hint">拖动旋转视角 · 滚轮缩放 · 双击复位</div>

<div class="readout">
{readout}
  <div class="row"><span class="small">{note}</span></div>
</div>
</main>
<script>
{kit}
</script>
<script>
{mkit}
</script>
<script>
{parts}
</script>
<script>
{scene_js}
</script>
</body>
</html>
"""


def control_html(cid: str, label: str, lo, hi, step, value: str, shown: str) -> str:
    return f"""  <div class="control">
    <div class="control-head"><label for="{cid}">{label}</label><output id="{cid}Value">{shown}</output></div>
    <input id="{cid}" type="range" min="{lo}" max="{hi}" step="{step}" value="{value}">
  </div>"""


def build_page(spec: dict, css: str, kit: str, mkit: str, parts: str) -> str:
    controls = "\n".join(control_html(*c) for c in spec["controls"])
    options = "\n".join(
        f'    <label><input id="{oid}" type="checkbox"{" checked" if checked else ""}>{label}</label>'
        for oid, label, checked in spec["options"]
    )
    legend = "\n".join(
        f'    <span><i style="background:{color}"></i>{text}</span>' for color, text in spec["legend"]
    )
    readout = "\n".join(
        f'  <div class="row"><strong>{sym}</strong> = <span id="{rid}">{initial}</span>'
        f'　<span class="small">（{label}）</span></div>'
        for sym, label, rid, initial in spec["readout"]
    )
    scene_js = (TOOLS / spec["scene"]).read_text(encoding="utf-8")
    return PAGE.format(
        title=spec["title"],
        aria=spec["aria"],
        subtitle=spec["subtitle"],
        css=css,
        controls=controls,
        options=options,
        legend=legend,
        readout=readout,
        note=spec["note"],
        kit=kit,
        mkit=mkit,
        parts=parts,
        scene_js=scene_js,
    )


def main() -> int:
    template = TEMPLATE_PAGE.read_text(encoding="utf-8")
    match = re.search(r"<style>(.*?)</style>", template, re.S)
    if not match:
        raise SystemExit("模板页面里没找到 <style> 块")
    css = match.group(1).rstrip()
    kit = KIT_SRC.read_text(encoding="utf-8").rstrip()
    mkit = (TOOLS / "mkit.js").read_text(encoding="utf-8").rstrip()
    parts = (TOOLS / "parts.js").read_text(encoding="utf-8").rstrip()

    OUT.mkdir(parents=True, exist_ok=True)
    for spec in FIGURES:
        html = build_page(spec, css, kit, mkit, parts)
        target = OUT / spec["file"]
        target.write_text(html, encoding="utf-8")
        print(f"写入 {target.relative_to(ROOT)}　{len(html):,} 字节")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
