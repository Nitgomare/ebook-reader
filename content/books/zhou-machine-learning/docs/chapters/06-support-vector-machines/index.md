# 第6章 支持向量机

## 6.1 间隔与支持向量

给定训练样本集 $D = \left\{  {\left( {{\mathbf{x}}_{1},{y}_{1}}\right) ,\left( {{\mathbf{x}}_{2},{y}_{2}}\right) ,\ldots ,\left( {{\mathbf{x}}_{m},{y}_{m}}\right) }\right\}  ,{y}_{i} \in  \{  - 1, + 1\}$ ,分类学习最基本的想法就是基于训练集 $D$ 在样本空间中找到一个划分超平面,将不同类别的样本分开. 但能将训练样本分开的划分超平面可能有很多, 如图 6.1 所示, 我们应该努力去找到哪一个呢?

![120_972_784_653_538_0.jpg](../../images/120_972_784_653_538_0.jpg)

图 6.1 存在多个划分超平面将两类训练样本分开

直观上看, 应该去找位于两类训练样本 “正中间” 的划分超平面, 即图 6.1 中红色的那个，因为该划分超平面对训练样本局部扰动的 “容忍” 性最好. 例如, 由于训练集的局限性或噪声的因素, 训练集外的样本可能比图 6.1 中的训练样本更接近两个类的分隔界, 这将使许多划分超平面出现错误, 而红色的超平面受影响最小. 换言之, 这个划分超平面所产生的分类结果是最鲁棒的, 对未见示例的泛化能力最强.

在样本空间中, 划分超平面可通过如下线性方程来描述:

$$
{\mathbf{w}}^{\mathrm{T}}\mathbf{x} + b = 0, \tag{6.1}
$$

其中 $\mathbf{w} = \left( {{w}_{1};{w}_{2};\ldots ;{w}_{d}}\right)$ 为法向量,决定了超平面的方向; $b$ 为位移项,决定了超平面与原点之间的距离. 显然,划分超平面可被法向量 $\mathbf{w}$ 和位移 $b$ 确定, 下面我们将其记为 $\left( {\mathbf{w}, b}\right)$ . 样本空间中任意点 $\mathbf{x}$ 到超平面 $\left( {\mathbf{w}, b}\right)$ 的距离可写为

$$
r = \frac{\left| {\mathbf{w}}^{\mathrm{T}}\mathbf{x} + b\right| }{\parallel \mathbf{w}\parallel }. \tag{6.2}
$$

假设超平面 $\left( {\mathbf{w}, b}\right)$ 能将训练样本正确分类,即对于 $\left( {{\mathbf{x}}_{i},{y}_{i}}\right)  \in  D$ ,若 ${y}_{i} = \; + 1$ ,则有 ${\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b > 0$ ; 若 ${y}_{i} =  - 1$ ,则有 ${\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b < 0$ . 令

$$
\left\{  \begin{array}{ll} {\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b \geq   + 1, & {y}_{i} =  + 1; \\  {\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b \leq   - 1, & {y}_{i} =  - 1. \end{array}\right. \tag{6.3}
$$

如图 6.2 所示，距离超平面最近的这几个训练样本点使式(6.3)的等号成立， 它们被称为 “支持向量” (support vector)，两个异类支持向量到超平面的距离之和为

$$
\gamma  = \frac{2}{\parallel \mathbf{w}\parallel } \tag{6.4}
$$

它被称为 “间隔” (margin).

![121_882_1155_764_545_0.jpg](../../images/121_882_1155_764_545_0.jpg)

图 6.2 支持向量与间隔

欲找到具有 “最大间隔” (maximum margin) 的划分超平面, 也就是要找到能满足式(6.3)中约束的参数 $w$ 和 $b$ ，使得 $\gamma$ 最大，即

$$
\mathop{\max }\limits_{{\mathbf{w}, b}}\frac{2}{\parallel \mathbf{w}\parallel } \tag{6.5}
$$

$$
\text{ s.t. }{y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b}\right)  \geq  1,\;i = 1,2,\ldots , m\text{ . }
$$

---

若超平面 $\left( {{\mathbf{w}}^{\prime },{b}^{\prime }}\right)$ 能将训练样本正确分类, 则总存在缩放变换 $\varsigma \mathbf{w} \mapsto  {\mathbf{w}}^{\prime }$ 和 $\varsigma b \mapsto  {b}^{\prime }$ 使式(6.3)成立.

每个样本点对应一个特征向量.

---

显然,为了最大化间隔,仅需最大化 $\parallel \mathbf{w}{\parallel }^{-1}$ ,这等价于最小化 $\parallel \mathbf{w}{\parallel }^{2}$ . 于是, 式(6.5)可重写为

$$
\mathop{\min }\limits_{{\mathbf{w}, b}}\frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} \tag{6.6}
$$

$$
\text{ s.t. }{y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b}\right)  \geq  1,\;i = 1,2,\ldots , m\text{ . }
$$

这就是支持向量机(Support Vector Machine, 简称 SVM)的基本型.

## 6.2 对偶问题

我们希望求解式(6.6)来得到大间隔划分超平面所对应的模型

$$
f\left( \mathbf{x}\right)  = {\mathbf{w}}^{\mathrm{T}}\mathbf{x} + b, \tag{6.7}
$$

其中 $\mathbf{w}$ 和 $b$ 是模型参数. 注意到式(6.6)本身是一个凸二次规划(convex quadratic programming) 问题, 能直接用现成的优化计算包求解, 但我们可以有更高效的办法.

对式(6.6)使用拉格朗日乘子法可得到其 “对偶问题” (dual problem). 具体来说,对式(6.6) 的每条约束添加拉格朗日乘子 ${\alpha }_{i} \geq  0$ ,则该问题的拉格朗日函数可写为

$$
L\left( {\mathbf{w}, b,\mathbf{\alpha }}\right)  = \frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} + \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}\left( {1 - {y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b}\right) }\right) , \tag{6.8}
$$

其中 $\mathbf{\alpha } = \left( {{\alpha }_{1};{\alpha }_{2};\ldots ;{\alpha }_{m}}\right)$ . 令 $L\left( {\mathbf{w}, b,\mathbf{\alpha }}\right)$ 对 $\mathbf{w}$ 和 $b$ 的偏导为零可得

$$
\mathbf{w} = \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i}{\mathbf{x}}_{i} \tag{6.9}
$$

$$
0 = \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i} \tag{6.10}
$$

将式(6.9)代入(6.8)，即可将 $L\left( {\mathbf{w}, b,\mathbf{\alpha }}\right)$ 中的 $\mathbf{w}$ 和 $b$ 消去，再考虑式(6.10)的约束，就得到式(6.6)的对偶问题

$$
\mathop{\max }\limits_{\mathbf{\alpha }}\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i} - \frac{1}{2}\mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j = 1}}^{m}{\alpha }_{i}{\alpha }_{j}{y}_{i}{y}_{j}{\mathbf{x}}_{i}^{\mathrm{T}}{\mathbf{x}}_{j} \tag{6.11}
$$

$$
\text{ s.t. }\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i} = 0\text{ , }
$$

$$
{\alpha }_{i} \geq  0,\;i = 1,2,\ldots , m.
$$

---

间隔貌似仅与 $w$ 有关， 但事实上 $b$ 通过约束隐式地影响着 $\mathbf{w}$ 的取值，进而对间隔产生影响.

参见附录 B.1.

---

解出 $\mathbf{\alpha }$ 后,求出 $\mathbf{w}$ 与 $b$ 即可得到模型

$$
f\left( \mathbf{x}\right)  = {\mathbf{w}}^{\mathrm{T}}\mathbf{x} + b
$$

$$
= \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i}{\mathbf{x}}_{i}^{\mathrm{T}}\mathbf{x} + b. \tag{6.12}
$$

从对偶问题(6.11)解出的 ${\alpha }_{i}$ 是式(6.8)中的拉格朗日乘子,它恰对应着训练样本 $\left( {{\mathbf{x}}_{i},{y}_{i}}\right)$ . 注意到式(6.6)中有不等式约束,因此上述过程需满足 KKT (Karush-Kuhn-Tucker) 条件, 即要求

