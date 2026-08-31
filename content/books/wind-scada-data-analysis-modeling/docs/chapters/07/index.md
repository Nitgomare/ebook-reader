# 第7章 风电机组SCADA数据智能识别

聚类、分类是数据挖掘的重要任务，也是两类常用的智能算法与模型。前者是自动寻找并建立分组规则，通过判断数据样本之间的相似性，把相似数据样本划分在一个簇中，属于无监督的智能学习方法；后者是从数据样本中选出已经分好类的训练集，并建立一个分类模型，再将该模型用于对没有分类的数据样本进行分类，属于有监督的智能学习方法。在风电SCADA数据分析中，异常数据筛选、风电机组及其部件运行工况识别和故障诊断经常采用聚类、分类算法，所谓异常数据和正常数据、异常状态和正常状态，从数据建模与分析角度而言是相同的，这里统称为数据智能识别。在异常数据筛选方面，提出基于密度分布的聚类算法、随机森林等智能模型应用于识别异常数据<sup>\[1-3\]</sup>；在风电机组故障数据识别方面，应用神经网络算法、模拟退火遗传算法、支持向量机等智能模型进行故障数据识别<sup>\[4-9\]</sup>；在风电机组运行工况数据识别方面，采用支持向量机方法、*K*-means聚类算法、时间序列分割算法等智能模型识别复杂的运行工况数据<sup>\[9-12\]</sup>。

本章提出基于密度的聚类方法、随机森林决策树模型、基于随机行走改进的麻雀搜索算法优化联想神经网络模型、自动分割聚类识别方法，并应用于风电SCADA数据分析中异常数据筛选、数据异常与数据工况识别。

## 7.1 基于DBSCAN聚类法的异常数据样本识别

### 7.1.1 DBSCAN算法的相关概念

基于密度的聚类方法（density-based spatial clustering of applications with noise, DBSCAN）是一种基于密度的空间聚类算法，是一种无监督的智能学习方法。这类密度聚类算法一般假定类别可以通过样本分布的紧密程度决定。同一类别的样本，它们之间是紧密相连的，也就是说，在该类别任意样本周围不远处一定有同类别的样本存在。通过将紧密相连的样本划为一类，这样就得到了一个聚类类别。通过将所有各组紧密相连的样本划为各个不同的类别，就得到了最终的所有聚类类别结果。应用DBSCAN算法识别异常样本、噪声数据的思路是：对于数据簇中的每一个数据点，在给定的半径范围内都至少包括给定数目的点，将具有足够高密度的数据区域划为一类，而将那些没有进入簇类的数据（即孤立点）就被视为异常样本剔除。以下简要介绍DBSCAN算法的基本概念。

（1）*r*邻域：给定对象半径为*r*的区域内称为该对象的邻域，如图7.1(a)所示。

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><p><img class="content-image" / style="width:131px" src="../../images/p2-image446.png"></p>
<p>(a)</p></th>
<th style="text-align: center;"><p><img class="content-image" / style="width:131px" src="../../images/p2-image447.png"></p>
<p>(b)</p></th>
<th style="text-align: center;"><p><img class="content-image" / style="width:131px" src="../../images/p2-image448.png"></p>
<p>(c)</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

图7.1 DBSCAN算法概念

（2）核心点：如果给定对象*r*邻域内的样本点数大于等于邻域密度阈值(MP)，则称该对象为核心对象。例如，假设MP=6，则图中的点*P*则为核心点，如图7.1(b)所示。

（3）直接密度可达：若点*Q*在核心点*P*的*r*邻域内，则称*Q*是从*P*出发可以直接密度可达（通俗理解，*P*和*Q*是直系亲属），如图7.1(c)所示。例如，图中点*Q*在核心点*P*的*r*邻域内，则*P*和*Q*为直接密度可达。当然，圈内的其他5个点与*P*也是直接密度可达的。

（4）密度可达：若存在*P*<sub>1</sub>, *P*<sub>2</sub>,…, *P<sub>m</sub>*是一列核心点，*P<sub>i</sub>*<sub>+1</sub>是从*P<sub>i</sub>*出发关于*r*和MP直接密度可达的（即*P*<sub>2</sub>在*P*<sub>1</sub>的圈内，*P*<sub>3</sub>在*P*<sub>2</sub>的圈内，*P*<sub>4</sub>在*P*<sub>3</sub>的圈内，以此类推，*P<sub>m</sub>*在*P<sub>m</sub>*<sub>−1</sub>的圈内），则称点*P<sub>m</sub>*是从*P*<sub>1</sub>出发关于*r*和MP密度可达的，如图7.2所示。

（5）密度相连：如果样本集中存在点*O*，使得点*P<sub>m</sub>*、*Q<sub>m</sub>*是从*O*出发关于*r*和MP密度可达的，那么点*P<sub>m</sub>*、*Q<sub>m</sub>*是关于*r*和MP密度相连的，如图7.2所示。

<img class="content-image" src="../../images/p2-image449.png" style="width:558px" alt="">

图7.2 密度相连

从上可知，邻域半径和邻域密度阈值是DBSCAN聚类中二个关键参数。基于邻域半径和邻域密度阈值，由样本点的密度可达关系，以最大密度相连的样本集合称为聚类，而归类不到任何一个类簇的孤立点，就视为异常样本或者噪声样本点。

SCADA数据包括传感器异常和结冰等大量异常数据，采用 DBSCAN聚类方法进行识别，它通过设置密度阈值来识别聚类。根据文献\[13\]，将MP设为4，邻域半径计算如下：

<img class="formula-display" src="../../images/p2-image450.png" style="width:131px" alt=""> (7.1)

式中，*m*为实验数据集目标个数；*n*为实验空间维数；<img class="formula-inline" src="../../images/p2-image451.png" style="width:20px" alt="">为阶乘函数；*V* 是*m*个目标形成的实验空间体积，即

<img class="formula-display" src="../../images/p2-image452.png" style="width:131px" alt=""> (7.2)

这里，<img class="formula-inline" src="../../images/p2-image453.png" style="width:33px" alt="">为最大价值函数；<img class="formula-inline" src="../../images/p2-image454.png" style="width:31px" alt="">为是最小价值函数；*x<sub>i</sub>*是 *m*-by-*n*实验数据矩阵中第*i*列数据。

### 7.1.2 风电机组实例分析

图7.3(a)为某年度一风电机组全年的风速-功率散点图，剔除停机数据再利用 DBSCAN聚类处理后得到的数据如图7.3(b)所示。图7.4(a)为该年度风电机组全年的风速-转速散点图，图7.5(a)为2年后风电机组全年的风速-转速散点图。分别利用DBSCAN聚类处理得到前后两年该风电机组的风速-转速散点数据，如图7.4(b)和7.5(b)所示。

<table>
<colgroup>
<col style="width: 49%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><img class="content-image" / style="width:1093px" src="../../images/p2-image455.png">(a) DBSCAN聚类处理前</th>
<th style="text-align: center;"><p><img class="content-image" / style="width:1097px" src="../../images/p2-image456.png"></p>
<p>(b) DBSCAN聚类处理后</p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;">图7.3 DBSCAN聚类分析的风速-功率散点</td>
</tr>
<tr>
<td style="text-align: center;"><img class="content-image" / style="width:1092px" src="../../images/p2-image457.png">(a) DBSCAN聚类处理前</td>
<td style="text-align: center;"><img class="content-image" / style="width:1092px" src="../../images/p2-image458.png">(b) DBSCAN聚类处理后</td>
</tr>
<tr>
<td colspan="2" style="text-align: center;">图7.4 第一年DBSCAN聚类分析的风速-转速散点</td>
</tr>
<tr>
<td style="text-align: center;"><p><img class="content-image" / style="width:1092px" src="../../images/p2-image459.png"></p>
<p>(a) DBSCAN聚类处理前</p></td>
<td style="text-align: center;"><p><img class="content-image" / style="width:1092px" src="../../images/p2-image460.png"></p>
<p>(b) DBSCAN聚类处理后</p></td>
</tr>
<tr>
<td colspan="2" style="text-align: center;">图7.5 两年后DBSCAN聚类分析的风速-转速散点</td>
</tr>
</tbody>
</table>

## 7.2 基于随机森林的异常数据样本识别

### 7.2.1 随机森林算法的相关概念

