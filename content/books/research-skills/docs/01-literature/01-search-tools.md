# 文献检索工具

文献的查找与下载属于科研基本技能，上手难度不高。遇到暂时找不到或下载不下来的文献时，不要局限于单一数据库，可以通过更换检索平台、调整关键词、检索 DOI、查找预印本或使用其他渠道继续尝试。

## 核心文献数据库

### 大模型与人工智能

- **[arXiv（Computer Science）](https://arxiv.org/)**：必看的预印本平台。大模型领域的前沿技术，例如最新时序基座模型、各类 LLM 架构及其工程应用，通常会第一时间在 arXiv 公开，是紧跟前沿的重要平台。

- **[IEEE Xplore](https://ieeexplore.ieee.org/)**：收录大量机器学习、大模型在电力系统、智能电网、控制工程和信号处理中的应用研究，也包含计算机视觉、数据挖掘等方向的重要会议论文。

- **[ACM Digital Library](https://dl.acm.org/)**：计算机领域的重要数据库。可重点关注数据挖掘、知识发现、搜索与推荐等方向的会议和期刊，其中的方法可迁移到风电多源时序数据挖掘、极端天气预测和设备状态分析中。

- **[OpenReview](https://openreview.net/)**：适合查找 ICLR、NeurIPS 等会议的论文、评审意见、作者回复和补充材料。

### 风电、电气与能源工程

- **[Elsevier ScienceDirect](https://www.sciencedirect.com/)**：能源领域期刊的重要来源，包含 *Renewable Energy*、*Energy*、*Applied Energy* 等期刊，适合查找风电预测、风机控制、状态监测和能源系统优化研究。

- **[Wiley Online Library](https://onlinelibrary.wiley.com/)**：包含风电领域的专业期刊，例如 *Wind Energy*，主要关注风力发电设备、空气动力学、结构载荷和风电场控制。

- **[SpringerLink](https://link.springer.com/)**：收录复杂系统控制、可再生能源并网、气象学、风速预测、机器学习等领域的期刊、会议论文和专业图书。

- **[中国知网（CNKI）](https://www.cnki.net/)**：中文电力与电气工程文献的重要检索平台。可重点检索《中国电机工程学报》《电网技术》《电力系统自动化》等期刊，了解国内风电集群并网、新能源消纳、智能运维及大模型在电网中的工程应用。

### 综合性引文索引数据库

- **[Web of Science](https://www.webofscience.com/)**：用于检索 SCIE、SSCI 等核心文献，适合系统检索、被引关系分析和研究趋势分析。

- **[Scopus](https://www.scopus.com/)**：爱思唯尔旗下的全学科引文数据库，收录范围较广，对人工智能、计算机科学和工程领域的会议论文覆盖较好。

- **[Google Scholar](https://scholar.google.com/)**：适合快速检索论文、作者主页、被引文献及同一篇文章的不同版本。当出版商页面无法阅读时，可以尝试通过“所有版本”查找其他可访问版本。

## 检索关键词与检索式

### 关键词拆分

不要直接把完整研究题目复制到检索框。应将研究问题拆分为若干关键词组。

以“面向风电功率预测的时序大模型”为例：

| 关键词类型 | 中文关键词 | 英文关键词 |
|---|---|---|
| 研究对象 | 风电、风速、风电场 | wind power, wind speed, wind farm |
| 研究任务 | 功率预测、短期预测 | power forecasting, short-term forecasting |
| 技术方法 | 大模型、Transformer、基座模型 | large language model, Transformer, foundation model |
| 数据类型 | 时序数据、多变量数据、SCADA | time series, multivariate data, SCADA |
| 泛化问题 | 迁移学习、少样本、跨风场 | transfer learning, few-shot learning, cross-farm |

### 布尔逻辑

常见逻辑符号包括：

| 运算符 | 含义 | 示例 |
|---|---|---|
| `AND` | 同时满足多个条件 | `"wind power" AND Transformer` |
| `OR` | 包含任意一个同义词 | `"wind power" OR "wind energy"` |
| `NOT` | 排除无关主题 | `"wind speed" NOT offshore` |
| `" "` | 精确匹配词组 | `"foundation model"` |
| `*` | 匹配不同词形 | `forecast*` |

### 检索式示例

```text
("wind power" OR "wind speed" OR "wind farm")
AND
("large language model" OR "LLM" OR "Transformer"
OR "foundation model" OR "time series foundation model"
OR "time-series model")
```

该检索式用于锁定同时包含“风电、风速或风电场”与“大模型、Transformer、基座模型或时序大模型”的相关论文。

!!! tip "双引号的作用"

    大模型、时序预测、风电等专有词组应使用双引号进行精确匹配。否则数据库可能将词组拆分后独立检索，产生大量无关结果。

## 文献脉络追踪

### 正向追踪：参考文献

找到领域内的核心论文后，查看其参考文献，重点寻找：

- 该方法的理论来源；
- 反复出现的经典论文；
- 数据集和评价指标的原始出处；
- 作者用于对比的基础方法；
- 研究方向中的重要综述。

### 逆向追踪：被引文献

在论文出版页面、Web of Science、Scopus 或 Google Scholar 中查看“被引情况”，了解：

- 后续研究如何使用该方法；
- 是否出现改进版本；
- 是否已经应用到新的工程场景；
- 原论文提出的问题是否已经解决；
- 当前研究前沿发展到了什么阶段。

### 文献图谱工具

- **[Connected Papers](https://www.connectedpapers.com/)**：输入一篇核心文献后，自动生成相关论文图谱。
- **[ResearchRabbit](https://www.researchrabbit.ai/)**：适合追踪作者、论文、主题和引用关系。
- **[Semantic Scholar](https://www.semanticscholar.org/)**：可用于发现相关论文、重要引用和研究脉络。

图谱工具适合快速扩展阅读，但不能替代正式数据库检索。

## 获取文献全文

当出版商页面无法直接下载 PDF 时，可以依次尝试以下渠道。

### 学校数据库与 WebVPN

优先使用学校图书馆已经购买的数据库资源。

常见流程：

1. 登录学校图书馆网站；
2. 在校外使用学校 WebVPN 或统一身份认证；
3. 进入对应数据库；
4. 搜索论文标题或 DOI；
5. 下载 PDF 全文。

对于电气、能源和人工智能方向，学校一般会购买部分 IEEE、Elsevier、Springer、Wiley、Web of Science 和知网资源。

### Google Scholar“所有版本”

在 Google Scholar 中搜索完整论文标题：

1. 查看搜索结果右侧是否存在 `[PDF]` 链接；
2. 点击结果下方的“所有版本”或 `All versions`；
3. 检查作者主页、机构知识库或预印本平台中的版本；
4. 对比标题、作者和年份，确认是否为同一篇论文。

### Unpaywall

**[Unpaywall](https://unpaywall.org/)** 用于查找论文的开放获取版本。

安装浏览器插件后，访问论文出版页面时，如果存在开放版本，页面右侧通常会显示绿色解锁图标。点击后可以访问作者公开的预印本、接收稿或机构知识库版本。

### 作者主页、课题组主页和代码仓库

部分作者会在以下位置公开论文：

- 作者个人主页；
- 课题组主页；
- 学校机构知识库；
- arXiv；
- ResearchGate；
- GitHub 项目主页；
- 论文配套代码仓库；
- 会议或项目官方网站。

建议直接搜索：

```text
论文完整标题 PDF
```

或：

```text
论文完整标题 作者姓名
```

### DOI 检索与 Sci-Hub

无论论文来自 IEEE、Wiley、Elsevier 还是 Springer，摘要页面一般都能找到以 `10.` 开头的 DOI。

例如：

```text
10.1109/TSTE.2025.xxxxxx
```

可以复制 DOI，并在可访问的 Sci-Hub 镜像入口中进行检索，例如：

```text
https://sci-hub.box/
```

如果 DOI 无法检索，也可以尝试使用完整论文标题。

!!! warning "内部使用说明"

    镜像入口可能随时间变化，也可能存在网络、版权和信息安全风险。不要在来源不明的网站输入学校统一身份认证账号或个人重要密码。

### 其他内部渠道

在合法合规和确保账号安全的前提下，也可以根据实际情况尝试：

- 课题组已有的文献库；
- 导师或师兄师姐保存的论文；
- 跨校文献互助；
- 使用其他高校朋友的 WebVPN 资源；
- 图书馆馆际互借或文献传递；
- 通过邮件联系通讯作者索取论文；
- 购买临时数据库镜像入口或文献下载服务。

!!! warning "账号与文件安全"

    不要购买来历不明的学校账号，不要在公共设备上保存 WebVPN 密码，不要下载可疑的可执行程序，也不要将未公开的内部数据上传到陌生网站。

## 推荐检索与下载流程

```text
明确研究问题
    ↓
拆分中英文关键词
    ↓
在 Google Scholar 或综合数据库初步检索
    ↓
在专业数据库补充检索
    ↓
确定综述、经典和最新核心论文
    ↓
追踪参考文献与被引文献
    ↓
优先通过学校数据库下载
    ↓
尝试公开版本、作者主页或其他渠道
    ↓
导入 Zotero 统一管理
```

---

*由郑圭晟整理*
