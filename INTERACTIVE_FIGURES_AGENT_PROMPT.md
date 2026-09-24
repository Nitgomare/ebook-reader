# 两本机器人教材交互图改造：Agent 工作提示词

下面的提示词可以直接复制给新的 AI Agent。它要求 Agent 完整审查两本书，并把适合动态演示的教材插图升级为“原图 / 可交互”形式。

---

## 可直接复制的提示词

你现在接管本地项目：

```text
D:\Userdata\Desktop\公共知识\mkdocstutorial\ebook-reader
```

你的任务是：系统检查以下两本书中的全部正文图片，识别所有适合制作成交互式教学图的插图，并将它们逐一升级为“原图 / 可交互”双模式，同时确保数学、运动学、动力学和控制含义准确。

目标书籍：

1. `content/books/craig-introduction-to-robotics/`  
   《机器人学导论（第3版）》
2. `content/books/robot-technology-basics/`  
   《机器人技术基础（第三版）》

开始任何工作前，必须完整阅读：

```text
AGENTS.md
PROJECT_HANDOFF.md
README.md
CHANGELOG.md
```

不要把本项目误认为 MkDocs 直接建站项目。每本书的 `mkdocs.yml` 只提供导航数据，正式构建由根目录 `build.py` 完成。

### 一、总体目标

对两本书的所有章节执行完整图片审查，不允许只凭文件名抽查。结合以下信息判断图片含义：

- 图片前后的正文。
- 图题和图号。
- 相关公式。
- 本节标题和知识目标。
- 图片本身的几何结构。

把适合动态表达的插图制作成交互式 HTML，并嵌入对应图的位置。原始图片必须完整保留，默认先显示原图，用户点击“可交互”后才加载交互版本。

最终效果应延续现有三个示范：

```text
《机器人学导论》第2章 图2-1
《机器人学导论》第2章 图2-19
《机器人技术基础》第3章 图3.10
```

### 二、先建立完整清单，再实施

先扫描两本书全部 Markdown 和图片，创建：

```text
INTERACTIVE_FIGURES_INVENTORY.md
```

清单至少包含：

| 书籍 | 章节 | 小节 | 图号 | 图题 | 图片路径 | 是否适合交互 | 推荐类型 | 交互变量 | 优先级 | 处理状态 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

“是否适合交互”必须给出明确结论，并说明依据。不要为了追求数量，把所有图片机械地改成交互图。

### 三、优先改造的图片类型

以下图片通常适合交互化：

1. 坐标系、位置矢量、方向矢量和姿态关系。
2. 绕固定轴或任意轴旋转、平移、复合变换。
3. 欧拉角、固定角、轴角、旋转矩阵和齐次变换。
4. D-H 坐标系、连杆长度、偏距、扭角和关节角。
5. 正运动学、逆运动学和多解构型。
6. 二连杆、三连杆及空间机械臂运动范围。
7. 速度、角速度、雅可比矩阵和奇异位形。
8. 力、力矩、惯性、质心及动力学关系。
9. 轨迹插值、速度曲线、加速度曲线和路径规划。
10. 控制系统框图中可通过参数观察响应的模型。
11. 传感器或执行器中结构简化后仍能准确表达原理的运动示意图。

下列内容通常不应强行交互化：

- 人物、设备或工业现场照片。
- 只承担装饰作用的图片。
- 复杂机械剖面图，但无法在合理成本内准确建模。
- 表格、书影、版权页和扫描文字页。
- 交互后不能增加理解、只会重复原图的图片。
- 无法从正文可靠判断几何关系或参数含义的图片。

遇到高价值但含义确实不明确的图，记录为“待核对”，不要擅自发明模型。

### 四、交互图设计要求

每个交互图必须服务于对应知识点，不是泛化的三维装饰。

至少满足：