$$
\left\{  \begin{array}{l} {\alpha }_{i} \geq  0; \\  {y}_{i}f\left( {\mathbf{x}}_{i}\right)  - 1 \geq  0; \\  {\alpha }_{i}\left( {{y}_{i}f\left( {\mathbf{x}}_{i}\right)  - 1}\right)  = 0. \end{array}\right. \tag{6.13}
$$

于是,对任意训练样本 $\left( {{\mathbf{x}}_{i},{y}_{i}}\right)$ ,总有 ${\alpha }_{i} = 0$ 或 ${y}_{i}f\left( {\mathbf{x}}_{i}\right)  = 1$ . 若 ${\alpha }_{i} = 0$ ,则该样本将不会在式(6.12) 的求和中出现,也就不会对 $f\left( \mathbf{x}\right)$ 有任何影响; 若 ${\alpha }_{i} > 0$ , 则必有 ${y}_{i}f\left( {\mathbf{x}}_{i}\right)  = 1$ ,所对应的样本点位于最大间隔边界上,是一个支持向量. 这显示出支持向量机的一个重要性质: 训练完成后, 大部分的训练样本都不需保留, 最终模型仅与支持向量有关.

那么, 如何求解式(6.11) 呢? 不难发现, 这是一个二次规划问题, 可使用通用的二次规划算法来求解; 然而, 该问题的规模正比于训练样本数, 这会在实际任务中造成很大的开销. 为了避开这个障碍, 人们通过利用问题本身的特性, 提出了很多高效算法, SMO (Sequential Minimal Optimization) 是其中一个著名的代表 [Platt, 1998].

SMO 的基本思路是先固定 ${\alpha }_{i}$ 之外的所有参数,然后求 ${\alpha }_{i}$ 上的极值. 由于存在约束 $\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i} = 0$ ,若固定 ${\alpha }_{i}$ 之外的其他变量,则 ${\alpha }_{i}$ 可由其他变量导出. 于是, SMO 每次选择两个变量 ${\alpha }_{i}$ 和 ${\alpha }_{j}$ ,并固定其他参数. 这样,在参数初始化后, SMO 不断执行如下两个步骤直至收敛:

- 选取一对需更新的变量 ${\alpha }_{i}$ 和 ${\alpha }_{j}$ ; - 固定 ${\alpha }_{i}$ 和 ${\alpha }_{j}$ 以外的参数,求解式(6.11)获得更新后的 ${\alpha }_{i}$ 和 ${\alpha }_{j}$ .

---

参见附录 B.1.

如 [Vapnik, 1999] 所述， 支持向量机这个名字强调了此类学习器的关键是如何从支持向量构建出解； 同时也暗示着其复杂度主要与支持向量的数目有关.

二次规划参见附录 B.2.

---

注意到只需选取的 ${\alpha }_{i}$ 和 ${\alpha }_{j}$ 中有一个不满足 KKT 条件(6.13),目标函数就会在迭代后减小 [Osuna et al., 1997]. 直观来看, KKT 条件违背的程度越大, 则变量更新后可能导致的目标函数值减幅越大. 于是, SMO 先选取违背 KKT 条件程度最大的变量. 第二个变量应选择一个使目标函数值减小最快的变量, 但由于比较各变量所对应的目标函数值减幅的复杂度过高, 因此 SMO 采用了一个启发式: 使选取的两变量所对应样本之间的间隔最大. 一种直观的解释是, 这样的两个变量有很大的差别, 与对两个相似的变量进行更新相比, 对它们进行更新会带给目标函数值更大的变化.

SMO 算法之所以高效, 恰由于在固定其他参数后, 仅优化两个参数的过程能做到非常高效. 具体来说,仅考虑 ${\alpha }_{i}$ 和 ${\alpha }_{j}$ 时,式(6.11)中的约束可重写为

$$
{\alpha }_{i}{y}_{i} + {\alpha }_{j}{y}_{j} = c,\;{\alpha }_{i} \geq  0,\;{\alpha }_{j} \geq  0, \tag{6.14}
$$

其中

$$
c =  - \mathop{\sum }\limits_{{k \neq  i, j}}{\alpha }_{k}{y}_{k} \tag{6.15}
$$

是使 $\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i} = 0$ 成立的常数. 用

$$
{\alpha }_{i}{y}_{i} + {\alpha }_{j}{y}_{j} = c \tag{6.16}
$$

消去式(6.11)中的变量 ${\alpha }_{j}$ ,则得到一个关于 ${\alpha }_{i}$ 的单变量二次规划问题,仅有的约束是 ${\alpha }_{i} \geq  0$ . 不难发现,这样的二次规划问题具有闭式解,于是不必调用数值优化算法即可高效地计算出更新后的 ${\alpha }_{i}$ 和 ${\alpha }_{j}$ .

如何确定偏移项 $b$ 呢? 注意到对任意支持向量 $\left( {{\mathbf{x}}_{s},{y}_{s}}\right)$ 都有 ${y}_{s}f\left( {\mathbf{x}}_{s}\right)  = 1$ , 即

$$
{y}_{s}\left( {\mathop{\sum }\limits_{{i \in  S}}{\alpha }_{i}{y}_{i}{\mathbf{x}}_{i}^{\mathrm{T}}{\mathbf{x}}_{s} + b}\right)  = 1, \tag{6.17}
$$

其中 $S = \left\{  {i \mid  {\alpha }_{i} > 0, i = 1,2,\ldots , m}\right\}$ 为所有支持向量的下标集. 理论上,可选取任意支持向量并通过求解式(6.17)获得 $b$ ,但现实任务中常采用一种更鲁棒的做法: 使用所有支持向量求解的平均值

$$
b = \frac{1}{\left| S\right| }\mathop{\sum }\limits_{{s \in  S}}\left( {{y}_{s} - \mathop{\sum }\limits_{{i \in  S}}{\alpha }_{i}{y}_{i}{\mathbf{x}}_{i}^{\mathrm{T}}{\mathbf{x}}_{s}}\right) . \tag{6.18}
$$

## 6.3 核函数

在本章前面的讨论中, 我们假设训练样本是线性可分的, 即存在一个划分超平面能将训练样本正确分类. 然而在现实任务中, 原始样本空间内也许并不存在一个能正确划分两类样本的超平面. 例如图 6.3 中的 “异或” 问题就不是线性可分的.

![125_708_528_1147_481_0.jpg](../../images/125_708_528_1147_481_0.jpg)

图 6.3 异或问题与非线性映射

对这样的问题, 可将样本从原始空间映射到一个更高维的特征空间, 使得样本在这个特征空间内线性可分. 例如在图 6.3 中, 若将原始的二维空间映射到一个合适的三维空间, 就能找到一个合适的划分超平面. 幸运的是, 如果原始空间是有限维, 即属性数有限, 那么一定存在一个高维特征空间使样本可分.

令 $\phi \left( \mathbf{x}\right)$ 表示将 $\mathbf{x}$ 映射后的特征向量，于是，在特征空间中划分超平面所对应的模型可表示为

$$
f\left( \mathbf{x}\right)  = {\mathbf{w}}^{\mathrm{T}}\phi \left( \mathbf{x}\right)  + b, \tag{6.19}
$$

其中 $\mathbf{w}$ 和 $b$ 是模型参数. 类似式(6.6),有

$$
\mathop{\min }\limits_{{\mathbf{w}, b}}\frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} \tag{6.20}
$$

$$
\text{ s.t. }{y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}\phi \left( {\mathbf{x}}_{i}\right)  + b}\right)  \geq  1,\;i = 1,2,\ldots , m\text{ . }
$$

其对偶问题是

$$
\mathop{\max }\limits_{\alpha }\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i} - \frac{1}{2}\mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j = 1}}^{m}{\alpha }_{i}{\alpha }_{j}{y}_{i}{y}_{j}\phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( {\mathbf{x}}_{j}\right) \tag{6.21}
$$

$$
\text{ s.t. }\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i} = 0\text{ , }
$$

$$
{\alpha }_{i} \geq  0,\;i = 1,2,\ldots , m.
$$

---

参见第 12 章.

---

求解式(6.21)涉及到计算 $\phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( {\mathbf{x}}_{j}\right)$ ,这是样本 ${\mathbf{x}}_{i}$ 与 ${\mathbf{x}}_{j}$ 映射到特征空间之后的内积. 由于特征空间维数可能很高, 甚至可能是无穷维, 因此直接计算 $\phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( {\mathbf{x}}_{j}\right)$ 通常是困难的. 为了避开这个障碍,可以设想这样一个函数:

$$
\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = \left\langle  {\phi \left( {\mathbf{x}}_{i}\right) ,\phi \left( {\mathbf{x}}_{j}\right) }\right\rangle   = \phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( {\mathbf{x}}_{j}\right) , \tag{6.22}
$$

即 ${\mathbf{x}}_{i}$ 与 ${\mathbf{x}}_{j}$ 在特征空间的内积等于它们在原始样本空间中通过函数 $\kappa \left( {\cdot , \cdot  }\right)$ 计算的结果. 有了这样的函数, 我们就不必直接去计算高维甚至无穷维特征空间中的内积, 于是式(6.21)可重写为

$$
\mathop{\max }\limits_{\alpha }\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i} - \frac{1}{2}\mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j = 1}}^{m}{\alpha }_{i}{\alpha }_{j}{y}_{i}{y}_{j}\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right) \tag{6.23}
$$

$$
\text{ s.t. }\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i} = 0
$$

