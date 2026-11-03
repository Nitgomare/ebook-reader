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
    scale: 96,
    yaw: -0.40,
    pitch: 0.30,
    minScale: 34,
    maxScale: 190
  });
  var M = MK.make(scene);

  // 机构平面离台面 = 1.05，机架铰链 A、D 固定；曲柄 1、连杆 2、摇杆 3、机架 4
  var DIMS = { r: 1.0, l: 3.2, d: 2.4, ad: 3.0, z0: 1.05 };
  var A = [0, DIMS.z0];
  var D = [DIMS.ad, DIMS.z0];

  var state = {
    theta: 42, r: DIMS.r, l: DIMS.l,
    auto: true, showTrace: true, showLabels: true
  };

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

  /** 当前机构的四个铰点：A、B（曲柄端）、C（连杆-摇杆）、D */
  function solve() {
    var t = state.theta * FK.DEG;
    var B = [A[0] + state.r * Math.cos(t), A[1] + state.r * Math.sin(t)];
    var C = circleHit(B, state.l, D, DIMS.d, true);
    return { A: A, B: B, C: C, D: D };
  }

  function traceCircle(center, radius) {
    var pts = [];
    for (var i = 0; i <= 72; i += 1) {
      var a = i / 72 * Math.PI * 2;
      pts.push([center[0] + radius * Math.cos(a), 0.62, center[1] + radius * Math.sin(a)]);
    }
    return pts;
  }

  /** 摇杆铰点 C 的摆动轨迹：把曲柄转一整圈，取每个位置的真实解 */
  function traceRockerArc() {
    var pts = [], keep = state.theta, i;
    for (i = 0; i <= 96; i += 1) {
      state.theta = i / 96 * 360;
      // 机架 4：把 A、D 两个固定铰连成一根卧杆，压在立柱之间
    M.box([(A[0] + D[0]) / 2, 0.46, DIMS.z0], [D[0] - A[0] + 0.1, 0.12, 0.15], "graphite", frameLayer);

    var s = solve();
      if (s.C) pts.push([s.C[0], 0.62, s.C[1]]);
    }
    state.theta = keep;
    return pts;
  }

  function stand(x, zTop) {
    M.box([x, 0.62, 0.09], [0.56, 0.72, 0.18], "graphite", frameLayer);
    M.box([x, 0.74, zTop / 2 + 0.04], [0.30, 0.30, zTop - 0.06], "graphite", frameLayer);
    M.box([x, 0.40, zTop], [0.30, 0.52, 0.30], "slate", frameLayer);
  }

  function render() {
    window.FigureLayout.fit(scene, state, 4.9);
    baseLayer.replaceChildren();
    frameLayer.replaceChildren();
    traceLayer.replaceChildren();
    linkLayer.replaceChildren();
    pinLayer.replaceChildren();
    labelLayer.replaceChildren();

    M.bench(-1.2, 4.4, -1.15, 1.15, 0.22, baseLayer, { label: "FIG 3-3", labelX: 0.3 });
    stand(A[0], DIMS.z0);
    stand(D[0], DIMS.z0);

    // 机架 4：把 A、D 两个固定铰连成一根卧杆，压在立柱之间
    M.box([(A[0] + D[0]) / 2, 0.46, DIMS.z0], [D[0] - A[0] + 0.1, 0.12, 0.15], "graphite", frameLayer);

    var s = solve();
    if (!s.C) {
      document.getElementById("psiOut").textContent = "无法装配";
      return;
    }
    var B = s.B, C = s.C;

    if (state.showTrace) {
      M.trace(traceCircle(A, state.r), "#c08a3e", traceLayer);
      M.trace(traceRockerArc(), "#5f868d", traceLayer);
    }

    // 从动件在后、连杆居中、主动曲柄在前：三层深度，遮挡关系与真实机构一致
    M.bar(D, C, 0.17, 0.20, 0.16, "teal", linkLayer);
    M.bar(B, C, 0.16, 0.00, 0.16, "steel", linkLayer);
    M.bar(A, B, 0.18, -0.20, 0.16, "brass", linkLayer);

    M.pin(D, 0.20, 0.15, 0.26, "slate", pinLayer);
    M.pin(C, 0.00, 0.14, 0.30, "slate", pinLayer);
    M.pin(B, -0.20, 0.14, 0.30, "slate", pinLayer);
    M.pin(A, -0.20, 0.16, 0.34, "ink", pinLayer);

    if (state.showLabels) {
      M.label([A[0], -0.20, A[1]], "A", -20, 4, labelLayer);
      M.label([B[0], -0.20, B[1]], "B", 4, -16, labelLayer);
      M.label([C[0], 0.0, C[1]], "C", 16, -6, labelLayer);
      M.label([D[0], 0.20, D[1]], "D", 18, 4, labelLayer);
    }

    var psi = rad2deg(Math.atan2(C[1] - D[1], C[0] - D[0]));
    var u = [B[0] - C[0], B[1] - C[1]];
    var v = [D[0] - C[0], D[1] - C[1]];
    var denom = Math.sqrt(u[0] * u[0] + u[1] * u[1]) * Math.sqrt(v[0] * v[0] + v[1] * v[1]);
    var cosG = Math.max(-1, Math.min(1, (u[0] * v[0] + u[1] * v[1]) / denom));
    var gamma = rad2deg(Math.acos(cosG));
    if (gamma > 90) gamma = 180 - gamma;

    document.getElementById("thetaOut").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("psiOut").textContent = psi.toFixed(1) + "°";
    document.getElementById("gammaOut").textContent = gamma.toFixed(1) + "°";
  }

  function syncInputs() {
    document.getElementById("theta").value = state.theta;
    document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("r").value = state.r;
    document.getElementById("rValue").textContent = state.r.toFixed(2);
    document.getElementById("l").value = state.l;
    document.getElementById("lValue").textContent = state.l.toFixed(2);
  }

  document.getElementById("theta").addEventListener("input", function (e) {
    state.theta = Number(e.target.value);
    syncInputs(); render();
  });
  document.getElementById("r").addEventListener("input", function (e) {
    state.r = Number(e.target.value);
    syncInputs(); render();
  });
  document.getElementById("l").addEventListener("input", function (e) {
    state.l = Number(e.target.value);
    syncInputs(); render();
  });
  document.getElementById("auto").addEventListener("change", function (e) {
    state.auto = e.target.checked;
  });
  document.getElementById("showTrace").addEventListener("change", function (e) {
    state.showTrace = e.target.checked;
    render();
  });
  document.getElementById("showLabels").addEventListener("change", function (e) {
    state.showLabels = e.target.checked;
    render();
  });
  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 42; state.r = DIMS.r; state.l = DIMS.l;
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
      state.theta = (state.theta + 66 * dt) % 360;
      document.getElementById("theta").value = state.theta;
      document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
      render();
    }
    requestAnimationFrame(tick);
  }

  syncInputs();
  window.FigureLayout.attach(scene, state, render, 4.9);
  requestAnimationFrame(tick);
}());