- 与教材的符号、轴向、图号和变量保持一致。
- 明确区分固定坐标系、运动坐标系、旋转前状态和旋转后状态。
- 滑块或开关改变后必须出现明显且正确的视觉变化。
- 对角度、长度、关节变量或时间参数显示当前数值。
- 使用颜色图例区分对象，但不能只依赖颜色表达含义。
- 需要时显示轨迹、投影、分量、角度弧、坐标标签或辅助线。
- 提供“重置”；适合时提供“自动旋转视角”。
- 交互控件不要遮挡核心图形。
- 字号在 iframe 内清晰可读。

对于真实三维关系：

- 鼠标拖动或触屏拖动旋转视角。
- 滚轮缩放。
- 必要时允许平移，但不能与页面滚动冲突。
- 水平拖动方向必须符合用户直觉。
- 使用 pointer capture，拖出图形区域后仍保持旋转。
- 设置 `touch-action: none`。
- 禁止文本选择和浏览器原生图片拖拽。

### 五、技术选型

优先级如下：

1. 单文件 HTML + 内联 CSS/JavaScript + SVG。
2. 单文件 HTML + Canvas。
3. 只有在真正需要三维网格、光照、相机或复杂模型时才使用 Three.js。

禁止直接依赖公网 CDN。交互图必须在没有公网资源的情况下正常运行。若必须使用 Three.js：

- 将确定版本的依赖文件保存到仓库。
- 使用相对路径。
- 确保 iframe 的 `sandbox="allow-scripts"` 下可运行。
- 记录依赖版本与许可证。

不要使用 Python 生成静态图片冒充交互图。

### 六、文件组织与命名

每本书自己的交互文件放在：

```text
content/books/<book-slug>/docs/interactive/
```

命名规则：

```text
figure-<章号>-<图序号>.html
```

示例：

```text
figure-2-19.html
figure-3-10.html
```

不要删除、移动或重命名原始图片。

### 七、正文嵌入模板

把原 Markdown 图片替换为以下容器，但容器内部仍引用原图片：

```html
<div class="interactive-figure"
     data-interactive-src="../../interactive/figure-X-X.html"
     data-interactive-title="图X-X 标题">
  <div class="interactive-figure-toolbar" role="group" aria-label="图X-X显示方式">
    <button type="button" class="is-active"
            data-figure-mode="original" aria-pressed="true">原图</button>
    <button type="button"
            data-figure-mode="interactive" aria-pressed="false">可交互</button>
  </div>
  <div class="interactive-figure-pane" data-figure-pane="original">
    <img src="../../images/原图片文件名.jpg" alt="准确的原图说明">
  </div>
  <div class="interactive-figure-pane" data-figure-pane="interactive" hidden>
    <div class="interactive-figure-loading">正在载入交互模型…</div>
  </div>
</div>

<p class="figure-caption">图X-X 标题（原图与交互示例）</p>
```

保持相对路径相对于当前 Markdown 文件正确。不要在路径中加入查询参数，因为当前构建器会丢弃资源 URL 的 query，只保留 fragment。

### 八、数学与物理正确性

每个交互图都必须以正文公式为依据进行自检：

- 旋转使用正确的右手定则。
- 轴角旋转应使用 Rodrigues 公式或等价旋转矩阵。
- 坐标系变换要区分主动旋转与被动旋转。
- 欧拉角必须严格遵守教材给出的旋转次序。
- D-H 参数要区分标准 D-H 与改进 D-H。
- 连杆长度、偏距、扭角和关节角不得互换。
- 速度和力矩方向要与坐标系一致。
- 轨迹、速度和加速度曲线要满足边界条件。

不要根据扫描图外观猜测公式。若正文和原图疑似矛盾，在清单中记录，并优先保持教材正文定义。

### 九、性能要求

- 默认只加载原图。
- 只有点击“可交互”才创建 iframe。
- 单个 HTML 不应包含巨大的 Base64 图片或模型。
- 动画使用 `requestAnimationFrame`。
- 页面不可见或关闭自动旋转后停止无意义动画。
- 不要一次性在章节加载多个正在运行的 Three.js 场景。
- 移动端降低不必要的像素密度和复杂度。

### 十、分批实施方式

按以下顺序处理，避免一次改动过大：

