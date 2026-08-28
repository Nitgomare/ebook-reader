---
title: 从零读懂机器学习
---

# NumPy 算法实践

用五个小实验观察 `fit()` 内部发生了什么。成熟项目仍应优先使用 scikit-learn；这里的重点是理解数值计算、验证实现并解释差异。

## 实验 1：线性回归不是求逆 { #linear-lab }

目标：用温度、转速和载荷估计轴承振动 RMS。线性模型为：

$$\hat y = Xw + b$$

`tiny_ml` 的早期实现直接计算 $(X^TX)^{-1}X^Ty$。公式直观，但显式求逆在特征相关或尺度差异大时不稳定。教学实现应使用最小二乘求解器：

```python
import numpy as np

class StableLinearRegression:
    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        if X.ndim != 2 or y.ndim != 1 or X.shape[0] != y.size:
            raise ValueError("X 应为二维，y 应为一维，且样本数一致")

        design = np.column_stack([np.ones(X.shape[0]), X])
        self.coef_all_, self.residuals_, self.rank_, _ = np.linalg.lstsq(
            design, y, rcond=None
        )
        return self

    @property
    def intercept_(self):
        return self.coef_all_[0]

    @property
    def coef_(self):
        return self.coef_all_[1:]

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        return X @ self.coef_ + self.intercept_
```

### 必须做的三个对照

```python
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

models = {
    "numpy_lstsq": StableLinearRegression(),
    "sklearn_ols": LinearRegression(),
    "ridge": Ridge(alpha=1.0),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(name, root_mean_squared_error(y_test, pred), mean_absolute_error(y_test, pred))
```

对比系数、误差和矩阵秩。如果 NumPy 与 sklearn 差异很大，先检查截距、数据划分和输入形状，不要先怀疑库。

## 实验 2：K-Means 的循环里发生了什么 { #clustering-lab }

K-Means 反复执行两步：把样本分配给最近中心，再用簇内均值更新中心。

```python
def kmeans_step(X, centers):
    squared_distance = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    labels = squared_distance.argmin(axis=1)
    new_centers = np.vstack([
        X[labels == k].mean(axis=0) if np.any(labels == k) else centers[k]
        for k in range(centers.shape[0])
    ])
    inertia = squared_distance[np.arange(X.shape[0]), labels].sum()
    return labels, new_centers, inertia
```

这里最重要的是数组形状：

- `X[:, None, :]` 是 `(样本, 1, 特征)`；
- `centers[None, :, :]` 是 `(1, 簇, 特征)`；
- 广播后距离矩阵是 `(样本, 簇)`。

机械工况聚类前必须先标准化。转速的数值可能是 1500，而峭度只有 3；不缩放时，欧氏距离几乎只看转速。

```python
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

model = make_pipeline(
    StandardScaler(),
    KMeans(n_clusters=3, n_init=20, random_state=42),
)
labels = model.fit_predict(features)
```

!!! warning "聚类编号没有物理含义"
    `0/1/2` 只是簇标签，换一次初始化可能会整体交换。要通过转速、载荷、频谱峰值等外部变量解释每个簇，不能把标签编号直接写成故障等级。

## 实验 3：PCA 是旋转坐标，不是自动找故障 { #pca-lab }

对中心化数据 $X_c$，PCA 找到方差最大的正交方向。更稳健的实现可使用对称矩阵专用分解：

```python
def pca_fit_transform(X, n_components=2):
    X = np.asarray(X, dtype=float)
    mean = X.mean(axis=0)
    centered = X - mean
    covariance = centered.T @ centered / (X.shape[0] - 1)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]
    components = eigenvectors[:, order[:n_components]]
    transformed = centered @ components
    explained_ratio = eigenvalues[order[:n_components]] / eigenvalues.sum()
    return transformed, components, explained_ratio
```

`tiny_ml` 展示了由特征分解得到投影矩阵的主线；现代实践还要补上：训练集拟合均值与主轴、测试集只做变换，且先处理单位尺度。

```python
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pca_pipeline = make_pipeline(StandardScaler(), PCA(n_components=0.95))
X_train_reduced = pca_pipeline.fit_transform(X_train)
X_test_reduced = pca_pipeline.transform(X_test)  # 不能再次 fit
```

PCA 的高方差方向不一定与故障最相关。载荷和转速变化常比早期故障强得多，所以 PCA 图上的分离可能只是工况差异。

## 实验 4：树与集成为什么适合表格特征 { #tree-ensemble-lab }

决策树通过阈值切分特征空间；回归树选择使两侧平方误差最小的切分。随机森林还需要两个随机性来源：

1. 每棵树使用有放回的 bootstrap 样本；
2. 每次节点划分只看随机抽取的一部分特征。

如果只随机选择特征、却让每棵树看到相同样本，树之间仍会高度相关，不能完整体现随机森林思想。工程中先用成熟实现：

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=300,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
```

特征重要性只能用于生成假设，不等于因果关系。高度相关的 RMS、方差、能量会互相分摊重要性；应补充置换重要性和物理解释。

## 实验 5：验证代码比模型代码更重要 { #validation-lab }

`tiny_ml` 的比较脚本体现了一个好习惯：同一数据划分上对照自写算法与 sklearn。现代化实验还必须修正三点：

- 不再使用已从 scikit-learn 删除的 Boston housing 数据集；回归可用 `load_diabetes` 或自己的公开数据。
- 预处理只在训练集上 `fit`，最好用 `Pipeline` 封装。
- 同一对象、设备、人员或试验批次的数据应分组划分，避免相似样本泄漏。

```python
from sklearn.model_selection import GroupShuffleSplit

splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
train_idx, test_idx = next(splitter.split(X, y, groups=run_id))
X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

assert set(run_id[train_idx]).isdisjoint(run_id[test_idx])
```

## 读源码时使用这张检查表

- [ ] 输入的形状、dtype、单位是什么？
- [ ] 参数在何处初始化，随机种子是否可控？
- [ ] 目标函数与书中哪条公式对应？
- [ ] 停止条件是否可能死循环？
- [ ] 空簇、奇异矩阵、溢出、缺失值如何处理？
- [ ] 训练阶段学到的状态是否只在 `fit()` 中更新？
- [ ] 与 sklearn 比较时是否使用完全相同的数据划分和指标？
- [ ] 结果差异来自实现错误、数值误差，还是定义不同？

> **来源说明：** 实验思路参考 [fengyang95/tiny_ml](https://github.com/fengyang95/tiny_ml)。完整算法目录、推导和上游代码入口统一放在 [tiny_ml 算法实验室](/book-sites/zhou-machine-learning/tinyml-lab/)；本站不复制发布无明确许可证的完整源码。

下一步进入 [第一个机器学习完整项目](first-project.md)，把数据生成、特征提取、分组划分、基线和评估串成一次完整实验。