$$
{\alpha }_{i} \geq  0,\;i = 1,2,\ldots , m.
$$

求解后即可得到

$$
f\left( \mathbf{x}\right)  = {\mathbf{w}}^{\mathrm{T}}\phi \left( \mathbf{x}\right)  + b
$$

$$
= \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i}\phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( \mathbf{x}\right)  + b
$$

$$
= \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i}\kappa \left( {\mathbf{x},{\mathbf{x}}_{i}}\right)  + b. \tag{6.24}
$$

这里的函数 $\kappa \left( {\cdot , \cdot  }\right)$ 就是 “核函数” (kernel function). 式(6.24) 显示出模型最优解可通过训练样本的核函数展开，这一展式亦称 “支持向量展式” (support vector expansion).

显然,若已知合适映射 $\phi \left( \cdot \right)$ 的具体形式,则可写出核函数 $\kappa \left( {\cdot , \cdot  }\right)$ . 但在现实任务中我们通常不知道 $\phi \left( \cdot \right)$ 是什么形式,那么,合适的核函数是否一定存在呢? 什么样的函数能做核函数呢? 我们有下面的定理:

---

这称为“核技巧” (kernel trick).

---

定理 6.1 (核函数) 令 $\mathcal{X}$ 为输入空间， $\kappa \left( {\cdot , \cdot  }\right)$ 是定义在 $\mathcal{X} \times  \mathcal{X}$ 上的对称函数,则 $\kappa$ 是核函数当且仅当对于任意数据 $D = \left\{  {{\mathbf{x}}_{1},{\mathbf{x}}_{2},\ldots ,{\mathbf{x}}_{m}}\right\}$ ,“核矩阵” (kernel matrix) $\mathbf{K}$ 总是半正定的:

$$
\mathbf{K} = \left\lbrack  \begin{matrix} \kappa \left( {{\mathbf{x}}_{1},{\mathbf{x}}_{1}}\right) & \cdots & \kappa \left( {{\mathbf{x}}_{1},{\mathbf{x}}_{j}}\right) & \cdots & \kappa \left( {{\mathbf{x}}_{1},{\mathbf{x}}_{m}}\right) \\  \vdots &  \ddots  & \vdots &  \ddots  & \vdots \\  \kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{1}}\right) & \cdots & \kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right) & \cdots & \kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{m}}\right) \\  \vdots &  \ddots  & \vdots &  \ddots  & \vdots \\  \kappa \left( {{\mathbf{x}}_{m},{\mathbf{x}}_{1}}\right) & \cdots & \kappa \left( {{\mathbf{x}}_{m},{\mathbf{x}}_{j}}\right) & \cdots & \kappa \left( {{\mathbf{x}}_{m},{\mathbf{x}}_{m}}\right)  \end{matrix}\right\rbrack
$$

定理 6.1 表明, 只要一个对称函数所对应的核矩阵半正定, 它就能作为核函数使用. 事实上, 对于一个半正定核矩阵, 总能找到一个与之对应的映射 $\phi$ . 换言之,任何一个核函数都隐式地定义了一个称为 “再生核希尔伯特空间" (Reproducing Kernel Hilbert Space, 简称 RKHS)的特征空间.

通过前面的讨论可知, 我们希望样本在特征空间内线性可分, 因此特征空间的好坏对支持向量机的性能至关重要. 需注意的是，在不知道特征映射的形式时，我们并不知道什么样的核函数是合适的，而核函数也仅是隐式地定义了这个特征空间. 于是, “核函数选择” 成为支持向量机的最大变数. 若核函数选择不合适, 则意味着将样本映射到了一个不合适的特征空间, 很可能导致性能不佳.

表 6.1 列出了几种常用的核函数.

表 6.1 常用核函数

<table><tr><td>名称</td><td>表达式</td><td>参数</td></tr><tr><td>线性核</td><td>$\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = {\mathbf{x}}_{i}^{\mathrm{T}}{\mathbf{x}}_{j}$</td><td></td></tr><tr><td>多项式核</td><td>$\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = {\left( {\mathbf{x}}_{i}^{\mathrm{T}}{\mathbf{x}}_{j}\right) }^{d}$</td><td>$d \geq  1$ 为多项式的次数</td></tr><tr><td>高斯核</td><td>$\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = \exp \left( {-\frac{\parallel {\mathbf{x}}_{i} - {\mathbf{x}}_{j}{\parallel }^{2}}{2{\sigma }^{2}}}\right)$</td><td>$\sigma  > 0$ 为高斯核的带宽(width)</td></tr><tr><td>拉普拉斯核</td><td>$\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = \exp \left( {-\frac{\begin{Vmatrix}{\mathbf{x}}_{i} - {\mathbf{x}}_{j}\end{Vmatrix}}{\sigma }}\right)$</td><td>$\sigma  > 0$</td></tr><tr><td>Sigmoid 核</td><td>$\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = \tanh \left( {\beta {\mathbf{x}}_{i}^{\mathrm{T}}{\mathbf{x}}_{j} + \theta }\right)$</td><td>$\tanh$ 为双曲正切函数, $\beta  > 0,\theta  < 0$</td></tr></table>

此外, 还可通过函数组合得到, 例如:

- 若 ${\kappa }_{1}$ 和 ${\kappa }_{2}$ 为核函数,则对于任意正数 ${\gamma }_{1}\text{ 、 }{\gamma }_{2}$ ,其线性组合

$$
{\gamma }_{1}{\kappa }_{1} + {\gamma }_{2}{\kappa }_{2} \tag{6.25}
$$

也是核函数;

---

证明可参阅 [Schölkopf and Smola, 2002].

这方面有一些基本的经验, 例如对文本数据通常采用线性核, 情况不明时可先尝试高斯核.

$d = 1$ 时退化为线性核. 高斯核亦称 RBF 核.

---

- 若 ${\kappa }_{1}$ 和 ${\kappa }_{2}$ 为核函数，则核函数的直积

$$
{\kappa }_{1} \otimes  {\kappa }_{2}\left( {\mathbf{x},\mathbf{z}}\right)  = {\kappa }_{1}\left( {\mathbf{x},\mathbf{z}}\right) {\kappa }_{2}\left( {\mathbf{x},\mathbf{z}}\right) \tag{6.26}
$$

也是核函数;

- 若 ${\kappa }_{1}$ 为核函数，则对于任意函数 $g\left( \mathbf{x}\right)$ ，

$$
\kappa \left( {\mathbf{x},\mathbf{z}}\right)  = g\left( \mathbf{x}\right) {\kappa }_{1}\left( {\mathbf{x},\mathbf{z}}\right) g\left( \mathbf{z}\right) \tag{6.27}
$$

也是核函数.

## 6.4 软间隔与正则化

在前面的讨论中, 我们一直假定训练样本在样本空间或特征空间中是线性可分的, 即存在一个超平面能将不同类的样本完全划分开. 然而, 在现实任务中往往很难确定合适的核函数使得训练样本在特征空间中线性可分; 退一步说, 即便恰好找到了某个核函数使训练集在特征空间中线性可分, 也很难断定这个貌似线性可分的结果不是由于过拟合所造成的.

缓解该问题的一个办法是允许支持向量机在一些样本上出错. 为此, 要引入 “软间隔” (soft margin)的概念, 如图 6.4 所示.

![128_904_1371_783_545_0.jpg](../../images/128_904_1371_783_545_0.jpg)

图 6.4 软间隔示意图. 红色圈出了一些不满足约束的样本.

具体来说, 前面介绍的支持向量机形式是要求所有样本均满足约束(6.3), 即所有样本都必须划分正确, 这称为 “硬间隔” (hard margin), 而软间隔则是允许某些样本不满足约束

$$
{y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b}\right)  \geq  1 \tag{6.28}
$$

当然, 在最大化间隔的同时, 不满足约束的样本应尽可能少. 于是, 优化目标可写为

$$
\mathop{\min }\limits_{{\mathbf{w}, b}}\frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} + C\mathop{\sum }\limits_{{i = 1}}^{m}{\ell }_{0/1}\left( {{y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b}\right)  - 1}\right) , \tag{6.29}
$$

其中 $C > 0$ 是一个常数, ${\ell }_{0/1}$ 是 “ $0/1$ 损失函数”

