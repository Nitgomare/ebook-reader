"""图3-17 棱柱联轴器（移动/平动关节）连杆 D-H 坐标系建立示意图
（《机器人技术基础（第三版）》3.3.1 二 2.(2) 与 3.3.2 一）。

教材依据（正文原话）：
- 3.3.1 2.(2)：“对于图3.17所示的棱柱联轴器，距离 d_i 成为联轴器(关节)变量，而联轴器的方向即为此
  联轴器移动的方向。该轴方向是规定的，但不同于转动关节的情况是该轴空间位置没有规定。对于联轴器
  来说，其长度 a_i 没有意义，令其为零。联轴器的坐标系原点与下一个规定的连杆原点重合。棱柱联轴器
  的 Z 轴在关节 i+1 的轴线上。X_i 轴平行或反向平行于棱柱联轴器矢量与 Z_i 矢量的叉积。当 d_i = 0 时，
  定义该联轴器的位置为零。”
- 3.3.1 2.(1)：关节变量“对于转动关节，θ_i 是关节变量，其他三个参数固定不变；对于移动关节，
  d_i 是关节变量，其他三个参数固定不变。”
- 式(3.20) 连杆变换矩阵（本教材标准 D-H 记法）：
      A_i = Rot(Z, θ_i)·Trans(a_i, 0, d_i)·Rot(X, α_i)
          = [[cθ, −sθ·cα,  sθ·sα, a·cθ],
             [sθ,  cθ·cα, −cθ·sα, a·sθ],
             [ 0,     sα,     cα,    d ],
             [ 0,      0,      0,    1 ]]
- 式(3.21) 联轴器（平动关节）的齐次变换矩阵 —— 令 a_i = 0 后式(3.20)退化为
      A_i = [[cθ, −sθ·cα,  sθ·sα,  0],
             [sθ,  cθ·cα, −cθ·sα,  0],
             [ 0,     sα,     cα,  d ],
             [ 0,      0,      0,  1]]
  教材该式第 3 行第 3 列在纸上排成 0（OCR 疑为排版误差），令其正交只能取 cα；
  本图按式(3.20) 代入 a_i = 0 计算，并在自检中与式(3.21) 的书面形式逐元素比对。

记法约定：本教材用**标准（standard / 经典）D-H**，但下标比克雷格书早一位 ——
教材把“关节轴 Z_{i−1} 与 Z_i 之间的连杆长度、扭角”写成 a_i、α_i
（克雷格书同几何量写作 a_{i−1}、α_{i−1}）。本图的 a_i = 0、d_i、α_i 一律按教材下标书写，
读数区给出两套下标的对照，避免 i−1 与 i 混用。移动关节的关节变量是 d_i（转动关节才是 θ_i）。

本图表达的教学点：
1. 棱柱（移动）关节：a_i = 0 —— 于是 O_i 落在 Z_{i−1} 上，d_i = 0 时 O_i 与 O_{i−1} 重合
   （“联轴器的坐标系原点与下一个规定的连杆原点重合”）。
2. d_i 沿 Z_{i−1} 量取，d_i = 0 定义零位；d_i 改变时 {i} 只沿 Z 平移，X/Y 分量不变。
3. 两轴平行（α_i = 0）时 Z_i ∥ Z_{i−1}；这是“棱柱联轴器的 Z 轴在关节 i+1 的轴线上”的几何含义。

脚本内自检（selfTest）：见文件末尾 —— ①式(3.21) 与式(3.20)(a=0) 逐元素一致；
②a_i = 0 时原点恒在 Z_{i−1} 轴上（X/Y 分量为 0，与 d_i、α_i 无关）；
③d_i = 0 时两原点距离为 0；④d_i 变化时只沿 Z 平移、X/Y 分量不变且位移量 = |Δd_i|；
⑤原点距离 = |d_i|（a_i = 0）；⑥旋转部分正交。失败直接 throw。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS  # noqa: E402

CSS = COMMON_CSS + """
.fig-note {
  margin-top: 9px;
  padding: 6px 9px;
  border: 1px solid #cddffb;
  border-radius: 9px;
  color: var(--blue-dark);
  background: var(--blue-soft);
  font-size: 11.5px;
  line-height: 1.5;
}
.fig-note b { color: #1d4ed8; }
.fig-note .em { color: #b45309; font-weight: 700; }
.sec-title {
  margin: 12px 0 0;
  padding-top: 9px;
  border-top: 1px dashed var(--line);
  color: #45566f;
  font-size: 11.5px;
  font-weight: 700;
}
.mtable {
  border-collapse: collapse;
  margin: 3px 0 0 6px;
  border-left: 1.6px solid #8fa2bd;
  border-right: 1.6px solid #8fa2bd;
}
.mtable td {
  padding: 0 3px;
  font: 10.5px/1.35 ui-monospace, SFMono-Regular, Consolas, monospace;
  text-align: right;
  color: #55637a;
}
.mtable td.hi { color: #174ea6; font-weight: 700; }
.mtable td.zero { color: #b45309; font-weight: 700; }
.mtable td.dim { color: #9aa8bd; }
.mat-cap { margin: 2px 0 0; color: #5b6a80; font-size: 10.5px; line-height: 1.5; }
.mat-cap b { color: var(--blue-dark); }
/* 桌面端把读数卡钉在右上角：图形便可用满整幅高度，且不被读数卡压住 */
@media (min-width: 721px) {
  .readout {
    top: 14px;
    right: 14px;
    bottom: auto;
    max-width: min(420px, calc(100% - 380px));
    font-size: 13.5px;
    line-height: 1.55;
  }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 12px; }
}
@media (max-width: 720px) {
  .readout { font-size: 12px; max-width: calc(100% - 16px); padding: 7px 9px; }
  .readout .row { white-space: normal; }
  .readout .small { font-size: 10.5px; }
  .mtable td { padding: 0 3px; font-size: 10.5px; }
  .mat-caption { font-size: 10px; }
  .panel .sec-title { margin-top: 8px; padding-top: 6px; }
  .panel .control { margin-top: 7px; }
  [data-mobile-hide] { display: none !important; }
}
"""

BODY = """
<svg class="viewport" id="viewport" viewBox="0 0 1000 700" preserveAspectRatio="none" role="img"
     aria-label="棱柱联轴器连杆D-H坐标系建立示意图：移动关节的a_i为零，坐标系{i}的原点与下一个连杆原点重合，d_i沿Z量取，d_i等于零定义零位">
  <defs>
    <marker id="arX" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.2" markerHeight="5.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="arY" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.2" markerHeight="5.2" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
    </marker>
    <marker id="arZ" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" markerHeight="5.6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#12944f"></path>
    </marker>
    <marker id="arZp" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#174ea6"></path>
    </marker>
    <marker id="arZi" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"></path>
    </marker>
    <marker id="arD" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c26a10"></path>
    </marker>
    <marker id="arA" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d93025"></path>
    </marker>
    <marker id="arRef" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"></path>
    </marker>
  </defs>
  <g id="gGrid"></g>
  <g id="gLink"></g>
  <g id="gAxisZ"></g>
  <g id="gDim"></g>
  <g id="gFrame"></g>
  <g id="gGhost"></g>
</svg>

<section class="panel" aria-label="图3.17 控制面板">
  <div class="panel-head">
    <div>
      <h1>图3.17 棱柱联轴器的 D-H 坐标系</h1>
      <p class="subtitle">移动（棱柱）关节：关节变量是 d<sub>i</sub>，连杆长度 a<sub>i</sub> = 0 ——
        所以 {i} 的原点落在 Z<sub>i−1</sub> 上，d<sub>i</sub> = 0 时与下一个连杆原点 O<sub>i−1</sub> 重合。</p>
    </div>
    <button class="reset" id="reset" type="button">重置</button>
  </div>

  <div class="fig-note">
    <b>标准 D-H 记法</b>（教材 3.3.1）：式(3.20) A<sub>i</sub> = Rot(Z,θ<sub>i</sub>)·Trans(a<sub>i</sub>,0,d<sub>i</sub>)·Rot(X,α<sub>i</sub>)；
    棱柱关节令 <span class="em">a<sub>i</sub> = 0</span> 得式(3.21)。
    教材下标比克雷格书早一位：教材 a<sub>i</sub>、α<sub>i</sub> ＝ 克雷格 a<sub>i−1</sub>、α<sub>i−1</sub>，
    本图只出现教材下标 i。
    <br><b>与转动关节的差别</b>：转动关节 a<sub>i</sub> ≠ 0、关节变量是 θ<sub>i</sub>（原点不在 Z<sub>i−1</sub> 上）；
    移动关节 a<sub>i</sub> = 0、关节变量是 d<sub>i</sub>、原点与下一个连杆原点重合。
  </div>

  <div class="control">
    <div class="control-head"><label for="d">关节变量 d<sub>i</sub>（沿 Z<sub>i−1</sub> 的移动量）</label><output id="dValue">0.60</output></div>
    <input id="d" type="range" min="-1.5" max="1.5" step="0.01" value="0.6">
  </div>
  <div class="control">
    <div class="control-head"><label for="e">两轴间距（横向偏置，可选）</label><output id="eValue">0.00</output></div>
    <input id="e" type="range" min="-0.8" max="0.8" step="0.01" value="0">
  </div>
  <div class="control">
    <div class="control-head"><label for="alpha">扭角 α<sub>i</sub>（−90°~90°）</label><output id="alphaValue">0.0°</output></div>
    <input id="alpha" type="range" min="-90" max="90" step="1" value="0">
  </div>

  <div class="options">
    <label><input id="showZero" type="checkbox" checked>显示零位（d<sub>i</sub>=0）虚线</label>
    <label><input id="showFrames" type="checkbox" checked>显示坐标系</label>
    <label><input id="showGhost" type="checkbox">与转动关节对比（阴影）</label>
    <label><input id="auto" type="checkbox">自动旋转视角</label>
  </div>

  <p class="sec-title">式(3.21) 棱柱关节的 A<sub>i</sub>（a<sub>i</sub> = 0）</p>
  <table class="mtable"><tbody id="mxBody"></tbody></table>
  <p class="mat-cap">第 4 列位移 = <b>[0, 0, d<sub>i</sub>]<sup>T</sup></b> —— X/Y 分量恒为 0，
    正是 a<sub>i</sub> = 0 的直接后果；<b>d<sub>i</sub> = 0</b> 时位移为零向量 ⇒ {i} 与 {i−1} 原点重合。</p>

  <div class="legend">
    <span><i style="background:#174ea6"></i>Z<sub>i−1</sub>（关节轴 / 移动方向）</span>
    <span><i style="background:#7c3aed"></i>Z<sub>i</sub>（下一连杆坐标系）</span>
    <span><i class="dot" style="background:#c26a10"></i>d<sub>i</sub> 量取方向</span>
    <span><i style="background:#d93025"></i>转动关节的 a<sub>i</sub> ≠ 0</span>
    <span><i style="background:#94a3b8"></i>零位参考（O 重合处）</span>
  </div>
</section>

<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>

<div class="readout">
  <div class="row" id="statusRow"><strong>关节类型</strong>：<span id="status">移动（棱柱）关节 i</span></div>
  <div class="row">d<sub>i</sub> = <strong><span id="roD">0.600</span></strong>　α<sub>i</sub> = <strong><span id="roA">0.0°</span></strong>
    　两原点距离 |O<sub>i</sub> − O<sub>i−1</sub>| = <strong><span id="roR">0.600</span></strong></div>
  <div class="row small">O<sub>i</sub> 在 {i−1} 中 = [ <span id="rox">0.000</span>, <span id="roy">0.000</span>, <span id="roz">0.600</span> ]<sup>T</sup>
    　（a<sub>i</sub> = 0 ⇒ X、Y 分量恒为 0）</div>
  <div class="row small">两轴关系：<span id="parallel">Z<sub>i</sub> ∥ Z<sub>i−1</sub>（α<sub>i</sub> = 0）</span></div>
  <div class="row small" data-mobile-hide>A<sub>i</sub> 位移列 = [ <span id="trx">0.000</span>, <span id="try">0.000</span>, <span id="trz">0.600</span> ]<sup>T</sup>
    = [0, 0, d<sub>i</sub>]<sup>T</sup>（式(3.21)）</div>
</div>
"""

SCRIPT = r"""
(function () {
  "use strict";

  var viewport = document.getElementById("viewport");
  var gGrid = document.getElementById("gGrid");
  var gLink = document.getElementById("gLink");
  var gAxisZ = document.getElementById("gAxisZ");
  var gDim = document.getElementById("gDim");
  var gFrame = document.getElementById("gFrame");
  var gGhost = document.getElementById("gGhost");

  var DEFAULTS = { d: 0.6, e: 0, alpha: 0, showZero: true, showFrames: true, showGhost: false, auto: false };

  // state 必须在任何取景/绘制函数首次调用之前定义（否则 fit() 抛错会让整页空白）
  var state = {
    d: DEFAULTS.d, e: DEFAULTS.e, alpha: DEFAULTS.alpha,
    showZero: true, showFrames: true, showGhost: false, auto: false,
    userZoom: false, zoomRatio: 1, compact: false
  };

  var C = {
    x: "#d93025", y: "#2563eb", z: "#12944f",
    prev: "#174ea6", next: "#7c3aed", dim: "#c26a10",
    link: "#cbd5e1", linkIn: "#eef3f9", metal: "#94a3b8",
    ref: "#94a3b8", grid: "#e2eaf5", text: "#334155",
    ghost: "#d93025"
  };

  var L = {
    base: 1.05,     // 杆件 i−1 沿关节轴的长度
    collar: 0.16,   // 移动副套筒半长
    arm: 0.95,      // 杆件 i 的长度
    armHalf: 0.11,  // 杆件 i 的半宽
    axisHalf: 1.45  // 关节轴线的半长
  };

  var scene = new FK.Scene({
    svg: viewport,
    origin: { x: 660, y: 350 },
    scale: 170,
    yaw: -0.74,
    pitch: 0.40,
    minScale: 40,
    maxScale: 680
  });

  /* ================================================================ 数学 */

  /**
   * 教材式(3.20)：A_i = Rot(Z,θ_i)·Trans(a_i,0,d_i)·Rot(X,α_i)（行主序 4×4）。
   * [a cθ, −sθ cα, sθ sα, a cθ;  sθ, cθ cα, −cθ sα, a sθ;  0, sα, cα, d;  0,0,0,1]
   */
  function transformA(theta, a, d, alpha) {
    var ct = Math.cos(theta), st = Math.sin(theta);
    var ca = Math.cos(alpha), sa = Math.sin(alpha);
    return [
      ct, -st * ca, st * sa, a * ct,
      st, ct * ca, -ct * sa, a * st,
      0, sa, ca, d,
      0, 0, 0, 1
    ];
  }

  /** 棱柱关节：a_i = 0，θ_i = 0（移动关节不发生绕 Z 的转动） */
  function prismaticA(d, alpha) { return transformA(0, 0, d, alpha); }

  /** 转动关节（对照用）：a_i ≠ 0，关节变量是 θ_i */
  function revoluteA(theta, a, d, alpha) { return transformA(theta, a, d, alpha); }

  function col(m, i) { return [m[i], m[4 + i], m[8 + i]]; }
  function at(o, dir, len) { return FK.Vec.add(o, FK.Vec.scale(dir, len)); }

  /* 世界坐标（{i−1} 系）中的布置：Z_{i−1} 竖直向上，横向偏置 e 沿 X */
  function layoutModel() {
    var A = prismaticA(state.d, state.alpha * FK.DEG);
    var Oprev = [state.e, 0, 0];
    var Oi = FK.Vec.add(Oprev, FK.M4.position(A));   // = Oprev + [0, 0, d]
    // 轴向控制点：Z_{i−1} / Z_i 及其“棱柱移动矢量”方向
    var vA = FK.Vec.normalize([0, 0, state.d]);      // 移动矢量方向（竖直）
    var vZ = FK.Vec.normalize(col(A, 2));            // Z_i 方向
    var vX = FK.Vec.normalize(col(A, 0));            // X_i 方向（= Z_{i−1} × Z_i 方向）
    return {
      A: A, Oprev: Oprev, Oi: Oi, vA: vA, vZ: vZ, vX: vX,
      // 杆件 i 的伸展方向：α = 0 时沿 X_i（水平），α ≠ 0 时沿 −Z_i（竖直分量被 α “吃掉”）
      armDir: Math.abs(state.alpha) < 1e-9 ? [1, 0, 0] : FK.Vec.scale(vZ, -1),
      originDist: FK.Vec.len(FK.Vec.sub(Oi, Oprev))
    };
  }

  /* ================================================================ 取景 */
  // 本底座的图把 viewBox 与容器像素 1:1 对齐（preserveAspectRatio="none"），
  // 再按“图形屏幕包围盒”反推 scale / origin，等价于克雷格版底座的 FK.AdaptiveScene。

  var _fitting = false;

  function boundsPoints(M) {
    var pts = [M.Oprev, M.Oi];
    pts.push(at(M.Oprev, [0, 0, 1], -0.75));
    pts.push(at(M.Oprev, [0, 0, 1], 1.35));
    pts.push(at(M.Oi, M.vZ, -0.6));
    pts.push(at(M.Oi, M.vZ, 0.9));
    pts.push(at(M.Oi, M.armDir, L.arm));
    pts.push(at(M.Oi, M.armDir, -0.28));
    pts.push(FK.Vec.add(M.Oprev, [-0.28, 0, 0]));
    pts.push([state.e + 0.9, 0, 0]);
    pts.push([state.e - 0.9, 0, 0]);
    return pts;
  }

  function fit(M) {
    if (_fitting) return;
    _fitting = true;
    var rect = viewport.getBoundingClientRect();
    var W = Math.max(300, Math.round(rect.width || 1000));
    var H = Math.max(300, Math.round(rect.height || 700));
    viewport.setAttribute("viewBox", "0 0 " + W + " " + H);
    viewport.setAttribute("preserveAspectRatio", "none");

    var narrow = W < 720;
    var ax0 = narrow ? 8 : 332, ax1 = W - 8;
    var ay0 = 12, ay1 = H - 12;
    var panel = document.querySelector(".panel");
    if (panel) {
      var pr = panel.getBoundingClientRect();
      if (narrow) { if (pr.top > 60) ay1 = Math.min(ay1, pr.top - 8); }
      else if (pr.right < W - 220) { ax0 = Math.max(ax0, pr.right + 12); }
    }
    // 读数卡固定在右上角（移动端在顶部）。图形要避开它，避免遮挡。
    var readout = document.querySelector(".readout");
    if (readout) {
      var rr = readout.getBoundingClientRect();
      var sy2 = H / Math.max(1, rect.height);
      var roBottom = (rr.bottom - rect.top) * sy2;
      if (!isFinite(roBottom)) roBottom = 0;
      if (narrow) {
        if (roBottom > 20 && ay1 - roBottom > 260) ay0 = Math.max(ay0, roBottom + 8);
      } else if (roBottom > 20 && roBottom < H - 120) {
        var belowH = ay1 - Math.max(ay0, roBottom + 10);
        var leftW = rr.left - 10 - ax0;
        if (belowH >= 250 || belowH * 1.4 >= leftW) ay0 = Math.max(ay0, roBottom + 10);
        else if (rr.left > ax0 + 190) ax1 = Math.min(ax1, rr.left - 10);
      }
    }
    if (ax1 - ax0 < 190) ax0 = 8;

    // 迭代收敛：每一轮都用“当前缩放对应的”屏幕外接框重新定缩放与位置
    //（不能拿旧缩放的尺寸去反推新缩放，那会把图形算小/算偏 —— 第一批出过这个问题）
    var pts = boundsPoints(M);
    var unit = scene.state.scale;
    var ratio = state.userZoom ? Math.max(0.2, Math.min(5, state.zoomRatio)) : 1;
    var passes = 4;
    for (var p = 0; p < passes; p += 1) {
      var e = screenExtent(pts);
      var eff = unit * ratio;
      var availW = Math.max(120, ax1 - ax0 - 24);
      var availH = Math.max(120, ay1 - ay0 - 24);
      var need = Math.max(e.w > 1e-6 ? e.w / eff : 0, e.h > 1e-6 ? e.h / eff : 0);
      var next = need > 1e-6 ? Math.min(availW, availH) / need : unit;
      unit = Math.max(scene.limits.minScale, Math.min(scene.limits.maxScale, next));
      scene.defaults.scale = unit;
      scene.state.scale = Math.max(scene.limits.minScale,
        Math.min(scene.limits.maxScale, unit * ratio));
      var e2 = screenExtent(pts);
      var sc = scene.state.scale / eff;
      var bcx = (e2.x0 + e2.x1) / 2;
      var bcy = (e2.y0 + e2.y1) / 2;
      scene.origin.x += (ax0 + ax1) / 2 - bcx * sc - (1 - sc) * scene.origin.x;
      scene.origin.y += (ay0 + ay1) / 2 - bcy * sc - (1 - sc) * scene.origin.y;
      var pad = (p === passes - 1) ? 8 : 20;
      var e3 = screenExtent(pts);
      if (e3.x1 > ax1 - pad) scene.origin.x -= e3.x1 - (ax1 - pad);
      if (e3.x0 < ax0 + pad) scene.origin.x += (ax0 + pad) - e3.x0;
      if (e3.y1 > ay1 - pad) scene.origin.y -= e3.y1 - (ay1 - pad);
      if (e3.y0 < ay0 + pad) scene.origin.y += (ay0 + pad) - e3.y0;
    }
    scene.baseOrigin.x = scene.origin.x;
    scene.baseOrigin.y = scene.origin.y;
    state.compact = (ax1 - ax0) < 430 || scene.state.scale < 96;
    _fitting = false;
  }

  /** 在给定缩放下的屏幕外接框 */
  function screenExtent(pts) {
    var dxs = [], dys = [], i, p;
    for (i = 0; i < pts.length; i += 1) {
      p = scene.project(pts[i]);
      dxs.push(p.x);
      dys.push(p.y);
    }
    var x0 = Math.min.apply(null, dxs), x1 = Math.max.apply(null, dxs);
    var y0 = Math.min.apply(null, dys), y1 = Math.max.apply(null, dys);
    return { x0: x0, x1: x1, y0: y0, y1: y1, w: x1 - x0, h: y1 - y0 };
  }

  /* ============================================================ 绘图工具 */

  function seg(a, b, attrs, parent) {
    var A = scene.project(a), B = scene.project(b);
    return scene.el("line", Object.assign({
      x1: A.x, y1: A.y, x2: B.x, y2: B.y, "stroke-linecap": "round"
    }, attrs || {}), parent);
  }

  function tag(v, str, attrs, dx, dy, parent) {
    var p = scene.project(v);
    var node = scene.el("text", Object.assign({
      x: p.x + (dx || 0), y: p.y + (dy || 0),
      "font-size": 14, "font-weight": 700, class: "fk-axis-label"
    }, attrs || {}), parent);
    node.textContent = str;
    return node;
  }

  function screenTag(x, y, str, attrs, parent) {
    var node = scene.el("text", Object.assign({
      x: x, y: y, "font-size": 13, "font-weight": 700, class: "fk-axis-label"
    }, attrs || {}), parent);
    node.textContent = str;
    return node;
  }

  function dotAt(v, r, fill, parent) {
    var p = scene.project(v);
    scene.el("circle", { cx: p.x, cy: p.y, r: r, fill: fill, class: "fk-point" }, parent);
  }

  /** 世界坐标矩形（用于画杆件/套筒的实体） */
  function quad(a, b, c, dd, attrs, parent) {
    var pts = [a, b, c, dd].map(function (v) {
      var p = scene.project(v);
      return p.x + "," + p.y;
    }).join(" ");
    scene.el("polygon", Object.assign({ points: pts }, attrs || {}), parent);
  }

  /** 坐标轴（带箭头 + 轴标） */
  function axis(o, dir, len, color, marker, label, parent, dx, dy) {
    var tip = at(o, dir, len);
    seg(o, tip, { stroke: color, "stroke-width": 2.6, "marker-end": "url(#" + marker + ")" }, parent);
    if (label) tag(tip, label, { fill: color, "font-size": 13.5 }, dx === undefined ? 5 : dx,
      dy === undefined ? 4 : dy, parent);
    return tip;
  }

  /** 沿世界 Z（= 关节轴方向）的尺寸线，量取范围 [z0, z1]（相对 Oprev 的 z 值） */
  function dimZ(z0, z1, sideX, color, text, parent) {
    var a = [state.e + sideX, 0, z0];
    var b = [state.e + sideX, 0, z1];
    var A = scene.project(a), B = scene.project(b);
    if (Math.abs(B.y - A.y) < 10) return;
    scene.el("line", {
      x1: A.x, y1: A.y, x2: B.x, y2: B.y, stroke: color, "stroke-width": 2,
      "marker-start": "url(#arD)", "marker-end": "url(#arD)"
    }, parent);
    [-1, 1].forEach(function (s) {
      var p = s < 0 ? A : B;
      scene.el("line", {
        x1: p.x - 9, y1: p.y, x2: p.x + 9, y2: p.y, stroke: color, "stroke-width": 2
      }, parent);
    });
    screenTag((A.x + B.x) / 2 + 16, (A.y + B.y) / 2 + 5, text,
      { fill: color, "font-size": 15, "font-style": "italic" }, parent);
  }

  /* ================================================================ 渲染 */

  function render() {
    gGrid.replaceChildren();
    gLink.replaceChildren();
    gAxisZ.replaceChildren();
    gDim.replaceChildren();
    gFrame.replaceChildren();
    gGhost.replaceChildren();

    var M = layoutModel();
    fit(M);

    var A = M.A, Oprev = M.Oprev, Oi = M.Oi;
    var zPrev = [0, 0, 1];
    var xPrev = [1, 0, 0];
    var yPrev = [0, 1, 0];
    var Xi = M.vX, Zi = M.vZ;
    var Yi = FK.Vec.normalize(FK.Vec.cross(Zi, Xi));

    // 地面网格
    for (var gi = -2; gi <= 2; gi += 1) {
      seg([-2, gi, 0], [2, gi, 0], { stroke: C.grid, "stroke-width": 1 }, gGrid);
      seg([gi, -2, 0], [gi, 2, 0], { stroke: C.grid, "stroke-width": 1 }, gGrid);
    }

    /* ---- 杆件 i−1（固定）与关节轴线 Z_{i−1} ---- */
    var p0 = at(Oprev, zPrev, -L.base * 0.55);
    var p1 = at(Oprev, zPrev, L.base);
    quad(at(p0, xPrev, -0.19), at(p1, xPrev, -0.19), at(p1, xPrev, 0.19), at(p0, xPrev, 0.19),
      { fill: "#e2e8f0", stroke: "#94a3b8", "stroke-width": 1.6 }, gLink);
    if (!state.compact) {
      tag(at(Oprev, zPrev, L.base * 0.62), "连杆 i−1", { fill: "#475569", "font-size": 13, "text-anchor": "end" },
        -15, 4, gLink);
    }
    // 关节轴线（= Z_{i−1} 所在直线 = 移动方向）
    seg(at(Oprev, zPrev, -L.axisHalf), at(Oprev, zPrev, L.axisHalf), {
      stroke: C.prev, "stroke-width": 3,
      "marker-start": "url(#arZp)", "marker-end": "url(#arZp)"
    }, gAxisZ);
    tag(at(Oprev, zPrev, L.axisHalf), "关节轴 Z" + "i\u22121" + "（= 移动方向）",
      { fill: C.prev, "font-size": 14, "text-anchor": "end" }, -16, -8, gAxisZ);

    /* ---- 移动副：套筒 + 杆件 i（刚体随 {i} 平移/转动） ---- */
    var c0 = at(Oi, zPrev, -L.collar);
    var c1 = at(Oi, zPrev, L.collar);
    quad(at(c0, xPrev, -0.27), at(c1, xPrev, -0.27), at(c1, xPrev, 0.27), at(c0, xPrev, 0.27),
      { fill: "#cbd5e1", stroke: "#64748b", "stroke-width": 1.8 }, gLink);
    // 杆件 i：以 O_i 为起点、沿 armDir 伸出，并用 X_i / Z_i 张成的截面
    var dArm = M.armDir;
    var nArm = FK.Vec.normalize(FK.Vec.cross(dArm, [0, 1, 0]));
    if (FK.Vec.len(nArm) < 1e-9) nArm = [0, 0, 1];
    var t0 = Oi, t1 = at(Oi, dArm, L.arm);
    quad(at(t0, nArm, -L.armHalf), at(t1, nArm, -L.armHalf), at(t1, nArm, L.armHalf), at(t0, nArm, L.armHalf),
      { fill: "#dbe3ee", stroke: "#7c8ba1", "stroke-width": 1.8 }, gLink);
    if (!state.compact) {
      var mid = scene.project([(Oi[0] + t1[0]) / 2, (Oi[1] + t1[1]) / 2, (Oi[2] + t1[2]) / 2]);
      screenTag(mid.x + 14, mid.y - 12, "连杆 i",
        { fill: "#475569", "font-size": 13 }, gLink);
    }

    /* ---- 两个坐标系 {i−1} 与 {i} ---- */
    if (state.showFrames) {
      axis(Oprev, xPrev, 0.62, C.x, "arX", "X\u0302" + "i\u22121", gFrame);
      axis(Oprev, yPrev, 0.62, C.y, "arY", "Y\u0302" + "i\u22121", gFrame);
      axis(Oprev, zPrev, 0.78, C.z, "arZ", "Z\u0302" + "i\u22121", gFrame, 6, -6);
      axis(Oi, Xi, 0.62, C.x, "arX", "X\u0302" + "i", gFrame);
      axis(Oi, Yi, 0.62, C.y, "arY", "Y\u0302" + "i", gFrame);
      axis(Oi, Zi, 0.78, C.z, "arZ", "Z\u0302" + "i", gFrame, 6, -6);
    } else {
      dotAt(Oprev, 4.6, "#334155", gFrame);
      dotAt(Oi, 4.6, "#334155", gFrame);
    }
    dotAt(Oprev, 5.4, C.prev, gFrame);
    dotAt(Oi, 5.4, C.next, gFrame);
    var pp = scene.project(Oprev), pi = scene.project(Oi);
    screenTag(pp.x - 12, pp.y + 22, "O" + "i\u22121", { fill: C.prev, "font-size": 13.5, "text-anchor": "end" }, gFrame);
    screenTag(pi.x + 14, pi.y + 20, "O" + "i", { fill: C.next, "font-size": 13.5 }, gFrame);
    screenTag(pi.x + 14, pi.y + 36, "{i}", { fill: C.next, "font-size": 13, "font-style": "italic" }, gFrame);

    /* ---- d_i 的量取方向与零位 ---- */
    var dist = M.originDist;
    if (Math.abs(state.d) > 0.02) {
      // 沿 Z_{i−1}（竖直）量取：从零位（与 O_{i−1} 同高点）到 O_i
      dimZ(0, state.d, 0.58, C.dim, "d" + "i" + " = " + FK.format(state.d, 2), gDim);
      // 移动矢量箭头：沿关节轴方向、长度 |d|
      seg([state.e - 0.30, 0, Math.min(0, state.d)], [state.e - 0.30, 0, Math.max(0, state.d)],
        { stroke: C.dim, "stroke-width": 3, "stroke-dasharray": "2 0", "marker-end": "url(#arD)" }, gDim);
      if (!state.compact) {
        tag([state.e - 0.30, 0, state.d * 0.5], "Z\u0302" + "i\u22121" + " 方向移动",
          { fill: C.dim, "font-size": 12, "text-anchor": "end" }, -8, 4, gDim);
      }
    }
    if (state.showZero) {
      // 零位参考：d_i = 0 时 {i} 的原点就落在这里（与 O_{i−1} 重合）
      var zp = scene.project(Oprev);
      scene.el("circle", {
        cx: zp.x, cy: zp.y, r: 15, fill: "none", stroke: C.ref,
        "stroke-width": 2, "stroke-dasharray": "5 4"
      }, gDim);
      if (!state.showFrames) {
        seg(Oprev, Oi, { stroke: C.ref, "stroke-width": 1.6, "stroke-dasharray": "5 4" }, gDim);
      }
      screenTag(zp.x - 18, zp.y - 44, "零位：d" + "i" + " = 0 ⇒ O" + "i" + " 与 O" + "i\u22121" + " 重合",
        { fill: "#64748b", "font-size": 12, "text-anchor": "end" }, gDim);
    }
    if (state.showZero && Math.abs(state.d) > 0.02) {
      seg(Oprev, Oi, { stroke: C.ref, "stroke-width": 1.5, "stroke-dasharray": "5 4" }, gDim);
      var mid = scene.project([state.e, 0, state.d / 2]);
      screenTag(mid.x - 8, mid.y + 4, "|d" + "i" + "| = " + FK.format(dist, 3) + "（a" + "i" + " = 0）",
        { fill: "#b45309", "font-size": 12, "text-anchor": "end" }, gDim);
    }

    /* ---- 与转动关节的对比（阴影） ---- */
    if (state.showGhost) {
      // 转动关节：a_i ≠ 0，{i} 的原点偏离 Z_{i−1}，且关节变量是 θ_i
      var aRev = 0.72;
      var thetaRev = 40 * FK.DEG;
      var Rev = revoluteA(thetaRev, aRev, 0, state.alpha * FK.DEG);
      var Orev = FK.Vec.add(Oprev, FK.M4.position(Rev));
      var RevX = FK.Vec.normalize(col(Rev, 0));
      var RevZ = FK.Vec.normalize(col(Rev, 2));
      seg(Oprev, Orev, {
        stroke: C.ghost, "stroke-width": 2.4, "stroke-dasharray": "8 6", "marker-end": "url(#arA)"
      }, gGhost);
      axis(Orev, RevX, 0.5, C.ghost, "arA", null, gGhost);
      axis(Orev, RevZ, 0.66, C.ghost, "arA", null, gGhost);
      var rp = scene.project(Orev);
      scene.el("circle", { cx: rp.x, cy: rp.y, r: 5, fill: "none", stroke: C.ghost, "stroke-width": 2 }, gGhost);
      screenTag(rp.x + 12, rp.y - 8, "转动关节：a" + "i" + " \u2260 0，原点不在 Z" + "i\u22121" + " 上",
        { fill: C.ghost, "font-size": 12 }, gGhost);
      // 绕 Z_{i−1} 的 θ_i 弧
      var pts = [], steps = 24, t, k;
      for (k = 0; k <= steps; k += 1) {
        t = thetaRev * (k / steps);
        pts.push(FK.Vec.add(Oprev, [0.42 * Math.cos(t) + aRev * 0.05, 0.42 * Math.sin(t), 0.30]));
      }
      scene.polyline(pts, { stroke: C.ghost, "stroke-width": 2, "stroke-dasharray": "6 5", fill: "none" }, gGhost);
      screenTag(rp.x + 12, rp.y + 8, "关节变量是 \u03b8" + "i", { fill: C.ghost, "font-size": 12 }, gGhost);
    }

    updateReadout(M);
  }

  /* ================================================================ 读数 */

  var MX_TPL = [
    [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]
  ];

  function updateMatrix(A) {
    var tbody = document.getElementById("mxBody");
    tbody.replaceChildren();
    for (var r = 0; r < 4; r += 1) {
      var tr = document.createElement("tr");
      for (var c = 0; c < 4; c += 1) {
        var v = A[MX_TPL[r][c]];
        var td = document.createElement("td");
        td.textContent = (Math.abs(v) < 5e-4 ? 0 : v).toFixed(3);
        if (r === 3) { td.className = "dim"; }
        else if (c === 3) { td.className = "zero"; }
        else if (c === 2 && r === 2) { td.className = "hi"; }
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    }
  }

  function updateReadout(M) {
    var p = FK.M4.position(M.A);
    document.getElementById("roD").textContent = FK.format(state.d, 3);
    document.getElementById("roA").textContent = FK.deg(state.alpha, 1);
    document.getElementById("roR").textContent = FK.format(M.originDist, 3);
    document.getElementById("rox").textContent = FK.format(p[0], 3);
    document.getElementById("roy").textContent = FK.format(p[1], 3);
    document.getElementById("roz").textContent = FK.format(p[2], 3);
    document.getElementById("trx").textContent = FK.format(M.A[3], 3);
    document.getElementById("try").textContent = FK.format(M.A[7], 3);
    document.getElementById("trz").textContent = FK.format(M.A[11], 3);
    var par = Math.abs(state.alpha) < 1e-9;
    document.getElementById("parallel").innerHTML = par
      ? "Z<sub>i</sub> ∥ Z<sub>i−1</sub>（α<sub>i</sub> = 0；棱柱联轴器的 Z 轴在关节 i+1 的轴线上）"
      : "Z<sub>i</sub> 与 Z<sub>i−1</sub> 夹角 = α<sub>i</sub> = " + FK.deg(state.alpha, 1) +
        "（a<sub>i</sub> 仍为 0，原点仍在同一根关节轴上）";
    document.getElementById("status").textContent = Math.abs(state.d) < 1e-9
      ? "移动（棱柱）关节 i：d\u1d62 = 0 —— 处于零位，{i} 与 {i−1} 原点重合"
      : "移动（棱柱）关节 i：关节变量 d\u1d62 = " + FK.format(state.d, 3) + "，a\u1d62 = 0";
    document.getElementById("status").style.color = Math.abs(state.d) < 1e-9 ? "#b45309" : "#174ea6";
    updateMatrix(M.A);
  }

  /* ================================================================ 交互 */

  function drawAll() { fit(layoutModel()); render(); }

  var rangeIds = ["d", "e", "alpha"];
  rangeIds.forEach(function (id) {
    var el = document.getElementById(id);
    el.addEventListener("input", function () {
      var v = Number(el.value);
      state[id] = v;
      document.getElementById(id + "Value").textContent =
        id === "alpha" ? FK.deg(v, 1) : FK.format(v, 2);
      drawAll();
    });
  });

  ["showZero", "showFrames", "showGhost"].forEach(function (id) {
    var el = document.getElementById(id);
    el.addEventListener("change", function () { state[id] = el.checked; render(); });
  });
  var autoEl = document.getElementById("auto");
  autoEl.addEventListener("change", function () { state.auto = autoEl.checked; scene.setAuto(state.auto); });

  document.getElementById("reset").addEventListener("click", function () {
    state.d = DEFAULTS.d; state.e = DEFAULTS.e; state.alpha = DEFAULTS.alpha;
    state.showZero = true; state.showFrames = true; state.showGhost = false; state.auto = false;
    state.userZoom = false;
    state.zoomRatio = 1;
    document.getElementById("d").value = DEFAULTS.d;
    document.getElementById("e").value = DEFAULTS.e;
    document.getElementById("alpha").value = DEFAULTS.alpha;
    document.getElementById("dValue").textContent = FK.format(DEFAULTS.d, 2);
    document.getElementById("eValue").textContent = FK.format(DEFAULTS.e, 2);
    document.getElementById("alphaValue").textContent = FK.deg(DEFAULTS.alpha, 1);
    document.getElementById("showZero").checked = true;
    document.getElementById("showFrames").checked = true;
    document.getElementById("showGhost").checked = false;
    document.getElementById("auto").checked = false;
    scene.setAuto(false);
    scene.reset();
    drawAll();
  });

  // 用户手动改变视角后不再覆盖其缩放：记录相对自适应缩放的倍率
  function rememberZoom() {
    state.userZoom = true;
    state.zoomRatio = Math.max(0.2, Math.min(5, scene.state.scale / scene.defaults.scale));
  }
  viewport.addEventListener("wheel", rememberZoom, { passive: true });
  viewport.addEventListener("pointerdown", rememberZoom);

  window.addEventListener("resize", function () {
    state.userZoom = false;
    state.zoomRatio = 1;
    drawAll();
  });
  window.addEventListener("load", function () { drawAll(); });

  /* ============================================================ 数值自检 */

  (function selfTest() {
    function assert(cond, msg) { if (!cond) throw new Error("图3.17 自检失败：" + msg); }
    function nearly(a, b, e) { return Math.abs(a - b) < (e === undefined ? 1e-12 : e); }

    // 0) 初始化顺序：state 必须在 fit() 首次调用之前定义
    assert(state && typeof state === "object" && typeof state.d === "number",
      "state 未定义或不完整（初始化顺序错误）");

    // 1) 式(3.21) 与 式(3.20) 代入 a_i = 0 逐元素一致；第 4 列为 [0, 0, d, 1]ᵀ
    [[0.6, 0], [-1.5, 0], [1.5, -90 * FK.DEG], [0, 90 * FK.DEG], [0.35, 35 * FK.DEG]].forEach(function (cse) {
      var d = cse[0], al = cse[1];
      var got = prismaticA(d, al);
      var ca = Math.cos(al), sa = Math.sin(al);
      var want = [1, 0, 0, 0, 0, ca, -sa, 0, 0, sa, ca, d, 0, 0, 0, 1];
      for (var i = 0; i < 16; i += 1) {
        assert(nearly(got[i], want[i]),
          "式(3.21) 元素 " + i + " 不符（d=" + d + ", α=" + al + "）：" + got[i] + " ≠ " + want[i]);
      }
      assert(nearly(got[3], 0) && nearly(got[7], 0),
        "a_i = 0 时位移的 X/Y 分量必须为 0");
      assert(nearly(got[11], d), "位移的 Z 分量必须等于 d_i");
    });

    // 2) 旋转部分正交且 det = +1（α_i ≠ 0 时也成立，说明式(3.21) 第 3 行第 3 列取 cα 是对的）
    [[0.6, 0], [0.6, 90 * FK.DEG], [-0.4, -55 * FK.DEG]].forEach(function (cse) {
      var R = FK.M4.rotation(prismaticA(cse[0], cse[1]));
      var i, j, k, sum, det;
      for (i = 0; i < 3; i += 1) {
        for (j = 0; j < 3; j += 1) {
          sum = 0;
          for (k = 0; k < 3; k += 1) sum += R[i * 3 + k] * R[j * 3 + k];
          assert(nearly(sum, i === j ? 1 : 0, 1e-12), "旋转部分非正交 @" + i + "," + j);
        }
      }
      det = R[0] * (R[4] * R[8] - R[5] * R[7]) - R[1] * (R[3] * R[8] - R[5] * R[6])
        + R[2] * (R[3] * R[7] - R[4] * R[6]);
      assert(nearly(det, 1, 1e-12), "旋转部分行列式应为 +1，实得 " + det);
    });

    // 3) a_i = 0 的核心后果：O_i 恒在 Z_{i−1} 轴上（X、Y 分量为 0），与 d_i、α_i 无关
    [0, 0.6, -1.5, 1.5, 0.123].forEach(function (d) {
      [0, 30, -90, 90, 47].forEach(function (adeg) {
        var p = FK.M4.position(prismaticA(d, adeg * FK.DEG));
        assert(nearly(p[0], 0, 1e-12) && nearly(p[1], 0, 1e-12),
          "a_i = 0 时 O_i 的 X/Y 分量应为 0（d=" + d + ", α=" + adeg + "），实得 " + JSON.stringify(p));
      });
    });

    // 4) d_i = 0 定义零位：两原点距离为 0（即“联轴器的坐标系原点与下一个连杆原点重合”）
    [[0, 0], [0, 45 * FK.DEG], [0, -90 * FK.DEG]].forEach(function (cse) {
      var p = FK.M4.position(prismaticA(cse[0], cse[1]));
      assert(nearly(FK.Vec.len(p), 0, 1e-12), "d_i = 0 时两原点距离应为 0，实得 " + FK.Vec.len(p));
    });

    // 5) d_i 变化只沿 Z 平移：X/Y 分量不变、位移量 = |Δd_i|、两原点距离 = |d_i|
    var dA = 0.6, dB = -1.1;
    var pa = FK.M4.position(prismaticA(dA, 40 * FK.DEG));
    var pb = FK.M4.position(prismaticA(dB, 40 * FK.DEG));
    assert(nearly(pa[0], pb[0], 1e-12) && nearly(pa[1], pb[1], 1e-12),
      "改变 d_i 时 X/Y 分量不应变化");
    assert(nearly(pb[2] - pa[2], dB - dA, 1e-12), "Z 分量变化量应等于 Δd_i");
    assert(nearly(FK.Vec.len(FK.Vec.sub(pb, pa)), Math.abs(dB - dA), 1e-12),
      "位移量应等于 |Δd_i|");
    [0.6, -1.5, 1.5].forEach(function (d) {
      [0, 25 * FK.DEG].forEach(function (al) {
        var p = FK.M4.position(prismaticA(d, al));
        assert(nearly(FK.Vec.len(p), Math.abs(d), 1e-12),
          "a_i = 0 ⇒ 两原点距离应恒等于 |d_i|（d=" + d + "）");
      });
    });

    // 6) 与转动关节的差异：转动关节 a_i ≠ 0 ⇒ 原点偏离 Z_{i−1}（X/Y 分量不为 0）
    var pr = FK.M4.position(revoluteA(40 * FK.DEG, 0.72, 0, 0));
    assert(nearly(pr[0], 0.72 * Math.cos(40 * FK.DEG), 1e-12) &&
      nearly(pr[1], 0.72 * Math.sin(40 * FK.DEG), 1e-12),
      "转动关节 O_i 应在 X/Y 平面内偏离原点（a_i ≠ 0）");
    assert(!nearly(pr[0], 0) || !nearly(pr[1], 0), "转动关节原点不应落在 Z_{i−1} 上");

    // 7) 逆变换自洽：A_i⁻¹·A_i = I（用于核对 d_i 的符号约定）
    var A = prismaticA(0.6, 25 * FK.DEG);
    var I = FK.M4.multiply(FK.M4.inverse(A), A);
    for (var m = 0; m < 16; m += 1) {
      assert(nearly(I[m], m % 5 === 0 ? 1 : 0, 1e-12), "A_i⁻¹·A_i 应为单位阵 @" + m);
    }
  }());

  drawAll();
}());
"""

FIGURE = {
    "id": "figure-3-17",
    "title": "图3.17 棱柱联轴器连杆 D-H 坐标系 · 人机交互演示（《机器人技术基础（第三版）》）",
    "css": CSS,
    "body": BODY,
    "script": SCRIPT,
}
