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

  // 双摇杆：两连架杆都只能摆动（造型机翻箱机构）。摆角由主动摇杆的转角决定。
  var DIMS = { ad: 3.6, ab: 2.4, bc: 1.6, cd: 2.4, z0: 1.05 };
  var A = [0, DIMS.z0];
  var D = [DIMS.ad, DIMS.z0];

  var state = { theta: 60, cd: DIMS.cd, auto: true, showTrace: true, showLabels: true };

  function rad2deg(v) { return v * 180 / Math.PI; }

  function circleHit(c0, r0, c1, r1, upper) {
    var dx = c1[0] - c0[0], dz = c1[1] - c0[1];
    var dist = Math.sqrt(dx * dx + dz * dz);
    if (dist > r0 + r1 - 1e-6 || dist < Math.abs(r0 - r1) + 1e-6) return null;
    var a = (r0 * r0 - r1 * r1 + dist * dist) / (2 * dist);
    var h = Math.sqrt(Math.max(0, r0 * r0 - a * a));
    var mx = c0[0] + a * dx / dist, mz = c0[1] + a * dz / dist;
    var p1 = [mx + h * dz / dist, mz - h * dx / dist];
    var p2 = [mx - h * dz / dist, mz + h * dx / dist];
    return upper ? (p1[1] > p2[1] ? p1 : p2) : (p1[1] < p2[1] ? p1 : p2);
  }

  function pose(theta) {
    var t = theta * FK.DEG;
    var B = [A[0] + DIMS.ab * Math.cos(t), A[1] + DIMS.ab * Math.sin(t)];
    var C = circleHit(B, DIMS.bc, D, state.cd, true);
    return { B: B, C: C };
  }

  function solve() { return pose(state.theta); }

  // 装配条件：|BC − CD| ≤ |BD| ≤ BC + CD。BD 只随主动摇杆转角变化，
  // 因此双摇杆的摆动范围由上式唯一确定，超出即无法装配。
  var THETA_MIN = 16;

  function thetaMax(cd) {
    var hi = DIMS.bc + cd - 0.02;
    var c = (DIMS.ab * DIMS.ab + DIMS.ad * DIMS.ad - hi * hi) / (2 * DIMS.ab * DIMS.ad);
    if (c <= -1) return 180;
    if (c >= 1) return THETA_MIN;
    return Math.acos(c) / FK.DEG;
  }

  function clampTheta() {
    var max = Math.max(THETA_MIN + 1, thetaMax(state.cd));
    if (state.theta < THETA_MIN) state.theta = THETA_MIN;
    if (state.theta > max - 0.5) state.theta = max - 0.5;
    var input = document.getElementById("theta");
    input.min = String(THETA_MIN);
    input.max = String(Math.round(max - 0.5));
    return max;
  }

  function sweep(fn, y) {
    var pts = [], i;
    var max = thetaMax(state.cd) - 0.6;
    for (i = 0; i <= 80; i += 1) {
      var theta = THETA_MIN + i / 80 * Math.max(0.1, max - THETA_MIN);
      var s = pose(theta);
      if (s.C) pts.push(fn(s, y));
    }
    return pts;
  }

  function stand(x, zTop) {
    M.box([x, 0.62, 0.09], [0.56, 0.72, 0.18], "graphite", frameLayer);
    M.box([x, 0.74, zTop / 2 + 0.04], [0.30, 0.30, zTop - 0.06], "graphite", frameLayer);
    M.box([x, 0.40, zTop], [0.30, 0.52, 0.30], "slate", frameLayer);
  }

  function render() {
    window.FigureLayout.fit(scene, state, 5.6);
    baseLayer.replaceChildren();
    frameLayer.replaceChildren();
    traceLayer.replaceChildren();
    linkLayer.replaceChildren();
    pinLayer.replaceChildren();
    labelLayer.replaceChildren();

    M.bench(-1.2, 5.0, -1.15, 1.15, 0.22, baseLayer, { label: "FIG 3-12", labelX: 0.2 });
    stand(A[0], DIMS.z0);
    stand(D[0], DIMS.z0);
    M.box([(A[0] + D[0]) / 2, 0.46, DIMS.z0], [D[0] - A[0] + 0.1, 0.12, 0.15], "graphite", frameLayer);

    // 先把转角夹进可装配区间，滑块范围随之更新，避免出现“无法装配”的空画面
    clampTheta();
    syncInputs();

    var s = solve();
    if (!s.C) {
      document.getElementById("psiOut").textContent = "临界位置";
      return;
    }
    var B = s.B, C = s.C;

    if (state.showTrace) {
      M.trace(sweep(function (p, y) { return [p.B[0], y, p.B[1]]; }, 0.62), "#c08a3e", traceLayer);
      M.trace(sweep(function (p, y) { return [p.C[0], y, p.C[1]]; }, 0.62), "#5f868d", traceLayer);
    }

    M.bar(D, C, 0.17, 0.22, 0.16, "teal", linkLayer);
    M.bar(B, C, 0.16, -0.42, 0.16, "steel", linkLayer);
    M.bar(A, B, 0.18, -0.22, 0.16, "brass", linkLayer);

    M.pin(D, 0.22, 0.15, 0.26, "slate", pinLayer);
    M.pin(C, -0.10, 0.14, 0.80, "slate", pinLayer);
    M.pin(B, -0.32, 0.14, 0.36, "slate", pinLayer);
    M.pin(A, -0.22, 0.16, 0.30, "ink", pinLayer);

    if (state.showLabels) {
      M.label([A[0], -0.20, A[1]], "A", -20, 4, labelLayer);
      M.label([B[0], -0.20, B[1]], "B", 4, -16, labelLayer);
      M.label([C[0], 0.0, C[1]], "C", 16, -6, labelLayer);
      M.label([D[0], 0.20, D[1]], "D", 18, 2, labelLayer);
    }

    var psi = rad2deg(Math.atan2(C[1] - D[1], C[0] - D[0]));
    var coupler = rad2deg(Math.atan2(C[1] - B[1], C[0] - B[0]));
    document.getElementById("thetaOut").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("psiOut").textContent = psi.toFixed(1) + "°";
    document.getElementById("couplerOut").textContent = coupler.toFixed(1) + "°";
  }

  function syncInputs() {
    document.getElementById("theta").value = state.theta;
    document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("cd").value = state.cd;
    document.getElementById("cdValue").textContent = state.cd.toFixed(2);
  }

  document.getElementById("theta").addEventListener("input", function (e) {
    state.theta = Number(e.target.value);
    syncInputs(); render();
  });
  document.getElementById("cd").addEventListener("input", function (e) {
    state.cd = Number(e.target.value);
    syncInputs(); render();
  });
  document.getElementById("auto").addEventListener("change", function (e) { state.auto = e.target.checked; });
  document.getElementById("showTrace").addEventListener("change", function (e) {
    state.showTrace = e.target.checked; render();
  });
  document.getElementById("showLabels").addEventListener("change", function (e) {
    state.showLabels = e.target.checked; render();
  });
  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 60; state.cd = DIMS.cd;
    state.auto = true; state.showTrace = true; state.showLabels = true;
    document.getElementById("auto").checked = true;
    document.getElementById("showTrace").checked = true;
    document.getElementById("showLabels").checked = true;
    scene.reset();
    syncInputs(); render();
  });

  var last = 0, dir = 1;
  function tick(ts) {
    if (!last) last = ts;
    var dt = Math.min(0.05, (ts - last) / 1000);
    last = ts;
    if (state.auto) {
      var hi = Math.max(THETA_MIN + 6, thetaMax(state.cd) - 4);
      state.theta += dir * 46 * dt;
      if (state.theta > hi) { state.theta = hi; dir = -1; }
      if (state.theta < THETA_MIN + 2) { state.theta = THETA_MIN + 2; dir = 1; }
      render();
    }
    requestAnimationFrame(tick);
  }

  syncInputs();
  window.FigureLayout.attach(scene, state, render, 5.6);
  requestAnimationFrame(tick);
}());
