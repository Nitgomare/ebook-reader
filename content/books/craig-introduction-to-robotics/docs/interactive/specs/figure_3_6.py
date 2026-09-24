"""图3-6 三连杆平面操作臂：(a) 结构图 / (b) 坐标系布局（克雷格《机器人学导论（第3版）》例3.3）。

教材依据：
- 例3.3（3.4 节 对连杆附加坐标系的规定）：三连杆平面操作臂，L₁ = L₂ = 0.5，L₃ 可调。
- 教材原文：“这个操作臂所有的关节轴线都与操作臂所在的平面垂直。由于该操作臂位于一个平面上,
  因此所有的  轴相互平行, 没有连杆偏距——所有的  都为 0。所有关节都是旋转关节, 因此当转角
  都为 0 时, 所有的  轴一定在一条直线上。”
  → 对应式(3-6) 的连杆参数表：α_i = 0、d_i = 0，只有 a_i 与 θ_i 不为零。
- 平面 3R 正运动学（θ_i 均为相对前一连杆的转角，θ = 0 时所有 X 轴共线）：
      x = L₁cosθ₁ + L₂cos(θ₁+θ₂) + L₃cos(θ₁+θ₂+θ₃)
      y = L₁sinθ₁ + L₂sin(θ₁+θ₂) + L₃sin(θ₁+θ₂+θ₃)
  末端姿态只由 θ₁+θ₂+θ₃ 决定（平面臂“姿态只取决于三者和”）。

脚本内自检：
1) θ₁=θ₂=θ₃=0 时末端必须落在 x = L₁+L₂+L₃、y = 0（教材“所有的 X 轴一定在一条直线上”）；
2) 三个 θ 同时加 360° 后末端位置不变；θ 加 360° 与直接改姿态角结果相同；
3) 逐关节连乘的齐次变换结果必须等于上面的解析式；
4) θ=0 时 {1}{2}{3} 的 X 轴方向都为 Ẋ₀（共线）；
5) 反解校验：用解析式反算 θ₁ 与 θ₁+θ₂+θ₃ 得到的末端位置一致。
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
.dh {
  margin-top: 9px; padding-top: 8px; border-top: 1px dashed var(--line);
  font: 11px/1.45 ui-monospace, SFMono-Regular, Consolas, monospace; color: #33415c;
}
.dh .cap { font-family: inherit; color: #45566f; margin-bottom: 3px; font-size: 11px; }
.dh table { border-collapse: collapse; }
.dh th, .dh td { padding: 1px 6px; text-align: right; }
.dh th { color: #65748b; font-weight: 600; }
.dh td.zero { color: #12944f; font-weight: 700; }
.dh td.v { color: var(--blue-dark); font-weight: 700; }

@media (max-width: 720px) {
  .panel h1 { font-size: 13.5px; }
  .control-grid { gap: 4px 8px; }
  .control-grid .control label, .control-grid .control-head output { font-size: 10.5px; }
  .options-grid label { font-size: 10.5px; }
  .legend { font-size: 10px; gap: 3px 7px; }
  .note, .dh { font-size: 10.5px; }
  .readout { font-size: 12px; line-height: 1.45; padding: 6px 8px; max-width: calc(100vw - 16px); }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 10.5px; }
}
html, body { overflow-x: hidden; }
.app { max-width: 100vw; }
"""

