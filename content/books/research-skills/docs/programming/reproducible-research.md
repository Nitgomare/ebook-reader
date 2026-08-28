---
title: 实验复现与项目整理
---

# 实验复现与项目整理：让结果经得起复查

“在我电脑上能跑”不是科研复现。合格的项目应该让同门在一台新电脑上，从原始数据和一条命令得到论文中的表格与图片。

## 推荐目录

```text
rotor-health/
├─ README.md                 # 问题、数据、安装、运行、结果
├─ pyproject.toml            # 依赖与工具配置
├─ configs/
│  └─ baseline.yaml          # 窗长、频带、模型参数
├─ data/
│  ├─ raw/                   # 原始数据，只读且通常不进 Git
│  ├─ interim/               # 可重新生成的中间数据
│  └─ processed/             # 特征表与数据字典
├─ src/rotor_health/
│  ├─ io.py                  # 读取与输入检查
│  ├─ signal.py              # 滤波、分窗、FFT
│  ├─ features.py            # 特征提取
│  └─ modeling.py            # 划分、训练、评估
├─ scripts/
│  ├─ make_features.py
│  └─ train_baseline.py
├─ tests/
│  ├─ test_signal.py
│  └─ test_features.py
└─ outputs/                  # 自动生成的图表与指标
```

原则是：Notebook 用于探索，`src/` 中的函数用于可信计算，`scripts/` 负责把步骤串起来。不要让最终结果依赖“按某个神秘顺序运行 17 个单元格”。

## 从一条命令开始设计

README 应给出最短复现路径：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python scripts/make_features.py --config configs/baseline.yaml
python scripts/train_baseline.py --config configs/baseline.yaml
```

每条命令应满足：重复运行不会破坏原始数据；缺少输入时立即报出清楚错误；产物写到固定目录；配置与日志能说明结果如何得到。

## 一张实验记录至少回答这些问题

| 类别 | 必须记录 |
|---|---|
| 数据 | 数据版本、设备/试验 ID、排除规则、样本与独立组数量 |
| 信号处理 | 单位、采样率、滤波器、窗长、重叠、窗函数 |
| 划分 | 分组变量、随机种子、训练/验证/测试比例 |
| 模型 | 特征列表、预处理、算法、超参数、软件版本 |
| 结果 | 主指标、每类指标、置信区间、失败样本、运行时间 |
| 代码 | Git commit、配置文件、执行命令、产物路径 |

推荐给每次实验保存一行结构化结果，而不是只把数字写在聊天记录里：

```csv
run_id,git_commit,data_version,split_seed,model,macro_f1,notes
2026-08-09-001,a1b2c3d,v2,42,logistic,0.781,grouped-by-bearing
```

## 三个最小测试最划算

```python
import numpy as np

def test_rms_of_constant_signal():
    x = np.full(128, 3.0)
    assert np.isclose(rms(x), 3.0)

def test_frequency_axis_matches_rfft():
    x = np.zeros(1024)
    assert frequency_axis(x, fs=2048).shape == np.fft.rfft(x).shape

def test_group_split_has_no_overlap():
    train_groups = {"run_01", "run_02"}
    test_groups = {"run_03"}
    assert train_groups.isdisjoint(test_groups)
```

它们不追求高覆盖率，而是保护三种最危险的错误：数值定义错、数组长度错、数据泄漏。

## 随机种子不是全部

```python
SEED = 42
rng = np.random.default_rng(SEED)
model = RandomForestClassifier(random_state=SEED, n_jobs=1)
```

固定种子能帮助调试，但不能替代稳健性分析。最终结果应在多个合理划分或多个设备上重复，并报告均值和变化范围。深度学习还可能受到 GPU 算子与库版本影响，README 应记录硬件与版本。

## 防止数据泄漏的检查顺序

1. 先按设备/试验划分，再进行任何由数据估计的变换。
2. 标准化、PCA、特征选择和缺失值填充只在训练集 `fit`。
3. 超参数只通过训练集内部交叉验证选择。
4. 测试集只用于最终一次报告，不据此修改特征。
5. 检查文件哈希、时间戳或相似度，排除重复数据。

使用 `Pipeline` 可以把前两点固化在代码里：

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=2_000, random_state=42),
)
pipeline.fit(X_train, y_train)
```

## 论文结果的最低证据链

<div class="workflow-flow workflow-flow--wide" aria-label="论文结果证据链">
  <span>原始数据 + 数据字典</span>
  <span>版本化处理配置</span>
  <span>可测试的特征函数</span>
  <span>无组间泄漏的划分</span>
  <span>简单基线 + 候选模型</span>
  <span>指标 + 置信区间 + 失败案例</span>
  <span>脚本生成论文图表</span>
</div>

链条中的任何一步靠手工操作，复现成本都会急剧上升。

## 提交前检查

- [ ] 新环境能按 README 安装并运行。
- [ ] 原始数据没有被脚本覆盖。
- [ ] 配置中写明单位、采样率、窗长和分组字段。
- [ ] 训练与测试的设备/试验 ID 无交集。
- [ ] 表格数字和图片由脚本自动生成。
- [ ] 报告简单基线，不只报告最复杂模型。
- [ ] 保存失败案例，并对异常高分主动排查泄漏。
- [ ] 记录 Git commit、依赖版本、随机种子和运行命令。

回到 [学习中心](index.md)，根据当前薄弱环节补读 Python、机器学习或深度学习教材。
