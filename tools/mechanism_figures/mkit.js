/*! mechanism-kit.js — 机械原理交互图的实体辅助（基于 figure-kit.js 的正交投影）
 *
 * 只用 SVG 路径堆出"有厚度的零件"：每块零件都是沿 y 方向挤出的棱柱，
 * 面按深度排序后用四档明暗上色，因此视角一转，侧面自然变暗、前脸保持受光。
 * 与本目录其它交互图共用 figure-kit.js / figure-layout.js 的交互（拖动、滚轮、双击）。
 */
window.MK = (function () {
  "use strict";

  function r2(v) { return Math.round(v * 100) / 100; }

  function make(scene, pal) {
    var P = {
      steel: { hi: "#fbfdff", base: "#c6d3e8", mid: "#9db0cd", dark: "#7186a8", line: "#5d708c" },
      slate: { hi: "#f2f6fc", base: "#bcc9de", mid: "#94a4bd", dark: "#6d7d97", line: "#5a6a83" },
      brass: { hi: "#fdf3d9", base: "#e8c98c", mid: "#c49f5c", dark: "#997a42", line: "#7d6334" },
      teal: { hi: "#eefafb", base: "#b2d6db", mid: "#87b4ba", dark: "#5f8d94", line: "#4e757c" },
      graphite: { hi: "#e9ebf0", base: "#c0c6d1", mid: "#969ea9", dark: "#747c87", line: "#5e6671" },
      ink: { hi: "#9aa6b8", base: "#5b6879", mid: "#48535f", dark: "#39424c", line: "#2f373f" }
    };
    var tone = function (name) { return P[name] || pal[name] || P.steel; };

    function polyD(pts3) {
      var d = "";
      for (var i = 0; i < pts3.length; i += 1) {
        var q = scene.project(pts3[i]);
        d += (i ? " L" : "M") + r2(q.x) + "," + r2(q.y);
      }
      return d + " Z";
    }

    function signedArea(pts3) {
      var a = 0, proj = [];
      for (var i = 0; i < pts3.length; i += 1) proj.push(scene.project(pts3[i]));
      for (var j = 0; j < proj.length; j += 1) {
        var p = proj[j], q = proj[(j + 1) % proj.length];
        a += p.x * q.y - q.x * p.y;
      }
      return a / 2;
    }

    function depthOf(pts3) {
      var d = 0;
      for (var i = 0; i < pts3.length; i += 1) d += scene.project(pts3[i]).depth;
      return d / pts3.length;
    }

    /** 一组面：先画远的，再按投影朝向取明暗（正面受光、侧面压暗） */
    function faces(list, layer) {
      for (var i = 0; i < list.length; i += 1) list[i].depth = depthOf(list[i].pts);
      list.sort(function (a, b) { return b.depth - a.depth; });
      for (var j = 0; j < list.length; j += 1) {
        var f = list[j];
        var fill = f.fill || (signedArea(f.pts) > 0 ? f.tone.base : f.tone.dark);
        scene.el("path", {
          d: polyD(f.pts),
          fill: fill,
          stroke: f.tone.line,
          "stroke-width": f.width === undefined ? 0.85 : f.width,
          "stroke-linejoin": "round",
          opacity: f.opacity === undefined ? 1 : f.opacity
        }, layer);
      }
    }

    /** 把 XZ 平面上的多边形沿 y 方向挤出成棱柱 */
    function extrude(xz, y0, thick, t, layer, opt) {
      opt = opt || {};
      var n = xz.length, front = [], back = [], list = [], i;
      for (i = 0; i < n; i += 1) {
        front.push([xz[i][0], y0, xz[i][1]]);
        back.push([xz[i][0], y0 + thick, xz[i][1]]);
      }
      var backRev = back.slice().reverse();
      list.push({ pts: backRev, fill: t.mid, tone: t });
      for (i = 0; i < n; i += 1) {
        var k = (i + 1) % n;
        list.push({ pts: [front[i], front[k], back[k], back[i]], fill: null, tone: t });
      }
      list.push({ pts: front, fill: t.base, tone: t });
      faces(list, layer);
      if (opt.edge) {
        scene.line([xz[0][0], y0, xz[0][1]], [xz[0][0], y0, xz[0][1]], {}, layer);
      }
    }

    /** 圆头长条（链杆）在 XZ 平面上的外轮廓 */
    function stadium(p1, p2, halfW, seg) {
      seg = seg || 9;
      var a = Math.atan2(p2[1] - p1[1], p2[0] - p1[0]);
      var pts = [], i, t;
      for (i = 0; i <= seg; i += 1) {
        t = a + Math.PI / 2 + Math.PI * (i / seg);
        pts.push([p1[0] + halfW * Math.cos(t), p1[1] + halfW * Math.sin(t)]);
      }
      for (i = 0; i <= seg; i += 1) {
        t = a - Math.PI / 2 + Math.PI * (i / seg);
        pts.push([p2[0] + halfW * Math.cos(t), p2[1] + halfW * Math.sin(t)]);
      }
      return pts;
    }

    /** 链杆：p1/p2 为 XZ 坐标；y 为零件所在深度，thick 为厚度 */
    function bar(p1, p2, halfW, y, thick, toneName, layer) {
      var t = tone(toneName);
      extrude(stadium(p1, p2, halfW), y, thick, t, layer);
      // 前脸高光：沿杆身上缘的一条窄亮边，让金属有受光感
      var a = Math.atan2(p2[1] - p1[1], p2[0] - p1[0]);
      var nx = Math.cos(a + Math.PI / 2), nz = Math.sin(a + Math.PI / 2);
      var off = halfW * 0.5;
      scene.line(
        [p1[0] + nx * off, y, p1[1] + nz * off],
        [p2[0] + nx * off, y, p2[1] + nz * off],
        { stroke: t.hi, "stroke-width": 2, "stroke-linecap": "round", opacity: 0.85 }, layer
      );
    }

    /** 销轴：沿 y 方向的圆柱，带倒角环与中心孔 */
    function pin(p, y, radius, thick, toneName, layer) {
      var t = tone(toneName || "slate");
      var n = 14, front = [], back = [], list = [], i, ang;
      for (i = 0; i < n; i += 1) {
        ang = (i / n) * Math.PI * 2;
        front.push([p[0] + radius * Math.cos(ang), y, p[1] + radius * Math.sin(ang)]);
        back.push([p[0] + radius * Math.cos(ang), y + thick, p[1] + radius * Math.sin(ang)]);
      }
      list.push({ pts: back.slice().reverse(), fill: t.mid, tone: t });
      for (i = 0; i < n; i += 1) {
        var k = (i + 1) % n;
        list.push({ pts: [front[i], front[k], back[k], back[i]], fill: null, tone: t });
      }
      faces(list, layer);
      scene.el("path", { d: polyD(front), fill: t.base, stroke: t.line, "stroke-width": 0.9 }, layer);
      scene.el("path", { d: polyD(front), fill: "none", stroke: t.hi, "stroke-width": 1.5, opacity: 0.7 }, layer);
      scene.el("circle", {
        cx: scene.project([p[0], y, p[1]]).x, cy: scene.project([p[0], y, p[1]]).y,
        r: radius * 0.26, fill: t.dark, stroke: t.line, "stroke-width": 0.6
      }, layer);
    }

    /** 长方体：底座、立柱、滑座、导轨座都用它 */
    function box(center, size, toneName, layer, opt) {
      opt = opt || {};
      var t = tone(toneName || "graphite");
      var cx = center[0], cy = center[1], cz = center[2];
      var hx = size[0] / 2, hy = size[1] / 2, hz = size[2] / 2;
      var v = [];
      for (var sx = -1; sx <= 1; sx += 2) {
        for (var sy = -1; sy <= 1; sy += 2) {
          for (var sz = -1; sz <= 1; sz += 2) v.push([cx + sx * hx, cy + sy * hy, cz + sz * hz]);
        }
      }
      // 顶点顺序：index = ((sx>0)*4 + (sy>0)*2 + (sz>0))
      function at(ix, iy, iz) { return v[(ix > 0 ? 4 : 0) + (iy > 0 ? 2 : 0) + (iz > 0 ? 1 : 0)]; }
      var list = [
        { pts: [at(-1, -1, -1), at(-1, 1, -1), at(-1, 1, 1), at(-1, -1, 1)], tone: t }, // x-
        { pts: [at(1, -1, -1), at(1, -1, 1), at(1, 1, 1), at(1, 1, -1)], tone: t },     // x+
        { pts: [at(-1, -1, -1), at(-1, -1, 1), at(1, -1, 1), at(1, -1, -1)], tone: t }, // y-
        { pts: [at(-1, 1, -1), at(1, 1, -1), at(1, 1, 1), at(-1, 1, 1)], tone: t },     // y+
        { pts: [at(-1, -1, 1), at(-1, 1, 1), at(1, 1, 1), at(1, -1, 1)], tone: t },     // z+
        { pts: [at(-1, -1, -1), at(1, -1, -1), at(1, 1, -1), at(-1, 1, -1)], tone: t }  // z-
      ];
      if (opt.topTone) list[4].fill = t.hi;
      faces(list, layer);
      var top = opt.highlightTop === false ? null : null;
      if (top) return top;
    }

    /** 水平底板：一台机构的工作台，前沿带刻度、四角带螺钉、前立面贴铭牌 */
    function bench(x0, x1, y0, y1, thick, layer, opt) {
      opt = opt || {};
      box([(x0 + x1) / 2, (y0 + y1) / 2, -thick / 2], [x1 - x0, y1 - y0, thick], "graphite", layer);
      // 台面刻度：只画前沿一条窄带，避免糊住台面
      for (var x = x0 + 0.25; x < x1 - 0.1; x += 0.25) {
        var major = Math.abs(x - Math.round(x)) < 1e-6;
        scene.line([x, y0 + 0.05, 0.001], [x, y0 + (major ? 0.26 : 0.15), 0.001],
          { stroke: major ? "#7f8794" : "#9aa1ad", "stroke-width": major ? 1.2 : 0.8 }, layer);
      }
      // 角螺钉（十字槽）
      var corners = [[x0 + 0.24, y1 - 0.24], [x1 - 0.24, y1 - 0.24], [x0 + 0.24, y0 + 0.24], [x1 - 0.24, y0 + 0.24]];
      for (var i = 0; i < corners.length; i += 1) {
        var c = corners[i], p = scene.project([c[0], c[1], 0]);
        scene.el("circle", { cx: p.x, cy: p.y, r: 4.8, fill: "#aeb5bf", stroke: "#7d848f", "stroke-width": 0.9 }, layer);
        scene.el("line", { x1: p.x - 3.2, y1: p.y, x2: p.x + 3.2, y2: p.y, stroke: "#666d78", "stroke-width": 1.3 }, layer);
        scene.el("line", { x1: p.x, y1: p.y - 3.2, x2: p.x, y2: p.y + 3.2, stroke: "#666d78", "stroke-width": 1.3 }, layer);
      }
      // 铭牌贴在前立面正中，不压台面刻度
      if (opt.label) {
        var lx = opt.labelX === undefined ? (x0 + x1) / 2 : opt.labelX;
        var pw = Math.max(0.56, (opt.label.length * 0.085));
        box([lx, y0 - 0.004, -thick * 0.5], [pw, 0.016, thick * 0.46], "brass", layer);
        var q = scene.project([lx, y0 - 0.05, -thick * 0.5]);
        var node = scene.el("text", {
          x: q.x, y: q.y + 3, "text-anchor": "middle",
          "font-size": 11.5, "font-family": "ui-monospace, Consolas, monospace",
          fill: "#4a3a1c", "letter-spacing": "0.5"
        }, layer);
        node.textContent = opt.label;
      }
    }

    function label(p, text, dx, dy, layer, opt) {
      opt = opt || {};
      return scene.text(p, text, {
        "font-size": opt.size || 15,
        "font-style": "italic",
        "font-family": "Georgia, 'Times New Roman', serif",
        fill: opt.fill || "#33415a",
        "text-anchor": "middle",
        "paint-order": "stroke",
        stroke: "#ffffff",
        "stroke-width": 3.2,
        "stroke-linejoin": "round"
      }, dx || 0, dy || 0, layer);
    }

    /** 虚线轨迹 */
    function trace(points, color, layer) {
      scene.polyline(points, {
        fill: "none", stroke: color, "stroke-width": 1.6,
        "stroke-dasharray": "6 5", "stroke-linecap": "round", opacity: 0.9
      }, layer);
    }

    return {
      pal: P, tone: tone, faces: faces, extrude: extrude, stadium: stadium,
      bar: bar, pin: pin, box: box, bench: bench, label: label, trace: trace
    };
  }

  return { make: make };
}());
