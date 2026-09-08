# 前置内容

## ROS 机器人编程

![0_0_0_1829_1430_0.jpg](../images/0_0_0_1829_1430_0.jpg)

从基本概念到机器人应用程序编程实战!

机器人操作系统

表允皙 I 赵汉哲 I 郑黎蝹 I 林泰勋

## ROS机器人编程

作者 表允皙赵汉哲郑黎蝹林泰勋

发行日 2017年12月22日

出版社 ROBOTIS Co., Ltd.

#1505, 145, Gasan Digital 1-ro, GeumCheon-gu, Seoul, Republic of Korea

E-mail contactus2@robotis.com

主页www.robotis.com

ISBN 979-11-962307-2-2

ALL RIGHTS RESERVED

Copyright © 2017 ROBOTIS Co., Ltd.

本著作物受著作权法保护。禁止无端转载和复制。

使用本书的部分或全部内容, 需要获得著作权者和ROBOTIS (株) 的书面同意。

ROS

机器人编程

表允皙 赵汉哲 郑黎蝹 林泰勋

故事在10年前和现在是一样的，但还没有明确的解答。原因是什么？会有多种看法， 但我认为机器人产业要形成新的商业模式还有很多不足的地方，还有很多需要解决的问题。我认为这个解决方案应该是跨越国界的超越性合作，我还认为软件平台和支持这些平台的社区可以解决这些问题。参与开发机器人操作系统ROS的有学术研究人员、工业一线开发人员和业余爱好者等人群。此外，不仅是机器人专业人士，还有网络专家、计算机科学家、计算机视觉专家也大有人参加，因此实现着机器人领域和其他诸多专业的知识的融合。机器人预计从现在开始以不同于以往的方式发展。我们认为, 通过开放和合作, 我们可以解决至今尚未解决的问题。我想说, 这不是未来的产业，而已经是现在的产业。

本书是我们四个人在完成多项有关ROS的项目的过程中获得的经验的基础上编写的 ROS机器人编程书。为了初次接触ROS的读者，尽可能涵盖了初学者所需要的大多数内容。进而包括了可以应用于嵌入式系统、移动机器人和机械手臂的ROS内容。为了尽量有助于ROS的初学者, 将ROS的介绍和各部分所需要的信息都标上脚注, 让读者可以自行在网上找到。真诚希望更多的人通过本书了解和参与当今日益加速的机器人工程的跨界式的知识融合和跨领域的合作。

下面我想对那些帮助我让这本书面世的人们表达我的谢意。我非常感谢ROS专家 Lee Ji-Hoon博士，Ahn Byung-kyu，Jung Keun-man，Seong Chang-Hyun博士和 Koo Sung-Yong博士，他们对有着诸多缺点的我总是给予新的指导。我想和他们说， 我将来想和你们一起做出更多的事情。另外, 感谢对这本不为人所知的ROS专业书籍的出版提供大力支持的Han Chang-Hoon代表，以及用最佳的编排使得读者更加容易理解ROS的Lee Yin-Ho，Son Will，Jason，Kim Kayla 老师。我还想感谢ROBOTIS的成员们。ROBOTIS，一家以“机器人是什么？”这一哲学疑问开始的公司，我想因为有了他们才有了这本书。我还要感谢立志通过开源代码让更多人一起思考和开发机器人的“开源团队(OST)”的成员，感谢开源生态界和社区的协助者Kim Jin-Wook先生，并向本书的共同作者，“ROS英雄团”， 赵汉哲、郑黎蝹和林泰勋鼓掌致意。还非常感谢正在一起编写日语版ROS书籍的我的指导教授日本九州大学的倉爪亮教授和長谷川勉教授。他们以丰富的研究经验引领我走向了研究者之路，至今也在不断地学到很多知识。借此机会，我想向教授传达我的心声“非常感谢您，给予我受益终生的敦敦教诲”。同时也向为这本书成功出版，不断激励我坚持不懈，向我积极反馈好的建议的开源机器人社区 Park Hyeng-Il和运营组以及为我加油地会员们，为开源机器人平台开发付出热情的公开项目负责人表示衷心的感谢。将来，我想继续以开源机器人为主题一起进行讨论，同时携手进行更有趣的项目。还要向facebook的机器人工程公开群运营组和为韩国机器人产业发展献计献策的群组成员表示感谢。也要感谢与我一起燃烧青春的机器人比赛团队“ROBIT”和机器人研究会“ROLAB”的师兄弟们。还有一点，本书之所以能面世的重要原因之一是本人所属的公司 “ROBOTIS” ，对开源代码编著活动及交流活动积极提供支持，为此向CTO Ha Yin-Yong和CEO Kim Byung-Soo表示谢意。

