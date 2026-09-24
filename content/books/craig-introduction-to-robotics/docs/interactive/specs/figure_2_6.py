"""图2-6 坐标系{B}绕Ẑ轴旋转30°（克雷格《机器人学导论（第3版）》例2.1）。

教材依据：
- 正文式(2-13)：ᴬP = ᴬ_B R · ᴮP，旋转矩阵的三列是{B}三轴单位矢量在{A}中的表达。
- 例2.1：{B} 与 {A} 原点重合，{B} 绕 Ẑ 轴相对 {A} 转 30°，ᴮP = [0, 2, 0]ᵀ，求 ᴬP。
  解得 ᴬP = [−1, 1.732, 0]ᵀ（脚本内做了断言自检）。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="坐标系B绕Z轴旋转θ的交互示意图">
  <defs>
    <marker id="arrowA" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"></path>
    </marker>
    <marker id="arrowAX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="arrowAY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="arrowAZ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="arrowB" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
  </defs>
  <g id="grid"></g>
  <g id="axesA"></g>
  <g id="axesB"></g>
  <g id="angle"></g>
  <g id="vectorLayer"></g>
</svg>

<section class="panel" aria-label="图2-6 控制面板">
  <div class="panel-head">
    <div>
      <h1>图2-6 {B}绕Ẑ轴旋转</h1>
      <p class="subtitle">两坐标系原点重合；{B}绕{A}的Ẑ轴转过θ，ᴮP 固定不动，观察 ᴬP = ᴬ_BR·ᴮP。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>
  <div class="control">
    <div class="control-head"><label for="theta">旋转角 θ</label><output id="thetaValue">30.0°</output></div>
    <input id="theta" type="range" min="-180" max="180" step="1" value="30">
  </div>
  <div class="options">
    <label><input id="showB" type="checkbox" checked>显示坐标系{B}</label>
    <label><input id="showP" type="checkbox" checked>显示点P与ᴬP</label>
    <label><input id="showComp" type="checkbox" checked>显示分量虚线</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>
  <div class="legend">
    <span><i style="background:#475569"></i>坐标系{A}（灰）</span>
    <span><i style="background:#d93025"></i>坐标系{B} 三轴</span>
    <span><i class="dot" style="background:#c26a10"></i>ᴬP 矢量</span>
    <span><i style="background:#94a3b8"></i>分量投影</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row"><strong>ᴮP</strong> = [ 0.000, 2.000, 0.000 ]ᵀ <span class="small">（{B}中不变）</span></div>
  <div class="row"><strong>ᴬP</strong> = [ <span id="px">-1.000</span>, <span id="py">1.732</span>, <span id="pz">0.000</span> ]ᵀ</div>
  <div class="row small">ᴬ_BR 第1列 = [ <span id="r11">0.866</span>, <span id="r21">0.500</span>, 0 ]ᵀ</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var gridLayer = document.getElementById("grid");
  var axesA = document.getElementById("axesA");
  var axesB = document.getElementById("axesB");
  var angleLayer = document.getElementById("angle");
  var vectorLayer = document.getElementById("vectorLayer");

  var scene = new FK.AdaptiveScene({
    svg: viewport,
    scale: 108,
    narrowScale: 74,
    yaw: -0.62,
    pitch: 0.42,
    onLayout: function (sc, box) {
      // 轴长随可用空间收缩，保证 3 个坐标轴始终完整落在画布内
      var available = Math.min(box.width * 0.42, box.height * 0.62);
      layout.axisLength = Math.max(1.6, Math.min(3.05, available / sc.state.scale));
    }
  });
  var layout = { axisLength: 3.05 };
  var state = { theta: 30, showB: true, showP: true, showComp: true };

  var COLORS = { A: "#475569", Bx: "#d93025", By: "#2563eb", Bz: "#12944f", vec: "#c26a10", comp: "#94a3b8" };

  function drawAxes(layer, matrix, spec, prefix) {
    var length = layout.axisLength;
    var dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    for (var i = 0; i < 3; i += 1) {
      var base = FK.M4.apply(matrix, [0, 0, 0]);
      var tip = FK.M4.apply(matrix, FK.Vec.scale(dirs[i], length));
      var a = scene.project(base);
      var b = scene.project(tip);
      scene.el("line", {
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        stroke: spec.colors[i], "stroke-width": spec.width,
        "marker-end": "url(#" + spec.markers[i] + ")"
      }, layer);
      var label = scene.el("text", {
        x: b.x + spec.dx[i], y: b.y + spec.dy[i], fill: spec.colors[i],
        "font-size": 17, "font-style": "italic", class: "fk-axis-label"
      }, layer);
      label.textContent = spec.labels[i];
    }
    var o = scene.project(FK.M4.apply(matrix, [0, 0, 0]));
    scene.el("circle", { cx: o.x, cy: o.y, r: 4.4, fill: "#334155" }, layer);
    var origin = scene.el("text", { x: o.x + spec.originDx, y: o.y + spec.originDy, class: "fk-origin-label" }, layer);
    origin.textContent = prefix === "A" ? "O" : "O'";
  }

  function drawArc(radius, start, end, color) {
    var steps = 48;
    var points = [];
    for (var i = 0; i <= steps; i += 1) {
      var t = start + (end - start) * (i / steps);
      points.push([radius * Math.cos(t), radius * Math.sin(t), 0]);
    }
    scene.polyline(points, { stroke: color, class: "fk-arc" }, angleLayer);
    var mid = start + (end - start) * 0.5;
    var p = scene.project([(radius + 0.34) * Math.cos(mid), (radius + 0.34) * Math.sin(mid), 0]);
    var text = scene.el("text", { x: p.x - 8, y: p.y + 6, fill: color, "font-size": 17, class: "fk-axis-label" }, angleLayer);
    text.textContent = "θ";
  }

  function drawComponent(from, to, color) {
    var a = scene.project(from);
    var b = scene.project(to);
    scene.el("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: color, class: "fk-projection" }, vectorLayer);
  }

  function render() {
    gridLayer.replaceChildren();
    axesA.replaceChildren();
    axesB.replaceChildren();
    angleLayer.replaceChildren();
    vectorLayer.replaceChildren();

    scene.grid(Math.max(2, Math.round(layout.axisLength)), 1);

    drawAxes(axesA, FK.M4.identity(), {
      labels: ["X\u0302\u2090", "Y\u0302\u2090", "Z\u0302\u2090"],
      colors: [COLORS.A, COLORS.A, COLORS.A],
      markers: ["arrowA", "arrowA", "arrowA"],
      dx: [9, 9, 9], dy: [-7, -7, -7], width: 3.1, originDx: -22, originDy: 20
    }, "A");

    var theta = state.theta * FK.DEG;
    var Rab = FK.M4.rotZ(theta);
    if (state.showB) {
      drawAxes(axesB, Rab, {
        labels: ["X\u0302\u1d47", "Y\u0302\u1d47", "Z\u0302\u1d47"],
        colors: [COLORS.Bx, COLORS.By, COLORS.Bz],
        markers: ["arrowAX", "arrowAY", "arrowAZ"],
        dx: [9, 9, 9], dy: [-7, 9, -7], width: 3.1, originDx: -22, originDy: 20
      }, "B");
    }

    // ᴮP 固定为 [0, 2, 0]，ᴬP = ᴬ_BR·ᴮP
    var Pb = [0, 2, 0];
    var Pa = FK.M4.apply(Rab, Pb);

    if (state.showP) {
      if (state.showComp) {
        drawComponent([0, 0, 0], [Pa[0], 0, 0], COLORS.comp);
        drawComponent([Pa[0], 0, 0], [Pa[0], Pa[1], 0], COLORS.comp);
        drawComponent([Pa[0], Pa[1], 0], Pa, COLORS.comp);
        drawComponent(Pa, [Pa[0], Pa[1], 0], COLORS.comp);
      }
      var o = [0, 0, 0];
      var a = scene.project(o);
      var b = scene.project(Pa);
      scene.el("line", {
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        stroke: COLORS.vec, class: "fk-vec-line", "marker-end": "url(#arrowB)"
      }, vectorLayer);
      scene.el("circle", { cx: b.x, cy: b.y, r: 6.5, fill: COLORS.vec, class: "fk-point" }, vectorLayer);
      var label = scene.el("text", {
        x: b.x + 13, y: b.y - 16, fill: "#8a4a08", "font-size": 19, class: "fk-point-label"
      }, vectorLayer);
      label.textContent = "\u1d2cP";
      var tag = scene.el("text", { x: b.x + 13, y: b.y + 26, fill: "#174ea6", "font-size": 15, class: "fk-point-label" }, vectorLayer);
      tag.textContent = "\u1d2eP = [0, 2, 0]\u1d40";
    }

    drawArc(1.15, 0, theta, "#7c3aed");

    document.getElementById("px").textContent = FK.format(Pa[0], 3);
    document.getElementById("py").textContent = FK.format(Pa[1], 3);
    document.getElementById("pz").textContent = FK.format(Pa[2], 3);
    var c = Math.cos(theta), s = Math.sin(theta);
    document.getElementById("r11").textContent = FK.format(c, 3);
    document.getElementById("r21").textContent = FK.format(s, 3);
    document.getElementById("thetaValue").textContent = FK.deg(state.theta, 1);
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges(
    [{ id: "theta", key: "theta", value: 30, format: function (v) { return FK.deg(v, 1); } }],
    state,
    render
  );
  FK.bindToggles(
    [
      { id: "showB", key: "showB" },
      { id: "showP", key: "showP" },
      { id: "showComp", key: "showComp" },
      { id: "auto", key: "auto", onChange: function (v) { scene.setAuto(v); } }
    ],
    state,
    render
  );

  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 30;
    state.showB = true;
    state.showP = true;
    state.showComp = true;
    state.auto = false;
    document.getElementById("showB").checked = true;
    document.getElementById("showP").checked = true;
    document.getElementById("showComp").checked = true;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    ranges.refresh();
    scene.reset();
    render();
  });

  // 教材自检：例2.1 当 θ = 30° 时 ᴬP 应为 (−1, √3, 0)
  (function selfTest() {
    var Rab = FK.M4.rotZ(30 * FK.DEG);
    var Pa = FK.M4.apply(Rab, [0, 2, 0]);
    var expected = [-1, Math.sqrt(3), 0];
    if (!FK.Vec.eq(FK.Vec.round(Pa, 6), FK.Vec.round(expected, 6), 1e-6)) {
      throw new Error("例2.1 数值自检失败：" + JSON.stringify(Pa));
    }
  }());

  render();
}());
"""

FIGURE = {
    "id": "figure-2-6",
    "title": "图2-6 坐标系{B}绕Ẑ轴旋转30° · 人机交互演示",
    "css": COMMON_CSS,
    "body": BODY,
    "script": SCRIPT,
}
