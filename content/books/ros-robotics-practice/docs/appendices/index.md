# 附录与资源索引

## 附录A 推荐阅读文献

## 教材

## 机器人学理论

1. 《机器人学导论》(Introduction to Robotics: Mechanics and Control, 3rd Edition)— John J. Craig

- 机器人学理论经典教材，涵盖空间变换、运动学、逆运动学、雅可比、动力学、轨迹规划、线性控制、非线性控制、力控制等

- 源于斯坦福大学课程，理论严谨，例题丰富

2. 《机器人操作的数学导论》(A Mathematical Introduction to Robotic Manipulation)― Richard M. Murray, Zexiang Li, S. Shankar Sastry

- 机器人操作的数学理论，更深入的运动学和动力学分析

3. 《概率机器人》 (Probabilistic Robotics) — Sebastian Thrun, Wolfram Burgard, Dieter Fox - SLAM和定位的理论基础，贝叶斯滤波、粒子滤波、卡尔曼滤波等

4. 《现代机器人学:机构、规划与控制》(Modern Robotics: Mechanics, Planning, and Control) — Kevin M. Lynch, Park Jin-Cheon

- 现代机器人学教材，配套在线课程和MATLAB/Python库， Northwestern大学课程

## ROS编程

5. 《ROS机器人编程》 — 赵汉哲等(ROBOTIS)

- 以TurtleBot3、OpenManipulator、OpenCR为载体，系统讲解ROS1/ROS2使用

- 包含ROS基础、命令、工具、编程、传感器、移动机器人、SLAM导航、机械臂等

6. 《ROS机器人编程实战》(Hands-On ROS for Robotics Programming) — Bernardo Ronquillo Japón

- 以GoPiGo3机器人为载体，从ROS基础到SLAM、导航、视觉的实战指南

7. 《精通ROS机器人编程》(Mastering ROS for Robotics Programming, 3rd Edition) —

Lentin Joseph, Jonathan Cacace

- ROS高级主题，包含插件、MoveIt、视觉、SLAM、多机器人等

8. 《ROS2机器人编程实战》(A Concise Introduction to Robot Programming with ROS2)一 Francisco Martín Rico

- ROS2入门教材，聚焦ROS2新特性和最佳实践

## 在线课程

- 斯坦福 CS223A: Introduction to Robotics - Oussama Khatib (对应Craig教材)

- MIT 6.421: Robotic Manipulation - Russ Tedrake (对应Modern Robotics)

- Northwestern University Modern Robotics - Kevin Lynch (Coursera, 免费)

- ETH Zurich Robot Dynamics — Marco Hutter (高级动力学与控制)

- The Construct / Robot Ignite Academy — ROS在线实战课程

## 网站与文档

- ROS官方文档:https://docs.ros.org/ (ROS2官方文档，最权威)

- ROS Wiki: http://wiki.ros.org/ (ROS1文档, 大量教程)

- MoveIt2文档:https://moveit.picknik.ai/ (机械臂运动规划)

- Nav2文档:https://navigation.ros.org/ (导航栈，配置教程详细)

- Gazebo文档:https://classic.gazebosim.org/ (仿真环境)

- 机器人StackExchange: https://robotics.stackexchange.com/ (问答社区)

- ROS Discourse: https://discourse.ros.org/ (官方讨论论坛)

- ROBOTIS e-Manual: https://emanual.robotis.com/ (TurtleBot3/OpenManipulator官方手册)

## 附录B 常用ROS2命令速查表

## 节点管理

2 ros2 node info /node_name #查看节点详细信息 (话题、服务、动作)

## 话题管理

---

		ros2 topic list 												#列出所有话题

		ros2 topic list -t 												#列出话题及类型

	ros2 topic info /topic_name 												#查看话题信息 (类型、发布者/订阅者数)

4 ros2 topic info -v /topic_name 												#查看详细信息(含QoS)

5 ros2 topic echo /topic_name 												#打印话题消息内容

6 ros2 topic echo --once /topic_name # 只打印一次