$$
{\ell }_{0/1}\left( z\right)  = \left\{  \begin{array}{ll} 1, & \text{ if }z < 0 \\  0, & \text{ otherwise } \end{array}\right. \tag{6.30}
$$

显然,当 $C$ 为无穷大时,式(6.29)迫使所有样本均满足约束(6.28),于是式(6.29)等价于(6.6); 当 $C$ 取有限值时,式(6.29)允许一些样本不满足约束.

然而, ${\ell }_{0/1}$ 非凸、非连续,数学性质不太好,使得式(6.29)不易直接求解. 于是,人们通常用其他一些函数来代替 ${\ell }_{0/1}$ ,称为 “替代损失” (surrogate loss). 替代损失函数一般具有较好的数学性质,如它们通常是凸的连续函数且是 ${\ell }_{0/1}$ 的上界. 图 6.5 给出了三种常用的替代损失函数:

$$
\text{ hinge 损失: }{\ell }_{\text{ hinge }}\left( z\right)  = \max \left( {0,1 - z}\right) \text{ ; } \tag{6.31}
$$

$$
\text{ 指数损失(exponential loss): }{\ell }_{exp}\left( z\right)  = \exp \left( {-z}\right) \text{ ; } \tag{6.32}
$$

对率损失(logistic loss): ${\ell }_{\text{ log }}\left( z\right)  = \log \left( {1 + \exp \left( {-z}\right) }\right)$ .(6.33)

若采用 hinge 损失, 则式(6.29)变成

$$
\mathop{\min }\limits_{{\mathbf{w}, b}}\frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} + C\mathop{\sum }\limits_{{i = 1}}^{m}\max \left( {0,1 - {y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b}\right) }\right) . \tag{6.34}
$$

引入 “松弛变量” (slack variables) ${\xi }_{i} \geq  0$ ,可将式(6.34)重写为

$$
\mathop{\min }\limits_{{\mathbf{w}, b,{\xi }_{i}}}\frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} + C\mathop{\sum }\limits_{{i = 1}}^{m}{\xi }_{i} \tag{6.35}
$$

$$
\text{ s.t. }{y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b}\right)  \geq  1 - {\xi }_{i}
$$

$$
{\xi }_{i} \geq  0, i = 1,2,\ldots , m.
$$

---

对率损失是对率函数的变形, 对率函数参见 3.3 节.

对率损失函数通常表示为 ${\ell }_{log}\left( \cdot \right)$ ，因此式(6.33)把式(3.15)中的 $\ln \left( \cdot \right)$ 改写为 $\log \left( \cdot \right)$ .

---

![130_760_126_1049_606_0.jpg](../../images/130_760_126_1049_606_0.jpg)

图 6.5 三种常见的替代损失函数: hinge损失、指数损失、对率损失

这就是常用的 “软间隔支持向量机”.

显然, 式(6.35)中每个样本都有一个对应的松弛变量, 用以表征该样本不满足约束 (6.28) 的程度. 但是, 与式(6.6)相似, 这仍是一个二次规划问题. 于是, 类似式(6.8), 通过拉格朗日乘子法可得到式(6.35)的拉格朗日函数

$$
L\left( {\mathbf{w}, b,\mathbf{\alpha },\mathbf{\xi },\mathbf{\mu }}\right)  = \frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} + C\mathop{\sum }\limits_{{i = 1}}^{m}{\xi }_{i}
$$

$$
+ \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}\left( {1 - {\xi }_{i} - {y}_{i}\left( {{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{i} + b}\right) }\right)  - \mathop{\sum }\limits_{{i = 1}}^{m}{\mu }_{i}{\xi }_{i}, \tag{6.36}
$$

其中 ${\alpha }_{i} \geq  0,{\mu }_{i} \geq  0$ 是拉格朗日乘子.

令 $L\left( {\mathbf{w}, b,\mathbf{\alpha },\mathbf{\xi },\mathbf{\mu }}\right)$ 对 $\mathbf{w}, b,{\xi }_{i}$ 的偏导为零可得

$$
\mathbf{w} = \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i}{\mathbf{x}}_{i} \tag{6.37}
$$

$$
0 = \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i} \tag{6.38}
$$

$$
C = {\alpha }_{i} + {\mu }_{i} \tag{6.39}
$$

将式(6.37)-(6.39)代入式(6.36)即可得到式(6.35)的对偶问题

$$
\mathop{\max }\limits_{\mathbf{\alpha }}\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i} - \frac{1}{2}\mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j = 1}}^{m}{\alpha }_{i}{\alpha }_{j}{y}_{i}{y}_{j}{\mathbf{x}}_{i}^{\mathrm{T}}{\mathbf{x}}_{j} \tag{6.40}
$$

$$
\text{ s.t. }\mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}{y}_{i} = 0\text{ , }
$$

$$
0 \leq  {\alpha }_{i} \leq  C,\;i = 1,2,\ldots , m.
$$

将式(6.40)与硬间隔下的对偶问题(6.11)对比可看出, 两者唯一的差别就在于对偶变量的约束不同: 前者是 $0 \leq  {\alpha }_{i} \leq  C$ ,后者是 $0 \leq  {\alpha }_{i}$ . 于是,可采用 6.2 节中同样的算法求解式(6.40); 在引入核函数后能得到与式(6.24)同样的支持向量展式.

类似式(6.13), 对软间隔支持向量机, KKT 条件要求

$$
\left\{  \begin{array}{l} {\alpha }_{i} \geq  0,\;{\mu }_{i} \geq  0, \\  {y}_{i}f\left( {\mathbf{x}}_{i}\right)  - 1 + {\xi }_{i} \geq  0, \\  {\alpha }_{i}\left( {{y}_{i}f\left( {\mathbf{x}}_{i}\right)  - 1 + {\xi }_{i}}\right)  = 0, \\  {\xi }_{i} \geq  0,{\mu }_{i}{\xi }_{i} = 0. \end{array}\right. \tag{6.41}
$$

于是,对任意训练样本 $\left( {{\mathbf{x}}_{i},{y}_{i}}\right)$ ,总有 ${\alpha }_{i} = 0$ 或 ${y}_{i}f\left( {\mathbf{x}}_{i}\right)  = 1 - {\xi }_{i}$ . 若 ${\alpha }_{i} = 0$ ,则该样本不会对 $f\left( \mathbf{x}\right)$ 有任何影响; 若 ${\alpha }_{i} > 0$ ,则必有 ${y}_{i}f\left( {\mathbf{x}}_{i}\right)  = 1 - {\xi }_{i}$ ,即该样本是支持向量: 由式 (6.39) 可知,若 ${\alpha }_{i} < C$ ,则 ${\mu }_{i} > 0$ ,进而有 ${\xi }_{i} = 0$ ,即该样本恰在最大间隔边界上; 若 ${\alpha }_{i} = C$ ,则有 ${\mu }_{i} = 0$ ,此时若 ${\xi }_{i} \leq  1$ 则该样本落在最大间隔内部,若 ${\xi }_{i} > 1$ 则该样本被错误分类. 由此可看出,软间隔支持向量机的最终模型仅与支持向量有关，即通过采用 hinge 损失函数仍保持了稀疏性.

## 那么，能否对式(6.29)使用其他的替代损失函数呢？

可以发现,如果使用对率损失函数 ${\ell }_{log}$ 来替代式(6.29)中的 $0/1$ 损失函数, 则几乎就得到了对率回归模型(3.27). 实际上, 支持向量机与对率回归的优化目标相近, 通常情形下它们的性能也相当. 对率回归的优势主要在于其输出具有自然的概率意义, 即在给出预测标记的同时也给出了概率, 而支持向量机的输出不具有概率意义, 欲得到概率输出需进行特殊处理 [Platt, 2000]; 此外, 对率回归能直接用于多分类任务，支持向量机为此则需进行推广[Hsu and Lin, 2002]. 另一方面, 从图 6.5 可看出, hinge 损失有一块 “平坦” 的零区域, 这使得支持向量机的解具有稀疏性，而对率损失是光滑的单调递减函数，不能导出类似支持向量的概念, 因此对率回归的解依赖于更多的训练样本, 其预测开销更大.

我们还可以把式(6.29)中的 0/1 损失函数换成别的替代损失函数以得到其他学习模型, 这些模型的性质与所用的替代函数直接相关, 但它们具有一个共性: 优化目标中的第一项用来描述划分超平面的 “间隔” 大小, 另一项 $\mathop{\sum }\limits_{{i = 1}}^{m}\ell \left( {f\left( {\mathbf{x}}_{i}\right) ,{y}_{i}}\right)$ 用来表述训练集上的误差,可写为更一般的形式

$$
\mathop{\min }\limits_{f}\Omega \left( f\right)  + C\mathop{\sum }\limits_{{i = 1}}^{m}\ell \left( {f\left( {\mathbf{x}}_{i}\right) ,{y}_{i}}\right) , \tag{6.42}
$$

参见 11.4 节.

其中 $\Omega \left( f\right)$ 称为 “结构风险” (structural risk),用于描述模型 $f$ 的某些性质; 第二项 $\mathop{\sum }\limits_{{i = 1}}^{m}\ell \left( {f\left( {\mathbf{x}}_{i}\right) ,{y}_{i}}\right)$ 称为 “经验风险” (empirical risk),用于描述模型与训练数据的契合程度; $C$ 用于对二者进行折中. 从经验风险最小化的角度来看, $\Omega \left( f\right)$ 表述了我们希望获得具有何种性质的模型(例如希望获得复杂度较小的模型), 这为引入领域知识和用户意图提供了途径; 另一方面, 该信息有助于削减假设空间, 从而降低了最小化训练误差的过拟合风险. 从这个角度来说, 式(6.42)称为 “正则化” (regularization) 问题, $\Omega \left( f\right)$ 称为正则化项, $C$ 则称为正则化常数. ${\mathrm{L}}_{p}$ 范数 (norm) 是常用的正则化项,其中 ${\mathrm{L}}_{2}$ 范数 $\parallel \mathbf{w}{\parallel }_{2}$ 倾向于 $\mathbf{w}$ 的分量取值尽量均衡,即非零分量个数尽量稠密,而 ${\mathrm{L}}_{0}$ 范数 $\parallel \mathbf{w}{\parallel }_{0}$ 和 ${\mathrm{L}}_{1}$ 范数 $\parallel \mathbf{w}{\parallel }_{1}$ 则倾向于 $\mathbf{w}$ 的分量尽量稀疏,即非零分量个数尽量少.

## 6.5 支持向量回归

现在我们来考虑回归问题. 给定训练样本 $D = \left\{  {\left( {{\mathbf{x}}_{1},{y}_{1}}\right) ,\left( {{\mathbf{x}}_{2},{y}_{2}}\right) ,\ldots }\right.$ , $\left. \left( {{\mathbf{x}}_{m},{y}_{m}}\right) \right\}  ,{y}_{i} \in  \mathbb{R}$ ,希望学得一个形如式(6.7)的回归模型,使得 $f\left( \mathbf{x}\right)$ 与 $y$ 尽可能接近, $\mathbf{w}$ 和 $b$ 是待确定的模型参数.

对样本 $\left( {\mathbf{x}, y}\right)$ ,传统回归模型通常直接基于模型输出 $f\left( \mathbf{x}\right)$ 与真实输出 $y$ 之间的差别来计算损失，当且仅当 $f\left( \mathbf{x}\right)$ 与 $y$ 完全相同时，损失才为零. 与此不同， 支持向量回归(Support Vector Regression,简称 SVR)假设我们能容忍 $f\left( \mathbf{x}\right)$ 与 $y$ 之间最多有 $\epsilon$ 的偏差,即仅当 $f\left( \mathbf{x}\right)$ 与 $y$ 之间的差别绝对值大于 $\epsilon$ 时才计算损失. 如图 6.6 所示,这相当于以 $f\left( \mathbf{x}\right)$ 为中心,构建了一个宽度为 ${2\epsilon }$ 的间隔带,若训练样本落入此间隔带, 则认为是被预测正确的.

---

正则化可理解为一种 “罚函数法”，即对不希望得到的结果施以惩罚, 从而使得优化过程趋向于希望目标. 从贝叶斯估计的角度来看，正则化项可认为是提供了模型的先验概率.

---

![133_878_124_779_547_0.jpg](../../images/133_878_124_779_547_0.jpg)

图 6.6 支持向量回归示意图. 红色显示出 $\epsilon$ -间隔带，落入其中的样本不计算损失.

于是, SVR 问题可形式化为

$$
\mathop{\min }\limits_{{\mathbf{w}, b}}\frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} + C\mathop{\sum }\limits_{{i = 1}}^{m}{\ell }_{\epsilon }\left( {f\left( {\mathbf{x}}_{i}\right)  - {y}_{i}}\right) , \tag{6.43}
$$

