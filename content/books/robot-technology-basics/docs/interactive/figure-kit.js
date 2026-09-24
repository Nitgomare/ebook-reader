/*!
 * figure-kit.js — 交互教学图公共底座
 *
 * 为两本机器人教材的交互图提供统一的三维投影、视图拖动/缩放、滑块与重置逻辑。
 * 纯原生 JavaScript，无任何外部依赖，可在 iframe sandbox="allow-scripts" 下运行。
 *
 * 主要 API（挂在 window.FK 上）：
 *   FK.Vec        三维向量运算（add/sub/scale/dot/cross/norm/normalize）
 *   FK.M4         4x4 齐次变换矩阵运算（identity/multiply/rotX/rotY/rotZ/rotAxis/translate/apply/fromRT/inverse）
 *   FK.Scene      可交互三维场景（SVG 或 Canvas 渲染、正交投影、指针捕获、滚轮缩放、自动旋转）
 *   FK.bindRanges 把 range 输入批量绑定到 state 并刷新
 *   FK.format     数值格式化
 *
 * 坐标约定：右手坐标系，x 向右、y 向前（屏幕内）、z 向上。
 * 投影：先绕 z 轴 yaw、再绕屏幕水平轴 pitch 的正交投影，可缩放。
 */
(function (global) {
  "use strict";

  /* ------------------------------------------------------------------ 向量 */

  var Vec = {
    add: function (a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; },
    sub: function (a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; },
    scale: function (a, s) { return [a[0] * s, a[1] * s, a[2] * s]; },
    dot: function (a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; },
    cross: function (a, b) {
      return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
      ];
    },
    len: function (a) { return Math.sqrt(Vec.dot(a, a)); },
    normalize: function (a) {
      var n = Vec.len(a);
      return n < 1e-12 ? [0, 0, 0] : Vec.scale(a, 1 / n);
    },
    /** 与教材一致：向量按列写成矩阵，转置后返回行向量字符串 */
    round: function (a, digits) {
      var d = digits === undefined ? 3 : digits;
      var p = Math.pow(10, d);
      return a.map(function (v) { return Math.round(v * p) / p; });
    },
    eq: function (a, b, eps) {
      var e = eps === undefined ? 1e-6 : eps;
      return Math.abs(a[0] - b[0]) < e && Math.abs(a[1] - b[1]) < e && Math.abs(a[2] - b[2]) < e;
    },
  };

  /* ------------------------------------------------------------------ 矩阵 */

  var M4 = {
    identity: function () { return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]; },
    /** 行主序 4x4 相乘 */
    multiply: function (a, b) {
      var out = new Array(16);
      for (var i = 0; i < 4; i += 1) {
        for (var j = 0; j < 4; j += 1) {
          var sum = 0;
          for (var k = 0; k < 4; k += 1) sum += a[i * 4 + k] * b[k * 4 + j];
          out[i * 4 + j] = sum;
        }
      }
      return out;
    },
    chain: function () {
      var out = M4.identity();
      for (var i = 0; i < arguments.length; i += 1) out = M4.multiply(out, arguments[i]);
      return out;
    },
    rotX: function (rad) {
      var c = Math.cos(rad), s = Math.sin(rad);
      return [1, 0, 0, 0, 0, c, -s, 0, 0, s, c, 0, 0, 0, 0, 1];
    },
    rotY: function (rad) {
      var c = Math.cos(rad), s = Math.sin(rad);
      return [c, 0, s, 0, 0, 1, 0, 0, -s, 0, c, 0, 0, 0, 0, 1];
    },
    rotZ: function (rad) {
      var c = Math.cos(rad), s = Math.sin(rad);
      return [c, -s, 0, 0, s, c, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
    },
    /** Rodrigues 轴角旋转；k 必须是单位轴（会自动归一化） */
    rotAxis: function (axis, rad) {
      var k = Vec.normalize(axis);
      var c = Math.cos(rad), s = Math.sin(rad), t = 1 - c;
      var x = k[0], y = k[1], z = k[2];
      return [
        t * x * x + c, t * x * y - s * z, t * x * z + s * y, 0,
        t * x * y + s * z, t * y * y + c, t * y * z - s * x, 0,
        t * x * z - s * y, t * y * z + s * x, t * z * z + c, 0,
        0, 0, 0, 1,
      ];
    },
    translate: function (v) {
      return [1, 0, 0, v[0], 0, 1, 0, v[1], 0, 0, 1, v[2], 0, 0, 0, 1];
    },
    /** 由旋转矩阵（行主序 3x3 数组）与位移构造齐次变换 */
    fromRT: function (r, p) {
      return [
        r[0], r[1], r[2], p[0],
        r[3], r[4], r[5], p[1],
        r[6], r[7], r[8], p[2],
        0, 0, 0, 1,
      ];
    },
    /** 变换一个点（含平移） */
    apply: function (m, v) {
      return [
        m[0] * v[0] + m[1] * v[1] + m[2] * v[2] + m[3],
        m[4] * v[0] + m[5] * v[1] + m[6] * v[2] + m[7],
        m[8] * v[0] + m[9] * v[1] + m[10] * v[2] + m[11],
      ];
    },
    /** 只变换方向（不含平移） */
    applyDir: function (m, v) {
      return [
        m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
        m[4] * v[0] + m[5] * v[1] + m[6] * v[2],
        m[8] * v[0] + m[9] * v[1] + m[10] * v[2],
      ];
    },
    /** 齐次逆变换：R 转置，-Rᵀp（教材式 2-45 的矩阵形式） */
    inverse: function (m) {
      var r = [m[0], m[1], m[2], m[4], m[5], m[6], m[8], m[9], m[10]];
      var rt = [r[0], r[3], r[6], r[1], r[4], r[7], r[2], r[5], r[8]];
      var p = [m[3], m[7], m[11]];
      var t = [
        -(rt[0] * p[0] + rt[1] * p[1] + rt[2] * p[2]),
        -(rt[3] * p[0] + rt[4] * p[1] + rt[5] * p[2]),
        -(rt[6] * p[0] + rt[7] * p[1] + rt[8] * p[2]),
      ];
      return M4.fromRT(rt, t);
    },
    /** 取 3x3 旋转部分 */
    rotation: function (m) {
      return [m[0], m[1], m[2], m[4], m[5], m[6], m[8], m[9], m[10]];
    },
    /** 取位移部分 */
    position: function (m) { return [m[3], m[7], m[11]]; },
    /** X-Y-Z 固定角（先绕 X 转 γ、再绕 Y 转 β、最后绕 Z 转 α），教材式 2-63 */
    fromFixedXYZ: function (gamma, beta, alpha) {
      return M4.chain(M4.rotZ(alpha), M4.rotY(beta), M4.rotX(gamma));
    },
    /** Z-Y-X 欧拉角（每次绕运动坐标系的新轴），教材式 2-71 */
    fromEulerZYX: function (alpha, beta, gamma) {
      return M4.chain(M4.rotZ(alpha), M4.rotY(beta), M4.rotX(gamma));
    },
  };

  /* ------------------------------------------------------------------ 场景 */

  var NS = "http://www.w3.org/2000/svg";
  var DEG = Math.PI / 180;

  /**
   * Scene 构造函数。
   * @param {object} options
   *   - svg: 承载投影图形的 SVG 元素（必填）
   *   - origin: 投影中心在 viewBox 中的位置，默认 {x: 560, y: 360}
   *   - scale: 每单位长度对应的像素数，默认 78
   *   - yaw / pitch: 初始视角（弧度）
   *   - minScale / maxScale / minPitch / maxPitch
   *   - onRender: 每次绘制后的回调（用于同步读数）
   *   - layer: 兼容字段；不传则使用 svg 自身作为绘图容器
   */
  function Scene(options) {
    var self = this;
    var opts = options || {};
    this.svg = opts.svg;
    if (!this.svg) throw new Error("FK.Scene 需要一个 svg 元素作为视图容器");
    this.layer = opts.layer || this.svg;
    this.defaults = {
      yaw: opts.yaw === undefined ? -0.72 : opts.yaw,
      pitch: opts.pitch === undefined ? 0.48 : opts.pitch,
      scale: opts.scale === undefined ? 78 : opts.scale,
      panX: 0,
      panY: 0,
    };
    this.limits = {
      minScale: opts.minScale === undefined ? 34 : opts.minScale,
      maxScale: opts.maxScale === undefined ? 190 : opts.maxScale,
      minPitch: opts.minPitch === undefined ? -1.15 : opts.minPitch,
      maxPitch: opts.maxPitch === undefined ? 1.15 : opts.maxPitch,
    };
    this.origin = opts.origin || { x: 560, y: 360 };
    this.baseOrigin = { x: this.origin.x, y: this.origin.y };
    this.state = {
      yaw: this.defaults.yaw,
      pitch: this.defaults.pitch,
      scale: this.defaults.scale,
      dragging: false,
      panning: false,
      pointerId: null,
      lastX: 0,
      lastY: 0,
      auto: false,
    };
    this.onRender = opts.onRender || null;
    this.autoSpeed = opts.autoSpeed === undefined ? 0.0032 : opts.autoSpeed;
    this._frame = 0;
    this._render = null;
    this._enableInteraction();
  }

  Scene.prototype = {
    /** 世界坐标 -> 屏幕坐标（正交投影 + 深度值） */
    project: function (v) {
      var s = this.state;
      var cy = Math.cos(s.yaw), sy = Math.sin(s.yaw);
      var cp = Math.cos(s.pitch), sp = Math.sin(s.pitch);
      var x1 = v[0] * cy - v[1] * sy;
      var y1 = v[0] * sy + v[1] * cy;
      var z1 = v[2];
      var depth = y1 * cp - z1 * sp;
      var vertical = y1 * sp + z1 * cp;
      return {
        x: this.origin.x + x1 * s.scale,
        y: this.origin.y - vertical * s.scale,
        depth: depth,
      };
    },
    /** 变换矩阵作用后再投影，便于处理带位姿的坐标系 */
    projectT: function (m, v) { return this.project(M4.apply(m, v)); },
    /** 清空图层 */
    clear: function () { while (this.layer.firstChild) this.layer.removeChild(this.layer.firstChild); },
    /** 创建 SVG 元素 */
    el: function (tag, attrs, parent) {
      var node = document.createElementNS(NS, tag);
      if (attrs) {
        Object.keys(attrs).forEach(function (key) {
          if (attrs[key] === null || attrs[key] === undefined) return;
          node.setAttribute(key, attrs[key]);
        });
      }
      (parent || this.layer).appendChild(node);
      return node;
    },
    /** 画一条线段（世界坐标） */
    line: function (a, b, attrs, parent) {
      var A = this.project(a), B = this.project(b);
      return this.el("line", Object.assign({ x1: A.x, y1: A.y, x2: B.x, y2: B.y }, attrs || {}), parent);
    },
    /** 画一条带箭头的线段，marker 为 marker id（不含 url()） */
    arrow: function (a, b, cls, marker, parent) {
      var A = this.project(a), B = this.project(b);
      return this.el("line", {
        x1: A.x, y1: A.y, x2: B.x, y2: B.y,
        class: cls,
        "marker-end": marker ? "url(#" + marker + ")" : null,
      }, parent);
    },
    /** 画文字标签 */
    text: function (v, str, attrs, dx, dy, parent) {
      var p = this.project(v);
      var node = this.el("text", Object.assign({
        x: p.x + (dx || 0),
        y: p.y + (dy || 0),
      }, attrs || {}), parent);
      node.textContent = str;
      return node;
    },
    /** 画一条折线 */
    polyline: function (points, attrs, parent) {
      var d = points.map(function (p) {
        var q = this.project(p);
        return q.x + "," + q.y;
      }, this).join(" ");
      return this.el("polyline", Object.assign({ points: d, fill: "none" }, attrs || {}), parent);
    },
    /** 画一个实心圆点 */
    dot: function (v, attrs, parent) {
      var p = this.project(v);
      return this.el("circle", Object.assign({ cx: p.x, cy: p.y, r: 6 }, attrs || {}), parent);
    },
    /**
     * 绘制一个坐标系（三根轴 + 标签）。
     * @param {number[]} m 4x4 齐次变换，定义坐标系在参考系中的位姿
     * @param {object} cfg { labels:[x,y,z], length, colors:[c1,c2,c3], marker, parent, dash }
     */
    axes: function (m, cfg) {
      var c = cfg || {};
      var len = c.length === undefined ? 2.4 : c.length;
      var labels = c.labels || ["X", "Y", "Z"];
      var colors = c.colors || ["#e23a34", "#1a73e8", "#2e9e63"];
      var dirs = [[len, 0, 0], [0, len, 0], [0, 0, len]];
      var group = c.parent || this.layer;
      for (var i = 0; i < 3; i += 1) {
        var tip = M4.apply(m, dirs[i]);
        var base = M4.apply(m, [0, 0, 0]);
        var A = this.project(base), B = this.project(tip);
        this.el("line", {
          x1: A.x, y1: A.y, x2: B.x, y2: B.y,
          stroke: colors[i],
          "stroke-width": c.width || 3.4,
          "stroke-dasharray": c.dash || null,
          "marker-end": c.marker ? "url(#" + c.marker + ")" : null,
        }, group);
        var node = this.el("text", {
          x: B.x + (c.dx === undefined ? 8 : c.dx),
          y: B.y + (c.dy === undefined ? -6 : c.dy),
          fill: colors[i],
        }, group);
        node.textContent = labels[i];
      }
      var origin = M4.apply(m, [0, 0, 0]);
      var p = this.project(origin);
      this.el("circle", { cx: p.x, cy: p.y, r: c.originR || 4, fill: "#2b3a52" }, group);
      if (c.originLabel) {
        var t = this.el("text", { x: p.x + 8, y: p.y + 16, fill: "#2b3a52" }, group);
        t.textContent = c.originLabel;
      }
      return group;
    },
    /** 绘制地面网格（xy 平面） */
    grid: function (half, step, attrs) {
      var h = half === undefined ? 3 : half;
      var s = step === undefined ? 1 : step;
      var group = this.el("g", { class: "fk-grid" });
      for (var i = -h; i <= h; i += s) {
        this.line([-h, i, 0], [h, i, 0], Object.assign({ class: "fk-grid-line" }, attrs || {}), group);
        this.line([i, -h, 0], [i, h, 0], Object.assign({ class: "fk-grid-line" }, attrs || {}), group);
      }
      return group;
    },
    /** 每次状态变化时调用的真实绘制函数 */
    setRenderer: function (fn) { this._render = fn; },
    /** 触发一次重绘 */
    render: function () {
      this.origin.x = this.baseOrigin.x;
      this.origin.y = this.baseOrigin.y;
      if (this._render) this._render(this);
      if (this.onRender) this.onRender(this);
    },
    reset: function () {
      this.state.yaw = this.defaults.yaw;
      this.state.pitch = this.defaults.pitch;
      this.state.scale = this.defaults.scale;
      this.origin.x = this.baseOrigin.x;
      this.origin.y = this.baseOrigin.y;
    },
    setAuto: function (on) {
      this.state.auto = !!on;
      if (this.state.auto && !this._frame) this._frame = requestAnimationFrame(this._tick.bind(this));
    },
    _tick: function () {
      this._frame = 0;
      if (!this.state.auto && !this.state.dragging) return;
      this.state.yaw += this.autoSpeed;
      this.render();
      if (this.state.auto) this._frame = requestAnimationFrame(this._tick.bind(this));
    },
    _enableInteraction: function () {
      var self = this;
      var svg = this.svg;
      svg.addEventListener("pointerdown", function (event) {
        if (event.button !== 0 && event.pointerType === "mouse") return;
        if (self.state.pointerId !== null) return;
        event.preventDefault();
        self.state.dragging = true;
        self.state.pointerId = event.pointerId;
        self.state.lastX = event.clientX;
        self.state.lastY = event.clientY;
        svg.classList.add("is-dragging");
        try { svg.setPointerCapture(event.pointerId); } catch (error) { /* 忽略 */ }
      });
      svg.addEventListener("pointermove", function (event) {
        if (!self.state.dragging || event.pointerId !== self.state.pointerId) return;
        event.preventDefault();
        var dx = event.clientX - self.state.lastX;
        var dy = event.clientY - self.state.lastY;
        self.state.lastX = event.clientX;
        self.state.lastY = event.clientY;
        // 水平拖动的直觉方向：向右拖动使模型向右转（观察者绕模型向左移动的等价效果）
        self.state.yaw += dx * 0.008;
        self.state.pitch = Math.max(
          self.limits.minPitch,
          Math.min(self.limits.maxPitch, self.state.pitch + dy * 0.007)
        );
        self.render();
      });
      function endDrag(event) {
        if (event && self.state.pointerId !== null && event.pointerId !== self.state.pointerId) return;
        self.state.dragging = false;
        self.state.pointerId = null;
        svg.classList.remove("is-dragging");
      }
      svg.addEventListener("pointerup", endDrag);
      svg.addEventListener("pointercancel", endDrag);
      svg.addEventListener("lostpointercapture", endDrag);
      svg.addEventListener("dragstart", function (event) { event.preventDefault(); });
      svg.addEventListener("wheel", function (event) {
        event.preventDefault();
        var factor = event.deltaY > 0 ? 0.92 : 1.08;
        self.state.scale = Math.max(
          self.limits.minScale,
          Math.min(self.limits.maxScale, self.state.scale * factor)
        );
        self.render();
      }, { passive: false });
      // 双击复位视角
      svg.addEventListener("dblclick", function () {
        self.reset();
        self.render();
      });
    },
  };

  /* ------------------------------------------------------------------ 工具 */

  /**
   * 把一组 range 控件绑定到 state，并统一在 input 时重绘。
   * @param {object[]} defs 每项 { id, key, value, format, onChange }
   * @param {object} state 目标状态对象
   * @param {function} render 刷新函数
   * @param {string} outputSuffix 输出元素的后缀，默认 "Value"
   */
  function bindRanges(defs, state, render, outputSuffix) {
    var suffix = outputSuffix || "Value";
    var sync = [];
    defs.forEach(function (def) {
      var input = document.getElementById(def.id);
      if (!input) return;
      var output = document.getElementById(def.id + suffix);
      function apply() {
        var raw = Number(input.value);
        state[def.key] = raw;
        if (output) {
          output.textContent = def.format ? def.format(raw) : String(raw);
        }
        if (def.onChange) def.onChange(raw, state);
        render();
      }
      input.value = def.value === undefined ? input.value : def.value;
      input.addEventListener("input", apply);
      sync.push({ input: input, output: output, def: def, apply: apply });
      apply();
    });
    return {
      /** 把 state 当前值写回控件 */
      refresh: function () {
        sync.forEach(function (item) {
          var value = state[item.def.key];
          if (value === undefined) return;
          item.input.value = value;
          if (item.output) {
            item.output.textContent = item.def.format ? item.def.format(value) : String(value);
          }
        });
      },
      apply: function () { sync.forEach(function (item) { item.apply(); }); },
    };
  }

  function bindToggles(defs, state, render) {
    defs.forEach(function (def) {
      var input = document.getElementById(def.id);
      if (!input) return;
      input.checked = !!state[def.key];
      input.addEventListener("change", function () {
        state[def.key] = input.checked;
        if (def.onChange) def.onChange(input.checked, state);
        render();
      });
    });
  }

  function format(value, digits) {
    var d = digits === undefined ? 2 : digits;
    var fixed = Number(value).toFixed(d);
    return fixed === "-" + (0).toFixed(d) ? (0).toFixed(d) : fixed;
  }

  /** 角度的常见显示：45.0° */
  function deg(value, digits) {
    return format(value, digits === undefined ? 1 : digits) + "°";
  }

  global.FK = {
    Vec: Vec,
    M4: M4,
    Scene: Scene,
    bindRanges: bindRanges,
    bindToggles: bindToggles,
    format: format,
    deg: deg,
    DEG: DEG,
  };
}(window));