随机森林(random forest, RF)是一种以决策树和投票（装袋）式算法结合的集成学习算法，可用于数据组合分类，还可用于回归算法模型的构建，是一种有监督的智能学习方法。 随机森林是一个包含多个决策树的[分类](https://baike.so.com/doc/10043458-10544400.html)器，可使用已知的正常数据样本和异常数据样本进行训练构建一个集成学习模型，模型能对未知数据样本进行正常或者异常识别。对于某些含有大量特征数据的样本识别，随机森林能够很好地学习，且对数据样本的分类效果很好。基于随机森林RF的异常数据样本识别原理，就是直接应用经过正常数据样本和异常数据样本训练而成的随机森林集成学习模型识别出异常数据样本予以剔除。以下介绍随机森林算法的基本概念。

决策树：一般是将特征分为两类，持续决策分类而呈树形结构，如图7.6所示。决策树也是一种基本的分类器，也是一种有监督的学习分类方法。

<img class="content-image" src="../../images/p2-image461.png" style="width:670px" alt="">

图7.6 决策树

分类器：给定一个样本的数据，判定这个样本属于哪个类别的算法。

分裂：在决策树的训练过程中，需要一次次的将训练数据集分裂成两个子数据集，这个过程就称为分裂。

特征：在分类问题中，输入到分类器中的数据称为特征。

待选特征：在决策树的构建过程中，需要按照一定的次序从全部的特征中选取特征。待选特征就是在目前的步骤之前还没有被选择的特征的集合。

分裂特征：按照待选特征的定义，每一次选取的特征就是分裂特征，因为选出的这些特征将数据集分成了一个个不相交的部分，所以称为分裂特征。

随机森林指的是利用多棵决策树对样本进行训练并预测的一种分类器，在其训练构建中实行样本数据的随机性选取和待选特征的随机选取，并且其输出的类别是由个别树输出的类别的众数而定。

随机森林是一种由数据驱动的非参数分类方法，在高维数据的分类问题上有较好的并行性和可扩展性。随机森林对于噪声和异常值由较好的容忍性，解决了决策树过拟合问题。

### 7.2.2 随机森林分类法识别流程

随机森林是利用自助采样对数据集进行抽样，并对每一个样本集计算训练一个决策树，每颗决策树都会对数据有一个分类结果，最终随机森林分类的结果由多个决策树分类后进行投票得出，如图7.7所示。

<img class="content-image" src="../../images/p2-image462.png" style="width:877px" alt="">

图7.7 随机森林分类识别示意图

决策树利用特征测试条件基于不纯性指标，将数据集分割成较小的数据集。不纯性是通过对实例的每个属性上的类别标签进行相关计算得出，对它影响最大的属性被选为分割数据的基准属性，并作为树的节点。基尼指数作为选择节点分裂特征的指标，基尼指数越小，集合中被选中的样本分错的概率越小，即纯度越高。假定样本集合为*D*，随机从集合*D*中抽取两个样本，其类别不一致的概率为基尼指数，表示为

$``$<img class="formula-inline" src="../../images/p2-image463.png" style="width:117px" alt=""> (7.3)

式中，<img class="formula-inline" src="../../images/p2-image464.png" style="width:13px" alt="">$`{\ \ \ \ \ \ p}_{k}`$表示选中的样本属于$`k`$类别的概率，<img class="formula-inline" src="../../images/p2-image465.png" style="width:35px" alt="">表示被分错的概率。如果用数据集*D*中参数特征<img class="formula-inline" src="../../images/p2-image466.png" style="width:8px" alt="">对数据集*D*进行划分，则参数<img class="formula-inline" src="../../images/p2-image467.png" style="width:8px" alt="">的基尼指数表示为

<img class="formula-display" src="../../images/p2-image468.png" style="width:135px" alt=""> (7.4)

式中，<img class="formula-inline" src="../../images/p2-image469.png" style="width:12px" alt="">表示样本集中*D*根据特征<img class="formula-inline" src="../../images/p2-image470.png" style="width:8px" alt="">划分的样本子集。从所有<img class="formula-inline" src="../../images/p2-image471.png" style="width:51px" alt="">（<img class="formula-inline" src="../../images/p2-image472.png" style="width:11px" alt="">表示数据集中第<img class="formula-inline" src="../../images/p2-image473.png" style="width:8px" alt="">个参数特征）筛选出最小的划分，这个划分点就是样本集合*D*的最优划分点。由此，决策树集成随机森林的步骤如下：

（1）采用自助采样法方法从原始训练集中，有放回的随机采样$`n`$个新的采样集，并构建$`n`$个分类决策树。每次未被抽到的样本组成袋外数据，可以用于对决策树的性能进行评估，计算模型的预测错误率，称为袋外数据误差。同时利用袋外数据可以对决策树的强度和决策树之间的相关性进行估计，进而得到随机森林泛化误差的估计。

（2）如果有*M*个特征，则在每一棵树的每个节点处随机抽取$`m_{try}`$个特征$`(m_{try},M)`$，然后在该节点处，计算每个特征的基尼指数，并按照最小原则，选择一个基尼指数最小的特征对该节点进行节点分裂，从而对数据集进行了分割。

（3）在构建模型过程中，对样本集进行了随机抽样；而且，对每一个样本集的特征也进行了随机选择，每棵树最大限度生长，不做剪枝。

（4）决策树组合在一起构成随机森林，用随机森林对待分类数据进行分类，预测结果由决策树的投票决定。

随机森林智能识别异常数据样本是一个二分类问题，通常根据混淆矩阵来评价识别模型的分类性能优劣，其中混淆矩阵是样本的真实标签和预测标签之间的关系矩阵，如下表7.1所示。TP代表正确的预测了该样本，且样本预测值是正样本；TN代表正确的预测了该样本，且样本预测值是负样本；FP代表真实样本是负样本，被预测成正样本；FN代表真实样本是正样本，被预测成负样本。

表7.1 混淆矩阵

<table>
<colgroup>
<col style="width: 36%" />
<col style="width: 30%" />
<col style="width: 32%" />
</colgroup>
<thead>
<tr>
<th rowspan="2" style="text-align: center;">实际情况</th>
<th colspan="2" style="text-align: center;">预测结果</th>
</tr>
<tr>
<th style="text-align: center;">正例</th>
<th style="text-align: center;">反例</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">正例</td>
<td style="text-align: center;">TP</td>
<td style="text-align: center;">FN</td>
</tr>
<tr>
<td style="text-align: center;">反例</td>
<td style="text-align: center;">FP</td>
<td style="text-align: center;">TN</td>
</tr>
</tbody>
</table>

根据混淆矩阵中四种预测结果之间的数量关系，可以计算获得正常数据样本被预测正确的概率、异常数据样本被预测错误的概率和所有被预测的样本预测正确的概率。前两者用来分析评价建模过程，后者作为评价模型的性能指标，一般称之为识别准确率。识别准确率用于评估随机森林模型的识别性能，数值越大，说明模型分类性能越好。在构建随机森林模型的过程中，决策树的个数、树的最大深度、树的根节点划分方法、随机选择的最大特征数等参数需要人工选择，这些称之为超参数的参数对模型识别性能有重要的影响，需要对这些超参数进行调节和优化，以便获得最优的超参数组合、性能优良的随机森林识别模型。

### 7.2.3 风电机组实例分析

> 1\. 数据样本集与模型构建

选取某风电场2MW直驱风电机组SCADA数据，数据集中的每个数据元组为10分钟平均值数据，时间尺度为两年。功率是风电机组最关键的特性，既可以作为判断风电机组正常运行的条件，也可以作为判断数据样本是否正常的条件，以便构造数据样本集。

随机森林识别模型构建中需要大量的具有正常或者异常数据样本标签的原始样本集，而且要求样本集中正常或者异常样本数量是平衡，以便获得性能优良的识别模型。原始样本集包括正常数据样本和异常数据样本，它们可以通过如下两个途径获得：一是根据现场实际运行状态，在SCADA数据样本标注出正常和异常样本；二是根据类似于前面拉依达准则、DBSCAN聚类识别方法，标注出正常数据样本和异常数据。这里，以功率作为判断数据样本是否正常的关键指标，基于SCADA数据分布，将功率数据在(*μ*−3*σ*, *μ*+3*σ*)外的数据样本称之为异常数据样本，而将功率数据在(*μ*−0.5*σ*, *μ*+1.5*σ*)内的数据样本作为正常数据样本。一般来说，就数据样本总量而言，风电机组SCADA系统原始样本集中异常数据样本远少于正常数据样本，这里采用欠采样方法对不平衡的数据样本集进行欠采样预处理，从大多数正常数据样本中选择最具代表性的样本进行训练，尽可能减少随机欠采样带来的信息丢失问题。最后，形成一个平衡的样本数据集，作为随机森林训练的数据学习，如图7.8所示。由图可以看出，经过欠采样方法处理后样本数据集中正常类别数据数量与异常类别数据数量比达到平衡。

在应用平衡数据集训练和构建随机森林模型过程中，将数据集划分为两部分，数据集中80%的数据作为训练集提供模型学习，数据集中20%的数据作为测试集提供模型测试并用来评估模型的精度。在构建随机森林模型的过程中，主要对影响随机森林精度较大的4个超参数做优化，分别为决策树的个数、树的最大深度、树的根节点划分方法、随机选择的最大特征数参数进行人工选择。综合考虑数据集大小、模型运行时间成本以及模型精度，通过对比分析，当决策树的个数为80、树深度为10时，模型识别准确率达到最高98.44%，并且模型泛化能力较好。

<div class="image-row"><img class="content-image" src="../../images/p2-image474.png" style="width:2205px" alt=""><img class="content-image" src="../../images/p2-image475.png" style="width:2205px" alt=""></div>

\(a\) 样本集不平衡 (b) 样本集平衡

图7.8 样本欠采样处理

> 3\. 识别结果分析

为了方便比较，首先应用DBSCAN方法，对原始SCADA数据进行低密度数据处理，得到风电机组风速和功率数据散点图，如图7.9(a)所示。从图可见，DBSCAN方法不能够识别出高密度的限功率数据和停机数据。然后，应用随机森林识别模型，选取风速、功率特征及其相关的发电机转速、转矩、频率、桨距角和环境温度等特征数据，对风电机组SCADA数据进行智能识别得到正常数据集，如图 7.9(b)所示，从图可以看出得到了较为满意的识别效果，能够识别出DBSCAN方法不能识别出的高密度限功率数据和停机数据。

<div class="image-row"><img class="content-image" src="../../images/p2-image476.png" style="width:1360px" alt=""><img class="content-image" src="../../images/p2-image477.png" style="width:1347px" alt=""></div>

\(a\) 判别原始数据集后的风速功率散点图 (b) 正常数据集中风速功率散点图

图 7.9 DBSCAN和RF两种模型识别结果

风电机组部件温度是SCADA数据中重要组成部分，影响因素较多而且机理非常复杂。以主轴承温度、发电机定子温度数据为例，将原始数据集和筛选后的正常数据集进行对比分析，如图7.8所示。根据风电机组工作机理，当风速大于切入风速时，风电机组处于发电状态，随着风速的增加，风轮机械能增大，发电机转矩增大，运行频率增加，进而主轴承温度和发电机定子温度也随之增加，在风速-温度的散点图上应呈现出这种趋势性，图7.10(a)和(b)分别为数据筛选前SCADA系统原始数据集中一年的主轴承温度和发电机定子温度的散点图。从图可以看出，在温度主数据带下方，当风速大于切入风速3m/s时，存在着多条横向的温度数据，这是因为在这一年中，存在着风速高于切入风速，风电机组不发电或因故障停机的情况，属于异常数据。这里，采用随机森林RF分类识别方法剔除异常数据样本后获得的正常数据集中主轴承温度和发电机定子温度数据散点，如图7.10(c)和(d)所示。从图可以看出，由于一年四季中温度的差异，主轴承和发电机定子的正常温度主数据带在上下方向上具有一定的宽度，同时由于一年之中，中风速段的风出现概率要多于高风速段的风出现概率，随着风速增加，主数据带上下方向上宽度变小；当风速高于切入风速，随着风速的增加，温度数据也呈现出增加的趋势性。这些都表明了随机森林RF分类方法对于风电机组温度数据有着优良的数据识别筛选效果。

<div class="image-row"><img class="content-image" src="../../images/p2-image478.png" style="width:1309px" alt=""><img class="content-image" src="../../images/p2-image479.png" style="width:1304px" alt=""></div>

\(a\) 数据筛选前主轴承温度散点图 (b) 数据筛选前发电机定子温度散点图

<div class="image-row"><img class="content-image" src="../../images/p2-image480.png" style="width:1309px" alt=""><img class="content-image" src="../../images/p2-image481.png" style="width:1304px" alt=""></div>

\(c\) 数据筛选后主轴承温度散点图 (d) 数据筛选后发电机定子温度散点图

图7.10 风电机组温度数据随机森林RF数据识别筛选效果

## 7.3 基于RWSSA-AANN的风电机组风速异常数据识别

风电SCADA数据来源于风电机组不同位置的传感器，其运行状态异常不但直接影响到数据正确性和质量，而且会对风电机组正常运行产生负面影响，甚至危及设备和人员的安全。开展基于SCADA异常数据识别，对风电机组正常运行和SCADA数据处理具有重要意义。统计表明，风电机组部件故障中传感器故障超过14%，而与传感器相关的系统故障也超过40%。一般来说，风电机组本体运行状态异常、风电机组传感器运行状态异常都将导致SCADA数据异常。若果风电机组本体运行状态正常，其传感器运行状态识别与SCADA异常数据识别就成为了同一个问题。本节以风电机组风速计及其SCADA风速数据为例，采用动态时间规整算法（dynamic time warping，DTW）选择一组风速强相关的风电机组作为机群；然后建立基于随机行走改进的麻雀搜索算法进行自动优化联想神经网络(random walk improved sparrow search algorithm-autoassociative artificial neural networks，RWSSA-AANN)模型，机群中的风电机组台数即为模型的输入节点数，模型的输入为各风电机组的实际风速，模型的输出为风速的预测值，利用模型识别风电机组风速计异常状态及其引起的风速异常数据样本。

### 7.3.1 风电场的风电机组分类

> 1\. 风速相关性评价

DTW是一种衡量两个时间序列之间的相似度的算法，通过把时间序列进行延伸和缩短，来计算两个时间序列性之间的相似性。如图7.11所示，实线代表时间序列，虚线表示两个时间序列之间的相似点。设两个时间序列分别为*X*和*Y*，其长度分别为\|*X*\|和\|*Y*\|，路径定义为*W*。归整路径的形式*W*=*W*<sub>1</sub>,*W*<sub>2</sub>,…,*W<sub>K</sub>*<sub>，</sub>其中Max(\|*X*\|,\|*Y*\|)≤*K*≤\|*X*\|+\|*Y*\|。*W<sub>k</sub>*的形式为(*i,j*)，其中*i*表示的是*X*中的*i*坐标，*i*=1,2,…,\|*X*\|，*j*表示的是*Y*中的*j*坐标，*j*=1,2,…,\|*Y*\|。归整路径*W*必须从*W*<sub>1</sub>=(1,1)开始，到*W<sub>K</sub>*=(\|*X*\|,\|*Y*\|)结尾，以保证*X*和*Y*中的每个坐标都在*W*中出现，并且*W*(*i*, *j*)的*i*和*j*必须是单调增加的，使图7.11中的虚线不会相交。通过DTW计算这些相似点之间的距离和，它来衡量两个时间序列之间的相似性。

距离最短的归整路径表达式如式（7.5）所示，表示当前格点距离Dist(*i*, *j*)，也就是点*i*和*j*的欧式距离（相似性）与可以到达该点的最小的邻近元素的累积距离之和，用符号*L*表示：

<img class="formula-display" src="../../images/p2-image482.png" style="width:260px" alt=""> （7.5）

<img class="content-image" src="../../images/p2-image483.png" style="width:3112px" alt="">

图7.11 两个时间序列之间的相似性

> 2\. 风电机组群确定

数据来源为某风电公司提供的23台风电机组的SCADA风速数据，风速测量采用转杯式机械旋转风速仪，其测量范围为0~50m/s，精确度为±2%测量值，分辨率为\<0.02 m/s。数据记录了该风场10000组正常数据。把每台风电机组的风速看成是一个时间序列，通过计算风电机组风速之间的*L*值得到风电机组群。把1号风电机组的风速作为基准序列*X*，其他风电机组的风速作为序列*Y*，分别计算*X*和*Y*之间*L*的平均值，*L*越小表示相似性越高，*L*的平均值如表7.2所示。

表7.2 *L*平均值

| 编号 |  2号  |  3号  |  4号  |  5号  |  6号  |  7号  |  8号  |  9号  |
|:----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| *L*  | 0.516 | 0.750 | 0.345 | 0.452 | 0.670 | 0.945 | 1.402 | 0.963 |
| 编号 | 10号  | 11号  | 12号  | 13号  | 14号  | 15号  | 16号  | 17号  |
| *L*  | 0.885 | 1.095 | 1.108 | 1.049 | 1.256 | 1.318 | 1.226 | 2.077 |
| 编号 | 18号  | 19号  | 20号  | 21号  | 22号  | 23号  |       |       |
| *L*  | 1.729 | 1.244 | 1.698 | 1.255 | 2.001 | 1.473 |       |       |

从表7.2中可以看出，1号与2、3、4、5、6、7、9、10号风电机组*L*值相对较小，因此对这几台风电机组进一步分析，表3.2为所选各风电机组之间*L*的平均值。从表7.3中把*L*的平均值为0.8的范围内1号、2号、3号、4号、5号、6号风电机组作为一个风电机组群。

表7.3 各风电机组之间的*L*平均值

<table style="width:100%;">
<colgroup>
<col style="width: 4%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 12%" />
<col style="width: 10%" />
<col style="width: 10%" />
<col style="width: 10%" />
<col style="width: 10%" />
<col style="width: 10%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th rowspan="2" style="text-align: center;"><p>编</p>
<p>号</p></th>
<th colspan="9" style="text-align: center;"><em>L</em>平均值</th>
</tr>
<tr>
<th style="text-align: center;">1</th>
<th style="text-align: center;">2</th>
<th style="text-align: center;">3</th>
<th style="text-align: center;">4</th>
<th style="text-align: center;">5</th>
<th style="text-align: center;">6</th>
<th style="text-align: center;">7</th>
<th style="text-align: center;">9</th>
<th style="text-align: center;">10</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">1</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0.516</td>
<td style="text-align: center;">0.750</td>
<td style="text-align: center;">0.345</td>
<td style="text-align: center;">0.452</td>
<td style="text-align: center;">0.670</td>
<td style="text-align: center;">0.945</td>
<td style="text-align: center;">0.963</td>
<td style="text-align: center;">0.885</td>
</tr>
<tr>
<td style="text-align: center;">2</td>
<td style="text-align: center;">0.516</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0.761</td>
<td style="text-align: center;">0.466</td>
<td style="text-align: center;">0.558</td>
<td style="text-align: center;">0.677</td>
<td style="text-align: center;">1.091</td>
<td style="text-align: center;">0.922</td>
<td style="text-align: center;">0.869</td>
</tr>
<tr>
<td style="text-align: center;">3</td>
<td style="text-align: center;">0.750</td>
<td style="text-align: center;">0.761</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0.753</td>
<td style="text-align: center;">0.745</td>
<td style="text-align: center;">0.675</td>
<td style="text-align: center;">0.736</td>
<td style="text-align: center;">0.990</td>
<td style="text-align: center;">1.031</td>
</tr>
<tr>
<td style="text-align: center;">4</td>
<td style="text-align: center;">0.345</td>
<td style="text-align: center;">0.466</td>
<td style="text-align: center;">0.753</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0.466</td>
<td style="text-align: center;">0.641</td>
<td style="text-align: center;">1.001</td>
<td style="text-align: center;">0.885</td>
<td style="text-align: center;">0.868</td>
</tr>
<tr>
<td style="text-align: center;">5</td>
<td style="text-align: center;">0.452</td>
<td style="text-align: center;">0.558</td>
<td style="text-align: center;">0.745</td>
<td style="text-align: center;">0.466</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0.721</td>
<td style="text-align: center;">1.146</td>
<td style="text-align: center;">0.939</td>
<td style="text-align: center;">0.856</td>
</tr>
<tr>
<td style="text-align: center;">6</td>
<td style="text-align: center;">0.670</td>
<td style="text-align: center;">0.677</td>
<td style="text-align: center;">0.675</td>
<td style="text-align: center;">0.641</td>
<td style="text-align: center;">0.721</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0.810</td>
<td style="text-align: center;">0.869</td>
<td style="text-align: center;">0.837</td>
</tr>
<tr>
<td style="text-align: center;">7</td>
<td style="text-align: center;">0.945</td>
<td style="text-align: center;">1.097</td>
<td style="text-align: center;">0.736</td>
<td style="text-align: center;">1.001</td>
<td style="text-align: center;">1.146</td>
<td style="text-align: center;">0.810</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">1.016</td>
<td style="text-align: center;">1.136</td>
</tr>
<tr>
<td style="text-align: center;">9</td>
<td style="text-align: center;">0.963</td>
<td style="text-align: center;">0.922</td>
<td style="text-align: center;">0.990</td>
<td style="text-align: center;">0.885</td>
<td style="text-align: center;">0.939</td>
<td style="text-align: center;">0.869</td>
<td style="text-align: center;">1.016</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0.656</td>
</tr>
<tr>
<td style="text-align: center;">10</td>
<td style="text-align: center;">0.885</td>
<td style="text-align: center;">0.869</td>
<td style="text-align: center;">1.031</td>
<td style="text-align: center;">0.868</td>
<td style="text-align: center;">0.856</td>
<td style="text-align: center;">0.837</td>
<td style="text-align: center;">1.136</td>
<td style="text-align: center;">0.656</td>
<td style="text-align: center;">0</td>
</tr>
</tbody>
</table>

### 7.3.2 RWSSA-AANN建模

自联想神经网络模型(autoassociative artificial neural networks, AANN)虽然在风电机组传感器故障诊断领域应用较少，但在其他领域的传感器故障诊断上得到广泛应用。但采用未优化的AANN模型会出现局部最优问题，需要对AANN模型参数进行优化，提升其性能。而麻雀搜索算法（sparrow search algorithm, SSA）可以提高AANN网络性能，因为SSA在准确性，收敛速度，稳定性和鲁棒性等方面表现较好，同时在高维运算时，能很好的提高其正确率，减少误差。在麻雀算法搜索之后用随机游走（random walk, RW）来改进，通过改进麻雀的最优位置，实现随机游走对最优麻雀进行扰动，提高其搜索性。在随机游走开始迭代阶段，其边界点相对较大，有助于改善麻雀算法的全局寻优能力，在迭代多次后，游走边界缩小了，可以改善算法的最优位置局部搜索性，提高预测模型的性能，增加了准确度。

> 1\. AANN模型

自联想神经网络由五层组成，主要包括输入层、映射层、瓶颈层、解映层和输出层。其模型如图7.12所示。AANN模型的特点是输入数据与输出数据为近似值，且维数相同，映射层和解映层采用非线性传递函数（S型）来进行映射。映射层、解映层和瓶颈层的节点数通过不停的尝试确定，评价指标可以是运行时间、误差值等。其工作过程描述为，输入数据经过映射层，映射到高维度空间中，然后通过瓶颈层进行压缩，瓶颈层的节点数是希望尽可能的少，再通过解映层进行解映，并通过重建数据从原始空间维度输出来。

<img class="content-image" src="../../images/p2-image484.png" style="width:971px" alt="">

图7.12 AANN模型结构图

图7.12中，*ω<sub>i </sub>*(*i*=1,2,3,4)表示各层之间的网络权值，*b<sub>j</sub>*(*j*=1,2,3,4) 表示为各层的偏置参数。可以得到每一层的输出向量表达式：

<img class="formula-display" src="../../images/p2-image485.png" style="width:120px" alt=""> (7.6)

<img class="formula-display" src="../../images/p2-image486.png" style="width:119px" alt=""> (7.7)

<img class="formula-display" src="../../images/p2-image487.png" style="width:122px" alt=""> (7.8)

<img class="formula-display" src="../../images/p2-image488.png" style="width:103px" alt=""> (7.9)

根据式（7.6）~式（7.9）可以得到AANN网络得到输出与输入的表达式：

> <img class="formula-inline" src="../../images/p2-image489.png" style="width:348px" alt=""> (7.10)

式中，*f* <sup>1</sup>、*f* <sup>2</sup>、*f* <sup>3</sup>、*f* <sup>4</sup>分别为映射层、瓶颈层、解映层和输出层的传递函数；*O<sub>e</sub>*表示的输出值，*e*=1,2,…,*n*；*i<sub>z</sub>*表示为输入值。

*f* <sup>1</sup>和*f* <sup>3</sup>分别为映射层、解映层的传递函数，采用logsig函数，其表达式为

<img class="formula-display" src="../../images/p2-image490.png" style="width:72px" alt=""> (7.11)

*f* <sup>2</sup>为瓶颈层的传递函数，采用tansig函数，其表达式为

<img class="formula-display" src="../../images/p2-image491.png" style="width:83px" alt=""> (7.12)

*f* <sup>4</sup>为输出层的传递函数，采用purelin函数，其表达式为

<img class="formula-display" src="../../images/p2-image492.png" style="width:49px" alt=""> (7.13)

> 2\. SSA模型

麻雀通常是群居的鸟类，它的能力主要是捕食和繁殖下一代，而这两种行为类似于捕食者和繁殖者，麻雀算法建立模型的规则如下所述。设麻雀的位置矩阵表示为<sup>\[14\]</sup>

<img class="formula-display" src="../../images/p2-image493.png" style="width:121px" alt=""> (7.14)

式中，*i*是麻雀的数量；*j*是待优化变量的维数。

所有麻雀的适应度值可以表示为如下形式：

<img class="formula-display" src="../../images/p2-image494.png" style="width:139px" alt=""> (7.15)

式中，*f*表示适应度值。

在每次迭代的过程中，发现者的位置更新表达式为

<img class="formula-display" src="../../images/p2-image495.png" style="width:139px" alt=""> (7.16)

式中，*t*表示当前迭代位置，*b*=1,2,…, *j*；<img class="formula-inline" src="../../images/p2-image496.png" style="width:22px" alt="">表示在迭代位置处于*t*时第*a*个麻雀所在第*b*维；<img class="formula-inline" src="../../images/p2-image497.png" style="width:10px" alt="">是一个\[0,1\]范围之内的随机数；*P*<sub>2</sub>表示警报值，它的范围是\[0,1\]；*T*是表示安全阈值，其范围为\[0.5,1\]；*n*为当前迭代次数；*Q*是服从正态分布的随机数；<img class="formula-inline" src="../../images/p2-image498.png" style="width:9px" alt="">表示1×*j*的矩阵。

当<img class="formula-inline" src="../../images/p2-image499.png" style="width:29px" alt="">表示麻雀群周边没有威胁者，捕食者可以进入大范围的搜索模式；当<img class="formula-inline" src="../../images/p2-image500.png" style="width:29px" alt="">时表示周边有威胁者，所有麻雀都需要迅速飞到其他安全区域去。搜寻者位置更新的表达式为

<img class="formula-display" src="../../images/p2-image501.png" style="width:189px" alt=""> (7.17)

式中，<img class="formula-inline" src="../../images/p2-image502.png" style="width:17px" alt="">是表示该群麻雀中最不理想的位置；<img class="formula-inline" src="../../images/p2-image503.png" style="width:16px" alt="">是捕食者占据的最佳位置；<img class="formula-inline" src="../../images/p2-image504.png" style="width:70px" alt="">，*A*为一个1×*j*的矩阵，动态分配为-1或1。

当*a* \> *i*/2时，表明适应性较差的第*a*个搜寻者最有可能被饿死。在进行训练时，把整个种群中10%~20%的麻雀定义为警惕性高的麻雀，并且自动生成它们的初始位置，即

<img class="formula-display" src="../../images/p2-image505.png" style="width:188px" alt=""> (7.18)

式中，<img class="formula-inline" src="../../images/p2-image506.png" style="width:23px" alt="">是群体的中心位置，代表着最佳值；<img class="formula-inline" src="../../images/p2-image507.png" style="width:11px" alt="">是一个参数，表示控制步长的大小；*k*的值是任意得到的，其范围在\[-1,1\]；*f<sub>a</sub>*是当前麻雀的适应度值；*f<sub>g</sub>*和*f<sub>w</sub>*是当前麻雀的最佳适应度值和最差适应度值。

当*f<sub>a </sub>*= *f<sub>w</sub>*时，若不加*ε*值，则会使得整个分母为0，因此为了防止这种情况的出现，在分母中加一个非常小的值。<img class="formula-inline" src="../../images/p2-image508.png" style="width:33px" alt="">表示目前这只麻雀离群体的位置有点远，基本上处于群体的边缘外部；<img class="formula-inline" src="../../images/p2-image509.png" style="width:33px" alt="">表示位置中心的麻雀意识到有危险，要向其他地方靠近。

> 3\. RW模型

随机游动过程的数学表达式为

<img class="formula-display" src="../../images/p2-image510.png" style="width:220px" alt=""> (7.19)

式中，<img class="formula-inline" src="../../images/p2-image511.png" style="width:24px" alt="">是随机游动步长的集合；cussum是计算出的累积总和；*t*是随机行走步数；*r*(*t*)是一个随机函数，表达式如下：

<img class="formula-display" src="../../images/p2-image512.png" style="width:92px" alt=""> (7.20)

式中，rand∈\[0,1\]。

由于可行区域中存在边界，式（7.19）不能直接用于更新麻雀的位置。为了确保在可行区域内的随机行走，需要由下式对其进行归一化：

<img class="formula-inline" src="../../images/p2-image513.png" style="width:138px" alt=""> （7.21)

