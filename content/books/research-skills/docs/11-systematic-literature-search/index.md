# 系统性文献检索操作手册

> **课程信息**
>
> - 内容制作：肖鑫
> - 配套视频：[前往 Bilibili 观看](https://www.bilibili.com/video/BV1iwYr6ZEyo/)

---

## 一、建立关键词表

### 1.1 中文关键词（根据你的专业方向选择）

| 概念组 | 核心词 | 同义词或相关词 |
|---|---|---|
| 研究对象 | 风电 | 风力发电、风电机组、风力发电机组、风电场、海上风电、陆上风电 |
| 数据或方法 | 大数据 | 风电数据、数据分析、数据挖掘、SCADA数据、人工智能、机器学习、深度学习、数字孪生 |
| 功率问题 | 功率预测 | 风电功率预测、风电出力预测、短期预测、超短期预测、功率波动 |
| 运维问题 | 故障诊断 | 状态监测、健康评估、异常检测、预测性维护、剩余寿命预测 |
| 系统问题 | 并网调度 | 风电消纳、电力系统调度、新能源并网、风储协同 |

### 1.2 英文关键词（根据你的专业方向选择）

| 概念组 | 核心词 | 同义词或相关词 |
|---|---|---|
| 研究对象 | wind power | wind energy, wind turbine, wind farm, offshore wind, onshore wind |
| 数据或方法 | big data | data analytics, data mining, SCADA data, artificial intelligence, machine learning, deep learning, digital twin |
| 功率问题 | power forecasting | wind power forecasting, wind power prediction, wind generation forecasting, short-term forecasting |
| 运维问题 | fault diagnosis | fault detection, condition monitoring, health assessment, predictive maintenance, remaining useful life |
| 系统问题 | grid integration | power system dispatch, renewable energy integration, wind-storage coordination |

### 1.3 关键词组合规则

- 同一概念组内的同义词用 `OR` 连接；
- 不同概念组之间用 `AND` 连接；
- 固定词组使用英文双引号；
- 先用较宽检索式了解文献规模，再逐步增加限制条件；
- 每次只改变一个条件，便于解释结果变化。

![](image/1.png)

---

## 二、选择检索网站

### 2.1 中文数据库

| 网站 | 地址 | 主要用途 |
|---|---|---|
| 中国知网 | https://www.cnki.net/ | 中文期刊、学位论文、核心期刊 |
| 万方数据 | https://www.wanfangdata.com.cn/ | 中文期刊、学位论文、科技报告 |
| 维普 | https://www.cqvip.com/ | 中文期刊补充检索 |
| 国家哲学社会科学文献中心 | https://www.ncpssd.org/ | 能源政策、产业、管理类文献 |

![](image/2.png)



![](image/3.png)



![](image/4.png)



### 2.2 英文数据库

| 网站 | 地址 | 主要用途 |
|---|---|---|
| Web of Science | https://www.webofscience.com/ | SCI、ESCI、引文追踪 |
| Scopus | https://www.scopus.com/ | 工程、能源、计算机综合检索 |
| ScienceDirect | https://www.sciencedirect.com/ | Elsevier能源和工程期刊全文 |
| IEEE Xplore | https://ieeexplore.ieee.org/ | 电力系统、控制、人工智能、传感器 |
| SpringerLink | https://link.springer.com/ | 能源、数据科学、智能制造 |
| Wiley Online Library | https://onlinelibrary.wiley.com/ | 风能、可靠性、能源工程 |
| Google Scholar | https://scholar.google.com/ | 补充检索和引用追踪 |
| Crossref | https://search.crossref.org/ | 核对DOI和书目信息 |
| OpenAlex | https://openalex.org/ | 免费查询论文和引用关系 |

![](image/5.png)



![](image/6.png)

![](image/7.png)

### 2.3 行业和标准网站

| 网站 | 地址 | 主要用途 |
|---|---|---|
| 国家能源局 | https://www.nea.gov.cn/ | 风电政策、装机和行业数据 |
| 全球风能理事会 | https://gwec.net/ | 全球风电行业报告 |
| 中国可再生能源学会风能专业委员会 | http://www.cwea.org.cn/ | 中国风电行业统计和报告 |
| 国家标准全文公开系统 | https://openstd.samr.gov.cn/ | 查询风电国家标准和行业术语 |

> 学术论文主要来自知网、Web of Science、Scopus、IEEE Xplore等数据库；行业报告和标准用于补充背景，不与学术论文混为一类。

---

## 三、正式检索：先做测试，再做最终检索

### 3.1 测试检索

目的：检查关键词是否合理，不立即确定最终文献数量。

先使用宽检索式：

#### 中文测试检索式

```text
(风电 OR 风力发电 OR 风电机组 OR 风电场)
AND
(大数据 OR 数据分析 OR 机器学习 OR 深度学习)
```

#### 英文测试检索式

```text
("wind power" OR "wind energy" OR "wind turbine" OR "wind farm")
AND
("big data" OR "data analytics" OR "machine learning" OR "deep learning")
```

如果结果太多：增加“功率预测”“故障诊断”“predictive maintenance”等应用词。  
如果结果太少：删除一个应用词，或将检索字段从“标题”放宽为“主题/标题摘要关键词”。

### 3.2 最终检索式示例

#### 风电功率预测

```text
("wind power" OR "wind energy" OR "wind farm")
AND
("machine learning" OR "deep learning" OR "big data")
AND
("power forecasting" OR "power prediction")
```

#### 风电机组故障诊断

```text
("wind turbine" OR "wind farm")
AND
("fault diagnosis" OR "fault detection" OR "condition monitoring" OR "predictive maintenance")
AND
("machine learning" OR "deep learning" OR "artificial intelligence" OR "big data")
```

---

## 四、如何导出文献

### 4.1 推荐格式

优先使用：用zotero管理文献  

### 4.2 如果下载不了文献

可以用学校的VPN下载，用机构登录，登录学校自己的账号

![](image/8.png)



![](image/9.png)

### 4.3 推荐文件夹结构

```text
风电大数据文献检索
01_原始检索结果
02_去重后文献
03_标题摘要筛选
04_全文筛选
05_最终纳入文献
06_排除文献
07_检索截图
08_文献提取表
```

### 4.4 推荐文件命名

```text
数据库_主题_日期
```

示例：

```text
CNKI_WindPowerBigData_2026-08-25.ris
WOS_WindTurbineFaultDiagnosis_2026-08-25.bib
Scopus_WindPowerForecasting_2026-08-25.csv
```

---

## 五、文献去重

推荐工具：Zotero

1. 先按DOI自动去重；
2. 再按论文题名去重；
3. 检查第一作者和发表年份；
4. 检查中文题名与英文题名是否为同一研究；
5. 人工确认后再删除。

---

## 六、文献筛选

### 6.1 纳入标准

- 研究对象是风电机组、风电场、海上风电或风电并网系统；
- 使用风电运行数据、SCADA数据、气象数据或电力数据；
- 研究功率预测、故障诊断、状态监测、智能运维或并网调度；
- 使用大数据、机器学习、深度学习、人工智能或数字孪生；
- 论文信息完整，能够获得题名、作者、年份和摘要；
- 属于综述、正式期刊、会议、学位论文、或权威报告。

### 6.2 排除标准

- 研究对象不是风电；
- 仅在背景部分提及风电；
- 实际研究的是光伏、火电或核电；
- 没有使用或分析风电数据；
- 新闻、广告、博客或商业宣传材料；
- 重复文献；
- 无法判断研究内容且无法获得全文。



---

## 七、检索结果统计

| 阶段 | 文献数量 |
|---|---:|
| 中文数据库初始结果 |  |
| 英文数据库初始结果 |  |
| 合并后总数 |  |
| 删除重复文献 |  |
| 标题摘要筛选后 |  |
| 全文筛选后 |  |
| 最终纳入文献 |  |
