"""图4-1 连杆长度为 l1 和 l2 的两连杆操作臂（克雷格《机器人学导论（第3版）》4.2 节）。

教材依据：
- 4.2 节解的存在性："现在讨论图4-1所示两连杆操作臂的工作空间。如果 l1 = l2，
  则可达工作空间是半径为 2l1 的圆，而灵巧工作空间仅是单独的一点，即原点。
  如果 l1 ≠ l2，则不存在灵巧工作空间，而可达工作空间为一外径为 l1+l2、
  内径为 |l1−l2| 的圆环。在可达工作空间内部，末端执行器有两种可能的方位，
  在工作空间的边界上只有一种可能的方位。"
- 同节："这里讨论的两连杆操作臂的工作空间是假设所有关节能够旋转 360 度……
  例如，对于图4-1所示的操作臂，θ1 的运动范围为 360 度，
  但只有当 0 ≤ θ2 ≤ 180° 时，可达工作空间才具有相同的范围，
  而此时仅有一个方位可以达到工作空间的每一个点。"
- 运动学（平面两连杆，θ1 为连杆1 相对 X 轴转角，θ2 为连杆2 相对连杆1 的转角）：
    x = l1·cosθ1 + l2·cos(θ1+θ2)
    y = l1·sinθ1 + l2·sin(θ1+θ2)
  于是 |OT| = √(l1² + l2² + 2·l1·l2·cosθ2)，θ2 = 0° 时 |OT| = l1+l2（外边界），
  θ2 = ±180° 时 |OT| = |l1−l2|（内边界）——脚本内以此做数值自检。

交互要点：把 l2 调小（例如 l1=1、l2=0.3）时圆环中央出现"空洞"，
这是本节最核心的几何结论（可达空间不是实心圆盘）。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 620" role="img"
     aria-label="两连杆平面操作臂及其可达工作空间圆环">
  <defs>
    <marker id="mDim" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="mDim2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.4" markerHeight="5.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#b45309"></path>
    </marker>
  </defs>
  <g id="ring"></g>
  <g id="sector"></g>
  <g id="trail"></g>
  <g id="dims"></g>
  <g id="labels"></g>
  <g id="arm"></g>
</svg>

<section class="panel" aria-label="图4-1 控制面板">
  <div class="panel-head">
    <div>
      <h1>图4-1 两连杆操作臂的工作空间</h1>
      <p class="subtitle">可达工作空间＝外径 l₁+l₂、内径 |l₁−l₂| 的圆环；
        圆环内部有两种方位，边界上只有一种方位（θ₂ = 0° 或 180°）。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>
  <div class="control">
    <div class="control-head"><label for="l1">连杆长度 l₁</label><output id="l1Value">1.00</output></div>
    <input id="l1" type="range" min="0.2" max="1.2" step="0.05" value="1">
  </div>
  <div class="control">
    <div class="control-head"><label for="l2">连杆长度 l₂</label><output id="l2Value">1.00</output></div>
    <input id="l2" type="range" min="0.2" max="1.2" step="0.05" value="1">
  </div>
  <div class="control">
    <div class="control-head"><label for="t1">关节角 θ₁</label><output id="t1Value">0.0°</output></div>
    <input id="t1" type="range" min="-180" max="180" step="1" value="0">
  </div>
  <div class="control">
    <div class="control-head"><label for="t2">关节角 θ₂</label><output id="t2Value">0.0°</output></div>
    <input id="t2" type="range" min="-180" max="180" step="1" value="0">
  </div>
  <div class="options">
    <label><input id="showRing" type="checkbox" checked>显示可达圆环</label>
    <label><input id="showSector" type="checkbox">显示关节限位扇形</label>
    <label><input id="showTrail" type="checkbox" checked>显示末端轨迹</label>
    <label><input id="showAlt" type="checkbox" checked>显示另一组解</label>
    <label><input id="sweep" type="checkbox">自动扫掠 θ₁/θ₂</label>
  </div>
  <div class="legend">
    <span><i style="background:#475569"></i>连杆（实心）</span>
    <span><i style="background:#2563eb"></i>可达圆环边界（虚线）</span>
    <span><i style="background:#94a3b8"></i>另一组解（θ₂ 变号）</span>
    <span><i style="background:#c26a10"></i>末端轨迹</span>
    <span>末端位置 T（橙点）</span>
  </div>
</section>

<div class="hint">拖动平移 · 滚轮缩放 · 双击复位</div>
<div class="readout">
  <div class="row">末端位置 <strong>T</strong> = ( <span id="tx">2.000</span>, <span id="ty">0.000</span> ) <span class="small">（单位：l 的同一长度单位）</span></div>
  <div class="row small">|OT| = <span id="tr">2.000</span> · 外径 l₁+l₂ = <span id="rout">2.000</span> · 内径 |l₁−l₂| = <span id="rin">0.000</span></div>
  <div class="row small" id="condRow">可达条件：…</div>
  <div class="row small" id="noteRow">…</div>
</div>
"""

