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

  // 曲柄滑块：偏距 e = 0 时对心，e > 0 时偏置；滑块沿水平导轨往复
  // z0 抬高到 1.45：曲柄整周回转时最低点仍在台面（z=0）之上
  var DIMS = { r: 1.2, l: 3.6, z0: 1.45 };
  var A = [0, DIMS.z0];

  var state = { theta: 30, r: DIMS.r, e: 0.6, auto: true, showTrace: true, showLabels: true };

  function rad2deg(v) { return v * 180 / Math.PI; }

  function pose(theta) {
    var t = theta * FK.DEG;
    var B = [A[0] + state.r * Math.cos(t), A[1] + state.r * Math.sin(t)];
    var zAxis = A[1] - state.e;
    var dz = B[1] - zAxis;
    var under = DIMS.l * DIMS.l - dz * dz;
    if (under <= 0) return { B: B, C: null, zAxis: zAxis };
    return { B: B, C: [B[0] + Math.sqrt(under), zAxis], zAxis: zAxis };
  }

  function solve() { return pose(state.theta); }

  function stroke() {
    var lo = Infinity, hi = -Infinity, i;
    for (i = 0; i <= 180; i += 1) {
      var s = pose(i / 180 * 360);
      if (!s.C) continue;
      lo = Math.min(lo, s.C[0]);
      hi = Math.max(hi, s.C[0]);
    }
    return hi - lo;
  }

  function stand() {
    M.box([A[0], 0.44, 0.09], [0.60, 0.64, 0.18], "graphite", frameLayer);
    M.box([A[0], 0.44, DIMS.z0 / 2 + 0.04], [0.32, 0.32, DIMS.z0 - 0.06], "graphite", frameLayer);
    M.box([A[0], 0.42, DIMS.z0], [0.34, 0.40, 0.30], "slate", frameLayer);
  }

  /** 导轨：一条中央导轨，滑块是骑在导轨顶面上的方座（底面正好落在导轨顶面） */
  function guide(zAxis, x0, x1) {
    var mid = (x0 + x1) / 2;
    var bedBottom = zAxis - 0.44;
    // 床身：托住导轨
    M.box([mid, 0, zAxis - 0.40], [x1 - x0, 0.52, 0.08], "graphite", frameLayer);
    // 中央导轨：顶面 zAxis-0.10，滑块坐在这上面
    M.box([mid, 0, zAxis - 0.25], [x1 - x0, 0.30, 0.30], "slate", frameLayer);
    // 两端支座：从台面（z=0）接到床身底面
    M.box([x0 + 0.26, 0, bedBottom / 2], [0.34, 0.50, bedBottom], "graphite", frameLayer);
    M.box([x1 - 0.26, 0, bedBottom / 2], [0.34, 0.50, bedBottom], "graphite", frameLayer);
  }

  function render() {
    window.FigureLayout.fit(scene, state, 5.2);
    baseLayer.replaceChildren();
    frameLayer.replaceChildren();
    traceLayer.replaceChildren();
    linkLayer.replaceChildren();
    pinLayer.replaceChildren();
    labelLayer.replaceChildren();

    var s0 = solve();
    var zAxis = s0.zAxis;
    var x0 = -1.4, x1 = 5.2;

    M.bench(-1.6, 5.6, -1.15, 1.15, 0.22, baseLayer, { label: "FIG 3-15", labelX: 0.0 });
    stand();
    guide(zAxis, x0, x1);

    if (!s0.C) {
      document.getElementById("sOut").textContent = "无法装配";
      return;
    }
    var B = s0.B, C = s0.C;

    if (state.showTrace) {
      var ring = [], i;
      for (i = 0; i <= 72; i += 1) {
        var a = i / 72 * Math.PI * 2;
        ring.push([A[0] + state.r * Math.cos(a), 0.62, A[1] + state.r * Math.sin(a)]);
      }
      M.trace(ring, "#c08a3e", traceLayer);
      M.trace([[C[0] - 0.22, 0.62, zAxis + 0.10], [C[0] + 0.22, 0.62, zAxis + 0.10]], "#5f868d", traceLayer);
    }

    M.bar(B, C, 0.16, -0.42, 0.16, "steel", linkLayer);
    M.bar(A, B, 0.18, -0.22, 0.16, "brass", linkLayer);
    // 滑块：骑在导轨顶面（zAxis-0.10）上的方座，底面与轨面贴合
    M.box([C[0], 0, zAxis + 0.10], [0.46, 0.56, 0.40], "slate", linkLayer);

    M.pin([C[0], zAxis + 0.10], -0.10, 0.13, 0.80, "slate", pinLayer);
    M.pin(B, -0.32, 0.14, 0.36, "slate", pinLayer);
    M.pin(A, -0.22, 0.16, 0.30, "ink", pinLayer);

    if (state.showLabels) {
      M.label([A[0], -0.26, A[1]], "A", -20, 4, labelLayer);
      M.label([B[0], -0.26, B[1]], "B", 6, -16, labelLayer);
      M.label([C[0], 0.0, zAxis + 0.10], "C", 4, 24, labelLayer);
    }

    // 传动角：连杆与滑块运动方向（水平）之间的锐角
    var u = [B[0] - C[0], B[1] - C[1]];
    var gamma = rad2deg(Math.acos(Math.max(-1, Math.min(1, -u[0] / Math.sqrt(u[0] * u[0] + u[1] * u[1])))));

    document.getElementById("thetaOut").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("sOut").textContent = (C[0] - A[0]).toFixed(2);
    document.getElementById("hOut").textContent = stroke().toFixed(2);
    document.getElementById("gammaOut").textContent = gamma.toFixed(1) + "°";
  }

  function syncInputs() {
    document.getElementById("theta").value = state.theta;
    document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
    document.getElementById("r").value = state.r;
    document.getElementById("rValue").textContent = state.r.toFixed(2);
    document.getElementById("e").value = state.e;
    document.getElementById("eValue").textContent = state.e.toFixed(2);
  }

  document.getElementById("theta").addEventListener("input", function (e) {
    state.theta = Number(e.target.value); syncInputs(); render();
  });
  document.getElementById("r").addEventListener("input", function (e) {
    state.r = Number(e.target.value); syncInputs(); render();
  });
  document.getElementById("e").addEventListener("input", function (e) {
    state.e = Number(e.target.value); syncInputs(); render();
  });
  document.getElementById("auto").addEventListener("change", function (e) { state.auto = e.target.checked; });
  document.getElementById("showTrace").addEventListener("change", function (e) {
    state.showTrace = e.target.checked; render();
  });
  document.getElementById("showLabels").addEventListener("change", function (e) {
    state.showLabels = e.target.checked; render();
  });
  document.getElementById("reset").addEventListener("click", function () {
    state.theta = 30; state.r = DIMS.r; state.e = 0.6;
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
      state.theta = (state.theta + 70 * dt) % 360;
      document.getElementById("theta").value = state.theta;
      document.getElementById("thetaValue").textContent = state.theta.toFixed(0) + "°";
      render();
    }
    requestAnimationFrame(tick);
  }

  syncInputs();
  window.FigureLayout.attach(scene, state, render, 5.2);
  requestAnimationFrame(tick);
}());