最后向我心爱的家人致谢。首先，向给予我无限的爱的父母说一声“我会永远敬爱你们，也时时刻刻心存对你们的感恩之心”。还有在旁边一直鼓励我，支持我的岳父母，"我对你们常怀感恩，一直爱着你们"。爱妻Ken-Mi, 你一直坚守在我的旁边，一直照顾着我，非常感谢你，爱你，以后我们要更幸福地生活。世界上最可爱的我的心肝们，儿子Ji-an还有女儿Ji-Woo, 我为了你们会努力成为使这个世界变得更美好幸福的好父亲。

2017年7月

表允晳

技术局限性，需要进行更多的研究。想要克服当前的问题，专家、相关企业、一般用户需要携手努力一起发展现状。除了机器人的制作和应用之外，我们需要一个协作和开发的平台，我认为这就是ROS平台。 ROS具备着降低技术壁垒和有益于传播的各种因素。 通过ROS平台，希望积累更多的知识和技术，使得更新更进步的机器人加入到我们的生活中。

嵌入式系统控制传感器和驱动器，进行实时数据处理，作为构成机器人的一部分， 起着重要作用。通常为了实时地进行数据处理，会使用微控制器。这本书以在嵌入式系统中使用ROS的方法和基本示例为中心进行叙述。我希望这些内容为那些使用ROS 搭建机器人嵌入式系统的用户助一臂之力。

我向Pyo Hyung-Joon, Park Hyung-Il和Park Byung-Hoon为创建OpenCR而付出的努力表示感谢，他们弥补了我的很多不足之处，也共度了很多的美好时光，因此给我留下了很多回忆。也非常感谢开源项目团队(OST)的成员，与他们在一起我觉得很活跃很开心。我衷心感谢Kim In-Wook，从我刚步入社会时开始到现在，一直与我同在, 在遇到困难时为给予我很多好的建议和激励。同时, 也要向为我人生提供新的挑战机会的ROBOTIS的Kim Byung-Soo代表表示衷心的谢意。当我还小时候，我看到了 Kim Byung-Soo代表在HiTel数码兴趣协会上的写作，通过他的文章我学到很多相关知识, 也成了从事机器人行业的动机。这使得我如今在他的公司开发机器人。

总以工作繁忙为借口没能陪伴儿子，心存亏欠，在此立下决心为我心爱的儿子成为好爸爸。当笔者备受压力时，默默陪伴我，支持我的爱妻Kyung-Sun，谢谢你理解和体谅我的任性，借此机会向你表达歉意的同时也要跟你说一声我爱你。

2017年7月

赵汉哲

让我们一起如愿以偿地制作我们想要制作的机器人吧! 以前我们曾经拿着与书本配套的机器人套件来制作机器人，仅仅做出简单的动作，也会很满足地说 “这就是机器人”。然而，近年来，随着计算机性能的发展、设备的成本降低、获取素材变得迅速与便捷，许多有关机器人的概念被重新定义着。机器人爱好者们已经大量开始投入到机器人制作当中，并且信息量变得庞大，随着各个品牌制作商把自己的产品进行自动化，如今汽车、飞机甚至潜艇都已成为机器人的平台。人们开始跨越科学领域，开始融合各自的技术，结果机器人终于开始被制作成梦想中的形态。我们可以说现在机器人行业正面临着全盛时期，但从中有些人可能开始跟不上日益变得高性能、高端化的潮流, 从而机器人产业可能将成为只有懂机器人的人才可以生存以及得到发展的领域。

我觉得ROS对他们来说是雪中送碳，即使没有专攻该领域也能学到相关技术，从而节省时间和金钱。 如果在使用过程中遇到问题，可以向制作人提问并得到反馈，将会形成互助体系。 如今，像宝马等公司也正在引入ROS。 通过ROS来运营公司或与其他公司合作，现可以说占据ROS的优势就会成为该领域的赢家。

我希望与本书的读者将来可以在ROS领域里相见。开源代码团队的组员们，尤其是给予我参与此书编著的表允皙博士，为诸多项目同甘共苦的赵汉哲和林泰勋，向你们表示感谢。

