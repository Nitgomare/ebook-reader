"""图3-9 点的旋转变换（《机器人技术基础（第三版）》3.2.1 节一、图3.9）。

教材依据：
- 正文图3.9 与坐标关系式：X_A' = X_A cosθ − Y_A sinθ，Y_A' = X_A sinθ + Y_A cosθ，Z_A' = Z_A。
- 式(3.9)（旋转矩阵形式）：
      [X_A']   [ cosθ  −sinθ  0 ] [X_A]
      [Y_A'] = [ sinθ   cosθ  0 ] [Y_A]
      [Z_A']   [   0      0   1 ] [Z_A]
- 式(3.10) 为同一变换的齐次形式；式(3.12) 把该 3×3 矩阵记作旋转算子 Rot(Z,θ)。
  θ 的正负按右手法则确定（右手拇指指向 +Z，四指绕向为 θ>0 的方向）。
- 关键结论：绕 Z 轴旋转不改变点的 z 坐标，即 Z_A' = Z_A（本图用虚线 + 读数强调这一点）。

脚本内自检（selfTest）：
1) θ=90°、A=(1.5, 0.8, 1.2) → A'=(−0.8, 1.5, 1.2)，与式(3.9) 的 cos/sin 展开逐项一致；
2) 对多组 θ∈{−180°,−135°,…,180°} 与 A 逐个验证 Z_A' = Z_A（容差 1e-12）；
3) 旋转不改变点到 z 轴的距离，且 θ=+90° 时 A' 与 Rot(Z,θ) 作用结果完全相同。
自检失败直接 throw。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

CSS = COMMON_CSS + """
/* 矩阵用 monospace 表格排版，避免等宽字体缺失导致的错位 */
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
.break { display: inline; }
/* 移动端：读数字号略降、矩阵列距收紧、矩阵另起一行避免横向溢出 */
@media (max-width: 720px) {
  .mtable { margin: 2px 0 2px 0; }
  .mtable td { padding: 0 3px; font-size: 11.5px; }
  .readout { font-size: 12.5px; max-width: calc(100% - 16px); }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 11px; }
  .break { display: block; }
  .panel .control { margin-top: 7px; }
  .panel .subtitle { display: none; }
  .panel .legend { margin-top: 7px; padding-top: 7px; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="点A绕Z轴旋转θ角到A撇的交互示意图，A与A撇的z坐标相同">
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
    <marker id="arrowV" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="arrowW" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="axesLayer"></g>
  <g id="arcLayer"></g>
  <g id="pointLayer"></g>
</svg>

<section class="panel" aria-label="图3-9 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3-9 点的旋转变换</h1>
      <p class="subtitle">固定坐标系 {A}；点 A 绕 Z 轴转过 θ 到 A′。转动轴的箭头按右手法则标正向，θ&gt;0 为逆时针（从 +Z 向原点看）。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="theta">旋转角 θ</label><output id="thetaValue">90.0°</output></div>
    <input id="theta" type="range" min="-180" max="180" step="1" value="90">
  </div>
  <div class="control">
    <div class="control-head"><label for="ax">点 A 的 X<sub>A</sub></label><output id="axValue">2.600</output></div>
    <input id="ax" type="range" min="-3" max="3" step="0.1" value="2.6">
  </div>
  <div class="control">
    <div class="control-head"><label for="ay">点 A 的 Y<sub>A</sub></label><output id="ayValue">1.500</output></div>
    <input id="ay" type="range" min="-3" max="3" step="0.1" value="1.5">
  </div>
  <div class="control">
    <div class="control-head"><label for="az">点 A 的 Z<sub>A</sub></label><output id="azValue">1.200</output></div>
    <input id="az" type="range" min="-2.6" max="2.6" step="0.1" value="1.2">
  </div>

  <div class="options">
    <label><input id="showRadii" type="checkbox" checked>半径 OA / OA′</label>
    <label><input id="showHeight" type="checkbox" checked>Z<sub>A</sub>=Z<sub>A′</sub> 高度线</label>
    <label><input id="showArc" type="checkbox" checked>旋转圆弧</label>
    <label><input id="showAxis" type="checkbox" checked>转动轴 +Z</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i class="dot" style="background:#c26a10"></i>点 A（旋转前）</span>
    <span><i class="dot" style="background:#7c3aed"></i>点 A′（旋转后）</span>
    <span><i style="background:#7c3aed"></i>A→A′ 圆弧轨迹</span>
    <span><i style="background:#94a3b8"></i>高度虚线</span>
  </div>
</section>

<div class="hint">拖动旋转视角 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row"><strong>A</strong>&nbsp;= [ <span id="axOut">2.600</span>, <span id="ayOut">1.500</span>, <span id="azOut">1.200</span> ]<sup>T</sup>
    <span class="small">（X<sub>A</sub>, Y<sub>A</sub>, Z<sub>A</sub>）</span></div>
  <div class="row"><strong>A′</strong> = [ <span id="bxOut">-1.500</span>, <span id="byOut">2.600</span>, <span id="bzOut">1.200</span> ]<sup>T</sup>
    <span class="small">（X<sub>A′</sub>, Y<sub>A′</sub>, Z<sub>A′</sub>）</span></div>
  <div class="row"><strong>θ</strong> = <span id="thetaOut">90.0°</span>
    <span class="small">　θ 正负按右手法则</span></div>
  <div class="row" style="margin-top:4px"><span class="small">式(3.9) 的旋转矩阵：</span></div>
  <div class="row"><table class="mtable" aria-label="绕Z轴的3乘3旋转矩阵">
      <tr><td class="pos" id="r11">0.000</td><td class="pos" id="r12">−1.000</td><td class="pos" id="r13">0.000</td></tr>
      <tr><td class="pos" id="r21">1.000</td><td class="pos" id="r22">0.000</td><td class="pos" id="r23">0.000</td></tr>
      <tr><td class="pos" id="r31">0.000</td><td class="pos" id="r32">0.000</td><td class="pos" id="r33">1.000</td></tr>
    </table><span class="break"></span>
    <span class="small" style="margin-left:8px">第3行 = [0, 0, 1] ⇒ <strong id="zKeep">Z<sub>A′</sub> = Z<sub>A</sub> = 1.200</strong></span></div>
</div>
"""

SCRIPT = r"""
(function () {
  "use strict";

  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var axesLayer = document.getElementById("axesLayer");
  var arcLayer = document.getElementById("arcLayer");
  var pointLayer = document.getElementById("pointLayer");

  var scene = new FK.Scene({
    svg: viewport,
    origin: { x: 470, y: 404 },
    scale: 62,
    yaw: -0.66,
    pitch: 0.44,
    minScale: 30,
    maxScale: 170
  });

  var DEFAULTS = { theta: 90, ax: 2.6, ay: 1.5, az: 1.2 };
  var state = {
    theta: DEFAULTS.theta, ax: DEFAULTS.ax, ay: DEFAULTS.ay, az: DEFAULTS.az,
    showRadii: true, showHeight: true, showArc: true, showAxis: true, auto: false
  };

  var COLORS = {
    A: "#c26a10", Ap: "#7c3aed", arc: "#7c3aed",
    height: "#94a3b8", radius: "#93a6bf", axisZ: "#12944f"
  };

  /** 窄屏时把投影中心上移并适度缩小，避免底部控制面板盖住图形 */
  function applyLayout() {
    var narrow = viewport.clientWidth <= 720 && viewport.clientWidth > 0;
    // 只调整投影中心，缩放交给用户滚轮（scene.setAutoZoom 由场景自己维护）
    scene.baseOrigin.x = narrow ? 500 : 470;
    scene.baseOrigin.y = narrow ? 330 : 404;
  }

  /** 按当前视口宽度给一个合适的初始缩放；用户缩放之后不再覆盖 */
  function applyInitialZoom() {
    var narrow = viewport.clientWidth <= 720 && viewport.clientWidth > 0;
    var target = narrow ? 54 : 62;
    scene.state.scale = target;
    scene.defaults.scale = target;
  }

  /** 读数的负号用 U+2212，避免与短横混淆 */
  function mnum(v, digits) {
    return FK.format(v, digits === undefined ? 3 : digits).replace("-", "\u2212");
  }

  /* --------------------------------------------------------------- 绘制辅助 */

  function seg(a, b, attrs, layer) {
    var p = scene.project(a), q = scene.project(b);
    return scene.el("line", Object.assign({
      x1: p.x, y1: p.y, x2: q.x, y2: q.y
    }, attrs), layer);
  }

  function label(v, text, attrs, dx, dy, layer) {
    var p = scene.project(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0), "font-size": 16
    }, attrs), layer);
    node.textContent = text;
    return node;
  }

  function drawAxes() {
    var axes = [
      { dir: [2.75, 0, 0], color: "#d93025", marker: "arrowX", name: "X\u0302\u2090", dx: 8, dy: -6 },
      { dir: [0, 2.75, 0], color: "#2563eb", marker: "arrowY", name: "Y\u0302\u2090", dx: 8, dy: -6 },
      { dir: [0, 0, 2.75], color: "#12944f", marker: "arrowZ", name: "Z\u0302\u2090", dx: 8, dy: -6 }
    ];
    for (var i = 0; i < axes.length; i += 1) {
      var a = axes[i];
      seg([0, 0, 0], a.dir, {
        stroke: a.color, "stroke-width": 3.2, "marker-end": "url(#" + a.marker + ")"
      }, axesLayer);
      label(a.dir, a.name, { fill: a.color, "font-style": "italic" }, a.dx, a.dy, axesLayer);
    }
    var o = scene.project([0, 0, 0]);
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.4, fill: "#334155" }, axesLayer);
    var origin = scene.el("text", {
      x: o.x - 24, y: o.y + 20, "font-size": 15, class: "fk-origin-label"
    }, axesLayer);
    origin.textContent = "O";
  }

  /** 在高度 z 的平面上画一段圆弧（绕 Z 轴） */
  function drawArc(radius, startDeg, endDeg, z, color) {
    var steps = 90;
    var points = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = (startDeg + (endDeg - startDeg) * (i / steps)) * FK.DEG;
      points.push([radius * Math.cos(t), radius * Math.sin(t), z]);
    }
    scene.polyline(points, { stroke: color, class: "fk-arc", "stroke-width": 3 }, arcLayer);
  }

  /* ------------------------------------------------------------------ 渲染 */

  function render() {
    applyLayout();
    gridLayer.replaceChildren();
    axesLayer.replaceChildren();
    arcLayer.replaceChildren();
    pointLayer.replaceChildren();

    // 地面网格限制在 ±3，避免投影后铺满画面
    var gridGroup = scene.el("g", { class: "fk-grid" }, gridLayer);
    for (var gi = -3; gi <= 3; gi += 1) {
      scene.line([-3, gi, 0], [3, gi, 0], { class: "fk-grid-line" }, gridGroup);
      scene.line([gi, -3, 0], [gi, 3, 0], { class: "fk-grid-line" }, gridGroup);
    }

    drawAxes();

    var theta = state.theta;
    var rad = theta * FK.DEG;
    var A = [state.ax, state.ay, state.az];
    var M = FK.M4.rotZ(rad);
    var Ap = FK.M4.apply(M, A);
    var r = Math.sqrt(A[0] * A[0] + A[1] * A[1]);
    var phi = Math.atan2(A[1], A[0]) / FK.DEG;

    // 转动轴 +Z 的右手法则示意（自带箭头的那根 Z 轴即转动轴）
    if (state.showAxis) {
      var tip = [0, 0, 2.95];
      seg([0, 0, 0], tip, {
        stroke: COLORS.axisZ, "stroke-width": 3.6, "marker-end": "url(#arrowZ)"
      }, axesLayer);
      // 右手法则螺旋箭头：绕 Z 轴的小弧
      var rotPts = [];
      for (var i = 0; i <= 40; i += 1) {
        var t = (i / 40) * 1.7 * Math.PI;
        rotPts.push([0.55 * Math.cos(t), 0.55 * Math.sin(t), 0.42 + 0.5 * (i / 40)]);
      }
      scene.polyline(rotPts, {
        stroke: COLORS.axisZ, "stroke-width": 2, "stroke-dasharray": "5 4", "fill": "none"
      }, axesLayer);
      label([0, 0, 2.95], "转动轴 Z（右手法则）", { fill: COLORS.axisZ, "font-size": 14 }, 9, -8, axesLayer);
    }

    // 半径 OA、OA′
    if (state.showRadii) {
      seg([0, 0, 0], A, { stroke: COLORS.radius, "stroke-width": 1.6, "stroke-dasharray": "6 5" }, pointLayer);
      seg([0, 0, 0], Ap, { stroke: COLORS.radius, "stroke-width": 1.6, "stroke-dasharray": "6 5" }, pointLayer);
    }

    // Z_A = Z_A' 高度线：z=Z_A 平面上的度量矩形 + 落到 Z 轴的虚线
    if (state.showHeight) {
      seg([0, 0, A[2]], A, { stroke: COLORS.height, "stroke-width": 1.7, "stroke-dasharray": "5 5" }, pointLayer);
      seg([0, 0, A[2]], Ap, { stroke: COLORS.height, "stroke-width": 1.7, "stroke-dasharray": "5 5" }, pointLayer);
      // z 高度刻度
      seg([0, 0, 0], [0, 0, A[2]], { stroke: COLORS.height, "stroke-width": 2.4 }, pointLayer);
      label([0, 0, A[2]], "z = " + FK.format(A[2], 2), { fill: "#5b6a80", "font-size": 14 }, -96, -8, pointLayer);
      seg([A[0], 0, A[2]], [A[0], A[1], A[2]], { stroke: "#cdd9e8", "stroke-width": 1.4, "stroke-dasharray": "4 4" }, pointLayer);
      seg([0, A[1], A[2]], [A[0], A[1], A[2]], { stroke: "#cdd9e8", "stroke-width": 1.4, "stroke-dasharray": "4 4" }, pointLayer);
    }

    // 圆弧轨迹（半径取 |OA 在 xy 平面的投影|）
    var rArc = Math.max(0.85, Math.min(3.45, r));
    if (state.showArc && Math.abs(theta) > 0.05) {
      drawArc(rArc, phi, phi + theta, A[2], COLORS.arc);
      if (r > 0.05) {
        var midDeg = phi + theta * 0.5;
        var mid = midDeg * FK.DEG;
        var arcLabelPos = [rArc * Math.cos(mid) * 1.0, rArc * Math.sin(mid) * 1.0, A[2]];
        var p = scene.project(arcLabelPos);
        var sgn = theta > 0 ? "+" : "\u2212";
        var t1 = scene.el("text", {
          x: p.x + 14, y: p.y - 6, fill: COLORS.arc, "font-size": 18,
          "font-style": "italic", class: "fk-axis-label"
        }, arcLayer);
        t1.textContent = "\u03b8";
        var t2 = scene.el("text", {
          x: p.x + 14, y: p.y + 15, fill: COLORS.arc, "font-size": 14,
          class: "fk-point-label"
        }, arcLayer);
        t2.textContent = "= " + sgn + FK.format(Math.abs(theta), 0) + "\u00b0";
      }
    } else if (state.showArc && r > 0.05) {
      // θ = 0 时退化为一点，用一个小圈提示“无旋转”
      scene.dot([A[0], A[1], A[2]], { r: 7, fill: "none", stroke: COLORS.arc, "stroke-width": 2 }, arcLayer);
    }

    // 点 A / A′ 与矢量
    seg([0, 0, 0], A, { stroke: COLORS.A, "stroke-width": 4.2, "marker-end": "url(#arrowV)" }, pointLayer);
    var pa = scene.project(A);
    scene.el("circle", { cx: pa.x, cy: pa.y, r: 6.5, fill: COLORS.A, class: "fk-point" }, pointLayer);
    label(A, "A", { fill: "#8a4a08", "font-size": 19, class: "fk-point-label" }, 12, -12, pointLayer);

    seg([0, 0, 0], Ap, { stroke: COLORS.Ap, "stroke-width": 4.2, "marker-end": "url(#arrowW)" }, pointLayer);
    var pb = scene.project(Ap);
    scene.el("circle", { cx: pb.x, cy: pb.y, r: 6.5, fill: COLORS.Ap, class: "fk-point" }, pointLayer);
    label(Ap, "A\u2032", { fill: "#5b21b6", "font-size": 19, class: "fk-point-label" }, 12, -12, pointLayer);

    // ---------------------------------------------------------------- 读数
    function put(id, value, digits) {
      var node = document.getElementById(id);
      if (node) node.textContent = mnum(value, digits === undefined ? 3 : digits);
    }
    put("axOut", A[0], 3); put("ayOut", A[1], 3); put("azOut", A[2], 3);
    put("bxOut", Ap[0], 3); put("byOut", Ap[1], 3); put("bzOut", Ap[2], 3);
    var c = Math.cos(rad), s = Math.sin(rad);
    put("r11", c, 3); put("r12", -s, 3); put("r13", 0, 3);
    put("r21", s, 3); put("r22", c, 3); put("r23", 0, 3);
    put("r31", 0, 3); put("r32", 0, 3); put("r33", 1, 3);
    document.getElementById("thetaOut").textContent = FK.deg(theta, 1);
    document.getElementById("zKeep").innerHTML =
      "Z<sub>A\u2032</sub> = Z<sub>A</sub> = " + FK.format(A[2], 3);
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "theta", key: "theta", value: DEFAULTS.theta, format: function (v) { return FK.deg(v, 1); } },
    { id: "ax", key: "ax", value: DEFAULTS.ax, format: function (v) { return FK.format(v, 3); } },
    { id: "ay", key: "ay", value: DEFAULTS.ay, format: function (v) { return FK.format(v, 3); } },
    { id: "az", key: "az", value: DEFAULTS.az, format: function (v) { return FK.format(v, 3); } }
  ], state, render);

  FK.bindToggles([
    { id: "showRadii", key: "showRadii" },
    { id: "showHeight", key: "showHeight" },
    { id: "showArc", key: "showArc" },
    { id: "showAxis", key: "showAxis" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  window.addEventListener("resize", function () { render(); });
  applyInitialZoom();

  document.getElementById("reset").addEventListener("click", function () {
    state.theta = DEFAULTS.theta;
    state.ax = DEFAULTS.ax;
    state.ay = DEFAULTS.ay;
    state.az = DEFAULTS.az;
    state.showRadii = true;
    state.showHeight = true;
    state.showArc = true;
    state.showAxis = true;
    state.auto = false;
    document.getElementById("showRadii").checked = true;
    document.getElementById("showHeight").checked = true;
    document.getElementById("showArc").checked = true;
    document.getElementById("showAxis").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    render();
  });

  /* ------------------------------------------------------------------ 自检 */
  (function selfTest() {
    // 1) 式(3.9) 展开式逐项核对：θ=90°、A=(1.5, 0.8, 1.2)
    var th = 90 * FK.DEG, c = Math.cos(th), s = Math.sin(th);
    var Ax = 1.5, Ay = 0.8, Az = 1.2;
    var byFormula = [Ax * c - Ay * s, Ax * s + Ay * c, Az];
    var byMatrix = FK.M4.apply(FK.M4.rotZ(th), [Ax, Ay, Az]);
    if (!FK.Vec.eq(FK.Vec.round(byMatrix, 9), FK.Vec.round([-0.8, 1.5, 1.2], 9), 1e-9)) {
      throw new Error("图3-9 自检失败：式(3.9) 数值不符 → " + JSON.stringify(byMatrix));
    }
    if (!FK.Vec.eq(FK.Vec.round(byFormula, 12), FK.Vec.round(byMatrix, 12), 1e-12)) {
      throw new Error("图3-9 自检失败：矩阵式与 cos/sin 展开式不一致");
    }
    // 2) Z_A' ≡ Z_A（对全量程 θ 与多组 A）
    var samples = [-180, -135, -90, -45, 0, 1, 45, 90, 135, 179, 180];
    var pts = [[1.5, 0.8, 1.2], [-2.4, 0.3, -1.7], [0.7, -2.9, 0.95], [0, 0, 0]];
    for (var i = 0; i < samples.length; i += 1) {
      for (var j = 0; j < pts.length; j += 1) {
        var out = FK.M4.apply(FK.M4.rotZ(samples[i] * FK.DEG), pts[j]);
        if (Math.abs(out[2] - pts[j][2]) > 1e-12) {
          throw new Error("图3-9 自检失败：Z_A' ≠ Z_A（θ=" + samples[i] + "）");
        }
        // 旋转保长（到原点的距离不变）
        if (Math.abs(FK.Vec.len(out) - FK.Vec.len(pts[j])) > 1e-12) {
          throw new Error("图3-9 自检失败：旋转不保长（θ=" + samples[i] + "）");
        }
      }
    }
    // 3) 教材图3.9 的读法：A=(2.6,1.5,1.2)、θ=90° → A'=(-1.5,2.6,1.2)
    var got = FK.M4.apply(FK.M4.rotZ(90 * FK.DEG), [2.6, 1.5, 1.2]);
    if (!FK.Vec.eq(FK.Vec.round(got, 9), [-1.5, 2.6, 1.2], 1e-9)) {
      throw new Error("图3-9 自检失败：默认参数下 A' 应为 (-1.5, 2.6, 1.2) → " + JSON.stringify(got));
    }
    // 4) 第 3 行必须为 [0,0,1]（这正是 Z 坐标不变的原因）
    var m = FK.M4.rotation(FK.M4.rotZ(37 * FK.DEG));
    if (Math.abs(m[6]) > 1e-15 || Math.abs(m[7]) > 1e-15 || Math.abs(m[8] - 1) > 1e-15) {
      throw new Error("图3-9 自检失败：旋转矩阵第 3 行不是 [0,0,1]");
    }
  }());

  render();
}());
"""

FIGURE = {
    "id": "figure-3-9",
    "title": "图3-9 点的旋转变换（绕Z轴转θ，Z_A′=Z_A） · 人机交互演示",
    "css": CSS,
    "body": BODY,
    "script": SCRIPT,
}
