# 第16章 强化学习

## 16.1 任务与奖赏

我们考虑一下如何种西瓜. 种瓜有许多步骤, 从一开始的选种, 到定期浇水、施肥、除草、杀虫, 经过一段时间才能收获西瓜. 通常要等到收获后, 我们才知道种出的瓜好不好. 若将得到好瓜作为辛勤种瓜劳动的奖赏，则在种瓜过程中当我们执行某个操作(例如，施肥)时，并不能立即获得这个最终奖赏，甚至难以判断当前操作对最终奖赏的影响，仅能得到一个当前反馈(例如，瓜苗看起来更健壮了). 我们需多次种瓜, 在种瓜过程中不断摸索, 然后才能总结出较好的种瓜策略. 这个过程抽象出来, 就是 “强化学习” (reinforcement learning).

![370_1049_1020_521_184_0.jpg](../../images/370_1049_1020_521_184_0.jpg)

图 16.1 强化学习图示

图 16.1 给出了强化学习的一个简单图示. 强化学习任务通常用马尔可夫决策过程 (Markov Decision Process,简称 MDP)来描述: 机器处于环境 $E$ 中,状态空间为 $X$ ,其中每个状态 $x \in  X$ 是机器感知到的环境的描述,如在种瓜任务上这就是当前瓜苗长势的描述; 机器能采取的动作构成了动作空间 $A$ ,如种瓜过程中有浇水、施不同的肥、使用不同的农药等多种可供选择的动作; 若某个动作 $a \in  A$ 作用在当前状态 $x$ 上,则潜在的转移函数 $P$ 将使得环境从当前状态按某种概率转移到另一个状态, 如瓜苗状态为缺水, 若选择动作浇水, 则瓜苗长势会发生变化, 瓜苗有一定的概率恢复健康, 也有一定的概率无法恢复; 在转移到另一个状态的同时,环境会根据潜在的 “奖赏” (reward) 函数 $R$ 反馈给机器一个奖赏,如保持瓜苗健康对应奖赏 +1 ,瓜苗凋零对应奖赏-10,最终种出了好瓜对应奖赏 +100 . 综合起来,强化学习任务对应了四元组 $E = \langle X, A, P, R\rangle$ , 其中 $P : X \times  A \times  X \mapsto  \mathbb{R}$ 指定了状态转移概率, $R : X \times  A \times  X \mapsto  \mathbb{R}$ 指定了奖赏；在有的应用中，奖赏函数可能仅与状态转移有关，即 $R : X \times  X \mapsto  \mathbb{R}$ .

图 16.2 给出了一个简单例子: 给西瓜浇水的马尔可夫决策过程. 该任务中只有四个状态(健康、缺水、溢水、凋亡)和两个动作(浇水、不浇水)，在每一步转移后, 若状态是保持瓜苗健康则获得奖赏 1 , 瓜苗缺水或溢水奖赏为 -1 , 这时通过浇水或不浇水可以恢复健康状态, 当瓜苗凋亡时奖赏是最小值 -100 且无法恢复. 图中箭头表示状态转移，箭头旁的 $a, p, r$ 分别表示导致状态转移的动作、转移概率以及返回的奖赏. 容易看出, 最优策略在 “健康” 状态选择动作 “浇水”、在 “溢水” 状态选择动作 “不浇水”、在 “缺水” 状态选择动作 “浇水”、在 “凋亡” 状态可选择任意动作.

---

亦称 “再励学习”.

---

![371_784_123_972_648_0.jpg](../../images/371_784_123_972_648_0.jpg)

图 16.2 给西瓜浇水问题的马尔可夫决策过程

需注意 “机器” 与 “环境” 的界限，例如在种西瓜任务中，环境是西瓜生长的自然世界; 在下棋对弈中, 环境是棋盘与对手; 在机器人控制中, 环境是机器人的躯体与物理世界. 总之, 在环境中状态的转移、奖赏的返回是不受机器控制的, 机器只能通过选择要执行的动作来影响环境, 也只能通过观察转移后的状态和返回的奖赏来感知环境.

机器要做的是通过在环境中不断地尝试而学得一个 “策略” (policy) $\pi$ ,根据这个策略,在状态 $x$ 下就能得知要执行的动作 $a = \pi \left( x\right)$ ,例如看到瓜苗状态是缺水时，能返回动作 “浇水”. 策略有两种表示方法:一种是将策略表示为函数 $\pi  : X \mapsto  A$ ,确定性策略常用这种表示; 另一种是概率表示 $\pi  : X \times  A \mapsto  \mathbb{R}$ , 随机性策略常用这种表示, $\pi \left( {x, a}\right)$ 为状态 $x$ 下选择动作 $a$ 的概率,这里必须有 $\mathop{\sum }\limits_{a}\pi \left( {x, a}\right)  = 1.$

策略的优劣取决于长期执行这一策略后得到的累积奖赏，例如某个策略使得瓜苗枯死，它的累积奖赏会很小，另一个策略种出了好瓜，它的累积奖赏会很大. 在强化学习任务中, 学习的目的就是要找到能使长期累积奖赏最大化的策略. 长期累积奖赏有多种计算方式,常用的有 “ $T$ 步累积奖赏” $\mathbb{E}\left\lbrack  {\frac{1}{T}\mathop{\sum }\limits_{{t = 1}}^{T}{r}_{t}}\right\rbrack$ 和 “ $\gamma$ 折扣累积奖赏” $\mathbb{E}\left\lbrack  {\mathop{\sum }\limits_{{t = 0}}^{{+\infty }}{\gamma }^{t}{r}_{t + 1}}\right\rbrack$ ,其中 ${r}_{t}$ 表示第 $t$ 步获得的奖赏值, $\mathbb{E}$ 表示对所有随机变量求期望.

读者也许已经感觉到强化学习与监督学习的差别. 若将这里的 “状态” 对应为监督学习中的 “示例”、 “动作” 对应为 “标记”，则可看出，强化学习中的 “策略” 实际上就相当于监督学习中的 “分类器” (当动作是离散的)或 “回归器” (当动作是连续的), 模型的形式并无差别. 但不同的是, 在强化学习中并没有监督学习中的有标记样本(即 “示例-标记” 对), 换言之, 没有人直接告诉机器在什么状态下应该做什么动作, 只有等到最终结果揭晓, 才能通过 “反思” 之前的动作是否正确来进行学习. 因此, 强化学习在某种意义上可看作具有“延迟标记信息”的监督学习问题.

## 16.2 K-摇臂赌博机

### 16.2.1 探索与利用

与一般监督学习不同，强化学习任务的最终奖赏是在多步动作之后才能观察到, 这里我们不妨先考虑比较简单的情形: 最大化单步奖赏, 即仅考虑一步操作. 需注意的是，即便在这样的简化情形下，强化学习仍与监督学习有显著不同, 因为机器需通过尝试来发现各个动作产生的结果, 而没有训练数据告诉机器应当做哪个动作.

欲最大化单步奖赏需考虑两个方面:一是需知道每个动作带来的奖赏，二是要执行奖赏最大的动作. 若每个动作对应的奖赏是一个确定值, 那么尝试一遍所有的动作便能找出奖赏最大的动作. 然而, 更一般的情形是, 一个动作的奖赏值是来自于一个概率分布, 仅通过一次尝试并不能确切地获得平均奖赏值.

实际上,单步强化学习任务对应了一个理论模型,即 “ $K$ -摇臂赌博机” $(K$ - armed bandit). 如图 16.3 所示, $K$ -摇臂赌博机有 $K$ 个摇臂,赌徒在投入一个硬币后可选择按下其中一个摇臂，每个摇臂以一定的概率吐出硬币，但这个概率赌徒并不知道. 赌徒的目标是通过一定的策略最大化自己的奖赏, 即获得最多的硬币.

若仅为获知每个摇臂的期望奖赏，则可采用 “仅探索” (exploration-only)法: 将所有的尝试机会平均分配给每个摇臂(即轮流按下每个摇臂), 最后以每个摇臂各自的平均吐币概率作为其奖赏期望的近似估计. 若仅为执行奖赏最大的动作，则可采用 “仅利用” (exploitation-only)法:按下目前最优的(即到目前为止平均奖赏最大的)摇臂, 若有多个摇臂同为最优, 则从中随机选取一个. 显然, “仅探索” 法能很好地估计每个摇臂的奖赏, 却会失去很多选择最优摇臂的机会; “仅利用” 法则相反, 它没有很好地估计摇臂期望奖赏, 很可能经常选不到最优摇臂. 因此, 这两种方法都难以使最终的累积奖赏最大化.

---

亦称 “ $K$ -摇臂老虎机”.

---

![373_1039_120_468_383_0.jpg](../../images/373_1039_120_468_383_0.jpg)

图 ${16.3K}$ -摇臂赌博机图示

事实上, “探索” (即估计摇臂的优劣)和 “利用" (即选择当前最优摇臂)这两者是矛盾的, 因为尝试次数(即总投币数)有限, 加强了一方则会自然削弱另一方，这就是强化学习所面临的 “探索-利用窘境” (Exploration-Exploitation dilemma). 显然, 欲累积奖赏最大, 则必须在探索与利用之间达成较好的折中.

## ${16.2.2\epsilon }$ -贪心

$\epsilon$ -贪心法基于一个概率来对探索和利用进行折中: 每次尝试时,以 $\epsilon$ 的概率进行探索,即以均匀概率随机选取一个摇臂; 以 $1 - \epsilon$ 的概率进行利用,即选择当前平均奖赏最高的摇臂(若有多个, 则随机选取一个).

令 $Q\left( k\right)$ 记录摇臂 $k$ 的平均奖赏. 若摇臂 $k$ 被尝试了 $n$ 次,得到的奖赏为 ${v}_{1},{v}_{2},\ldots ,{v}_{n}$ ,则平均奖赏为

$$
Q\left( k\right)  = \frac{1}{n}\mathop{\sum }\limits_{{i = 1}}^{n}{v}_{i} \tag{16.1}
$$

若直接根据式(16.1)计算平均奖赏，则需记录 $n$ 个奖赏值. 显然，更高效的做法是对均值进行增量式计算，即每尝试一次就立即更新 $Q\left( k\right)$ . 不妨用下标来表示尝试的次数,初始时 ${Q}_{0}\left( k\right)  = 0$ . 对于任意的 $n \geq  1$ ,若第 $n - 1$ 次尝试后的平均奖赏为 ${Q}_{n - 1}\left( k\right)$ ,则在经过第 $n$ 次尝试获得奖赏 ${v}_{n}$ 后,平均奖赏应更新为