SCRIPT = r"""
(function () {
  var viewport = document.getElementById("viewport");
  var L = {
    ring: document.getElementById("ring"),
    sector: document.getElementById("sector"),
    trail: document.getElementById("trail"),
    dims: document.getElementById("dims"),
    labels: document.getElementById("labels"),
    arm: document.getElementById("arm")
  };

  var BASE_SCALE = 88;
  var scene = new FK.Scene({ svg: viewport, origin: { x: 560, y: 330 }, scale: BASE_SCALE });
  var state = {
    l1: 1, l2: 1, t1: 0, t2: 0,
    showRing: true, showSector: false, showTrail: true, showAlt: true, sweep: false
  };
  var pan = { x: 0, y: 0, dragging: false, id: null, lx: 0, ly: 0 };
  var trail = [];
  var sweepFrame = 0, sweepPhase = -180, sweepTurn = 1;

  /* 纯平面投影：世界 (x, y) -> 屏幕，拖动平移、滚轮缩放由 FK.Scene 负责 */
  scene.project = function (v) {
    var s = scene.state.scale;
    return {
      x: this.origin.x + pan.x + v[0] * s,
      y: this.origin.y + pan.y - v[1] * s,
      depth: v[2] || 0
    };
  };

  var COL = { link: "#475569", link2: "#64748b", joint: "#1e293b", ring: "#2563eb", alt: "#94a3b8", trail: "#c26a10", tip: "#c26a10", sector: "#2563eb" };

  /* ------------------------------------------------------------- 运动学 */
  function fk(l1, l2, t1, t2) {
    var elbow = [l1 * Math.cos(t1), l1 * Math.sin(t1)];
    var tip = [elbow[0] + l2 * Math.cos(t1 + t2), elbow[1] + l2 * Math.sin(t1 + t2)];
    return { elbow: elbow, tip: tip };
  }
  function mirrorElbow(elbow, tip) {
    var r = Math.sqrt(tip[0] * tip[0] + tip[1] * tip[1]);
    if (r < 1e-9) return null;
    var ux = tip[0] / r, uy = tip[1] / r;
    var d = elbow[0] * ux + elbow[1] * uy;
    return [2 * d * ux - elbow[0], 2 * d * uy - elbow[1]];
  }

  /* -------------------------------------------------------------- 绘图 */
  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    return scene.el("line", Object.assign({ x1: A.x, y1: A.y, x2: B.x, y2: B.y }, attrs || {}), parent);
  }
  function tag(v, str, attrs, dx, dy, parent) {
    var p = scene.project(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0),
      "font-size": 15, "font-weight": 700, class: "fk-axis-label"
    }, attrs || {}), parent);
    node.textContent = str;
    return node;
  }
  function circlePts(r, n) {
    var pts = [], i;
    for (i = 0; i <= n; i += 1) {
      var a = i * 2 * Math.PI / n;
      pts.push([r * Math.cos(a), r * Math.sin(a), 0]);
    }
    return pts;
  }
  function sp(r, ang) {
    var p = scene.project([r * Math.cos(ang), r * Math.sin(ang), 0]);
    return p.x.toFixed(1) + " " + p.y.toFixed(1);
  }
  function ringPath(rout, rin) {
    var n = 120, i, d;
    if (rout <= 1e-6) return "";
    d = "M " + sp(rout, 0);
    for (i = 1; i <= n; i += 1) d += " L " + sp(rout, i * 2 * Math.PI / n);
    d += " Z";
    if (rin > 1e-6) {
      d += " M " + sp(rin, 0);
      for (i = 1; i <= n; i += 1) d += " L " + sp(rin, i * 2 * Math.PI / n);
      d += " Z";
    }
    return d;
  }
  function sectorPath(rout, rin, a0, a1) {
    var n = 60, i, ang, d = "";
    if (rout <= 1e-6) return "";
    for (i = 0; i <= n; i += 1) {
      ang = a0 + (a1 - a0) * i / n;
      d += (i === 0 ? "M " : " L ") + sp(rout, ang);
    }
    for (i = n; i >= 0; i -= 1) {
      ang = a0 + (a1 - a0) * i / n;
      d += " L " + sp(rin, ang);
    }
    return d + " Z";
  }
  function dimLine(a, b, offX, offY, text, color, marker) {
    var A = scene.project(a), B = scene.project(b);
    var ax = A.x + offX, ay = A.y + offY, bx = B.x + offX, by = B.y + offY;
    scene.el("line", {
      x1: ax, y1: ay, x2: bx, y2: by, stroke: color, "stroke-width": 1.6,
      "marker-start": "url(#" + marker + ")", "marker-end": "url(#" + marker + ")"
    }, L.dims);
    var t = scene.el("text", {
      x: (ax + bx) / 2, y: (ay + by) / 2 - 6, "text-anchor": "middle",
      fill: color, "font-size": 14, "font-weight": 700, class: "fk-axis-label"
    }, L.dims);
    t.textContent = text;
  }

  function drawBase() {
    seg([-0.30, 0, 0], [0.30, 0, 0], { stroke: COL.joint, "stroke-width": 3.4 }, L.arm);
    var i;
    for (i = -3; i <= 3; i += 1) {
      seg([i * 0.09 - 0.14, 0, 0], [i * 0.09 + 0.02, -0.13, 0], { stroke: COL.joint, "stroke-width": 1.6 }, L.arm);
    }
  }

  function drawArm(t1, t2, l1, l2) {
    var K = fk(l1, l2, t1, t2);
    var e = K.elbow, tip = K.tip;
    // 另一组解（对 OT 连线镜像）
    var alt = state.showAlt ? mirrorElbow(e, tip) : null;
    if (alt && Math.hypot(alt[0] - e[0], alt[1] - e[1]) > 0.02) {
      seg([0, 0, 0], [alt[0], alt[1], 0], { stroke: COL.alt, "stroke-width": 7, "stroke-dasharray": "9 7", "stroke-linecap": "round" }, L.arm);
      seg([alt[0], alt[1], 0], tip, { stroke: COL.alt, "stroke-width": 7, "stroke-dasharray": "9 7", "stroke-linecap": "round" }, L.arm);
      // 标签朝远离末端 T 的方向让开，避免与 T 标签重叠
      var ax = alt[0] - tip[0], ay = alt[1] - tip[1];
      var an = Math.hypot(ax, ay) || 1;
      tag(alt, "另一组解（θ₂ 变号）", { fill: "#64748b", "font-size": 13, "text-anchor": ax / an > 0 ? "start" : "end" },
        (ax / an) * 26, -(ay / an) * 26 + 10, L.arm);
    }
    drawBase();
    seg([0, 0, 0], e, { stroke: COL.link, "stroke-width": 12, "stroke-linecap": "round" }, L.arm);
    seg(e, tip, { stroke: COL.link2, "stroke-width": 10, "stroke-linecap": "round" }, L.arm);
    // 关节与末端
    var o = scene.project([0, 0, 0]);
    scene.el("circle", { cx: o.x, cy: o.y, r: 8, fill: "#fff", stroke: COL.joint, "stroke-width": 3 }, L.arm);
    var ep = scene.project(e);
    scene.el("circle", { cx: ep.x, cy: ep.y, r: 7, fill: "#fff", stroke: COL.joint, "stroke-width": 3 }, L.arm);
    var tp = scene.project(tip);
    scene.el("circle", { cx: tp.x, cy: tp.y, r: 6.6, fill: COL.tip, stroke: "#fff", "stroke-width": 2.2 }, L.arm);
    tag(tip, "T", { fill: "#8a4a08", "font-size": 16 }, 12, -12, L.arm);
    tag([l1 * 0.55 * Math.cos(t1), l1 * 0.55 * Math.sin(t1), 0], "l₁", { fill: "#334155", "font-size": 15 }, -18, -8, L.arm);
    var mx = e[0] + 0.5 * l2 * Math.cos(t1 + t2), my = e[1] + 0.5 * l2 * Math.sin(t1 + t2);
    tag([mx, my, 0], "l₂", { fill: "#334155", "font-size": 15 }, 12, -8, L.arm);
    // 角弧
    var r1 = Math.min(0.34, 0.42 * l1);
    var pts = [], i, a;
    for (i = 0; i <= 40; i += 1) {
      a = t1 * i / 40;
      pts.push([r1 * Math.cos(a), r1 * Math.sin(a), 0]);
    }
    if (Math.abs(t1) > 0.02) {
      scene.polyline(pts, { stroke: "#0e7490", class: "fk-arc" }, L.arm);
      tag([r1 * 1.35 * Math.cos(t1 * 0.5), r1 * 1.35 * Math.sin(t1 * 0.5), 0], "θ₁", { fill: "#0e7490", "font-size": 15 }, 0, 5, L.arm);
    }
    var r2 = Math.min(0.30, 0.42 * l2);
    var base = t1;
    var p2 = [], b;
    for (i = 0; i <= 40; i += 1) {
      b = base + t2 * i / 40;
      p2.push([e[0] + r2 * Math.cos(b), e[1] + r2 * Math.sin(b), 0]);
    }
    if (Math.abs(t2) > 0.02) {
      scene.polyline(p2, { stroke: "#7c3aed", class: "fk-arc" }, L.arm);
      tag([e[0] + r2 * 1.5 * Math.cos(base + t2 * 0.5), e[1] + r2 * 1.5 * Math.sin(base + t2 * 0.5), 0], "θ₂", { fill: "#7c3aed", "font-size": 15 }, 0, 5, L.arm);
    }
    return tip;
  }

  /* ------------------------------------------------------------------ 渲染 */
  function render() {
    var k;
    for (k in L) { if (Object.prototype.hasOwnProperty.call(L, k)) L[k].replaceChildren(); }

    var l1 = state.l1, l2 = state.l2;
    var t1 = state.t1 * FK.DEG, t2 = state.t2 * FK.DEG;
    var rout = l1 + l2, rin = Math.abs(l1 - l2);

    if (state.showRing && rout > 1e-6) {
      scene.el("path", {
        d: ringPath(rout, rin), "fill-rule": "evenodd",
        fill: "rgba(37, 99, 235, 0.10)", stroke: "none"
      }, L.ring);
      scene.polyline(circlePts(rout, 120), { stroke: COL.ring, "stroke-width": 2.2, "stroke-dasharray": "9 7" }, L.ring);
      if (rin > 1e-6) {
        scene.polyline(circlePts(rin, 120), { stroke: COL.ring, "stroke-width": 2.2, "stroke-dasharray": "9 7" }, L.ring);
      }
    }

    if (state.showSector && rout > 1e-6) {
      var a0 = -Math.PI / 2, a1 = Math.PI / 2;
      scene.el("path", {
        d: sectorPath(rout, rin, a0, a1),
        fill: "rgba(14, 116, 144, 0.14)", stroke: "none"
      }, L.sector);
      seg([0, 0, 0], [rout * Math.cos(a0), rout * Math.sin(a0), 0], { stroke: "#0e7490", "stroke-width": 1.8, "stroke-dasharray": "7 6" }, L.sector);
      seg([0, 0, 0], [rout * Math.cos(a1), rout * Math.sin(a1), 0], { stroke: "#0e7490", "stroke-width": 1.8, "stroke-dasharray": "7 6" }, L.sector);
      var rm = rin + (rout - rin) * 0.62;
      tag([rm * Math.cos(0.62), rm * Math.sin(0.62), 0], "θ₁ 限位 ±90° 示例扇形", { fill: "#0e7490", "font-size": 13.5 }, 0, -10, L.sector);
    }

    if (state.showTrail && trail.length > 1) {
      scene.polyline(trail, { stroke: COL.trail, "stroke-width": 3, opacity: 0.85 }, L.trail);
    }
    pushTrail(fk(l1, l2, t1, t2).tip);

    // 半径尺寸线（沿 218°/258° 方向，避开坐标轴与读数卡）
    if (rout > 1e-6) {
      var D = 218 * FK.DEG;
      var eOut = [rout * Math.cos(D), rout * Math.sin(D), 0];
      scene.el("line", {
        x1: scene.project([0, 0, 0]).x, y1: scene.project([0, 0, 0]).y,
        x2: scene.project(eOut).x, y2: scene.project(eOut).y,
        stroke: "#2563eb", "stroke-width": 1.5, "stroke-dasharray": "6 5"
      }, L.dims);
      dimLine([0, 0, 0], eOut, 0, -18, "外径 l₁+l₂ = " + FK.format(rout, 3), "#2563eb", "mDim");
      if (rin > 1e-6) {
        var D2 = 258 * FK.DEG;
        var eIn = [rin * Math.cos(D2), rin * Math.sin(D2), 0];
        dimLine([0, 0, 0], eIn, 14, 10, "内径 |l₁−l₂| = " + FK.format(rin, 3), "#b45309", "mDim2");
      }
    }

    var tip = drawArm(t1, t2, l1, l2);

    /* ---------------------------------------------------------------- 读数 */
    var r = Math.sqrt(tip[0] * tip[0] + tip[1] * tip[1]);
    document.getElementById("tx").textContent = FK.format(tip[0], 3);
    document.getElementById("ty").textContent = FK.format(tip[1], 3);
    document.getElementById("tr").textContent = FK.format(r, 3);
    document.getElementById("rout").textContent = FK.format(rout, 3);
    document.getElementById("rin").textContent = FK.format(rin, 3);

    var c2 = Math.cos(t2);
    var cond = document.getElementById("condRow");
    var onOuter = Math.abs(c2 - 1) < 1e-9;
    var onInner = rin > 1e-6 ? Math.abs(c2 + 1) < 1e-9 : (r < 1e-9);
    if (l1 === l2 && Math.abs(t2) === 180) onInner = true;
    var analytic = Math.sqrt(l1 * l1 + l2 * l2 + 2 * l1 * l2 * c2);
    if (onOuter) {
      cond.className = "row small ok";
      cond.textContent = "θ₂ = 0° → 位于外边界 |OT| = l₁+l₂ = " + FK.format(rout, 3) + "：只有一种方位（等效单连杆）";
    } else if (onInner) {
      cond.className = "row small warn";
      cond.textContent = "θ₂ = ±180° → 位于内边界 |OT| = |l₁−l₂| = " + FK.format(rin, 3) + "：只有一种方位（两连杆重叠）";
    } else {
      cond.className = "row small";
      cond.textContent = "θ₂ = " + FK.deg(state.t2, 1) + " → 圆环内部（|l₁−l₂| < |OT| < l₁+l₂）：有两种方位；"
        + "|OT| 解析值 √(l₁²+l₂²+2l₁l₂cosθ₂) = " + FK.format(analytic, 3);
    }

    var note = document.getElementById("noteRow");
    if (Math.abs(l1 - l2) < 1e-9) {
      note.textContent = "l₁ = l₂：" + "可达工作空间是半径 2l₁ = " + FK.format(rout, 3) + " 的实心圆，灵巧工作空间仅是原点这一点";
    } else {
      note.textContent = "l₁ ≠ l₂：" + "可达工作空间是圆环（中央为空洞，半径 < |l₁−l₂| = " + FK.format(rin, 3)
        + " 的点不可达），不存在灵巧工作空间";
    }
  }

  /* --------------------------------------------------------------- 轨迹 */
  function pushTrail(tip) {
    if (!state.showTrail) return;
    var last = trail[trail.length - 1];
    if (!last || Math.hypot(tip[0] - last[0], tip[1] - last[1]) > 0.004) {
      trail.push([tip[0], tip[1], 0]);
      if (trail.length > 2000) trail.shift();
    }
  }

  /* ------------------------------------------------------------ 自动扫掠 */
  function sweepTick() {
    sweepFrame = 0;
    if (!state.sweep) return;
    state.t2 += 2.4 * sweepTurn;
    if (state.t2 >= 180) { state.t2 = 180; sweepTurn = -1; }
    if (state.t2 <= -180) { state.t2 = -180; sweepTurn = 1; }
    state.t1 += 0.45;
    if (state.t1 > 180) state.t1 -= 360;
    var i1 = document.getElementById("t1"), i2 = document.getElementById("t2");
    i1.value = state.t1; i2.value = state.t2;
    document.getElementById("t1Value").textContent = FK.deg(state.t1, 1);
    document.getElementById("t2Value").textContent = FK.deg(state.t2, 1);
    pushTrail(fk(state.l1, state.l2, state.t1 * FK.DEG, state.t2 * FK.DEG).tip);
    render();
    sweepFrame = requestAnimationFrame(sweepTick);
  }

  /* ------------------------------------------------------------------ 布局 */
  function layout() {
    var w = viewport.clientWidth || window.innerWidth;
    var h = viewport.clientHeight || window.innerHeight;
    if (w / h < 1.05) {
      viewport.setAttribute("viewBox", "0 0 420 780");
      viewport.setAttribute("preserveAspectRatio", "xMidYMin meet");
      scene.baseOrigin = { x: 210, y: 300 };
      scene.state.scale = 62;
      scene.defaults.scale = 62;
    } else {
      viewport.setAttribute("viewBox", "0 0 1000 620");
      viewport.setAttribute("preserveAspectRatio", "xMidYMid meet");
      scene.baseOrigin = { x: 505, y: 268 };
      scene.state.scale = BASE_SCALE;
      scene.defaults.scale = BASE_SCALE;
    }
    scene.origin.x = scene.baseOrigin.x;
    scene.origin.y = scene.baseOrigin.y;
  }

  scene.setRenderer(render);

  var ranges = FK.bindRanges([
    { id: "l1", key: "l1", value: 1, format: function (v) { return FK.format(v, 2); } },
    { id: "l2", key: "l2", value: 1, format: function (v) { return FK.format(v, 2); } },
    { id: "t1", key: "t1", value: 0, format: function (v) { return FK.deg(v, 1); } },
    { id: "t2", key: "t2", value: 0, format: function (v) { return FK.deg(v, 1); } }
  ], state, function () { render(); });

  // 连杆长度改变时旧轨迹失效，清空
  document.getElementById("l1").addEventListener("input", function () { trail = []; });
  document.getElementById("l2").addEventListener("input", function () { trail = []; });

  FK.bindToggles([
    { id: "showRing", key: "showRing" },
    { id: "showSector", key: "showSector" },
    { id: "showTrail", key: "showTrail" },
    { id: "showAlt", key: "showAlt" },
    {
      id: "sweep", key: "sweep", onChange: function (v) {
        if (v && !sweepFrame) sweepFrame = requestAnimationFrame(sweepTick);
      }
    }
  ], state, function () { render(); });

  document.getElementById("reset").addEventListener("click", function () {
    state.l1 = 1; state.l2 = 1; state.t1 = 0; state.t2 = 0;
    state.showRing = true; state.showSector = false; state.showTrail = true; state.showAlt = true; state.sweep = false;
    document.getElementById("showRing").checked = true;
    document.getElementById("showSector").checked = false;
    document.getElementById("showTrail").checked = true;
    document.getElementById("showAlt").checked = true;
    document.getElementById("sweep").checked = false;
    trail = [];
    pan.x = 0; pan.y = 0;
    ranges.refresh();
    scene.reset();
    layout();
    render();
  });

  /* 拖动平移（平面图不使用三维旋转） */
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

  /* --------------------------------------------------------------- 自检 */
  (function selfTest() {
    function close(a, b, eps) { return Math.abs(a - b) < (eps === undefined ? 1e-9 : eps); }
    var L1 = 1, L2 = 0.3;

    // 1) θ₂ = 0° → |OT| = l₁+l₂（外边界）
    var k1 = fk(L1, L2, 0.7, 0);
    if (!close(FK.Vec.len([k1.tip[0], k1.tip[1], 0]), L1 + L2)) {
      throw new Error("θ₂=0 时 |OT| 应为 l₁+l₂ = 1.3");
    }
    // 2) θ₂ = 180° → |OT| = |l₁−l₂|（内边界）
    var k2 = fk(L1, L2, -1.2, Math.PI);
    if (!close(FK.Vec.len([k2.tip[0], k2.tip[1], 0]), Math.abs(L1 - L2))) {
      throw new Error("θ₂=180° 时 |OT| 应为 |l₁−l₂| = 0.7");
    }
    // 3) 扫掠极值即圆环内外径
    var mn = Infinity, mx = -Infinity, i, r;
    for (i = 0; i <= 1440; i += 1) {
      var kk = fk(L1, L2, 0.3, i * Math.PI / 720);
      r = FK.Vec.len([kk.tip[0], kk.tip[1], 0]);
      if (r < mn) mn = r;
      if (r > mx) mx = r;
    }
    if (!close(mx, L1 + L2, 1e-6) || !close(mn, Math.abs(L1 - L2), 1e-6)) {
      throw new Error("扫掠极值应为 [0.7, 1.3]，实得 [" + mn + ", " + mx + "]");
    }
    // 4) 解析式 √(l₁²+l₂²+2l₁l₂cosθ₂) 与运动学一致
    for (i = 0; i <= 36; i += 1) {
      var th = i * 10 * FK.DEG;
      var kk2 = fk(L1, L2, 0.9, th);
      var rr = FK.Vec.len([kk2.tip[0], kk2.tip[1], 0]);
      var an = Math.sqrt(L1 * L1 + L2 * L2 + 2 * L1 * L2 * Math.cos(th));
      if (!close(rr, an, 1e-9)) throw new Error("|OT| 解析式自检失败 @" + i);
    }
    // 5) l₁ = l₂ → 内径为 0（原点可达）
    var k3 = fk(1, 1, 0, Math.PI);
    if (!close(FK.Vec.len([k3.tip[0], k3.tip[1], 0]), 0, 1e-12)) {
      throw new Error("l₁=l₂ 且 θ₂=180° 时末端应回到原点");
    }
    // 6) 边界上只有一种方位：θ₂=0/180° 时镜像解与原解重合
    var kb = fk(L1, L2, 0.4, 0);
    var mb = mirrorElbow(kb.elbow, kb.tip);
    if (!close(mb[0], kb.elbow[0], 1e-9) || !close(mb[1], kb.elbow[1], 1e-9)) {
      throw new Error("θ₂=0（外边界）镜像解应重合");
    }
    var kc = fk(L1, L2, 0.4, Math.PI);
    var mc = mirrorElbow(kc.elbow, kc.tip);
    if (!close(mc[0], kc.elbow[0], 1e-9) || !close(mc[1], kc.elbow[1], 1e-9)) {
      throw new Error("θ₂=180°（内边界）镜像解应重合");
    }
    // 7) 圆环内部两种方位：θ₂=90° 时镜像解与原解不同
    var kd = fk(L1, L2, 0.4, Math.PI / 2);
    var md = mirrorElbow(kd.elbow, kd.tip);
    if (Math.hypot(md[0] - kd.elbow[0], md[1] - kd.elbow[1]) < 1e-6) {
      throw new Error("圆环内部应存在两个不同方位");
    }
  }());

  layout();
  render();
}());
"""

FIGURE = {
    "id": "figure-4-1",
    "title": "图4-1 两连杆操作臂的工作空间 · 人机交互演示",
    "css": COMMON_CSS + """
.readout .row { white-space: normal; }
.readout .warn { color: #b45309; font-weight: 700; }
.readout .ok { color: #15803d; font-weight: 700; }
@media (max-width: 720px) {
  .readout { padding: 7px 10px; font-size: 12px; }
  .readout .small { font-size: 10.5px; }
}
""",
    "body": BODY,
    "script": SCRIPT,
}
