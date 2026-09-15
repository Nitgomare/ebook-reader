# 风电 SCADA 数据分析

本课程以风电机组 SCADA 数据为对象，讲解数据检查、清洗、探索性分析、特征关系判断以及线性回归和 KNN 回归建模，并通过对比实验理解不同方法的适用条件。

> **配套资源**
>
> - [观看风电 SCADA 数据分析教学视频（哔哩哔哩）](https://www.bilibili.com/video/BV1VCbG6YEp5/)
>
> **内容制作：庄锦良**

> 本案例基于风电场 SCADA（数据采集与监视控制）系统采集到的传感器数据，完成一整套**从数据清洗 → 探索性数据分析(EDA) → 特征工程 → 线性回归 / KNN 回归建模 → 模型评估与残差分析**的完整流程。
>
> 核心目标：利用 **风速、发电机转速、桨距角** 三个特征，预测风机的**发电功率**。

**学习目标：**

1. 掌握用 pandas 进行数据清洗（去重、按建模列去空值、物理边界过滤）
2. 掌握 matplotlib / seaborn 面向对象绘图（折线图、柱状图、散点图、箱线图、热力图）
3. 掌握 `pd.cut()` 数据分箱 + `groupby().mean()` 分组统计
4. 掌握线性回归建模流程（数据划分、标准化、K 折交叉验证、还原原始空间业务公式）
5. 掌握 KNN 回归 + `GridSearchCV` 网格搜索调参
6. 掌握模型结果可视化与残差分析

---

## 一、环境准备与数据加载

### 【实操】导入工具包

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 解决图表中文显示问题（Mac 用户请把 'SimHei' 改为 'Arial Unicode MS'）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False   # 解决负号 '-' 显示为方块的问题
```

### 【实操】读取数据

> ⚠️ **数据说明（复现必读）**：本案例使用 `风电scada练习数据.xlsx`（约 13.9 MB，共 **285716 行 × 5 列**：`风速、风向、功率、桨距角、发电机转速`，全部 float64、无缺失值）。原始路径为 `C:\Users\username\Desktop\风电scada练习数据.xlsx`，复现时请替换成你自己电脑上该文件的真实路径。

```python
source = r'C:\Users\username\Desktop\风电scada练习数据.xlsx'
df = pd.read_excel(source)

print('前五行数据')
print(df.head())
print(f'表格的形状{df.shape}')
print(df.info())
```

**运行结果（前五行 + 数据概况）：**

```
前五行数据
     风速    风向      功率  桨距角    发电机转速
0  6.80  2.28  1114.6  0.0  1532.31
1  6.81 -1.69  1108.3  0.0  1534.09
2  6.97 -3.10  1138.7  0.0  1535.36
3  6.97 -5.48  1121.6  0.0  1537.48
4  6.77 -4.23  1145.7  0.0  1537.91
表格的形状(285716, 5)
```

可以看到数据共 **285716 行 × 5 列**，字段为 `风速、风向、功率、桨距角、发电机转速`，全部 float64、无缺失值。

---

## 二、数据清洗

### 【掌握】为什么要清洗数据

原始 SCADA 数据通常存在三类"脏数据"：

1. **重复值** —— 传感器重复上报
2. **缺失值** —— 某一时刻某个传感器没有采集到
3. **物理不可能的数据** —— 例如风速为负、功率超过风机额定功率等（传感器故障或传输错误）

如果直接拿去建模，这些脏数据会"带偏"模型，所以要先清洗。

### 【实操】清洗三步走

```python
# ================= 第 1 步：去除重复值 =================
df = df.drop_duplicates()

# ================= 第 2 步：只对【建模用到的列】去空值 =================
# 注意：不是对整个 df 去空值，否则某一行只要任意一列空白就被整行删除，
#       会造成"过度删行"，白白损失大量有效数据。
use_cols = ['风速', '功率', '发电机转速', '桨距角']
df = df.dropna(subset=use_cols)

# ================= 第 3 步：只删除物理不可能的数据（风机物理边界） =================
# 风速：不能小于 0，不能大于 30 m/s；功率：不能为负，不能超过风机额定 2500 kW
cond_wind_err  = (df['风速'] < 0) | (df['风速'] > 30)
cond_power_err = (df['功率'] < 0) | (df['功率'] > 2500)

# 取反 ~ 保留"正常"的数据
df_clean = df[~(cond_wind_err | cond_power_err)].copy()

# ================= 打印清洗结果对比 =================
original_count = df.shape[0]      # shape[0] 为行数
clean_count = df_clean.shape[0]
print(f'清洗前共有数据: {original_count} 行')
print(f'清洗后剩下数据: {clean_count} 行')
print(f'剔除物理异常样本: {original_count - clean_count} 行')
```

**运行结果：**

```
清洗前共有数据: 285712 行
清洗后剩下数据: 173271 行
剔除物理异常样本: 112441 行
```

> 原始 285716 行去掉重复值后剩 285712 行，再剔除 **112441 条**物理异常样本（约占 39%）。说明 SCADA 原始数据里存在大量风速为负 / 超过 30 m/s、功率为负 / 超过 2500 kW 的异常记录，清洗这一步至关重要。

**知识点小结：**

- `df.drop_duplicates()`：删除完全重复的行
- `df.dropna(subset=[...])`：只对指定列判断空值，其他列为空不删除
- `(df['风速'] < 0) | (df['风速'] > 30)`：构造布尔掩码，`|` 表示"或"
- `~`：对布尔掩码取反，`df[~cond]` 表示"保留不满足条件的行"

---

## 三、探索性数据分析（EDA）与可视化

### 【实操】图 1：风速与功率的趋势变化（双 Y 轴折线图）

风速和功率的量纲相差很大，如果画在同一个 Y 轴上，功率曲线会把风速曲线"压扁"。这时用 `ax1.twinx()` 创建一个**共用一个 X 轴的第二个 Y 轴**，两条曲线各自用自己的刻度，一眼看清变化趋势。

```python
fig, ax1 = plt.subplots(figsize=[12, 5])
plt.title('风速与功率的趋势变化(折线图)')

# 只取前 200 条数据画图，避免线条太密
df_sub = df_clean.head(200)

x = df_sub.index
y_power = df_sub['功率']
y_wind = df_sub['风速']

# 左轴：功率（实线）
ax1.plot(x, y_power, label='功率', color='blue', linewidth=2)
ax1.legend(loc='best')

# 核心步骤：让 ax2 和 ax1 共用一个 x 轴
ax2 = ax1.twinx()
# 右轴：风速（虚线）
ax2.plot(x, y_wind, label='风速', color='red', linewidth=2, linestyle='--')
ax2.legend(loc='upper left')

# 坐标轴与标题
ax1.set_xlabel('数据序号-时间前后')   # x 轴是共用的
ax1.set_ylabel('功率', color='blue')
ax1.tick_params(axis='y', colors='green')
ax2.set_ylabel('风速', color='blue')
ax2.tick_params(axis='y', colors='green')

# 整体美化：网格线
ax1.grid(True, alpha=0.3)
plt.show()
```

> 运行上方代码后可生成“图 1：风速与功率的趋势变化（双 Y 轴折线图）”。

**知识点小结：**

- `plt.subplots(figsize=[12, 5])`：创建画板，设置画布大小
- `ax1.twinx()`：复制一个共用 X 轴的新坐标轴 `ax2`
- `ax1.legend()`：显示图例，`loc='best'` 自动找最优位置

---

### 【掌握】数据"分箱"处理（pd.cut）

在画柱状图、箱线图之前，需要先把连续的**风速**切成一个个**区间（档位）**，这就是"分箱"。

`pd.cut(x, bins, labels)` 三个参数：

- `x`：要被切分的数据
- `bins`：切分边界，例如 `[0, 3, 6, 9, 12, 15, 25]`
- `labels`：给每个区间起的名字，例如 `['0-3', '3-6', ...]`

### 【实操】图 2：不同风速区间的平均功率（柱状图）

```python
# ================= 核心步骤：数据"分箱"处理 =================
bins = [0, 3, 6, 9, 12, 15, 25]                       # 档位边界
labels = ['0-3', '3-6', '6-9', '9-12', '12-15', '15+']  # 档位名称

# pd.cut() 根据风速把每一行数据贴上对应的"区间"标签
df_clean['风速区间'] = pd.cut(df_clean['风速'], bins=bins, labels=labels)

# 按"风速区间"分组，求每组"功率"的平均值（要先有组别才能分组）
power_mean = df_clean.groupby('风速区间', observed=False)['功率'].mean()

# ================= 面向对象绘图 =================
fig, ax1 = plt.subplots(figsize=(10, 6))

# 画柱状图 ax1.bar(X轴类别, Y轴数值)
bars = ax1.bar(power_mean.index, power_mean.values, color='#5DADE2', edgecolor='black')
# 说明：power_mean.index 就是左边的标签序列，等价于 labels

ax1.set_title('不同风速区间的平均发电功率 (柱状图)')
ax1.set_xlabel('风速区间 (m/s)')
ax1.set_ylabel('平均功率 (kW)')

# 高级技巧：只保留横向网格线 (axis='y')，看起来更清爽
ax1.grid(axis='y', alpha=0.3)

# 在每根柱子顶端标注数值
for bar in bars:
    yval = bar.get_height()
    if pd.notnull(yval):
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 20,
                 f'{yval:.0f}', ha='center', va='bottom', fontsize=10)

