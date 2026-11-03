/* 图3-15 曲柄滑块机构（偏置）：曲柄整周回转，滑块沿中央导轨往复 */
(function () {
  "use strict";

  var DIMS = { r: 1.2, l: 3.6, z0: 1.45, railTop: 0.30 };
  var A = [0, DIMS.z0];
  var state = { theta: 40, r: 1.2, e: 0.60, auto: true, showTrace: true, showLabels: true };
  var LAYERS = ["baseLayer", "traceLayer", "frameLayer", "linkLayer", "pinLayer", "labelLayer"];
  var scene, M, P, S, layer = {};

  function pose(theta) {
    var th = (theta === undefined ? state.theta : theta) * Math.PI / 180;
    var B = [A[0] + Math.cos(th) * state.r, A[1] + Math.sin(th) * state.r];
    var zRail = A[1] - state.e;
    var dz = B[1] - zRail;
    var under = DIMS.l * DIMS.l - dz * dz;
    if (under <= 0) return { A: A, B: B, C: null, zRail: zRail };
    return { A: A, B: B, C: [B[0] + Math.sqrt(under), zRail], zRail: zRail };
  }

  function stroke() {
    var lo = 1e9, hi = -1e9;
    for (var t = 0; t < 360; t += 1) {
      var s = pose(t);
      if (!s.C) continue;
      lo = Math.min(lo, s.C[0]); hi = Math.max(hi, s.C[0]);
    }
    return hi - lo;
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

  function render() {
    clearAll();
    if (window.FigureLayout) window.FigureLayout.fit(scene, state, 6.6);
    var s = pose();
    var zRail = s.zRail;

    M.bench(-1.55, 4.85, -1.10, 1.00, 0.26, layer.baseLayer, { label: "FIG 3-15", labelX: 0.55 });

    // 床身 + 两端支座 + 一条中央导轨，滑块骑在轨顶
    var bedZ = zRail - 0.34;
    M.box([(A[0] + 4.6) / 2, 0, bedZ + 0.02], [5.0, 0.66, 0.34], "graphite", layer.frameLayer, { bevel: 0.04 });
    M.box([-0.9, 0, bedZ / 2], [0.26, 0.66, Math.max(0.2, bedZ)], "graphite", layer.frameLayer, { bevel: 0.03 });
    M.box([4.5, 0, bedZ / 2], [0.26, 0.66, Math.max(0.2, bedZ)], "graphite", layer.frameLayer, { bevel: 0.03 });
    M.box([1.85, 0, zRail - 0.16], [5.0, 0.26, 0.26], "slate", layer.frameLayer, { bevel: 0.03 });

    if (state.showTrace) ring(A[0], A[1], state.r, -0.30, P.brass.dark);

    S.pedestal(A[0], A[1], 0.34, { layer: layer.frameLayer });
    if (!s.C) { setText("sOut", "—"); setText("hOut", "—"); setText("gammaOut", "—"); return; }

    // 滑块
    M.box([s.C[0], 0, zRail + 0.06], [0.46, 0.62, 0.34], "slate", layer.linkLayer, { bevel: 0.04 });
    S.linkBar([s.B[0], s.B[1]], [s.C[0], s.C[1]], 0.115, -0.30, 0.16, "steel", layer.linkLayer);
    S.linkBar([A[0], A[1]], [s.B[0], s.B[1]], 0.115, -0.10, 0.16, "brass", layer.linkLayer);

    S.cylY(A[0], A[1], 0.105, -0.36, 0.50, "ink", layer.pinLayer, { seg: 20 });
    S.cylY(s.B[0], s.B[1], 0.085, -0.40, -0.02, "steel", layer.pinLayer, { seg: 18 });
    S.cylY(s.C[0], zRail + 0.06, 0.090, -0.40, 0.36, "steel", layer.pinLayer, { seg: 18 });

    if (state.showLabels) {
      var put = function (p, name, dx, dy) {
        var q = scene.project([p[0], -0.44, p[1]]);
        var t = MP.el("text", {
          x: q.x + (dx || 0), y: q.y + (dy || 0), "text-anchor": "middle", "font-size": 15,
          "font-weight": 700, fill: "#25313f", "paint-order": "stroke", stroke: "#ffffff", "stroke-width": 4
        }, layer.labelLayer);
        t.textContent = name;
      };
      put(A, "A", -24, 22); put(s.B, "B", 20, -12); put([s.C[0], zRail], "C", 6, 26);
    }

    var gamma = Math.atan2(Math.abs(s.B[1] - s.C[1]), Math.abs(s.C[0] - s.B[0])) * 180 / Math.PI;
    setText("thetaValue", state.theta.toFixed(0) + "°");
    setText("rValue", state.r.toFixed(2));
    setText("eValue", state.e.toFixed(2));
    setText("thetaOut", state.theta.toFixed(0) + "°");
    setText("sOut", s.C[0].toFixed(2));
    setText("hOut", stroke().toFixed(2));
    setText("gammaOut", gamma.toFixed(1) + "°");
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
     ["r", "r", "rValue", function (v) { return v.toFixed(2); }],
     ["e", "e", "eValue", function (v) { return v.toFixed(2); }]].forEach(function (row) {
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
      state.theta = 40; state.r = 1.2; state.e = 0.60;
      [["theta", 40], ["r", 1.2], ["e", 0.6]].forEach(function (pair) {
        var input = document.getElementById(pair[0]); if (input) input.value = pair[1];
      });
      setText("thetaValue", "40°"); setText("rValue", "1.20"); setText("eValue", "0.60");
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
    if (window.FigureLayout) window.FigureLayout.attach(scene, state, render, 6.6);
    runLoop();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