7 - ros2 topic pub /topic_name type "\{data\}" # 发布消息

8 * ros2 topic pub -r 1 /topic_name type "\{data\}" # 以1Hz

9 ros2 topic hz /topic_name 												#查看发布频率

10 ros2 topic bw /topic_name 												#查看带宽

11 ros2 topic find type_name 												#查找指定类型的话题

---

## 服务管理

---

			ros2 service list 																							#列出所有服务

		ros2 service list -t 																							#列出服务及类型

		ros2 service type /service_name 																							#查看服务类型

4 * ros2 service call /service_name 																						type "\{request\}" # 调用服务

5 ros2 service find type_name 																								#查找指定类型的服务

---

## 动作管理

---

	ros2 action list 												#列出所有动作

2 ros2 action list -t 												#列出动作及类型

3 ros2 action info /action_name 												#查看动作信息

4 - ros2 action send_goal /action_name type "\{goal\}" # 发送目标

5 - ros2 action send_goal --feedback /action_name type "\{goal\}" # 发送目标并显示

	反馈

---

## 参数管理

#列出所有运行中的节点

---

	ros2 param list /node_name # 列出节点的所有参数

	ros2 param get /node_name param # 获取参数值

	ros2 param set /node_name param value # 设置参数值

4 ros2 param dump /node_name # 导出参数到YAML

	ros2 param load /node_name file.yaml # 从YAML加载参数

6 ros2 param delete /node_name param # 删除参数

7 ros2 param describe /node_name param # 描述参数

---

## 功能包管理

---

	ros2 pkg list 													#列出所有已安装功能包

	ros2 pkg prefix package_name 													#查看功能包安装路径

	ros2 pkg executables package_name # 查看功能包的可执行文件

	ros2 pkg dependencies package_name # 查看功能包依赖

	ros2 pkg create --build-type ament_cmake --dependencies rclcpp std_msgs pk

	g # 创建C++包

6 ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs pk

	g # 创建Python包

---

## 运行与构建

---

				ros2 run package node 																															#运行节点

				ros2 run package node --ros-args 																																p param:=value # 运行时设置参数

				ros2 launch package launch.py 																															#运行launch文件

	4 ros2 launch ./launch.py 																															#运行当前目录的launch文件

	5 colcon build 																															#构建工作空间

6 colcon build --packages-select 																																	#只构建指定包

7 colcon build --symlink-install 																															#符号链接安装(开发用)

		B colcon build --cmake-args -DCMAKE 																															_BUILD_TYPE=Debug # Debug模式

	9 colcon test 																															#运行测试

10 colcon test-result --verbose 																															#查看测试结果

11 source install/setup.bash 																															#加载工作空间环境

---

## TF坐标变换

---

	ros2 run tf2_tools view_frames # 生成TF树图 (frames.pdf)

	ros2 run tf2_ros tf2_echo frame1 frame2 # 查看两坐标系间的变换

3 ros2 run tf2_ros static_transform_publisher x y z qx qy qz qw parent child

	#发布静态变换

4 ros2 topic echo / tf 												#查看动态TF消息

5 ros2 topic echo /tf_static 												#查看静态TF消息

---

## Bag数据记录与回放

---

					ros2 bag record -a 																																								#录制所有话题

					ros2 bag record /topic1 /topic2 																																								#录制指定话题

					ros2 bag record -o name /topic 																																								#指定输出名

	4 ros2 bag record --compression-mode file --compression-format zstd -a # 压

					缩录制

	5 ros2 bag play bag_dir/ 																																								#回放bag

	6 ros2 bag play -1 bag_dir/ 																																								#循环回放

	7 ros2 bag play -r 2.0 bag_dir/ 																																								#2倍速回放

					ros2 bag play --start-offset 10.0 																																								bag_dir/ # 跳过前10秒

				ros2 bag play bag_dir/ --topics / 																																							/scan /odom # 只回放指定话题

10 ros2 bag info bag_dir/ 																																								#查看bag信息

---

## 接口(消息/服务/动作)

