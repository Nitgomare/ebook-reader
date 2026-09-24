"""图2-17 / 图2-18 合页：X-Y-Z 固定角与 Z-Y-X 欧拉角的对偶性。

教材依据（克雷格《机器人学导论（第3版）》第2章“姿态的其他描述方法”）：
- 图2-17 / 式(2-63)：X-Y-Z 固定角坐标系。令 {B} 与 {A} 重合，先绕 X̂_A 转 γ，
  再绕 Ŷ_A 转 β，最后绕 Ẑ_A 转 α；三个旋转轴始终是固定参考系 {A} 的轴。
  ᴬR_XYZ(γ,β,α) = R_Z(α)·R_Y(β)·R_X(γ)，乘积结果见式(2-64)。
- 图2-18 / 式(2-69)~(2-71)：Z-Y-X 欧拉角。每次绕**运动坐标系**当前的新轴旋转：
  先绕 Ẑ 转 α 得 {B′}，再绕 Ŷ′ 转 β 得 {B″}，最后绕 X̂″ 转 γ 得 {B}；
  ᴬR = ᴬ_{B′}R · ^{B′}_{B″}R · ^{B″}_B R = R_Z(α)·R_Y(β)·R_X(γ)（式2-70），
  与式(2-63)形式完全相同。
- 对偶性（正文紧接式(2-71)之后的结论）：三次绕固定轴旋转的最终姿态，与以**相反顺序**
  三次绕运动坐标轴旋转的最终姿态相同；因此式(2-71)与式(2-64)等价（正文原文：
  “因为式 (2-71) 和式 (2-64) 等价, 所以无需通过旋转矩阵的反复计算去求Z-Y-X欧拉角”）。
  本页把这两条路径并排放进一个页面：标签页切换两种“轴如何变”的描述，
  读数区同时算出两条路径的 3×3 矩阵并给出逐元素残差（恒为 0，即完全等价）。

注：教材式(2-72)是 Z-Y-Z 欧拉角，不是本页的 Z-Y-X；本页对偶性依据的是
式(2-63)/(2-64) 与式(2-69)~(2-71) 的等价关系。

本页用到的公共底座函数：FK.M4.fromFixedXYZ(γ,β,α)（式2-63）与
FK.M4.fromEulerZYX(α,β,γ)（式2-71），二者在教材语义下互为对偶、结果相同。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="图2-17 X-Y-Z固定角与图2-18 Z-Y-X欧拉角的对比交互示意图">
  <defs>
    <marker id="mkA" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"></path></marker>
    <marker id="mkX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path></marker>
    <marker id="mkY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path></marker>
    <marker id="mkZ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path></marker>
    <marker id="mkMove" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5.2" markerHeight="5.2"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path></marker>
  </defs>
  <g id="grid"></g>
  <g id="ghost"></g>
  <g id="fixedAxes"></g>
  <g id="arcLayer"></g>
  <g id="frameA"></g>
  <g id="framesMid"></g>
  <g id="frameB"></g>
  <g id="notes"></g>
</svg>

<section class="panel" aria-label="图2-17与图2-18控制面板">
  <div class="panel-head">
    <div>
      <h1>图2-17 / 图2-18 固定角与欧拉角</h1>
      <p class="subtitle" id="subtitle">固定角 X-Y-Z：三次都绕 {A} 的固定轴，顺序 X(γ) → Y(β) → Z(α)。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="tabs" role="tablist">
    <button id="tabFixed" class="is-active" type="button">固定角 X-Y-Z（图2-17）</button>
    <button id="tabEuler" type="button">欧拉角 Z-Y-X（图2-18）</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="alpha">α（绕 Ẑ 的转角）</label><output id="alphaValue">30.0°</output></div>
    <input id="alpha" type="range" min="-180" max="180" step="1" value="30">
  </div>
  <div class="control">
    <div class="control-head"><label for="beta">β（绕 Ŷ 的转角）</label><output id="betaValue">30.0°</output></div>
    <input id="beta" type="range" min="-90" max="90" step="1" value="30">
  </div>
  <div class="control">
    <div class="control-head"><label for="gamma">γ（绕 X̂ 的转角）</label><output id="gammaValue">30.0°</output></div>
    <input id="gamma" type="range" min="-180" max="180" step="1" value="30">
  </div>

  <div class="options">
    <label><input id="showMid" type="checkbox" checked>显示中间坐标系 {B′}/{B″}</label>
    <label><input id="showFixed" type="checkbox" checked>显示固定参考轴与旋转弧</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i style="background:#64748b"></i>{A} 固定轴</span>
    <span><i style="background:#d93025"></i>X̂ 轴</span>
    <span><i style="background:#2563eb"></i>Ŷ 轴</span>
    <span><i style="background:#12944f"></i>Ẑ 轴</span>
    <span><i style="background:#7c3aed"></i>旋转轴与转角</span>
    <span><i style="background:#9aa7b8"></i>另一条路径的中间系（幽灵）</span>
  </div>
  <p class="subtitle" style="margin-bottom:0" id="dofNote">固定轴：X̂_A、Ŷ_A、Ẑ_A 三条轴全程不动。</p>
</section>

<div class="hint">拖动旋转视角 · 滚轮缩放 · 双击复位</div>

<div class="readout" id="readout">
  <div class="row small readout-row" id="routeA">固定角 ᴬR_XYZ(γ,β,α) := R_Z(α)·R_Y(β)·R_X(γ)　【式2-63】</div>
  <table class="m3" aria-label="旋转矩阵">
    <tr><td id="m11">0.000</td><td id="m12">0.000</td><td id="m13">0.000</td></tr>
    <tr><td id="m21">0.000</td><td id="m22">0.000</td><td id="m23">0.000</td></tr>
    <tr><td id="m31">0.000</td><td id="m32">0.000</td><td id="m33">0.000</td></tr>
  </table>
  <div class="row small readout-row" id="routeB">欧拉角 ᴬR_Z′Y′X′(α,β,γ) := R_Z(α)·R_Y(β)·R_X(γ)　【式2-70】</div>
  <div class="row small readout-row">对偶性校验：<span id="dualText">两条路径矩阵相同（逐元素差 0）</span>　max|Δr| = <span id="dualResidual">0.0e+0</span>　tr = <span id="trace">0.000</span></div>
  <div class="row small wrap" id="frameColorNote">彩色细轴 = 最终 {B}（X̂ᴮ 红 / Ŷᴮ 蓝 / Ẑᴮ 绿）；淡色轴 = 中间系 {B′}、{B″}；灰色虚线 = 另一条路径的 {B′}、{B″}（两条路径最终 {B} 重合）</div>
</div>
"""

