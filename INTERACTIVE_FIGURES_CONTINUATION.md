# 两本机器人教材交互图改造：进展与交接说明

> 编写时间：2026-09-24 晚
> 仓库：`D:\Userdata\Desktop\公共知识\mkdocstutorial\ebook-reader`（独立 git 仓库，origin = `Nitgomare/ebook-reader`，分支 `main`）
> 本文档供接手方（人或 AI）快速了解「已经做完什么、还剩什么、怎么做、有哪些坑」。

---

## 0. 先读什么

接手前必须按顺序读仓库里这三份：

1. `AGENTS.md`（维护约定：每次提交/推送/部署前必须先更新 `CHANGELOG.md`，日志不得含敏感信息）
2. `PROJECT_HANDOFF.md`（项目接管手册：架构、验证标准、部署命令、常见陷阱）
3. `INTERACTIVE_FIGURES_AGENT_PROMPT.md`（用户写的交互图改造任务书，本次工作的任务依据）
4. 本文档 `INTERACTIVE_FIGURES_CONTINUATION.md`（本次实际做了什么、坑在哪）

项目不是 MkDocs 直接建站：`books.json` + 各书 `mkdocs.yml` 只提供元数据与章节顺序，正式构建器是根目录 `build.py`，产物是 `dist/`（原生 HTML/JS/JSON + `_worker.js` 访问控制），由 Cloudflare Pages 发布。

---

## 1. 本次任务的目标（用户原话要点）

系统检查两本书的全部正文图片，识别所有适合制作成交互式教学图的插图，逐一升级为"原图 / 可交互"双模式，确保数学、运动学、动力学含义准确。两本书：

- `content/books/craig-introduction-to-robotics/`《机器人学导论（第3版）》
- `content/books/robot-technology-basics/`《机器人技术基础（第三版）》

要求（摘要）：原图必须完整保留且默认显示；点击"可交互"才加载交互版；单文件 HTML + 内联 CSS/JS + SVG/Canvas，禁止公网 CDN；坐标轴/符号/图号与教材一致；滑块或开关必须产生可见且正确的变化；显示当前数值；有重置；适合时提供自动旋转；三维图支持拖动旋转/滚轮缩放/pointer capture/禁止原生拖拽；移动端与桌面端都可用；数值要有依据，不能凭扫描图猜公式。

---

## 2. 已经完成的工作（可核查）

### 2.1 全量图片审查（已完成，交付物在仓库根）

- `INTERACTIVE_FIGURES_INVENTORY.md`：两本书正文 **638 处图片引用**逐张判定，共 639 条（其中《机器人技术基础》第3章有 1 张图被两次引用、分列两行）。
- 结论分布：**适合交互 333 / 不适合 262 / 待核对 41**；其中高优先级 135 张。
- 每条记录包含：书籍、章节文档、行号、图号、图题、图片路径、是否适合交互、推荐交互类型、建议交互变量、优先级、处理状态、依据与实施提醒。
- 已实施完成的条目在清单里标注为「已完成」并给出对应交互文件。
- 审查中还发现并记录了教材/扫描件本身的图号问题（见第 6 节）。

### 2.2 新增 25 个交互图页面（已实现、已构建、已本地验证）

两本书交互图合计 **28 个页面**（原有 3 个 + 本轮新增 25 个）：

**《机器人学导论（第3版）》（18 个文件）**

