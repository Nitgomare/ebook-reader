# 第10章 降维与度量学习

## 10.1 k近邻学习

$k$ 近邻 $\left( k\right.$ -Nearest Neighbor,简称 $k$ NN $)$ 学习是一种常用的监督学习方法, 其工作机制非常简单: 给定测试样本, 基于某种距离度量找出训练集中与其最靠近的 $k$ 个训练样本，然后基于这 $k$ 个 “邻居” 的信息来进行预测. 通常，在分类任务中可使用 “投票法”,即选择这 $k$ 个样本中出现最多的类别标记作为预测结果; 在回归任务中可使用 “平均法”,即将这 $k$ 个样本的实值输出标记的平均值作为预测结果; 还可基于距离远近进行加权平均或加权投票, 距离越近的样本权重越大.

与前面介绍的学习方法相比, $k$ 近邻学习有一个明显的不同之处: 它似乎没有显式的训练过程! 事实上, 它是 “懒惰学习” (lazy learning) 的著名代表, 此类学习技术在训练阶段仅仅是把样本保存起来, 训练时间开销为零, 待收到测试样本后再进行处理; 相应的, 那些在训练阶段就对样本进行学习处理的方法, 称为 “急切学习” (eager learning).

图 10.1 给出了 $k$ 近邻分类器的一个示意图. 显然, $k$ 是一个重要参数,当 $k$ 取不同值时，分类结果会有显著不同. 另一方面，若采用不同的距离计算方式， 则找出的 “近邻” 可能有显著差别, 从而也会导致分类结果有显著不同.

暂且假设距离计算是 “恰当” 的,即能够恰当地找出 $k$ 个近邻,我们来对 “最近邻分类器” (1NN,即 $k = 1$ ) 在二分类问题上的性能做一个简单的讨论.

![224_966_1688_648_379_0.jpg](../../images/224_966_1688_648_379_0.jpg)

图 10.1 $k$ 近邻分类器示意图. 虚线显示出等距线; 测试样本在 $k = 1$ 或 $k = 5$ 时被判别为正例, $k = 3$ 时被判别为反例.

---

所谓“近朱者赤，近墨者黑”.

参见 8.4 节.

---

给定测试样本 $\mathbf{x}$ ,若其最近邻样本为 $\mathbf{z}$ ,则最近邻分类器出错的概率就是 $\mathbf{x}$ 与 $\mathbf{z}$ 类别标记不同的概率,即

$$
P\left( {err}\right)  = 1 - \mathop{\sum }\limits_{{c \in  \mathcal{Y}}}P\left( {c \mid  \mathbf{x}}\right) P\left( {c \mid  \mathbf{z}}\right) . \tag{10.1}
$$

---

贝叶斯最优分类器参见 7.1 节.

---

假设样本独立同分布,且对任意 $\mathbf{x}$ 和任意小正数 $\delta$ ,在 $\mathbf{x}$ 附近 $\delta$ 距离范围内总能找到一个训练样本; 换言之, 对任意测试样本, 总能在任意近的范围内找到式(10.1)中的训练样本 $\mathbf{z}$ . 令 ${c}^{ * } = \arg \mathop{\max }\limits_{{c \in  \mathcal{Y}}}P\left( {c \mid  \mathbf{x}}\right)$ 表示贝叶斯最优分类器的结果, 有

$$
P\left( {err}\right)  = 1 - \mathop{\sum }\limits_{{c \in  \mathcal{Y}}}P\left( {c \mid  \mathbf{x}}\right) P\left( {c \mid  \mathbf{z}}\right)
$$

$$
\simeq  1 - \mathop{\sum }\limits_{{c \in  \mathcal{Y}}}{P}^{2}\left( {c \mid  \mathbf{x}}\right)
$$

$$
\leq  1 - {P}^{2}\left( {{c}^{ * } \mid  \mathbf{x}}\right)
$$

$$
= \left( {1 + P\left( {{c}^{ * } \mid  \mathbf{x}}\right) }\right) \left( {1 - P\left( {{c}^{ * } \mid  \mathbf{x}}\right) }\right)
$$

$$
\leq  2 \times  \left( {1 - P\left( {{c}^{ * } \mid  \mathbf{x}}\right) }\right) . \tag{10.2}
$$

---

为便于初学者理解, 本节仅做了一个简化讨论, 更严格的分析参阅 [Cover and Hart, 1967].

---

于是我们得到了有点令人惊讶的结论: 最近邻分类器虽简单, 但它的泛化错误率不超过贝叶斯最优分类器的错误率的两倍！

## 10.2 低维嵌入

---

作为参照量:宇宙间基本粒子的总数约为 ${10}^{80}$ (一粒灰尘中含有几十亿个基本粒子).

---

上一节的讨论是基于一个重要假设: 任意测试样本 $\mathbf{x}$ 附近任意小的 $\delta$ 距离范围内总能找到一个训练样本，即训练样本的采样密度足够大，或称为 “密采样” (dense sample). 然而, 这个假设在现实任务中通常很难满足, 例如若 $\delta  = {0.001}$ ,仅考虑单个属性,则仅需 1000 个样本点平均分布在归一化后的属性取值范围内, 即可使得任意测试样本在其附近 0.001 距离范围内总能找到一个训练样本, 此时最近邻分类器的错误率不超过贝叶斯最优分类器的错误率的两倍. 然而, 这仅是属性维数为 1 的情形, 若有更多的属性, 则情况会发生显著变化. 例如假定属性维数为 20, 若要求样本满足密采样条件, 则至少需 ${\left( {10}^{3}\right) }^{20} = {10}^{60}$ 个样本. 现实应用中属性维数经常成千上万,要满足密采样条件所需的样本数目是无法达到的天文数字. 此外, 许多学习方法都涉及距离计算, 而高维空间会给距离计算带来很大的麻烦, 例如当维数很高时甚至连计算内积都不再容易.

事实上, 在高维情形下出现的数据样本稀疏、距离计算困难等问题, 是所有机器学习方法共同面临的严重障碍, 被称为 “维数灾难” (curse of dimensionality).

缓解维数灾难的一个重要途径是降维(dimension reduction)，亦称 “维数约简”, 即通过某种数学变换将原始高维属性空间转变为一个低维 “子空间" (subspace), 在这个子空间中样本密度大幅提高, 距离计算也变得更为容易. 为什么能进行降维? 这是因为在很多时候, 人们观测或收集到的数据样本虽是高维的, 但与学习任务密切相关的也许仅是某个低维分布, 即高维空间中的一个低维 “嵌入” (embedding). 图 10.2 给出了一个直观的例子. 原始高维空间中的样本点, 在这个低维嵌入子空间中更容易进行学习.

![226_805_867_967_537_0.jpg](../../images/226_805_867_967_537_0.jpg)

图 10.2 低维嵌入示意图

若要求原始空间中样本之间的距离在低维空间中得以保持, 如图 10.2 所示, 即得到 “多维缩放” (Multiple Dimensional Scaling, 简称 MDS) [Cox and Cox, 2001] 这样一种经典的降维方法. 下面做一个简单的介绍.

假定 $m$ 个样本在原始空间的距离矩阵为 $\mathbf{D} \in  {\mathbb{R}}^{m \times  m}$ ,其第 $i$ 行 $j$ 列的元素 ${\operatorname{dist}}_{ij}$ 为样本 ${\mathbf{x}}_{i}$ 到 ${\mathbf{x}}_{j}$ 的距离. 我们的目标是获得样本在 ${d}^{\prime }$ 维空间的表示 $\mathbf{Z} \in  {\mathbb{R}}^{{d}^{\prime } \times  m},{d}^{\prime } \leq  d$ ,且任意两个样本在 ${d}^{\prime }$ 维空间中的欧氏距离等于原始空间中的距离,即 $\begin{Vmatrix}{{\mathbf{z}}_{i} - {\mathbf{z}}_{j}}\end{Vmatrix} = {\operatorname{dist}}_{ij}$ .

令 $\mathbf{B} = {\mathbf{Z}}^{\mathrm{T}}\mathbf{Z} \in  {\mathbb{R}}^{m \times  m}$ ,其中 $\mathbf{B}$ 为降维后样本的内积矩阵, ${b}_{ij} = {\mathbf{z}}_{i}^{\mathrm{T}}{\mathbf{z}}_{j}$ ,有

$$
{dis}{t}_{ij}^{2} = {\begin{Vmatrix}{\mathbf{z}}_{i}\end{Vmatrix}}^{2} + {\begin{Vmatrix}{\mathbf{z}}_{j}\end{Vmatrix}}^{2} - 2{\mathbf{z}}_{i}^{\mathrm{T}}{\mathbf{z}}_{j}
$$

