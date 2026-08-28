## 附录

## A 矩阵

### A.1 基本演算

记实矩阵 $\mathbf{A} \in  {\mathbb{R}}^{m \times  n}$ 第 $i$ 行第 $j$ 列的元素为 ${\left( \mathbf{A}\right) }_{ij} = {A}_{ij}$ . 矩阵 $\mathbf{A}$ 的转置(transpose)记为 ${\mathbf{A}}^{\mathrm{T}},{\left( {\mathbf{A}}^{\mathrm{T}}\right) }_{ij} = {A}_{ji}$ . 显然,

$$
{\left( \mathbf{A} + \mathbf{B}\right) }^{\mathrm{T}} = {\mathbf{A}}^{\mathrm{T}} + {\mathbf{B}}^{\mathrm{T}}, \tag{A.1}
$$

$$
{\left( \mathbf{{AB}}\right) }^{\mathrm{T}} = {\mathbf{B}}^{\mathrm{T}}{\mathbf{A}}^{\mathrm{T}}. \tag{A.2}
$$

对于矩阵 $\mathbf{A} \in  {\mathbb{R}}^{m \times  n}$ ,若 $m = n$ 则称为 $n$ 阶方阵. 用 ${\mathbf{I}}_{n}$ 表示 $n$ 阶单位阵,方阵 $\mathbf{A}$ 的逆矩阵 ${\mathbf{A}}^{-1}$ 满足 $\mathbf{A}{\mathbf{A}}^{-1} = {\mathbf{A}}^{-1}\mathbf{A} = \mathbf{I}$ . 不难发现,

$$
{\left( {\mathbf{A}}^{\mathrm{T}}\right) }^{-1} = {\left( {\mathbf{A}}^{-1}\right) }^{\mathrm{T}}, \tag{A.3}
$$

$$
{\left( \mathbf{{AB}}\right) }^{-1} = {\mathbf{B}}^{-1}{\mathbf{A}}^{-1}. \tag{A.4}
$$

对于 $n$ 阶方阵 $\mathbf{A}$ ，它的迹(trace)是主对角线上的元素之和，即 $\operatorname{tr}\left( \mathbf{A}\right)  = \; \mathop{\sum }\limits_{{i = 1}}^{n}{A}_{ii}$ . 迹有如下性质:

$$
\operatorname{tr}\left( {\mathbf{A}}^{\mathrm{T}}\right)  = \operatorname{tr}\left( \mathbf{A}\right) , \tag{A.5}
$$

$$
\operatorname{tr}\left( {\mathbf{A} + \mathbf{B}}\right)  = \operatorname{tr}\left( \mathbf{A}\right)  + \operatorname{tr}\left( \mathbf{B}\right) , \tag{A.6}
$$

$$
\operatorname{tr}\left( \mathbf{{AB}}\right)  = \operatorname{tr}\left( \mathbf{{BA}}\right) , \tag{A.7}
$$

$$
\operatorname{tr}\left( \mathbf{{ABC}}\right)  = \operatorname{tr}\left( \mathbf{{BCA}}\right)  = \operatorname{tr}\left( \mathbf{{CAB}}\right) . \tag{A.8}
$$

$n$ 阶方阵 $\mathbf{A}$ 的行列式(determinant)定义为

$$
\det \left( \mathbf{A}\right)  = \mathop{\sum }\limits_{{\mathbf{\sigma } \in  {S}_{n}}}\operatorname{par}\left( \mathbf{\sigma }\right) {A}_{1{\sigma }_{1}}{A}_{2{\sigma }_{2}}\ldots {A}_{1{\sigma }_{n}}, \tag{A.9}
$$

其中 ${S}_{n}$ 为所有 $n$ 阶排列(permutation)的集合, $\operatorname{par}\left( \mathbf{\sigma }\right)$ 的值为 -1 或 +1 取决于 $\mathbf{\sigma } = \left( {{\sigma }_{1},{\sigma }_{2},\ldots ,{\sigma }_{n}}\right)$ 为奇排列或偶排列,即其中出现降序的次数为奇数或偶

---

常直接用 $\mathbf{I}$ 表示单位阵.

---

数,例如 $\left( {1,3,2}\right)$ 中降序次数为 $1,\left( {1,4,3,2}\right)$ 中降序次数为 2 . 对于单位阵,有 $\det \left( \mathbf{I}\right)  = 1$ . 对于 2 阶方阵,有

$$
\det \left( \mathbf{A}\right)  = \det \left( \begin{array}{ll} {A}_{11} & {A}_{12} \\  {A}_{21} & {A}_{22} \end{array}\right)  = {A}_{11}{A}_{22} - {A}_{12}{A}_{21}.
$$

$n$ 阶方阵 $\mathbf{A}$ 的行列式有如下性质:

$$
\det \left( {c\mathbf{A}}\right)  = {c}^{n}\det \left( \mathbf{A}\right) , \tag{A.10}
$$

$$
\det \left( {\mathbf{A}}^{\mathrm{T}}\right)  = \det \left( \mathbf{A}\right) , \tag{A.11}
$$

$$
\det \left( \mathbf{{AB}}\right)  = \det \left( \mathbf{A}\right) \det \left( \mathbf{B}\right) , \tag{A.12}
$$

$$
\det \left( {\mathbf{A}}^{-1}\right)  = \det {\left( \mathbf{A}\right) }^{-1}, \tag{A.13}
$$

$$
\det \left( {\mathbf{A}}^{n}\right)  = \det {\left( \mathbf{A}\right) }^{n}. \tag{A.14}
$$

矩阵 $\mathbf{A} \in  {\mathbb{R}}^{m \times  n}$ 的 Frobenius 范数定义为

$$
\parallel \mathbf{A}{\parallel }_{F} = {\left( \operatorname{tr}\left( {\mathbf{A}}^{\mathrm{T}}\mathbf{A}\right) \right) }^{1/2} = {\left( \mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j = 1}}^{n}{A}_{ij}^{2}\right) }^{1/2}. \tag{A.15}
$$

容易看出,矩阵的 Frobenius 范数就是将矩阵张成向量后的 ${\mathrm{L}}_{2}$ 范数.

### A.2 导数

向量 $\mathbf{a}$ 相对于标量 $x$ 的导数(derivative)，以及 $x$ 相对于 $\mathbf{a}$ 的导数都是向量,其第 $i$ 个分量分别为

$$
{\left( \frac{\partial \mathbf{a}}{\partial x}\right) }_{i} = \frac{\partial {a}_{i}}{\partial x}, \tag{A.16}
$$

$$
{\left( \frac{\partial x}{\partial \mathbf{a}}\right) }_{i} = \frac{\partial x}{\partial {a}_{i}}. \tag{A.17}
$$

类似的,矩阵 $\mathbf{A}$ 对于标量 $x$ 的导数,以及 $x$ 对于 $\mathbf{A}$ 的导数都是矩阵,其第 $i$ 行第 $j$ 列上的元素分别为

$$
{\left( \frac{\partial \mathbf{A}}{\partial x}\right) }_{ij} = \frac{\partial {A}_{ij}}{\partial x}, \tag{A.18}
$$

$$
{\left( \frac{\partial x}{\partial \mathbf{A}}\right) }_{ij} = \frac{\partial x}{\partial {A}_{ij}}. \tag{A.19}
$$

对于函数 $f\left( \mathbf{x}\right)$ ,假定其对向量的元素可导,则 $f\left( \mathbf{x}\right)$ 关于 $\mathbf{x}$ 的一阶导数是一个向量，其第 $i$ 个分量为

$$
{\left( \nabla f\left( \mathbf{x}\right) \right) }_{i} = \frac{\partial f\left( \mathbf{x}\right) }{\partial {x}_{i}}, \tag{A.20}
$$

$f\left( \mathbf{x}\right)$ 关于 $\mathbf{x}$ 的二阶导数是称为海森矩阵(Hessian matrix)的一个方阵,其第 $i$ 行第 $j$ 列上的元素为

$$
{\left( {\nabla }^{2}f\left( \mathbf{x}\right) \right) }_{ij} = \frac{{\partial }^{2}f\left( \mathbf{x}\right) }{\partial {x}_{i}\partial {x}_{j}}. \tag{A.21}
$$

向量和矩阵的导数满足乘法法则(product rule)

$$
\frac{\partial {\mathbf{x}}^{\mathrm{T}}\mathbf{a}}{\partial \mathbf{x}} = \frac{\partial {\mathbf{a}}^{\mathrm{T}}\mathbf{x}}{\partial \mathbf{x}} = \mathbf{a}, \tag{A.22}
$$

$$
\frac{\partial \mathbf{{AB}}}{\partial \mathbf{x}} = \frac{\partial \mathbf{A}}{\partial \mathbf{x}}\mathbf{B} + \mathbf{A}\frac{\partial \mathbf{B}}{\partial \mathbf{x}}. \tag{A.23}
$$

---

$a$ 相对于 $x$ 为常向量.

---

由 ${\mathbf{A}}^{-1}\mathbf{A} = \mathbf{I}$ 和 式(A.23),逆矩阵的导数可表示为

$$
\frac{\partial {\mathbf{A}}^{-1}}{\partial x} =  - {\mathbf{A}}^{-1}\frac{\partial \mathbf{A}}{\partial x}{\mathbf{A}}^{-1}. \tag{A.24}
$$

若求导的标量是矩阵 $\mathbf{A}$ 的元素,则有

$$
\frac{\partial \operatorname{tr}\left( \mathbf{{AB}}\right) }{\partial {A}_{ij}} = {B}_{ji} \tag{A.25}
$$

$$
\frac{\partial \operatorname{tr}\left( \mathbf{{AB}}\right) }{\partial \mathbf{A}} = {\mathbf{B}}^{\mathrm{T}}. \tag{A.26}
$$

