"""图1-8 球坐标型机器人（《机器人技术基础（第三版）》1.2.5 节 三、球坐标型机器人）。

教材依据（第1章 1.2.5 按坐标形式分类）：
- 正文原话：“这类机器人手臂的运动由一个直线运动和两个转动所组成，如图 1.8 所示，
  即沿手臂方向 (X 轴) 的伸缩、绕 Y 轴的俯仰和绕 Z 轴的回转。UNIMATE 机器人是其典型代表。”
- 同节对比四类机器人的运动轴组合：
    直角坐标型＝3 个移动（沿 X 纵向、沿 Y 横向、沿 Z 升降，图1.6）；
    圆柱坐标型＝1 转 2 移（绕立柱转动 + 沿立柱升降 + 立柱平面内伸缩，图1.7 VERSATRAN）；
    球坐标型  ＝2 转 1 移（绕 Z 回转 + 绕 Y 俯仰 + 沿手臂 X 伸缩，本图）；
    关节坐标型＝3 个转动（图1.9 PUMA）。
- 本图强调的判据：球坐标型的俯仰是“绕 Y 轴”，不是绕 Z 轴；圆柱坐标型没有俯仰轴，
  它沿 Z 轴升降。两者都“绕 Z 回转 + 沿 X 伸缩”，区别只在第二个自由度是
  “绕 Y 俯仰”（球坐标）还是“沿 Z 升降”（圆柱坐标）——图内用文字直接标出这一句。

运动学（本图采用并写清的几何关系，脚本内断言自检）：
- 基座高度 h = 0.8 固定；肩关节（俯仰轴所在处）位于 (0, 0, h)。
- 关节变量：回转角 φ 绕 Ẑ；俯仰角 θ 绕 Ŷ（**θ = 0 时手臂水平指向基座 X̂ 正向，
  θ > 0 时手臂抬起**，即 θ 为手臂相对水平面的仰角）；伸缩长度 d 为手臂沿自身轴线的伸出量。
  记手臂单位方向 u = Rot(Ŷ, −θ)·[1,0,0]ᵀ = [cosθ, 0, sinθ]ᵀ，则
      ᴬP = Rot(Ẑ, φ) · ( [0,0,h]ᵀ + d·u )
         = [ d·cosθ·cosφ , d·cosθ·sinφ , h + d·sinθ ]ᵀ
- 自检 1（题面要求的“三个变量取 0 时的几何关系”）：φ = θ = 0、d = 1.2 时，
  末端 z = h + d·sinθ = h = 0.8，水平投影 = d·cosθ = d = 1.2，x = d、y = 0；
  一般地 θ 取任意值时恒有“末端相对肩关节的水平投影 = d·cosθ、竖向升高 = d·sinθ”，
  即 **肩关节高度 + 手臂竖向升高 = 末端高度**（θ = 0 时升高为 0，末端与肩同高）。
- 自检 2：回转 360°（φ → φ ± 360°）后末端回到原位（误差 < 1e-9）。
- 自检 3：俯仰 θ 只改变“水平投影半径 d·cosθ”与“升高 d·sinθ”，不改变方位角；
  θ = ±90° 时水平投影为 0（手臂竖直，末端落在回转轴上）；
  且 θ = 0 时末端到肩关节的距离恒等于伸缩长度 d（伸缩量即手臂长度）。
- 自检 4：沿手臂的移动副不产生任何转动——伸缩轴与手臂方向恒重合，
  末端相对肩关节的位移始终与手臂轴线平行（区别于旋转副）。
自检失败直接 throw。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

CSS = COMMON_CSS + """
.readout .row { white-space: normal; }
.readout .ok { color: #15803d; font-weight: 700; }
.panel h1 { overflow-wrap: anywhere; }
/* 读数卡移到左下角：三维手臂向右上伸出，左下角基本为空 */
.readout { right: auto; left: 16px; max-width: min(430px, calc(100% - 32px)); }
/* 图例线型：虚线段表示“轴向/轨迹提示”，避免只靠颜色区分 */
.legend i.dash { background-image: repeating-linear-gradient(90deg, #fff 0 3px, transparent 3px 6px); background-color: transparent; }
@media (max-width: 720px) {
  .panel { padding: 9px 11px; }
  .panel h1 { font-size: 13.5px; }
  .control { margin-top: 5px; }
  input[type="range"] { margin: 4px 0 0; }
  .options, .legend { margin-top: 6px; padding-top: 5px; gap: 4px 9px; font-size: 11px; }
  .readout { left: 8px; right: 8px; max-width: none; padding: 6px 8px; font-size: 11.5px; line-height: 1.45; }
  .readout .small { font-size: 10.5px; }
  /* 窄屏顶部空间紧张：隐藏次要两行，保证图形有足够高度 */
  .readout .row:nth-child(3), .readout .row:nth-child(4) { display: none; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="球坐标型机器人：绕Z轴回转、绕Y轴俯仰、沿手臂X轴伸缩的交互示意">
  <defs>
    <marker id="f8X" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="f8Y" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="f8Z" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="f8V" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="f8S" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="f8A" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="f8W" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
  </defs>
  <g id="f8Grid"></g>
  <g id="f8Work"></g>
  <g id="f8Trail"></g>
  <g id="f8Body"></g>
  <g id="f8Axes"></g>
  <g id="f8Tip"></g>
</svg>

<section class="panel" aria-label="图1-8 控制面板">
  <div class="panel-head">
    <div>
      <h1>图1-8 球坐标型机器人</h1>
      <p class="subtitle">2 个转动 + 1 个移动：绕 Ẑ 回转 φ、绕 Ŷ 俯仰 θ、沿手臂 X̂ 伸缩 d。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="yaw">回转角 φ（绕 Ẑ）</label><output id="yawValue">30.0°</output></div>
    <input id="yaw" type="range" min="-180" max="180" step="1" value="30">
  </div>
  <div class="control">
    <div class="control-head"><label for="pitch">俯仰角 θ（绕 Ŷ）</label><output id="pitchValue">40.0°</output></div>
    <input id="pitch" type="range" min="-80" max="80" step="1" value="40">
  </div>
  <div class="control">
    <div class="control-head"><label for="ext">伸缩长度 d（沿 X̂）</label><output id="extValue">1.200</output></div>
    <input id="ext" type="range" min="0.4" max="2" step="0.01" value="1.2">
  </div>

  <div class="options">
    <label><input id="showFrame" type="checkbox" checked>显示坐标系与轴标</label>
    <label><input id="showWork" type="checkbox" checked>显示工作空间提示</label>
    <label><input id="showSweep" type="checkbox" checked>显示末端轨迹弧线</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i style="background:#d93025"></i>X̂（伸缩轴，红色）</span>
    <span><i style="background:#2563eb"></i>Ŷ（俯仰轴，蓝色·虚线）</span>
    <span><i style="background:#12944f"></i>Ẑ（回转轴，绿色）</span>
    <span><i class="dash" style="background:#c26a10"></i>伸缩活塞滑移副</span>
    <span><i class="dot" style="background:#c26a10"></i>末端点 P</span>
    <span><i class="dash" style="background:#7c3aed"></i>单变量运动轨迹弧线</span>
  </div>
</section>

<div class="hint">拖动旋转视角 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row"><strong>关节变量</strong>：φ = <span id="yawOut">30.0°</span>，θ = <span id="pitchOut">40.0°</span>，d = <span id="extOut">1.200</span></div>
  <div class="row"><strong>末端 ᴬP</strong> = ( <span id="pxOut">0.959</span>, <span id="pyOut">0.554</span>, <span id="pzOut">1.571</span> )<span class="small">（基坐标系 {A}，长度单位）</span></div>
  <div class="row small">回转投影半径 r = d·cosθ = <span id="rOut">0.919</span>；基座高度 h = 0.800；
    末端高度 z = h + d·sinθ（θ = 0 时手臂水平、末端与肩同高）</div>
  <div class="row small" id="axisNote">回转轴 Ẑ 竖直；俯仰轴 Ŷ 水平，θ 为手臂相对水平面的仰角——球坐标型的第二轴是俯仰，
    圆柱坐标型（图1.7）为沿 Ẑ 升降。</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gGrid = document.getElementById("f8Grid");
  var gWork = document.getElementById("f8Work");
  var gTrail = document.getElementById("f8Trail");
  var gBody = document.getElementById("f8Body");
  var gAxes = document.getElementById("f8Axes");
  var gTip = document.getElementById("f8Tip");

  var scene = new FK.Scene({
    svg: viewport, origin: { x: 505, y: 420 }, scale: 80,
    yaw: -0.66, pitch: 0.44, minScale: 34, maxScale: 190
  });

  var BASE_H = 0.8;               // 基座（肩关节）高度 h，固定
  var DEFAULTS = { yaw: 30, pitch: 40, ext: 1.2 };
  var state = {
    yaw: DEFAULTS.yaw, pitch: DEFAULTS.pitch, ext: DEFAULTS.ext,
    showFrame: true, showWork: true, showSweep: true, auto: false, compact: false
  };

  /* 自适应取景：viewBox 与视口像素 1:1。state 必须在 fit() 首次调用之前声明（见上）。 */
  function fit() {
    var rect = viewport.getBoundingClientRect();
    var W = Math.max(260, Math.round(rect.width || 1000));
    var H = Math.max(260, Math.round(rect.height || 620));
    viewport.setAttribute("viewBox", "0 0 " + W + " " + H);
    viewport.setAttribute("preserveAspectRatio", "xMidYMid meet");
    var narrow = W < 620;
    var availW = W * (narrow ? 0.86 : 0.60);
    var availH = H * (narrow ? 0.54 : 0.62);
    var k = Math.min(availW / 4.4, availH / (narrow ? 2.9 : 3.3));
    scene.state.scale = Math.max(34, Math.min(190, k));
    scene.defaults.scale = scene.state.scale;
    state.compact = scene.state.scale < 62;
    scene.baseOrigin.x = W * 0.5;
    scene.baseOrigin.y = H * (narrow ? 0.34 : 0.66);
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  var C = {
    x: "#d93025", y: "#2563eb", z: "#12944f", frame: "#475569",
    piston: "#c26a10", rod: "#e08b3a", tip: "#c26a10", work: "#94a3b8",
    trailYaw: "#7c3aed", trailPitch: "#0e7490", axial: "#c26a10"
  };

  var sweep = { frame: 0, dir: 1 };

  /* ------------------------------------------------------------ 运动学 */

  /** 球坐标型 FK：手臂方向 u = Rot(Ŷ,−θ)·[1,0,0]ᵀ，末端 = Rot(Ẑ,φ)·(肩关节 + d·u) */
  function fk(yawDeg, pitchDeg, d) {
    var phi = Number(yawDeg) * FK.DEG, th = Number(pitchDeg) * FK.DEG;
    var len = Number(d);
    // Rot(Ŷ, −θ) 作用在 [1,0,0] 上 → [cosθ, 0, sinθ]：θ>0 手臂抬起
    var shoulder = [0, 0, BASE_H];
    var arm = [len * Math.cos(th), 0, BASE_H + len * Math.sin(th)];
    var P = FK.M4.apply(FK.M4.rotZ(phi), arm);
    return {
      shoulder: shoulder,
      tip: P,
      // 伸缩轴（手臂轴线）方向：Rot(Ẑ,φ)·Rot(Ŷ,−θ)·[1,0,0]ᵀ
      axisX: FK.M4.applyDir(FK.M4.chain(FK.M4.rotZ(phi), FK.M4.rotY(-th)), [1, 0, 0]),
      // 基准手臂方向 Rot(Ẑ,φ)·[1,0,0]ᵀ，用于竖直平面内的俯仰弧线
      armDir: [Math.cos(phi), Math.sin(phi), 0]
    };
  }

  /* ------------------------------------------------------------ 绘图辅助 */

  function seg(a, b, attrs, layer) {
    var p = scene.project(a), q = scene.project(b);
    return scene.el("line", Object.assign({ x1: p.x, y1: p.y, x2: q.x, y2: q.y }, attrs || {}), layer);
  }
  function put(v, str, attrs, dx, dy, layer) {
    var p = scene.project(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0), "font-size": 15,
      class: "fk-axis-label", "paint-order": "stroke"
    }, attrs || {}), layer);
    node.textContent = str;
    return node;
  }
  function curve(pts, attrs, layer) {
    return scene.polyline(pts, Object.assign({ fill: "none" }, attrs || {}), layer);
  }
  function circlePts(r, z, n) {
    var out = [], i;
    for (i = 0; i <= n; i += 1) {
      var a = i * 2 * Math.PI / n;
      out.push([r * Math.cos(a), r * Math.sin(a), z]);
    }
    return out;
  }
  /** 竖直平面（方位角 phi 所在平面）内绕 Ŷ 俯仰的弧线 */
  function pitchArc(phiDeg, d, fromDeg, toDeg, n) {
    var phi = Number(phiDeg) * FK.DEG, u = [Math.cos(phi), Math.sin(phi), 0], out = [], i;
    for (i = 0; i <= n; i += 1) {
      var th = (fromDeg + (toDeg - fromDeg) * i / n) * FK.DEG;
      var r = Number(d) * Math.cos(th), dz = BASE_H + Number(d) * Math.sin(th);
      out.push([u[0] * r, u[1] * r, dz]);
    }
    return out;
  }
  /** 绕 Z 回转的圆弧 */
  function yawCircle(r, z, fromDeg, toDeg, n) {
    var out = [], i;
    for (i = 0; i <= n; i += 1) {
      var a = (fromDeg + (toDeg - fromDeg) * i / n) * FK.DEG;
      out.push([r * Math.cos(a), r * Math.sin(a), z]);
    }
    return out;
  }
  /** 当前投影缩放（把像素量换算成世界量时用，避免把像素当世界量） */
  function approxScale() { return scene.state.scale; }

  /* --------------------------------------------------------- 各部件绘制 */

  function drawBase() {
    // 地面基座（圆柱简图）
    var r = 0.34, z0 = 0, z1 = BASE_H;
    curve(circlePts(r, z0, 48), { stroke: C.frame, "stroke-width": 2.2 }, gBody);
    curve(circlePts(r, z1, 48), { stroke: C.frame, "stroke-width": 2.2 }, gBody);
    var i;
    for (i = 0; i < 12; i += 1) {
      var a = i * Math.PI / 6;
      seg([r * Math.cos(a), r * Math.sin(a), z0], [r * Math.cos(a), r * Math.sin(a), z1],
        { stroke: "#a9b7c9", "stroke-width": 1.1 }, gBody);
    }
    // 机座地面投影（脚）
    seg([-0.55, -0.55, 0], [0.55, -0.55, 0], { stroke: "#c3cede", "stroke-width": 2.4 }, gBody);
    seg([-0.55, 0.55, 0], [0.55, 0.55, 0], { stroke: "#c3cede", "stroke-width": 2.4 }, gBody);
    seg([-0.55, -0.55, 0], [-0.55, 0.55, 0], { stroke: "#c3cede", "stroke-width": 2.4 }, gBody);
    seg([0.55, -0.55, 0], [0.55, 0.55, 0], { stroke: "#c3cede", "stroke-width": 2.4 }, gBody);
  }

  /** 回转体：绕 Ẑ 的转台（基座顶面上的一段扇形），标出 φ 的转向 */
  function drawYawJoint(yawDeg) {
    var r = 0.42, z = BASE_H, pts = yawCircle(r, z, 0, yawDeg, 48);
    if (Math.abs(yawDeg) > 0.5) {
      curve(pts, { stroke: C.z, "stroke-width": 2.6, "stroke-dasharray": "6 5" }, gBody);
      curve([pts[pts.length - 1], [0, 0, z]], { stroke: C.z, "stroke-width": 2, "stroke-dasharray": "4 4" }, gBody);
    }
    // 回转轴的螺旋箭头（右手法则）
    var sp = [], i;
    for (i = 0; i <= 60; i += 1) {
      var t = (i / 60) * 2.4 * Math.PI;
      sp.push([0.72 * Math.cos(t), 0.72 * Math.sin(t), BASE_H + 0.42 + 0.30 * (i / 60)]);
    }
    curve(sp, { stroke: C.z, "stroke-width": 1.6, "stroke-dasharray": "5 4", opacity: 0.85 }, gBody);
    put([0.72 * Math.cos(2.4 * Math.PI), 0.72 * Math.sin(2.4 * Math.PI), BASE_H + 0.72],
      "φ", { fill: C.z, "font-size": 17, "font-style": "italic" }, 6, -6, gBody);
  }

  /** 俯仰轴 Ŷ：水平双箭头（贯穿肩关节），并画俯仰弧线 */
  function drawPitchJoint(yawDeg, pitchDeg, d, armDir) {
    // 俯仰轴线方向：绕 Ẑ 回转后的 Y 方向
    var yDir = [-Math.sin(yawDeg * FK.DEG), Math.cos(yawDeg * FK.DEG), 0];
    var L = 1.05;
    var aP = FK.Vec.add([0, 0, BASE_H], FK.Vec.scale(yDir, -L));
    var bP = FK.Vec.add([0, 0, BASE_H], FK.Vec.scale(yDir, L));
    seg(aP, bP, { stroke: C.y, "stroke-width": 2.6, "stroke-dasharray": "10 6" }, gAxes);
    seg(aP, FK.Vec.add(aP, FK.Vec.scale(yDir, -0.16)), { stroke: C.y, "stroke-width": 2.6 }, gAxes);
    seg(bP, FK.Vec.add(bP, FK.Vec.scale(yDir, 0.16)), { stroke: C.y, "stroke-width": 2.6 }, gAxes);
    put(bP, "Ŷ 俯仰轴", { fill: C.y, "font-size": 14 }, 8, -8, gAxes);

    // 俯仰角 θ 的弧线（竖直平面内）
    if (Math.abs(pitchDeg) > 0.5) {
      var arc = pitchArc(yawDeg, d, 0, pitchDeg, 48);
      curve(arc, { stroke: C.trailPitch, "stroke-width": 2.8, "stroke-dasharray": "7 5" }, gTrail);
      var mid = pitchArc(yawDeg, d * 0.62, pitchDeg * 0.28, pitchDeg * 0.28, 1)[0];
      put(mid, "θ = " + FK.format(pitchDeg, 0) + "\u00b0", { fill: C.trailPitch, "font-size": 14 }, 6, 4, gTrail);
      // θ 的参考水平线（θ = 0 手臂方向）
      var refEnd = [armDir[0] * d, armDir[1] * d, BASE_H];
      curve([FK.Vec.scale(armDir, 0.18), refEnd], { stroke: "#cbd5e1", "stroke-width": 1.4, "stroke-dasharray": "5 5" }, gTrail);
    }
  }

  /** 伸缩臂：活塞式滑移副（缸体 + 活塞杆），沿手臂 X̂ 方向 */
  function drawArm(yawDeg, pitchDeg, d) {
    var arm = fk(yawDeg, pitchDeg, d);
    var angDeg = yawDeg;                 // 手臂在水平面内的方位角
    var cylLen = Math.min(d * 0.45, d - 0.25);   // 缸体：固定端
    var cylH = 0.27, rodH = 0.105;

    var g = scene.el("g", {
      transform: "translate(" + scene.baseOrigin.x.toFixed(2) + "," + scene.baseOrigin.y.toFixed(2) +
        ") rotate(" + (-angDeg).toFixed(3) + ")"
    }, gBody);
    // 缸体（固定端，从肩关节伸出）
    scene.el("rect", {
      x: 0, y: -cylH / 2, width: cylLen, height: cylH, rx: 4,
      fill: "#f7e5d0", stroke: C.piston, "stroke-width": 2.4
    }, g);
    // 端盖
    scene.el("line", {
      x1: cylLen, y1: -cylH / 2 - 0.035, x2: cylLen, y2: cylH / 2 + 0.035,
      stroke: "#a35c07", "stroke-width": 2.2
    }, g);
    // 活塞杆（伸出端）—— 细杆从缸体中伸出，到手臂末端
    scene.el("rect", {
      x: cylLen - 0.04, y: -rodH / 2, width: Math.max(0.10, d - cylLen + 0.04), height: rodH,
      fill: C.rod, stroke: "#a35c07", "stroke-width": 1.1
    }, g);
    // 滑移副符号：沿手臂方向的虚线（移动副，不是旋转副）
    scene.el("line", {
      x1: cylLen, y1: 0, x2: d, y2: 0, stroke: "#a35c07", "stroke-width": 1.1,
      "stroke-dasharray": "7 6", opacity: 0.8
    }, g);
    // 行程尺寸线：双箭头表示“沿 X̂ 的直线移动”
    var s = approxScale();
    scene.el("line", {
      x1: cylLen, y1: -cylH / 2 - 11 / s, x2: d, y2: -cylH / 2 - 11 / s,
      stroke: C.axial, "stroke-width": 1.6,
      "marker-start": "url(#f8S)", "marker-end": "url(#f8S)"
    }, g);
    var lab = scene.el("text", {
      x: (cylLen + d) / 2, y: -cylH / 2 - 20 / s, "text-anchor": "middle",
      fill: "#8a4a08", "font-size": 13.5, class: "fk-axis-label"
    }, g);
    lab.textContent = "d = " + FK.format(d, 3);

    // 肩关节（俯仰关节）圆心
    var sp = scene.project([0, 0, BASE_H]);
    scene.el("circle", { cx: sp.x, cy: sp.y, r: 7, fill: "#fff", stroke: C.y, "stroke-width": 3 }, gBody);
    return arm;
  }

  function drawArmAxis(yawDeg, pitchDeg, d, arm) {
    // 伸缩轴 X̂：与手臂重合，箭头指向末端
    var tip = FK.Vec.add([0, 0, BASE_H], FK.Vec.scale(arm.axisX, d + 0.30));
    seg([0, 0, BASE_H], tip, { stroke: C.x, "stroke-width": 3.2, "marker-end": "url(#f8X)" }, gAxes);
    if (state.showFrame && !state.compact) {
      var p = scene.project(tip);
      var t = scene.el("text", {
        x: 0, y: 18, fill: C.x, "font-size": 13.5, class: "fk-axis-label",
        "text-anchor": "middle"
      }, gAxes);
      t.textContent = "X\u0302 伸缩轴（移动副）";
      var rot = FK.format(-yawDeg, 2);
      t.setAttribute("transform", "translate(" + (p.x + 6).toFixed(2) + "," + (p.y - 6).toFixed(2) +
        ") rotate(" + rot + ")");
    }
  }

  function drawFrame(arm) {
    if (!state.showFrame) return;
    var L = 2.45;
    // 基坐标系 {A} 的两个水平轴沿地面网格（避免竖线把机器人罩住）
    seg([0, 0, 0], [L, 0, 0], { stroke: C.x, "stroke-width": 2.6, "marker-end": "url(#f8X)" }, gAxes);
    seg([0, 0, 0], [0, L, 0], { stroke: C.y, "stroke-width": 2.6, "marker-end": "url(#f8Y)" }, gAxes);
    seg([0, 0, 0], [0, 0, 2.55], { stroke: C.z, "stroke-width": 3.4, "marker-end": "url(#f8Z)" }, gAxes);
    put([L, 0, 0], "X\u0302\u2090", { fill: C.x, "font-size": 15, "font-style": "italic" }, 8, 2, gAxes);
    put([0, L, 0], "Y\u0302\u2090", { fill: C.y, "font-size": 15, "font-style": "italic" }, 8, 8, gAxes);
    put([0, 0, 2.55], "Z\u0302\u2090 回转轴", { fill: C.z, "font-size": 16, "font-style": "italic" }, 10, -8, gAxes);
    var o = scene.project([0, 0, 0]);
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.2, fill: "#334155" }, gAxes);
    var t = scene.el("text", { x: o.x - 22, y: o.y + 20, class: "fk-origin-label" }, gAxes);
    t.textContent = "O";
  }

  /** 工作空间提示：伸缩 d=0.4~2.0 × 俯仰 ±80° 的包络示意（只画关键几条，保持画面干净） */
  function drawWork(yawDeg, pitchDeg, d) {
    if (!state.showWork) return;
    var DMAX = 2.0, PMAX = 80;
    // 最大伸缩、沿俯仰范围扫出的两条经线（φ 与 φ+180°）
    curve(pitchArc(yawDeg, DMAX, -PMAX, PMAX, 60),
      { stroke: C.work, "stroke-width": 1.8, "stroke-dasharray": "4 6", opacity: 0.9 }, gWork);
    curve(pitchArc(yawDeg + 180, DMAX, -PMAX, PMAX, 60),
      { stroke: C.work, "stroke-width": 1.8, "stroke-dasharray": "4 6", opacity: 0.9 }, gWork);
    // 肩部高度处、最大伸缩的纬圆（回转可达范围）
    curve(yawCircle(DMAX, BASE_H, 0, 360, 72),
      { stroke: C.work, "stroke-width": 1.5, "stroke-dasharray": "3 6", opacity: 0.85 }, gWork);
    var uy = [Math.cos(yawDeg * FK.DEG), Math.sin(yawDeg * FK.DEG), 0];
    var labelAt = FK.Vec.scale(uy, DMAX * Math.cos(18 * FK.DEG));
    labelAt[2] = BASE_H + DMAX * Math.sin(18 * FK.DEG);
    put(labelAt, "工作空间提示 · d = 0.4~2.0、俯仰 ±80° 的包络（示意）",
      { fill: "#64748b", "font-size": 13 }, 10, 16, gWork);
  }

  /** 单变量运动轨迹弧线：回转（绕 Ẑ）、俯仰（绕 Ŷ）、伸缩（沿 X̂） */
  function drawSweep(yawDeg, pitchDeg, d, arm) {
    if (!state.showSweep) return;
    // 1) 回转轨迹：保持 θ、d 不变，φ 在限位内扫掠
    var z = BASE_H + d * Math.sin(pitchDeg * FK.DEG);
    var r = d * Math.cos(pitchDeg * FK.DEG);
    curve(yawCircle(r, z, -180, 180, 96), { stroke: C.trailYaw, "stroke-width": 2, "stroke-dasharray": "5 5", opacity: 0.55 }, gTrail);
    // 2) 伸缩轨迹：保持 φ、θ 不变，d 从 0.4 到 2.0
    var a = FK.Vec.add([0, 0, BASE_H], FK.Vec.scale(arm.axisX, 0.4));
    var b = FK.Vec.add([0, 0, BASE_H], FK.Vec.scale(arm.axisX, 2.0));
    seg(a, b, { stroke: C.x, "stroke-width": 2.4, "stroke-dasharray": "8 5", opacity: 0.7 }, gTrail);
    put(b, "沿 X\u0302 伸缩轨迹", { fill: C.x, "font-size": 13 }, 8, -12, gTrail);
  }

  /** 末端高度线与回转投影半径线 */
  function drawTip(arm, d) {
    var P = arm.tip;
    // 末端矢量
    seg([0, 0, 0], P, { stroke: C.tip, "stroke-width": 3.6, "marker-end": "url(#f8V)" }, gTip);
    // 末端点
    var p = scene.project(P);
    scene.el("circle", { cx: p.x, cy: p.y, r: 6.6, fill: C.tip, class: "fk-point" }, gTip);
    var t = scene.el("text", { x: p.x + 10, y: p.y - 14, fill: "#8a4a08", "font-size": 18, class: "fk-point-label" }, gTip);
    t.textContent = "P";
    // 高度线（z = h + d·sinθ）、地面投影点与回转投影半径
    seg([0, 0, P[2]], P, { stroke: "#94a3b8", "stroke-width": 1.4, "stroke-dasharray": "5 5" }, gTip);
    seg([P[0], P[1], 0], P, { stroke: "#94a3b8", "stroke-width": 1.4, "stroke-dasharray": "5 5" }, gTip);
    seg([0, 0, 0], [P[0], P[1], 0], { stroke: "#94a3b8", "stroke-width": 1.4, "stroke-dasharray": "5 5" }, gTip);
    seg([0, 0, 0], [0, 0, P[2]], { stroke: "#cbd5e1", "stroke-width": 1.2 }, gTip);
    var pr = Math.hypot(P[0], P[1]);
    if (pr > 0.05) {
      curve(yawCircle(pr, 0, 0, state.yaw, 48), { stroke: "#cbd5e1", "stroke-width": 1.2, "stroke-dasharray": "4 5" }, gTip);
    }
    put([P[0], P[1], 0], "r = d·cosθ", { fill: "#64748b", "font-size": 13 }, 6, 18, gTip);
    put([0, 0, P[2]], "z = h + d·sinθ", { fill: "#64748b", "font-size": 13 }, 10, -6, gTip);
  }

  /* ------------------------------------------------------------- 渲染 */

  function render() {
    var k;
    var layers = [gGrid, gWork, gTrail, gBody, gAxes, gTip];
    for (k = 0; k < layers.length; k += 1) layers[k].replaceChildren();

    // 地面网格
    var half = 2.6;
    var gg = scene.el("g", { class: "fk-grid" }, gGrid);
    for (var i = -2; i <= 2; i += 0.5) {
      scene.line([-half, i, 0], [half, i, 0], { class: "fk-grid-line" }, gg);
      scene.line([i, -half, 0], [i, half, 0], { class: "fk-grid-line" }, gg);
    }

    var arm = fk(state.yaw, state.pitch, state.ext);

    drawWork(state.yaw, state.pitch, state.ext);
    drawFrame(arm);
    drawBase();
    drawYawJoint(state.yaw);
    drawPitchJoint(state.yaw, state.pitch, state.ext, arm.armDir);
    drawSweep(state.yaw, state.pitch, state.ext, arm);
    drawArm(state.yaw, state.pitch, state.ext);
    drawArmAxis(state.yaw, state.pitch, state.ext, arm);
    drawTip(arm, state.ext);

    /* ---------------------------------------------------------- 读数 */
    var P = arm.tip;
    document.getElementById("yawOut").textContent = FK.deg(state.yaw, 1);
    document.getElementById("pitchOut").textContent = FK.deg(state.pitch, 1);
    document.getElementById("extOut").textContent = FK.format(state.ext, 3);
    document.getElementById("pxOut").textContent = FK.format(P[0], 3);
    document.getElementById("pyOut").textContent = FK.format(P[1], 3);
    document.getElementById("pzOut").textContent = FK.format(P[2], 3);
    document.getElementById("rOut").textContent = FK.format(state.ext * Math.cos(state.pitch * FK.DEG), 3);
    var note = document.getElementById("axisNote");
    note.className = "row small ok";
    note.textContent = "回转轴 Ẑ 竖直、俯仰轴 Ŷ 水平（θ 为手臂仰角）：球坐标型 = 2 转 1 移；"
      + "圆柱坐标型（图1.7）第二个自由度是沿 Ẑ 升降（1 转 2 移），没有俯仰轴。";
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "yaw", key: "yaw", value: DEFAULTS.yaw, format: function (v) { return FK.deg(v, 1); } },
    { id: "pitch", key: "pitch", value: DEFAULTS.pitch, format: function (v) { return FK.deg(v, 1); } },
    { id: "ext", key: "ext", value: DEFAULTS.ext, format: function (v) { return FK.format(v, 3); } }
  ], state, render);

  FK.bindToggles([
    { id: "showFrame", key: "showFrame" },
    { id: "showWork", key: "showWork" },
    { id: "showSweep", key: "showSweep" },
    {
      id: "auto", key: "auto", onChange: function (v) {
        scene.setAuto(v);
        if (v && !sweep.frame) sweep.frame = requestAnimationFrame(sweepTick);
        if (!v) { /* 关节不再自走，仅保留视角自转 */ }
      }
    }
  ], state, render);

  /* 自动演示：φ 往复回转 + θ 缓慢摆动，便于观察三个变量的作用 */
  function sweepTick() {
    sweep.frame = 0;
    if (!state.auto) return;
    state.yaw += 0.9 * sweep.dir;
    if (state.yaw > 180) { state.yaw = 180; sweep.dir = -1; }
    if (state.yaw < -180) { state.yaw = -180; sweep.dir = 1; }
    state.pitch = 40 * Math.sin(state.yaw * FK.DEG);
    document.getElementById("yaw").value = state.yaw;
    document.getElementById("pitch").value = state.pitch;
    document.getElementById("yawValue").textContent = FK.deg(state.yaw, 1);
    document.getElementById("pitchValue").textContent = FK.deg(state.pitch, 1);
    render();
    sweep.frame = requestAnimationFrame(sweepTick);
  }

  document.getElementById("reset").addEventListener("click", function () {
    state.yaw = DEFAULTS.yaw;
    state.pitch = DEFAULTS.pitch;
    state.ext = DEFAULTS.ext;
    state.showFrame = true;
    state.showWork = true;
    state.showSweep = true;
    state.auto = false;
    document.getElementById("showFrame").checked = true;
    document.getElementById("showWork").checked = true;
    document.getElementById("showSweep").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    fit();
    render();
  });

  window.addEventListener("resize", function () { fit(); render(); });
  window.addEventListener("load", function () { fit(); render(); });

  /* ------------------------------------------------------------- 自检 */
  (function selfTest() {
    function close(a, b, eps) { return Math.abs(a - b) < (eps === undefined ? 1e-9 : eps); }

    // 1) 三个变量取 0（φ=0、θ=0、d=0.4）时：手臂水平，末端 x = d、y = 0，z = 基座高度 h，
    //    “基座高度 + 手臂沿 Ẑ 的升高量（d·sinθ = 0） = 末端高度”这一关系成立
    var P0 = fk(0, 0, 0.4).tip;
    if (!close(P0[0], 0.4) || !close(P0[1], 0)) {
      throw new Error("图1-8 自检失败：φ=θ=0 时末端应为 (d,0,h) = (0.4,0,0.8)，实得 " + JSON.stringify(P0));
    }
    if (!close(P0[2], BASE_H + 0.4 * Math.sin(0))) {
      throw new Error("图1-8 自检失败：φ=θ=0 时末端 z 应为 h + d·sinθ = " + BASE_H + "，实得 " + P0[2]);
    }
    // 一般化：z = h + d·sinθ（竖直升高量），水平投影 = d·cosθ（题面要求的几何关系）
    var gen = [[0, 0, 0.4], [30, 40, 1.2], [-125, -80, 2.0], [180, 80, 0.4], [90, 12, 0.75]];
    for (var gi = 0; gi < gen.length; gi += 1) {
      var gk = fk(gen[gi][0], gen[gi][1], gen[gi][2]);
      if (!close(gk.tip[2], BASE_H + gen[gi][2] * Math.sin(gen[gi][1] * FK.DEG))) {
        throw new Error("图1-8 自检失败：z ≠ h + d·sinθ @case" + gi);
      }
      if (!close(Math.hypot(gk.tip[0], gk.tip[1]),
        Math.abs(gen[gi][2] * Math.cos(gen[gi][1] * FK.DEG)))) {
        throw new Error("图1-8 自检失败：水平投影 ≠ d·cosθ @case" + gi);
      }
    }

    // 2) 回转 360° 后末端回到原位
    var A1 = fk(37, 40, 1.2).tip;
    var A2 = fk(37 + 360, 40, 1.2).tip;
    if (!FK.Vec.eq(FK.Vec.round(A1, 12), FK.Vec.round(A2, 12), 1e-9)) {
      throw new Error("图1-8 自检失败：回转 360° 后末端未回到原位");
    }
    var A3 = fk(37 - 360, 40, 1.2).tip;
    if (!FK.Vec.eq(FK.Vec.round(A1, 12), FK.Vec.round(A3, 12), 1e-9)) {
      throw new Error("图1-8 自检失败：回转 −360° 后末端未回到原位");
    }

    // 3) 绕 Ŷ 俯仰：θ=0 时手臂水平（z = h、水平投影 = d）；θ=90° 时手臂竖直（水平投影 0、z = h+d）
    var B0 = fk(52, 0, 1.3).tip;
    if (!close(B0[2], BASE_H) || !close(Math.hypot(B0[0], B0[1]), 1.3)) {
      throw new Error("图1-8 自检失败：θ=0 时 z 应为 h 且水平投影应为 d");
    }
    var B90 = fk(52, 90, 1.3).tip;
    if (!close(Math.hypot(B90[0], B90[1]), 0, 1e-9) || !close(B90[2], BASE_H + 1.3)) {
      throw new Error("图1-8 自检失败：θ=90° 时末端应落在回转轴上（水平投影 0）");
    }
    // θ>0 必须“抬起”（z 随 θ 单调增）：方向不能反
    if (!(fk(0, 20, 1.2).tip[2] < fk(0, 60, 1.2).tip[2])) {
      throw new Error("图1-8 自检失败：θ 增大时末端高度必须增大（俯仰方向不能反）");
    }
    // 俯仰不改变 φ 所定义的方位角
    var phi0 = Math.atan2(B0[1], B0[0]);
    var phi90 = Math.atan2(fk(52, 33, 1.3).tip[1], fk(52, 33, 1.3).tip[0]);
    if (!close(phi0, phi90, 1e-12)) throw new Error("图1-8 自检失败：俯仰改变了方位角");

    // 4) 沿手臂方向的是移动副：伸缩轴方向 = Rot(Ẑ,φ)·Rot(Ŷ,−θ)·[1,0,0]ᵀ，
    //    且末端相对肩关节的位移始终与该轴平行、长度恒等于伸缩量 d
    var cases = [[0, 0, 0.4], [30, 40, 1.2], [-125, -80, 2.0], [180, 80, 0.4]];
    for (var i = 0; i < cases.length; i += 1) {
      var arm = fk(cases[i][0], cases[i][1], cases[i][2]);
      var rel = FK.Vec.sub(arm.tip, arm.shoulder);
      var cross = FK.Vec.cross(FK.Vec.normalize(rel), FK.Vec.normalize(arm.axisX));
      if (FK.Vec.len(cross) > 1e-12) {
        throw new Error("图1-8 自检失败：伸缩轴与手臂方向不重合（应为移动副）@case" + i);
      }
      if (!close(FK.Vec.len(rel), cases[i][2], 1e-9)) {
        throw new Error("图1-8 自检失败：末端到肩关节距离应恒等于伸缩长度 d @case" + i);
      }
      // θ = 0 时手臂必须水平（沿 X̂）
      if (cases[i][1] === 0 && !close(rel[2], 0)) {
        throw new Error("图1-8 自检失败：θ=0 时手臂应水平");
      }
      // 伸缩量只改变手臂长度，不改变方向
      var arm2 = fk(cases[i][0], cases[i][1], cases[i][2] + 0.3);
      var rel2 = FK.Vec.sub(arm2.tip, arm2.shoulder);
      var cross2 = FK.Vec.cross(FK.Vec.normalize(rel), FK.Vec.normalize(rel2));
      if (FK.Vec.len(cross2) > 1e-12) {
        throw new Error("图1-8 自检失败：改变伸缩量后手臂方向发生了变化 @case" + i);
      }
    }

    // 5) 默认参数下末端应与读数一致（θ=40°、d=1.2、φ=30°）
    var Pd = fk(30, 40, 1.2).tip;
    var expect = [1.2 * Math.cos(40 * FK.DEG) * Math.cos(30 * FK.DEG),
      1.2 * Math.cos(40 * FK.DEG) * Math.sin(30 * FK.DEG),
      BASE_H + 1.2 * Math.sin(40 * FK.DEG)];
    if (!FK.Vec.eq(FK.Vec.round(Pd, 9), FK.Vec.round(expect, 9), 1e-9)) {
      throw new Error("图1-8 自检失败：默认参数解析解不一致 → " + JSON.stringify(Pd));
    }

    // 6) 伸缩行程的两个极值（d=0.4 / 2.0）在 θ=0 时给出 h+0.4 与 h+2.0
    if (!close(fk(0, 0, 2.0).tip[2], BASE_H + 2.0)) {
      throw new Error("图1-8 自检失败：d=2.0、θ=0 时 z 应为 h+2.0");
    }
  }());

  fit();
  render();
}());
"""

FIGURE = {
    "id": "figure-1-8",
    "title": "图1-8 球坐标型机器人（绕Z回转·绕Y俯仰·沿X伸缩） · 人机交互演示",
    "css": CSS,
    "body": BODY,
    "script": SCRIPT,
}