其中 $C$ 为正则化常数, ${\ell }_{\epsilon }$ 是图 6.7 所示的 $\epsilon$ -不敏感损失 ( $\epsilon$ -insensitive loss) 函数

$$
{\ell }_{\epsilon }\left( z\right)  = \left\{  \begin{array}{ll} 0, & \text{ if }\left| z\right|  \leq  \epsilon ; \\  \left| z\right|  - \epsilon , & \text{ otherwise. } \end{array}\right. \tag{6.44}
$$

---

间隔带两侧的松弛程度可有所不同.

---

引入松弛变量 ${\xi }_{i}$ 和 ${\widehat{\xi }}_{i}$ ，可将式(6.43)重写为

$$
\mathop{\min }\limits_{{\mathbf{w}, b,{\xi }_{i},{\widehat{\xi }}_{i}}}\frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} + C\mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\xi }_{i} + {\widehat{\xi }}_{i}}\right) \tag{6.45}
$$

$$
\text{ s.t. }f\left( {\mathbf{x}}_{i}\right)  - {y}_{i} \leq  \epsilon  + {\xi }_{i}\text{ , }
$$

$$
{y}_{i} - f\left( {\mathbf{x}}_{i}\right)  \leq  \epsilon  + {\widehat{\xi }}_{i}
$$

$$
{\xi }_{i} \geq  0,{\widehat{\xi }}_{i} \geq  0, i = 1,2,\ldots , m.
$$

![133_847_1653_889_480_0.jpg](../../images/133_847_1653_889_480_0.jpg)

图 ${6.7\epsilon }$ -不敏感损失函数

类似式(6.36),通过引入拉格朗日乘子 ${\mu }_{i} \geq  0,{\widehat{\mu }}_{i} \geq  0,{\alpha }_{i} \geq  0,{\widehat{\alpha }}_{i} \geq  0$ ,由拉格朗日乘子法可得到式(6.45)的拉格朗日函数

$$
L\left( {\mathbf{w}, b,\mathbf{\alpha },\widehat{\mathbf{\alpha }},\mathbf{\xi },\widehat{\mathbf{\xi }},\mathbf{\mu },\widehat{\mathbf{\mu }}}\right)
$$

$$
= \frac{1}{2}\parallel \mathbf{w}{\parallel }^{2} + C\mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\xi }_{i} + {\widehat{\xi }}_{i}}\right)  - \mathop{\sum }\limits_{{i = 1}}^{m}{\mu }_{i}{\xi }_{i} - \mathop{\sum }\limits_{{i = 1}}^{m}{\widehat{\mu }}_{i}{\widehat{\xi }}_{i}
$$

$$
+ \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}\left( {f\left( {\mathbf{x}}_{i}\right)  - {y}_{i} - \epsilon  - {\xi }_{i}}\right)  + \mathop{\sum }\limits_{{i = 1}}^{m}{\widehat{\alpha }}_{i}\left( {{y}_{i} - f\left( {\mathbf{x}}_{i}\right)  - \epsilon  - {\widehat{\xi }}_{i}}\right) . \tag{6.46}
$$

将式(6.7)代入，再令 $L\left( {\mathbf{w}, b,\mathbf{\alpha },\widehat{\mathbf{\alpha }},\mathbf{\xi },\widehat{\mathbf{\xi }},\mathbf{\mu },\widehat{\mathbf{\mu }}}\right)$ 对 $\mathbf{w}, b,{\xi }_{i}$ 和 ${\widehat{\xi }}_{i}$ 的偏导为零可得

$$
\mathbf{w} = \mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right) {\mathbf{x}}_{i}, \tag{6.47}
$$

$$
0 = \mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right) , \tag{6.48}
$$

$$
C = {\alpha }_{i} + {\mu }_{i}, \tag{6.49}
$$

$$
C = {\widehat{\alpha }}_{i} + {\widehat{\mu }}_{i}. \tag{6.50}
$$

将式(6.47)-(6.50)代入式(6.46)，即可得到 SVR 的对偶问题

$$
\mathop{\max }\limits_{{\mathbf{\alpha },\widehat{\mathbf{\alpha }}}}\;\mathop{\sum }\limits_{{i = 1}}^{m}{y}_{i}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right)  - \epsilon \left( {{\widehat{\alpha }}_{i} + {\alpha }_{i}}\right) \tag{6.51}
$$

$$
- \frac{1}{2}\mathop{\sum }\limits_{{i = 1}}^{m}\mathop{\sum }\limits_{{j = 1}}^{m}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right) \left( {{\widehat{\alpha }}_{j} - {\alpha }_{j}}\right) {\mathbf{x}}_{i}^{\mathrm{T}}{\mathbf{x}}_{j}
$$

$$
\text{ s.t. }\mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right)  = 0
$$

$$
0 \leq  {\alpha }_{i},{\widehat{\alpha }}_{i} \leq  C
$$

上述过程中需满足 KKT 条件，即要求