同时想感谢在机器人领域里慷慨提供各种建议和帮助的Song Hyeon-Jong和Kim Hyeon-Seok，能使得我不断思考的Kim Jin-Wook，为主办自主驾驶比赛而一起努力的Seng Ki-Jae, 共度美好时光的开源机器人论坛 (OROCA) 的AuTURBO项目的成员们，谢谢大家。还要想为我不断牺牲的父母说:“我会一直孝敬你们”。同时也向陪伴我的弟弟和一直与我同在的Kim Ha表示感谢，最后我把所有荣耀献给创造我的上帝。

2017年7月

郑黎蝹

待着不断提高改善的生活，但是可能会更早到来的对于劳动市场的负面影响的展望会使得人们更加不安。如此, 我们身边正在进行的机器人和人工智能的研究和发展, 会在不久的将来会对我们产生深远的影响。 所以我们更要关注机器人技术的发展，试着去了解并为未来做好准备。

为了应对快速发展的技术，开源代码正在利用集体智能来促进技术的发展和普及。 现在，机器人技术可以通过开源代码，与多种多样的人共同工作和共同发展， 复杂的算法也可以很容易地应用在个人机器人中。 从而, 我们可以防止因为技术被归属于特定群体而影响整个社会的情况，也可以一步一步地揭开机器人的神秘面貌， 克服恐惧心理。

我的目标是通过技术的应用和变化给人们带来感动，使他们对这些技术更感兴趣。 作为第一步，我试图通过开源代码社区学习各种机器人技术，并开放自己项目的代码，努力与各种各样的人进行协作。 以后，我正计划着与机器人以外其他领域的人进行交流，互相分享经验和技术。 通过这种方式推广技术，并为人们提供各种体验，使得人们轻松地适应未来社会的变化。

我参与了这本书的机械手臂部分的编著，比较易懂地整理了维基里ROS、 Gazebo、MoveIt!的内容，同时花了大量时间去试图总结那些没有在维基解释的部分，努力将更多更准确的信息传达给读者。 我想继续精益求精，成为与人们分享所学到的知识的人。

首先想要向表允皙博士表示感谢，直到这本书出版，他作为学校前辈、公司领导、老师，教给我很多知识的同时也给予我勇气和机会。还有对Sung Chang-Hyeon博士表示感谢，在百忙之中腾出时间编审原稿，并且诚恳地回答各种各样的问题。 我还要感谢从早到晚一起共事的开源代码团队的同事们和总是面带微笑，充满热情的所有ROBOTIS员工。还要向研究生院指导教授Lee Jong-Ho教授表示感谢, 在他的指导下, 不仅. 能学到工学知识和研究过程, 还能培养真诚、耐心和责任感。 再次感谢您。

最后, 一直在旁边默默地帮助我们、热心地守护我们的爸爸和比任何人都更有好奇心和创造力的敬爱的母亲，虽然比我小两岁，但一直像朋友般陪伴着我的唯一的弟弟， 我想对你们说谢谢你们，我爱你们。 而且也要感谢在过去7年时间一直陪伴着我，有时像姐姐一样包容我，使我感受幸福，有时像妹妹一样撒娇，使我心动的Kim Go-En，谢谢你！

2017年7月

林泰勋代表作者表允皙是ROBOTIS的研究员，他是开源团队的负责人，正在研究和开发基于开源项目的服务机器人的支持系统。机器人总是会抛给我们更多需要思考的问题， 让我们更加细心地接近和观察我们的生活。从光云大学电子工程专业本科毕业之后在韩国科学技术研究院(KIST)工作，之后赴日本九州大学，以人工智能工程专业获得硕士及博士学位。喜欢分享技术，比如偶尔向机器人报社、无线航模、机器人月刊、ROBOCON MAGAZINE，等报纸和杂志投稿。喜欢和拥有机器人梦想的人们畅谈，在“为机器人工程的开放社区”及以开源机器人技术为宗旨的“开源机器人技术共享社区(WWW.OROCA.ORG)”进行公开讲座并进行公开项目。一向喜欢举办活动，因此期待通过机器人及ROS相关的演讲、讲座、研讨会、展会等活动中能遇见本书的读者。

## 赵汉哲 (Cho)

作者赵汉哲在ROBOTIS负责机器人控制器和固件的开发。曾在LG CNS担任ATM的固件开发，对于编程和机器人有浓厚的兴趣。在中学时期参观Micro Mouse比赛成了认识机器人的契机，至今喜爱学习和分享与机器人有关的技术。尤其是对于控制硬件的固件和FPGA深感魅力，制作与此相关的机器人作品。认为技术是在分享的时候能得到更大的发展，梦想着即便时间流逝，到了老年也能过着焊硬件、编代码的生活。

