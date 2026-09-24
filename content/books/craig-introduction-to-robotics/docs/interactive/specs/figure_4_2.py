"""图4-2 三连杆操作臂（虚线代表第二个解）——克雷格《机器人学导论（第3版）》4.2 节。

教材依据：
- 4.2 节原文：“图4-2所示为在某一位姿下带有末端执行器的三连杆平面操作臂。虚线表示第二个
  可能的位形，在这个位形下，末端操作器的可达位姿与第一个位形相同。”
- 式(4-12)：x² + y² = l1² + l2² + 2·l1·l2·c2 → 式(4-14)：c2 = (x²+y²−l1²−l2²)/(2l1l2)；
- 式(4-15)：s2 = ±√(1−c2²)，正负号的两种取法就是图中的实线解与虚线解（θ2 取相反符号）；
- 式(4-16)：θ2 = Atan2(s2, c2)；式(4-28)：θ1+θ2+θ3 = Atan2(sφ, cφ) = φ。

本图要点：同一个末端位姿 (x, y, φ) 对应两组关节角，两组解的末端位置**完全重合**，
只有中间关节的转角符号相反。脚本内用正运动学做了误差断言（< 1e-9）。

说明：教材把 T 取在腕部（坐标系{3}的原点，即第三连杆末端），此时第三连杆的方位角就是 φ；
本图把 l3 也暴露成滑块（默认 0.4），l3 不为 0 时目标点 T 就是带工具的操作臂末端。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.panel h1 { font-size: 15px; }
.mode-tabs { margin-top: 11px; }
.control-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 7px 12px;
  margin-top: 10px;
}
.control-grid .control { margin-top: 0; min-width: 0; }
.control-grid .control label { font-size: 12px; }
.control-grid .control output { font-size: 12px; }
.control-grid input[type="range"] { margin: 7px 0 1px; }

.readout { max-width: min(620px, calc(100% - 32px)); }
.readout table { border-collapse: collapse; width: 100%; font: inherit; }
.readout th {
  padding: 1px 10px 3px 0;
  color: #5b6a80;
  font: 700 12px -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
  text-align: left;
  white-space: nowrap;
}
.readout td {
  padding: 1px 12px 1px 0;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}
.readout td:last-child, .readout th:last-child { padding-right: 0; }
.readout .row { white-space: normal; }
.readout .warn { color: #b45309; font-weight: 700; }
.readout .ok { color: #15803d; font-weight: 700; }
.readout .a { color: #1d4ed8; }
.readout .b { color: #64748b; }
.readout .tip { color: #c2410c; }

@media (max-width: 720px) {
  .panel h1 { font-size: 13.5px; }
  .mode-tabs button { font-size: 11px; padding: 5px 2px; }
  .control-grid { gap: 5px 8px; }
  .control-grid .control label { font-size: 10.5px; }
  .control-grid .control output { font-size: 10.5px; }
  .readout { font-size: 12px; line-height: 1.45; padding: 6px 8px; }
  .readout .small { font-size: 10px; }
  /* 窄屏下把表格摊平：每个解一行、角度与末端各占一行 */
  .readout table { display: block; }
  .readout thead { display: none; }
  .readout tbody { display: block; }
  .readout tr {
    display: block;
    margin-top: 3px;
    font-size: 10px;
    line-height: 1.5;
  }
  .readout td { display: inline; padding: 0; font-size: 10px; }
  .readout td:first-child { font-weight: 700; }
  .readout td:nth-child(2)::before { content: "θ₁="; }
  .readout td:nth-child(3)::before { content: " θ₂="; }
  .readout td:nth-child(4)::before { content: " θ₃="; }
  .readout td:nth-child(5) { display: block; }
  .readout td:nth-child(5)::before { content: "末端 "; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="三连杆平面操作臂的两个逆解：同一末端位姿对应实线与虚线两个位形">
  <defs>
    <marker id="mAxis" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"></path>
    </marker>
    <marker id="mRing" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
  </defs>
  <g id="angles"></g>
  <g id="armA"></g>
  <g id="armB"></g>
  <g id="labels"></g>
</svg>

<section class="panel" aria-label="图4-2 控制面板">
  <div class="panel-head">
    <div>
      <h1>图4-2 三连杆操作臂的两个解</h1>
      <p class="subtitle">同一目标位姿 (x, y, φ) 有两组关节角：实线解与虚线解（θ₂ 取 −θ₂）。
        两组解的末端完全重合，只有中间关节的转向相反。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="mode-tabs tabs">
    <button id="modeSolid" type="button" class="is-active">实线解</button>
    <button id="modeDashed" type="button">虚线解</button>
    <button id="modeBoth" type="button">两解并显</button>
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="tx">目标 x</label><output id="txValue">0.70</output></div>
      <input id="tx" type="range" min="-1.3" max="1.3" step="0.02" value="0.7">
    </div>
    <div class="control">
      <div class="control-head"><label for="ty">目标 y</label><output id="tyValue">0.40</output></div>
      <input id="ty" type="range" min="-1.3" max="1.3" step="0.02" value="0.4">
    </div>
    <div class="control">
      <div class="control-head"><label for="phi">目标姿态 φ</label><output id="phiValue">0.0°</output></div>
      <input id="phi" type="range" min="-180" max="180" step="1" value="0">
    </div>
    <div class="control">
      <div class="control-head"><label for="l1">连杆 l₁</label><output id="l1Value">1.00</output></div>
      <input id="l1" type="range" min="0.6" max="1.2" step="0.05" value="1">
    </div>
    <div class="control">
      <div class="control-head"><label for="l2">连杆 l₂</label><output id="l2Value">1.00</output></div>
      <input id="l2" type="range" min="0.6" max="1.2" step="0.05" value="1">
    </div>
    <div class="control">
      <div class="control-head"><label for="l3">连杆 l₃</label><output id="l3Value">0.40</output></div>
      <input id="l3" type="range" min="0" max="0.6" step="0.05" value="0.4">
    </div>
  </div>

  <div class="options">
    <label><input id="showAngles" type="checkbox" checked>关节角弧</label>
    <label><input id="showTarget" type="checkbox" checked>目标点</label>
  </div>

  <div class="legend">
    <span><i style="background:#1d4ed8"></i>实线解 A（θ₂ &gt; 0）</span>
    <span><i style="background:#94a3b8"></i>虚线解 B（θ₂′ = −θ₂）</span>
    <span><i class="dot" style="background:#c2410c"></i>目标位姿 T</span>
    <span><i style="background:#0e7490"></i>关节角弧（θ′ 为虚线解）</span>
  </div>
</section>

<div class="hint">拖动平移 · 滚轮缩放 · 双击复位</div>

<div class="readout" id="readout">
  <div class="row">目标位姿 <strong>T</strong> = ( <span id="rtx">0.70</span>, <span id="rty">0.40</span> )，φ = <span id="rphi">0.0°</span>
    <span class="small">（腕点 W = T − l₃·[cφ, sφ]）</span></div>
  <table id="kineTable">
    <thead><tr><th>解</th><th>θ₁</th><th>θ₂</th><th>θ₃</th><th>末端 (x, y)</th></tr></thead>
    <tbody id="kineBody"></tbody>
  </table>
  <div class="row small" id="noteRow">…</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var L = {
    angles: document.getElementById("angles"),
    armA: document.getElementById("armA"),
    armB: document.getElementById("armB"),
    labels: document.getElementById("labels")
  };

  var BASE_SCALE = 155;
  var scene = new FK.Scene({ svg: viewport, origin: { x: 462, y: 300 }, scale: BASE_SCALE });
  var state = {
    tx: 0.7, ty: 0.4, phi: 0,
    l1: 1, l2: 1, l3: 0.4,
    mode: "solid",
    showAngles: true, showTarget: true
  };
  /* 平移/缩放在屏幕像素里做，因此与世界坐标无关 */
  var pan = { x: 0, y: 0, dragging: false, id: null, lx: 0, ly: 0 };

  /* 纯平面投影：世界 (x, y) -> 屏幕；v[2] 只用于给关节圆点排序留位 */
  scene.project = function (v) {
    var s = scene.state.scale;
    return {
      x: this.origin.x + pan.x + v[0] * s,
      y: this.origin.y + pan.y - v[1] * s,
      depth: v[2] || 0
    };
  };

  var COL = {
    link: "#1d4ed8", link2: "#3b6fe0", joint: "#1e293b",
    alt: "#94a3b8", altJoint: "#a8b3c4",
    t1: "#0e7490", t2: "#7c3aed", t3: "#b45309",
    target: "#c2410c"
  };

  /* ------------------------------------------------------------ 运动学 */
  function fk(l1, l2, l3, t1, t2, t3) {
    var a12 = t1 + t2;
    var a123 = a12 + t3;
    var p0 = [0, 0];
    var p1 = [l1 * Math.cos(t1), l1 * Math.sin(t1)];
    var p2 = [p1[0] + l2 * Math.cos(a12), p1[1] + l2 * Math.sin(a12)];
    var p3 = [p2[0] + l3 * Math.cos(a123), p2[1] + l3 * Math.sin(a123)];
    return { joints: [p0, p1, p2, p3], angles: [t1, a12, a123] };
  }

  /* 逆解：先把目标点按 φ 折算到腕点，再用式(4-14)/(4-15) 解 θ1、θ2，
     最后由式(4-28) 的 φ = θ1+θ2+θ3 解出 θ3。返回两支解（θ2 取 ±）。
     退化情形：腕点正好落在原点（式(4-27) 的 x = y = 0）时 θ1 取任意值，
     教材 4.4 节对此有说明，这里取 θ1 = 0 并置 degenerate 标志。 */
  function ik(l1, l2, l3, x, y, phi) {
    var wx = x - l3 * Math.cos(phi);
    var wy = y - l3 * Math.sin(phi);
    var d = wx * wx + wy * wy;
    var c2 = (d - l1 * l1 - l2 * l2) / (2 * l1 * l2);
    var reach = l1 + l2;
    var rW = Math.sqrt(d);
    if (d < 1e-18) {
      var t2 = Math.PI;
      return {
        ok: true, degenerate: true, c2: -1, c2raw: -1, rW: 0, reach: reach,
        wrist: [0, 0], branch: [
          { name: "A", sign: 1, t1: 0, t2: t2, t3: phi - t2, tip: fk(l1, l2, l3, 0, t2, phi - t2).joints[3] },
          { name: "B", sign: -1, t1: 0, t2: -t2, t3: phi + t2, tip: fk(l1, l2, l3, 0, -t2, phi + t2).joints[3] }
        ]
      };
    }
    if (c2 > 1 || c2 < -1) {
      return { ok: false, degenerate: false, c2: c2, c2raw: c2, rW: rW, reach: reach, wrist: [wx, wy], branch: [] };
    }
    var c2c = Math.max(-1, Math.min(1, c2));
    var beta = Math.atan2(wy, wx);
    var cosPsi = (d + l1 * l1 - l2 * l2) / (2 * l1 * rW);
    var psi = Math.acos(Math.max(-1, Math.min(1, cosPsi)));
    var t2a = Math.atan2(Math.sqrt(Math.max(0, 1 - c2c * c2c)), c2c);
    var branch = [
      { name: "A", sign: 1, t1: beta - psi, t2: t2a },
      { name: "B", sign: -1, t1: beta + psi, t2: -t2a }
    ];
    branch.forEach(function (b) {
      b.t3 = phi - b.t1 - b.t2;
      b.tip = fk(l1, l2, l3, b.t1, b.t2, b.t3).joints[3];
    });
    return {
      ok: true, degenerate: false, c2: c2c, c2raw: c2, rW: rW, reach: reach,
      wrist: [wx, wy], psi: psi, beta: beta, branch: branch
    };
  }

  /* ------------------------------------------------------------- 绘图 */
  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    return scene.el("line", Object.assign({ x1: A.x, y1: A.y, x2: B.x, y2: B.y }, attrs || {}), parent);
  }
  function tag(v, str, attrs, dx, dy, parent) {
    var p = scene.project(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0),
      "font-size": 14.5, "font-weight": 700, class: "fk-axis-label"
    }, attrs || {}), parent);
    node.textContent = str;
    return node;
  }
  /* 关节角弧：从 a0 到 a1（弧度，带符号） */  function drawArc(cx, cy, r, a0, a1, color, label, lr, ldx, ldy, layer) {
    var n = 44, pts = [], i;
    for (i = 0; i <= n; i += 1) {
      var a = a0 + (a1 - a0) * i / n;
      pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a), 0]);
    }
    scene.polyline(pts, { stroke: color, class: "fk-arc" }, layer);
    if (!label) return;
    var mid = a0 + (a1 - a0) * 0.5;
    tag([cx + lr * Math.cos(mid), cy + lr * Math.sin(mid), 0], label,
      { fill: color, "font-size": 13.5, "text-anchor": "middle" }, ldx || 0, ldy || 4, layer);
  }

  /* 画一套位形：关节序列 + 关节圆点 + 各连杆中点标签 */
  function drawArm(sol, sel, l1, l2, l3) {
    var K = fk(l1, l2, l3, sel.t1, sel.t2, sel.t3);
    var j = K.joints, i;
    var LAYER = sel.name === "A" ? L.armA : L.armB;
    var main = sel.name === "A";
    var color = main ? COL.link : COL.alt;
    var widths = [main ? 13 : 8, main ? 13 : 8, main ? 8 : 6];
    var dashes = [main ? null : "10 8", main ? null : "10 8", main ? null : "7 6"];
    for (i = 0; i < 3; i += 1) {
      if (i === 2 && l3 < 1e-6) continue;
      seg(j[i], j[i + 1], {
        stroke: i === 2 && main ? "#60a5fa" : color,
        "stroke-width": widths[i], "stroke-dasharray": dashes[i],
        "stroke-linecap": "round"
      }, LAYER);
    }
    for (i = 0; i < 4; i += 1) {
      if (i === 3 && l3 < 1e-6) continue;
      var p = scene.project(j[i]);
      scene.el("circle", {
        cx: p.x, cy: p.y, r: i === 0 ? 6.5 : 5.5,
        fill: "#fff", stroke: main ? COL.joint : COL.altJoint, "stroke-width": 2.6
      }, LAYER);
    }
    /* 连杆标签（l₃ 只给主解标一次） */
    var mid1 = [(j[0][0] + j[1][0]) / 2, (j[0][1] + j[1][1]) / 2];
    var mid2 = [(j[1][0] + j[2][0]) / 2, (j[1][1] + j[2][1]) / 2];
    tag(mid1, "l\u2081", { fill: main ? "#1e3a8a" : "#7b8798", "font-size": 14 }, -16, -8, L.labels);
    tag(mid2, "l\u2082", { fill: main ? "#1e3a8a" : "#7b8798", "font-size": 14 }, 12, -8, L.labels);
    return K;
  }

  /* 画 θ1、θ2、θ3 的角弧：solid 解用实线色，dashed 解用灰色并标 ( ′ ) */
  function drawAngles(sel, l1, l2, l3, dashed) {
    var K = fk(l1, l2, l3, sel.t1, sel.t2, sel.t3);
    var j = K.joints;
    var c1 = dashed ? "#a8b3c4" : COL.t1;
    var c2 = dashed ? "#b6a6d8" : COL.t2;
    var c3 = dashed ? "#c9ab7f" : COL.t3;
    var sfx = dashed ? "\u2032" : "";
    drawArc(0, 0, Math.min(0.30, 0.30 * l1), 0, sel.t1, c1, "\u03b8\u2081" + sfx, 0.40, 0, 5, L.angles);
    drawArc(j[1][0], j[1][1], Math.min(0.26, 0.30 * l2), sel.t1, sel.t1 + sel.t2, c2, "\u03b8\u2082" + sfx, 0.36, 0, 5, L.angles);
    if (l3 > 1e-6) {
      drawArc(j[2][0], j[2][1], Math.min(0.22, 0.30 * l3), sel.t1 + sel.t2, sel.t1 + sel.t2 + sel.t3, c3, "\u03b8\u2083" + sfx, 0.32, -10, -8, L.angles);
    }
  }

  function drawBase() {
    seg([-0.30, 0, 0], [0.30, 0, 0], { stroke: "#334155", "stroke-width": 3.4 }, L.armA);
    for (var i = -3; i <= 3; i += 1) {
      seg([i * 0.09 - 0.14, 0, 0], [i * 0.09 + 0.02, -0.13, 0], { stroke: "#334155", "stroke-width": 1.5 }, L.armA);
    }
  }

  function drawAxes() {
    seg([0, 0, 0], [0.55, 0, 0], { stroke: "#64748b", "stroke-width": 2, "marker-end": "url(#mAxis)" }, L.labels);
    seg([0, 0, 0], [0, 0.55, 0], { stroke: "#64748b", "stroke-width": 2, "marker-end": "url(#mAxis)" }, L.labels);
    tag([0.55, 0, 0], "X", { fill: "#64748b", "font-size": 13 }, 5, 15, L.labels);
    tag([0, 0.55, 0], "Y", { fill: "#64748b", "font-size": 13 }, 7, -4, L.labels);
    tag([0, 0, 0], "O", { fill: "#475569", "font-size": 14 }, -18, 18, L.labels);
  }

  function drawTarget(x, y, phi) {
    seg([x, y, 0], [x + 0.42 * Math.cos(phi), y + 0.42 * Math.sin(phi), 0],
      { stroke: COL.target, "stroke-width": 3, "stroke-dasharray": "7 5" }, L.labels);
    var p = scene.project([x, y, 0]);
    scene.el("circle", { cx: p.x, cy: p.y, r: 6.6, fill: COL.target, stroke: "#fff", "stroke-width": 2.4, class: "fk-point" }, L.labels);
    tag([x, y, 0], "T", { fill: "#8a3a0c", "font-size": 16 }, 12, -24, L.labels);
    tag([x, y, 0], "T = (" + FK.format(x, 2) + ", " + FK.format(y, 2) + ")\uff0c\u03c6 = " + FK.deg(degNorm(phi), 0),
      { fill: "#8a3a0c", "font-size": 12 }, 12, 38, L.labels);
  }

  /* ------------------------------------------------------------ 读数 */
  function degNorm(rad) {
    var d = rad / FK.DEG;
    d = d % 360;
    if (d > 180) d -= 360;
    if (d <= -180) d += 360;
    return d;
  }
  function degNormNum(d) {
    d = d % 360;
    if (d > 180) d -= 360;
    if (d <= -180) d += 360;
    return d;
  }

  function kineRowsHTML(sol, sign2, label, cls) {
    if (!sol.ok) {
      return '<tr class="' + cls + '"><td>' + label + "</td><td>—</td><td>—</td><td>—</td></tr>";
    }
    var b = sol.branch[sign2 >= 0 ? 0 : 1];
    var tip = b.tip;
    return '<tr class="' + cls + '"><td>' + label + "</td>"
      + "<td>" + FK.deg(degNorm(b.t1), 1) + "</td>"
      + "<td>" + FK.deg(degNorm(b.t2), 1) + "</td>"
      + "<td>" + FK.deg(degNorm(b.t3), 1) + "</td>"
      + "<td>(" + FK.format(tip[0], 3) + ", " + FK.format(tip[1], 3) + ")</td></tr>";
  }

  /* ----------------------------------------------------------- 渲染 */
  function render() {
    var k;
    for (k in L) { if (Object.prototype.hasOwnProperty.call(L, k)) L[k].replaceChildren(); }

    var l1 = state.l1, l2 = state.l2, l3 = state.l3;
    var x = state.tx, y = state.ty, phi = state.phi * FK.DEG;
    var sol = ik(l1, l2, l3, x, y, phi);

    drawAxes();
    drawBase();

    if (sol.ok) {
      var showA = state.mode !== "dashed";
      var showB = state.mode !== "solid";
      if (showA) drawArm(sol, sol.branch[0], l1, l2, l3);
      if (showB) drawArm(sol, sol.branch[1], l1, l2, l3);
      if (state.showAngles) {
        if (showA) drawAngles(sol.branch[0], l1, l2, l3, false);
        if (showB) drawAngles(sol.branch[1], l1, l2, l3, true);
      }
      /* 腕点 W 与目标点 T 都是两解共用的 */
      var w = scene.project([sol.wrist[0], sol.wrist[1], 0]);
      scene.el("circle", { cx: w.x, cy: w.y, r: 3.6, fill: "#475569" }, L.labels);
      tag([sol.wrist[0], sol.wrist[1], 0], "W", { fill: "#475569", "font-size": 13 }, 9, 16, L.labels);
    }
    if (state.showTarget) drawTarget(x, y, phi);

    /* -------------------------------------------------------- 读数表 */
    document.getElementById("kineBody").innerHTML =
      kineRowsHTML(sol, 1, "\u5b9e\u7ebf\u89e3 A\uff08\u03b8\u2082 &gt; 0\uff09", "a")
      + kineRowsHTML(sol, -1, "\u865a\u7ebf\u89e3 B\uff08\u03b8\u2082\u2032 = \u2212\u03b8\u2082\uff09", "b");

    document.getElementById("rtx").textContent = FK.format(x, 2);
    document.getElementById("rty").textContent = FK.format(y, 2);
    document.getElementById("rphi").textContent = FK.deg(state.phi, 1);

    var note = document.getElementById("noteRow");
    if (!sol.ok) {
      note.className = "row small warn";
      note.textContent = "无解：目标点超出可达范围。c\u2082 = " + FK.format(sol.c2raw, 3)
        + " 越界（式(4-14) 要求 −1 \u2264 c\u2082 \u2264 1），腕点距原点 "
        + FK.format(sol.rW, 3) + " > l\u2081+l\u2082 = " + FK.format(sol.reach, 3) + "。";
    } else if (sol.degenerate) {
      note.className = "row small warn";
      note.textContent = "退化情形：腕点正好落在原点（教材式(4-27) 的 x = y = 0），θ\u2081 可取任意值。"
        + "此处取 θ\u2081 = 0，得 θ\u2082 = ±180°（两连杆折返），两组解末端仍重合于 T。";
    } else {
      var bA = sol.branch[0], bB = sol.branch[1];
      var dA = Math.hypot(bA.tip[0] - x, bA.tip[1] - y);
      var dB = Math.hypot(bB.tip[0] - x, bB.tip[1] - y);
      var rRel = Math.abs(dA - dB) / Math.max(1e-12, Math.max(dA, dB, 1e-12));
      note.className = "row small ok";
      note.textContent = "两组解末端完全重合：|T_A − T_B| = " + dA.toExponential(2)
        + "（式(4-15) 的 ± 就是图中实线/虚线两个位形）；"
        + "\u03b8\u2082 = " + FK.deg(degNorm(bA.t2), 1) + " \u2194 " + FK.deg(degNorm(bB.t2), 1)
        + "，\u03b8\u2081 = " + FK.deg(degNorm(bA.t1), 1) + " \u2194 " + FK.deg(degNorm(bB.t1), 1)
        + "，两解支距 " + rRel.toExponential(1) + "。";
      if (Math.abs(state.l3) < 1e-9) {
        note.textContent += " 当前 l\u2083 = 0：T 即腕点（教材图4-2 的取法）。";
      }
    }
  }

  /* ----------------------------------------------------------- 布局 */
  function layout() {
    var w = viewport.clientWidth || window.innerWidth;
    var h = viewport.clientHeight || window.innerHeight;
    if (w / h < 1.05) {
      viewport.setAttribute("viewBox", "0 0 420 780");
      viewport.setAttribute("preserveAspectRatio", "xMidYMin meet");
      scene.baseOrigin = { x: 208, y: 252 };
      scene.state.scale = 95;
      scene.defaults.scale = 95;
    } else {
      viewport.setAttribute("viewBox", "0 0 1000 620");
      viewport.setAttribute("preserveAspectRatio", "xMidYMid meet");
      scene.baseOrigin = { x: 462, y: 300 };
      scene.state.scale = BASE_SCALE;
      scene.defaults.scale = BASE_SCALE;
    }
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "tx", key: "tx", value: 0.7, format: function (v) { return FK.format(v, 2); } },
    { id: "ty", key: "ty", value: 0.4, format: function (v) { return FK.format(v, 2); } },
    { id: "phi", key: "phi", value: 0, format: function (v) { return FK.deg(v, 1); } },
    { id: "l1", key: "l1", value: 1, format: function (v) { return FK.format(v, 2); } },
    { id: "l2", key: "l2", value: 1, format: function (v) { return FK.format(v, 2); } },
    { id: "l3", key: "l3", value: 0.4, format: function (v) { return FK.format(v, 2); } }
  ], state, render);

  FK.bindToggles([
    { id: "showAngles", key: "showAngles" },
    { id: "showTarget", key: "showTarget" }
  ], state, render);

  function setMode(mode) {
    state.mode = mode;
    document.getElementById("modeSolid").classList.toggle("is-active", mode === "solid");
    document.getElementById("modeDashed").classList.toggle("is-active", mode === "dashed");
    document.getElementById("modeBoth").classList.toggle("is-active", mode === "both");
    render();
  }
  document.getElementById("modeSolid").addEventListener("click", function () { setMode("solid"); });
  document.getElementById("modeDashed").addEventListener("click", function () { setMode("dashed"); });
  document.getElementById("modeBoth").addEventListener("click", function () { setMode("both"); });

  document.getElementById("reset").addEventListener("click", function () {
    state.tx = 0.7; state.ty = 0.4; state.phi = 0;
    state.l1 = 1; state.l2 = 1; state.l3 = 0.4;
    state.mode = "solid";
    state.showAngles = true; state.showTarget = true;
    document.getElementById("showAngles").checked = true;
    document.getElementById("showTarget").checked = true;
    document.getElementById("modeSolid").classList.add("is-active");
    document.getElementById("modeDashed").classList.remove("is-active");
    document.getElementById("modeBoth").classList.remove("is-active");
    pan.x = 0; pan.y = 0;
    ranges.refresh();
    scene.reset();
    layout();
    render();
  });

  /* 拖动平移（平面图不用三维旋转） */
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
  window.addEventListener("resize", function () { layout(); render(); });

  /* --------------------------------------------------------- 数值自检 */
  (function selfTest() {
    var EPS = 1e-9;
    var L1 = 1, L2 = 1, L3 = 0.4;

    /* 自检1：默认目标 (0.7, 0.4)、φ = 0° 时，两组解的末端位置必须完全一致（< 1e-9）。
       教材式(4-15) 的 ± 就是这两个位形；末端位置与姿态都应重合。 */
    var s0 = ik(L1, L2, L3, 0.7, 0.4, 0);
    if (!s0.ok) throw new Error("默认目标 (0.7,0.4) 应在可达范围内");
    var A = s0.branch[0], B = s0.branch[1];
    var dp = Math.hypot(A.tip[0] - B.tip[0], A.tip[1] - B.tip[1]);
    if (!(dp < EPS)) throw new Error("两解末端位置误差应 < 1e-9，实得 " + dp);
    if (Math.abs(A.t1 + A.t2 + A.t3 - B.t1 - B.t2 - B.t3) > EPS) {
      throw new Error("两解末端姿态应相同（θ1+θ2+θ3 = φ）");
    }
    /* 两组解各自的 FK 都必须命中目标点 */
    [A, B].forEach(function (b, i) {
      var K = fk(L1, L2, L3, b.t1, b.t2, b.t3);
      if (Math.hypot(K.joints[3][0] - 0.7, K.joints[3][1] - 0.4) > EPS) {
        throw new Error("解 " + i + " 的 FK 未命中目标点");
      }
    });
    /* θ2 取相反符号（教材提醒：虚线解是 θ2 取 −θ2） */
    if (Math.abs(A.t2 + B.t2) > EPS) throw new Error("两解的 θ2 应互为相反数");
    /* 解析值对照：c2 = (x²+y²−l1²−l2²)/(2l1l2)（式(4-14)） */
    var c2 = (0.7 * 0.7 + 0.4 * 0.4 - L1 * L1 - L2 * L2) / (2 * L1 * L2);
    if (Math.abs(Math.cos(A.t2) - c2) > EPS) throw new Error("θ2 的余弦应等于式(4-14) 的 c2");

    /* 自检2：边界与越界。r = l1+l2 时 c2 = 1、两组解退化为同一位形；r > l1+l2 应判无解。 */
    var sEdge = ik(L1, L2, 0, 2, 0, 0);
    if (!sEdge.ok || Math.abs(sEdge.c2 - 1) > EPS) throw new Error("边界 r = l1+l2 时应有唯一解 c2 = 1");
    if (Math.abs(sEdge.branch[0].t2) > 1e-9) throw new Error("边界上 θ2 应为 0");
    var sOut = ik(L1, L2, 0, 2.05, 0, 0);
    if (sOut.ok) throw new Error("r > l1+l2 时应显示无解");
    if (!(sOut.c2raw > 1)) throw new Error("越界时 c2 必须大于 1");
    /* 目标超远（滑块极限 ±1.3, ±1.3，l3 = 0 时 r ≈ 1.84 < 2）也应被正确判定 */
    var sFar = ik(L1, L2, 0, 1.3, 1.3, 0);
    if (sFar.ok) throw new Error("(1.3,1.3) 相对 l1+l2 = 2 应无解");
    if (!(sFar.rW > L1 + L2)) throw new Error("无解判据应为 r > l1+l2");

    /* 自检3：随机目标（可达范围内）扫一遍，两解末端位置误差恒 < 1e-9 */
    var k, t, x, y;
    for (k = 0; k < 240; k += 1) {
      t = k * 0.1309;
      var rr = 0.35 + 1.25 * ((k % 17) / 16);
      x = rr * Math.cos(t);
      y = rr * Math.sin(t);
      var s = ik(L1, L2, L3, x, y, (k * 7) % 360 * FK.DEG - Math.PI);
      if (!s.ok) continue;
      var e = Math.hypot(s.branch[0].tip[0] - s.branch[1].tip[0], s.branch[0].tip[1] - s.branch[1].tip[1]);
      if (!(e < EPS)) throw new Error("扫掠自检失败 @" + k + "，误差 " + e);
      var K1 = fk(L1, L2, L3, s.branch[0].t1, s.branch[0].t2, s.branch[0].t3);
      if (Math.hypot(K1.joints[3][0] - x, K1.joints[3][1] - y) > 1e-9) {
        throw new Error("扫掠 FK 自检失败 @" + k);
      }
    }

    /* 自检4：l3 = 0 时目标点即腕点，逆解与教材式(4-14)–(4-16) 的取法一致 */
    var s2 = ik(L1, L2, 0, 0.7, 0.4, 0.6);
    if (!s2.ok) throw new Error("l3 = 0 时 (0.7,0.4) 应有解");
    if (Math.hypot(s2.wrist[0] - 0.7, s2.wrist[1] - 0.4) > EPS) throw new Error("l3 = 0 时腕点应等于目标点");
    if (Math.abs(s2.branch[0].t3 - 0.6) > EPS) throw new Error("l3 = 0 时 θ3 应等于 φ − θ1 − θ2");

    /* 自检5：退化情形（腕点落在原点，式(4-27) 的 x = y = 0）不得产生 NaN，
       两组解仍要重合，θ2 = ±180° */
    var sDeg = ik(0.6, 0.6, 0, 0, 0, 0);
    if (!sDeg.ok || !sDeg.degenerate) throw new Error("腕点在原点应判为退化情形且有解");
    if (!isFinite(sDeg.c2raw) || !isFinite(sDeg.branch[0].t2) || !isFinite(sDeg.branch[1].t2)) {
      throw new Error("退化情形的角度/余弦不得为 NaN");
    }
    if (Math.abs(Math.abs(sDeg.branch[0].t2) - Math.PI) > EPS) throw new Error("退化情形 θ2 应为 ±180°");
    if (Math.hypot(sDeg.branch[0].tip[0] - sDeg.branch[1].tip[0],
                   sDeg.branch[0].tip[1] - sDeg.branch[1].tip[1]) > EPS) {
      throw new Error("退化情形两组解末端应重合");
    }
  }());

  layout();
  render();
}());
"""

FIGURE = {
    "id": "figure-4-2",
    "title": "图4-2 三连杆操作臂的两个逆解 · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
