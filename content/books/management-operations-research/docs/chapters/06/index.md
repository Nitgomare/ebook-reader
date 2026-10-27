# 第6章 单纯形法的灵敏度分析与对偶


在第二章里我们用图解法进行了灵敏度分析,在第三章里我们讨论了如何用计算机输出的信息对线性规划问题进行灵敏度分析.在这一章里我们将研究如何利用最优单纯形表进行灵敏度分析.同时在本章中我们还要介绍线性规划问题的对偶问题,以及对偶问题的经济解释.

## 6.1 单纯形表的灵敏度分析

## 一、目标函数中变量系数 $c_{K}$ 的灵敏度分析

1. 在最终的单纯形表里， $x_{K}$ 是非基变量

在这种情况下，由于约束方程系数增广矩阵在迭代中只是其本身的行的初等变换，与 $c_{K}$ 没有任何关系，所以当 $c_{K}$ 变成 $c_{K} + \Delta c_{K}$ 时，在最终单纯形表中其系数的增广矩阵不变.又因为 $x_{K}$ 是非基变量，所以基变量的目标函数的系数不变，即 $\pmb{c}_{B}$ 不变，可知 $z_{K}$ 也不变，只是 $c_{K}$ 变成了 $c_{K} + \Delta c_{K}$ .这时 $\sigma_K = c_K - z_K$ 就变成了 $c_{K} + \Delta c_{K} - z_{K} = \sigma_{K} + \Delta c_{K}$ .要使得原来的最优解仍为最优解，只要 $\sigma_K + \Delta c_K\leqslant 0$ 即可，也就是 $c_{K}$ 的增量 $\Delta c_{K}\leqslant -\sigma_{K}$ 即可.

2. 在最终的单纯形表中， $x_{K}$ 是基变量

当 $c_{K}$ 变成 $c_{K} + \Delta c_{K}$ 时，同上面一样，可知在最终的单纯形表中的约束方程的增广矩阵不变，但是基变量在目标函数中的系数 $c_{B}$ 变了，则 $z_{j}(j=1,2,\cdots,n)$ 一般也变了，不妨设 $c_{B} = (c_{B1}, c_{B2}, \cdots, c_{K}, \cdots, c_{Bm})$ ，当 $c_{B}$ 变成 $(c_{B1}, c_{B2}, \cdots, c_{K} + \Delta c_{K}, \cdots, c_{Bm})$ ，则


$$
z _ {j} = \left(c _ {B 1}, c _ {B 2}, \dots , c _ {K}, \dots , c _ {B m}\right) \left(a _ {1 j} ^ {\prime}, a _ {2 j} ^ {\prime}, \dots , a _ {k j} ^ {\prime}, \dots , a _ {m j} ^ {\prime}\right) ^ {\mathrm{T}}
$$


就变成了


$$
\begin{array}{r l} z _ {j} ^ {\prime} & = \left(c _ {B 1}, c _ {B 2}, \dots , c _ {K} + \Delta c _ {K}, \dots , c _ {B m}\right) \left(a _ {1 j} ^ {\prime}, a _ {2 j} ^ {\prime}, \dots , a _ {k j} ^ {\prime}, \dots , a _ {m j} ^ {\prime}\right) ^ {\mathrm{T}} \\ & = c _ {B 1} a _ {1 j} ^ {\prime} + c _ {B 2} a _ {2 j} ^ {\prime} + \dots + \left(c _ {K} + \Delta c _ {K}\right) a _ {k j} ^ {\prime} + \dots + c _ {B m} a _ {m j} ^ {\prime} \end{array}
$$



$$
\begin{array}{l} = c _ {B 1} a _ {1 j} ^ {\prime} + c _ {B 2} a _ {2 j} ^ {\prime} + \dots + c _ {k} a _ {k j} ^ {\prime} + c _ {B m} a _ {m j} ^ {\prime} + \Delta c _ {k} a _ {k j} ^ {\prime} \\ = z _ {j} + \Delta c _ {k} a _ {k j} ^ {\prime}. \end{array}
$$


这样检验数 $\sigma_{j}(j=1,2,\cdots,m)$ 变成了 $\sigma_{j}^{\prime}$ ，有


$$
\begin{array}{r l} \sigma_ {j} ^ {\prime} & = c _ {j} - z _ {j} ^ {\prime} = c _ {j} - (z _ {j} + \Delta c _ {k} a _ {k j} ^ {\prime}) \\ & = (c _ {j} - z _ {j}) - \Delta c _ {k} a _ {k j} ^ {\prime} = \sigma_ {j} - \Delta c _ {k} a _ {k j} ^ {\prime}. \end{array}
$$


要使最优解不变, 只要当 $j \neq k$ 时, $\sigma_{j}^{\prime} \leqslant 0$ , 也就是


$$
\sigma_ {j} - \Delta c _ {k} a _ {k j} ^ {\prime} \leqslant 0,
$$



$$
\Delta c _ {k} a _ {k j} ^ {\prime} \geqslant \sigma_ {j}.
$$


当 $a_{kj}^{\prime} > 0$ 时， $\Delta c_k\geqslant \frac{\sigma_j}{a_{kj}^{\prime}}$ ，这里 $\frac{\sigma_j}{a_{kj}^{\prime}}\leqslant 0;$

当 $a_{kj}^{\prime} < 0$ 时， $\Delta c_k\leqslant \frac{\sigma_j}{a_{kj}^{\prime}}$ ，这里 $\frac{\sigma_j}{a_{kj}^{\prime}}\geqslant 0.$

而当 $j = k$ 时， $\sigma_{k}^{\prime} = c_{k} + \Delta c_{k} - z_{k}^{\prime} = c_{k} + \Delta c_{k} - z_{k} - \Delta c_{k} \cdot a_{kk}^{\prime}$ ，因为 $x_{k}$ 是基变量，可知 $\sigma_{k} = 0, a_{kk}^{\prime} = 1$ ，故知 $\sigma_{k}^{\prime} = 0$ .

这也就是说,要使最优解不变,对于除了 $a_{kk}^{\prime}$ 外的所有的小于零的 $a_{kj}^{\prime}, c_{k}$ 的增量 $\Delta c_{k}$ 都要小于等于 $\frac{\sigma_{j}}{a_{kj}^{\prime}}$ , 对于所有大于零的 $a_{kj}^{\prime}, \Delta c_{k}$ 都要大于等于 $\frac{\sigma_{j}}{a_{kj}^{\prime}}$ . 我们用数学式表示使得最优解不变的 $\Delta c$ 的变化范围为


$$
\max \left\{\frac {\sigma_ {j}}{a _ {k j} ^ {\prime}} \mid a _ {k j} ^ {\prime} > 0 \right\} \leqslant \Delta c _ {k} \leqslant \min \left\{\frac {\sigma_ {j}}{a _ {k j} ^ {\prime}} \mid a _ {k j} ^ {\prime} <   0 \right\}.
$$


下面以第二章例 1 为例, 在最终的单纯形表上对 $c_{j}$ 进行灵敏度分析. 此题的数学模型如下:


$$
\max z =50x _ {1} +100x _ {2};
$$


约束条件：


$$
\begin{array}{l}x _ {1} + x _ {2} \leqslant 300,\\2 x _ {1} + x _ {2} \leqslant 400,\\x _ {2} \leqslant 250,\\x _ {1}, x _ {2} \geqslant 0.\\\end{array}
$$


此题在第五章里,我们已得到其最终的单纯形表如表6-1所示.

表6-1

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td rowspan="2">b</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="3">2</td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>50</td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>50</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>250</td></tr><tr><td rowspan="2">2</td><td colspan="2" rowspan="2"> <span class="arithmatex">\(z_j\)</span>  <span class="arithmatex">\(c_j - z_j\)</span> </td><td>50</td><td>100</td><td>50</td><td>0</td><td>50</td><td rowspan="2">27500</td></tr><tr><td>0</td><td>0</td><td>-50</td><td>0</td><td>-50</td></tr></table>

我们先对非基变量 $s_{1}$ 的目标函数的系数 $c_{3}$ 进行灵敏度分析.

这里 $\sigma_{3}=-50$ ，所以当 $c_{3}$ 的增量 $\Delta c_{3}\leqslant-(-50)$ ，即 $\Delta c_{3}\leqslant50$ 时，最优解不变，也就是说 $s_{1}$ 的目标函数的系数 $c_{3}^{\prime}=c_{3}+\Delta c_{3}\leqslant0+50=50$ 时，最优解不变.

我们再对基变量 $x_{1}$ 的目标函数的系数 $c_{1}$ 进行灵敏度分析.

在 $a_{11}^{\prime}, a_{12}^{\prime}, a_{13}^{\prime}, a_{14}^{\prime}, a_{15}^{\prime}$ 中，除了 $a_{11}^{\prime}$ 外还知道 $a_{13}^{\prime}$ 大于零， $a_{15}^{\prime}$ 小于零，可知 $\frac{\sigma_3}{a_{13}^{\prime}} = \frac{-50}{1} = -50$ ，有 $\max \left\{\frac{\sigma_j}{a_{1j}^{\prime}} \mid a_{1j}^{\prime} > 0\right\} = \max \{-50\} = -50.$ 同样有


$$
\min \left\{\frac {\sigma_ {j}}{a _ {1 j} ^ {\prime}} \mid a _ {1 j} ^ {\prime} <   0 \right\} = \min \left\{\frac {\sigma_ {5}}{a _ {15} ^ {\prime}} \right\} = \min \left\{\frac {-50}{- 1} \right\} =50.
$$


这样可知当 $-50\leqslant \Delta c_{1} \leqslant 50$ 时，也就是 $50-50\leqslant c_{1}' = c_{1} + \Delta c_{1} \leqslant 50+50$ ，即 $0 \leqslant c_{1}' \leqslant 100$ 时最优解不变.

我们也可以按以下方法来计算出使最优解不变的 $c_{1}^{\prime}$ 的变化范围.

在最终的单纯形表中，用 $c_{1}^{\prime}$ 代替原来的 $c_{1}=50$ ，计算如表 6-2 所示.

