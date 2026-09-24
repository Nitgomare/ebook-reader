"""图2-7 在一般情况下的矢量变换（克雷格《机器人学导论（第3版）》2.3 节）。

教材依据：
- 正文式(2-17)：ᴬP = ᴬ_BR·ᴮP + ᴬP_BORG。
- 正文对式(2-17) 的分解原文：“首先将 ᴮP 变换到一个中间坐标系，这个坐标系和 {A} 的姿态相同、
  原点和 {B} 的原点重合。这可以像上一节中那样由左乘矩阵 ᴬ_BR 得到。然后仍用简单的矢量加法
  将原点平移，并得到…”。图中的虚线灰色坐标系即为该中间坐标系。
- 脚本自检：取教材例2.2 的数据（ᴬP_BORG=(10,5,0)、θ=30°、ᴮP=(3,7,0)）时，
  两步结果必须等于 ᴬP = [9.098, 12.562, 0]（式(2-23)）；且退化情形（ᴬP_BORG=0、ᴮP=(0,2,0)）
  必须等于例2.1 的 ᴬP = (−1, 1.732, 0)（式(2-16)）。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.control-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 7px 10px; margin-top: 9px; }
.control-grid .control { margin-top: 0; min-width: 0; }
.control-grid .control-head { display: block; line-height: 1.3; }
.control-grid .control-head output { display: block; font-size: 11.5px; }
.control-grid .control label { font-size: 11.5px; }
.control-grid input[type="range"] { margin: 3px 0 1px; height: 3px; }
.options-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 5px 10px; margin-top: 10px; }
.options-grid label { display: inline-flex; align-items: center; gap: 5px; color: #4a5a72; font-size: 11.5px; cursor: pointer; white-space: nowrap; }
.options-grid input { accent-color: var(--blue); flex: none; }
.panel .legend { gap: 4px 10px; }
@media (max-width: 720px) {
  .panel h1 { font-size: 14px; }
  .control-grid { gap: 5px 8px; }
  .control-grid .control label, .control-grid .control-head output { font-size: 10.5px; }
  .options-grid { gap: 4px 8px; }
  .options-grid label { font-size: 10.5px; }
  .panel .legend { font-size: 10.5px; gap: 3px 8px; }
  .readout { font-size: 12px; line-height: 1.45; padding: 6px 8px; }
  .readout .small { font-size: 10.5px; }
}

/* 移动端收尾：确保 390px 宽下不出现横向溢出、面板与读数都收在视口内 */
html, body { overflow-x: hidden; }
.app { max-width: 100vw; }
@media (max-width: 720px) {
  .panel { overflow-x: hidden; }
  .panel h1 { font-size: 13.5px; }
  .legend { font-size: 10px; gap: 3px 7px; }
  .legend span { white-space: nowrap; }
  .options-grid label { font-size: 10px; }
  .readout { max-width: calc(100% - 16px); overflow-wrap: anywhere; }
}

/* 移动端硬性约束：任何块都不得超出 390px 视口 */
@media (max-width: 720px) {
  .readout {
    max-width: calc(100vw - 16px) !important;
    white-space: normal !important;
    word-break: break-word;
  }
  .readout .row { white-space: normal !important; }
  .panel { max-width: calc(100vw - 16px) !important; }
  .matrix { max-width: calc(100vw - 16px) !important; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="矢量从坐标系B到坐标系A的一般变换：先旋转到中间坐标系，再加平移的交互示意图">
  <defs>
    <marker id="mAxis" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"></path>
    </marker>
    <marker id="mBx" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="mBy" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="mBz" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="mVec" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
    <marker id="mFin" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="mTr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="frameC"></g>
  <g id="axesA"></g>
  <g id="frameB"></g>
  <g id="vectorLayer"></g>
  <g id="angleLayer"></g>
  <g id="labelLayer"></g>
</svg>

<section class="panel" aria-label="图2-7 控制面板">
  <div class="panel-head">
    <div>
      <h1>图2-7 一般情况下的矢量变换</h1>
      <p class="subtitle">第1步：左乘 ᴬ_BR，把 ᴮP 转到“与{A}姿态相同、原点与{B}重合”的中间坐标系（灰色虚线架）；第2步：矢量加法加上 ᴬP_BORG，得 ᴬP = ᴬ_BR·ᴮP + ᴬP_BORG（式2-17）。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="theta">旋转角 θ</label><output id="thetaValue">30.0°</output></div>
      <input id="theta" type="range" min="-180" max="180" step="1" value="30">
    </div>
    <div class="control">
      <div class="control-head"><label for="bx">ᴬP_BORG x</label><output id="bxValue">10.0</output></div>
      <input id="bx" type="range" min="-10" max="10" step="0.5" value="10">
    </div>
    <div class="control">
      <div class="control-head"><label for="by">ᴬP_BORG y</label><output id="byValue">5.0</output></div>
      <input id="by" type="range" min="-10" max="10" step="0.5" value="5">
    </div>
    <div class="control">
      <div class="control-head"><label for="bz">ᴬP_BORG z</label><output id="bzValue">0.0</output></div>
      <input id="bz" type="range" min="-6" max="6" step="0.5" value="0">
    </div>
    <div class="control">
      <div class="control-head"><label for="px">ᴮP x</label><output id="pxValue">3.0</output></div>
      <input id="px" type="range" min="-10" max="10" step="0.5" value="3">
    </div>
    <div class="control">
      <div class="control-head"><label for="py">ᴮP y</label><output id="pyValue">7.0</output></div>
      <input id="py" type="range" min="-10" max="10" step="0.5" value="7">
    </div>
    <div class="control">
      <div class="control-head"><label for="pz">ᴮP z</label><output id="pzValue">0.0</output></div>
      <input id="pz" type="range" min="-6" max="6" step="0.5" value="0">
    </div>
    <div class="control">
      <div class="control-head"><label for="showVecB">显示 ᴮP</label><output id="showVecBValue">显示</output></div>
      <input id="showVecB" type="range" min="0" max="1" step="1" value="1" aria-label="显示矢量 BP">
    </div>
    <div class="control">
      <div class="control-head"><label for="auto">自动旋转</label><output id="autoValue">关</output></div>
      <input id="auto" type="range" min="0" max="1" step="1" value="0" aria-label="自动旋转视角">
    </div>
  </div>

  <div class="options-grid">
    <label><input id="step2" type="checkbox" checked>两步都看</label>
    <label><input id="showC" type="checkbox" checked>中间坐标系</label>
    <label><input id="showComp" type="checkbox" checked>分量虚线</label>
  </div>

  <div class="legend">
    <span><i style="background:#64748b"></i>坐标系{A}</span>
    <span><i style="background:#d93025"></i>坐标系{B}</span>
    <span><i class="dot" style="background:#0e7490"></i>第1步 ᴬ_BR·ᴮP</span>
    <span><i class="dot" style="background:#c26a10"></i>第2步 ᴬP</span>
    <span><i style="background:#7c3aed"></i>平移 ᴬP_BORG</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row"><strong>第1步</strong> ᴬ_BR·ᴮP = [ <span id="m1">4.330</span>, <span id="m2">2.500</span>, <span id="m3">0.000</span> ]ᵀ</div>
  <div class="row"><strong>第2步</strong> + ᴬP_BORG = [ <span id="b1">10.000</span>, <span id="b2">5.000</span>, <span id="b3">0.000</span> ]ᵀ</div>
  <div class="row"><strong>ᴬP</strong> = [ <span id="px">9.098</span>, <span id="py">12.562</span>, <span id="pz">0.000</span> ]ᵀ</div>
  <div class="row small">ᴮP = [ <span id="q1">3.000</span>, <span id="q2">7.000</span>, <span id="q3">0.000</span> ]ᵀ（在{B}中不变）</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var LAYERS = ["grid", "frameC", "axesA", "frameB", "vectorLayer", "angleLayer", "labelLayer"];
  var gridLayer = document.getElementById("grid");
  var frameC = document.getElementById("frameC");
  var axesA = document.getElementById("axesA");
  var frameB = document.getElementById("frameB");
  var vectorLayer = document.getElementById("vectorLayer");
  var angleLayer = document.getElementById("angleLayer");
  var labelLayer = document.getElementById("labelLayer");

  /* 桌面 1200x700 与移动 390x844 下，SVG(viewBox 1000x620) 都居中缩放：屏幕上可用的内容带
     换算回 viewBox 约为 x∈[220,780]、y∈[30,330]，故固定用这一矩形做自动取景。 */
  /* 面板在桌面端占左侧 304px、移动端占底部；SVG(viewBox 1000x620) 居中缩放后，
     屏幕上可安全绘制的内容带换算回 viewBox 约为 x∈[420,890]、y∈[40,300]，
     故用中心 (655,170)、470x260 的矩形做自动取景。 */
  var FIT = { cx: 655, cy: 170, w: 470, h: 260 };
  var scene = new FK.Scene({ svg: viewport, origin: { x: FIT.cx, y: FIT.cy }, scale: 34, yaw: -0.62, pitch: 0.42 });
  var state = {
    theta: 30,
    Bx: 10, By: 5, Bz: 0,
    Px: 3, Py: 7, Pz: 0,
    step2: true, showC: true, showComp: true, showVecB: 1, auto: 0
  };

  var COLORS = {
    A: "#64748b", Bx: "#d93025", By: "#2563eb", Bz: "#12944f",
    C: "#94a3b8", step1: "#0e7490", final: "#c26a10", trans: "#7c3aed"
  };

  /* ---------------- 投影与自动取景 ----------------
     屏幕坐标（世界坐标 v，yaw/pitch 与 FK.Scene 一致）：
       u = 0.86*vx − 0.50*vy ;  w = 0.50*vx + 0.86*vy ;  screen_y = oy − scale*w */
  var UC = [0.86, -0.50];
  var WC = [0.50, 0.86];

  function projU(v) { return UC[0] * v[0] + UC[1] * v[1]; }
  function projW(v) { return WC[0] * v[0] + WC[1] * v[1]; }

  function fitView(points) {
    var uMin = Infinity, uMax = -Infinity, sMin = Infinity, sMax = -Infinity;
    for (var i = 0; i < points.length; i += 1) {
      var u = projU(points[i]);
      var s = -projW(points[i]);            // 屏幕上向上的方向 = −w，故 y 跨度取 s 的跨度
      if (u < uMin) uMin = u;
      if (u > uMax) uMax = u;
      if (s < sMin) sMin = s;
      if (s > sMax) sMax = s;
    }
    var spanU = Math.max(0.5, uMax - uMin);
    var spanS = Math.max(0.5, sMax - sMin);
    var scale = Math.max(12, Math.min(52, FIT.w / spanU, FIT.h / spanS));
    scene.state.scale = scale;
    scene.origin.x = scene.baseOrigin.x = FIT.cx - (uMin + uMax) * scale / 2;
    scene.origin.y = scene.baseOrigin.y = FIT.cy - (sMin + sMax) * scale / 2;
  }

  /* ---------------- 标签避让 ---------------- */
  /* 预留区：桌面端控制面板（左侧）、数值读数（右下）、提示（右上），避免标签被压住 */
  var RESERVED = [
    { x1: -400, y1: -400, x2: 350, y2: 700 },
    { x1: 660, y1: 415, x2: 1300, y2: 700 },
    { x1: 640, y1: -100, x2: 1300, y2: 70 }
  ];
  var boxes = [];
  function overlaps(a, b) { return !(a.x2 < b.x1 || b.x2 < a.x1 || a.y2 < b.y1 || b.y2 < a.y1); }
  /* 从 prefs 里挑第一个不与“预留区/已放标签”重叠的落点；layer 指定文字挂到哪个图层 */
  function place(p, text, font, color, prefs, cls, layer, extra) {
    var w = text.length * font * 0.72 + 4;
    var h = font * 1.25;
    var chosen = null, penalty = Infinity;
    for (var i = 0; i < prefs.length && !chosen; i += 1) {
      var x = p.x + prefs[i][0];
      if (prefs[i].length > 2 && prefs[i][2] !== undefined && x < prefs[i][2]) x = prefs[i][2];
      var grow = i * 4;
      var box = {
        x1: x - grow, y1: p.y + prefs[i][1] - h + 3 - grow,
        x2: x + w + grow, y2: p.y + prefs[i][1] + 3 + grow
      };
      var hit = false;
      for (var j = 0; j < RESERVED.length; j += 1) { if (overlaps(box, RESERVED[j])) { hit = true; break; } }
      for (var k = 0; !hit && k < boxes.length; k += 1) { if (overlaps(box, boxes[k])) hit = true; }
      var cost = (hit ? 100 : 0) + i + grow / 10;
      if (cost < penalty) { penalty = cost; chosen = box; }
      if (!hit) break;
    }
    if (!chosen) {
      var last = prefs[prefs.length - 1];
      var lx = p.x + last[0];
      if (last.length > 2 && last[2] !== undefined && lx < last[2]) lx = last[2];
      chosen = { x1: lx, y1: p.y + last[1] - h + 3, x2: lx + w, y2: p.y + last[1] + 3 };
    }
    boxes.push(chosen);
    var attrs = {
      x: chosen.x1, y: chosen.y1 + h - 4, fill: color, "font-size": font,
      class: cls || "fk-point-label"
    };
    if (extra) { Object.keys(extra).forEach(function (key) { attrs[key] = extra[key]; }); }
    var node = scene.el("text", attrs, layer || labelLayer);
    node.textContent = text;
    return node;
  }

  /* ---------------- 图元 ---------------- */
  function drawAxes(layer, matrix, spec, vLabel) {
    var dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    var labels = spec.labels;
    if (vLabel) { labels = [spec.labels[0], spec.labels[1], spec.labels[2]]; }
    for (var i = 0; i < 3; i += 1) {
      // 负半轴（虚线，便于看出 {A} 与中间坐标系姿态相同）
      var neg = scene.project(FK.M4.apply(matrix, FK.Vec.scale(dirs[i], -spec.back)));
      var base = scene.project(FK.M4.apply(matrix, [0, 0, 0]));
      if (spec.back > 0) {
        scene.el("line", {
          x1: base.x, y1: base.y, x2: neg.x, y2: neg.y, stroke: spec.colors[i],
          "stroke-width": 1.6, "stroke-dasharray": "6 6", opacity: 0.5
        }, layer);
      }
      var tip = scene.project(FK.M4.apply(matrix, FK.Vec.scale(dirs[i], spec.length)));
      scene.el("line", {
        x1: base.x, y1: base.y, x2: tip.x, y2: tip.y,
        stroke: spec.colors[i], "stroke-width": spec.width, opacity: spec.opacity || 1,
        "marker-end": "url(#" + spec.markers[i] + ")"
      }, layer);
      // 轴名放在端点外侧；若与已有标签冲突则在端点周围换方位，实在不行返回原位
      var vx = tip.x - base.x, vy = tip.y - base.y;
      var vl = Math.max(1e-6, Math.sqrt(vx * vx + vy * vy));
      var ux = vx / vl, uy = vy / vl;
      var off = spec.font * 0.72;
      place(tip, labels[i], spec.font, spec.colors[i], [
        [spec.dx[i], spec.dy[i]],
        [ux * off, uy * off + spec.font * 0.42],
        [-uy * off - spec.font * 0.62, ux * off],
        [uy * off, -ux * off + spec.font * 0.42],
        [-ux * off - spec.font * 0.9, uy * off],
        [spec.dx[i], spec.dy[i]]
      ], "fk-axis-label", layer, { "font-style": "italic", opacity: spec.opacity || 1 });
    }
    var o = scene.project(FK.M4.apply(matrix, [0, 0, 0]));
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.2, fill: spec.originFill || "#334155", opacity: spec.opacity || 1 }, layer);
    if (spec.originLabel) {
      place(o, spec.originLabel, 15, spec.originFill || "#475569", spec.originPrefs || [[-46, -8], [-46, 26], [12, 26], [12, -6]], "fk-origin-label");
    }
  }

  function drawComponent(from, to) {
    var a = scene.project(from), b = scene.project(to);
    scene.el("line", {
      x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: "#a9b6c9",
      "stroke-dasharray": "7 6", "stroke-width": 2, class: "fk-projection"
    }, vectorLayer);
  }

  function drawVector(from, to, color, marker, text, opts) {
    var a = scene.project(from), b = scene.project(to);
    scene.el("line", {
      x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: color, "stroke-width": opts.width,
      "stroke-dasharray": opts.dash || null, "marker-end": "url(#" + marker + ")", opacity: opts.opacity || 1
    }, vectorLayer);
    scene.el("circle", { cx: b.x, cy: b.y, r: opts.r, fill: color, class: "fk-point", opacity: opts.opacity || 1 }, vectorLayer);
    place(b, text, opts.font, opts.fill, opts.prefs, "fk-point-label");
  }

  function drawArc(radius, start, end) {
    if (Math.abs(end - start) < 1e-4) return;
    var steps = 44, points = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = start + (end - start) * (i / steps);
      points.push([radius * Math.cos(t), radius * Math.sin(t), 0]);
    }
    scene.polyline(points, { stroke: "#7c3aed", class: "fk-arc" }, angleLayer);
    var mid = start + (end - start) * 0.5;
    place(scene.project([(radius + 0.6) * Math.cos(mid), (radius + 0.6) * Math.sin(mid), 0]), "\u03b8", 16, "#7c3aed", [[-8, 6], [-8, -14], [6, 6]]);
  }

  /* ---------------- 主绘制 ---------------- */
  function render() {
    gridLayer.replaceChildren();
    frameC.replaceChildren();
    axesA.replaceChildren();
    frameB.replaceChildren();
    vectorLayer.replaceChildren();
    angleLayer.replaceChildren();
    labelLayer.replaceChildren();
    boxes = [];

    var theta = state.theta * FK.DEG;
    var Rab = FK.M4.rotZ(theta);
    var PB = [state.Px, state.Py, state.Pz];
    var PBORG = [state.Bx, state.By, state.Bz];
    var step1 = FK.M4.apply(Rab, PB);          // ᴬ_BR·ᴮP：第1步（只旋转）
    var PA = FK.Vec.add(step1, PBORG);         // 式(2-17)：第2步再加平移

    // 自动取景：以关键点与坐标轴端点为准（栅格只作背景，允许略微越界）
    var ak = 2.4;
    var pts = [
      [0, 0, 0], PA, PBORG, step1, PB,
      [ak, 0, 0], [-ak, 0, 0], [0, ak, 0], [0, -ak, 0], [0, 0, ak], [0, 0, -ak]
    ];
    fitView(pts);

    scene.grid(3, 1);

    // 中间坐标系：与 {A} 姿态相同、原点与 {B} 重合（虚线灰架）
    if (state.showC) {
      drawAxes(frameC, FK.M4.translate(PBORG), {
        length: 1.35, back: 0.6, width: 2.4, font: 15,
        labels: ["X\u0302\u1d9c", "Y\u0302\u1d9c", "Z\u0302\u1d9c"],
        colors: [COLORS.C, COLORS.C, COLORS.C], markers: ["mAxis", "mAxis", "mAxis"],
        dx: [5, 6, 9], dy: [-3, 14, -6], originFill: "#94a3b8",
        originLabel: "中间系 C", originPrefs: [[-72, 30], [-72, -6], [12, 28]], opacity: 0.95
      });
    }

    // 坐标系{A}
    drawAxes(axesA, FK.M4.identity(), {
      length: 2.6, back: 1.1, width: 3.0, font: 18,
      labels: ["X\u0302\u2090", "Y\u0302\u2090", "Z\u0302\u2090"],
      colors: [COLORS.A, COLORS.A, COLORS.A], markers: ["mAxis", "mAxis", "mAxis"],
      dx: [10, 10, 12], dy: [-6, -6, -6], originLabel: "O"
    });

    // 坐标系{B}：原点在 ᴬP_BORG、姿态 ᴬ_BR
    drawAxes(frameB, FK.M4.fromRT(FK.M4.rotation(Rab), PBORG), {
      length: 2.3, back: 0.9, width: 3.0, font: 18,
      labels: ["X\u0302\u1d47", "Y\u0302\u1d47", "Z\u0302\u1d47"],
      colors: [COLORS.Bx, COLORS.By, COLORS.Bz], markers: ["mBx", "mBy", "mBz"],
      dx: [9, 10, 11], dy: [-5, -6, -46], originLabel: "O\u2032",
      originPrefs: [[16, 28], [-34, 28], [-34, -8], [16, -8]]
    });

    // 分量虚线（指向当前显示的那个矢量）
    if (state.showComp) {
      var tip = state.step2 ? PA : step1;
      drawComponent([0, 0, 0], [tip[0], 0, 0]);
      drawComponent([tip[0], 0, 0], [tip[0], tip[1], 0]);
      drawComponent([tip[0], tip[1], 0], tip);
      drawComponent(tip, [tip[0], tip[1], 0]);
    }

    // ᴮP（固定在{B}中）
    if (state.showVecB) {
      drawVector(PBORG, PA, COLORS.Bx, "mBx", "\u1d2eP", {
        width: 2.4, dash: "9 5", opacity: 0.85, r: 4.6, font: 16, fill: "#a02a20",
        prefs: [[-42, -10], [-42, 22], [12, -12]]
      });
    }

    // 第1步：ᴬ_BR·ᴮP
    drawVector([0, 0, 0], step1, COLORS.step1, "mVec", "\u1d2c_BR\u00b7\u1d2eP", {
      width: 3.4, opacity: 1, r: 5.4, font: 16, fill: "#0b5a70",
      prefs: [[13, -9], [13, 23], [-96, -9]]
    });

    if (state.step2) {
      // 第2步：平移量 ᴬP_BORG（从中间系原点画到 ᴬP）
      drawVector(PBORG, PA, COLORS.trans, "mTr", "\u1d2cP_BORG", {
        width: 3.4, opacity: 1, r: 5.4, font: 16, fill: "#5b21b6",
        prefs: [[-88, 32, 360], [14, 30], [-88, -12], [14, -14]]
      });
      // 最终 ᴬP
      drawVector([0, 0, 0], PA, COLORS.final, "mFin", "\u1d2cP", {
        width: 4.2, opacity: 1, r: 7, font: 20, fill: "#8a4a08",
        prefs: [[16, -18, 560], [16, 18, 560], [-44, -20]]
      });
    }

    drawArc(1.1, 0, theta);

    document.getElementById("m1").textContent = FK.format(step1[0], 3);
    document.getElementById("m2").textContent = FK.format(step1[1], 3);
    document.getElementById("m3").textContent = FK.format(step1[2], 3);
    document.getElementById("b1").textContent = FK.format(PBORG[0], 3);
    document.getElementById("b2").textContent = FK.format(PBORG[1], 3);
    document.getElementById("b3").textContent = FK.format(PBORG[2], 3);
    document.getElementById("px").textContent = FK.format(PA[0], 3);
    document.getElementById("py").textContent = FK.format(PA[1], 3);
    document.getElementById("pz").textContent = FK.format(PA[2], 3);
    document.getElementById("q1").textContent = FK.format(PB[0], 3);
    document.getElementById("q2").textContent = FK.format(PB[1], 3);
    document.getElementById("q3").textContent = FK.format(PB[2], 3);
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "theta", key: "theta", value: 30, format: function (v) { return FK.deg(v, 1); } },
    { id: "bx", key: "Bx", value: 10, format: function (v) { return FK.format(v, 1); } },
    { id: "by", key: "By", value: 5, format: function (v) { return FK.format(v, 1); } },
    { id: "bz", key: "Bz", value: 0, format: function (v) { return FK.format(v, 1); } },
    { id: "px", key: "Px", value: 3, format: function (v) { return FK.format(v, 1); } },
    { id: "py", key: "Py", value: 7, format: function (v) { return FK.format(v, 1); } },
    { id: "pz", key: "Pz", value: 0, format: function (v) { return FK.format(v, 1); } },
    { id: "showVecB", key: "showVecB", value: 1, format: function (v) { return v ? "显示" : "隐藏"; } },
    {
      id: "auto", key: "auto", value: 0,
      format: function (v) { return v ? "开" : "关"; },
      onChange: function (v) { scene.setAuto(!!v); }
    }
  ], state, render);

  FK.bindToggles([
    { id: "step2", key: "step2" },
    { id: "showC", key: "showC" },
    { id: "showComp", key: "showComp" }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 30;
    state.Bx = 10; state.By = 5; state.Bz = 0;
    state.Px = 3; state.Py = 7; state.Pz = 0;
    state.step2 = true; state.showC = true; state.showComp = true; state.showVecB = 1; state.auto = 0;
    document.getElementById("step2").checked = true;
    document.getElementById("showC").checked = true;
    document.getElementById("showComp").checked = true;
    document.getElementById("showVecB").value = 1;
    scene.setAuto(false);
    document.getElementById("autoValue").textContent = "关";
    ranges.refresh();
    scene.reset();
    render();
  });

  /* 教材自检 1：例2.2（θ=30°、ᴬP_BORG=(10,5,0)、ᴮP=(3,7,0)）→ 式(2-23) ᴬP=(9.098,12.562,0) */
  /* 教材自检 2：两步分解式(2-17) 与齐次变换式(2-18) 结果必须一致 */
  /* 教材自检 3：退化情形（ᴬP_BORG=0、ᴮP=(0,2,0)）→ 例2.1 式(2-16) ᴬP=(−1,√3,0) */
  (function selfTest() {
    var Rab = FK.M4.rotZ(30 * FK.DEG);
    var PBORG = [10, 5, 0];
    var PB = [3, 7, 0];
    var step1 = FK.M4.apply(Rab, PB);
    var PA = FK.Vec.add(step1, PBORG);
    var expected = [9.098, 12.562, 0];
    if (!FK.Vec.eq(FK.Vec.round(PA, 3), expected, 1e-3)) {
      throw new Error("例2.2 数值自检失败：ᴬP = " + JSON.stringify(PA) + "，期望 " + JSON.stringify(expected));
    }
    var T = FK.M4.fromRT(FK.M4.rotation(Rab), PBORG);
    var direct = FK.M4.apply(T, PB);
    if (!FK.Vec.eq(FK.Vec.round(direct, 9), FK.Vec.round(PA, 9), 1e-9)) {
      throw new Error("式(2-17) 与式(2-18) 结果不一致：" + JSON.stringify(direct));
    }
    var pure = FK.M4.apply(FK.M4.rotZ(30 * FK.DEG), [0, 2, 0]);
    if (!FK.Vec.eq(FK.Vec.round(pure, 6), FK.Vec.round([-1, Math.sqrt(3), 0], 6), 1e-6)) {
      throw new Error("例2.1 退化情形自检失败：" + JSON.stringify(pure));
    }
  }());

  scene.setAuto(false);
  render();
}());
"""

FIGURE = {
    "id": "figure-2-7",
    "title": "图2-7 在一般情况下的矢量变换 · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}