$$
= {b}_{ii} + {b}_{jj} - 2{b}_{ij}. \tag{10.3}
$$

---

[Bellman, 1957] 最早提出，亦称 “维数诅咒” 、 “维数危机”.

另一个重要途径是特征选择，参见第 11 章.

---

$\mathbf{0} \in  {\mathbb{R}}^{{d}^{\prime }}$ 为全零向量.

为便于讨论,令降维后的样本 $\mathbf{Z}$ 被中心化,即 $\mathop{\sum }\limits_{{i = 1}}^{m}{z}_{i} = \mathbf{0}$ . 显然,矩阵 $\mathbf{B}$ 的行与列之和均为零,即 $\mathop{\sum }\limits_{{i = 1}}^{m}{b}_{ij} = \mathop{\sum }\limits_{{j = 1}}^{m}{b}_{ij} = 0$ . 易知

$$
\mathop{\sum }\limits_{{i = 1}}^{m}{\operatorname{dist}}_{ij}^{2} = \operatorname{tr}\left( \mathbf{B}\right)  + m{b}_{jj} \tag{10.4}
$$

$$
\mathop{\sum }\limits_{{j = 1}}^{m}{\operatorname{dist}}_{ij}^{2} = \operatorname{tr}\left( \mathbf{B}\right)  + m{b}_{ii} \tag{10.5}
$$

$$
\mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j = 1}}^{m}{\operatorname{dist}}_{ij}^{2} = {2m}\operatorname{tr}\left( \mathbf{B}\right) , \tag{10.6}
$$

其中 $\operatorname{tr}\left( \cdot \right)$ 表示矩阵的迹(trace), $\operatorname{tr}\left( \mathbf{B}\right)  = \mathop{\sum }\limits_{{i = 1}}^{m}{\begin{Vmatrix}{\mathbf{z}}_{i}\end{Vmatrix}}^{2}$ . 令

$$
{\operatorname{dist}}_{i \cdot  }^{2} = \frac{1}{m}\mathop{\sum }\limits_{{j = 1}}^{m}{\operatorname{dist}}_{ij}^{2}, \tag{10.7}
$$

$$
{\operatorname{dist}}_{\cdot j}^{2} = \frac{1}{m}\mathop{\sum }\limits_{{i = 1}}^{m}{\operatorname{dist}}_{ij}^{2}, \tag{10.8}
$$

$$
{\text{ dist }}_{ \cdot  }^{2} = \frac{1}{{m}^{2}}\mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j = 1}}^{m}{\text{ dist }}_{ij}^{2}, \tag{10.9}
$$

由式(10.3)和式(10.4) $\sim  \left( {10.9}\right)$ 可得

$$
{b}_{ij} =  - \frac{1}{2}\left( {{\operatorname{dist}}_{ij}^{2} - {\operatorname{dist}}_{i \cdot  }^{2} - {\operatorname{dist}}_{\cdot j}^{2} + {\operatorname{dist}}_{\cdot  \cdot  }^{2}}\right) , \tag{10.10}
$$

由此即可通过降维前后保持不变的距离矩阵 $\mathbf{D}$ 求取内积矩阵 $\mathbf{B}$ .

对矩阵 $\mathbf{B}$ 做特征值分解(eigenvalue decomposition), $\mathbf{B} = \mathbf{V}\mathbf{\Lambda }{\mathbf{V}}^{\mathrm{T}}$ ,其中 $\mathbf{\Lambda } = \operatorname{diag}\left( {{\lambda }_{1},{\lambda }_{2},\ldots ,{\lambda }_{d}}\right)$ 为特征值构成的对角矩阵, ${\lambda }_{1} \geq  {\lambda }_{2} \geq  \ldots  \geq  {\lambda }_{d},\mathbf{V}$ 为特征向量矩阵. 假定其中有 ${d}^{ * }$ 个非零特征值,它们构成对角矩阵 ${\mathbf{\Lambda }}_{ * } = \; \operatorname{diag}\left( {{\lambda }_{1},{\lambda }_{2},\ldots ,{\lambda }_{{d}^{ * }}}\right)$ ,令 ${\mathbf{V}}_{ * }$ 表示相应的特征向量矩阵,则 $\mathbf{Z}$ 可表达为

$$
\mathbf{Z} = {\mathbf{\Lambda }}_{ * }^{1/2}{\mathbf{V}}_{ * }^{\mathrm{T}} \in  {\mathbb{R}}^{{d}^{ * } \times  m}. \tag{10.11}
$$

在现实应用中为了有效降维, 往往仅需降维后的距离与原始空间中的距离尽可能接近,而不必严格相等. 此时可取 ${d}^{\prime } \ll  d$ 个最大特征值构成对角矩阵 $\widetilde{\mathbf{\Lambda }} = \operatorname{diag}\left( {{\lambda }_{1},{\lambda }_{2},\ldots ,{\lambda }_{{d}^{\prime }}}\right)$ ,令 $\widetilde{\mathbf{V}}$ 表示相应的特征向量矩阵,则 $\mathbf{Z}$ 可表达为

$$
\mathbf{Z} = {\widetilde{\mathbf{\Lambda }}}^{1/2}{\widetilde{\mathbf{V}}}^{\mathrm{T}} \in  {\mathbb{R}}^{{d}^{\prime } \times  m}. \tag{10.12}
$$

图 10.3 给出了 MDS 算法的描述.

输入: 距离矩阵 $\mathbf{D} \in  {\mathbb{R}}^{m \times  m}$ ,其元素 ${\operatorname{dist}}_{ij}$ 为样本 ${\mathbf{x}}_{i}$ 到 ${\mathbf{x}}_{j}$ 的距离; 低维空间维数 ${d}^{\prime }$ .

过程:

1: 根据式(10.7) $\sim  \left( {10.9}\right)$ 计算 ${\operatorname{dist}}_{i \cdot  }^{2},{\operatorname{dist}}_{\cdot j}^{2},{\operatorname{dist}}_{\cdot i}^{2}$ ;

2: 根据式(10.10)计算矩阵 $\mathbf{B}$ ;

3: 对矩阵 $\mathbf{B}$ 做特征值分解;

4: 取 $\widetilde{\mathbf{\Lambda }}$ 为 ${d}^{\prime }$ 个最大特征值所构成的对角矩阵, $\widetilde{\mathbf{V}}$ 为相应的特征向量矩阵.

输出: 矩阵 $\widetilde{\mathbf{V}}{\widetilde{\mathbf{\Lambda }}}^{1/2} \in  {\mathbb{R}}^{m \times  {d}^{\prime }}$ ,每行是一个样本的低维坐标

图 10.3 MDS 算法

一般来说, 欲获得低维子空间, 最简单的是对原始高维空间进行线性变换. 给定 $d$ 维空间中的样本 $\mathbf{X} = \left( {{\mathbf{x}}_{1},{\mathbf{x}}_{2},\ldots ,{\mathbf{x}}_{m}}\right)  \in  {\mathbb{R}}^{d \times  m}$ ,变换之后得到 ${d}^{\prime } \leq  d$ 维空间中的样本

$$
\mathbf{Z} = {\mathbf{W}}^{\mathrm{T}}\mathbf{X} \tag{10.13}
$$

其中 $\mathbf{W} \in  {\mathbb{R}}^{d \times  {d}^{\prime }}$ 是变换矩阵, $\mathbf{Z} \in  {\mathbb{R}}^{{d}^{\prime } \times  m}$ 是样本在新空间中的表达.

变换矩阵 $\mathbf{W}$ 可视为 ${d}^{\prime }$ 个 $d$ 维基向量, ${\mathbf{z}}_{i} = {\mathbf{W}}^{\mathrm{T}}{\mathbf{x}}_{i}$ 是第 $i$ 个样本与这 ${d}^{\prime }$ 个基向量分别做内积而得到的 ${d}^{\prime }$ 维属性向量. 换言之, ${\mathbf{z}}_{i}$ 是原属性向量 ${\mathbf{x}}_{i}$ 在新坐标系 $\left\{  {{\mathbf{w}}_{1},{\mathbf{w}}_{2},\cdots ,{\mathbf{w}}_{{d}^{\prime }}}\right\}$ 中的坐标向量. 若 ${\mathbf{w}}_{i}$ 与 ${\mathbf{w}}_{j}\left( {i \neq  j}\right)$ 正交,则新坐标系是一个正交坐标系,此时 $\mathbf{W}$ 为正交变换. 显然,新空间中的属性是原空间中属性的线性组合.

