"""图2-5 矢量的旋转（克雷格《机器人学导论（第3版）》2.3 节，式(2-11)~式(2-13)）。

教材依据：
- 正文（图2-5 段）：“矢量相对于某坐标系{B}的定义…想求矢量相对另一个坐标系{A}的定义，
  且这两个坐标系的原点重合”。
- 式(2-11)：ᴬ_BR = [ᴬX̂_B ᴬŶ_B ᴬẐ_B]，其列为{B}的单位矢量在{A}中的描述；
  其行为{A}的单位矢量在{B}中的描述。
- 式(2-12)：ᴬp_x = ᴮX̂_A·ᴮP，ᴬp_y = ᴮŶ_A·ᴮP，ᴬp_z = ᴮẐ_A·ᴮP
  ——“任一矢量的分量就是该矢量在参考系上单位矢量方向的投影。投影是由矢量点积计算的”。
- 式(2-13)：ᴬP = ᴬ_BR·ᴮP（原点重合，只做姿态映射；ᴮP 在{B}中不变）。

自检：θ=30° 时 ᴬ_BR 三列 = [0.866,0.500,0] / [-0.500,0.866,0] / [0,0,1]；
ᴮP=[0,2,0] 时 ᴬP = [-1.000,1.732,0.000]（与例2.1、式(2-16)一致）；
并逐分量校验式(2-12) 的点积等于 ᴬP 的分量。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.readout .row { white-space: normal; }
.readout .row.matrix { font-size: 13px; }
.readout .row.matrix b { color: var(--blue-dark); font-weight: 700; }
.viewport { z-index: 0; }
.panel, .readout, .hint { z-index: 2; }
@media (max-width: 720px) {
  .readout { font-size: 12px; }
  .readout .row.matrix { font-size: 11.5px; }
  .readout .small { font-size: 11.5px; }
  .legend { font-size: 11px; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="图2-5 矢量的旋转：原点重合的坐标系{A}与{B}中同一矢量ᴮP的两种描述">
  <defs>
    <marker id="arrowA" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"></path>
    </marker>
    <marker id="arrowBX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="arrowBY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="arrowBZ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="arrowP" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="axesA"></g>
  <g id="axesB"></g>
  <g id="compLayer"></g>
  <g id="vecLayer"></g>
  <g id="angleLayer"></g>
</svg>

<section class="panel" aria-label="图2-5 控制面板">
  <div class="panel-head">
    <div>
      <h1>图2-5 矢量的旋转</h1>
      <p class="subtitle">{A} 与 {B} 原点重合；{B} 相对 {A} 有姿态 ᴬ_BR。同一个物理点 P，
        ᴬP = ᴬ_BR·ᴮP，分量 = 矢量在单位矢量上的投影（式2-12、式2-13）。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="theta">姿态角 θ（{B} 绕 Ẑ_A）</label><output id="thetaValue">30.0°</output></div>
    <input id="theta" type="range" min="-180" max="180" step="1" value="30">
  </div>
  <div class="control">
    <div class="control-head"><label for="pbx">ᴮP 的 x 分量</label><output id="pbxValue">0.00</output></div>
    <input id="pbx" type="range" min="-5" max="5" step="0.1" value="0">
  </div>
  <div class="control">
    <div class="control-head"><label for="pby">ᴮP 的 y 分量</label><output id="pbyValue">2.00</output></div>
    <input id="pby" type="range" min="-5" max="5" step="0.1" value="2">
  </div>
  <div class="control">
    <div class="control-head"><label for="pbz">ᴮP 的 z 分量</label><output id="pbzValue">0.00</output></div>
    <input id="pbz" type="range" min="-5" max="5" step="0.1" value="0">
  </div>

  <div class="options">
    <label><input id="showB" type="checkbox" checked>显示坐标系{B}</label>
    <label><input id="showProj" type="checkbox" checked>显示投影虚线</label>
    <label><input id="showLabels" type="checkbox" checked>显示分量数值</label>
    <label><input id="showArc" type="checkbox" checked>显示转角 θ 圆弧</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i style="background:#475569"></i>坐标系{A}</span>
    <span><i style="background:#d93025"></i>坐标系{B} 三轴</span>
    <span><i class="dot" style="background:#c26a10"></i>矢量 P（ᴬP = ᴮP 同一条）</span>
    <span><i style="background:#94a3b8"></i>分量投影</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row"><strong>ᴮP</strong> = [ <span id="bx">0.000</span>, <span id="by">2.000</span>, <span id="bz">0.000</span> ]<sup>T</sup>
    <span class="small">（在 {B} 中不变）</span></div>
  <div class="row"><strong>ᴬP</strong> = [ <span id="ax">-1.000</span>, <span id="ay">1.732</span>, <span id="az">0.000</span> ]<sup>T</sup>
    <span class="small" id="projNote">（= 矢量在 X̂_A 上的投影 等）</span></div>
  <div class="row matrix"><b>ᴬ_BR</b> 的三列（列 = {B} 三轴在 {A} 中的表达）：
    第1列 [<span id="c11">0.866</span>, <span id="c21">0.500</span>, <span id="c31">0.000</span>]<br>
    第2列 [<span id="c12">-0.500</span>, <span id="c22">0.866</span>, <span id="c32">0.000</span>]；
    第3列 [<span id="c13">0.000</span>, <span id="c23">0.000</span>, <span id="c33">1.000</span>]</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var axesA = document.getElementById("axesA");
  var axesB = document.getElementById("axesB");
  var compLayer = document.getElementById("compLayer");
  var vecLayer = document.getElementById("vecLayer");
  var angleLayer = document.getElementById("angleLayer");

  var scene = new FK.Scene({ svg: viewport, origin: { x: 560, y: 352 }, scale: 78, yaw: -0.5, pitch: 0.36 });

  // 响应式取景：视口窄时缩小 viewBox，让刻度文字不被等比压得太小
  var LAYOUTS = [
    { max: 720, view: [700, 470], origin: { x: 372, y: 238 }, scale: 56 },
    { max: 1e9, view: [1000, 620], origin: { x: 556, y: 356 }, scale: 70 }
  ];
  function layout() {
    var w = viewport.clientWidth || 1200;
    for (var i = 0; i < LAYOUTS.length; i += 1) {
      if (w <= LAYOUTS[i].max) return LAYOUTS[i];
    }
    return LAYOUTS[LAYOUTS.length - 1];
  }
  function fit() {
    var L = layout();
    viewport.setAttribute("viewBox", "0 0 " + L.view[0] + " " + L.view[1]);
    scene.origin.x = L.origin.x;
    scene.origin.y = L.origin.y;
    scene.baseOrigin.x = L.origin.x;
    scene.baseOrigin.y = L.origin.y;
    scene.state.scale = L.scale;
    scene.defaults.scale = L.scale;
  }

  var COLORS = {
    A: "#475569",
    Bx: "#d93025", By: "#2563eb", Bz: "#12944f",
    vec: "#c26a10", comp: "#94a3b8", proj: "#64748b", arc: "#7c3aed"
  };

  var state = {
    theta: 30,
    pbx: 0, pby: 2, pbz: 0,
    showB: true, showProj: true, showLabels: true, showArc: true, auto: false
  };

  /* ------------------------------------------------------------ 绘制辅助 */

  function drawAxisFrame(layer, matrix, cfg) {
    var length = 3.05;
    var dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    var origin = FK.M4.apply(matrix, [0, 0, 0]);
    for (var i = 0; i < 3; i += 1) {
      var tip = FK.M4.apply(matrix, FK.Vec.scale(dirs[i], length));
      var a = scene.project(origin);
      var b = scene.project(tip);
      scene.el("line", {
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        stroke: cfg.colors[i], "stroke-width": cfg.width,
        "marker-end": "url(#" + cfg.markers[i] + ")"
      }, layer);
      var label = scene.el("text", {
        x: b.x + cfg.dx[i], y: b.y + cfg.dy[i], fill: cfg.colors[i],
        "font-size": 16.5, "font-style": "italic", class: "fk-axis-label"
      }, layer);
      label.textContent = cfg.labels[i];
    }
    var o = scene.project(origin);
    scene.el("circle", { cx: o.x, cy: o.y, r: 8, fill: "none", stroke: "#94a3b8", "stroke-width": 1.4 }, layer);
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.4, fill: "#334155" }, layer);
    var tag = scene.el("text", { x: o.x + cfg.originDx, y: o.y + cfg.originDy, class: "fk-origin-label" }, layer);
    tag.textContent = cfg.originLabel;
    if (cfg.originNote) {
      var note = scene.el("text", { x: o.x + cfg.originDx, y: o.y + cfg.originDy + 15, class: "fk-origin-label" }, layer);
      note.textContent = cfg.originNote;
    }
  }

  /** 在单位方向 u 上、从原点起每 1 个单位画一道短线，表示"矢量在单位矢量上的投影" */
  function drawRungs(u, comp, color, tag) {
    if (Math.abs(comp) < 0.06) return;
    var n = Math.max(1, Math.round(Math.abs(comp)));
    var sgn = comp >= 0 ? 1 : -1;
    var w = [1, 0, 0], h = [0, 1, 0];
    if (tag === "x") { w = [0, 1, 0]; h = [0, 0, 1]; }
    else if (tag === "y") { w = [1, 0, 0]; h = [0, 0, 1]; }
    var step = n > 5 ? n / 5 : 1;
    for (var t = 0; t <= n + 1e-9; t += step) {
      var base = FK.Vec.scale(u, sgn * t);
      scene.line(FK.Vec.add(base, FK.Vec.scale(w, -0.1)), FK.Vec.add(base, FK.Vec.scale(w, 0.1)),
        { stroke: color, "stroke-width": 1.6, opacity: 0.75 }, compLayer);
      scene.line(FK.Vec.add(base, FK.Vec.scale(h, -0.1)), FK.Vec.add(base, FK.Vec.scale(h, 0.1)),
        { stroke: color, "stroke-width": 1.6, opacity: 0.75 }, compLayer);
    }
  }

  /** 残差线（垂直于坐标轴的投影线）风格 */
  var DROP = { stroke: "#94a3b8", "stroke-width": 1.8, "stroke-dasharray": "6 5", fill: "none", opacity: 0.9 };

  /** ᴬP 在 {A} 三轴上的投影：一条竖直垂线 + 两条水平投影线（不画填充，避免原点附近噪声） */
  function drawProjectionFrame(P) {
    if (Math.abs(P[0]) < 0.02 && Math.abs(P[1]) < 0.02 && Math.abs(P[2]) < 0.02) return;
    var foot = [P[0], P[1], 0];
    if (Math.abs(P[2]) > 0.02) scene.line(P, foot, DROP, compLayer);
    if (Math.abs(P[1]) > 0.02) scene.line(foot, [P[0], 0, 0], DROP, compLayer);
    if (Math.abs(P[0]) > 0.02) scene.line(foot, [0, P[1], 0], DROP, compLayer);
  }

  function drawAngleArc(radius, endRad, color) {
    var steps = 44;
    var points = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = endRad * (i / steps);
      points.push([radius * Math.cos(t), radius * Math.sin(t), 0]);
    }
    scene.polyline(points, { stroke: color, class: "fk-arc" }, angleLayer);
    var mid = endRad * 0.5;
    var p = scene.project([(radius + 0.42) * Math.cos(mid), (radius + 0.42) * Math.sin(mid), 0]);
    var txt = scene.el("text", { x: p.x - 13, y: p.y + 2, fill: color, "font-size": 17, class: "fk-axis-label" }, angleLayer);
    txt.textContent = "\u03b8";
    var degTxt = scene.el("text", { x: p.x + 7, y: p.y + 18, fill: color, "font-size": 12.5, class: "fk-axis-label" }, angleLayer);
    degTxt.textContent = FK.deg(state.theta, 1);
  }

  /* ------------------------------------------------------------ 主渲染 */

  function render() {
    gridLayer.replaceChildren();
    axesA.replaceChildren();
    axesB.replaceChildren();
    compLayer.replaceChildren();
    vecLayer.replaceChildren();
    angleLayer.replaceChildren();

    scene.grid(3, 1);

    var theta = state.theta * FK.DEG;
    var Rab = FK.M4.rotZ(theta);

    drawAxisFrame(axesA, FK.M4.identity(), {
      labels: ["X\u0302\u2090", "Y\u0302\u2090", "Z\u0302\u2090"],
      colors: [COLORS.A, COLORS.A, COLORS.A],
      markers: ["arrowA", "arrowA", "arrowA"],
      dx: [10, 10, 10], dy: [-8, -8, -8], width: 3.1,
      originDx: -46, originDy: 15, originLabel: "O", originNote: "（{A}、{B} 原点重合）"
    });

    if (state.showB) {
      drawAxisFrame(axesB, Rab, {
        labels: ["X\u0302\u1d47", "Y\u0302\u1d47", "Z\u0302\u1d47"],
        colors: [COLORS.Bx, COLORS.By, COLORS.Bz],
        markers: ["arrowBX", "arrowBY", "arrowBZ"],
        dx: [10, 10, 10], dy: [-8, 9, -8], width: 3.1,
        originDx: 34, originDy: -22, originLabel: "O' = O"
      });
    }

    // ᴮP 在 {B} 中不变；ᴬP = ᴬ_BR·ᴮP（原点重合，纯姿态映射，故用 applyDir）
    var Pb = [state.pbx, state.pby, state.pbz];
    var Pa = FK.M4.applyDir(Rab, Pb);

    var U = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    var compColors = ["#d93025", "#2563eb", "#12944f"];

    if (state.showProj) {
      drawProjectionFrame(Pa);
      drawRungs(U[0], Pa[0], compColors[0], "x");
      drawRungs(U[1], Pa[1], compColors[1], "y");
      drawRungs(U[2], Pa[2], compColors[2], "z");
      // 分量读数放在三条投影线的落点附近
      var compTags = [
        { p: [Pa[0], 0, 0], dx: -52, dy: 20, v: Pa[0], c: compColors[0], anchor: "end" },
        { p: [0, Pa[1], 0], dx: -92, dy: 18, v: Pa[1], c: compColors[1], anchor: "end" },
        { p: [0, 0, Pa[2]], dx: 70, dy: 4, v: Pa[2], c: compColors[2], anchor: "start" }
      ];
      if (state.showLabels) {
        for (var ci = 0; ci < compTags.length; ci += 1) {
          if (Math.abs(compTags[ci].v) < 0.02) continue;
          var q = scene.project(compTags[ci].p);
          var node = scene.el("text", {
            x: q.x + compTags[ci].dx, y: q.y + compTags[ci].dy,
            fill: compTags[ci].c, "font-size": 12.5, class: "fk-point-label",
            "text-anchor": compTags[ci].anchor
          }, compLayer);
          node.textContent = (compTags[ci].v >= 0 ? "+" : "\u2212") + FK.format(Math.abs(compTags[ci].v), 2);
        }
      }
    }

    // 矢量本身：物理上只有一条 P；在 {A} 中读作 ᴬP，在 {B} 中读作 ᴮP
    var O = [0, 0, 0];
    var o = scene.project(O);
    var pEnd = scene.project(Pa);
    var len = FK.Vec.len(Pa);
    scene.el("line", {
      x1: o.x, y1: o.y, x2: pEnd.x, y2: pEnd.y,
      stroke: COLORS.vec, class: "fk-vec-line", "marker-end": "url(#arrowP)"
    }, vecLayer);
    scene.el("circle", { cx: pEnd.x, cy: pEnd.y, r: 6.2, fill: COLORS.vec, class: "fk-point" }, vecLayer);

    var labelP = scene.el("text", {
      x: pEnd.x + 12, y: pEnd.y - 18, fill: "#8a4a08", "font-size": 17, class: "fk-point-label"
    }, vecLayer);
    labelP.textContent = "\u1d2cP = \u1d2eP";

    if (state.showLabels) {
      var readA = scene.el("text", { x: pEnd.x + 12, y: pEnd.y + 9, fill: "#475569", "font-size": 13.5, class: "fk-point-label" }, vecLayer);
      readA.textContent = "\u1d2cP = [" + FK.format(Pa[0], 2) + ", " + FK.format(Pa[1], 2) + ", " + FK.format(Pa[2], 2) + "]\u1d40";
      var readB = scene.el("text", { x: pEnd.x + 12, y: pEnd.y + 28, fill: "#7c3aed", "font-size": 13.5, class: "fk-point-label" }, vecLayer);
      readB.textContent = "\u1d2eP = [" + FK.format(Pb[0], 2) + ", " + FK.format(Pb[1], 2) + ", " + FK.format(Pb[2], 2) + "]\u1d40";
    }

    if (state.showArc && Math.abs(state.theta) > 1.2) {
      drawAngleArc(1.18, theta, COLORS.arc);
    }
    /* -------------------------------------------------- 读数 */
    var R = FK.M4.rotation(Rab);
    document.getElementById("bx").textContent = FK.format(Pb[0], 3);
    document.getElementById("by").textContent = FK.format(Pb[1], 3);
    document.getElementById("bz").textContent = FK.format(Pb[2], 3);
    document.getElementById("ax").textContent = FK.format(Pa[0], 3);
    document.getElementById("ay").textContent = FK.format(Pa[1], 3);
    document.getElementById("az").textContent = FK.format(Pa[2], 3);
    // 第 j 列的三行依次是 R[0*3+j], R[1*3+j], R[2*3+j]
    document.getElementById("c11").textContent = FK.format(R[0], 3);
    document.getElementById("c21").textContent = FK.format(R[3], 3);
    document.getElementById("c31").textContent = FK.format(R[6], 3);
    document.getElementById("c12").textContent = FK.format(R[1], 3);
    document.getElementById("c22").textContent = FK.format(R[4], 3);
    document.getElementById("c32").textContent = FK.format(R[7], 3);
    document.getElementById("c13").textContent = FK.format(R[2], 3);
    document.getElementById("c23").textContent = FK.format(R[5], 3);
    document.getElementById("c33").textContent = FK.format(R[8], 3);

    var note = document.getElementById("projNote");
    if (state.showProj && len > 1e-6) {
      var d1 = FK.Vec.dot([R[0], R[1], R[2]], Pb);
      var d2 = FK.Vec.dot([R[3], R[4], R[5]], Pb);
      var d3 = FK.Vec.dot([R[6], R[7], R[8]], Pb);
      note.textContent = "\uff08\u70b9\u79ef\u6821\u9a8c\uff1a[" + FK.format(d1, 3) + ", " + FK.format(d2, 3) + ", " + FK.format(d3, 3) + "]\uff09";
    } else {
      note.textContent = "\uff08\u5206\u91cf = \u77e2\u91cf\u5728\u5355\u4f4d\u77e2\u91cf\u4e0a\u7684\u6295\u5f71\uff09";
    }
    document.getElementById("thetaValue").textContent = FK.deg(state.theta, 1);
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "theta", key: "theta", value: 30, format: function (v) { return FK.deg(v, 1); } },
    { id: "pbx", key: "pbx", value: 0, format: function (v) { return FK.format(v, 2); } },
    { id: "pby", key: "pby", value: 2, format: function (v) { return FK.format(v, 2); } },
    { id: "pbz", key: "pbz", value: 0, format: function (v) { return FK.format(v, 2); } }
  ], state, render);

  FK.bindToggles([
    { id: "showB", key: "showB" },
    { id: "showProj", key: "showProj" },
    { id: "showLabels", key: "showLabels" },
    { id: "showArc", key: "showArc" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 30;
    state.pbx = 0; state.pby = 2; state.pbz = 0;
    state.showB = true; state.showProj = true; state.showLabels = true; state.showArc = true; state.auto = false;
    document.getElementById("showB").checked = true;
    document.getElementById("showProj").checked = true;
    document.getElementById("showLabels").checked = true;
    document.getElementById("showArc").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    fit();
    scene.reset();
    render();
  });

  /* ------------------------------------------------ 教材数值自检（失败即抛错） */
  (function selfTest() {
    function near(a, b, eps) { return Math.abs(a - b) < (eps === undefined ? 1e-6 : eps); }

    // 1) 式(2-14)：θ=30° 时 ᴬ_BR 的三列
    var R = FK.M4.rotation(FK.M4.rotZ(30 * FK.DEG));
    var col1 = [R[0], R[3], R[6]];
    var col2 = [R[1], R[4], R[7]];
    var col3 = [R[2], R[5], R[8]];
    if (!FK.Vec.eq(FK.Vec.round(col1, 3), [0.866, 0.5, 0], 1e-3)) throw new Error("列1自检失败 " + col1);
    if (!FK.Vec.eq(FK.Vec.round(col2, 3), [-0.5, 0.866, 0], 1e-3)) throw new Error("列2自检失败 " + col2);
    if (!FK.Vec.eq(FK.Vec.round(col3, 3), [0, 0, 1], 1e-3)) throw new Error("列3自检失败 " + col3);

    // 2) 例2.1 / 式(2-16)：ᴮP = [0,2,0] 时 ᴬP = [-1.000, 1.732, 0.000]
    var Pa = FK.M4.applyDir(FK.M4.rotZ(30 * FK.DEG), [0, 2, 0]);
    if (!FK.Vec.eq(FK.Vec.round(Pa, 3), [-1, 1.732, 0], 1e-3)) throw new Error("式(2-16)自检失败 " + Pa);
    if (!FK.Vec.eq(FK.Vec.round(Pa, 9), [-1, Math.sqrt(3), 0], 1e-9)) throw new Error("例2.1 精确值自检失败 " + Pa);

    // 3) 式(2-12)：ᴬP 的每个分量 = 相应单位矢量与 ᴮP 的点积
    var Pb = [0, 2, 0];
    var dots = [
      FK.Vec.dot([R[0], R[1], R[2]], Pb),
      FK.Vec.dot([R[3], R[4], R[5]], Pb),
      FK.Vec.dot([R[6], R[7], R[8]], Pb)
    ];
    if (!FK.Vec.eq(FK.Vec.round(dots, 9), FK.Vec.round(Pa, 9), 1e-9)) throw new Error("式(2-12)点积自检失败 " + dots);

    // 4) 一般情形：ᴬP = ᴬ_BR·ᴮP 且长度保持（纯姿态映射不改变矢量长度）
    var Pb2 = [1.3, -2.2, 0.7];
    var Pa2 = FK.M4.applyDir(FK.M4.rotZ(-73 * FK.DEG), Pb2);
    if (Math.abs(FK.Vec.len(Pa2) - FK.Vec.len(Pb2)) > 1e-9) throw new Error("长度保持自检失败");
  }());

  fit();
  window.addEventListener("resize", function () {
    fit();
    scene.reset();
    render();
  });
  render();
}());
"""

FIGURE = {
    "id": "figure-2-5",
    "title": "图2-5 矢量的旋转 · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
