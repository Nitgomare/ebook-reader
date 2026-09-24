"""图4-8 平面三连杆机器人的平面几何关系——克雷格《机器人学导论（第3版）》4.4 节几何解。

教材依据（4.4 节"几何解"原文）：
- "图4-8中示出了由 l1 和 l2 所组成的三角形及连接坐标系{0}的原点和坐标系{3}的原点的连线。
  图中虚线表示该三角形的另一种可能情况，同样能够达到坐标系(3)的位置。对于实线表示的三角形，
  利用余弦定理求解 θ2： x² + y² = l1² + l2² − 2·l1·l2·cos(180+θ2)  …… 式(4-29)"
- 式(4-30)：c2 = (x²+y²−l1²−l2²)/(2l1l2)；
- 式(4-31)：β = Atan2(y, x)；
- 式(4-32)：cosψ = (x²+y²+l1²−l2²)/(2·l1·√(x²+y²))，求反余弦使 0 ≤ ψ ≤ 180°；
- 式(4-33)：θ1 = β ± ψ，"当 θ2 < 0 时 θ1 取 + 号；当 θ2 > 0 时 θ1 取 − 号"；
- 同节："为使该三角形成立，到目标点的距离 √(x²+y²) 必须小于或等于两个连杆的长度之和 l1+l2"。
- 另一解："另一个可能的解（由虚线所示的三角形）可以通过对称关系 θ2′ = −θ2 得到。"

注意：式(4-29) 与式(4-12) 等价（cos(180+θ2) = −cosθ2），脚本内两条式子都做了一致性断言，
因此式(4-29) 的 180+θ2 取的是三角形内角（θ2 = 0 时两连杆拉直，内角为 180°）。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

EXTRA_CSS = """
.control-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 7px 12px;
  margin-top: 10px;
}
.control-grid .control { margin-top: 0; min-width: 0; }
.control-grid .control label { font-size: 12px; }
.control-grid .control output { font-size: 12px; }
.control-grid input[type="range"] { margin: 7px 0 1px; }

.readout { max-width: min(640px, calc(100% - 32px)); }
.readout table { border-collapse: collapse; width: 100%; font: inherit; }
.readout th {
  padding: 1px 10px 3px 0;
  color: #5b6a80;
  font: 700 12px -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
  text-align: left;
  white-space: nowrap;
}
.readout td {
  padding: 1px 12px 1px 0;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}