$$
{Q}_{n}\left( k\right)  = \frac{1}{n}\left( {\left( {n - 1}\right)  \times  {Q}_{n - 1}\left( k\right)  + {v}_{n}}\right) \tag{16.2}
$$

式(16.3)会在 16.4.2 节中用到.

$$
= {Q}_{n - 1}\left( k\right)  + \frac{1}{n}\left( {{v}_{n} - {Q}_{n - 1}\left( k\right) }\right) . \tag{16.3}
$$

这样,无论摇臂被尝试多少次都仅需记录两个值: 已尝试次数 $n - 1$ 和最近平均奖赏 ${Q}_{n - 1}\left( k\right)$ . $\epsilon$ -贪心算法描述如图 16.4 所示.

---

输入: 摇臂数 $K$ ;

			奖赏函数 $R$ ;

			尝试次数 $T$ ;

			探索概率 $\epsilon$ .

过程:

		$r = 0$

		$\forall i = 1,2,\ldots K : Q\left( i\right)  = 0,\operatorname{count}\left( i\right)  = 0;$

		for $t = 1,2,\ldots , T$ do

			if rand $\left( \right)  < \epsilon$ then

				$k =$ 从 $1,2,\ldots , K$ 中以均匀分布随机选取

			else

				$k = \arg \mathop{\max }\limits_{i}Q\left( i\right)$

			end if

			$v = R\left( k\right) ;$

			$r = r + v$

			$Q\left( k\right)  = \frac{Q\left( k\right)  \times  \operatorname{count}\left( k\right)  + v}{\operatorname{count}\left( k\right)  + 1};$

			$\operatorname{count}\left( k\right)  = \operatorname{count}\left( k\right)  + 1$

		end for

输出: 累积奖赏 $r$

---

图 ${16.4\epsilon }$ -贪心算法

---

$Q\left( i\right)$ 和 $\operatorname{count}\left( i\right)$ 分别记录摇臂 $i$ 的平均奖赏和选中次数.

在 $\left\lbrack  {0,1}\right\rbrack$ 中生成随机数.

---

本次尝试的奖赏值.

式(16.2)更新平均奖赏.

若摇臂奖赏的不确定性较大，例如概率分布较宽时，则需更多的探索，此时需要较大的 $\epsilon$ 值；若摇臂的不确定性较小，例如概率分布较集中时，则少量的尝试就能很好地近似真实奖赏，此时需要的 $\epsilon$ 较小. 通常令 $\epsilon$ 取一个较小的常数， 如 0.1 或 0.01 . 然而, 若尝试次数非常大, 那么在一段时间后, 摇臂的奖赏都能很好地近似出来,不再需要探索,这种情形下可让 $\epsilon$ 随着尝试次数的增加而逐渐减小,例如令 $\epsilon  = 1/\sqrt{t}$ .

### 16.2.3 Softmax

Softmax 算法基于当前已知的摇臂平均奖赏来对探索和利用进行折中. 若各摇臂的平均奖赏相当，则选取各摇臂的概率也相当；若某些摇臂的平均奖赏明显高于其他摇臂，则它们被选取的概率也明显更高. Softmax 算法中摇臂概率的分配是基于 Boltzmann 分布

$$
P\left( k\right)  = \frac{{e}^{\frac{Q\left( k\right) }{\tau }}}{\mathop{\sum }\limits_{{i = 1}}^{K}{e}^{\frac{Q\left( i\right) }{\tau }}}, \tag{16.4}
$$

其中, $Q\left( i\right)$ 记录当前摇臂的平均奖赏; $\tau  > 0$ 称为 “温度”, $\tau$ 越小则平均奖赏高的摇臂被选取的概率越高. $\tau$ 趋于 0 时 Softmax 将趋于 “仅利用”, $\tau$ 趋于无穷大时 Softmax 则将趋于 “仅探索”. Softmax 算法描述如图 16.5 所示.

---

输入: 摇臂数 $K$ ;

			奖赏函数 $R$ ;

			尝试次数 $T$ ;

			温度参数 $\tau$ .

过程:

	$r = 0$ ;

		$\forall i = 1,2,\ldots K : Q\left( i\right)  = 0,$ count $\left( i\right)  = 0;$

		for $t = 1,2,\ldots , T$ do

		$k =$ 从 $1,2,\ldots , K$ 中根据式(16.4)随机选取

		$v = R\left( k\right)$

		$r = r + v$

		$Q\left( k\right)  = \frac{Q\left( k\right)  \times  \operatorname{count}\left( k\right)  + v}{\operatorname{count}\left( k\right)  + 1};$

		$\operatorname{count}\left( k\right)  = \operatorname{count}\left( k\right)  + 1$

		end for

输出: 累积奖赏 $r$

---

图 16.5 Softmax算法

$\epsilon$ -贪心算法与 Softmax 算法孰优孰劣,主要取决于具体应用. 为了更直观地观察它们的差别, 考虑一个简单的例子: 假定 2-摇臂赌博机的摇臂 1 以 0.4 的概率返回奖赏 1 , 以 0.6 的概率返回奖赏 0 ; 摇臂 2 以 0.2 的概率返回奖赏 1 , 以 0.8 的概率返回奖赏 0 . 图 16.6 显示了不同算法在不同参数下的平均累积奖赏, 其中每条曲线对应于重复 1000 次实验的平均结果. 可以看出, Softmax $\left( {\tau  = {0.01}}\right)$ 的曲线与 “仅利用” 的曲线几乎重合.

对于离散状态空间、离散动作空间上的多步强化学习任务, 一种直接的办法是将每个状态上动作的选择看作一个 $K$ -摇臂赌博机问题,用强化学习任务的累积奖赏来代替 $K$ -摇臂赌博机算法中的奖赏函数，即可将赌博机算法用于每个状态:对每个状态分别记录各动作的尝试次数、当前平均累积奖赏等信息, 基于赌博机算法选择要尝试的动作. 然而这样的做法有很多局限, 因为它没有考虑强化学习任务马尔可夫决策过程的结构. 在 16.3 节将会看到, 若能有效考虑马尔可夫决策过程的特性, 则可有更聪明的办法.

---

第 4 行中式(16.4)的参数.

$Q\left( i\right)$ 和 $\operatorname{count}\left( i\right)$ 分别记录摇臂 $i$ 的平均奖赏和选中次数.

本次尝试的奖赏值.

式(16.2)更新平均奖赏.

---

![376_855_134_892_578_0.jpg](../../images/376_855_134_892_578_0.jpg)

图 16.6 不同算法在 2-摇臂赌博机上的性能比较

## 16.3 有模型学习

考虑多步强化学习任务, 暂且先假定任务对应的马尔可夫决策过程四元组 $E = \langle X, A, P, R\rangle$ 均为已知,这样的情形称为 “模型已知”,即机器已对环境进行了建模, 能在机器内部模拟出与环境相同或近似的状况. 在已知模型的环境中学习称为 “有模型学习” (model-based learning). 此时,对于任意状态 $x,{x}^{\prime }$ 和动作 $a$ ,在 $x$ 状态下执行动作 $a$ 转移到 ${x}^{\prime }$ 状态的概率 ${P}_{x \rightarrow  {x}^{\prime }}^{a}$ 是已知的,该转移所带来的奖赏 ${R}_{x \rightarrow  {x}^{\prime }}^{a}$ 也是已知的. 为便于讨论,不妨假设状态空间 $X$ 和动作空间 $A$ 均为有限.

### 16.3.1 策略评估

在模型已知时，对任意策略 $\pi$ 能估计出该策略带来的期望累积奖赏. 令函数 ${V}^{\pi }\left( x\right)$ 表示从状态 $x$ 出发，使用策略 $\pi$ 所带来的累积奖赏；函数 ${Q}^{\pi }\left( {x, a}\right)$ 表示从状态 $x$ 出发,执行动作 $a$ 后再使用策略 $\pi$ 带来的累积奖赏. 这里的 $V\left( \cdot \right)$ 称为 “状态值函数” (state value function), $Q\left( \cdot \right)$ 称为 “状态-动作值函数” (state-action value function), 分别表示指定 “状态” 上以及指定 “状态-动作”上的累积奖赏.

---

16.4 节将讨论模型未知情形.

---

由累积奖赏的定义，有状态值函数

$$
\left\{  \begin{array}{ll} {V}_{T}^{\pi }\left( x\right)  = {\mathbb{E}}_{\pi }\left\lbrack  {\frac{1}{T}\mathop{\sum }\limits_{{t = 1}}^{T}{r}_{t} \mid  {x}_{0} = x}\right\rbrack  , & T\text{ 步累积奖赏; } \\  {V}_{\gamma }^{\pi }\left( x\right)  = {\mathbb{E}}_{\pi }\left\lbrack  {\mathop{\sum }\limits_{{t = 0}}^{{+\infty }}{\gamma }^{t}{r}_{t + 1} \mid  {x}_{0} = x}\right\rbrack  , & \gamma \text{ 折扣累积奖赏. } \end{array}\right. \tag{16.5}
$$

为叙述简洁，后面在涉及上述两种累积奖赏时，就不再说明奖赏类别，读者从上下文应能容易地判知. 令 ${x}_{0}$ 表示起始状态， ${a}_{0}$ 表示起始状态上采取的第一个动作; 对于 $T$ 步累积奖赏,用下标 $t$ 表示后续执行的步数. 我们有状态-动作值函数

$$
\left\{  \begin{array}{l} {Q}_{T}^{\pi }\left( {x, a}\right)  = {\mathbb{E}}_{\pi }\left\lbrack  {\frac{1}{T}\mathop{\sum }\limits_{{t = 1}}^{T}{r}_{t} \mid  {x}_{0} = x,{a}_{0} = a}\right\rbrack  ; \\  {Q}_{\gamma }^{\pi }\left( {x, a}\right)  = {\mathbb{E}}_{\pi }\left\lbrack  {\mathop{\sum }\limits_{{t = 0}}^{{+\infty }}{\gamma }^{t}{r}_{t + 1} \mid  {x}_{0} = x,{a}_{0} = a}\right\rbrack  . \end{array}\right. \tag{16.6}
$$

由于 MDP 具有马尔可夫性质, 即系统下一时刻的状态仅由当前时刻的状态决定,不依赖于以往任何状态,于是值函数有很简单的递归形式. 对于 $T$ 步累积奖赏有

$$
{V}_{T}^{\pi }\left( x\right)  = {\mathbb{E}}_{\pi }\left\lbrack  {\frac{1}{T}\mathop{\sum }\limits_{{t = 1}}^{T}{r}_{t} \mid  {x}_{0} = x}\right\rbrack
$$

$$
= {\mathbb{E}}_{\pi }\left\lbrack  {\frac{1}{T}{r}_{1} + \frac{T - 1}{T}\frac{1}{T - 1}\mathop{\sum }\limits_{{t = 2}}^{T}{r}_{t}\left| {\;{x}_{0} = x}\right. }\right\rbrack
$$

$$
= \mathop{\sum }\limits_{{a \in  A}}\pi \left( {x, a}\right) \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{T}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{T - 1}{T}{\mathbb{E}}_{\pi }\left\lbrack  {\frac{1}{T - 1}\mathop{\sum }\limits_{{t = 1}}^{{T - 1}}{r}_{t} \mid  {x}_{0} = {x}^{\prime }}\right\rbrack  }\right)
$$

