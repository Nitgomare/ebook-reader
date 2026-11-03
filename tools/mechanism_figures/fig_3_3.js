/* 图3-3 铰链四杆机构（曲柄摇杆）：一台小试验台
 * 底板 + 两个轴承立柱 + 三根链杆 + 四根销轴。曲柄 AB 整周回转，摇杆 CD 往复摆动。 */
(function () {
  "use strict";

  var DIMS = { r: 1.0, l: 3.2, d: 2.4, ad: 3.0, z0: 1.36 };
  var A = [0, DIMS.z0];
  var D = [DIMS.ad, DIMS.z0];

  var state = { theta: 48, r: 1.0, l: 3.2, auto: true, showTrace: true, showLabels: true };
  var LAYERS = ["baseLayer", "traceLayer", "frameLayer", "linkLayer", "pinLayer", "labelLayer"];
  var scene, M, P, S;
  var layer = {};

  function grabLayers() {
    LAYERS.forEach(function (id) { layer[id] = document.getElementById(id); });
  }

  function clearAll() {
    LAYERS.forEach(function (id) { if (layer[id]) layer[id].replaceChildren(); });
  }

  function solve() {
    var r = state.r, l = state.l, d = DIMS.d;
    var th = state.theta * Math.PI / 180;
    var B = [A[0] + Math.cos(th) * r, A[1] + Math.sin(th) * r];
    var dx = D[0] - B[0], dz = D[1] - B[1];
    var dist = Math.hypot(dx, dz);
    if (dist > l + d - 1e-6 || dist < Math.abs(l - d) + 1e-6) return { A: A, D: D, B: B, C: null };
    var a = (l * l - d * d + dist * dist) / (2 * dist);
    var h = Math.sqrt(Math.max(0, l * l - a * a));
    var mx = B[0] + (dx / dist) * a, mz = B[1] + (dz / dist) * a;
    var C1 = [mx - (dz / dist) * h, mz + (dx / dist) * h];
    var C2 = [mx + (dz / dist) * h, mz - (dx / dist) * h];
    return { A: A, D: D, B: B, C: C1[1] > C2[1] ? C1 : C2 };
  }

  function traceCircle(cx, cz, radius, y, color) {
    var pts = [];
    for (var i = 0; i <= 96; i++) {
      var a = (i / 96) * Math.PI * 2;
      var p = scene.project([cx + Math.cos(a) * radius, y, cz + Math.sin(a) * radius]);
      pts.push((i ? "L" : "M") + p.x.toFixed(2) + " " + p.y.toFixed(2));
    }
    MP.el("path", {
      d: pts.join("") + "Z", fill: "none", stroke: color,
      "stroke-width": 1.4, "stroke-dasharray": "7 6", opacity: 0.72
    }, layer.traceLayer);
  }

  function traceRockerArc() {
    var pts = [];
    var save = state.theta;
    for (var t = 0; t <= 720; t++) {
      state.theta = (t / 720) * 360;
      var s = solve();
      if (s.C) {
        var p = scene.project([s.C[0], 0.30, s.C[1]]);
        pts.push((pts.length ? "L" : "M") + p.x.toFixed(2) + " " + p.y.toFixed(2));
      }
    }
    state.theta = save;
    if (pts.length < 6) return;
    MP.el("path", { d: pts.join(""), fill: "none", stroke: P.teal.dark, "stroke-width": 1.4, "stroke-dasharray": "7 6", opacity: 0.68 }, layer.traceLayer);
  }

  function setText(id, text) {
    var node = document.getElementById(id);
    if (node && node.textContent !== text) node.textContent = text;
  }

  function render() {
    clearAll();
    if (window.FigureLayout) window.FigureLayout.fit(scene, state, 5.4);

    var s = solve();

    // 1. 底座
    M.bench(-1.35, 4.55, -1.20, 1.05, 0.24, layer.baseLayer, { label: "FIG 3-3", labelX: 0.30 });

    // 2. 轨迹虚线（在实体之下）
    if (state.showTrace) {
      traceCircle(A[0], A[1], state.r, 0.62, P.brass.dark);
      traceRockerArc();
      traceCircle(D[0], D[1], DIMS.d, 0.30, P.teal.dark);
    }

    // 3. 机架：两个轴承立柱 + 横梁
    S.pedestal(A[0], A[1], 0.60, { layer: layer.frameLayer });
    S.pedestal(D[0], D[1], 0.60, { layer: layer.frameLayer });
    // 两根立柱之间的一道细筋，比横梁更像试验台的拉杆
    M.box([(A[0] + D[0]) / 2, 0.60, 0.62], [D[0] - A[0] - 0.30, 0.10, 0.10], "graphite", layer.frameLayer, { bevel: 0.02 });
    // 立柱根部加两块三角形肋，读起来是铸件而不是竖着的豆腐块
    [A[0], D[0]].forEach(function (x) {
      M.box([x, 0.60, 0.32], [0.16, 0.30, 0.30], "graphite", layer.frameLayer, { bevel: 0.03 });
    });

    if (!s.C) {
      var warn = MP.el("text", { x: 470, y: 300, "text-anchor": "middle", "font-size": 15, fill: "#8a5a1e" }, layer.labelLayer);
      warn.textContent = "此尺寸下无法装配";
      setText("psiOut", "—"); setText("gammaOut", "—");
      return;
    }

    // 4. 摇杆 CD（后层）
    S.linkBar([s.C[0], s.C[1]], [D[0], D[1]], 0.125, 0.16, 0.17, "teal", layer.linkLayer);
    // 5. 连杆 BC（中层，白钢）
    S.linkBar([s.B[0], s.B[1]], [s.C[0], s.C[1]], 0.135, -0.02, 0.18, "steel", layer.linkLayer);
    // 6. 曲柄 AB（最外，黄铜）
    S.linkBar([A[0], A[1]], [s.B[0], s.B[1]], 0.115, -0.20, 0.16, "brass", layer.linkLayer);

    // 7. 销轴：贯穿立柱与所有杆件
    S.cylY(A[0], A[1], 0.115, -0.34, 0.80, "ink", layer.pinLayer, { seg: 20 });
    S.cylY(D[0], D[1], 0.100, -0.02, 0.80, "steel", layer.pinLayer, { seg: 20 });
    S.cylY(s.B[0], s.B[1], 0.092, -0.32, 0.06, "steel", layer.pinLayer, { seg: 18 });
    S.cylY(s.C[0], s.C[1], 0.088, -0.14, 0.28, "steel", layer.pinLayer, { seg: 18 });

    // 8. 标注
    if (state.showLabels) {
      var put = function (p, name, dx, dy) {
        var q = scene.project([p[0], -0.38, p[1]]);
        var t = MP.el("text", {
          x: q.x + (dx || 0), y: q.y + (dy || 0), "text-anchor": "middle", "font-size": 15,
          "font-weight": 700, fill: "#25313f", "paint-order": "stroke", stroke: "#ffffff", "stroke-width": 4
        }, layer.labelLayer);
        t.textContent = name;
      };
      put(A, "A", -26, 20); put(s.B, "B", 22, -12); put(s.C, "C", 24, -10); put(D, "D", 26, 18);
    }

    // 9. 读数
    var th = state.theta;
    var psi = Math.atan2(s.C[1] - D[1], s.C[0] - D[0]) * 180 / Math.PI;
    var v1 = [s.B[0] - s.C[0], s.B[1] - s.C[1]];
    var v2 = [D[0] - s.C[0], D[1] - s.C[1]];
    var cosg = (v1[0] * v2[0] + v1[1] * v2[1]) / (Math.hypot(v1[0], v1[1]) * Math.hypot(v2[0], v2[1]));
    var gamma = Math.acos(Math.max(-1, Math.min(1, cosg))) * 180 / Math.PI;
    if (gamma > 90) gamma = 180 - gamma;
    setText("thetaValue", th.toFixed(0) + "°");
    setText("rValue", state.r.toFixed(2));
    setText("lValue", state.l.toFixed(2));
    setText("psiOut", psi.toFixed(1) + "°");
    setText("gammaOut", gamma.toFixed(1) + "°");
    setText("thetaOut", th.toFixed(0) + "°");
  }

  var raf = 0, last = 0;
  function tick(now) {
    raf = 0;
    var dt = last ? Math.min((now - last) / 1000, 1 / 20) : 1 / 60;
    last = now;
    if (!state.auto) { last = 0; return; }
    state.theta = (state.theta + 66 * dt) % 360;
    render();
    raf = requestAnimationFrame(tick);
  }
  function runLoop() {
    if (!raf && state.auto) raf = requestAnimationFrame(tick);
  }

  function bind() {
    [["theta", "theta", "thetaValue", function (v) { return v.toFixed(0) + "°"; }],
     ["r", "r", "rValue", function (v) { return v.toFixed(2); }],
     ["l", "l", "lValue", function (v) { return v.toFixed(2); }]].forEach(function (row) {
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
      state.theta = 48; state.r = DIMS.r; state.l = DIMS.l;
      [["theta", 48], ["r", DIMS.r], ["l", DIMS.l]].forEach(function (pair) {
        var input = document.getElementById(pair[0]);
        if (input) input.value = pair[1];
      });
      setText("thetaValue", "48°"); setText("rValue", DIMS.r.toFixed(2)); setText("lValue", DIMS.l.toFixed(2));
      scene.reset(); render();
    });
  }

  function boot() {
    grabLayers();
    scene = new FK.Scene({
      svg: document.getElementById("viewport"), origin: { x: 470, y: 330 }, scale: 96,
      yaw: -0.40, pitch: 0.30, minScale: 34, maxScale: 190
    });
    M = window.MK.make(scene, {});
    P = M.pal;
    S = window.MP.make(scene, M);
    bind();
    render();
    if (window.FigureLayout) window.FigureLayout.attach(scene, state, render, 5.4);
    runLoop();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