基于线性变换来进行降维的方法称为线性降维方法, 它们都符合式(10.13)的基本形式, 不同之处是对低维子空间的性质有不同的要求, 相当于对 $\mathbf{W}$ 施加了不同的约束. 在下一节我们将会看到,若要求低维子空间对样本具有最大可分性, 则将得到一种极为常用的线性降维方法.

对降维效果的评估, 通常是比较降维前后学习器的性能, 若性能有所提高则认为降维起到了作用. 若将维数降至二维或三维, 则可通过可视化技术来直观地判断降维效果.

## 10.3 主成分分析

主成分分析(Principal Component Analysis, 简称 PCA)是最常用的一种降维方法. 在介绍 PCA 之前, 不妨先考虑这样一个问题: 对于正交属性空间中的样本点, 如何用一个超平面(直线的高维推广)对所有样本进行恰当的表达?

---

通常令 ${d}^{\prime } \ll  d$ .

亦称 “主分量分析”

---

容易想到, 若存在这样的超平面, 那么它大概应具有这样的性质:

- 最近重构性: 样本点到这个超平面的距离都足够近;

- 最大可分性:样本点在这个超平面上的投影能尽可能分开.

有趣的是, 基于最近重构性和最大可分性, 能分别得到主成分分析的两种等价推导. 我们先从最近重构性来推导.

假定数据样本进行了中心化,即 $\mathop{\sum }\limits_{i}{\mathbf{x}}_{i} = \mathbf{0}$ ; 再假定投影变换后得到的新坐标系为 $\left\{  {{\mathbf{w}}_{1},{\mathbf{w}}_{2},\ldots ,{\mathbf{w}}_{d}}\right\}$ ,其中 ${\mathbf{w}}_{i}$ 是标准正交基向量, ${\begin{Vmatrix}{\mathbf{w}}_{i}\end{Vmatrix}}_{2} = 1,{\mathbf{w}}_{i}^{\mathrm{T}}{\mathbf{w}}_{j} = 0 \; \left( {i \neq  j}\right)$ . 若丢弃新坐标系中的部分坐标,即将维度降低到 ${d}^{\prime } < d$ ,则样本点 ${\mathbf{x}}_{i}$ 在低维坐标系中的投影是 ${\mathbf{z}}_{i} = \left( {{z}_{i1};{z}_{i2};\ldots ;{z}_{i{d}^{\prime }}}\right)$ ,其中 ${z}_{ij} = {\mathbf{w}}_{j}^{\mathrm{T}}{\mathbf{x}}_{i}$ 是 ${\mathbf{x}}_{i}$ 在低维坐标系下第 $j$ 维的坐标. 若基于 ${z}_{i}$ 来重构 ${x}_{i}$ ,则会得到 ${\widehat{x}}_{i} = \mathop{\sum }\limits_{{j = 1}}^{{d}^{\prime }}{z}_{ij}{w}_{j}$ .

考虑整个训练集,原样本点 ${\mathbf{x}}_{i}$ 与基于投影重构的样本点 ${\widehat{\mathbf{x}}}_{i}$ 之间的距离为

$$
\mathop{\sum }\limits_{{i = 1}}^{m}{\begin{Vmatrix}\mathop{\sum }\limits_{{j = 1}}^{{d}^{\prime }}{z}_{ij}{\mathbf{w}}_{j} - {\mathbf{x}}_{i}\end{Vmatrix}}_{2}^{2} = \mathop{\sum }\limits_{{i = 1}}^{m}{\mathbf{z}}_{i}^{\mathrm{T}}{\mathbf{z}}_{i} - 2\mathop{\sum }\limits_{{i = 1}}^{m}{\mathbf{z}}_{i}^{\mathrm{T}}{\mathbf{W}}^{\mathrm{T}}{\mathbf{x}}_{i} + \text{ const }
$$

$$
\propto   - \operatorname{tr}\left( {{\mathbf{W}}^{\mathrm{T}}\left( {\mathop{\sum }\limits_{{i = 1}}^{m}{\mathbf{x}}_{i}{\mathbf{x}}_{i}^{\mathrm{T}}}\right) \mathbf{W}}\right) . \tag{10.14}
$$

根据最近重构性,式 (10.14) 应被最小化,考虑到 ${\mathbf{w}}_{j}$ 是标准正交基, $\mathop{\sum }\limits_{i}{\mathbf{x}}_{i}{\mathbf{x}}_{i}^{\mathrm{T}}$ 是协方差矩阵, 有

$$
\mathop{\min }\limits_{\mathbf{W}} - \operatorname{tr}\left( {{\mathbf{W}}^{\mathrm{T}}\mathbf{X}{\mathbf{X}}^{\mathrm{T}}\mathbf{W}}\right) \tag{10.15}
$$

$$
\text{ s.t. }{\mathbf{W}}^{\mathrm{T}}\mathbf{W} = \mathbf{I}\text{ . }
$$

这就是主成分分析的优化目标.

从最大可分性出发, 能得到主成分分析的另一种解释. 我们知道, 样本点 ${\mathbf{x}}_{i}$ 在新空间中超平面上的投影是 ${\mathbf{W}}^{\mathrm{T}}{\mathbf{x}}_{i}$ ,若所有样本点的投影能尽可能分开, 则应该使投影后样本点的方差最大化，如图 10.4 所示.

投影后样本点的方差是 $\mathop{\sum }\limits_{i}{\mathbf{W}}^{\mathrm{T}}{\mathbf{x}}_{i}{\mathbf{x}}_{i}^{\mathrm{T}}\mathbf{W}$ ，于是优化目标可写为

$$
\mathop{\max }\limits_{\mathbf{W}}\operatorname{tr}\left( {{\mathbf{W}}^{\mathrm{T}}\mathbf{X}{\mathbf{X}}^{\mathrm{T}}\mathbf{W}}\right) \tag{10.16}
$$

$$
\text{ s.t. }{\mathbf{W}}^{\mathrm{T}}\mathbf{W} = \mathbf{I}\text{ , }
$$

显然, 式(10.16)与(10.15)等价.

---

const 是一个常数.

---

![230_991_125_634_506_0.jpg](../../images/230_991_125_634_506_0.jpg)

图 10.4 使所有样本的投影尽可能分开 (如图中红线所示), 则需最大化投影点的方差

对式(10.15)或(10.16)使用拉格朗日乘子法可得

$$
\mathbf{X}{\mathbf{X}}^{\mathrm{T}}\mathbf{W} = \lambda \mathbf{W} \tag{10.17}
$$

---

实践中常通过对 $\mathbf{X}$ 进行奇异值分解来代替协方差矩阵的特征值分解.

---

于是,只需对协方差矩阵 ${\mathbf{{XX}}}^{\mathrm{T}}$ 进行特征值分解,将求得的特征值排序: ${\lambda }_{1} \geq  {\lambda }_{2} \geq  \ldots  \geq  {\lambda }_{d}$ ,再取前 ${d}^{\prime }$ 个特征值对应的特征向量构成 $\mathbf{W} = \left( {\mathbf{w}}_{1}\right.$ , ${\mathbf{w}}_{2},\ldots ,{\mathbf{w}}_{{d}^{\prime }}$ ). 这就是主成分分析的解. PCA 算法描述如图 10.5 所示.

---

PCA 也可看作是逐一选取方差最大方向，即先对协方差矩阵 $\mathop{\sum }\limits_{i}{\mathbf{x}}_{i}{\mathbf{x}}_{i}^{\mathrm{T}}$ 做特征值分解,取最大特征值对应的特征向量 ${\mathbf{w}}_{1}$ ; 再对 $\mathop{\sum }\limits_{i}{\mathbf{x}}_{i}{\mathbf{x}}_{i}^{\mathrm{T}} - {\lambda }_{1}{\mathbf{w}}_{1}{\mathbf{w}}_{1}^{\mathrm{T}}$ 做特征值分解, 取最大特征值对应的特征向量 ${\mathbf{w}}_{2}$ ; ……由 $\mathbf{W}$ 各分量正交及

$$
\mathop{\sum }\limits_{{i = 1}}^{m}{\mathbf{x}}_{i}{\mathbf{x}}_{i}^{\mathrm{T}} = \mathop{\sum }\limits_{{j = 1}}^{d}{\lambda }_{j}{\mathbf{w}}_{j}{\mathbf{w}}_{j}^{\mathrm{T}}
$$

可知，上述逐一选取方差最大方向的做法与直接选取最大 ${d}^{\prime }$ 个特征值等价.

---

---

输入: 样本集 $D = \left\{  {{\mathbf{x}}_{1},{\mathbf{x}}_{2},\ldots ,{\mathbf{x}}_{m}}\right\}$ ;

	低维空间维数 ${d}^{\prime }$ .