plt.show()
```

> 运行上方代码后可生成“图 2：不同风速区间的平均发电功率（柱状图）”。

**知识点小结：**

- `groupby('风速区间')['功率'].mean()`：分组 → 取列 → 聚合求均值
- `bar.get_height()`：拿到柱子的高度（数值）
- `ax1.text(x, y, s, ha, va)`：在图上的 (x, y) 位置写文字，`ha/va` 控制对齐方式

---

### 【实操】图 3：风速-功率散点图

从清洗后的数据里随机抽 10000 条画散点图，观察风速和功率之间的大致分布形态（功率随风速增大而上升）。

```python
df_sample = df_clean.sample(n=10000, random_state=44)
x = df_sample['风速']
y = df_sample['功率']

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.scatter(x, y, color='green', s=5, alpha=0.3)

ax1.set_title('风速分布频率 (直方图)')   # 注：此处代码里写的是散点图，标题沿用了原作者
ax1.set_xlabel('风速 (m/s)')
ax1.set_ylabel('记录次数 (频数)')
ax1.grid(axis='y', alpha=0.3)
plt.show()
```

> 运行上方代码后可生成“图 3：风速—功率散点图”。

**知识点小结：**

- `df.sample(n=10000, random_state=44)`：随机抽样，`random_state` 固定随机种子保证可复现
- `ax1.scatter(x, y, s=5, alpha=0.3)`：`s` 控制点大小，`alpha` 控制透明度（点太多时半透明能看清密度）

---

### 【实操】图 4：不同风速区间下的功率分布与异常值（箱线图）

箱线图能直观展示每个区间内功率的**中位数、四分位数以及异常值（红点）**。

```python
# 重新分箱（和柱状图保持一致）
df_clean['风速区间'] = pd.cut(df_clean['风速'], bins=bins, labels=labels)

