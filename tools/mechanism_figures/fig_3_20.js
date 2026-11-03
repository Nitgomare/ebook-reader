/* 图3-20 牛头刨床的摆动导杆机构：曲柄整周回转，滑块推着导杆绕 C 摆动 */
(function () {
  "use strict";

  var DIMS = { a: 2.0, r: 0.9, guideLen: 2.75, zA: 2.35, zC: 0.85 };
  var A = [0, DIMS.zA];
  var C = [0, DIMS.zC];
  var state = { theta: 30, r: 0.9, auto: true, showTrace: true, showLabels: true };
  var LAYERS = ["baseLayer", "traceLayer", "frameLayer", "linkLayer", "pinLayer", "labelLayer"];
  var scene, M, P, S, layer = {};

  function pose(theta) {
    var th = (theta === undefined ? state.theta : theta) * Math.PI / 180;
    var B = [A[0] + Math.cos(th) * state.r, A[1] + Math.sin(th) * state.r];
    var dx = B[0] - C[0], dz = B[1] - C[1];
    var len = Math.hypot(dx, dz);
    return { A: A, C: C, B: B, u: [dx / len, dz / len], len: len };
  }

  function clearAll() { LAYERS.forEach(function (id) { if (layer[id]) layer[id].replaceChildren(); }); }
  function setText(id, t) { var n = document.getElementById(id); if (n && n.textContent !== t) n.textContent = t; }

  function ring(cx, cz, radius, y, color) {
    var d = "";
    for (var i = 0; i <= 96; i++) {
      var a = (i / 96) * Math.PI * 2;
      var p = scene.project([cx + Math.cos(a) * radius, y, cz + Math.sin(a) * radius]);
      d += (i ? "L" : "M") + p.x.toFixed(2) + " " + p.y.toFixed(2);
    }
    MP.el("path", { d: d + "Z", fill: "none", stroke: color, "stroke-width": 1.4, "stroke-dasharray": "7 6", opacity: 0.7 }, layer.traceLayer);
  }

  function topArc() {
    var half = Math.asin(Math.min(1, state.r / DIMS.a));
    var d = "";
    for (var i = 0; i <= 60; i++) {
      var a = -half + (2 * half) * i / 60;
      var p = scene.project([Math.sin(a) * DIMS.guideLen, 0.34, C[1] + Math.cos(a) * DIMS.guideLen]);
      d += (i ? "L" : "M") + p.x.toFixed(2) + " " + p.y.toFixed(2);
    }
    MP.el("path", { d: d, fill: "none", stroke: "#4f9aa2", "stroke-width": 1.4, "stroke-dasharray": "7 6", opacity: 0.7 }, layer.traceLayer);
  }

  function render() {
    clearAll();
    if (window.FigureLayout) window.FigureLayout.fit(scene, state, 6.2);
    var s = pose();

    M.bench(-1.05, 1.25, -0.85, 0.85, 0.26, layer.baseLayer, { label: "FIG 3-20", labelX: 0.10 });

    if (state.showTrace) { ring(A[0], A[1], state.r, -0.28, P.brass.dark); topArc(); }

    // 机架：A 立柱立在 C 后方，只让销轴穿到机构平面
    S.pedestal(A[0], A[1], 0.58, { layer: layer.frameLayer });
    S.pedestal(C[0], C[1], 0.44, { layer: layer.frameLayer });
    M.box([0, 0.58, 0.42], [0.16, 0.16, Math.max(0.2, C[1] - 0.42)], "graphite", layer.frameLayer, { bevel: 0.02 });

    var end = [s.C[0] + s.u[0] * DIMS.guideLen, s.C[1] + s.u[1] * DIMS.guideLen];
    var back = [s.C[0] - s.u[0] * 0.32, s.C[1] - s.u[1] * 0.32];
    S.linkBar(back, end, 0.135, 0.16, 0.18, "teal", layer.linkLayer);

    // 滑块：夹在导杆上的一块滑枕，B 处的销轴穿过它
    var sl = 0.22;
    S.linkBar([s.B[0] - s.u[0] * sl, s.B[1] - s.u[1] * sl], [s.B[0] + s.u[0] * sl, s.B[1] + s.u[1] * sl], 0.170, 0.02, 0.40, "slate", layer.linkLayer);
    S.linkBar([A[0], A[1]], [s.B[0], s.B[1]], 0.100, -0.26, 0.14, "brass", layer.linkLayer);

    S.cylY(A[0], A[1], 0.100, -0.38, 0.50, "ink", layer.pinLayer, { seg: 20 });
    S.cylY(C[0], C[1], 0.095, 0.26, 0.70, "steel", layer.pinLayer, { seg: 20 });
    S.cylY(s.B[0], s.B[1], 0.105, -0.34, 0.20, "steel", layer.pinLayer, { seg: 18 });

    if (state.showLabels) {
      var put = function (p, name, dx, dy) {
        var q = scene.project([p[0], -0.42, p[1]]);
        var t = MP.el("text", {
          x: q.x + (dx || 0), y: q.y + (dy || 0), "text-anchor": "middle", "font-size": 15,
          "font-weight": 700, fill: "#25313f", "paint-order": "stroke", stroke: "#ffffff", "stroke-width": 4
        }, layer.labelLayer);
        t.textContent = name;
      };
      put(A, "A", -24, 14); put(s.B, "B", 22, -10); put(C, "C", -22, 18);
    }

    var phi = Math.atan2(s.u[0], s.u[1]) * 180 / Math.PI;
    var swing = 2 * Math.asin(Math.min(1, state.r / DIMS.a)) * 180 / Math.PI;
    var k = (180 + swing) / (180 - swing);
    setText("thetaValue", state.theta.toFixed(0) + "°");
    setText("rValue", state.r.toFixed(2));
    setText("thetaOut", state.theta.toFixed(0) + "°");
    setText("phiOut", phi.toFixed(1) + "°");
    setText("swingOut", swing.toFixed(1) + "°");
    setText("kOut", k.toFixed(2));
  }

  var raf = 0, last = 0;
  function tick(now) {
    raf = 0;
    var dt = last ? Math.min((now - last) / 1000, 1 / 20) : 1 / 60;
    last = now;
    if (!state.auto) { last = 0; return; }
    state.theta = (state.theta + 54 * dt) % 360;
    render();
    raf = requestAnimationFrame(tick);
  }
  function runLoop() { if (!raf && state.auto) raf = requestAnimationFrame(tick); }

  function bind() {
    [["theta", "theta", "thetaValue", function (v) { return v.toFixed(0) + "°"; }],
     ["r", "r", "rValue", function (v) { return v.toFixed(2); }]].forEach(function (row) {
      var input = document.getElementById(row[0]);
      if (!input) return;
      input.addEventListener("input", function () {
        state[row[1]] = parseFloat(input.value);
        setText(row[2], row[3](state[row[1]]));
        render();
      });
    });
    ["auto", "showTrace", "showLabels"].forEach(function (id) {
      var box = document.getElementById(id);
      if (!box) return;
      box.addEventListener("change", function () {
        state[id] = box.checked;
        if (id === "auto" && box.checked) { last = 0; runLoop(); } else render();
      });
    });
    var reset = document.getElementById("reset");
    if (reset) reset.addEventListener("click", function () {
      state.theta = 30; state.r = 0.9;
      [["theta", 30], ["r", 0.9]].forEach(function (pair) {
        var input = document.getElementById(pair[0]); if (input) input.value = pair[1];
      });
      setText("thetaValue", "30°"); setText("rValue", "0.90");
      scene.reset(); render();
    });
  }

  function boot() {
    LAYERS.forEach(function (id) { layer[id] = document.getElementById(id); });
    scene = new FK.Scene({
      svg: document.getElementById("viewport"), origin: { x: 470, y: 330 }, scale: 96,
      yaw: -0.40, pitch: 0.30, minScale: 34, maxScale: 190
    });
    M = window.MK.make(scene, {});
    P = M.pal;
    S = window.MP.make(scene, M);
    bind(); render();
    if (window.FigureLayout) window.FigureLayout.attach(scene, state, render, 6.2);
    runLoop();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
