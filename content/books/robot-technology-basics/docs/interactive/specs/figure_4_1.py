"""图4-1 二自由度平面关节型机器人简图（雅可比与奇异位形）
（《机器人技术基础（第三版）》4.1.1 机器人雅可比的定义 / 4.1.2 速度分析 / 4.1.3 讨论）。

教材依据：
- 式(4.1)：X = l₁cθ₁ + l₂c₁₂，Y = l₁sθ₁ + l₂s₁₂。
- 式(4.2)：X = X(θ₁, θ₂)，Y = Y(θ₁, θ₂)——末端坐标是关节角的函数。
- 式(4.4)：J = [[∂X/∂θ₁, ∂X/∂θ₂], [∂Y/∂θ₁, ∂Y/∂θ₂]]；式(4.5)(4.6)：
  J = [[−l₁sθ₁ − l₂s₁₂, −l₂s₁₂], [l₁cθ₁ + l₂c₁₂, l₂c₁₂]]。
- 式(4.10)：v = J(q)·q̇；式(4.12)：J⁻¹ = (1/(l₁l₂sθ₂))·[[l₂c₁₂, l₂s₁₂], [−l₁cθ₁−l₂c₁₂, −l₁sθ₁−l₂s₁₂]]。
- det J = l₁l₂ sinθ₂（正文 4.1.3：“当 l₁l₂sθ₂ = 0 时式(4.12)无解……二臂完全伸直或完全折回，
  机器人处于奇异形位……手部只能沿着一个方向（即与臂垂直的方向）运动”）。
- 例4.1：l₁ = l₂ = 0.5 m，θ₁ = 30°、θ₂ = −60°，手部沿 X₀ 正向 1.0 m/s ⇒ θ̇₁ = −2 rad/s、θ̇₂ = 4 rad/s
  （脚本内做了断言自检；正文式(4.12)中 c₂/(l₁sθ₂) = −2 要求 sθ₂ < 0，即 θ₂ 取 −60°）。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.legend i.dash { background-image: repeating-linear-gradient(90deg, #fff 0 3px, transparent 3px 6px); background-color: transparent; }
.readout .meter { display: block; height: 6px; margin-top: 4px; border-radius: 999px; background: #e3ebf6; overflow: hidden; }
.readout .meter i { display: block; height: 100%; width: 0; border-radius: 999px; background: #12944f; transition: width .12s linear, background .12s linear; }
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
  .readout {
    padding: 6px 8px; font-size: 11.5px; line-height: 1.45;
    max-width: calc(100% - 16px);
  }
  .readout .small { font-size: 10.5px; }
  .readout .row { white-space: normal; }
  .readout .row:nth-child(6), .readout .row:nth-child(7) { display: none; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 700" preserveAspectRatio="none"
     role="img" aria-label="二自由度平面关节型机器人雅可比与奇异位形示意图">
  <defs>
    <marker id="f4Base" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"></path>
    </marker>
    <marker id="f4V" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="f4C1" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="f4C2" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="f4Warn" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
  </defs>
  <g id="f4Grid"></g>
  <g id="f4Sing"></g>
  <g id="f4Base"></g>
  <g id="f4Arm"></g>
  <g id="f4Jac"></g>
  <g id="f4Vel"></g>
  <g id="f4Labels"></g>
</svg>

<section class="panel" aria-label="图4-1 控制面板">
  <div class="panel-head">
    <div>
      <h1>图4-1 2R 机器人雅可比</h1>
      <p class="subtitle">X = l₁cθ₁ + l₂c₁₂，Y = l₁sθ₁ + l₂s₁₂；v = J·q̇，det J = l₁l₂sinθ₂。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>
  <div class="control">
    <div class="control-head"><label for="t1">关节角 θ₁</label><output id="t1Value">30.0°</output></div>
    <input id="t1" type="range" min="-180" max="180" step="1" value="30">
  </div>
  <div class="control">
    <div class="control-head"><label for="t2">关节角 θ₂</label><output id="t2Value">-60.0°</output></div>
    <input id="t2" type="range" min="-180" max="180" step="1" value="-60">
  </div>
  <div class="control">
    <div class="control-head"><label for="l1">连杆长 l₁</label><output id="l1Value">0.50</output></div>
    <input id="l1" type="range" min="0.2" max="0.9" step="0.01" value="0.5">
  </div>
  <div class="control">
    <div class="control-head"><label for="l2">连杆长 l₂</label><output id="l2Value">0.50</output></div>
    <input id="l2" type="range" min="0.2" max="0.9" step="0.01" value="0.5">
  </div>
  <div class="control">
    <div class="control-head"><label for="w1">关节速度 θ̇₁</label><output id="w1Value">0.50</output></div>
    <input id="w1" type="range" min="-3" max="3" step="0.05" value="0.5">
  </div>
  <div class="control">
    <div class="control-head"><label for="w2">关节速度 θ̇₂</label><output id="w2Value">0.50</output></div>
    <input id="w2" type="range" min="-3" max="3" step="0.05" value="0.5">
  </div>
  <div class="options">
    <label><input id="showVel" type="checkbox" checked>显示末端速度矢量</label>
    <label><input id="showJac" type="checkbox" checked>显示雅可比矩阵</label>
    <label><input id="showCol" type="checkbox" checked>显示 J₁θ̇₁ / J₂θ̇₂ 分量</label>
    <label><input id="swing" type="checkbox">自动摆动</label>
  </div>
  <div class="legend">
    <span><i style="background:#334155"></i>连杆 l₁ / l₂</span>
    <span><i class="dot" style="background:#7c3aed"></i>末端速度 v = Jq̇</span>
    <span><i style="background:#2563eb"></i>J₁θ̇₁（关节1贡献）</span>
    <span><i style="background:#c26a10"></i>J₂θ̇₂（关节2贡献）</span>
    <span><i class="dash" style="background:#d93025"></i>奇异位形（完全伸直/折回）</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row"><strong>末端</strong> X = <span id="fx">0.433</span> m，Y = <span id="fy">0.750</span> m</div>
  <div class="row"><strong>J</strong> = [ <span id="j11">-0.750</span>, <span id="j12">-0.500</span> ; <span id="j21">0.433</span>, <span id="j22">0.000</span> ]</div>
  <div class="row"><strong>det J</strong> = l₁l₂sinθ₂ = <span id="det">-0.2165</span> m²</div>
  <div class="row"><span class="small">|det J| 占最大值 l₁l₂ 的 <span id="detPct">86.6</span>%</span>
    <span class="meter"><i id="detBar" style="width:86.6%"></i></span></div>
  <div class="row" id="singRow"><strong>奇异形位</strong>：<span id="sing">否（接近奇异）</span></div>
  <div class="row small" id="singNote"></div>
  <div class="row small">由 v = Jq̇ 反算：q̇ = J⁻¹v = [ <span id="rq1">0.00</span>, <span id="rq2">0.00</span> ] rad/s</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gGrid = document.getElementById("f4Grid");
  var gSing = document.getElementById("f4Sing");
  var gBase = document.getElementById("f4Base");
  var gArm = document.getElementById("f4Arm");
  var gJac = document.getElementById("f4Jac");
  var gVel = document.getElementById("f4Vel");
  var gLabels = document.getElementById("f4Labels");

  var scene = new FK.Scene({
    svg: viewport, origin: { x: 620, y: 330 }, scale: 200,
    yaw: -1.12, pitch: 0.86, minScale: 60, maxScale: 360
  });

  var state = {
    t1: 30, t2: -60, l1: 0.5, l2: 0.5, w1: 0.5, w2: 0.5,
    showVel: true, showJac: true, showCol: true, swing: false, compact: false
  };

  /** 自适应取景：viewBox 与视口像素 1:1，图形只占用面板上方的可用区域。 */
  function fit() {
    var rect = viewport.getBoundingClientRect();
    var W = Math.max(240, Math.round(rect.width));
    var H = Math.max(240, Math.round(rect.height));
    try {
      var ctm = viewport.getScreenCTM();
      if (ctm && ctm.d > 0.01) {
        var box = viewport.ownerSVGElement ? viewport.ownerSVGElement : viewport;
        var dy = box.getBoundingClientRect().height / ctm.d;
        if (isFinite(dy) && dy > 100 && dy < 6000) H = Math.round(dy);
      }
    } catch (e) { /* 忽略 */ }
    viewport.setAttribute("viewBox", "0 0 " + W + " " + H);

    var panel = document.querySelector(".panel");
    var panelTop = H;
    if (panel) {
      var py = panel.getBoundingClientRect().top * (H / Math.max(1, rect.height));
      if (py > 40 && py < H) panelTop = py;
    }
    var avail = Math.max(130, Math.min(H, panelTop) - 22);
    var k = Math.min(avail / 2.25, W / 3.3);

    scene.origin.x = W * 0.5;
    scene.origin.y = avail * 0.5 + 12;
    scene.state.scale = Math.max(50, Math.min(360, k));
    state.compact = scene.state.scale < 120;
    scene.baseOrigin.x = scene.origin.x;
    scene.baseOrigin.y = scene.origin.y;
  }
  window.addEventListener("resize", function () { fit(); render(); });
  window.addEventListener("load", function () { fit(); render(); });

  var C = {
    link: "#334155", joint: "#334155", base: "#1f2937",
    v: "#7c3aed", c1: "#2563eb", c2: "#c26a10",
    singular: "#d93025", safe: "#12944f", work: "#94a3b8", warn: "#c26a10"
  };

  // 速度矢量与雅可比列矢量的绘图比例：1 (m/s) 画成 0.35 (m) 世界长度，
  // 并限制单个箭头不超过臂长的约 60%，保证箭头与标签始终落在画布内。
  var VEL_UNIT = 0.35;
  var SWING = { frame: 0, base: { t1: 30, t2: -60 } };
  var ranges = null;   // 在交互绑定处赋值

  /* --------------------------------------------------------- 运动学核心 */

  /** 式(4.1)：正运动学 */
  function fk(t1, t2, l1, l2) {
    var c1 = Math.cos(t1), s1 = Math.sin(t1);
    var c12 = Math.cos(t1 + t2), s12 = Math.sin(t1 + t2);
    return {
      x: l1 * c1 + l2 * c12,
      y: l1 * s1 + l2 * s12,
      elbow: [l1 * c1, l1 * s1]
    };
  }

  /** 式(4.6)：2×2 速度雅可比 */
  function jacobian(t1, t2, l1, l2) {
    var s1 = Math.sin(t1), c1 = Math.cos(t1);
    var s12 = Math.sin(t1 + t2), c12 = Math.cos(t1 + t2);
    return {
      j11: -l1 * s1 - l2 * s12, j12: -l2 * s12,
      j21: l1 * c1 + l2 * c12, j22: l2 * c12
    };
  }

  /** 末端速度 v = J·q̇（式 4.10） */
  function tipVelocity(J, w1, w2) {
    return [J.j11 * w1 + J.j12 * w2, J.j21 * w1 + J.j22 * w2];
  }

  /* ------------------------------------------------------------ 绘图工具 */

  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    scene.el("line", Object.assign({
      x1: A.x, y1: A.y, x2: B.x, y2: B.y, "stroke-linecap": "round", fill: "none"
    }, attrs || {}), parent);
  }

  function dot(v, r, fill, parent) {
    var p = scene.project(v);
    scene.el("circle", { cx: p.x, cy: p.y, r: r, fill: fill, class: "fk-point" }, parent);
  }

  function text(v, str, dx, dy, fill, size, parent, anchor) {
    var node = scene.text(v, str, {
      dx: dx, dy: dy, fill: fill, "font-size": size,
      "font-weight": 700, "text-anchor": anchor || "start", class: "fk-point-label"
    }, 0, 0, parent);
    return node;
  }

  /**
   * 速度矢量的箭头端点：按 VEL_UNIT 比例换算成世界长度，
   * 并限制最大长度为 cap（约为臂长的若干分之一），保证箭头不出画布。
   */
  function arrowTip(from, vec, cap) {
    var n = Math.hypot(vec[0], vec[1]);
    if (n < 1e-9) return from.slice();
    var len = Math.min(n * VEL_UNIT, cap);
    return [from[0] + vec[0] / n * len, from[1] + vec[1] / n * len, 0];
  }

  function arcZ0(radius, a0, a1, color, textAt, parent) {
    var steps = 30, pts = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = a0 + (a1 - a0) * (i / steps);
      pts.push([radius * Math.cos(t), radius * Math.sin(t), 0]);
    }
    scene.polyline(pts, { stroke: color, class: "fk-arc" }, parent);
    if (textAt) {
      var mid = a0 + (a1 - a0) * 0.5;
      var p = scene.project([(radius + 0.13) * Math.cos(mid), (radius + 0.13) * Math.sin(mid), 0]);
      var node = scene.el("text", {
        x: p.x - 9, y: p.y + 6, fill: color, "font-size": 17,
        "font-weight": 700, class: "fk-axis-label"
      }, parent);
      node.textContent = textAt;
    }
  }

  /* --------------------------------------------------------------- 绘制 */

  function render() {
    gGrid.replaceChildren();
    gSing.replaceChildren();
    gBase.replaceChildren();
    gArm.replaceChildren();
    gJac.replaceChildren();
    gVel.replaceChildren();
    gLabels.replaceChildren();

    scene.grid(1.4, 0.4);

    var t1 = state.t1 * FK.DEG, t2 = state.t2 * FK.DEG;
    var l1 = state.l1, l2 = state.l2;
    var pos = fk(t1, t2, l1, l2);
    var J = jacobian(t1, t2, l1, l2);
    var det = J.j11 * J.j22 - J.j12 * J.j21;      // = l₁l₂ sinθ₂
    var detMax = l1 * l2;
    var ratio = detMax > 0 ? Math.abs(det) / detMax : 0;
    // sinθ₂ 的绝对值：用位形判断奇异（θ₂ → 0° 或 ±180°）
    var singLevel = Math.abs(Math.sin(t2));
    var singular = singLevel < 0.06;
    var near = !singular && (singLevel < 0.22 || ratio < 0.22);

    var O = [0, 0, 0];
    var E = [pos.elbow[0], pos.elbow[1], 0];
    var P = [pos.x, pos.y, 0];

    // 基座
    seg(O, [0, 0.4, 0], { stroke: C.work, "stroke-width": 2.6, "stroke-dasharray": "5 5", "marker-end": "url(#f4Base)" }, gBase);
    text([0, 0.4, 0], "\u1dbb\u0302", 8, -6, "#64748b", 14, gBase);
    var o0 = scene.project(O);
    scene.el("rect", { x: o0.x - 13, y: o0.y - 3, width: 26, height: 9, rx: 3, fill: C.base, opacity: 0.85 }, gBase);

    // 奇异形位指示：完全伸直（θ₂ = 0）与完全折回（θ₂ = ±180°）的目标位置
    var reachMax = l1 + l2, reachMin = Math.abs(l1 - l2);
    var dirSign = Math.abs(t2) > Math.PI / 2 ? -1 : 1;
    var tipMax = [dirSign * reachMax * Math.cos(t1), dirSign * reachMax * Math.sin(t1), 0];
    seg(O, tipMax, { stroke: C.singular, "stroke-width": 2.4, "stroke-dasharray": "9 7", opacity: 0.75 }, gSing);
    if (!state.compact) {
      text(tipMax, Math.abs(t2) > Math.PI / 2 ? "完全折回 |det J| = 0" : "完全伸直 |det J| = 0",
        10, Math.abs(t2) > Math.PI / 2 ? 22 : -10, C.singular, 15, gSing);
    }

    // 手臂
    seg(O, E, { stroke: C.link, "stroke-width": 8.4 }, gArm);
    seg(E, P, { stroke: C.link, "stroke-width": 8.4 }, gArm);
    dot(O, 6.4, C.base, gArm);
    dot(E, 5.6, C.joint, gArm);
    dot(P, 5.2, C.joint, gArm);
    arcZ0(Math.min(0.2, l1 * 0.42), 0, t1, C.joint, "\u03b8\u2081", gArm);
    arcZ0(l1 * 0.8, t1, t1 + t2, C.warn, "\u03b8\u2082", gArm);

    // 雅可比矩阵：两列 = 关节1、关节2单独运动产生的端点速度方向
    var velCap = 0.6 * (l1 + l2);   // 单个箭头不超过臂长的 60%，保证不出画布
    if (state.showCol) {
      var v1 = [J.j11 * state.w1, J.j21 * state.w1];
      var v2 = [J.j12 * state.w2, J.j22 * state.w2];
      if (Math.hypot(v1[0], v1[1]) > 1e-4) {
        var tip1 = arrowTip(P, v1, velCap);
        seg(P, tip1, { stroke: C.c1, "stroke-width": 3.4, "marker-end": "url(#f4C1)" }, gJac);
        text(tip1, "J\u2081\u03b8\u0307\u2081", 8, 18, C.c1, 15, gJac, "start");
      }
      if (Math.hypot(v2[0], v2[1]) > 1e-4) {
        var tip2 = arrowTip(P, v2, velCap);
        seg(P, tip2, { stroke: C.c2, "stroke-width": 3.4, "marker-end": "url(#f4C2)" }, gJac);
        text(tip2, "J\u2082\u03b8\u0307\u2082", 10, -8, C.c2, 15, gJac, "start");
      }
    }

    // 末端速度 v = J·q̇
    var v = tipVelocity(J, state.w1, state.w2);
    var vLen = Math.hypot(v[0], v[1]);
    if (state.showVel) {
      if (vLen > 1e-4) {
        var tipV = arrowTip(P, v, 0.75 * (l1 + l2));
        seg(P, tipV, { stroke: C.v, "stroke-width": 5.2, "marker-end": "url(#f4V)" }, gVel);
        // 标签放在箭头延长线上、并朝远离画面右下角（读数区）的一侧偏移，避免被读数区遮挡
        var dve = Math.atan2(J.j22, J.j12);
        var off = (Math.cos(dve) > 0.35) ? -0.17 : 0.17;
        var lp = [tipV[0] + Math.cos(dve) * off, tipV[1] + Math.sin(dve) * off, 0];
        text(lp, state.compact ? "v  |v| = " + FK.format(vLen, 3) + " m/s"
          : "v = Jq\u0307  |v| = " + FK.format(vLen, 3) + " m/s",
          0, 0, "#5b21b6", 16, gVel, "middle");
      } else {
        text(P, "v = 0（该位形下末端瞬时静止）", 14, -14, "#5b21b6", 16, gVel);
      }
    }

    // 奇异提示（读数区 + 视觉反馈）
    if (singular) {
      var ring = scene.project(P);
      scene.el("circle", {
        cx: ring.x, cy: ring.y, r: 26, fill: "none",
        stroke: C.singular, "stroke-width": 3, "stroke-dasharray": "7 6"
      }, gSing);
      var nearRight = P[0] > 0.1 * (l1 + l2);
      text(P, state.compact ? "\u5947\u5f02\uff1adet J = 0" : "\u5947\u5f02\u4f4d\u5f62\uff1adet J = 0\uff0c\u672b\u7aef\u5931\u53bb\u4e00\u4e2a\u81ea\u7531\u5ea6",
        nearRight ? -30 : 24, -26, C.singular, 17, gSing, nearRight ? "end" : "start");
    } else if (near) {
      var ring2 = scene.project(P);
      scene.el("circle", {
        cx: ring2.x, cy: ring2.y, r: 20, fill: "none",
        stroke: C.warn, "stroke-width": 2.4, "stroke-dasharray": "6 6", opacity: 0.9
      }, gSing);
      text(P, "接近奇异：|det J| 很小", 24, -22, C.warn, 16, gSing);
    }

    updateReadout(pos, J, det, detMax, ratio, singLevel, singular, near, v);

    document.getElementById("t1Value").textContent = FK.deg(state.t1, 1);
    document.getElementById("t2Value").textContent = FK.deg(state.t2, 1);
    document.getElementById("l1Value").textContent = FK.format(state.l1, 2);
    document.getElementById("l2Value").textContent = FK.format(state.l2, 2);
    document.getElementById("w1Value").textContent = FK.format(state.w1, 2);
    document.getElementById("w2Value").textContent = FK.format(state.w2, 2);
  }

  function updateReadout(pos, J, det, detMax, ratio, singLevel, singular, near, v) {
    document.getElementById("fx").textContent = FK.format(pos.x, 3);
    document.getElementById("fy").textContent = FK.format(pos.y, 3);
    document.getElementById("j11").textContent = FK.format(J.j11, 3);
    document.getElementById("j12").textContent = FK.format(J.j12, 3);
    document.getElementById("j21").textContent = FK.format(J.j21, 3);
    document.getElementById("j22").textContent = FK.format(J.j22, 3);
    document.getElementById("det").textContent = FK.format(det, 4);
    document.getElementById("detPct").textContent = FK.format(ratio * 100, 1);
    var bar = document.getElementById("detBar");
    bar.style.width = Math.max(0, Math.min(100, ratio * 100)).toFixed(1) + "%";
    bar.style.background = singular ? C.singular : (near ? C.warn : C.safe);

    var singEl = document.getElementById("sing");
    var noteEl = document.getElementById("singNote");
    if (singular) {
      singEl.textContent = "是（det J = 0，二臂完全伸直或完全折回）";
      singEl.style.color = C.singular;
      noteEl.textContent = "J 降秩：末端只能沿与臂垂直的方向运动，其他方向需要无穷大关节速度。";
      noteEl.style.color = C.singular;
    } else if (near) {
      singEl.textContent = "接近奇异（θ\u2082 趋近 0° 或 ±180°）";
      singEl.style.color = C.warn;
      noteEl.textContent = "|det J| 很小，逆雅可比 J\u207b\u00b9 的元素迅速增大，末端某些方向需要极大的关节速度。";
      noteEl.style.color = C.warn;
    } else {
      singEl.textContent = "否（θ\u2082 = " + FK.deg(state.t2, 1) + "，|det J| 充足）";
      singEl.style.color = C.safe;
      noteEl.textContent = "";
    }

    // 由 v = Jq̇ 反算关节速度：q̇ = J⁻¹v —— 奇异位形附近会迅速发散
    var q1 = NaN, q2 = NaN;
    if (Math.abs(det) > 1e-9) {
      q1 = (J.j22 * v[0] - J.j12 * v[1]) / det;
      q2 = (-J.j21 * v[0] + J.j11 * v[1]) / det;
    }
    var big = !isFinite(q1) || !isFinite(q2) || Math.abs(q1) > 20 || Math.abs(q2) > 20;
    document.getElementById("rq1").textContent = isFinite(q1) ? FK.format(q1, 3) : "∞";
    document.getElementById("rq2").textContent = isFinite(q2) ? FK.format(q2, 3) : "∞";
    document.getElementById("rq1").style.color = big ? C.singular : "";
    document.getElementById("rq2").style.color = big ? C.singular : "";
    if (big && !singular) {
      noteEl.textContent = "所需关节速度已超过工程可用范围（|q\u0307| > 20 rad/s）。";
      noteEl.style.color = C.singular;
    }
  }

  /* ----------------------------------------------------------- 交互绑定 */

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "t1", key: "t1", value: 30, format: function (v) { return FK.deg(v, 1); } },
    { id: "t2", key: "t2", value: -60, format: function (v) { return FK.deg(v, 1); } },
    { id: "l1", key: "l1", value: 0.5, format: function (v) { return FK.format(v, 2); } },
    { id: "l2", key: "l2", value: 0.5, format: function (v) { return FK.format(v, 2); } },
    { id: "w1", key: "w1", value: 0.5, format: function (v) { return FK.format(v, 2); } },
    { id: "w2", key: "w2", value: 0.5, format: function (v) { return FK.format(v, 2); } }
  ], state, render);

  var swingBox = document.getElementById("swing");

  function stopSwing(restore) {
    if (SWING.frame) { cancelAnimationFrame(SWING.frame); SWING.frame = 0; }
    state.swing = false;
    swingBox.checked = false;
    if (restore) {
      state.t1 = SWING.base.t1;
      state.t2 = SWING.base.t2;
      if (ranges) ranges.refresh();
    }
  }

  var swingStart = 0;
  function tick(now) {
    SWING.frame = 0;
    if (!state.swing) return;
    if (!swingStart) swingStart = now;
    var t = (now - swingStart) / 1000;
    state.t1 = SWING.base.t1 + 55 * Math.sin(1.1 * t);
    state.t2 = SWING.base.t2 + 55 * Math.sin(0.63 * t + 1.1);
    // 摆动时视觉上更关注奇异：把滑杆同步，再重绘
    document.getElementById("t1").value = state.t1;
    document.getElementById("t2").value = state.t2;
    render();
    SWING.frame = requestAnimationFrame(tick);
  }

  swingBox.addEventListener("change", function () {
    if (swingBox.checked) {
      SWING.base = { t1: state.t1, t2: state.t2 };
      swingStart = 0;
      state.swing = true;
      if (!SWING.frame) SWING.frame = requestAnimationFrame(tick);
    } else {
      stopSwing(true);
      render();
    }
  });

  FK.bindToggles([
    { id: "showVel", key: "showVel" },
    { id: "showJac", key: "showJac" },
    { id: "showCol", key: "showCol" }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    stopSwing(false);
    state.t1 = 30; state.t2 = -60; state.l1 = 0.5; state.l2 = 0.5;
    state.w1 = 0.5; state.w2 = 0.5;
    state.showVel = true; state.showJac = true; state.showCol = true;
    document.getElementById("showVel").checked = true;
    document.getElementById("showJac").checked = true;
    document.getElementById("showCol").checked = true;
    scene.setAuto(false);
    ranges.refresh();
    fit();
    scene.reset();
    render();
  });

  /* ------------------------------------------------------------- 数值自检 */

  (function selfTest() {
    function assert(cond, msg) { if (!cond) throw new Error("图4-1 自检失败：" + msg); }
    var l1 = 0.5, l2 = 0.5;

    // 0) 初始化顺序：state 必须在 fit() 首次调用之前完成定义，且 fit() 已生效
    assert(state && typeof state === "object" && typeof state.compact === "boolean",
      "state 未定义或结构不完整（初始化顺序错误）");
    assert(typeof scene.state.scale === "number" && scene.state.scale > 0,
      "fit() 未正确设置 scene.state.scale");

    // 1) det J = l₁l₂sinθ₂：θ₂ = 90° 取最大值 l₁l₂，θ₂ = 0° / ±180° 为 0
    var J90 = jacobian(30 * FK.DEG, 90 * FK.DEG, l1, l2);
    var det90 = J90.j11 * J90.j22 - J90.j12 * J90.j21;
    assert(Math.abs(Math.abs(det90) - l1 * l2) < 1e-12,
      "θ₂ = 90° 时 |det J| 应为 l₁l₂ = " + (l1 * l2) + "，实得 " + det90);
    var J0 = jacobian(30 * FK.DEG, 0, l1, l2);
    assert(Math.abs(J0.j11 * J0.j22 - J0.j12 * J0.j21) < 1e-12, "θ₂ = 0° 时 det J 应为 0");
    var J180 = jacobian(30 * FK.DEG, 180 * FK.DEG, l1, l2);
    assert(Math.abs(J180.j11 * J180.j22 - J180.j12 * J180.j21) < 1e-12, "θ₂ = ±180° 时 det J 应为 0");

    // 2) 例4.1：l₁ = l₂ = 0.5，θ₁ = 30°、θ₂ = −60°，v = [1, 0] ⇒ θ̇₁ = −2、θ̇₂ = 4 rad/s
    //    （正文式(4.12)中该项为 c₂/l₁sθ₂ = 0.5/(0.5×(−0.866)) = −1/0.5 = −2，故 θ₂ 取 −60°）
    var J = jacobian(30 * FK.DEG, -60 * FK.DEG, 0.5, 0.5);
    var det = J.j11 * J.j22 - J.j12 * J.j21;
    var q1 = (J.j22 * 1 - J.j12 * 0) / det;
    var q2 = (-J.j21 * 1 + J.j11 * 0) / det;
    assert(Math.abs(q1 + 2) < 1e-9, "例4.1 θ̇₁ 应为 −2 rad/s，实得 " + q1);
    assert(Math.abs(q2 - 4) < 1e-9, "例4.1 θ̇₂ 应为 4 rad/s，实得 " + q2);

    // 3) v = Jq̇ 等于直接对式(4.1)求导：
    //    Ẋ = −(l₁sθ₁ + l₂s₁₂)θ̇₁ − l₂s₁₂θ̇₂；Ẏ = (l₁cθ₁ + l₂c₁₂)θ̇₁ + l₂c₁₂θ̇₂
    var Jq = jacobian(30 * FK.DEG, -60 * FK.DEG, l1, l2);
    var qd1 = 0.5, qd2 = 0.5;
    var c1 = Math.cos(30 * FK.DEG), s1 = Math.sin(30 * FK.DEG);
    var c12 = Math.cos(-30 * FK.DEG), s12 = Math.sin(-30 * FK.DEG);
    var ana = tipVelocity(Jq, qd1, qd2);
    var direct = [-(l1 * s1 + l2 * s12) * qd1 - l2 * s12 * qd2,
      (l1 * c1 + l2 * c12) * qd1 + l2 * c12 * qd2];
    assert(Math.abs(ana[0] - direct[0]) < 1e-12 && Math.abs(ana[1] - direct[1]) < 1e-12,
      "v = Jq̇ 与式(4.1)求导不符：" + JSON.stringify(ana) + " vs " + JSON.stringify(direct));

    // 5) 绘图比例：箭头长度必须可控（不超过 cap），否则会冲出画布
    var tipTest = arrowTip([0, 0, 0], [10, 10], 0.5);
    assert(Math.abs(Math.hypot(tipTest[0], tipTest[1]) - 0.5) < 1e-12,
      "arrowTip 未按 cap 截断，实得 " + Math.hypot(tipTest[0], tipTest[1]));

    // 4) 奇异位形的物理后果：θ₂ → 0 时给定 v 需要极大的关节速度
    var Js = jacobian(30 * FK.DEG, 0.5 * FK.DEG, l1, l2);
    var ds = Js.j11 * Js.j22 - Js.j12 * Js.j21;
    var qs = (Js.j22 * 1 - Js.j12 * 0) / ds;
    assert(Math.abs(qs) > 20, "接近 θ₂ = 0 时所需关节速度应发散，实得 " + qs);
  }());

  fit();
  render();
}());
"""

FIGURE = {
    "id": "figure-4-1",
    "title": "图4-1 二自由度平面关节型机器人简图（雅可比与奇异位形） · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
