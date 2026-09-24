"""图2-10 / 图2-11 旋转算子与复合变换算子（克雷格《机器人学导论（第3版）》例2.3、例2.4）。

教材依据：
- 图2-10 / 例2.3：矢量 ᴬP₁ = [0, 2, 0]ᵀ 绕 Ẑ 轴旋转 30°，得 ᴬP₂ = R_Z(30°)·ᴬP₁。
  式(2-30) 给出旋转算子 R_z(θ) 的矩阵形式；注意这是**矢量绕轴主动旋转**，
  与图2-6“坐标系旋转后同一矢量在新系中的表达”不是同一件事。
- 图2-11 / 例2.4：同一矢量先绕 Ẑ 轴旋转 30°，再沿 X̂_A 平移 10、沿 Ŷ_A 平移 5，
  得 ᴬP₂ = T·ᴬP₁，其中 T = D_X(10)·D_Y(5)·R_Z(30°)（式(2-34)）。
  数值与例2.2 相同（[9.098, 12.562, 0]ᵀ），但含义是**算子作用在矢量上**，
  而不是图2-8 的“坐标系变换后求同一物理点的新坐标”。

规格文件内自检：
1. 例2.3：R_Z(30°)·[0,2,0]ᵀ 必须等于 [−1, √3, 0]ᵀ；
2. 例2.4：T·[0,2,0]ᵀ 必须等于式(2-34) 的结果 [9.098, 12.562, 0]ᵀ；
3. 旋转算子的 4×4 形式最后一行必须是 [0,0,0,1]，且 R 部分正交。
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
.options-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 5px 10px; margin-top: 10px; }
.options-grid label { display: inline-flex; align-items: center; gap: 5px; color: #4a5a72; font-size: 11.5px; cursor: pointer; white-space: nowrap; }
.options-grid input { accent-color: var(--blue); flex: none; }
.matrix {
  position: absolute;
  right: 16px;
  bottom: 16px;
  padding: 9px 12px 10px;
  border: 1px solid rgba(30, 64, 175, 0.12);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 10px 26px rgba(30, 64, 175, 0.10);
  font: 12.5px/1.5 ui-monospace, SFMono-Regular, Consolas, monospace;
  color: #334155;
}
.matrix .cap { font-size: 12px; color: #174ea6; font-weight: 700; margin-bottom: 3px; }
.matrix .row { white-space: pre; }
.matrix .t { color: #5b21b6; font-weight: 700; }
.matrix .b { color: #94a3b8; }
.matrix.is-hidden { display: none; }

@media (max-width: 720px) {
  .panel h1 { font-size: 14px; }
  .control-grid { gap: 5px 8px; }
  .control-grid .control label, .control-grid .control-head output { font-size: 10.5px; }
  .options-grid label { font-size: 10.5px; }
  .readout { font-size: 12px; line-height: 1.45; padding: 6px 8px; }
  .matrix {
    right: 8px; left: 8px; bottom: 8px;
    font-size: 10.5px; line-height: 1.35; padding: 6px 8px;
  }
  .matrix .cap { font-size: 10.5px; margin-bottom: 2px; }
}
"""