$$
= \mathop{\sum }\limits_{{a \in  A}}\pi \left( {x, a}\right) \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{T}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{T - 1}{T}{V}_{T - 1}^{\pi }\left( {x}^{\prime }\right) }\right) . \tag{16.7}
$$

类似的,对于 $\gamma$ 折扣累积奖赏有

$$
{V}_{\gamma }^{\pi }\left( x\right)  = \mathop{\sum }\limits_{{a \in  A}}\pi \left( {x, a}\right) \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + \gamma {V}_{\gamma }^{\pi }\left( {x}^{\prime }\right) }\right) . \tag{16.8}
$$

需注意的是,正是由于 $P$ 和 $R$ 已知,才可以进行全概率展开.

读者可能已发现, 用上面的递归等式来计算值函数, 实际上就是一种动态规划算法. 对于 ${V}_{T}^{\pi }$ ,可设想递归一直进行下去,直到最初的起点; 换言之,从值函数的初始值 ${V}_{0}^{\pi }$ 出发,通过一次迭代能计算出每个状态的单步奖赏 ${V}_{1}^{\pi }$ ,进而

---

这样的递归等式称为 Bellman 等式.

动作-状态全概率展开.

---

---

输入: MDP 四元组 $E = \langle X, A, P, R\rangle$ ;

			被评估的策略 $\pi$ ;

			累积奖赏参数 $T$ .

过程:

		$\forall x \in  X : V\left( x\right)  = 0$ ;

		for $t = 1,2,\ldots$ do

			$\forall x \in  X : {V}^{\prime }\left( x\right)  = \mathop{\sum }\limits_{{a \in  A}}\pi \left( {x, a}\right) \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{t}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{t - 1}{t}V\left( {x}^{\prime }\right) }\right) ;$

			if $t = T + 1$ then

				break

			else

				$V = {V}^{\prime }$

			end if

		end for

输出: 状态值函数 $V$

---

图 16.7 基于 $T$ 步累积奖赏的策略评估算法

---

$V\left( x\right)$ 为 $x$ 的累积奖赏.

式(16.7)更新值函数.

---

这个写法是为了便于在同样的算法框架下考虑 $T$ 步累积奖赏和 $\gamma$ 折扣累积奖赏. 从单步奖赏出发,通过一次迭代计算出两步累积奖赏 ${V}_{2}^{\pi }$ , ……图 16.7 中算法遵循了上述流程,对于 $T$ 步累积奖赏,只需迭代 $T$ 轮就能精确地求出值函数.

---

参见习题 16.2.

---

对于 ${V}_{\gamma }^{\pi }$ ,由于 ${\gamma }^{t}$ 在 $t$ 很大时趋于 0,因此也能使用类似的算法,只需将图 16.7 算法的第 3 行根据式(16.8)进行替换. 此外, 由于算法可能会迭代很多次, 因此需设置一个停止准则. 常见的是设置一个阈值 $\theta$ ,若在执行一次迭代后值函数的改变小于 $\theta$ 则算法停止; 相应的,图 16.7 算法第 4 行中的 $t = T + 1$ 需替换为

$$
\mathop{\max }\limits_{{x \in  X}}\left| {V\left( x\right)  - {V}^{\prime }\left( x\right) }\right|  < \theta . \tag{16.9}
$$

有了状态值函数 $V$ ,就能直接计算出状态-动作值函数

$$
\left\{  \begin{array}{l} {Q}_{T}^{\pi }\left( {x, a}\right)  = \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{T}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{T - 1}{T}{V}_{T - 1}^{\pi }\left( {x}^{\prime }\right) }\right) ; \\  {Q}_{\gamma }^{\pi }\left( {x, a}\right)  = \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + \gamma {V}_{\gamma }^{\pi }\left( {x}^{\prime }\right) }\right) . \end{array}\right. \tag{16.10}
$$

### 16.3.2 策略改进

对某个策略的累积奖赏进行评估后, 若发现它并非最优策略, 则当然希望对其进行改进. 理想的策略应能最大化累积奖赏

$$
{\pi }^{ * } = \underset{\pi }{\arg \max }\mathop{\sum }\limits_{{x \in  X}}{V}^{\pi }\left( x\right) . \tag{16.11}
$$

一个强化学习任务可能有多个最优策略,最优策略所对应的值函数 ${V}^{ * }$ 称为最优值函数，即

$$
\forall x \in  X : {V}^{ * }\left( x\right)  = {V}^{{\pi }^{ * }}\left( x\right) . \tag{16.12}
$$

注意,当策略空间无约束时式 (16.12) 的 ${V}^{ * }$ 才是最优策略对应的值函数,例如对离散状态空间和离散动作空间，策略空间是所有状态上所有动作的组合，共有 ${\left| A\right| }^{\left| X\right| }$ 种不同的策略. 若策略空间有约束,则违背约束的策略是 “不合法” 的, 即便其值函数所取得的累积奖赏值最大, 也不能作为最优值函数.

由于最优值函数的累积奖赏值已达最大，因此可对前面的 Bellman 等式(16.7)和(16.8)做一个改动，即将对动作的求和改为取最优:

$$
\left\{  \begin{array}{l} {V}_{T}^{ * }\left( x\right)  = \mathop{\max }\limits_{{a \in  A}}\mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{T}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{T - 1}{T}{V}_{T - 1}^{ * }\left( {x}^{\prime }\right) }\right) ; \\  {V}_{\gamma }^{ * }\left( x\right)  = \mathop{\max }\limits_{{a \in  A}}\mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + \gamma {V}_{\gamma }^{ * }\left( {x}^{\prime }\right) }\right) . \end{array}\right. \tag{16.13}
$$

换言之,

$$
{V}^{ * }\left( x\right)  = \mathop{\max }\limits_{{a \in  A}}{Q}^{{\pi }^{ * }}\left( {x, a}\right) . \tag{16.14}
$$

代入式(16.10)可得最优状态-动作值函数

$$
\left\{  \begin{array}{l} {Q}_{T}^{ * }\left( {x, a}\right)  = \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{T}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{T - 1}{T}\mathop{\max }\limits_{{{a}^{\prime } \in  A}}{Q}_{T - 1}^{ * }\left( {{x}^{\prime },{a}^{\prime }}\right) }\right) ; \\  {Q}_{\gamma }^{ * }\left( {x, a}\right)  = \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + \gamma \mathop{\max }\limits_{{{a}^{\prime } \in  A}}{Q}_{\gamma }^{ * }\left( {{x}^{\prime },{a}^{\prime }}\right) }\right) . \end{array}\right. \tag{16.15}
$$

上述关于最优值函数的等式, 称为最优 Bellman 等式, 其唯一解是最优值函数.

最优 Bellman 等式揭示了非最优策略的改进方式: 将策略选择的动作改变为当前最优的动作. 显然, 这样的改变能使策略更好. 不妨令动作改变后对应的策略为 ${\pi }^{\prime }$ ,改变动作的条件为 ${Q}^{\pi }\left( {x,{\pi }^{i}\left( x\right) }\right)  \geq  {V}^{\pi }\left( x\right)$ ,以 $\gamma$ 折扣累积奖赏为例, 由式(16.10)可计算出递推不等式

$$
{V}^{\pi }\left( x\right)  \leq  {Q}^{\pi }\left( {x,{\pi }^{\prime }\left( x\right) }\right)
$$

$$
= \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{{\pi }^{\prime }\left( x\right) }\left( {{R}_{x \rightarrow  {x}^{\prime }}^{{\pi }^{\prime }\left( x\right) } + \gamma {V}^{\pi }\left( {x}^{\prime }\right) }\right)
$$

$$
\leq  \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{{\pi }^{\prime }\left( x\right) }\left( {{R}_{x \rightarrow  {x}^{\prime }}^{{\pi }^{\prime }\left( x\right) } + \gamma {Q}^{\pi }\left( {{x}^{\prime },{\pi }^{\prime }\left( {x}^{\prime }\right) }\right) }\right)
$$

$$
= \ldots
$$

$$
= {V}^{{\pi }^{\prime }}\left( x\right) \text{ . } \tag{16.16}
$$

值函数对于策略的每一点改进都是单调递增的,因此对于当前策略 $\pi$ ,可放心地将其改进为

$$
{\pi }^{\prime }\left( x\right)  = \underset{a \in  A}{\arg \max }{Q}^{\pi }\left( {x, a}\right) \tag{16.17}
$$

直到 ${\pi }^{\prime }$ 与 $\pi$ 一致、不再发生变化,此时就满足了最优 Bellman 等式,即找到了最优策略.

### 16.3.3 策略迭代与值迭代

由前两小节我们知道了如何评估一个策略的值函数, 以及在策略评估后如何改进至获得最优策略. 显然, 将这两者结合起来即可得到求解最优解的方法: 从一个初始策略(通常是随机策略)出发, 先进行策略评估, 然后改进策略, 评估改进的策略, 再进一步改进策略, 一一...不断迭代进行策略评估和改进, 直到策略收敛、不再改变为止. 这样的做法称为 “策略迭代” (policy iteration).

图 16.8 给出的算法描述,就是在基于 $T$ 步累积奖赏策略评估的基础上,加入策略改进而形成的策略迭代算法. 类似的,可得到基于 $\gamma$ 折扣累积奖赏的策略迭代算法. 策略迭代算法在每次改进策略后都需重新进行策略评估, 这通常比较耗时.

---

输入: MDP 四元组 $E = \langle X, A, P, R\rangle$ ;

			累积奖赏参数 $T$ .

过程:

	$\forall x \in  X : V\left( x\right)  = 0,\pi \left( {x, a}\right)  = \frac{1}{\left| A\left( x\right) \right| };$

		loop

			for $t = 1,2,\ldots$ do

				$\forall x \in  X : {V}^{\prime }\left( x\right)  = \mathop{\sum }\limits_{{a \in  A}}\pi \left( {x, a}\right) \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{t}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{t - 1}{t}V\left( {x}^{\prime }\right) }\right) ;$

				if $t = T + 1$ then

					break

				else

					$V = {V}^{\prime }$

				end if

			end for

			$\forall x \in  X : {\pi }^{\prime }\left( x\right)  = \arg \mathop{\max }\limits_{{a \in  A}}Q\left( {x, a}\right) ;$

			if $\forall x : {\pi }^{\prime }\left( x\right)  = \pi \left( x\right)$ then

				break

			else

				$\pi  = {\pi }^{\prime }$

			end if

		end loop

