"""图3-11 两次旋转变换（《机器人技术基础（第三版）》例3.4，3.2.1 节三、算子左/右乘规则）。

教材依据：
- 例3.4：已知坐标系中点 U 的位置矢量 U = [7, 3, 2, 1]ᵀ，将此点绕 Z 轴旋转 90°，再绕 Y 轴旋转 90°，
  求旋转变换后所得的点 W。
- 教材解（原文）：W = Rot(Y, 90°)·Rot(Z, 90°)·U。两次旋转都相对固定坐标系进行，故算子左乘；
  后一次的算子写在最左边，运算顺序自右向左。
- 式(3.12) Rot(Z,θ)、式(3.14) Rot(Y,θ)（本图把该 4×4 旋转算子截取 3×3 显示）。
- 教材逐步结果：
    Rot(Z,90°) = [[0,-1,0],[1,0,0],[0,0,1]]，Rot(Z,90°)·U = [-3, 7, 2]ᵀ；
    Rot(Y,90°) = [[0,0,1],[0,1,0],[-1,0,0]]，W = [2, 7, 3]ᵀ。
  核对：z 分量 2 在第一步不变（绕 Z 转），第二步由 y 分量 7 变成新的 z 分量 —— 与教材一致。

脚本内自检（selfTest）：
1) θ₁=90°、θ₂=90°、U=[7,3,2]ᵀ 时，Rot(Z,90°)·U = (-3,7,2)，W = (2,7,3)（与教材一致）；
2) 直接按 3×3 手写矩阵与 FK.M4.rotZ / rotY 结果逐元素相等；
3) 交换次序得到的结果不同（Rot(Y)·Rot(Z) 与 Rot(Z)·Rot(Y) 在本例中不等），
   以此提示“左乘顺序不能颠倒”；
4) 任意 θ₁、θ₂ 下复合矩阵应为正交矩阵（RᵀR = I，det = +1）。
自检失败直接 throw。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

CSS = COMMON_CSS + """
.mtable {
  border-collapse: collapse;
  margin: 2px 0 2px 9px;
  border-left: 1.6px solid #8fa2bd;
  border-right: 1.6px solid #8fa2bd;
  border-radius: 3px;
}
.mtable td {
  padding: 0 5px;
  font: 13px/1.42 ui-monospace, SFMono-Regular, Consolas, monospace;
  text-align: right;
  color: #33415a;
}
.mtable td.pos { color: #174ea6; font-weight: 700; }
.mtlabel { color: #5b6a80; font-size: 12.5px; margin-right: 4px; }
/* 桌面端三张矩阵并排，压住读数的宽度，给图形留出空间 */
.mrow-group { display: flex; flex-wrap: wrap; gap: 4px 18px; align-items: flex-start; }
.mat-note { display: none; }
@media (max-width: 1100px) {
  .mrow-group { display: block; }
}
/* 手机竖屏可用高度有限：三张 4×4 矩阵改为一行矩阵摘要，交互控件保持完整可用 */
@media (max-width: 720px) {
  .mtable { margin: 2px 0 2px 0; }
  .mtable td { padding: 0 3px; font-size: 11.5px; }
  .readout { font-size: 12.5px; max-width: calc(100% - 16px); }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 11px; }
  .panel .control { margin-top: 7px; }
  .panel .subtitle { display: none; }
  .panel .legend { display: none; }
  [data-mobile-hide] { display: none !important; }
  .mat-note { display: block; }
  .hint { display: none; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="点U先绕Z轴转90度再绕Y轴转90度得到点W的交互示意图">
  <defs>
    <marker id="arrowX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="arrowY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="arrowZ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="arrowU" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="arrowM" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
    <marker id="arrowW" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="axesLayer"></g>
  <g id="arcLayer"></g>
  <g id="vecLayer"></g>
</svg>

<section class="panel" aria-label="图3-11 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3-11 两次旋转变换</h1>
      <p class="subtitle">U 先绕 Z 轴转 θ₁，再绕 Y 轴转 θ₂ 得 W。两次都相对固定坐标系，故算子左乘：
        W = Rot(Y,θ₂)·Rot(Z,θ₁)·U（自右向左运算）。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="t1">第一步：绕 Z 轴角 θ₁</label><output id="t1Value">90.0°</output></div>
    <input id="t1" type="range" min="-180" max="180" step="1" value="90">
  </div>
  <div class="control">
    <div class="control-head"><label for="t2">第二步：绕 Y 轴角 θ₂</label><output id="t2Value">90.0°</output></div>
    <input id="t2" type="range" min="-180" max="180" step="1" value="90">
  </div>
  <div class="control">
    <div class="control-head"><label for="ux">U 的 X 分量</label><output id="uxValue">7.0</output></div>
    <input id="ux" type="range" min="-8" max="8" step="0.5" value="7">
  </div>
  <div class="control">
    <div class="control-head"><label for="uy">U 的 Y 分量</label><output id="uyValue">3.0</output></div>
    <input id="uy" type="range" min="-8" max="8" step="0.5" value="3">
  </div>
  <div class="control">
    <div class="control-head"><label for="uz">U 的 Z 分量</label><output id="uzValue">2.0</output></div>
    <input id="uz" type="range" min="-8" max="8" step="0.5" value="2">
  </div>

  <div class="options">
    <label><input id="step1" type="checkbox">只看第 1 次旋转（Rot(Z,θ₁)·U）</label>
    <label><input id="step2" type="checkbox" checked>标出第 2 次旋转角 θ<sub>2</sub></label>
    <label><input id="showComp" type="checkbox" checked>分量虚线（U 与 W）</label>
    <label><input id="showOnly" type="checkbox">隐藏中间点 R<sub>Z</sub>·U</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i class="dot" style="background:#c26a10"></i>U（原始矢量）</span>
    <span><i class="dot" style="background:#0e7490"></i>Rot(Z,θ₁)·U（中间结果）</span>
    <span><i class="dot" style="background:#7c3aed"></i>W（最终结果）</span>
    <span><i style="background:#7c3aed"></i>旋转轨迹弧</span>
  </div>
</section>

<div class="hint">拖动旋转视角 · 滚轮缩放 · 双击复位</div>

<div class="readout" id="readout">
  <div class="row"><strong>U</strong> = [ <span id="uOut">7.000</span>, <span id="vOut">3.000</span>, <span id="wOut">2.000</span> ]<sup>T</sup>
    <span class="small">（教材原始坐标）</span></div>
  <div class="row"><strong>Rot(Z,θ₁)·U</strong> = [ <span id="mOut">-3.000</span>, <span id="nOut">7.000</span>, <span id="oOut">2.000</span> ]<sup>T</sup></div>
  <div class="row"><strong>W</strong> = [ <span id="xOut">2.000</span>, <span id="yOut">7.000</span>, <span id="zOut">3.000</span> ]<sup>T</sup>
    <span class="small">（= Rot(Y,θ₂)·Rot(Z,θ₁)·U）</span></div>
  <div class="row" id="matrixRows" data-mobile-hide><div class="mrow-group"></div></div>
  <div class="row mat-note"><span class="small">手机端只显示矢量读数；三张 4×4 矩阵在桌面/平板视口显示。</span></div>
</div>
"""

SCRIPT = r"""
(function () {
  "use strict";

  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var axesLayer = document.getElementById("axesLayer");
  var arcLayer = document.getElementById("arcLayer");
  var vecLayer = document.getElementById("vecLayer");

    var scene = new FK.Scene({
    svg: viewport,
    origin: { x: 340, y: 430 },
    scale: 40,
    yaw: -0.68,
    pitch: 0.45,
    minScale: 20,
    maxScale: 120
  });

  var DEFAULTS = { t1: 90, t2: 90, ux: 7, uy: 3, uz: 2 };
  var state = {
    t1: DEFAULTS.t1, t2: DEFAULTS.t2, ux: DEFAULTS.ux, uy: DEFAULTS.uy, uz: DEFAULTS.uz,
    step1: false, step2: true, showComp: true, showOnly: false, auto: false
  };

  var C = {
    U: "#c26a10", M: "#0e7490", W: "#7c3aed",
    comp: "#c3cede", radius: "#a8b7ca", edge: "#94a3b8"
  };

  function applyLayout() {
    var narrow = viewport.clientWidth <= 720 && viewport.clientWidth > 0;
    scene.baseOrigin.x = narrow ? 430 : 340;
    scene.baseOrigin.y = narrow ? 320 : 430;
  }

  function applyInitialZoom() {
    var narrow = viewport.clientWidth <= 720 && viewport.clientWidth > 0;
    var target = narrow ? 30 : 40;
    scene.state.scale = target;
    scene.defaults.scale = target;
  }

  function mnum(v, digits) {
    return FK.format(v, digits === undefined ? 3 : digits).replace("-", "\u2212");
  }

  function vecStr(v) {
    return "[ " + mnum(v[0], 3) + ", " + mnum(v[1], 3) + ", " + mnum(v[2], 3) + " ]";
  }

  /* --------------------------------------------------------------- 绘制辅助 */

  function seg(a, b, attrs, layer) {
    var p = scene.project(a), q = scene.project(b);
    return scene.el("line", Object.assign({
      x1: p.x, y1: p.y, x2: q.x, y2: q.y
    }, attrs), layer);
  }

  function tag(v, text, attrs, dx, dy, layer) {
    var p = scene.project(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0), "font-size": 16
    }, attrs), layer);
    node.textContent = text;
    return node;
  }

  /** 画一条从原点出发的矢量（带彩色箭头与圆点），返回屏幕上端点坐标 */
  function drawVector(v, color, marker, name, cfg) {
    var c = cfg || {};
    if (c.dim) {
      seg([0, 0, 0], v, { stroke: color, "stroke-width": 2, "stroke-dasharray": "6 6", opacity: 0.55 }, vecLayer);
      return scene.project(v);
    }
    seg([0, 0, 0], v, { stroke: color, "stroke-width": 4.2, "marker-end": "url(#" + marker + ")" }, vecLayer);
    var p = scene.project(v);
    scene.el("circle", { cx: p.x, cy: p.y, r: 6.4, fill: color, class: "fk-point" }, vecLayer);
    var t = scene.el("text", {
      x: p.x + (c.dx === undefined ? 12 : c.dx),
      y: p.y + (c.dy === undefined ? -12 : c.dy),
      fill: c.textColor || color, "font-size": 18, class: "fk-point-label"
    }, vecLayer);
    t.textContent = name;
    if (c.value) {
      var t2 = scene.el("text", {
        x: p.x + (c.dx === undefined ? 12 : c.dx),
        y: p.y + (c.dy === undefined ? -12 : c.dy) + 20,
        fill: c.textColor || color, "font-size": 13, class: "fk-point-label"
      }, vecLayer);
      t2.textContent = c.value;
    }
    return p;
  }

  function drawComponents(v, color) {
    seg([0, 0, 0], [v[0], 0, 0], { stroke: color, "stroke-width": 1.6, "stroke-dasharray": "5 5" }, vecLayer);
    seg([v[0], 0, 0], [v[0], v[1], 0], { stroke: color, "stroke-width": 1.6, "stroke-dasharray": "5 5" }, vecLayer);
    seg([v[0], v[1], 0], v, { stroke: color, "stroke-width": 1.6, "stroke-dasharray": "5 5" }, vecLayer);
    seg(v, [v[0], v[1], 0], { stroke: color, "stroke-width": 1.6, "stroke-dasharray": "5 5" }, vecLayer);
    seg([0, 0, 0], [v[0], v[1], 0], { stroke: color, "stroke-width": 1.3, "stroke-dasharray": "3 5" }, vecLayer);
  }

  function drawAxes() {
    var axes = [
      { dir: [7.6, 0, 0], color: "#d93025", marker: "arrowX", name: "X", dx: 9, dy: -6 },
      { dir: [0, 7.6, 0], color: "#2563eb", marker: "arrowY", name: "Y", dx: 9, dy: -6 },
      { dir: [0, 0, 7.6], color: "#12944f", marker: "arrowZ", name: "Z", dx: 9, dy: -6 }
    ];
    for (var i = 0; i < axes.length; i += 1) {
      var a = axes[i];
      seg([0, 0, 0], a.dir, {
        stroke: a.color, "stroke-width": 3, "marker-end": "url(#" + a.marker + ")"
      }, axesLayer);
      tag(a.dir, a.name, { fill: a.color, "font-style": "italic", "font-size": 17 }, a.dx, a.dy, axesLayer);
    }
    var o = scene.project([0, 0, 0]);
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.4, fill: "#334155" }, axesLayer);
    var origin = scene.el("text", { x: o.x - 26, y: o.y + 20, "font-size": 15, class: "fk-origin-label" }, axesLayer);
    origin.textContent = "O";
  }

  /** 画一段圆弧（点绕某轴旋转的轨迹），axisSpec 给出轴与半径 */
  function drawArcFromTo(center, axis, from, to, steps, color, width) {
    var r = FK.Vec.sub(from, center);
    var k = FK.Vec.normalize(axis);
    var arcPts = [];
    var total = angleBetween(from, to, center, k);
    for (var i = 0; i <= steps; i += 1) {
      var t = total * (i / steps);
      arcPts.push(FK.Vec.add(center, rotateAbout(r, k, t)));
    }
    scene.polyline(arcPts, { stroke: color, "stroke-width": width || 2.6, "stroke-dasharray": "7 6" }, arcLayer);
    return arcPts;
  }

  function rotateAbout(v, k, t) {
    var c = Math.cos(t), s = Math.sin(t);
    var kv = FK.Vec.cross(k, v);
    var d = FK.Vec.dot(k, v);
    return [
      v[0] * c + kv[0] * s + k[0] * d * (1 - c),
      v[1] * c + kv[1] * s + k[1] * d * (1 - c),
      v[2] * c + kv[2] * s + k[2] * d * (1 - c)
    ];
  }

  function angleBetween(from, to, center, k) {
    var a = FK.Vec.normalize(FK.Vec.sub(from, center));
    var b = FK.Vec.normalize(FK.Vec.sub(to, center));
    var cosT = Math.max(-1, Math.min(1, FK.Vec.dot(a, b)));
    var ang = Math.acos(cosT);
    // 用 k 判断旋向（右手法则）
    var sign = FK.Vec.dot(FK.Vec.cross(a, b), k) >= 0 ? 1 : -1;
    return ang * sign;
  }

  /** 取圆弧的中间方向并外推，用于摆放 θ 角标 */
  function blend(from, to, t, push) {
    var dir = FK.Vec.normalize(FK.Vec.add(
      FK.Vec.scale(FK.Vec.normalize(from), 1 - t),
      FK.Vec.scale(FK.Vec.normalize(to), t)
    ));
    var radius = (FK.Vec.len(from) * (1 - t) + FK.Vec.len(to) * t) * push;
    return FK.Vec.scale(dir, radius);
  }

  /* ------------------------------------------------------------------ 矩阵表 */

  function buildMatrixTable(id, label, color) {
    var rows = "";
    for (var r = 0; r < 4; r += 1) {
      rows += "<tr>";
      for (var c = 0; c < 4; c += 1) {
        rows += '<td class="pos" id="' + id + "-" + r + "-" + c + '">0.000</td>';
      }
      rows += "</tr>";
    }
    return '<div class="mrow"><div class="mtlabel" style="color:' + color + '">' + label +
      '</div><table class="mtable" aria-label="' + label + '">' + rows + "</table></div>";
  }

  function fillMatrix(id, m) {
    for (var r = 0; r < 4; r += 1) {
      for (var c = 0; c < 4; c += 1) {
        var node = document.getElementById(id + "-" + r + "-" + c);
        if (node) node.textContent = mnum(m[r * 4 + c], 3);
      }
    }
  }

  /* ------------------------------------------------------------------ 渲染 */

  function render() {
    applyLayout();
    gridLayer.replaceChildren();
    axesLayer.replaceChildren();
    arcLayer.replaceChildren();
    vecLayer.replaceChildren();

    var gridGroup = scene.el("g", { class: "fk-grid" }, gridLayer);
    for (var gi = -2; gi <= 8; gi += 2) {
      scene.line([-2, gi, 0], [8, gi, 0], { class: "fk-grid-line" }, gridGroup);
      scene.line([gi, -2, 0], [gi, 8, 0], { class: "fk-grid-line" }, gridGroup);
    }

    drawAxes();

    var t1 = state.t1 * FK.DEG;
    var t2 = state.t2 * FK.DEG;
    var U = [state.ux, state.uy, state.uz];
    var Rz = FK.M4.rotZ(t1);
    var Ry = FK.M4.rotY(t2);
    var Mid = FK.M4.apply(Rz, U);
    var W = FK.M4.apply(Ry, Mid);
    var RyRz = FK.M4.multiply(Ry, Rz);

    // 滚动轨迹：第 1 步绕 Z 轴、第 2 步绕 Y 轴
    var showMid = !state.showOnly;
    var firstOnly = state.step1;

    if (state.showComp && !firstOnly) {
      drawComponents(U, C.comp);
      drawComponents(W, C.comp);
    }

    // 第 1 步轨迹（绕 Z 轴）
    drawArcFromTo([0, 0, 0], [0, 0, 1], U, Mid, 64, "rgba(194,106,16,0.85)", 2.4);
    // 第 2 步轨迹（绕 Y 轴）：默认显示，便于看到“第二步”的绕行关系
    if (!firstOnly) {
      drawArcFromTo([0, 0, 0], [0, 1, 0], Mid, W, 64, "rgba(14,116,144,0.9)", 2.4);
    }
    if (firstOnly) {
      // 只看第 1 次旋转：突出 U 与 Rot(Z,θ₁)·U
      var pU1 = scene.project(U);
      drawVector(U, C.U, "arrowU", "U", { value: vecStr(U) + "\u1d40", dx: pU1.x > 520 ? -215 : 16, dy: -14 });
      drawVector(Mid, C.M, "arrowM", "Rot(Z,\u03b8\u2081)\u00b7U",
        { value: vecStr(Mid) + "\u1d40", dx: 14, dy: -14 });
    } else {
      // U 的箭头指向画面右侧、靠近读数框；标签自动放到箭头左侧，避免被读数框遮住
      var pU = scene.project(U);
      var uDx = pU.x > 520 ? -215 : 16;
      drawVector(U, C.U, "arrowU", "U", { value: vecStr(U) + "\u1d40", dx: uDx, dy: -12 });
      drawVector(Mid, C.M, "arrowM", "Rot(Z,\u03b8\u2081)\u00b7U",
        { value: vecStr(Mid) + "\u1d40", dx: 14, dy: 22, dim: !showMid });
      drawVector(W, C.W, "arrowW", "W", { value: vecStr(W) + "\u1d40", dx: 14, dy: -14 });
    }

    // 两步旋转的角度标注
    if (!firstOnly) {
      if (state.t1 !== 0) {
        var p1 = scene.project(blend(U, Mid, 0.62, 1.14));
        var a1 = scene.el("text", {
          x: p1.x, y: p1.y, fill: "#a35a0d", "font-size": 17, class: "fk-axis-label"
        }, arcLayer);
        a1.textContent = "\u03b8\u2081 = " + FK.format(state.t1, 0) + "\u00b0";
      }
      if (state.step2) {
        var p2 = scene.project(blend(Mid, W, 0.62, 1.14));
        var a2 = scene.el("text", {
          x: p2.x, y: p2.y, fill: "#0e7490", "font-size": 17, class: "fk-axis-label"
        }, arcLayer);
        a2.textContent = "\u03b8\u2082 = " + FK.format(state.t2, 0) + "\u00b0";
      }
    }

    // ---------------------------------------------------------------- 读数
    function put(id, value, digits) {
      var node = document.getElementById(id);
      if (node) node.textContent = mnum(value, digits === undefined ? 3 : digits);
    }
    put("uOut", U[0]); put("vOut", U[1]); put("wOut", U[2]);
    put("mOut", Mid[0]); put("nOut", Mid[1]); put("oOut", Mid[2]);
    put("xOut", W[0]); put("yOut", W[1]); put("zOut", W[2]);

    var rowsHost = document.getElementById("matrixRows");
    var html = buildMatrixTable("rz", "Rot(Z,\u03b8\u2081) =", "#a35a0d") +
      buildMatrixTable("ry", "Rot(Y,\u03b8\u2082) =", "#0e7490") +
      buildMatrixTable("rt", "Rot(Y,\u03b8\u2082)\u00b7Rot(Z,\u03b8\u2081) =", "#5b21b6");
    rowsHost.innerHTML = '<div class="mrow-group">' + html + "</div>";
    fillMatrix("rz", Rz);
    fillMatrix("ry", Ry);
    fillMatrix("rt", RyRz);
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "t1", key: "t1", value: DEFAULTS.t1, format: function (v) { return FK.deg(v, 1); } },
    { id: "t2", key: "t2", value: DEFAULTS.t2, format: function (v) { return FK.deg(v, 1); } },
    { id: "ux", key: "ux", value: DEFAULTS.ux, format: function (v) { return FK.format(v, 1); } },
    { id: "uy", key: "uy", value: DEFAULTS.uy, format: function (v) { return FK.format(v, 1); } },
    { id: "uz", key: "uz", value: DEFAULTS.uz, format: function (v) { return FK.format(v, 1); } }
  ], state, render);

  FK.bindToggles([
    { id: "step1", key: "step1" },
    { id: "step2", key: "step2" },
    { id: "showComp", key: "showComp" },
    { id: "showOnly", key: "showOnly" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.t1 = DEFAULTS.t1;
    state.t2 = DEFAULTS.t2;
    state.ux = DEFAULTS.ux;
    state.uy = DEFAULTS.uy;
    state.uz = DEFAULTS.uz;
    state.step1 = false;
    state.step2 = true;
    state.showComp = true;
    state.showOnly = false;
    state.auto = false;
    ["step1", "showOnly", "auto"].forEach(function (id) {
      var node = document.getElementById(id);
      if (node) node.checked = false;
    });
    document.getElementById("step2").checked = true;
    document.getElementById("showComp").checked = true;
    scene.setAuto(false);
    ranges.refresh();
    applyInitialZoom();
    scene.reset();
    render();
  });

  window.addEventListener("resize", function () { render(); });
  applyInitialZoom();

  /* ------------------------------------------------------------------ 自检 */
  (function selfTest() {
    var SQ2 = Math.SQRT2;
    // 1) 教材例3.4：θ₁=θ₂=90°，U=[7,3,2]ᵀ → Rot(Z,90°)·U=(-3,7,2)，W=(2,7,3)
    var Rz90 = FK.M4.rotZ(90 * FK.DEG);
    var Ry90 = FK.M4.rotY(90 * FK.DEG);
    var mid = FK.M4.apply(Rz90, [7, 3, 2]);
    if (!FK.Vec.eq(FK.Vec.round(mid, 9), [-3, 7, 2], 1e-9)) {
      throw new Error("图3-11 自检失败：Rot(Z,90°)·U 应为 (-3,7,2)，实际 " + JSON.stringify(mid));
    }
    var w = FK.M4.apply(Ry90, mid);
    if (!FK.Vec.eq(FK.Vec.round(w, 9), [2, 7, 3], 1e-9)) {
      throw new Error("图3-11 自检失败：W 应为 (2,7,3)，实际 " + JSON.stringify(w));
    }
    // 2) 与教材手写 3x3 矩阵逐元素一致（教材式(3.12)/(3.14) 的 3x3 部分）
    var expectRz = [0, -1, 0, 1, 0, 0, 0, 0, 1];
    var expectRy = [0, 0, 1, 0, 1, 0, -1, 0, 0];
    var gotRz = FK.M4.rotation(Rz90);
    var gotRy = FK.M4.rotation(Ry90);
    for (var i = 0; i < 9; i += 1) {
      if (Math.abs(gotRz[i] - expectRz[i]) > 1e-12) throw new Error("图3-11 自检失败：Rot(Z,90°) 第 " + i + " 项不符");
      if (Math.abs(gotRy[i] - expectRy[i]) > 1e-12) throw new Error("图3-11 自检失败：Rot(Y,90°) 第 " + i + " 项不符");
    }
    // 3) 复合顺序不可交换：Rot(Z,90°)·Rot(Y,90°)·U = (-3,2,-7) ≠ Rot(Y,90°)·Rot(Z,90°)·U = (2,7,3)
    var swapped = FK.M4.apply(FK.M4.rotZ(90 * FK.DEG), FK.M4.apply(FK.M4.rotY(90 * FK.DEG), [7, 3, 2]));
    if (!FK.Vec.eq(FK.Vec.round(swapped, 9), [-3, 2, -7], 1e-9)) {
      throw new Error("图3-11 自检失败：交换次序的结果应为 (-3,2,-7)，实际 " + JSON.stringify(swapped));
    }
    if (FK.Vec.eq(FK.Vec.round(swapped, 9), FK.Vec.round(w, 9), 1e-9)) {
      throw new Error("图3-11 自检失败：交换次序后结果不应相同");
    }
    // 4) 45° 参照点：Rot(Z,45°)·[1,0,0] = (√2/2, √2/2, 0)
    var h = FK.M4.apply(FK.M4.rotZ(45 * FK.DEG), [1, 0, 0]);
    if (!FK.Vec.eq(FK.Vec.round(h, 9), [SQ2 / 2, SQ2 / 2, 0], 1e-9)) {
      throw new Error("图3-11 自检失败：Rot(Z,45°)·[1,0,0] 应为 (√2/2,√2/2,0)");
    }
    // 5) 任意角度的复合矩阵都应正交且 det=+1
    var samples = [-180, -90, -33, 0, 21, 90, 137, 180];
    for (var a = 0; a < samples.length; a += 1) {
      for (var b = 0; b < samples.length; b += 1) {
        var R = FK.M4.rotation(FK.M4.multiply(FK.M4.rotY(samples[b] * FK.DEG), FK.M4.rotZ(samples[a] * FK.DEG)));
        var RtR = [
          R[0] * R[0] + R[3] * R[3] + R[6] * R[6],
          R[0] * R[1] + R[3] * R[4] + R[6] * R[7],
          R[0] * R[2] + R[3] * R[5] + R[6] * R[8],
          R[1] * R[1] + R[4] * R[4] + R[7] * R[7],
          R[1] * R[2] + R[4] * R[5] + R[7] * R[8],
          R[2] * R[2] + R[5] * R[5] + R[8] * R[8]
        ];
        var expect = [1, 0, 0, 1, 0, 1];
        for (var k = 0; k < 6; k += 1) {
          if (Math.abs(RtR[k] - expect[k]) > 1e-12) {
            throw new Error("图3-11 自检失败：复合矩阵不正交（θ₁=" + samples[a] + ", θ₂=" + samples[b] + "）");
          }
        }
        var det = R[0] * (R[4] * R[8] - R[5] * R[7]) - R[1] * (R[3] * R[8] - R[5] * R[6]) +
          R[2] * (R[3] * R[7] - R[4] * R[6]);
        if (Math.abs(det - 1) > 1e-12) {
          throw new Error("图3-11 自检失败：复合矩阵 det ≠ 1");
        }
      }
    }
  }());

  render();
}());
"""

FIGURE = {
    "id": "figure-3-11",
    "title": "图3-11 两次旋转变换（例3.4：U 先绕Z转90°再绕Y转90°得W） · 人机交互演示",
    "css": CSS,
    "body": BODY,
    "script": SCRIPT,
}
