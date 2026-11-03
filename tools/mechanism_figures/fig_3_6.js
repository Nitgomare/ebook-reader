/* 图3-6 冲床的双曲柄机构：两台曲柄箱对置，连杆跨在中间 */
(function () {
  "use strict";

  var DIMS = { ad: 0.9, ab: 1.4, cd: 1.3, z0: 1.55 };
  var A = [0, DIMS.z0];
  var D = [DIMS.ad, DIMS.z0];
  var state = { theta: 20, bc: 1.40, auto: true, showTrace: true, showLabels: true };
  var LAYERS = ["baseLayer", "traceLayer", "frameLayer", "linkLayer", "pinLayer", "labelLayer"];
  var scene, M, P, S, layer = {}, prevC = null;

  function solve(theta, track) {
    var deg = (theta === undefined ? state.theta : theta);
    var th = deg * Math.PI / 180;
    var B = [A[0] + Math.cos(th) * DIMS.ab, A[1] + Math.sin(th) * DIMS.ab];
    var db = Math.hypot(B[0] - D[0], B[1] - D[1]);
    var bc = state.bc, cd = DIMS.cd;
    if (db > bc + cd || db < Math.abs(bc - cd)) return { A: A, D: D, B: B, C: null };
    var a = (bc * bc - cd * cd + db * db) / (2 * db);
    var h = Math.sqrt(Math.max(0, bc * bc - a * a));
    var ux = (B[0] - D[0]) / db, uz = (B[1] - D[1]) / db;
    var mx = D[0] + ux * a, mz = D[1] + uz * a;
    var C1 = [mx - uz * h, mz + ux * h], C2 = [mx + uz * h, mz - ux * h];
    // 圆交点有两个装配分支；固定取“上方”会在分支切换处让杆件瞬间翻面，
    // 所以按上一帧的位置就近选择，保证连杆连续转动。
    var pick;
    if (prevC) {
      var d1 = Math.hypot(C1[0] - prevC[0], C1[1] - prevC[1]);
      var d2 = Math.hypot(C2[0] - prevC[0], C2[1] - prevC[1]);
      pick = d1 <= d2 ? C1 : C2;
    } else {
      pick = C1[1] > C2[1] ? C1 : C2;
    }
    if (track) prevC = pick;
    return { A: A, D: D, B: B, C: pick };
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
    if (window.FigureLayout) window.FigureLayout.fit(scene, state, 5.2);
    var s = solve(undefined, true);

    M.bench(-1.75, 2.65, -1.25, 1.10, 0.26, layer.baseLayer, { label: "FIG 3-6", labelX: 0.55 });

    if (state.showTrace) {
      ring(A[0], A[1], DIMS.ab, -0.34, P.brass.dark);
      ring(D[0], D[1], DIMS.cd, 0.34, "#7c6aa8");
    }

    S.pedestal(A[0], A[1], 0.62, { layer: layer.frameLayer });
    S.pedestal(D[0], D[1], 0.62, { layer: layer.frameLayer });
    M.box([(A[0] + D[0]) / 2, 0.62, 0.52], [Math.max(0.2, D[0] - A[0] - 0.25), 0.10, 0.10], "graphite", layer.frameLayer, { bevel: 0.02 });

    if (!s.C) {
      var warn = MP.el("text", { x: 470, y: 300, "text-anchor": "middle", "font-size": 15, fill: "#8a5a1e" }, layer.labelLayer);
      warn.textContent = "此尺寸下无法装配";
      setText("phiOut", "—"); setText("ratioOut", "—");
      return;
    }

    // 从动曲柄 CD 在里层，连杆居中，主动曲柄 AB 在最外层
    S.linkBar([s.C[0], s.C[1]], [D[0], D[1]], 0.115, 0.24, 0.16, "graphite", layer.linkLayer);
    S.linkBar([s.B[0], s.B[1]], [s.C[0], s.C[1]], 0.125, 0.02, 0.17, "steel", layer.linkLayer);
    S.linkBar([A[0], A[1]], [s.B[0], s.B[1]], 0.115, -0.22, 0.16, "brass", layer.linkLayer);

    S.cylY(A[0], A[1], 0.100, -0.32, 0.82, "ink", layer.pinLayer, { seg: 20 });
    S.cylY(D[0], D[1], 0.095, 0.16, 0.82, "steel", layer.pinLayer, { seg: 20 });
    S.cylY(s.B[0], s.B[1], 0.082, -0.30, 0.10, "steel", layer.pinLayer, { seg: 18 });
    S.cylY(s.C[0], s.C[1], 0.082, -0.06, 0.34, "steel", layer.pinLayer, { seg: 18 });

    if (state.showLabels) {
      var put = function (p, name, dx, dy) {
        var q = scene.project([p[0], -0.40, p[1]]);
        var t = MP.el("text", {
          x: q.x + (dx || 0), y: q.y + (dy || 0), "text-anchor": "middle", "font-size": 15,
          "font-weight": 700, fill: "#25313f", "paint-order": "stroke", stroke: "#ffffff", "stroke-width": 4
        }, layer.labelLayer);
        t.textContent = name;
      };
      put(A, "A", -22, 18); put(s.B, "B", 22, -10); put(s.C, "C", 10, -16); put(D, "D", 26, 16);
    }

    var phi = Math.atan2(s.C[1] - D[1], s.C[0] - D[0]) * 180 / Math.PI;
    var save = state.theta;
    state.theta = save + 0.5; var s2 = solve(save + 0.5, false); state.theta = save;
    var ratio = "—";
    if (s2.C) {
      var p1 = Math.atan2(s.C[1] - D[1], s.C[0] - D[0]);
      var p2 = Math.atan2(s2.C[1] - D[1], s2.C[0] - D[0]);
      var dphi = p2 - p1;
      while (dphi > Math.PI) dphi -= Math.PI * 2;
      while (dphi < -Math.PI) dphi += Math.PI * 2;
      ratio = (dphi * 180 / Math.PI / 0.5).toFixed(2);
    }
    setText("thetaValue", state.theta.toFixed(0) + "°");
    setText("thetaOut", state.theta.toFixed(0) + "°");
    setText("phiOut", phi.toFixed(1) + "°");
    setText("ratioOut", ratio);
  }

  var timer = 0, last = 0;
  function step() {
    var now = Date.now();
    var dt = last ? Math.min((now - last) / 1000, 1 / 20) : 1 / 60;
    last = now;
    if (!state.auto) { last = 0; return; }
    state.theta = (state.theta + 52 * dt) % 360;
    render();
  }
  // 用定时器而不是 requestAnimationFrame：页面被 iframe 或标签页隐藏时 rAF 会暂停，
  // 观感就是“曲柄不走了”；定时器不受此影响。
  function runLoop() {
    if (timer) return;
    last = 0;
    timer = setInterval(function () {
      if (!state.auto) { clearInterval(timer); timer = 0; return; }
      step();
    }, 33);
  }

  function bind() {
    [["theta", "theta", "thetaValue", function (v) { return v.toFixed(0) + "°"; }],
     ["bc", "bc", "bcValue", function (v) { return v.toFixed(2); }]].forEach(function (row) {
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
      state.theta = 20; state.bc = 1.40; prevC = null;
      var t = document.getElementById("theta"); if (t) t.value = 20;
      var b = document.getElementById("bc"); if (b) b.value = 1.40;
      setText("thetaValue", "20°"); setText("bcValue", "1.40");
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