SCRIPT = r"""
(function () {
  var COL = {
    A: "#64748b",
    X: "#d93025", Y: "#2563eb", Z: "#12944f",
    X1: "#e0736a", Y1: "#6a97ea", Z1: "#5cb389",
    move: "#7c3aed",
    ghost: "#9aa7b8"
  };

  var viewport = document.getElementById("viewport");
  var layers = {};
  ["grid", "ghost", "fixedAxes", "arcLayer", "frameA", "framesMid", "frameB", "notes"].forEach(function (id) {
    layers[id] = document.getElementById(id);
  });

  var scene = new FK.Scene({
    svg: viewport,
    origin: { x: 600, y: 306 },
    scale: 84,
    yaw: -0.74,
    pitch: 0.44
  });

  function layout() {
    var W = viewport.clientWidth || window.innerWidth || 1000;
    var H = viewport.clientHeight || window.innerHeight || 700;
    var readout = document.querySelector(".readout");
    var panel = document.querySelector(".panel");
    var bandTop = readout ? readout.getBoundingClientRect().bottom : 0;
    var bandBottom = panel ? panel.getBoundingClientRect().top : H;
    computeUI(W);
    if (W <= 720) {
      /* 竖屏：viewBox 与元素同纵横比，1 用户单位 = PX 屏幕像素 */
      var PX = 0.8;
      var vbW = Math.round(W / PX);
      var vbH = Math.round(H / PX);
      viewport.setAttribute("viewBox", "0 0 " + vbW + " " + vbH);
      var band = Math.max(140, bandBottom - bandTop);
      var radius = Math.max(66, Math.min(band / 2 - 8, W / 2 - 14));
      UI.radius = radius / PX;
      UI.bandBottom = bandBottom / PX;
      scene.baseOrigin.x = vbW / 2;
      scene.baseOrigin.y = ((bandTop + bandBottom) / 2) / PX;
      scene.defaults.scale = (radius / 2.2) / PX;
    } else {
      viewport.setAttribute("viewBox", "0 0 1000 620");
      scene.baseOrigin.x = Math.max(W * 0.55, 520);
      scene.baseOrigin.y = H * 0.47;
      scene.defaults.scale = 88;
    }
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  var state = { alpha: 30, beta: 30, gamma: 30, mode: "fixed", showMid: true, showFixed: true, auto: false };

  /* 移动端：把 viewBox 改成与 iframe 同纵横比的“竖屏 viewBox”，
     使 SVG 用户单位与屏幕像素是固定倍率（px），字号/线宽就不必再缩放 */
  var UI = { font: 1, stroke: 1, halo: 5, mobile: false };

  function computeUI(w) {
    UI.mobile = w <= 720;
    UI.font = 1;
    UI.stroke = 1;
    UI.halo = 5;
  }

  function fs(base) { return Math.round(base * UI.font * 10) / 10; }
  function sw(base) { return Math.round(base * UI.stroke * 10) / 10; }

  function dir(m, col) {
    return [m[(col - 1) * 4], m[(col - 1) * 4 + 1], m[(col - 1) * 4 + 2]];
  }

  /* 绕正轴右手旋转时，弧从垂直基 u 扫到垂直基 v：X→(Y,Z)、Y→(Z,X)、Z→(X,Y) */
  var AXIS_WORLD = [
    [[0, 1, 0], [0, 0, 1]],
    [[0, 0, 1], [1, 0, 0]],
    [[1, 0, 0], [0, 1, 0]]
  ];

  /* ---------------- 姿态计算 ---------------- */

  function clearAxes(m) {
    return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
  }

  /* 图2-17：X-Y-Z 固定角，先后为 R_X(γ)、R_Y(β)、R_Z(α)；三个中间量都相对 {A} 描述 */
  function fixedSequence(al, be, gm) {
    var R1 = FK.M4.rotX(gm), R2 = FK.M4.rotY(be), R3 = FK.M4.rotZ(al);
    return {
      frames: [
        { R: R1, label: "R_X(γ)", desc: "{B} 绕 X̂_A 转 γ" },
        { R: FK.M4.multiply(R2, R1), label: "R_Y(β)R_X(γ)", desc: "再绕 Ŷ_A 转 β" },
        { R: FK.M4.multiply(R3, FK.M4.multiply(R2, R1)), label: "R_Z(α)R_Y(β)R_X(γ)", desc: "最后绕 Ẑ_A 转 α" }
      ],
      moves: [
        { angle: gm, axisIndex: 0, frame: "A", basis: AXIS_WORLD[0], tag: "γ 绕 X\u0302" },
        { angle: be, axisIndex: 1, frame: "A", basis: AXIS_WORLD[1], tag: "β 绕 Y\u0302" },
        { angle: al, axisIndex: 2, frame: "A", basis: AXIS_WORLD[2], tag: "α 绕 Z\u0302" }
      ]
    };
  }

  /* 图2-18：Z-Y-X 欧拉角，每次绕运动坐标系的新轴；{B′}、{B″} 逐级带撇号 */
  function eulerSequence(al, be, gm) {
    var base = clearAxes();
    var R1 = FK.M4.rotZ(al);
    var F1 = FK.M4.multiply(base, R1);
    var R2 = FK.M4.rotY(be);
    var F2 = matrixOnFrame(F1, R2);
    var R3 = FK.M4.rotX(gm);
    var F3 = matrixOnFrame(F2, R3);
    return {
      frames: [
        { R: F1, label: "R_Z(α)", desc: "{B′}：绕 Ẑ 转 α" },
        { R: F2, label: "R_Z(α)R_Y(β)", desc: "{B″}：再绕 Ŷ′ 转 β" },
        { R: F3, label: "R_Z(α)R_Y(β)R_X(γ)", desc: "{B}：最后绕 X̂″ 转 γ" }
      ],
      moves: [
        { angle: al, axisIndex: 2, frame: "{B}", basis: frameBasis(base, 2), tag: "α 绕 \u1e90" },
        { angle: be, axisIndex: 1, frame: "{B\u2032}", basis: frameBasis(F1, 1), tag: "β 绕 Y\u0302\u2032" },
        { angle: gm, axisIndex: 0, frame: "{B\u2033}", basis: frameBasis(F2, 0), tag: "γ 绕 X\u0302\u2033" }
      ]
    };
  }

  /* 在运动坐标系 F 上再绕其某轴转 rad（左乘），等价于 ^{A}_{F'}R = ^{A}_{F}R · R_axis(rad) */
  function matrixOnFrame(F, Raxis) {
    return FK.M4.multiply(F, Raxis);
  }

  /* 运动坐标系 F 中绕其第 axisIndex 个轴旋转时，弧所用的一对垂直基（取该系的另外两列） */
  function frameBasis(F, axisIndex) {
    var cols = [dir(F, 1), dir(F, 2), dir(F, 3)];
    if (axisIndex === 0) return [cols[1], cols[2]];
    if (axisIndex === 1) return [cols[2], cols[0]];
    return [cols[0], cols[1]];
  }

  function rotationMatrix(sequence) {
    return sequence.frames[2].R;
  }

  function matrix3(sequence) {
    var m = rotationMatrix(sequence);
    return FK.M4.rotation(m);
  }

  /* ---------------- 绘图 ---------------- */

  function projectPoint(v) { return scene.project(v); }

  function drawAxes(layer, R, cfg) {
    var origin = FK.M4.apply(R, [0, 0, 0]);
    var o = projectPoint(origin);
    var colored = cfg.colored;
    var labels = cfg.labels;
    var len = cfg.length === undefined ? 2.35 : cfg.length;
    var dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    for (var i = 0; i < 3; i += 1) {
      var tip = FK.M4.apply(R, FK.Vec.scale(dirs[i], len));
      var b = projectPoint(tip);
      scene.el("line", {
        x1: o.x, y1: o.y, x2: b.x, y2: b.y,
        stroke: colored[i],
        "stroke-width": sw(cfg.width === undefined ? 3.2 : cfg.width),
        "stroke-dasharray": cfg.dash ? (cfg.dash[0] * UI.stroke).toFixed(1) + " " + (cfg.dash[1] * UI.stroke).toFixed(1) : null,
        opacity: cfg.opacity === undefined ? 1 : cfg.opacity,
        "marker-end": cfg.marker ? "url(#" + cfg.marker + ")" : null
      }, layer);
      if (labels && labels[i]) {
        var up = b.y < o.y;
        var t = scene.el("text", {
          x: b.x + 8 * UI.font * 0.7,
          y: b.y + (up ? -8 : 20) * UI.font * 0.6,
          fill: colored[i],
          "font-size": fs(cfg.fontSize || 17),
          "font-style": "italic",
          "stroke-width": UI.halo,
          opacity: cfg.opacity === undefined ? 1 : cfg.opacity,
          class: "fk-axis-label"
        }, layer);
        t.textContent = labels[i];
      }
    }
    scene.el("circle", { cx: o.x, cy: o.y, r: sw(4.4), fill: "#334155", opacity: cfg.opacity === undefined ? 1 : cfg.opacity }, layer);
    if (cfg.originLabel) {
      var ot = scene.el("text", {
        x: o.x + 7 * UI.font * 0.6, y: o.y + 21 * UI.font * 0.7, class: "fk-origin-label",
        "font-size": fs(15), "stroke-width": UI.halo,
        opacity: cfg.opacity === undefined ? 1 : cfg.opacity
      }, layer);
      ot.textContent = cfg.originLabel;
    }
    return o;
  }

  /* 固定参考轴：以 {A} 为轴心的长半透明轴，强调“轴不动” */
  function drawFixedAxisLines() {
    var o = projectPoint([0, 0, 0]);
    var cfg = [
      { v: [1, 0, 0], c: COL.X, name: "X\u0302\u2090", step: "先绕 X\u0302\u2090 转 γ" },
      { v: [0, 1, 0], c: COL.Y, name: "Y\u0302\u2090", step: "再绕 Y\u0302\u2090 转 β" },
      { v: [0, 0, 1], c: COL.Z, name: "Z\u0302\u2090", step: "最后绕 Z\u0302\u2090 转 α" }
    ];
    cfg.forEach(function (item) {
      var half = UI.mobile ? 3.4 : 2.9;
      var a = projectPoint(FK.Vec.scale(item.v, -half));
      var b = projectPoint(FK.Vec.scale(item.v, half));
      scene.el("line", {
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        stroke: item.c, "stroke-width": sw(2), opacity: 0.26,
        "stroke-dasharray": (10 * UI.stroke).toFixed(1) + " " + (7 * UI.stroke).toFixed(1)
      }, layers.fixedAxes);
      var end = projectPoint(FK.Vec.scale(item.v, half));
      var compact = UI.mobile;
      var label = compact ? item.name : (item.name + "（" + item.step + "）");
      var t = scene.el("text", {
        x: end.x + 6 * UI.font * 0.7, y: end.y + (end.y < o.y ? -8 : 20) * UI.font * 0.6,
        fill: item.c, "font-size": fs(13.5), opacity: 0.95, "stroke-width": UI.halo, class: "fk-axis-label"
      }, layers.fixedAxes);
      t.textContent = label;
    });
  }

  /* 旋转弧：绕 axisInFrame 轴，从 u 方向转到 v 方向；u/v 垂直于该轴但可任意取，弧长即转角 */
  function drawArc(frameLabel, axisLabel, axisInFrame, u, v, angleRad, tint, radius, tag) {
    if (Math.abs(angleRad) < 2e-3) return;
    var o = FK.M4.apply(axisInFrame, [0, 0, 0]);
    var uv = FK.M4.applyDir(axisInFrame, u);
    var vv = FK.M4.applyDir(axisInFrame, v);
    var steps = 52;
    var pts = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = angleRad * (i / steps);
      var w = FK.Vec.add(FK.Vec.scale(uv, Math.cos(t)), FK.Vec.scale(vv, Math.sin(t)));
      pts.push(FK.Vec.add(o, FK.Vec.scale(w, radius)));
    }
    scene.polyline(pts, { stroke: tint, "stroke-width": sw(3), opacity: 0.95 }, layers.arcLayer);

    var p0 = projectPoint(pts[pts.length - 1]);
    var p1 = projectPoint(pts[pts.length - 2]);
    var hx = p0.x - p1.x, hy = p0.y - p1.y;
    var hl = Math.sqrt(hx * hx + hy * hy) || 1;
    hx /= hl; hy /= hl;
    var w1 = projectPoint(pts[Math.max(0, pts.length - 4)]);
    var wx = w1.x - p0.x, wy = w1.y - p0.y;
    var wl = Math.sqrt(wx * wx + wy * wy) || 1;
    wx /= wl; wy /= wl;
    var head = 13 * UI.stroke;
    scene.el("polyline", {
      points: [
        (p0.x - hx * head - wx * head * 0.55).toFixed(2) + "," + (p0.y - hy * head - wy * head * 0.55).toFixed(2),
        p0.x.toFixed(2) + "," + p0.y.toFixed(2),
        (p0.x - hx * head + wx * head * 0.55).toFixed(2) + "," + (p0.y - hy * head + wy * head * 0.55).toFixed(2)
      ].join(" "),
      fill: "none", stroke: tint, "stroke-width": sw(3), "stroke-linejoin": "round"
    }, layers.arcLayer);

    var mid = pts[Math.round(steps / 2)];
    var mp = projectPoint(mid);
    var op = projectPoint(o);
    var rx = mp.x - op.x, ry = mp.y - op.y;
    var rl = Math.sqrt(rx * rx + ry * ry) || 1;
    var label = scene.el("text", {
      x: mp.x + (rx / rl) * 20 * UI.stroke, y: mp.y + (ry / rl) * 20 * UI.stroke - 6,
      fill: tint,
      "font-size": fs(15), "font-weight": 700, "stroke-width": UI.halo,
      class: "fk-axis-label"
    }, layers.arcLayer);
    label.textContent = tag;
  }

  /* ---------------- 主绘制 ---------------- */

  function build() {
    var al = state.alpha * FK.DEG, be = state.beta * FK.DEG, gm = state.gamma * FK.DEG;
    var fixed = fixedSequence(al, be, gm);
    var euler = eulerSequence(al, be, gm);
    return { fixed: fixed, euler: euler, current: state.mode === "fixed" ? fixed : euler, other: state.mode === "fixed" ? euler : fixed };
  }

  function updateMatrixDom(seq) {
    var r = matrix3(seq);
    var ids = ["11", "12", "13", "21", "22", "23", "31", "32", "33"];
    for (var i = 0; i < 9; i += 1) {
      var node = document.getElementById("m" + ids[i]);
      if (node) node.textContent = FK.format(r[i], 3);
    }
    var tr = r[0] + r[4] + r[8];
    document.getElementById("trace").textContent = FK.format(tr, 3);
  }

  function render() {
    Object.keys(layers).forEach(function (k) { layers[k].replaceChildren(); });

    scene.grid(3, 1);

    var data = build();
    var R = rotationMatrix(data.current);

    /* 参考坐标系 {A}（固定） */
    drawAxes(layers.frameA, clearAxes(), {
      colored: [COL.A, COL.A, COL.A],
      labels: ["X\u0302\u2090", "Y\u0302\u2090", "Z\u0302\u2090"],
      marker: "mkA", width: 2.7, opacity: 0.95, originLabel: "O", fontSize: 16
    });

    /* 固定轴长线与旋转弧 */
    if (state.showFixed) {
      if (state.mode === "fixed") {
        drawFixedAxisLines();
      }
      data.current.moves.forEach(function (mv) {
        var tint = COL.move;
        if (state.mode === "euler") {
          tint = mv.frame === "{B}" ? "#7c3aed" : (mv.frame === "{B\u2032}" ? "#6d28d9" : "#5b21b6");
        }
        drawArc(mv.frame, mv.tag, clearAxes(), mv.basis[0], mv.basis[1], mv.angle, tint, 1.15, mv.tag);
      });
    }

    /* 幽灵：另一条路径的中间系。两条路径的最终 {B} 完全相同（对偶性），
       所以只把“另一条路径的中间步骤”画成灰虚线，才看得出中间步骤其实不一样 */
    if (state.showMid) {
      drawAxes(layers.ghost, data.other.frames[0].R, {
        colored: [COL.ghost, COL.ghost, COL.ghost],
        labels: null, dash: [11, 8], width: 2.2, opacity: 0.34
      });
      drawAxes(layers.ghost, data.other.frames[1].R, {
        colored: [COL.ghost, COL.ghost, COL.ghost],
        labels: null, dash: [6, 7], width: 2.2, opacity: 0.42
      });
    }

    /* 本路径的中间系：淡色细虚线，不抢主轴标签；底部一行说明随开关切换 */
    var frames = data.current.frames;
    if (state.showMid) {
      drawAxes(layers.framesMid, frames[0].R, {
        colored: [COL.X1, COL.Y1, COL.Z1],
        labels: null,
        dash: [9, 7], width: 2.2, opacity: 0.5, fontSize: 15
      });
      drawAxes(layers.framesMid, frames[1].R, {
        colored: [COL.X1, COL.Y1, COL.Z1],
        labels: labelsFor(2),
        dash: [5, 6], width: 2.4, opacity: 0.72, fontSize: 15
      });
    }
    var noteText;
    if (!state.showMid) {
      noteText = UI.mobile ? "中间坐标系已隐藏" : "中间坐标系已隐藏（只显示 {A} 与最终 {B}）";
    } else if (UI.mobile) {
      noteText = state.mode === "fixed"
        ? "淡色虚线 = 中间量 {B}\u2032、{B}\u2033（相对 {A}）"
        : "淡色虚线 = {B}\u2032、{B}\u2033（绕新轴转后的中间姿态）";
    } else {
      noteText = state.mode === "fixed"
        ? "淡色虚线 = 固定角三次旋转的中间量 {B}\u2032、{B}\u2033（都相对 {A} 描述，轴平行于 {A}）"
        : "淡色虚线 = 运动系中间姿态 {B}\u2032（绕 \u1e90 转 α 后）、{B}\u2033（再绕 Y\u0302\u2032 转 β 后）";
    }
    var noteY = UI.mobile ? (UI.bandBottom - 16) : 588;
    var pad = 8 * UI.stroke;
    var boxW = noteText.length * (UI.mobile ? 7.8 : 8.4) + 26;
    scene.el("rect", {
      x: 26 - pad, y: noteY - fs(13.5) - pad * 0.6,
      width: boxW, height: fs(13.5) + pad * 1.6, rx: 6,
      fill: "#ffffff", opacity: 0.8
    }, layers.notes);
    var tagMid = scene.el("text", {
      x: 26, y: noteY, fill: state.showMid ? "#54637a" : "#8b98a9",
      "font-size": fs(13.5), "stroke-width": 0, class: "fk-axis-label"
    }, layers.notes);
    tagMid.textContent = noteText;

    /* 最终 {B} */
    var finalLabels = ["X\u0302\u1d47", "Y\u0302\u1d47", "Z\u0302\u1d47"];
    drawAxes(layers.frameB, R, {
      colored: [COL.X, COL.Y, COL.Z],
      labels: finalLabels,
      marker: "mkX", width: 3.3, originLabel: null,
      fontSize: 17, length: 2.15
    });
    updateMatrixDom(data.current);

    var rA = matrix3(data.fixed), rB = matrix3(data.euler);
    var maxd = 0;
    for (var i = 0; i < 9; i += 1) maxd = Math.max(maxd, Math.abs(rA[i] - rB[i]));
    document.getElementById("dualResidual").textContent = maxd.toExponential(2);
    document.getElementById("dualText").textContent = maxd < 1e-12
      ? "两条路径矩阵逐元素完全相同（残差 0，等价）"
      : "两条路径矩阵存在偏差：" + maxd.toExponential(2);

    document.getElementById("routeA").textContent = state.mode === "fixed"
      ? "固定角 ᴬR_XYZ(γ,β,α) := R_Z(α)·R_Y(β)·R_X(γ)　【式2-63/2-64】"
      : "固定角（对偶参照）ᴬR_XYZ(γ,β,α) := R_Z(α)·R_Y(β)·R_X(γ)　【式2-63】";
    document.getElementById("routeB").textContent = state.mode === "euler"
      ? "欧拉角 ᴬR_Z′Y′X′(α,β,γ) := ᴬ_{B′}R·^{B′}_{B″}R·^{B″}_B R = R_Z(α)·R_Y(β)·R_X(γ)　【式2-69~2-71】"
      : "欧拉角（对偶参照）ᴬR_Z′Y′X′(α,β,γ) := R_Z(α)·R_Y(β)·R_X(γ)　【式2-70】";
  }

  function labelsFor(level) {
    if (state.mode === "euler") {
      if (level === 1) return ["X\u0302\u2032", "Y\u0302\u2032", "Z\u0302\u2032"];
      return ["X\u0302\u2032\u2032", "Y\u0302\u2032\u2032", "Z\u0302\u2032\u2032"];
    }
    return ["X\u0302\u2032", "Y\u0302\u2032", "Z\u0302\u2032"];
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "alpha", key: "alpha", value: 30, format: function (v) { return FK.deg(v, 1); } },
    { id: "beta", key: "beta", value: 30, format: function (v) { return FK.deg(v, 1); } },
    { id: "gamma", key: "gamma", value: 30, format: function (v) { return FK.deg(v, 1); } }
  ], state, render);

  FK.bindToggles([
    { id: "showMid", key: "showMid" },
    { id: "showFixed", key: "showFixed" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  function setMode(mode) {
    state.mode = mode;
    var tabFixed = document.getElementById("tabFixed");
    var tabEuler = document.getElementById("tabEuler");
    var isFixed = mode === "fixed";
    tabFixed.classList.toggle("is-active", isFixed);
    tabEuler.classList.toggle("is-active", !isFixed);
    tabFixed.setAttribute("aria-selected", isFixed ? "true" : "false");
    tabEuler.setAttribute("aria-selected", !isFixed ? "true" : "false");
    document.getElementById("subtitle").textContent = isFixed
      ? "固定角 X-Y-Z：三次都绕 {A} 的固定轴，顺序 X(γ) → Y(β) → Z(α)。"
      : "欧拉角 Z-Y-X：每次绕运动坐标系的新轴，顺序 Z(α) → Y′(β) → X″(γ)。";
    document.getElementById("dofNote").textContent = isFixed
      ? "固定轴：X̂_A、Ŷ_A、Ẑ_A 三条轴全程不动。"
      : "运动轴：Ẑ → Ŷ′ → X̂″ 随上一次旋转而改变方向。";
    render();
  }

  document.getElementById("tabFixed").addEventListener("click", function () { setMode("fixed"); });
  document.getElementById("tabEuler").addEventListener("click", function () { setMode("euler"); });

  document.getElementById("reset").addEventListener("click", function () {
    state.alpha = 30; state.beta = 30; state.gamma = 30;
    state.showMid = true; state.showFixed = true; state.auto = false;
    document.getElementById("showMid").checked = true;
    document.getElementById("showFixed").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    scene.state.scale = scene.defaults.scale;
    layout();
    setMode("fixed");
  });

  var resizeTimer = 0;
  window.addEventListener("resize", function () {
    if (resizeTimer) window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(function () { layout(); render(); }, 120);
  });

  /* ---------------- 数值自检 ---------------- */
  (function selfTest() {
    function maxDiff(a, b) {
      var m = 0;
      for (var i = 0; i < 9; i += 1) m = Math.max(m, Math.abs(a[i] - b[i]));
      return m;
    }
    function check(alDeg, beDeg, gmDeg) {
      var fixed = FK.M4.fromFixedXYZ(gmDeg * FK.DEG, beDeg * FK.DEG, alDeg * FK.DEG);
      var euler = FK.M4.fromEulerZYX(alDeg * FK.DEG, beDeg * FK.DEG, gmDeg * FK.DEG);
      var rf = FK.M4.rotation(fixed), re = FK.M4.rotation(euler);
      var d = maxDiff(rf, re);
      if (!(d < 1e-12)) {
        throw new Error("对偶性自检失败 (" + alDeg + "," + beDeg + "," + gmDeg + ")：max|Δr| = " + d);
      }
      var m = rotationMatrix(eulerSequence(alDeg * FK.DEG, beDeg * FK.DEG, gmDeg * FK.DEG));
      var d2 = maxDiff(FK.M4.rotation(m), re);
      if (!(d2 < 1e-12)) {
        throw new Error("逐步欧拉角自检失败：" + d2);
      }
      var det =
        m[0] * (m[5] * m[10] - m[6] * m[9]) -
        m[1] * (m[4] * m[10] - m[6] * m[8]) +
        m[2] * (m[4] * m[9] - m[5] * m[8]);
      if (Math.abs(det - 1) > 1e-9) throw new Error("旋转矩阵行列式不为 1：" + det);
    }
    check(30, 30, 30);
    check(40, 30, 20);
    check(-65, -40, 125);
  }());

  layout();
  var initialMode = "fixed";
  var params = {};
  try {
    (window.location.search || "").replace(/^\?/, "").split("&").forEach(function (pair) {
      var kv = pair.split("=");
      if (kv[0]) params[decodeURIComponent(kv[0]).toLowerCase()] = decodeURIComponent(kv[1] || "");
    });
    if ((params.mode || "").toLowerCase() === "euler") initialMode = "euler";
    [["alpha", "alpha"], ["beta", "beta"], ["gamma", "gamma"]].forEach(function (item) {
      var raw = Number(params[item[0]]);
      if (params[item[0]] !== undefined && isFinite(raw)) {
        var lo = item[0] === "beta" ? -90 : -180;
        var hi = item[0] === "beta" ? 90 : 180;
        state[item[1]] = Math.max(lo, Math.min(hi, raw));
      }
    });
    if (params.showmid === "0") { state.showMid = false; document.getElementById("showMid").checked = false; }
    if (params.showfixed === "0") { state.showFixed = false; document.getElementById("showFixed").checked = false; }
  } catch (error) { /* 忽略 */ }
  ranges.refresh();
  setMode(initialMode);
}());
"""