过程:

1: 对所有样本进行中心化: ${\mathbf{x}}_{i} \leftarrow  {\mathbf{x}}_{i} - \frac{1}{m}\mathop{\sum }\limits_{{i = 1}}^{m}{\mathbf{x}}_{i}$ ;

2: 计算样本的协方差矩阵 $\mathbf{X}{\mathbf{X}}^{\mathrm{T}}$ ;

3: 对协方差矩阵 ${\mathbf{{XX}}}^{\mathrm{T}}$ 做特征值分解;

4: 取最大的 ${d}^{\prime }$ 个特征值所对应的特征向量 ${\mathbf{w}}_{1},{\mathbf{w}}_{2},\ldots ,{\mathbf{w}}_{{d}^{\prime }}$ .

输出: 投影矩阵 $\mathbf{W} = \left( {{\mathbf{w}}_{1},{\mathbf{w}}_{2},\ldots ,{\mathbf{w}}_{{d}^{\prime }}}\right)$ .

---

图 10.5 PCA 算法

降维后低维空间的维数 ${d}^{\prime }$ 通常是由用户事先指定,或通过在 ${d}^{\prime }$ 值不同的低维空间中对 $k$ 近邻分类器(或其他开销较小的学习器) 进行交叉验证来选取较好的 ${d}^{\prime }$ 值. 对 PCA,还可从重构的角度设置一个重构阈值,例如 $t = {95}\%$ ,然后选取使下式成立的最小 ${d}^{\prime }$ 值:

$$
\frac{\mathop{\sum }\limits_{{i = 1}}^{{d}^{\prime }}{\lambda }_{i}}{\mathop{\sum }\limits_{{i = 1}}^{d}{\lambda }_{i}} \geq  t \tag{10.18}
$$

---

保存均值向量是为了通过向量减法对新样本同样进行中心化.

---

PCA 仅需保留 $\mathbf{W}$ 与样本的均值向量即可通过简单的向量减法和矩阵-向量乘法将新样本投影至低维空间中. 显然, 低维空间与原始高维空间必有不同, 因为对应于最小的 $d - {d}^{\prime }$ 个特征值的特征向量被舍弃了,这是降维导致的结果. 但舍弃这部分信息往往是必要的:一方面，舍弃这部分信息之后能使样本的采样密度增大, 这正是降维的重要动机; 另一方面, 当数据受到噪声影响时, 最小的特征值所对应的特征向量往往与噪声有关, 将它们舍弃能在一定程度上起到去噪的效果.

## 10.4 核化线性降维

线性降维方法假设从高维空间到低维空间的函数映射是线性的, 然而, 在不少现实任务中, 可能需要非线性映射才能找到恰当的低维嵌入. 图 10.6 给出了一个例子, 样本点从二维空间中的矩形区域采样后以 S 形曲面嵌入到三维空间, 若直接使用线性降维方法对三维空间观察到的样本点进行降维, 则将丢失原本的低维结构. 为了对 “原本采样的” 低维空间与降维后的低维空间加以区别, 我们称前者为 “本真” (intrinsic)低维空间.

![231_681_1182_1164_400_0.jpg](../../images/231_681_1182_1164_400_0.jpg)

图 10.6 三维空间中观察到的 3000 个样本点, 是从本真二维空间中矩形区域采样后以 S 形曲面嵌入, 此情形下线性降维会丢失低维结构. 图中数据点的染色显示出低维空间的结构.

---

参见 6.6 节.

---

非线性降维的一种常用方法, 是基于核技巧对线性降维方法进行 “核化" (kernelized). 下面我们以核主成分分析(Kernelized PCA, 简称 KPCA) [Schölkopf et al., 1998] 为例来进行演示.

假定我们将在高维特征空间中把数据投影到由 $\mathbf{W}$ 确定的超平面上,即 PCA 欲求解

$$
\left( {\mathop{\sum }\limits_{{i = 1}}^{m}{\mathbf{z}}_{i}{\mathbf{z}}_{i}^{\mathrm{T}}}\right) \mathbf{W} = \lambda \mathbf{W} \tag{10.19}
$$

其中 ${z}_{i}$ 是样本点 ${x}_{i}$ 在高维特征空间中的像. 易知

$$
\mathbf{W} = \frac{1}{\lambda }\left( {\mathop{\sum }\limits_{{i = 1}}^{m}{z}_{i}{z}_{i}^{\mathrm{T}}}\right) \mathbf{W} = \mathop{\sum }\limits_{{i = 1}}^{m}{z}_{i}\frac{{z}_{i}^{\mathrm{T}}\mathbf{W}}{\lambda }
$$

$$
= \mathop{\sum }\limits_{{i = 1}}^{m}{z}_{i}{\alpha }_{i} \tag{10.20}
$$

其中 ${\mathbf{\alpha }}_{i} = \frac{1}{\lambda }{\mathbf{z}}_{i}^{\mathrm{T}}\mathbf{W}$ . 假定 ${\mathbf{z}}_{i}$ 是由原始属性空间中的样本点 ${\mathbf{x}}_{i}$ 通过映射 $\phi$ 产生, 即 ${\mathbf{z}}_{i} = \phi \left( {\mathbf{x}}_{i}\right) , i = 1,2,\ldots , m$ . 若 $\phi$ 能被显式表达出来,则通过它将样本映射至高维特征空间, 再在特征空间中实施 PCA 即可. 式(10.19)变换为

$$
\left( {\mathop{\sum }\limits_{{i = 1}}^{m}\phi \left( {\mathbf{x}}_{i}\right) \phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}}\right) \mathbf{W} = \lambda \mathbf{W}, \tag{10.21}
$$

式(10.20)变换为

$$
\mathbf{W} = \mathop{\sum }\limits_{{i = 1}}^{m}\phi \left( {\mathbf{x}}_{i}\right) {\mathbf{\alpha }}_{i}. \tag{10.22}
$$

一般情形下，我们不清楚 $\phi$ 的具体形式，于是引入核函数

$$
\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = \phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( {\mathbf{x}}_{j}\right) . \tag{10.23}
$$

将式(10.22)和(10.23)代入式(10.21)后化简可得

$$
\mathbf{{KA}} = \lambda \mathbf{A}, \tag{10.24}
$$

其中 $\mathbf{K}$ 为 $\kappa$ 对应的核矩阵, ${\left( \mathbf{K}\right) }_{ij} = \kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right) ,\mathbf{A} = \left( {{\mathbf{\alpha }}_{1};{\mathbf{\alpha }}_{2};\ldots ;{\mathbf{\alpha }}_{m}}\right)$ . 显然, 式 (10.24) 是特征值分解问题,取 $\mathbf{K}$ 最大的 ${d}^{\prime }$ 个特征值对应的特征向量即可.

对新样本 $x$ ,其投影后的第 $j\left( {j = 1,2,\ldots ,{d}^{\prime }}\right)$ 维坐标为

$$
{z}_{j} = {\mathbf{w}}_{j}^{\mathrm{T}}\phi \left( \mathbf{x}\right)  = \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}^{j}\phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( \mathbf{x}\right)
$$

$$
= \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}^{j}\kappa \left( {{\mathbf{x}}_{i},\mathbf{x}}\right) , \tag{10.25}
$$

其中 ${\mathbf{\alpha }}_{i}$ 已经过规范化, ${\alpha }_{i}^{j}$ 是 ${\mathbf{\alpha }}_{i}$ 的第 $j$ 个分量. 式(10.25)显示出,为获得投影后的坐标, KPCA 需对所有样本求和, 因此它的计算开销较大.

## 10.5 流形学习

流形学习(manifold learning)是一类借鉴了拓扑流形概念的降维方法. “流形”是在局部与欧氏空间同胚的空间, 换言之, 它在局部具有欧氏空间的性质, 能用欧氏距离来进行距离计算. 这给降维方法带来了很大的启发: 若低维流形嵌入到高维空间中, 则数据样本在高维空间的分布虽然看上去非常复杂, 但在局部上仍具有欧氏空间的性质, 因此, 可以容易地在局部建立降维映射关系, 然后再设法将局部映射关系推广到全局. 当维数被降至二维或三维时, 能对数据进行可视化展示，因此流形学习也可被用于可视化. 本节介绍两种著名的流形学习方法.

### 10.5.1 等度量映射