# ===== 剥离 X 轴和 Y 轴 =====
x_category = df_clean['风速区间']   # X轴：分好类的风速区间
y_power = df_clean['功率']          # Y轴：对应的功率数值

fig, ax1 = plt.subplots(figsize=(10, 6))

# seaborn 画箱线图，ax=ax1 把它钉进我们的画框
# flierprops 专门用来设置"异常值红点"的样式
sns.boxplot(
    x=x_category,
    y=y_power,
    hue=x_category,        # 让颜色跟着 X 轴的分类走
    legend=False,          # X 轴已有标签，关掉重复的图例
    ax=ax1,
    palette='Set3',
    flierprops={'marker': 'o', 'markerfacecolor': 'red', 'markersize': 3, 'alpha': 0.5}
)

ax1.set_title('不同风速区间下的功率分布与异常值 (箱线图)')
ax1.set_xlabel('风速区间 (m/s)')
ax1.set_ylabel('发电功率 (kW)')
ax1.grid(axis='y', alpha=0.3)
plt.show()
```

> 运行上方代码后可生成“图 4：不同风速区间下的功率分布与异常值（箱线图）”。

**知识点小结：**

- `sns.boxplot(...)`：seaborn 高级统计图，`ax=` 参数绑定到指定坐标轴
- `hue=x_category`：按分类着色（新版 seaborn 要求显式指定）
- `flierprops`：异常点样式字典

---

### 【实操】图 5：风机各传感器数据相关性热力图

相关系数矩阵 `.corr()` 能一眼看出"哪些特征和功率关系最密切"，帮助做特征筛选。

```python
# 选出需要计算关系的几列核心特征
features_to_check = df_clean[['风速', '发电机转速', '桨距角', '风向', '功率']]