1. 完成全书图片清单。
2. 先处理“高优先级”坐标变换和运动学图。
3. 再处理轨迹、速度、动力学和控制图。
4. 每一章完成后运行构建和视觉检查。
5. 两本书全部完成后再进行一次全站完整回归。

每批都要在清单中更新状态：

```text
未开始 / 制作中 / 已完成 / 不适合 / 待核对
```

不要在没有清单和语义判断的情况下批量替换所有 `<img>`。

### 十一、验证要求

每个交互图至少验证：

- 原图按钮正常。
- 可交互按钮正常。
- 首次切换能加载 iframe。
- 再次切换不会产生重复 iframe。
- 每个滑块和复选框有效。
- 重置有效。
- 水平和垂直拖动方向合理。
- 鼠标拖出图形区域仍能完成拖动。
- 不会选中文字或拖动浏览器图片。
- 滚轮缩放不会导致页面异常滚动。
- 触屏操作可用。
- 1200×700 桌面窗口正常。
- 390×844 移动端窗口正常。
- 原图、标题、图题和后续正文顺序正确。
- 页面没有横向溢出。

每章完成后运行：

```powershell
..\.venv\Scripts\python.exe manage.py check
```

最终发布前必须再次运行完整检查，不能使用 `--book` 代替全站检查。

### 十二、视觉检查

启动本地站点：

```powershell
..\.venv\Scripts\python.exe manage.py preview
```

使用浏览器实际打开章节；不能只检查独立 HTML。需要确认外层“原图 / 可交互”按钮、iframe 高度、图题和正文衔接都正确。

可以使用 Chrome 无界面截图辅助检查：

```powershell
& 'C:\Program Files\Google\Chrome\Application\chrome.exe' `
  --headless --disable-gpu --no-sandbox `
  --window-size=1200,700 `
  --screenshot='C:\Users\18066\AppData\Local\Temp\interactive-check.png' `
  'http://127.0.0.1:8010/目标地址'
```

### 十三、Git 与变更安全

工作区内可能存在用户未提交文件。开始前执行：

```powershell
git status --short
```

要求：

- 不删除或覆盖无关文件。
- 不使用 `git reset --hard` 或 `git clean -fd`。
- 只暂存与交互图任务相关的文件。
- 每次提交、推送、部署前更新 `CHANGELOG.md`。
- 提交信息使用清晰中文。
- `dist/` 必须随源文件一起提交。
- 不在提交中写入密码、密钥或用户信息。

### 十四、最终交付物

任务结束时必须提供：

1. `INTERACTIVE_FIGURES_INVENTORY.md` 完整审查清单。
2. 所有新增交互 HTML 源文件。
3. 两本书对应 Markdown 的“原图 / 可交互”容器。
4. 同步更新的 `dist/`。
5. 更新后的 `CHANGELOG.md`。
6. 全站检查结果。
7. 桌面端和移动端视觉验证结果。
8. Git 提交号。
9. Cloudflare Pages 部署地址和部署状态。
10. 一份最终汇总表，列出：书名、章节、小节、图号、交互类型和直接访问链接。

### 十五、提交与部署

完成全部验证后：

```powershell
git push origin main
```

部署：

```powershell
npx --yes wrangler@4.37.0 pages deploy dist `
  --project-name research-knowledge-hub `
  --branch main
```

部署后检查：

```powershell
npx --yes wrangler@4.37.0 pages deployment list `
  --project-name research-knowledge-hub
```

确认最新 Production 部署的 Source 等于本次提交号。如果生产站要求登录，未认证请求返回的 200 页面可能只是登录页，不能据此判断交互资源内容是否正确。

你拥有在上述明确范围内自主分析、修改、构建、提交、推送和部署的权限。除非出现教材语义无法可靠判断、需要新增外部依赖、需要修改认证系统或发现用户文件冲突，否则不要中途等待确认；持续完成两本书的全部审查、实施、验证和交付。

---

## 使用说明

建议把上面的整段提示词交给能够直接读取同一工作区的 Agent。若只希望它先做方案、不修改文件，请把最后一段改成：

> 目前只完成全量审查清单和改造方案，不修改任何源文件、不提交、不推送、不部署；等待我审核清单后再实施。

