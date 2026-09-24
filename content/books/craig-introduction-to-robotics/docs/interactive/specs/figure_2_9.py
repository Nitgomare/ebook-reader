"""图2-9 平移算子（克雷格《机器人学导论（第3版）》2.4 节，式(2-24)~式(2-26)）。

教材依据：
- 图2-9 段原文：“平移将空间中的一个点沿着一个已知的矢量方向移动一定距离……
  当一个矢量相对于一个坐标系‘向前移动’时，既可以认为是矢量‘向前移动’，
  也可以认为坐标系‘向后移动’，二者的数学表达式是相同的，只不过是观察位置不同。
  图2-9 表示矢量 ᴬP₁ 怎样通过矢量 ᴬQ 进行平移。这里，矢量 ᴬQ 给出了进行平移的信息。”
- 式(2-24)：ᴬP₂ = ᴬP₁ + ᴬQ（ᴬQ 即平移矢量 Q）。
- 式(2-25)：ᴬP₂ = D_Q(q)·ᴬP₁；q 是沿 Q̂ 方向的有符号平移量。
- 式(2-26)：D_Q(q) = [[1,0,0,q_x],[0,1,0,q_y],[0,0,1,q_z],[0,0,0,1]]。

符号说明（任务审查清单强调）：式(2-9)(映射)与式(2-24)(算子)数学表达式相同，
差别仅在 ᴬP_BORG 的定义（{B} 原点在 {A} 中的位置）——若改用 ᴮP_AORG，
两式之间就会出现符号变化，这正是“矢量向前移动”还是“坐标系向后移动”的区别。
本图“坐标系后移”模式据此画出 Ō' = O − ᴬQ，并把同一数学结果 ᴬP₂ 标出来。

自检：D_Q·[3,7,0] = [13,12,0]（Q=[10,5,0]，与式(2-34)的位移部分一致）；
P₁=[1,2,0]、Q=[2,1,1] ⇒ P₂=[3,3,1]（同一元素分别用加式(2-24)和 D_Q 式(2-26) 计算，结果必须一致）；
D_Q 的最后一行为 [0,0,0,1]；D_Q 的逆把 P₂ 还原为 P₁。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.readout .row { white-space: normal; }
.readout .row.matrix { font-size: 13px; }
.readout .row.matrix b { color: var(--blue-dark); font-weight: 700; }
.panel .hint { position: static; display: block; margin-top: 10px; border-radius: 9px; line-height: 1.6; white-space: normal; }
.viewport { z-index: 0; }
.panel, .readout, .hint { z-index: 2; }
@media (max-width: 720px) {
  .readout { font-size: 12px; }
  .readout .row.matrix { font-size: 11.5px; }
  .readout .small { font-size: 11.5px; }
  .legend { font-size: 11px; }
  .panel .hint { display: none; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="图2-9 平移算子：矢量ᴬP₁沿ᴬQ平移得ᴬP₂，以及坐标系后移的等价解释">
  <defs>
    <marker id="arrowA" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"></path>
    </marker>
    <marker id="arrowP1" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="arrowQ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="arrowP2" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
    <marker id="arrowAp" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="ghost"></g>
  <g id="axesA"></g>
  <g id="axesB"></g>
  <g id="compLayer"></g>
  <g id="vecLayer"></g>
</svg>

<section class="panel" aria-label="图2-9 控制面板">
  <div class="panel-head">
    <div>
      <h1>图2-9 平移算子</h1>
      <p class="subtitle">ᴬP₂ = ᴬP₁ + ᴬQ（式2-24），写成矩阵算子即 ᴬP₂ = D_Q(q)·ᴬP₁（式2-25、式2-26）。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="tabs">
    <button id="modeVec" type="button" class="is-active">① 矢量前移</button>
    <button id="modeFrame" type="button">② 坐标系后移</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="p1x">ᴬP₁ 的 x 分量</label><output id="p1xValue">1.00</output></div>
    <input id="p1x" type="range" min="-5" max="5" step="0.1" value="1">
  </div>
  <div class="control">
    <div class="control-head"><label for="p1y">ᴬP₁ 的 y 分量</label><output id="p1yValue">2.00</output></div>
    <input id="p1y" type="range" min="-5" max="5" step="0.1" value="2">
  </div>
  <div class="control">
    <div class="control-head"><label for="p1z">ᴬP₁ 的 z 分量</label><output id="p1zValue">0.00</output></div>
    <input id="p1z" type="range" min="-5" max="5" step="0.1" value="0">
  </div>
  <div class="control">
    <div class="control-head"><label for="qx">ᴬQ 的 x 分量 q_x</label><output id="qxValue">2.00</output></div>
    <input id="qx" type="range" min="-5" max="5" step="0.1" value="2">
  </div>
  <div class="control">
    <div class="control-head"><label for="qy">ᴬQ 的 y 分量 q_y</label><output id="qyValue">1.00</output></div>
    <input id="qy" type="range" min="-5" max="5" step="0.1" value="1">
  </div>
  <div class="control">
    <div class="control-head"><label for="qz">ᴬQ 的 z 分量 q_z</label><output id="qzValue">1.00</output></div>
    <input id="qz" type="range" min="-5" max="5" step="0.1" value="1">
  </div>

  <div class="options">
    <label><input id="showD" type="checkbox" checked>显示 4×4 平移算子 D_Q</label>
    <label><input id="showComp" type="checkbox" checked>显示平移平行四边形</label>
    <label><input id="showLabels" type="checkbox" checked>显示分量数值</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i style="background:#c26a10"></i>ᴬP₁（原矢量）</span>
    <span><i style="background:#7c3aed"></i>ᴬQ（平移矢量）</span>
    <span><i style="background:#0e7490"></i>ᴬP₂ = ᴬP₁ + ᴬQ</span>
    <span><i class="dot" style="background:#12944f"></i>后移后的坐标系原点 O'</span>
  </div>

  <div class="hint" id="modeNote">
    “当一个矢量相对于一个坐标系‘向前移动’时，既可以认为是矢量‘向前移动’，
    也可以认为坐标系‘向后移动’，二者的数学表达式是相同的，只不过是观察位置不同。”
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row"><strong>ᴬP₁</strong> = [ <span id="r1x">1.000</span>, <span id="r1y">2.000</span>, <span id="r1z">0.000</span> ]<sup>T</sup></div>
  <div class="row"><strong>ᴬQ</strong> = [ <span id="rqx">2.000</span>, <span id="rqy">1.000</span>, <span id="rqz">1.000</span> ]<sup>T</sup>
    <span class="small" id="qmag">（q = 2.449）</span></div>
  <div class="row"><strong>ᴬP₂</strong> = [ <span id="r2x">3.000</span>, <span id="r2y">3.000</span>, <span id="r2z">1.000</span> ]<sup>T</sup>
    <span class="small">= ᴬP₁ + ᴬQ</span></div>
  <div class="row matrix" id="dqRow"><b>D_Q(q)</b> =
    第1行 [ 1, 0, 0, <span id="qmx">2.000</span> ]；
    第2行 [ 0, 1, 0, <span id="qmy">1.000</span> ]；
    第3行 [ 0, 0, 1, <span id="qmz">1.000</span> ]；<br>
    第4行 [ 0, 0, 0, <span id="qm1">1</span> ]（齐次变换的最后一行）</div>
  <div class="row small" id="modeReadout">模式①：矢量 ᴬP₁ 沿 ᴬQ“向前移动”到 ᴬP₂。</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var ghostLayer = document.getElementById("ghost");
  var axesA = document.getElementById("axesA");
  var axesB = document.getElementById("axesB");
  var compLayer = document.getElementById("compLayer");
  var vecLayer = document.getElementById("vecLayer");

  var scene = new FK.Scene({ svg: viewport, origin: { x: 560, y: 352 }, scale: 76, yaw: -0.5, pitch: 0.36 });

  // 响应式取景：视口窄时缩小 viewBox，让刻度文字不被等比压得太小
  var LAYOUTS = [
    { max: 720, view: [700, 470], origin: { x: 348, y: 194 }, scale: 46 },
    { max: 1e9, view: [1000, 620], origin: { x: 560, y: 330 }, scale: 50 }
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
    A: "#475569", p1: "#c26a10", q: "#7c3aed", p2: "#0e7490",
    comp: "#94a3b8", ghost: "#cbd5e1", originB: "#12944f"
  };

  var state = {
    p1x: 1, p1y: 2, p1z: 0,
    qx: 2, qy: 1, qz: 1,
    mode: "vec",
    showD: true, showComp: true, showLabels: true, auto: false
  };

  function drawAxisFrame(layer, matrix, cfg) {
    var length = 3.05;
    var dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    var origin = FK.M4.apply(matrix, [0, 0, 0]);
    var withLabels = cfg.labels !== false;
    for (var i = 0; i < 3; i += 1) {
      var tip = FK.M4.apply(matrix, FK.Vec.scale(dirs[i], length));
      var a = scene.project(origin);
      var b = scene.project(tip);
      scene.el("line", {
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        stroke: cfg.colors[i], "stroke-width": cfg.width,
        "marker-end": "url(#" + cfg.markers[i] + ")"
      }, layer);
      if (!withLabels) continue;
      var label = scene.el("text", {
        x: b.x + cfg.dx[i], y: b.y + cfg.dy[i], fill: cfg.colors[i],
        "font-size": 16.5, "font-style": "italic", class: "fk-axis-label"
      }, layer);
      label.textContent = cfg.labelTexts ? cfg.labelTexts[i] : (cfg.labels ? cfg.labels[i] : ["X\u0302", "Y\u0302", "Z\u0302"][i]);
    }
    var o = scene.project(origin);
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.4, fill: "#334155" }, layer);
    if (!withLabels) return;
    var tag = scene.el("text", { x: o.x + cfg.originDx, y: o.y + cfg.originDy, class: "fk-origin-label" }, layer);
    tag.textContent = cfg.originLabel;
  }

  /** 带箭头的矢量（世界坐标） */
  function drawArrow(from, to, color, marker, width, dash, layer) {
    var a = scene.project(from);
    var b = scene.project(to);
    scene.el("line", {
      x1: a.x, y1: a.y, x2: b.x, y2: b.y,
      stroke: color, "stroke-width": width, "stroke-dasharray": dash || null,
      "marker-end": "url(#" + marker + ")"
    }, layer || vecLayer);
    return b;
  }

  function drawProjectionLadder(P, comps) {
    var U = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    var colors = ["#d93025", "#2563eb", "#12944f"];
    var tags = ["x", "y", "z"];
    for (var i = 0; i < 3; i += 1) {
      if (Math.abs(comps[i]) < 0.06) continue;
      var n = Math.max(1, Math.round(Math.abs(comps[i])));
      var sgn = comps[i] >= 0 ? 1 : -1;
      var w = [1, 0, 0], h = [0, 1, 0];
      if (tags[i] === "x") { w = [0, 1, 0]; h = [0, 0, 1]; }
      else if (tags[i] === "y") { w = [1, 0, 0]; h = [0, 0, 1]; }
      var step = n > 5 ? n / 5 : 1;
      for (var t = 0; t <= n + 1e-9; t += step) {
        var base = FK.Vec.scale(U[i], sgn * t);
        scene.line(FK.Vec.add(base, FK.Vec.scale(w, -0.09)), FK.Vec.add(base, FK.Vec.scale(w, 0.09)),
          { stroke: colors[i], "stroke-width": 1.5, opacity: 0.72 }, compLayer);
        scene.line(FK.Vec.add(base, FK.Vec.scale(h, -0.09)), FK.Vec.add(base, FK.Vec.scale(h, 0.09)),
          { stroke: colors[i], "stroke-width": 1.5, opacity: 0.72 }, compLayer);
      }
    }
  }

  function render() {
    gridLayer.replaceChildren();
    ghostLayer.replaceChildren();
    axesA.replaceChildren();
    axesB.replaceChildren();
    compLayer.replaceChildren();
    vecLayer.replaceChildren();

    scene.grid(3, 1, null, gridLayer);

    var P1 = [state.p1x, state.p1y, state.p1z];
    var Q = [state.qx, state.qy, state.qz];
    var P2 = FK.Vec.add(P1, Q);
    var O = [0, 0, 0];

    drawAxisFrame(axesA, FK.M4.identity(), {
      labels: ["X\u0302\u2090", "Y\u0302\u2090", "Z\u0302\u2090"],
      colors: [COLORS.A, COLORS.A, COLORS.A],
      markers: ["arrowA", "arrowA", "arrowA"],
      dx: [10, 10, 10], dy: [-8, -8, -8], width: 3.1,
      originDx: -30, originDy: 26, originLabel: "O（{A} 原点）"
    });

    /* 模式②：坐标系“向后移动”——同一数学表达式，观察位置不同。
       教材用 ᴬP_BORG 定义 {B} 原点位置使式(2-9)与式(2-24)表达式相同；
       若改用 ᴮP_AORG，两式之间出现符号变化。此处画出 O' = O − ᴬQ。 */
    if (state.mode === "frame") {
      var negQ = FK.Vec.scale(Q, -1);
      var qLen = FK.Vec.len(Q);
      var farEnough = qLen > 0.35;
      drawAxisFrame(ghostLayer, FK.M4.identity(), {
        labels: false,
        colors: [COLORS.ghost, COLORS.ghost, COLORS.ghost],
        markers: ["", "", ""], dx: [0, 0, 0], dy: [0, 0, 0], width: 2.2,
        originDx: -18, originDy: 18, originLabel: "O"
      });
      drawAxisFrame(axesB, FK.M4.translate(negQ), {
        labels: true,
        labelTexts: ["X\u0302\u2090\u2032", "Y\u0302\u2090\u2032", "Z\u0302\u2090\u2032"],
        colors: [COLORS.originB, COLORS.originB, COLORS.originB],
        markers: ["arrowAp", "arrowAp", "arrowAp"],
        dx: [11, 11, 11], dy: [-8, 10, -8], width: 2.6,
        originDx: 12, originDy: -16, originLabel: "O' = O \u2212 \u1d2cQ"
      });
      if (farEnough) {
        // {B} 中读出的同一矢量：ᴮP = ᴬP₂ − (−Q) 的几何含义
        drawArrow(O, negQ, COLORS.originB, "arrowAp", 2.6, "9 6", compLayer);
        var mid = scene.project(FK.Vec.scale(negQ, 0.5));
        var t = scene.el("text", {
          x: mid.x + 10, y: mid.y - 8, fill: "#0f766e", "font-size": 13.5, class: "fk-point-label"
        }, compLayer);
        t.textContent = "\u2212\u1d2cQ\uff08\u5750\u6807\u7cfb\u540e\u79fb\uff09";
      }
    }

    // 平移平行四边形：O→P₁、P₁→P₂、O→ᴬQ（教材图2-9 的作图法）
    if (state.showComp) {
      var links = [[O, P1], [P1, P2], [O, Q]];
      for (var i = 0; i < links.length; i += 1) {
        var a = scene.project(links[i][0]);
        var b = scene.project(links[i][1]);
        scene.el("line", {
          x1: a.x, y1: a.y, x2: b.x, y2: b.y,
          stroke: COLORS.comp, class: "fk-projection"
        }, compLayer);
      }
      drawProjectionLadder(P1, P1);
    }

    // ᴬP₁（原矢量，从 O 出发）
    var e1 = drawArrow(O, P1, COLORS.p1, "arrowP1", 4.4);
    // ᴬP₂ = ᴬP₁ + ᴬQ（从 O 出发的平移结果）
    var e3 = drawArrow(O, P2, COLORS.p2, "arrowP2", 4.6);
    // ᴬQ：由 P₁ 末端指向 P₂ 末端的平移段（长度 = |Q|）
    var qTo = FK.Vec.add(P1, Q);
    drawArrow(P1, qTo, COLORS.q, "arrowQ", 3.4, "10 6");
    var midQ = scene.project(FK.Vec.add(P1, FK.Vec.scale(Q, 0.5)));
    var lq = scene.el("text", { x: midQ.x + 14, y: midQ.y - 18, fill: "#5b21b6", "font-size": 17, class: "fk-point-label" }, vecLayer);
    lq.textContent = "\u1d2cQ";
    if (state.showLabels) {
      var vq = scene.el("text", { x: midQ.x + 14, y: midQ.y - 2, fill: "#5b21b6", "font-size": 12.5, class: "fk-point-label" }, vecLayer);
      vq.textContent = "[" + FK.format(Q[0], 2) + ", " + FK.format(Q[1], 2) + ", " + FK.format(Q[2], 2) + "]\u1d40";
    }

    scene.el("circle", { cx: e1.x, cy: e1.y, r: 5.4, fill: COLORS.p1, class: "fk-point" }, vecLayer);
    scene.el("circle", { cx: e3.x, cy: e3.y, r: 6.2, fill: COLORS.p2, class: "fk-point" }, vecLayer);

    var l1 = scene.el("text", { x: e1.x - 70, y: e1.y + 24, fill: "#8a4a08", "font-size": 15.5, class: "fk-point-label" }, vecLayer);
    l1.textContent = "\u1d2cP\u2081";
    var l3 = scene.el("text", { x: e3.x + 12, y: e3.y - 14, fill: "#0e7490", "font-size": 18, class: "fk-point-label" }, vecLayer);
    l3.textContent = "\u1d2cP\u2082";

    if (state.showLabels) {
      var t1 = scene.el("text", { x: e1.x - 70, y: e1.y + 41, fill: "#8a4a08", "font-size": 12.5, class: "fk-point-label" }, vecLayer);
      t1.textContent = "[" + FK.format(P1[0], 2) + ", " + FK.format(P1[1], 2) + ", " + FK.format(P1[2], 2) + "]\u1d40";
      var t3 = scene.el("text", { x: e3.x + 12, y: e3.y + 8, fill: "#0e7490", "font-size": 13, class: "fk-point-label" }, vecLayer);
      t3.textContent = "[" + FK.format(P2[0], 2) + ", " + FK.format(P2[1], 2) + ", " + FK.format(P2[2], 2) + "]\u1d40";
    }

    /* -------------------------------------------------- 读数 */
    document.getElementById("r1x").textContent = FK.format(P1[0], 3);
    document.getElementById("r1y").textContent = FK.format(P1[1], 3);
    document.getElementById("r1z").textContent = FK.format(P1[2], 3);
    document.getElementById("rqx").textContent = FK.format(Q[0], 3);
    document.getElementById("rqy").textContent = FK.format(Q[1], 3);
    document.getElementById("rqz").textContent = FK.format(Q[2], 3);
    document.getElementById("r2x").textContent = FK.format(P2[0], 3);
    document.getElementById("r2y").textContent = FK.format(P2[1], 3);
    document.getElementById("r2z").textContent = FK.format(P2[2], 3);
    document.getElementById("qmag").textContent = "\uff08q = " + FK.format(FK.Vec.len(Q), 3) + "\uff09";

    // 式(2-26) 的 D_Q：平移量直接来自 q 与 D_Q·ᴬP₁ 的计算结果
    var D = FK.M4.translate(Q);
    var P2m = FK.M4.apply(D, P1);
    document.getElementById("qmx").textContent = FK.format(D[3], 3);
    document.getElementById("qmy").textContent = FK.format(D[7], 3);
    document.getElementById("qmz").textContent = FK.format(D[11], 3);
    document.getElementById("qm1").textContent = FK.format(D[15], 0);
    document.getElementById("dqRow").style.display = state.showD ? "" : "none";

    var note = document.getElementById("modeReadout");
    if (state.mode === "vec") {
      note.textContent = "\u6a21\u5f0f\u2460\uff1a\u77e2\u91cf \u1d2cP\u2081 \u6cbf \u1d2cQ \u201c\u5411\u524d\u79fb\u52a8\u201d\u5230 \u1d2cP\u2082\uff1b"
        + "D_Q\u00b7\u1d2cP\u2081 = [" + FK.format(P2m[0], 3) + ", " + FK.format(P2m[1], 3) + ", " + FK.format(P2m[2], 3) + "]\u1d40\u3002";
    } else {
      note.textContent = "\u6a21\u5f0f\u2461\uff1a\u5750\u6807\u7cfb\u201c\u5411\u540e\u79fb\u52a8\u201d\u5230 O' = O \u2212 \u1d2cQ\uff0c"
        + "\u540c\u4e00\u77e2\u91cf\u5728\u65b0\u5750\u6807\u7cfb\u4e2d\u7684\u8868\u8fbe\u53d8\u4e3a \u1d2cP\u2082 \u2212 (\u2212\u1d2cQ) = \u1d2cP\u2081\uff0c"
        + "\u6570\u5b66\u8868\u8fbe\u5f0f\u4e0e\u6a21\u5f0f\u2460\u76f8\u540c\u3002";
    }

    document.getElementById("modeVec").className = state.mode === "vec" ? "is-active" : "";
    document.getElementById("modeFrame").className = state.mode === "frame" ? "is-active" : "";
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "p1x", key: "p1x", value: 1, format: function (v) { return FK.format(v, 2); } },
    { id: "p1y", key: "p1y", value: 2, format: function (v) { return FK.format(v, 2); } },
    { id: "p1z", key: "p1z", value: 0, format: function (v) { return FK.format(v, 2); } },
    { id: "qx", key: "qx", value: 2, format: function (v) { return FK.format(v, 2); } },
    { id: "qy", key: "qy", value: 1, format: function (v) { return FK.format(v, 2); } },
    { id: "qz", key: "qz", value: 1, format: function (v) { return FK.format(v, 2); } }
  ], state, render);

  FK.bindToggles([
    { id: "showD", key: "showD" },
    { id: "showComp", key: "showComp" },
    { id: "showLabels", key: "showLabels" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  document.getElementById("modeVec").addEventListener("click", function () {
    state.mode = "vec";
    render();
  });
  document.getElementById("modeFrame").addEventListener("click", function () {
    state.mode = "frame";
    render();
  });

  document.getElementById("reset").addEventListener("click", function () {
    state.p1x = 1; state.p1y = 2; state.p1z = 0;
    state.qx = 2; state.qy = 1; state.qz = 1;
    state.mode = "vec";
    state.showD = true; state.showComp = true; state.showLabels = true; state.auto = false;
    document.getElementById("showD").checked = true;
    document.getElementById("showComp").checked = true;
    document.getElementById("showLabels").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    fit();
    scene.reset();
    render();
  });

  /* ------------------------------------------------ 教材数值自检（失败即抛错） */
  (function selfTest() {
    // 1) 式(2-26)：最后一行必须是 [0,0,0,1]
    var D = FK.M4.translate([10, 5, 0]);
    if (!FK.Vec.eq([D[12], D[13], D[14]], [0, 0, 0], 1e-12) || Math.abs(D[15] - 1) > 1e-12) {
      throw new Error("D_Q 最后一行自检失败");
    }
    // 2) 式(2-24) 与式(2-25)/(2-26) 必须给出同一结果：Q=[10,5,0]、P₁=[3,7,0] ⇒ [13,12,0]
    //    （与例2.2、式(2-34) 的位移部分一致：9.098+... 的纯平移情形）
    var p1 = [3, 7, 0], q = [10, 5, 0];
    var sum = FK.Vec.add(p1, q);
    var viaD = FK.M4.apply(FK.M4.translate(q), p1);
    if (!FK.Vec.eq(FK.Vec.round(sum, 9), [13, 12, 0], 1e-9)) throw new Error("式(2-24)自检失败 " + sum);
    if (!FK.Vec.eq(FK.Vec.round(viaD, 9), FK.Vec.round(sum, 9), 1e-12)) throw new Error("式(2-25)自检失败 " + viaD);
    // 3) 默认参数：P₁=[1,2,0]、Q=[2,1,1] ⇒ P₂=[3,3,1]
    if (!FK.Vec.eq(FK.Vec.add([1, 2, 0], [2, 1, 1]), [3, 3, 1], 1e-12)) throw new Error("默认值自检失败");
    // 4) 逆算子把 P₂ 还原为 P₁
    var back = FK.M4.apply(FK.M4.inverse(FK.M4.translate([2, 1, 1])), [3, 3, 1]);
    if (!FK.Vec.eq(FK.Vec.round(back, 9), [1, 2, 0], 1e-9)) throw new Error("逆算子自检失败 " + back);
    // 5) 坐标系后移：O' = O − Q，则同一矢量在新系中读作 P₂ − (−Q) = P₁
    var O2 = FK.Vec.scale([2, 1, 1], -1);
    if (!FK.Vec.eq(FK.Vec.sub([3, 3, 1], O2), [1, 2, 0], 1e-12)) throw new Error("坐标系后移自检失败");
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
    "id": "figure-2-9",
    "title": "图2-9 平移算子 · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