# .corr() 一键算出两两之间的相关系数矩阵（取值范围 -1 ~ 1）
corr_matrix = features_to_check.corr()

fig, ax1 = plt.subplots(figsize=(8, 6))

# sns.heatmap 画热力图，强制绑定到 ax1
# annot=True  把具体数字写在方块里
# cmap='coolwarm'  暖色(红)代表正相关，冷色(蓝)代表负相关
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax1)

ax1.set_title('风机各传感器数据相关性热力图')
plt.show()
```

> 运行上方代码后可生成“图 5：风机各传感器数据相关性热力图”。

**知识点小结：**

- `df.corr()`：皮尔逊相关系数矩阵，越接近 1 正相关越强，越接近 -1 负相关越强
- `sns.heatmap(corr_matrix, annot=True, fmt='.2f')`：`annot` 标注数值，`fmt` 控制小数位数
- 从热力图可发现：**风速、发电机转速**与功率高度正相关，是最重要的特征

---

## 四、线性回归模型

### 【知道】线性回归 API

```python
from sklearn.linear_model import LinearRegression
```

线性回归利用回归方程对**一个或多个自变量（特征）与因变量（目标）之间**的关系进行建模。其学习过程本质上就是求一组权重系数 w，使预测值与真实值的均方误差最小。

### 【实操】特征与目标锁定 + 划分与标准化

```python
# ============ 1. 锁定特征与目标 ============
feature_cols = ['风速', '发电机转速', '桨距角']
X = df_clean[feature_cols]
y = df_clean['功率']

# ============ 2. 划分与标准化 ============
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()                     # 标准化
X_train_scaled = scaler.fit_transform(X_train)  # fit 计算均值/标准差 + transform 变换（训练集）
X_test_scaled = scaler.transform(X_test)        # 用上方 fit 出来的均值/标准差做变换（测试集）
```

**为什么要标准化？** 风速、发电机转速、桨距角三者的量纲相差巨大（转速上千、桨距角只有个位数），如果不标准化，量级大的特征会"支配"模型，导致其他特征学不到东西。标准化把每个特征变成**均值为 0、标准差为 1** 的标准正态分布。

### 【掌握】K 折交叉验证（看稳定性）

```python
model = LinearRegression()   # 创建线性回归模型

# K折交叉验证：把训练集分成 5 份，轮流用其中 4 份训练、1 份验证，共打分 5 次
cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
print('\n--- K折交叉验证 ---')
print(f'5次打分: {cv_scores}')
print(f'平均稳定得分: {cv_scores.mean():.4f}')
```

**运行结果：**

```
--- K折交叉验证 ---
5次打分: [0.9532089  0.95339876 0.95291757 0.95367115 0.95295293]
平均稳定得分: 0.9532
```

5 次打分非常接近（都在 0.953 左右），说明模型在不同数据划分下都很稳定。

**交叉验证的作用**：单次划分的结果有偶然性，交叉验证多次评估取平均，得到的分数更能反映模型的真实稳定水平。

### 【实操】终极训练 + 模型评估

```python
model.fit(X_train_scaled, y_train)   # 用全部训练集做最终训练

y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print('\n--- 测试集最终评估 ---')
print(f'RMSE (均方根误差): {rmse:.2f} kW')
print(f'R² 得分: {r2:.4f}')
```

**运行结果：**

```
--- 测试集最终评估 ---
RMSE (均方根误差): 209.40 kW
R² 得分: 0.9533
```

**评估指标：**

- **MSE（均方误差）**：预测值与真实值误差平方的均值，越小越好
- **RMSE（均方根误差）**：MSE 开根号，量纲和原目标一致，更直观，且会"放大"大误差的影响
- **R²（决定系数）**：取值越接近 1 说明拟合越好，越接近 0 越差

### 【掌握】还原原始空间业务公式

模型是在**标准化之后**的数据上训练的，所以 `model.coef_` 和 `model.intercept_` 是"标准化空间"里的参数。要得到能直接给业务人员看的原始公式，需要做一次**反标准化还原**：

```python
# 提取标准化后的参数并还原到原始空间
original_coef = model.coef_ / scaler.scale_              # 还原权重
original_intercept = model.intercept_ - np.sum(original_coef * scaler.mean_)   # 还原截距