等度量映射(Isometric Mapping, 简称 Isomap) [Tenenbaum et al., 2000] 的基本出发点, 是认为低维流形嵌入到高维空间之后, 直接在高维空间中计算直线距离具有误导性, 因为高维空间中的直线距离在低维嵌入流形上是不可达的. 如图 10.7(a)所示, 低维嵌入流形上两点间的距离是 “测地线” (geodesic)距离: 想象一只虫子从一点爬到另一点，如果它不能脱离曲面行走，那么图10.7(a)中的红色曲线是距离最短的路径, 即 S 曲面上的测地线, 测地线距离是两点之间的本真距离. 显然, 直接在高维空间中计算直线距离是不恰当的.

![233_699_1324_1121_552_0.jpg](../../images/233_699_1324_1121_552_0.jpg)

图 10.7 低维嵌入流形上的测地线距离(红色) 不能用高维空间的直线距离计算, 但能用近邻距离来近似

那么，如何计算测地线距离呢? 这时我们可利用流形在局部上与欧氏空间同胚这个性质, 对每个点基于欧氏距离找出其近邻点, 然后就能建立一个近邻连接图, 图中近邻点之间存在连接, 而非近邻点之间不存在连接, 于是, 计算两点之间测地线距离的问题, 就转变为计算近邻连接图上两点之间的最短路径问题. 从图 10.7(b)可看出, 基于近邻距离逼近能获得低维流形上测地线距离很好的近似.

在近邻连接图上计算两点间的最短路径, 可采用著名的 Dijkstra 算法或 Floyd 算法, 在得到任意两点的距离之后, 就可通过 10.2 节介绍的 MDS 方法来获得样本点在低维空间中的坐标. 图 10.8 给出了 Isomap 算法描述.

---

输入: 样本集 $D = \left\{  {{\mathbf{x}}_{1},{\mathbf{x}}_{2},\ldots ,{\mathbf{x}}_{m}}\right\}$ ;

				近邻参数 $k$ ;

				低维空间维数 ${d}^{\prime }$ .

过程:

		for $i = 1,2,\ldots , m$ do

			确定 ${\mathbf{x}}_{i}$ 的 $k$ 近邻;

			${\mathbf{x}}_{i}$ 与 $k$ 近邻点之间的距离设置为欧氏距离,与其他点的距离设置为无穷大;

		end for

	5:调用最短路径算法计算任意两样本点之间的距离 $\operatorname{dist}\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)$ ;

		将 $\operatorname{dist}\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)$ 作为 MDS 算法的输入;

		return MDS 算法的输出

输出: 样本集 $D$ 在低维空间的投影 $Z = \left\{  {{z}_{1},{z}_{2},\ldots ,{z}_{m}}\right\}$ .

---

图 10.8 Isomap 算法

需注意的是，Isomap 仅是得到了训练样本在低维空间的坐标，对于新样本， 如何将其映射到低维空间呢? 这个问题的常用解决方案, 是将训练样本的高维空间坐标作为输入、低维空间坐标作为输出, 训练一个回归学习器来对新样本的低维空间坐标进行预测. 这显然仅是一个权宜之计, 但目前似乎并没有更好的办法.

对近邻图的构建通常有两种做法, 一种是指定近邻点个数, 例如欧氏距离最近的 $k$ 个点为近邻点,这样得到的近邻图称为 $k$ 近邻图; 另一种是指定距离阈值 $\epsilon$ ,距离小于 $\epsilon$ 的点被认为是近邻点,这样得到的近邻图称为 $\epsilon$ 近邻图. 两种方式均有不足, 例如若近邻范围指定得较大, 则距离很远的点可能被误认为近邻, 这样就出现 “短路” 问题; 近邻范围指定得较小, 则图中有些区域可能与其他区域不存在连接, 这样就出现 “断路” 问题. 短路与断路都会给后续的最短路径计算造成误导.

### 10.5.2 局部线性嵌入

与 Isomap 试图保持近邻样本之间的距离不同，局部线性嵌入(Locally Linear Embedding, 简称LLE) [Roweis and Saul, 2000] 试图保持邻域内样本之间的线性关系. 如图 10.9 所示，假定样本点 ${\mathbf{x}}_{i}$ 的坐标能通过它的邻域样本 ${\mathbf{x}}_{j}$ ， ${\mathbf{x}}_{k},{\mathbf{x}}_{l}$ 的坐标通过线性组合而重构出来，即

$$
{\mathbf{x}}_{i} = {w}_{ij}{\mathbf{x}}_{j} + {w}_{ik}{\mathbf{x}}_{k} + {w}_{il}{\mathbf{x}}_{l}, \tag{10.26}
$$

---

1972 年图灵奖得主 E. W. Dijkstra 和 1978 年图灵奖得主 R. Floyd 分别提出的著名算法, 参阅数据结构教科书.

MDS 参见 10.2 节.

---

![235_833_123_858_385_0.jpg](../../images/235_833_123_858_385_0.jpg)

图 10.9 高维空间中的样本重构关系在低维空间中得以保持

LLE 希望式(10.26)的关系在低维空间中得以保持.

LLE 先为每个样本 ${\mathbf{x}}_{i}$ 找到其近邻下标集合 ${Q}_{i}$ ,然后计算出基于 ${Q}_{i}$ 中的样本点对 ${\mathbf{x}}_{i}$ 进行线性重构的系数 ${\mathbf{w}}_{i}$ :

$$
{\mathbf{w}}_{1},{\mathbf{w}}_{2},\ldots ,{\mathbf{w}}_{m}\mathop{\sum }\limits_{{i = 1}}^{m}{\begin{Vmatrix}{\mathbf{x}}_{i} - \mathop{\sum }\limits_{{j \in  {Q}_{i}}}{w}_{ij}{\mathbf{x}}_{j}\end{Vmatrix}}_{2}^{2} \tag{10.27}
$$

$$
\text{ s.t. }\mathop{\sum }\limits_{{j \in  {Q}_{i}}}{w}_{ij} = 1\text{ , }
$$

其中 ${\mathbf{x}}_{i}$ 和 ${\mathbf{x}}_{j}$ 均为已知,令 ${C}_{jk} = {\left( {\mathbf{x}}_{i} - {\mathbf{x}}_{j}\right) }^{\mathrm{T}}\left( {{\mathbf{x}}_{i} - {\mathbf{x}}_{k}}\right) ,{w}_{ij}$ 有闭式解

$$
{w}_{ij} = \frac{\mathop{\sum }\limits_{{k \in  {Q}_{i}}}{C}_{jk}^{-1}}{\mathop{\sum }\limits_{{l, s \in  {Q}_{i}}}{C}_{ls}^{-1}}. \tag{10.28}
$$

LLE 在低维空间中保持 ${\mathbf{w}}_{i}$ 不变,于是 ${\mathbf{x}}_{i}$ 对应的低维空间坐标 ${\mathbf{z}}_{i}$ 可通过下式求解:

$$
\mathop{\min }\limits_{{{\mathbf{z}}_{1},{\mathbf{z}}_{2},\ldots ,{\mathbf{z}}_{m}}}\mathop{\sum }\limits_{{i = 1}}^{m}{\begin{Vmatrix}{\mathbf{z}}_{i} - \mathop{\sum }\limits_{{j \in  {Q}_{i}}}{w}_{ij}{\mathbf{z}}_{j}\end{Vmatrix}}_{2}^{2} \tag{10.29}
$$

式(10.27)与(10.29)的优化目标同形, 唯一的区别是式(10.27)中需确定的是 ${\mathbf{w}}_{i}$ ,而式(10.29) 中需确定的是 ${\mathbf{x}}_{i}$ 对应的低维空间坐标 ${\mathbf{z}}_{i}$ .

令 $\mathbf{Z} = \left( {{\mathbf{z}}_{1},{\mathbf{z}}_{2},\ldots ,{\mathbf{z}}_{m}}\right)  \in  {\mathbb{R}}^{{d}^{\prime } \times  m},{\left( \mathbf{W}\right) }_{ij} = {w}_{ij}$ ,

$$
\mathbf{M} = {\left( \mathbf{I} - \mathbf{W}\right) }^{\mathrm{T}}\left( {\mathbf{I} - \mathbf{W}}\right) , \tag{10.30}
$$

则式(10.29)可重写为

$$
\mathop{\min }\limits_{\mathbf{Z}}\operatorname{tr}\left( {\mathbf{Z}\mathbf{M}{\mathbf{Z}}^{\mathrm{T}}}\right) , \tag{10.31}
$$

$$
\text{ s.t. }{\mathbf{{ZZ}}}^{\mathrm{T}} = \mathbf{I}\text{ . }
$$

式(10.31)可通过特征值分解求解: $\mathbf{M}$ 最小的 ${d}^{\prime }$ 个特征值对应的特征向量组成的矩阵即为 ${\mathbf{Z}}^{\mathrm{T}}$ .

