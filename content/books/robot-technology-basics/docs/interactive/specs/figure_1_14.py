"""图1-14 A4020 型 SCARA 机器人的工作范围
（《机器人技术基础（第三版）》1.4.1 机器人的主要技术参数 > 六、工作范围 / 七、承载能力）。

教材依据：
- 正文 1.4.1 六、工作范围：“……人和 A4020 型 SCARA 机器人的工作范围。”（图1.13 为
  MOTOMAN UP6 的俯视/主视工作范围，图1.14 为 A4020 型 SCARA 机器人的工作范围）。
- 图1.14 是一张**平面图**：图内 X 轴向上、Y 轴向左（右手系，Z 指向纸外）。
  图上标注：X 轴正方向一侧的“−30°”、大臂回转的两个极限“170°”、
  小圆弧半径“R181”、大圆弧半径“R700”，以及虚线圆半径“R300”与“155°”“2.5°”。
- 教材原文把图中两个数值写作大臂 R700、内弧 R181——本图读数区注明“教材原始数值”，
  并在图上按 700 / 181 这两个半径绘制大弧与内弧（不颠倒）。
- 运动学（平面两连杆，θ₁ 为大臂相对 X 轴的转角，θ₂ 为小臂相对大臂的转角）：
      X = l₁·cosθ₁ + l₂·cos(θ₁+θ₂)
      Y = l₁·sinθ₁ + l₂·sin(θ₁+θ₂)
  θ₂ = 0° 时末端半径 r = l₁ + l₂（全伸，最大）；θ₂ = ±180° 时 r = |l₁ − l₂|（全缩，最小）——
  脚本内以此做断言自检，并把这两个极值半径在图上标出。
- 关节限位：θ₁ ∈ [−135°, 135°]、θ₂ ∈ [−145°, 145°]（两个关节在画面上各自形成一个
  关节限位扇形；图 1.14 上的 170° 是大臂回转的极限、155°/2.5° 是内弧缺口处的
  让位角，本图把这些值原样标在图上）。

可达区域判据（读数区随参数实时判定）：
    r < 内弧半径 → 落在内弧以内的死区（< 内弧半径）
    内弧半径 ≤ r ≤ 大臂半径 → 环内
    r > 大臂半径 → 超出工作范围
自检失败直接 throw。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

CSS = COMMON_CSS + """
.readout .row { white-space: normal; }
.readout .ok { color: #15803d; font-weight: 700; }
.readout .warn { color: #b3261e; font-weight: 700; }
.readout .note { color: #b45309; font-weight: 700; }
.panel h1 { overflow-wrap: anywhere; }
/* 图例线型：虚线/点线表示“边界与限位”，避免只靠颜色区分 */
.legend i.dash { background-image: repeating-linear-gradient(90deg, #fff 0 4px, transparent 4px 8px); background-color: transparent; }
.legend i.dotline { background-image: repeating-linear-gradient(90deg, #fff 0 2px, transparent 2px 5px); background-color: transparent; }
@media (max-width: 720px) {
  .panel { padding: 9px 11px; }
  .panel h1 { font-size: 13.5px; }
  .control { margin-top: 4px; }
  .control label, .control output { font-size: 12px; }
  input[type="range"] { margin: 3px 0 0; height: 3px; }
  .options, .legend { margin-top: 6px; padding-top: 5px; gap: 4px 9px; font-size: 11px; }
  .readout { left: 8px; right: 8px; max-width: none; padding: 6px 8px; font-size: 11.5px; line-height: 1.45; }
  .readout .small { font-size: 10.5px; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1200 700" role="img"
     aria-label="A4020型SCARA机器人的平面工作范围：外弧R700、内弧R181构成的圆环扇形">
  <defs>
    <marker id="f14Dim" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="f14Dim2" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#b45309"></path>
    </marker>
    <marker id="f14X" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="f14Y" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="f14V" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
  </defs>
  <g id="f14Grid"></g>
  <g id="f14Ring"></g>
  <g id="f14Fan"></g>
  <g id="f14Dim"></g>
  <g id="f14Trail"></g>
  <g id="f14Base"></g>
  <g id="f14Arm"></g>
  <g id="f14Label"></g>
</svg>

<section class="panel" aria-label="图1-14 控制面板">
  <div class="panel-head">
    <div>
      <h1>图1-14 A4020 SCARA 的工作范围</h1>
      <p class="subtitle">平面图：X 轴向上、Y 轴向左。外弧＝大臂 R700，内弧＝小臂 R181。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="l1">大臂长度 l₁（mm）</label><output id="l1Value">700</output></div>
    <input id="l1" type="range" min="200" max="900" step="10" value="700">
  </div>
  <div class="control">
    <div class="control-head"><label for="l2">小臂长度 l₂（mm）</label><output id="l2Value">181</output></div>
    <input id="l2" type="range" min="80" max="400" step="1" value="181">
  </div>
  <div class="control">
    <div class="control-head"><label for="t1">大臂转角 θ₁（绕 Z）</label><output id="t1Value">45.0°</output></div>
    <input id="t1" type="range" min="-135" max="135" step="1" value="45">
  </div>
  <div class="control">
    <div class="control-head"><label for="t2">小臂转角 θ₂（相对大臂）</label><output id="t2Value">0.0°</output></div>
    <input id="t2" type="range" min="-145" max="145" step="1" value="0">
  </div>

  <div class="options">
    <label><input id="showRing" type="checkbox" checked>显示可达区域</label>
    <label><input id="showFan" type="checkbox" checked>显示关节限位扇形</label>
    <label><input id="showTrail" type="checkbox" checked>显示末端轨迹</label>
    <label><input id="showR300" type="checkbox" checked>显示 R300 虚线圆与 155°/2.5° 让位角</label>
    <label><input id="sweep" type="checkbox">自动扫掠 θ₁ / θ₂</label>
  </div>

  <div class="legend">
    <span><i style="background:#2563eb"></i>外弧 r = l₁ = 700（实线）</span>
    <span><i style="background:#0e7490"></i>内弧 r = l₂ = 181（实线）</span>
    <span><i class="dash" style="background:#7c3aed"></i>θ₁ 极限 170° / 关节限位扇形</span>
    <span><i class="dotline" style="background:#b45309"></i>R300 虚线圆（155° / 2.5° 让位角）</span>
    <span><i style="background:#475569"></i>两连杆构型（实心）</span>
    <span><i class="dot" style="background:#c26a10"></i>末端点 T</span>
  </div>
</section>

<div class="hint">拖动平移 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row"><strong>末端 T</strong> = ( X = <span id="txOut">700.0</span>, Y = <span id="tyOut">0.0</span> ) mm
    <span class="small">（图内 X 向上、Y 向左）</span></div>
  <div class="row"><strong>末端半径 r</strong> = <span id="rOut">700.0</span> mm
    <span class="small">｜ 大臂半径 l₁ = <span id="r1Out">700</span> mm，内弧半径 l₂ = <span id="r2Out">181</span> mm</span></div>
  <div class="row" id="zoneRow">所处区间：环内</div>
  <div class="row small" id="extRow">极值半径：θ₂=0° → l₁+l₂ = <span id="rSumOut">881</span> mm（最大）；θ₂=±180° → |l₁−l₂| = <span id="rDifOut">519</span> mm（最小）</div>
  <div class="row small note" id="bookRow">教材原始数值（图1.14）：大臂 R700、内弧 R181；图上另有 R300 虚线圆与 155°、2.5° 让位角。</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var L = {
    grid: document.getElementById("f14Grid"),
    ring: document.getElementById("f14Ring"),
    fan: document.getElementById("f14Fan"),
    dim: document.getElementById("f14Dim"),
    trail: document.getElementById("f14Trail"),
    base: document.getElementById("f14Base"),
    arm: document.getElementById("f14Arm"),
    label: document.getElementById("f14Label")
  };

  var scene = new FK.Scene({
    svg: viewport, origin: { x: 700, y: 360 }, scale: 0.30,
    yaw: 0, pitch: 0, minScale: 0.06, maxScale: 1.6
  });

  var DEFAULTS = { l1: 700, l2: 181, t1: 45, t2: 0 };
  var state = {
    l1: DEFAULTS.l1, l2: DEFAULTS.l2, t1: DEFAULTS.t1, t2: DEFAULTS.t2,
    showRing: true, showFan: true, showTrail: true, showR300: true, sweep: false, compact: false
  };

  // 教材图1.14 上标注的角度（原样显示，供对照）
  var BOOK = { outerLimit: 170, gapSmall: 155, gapMin: 2.5, rDash: 300, t1Top: -30 };

  var pan = { x: 0, y: 0, id: null, lx: 0, ly: 0 };
  var trail = [];
  var sweep = { frame: 0, dir: 1 };

  /* 平面投影：世界 X 在屏幕向上，世界 Y 在屏幕向左（与图1.14 一致） */
  function proj(v) {
    var s = scene.state.scale;
    return {
      x: scene.baseOrigin.x + pan.x - v[1] * s,
      y: scene.baseOrigin.y + pan.y - v[0] * s,
      depth: 0
    };
  }

  /** 自适应取景：viewBox 与视口像素 1:1；state 已在 fit() 首次调用之前声明。 */
  function fit() {
    var rect = viewport.getBoundingClientRect();
    var W = Math.max(260, Math.round(rect.width || 1200));
    var H = Math.max(260, Math.round(rect.height || 700));
    viewport.setAttribute("viewBox", "0 0 " + W + " " + H);
    viewport.setAttribute("preserveAspectRatio", "xMidYMid meet");
    var narrow = W < 720;
    var availW = W * (narrow ? 0.94 : 0.50);
    var availH = H * (narrow ? 0.50 : 0.78);
    var span = Math.max(1, state.l1 + state.l2 + 150);
    var k = Math.min(availW / (2.05 * span), availH / (narrow ? 1.85 : 2.15) / span);
    scene.state.scale = Math.max(0.06, Math.min(1.6, k));
    scene.defaults.scale = scene.state.scale;
    state.compact = scene.state.scale * span < 120;
    scene.baseOrigin.x = W * (narrow ? 0.5 : 0.46);
    scene.baseOrigin.y = H * (narrow ? 0.30 : 0.40);
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  var C = {
    outer: "#2563eb", inner: "#0e7490", fan: "#7c3aed", dash: "#b45309",
    link: "#475569", link2: "#64748b", joint: "#1e293b", tip: "#c26a10",
    trail: "#c26a10", axisX: "#d93025", axisY: "#2563eb", work: "#93a6bf"
  };

  /* ------------------------------------------------------------ 运动学 */

  /** 平面两连杆 FK（X 向上、Y 向左的教材平面） */
  function fk(l1, l2, t1Deg, t2Deg) {
    var t1 = t1Deg * FK.DEG, t2 = t2Deg * FK.DEG;
    var elbow = [l1 * Math.cos(t1), l1 * Math.sin(t1)];
    var tip = [elbow[0] + l2 * Math.cos(t1 + t2), elbow[1] + l2 * Math.sin(t1 + t2)];
    return { elbow: elbow, tip: tip };
  }
  /** r(θ₂) = √(l₁² + l₂² + 2l₁l₂cosθ₂) 的解析式 */
  function radiusAnalytic(l1, l2, t2Deg) {
    return Math.sqrt(l1 * l1 + l2 * l2 + 2 * l1 * l2 * Math.cos(t2Deg * FK.DEG));
  }

  /* ------------------------------------------------------------ 绘图辅助 */

  function sp(r, angRad) { return [r * Math.cos(angRad), r * Math.sin(angRad), 0]; }
  /** 以 (cx, cy) 为圆心、半径 r、从 a0 扫到 a1 的圆弧路径（默认圆心为机座原点） */
  function ptPath(r, a0, a1, n, cx, cy) {
    var ox = cx === undefined ? 0 : cx, oy = cy === undefined ? 0 : cy;
    var d = "", i, a, p;
    for (i = 0; i <= n; i += 1) {
      a = a0 + (a1 - a0) * i / n;
      p = proj([ox + r * Math.cos(a), oy + r * Math.sin(a), 0]);
      d += (i === 0 ? "M " : " L ") + p.x.toFixed(2) + " " + p.y.toFixed(2);
    }
    return d;
  }
  function annulusPath(rout, rin, a0, a1) {
    if (rout <= 1e-6) return "";
    var d = ptPath(rout, a0, a1, 72), i, a;
    for (i = 72; i >= 0; i -= 1) {
      a = a0 + (a1 - a0) * i / 72;
      var p = proj(sp(Math.max(rin, 0), a));
      d += " L " + p.x.toFixed(2) + " " + p.y.toFixed(2);
    }
    return d + " Z";
  }
  function arc(r, a0, a1, attrs, layer, n) {
    return scene.el("path", Object.assign({
      d: ptPath(r, a0, a1, n === undefined ? 72 : n), fill: "none"
    }, attrs || {}), layer);
  }
  function seg(a, b, attrs, layer) {
    var p = proj(a), q = proj(b);
    return scene.el("line", Object.assign({ x1: p.x, y1: p.y, x2: q.x, y2: q.y }, attrs || {}), layer);
  }
  function tag(v, str, attrs, dx, dy, layer) {
    var p = proj(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0), "font-size": 14,
      "font-weight": 700, class: "fk-axis-label"
    }, attrs || {}), layer);
    node.textContent = str;
    return node;
  }
  function dimLine(a, b, offX, offY, text, color, marker) {
    var A = proj(a), B = proj(b);
    var ax = A.x + offX, ay = A.y + offY, bx = B.x + offX, by = B.y + offY;
    scene.el("line", {
      x1: ax, y1: ay, x2: bx, y2: by, stroke: color, "stroke-width": 1.6,
      "marker-start": "url(#" + marker + ")", "marker-end": "url(#" + marker + ")"
    }, L.dim);
    var t = scene.el("text", {
      x: (ax + bx) / 2, y: (ay + by) / 2 - 7, "text-anchor": "middle",
      fill: color, "font-size": 13.5, "font-weight": 700, class: "fk-axis-label"
    }, L.dim);
    t.textContent = text;
  }
  /** 关节限位扇形（θ 范围）：圆心可在肘关节，画圆弧 + 两条限位边线 */
  function jointFan(cx, cy, r, a0Deg, a1Deg, color) {
    var a0 = a0Deg * FK.DEG, a1 = a1Deg * FK.DEG;
    scene.el("path", {
      d: ptPath(r, a0, a1, 64, cx, cy), fill: "none",
      stroke: color, "stroke-width": 2, "stroke-dasharray": "7 6"
    }, L.fan);
    seg([cx, cy, 0], [cx + r * Math.cos(a0), cy + r * Math.sin(a0), 0],
      { stroke: color, "stroke-width": 1.3, "stroke-dasharray": "5 6" }, L.fan);
    seg([cx, cy, 0], [cx + r * Math.cos(a1), cy + r * Math.sin(a1), 0],
      { stroke: color, "stroke-width": 1.3, "stroke-dasharray": "5 6" }, L.fan);
  }

  /* -------------------------------------------------------------- 绘制 */

  function drawGrid(span) {
    var g = scene.el("g", { class: "fk-grid" }, L.grid);
    var step = 100, i;
    for (i = -Math.ceil(span / step); i <= Math.ceil(span / step); i += 1) {
      var p = proj([i * step, -span, 0]), q = proj([i * step, span, 0]);
      scene.el("line", { x1: p.x, y1: p.y, x2: q.x, y2: q.y, class: "fk-grid-line" }, g);
      var p2 = proj([-span, i * step, 0]), q2 = proj([span, i * step, 0]);
      scene.el("line", { x1: p2.x, y1: p2.y, x2: q2.x, y2: q2.y, class: "fk-grid-line" }, g);
    }
  }

  function drawAxes(span) {
    var ax = [span, 0, 0], ay = [0, span, 0];
    seg([-0.35 * span, 0, 0], ax, { stroke: C.axisX, "stroke-width": 3, "marker-end": "url(#f14X)" }, L.label);
    seg([0, -0.35 * span, 0], ay, { stroke: C.axisY, "stroke-width": 3, "marker-end": "url(#f14Y)" }, L.label);
    tag(ax, "X", { fill: C.axisX, "font-size": 18, "font-style": "italic" }, -6, -10, L.label);
    tag(ay, "Y", { fill: C.axisY, "font-size": 18, "font-style": "italic" }, 14, 4, L.label);
    var o = proj([0, 0, 0]);
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.4, fill: "#334155" }, L.label);
    var t = scene.el("text", { x: o.x + 10, y: o.y + 20, class: "fk-origin-label" }, L.label);
    t.textContent = "O（机座）";
  }

  /** 工作范围：外弧 l₁、内弧 l₂、θ₁ 极限 170°、R300 虚线圆与 155°/2.5° 让位角 */
  function drawWorkspace(l1, l2, t1Deg) {
    var a1 = t1Deg * FK.DEG;
    var lim = BOOK.outerLimit * FK.DEG;
    var rout = l1, rin = l2;
    var i, k, a;

    if (state.showRing) {
      // 1) 整体可达环（圆环扇形）：内弧 l₂ 到外弧 l₁
      scene.el("path", {
        d: annulusPath(rout, rin, -Math.PI, Math.PI), "fill-rule": "evenodd",
        fill: "rgba(37, 99, 235, 0.08)", stroke: "none"
      }, L.ring);
      // 2) 挖掉 θ₁ 超出 ±170° 的两个楔形（约 ±10°），这就是“扇形”而不是整圆环的原因
      for (i = 0; i < 2; i += 1) {
        var s = i === 0 ? lim : Math.PI;
        var e = i === 0 ? Math.PI : 2 * Math.PI - lim;
        scene.el("path", {
          d: annulusPath(rout, rin, s, e), "fill-rule": "evenodd",
          fill: "rgba(255, 255, 255, 0.96)", stroke: "none"
        }, L.ring);
        // 楔形边线（θ₁ 的两个极限）
        var aa = i === 0 ? lim : -lim;
        seg([0, 0, 0], [rout * Math.cos(aa), rout * Math.sin(aa), 0],
          { stroke: C.fan, "stroke-width": 2, "stroke-dasharray": "9 6" }, L.ring);
      }
      // 3) 外弧（大臂半径 R700）与内弧（小臂半径 R181）—— 实线
      arc(rout, -lim, lim, { stroke: C.outer, "stroke-width": 2.8 }, L.ring, 140);
      arc(rin, -lim, lim, { stroke: C.inner, "stroke-width": 2.8 }, L.ring, 140);
      tag([rout * Math.cos(lim) * 0.99, rout * Math.sin(lim) * 0.99, 0], "170°（θ₁ 极限）",
        { fill: C.fan, "font-size": 13 }, 6, -10, L.ring);
      tag([rout * Math.cos(-lim) * 0.99, rout * Math.sin(-lim) * 0.99, 0], "170°（θ₁ 极限）",
        { fill: C.fan, "font-size": 13 }, 6, 18, L.ring);
      // 内外弧半径标注：放在 140° / 145° 方向、弧线外侧，避开连杆与机座
      tag([rout * 1.02 * Math.cos(140 * FK.DEG), rout * 1.02 * Math.sin(140 * FK.DEG), 0],
        "外弧 = 大臂半径 l₁ = " + FK.format(rout, 0) + " mm",
        { fill: C.outer, "font-size": 13.5 }, -10, -8, L.ring);
      tag([rin * 6.6 * Math.cos(145 * FK.DEG), rin * 6.6 * Math.sin(145 * FK.DEG), 0],
        "内弧 = 小臂半径 l₂ = " + FK.format(rin, 0) + " mm",
        { fill: C.inner, "font-size": 13.5 }, -10, 20, L.ring);
    }
    // 4) 当前 θ₁ 方向与 θ₁ 扇形角
    seg([0, 0, 0], [rout * 1.03 * Math.cos(a1), rout * 1.03 * Math.sin(a1), 0],
      { stroke: "#94a3b8", "stroke-width": 1.2, "stroke-dasharray": "4 5" }, L.ring);
    arc(rout * 0.30, 0, a1, { stroke: "#0e7490", "stroke-width": 2.4, "stroke-dasharray": "6 5" }, L.ring, 48);
    tag([rout * 0.36 * Math.cos(a1 * 0.5), rout * 0.36 * Math.sin(a1 * 0.5), 0],
      "θ₁ = " + FK.format(t1Deg, 1) + "\u00b0", { fill: "#0e7490", "font-size": 13.5 }, 0, 5, L.ring);

    if (state.showR300) {
      // 教材图1.14 上的两条 R300 虚线圆：分别位于 X 轴两侧，
      // 表示小臂绕肘关节回转时末端的轨迹范围（半径 R300），并标出 155° 与 2.5° 让位角。
      var t1v = -BOOK.t1Top * FK.DEG;            // 30°，与图1.14 的 −30° 标注对应
      var cx = l1 * Math.cos(t1v), cy = l1 * Math.sin(t1v);
      for (i = 0; i < 2; i += 1) {
        var sign = i === 0 ? 1 : -1;
        var ox = cx, oy = sign * cy;
        scene.el("path", {
          d: ptPath(BOOK.rDash, 0, 2 * Math.PI, 140, ox, oy), fill: "none",
          stroke: C.dash, "stroke-width": 1.5, "stroke-dasharray": "2 6"
        }, L.ring);
        tag([ox, oy, 0], "R" + BOOK.rDash + " 虚线圆（小臂回转 155°）",
          { fill: C.dash, "font-size": 12 }, 10, sign > 0 ? -6 : 18, L.ring);
        // 155° 让位角：自肘关节沿远离机座方向展开
        var af = (180 - BOOK.gapSmall) * FK.DEG * sign;
        seg([ox, oy, 0], [ox + l2 * Math.cos(af), oy + l2 * Math.sin(af), 0],
          { stroke: C.dash, "stroke-width": 1.2, "stroke-dasharray": "4 5" }, L.ring);
        tag([ox + l2 * 0.72 * Math.cos(af * 0.5), oy + l2 * 0.72 * Math.sin(af * 0.5), 0],
          "155°", { fill: C.dash, "font-size": 13 }, 6, sign > 0 ? 0 : 14, L.ring);
        // 2.5° 让位角：R300 圆内侧与 X 轴之间的空隙
        var ag = Math.PI * sign * 0.5;
        seg([ox, oy, 0], [ox + BOOK.rDash * 0.94 * Math.cos(ag), oy + BOOK.rDash * 0.94 * Math.sin(ag), 0],
          { stroke: C.dash, "stroke-width": 1.1, "stroke-dasharray": "3 5" }, L.ring);
        tag([ox + BOOK.rDash * 1.14 * Math.cos(ag), oy + BOOK.rDash * 1.14 * Math.sin(ag), 0],
          BOOK.gapMin + "°", { fill: C.dash, "font-size": 12 }, 4, sign > 0 ? 14 : 0, L.ring);
      }
      // 图1.14 上的 −30° 标注（X 轴正方向一侧）
      var ta = BOOK.t1Top * FK.DEG;
      seg([0, 0, 0], [l1 * 1.06 * Math.cos(ta), l1 * 1.06 * Math.sin(ta), 0],
        { stroke: "#94a3b8", "stroke-width": 1.2 }, L.ring);
      tag([l1 * 1.06 * Math.cos(ta), l1 * 1.06 * Math.sin(ta), 0],
        BOOK.t1Top + "\u00b0", { fill: "#64748b", "font-size": 12.5 }, 4, -10, L.ring);
    }

    if (state.showFan) {
      // θ₁ 的关节限位扇形（以机座为圆心，±135°）
      arc(l1 * 0.985, -135 * FK.DEG, 135 * FK.DEG,
        { stroke: C.fan, "stroke-width": 1.6, "stroke-dasharray": "4 6", opacity: 0.85 }, L.fan, 96);
      // θ₂ 的关节限位扇形（以小臂回转中心为圆心，随构型移动）
      var K = fk(l1, l2, t1Deg, 0);
      jointFan(K.elbow[0], K.elbow[1], Math.max(l2 * 0.42, 70), -145, 145, "#0e7490");
      tag([K.elbow[0] - l2 * 0.5, K.elbow[1] + l2 * 0.5, 0], "θ₂ 限位 ±145°",
        { fill: "#0e7490", "font-size": 12.5 }, 8, -10, L.fan);
    }
  }

  /** 极值半径与外/内弧半径标注 */
  function drawDims(l1, l2) {
    var D1 = 208 * FK.DEG;          // 外弧半径尺寸线方向（避开读数卡）
    var D2 = 238 * FK.DEG;
    seg([0, 0, 0], [l1 * Math.cos(D1), l1 * Math.sin(D1), 0],
      { stroke: C.outer, "stroke-width": 1.3, "stroke-dasharray": "6 5" }, L.dim);
    dimLine([0, 0, 0], [l1 * Math.cos(D1), l1 * Math.sin(D1), 0], 0, -16,
      "大臂半径 l₁ = " + FK.format(l1, 0), C.outer, "f14Dim");
    seg([0, 0, 0], [l2 * Math.cos(D2), l2 * Math.sin(D2), 0],
      { stroke: C.inner, "stroke-width": 1.3, "stroke-dasharray": "6 5" }, L.dim);
    dimLine([0, 0, 0], [l2 * Math.cos(D2), l2 * Math.sin(D2), 0], 16, 12,
      "内弧半径 l₂ = " + FK.format(l2, 0), C.inner, "f14Dim2");
    // 极值半径（θ₂ = 0 / ±180°）用虚线圆标出
    arc(l1 + l2, 0, 2 * Math.PI, { stroke: C.outer, "stroke-width": 1.2, "stroke-dasharray": "2 7", opacity: 0.8 }, L.dim, 160);
    arc(Math.abs(l1 - l2), 0, 2 * Math.PI, { stroke: C.inner, "stroke-width": 1.2, "stroke-dasharray": "2 7", opacity: 0.8 }, L.dim, 160);
    tag([0, l1 + l2, 0], "θ₂=0° → r = l₁+l₂ = " + FK.format(l1 + l2, 0) + " mm（最大）",
      { fill: C.outer, "font-size": 12.5 }, 10, -6, L.dim);
    tag([0, Math.abs(l1 - l2), 0], "θ₂=±180° → r = |l₁−l₂| = " + FK.format(Math.abs(l1 - l2), 0) + " mm（最小）",
      { fill: C.inner, "font-size": 12.5 }, 10, 16, L.dim);
  }

  function drawBase() {
    // 机座简图（俯视：矩形 + 两个安装孔），沿 Y 方向较长
    var w = 190, h = 120;
    var c0 = proj([-h / 2, -w / 2, 0]), c1 = proj([h / 2, w / 2, 0]);
    var x0 = Math.min(c0.x, c1.x), y0 = Math.min(c0.y, c1.y);
    scene.el("rect", {
      x: x0, y: y0, width: Math.abs(c1.x - c0.x), height: Math.abs(c1.y - c0.y), rx: 6,
      fill: "#eef2f7", stroke: C.joint, "stroke-width": 2.2
    }, L.base);
    var i;
    for (i = -1; i <= 1; i += 2) {
      var p = proj([0, i * (w / 2 + 26), 0]);
      scene.el("circle", { cx: p.x, cy: p.y, r: 7, fill: "#fff", stroke: C.joint, "stroke-width": 2 }, L.base);
    }
  }

  /** 两连杆构型 + 末端点（实心连杆，示意臂厚） */
  function drawArm(l1, l2, t1Deg, t2Deg) {
    function thickSeg(a, b, t, fill, stroke) {
      var dx = b[0] - a[0], dy = b[1] - a[1];
      var len = Math.hypot(dx, dy) || 1;
      var nx = -dy / len * t / 2, ny = dx / len * t / 2;
      var P = [[a[0] + nx, a[1] + ny], [b[0] + nx, b[1] + ny],
        [b[0] - nx, b[1] - ny], [a[0] - nx, a[1] - ny]];
      var d = "", i, q;
      for (i = 0; i < 4; i += 1) {
        q = proj([P[i][0], P[i][1], 0]);
        d += (i === 0 ? "M " : " L ") + q.x.toFixed(2) + " " + q.y.toFixed(2);
      }
      scene.el("path", { d: d + " Z", fill: fill, stroke: stroke, "stroke-width": 1.4 }, L.arm);
    }

    var K = fk(l1, l2, t1Deg, t2Deg);
    var O = [0, 0], E = K.elbow, T = K.tip;
    drawBase();
    thickSeg(O, E, Math.max(16, l1 * 0.055), C.link, "#2b3a52");
    thickSeg(E, T, Math.max(12, l2 * 0.16), C.link2, "#3f4c5e");

    // 关节
    var o = proj([0, 0, 0]);
    scene.el("circle", { cx: o.x, cy: o.y, r: 9, fill: "#fff", stroke: C.joint, "stroke-width": 3 }, L.arm);
    var e = proj(E);
    scene.el("circle", { cx: e.x, cy: e.y, r: 8, fill: "#fff", stroke: C.joint, "stroke-width": 3 }, L.arm);
    // 末端点与矢量
    var t = proj(T);
    seg([0, 0, 0], [T[0], T[1], 0], { stroke: C.tip, "stroke-width": 2.4, "marker-end": "url(#f14V)" }, L.arm);
    scene.el("circle", { cx: t.x, cy: t.y, r: 7, fill: C.tip, stroke: "#fff", "stroke-width": 2.2, class: "fk-point" }, L.arm);
    tag(T, "T", { fill: "#8a4a08", "font-size": 17 }, 12, -12, L.arm);
    tag([l1 * 0.5 * Math.cos(t1Deg * FK.DEG), l1 * 0.5 * Math.sin(t1Deg * FK.DEG), 0],
      "l₁", { fill: "#334155", "font-size": 14 }, -6, -10, L.arm);
    var tm = (t1Deg + t2Deg * 0.5) * FK.DEG;
    tag([E[0] + l2 * 0.5 * Math.cos(tm), E[1] + l2 * 0.5 * Math.sin(tm), 0],
      "l₂", { fill: "#334155", "font-size": 14 }, 10, -8, L.arm);
    return T;
  }

  /* -------------------------------------------------------------- 渲染 */

  function render() {
    var k, key;
    for (key in L) {
      if (Object.prototype.hasOwnProperty.call(L, key)) L[key].replaceChildren();
    }

    var l1 = state.l1, l2 = state.l2;
    var span = l1 + l2 + 160;

    drawGrid(span);
    drawWorkspace(l1, l2, state.t1);
    drawDims(l1, l2);
    drawAxes(span * 0.86);

    var T = drawArm(l1, l2, state.t1, state.t2);

    // 末端轨迹
    if (state.showTrail) {
      var r = Math.hypot(T[0], T[1]);
      var last = trail[trail.length - 1];
      if (!last || Math.hypot(r - last[0], Math.atan2(T[1], T[0]) - last[1]) > 0.004) {
        trail.push([r, Math.atan2(T[1], T[0])]);
        if (trail.length > 3000) trail.shift();
      }
      if (trail.length > 1) {
        var d = "", i, p;
        for (i = 0; i < trail.length; i += 1) {
          p = proj([trail[i][0] * Math.cos(trail[i][1]), trail[i][0] * Math.sin(trail[i][1]), 0]);
          d += (i === 0 ? "M " : " L ") + p.x.toFixed(2) + " " + p.y.toFixed(2);
        }
        scene.el("path", { d: d, fill: "none", stroke: C.trail, "stroke-width": 2.6, opacity: 0.85 }, L.trail);
      }
    }

    /* ------------------------------------------------------------ 读数 */
    var rr = Math.hypot(T[0], T[1]);
    document.getElementById("txOut").textContent = FK.format(T[0], 1);
    document.getElementById("tyOut").textContent = FK.format(T[1], 1);
    document.getElementById("rOut").textContent = FK.format(rr, 1);
    document.getElementById("r1Out").textContent = FK.format(l1, 0);
    document.getElementById("r2Out").textContent = FK.format(l2, 0);
    document.getElementById("rSumOut").textContent = FK.format(l1 + l2, 0);
    document.getElementById("rDifOut").textContent = FK.format(Math.abs(l1 - l2), 0);
    document.getElementById("l1Value").textContent = FK.format(l1, 0);
    document.getElementById("l2Value").textContent = FK.format(l2, 0);

    var zone = document.getElementById("zoneRow");
    var rin = Math.min(l1, l2), rout = Math.max(l1, l2);
    if (rr < rin - 1e-6) {
      zone.className = "row warn";
      zone.textContent = "所处区间：<内弧半径（" + FK.format(rr, 1) + " mm < " + FK.format(rin, 0)
        + " mm）——落在内弧以内的不可达死区；超出工作范围";
    } else if (rr > rout + 1e-6) {
      zone.className = "row warn";
      zone.textContent = "所处区间：>外弧半径（" + FK.format(rr, 1) + " mm > " + FK.format(rout, 0)
        + " mm）——超出工作范围";
    } else {
      zone.className = "row ok";
      zone.textContent = "所处区间：环内（" + FK.format(rin, 0) + " mm ≤ r = " + FK.format(rr, 1)
        + " mm ≤ " + FK.format(rout, 0) + " mm）——在工作范围内";
    }
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "l1", key: "l1", value: DEFAULTS.l1, format: function (v) { return FK.format(v, 0); }, onChange: function () { trail = []; } },
    { id: "l2", key: "l2", value: DEFAULTS.l2, format: function (v) { return FK.format(v, 0); }, onChange: function () { trail = []; } },
    { id: "t1", key: "t1", value: DEFAULTS.t1, format: function (v) { return FK.deg(v, 1); } },
    { id: "t2", key: "t2", value: DEFAULTS.t2, format: function (v) { return FK.deg(v, 1); } }
  ], state, render);

  FK.bindToggles([
    { id: "showRing", key: "showRing" },
    { id: "showFan", key: "showFan" },
    { id: "showTrail", key: "showTrail" },
    { id: "showR300", key: "showR300" },
    {
      id: "sweep", key: "sweep", onChange: function (v) {
        if (v && !sweep.frame) sweep.frame = requestAnimationFrame(sweepTick);
      }
    }
  ], state, render);

  function sweepTick() {
    sweep.frame = 0;
    if (!state.sweep) return;
    state.t2 += 2.6 * sweep.dir;
    if (state.t2 >= 145) { state.t2 = 145; sweep.dir = -1; }
    if (state.t2 <= -145) { state.t2 = -145; sweep.dir = 1; }
    state.t1 += 0.6;
    if (state.t1 > 135) state.t1 -= 270;
    document.getElementById("t1").value = state.t1;
    document.getElementById("t2").value = state.t2;
    document.getElementById("t1Value").textContent = FK.deg(state.t1, 1);
    document.getElementById("t2Value").textContent = FK.deg(state.t2, 1);
    render();
    sweep.frame = requestAnimationFrame(sweepTick);
  }

  document.getElementById("reset").addEventListener("click", function () {
    state.l1 = DEFAULTS.l1;
    state.l2 = DEFAULTS.l2;
    state.t1 = DEFAULTS.t1;
    state.t2 = DEFAULTS.t2;
    state.showRing = true;
    state.showFan = true;
    state.showTrail = true;
    state.showR300 = true;
    state.sweep = false;
    document.getElementById("showRing").checked = true;
    document.getElementById("showFan").checked = true;
    document.getElementById("showTrail").checked = true;
    document.getElementById("showR300").checked = true;
    document.getElementById("sweep").checked = false;
    trail = [];
    pan.x = 0; pan.y = 0;
    ranges.refresh();
    scene.reset();
    fit();
    render();
  });

  /* 拖动平移（平面图不使用三维旋转） */
  viewport.addEventListener("pointerdown", function (event) {
    if (pan.id !== null) return;
    pan.id = event.pointerId; pan.lx = event.clientX; pan.ly = event.clientY;
    try { viewport.setPointerCapture(event.pointerId); } catch (e) { /* 忽略 */ }
  });
  viewport.addEventListener("pointermove", function (event) {
    if (pan.id === null || event.pointerId !== pan.id) return;
    pan.x += event.clientX - pan.lx;
    pan.y += event.clientY - pan.ly;
    pan.lx = event.clientX; pan.ly = event.clientY;
    render();
  });
  function endPan(event) {
    if (event && pan.id !== null && event.pointerId !== pan.id) return;
    pan.id = null;
  }
  viewport.addEventListener("pointerup", endPan);
  viewport.addEventListener("pointercancel", endPan);
  viewport.addEventListener("lostpointercapture", endPan);
  viewport.addEventListener("dblclick", function () {
    pan.x = 0; pan.y = 0;
    // FK.Scene 的双击处理器会复位缩放，这里重新取景以保持一致
    fit();
    render();
  });
  window.addEventListener("resize", function () { fit(); render(); });
  window.addEventListener("load", function () { fit(); render(); });

  // 滚轮缩放：FK.Scene 只改 state.scale，本项目用 baseOrigin 定位，需要重绘
  viewport.addEventListener("wheel", function () { requestAnimationFrame(render); }, { passive: true });

  /* --------------------------------------------------------------- 自检 */
  (function selfTest() {
    function close(a, b, eps) { return Math.abs(a - b) < (eps === undefined ? 1e-9 : eps); }
    var L1 = 700, L2 = 181;

    // 1) θ₂ = 0° → 末端半径 = 大臂 + 小臂
    var k1 = fk(L1, L2, 37, 0);
    if (!close(Math.hypot(k1.tip[0], k1.tip[1]), L1 + L2, 1e-9)) {
      throw new Error("图1-14 自检失败：θ₂=0 时末端半径应为 l₁+l₂ = 881");
    }
    // 2) θ₂ = ±180° → 末端半径 = |大臂 − 小臂|
    var k2 = fk(L1, L2, -122, 180);
    if (!close(Math.hypot(k2.tip[0], k2.tip[1]), Math.abs(L1 - L2), 1e-9)) {
      throw new Error("图1-14 自检失败：θ₂=180° 时末端半径应为 |l₁−l₂| = 519");
    }
    var k2b = fk(L1, L2, 88, -180);
    if (!close(Math.hypot(k2b.tip[0], k2b.tip[1]), Math.abs(L1 - L2), 1e-9)) {
      throw new Error("图1-14 自检失败：θ₂=−180° 时末端半径应为 |l₁−l₂| = 519");
    }
    // 3) 解析式 r(θ₂) = √(l₁²+l₂²+2l₁l₂cosθ₂) 与运动学一致，且极值为 881 / 519
    var mn = Infinity, mx = -Infinity, i, r;
    for (i = 0; i <= 720; i += 1) {
      var th = i * 0.5 - 180;
      var kk = fk(L1, L2, 0.7, th);
      r = Math.hypot(kk.tip[0], kk.tip[1]);
      if (Math.abs(r - radiusAnalytic(L1, L2, th)) > 1e-9) {
        throw new Error("图1-14 自检失败：|OT| 解析式不一致 @θ₂=" + th);
      }
      if (r < mn) mn = r;
      if (r > mx) mx = r;
    }
    if (!close(mx, L1 + L2, 1e-6) || !close(mn, Math.abs(L1 - L2), 1e-6)) {
      throw new Error("图1-14 自检失败：扫掠极值应为 [519, 881]，实得 [" + mn + ", " + mx + "]");
    }
    // 4) 教材数值区间：R181 ≤ r ≤ R700 是可达环；默认参数（θ₁=45°、θ₂=0）下 r = 881 超出 R700
    if (!(L2 <= L1)) throw new Error("图1-14 自检失败：内弧半径应不大于外弧半径");
    if (!(70 < L2 && L2 < L1)) throw new Error("图1-14 自检失败：教材数值 R181/R700 应满足 内弧 < 外弧");
    var rOut = Math.hypot(fk(L1, L2, 45, 0).tip[0], fk(L1, L2, 45, 0).tip[1]);
    if (rOut <= L1) throw new Error("图1-14 自检失败：默认构型（θ₂=0）应超出 R700 外弧");
    // 5) θ₂=0 时小臂与大臂共线（肘关节在 l₁ 方向上）
    var ke = fk(L1, L2, 45, 0);
    var cr = ke.elbow[0], ci = ke.elbow[1];
    if (!close(ci, cr * Math.tan(45 * FK.DEG), 1e-9)) {
      throw new Error("图1-14 自检失败：θ₂=0 时两连杆应共线");
    }
    // 6) 关节限位内可达：θ₁=±135°、θ₂=±145° 的末端都在 [|l₁−l₂|, l₁+l₂] 内
    var lim = [[135, 145], [-135, -145], [135, -145], [-135, 145]];
    for (i = 0; i < lim.length; i += 1) {
      var kl = fk(L1, L2, lim[i][0], lim[i][1]);
      var rl = Math.hypot(kl.tip[0], kl.tip[1]);
      if (rl < Math.abs(L1 - L2) - 1e-6 || rl > L1 + L2 + 1e-6) {
        throw new Error("图1-14 自检失败：限位角落点越界 @case" + i);
      }
    }
  }());

  fit();
  render();
}());
"""

FIGURE = {
    "id": "figure-1-14",
    "title": "图1-14 A4020型SCARA机器人的工作范围（外弧R700·内弧R181） · 人机交互演示",
    "css": CSS,
    "body": BODY,
    "script": SCRIPT,
}
