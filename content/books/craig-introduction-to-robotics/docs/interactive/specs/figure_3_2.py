"""图3-2 连杆长度 a 与转角 α（克雷格《机器人学导论（第3版）》3.2 节 连杆描述）。

教材依据：
- 3.2 节原文：“三维空间中的任意两个轴之间的距离均为一个确定值, 两个轴之间的距离即为两轴之间
  公垂线的长度。两轴之间的公垂线总是存在的, 当两轴不平行时, 两轴之间的公垂线只有一条。
  当两关节轴平行时, 则存在无数条长度相等的公垂线。……关节轴 和关节轴 之间公垂线的长度为
  即为连杆长度。”
- 转角 α_{i−1}：绕公垂线（右手定则）把关节轴 i−1 转到关节轴 i 的角度。由于公垂线同时垂直于
  两轴，绕它转动可以把轴 i−1 精确地转到轴 i，且转过的角度正是两轴之间的夹角：
      n̂ = r̂₁ × r̂₂ / |r̂₁ × r̂₂|,   α = atan2( |r̂₁×r̂₂| , r̂₁·r̂₂ ) ∈ [0°, 180°]
  脚本里就是用这条关系**反解**出实际转角（而不是直接复用滑块），并断言其与滑块一致。

图元约定（与教材图3-2 对应）：
- 两条直线 = 两个关节轴；夹在中间的线段 = 两轴唯一的公垂线，其长度标为 a_{i−1}；
- 公垂线与两轴都垂直 → 两个直角小方块；
- 绕公垂线的弧形箭头 = 转角 α_{i−1}（右手绕 n̂ 从轴 i−1 转向轴 i）；
- α = 0° / 180° 时两轴平行/反向平行 → 按机械制图习惯画**三短划线**，并提示“公垂线有无数条”。

坐标构造（与教材推导一一对应，滑块 a、α、β、φ 都能单独观察）：
    r̂₁ = Ẑ
    n̂  = (sinβ·cosφ, sinβ·sinφ, cosβ)      β 决定 n̂ 与 Ẑ 的夹角、φ 决定它绕 Ẑ 的方位
    r̂₂ = R_{n̂}(α)·r̂₁,   轴2 过点 Q = a·n̂，方向 r̂₂
于是 n̂·r̂₁ = n̂·r̂₂ = 0（公垂线定义自动成立），|r̂₁×r̂₂| = |sin α|（两轴夹角 = |α|），
轴2 到轴1 的距离 |(Q−P)×r̂₂| = a。这些量在下面的自检里逐条断言。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.control-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px 12px; margin-top: 8px; }
.control-grid .control { margin-top: 2px; min-width: 0; }
.control-grid .control-head { display: block; line-height: 1.3; }
.control-grid .control-head output { display: block; font-size: 11.5px; }
.control-grid .control label { font-size: 11.5px; }
.control-grid input[type="range"] { margin: 3px 0 1px; height: 3px; }
.options-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 5px 10px; margin-top: 10px; }
.options-grid label { display: inline-flex; align-items: center; gap: 5px; color: #4a5a72; font-size: 11.5px; cursor: pointer; white-space: nowrap; }
.options-grid input { accent-color: var(--blue); flex: none; }
.note {
  margin-top: 9px; padding: 6px 8px; border: 1px solid #cddffb; border-radius: 9px;
  color: var(--blue-dark); background: var(--blue-soft); font-size: 11.5px; line-height: 1.5;
}
.note.warn { border-color: #f3d19b; color: #92400e; background: #fef6e7; }
.legend { gap: 4px 10px; font-size: 11px; }
.legend i.dash { width: 14px; height: 0; border-top: 3px dashed #0e7490; }

@media (max-width: 720px) {
  .panel h1 { font-size: 13.5px; }
  .control-grid { gap: 5px 9px; }
  .control-grid .control label, .control-grid .control-head output { font-size: 10.5px; }
  .options-grid label { font-size: 10.5px; }
  .legend { font-size: 10px; gap: 3px 7px; }
  .note { font-size: 10.5px; }
  .readout { font-size: 12px; line-height: 1.45; padding: 6px 8px; max-width: calc(100vw - 16px); }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 10.5px; }
}
html, body { overflow-x: hidden; }
.app { max-width: 100vw; }
"""