作者郑黎蝹是ROBOTIS的研究员，负责开发自主驾驶系统及舵机控制应用程序。认为人与人之间无法互补的空缺正是机器人存在的意义所在，并在机器人研发过程中也努力实践这种理念。曾获早稻田大学电气工程与生物技术系学士学位和硕士学位。 他曾一边为ROBOCON杂志寄稿，一边负责大规模机器人大赛R-BIZ CHALLENGE的自主驾驶比赛。 目前，正在开展“开源机器人技术共享社区(WWW.OROCA.ORG)”中的自主驾驶机器人研究项目。

## 林泰勋 (Darby)

作者林泰勋是ROBOTIS的一名研究员，在开源团队中负责Turtle Bot 3 和 OpenManipulator的开发，此外还担负着本团队的颜值。相信创意需要丰富的经验和广博的知识，喜欢旅行、读书以及与各行各业的人们进行对话。给更多人提供独特的体验和平实的感动正是他开发机器人的目标。努力通过与电影、展会、媒体等各领域的专家合作共事来实现自己的梦想。

从2016年起，在“开源机器人技术共享社区”参与“LooKSo in Film”活动，担任 “冷冷剧作家”及软件工程师。

## 开源软件及硬件

本书中用到的开源软件及硬件都公开在Github及Onshape的存储库，并时刻接收用户的反馈和改进意见，持续进行版本升级。下面是与本书中用到的开源软件及硬件相关的Github及Onshape的链接。

## 开源软件列表

- https://github.com/ROBOTIS-GIT/robotis_tools $\rightarrow$ 第3章

- https://github.com/ROBOTIS-GIT/ros_tutorials $\rightarrow$ 第4,第7,第13章

- https://github.com/ROBOTIS-GIT/DynamixelSDK $\rightarrow$ 第8,第10章

- https://github.com/ROBOTIS-GIT/dynamixel-workbench $\rightarrow$ 第8,第13章

- https://github.com/ROBOTIS-GIT/dynamixel-workbench-msgs $\rightarrow$ 第8,第13章

- https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver $\rightarrow$ 第8,第10,第11章

- https://github.com/ROBOTIS-GIT/OpenCR $\rightarrow$ 第9,第12章

- https://github.com/ROBOTIS-GIT/turtlebot3 $\rightarrow$ 第10,第11章

- https://github.com/ROBOTIS-GIT/turtlebot3_msgs $\rightarrow$ 第10,第11章

- https://github.com/ROBOTIS-GIT/turtlebot3_simulations $\rightarrow$ 第10,第11章

- https://github.com/ROBOTIS-GIT/turtlebot3_applications $\rightarrow$ 第10,第11章

- https://github.com/ROBOTIS-GIT/turtlebot3_deliver $\rightarrow$ 第12章

- https://github.com/ROBOTIS-GIT/open_manipulator $\rightarrow$ 第13章

## 开源硬件列表

OpenCR (第9章)

- Board:

TurtleBot3 (第10章、第11章、第12章、第13章)

<table><tr><td colspan="2">- Turtlebous (第10早、弟11早、弟12早、弟13早)</td></tr><tr><td>- Burger:</td><td>http://www.robotis.com/service/download.php?no=676</td></tr><tr><td>- Waffle:</td><td>http://www.robotis.com/service/download.php?no=677</td></tr><tr><td>- Waffle Pi:</td><td>http://www.robotis.com/service/download.php?no=678</td></tr><tr><td>- Friends OpenManipulator Chain:</td><td>http://www.robotis.com/service/download.php?no=679</td></tr><tr><td>- Friends Segway:</td><td>http://www.robotis.com/service/download.php?no=680</td></tr><tr><td>- Friends Conveyor:</td><td>http://www.robotis.com/service/download.php?no=681</td></tr><tr><td>- Friends Monster:</td><td>http://www.robotis.com/service/download.php?no=682</td></tr><tr><td>- Friends Tank:</td><td>http://www.robotis.com/service/download.php?no=683</td></tr><tr><td>- Friends Omni:</td><td>http://www.robotis.com/service/download.php?no=684</td></tr><tr><td>- Friends Mecanum:</td><td>http://www.robotis.com/service/download.php?no=685</td></tr><tr><td>- Friends Bike:</td><td>http://www.robotis.com/service/download.php?no=686</td></tr><tr><td>- Friends Road Train:</td><td>http://www.robotis.com/service/download.php?no=687</td></tr><tr><td>- Friends Real TurtleBot:</td><td>http://www.robotis.com/service/download.php?no=688</td></tr><tr><td>- Friends Carrier:</td><td>http://www.robotis.com/service/download.php?no=689</td></tr><tr><td colspan="2">OpenManipulator (第10、第13章)</td></tr><tr><td>- Chain:</td><td>http://www.robotis.com/service/download.php?no=690</td></tr><tr><td>- SCARA:</td><td>http://www.robotis.com/service/download.php?no=691</td></tr><tr><td>- Link:</td><td>http://www.robotis.com/service/download.php?no=692</td></tr></table>