BODY = """
<svg class="viewport" id="viewport" role="img"
     aria-label="旋转算子与复合变换算子作用在矢量上的交互示意图">
  <defs>
    <marker id="mAxis" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"></path>
    </marker>
    <marker id="mP1" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="mP2" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#174ea6"></path>
    </marker>
    <marker id="mMid" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="mQ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="axes"></g>
  <g id="guides"></g>
  <g id="vectors"></g>
  <g id="labels"></g>
</svg>

<section class="panel" aria-label="图2-10 / 图2-11 控制面板">
  <div class="panel-head">
    <div>
      <h1 id="panelTitle">图2-10 旋转算子</h1>
      <p class="subtitle" id="panelSub">同一个矢量 ᴬP₁ 被算子作用后成为 ᴬP₂。这里是“矢量被旋转”，不是“换一个坐标系看同一个点”。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="tabs" role="tablist">
    <button type="button" id="tabRot" class="is-active" data-mode="rotate" role="tab">图2-10 旋转算子</button>
    <button type="button" id="tabTrans" data-mode="transform" role="tab">图2-11 复合算子</button>
  </div>

  <div class="control">
    <div class="control-head"><label for="theta">旋转角 θ（绕 Ẑ_A）</label><output id="thetaValue">30.0°</output></div>
    <input id="theta" type="range" min="-180" max="180" step="1" value="30">
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="px">ᴬP₁ 的 x</label><output id="pxValue">0.00</output></div>
      <input id="px" type="range" min="-4" max="4" step="0.1" value="0">
    </div>
    <div class="control">
      <div class="control-head"><label for="py">ᴬP₁ 的 y</label><output id="pyValue">2.00</output></div>
      <input id="py" type="range" min="-4" max="4" step="0.1" value="2">
    </div>
    <div class="control">
      <div class="control-head"><label for="pz">ᴬP₁ 的 z</label><output id="pzValue">0.00</output></div>
      <input id="pz" type="range" min="-4" max="4" step="0.1" value="0">
    </div>
  </div>

  <div id="shiftGrid" class="control-grid">
    <div class="control">
      <div class="control-head"><label for="dx">平移 q<sub>x</sub></label><output id="dxValue">10.0</output></div>
      <input id="dx" type="range" min="-16" max="16" step="0.5" value="10">
    </div>
    <div class="control">
      <div class="control-head"><label for="dy">平移 q<sub>y</sub></label><output id="dyValue">5.0</output></div>
      <input id="dy" type="range" min="-16" max="16" step="0.5" value="5">
    </div>
    <div class="control">
      <div class="control-head"><label for="dz">平移 q<sub>z</sub></label><output id="dzValue">0.0</output></div>
      <input id="dz" type="range" min="-8" max="8" step="0.5" value="0">
    </div>
  </div>

  <div class="options-grid">
    <label><input id="showMid" type="checkbox" checked>显示中间结果</label>
    <label><input id="showGuide" type="checkbox" checked>显示分量虚线</label>
    <label><input id="showMatrix" type="checkbox" checked>显示 4×4 算子</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <div class="legend">
    <span><i style="background:#475569"></i>固定坐标系{A}</span>
    <span><i style="background:#c26a10"></i>矢量 ᴬP₁</span>
    <span><i style="background:#12944f"></i>R_Z(θ)·ᴬP₁</span>
    <span><i style="background:#174ea6"></i>结果 ᴬP₂</span>
    <span><i style="background:#7c3aed"></i>平移量 ᴬQ</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row" id="rowP1"><strong>ᴬP₁</strong> = [ 0.000, 2.000, 0.000 ]ᵀ</div>
  <div class="row" id="rowMid" class="small"><strong>R_Z(θ)·ᴬP₁</strong> = [ −1.000, 1.732, 0.000 ]ᵀ</div>
  <div class="row"><strong>ᴬP₂</strong> = [ <span id="rx">-1.000</span>, <span id="ry">1.732</span>, <span id="rz">0.000</span> ]ᵀ</div>
</div>

<div class="matrix" id="matrix"></div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var axesLayer = document.getElementById("axes");
  var guideLayer = document.getElementById("guides");
  var vectorLayer = document.getElementById("vectors");
  var labelLayer = document.getElementById("labels");
  var matrixBox = document.getElementById("matrix");

  var state = {
    mode: "rotate", theta: 30, px: 0, py: 2, pz: 0,
    dx: 10, dy: 5, dz: 0,
    showMid: true, showGuide: true, showMatrix: true, auto: false
  };
  var layout = { axisLength: 3.2, unit: 1 };

  var C = {
    axis: "#475569", p1: "#c26a10", mid: "#12944f", p2: "#174ea6", q: "#7c3aed", guide: "#94a3b8"
  };

  var scene = new FK.AdaptiveScene({
    svg: viewport,
    scale: 46,
    narrowScale: 30,
    yaw: -0.62,
    pitch: 0.42,
    wide: { x: 0.5, y: 0.6 },
    narrow: { x: 0.55, y: 0.42 },
    tall: { x: 0.5, y: 0.4 },
    onLayout: function (sc, box) {
      // 例2.4 的结果最远到 ≈ (12.6, 12.6)：轴长与投影缩放都要覆盖它
      var span = state.mode === "transform" ? 15.5 : 6.4;
      var available = Math.min(
        box.width * (box.narrow ? 0.52 : 0.6),
        box.height * (box.narrow ? 0.6 : 0.78)
      );
      sc.state.scale = Math.max(14, Math.min(52, available / span));
      layout.axisLength = state.mode === "transform" ? 4.2 : 3.2;
      layout.unit = sc.state.scale;
    }
  });

  function axes() {
    var len = layout.axisLength;
    var dirs = [[len, 0, 0], [0, len, 0], [0, 0, len]];
    var names = ["X\u0302\u2090", "Y\u0302\u2090", "Z\u0302\u2090"];
    var colors = ["#d93025", "#2563eb", "#12944f"];
    for (var i = 0; i < 3; i += 1) {
      scene.arrow([0, 0, 0], dirs[i], null, "mAxis", axesLayer);
      var p = scene.project(dirs[i]);
      var node = scene.el("text", { x: p.x + 9, y: p.y - 7, fill: colors[i], "font-size": 15, "font-style": "italic", class: "fk-axis-label" }, axesLayer);
      node.textContent = names[i];
    }
    var o = scene.project([0, 0, 0]);
    var label = scene.el("text", { x: o.x - 24, y: o.y + 20, class: "fk-origin-label" }, axesLayer);
    label.textContent = "O";
  }

  function vec(a, b, color, marker, width, parent) {
    var A = scene.project(a), B = scene.project(b);
    var el = scene.el("line", {
      x1: A.x, y1: A.y, x2: B.x, y2: B.y,
      stroke: color, "stroke-width": width || 4.4, class: "fk-vec-line",
      "marker-end": "url(#" + marker + ")"
    }, parent);
    return el;
  }

  function tag(v, str, color, dx, dy, size, parent) {
    var p = scene.project(v);
    var node = scene.el("text", {
      x: p.x + dx, y: p.y + dy, fill: color,
      "font-size": size || 16, class: "fk-vec-label"
    }, parent || labelLayer);
    node.textContent = str;
  }

  function dashed(a, b, color) {
    var A = scene.project(a), B = scene.project(b);
    scene.el("line", {
      x1: A.x, y1: A.y, x2: B.x, y2: B.y,
      stroke: color || C.guide, class: "fk-projection"
    }, guideLayer);
  }

  function arcZ(radius, from, to, color, text) {
    var steps = 40;
    var pts = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = from + (to - from) * (i / steps);
      pts.push([radius * Math.cos(t), radius * Math.sin(t), 0]);
    }
    scene.polyline(pts, { stroke: color, class: "fk-arc" }, guideLayer);
    var mid = from + (to - from) * 0.5;
    var p = scene.project([(radius + 0.28) * Math.cos(mid), (radius + 0.28) * Math.sin(mid), 0]);
    var node = scene.el("text", { x: p.x - 10, y: p.y + 5, fill: color, "font-size": 16, class: "fk-axis-label" }, guideLayer);
    node.textContent = text;
  }

  function matrixRows(title, rows, highlightLast) {
    var html = '<div class="cap">' + title + "</div>";
    rows.forEach(function (row, index) {
      var cls = highlightLast && index === 3 ? ' class="b"' : "";
      html += '<div class="row"' + cls + ">[ " + row.map(function (x) { return FK.format(x, 3).padStart(8); }).join(" ") + " ]</div>";
    });
    return html;
  }

  function render() {
    gridLayer.replaceChildren();
    axesLayer.replaceChildren();
    guideLayer.replaceChildren();
    vectorLayer.replaceChildren();
    labelLayer.replaceChildren();

    var P1 = [state.px, state.py, state.pz];
    var theta = state.theta * FK.DEG;
    var R = FK.M4.rotZ(theta);
    var mid = FK.M4.apply(R, P1);
    var Q = state.mode === "transform" ? [state.dx, state.dy, state.dz] : [0, 0, 0];
    var P2 = FK.Vec.add(mid, Q);

    scene.grid(Math.max(2, Math.round(layout.axisLength)), 1);
    axes();

    if (state.showGuide) {
      dashed([0, 0, 0], [P1[0], P1[1], 0], C.guide);
      dashed([P1[0], P1[1], 0], P1, C.guide);
      dashed([0, 0, 0], [mid[0], mid[1], 0], C.guide);
      dashed([mid[0], mid[1], 0], mid, C.guide);
      if (state.mode === "transform") {
        dashed(mid, [mid[0], mid[1], mid[2] + Q[2]], C.q);
        dashed([mid[0], mid[1], mid[2] + Q[2]], P2, C.q);
        dashed(mid, P2, C.q);
      }
    }

    vec([0, 0, 0], P1, C.p1, "mP1");
    tag(P1, "\u1d2cP\u2081", C.p1, 12, -12, 17);

    if (state.showMid && state.mode === "transform") {
      vec([0, 0, 0], mid, C.mid, "mMid", 3.6);
      tag(mid, "R_Z(\u03b8)\u00b7\u1d2cP\u2081", C.mid, 12, -12, 15);
    }

    if (state.mode === "transform") {
      vec(mid, P2, C.q, "mQ", 3.6);
      var mp = FK.Vec.scale(FK.Vec.add(mid, P2), 0.5);
      tag(mp, "\u1d2cQ", C.q, 10, -8, 15);
    }

    vec([0, 0, 0], P2, C.p2, "mP2", 5);
    tag(P2, "\u1d2cP\u2082", C.p2, 12, -12, 18);

    if (state.mode === "rotate") {
      arcZ(Math.min(1.4, FK.Vec.len(P1) * 0.55), state.px === 0 && state.py === 0 ? 0 : Math.atan2(P1[1], P1[0]), state.px === 0 && state.py === 0 ? theta : Math.atan2(P1[1], P1[0]) + theta, C.mid, "\u03b8");
    } else {
      arcZ(Math.min(2.4, layout.axisLength * 0.7), 0, theta, C.mid, "\u03b8");
    }

    // 读数
    document.getElementById("rowP1").innerHTML = "<strong>\u1d2cP\u2081</strong> = [ " +
      FK.format(P1[0], 3) + ", " + FK.format(P1[1], 3) + ", " + FK.format(P1[2], 3) + " ]\u1d40";
    var rowMid = document.getElementById("rowMid");
    if (state.mode === "transform") {
      rowMid.style.display = "";
      rowMid.innerHTML = "<strong>R_Z(\u03b8)\u00b7\u1d2cP\u2081 + \u1d2cQ</strong> = [ " +
        FK.format(mid[0], 3) + ", " + FK.format(mid[1], 3) + ", " + FK.format(mid[2], 3) + " ]\u1d40 + [ " +
        FK.format(Q[0], 2) + ", " + FK.format(Q[1], 2) + ", " + FK.format(Q[2], 2) + " ]\u1d40";
    } else {
      rowMid.style.display = "none";
    }
    document.getElementById("rx").textContent = FK.format(P2[0], 3);
    document.getElementById("ry").textContent = FK.format(P2[1], 3);
    document.getElementById("rz").textContent = FK.format(P2[2], 3);

    // 4×4 算子
    if (state.showMatrix) {
      matrixBox.classList.remove("is-hidden");
      if (state.mode === "rotate") {
        matrixBox.innerHTML = matrixRows("R_Z(\u03b8) =", [
          [Math.cos(theta), -Math.sin(theta), 0, 0],
          [Math.sin(theta), Math.cos(theta), 0, 0],
          [0, 0, 1, 0],
          [0, 0, 0, 1]
        ], true);
      } else {
        var T = FK.M4.chain(FK.M4.translate(Q), FK.M4.rotZ(theta));
        matrixBox.innerHTML = matrixRows("T = D_X(q_x)\u00b7D_Y(q_y)\u00b7R_Z(\u03b8)（式2-34）=", [
          [T[0], T[1], T[2], T[3]],
          [T[4], T[5], T[6], T[7]],
          [T[8], T[9], T[10], T[11]],
          [T[12], T[13], T[14], T[15]]
        ], true);
      }
    } else {
      matrixBox.classList.add("is-hidden");
    }
  }

  scene.setRenderer(render);

  // 先把渲染器接上，再绑定滑块（bindRanges 初始化时就会触发一次渲染）
  var ranges = FK.bindRanges([
    { id: "theta", key: "theta", value: 30, format: function (v) { return FK.deg(v, 1); } },
    { id: "px", key: "px", value: 0, format: function (v) { return FK.format(v, 2); } },
    { id: "py", key: "py", value: 2, format: function (v) { return FK.format(v, 2); } },
    { id: "pz", key: "pz", value: 0, format: function (v) { return FK.format(v, 2); } },
    { id: "dx", key: "dx", value: 10, format: function (v) { return FK.format(v, 1); } },
    { id: "dy", key: "dy", value: 5, format: function (v) { return FK.format(v, 1); } },
    { id: "dz", key: "dz", value: 0, format: function (v) { return FK.format(v, 1); } }
  ], state, function () { scene.fit(); render(); });

  FK.bindToggles([
    { id: "showMid", key: "showMid" },
    { id: "showGuide", key: "showGuide" },
    { id: "showMatrix", key: "showMatrix" },
    { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
  ], state, render);

  function setMode(mode) {
    state.mode = mode;
    document.getElementById("tabRot").classList.toggle("is-active", mode === "rotate");
    document.getElementById("tabTrans").classList.toggle("is-active", mode === "transform");
    document.getElementById("shiftGrid").style.display = mode === "transform" ? "" : "none";
    document.getElementById("panelTitle").textContent = mode === "rotate" ? "图2-10 旋转算子" : "图2-11 复合变换算子";
    document.getElementById("panelSub").textContent = mode === "rotate"
      ? "例2.3：矢量 ᴬP₁ 被旋转算子 R_Z(θ) 作用后成为 ᴬP₂。这是矢量本身转动，不是换坐标系看同一个点。"
      : "例2.4：同一矢量先被 R_Z(θ) 旋转，再被平移算子 ᴬQ 平移，合成算子 T = D_X·D_Y·R_Z。";
    scene.fit();
    render();
  }

  document.getElementById("tabRot").addEventListener("click", function () { setMode("rotate"); });
  document.getElementById("tabTrans").addEventListener("click", function () { setMode("transform"); });

  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 30; state.px = 0; state.py = 2; state.pz = 0;
    state.dx = 10; state.dy = 5; state.dz = 0;
    state.showMid = true; state.showGuide = true; state.showMatrix = true; state.auto = false;
    ["showMid", "showGuide", "showMatrix"].forEach(function (id) { document.getElementById(id).checked = true; });
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    scene.fit();
    render();
  });

  // 教材数值自检
  (function selfTest() {
    var R = FK.M4.rotZ(30 * FK.DEG);
    var mid = FK.M4.apply(R, [0, 2, 0]);
    if (!FK.Vec.eq(FK.Vec.round(mid, 6), [-1, Math.sqrt(3), 0], 1e-6)) {
      throw new Error("例2.3 自检失败：" + JSON.stringify(mid));
    }
    var T = FK.M4.chain(FK.M4.translate([10, 5, 0]), R);
    var p2 = FK.M4.apply(T, [0, 2, 0]);
    if (!FK.Vec.eq(FK.Vec.round(p2, 3), [9.098, 12.562, 0], 1e-3)) {
      throw new Error("例2.4 自检失败：" + JSON.stringify(p2));
    }
    var rot = FK.M4.rotation(R);
    for (var i = 0; i < 3; i += 1) {
      for (var j = 0; j < 3; j += 1) {
        var dot = 0;
        for (var k = 0; k < 3; k += 1) dot += rot[i * 3 + k] * rot[j * 3 + k];
        var want = i === j ? 1 : 0;
        if (Math.abs(dot - want) > 1e-9) throw new Error("旋转算子非正交");
      }
    }
  }());

  document.getElementById("shiftGrid").style.display = "none";
  scene.fit();
  render();
  setMode("rotate");
}());
"""

FIGURE = {
    "id": "figure-2-10-11",
    "title": "图2-10 / 图2-11 旋转算子与复合变换算子 · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
