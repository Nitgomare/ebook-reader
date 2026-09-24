"""图3-20 一个3R腕部机构简图（克雷格《机器人学导论（第3版）》3.7 节 PUMA560 腕部）。

教材依据：
- 正文 3.7 节（PUMA560）："这台机器人与许多工业机器人一样，关节4、5和6的轴线相交于同一点，
  并且交点与坐标系 {4}、{5}、{6}的原点重合，而且关节轴4、5、6相互垂直。
  图3-20所示为机器人腕部机构的运动简图。"
  （图3-20 图注："一个3R腕部机构简图，三个轴相互垂直并相交于一点，这种设计用于PUMA560和许多工业机器人中"）
- 连杆参数表（图3-21）：α3 = −90°、α4 = +90°、α5 = −90°，d5 = d6 = 0，
  a3 ≈ 0（很小），d4 为前臂轴线长度。本图按改进型（克雷格）D-H 建模：
  ᵢ⁻¹ᵢT = Rx(α_{i-1})·Dx(a_{i-1})·Rz(θᵢ)·Dz(dᵢ)。
- 式(3-9) 的腕部部分：
    ₄³T = [[c4, −s4, 0, a3], [0, 0, 1, d4], [−s4, −c4, 0, 0]]
    ₅⁴T = [[c5, −s5, 0, 0], [0, 0, −1, 0], [s5, c5, 0, 0]]
    ₆⁵T = [[c6, −s6, 0, 0], [0, 0, 1, 0], [−s6, −c6, 0, 0]]
- 式(3-10)：₆⁴T = ₅⁴T·₆⁵T，其第 3 列（Ẑ₆ 在 {4} 中的表达）为 (−s5, 0, c5)：
  θ5 = 0° 或 ±180° 时 Ẑ₆ ∥ Ẑ₄ —— 关节4 与关节6 转轴重合，θ4 与 θ6 解耦失败，
  末端姿态只由 θ4+θ6 决定。这就是腕部奇异位形。
- 式(3-11)：₆³T = ₄³T·₆⁴T（脚本内与 D-H 连乘结果逐元素对照，作为数值自检）。

建模说明：本图取 a3 = 0（PUMA560 中 a3 ≈ 0.02 m，相对 d4 很小），使三轴严格交于一点，
d4 表示坐标系 {3} 原点到腕心的距离；工具坐标系 {T} 由 {6} 沿 Ẑ₆ 平移工具长度 L_T 得到。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="3R腕部机构简图：三个关节轴两两垂直并相交于腕心 O">
  <defs>
    <marker id="mJ4" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="mJ5" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
    <marker id="mJ6" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="mX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="mY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="mZ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="mDim" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#334155"></path>
    </marker>
  </defs>
  <g id="ground"></g>
  <g id="links"></g>
  <g id="axes"></g>
  <g id="arcs"></g>
  <g id="frames"></g>
  <g id="tool"></g>
  <g id="overlay"></g>
</svg>

<section class="panel" aria-label="图3-20 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3-20 3R 腕部机构（三轴交于一点）</h1>
      <p class="subtitle">PUMA560 腕部：关节轴 4、5、6 依次垂直并相交于腕心 O（{4}{5}{6} 原点重合）。
        θ₅ = 0° 或 ±180° 时轴4 与轴6 共线，θ₄ 与 θ₆ 解耦失败。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>
  <div class="control">
    <div class="control-head"><label for="t4">关节角 θ₄（绕轴4 Ẑ₄）</label><output id="t4Value">0.0°</output></div>
    <input id="t4" type="range" min="-180" max="180" step="1" value="0">
  </div>
  <div class="control">
    <div class="control-head"><label for="t5">关节角 θ₅（绕轴5 Ẑ₅）</label><output id="t5Value">0.0°</output></div>
    <input id="t5" type="range" min="-180" max="180" step="1" value="0">
  </div>
  <div class="control">
    <div class="control-head"><label for="t6">关节角 θ₆（绕轴6 Ẑ₆）</label><output id="t6Value">0.0°</output></div>
    <input id="t6" type="range" min="-180" max="180" step="1" value="0">
  </div>
  <div class="control">
    <div class="control-head"><label for="tool">工具长度 L_T（{6}→{T}）</label><output id="toolValue">0.00</output></div>
    <input id="tool" type="range" min="0" max="1.2" step="0.05" value="0">
  </div>
  <div class="options">
    <label><input id="showFrames" type="checkbox" checked>显示坐标系</label>
    <label><input id="showArcs" type="checkbox" checked>显示转角圆弧</label>
    <label><input id="showGrid" type="checkbox" checked>显示底面网格</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>
  <div class="legend">
    <span><i style="background:#7c3aed"></i>关节4轴 Ẑ₄</span>
    <span><i style="background:#0e7490"></i>关节5轴 Ẑ₅</span>
    <span><i style="background:#c26a10"></i>关节6轴 Ẑ₆</span>
    <span><i style="background:#334155"></i>工具 / 法兰</span>
    <span><i class="dot" style="background:#dc2626"></i>奇异位形提示</span>
    <span>坐标系轴：<i style="background:#d93025"></i>Ẋ <i style="background:#2563eb"></i>Ẏ <i style="background:#12944f"></i>Ẑ</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row"><strong>θ₄, θ₅, θ₆</strong> = <span id="q4">0.0°</span>, <span id="q5">0.0°</span>, <span id="q6">0.0°</span></div>
  <div class="row small">腕部姿态矩阵 ³₆R（相对坐标系 {3}，式(3-11)）：</div>
  <div class="row mat">[ <span id="m00">1.000</span><span id="m01">0.000</span><span id="m02">0.000</span> ]</div>
  <div class="row mat">[ <span id="m10">0.000</span><span id="m11">0.000</span><span id="m12">1.000</span> ]</div>
  <div class="row mat">[ <span id="m20">0.000</span><span id="m21">-1.000</span><span id="m22">0.000</span> ]</div>
  <div class="row small">工具轴 Ẑ_T（{3} 中）= [<span id="ztx">0.000</span>, <span id="zty">1.000</span>, <span id="ztz">0.000</span>]ᵀ = [−c₄s₅, c₅, s₄s₅]</div>
  <div class="row small">轴4⊥轴5、轴5⊥轴6 恒为 90.0°；轴4–轴6 夹角 acos(Ẑ₄·Ẑ₆) = <span id="ang46">0.0°</span></div>
  <div class="row" id="singRow">…</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var L = {
    ground: document.getElementById("ground"),
    links: document.getElementById("links"),
    axes: document.getElementById("axes"),
    arcs: document.getElementById("arcs"),
    frames: document.getElementById("frames"),
    tool: document.getElementById("tool"),
    overlay: document.getElementById("overlay")
  };

  var D4 = 1.60;      // 坐标系 {3} 原点到腕心的距离（对应 PUMA560 的 d4）
  var FLANGE = 0.58;  // 腕心到法兰面（L_T = 0 时 {T} 的位置）
  var BASE_SCALE = 74;

  var scene = new FK.Scene({
    svg: viewport, origin: { x: 548, y: 300 }, scale: BASE_SCALE, yaw: -0.62, pitch: 0.34
  });
  var state = { t4: 0, t5: 0, t6: 0, tool: 0, showFrames: true, showArcs: true, showGrid: true };

  var COL = {
    j4: "#7c3aed", j5: "#0e7490", j6: "#c26a10",
    x: "#d93025", y: "#2563eb", z: "#12944f",
    link: "#94a3b8", linkDark: "#475569", tool: "#334155",
    warn: "#dc2626", muted: "#64748b", grid: "#e2eaf5"
  };

  /* --- 改进型（克雷格）D-H：ᵢ⁻¹ᵢT = Rx(α) · Dx(a) · Rz(θ) · Dz(d) --- */
  function dh(alpha, a, d, theta) {
    return FK.M4.chain(
      FK.M4.rotX(alpha),
      FK.M4.translate([a, 0, 0]),
      FK.M4.rotZ(theta),
      FK.M4.translate([0, 0, d])
    );
  }

  /* 显示变换：把 {3} 中的 Ẑ₄（= Ŷ₃，前臂轴线）转到屏幕竖直向上，并把腕心移到显示原点 */
  var DSP = FK.M4.chain(FK.M4.rotX(Math.PI / 2), FK.M4.translate([0, -D4, 0]));

  function pose(t4, t5, t6) {
    var T34 = dh(-Math.PI / 2, 0, D4, t4 * FK.DEG);
    var T45 = dh(Math.PI / 2, 0, 0, t5 * FK.DEG);
    var T56 = dh(-Math.PI / 2, 0, 0, t6 * FK.DEG);
    var T36 = FK.M4.chain(T34, T45, T56);
    return {
      T36: T36,
      R36: FK.M4.rotation(T36),
      W4: FK.M4.multiply(DSP, T34),
      W5: FK.M4.multiply(DSP, FK.M4.multiply(T34, T45)),
      W6: FK.M4.multiply(DSP, T36)
    };
  }

  /* ---------------------------------------------------------------- 绘图工具 */
  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    return scene.el("line", Object.assign({ x1: A.x, y1: A.y, x2: B.x, y2: B.y }, attrs || {}), parent);
  }
  function tag(v, str, attrs, dx, dy, parent) {
    var p = scene.project(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0),
      "font-size": 15, "font-weight": 700, class: "fk-axis-label"
    }, attrs || {}), parent);
    node.textContent = str;
    return node;
  }
  function dir(M, v) { return FK.M4.applyDir(M, v); }
  function zAxis(M) { return dir(M, [0, 0, 1]); }
  function xAxis(M) { return dir(M, [1, 0, 0]); }
  function yAxis(M) { return dir(M, [0, 1, 0]); }
  function at(o, d, l) { return FK.Vec.add(o, FK.Vec.scale(d, l)); }

  function drawGrid() {
    var z = -2.25, half = 1.0, step = 0.5, v;
    for (v = -half; v <= half + 1e-9; v += step) {
      seg([-half, v, z], [half, v, z], { stroke: COL.grid, "stroke-width": 1 }, L.ground);
      seg([v, -half, z], [v, half, z], { stroke: COL.grid, "stroke-width": 1 }, L.ground);
    }
  }

  /* 前臂（与关节4轴同轴的一段）+ 断口标记 */
  function drawForearm() {
    seg([0, 0, -2.30], [0, 0, -0.42], { stroke: "#cbd5e1", "stroke-width": 17, "stroke-linecap": "round" }, L.links);
    seg([0, 0, -2.30], [0, 0, -0.42], { stroke: "#eef3f9", "stroke-width": 9, "stroke-linecap": "round" }, L.links);
    seg([-0.14, 0, -0.50], [0.14, 0, -0.50], { stroke: COL.linkDark, "stroke-width": 2.4 }, L.links);
    tag([0, 0, -2.10], "前臂（与轴4 同轴）", { fill: COL.muted, "font-size": 14, "text-anchor": "end" }, -16, 6, L.links);
  }

  /* 关节体（短粗半透明鼓形）+ 双箭头虚线轴 */
  function drum(o, d, half, color) {
    seg(at(o, d, -half), at(o, d, half),
      { stroke: color, "stroke-width": 24, "stroke-linecap": "round", opacity: 0.18 }, L.axes);
  }
  function drawJointAxis(o, d, half, color, marker, text, dx, dy, anchor) {
    seg(at(o, d, -half), at(o, d, half), {
      stroke: color, "stroke-width": 2.6, "stroke-dasharray": "11 7",
      "marker-start": "url(#" + marker + ")", "marker-end": "url(#" + marker + ")"
    }, L.axes);
    tag(at(o, d, half), text, { fill: color, "text-anchor": anchor || "start" }, dx, dy, L.axes);
  }

  /* 坐标系：默认只画 X、Y 细轴（Z 轴即关节轴，已单独画出）；labeled 时再加文字 */
  function drawFrame(M, len, prefix, full, labeled) {
    var o = FK.M4.position(M);
    var xe = at(o, xAxis(M), len);
    var ye = at(o, yAxis(M), len);
    seg(o, xe, { stroke: COL.x, "stroke-width": 1.9, "marker-end": "url(#mX)" }, L.frames);
    seg(o, ye, { stroke: COL.y, "stroke-width": 1.9, "marker-end": "url(#mY)" }, L.frames);
    if (labeled) {
      tag(xe, "Ẋ" + prefix, { fill: COL.x, "font-size": 12.5 }, 5, 4, L.frames);
      tag(ye, "Ẏ" + prefix, { fill: COL.y, "font-size": 12.5 }, 5, 4, L.frames);
    }
    if (full) {
      var ze = at(o, zAxis(M), len * 0.92);
      seg(o, ze, { stroke: COL.z, "stroke-width": 1.9, "marker-end": "url(#mZ)" }, L.frames);
      if (labeled) tag(ze, "Ẑ" + prefix, { fill: COL.z, "font-size": 12.5 }, 5, 4, L.frames);
    }
  }

  /* 绕 dirZ 从 dirX0 转到 dirX 的圆弧（含 θ 标签；θ=0 时只画参考刻线） */
  function rotArc(o, dirZ, dirX0, dirX, radius, color, name, lx, ly) {
    var u = FK.Vec.normalize(dirX0);
    var w = FK.Vec.normalize(dirZ);
    var v = FK.Vec.cross(w, u);
    var ang = Math.atan2(FK.Vec.dot(dirX, v), FK.Vec.dot(dirX, u));
    if (Math.abs(ang) < 0.006) {
      seg(at(o, u, radius * 0.9), at(o, u, radius * 1.06), { stroke: color, "stroke-width": 2.2, opacity: 0.75 }, L.arcs);
    } else {
      var steps = Math.max(8, Math.round(Math.abs(ang) / 0.07));
      var pts = [], i, t;
      for (i = 0; i <= steps; i += 1) {
        t = ang * (i / steps);
        pts.push(FK.Vec.add(o, FK.Vec.add(FK.Vec.scale(u, radius * Math.cos(t)), FK.Vec.scale(v, radius * Math.sin(t)))));
      }
      scene.polyline(pts, { stroke: color, class: "fk-arc" }, L.arcs);
    }
    var mid = ang * 0.5;
    tag(FK.Vec.add(o, FK.Vec.add(
      FK.Vec.scale(u, radius * 1.26 * Math.cos(mid)),
      FK.Vec.scale(v, radius * 1.26 * Math.sin(mid))
    )), name, { fill: color, "font-size": 16, "text-anchor": "middle" }, lx || 0, (ly || 0) + 5, L.arcs);
  }

  /* 屏幕空间尺寸标注（双箭头） */
  function dimLine(a, b, offset, text, color) {
    var A = scene.project(a), B = scene.project(b);
    var dx = B.x - A.x, dy = B.y - A.y, len = Math.sqrt(dx * dx + dy * dy);
    if (len < 6) return;
    var nx = -dy / len, ny = dx / len;
    var ax = A.x + nx * offset, ay = A.y + ny * offset;
    var bx = B.x + nx * offset, by = B.y + ny * offset;
    scene.el("line", {
      x1: ax, y1: ay, x2: bx, y2: by, stroke: color,
      "stroke-width": 1.6, "marker-start": "url(#mDim)", "marker-end": "url(#mDim)"
    }, L.tool);
    var t = scene.el("text", {
      x: (ax + bx) / 2 + nx * 14, y: (ay + by) / 2 + ny * 14 + 5,
      "text-anchor": "middle", fill: color, "font-size": 13.5,
      "font-weight": 700, class: "fk-axis-label"
    }, L.tool);
    t.textContent = text;
  }

  /* ------------------------------------------------------------------ 渲染 */
  function render() {
    var k;
    for (k in L) { if (Object.prototype.hasOwnProperty.call(L, k)) L[k].replaceChildren(); }

    var t4 = state.t4, t5 = state.t5, t6 = state.t6;
    var P = pose(t4, t5, t6);
    var O = [0, 0, 0];                       // 腕心：{4}{5}{6} 原点，三轴交点
    var z4 = zAxis(P.W4), z5 = zAxis(P.W5), z6 = zAxis(P.W6);

    if (state.showGrid) drawGrid();
    drawForearm();

    drum(O, z4, 0.32, COL.j4);
    drum(O, z5, 0.27, COL.j5);
    drum(O, z6, 0.24, COL.j6);

    drawJointAxis(O, z4, 1.45, COL.j4, "mJ4", "关节4轴 Ẑ₄（θ₄）", -18, -10, "end");
    drawJointAxis(O, z5, 1.32, COL.j5, "mJ5", "关节5轴 Ẑ₅（θ₅）", -16, 20, "end");
    drawJointAxis(O, z6, 1.32, COL.j6, "mJ6", "关节6轴 Ẑ₆（θ₆）", -16, 20, "end");

    var op = scene.project(O);
    scene.el("circle", { cx: op.x, cy: op.y, r: 7.5, fill: "#1e293b", stroke: "#fff", "stroke-width": 2.4 }, L.axes);
    tag(O, "O", { fill: "#334155", "font-size": 15 }, -18, 22, L.axes);

    if (state.showArcs) {
      var P0 = pose(0, t5, t6);
      var P5 = pose(t4, 0, t6);
      var P6 = pose(t4, t5, 0);
      rotArc(O, z4, xAxis(P0.W4), xAxis(P.W4), 1.06, COL.j4, "θ₄", 0, -12);
      rotArc(O, z5, xAxis(P5.W5), xAxis(P.W5), 0.80, COL.j5, "θ₅", -12, 10);
      rotArc(O, z6, xAxis(P6.W6), xAxis(P.W6), 0.56, COL.j6, "θ₆", 12, 8);
    }

    if (state.showFrames) {
      drawFrame(DSP, 0.40, "₃", true, true);
      drawFrame(P.W4, 0.62, "₄", false, false);
      drawFrame(P.W5, 0.54, "₅", false, false);
      drawFrame(P.W6, 0.46, "₆", false, false);
    }

    var tip = at(O, z6, FLANGE + state.tool);
    var flangeEnd = at(O, z6, FLANGE);
    seg(at(O, z6, 0.34), flangeEnd, { stroke: "#94a3b8", "stroke-width": 17, "stroke-linecap": "round" }, L.tool);
    if (state.tool > 0.001) {
      seg(at(O, z6, FLANGE - 0.08), tip, { stroke: COL.tool, "stroke-width": 9, "stroke-linecap": "round" }, L.tool);
      dimLine(flangeEnd, tip, 30, "L_T = " + FK.format(state.tool, 2), "#334155");
    }
    if (state.showFrames) {
      drawFrame(FK.M4.multiply(P.W6, FK.M4.translate([0, 0, FLANGE + state.tool])), 0.36, "T", false, true);
    }    var tp = scene.project(tip);
    scene.el("circle", { cx: tp.x, cy: tp.y, r: 5.4, fill: "#0f172a", stroke: "#fff", "stroke-width": 2 }, L.tool);
    tag(tip, "工具坐标系 {T}", { fill: "#0f172a", "font-size": 14, "text-anchor": "end" }, -16, -6, L.tool);

    /* 奇异位形反馈 */
    var c5 = FK.Vec.dot(z4, z6);
    var ang46 = Math.acos(Math.max(-1, Math.min(1, c5))) / FK.DEG;
    var sing = Math.abs(t5) <= 2 || Math.abs(t5) >= 178;
    if (sing) {
      seg(at(O, z4, -1.55), at(O, z4, 1.55),
        { stroke: COL.warn, "stroke-width": 10, "stroke-linecap": "round", opacity: 0.20 }, L.overlay);
      scene.el("circle", {
        cx: op.x, cy: op.y, r: 30, fill: "none", stroke: COL.warn,
        "stroke-width": 3, "stroke-dasharray": "7 6"
      }, L.overlay);
      var wp = scene.project(at(O, z4, 1.60));
      scene.el("text", {
        x: wp.x + 18, y: wp.y - 14, "text-anchor": "start", fill: COL.warn,
        "font-size": 16.5, "font-weight": 700, class: "fk-axis-label"
      }, L.overlay).textContent = "⚠ 轴4 与 轴6 共线";
      scene.el("text", {
        x: wp.x + 18, y: wp.y + 8, "text-anchor": "start", fill: COL.warn,
        "font-size": 14, "font-weight": 700, class: "fk-axis-label"
      }, L.overlay).textContent = "θ₄ 与 θ₆ 解耦失败";
    }

    /* ---------------------------------------------------------------- 读数 */
    var R = P.R36;
    document.getElementById("q4").textContent = FK.deg(t4, 1);
    document.getElementById("q5").textContent = FK.deg(t5, 1);
    document.getElementById("q6").textContent = FK.deg(t6, 1);
    document.getElementById("m00").textContent = FK.format(R[0], 3);
    document.getElementById("m01").textContent = FK.format(R[1], 3);
    document.getElementById("m02").textContent = FK.format(R[2], 3);
    document.getElementById("m10").textContent = FK.format(R[3], 3);
    document.getElementById("m11").textContent = FK.format(R[4], 3);
    document.getElementById("m12").textContent = FK.format(R[5], 3);
    document.getElementById("m20").textContent = FK.format(R[6], 3);
    document.getElementById("m21").textContent = FK.format(R[7], 3);
    document.getElementById("m22").textContent = FK.format(R[8], 3);
    var zt = FK.M4.applyDir(P.T36, [0, 0, 1]);
    document.getElementById("ztx").textContent = FK.format(zt[0], 3);
    document.getElementById("zty").textContent = FK.format(zt[1], 3);
    document.getElementById("ztz").textContent = FK.format(zt[2], 3);
    document.getElementById("ang46").textContent = FK.deg(ang46, 1);

    var row = document.getElementById("singRow");
    if (sing) {
      row.className = "row warn";
      row.textContent = "⚠ 奇异：轴4 与轴6 共线（θ₅ = " + FK.deg(t5, 0) + "），θ₄ 与 θ₆ 解耦失败 —— 姿态只由 θ₄+θ₆ = "
        + FK.deg(t4 + t6, 1) + " 决定";
    } else {
      row.className = "row ok";
      row.textContent = "✓ 非奇异：轴4–轴6 夹角 " + FK.deg(ang46, 1) + " > 0，θ₄ 与 θ₆ 各自独立可解";
    }
  }

  /* --------------------------------------------------------------- 布局 */
  function layout() {
    var w = viewport.clientWidth || window.innerWidth;
    var h = viewport.clientHeight || window.innerHeight;
    if (w / h < 1.05) {
      // 竖屏：改用竖版 viewBox，避免图形被底部面板与右上读数卡遮挡
      viewport.setAttribute("viewBox", "0 0 420 800");
      viewport.setAttribute("preserveAspectRatio", "xMidYMin meet");
      scene.baseOrigin = { x: 210, y: 318 };
    } else {
      viewport.setAttribute("viewBox", "0 0 1000 620");
      viewport.setAttribute("preserveAspectRatio", "xMidYMid meet");
      scene.baseOrigin = { x: 548, y: 300 };
    }
    scene.state.scale = BASE_SCALE;
    scene.defaults.scale = BASE_SCALE;
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "t4", key: "t4", value: 0, format: function (v) { return FK.deg(v, 1); } },
    { id: "t5", key: "t5", value: 0, format: function (v) { return FK.deg(v, 1); } },
    { id: "t6", key: "t6", value: 0, format: function (v) { return FK.deg(v, 1); } },
    { id: "tool", key: "tool", value: 0, format: function (v) { return FK.format(v, 2); } }
  ], state, render);

  FK.bindToggles([
    { id: "showFrames", key: "showFrames" },
    { id: "showArcs", key: "showArcs" },
    { id: "showGrid", key: "showGrid" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.t4 = 0; state.t5 = 0; state.t6 = 0; state.tool = 0;
    state.showFrames = true; state.showArcs = true; state.showGrid = true; state.auto = false;
    document.getElementById("showFrames").checked = true;
    document.getElementById("showArcs").checked = true;
    document.getElementById("showGrid").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    layout();
    render();
  });

  window.addEventListener("resize", function () { layout(); render(); });

  /* --------------------------------------------------------------- 自检 */
  (function selfTest() {
    function eq(a, b, eps) { return Math.abs(a - b) < (eps === undefined ? 1e-9 : eps); }

    // 1) 教材式(3-10)：₆⁴T = ₅⁴T·₆⁵T
    var a4 = 40 * FK.DEG, a5 = 35 * FK.DEG, a6 = 25 * FK.DEG;
    var c4 = Math.cos(a4), s4 = Math.sin(a4);
    var c5 = Math.cos(a5), s5 = Math.sin(a5);
    var c6 = Math.cos(a6), s6 = Math.sin(a6);
    var T45 = dh(Math.PI / 2, 0, 0, a5);
    var T46 = FK.M4.chain(T45, dh(-Math.PI / 2, 0, 0, a6));
    var exp46 = [
      c5 * c6, -c5 * s6, -s5, 0,
      s6, c6, 0, 0,
      s5 * c6, -s5 * s6, c5, 0,
      0, 0, 0, 1
    ];
    var i;
    for (i = 0; i < 16; i += 1) {
      if (!eq(T46[i], exp46[i])) throw new Error("式(3-10) 自检失败 @" + i + "：" + T46[i]);
    }

    // 2) 教材式(3-11)：₆³T = ₄³T·₆⁴T（a₃ = 0）
    var T34 = dh(-Math.PI / 2, 0, D4, a4);
    var T36 = FK.M4.chain(T34, T46);
    var exp36 = [
      c4 * c5 * c6 - s4 * s6, -c4 * c5 * s6 - s4 * c6, -c4 * s5, 0,
      s5 * c6, -s5 * s6, c5, D4,
      -s4 * c5 * c6 - c4 * s6, s4 * c5 * s6 - c4 * c6, s4 * s5, 0,
      0, 0, 0, 1
    ];
    for (i = 0; i < 16; i += 1) {
      if (!eq(T36[i], exp36[i])) throw new Error("式(3-11) 自检失败 @" + i + "：" + T36[i]);
    }

    // 3) 三轴交于一点：{4}{5}{6} 原点重合，且等于腕心 (0, d4, 0)
    var W4 = dh(-Math.PI / 2, 0, D4, 53 * FK.DEG);
    var W5 = FK.M4.chain(W4, dh(Math.PI / 2, 0, 0, -21 * FK.DEG));
    var o4 = FK.M4.position(W4);
    var o5 = FK.M4.position(W5);
    var o6 = FK.M4.position(T36);
    if (!FK.Vec.eq(o4, o5, 1e-12) || !FK.Vec.eq(o5, o6, 1e-12)) throw new Error("三轴交点自检失败");
    if (!FK.Vec.eq(o6, [0, D4, 0], 1e-12)) throw new Error("腕心位置自检失败：" + JSON.stringify(o6));

    // 4) 两两垂直：轴4⊥轴5、轴5⊥轴6；轴4–轴6 夹角 = |θ₅|
    var q = pose(31, -47, 62);
    if (!eq(FK.Vec.dot(zAxis(q.W4), zAxis(q.W5)), 0, 1e-12)) throw new Error("轴4⊥轴5 自检失败");
    if (!eq(FK.Vec.dot(zAxis(q.W5), zAxis(q.W6)), 0, 1e-12)) throw new Error("轴5⊥轴6 自检失败");
    if (!eq(Math.acos(Math.max(-1, Math.min(1, FK.Vec.dot(zAxis(q.W4), zAxis(q.W6))))) / FK.DEG, 47, 1e-9)) {
      throw new Error("轴4–轴6 夹角应等于 |θ₅|");
    }

    // 5) 腕部奇异：θ₅ = 0° 与 ±180° 时 Ẑ₆ ∥ Ẑ₄（共线）
    var s0 = pose(63, 0, -28);
    var s180 = pose(63, 180, -28);
    if (FK.Vec.len(FK.Vec.cross(zAxis(s0.W4), zAxis(s0.W6))) > 1e-12) throw new Error("θ₅=0 应共线");
    if (FK.Vec.len(FK.Vec.cross(zAxis(s180.W4), zAxis(s180.W6))) > 1e-12) throw new Error("θ₅=180° 应共线");

    // 6) θ₅ = 0 时末端姿态只由 θ₄+θ₆ 决定（两组不同 θ₄、θ₆ 但和为 55° 的姿态应相同）
    var g1 = pose(20, 0, 35);
    var g2 = pose(-15, 0, 70);
    for (i = 0; i < 9; i += 1) {
      if (!eq(g1.R36[i], g2.R36[i], 1e-12)) throw new Error("θ₅=0 时应只取决于 θ₄+θ₆");
    }
  }());

  layout();
  render();
}());
"""

FIGURE = {
    "id": "figure-3-20",
    "title": "图3-20 3R 腕部机构（三轴交于一点） · 人机交互演示",
    "css": COMMON_CSS + """
.readout .row { white-space: normal; }
.readout .mat { font: 13px/1.6 ui-monospace, SFMono-Regular, Consolas, monospace; letter-spacing: 0.2px; }
.readout .mat span { display: inline-block; width: 4.9em; text-align: right; }
.readout .warn { color: #b91c1c; font-weight: 700; }
.readout .ok { color: #15803d; }
@media (max-width: 720px) {
  .readout { padding: 7px 10px; font-size: 12px; }
  .readout .small { font-size: 10.5px; }
  .readout .mat { font-size: 10.5px; }
  .readout .mat span { width: 4.1em; }
  .readout .warn { font-weight: 600; }
}
""",
    "body": BODY,
    "script": SCRIPT,
}