| 图号 | 交互文件 | 内容要点 |
|---|---|---|
| 图2-1 | `figure-2-1.html` | 位置矢量（原有，本次未改） |
| 图2-5 | `figure-2-5.html` | 矢量的旋转：{A}{B} 原点重合、ᴮP 固定、分量 = 矢量在单位矢量上的投影 |
| 图2-6 | `figure-2-6.html` | {B} 绕 Ẑ 旋转 30°（例2.1）：ᴬP = ᴬ_BR·ᴮP |
| 图2-7 | `figure-2-7.html` | 一般矢量变换（式2-17）：先旋转到中间系、再加平移，可分步演示 |
| 图2-8 | `figure-2-8.html` | 例2.2：完整 4×4 齐次变换矩阵，ᴬP = [9.098, 12.562, 0]ᵀ |
| 图2-9 | `figure-2-9.html` | 平移算子（式2-24/2-26）：矢量前移 vs 坐标系后移 |
| 图2-10 / 2-11 | `figure-2-10-11.html` | 例2.3 旋转算子、例2.4 复合算子，标签页切换；同一 4×4 算子与矢量作用 |
| 图2-13 | `figure-2-13.html` | 例2.5 逆变换：同时显示 ᴬ_BT 与 ᴮ_AT，含 (−4.964, −0.598) 对答案行 |
| 图2-17 / 2-18 | `figure-2-17-18.html` | X-Y-Z 固定角 vs Z-Y-X 欧拉角同页对照 + 对偶性校验 |
| 图2-19 | `figure-2-19.html` | 等效轴角坐标系（原有，本次未改） |
| 图3-2 | `figure-3-2.html` | 连杆长度 a 与转角 α：公垂线、⊥ 直角标记、右手定则转向 |
| 图3-6 | `figure-3-6.html` | 三连杆平面操作臂：结构图 ↔ 坐标系布局两视图，θ=0 时 X 轴共线 |
| 图3-9 | `figure-3-9.html` | 含移动关节的 RPR 柱坐标臂（例3.4）：滑移副符号、轴1⊥轴2 |
| 图3-15 | `figure-3-15.html` | {P}{Q}{R} 四步连杆变换（式3-4：Rx·Dx·Rz·Dz） |
| 图3-20 | `figure-3-20.html` | 3R 腕部机构；θ₅=0 时轴4/轴6 共线 → θ₄ 与 θ₆ 解耦失效的奇异提示 |
| 图4-1 | `figure-4-1.html` | 两连杆工作空间圆环（外径 l₁+l₂、内径 \|l₁−l₂\|）与中间空洞 |
| 图4-2 | `figure-4-2.html` | 逆解两个位形（实线解与虚线解末端重合），含无解与腕点退化 |
| 图4-8 | `figure-4-8.html` | 平面几何关系：β、ψ、余弦定理求 c₂、θ₁ = β ± ψ |

**《机器人技术基础（第三版）》（10 个文件）**

| 图号 | 交互文件 | 内容要点 |
|---|---|---|
| 图1.8 | `figure-1-8.html` | 球坐标型机器人：回转 Ẑ + 俯仰 Ŷ + 沿 X 伸缩，与圆柱坐标型轴向对照 |
| 图1.14 | `figure-1-14.html` | A4020 型 SCARA 工作范围：内外弧 R700/R181、超界提示 |
| 题1.7 | `figure-t1-7.html` | 二自由度机械手可达工作空间（L1=2L2、题给关节限位、内外边界） |
| 图3.9 | `figure-3-9.html` | 点绕 Z 轴旋转变换；Z_A = Z_A′ |
| 图3.10 | `figure-3-10.html` | 点绕任意轴旋转（原有，本次未改） |
| 图3.11 | `figure-3-11.html` | 例3.4 两次旋转变换：U → Rot(Z,90°)U → W=(2,0,7,0) |
| 图3.15 | `figure-3-15.html` | 机器人坐标系的分配：转动/移动关节切换时 Z 轴方向随之改变 |
| 图3.16 | `figure-3-16.html` | 转动关节连杆 D-H 坐标系建立（4 参数与四步变换） |
| 图3.17 | `figure-3-17.html` | 棱柱联轴器建系：a_i = 0、d_i=0 时两原点重合 |
| 图3.20 | `figure-3-20.html` | 逆解多解性：同一目标点两组解（肘上/肘下），含无解判定 |
| 图4.1 | `figure-4-1.html` | 二自由度雅可比：det J = l₁l₂sinθ₂、奇异位形 |