表6-2

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td rowspan="2">b</td></tr><tr><td> <span class="arithmatex">\(c_1&#x27;\)</span> </td><td>100</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="4">2</td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(c_1&#x27;\)</span> </td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>50</td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>50</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>250</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span>  <span class="arithmatex">\(c_j - z_j\)</span> </td><td> <span class="arithmatex">\(c_1&#x27;\)</span> 0</td><td>1000</td><td> <span class="arithmatex">\(c_1&#x27; - c_1&#x27;\)</span> </td><td>00</td><td> <span class="arithmatex">\(-c_1&#x27; + 100\)</span>  <span class="arithmatex">\(c_1&#x27; - 100\)</span> </td><td></td></tr></table>

从 $\sigma_3\leqslant 0$ ，得到 $-c_{1}^{\prime}\leqslant 0$ ，即


$$
c _ {1} ^ {\prime} \geqslant 0,\tag{6.1}
$$


并且从 $\sigma_{5}\leqslant0$ , 得到 $c_{1}^{\prime}-100\leqslant0$


$$
c _ {1} ^ {\prime} \leqslant 100.\tag{6.2}
$$


从(6.1)式和(6.2)式我们知道当 $0 \leqslant c_{1}^{\prime} \leqslant 100$ 时最优解不变, 如果采取了不属于这范围的 $c_{1}^{\prime}$ , 必存在某个检验数 $\sigma_{j} > 0$ , 我们可以继续用单纯形表进行迭代, 以求出新的最优解.

用最终单纯形表对 $c_{j}$ 进行灵敏度分析, 求得使最优解保持不变的 $c_{1}, c_{3}$ 的变化范围, 与我们在第三章里用计算机求解所得的结果是一样的, 其实“管理运筹学”软件就是按这种方法进行编程, 对 $c_{j}$ 进行灵敏度分析的.

## 二、约束方程中常数项的灵敏度分析

我们在第三章对线性规划问题的计算机求解中,也曾经对约束方程中常数项 $b_{j}$ 进行了灵敏度分析.根据计算机输出的表格,我们能够知道,约束方程常数项在什么范围内变化时,其对偶价格不变,那么在用单纯形表对 $b_{j}$ 进行灵敏度分析时,首先应从单纯形表中找到有关对偶价格的信息.

在第三章里我们给出了对偶价格的定义:约束条件的常数项增加一个单位而使最优目标值得到改进的数量.根据这个定义,我们可以发现约束条件的对偶价格与松弛变量(或剩余变量,或人工变量)的 $z_{j}$ 有关.下面我们仍以第二章例1为例在其最终单纯形表上找出其约束条件的对偶价格.

此题的最终单纯形表如表 6-3 所示, 这是一个求目标函数最大值的问题.

表6-3

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td rowspan="2">b</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="5">2</td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>50</td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>50</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>250</td></tr><tr><td rowspan="2" colspan="2"> <span class="arithmatex">\(z_j\)</span>  <span class="arithmatex">\(c_j - z_j\)</span> </td><td>50</td><td>100</td><td>50</td><td>0</td><td>50</td><td>27500</td></tr><tr><td>0</td><td>0</td><td>-50</td><td>0</td><td>-50</td><td></td></tr></table>

从表 6-3 可以发现设备台时数的约束方程中的松弛变量 $s_{1}$ 的 $z_{j}$ 值 50正好等于计算机解中设备台时数的对偶价格；原料 A 约束方程中的松弛变量 $s_{2}$ 的 $z_{j}$ 值 0 正好等于计算机解中的原料 A 的对偶价格；同样原料 B 的约束方程中的松弛变量 $s_{3}$ 的 $z_{j}$ 值 50正好等于计算机解中的原料 B 的对偶价格.松弛变量的 $z_{j}$ 值是否等于对应的约束条件的对偶价格呢？回答是肯定的.

首先我们知道在最优解中 $s_{2}=50$ 是基变量,也就是说,原料 A 有 50kg 没用完,再增加原料 A 是不会带来任何利润的,故原料 A 的对偶价格为零.在最终单纯形表上当松弛变量为基变量时,都有其检验数 $\sigma_{j}$ 为零.我们又知道对任何的松弛变量,它在目标函数中的系数 $c_{j}$ 都为零,那么为基变量的松弛变量的 $z_{j}$ 也必然为零,因为 $z_{j}=c_{j}-\sigma_{j}=0-0=0$ ,这正确地反映了对于任何为基变量的松弛变量,其所对应的约束条件的对偶价格为零.

下面我们来看一看对于非基变量的松弛变量的 $z_{j}$ 值是否也正确地给出了与其对应的约束条件的对偶价格.因为对所有松弛变量都有 $c_{j} = 0$ ，所以 $z_{j} = c_{j} - \sigma_{j} = -\sigma_{j}$ .在对非基变量的目标函数的灵敏度分析中，我们知道当 $\Delta c_{j}\leqslant -\sigma_{j}$ 时最优解不变.也就是说，当 $\Delta c_{j}\leqslant -\sigma_{j}$ 时，非基变量仍然为非基变量，仍然为零.这时与其对应的约束条件譬如说设备台时数全部使用完了.只有当 $\Delta c_j\geqslant -\sigma_j$ ，也就是 $\Delta c_j\geqslant z_j$ 时，对应为非基变量的松弛变量要变成入基变量了.对于设备台时数来说，当其松弛变量在目标函数中系数从零变到 $z_{3} =50$ 时，也就是说只有当余下一个台时数的设备从不能获利变成能获利50元时，譬如说别人愿意出价50元买一台设备时，我们就不必为生产产品I，Ⅱ而使用完所有的设备台时了，这正说明了设备台时数的对偶价格就是 $z_{3} =50$ 元.同样我们也可以知道原料B的对偶价格为 $z_{5} =50$ 元.

对于含有大于等于号的约束条件,我们为了化成标准形式就添上了剩余变量.这时这个约束条件的对偶价格就和这个剩余变量的 $z_{j}$ 有关了.只不过当约束条件的常数项增加一个单位时,约束条件更严格了.这将给满足约束条件带来些困难,使最优目标函数值“恶化”而不是改进,故这时约束条件的对偶价格应取 $z_{j}$ 值的相反数 $-z_{j}$ .

对于含有等于号的约束条件,其约束条件的对偶价格就和该约束方程的人工变量有关了.其约束条件的对偶价格等于此约束方程的人工变量的 $z_{j}$ 值.

下面给出一个由最终单纯形表对于不同约束类型的对偶价格的取值,如表6-4所示.

表6-4

<table><tr><td>约束类型</td><td>对偶价格的取值</td></tr><tr><td> <span class="arithmatex">\(\leqslant\)</span> </td><td>等于这个约束条件对应的松弛变量的 <span class="arithmatex">\(z_{j}\)</span> 值</td></tr><tr><td> <span class="arithmatex">\(\geqslant\)</span> </td><td>等于与这个约束条件对应的剩余变量的 <span class="arithmatex">\(z_{j}\)</span> 值的相反数 <span class="arithmatex">\(-z_{j}\)</span> </td></tr><tr><td>=</td><td>等于与这个约束条件对应的人工变量的 <span class="arithmatex">\(z_{j}\)</span> 值</td></tr></table>

从对偶价格的定义可以知道,当对偶价格为正时,它将改进目标函数值.对于求目标函数最大值的线性规划来说,改进就是增加其目标函数值;而对求目标函数最小值的线性规划来说,改进就是减少其目标函数值.当对偶价格为负时,它将“恶化”目标函数值.对求目标函数最大值的线性规划来说,恶化就是减少其目标函数值;而对求目标函数最小值的线性规划来说,“恶化”就是增加其目标函数值.在第三章我们已提及过影子价格的概念,在求目标函数最大值的线性规划中,对偶价格等于影子价格;而在求目标函数最小值的线性规划中,影子价格为对偶价格的相反数.

由此可以得到表6-5.

表6-5

<table><tr><td rowspan="2">约束条件</td><td colspan="2">影子价格的取值</td></tr><tr><td>求目标函数最大值的线性规划</td><td>求目标函数最小值的线性规划</td></tr><tr><td> <span class="arithmatex">\(\leqslant\)</span> </td><td>等于与这个约束条件对应的松弛变量的 <span class="arithmatex">\(z_{j}\)</span> 值</td><td>等于与这个约束条件对应的松弛变量的 <span class="arithmatex">\(z_{j}\)</span> 值的相反数 <span class="arithmatex">\(-z_{j}\)</span> </td></tr><tr><td> <span class="arithmatex">\(\geqslant\)</span> </td><td>等于与这个约束条件对应的剩余变量的 <span class="arithmatex">\(z_{j}\)</span> 值的相反数 <span class="arithmatex">\(-z_{j}\)</span> </td><td>等于与这个约束条件对应的剩余变量的 <span class="arithmatex">\(z_{j}\)</span> 值</td></tr><tr><td>=</td><td>等于与这个约束条件对应的人工变量 <span class="arithmatex">\(z_{j}\)</span> 值</td><td>等于与这个约束条件对应的人工变量 <span class="arithmatex">\(z_{j}\)</span> 值的相反数 <span class="arithmatex">\(-z_{j}\)</span> </td></tr></table>

下面我们就来求出 $b_{j}$ 的变化范围， $b_{j}$ 在这个范围内变化时其对偶价格不变.

当 $b_{j}$ 变成 $b_{j}^{\prime} = b_{j} + \Delta b_{j}$ 时，由于单纯形表的迭代实际是约束方程的增广矩阵进行初等行变换， $b_{j}$ 的变化并不影响系数矩阵的迭代，故其最终单纯形表中的系数矩阵没有变化。要使其对偶价格不变，只要原来最终单纯形表中的所有 $z_{j}$ 值都不变，而 $z_{j}$ 值是由基变量的系数与系数矩阵中 $j$ 列对应元素相乘所得，即 $z_{j} = c_{B} \cdot p_{j}^{\mathrm{T}}$ 。这样基变量的系数 $c_{B}$ 不变，也就是所有的基变量仍然是基变量，即基不变时，原线性规划问题的对偶价格就不变。而要使所有的基变量仍然是基变量只要当 $b_{j}$ 变化成 $b_{j}^{\prime} = b_{j} + \Delta b_{j}$ 时，原来的基不变所得到的基本解仍然是可行解，也就是所求得的基变量的值仍然大于等于零。一般地说，由于 $b_{j}$ 的变化，资源投入起了变化，最优解是变化的。这时我们也可以看出：所谓使其对偶价格不变的 $b_{j}$ 的变化范围，也就是使其最优解的所有基变量（最优基）不变，且所得的最优解仍然是可行的 $b_{j}$ 的变化范围。下面我们来看一下当某个 $b_{k}$ 变成 $b_{k}^{\prime} = b_{k} + \Delta b_{k}$ 时在原来的最终单纯形表中的基不变的条件下，最终单纯形表会有什么变化。单纯形表的迭代实际上是约束方程的增广矩阵的行的初等变换， $b_{k}$ 的变化不会影响系数矩阵的迭代，所以最终单纯形表的系数矩阵不变，又已知最终单纯形表中的基不变，可知 $c_{B}$ 不变，这样 $z_{j} = c_{B} \cdot p_{j}^{\mathrm{T}}$ 也不变，检验数 $\sigma_{j} = c_{j} - z_{j}$ ，因此也不变，唯一带来变化的只是最终单纯形表中的 $b$ 列，那么 $b_{k}$ 变化前后的 $b$ 列到底有什么关系呢？

原来的约束方程组不妨用矩阵表示为 Ax=b，通过一些单纯形表的迭代变成以 B 为基的最终单纯形表，实际上也就是在原来的约束方程组左乘 $B^{-1}$ . 即 $B^{-1}Ax=B^{-1}b$ ，这里 $B^{-1}$ 是基 B 的逆矩阵，在初始单纯形表里的系数矩阵中的单位矩阵通过迭代在最终单纯形表里正好就变成了 $B^{-1}$ ，这里可知


$$
\boldsymbol {B} ^ {- 1} = \left( \begin{array}{r r r} 1 & 0 & - 1 \\ - 2 & 1 & 1 \\ 0 & 0 & 1 \end{array} \right),
$$


其实迭代过程也是用矩阵初等变换求 B 的逆阵 $B^{-1}$ 的过程. 这样在最终单纯形表里系数矩阵就是 $B^{-1} \cdot A$ ，基变量（记为 $x_{B}$ ）的解就为 $B^{-1}b$ ，记在单纯形表的 b 列中. 当 $b_{k}$ 变成 $b_{k} + \Delta b_{k}$ 时，也就是原来初始单纯形表中的 b 向量变成了 $b'$ 向量，这里


$$
\boldsymbol {b} = \left( \begin{array}{c} b _ {1} \\ b _ {2} \\ \vdots \\ b _ {k} \\ \vdots \\ b _ {m} \end{array} \right), \quad \boldsymbol {b} ^ {\prime} = \left( \begin{array}{c} b _ {1} \\ b _ {2} \\ \vdots \\ b _ {k} + \Delta b _ {k} \\ \vdots \\ b _ {m} \end{array} \right) = \left( \begin{array}{c} b _ {1} \\ b _ {2} \\ \vdots \\ b _ {k} \\ \vdots \\ b _ {m} \end{array} \right) + \left( \begin{array}{c} 0 \\ 0 \\ \vdots \\ \Delta b _ {k} \\ \vdots \\ 0 \end{array} \right) = \boldsymbol {b} + \left( \begin{array}{c} 0 \\ 0 \\ \vdots \\ \Delta b _ {k} \\ \vdots \\ 0 \end{array} \right).
$$


令 $\Delta\boldsymbol{b}=(0,0,\cdots,0,\Delta b_{k},0,\cdots,0)^{\mathrm{T}}$ ，则有 $b^{\prime}=b+\Delta b$ .

这样在最终单纯形表中基变量 $x_{B}$ 的解就变成了 $\boldsymbol{x}_{B}^{\prime}=\boldsymbol{B}^{-1}(\boldsymbol{b}+\Delta\boldsymbol{b})=\boldsymbol{B}^{-1}\boldsymbol{b}+\boldsymbol{B}^{-1}\Delta\boldsymbol{b}$ . 要使 $x_{B}^{\prime}$ 为可行解, 只要 $B^{-1}b+B^{-1}\Delta b\geqslant0$ 即可, 在此不等式中求出的 $\Delta b_{k}$ 的变化范围, 就是使得第 k 个约束条件的对偶价格不变的 $b_{k}$ 的变化范围.

我们知道 $B^{-1}b$ 就是原来最终单纯形表中基变量 $x_{B}$ 的值，而 $B^{-1}\Delta b$ 项中的 $\Delta b=(0,0,\cdots,0,\Delta b_{k},0,\cdots,0)^{\mathrm{T}}$ ，这样可知 $B^{-1}\Delta b$ 就等于矩阵 $B^{-1}$ 中的第 k 列乘以 $\Delta b_{k}$ 所得的结果，即


$$
\boldsymbol {B} ^ {- 1} \Delta \boldsymbol {b} = \Delta b _ {k} \cdot \boldsymbol {D} _ {K}.
$$


其中 $D_{k}$ 是 $B^{-1}$ 第k列,有


$$
\boldsymbol {D} _ {K} = \left( \begin{array}{c} d _ {1 k} ^ {\prime} \\ d _ {2 k} ^ {\prime} \\ \vdots \\ d _ {m k} ^ {\prime} \end{array} \right),
$$


则


$$
\boldsymbol {B} ^ {- 1} \Delta \boldsymbol {b} = \left( \begin{array}{c} \Delta b _ {k} \cdot d _ {1 k} ^ {\prime} \\ \Delta b _ {k} \cdot d _ {2 k} ^ {\prime} \\ \Delta b _ {k} \cdot d _ {3 k} ^ {\prime} \\ \vdots \\ \Delta b _ {k} \cdot d _ {m k} ^ {\prime} \end{array} \right).
$$


所以新的最优解 $x_{B}^{\prime}$ 有


$$
\boldsymbol {x} _ {B} ^ {\prime} = \boldsymbol {x} _ {B} + \boldsymbol {B} ^ {- 1} \Delta \boldsymbol {b} = \left( \begin{array}{c} x _ {B 1} \\ x _ {B 2} \\ \vdots \\ x _ {B m} \end{array} \right) + \left( \begin{array}{c} \Delta b _ {k} \cdot d _ {1 k} ^ {\prime} \\ \Delta b _ {k} \cdot d _ {2 k} ^ {\prime} \\ \vdots \\ \Delta b _ {k} \cdot d _ {m k} ^ {\prime} \end{array} \right).
$$


要使 $x_{B}^{\prime}\geqslant 0$ ，也就是


$$
\left( \begin{array}{c} x _ {B 1} + \Delta b _ {k} d _ {1 k} ^ {\prime} \\ x _ {B 2} + \Delta b _ {k} d _ {2 k} ^ {\prime} \\ \vdots \\ x _ {B m} + \Delta b _ {k} d _ {m k} ^ {\prime} \end{array} \right) \geqslant 0,
$$


只需要各个分量 $x_{B1}+\Delta b_{k}d'_{1k}\geqslant0,x_{B2}+\Delta b_{k}d'_{2k}\geqslant0,\cdots,x_{Bi}+\Delta b_{k}d'_{ik}\geqslant0,\cdots,x_{Bm}+\Delta b_{k}d'_{mk}\geqslant0$ 即可.在上述的不等式中求出满足所有不等式的 $\Delta b_{k}$ 的范围,也就确定了 $b_{k}$ 的变化范围, $b_{k}$ 在此范围内变化使得其对应的约束条件的对偶价格不变.

用一个数学式子来表示 $b_{k}$ 的允许变化的范围：


$$
\max \left\{- \frac {x _ {B i}}{d _ {i k} ^ {\prime}} \mid d _ {i k} ^ {\prime} > 0 \right\} \leqslant \Delta b _ {k} \leqslant \min \left\{- \frac {x _ {B i}}{d _ {i k} ^ {\prime}} \mid d _ {i k} ^ {\prime} <   0 \right\}.
$$


我们知道初始单纯形表里的系数矩阵中的单位矩阵通过迭代在最终单纯形表里就变成了 $B^{-1}$ .那么 $B^{-1}$ 的第k列怎么在最终单纯形表中确认呢？ $B^{-1}$ 的第k列是由初始单纯形表里的系数矩阵中的单位矩阵中的单位列向量 $e_{k}$ （这是一个除了第k个分量为1，其余都为0的列向量），通过迭代在最终单纯形表中就变成了 $B^{-1}$ 的第k列.如果第k个约束方程中有松弛变量，那么这个松弛变量在最终单纯形表上的系数列正好就是 $B^{-1}$ 的第k列，因为这个松弛变量在初始单纯形表上的系数列正好就是单位向量 $e_{k}$ .如果第k个约束方程有剩余变量，那么 $B^{-1}$ 的第k列正好等于这个剩余变量在最终单纯形表上的系数列的相反数，因为这个剩余变量在初始单纯形表上的系数列正好是单位向量 $e_{k}$ 的负向量.如果第k个约束方程只有人工变量，那么 $B^{-1}$ 的第k列正好是这个人工变量在最终单纯形表上的系数列，因为这个人工变量在初始单纯形表上的系数列正好是单位向量 $e_{k}$ .

下面我们仍以第二章例1为例在最终单纯形表上对 $b_{j}$ 进行灵敏度分析.此题的最终单纯形表如表6-6所示.

表6-6

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td rowspan="2">b</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="5">2</td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>50</td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>50</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>250</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>50</td><td>0</td><td>50</td><td rowspan="2">27500</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>0</td><td>0</td><td>-50</td><td>0</td><td>-50</td></tr></table>

我们对 $b_{1}$ 进行灵敏度分析，因为在第一个约束方程中含有松弛变量 $s_1$ ，所以松弛变量在最终单纯形表中的系数列 $(1, -2, 0)^{\mathrm{T}}$ 就是 $B^{-1}$ 的第一列. 因为 $d_{11}^{\prime} = 1 > 0, d_{21}^{\prime} = -2 < 0, x_{1} = 50, x_{2} = 50$ , 可知 $\max_{i} \left\{ -\frac{x_{Bi}}{d_{i1}} \cdot \middle| d_{i1}^{\prime} > 0 \right\} = -\frac{50}{1} = -50, \text{而} \min_{i} \left\{ -\frac{x_{Bi}}{d_{i1}} \middle| d_{i1}^{\prime} < 0 \right\} = \frac{-50}{-2} = 25, \text{故有当} -50 \leqslant \Delta b_{1} \leqslant 25 \text{时, 也就是当} 300 - 50 \leqslant b_{1}^{\prime} = b_{1} + \Delta b_{1} \leqslant 300 + 25, 250 \leqslant b_{1}^{\prime} \leqslant 325 \text{时, 第} 1 \text{个约束条件对偶价格不变. 结合本例的实际意义即可阐述为: 当设备台时数在} 250 \text{与} 325 \text{之间变化时, 该约束条件即设备台时数的对偶价格不变, 都为每设备台时} 50 \text{元. 这样所得的结果和用计算机计算输出的结果是一样的.}$

## 三、约束方程系数矩阵 A 的灵敏度分析

下面分两种情况讨论.

（1）在初始单纯形表上的变量 $x_{k}$ 的系数列 $p_{k}$ 改变为 $p_{k}^{\prime}$ ，经过迭代后，在最终单纯形表上 $x_{k}$ 是非基变量.

由于单纯形表的迭代是约束方程的增广矩阵的行变换， $p_{k}$ 变成 $p_{k}^{\prime}$ 仅仅影响最终单纯形表上的第 k 列数据，包括 $x_{k}$ 的系数列、 $z_{k}$ 以及 $\sigma_{k}$ ，这时最终单纯形表上的 $x_{k}$ 的系数列就变成 $B^{-1}p_{k}^{\prime}$ ，而 $z_{k}$ 就变成 $c_{B}B^{-1}p_{k}^{\prime}$ ，新的检验数 $\sigma_{k}^{\prime}=c_{k}-c_{B}B^{-1}p_{k}^{\prime}$ .

若 $\sigma_{k}^{\prime}\leqslant0$ ，则原最优解仍然是最优解；若 $\sigma_{k}^{\prime}>0$ ，则继续进行迭代以求出新的最优解.

例 1 以第二章例 1 为基础, 设该厂除了生产产品 I, II 外, 现试制成一个新产品 III, 已知生产产品 III 每件需要设备 2 台时, 并消耗原料 A 0.5kg, 原料 B 1.5kg, 获利 150元, 问该厂是否应生产该产品和生产多少?

解 这是一个增加一个新的变量的问题. 我们可以把它认为是一个改变变量 $x_{3}$ 在初始表上的系数列的问题, 从 $(0,0,0)^{\mathrm{T}}$ 变成 $(2,0.5,1.5)^{\mathrm{T}}$ . 这样在原来的最终表上添上新的一列变量, $x_{3}$ 的一列, 把它放在 $s_{3}$ 之后的第6列上, 显然 $x_{3}$ 是非基变量, 在最终表上 $(2,0.5,1.5)$ 就变成了


$$
\pmb {B} ^ {- 1} \pmb {p} _ {6} = \left( \begin{array}{c c c} 1 & 0 & - 1 \\ - 2 & 1 & 1 \\ 0 & 0 & 1 \end{array} \right) \cdot \left( \begin{array}{c} 2 \\0.5\\1.5\end{array} \right) = \left( \begin{array}{c} 2 -1.5\\ - 4 +0.5+1.5\\1.5\end{array} \right) = \left( \begin{array}{c}0.5\\ - 2 \\1.5\end{array} \right).
$$


这时 $z_{6} =50\times 0.5+100\times 1.5=25+150, \sigma_{6} = c_{6} - z_{6} =150-175= -25$ . 如表6-7所示，这时新变量的检验数 $\sigma_{6}$ 小于零，可知原最优解就是新问题的最优解，即该厂还应该生产产品I50件，产品II250件，不生产产品III可得最大利润27500元.

表6-7

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td> <span class="arithmatex">\(x_3\)</span> </td><td rowspan="2">b</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td><td>150</td></tr><tr><td rowspan="5"></td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>0.5</td><td>50</td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>-2</td><td>50</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1.5</td><td>250</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>50</td><td>0</td><td>50</td><td>175</td><td rowspan="2">27500</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>0</td><td>0</td><td>-50</td><td>0</td><td>-50</td><td>-25</td></tr></table>

例 2 假设例 1 中产品Ⅲ的工艺结构有了改进, 这时生产 1 件产品Ⅲ需要使用设备 1.5台时, 消耗原料 A 为 2 kg, 原料 B 为 1 kg, 每件产品Ⅲ的利润为 160元, 问该厂的原生产计划是否要修改?

解 首先求出 $x_{3}$ 在最终表上的系数列 $B^{-1}p_{6}^{\prime}$ (注意, 这里 $x_{3}$ 在原最终单纯形表中都是非基变量).


$$
\boldsymbol {B} ^ {- 1} \boldsymbol {p} _ {6} ^ {\prime} = \left( \begin{array}{r r r} 1 & 0 & - 1 \\ - 2 & 1 & 1 \\ 0 & 0 & 1 \end{array} \right) \cdot \left( \begin{array}{l}1.5\\ 2 \\ 1 \end{array} \right) = \left( \begin{array}{c}1.5- 1 \\ 0 \\ 1 \end{array} \right) = \left( \begin{array}{l}0.5\\ 0 \\ 1 \end{array} \right),
$$



$$
z _ {6} ^ {\prime} = (50, 0,100) \left( \begin{array}{c c} 0. & 5 \\ 0 & \\ 1 & \end{array} \right) =125,
$$



$$
\sigma_ {6} ^ {\prime} = c _ {j} ^ {\prime} - z _ {6} ^ {\prime} =160-125=35,
$$


把上述数据填入表6-8.

表 6-8

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_{B}\)</span> </td><td> <span class="arithmatex">\(x_{1}\)</span> </td><td> <span class="arithmatex">\(x_{2}\)</span> </td><td> <span class="arithmatex">\(s_{1}\)</span> </td><td> <span class="arithmatex">\(s_{2}\)</span> </td><td> <span class="arithmatex">\(s_{3}\)</span> </td><td> <span class="arithmatex">\(x_{3}\)</span> </td><td rowspan="2">b</td><td rowspan="2"></td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td><td>160</td></tr><tr><td rowspan="5">2</td><td> <span class="arithmatex">\(x_{1}\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>0.5</td><td>50</td><td> <span class="arithmatex">\(\frac{50}{0.5}\)</span> </td></tr><tr><td> <span class="arithmatex">\(s_{2}\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>0</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(x_{2}\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>250</td><td> <span class="arithmatex">\(\frac{250}{1}\)</span> </td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_{j}\)</span> </td><td>50</td><td>100</td><td>50</td><td>0</td><td>50</td><td>125</td><td rowspan="2">27500</td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_{j}-z_{j}\)</span> </td><td>0</td><td>0</td><td>-50</td><td>0</td><td>-50</td><td>35</td></tr></table>

显然，由于 $\sigma_6 > 0$ ，可知此解不是最优解，我们要进行第3次迭代，选 $x_{3}$ 为入基变量， $x_{1}$ 为出

基变量,如表 6-9 所示.

表6-9

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td> <span class="arithmatex">\(x_3\)</span> </td><td rowspan="2">b</td><td rowspan="2"></td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td><td>160</td></tr><tr><td rowspan="5">3</td><td> <span class="arithmatex">\(x_3\)</span> </td><td>160</td><td>2</td><td>0</td><td>2</td><td>0</td><td>-2</td><td>1</td><td>100</td><td>—</td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>0</td><td>50</td><td> <span class="arithmatex">\(\frac{50}{1}\)</span> </td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>-2</td><td>1</td><td>-2</td><td>0</td><td>3</td><td>0</td><td>150</td><td> <span class="arithmatex">\(\frac{150}{3}\)</span> </td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>120</td><td>100</td><td>120</td><td>0</td><td>-20</td><td>160</td><td rowspan="2">31000</td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>-70</td><td>0</td><td>-120</td><td>0</td><td>20</td><td>0</td></tr><tr><td rowspan="5">4</td><td> <span class="arithmatex">\(x_3\)</span> </td><td>160</td><td>2</td><td>0</td><td>-2</td><td>2</td><td>0</td><td>1</td><td>200</td><td rowspan="5"></td></tr><tr><td> <span class="arithmatex">\(s_3\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>0</td><td>50</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>-2</td><td>1</td><td>4</td><td>-3</td><td>0</td><td>0</td><td>0</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>120</td><td>100</td><td>80</td><td>20</td><td>0</td><td>160</td><td rowspan="2">32000</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>-70</td><td>0</td><td>-80</td><td>-20</td><td>0</td><td>0</td></tr></table>

由表 6-9 可知此规划的最优解为 $x_{1}=0, x_{2}=0, s_{1}=0, s_{2}=0, s_{3}=50, x_{3}=200$ ，此时，最大目标函数为 32000元。也就是说，该厂的新的生产计划为不生产产品 I，II，生产产品 III 200件，可获最大利润 32000元。

（2）在初始表上的变量 $x_{k}$ 的系数列 $\pmb{p}_{k}$ 改变为 $\pmb{p}_{k}^{\prime}$ ，经过迭代后，在最终表上 $x_{k}$ 是基变量，在这种情况下原最优解的可行性和最优解都可能遭到破坏，问题变得十分复杂。一般不去修改原最终表，而是重新计算。

## 四、增加一个约束条件的灵敏度分析

在原线性规划中增加一个约束条件时,先将原问题最优解的变量值代入新增的约束条件.如果满足,则说明新增的条件没有起到限制作用,故原最优解不变;否则,将新增的约束添入原最终单纯形表中进一步求解.

例 3 仍以第二章例 1 为基础, 假如除了在设备台时及原材料 A, B 上对该厂的生产有限制外,还有电力供应上的限制.最高供应电量为5000度,而生产一个产品Ⅰ需要用电10度,生产一个产品Ⅱ需要用电30度.试分析此时该厂获得最大利润的生产计划.

解 先将原问题的最优解 $x_{1}=50, x_{2}=250$ 代入用电量的约束条件


$$
10x _ {1} +30x _ {2} \leqslant 5000,
$$


得


$$
10\times 50+30\times 250=500+7500>5000,
$$


所以原来的最优解不是本例的最优解.

在用电量的约束条件中加入松弛变量 $s_{4}$ 后得


$$
10x _ {1} +30x _ {2} + s _ {4} =5000.
$$


把这个约束条件加入到原来最终单纯形表上,其中 $s_{4}$ 为基变量,如表 6-10所示.

表6-10

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td> <span class="arithmatex">\(s_4\)</span> </td><td rowspan="2">b</td><td rowspan="2">比值</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="6"></td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>0</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>0</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>250</td><td></td></tr><tr><td> <span class="arithmatex">\(s_4\)</span> </td><td>0</td><td>10</td><td>30</td><td>0</td><td>0</td><td>0</td><td>1</td><td>5 000</td><td></td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>50</td><td>0</td><td>50</td><td>0</td><td rowspan="2">27500</td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(\sigma_j=c_j-z_j\)</span> </td><td>0</td><td>0</td><td>-50</td><td>0</td><td>-50</td><td>0</td></tr></table>

表 6-10中的 $x_{1}, x_{2}$ 不是单位向量, 故进行行的线性变换, 得到表 6-11.
表 6-11

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td> <span class="arithmatex">\(s_4\)</span> </td><td rowspan="2">b</td><td rowspan="2">比值</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="6"></td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>0</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>0</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>250</td><td></td></tr><tr><td> <span class="arithmatex">\(s_4\)</span> </td><td>0</td><td>0</td><td>0</td><td>-10</td><td>0</td><td>-20</td><td>1</td><td>-3 000</td><td></td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>50</td><td>0</td><td>50</td><td>0</td><td rowspan="2">27500</td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(\sigma_j = c_j - z_j\)</span> </td><td>0</td><td>0</td><td>-50</td><td>0</td><td>-50</td><td>0</td></tr></table>

上表中的 $s_4$ 行的约束可以写为


$$
-10s _ {1} -20s _ {3} + s _ {4} = -3000.
$$


上式两边乘以-1,再加上人工变量 $a_{1}$ 得


$$
10s _ {1} +20s _ {3} - s _ {4} + a _ {1} =3000.
$$


用上式替换表6-11中的 $s_4$ 行得到表6-12.

表6-12

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td> <span class="arithmatex">\(s_4\)</span> </td><td> <span class="arithmatex">\(a_1\)</span> </td><td rowspan="2">b</td><td rowspan="2">比值</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td><td>0</td><td>-M</td></tr><tr><td rowspan="6"></td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>0</td><td>0</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>0</td><td>0</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>250</td><td></td></tr><tr><td> <span class="arithmatex">\(a_1\)</span> </td><td>-M</td><td>0</td><td>0</td><td>10</td><td>0</td><td>20</td><td>-1</td><td>1</td><td>3 000</td><td></td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>50-10M</td><td>0</td><td>50-20M</td><td>M</td><td>-M</td><td rowspan="2"></td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(σ_j=c_j-z_j\)</span> </td><td>0</td><td>0</td><td>10M-50</td><td>0</td><td>20M-50</td><td>-M</td><td>0</td></tr><tr><td rowspan="6"></td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>-1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>100</td><td></td></tr><tr><td> <span class="arithmatex">\(s_3\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>0</td><td>0</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>2</td><td>-1</td><td>0</td><td>0</td><td>0</td><td>200</td><td></td></tr><tr><td> <span class="arithmatex">\(a_1\)</span> </td><td>-M</td><td>0</td><td>0</td><td>50</td><td>-20</td><td>0</td><td>-1</td><td>1</td><td>2 000</td><td></td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>150-50M</td><td>20M-50</td><td>0</td><td>M</td><td>-M</td><td rowspan="2"></td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(σ_j=c_j-z_j\)</span> </td><td>0</td><td>0</td><td>50M-150</td><td>50-20M</td><td>0</td><td>-M</td><td>0</td></tr><tr><td rowspan="6"></td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>0</td><td>3/5</td><td>0</td><td>-1/50</td><td>1/50</td><td>140</td><td></td></tr><tr><td> <span class="arithmatex">\(s_3\)</span> </td><td>0</td><td>0</td><td>0</td><td>0</td><td>1/5</td><td>1</td><td>-2/50</td><td>2/50</td><td>130</td><td></td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>-1/5</td><td>0</td><td>2/50</td><td>-2/50</td><td>120</td><td></td></tr><tr><td> <span class="arithmatex">\(s_1\)</span> </td><td>0</td><td>0</td><td>0</td><td>1</td><td>-2/5</td><td>0</td><td>-1/50</td><td>1/50</td><td>40</td><td></td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>0</td><td>10</td><td>0</td><td>3</td><td>-3</td><td rowspan="2"></td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(σ_j=c_j-z_j\)</span> </td><td>0</td><td>0</td><td>0</td><td>-10</td><td>0</td><td>-3</td><td>-M+3</td></tr></table>

由表 6-12可知最优解为 $x_{1}=140, x_{2}=120, s_{1}=40, s_{3}=130, s_{2}=s_{4}=a_{1}=0$ ，即该工厂在添加了用电限量以后的最优生产计划为产品 I 生产 140件，产品 II 生产 120件.

在学了灵敏度分析之后,我们来看一看如何从“管理运筹学”软件的计算输出去识别线性规划问题有唯一解,还是具有无穷多组解.从单纯形法我们知道有无穷多组解的识别方法为是否存在一个非基变量的检验数为零,如果存在,则此线性规划有无穷多组解,如不存在,则此线性规划只有唯一解.

我们分两种情况进行讨论.

（1）如果在最终表上检验数为零的非基变量是松弛变量或剩余变量 $s_k$ 。显然在计算机输出中没有专门松弛变量与剩余变量栏，但是我们仍然可以从输出中找到它们的信息。首先由于是非基变量，可知在最优解中其值都为零，也就是在计算机输出的约束条件栏里，某一个约束条件的松弛或剩余变量的值为零，又因为这个非基变量的检验数为零，所以这个约束条件的对偶价格为零。反过来说，如果在计算机输出的约束条件栏里有一个约束条件的松弛或剩余变量为零，且其对偶价格也为零，那么我们就可知道有一个非基变量的松弛变量或剩余变量的检验数为零，这个线性规划有无穷多组解。

（2）如果在最终单纯形表上，检验数为零的非基变量是一般决策变量 $x_{k}$ .我们在对非基变量 $x_{k}$ 的目标系数 $c_{k}$ 的灵敏度分析中知道 $\Delta c_{k}\leqslant\sigma_{k}$ ，对任何非基变量 $x_{i}$ 在计算机输出的相差值一栏中就记录了 $\sigma_{i}$ 的值，它表示只有目标函数系数 $c_{i}$ 的增量改进了 $\sigma_{i}$ 的值， $x_{i}$ 才有可能成为基变量而取正值.因为 $\sigma_{k}=0$ ，所以我们很容易从计算机输出中识别出 $x_{k}$ ，也就是说只要在计算机输出中存在一个取值为零的决策变量并且其相差值也为零，我们就可以确认这个变量就是最终表上检验数为零的非基变量，可知此线性规划有无穷多组解.如果在计算机输出解的信息中不存在上述这两种情况，我们可以断定此线性规划只有唯一最优解.

## 6.2 线性规划的对偶问题

每一个线性规划问题,都存在一个与它密切相关的线性规划问题,我们称其中的任一个为原问题,另一个为对偶问题.在这一节中我们将揭示原问题与对偶问题的关系,如何将原问题转化为其对偶问题,如何从原问题的求解的结果中去找到其对偶问题的答案,并介绍对偶问题的经济解释以及对偶单纯形法.

我们先来看一个例题.

例 4 某工厂在计划期内安排 I, II 两种产品, 生产单位产品所需设备 A, B, C 的台时如表 6-13所示.

表6-13

<table><tr><td></td><td>I</td><td>II</td><td>资源限量</td></tr><tr><td>设备A</td><td>1</td><td>1</td><td>300台时</td></tr><tr><td>设备B</td><td>2</td><td>1</td><td>400台时</td></tr><tr><td>设备C</td><td>0</td><td>1</td><td>250台时</td></tr></table>

教学视频:线性规划的对偶问题1

教学视频:线性规划的对偶问题2

该工厂每生产一单位产品Ⅰ可获利50元,每生产一单位产品Ⅱ可获利100元,问工厂应分别生产多少产品Ⅰ和产品Ⅱ,才能使工厂获利最多?

此例题与第二章例 1 有相同之处, 只不过把原料 A, B 改成了设备 B, 设备 C, 做这些改动是为了使读者更容易理解.

这个问题的数学模型与第二章的例 1 是一样的, 求解的结果也是一样的.

设 $x_{1}$ 为产品 I 的计划产量, $x_{2}$ 为产品 II 的计划产量, 则有


$$
\max z =50x _ {1} +100x _ {2};
$$


约束条件：


$$
\begin{array}{l}x _ {1} + x _ {2} \leqslant 300,\\2 x _ {1} + x _ {2} \leqslant 400,\\x _ {2} \leqslant 250,\\x _ {1}, x _ {2} \geqslant 0.\\\end{array}
$$


现在我们从另一个角度来考虑这个问题.假如有另外一个工厂要求租用该厂的设备 A, B, C, 那么该厂的厂长应该如何来确定合理的租金呢?

设 $y_{1}, y_{2}, y_{3}$ 分别为设备 A, B, C 的每台时的租金. 为了叙述方便, 这里把租金定义为扣除成本后的利润, 也就是由于出租可以获得的利润. 作为出租者来说, 生产单位产品 I 所需各设备的台时总租金不应当低于原利润, 即 $y_{1} + 2y_{2} \geqslant 50$ , 否则就不出租, 还是用于生产产品 I 以获利 50元; 同样生产一单位产品 II 所需各设备的台时的总租金也不应当低于原利润, 即 $y_{1} + y_{2} + y_{3} \geqslant 100$ , 否则这些设备台时就不出租, 还是用于生产产品 II 以获利 100元。但对于租用者来说, 他要求在满足上述要求的前提下, 也就是在出租者愿意出租的前提下尽量要求全部设备台时的总租金越低越好, 即 $\min 300y_{1} +400y_{2} +250y_{3}$ , 这样我们得到了该问题的数学模型:


$$
\min f =300y _ {1} +400y _ {2} +250y _ {3};
$$


约束条件：


$$
\begin{array}{l}y _ {1} + 2 y _ {2} \geqslant 50,\\y _ {1} + y _ {2} + y _ {3} \geqslant 100,\\y _ {1}, y _ {2}, y _ {3} \geqslant 0.\\\end{array}
$$


这样从两个不同的角度来考虑同一个工厂的最大利润(最小租金)的问题,所建立起来的两个线性规划模型就是一对对偶问题,其中一个叫做原问题,而另外一个就叫对偶问题.

如果我们把求目标函数最大值的线性规划问题当做原问题,则求目标函数最小值的线性规划问题就是对偶问题.下面来研究这两个问题在数学模型上的关系.

(1)求目标函数最大值的线性规划问题中有 n 个变量 m 个约束条件，它的约束条件都是小于等于不等式。而其对偶则是求目标函数为最小值的线性规划问题，有 m 个变量 n 个约束条件，其约束条件都为大于等于不等式。

(2)原问题的目标函数中的变量系数为对偶问题中的约束条件的常数项，并且原问题的目标函数中的第 $i$ 个变量的系数就等于对偶问题中的第 $i$ 个约束条件的常数项.

(3)原问题的约束条件的常数项为对偶问题的目标函数中的变量的系数，并且原问题的第 $i$ 个约束条件的常数项就等于对偶问题的目标函数中的第 $i$ 个变量的系数.

(4)对偶问题的约束条件的系数矩阵 A 是原问题约束条件的系数矩阵的转置 $A^{T}$ . 设


$$
\boldsymbol {A} = \left( \begin{array}{c c c c} a _ {11} & a _ {12} & \dots & a _ {1 n} \\ \vdots & \vdots & & \vdots \\ a _ {m 1} & a _ {m 2} & \dots & a _ {m n} \end{array} \right),
$$


则


$$
\boldsymbol {A} ^ {\mathrm{T}} = \left( \begin{array}{c c c c} a _ {11} & a _ {21} & \dots & a _ {m 1} \\ \vdots & \vdots & & \vdots \\ a _ {1 n} & a _ {2 n} & \dots & a _ {m n} \end{array} \right).
$$


如果我们用矩阵形式来表示,则原问题为


$$
\left\{ \begin{array}{l} \max z = c x, \\ A x \leqslant b, \\ x \geqslant 0. \end{array} \right.
$$


其中 A 是 $m \times n$ 矩阵，该问题有 m 个约束条件 n 个变量， $\boldsymbol{x} = (x_{1}, x_{2}, \cdots, x_{n})^{\mathrm{T}}$ ， $\boldsymbol{b} = (b_{1}, b_{2}, \cdots, b_{m})^{\mathrm{T}}$ ， $\boldsymbol{c} = (c_{1}, c_{2}, \cdots, c_{n})$ .

对偶问题为


$$
\left\{ \begin{array}{l} \min f = \boldsymbol {b} ^ {\mathrm{T}} \cdot \boldsymbol {y}, \\ \boldsymbol {A} ^ {\mathrm{T}} \cdot \boldsymbol {y} \geqslant \boldsymbol {c} ^ {\mathrm{T}}, \\ \boldsymbol {y} \geqslant 0. \end{array} \right.
$$


其中 $A^{T}$ 是 A 的转置, $b^{T}$ 是 b 的转置, $c^{T}$ 是 c 的转置, $y=(y_{1},y_{2},\cdots,y_{m})^{T}$ .

以上问题的原问题我们已在第五章里用单纯形法求出,现在我们用单纯形法求出其对偶问题的解.

加上剩余变量 $s_{1}, s_{2}$ 和人工变量 $a_{1}$ ，把此问题化成标准形式：


$$
\max (- f) = -300y _ {1} -400y _ {2} -250y _ {3} - M a _ {1};
$$


约束条件：


$$
\begin{array}{l}y _ {1} + 2 y _ {2} - s _ {1} + a _ {1} =50,\\y _ {1} + y _ {2} + y _ {3} - s _ {2} =100,\\y _ {1}, y _ {2}, y _ {3}, s _ {1}, s _ {2}, a _ {1} \geqslant 0.\\\end{array}
$$


把上述数据填入单纯形表计算,如表6-14所示.

我们得到最优解 $y_{1}=50, y_{2}=0, y_{3}=50, s_{1}=0, s_{2}=0, a_{1}=0, -f$ 的最大值为 -27500，即目标函数 f 的最小值为 f=27500元.

表6-14

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(y_1\)</span> </td><td> <span class="arithmatex">\(y_2\)</span> </td><td> <span class="arithmatex">\(y_3\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(a_1\)</span> </td><td rowspan="2">b</td><td rowspan="2"></td></tr><tr><td>-300</td><td>-400</td><td>-250</td><td>0</td><td>0</td><td>-M</td></tr><tr><td rowspan="4">1</td><td> <span class="arithmatex">\(a_1\)</span> </td><td>-M</td><td>1</td><td>2</td><td>0</td><td>-1</td><td>0</td><td>1</td><td>50</td><td> <span class="arithmatex">\(\frac{50}{2}\)</span> </td></tr><tr><td> <span class="arithmatex">\(y_3\)</span> </td><td>-250</td><td>1</td><td>1</td><td>1</td><td>0</td><td>-1</td><td>0</td><td>100</td><td> <span class="arithmatex">\(\frac{100}{1}\)</span> </td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>-M-250</td><td>-2M-250</td><td>-250</td><td>M</td><td>250</td><td>-M</td><td rowspan="2" colspan="2">-50M-25000</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j-z_j\)</span> </td><td>M-50</td><td>2M-150</td><td>0</td><td>-M</td><td>-250</td><td>0</td></tr><tr><td rowspan="4">2</td><td> <span class="arithmatex">\(y_2\)</span> </td><td>-400</td><td>1/2</td><td>1</td><td>0</td><td>-1/2</td><td>0</td><td>1/2</td><td>25</td><td> <span class="arithmatex">\(\frac{25}{1/2}\)</span> </td></tr><tr><td> <span class="arithmatex">\(y_3\)</span> </td><td>-250</td><td>1/2</td><td>0</td><td>1</td><td>1/2</td><td>-1</td><td>-1/2</td><td>75</td><td> <span class="arithmatex">\(\frac{75}{1/2}\)</span> </td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>-325</td><td>-400</td><td>-250</td><td>75</td><td>250</td><td>-75</td><td rowspan="2">-28750</td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j-z_j\)</span> </td><td>25</td><td>0</td><td>0</td><td>-75</td><td>-250</td><td>-M+75</td></tr><tr><td rowspan="4">3</td><td> <span class="arithmatex">\(y_1\)</span> </td><td>-300</td><td>1</td><td>2</td><td>0</td><td>-1</td><td>0</td><td>1</td><td>50</td><td></td></tr><tr><td> <span class="arithmatex">\(y_3\)</span> </td><td>-250</td><td>0</td><td>-1</td><td>1</td><td>1</td><td>-1</td><td>-1</td><td>50</td><td></td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>-300</td><td>-350</td><td>-250</td><td>50</td><td>250</td><td>-50</td><td rowspan="2">-27500</td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j-z_j\)</span> </td><td>0</td><td>-50</td><td>0</td><td>-50</td><td>-250</td><td>-M+50</td></tr></table>

从上面可知每台时的租金如下:设备 A 为 50元,设备 B 为 0 元,设备 C 为 50元.这样把工厂的所有设备出租可获得租金 27500元.对出租者来说这些钱不比自己生产所得的利润少,因为满足约束条件;对租用者来说这些租金是出租者愿意出租设备的最小费用,因为这是目标函数的最小值.

通过与原问题的最优解比较,我们发现对偶问题的最优解即最佳租金恰好等于原问题各种设备的对偶价格,这在道理上也能讲得通,各种设备出租的租金应该等于该种设备每台时给工厂所带来的利润,对偶问题的最优值即所有设备总台时数的总租金的最低价正好等于原问题工厂自己安排生产所获得的最大总利润.

以后我们不必解此对偶问题,就可以从原问题的最优单纯形表上得到其对偶问题的最优解,从原问题的资源的对偶价格来得到对偶问题的资源的租金,从原问题的最优目标函数值,即最大利润来得到对偶问题的最优目标函数值,即各种设备总台时数的总租金.反过来也一样,如果我们已求得此对偶问题的最终单纯形表,从表上我们可找到产品Ⅰ的对偶价格为-50元,也就是说当每件产品Ⅰ的利润增加1元,则最低的总租金也就是原问题的总利润将要提高50元,这条信息告诉我们工厂最优生产计划为生产50件产品Ⅰ.同样从对偶问题的最终表可找到产品Ⅱ的对偶价格为-250元,也就是说当每件产品Ⅱ的利润增加1元,则最低总租金即原问题的总利润将要提高250元,这条信息告诉我们工厂最优生产计划为生产250件产品Ⅱ.从对偶问题的最低总租金27 500元可得到原问题工厂的最大利润为27 500元.

这样对于两个有对偶关系的线性规划的问题我们只要求得了其中一个最优解,就可以从这个问题的对偶价格而求得其对偶问题的最优解,知道了其中一个最优值也就找到了其对偶问题的最优值,因为这两个最优值相等.所以以后我们求解一个线性规划问题时,可以把其对偶问题放一起来加以考虑,找一个比较容易求解的来求解,求出了一个问题的最优解同时也就求出了另一个问题的最优解.上述的例题要求租金的合理定价不如我们求解工厂的最大利润,因为求最大利润比较容易,不需要加上人工变量,而求出了最大利润的问题,也就求出了租金合理定价的问题.

前面我们讲了如何写出求最大值(最小值)的线性规划问题的对偶问题,但要求该最大值(最小值)线性规划问题的约束条件都取小于等于号(大于等于号).下面来阐述如何写出任一个线性规划问题的对偶问题.

为了便于阐述,我们不妨以下面的线性规划为例,写出它的对偶问题.


$$
\max z = 3 x _ {1} + 4 x _ {2} + 6 x _ {3};
$$


约束条件：


$$
\begin{array}{l}2 x _ {1} + 3 x _ {2} + 6 x _ {3} \leqslant 440,\\6 x _ {1} - 4 x _ {2} - x _ {3} \geqslant 100,\\5 x _ {1} - 3 x _ {2} + x _ {3} =200,\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


这是一个求最大值的线性规划问题.为了写出它的对偶问题,我们不妨把它的约束条件都变换成取小于等于号的不等式.显然第一个约束条件已符合要求,不要做任何变动,而第二个约束条件,我们只要两边都乘以-1,使不等号方向改变即可,得


$$
- 6 x _ {1} + 4 x _ {2} + x _ {3} \leqslant -100.
$$


这样第二个约束条件也就符合要求了.对于第三个约束条件,我们可以用小于等于和大于等于两个约束条件来替代它,即有


$$
\begin{array}{l} {5 x _ {1} - 3 x _ {2} + x _ {3} \geqslant 200,} \\ {5 x _ {1} - 3 x _ {2} + x _ {3} \leqslant 200.} \end{array}
$$


显然这两个约束条件与原来第三个约束条件是等价的,我们再把其中的


$$
5 x _ {1} - 3 x _ {2} + x _ {3} \geqslant 200
$$


两边都乘以-1,得


$$
- 5 x _ {1} + 3 x _ {2} - x _ {3} \leqslant -200,
$$


通过上面的一些变换,我们得到了一个和原线性规划等价的线性规划问题:


$$
\max z = 3 x _ {1} + 4 x _ {2} + 6 x _ {3};
$$


约束条件：


$$
\begin{array}{l}2 x _ {1} + 3 x _ {2} + 6 x _ {3} \leqslant 440,\\- 6 x _ {1} + 4 x _ {2} + x _ {3} \leqslant -100,\\5 x _ {1} - 3 x _ {2} + x _ {3} \leqslant 200,\\- 5 x _ {1} + 3 x _ {2} - x _ {3} \leqslant -200,\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


这个求最大值的线性规划问题的约束条件都取小于等于号,我们马上可以写出其对偶问题:


$$
\min f =440y _ {1} -100y _ {2} +200y _ {3} ^ {\prime} -200y _ {3} ^ {\prime \prime};
$$


约束条件：


$$
\begin{array}{l}2 y _ {1} - 6 y _ {2} + 5 y _ {3} ^ {\prime} - 5 y _ {3} ^ {\prime \prime} \geqslant 3,\\3 y _ {1} + 4 y _ {2} - 3 y _ {3} ^ {\prime} + 3 y _ {3} ^ {\prime \prime} \geqslant 4,\\6 y _ {1} + y _ {2} + y _ {3} ^ {\prime} - y _ {3} ^ {\prime \prime} \geqslant 6,\\y _ {1}, y _ {2}, y _ {3} ^ {\prime}, y _ {3} ^ {\prime \prime} \geqslant 0.\\\end{array}
$$


这里 $y_{3}^{\prime}, y_{3}^{\prime\prime}$ 和 $y_{1}, y_{2}$ 一样都是不同的决策变量，为了表示这两个决策变量都来源于原问题的第三个约束条件，记为 $y_{3}^{\prime}, y_{3}^{\prime\prime}$ .

因为在该对偶问题中 $y_{3}^{\prime}$ 和 $y_{3}^{\prime\prime}$ 的系数只相差一个符号, 我们可以把上面的对偶问题化为


$$
\min f =440y _ {1} -100y _ {2} +200(y _ {3} ^ {\prime} - y _ {3} ^ {\prime \prime});
$$


约束条件：


$$
\begin{array}{l}2 y _ {1} - 6 y _ {2} + 5 (y _ {3} ^ {\prime} - y _ {3} ^ {\prime \prime}) \geqslant 3,\\3 y _ {1} + 4 y _ {2} + 3 (y _ {3} ^ {\prime} - y _ {3} ^ {\prime \prime}) \geqslant 4,\\6 y _ {1} + y _ {2} + (y _ {3} ^ {\prime} - y _ {3} ^ {\prime \prime}) \geqslant 6,\\y _ {1}, y _ {2}, y _ {3} ^ {\prime}, y _ {3} ^ {\prime \prime} \geqslant 0.\\\end{array}
$$


进一步,我们可以令 $y_{3}=y_{3}^{\prime}-y_{3}^{\prime\prime}$ ，这时当 $y_{3}^{\prime}\geqslant y_{3}^{\prime\prime}$ 时， $y_{3}\geqslant0$ ，当 $y_{3}^{\prime}\leqslant y_{3}^{\prime\prime}$ 时， $y_{3}\leqslant0$ 。这也就是说，尽管 $y_{3}^{\prime},y_{3}^{\prime\prime}\geqslant0$ ，但 $y_{3}$ 的取值可以为正，可以为零，可以为负，即 $y_{3}$ 没有非负限制。

这样我们把原规划的对偶问题化为


$$
\min f =440y _ {1} -100y _ {2} +200y _ {3};
$$


约束条件：


$$
\begin{array}{l}2 y _ {1} - 6 y _ {2} + 5 y _ {3} \geqslant 3,\\3 y _ {1} + 4 y _ {2} + 3 y _ {3} \geqslant 4,\\6 y _ {1} + y _ {2} + y _ {3} \geqslant 6,\\y _ {1}, y _ {2} \geqslant 0, y _ {3} \text {没有非负限制}.\\\end{array}
$$


对照原线性规划问题,我们可以知道当原线性规划问题的第i个约束条件取等号时,则其对偶问题的i个决策变量没有非负限制.如果当原线性规划问题中的第i个决策变量 $x_{i}$ 没有非负限制时,我们也可以用 $x_{i}=x_{i}^{\prime}-x_{i}^{\prime\prime}$ 进行替换,这里 $x_{i}^{\prime}\geqslant0,x_{i}^{\prime\prime}\geqslant0$ ,用类似的方法知道其对偶问题中第i个约束条件取等号,这里不做详细论述了.另外值得一提的是用大于等于零的两个决策变量之差来代替无非负限制的决策变量也是求解含有无非负限制的决策变量的线性规划问题的一种方法.下面我们用一个例子来说明如何写出一个任意线性规划问题的对偶问题.

原线性规划问题为


$$
\min f = 3 x _ {1} + 9 x _ {2} + 4 x _ {3};
$$


约束条件：


$$
\begin{array}{l}x _ {1} + 2 x _ {2} + 3 x _ {3} =180,\\2 x _ {1} - 3 x _ {2} + x _ {3} \leqslant 60,\\5 x _ {1} + 3 x _ {2} \geqslant 240,\\x _ {1} \geqslant 0, x _ {2} \geqslant 0, x _ {3} \text {无非负限制}.\\\end{array}
$$


首先在写对偶问题之前,我们先把第二个约束条件两边乘以-1得


$$
- 2 x _ {1} + 3 x _ {2} - x _ {3} \geqslant -60,
$$


然后按照上面的规则,我们可以得到其对偶问题为


$$
\max z =180y _ {1} -60y _ {2} +240y _ {3};
$$


约束条件：


$$
\begin{array}{l}y _ {1} - 2 y _ {2} + 5 y _ {3} \leqslant 3,\\2 y _ {1} + 3 y _ {2} + 3 y _ {3} \leqslant 9,\\3 y _ {1} - y _ {2} = 4,\\$y_{2}, y_{3} \geqslant 0, y_{1}$ 没有非负限制.\\\end{array}
$$


## 6.3 对偶规划的基本性质

## 一、对称性

即对偶问题的对偶是原问题.

证 设原问题为

约束条件：


$$
\begin{array}{l}\begin{array}{l} \max z = c X; \\ A X \leqslant b, \\ x _ {i} \geqslant 0. \end{array}\tag{1}\\\end{array}
$$


其对偶问题为

约束条件：


$$
\begin{array}{l}\begin{array}{l} \min f = \pmb {b} ^ {\mathrm{T}} \pmb {Y}; \\ \pmb {A} ^ {\mathrm{T}} \pmb {Y} \geqslant \pmb {c} ^ {\mathrm{T}}, \\ y _ {i} \geqslant 0. \end{array}\tag{2}\\\end{array}
$$


我们把上面的对偶问题改写为


$$
\max (- f) = (- \pmb {b} ^ {\mathrm{T}} \pmb {Y});
$$


约束条件：


$$
\begin{array}{l}- \pmb {A} ^ {\mathrm{T}} \pmb {Y} \leqslant - \pmb {c} ^ {\mathrm{T}},\\y _ {i} \geqslant 0.\\\end{array}
$$


这样就可以得到这个问题的对偶：


$$
\min (- z) = \left(- c ^ {\mathrm{T}}\right) X;
$$


约束条件：


$$
\begin{array}{l}- \boldsymbol {A} ^ {\mathrm{T}} \boldsymbol {X} \geqslant - \boldsymbol {b} ^ {\mathrm{T}},\\x _ {i} \geqslant 0.\\\end{array}
$$


则上面的规划可改写为


$$
\max z = \boldsymbol {c} ^ {\mathrm{T}} \boldsymbol {X};
$$


约束条件：


$$
\begin{array}{l}\boldsymbol {A} ^ {\mathrm{T}} \boldsymbol {X} \leqslant \boldsymbol {b} ^ {\mathrm{T}},\\x _ {i} \geqslant 0.\\\end{array}
$$


即为原问题.

## 二、弱对偶性

即对于原问题(1)和对偶问题(2)的可行解 $\hat{X},\hat{Y}$ ，都有 $c\hat{X}\leqslant b^{T}\hat{Y}$ .

证 因为 $\hat{X}$ 是原问题的可行解, 所以有


$$
A   \hat {X} \leqslant b   \text {且}   \hat {x} _ {i} \geqslant 0.
$$


$\hat{\pmb{Y}}^{\mathrm{T}}$ 是对偶问题可行解， $\hat{y}_i\geqslant 0$ ，用 $\hat{\pmb{Y}}^{\mathrm{T}}$ 左乘 $A\hat{X}\leqslant b$ 得


$$
\hat {Y} ^ {\mathrm{T}} A \hat {X} \leqslant \hat {Y} ^ {\mathrm{T}} b.\tag{6.3}
$$


同样 $\hat{Y}$ 为对偶问题可行解,故有


$$
\boldsymbol {A} ^ {\mathrm{T}} \hat {\boldsymbol {Y}} \geqslant \boldsymbol {c} ^ {\mathrm{T}}, \hat {y} _ {i} \geqslant 0.
$$


用 $\hat{X}^{\mathrm{T}}$ 左乘 $A^{\mathrm{T}}\hat{Y}\geqslant c^{\mathrm{T}}$ 得


$$
\hat {X} ^ {\mathrm{T}} A ^ {\mathrm{T}} \hat {Y} \geqslant \hat {X} ^ {\mathrm{T}} c ^ {\mathrm{T}}.
$$


转置得


$$
\hat {Y} ^ {\mathrm{T}} A \hat {X} \geqslant c \hat {X}.\tag{6.4}
$$


从(6.3)式和(6.4)式可得 $\hat{Y}^{T}b\geqslant c\hat{X}.$

由弱对偶性,可得出以下推论:

(1)原问题任一可行解的目标函数值是其对偶问题目标函数值的下界；反之，对偶问题任一可行解的目标函数值是其原问题目标函数值的上界.

(2)如原问题有可行解且目标函数值无界（或具有无界解），则其对偶问题无可行解；反之，对偶问题有可行解且目标函数值无界，则其原问题无可行解（注意：此性质的逆不成立，当对偶问题无可行解时，其原问题或具有无界解或无可行解，反之亦然）.

(3)若原问题有可行解而其对偶问题无可行解，则原问题目标函数值无界；反之，对偶问题有可行解而其原问题无可行解，则对偶问题的目标函数值无界.

## 三、最优性

如果 $\hat{X}$ 是原问题(1)的可行解， $\hat{Y}$ 是对偶问题(2)的可行解，并且


$$
\boldsymbol {c} \hat {\boldsymbol {X}} = \boldsymbol {b} ^ {\mathrm{T}} \hat {\boldsymbol {Y}},
$$


则 $\hat{X}$ 和 $\hat{Y}$ 分别为原问题(1)和对偶问题(2)的最优解.

证 设 $X^{*}, Y^{*}$ 分别为原问题(1)和对偶问题(2)的最优解, 则有


$$
c   \hat {X} \leqslant c X ^ {*}   \text {且}   b ^ {\mathrm{T}} Y ^ {*} \leqslant b ^ {\mathrm{T}}   \hat {Y}.
$$


又因为 $c \hat{X} = b^{T} \hat{Y}$ ，故有


$$
\boldsymbol {c} \hat {\boldsymbol {X}} = \boldsymbol {c} \boldsymbol {X} ^ {*} = \boldsymbol {b} ^ {\mathrm{T}} \boldsymbol {Y} ^ {*} = \boldsymbol {b} ^ {\mathrm{T}} \hat {\boldsymbol {Y}}.
$$


## 四、强对偶性

即若原问题(1)及其对偶问题(2)都有可行解,则两者都有最优解,且它们的最优解的目标函数都相等.

证 由于两者都有可行解,从弱对偶的推论(1)可知,原问题与对偶问题的目标函数分别有上界和下界,所以两者都有最优解;同时我们又知道原问题的对偶价格即为对偶问题的一个可行解,并知这个可行解的目标函数值即为原问题的目标函数值,从最优性即可知这个目标函数即为原问题和对偶问题的目标函数值.

## 五、互补松弛性

在线性规划问题的最优解中,如果对应某一约束条件的对偶变量值为非零,则该约束条件取严格等式;反之,如果约束条件取严格不等式,则其对应的对偶变量一定为零,也即

若 $y_{i}^{*} > 0$ ，则有 $\sum_{j=1}^{n} a_{ij} x_{j}^{*} = b_{i}$

若 $\sum_{j=1}^{n} a_{ij} x_j^* < b_i$ ，则有 $y_i^* = 0$ .

证 从弱对偶性知 $c\hat{X}\leqslant \hat{Y}^{\mathrm{T}}A\hat{X}\leqslant \hat{Y}^{\mathrm{T}}b.$

因为 $X^{*}, Y^{*}$ 分别为原问题(1)及其对偶问题(2)的最优解, 又从最优性 $cX^{*} = Y^{*T}b$ 知 $Y^{*T}AX^{*} = Y^{*T}b$ , 即得


$$
\boldsymbol {Y} ^ {* \mathrm{T}} (\boldsymbol {A X} ^ {*} - \boldsymbol {b}) = 0.
$$


由于 $Y^{*\mathrm{T}} \geqslant 0, AX^{*} - b \leqslant 0$ ，由矩阵乘法可知，行向量 $Y^{*\mathrm{T}}$ 乘以列向量 $AX^{*} - b$ 时，要使乘积为零向量，则 $Y^{*}$ 的第 $i$ 个分量 $y_{i}^{*} > 0$ （不为零）时， $AX^{*} - b$ 的第 $i$ 个分量 $\sum_{j=1}^{n} a_{ij} x_{j}^{*} - b_{i}$ 必为零，即 $\sum_{j=1}^{n} a_{ij} x_{j}^{*} - b_{i} = 0.$ 同样，当 $\sum_{j=1}^{n} a_{ij} x_{j}^{*} - b_{i} < 0$ （不为零）时， $y_{i}^{*} = 0.$

## 6.4 对偶单纯形法

对偶单纯形法和单纯形法一样都是求解原线性规划问题的一种方法. 单纯形法是在保持原问题的所有约束条件的常数大于等于零的情况下, 通过迭代, 使得所有的检验数都小于等于零, 最后求得最优解; 而对偶单纯形法则是在保持原问题的所有检验数都小于等于零的情况下, 通过迭代, 使得所有约束条件的常数项都大于等于零, 最后求得最优解.

使用对偶单纯形法时,初始解可以是非可行解,对于一些大于等于号的约束不等式不需要添加人工变量,只要把该不等式两边乘以-1,化成小于等于不等式的约束,就可用对偶单纯形法来求解,简化计算。这是对偶单纯形的优点,但是对偶单纯形法在使用上有很大的局限性,这主要是对大多数线性规划问题,很难找到一个初始解使得其所有检验数都小于等于零,因而这种方法在求解线性规划问题时很少单独应用.但在灵敏度分析中,有时需要用对偶单纯形法,这样可使问题处理简化.

下面就第二章例 1 为例说明在灵敏度分析时如何使用对偶单纯形法以及对偶单纯形法的求解过程.

在上节对 $b$ 的灵敏度分析中已知当 $250\leqslant b_{1}^{\prime} \leqslant 325$ 时第一个约束条件的对偶价格不变，现在如果 $b_{1} =300$ 变成 $b_{1}^{\prime} =350$ 了，请问这时第一个约束方程的对偶价格应为多少呢？对这个问题我们用对偶单纯形法进行求解.

先求出在第2次迭代表上的常数列


$$
\begin{array}{r l} \boldsymbol {x} _ {B} ^ {\prime} & = \boldsymbol {x} _ {B} + \boldsymbol {B} ^ {- 1} \Delta \boldsymbol {b} = \left( \begin{array}{c}50\\50\\250\end{array} \right) + \left( \begin{array}{c} 1 \cdot \Delta b _ {1} \\ - 2 \cdot \Delta b _ {1} \\ 0 \cdot \Delta b _ {1} \end{array} \right) \\ & = \left( \begin{array}{c}50\\50\\250\end{array} \right) + \left( \begin{array}{c} 1 \times 50\\ - 2 \times 50\\ 0 \times 50\end{array} \right) = \left( \begin{array}{c}50\\50\\250\end{array} \right) + \left( \begin{array}{c}50\\ -100\\ 0 \end{array} \right) = \left( \begin{array}{c}100\\ -50\\250\end{array} \right). \end{array}
$$


代入第 2 次迭代表, 如表 6-15所示.

从表 6-15可知 $b_{2} = -50$ . 如果要按单纯形法解此题, 则第一是把此约束方程乘以 -1, 把 $b_{2}$ 化成 50, 第二再加上人工变量 $a_{1}$ , 第三在目标函数上加上罚因子 $-M \cdot a_{1}$ , 然后再用单纯形法计算, 这是很麻烦的. 现在由于在此单纯形表上检验数都小于等于零, 所以我们可以用对偶单纯形法

来做.

（1）确定出基变量，在常数项列中找到一个最小的负常量，则这个负常量所在行的基变量为出基变量，在此例中 $b_{2} = -50$ 是最小的负常数，所以 $s_{2}$ 就确定为出基变量.

表6-15

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td rowspan="2">b</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="5">2</td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>1</td><td>0</td><td>-1</td><td>100</td></tr><tr><td> <span class="arithmatex">\(s_2\)</span> </td><td>0</td><td>0</td><td>0</td><td>-2</td><td>1</td><td>1</td><td>-50</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>250</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>50</td><td>0</td><td>50</td><td rowspan="2"></td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>0</td><td>0</td><td>-50</td><td>0</td><td>-50</td></tr></table>

（2）确定入基变量，在单纯形表中检查出基变量 $x_{k}$ 所在行的各系数 $a_{kj}$（$j=1,2,\cdots,n$），如果所有的 $a_{kj}$ 都大于等于零，则无可行解，停止计算，若存在 $a_{kj}$ 为负数，则计算所有为负数的 $a_{kj}$ 与其对应的 $\sigma_{j}$ 的比值 $\frac{\sigma_{j}}{a_{kj}}$ ，求出其中的最小值，即


$$
\min _ {j} \left\{\frac {\sigma_ {j}}{a _ {k j}} \mid a _ {k j} <   0 \right\}.
$$


确定具有最小比值 $\frac{\sigma_j}{a_{kj}}$ 的 $x_{t}$ 为入基变量，在本例中第二行系数里只有 $a_{23} = -2 < 0$ ，故取 $s_1$ 为入基变量，这样做可保证所有 $\sigma_{j}$ 仍有 $\sigma_{j} \leqslant 0$ .

（3）以 $a_{kt}$ 为主元，按原单纯形法在表中进行迭代运算，得到新的单纯形表，对本例以 $a_{23}$ 为主元，得新的单纯形表，如表 6-16所示.

表6-16

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td rowspan="2">b</td></tr><tr><td>50</td><td>100</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="5"></td><td> <span class="arithmatex">\(x_1\)</span> </td><td>50</td><td>1</td><td>0</td><td>0</td><td>1/2</td><td>-1/2</td><td>75</td></tr><tr><td> <span class="arithmatex">\(s_1\)</span> </td><td>0</td><td>0</td><td>0</td><td>1</td><td>-1/2</td><td>-1/2</td><td>25</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>100</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>250</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>50</td><td>100</td><td>0</td><td>25</td><td>75</td><td rowspan="2">28750</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>0</td><td>0</td><td>0</td><td>-25</td><td>-75</td></tr></table>

表 6-16是先把第 2 行除以 -2，使得 $a_{23}$ 变成 1，同时也使得 $b_{2}$ 大于等于零，为 25，再进行初

等行变换使 $a_{13}$ 和 $a_{33}$ 变成零.

（4）检查常数列的值，若都已经非负，那么此解就是最优解了。如果还存在负的常数，请重复（1）至（4）的步骤。在此例中常数列的值都已经非负，所以此时的解 $x_{1} =75, x_{2} =250, s_{1} =25, s_{2} = 0$ ， $s_{3} = 0$ 为最优解，此时第一约束条件即设备台时的对偶价格为零，起了变化。

## 习题

1. 考虑下列线性规划：


$$
\max z =20x _ {1} + 8 x _ {2} + 6 x _ {3};
$$


约束条件：


$$
\begin{array}{l}8 x _ {1} + 3 x _ {2} + 2 x _ {3} \leqslant 250,\\2 x _ {1} + x _ {2} \leqslant 50,\\4 x _ {1} + 3 x _ {3} \leqslant 150,\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


此线性规划的最终单纯形表如表 6-17所示.

表6-17

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(x_3\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td> <span class="arithmatex">\(s_3\)</span> </td><td rowspan="2">b</td></tr><tr><td>20</td><td>8</td><td>6</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="5">4</td><td> <span class="arithmatex">\(s_1\)</span> </td><td>0</td><td> <span class="arithmatex">\(-\frac{2}{3}\)</span> </td><td>0</td><td>0</td><td>1</td><td>-3</td><td> <span class="arithmatex">\(-\frac{2}{3}\)</span> </td><td>0</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td>8</td><td>2</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>50</td></tr><tr><td> <span class="arithmatex">\(x_3\)</span> </td><td>6</td><td> <span class="arithmatex">\(\frac{4}{3}\)</span> </td><td>0</td><td>1</td><td>0</td><td>0</td><td> <span class="arithmatex">\(\frac{1}{3}\)</span> </td><td>50</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>24</td><td>8</td><td>6</td><td>0</td><td>8</td><td>2</td><td>700</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j-z_j\)</span> </td><td>-4</td><td>0</td><td>0</td><td>0</td><td>-8</td><td>-2</td><td></td></tr></table>

（1） 计算使最优解不变的 $c_{1}$ 的变化范围.

（2） 计算使最优解不变的 $c_{2}$ 的变化范围.

（3） 计算使最优解不变的 $c_{s_{2}}$ 的变化范围.

2. 对第五章习题 13(2) 最终单纯形表中的目标函数系数进行灵敏度分析.

（1） 计算使得最优解不变的 $c_{1}$ 的变化范围.

（2） 计算使得最优解不变的 $c_{3}$ 的变化范围.

（3） 计算使得最优解不变的 $c_{2}$ 的变化范围.

3. 见本章习题 1 的线性规划及其最终单纯形表.

（1） 求出 $b_{1}$ 的变化范围, 在此范围内其对偶价格不变.

（2） 求出 $b_{2}$ 的变化范围, 在此范围内其对偶价格不变.

（3） 求出 $b_{3}$ 的变化范围, 在此范围内其对偶价格不变.

4. 对第五章习题 13(2) 最终单纯形表的约束方程的常数项进行灵敏度分析.

（1） 求出 $b_{1}$ 的变化范围, 在此范围内其最优基不变, 且所得的解仍然是可行的.

（2） 求出 $b_{2}$ 的变化范围, 在此范围内其最优基不变, 且所得的解仍然是可行的.

（3） 求出 $b_{3}$ 的变化范围, 在此范围内其最优基不变, 且所得的解仍然是可行的.

5. 已知线性规划问题：


$$
\min f = 5 x _ {1} - 5 x _ {2} -13x _ {3};
$$


约束条件：


$$
\begin{array}{l}- x _ {1} + x _ {2} + 3 x _ {3} \leqslant 20,\\12x _ {1} + 4 x _ {2} +10x _ {3} \leqslant 100,\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


将问题化为标准型之后求解,最优值为-100,最终单纯形表如表6-18所示.

表6-18

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(x_3\)</span> </td><td> <span class="arithmatex">\(x_4\)</span> </td><td> <span class="arithmatex">\(x_5\)</span> </td><td rowspan="2">b</td></tr><tr><td>-5</td><td>5</td><td>13</td><td>0</td><td>0</td></tr><tr><td rowspan="3">2</td><td> <span class="arithmatex">\(x_2\)</span> </td><td>5</td><td>-1</td><td>1</td><td>3</td><td>1</td><td>0</td><td>20</td></tr><tr><td> <span class="arithmatex">\(x_5\)</span> </td><td>0</td><td>16</td><td>0</td><td>-2</td><td>-4</td><td>1</td><td>20</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>0</td><td>0</td><td>-2</td><td>-5</td><td>0</td><td></td></tr></table>

（1） 写出其最优基矩阵 B 及其逆矩阵 $B^{-1}$ ;

（2） 当 $b_{2}$ 由 100变为 60时, 最优解有什么变化?

（3） $x_{1}$ 的系数列向量由 $\begin{pmatrix}-1\\12\end{pmatrix}$ 变为 $\begin{pmatrix}0\\5\end{pmatrix}$ 的时候,最优解有什么变化?

（4）增加一个约束条件 $x_{1} + 2x_{2} + x_{3}\leqslant 30$ ，最优解有什么变化？

6. 已知线性规划问题：


$$
\max z = 4 x _ {1} + 3 x _ {2} + 2 x _ {3}
$$


约束条件：


$$
\begin{array}{l}4 x _ {1} + x _ {2} + x _ {3} \leqslant 15\\6 x _ {1} + 4 x _ {2} + 3 x _ {3} \leqslant 42\\x _ {1}, x _ {2}, x _ {3} \geqslant 0\\\end{array}
$$


最优单纯形表如表 6-19所示.

表6-19

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_{B}\)</span> </td><td> <span class="arithmatex">\(x_{1}\)</span> </td><td> <span class="arithmatex">\(x_{2}\)</span> </td><td> <span class="arithmatex">\(x_{3}\)</span> </td><td> <span class="arithmatex">\(s_{1}\)</span> </td><td> <span class="arithmatex">\(s_{2}\)</span> </td><td rowspan="2">b</td></tr><tr><td>4</td><td>3</td><td>2</td><td>0</td><td>0</td></tr><tr><td rowspan="4">3</td><td> <span class="arithmatex">\(s_{1}\)</span> </td><td>0</td><td>2.5</td><td>0</td><td>0.25</td><td>1</td><td>-0.25</td><td>4.5</td></tr><tr><td> <span class="arithmatex">\(x_{2}\)</span> </td><td>3</td><td>1.5</td><td>1</td><td>0.75</td><td>0</td><td>0.25</td><td>10.5</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_{j}\)</span> </td><td>4.5</td><td>3</td><td>2.25</td><td>0</td><td>0.75</td><td>31.5</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_{j}-z_{j}\)</span> </td><td>-0.5</td><td>0</td><td>-0.25</td><td>0</td><td>-0.75</td><td></td></tr></table>

