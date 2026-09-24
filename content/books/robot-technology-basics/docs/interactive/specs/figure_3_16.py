"""图3-16 转动关节连杆 D-H 坐标系建立示意图（《机器人技术基础（第三版）》3.3.1 节二、D-H 方法）。

教材依据：
- 正文图3.16 与 3.3.1(1)：连杆坐标系的 Z 轴位于转动关节轴线上；两轴线的公垂线为 X 轴，
  方向指向下一个连杆；公垂线与 Z 轴的交点为坐标系原点；Y 轴由 X、Z 按右手系确定。
- 4 个参数：连杆长度 a、连杆扭角 α、连杆距离 d、连杆夹角 θ。
  本图按标准 D-H 记法写 a_{i−1}、α_{i−1}、d_i、θ_i（教材正文 OCR 把同一组几何量写成 a_i、α_i、d_i、θ_i，
  下标约定不同、几何含义相同——见读数区的说明）。几何量：
    · 关节轴 i−1 就是 Z_{i−1} 的轴线；Z_i 的轴线就是关节轴 i（随 θ_i 绕 Z_{i−1} 摆动）；
    · a_{i−1}：两关节轴的公垂线长度，方向沿 X_i，即 Z_{i−1}×Z_i 的方向；
    · α_{i−1}：绕公垂线（X_i）把 Z_{i−1} 转到 Z_i 的转角；
    · d_i：沿 Z_{i−1} 从 O_{i−1} 量到公垂线垂足的有向距离；
    · θ_i：绕 Z_{i−1} 由 X_{i−1} 转到 X_i 的转角。
- 教材 3.3.2 的四步变换（式(3.20)）：A = Rot(Z,θ_i)·Trans(a_{i−1},0,d_i)·Rot(X,α_{i−1})。
  本图把连杆坐标系 {i} 的位姿**完全由该变换算出**，不靠肉眼摆放，
  因此 Z_i 会随 θ_i 绕 Z_{i−1} 一起转——这正是关节转动时末端轴线跟着摆的物理事实。

脚本内自检（selfTest）：见文件末尾，逐项核对公垂线长度/方向、两轴夹角、两轴公垂距离、
d 沿 Z_{i−1} 的距离、X_i 与 X_{i−1} 的夹角等于 θ_i，以及四步连乘与连杆变换逐元素一致。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

CSS = COMMON_CSS + """
.mtable {
  border-collapse: collapse;
  margin: 2px 0 2px 10px;
  border-left: 1.6px solid #8fa2bd;
  border-right: 1.6px solid #8fa2bd;
  border-radius: 3px;
}
.mtable td {
  padding: 0 5px;
  font: 12.5px/1.4 ui-monospace, SFMono-Regular, Consolas, monospace;
  text-align: right;
  color: #55637a;
}
.mtable td.theta { color: #2563eb; font-weight: 700; }
.mtable td.alpha { color: #7c3aed; font-weight: 700; }
.mtable td.len { color: #c26a10; font-weight: 700; }
.mtable td.dist { color: #0b6b3a; font-weight: 700; }
.mat-inline { display: flex; align-items: flex-start; gap: 10px; flex-wrap: wrap; }
.mat-caption { color: #5b6a80; font-size: 11.5px; line-height: 1.6; max-width: 260px; }
.mat-caption b.theta { color: #2563eb; }
.mat-caption b.alpha { color: #7c3aed; }
.mat-caption b.len { color: #c26a10; }
.mat-caption b.dist { color: #0b6b3a; }
.degen { color: #b3261e; font-size: 11.5px; margin-top: 3px; display: none; }
.degen.on { display: block; }
@media (max-width: 720px) {
  .readout { font-size: 12.5px; max-width: calc(100% - 16px); }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 11px; }
  .mtable { margin: 2px 0 2px 0; }
  .mtable td { padding: 0 3px; font: 11px/1.4 ui-monospace, SFMono-Regular, Consolas, monospace; }
  .mat-caption { font-size: 10.5px; max-width: none; }
  .mat-inline { display: block; }
  .panel .control { margin-top: 7px; }
  .panel .subtitle { display: none; }
  .panel .legend { margin-top: 7px; padding-top: 7px; }
  [data-mobile-hide] { display: none !important; }
  .hint { display: none; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="转动关节两条关节轴、公垂线、扭角、连杆距离与两个D-H坐标系的交互示意图">
  <defs>
    <marker id="arrowPrev" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#174ea6"></path>
    </marker>
    <marker id="arrowNext" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="arrowA" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="arrowD" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="arrowCross" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="arrowX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="arrowY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="jointLayer"></g>
  <g id="dimLayer"></g>
  <g id="frameLayer"></g>
</svg>

<section class="panel" aria-label="图3-16 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3-16 转动关节 D-H 坐标系</h1>
      <p class="subtitle">Z<sub>i−1</sub> 与 Z<sub>i</sub> 是两根关节轴的轴线（异面直线，公垂线唯一）。
        坐标系 {i} 的位姿由式(3.14) 的连杆变换算出，所以拨动 θ<sub>i</sub> 时 Z<sub>i</sub> 会绕
        Z<sub>i−1</sub> 一起摆。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="a">连杆长度 a<sub>i−1</sub></label><output id="aValue">1.600</output></div>
    <input id="a" type="range" min="0.5" max="2.4" step="0.05" value="1.6">
  </div>
  <div class="control">
    <div class="control-head"><label for="alpha">连杆扭角 α<sub>i−1</sub></label><output id="alphaValue">25.0°</output></div>
    <input id="alpha" type="range" min="-70" max="70" step="1" value="25">
  </div>
  <div class="control">
    <div class="control-head"><label for="d">连杆距离 d<sub>i</sub></label><output id="dValue">0.900</output></div>
    <input id="d" type="range" min="0" max="1.8" step="0.05" value="0.9">
  </div>
  <div class="control">
    <div class="control-head"><label for="theta">连杆夹角 θ<sub>i</sub>（关节变量）</label><output id="thetaValue">30.0°</output></div>
    <input id="theta" type="range" min="-180" max="180" step="1" value="30">
  </div>

  <div class="options">
    <label><input id="showPerp" type="checkbox" checked>公垂线 a<sub>i−1</sub> 与叉积箭头</label>
    <label><input id="showTwist" type="checkbox" checked>扭角弧 α<sub>i−1</sub></label>
    <label><input id="showOffset" type="checkbox" checked>偏距标注 d<sub>i</sub></label>
    <label><input id="showJoint" type="checkbox" checked>连杆夹角 θ<sub>i</sub></label>
    <label><input id="showFrames" type="checkbox" checked>坐标系的 X / Y 轴</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i style="background:#174ea6"></i>关节轴 i−1（Z<sub>i−1</sub>）</span>
    <span><i style="background:#7c3aed"></i>关节轴 i（Z<sub>i</sub>）</span>
    <span><i style="background:#c26a10"></i>公垂线 a<sub>i−1</sub></span>
    <span><i style="background:#12944f"></i>沿 Z<sub>i−1</sub> 的 d<sub>i</sub></span>
  </div>
</section>

<div class="hint">拖动旋转视角 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row">
    <strong>a<sub>i−1</sub></strong> = <span id="aOut">1.600</span>　
    <strong>α<sub>i−1</sub></strong> = <span id="alphaOut">25.0°</span>　
    <strong>d<sub>i</sub></strong> = <span id="dOut">0.900</span>　
    <strong>θ<sub>i</sub></strong> = <span id="thetaOut">30.0°</span>
  </div>
  <div class="row small" style="white-space:normal">连杆变换（教材 3.3.2 四步，式(3.20)）：<br>绕 Z 转 θ<sub>i</sub> → 沿 Z 移 d<sub>i</sub> → 沿 X 移 a<sub>i−1</sub> → 绕 X 转 α<sub>i−1</sub></div>
  <div class="row" style="white-space:normal"><div class="mat-inline">
    <table class="mtable" aria-label="连杆变换矩阵">
      <tr><td class="theta" id="t-0-0">0.866</td><td class="alpha" id="t-0-1">−0.453</td><td class="alpha" id="t-0-2">0.211</td><td class="len" id="t-0-3">1.386</td></tr>
      <tr><td class="theta" id="t-1-0">0.500</td><td class="alpha" id="t-1-1">0.785</td><td class="alpha" id="t-1-2">−0.366</td><td class="len" id="t-1-3">0.800</td></tr>
      <tr><td id="t-2-0">0.000</td><td class="alpha" id="t-2-1">0.423</td><td class="alpha" id="t-2-2">0.906</td><td class="dist" id="t-2-3">0.900</td></tr>
      <tr><td id="t-3-0">0.000</td><td id="t-3-1">0.000</td><td id="t-3-2">0.000</td><td id="t-3-3">1.000</td></tr>
    </table>
    <div class="mat-caption">
      第 1 列 = [<b class="theta">cθ<sub>i</sub></b>, <b class="theta">sθ<sub>i</sub></b>, 0]ᵀ = X<sub>i</sub>；<br>
      第 4 列 = [<b class="len">a<sub>i−1</sub>cθ<sub>i</sub></b>, <b class="len">a<sub>i−1</sub>sθ<sub>i</sub></b>, <b class="dist">d<sub>i</sub></b>]ᵀ = O<sub>i</sub>；<br>
      第 2、3 列含 <b class="alpha">α<sub>i−1</sub></b>。教材正文把同一组几何量写成 a<sub>i</sub>、α<sub>i</sub>。
    </div>
  </div></div>
  <div class="degen" id="degen">α<sub>i−1</sub> ≈ 0：两关节轴平行，公垂线多值，连杆坐标系原点不唯一（教材 3.3.1 的特殊情况）。</div>
</div>
"""

SCRIPT = r"""
(function () {
  "use strict";

  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var jointLayer = document.getElementById("jointLayer");
  var dimLayer = document.getElementById("dimLayer");
  var frameLayer = document.getElementById("frameLayer");

  var scene = new FK.Scene({
    svg: viewport,
    origin: { x: 410, y: 330 },
    scale: 76,
    yaw: -0.72,
    pitch: 0.44,
    minScale: 30,
    maxScale: 170
  });

  var DEFAULTS = { a: 1.6, alpha: 25, d: 0.9, theta: 30 };
  var state = {
    a: DEFAULTS.a, alpha: DEFAULTS.alpha, d: DEFAULTS.d, theta: DEFAULTS.theta,
    showPerp: true, showTwist: true, showOffset: true, showJoint: true,
    showFrames: true, auto: false
  };

  var C = {
    prev: "#174ea6", next: "#7c3aed",
    a: "#c26a10", d: "#0b6b3a",
    fx: "#d93025", fy: "#2563eb",
    joint: "#2b3a52", ref: "#9aa8bb"
  };

  var ZAX = [0, 0, 1];              // 世界/图纸 z 轴，约定等于 Z_{i-1}
  var XAX = [1, 0, 0];              // 约定等于 X_{i-1}

  function applyLayout() {
    var narrow = viewport.clientWidth <= 720 && viewport.clientWidth > 0;
    scene.baseOrigin.x = narrow ? 452 : 410;
    scene.baseOrigin.y = narrow ? 306 : 330;
  }

  function applyInitialZoom() {
    var narrow = viewport.clientWidth <= 720 && viewport.clientWidth > 0;
    var target = narrow ? 62 : 76;
    scene.state.scale = target;
    scene.defaults.scale = target;
  }

  function mnum(v, digits) {
    return FK.format(v, digits === undefined ? 3 : digits).replace("-", "\u2212");
  }

  /** 连杆变换：教材四步 A = Rot(Z,θ)·Trans(a,0,d)·Rot(X,α) */
  function linkTransform(a, alpha, d, theta) {
    return FK.M4.chain(
      FK.M4.rotZ(theta),
      FK.M4.translate([a, 0, d]),
      FK.M4.rotX(alpha)
    );
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
      x: p.x + (dx || 0), y: p.y + (dy || 0), "font-size": 15
    }, attrs), layer);
    node.textContent = text;
    return node;
  }

  function dotAt(v, color, r) {
    var p = scene.project(v);
    return scene.el("circle", {
      cx: p.x, cy: p.y, r: r || 5, fill: color, stroke: "#fff", "stroke-width": 1.5
    }, frameLayer);
  }

  /** 画一个坐标系的 X / Y 轴（Z 轴就是关节轴本身，不重复画） */
  function drawFrameXY(o, X, Y, cfg) {
    var len = cfg.length;
    seg(o, FK.Vec.add(o, FK.Vec.scale(X, len)), {
      stroke: C.fx, "stroke-width": cfg.width, "marker-end": "url(#arrowX)",
      "stroke-dasharray": cfg.dash || null
    }, frameLayer);
    seg(o, FK.Vec.add(o, FK.Vec.scale(Y, len)), {
      stroke: C.fy, "stroke-width": cfg.width, "marker-end": "url(#arrowY)",
      "stroke-dasharray": cfg.dash || null
    }, frameLayer);
    tag(FK.Vec.add(o, FK.Vec.scale(X, len)), cfg.xLabel,
      { fill: C.fx, "font-style": "italic", "font-size": cfg.fontSize }, 7, 16, frameLayer);
    tag(FK.Vec.add(o, FK.Vec.scale(Y, len)), cfg.yLabel,
      { fill: C.fy, "font-style": "italic", "font-size": cfg.fontSize }, 7, 16, frameLayer);
    dotAt(o, C.joint, cfg.dotR);
    tag(o, cfg.oLabel, { fill: C.joint, "font-size": 14 }, cfg.ox, cfg.oy, frameLayer);
  }

  /** 绕 axis 从 from 方向转到 to 方向画圆弧（带符号角，用于扭角 α）*/
  function drawAngleArc(center, from, to, axis, radius, color, label, labelPush, labelDx, labelDy) {
    var a0 = FK.Vec.normalize(from);
    var a1 = FK.Vec.normalize(to);
    var av = FK.Vec.normalize(axis);
    var total = Math.atan2(FK.Vec.dot(FK.Vec.cross(a0, a1), av), FK.Vec.dot(a0, a1));
    if (Math.abs(total) < 1e-9) return;
    var perp = FK.Vec.cross(av, a0);          // av·a0 = 0 时成立
    var pts = [];
    var steps = 40;
    for (var i = 0; i <= steps; i += 1) {
      var t = total * (i / steps);
      var dir = FK.Vec.add(FK.Vec.scale(a0, Math.cos(t)), FK.Vec.scale(perp, Math.sin(t)));
      pts.push(FK.Vec.add(center, FK.Vec.scale(dir, radius)));
    }
    scene.polyline(pts, {
      stroke: color, "stroke-width": 2.6, "stroke-dasharray": "6 5", fill: "none"
    }, dimLayer);
    var midDir = FK.Vec.add(FK.Vec.scale(a0, Math.cos(total / 2)), FK.Vec.scale(perp, Math.sin(total / 2)));
    tag(FK.Vec.add(center, FK.Vec.scale(midDir, radius * (labelPush || 1.7))), label,
      { fill: color, "font-size": 16, class: "fk-axis-label" },
      labelDx === undefined ? -10 : labelDx, labelDy === undefined ? 6 : labelDy, dimLayer);
  }

  /* ------------------------------------------------------------------ 渲染 */

  function render() {
    applyLayout();
    gridLayer.replaceChildren();
    jointLayer.replaceChildren();
    dimLayer.replaceChildren();
    frameLayer.replaceChildren();

    var a = state.a;
    var alpha = state.alpha * FK.DEG;
    var d = state.d;
    var theta = state.theta * FK.DEG;
    var degenerate = Math.abs(state.alpha) < 2;

    // 全部几何量都由连杆变换推出，避免“画一套、算一套”
    var A = linkTransform(a, alpha, d, theta);
    var R = FK.M4.rotation(A);
    var Oi = FK.M4.position(A);                 // = (a·cθ, a·sθ, d)
    var Xi = [R[0], R[3], R[6]];                // X_i（第 1 列）
    var Yi = [R[1], R[4], R[7]];                // Y_i（第 2 列）
    var Zi = degenerate ? ZAX : [R[2], R[5], R[8]];  // Z_i（第 3 列）= 关节轴 i 的方向
    var foot = [0, 0, d];                       // 公垂线在 Z_{i-1} 上的垂足

    // 地面网格（弱参照）
    var gridGroup = scene.el("g", { class: "fk-grid" }, gridLayer);
    for (var gi = -2; gi <= 3; gi += 1) {
      scene.line([-2, gi, 0], [3, gi, 0], { class: "fk-grid-line" }, gridGroup);
      scene.line([gi, -2, 0], [gi, 3, 0], { class: "fk-grid-line" }, gridGroup);
    }

    /* --- 关节轴 i-1（= Z_{i-1}） ------------------------------------ */
    var zTop = 2.35;
    seg([0, 0, -1.15], [0, 0, zTop], {
      stroke: C.prev, "stroke-width": 3.4, "marker-end": "url(#arrowPrev)"
    }, jointLayer);
    tag([0, 0, zTop], "关节轴 i\u22121（Z" + "i\u22121" + "）",
      { fill: C.prev, "font-size": 15, class: "fk-axis-label" }, -92, -4, jointLayer);

    /* --- 关节轴 i（= Z_i），过 O_i，方向 Zi ------------------------- */
    var lo = FK.Vec.add(Oi, FK.Vec.scale(Zi, -1.0));
    var hi = FK.Vec.add(Oi, FK.Vec.scale(Zi, 1.85));
    seg(lo, hi, {
      stroke: C.next, "stroke-width": 3.4, "marker-end": "url(#arrowNext)"
    }, jointLayer);
    tag(hi, "关节轴 i（Z" + "i" + "）",
      { fill: C.next, "font-size": 15, class: "fk-axis-label" }, 16, 6, jointLayer);

    /* --- 公垂线 a_{i-1} 与叉积箭头 ---------------------------------- */
    if (state.showPerp) {
      seg(foot, Oi, {
        stroke: C.a, "stroke-width": 3.2, "marker-end": "url(#arrowA)"
      }, dimLayer);
      if (a > 0.25) {
        tag(FK.Vec.add(FK.Vec.scale(foot, 0.45), FK.Vec.scale(Oi, 0.55)), "a" + "i\u22121",
          { fill: "#8a4a08", "font-size": 17, "font-style": "italic", class: "fk-axis-label" },
          -12, 24, dimLayer);
      }
      // 叉积方向：Z_{i-1} × Z_i ∝ X_i（画在原点附近，指向公垂线方向）
      var crossDir = FK.Vec.normalize(FK.Vec.cross(ZAX, Zi));
      seg([0, 0, 0], FK.Vec.scale(crossDir, 0.78), {
        stroke: C.a, "stroke-width": 2, "stroke-dasharray": "5 4", "marker-end": "url(#arrowCross)"
      }, dimLayer);
      tag(FK.Vec.scale(crossDir, 0.5), "Z\u0302" + "i\u22121" + " \u00d7 Z\u0302" + "i" + " \u221d X\u0302" + "i",
        { fill: "#8a4a08", "font-size": 12.5, "data-mobile-hide": "1" }, -20, 58, dimLayer);
    }

    /* --- 沿 Z_{i-1} 的偏距 d_i -------------------------------------- */
    if (state.showOffset) {
      seg([0, 0, 0], foot, { stroke: C.d, "stroke-width": 3.6 }, dimLayer);
      if (d > 0.12) {
        tag([0, 0, d * 0.5], "d" + "i",
          { fill: C.d, "font-size": 17, "font-style": "italic", class: "fk-axis-label" },
          -66, 6, dimLayer);
      }
      var fp = scene.project(foot);
      scene.el("circle", { cx: fp.x, cy: fp.y, r: 4, fill: C.d }, dimLayer);
    }

    /* --- 扭角 α_{i-1}：绕 X_i 从 Z_{i-1} 转到 Z_i -------------------- */
    if (state.showTwist) {
      if (degenerate) {
        tag([0, 1.0, 0.35], "\u03b1" + "i\u22121" + " \u2248 0\uff1a\u4e24\u8f74\u5e73\u884c",
          { fill: "#b3261e", "font-size": 14, class: "fk-axis-label" }, -60, 0, dimLayer);
      } else {
        // 在 O_i 处补一段沿 Z_{i-1} 的参考虚线，明确 α 是两条轴线方向的夹角
        seg(Oi, FK.Vec.add(Oi, FK.Vec.scale(ZAX, 0.85)), {
          stroke: C.ref, "stroke-width": 1.6, "stroke-dasharray": "4 4"
        }, dimLayer);
        tag(FK.Vec.add(Oi, FK.Vec.scale(ZAX, 0.85)), "\u2225 Z" + "i\u22121",
          { fill: C.ref, "font-size": 12.5, "data-mobile-hide": "1" }, -62, 12, dimLayer);
        drawAngleArc(Oi, ZAX, Zi, Xi, 0.6, C.next, "\u03b1" + "i\u22121", 2.35, -68, 4);
      }
    }

    /* --- 连杆夹角 θ_i：绕 Z_{i-1} 从 X_{i-1} 到 X_i ------------------ */
    if (state.showJoint) {
      var thArcPts = [];
      var tSteps = 40;
      for (var k = 0; k <= tSteps; k += 1) {
        var t = theta * (k / tSteps);
        thArcPts.push(FK.Vec.add(foot, [0.42 * Math.cos(t), 0.42 * Math.sin(t), 0]));
      }
      scene.polyline(thArcPts, {
        stroke: "#2563eb", "stroke-width": 2.4, "stroke-dasharray": "6 5", fill: "none"
      }, dimLayer);
      var midT = theta / 2;
      tag(FK.Vec.add(foot, [0.42 * 2.0 * Math.cos(midT), 0.42 * 2.0 * Math.sin(midT), 0]),
        "\u03b8" + "i",
        { fill: "#174ea6", "font-size": 17, "font-style": "italic", class: "fk-axis-label" },
        -70, 34, dimLayer);
      seg(foot, FK.Vec.add(foot, [0.58, 0, 0]), {
        stroke: "#8fb0ea", "stroke-width": 1.4, "stroke-dasharray": "4 4"
      }, dimLayer);
      tag(FK.Vec.add(foot, [0.58, 0, 0]), "\u2225 X" + "i\u22121",
        { fill: "#5b6a80", "font-size": 12.5, "data-mobile-hide": "1" }, -46, -6, dimLayer);
    }

    /* --- 两个连杆坐标系（只画 X / Y；Z 就是关节轴） ------------------ */
    if (state.showFrames) {
      drawFrameXY([0, 0, 0], XAX, [0, 1, 0], {
        length: 1.05, width: 2.3, dash: "7 4",
        xLabel: "X" + "i\u22121", yLabel: "Y" + "i\u22121",
        oLabel: "O" + "i\u22121", ox: -40, oy: 20, fontSize: 14, dotR: 4.4
      });
      drawFrameXY(Oi, Xi, Yi, {
        length: 1.05, width: 3.0,
        xLabel: "X" + "i", yLabel: "Y" + "i",
        oLabel: "O" + "i", ox: -30, oy: -18, fontSize: 15, dotR: 5
      });
    } else {
      dotAt([0, 0, 0], C.joint, 4.6);
      dotAt(Oi, C.joint, 5);
    }

    /* --- 退化提示 ---------------------------------------------------- */
    var degenNode = document.getElementById("degen");
    if (degenNode) {
      if (degenerate) degenNode.classList.add("on");
      else degenNode.classList.remove("on");
    }

    /* --- 读数 -------------------------------------------------------- */
    function put(id, text) {
      var node = document.getElementById(id);
      if (node) node.textContent = text;
    }
    put("aOut", FK.format(a, 3));
    put("alphaOut", FK.deg(state.alpha, 1));
    put("dOut", FK.format(d, 3));
    put("thetaOut", FK.deg(state.theta, 1));

    var CELLS = ["theta", "alpha", "alpha", "len",
      "theta", "alpha", "alpha", "len",
      "", "alpha", "alpha", "dist",
      "", "", "", ""];
    for (var r = 0; r < 4; r += 1) {
      for (var cc = 0; cc < 4; cc += 1) {
        var cell = document.getElementById("t-" + r + "-" + cc);
        if (cell) {
          cell.textContent = mnum(A[r * 4 + cc], 3);
          cell.className = CELLS[r * 4 + cc];
        }
      }
    }
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "a", key: "a", value: DEFAULTS.a, format: function (v) { return FK.format(v, 3); } },
    { id: "alpha", key: "alpha", value: DEFAULTS.alpha, format: function (v) { return FK.deg(v, 1); } },
    { id: "d", key: "d", value: DEFAULTS.d, format: function (v) { return FK.format(v, 3); } },
    { id: "theta", key: "theta", value: DEFAULTS.theta, format: function (v) { return FK.deg(v, 1); } }
  ], state, render);

  FK.bindToggles([
    { id: "showPerp", key: "showPerp" },
    { id: "showTwist", key: "showTwist" },
    { id: "showOffset", key: "showOffset" },
    { id: "showJoint", key: "showJoint" },
    { id: "showFrames", key: "showFrames" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.a = DEFAULTS.a;
    state.alpha = DEFAULTS.alpha;
    state.d = DEFAULTS.d;
    state.theta = DEFAULTS.theta;
    state.showPerp = true;
    state.showTwist = true;
    state.showOffset = true;
    state.showJoint = true;
    state.showFrames = true;
    state.auto = false;
    ["showPerp", "showTwist", "showOffset", "showJoint", "showFrames"].forEach(function (id) {
      document.getElementById(id).checked = true;
    });
    document.getElementById("auto").checked = false;
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
    var configs = [
      [1.6, 25 * FK.DEG, 0.9],
      [0.5, 70 * FK.DEG, 1.8],
      [2.4, -60 * FK.DEG, 0.25],
      [1.0, 5 * FK.DEG, 1.0]
    ];
    var thetas = [0, 30, -90, 45, 137, 180, -180];

    function wrap180(rad) {
      var v = rad;
      while (v > Math.PI) v -= 2 * Math.PI;
      while (v <= -Math.PI) v += 2 * Math.PI;
      return v;
    }

    for (var ci = 0; ci < configs.length; ci += 1) {
      var a = configs[ci][0], al = configs[ci][1], d = configs[ci][2];
      for (var ti = 0; ti < thetas.length; ti += 1) {
        var th = thetas[ti] * FK.DEG;
        var M = linkTransform(a, al, d, th);
        var R = FK.M4.rotation(M);
        var Oi = FK.M4.position(M);
        var Xi = [R[0], R[3], R[6]];
        var Zi = [R[2], R[5], R[8]];
        var foot = [0, 0, d];

        // 1) a_{i-1}：公垂线长度 = |Oi - foot|，方向沿 X_i
        var perp = FK.Vec.sub(Oi, foot);
        if (Math.abs(FK.Vec.len(perp) - a) > 1e-12) {
          throw new Error("图3-16 自检失败：公垂线长度 ≠ a_{i−1}");
        }
        if (!FK.Vec.eq(FK.Vec.round(FK.Vec.normalize(perp), 9), FK.Vec.round(Xi, 9), 1e-9)) {
          throw new Error("图3-16 自检失败：公垂线方向应为 X_i");
        }
        // 2) 垂足落在 Z_{i-1} 轴上，且 d_i = |O_{i-1} → 垂足|
        if (Math.abs(foot[0]) > 1e-15 || Math.abs(foot[1]) > 1e-15) {
          throw new Error("图3-16 自检失败：公垂线垂足不在 Z_{i−1} 轴上");
        }
        if (Math.abs(FK.Vec.len(foot) - d) > 1e-12) {
          throw new Error("图3-16 自检失败：d_i 不等于垂足到 O_{i−1} 的距离");
        }
        // 3) X_i ⊥ Z_{i-1} ⊥ ？、Z_i ⊥ X_i，且 X_i 与 X_{i-1} 的夹角 = θ_i
        if (Math.abs(FK.Vec.dot(Xi, [0, 0, 1])) > 1e-12 || Math.abs(FK.Vec.dot(Zi, Xi)) > 1e-12) {
          throw new Error("图3-16 自检失败：X_i 应同时垂直于 Z_{i−1} 与 Z_i");
        }
        var angX = wrap180(Math.atan2(Xi[1], Xi[0]));
        if (Math.abs(wrap180(angX - wrap180(th))) > 1e-12) {
          throw new Error("图3-16 自检失败：X_i 与 X_{i−1} 的夹角应等于 θ_i");
        }
        // 4) 两关节轴夹角 = |α|；两轴公垂距离 = |a|
        var cosAxes = Math.max(-1, Math.min(1, FK.Vec.dot([0, 0, 1], Zi)));
        if (Math.abs(Math.acos(cosAxes) - Math.abs(al)) > 1e-12) {
          throw new Error("图3-16 自检失败：两关节轴夹角应等于 |α_{i−1}|");
        }
        var crossAxes = FK.Vec.cross([0, 0, 1], Zi);
        if (FK.Vec.len(crossAxes) > 1e-12) {
          var dist = Math.abs(FK.Vec.dot(Oi, FK.Vec.normalize(crossAxes)));
          if (Math.abs(dist - Math.abs(a)) > 1e-12) {
            throw new Error("图3-16 自检失败：两关节轴之间的最短距离应为 |a_{i−1}|，实际 " + dist);
          }
        }
        // 5) R 正交、det = +1
        if (Math.abs(R[0] * R[1] + R[3] * R[4] + R[6] * R[7]) > 1e-12) {
          throw new Error("图3-16 自检失败：R 不正交");
        }
        var det = R[0] * (R[4] * R[8] - R[5] * R[7]) - R[1] * (R[3] * R[8] - R[5] * R[6]) +
          R[2] * (R[3] * R[7] - R[4] * R[6]);
        if (Math.abs(det - 1) > 1e-12) throw new Error("图3-16 自检失败：det(R) ≠ 1");
      }
      // 6) θ=0 的可手算特例：O_i = (a,0,d)，Z_i = (0,−sinα,cosα)
      var M0 = linkTransform(a, al, d, 0);
      if (!FK.Vec.eq(FK.Vec.round(FK.M4.position(M0), 12), [a, 0, d], 1e-12)) {
        throw new Error("图3-16 自检失败：θ=0 时 O_i 应为 (a,0,d)");
      }
      var R0 = FK.M4.rotation(M0);
      var Z0 = [R0[2], R0[5], R0[8]];
      var expectZ0 = [0, -Math.sin(al), Math.cos(al)];
      if (!FK.Vec.eq(FK.Vec.round(Z0, 12), FK.Vec.round(expectZ0, 12), 1e-12)) {
        throw new Error("图3-16 自检失败：θ=0 时 Z_i 应为 (0,−sinα,cosα)");
      }
    }

    // 7) 四步连乘（教材写法）与连杆变换逐元素一致
    var a0 = 1.6, al0 = 25 * FK.DEG, d0 = 0.9;
    var fourStep = FK.M4.chain(
      FK.M4.rotZ(37 * FK.DEG),
      FK.M4.translate([a0, 0, d0]),
      FK.M4.rotX(al0)
    );
    var direct = linkTransform(a0, al0, d0, 37 * FK.DEG);
    for (var m = 0; m < 16; m += 1) {
      if (Math.abs(fourStep[m] - direct[m]) > 1e-12) {
        throw new Error("图3-16 自检失败：四步连乘与连杆变换不一致（第 " + m + " 项）");
      }
    }
    // 8) 默认参数下的矩阵参照值（与教材式(3.20) 同形，θ=30°、α=25°、a=1.6、d=0.9）
    var MD = linkTransform(1.6, 25 * FK.DEG, 0.9, 30 * FK.DEG);
    var expectD = [
      0.866025403784439, -0.453153893518325, 0.211309130870350, 1.385640646055102,
      0.5, 0.784885567221396, -0.365998150770667, 0.8,
      0, 0.422618261740699, 0.906307787036650, 0.9,
      0, 0, 0, 1
    ];
    for (var q = 0; q < 16; q += 1) {
      if (Math.abs(MD[q] - expectD[q]) > 1e-9) {
        throw new Error("图3-16 自检失败：默认参数下矩阵第 " + q + " 项应为 " + expectD[q] + "，实际 " + MD[q]);
      }
    }
  }());

  render();
}());
"""

FIGURE = {
    "id": "figure-3-16",
    "title": "图3-16 转动关节连杆D-H坐标系建立示意图 · 人机交互演示",
    "css": CSS,
    "body": BODY,
    "script": SCRIPT,
}
