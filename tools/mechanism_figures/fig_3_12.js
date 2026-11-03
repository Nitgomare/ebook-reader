/* 图3-12 造型机翻箱机构：双摇杆，两根连架杆都只在有限角度内摆动 */
(function () {
  "use strict";

  var DIMS = { ad: 2.60, ab: 1.70, cd: 1.70, z0: 1.50 };
  var A = [0, DIMS.z0];
  var D = [DIMS.ad, DIMS.z0];
  var state = { theta: 62, cd: 1.70, auto: true, showTrace: true, showLabels: true };
  var LAYERS = ["baseLayer", "traceLayer", "frameLayer", "linkLayer", "pinLayer", "labelLayer"];
  var scene, M, P, S, layer = {}, dir = 1;

  function solve(theta) {
    var th = (theta === undefined ? state.theta : theta) * Math.PI / 180;
    var B = [A[0] + Math.cos(th) * DIMS.ab, A[1] + Math.sin(th) * DIMS.ab];
    var bc = 1.20, cd = state.cd;
    var db = Math.hypot(B[0] - D[0], B[1] - D[1]);
    if (db > bc + cd || db < Math.abs(bc - cd)) return { A: A, D: D, B: B, C: null };
    var a = (bc * bc - cd * cd + db * db) / (2 * db);
    var h = Math.sqrt(Math.max(0, bc * bc - a * a));
    var ux = (B[0] - D[0]) / db, uz = (B[1] - D[1]) / db;
    var mx = D[0] + ux * a, mz = D[1] + uz * a;
    var C1 = [mx - uz * h, mz + ux * h], C2 = [mx + uz * h, mz - ux * h];
    return { A: A, D: D, B: B, C: C1[1] > C2[1] ? C1 : C2 };
  }

  // 装配条件把 θ 限制在一个连续区间里：扫描出当前 θ 所属的那一段
  function limits() {
    var lo = state.theta, hi = state.theta, t;
    for (t = state.theta; t > state.theta - 360; t -= 0.5) {
      if (!solve(t).C) break;
      lo = t;
    }
    for (t = state.theta; t < state.theta + 360; t += 0.5) {
      if (!solve(t).C) break;
      hi = t;
    }
    return [Math.ceil(lo), Math.floor(hi)];
  }

  function clearAll() { LAYERS.forEach(function (id) { if (layer[id]) layer[id].replaceChildren(); }); }
  function setText(id, t) { var n = document.getElementById(id); if (n && n.textContent !== t) n.textContent = t; }

  function arc(cx, cz, radius, a0, a1, y, color) {
    var d = "";
    for (var i = 0; i <= 72; i++) {
      var a = (a0 + (a1 - a0) * i / 72) * Math.PI / 180;
      var p = scene.project([cx + Math.cos(a) * radius, y, cz + Math.sin(a) * radius]);
      d += (i ? "L" : "M") + p.x.toFixed(2) + " " + p.y.toFixed(2);
    }
    MP.el("path", { d: d, fill: "none", stroke: color, "stroke-width": 1.4, "stroke-dasharray": "7 6", opacity: 0.7 }, layer.traceLayer);
  }

  function render() {
    clearAll();
    if (window.FigureLayout) window.FigureLayout.fit(scene, state, 6.4);
    var lim = limits();
    if (state.theta < lim[0] || state.theta > lim[1]) state.theta = Math.min(Math.max(state.theta, lim[0]), lim[1]);
    var slider = document.getElementById("theta");
    if (slider && (parseFloat(slider.min) !== lim[0] || parseFloat(slider.max) !== lim[1])) {
      slider.min = lim[0]; slider.max = lim[1];
    }
    var s = solve();

    M.bench(-1.55, 4.25, -1.20, 1.05, 0.26, layer.baseLayer, { label: "FIG 3-12", labelX: 0.40 });

    if (state.showTrace) {
      arc(A[0], A[1], DIMS.ab, lim[0], lim[1], -0.34, P.brass.dark);
      arc(D[0], D[1], state.cd, lim[0], lim[1], 0.34, "#4f9aa2");
    }

    S.pedestal(A[0], A[1], 0.60, { layer: layer.frameLayer });
    S.pedestal(D[0], D[1], 0.60, { layer: layer.frameLayer });
    M.box([(A[0] + D[0]) / 2, 0.60, 0.60], [D[0] - A[0] - 0.30, 0.10, 0.10], "graphite", layer.frameLayer, { bevel: 0.02 });

    if (!s.C) { setText("psiOut", "—"); setText("couplerOut", "—"); return; }

    S.linkBar([s.C[0], s.C[1]], [D[0], D[1]], 0.115, 0.20, 0.16, "teal", layer.linkLayer);
    S.linkBar([s.B[0], s.B[1]], [s.C[0], s.C[1]], 0.125, -0.02, 0.17, "steel", layer.linkLayer);
    S.linkBar([A[0], A[1]], [s.B[0], s.B[1]], 0.115, -0.24, 0.16, "brass", layer.linkLayer);

    S.cylY(A[0], A[1], 0.105, -0.34, 0.80, "ink", layer.pinLayer, { seg: 20 });
    S.cylY(D[0], D[1], 0.098, 0.10, 0.80, "steel", layer.pinLayer, { seg: 20 });
    S.cylY(s.B[0], s.B[1], 0.085, -0.34, 0.06, "steel", layer.pinLayer, { seg: 18 });
    S.cylY(s.C[0], s.C[1], 0.085, -0.14, 0.28, "steel", layer.pinLayer, { seg: 18 });

    if (state.showLabels) {
      var put = function (p, name, dx, dy) {
        var q = scene.project([p[0], -0.42, p[1]]);
        var t = MP.el("text", {
          x: q.x + (dx || 0), y: q.y + (dy || 0), "text-anchor": "middle", "font-size": 15,
          "font-weight": 700, fill: "#25313f", "paint-order": "stroke", stroke: "#ffffff", "stroke-width": 4
        }, layer.labelLayer);
        t.textContent = name;
      };
      put(A, "A", -24, 20); put(s.B, "B", 18, -14); put(s.C, "C", 16, -16); put(D, "D", 24, 20);
    }

    var psi = Math.atan2(s.C[1] - D[1], s.C[0] - D[0]) * 180 / Math.PI;
    var beta = Math.atan2(s.C[1] - s.B[1], s.C[0] - s.B[0]) * 180 / Math.PI;
    setText("thetaValue", state.theta.toFixed(0) + "°");
    setText("thetaOut", state.theta.toFixed(0) + "°");
    setText("psiOut", psi.toFixed(1) + "°");
    setText("couplerOut", beta.toFixed(1) + "°");
  }

  var timer = 0, last = 0;
  function step() {
    var now = Date.now();
    var dt = last ? Math.min((now - last) / 1000, 1 / 20) : 1 / 60;
    last = now;
    if (!state.auto) { last = 0; return; }
    var lim = limits();
    state.theta += dir * 26 * dt;
    if (state.theta > lim[1]) { state.theta = lim[1]; dir = -1; }
    if (state.theta < lim[0]) { state.theta = lim[0]; dir = 1; }
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
     ["cd", "cd", "cdValue", function (v) { return v.toFixed(2); }]].forEach(function (row) {
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
      state.theta = 62; state.cd = 1.70; dir = 1;
      var t = document.getElementById("theta"); if (t) t.value = 62;
      var c = document.getElementById("cd"); if (c) c.value = 1.70;
      setText("thetaValue", "62°"); setText("cdValue", "1.70");
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
    if (window.FigureLayout) window.FigureLayout.attach(scene, state, render, 6.4);
    runLoop();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