其中， $s_{1}, s_{2}$ 分别为第 1, 2 约束方程中的松弛变量.

（1） 请求出最优基不变的 $b_{1}, b_{2}$ 的变化范围；

（2） 请求出最优解不变的 $c_{1}, c_{2}, c_{3}$ 的变化范围；

（3）在原线性规划约束条件的基础上，增加下面的约束条件：


$$
x _ {1} + 2 x _ {2} + x _ {3} \leqslant 12
$$


其最优解是否变化,如变化,请求出最优解.

7. 某公司制造三种产品 A, B, C, 需要两种资源（劳动力和原材料），要求确定总利润最大的最优生产计划。该问题的线性规划模型如下：


$$
\max z = 3 x _ {1} + x _ {2} + 5 x _ {3};
$$


约束条件：


$$
\begin{array}{l}6 x _ {1} + 3 x _ {2} + 5 x _ {3} \leqslant 45(\text {劳动力}),\\3 x _ {1} + 4 x _ {2} + 5 x _ {3} \leqslant 30(\text { 原材料 }),\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


其中 $x_{1}, x_{2}, x_{3}$ 是产品A,B,C的产量.

这个线性规划问题的最终单纯形表如表 6-20所示.

表6-20

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(x_3\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td rowspan="2">b</td></tr><tr><td>3</td><td>1</td><td>5</td><td>0</td><td>0</td></tr><tr><td rowspan="4"></td><td> <span class="arithmatex">\(s_1\)</span> </td><td>0</td><td>3</td><td>-1</td><td>0</td><td>1</td><td>-1</td><td>15</td></tr><tr><td> <span class="arithmatex">\(x_3\)</span> </td><td>5</td><td> <span class="arithmatex">\(\frac{3}{5}\)</span> </td><td> <span class="arithmatex">\(\frac{4}{5}\)</span> </td><td>1</td><td>0</td><td> <span class="arithmatex">\(\frac{1}{5}\)</span> </td><td>6</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>3</td><td>4</td><td>5</td><td>0</td><td>1</td><td>30</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>0</td><td>-3</td><td>0</td><td>0</td><td>-1</td><td></td></tr></table>

(1)求出使得最优解不变的产品A的单位利润变动范围.问 $c_{1} = 2$ 时最优解变不变？

(2) 假定能以 10元的代价增加 15个单位的材料, 这样做是否有利?

(3) 求出使劳动力对偶价格不变的 $b_{1}$ 的变化范围.

(4)由于技术上的突破，每单位产品 B 原材料的需要量减少为 2 单位，这时是否需要改变生产计划？为什么？

(5)假如这时，又试制成新产品 D，生产一个单位新产品 D 需要劳动力 4 单位，原材料 3 单位，而每单位的新产品 D 的利润为 3 元。请问这时生产计划是否要进行修改？为什么？怎样修改？

8. 某食品厂能够生产 3 种食品, 生产食品 A, B, C 每吨产品利润分别为 2.5万元, 2 万元, 3 万元. 各食品需要经过 3 道工序进行加工完成, 各种食品生产 1 吨所需工时数及各工序可用总工时数如表 6-21所示.

表6-21

<table><tr><td>项目</td><td>A食品</td><td>B食品</td><td>C食品</td><td>总工时数</td></tr><tr><td>工序1</td><td>8</td><td>16</td><td>10</td><td>350</td></tr><tr><td>工序2</td><td>10</td><td>5</td><td>5</td><td>450</td></tr><tr><td>工序3</td><td>2</td><td>13</td><td>5</td><td>400</td></tr></table>

(1) 如何充分利用资源,使得厂家获利最大?

(2)为了增加产量，厂家通过各种手段扩大工时数，若工序1每增加10工时数，需要消耗成本10万元，请问这样做是否合算？

(3)若对食品 B 的加工工序进行了改良，生产每吨 B 三种工序用时分别减少了 2 工时、1 工时、2 工时，请问这时最优生产计划是否改变？

(4)现有甲和乙两种新产品，生产每吨产品分别获利3.2万元和3万元。甲产品每道工序所需工时分别为4,8,10。乙产品每道工序所需工时分别为5,8,9。总工时不变的情况下，在生产A,B,C产品时可考虑再增加一种产品投产，请问投产哪种新产品更合算？

9. 请对第三章习题6,7,8,9,10的“管理运筹学”软件的输出信息进行判断.哪些最优解是唯一的最优解？哪些最优解有无穷多组最优解？为什么？

10.写出下列线性规划的对偶问题：

(1)


$$
\max z = 2 x _ {1} + x _ {2} + x _ {3};
$$


约束条件：


$$
\begin{array}{l}x _ {1} + x _ {2} + x _ {3} \leqslant 10,\\x _ {1} + 5 x _ {2} + x _ {3} \leqslant 20,\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


(2)


$$
\min f = 4 x _ {1} + 4 x _ {2} + 2 x _ {3};
$$


约束条件：


$$
\begin{array}{l}\frac {1}{2} x _ {1} + 2 x _ {2} + 2 x _ {3} \geqslant 100,\\4 x _ {1} + 6 x _ {2} + 3 x _ {3} \geqslant 200,\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


11.写出下列线性规划的对偶问题：

(1)


$$
\max z = x _ {1} + 2 x _ {2} + 5 x _ {3};
$$


约束条件：


$$
\begin{array}{l}2 x _ {1} + 3 x _ {2} + x _ {3} \geqslant 10,\\3 x _ {1} + x _ {2} + x _ {3} \leqslant 50,\\x _ {1} + x _ {3} =20,\\x _ {1} \geqslant 0, x _ {2} \geqslant 0, x _ {3} \text {无非负限制}.\\\end{array}
$$


(2)


$$
\min f = x _ {1} + 3 x _ {2} + 2 x _ {3};
$$


约束条件：


$$
\begin{array}{l}x _ {1} + 2 x _ {2} + 3 x _ {3} \geqslant 6,\\x _ {1} - x _ {2} + 2 x _ {3} \leqslant 3,\\- x _ {1} + x _ {2} + x _ {3} = 2,\\x _ {1} \geqslant 0, x _ {2} \text {无非负限制}, x _ {3} \leqslant 0.\\\end{array}
$$


(提示:可以设 $x_{3}^{\prime}=-x_{3}$ 替代 $x_{3}$ ，这时就有 $x_{3}^{\prime}\geqslant0.$ )

12.已知线性规划问题：


$$
\min f = x _ {1} + x _ {2} + x _ {3} + x _ {4} + x _ {5};
$$


约束条件：


$$
\begin{array}{l}x _ {1} + x _ {2} \geqslant 6,\\x _ {2} + x _ {3} \geqslant 7,\\x _ {3} + x _ {4} \geqslant 8,\\x _ {4} + x _ {5} \geqslant 9,\\x _ {1} + x _ {5} \geqslant 10,\\x _ {1}, x _ {2}, x _ {3}, x _ {4}, x _ {5} \geqslant 0.\\\end{array}
$$


(1) 写出该问题的对偶问题；

(2)利用“管理运筹学”软件分别求解原问题和对偶问题；

(3)若是选用单纯形法求解，两个问题选用哪一个求解目标函数最优值更简单？为什么？

13.已知表 6-22为求解线性规划问题的最终单纯形表, 表中 $s_1, s_2$ 为松弛变量, 问题的约束为 $\leqslant$ 形式.

表6-22

<table><tr><td rowspan="2">迭代次数</td><td rowspan="2">基变量</td><td rowspan="2"> <span class="arithmatex">\(c_B\)</span> </td><td> <span class="arithmatex">\(x_1\)</span> </td><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(x_3\)</span> </td><td> <span class="arithmatex">\(s_1\)</span> </td><td> <span class="arithmatex">\(s_2\)</span> </td><td rowspan="2">b</td></tr><tr><td> <span class="arithmatex">\(c_1\)</span> </td><td> <span class="arithmatex">\(c_2\)</span> </td><td> <span class="arithmatex">\(c_3\)</span> </td><td>0</td><td>0</td></tr><tr><td rowspan="4">3</td><td> <span class="arithmatex">\(x_3\)</span> </td><td> <span class="arithmatex">\(c_3\)</span> </td><td>1</td><td>0</td><td>1</td><td> <span class="arithmatex">\(\frac{1}{2}\)</span> </td><td> <span class="arithmatex">\(-\frac{1}{2}\)</span> </td><td>5</td></tr><tr><td> <span class="arithmatex">\(x_2\)</span> </td><td> <span class="arithmatex">\(c_2\)</span> </td><td>2</td><td>1</td><td>0</td><td> <span class="arithmatex">\(\frac{1}{2}\)</span> </td><td> <span class="arithmatex">\(\frac{1}{2}\)</span> </td><td>25</td></tr><tr><td colspan="2"> <span class="arithmatex">\(z_j\)</span> </td><td>3</td><td>2</td><td>-1</td><td> <span class="arithmatex">\(\frac{1}{2}\)</span> </td><td> <span class="arithmatex">\(\frac{3}{2}\)</span> </td><td>45</td></tr><tr><td colspan="2"> <span class="arithmatex">\(c_j - z_j\)</span> </td><td>-1</td><td>0</td><td>0</td><td> <span class="arithmatex">\(-\frac{1}{2}\)</span> </td><td> <span class="arithmatex">\(-\frac{3}{2}\)</span> </td><td></td></tr></table>

（1） 写出原线性规划问题；

（2） 写出原问题的对偶问题；

（3） 直接由表 6-22写出对偶问题的最优解.

14.写出以下线性规划问题的对偶问题,考虑用哪一种形式求解相应线性规划问题更简单,并选择合适方法进行求解:

(1)


$$
\min f = 2 x _ {1} + 3 x _ {2} + 5 x _ {3};
$$


约束条件：


$$
\begin{array}{l}3 x _ {1} + 2 x _ {2} + x _ {3} \geqslant 4,\\x _ {1} + 3 x _ {2} + x _ {3} \geqslant 12,\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


(2)


$$
\min f = 2 x _ {1} - 2 x _ {2} +10x _ {3};
$$


约束条件：


$$
\begin{array}{l}2 x _ {1} + 3 x _ {2} + 5 x _ {3} \geqslant 2,\\- 3 x _ {1} - x _ {2} + x _ {3} \geqslant 3,\\x _ {1} + 4 x _ {2} + x _ {3} \geqslant 5,\\\end{array}
$$


15.判断下列说法是否正确？为什么？

（1）原问题存在可行解，则其对偶问题也一定存在可行解；

(2) 原问题解为无界, 则其对偶问题无可行解;

（3）对偶问题无可行解，则原问题也一定无可行解；

(4) 若原问题和对偶问题都存在可行解, 则该线性规划问题一定存在最优解.

16.用单纯形法求解下列线性规划问题：


$$
\min f = x _ {1} + 2 x _ {2} + 3 x _ {3};
$$


约束条件：


$$
\begin{array}{l}x _ {1} - x _ {2} + x _ {3} \geqslant 4,\\x _ {1} + x _ {2} + 2 x _ {3} \leqslant 8,\\x _ {2} - x _ {3} \geqslant 2,\\x _ {1}, x _ {2}, x _ {3} \geqslant 0.\\\end{array}
$$


17.已知线性规划问题：


$$
\max z = x _ {1} + 2 x _ {2};
$$


约束条件：


$$
\begin{array}{l}x _ {1} \leqslant 5 + t,\\x _ {1} + x _ {2} \leqslant 10- t,\\x _ {2} \leqslant 3 + t,\\x _ {1}, x _ {2} \geqslant 0.\\\end{array}
$$


其中 $0 \leqslant t \leqslant 10$ ，试分析随着 t 的变化，最优解的变化情况。

18.已知线性规划问题：


$$
\max z = (5 + 3 t) x _ {1} + (12+ 2 t) x _ {2} + (10- t) x _ {3}
$$


约束条件：


$$
\begin{array}{l}x _ {1} + x _ {2} + x _ {3} \leqslant 30\\2 x _ {1} + 2 x _ {2} + x _ {3} \leqslant 40\\x _ {1}, x _ {2}, x _ {3} \geqslant 0\\\end{array}
$$


其中， $t \geqslant 0$ ，试分析随着 t 的变化，最优解的变化情况。

19.已知线性规划问题：


$$
\max z = 2 x _ {1} - 3 x _ {2} + x _ {3}
$$


约束条件：


$$
\begin{array}{l}- 2 x _ {1} + x _ {2} + 2 x _ {3} \leqslant 5\\- x _ {1} + 4 x _ {2} - x _ {3} \leqslant 1\\2 x _ {1} + 5 x _ {2} - 2 x _ {3} \leqslant 3\\x _ {1}, x _ {2}, x _ {3} \geqslant 0\\\end{array}
$$


试用对偶理论证明上述线性规划问题无最优解.

20.设有线性规划如下：


$$
\max z = 3 x _ {1} + 2 x _ {2} + x _ {3} + 4 x _ {4}
$$


约束条件：


$$
\begin{array}{l}x _ {1} + 3 x _ {2} + x _ {4} \leqslant 10\\2 x _ {1} + x _ {2} + x _ {3} \leqslant 8\\3 x _ {2} + 2 x _ {3} + x _ {4} = 8\\4 x _ {1} + x _ {2} + x _ {3} \leqslant 12\\x _ {1}, x _ {2}, x _ {3} \geqslant 0, x _ {4} \text {无约束}\\\end{array}
$$


(1) 写出该问题的对偶问题；

(2) 已知原问题最优解为 $X^{*} = (2,0,0,8)^{\mathrm{T}}$ ，试根据对偶理论，直接求出对偶问题的最优解.

21.已知线性规划问题：


$$
\max z = 2 x _ {1} + 2 x _ {2} + x _ {3} + x _ {4};
$$


约束条件：


$$
\begin{array}{l}x _ {1} + 2 x _ {2} + 3 x _ {3} + 4 x _ {4} \leqslant 20,\\4 x _ {1} + 3 x _ {2} + 2 x _ {3} + x _ {4} \leqslant 20,\\x _ {1}, x _ {2}, x _ {3}, x _ {4} \geqslant 0.\\\end{array}
$$


其对偶问题的最优解为 $y_{1} = \frac{1}{10}, y_{2} = \frac{3}{5}$ ，目标函数最小值为 14.试用互补松弛定理求解原问题的最优解.

---