式中，<img class="formula-inline" src="../../images/p2-image514.png" style="width:11px" alt="">是第*i*维变量随机游动的最小值；*H<sub>i</sub>*是第*i*维变量随机游动的最大值；<img class="formula-inline" src="../../images/p2-image515.png" style="width:12px" alt="">是第*t*次迭代中第*i*维变量的最小值；<img class="formula-inline" src="../../images/p2-image516.png" style="width:14px" alt="">是第*t*次迭代中*i*维变量的最大值。

> 4\. RWSSA-AANN建模流程

AANN是前馈神经网络，它通过大量的数据进行训练而成。训练过程中误差函数自动调整隐含层各节点传递函数的权值和偏置参数，而权值和偏置参数的取值关系到整个网络性能，其值是随机产生的，因此每次的结果都不一样。采用随机游走改进的麻雀搜索算法（random walk improved sparrow search algorithm，RWSSA）优化AANN权重和偏移参数，然后对网络进行训练，将大大提高神经网络的性能，避免局部最优问题。RWSSA在精度、收敛速度、稳定性和鲁棒性方面优于遗传算法（genetic algorithm，GA）、粒子群优化算法（particle swarm optimization algorithm，PSO）等。

通过设置AANN模型参数，采用RWSSA寻找出AANN神经网络的最优权值和偏置参数，并应用到已经建好的AANN网络中去，得到RWSSA-AANN模型，模型建立流程如下。

