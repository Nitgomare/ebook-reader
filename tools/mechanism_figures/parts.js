/* 零件库：等轴测小机械的底座、轴承立柱、销轴与链杆。
   依赖 figure-kit.js 的 scene.project 与 mkit.js 的挤压/着色，目标按 anatomy 的做工：
   每个零件都坐在另一个零件上，分面明暗四档，线收在零件边缘。 */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";

  function el(tag, attrs, parent) {
    var node = document.createElementNS(NS, tag);
    for (var key in attrs) {
      if (Object.prototype.hasOwnProperty.call(attrs, key)) node.setAttribute(key, attrs[key]);
    }
    if (parent) parent.appendChild(node);
    return node;
  }

  function make(scene, mk) {
    var pal = mk.pal;

    function linkBar(p, q, halfW, y, thick, toneName, layer, opt) {
      opt = opt || {};
      var tone = mk.tone(toneName);
      mk.bar(p, q, halfW, y, thick, toneName, layer);
      // 两端圆眼：孔里露出销轴，说明是铰接而不是焊死
      [p, q].forEach(function (c) {
        var ring = [];
        for (var i = 0; i <= 22; i++) {
          var a = (i / 22) * Math.PI * 2;
          ring.push([c[0] + Math.cos(a) * halfW * 0.62, y + thick / 2 + 0.004, c[1] + Math.sin(a) * halfW * 0.62]);
        }
        var d = "";
        ring.forEach(function (v, idx) {
          var s2 = scene.project(v);
          d += (idx ? "L" : "M") + s2.x.toFixed(2) + " " + s2.y.toFixed(2);
        });
        el("path", { d: d + "Z", fill: tone.dark, stroke: tone.line, "stroke-width": 0.8 }, layer);
      });
      // 上缘一道受光，让杆件有金属厚度
      if (opt.highlight !== false) {
        var up = [];
        for (var m = 0; m <= 14; m++) {
          var t2 = m / 14;
          up.push([
            p[0] + (q[0] - p[0]) * t2 + (q[1] - p[1]) / Math.hypot(q[0] - p[0], q[1] - p[1]) * halfW * 0.82,
            y + thick / 2 + 0.006,
            p[1] + (q[1] - p[1]) * t2 - (q[0] - p[0]) / Math.hypot(q[0] - p[0], q[1] - p[1]) * halfW * 0.82
          ]);
        }
        var dh = "";
        up.forEach(function (v, idx2) {
          var s3 = scene.project(v);
          dh += (idx2 ? "L" : "M") + s3.x.toFixed(2) + " " + s3.y.toFixed(2);
        });
        el("path", { d: dh, fill: "none", stroke: tone.hi, "stroke-width": 1.5, "stroke-linecap": "round", opacity: 0.85 }, layer);
      }
    }

    function cylY(cx, cz, radius, y0, y1, toneName, layer, opt) {
      opt = opt || {};
      var centre = (y0 + y1) / 2;
      var thick = Math.abs(y1 - y0);
      mk.pin([cx, cz], centre, radius, thick, toneName, layer);
      // 两端挡圈
      [y0, y1].forEach(function (yy) {
        var tone = mk.tone(toneName);
        var pts = [];
        for (var i = 0; i <= 20; i++) {
          var a = (i / 20) * Math.PI * 2;
          pts.push([cx + Math.cos(a) * radius * 0.55, yy, cz + Math.sin(a) * radius * 0.55]);
        }
        var d = "";
        pts.forEach(function (v, idx) {
          var s2 = scene.project(v);
          d += (idx ? "L" : "M") + s2.x.toFixed(2) + " " + s2.y.toFixed(2);
        });
        el("path", { d: d + "Z", fill: "none", stroke: tone.dark, "stroke-width": 1.1 }, layer);
      });
    }

    // 轴承立柱：地脚板 → 立柱 → 轴承座（沿 y 的圆柱）→ 压盖螺栓
    function pedestal(x, zTop, yBoss, opt) {
      opt = opt || {};
      var base = opt.layer || null;
      var foot = 0.46;
      mk.box([x, yBoss, (opt.z0 || 0) + 0.05], [foot, foot * 1.5, 0.10], "graphite", base, { bevel: 0.03 });
      mk.box([x, yBoss, ((opt.z0 || 0) + 0.10 + zTop - 0.22) / 2], [foot * 0.62, foot * 0.86, zTop - 0.32 - (opt.z0 || 0)], "graphite", base, { bevel: 0.03 });
      // 立柱与轴承座之间的肋
      mk.box([x, yBoss, zTop - 0.24], [foot * 0.5, foot * 1.2, 0.16], "graphite", base, { bevel: 0.02 });
      cylY(x, zTop, 0.20, yBoss - 0.19, yBoss + 0.19, "steel", base, { seg: 22 });
      // 压盖螺栓：两颗小圆点落在座顶
      [-0.10, 0.10].forEach(function (dy) {
        var p = scene.project([x, yBoss + dy, zTop + 0.21]);
        el("circle", { cx: p.x, cy: p.y, r: 2.1, fill: pal.graphite.dark, stroke: pal.graphite.line, "stroke-width": 0.7 }, base);
      });
    }

    // 底座：台面 + 地脚 + 螺钉 + 刻度尺 + 铭牌
    function bench(x0, x1, y0, y1, thick, layer, opt) {
      opt = opt || {};
      mk.box([(x0 + x1) / 2, (y0 + y1) / 2, -thick / 2], [x1 - x0, y1 - y0, thick], "graphite", layer, { bevel: 0.05 });
      // 台面倒角与四周倒棱，让台面有厚度而不像纸片
      mk.box([(x0 + x1) / 2, (y0 + y1) / 2, 0.012], [x1 - x0 - 0.10, y1 - y0 - 0.10, 0.028], "graphite", layer, { bevel: 0.03 });
      var feet = [[x0 + 0.20, y0 + 0.20], [x1 - 0.20, y0 + 0.20], [x0 + 0.20, y1 - 0.20], [x1 - 0.20, y1 - 0.20]];
      feet.forEach(function (f) {
        mk.box([f[0], f[1], -thick - 0.055], [0.30, 0.30, 0.11], "graphite", layer, { bevel: 0.02 });
        mk.box([f[0], f[1], -thick - 0.115], [0.20, 0.20, 0.02], "ink", layer, { bevel: 0.01 });
      });
      feet.forEach(function (f) {
        var p = scene.project([f[0], f[1], 0.03]);
        el("circle", { cx: p.x, cy: p.y, r: 2.6, fill: "none", stroke: pal.graphite.mid, "stroke-width": 1 }, layer);
        el("circle", { cx: p.x, cy: p.y, r: 1.1, fill: pal.graphite.dark }, layer);
      });
      // 前沿刻度尺：每 5 小格一长格
      var ticks = [];
      var step = (x1 - x0) / 20;
      for (var i = 0; i <= 20; i++) {
        var x = x0 + step * i;
        var long = i % 5 === 0;
        ticks.push({ a: [x, y1 - 0.02], b: [x, y1 - (long ? 0.13 : 0.07)] });
      }
      ticks.forEach(function (t) {
        var p1 = scene.project([t.a[0], t.a[1], 0.031]);
        var p2 = scene.project([t.b[0], t.b[1], 0.031]);
        el("line", { x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y, stroke: pal.graphite.mid, "stroke-width": 1 }, layer);
      });
      // 铭牌：黄铜片上压字
      var label = opt.label || "";
      if (label) {
        var lx = opt.labelX === undefined ? (x0 + 0.55) : x0 + opt.labelX;
        var w = Math.max(0.62, label.length * 0.088);
        mk.box([lx + w / 2, y1 - 0.30, 0.036], [w, 0.20, 0.018], "brass", layer, { bevel: 0.012 });
        var p = scene.project([lx + w / 2, y1 - 0.30, 0.046]);
        var text = el("text", {
          x: p.x, y: p.y + 3.2, "text-anchor": "middle",
          "font-size": 10.5, "font-family": "ui-monospace,SFMono-Regular,Menlo,monospace",
          "letter-spacing": 0.6, fill: "#4a3a1c"
        }, layer);
        text.textContent = label;
      }
    }

    return { bench: bench, pedestal: pedestal, linkBar: linkBar, cylY: cylY, el: el };
  }

  window.MP = { make: make, el: el };
})();
