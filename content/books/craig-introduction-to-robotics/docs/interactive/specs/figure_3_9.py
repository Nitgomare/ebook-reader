"""图3-9 包含一个移动关节的三自由度操作臂（克雷格《机器人学导论（第3版）》例3.4，RPR 柱坐标臂）。

教材依据：
- 例3.4：关节轴 1 与轴 2 垂直；关节变量为 θ₁（绕轴1 转动）、d₂（沿轴2 移动）、θ₃（绕末端轴转动）；
  连杆参数 α₁ = 90°、d₁ = 0（表里其余 a、α 中只有 α₁ 非零，d₁ = 0 说明两轴相交）。
- 教材原文（图3-9 之后）：“注意到在该图中机器人所处的位置 , 所以坐标系 和坐标系 在图中完全重合。
  注意，坐标系 {0} 虽然没有建在机器人法兰基座的最底部，但仍然刚性地固连于连杆0上……”
  → 本图把 {0} 建在两关节轴的交点处（例3.4 里 d₁ = 0 正是“两轴相交”）。
- 正运动学（按教材“先绕 Z 转 θ₁、再沿新的水平轴移动 d₂、最后绕新轴转 θ₃”的约定）：
      ¹₀T = R_Z(θ₁)·R_X(90°)·D_X(d₂)  →  末端在 {0} 中：
      x = d₂·cosθ₁ ,   y = d₂·sinθ₁ ,   z = 0
  末端高度恒为 0（柱坐标臂只在水平面内伸缩），位置与 θ₃ 无关——θ₃ 只改变末端姿态。
  脚本用 FK.M4.chain 逐项连乘，并与上面的解析式逐点比对。

脚本内自检：
1) d₂ = 0 且 θ₁ = θ₃ = 0 → 末端 = 轴交点 O（{0} 原点），z = 0；
2) 与教材例3.4 的 (θ₁, d₂, θ₃) = (90°, 0.8, 0°) → 末端 = (0, 0.8, 0)（满足 x²+y² = d₂²）；
3) 末端到 {0} 原点的距离恒为 d₂（与 θ₁、θ₃ 无关）；
4) θ₃ 改变不影响末端位置（移动关节 + 末端旋转关节的退化特征）；
5) 两关节轴垂直：轴1 方向 = Ẑ₀，轴2 方向 = (cosθ₁, sinθ₁, 0)，点乘恒为 0。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.control-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px 10px; margin-top: 8px; }
.control-grid .control { margin-top: 2px; min-width: 0; }
.control-grid .control-head { display: block; line-height: 1.3; }
.control-grid .control-head output { display: block; font-size: 11.5px; }
.control-grid .control label { font-size: 11.5px; }
.control-grid input[type="range"] { margin: 3px 0 1px; height: 3px; }
.options-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 5px 10px; margin-top: 10px; }
.options-grid label { display: inline-flex; align-items: center; gap: 5px; color: #4a5a72; font-size: 11.5px; cursor: pointer; white-space: nowrap; }
.options-grid input { accent-color: var(--blue); flex: none; }
.note {
  margin-top: 9px; padding: 6px 8px; border: 1px solid #cddffb; border-radius: 9px;
  color: var(--blue-dark); background: var(--blue-soft); font-size: 11.5px; line-height: 1.5;
}
.note.warn { border-color: #f3d19b; color: #92400e; background: #fef6e7; }
.legend { gap: 4px 10px; font-size: 11px; }
.legend i.hollow { width: 12px; height: 12px; border: 2px solid #0e7490; border-radius: 3px; background: #fff; }

@media (max-width: 720px) {
  .panel h1 { font-size: 13.5px; }
  .control-grid { gap: 4px 8px; }
  .control-grid .control label, .control-grid .control-head output { font-size: 10.5px; }
  .options-grid label { font-size: 10.5px; }
  .legend { font-size: 10px; gap: 3px 7px; }
  .note { font-size: 10.5px; }
  .readout { font-size: 12px; line-height: 1.45; padding: 6px 8px; max-width: calc(100vw - 16px); }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 10.5px; }
}
html, body { overflow-x: hidden; }
.app { max-width: 100vw; }
"""