BODY = """
<svg class="viewport" id="viewport" role="img"
     aria-label="两条关节轴、它们的公垂线与绕公垂线的转角α的交互三维示意图">
  <defs>
    <marker id="mAxis1" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"></path>
    </marker>
    <marker id="mAxis2" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#174ea6"></path>
    </marker>
    <marker id="mNormal" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#b45309"></path>
    </marker>
    <marker id="mAlpha" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.8" markerHeight="5.8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="mDir" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.2" markerHeight="5.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="axisLayer"></g>
  <g id="dimLayer"></g>
  <g id="labelLayer"></g>
</svg>

<section class="panel" aria-label="图3-2 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3-2 连杆长度 a 与转角 α</h1>
      <p class="subtitle">两关节轴之间只有一条公垂线，它的长度就是连杆长度 a<sub>i−1</sub>；绕这条公垂线
        （右手定则）把轴 i−1 转到轴 i 的角度就是 α<sub>i−1</sub>。公垂线与两轴都垂直。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="a">连杆长度 a<sub>i−1</sub></label><output id="aValue">1.00</output></div>
    <input id="a" type="range" min="0.2" max="2.5" step="0.05" value="1">
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="alpha">转角 α<sub>i−1</sub></label><output id="alphaValue">45.0°</output></div>
      <input id="alpha" type="range" min="-180" max="180" step="1" value="45">
    </div>
    <div class="control">
      <div class="control-head"><label for="beta">方位 β</label><output id="betaValue">65.0°</output></div>
      <input id="beta" type="range" min="0" max="180" step="1" value="65">
    </div>
    <div class="control">
      <div class="control-head"><label for="phi">方位 φ</label><output id="phiValue">0°</output></div>
      <input id="phi" type="range" min="0" max="360" step="1" value="0">
    </div>
    <div class="control">
      <div class="control-head"><label for="axisLen">轴显示长度</label><output id="axisLenValue">1.05</output></div>
      <input id="axisLen" type="range" min="0.5" max="2.4" step="0.05" value="1.05">
    </div>
  </div>

  <div class="options-grid">
    <label><input id="showNormal" type="checkbox" checked>显示公垂线</label>
    <label><input id="showRight" type="checkbox" checked>直角标记</label>
    <label><input id="showParallel" type="checkbox" checked>平行三短划线</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="note" id="specialNote"></div>

  <div class="legend">
    <span><i style="background:#475569"></i>关节轴 i−1</span>
    <span><i style="background:#174ea6"></i>关节轴 i</span>
    <span><i style="background:#b45309"></i>公垂线（长 a）</span>
    <span><i style="background:#7c3aed"></i>转角 α（绕公垂线）</span>
    <span><i class="dash" style="background:none"></i>三短划线＝两轴平行</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row"><strong>a<sub>i−1</sub></strong> = <span id="roA">1.000</span>　<strong>α<sub>i−1</sub></strong> = <span id="roAlpha">45.0°</span>　<strong>β</strong> = <span id="roBeta">65.0°</span></div>
  <div class="row small">实测：两轴夹角 = <span id="roMeas">45.0°</span>　·　|r̂₁×r̂₂| = <span id="roSin">0.707</span>　·　r̂₁·r̂₂ = <span id="roDot">0.707</span></div>
  <div class="row small">垂直性：n̂·r̂₁ = <span id="roD1">0.000</span>　n̂·r̂₂ = <span id="roD2">0.000</span>　两轴距离 = <span id="roDist">1.000</span></div>
  <div class="row small" id="roSign">α 的正方向：右手拇指指向 n̂，四指从轴 i−1 卷向轴 i。</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var axisLayer = document.getElementById("axisLayer");
  var dimLayer = document.getElementById("dimLayer");
  var labelLayer = document.getElementById("labelLayer");
  var svgNS = "http://www.w3.org/2000/svg";

  var DEFAULTS = { a: 1, alpha: 45, beta: 65, phi: 0, axisLen: 1.05 };
  var state = {
    a: DEFAULTS.a, alpha: DEFAULTS.alpha, beta: DEFAULTS.beta, phi: DEFAULTS.phi,
    axisLen: DEFAULTS.axisLen,
    showNormal: true, showRight: true, showParallel: true, auto: false
  };

  /* 公垂线方向：与 Ẑ 成 β 角、绕 Ẑ 的方位为 φ */
  function normalDir(beta, phi) {
    return [-Math.sin(beta) * Math.sin(phi), Math.sin(beta) * Math.cos(phi), Math.cos(beta)];
  }

  /* ---------------- 取景矩形（初值按 viewBox 1000x620） ----------------
     桌面 1200x700：viewBox x 0..1000 → 屏幕 34..1537，y 0..620 → 屏幕 7..691。
     左侧让给控制面板；右下角让给读数卡；右上角让给提示条。 */
  var FIT = { cx: 640, cy: 290, w: 520, h: 340 };

  var layout = { axisLength: DEFAULTS.axisLen };
  var boxes = [];

  var scene = new FK.AdaptiveScene({
    svg: viewport,
    scale: 118,
    narrowScale: 76,
    yaw: -0.60,
    pitch: 0.24,
    wide: { x: 0.62, y: 0.44 },
    narrow: { x: 0.52, y: 0.32 },
    tall: { x: 0.52, y: 0.30 },
    onLayout: function (sc, box) {
      if (box.narrow) {
        FIT.cx = box.width * 0.52;
        FIT.cy = box.height * 0.33;
        FIT.w = box.width * 0.88;
        FIT.h = box.height * 0.40;
      } else {
        FIT.cx = box.width * 0.61;
        FIT.cy = box.height * 0.45;
        FIT.w = box.width * 0.52;
        FIT.h = box.height * 0.56;
      }
    }
  });

  /* ---------------- 基础图元 ---------------- */
  function el(tag, attrs, parent) { return scene.el(tag, attrs, parent || axisLayer); }
  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    return el("line", Object.assign({ x1: A.x, y1: A.y, x2: B.x, y2: B.y }, attrs || {}), parent);
  }
  function poly(points, attrs, parent) { return scene.polyline(points, attrs, parent || axisLayer); }
  function overlaps(a, b) { return !(a.x2 < b.x1 || b.x2 < a.x1 || a.y2 < b.y1 || b.y2 < a.y1); }

  /* 关节轴：整条轴线 + 正方向一侧的箭头（关节轴的轴向） */
  function axisLine(P, dir, color, marker, len) {
    var a = FK.Vec.add(P, FK.Vec.scale(dir, -len));
    var b = FK.Vec.add(P, FK.Vec.scale(dir, len));
    seg(a, b, { stroke: color, "stroke-width": 3.2, "stroke-linecap": "round" }, axisLayer);
    seg(P, FK.Vec.add(P, FK.Vec.scale(dir, len * 0.86)),
      { stroke: color, "stroke-width": 3.2, "marker-end": "url(#" + marker + ")" }, axisLayer);
  }

  /* 三短划线：机械制图里表示两轴平行（画在公垂线与轴的交点处，方向沿公垂线） */
  function parallelMarks(P, dirNormal, color) {
    [0.06, 0.34, 0.62].forEach(function (s) {
      var half = layout.axisLength * 0.17;
      var c = FK.Vec.add(P, FK.Vec.scale(dirNormal, s * layout.axisLength));
      seg(FK.Vec.add(c, FK.Vec.scale(dirNormal, -half)),
        FK.Vec.add(c, FK.Vec.scale(dirNormal, half)),
        { stroke: color, "stroke-width": 2.4 }, axisLayer);
    });
  }

  /* 直角标记：沿公垂线方向、沿轴方向各取一条等长的屏幕边，拼成小方块 */
  function rightAngle(P, dirNormal, dirAxis, color) {
    var O = scene.project(P);
    var N = scene.project(FK.Vec.add(P, dirNormal));
    var T = scene.project(FK.Vec.add(P, dirAxis));
    function unit(p, q) {
      var dx = q.x - p.x, dy = q.y - p.y;
      var n = Math.sqrt(dx * dx + dy * dy);
      if (n < 1e-6) return null;
      return { x: dx / n, y: dy / n };
    }
    var un = unit(O, N), ut = unit(O, T);
    if (!un || !ut) return;
    var s = 14;
    var p1 = { x: O.x + un.x * s, y: O.y + un.y * s };
    var p2 = { x: p1.x + ut.x * s, y: p1.y + ut.y * s };
    var p3 = { x: O.x + ut.x * s, y: O.y + ut.y * s };
    poly([[p1.x, p1.y, 0], [p2.x, p2.y, 0], [p3.x, p3.y, 0]],
      { stroke: color, "stroke-width": 2, fill: "none" }, dimLayer);
  }

  /* 尺寸线：把公垂线抬离轴线一点，两端画斜线，中间写 a_{i−1} */
  function dimension(P, Q, color) {
    var A = scene.project(P), B = scene.project(Q);
    var dx = B.x - A.x, dy = B.y - A.y;
    var len = Math.sqrt(dx * dx + dy * dy);
    if (len < 26) return;
    var ux = dx / len, uy = dy / len;
    var nx = -uy, ny = ux;
    if (ny > 0) { nx = -nx; ny = -ny; }
    var off = 26;
    var a = { x: A.x + nx * off, y: A.y + ny * off };
    var b = { x: B.x + nx * off, y: B.y + ny * off };
    [A, B].forEach(function (src, i) {
      var tgt = i === 0 ? a : b;
      el("line", {
        x1: src.x, y1: src.y, x2: tgt.x, y2: tgt.y,
        stroke: color, "stroke-width": 1.2, "stroke-dasharray": "4 4", opacity: 0.6
      }, dimLayer);
    });
    el("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: color, "stroke-width": 1.8 }, dimLayer);
    var sx = (ux + nx) / Math.SQRT2, sy = (uy + ny) / Math.SQRT2;
    [a, b].forEach(function (p) {
      [-3.4, 3.4].forEach(function (t) {
        var cx = p.x + ux * t, cy = p.y + uy * t;
        el("line", {
          x1: cx - sx * 7, y1: cy - sy * 7, x2: cx + sx * 7, y2: cy + sy * 7,
          stroke: color, "stroke-width": 1.8
        }, dimLayer);
      });
    });
    var mp = { x: (a.x + b.x) / 2 + nx * 14, y: (a.y + b.y) / 2 + ny * 14 };
    richLabel(mp.x, mp.y + 5, [["a", 0, 17], ["i\u22121", 6, 11]], color, "middle");
    boxes.push({ x1: mp.x - 20, y1: mp.y - 12, x2: mp.x + 20, y2: mp.y + 14 });
  }

  function richLabel(x, y, parts, color, anchor) {
    var node = el("text", {
      x: x, y: y, fill: color, "font-size": 16, "text-anchor": anchor || "start",
      class: "fk-axis-label"
    }, labelLayer);
    parts.forEach(function (part) {
      var sp = document.createElementNS(svgNS, "tspan");
      sp.setAttribute("dy", part[1] || 0);
      sp.setAttribute("font-size", part[2] || 16);
      sp.textContent = part[0];
      node.appendChild(sp);
    });
    return node;
  }

  /* 标签避让：给出若干候选偏移，挑第一个不压已放标签的 */
  function place(p, text, font, color, prefs) {
    var w = text.length * font * 0.70 + 4;
    var h = font * 1.25;
    var chosen = null, best = Infinity;
    for (var i = 0; i < prefs.length; i += 1) {
      var x = p.x + prefs[i][0], y = p.y + prefs[i][1];
      var box = { x1: x - 3, y1: y - h + 2, x2: x + w + 3, y2: y + 4 };
      var hit = false;
      for (var k = 0; k < boxes.length; k += 1) { if (overlaps(box, boxes[k])) { hit = true; break; } }
      var cost = (hit ? 100 : 0) + i * 0.5;
      if (cost < best) { best = cost; chosen = box; }
      if (!hit) break;
    }
    if (!chosen) chosen = { x1: p.x + 10, y1: p.y - h + 2, x2: p.x + 10 + w, y2: p.y + 4 };
    boxes.push(chosen);
    var node = el("text", {
      x: chosen.x1 + 3, y: chosen.y1 + h - 4, fill: color, "font-size": font,
      class: "fk-axis-label"
    }, labelLayer);
    node.textContent = text;
    return node;
  }

  /* ---------------- 几何：由 (a, α, β, φ) 构造两条轴 ---------------- */
  function geometry() {
    var beta = state.beta * FK.DEG, phi = state.phi * FK.DEG, alpha = state.alpha * FK.DEG;
    var n = normalDir(beta, phi);
    var r1 = [0, 0, 1];
    var r2 = FK.M4.applyDir(FK.M4.rotAxis(n, alpha), r1);
    var cross = FK.Vec.cross(r1, r2);
    var P = [0, 0, 0];
    var Q = FK.Vec.scale(n, state.a);
    var cr = FK.Vec.len(cross);
    // 反解转角：模长 = 两轴夹角；符号由 n̂ = r̂₁×r̂₂ 的右手定则给出（与滑块的 α 正方向一致）
    var solvedAlpha = cr > 1e-9
      ? Math.atan2(cr, FK.Vec.dot(r1, r2)) * (state.alpha < 0 ? -1 : 1)
      : (FK.Vec.dot(r1, r2) > 0 ? 0 : Math.PI);
    return { beta: beta, phi: phi, n: n, r1: r1, r2: r2, P: P, Q: Q, cross: cross, solvedAlpha: solvedAlpha };
  }

  /* ---------------- 主绘制 ---------------- */
  function render() {
    gridLayer.replaceChildren();
    axisLayer.replaceChildren();
    dimLayer.replaceChildren();
    labelLayer.replaceChildren();
    boxes = [];
    layout.axisLength = state.axisLen;

    var g = geometry();
    var L = layout.axisLength;
    var parallel = Math.abs(Math.sin(g.solvedAlpha)) < 1e-9;

    /* 1) 取景：两条轴的端点、公垂线、外扩半径都纳入 */
    var pts = [[0, 0, 0], FK.Vec.scale(g.n, state.a + 0.26)];
    [g.P, g.Q].forEach(function (O) {
      [g.r1, g.r2].forEach(function (d) {
        pts.push(FK.Vec.add(O, FK.Vec.scale(d, L)));
        pts.push(FK.Vec.add(O, FK.Vec.scale(d, -L)));
      });
    });
    fitView(pts);
    scene.grid(Math.max(2, Math.round(L)), 1, null, gridLayer);

    /* 2) 两条关节轴 */
    axisLine(g.P, g.r1, "#475569", "mAxis1", L);
    axisLine(g.Q, g.r2, "#174ea6", "mAxis2", L);

    /* 3) 公垂线（从轴1 到轴2，长度恰为 a） */
    if (state.showNormal) {
      seg(g.P, g.Q, { stroke: "#b45309", "stroke-width": 5.4, "stroke-linecap": "round", "marker-end": "url(#mNormal)" }, dimLayer);
      var mid = FK.Vec.scale(FK.Vec.add(g.P, g.Q), 0.5);
      place(scene.project(mid), "公垂线", 14, "#8a4a08", [[16, -34], [16, 30], [-70, -34], [-70, 30]]);
      dimension(g.P, g.Q, "#b45309");
    }

    /* 4) 绕公垂线的转角 α：以公垂线为轴把 r₁ 转到 r₂ 的弧形箭头 */
    if (!parallel && Math.abs(state.alpha) > 1) {
      var radius = Math.max(0.30, state.a * 0.40);
      var arc = [];
      for (var i = 0; i <= 44; i += 1) {
        var t = (state.alpha * FK.DEG) * (i / 44);
        var v = FK.M4.applyDir(FK.M4.rotAxis(g.n, t), g.r1);
        arc.push(FK.Vec.add(g.P, FK.Vec.scale(v, radius)));
      }
      poly(arc, {
        stroke: "#7c3aed", "stroke-width": 2.6, fill: "none",
        "stroke-dasharray": "7 5", "marker-end": "url(#mAlpha)"
      }, dimLayer);
      var vm = FK.M4.applyDir(FK.M4.rotAxis(g.n, (state.alpha * FK.DEG) * 0.5), g.r1);
      var lp = scene.project(FK.Vec.add(g.P, FK.Vec.scale(vm, radius + 0.34)));
      var node = el("text", {
        x: lp.x - 14, y: lp.y + 4, fill: "#7c3aed", "font-size": 18, class: "fk-axis-label"
      }, labelLayer);
      node.textContent = "\u03b1";
      var sp = el("text", {
        x: lp.x - 14, y: lp.y + 22, fill: "#5b21b6", "font-size": 12.5, class: "fk-axis-label"
      }, labelLayer);
      sp.textContent = "\u03b1\u1d62\u208b\u2081 = " + FK.deg(state.alpha, 1);
      boxes.push({ x1: lp.x - 18, y1: lp.y - 12, x2: lp.x + 70, y2: lp.y + 26 });
    }

    /* 5) 直角标记（公垂线 ⊥ 两轴） */
    if (state.showRight && !parallel) {
      rightAngle(g.P, g.n, g.r1, "#b45309");
      rightAngle(g.Q, FK.Vec.scale(g.n, -1), g.r2, "#b45309");
    }

    /* 6) 平行时的三短划线 */
    if (parallel && state.showParallel) {
      parallelMarks(g.P, g.n, "#0e7490");
      parallelMarks(g.Q, g.n, "#0e7490");
      var tp = scene.project(FK.Vec.add(g.P, FK.Vec.scale(g.n, -L * 0.75)));
      var note = el("text", {
        x: tp.x - 80, y: tp.y + 4, fill: "#0e7490", "font-size": 13, class: "fk-axis-label"
      }, labelLayer);
      note.textContent = "\u2261 两轴平行：公垂线有无数条";
      boxes.push({ x1: tp.x - 84, y1: tp.y - 12, x2: tp.x + 92, y2: tp.y + 10 });
    }

    /* 7) 公垂线方向与轴名标注 */
    var np = scene.project(FK.Vec.scale(g.n, Math.max(0.14, state.a * 0.18)));
    el("text", {
      x: np.x + 9, y: np.y + 17, fill: "#b45309", "font-size": 15, "font-style": "italic", class: "fk-axis-label"
    }, labelLayer).textContent = "n\u0302";
    boxes.push({ x1: np.x + 5, y1: np.y + 3, x2: np.x + 30, y2: np.y + 21 });

    place(scene.project(FK.Vec.add(g.P, FK.Vec.scale(g.r1, L * 0.88))),
      "\u5173\u8282\u8f74 i\u22121", 14, "#475569", [[16, -4], [-104, -4], [16, 22], [-104, 22]]);
    place(scene.project(FK.Vec.add(g.Q, FK.Vec.scale(g.r2, L * 0.88))),
      "\u5173\u8282\u8f74 i", 14, "#174ea6", [[16, -4], [-88, -4], [16, 22], [-88, 22]]);

    if (!parallel) {
      seg(FK.Vec.add(g.P, FK.Vec.scale(g.n, state.a + 0.04)), FK.Vec.add(g.P, FK.Vec.scale(g.n, state.a + 0.30)),
        { stroke: "#0e7490", "stroke-width": 2.2, "marker-end": "url(#mDir)" }, dimLayer);
    }

    /* 8) 读数 */
    var d1 = FK.Vec.dot(g.n, g.r1), d2 = FK.Vec.dot(g.n, g.r2);
    var q = FK.Vec.sub(g.Q, g.P);
    var dist = FK.Vec.len(FK.Vec.cross(q, g.r2));
    document.getElementById("roA").textContent = FK.format(state.a, 3);
    document.getElementById("roAlpha").textContent = FK.deg(state.alpha, 1);
    document.getElementById("roBeta").textContent = FK.deg(state.beta, 1);
    document.getElementById("roMeas").textContent = FK.deg(g.solvedAlpha / FK.DEG, 1);
    document.getElementById("roSin").textContent = FK.format(FK.Vec.len(g.cross), 3);
    document.getElementById("roDot").textContent = FK.format(FK.Vec.dot(g.r1, g.r2), 3);
    document.getElementById("roD1").textContent = FK.format(d1, 3);
    document.getElementById("roD2").textContent = FK.format(d2, 3);
    document.getElementById("roDist").textContent = FK.format(dist, 3);
    document.getElementById("roSign").textContent = parallel
      ? "α = " + FK.deg(state.alpha, 1) + "：两轴平行或反向平行，公垂线有无穷多条、长度都是 a = " + FK.format(state.a, 3)
      : "α 的正方向：右手拇指指向 n̂（从轴 i−1 指向轴 i 的公垂线方向），四指从轴 i−1 卷向轴 i；当前实测 "
        + FK.deg(g.solvedAlpha / FK.DEG, 1);

    var note = document.getElementById("specialNote");
    if (Math.abs(state.alpha) < 1e-9) {
      note.className = "note warn";
      note.innerHTML = "<b>特殊情况 α = 0°</b>：两轴互相平行 → 公垂线不唯一（存在无数条等长的公垂线），图中画三短划线表示平行。";
    } else if (Math.abs(Math.abs(state.alpha) - 180) < 1e-9) {
      note.className = "note warn";
      note.innerHTML = "<b>特殊情况 α = 180°</b>：两轴反向平行（作为两条直线仍然平行）→ 公垂线同样不唯一，三短划线表示平行。";
    } else {
      note.className = "note";
      note.innerHTML = "两轴不平行时公垂线<b>只有一条</b>：它同时垂直于两轴（图中两个直角小方块），长度 = a<sub>i−1</sub> = "
        + FK.format(state.a, 3) + "；绕它把轴 i−1 转到轴 i 的角度 = α<sub>i−1</sub> = " + FK.deg(state.alpha, 1) + "。";
    }
  }

  /* 把内容按 FIT 矩形等比装进去（先算投影包围盒，再定 scale 与 origin） */
  function fitView(points) {
    var yaw = scene.state.yaw, pitch = scene.state.pitch;
    var cy = Math.cos(yaw), sy = Math.sin(yaw);
    var cp = Math.cos(pitch), sp = Math.sin(pitch);
    function u(v) { return v[0] * cy - v[1] * sy; }
    function s(v) { return -((v[0] * sy + v[1] * cy) * sp + v[2] * cp); }
    var uMin = Infinity, uMax = -Infinity, sMin = Infinity, sMax = -Infinity;
    for (var i = 0; i < points.length; i += 1) {
      var uu = u(points[i]), ss = s(points[i]);
      if (uu < uMin) uMin = uu;
      if (uu > uMax) uMax = uu;
      if (ss < sMin) sMin = ss;
      if (ss > sMax) sMax = ss;
    }
    var spanU = Math.max(0.6, uMax - uMin);
    var spanS = Math.max(0.6, sMax - sMin);
    var scale = Math.max(34, Math.min(210, FIT.w / spanU, FIT.h / spanS));
    scene.state.scale = scale;
    scene.origin.x = FIT.cx - (uMin + uMax) * scale / 2;
    scene.origin.y = FIT.cy - (sMin + sMax) * scale / 2;
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "a", key: "a", value: DEFAULTS.a, format: function (v) { return FK.format(v, 2); } },
    { id: "alpha", key: "alpha", value: DEFAULTS.alpha, format: function (v) { return FK.deg(v, 1); } },
    { id: "beta", key: "beta", value: DEFAULTS.beta, format: function (v) { return FK.deg(v, 1); } },
    { id: "phi", key: "phi", value: DEFAULTS.phi, format: function (v) { return FK.deg(v, 0); } },
    { id: "axisLen", key: "axisLen", value: DEFAULTS.axisLen, format: function (v) { return FK.format(v, 2); } }
  ], state, function () { render(); });

  FK.bindToggles([
    { id: "showNormal", key: "showNormal" },
    { id: "showRight", key: "showRight" },
    { id: "showParallel", key: "showParallel" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.a = DEFAULTS.a; state.alpha = DEFAULTS.alpha;
    state.beta = DEFAULTS.beta; state.phi = DEFAULTS.phi; state.axisLen = DEFAULTS.axisLen;
    state.showNormal = true; state.showRight = true; state.showParallel = true; state.auto = false;
    document.getElementById("showNormal").checked = true;
    document.getElementById("showRight").checked = true;
    document.getElementById("showParallel").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    render();
  });

  /* ---------------- 教材数值自检 ---------------- */
  (function selfTest() {
    var RAD = FK.DEG;
    function geoOf(a, alphaDeg, betaDeg, phiDeg) {
      var n = normalDir(betaDeg * RAD, phiDeg * RAD);
      var r1 = [0, 0, 1];
      var r2 = FK.M4.applyDir(FK.M4.rotAxis(n, alphaDeg * RAD), r1);
      return { n: n, r1: r1, r2: r2, P: [0, 0, 0], Q: FK.Vec.scale(n, a) };
    }
    function close(x, y, eps) { return Math.abs(x - y) < (eps === undefined ? 1e-9 : eps); }
    function lineDistance(P, r1, Q, r2) {
      var c = FK.Vec.cross(r1, r2);
      var cn = FK.Vec.len(c);
      if (cn < 1e-9) return FK.Vec.len(FK.Vec.cross(FK.Vec.sub(Q, P), r1));
      return Math.abs(FK.Vec.dot(FK.Vec.sub(Q, P), FK.Vec.scale(c, 1 / cn)));
    }

    var g = geoOf(1, 45, 60, 25);
    // 1) 公垂线同时垂直于两轴
    if (!close(FK.Vec.dot(g.n, g.r1), 0) || !close(FK.Vec.dot(g.n, g.r2), 0)) {
      throw new Error("公垂线应同时垂直于两轴，实得 " + FK.Vec.dot(g.n, g.r1) + " / " + FK.Vec.dot(g.n, g.r2));
    }
    // 2) 绕公垂线转 α 后轴2 的方向 = R(n̂, α)·轴1 方向（这正是 α 的定义）
    if (!FK.Vec.eq(g.r2, FK.M4.applyDir(FK.M4.rotAxis(g.n, 45 * RAD), g.r1), 1e-12)) {
      throw new Error("α 应是把轴 i−1 绕公垂线转到轴 i 的角");
    }
    // 3) 两轴夹角 = α，且 |r̂₁×r̂₂| = sin α
    if (!close(FK.Vec.len(FK.Vec.cross(g.r1, g.r2)), Math.sin(45 * RAD))) {
      throw new Error("|r̂₁×r̂₂| 应为 sin α，实得 " + FK.Vec.len(FK.Vec.cross(g.r1, g.r2)));
    }
    if (!close(Math.acos(Math.max(-1, Math.min(1, FK.Vec.dot(g.r1, g.r2)))) / RAD, 45, 1e-9)) {
      throw new Error("两轴夹角应等于 α = 45°");
    }
    // 4) 公垂线长度 = a：轴2 上任意点到轴1 的距离都是 a
    if (!close(lineDistance(g.P, g.r1, g.Q, g.r2), 1)) {
      throw new Error("两轴距离应为 a = 1，实得 " + lineDistance(g.P, g.r1, g.Q, g.r2));
    }
    if (!close(lineDistance(g.P, g.r1, FK.Vec.add(g.Q, FK.Vec.scale(g.r2, 1.7)), g.r2), 1, 1e-9)) {
      throw new Error("轴2 上任意点到轴1 的距离都应为 a");
    }
    // 5) 反解：由两轴本身求出 n̂ 与 α，应与构造值一致
    var got = geoOf(0.7, -120, 40, 200);
    var cr = FK.Vec.cross(got.r1, got.r2);
    if (!close(Math.atan2(FK.Vec.len(cr), FK.Vec.dot(got.r1, got.r2)) / RAD, 120, 1e-9)) {
      throw new Error("反解 α 应为 +120°（转角取 0°~180°），实得 "
        + Math.atan2(FK.Vec.len(cr), FK.Vec.dot(got.r1, got.r2)) / RAD);
    }
    if (!FK.Vec.eq(FK.Vec.round(FK.Vec.normalize(cr), 9), FK.Vec.round(got.n, 9), 1e-9)) {
      throw new Error("n̂ = r̂₁×r̂₂ 应与构造的公垂线方向一致");
    }
    // 6) 特殊情况 α = 0 / 180：两轴平行或反向平行（|r̂₁×r̂₂| = 0），公垂线不唯一
    var g0 = geoOf(1, 0, 60, 25);
    if (FK.Vec.len(FK.Vec.cross(g0.r1, g0.r2)) > 1e-12 || !close(FK.Vec.dot(g0.r1, g0.r2), 1)) {
      throw new Error("α = 0° 时两轴应平行同向");
    }
    var g180 = geoOf(1, 180, 60, 25);
    if (FK.Vec.len(FK.Vec.cross(g180.r1, g180.r2)) > 1e-12 || !close(FK.Vec.dot(g180.r1, g180.r2), -1)) {
      throw new Error("α = 180° 时两轴应反向平行");
    }
    // 7) α 变号不改变两轴作为直线的夹角与距离
    [-180, -135, -90, 90, 135].forEach(function (deg) {
      var gp = geoOf(1, deg, 60, 25), gm = geoOf(1, -deg, 60, 25);
      if (!close(FK.Vec.len(FK.Vec.cross(gp.r1, gp.r2)), FK.Vec.len(FK.Vec.cross(gm.r1, gm.r2)), 1e-12)) {
        throw new Error("α 与 −α 的两轴夹角应相同（" + deg + "）");
      }
      if (!close(lineDistance(gp.P, gp.r1, gp.Q, gp.r2), 1)) throw new Error("±α 时距离都应为 a");
    });
  }());

  render();
}());
"""

FIGURE = {
    "id": "figure-3-2",
    "title": "图3-2 连杆长度 a 与转角 α · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