（1）数据处理。选取风电机组正常运行的SCADA历史数据，并进行标准化处理，将风速归化到\[0,1\]区间，以消除模型训练过程中每个数据之间绝对值差异的影响。

（2）设置AANN网络结构。输入输出层的节点数为风电机组群数6。隐藏层节点数不同对训练结果影响很大，其值根据不同节点训练结果的MSE值、运行时间和降噪水平（reduce noise level，RNL）来确定，其中，MSE值的计算表达式如下：

<img class="formula-display" src="../../images/p2-image517.png" style="width:127px" alt=""> （7.22）

式中，*m*为训练（或测试）样本数量；*n*为训练（或测试）的输入维数；<img class="formula-inline" src="../../images/p2-image518.png" style="width:12px" alt="">表示第*j*个训练/测试样本的第*i*个网络目标输入值；<img class="formula-inline" src="../../images/p2-image519.png" style="width:13px" alt="">是第*j*个训练/测试样本的第*i*个网络预测输出值，二者的值越小，模型的精度就越高。

降噪水平RNL如下计算：

<img class="formula-display" src="../../images/p2-image520.png" style="width:106px" alt=""> （7.23）

式中，<img class="formula-inline" src="../../images/p2-image521.png" style="width:14px" alt="">是输出值的平均噪声方差；<img class="formula-inline" src="../../images/p2-image522.png" style="width:14px" alt="">是输入值的平均噪音方差。