$$
\left\{  \begin{array}{l} {\alpha }_{i}\left( {f\left( {\mathbf{x}}_{i}\right)  - {y}_{i} - \epsilon  - {\xi }_{i}}\right)  = 0, \\  {\widehat{\alpha }}_{i}\left( {{y}_{i} - f\left( {\mathbf{x}}_{i}\right)  - \epsilon  - {\widehat{\xi }}_{i}}\right)  = 0, \\  {\alpha }_{i}{\widehat{\alpha }}_{i} = 0,{\xi }_{i}{\widehat{\xi }}_{i} = 0, \\  \left( {C - {\alpha }_{i}}\right) {\xi }_{i} = 0,\left( {C - {\widehat{\alpha }}_{i}}\right) {\widehat{\xi }}_{i} = 0. \end{array}\right. \tag{6.52}
$$

可以看出,当且仅当 $f\left( {\mathbf{x}}_{i}\right)  - {y}_{i} - \epsilon  - {\xi }_{i} = 0$ 时 ${\alpha }_{i}$ 能取非零值,当且仅当 ${y}_{i} - f\left( {\mathbf{x}}_{i}\right)  - \epsilon  - {\widehat{\xi }}_{i} = 0$ 时 ${\widehat{\alpha }}_{i}$ 能取非零值. 换言之,仅当样本 $\left( {{\mathbf{x}}_{i},{y}_{i}}\right)$ 不落入 $\epsilon$ -间隔带中,相应的 ${\alpha }_{i}$ 和 ${\widehat{\alpha }}_{i}$ 才能取非零值. 此外,约束 $f\left( {\mathbf{x}}_{i}\right)  - {y}_{i} - \epsilon  - {\xi }_{i} = 0$ 和 ${y}_{i} - f\left( {\mathbf{x}}_{i}\right)  - \epsilon  - {\widehat{\xi }}_{i} = 0$ 不能同时成立,因此 ${\alpha }_{i}$ 和 ${\widehat{\alpha }}_{i}$ 中至少有一个为零.

将式(6.47)代入(6.7)，则 SVR 的解形如

$$
f\left( \mathbf{x}\right)  = \mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right) {\mathbf{x}}_{i}^{\mathrm{T}}\mathbf{x} + b. \tag{6.53}
$$

能使式(6.53)中的 $\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right)  \neq  0$ 的样本即为 SVR 的支持向量，它们必落在 $\epsilon$ -间隔带之外. 显然, SVR 的支持向量仅是训练样本的一部分,即其解仍具有稀疏性.

由 KKT 条件(6.52)可看出,对每个样本 $\left( {{\mathbf{x}}_{i},{y}_{i}}\right)$ 都有 $\left( {C - {\alpha }_{i}}\right) {\xi }_{i} = 0$ 且 ${\alpha }_{i}\left( {f\left( {\mathbf{x}}_{i}\right)  - {y}_{i} - \epsilon  - {\xi }_{i}}\right)  = 0$ . 于是,在得到 ${\alpha }_{i}$ 后,若 $0 < {\alpha }_{i} < C$ ,则必有 ${\xi }_{i} = 0$ , 进而有

$$
b = {y}_{i} + \epsilon  - \mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right) {\mathbf{x}}_{i}^{\mathrm{T}}\mathbf{x}. \tag{6.54}
$$

因此,在求解式(6.51)得到 ${\alpha }_{i}$ 后,理论上来说,可任意选取满足 $0 < {\alpha }_{i} < C$ 的样本通过式(6.54)求得 $b$ . 实践中常采用一种更鲁棒的办法: 选取多个(或所有)满足条件 $0 < {\alpha }_{i} < C$ 的样本求解 $b$ 后取平均值.

若考虑特征映射形式(6.19), 则相应的, 式(6.47)将形如

$$
\mathbf{w} = \mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right) \phi \left( {\mathbf{x}}_{i}\right) . \tag{6.55}
$$

将式(6.55)代入(6.19)，则 SVR 可表示为

$$
f\left( \mathbf{x}\right)  = \mathop{\sum }\limits_{{i = 1}}^{m}\left( {{\widehat{\alpha }}_{i} - {\alpha }_{i}}\right) \kappa \left( {\mathbf{x},{\mathbf{x}}_{i}}\right)  + b, \tag{6.56}
$$

---

落在 $\epsilon$ -间隔带中的样本都满足 ${\alpha }_{i} = 0$ 且 ${\widehat{\alpha }}_{i} = 0$ .

---

其中 $\kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)  = \phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( {\mathbf{x}}_{j}\right)$ 为核函数.

## 6.6 核方法

回顾式(6.24)和(6.56)可发现,给定训练样本 $\left\{  {\left( {{\mathbf{x}}_{1},{y}_{1}}\right) ,\left( {{\mathbf{x}}_{2},{y}_{2}}\right) ,\ldots }\right.$ , $\left. \left( {{\mathbf{x}}_{m},{y}_{m}}\right) \right\}$ ,若不考虑偏移项 $b$ ,则无论 SVM 还是 SVR,学得的模型总能表示成核函数 $\kappa \left( {\mathbf{x},{\mathbf{x}}_{i}}\right)$ 的线性组合. 不仅如此，事实上我们有下面这个称为 “表示定理" (representer theorem)的更一般的结论:

定理 6.2 (表示定理) 令 $\mathbb{H}$ 为核函数 $\kappa$ 对应的再生核希尔伯特空间, $\parallel h{\parallel }_{\mathbb{H}}$ 表示 $\mathbb{H}$ 空间中关于 $h$ 的范数,对于任意单调递增函数 $\Omega  : \left\lbrack  {0,\infty }\right\rbrack   \mapsto  \mathbb{R}$ 和任意非负损失函数 $\ell  : {\mathbb{R}}^{m} \mapsto  \left\lbrack  {0,\infty }\right\rbrack$ ,优化问题

$$
\mathop{\min }\limits_{{h \in  \mathbb{H}}}F\left( h\right)  = \Omega \left( {\parallel h{\parallel }_{\mathbb{H}}}\right)  + \ell \left( {h\left( {\mathbf{x}}_{1}\right) , h\left( {\mathbf{x}}_{2}\right) ,\ldots , h\left( {\mathbf{x}}_{m}\right) }\right) \tag{6.57}
$$

的解总可写为

$$
{h}^{ * }\left( \mathbf{x}\right)  = \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}\kappa \left( {\mathbf{x},{\mathbf{x}}_{i}}\right) . \tag{6.58}
$$

表示定理对损失函数没有限制,对正则化项 $\Omega$ 仅要求单调递增,甚至不要求 $\Omega$ 是凸函数,意味着对于一般的损失函数和正则化项,优化问题(6.57)的最优解 ${h}^{ * }\left( \mathbf{x}\right)$ 都可表示为核函数 $\kappa \left( {\mathbf{x},{\mathbf{x}}_{i}}\right)$ 的线性组合; 这显示出核函数的巨大威力.

人们发展出一系列基于核函数的学习方法, 统称为 “核方法” (kernel methods). 最常见的, 是通过 “核化” (即引入核函数)来将线性学习器拓展为非线性学习器. 下面我们以线性判别分析为例来演示如何通过核化来对其进行非线性拓展, 从而得到 “核线性判别分析” (Kernelized Linear Discriminant Analysis, 简称 KLDA).

我们先假设可通过某种映射 $\phi  : \mathcal{X} \mapsto  \mathbb{F}$ 将样本映射到一个特征空间 $\mathbb{F}$ ,然后在 $\mathbb{F}$ 中执行线性判别分析,以求得

$$
h\left( \mathbf{x}\right)  = {\mathbf{w}}^{\mathrm{T}}\phi \left( \mathbf{x}\right) . \tag{6.59}
$$

---

证明参阅 [Schölkopf and Smola, 2002], 其中用到了关于实对称矩阵正定性充要条件的 Mercer 定理.

线性判别分析见 3.4 节.

---

类似于式(3.35), KLDA 的学习目标是

$$
\mathop{\max }\limits_{\mathbf{w}}J\left( \mathbf{w}\right)  = \frac{{\mathbf{w}}^{\mathrm{T}}{\mathbf{S}}_{b}^{\phi }\mathbf{w}}{{\mathbf{w}}^{\mathrm{T}}{\mathbf{S}}_{w}^{\phi }\mathbf{w}}, \tag{6.60}
$$

其中 ${\mathbf{S}}_{b}^{\phi }$ 和 ${\mathbf{S}}_{w}^{\phi }$ 分别为训练样本在特征空间 $\mathbb{F}$ 中的类间散度矩阵和类内散度矩阵. 令 ${X}_{i}$ 表示第 $i \in  \{ 0,1\}$ 类样本的集合,其样本数为 ${m}_{i}$ ; 总样本数 $m = {m}_{0} + {m}_{1}$ . 第 $i$ 类样本在特征空间 $\mathbb{F}$ 中的均值为

$$
{\mathbf{\mu }}_{i}^{\phi } = \frac{1}{{m}_{i}}\mathop{\sum }\limits_{{\mathbf{x} \in  {X}_{i}}}\phi \left( \mathbf{x}\right) , \tag{6.61}
$$

两个散度矩阵分别为