.readout td:last-child, .readout th:last-child { padding-right: 0; }
.readout .row { white-space: normal; }
.readout .warn { color: #b45309; font-weight: 700; }
.readout .ok { color: #15803d; font-weight: 700; }
.readout .n1 { color: #d93025; font-weight: 700; }
.readout .n2 { color: #64748b; }

@media (max-width: 720px) {
  .panel h1 { font-size: 13.5px; }
  .control-grid { gap: 5px 8px; }
  .control-grid .control label { font-size: 10.5px; }
  .control-grid .control output { font-size: 10.5px; }
  .readout { font-size: 12px; line-height: 1.45; padding: 6px 8px; }
  .readout .small { font-size: 9.5px; }
  /* 两个长图例各自独占一行，避免末行被面板裁掉 */
  .legend { margin-top: 7px; padding-top: 7px; }
  .legend span { flex: 1 1 100%; }
  /* 窄屏下把表格摊平：每个解一行、角度与末端各占一行 */
  .readout table { display: block; }
  .readout thead { display: none; }
  .readout tbody { display: block; }
  .readout tr { display: block; margin-top: 3px; font-size: 10px; line-height: 1.5; }
  .readout td { display: inline; padding: 0; font-size: 10px; }
  .readout td:first-child { font-weight: 700; }
  .readout td:nth-child(2)::before { content: "θ₁="; }
  .readout td:nth-child(3)::before { content: " θ₂="; }
  .readout td:nth-child(4) { display: block; }
  .readout td:nth-child(4)::before { content: "末端 "; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="平面三连杆机器人由 l1、l2 组成的三角形与 β、ψ、θ2 的几何关系">
  <defs>
    <marker id="mAxis" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"></path>
    </marker>
  </defs>
  <g id="circle"></g>
  <g id="angles"></g>
  <g id="tri1"></g>
  <g id="tri2"></g>
  <g id="labels"></g>
</svg>

<section class="panel" aria-label="图4-8 控制面板">
  <div class="panel-head">
    <div>
      <h1>图4-8 平面三连杆的平面几何关系</h1>
      <p class="subtitle">用余弦定理求 θ₂，再解出 β、ψ 与 θ₁ = β ± ψ：
        l₁ 与 l₂ 组成的三角形有实线、虚线两种摆法，末端都落在目标点。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="control-grid">
    <div class="control">
      <div class="control-head"><label for="tx">目标 x</label><output id="txValue">0.90</output></div>
      <input id="tx" type="range" min="-1.6" max="1.6" step="0.02" value="0.7">
    </div>
    <div class="control">
      <div class="control-head"><label for="ty">目标 y</label><output id="tyValue">0.50</output></div>
      <input id="ty" type="range" min="-1.6" max="1.6" step="0.02" value="0.6">
    </div>
    <div class="control">
      <div class="control-head"><label for="l1">连杆 l₁</label><output id="l1Value">1.00</output></div>
      <input id="l1" type="range" min="0.5" max="1.2" step="0.05" value="1">
    </div>
    <div class="control">
      <div class="control-head"><label for="l2">连杆 l₂</label><output id="l2Value">1.00</output></div>
      <input id="l2" type="range" min="0.5" max="1.2" step="0.05" value="1">
    </div>
  </div>

  <div class="options">
    <label><input id="showAux" type="checkbox" checked>辅助线（O→T 连线与半径圆）</label>
    <label><input id="showAlt" type="checkbox" checked>第二组解的虚线三角形</label>
  </div>

  <div class="legend">
    <span><i style="background:#d93025"></i>实线三角形（θ₂ &lt; 0，θ₁ = β + ψ）</span>
    <span><i style="background:#94a3b8"></i>虚线三角形（θ₂′ = −θ₂，θ₁ = β − ψ）</span>
    <span><i style="background:#2563eb"></i>O→T 连线（长度 √(x²+y²)）</span>
    <span><i style="background:#0e7490"></i>角 β</span>
    <span><i style="background:#d93025"></i>角 ψ</span>
    <span><i style="background:#7c3aed"></i>三角形内角 180−|θ₂|</span>
  </div>
</section>

<div class="hint">拖动平移 · 滚轮缩放 · 双击复位</div>

<div class="readout" id="readout">
  <div class="row">目标点 <strong>T</strong> = ( <span id="rtx">0.70</span>, <span id="rty">0.60</span> )，
    r = √(x²+y²) = <span id="rr">0.922</span>，l₁+l₂ = <span id="rreach">2.00</span></div>
  <div class="row small">β = Atan2(y, x) = <span id="rbeta">40.6°</span>　·　
    cos ψ = (r²+l₁²−l₂²)/(2l₁r) = <span id="rcospsi">0.4610</span> → ψ = <span id="rpsi">62.6°</span></div>
  <div class="row small">式(4-29) cos(180+θ₂) = <span id="rcos180">0.5753</span>
    <span class="small">（= −c₂，见式(4-30)）</span></div>
  <table id="kineTable">
    <thead><tr><th>解</th><th>θ₁</th><th>θ₂</th><th>末端 (x, y)</th></tr></thead>
    <tbody id="kineBody"></tbody>
  </table>
  <div class="row small" id="noteRow">…</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var L = {
    circle: document.getElementById("circle"),
    angles: document.getElementById("angles"),
    tri1: document.getElementById("tri1"),
    tri2: document.getElementById("tri2"),
    labels: document.getElementById("labels")
  };

  var BASE_SCALE = 110;
  var scene = new FK.Scene({ svg: viewport, origin: { x: 490, y: 262 }, scale: BASE_SCALE });
  var state = {
    tx: 0.7, ty: 0.6, l1: 1, l2: 1,
    showAux: true, showAlt: true
  };
  var pan = { x: 0, y: 0, dragging: false, id: null, lx: 0, ly: 0 };

  /* 纯平面投影：世界 (x, y) -> 屏幕 */
  scene.project = function (v) {
    var s = scene.state.scale;
    return {
      x: this.origin.x + pan.x + v[0] * s,
      y: this.origin.y + pan.y - v[1] * s,
      depth: v[2] || 0
    };
  };

  var COL = {
    base: "#2563eb", tri: "#d93025", triAlt: "#94a3b8",
    joint: "#1e293b", beta: "#0e7490", psi: "#d93025",
    inner: "#7c3aed", target: "#c2410c"
  };

  /* --------------------------------------------------------- 几何解 */
  /* 按 4.4 节几何法：式(4-30) 求 c2、式(4-32) 求 ψ（0~180°）、式(4-31) 求 β、式(4-33) 求 θ1。
     θ2 取 ± 得两组三角形：θ2 < 0 用 θ1 = β + ψ，θ2 > 0 用 θ1 = β − ψ。 */
  function geom(l1, l2, x, y) {
    var r = Math.hypot(x, y);
    var sum = l1 + l2;
    var beta = Math.atan2(y, x);
    var c2 = (r * r - l1 * l1 - l2 * l2) / (2 * l1 * l2);
    if (r < 1e-9) {
      return { r: 0, beta: 0, valid: false, reason: "origin", sum: sum, c2raw: c2, c2: c2 };
    }
    if (r > sum && r - sum > 1e-9) {
      return { r: r, beta: beta, valid: false, reason: "far", sum: sum, c2raw: c2, c2: c2 };
    }
    var c2c = Math.max(-1, Math.min(1, c2));
    var cosPsiRaw = (r * r + l1 * l1 - l2 * l2) / (2 * l1 * r);
    var cosPsi = Math.max(-1, Math.min(1, cosPsiRaw));
    var psi = Math.acos(cosPsi);
    var s2 = Math.sqrt(Math.max(0, 1 - c2c * c2c));
    var t2neg = Math.atan2(-s2, c2c);          /* θ2 < 0：θ1 = β + ψ */
    var t2pos = Math.atan2(s2, c2c);           /* θ2 > 0：θ1 = β − ψ */
    return {
      r: r, beta: beta, psi: psi, c2: c2c, c2raw: c2, cosPsi: cosPsi,
      valid: true, sum: sum, clamped: Math.abs(c2c - c2) > 1e-12,
      branch: [
        { name: "1", t2: t2neg, t1: beta + psi, sign: "+" },
        { name: "2", t2: t2pos, t1: beta - psi, sign: "\u2212" }
      ]
    };
  }

  function fk(l1, l2, t1, t2) {
    var e = [l1 * Math.cos(t1), l1 * Math.sin(t1)];
    return { elbow: e, tip: [e[0] + l2 * Math.cos(t1 + t2), e[1] + l2 * Math.sin(t1 + t2)] };
  }

  /* ------------------------------------------------------------- 绘图 */
  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    return scene.el("line", Object.assign({ x1: A.x, y1: A.y, x2: B.x, y2: B.y }, attrs || {}), parent);
  }
  function tag(v, str, attrs, dx, dy, parent) {
    var p = scene.project(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0),
      "font-size": 14.5, "font-weight": 700, class: "fk-axis-label"
    }, attrs || {}), parent);
    node.textContent = str;
    return node;
  }
  function dot(v, r, fill, parent) {
    var p = scene.project(v);
    return scene.el("circle", { cx: p.x, cy: p.y, r: r, fill: fill, stroke: "#fff", "stroke-width": 2.2, class: "fk-point" }, parent);
  }
  /* 角度弧：从 a0 到 a1（弧度，带符号），label 放在半径 lr 处的角平分线方向 */
  function arc(layer, cx, cy, r, a0, a1, color, label, lr, ldx, ldy, fs) {
    var n = 44, pts = [], i;
    for (i = 0; i <= n; i += 1) {
      var a = a0 + (a1 - a0) * i / n;
      pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a), 0]);
    }
    scene.polyline(pts, { stroke: color, class: "fk-arc" }, layer);
    if (!label) return;
    var mid = a0 + (a1 - a0) * 0.5;
    tag([cx + lr * Math.cos(mid), cy + lr * Math.sin(mid), 0], label,
      { fill: color, "font-size": fs || 14, "text-anchor": "middle" }, ldx || 0, ldy || 4, layer);
  }

  function drawAxes(reach) {
    var len = Math.max(0.7, Math.min(reach, 2.2));
    seg([-0.35, 0, 0], [len, 0, 0], { stroke: "#94a3b8", "stroke-width": 2, "marker-end": "url(#mAxis)" }, L.labels);
    seg([0, -0.35, 0], [0, len, 0], { stroke: "#94a3b8", "stroke-width": 2, "marker-end": "url(#mAxis)" }, L.labels);
    tag([len, 0, 0], "X", { fill: "#64748b", "font-size": 13 }, 6, 16, L.labels);
    tag([0, len, 0], "Y", { fill: "#64748b", "font-size": 13 }, 8, -4, L.labels);
  }

  function drawBase() {
    seg([-0.26, 0, 0], [0.26, 0, 0], { stroke: "#334155", "stroke-width": 3.4 }, L.tri1);
    for (var i = -3; i <= 3; i += 1) {
      seg([i * 0.08 - 0.12, 0, 0], [i * 0.08 + 0.02, -0.12, 0], { stroke: "#334155", "stroke-width": 1.5 }, L.tri1);
    }
  }

  function drawTriangle(G, color, width, dash, labelSide) {
    var e = G.elbow, tip = G.tip;
    /* 两条连杆（关节圆点在渲染末尾统一画，保证压在上面） */
    seg([0, 0, 0], e, { stroke: color, "stroke-width": width, "stroke-dasharray": dash, "stroke-linecap": "round" }, L.tri1);
    seg(e, tip, { stroke: color, "stroke-width": width, "stroke-dasharray": dash, "stroke-linecap": "round" }, L.tri1);
    var m1 = [e[0] * 0.5, e[1] * 0.5];
    var m2 = [(e[0] + tip[0]) * 0.5, (e[1] + tip[1]) * 0.5];
    var k = labelSide || 1;
    tag(m1, "l\u2081", { fill: color, "font-size": 14 }, 11 * k, 18 * k, L.labels);
    tag(m2, "l\u2082", { fill: color, "font-size": 14 }, 17 * k, 6 * k, L.labels);
  }

  /* ------------------------------------------------------------ 渲染 */
  function render() {
    var k;
    for (k in L) { if (Object.prototype.hasOwnProperty.call(L, k)) L[k].replaceChildren(); }

    var l1 = state.l1, l2 = state.l2, x = state.tx, y = state.ty;
    var G = geom(l1, l2, x, y);
    var valid = G.valid;
    var b1 = valid ? G.branch[0] : null;
    var b2 = valid ? G.branch[1] : null;
    var K1 = valid ? fk(l1, l2, b1.t1, b1.t2) : null;
    var K2 = valid ? fk(l1, l2, b2.t1, b2.t2) : null;

    if (state.showAux && G.r > 1e-9) {
      /* 半径圆：以 O 为心、r 为半径 */
      var pts = [], i;
      for (i = 0; i <= 160; i += 1) {
        var a = i * 2 * Math.PI / 160;
        pts.push([G.r * Math.cos(a), G.r * Math.sin(a), 0]);
      }
      scene.polyline(pts, { stroke: "#93c5fd", "stroke-width": 1.6, "stroke-dasharray": "6 7" }, L.circle);
    }
    drawAxes(l1 + l2);

    if (valid) {
      /* O→T 连线：两个三角形共用的底边，也是 β、ψ 角的参考边，恒显示 */
      seg([0, 0, 0], [x, y, 0], {
        stroke: COL.base, "stroke-width": 3
      }, L.circle);
      tag([x * 0.46, y * 0.46], "r", { fill: "#1d4ed8", "font-size": 14 }, 4, -14, L.circle);
    }

    drawBase();

    if (valid) {
      /* 第二组解（θ2 取 +，θ1 = β − ψ）——教材图4-8 的虚线三角形 */
      if (state.showAlt) {
        seg([0, 0, 0], K2.elbow, { stroke: COL.triAlt, "stroke-width": 8, "stroke-dasharray": "10 8", "stroke-linecap": "round" }, L.tri2);
        seg(K2.elbow, K2.tip, { stroke: COL.triAlt, "stroke-width": 8, "stroke-dasharray": "10 8", "stroke-linecap": "round" }, L.tri2);
        tag([K2.elbow[0] * 0.5, K2.elbow[1] * 0.5], "l\u2081\u2032", { fill: "#7b8798", "font-size": 13 }, 6, -10, L.labels);
        tag([(K2.elbow[0] + x) * 0.5, (K2.elbow[1] + y) * 0.5], "l\u2082\u2032", { fill: "#7b8798", "font-size": 13 }, 10, -8, L.labels);
        dot(K2.elbow, 5, "#cbd5e1", L.tri2);
      }
      /* 主解（θ2 取 −，θ1 = β + ψ）——实线三角形 */
      drawTriangle(K1, COL.tri, 11, null, -1);

      /* 角 β、ψ（O 处）与三角形内角（E 处） */
      var rb = Math.min(0.30, 0.34 * G.r);
      arc(L.angles, 0, 0, rb, 0, G.beta, COL.beta, "\u03b2", rb * 1.85, 22, 2, 14);
      var rp = rb * 1.72;
      arc(L.angles, 0, 0, rp, b1.t1, G.beta, COL.psi, "\u03c8", rp * 1.7, 8, 14, 14);
      if (state.showAlt) {
        arc(L.angles, 0, 0, rp * 1.22, G.beta, b2.t1, "#94a3b8", "\u03c8\u2032", rp * 1.85, -4, 18, 12.5);
      }
      /* 三角形内角：|180+θ2| = 180 − |θ2|。角弧画出来，"180−|θ2|" 的数值放在读数区，
         避免与 l1/l2 连线抢位置（三角形越扁，可用空隙越小）。 */
      var e0 = Math.atan2(-K1.elbow[1], -K1.elbow[0]);       /* E→O 方向 */
      var e1 = Math.atan2(y - K1.elbow[1], x - K1.elbow[0]); /* E→T 方向 */
      var ri = Math.min(0.30, 0.30 * l1, 0.30 * l2);
      var d0 = e1 - e0;
      while (d0 > Math.PI) d0 -= 2 * Math.PI;
      while (d0 < -Math.PI) d0 += 2 * Math.PI;
      arc(L.angles, K1.elbow[0], K1.elbow[1], ri, e0, e0 + d0, COL.inner, null, 0, 0, 0);

      /* 关节与目标点 */
      dot([0, 0, 0], 6.5, "#fff", L.labels);
      scene.el("circle", {
        cx: scene.project([0, 0, 0]).x, cy: scene.project([0, 0, 0]).y, r: 6.5,
        fill: "#fff", stroke: COL.joint, "stroke-width": 2.6
      }, L.labels);
      var ep = scene.project(K1.elbow);
      scene.el("circle", { cx: ep.x, cy: ep.y, r: 5.6, fill: "#fff", stroke: COL.joint, "stroke-width": 2.6 }, L.labels);
      dot([x, y, 0], 6.4, COL.target, L.labels);
      tag([x, y, 0], "T (x, y)", { fill: "#8a3a0c", "font-size": 14 }, 12, -12, L.labels);
      tag([0, 0, 0], "O", { fill: "#475569", "font-size": 14 }, -22, 20, L.labels);
      tag(K1.elbow, "E", { fill: "#475569", "font-size": 13.5 }, 6, -14, L.labels);
      tag(K1.elbow, "\u03b8\u2082 = " + FK.deg(degNorm(b1.t2), 1),
        { fill: "#a02a20", "font-size": 12.5 }, -128, -30, L.labels);
    }

    /* -------------------------------------------------------- 读数 */
    document.getElementById("rtx").textContent = FK.format(x, 2);
    document.getElementById("rty").textContent = FK.format(y, 2);
    document.getElementById("rr").textContent = FK.format(G.r, 3);
    document.getElementById("rreach").textContent = FK.format(l1 + l2, 3);

    function rowsHTML() {
      if (!valid) {
        return '<tr class="n1"><td>—</td><td>—</td><td>—</td><td>—</td></tr>';
      }
      var out = "";
      [[b1, "n1", "\u5b9e\u7ebf\uff1a\u03b8\u2081 = \u03b2 + \u03c8"], [b2, "n2", "\u865a\u7ebf\uff1a\u03b8\u2081 = \u03b2 \u2212 \u03c8"]].forEach(function (it) {
        var b = it[0], K = fk(l1, l2, b.t1, b.t2);
        out += '<tr class="' + it[1] + '"><td>' + it[2] + "</td>"
          + "<td>" + FK.deg(degNorm(b.t1), 1) + "</td>"
          + "<td>" + FK.deg(degNorm(b.t2), 1) + "</td>"
          + "<td>(" + FK.format(K.tip[0], 3) + ", " + FK.format(K.tip[1], 3) + ")</td></tr>";
      });
      return out;
    }
    document.getElementById("kineBody").innerHTML = rowsHTML();

    var note = document.getElementById("noteRow");
    if (!valid) {
      note.className = "row small warn";
      if (G.reason === "far") {
        note.textContent = "无解：r = " + FK.format(G.r, 3) + " > l\u2081+l\u2082 = " + FK.format(G.sum, 3)
          + "，两连杆三角形无法闭合。式(4-29) 的 c\u2082 = " + FK.format(G.c2raw, 3)
          + " 已越界（要求 −1 \u2264 c\u2082 \u2264 1），读数按 ±1 截断显示。";
      } else {
        note.textContent = "无解：目标点与原点重合（r = 0），\u03b2 \u4e0e \u03c8 均不确定。";
      }
      document.getElementById("rbeta").textContent = "—";
      document.getElementById("rpsi").textContent = "—";
      document.getElementById("rcospsi").textContent = "—";
      document.getElementById("rcos180").textContent = "—";
    } else {
      document.getElementById("rbeta").textContent = FK.deg(degNorm(G.beta), 1);
      document.getElementById("rpsi").textContent = FK.deg(G.psi, 1);
      document.getElementById("rcospsi").textContent = FK.format(G.cosPsi, 4);
      document.getElementById("rcos180").textContent = FK.format(-G.c2, 4);
      note.className = "row small ok";
      var e1 = Math.hypot(K1.tip[0] - x, K1.tip[1] - y);
      var e2 = Math.hypot(K2.tip[0] - x, K2.tip[1] - y);
      note.textContent = "两组解都把末端送到 T：误差 " + e1.toExponential(2) + " 与 " + e2.toExponential(2)
        + "；三角形内角 = 180\u2212|\u03b8\u2082| = " + FK.deg(180 - Math.abs(degNorm(b1.t2)), 1)
        + "，而 \u03b8\u2082 = " + FK.deg(degNorm(b1.t2), 1) + "（θ₂ = 0 时两连杆拉直、内角 180°）。";
      if (Math.abs(G.r - (l1 + l2)) < 1e-9) {
        note.textContent += " 当前 r = l\u2081+l\u2082：两连杆拉直，两组解重合。";
      }
      if (G.c2 >= 1 - 1e-12 || G.c2 <= -1 + 1e-12) {
        note.textContent += " 当前 c\u2082 已达 ±1 边界。";
      }
    }
  }

  function degNorm(rad) {
    var d = rad / FK.DEG;
    d = d % 360;
    if (d > 180) d -= 360;
    if (d <= -180) d += 360;
    return d;
  }

  /* ----------------------------------------------------------- 布局 */
  function layout() {
    var w = viewport.clientWidth || window.innerWidth;
    var h = viewport.clientHeight || window.innerHeight;
    if (w / h < 1.05) {
      viewport.setAttribute("viewBox", "0 0 420 780");
      viewport.setAttribute("preserveAspectRatio", "xMidYMin meet");
      scene.baseOrigin = { x: 228, y: 330 };
      scene.state.scale = 105;
      scene.defaults.scale = 105;
    } else {
      viewport.setAttribute("viewBox", "0 0 1000 620");
      viewport.setAttribute("preserveAspectRatio", "xMidYMid meet");
      scene.baseOrigin = { x: 490, y: 262 };
      scene.state.scale = BASE_SCALE;
      scene.defaults.scale = BASE_SCALE;
    }
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "tx", key: "tx", value: 0.7, format: function (v) { return FK.format(v, 2); } },
    { id: "ty", key: "ty", value: 0.6, format: function (v) { return FK.format(v, 2); } },
    { id: "l1", key: "l1", value: 1, format: function (v) { return FK.format(v, 2); } },
    { id: "l2", key: "l2", value: 1, format: function (v) { return FK.format(v, 2); } }
  ], state, render);

  FK.bindToggles([
    { id: "showAux", key: "showAux" },
    { id: "showAlt", key: "showAlt" }
  ], state, render);

  document.getElementById("reset").addEventListener("click", function () {
    state.tx = 0.7; state.ty = 0.6; state.l1 = 1; state.l2 = 1;
    state.showAux = true; state.showAlt = true;
    document.getElementById("showAux").checked = true;
    document.getElementById("showAlt").checked = true;
    pan.x = 0; pan.y = 0;
    ranges.refresh();
    scene.reset();
    layout();
    render();
  });

  viewport.addEventListener("pointerdown", function (event) {
    if (pan.id !== null) return;
    pan.id = event.pointerId; pan.lx = event.clientX; pan.ly = event.clientY; pan.dragging = true;
  });
  viewport.addEventListener("pointermove", function (event) {
    if (!pan.dragging || event.pointerId !== pan.id) return;
    pan.x += event.clientX - pan.lx;
    pan.y += event.clientY - pan.ly;
    pan.lx = event.clientX; pan.ly = event.clientY;
    render();
  });
  function endPan(event) {
    if (event && pan.id !== null && event.pointerId !== pan.id) return;
    pan.dragging = false; pan.id = null;
  }
  viewport.addEventListener("pointerup", endPan);
  viewport.addEventListener("pointercancel", endPan);
  viewport.addEventListener("lostpointercapture", endPan);
  viewport.addEventListener("dblclick", function () { pan.x = 0; pan.y = 0; render(); });
  window.addEventListener("resize", function () { layout(); render(); });

  /* --------------------------------------------------------- 数值自检 */
  (function selfTest() {
    var EPS = 1e-9;
    var L1 = 1, L2 = 1;

    /* 自检1：默认目标 (0.9, 0.5)。由 (β, ψ) 构造的两组 θ1 都必须把末端送到目标点 */
    var G = geom(L1, L2, 0.9, 0.5);
    if (!G.valid) throw new Error("(0.9,0.5) 应在可达范围内");
    G.branch.forEach(function (b, i) {
      var K = fk(L1, L2, b.t1, b.t2);
      var err = Math.hypot(K.tip[0] - 0.9, K.tip[1] - 0.5);
      if (!(err < EPS)) throw new Error("第 " + (i + 1) + " 组解未命中目标点，误差 " + err);
    });
    /* 式(4-33)：θ2 < 0 用 β+ψ，θ2 > 0 用 β−ψ */
    if (!(G.branch[0].t2 < 0 && G.branch[0].t1 === G.beta + G.psi)) {
      throw new Error("θ2 < 0 时应取 θ1 = β + ψ");
    }
    if (!(G.branch[1].t2 > 0 && G.branch[1].t1 === G.beta - G.psi)) {
      throw new Error("θ2 > 0 时应取 θ1 = β − ψ");
    }
    /* ψ 取值必须在 0~180° */
    if (!(G.psi >= 0 && G.psi <= Math.PI)) throw new Error("ψ 必须落在 0~180° 内");
    /* 式(4-29) 与式(4-12) 必须等价：−cos(180+θ2) = cos θ2 */
    if (Math.abs(-Math.cos(Math.PI + G.branch[0].t2) - Math.cos(G.branch[0].t2)) > EPS) {
      throw new Error("式(4-29) 的 cos(180+θ2) 与式(4-12) 的 cosθ2 不等价");
    }
    /* 式(4-29) 解出的 c2 必须等于式(4-30) */
    var c2from29 = -(G.r * G.r - L1 * L1 - L2 * L2) / (2 * L1 * L2);
    if (Math.abs(c2from29 - G.c2) > EPS) throw new Error("式(4-29)/(4-30) 的 c2 不一致");
    /* 余弦定理：r² = l1²+l2²−2l1l2cos(180+θ2) */
    var lhs = G.r * G.r;
    var rhs = L1 * L1 + L2 * L2 - 2 * L1 * L2 * Math.cos(Math.PI + G.branch[0].t2);
    if (Math.abs(lhs - rhs) > 1e-9) throw new Error("式(4-29) 余弦定理自检失败");

    /* 自检2：r > l1+l2 时 c2 越界，必须判无解（并 clamp 到 ±1 供读数显示） */
    var Gfar = geom(L1, L2, 1.6, 1.6);
    if (Gfar.valid) throw new Error("r = 2.263 > 2 应判无解");
    if (!(Gfar.c2raw > 1)) throw new Error("越界时 c2 必须大于 1");
    if (!(Gfar.r > L1 + L2)) throw new Error("越界判据应为 r > l1+l2");
    /* 边界 r = l1+l2：有解且两组解重合（θ2 = 0） */
    var Gedge = geom(L1, L2, 2, 0);
    if (!Gedge.valid) throw new Error("r = l1+l2 应有解");
    if (Math.abs(Gedge.c2 - 1) > EPS) throw new Error("边界上 c2 = 1");
    if (Math.abs(Gedge.branch[0].t2) > EPS || Math.abs(Gedge.branch[1].t2) > EPS) {
      throw new Error("边界上 θ2 = 0，两组解重合");
    }
    if (Math.abs(Gedge.psi) > EPS) throw new Error("边界上 ψ = 0");

    /* 自检3：l1 ≠ l2 的圆环内部扫掠——两组解的末端误差恒 < 1e-9，ψ ∈ [0,180°] */
    var k;
    for (k = 0; k < 240; k += 1) {
      var ang = k * 0.1309;
      var rad = 0.3 + 1.1 * ((k % 19) / 18);
      var x = rad * Math.cos(ang), y = rad * Math.sin(ang);
      var g = geom(0.9, 1.1, x, y);
      if (!g.valid) continue;
      if (!(g.psi >= 0 && g.psi <= Math.PI)) throw new Error("扫掠中 ψ 越界 @" + k);
      var A = fk(0.9, 1.1, g.branch[0].t1, g.branch[0].t2);
      var B = fk(0.9, 1.1, g.branch[1].t1, g.branch[1].t2);
      if (Math.hypot(A.tip[0] - x, A.tip[1] - y) > 1e-9) throw new Error("扫掠实线解未命中 @" + k);
      if (Math.hypot(B.tip[0] - x, B.tip[1] - y) > 1e-9) throw new Error("扫掠虚线解未命中 @" + k);
      /* 式(4-32) 的 cosψ 与三角形几何一致：|E−O| = l1、|E−T| = l2 由构造保证 */
      if (Math.abs(Math.hypot(A.tip[0] - x, A.tip[1] - y)) > 1e-9) throw new Error("命中自检失败 @" + k);
    }

    /* 自检4：θ2 = 180°（两连杆折返，r = |l1−l2|）时三角形退化，内角为 0 */
    var Gfold = geom(1, 0.4, 0.6, 0);
    if (!Gfold.valid) throw new Error("r = |l1−l2| = 0.6 应有解");
    if (Math.abs(Math.abs(degNormLocal(Gfold.branch[0].t2)) - 180) > 1e-6) {
      throw new Error("r = |l1−l2| 时 θ2 应为 ±180°");
    }
    if (Math.abs(Math.PI - Math.abs(Gfold.branch[0].t2)) > 1e-9) {
      throw new Error("θ2 = ±180° 时三角形内角应为 0");
    }
    function degNormLocal(rad) {
      var d = rad / FK.DEG % 360;
      if (d > 180) d -= 360;
      if (d <= -180) d += 360;
      return d;
    }
  }());

  layout();
  render();
}());
"""

FIGURE = {
    "id": "figure-4-8",
    "title": "图4-8 平面三连杆的平面几何关系 · 人机交互演示",
    "css": COMMON_CSS + EXTRA_CSS,
    "body": BODY,
    "script": SCRIPT,
}
