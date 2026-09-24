"""图2-13 相对于坐标系{A}的坐标系{B}（克雷格《机器人学导论（第3版）》例2.5，逆变换）。

教材依据：
- 例2.5 原文：“图2-13表示坐标系 {B} 绕坐标系 {A} 的 Ẑ 轴旋转 30 度，沿 X̂_A 平移 4 个单位，
  沿 Ŷ_A 平移 3 个单位，于是得到 ᴬ_BT，求 ᴮ_AT。”
- 式(2-42)：ᴮ_AR = ᴬ_BRᵀ；式(2-44)：ᴮP_AORG = −ᴬ_BRᵀ·ᴬP_BORG；
  式(2-45)：ᴮ_AT = [ ᴬ_BRᵀ , −ᴬ_BRᵀ·ᴬP_BORG ; 0 0 0 1 ]，即 ᴬ_BT⁻¹。
- 式(2-47)：例2.5 的解 ᴮ_AT 的平移列 = (−4.964, −0.598, 0)。
- 脚本自检（3 条）：
  1) 教材例2.5 数值（θ=30°、ᴬP_BORG=(4,3,0)）代入式(2-45) 必须得到式(2-47) 的矩阵；
  2) 把例2.2 的 ᴬP=(9.098,12.562,0) 代回 ᴮP=ᴬ_BT⁻¹·ᴬP 必须得到 ᴮP=(3,7,0)；
  3) FK.M4.inverse(ᴬ_BT) 必须与式(2-45) 的构造结果逐元素一致。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.control-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 7px 10px; margin-top: 9px; }
.control-grid .control { margin-top: 0; min-width: 0; }
.control-grid .control-head { display: block; line-height: 1.3; }
.control-grid .control-head output { display: block; font-size: 11.5px; }
.control-grid .control label { font-size: 11.5px; }
.control-grid input[type="range"] { margin: 3px 0 1px; height: 3px; }
.options-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 5px 10px; margin-top: 10px; }
.options-grid label { display: inline-flex; align-items: center; gap: 5px; color: #4a5a72; font-size: 11.5px; cursor: pointer; white-space: nowrap; }
.options-grid input { accent-color: var(--blue); flex: none; }
.panel .legend { gap: 4px 10px; }
.mode-tabs { margin-top: 10px; }

.matrix {
  position: absolute;
  right: 16px;
  bottom: 288px;
  left: auto;
  width: 300px;
  padding: 7px 10px 8px;
  border: 1px solid rgba(30, 64, 175, 0.12);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 10px 26px rgba(30, 64, 175, 0.10);
  font: 11.5px/1.38 ui-monospace, SFMono-Regular, Consolas, monospace;
  color: #334155;
}
.matrix .cap { font-size: 11.5px; color: #174ea6; font-weight: 700; margin-bottom: 2px; }
.matrix + .matrix { bottom: 140px; }
.matrix .row { white-space: pre; }
.matrix .b { color: #94a3b8; }
.matrix .r { color: #b3261e; }
.matrix .t { color: #5b21b6; font-weight: 700; }
.matrix .h { color: #12944f; }
.matrix .inv { color: #0e7490; }
.matrix.is-hidden { display: none; }

@media (max-width: 720px) {
  .panel h1 { font-size: 14px; }
  .mode-tabs { flex-direction: column; }
  .mode-tabs button { width: 100%; }
  .control-grid { gap: 5px 8px; }
  .control-grid .control label, .control-grid .control-head output { font-size: 10.5px; }
  .options-grid { gap: 4px 8px; }
  .options-grid label { font-size: 10.5px; }
  .panel .legend { font-size: 10.5px; gap: 3px 8px; }
  .readout { font-size: 11px; line-height: 1.4; padding: 5px 7px; max-width: calc(100% - 16px); }
  .readout .small { font-size: 9.5px; }
  .matrix {
    right: 8px; top: 104px; bottom: auto; left: 8px; width: auto;
    font-size: 9.5px; line-height: 1.3; padding: 5px 7px;
    overflow: hidden;
  }
  .matrix + .matrix { top: 214px; bottom: auto; }
  .matrix .cap { font-size: 10px; }
  .matrix .small { display: none; }
}

/* 移动端收尾：确保 390px 宽下不出现横向溢出、面板与读数都收在视口内 */
html, body { overflow-x: hidden; }
.app { max-width: 100vw; }
@media (max-width: 720px) {
  .panel { overflow-x: hidden; }
  .panel h1 { font-size: 13.5px; }
  .legend { font-size: 10px; gap: 3px 7px; }
  .legend span { white-space: nowrap; }
  .options-grid label { font-size: 10px; }
  .readout { max-width: calc(100% - 16px); overflow-wrap: anywhere; }
}

/* 移动端硬性约束：任何块都不得超出 390px 视口 */
@media (max-width: 720px) {
  .readout {
    max-width: calc(100vw - 16px) !important;
    white-space: normal !important;
    word-break: break-word;
  }
  .readout .row { white-space: normal !important; }
  .panel { max-width: calc(100vw - 16px) !important; }
  .matrix { max-width: calc(100vw - 16px) !important; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="逆变换：由坐标系B相对A的齐次变换求A相对B的变换的交互示意图">
  <defs>
    <marker id="mAxis" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"></path>
    </marker>
    <marker id="mBx" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="mBy" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="mBz" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.2" markerHeight="6.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="mFwd" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="mInv" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0e7490"></path>
    </marker>
    <marker id="mT" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="axesA"></g>
  <g id="frameB"></g>
  <g id="vectorLayer"></g>
  <g id="angleLayer"></g>
  <g id="labelLayer"></g>
</svg>

<section class="panel" aria-label="图2-13 控制面板">
  <div class="panel-head">
    <div>
      <h1>图2-13 相对{A}的坐标系{B}（逆变换）</h1>
      <p class="subtitle">例2.5：ᴬ_BT 已知，求 ᴮ_AT。式(2-45) 用“旋转取转置 + 平移写成 −ᴬ_BRᵀ·ᴬP_BORG”求逆，比直接对 4×4 求逆更省算；它与图2-8 的 ᴬP = ᴬ_BT·ᴮP 正好互为反向。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="mode-tabs tabs">
    <button id="modeFwd" type="button" class="is-active">正向 ᴬP = ᴬ_BT·ᴮP</button>
    <button id="modeInv" type="button">逆向 ᴮP = ᴬ_BT⁻¹·ᴬP</button>
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="theta">旋转角 θ</label><output id="thetaValue">30.0°</output></div>
      <input id="theta" type="range" min="-180" max="180" step="1" value="30">
    </div>
    <div class="control">
      <div class="control-head"><label for="bx">平移 x</label><output id="bxValue">10.0</output></div>
      <input id="bx" type="range" min="-10" max="10" step="0.5" value="10">
    </div>
    <div class="control">
      <div class="control-head"><label for="by">平移 y</label><output id="byValue">5.0</output></div>
      <input id="by" type="range" min="-10" max="10" step="0.5" value="5">
    </div>
    <div class="control">
      <div class="control-head"><label for="vx" id="vxLabel">ᴮP x</label><output id="vxValue">3.0</output></div>
      <input id="vx" type="range" min="-10" max="10" step="0.01" value="3">
    </div>
    <div class="control">
      <div class="control-head"><label for="vy" id="vyLabel">ᴮP y</label><output id="vyValue">7.0</output></div>
      <input id="vy" type="range" min="-10" max="10" step="0.01" value="7">
    </div>
    <div class="control">
      <div class="control-head"><label for="vz" id="vzLabel">ᴮP z</label><output id="vzValue">0.0</output></div>
      <input id="vz" type="range" min="-6" max="6" step="0.01" value="0">
    </div>
  </div>

  <div class="options-grid">
    <label><input id="showT" type="checkbox" checked>矩阵</label>
    <label><input id="showComp" type="checkbox" checked>分量虚线</label>
    <label><input id="auto" type="checkbox">自动旋转</label>
  </div>

  <div class="legend">
    <span><i style="background:#64748b"></i>坐标系{A}</span>
    <span><i style="background:#d93025"></i>坐标系{B}</span>
    <span><i class="dot" style="background:#c26a10"></i>正向 ᴬP</span>
    <span><i class="dot" style="background:#0e7490"></i>逆向 ᴮP</span>
    <span><i style="background:#7c3aed"></i>ᴬP_BORG / ᴮP_AORG</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>

<div class="matrix" id="matrixT">
  <div class="cap">ᴬ_BT（式2-45 的输入，例2.5 式2-46）</div>
  <div id="rowsA"></div>
</div>

<div class="matrix" id="matrixInv">
  <div class="cap">ᴮ_AT = ᴬ_BT⁻¹（式2-45，例2.5 式2-47）</div>
  <div id="rowsB"></div>
  <div class="small" style="font-size:10.5px;color:#65748b">平移列 = −ᴬ_BRᵀᴬP_BORG = ᴮP_AORG</div>
</div>

<div class="readout">
  <div class="row"><strong id="inLabel">ᴮP</strong> = [ <span id="i1">3.00</span>, <span id="i2">7.00</span>, <span id="i3">0.00</span> ]ᵀ <span class="small">（给定）</span></div>
  <div class="row"><strong id="outLabel">ᴬP</strong> = [ <span id="o1">9.098</span>, <span id="o2">12.562</span>, <span id="o3">0.000</span> ]ᵀ <span class="small">（结果）</span></div>
  <div class="row small">ᴬP_BORG = [ <span id="t1">10.000</span>, <span id="t2">5.000</span>, 0.000 ]ᵀ　·　ᴮP_AORG = [ <span id="u1">-4.964</span>, <span id="u2">-0.598</span>, 0.000 ]ᵀ</div>
  <div class="row small">教材例2.5 对照：平移 (4,3) 时 ᴮP_AORG = [ <span id="e1">-4.964</span>, <span id="e2">-0.598</span>, 0 ]ᵀ（与上一致）</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var axesA = document.getElementById("axesA");
  var frameB = document.getElementById("frameB");
  var vectorLayer = document.getElementById("vectorLayer");
  var angleLayer = document.getElementById("angleLayer");
  var labelLayer = document.getElementById("labelLayer");

  /* 取景矩形（viewBox 1000x620）。桌面 1200x700：viewBox x 0..1000 → 屏幕 34..1537，y 0..620 → 7..691；
     面板占左侧（viewBox x<~180），两块矩阵占右侧偏下（viewBox x>650, y>380）。 */
  var FIT = { cx: 470, cy: 210, w: 520, h: 330 };
  var scene = new FK.Scene({ svg: viewport, origin: { x: FIT.cx, y: FIT.cy }, scale: 40, yaw: -0.62, pitch: 0.42 });
  var state = {
    mode: "fwd",
    theta: 30, Bx: 10, By: 5,
    vx: 3, vy: 7, vz: 0,
    showT: true, showComp: true, auto: false
  };

  var COLORS = {
    A: "#64748b", Bx: "#d93025", By: "#2563eb", Bz: "#12944f",
    comp: "#a9b6c9", trans: "#7c3aed", fwd: "#c26a10", inv: "#0e7490"
  };

  var UC = [0.86, -0.50];
  var WC = [0.50, 0.86];
  function projU(v) { return UC[0] * v[0] + UC[1] * v[1]; }
  function projW(v) { return WC[0] * v[0] + WC[1] * v[1]; }

  function fitView(points) {
    var uMin = Infinity, uMax = -Infinity, sMin = Infinity, sMax = -Infinity;
    for (var i = 0; i < points.length; i += 1) {
      var u = projU(points[i]);
      var s = -projW(points[i]);
      if (u < uMin) uMin = u;
      if (u > uMax) uMax = u;
      if (s < sMin) sMin = s;
      if (s > sMax) sMax = s;
    }
    var scale = Math.max(12, Math.min(52, FIT.w / Math.max(0.5, uMax - uMin), FIT.h / Math.max(0.5, sMax - sMin)));
    scene.state.scale = scale;
    scene.origin.x = scene.baseOrigin.x = FIT.cx - (uMin + uMax) * scale / 2;
    scene.origin.y = scene.baseOrigin.y = FIT.cy - (sMin + sMax) * scale / 2;
  }

  /* ---------------- 标签避让 ---------------- */
  var RESERVED = [
    { x1: -500, y1: -500, x2: 180, y2: 800 },
    { x1: 640, y1: 380, x2: 1400, y2: 800 }
  ];
  var boxes = [];
  function overlaps(a, b) { return !(a.x2 < b.x1 || b.x2 < a.x1 || a.y2 < b.y1 || b.y2 < a.y1); }
  function place(p, text, font, color, prefs, cls, layer, extra) {
    var w = text.length * font * 0.72 + 4;
    var h = font * 1.25;
    var chosen = null, penalty = Infinity;
    for (var i = 0; i < prefs.length; i += 1) {
      var x = p.x + prefs[i][0];
      if (prefs[i].length > 2 && prefs[i][2] !== undefined && x < prefs[i][2]) x = prefs[i][2];
      var grow = i * 4;
      var box = {
        x1: x - grow, y1: p.y + prefs[i][1] - h + 3 - grow,
        x2: x + w + grow, y2: p.y + prefs[i][1] + 3 + grow
      };
      var hit = false;
      for (var j = 0; j < RESERVED.length; j += 1) { if (overlaps(box, RESERVED[j])) { hit = true; break; } }
      for (var k = 0; !hit && k < boxes.length; k += 1) { if (overlaps(box, boxes[k])) hit = true; }
      var cost = (hit ? 100 : 0) + i + grow / 10;
      if (cost < penalty) { penalty = cost; chosen = box; }
      if (!hit) break;
    }
    if (!chosen) { chosen = { x1: p.x, y1: p.y - h + 3, x2: p.x + w, y2: p.y + 3 }; }
    boxes.push(chosen);
    var attrs = { x: chosen.x1, y: chosen.y1 + h - 4, fill: color, "font-size": font, class: cls || "fk-point-label" };
    if (extra) { Object.keys(extra).forEach(function (key) { attrs[key] = extra[key]; }); }
    var node = scene.el("text", attrs, layer || labelLayer);
    node.textContent = text;
    return node;
  }

  function drawAxes(layer, matrix, spec) {
    var dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    for (var i = 0; i < 3; i += 1) {
      var base = scene.project(FK.M4.apply(matrix, [0, 0, 0]));
      var tip = scene.project(FK.M4.apply(matrix, FK.Vec.scale(dirs[i], spec.length)));
      scene.el("line", {
        x1: base.x, y1: base.y, x2: tip.x, y2: tip.y,
        stroke: spec.colors[i], "stroke-width": spec.width,
        "marker-end": "url(#" + spec.markers[i] + ")"
      }, layer);
      var vx = tip.x - base.x, vy = tip.y - base.y;
      var vl = Math.max(1e-6, Math.sqrt(vx * vx + vy * vy));
      var ux = vx / vl, uy = vy / vl, off = spec.font * 0.72;
      place(tip, spec.labels[i], spec.font, spec.colors[i], [
        [spec.dx[i], spec.dy[i]],
        [ux * off, uy * off + spec.font * 0.42],
        [-uy * off - spec.font * 0.62, ux * off],
        [uy * off, -ux * off + spec.font * 0.42],
        [-ux * off - spec.font * 0.9, uy * off],
        [spec.dx[i], spec.dy[i]]
      ], "fk-axis-label", layer, { "font-style": "italic" });
    }
    var o = scene.project(FK.M4.apply(matrix, [0, 0, 0]));
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.2, fill: spec.originFill || "#334155" }, layer);
    if (spec.originLabel) {
      place(o, spec.originLabel, 15, spec.originFill || "#475569",
        spec.originPrefs || [[-40, -8], [-40, 28], [14, 28], [14, -8]], "fk-origin-label");
    }
  }

  function drawComponent(from, to) {
    var a = scene.project(from), b = scene.project(to);
    scene.el("line", {
      x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: COLORS.comp,
      "stroke-dasharray": "7 6", "stroke-width": 2, class: "fk-projection"
    }, vectorLayer);
  }

  function drawArrow(from, to, color, marker, labelText, prefs, font) {
    var a = scene.project(from), b = scene.project(to);
    scene.el("line", {
      x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: color,
      "stroke-width": 4.0, "marker-end": "url(#" + marker + ")"
    }, vectorLayer);
    scene.el("circle", { cx: b.x, cy: b.y, r: 6.6, fill: color, class: "fk-point" }, vectorLayer);
    place(b, labelText, font || 19, color, prefs);
  }

  /* 按行渲染 4×4 矩阵（直接拼字符串，保证显示值与计算值一致） */
  function matrixRowsHTML(M, cls) {
    var html = "";
    for (var r = 0; r < 4; r += 1) {
      var c = r < 3 ? cls : "h";
      html += '<div class="row"><span class="b">[</span> ' +
        '<span class="' + c + '">' + FK.format(M[r * 4], 3) + '</span>  ' +
        '<span class="' + c + '">' + FK.format(M[r * 4 + 1], 3) + '</span>  ' +
        '<span class="' + c + '">' + FK.format(M[r * 4 + 2], 3) + '</span>   ' +
        '<span class="' + (r < 3 ? "t" : "h") + '">' + FK.format(M[r * 4 + 3], 3) + '</span> ' +
        '<span class="b">]</span></div>';
    }
    return html;
  }

  function render() {
    gridLayer.replaceChildren();
    axesA.replaceChildren();
    frameB.replaceChildren();
    vectorLayer.replaceChildren();
    angleLayer.replaceChildren();
    labelLayer.replaceChildren();
    boxes = [];

    var theta = state.theta * FK.DEG;
    var Rab = FK.M4.rotZ(theta);
    var PBORG = [state.Bx, state.By, 0];
    var T = FK.M4.fromRT(FK.M4.rotation(Rab), PBORG);   // ᴬ_BT
    var Tinv = FK.M4.inverse(T);                        // ᴮ_AT（式2-45 / 式2-42+2-44）
    var PAORG = [Tinv[3], Tinv[7], Tinv[11]];           // ᴮP_AORG = −ᴬ_BRᵀᴬP_BORG

    var given = [state.vx, state.vy, state.vz];
    var fwd = state.mode === "fwd";
    var PB = fwd ? given : FK.M4.apply(Tinv, given);
    var PA = fwd ? FK.M4.apply(T, given) : given;

    var ak = 2.6;
    fitView([
      [0, 0, 0], PA, PBORG, PAORG, PB,
      [ak, 0, 0], [-ak, 0, 0], [0, ak, 0], [0, -ak, 0], [0, 0, ak], [0, 0, -ak]
    ]);
    scene.grid(3, 1);

    drawAxes(axesA, FK.M4.identity(), {
      length: 2.6, width: 3.0, font: 18,
      labels: ["X\u0302\u2090", "Y\u0302\u2090", "Z\u0302\u2090"],
      colors: [COLORS.A, COLORS.A, COLORS.A], markers: ["mAxis", "mAxis", "mAxis"],
      dx: [10, 10, 12], dy: [-6, -6, -6], originLabel: "O"
    });

    drawAxes(frameB, T, {
      length: 2.4, width: 3.0, font: 18,
      labels: ["X\u0302\u1d47", "Y\u0302\u1d47", "Z\u0302\u1d47"],
      colors: [COLORS.Bx, COLORS.By, COLORS.Bz], markers: ["mBx", "mBy", "mBz"],
      dx: [9, 10, 11], dy: [-5, -6, -44], originLabel: "O\u2032",
      originPrefs: [[16, 30], [-36, 30], [-36, -8], [16, -8]]
    });

    // 平移矢量：ᴬP_BORG（O→O′，紫）与 ᴮP_AORG（O′→O，青）
    var a0 = scene.project([0, 0, 0]), a1 = scene.project(PBORG);
    scene.el("line", {
      x1: a0.x, y1: a0.y, x2: a1.x, y2: a1.y, stroke: COLORS.trans,
      "stroke-width": 3.2, "marker-end": "url(#mT)"
    }, vectorLayer);
    scene.el("circle", { cx: a1.x, cy: a1.y, r: 4.2, fill: COLORS.trans }, vectorLayer);
    place(a1, "\u1d2cP_BORG", 15, "#5b21b6", [[-84, 28, 200], [12, 28], [-84, -10], [12, -12]]);
    place(scene.project(PAORG), "\u1d2eP_AORG", 15, COLORS.inv, [[-84, 28], [-84, -10], [12, 26]]);

    if (state.showComp) {
      var tip = fwd ? PA : PB;
      var org = fwd ? [0, 0, 0] : PBORG;
      drawComponent(org, [org[0] + tip[0], org[1], org[2]]);
      drawComponent([org[0] + tip[0], org[1], org[2]], [org[0] + tip[0], org[1] + tip[1], org[2]]);
      drawComponent([org[0] + tip[0], org[1] + tip[1], org[2]], [org[0] + tip[0], org[1] + tip[1], org[2] + tip[2]]);
    }

    if (fwd) {
      // ᴮP 在 {B} 中：从 O′ 出发
      var s0 = scene.project(PBORG), s1 = scene.project(PA);
      scene.el("line", {
        x1: s0.x, y1: s0.y, x2: s1.x, y2: s1.y, stroke: COLORS.Bx,
        "stroke-width": 2.4, "stroke-dasharray": "9 5", opacity: 0.85, "marker-end": "url(#mBx)"
      }, vectorLayer);
      place(s1, "\u1d2eP", 16, "#a02a20", [[-42, -10], [-42, 22], [12, -12]]);
      drawArrow([0, 0, 0], PA, COLORS.fwd, "mFwd", "\u1d2cP", [[16, -18, 540], [16, 18, 540], [-44, -20]]);
    } else {
      // ᴬP 在 {A} 中：从 O 出发；同时显示由 {B} 描述的 ᴮP 箭头
      drawArrow([0, 0, 0], PA, COLORS.fwd, "mFwd", "\u1d2cP（给定）", [[16, -18, 520], [16, 18, 520], [-96, -20]], 17);
      drawArrow(PBORG, PA, COLORS.inv, "mInv", "\u1d2eP", [[14, -14], [-40, -14], [14, 18]]);
    }

    // 旋转弧
    if (Math.abs(theta) > 1e-4) {
      var steps = 44, points = [];
      for (var i = 0; i <= steps; i += 1) {
        var t = theta * (i / steps);
        points.push([1.15 * Math.cos(t), 1.15 * Math.sin(t), 0]);
      }
      scene.polyline(points, { stroke: "#7c3aed", class: "fk-arc" }, angleLayer);
      place(scene.project([1.75 * Math.cos(theta / 2), 1.75 * Math.sin(theta / 2), 0]),
        "\u03b8", 16, "#7c3aed", [[-12, 22], [8, 6], [-12, -6]]);
    }

    // 矩阵
    document.getElementById("rowsA").innerHTML = matrixRowsHTML(T, "r");
    document.getElementById("rowsB").innerHTML = matrixRowsHTML(Tinv, "inv");
    document.getElementById("matrixT").classList.toggle("is-hidden", !state.showT);
    document.getElementById("matrixInv").classList.toggle("is-hidden", !state.showT);

    // 读数
    document.getElementById("inLabel").textContent = fwd ? "\u1d2eP" : "\u1d2cP";
    document.getElementById("outLabel").textContent = fwd ? "\u1d2cP" : "\u1d2eP";
    document.getElementById("i1").textContent = FK.format(given[0], 2);
    document.getElementById("i2").textContent = FK.format(given[1], 2);
    document.getElementById("i3").textContent = FK.format(given[2], 2);
    var out = fwd ? PA : PB;
    document.getElementById("o1").textContent = FK.format(out[0], 3);
    document.getElementById("o2").textContent = FK.format(out[1], 3);
    document.getElementById("o3").textContent = FK.format(out[2], 3);
    document.getElementById("t1").textContent = FK.format(PBORG[0], 3);
    document.getElementById("t2").textContent = FK.format(PBORG[1], 3);
    document.getElementById("u1").textContent = FK.format(PAORG[0], 3);
    document.getElementById("u2").textContent = FK.format(PAORG[1], 3);
    // 教材例2.5 对照值（θ 与平移取例2.5 的 30°、(4,3)）
    var Tinv25 = FK.M4.inverse(FK.M4.fromRT(FK.M4.rotation(FK.M4.rotZ(30 * FK.DEG)), [4, 3, 0]));
    document.getElementById("e1").textContent = FK.format(Tinv25[3], 3);
    document.getElementById("e2").textContent = FK.format(Tinv25[7], 3);

    document.getElementById("vxLabel").textContent = fwd ? "\u1d2eP x" : "\u1d2cP x";
    document.getElementById("vyLabel").textContent = fwd ? "\u1d2eP y" : "\u1d2cP y";
    document.getElementById("vzLabel").textContent = fwd ? "\u1d2eP z" : "\u1d2cP z";
  }

  scene.setRenderer(render);

  function switchMode(mode) {
    if (state.mode === mode) return;
    var Tinv = FK.M4.inverse(FK.M4.fromRT(FK.M4.rotation(FK.M4.rotZ(state.theta * FK.DEG)), [state.Bx, state.By, 0]));
    var cur = state.mode === "fwd"
      ? FK.M4.apply(FK.M4.fromRT(FK.M4.rotation(FK.M4.rotZ(state.theta * FK.DEG)), [state.Bx, state.By, 0]), [state.vx, state.vy, state.vz])
      : FK.M4.apply(Tinv, [state.vx, state.vy, state.vz]);
    state.mode = mode;
    state.vx = cur[0];
    state.vy = cur[1];
    state.vz = cur[2];
    document.getElementById("modeFwd").classList.toggle("is-active", mode === "fwd");
    document.getElementById("modeInv").classList.toggle("is-active", mode === "inv");
    ranges.refresh();
    render();
  }

  var ranges = FK.bindRanges([
    { id: "theta", key: "theta", value: 30, format: function (v) { return FK.deg(v, 1); } },
    { id: "bx", key: "Bx", value: 10, format: function (v) { return FK.format(v, 1); } },
    { id: "by", key: "By", value: 5, format: function (v) { return FK.format(v, 1); } },
    { id: "vx", key: "vx", value: 3, format: function (v) { return FK.format(v, 2); } },
    { id: "vy", key: "vy", value: 7, format: function (v) { return FK.format(v, 2); } },
    { id: "vz", key: "vz", value: 0, format: function (v) { return FK.format(v, 2); } }
  ], state, render);

  FK.bindToggles([
    { id: "showT", key: "showT" },
    { id: "showComp", key: "showComp" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(!!v); } }
  ], state, render);

  document.getElementById("modeFwd").addEventListener("click", function () { switchMode("fwd"); });
  document.getElementById("modeInv").addEventListener("click", function () { switchMode("inv"); });

  document.getElementById("reset").addEventListener("click", function () {
    state.mode = "fwd";
    state.theta = 30;
    state.Bx = 10; state.By = 5;
    state.vx = 3; state.vy = 7; state.vz = 0;
    state.showT = true; state.showComp = true; state.auto = false;
    document.getElementById("modeFwd").classList.add("is-active");
    document.getElementById("modeInv").classList.remove("is-active");
    document.getElementById("showT").checked = true;
    document.getElementById("showComp").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    render();
  });

  /* 教材自检 */
  (function selfTest() {
    // 自检1：例2.5（θ=30°、ᴬP_BORG=(4,3,0)）代入式(2-45) 必须得到式(2-47)
    var T25 = FK.M4.fromRT(FK.M4.rotation(FK.M4.rotZ(30 * FK.DEG)), [4, 3, 0]);
    var inv25 = FK.M4.inverse(T25);
    var expect47 = [
      0.866, 0.500, 0.000, -4.964,
      -0.500, 0.866, 0.000, -0.598,
      0.000, 0.000, 1.000, 0.0,
      0, 0, 0, 1
    ];
    for (var i = 0; i < 16; i += 1) {
      if (Math.abs(inv25[i] - expect47[i]) > 1.5e-3) {
        throw new Error("式(2-47) 逆变换自检失败，下标 " + i + "：" + inv25[i] + " vs " + expect47[i]);
      }
    }
    // 自检2：把例2.2 的 ᴬP 代回 ᴮP = ᴬ_BT⁻¹·ᴬP 必须得到 (3,7,0)
    var T22 = FK.M4.fromRT(FK.M4.rotation(FK.M4.rotZ(30 * FK.DEG)), [10, 5, 0]);
    var PA22 = FK.M4.apply(T22, [3, 7, 0]);
    if (!FK.Vec.eq(FK.Vec.round(PA22, 3), [9.098, 12.562, 0], 1e-3)) {
      throw new Error("例2.2 正向自检失败：" + JSON.stringify(PA22));
    }
    var back = FK.M4.apply(FK.M4.inverse(T22), PA22);
    if (!FK.Vec.eq(FK.Vec.round(back, 6), [3, 7, 0], 1e-6)) {
      throw new Error("例2.5 逆向自检失败：ᴮP = " + JSON.stringify(back));
    }
    // 自检3：式(2-45) 的构造式与 FK.M4.inverse 必须一致（并覆盖例2.5 的平移解）
    var R = FK.M4.rotation(FK.M4.rotZ(30 * FK.DEG));
    var Rt = [R[0], R[3], R[6], R[1], R[4], R[7], R[2], R[5], R[8]];
    var p = [4, 3, 0];
    var minus = [
      -(Rt[0] * p[0] + Rt[1] * p[1] + Rt[2] * p[2]),
      -(Rt[3] * p[0] + Rt[4] * p[1] + Rt[5] * p[2]),
      -(Rt[6] * p[0] + Rt[7] * p[1] + Rt[8] * p[2])
    ];
    if (Math.abs(minus[0] + 4.964) > 1.5e-3 || Math.abs(minus[1] + 0.598) > 1.5e-3) {
      throw new Error("式(2-44) ᴮP_AORG 自检失败：" + JSON.stringify(minus));
    }
    if (!FK.Vec.eq(FK.Vec.round([inv25[3], inv25[7], inv25[11]], 6), FK.Vec.round(minus, 6), 1e-9)) {
      throw new Error("式(2-45) 与 FK.M4.inverse 不一致");
    }
  }());

  scene.setAuto(false);
  render();
}());
"""

FIGURE = {
    "id": "figure-2-13",
    "title": "图2-13 相对于坐标系{A}的坐标系{B}（例2.5 逆变换）· 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}