使用列文伯格-马夸尔特(Levenberg-Marquardt)算法作为训练方法，将目标设置为0.00001，时间设置为100s，学习率设置为0.01。将 *R*设为输入层节点的数量，将*S*<sub>1</sub>设为映射层节点的数量，将*S*<sub>2</sub>设为瓶颈层节点的数量，*S*<sub>3</sub>为解映层节点个数，*T*为输出层节点个数，模型结构为*R*-*S*<sub>1</sub>-*S*<sub>2</sub>-*S*<sub>3</sub>-*T*，不同网络结构的训练结果如表7.4所示，综合分析选用模型结构为6-23-5-23-6。

表7.4 不同网络结构的训练结果

| 结构 | MSE/(m/s)<sup>2</sup> | Time/s | RNL |
|----|:--:|:--:|:--:|
| 6-17-4-17-6 | 9.490<img class="formula-inline" src="../../images/p2-image523.png" style="width:19px" alt=""> | 187.229 | 32.62% |
| 6-15-3-15-6 | 9.764<img class="formula-inline" src="../../images/p2-image523.png" style="width:19px" alt=""> | 191.332 | 28.34% |
| 6-23-5-23-6 | 9.602<img class="formula-inline" src="../../images/p2-image523.png" style="width:19px" alt=""> | 35.329 | 36.44% |
| 6-19-5-19-6 | 9.658<img class="formula-inline" src="../../images/p2-image523.png" style="width:19px" alt=""> | 55.0419 | 35.08% |
| 6-19-4-19-6 | 9.618<img class="formula-inline" src="../../images/p2-image523.png" style="width:19px" alt=""> | 46.001 | 33.72% |

（3）定义RWSSA算法的维数*k*。搜索空间维数由下式计算：

<img class="formula-display" src="../../images/p2-image524.png" style="width:230px" alt=""> （7.24）

把模型结构参数代入式（7.24），可以算得维数为563。

（4）设置RWSSA的参数。根据多次实验选取迭代次数为30次；种群规模为50只；捕食者的比例为20%；安全阈值*T*<sub>1</sub>取0.8；设意识到危险的麻雀数量为种群的20%。

（5）确定RWSSA适应值。使用设置的参数，迭代计算RWSSA算法，并在每次迭代和排序结束时更新最佳适应值。

（6）位置更新。更新捕食者麻雀位置，更新加入麻雀位置，更新警戒者麻雀位置，计算适应度值并利用随机游走更新麻雀位置。

（7）最优解生成。是否满足停止条件，满足条件得到最优适应度值及全局最优位置集，得到最优权值和阈值。若果不满足条件，重复执行第6步。

（8）优化AANN网络。把取得的最优权值和阈值赋予给式（7.10），提高AANN模型的预测精度。

### 7.3.3 风速计故障识别

> 1\. 故障阈值设定

AANN模型的输入参数为风电机组群中6台风电机组的风速。假设*i*<sub>1</sub>~*i*<sub>6</sub>表示6个风速仪的实际数据输入，*o*<sub>1</sub>~*o*<sub>6</sub>表示模型的6个预测输出，当输入无故障时，按照AANN模型的特点，得到的输出数据与输入数据相等，即误差平方和（sum squares error，SSE）理想值为0，如式(7.21)所示，但因为误差等因素的存在SSE只能接近于0。通过数据筛选得到13000组数据分成12000个训练数据和1000个测试数据，当模型训练好之后，利用测试数据进行测试，然后把每次检测得到的SSE值组成一个序列，这样得到全部1000组数据的SSE值。由于AANN模型内部的非正交特性，当某一个输入值异常时，会影响到整个模型的输出值，算出的SSE值也会变化较大。

<img class="formula-display" src="../../images/p2-image525.png" style="width:149px" alt=""> (7.25)

式中，*i*为输入AANN模型的值；*o*为AANN的输出值；*j*为模型输入参数个数。判断风速仪的状态是根据得到的SSE序列值和阈值的关系来确定的，阈值的选取可以根据检测时间、可靠性、灵敏性等来确定，根据训练结果求得SSE值，取 95%置信限下对应值作为故障判别阈值，值为0.3373。当SSE序列中值超过阈值时，判断状态异常。

> 2\. 模拟故障设定与识别

通过模拟故障诊断，可以有效验证模型是否能够检测到设定的运行状态，并根据检测和故障设置判断模型是否满足要求。只有当模型能够有效地检测模拟故障时，模型才能检测实际SCADA数据并获得正确的结果。

模拟风速仪异常状态是在正常的1000组测试数据中注入故障数据，通过RWSSA-AANN模型来实现识别。模拟故障类型主要有固定偏差故障、失效故障和漂移故障。

图7.13为风电机组发生固定偏差故障图，故障设置为3号风电机组第600~720个数的时间段加入幅值为0.8m/s的偏差。如图7.13(c)所示，3号风电机组风速仪发生了偏差故障，从600个数据也就是5月30日17点15分出现偏差故障，对于偏差故障能快速检测出来，无故障风电机组风速仪的SSE值除少数点外基本在检测阈值以下。

图7.14为风电机组发生失效故障图，故障设置为4号风电机组第200~350个数的时间段风速缓慢降到2m/s。从图7.14(d)看出4号风电机组风速仪发生故障，在第203个数据即5月27号23点05分左右，其故障被检测出来。而其他无故障风速仪的SSE值除几个点外基本保持在检测阈值以下。

图7.15为风电机组发生漂移故障，故障设置是在5号风电机组第400~580个数的时间段注入增益为0.02的漂移。图7.15(e)中曲线可以看出为风速仪漂移故障，在5号风电机组风速仪在第400个点，即5月29号7点55分开始出现单个漂移故障，由于漂移变化很小，在第414个数据其故障幅度达到最小检测值时被检测出来，即5月29号10点15分左右，而其他无故障传感器的SSE值基本保持在检测阈值以下。

<img class="content-image" src="../../images/p2-image526.png" style="width:3804px" alt="">

图7.13 风电机组风速仪发生固定偏差故障图

<img class="content-image" src="../../images/p2-image527.png" style="width:3930px" alt="">

图7.14 风电机组风速仪发生失效故障

<img class="content-image" src="../../images/p2-image528.png" style="width:3773px" alt="">

图7.15 风电机组风速仪发生漂移故障

### 7.3.4 风电机组实例分析

> 1\. 数据准备

实际数据由某风电公司提供，包括共五年的10分钟数据。因此，每年对应的每台风电机组的数据由52560组数据组成。但由于某些原因，并非每年的数据都有52560组，中间某些时间间隔的数据出现了缺失。为了保证测试的可靠性，基于缺失值前后的数据，使用拉格朗日插值法来补充缺失数据。

> 2\. 风速计故障数据识别

利用训练好的模型识别处理过的数据，当识别出故障状态时，充分利用无故障风电机组风速仪风速、功率关系等进行验证识别结果正确与否。

利用模型识别1~6号风电机组风速仪失效故障，其结果如图7.16所示。在图7.16(a)中，1号风电机组风速仪在第25304个数。图7.16(e)中曲线显示5号风电机组风速仪在第25339个数。从对应的实际风速曲线可以明显的看出上述时间段，风速仪发生了失效故障。由于运行过程中，各种因素对风速仪的影响，其他无故障风速仪有少数点超过了阈值，可以不作处理。

<img class="content-image" src="../../images/p2-image529.png" style="width:4141px" alt="">

图7.16 风电机组风速仪失效状态图

图7.17为某年度1~6号风电机组风速仪状态识别图。如图7.17(e)所示，3号风电机组风速仪在第42459个点，识别出发生故障，通过曲线可以近似认为是固定偏差故障。图7.17(g)为对应的3号风电机组功率曲线图，理论功率为风速通过三次样条插值法拟合而成的功率，图7.17(g)看出该时段理论功率持续大于实际功率，而其他5台未发生故障的风电机组功率曲线图，同时段实际功率是大于理论功率的。

图7.18为其他年度1~6号风电机组风速仪状态识别图。如图7.18(e)所示，3号风电机组风速仪在第16035个点，识别出发生故障，通过曲线可以近似认为是漂移故障。图7.18(g)为对应的3号风电机组功率曲线图，持续出现理论功率大于实际功率的情况，与其他5台风电机组同时段的情况不同。在图7.18(g)中，实际功率与理论功率的差值与图7.18(e)中3号风电机组的风速SSE值基本符合风速与功率的拟合值关系。

<img class="content-image" src="../../images/p2-image530.png" style="width:4318px" alt="">

图7.17 某年度风电机组风速仪状态图

<img class="content-image" src="../../images/p2-image531.png" style="width:3962px" alt="">

图7.18 不同年度风电机组风速仪状态图

> 3\. 三种方法比较分析

为了分析评价RWSSA-AANN模型的精度和准确性，采用AANN、GA-AANN、PCA和RWSSA-AANN三种模型进行对比，得到每一种模型的MSE值，如表7.5所示。结果表明，RWSSA-AANN模型的MSE值都小于AANN、GA-AANN和PCA模型。RWSSA-AANN模型精度高、误差小，有利于提高风电机组风速仪故障数据识别的准确性。

表7.5 三种模型MSE值比较