print('\n=============================================')
print('             最终提取的线性回归公式')
print('=============================================')
formula = f'功率 = {original_intercept:.2f}'
for feature, coef in zip(feature_cols, original_coef):
    if coef >= 0:
        formula += f' + {coef:.4f} * {feature}'
    else:
        formula += f' - {abs(coef):.4f} * {feature}'
print(formula)
print('=============================================\n')
```

**运行结果：**

```
=============================================
             最终提取的线性回归公式
=============================================
功率 = -3053.20 + 29.4777 * 风速 + 2.8264 * 发电机转速 + 65.5215 * 桨距角
=============================================
```

**还原公式推导（理解即可）：**

- 标准化：`z = (x - mean) / scale`
- 模型：`ŷ = w_std · z + b_std = Σ w_std_i · (x_i - mean_i)/scale_i + b_std`
- 展开合并同类项：
  - 权重：`w_i = w_std_i / scale_i`
  - 截距：`b = b_std - Σ(w_i · mean_i)`

这就是上面两行代码的数学依据。线性回归是**可解释的"白盒"模型**，这是它相比 KNN 最大的优势。

### 【实操】预测未来数据

```python
future_data = pd.DataFrame({
    '风速': [5.5, 9.2, 14.5],
    '发电机转速': [900, 1400, 1600],
    '桨距角': [0.5, 1.2, 15.0]
})

future_scaled = scaler.transform(future_data)          # 新数据必须用同一个 scaler 标准化！
future_predictions = model.predict(future_scaled)

print('--- 预测未来的全新数据 ---')
for i in range(len(future_data)):
    print(f'场景 {i+1} [风速 {future_data.loc[i, "风速"]} m/s] -> 预测功率: {future_predictions[i]:.2f} kW')
```

**运行结果：**

```
--- 预测未来的全新数据 ---
场景 1 [风速 5.5 m/s] -> 预测功率: -314.56 kW
场景 2 [风速 9.2 m/s] -> 预测功率: 1253.56 kW
场景 3 [风速 14.5 m/s] -> 预测功率: 2879.27 kW
```

> ⚠️ 两个关键点：
> 1. **新数据一定要用训练时的那个 scaler 来 transform**，否则量纲不一致，预测结果就是错的。
> 2. 注意**场景 1 预测出 -314.56 kW 的负功率**，物理上不可能！这是因为"低风速 + 高转速"的组合在训练数据里很罕见，线性回归强行线性外推，结果溢出到负值区间——这正是线性回归**外推能力差**的典型缺陷。

---

## 五、KNN 回归模型

### 【知道】KNN 回归 API

```python
from sklearn.neighbors import KNeighborsRegressor
```

KNN（K 近邻）回归的思想：对一个新的样本，找特征空间里离它**最近的 K 个训练样本**，把这 K 个样本目标值的**平均值**作为预测值。KNN 极其依赖距离，所以**必须先做标准化**。

### 【掌握】网格搜索 GridSearchCV 寻找最优 K 值

K 到底取多少最好？靠"拍脑袋"不行，用**网格搜索 + 交叉验证**自动把候选 K 挨个试一遍，选出得分最高的那个。

```python
print('正在网格搜索寻找最优K值......')

# 候选 K：根据风电大数据，K 不要太小，取 3~30 区间
param_grid = {
    'n_neighbors': [3, 5, 7, 10, 12, 15, 20, 25, 30]
}

# 5折交叉验证，评价指标 r²
grid = GridSearchCV(
    estimator=KNeighborsRegressor(),
    param_grid=param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1            # 使用全部 CPU 加速运算
)

