(function () {
  "use strict";

  var viewport = document.getElementById("viewport");
  var baseLayer = document.getElementById("baseLayer");
  var frameLayer = document.getElementById("frameLayer");
  var traceLayer = document.getElementById("traceLayer");
  var linkLayer = document.getElementById("linkLayer");
  var pinLayer = document.getElementById("pinLayer");
  var labelLayer = document.getElementById("labelLayer");

  var scene = new FK.Scene({
    svg: viewport,
    origin: { x: 470, y: 330 },
    scale: 92,
    yaw: -0.40,
    pitch: 0.30,
    minScale: 34,
    maxScale: 190
  });
  var M = MK.make(scene);

  // 牛头刨床的摆动导杆机构 ABC：曲柄 AB 整周回转，导杆绕 C 摆动，滑块在导杆中滑
  var DIMS = { a: 2.3, r: 1.0, guideLen: 2.9, zA: 3.05, zC: 0.78 };
  var A = [0, DIMS.zA];
  var C = [0, DIMS.zC];

  var state = { theta: 0, r: DIMS.r, auto: true, showTrace: true, showLabels: true };

  function rad2deg(v) { return v * 180 / Math.PI; }

  function pose(theta) {
    var t = theta * FK.DEG;
    var B = [A[0] + state.r * Math.cos(t), A[1] + state.r * Math.sin(t)];
    var dx = B[0] - C[0], dz = B[1] - C[1];
    var len = Math.sqrt(dx * dx + dz * dz);
    return { B: B, u: [dx / len, dz / len], len: len };
  }

  function solve() { return pose(state.theta); }

  /** 导杆摆角（相对 AC 竖直方向，顺时针为正） */
  function swing(theta) {
    var s = pose(theta);
    return rad2deg(Math.atan2(s.u[0], s.u[1]));
  }

  /** 立柱 + 悬臂：立柱在一旁，用横臂把销轴托到机构平面，避免挡住导杆的摆动范围 */
  function bracket(xCol, zCol, xPin, zPin, y0, y1) {
    var zBase = 0.20;
    M.box([xCol, y0, 0.09], [0.56, 0.60, 0.18], "graphite", frameLayer);
    M.box([xCol, y0, (zCol + zBase) / 2], [0.28, 0.30, Math.max(0.24, zCol + 0.08 - zBase)], "graphite", frameLayer);
    M.box([(xCol + xPin) / 2, y0, zCol], [Math.abs(xCol - xPin) + 0.26, 0.30, 0.26], "slate", frameLayer);
    if (Math.abs(y0 - y1) > 0.05) {
      M.box([xPin, (y0 + y1) / 2, zPin], [0.30, Math.abs(y0 - y1) + 0.14, 0.26], "slate", frameLayer);
    }
  }

  function render() {
    window.FigureLayout.fit(scene, state, 5.4);
    baseLayer.replaceChildren();
    frameLayer.replaceChildren();
    traceLayer.replaceChildren();
    linkLayer.replaceChildren();
    pinLayer.replaceChildren();
    labelLayer.replaceChildren();

    M.bench(-1.6, 2.4, -1.15, 1.15, 0.22, baseLayer, { label: "FIG 3-20", labelX: -0.6 });
    bracket(-0.72, DIMS.zA, A[0], DIMS.zA, 0.0, -0.24);
    bracket(0.02, DIMS.zC, C[0] + 0.02, DIMS.zC, 0.42, 0.18);

    var s = solve();
    var B = s.B, u = s.u;
    var tip = [C[0] + u[0] * DIMS.guideLen, C[1] + u[1] * DIMS.guideLen];
    var back = [C[0] - u[0] * 0.42, C[1] - u[1] * 0.42];

    if (state.showTrace) {
      var ring = [], i;
      for (i = 0; i <= 72; i += 1) {
        var a = i / 72 * Math.PI * 2;
        ring.push([A[0] + state.r * Math.cos(a), 0.62, A[1] + state.r * Math.sin(a)]);
      }
      M.trace(ring, "#c08a3e", traceLayer);
      var arc = [];
      for (i = 0; i <= 48; i += 1) {
        var th = i / 48 * 360;
        var p = pose(th);
        arc.push([C[0] + p.u[0] * 3.3, 0.52, C[1] + p.u[1] * 3.3]);
      }
      M.trace(arc, "#5f868d", traceLayer);
    }

    // 导杆（在后）→ 滑块（中）→ 曲柄（前）
    M.bar(back, tip, 0.15, 0.18, 0.14, "teal", linkLayer);
    var sleeveA = [B[0] - u[0] * 0.26, B[1] - u[1] * 0.26];
    var sleeveB = [B[0] + u[0] * 0.26, B[1] + u[1] * 0.26];
    M.bar(sleeveA, sleeveB, 0.24, -0.06, 0.26, "slate", linkLayer);
    M.bar(A, B, 0.18, -0.24, 0.16, "brass", linkLayer);

    M.pin(C, 0.18, 0.15, 0.28, "slate", pinLayer);
    M.pin(B, -0.24, 0.15, 0.32, "ink", pinLayer);
    M.pin(A, -0.24, 0.16, 0.34, "ink", pinLayer);

    if (state.showLabels) {
      M.label([A[0], -0.24, A[1]], "A", -20, -2, labelLayer);
      M.label([B[0], -0.24, B[1]], "B", 18, -8, labelLayer);
      M.label([C[0], 0.18, C[1]], "C", -18, 16, labelLayer);
    }

    var phi = swing(state.theta);
    var psiMax = 2 * Math.asin(Math.min(1, state.r / DIMS.a)) / FK.DEG;
    var K = (180 + psiMax) / (180 - psiMax);

    document.getElementById("thetaOut").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("phiOut").textContent = phi.toFixed(1) + "°";
    document.getElementById("swingOut").textContent = psiMax.toFixed(1) + "°";
    document.getElementById("kOut").textContent = K.toFixed(2);
  }

  function syncInputs() {
    document.getElementById("theta").value = state.theta;
    document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("r").value = state.r;
    document.getElementById("rValue").textContent = state.r.toFixed(2);
  }

  document.getElementById("theta").addEventListener("input", function (e) {
    state.theta = Number(e.target.value); syncInputs(); render();
  });
  document.getElementById("r").addEventListener("input", function (e) {
    state.r = Number(e.target.value); syncInputs(); render();
  });
  document.getElementById("auto").addEventListener("change", function (e) { state.auto = e.target.checked; });
  document.getElementById("showTrace").addEventListener("change", function (e) {
    state.showTrace = e.target.checked; render();
  });
  document.getElementById("showLabels").addEventListener("change", function (e) {
    state.showLabels = e.target.checked; render();
  });
  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 0; state.r = DIMS.r;
    state.auto = true; state.showTrace = true; state.showLabels = true;
    document.getElementById("auto").checked = true;
    document.getElementById("showTrace").checked = true;
    document.getElementById("showLabels").checked = true;
    scene.reset();
    syncInputs(); render();
  });

  var last = 0;
  function tick(ts) {
    if (!last) last = ts;
    var dt = Math.min(0.05, (ts - last) / 1000);
    last = ts;
    if (state.auto) {
      state.theta = (state.theta + 64 * dt) % 360;
      document.getElementById("theta").value = state.theta;
      document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
      render();
    }
    requestAnimationFrame(tick);
  }

  syncInputs();
  window.FigureLayout.attach(scene, state, render, 5.4);
  requestAnimationFrame(tick);
}());
