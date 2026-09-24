"""交互图公共样式与标签常量。

各图规格文件通过 COMMON_CSS / AXIS_LABELS 复用统一视觉语言：
- 藏青 + 精准蓝为主色，浅底为主，不使用大面积渐变与玻璃拟态。
- 面板在桌面端位于左上角，移动端自动展开为全宽底部卡片，避免遮挡核心图形。
- 全部尺寸用 px / vh，不依赖网络字体。
"""

COMMON_CSS = """
:root {
  color-scheme: light;
  --ink: #14213d;
  --muted: #65748b;
  --line: #d9e2ef;
  --surface: rgba(255, 255, 255, 0.94);
  --blue: #2563eb;
  --blue-dark: #174ea6;
  --blue-soft: #eaf2ff;
  --red: #d93025;
  --green: #12944f;
  --violet: #7c3aed;
  --orange: #c26a10;
  --cyan: #0e7490;
}
* { box-sizing: border-box; }
html, body { width: 100%; height: 100%; margin: 0; }
body {
  overflow: hidden;
  color: var(--ink);
  background: linear-gradient(160deg, #f8fbff 0%, #eef4fb 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC",
    "Microsoft YaHei", Arial, sans-serif;
  -webkit-text-size-adjust: 100%;
}
button, input, select { font: inherit; }
.app {
  position: relative;
  width: 100vw;
  height: 100vh;
  min-height: 460px;
  overflow: hidden;
  user-select: none;
  -webkit-user-select: none;
}
.viewport {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  cursor: grab;
  touch-action: none;
  -webkit-user-drag: none;
  overscroll-behavior: contain;
}
.viewport.is-dragging { cursor: grabbing; }
.fk-grid-line { stroke: #e2eaf5; stroke-width: 1; }
.fk-axis { stroke-width: 3.2; }
.fk-axis-label, .fk-point-label, .fk-vec-label, .fk-origin-label {
  font-weight: 700;
  paint-order: stroke;
  stroke: #f7fafe;
  stroke-width: 5px;
  stroke-linejoin: round;
}
.fk-origin-label { font-size: 15px; fill: #475569; }
.fk-vec-line { stroke-width: 4.4; fill: none; }
.fk-projection { stroke-width: 2.2; stroke-dasharray: 7 6; fill: none; }
.fk-arc { fill: none; stroke-width: 2.6; stroke-dasharray: 6 5; }
.fk-point { stroke: #fff; stroke-width: 2.6; }

.panel {
  position: absolute;
  top: 16px;
  left: 16px;
  width: min(304px, calc(100% - 32px));
  max-height: calc(100% - 32px);
  overflow: auto;
  padding: 15px 17px 14px;
  border: 1px solid rgba(30, 64, 175, 0.14);
  border-radius: 14px;
  background: var(--surface);
  box-shadow: 0 16px 36px rgba(30, 64, 175, 0.14);
}
.panel-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
.panel h1 { margin: 0; font-size: 15px; line-height: 1.4; }
.panel .subtitle { margin: 5px 0 12px; color: var(--muted); font-size: 11.5px; line-height: 1.55; }
.reset {
  flex: none;
  padding: 5px 10px;
  border: 1px solid #bfd2ef;
  border-radius: 7px;
  color: var(--blue-dark);
  background: #fff;
  cursor: pointer;
}
.reset:hover { background: var(--blue-soft); }
.control { margin-top: 10px; }
.control-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
}
.control label { color: #42526a; font-size: 12.5px; }
.control output {
  color: var(--blue-dark);
  font: 700 12.5px ui-monospace, SFMono-Regular, Consolas, monospace;
}
input[type="range"] {
  width: 100%;
  height: 4px;
  margin: 8px 0 2px;
  border-radius: 999px;
  outline: none;
  background: #dbe5f1;
  appearance: none;
}
input[type="range"]::-webkit-slider-thumb {
  width: 16px; height: 16px;
  border: 3px solid #fff;
  border-radius: 50%;
  background: var(--blue);
  box-shadow: 0 2px 7px rgba(37, 99, 235, 0.42);
  cursor: pointer;
  appearance: none;
}
input[type="range"]::-moz-range-thumb {
  width: 12px; height: 12px;
  border: 3px solid #fff;
  border-radius: 50%;
  background: var(--blue);
  cursor: pointer;
}
.options { display: flex; flex-wrap: wrap; gap: 8px 14px; margin-top: 12px; }
.options label { display: inline-flex; align-items: center; gap: 6px; color: #4a5a72; font-size: 12px; cursor: pointer; }
.options input { accent-color: var(--blue); }
.legend { display: flex; flex-wrap: wrap; gap: 6px 12px; margin-top: 11px; padding-top: 10px; border-top: 1px dashed var(--line); color: #5b6a80; font-size: 11.5px; }
.legend span { display: inline-flex; align-items: center; gap: 5px; }
.legend i { display: inline-block; width: 14px; height: 3px; border-radius: 2px; }
.legend i.dot { width: 9px; height: 9px; border-radius: 50%; }

.readout {
  position: absolute;
  right: 16px;
  bottom: 16px;
  max-width: min(460px, calc(100% - 32px));
  padding: 10px 13px;
  border: 1px solid rgba(30, 64, 175, 0.12);
  border-radius: 10px;
  color: #3d4c63;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 10px 26px rgba(30, 64, 175, 0.09);
  font: 15px/1.6 "Cambria Math", "Times New Roman", serif;
}
.readout .row { white-space: nowrap; }
.readout strong { color: var(--blue-dark); font-family: inherit; }
.readout .small { font-size: 13px; color: #5b6a80; }
.hint {
  position: absolute;
  right: 16px;
  top: 16px;
  padding: 7px 11px;
  border-radius: 999px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.82);
  font-size: 11px;
}
.tabs { display: flex; gap: 6px; margin-bottom: 10px; }
.tabs button {
  flex: 1;
  padding: 6px 4px;
  border: 1px solid #cfdcf0;
  border-radius: 8px;
  color: #45566f;
  background: #fff;
  font-size: 12px;
  cursor: pointer;
}
.tabs button.is-active { border-color: var(--blue); color: #fff; background: var(--blue); }

@media (max-width: 720px) {
  .app { min-height: 540px; }
  .panel {
    top: auto;
    bottom: 8px;
    left: 8px;
    width: calc(100% - 16px);
    max-height: 54%;
    padding: 12px 14px;
    border-radius: 12px;
  }
  .panel .subtitle { display: none; }
  .readout { top: 8px; right: 8px; bottom: auto; font-size: 13px; max-width: calc(100% - 16px); }
  .hint { display: none; }
  .legend { margin-top: 8px; padding-top: 8px; }
}
"""

# 教材符号与配色约定：X 红、Y 蓝、Z 绿；旋转轴/角标用紫色
AXIS_LABELS = {
    "A": {"labels": ["X\u0302\u2090", "Y\u0302\u2090", "Z\u0302\u2090"], "colors": ["#d93025", "#2563eb", "#12944f"]},
}