FIGURE = {
    "id": "figure-2-17-18",
    "title": "图2-17/2-18 X-Y-Z固定角与Z-Y-X欧拉角 · 对偶性交互演示",
    "css": COMMON_CSS + """
.m3 {
  margin: 6px 0 9px;
  border-collapse: collapse;
  font: 700 13.5px/1.45 ui-monospace, SFMono-Regular, Consolas, monospace;
}
.m3 td {
  min-width: 62px;
  padding: 1px 7px 1px 0;
  text-align: right;
  color: var(--blue-dark);
  border-left: 2px solid var(--line);
  padding-left: 8px;
}
.m3 tr:first-child td { padding-top: 3px; }
.m3 tr:last-child td { padding-bottom: 3px; }
.readout .wrap { white-space: normal; max-width: 420px; line-height: 1.45; }
.readout .readout-row { white-space: normal; max-width: 430px; }
@media (max-width: 720px) {
  .readout { font-size: 12px; line-height: 1.4; padding: 7px 9px; max-width: calc(100% - 16px); }
  .readout .small { font-size: 11px; }
  .readout .row, .readout .readout-row, .readout .wrap {
    white-space: normal;
    max-width: 100%;
    overflow-wrap: break-word;
    word-break: break-word;
  }
  .readout { overflow: hidden; }
  .readout strong { word-break: break-word; }
  .m3 { font-size: 12px; margin: 4px 0 6px; }
  .m3 td { min-width: 52px; padding: 0 5px; }
  .tabs button { font-size: 11px; }
}
""",
    "body": BODY,
    "script": SCRIPT,
}