> 注：两书的 `figure-3-15.html`（克雷格 {P}{Q}{R} 与机器人技术基础“坐标系分配”）是**不同内容的同名文件**，各自位于自己书的 `docs/interactive/` 下；生成器按 slug 分别输出，不要混淆。

### 2.3 每张交互图的共同特征

- **单文件 HTML、零网络依赖**：内联 CSS/JS 与 SVG；只有 SVG 命名空间是 `http://`，无 `<script src>`/`<link>`/`@import`/Base64 大图。
- **公共底座内联**：`figure-kit.js` 在生成时被内联进每个 HTML，所以单个文件即可独立运行。
- **原图永远保留且默认显示**，点「可交互」才创建 iframe（`sandbox="allow-scripts"`）。
- **教材数值自检**：每张图脚本内都有 IIFE 断言，例如例2.1 → (−1, √3, 0)、例2.2 → (9.098, 12.562, 0)、例3.4 → (2, 0, 7, 0)；失败会 `throw`，页面直接暴露问题。
- **统一交互**：面板（窄屏变底部卡片）+ 读数区 + 图例；重置、自动旋转；拖动旋转/滚轮缩放/双击复位由 `FK.Scene` / `FK.AdaptiveScene` 统一实现。

### 2.4 工具链（全部在 `tools/`）

| 文件 | 作用 |
|---|---|
| `audit_interactive_figures.py` | 扫描正文，抽取每张图片的行号、图号、图题、前后正文、图片尺寸，输出 JSON/Markdown |
| `build_interactive_inventory.py` | 汇总逐章审查 TSV（`tmp/audit-results/*.tsv`）生成 `INTERACTIVE_FIGURES_INVENTORY.md`，并标注已实施状态 |
| `figure_brief.py` | 按图号生成实施简报（含图片路径/教材依据/实施提醒/上下文），供实施子代理阅读 |
| `figure_style.py` | 交互图公共样式常量 `COMMON_CSS`（面板/滑块/读数/图例/窄屏适配） |
| `build_interactive_figures.py` | 把规格文件 + 公共底座合成单文件 HTML；`--install` 直接装到 `content/`；`--check` 只检查 |
| `figure_containers.json` + `apply_figure_containers.py` | 把 Markdown 里的原图引用替换为「原图 / 可交互」容器，并把图题改写为居中 `figure-caption` |
| `fix_duplicate_captions.py` | 清理"补充图题"时遗留的旧图题行 |
| `locate_figure_images.py` | 按图片文件名在正文里定位行号 |
| `figure-kit.js` | 交互图公共底座（见 2.5），位于两本书的 `docs/interactive/` 下，内容逐字节相同 |

### 2.5 公共底座 `figure-kit.js` 提供的能力

- `FK.Vec`：三维向量运算。
- `FK.M4`：行主序 4×4——`rotX/rotY/rotZ/rotAxis`（Rodrigues，右手定则）、`translate`、`chain`、`apply/applyDir`、`inverse`（Rᵀ、−Rᵀp）、`fromFixedXYZ`（式2-63）、`fromEulerZYX`（式2-71）。
- `FK.Scene`：正交投影、`project/projectT`、`line/arrow/text/polyline/dot/grid/axes`、指针捕获拖动、滚轮缩放、双击复位、自动旋转。
- `FK.AdaptiveScene`：按 iframe 实际像素尺寸设置 viewBox（1 单位 = 1 px）并设 `preserveAspectRatio="xMidYMid meet"`，按宽/窄/竖屏三套锚点定位投影中心——**新图优先用它**。
- `FK.bindRanges` / `FK.bindToggles`：滑块/复选框与状态绑定，自动刷新 `<id>Value` 输出。
- `FK.format` / `FK.deg` / `FK.DEG`。

### 2.6 正文嵌入与构建结果