$$
{\mathbf{S}}_{b}^{\phi } = \left( {{\mathbf{\mu }}_{1}^{\phi } - {\mathbf{\mu }}_{0}^{\phi }}\right) {\left( {\mathbf{\mu }}_{1}^{\phi } - {\mathbf{\mu }}_{0}^{\phi }\right) }^{\mathrm{T}}; \tag{6.62}
$$

$$
{\mathbf{S}}_{w}^{\phi } = \mathop{\sum }\limits_{{i = 0}}^{1}\mathop{\sum }\limits_{{\mathbf{x} \in  {X}_{i}}}\left( {\phi \left( \mathbf{x}\right)  - {\mathbf{\mu }}_{i}^{\phi }}\right) {\left( \phi \left( \mathbf{x}\right)  - {\mathbf{\mu }}_{i}^{\phi }\right) }^{\mathrm{T}}. \tag{6.63}
$$

通常我们难以知道映射 $\phi$ 的具体形式,因此使用核函数 $\kappa \left( {\mathbf{x},{\mathbf{x}}_{i}}\right)  = \; \phi {\left( {\mathbf{x}}_{i}\right) }^{\mathrm{T}}\phi \left( \mathbf{x}\right)$ 来隐式地表达这个映射和特征空间 $\mathbb{F}$ . 把 $J\left( \mathbf{w}\right)$ 作为式(6.57)中的损失函数 $\ell$ ,再令 $\Omega  \equiv  0$ ,由表示定理,函数 $h\left( \mathbf{x}\right)$ 可写为

$$
h\left( \mathbf{x}\right)  = \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}\kappa \left( {\mathbf{x},{\mathbf{x}}_{i}}\right) , \tag{6.64}
$$

于是由式(6.59)可得

$$
\mathbf{w} = \mathop{\sum }\limits_{{i = 1}}^{m}{\alpha }_{i}\phi \left( {\mathbf{x}}_{i}\right) . \tag{6.65}
$$

令 $\mathbf{K} \in  {\mathbb{R}}^{m \times  m}$ 为核函数 $\kappa$ 所对应的核矩阵, ${\left( \mathbf{K}\right) }_{ij} = \kappa \left( {{\mathbf{x}}_{i},{\mathbf{x}}_{j}}\right)$ . 令 ${\mathbf{1}}_{i} \in \; \{ 1,0{\} }^{m \times  1}$ 为第 $i$ 类样本的指示向量,即 ${\mathbf{1}}_{i}$ 的第 $j$ 个分量为 1 当且仅当 ${\mathbf{x}}_{j} \in  {X}_{i}$ , 否则 ${\mathbf{1}}_{i}$ 的第 $j$ 个分量为 0 . 再令

$$
{\widehat{\mathbf{\mu }}}_{0} = \frac{1}{{m}_{0}}\mathbf{K}{\mathbf{1}}_{0}, \tag{6.66}
$$

$$
{\widehat{\mathbf{\mu }}}_{1} = \frac{1}{{m}_{1}}\mathbf{K}{\mathbf{1}}_{1}, \tag{6.67}
$$

$$
\mathbf{M} = \left( {{\widehat{\mathbf{\mu }}}_{0} - {\widehat{\mathbf{\mu }}}_{1}}\right) {\left( {\widehat{\mathbf{\mu }}}_{0} - {\widehat{\mathbf{\mu }}}_{1}\right) }^{\mathrm{T}}, \tag{6.68}
$$

$$
\mathbf{N} = {\mathbf{{KK}}}^{\mathrm{T}} - \mathop{\sum }\limits_{{i = 0}}^{1}{m}_{i}{\widehat{\mathbf{\mu }}}_{i}{\widehat{\mathbf{\mu }}}_{i}^{\mathrm{T}}. \tag{6.69}
$$

于是, 式(6.60)等价为

$$
\mathop{\max }\limits_{\mathbf{\alpha }}J\left( \mathbf{\alpha }\right)  = \frac{{\mathbf{\alpha }}^{\mathrm{T}}\mathbf{M}\mathbf{\alpha }}{{\mathbf{\alpha }}^{\mathrm{T}}\mathbf{N}\mathbf{\alpha }}. \tag{6.70}
$$

显然,使用线性判别分析求解方法即可得到 $\mathbf{\alpha }$ ,进而可由式(6.64)得到投影函数 $h\left( \mathbf{x}\right)$ .

## 6.7 阅读材料

支持向量机于 1995 年正式发表 [Cortes and Vapnik, 1995]，由于在文本分类任务中显示出卓越性能 [Joachims, 1998]，很快成为机器学习的主流技术，并直接掀起了 “统计学习” (statistical learning) 在 2000 年前后的高潮. 但实际上, 支持向量的概念早在二十世纪六十年代就已出现, 统计学习理论在七十年代就已成型. 对核函数的研究更早, Mercer 定理 [Cristianini and Shawe-Taylor, 2000] 可追溯到 1909 年, RKHS 则在四十年代就已被研究, 但在统计学习兴起后, 核技巧才真正成为机器学习的通用基本技术. 关于支持向量机和核方法有很多专门书籍和介绍性文章 [Cristianini and Shawe-Taylor, 2000; Burges, 1998; 邓乃扬 与 田英杰, 2009; Schölkopf et al., 1999; Schölkopf and Smola, 2002], 统计学习理论则可参阅 [Vapnik, 1995, 1998, 1999].

支持向量机的求解通常是借助于凸优化技术 [Boyd and Vandenberghe, 2004]. 如何提高效率, 使 SVM 能适用于大规模数据一直是研究重点. 对线性核 SVM 已有很多成果, 例如基于割平面法(cutting plane algorithm)的 SVMperf 具有线性复杂度 [Joachims, 2006], 基于随机梯度下降的 Pegasos 速度甚至更快 [Shalev-Shwartz et al., 2011], 而坐标下降法则在稀疏数据上有很高的效率 [Hsieh et al.,2008]. 非线性核 SVM 的时间复杂度在理论上不可能低于 $O\left( {m}^{2}\right)$ , 因此研究重点是设计快速近似算法, 如基于采样的 CVM [Tsang et al., 2006]、 基于低秩逼近的 Nyström 方法 [Williams and Seeger, 2001]、基于随机傅里叶特征的方法 [Rahimi and Recht, 2007]等. 最近有研究显示, 当核矩阵特征值有很大差别时, Nyström 方法往往优于随机傅里叶特征方法 [Yang et al., 2012].

支持向量机是针对二分类任务设计的, 对多分类任务要进行专门的推广 [Hsu and Lin, 2002], 对带结构输出的任务也已有相应的算法 [Tsochantaridis et al., 2005]. 支持向量回归的研究始于 [Drucker et al., 1997], [Smola and Schölkopf, 2004] 给出了一个较为全面的介绍.

---

求解方法参见 3.4 节.

线性核 SVM 迄今仍是文本分类的首选技术. 一个重要原因可能是:若将每个单词作为文本数据的一个属性, 则该属性空间维数很高, 冗余度很大, 其描述能力足以将不同文档 “打散”. 关于打散, 参见 12.4 节.

$m$ 是样本个数.

---

核函数直接决定了支持向量机与核方法的最终性能，但遗憾的是，核函数的选择是一个未决问题. 多核学习(multiple kernel learning) 使用多个核函数并通过学习获得其最优凸组合作为最终的核函数 [Lanckriet et al., 2004; Bach et al., 2004], 这实际上是在借助集成学习机制.

替代损失函数在机器学习中被广泛使用. 但是，通过求解替代损失函数得到的是否仍是原问题的解? 这在理论上称为替代损失的 “一致性" (consistency)问题. [Vapnik and Chervonenkis, 1991] 给出了基于替代损失进行经验风险最小化的一致性充要条件, [Zhang, 2004] 证明了几种常见凸替代损失函数的一致性.

SVM 已有很多软件包, 比较著名的有 LIBSVM [Chang and Lin, 2011] 和 LIBLINEAR [Fan et al., 2008] 等.

集成学习参见第 8 章.

---

一致性亦称“相合性”.

---

## 习题

LIBSVM 见 http://www.csie.ntu.edu.tw/~cjlin/libsvm/.

西瓜数据集 ${3.0\alpha }$ 见 p.89 的表 4.5.

UCI 数据集见 http://archive.ics.uci.edu/ml/.

1 试证明样本空间中任意点 $\mathbf{x}$ 到超平面 $\left( {\mathbf{w}, b}\right)$ 的距离为式(6.2).

试使用 LIBSVM,在西瓜数据集 ${3.0\alpha }$ 上分别用线性核和高斯核训练一个 SVM, 并比较其支持向量的差别.

3.3 选择两个 UCI 数据集, 分别用线性核和高斯核训练一个 SVM, 并与 BP 神经网络和 C4.5 决策树进行实验比较.

6.4 试讨论线性判别分析与线性核支持向量机在何种条件下等价.