输出: 最优策略 $\pi$

---

图 16.8 基于 $T$ 步累积奖赏的策略迭代算法

---

$\left| {A\left( x\right) }\right|$ 是 $x$ 状态下所有可选动作数.

式(16.7)更新值函数.

式(16.10)计算 $Q$ 值.

参见习题 16.3.

---

由式(16.16)可知，策略改进与值函数的改进是一致的，因此可将策略改进视为值函数的改善，即由式(16.13)可得

$$
\left\{  \begin{array}{l} {V}_{T}\left( x\right)  = \mathop{\max }\limits_{{a \in  A}}\mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{T}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{T - 1}{T}{V}_{T - 1}\left( {x}^{\prime }\right) }\right) ; \\  {V}_{\gamma }\left( x\right)  = \mathop{\max }\limits_{{a \in  A}}\mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + \gamma {V}_{\gamma }\left( {x}^{\prime }\right) }\right) . \end{array}\right. \tag{16.18}
$$

于是可得到值迭代(value iteration)算法, 如图 16.9 所示.

---

输入: MDP 四元组 $E = \langle X, A, P, R\rangle$ ;

			累积奖赏参数 $T$ ;

			收敛阈值 $\theta$ .

过程:

		$\forall x \in  X : V\left( x\right)  = 0$ ;

		for $t = 1,2,\ldots$ do

		$\forall x \in  X : {V}^{\prime }\left( x\right)  = \mathop{\max }\limits_{{a \in  A}}\mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {\frac{1}{t}{R}_{x \rightarrow  {x}^{\prime }}^{a} + \frac{t - 1}{t}V\left( {x}^{\prime }\right) }\right) ;$

			if $\mathop{\max }\limits_{{x \in  X}}\left| {V\left( x\right)  - {V}^{\prime }\left( x\right) }\right|  < \theta$ then

				break

			else

				$V = {V}^{\prime }$

			end if

		end for

输出: 策略 $\pi \left( x\right)  = \arg \mathop{\max }\limits_{{a \in  A}}Q\left( {x, a}\right)$

---

图 16.9 基于 $T$ 步累积奖赏的值迭代算法

---

式(16.18)更新值函数.

式(16.10)计算 $Q$ 值.

---

若采用 $\gamma$ 折扣累积奖赏,只需将图 16.9 算法中第 3 行替换为

$$
\forall x \in  X : {V}^{\prime }\left( x\right)  = \mathop{\max }\limits_{{a \in  A}}\mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + {\gamma V}\left( {x}^{\prime }\right) }\right) . \tag{16.19}
$$

从上面的算法可看出, 在模型已知时强化学习任务能归结为基于动态规划的寻优问题. 与监督学习不同, 这里并未涉及到泛化能力, 而是为每一个状态找到最好的动作.

## 16.4 免模型学习

在现实的强化学习任务中，环境的转移概率、奖赏函数往往很难得知，甚至很难知道环境中一共有多少状态. 若学习算法不依赖于环境建模, 则称为 “免模型学习” (model-free learning), 这比有模型学习要困难得多.

### 16.4.1 蒙特卡罗强化学习

在免模型情形下, 策略迭代算法首先遇到的问题是策略无法评估, 这是由于模型未知而导致无法做全概率展开. 此时, 只能通过在环境中执行选择的动作,来观察转移的状态和得到的奖赏. 受 $K$ 摇臂赌博机的启发,一种直接的策略评估替代方法是多次 “采样”, 然后求取平均累积奖赏来作为期望累积奖赏的近似, 这称为蒙特卡罗强化学习. 由于采样必须为有限次数, 因此该方法更适合于使用 $T$ 步累积奖赏的强化学习任务.

另一方面，策略迭代算法估计的是状态值函数 $V$ ，而最终的策略是通过状态-动作值函数 $Q$ 来获得. 当模型已知时，从 $V$ 到 $Q$ 有很简单的转换方法，而当模型未知时,这也会出现困难. 于是,我们将估计对象从 $V$ 转变为 $Q$ ,即估计每一对 “状态-动作” 的值函数.

此外, 在模型未知的情形下, 机器只能是从一个起始状态(或起始状态集合)开始探索环境，而策略迭代算法由于需对每个状态分别进行估计，因此在这种情形下无法实现. 例如探索种瓜的过程只能从播下种子开始，而不能任意选择种植过程中的一个状态开始. 因此, 我们只能在探索的过程中逐渐发现各个状态并估计各状态-动作对的值函数.

综合起来，在模型未知的情形下，我们从起始状态出发，使用某种策略进行采样,执行该策略 $T$ 步并获得轨迹

$$
< {x}_{0},{a}_{0},{r}_{1},{x}_{1},{a}_{1},{r}_{2},\ldots ,{x}_{T - 1},{a}_{T - 1},{r}_{T},{x}_{T} >
$$

然后，对轨迹中出现的每一对状态-动作，记录其后的奖赏之和，作为该状态-动作对的一次累积奖赏采样值. 多次采样得到多条轨迹后, 将每个状态-动作对的累积奖赏采样值进行平均，即得到状态-动作值函数的估计.

可以看出, 欲较好地获得值函数的估计, 就需要多条不同的采样轨迹. 然而, 我们的策略有可能是确定性的, 即对于某个状态只会输出一个动作, 若使用这样的策略进行采样,则只能得到多条相同的轨迹. 这与 $K$ 摇臂赌博机的 “仅利用” 法面临相同的问题,因此可借鉴探索与利用折中的办法,例如使用 $\epsilon$ -贪心法,以 $\epsilon$ 的概率从所有动作中均匀随机选取一个,以 $1 - \epsilon$ 的概率选取当前最优动作. 我们将确定性的策略 $\pi$ 称为 “原始策略”,在原始策略上使用 $\epsilon$ -贪心法的策略记为