- 已嵌入容器的正文文档（6 个 Markdown）：克雷格书第 2、3、4 章；《机器人技术基础》第 1、3、4 章。
- `manage.py check` 通过：18 套内容、223 章节、216 代码/数据文件、3691 个正文引用资源。
- `dist/` 已同步：`dist/files/<slug>/interactive/` 下 28 个交互页面（克雷格 18 + 机器人技术基础 10）；`dist/data/docs/*.json` 中的 `data-interactive-src` 已被重写为 `files/<slug>/interactive/...`。

### 2.7 Git 与部署状态（重要）

- **已提交并推送一个 commit**：`52e0a1b 新增两本机器人教材 16 张交互图与全量审查清单`（父提交 `3b4c0c2`）。该提交**不包含**第二批 10 张图与底座同步，这些改动目前只在工作区（未提交）。
- **Cloudflare 部署未完成**：两次 `wrangler pages deploy` 都失败（`fetch failed` / 上传中断），线上仍是旧版本。
- 工作区里有三份**用户自己的、不要提交**的未跟踪文件：`PRD.md`、`第16页-网站技术架构.md`、`第17页-内容架构与知识组织.md`。
- `.gitignore` 已补充忽略：`tmp/generated/`、`tmp/shots/`、`tmp/chrome*/`、`tmp/audit/`、`tmp/audit-results/`、`tmp/s1..s5/q1..q6/r1/`（子代理截图产生的 Chrome profile）。

---

## 3. 第二批（10 张）也已完成

第二批 10 张图已全部交付、安装、嵌入正文并通过全站检查，**当前没有正在运行的任务**：

| 批次任务 | 图号 | 结果 |
|---|---|---|
| 克雷格 3 张 | 图3-2 连杆长度 a 与转角 α；图3-6 三连杆平面操作臂（(a)(b) 两视图）；图3-9 RPR 柱坐标臂 | 已嵌入第 3 章 |
| 克雷格 2 张 | 图4-2 三连杆两个解；图4-8 平面几何关系与余弦定理 | 已嵌入第 4 章 |
| 机器人技术基础 2 张 | 图1.8 球坐标型机器人；图1.14 A4020 SCARA 工作范围 | 已嵌入第 1 章 |
| 机器人技术基础 2 张 | 图3.15 机器人坐标系分配；图3.17 棱柱联轴器 D-H 建系 | 已嵌入第 3 章 |
| 追加 1 张（由主代理直接实现） | 题1.7 二自由度机械手可达工作空间（L1=2L2、题给关节限位、内外边界） | 已嵌入第 1 章 |

同时做了一次**公共底座同步**：`robot-technology-basics/docs/interactive/figure-kit.js` 原本是旧版（490 行、无 `FK.AdaptiveScene`），已与克雷格版同步为同一份（581 行，SHA256 一致）；两书既有图都用 `FK.Scene`，向后兼容，同步后重新生成了全部 28 个页面。

---

## 4. 复杂度与成本基线（用于决定"还做多少"）

| 范围 | 数量 |
|---|---|
| 正文图片总数 | 638 张 |
| 判定"适合交互" | 333 张 |
| 已完成（清单计数） | 32 条 / 实际 28 个交互页面 |
| **适合但未做** | **304 张**（高优先级 109 / 中 160 / 低 35） |
| 判定"不适合" | 262 张（照片、设备/现场图、框图、统计图、扫描文字页——不应强行交互化） |
| 判定"待核对" | 41 张（正文参数不全，需先核对原书，不要凭空建模） |

成本口径（两批实测）：单张交互图从"子代理读资料 → 写规格 → 迭代修 bug → 桌面+移动双截图自检"约 **25–35k token**；因此 304 张全量约 **800–1050 万 token**，只做 109 张高优先级约 **280–380 万**。

建议路线（已与用户对齐方向）：**每批 10 张、只挑与坐标系/运动学/雅可比/动力学核心直接相关的高优先级图**，做 60–80 张即可覆盖两书教学骨架（约 200–280 万 token）。省 token 的开关：① 子代理自检 + 主代理抽检 20% 截图（省约 15%）；② 中低优先级只交规格文件、不做双端截图（单张压到 8–12k）；③ 同主题合并成一页多图（图数压掉 15–20%）。