LLE 的算法描述如图 10.10 所示. 算法第 4 行显示出: 对于不在样本 ${\mathbf{x}}_{i}$ 邻域区域的样本 ${\mathbf{x}}_{j}$ ,无论其如何变化都对 ${\mathbf{x}}_{i}$ 和 ${\mathbf{z}}_{i}$ 没有任何影响; 这种将变动限制在局部的思想在许多地方都有用.

---

输入:样本集 $D = \left\{  {{\mathbf{x}}_{1},{\mathbf{x}}_{2},\ldots ,{\mathbf{x}}_{m}}\right\}$ ;

		近邻参数 $k$ ;

		低维空间维数 ${d}^{\prime }$ .

过程:

	for $i = 1,2,\ldots , m$ do

2: 确定 ${\mathbf{x}}_{i}$ 的 $k$ 近邻;

3: 从式 $\left( {10.27}\right)$ 求得 ${w}_{ij}, j \in  {Q}_{i}$ ;

4: 对于 $j \notin  {Q}_{i}$ ,令 ${w}_{ij} = 0$ ;

	end for

	:从式(10.30)得到 $\mathbf{M}$ ;

7: 对 $\mathbf{M}$ 进行特征值分解;

8: return $\mathbf{M}$ 的最小 ${d}^{\prime }$ 个特征值对应的特征向量

输出: 样本集 $D$ 在低维空间的投影 $Z = \left\{  {{z}_{1},{z}_{2},\ldots ,{z}_{m}}\right\}$ .

---

图 10.10 LLE 算法

## 10.6 度量学习

在机器学习中, 对高维数据进行降维的主要目的是希望找到一个合适的低维空间, 在此空间中进行学习能比原始空间性能更好. 事实上, 每个空间对应了在样本属性上定义的一个距离度量, 而寻找合适的空间, 实质上就是在寻找一个合适的距离度量. 那么, 为何不直接尝试 “学习” 出一个合适的距离度量呢? 这就是度量学习(metric learning)的基本动机.

---

亦称 “距离度量学习” (distance metric learning).

---

欲对距离度量进行学习, 必须有一个便于学习的距离度量表达形式. 9.3 节给出了很多种距离度量的表达式, 但它们都是 “固定的”、没有可调节的参数, 因此不能通过对数据样本的学习来加以改善. 为此, 我们先来做一个推广.

对两个 $d$ 维样本 ${\mathbf{x}}_{i}$ 和 ${\mathbf{x}}_{j}$ ,它们之间的平方欧氏距离可写为

$$
{dist}_{\mathrm{{ed}}}^{2}\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = \left| \right| {\mathbf{x}}_{i} - {\mathbf{x}}_{j}{\left| \right| }_{2}^{2} = {dist}_{{ij},1}^{2} + {dist}_{{ij},2}^{2} + \ldots  + {dist}_{{ij}, d}^{2}\;, \tag{10.32}
$$

其中 ${dis}{t}_{{ij}, k}$ 表示 ${\mathbf{x}}_{i}$ 与 ${\mathbf{x}}_{j}$ 在第 $k$ 维上的距离. 若假定不同属性的重要性不同, 则可引入属性权重 $\mathbf{w}$ ,得到

$$
{\operatorname{dist}}_{\mathrm{{wed}}}^{2}\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = \left| \right| {\mathbf{x}}_{i} - {\mathbf{x}}_{j}{\left| \right| }_{2}^{2} = {w}_{1} \cdot  {\operatorname{dist}}_{{ij},1}^{2} + {w}_{2} \cdot  {\operatorname{dist}}_{{ij},2}^{2} + \ldots  + {w}_{d} \cdot  {\operatorname{dist}}_{{ij}, d}^{2}
$$

$$
= {\left( {\mathbf{x}}_{i} - {\mathbf{x}}_{j}\right) }^{\mathrm{T}}\mathbf{W}\left( {{\mathbf{x}}_{i} - {\mathbf{x}}_{j}}\right) , \tag{10.33}
$$

其中 ${w}_{i} \geq  0,\mathbf{W} = \operatorname{diag}\left( \mathbf{w}\right)$ 是一个对角矩阵, ${\left( \mathbf{W}\right) }_{ii} = {w}_{i}$ .

式(10.33)中的 $\mathbf{W}$ 可通过学习确定,但我们还能再往前走一步: $\mathbf{W}$ 的非对角元素均为零, 这意味着坐标轴是正交的, 即属性之间无关; 但现实问题中往往不是这样, 例如考虑西瓜的 “重量” 和 “体积” 这两个属性, 它们显然是正相关的, 其对应的坐标轴不再正交. 为此, 将式(10.33)中的 W 替换为一个普通的半正定对称矩阵 $\mathbf{M}$ ,于是就得到了马氏距离 (Mahalanobis distance)

$$
{\operatorname{dist}}_{\operatorname{mah}}^{2}\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = {\left( {\mathbf{x}}_{i} - {\mathbf{x}}_{j}\right) }^{\mathrm{T}}\mathbf{M}\left( {{\mathbf{x}}_{i} - {\mathbf{x}}_{j}}\right)  = {\begin{Vmatrix}{\mathbf{x}}_{i} - {\mathbf{x}}_{j}\end{Vmatrix}}_{\mathbf{M}}^{2}, \tag{10.34}
$$

其中 $\mathbf{M}$ 亦称 “度量矩阵”,而度量学习则是对 $\mathbf{M}$ 进行学习. 注意到为了保持距离非负且对称, $\mathbf{M}$ 必须是(半)正定对称矩阵,即必有正交基 $\mathbf{P}$ 使得 $\mathbf{M}$ 能写为 $\mathbf{M} = {\mathbf{{PP}}}^{\mathrm{T}}$ .

对 $\mathbf{M}$ 进行学习当然要设置一个目标. 假定我们是希望提高近邻分类器的性能, 则可将 M 直接嵌入到近邻分类器的评价指标中去, 通过优化该性能指标相应地求得 $\mathbf{M}$ . 下面我们以近邻成分分析(Neighbourhood Component Analysis, 简称 NCA) [Goldberger et al., 2005] 为例进行讨论.

近邻分类器在进行判别时通常使用多数投票法, 邻域中的每个样本投 1 票, 邻域外的样本投 0 票. 不妨将其替换为概率投票法. 对于任意样本 ${\mathbf{x}}_{j}$ ,它对 ${\mathbf{x}}_{i}$ 分类结果影响的概率为

$$
{p}_{ij} = \frac{\exp \left( {-{\begin{Vmatrix}{\mathbf{x}}_{i} - {\mathbf{x}}_{j}\end{Vmatrix}}_{\mathbf{M}}^{2}}\right) }{\mathop{\sum }\limits_{l}\exp \left( {-{\begin{Vmatrix}{\mathbf{x}}_{i} - {\mathbf{x}}_{l}\end{Vmatrix}}_{\mathbf{M}}^{2}}\right) }, \tag{10.35}
$$

---

即欧氏距离的平方, 这是为了后面推导的便利.

马氏距离以印度数学家 P. C. Mahalanobis 命名. 标准马氏距离中 $\mathbf{M}$ 是协方差矩阵的逆,即 $\mathbf{M} = \; {\mathbf{\sum }}^{-1}$ ; 在度量学习中 $\mathbf{M}$ 被赋予更大的灵活性.

---

当 $i = j$ 时， ${p}_{ij}$ 最大. 显然， ${\mathbf{x}}_{j}$ 对 ${\mathbf{x}}_{i}$ 的影响随着它们之间距离的增大而减小. 若以留一法 (LOO) 正确率的最大化为目标,则可计算 ${\mathbf{x}}_{i}$ 的留一法正确率,即它被自身之外的所有样本正确分类的概率为

$$
{p}_{i} = \mathop{\sum }\limits_{{j \in  {\Omega }_{i}}}{p}_{ij} \tag{10.36}
$$

其中 ${\Omega }_{i}$ 表示与 ${\mathbf{x}}_{i}$ 属于相同类别的样本的下标集合. 于是,整个样本集上的留一法正确率为

$$
\mathop{\sum }\limits_{{i = 1}}^{m}{p}_{i} = \mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j \in  {\Omega }_{i}}}{p}_{ij} \tag{10.37}
$$

将式(10.35)代入(10.37)，再考虑到 $\mathbf{M} = {\mathbf{{PP}}}^{\mathrm{T}}$ ，则 NCA 的优化目标为