---

		ros2 interface list # 列出所有接口

		ros2 interface list | grep LaserScan # 搜索接口

	ros2 interface show std_msgs/msg/String # 查看接口定义

- ros2 interface package sensor_msgs # 列出某个包的所有接口

5 ros2 interface packages 																				#列出所有包含接口的包

---

## 系统诊断

---

		ros2 doctor

		ros2 doctor --report

		ros2 wtf

	ros2 daemon start

ros2 daemon stop

6 ros2 daemon status

---

#系统诊断

#详细诊断报告

#问题排查 (what the failure)

#启动守护进程 (加速命令响应)

#停止守护进程

#查看守护进程状态

## 常用组合命令

---

#查看当前系统所有节点和话题

ros2 node list && ros2 topic list

#查看某个节点发布和订阅的所有话题

ros2 node info /node_name

#录制所有话题并压缩

ros2 bag record -a --compression-mode file --compression-format zstd -o ex

periment1

#查看激光雷达数据的频率和范围

ros2 topic hz /scan

ros2 topic echo /scan --once | head -20

#遥控机器人并同时查看速度命令

ros2 run turtlebot3_teleop teleop_keyboard # 终端1

ros2 topic echo /cmd_vel 	#终端2

---

## 附录C 机器人学数学公式速查

## 空间变换

## 旋转矩阵

绕X轴旋转 $\theta$ :

---

${Rx}\left( \theta \right)  = \lbrack 1$

	[0 cos(θ) -sin(θ)]

	[0 sin(θ) cos(θ)]

---

## 绕Y轴旋转 $\theta$ :

---

${Ry}\left( \theta \right)  = \left\lbrack  \begin{array}{lll} \cos \left( \theta \right) & 0 & \sin \left( \theta \right)  \end{array}\right\rbrack$

	$\left\lbrack  \begin{array}{llllll}  & 0 & & 1 & & 0 \end{array}\right\rbrack$

	[-sin(θ) 0 cos(θ)]

---

绕Z轴旋转 $\theta$ :

---

${Rz}\left( \theta \right)  = \lbrack \cos \left( \theta \right)  - \sin \left( \theta \right) \;0$

	[sin(θ) cos(θ) 0]

	[ 0 ]

---

## 齐次变换矩阵

---

$\mathrm{T} = \left\lbrack  \begin{array}{ll} \mathrm{R} & \mathrm{p} \end{array}\right\rbrack$ 			(4×4矩阵，R为3×3旋转矩阵， $p$ 为3×1位置向量)

	[0 1]

---

## 逆变换

---