进而有

$$
\frac{\partial \operatorname{tr}\left( {{\mathbf{A}}^{\mathrm{T}}\mathbf{B}}\right) }{\partial \mathbf{A}} = \mathbf{B}, \tag{A.27}
$$

$$
\frac{\partial \operatorname{tr}\left( \mathbf{A}\right) }{\partial \mathbf{A}} = \mathbf{I}, \tag{A.28}
$$

$$
\frac{\partial \operatorname{tr}\left( {\mathbf{A}\mathbf{B}{\mathbf{A}}^{\mathrm{T}}}\right) }{\partial \mathbf{A}} = \mathbf{A}\left( {\mathbf{B} + {\mathbf{B}}^{\mathrm{T}}}\right) . \tag{A.29}
$$

由式(A.15)和(A.29)有

$$
\frac{\partial \parallel \mathbf{A}{\parallel }_{F}^{2}}{\partial \mathbf{A}} = \frac{\partial \operatorname{tr}\left( {\mathbf{A}{\mathbf{A}}^{\mathrm{T}}}\right) }{\partial \mathbf{A}} = 2\mathbf{A}. \tag{A.30}
$$

链式法则(chain rule)是计算复杂导数时的重要工具. 简单地说,若函数 $f$ 是 $g$ 和 $h$ 的复合,即 $f\left( x\right)  = g\left( {h\left( x\right) }\right)$ ,则有

$$
\frac{\partial f\left( x\right) }{\partial x} = \frac{\partial g\left( {h\left( x\right) }\right) }{\partial h\left( x\right) } \cdot  \frac{\partial h\left( x\right) }{\partial x}. \tag{A.31}
$$

例如在计算下式时,将 $\mathbf{{Ax}} - \mathbf{b}$ 看作一个整体可简化计算:

$$
\frac{\partial }{\partial \mathbf{x}}{\left( \mathbf{A}\mathbf{x} - \mathbf{b}\right) }^{\mathrm{T}}\mathbf{W}\left( {\mathbf{A}\mathbf{x} - \mathbf{b}}\right)  = \frac{\partial \left( {\mathbf{A}\mathbf{x} - \mathbf{b}}\right) }{\partial \mathbf{x}} \cdot  2\mathbf{W}\left( {\mathbf{A}\mathbf{x} - \mathbf{b}}\right)
$$

$$
= 2\mathbf{{AW}}\left( {\mathbf{A}\mathbf{x} - \mathbf{b}}\right) . \tag{A.32}
$$

### A.3 奇异值分解

任意实矩阵 $\mathbf{A} \in  {\mathbb{R}}^{m \times  n}$ 都可分解为

$$
\mathbf{A} = \mathbf{U}\mathbf{\sum }{\mathbf{V}}^{\mathrm{T}} \tag{A.33}
$$

其中, $\mathbf{U} \in  {\mathbb{R}}^{m \times  m}$ 是满足 ${\mathbf{U}}^{\mathrm{T}}\mathbf{U} = \mathbf{I}$ 的 $m$ 阶酉矩阵(unitary matrix); $\mathbf{V} \in  {\mathbb{R}}^{n \times  n}$ 是满足 ${\mathbf{V}}^{\mathrm{T}}\mathbf{V} = \mathbf{I}$ 的 $n$ 阶酉矩阵; $\mathbf{\sum } \in  {\mathbb{R}}^{m \times  n}$ 是 $m \times  n$ 的矩阵,其中 ${\left( \mathbf{\sum }\right) }_{ii} = {\sigma }_{i}$ 且其他位置的元素均为 $0,{\sigma }_{i}$ 为非负实数且满足 ${\sigma }_{1} \geq  {\sigma }_{2} \geq  \ldots  \geq  0$ .

式(A.33)中的分解称为奇异值分解(Singular Value Decomposition, 简称 SVD),其中 $\mathbf{U}$ 的列向量 ${\mathbf{u}}_{i} \in  {\mathbb{R}}^{m}$ 称为 $\mathbf{A}$ 的左奇异向量(left-singular vector), $\mathbf{V}$ 的列向量 ${\mathbf{v}}_{i} \in  {\mathbb{R}}^{n}$ 称为 $\mathbf{A}$ 的右奇异向量(right-singular vector), ${\sigma }_{i}$ 称为奇异值(singular value). 矩阵 $\mathbf{A}$ 的秩(rank)就等于非零奇异值的个数.

奇异值分解有广泛的用途，例如对于低秩矩阵近似(low-rank matrix approximation)问题,给定一个秩为 $r$ 的矩阵 $\mathbf{A}$ ,欲求其最优 $k$ 秩近似矩阵 $\widetilde{\mathbf{A}}$ , $k \leq  r$ ,该问题可形式化为

$$
\mathop{\min }\limits_{{\widetilde{\mathbf{A}} \in  {\mathbb{R}}^{m \times  n}}}\parallel \mathbf{A} - \widetilde{\mathbf{A}}{\parallel }_{F} \tag{A.34}
$$

$$
\text{ s.t. }\operatorname{rank}\left( \widetilde{\mathbf{A}}\right)  = k\text{ . }
$$

---

常将奇异值按降序排列以确保 $\mathbf{\sum }$ 的唯一性.

当 $\mathbf{A}$ 为对称正定矩阵时, 奇异值分解与特征值分解结果相同.

---

奇异值分解提供了上述问题的解析解: 对矩阵 $\mathbf{A}$ 进行奇异值分解后,将矩阵 $\mathbf{\sum }$ 中的 $r - k$ 个最小的奇异值置零获得矩阵 ${\mathbf{\sum }}_{k}$ ,即仅保留最大的 $k$ 个奇异值, 则

$$
{\mathbf{A}}_{k} = {\mathbf{U}}_{k}{\mathbf{\sum }}_{k}{\mathbf{V}}_{k}^{\mathrm{T}} \tag{A.35}
$$

就是式(A.34)的最优解,其中 ${\mathbf{U}}_{k}$ 和 ${\mathbf{V}}_{k}$ 分别是式(A.33)中的前 $\mathrm{k}$ 列组成的矩阵. 这个结果称为 Eckart-Young-Mirsky 定理.

## B 优化

### B.1 拉格朗日乘子法

拉格朗日乘子法(Lagrange multipliers)是一种寻找多元函数在一组约束下的极值的方法. 通过引入拉格朗日乘子,可将有 $d$ 个变量与 $k$ 个约束条件的最优化问题转化为具有 $d + k$ 个变量的无约束优化问题求解.

先考虑一个等式约束的优化问题. 假定 $\mathbf{x}$ 为 $d$ 维向量,欲寻找 $\mathbf{x}$ 的某个取值 ${\mathbf{x}}^{ * }$ ,使目标函数 $f\left( \mathbf{x}\right)$ 最小且同时满足 $g\left( \mathbf{x}\right)  = 0$ 的约束. 从几何角度看,该问题的目标是在由方程 $g\left( \mathbf{x}\right)  = 0$ 确定的 $d - 1$ 维曲面上寻找能使目标函数 $f\left( \mathbf{x}\right)$ 最小化的点. 此时不难得到如下结论:

- 对于约束曲面上的任意点 $\mathbf{x}$ ,该点的梯度 $\nabla g\left( \mathbf{x}\right)$ 正交于约束曲面;

- 在最优点 ${\mathbf{x}}^{ * }$ ,目标函数在该点的梯度 $\nabla f\left( {\mathbf{x}}^{ * }\right)$ 正交于约束曲面.

由此可知,在最优点 ${\mathbf{x}}^{ * }$ ,如附图B. 1 所示,梯度 $\nabla g\left( \mathbf{x}\right)$ 和 $\nabla f\left( \mathbf{x}\right)$ 的方向必相同或相反,即存在 $\lambda  \neq  0$ 使得

$$
\nabla f\left( {\mathbf{x}}^{ * }\right)  + \lambda \nabla g\left( {\mathbf{x}}^{ * }\right)  = 0, \tag{B.1}
$$

λ称为拉格朗日乘子. 定义拉格朗日函数

$$
L\left( {\mathbf{x},\lambda }\right)  = f\left( \mathbf{x}\right)  + {\lambda g}\left( \mathbf{x}\right) , \tag{B.2}
$$

不难发现,将其对 $\mathbf{x}$ 的偏导数 ${\nabla }_{\mathbf{x}}L\left( {\mathbf{x},\lambda }\right)$ 置零即得式(B.1),同时,将其对 $\lambda$ 的偏导数 ${\nabla }_{\lambda }L\left( {\mathbf{x},\lambda }\right)$ 置零即得约束条件 $g\left( \mathbf{x}\right)  = 0$ . 于是,原约束优化问题可转化为对拉格朗日函数 $L\left( {\mathbf{x},\lambda }\right)$ 的无约束优化问题.

---

函数等值线与约束曲面相切.

可通过反证法证明: 若梯度 $\nabla f\left( {\mathbf{x}}^{ * }\right)$ 与约束曲面不正交，则仍可在约束曲面上移动该点使函数值进一步下降.

对等式约束, $\lambda$ 可能为正也可能为负.

---

![403_705_136_1105_469_0.jpg](../images/403_705_136_1105_469_0.jpg)

附图B. 1 拉格朗日乘子法的几何含义: 在 (a) 等式约束 $g\left( \mathbf{x}\right)  = 0$ 或 (b) 不等式约束 $g\left( \mathbf{x}\right)  \leq  0$ 下,最小化目标函数 $f\left( \mathbf{x}\right)$ . 红色曲线表示 $g\left( \mathbf{x}\right)  = 0$ 构成的曲面,而其围成的阴影区域表示 $g\left( \mathbf{x}\right)  < 0$ .