6.5 试述高斯核 SVM 与 RBF 神经网络之间的联系.

6.6 试析 SVM 对噪声敏感的原因.

6.7 试给出式(6.52)的完整 KKT 条件.

3.8 以西瓜数据集 ${3.0\alpha }$ 的“密度”为输入,“含糖率”为输出,试使用 LIBSVM 训练一个 SVR.

6.9 试使用核技巧推广对率回归, 产生 “核对率回归”.

6.10* 试设计一个能显著减少 SVM 中支持向量的数目而不显著降低泛化性能的方法.

## 参考文献

邓乃扬 与 田英杰. (2009). 支持向量机: 理论、算法与拓展. 科学出版社, 北京.

Bach, R. R., G. R. G. Lanckriet, and M. I. Jordan. (2004). "Multiple kernel learning, conic duality, and the SMO algorithm." In Proceedings of the 21st International Conference on Machine Learning (ICML), 6-13, Banff, Canada.

Boyd, S. and L. Vandenberghe. (2004). Convex Optimization. Cambridge University Press, Cambridge, UK.

Burges, C. J. C. (1998). "A tutorial on support vector machines for pattern recognition." Data Mining and Knowledge Discovery, 2(1):121-167.

Chang, C.-C. and C.-J. Lin. (2011). "LIBSVM: A library for support vector machines." ACM Transactions on Intelligent Systems and Technology, 2(3): 27.

Cortes, C. and V. N. Vapnik. (1995). "Support vector networks." Machine Learning, 20(3):273-297.

Cristianini, N. and J. Shawe-Taylor. (2000). An Introduction to Support Vector Machines and Other Kernel-Based Learning Methods. Cambridge University Press, Cambridge, UK.

Drucker, H., C. J. C. Burges, L. Kaufman, A. J. Smola, and V. Vapnik. (1997). "Support vector regression machines." In Advances in Neural Information Processing Systems 9 (NIPS) (M. C. Mozer, M. I. Jordan, and T. Petsche, eds.), 155-161, MIT Press, Cambridge, MA.

Fan, R.-E., K.-W. Chang, C.-J. Hsieh, X.-R. Wang, and C.-J. Lin. (2008). "LIBLINEAR: A library for large linear classification." Journal of Machine Learning Research, 9:1871-1874.

Hsieh, C.-J., K.-W. Chang, C.-J. Lin, S. S. Keerthi, and S. Sundararajan. (2008). "A dual coordinate descent method for large-scale linear SVM." In Proceedings of the 25th International Conference on Machine Learning (ICML), 408-415, Helsinki, Finland.

Hsu, C.-W. and C.-J. Lin. (2002). "A comparison of methods for multi-class support vector machines." IEEE Transactions on Neural Networks, 13(2): 415-425.

Joachims, T. (1998). "Text classification with support vector machines: Learning with many relevant features." In Proceedings of the 10th European Conference on Machine Learning (ECML), 137-142, Chemnitz, Germany.

Joachims, T. (2006). "Training linear SVMs in linear time." In Proceedings of the 12th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 217-226, Philadelphia, PA.

Lanckriet, G. R. G., N. Cristianini, and M. I. Jordan P. Bartlett, L. El Ghaoui. (2004). "Learning the kernel matrix with semidefinite programming." Journal of Machine Learning Research, 5:27-72.

Osuna, E., R. Freund, and F. Girosi. (1997). "An improved training algorithm for support vector machines." In Proceedings of the IEEE Workshop on Neural Networks for Signal Processing (NNSP), 276-285, Amelia Island, FL.

Platt, J. (1998). "Sequential minimal optimization: A fast algorithm for training support vector machines." Technical Report MSR-TR-98-14, Microsoft Research.

Platt, J. (2000). "Probabilities for (SV) machines." In Advances in Large Margin Classifiers (A. Smola, P. Bartlett, B. Schölkopf, and D. Schuurmans, eds.), 61-74, MIT Press, Cambridge, MA.

Rahimi, A. and B. Recht. (2007). "Random features for large-scale kernel machines." In Advances in Neural Information Processing Systems 20 (NIPS) (J.C. Platt, D. Koller, Y. Singer, and S. Roweis, eds.), 1177-1184, MIT Press, Cambridge, MA.

Schölkopf, B., C. J. C. Burges, and A. J. Smola, eds. (1999). Advances in Kernel Methods: Support Vector Learning. MIT Press, Cambridge, MA.

Schölkopf, B. and A. J. Smola, eds. (2002). Learning with Kernels: Support Vector Machines, Regularization, Optimization and Beyond. MIT Press, Cambridge, MA.

Shalev-Shwartz, S., Y. Singer, N. Srebro, and A. Cotter. (2011). "Pegasos: Primal estimated sub-gradient solver for SVM." Mathematical Programming, 127(1):3-30.

Smola, A. J. and B. Schölkopf. (2004). "A tutorial on support vector regression." Statistics and Computing, 14(3):199-222.

Tsang, I. W., J. T. Kwok, and P. Cheung. (2006). "Core vector machines: Fast SVM training on very large data sets." Journal of Machine Learning Research, 6:363-392.

Tsochantaridis, I., T. Joachims, T. Hofmann, and Y. Altun. (2005). "Large margin methods for structured and interdependent output variables." Journal of Machine Learning Research, 6:1453-1484.

Vapnik, V. N. (1995). The Nature of Statistical Learning Theory. Springer, New York, NY.

Vapnik, V. N. (1998). Statistical Learning Theory. Wiley, New York, NY.

Vapnik, V. N. (1999). "An overview of statistical learning theory." IEEE Transactions on Neural Networks, 10(5):988-999.

Vapnik, V. N. and A. J. Chervonenkis. (1991). "The necessary and sufficient conditions for consistency of the method of empirical risk." Pattern Recognition and Image Analysis, 1(3):284-305.

Williams, C. K. and M. Seeger. (2001). "Using the Nyström method to speed up kernel machines." In Advances in Neural Information Processing Systems 13 (NIPS) (T. K. Leen, T. G. Dietterich, and V. Tresp, eds.), 682-688, MIT Press, Cambridge, MA.

Yang, T.-B., Y.-F. Li, M. Mahdavi, R. Jin, and Z.-H. Zhou. (2012), "Nyström method vs random Fourier features: A theoretical and empirical comparison." In Advances in Neural Information Processing Systems 25 (NIPS) (P. Bartlett, F. C. N. Pereira, C. J. C. Burges, L. Bottou, and K. Q. Weinberger, eds.), 485-493, MIT Press, Cambridge, MA.

Zhang, T. (2004). "Statistical behavior and consistency of classification methods based on convex risk minimization (with discussion)." Annals of Statistics, 32(5):56-85.

休息一会儿

![144_1641_300_280_359_0.jpg](../../images/144_1641_300_280_359_0.jpg)

## 小故事:统计学习理论之父弗拉基米尔·瓦普尼克

弗拉基米尔 瓦普尼克 (Vladimir N. Vapnik, 1936- ) 是杰出的数学家、统计学家、计算机科学家. 他出生于苏联，1958 年在乌兹别克国立大学获数学硕士学位，1964 年在莫斯科控制科学学院获统计学博士学位，此后一直在该校工作并担任计算机系主任. 1990 年(苏联解体的前一年)他离开苏联来到新泽西州的美国电话电报公司贝尔实验室工作，1995 年发表了最初的 SVM 文章. 当时神经网络正当红, 因此这篇文章被权威期刊 Machine Learning 要求以“支持向量网络”的名义发表.

实际上, 瓦普尼克在 1963 年就已提出了支持向量的概念, 1968 年他与另一位苏联数学家 A. Chervonenkis 提出了以他们两人的姓氏命名的 “VC 维”, 1974 年又提出了结构风险最小化原则, 使得统计学习理论在二十世纪七十年代就已成型. 但这些工作主要是以俄文发表的，直到瓦普尼克随着东欧剧变和苏联解体导致的苏联科学家移民潮来到美国，这方面的研究才在西方学术界引起重视，统计学习理论、支持向量机、核方法在二十世纪末大红大紫.

瓦普尼克 2002 年离开美国电话电报公司加入普林斯顿的 NEC 实验室, 2014 年加盟脸书(Facebook)公司人工智能实验室. 1995 年之后他还在伦敦大学、哥伦比亚大学等校任教授. 据说瓦普尼克在苏联根据一本字典自学了英语及其发音. 他有一句名言被广为传诵: “Nothing is more practical than a good theory."

---

SVM 的确与神经网络有密切联系: 若将隐层神经元数设置为训练样本数， 且每个训练样本对应一个神经元中心，则以高斯径向基函数为激活函数的 RBF 网络(参见 5.5.1 节)恰与高斯核 SVM 的预测函数相同.

---

<table><tr><td>___。</td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr></table>