BODY = """
<svg class="viewport" id="viewport" role="img"
     aria-label="RPR 柱坐标三自由度操作臂（转动-移动-转动）的交互三维示意图">
  <defs>
    <marker id="mX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="mY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="mZ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="mTheta1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
    <marker id="mTheta3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="mD2" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="mArm" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="rangeLayer"></g>
  <g id="armLayer"></g>
  <g id="dimLayer"></g>
  <g id="frameLayer"></g>
  <g id="labelLayer"></g>
</svg>

<section class="panel" aria-label="图3-9 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3-9 含一个移动关节的 3 自由度臂</h1>
      <p class="subtitle">例3.4 的 RPR 柱坐标臂：关节轴 1（竖直转动）⊥ 关节轴 2（水平移动）。
        α₁ = 90°、d₁ = 0 → 两关节轴相交，{0} 就建在交点处。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="t1">转动 θ₁</label><output id="t1Value">0.0°</output></div>
      <input id="t1" type="range" min="-180" max="180" step="1" value="0">
    </div>
    <div class="control">
      <div class="control-head"><label for="d2">移动 d₂</label><output id="d2Value">0.80</output></div>
      <input id="d2" type="range" min="0" max="2" step="0.05" value="0.8">
    </div>
    <div class="control">
      <div class="control-head"><label for="t3">转动 θ₃</label><output id="t3Value">0.0°</output></div>
      <input id="t3" type="range" min="-180" max="180" step="1" value="0">
    </div>
  </div>

  <div class="options-grid">
    <label><input id="showFrames" type="checkbox" checked>坐标系 {0}{1}{2}{3}</label>
    <label><input id="showRange" type="checkbox" checked>工作范围提示</label>
    <label><input id="showSymbol" type="checkbox" checked>关节符号</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="note" id="specialNote"></div>

  <div class="legend">
    <span><i style="background:#475569"></i>轴1 竖直转动副</span>
    <span><i class="hollow"></i>轴2 水平移动副（活塞）</span>
    <span><i style="background:#0e7490"></i>θ₁ 转角</span>
    <span><i style="background:#7c3aed"></i>θ₃ 转角</span>
    <span><i class="dot" style="background:#c26a10"></i>末端点</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row">末端在 {0}：<strong>P</strong> = [ <span id="rx">0.800</span>, <span id="ry">0.000</span>, <span id="rz">0.000</span> ]ᵀ</div>
  <div class="row">关节变量：( θ₁, d₂, θ₃ ) = ( <span id="rv1">0.0°</span>, <span id="rv2">0.800</span>, <span id="rv3">0.0°</span> )</div>
  <div class="row small">与 {0} 原点距离 = <span id="rdist">0.800</span>（恒等于 d₂）　·　z = <span id="rz2">0.000</span>（恒为 0）</div>
  <div class="row small" id="rnote">轴1 方向 = Ẑ₀，轴2 方向 = (cosθ₁, sinθ₁, 0)，点乘恒为 0（垂直）</div>
  <div class="row small">D-H 记法（例3.4）：Ẑ<sub>i−1</sub> 沿关节 i 轴，轴1 竖直、轴2 水平，交于 {0} 原点。</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var rangeLayer = document.getElementById("rangeLayer");
  var armLayer = document.getElementById("armLayer");
  var dimLayer = document.getElementById("dimLayer");
  var frameLayer = document.getElementById("frameLayer");
  var labelLayer = document.getElementById("labelLayer");
  var svgNS = "http://www.w3.org/2000/svg";

  var DEFAULTS = { t1: 0, d2: 0.8, t3: 0 };
  var state = {
    t1: DEFAULTS.t1, d2: DEFAULTS.d2, t3: DEFAULTS.t3,
    showFrames: true, showRange: true, showSymbol: true, auto: false
  };

  /* 允许用 #t1=90&d2=0.8&t3=0 指定初始状态（便于核对例3.4 的数值） */
  (function readHash() {
    var raw = (window.location.hash || "").replace(/^#/, "");
    if (!raw) return;
    raw.split("&").forEach(function (kv) {
      var parts = kv.split("=");
      if (parts.length !== 2) return;
      var key = decodeURIComponent(parts[0]);
      var value = Number(decodeURIComponent(parts[1]));
      if (!isFinite(value)) return;
      if (key === "t1" || key === "t3") state[key] = Math.max(-180, Math.min(180, value));
      if (key === "d2") state.d2 = Math.max(0, Math.min(2, value));
    });
  }());

  /* ---------------- 取景矩形（初值按 1000x620 设计稿） ----------------
     桌面：左侧让给 304px 面板，右下角让给读数卡；
     移动端：面板在底部，读数卡在顶部。 */
  var FIT = { cx: 620, cy: 300, halfW: 430, halfH: 280 };

  var scene = new FK.AdaptiveScene({
    svg: viewport,
    scale: 132,
    narrowScale: 86,
    yaw: -0.72,
    pitch: 0.56,
    wide: { x: 0.62, y: 0.5 },
    narrow: { x: 0.5, y: 0.33 },
    tall: { x: 0.5, y: 0.3 },
    onLayout: function (sc, box) {
      if (box.narrow) {
        FIT.cx = box.width * 0.5; FIT.cy = box.height * 0.355;
        FIT.halfW = box.width * 0.46; FIT.halfH = box.height * 0.235;
      } else {
        FIT.cx = box.width * 0.63; FIT.cy = box.height * 0.50;
        FIT.halfW = box.width * 0.25; FIT.halfH = box.height * 0.40;
      }
    }
  });

  var COL = {
    base: "#475569", arm: "#64748b", carriage: "#334155", rod: "#94a3b8",
    t1: "#0e7490", t3: "#7c3aed", d2: "#c26a10", tip: "#c26a10",
    range: "#2563eb", rangeFill: "rgba(37, 99, 235, 0.10)",
    x: "#d93025", y: "#2563eb", z: "#12944f"
  };

  /* ---------------- 图元 ---------------- */
  function el(tag, attrs, parent) { return scene.el(tag, attrs, parent || armLayer); }
  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    return el("line", Object.assign({ x1: A.x, y1: A.y, x2: B.x, y2: B.y }, attrs || {}), parent);
  }
  function poly(points, attrs, parent) { return scene.polyline(points, attrs, parent || armLayer); }
  function overlaps(a, b) { return !(a.x2 < b.x1 || b.x2 < a.x1 || a.y2 < b.y1 || b.y2 < a.y1); }
  var boxes = [];
  function place(p, text, font, color, prefs, italic) {
    var q = scene.project(p);
    var w = text.length * font * 0.70 + 4, h = font * 1.25;
    var chosen = null, best = Infinity;
    for (var i = 0; i < prefs.length; i += 1) {
      var x = q.x + prefs[i][0], y = q.y + prefs[i][1];
      var box = { x1: x - 3, y1: y - h + 2, x2: x + w + 3, y2: y + 4 };
      var hit = false;
      for (var k = 0; k < boxes.length; k += 1) { if (overlaps(box, boxes[k])) { hit = true; break; } }
      var cost = (hit ? 100 : 0) + i * 0.5;
      if (cost < best) { best = cost; chosen = box; }
      if (!hit) break;
    }
    if (!chosen) chosen = { x1: q.x + 10, y1: q.y - h + 2, x2: q.x + 10 + w, y2: q.y + 4 };
    boxes.push(chosen);
    var node = el("text", {
      x: chosen.x1 + 3, y: chosen.y1 + h - 4, fill: color, "font-size": font,
      class: "fk-axis-label", "font-style": italic ? "italic" : "normal"
    }, labelLayer);
    node.textContent = text;
    return node;
  }

  /* ---------------- 正运动学 ----------------
     1_0T = R_Z(θ₁)·R_X(α₁)·D_X(d₂)，α₁ = 90°（例3.4）；末端在 {0} 中：x = d₂cosθ₁, y = d₂sinθ₁, z = 0 */
  function fk(t1, d2, t3) {
    var a1 = 90 * FK.DEG;
    var T = FK.M4.chain(FK.M4.rotZ(t1), FK.M4.rotX(a1), FK.M4.translate([d2, 0, 0]));
    var T3 = FK.M4.chain(T, FK.M4.rotZ(t3));
    var origin0 = [0, 0, 0];
    var origin1 = FK.M4.position(FK.M4.chain(FK.M4.rotZ(t1), FK.M4.rotX(a1)));
    var origin2 = FK.M4.position(T);
    return {
      T: T, T3: T3, origin0: origin0, origin1: origin1, origin2: origin2,
      tip: origin2, armDir: [Math.cos(t1), Math.sin(t1), 0]
    };
  }

  /* ---------------- 绘制部件 ---------------- */
  function drawFrame(m, len, tags, colors) {
    var dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    var markers = ["mX", "mY", "mZ"];
    var O = scene.project(FK.M4.apply(m, [0, 0, 0]));
    for (var i = 0; i < 3; i += 1) {
      var tip = FK.M4.apply(m, FK.Vec.scale(dirs[i], len));
      var B = scene.project(tip);
      el("line", {
        x1: O.x, y1: O.y, x2: B.x, y2: B.y, stroke: colors[i],
        "stroke-width": 2.6, "marker-end": "url(#" + markers[i] + ")"
      }, frameLayer);
      var node = el("text", {
        x: B.x + 6, y: B.y - 5, fill: colors[i], "font-size": 13, "font-style": "italic", class: "fk-axis-label"
      }, frameLayer);
      node.textContent = ["X\u0302", "Y\u0302", "Z\u0302"][i] + tags;
    }
    el("circle", { cx: O.x, cy: O.y, r: 3.4, fill: "#334155" }, frameLayer);
  }

  /* 移动副符号：机械制图里的“活塞”——缸体方框 + 活塞杆 + 双斜线（绝不是旋转副的圆） */
  function pistonSymbol(from, to, size, color) {
    var D = FK.Vec.sub(to, from);
    var dist = FK.Vec.len(D);
    if (dist < 1e-6) return;
    var dir = FK.Vec.normalize(D);
    var perp = FK.Vec.normalize(FK.Vec.cross(dir, [0, 0, 1]));
    if (!perp || FK.Vec.len(perp) < 0.5) perp = FK.Vec.normalize(FK.Vec.cross(dir, [0, 1, 0]));
    // 缸体：从肩部起沿臂方向的方框（固定在内侧）
    var boxLen = Math.min(dist * 0.42, 0.34);
    var box = [
      FK.Vec.add(from, FK.Vec.scale(perp, size)),
      FK.Vec.add(FK.Vec.add(from, FK.Vec.scale(perp, size)), FK.Vec.scale(dir, boxLen)),
      FK.Vec.add(FK.Vec.add(from, FK.Vec.scale(perp, -size)), FK.Vec.scale(dir, boxLen)),
      FK.Vec.add(from, FK.Vec.scale(perp, -size))
    ];
    poly(box.concat([box[0]]), { stroke: "#475569", "stroke-width": 2, fill: "rgba(148,163,184,0.22)" }, armLayer);
    // 活塞杆：从缸体伸到滑座
    seg(FK.Vec.add(from, FK.Vec.scale(dir, boxLen * 0.5)), to,
      { stroke: color, "stroke-width": 5, "stroke-linecap": "round" }, armLayer);
    // 滑座（末端侧的滑块）
    var car = [
      FK.Vec.add(to, FK.Vec.scale(perp, size * 1.5)),
      FK.Vec.add(FK.Vec.add(to, FK.Vec.scale(perp, size * 1.5)), FK.Vec.scale(dir, size * 2.4)),
      FK.Vec.add(FK.Vec.add(to, FK.Vec.scale(perp, -size * 1.5)), FK.Vec.scale(dir, size * 2.4)),
      FK.Vec.add(to, FK.Vec.scale(perp, -size * 1.5))
    ];
    poly(car.concat([car[0]]), { stroke: color, "stroke-width": 2.2, fill: "rgba(51,65,85,0.16)" }, armLayer);
    // 双斜线：移动副（滑移副）的图例符号
    var diag = FK.Vec.normalize(FK.Vec.add(dir, perp));
    [0.40, 0.58].forEach(function (s) {
      var c = FK.Vec.add(from, FK.Vec.scale(D, s));
      seg(FK.Vec.add(c, FK.Vec.scale(diag, -size * 0.85)), FK.Vec.add(c, FK.Vec.scale(diag, size * 0.85)),
        { stroke: color, "stroke-width": 2.4 }, armLayer);
    });
  }

  /* 转动副符号：端面小圆 + 转角弧 */
  function revoluteArc(center, radius, from, sweep, color, marker, label) {
    if (Math.abs(sweep) < 0.02) return;
    var pts = [];
    for (var i = 0; i <= 48; i += 1) {
      var a = from + sweep * (i / 48);
      pts.push([center[0] + radius * Math.cos(a), center[1] + radius * Math.sin(a), center[2]]);
    }
    poly(pts, {
      stroke: color, "stroke-width": 2.6, "stroke-dasharray": "7 5", fill: "none",
      "marker-end": "url(#" + marker + ")"
    }, dimLayer);
    var mid = from + sweep * 0.5;
    place([center[0] + (radius + 0.10) * Math.cos(mid), center[1] + (radius + 0.10) * Math.sin(mid), center[2]],
      label, 15, color, [[-10, -8], [10, 6], [-10, 18], [10, -18]]);
  }

  /* 工作范围：柱坐标臂只在水平面内伸缩（z 恒为 0），因此工作空间是 xy 平面上的圆盘（半径 0~2.0） */
  function drawRange() {
    var rMax = 1.6, rNow = state.d2;   // 工作范围提示取 d₂ ∈ [0, 2] 内的示意外沿
    // θ₁ 扇形（±180°，浅色圆盘）
    var sector = [[0, 0, 0]];
    for (var k = 0; k <= 64; k += 1) {
      var ang = -Math.PI + k * 2 * Math.PI / 64;
      sector.push([rMax * Math.cos(ang), rMax * Math.sin(ang), 0]);
    }
    poly(sector, { fill: COL.rangeFill, stroke: "none" }, rangeLayer);
    // 半径刻度圆（当前 d₂ 加粗显示）
    [0.4, 0.8, 1.2, rMax].forEach(function (r) {
      var pts = [];
      for (var i = 0; i <= 72; i += 1) {
        var a = i * 2 * Math.PI / 72;
        pts.push([r * Math.cos(a), r * Math.sin(a), 0]);
      }
      poly(pts, {
        stroke: COL.range, "stroke-width": r === rNow ? 2.6 : 1.4,
        "stroke-dasharray": r === rNow ? "10 6" : "6 7",
        opacity: r === rNow ? 0.95 : 0.5, fill: "none"
      }, rangeLayer);
    });
    for (var j = 0; j < 6; j += 1) {
      var a2 = j * Math.PI / 3 + Math.PI / 6;
      seg([0, 0, 0], [rMax * Math.cos(a2), rMax * Math.sin(a2), 0],
        { stroke: COL.range, "stroke-width": 1.1, opacity: 0.55 }, rangeLayer);
      seg([rNow * Math.cos(a2), rNow * Math.sin(a2), 0], [rMax * Math.cos(a2), rMax * Math.sin(a2), 0],
        { stroke: COL.range, "stroke-width": 1.1, opacity: 0.35 }, rangeLayer);
    }
    place([rMax * Math.cos(Math.PI * 0.72), rMax * Math.sin(Math.PI * 0.72), 0],
      "\u5de5\u4f5c\u8303\u56f4\uff1a\u534a\u5f84 0 \u2192 " + FK.format(rMax, 1) + " \u7684\u5706\u76d8", 13, "#174ea6",
      [[10, -8], [10, 16], [-160, -8]]);
  }

  /* ---------------- 主绘制 ---------------- */
  function render() {
    gridLayer.replaceChildren();
    rangeLayer.replaceChildren();
    armLayer.replaceChildren();
    dimLayer.replaceChildren();
    frameLayer.replaceChildren();
    labelLayer.replaceChildren();
    boxes = [];

    var t1 = state.t1 * FK.DEG;
    var t3 = state.t3 * FK.DEG;
    var K = fk(t1, state.d2, t3);

    /* 取景：基座、当前臂端、工作范围外沿、各坐标系轴端 */
    var pts = [[0, 0, 0], [0, 0, 0.55], K.tip, [1.62, 0, 0], [-1.62, 0, 0], [0, 1.62, 0], [0, -1.62, 0], [0, 0, -0.30]];
    pts.push(FK.Vec.add(K.origin2, [0.26, 0, 0]));
    pts.push(FK.Vec.add(K.origin2, [-0.26, 0, 0]));
    pts.push(FK.Vec.add(K.origin2, [0, 0, 0.26]));
    fitView(pts);

    scene.grid(1, 1, null, gridLayer);

    if (state.showRange) drawRange();

    var D = K.armDir;

    /* 1) 基座与竖直转动关节（轴1） */
    var baseH = 0.30, baseR = 0.26;
    (function base() {
      var ring = [];
      for (var i = 0; i <= 40; i += 1) {
        var a = i * 2 * Math.PI / 40;
        ring.push([baseR * Math.cos(a), baseR * Math.sin(a), 0]);
      }
      poly(ring, { stroke: COL.base, "stroke-width": 2.4, fill: "rgba(71,85,105,0.10)" }, armLayer);
      // 立柱：4 条竖直母线
      [0, 0.25, 0.5, 0.75].forEach(function (f) {
        var a3 = f * 2 * Math.PI;
        seg([baseR * Math.cos(a3), baseR * Math.sin(a3), 0], [baseR * Math.cos(a3), baseR * Math.sin(a3), baseH],
          { stroke: COL.base, "stroke-width": 1.6 }, armLayer);
      });
      var top = [];
      for (var k = 0; k <= 40; k += 1) {
        var a4 = k * 2 * Math.PI / 40;
        top.push([baseR * Math.cos(a4), baseR * Math.sin(a4), baseH]);
      }
      poly(top, { stroke: COL.base, "stroke-width": 2.2 }, armLayer);
      // 固定基座的地脚斜线
      for (var m = -2; m <= 2; m += 1) {
        seg([m * 0.10 - 0.06, -0.10, 0], [m * 0.10 + 0.02, -0.22, 0], { stroke: COL.base, "stroke-width": 1.4 }, armLayer);
      }
    }());
    // 轴1：竖直转动副的轴线
    seg([0, 0, 0], [0, 0, 0.70], { stroke: COL.base, "stroke-width": 3.4, "marker-end": "url(#mArm)" }, armLayer);
    place([0, 0, 0.70], "\u8f74 1", 14, "#475569", [[10, -6], [-40, -6], [10, 16]]);

    /* 2) 水平移动关节（轴2，滑移副）与连杆 */
    if (state.d2 > 0.02) {
      pistonSymbol([0, 0, 0], K.origin2, 0.075, COL.carriage);
      // 活塞杆中心线（移动方向）
      seg([0, 0, 0], FK.Vec.add(K.origin2, FK.Vec.scale(D, 0.22)),
        { stroke: COL.d2, "stroke-width": 2, "stroke-dasharray": "9 6", "marker-end": "url(#mD2)" }, dimLayer);
      var mid = FK.Vec.scale(K.origin2, 0.55);
      place(mid, "d\u2082", 15, "#8a4a08", [[0, -30], [0, 26], [16, -12]]);
    }

    /* 3) 末端转动关节（轴3）与末端点 */
    seg(K.origin2, FK.Vec.add(K.origin2, [0, 0, 0.26]), { stroke: COL.t3, "stroke-width": 3.2 }, armLayer);
    // θ₃ 绕竖直末端轴转动：在水平面内由臂方向扫过 t3，扇面定位在当前臂方向附近
    revoluteArc([K.origin2[0], K.origin2[1], 0], 0.24, t1, t3, COL.t3, "mTheta3", "\u03b8\u2083 = " + FK.deg(state.t3, 1));
    var tp = scene.project(K.tip);
    el("circle", { cx: tp.x, cy: tp.y, r: 6.6, fill: COL.tip, stroke: "#fff", "stroke-width": 2.2, class: "fk-point" }, armLayer);
    place(K.tip, "\u672b\u7aef", 15, "#8a4a08", [[14, -10], [14, 22], [-44, -12]]);

    /* 4) 轴交点的“点”标记（教材在轴交点用小圆点） */
    if (state.showSymbol) {
      var o = scene.project([0, 0, 0]);
      el("circle", { cx: o.x, cy: o.y, r: 4.2, fill: "#0e7490", stroke: "#fff", "stroke-width": 1.6 }, armLayer);
      place([0, 0, 0], "\u4e24\u8f74\u4ea4\u70b9 O", 13, "#0e7490", [[-84, 34], [12, 34], [-84, -10]]);
    }

    /* 5) θ₁ 转角：从 +X₀ 转到臂方向 */
    revoluteArc([0, 0, 0.06], 0.34, 0, t1, COL.t1, "mTheta1", "\u03b8\u2081 = " + FK.deg(state.t1, 1));

    /* 6) 坐标系 {0}{1}{2}{3}：例3.4 的 D-H 记法 z_{i−1} 沿关节 i 轴 */
    if (state.showFrames) {
      drawFrame(FK.M4.identity(), 0.34, "_{0}", [COL.x, COL.y, COL.z]);
      var T1 = FK.M4.chain(FK.M4.rotZ(t1), FK.M4.rotX(90 * FK.DEG));
      drawFrame(T1, 0.26, "_{1}", [COL.x, COL.y, COL.z]);
      drawFrame(K.T, 0.24, "_{2}", [COL.x, COL.y, COL.z]);
      drawFrame(K.T3, 0.22, "_{3}", [COL.x, COL.y, COL.z]);
    } else {
      // 至少要标出 {0} 的三个轴，方便对照读数
      drawFrame(FK.M4.identity(), 0.34, "_{0}", [COL.x, COL.y, COL.z]);
    }

    /* 7) 读数 */
    var d2 = state.d2;
    var dist = Math.sqrt(K.tip[0] * K.tip[0] + K.tip[1] * K.tip[1] + K.tip[2] * K.tip[2]);
    document.getElementById("rx").textContent = FK.format(K.tip[0], 3);
    document.getElementById("ry").textContent = FK.format(K.tip[1], 3);
    document.getElementById("rz").textContent = FK.format(K.tip[2], 3);
    document.getElementById("rv1").textContent = FK.deg(state.t1, 1);
    document.getElementById("rv2").textContent = FK.format(d2, 3);
    document.getElementById("rv3").textContent = FK.deg(state.t3, 1);
    document.getElementById("rdist").textContent = FK.format(dist, 3);
    document.getElementById("rz2").textContent = FK.format(K.tip[2], 3);
    document.getElementById("rnote").textContent =
      "轴1 方向 = Ẑ₀ = (0,0,1)，轴2 方向 = (cosθ₁, sinθ₁, 0)；点乘恒为 0（两轴垂直，α₁ = 90°）";

    var note = document.getElementById("specialNote");
    if (d2 < 1e-9) {
      note.className = "note warn";
      note.innerHTML = "<b>d₂ = 0</b>：末端落在两关节轴的交点 O（{0} 的原点）上，此时 {0} 与“末端所在点”重合；"
        + "移动关节完全缩回。";
    } else {
      note.className = "note";
      note.innerHTML = "末端高度恒为 z = 0（柱坐标臂只在水平面内伸缩）；位置只由 θ₁、d₂ 决定，"
        + "θ₃ 改变末端姿态而不改变末端位置——这是含移动关节操作臂的典型退化特征。";
    }
  }

  /* 取景：把点集等比装进 FIT 矩形 */
  function fitView(points) {
    var yaw = scene.state.yaw, pitch = scene.state.pitch;
    var cy = Math.cos(yaw), sy = Math.sin(yaw);
    var cp = Math.cos(pitch), sp = Math.sin(pitch);
    function u(v) { return v[0] * cy - v[1] * sy; }
    function s(v) { return -((v[0] * sy + v[1] * cy) * sp + v[2] * cp); }
    var uMin = Infinity, uMax = -Infinity, sMin = Infinity, sMax = -Infinity;
    for (var i = 0; i < points.length; i += 1) {
      var uu = u(points[i]), ss = s(points[i]);
      if (uu < uMin) uMin = uu;
      if (uu > uMax) uMax = uu;
      if (ss < sMin) sMin = ss;
      if (ss > sMax) sMax = ss;
    }
    var spanU = Math.max(0.6, uMax - uMin);
    var spanS = Math.max(0.6, sMax - sMin);
    var scale = Math.max(40, Math.min(190, 2 * FIT.halfW / spanU, 2 * FIT.halfH / spanS));
    scene.state.scale = scale;
    scene.defaults.scale = scale;
    scene.baseOrigin.x = FIT.cx - (uMin + uMax) * scale / 2;
    scene.baseOrigin.y = FIT.cy - (sMin + sMax) * scale / 2;
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "t1", key: "t1", value: DEFAULTS.t1, format: function (v) { return FK.deg(v, 1); } },
    { id: "d2", key: "d2", value: DEFAULTS.d2, format: function (v) { return FK.format(v, 2); } },
    { id: "t3", key: "t3", value: DEFAULTS.t3, format: function (v) { return FK.deg(v, 1); } }
  ], state, function () { render(); });

  FK.bindToggles([
    { id: "showFrames", key: "showFrames" },
    { id: "showRange", key: "showRange" },
    { id: "showSymbol", key: "showSymbol" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.t1 = DEFAULTS.t1; state.d2 = DEFAULTS.d2; state.t3 = DEFAULTS.t3;
    state.showFrames = true; state.showRange = true; state.showSymbol = true; state.auto = false;
    document.getElementById("showFrames").checked = true;
    document.getElementById("showRange").checked = true;
    document.getElementById("showSymbol").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    scene.fit();
    render();
  });

  /* ---------------- 教材数值自检 ---------------- */
  (function selfTest() {
    function close(x, y, eps) { return Math.abs(x - y) < (eps === undefined ? 1e-9 : eps); }
    var A1 = 90 * FK.DEG;
    function dh(t1, d2, t3) {
      var T = FK.M4.chain(FK.M4.rotZ(t1), FK.M4.rotX(A1), FK.M4.translate([d2, 0, 0]), FK.M4.rotZ(t3));
      return { T: T, p: FK.M4.position(T) };
    }
    function analytic(t1, d2) { return [d2 * Math.cos(t1), d2 * Math.sin(t1), 0]; }

    // 1) d₂ = 0、θ₁ = θ₃ = 0 → 末端在 {0} 原点
    var k0 = dh(0, 0, 0);
    if (!FK.Vec.eq(FK.Vec.round(k0.p, 12), [0, 0, 0], 1e-12)) {
      throw new Error("d₂=0 且 θ₁=θ₃=0 时末端应为 {0} 原点，实得 " + JSON.stringify(k0.p));
    }
    // 2) 例3.4：(θ₁, d₂, θ₃) = (90°, 0.8, 0°) → (0, 0.8, 0)
    var k1 = dh(90 * FK.DEG, 0.8, 0);
    if (!FK.Vec.eq(FK.Vec.round(k1.p, 9), [0, 0.8, 0], 1e-9)) {
      throw new Error("例3.4 末端坐标应为 (0, 0.8, 0)，实得 " + JSON.stringify(k1.p));
    }
    // 3) 一般情形：D-H 连乘 = 解析式 (d₂cosθ₁, d₂sinθ₁, 0)，z 恒为 0
    [[0, 0.8, 0], [0.6, 1.4, -1.2], [-2.2, 0.35, 2.0], [Math.PI, 2.0, 0.7]].forEach(function (c, index) {
      var got = dh(c[0], c[1], c[2]).p;
      var want = analytic(c[0], c[1]);
      if (!FK.Vec.eq(FK.Vec.round(got, 12), FK.Vec.round(want, 12), 1e-12)) {
        throw new Error("第" + (index + 1) + "组 D-H 连乘与解析式不一致：" + JSON.stringify(got) + " vs " + JSON.stringify(want));
      }
      if (!close(got[2], 0, 1e-12)) throw new Error("末端高度应恒为 0");
    });
    // 4) 末端到 {0} 原点的距离恒等于 d₂，且与 θ₃ 无关
    [0, 0.5, -1.9, Math.PI].forEach(function (t1v) {
      [0, 0.3, 1.2, 2.0].forEach(function (d2v) {
        var p1 = dh(t1v, d2v, 0).p, p2 = dh(t1v, d2v, 1.7).p;
        if (!close(FK.Vec.len(p1), d2v, 1e-12) || !close(FK.Vec.len(p2), d2v, 1e-12)) {
          throw new Error("末端到原点距离应等于 d₂ = " + d2v);
        }
        if (!FK.Vec.eq(FK.Vec.round(p1, 12), FK.Vec.round(p2, 12), 1e-12)) {
          throw new Error("θ₃ 不应改变末端位置");
        }
      });
    });
    // 5) 两关节轴垂直：轴1 = Ẑ₀，轴2 = (cosθ₁, sinθ₁, 0)
    [0, 0.4, -1.3, 2.7].forEach(function (t1v) {
      var axis1 = FK.M4.applyDir(FK.M4.identity(), [0, 0, 1]);
      var axis2 = FK.M4.applyDir(FK.M4.rotZ(t1v), FK.M4.applyDir(FK.M4.rotX(A1), [1, 0, 0]));
      if (!close(FK.Vec.dot(axis1, axis2), 0, 1e-12)) throw new Error("轴1 与轴2 应恒垂直（α₁ = 90°）");
      if (!FK.Vec.eq(FK.Vec.round(axis2, 9), FK.Vec.round([Math.cos(t1v), Math.sin(t1v), 0], 9), 1e-9)) {
        throw new Error("轴2 方向应为 (cosθ₁, sinθ₁, 0)");
      }
    });
    // 6) 表参数：α₁ = 90°、d₁ = 0（两轴相交于 {0} 原点）
    var Talpha = FK.M4.chain(FK.M4.rotZ(0), FK.M4.rotX(A1), FK.M4.translate([0, 0, 0]));
    if (!FK.Vec.eq(FK.Vec.round(FK.M4.position(Talpha), 12), [0, 0, 0], 1e-12)) {
      throw new Error("d₁ = 0 时轴2 应过 {0} 原点（两轴相交）");
    }
  }());

  render();
}());
"""

FIGURE = {
    "id": "figure-3-9",
    "title": "图3-9 含一个移动关节的三自由度操作臂（例3.4 RPR）· 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
