"""图3-15 连杆变换的四步分解与中间坐标系 {P}{Q}{R}（克雷格《机器人学导论（第3版）》第3章）。

教材依据：
- 式(3-4)（本教材标准 D-H 记法）：{}^{i-1}_i T = R_X(α_{i-1}) · D_X(a_{i-1}) · R_Z(θ_i) · D_Z(d_i)。
  教材把四步基本变换产生的中间坐标系依次记为 {P}、{Q}、{R}，于是
  {i-1} --绕 X̂_{i-1} 转 α_{i-1}--> {P} --沿 X̂_{i-1} 移 a_{i-1}--> {Q}
         --绕 Ẑ_Q 转 θ_i--> {R} --沿 Ẑ_R 移 d_i--> {i}。
- 式(3-4) 展开后的 4×4（下标 i-1 属于 α 与 a，i 属于 θ 与 d）：
      [ cθ     -sθ      0     a      ]
      [ sθ·cα   cθ·cα  -sα    -sα·d  ]
      [ sθ·sα   cθ·sα   cα     cα·d  ]
      [ 0       0       0      1     ]
  脚本内用 FK.M4.chain 连乘与该展开式逐元素比对（四组参数 + 默认值显式断言），失败即 throw。
- 提醒：本教材用“标准 D-H”（{i} 固定在连杆远端，α_{i-1}、a_{i-1} 的下标是 i-1），
  不要与改进型（modified D-H）记法混淆。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.step-banner {
  margin-top: 9px;
  padding: 6px 9px;
  border: 1px solid #cddffb;
  border-radius: 9px;
  color: var(--blue-dark);
  background: var(--blue-soft);
  font-size: 12px;
  line-height: 1.5;
}
.step-banner b { color: #1d4ed8; }
.step-banner .chain { color: #5b6a80; font-size: 11px; }
.control-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 12px; margin-top: 6px; }
.control-grid .control { margin-top: 6px; }
.control-grid .control label { font-size: 11.5px; }
.control-grid .control output { font-size: 11.5px; }
.control-grid input[type="range"] { margin: 6px 0 0; }
.options { margin-top: 9px; }
.legend { margin-top: 8px; padding-top: 8px; gap: 4px 10px; font-size: 11px; }
.matrix-block { margin-top: 9px; padding-top: 8px; border-top: 1px dashed var(--line); }
.mx + .mx { margin-top: 8px; }
.mx-head { margin-bottom: 3px; color: #45566f; font-size: 11px; }
.mx-head strong { color: var(--blue-dark); }
.mx-grid {
  border-collapse: collapse;
  border-left: 2px solid #b9c8dd;
  border-right: 2px solid #b9c8dd;
  font: 10.5px/1.35 ui-monospace, SFMono-Regular, Consolas, monospace;
}
.mx-grid td { padding: 0 5px; text-align: right; color: #33415c; }
.mx-grid td.pos { color: var(--blue-dark); font-weight: 700; }
.mx-grid td.hi { color: #b45309; font-weight: 700; }
.mx-grid td.dim { color: #9aa8bd; }

@media (max-width: 720px) {
  .readout { font-size: 12.5px; }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 11.5px; }
  .step-banner { font-size: 11.5px; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="连杆变换四步分解与中间坐标系 P、Q、R 的交互三维示意图">
  <defs>
    <marker id="arrowX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="arrowY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="arrowZ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="arrowP" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="arrowQ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="arrowR" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
    <marker id="arrowD" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#b91c1c"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="dimLayer"></g>
  <g id="axesLayer"></g>
  <g id="labelLayer"></g>
</svg>

<section class="panel" aria-label="图3-15 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3-15 中间坐标系 {P}{Q}{R}</h1>
      <p class="subtitle">式(3-4) 四步分解：{i−1} →绕X转α<sub>i−1</sub>→ {P} →沿X移a<sub>i−1</sub>→ {Q} →绕Z转θ<sub>i</sub>→ {R} →沿Z移d<sub>i</sub>→ {i}。拖动“步骤”逐帧看清每一步。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="step-banner" id="stepBanner"></div>

  <div class="control">
    <div class="control-head"><label for="step">步骤（显示到第 k 步）</label><output id="stepValue">4 / 4</output></div>
    <input id="step" type="range" min="1" max="4" step="1" value="4">
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="alpha">扭角 α<sub>i−1</sub></label><output id="alphaValue">-90.0°</output></div>
      <input id="alpha" type="range" min="-180" max="180" step="1" value="-90">
    </div>
    <div class="control">
      <div class="control-head"><label for="a">长度 a<sub>i−1</sub></label><output id="aValue">0.50</output></div>
      <input id="a" type="range" min="0" max="2" step="0.05" value="0.5">
    </div>
    <div class="control">
      <div class="control-head"><label for="theta">关节角 θ<sub>i</sub></label><output id="thetaValue">30.0°</output></div>
      <input id="theta" type="range" min="-180" max="180" step="1" value="30">
    </div>
    <div class="control">
      <div class="control-head"><label for="d">偏距 d<sub>i</sub></label><output id="dValue">0.50</output></div>
      <input id="d" type="range" min="-2" max="2" step="0.05" value="0.5">
    </div>
  </div>

  <div class="options">
    <label><input id="play" type="checkbox">自动逐步播放</label>
    <label><input id="showAnno" type="checkbox" checked>显示参数标注</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i style="background:#475569"></i>{i−1}</span>
    <span><i style="background:#c26a10"></i>{P} 绕X转α</span>
    <span><i style="background:#7c3aed"></i>{Q} 沿X移a</span>
    <span><i style="background:#0e7490"></i>{R} 绕Z转θ</span>
    <span><i style="background:#174ea6"></i>{i} 沿Z移d</span>
  </div>

  <div class="matrix-block">
    <div class="mx">
      <div class="mx-head" id="mxHeadStep"></div>
      <table class="mx-grid"><tbody id="mxStep"></tbody></table>
    </div>
    <div class="mx">
      <div class="mx-head" id="mxHeadAcc"></div>
      <table class="mx-grid"><tbody id="mxAcc"></tbody></table>
    </div>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row"><strong>第 <span id="roStep">4</span> / 4 步</strong> <span class="small" id="roStepName"></span></div>
  <div class="row">累计变换位移 <strong>p</strong> = [ <span id="rox">0.500</span>, <span id="roy">0.500</span>, <span id="roz">0.000</span> ]ᵀ</div>
  <div class="row small">α<sub>i−1</sub> = <span id="roAlpha">-90.0°</span> · a<sub>i−1</sub> = <span id="roA">0.50</span> · θ<sub>i</sub> = <span id="roTheta">30.0°</span> · d<sub>i</sub> = <span id="roD">0.50</span></div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var dimLayer = document.getElementById("dimLayer");
  var axesLayer = document.getElementById("axesLayer");
  var labelLayer = document.getElementById("labelLayer");

  var DEFAULTS = { step: 4, alpha: -90, a: 0.5, theta: 30, d: 0.5 };
  var state = {
    step: DEFAULTS.step, alpha: DEFAULTS.alpha, a: DEFAULTS.a,
    theta: DEFAULTS.theta, d: DEFAULTS.d,
    showAnno: true, play: false, auto: false
  };

  // 允许用 #alpha=0&a=0&theta=0&d=0&step=2 指定初始状态（便于核对极值与退化情形）
  (function readHash() {
    var raw = (window.location.hash || "").replace(/^#/, "");
    if (!raw) return;
    raw.split("&").forEach(function (kv) {
      var parts = kv.split("=");
      if (parts.length !== 2) return;
      var key = decodeURIComponent(parts[0]);
      var value = Number(decodeURIComponent(parts[1]));
      if (!isFinite(value)) return;
      if (key === "step") state.step = Math.max(1, Math.min(4, Math.round(value)));
      if (key === "alpha") state.alpha = Math.max(-180, Math.min(180, value));
      if (key === "a") state.a = Math.max(0, Math.min(2, value));
      if (key === "theta") state.theta = Math.max(-180, Math.min(180, value));
      if (key === "d") state.d = Math.max(-2, Math.min(2, value));
    });
  }());

  var scene = new FK.Scene({ svg: viewport, origin: { x: 700, y: 364 }, scale: 126, yaw: -0.68, pitch: 0.44 });

  var C = {
    x: "#d93025", y: "#2563eb", z: "#12944f",
    P: "#c26a10", Q: "#7c3aed", R: "#0e7490", D: "#b91c1c",
    base: "#475569", final: "#174ea6"
  };
  var DIRS = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];

  var STEP_INFO = [
    { from: "{i−1}", to: "{P}", act: "绕 X̂<sub>i−1</sub> 旋转 α<sub>i−1</sub>", mat: "R<sub>X</sub>(α<sub>i−1</sub>)", color: C.P },
    { from: "{P}", to: "{Q}", act: "沿 X̂<sub>i−1</sub> 平移 a<sub>i−1</sub>", mat: "D<sub>X</sub>(a<sub>i−1</sub>)", color: C.Q },
    { from: "{Q}", to: "{R}", act: "绕 Ẑ<sub>Q</sub> 旋转 θ<sub>i</sub>", mat: "R<sub>Z</sub>(θ<sub>i</sub>)", color: C.R },
    { from: "{R}", to: "{i}", act: "沿 Ẑ<sub>R</sub> 平移 d<sub>i</sub>", mat: "D<sub>Z</sub>(d<sub>i</sub>)", color: C.D }
  ];

  /* ------------------------------------------------------------ 绘制工具 */

  function richText(x, y, parts, attrs, parent) {
    var node = scene.el("text", Object.assign({ x: x, y: y }, attrs || {}), parent);
    parts.forEach(function (part) {
      var span = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
      span.setAttribute("dy", part[1] || 0);
      span.setAttribute("font-size", part[2] || 15);
      span.textContent = part[0];
      node.appendChild(span);
    });
    return node;
  }

  function sub(main, subText, size) {
    return [[main, 0, size || 15], [subText, 5, (size || 15) - 4.5]];
  }

  function richTextRot(x, y, deg, parts, attrs, parent) {
    var node = richText(x, y, parts, attrs, parent);
    node.setAttribute("transform", "rotate(" + deg + " " + x + " " + y + ")");
    node.setAttribute("text-anchor", "middle");
    return node;
  }

  function drawFrame(m, cfg) {
    var O = scene.project(FK.M4.apply(m, [0, 0, 0]));
    for (var i = 0; i < 3; i += 1) {
      var tip = FK.M4.apply(m, FK.Vec.scale(DIRS[i], cfg.len));
      var B = scene.project(tip);
      scene.el("line", {
        x1: O.x, y1: O.y, x2: B.x, y2: B.y,
        stroke: cfg.colors[i],
        "stroke-width": cfg.width,
        "stroke-dasharray": cfg.dash || null,
        "marker-end": "url(#" + cfg.markers[i] + ")"
      }, axesLayer);
    }
    scene.el("circle", { cx: O.x, cy: O.y, r: 4.2, fill: cfg.dot, class: "fk-point" }, axesLayer);
    return O;
  }

  function axisLabel(m, index, len, parts, dx, dy, color) {
    var p = scene.project(FK.M4.apply(m, FK.Vec.scale(DIRS[index], len)));
    richText(p.x + dx, p.y + dy, parts, { fill: color, "font-size": 15, class: "fk-axis-label" }, labelLayer);
  }

  /** 坐标系名称标牌；x、y 是标牌左上角的屏幕坐标，leader 是引线终点（屏幕坐标） */
  function badge(x, y, text, color, leader) {
    var w = 22 + text.length * 7.6;
    var h = 19;
    if (leader) {
      scene.el("line", {
        x1: x + w + 3, y1: y + h / 2,
        x2: leader.x, y2: leader.y,
        stroke: "#9aa8bd", "stroke-width": 1.1, "stroke-dasharray": "4 4"
      }, labelLayer);
    }
    scene.el("rect", {
      x: x, y: y, width: w, height: h, rx: 6,
      fill: "#ffffff", "fill-opacity": 0.94, stroke: color, "stroke-width": 1.6
    }, labelLayer);
    var t = scene.el("text", {
      x: x + w / 2, y: y + 13.4, "text-anchor": "middle", fill: color,
      "font-size": 12, "font-weight": 700, "font-style": "italic"
    }, labelLayer);
    t.textContent = text;
    return { x: x, y: y, w: w, h: h };
  }

  /** 弧形箭头：plane = "YZ"（绕X轴，从Y转向Z）或 "XY"（绕Z轴，从X转向Y） */
  function drawArc(m, plane, radius, angle, color, marker, parts) {
    if (Math.abs(angle) < 1.5 * FK.DEG) return;
    var steps = Math.max(10, Math.round(Math.abs(angle) / FK.DEG / 4));
    var pts = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = angle * (i / steps);
      pts.push(FK.M4.apply(m, plane === "YZ"
        ? [0, radius * Math.cos(t), radius * Math.sin(t)]
        : [radius * Math.cos(t), radius * Math.sin(t), 0]));
    }
    scene.polyline(pts, {
      stroke: color, "stroke-width": 2.4, "stroke-dasharray": "6 5",
      "marker-end": "url(#" + marker + ")"
    }, dimLayer);
    var mid = angle * 0.5;
    var label = FK.M4.apply(m, plane === "YZ"
      ? [0, (radius + 0.34) * Math.cos(mid), (radius + 0.34) * Math.sin(mid)]
      : [(radius + 0.34) * Math.cos(mid), (radius + 0.34) * Math.sin(mid), 0]);
    var q = scene.project(label);
    richText(q.x, q.y + 5, parts, { fill: color, "font-size": 15, "text-anchor": "middle", class: "fk-vec-label" }, labelLayer);
  }

  /** 尺寸线：两端双斜线 + 尺寸界线 + 数值标签（标签沿尺寸线方向旋转）；down=true 时放在轴线“下方” */
  function dimension(p1, p2, offPx, color, parts, down, labelOff) {
    var A = scene.project(p1);
    var B = scene.project(p2);
    var dx = B.x - A.x;
    var dy = B.y - A.y;
    var len = Math.sqrt(dx * dx + dy * dy);
    if (len < 8) return;
    var ux = dx / len;
    var uy = dy / len;
    var nx = -uy;
    var ny = ux;
    if ((down && ny < 0) || (!down && ny > 0)) { nx = -nx; ny = -ny; }
    var a = { x: A.x + nx * offPx, y: A.y + ny * offPx };
    var b = { x: B.x + nx * offPx, y: B.y + ny * offPx };
    [A, B].forEach(function (src, index) {
      var tgt = index === 0 ? a : b;
      scene.el("line", {
        x1: src.x, y1: src.y, x2: tgt.x, y2: tgt.y,
        stroke: color, "stroke-width": 1.2, "stroke-dasharray": "4 4", opacity: 0.65
      }, dimLayer);
    });
    scene.el("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: color, "stroke-width": 1.9 }, dimLayer);
    var sx = (ux + nx) / Math.SQRT2;
    var sy = (uy + ny) / Math.SQRT2;
    [a, b].forEach(function (p) {
      [-3.6, 3.6].forEach(function (offset) {
        var cx = p.x + ux * offset;
        var cy = p.y + uy * offset;
        scene.el("line", {
          x1: cx - sx * 7.5, y1: cy - sy * 7.5, x2: cx + sx * 7.5, y2: cy + sy * 7.5,
          stroke: color, "stroke-width": 1.9
        }, dimLayer);
      });
    });
    var angle = Math.atan2(uy, ux) * 180 / Math.PI;
    if (angle > 90) angle -= 180;
    if (angle < -90) angle += 180;
    var lo = labelOff === undefined ? 11 : labelOff;
    var mp = { x: (a.x + b.x) / 2 + nx * lo, y: (a.y + b.y) / 2 + ny * lo };
    richTextRot(mp.x, mp.y + 5, angle, parts, { fill: color, "font-size": 15, class: "fk-vec-label" }, labelLayer);
  }

  /* ------------------------------------------------------------ 面板矩阵 */

  var IDENTITY = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];

  function fillMatrix(tbody, m, mode) {
    tbody.replaceChildren();
    for (var r = 0; r < 4; r += 1) {
      var tr = document.createElement("tr");
      for (var c = 0; c < 4; c += 1) {
        var v = m[r * 4 + c];
        var td = document.createElement("td");
        td.textContent = (Math.abs(v) < 5e-4 ? 0 : v).toFixed(3);
        if (r === 3) td.className = "dim";
        else if (mode === "pos" && c === 3) td.className = "pos";
        else if (mode === "hi" && Math.abs(v - IDENTITY[r * 4 + c]) > 1e-9) td.className = "hi";
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    }
  }

  /* ------------------------------------------------------------ 主绘制 */

  function render() {
    gridLayer.replaceChildren();
    dimLayer.replaceChildren();
    axesLayer.replaceChildren();
    labelLayer.replaceChildren();

    scene.grid(3, 1, null, gridLayer);

    var alpha = state.alpha * FK.DEG;
    var theta = state.theta * FK.DEG;
    var k = state.step;

    var I = FK.M4.identity();
    var T1 = FK.M4.rotX(alpha);
    var T2 = FK.M4.translate([state.a, 0, 0]);
    var T3 = FK.M4.rotZ(theta);
    var T4 = FK.M4.translate([0, 0, state.d]);
    var TP = T1;
    var TQ = FK.M4.multiply(TP, T2);
    var TR = FK.M4.multiply(TQ, T3);
    var TI = FK.M4.multiply(TR, T4);

    // 1) 坐标轴：{i−1} 恒显示，之后逐步出现 {P}、{Q}、{R}、{i}
    drawFrame(I, {
      len: 1.75, width: 3.0, colors: [C.x, C.y, C.z],
      markers: ["arrowX", "arrowY", "arrowZ"], dot: C.base
    });
    var mids = [
      { m: TP, len: 1.42, color: C.P, marker: "arrowP" },
      { m: TQ, len: 1.14, color: C.Q, marker: "arrowQ" },
      { m: TR, len: 0.90, color: C.R, marker: "arrowR" }
    ];
    for (var i = 0; i < Math.min(k, 3); i += 1) {
      var mid = mids[i];
      drawFrame(mid.m, {
        len: mid.len, width: 2.5, dash: "9 6",
        colors: [mid.color, mid.color, mid.color],
        markers: [mid.marker, mid.marker, mid.marker], dot: mid.color
      });
    }
    if (k >= 4) {
      drawFrame(TI, {
        len: 1.75, width: 3.6, colors: [C.x, C.y, C.z],
        markers: ["arrowX", "arrowY", "arrowZ"], dot: C.final
      });
    }

    // 2) 参数标注（弧形箭头 / 尺寸线）
    if (state.showAnno) {
      if (k >= 1) drawArc(I, "YZ", 0.86, alpha, C.P, "arrowP", sub("α", "i−1", 16));
      if (k >= 3) drawArc(TQ, "XY", 0.58, theta, C.R, "arrowR", sub("θ", "i", 16));
      if (k >= 2) dimension([0, 0, 0], [state.a, 0, 0], 44, C.Q, sub("a", "i−1", 16), true, 11);
      if (k >= 4) dimension(FK.M4.position(TR), FK.M4.position(TI), 30, C.D, sub("d", "i", 16), false, -11);
    }

    // 3) 坐标系名称：{i−1}/{P}/{Q}/{R} 统一泊成左侧一列，用细引线指向各自原点；{i} 贴住自身原点
    var O = scene.project([0, 0, 0]);
    var Qs = scene.project(FK.M4.position(TQ));
    var Is = scene.project(FK.M4.position(TI));
    var colX = O.x - 80;
    badge(colX, O.y - 38, "{i−1}", C.base, { x: O.x - 8, y: O.y - 6 });
    if (k >= 1) badge(colX, O.y + 3, "{P}", C.P, { x: O.x + 4, y: O.y + 4 });
    if (k >= 2) badge(colX, O.y + 44, "{Q}", C.Q, { x: Qs.x - 14, y: Qs.y - 8 });
    if (k >= 3) badge(colX, O.y + 85, "{R}", C.R, { x: Qs.x - 12, y: Qs.y + 10 });
    if (k >= 4) badge(Is.x + 25, Is.y - 10, "{i}", C.final, null);

    axisLabel(I, 0, 1.75, sub("X\u0302", "i−1"), 8, 16, C.x);
    axisLabel(I, 1, 1.75, sub("Y\u0302", "i−1"), 8, -8, C.y);
    axisLabel(I, 2, 1.75, sub("Z\u0302", "i−1"), 10, -8, C.z);
    if (k >= 4) {
      var degenerate = FK.Vec.len(FK.Vec.sub(FK.M4.position(TI), [0, 0, 0])) < 0.22;
      axisLabel(TI, 0, 1.75, sub("X\u0302", "i"), 8, 16 + (degenerate ? 22 : 0), C.x);
      axisLabel(TI, 1, 1.75, sub("Y\u0302", "i"), 8, -8 - (degenerate ? 22 : 0), C.y);
      axisLabel(TI, 2, 1.75, sub("Z\u0302", "i"), 10, -8 - (degenerate ? 20 : 0), C.z);
    }
    if (k === 2) axisLabel(TP, 0, 1.42, sub("X\u0302", "P"), 8, 16, C.P);
    if (k === 3) axisLabel(TQ, 2, 1.14, sub("Z\u0302", "Q"), -14, -12, C.Q);
    if (k === 4) axisLabel(TR, 2, 0.90, sub("Z\u0302", "R"), -30, -14, C.R);

    // 4) 读数与矩阵
    var info = STEP_INFO[k - 1];
    var acc = k === 1 ? TP : (k === 2 ? TQ : (k === 3 ? TR : TI));
    var steps = [T1, T2, T3, T4];
    var names = ["{i−1}", "{P}", "{Q}", "{R}", "{i}"].slice(0, k + 1);

    document.getElementById("stepBanner").innerHTML =
      "<b>第 " + k + " 步</b>：" + info.from + " <span style='color:" + info.color + "'>— " + info.act + " →</span> " + info.to +
      "<br><span class='chain'>已显示 " + names.join("、") + "（共 " + (k + 1) + " 个坐标系）</span>";

    document.getElementById("mxHeadStep").innerHTML = "本步 T<sub>" + k + "</sub> = " + info.mat;
    fillMatrix(document.getElementById("mxStep"), steps[k - 1], "hi");
    document.getElementById("mxHeadAcc").innerHTML = k === 4
      ? "连乘 <sup>i−1</sup><sub>i</sub>T = T<sub>1</sub>T<sub>2</sub>T<sub>3</sub>T<sub>4</sub>"
      : "累乘 T<sub>1</sub>···T<sub>" + k + "</sub>（还没到 {i}）";
    fillMatrix(document.getElementById("mxAcc"), acc, "pos");

    var p = FK.M4.position(acc);
    document.getElementById("roStep").textContent = k;
    document.getElementById("roStepName").innerHTML = info.act + " → " + info.to;
    document.getElementById("rox").textContent = FK.format(p[0], 3);
    document.getElementById("roy").textContent = FK.format(p[1], 3);
    document.getElementById("roz").textContent = FK.format(p[2], 3);
    document.getElementById("roAlpha").textContent = FK.deg(state.alpha, 1);
    document.getElementById("roA").textContent = FK.format(state.a, 2);
    document.getElementById("roTheta").textContent = FK.deg(state.theta, 1);
    document.getElementById("roD").textContent = FK.format(state.d, 2);
  }

  scene.setRenderer(render);

  /* ------------------------------------------------------------ 响应式布局 */

  function relayout() {
    var rect = viewport.getBoundingClientRect();
    var W = Math.max(360, Math.round(rect.width || window.innerWidth));
    var H = Math.max(360, Math.round(rect.height || window.innerHeight));
    viewport.setAttribute("viewBox", "0 0 " + W + " " + H);
    var narrow = W < 720;
    scene.baseOrigin.x = narrow ? W * 0.34 : W * 0.50;
    scene.baseOrigin.y = narrow ? H * 0.28 : H * 0.5;
    var unit = narrow
      ? Math.max(46, Math.min(70, W * 0.17))
      : Math.max(70, Math.min(144, W * 0.12));
    scene.defaults.scale = unit;
    scene.state.scale = unit;
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  /* ------------------------------------------------------------ 交互绑定 */

  var ranges = FK.bindRanges(
    [
      { id: "step", key: "step", value: state.step, format: function (v) { return v + " / 4"; } },
      { id: "alpha", key: "alpha", value: state.alpha, format: function (v) { return FK.deg(v, 1); } },
      { id: "a", key: "a", value: state.a, format: function (v) { return FK.format(v, 2); } },
      { id: "theta", key: "theta", value: state.theta, format: function (v) { return FK.deg(v, 1); } },
      { id: "d", key: "d", value: state.d, format: function (v) { return FK.format(v, 2); } }
    ],
    state,
    render
  );

  var playFrame = 0;
  var playClock = 0;
  var playLast = 0;

  function playTick(t) {
    playFrame = 0;
    if (!state.play) return;
    if (!playLast) playLast = t;
    playClock += t - playLast;
    playLast = t;
    if (playClock >= 950) {
      playClock = 0;
      state.step = state.step >= 4 ? 1 : state.step + 1;
      ranges.refresh();
      render();
    }
    playFrame = requestAnimationFrame(playTick);
  }

  function setPlay(on) {
    state.play = !!on;
    playClock = 0;
    playLast = 0;
    if (state.play) {
      if (!playFrame) playFrame = requestAnimationFrame(playTick);
    } else if (playFrame) {
      cancelAnimationFrame(playFrame);
      playFrame = 0;
    }
  }

  FK.bindToggles(
    [
      { id: "play", key: "play", onChange: setPlay },
      { id: "showAnno", key: "showAnno" },
      { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
    ],
    state,
    render
  );

  document.getElementById("reset").addEventListener("click", function () {
    state.step = DEFAULTS.step;
    state.alpha = DEFAULTS.alpha;
    state.a = DEFAULTS.a;
    state.theta = DEFAULTS.theta;
    state.d = DEFAULTS.d;
    state.showAnno = true;
    state.auto = false;
    setPlay(false);
    document.getElementById("showAnno").checked = true;
    document.getElementById("auto").checked = false;
    document.getElementById("play").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    render();
  });

  window.addEventListener("resize", function () {
    relayout();
    render();
  });

  /* ------------------------------------------------------------ 教材数值自检 */

  (function selfTest() {
    // 式(3-4) 展开式（本教材标准 D-H 记法）
    function expand(alpha, a, theta, d) {
      var ca = Math.cos(alpha), sa = Math.sin(alpha);
      var ct = Math.cos(theta), st = Math.sin(theta);
      return [
        ct, -st, 0, a,
        st * ca, ct * ca, -sa, -sa * d,
        st * sa, ct * sa, ca, ca * d,
        0, 0, 0, 1
      ];
    }
    function chain(alpha, a, theta, d) {
      return FK.M4.chain(
        FK.M4.rotX(alpha),
        FK.M4.translate([a, 0, 0]),
        FK.M4.rotZ(theta),
        FK.M4.translate([0, 0, d])
      );
    }
    var cases = [
      [-90 * FK.DEG, 0.5, 30 * FK.DEG, 0.5],
      [37 * FK.DEG, 1.2, -64 * FK.DEG, -0.8],
      [0, 0, 0, 0],
      [180 * FK.DEG, 0, -180 * FK.DEG, 2]
    ];
    cases.forEach(function (cse, index) {
      var got = chain(cse[0], cse[1], cse[2], cse[3]);
      var want = expand(cse[0], cse[1], cse[2], cse[3]);
      for (var i = 0; i < 16; i += 1) {
        if (Math.abs(got[i] - want[i]) > 1e-12) {
          throw new Error("式(3-4) 自检失败（第" + (index + 1) + "组，元素" + i + "）：" + got[i] + " ≠ " + want[i]);
        }
      }
      var R = FK.M4.rotation(got);
      for (var r = 0; r < 3; r += 1) {
        for (var c2 = 0; c2 < 3; c2 += 1) {
          var sum = 0;
          for (var kk = 0; kk < 3; kk += 1) sum += R[r * 3 + kk] * R[c2 * 3 + kk];
          if (Math.abs(sum - (r === c2 ? 1 : 0)) > 1e-12) {
            throw new Error("旋转部分非正交（第" + (index + 1) + "组）");
          }
        }
      }
    });
    // 默认参数（α=−90°, a=0.5, θ=30°, d=0.5）下 ^{i-1}_iT 的显式数值
    var Tdef = chain(-90 * FK.DEG, 0.5, 30 * FK.DEG, 0.5);
    var expected = [
      0.8660254037844387, -0.5, 0, 0.5,
      0, 0, 1, 0.5,
      -0.5, -0.8660254037844387, 0, 0,
      0, 0, 0, 1
    ];
    for (var j = 0; j < 16; j += 1) {
      if (Math.abs(Tdef[j] - expected[j]) > 1e-12) {
        throw new Error("默认参数数值自检失败（元素" + j + "）：" + Tdef[j] + " ≠ " + expected[j]);
      }
    }
    // 默认参数下 {i} 原点 = [a, −sα·d, cα·d] = [0.5, 0.5, 0]
    var p = FK.M4.position(Tdef);
    if (!FK.Vec.eq(FK.Vec.round(p, 9), [0.5, 0.5, 0], 1e-9)) {
      throw new Error("默认参数 {i} 原点自检失败：" + JSON.stringify(p));
    }
    // 四个中间坐标系的原点：{P} 与 {i−1} 重合，{Q} 在 [a,0,0]，{R} 与 {Q} 重合
    var eps = 1e-12;
    if (!FK.Vec.eq(FK.M4.position(FK.M4.rotX(-90 * FK.DEG)), [0, 0, 0], eps)) {
      throw new Error("中间坐标系 {P} 原点自检失败");
    }
    if (!FK.Vec.eq(FK.M4.position(chain(-90 * FK.DEG, 0.5, 0, 0)), [0.5, 0, 0], eps)) {
      throw new Error("中间坐标系 {Q} 原点自检失败");
    }
    if (!FK.Vec.eq(FK.M4.position(chain(-90 * FK.DEG, 0.5, 30 * FK.DEG, 0)), [0.5, 0, 0], eps)) {
      throw new Error("中间坐标系 {R} 与 {Q} 应重合，自检失败");
    }
  }());

  relayout();
  render();
}());
"""

FIGURE = {
    "id": "figure-3-15",
    "title": "图3-15 中间坐标系{P}{Q}{R} · 连杆变换四步分解",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