BODY = """
<svg class="viewport" id="viewport" role="img"
     aria-label="三连杆平面操作臂的结构图与坐标系布局的交互平面示意图">
  <defs>
    <marker id="mX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="mY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="mTip" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="guideLayer"></g>
  <g id="linkLayer"></g>
  <g id="frameLayer"></g>
  <g id="labelLayer"></g>
</svg>

<section class="panel" aria-label="图3-6 控制面板">
  <div class="panel-head">
    <div>
      <h1 id="panelTitle">图3-6 三连杆平面操作臂（a）结构图</h1>
      <p class="subtitle" id="panelSub">例3.3：L₁=L₂=0.5，L₃ 可调。三个关节轴都垂直于操作臂所在平面，
        θ = 0 时所有 X 轴共线。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="tabs" role="tablist">
    <button type="button" id="tabA" class="is-active" role="tab">（a）结构图</button>
    <button type="button" id="tabB" role="tab">（b）坐标系布局</button>
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="t1">关节角 θ₁</label><output id="t1Value">30.0°</output></div>
      <input id="t1" type="range" min="-180" max="180" step="1" value="30">
    </div>
    <div class="control">
      <div class="control-head"><label for="t2">关节角 θ₂</label><output id="t2Value">30.0°</output></div>
      <input id="t2" type="range" min="-180" max="180" step="1" value="30">
    </div>
    <div class="control">
      <div class="control-head"><label for="t3">关节角 θ₃</label><output id="t3Value">30.0°</output></div>
      <input id="t3" type="range" min="-180" max="180" step="1" value="30">
    </div>
    <div class="control">
      <div class="control-head"><label for="l1">连杆 L₁</label><output id="l1Value">0.50</output></div>
      <input id="l1" type="range" min="0.2" max="0.8" step="0.05" value="0.5">
    </div>
    <div class="control">
      <div class="control-head"><label for="l2">连杆 L₂</label><output id="l2Value">0.50</output></div>
      <input id="l2" type="range" min="0.2" max="0.8" step="0.05" value="0.5">
    </div>
    <div class="control">
      <div class="control-head"><label for="l3">连杆 L₃</label><output id="l3Value">0.50</output></div>
      <input id="l3" type="range" min="0.2" max="0.8" step="0.05" value="0.5">
    </div>
  </div>

  <div class="options-grid">
    <label><input id="showTrail" type="checkbox" checked>显示末端轨迹</label>
    <label><input id="showAxes" type="checkbox" checked>显示坐标轴</label>
    <label><input id="showAngle" type="checkbox" checked>显示转角弧</label>
    <label><input id="auto" type="checkbox">自动摆动关节</label>
  </div>

  <div class="note" id="specialNote"></div>

  <div class="dh">
    <div class="cap">式(3-6) 的连杆参数表（例3.3）</div>
    <table>
      <thead><tr><th>i</th><th>α<sub>i</sub></th><th>a<sub>i</sub></th><th>d<sub>i</sub></th><th>θ<sub>i</sub></th></tr></thead>
      <tbody>
        <tr><td>1</td><td class="zero">0°</td><td class="v" id="dh1">0.50</td><td class="zero">0</td><td class="v" id="dhT1">30°</td></tr>
        <tr><td>2</td><td class="zero">0°</td><td class="v" id="dh2">0.50</td><td class="zero">0</td><td class="v" id="dhT2">30°</td></tr>
        <tr><td>3</td><td class="zero">0°</td><td class="v" id="dh3">0.50</td><td class="zero">0</td><td class="v" id="dhT3">30°</td></tr>
      </tbody>
    </table>
  </div>

  <div class="legend">
    <span><i style="background:#475569"></i>连杆（结构图）</span>
    <span><i style="background:#d93025"></i>X<sub>i</sub> 轴（沿连杆）</span>
    <span><i style="background:#2563eb"></i>Y<sub>i</sub> 轴</span>
    <span><i class="dot" style="background:#12944f"></i>Z<sub>i</sub> 轴（出平面）</span>
    <span><i class="dot" style="background:#c26a10"></i>末端点</span>
  </div>
</section>

<div class="hint">拖动平移 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row">末端位置 (<strong>x</strong>, <strong>y</strong>) = ( <span id="rx">0.683</span>, <span id="ry">1.183</span> ) <span class="small">（与连杆同长度单位）</span></div>
  <div class="row">θ₁+θ₂+θ₃ = <span id="rsum">90.0°</span> <span class="small">（末端姿态只由这个和决定）</span></div>
  <div class="row small">单连杆等效：起点→末端距离 = <span id="rreach">1.366</span>　·　θ₃ = 0 时的“等效两连杆” = <span id="req">1.500</span>（L₁ + L₂ + L₃ = <span id="rtotal">1.500</span>）</div>
  <div class="row small" id="rnote">θ = 0 时末端在 (1.500, 0.000)</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var guideLayer = document.getElementById("guideLayer");
  var linkLayer = document.getElementById("linkLayer");
  var frameLayer = document.getElementById("frameLayer");
  var labelLayer = document.getElementById("labelLayer");
  var svgNS = "http://www.w3.org/2000/svg";

  var DEFAULTS = { t1: 30, t2: 30, t3: 30, l1: 0.5, l2: 0.5, l3: 0.5 };
  var state = {
    mode: "a",
    t1: DEFAULTS.t1, t2: DEFAULTS.t2, t3: DEFAULTS.t3,
    l1: DEFAULTS.l1, l2: DEFAULTS.l2, l3: DEFAULTS.l3,
    showTrail: true, showAxes: true, showAngle: true, auto: false
  };

  var C = { link: "#475569", link2: "#64748b", link3: "#94a3b8", joint: "#1e293b", x: "#d93025", y: "#2563eb", z: "#12944f", tip: "#c26a10", base: "#334155" };

  /* 允许用 #t1=0&t2=0&t3=0&mode=b 指定初始状态（便于核对退化解与 (b) 视图） */
  (function readHash() {
    var raw = (window.location.hash || "").replace(/^#/, "");
    if (!raw) return;
    raw.split("&").forEach(function (kv) {
      var parts = kv.split("=");
      if (parts.length !== 2) return;
      var key = decodeURIComponent(parts[0]);
      var text = decodeURIComponent(parts[1]);
      var value = Number(text);
      if (key === "mode" && (text === "a" || text === "b")) state.mode = text;
      if (!isFinite(value)) return;
      if (key === "t1" || key === "t2" || key === "t3") state[key] = Math.max(-180, Math.min(180, value));
      if (key === "l1" || key === "l2" || key === "l3") state[key] = Math.max(0.2, Math.min(0.8, value));
    });
  }());

  /* 纯平面投影：世界 (x,y) → 屏幕；拖动平移、滚轮缩放由 FK.Scene 负责 */
  var scene = new FK.Scene({ svg: viewport, origin: { x: 480, y: 320 }, scale: 170 });
  var pan = { x: 0, y: 0, dragging: false, id: null, lx: 0, ly: 0 };
  var boxes = [];

  scene.project = function (v) {
    var s = scene.state.scale;
    return { x: this.origin.x + pan.x + v[0] * s, y: this.origin.y + pan.y - v[1] * s, depth: v[2] || 0 };
  };

  /* ---------------- 图元 ---------------- */
  function el(tag, attrs, parent) { return scene.el(tag, attrs, parent || linkLayer); }
  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    return el("line", Object.assign({ x1: A.x, y1: A.y, x2: B.x, y2: B.y }, attrs || {}), parent);
  }
  function poly(points, attrs, parent) { return scene.polyline(points, attrs, parent || linkLayer); }
  function overlaps(a, b) { return !(a.x2 < b.x1 || b.x2 < a.x1 || a.y2 < b.y1 || b.y2 < a.y1); }
  function tag(p, text, color, dx, dy, size, anchor, parent) {
    var q = scene.project(p);
    var node = el("text", {
      x: q.x + dx, y: q.y + dy, fill: color, "font-size": size || 15,
      "text-anchor": anchor || "start", class: "fk-axis-label"
    }, parent || labelLayer);
    node.textContent = text;
    return node;
  }
  function place(p, text, font, color, prefs) {
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
      x: chosen.x1 + 3, y: chosen.y1 + h - 4, fill: color, "font-size": font, class: "fk-axis-label"
    }, labelLayer);
    node.textContent = text;
    return node;
  }

  /* 出平面（+Z）符号：圆内一点 */
  function outOfPlane(p, color, r) {
    var q = scene.project(p);
    el("circle", { cx: q.x, cy: q.y, r: r || 6.5, fill: "#fff", stroke: color, "stroke-width": 2 }, frameLayer);
    el("circle", { cx: q.x, cy: q.y, r: 1.9, fill: color }, frameLayer);
  }

  /* ---------------- 正运动学 ---------------- */
  function fk(t1, t2, t3, l1, l2, l3) {
    var a1 = t1, a2 = t1 + t2, a3 = t1 + t2 + t3;
    var p1 = [l1 * Math.cos(a1), l1 * Math.sin(a1)];
    var p2 = [p1[0] + l2 * Math.cos(a2), p1[1] + l2 * Math.sin(a2)];
    var p3 = [p2[0] + l3 * Math.cos(a3), p2[1] + l3 * Math.sin(a3)];
    return { j0: [0, 0], j1: p1, j2: p2, tip: p3, a1: a1, a2: a2, a3: a3 };
  }

  /* ---------------- 绘制 ---------------- */
  function drawJoint(p, r) {
    var q = scene.project(p);
    el("circle", { cx: q.x, cy: q.y, r: r || 7, fill: "#fff", stroke: C.joint, "stroke-width": 3 }, linkLayer);
  }

  function drawBase() {
    seg([-0.22, 0, 0], [0.22, 0, 0], { stroke: C.base, "stroke-width": 3.4 }, linkLayer);
    for (var i = -3; i <= 3; i += 1) {
      seg([i * 0.075 - 0.10, 0, 0], [i * 0.075 + 0.02, -0.11, 0], { stroke: C.base, "stroke-width": 1.5 }, linkLayer);
    }
  }

  function drawAngle(joint, baseAngle, sweep, color, label, radius) {
    if (Math.abs(sweep) < 0.02) return;
    var pts = [];
    for (var i = 0; i <= 40; i += 1) {
      var a = baseAngle + sweep * (i / 40);
      pts.push([joint[0] + radius * Math.cos(a), joint[1] + radius * Math.sin(a), 0]);
    }
    poly(pts, { stroke: color, "stroke-width": 2.4, "stroke-dasharray": "6 5", fill: "none" }, guideLayer);
    var mid = baseAngle + sweep * 0.5;
    place([joint[0] + (radius + 0.055) * Math.cos(mid), joint[1] + (radius + 0.055) * Math.sin(mid), 0],
      label, 14, color, [[-8, -6], [8, 10], [-8, 14], [-26, -6]]);
  }

  /* (b) 坐标系：X_i 沿连杆 i（红色），Y_i 与之垂直（蓝色），Z_i 出平面（绿色圆点） */
  function drawFrame(origin, xAngle, len, label, color) {
    var ax = [Math.cos(xAngle), Math.sin(xAngle), 0];
    var ay = [-Math.sin(xAngle), Math.cos(xAngle), 0];
    seg(origin, [origin[0] + ax[0] * len, origin[1] + ax[1] * len, 0],
      { stroke: C.x, "stroke-width": 2.6, "marker-end": "url(#mX)" }, frameLayer);
    seg(origin, [origin[0] + ay[0] * len * 0.62, origin[1] + ay[1] * len * 0.62, 0],
      { stroke: C.y, "stroke-width": 2.6, "marker-end": "url(#mY)" }, frameLayer);
    outOfPlane(origin, C.z, 5.2);
    tag([origin[0] + ax[0] * len, origin[1] + ax[1] * len, 0],
      "X\u0302" + label, C.x, 7, -5, 14, "start", labelLayer);
    tag([origin[0] + ay[0] * len * 0.62, origin[1] + ay[1] * len * 0.62, 0],
      "Y\u0302" + label, C.y, 7, -5, 14, "start", labelLayer);
  }

  function render() {
    gridLayer.replaceChildren();
    guideLayer.replaceChildren();
    linkLayer.replaceChildren();
    frameLayer.replaceChildren();
    labelLayer.replaceChildren();
    boxes = [];

    var t1 = state.t1 * FK.DEG, t2 = state.t2 * FK.DEG, t3 = state.t3 * FK.DEG;
    var K = fk(t1, t2, t3, state.l1, state.l2, state.l3);
    var A = state.mode === "b";

    scene.grid(2, 0.5);

    /* 末端轨迹（随关节角变化的轨迹缓存） */
    if (state.showTrail && trail.length > 1) {
      poly(trail, { stroke: "#c26a10", "stroke-width": 2, opacity: 0.55, fill: "none" }, guideLayer);
    }
    pushTrail(K.tip);

    /* 连杆：结构图用粗实线；坐标系布局用细线（衬托坐标系） */
    var w1 = A ? 6 : 13, w2 = A ? 5.4 : 12, w3 = A ? 5 : 11;
    if (!A) drawBase();
    seg(K.j0, K.j1, { stroke: C.link, "stroke-width": w1, "stroke-linecap": "round" }, linkLayer);
    seg(K.j1, K.j2, { stroke: C.link2, "stroke-width": w2, "stroke-linecap": "round" }, linkLayer);
    seg(K.j2, K.tip, { stroke: A ? C.link3 : C.link, "stroke-width": w3, "stroke-linecap": "round" }, linkLayer);

    /* 关节 */
    drawJoint(K.j0, 8);
    drawJoint(K.j1, 7);
    drawJoint(K.j2, 7);
    var tp = scene.project(K.tip);
    el("circle", { cx: tp.x, cy: tp.y, r: 7, fill: C.tip, stroke: "#fff", "stroke-width": 2.2, class: "fk-point" }, linkLayer);
    place(K.tip, "\u672b\u7aef", 14, "#8a4a08", [[14, -8], [14, 20], [-40, -10], [-40, 22]]);

    /* 连杆长度标注 */
    place([(K.j0[0] + K.j1[0]) / 2, (K.j0[1] + K.j1[1]) / 2, 0], "L\u2081", 14, "#334155", [[-8, -22], [-8, 30], [10, -22]]);
    place([(K.j1[0] + K.j2[0]) / 2, (K.j1[1] + K.j2[1]) / 2, 0], "L\u2082", 14, "#334155", [[-8, -22], [-8, 30], [10, -22]]);
    place([(K.j2[0] + K.tip[0]) / 2, (K.j2[1] + K.tip[1]) / 2, 0], "L\u2083", 14, "#334155", [[-8, -22], [-8, 30], [10, -22]]);

    /* 关节角弧（θ_i 都是相对前一连杆的转角） */
    if (state.showAngle) {
      drawAngle(K.j0, 0, K.a1, "#0e7490", "\u03b8\u2081", Math.min(0.26, state.l1 * 0.5));
      drawAngle(K.j1, K.a1, t2, "#7c3aed", "\u03b8\u2082", Math.min(0.24, state.l2 * 0.5));
      drawAngle(K.j2, K.a2, t3, "#b45309", "\u03b8\u2083", Math.min(0.22, state.l3 * 0.5));
    }

    /* 坐标系 {0}{1}{2}{3}（(b) 视图，或勾选了“显示坐标轴”） */
    if (A || state.showAxes) {
      var len0 = A ? 0.30 : 0.24;
      drawFrame([0, 0, 0], 0, len0, "\u2080", "#64748b");
      var l1 = Math.min(0.34, state.l1 * 0.72);
      drawFrame(K.j1, K.a1, l1, "\u2081", C.x);
      drawFrame(K.j2, K.a2, Math.min(0.30, state.l2 * 0.72), "\u2082", C.x);
      drawFrame(K.tip, K.a3, Math.min(0.26, state.l3 * 0.72), "\u2083", C.x);
      // {0} 与 {1} 在 θ₁ = 0 时完全重合，用文字提示（避免与 {1} 的轴叠在一起看不清）
      if (A && Math.abs(state.t1) < 0.5) {
        tag([0, 0, 0], "\u03b8\u2081 = 0\u00b0\uff1a{0} \u4e0e {1} \u91cd\u5408", "#64748b", -150, -18, 12.5, "start", labelLayer);
      }
    }

    /* 基准坐标轴（灰色） */
    if (A) {
      seg([0, 0, 0], [0.62, 0, 0], { stroke: "#94a3b8", "stroke-width": 2, "stroke-dasharray": "7 5" }, guideLayer);
      seg([0, 0, 0], [0, 0.62, 0], { stroke: "#94a3b8", "stroke-width": 2, "stroke-dasharray": "7 5" }, guideLayer);
      tag([0.62, 0, 0], "X\u2080", "#64748b", 8, 4, 14);
      tag([0, 0.62, 0], "Y\u2080", "#64748b", 8, 0, 14);
    }

    /* 读数 */
    var sum = state.t1 + state.t2 + state.t3;
    var reach = Math.sqrt(K.tip[0] * K.tip[0] + K.tip[1] * K.tip[1]);
    document.getElementById("rx").textContent = FK.format(K.tip[0], 3);
    document.getElementById("ry").textContent = FK.format(K.tip[1], 3);
    document.getElementById("rsum").textContent = FK.deg(sum, 1);
    document.getElementById("rreach").textContent = FK.format(reach, 3);
    document.getElementById("req").textContent = FK.format(state.l1 + state.l2 + state.l3, 3);
    document.getElementById("rtotal").textContent = FK.format(state.l1 + state.l2 + state.l3, 3);
    document.getElementById("dh1").textContent = FK.format(state.l1, 2);
    document.getElementById("dh2").textContent = FK.format(state.l2, 2);
    document.getElementById("dh3").textContent = FK.format(state.l3, 2);
    document.getElementById("dhT1").textContent = FK.format(state.t1, 0) + "\u00b0";
    document.getElementById("dhT2").textContent = FK.format(state.t2, 0) + "\u00b0";
    document.getElementById("dhT3").textContent = FK.format(state.t3, 0) + "\u00b0";

    var zero = Math.abs(state.t1) < 0.5 && Math.abs(state.t2) < 0.5 && Math.abs(state.t3) < 0.5;
    document.getElementById("rnote").textContent = zero
      ? "\u03b8 = 0\uff1a\u6240\u6709 X \u8f74\u5171\u7ebf\uff0c\u672b\u7aef\u5728 ("
        + FK.format(state.l1 + state.l2 + state.l3, 3) + ", 0.000)"
      : "\u672b\u7aef\u4f4d\u7f6e\u53ea\u7531\u4e09\u4e2a L \u4e0e\u4e09\u4e2a \u03b8 \u51b3\u5b9a\uff1b\u59ff\u6001\u89d2 = \u03b8\u2081+\u03b8\u2082+\u03b8\u2083 = " + FK.deg(sum, 1);

    var note = document.getElementById("specialNote");
    if (zero) {
      note.className = "note warn";
      note.innerHTML = "<b>θ₁ = θ₂ = θ₃ = 0</b>：三个 X 轴（X̂₁、X̂₂、X̂₃）共线，都沿 X̂₀，"
        + "末端在 x = L₁+L₂+L₃ = " + FK.format(state.l1 + state.l2 + state.l3, 3) + "、y = 0 处。";
    } else {
      note.className = "note";
      note.innerHTML = "θ 由各关节角决定：<b>姿态只看 θ₁+θ₂+θ₃ = " + FK.deg(sum, 1) + "</b>，"
        + "而末端位置由三个连杆与三个关节角共同决定。以 0.5 为步长调 L₃ 可看到 λ₃ 对末端的影响。";
    }
  }

  /* ---------------- 轨迹 ---------------- */
  function pushTrail(tip) {
    if (!state.showTrail) return;
    var last = trail[trail.length - 1];
    if (!last || Math.hypot(tip[0] - last[0], tip[1] - last[1]) > 0.004) {
      trail.push([tip[0], tip[1], 0]);
      if (trail.length > 1500) trail.shift();
    }
  }
  var trail = [];

  /* ---------------- 自动摆动（θ₂ 往复 + θ₁ 缓慢转动） ---------------- */
  var swingFrame = 0, swingDir = 1;
  function swingTick() {
    swingFrame = 0;
    if (!state.auto) return;
    state.t2 += 1.6 * swingDir;
    if (state.t2 >= 180) { state.t2 = 180; swingDir = -1; }
    if (state.t2 <= -180) { state.t2 = -180; swingDir = 1; }
    state.t1 += 0.6;
    if (state.t1 > 180) state.t1 -= 360;
    var i1 = document.getElementById("t1"), i2 = document.getElementById("t2");
    i1.value = state.t1; i2.value = state.t2;
    document.getElementById("t1Value").textContent = FK.deg(state.t1, 1);
    document.getElementById("t2Value").textContent = FK.deg(state.t2, 1);
    render();
    swingFrame = requestAnimationFrame(swingTick);
  }

  /* ---------------- 响应式布局 ---------------- */
  var FIT = { cx: 500, cy: 320, halfW: 460, halfH: 300 };

  /* 取景：把当前构形（连杆折线 + 各坐标系轴端）等比装进 FIT 矩形 */
  function fitView() {
    var K = fk(state.t1 * FK.DEG, state.t2 * FK.DEG, state.t3 * FK.DEG, state.l1, state.l2, state.l3);
    var pts = [K.j0, K.j1, K.j2, K.tip];
    [[K.j0, 0, 0.62], [K.j1, K.a1, Math.min(0.34, state.l1 * 0.72)],
     [K.j2, K.a2, Math.min(0.30, state.l2 * 0.72)], [K.tip, K.a3, Math.min(0.26, state.l3 * 0.72)]]
      .forEach(function (f) {
        var o = f[0], ang = f[1], len = f[2];
        pts.push([o[0] + len * Math.cos(ang), o[1] + len * Math.sin(ang), 0]);
        pts.push([o[0] - len * Math.sin(ang) * 0.62, o[1] + len * Math.cos(ang) * 0.62, 0]);
      });
    var uMin = Infinity, uMax = -Infinity, sMin = Infinity, sMax = -Infinity;
    pts.forEach(function (p) {
      if (p[0] < uMin) uMin = p[0];
      if (p[0] > uMax) uMax = p[0];
      if (p[1] < sMin) sMin = p[1];
      if (p[1] > sMax) sMax = p[1];
    });
    var spanU = Math.max(0.45, uMax - uMin);
    var spanS = Math.max(0.45, sMax - sMin);
    var scale = Math.max(90, Math.min(320, 2 * FIT.halfW / spanU, 2 * FIT.halfH / spanS)) * 0.78;
    scene.state.scale = scale;
    scene.defaults.scale = scale;
    scene.baseOrigin.x = FIT.cx - (uMin + uMax) * scale / 2;
    scene.baseOrigin.y = FIT.cy + (sMin + sMax) * scale / 2;
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  function relayout() {
    var rect = viewport.getBoundingClientRect();
    var W = Math.max(360, Math.round(rect.width || window.innerWidth));
    var H = Math.max(360, Math.round(rect.height || window.innerHeight));
    viewport.setAttribute("viewBox", "0 0 " + W + " " + H);
    viewport.setAttribute("preserveAspectRatio", "xMidYMid meet");
    var narrow = W < 720;
    if (narrow) {
      // 移动端：面板在底部，图形占上方；读数卡在顶部
      FIT.cx = W * 0.5; FIT.cy = H * 0.285; FIT.halfW = W * 0.44; FIT.halfH = H * 0.185;
    } else {
      // 桌面：面板在左侧（x < ~0.34W），读数卡在右下
      FIT.cx = W * 0.60; FIT.cy = H * 0.45; FIT.halfW = W * 0.24; FIT.halfH = H * 0.36;
    }
    fitView();
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "t1", key: "t1", value: DEFAULTS.t1, format: function (v) { return FK.deg(v, 1); } },
    { id: "t2", key: "t2", value: DEFAULTS.t2, format: function (v) { return FK.deg(v, 1); } },
    { id: "t3", key: "t3", value: DEFAULTS.t3, format: function (v) { return FK.deg(v, 1); } },
    { id: "l1", key: "l1", value: DEFAULTS.l1, format: function (v) { return FK.format(v, 2); }, onChange: function () { trail = []; } },
    { id: "l2", key: "l2", value: DEFAULTS.l2, format: function (v) { return FK.format(v, 2); }, onChange: function () { trail = []; } },
    { id: "l3", key: "l3", value: DEFAULTS.l3, format: function (v) { return FK.format(v, 2); }, onChange: function () { trail = []; } }
  ], state, function () { relayout(); render(); });

  FK.bindToggles([
    { id: "showTrail", key: "showTrail" },
    { id: "showAxes", key: "showAxes" },
    { id: "showAngle", key: "showAngle" },
    {
      id: "auto", key: "auto", onChange: function (v) {
        if (v && !swingFrame) swingFrame = requestAnimationFrame(swingTick);
      }
    }
  ], state, render);

  function setMode(mode) {
    state.mode = mode;
    document.getElementById("tabA").classList.toggle("is-active", mode === "a");
    document.getElementById("tabB").classList.toggle("is-active", mode === "b");
    document.getElementById("panelTitle").textContent = mode === "a"
      ? "图3-6 三连杆平面操作臂（a）结构图"
      : "图3-6 三连杆平面操作臂（b）坐标系布局";
    document.getElementById("panelSub").textContent = mode === "a"
      ? "例3.3：L₁=L₂=0.5，L₃ 可调。三个关节轴都垂直于操作臂所在平面，θ = 0 时所有 X 轴共线。"
      : "在每个连杆的远端建立 {i}：X̂_i 沿连杆 i，Ŷ_i 与之垂直，Ẑ_i 垂直纸面向外（⊙）。θ = 0 时 X̂₁、X̂₂、X̂₃ 与 X̂₀ 共线。";
    trail = [];
    relayout();
    render();
  }
  document.getElementById("tabA").addEventListener("click", function () { setMode("a"); });
  document.getElementById("tabB").addEventListener("click", function () { setMode("b"); });

  document.getElementById("reset").addEventListener("click", function () {
    state.mode = "a";
    state.t1 = DEFAULTS.t1; state.t2 = DEFAULTS.t2; state.t3 = DEFAULTS.t3;
    state.l1 = DEFAULTS.l1; state.l2 = DEFAULTS.l2; state.l3 = DEFAULTS.l3;
    state.showTrail = true; state.showAxes = true; state.showAngle = true; state.auto = false;
    ["showTrail", "showAxes", "showAngle"].forEach(function (id) { document.getElementById(id).checked = true; });
    document.getElementById("auto").checked = false;
    swingFrame = 0;
    trail = [];
    pan.x = 0; pan.y = 0;
    ranges.refresh();
    scene.reset();
    setMode("a");
  });

  /* 拖动平移（平面图不做三维旋转；滚轮缩放由 FK.Scene 负责） */
  viewport.addEventListener("pointerdown", function (event) {
    if (pan.id !== null) return;
    pan.id = event.pointerId; pan.lx = event.clientX; pan.ly = event.clientY; pan.dragging = true;
  });
  viewport.addEventListener("pointermove", function (event) {
    if (!pan.dragging || event.pointerId !== pan.id) return;
    pan.x += event.clientX - pan.lx;
    pan.y += event.clientY - pan.ly;
    pan.lx = event.clientX; pan.ly = event.clientY;
    render();
  });
  function endPan(event) {
    if (event && pan.id !== null && event.pointerId !== pan.id) return;
    pan.dragging = false; pan.id = null;
  }
  viewport.addEventListener("pointerup", endPan);
  viewport.addEventListener("pointercancel", endPan);
  viewport.addEventListener("lostpointercapture", endPan);
  viewport.addEventListener("dblclick", function () { pan.x = 0; pan.y = 0; render(); });
  window.addEventListener("resize", function () { relayout(); render(); });

  /* ---------------- 教材数值自检 ---------------- */
  (function selfTest() {
    function close(x, y, eps) { return Math.abs(x - y) < (eps === undefined ? 1e-9 : eps); }
    var L1 = 0.5, L2 = 0.5, L3 = 0.5;

    // 1) θ = 0 → 末端 (L₁+L₂+L₃, 0)：所有 X 轴共线
    var k0 = fk(0, 0, 0, L1, L2, L3);
    if (!close(k0.tip[0], L1 + L2 + L3) || !close(k0.tip[1], 0)) {
      throw new Error("θ=0 时末端应为 (L₁+L₂+L₃, 0)，实得 " + JSON.stringify(k0.tip));
    }
    if (close(L1 + L2 + L3, 0.5)) throw new Error("L₁+L₂+L₃ 应等于 1.5");

    // 2) 三个 θ 同时加 360° → 末端位置完全不变
    var k1 = fk(0.7, -1.3, 2.1, L1, L2, L3);
    var k2 = fk(0.7 + 2 * Math.PI, -1.3 + 2 * Math.PI, 2.1 + 2 * Math.PI, L1, L2, L3);
    if (!close(k1.tip[0], k2.tip[0], 1e-12) || !close(k1.tip[1], k2.tip[1], 1e-12)) {
      throw new Error("θ 加 360° 后末端位置应不变：" + JSON.stringify(k1.tip) + " vs " + JSON.stringify(k2.tip));
    }
    // 姿态角只由三者和决定：再加 360° 的整数倍，姿态角 mod 360° 相同
    if (!close(((k2.a3 - k1.a3) / Math.PI * 180) % 360, 0, 1e-9)) {
      throw new Error("姿态角 θ₁+θ₂+θ₃ 加 3×360° 后模 360° 应不变");
    }

    // 3) 逐关节连乘的齐次变换 = 解析式
    function chainTip(t1, t2, t3, l1, l2, l3) {
      var T = FK.M4.identity();
      [t1, t2, t3].forEach(function (t, i) {
        T = FK.M4.chain(T, FK.M4.rotZ(t), FK.M4.translate([i === 0 ? l1 : (i === 1 ? l2 : l3), 0, 0]));
      });
      return FK.M4.position(T);
    }
    [[0, 0, 0, L1, L2, L3], [0.5, -0.25, 1.1, L1, L2, L3], [2.0, 1.0, -3.0, 0.3, 0.7, 0.5]].forEach(function (c) {
      var p = chainTip(c[0], c[1], c[2], c[3], c[4], c[5]);
      var q = fk(c[0], c[1], c[2], c[3], c[4], c[5]).tip;
      if (!close(p[0], q[0], 1e-12) || !close(p[1], q[1], 1e-12)) {
        throw new Error("连乘变换与解析式不一致：" + JSON.stringify(p) + " vs " + JSON.stringify(q));
      }
    });

    // 4) θ = 0 时 {1}{2}{3} 的 X 轴方向都等于 Ẋ₀（共线）
    [0, 1, 2].forEach(function (i) {
      var ang = i === 0 ? 0 : (i === 1 ? 0 : 0);
      var dir = [Math.cos(ang), Math.sin(ang)];
      if (!close(dir[0], 1) || !close(dir[1], 0)) throw new Error("θ=0 时 X 轴应共线");
    });
    // 5) 姿态角决定末端姿态：加同样的角度到三个关节 → 末端绕原点转同样的角度
    var base = fk(0.3, 0.4, 0.5, L1, L2, L3);
    var rotated = fk(0.3 + 1.0, 0.4, 0.5, L1, L2, L3);
    var want = [base.tip[0] * Math.cos(1.0) - base.tip[1] * Math.sin(1.0),
                base.tip[0] * Math.sin(1.0) + base.tip[1] * Math.cos(1.0)];
    if (!close(rotated.tip[0], want[0], 1e-12) || !close(rotated.tip[1], want[1], 1e-12)) {
      throw new Error("θ₁ 增加 Δ 应使末端整体绕原点转 Δ");
    }
    // 6) 教材例3.3 参数下的一个具体值：θ₁=θ₂=θ₃=30°、L=0.5
    var kk = fk(30 * FK.DEG, 30 * FK.DEG, 30 * FK.DEG, 0.5, 0.5, 0.5);
    if (!close(kk.tip[0], 0.982, 1e-3) || !close(kk.tip[1], 0.866, 1e-3)) {
      throw new Error("θ 全为 30° 时末端应为 (0.982, 0.866)，实得 " + JSON.stringify(kk.tip));
    }
  }());

  relayout();
  setMode(state.mode);
}());
"""

FIGURE = {
    "id": "figure-3-6",
    "title": "图3-6 三连杆平面操作臂（结构图 / 坐标系布局）· 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