$$
{\pi }^{\epsilon }\left( x\right)  = \left\{  \begin{array}{ll} \pi \left( x\right) , & \text{ 以概率 }1 - \epsilon ; \\  A\text{ 中以均匀概率选取的动作, } & \text{ 以概率 }\epsilon . \end{array}\right. \tag{16.20}
$$

---

亦称 “无模型学习”.

蒙特卡罗方法参见 14.7 节；14.5.1 节中使用过马尔可夫链蒙特卡罗方法.

假定只有一个最优动作.

---

对于最大化值函数的原始策略 $\pi  = \arg \mathop{\max }\limits_{a}Q\left( {x, a}\right)$ ,其 $\epsilon$ -贪心策略 ${\pi }^{\epsilon }$ 中,当前最优动作被选中的概率是 $1 - \epsilon  + \frac{\epsilon }{\left| A\right| }$ ,而每个非最优动作被选中的概率是 $\frac{\epsilon }{\left| A\right| }$ . 于是, 每个动作都有可能被选取, 而多次采样将会产生不同的采样轨迹.

与策略迭代算法类似, 使用蒙特卡罗方法进行策略评估后, 同样要对策略进行改进. 前面在讨论策略改进时利用了式(16.16)揭示的单调性, 通过换入当前最优动作来改进策略. 对于任意原始策略 $\pi$ ,其 $\epsilon$ -贪心策略 ${\pi }^{\epsilon }$ 仅是将 $\epsilon$ 的概率均匀分配给所有动作,因此对于最大化值函数的原始策略 ${\pi }^{\prime }$ ,同样有 ${Q}^{\pi }\left( {x,{\pi }^{\prime }\left( x\right) }\right)  \geq  {V}^{\pi }\left( x\right)$ ,于是式(16.16)仍成立,即可以使用同样方法来进行策略改进.

图 16.10 给出了上述过程的算法描述, 这里被评估与被改进的是同一个策略, 因此称为 “同策略” (on-policy)蒙特卡罗强化学习算法. 算法中奖赏均值采用增量式计算，每采样出一条轨迹，就根据该轨迹涉及的所有 “状态-动作” 对来对值函数进行更新.

---

输入: 环境 $E$ ;

			动作空间 $A$ ;

			起始状态 ${x}_{0}$ ;

			策略执行步数 $T$ .

过程:

1: $Q\left( {x, a}\right)  = 0,\operatorname{count}\left( {x, a}\right)  = 0,\pi \left( {x, a}\right)  = \frac{1}{\left| A\left( x\right) \right| }$ ;

	for $s = 1,2,\ldots$ do

	8: 在 $E$ 中执行策略 $\pi$ 产生轨迹

			$< {x}_{0},{a}_{0},{r}_{1},{x}_{1},{a}_{1},{r}_{2},\ldots ,{x}_{T - 1},{a}_{T - 1},{r}_{T},{x}_{T} > ;$

			for $t = 0,1,\ldots , T - 1$ do

				$R = \frac{1}{T - t}\mathop{\sum }\limits_{{i = t + 1}}^{T}{r}_{i}$

				$Q\left( {{x}_{t},{a}_{t}}\right)  = \frac{Q\left( {{x}_{t},{a}_{t}}\right)  \times  \operatorname{count}\left( {{x}_{t},{a}_{t}}\right)  + R}{\operatorname{count}\left( {{x}_{t},{a}_{t}}\right)  + 1};$

				$\operatorname{count}\left( {{x}_{t},{a}_{t}}\right)  = \operatorname{count}\left( {{x}_{t},{a}_{t}}\right)  + 1$

			end for

			对所有已见状态 $x$ :

		$\pi \left( {x, a}\right)  = \left\{  \begin{array}{ll} \arg \mathop{\max }\limits_{{a}^{\prime }}Q\left( {x,{a}^{\prime }}\right) , & \text{ 以概率 }1 - \\  \text{ 以均匀概率从 }A\text{ 中选取动作, } & \text{ 以概率 }\epsilon . \end{array}\right.$

10: end for

输出: 策略 $\pi$

---

图 16.10 同策略蒙特卡罗强化学习算法

---

默认均匀概率选取动作. 采样第 $s$ 条轨迹.

对每一个状态-动作对. 计算轨迹中的累积奖赏. 式(16.2)更新平均奖赏.

---

根据值函数得到策略.

同策略蒙特卡罗强化学习算法最终产生的是 $\epsilon$ -贪心策略. 然而,引入 $\epsilon$ -贪心是为了便于策略评估,在使用策略时并不需要 $\epsilon$ -贪心; 实际上我们希望改进的是原始(非 $\epsilon$ -贪心)策略. 那么,能否仅在策略评估时引入 $\epsilon$ -贪心,而在策略改进时却改进原始策略呢?

这其实是可行的. 不妨用两个不同的策略 $\pi$ 和 ${\pi }^{\prime }$ 来产生采样轨迹,两者的区别在于每个 “状态-动作对” 被采样的概率不同. 一般的,函数 $f$ 在概率分布 $p$ 下的期望可表达为

$$
\mathbb{E}\left\lbrack  f\right\rbrack   = {\int }_{x}p\left( x\right) f\left( x\right) \mathrm{d}x, \tag{16.21}
$$

可通过从概率分布 $p$ 上的采样 $\left\{  {{x}_{1},{x}_{2},\ldots ,{x}_{m}}\right\}$ 来估计 $f$ 的期望,即

$$
\widehat{\mathbb{E}}\left\lbrack  f\right\rbrack   = \frac{1}{m}\mathop{\sum }\limits_{{i = 1}}^{m}f\left( x\right) . \tag{16.22}
$$

若引入另一个分布 $q$ ,则函数 $f$ 在概率分布 $p$ 下的期望也可等价地写为

$$
\mathbb{E}\left\lbrack  f\right\rbrack   = {\int }_{x}q\left( x\right) \frac{p\left( x\right) }{q\left( x\right) }f\left( x\right) \mathrm{d}x. \tag{16.23}
$$

上式可看作 $\frac{p\left( x\right) }{q\left( x\right) }f\left( x\right)$ 在分布 $q$ 下的期望,因此通过在 $q$ 上的采样 $\left\{  {x}_{1}^{\prime }\right.$ , $\left. {{x}_{2}^{\prime },\ldots ,{x}_{m}^{\prime }}\right\}$ 可估计为

$$
\widehat{\mathbb{E}}\left\lbrack  f\right\rbrack   = \frac{1}{m}\mathop{\sum }\limits_{{i = 1}}^{m}\frac{p\left( {x}_{i}^{\prime }\right) }{q\left( {x}_{i}^{\prime }\right) }f\left( {x}_{i}^{\prime }\right) . \tag{16.24}
$$

回到我们的问题上来,使用策略 $\pi$ 的采样轨迹来评估策略 $\pi$ ,实际上就是对累积奖赏估计期望

$$
Q\left( {x, a}\right)  = \frac{1}{m}\mathop{\sum }\limits_{{i = 1}}^{m}{r}_{i}. \tag{16.25}
$$

若改用策略 ${\pi }^{\prime }$ 的采样轨迹来评估策略 $\pi$ ,则仅需对累积奖赏加权,即

$$
Q\left( {x, a}\right)  = \frac{1}{m}\mathop{\sum }\limits_{{i = 1}}^{m}\frac{{P}_{i}^{\pi }}{{P}_{i}^{{\pi }^{\prime }}}{r}_{i}, \tag{16.26}
$$

其中 ${P}_{i}^{\pi }$ 和 ${P}_{i}^{{\pi }^{\prime }}$ 分别表示两个策略产生第 $i$ 条轨迹的概率. 对于给定的一条轨迹 $\left\langle  {{x}_{0},{a}_{0},{r}_{1},\ldots ,{x}_{T - 1},{a}_{T - 1},{r}_{T},{x}_{T}}\right\rangle$ ,策略 $\pi$ 产生该轨迹的概率为

$$
{P}^{\pi } = \mathop{\prod }\limits_{{i = 0}}^{{T - 1}}\pi \left( {{x}_{i},{a}_{i}}\right) {P}_{{x}_{i} \rightarrow  {x}_{i + 1}}^{{a}_{i}}. \tag{16.27}
$$

虽然这里用到了环境的转移概率 ${P}_{{x}_{i} \rightarrow  {x}_{i + 1}}^{{a}_{i}}$ ,但式(16.24)中实际只需两个策略概率的比值

$$
\frac{{P}^{\pi }}{{P}^{{\pi }^{\prime }}} = \mathop{\prod }\limits_{{i = 0}}^{{T - 1}}\frac{\pi \left( {{x}_{i},{a}_{i}}\right) }{{\pi }^{\prime }\left( {{x}_{i},{a}_{i}}\right) }. \tag{16.28}
$$

---

这样基于一个分布的采样来估计另一个分布下的期望, 称为重要性采样(importance sampling).

---

若 $\pi$ 为确定性策略而 ${\pi }^{\prime }$ 是 $\pi$ 的 $\epsilon$ -贪心策略,则 $\pi \left( {{x}_{i},{a}_{i}}\right)$ 始终为 $1,{\pi }^{\prime }\left( {{x}_{i},{a}_{i}}\right)$ 为 $\frac{\epsilon }{\left| A\right| }$ 或 $1 - \epsilon  + \frac{\epsilon }{\left| A\right| }$ ，于是就能对策略 $\pi$ 进行评估了. 图 16.11 给出了 “异策略” (off-policy) 蒙特卡罗强化学习算法的描述.

---

输入:环境 $E$ ；

			动作空间 $A$ ;

			起始状态 ${x}_{0}$ ;

			策略执行步数 $T$ .

过程:

		$Q\left( {x, a}\right)  = 0,\operatorname{count}\left( {x, a}\right)  = 0,\pi \left( {x, a}\right)  = \frac{1}{\left| A\left( x\right) \right| };$

	2: for $s = 1,2,\ldots$ do

		在 $E$ 中执行 $\pi$ 的 $\epsilon$ -贪心策略产生轨迹

			$< {x}_{0},{a}_{0},{r}_{1},{x}_{1},{a}_{1},{r}_{2},\ldots ,{x}_{T - 1},{a}_{T - 1},{r}_{T},{x}_{T} > ;$

			${p}_{i} = \left\{  \begin{array}{ll} 1 - \epsilon  + \epsilon /\left| A\right| , & {a}_{i} = \pi \left( x\right) \\  \epsilon /\left| A\right| , & {a}_{i} \neq  \pi \left( x\right)  \end{array}\right.$

			for $t = 0,1,\ldots , T - 1$ do

				$R = \frac{1}{T - t}\mathop{\sum }\limits_{{i = t + 1}}^{T}\left( {{r}_{i} \times  \mathop{\prod }\limits_{{j = i}}^{{T - 1}}\frac{1}{{p}_{j}}}\right)$

				$Q\left( {{x}_{t},{a}_{t}}\right)  = \frac{Q\left( {{x}_{t},{a}_{t}}\right)  \times  \operatorname{count}\left( {{x}_{t},{a}_{t}}\right)  + R}{\operatorname{count}\left( {{x}_{t},{a}_{t}}\right)  + 1};$

				$\operatorname{count}\left( {{x}_{t},{a}_{t}}\right)  = \operatorname{count}\left( {{x}_{t},{a}_{t}}\right)  + 1$

			end for

			$\pi \left( x\right)  = \arg \mathop{\max }\limits_{{a}^{\prime }}Q\left( {x,{a}^{\prime }}\right)$

		end for

输出: 策略 $\pi$

---

图 16.11 异策略蒙特卡罗强化学习算法

### 16.4.2 时序差分学习

蒙特卡罗强化学习算法通过考虑采样轨迹, 克服了模型未知给策略估计造成的困难. 此类算法需在完成一个采样轨迹后再更新策略的值估计, 而前面介绍的基于动态规划的策略迭代和值迭代算法在每执行一步策略后就进行值函数更新. 两者相比, 蒙特卡罗强化学习算法的效率低得多, 这里的主要问题是蒙特卡罗强化学习算法没有充分利用强化学习任务的 MDP 结构. 时序差分 (Temporal Difference, 简称 TD) 学习则结合了动态规划与蒙特卡罗方法的思想, 能做到更高效的免模型学习.

蒙特卡罗强化学习算法的本质, 是通过多次尝试后求平均来作为期望累积奖赏的近似，但它在求平均时是 “批处理式” 进行的，即在一个完整的采样轨迹完成后再对所有的状态-动作对进行更新. 实际上这个更新过程能增量式进行. 对于状态-动作对 $\left( {x, a}\right)$ ,不妨假定基于 $t$ 个采样已估计出值函数 ${Q}_{t}^{\pi }\left( {x, a}\right)  = \frac{1}{t}\mathop{\sum }\limits_{{i = 1}}^{t}{r}_{i}$ ,则在得到第 $t + 1$ 个采样 ${r}_{t + 1}$ 时,类似式(16.3),有

$$
{Q}_{t + 1}^{\pi }\left( {x, a}\right)  = {Q}_{t}^{\pi }\left( {x, a}\right)  + \frac{1}{t + 1}\left( {{r}_{t + 1} - {Q}_{t}^{\pi }\left( {x, a}\right) }\right) . \tag{16.29}
$$

---

默认均匀概率选取动作. 采样第 $s$ 条轨迹.

重要性采样系数.

计算修正的累积奖赏.

式(16.2) 更新平均奖赏.

根据值函数得到策略.

---

显然,只需给 ${Q}_{t}^{\pi }\left( {x, a}\right)$ 加上增量 $\frac{1}{t + 1}\left( {{r}_{t + 1} - {Q}_{t}^{\pi }\left( {x, a}\right) }\right)$ 即可. 更一般的,将 $\frac{1}{t + 1}$ 替换为系数 ${\alpha }_{t + 1}$ ,则可将增量项写作 ${\alpha }_{t + 1}\left( {{r}_{t + 1} - {Q}_{t}^{\pi }\left( {x, a}\right) }\right)$ . 在实践中通常令 ${\alpha }_{t}$ 为一个较小的正数值 $\alpha$ ,若将 ${Q}_{t}^{\pi }\left( {x, a}\right)$ 展开为每步累积奖赏之和,则可看出系数之和为 1,即令 ${\alpha }_{t} = \alpha$ 不会影响 ${Q}_{t}$ 是累积奖赏之和这一性质. 更新步长 $\alpha$ 越大, 则越靠后的累积奖赏越重要.

以 $\gamma$ 折扣累积奖赏为例,利用动态规划方法且考虑到模型未知时使用状态-动作值函数更方便，由式(16.10)有

$$
{Q}^{\pi }\left( {x, a}\right)  = \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + \gamma {V}^{\pi }\left( {x}^{\prime }\right) }\right)
$$

$$
= \mathop{\sum }\limits_{{{x}^{\prime } \in  X}}{P}_{x \rightarrow  {x}^{\prime }}^{a}\left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + \gamma \mathop{\sum }\limits_{{{a}^{\prime } \in  A}}\pi \left( {{x}^{\prime },{a}^{\prime }}\right) {Q}^{\pi }\left( {{x}^{\prime },{a}^{\prime }}\right) }\right) . \tag{16.30}
$$