# 只用训练集做网格搜索！！！绝对不能喂全部数据（否则会数据泄漏）
grid.fit(X_train_scaled, y_train)

print(f'最优超参数K = {grid.best_params_["n_neighbors"]}')
print(f'训练集5折交叉验证最优R² = {grid.best_score_:.4f}')

# 拿到训练出来的最优 KNN 模型，后面全部用 knn_model
knn_model = grid.best_estimator_
```

**运行结果：**

```
正在网格搜索寻找最优K值......
最优超参数K = 15
训练集5折交叉验证最优R² = 0.9971
```

**GridSearchCV 关键属性：**

- `grid.best_params_`：最优超参数组合
- `grid.best_score_`：最优超参数对应的交叉验证平均得分
- `grid.best_estimator_`：已经用最优参数训练好的模型

### 【实操】模型评估 + 预测未来

```python
y_pred = knn_model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print('\n--- 测试集最终评估 ---')
print(f'RMSE (均方根误差): {rmse:.2f} kW')
print(f'R² 得分: {r2:.4f}')

print('\n[业务提示] KNN 是黑盒算法，无法像线性回归那样提取业务公式。\n')

future_scaled = scaler.transform(future_data)
future_predictions = knn_model.predict(future_scaled)

print('--- 预测未来的全新数据 ---')
for i in range(len(future_data)):
    print(f'场景 {i+1} [风速 {future_data.loc[i, "风速"]} m/s] -> 预测功率: {future_predictions[i]:.2f} kW')
```

**运行结果：**

```
--- 测试集最终评估 ---
RMSE (均方根误差): 52.46 kW
R² 得分: 0.9971

[业务提示] KNN 是黑盒算法，无法像线性回归那样提取业务公式。

--- 预测未来的全新数据 ---
场景 1 [风速 5.5 m/s] -> 预测功率: 308.02 kW
场景 2 [风速 9.2 m/s] -> 预测功率: 868.27 kW
场景 3 [风速 14.5 m/s] -> 预测功率: 1475.52 kW
```

> 💡 **对比亮点**：同样是场景 1（低风速 + 高转速），线性回归预测出荒谬的 **-314.56 kW**，而 KNN 给出合理的 **308.02 kW**。原因是 KNN 只在"邻近训练样本"之间插值，不会像线性回归那样外推出物理不可能的值。这就是非线性模型在这类数据上的优势。

---

## 六、模型结果可视化与残差分析

> 说明：下面两段代码里的 `y_test` 和 `y_pred` 用的是**上一步 KNN 模型**的预测结果（因为 `y_pred` 变量已被 KNN 覆盖）。若想看线性回归的效果，只需在跑完线性回归后立刻执行这两段代码即可。

### 【实操】图 6：真实值 vs 预测值对比

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# ---------- 图 1：真实值 vs 预测值（散点分布） ----------
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
padding = (max_val - min_val) * 0.05

# 画"完美预测线 y=x"（红色虚线），点越贴近它说明预测越准
ax1.plot([min_val-padding, max_val+padding],
         [min_val-padding, max_val+padding],
         color='red', linestyle='--', linewidth=2, label='完美预测线 (y=x)')

ax1.scatter(y_test, y_pred, alpha=0.4, color='dodgerblue', s=10, label='模型预测点')

ax1.set_title('图1：真实功率 vs 预测功率分布')
ax1.set_xlabel('真实功率 (kW)')
ax1.set_ylabel('预测功率 (kW)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# ---------- 图 2：局部样本跟踪拟合（折线图） ----------
samples_to_plot = min(100, len(y_test))
y_test_subset = np.array(y_test)[:samples_to_plot]
y_pred_subset = np.array(y_pred)[:samples_to_plot]
x_index = range(samples_to_plot)

ax2.plot(x_index, y_test_subset, label='真实功率', color='black', marker='o', markersize=4, alpha=0.7)
ax2.plot(x_index, y_pred_subset, label='预测功率', color='darkorange', linestyle='--', marker='x', markersize=4, alpha=0.9)

ax2.set_title(f'图2：测试集前 {samples_to_plot} 个样本的曲线追踪')
ax2.set_xlabel('随机样本编号')
ax2.set_ylabel('发电功率 (kW)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

> 运行上方代码后可生成“图 6：真实功率与预测功率对比”。

### 【实操】图 7：残差分析（终极体检）

残差 = 真实值 - 预测值。残差分析能判断模型是否"有偏见"：

- 残差直方图若**以 0 为中心对称**（近似正态），说明模型无系统性偏差
- 残差散点图若**随机分布在 0 线两侧**、没有明显趋势，说明模型拟合良好；若出现"喇叭口"或明显曲线趋势，说明还有规律没学到

```python
# 1. 计算残差：y_test 是真实答案，y_pred 是模型考出来的答案
residuals = y_test - y_pred

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# ---------- 图 1：残差分布直方图（带 KDE 核密度曲线） ----------
sns.histplot(residuals, bins=50, kde=True, color='purple', ax=ax1)
ax1.axvline(x=0, color='red', linestyle='--', linewidth=2)   # 红色警戒线 = 完美零误差线

