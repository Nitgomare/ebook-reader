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
    origin: { x: 470, y: 320 },
    scale: 96,
    yaw: -0.40,
    pitch: 0.30,
    minScale: 34,
    maxScale: 190
  });
  var M = MK.make(scene);

  // 双曲柄：最短杆是机架，两个连架杆都能整周回转（冲床的传动部分）
  var DIMS = { ad: 1.2, ab: 2.0, bc: 2.4, cd: 1.8, z0: 2.30 };
  var A = [0, DIMS.z0];
  var D = [DIMS.ad, DIMS.z0];

  var state = { theta: 0, bc: DIMS.bc, auto: true, showTrace: true, showLabels: true };

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
    var C = circleHit(B, state.bc, D, DIMS.cd, true);
    return { B: B, C: C };
  }

  function solve() { return pose(state.theta); }

  function phiAt(theta) {
    var s = pose(theta);
    if (!s.C) return null;
    return rad2deg(Math.atan2(s.C[1] - D[1], s.C[0] - D[0]));
  }

  function ring(center, radius, y) {
    var pts = [], i;
    for (i = 0; i <= 72; i += 1) {
      var a = i / 72 * Math.PI * 2;
      pts.push([center[0] + radius * Math.cos(a), y, center[1] + radius * Math.sin(a)]);
    }
    return pts;
  }

  function arcOf(samples, y) {
    var pts = [], i;
    for (i = 0; i <= 96; i += 1) {
      var s = pose(i / 96 * 360);
      if (s.C) pts.push([s.C[0], y, s.C[1]]);
    }
    return pts;
  }

  function stand(x, zTop) {
    M.box([x, 0.62, 0.09], [0.52, 0.72, 0.18], "graphite", frameLayer);
    M.box([x, 0.74, zTop / 2 + 0.04], [0.28, 0.28, zTop - 0.06], "graphite", frameLayer);
    M.box([x, 0.40, zTop], [0.28, 0.52, 0.30], "slate", frameLayer);
  }

  function render() {
    window.FigureLayout.fit(scene, state, 6.4);
    baseLayer.replaceChildren();
    frameLayer.replaceChildren();
    traceLayer.replaceChildren();
    linkLayer.replaceChildren();
    pinLayer.replaceChildren();
    labelLayer.replaceChildren();

    M.bench(-1.7, 3.1, -1.15, 1.15, 0.22, baseLayer, { label: "FIG 3-6", labelX: -0.4 });
    stand(A[0], DIMS.z0);
    stand(D[0], DIMS.z0);
    M.box([(A[0] + D[0]) / 2, 0.46, DIMS.z0], [D[0] - A[0] + 0.1, 0.12, 0.15], "graphite", frameLayer);

    var s = solve();
    if (!s.C) {
      document.getElementById("phiOut").textContent = "无法装配";
      return;
    }
    var B = s.B, C = s.C;

    if (state.showTrace) {
      M.trace(ring(A, DIMS.ab, 0.62), "#c08a3e", traceLayer);
      M.trace(ring(D, DIMS.cd, 0.62), "#8a76b8", traceLayer);
      M.trace(arcOf(null, 0.30), "#5f868d", traceLayer);
    }

    // 从动曲柄在后、连杆居中、主动曲柄在前
    M.bar(D, C, 0.17, 0.20, 0.16, "teal", linkLayer);
    M.bar(B, C, 0.16, 0.00, 0.16, "steel", linkLayer);
    M.bar(A, B, 0.18, -0.20, 0.16, "brass", linkLayer);

    M.pin(D, 0.20, 0.15, 0.26, "slate", pinLayer);
    M.pin(C, 0.00, 0.14, 0.30, "slate", pinLayer);
    M.pin(B, -0.20, 0.14, 0.30, "slate", pinLayer);
    M.pin(A, -0.20, 0.16, 0.34, "ink", pinLayer);

    if (state.showLabels) {
      M.label([A[0], -0.20, A[1]], "A", -20, 4, labelLayer);
      M.label([B[0], -0.20, B[1]], "B", 6, -16, labelLayer);
      M.label([C[0], 0.0, C[1]], "C", 16, -6, labelLayer);
      M.label([D[0], 0.20, D[1]], "D", 18, 2, labelLayer);
    }

    var phi = phiAt(state.theta);
    var p1 = phiAt(state.theta + 0.4), p0 = phiAt(state.theta - 0.4);
    var ratio = (p1 !== null && p0 !== null) ? (p1 - p0) / 0.8 : NaN;
    if (ratio < -180) ratio += 360;
    if (ratio > 180) ratio -= 360;

    document.getElementById("thetaOut").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("phiOut").textContent = (phi === null ? "—" : phi.toFixed(1) + "°");
    document.getElementById("ratioOut").textContent = isNaN(ratio) ? "—" : ratio.toFixed(2);
  }

  function syncInputs() {
    document.getElementById("theta").value = state.theta;
    document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("bc").value = state.bc;
    document.getElementById("bcValue").textContent = state.bc.toFixed(2);
  }

  document.getElementById("theta").addEventListener("input", function (e) {
    state.theta = Number(e.target.value);
    syncInputs(); render();
  });
  document.getElementById("bc").addEventListener("input", function (e) {
    state.bc = Number(e.target.value);
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
    state.theta = 0; state.bc = DIMS.bc;
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
      state.theta = (state.theta + 62 * dt) % 360;
      document.getElementById("theta").value = state.theta;
      document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
      render();
    }
    requestAnimationFrame(tick);
  }

  syncInputs();
  window.FigureLayout.attach(scene, state, render, 4.6);
  requestAnimationFrame(tick);
}());