通过增量求和可得

$$
{Q}_{t + 1}^{\pi }\left( {x, a}\right)  = {Q}_{t}^{\pi }\left( {x, a}\right)  + \alpha \left( {{R}_{x \rightarrow  {x}^{\prime }}^{a} + \gamma {Q}_{t}^{\pi }\left( {{x}^{\prime },{a}^{\prime }}\right)  - {Q}_{t}^{\pi }\left( {x, a}\right) }\right) , \tag{16.31}
$$

其中 ${x}^{\prime }$ 是前一次在状态 $x$ 执行动作 $a$ 后转移到的状态, ${a}^{\prime }$ 是策略 $\pi$ 在 ${x}^{\prime }$ 上选择的动作.

使用式(16.31)，每执行一步策略就更新一次值函数估计，于是得到图 16.12 的算法. 该算法由于每次更新值函数需知道前一步的状态(state)、前一步的动作(action)、奖赏值(reward)、当前状态(state)、将要执行的动作(action)，由此得名为 Sarsa 算法 [Rummery and Niranjan, 1994]. 显然, Sarsa 是一个同策略算法,算法中评估(第 6 行)、执行(第 5 行)的均为 $\epsilon$ -贪心策略.

将 Sarsa 修改为异策略算法, 则得到图 16.13 描述的 Q-学习(Q-learning)算法 [Watkins and Dayan, 1992],该算法评估(第 6 行)的是 $\epsilon$ -贪心策略,而执行(第 5 行)的是原始策略.

---

将这几个英文单词的首字母连起来.

---

---

输入: 环境 $E$ ;

			动作空间 $A$ ;

			起始状态 ${x}_{0}$ ;

			奖赏折扣 $\gamma$ ;

			更新步长 $\alpha$ .

过程:

		$Q\left( {x, a}\right)  = 0,\pi \left( {x, a}\right)  = \frac{1}{\left| A\left( x\right) \right| };$

		$x = {x}_{0}, a = \pi \left( x\right) ;$

		for $t = 1,2,\ldots$ do

			$r,{x}^{\prime } =$ 在 $E$ 中执行动作 $a$ 产生的奖赏与转移的状态;

			${a}^{\prime } = {\pi }^{\epsilon }\left( {x}^{\prime }\right)$

			$Q\left( {x, a}\right)  = Q\left( {x, a}\right)  + \alpha \left( {r + {\gamma Q}\left( {{x}^{\prime },{a}^{\prime }}\right)  - Q\left( {x, a}\right) }\right) ;$

			$\pi \left( x\right)  = \arg \mathop{\max }\limits_{{a}^{\prime \prime }}Q\left( {x,{a}^{\prime \prime }}\right)$

			$x = {x}^{\prime }, a = {a}^{\prime }$

		end for

输出: 策略 $\pi$

---

图 16.12 Sarsa 算法

默认均匀概率选取动作.

---

单步执行策略.

原始策略的 $\epsilon$ -贪心策略.

式(16.31)更新值函数.

---

---

输入:环境 $E$ ；

			动作空间 $A$ ;

			起始状态 ${x}_{0}$ ;

			奖赏折扣 $\gamma$ ;

			更新步长 $\alpha$ .

过程:

		$Q\left( {x, a}\right)  = 0,\pi \left( {x, a}\right)  = \frac{1}{\left| A\left( x\right) \right| };$

		$x = {x}_{0};$

		for $t = 1,2,\ldots$ do

		$r,{x}^{\prime } =$ 在 $E$ 中执行动作 ${\pi }^{\epsilon }\left( x\right)$ 产生的奖赏与转移的状态;

			${a}^{\prime } = \pi \left( {x}^{\prime }\right)$

		$Q\left( {x, a}\right)  = Q\left( {x, a}\right)  + \alpha \left( {r + {\gamma Q}\left( {{x}^{\prime },{a}^{\prime }}\right)  - Q\left( {x, a}\right) }\right) ;$

			$\pi \left( x\right)  = \arg \mathop{\max }\limits_{{a}^{\prime \prime }}Q\left( {x,{a}^{\prime \prime }}\right) ;$

			$x = {x}^{\prime }, a = {a}^{\prime }$

		end for

输出: 策略 $\pi$

---

图 16.13 Q-学习算法

默认均匀概率选取动作.

单步执行策略.

原始策略.

式(16.31)更新值函数.

## 16.5 值函数近似

前面我们一直假定强化学习任务是在有限状态空间上进行, 每个状态可用一个编号来指代; 值函数则是关于有限状态的 “表格值函数” (tabular value function),即值函数能表示为一个数组,输入 $i$ 对应的函数值就是数组元素 $i$ 的值, 且更改一个状态上的值不会影响其他状态上的值. 然而, 现实强化学习任务所面临的状态空间往往是连续的，有无穷多个状态. 这该怎么办呢?

一个直接的想法是对状态空间进行离散化, 将连续状态空间转化为有限离散状态空间, 然后就能使用前面介绍的方法求解. 遗憾的是, 如何有效地对状态空间进行离散化是一个难题, 尤其是在对状态空间进行探索之前.

实际上, 我们不妨直接对连续状态空间的值函数进行学习. 假定状态空间为 $n$ 维实数空间 $X = {\mathbb{R}}^{n}$ ,此时显然无法用表格值函数来记录状态值. 先考虑简单情形，即值函数能表达为状态的线性函数 [Busoniu et al., 2010]

$$
{V}_{\mathbf{\theta }}\left( \mathbf{x}\right)  = {\mathbf{\theta }}^{\mathrm{T}}\mathbf{x}, \tag{16.32}
$$

其中 $\mathbf{x}$ 为状态向量， $\mathbf{\theta }$ 为参数向量. 由于此时的值函数难以像有限状态那样精确记录每个状态的值, 因此这样值函数的求解被称为值函数近似 (value function approximation).

我们希望通过式(16.32)学得的值函数尽可能近似真实值函数 ${V}^{\pi }$ ,近似程度常用最小二乘误差来度量:

$$
{E}_{\mathbf{\theta }} = {\mathbb{E}}_{\mathbf{x} \sim  \pi }\left\lbrack  {\left( {V}^{\pi }\left( \mathbf{x}\right)  - {V}_{\mathbf{\theta }}\left( \mathbf{x}\right) \right) }^{2}\right\rbrack  , \tag{16.33}
$$

其中 ${\mathbb{E}}_{\mathbf{x} \sim  \pi }$ 表示由策略 $\pi$ 所采样而得的状态上的期望.

为了使误差最小化，采用梯度下降法，对误差求负导数

$$
- \frac{\partial {E}_{\mathbf{\theta }}}{\partial \mathbf{\theta }} = {\mathbb{E}}_{\mathbf{x} \sim  \pi }\left\lbrack  {2\left( {{V}^{\pi }\left( \mathbf{x}\right)  - {V}_{\mathbf{\theta }}\left( \mathbf{x}\right) }\right) \frac{\partial {V}_{\mathbf{\theta }}\left( \mathbf{x}\right) }{\partial \mathbf{\theta }}}\right\rbrack
$$

$$
= {\mathbb{E}}_{\mathbf{x} \sim  \pi }\left\lbrack  {2\left( {{V}^{\pi }\left( \mathbf{x}\right)  - {V}_{\mathbf{\theta }}\left( \mathbf{x}\right) }\right) \mathbf{x}}\right\rbrack  , \tag{16.34}
$$

于是可得到对于单个样本的更新规则

$$
\mathbf{\theta } = \mathbf{\theta } + \alpha \left( {{V}^{\pi }\left( \mathbf{x}\right)  - {V}_{\mathbf{\theta }}\left( \mathbf{x}\right) }\right) \mathbf{x}. \tag{16.35}
$$

我们并不知道策略的真实值函数 ${V}^{\pi }$ ，但可借助时序差分学习，基于 ${V}^{\pi }\left( \mathbf{x}\right)  = r + \gamma {V}^{\pi }\left( {\mathbf{x}}^{\prime }\right)$ 用当前估计的值函数代替真实值函数，即

$$
\mathbf{\theta } = \mathbf{\theta } + \alpha \left( {r + \gamma {V}_{\mathbf{\theta }}\left( {\mathbf{x}}^{\prime }\right)  - {V}_{\mathbf{\theta }}\left( \mathbf{x}\right) }\right) \mathbf{x}
$$

$$
= \mathbf{\theta } + \alpha \left( {r + \gamma {\mathbf{\theta }}^{\mathrm{T}}{\mathbf{x}}^{\prime } - {\mathbf{\theta }}^{\mathrm{T}}\mathbf{x}}\right) \mathbf{x}, \tag{16.36}
$$

其中 ${\mathbf{x}}^{\prime }$ 是下一时刻的状态.

需注意的是, 在时序差分学习中需要状态-动作值函数以便获取策略. 这里一种简单的做法是令 $\mathbf{\theta }$ 作用于表示状态和动作的联合向量上,例如给状态向量增加一维用于存放动作编号,即将式(16.32)中的 $\mathbf{x}$ 替换为 $\left( {\mathbf{x};a}\right)$ ; 另一种做法是用 $0/1$ 对动作选择进行编码得到向量 $\mathbf{a} = \left( {0;\ldots ;1;\ldots ;0}\right)$ ，其中 “ 1 ” 表示该动作被选择,再将状态向量与其合并得到 $\left( {\mathbf{x};\mathbf{a}}\right)$ ,用于替换式(16.32)中的 $\mathbf{x}$ . 这样就使得线性近似的对象为状态-动作值函数.

核方法参见第 6 章.

基于线性值函数近似来替代 Sarsa 算法中的值函数，即可得到图 16.14 的线性值函数近似 Sarsa 算法. 类似地可得到线性值函数近似 Q-学习算法. 显然, 可以容易地用其他学习方法来代替式(16.32)中的线性学习器, 例如通过引入核方法实现非线性值函数近似.

---

输入:环境 $E$ ；

			动作空间 $A$ ;

			起始状态 ${x}_{0}$ ;

			奖赏折扣 $\gamma$ ;

			更新步长 $\alpha$ .