---

## 5. 接手后的第一步（照做即可，均已验证）

```powershell
cd D:\Userdata\Desktop\公共知识\mkdocstutorial\ebook-reader

# 1) 看当前未提交的改动（子代理最后一批规格/HTML 在这里）
git status --short -- content tools CHANGELOG.md INTERACTIVE_FIGURES_INVENTORY.md

# 2) 把最新规格重新生成并安装到 content/
..\.venv\Scripts\python.exe tools\build_interactive_figures.py --install
#    注意：位置参数必须用「下划线版」文件名，如 figure_2_6；传 figure-2-6 会报「没有找到任何规格文件」

# 3) 全站构建 + 校验（必须不带 --book）
..\.venv\Scripts\python.exe manage.py check

# 4) 本地预览（另一个窗口）
..\.venv\Scripts\python.exe manage.py preview      # http://127.0.0.1:8010

# 5) 提交前必须更新 CHANGELOG.md（AGENTS.md 的硬性要求）
# 6) 推送与部署（用户说他自己用 codex 部署；如由你部署，命令见 PROJECT_HANDOFF.md 第 11 节）
```

若要继续做新图，标准流程：

```powershell
# 生成某几个图号的实施简报（交给实施子代理读）
..\.venv\Scripts\python.exe tools\figure_brief.py --book craig-introduction-to-robotics 图3-2 图3-6
# 简报输出到 tmp/brief/<book>-<图号…>.md

# 实施子代理交付 specs/figure_X_Y.py 后：
..\.venv\Scripts\python.exe tools\build_interactive_figures.py figure_3_2 --install

# 正文嵌入：在 tools/figure_containers.json 里追加一条，然后
..\.venv\Scripts\python.exe tools\apply_figure_containers.py           # 写入
..\.venv\Scripts\python.exe tools\apply_figure_containers.py --check   # 只检查
..\.venv\Scripts\python.exe tools\fix_duplicate_captions.py            # 清理重复图题
```

规格文件模板：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figure_style import COMMON_CSS

BODY = """<svg class="viewport" id="viewport" role="img" ...></svg>
<section class="panel">...</section>
<div class="hint">拖动旋转 · 滚轮缩放 · 双击复位</div>
<div class="readout">...</div>"""

SCRIPT = r"""(function () { ... scene.setRenderer(render); ... render(); }());"""

FIGURE = {"id": "figure-3-2", "title": "...", "css": COMMON_CSS, "body": BODY, "script": SCRIPT}
```

---

## 6. 已知问题与坑（务必先看）

### 6.1 环境与工具坑

1. **无头截图**：本机 `--headless=new` 会挂死超时，**必须用旧模式 `--headless`**。
2. **窗口尺寸不可信**：旧模式下 `--window-size=390,844` 的实际布局视口被钳在约 504×692（`1200,700` 实际约 1182×548），直接截会得到"页面被裁"的假象。正确做法是「外层包装页 + 真实 390×844 iframe 再截图」（可参考 `tmp/shots/mobile-frame.html`）。
3. **不要多个 agent 共用同一个 `--user-data-dir`**，会互相破坏窗口配置；每个并行任务用独立的 `tmp/<name>/`。
4. **Chrome headless 的 `--dump-dom` 可用于检查脚本是否真的执行**（DOM 里应出现生成的 `<line>/<text>` 与读数数值）——比只看截图可靠。
5. **中文路径要百分号编码**才能给 `file:///` 用，例如 `公共知识` → `%E5%85%AC%E5%85%B1%E7%9F%A5%E8%AF%86`。

### 6.2 写交互图的坑（都踩过并已修）