现在考虑不等式约束 $g\left( \mathbf{x}\right)  \leq  0$ ,如附图B. 1 所示，此时最优点 ${\mathbf{x}}^{ * }$ 或在 $g\left( \mathbf{x}\right)  < 0$ 的区域中,或在边界 $g\left( \mathbf{x}\right)  = 0$ 上. 对于 $g\left( \mathbf{x}\right)  < 0$ 的情形,约束 $g\left( \mathbf{x}\right)  \leq  0$ 不起作用,可直接通过条件 $\nabla f\left( \mathbf{x}\right)  = 0$ 来获得最优点; 这等价于将 $\lambda$ 置零然后对 ${\nabla }_{\mathbf{x}}L\left( {\mathbf{x},\lambda }\right)$ 置零得到最优点. $g\left( \mathbf{x}\right)  = 0$ 的情形类似于上面等式约束的分析,但需注意的是,此时 $\nabla f\left( {\mathbf{x}}^{ * }\right)$ 的方向必与 $\nabla g\left( {\mathbf{x}}^{ * }\right)$ 相反,即存在常数 $\lambda  > 0$ 使得 $\nabla f\left( {\mathbf{x}}^{ * }\right)  + \lambda \nabla g\left( {\mathbf{x}}^{ * }\right)  = 0$ . 整合这两种情形,必满足 ${\lambda g}\left( \mathbf{x}\right)  = 0$ . 因此, 在约束 $g\left( \mathbf{x}\right)  \leq  0$ 下最小化 $f\left( \mathbf{x}\right)$ ，可转化为在如下约束下最小化式(B.2) 的拉格朗日函数:

$$
\left\{  \begin{array}{l} g\left( \mathbf{x}\right)  \leq  0 \\  \lambda  \geq  0; \\  {\mu }_{j}{g}_{j}\left( \mathbf{x}\right)  = 0. \end{array}\right. \tag{B.3}
$$

式(B.3)称为 Karush-Kuhn-Tucker (简称KKT)条件.

上述做法可推广到多个约束. 考虑具有 $m$ 个等式约束和 $n$ 个不等式约束, 且可行域 $\mathbb{D} \subset  {\mathbb{R}}^{d}$ 非空的优化问题

$$
\mathop{\min }\limits_{\mathbf{x}}f\left( \mathbf{x}\right) \tag{B.4}
$$

$$
\text{ s.t. }{h}_{i}\left( \mathbf{x}\right)  = 0\;\left( {i = 1,\ldots , m}\right) \text{ , }
$$

$$
{g}_{j}\left( \mathbf{x}\right)  \leq  0\;\left( {j = 1,\ldots , n}\right) .
$$

引入拉格朗日乘子 $\mathbf{\lambda } = {\left( {\lambda }_{1},{\lambda }_{2},\ldots ,{\lambda }_{m}\right) }^{\mathrm{T}}$ 和 $\mathbf{\mu } = {\left( {\mu }_{1},{\mu }_{2},\ldots ,{\mu }_{n}\right) }^{\mathrm{T}}$ ,相应的拉格朗日函数为

$$
L\left( {\mathbf{x},\mathbf{\lambda },\mathbf{\mu }}\right)  = f\left( \mathbf{x}\right)  + \mathop{\sum }\limits_{{i = 1}}^{m}{\lambda }_{i}{h}_{i}\left( \mathbf{x}\right)  + \mathop{\sum }\limits_{{j = 1}}^{n}{\mu }_{j}{g}_{j}\left( \mathbf{x}\right) , \tag{B.5}
$$

由不等式约束引入的 KKT 条件 $\left( {j = 1,2,\ldots , n}\right)$ 为

$$
\left\{  \begin{array}{l} {g}_{j}\left( \mathbf{x}\right)  \leq  0 \\  {\mu }_{j} \geq  0 \\  {\mu }_{j}{g}_{j}\left( \mathbf{x}\right)  = 0 \end{array}\right. \tag{B.6}
$$

一个优化问题可以从两个角度来考察, 即 “主问题” (primal problem)和 “对偶问题” (dual problem). 对主问题(B.4), 基于式(B.5), 其拉格朗日 “对偶函数” (dual function) $\Gamma  : {\mathbb{R}}^{m} \times  {\mathbb{R}}^{n} \mapsto  \mathbb{R}$ 定义为

$$
\Gamma \left( {\mathbf{\lambda },\mathbf{\mu }}\right)  = \mathop{\inf }\limits_{{\mathbf{x} \in  \mathbb{D}}}L\left( {\mathbf{x},\mathbf{\lambda },\mathbf{\mu }}\right)
$$

$$
= \mathop{\inf }\limits_{{\mathbf{x} \in  \mathbb{D}}}\left( {f\left( \mathbf{x}\right)  + \mathop{\sum }\limits_{{i = 1}}^{m}{\lambda }_{i}{h}_{i}\left( \mathbf{x}\right)  + \mathop{\sum }\limits_{{j = 1}}^{n}{\mu }_{j}{g}_{j}\left( \mathbf{x}\right) }\right) \tag{B.7}
$$

若 $\widetilde{\mathbf{x}} \in  \mathbb{D}$ 为主问题(B.4)可行域中的点,则对任意 $\mathbf{\mu } \succcurlyeq  0$ 和 $\mathbf{\lambda }$ 都有

$$
\mathop{\sum }\limits_{{i = 1}}^{m}{\lambda }_{i}{h}_{i}\left( \mathbf{x}\right)  + \mathop{\sum }\limits_{{j = 1}}^{n}{\mu }_{j}{g}_{j}\left( \mathbf{x}\right)  \leq  0, \tag{B.8}
$$

进而有

$$
\Gamma \left( {\mathbf{\lambda },\mathbf{\mu }}\right)  = \mathop{\inf }\limits_{{\mathbf{x} \in  \mathbb{D}}}L\left( {\mathbf{x},\mathbf{\lambda },\mathbf{\mu }}\right)  \leq  L\left( {\widetilde{\mathbf{x}},\mathbf{\lambda },\mathbf{\mu }}\right)  \leq  f\left( \widetilde{\mathbf{x}}\right) . \tag{B.9}
$$

若主问题(B.4)的最优值为 ${p}^{ * }$ ,则对任意 $\mathbf{\mu } \succcurlyeq  0$ 和 $\mathbf{\lambda }$ 都有

$$
\Gamma \left( {\mathbf{\lambda },\mathbf{\mu }}\right)  \leq  {p}^{ * }, \tag{B.10}
$$

即对偶函数给出了主问题最优值的下界. 显然,这个下界取决于 $\mathbf{\mu }$ 和 $\mathbf{\lambda }$ 的值. 于是, 一个很自然的问题是: 基于对偶函数能获得的最好下界是什么? 这就引出了优化问题

$$
\mathop{\max }\limits_{{\mathbf{\lambda },\mathbf{\mu }}}\Gamma \left( {\mathbf{\lambda },\mathbf{\mu }}\right) \text{ s.t. }\mathbf{\mu } \succcurlyeq  0. \tag{B.11}
$$

---

在推导对偶问题时, 常通过将拉格朗日乘子 $L\left( {\mathbf{x},\mathbf{\lambda },\mathbf{\mu }}\right)$ 对 $\mathbf{x}$ 求导并令导数为 0 , 来获得对偶函数的表达形式.

$\mu  \succcurlyeq  0$ 表示 $\mu$ 的分量均为非负.

---

式(B.11)就是主问题(B.4)的对偶问题,其中 $\mathbf{\lambda }$ 和 $\mathbf{\mu }$ 称为 “对偶变量” (dual variable). 无论主问题(B.4)的凸性如何, 对偶问题(B.11)始终是凸优化问题.

考虑式(B.11)的最优值 ${d}^{ * }$ ,显然有 ${d}^{ * } \leq  {p}^{ * }$ ,这称为 “弱对偶性” (weak duality)成立; 若 ${d}^{ * } = {p}^{ * }$ ,则称为 “强对偶性” (strong duality)成立,此时由对偶问题能获得主问题的最优下界. 对于一般的优化问题, 强对偶性通常不成立. 但是,若主问题为凸优化问题,如式(B.4)中 $f\left( \mathbf{x}\right)$ 和 ${g}_{j}\left( \mathbf{x}\right)$ 均为凸函数, ${h}_{i}\left( \mathbf{x}\right)$ 为仿射函数，且其可行域中至少有一点使不等式约束严格成立，则此时强对偶性成立. 值得注意的是, 在强对偶性成立时, 将拉格朗日函数分别对原变量和对偶变量求导, 再并令导数等于零, 即可得到原变量与对偶变量的数值关系. 于是, 对偶问题解决了, 主问题也就解决了.

### B.2 二次规划

二次规划(Quadratic Programming, 简称 QP)是一类典型的优化问题, 包括凸二次优化和非凸二次优化. 在此类问题中, 目标函数是变量的二次函数, 而约束条件是变量的线性不等式.

假定变量个数为 $d$ ,约束条件的个数为 $m$ ,则标准的二次规划问题形如

$$
\mathop{\min }\limits_{\mathbf{x}}\frac{1}{2}{\mathbf{x}}^{\mathrm{T}}\mathbf{Q}\mathbf{x} + {\mathbf{c}}^{\mathrm{T}}\mathbf{x} \tag{B.12}
$$

$$
\text{ s.t. }\mathbf{A}\mathbf{x} \leq  \mathbf{b}\text{ , }
$$

其中 $\mathbf{x}$ 为 $d$ 维向量, $\mathbf{Q} \in  {\mathbb{R}}^{d \times  d}$ 为实对称矩阵, $\mathbf{A} \in  {\mathbb{R}}^{m \times  d}$ 为实矩阵, $\mathbf{b} \in  {\mathbb{R}}^{m}$ 和 $\mathbf{c} \in  {\mathbb{R}}^{d}$ 为实向量, $\mathbf{A}\mathbf{x} \leq  \mathbf{b}$ 的每一行对应一个约束.

若 $\mathbf{Q}$ 为半正定矩阵，则式(B.12)目标函数是凸函数，相应的二次规划是凸二次优化问题; 此时若约束条件 $\mathbf{A}\mathbf{x} \leq  \mathbf{b}$ 定义的可行域不为空，且目标函数在此可行域有下界,则该问题将有全局最小值. 若 $\mathbf{Q}$ 为正定矩阵,则该问题有唯一的全局最小值. 若 $\mathbf{Q}$ 为非正定矩阵,则式(B.12)是有多个平稳点和局部极小点的 NP 难问题.

常用的二次规划解法有椭球法(ellipsoid method)、内点法(interior point)、增广拉格朗日法(augmented Lagrangian)、梯度投影法(gradient projection) 等. 若 $\mathbf{Q}$ 为正定矩阵,则相应的二次规划问题可由椭球法在多项式时间内求解.

---

这称为 Slater 条件.

非标准二次规划问题中可以包含等式约束. 注意到等式约束能用两个不等式约束来代替；不等式约束可通过增加松弛变量的方式转化为等式约束.

---

### B.3 半正定规划

半正定规划(Semi-Definite Programming, 简称SDP)是一类凸优化问题, 其中的变量可组织成半正定对称矩阵形式, 且优化问题的目标函数和约束都是这些变量的线性函数.

给定 $d \times  d$ 的对称矩阵 $\mathbf{X}\text{ 、 }\mathbf{C}$ ,

$$
\mathbf{C} \cdot  \mathbf{X} = \mathop{\sum }\limits_{{i = 1}}^{d}\mathop{\sum }\limits_{{j = 1}}^{d}{C}_{ij}{X}_{ij} \tag{B.13}
$$

若 ${\mathbf{A}}_{i}\left( {i = 1,2,\ldots , m}\right)$ 也是 $d \times  d$ 的对称矩阵, ${b}_{i}\left( {i = 1,2,\ldots , m}\right)$ 为 $m$ 个实数, 则半正定规划问题形如

$$
\mathop{\min }\limits_{\mathbf{X}}\mathbf{C} \cdot  \mathbf{X} \tag{B.14}
$$

$$
\text{ s.t. }{\mathbf{A}}_{i} \cdot  \mathbf{X} = {b}_{i}, i = 1,2,\ldots , m
$$

$$
\mathbf{X} \succcurlyeq  0
$$

半正定规划与线性规划都拥有线性的目标函数和约束, 但半正定规划中的约束 $\mathbf{X} \succcurlyeq  0$ 是一个非线性、非光滑约束条件. 在优化理论中,半正定规划具有一定的一般性, 能将几种标准的优化问题(如线性规划、二次规划)统一起来.

常见的用于求解线性规划的内点法经过少许改造即可求解半正定规划问题, 但半正定规划的计算复杂度较高, 难以直接用于大规模问题.

### B.4 梯度下降法

梯度下降法(gradient descent)是一种常用的一阶(first-order)优化方法, 是求解无约束优化问题最简单、最经典的方法之一.

考虑无约束优化问题 $\mathop{\min }\limits_{\mathbf{x}}f\left( \mathbf{x}\right)$ ,其中 $f\left( \mathbf{x}\right)$ 为连续可微函数. 若能构造一个序列 ${\mathbf{x}}^{0},{\mathbf{x}}^{1},{\mathbf{x}}^{2},\ldots$ 满足

$$
f\left( {\mathbf{x}}^{t + 1}\right)  < f\left( {\mathbf{x}}^{t}\right) , t = 0,1,2,\ldots \tag{B.15}
$$

则不断执行该过程即可收敛到局部极小点. 欲满足式(B.15)，根据泰勒展式有

$$
f\left( {\mathbf{x} + \Delta \mathbf{x}}\right)  \simeq  f\left( \mathbf{x}\right)  + \Delta {\mathbf{x}}^{\mathrm{T}}\nabla f\left( \mathbf{x}\right) , \tag{B.16}
$$

于是,欲满足 $f\left( {\mathbf{x} + \Delta \mathbf{x}}\right)  < f\left( \mathbf{x}\right)$ ,可选择

$$
\Delta \mathbf{x} =  - \gamma \nabla f\left( \mathbf{x}\right) , \tag{B.17}
$$

---

$\mathbf{X} \succcurlyeq  0$ 表示 $\mathbf{X}$ 半正定.

一阶方法仅使用目标函数的一阶导数, 不利用其高阶导数.

---

其中步长 $\gamma$ 是一个小常数. 这就是梯度下降法.

若目标函数 $f\left( \mathbf{x}\right)$ 满足一些条件，则通过选取合适的步长，就能确保通过梯度下降收敛到局部极小点. 例如若 $f\left( \mathbf{x}\right)$ 满足 $L$ -Lipschitz 条件，则将步长设置为 $1/\left( {2L}\right)$ 即可确保收敛到局部极小点. 当目标函数为凸函数时,局部极小点就对应着函数的全局最小点, 此时梯度下降法可确保收敛到全局最优解.

当目标函数 $f\left( \mathbf{x}\right)$ 二阶连续可微时，可将式(B.16)替换为更精确的二阶泰勒展式, 这样就得到了牛顿法(Newton's method). 牛顿法是典型的二阶方法, 其迭代轮数远小于梯度下降法. 但牛顿法使用了二阶导数 ${\nabla }^{2}f\left( \mathbf{x}\right)$ ,其每轮迭代中涉及到海森矩阵(A.21)的求逆, 计算复杂度相当高, 尤其在高维问题中几乎不可行. 若能以较低的计算代价寻找海森矩阵的近似逆矩阵, 则可显著降低计算开销, 这就是拟牛顿法(quasi-Newton method).

### B.5 坐标下降法

坐标下降法(coordinate descent)是一种非梯度优化方法, 它在每步迭代中沿一个坐标方向进行搜索, 通过循环使用不同的坐标方向来达到目标函数的局部极小值.

不妨假设目标是求解函数 $f\left( \mathbf{x}\right)$ 的极小值,其中 $\mathbf{x} = {\left( {x}_{1},{x}_{2},\ldots ,{x}_{d}\right) }^{\mathrm{T}} \in \; {\mathbb{R}}^{d}$ 是一个 $d$ 维向量. 从初始点 ${\mathbf{x}}^{0}$ 开始,坐标下降法通过迭代地构造序列 ${\mathbf{x}}^{0},{\mathbf{x}}^{1},{\mathbf{x}}^{2},\ldots$ 来求解该问题, ${\mathbf{x}}^{t + 1}$ 的第 $i$ 个分量 ${x}_{i}^{t + 1}$ 构造为

$$
{x}_{i}^{t + 1} = \underset{y \in  \mathbb{R}}{\arg \min }f\left( {{x}_{1}^{t + 1},\ldots ,{x}_{i - 1}^{t + 1}, y,{x}_{i + 1}^{t},\ldots ,{x}_{d}^{t}}\right) . \tag{B.18}
$$

通过执行此操作，显然有

$$
f\left( {\mathbf{x}}^{0}\right)  \geq  f\left( {\mathbf{x}}^{1}\right)  \geq  f\left( {\mathbf{x}}^{2}\right)  \geq  \ldots \tag{B.19}
$$

与梯度下降法类似,通过迭代执行该过程,序列 ${\mathbf{x}}^{0},{\mathbf{x}}^{1},{\mathbf{x}}^{2},\ldots$ 能收敛到所期望的局部极小点或驻点(stationary point).

坐标下降法不需计算目标函数的梯度, 在每步迭代中仅需求解一维搜索问题, 对于某些复杂问题计算较为简便. 但若目标函数不光滑, 则坐标下降法有可能陷入非驻点(non-stationary point).

---

每步的步长 ${\gamma }_{t}$ 可不同.

$L$ -Lipschitz条件是指对于任意 $x$ ,存在常数 $L$ 使得 $\parallel \nabla f\left( \mathbf{x}\right) \parallel  \leq  L$ 成立.

求解极大值问题时亦称 “坐标上升法” (coordinate ascent).

---

## C 概率分布

### C.1 常见概率分布

本节简要介绍几种常见概率分布. 对于每种分布, 我们将给出概率密度函数以及期望 $\mathbb{E}\left\lbrack  \cdot \right\rbrack$ 、方差 $\operatorname{var}\left\lbrack  \cdot \right\rbrack$ 和协方差 $\operatorname{cov}\left\lbrack  {\cdot , \cdot  }\right\rbrack$ 等几个主要的统计量.

#### C.1.1 均匀分布

---

这里仅介绍连续均匀分布.

---

均匀分布(uniform distribution)是关于定义在区间 $\left\lbrack  {a, b}\right\rbrack  \left( {a < b}\right)$ 上连续变量的简单概率分布, 其概率密度函数如附图C. 1 所示.

$$
p\left( {x \mid  a, b}\right)  = \mathrm{U}\left( {x \mid  a, b}\right)  = \frac{1}{b - a}; \tag{C.1}
$$

$$
\mathbb{E}\left\lbrack  x\right\rbrack   = \frac{a + b}{2} \tag{C.2}
$$

$$
\operatorname{var}\left\lbrack  x\right\rbrack   = \frac{{\left( b - a\right) }^{2}}{12} \tag{C.3}
$$

![408_984_698_687_502_0.jpg](../images/408_984_698_687_502_0.jpg)

附图C. 1 均匀分布的概率密度函数

不难发现,若变量 $x$ 服从均匀分布 $\mathrm{U}\left( {x \mid  0,1}\right)$ 且 $a < b$ ,则 $a + \left( {b - a}\right) x$ 服从均匀分布 $\mathrm{U}\left( {x \mid  a, b}\right)$ .

#### C.1.2 伯努利分布

---

以瑞士数学家雅各布. 伯努利 (Jacob Bernoulli, 1654-1705)的名字命名.

---

伯努利分布(Bernoulli distribution)是关于布尔变量 $x \in  \{ 0,1\}$ 的概率分布,其连续参数 $\mu  \in  \left\lbrack  {0,1}\right\rbrack$ 表示变量 $x = 1$ 的概率.

$$
P\left( {x \mid  \mu }\right)  = \operatorname{Bern}\left( {x \mid  \mu }\right)  = {\mu }^{x}{\left( 1 - \mu \right) }^{1 - x}; \tag{C.4}
$$

$$
\mathbb{E}\left\lbrack  x\right\rbrack   = \mu ; \tag{C.5}
$$

$$
\operatorname{var}\left\lbrack  x\right\rbrack   = \mu \left( {1 - \mu }\right) . \tag{C.6}
$$

#### C.1.3 二项分布

二项分布(binomial distribution)用以描述 $N$ 次独立的伯努利实验中有 $m$ 次成功(即 $x = 1$ )的概率,其中每次伯努利实验成功的概率为 $\mu  \in  \left\lbrack  {0,1}\right\rbrack$ .

$$
P\left( {m \mid  N,\mu }\right)  = \operatorname{Bin}\left( {m \mid  N,\mu }\right)  = \left( \begin{array}{l} N \\  m \end{array}\right) {\mu }^{m}{\left( 1 - \mu \right) }^{N - m}; \tag{C.7}
$$

$$
\mathbb{E}\left\lbrack  x\right\rbrack   = {N\mu }; \tag{C.8}
$$

$$
\operatorname{var}\left\lbrack  x\right\rbrack   = {N\mu }\left( {1 - \mu }\right) . \tag{C.9}
$$

当 $N = 1$ 时,二项分布退化为伯努利分布.

#### C.1.4 多项分布

若将伯努利分布由单变量扩展为 $d$ 维向量 $\mathbf{x}$ ,其中 ${x}_{i} \in  \{ 0,1\}$ 且 $\mathop{\sum }\limits_{{i = 1}}^{d}{x}_{i} =$ 1,并假设 ${x}_{i}$ 取 1 的概率为 ${\mu }_{i} \in  \left\lbrack  {0,1}\right\rbrack  ,\mathop{\sum }\limits_{{i = 1}}^{d}{\mu }_{i} = 1$ ,则将得到离散概率分布

$$
P\left( {\mathbf{x} \mid  \dot{\mathbf{\mu }}}\right)  = \mathop{\prod }\limits_{{i = 1}}^{d}{\mu }_{i}^{{x}_{i}} \tag{C.10}
$$

$$
\mathbb{E}\left\lbrack  {x}_{i}\right\rbrack   = {\mu }_{i}; \tag{C.11}
$$

$$
\operatorname{var}\left\lbrack  {x}_{i}\right\rbrack   = {\mu }_{i}\left( {1 - {\mu }_{i}}\right) ; \tag{C.12}
$$

$$
\operatorname{cov}\left\lbrack  {{x}_{j},{x}_{i}}\right\rbrack   = \mathbb{I}\left\lbrack  {j = i}\right\rbrack  {\mu }_{i}. \tag{C.13}
$$

在此基础上扩展二项分布则得到多项分布(multinomial distribution), 它描述了在 $N$ 次独立实验中有 ${m}_{i}$ 次 ${x}_{i} = 1$ 的概率.

$$
P\left( {{m}_{1},{m}_{2},\ldots ,{m}_{d} \mid  N,\mathbf{\mu }}\right)  = \operatorname{Mult}\left( {{m}_{1},{m}_{2},\ldots ,{m}_{d} \mid  N,\mathbf{\mu }}\right)
$$

$$
= \frac{N!}{{m}_{1}!{m}_{2}!\ldots {m}_{d}!}\mathop{\prod }\limits_{{i = 1}}^{d}{\mu }_{i}^{{m}_{i}}; \tag{C.14}
$$

$$
\mathbb{E}\left\lbrack  {m}_{i}\right\rbrack   = N{\mu }_{i}; \tag{C.15}
$$

$$
\operatorname{var}\left\lbrack  {m}_{i}\right\rbrack   = N{\mu }_{i}\left( {1 - {\mu }_{i}}\right) ; \tag{C.16}
$$

$$
\operatorname{cov}\left\lbrack  {{m}_{j},{m}_{i}}\right\rbrack   =  - N{\mu }_{j}{\mu }_{i}. \tag{C.17}
$$

---

对于参数 $\mu$ ，二项分布的共轭先验分布是贝塔分布. 共轭分布参见 C.2.

对于参数 $\mu$ ,多项分布的共轭先验分布是狄利克雷分布. 共轭分布参见 C.2.

---

#### C.1.5 贝塔分布

贝塔分布(Beta distribution)是关于连续变量 $\mu  \in  \left\lbrack  {0,1}\right\rbrack$ 的概率分布,它由两个参数 $a > 0$ 和 $b > 0$ 确定,其概率密度函数如附图C. 2 所示.

$$
p\left( {\mu  \mid  a, b}\right)  = \operatorname{Beta}\left( {\mu  \mid  a, b}\right)  = \frac{\Gamma \left( {a + b}\right) }{\Gamma \left( a\right) \Gamma \left( b\right) }{\mu }^{a - 1}{\left( 1 - \mu \right) }^{b - 1}
$$

$$
= \frac{1}{B\left( {a, b}\right) }{\mu }^{a - 1}{\left( 1 - \mu \right) }^{b - 1}; \tag{C.18}
$$

$$
\mathbb{E}\left\lbrack  \mu \right\rbrack   = \frac{a}{a + b}; \tag{C.19}
$$

$$
\operatorname{var}\left\lbrack  \mu \right\rbrack   = \frac{ab}{{\left( a + b\right) }^{2}\left( {a + b + 1}\right) }, \tag{C.20}
$$

![410_921_570_764_648_0.jpg](../images/410_921_570_764_648_0.jpg)

附图C. 2 贝塔分布的概率密度函数

其中 $\Gamma \left( a\right)$ 为 Gamma 函数

$$
\Gamma \left( a\right)  = {\int }_{0}^{+\infty }{t}^{a - 1}{e}^{-t}\mathrm{\;d}\mathrm{t} \tag{C.21}
$$

$B\left( {a, b}\right)$ 为 Beta 函数

$$
B\left( {a, b}\right)  = \frac{\Gamma \left( a\right) \Gamma \left( b\right) }{\Gamma \left( {a + b}\right) }. \tag{C.22}
$$

当 $a = b = 1$ 时,贝塔分布退化为均匀分布.

#### C.1.6 狄利克雷分布

狄利克雷分布(Dirichlet distribution) 是关于一组 $d$ 个连续变量 ${\mu }_{i} \in  \left\lbrack  {0,1}\right\rbrack$ 的概率分布, $\mathop{\sum }\limits_{{i = 1}}^{d}{\mu }_{i} = 1$ . 令 $\mathbf{\mu } = \left( {{\mu }_{1};{\mu }_{2};\ldots ;{\mu }_{d}}\right)$ ,参数 $\mathbf{\alpha } = \left( {{\alpha }_{1};{\alpha }_{2};\ldots ;{\alpha }_{d}}\right)$ , ${\alpha }_{i} > 0,\widehat{\alpha } = \mathop{\sum }\limits_{{i = 1}}^{d}{\alpha }_{i}.$

$$
p\left( {\mathbf{\mu } \mid  \mathbf{\alpha }}\right)  = \operatorname{Dir}\left( {\mathbf{\mu } \mid  \mathbf{\alpha }}\right)  = \frac{\Gamma \left( \widehat{\alpha }\right) }{\Gamma \left( {\alpha }_{1}\right) \ldots \Gamma \left( {\alpha }_{i}\right) }\mathop{\prod }\limits_{{i = 1}}^{d}{\mu }_{i}^{{\alpha }_{i} - 1}; \tag{C.23}
$$

$$
\mathbb{E}\left\lbrack  {\mu }_{i}\right\rbrack   = \frac{{\alpha }_{i}}{\widehat{\alpha }}; \tag{C.24}
$$

$$
\operatorname{var}\left\lbrack  {\mu }_{i}\right\rbrack   = \frac{{\alpha }_{i}\left( {\widehat{\alpha } - {\alpha }_{i}}\right) }{{\widehat{\alpha }}^{2}\left( {\widehat{\alpha } + 1}\right) }; \tag{C.25}
$$

$$
\operatorname{cov}\left\lbrack  {{\mu }_{j},{\mu }_{i}}\right\rbrack   = \frac{{\alpha }_{j}{\alpha }_{i}}{{\widehat{\alpha }}^{2}\left( {\widehat{\alpha } + 1}\right) }. \tag{C.26}
$$

当 $d = 2$ 时,狄利克雷分布退化为贝塔分布.

#### C.1.7 高斯分布

高斯分布(Gaussian distribution)亦称正态分布(normal distribution)，是应用最为广泛的连续概率分布.

$\sigma$ 为标准差.

对于单变量 $x \in  \left( {-\infty ,\infty }\right)$ ,高斯分布的参数为均值 $\mu  \in  \left( {-\infty ,\infty }\right)$ 和方差 ${\sigma }^{2} > 0$ . 附图C. 3 给出了在几组不同参数下高斯分布的概率密度函数.

$$
p\left( {x \mid  \mu ,{\sigma }^{2}}\right)  = \mathcal{N}\left( {x \mid  \mu ,{\sigma }^{2}}\right)  = \frac{1}{\sqrt{{2\pi }{\sigma }^{2}}}\exp \left\{  {-\frac{{\left( x - \mu \right) }^{2}}{2{\sigma }^{2}}}\right\}  ; \tag{C.27}
$$

$$
\mathbb{E}\left\lbrack  x\right\rbrack   = \mu ; \tag{C.28}
$$

$$
\operatorname{var}\left\lbrack  x\right\rbrack   = {\sigma }^{2}. \tag{C.29}
$$

对于 $d$ 维向量 $\mathbf{x}$ ,多元高斯分布的参数为 $d$ 维均值向量 $\mathbf{\mu }$ 和 $d \times  d$ 的对称正定协方差矩阵 $\mathbf{\sum }$ .

$$
p\left( {\mathbf{x} \mid  \mathbf{\mu },\mathbf{\sum }}\right)  = \mathcal{N}\left( {\mathbf{x} \mid  \mathbf{\mu },\mathbf{\sum }}\right)
$$

$$
= \frac{1}{\sqrt{{\left( 2\pi \right) }^{d}\det \left( \mathbf{\sum }\right) }}\exp \left\{  {-\frac{1}{2}{\left( \mathbf{x} - \mathbf{\mu }\right) }^{\mathrm{T}}{\mathbf{\sum }}^{-1}\left( {\mathbf{x} - \mathbf{\mu }}\right) }\right\}  ; \tag{C.30}
$$

$$
\mathbb{E}\left\lbrack  \mathbf{x}\right\rbrack   = \mathbf{\mu }; \tag{C.31}
$$

$$
\operatorname{cov}\left\lbrack  x\right\rbrack   = \sum . \tag{C.32}
$$

---

以德国数学家狄利克雷 (1805-1859)的名字命名.

---

![412_761_132_1091_618_0.jpg](../images/412_761_132_1091_618_0.jpg)

附图C. 3 高斯分布的概率密度函数

### C.2 共轭分布

假设变量 $x$ 服从分布 $P\left( {x \mid  \Theta }\right)$ ,其中 $\Theta$ 为参数, $X = \left\{  {{x}_{1},{x}_{2},\ldots ,{x}_{m}}\right\}$ 为变量 $x$ 的观测样本,假设参数 $\Theta$ 服从先验分布 $\Pi \left( \Theta \right)$ . 若由先验分布 $\Pi \left( \Theta \right)$ 和抽样分布 $P\left( {X \mid  \Theta }\right)$ 决定的后验分布 $F\left( {\Theta  \mid  X}\right)$ 与 $\Pi \left( \Theta \right)$ 是同种类型的分布,则称先验分布 $\Pi \left( \Theta \right)$ 为分布 $P\left( {x \mid  \Theta }\right)$ 或 $P\left( {X \mid  \Theta }\right)$ 的共轭分布(conjugate distribution).

例如,假设 $x \sim  \operatorname{Bern}\left( {x \mid  \mu }\right) , X = \left\{  {{x}_{1},{x}_{2},\ldots ,{x}_{m}}\right\}$ 为观测样本, $\bar{x}$ 为观测样本的均值, $\mu  \sim  \operatorname{Beta}\left( {\mu  \mid  a, b}\right)$ ,其中 $a, b$ 为已知参数,则 $\mu$ 的后验分布

$$
F\left( {\mu  \mid  X}\right)  \propto  \operatorname{Beta}\left( {\mu  \mid  a, b}\right) P\left( {X \mid  \mu }\right)
$$

$$
= \frac{{\mu }^{a - 1}{\left( 1 - \mu \right) }^{b - 1}}{B\left( {a, b}\right) }{\mu }^{m\bar{x}}{\left( 1 - \mu \right) }^{m - m\bar{x}}
$$

$$
= \frac{1}{B\left( {a + m\bar{x}, b + m - m\bar{x}}\right) }{\mu }^{a + m\bar{x} - 1}{\left( 1 - \mu \right) }^{b + m - m\bar{x} - 1}
$$

$$
= \operatorname{Beta}\left( {\mu  \mid  {a}^{\prime },{b}^{\prime }}\right) , \tag{C.33}
$$

亦为贝塔分布,其中 ${a}^{\prime } = a + m\bar{x},{b}^{\prime } = b + m - m\bar{x}$ ,这意味着贝塔分布与伯努利分布共轭. 类似可知，多项分布的共轭分布是狄利克雷分布，而高斯分布的共轭分布仍是高斯分布.

---

这里仅考虑高斯分布方差已知、均值服从先验的情形.

---

先验分布反映了某种先验信息, 后验分布既反映了先验分布提供的信息、 又反映了样本提供的信息. 当先验分布与抽样分布共轭时, 后验分布与先验分布属于同种类型, 这意味着先验信息与样本提供的信息具有某种同一性. 于是, 若使用后验分布作为进一步抽样的先验分布, 则新的后验分布仍将属于同种类型. 因此, 共轭分布在不少情形下会使问题得以简化. 例如在式(C.33)的例子中，对服从伯努利分布的事件 $X$ 使用贝塔先验分布，则贝塔分布的参数值 $a$ 和 $b$ 可视为对伯努利分布的真实情况(事件发生和不发生)的预估. 随着 “证据” (样本)的不断到来,贝塔分布的参数值从 $a, b$ 变化为 $a + m\bar{x}, b + m - m\bar{x}$ , 且 $a/\left( {a + b}\right)$ 将随着 $m$ 的增大趋近于伯努利分布的真实参数值 $\bar{x}$ . 显然,使用共轭先验之后,只需调整 $a$ 和 $b$ 这两个预估值即可方便地进行模型更新.

### C.3 KL散度

KL散度(Kullback-Leibler divergence), 亦称相对熵(relative entropy)或信息散度(information divergence)，可用于度量两个概率分布之间的差异. 给定两个概率分布 $P$ 和 $Q$ ,二者之间的KL散度定义为

$$
\operatorname{KL}\left( {P\parallel Q}\right)  = {\int }_{-\infty }^{\infty }p\left( x\right) \log \frac{p\left( x\right) }{q\left( x\right) }\mathrm{d}x, \tag{C.34}
$$

其中 $p\left( x\right)$ 和 $q\left( x\right)$ 分别为 $P$ 和 $Q$ 的概率密度函数.

KL散度满足非负性, 即

$$
\operatorname{KL}\left( {P\parallel Q}\right)  \geq  0, \tag{C.35}
$$

当且仅当 $P = Q$ 时 $\mathrm{{KL}}\left( {P\parallel Q}\right)  = 0$ . 但是, $\mathrm{{KL}}$ 散度不满足对称性,即

$$
\operatorname{KL}\left( {P\parallel Q}\right)  \neq  \operatorname{KL}\left( {Q\parallel P}\right) , \tag{C.36}
$$

因此, KL散度不是一个度量(metric).

若将KL散度的定义 (C.34) 展开, 可得

$$
\mathrm{{KL}}\left( {P\parallel Q}\right)  = {\int }_{-\infty }^{\infty }p\left( x\right) \log p\left( x\right) \mathrm{d}x - {\int }_{-\infty }^{\infty }p\left( x\right) \log q\left( x\right) \mathrm{d}x
$$

$$
=  - H\left( P\right)  + H\left( {P, Q}\right) , \tag{C.37}
$$

其中 $H\left( P\right)$ 为熵(entropy), $H\left( {P, Q}\right)$ 为 $P$ 和 $Q$ 的交叉熵(cross entropy). 在信息论中,熵 $H\left( P\right)$ 表示对来自 $P$ 的随机变量进行编码所需的最小字节数,而交叉熵 $H\left( {P, Q}\right)$ 则表示使用基于 $Q$ 的编码对来自 $P$ 的变量进行编码所需的字节数. 因此, KL散度可认为是使用基于 $Q$ 的编码对来自 $P$ 的变量进行编码所需的 “额外” 字节数; 显然,额外字节数必然非负,当且仅当 $P = Q$ 时额外字节数为零.

---

这里假设两个分布均为连续型概率分布; 对于离散型概率分布, 只需将定义中的积分替换为对所有离散值遍历求和.

度量应满足四个基本性质, 参见9.3节.

---

<table><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td>-</td><td></td></tr></table>

## 后 记

写作本书的主因, 是 2016 年准备在南京大学开设 “机器学习” 课. 十五年前笔者曾主张开设此课, 但那时国内对机器学习闻之不多, 不少人听到这个名字的第一反应是 “学习什么机器?” 学校估计学生兴趣不大, 于是笔者开设了 “数据挖掘” 这门名字听上去就觉得很有用的课. 被评为省优秀研究生课程后, 又给本科生单开了一门 “数据挖掘导论”. 这两门课很受欢迎, 选修学生很多, 包括不少外来蹭听生. 虽然课上有一多半其实在讲机器学习, 但笔者仍一直希望专开一门机器学习课, 因笔者以为机器学习迟早会变成计算机学科的基础内容.

图灵奖得主 E. W. Dijkstra 曾说 “计算机科学并不仅是关于计算机, 就像天文学并不仅是关于望远镜”. 正如天文学早期的研究关注如何制造望远镜, 计算机科学早期研究是在关注如何令计算机运转. 到了今天，建造强大的天文望远镜虽仍重要，但天文学更要紧的是 “用”望远镜来开展研究. 类似地, 计算机科学发展至今, 也该到了从关注 “造” 计算机转入更关注 “用” 计算机来认识和改造世界的阶段, 其中最重要的无疑是用计算机对数据进行分析, 因为这是计算的主要目的, 而这就离不开机器学习. 十多年前在国内某次重要论坛上笔者刚抛出此观点就被专家迎头指斥, 但今日来看, 甚至很多计算机学科外人士都已对机器学习的重大价值津津乐道, 现在才开设机器学习基础课似乎已有点嫌晚了.

1995 年在南大图书馆偶然翻看了《机器学习: 通往人工智能的途径》, 这算是笔者接触机器学习的开始. 那时机器学习在国内问津者寥, 甚至连科研人员申请基金项目也无合适代码方向可报. 周边无专家可求教，又因国内科研经费匮乏而几无国际交流，加之学校尚无互联网和电子文献库， 能看到的最新文献仅是两年前出版且页数不全的某 IEEE 汇刊……可谓举步维艰, 经历的困惑和陷阱不可胜数. 笔者切身体会到, 入门阶段接触的书籍是何等重要, 对自学者尤甚. 一本好书能让人少走许多弯路, 材料不佳则后续要花费数倍精力方能纠偏. 中文书当然要国人自己来写. 虽已不需靠 “写书出名”, 且深知写教科书极耗时间精力, 但踌躇后笔者仍决定动手写这本书, 唯望为初学者略尽绵薄之力.

有人说 “一千个人眼中就有一千个哈姆雷特”，一个学科何尝不是如此. 之所以不欲使用市面上流行的教科书(主要是英文的), 除了觉得对大多数中国学生来说中文教科书更便于学习, 另一个原因则是希望从笔者自己的视角来展现机器学习.

2013 年中开始规划提纲, 由此进入了焦躁的两年. 该写哪些内容、先写什么后写什么、从哪个角度写、写到什么程度, 总有千丝万缕需考虑. 及至写作进行, 更是战战兢兢, 深恐不慎误人子弟. 写书难, 写教科书更难. 两年下来, 甘苦自知. 子曰: “取乎其上, 得乎其中; 取乎其中, 得乎其下”, 且以顶级的态度, 出一本勉强入得方家法眼之书.

本书贯穿以西瓜为例，一则因为瓜果中笔者尤喜西瓜，二则因为西瓜在笔者所生活的区域有个有趣的蕴义. 朋友小聚、请客吃饭, 菜已全而主未知, 或馔未齐而人待走, 都挺尴尬. 于是聪明人发明了“潜规则”: 席终上西瓜. 无论整盘抑或小碟, 宾主见瓜至, 则心领神会准备起身, 皆大欢喜. 久而久之，无论菜肴价格贵贱、场所雅鄙，宴必有西瓜. 若将宴席比作(未来)应用系统，菜肴比作所涉技术, 则机器学习好似那必有的西瓜, 它可能不是最 “高大上” 的, 但却是离不了的、没用上总觉得不甘心的.

本书写作过程从材料搜集，到习题设计，再到阅读校勘，都得到了笔者的很多学生、同事和学术界朋友的支持和帮助, 在此谨列出他们的姓名以致谢意(姓氏拼音序): 陈松灿, 戴望州, 高阳, 高尉, 黄圣君, 黎铭, 李楠, 李武军, 李宇峰, 钱超, 王魏, 王威廉, 吴建鑫, 徐森, 俞扬, 詹德川, 张利军, 张敏灵, 朱军. 书稿在 LAMDA 组学生 2015 年暑期讨论班上试讲, 高斌斌、郭翔宇、李绍园、钱鸿、沈芷玉、叶翰嘉、张腾等同学又帮助发现了许多笔误. 特别感谢李楠把笔者简陋的手绘图转变为精致的插图, 俞扬帮助调整排版格式和索引, 刘冲把笔者对封面设计的想法具体表现出来.

中国计算机学会终身成就奖得主、中国科学院院士陆汝钤先生是我国人工智能事业的开拓者之一, 他在 1988 年和 1996 年出版的《人工智能》(上、下册)曾给予笔者很多启发. 承蒙陆老师厚爱在百忙中为本书作序，不胜惶恐之至. 陆老师在序言中提出的问题很值得读者在本书之后的进阶学习与研究中深思.

感谢清华大学出版社薛慧老师为本书出版所做的努力. 十二年前笔者入选国家杰出青年科学基金时薛老师即邀著书，笔者以年纪尚轻、学力未逮婉辞. 十年前“机器学习及其应用” 研讨会(MLA)从陆汝钤院士肇始的复旦大学智能信息处理重点实验室移师南京，参会人数从复旦最初的 20 人, 发展到 2010 年 400 余人, 此后在清华、复旦、西电达 800 余人, 今年再回南大竟至 1300 余人，场面热烈. MLA 倡导 “学术至上、其余从简”，不搞繁文缛节，参会免费. 但即便如此，仍有很多感兴趣的师生因旅费不菲而难以参加. 于是笔者提议每两年以《机器学习及其应用》为题出版一本报告选集以飨读者. 这个主意得到了薛老师、陆老师以及和笔者一起长期组织 MLA、去年因病去世的王珏老师的大力支持. 此类专业性学术文集销量不大, 出版社多半要贴钱. 笔者曾跟薛老师说，自著的第一本中文书必交由薛老师在清华出版，或可稍为出版社找补. 转眼《机器学习及其应用》系列已出到第六本，薛老师或以为十年前是玩笑话，某日告之书快完稿时她蓦然惊喜.

最后要感谢笔者的家人，本书几乎耗尽了两年来笔者所有的节假日和空闲时间. 写作时垂髫犬子常跑来案边，不是问“爸爸去哪儿？”而是看几眼然后问“爸爸你又写了几页？”为了给他满意的答复, 笔者埋头努力.

周志华

2015 年 11 月于南京渐宽斋

## 索 引

0/1损失函数, 130, 147

5 × 2 交叉验证, 41

$\epsilon$ -贪心,374

AdaBoost, 173

ART网络, 108

Bagging, 178

Bellman等式, 380

Boltzmann分布, 111

Boltzmann机, 111

Boosting, 173, 190

BP算法, 101

BP网络, 101

C4.5决策树, 78, 83

CART决策树, 79

ECOC, 64

Elman网络, 111

EM算法, 162, 208, 295, 335

${F1},{32}$

Fisher判别分析, 60

Friedman检验, 42

Frobenius 范数, 400

Hoeffding不等式, 192, 268

hinge损失, 130

ID3决策树, 75

ILP, 357, 364

Jensen不等式, 268

$K$ -摇臂赌博机, 373

KKT条件, 124, 132, 135

KL散度, 335, 414

Kohonen网络, 109

$k$ 折交叉验证,26

$k$ 近邻,225

$k$ 均值算法,202,218

${\mathrm{L}}_{1}$ 正则化,253

${\mathrm{L}}_{2}$ 正则化,253

LASSO, 252, 261

Lipschitz条件, 253

LVQ, 204, 218

M-P神经元模型, 97

McDiarmid不等式, 268

MCMC, 331

McNemar检验, 41

MDP, 371

Mercer定理, 137, 139

MH算法, 333

MvM, 63

Nemenyi后续检验, 43

OvO, 63

OvR, 63

P-R曲线, 31

PAC辨识, 269

PAC可学习, 269

PAC学习算法, 270

PCA, 229

Q-学习, 387, 393

Rademacher复杂度, 279

RBF网络, 108

ReLU, 114

RIPPER, 353

RKHS, 128

ROC曲线, 33, 46

S3VM, 298

Sarsa 算法, 387, 390

Sigmoid函数, 58, 98, 102

Softmax, 375

SOM网络, 109

Stacking, 184

SVM, 123

TD学习, 386, 393

Tikhonov正则化, 252

VC维, 273, 274

V型结构, 158

WEKA, 16

奥卡姆剃刀, 7, 17

版本空间, 5

半监督聚类, 240, 307

半监督学习, 293, 294

半监督支持向量机, 298

半朴素贝叶斯分类器, 154

半正定规划, 407

包裹式特征选择, 250

包外估计, 27, 179

贝塔分布, 411

贝叶斯定理, 148

贝叶斯分类器, 164

贝叶斯风险, 147

贝叶斯决策论, 147

贝叶斯模型平均, 185

贝叶斯网, 156, 319, 339

贝叶斯学习, 164

贝叶斯最优分类器, 147

本真低维空间，232

本真距离, 234

必连约束, 239, 307

边际独立性, 158

边际分布, 328

边际化, 158, 328

边际似然, 163

编码矩阵, 65

变分推断, 334

变量消去, 328

标记, 2

标记传播, 302

标记空间, 3

表格值函数, 388

表示定理, 137

表示学习, 114

伯努利分布, 409

不可分, 269, 272

不可知PAC可学习, 273

不一致, 269

参数估计, 54

参数调节, 28

参数空间, 106

策略, 372

策略迭代, 381

测地线距离, 234

测试, 3

测试样本, 3

层次聚类, 214

查全率, 30

查询, 293

查准率, 30

差异性度量, 187

超父，155

成对马尔可夫性, 325

冲突消解, 348

重采样, 177

重赋权, 177

簇, 3, 197

错误率, 23, 29

打散, 273

带序规则, 348

代价, 35, 47

代价矩阵, 35

代价敏感, 36, 67

代价曲线, 36

单隐层网络, 101

道德图, 158

等度量映射，234

低密度分隔, 298

低维嵌入, 226

低秩矩阵近似, 402

狄利克雷分布, 412

递归神经网络, 111

典型相关分析, 240

独立同分布, 3, 267

独依赖估计, 154

度量学习, 237

端正图, 158

对比散度, 112

对分, 273

对率函数, 58

对率回归, 58, 132, 325

对率损失, 130

对偶函数, 405

对偶问题, 123, 405

对数几率函数, 58, 98

对数几率回归, 57

对数似然, 59, 149

对数线性回归, 56

多变量决策树, 88, 92

多标记学习, 68

多层前馈神经网络, 100

多分类, 3

多分类器系统, 171

多分类学习, 63

多核学习, 140

多视图学习, 240, 304

多维缩放, 227

多项分布, 410

多样性, 172

多样性度量, 187

多元线性回归, 55

二次规划, 406

二分类, 3

二项分布, 410

二项检验, 38

发散, 113

罚函数法, 133

反向传播算法, 101

泛化, 3, 121, 350

泛化误差, 23, 267

非参数化方法, 340

非度量距离, 201

非线性降维, 232

非线性可分, 99

分层采样, 25

分而治之, 74

分类, 3

分歧, 185, 304

风险, 147

符号主义, 10, 363

概率近似正确, 268

概率模型, 206, 319

概率图模型, 156, 319

概念类, 268

概念学习, 4, 17

感知机, 98

高斯份布, 412

高斯核, 128

高斯混合, 206, 296

割平面法, 139

个体学习器, 171

功能神经元, 99

共轭分布, 413

关系学习, 363

广义 $\delta$ 规则,115

广义瑞利商, 61

广义线性模型, 57

规范化, 36, 183

规则, 347

规则学习, 347

归结商, 362

归纳, 359

归纳逻辑程序设计, 357, 364

归纳偏好, 6

归纳学习, 4, 11

归一化, 36

过采样, 67

过滤式特征选择, 249

过拟合, 23, 104, 191, 352

过配, 23

行列式, 399

豪斯多夫距离, 220

核范数, 260

核方法, 137

核函数, 126

核化, 137, 232

核化线性降维, 232

核技巧, 127

核矩阵, 128, 138, 233

核线性判别分析, 137

核主成分分析, 232

合一, 361

宏F1,32

宏查全率, 32

宏查准率, 32

后剪枝, 79, 352

划分超平面, 121, 298

划分选择, 75, 92

话题模型, 337

回归, 3

汇合, 114

混合属性, 201

混合专家, 191, 313

混淆矩阵, 30

基尼指数, 79

基学习器, 171

基学习算法, 171

基于分歧的方法, 304

基于能量的模型, 111

机械学习, 11

迹, 399

迹范数, 260

激活函数, 98

吉布斯采样, 161, 334

极大似然法, 59, 149, 297

极大似然估计, 149, 328

集成修剪, 191

集成学习, 171, 311

急切学习, 225

级联相关, 110

挤压函数, 98

几率, 58

计算学习理论, 267

加权距离, 201

加权平均, 182, 225

加权投票, 183, 225

加性模型, 173

假设, 2, 269

假设检验, 37

假设空间, 268

监督学习, 3

间隔, 122

简单平均, 182

剪枝, 79, 352

奖赏, 371

降维, 227

交叉验证成对 $t$ 检验,40

交叉验证法, 26

交叉熵, 415

街区距离, 200

阶跃函数, 57, 98

结构风险, 133

近端梯度下降，253，259

近邻成分分析, 238

近似动态规划, 393

近似推断, 161, 328, 331

精度, 23, 29

精确推断, 161, 328

经验风险, 133

经验风险最小化, 278

经验误差, 23, 267

径向基函数, 108

竞争型学习, 108

纠错输出码, 64

局部极小, 106

局部马尔可夫性, 324

局部线性嵌入, 235

矩阵补全, 259

聚类, 3, 197

聚类集成, 219

聚类假设, 294

距离度量, 199

距离度量学习, 201, 237

卷积神经网络，113

决策树, 73, 363

决策树桩, 82

绝对多数投票, 182

均方误差, 29, 54

均匀分布, 409

均匀稳定性, 285

可分, 269, 270

可解释性, 115, 191

可塑性-稳定性窘境, 109

拉格朗日乘子法, 403

拉普拉斯修正, 153

拉斯维加斯方法, 251

懒惰学习, 154, 225, 240

累积误差逆传播，105

类比学习, 11

类别不平衡, 66, 299

类间散度矩阵, 61, 138

类内散度矩阵, 61, 138

离散化, 83

离散属性, 200

联系函数, 57

连接权, 101, 104

连接主义, 10

连续属性, 200

链式法则, 103, 402

列联表, 41, 187

列名属性, 200

岭回归, 252

留出法, 25

流形假设, 240, 294

流形学习, 234

流形正则化, 240

逻辑文字, 347

码书学习, 255

马尔可夫决策过程, 371

马尔可夫链, 161, 320

马尔可夫随机场, 322

马尔可夫毯, 325

马尔可夫网, 319

曼哈顿距离, 200

没有免费的午餐定理, 9

蒙特卡罗方法, 251, 340, 384

密采样, 226

密度聚类, 211

免模型学习, 382

闵可夫斯基距离, 200, 220

命题规则, 348

模仿学习, 390

模拟退火，107

模型选择, 24

默认规则, 348

逆归结, 359

逆强化学习, 391

欧氏距离, 200

盘式记法, 334

判别式模型, 148, 325

判定树, 73

偏差-方差分解, 44, 177

偏好, 6

平方损失, 54

平衡点, 31

平均场, 337

平均法, 225

平稳分布, 161

朴素贝叶斯分类器, 150

奇异值分解, 231, 402

恰PAC可学习, 270

迁移学习, 17

嵌入式特征选择, 252

欠采样, 67

欠拟合, 23

欠配, 23

强化学习, 371

切比雪夫距离, 200

亲和矩阵, 301

权共享, 113

全局马尔可夫性, 323

全局散度矩阵, 62

全局最小, 106

缺省规则, 348

缺失值, 85

人工神经网络，97

人工智能，10

冗余特征, 247

软间隔, 129

软间隔支持向量机, 131

弱学习器, 171

熵, 415

上采样, 67

深度学习, 113

神经网络, 97

神经元, 97

生成式模型, 148, 295, 325

胜者通吃, 108

时间复杂度, 269

时序差分学习, 386, 393

示教学习, 11

示例, 2

势函数, 322

视图, 304

收敛，99

受限 Boltzmann 机, 112

属性, 2

属性空间，2

属性子集，189

数据集，2

数据挖掘, 14

数据预处理, 247

数值属性, 200

似然, 148

似然率, 352

松弛变量, 130

随机森林, 179

随机子空间, 189

探索-利用窘境, 374

特化, 350

特征, 2, 247

特征工程, 114

特征向量, 2

特征选择, 247

特征学习, 114

梯度下降, 102, 254, 389, 407

替代函数, 58

替代损失, 130

条件独立性假设, 150, 305

条件风险，147

条件随机场, 325

同父，158

统计关系学习, 364

统计学习, 12, 139

投票法, 172, 225

图半监督学习, 300

推断, 319

微F1,32

微查全率，32

微查准率, 32

维数约简, 227

维数灾难, 227, 247

未标记样本, 293

稳定基学习器, 189

稳定性, 284

无导师学习, 3

无关特征, 247

无监督学习, 3, 197

无监督逐层训练，113

无序属性, 200

勿连约束, 239, 307

误差, 23

误差一分歧分解, 185

误差逆传播，101

稀疏编码，255

稀疏表示，67,255

稀疏性，67

下采样，67

先验, 148

线性超平面, 99

线性核, 128

线性回归, 53, 252

线性降维, 229

线性可分, 99, 126

线性模型, 53

线性判别分析, 60, 139

相对多数投票, 183

相对熵, 414

相关特征, 247

相似度度量, 201

协同过滤, 259

协同训练, 304

斜决策树, 90

信念传播, 330, 340

信念网, 156

信息散度, 414

信息增益, 75, 248

信息熵, 75

序贯覆盖, 349

选择性集成, 191

学习, 2

学习率, 99

学习器, 2

学习向量量化, 204

训练，2

训练集, 2

训练误差, 23

训练样本, 2

压缩感知, 257

哑结点, 99

演绎, 359

验证集, 28, 105

样本, 2

样本复杂度, 270

样本空间, 2

样例, 2

一阶规则, 348

一致性，140

遗传算法，107

异常检测, 219

因子, 322

隐变量, 162, 319

隐狄利克雷分配模型, 337

隐马尔可夫模型, 319

硬间隔, 129

优先级规则, 348

有标记样本, 293

有导师学习, 3

有模型学习, 377

有限假设空间, 270

有向分离, 158

有效性指标, 197

有序属性, 200

预剪枝, 79, 352

阈值, 97, 104

阈值逻辑单元, 98

阈值移动，67

元规则, 348

原型聚类, 202

原子命题, 348

再励学习, 371

再平衡, 67

再生核希尔伯特空间, 128

再缩放, 67

在线学习, 109, 241, 393

早停, 105

增长函数, 273

增量学习, 92, 109

增益率, 77

召回率, 30

真相, 2

振荡, 99

正态分布, 412

正则化, 56, 105, 133

证据, 148

支持向量，122

支持向量回归，133

支持向量机，123

支持向量展式, 127

直推学习, 295

值迭代, 382

值函数近似, 388

指数损失, 130, 173

置换, 361

置信度, 38

主成分分析, 229

主动学习, 293

状态-动作值函数, 377

状态值函数, 377

准确率, 30

子集评价，248

子集搜索, 248

子空间, 189, 227

自适应谐振理论, 108

自助采样法, 178

自助法, 27

自组织映射, 109

字典学习, 255

总体代价, 36

最近邻分类器, 225

最小二乘法, 54, 72

最小描述长度, 159

最小一般泛化, 358

最一般合一置换, 361

坐标下降, 163, 408

<table><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr></table>

MACHINE

LEARNIC