过程:

	$\mathbf{\theta } = \mathbf{0};$

	$\mathbf{x} = {\mathbf{x}}_{0}, a = \pi \left( \mathbf{x}\right)  = \arg \mathop{\max }\limits_{{a}^{\prime \prime }}{\mathbf{\theta }}^{\mathrm{T}}\left( {\mathbf{x};{a}^{\prime \prime }}\right) ;$

		for $t = 1,2,\ldots$ do

		$r,{\dot{\mathbf{x}}}^{\prime } =$ 在 $E$ 中执行动作 $a$ 产生的奖赏与转移的状态;

		${a}^{\prime } = {\pi }^{\epsilon }\left( {\mathbf{x}}^{\prime }\right)$

		$\mathbf{\theta } = \mathbf{\theta } + \alpha \left( {r + \gamma {\mathbf{\theta }}^{\mathrm{T}}\left( {{\mathbf{x}}^{\prime };{a}^{\prime }}\right)  - {\mathbf{\theta }}^{\mathrm{T}}\left( {\mathbf{x};a}\right) }\right) \left( {\mathbf{x};a}\right) ;$

		$\pi \left( \mathbf{x}\right)  = \arg \mathop{\max }\limits_{{a}^{\prime \prime }}{\mathbf{\theta }}^{\mathrm{T}}\left( {\mathbf{x};{a}^{\prime \prime }}\right) ;$

		$\mathbf{x} = {\mathbf{x}}^{\prime }, a = {a}^{\prime }$

	end for

输出: 策略 $\pi$

---

图 16.14 线性值函数近似 Sarsa 算法

---

原始策略的 $\epsilon$ -贪心策略. 式(16.36)更新参数.

---

## 16.6 模仿学习

---

亦称 “学徒学习” (apprenticeship learning), “示范学习” (learning from demonstration), “观察学习” (learning by watching); 与机器学习早期的“示教学习”有直接联系，参见 1.5 节.

---

在强化学习的经典任务设置中，机器所能获得的反馈信息仅有多步决策后的累积奖赏，但在现实任务中，往往能得到人类专家的决策过程范例，例如在种瓜任务上能得到农业专家的种植过程范例. 从这样的范例中学习，称为 “模仿学习" (imitation learning).

### 16.6.1 直接模仿学习

强化学习任务中多步决策的搜索空间巨大, 基于累积奖赏来学习很多步之前的合适决策非常困难, 而直接模仿人类专家的 “状态-动作对” 可显著缓解这一困难，我们称其为“直接模仿学习”.

假定我们获得了一批人类专家的决策轨迹数据 $\left\{  {{\tau }_{1},{\tau }_{2},\ldots ,{\tau }_{m}}\right\}$ ,每条轨迹包含状态和动作序列

$$
{\tau }_{i} = \left\langle  {{s}_{1}^{i},{a}_{1}^{i},{s}_{2}^{i},{a}_{2}^{i},\ldots ,{s}_{{n}_{i} + 1}^{i}}\right\rangle  ,
$$

其中 ${n}_{i}$ 为第 $i$ 条轨迹中的转移次数.

有了这样的数据, 就相当于告诉机器在什么状态下应选择什么动作, 于是可利用监督学习来学得符合人类专家决策轨迹数据的策略.

我们可将所有轨迹上的所有 “状态-动作对” 抽取出来, 构造出一个新的数据集合

$$
D = \left\{  {\left( {{s}_{1},{a}_{1}}\right) ,\left( {{s}_{2},{a}_{2}}\right) ,\ldots ,\left( {{s}_{\mathop{\sum }\limits_{{i = 1}}^{m}{n}_{i}},{a}_{\mathop{\sum }\limits_{{i = 1}}^{m}{n}_{i}}}\right) }\right\}  ,
$$

即把状态作为特征,动作作为标记; 然后,对这个新构造出的数据集合 $D$ 使用分类(对于离散动作)或回归(对于连续动作)算法即可学得策略模型. 学得的这个策略模型可作为机器进行强化学习的初始策略, 再通过强化学习方法基于环境反馈进行改进, 从而获得更好的策略.

### 16.6.2 逆强化学习

在很多任务中, 设计奖赏函数往往相当困难, 从人类专家提供的范例数据中反推出奖赏函数有助于解决该问题, 这就是逆强化学习 (inverse reinforcement learning) [Abbeel and Ng, 2004].

在逆强化学习中,我们知道状态空间 $X$ 、动作空间 $A$ ,并且与直接模仿学习类似,有一个决策轨迹数据集 $\left\{  {{\tau }_{1},{\tau }_{2},\ldots ,{\tau }_{m}}\right\}$ . 逆强化学习的基本思想是: 欲使机器做出与范例一致的行为, 等价于在某个奖赏函数的环境中求解最优策略, 该最优策略所产生的轨迹与范例数据一致. 换言之, 我们要寻找某种奖赏函数使得范例数据是最优的, 然后即可使用这个奖赏函数来训练强化学习策略.

不妨假设奖赏函数能表达为状态特征的线性函数，即 $R\left( \mathbf{x}\right)  = {\mathbf{w}}^{\mathrm{T}}\mathbf{x}$ . 于是， 策略 $\pi$ 的累积奖赏可写为

$$
{\rho }^{\pi } = \mathbb{E}\left\lbrack  {\mathop{\sum }\limits_{{t = 0}}^{{+\infty }}{\gamma }^{t}R\left( {\mathbf{x}}_{t}\right)  \mid  \pi }\right\rbrack   = \mathbb{E}\left\lbrack  {\mathop{\sum }\limits_{{t = 0}}^{{+\infty }}{\gamma }^{t}{\mathbf{w}}^{\mathrm{T}}{\mathbf{x}}_{t} \mid  \pi }\right\rbrack
$$

$$
= {\mathbf{w}}^{\mathrm{T}}\mathbb{E}\left\lbrack  {\mathop{\sum }\limits_{{t = 0}}^{{+\infty }}{\gamma }^{t}{\mathbf{x}}_{t} \mid  \pi }\right\rbrack  , \tag{16.37}
$$

即状态向量加权和的期望与系数 $\mathbf{w}$ 的内积.

将状态向量的期望 $\mathbb{E}\left\lbrack  {\mathop{\sum }\limits_{{t = 0}}^{{+\infty }}{\gamma }^{t}{\mathbf{x}}_{t} \mid  \pi }\right\rbrack$ 简写为 ${\overline{\mathbf{x}}}^{\pi }$ . 注意到获得 ${\overline{\mathbf{x}}}^{\pi }$ 需求取期望. 我们可使用蒙特卡罗方法通过采样来近似期望, 而范例轨迹数据集恰可看作最优策略的一个采样, 于是, 可将每条范例轨迹上的状态加权求和再平均, 记为 ${\overline{\mathbf{x}}}^{ * }$ . 对于最优奖赏函数 $R\left( \mathbf{x}\right)  = {\mathbf{w}}^{*\mathrm{\;T}}\mathbf{x}$ 和任意其他策略产生的 ${\overline{\mathbf{x}}}^{\pi }$ ,有

$$
{\mathbf{w}}^{*\mathrm{\;T}}{\overline{\mathbf{x}}}^{ * } - {\mathbf{w}}^{*\mathrm{\;T}}{\overline{\mathbf{x}}}^{\pi } = {\mathbf{w}}^{*\mathrm{\;T}}\left( {{\overline{\mathbf{x}}}^{ * } - {\overline{\mathbf{x}}}^{\pi }}\right)  \geq  0. \tag{16.38}
$$

若能对所有策略计算出 $\left( {{\overline{\mathbf{x}}}^{ * } - {\overline{\mathbf{x}}}^{\pi }}\right)$ ,即可解出

$$
{\mathbf{w}}^{ * } = \underset{\mathbf{w}}{\arg \max }\mathop{\min }\limits_{\pi }{\mathbf{w}}^{\mathrm{T}}\left( {{\overline{\mathbf{x}}}^{ * } - {\overline{\mathbf{x}}}^{\pi }}\right) \tag{16.39}
$$

$$
\text{ s.t. }\parallel \mathbf{w}\parallel  \leq  1
$$

显然, 我们难以获得所有策略, 一个较好的办法是从随机策略开始, 迭代地求解更好的奖赏函数, 基于奖赏函数获得更好的策略, 直至最终获得最符合范例轨迹数据集的奖赏函数和策略，如图 16.15 算法所示. 注意在求解更好的奖赏函数时，需将式(16.39)中对所有策略求最小改为对之前学得的策略求最小.

---

输入: 环境 $E$ ;

					状态空间 $X$ ;

					动作空间 $A$ ;

					范例轨迹数据集 $D = \left\{  {{\tau }_{1},{\tau }_{2},\ldots ,{\tau }_{m}}\right\}$ .

过程:

	1: ${\overline{\mathbf{x}}}^{ * } =$ 从范例轨迹中算出状态加权和的均值向量;

			$\pi  =$ 随机策略;

			for $t = 1,2,\ldots$ do

				${\overline{\mathbf{x}}}_{t}^{\pi } =$ 从 $\pi$ 的采样轨迹算出状态加权和的均值向量;

			求解 ${\mathbf{w}}^{ * } = \arg \mathop{\max }\limits_{\mathbf{w}}\mathop{\min }\limits_{{i = 1}}^{t}{\mathbf{w}}^{\mathrm{T}}\left( {{\widetilde{\mathbf{x}}}^{ * } - {\overline{\mathbf{x}}}_{i}^{\pi }}\right) \;$ s.t. $\;\parallel \mathbf{w}\parallel  \leq  1$ ;

				$\pi  =$ 在环境 $\left\langle  {X, A, R\left( \mathbf{x}\right)  = {{\mathbf{w}}^{ * }}^{\mathrm{T}}\mathbf{x}}\right\rangle$ 中求解最优策略;

			end for

输出: 奖赏函数 $R\left( \mathbf{x}\right)  = {\mathbf{w}}^{*\mathrm{\;T}}\mathbf{x}$ 与策略 $\pi$

---

图 16.15 迭代式逆强化学习算法

## 16.7 阅读材料

强化学习专门书籍中最著名的是 [Sutton and Barto, 1998]. [Gosavi, 2003] 从优化的角度来讨论强化学习, [Whiteson, 2010] 则侧重于介绍基于演化算法搜索的强化学习方法. [Mausam and Kolobov, 2012] 从马尔可夫决策过程的视角介绍强化学习, [Sigaud and Buffet, 2010] 覆盖了很多内容, 包括本章未介绍的部分可观察马尔可夫决策过程 (Partially Observable MDP, 简称 POMDP)、 策略梯度法等. 基于值函数近似的强化学习可参阅 [Busoniu et al., 2010].

欧洲强化学习研讨会(EWRL)是专门性的强化学习系列研讨会，多学科强化学习与决策会议(RLDM)则是从 2013 年开始的新会议.

[Kaelbling et al., 1996] 是一个较早的强化学习综述, [Kober et al., 2013; Deisenroth et al., 2013] 则综述了强化学习在机器人领域的应用.