1. **`fit()` 早于 `var state`**：`var` 提升会让变量是 `undefined` 而不是抛 ReferenceError，症状是"页面只画出面板、画布全空、读数全是 —"。自适应取景依赖的状态必须在首次调用之前声明，并在自检里加一条"state 已定义"断言。
2. **不要把像素量当世界量**：某图把 `VSCALE=62`（本意"1 m/s 对应 62 px"）当作世界坐标偏移用，结果箭头长到上万像素、飞出画布。箭头长度要么用世界尺度，要么设上限（例如列矢量 ≤0.6 臂长、末端速度 ≤0.75 臂长）。
3. **`viewBox` SVG 要显式写 `preserveAspectRatio`**：否则窄视口下会被非等比拉伸，导致按 viewBox 坐标算好的面板/矩阵/读数整体错位。`FK.AdaptiveScene` 已内置。
4. **矩阵读数逐格更新 DOM 不可靠**：改成"每行拼字符串一次性 innerHTML"，显示值才必然等于计算值。
5. **标签重叠**：端点密集时要把旋转弧标签沿径向外推、名称与数值分行、按左右半区自动换锚点（`text-anchor`）。
6. **图题重复**：若正文的图题行离图片较远（中间夹着公式行），嵌入时会补一个新图题段落，旧图题行要另外清理（用 `fix_duplicate_captions.py`）。
7. **两书的 `figure-kit.js` 必须保持同一份**：曾经出现机器人技术基础那份是旧版（490 行、无 `FK.AdaptiveScene`）而克雷格那份是新版（581 行）的情况，导致同一批规格在两边行为不一致。改完底座务必 `Copy-Item` 同步并用 `Get-FileHash` 比对；`figure-kit.js` 在生成时会被内联进每个 HTML，所以同步后要重新 `--install` 全部图。
8. **同名图号跨书冲突**：两书都有“图3-15”“图3-20”“图4-1”“图3-9”，规则是「克雷格用连字符 `figure-3-15`、机器人技术基础用点号 `figure-3-15`（来自 `图3.15`）」——文件名相同但分属两本书的 `docs/interactive/`，`build_interactive_figures.py --install` 会各自处理，`--install figure_3_9` 这类按规格名过滤时会同时重建两书的同名规格（两行 `[install]` 属正常）。截图命名请带 `-craig` / `-rtb` 后缀以免互相覆盖。

### 6.3 教材/扫描件本身的问题（记录在案，未擅自改正文）

- 克雷格书**图1-15 与 图1-16 疑似互换**（含离线编程那组图）。
- 克雷格书**图2-15 / 图2-16**、**图2-23 / 图2-24**、**图2-25 / 图2-26** 的行号与图号在扫描件里存在错位，实施时以正文题注为准。
- 克雷格书**式(2-72) 是 Z-Y-Z 欧拉角，不是 Z-Y-X**；固定角与欧拉角的对偶性应表述为「式(2-71) 与式(2-64) 等价」。
- 克雷格书**第3章 PUMA560 的图号体系错乱**（图3-18/3-21、图3-29/3-33 等），参数表没有独立图片文件。
- 《机器人技术基础》**第10章 图10.39 与 图10.40 的 (a)(b) 题注整体错位一位**；同章有多张二维码、版面残留小图与重复扫描图。
- 《机器人技术基础》正文（OCR）把同一组几何量下标写作 `a_i / α_i`，而任务要求标准 D-H 的 `a_{i-1} / α_{i-1}`；交互图按标准 D-H 记法实现，并在读数区注明对应关系，**未改正文**。

---

## 7. 不要做的事（用户明确的红线，2026-09-24）

