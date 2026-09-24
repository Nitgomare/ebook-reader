"""图3-20 机器人运动学逆解多解性示意图（《机器人技术基础（第三版）》3.5.1 一、多解性）。

教材依据：
- 式(3.24)：末端连杆位姿 = A1A2A3A4A5A6；给定末端位姿求关节变量即运动学逆解。
- 3.5.1 正文原话：“机器人的运动学逆解具有多解性，如图3.20所示，对于给定的位置与姿态，
  它具有两组解。”“造成机器人运动学逆解具有多解的原因是由于解反三角函数方程产生的。”
- 本图用二自由度平面关节臂（2R）作最小可解模型：对同一目标点 (x, y)，
  由余弦定理 cθ2 = (r² − l1² − l2²)/(2 l1 l2) 得 θ2 = ±acos(cθ2)，
  两个符号分别对应“肘上解”与“肘下解”（即教材所说的两组解）。
- 目标姿态 φ 由平面臂自协调条件 φ = θ1 + θ2 保证（绕 Ẑ 转动的 2R 臂可实现任意平面姿态）。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.legend i.dash { background-image: repeating-linear-gradient(90deg, #fff 0 3px, transparent 3px 6px); background-color: transparent; }
.readout .row.is-warn { color: #b3261e; }
.panel-head .reset { box-sizing: border-box; white-space: nowrap; }
.panel h1 { overflow-wrap: anywhere; }
@media (max-width: 720px) {
  .panel { padding: 9px 11px; }
  .panel h1 { font-size: 13.5px; }
  .control { margin-top: 4px; }
  .control label { font-size: 12px; }
  .control output { font-size: 12px; }
  input[type="range"] { margin: 3px 0 0; height: 3px; }
  input[type="range"]::-webkit-slider-thumb { width: 14px; height: 14px; }
  .options, .legend { margin-top: 6px; padding-top: 5px; gap: 4px 9px; }
  .options label, .legend { font-size: 11px; }
  .tabs { margin-bottom: 5px; }
  .tabs button { padding: 5px 1px; font-size: 11.5px; }
  .readout {
    padding: 6px 8px; font-size: 11.5px; line-height: 1.45;
    max-width: min(300px, calc(100% - 16px));
  }
  .readout .small { font-size: 10.5px; }
  .readout .row { white-space: normal; }
  .readout .row:nth-child(5), .readout .row:nth-child(6) { display: none; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 640" preserveAspectRatio="none"
     role="img" aria-label="机器人运动学逆解多解性示意图">
  <defs>
    <marker id="arT" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
    <marker id="arA" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="arB" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="arAX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.2" markerHeight="5.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"></path>
    </marker>
    <marker id="arWarn" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
  </defs>
  <g id="gGrid"></g>
  <g id="gWork"></g>
  <g id="gArm2"></g>
  <g id="gArm1"></g>
  <g id="gTarget"></g>
  <g id="gMarks"></g>
</svg>

<section class="panel" aria-label="图3-20 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3-20 逆解多解性</h1>
      <p class="subtitle">同一目标点，反三角函数给出两组关节解：θ₂ 取正号与负号各一组，分别对应肘上 / 肘下构型。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>
  <div class="tabs" id="modeTabs">
    <button type="button" data-mode="up">肘上解</button>
    <button type="button" data-mode="down">肘下解</button>
    <button type="button" data-mode="both" class="is-active">两解并显</button>
  </div>
  <div class="control">
    <div class="control-head"><label for="tx">目标点 x</label><output id="txValue">0.60</output></div>
    <input id="tx" type="range" min="-1.5" max="1.5" step="0.01" value="0.6">
  </div>
  <div class="control">
    <div class="control-head"><label for="ty">目标点 y</label><output id="tyValue">0.45</output></div>
    <input id="ty" type="range" min="-1.5" max="1.5" step="0.01" value="0.45">
  </div>
  <div class="control">
    <div class="control-head"><label for="phi">目标姿态 φ</label><output id="phiValue">0.0°</output></div>
    <input id="phi" type="range" min="-180" max="180" step="1" value="0">
  </div>
  <div class="control">
    <div class="control-head"><label for="l1">连杆长 l₁</label><output id="l1Value">0.50</output></div>
    <input id="l1" type="range" min="0.2" max="0.9" step="0.01" value="0.5">
  </div>
  <div class="control">
    <div class="control-head"><label for="l2">连杆长 l₂</label><output id="l2Value">0.50</output></div>
    <input id="l2" type="range" min="0.2" max="0.9" step="0.01" value="0.5">
  </div>
  <div class="options">
    <label><input id="showWork" type="checkbox" checked>显示可达工作空间</label>
    <label><input id="showFrame" type="checkbox" checked>显示目标坐标系</label>
    <label><input id="showLink" type="checkbox" checked>显示构型标注</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>
  <div class="legend">
    <span><i style="background:#2563eb"></i>肘上解（θ₂&gt;0，实线）</span>
    <span><i class="dash" style="background:#c26a10"></i>肘下解（θ₂&lt;0，虚线）</span>
    <span><i class="dot" style="background:#d93025"></i>目标点 (x, y)</span>
    <span><i style="background:#0e7490"></i>目标姿态 φ</span>
    <span><i class="dash" style="background:#94a3b8"></i>可达工作空间边界</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row" id="statusRow"><strong>状态</strong>：<span id="status">正常</span></div>
  <div class="row"><strong>目标点</strong>：( <span id="tvx">0.60</span>, <span id="tvy">0.45</span> ) m，姿态 φ = <span id="tvphi">0.0°</span></div>
  <div class="row"><strong>肘上解</strong> θ₁ = <span id="up1">—</span>，θ₂ = <span id="up2">—</span>，φ = <span id="up3">—</span></div>
  <div class="row"><strong>肘下解</strong> θ₁ = <span id="dn1">—</span>，θ₂ = <span id="dn2">—</span>，φ = <span id="dn3">—</span></div>
  <div class="row small">两组末端位置：<span id="sameMsg">—</span>（φ 为各自的 θ₁+θ₂）</div>
  <div class="row small">可达半径 |l₁−l₂| = <span id="rmin">0.00</span> m ～ l₁+l₂ = <span id="rmax">1.00</span> m</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gGrid = document.getElementById("gGrid");
  var gWork = document.getElementById("gWork");
  var gArm1 = document.getElementById("gArm1");
  var gArm2 = document.getElementById("gArm2");
  var gTarget = document.getElementById("gTarget");
  var gMarks = document.getElementById("gMarks");

  var scene = new FK.Scene({
    svg: viewport, origin: { x: 500, y: 300 }, scale: 205,
    yaw: -1.12, pitch: 0.86, minScale: 70, maxScale: 400
  });

  // 注意：state 必须先于 fit() 的首次调用定义（fit 会写 state.compact / state.scale）
  var state = {
    tx: 0.6, ty: 0.45, phi: 0, l1: 0.5, l2: 0.5,
    mode: "both", showWork: true, showFrame: true, showLink: true, auto: false,
    compact: false, scale: 150
  };

  var C = {
    A: "#2563eb", B: "#c26a10", base: "#334155",
    target: "#d93025", pose: "#0e7490", work: "#94a3b8",
    warn: "#d93025", text: "#14213d"
  };

  /**
   * 自适应取景：整张 SVG 只画在面板上方的可用区域内。
   * 做法是把 viewBox 与视口像素 1:1 对齐（preserveAspectRatio="none"），
   * 于是“1 世界单位 = k 像素”，可用高度可以直接由面板顶边算出，
   * 避免固定 viewBox 与不同宽高比视口之间出现留白或压到面板下面。
   */
  function fit() {
    var rect = viewport.getBoundingClientRect();
    var W = Math.max(240, Math.round(rect.width));
    var H = Math.max(240, Math.round(rect.height));
    // 真·渲染尺寸：SVG 的实际视口不一定等于 CSS 盒（无头截图下尤其如此），
    // 用 getScreenCTM 反推 y 方向的实际缩放，避免图形被压扁或留白。
    try {
      var ctm = viewport.getScreenCTM();
      if (ctm && ctm.d > 0.01) {
        var bh = viewport.ownerSVGElement ? viewport.ownerSVGElement : viewport;
        var dy = bh.getBoundingClientRect().height / ctm.d;
        if (isFinite(dy) && dy > 100 && dy < 6000) H = Math.round(dy);
      }
    } catch (e) { /* 忽略，退回 CSS 盒尺寸 */ }
    viewport.setAttribute("viewBox", "0 0 " + W + " " + H);

    var panel = document.querySelector(".panel");
    var panelTop = H;
    if (panel) {
      var pr = panel.getBoundingClientRect();
      var py = pr.top * (H / Math.max(1, rect.height));
      if (py > 40 && py < H) panelTop = py;
    }
    var avail = Math.max(130, Math.min(H, panelTop) - 22);
    var k = Math.min(avail / 2.2, W / 3.4);

    scene.origin.x = W * 0.5;
    scene.origin.y = avail * 0.5 + 10;
    scene.state.scale = Math.max(55, Math.min(320, k));
    state.compact = scene.state.scale < 132;   // 小窗时精简标注，避免文字互相压盖
    state.scale = scene.state.scale;
    scene.baseOrigin.x = scene.origin.x;
    scene.baseOrigin.y = scene.origin.y;
  }
  fit();
  window.addEventListener("resize", function () { fit(); render(); });
  window.addEventListener("load", function () { fit(); render(); });

  /* --------------------------------------------------- 运动学：正解与逆解 */

  /** 正解：末端位置 + 末端姿态（平面臂自协调 φ = θ₁ + θ₂） */
  function fk(t1, t2, l1, l2) {
    var x = l1 * Math.cos(t1) + l2 * Math.cos(t1 + t2);
    var y = l1 * Math.sin(t1) + l2 * Math.sin(t1 + t2);
    return { x: x, y: y, phi: t1 + t2, elbow: [l1 * Math.cos(t1), l1 * Math.sin(t1)] };
  }

  /**
   * 位置逆解：给定目标点，返回两组关节解（“肘上 / 肘下”）。
   * cθ₂ = (r² − l₁² − l₂²)/(2 l₁ l₂)  ⇒  θ₂ = ±acos(cθ₂)（反三角函数多值性 → 两组解）
   * θ₁ = atan2(y, x) − atan2(l₂ sinθ₂, l₁ + l₂ cosθ₂)。
   * 两组解的末端位置完全相同；平面 2R 臂自协调 φ = θ₁ + θ₂，故两组解各自的
   * 末端姿态一般不同——这正是图 3.20 要说明的“同一位置有两组构型”的多解性
   * （要同时满足给定姿态，需在两组位置解中按姿态/避障等准则取舍）。
   */
  function ik(tx, ty, phi, l1, l2) {
    var r = Math.sqrt(tx * tx + ty * ty);
    var rmin = Math.abs(l1 - l2), rmax = l1 + l2;
    var c2 = (r * r - l1 * l1 - l2 * l2) / (2 * l1 * l2);
    if (c2 > 1 + 1e-12 || c2 < -1 - 1e-12) {
      return { ok: false, r: r, rmin: rmin, rmax: rmax };
    }
    c2 = Math.max(-1, Math.min(1, c2));
    var t2 = Math.acos(c2);
    var up = t1Of(t2), dn = t1Of(-t2);
    function t1Of(q2) {
      return Math.atan2(ty, tx) - Math.atan2(l2 * Math.sin(q2), l1 + l2 * Math.cos(q2));
    }
    function wrap(a) {
      while (a > Math.PI) a -= 2 * Math.PI;
      while (a < -Math.PI) a += 2 * Math.PI;
      return a;
    }
    return {
      ok: true, r: r, rmin: rmin, rmax: rmax,
      up: { t1: wrap(up), t2: t2 },
      dn: { t1: wrap(dn), t2: -t2 },
      c2: c2
    };
  }

  /* ------------------------------------------------------------ 绘图工具 */

  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    scene.el("line", Object.assign({
      x1: A.x, y1: A.y, x2: B.x, y2: B.y, "stroke-linecap": "round", fill: "none"
    }, attrs || {}), parent);
  }

  function label(v, str, dx, dy, fill, size, parent, anchor) {
    var node = scene.text(v, str, {
      dx: dx, dy: dy, fill: fill, "font-size": size,
      "font-weight": 700, "text-anchor": anchor || "start", class: "fk-point-label"
    }, 0, 0, parent);
    return node;
  }

  function dot(v, r, fill, parent) {
    var p = scene.project(v);
    scene.el("circle", { cx: p.x, cy: p.y, r: r, fill: fill, class: "fk-point" }, parent);
  }

  /** z=0 平面上的圆（工作空间边界） */
  function circleZ0(radius, attrs, parent) {
    var pts = [], steps = 96;
    for (var i = 0; i <= steps; i += 1) {
      var t = 2 * Math.PI * i / steps;
      pts.push([radius * Math.cos(t), radius * Math.sin(t), 0]);
    }
    scene.polyline(pts, attrs, parent);
  }

  /** 关节角度弧线 */
  function arcZ0(radius, a0, a1, color, parent, textAt, textDx, textDy) {
    var steps = 30, pts = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = a0 + (a1 - a0) * (i / steps);
      pts.push([radius * Math.cos(t), radius * Math.sin(t), 0]);
    }
    scene.polyline(pts, { stroke: color, class: "fk-arc" }, parent);
    if (textAt) {
      var mid = a0 + (a1 - a0) * 0.5;
      var p = scene.project([(radius + 0.11) * Math.cos(mid), (radius + 0.11) * Math.sin(mid), 0]);
      var node = scene.el("text", {
        x: p.x + (textDx || -9), y: p.y + (textDy || 6), fill: color, "font-size": 17,
        "font-weight": 700, class: "fk-axis-label"
      }, parent);
      node.textContent = textAt;
    }
  }

  /** 目标坐标系 {T}：只画 Ẑ 轴与表示目标姿态 φ 的 X̂ 轴（φ 角弧已标出 φ） */
  function drawTargetFrame(sol) {
    var phiT = state.phi * FK.DEG;
    var o = [state.tx, state.ty, 0];
    var len = 0.17;
    if (state.showFrame) {
      // Ẑ：垂直于工作平面
      var zTip = [o[0], o[1], len * 1.1];
      seg(o, zTip, { stroke: "#12944f", "stroke-width": 2.6, "stroke-dasharray": "6 5", "marker-end": "url(#arA)" }, gTarget);
      label(zTip, "Z\u0302\u209c", 7, -6, "#12944f", 13, gTarget);
      // X̂：目标姿态方向
      var xDir = [Math.cos(phiT), Math.sin(phiT), 0];
      var xTip = FK.Vec.add(o, FK.Vec.scale(xDir, len));
      seg(o, xTip, { stroke: C.pose, "stroke-width": 3.2, "marker-end": "url(#arT)" }, gTarget);
      var xRight = state.tx > 0.15 * (state.l1 + state.l2);
      if (!state.compact) {
        label(xTip, "X\u0302\u209c（目标姿态 \u03c6）",
          xRight ? -12 : 12, -30, C.pose, 14, gTarget, xRight ? "end" : "start");
      }
      // φ 角弧（从 +X 转到姿态方向）
      arcZ0(0.3, 0, phiT, C.pose, gTarget, "\u03c6", state.tx > 0 ? -24 : 6, -6);
    }
    // 目标点十字标（红色，超出工作空间时更醒目）
    var reach = sol.ok;
    var col = reach ? C.target : C.warn;
    var r0 = 0.04, r1 = 0.1;
    var dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
    for (var k = 0; k < dirs.length; k += 1) {
      seg([state.tx + dirs[k][0] * r0, state.ty + dirs[k][1] * r0, 0],
          [state.tx + dirs[k][0] * r1, state.ty + dirs[k][1] * r1, 0],
          { stroke: col, "stroke-width": reach ? 3.4 : 4.4 }, gTarget);
    }
    dot(o, reach ? 5.4 : 6.6, col, gTarget);
    var tRight = state.tx > 0.15 * (state.l1 + state.l2);
    label(o, "目标点 (" + FK.format(state.tx, 2) + ", " + FK.format(state.ty, 2) + ")",
      tRight ? -14 : 16, 38, reach ? "#8a1c14" : C.warn, 16, gTarget, tRight ? "end" : "start");
  }

  /** 画一组解（含构型文字标注） */
  function drawBranch(sol, color, name, dash, parent) {
    var el = fk(sol.t1, sol.t2, state.l1, state.l2);
    var O = [0, 0, 0];
    var E = [el.elbow[0], el.elbow[1], 0];
    var P = [el.x, el.y, 0];
    var attrs = {
      stroke: color, "stroke-width": 7.2,
      "stroke-dasharray": dash || null
    };
    seg(O, E, attrs, parent);
    seg(E, P, attrs, parent);
    dot(O, 6, C.base, parent);
    dot(E, 5, color, parent);
    dot(P, 4.6, color, parent);
    if (state.showLink) {
      var conf = (sol.t2 >= 1e-9 ? "\u03b8\u2082 > 0" : (sol.t2 <= -1e-9 ? "\u03b8\u2082 < 0" : "\u03b8\u2082 = 0"));
      var caption = state.compact ? name : (name + "（" + conf + "）");
      scene.text(E, caption, {
        dx: -22, dy: -16, fill: color, "font-size": state.compact ? 14 : 17,
        "font-weight": 700, "text-anchor": "end", class: "fk-point-label"
      }, 0, 0, parent);
    }
    return null;
  }

  /* --------------------------------------------------------------- 绘制 */

  function render() {
    gGrid.replaceChildren();
    gWork.replaceChildren();
    gArm2.replaceChildren();
    gArm1.replaceChildren();
    gTarget.replaceChildren();
    gMarks.replaceChildren();

    // 网格必须画进 gGrid：render() 只清理命名的 <g> 图层，
    // 若让 grid() 落在根 SVG，每次重绘都会累积一套网格（拖影根因）。
    scene.grid(1.4, 0.4, null, gGrid);

    // 基座坐标系与基座
    seg([0, 0, 0], [0, 0.42, 0], { stroke: "#94a3b8", "stroke-width": 2.6, "stroke-dasharray": "5 5", "marker-end": "url(#arAX)" }, gWork);
    var bz = label([0, 0.42, 0], "\u1dbb\u0302", 8, -6, "#64748b", 14, gWork);
    var o0 = scene.project([0, 0, 0]);
    scene.el("rect", {
      x: o0.x - 13, y: o0.y - 3, width: 26, height: 9, rx: 3,
      fill: C.base, opacity: 0.85
    }, gWork);

    var l1 = state.l1, l2 = state.l2;
    var sol = ik(state.tx, state.ty, state.phi, l1, l2);

    if (state.showWork) {
      circleZ0(l1 + l2, { stroke: C.work, class: "fk-arc", "stroke-width": 2.4 }, gWork);
      if (Math.abs(l1 - l2) > 0.02) {
        circleZ0(Math.abs(l1 - l2), { stroke: C.work, class: "fk-arc", "stroke-width": 2.4 }, gWork);
      }
      label([0, l1 + l2, 0], "可达外边界 l\u2081+l\u2082 = " + FK.format(l1 + l2, 2) + " m",
        0, -16, "#64748b", 15, gWork, "middle");
    }

    // 模式决定显示哪一组解：先画肘下（虚线）再画肘上（实线）避免遮盖
    var showUp = state.mode !== "down";
    var showDn = state.mode !== "up";

    if (sol.ok) {
      if (showDn) { drawBranch(sol.dn, C.B, "肘下解", "11 8", gArm2); }
      if (showUp) { drawBranch(sol.up, C.A, "肘上解", null, gArm1); }
      // 关节角弧线：θ₁ 在基座处，θ₂ 在肘部处（θ₂ 的正负即多解性的来源）
      arcZ0(Math.min(0.19, l1 * 0.4), 0, sol.up.t1, C.A, gArm1, "\u03b8\u2081", -2, -17);
      if (showUp) {
        arcZ0(Math.min(0.24, l1 * 0.5), sol.up.t1, sol.up.t1 + sol.up.t2, C.A, gArm1, "\u03b8\u2082", 8, 12);
      }
      if (showDn) {
        arcZ0(Math.min(0.24, l1 * 0.5), sol.dn.t1, sol.dn.t1 + sol.dn.t2, C.B, gArm2, null);
      }
      drawTargetFrame(sol);
    } else {
      // 无解：给出提示箭头（从端点指向目标）并说明
      drawTargetFrame(sol);
      var nearest = FK.Vec.scale(FK.Vec.normalize([state.tx, state.ty, 0]), l1 + l2);
      seg([nearest[0], nearest[1], 0], [state.tx, state.ty, 0],
        { stroke: C.warn, "stroke-width": 3, "stroke-dasharray": "8 6" }, gMarks);
      label([state.tx, state.ty, 0], "超出可达工作空间，无解",
        state.tx > 0.4 * (l1 + l2) ? -18 : 18, -20, C.warn, 19, gMarks,
        state.tx > 0.4 * (l1 + l2) ? "end" : "start");
      var mid = scene.project([(nearest[0] + state.tx) / 2, (nearest[1] + state.ty) / 2, 0]);
      scene.el("text", {
        x: mid.x + 10, y: mid.y + 20, fill: C.warn, "font-size": 15,
        "font-weight": 700, class: "fk-point-label"
      }, gMarks).textContent = "缺口 " + FK.format(sol.r - (l1 + l2), 3) + " m";
    }

    updateReadout(sol, showUp, showDn);
  }

  /* --------------------------------------------------------------- 读数 */

  function updateReadout(sol, showUp, showDn) {
    document.getElementById("tvx").textContent = FK.format(state.tx, 2);
    document.getElementById("tvy").textContent = FK.format(state.ty, 2);
    document.getElementById("tvphi").textContent = FK.deg(state.phi, 1);
    document.getElementById("rmin").textContent = FK.format(sol.rmin, 2);
    document.getElementById("rmax").textContent = FK.format(sol.rmax, 2);

    var statusEl = document.getElementById("status");
    var statusRow = document.getElementById("statusRow");
    if (!sol.ok) {
      statusEl.textContent = "无解（超出可达工作空间）";
      statusEl.style.color = C.warn;
      statusRow.classList.add("is-warn");
      document.getElementById("up1").textContent = "—";
      document.getElementById("up2").textContent = "—";
      document.getElementById("up3").textContent = "—";
      document.getElementById("dn1").textContent = "—";
      document.getElementById("dn2").textContent = "—";
      document.getElementById("dn3").textContent = "—";
      document.getElementById("sameMsg").textContent = "无解，无法比较两组末端位置";
    } else {
      var eu = fk(sol.up.t1, sol.up.t2, state.l1, state.l2);
      var ed = fk(sol.dn.t1, sol.dn.t2, state.l1, state.l2);
      var err = Math.max(Math.abs(eu.x - ed.x), Math.abs(eu.y - ed.y), Math.abs(eu.phi - ed.phi));
      document.getElementById("up1").textContent = FK.deg(sol.up.t1 / FK.DEG, 1);
      document.getElementById("up2").textContent = FK.deg(sol.up.t2 / FK.DEG, 1);
      document.getElementById("up3").textContent = FK.deg(eu.phi / FK.DEG, 1);
      document.getElementById("dn1").textContent = FK.deg(sol.dn.t1 / FK.DEG, 1);
      document.getElementById("dn2").textContent = FK.deg(sol.dn.t2 / FK.DEG, 1);
      document.getElementById("dn3").textContent = FK.deg(ed.phi / FK.DEG, 1);
      var collapsed = Math.abs(sol.up.t2) < 1e-9;
      document.getElementById("sameMsg").textContent = collapsed
        ? "两解重合（θ\u2082 = 0°，手臂完全伸直，处于工作空间边界）"
        : "完全一致（误差 " + err.toExponential(1) + "）";
      if (collapsed) {
        statusEl.textContent = "边界奇异形位（θ\u2082 = 0°，两组解重合）";
        statusEl.style.color = C.B;
        statusRow.classList.add("is-warn");
      } else {
        statusEl.textContent = "正常：两组解";
        statusEl.style.color = "#12944f";
        statusRow.classList.remove("is-warn");
      }
    }
    document.getElementById("txValue").textContent = FK.format(state.tx, 2);
    document.getElementById("tyValue").textContent = FK.format(state.ty, 2);
    document.getElementById("phiValue").textContent = FK.deg(state.phi, 1);
    document.getElementById("l1Value").textContent = FK.format(state.l1, 2);
    document.getElementById("l2Value").textContent = FK.format(state.l2, 2);
  }

  /* ----------------------------------------------------------- 交互绑定 */

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "tx", key: "tx", value: 0.6, format: function (v) { return FK.format(v, 2); } },
    { id: "ty", key: "ty", value: 0.45, format: function (v) { return FK.format(v, 2); } },
    { id: "phi", key: "phi", value: 0, format: function (v) { return FK.deg(v, 1); } },
    { id: "l1", key: "l1", value: 0.5, format: function (v) { return FK.format(v, 2); } },
    { id: "l2", key: "l2", value: 0.5, format: function (v) { return FK.format(v, 2); } }
  ], state, render);

  FK.bindToggles([
    { id: "showWork", key: "showWork" },
    { id: "showFrame", key: "showFrame" },
    { id: "showLink", key: "showLink" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  var tabs = document.getElementById("modeTabs");
  tabs.addEventListener("click", function (event) {
    var button = event.target.closest("button[data-mode]");
    if (!button) return;
    state.mode = button.getAttribute("data-mode");
    Array.prototype.forEach.call(tabs.querySelectorAll("button"), function (b) {
      b.classList.toggle("is-active", b === button);
    });
    render();
  });

  document.getElementById("reset").addEventListener("click", function () {
    state.tx = 0.6; state.ty = 0.45; state.phi = 0; state.l1 = 0.5; state.l2 = 0.5;
    state.mode = "both"; state.showWork = true; state.showFrame = true; state.showLink = true;
    state.auto = false;
    document.getElementById("showWork").checked = true;
    document.getElementById("showFrame").checked = true;
    document.getElementById("showLink").checked = true;
    document.getElementById("auto").checked = false;
    Array.prototype.forEach.call(tabs.querySelectorAll("button"), function (b) {
      b.classList.toggle("is-active", b.getAttribute("data-mode") === "both");
    });
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    fit();
    render();
  });

  /* ------------------------------------------------------------- 数值自检 */

  (function selfTest() {
    function assert(cond, msg) { if (!cond) throw new Error("图3-20 自检失败：" + msg); }

    // 0) 初始化顺序：state 必须在 fit() 首次调用之前完成定义（否则 fit 抛 TypeError）
    assert(state && typeof state === "object" && typeof state.compact === "boolean",
      "state 未定义或结构不完整（初始化顺序错误）");
    assert(typeof scene.state.scale === "number" && scene.state.scale > 0,
      "fit() 未正确设置 scene.state.scale");

    // 1) 同一目标点：两组解算出的末端位置完全一致（误差 < 1e-9），且都命中目标点
    var cases = [[0.6, 0.45, 0], [0.7, 0.35, 25], [-0.55, 0.62, -140], [0.3, -0.7, 90]];
    cases.forEach(function (c) {
      var s = ik(c[0], c[1], c[2], 0.5, 0.5);
      assert(s.ok, "点 (" + c[0] + "," + c[1] + ") 应可解");
      var eu = fk(s.up.t1, s.up.t2, 0.5, 0.5);
      var ed = fk(s.dn.t1, s.dn.t2, 0.5, 0.5);
      var e = Math.max(Math.abs(eu.x - ed.x), Math.abs(eu.y - ed.y));
      assert(e < 1e-9, "两组解末端位置不一致：" + e);
      assert(Math.abs(eu.x - c[0]) < 1e-9 && Math.abs(eu.y - c[1]) < 1e-9,
        "正解回代位置不符：" + JSON.stringify(eu));
      assert(s.up.t2 > 0 && s.dn.t2 < 0, "两组解 θ₂ 符号应相反：" + s.up.t2 + " / " + s.dn.t2);
    });

    // 1b) 工作空间边界上的目标点（r = l₁+l₂）：两组解重合于 θ₂ = 0
    var sEdge0 = ik(0.8, 0.6, 0, 0.5, 0.5);
    assert(sEdge0.ok && Math.abs(sEdge0.up.t2) < 1e-9 && Math.abs(sEdge0.dn.t2) < 1e-9,
      "边界点 (0.8, 0.6) 两解应重合且 θ₂ = 0");

    // 1c) 末端姿态：平面 2R 臂自协调关系 φ = θ₁ + θ₂。
    //     ik() 为位置逆解（不含姿态约束），因此图标里把“目标姿态 φ”与两组位置解的关系
    //     显式呈现：两组解各自的 φ = θ₁ + θ₂ 一般不同，二者都能到达同一目标点。
    var sPose = ik(0.6, 0.45, 0, 0.5, 0.5);
    var poseUp = fk(sPose.up.t1, sPose.up.t2, 0.5, 0.5);
    var poseDn = fk(sPose.dn.t1, sPose.dn.t2, 0.5, 0.5);
    assert(Math.abs(poseUp.phi - (sPose.up.t1 + sPose.up.t2)) < 1e-12 &&
      Math.abs(poseDn.phi - (sPose.dn.t1 + sPose.dn.t2)) < 1e-12, "φ = θ₁ + θ₂ 关系不成立");
    assert(Math.abs(poseUp.phi - poseDn.phi) > 1e-6,
      "内部点两组解的姿态应不同（这正是需要取舍的原因之一）");

    // 2) 目标点超出 l₁+l₂ 时无解
    assert(!ik(1.05, 0.4, 0, 0.5, 0.5).ok, "r > l₁+l₂ 应判为无解");
    assert(!ik(0.9, 0.9, 0, 0.5, 0.5).ok, "r > l₁+l₂ 应判为无解");
    assert(!ik(0.05, 0.0, 0, 0.6, 0.3).ok, "r < |l₁−l₂| 应判为无解");
    assert(ik(0.95, 0.0, 0, 0.5, 0.5).ok, "边界上 r = l₁+l₂ 应可解");

    // 3) 模式开关：两组解同时可算（供两解并显使用）
    var sBoth = ik(0.6, 0.45, 0, 0.5, 0.5);
    assert(sBoth.ok, "默认目标点 (0.6, 0.45) 应可解");
    assert(sBoth.up.t2 > 1e-6 && sBoth.dn.t2 < -1e-6,
      "默认目标点应给出两组明显不同的解，实得 θ₂ = " + sBoth.up.t2);
    // 4) 目标点恰在工作空间边界 (0.8, 0.6)，r = l₁+l₂ = 1 时两组解重合于 θ₂ = 0
    var sEdge = ik(0.8, 0.6, 0, 0.5, 0.5);
    assert(sEdge.ok && Math.abs(sEdge.up.t2) < 1e-9 && Math.abs(sEdge.dn.t2) < 1e-9,
      "目标点 (0.8, 0.6) 在 r = l₁+l₂ 上，两解应重合且 θ₂ = 0");
    assert(!ik(0.8, 0.61, 0, 0.5, 0.5).ok, "r > l₁+l₂ 应判为无解");
  }());

  render();
}());
"""

FIGURE = {
    "id": "figure-3-20",
    "title": "图3-20 机器人运动学逆解多解性示意图 · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