[Kuleshov and Precup, 2000] 和 [Vermorel and Mohri, 2005] 介绍了多种 $K$ -摇臂赌博机算法并进行了比较. 多摇臂赌博机模型在统计学领域有大量研究 [Berry and Fristedt, 1985], 近年来在 “在线学习” (online learning)、 “对抗学习" (adversarial learning) 等方面有广泛应用, [Bubeck and Cesa-Bianchi, 2012] 对其 “悔界” (regret bound)分析方面的结果进行了综述.

时序差分(TD)学习最早是 A. Samuel 在他著名的跳棋工作中提出, [Sutton,1988] 提出了 $\operatorname{TD}\left( \lambda \right)$ 算法,由于 [Tesauro,1995] 基于 $\operatorname{TD}\left( \lambda \right)$ 研制的 TD-Gammon 程序在西洋双陆棋上达到人类世界冠军水平而使 TD 学习备受关注. Q-学习算法是 [Watkins and Dayan, 1992] 提出, Sarsa 则是在 Q-学习算法基础上的改进 [Rummery and Niranjan, 1994]. TD 学习近年来仍有改进和推广, 例如广义 TD 学习 [Ueno et al., 2011]、使用资格迹(eligibility traces)的 TD 学习 [Geist and Scherrer, 2014]等. [Dann et al., 2014] 对 TD 学习中的策略评估方法进行了比较.

模仿学习被认为是强化学习提速的重要手段 [Lin, 1992; Price and Boutili-er, 2003], 在机器人领域被广泛使用 [Argall et al., 2009]. [Abbeel and Ng, 2004; Langford and Zadrozny, 2005] 提出了逆强化学习方法.

在运筹学与控制论领域，强化学习方面的研究被称为 “近似动态规划" (approximate dynamic programming), 可参阅 [Bertsekas, 2012].

---

“后悔” (regret)是指在不确定性条件下的决策与确定性条件下的决策所获得的奖赏间的差别.

Samuel 跳棋工作参见 p.22.

---

## 习题

16.1 用于 $K$ -摇臂赌博机的 UCB (Upper Confidence Bound,上置信界)方法每次选择 $Q\left( k\right)  + {UC}\left( k\right)$ 最大的摇臂,其中 $Q\left( k\right)$ 为摇臂 $k$ 当前的平均奖赏, ${UC}\left( k\right)$ 为置信区间. 例如

$$
Q\left( k\right)  + \sqrt{\frac{2\ln n}{{n}_{k}}}
$$

其中 $n$ 为已执行所有摇臂的总次数, ${n}_{k}$ 为已执行摇臂 $k$ 的次数. 试比较 UCB 方法与 $\epsilon$ -贪心法和 Softmax 方法的异同.

16.2 借鉴图 16.7,试写出基于 $\gamma$ 折扣奖赏函数的策略评估算法.

16.3 借鉴图 16.8,试写出基于 $\gamma$ 折扣奖赏函数的策略迭代算法.

16.4 在没有 MDP 模型时, 可以先学习 MDP 模型(例如使用随机策略进行采样, 从样本中估计出转移函数和奖赏函数), 然后再使用有模型强化学习方法. 试述该方法与免模型强化学习方法的优缺点.

16.5 试推导出 Sarsa 算法的更新公式(16.31).

16.6 试借鉴图 16.14 给出线性值函数近似 Q-学习算法.

16.7 线性值函数近似在实践中往往有较大误差. 试结合 BP 神经网络, 将线性值函数近似 Sarsa 算法推广为使用神经网络近似的 Sarsa 算法.

16.8 试结合核方法, 将线性值函数近似 Sarsa 算法推广为使用核函数的非线性值函数近似 Sarsa 算法.

16.9 对于目标驱动 (goal-directed) 的强化学习任务, 目标是到达某一状态, 例如将汽车驾驶到预定位置. 试为这样的任务设置奖赏函数，并讨论不同奖赏函数的作用(例如每一步未达目标的奖赏为 0 、-1 或 1 ).

$\mathbf{{16.10}^{ * }}$ 与传统监督学习不同,直接模仿学习在不同时刻所面临的数据分布可能不同. 试设计一个考虑不同时刻数据分布变化的模仿学习算法.

## 参考文献

Abbeel, P. and A. Y. Ng. (2004). "Apprenticeship learning via inverse reinforcement learning." In Proceedings of the 21st International Conference on Machine Learning (ICML), Banff, Canada.

Argall, B. D., S. Chernova, M. Veloso, and B. Browning. (2009). "A survey of robot learning from demonstration." Robotics and Autonomous Systems, 57(5):469-483.

Berry, D. and B. Fristedt. (1985). Bandit Problems. Chapman & Hall/CRC, London, UK.

Bertsekas, D. P. (2012). Dynamic Programming and Optimal Control: Approximate Dynamic Programming, 4th edition. Athena Scientific, Nashua, NH.

Bubeck, S. and N. Cesa-Bianchi. (2012). "Regret analysis of stochastic and nonstochastic multi-armed bandit problems." Foundations and Trends in Machine Learning, 5(1):1-122.

Busoniu, L., R. Babuska, B. De Schutter, and D. Ernst. (2010). Reinforcement Learning and Dynamic Programming Using Function Approximators. Chapman & Hall/CRC Press, Boca Raton, FL.

Dann, C., G. Neumann, and J. Peters. (2014). "Policy evaluation with temporal differences: A survey and comparison." Journal of Machine Learning Research, 15:809-883.

Deisenroth, M. P., G. Neumann, and J. Peters. (2013). "A survey on policy search for robotics." Foundations and Trends in Robotics, 2(1-2):1-142.

Geist, M. and B. Scherrer. (2014). "Off-policy learning with eligibility traces: A survey." Journal of Machine Learning Research, 15:289-333.

Gosavi, A. (2003). Simulation-Based Optimization: Parametric Optimization Techniques and Reinforcement Learning. Kluwer, Norwell, MA.

Kaelbling, L. P., M. L. Littman, and A. W. Moore. (1996). "Reinforcement learning: A survey." Journal of Artificial Intelligence Research, 4:237-285.

Kober, J., J. A. Bagnell, and J. Peters. (2013). "Reinforcement learning in robotics: A survey." International Journal on Robotics Research, 32(11): 1238-1274.

Kuleshov, V. and D. Precup. (2000). "Algorithms for the multi-armed bandit problem." Journal of Machine Learning Research, 1:1-48.

Langford, J. and B. Zadrozny. (2005). "Relating reinforcement learning performance to classification performance." In Proceedings of the 22nd International Conference on Machine Learning (ICML), 473-480, Bonn, Germany.

Lin, L.-J. (1992). "Self-improving reactive agents based on reinforcement learning, planning and teaching." Machine Learning, 8(3-4):293-321.

Mausam and A. Kolobov. (2012). Planning with Markov Decision Processes: An AI Perspective. Morgan & Claypool, San Rafael, CA.

Price, B. and C. Boutilier. (2003). "Accelerating reinforcement learning through implicit imitation." Journal of Artificial Intelligence Research, 19: 569-629.

Rummery, G. A. and M. Niranjan. (1994). "On-line Q-learning using connec-tionist systems." Technical Report CUED/F-INFENG/TR 166, Engineering Department, Cambridge University, Cambridge, UK.

Sigaud, O. and O. Buffet. (2010). Markov Decision Processes in Artificial Intelligence. Wiley, Hoboken, NJ.

Sutton, R. S. (1988). "Learning to predict by the methods of temporal differences." Machine Learning, 3(1):9-44.

Sutton, R. S. and A. G. Barto. (1998). Reinforcement Learning: An Introduction. MIT Press, Cambridge, MA.

Tesauro, G. (1995). "Temporal difference learning and TD-Gammon." Communications of the ACM, 38(3):58-68.

Ueno, T., S. Maeda, M. Kawanabe, and S. Ishii. (2011). "Generalized TD learning." Journal of Machine Learning Research, 12:1977-2020.

Vermorel, J. and M. Mohri. (2005). "Multi-armed bandit algorithms and empirical evaluation." In Proceedings of the 16th European Conference on Machine Learning (ECML), 437-448, Porto, Portugal.

Watkins, C. J. C. H. and P. Dayan. (1992). "Q-learning." Machine Learning, 8 (3-4):279-292.

Whiteson, S. (2010). Adaptive Representations for Reinforcement Learning. Springer, Berlin.

休息一会儿

![396_1667_308_278_351_0.jpg](../../images/396_1667_308_278_351_0.jpg)

## 小故事:马尔可夫决策过程与安德烈·马尔可夫

安德烈・安德烈维奇・马尔可夫(Andrey Andreyevich Markov, 1856—1922)是著名俄罗斯数学家、圣彼得堡数学学派代表性人物，在概率论、数论、函数逼近论、微分方程等方面有重要贡献.

马尔可夫出生在莫斯科东南的梁赞(Ryazan)，17 岁时独立发现了一种线性常微分方程的解法，引起了圣彼得堡大学几位数学家的注意. 1874 年他考入圣彼得堡大学数学系, 1878 年毕业并留校任教, 1884 年获博士学位，导师是圣彼得堡学派领袖、著名数学家切比雪夫. 此后马尔可夫一直在圣彼得堡大学任教. 马尔可夫在早期主要是沿着切比雪夫开创的方向，改进和完善了大数定律和中心极限定理，但他最重要的工作无疑是开辟了随机过程这个领域. 他在1906-1912年间提出了马尔可夫链, 开创了对马尔可夫过程的研究. 现实世界里小到分子的布朗运动、大到传染病流行过程，马尔可夫过程几乎无所不在. 在他的名著《概率演算》中, 马尔可夫是以普希金的长诗《叶甫根尼·奥涅金》中元、辅音字母变化的规律为例来展示马尔可夫链的性质. 马尔可夫决策过程是马尔可夫过程与确定性动态规划的结合，基本思想在二十世纪五十年代出现，此时马尔可夫已去世三十多年了.

马尔可夫的儿子也叫安德烈·安德烈维奇·马尔可夫 (1903-1979)，也是著名数学家，数理逻辑中的 “马尔可夫原则” (Markov Principle)、 “马尔可夫规则" (Markov Rule)，理论计算机科学中图灵完备的 “马尔可夫算法” 等，是以小马尔可夫的名字命名的. 马尔可夫的弟弟弗拉基米尔·安德烈维奇 · 马尔可夫(1871-1897)也是一位数学家，“马尔可夫兄弟不等式”就是以他和哥哥安德烈的名字命名的.

---

切比雪夫在圣彼得堡大学培养出马尔可夫、李亚普诺夫、柯尔金、格拉维等著名数学家，还影响了圣彼得堡大学之外的很多数学家. 圣彼得堡学派标志着俄罗斯数学走到了世界前沿.

---

<table><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>___.</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>数 。 题</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>中国</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>数量的变化</td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>