$$
\mathop{\min }\limits_{\mathbf{P}}1 - \mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j \in  {\Omega }_{i}}}\frac{\exp \left( {-{\begin{Vmatrix}{\mathbf{P}}^{\mathrm{T}}{\mathbf{x}}_{i} - {\mathbf{P}}^{\mathrm{T}}{\mathbf{x}}_{j}\end{Vmatrix}}_{2}^{2}}\right) }{\mathop{\sum }\limits_{l}\exp \left( {-{\begin{Vmatrix}{\mathbf{P}}^{\mathrm{T}}{\mathbf{x}}_{i} - {\mathbf{P}}^{\mathrm{T}}{\mathbf{x}}_{l}\end{Vmatrix}}_{2}^{2}}\right) }. \tag{10.38}
$$

求解式(10.38)即可得到最大化近邻分类器 LOO 正确率的距离度量矩阵 $\mathbf{M}$ .

实际上, 我们不仅能把错误率这样的监督学习目标作为度量学习的优化目标, 还能在度量学习中引入领域知识. 例如, 若已知某些样本相似、某些样本不相似，则可定义 “必连” (must-link)约束集合 $\mathcal{M}$ 与 “勿连” (cannot-link)约束集合 $\mathcal{C},\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  \in  \mathcal{M}$ 表示 ${\mathbf{x}}_{i}$ 与 ${\mathbf{x}}_{j}$ 相似， $\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{k}}\right)  \in  \mathcal{C}$ 表示 ${\mathbf{x}}_{i}$ 与 ${\mathbf{x}}_{k}$ 不相似. 显然, 我们希望相似的样本之间距离较小, 不相似的样本之间距离较大, 于是可通过求解下面这个凸优化问题获得适当的度量矩阵 $\mathbf{M}$ [Xing et al.,2003]:

$$
\mathop{\min }\limits_{\mathbf{M}}\mathop{\sum }\limits_{{\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  \in  \mathcal{M}}}{\begin{Vmatrix}{\mathbf{x}}_{i} - {\mathbf{x}}_{j}\end{Vmatrix}}_{\mathbf{M}}^{2} \tag{10.39}
$$

$$
\text{ s.t. }\mathop{\sum }\limits_{{\left( {{\mathbf{x}}_{i},{\mathbf{x}}_{k}}\right)  \in  \mathcal{C}}}{\begin{Vmatrix}{\mathbf{x}}_{i} - {\mathbf{x}}_{k}\end{Vmatrix}}_{\mathbf{M}}^{2} \geq  1,
$$

$$
\mathbf{M} \succcurlyeq  0
$$

其中约束 $\mathbf{M} \succcurlyeq  0$ 表明 $\mathbf{M}$ 必须是半正定的. 式(10.39)要求在不相似样本间的距离不小于 1 的前提下, 使相似样本间的距离尽可能小.

---

留一法参见 2.2.2 节.

可用随机梯度下降法求解 [Goldberger et al., 2005].

度量学习自身通常并不要求学得的 $\mathbf{M}$ 是低秩的.

---

不同的度量学习方法针对不同目标获得 “好” 的半正定对称距离度量矩阵 $\mathbf{M}$ ,若 $\mathbf{M}$ 是一个低秩矩阵,则通过对 $\mathbf{M}$ 进行特征值分解,总能找到一组正交基,其正交基数目为矩阵 $\mathbf{M}$ 的秩 $\operatorname{rank}\left( \mathbf{M}\right)$ ,小于原属性数 $d$ . 于是,度量学习学得的结果可衍生出一个降维矩阵 $\mathbf{P} \in  {\mathbb{R}}^{d \times  \operatorname{rank}\left( \mathbf{M}\right) }$ ,能用于降维之目的.

## 10.7 阅读材料

懒惰学习方法主要有 $k$ 近邻学习器、懒惰决策树 [Friedman et al.,1996]; 朴素贝叶斯分类器能以懒惰学习方式使用, 也能以急切学习方式使用. 关于懒惰学习的更多内容可参阅 [Aha, 1997].

主成分分析是一种无监督的线性降维方法, 监督线性降维方法最著名的是线性判别分析(LDA) [Fisher, 1936], 参见 3.4 节, 其核化版本 KLDA [Baudat and Anouar, 2000] 参见 6.6 节. 通过最大化两个变量集合之间的相关性, 则可得到 “典型相关分析” (Canonical Correlation Analysis, 简称 CCA) [Hotelling, 1936] 及其核化版本 KCCA [Harden et al., 2004], 该方法在多视图学习(multiview learning) 中有广泛应用. 在模式识别领域人们发现, 直接对矩阵对象(例如一幅图像)进行降维操作会比将其拉伸为向量(例如把图像逐行拼接成一个向量)再进行降维操作有更好的性能, 于是产生了2DPCA [Yang et al., 2004]、2DLDA [Ye et al., 2005]、(2D) ${}^{2}\mathrm{{PCA}}$ [Zhang and Zhou, 2005] 等方法, 以及基于张量(tensor)的方法 [Kolda and Bader, 2009].

参见第 13 章.

除了 Isomap 和 LLE, 常见的流形学习方法还有拉普拉斯特征映射 (Lapl-cian Eigenmaps, 简称 LE) [Belkin and Niyogi, 2003]、局部切空间对齐(Local Tangent Space Alignment, 简称 LTSA) [Zhang and Zha, 2004] 等. 局部保持投影(Locality Preserving Projections, 简称 LPP) [He and Niyogi, 2004] 是基于 LE 的线性降维方法. 对监督学习而言, 根据类别信息扭曲后的低维空间常比本真低维空间更有利 [Geng et al., 2005]. 值得注意的是, 流形学习欲有效进行邻域保持则需样本密采样, 而这恰是高维情形下面临的重大障碍, 因此流形学习方法在实践中的降维性能往往没有预期的好; 但邻域保持的想法对机器学习的其他分支产生了重要影响, 例如半监督学习中有著名的流形假设、流形正则化 [Belkin et al., 2006]. [Yan et al., 2007] 从图嵌入的角度给出了降维方法的一个统一框架.

---

半监督聚类见 13.6 节.

---

将必连关系、勿连关系作为学习任务优化目标的约束，在半监督聚类的研究中使用得更早 [Wagstaff et al., 2001]. 在度量学习中, 由于这些约束是对所有样本同时发生作用 [Xing et al., 2003], 因此相应的方法被称为全局度量学习方法. 人们也尝试利用局部约束(例如邻域内的三元关系), 从而产生了局部距离度量学习方法 [Weinberger and Saul, 2009], 甚至有一些研究试图为每个样本产生最合适的距离度量 [Frome et al., 2007; Zhan et al., 2009]. 在具体的学习与优化求解方面, 不同的度量学习方法往往采用了不同的技术, 例如 [Yang et al., 2006] 将度量学习转化为判别式概率模型框架下基于样本对的二分类问题求解, [Davis et al., 2007] 将度量学习转化为信息论框架下的 Bregman 优化问题, 能方便地进行在线学习.

## 习题

1 编程实现 $k$ 近邻分类器,在西瓜数据集 ${3.0\alpha }$ 上比较其分类边界与决策树分类边界之异同.

10.2 令 ${err}\text{ 、 }{er}{r}^{ * }$ 分别表示最近邻分类器与贝叶斯最优分类器的期望错误率, 试证明

$$
{\operatorname{err}}^{ * } \leq  \operatorname{err} \leq  {\operatorname{err}}^{ * }\left( {2 - \frac{\left| \mathcal{Y}\right| }{\left| \mathcal{Y}\right|  - 1} \times  {\operatorname{err}}^{ * }}\right) . \tag{10.40}
$$

10.3 在对高维数据降维之前应先进行 “中心化”, 常见的是将协方差矩阵 ${\mathbf{{XX}}}^{\mathrm{T}}$ 转化为 ${\mathbf{{XHH}}}^{\mathrm{T}}{\mathbf{X}}^{\mathrm{T}}$ ,其中 $\mathbf{H} = \mathbf{I} - \frac{1}{m}{\mathbf{{11}}}^{\mathrm{T}}$ ,试析其效果.

10.4 在实践中,协方差矩阵 $\mathbf{X}{\mathbf{X}}^{\mathrm{T}}$ 的特征值分解常由中心化后的样本矩阵 $\mathbf{X}$ 的奇异值分解代替,试述其原因.

0.5 降维中涉及的投影矩阵通常要求是正交的. 试述正交、非正交投影矩阵用于降维的优缺点.

princomp 函数调用.

10.6 试使用 MATLAB 中的 PCA 函数对 Yale 人脸数据集进行降维, 并观察前 20 个特征向量所对应的图像.

Yale 人脸数据集见 http://vision.ucsd.edu/content /yale-face-database.

0.7 试述核化线性降维与流形学习之间的联系及优缺点.