<table>
<colgroup>
<col style="width: 37%" />
<col style="width: 27%" />
<col style="width: 34%" />
</colgroup>
<thead>
<tr>
<th rowspan="2" style="text-align: center;">算法模型</th>
<th colspan="2" style="text-align: center;">MSE(m/s)<sup>2</sup></th>
</tr>
<tr>
<th style="text-align: center;">2014/NO4</th>
<th style="text-align: center;">2016/NO3</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">AANN</td>
<td style="text-align: center;">0.0254</td>
<td style="text-align: center;">1.28<img class="formula-inline" / style="width:21px" src="../../images/p2-image532.png"></td>
</tr>
<tr>
<td style="text-align: center;">GA-AANN</td>
<td style="text-align: center;">0.055</td>
<td style="text-align: center;">7.07<img class="formula-inline" / style="width:21px" src="../../images/p2-image533.png"></td>
</tr>
<tr>
<td style="text-align: center;">PCA</td>
<td style="text-align: center;">0.056</td>
<td style="text-align: center;">1.47<img class="formula-inline" / style="width:21px" src="../../images/p2-image532.png"></td>
</tr>
<tr>
<td style="text-align: center;">RWSSA-AANN</td>
<td style="text-align: center;">0.0048</td>
<td style="text-align: center;">5.51<img class="formula-inline" / style="width:21px" src="../../images/p2-image533.png"></td>
</tr>
</tbody>
</table>

## 7.4 基于TICC算法的风电机组SCADA数据工况识别

面对复杂多变的风资源环境，风电机组设计了多种运行工况以便最大限度获取风能和减少损伤。风电机组不同的工况有着不同的控制模式和运行机制，SCADA数据是表征风电机组运行参数和状态变化的数值。准确识别SCADA数据所处的风电机组工况，是深入理解风电机组运行规律、评估风电机组运行状态的前提。针对风电机组高维SCADA时序数据的工况识别问题，提出一种基于Toplize逆协方差聚类（toplize inverse covariance clustering，TICC）的风电机组运行工况自动分割聚类识别方法。首先，从SCADA数据中选取风速、轮毂转速和桨距角等少量特定参数作为初始分割聚类对象，分析特定参数的运行规律，确定风电机组正常运行的六种工况。然后，选取一段特定参数的历史数据，利用TICC算法进行离线聚类分割，获得聚类的最优特征参数；将最优特征参数作为TICC算法的输入，对新的特定参数时间序列数据进行聚类。最后根据特定参数时间序列的聚类结果，对未进行分割的SCADA时序数据进行聚类处理、实现数据工况识别。

### 7.4.1 风电机组运行工况分析

由风力发电机的运行控制规律可知，理论风速和功率、风速和轮毂转速（发电机转速与轮毂转速运行规律一致，可等效替代）、风速和桨距角存在一定的函数关系。以某2MW双馈式风电机组为例，切入风速为3m/s，切出风速为25m/s，额定风速为12m/s，它的理论运行控制曲线如图7.19所示。风速3~5m/s区间为启动区，风电机组以设定的初始转速运行，开始进行并网发电。随着风速的增加，转速不断增加，该阶段主要为了控制追踪风能系数最优曲线的工作点，捕获最大风能，将其称为最大风能追踪区。在风速为9m/s时，由于风电机组的旋转部件受到机械强度的限制，发电机达到额定转速，以后直到达到最大功率点12 m/s，转速将保持不变，桨距角继续增大，该区域为恒转速区。在最大风能追踪区与恒转速区，存在一个短暂的过渡区域，主要为降低转速的增速，使得风电机组运行状态平稳，该区域称为恒转速过渡区。风速达到额定转速12m/s时，风速继续增大，桨距角不断增加，发电机转速继续维持额定转速不变，功率保持在额定功率，直至风速超过切出风速，该区域称为恒功率区。在恒功率区与恒转速区之间存在一个过渡区域，主要保证风电机组在运行状态转化时，减少风轮的机械应力和输出功率的波动，减少功率变化对传动链的瞬态冲击。根据上面的分析，综合风速-功率，风速-转速和风速-桨距角的控制规律（不同MW级风电机组的理论运行规律一致），将风电机组的运行规律分为I~VI六个工况，具体的名称和特征汇于表7.6，各个区域对应的风速区间标注于图7.19。最大风能追踪区、恒转速区和恒功率区是风电机组主要运行区域，但启动区、恒转速过渡区和恒功率过渡区为风电机组运行状态转化过渡区域，对风电机组机械应力和输出功率波动、传动链运行平稳性都有重要的影响。区分六个运行工况的特点，并以此准确匹配SCADA时间序列对应的数据段，对于深入了解风电机组运行机制和控制原理、准确开展风电机组状态评估和故障诊断具有重要作用。

表7.6 运行状态分类说明表

| 编号 |    区域名称    |              特征描述              |
|:----:|:--------------:|:----------------------------------:|
|  I   |     启动区     |   功率增加、最小转速、桨距角不变   |
|  II  | 最大风能追踪区 | 功率增加、转速直线上升，桨距角不变 |
| III  |  恒转速过渡区  | 功率增加、转速增速放缓、桨距角不变 |
|  IV  |    恒转速区    |   功率增加，额定转速、桨距角不变   |
|  V   |  恒功率过渡区  | 功率增速放缓、额定转速、桨距角增加 |
|  VI  |    恒功率区    |   额定功率、额定转速，桨距角增加   |

<img class="content-image" src="../../images/p2-image534.png" style="width:1432px" alt="">

图7.19 风电机组风速与转速、桨距角和功率的理论曲线

### 7.4.2 高维时序数据在线分割聚类算法

从SCADA数据中，选取其中的风速、风向、功率、轮毂转速、振动、定子温度等6个关键参数，将其时间序列绘制于图7.20。从曲线的趋势可以看出，一些参数的特征和模式类似，如功率和转速；而有些完全不同，如振动和定子温度。对包含上百个参数的SCADA数据进行实时处理，对算法和硬件都有很高要求。通过对风电机组运行规律分析，可以将SCADA数据分为三类：第一类是环境参数，如风速、风向、环境温度和气压等；第二类是与输出能量转换过程相关的控制参数，如功率、电压和电流等；第三类是反映风电机组运行状态的体征参数，例如部件温度、振动等。环境参数和控制参数决定风电机组运行工况，体征参数是风电机组运行状态的一种体现。

<img class="content-image" src="../../images/p2-image535.png" style="width:1815px" alt="">图7.20 SCADA系统中6组时间序列数据

> 1\. Toplize逆协方差聚类算法

Toplize逆协方差聚类算法将多维时间信号的每个维度的时间戳组合成多个时间段，考虑连续时间窗口内数据的维度和时间关系，将每个时间段定义为可重复的状态。图7.21为时序分割示意图，纵坐标代表不同的传感器或者信道，横坐标为时间，窗口代表连续的时间段。

<img class="content-image" src="../../images/p2-image536.png" style="width:1459px" alt="">图7.21 时序分割示意图

TICC算法中的每个簇由相关网络或马尔可夫随机场（markov random field，MRF）定义，描述每个簇内不同时间戳数据的相互联系。TICC算法主要包括三个步骤：首先，将多维时间序列信号分为若干段；然后，根据信号段之间的相似性进行聚类；最后，得到总体聚类结果。TICC算法解决的主要问题是如何获得每个聚类中不同变量之间的相互依赖关系，TICC问题的数学模型具有如下形式<sup>\[15\]</sup>：

<img class="formula-inline" src="../../images/p2-image537.png" style="width:7px" alt=""><img class="formula-inline" src="../../images/p2-image538.png" style="width:240px" alt=""> (7.26)

其中，似然函数展开为

<img class="formula-display" src="../../images/p2-image539.png" style="width:260px" alt=""> (7.27)

式中，<img class="formula-inline" src="../../images/p2-image540.png" style="width:38px" alt="">是正则化参数；*n*为参数数量；*w*为窗口大小；<img class="formula-inline" src="../../images/p2-image541.png" style="width:36px" alt="">为哈达玛乘积的1范数惩罚；<img class="formula-inline" src="../../images/p2-image542.png" style="width:10px" alt="">为各个聚类簇的数据集，<img class="formula-inline" src="../../images/p2-image543.png" style="width:46px" alt="">是<img class="formula-inline" src="../../images/p2-image544.png" style="width:14px" alt="">来自聚类*i*的对数似然值；<img class="formula-inline" src="../../images/p2-image545.png" style="width:10px" alt="">是加强时间一致性的参数；<img class="formula-inline" src="../../images/p2-image546.png" style="width:50px" alt="">为检查相邻点是否被分配给同一聚类的指示函数；<img class="formula-inline" src="../../images/p2-image547.png" style="width:12px" alt="">为第*i*类的经验平均值；*T*是对称分块Toplize矩阵的集合。

方程(7.27)是一个混合的组合连续优化问题，其中有两个重要的变量：聚类数*K*和逆协方差<img class="formula-inline" src="../../images/p2-image548.png" style="width:11px" alt="">，这两个变量共同作用，使问题高度非凸。可以通过期望最大化（expectation maximum，EM）的交替最小化算法来交替分配数据点到簇，然后更新簇参数。应用EM方法，方程（7.27）的解可以分解为一个聚类分配问题和一个Toplitz图形套索问题。

TICC问题中的聚类分配问题可以描述如下：

<img class="formula-display" src="../../images/p2-image549.png" style="width:171px" alt=""> (7.28)

这个TICC问题的子问题被称为集群分配问题，方程（7.28）运用线性规划，寻找从时间戳1到*T*的成本路径，并求出最短路径。

TICC问题的另一个子问题，Toplitz图形套索问题数学表示如下：

<img class="formula-display" src="../../images/p2-image550.png" style="width:200px" alt=""> (7.29)

由于很难直接解决这个问题，方程（7.29）可以根据每个聚类的逆协方差矩阵的特征转化为如下凸优化问题：

<img class="formula-display" src="../../images/p2-image551.png" style="width:174px" alt=""> (7.30)

上式可以写成增广拉格朗日函数的形式：

<img class="formula-display" src="../../images/p2-image553.png" style="width:149px" alt=""> (7.31)

这个问题可以通过交替方向乘子法（alternating direction method of multipliers，ADMM）来优化解决。TICC在一个循环中迭代解决集群分配问题和图形套索问题，更新参数直到获得整体最优解。

