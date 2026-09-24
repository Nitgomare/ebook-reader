"""图2-8 经平移和旋转的坐标系{B}（克雷格《机器人学导论（第3版）》例2.2）。

教材依据：
- 例2.2 原文：“图2-8表示了一个坐标系 {B}，它绕坐标系 {A} 的 Ẑ 轴旋转了 30 度，沿 X̂_A 平移
  10 个单位，再沿 Ŷ_A 平移 5 个单位。已知 ᴮP = [3, 7, 0]ᵀ，求 ᴬP。”
- 式(2-21) 齐次变换矩阵 ᴬ_BT（右上角 3×1 为平移列、最后一行为 [0 0 0 1]）；
  式(2-23)：ᴬP = ᴬ_BT·ᴮP = [9.098, 12.562, 0]ᵀ。
- 脚本自检：默认参数（θ=30°、平移 (10,5,0)、ᴮP=(3,7,0)）必须给出式(2-23) 的结果；
  并把 ᴬ_BT 的 4×4 各元素与式(2-21) 逐项比对。
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

/* 齐次变换矩阵显示：4×4 完整矩阵 */
.matrix {
  position: absolute;
  right: 16px;
  bottom: 178px;
  padding: 9px 12px 10px;
  border: 1px solid rgba(30, 64, 175, 0.12);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 10px 26px rgba(30, 64, 175, 0.10);
  font: 13px/1.5 ui-monospace, SFMono-Regular, Consolas, monospace;
  color: #334155;
}
.matrix .cap { font-size: 12px; color: #174ea6; font-weight: 700; margin-bottom: 3px; }
.matrix .row { white-space: pre; }
.matrix .b { color: #94a3b8; }
.matrix .r { color: #b3261e; }
.matrix .t { color: #5b21b6; font-weight: 700; }
.matrix .h { color: #12944f; }
.matrix.is-hidden { display: none; }

@media (max-width: 720px) {
  .panel h1 { font-size: 14px; }
  .control-grid { gap: 5px 8px; }
  .control-grid .control label, .control-grid .control-head output { font-size: 10.5px; }
  .options-grid { gap: 4px 8px; }
  .options-grid label { font-size: 10.5px; }
  .panel .legend { font-size: 10.5px; gap: 3px 8px; }
  .readout { font-size: 12px; line-height: 1.45; padding: 6px 8px; }
  .readout .small { font-size: 10.5px; }
  .matrix {
    right: 8px; top: 96px; bottom: auto; left: 8px;
    font-size: 10.5px; line-height: 1.35; padding: 6px 8px;
    max-width: calc(100% - 16px);
    overflow: hidden;
  }
  .matrix .cap { font-size: 10.5px; margin-bottom: 2px; }
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
     aria-label="经旋转和平移后的坐标系B与齐次变换矩阵的交互示意图">
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
    <marker id="mP" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.6" markerHeight="6.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
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

<section class="panel" aria-label="图2-8 控制面板">
  <div class="panel-head">
    <div>
      <h1>图2-8 经平移和旋转的坐标系{B}</h1>
      <p class="subtitle">例2.2：{B} 绕 Ẑ 轴转 θ，再沿 X̂_A、Ŷ_A 平移 ᴬP_BORG；ᴮP 随 {B} 一起被搬运。式(2-21) 的齐次变换矩阵把“旋转在前、平移在后”写成一个 4×4 算子。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
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
      <div class="control-head"><label for="px">ᴮP x</label><output id="pxValue">3.0</output></div>
      <input id="px" type="range" min="-10" max="10" step="0.5" value="3">
    </div>
    <div class="control">
      <div class="control-head"><label for="py">ᴮP y</label><output id="pyValue">7.0</output></div>
      <input id="py" type="range" min="-10" max="10" step="0.5" value="7">
    </div>
    <div class="control">
      <div class="control-head"><label for="pz">ᴮP z</label><output id="pzValue">0.0</output></div>
      <input id="pz" type="range" min="-6" max="6" step="0.5" value="0">
    </div>
  </div>

  <div class="options-grid">
    <label><input id="showT" type="checkbox" checked>显示齐次矩阵</label>
    <label><input id="showComp" type="checkbox" checked>分量虚线</label>
    <label><input id="auto" type="checkbox">自动旋转</label>
  </div>

  <div class="legend">
    <span><i style="background:#64748b"></i>坐标系{A}</span>
    <span><i style="background:#d93025"></i>坐标系{B}</span>
    <span><i style="background:#7c3aed"></i>平移 ᴬP_BORG</span>
    <span><i class="dot" style="background:#c26a10"></i>ᴬP = ᴬ_BT·ᴮP</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>

<div class="matrix" id="matrix">
  <div class="cap">ᴬ_BT（式2-21，4×4 齐次变换矩阵）</div>
  <div id="matrixRows"></div>
  <div class="small" style="font-size:11.5px;color:#65748b">左 3×3：旋转 ᴬ_BR（红）　·　右上 3×1：平移 ᴬP_BORG（紫）　·　末行 [0 0 0 1]（绿）</div>
</div>

<div class="readout">
  <div class="row"><strong>ᴮP</strong> = [ <span id="q1">3.000</span>, <span id="q2">7.000</span>, <span id="q3">0.000</span> ]ᵀ <span class="small">（在{B}中）</span></div>
  <div class="row"><strong>ᴬ_BR·ᴮP</strong> = [ <span id="r1">-0.902</span>, <span id="r2">7.562</span>, <span id="r3">0.000</span> ]ᵀ <span class="small">（先旋转）</span></div>
  <div class="row"><strong>+ ᴬP_BORG</strong> = [ <span id="t1">10.000</span>, <span id="t2">5.000</span>, <span id="t3">0.000</span> ]ᵀ <span class="small">（后平移）</span></div>
  <div class="row"><strong>ᴬP</strong> = [ <span id="ax">9.098</span>, <span id="ay">12.562</span>, <span id="az">0.000</span> ]ᵀ <span class="small">（例2.2 式2-23）</span></div>
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

  /* 取景矩形（viewBox 1000x620）。桌面 1200x700：viewBox x 0..1000 → 屏幕 34..1537（两侧各余 ~34px），
     y 0..620 → 屏幕 7..691；面板占左侧 304px（viewBox x<~180），读数占右下（viewBox x>650, y>440）。 */
  var FIT = { cx: 505, cy: 200, w: 560, h: 330 };
  var scene = new FK.Scene({ svg: viewport, origin: { x: FIT.cx, y: FIT.cy }, scale: 40, yaw: -0.62, pitch: 0.42 });
  var state = { theta: 30, Bx: 10, By: 5, Px: 3, Py: 7, Pz: 0, showT: true, showComp: true, auto: false };

  var COLORS = {
    A: "#64748b", Bx: "#d93025", By: "#2563eb", Bz: "#12944f",
    comp: "#a9b6c9", trans: "#7c3aed", final: "#c26a10"
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
    { x1: 650, y1: 440, x2: 1400, y2: 800 }
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
    if (!chosen) {
      chosen = { x1: p.x, y1: p.y - h + 3, x2: p.x + w, y2: p.y + 3 };
    }
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

  function drawArc(radius, start, end) {
    if (Math.abs(end - start) < 1e-4) return;
    var steps = 44, points = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = start + (end - start) * (i / steps);
      points.push([radius * Math.cos(t), radius * Math.sin(t), 0]);
    }
    scene.polyline(points, { stroke: "#7c3aed", class: "fk-arc" }, angleLayer);
    var mid = start + (end - start) * 0.5;
    place(scene.project([(radius + 0.6) * Math.cos(mid), (radius + 0.6) * Math.sin(mid), 0]),
      "\u03b8", 16, "#7c3aed", [[-12, 22], [8, 6], [-12, -6]]);
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
    var PB = [state.Px, state.Py, state.Pz];
    var rot = FK.M4.apply(Rab, PB);            // 只旋转（“旋转在前”）
    var PA = FK.Vec.add(rot, PBORG);           // 再加平移（“平移在后”）
    var T = FK.M4.fromRT(FK.M4.rotation(Rab), PBORG);

    var ak = 2.6;
    fitView([
      [0, 0, 0], PA, PBORG, rot, PB,
      [ak, 0, 0], [-ak, 0, 0], [0, ak, 0], [0, -ak, 0], [0, 0, ak], [0, 0, -ak]
    ]);
    scene.grid(3, 1, null, gridLayer);

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

    // 平移矢量 ᴬP_BORG（O → O′）
    var a0 = scene.project([0, 0, 0]), a1 = scene.project(PBORG);
    scene.el("line", {
      x1: a0.x, y1: a0.y, x2: a1.x, y2: a1.y, stroke: COLORS.trans,
      "stroke-width": 3.4, "marker-end": "url(#mT)"
    }, vectorLayer);
    scene.el("circle", { cx: a1.x, cy: a1.y, r: 4.4, fill: COLORS.trans }, vectorLayer);
    place(a1, "\u1d2cP_BORG", 16, "#5b21b6", [[-88, 30, 200], [14, 30], [-88, -12], [14, -14]]);

    // 分量虚线：以 ᴬP 为终点
    if (state.showComp) {
      drawComponent([0, 0, 0], [PA[0], 0, 0]);
      drawComponent([PA[0], 0, 0], [PA[0], PA[1], 0]);
      drawComponent([PA[0], PA[1], 0], PA);
      drawComponent(PA, [PA[0], PA[1], 0]);
    }

    // ᴬP = ᴬ_BT·ᴮP
    var b0 = scene.project([0, 0, 0]), b1 = scene.project(PA);
    scene.el("line", {
      x1: b0.x, y1: b0.y, x2: b1.x, y2: b1.y, stroke: COLORS.final,
      "stroke-width": 4.2, "marker-end": "url(#mP)"
    }, vectorLayer);
    scene.el("circle", { cx: b1.x, cy: b1.y, r: 7, fill: COLORS.final, class: "fk-point" }, vectorLayer);
    place(b1, "\u1d2cP", 20, "#8a4a08", [[16, -18, 560], [16, 18, 560], [-44, -20]]);

    // ᴮP（在 {B} 中），由 O′ + ᴬ_BR·ᴮP 得到
    var c1 = scene.project(PA);
    var c0 = scene.project(PBORG);
    scene.el("line", {
      x1: c0.x, y1: c0.y, x2: c1.x, y2: c1.y, stroke: COLORS.Bx,
      "stroke-width": 2.4, "stroke-dasharray": "9 5", opacity: 0.85, "marker-end": "url(#mBx)"
    }, vectorLayer);
    place(c1, "\u1d2eP", 16, "#a02a20", [[-42, -10], [-42, 22], [12, -12]]);

    drawArc(1.15, 0, theta);

    // 矩阵（按行拼字符串渲染，保证显示值与计算值一致）
    var rows = "";
    for (var r = 0; r < 4; r += 1) {
      var cls = r < 3 ? "r" : "h";
      rows += '<div class="row"><span class="b">[</span> ' +
        '<span class="' + cls + '">' + FK.format(T[r * 4], 3) + '</span>  ' +
        '<span class="' + cls + '">' + FK.format(T[r * 4 + 1], 3) + '</span>  ' +
        '<span class="' + cls + '">' + FK.format(T[r * 4 + 2], 3) + '</span>   ' +
        '<span class="' + (r < 3 ? "t" : "h") + '">' + FK.format(T[r * 4 + 3], 3) + '</span> ' +
        '<span class="b">]</span></div>';
    }
    document.getElementById("matrixRows").innerHTML = rows;
    document.getElementById("q1").textContent = FK.format(PB[0], 3);
    document.getElementById("q2").textContent = FK.format(PB[1], 3);
    document.getElementById("q3").textContent = FK.format(PB[2], 3);
    document.getElementById("r1").textContent = FK.format(rot[0], 3);
    document.getElementById("r2").textContent = FK.format(rot[1], 3);
    document.getElementById("r3").textContent = FK.format(rot[2], 3);
    document.getElementById("t1").textContent = FK.format(PBORG[0], 3);
    document.getElementById("t2").textContent = FK.format(PBORG[1], 3);
    document.getElementById("t3").textContent = FK.format(PBORG[2], 3);
    document.getElementById("ax").textContent = FK.format(PA[0], 3);
    document.getElementById("ay").textContent = FK.format(PA[1], 3);
    document.getElementById("az").textContent = FK.format(PA[2], 3);
    document.getElementById("matrix").classList.toggle("is-hidden", !state.showT);
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "theta", key: "theta", value: 30, format: function (v) { return FK.deg(v, 1); } },
    { id: "bx", key: "Bx", value: 10, format: function (v) { return FK.format(v, 1); } },
    { id: "by", key: "By", value: 5, format: function (v) { return FK.format(v, 1); } },
    { id: "px", key: "Px", value: 3, format: function (v) { return FK.format(v, 1); } },
    { id: "py", key: "Py", value: 7, format: function (v) { return FK.format(v, 1); } },
    { id: "pz", key: "Pz", value: 0, format: function (v) { return FK.format(v, 1); } }
  ], state, render);

  FK.bindToggles([
    { id: "showT", key: "showT" },
    { id: "showComp", key: "showComp" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(!!v); } }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 30;
    state.Bx = 10; state.By = 5;
    state.Px = 3; state.Py = 7; state.Pz = 0;
    state.showT = true; state.showComp = true; state.auto = false;
    document.getElementById("showT").checked = true;
    document.getElementById("showComp").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    render();
  });

  /* 教材自检：例2.2 —— ᴬ_BT 应等于式(2-21)，ᴬP 应等于式(2-23) = [9.098, 12.562, 0] */
  (function selfTest() {
    var T = FK.M4.fromRT(FK.M4.rotation(FK.M4.rotZ(30 * FK.DEG)), [10, 5, 0]);
    if (!FK.Vec.eq(FK.Vec.round([T[0], T[1], T[2]], 3), [0.866, -0.500, 0.000], 1e-3) ||
        !FK.Vec.eq(FK.Vec.round([T[4], T[5], T[6]], 3), [0.500, 0.866, 0.000], 1e-3) ||
        T[3] !== 10 || T[7] !== 5 || T[11] !== 0 ||
        T[12] !== 0 || T[13] !== 0 || T[14] !== 0 || T[15] !== 1) {
      throw new Error("式(2-21) 齐次变换矩阵自检失败：" + JSON.stringify(T));
    }
    var PA = FK.M4.apply(T, [3, 7, 0]);
    if (!FK.Vec.eq(FK.Vec.round(PA, 3), [9.098, 12.562, 0], 1e-3)) {
      throw new Error("例2.2 数值自检失败：ᴬP = " + JSON.stringify(PA));
    }
    // 旋转在前、平移在后：先旋转不应该受 ᴬP_BORG 影响
    var rot = FK.M4.apply(FK.M4.rotZ(30 * FK.DEG), [3, 7, 0]);
    if (!FK.Vec.eq(FK.Vec.round(FK.Vec.add(rot, [10, 5, 0]), 9), FK.Vec.round(PA, 9), 1e-9)) {
      throw new Error("“先旋转再加平移”与齐次变换结果不一致");
    }
  }());

  scene.setAuto(false);
  render();
}());
"""

FIGURE = {
    "id": "figure-2-8",
    "title": "图2-8 经平移和旋转的坐标系{B}（例2.2）· 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}