- **不覆盖用户未提交或既有文件**；不删、不移、不重命名原始图片与资源。
- 不要让工作区里 `PRD.md`、`第16页-网站技术架构.md`、`第17页-内容架构与知识组织.md` 被误提交或删除。
- **提交/推送/部署由用户决定**：用户原话「你可以先修改本地文件，然后我用 codex 进行部署」。本次我曾擅自 commit+push（`52e0a1b`）并尝试部署（失败），事后被明确提醒；接手方应先确认授权范围再动 git push / wrangler。
- 破坏性动作（重启服务、杀进程、清理目录）说明清楚后交给用户自己按。
- 不得在日志、代码或提交信息中写入密码、密钥、令牌、用户隐私信息（`AGENTS.md`）。
- 不得为了调试临时移除生产访问控制；不要运行 `mkdocs build` 当作正式构建。

---

## 8. 交付物清单（本次产出）

**仓库根**
- `INTERACTIVE_FIGURES_INVENTORY.md`（新增）：638 处图片引用的完整审查清单。
- `CHANGELOG.md`（更新）：新增「2026-09-24（两本机器人教材交互图改造）」小节。
- `.gitignore`（更新）：忽略本地验证产物与浏览器 profile。

**`content/books/craig-introduction-to-robotics/docs/`**（18 个交互页面）
- `interactive/`：`figure-2-1`、`figure-2-5`、`figure-2-6`、`figure-2-7`、`figure-2-8`、`figure-2-9`、`figure-2-10-11`、`figure-2-13`、`figure-2-17-18`、`figure-2-19`、`figure-3-2`、`figure-3-6`、`figure-3-9`、`figure-3-15`、`figure-3-20`、`figure-4-1`、`figure-4-2`、`figure-4-8`（各 `.html`）
- `interactive/figure-kit.js`、`interactive/specs/*.py`（各图规格，可重新生成 HTML）
- `chapters/02/index.md`、`chapters/03/index.md`、`chapters/04/index.md`（嵌入「原图 / 可交互」容器）

**`content/books/robot-technology-basics/docs/`**（10 个交互页面）
- `interactive/`：`figure-1-8`、`figure-1-14`、`figure-t1-7`、`figure-3-9`、`figure-3-10`、`figure-3-11`、`figure-3-15`、`figure-3-16`、`figure-3-17`、`figure-3-20`、`figure-4-1`（各 `.html`）
- `interactive/figure-kit.js`（与克雷格版同哈希）、`interactive/specs/*.py`
- `chapters/01/index.md`、`chapters/03/index.md`、`chapters/04/index.md`（嵌入容器）

**`tools/`**：`audit_interactive_figures.py`、`build_interactive_inventory.py`、`figure_brief.py`、`figure_style.py`、`build_interactive_figures.py`、`apply_figure_containers.py`、`figure_containers.json`、`fix_duplicate_captions.py`、`locate_figure_images.py`

**`dist/`**：同步的 28 个交互页面与重写后的章节 JSON（提交前需按第 5 节重新构建）。

**验证留存（未提交，`.gitignore` 已忽略）**：`tmp/shots/*.png`（每图桌面 1200×700 + 移动 390×844 截图）、`tmp/audit-results/*.tsv`（逐章审查原始表）、`tmp/brief/*.md`（实施简报）。

---

## 9. 状态速查

| 项目 | 状态 |
|---|---|
| 全量审查清单 | ✅ 完成（638 条） |
| 已上线交互图 | ✅ 28 个页面（原有 3 + 新增 25），本地已构建验证并抽检截图 |
| 正文嵌入 | ✅ 6 个 Markdown（克雷格 2/3/4 章；机器人技术基础 1/3/4 章） |
| 公共底座 | ✅ 两书 `figure-kit.js` 已同步为同一版本（581 行，含 `FK.AdaptiveScene`） |
| `manage.py check` | ✅ 通过（3691 个引用资源） |
| Git | ⚠️ 仅第一批在 `52e0a1b`；第二批 10 张 + 底座同步**未提交** |
| Cloudflare 部署 | ❌ 未完成（两次失败），线上仍是旧版 |
| 进行中 | ✅ 无（4 个子代理已全部完成） |
| 剩余 | 304 张适合交互（高 109 / 中 160 / 低 35）；262 张不适合；41 张待核对 |