> 2\. 模型参数的选择原则

在TICC算法中，需要设置的重要模型参数为窗口大小和聚类的数量。TICC算法不是单独划分每个时间点的数据，而是在每个时间点组装短的窗口或子序列，并将它们连接成一个维度的向量，这个向量的长度为信号输入的数量乘以窗口大小。Toeplize约束假设每个簇的结构是恒定的，但窗口大小仍然是一个相关参数，窗口大小代表了连续时间点之间的相关性。窗口越大，窗口时间数据越长。窗口大小过大导致很难正确划分出时间段边界上的点，而且它们在边界上是恒定的假设也可能不成立。因此，窗口大小一般被认为是相对较小的，在选择时应综合考虑相关应用领域的经验、观测的粒度和平均预期长度，可以通过贝叶斯信息量（Baysian information criterion，BIC）分速或交叉验证来确定。与许多聚类算法一样，聚类的数量是TICC的另一个重要参数，具体数值可以通过不同的方式确定：如果有标记的真实数据集，可以根据真实数据集的标签来确定聚类的数量，或者根据相应领域专家的先验知识来确定聚类的理论数量。如果没有这样的数据，可以使用BIC分数、宏观F1（marco-F1）分数或轮廓系数进行选择。一般来说，聚类数量的确定值往往取决于应用场景本身，主要是因为除了聚类的准确性之外，还需要给出数据的可解释性，通过对理论运行特性曲线的分析，确定聚类数为6。

> 3\. 时序数据在线分割聚类算法

风电SCADA高维时间序列数据的在线聚类识别流程如图7.22所示，主要包括四个部分：运行规律分析、TICC方法的离线学习、TICC方法的在线分割和聚类识别结果的映射。

<img class="content-image" src="../../images/p2-image554.png" style="width:435px" alt="">

图7.22 时序分割聚类方法流程图

> 1\) 风电机组运行规律分析

从SCADA系统中环境和控制参数数据中选取风速、转速（轮毂转速或发电机转速）、桨距角和输出功率等参数，作为分段数据集使用。分段数据集中的一些历史数据被用作TICC方法的离线训练的目标数据。对于历史数据集，选择至少连续数天的秒级数据，在此期间要求风电机组处于正常运行状态，能够连续数小时发电，并且工况良好。对风电机组的风速-功率、风速-转速和风速-桨距角的理论运行规则进行分析，并与分析要求相结合，确定需要分类的运行状态特征和需要划分的群组数量，为之后的划分和聚类提供初始参数值。

> 2\) TICC方法的离线训练

离线训练的目的是为了获得训练数据集下的最佳特征参数，并在最佳参数下验证离线分割结果。

（1）参数输入与数据堆叠。根据控制规律的特点和工作条件，将聚类数和窗口大小输入训练数据集。基于窗口大小的数据建立原始数据集：

<img class="formula-display" src="../../images/p2-image555.png" style="width:128px" alt=""> （7.32）

堆叠后数据集：<img class="formula-inline" src="../../images/p2-image556.png" style="width:92px" alt="">，其中<img class="formula-inline" src="../../images/p2-image557.png" style="width:168px" alt="">，<img class="formula-inline" src="../../images/p2-image558.png" style="width:12px" alt="">为<img class="formula-inline" src="../../images/p2-image559.png" style="width:32px" alt="">形式的矩阵。

（2）初始化聚类结果。最初的聚类结果是用高斯混合模型对叠加数据进行聚类，并根据如下两式计算数据的原始和叠加均值的结果。

原始均值为

<img class="formula-display" src="../../images/p2-image560.png" style="width:213px" alt=""> (7.33)

堆叠均值为

<img class="formula-display" src="../../images/p2-image561.png" style="width:170px" alt=""> (7.34)

式中，<img class="formula-inline" src="../../images/p2-image562.png" style="width:8px" alt="">表示数据矩阵行数。

（3）模型参数优化。将原始均值、堆叠均值和堆叠数据集等参数作为输入，利用ADMM算法进行参数优化，得到每个簇的逆协方差矩阵<img class="formula-inline" src="../../images/p2-image563.png" style="width:14px" alt="">。目标问题为

<img class="formula-display" src="../../images/p2-image564.png" style="width:142px" alt=""> (7.35)

将得到的逆协方差矩阵整形为Toplize协方差矩阵形式：

<img class="content-image" src="../../images/p2-image565.png" style="width:200px" alt=""> (7.36)

（4）聚类分配更新。通过线性规划来解决最短路径问题，找到一条从时间戳1到T的成本路径，以便更新聚类分配结果，线性规划方法如图7.23所示。

目标问题为

<img class="formula-display" src="../../images/p2-image566.png" style="width:168px" alt=""> (7.37)

（5）迭代终止条件。重复步骤（3）和（4），直到当前聚类分配的结果与上一次聚类分配的结果相匹配，或者达到最大迭代次数。原始均值、叠加均值和逆协方差矩阵参数作为最优特征参数被输出。

<img class="content-image" src="../../images/p2-image567.png" style="width:853px" alt="">

图7.23 线性规划示意图

> 3\) TICC方法的在线分割

在线分割是基于离线训练中得到的最优特征参数进行的时序快速分割，可以大大减少实时使用的时间。以离线训练中步骤（5）和（1）输出的最优特征参数、簇数和窗口数作为TICC方法在线分割的初始输入，可以直接通过线性规划求解，得到数据聚类结果。

> 4\) 聚类结果映射

在使用TICC方法对一部分SCADA数据中的特定参数进行分割和聚类后，可以得到分割后工况的标签和聚类特征。对于没有用TICC方法处理过的时间序列数据，可以用聚类的结果进行特征映射，实现聚类结果的映射。例如，在使用TICC方法对风速、转速、桨距角和功率的时间序列进行分割和聚类后，可以将结果映射到温度和振动等参数上。

### 7.4.3 风电机组实例分析

> 1\. 数据准备

采用某风电场2.5MW双馈式风电机组的秒级SCADA数据作为研究数据集。基于前面的风电机组控制规律分析，选取其中风速、发电机转速、功率和桨距角四个参数的时间序列数据作为聚类对象。对SCADA原始数据集进行空值充填、异常值过滤等预处理，也不考虑停机、限功率等与理论运行特征曲线不一致的特殊工况。

> 2\. 时序分割结果分析

根据风电机组风速-功率、风速-转速和风速-桨距角的分析，设定聚类数为6。通过变参数计算不同窗口数下的宏观F1分数，选取其中最优的一个参数，最终获得最优的窗口数为5。应用TICC方法对数据进行分割聚类，将不同聚类簇用不同形状表示。由于时序分割结果用时序图表示比较抽象，难以直接看出变量之间关联关系，而风电机组参数间存在着紧密的联系，为此绘制聚类前后的散点图于图7.24~图7.26中，不同形状对应的工况标签列于表7.7中。

表7.7 数据聚类识别结果及其工况和标签

|  簇编号  |   1   |   2   |   3    |   4   |   5    |   6    |
|:--------:|:-----:|:-----:|:------:|:-----:|:------:|:------:|
| 形状名称 | 圆形  |  点   | 正方形 | 菱形  | 六角形 | 三角形 |
| 形状符号 | **○** | **·** | **□**  | **◇** | **✡**  | **△**  |
| **工况** |   I   |  II   |  III   |  IV   |   V    |   VI   |

将图7.24与图7.25、图7.26合并观察，可以分析分割聚类结果的合理性。由于聚类簇直接有重叠，为了能更加清楚观察某一簇的特点，单独将其绘制于图7.27。圆形表示工况I，代表风电机组开始启动，此时风速大于切入风速，对应功率值较小，转速并没有大幅变化，桨距角也没有变化，图7.26(a)圆形散点与理论分析特征一致。图7.24实点部分功率逐渐增大，转速开始增大，桨距角值几乎恒定为零，通过图7.27(b)可以看到该簇大致趋势正好与表7.6中工况II相对应。图7.25和图7.26的正方形的变化情况似乎与工况II的变化情况一致，与理论工况III的情况有所区别，这是因为理论曲线只是一条线，而实际采集到的数据具有高分辨率的特点，将理论曲线中不太明显的斜率变化弱化了，但通过图7.27(c)可以看到该簇大致趋势变化情况依然与理论工况III相对应。图7.24菱形部分的功率依然是增大的，但图7.24菱形部分的转速趋于稳定，图7.26的部分的桨距角由稳定逐渐开始变化，通过图7.27(d)可以看到该簇大致趋势与工况IV所述情况一致。图7.24六角形部分功率趋于稳定，图7.25六角形部分转速稳定，图7.26六角形部分桨距角变化增大，通过图7.27 (e)可以看到该簇大致趋势与工况V一致。图7.24、图7.25各自三角形部分代表的功率、转速稳定，图7.26三角形部分代表的桨距角持续变化，风电机组进入恒功率状态，通过图7.27 (f)可以看到该簇大致趋势与工况VI情况一致。综合上面的分析可以看出，TICC算法分割聚类的结果与理论工况分析的特征一致。

<div class="image-row"><img class="content-image" src="../../images/p2-image568.png" style="width:619px" alt=""><img class="content-image" src="../../images/p2-image569.png" style="width:605px" alt=""></div>

\(a\) 风速-功率散点图 (b) 风速-功率散点聚类图

图7.24 风速-功率聚类前后散点对比结果

<div class="image-row"><img class="content-image" src="../../images/p2-image570.png" style="width:720px" alt=""><img class="content-image" src="../../images/p2-image571.png" style="width:706px" alt=""></div>

\(a\) 风速-转速散点图 (b) 风速-转速散点聚类图

图7.25 风速-转速聚类前后散点对比结果

<div class="image-row"><img class="content-image" src="../../images/p2-image572.png" style="width:734px" alt=""><img class="content-image" src="../../images/p2-image573.png" style="width:694px" alt=""></div>

\(a\) 风速-桨距角散点图 (b) 风速-桨距角散点聚类图

图7.26 风速-桨距角聚类前后散点对比结果