ax1.set_title('图1：残差分布直方图 (看模型是否有偏见)')
ax1.set_xlabel('残差 (真实功率 - 预测功率) kW')
ax1.set_ylabel('样本数量')
ax1.grid(True, alpha=0.3)

# ---------- 图 2：预测值 vs 残差散点图 ----------
ax2.scatter(y_pred, residuals, alpha=0.3, color='teal', s=10)
ax2.axhline(y=0, color='red', linestyle='--', linewidth=2)   # 0 误差水平基准线

ax2.set_title('图2：预测功率 vs 残差 (找模型的软肋)')
ax2.set_xlabel('预测功率 (kW)')
ax2.set_ylabel('残差 (kW)')
ax2.grid(True, alpha=0.3)

# 增加一条残差拟合趋势线，一眼看清有没有趋势
sns.regplot(x=y_pred, y=residuals, scatter=False, color='orange', ax=ax2)

plt.tight_layout()
plt.show()
```

> 运行上方代码后可生成“图 7：残差分析”。

---

## 七、总结：线性回归 vs KNN 回归

**本案例实际成绩对比：**

| 指标 | 线性回归 | KNN 回归（K=15） |
| :--- | :---: | :---: |
| 交叉验证 R² | 0.9532 | 0.9971 |
| 测试集 R² | 0.9533 | **0.9971** |
| 测试集 RMSE | 209.40 kW | **52.46 kW** |
| 场景1（低风速）预测 | -314.56 kW（❌ 负值荒谬） | **308.02 kW**（✅ 合理） |
| 能否提取业务公式 | ✅ `功率 = -3053.20 + 29.48·风速 + 2.83·转速 + 65.52·桨距角` | ❌ 黑盒 |

> 注：上表指标来自原始 notebook 的运行记录。由于 `train_test_split` 在不同 scikit-learn 版本下的随机划分存在细微差异，用当前最新库重新复现时 R² 可能有 ±0.01 左右的浮动（本机复现：线性回归 R²≈0.945、KNN R²≈0.993，最优 K 仍为 15），不影响"KNN 优于线性回归"的结论。

**算法特性对比：**

| 对比维度 | 线性回归 | KNN 回归 |
| :--- | :--- | :--- |
| **算法类型** | 参数模型（学习权重 w） | 惰性学习（无显式训练） |
| **可解释性** | ✅ 白盒，可提取业务公式 | ❌ 黑盒，无法解释 |
| **对标准化依赖** | 依赖（量纲影响权重） | **极强依赖**（基于距离） |
| **超参数** | 几乎没有 | K 值（需网格搜索调优） |
| **适用场景** | 关系近似线性的数据 | 非线性、局部相似的数据 |
| **预测速度** | 快 | 慢（要遍历所有训练样本） |

> 本案例中 KNN（R²=0.9971）明显优于线性回归（R²=0.9533），因为风速-功率关系并非简单线性，且 KNN 不会外推出负功率这类荒谬值。

**本案例完整流程回顾：**

```
数据加载 → 数据清洗（去重/去空/物理边界）→ EDA可视化（折线/柱状/散点/箱线/热力图）
→ 特征工程（标准化）→ 线性回归（交叉验证 + 还原公式）→ KNN回归（网格搜索）
→ 模型评估（RMSE/R²）→ 结果可视化 + 残差分析
```