## 开源软件下载

本书中涉及到的所有代码均保存在Github的存储库中。下载源代码的方法有 利用Git命令直接下载和 通过浏览器下载压缩文件的方法。两种下载方法请参考如下说明。

## 1 用命令下载

为了在Linux里用git命令直接下载，需要先安装git。请打开终端，如下安装git。

\$ sudo apt-get install git

然后用如下命令下载相应存储库中的源代码。(例:ros_tutorials功能包)

\$ git clone https://github.com/ROBOTIS-GIT/ros_tutorials.git

## 2 从浏览器下载

用浏览器访问相应地址(https://github.com/ROBOTIS-GIT/ros_tutorials)可以访问Github的存储库。点击右上角的 “Clone or download” → “Download ZIP” 按键，就可以下载压缩文件。

## 开源资源

本书中用作教育器材的ROS官方机器人平台 "TurtleBot3" 的最新信息可以从如下的公开渠道获取。通过一步步实习(持续升级的)开源程序和丰富的TurtleBot3的应用案例，想必读者的ROS机器人编程实力会大有长进。

- TurtleBot 官网 http://www.turtlebot.com

- TurtleBot3 Wiki网站 http://turtlebot3.robotis.com

- TurtleBot3 视频 https://www.youtube.com/c/ROBOTISOpenSourceTeam

此外，用于搭建ROS嵌入式系统的 "OpenCR" 控制器、学习机械手臂操控的 "OpenManipulator"， 等本书中介绍的项目的相关内容也都已公开。不仅如此，在TurtleBot3及OpenManipulator用作舵机的 "Dynamixel"，关于它的信息和它的必用软件“Dynamixel SDK”及“Dynamixel Workbench”也在如下链接公开最新信息和例子。

OpenCR [http://emanual.robotis.com/] > [PARTS] > [Controller] > [OpenCR]

OpenManipulator [http://emanual.robotis.com/] > [PLATFORM] > [OpenManipulator]

Dynamixel SDK http://wiki.ros.org/dynamixel_sdk

[http://emanual.robotis.com/] > [SOFTWARE] > [DYNAMIXEL] > [Dynamixel SDK]

Dynamixel Workbench http://wiki.ros.org/dynamixel_workbench

[http://emanual.robotis.com/] > [SOFTWARE] > [DYNAMIXEL] > [Dynamixel Workbench]

最后, 读者也可以参考公开的ROS学习参考资料。这些资料由本书的各章要点和实战实例组成，因此如果与本书一起使用，想必会有助于团队学习和研讨会。

- 讲义资料 https://github.com/ROBOTIS-GIT/ros_seminar

参考资料 https://github.com/ROBOTIS-GIT/ros_book

源/我码资料 https://github.com/ROBOTIS-GIT/ros_tutorials

## 相关社区及提问

Robot Source Community http://www.robotsource.org/

ROS Discourse https://discourse.ros.org/

ROS Answers http://answers.ros.org/

ROS Wiki http://wiki.ros.org/

## 专业术语

本书中的ROS相关术语尽量使用了国内常用的ROS术语，但有些术语则为了更清楚地表达，直接采用了英文原词。

## 中文术语表

<table><tr><td>英文术语</td><td>中文术语</td><td>英文术语</td><td>中文术语</td></tr><tr><td>Node</td><td>节点</td><td>Private Name</td><td>私有名称</td></tr><tr><td>Master</td><td>主节点</td><td>Relative Name</td><td>相对名称</td></tr><tr><td>Package</td><td>功能包</td><td>NodeHandle</td><td>节点句柄</td></tr><tr><td>Metapackage</td><td>元功能包</td><td>Timer</td><td>计时器</td></tr><tr><td>Dependent Package</td><td>依赖包</td><td>Transform</td><td>变换</td></tr><tr><td>Message</td><td>消息</td><td>Master PC</td><td>总机</td></tr><tr><td>Service</td><td>服务</td><td>Host PC</td><td>主机</td></tr><tr><td>Topic</td><td>话题</td><td>Build</td><td>构建</td></tr><tr><td>Service Server</td><td>服务服务器</td><td>Motion Planning</td><td>运动规划</td></tr><tr><td>Service Client</td><td>服务客户端</td><td>Odometry</td><td>测位</td></tr><tr><td>Parameter Server</td><td>参数服务器</td><td>Pose</td><td>姿态</td></tr><tr><td>Publisher</td><td>发布者</td><td>Play/Replay</td><td>回放</td></tr><tr><td>Subscriber</td><td>订阅者</td><td>Introspection</td><td>自检</td></tr><tr><td>Launch</td><td>启动</td><td>Icon</td><td>图标</td></tr><tr><td>Client Library</td><td>客户端库</td><td>Dead Reckoning</td><td>导航推测</td></tr><tr><td>Repositories</td><td>存储库</td><td>Base</td><td>基座</td></tr><tr><td>Namespace</td><td>命名空间</td><td>Link</td><td>连杆</td></tr><tr><td>Base Name</td><td>基本名称</td><td>Joint</td><td>关节</td></tr><tr><td>Global Name</td><td>全局名称</td><td>End Effector</td><td>末端执行器</td></tr></table>

## 许可说明

本书中使用的开源代码遵循分别指定的许可，著作权者或贡献者对因使用本软件而发生的直接或间接的损害、偶发或后果性损害赔偿，特殊或一般损害赔偿，对任何原因，责任，合同，义务，责任或侵权行为(包括疏忽)不承担责任。

- 本书中使用的开源代码会根据读者使用的时间，可能会有版本变化，因此在运行时可能会有相异的结果。

本书中出现的公司名称和产品名称通常为各公司的注册商标，文中将省略TM，(c)，(c)标记。

– 如果您对本书内容有任何疑问，请联系出版社或上述社区。

第1章 / 机器人软件平台

1.1. 平台的组件 2

1.2. 机器人软件平台 3

1.3. 机器人软件平台的必要性 5

1.4. 机器人软件平台将带来的未来 6

第2章 / 机器人操作系统ROS

2.1. ROS简介 10

2.2. 元操作系统 10

2.3. ROS的目的 12

2.4. ROS的组件 13

2.5. ROS的生态系统 14

2.6. ROS的历史 15

2.7. ROS的版本 16

2.7.1. 版本规则 18

2.7.2. 版本周期 19

2.7.3. 选择版本 20

第3章 / 搭建ROS开发环境

3.1. 安装ROS 24

3.1.1. 常规安装 24

3.1.2. 简易安装 29

3.2. 搭建ROS开发环境 29

3.2.1. ROS配置 29

3.2.2. 集成开发环境(IDE) 33

3.3. ROS操作测试 36

第4章 / ROS的重要概念

4.1. ROS术语 41

4.2. 消息通信 50

4.2.1. 话题(topic) 51

4.2.2. 服务(service) 52

4.2.3. 动作 (action) 52

4.2.4. 参数(parameter) 54

4.2.5. 消息通信的过程 54

4.3. 消息 60

4.3.1.msg文件 63

4.3.2.srv文件 63

4.3.3.action文件 64

4.4. 名称 (name) 64

4.5. 坐标变换(TF) 67

4.6. 客户端库 68

4.7. 异构设备间的通信 69

4.8. 文件系统 70

4.8.1. 文件组织结构 70

4.8.2. 安装目录 71

4.8.3. 工作目录 73

4.9. 构建系统 75

4.9.1. 创建功能包 75

4.9.2. 修改功能包配置文件(package.xml) 76

4.9.3. 修改构建配置文件(CMakeLists.txt) 79

4.9.4. 编写源代码 88

4.9.5. 构建功能包 90

4.9.6. 运行节点 90

第5章 ╱ ROS命令

5.1. ROS命令概述 93

5.2. ROS shell命令 95

5.2.1. roscd:移动ROS目录 95

5.2.2. rosls:ROS文件列表 96

5.2.3. rosed:ROS编辑命令 96

5.3. ROS执行命令 97

5.3.1. roscore: 运行roscore 97

5.3.2. rosrun:运行ROS节点 99

5.3.3. roslaunch:运行多个ROS节点 99

5.3.4. rosclean:检查及删除ROS日志 100

5.4. ROS信息命令 101

5.4.1. 运行节点 101

5.4.2. rosnode: ROS节点 102

5.4.3. rostopic: ROS话题 104

5.4.4. rosservice:ROS服务 108

5.4.5. rosparam:ROS参数 111

5.4.6. rosmsg: ROS消息信息 114

5.4.7. rossrv:ROS服务信息 116

5.4.8. rosbag:ROS日志信息 118

5.5. ROS catkin命令 122

5.6. ROS功能包命令 125

第6章 ╱ ROS工具

6.1. 三维可视化工具(RViz) 130

6.1.1. RViz安装与运行 133

6.1.2. RViz画面布局 134

6.1.3. RViz显示屏 136

6.2. ROS GUI开发工具(rqt) 137

6.2.1. rqt安装与运行 138

6.2.2. rqt插件 139

6.2.3. rqt_image_view 142

6.2.4. rqt_graph 143

6.2.5. rqt_plot 145

6.2.6. rqt_bag 147

第7章 ╱ ROS编程基础

7.1. ROS编程前须知事项 150

7.1.1. 标准单位 150

7.1.2. 坐标表现方式 151

7.1.3. 编程规则 152

7.2. 发布者节点和订阅者节点的创建和运行 153

7.2.1. 创建功能包 153

7.2.2. 修改功能包配置文件 153

7.2.3. 修改构建配置文件(CMakeLists.txt) 154

7.2.4. 创建消息文件 156

7.2.5. 创建发布者节点 157

7.2.6. 创建订阅者节点 158

7.2.7. 构建(build)节点 159

7.2.8. 运行发布者 160

7.2.9. 运行订阅者 161

7.2.10. 检查运行中的节点的通信状态 162

7.3. 创建和运行服务服务器与客户端节点 163

7.3.1. 创建功能包 164

7.3.2. 修改功能包配置文件(package.xml) 164

7.3.3. 修改构建配置文件(CMakeLists.txt) 165

7.3.4. 创建服务文件 166

7.3.5. 创建服务服务器节点 167

7.3.6. 创建服务客户端节点 168

7.3.7. 构建节点 170

7.3.8. 运行服务服务器 170

7.3.9. 运行服务客户端 171

7.3.10. rosservice call命令的用法 172

7.3.11.GUI工具Service Caller的用法 172

7.4. 创建和运行动作服务器和客户端节点 174

7.4.1. 生成功能包 174

7.4.2. 修改功能包配置文件(package.xml) 174

7.4.3. 修改构建配置文件(CMakeLists.txt) 175

7.4.4. 创建动作文件 176

7.4.5. 创建动作服务节点 177

7.4.6. 创建客户端节点 180

7.4.7. 构建节点 181

7.4.8. 运行动作服务器 182

7.4.9. 运行动作客户端 184

7.5. 参数的用法 185

7.5.1. 利用参数创建节点 185

7.5.2. 设置参数 187

7.5.3. 读取参数 188

7.5.4. 构建节点和运行节点 188

7.5.5. 查看参数目录 188

7.5.6. 参数的用例 189

7.6. roslaunch的用法 190

7.6.1. roslaunch的应用 190

7.6.2. Launch标签 193

第8章 / 机器人、传感器和电机

8.1. 机器人功能包 196

8.2. 传感器功能包 199

8.2.1. 传感器的类型 199

8.2.2. 传感器功能包的分类 200

8.3. 相机 201

8.3.1. USB摄像头相关功能包 202

8.3.2. USB摄像头测试 202

8.3.3. 查看图像信息 204

8.3.4. 远程传输图像 207

8.3.5. 相机校准 208

8.4. 深度相机(Depth Camera) 214

8.4.1. Depth Camera的类型 215

8.4.2. Depth Camera测试 217

8.4.3. Point Cloud Data(点云数据)的可视化 218

8.4.4. Point Cloud Data相关库 219

8.5. 激光距离传感器 219

8.5.1. LDS传感器距离测量原理 220

8.5.2. LDS测试 221

8.5.3. 可视化LDS的距离值 223

8.5.4. LDS的应用 224

8.6. 电机功能包 226

8.6.1. Dynamixel舵机 226

8.7. 已公开的功能包的用法 227

8.7.1.搜索功能包 228

8.7.2. 安装依赖包 231

8.7.3. 安装功能包 232

8.7.4. 运行功能包 233

第9章 / 嵌入式系统

9.1.OpenCR 238

9.1.1.特点 239

9.1.2. 控制板规格 241

9.1.3. 搭建开发环境 244

9.1.4. OpenCR例程 253

9.2. rosserial 258

9.2.1. rosserial server 259

9.2.2. rosserial client 259

9.2.3. rosserial协议 260

9.2.4. rosserial的约束条件 262

9.2.5. 安装rosserial 263

9.2.6. rosserial例程 265

9.3. TurtleBot3的固件 276

9.3.1. TurtleBot3 Burger固件 276

9.3.2. TurtleBot3 Waffle和Waffle Pi固件 277

9.3.3. TurtleBot3配置固件 278

第10章 / 移动机器人

10.1.ROS支持的机器人 283

10.2.TurtleBot3系列机器人 283

10.3.TurleBot3的硬件 284

10.4.TurtleBot3软件 287

10.5.TurtleBot3的开发环境 288

10.6.TurtleBot3远程控制 291

10.6.1. 遥控TurtleBot3 291

10.6.2.可视化TurtleBot3 293

10.7.Turtlebot3话题 294

10.7.1.订阅话题 296

10.7.2.通过订阅话题控制机器人 296

10.7.3.发布话题 297

10.7.4.通过发布话题识别机器人状态 298

10.8. 使用RViz仿真TurtleBot3 301

10.8.1.仿真 301

10.8.2. 运行虚拟机器人 302

10.8.3.Odometry和TF 303

10.9.利用Gazebo仿真TurtleBot3 307

10.9.1. Gazebo仿真器 307

10.9.2. 启动虚拟机器人 309

10.9.3. 虚拟SLAM和导航 312

第11章 ／ SLAM和导航

11.1.导航及其组成要素 317

11.1.1.移动机器人的导航 317

11.1.2.地图 318

11.1.3. 测量或估计机器人姿态的功能 318

11.1.4. 识别障碍物，如墙壁和物体 321

11.1.5. 计算最优路径和行驶功能 321

11.2.SLAM实习篇 321

11.2.1.对于使用SLAM的机器人的硬件限制 322

11.2.2.SLAM的实验环境 323

11.2.3. 用于SLAM的ROS功能包 324

11.2.4.运行SLAM 324

11.2.5. 利用预先准备好的bag文件运行的SLAM 327

11.3.SLAM应用篇 328

11.3.1.地图 328

11.3.2.SLAM所需的信息 330

11.3.3.SLAM的处理过程 331

11.3.4. 坐标变换(TF) 333

11.3.5.turtlebot3_slam功能包 334

11.4.SLAM理论篇 337

11.4.1.SLAM 337

11.4.2. 多种位置估计(localization)方法论 338

11.5.导航实战篇 342

11.5.1. 用于导航的ROS功能包 342

11.5.2.运行导航 342

11.6. 导航应用程序 345

11.6.1. 导航 345

11.6.2. 导航所需的信息 346

11.6.3.turtlebot3_navigation的各节点和话题状态 348

11.6.4.turtlebot3_navigation设置 349

11.6.5. 设置turtlebot3_navigation的详细参数 354

11.7. 导航理论篇 361

11.7.1.Costmap 361

11.7.2.AMCL 363

11.7.3. Dynamic Window Approach(DWA) 365

第12章 / 服务机器人

12.1.配送服务机器人 368

12.2.配送服务机器人的结构 368

12.2.1.系统结构 368

12.2.2.系统设计 369

12.2.3. 服务核心节点 373

12.2.4.服务主节点 383

12.2.5. 服务从节点 390

12.3. 用ROS Java进行Android平板PC编程 396

第13章 / 机械手臂

13.1.机械手臂介绍 405

13.1.1. 机械手臂的结构和控制 405

13.1.2. 机械手臂和ROS 408

13.2.OpenManipulator建模和仿真 409

13.2.1.OpenManipulator 410

13.2.2.机械手臂建模 410

13.2.3. Gazebo设置 428

13.3.MoveIt! 436

13.3.1.move_group 436

13.3.2. MoveIt! Setup Assistant 437

13.3.3. Gazebo仿真 452

13.4. 应用于实际平台 455

13.4.1. 准备和控制OpenManipulator 456

13.4.2.OpenManipulator与TurtleBot3 Waffle及Waffle Pi 460

463