1 2 		${T}^{-1} = \left\lbrack  {R}^{T}\right.$ 									$- {R}^{T}p\rbrack$

						[0 										1

---

## 变换复合

---

${}^{ \land  }$ A T_C = ^A T_B × ^B T_C

---

## ZYX欧拉角(Roll-Pitch-Yaw)转旋转矩阵

---

$\mathrm{L}R = {Rz}$ (yaw) $\times  {Ry}$ (pitch) $\times  {Rx}$ (roll)

---

## 四元数

单位四元数 $q = \left\lbrack  {w, x, y, z}\right\rbrack$ ，满足 ${w}^{2} + {x}^{2} + {y}^{2} + {z}^{2} = 1$

四元数转旋转矩阵:

---

$R = \left\lbrack  {1 - 2\left( {{y}^{2} + {z}^{2}}\right) }\right.$ 										2 (xy-zw) 																	2(xz+yw)

		[ 2(xy+zw) 										$1 - 2\left( {{x}^{2} + {z}^{2}}\right)$ 																	2(yz-xw) ]

		[ 2(xz-yw) 											2(yz+xw) 																	$1 - 2\left( {{x}^{2} + {y}^{2}}\right) \rbrack$

---

## D-H参数变换

---

$1\;1\;2\left\lbrack  {i - 1}\right\rbrack  T - i = \operatorname{Rotz}\left( {\theta }_{i}\right)  \times  \operatorname{Transz}\left( {d}_{i}\right)  \times  \operatorname{Transx}\left( {a}_{i}\right)  \times  \operatorname{Rotx}\left( {\alpha }_{i}\right)$

---

展开:

---

																																											^\{i-1\}T_i = [

																															$\left\lbrack  {\cos {\theta }_{i}, - \sin {\theta }_{i}\cos {\alpha }_{i},\sin {\theta }_{i}\sin {\alpha }_{i},{a}_{i}\cos {\theta }_{i}}\right\rbrack  ,$

																[sin ${\theta }_{i}$ , $\cos {\theta }_{i}\cos {\alpha }_{i}$ , $- \cos {\theta }_{i}\sin {\alpha }_{i}$ , ${a}_{i}$ sin ${\theta }_{i}$ ],

								$\left\lbrack  {0,\;\sin {\alpha }_{i},\;\cos {\alpha }_{i},\;{d}_{i}}\right\rbrack$

[ 0, 0, 0, 0, 1 ]

																																										]

---

## 运动学

## 正运动学

---

${}^{0}T = {}^{0}{T}_{1} \times  {}^{1}{T}_{2} \times  \ldots  \times  {}^{n - 1}T$

---

## 二自由度平面臂正运动学

---

$x = {l1}\cos {\theta 1} + {l2}\cos \left( {{\theta 1} + {\theta 2}}\right)$

	$y = {l1}\sin {\theta 1} + {l2}\sin \left( {{\theta 1} + {\theta 2}}\right)$

	$\varphi  = {\theta 1} + {\theta 2}$

---

## 二自由度平面臂逆运动学

---

${r}^{2} = {x}^{2} + {y}^{2}$

		$\cos {\theta 2} = \left( {{r}^{2} - l{1}^{2} - l{2}^{2}}\right) /\left( {2l1l2}\right)$

${\theta 2} =  \pm  \arccos \left( {\cos {\theta 2}}\right)$

${\theta 1} = \operatorname{atan}2\left( {y, x}\right)  - \operatorname{atan}2\left( {{l2}\sin {\theta 2},{l1} + {l2}\cos {\theta 2}}\right)$

---

## 雅可比

## 定义

---

$v = J\left( q\right) \dot{q}$

---

$v = {\left\lbrack  v\_ x, v\_ y, v\_ z,\omega \_ x,\omega \_ y,\omega \_ z\right\rbrack  }^{ \land  }T\left( {6 \times  1}\right)$ ， $\dot{q}$ 为关节速度(n×1)，J为6×n矩阵

## 转动关节i的雅可比列

---

${J}_{i} = \left\lbrack  {{z}_{i - 1} \times  \left( {p - {p}_{i - 1}}\right) }\right\rbrack$

	[Zi-1

---

## 移动关节i的雅可比列

---

${J}_{i} = \left\lbrack  {z}_{i - 1}\right\rbrack$

	[0 ]

---

## 二自由度平面臂雅可比

---

$J = \lbrack  - {l1}\sin {\theta 1} - {l2}\sin \left( {{\theta 1} + {\theta 2}}\right)$

	[ l1 cosθ1 + l2 cos(θ1+θ2)

	[ 1 											1

---

## 力域雅可比(虚功原理)

---

$\tau  = {J}^{\tau }\left( q\right) F$

---

τ为关节力矩(n×1)，F为末端力/力矩(6×1)

## 速度级逆运动学

---

$\dot{q} = {J}^{ + }\dot{x} + \left( {I - {J}^{ + }J}\right) {\dot{q}}_{0}$

---

${\mathrm{J}}^{ + }$ 为伪逆，第二项为零空间投影(冗余度机器人优化次要目标)

## 动力学

## 标准形式

---

$M\left( q\right) \ddot{q} + C\left( {q,\dot{q}}\right) \dot{q} + G\left( q\right)  = \tau$

---

- M(q): nxn质量矩阵 (对称正定)

- $\mathrm{C}\left( {\mathrm{q},\dot{\mathrm{q}}}\right)  : \mathrm{n} \times  \mathrm{n}$ 科氏力/离心力矩阵

- G(q): nx1重力向量

- d: n×1关节力矩

## 牛顿-欧拉递推

- 向外递推:角速度、角加速度、质心加速度(基座→末端)

- 向内递推:力、力矩、关节驱动力矩(末端→基座)

- 复杂度: $O\left( n\right)$

## 拉格朗日方程

---

	$L = K - P$

$d/{dt}\left( {\partial L/\partial {\dot{q}}_{i}}\right)  - \partial L/\partial {q}_{i} = {\tau }_{i}$

---

## 动能

---

$K = \left( {1/2}\right) {\dot{q}}^{T}M\left( q\right) \dot{q}$

---

## 控制

## PID控制

---

$\tau  = {Kp}\mathrm{e} + {Kd}\dot{e} + {Ki}\int e\mathrm{\;d}t$

e = qd - q

---

## 计算力矩控制

---

$\tau  = M\left( q\right) \left\lbrack  {\ddot{q}d + {Kd}\dot{e} + {Kp}\mathrm{e}}\right\rbrack   + C\left( {q,\dot{q}}\right) \dot{q} + G\left( q\right)$

---

代入动力学方程得: $\ddot{e} + {Kd}\dot{e} + {Kp}e = 0$ (线性二阶系统)

## 阻抗控制

---

$1\;M\;d\;\ddot{x} + B\;d\;\dot{x} + {K\;d}\;x = F\;{ext}$

---

- M_d: 期望惯性

- B_d: 期望阻尼

- K_d: 期望刚度

## 阻尼最小二乘法 (DLS, 逆运动学)

---

${\Delta \theta } = {J}^{\top }{\left( J{J}^{\top } + {\lambda }^{2}I\right) }^{-1}{\Delta x}$

---

λ为阻尼系数，接近奇异时增大

## 轨迹生成

## 三次多项式

---

	$\theta \left( t\right)  = {a}_{0} + {a}_{1}t + {a}_{2}{t}^{2} + {a}_{3}{t}^{3}$

2 边界条件: $\theta \left( 0\right)  = {\theta 0},\dot{\theta }\left( 0\right)  = {v0},\theta \left( {tf}\right)  = {\theta f},\dot{\theta }\left( {tf}\right)  = {vf}$

---

## 五次多项式

---

$\theta \left( t\right)  = {a}_{0} + {a}_{1}t + {a}_{2}{t}^{2} + {a}_{3}{t}^{3} + {a}_{4}{t}^{4} + {a}_{5}{t}^{5}$

	边界条件: 增加 $\ddot{\theta }\left( 0\right)  = {a0},\ddot{\theta }\left( {tf}\right)  = {af}$

---

## 梯形速度

- 加速段(抛物线，加速度恒定)

- 匀速段(速度恒定)

- 减速段(抛物线，加速度恒定)

## 差速机器人运动学

## 正运动学

---

$v = \left( {v - r + v - l}\right) /2$

	$\omega  = \left( {v - r - {vl}}\right) /B$

---

$v\_ r/v\_ l$ 为右/左轮线速度, B为轮距

## 逆运动学

---

$v - l = v - {\omega B}/2$

	$v - r = v + {\omega B}/2$

---

## 里程计

---

${\Delta d} = \left( {{\Delta d} - 1 + {\Delta d} - r}\right) /2$

	${\Delta \theta } = \left( {\Delta {d}_{ - }r - \Delta {d}_{ - }l}\right) /B$

	$x +  = {\Delta d}\cos \left( {\theta  + {\Delta \theta }/2}\right)$

	$y +  = {\Delta d}\sin \left( {\theta  + {\Delta \theta }/2}\right)$

$\theta  = {\Delta \theta }$

---

## 附录D GitHub开源项目精选

## ROS核心框架

<table><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>ros2</td><td>ROS2核心仓库，包含客户端库、DDS适配、构建工具等</td><td>https://github.com/ros2/ros2</td></tr><tr><td>rclcpp</td><td>ROS2 C++客户端库</td><td>https://github.com/ros2/rclc pp</td></tr><tr><td>rclpy</td><td>ROS2 Python客户端库</td><td>https://github.com/ros2/rclp y</td></tr><tr><td>examples</td><td>ROS2官方示例代码</td><td>https://github.com/ros2/exa mples</td></tr></table>

<table><tr><td>design</td><td>ROS2设计文档</td><td>https://github.com/ros2/desi gn</td></tr></table>

## 导航与SLAM

<table><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>navigation2</td><td>ROS2官方导航栈，包含规划器、控制器、恢复行为、行为树</td><td>https://github.com/ros-navigation/navigation2</td></tr><tr><td>slam_toolbox</td><td>ROS2推荐的2D SLAM工具包，支持 lifelong mapping</td><td>https://github.com/SteveMac enski/slam_toolbox</td></tr><tr><td>cartographer</td><td>Google开源的SLAM系统，支持2D/3D，图优化</td><td>https://github.com/cartograp her-project/cartographer</td></tr><tr><td>cartographer_ros</td><td>Cartographer的ROS集成</td><td>https://github.com/cartograp her-project/cartographer_ros</td></tr><tr><td>amcl</td><td>自适应蒙特卡洛定位(ROS2版本在navigation2中)</td><td>https://github.com/ros-planning/navigation2</td></tr><tr><td>robot_localization</td><td>EKF/UKF多传感器融合定位</td><td>https://github.com/cra-ros-pkg/robot_localization</td></tr></table>

## 机械臂与运动规划

<table id="cross-table-7"><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>moveit2</td><td>ROS2机械臂运动规划框架，运动学/规划/碰撞/抓取</td><td>https://github.com/moveit/m oveit2</td></tr><tr><td>moveit2_tutorials</td><td>MoveIt2官方教程</td><td>https://github.com/moveit/m oveit2_tutorials</td></tr><tr><td>ompl</td><td>开放运动规划库(OMPL)， MoveIt默认规划库</td><td>https://github.com/ompl/om pl</td></tr><tr><td>trac_ik</td><td>改进的逆运动学求解器，比KDL 更鲁棒</td><td>https://github.com/traclabs/t rac_ik</td></tr><tr><td>descartes</td><td>笛卡尔路径规划器</td><td>https://github.com/ros-industrial-consortium/descartes</td></tr><tr><td>pilz_industrial_motion</td><td>工业机器人运动规划 (PTP/LIN/CIRC)</td><td>https://github.com/PilzDE/pil z_industrial_motion</td></tr></table>

## 控制

<table><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>ros2_control</td><td>ROS2官方控制框架，硬件抽象 +控制器管理</td><td>https://github.com/ros-controls/ros2_control</td></tr><tr><td>ros2_controllers</td><td>ros2_control的控制器集合(位置/速度/力矩/差速/关节轨迹)</td><td>https://github.com/ros-controls/ros2_controllers</td></tr><tr><td>control_toolbox</td><td>控制工具箱(PID、滤波器等)</td><td>https://github.com/ros-controls/control_toolbox</td></tr><tr><td>eigen_stl_containers</td><td>Eigen STL容器</td><td>https://github.com/ros/eigen _stl_containers</td></tr></table>

## 仿真与可视化

<table id="cross-table-8"><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>gazebo</td><td>Gazebo Classic物理仿真器</td><td>https://github.com/gazebosi m/gazebo-classic</td></tr><tr><td>gz-sim</td><td>Gazebo Sim(新一代，原 Ignition)</td><td>https://github.com/gazebosi m/gz-sim</td></tr><tr><td>gazebo_ros_pkgs</td><td>Gazebo的ROS2集成插件</td><td>https://github.com/ros-simulation/gazebo_ros_pkgs</td></tr><tr><td>rviz</td><td>RViz三维可视化工具(ROS2版本)</td><td>https://github.com/ros2/rviz</td></tr><tr><td>webots</td><td>开源机器人仿真器 (Cyberbotics)</td><td>https://github.com/cyberboti cs/webots</td></tr><tr><td>mujoco</td><td>MuJoCo物理引擎(Google DeepMind开源)</td><td>https://github.com/google-deepmind/mujoco</td></tr><tr><td>Isaac Sim</td><td>NVIDIA机器人仿真平台</td><td>https://developer.nvidia.com/ isaac-sim</td></tr></table>

## 机器人学理论与算法

<table id="cross-table-9"><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>pinocchio</td><td>高效刚体动力学库 (C++/Python)，运动学/动力学/雅可比/解析导数</td><td>https://github.com/stack-of-tasks/pinocchio</td></tr><tr><td>Drake</td><td>机器人动力学与控制(MIT， C++/Python)</td><td>https://github.com/RobotLoc omotion/drake</td></tr><tr><td>iDynTree</td><td>机器人动力学库(IIT，多体动力学)</td><td>https://github.com/robotolog y/idyntree</td></tr><tr><td>qpOASES</td><td>二次规划求解器(用于 MPC/WBC)</td><td>https://github.com/coin-or/qpOASES</td></tr><tr><td>OSQP</td><td>算子分裂二次规划求解器</td><td>https://github.com/osqp/osq p</td></tr><tr><td>ModernRobotics</td><td>Modern Robotics教材的 MATLAB/Python库</td><td>https://github.com/NxRLab/ ModernRobotics</td></tr><tr><td>MATLAB-For-Robotics</td><td>Craig教材的MATLAB代码(变换/运动学/动力学/轨迹/控制)</td><td>https://github.com/SakethGG /MATLAB-For-Robotics-concepts</td></tr><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>vision_opencv</td><td>OpenCV的ROS2集成 (cv_bridge、 image_geometry)</td><td>https://github.com/ros-perception/vision_opencv</td></tr><tr><td>image_pipeline</td><td>图像处理流水线(相机标定、矫正、深度处理)</td><td>https://github.com/ros-perception/image_pipeline</td></tr><tr><td>pcl</td><td>点云库(PCL)</td><td>https://github.com/PointClou dLibrary/pcl</td></tr><tr><td>perception_pcl</td><td>PCL的ROS2集成</td><td>https://github.com/ros-perception/perception_pcl</td></tr><tr><td>Open3D</td><td>现代点云处理库(Python友好)</td><td>https://github.com/isl-org/Open3D</td></tr><tr><td>realsense-ros</td><td>Intel RealSense相机的ROS2驱动</td><td>https://github.com/IntelRealS ense/realsense-ros</td></tr><tr><td>ORB-SLAM3</td><td>视觉SLAM(单目/双目/RGBD/IMU)</td><td>https://github.com/UZ-SLAMLab/ORB_SLAM3</td></tr><tr><td>yolov5</td><td>YOLOv5目标检测</td><td>https://github.com/ultralytics /yolov5</td></tr></table>

## 感知与视觉

## 机器人平台

<table id="cross-table-10"><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>turtlebot3</td><td>TurtleBot3官方仓库(固件/驱动/仿真/SLAM/导航/应用)</td><td>https://github.com/ROBOTIS -GIT/turtlebot3</td></tr><tr><td>turtlebot3_simulations</td><td>TurtleBot3仿真(Gazebo模型/ 世界)</td><td>https://github.com/ROBOTIS -GIT/turtlebot3_simulations</td></tr><tr><td>open_manipulator</td><td>OpenManipulator机械臂(驱动/MoveIt/仿真)</td><td>https://github.com/ROBOTIS -GIT/open_manipulator</td></tr><tr><td>OpenCR</td><td>OpenCR控制板(固件/Arduino 库/ROS)</td><td>https://github.com/ROBOTIS -GIT/OpenCR</td></tr><tr><td>DynamixelSDK</td><td>Dynamixel舵机SDK (C++/Python/Java等)</td><td>https://github.com/ROBOTIS -GIT/DynamixelSDK</td></tr><tr><td>universal_robot</td><td>Universal Robots机械臂驱动 (UR3/5/10/e系列)</td><td>https://github.com/Universal Robots/Universal_Robots_RO S2_Driver</td></tr><tr><td>franka_ros</td><td>Franka Emika Panda机械臂 (libfranka/ROS)</td><td>https://github.com/frankaemi ka/franka_ros</td></tr><tr><td>Husky</td><td>Clearpath Husky移动机器人</td><td>https://github.com/husky/hu sky</td></tr></table>

## 教程与学习资源

<table id="cross-table-11"><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>ros2_for_beginners_code</td><td>ROS2初学者代码(按章节， C++/Python，话题/服务/动作/TF/导航/MoveIt)</td><td>https://github.com/homalozo a/ros2_for_beginners_code</td></tr><tr><td>ROS-Theory-Practice</td><td>ROS理论与实践教程代码(建模/仿真/导航/实体)</td><td>https://github.com/jingxuany ang/ROS-Theory-Practice</td></tr><tr><td>how-to-learn-robotics</td><td>开源机器人学学习指南(数学/ 运动学/动力学/控制/ROS)</td><td>https://github.com/ysu341/h ow-to-learn-robotics</td></tr><tr><td>Hands-On-ROS</td><td>《ROS机器人编程实战》配套代码(GoPiGo3/SLAM/导航/ 视觉)</td><td>https://github.com/PacktPubl ishing/Hands-On-ROS-for-Robotics-Programming</td></tr><tr><td>ros_robotics_projects</td><td>ROS机器人项目实例(人脸识别/聊天/手势/目标检测/深度学习/SLAM)</td><td>https://github.com/qboticsla bs/ros_robotics_projects</td></tr><tr><td>Mastering-ROS</td><td>《精通ROS机器人编程》配套代码(传感器/执行器/融合/机械臂/插件)</td><td>https://github.com/PacktPubl ishing/Mastering-ROS-for-Robotics-Programming-Third-edition</td></tr><tr><td>ros2_knowledge</td><td>ROS2知识整理(概念/命令/最佳实践)</td><td>https://github.com/zhangrela y/ros2_knowledge</td></tr><tr><td>awesome-ros2</td><td>ROS2精选资源列表</td><td>https://github.com/vmayoral/ awesome-ros2</td></tr></table>

## 开发工具

<table><tr><td>项目</td><td>说明</td><td>链接</td></tr><tr><td>colcon</td><td>ROS2构建工具</td><td>https://github.com/colcon/co lcon-core</td></tr><tr><td>rosdep</td><td>ROS依赖管理工具</td><td>https://github.com/ros-infrastructure/rosdep</td></tr><tr><td>vcstool</td><td>版本控制工具(管理多个仓库)</td><td>https://github.com/dirk-thomas/vcstool</td></tr><tr><td>catkin</td><td>ROS1构建工具(兼容)</td><td>https://github.com/ros/catki n</td></tr><tr><td>plotjuggler</td><td>数据可视化工具(ROS话题/CSV，比rqt_plot强大)</td><td>https://github.com/facontida vide/PlotJuggler</td></tr><tr><td>foxglove-studio</td><td>机器人数据可视化平台(替代 RViz, Web/桌面)</td><td>https://github.com/foxglove/ studio</td></tr></table>

本书完

本书融合了《机器人学导论》(John J. Craig)的理论体系与《ROS机器人编程》(ROBOTIS)的工程实践，涵盖从空间变换、运动学、动力学、控制理论，到ROS环境搭建、通信机制、传感器、建模仿真、SLAM导航、机械臂控制，再到综合项目实战的完整知识体系。

每章均嵌入了相关的B站视频教程和GitHub开源项目，建议读者边学边练，在仿真环境中验证理论，在实体机器人上积累工程经验。

理论是实践的基础，实践是理论的验证。祝你在机器人学的学习道路上不断进步！

本书基于两本经典教材的公开目录和知识体系编写，仅供学习参考。如需深入学习，请阅读原书。