<div class="image-row"><img class="content-image" src="../../images/p2-image574.png" style="width:834px" alt=""><img class="content-image" src="../../images/p2-image575.png" style="width:1611px" alt=""></div>

> \(a\) 分割聚类后三种特性曲线簇1散点图 (b) 分割聚类后三种特性曲线簇2散点图

<div class="image-row"><img class="content-image" src="../../images/p2-image576.png" style="width:781px" alt=""><img class="content-image" src="../../images/p2-image577.png" style="width:771px" alt=""></div>

> \(c\) 分割聚类后三种特性曲线簇3散点图 (d) 分割聚类后三种特性曲线簇4散点图

<div class="image-row"><img class="content-image" src="../../images/p2-image578.png" style="width:873px" alt=""><img class="content-image" src="../../images/p2-image579.png" style="width:878px" alt=""></div>

> \(e\) 分割聚类后三种特性曲线簇5散点图 (f) 分割聚类后三种特性曲线簇6散点图

图7.27 六种工况下风电机组风速与功率、转速、桨距角数据分割聚类结果

> 3\. 数据聚类方法对比分析

将TICC算法与模糊*C*均值聚类（fuzzy *C*-means clustering，FCM）算法、高斯混合模型（gaussian mixture model，GMM）算法、*K*均值（*K*-means）算法进行研究，来分析比较各聚类方法在处理多维时序数据聚类问题上的优劣。各聚类算法输入的数据集相同，聚类数目设置相同，将各算法聚类结果转化为风速-功率散点图形式，如图7.28-图7.31所示。由图7.28和图7.30可以明显看出，FCM和*K*-means算法得到的结果只是基于功率参数进行分段阈值划分，没有考虑风速等其他参数对功率的影响，不能反映出不同参数之间的联系，且各簇之间没有交叉覆盖关系，无法反映工况之间的变化关系，这跟理论运行工况的特征不符。由图7.29和图7.31可以看出，GMM算法并不像FCM算法和*K*-means算法一样以功率参数为基准进行分段划分，GMM算法与TICC算法的结果都有交叉覆盖关系。但两种算法相比较，GMM算法结果的各簇之间交叉范围小，簇5与簇6之间的过渡不符合表7.6所示的工况V，即没有划分出恒功率过渡区，这与理论运行特性并不相符。由于高维时序数据的维度之间以及连续时间段内的数据是有着一定的联系的，而传统聚类方法无法寻找出这种维度之间、连续之间所内含的关系，也就因此无法对高维数据进行准确的聚类，这个问题当维数越高时越明显。例如，*K*-means的传统聚类分析算法对低维时序数据进行聚类时，先在时间戳上随机选择*k*个点，将数据根据相似程度进行聚类，然后重新计算聚类质心，再根据新的聚类质心对时间戳上的数据进行相似分析并聚类，重复两个步骤直到达到精度为止，计算出最终整个时间戳上数据的聚类结果，最后对聚类的结果进行解释与评价。但这些传统的时序数据聚类方法在对高维时序数据进行聚类计算时得到的结果会存在精度低、聚类效果差等问题。而TICC算法却充分考虑数据本身和数据之间的相关关系，由此可以获得理想的聚类结构，所以，对风电SCADA数据进行时间序列聚类的效果要优于其他几种算法。

<div class="image-row"><img class="content-image" src="../../images/p2-image580.png" style="width:6236px" alt=""><img class="content-image" src="../../images/p2-image581.png" style="width:6236px" alt=""></div>

图7.28 FCM分割聚类结果 图7.29 GMM方法分割聚类结果

<div class="image-row"><img class="content-image" src="../../images/p2-image582.png" style="width:6236px" alt=""><img class="content-image" src="../../images/p2-image583.png" style="width:6236px" alt=""></div>

图7.30 *K*-means方法分割聚类结果 图7.31 TICC方法分割聚类结果

> 4\. TICC方法应用

利用TICC方法，遵循运行工况分析、TICC方法的离线训练、TICC方法的在线分割和聚类结果映射等步骤，对某风电场SCADA数据50个参数进行分割聚类和工况标签。步骤1，从50个参数中选取4个特征参数作为分割聚类初始对象，理论分析参数之间的关系和包含的工况特征；步骤2，从中选取一段时间的数据作为离线数据集，如选择其中3天的连续秒级数据对TICC方法进行训练；步骤3，将计算得到的TICC特征值，作为在线分割方法的输入，对新的时序数据进行分割聚类和工况标签化处理；步骤4，将聚类结果映射，将4个完成分割聚类和工况标签化的参数的时序数据基于相同横向时间刻度纵向映射到其他45个维度的时间序列。

由于SCADA系统环境参数、体征参数和控制参数之间存在着一定的内部联系，所以将特征参数数据在时间刻度上分割后，可将分割结果根据时间区间直接映射到纵向的其他维度时间序列。为了说明分割聚类后的映射过程，将一组分割映射后的风速、功率、轮毂转速、桨距角、风向、*x*轴振动、*y*轴振动、定子温度和轮毂温度的时序数据绘于图7.32中。风速、功率、轮毂转速和桨距角为利用TICC方法进行分割聚类的结果，其余参数为未分割聚类的数据。将这九组时间序列的横轴统一为时间刻度，分割结果中各个分割时间段的工况标签，可以作为其余维度相同时间段的工况标签，避免重复的计算。

<img class="content-image" src="../../images/p2-image584.png" style="width:11340px" alt="">

图7.32 多维SCADA时序数据分割聚类结果

图7.32为在线分割运行状态映射结果图，其中不同区域用虚线划分，并将其用a~f字母进行标记。区域b对应于表7.6的运行工况I，该运行状态下风电机组启动，*x*和*y*方向的振动变化幅度大，温度变化不明显；区域a对应于运行工况II，该状态下转速开始变化增大，*x*和*y*方向的振动变化幅度减小，趋于平稳，温度变化不明显；区域d对应于运行工况III，*x*和*y*方向的振动变化幅度小，温度变化不明显；区域c对应于运行工况IV，*x*和*y*方向的振动变化幅度不明显，定子温度逐渐上升，轮毂温度略微下降；区域e对应于运行工况V，*x*和*y*方向的振动变化幅度增大，定子温度增大，轮毂温度略微下降；区域f对应于运行工况VI，*x*和*y*方向的振动变化幅度明显，定子温度增大并将达到峰值，轮毂温度变化稳定。通过对SCADA数据进行分割聚类，实现了数据工况特征识别。为了分析该方法的计算效率，以某风电场三天的秒级SCADA数据为例，选取其中四个参数进行离线聚类耗时需一小时左右才能得到聚类结果，但若将相同SCADA数据用训练好的模型进行在线分割，同样维度与时间长度的SCADA数据只需一两分钟即可完成。由上分析可知，本节提出的高维时序数据在线分割聚类算法，充分考虑风电机组的运行规律和特点，首先通过理论分析将高维问题进行降维，尽量避免过高的维度，同时在聚类数目选择时，分析数据之间的物理关联性，选择合适的聚类数目；然后再利用TICC方法时采取离线训练和在线计算两个步骤，这样可以有效保障在线的计算效率；最后利用了简单的聚类结果映射的方法，来处理高维分割聚类的问题。通过多个环节优化和缩减时间，TICC方法避免了高维问题求解需要消耗的大量迭代求解时间，最终达到高维时序数据在线高效处理的目的。

## 7.5 参考文献

1.  雷萌, 郭鹏, 刘博嵩. 基于自适应DBSCAN算法的风电机组异常数据识别研究\[J\]. 动力工程学报, 2021, 41(10): 859-865.

2.  Zhu A, Xiao Z, Zhao Q. Power data preprocessing method of mountain wind farm based on POT-DBSCAN\[J\]. Energy Engineering, 2021, 118(3): 549-563.

3.  Zhang L, Kai L, Wang Y, et al. Ice detection model of wind turbine blades based on random forest classifier\[J\]. Energies, 2018, 11(10): 2548.

4.  Vidal, Y, Pozo F, Tutiven C. Wind turbine multi-fault detection and classiﬁcation based on SCADA Data\[J\]. Energies, 2018, 11: 3018.

5.  Pashazaden V, Salmasi F R, Araabi B N. Data driven sensor and actuator fault detection and isolation in wind turbine using classiﬁer fusion\[J\]. Renewable Energy, 2018, 116:99-106.

6.  Zheng K, Li S B. Prediction of the remaining service life of bearing based on associative neural network\[J\]. Mechanical Design and Manufacturing, 2020, 11:203-206.

7.  Zhou L, Zhao Q, Wang X, Zhu A. Fault diagnosis and reconstruction of wind turbine anemometer based on RWSSA-AANN\[J\]. Energies, 2021, 14: 6905.

8.  周凌, 赵前程, 石照耀, 等. 风电场风电机组机载风速仪状态自确认\[J\]. 太阳能学报, 2022, 43(11): 172-178

9.  刘永前, 王飞, 时文刚, 等. 基于支持向量机的风电机组运行工况分类方法\[J\]. 太阳能学报, 2010, 31(9): 1191-1197．

10. 董玉亮, 李亚琼, 曹海斌, 等. 基于运行工况辨识的风电机组健康状态实时评价方法\[J\]. 中国电机工程学报, 2013, 33(11): 88-95.

11. Hallac D, Nystrup P, Boyd S. Greedy gaussian segmentation of multivariate time series\[J\]. Advances in Data Analysis and Classification, 2016, 13:727-751.

12. 肖钊, 邓杰文, 刘晓明, 等. 基于运行规律和 TICC 算法的风电 SCADA 高维时序数据聚类方法\[J\]. 机械工程学报, 2022, 58(23): 196-207.

13. Daszykowski M, Walczak B, Massart D L. Looking for natural patterns in data, Part 1: Density-based approach\[J\]. Chemometrics and Intelligent laboratory systems, 2001, 56(2): 83-92.

14. Jian K X, Bo S. A novel swarm intelligence optimization approach: sparrow search algorithm\[J\]. Systems Science & Control Engineering, 2020, 8(1): 22-34.

15. Hallac D, Vare S, Boyd S, et al. Toeplitz inverse covariance-based clustering of multivariate time series data\[C\]. Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Halifax, Canada, 2017: 215-223.