${10.8}^{ * }\;k$ 近邻图和 $\epsilon$ 近邻图存在的短路和断路问题会给 Isomap 造成困扰,试设计一个方法缓解该问题.

* 试设计一个方法为新样本找到 LLE 降维后的低维坐标.

参见 9.3 节. 试述如何确保度量学习产生的距离能满足距离度量的四条基本性质.

---

西瓜数据集 ${3.0\alpha }$ 见 p.89 的表 4.5.

---

## 参考文献

Aha, D., ed. (1997). Lazy Learning. Kluwer, Norwell, MA.

Baudat, G. and F. Anouar. (2000). "Generalized discriminant analysis using a kernel approach." Neural Computation, 12(10):2385-2404.

Belkin, M. and P. Niyogi. (2003). "Laplacian eigenmaps for dimensionality reduction and data representation." Neural Computation, 15(6):1373-1396.

Belkin, M., P. Niyogi, and V. Sindhwani. (2006). "Manifold regularization: A geometric framework for learning from labeled and unlabeled examples." Journal of Machine Learning Research, 7:2399-2434.

Bellman, R. E. (1957). Dynamic Programming. Princeton University Press, Princeton, NJ.

Cover, T. M. and P. E. Hart. (1967). "Nearest neighbor pattern classification." IEEE Transactions on Information Theory, 13(1):21-27.

Cox, T. F. and M. A. Cox. (2001). Multidimensional Scaling. Chapman & Hal- 1/CRC, London, UK.

Davis, J. V., B. Kulis, P. Jain, S. Sra, and I. S. Dhillon. (2007). "Information-theoretic metric learning." In Proceedings of the 24th International Conference on Machine Learning (ICML), 209-216, Corvalis, OR.

Fisher, R. A. (1936). "The use of multiple measurements in taxonomic problems." Annals of Eugenics, 7(2):179-188.

Friedman, J. H., R. Kohavi, and Y. Yun. (1996). "Lazy decision trees." In Proceedings of the 13th National Conference on Aritificial Intelligence (AAAI), 717-724, Portland, OR.

Frome, A., Y. Singer, and J. Malik. (2007). "Image retrieval and classification using local distance functions." In Advances in Neural Information Processing Systems 19 (NIPS) (B. Schölkopf, J. C. Platt, and T. Hoffman, eds.), 417-424, MIT Press, Cambridge, MA.

Geng, X., D.-C. Zhan, and Z.-H. Zhou. (2005). "Supervised nonlinear dimensionality reduction for visualization and classification." IEEE Transactions on Systems, Man, and Cybernetics - Part B: Cybernetics, 35(6):1098-1107.

Goldberger, J., G. E. Hinton, S. T. Roweis, and R. R. Salakhutdinov. (2005). "Neighbourhood components analysis." In Advances in Neural Information Processing Systems 17 (NIPS) (L. K. Saul, Y. Weiss, and L. Bottou, eds.), 513-520, MIT Press, Cambridge, MA.

Harden, D. R., S. Szedmak, and J. Shawe-Taylor. (2004). "Canonical correlation analysis: An overview with application to learning methods." Neural Computation, 16(12):2639-2664.

He, X. and P. Niyogi. (2004). "Locality preserving projections." In Advances in Neural Information Processing Systems 16 (NIPS) (S. Thrun, L. K. Saul, and B. Schölkopf, eds.), 153-160, MIT Press, Cambridge, MA.

Hotelling, H. (1936). "Relations between two sets of variates." Biometrika, 28 (3-4):321-377.

Kolda, T. G. and B. W. Bader. (2009). "Tensor decompositions and applications." SIAM Review, 51(3):455-500.

Roweis, S. T. and L. K. Saul. (2000). "Locally linear embedding." Science, 290 (5500):2323-2316.

Schölkopf, B., A. Smola, and K.-R. Müller. (1998). "Nonlinear component analysis as a kernel eigenvalue problem." Neural Computation, 10(5):1299-1319.

Tenenbaum, J. B., V. de Silva, and J. C. Langford. (2000). "A global geometric framework for nonlinear dimensionality reduction." Science, 290(5500): 2319-2323.

Wagstaff, K., C. Cardie, S. Rogers, and S. Schrödl. (2001). "Constrained $k$ -means clustering with background knowledge." In Proceedings of the 18th International Conference on Machine Learning (ICML), 577-584, Williamstown, MA.

Weinberger, K. Q. and L. K. Saul. (2009). "Distance metric learning for large margin nearest neighbor classification." Journal of Machine Learning Research, 10:207-244.

Xing, E. P., A. Y. Ng, M. I. Jordan, and S. Russell. (2003). "Distance metric learning, with application to clustering with side-information." In Advances in Neural Information Processing Systems 15 (NIPS) (S. Becker, S. Thrun, and K. Obermayer, eds.), 505-512, MIT Press, Cambridge, MA.

Yan, S., D. Xu, B. Zhang, and H.-J. Zhang. (2007). "Graph embedding and extensions: A general framework for dimensionality reduction." IEEE Transactions on Pattern Analysis and Machine Intelligence, 29(1):40-51.

Yang, J., D. Zhang, A. F. Frangi, and J.-Y. Yang. (2004). "Two-dimensional PCA: A new approach to appearance-based face representation and recognition." IEEE Transactions on Pattern Analysis and Machine Intelligence, 26(1):131-137.

Yang, L., R. Jin, R. Sukthankar, and Y. Liu. (2006). "An efficient algorithm for local distance metric learning." In Proceedings of the 21st National Conference on Artificial Intelligence (AAAI), 543-548, Boston, MA.

Ye, J., R. Janardan, and Q. Li. (2005). "Two-dimensional linear discriminant analysis." In Advances in Neural Information Processing Systems 17 (NIPS) (L. K. Saul, Y. Weiss, and L. Bottou, eds.), 1569-1576, MIT Press, Cambridge, MA.

Zhan, D.-C., Y.-F. Li, and Z.-H. Zhou. (2009). "Learning instance specific distances using metric propagation." In Proceedings of the 26th International Conference on Machine Learning (ICML), 1225-1232, Montreal, Canada.

Zhang, D. and Z.-H. Zhou. (2005). "(2D)2PCA: 2-directional 2-dimensional PCA for efficient face representation and recognition." Neurocomputing, 69 (1-3):224-231.

Zhang, Z. and H. Zha. (2004). "Principal manifolds and nonlinear dimension reduction via local tangent space alignment." SIAM Journal on Scientific Computing, 26(1):313-338. 休息一会儿

![245_1615_314_275_349_0.jpg](../../images/245_1615_314_275_349_0.jpg)

## 小故事:主成分分析与卡尔·皮尔逊

主成分分析(PCA)是迄今最常用的降维方法，它有许多名字，例如线性代数中的散度矩阵奇异值分解 (SVD)、 统计学中的因子分析 (factor analysis)、信号处理中的离散 Karhünen-Loève 变换、图像分析中的 Hotelling 变换、文本分析中的潜在语义分析 (LSA)、机械工程中的本征正交分解 (POD)、气象学中的经验直交函数 (EOF)、结构动力学中的经验模分析 (EMA)、心理测量学中的 Schmidt-Mirsky 定理等.

卡尔・皮尔逊 (Karl Pearson, 1857-1936) 在 1901 年发明了 PCA. 皮尔逊是一位罕见的百科全书式的学者，他是统计学家、应用数学家、哲学家、历史学家、民俗学家、宗教学家、人类学家、语言学家，还是社会活动家、教育改革家、作家. 1879 年他从剑桥大学国王学院数学系毕业，此后到德国海德堡大学、柏林大学等地游学，涉猎广泛. 1884 年他开始在伦敦大学学院 (University College London, 简称 UCL) 担任应用数学讲席教授, 39 岁时成为英国皇家学会会士. 他在 1892 年出版的科学哲学经典名著《科学的规范》, 为爱因斯坦创立相对论提供了启发. 皮尔逊对统计学作出了极为重要的贡献，例如他提出了相关系数、标准差、卡方检验、矩估计等，并为假设检验理论、统计决策理论奠定了基础，被尊为 “统计学之父”.

皮尔逊开展统计学研究是因受到了生物学家 F. Galton 和 W. Welton 的影响, 希望使进化论能进行定量描述和分析. 1901 年他们三人创立了著名的统计学期刊 Biometrika, 皮尔逊担任主编直至去世. 皮尔逊的独子 Egon 也是著名统计学家，是著名的 “奈曼-皮尔逊定理” 中的皮尔逊，他子承父业出任 UCL 的统计学教授以及 Biometrika 主编, 后来担任了英国皇家统计学会主席.

---

Galton 是达尔文的表弟， “优生学”发明人.

---
