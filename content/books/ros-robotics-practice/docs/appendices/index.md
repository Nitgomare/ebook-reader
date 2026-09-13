# 附录与资源索引

---

## 附录A 推荐阅读文献
## 教材
### 机器人学理论
1. **《机器人学导论》（Introduction to Robotics: Mechanics and Control, 3rd Edition）** — John J. Craig
    - 机器人学理论经典教材，涵盖空间变换、运动学、逆运动学、雅可比、动力学、轨迹规划、线性控制、非线性控制、力控制等
    - 源于斯坦福大学课程，理论严谨，例题丰富
2. **《机器人操作的数学导论》（A Mathematical Introduction to Robotic Manipulation）** — Richard M. Murray, Zexiang Li, S. Shankar Sastry
    - 机器人操作的数学理论，更深入的运动学和动力学分析
3. **《概率机器人》（Probabilistic Robotics）** — Sebastian Thrun, Wolfram Burgard, Dieter Fox
    - SLAM和定位的理论基础，贝叶斯滤波、粒子滤波、卡尔曼滤波等
4. **《现代机器人学：机构、规划与控制》（Modern Robotics: Mechanics, Planning, and Control）** — Kevin M. Lynch, Park Jin-Cheon
    - 现代机器人学教材，配套在线课程和MATLAB/Python库， Northwestern大学课程

### ROS编程
5. **《ROS机器人编程》** — 赵汉哲等（ROBOTIS）
    - 以TurtleBot3、OpenManipulator、OpenCR为载体，系统讲解ROS1/ROS2使用
    - 包含ROS基础、命令、工具、编程、传感器、移动机器人、SLAM导航、机械臂等
6. **《ROS机器人编程实战》（Hands-On ROS for Robotics Programming）** — Bernardo Ronquillo Japón
    - 以GoPiGo3机器人为载体，从ROS基础到SLAM、导航、视觉的实战指南
7. **《精通ROS机器人编程》（Mastering ROS for Robotics Programming, 3rd Edition）** — Lentin Joseph, Jonathan Cacace
    - ROS高级主题，包含插件、MoveIt、视觉、SLAM、多机器人等
8. **《ROS2机器人编程实战》（A Concise Introduction to Robot Programming with ROS2）** — Francisco Martín Rico
    - ROS2入门教材，聚焦ROS2新特性和最佳实践

## 在线课程
+ **斯坦福 CS223A：Introduction to Robotics** — Oussama Khatib（对应Craig教材）
+ **MIT 6.421：Robotic Manipulation** — Russ Tedrake（对应Modern Robotics）
+ **Northwestern University Modern Robotics** — Kevin Lynch（Coursera，免费）
+ **ETH Zurich Robot Dynamics** — Marco Hutter（高级动力学与控制）
+ **The Construct / Robot Ignite Academy** — ROS在线实战课程

## 网站与文档
+ **ROS官方文档**：[https://docs.ros.org/](https://docs.ros.org/) （ROS2官方文档，最权威）
+ **ROS Wiki**：[http://wiki.ros.org/](http://wiki.ros.org/) （ROS1文档，大量教程）
+ **MoveIt2文档**：[https://moveit.picknik.ai/](https://moveit.picknik.ai/) （机械臂运动规划）
+ **Nav2文档**：[https://navigation.ros.org/](https://navigation.ros.org/) （导航栈，配置教程详细）
+ **Gazebo文档**：[https://classic.gazebosim.org/](https://classic.gazebosim.org/) （仿真环境）
+ **机器人StackExchange**：[https://robotics.stackexchange.com/](https://robotics.stackexchange.com/) （问答社区）
+ **ROS Discourse**：[https://discourse.ros.org/](https://discourse.ros.org/) （官方讨论论坛）
+ **ROBOTIS e-Manual**：[https://emanual.robotis.com/](https://emanual.robotis.com/) （TurtleBot3/OpenManipulator官方手册）

---

## 附录B 常用ROS2命令速查表
## 节点管理
```bash
ros2 node list                    # 列出所有运行中的节点
ros2 node info /node_name         # 查看节点详细信息（话题、服务、动作）
```

## 话题管理
```bash
ros2 topic list                   # 列出所有话题
ros2 topic list -t                # 列出话题及类型
ros2 topic info /topic_name       # 查看话题信息（类型、发布者/订阅者数）
ros2 topic info -v /topic_name    # 查看详细信息（含QoS）
ros2 topic echo /topic_name       # 打印话题消息内容
ros2 topic echo --once /topic_name # 只打印一次
ros2 topic pub /topic_name type "{data}"  # 发布消息
ros2 topic pub -r 1 /topic_name type "{data}"  # 以1Hz频率发布
ros2 topic hz /topic_name         # 查看发布频率
ros2 topic bw /topic_name         # 查看带宽
ros2 topic find type_name         # 查找指定类型的话题
```

## 服务管理
```bash
ros2 service list                 # 列出所有服务
ros2 service list -t              # 列出服务及类型
ros2 service type /service_name   # 查看服务类型
ros2 service call /service_name type "{request}"  # 调用服务
ros2 service find type_name       # 查找指定类型的服务
```

## 动作管理
```bash
ros2 action list                  # 列出所有动作
ros2 action list -t               # 列出动作及类型
ros2 action info /action_name     # 查看动作信息
ros2 action send_goal /action_name type "{goal}"  # 发送目标
ros2 action send_goal --feedback /action_name type "{goal}"  # 发送目标并显示反馈
```

## 参数管理
```bash
ros2 param list /node_name        # 列出节点的所有参数
ros2 param get /node_name param   # 获取参数值
ros2 param set /node_name param value  # 设置参数值
ros2 param dump /node_name        # 导出参数到YAML
ros2 param load /node_name file.yaml  # 从YAML加载参数
ros2 param delete /node_name param  # 删除参数
ros2 param describe /node_name param  # 描述参数
```

## 功能包管理
```bash
ros2 pkg list                     # 列出所有已安装功能包
ros2 pkg prefix package_name      # 查看功能包安装路径
ros2 pkg executables package_name # 查看功能包的可执行文件
ros2 pkg dependencies package_name # 查看功能包依赖
ros2 pkg create --build-type ament_cmake --dependencies rclcpp std_msgs pkg  # 创建C++包
ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs pkg    # 创建Python包
```

## 运行与构建
```bash
ros2 run package node             # 运行节点
ros2 run package node --ros-args -p param:=value  # 运行时设置参数
ros2 launch package launch.py     # 运行launch文件
ros2 launch ./launch.py           # 运行当前目录的launch文件
colcon build                      # 构建工作空间
colcon build --packages-select pkg  # 只构建指定包
colcon build --symlink-install    # 符号链接安装（开发用）
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Debug  # Debug模式
colcon test                       # 运行测试
colcon test-result --verbose      # 查看测试结果
source install/setup.bash         # 加载工作空间环境
```

## TF坐标变换
```bash
ros2 run tf2_tools view_frames   # 生成TF树图（frames.pdf）
ros2 run tf2_ros tf2_echo frame1 frame2  # 查看两坐标系间的变换
ros2 run tf2_ros static_transform_publisher x y z qx qy qz qw parent child  # 发布静态变换
ros2 topic echo /tf               # 查看动态TF消息
ros2 topic echo /tf_static        # 查看静态TF消息
```

## Bag数据记录与回放
```bash
ros2 bag record -a                # 录制所有话题
ros2 bag record /topic1 /topic2   # 录制指定话题
ros2 bag record -o name /topic    # 指定输出名
ros2 bag record --compression-mode file --compression-format zstd -a  # 压缩录制
ros2 bag play bag_dir/            # 回放bag
ros2 bag play -l bag_dir/         # 循环回放
ros2 bag play -r 2.0 bag_dir/     # 2倍速回放
ros2 bag play --start-offset 10.0 bag_dir/  # 跳过前10秒
ros2 bag play bag_dir/ --topics /scan /odom  # 只回放指定话题
ros2 bag info bag_dir/            # 查看bag信息
```

## 接口（消息/服务/动作）
```bash
ros2 interface list               # 列出所有接口
ros2 interface list | grep LaserScan  # 搜索接口
ros2 interface show std_msgs/msg/String  # 查看接口定义
ros2 interface package sensor_msgs  # 列出某个包的所有接口
ros2 interface packages           # 列出所有包含接口的包
```

## 系统诊断
```bash
ros2 doctor                       # 系统诊断
ros2 doctor --report              # 详细诊断报告
ros2 wtf                          # 问题排查（what the failure）
ros2 daemon start                 # 启动守护进程（加速命令响应）
ros2 daemon stop                  # 停止守护进程
ros2 daemon status                # 查看守护进程状态
```

## 常用组合命令
```bash
# 查看当前系统所有节点和话题
ros2 node list && ros2 topic list

# 查看某个节点发布和订阅的所有话题
ros2 node info /node_name

# 录制所有话题并压缩
ros2 bag record -a --compression-mode file --compression-format zstd -o experiment1

# 查看激光雷达数据的频率和范围
ros2 topic hz /scan
ros2 topic echo /scan --once | head -20

# 遥控机器人并同时查看速度命令
ros2 run turtlebot3_teleop teleop_keyboard  # 终端1
ros2 topic echo /cmd_vel                      # 终端2
```

---

## 附录C 机器人学数学公式速查
## 空间变换
### 旋转矩阵
**绕X轴旋转θ：**

```plain
Rx(θ) = [1    0       0   ]
        [0  cos(θ) -sin(θ)]
        [0  sin(θ)  cos(θ)]
```

**绕Y轴旋转θ：**

```plain
Ry(θ) = [ cos(θ)  0  sin(θ)]
        [   0     1    0   ]
        [-sin(θ)  0  cos(θ)]
```

**绕Z轴旋转θ：**

```plain
Rz(θ) = [cos(θ) -sin(θ)  0]
        [sin(θ)  cos(θ)  0]
        [  0       0     1]
```

### 齐次变换矩阵
```plain
T = [R  p]    （4×4矩阵，R为3×3旋转矩阵，p为3×1位置向量）
    [0  1]
```

### 逆变换
```plain
T⁻¹ = [Rᵀ  -Rᵀp]
      [0     1  ]
```

### 变换复合
```plain
^A T_C = ^A T_B × ^B T_C
```

### ZYX欧拉角（Roll-Pitch-Yaw）转旋转矩阵
```plain
R = Rz(yaw) × Ry(pitch) × Rx(roll)
```

### 四元数
单位四元数 q = [w, x, y, z]，满足 w² + x² + y² + z² = 1  
四元数转旋转矩阵：

```plain
R = [1-2(y²+z²)    2(xy-zw)      2(xz+yw)  ]
    [  2(xy+zw)    1-2(x²+z²)    2(yz-xw)  ]
    [  2(xz-yw)      2(yz+xw)    1-2(x²+y²)]
```

## D-H参数变换
```plain
^{i-1}T_i = Rotz(θᵢ) × Transz(dᵢ) × Transx(aᵢ) × Rotx(αᵢ)
```

展开：

```plain
^{i-1}T_i = [
[cosθᵢ, -sinθᵢ cosαᵢ,  sinθᵢ sinαᵢ, aᵢ cosθᵢ],
[sinθᵢ,  cosθᵢ cosαᵢ, -cosθᵢ sinαᵢ, aᵢ sinθᵢ],
[  0,       sinαᵢ,        cosαᵢ,       dᵢ     ],
[  0,         0,             0,          1      ]
]
```

## 运动学
### 正运动学
```plain
⁰Tₙ = ⁰T₁ × ¹T₂ × ... × ⁿ⁻¹Tₙ
```

### 二自由度平面臂正运动学
```plain
x = l1 cosθ1 + l2 cos(θ1+θ2)
y = l1 sinθ1 + l2 sin(θ1+θ2)
φ = θ1 + θ2
```

### 二自由度平面臂逆运动学
```plain
r² = x² + y²
cosθ2 = (r² - l1² - l2²) / (2 l1 l2)
θ2 = ± arccos(cosθ2)
θ1 = atan2(y, x) - atan2(l2 sinθ2, l1 + l2 cosθ2)
```

## 雅可比
### 定义
```plain
v = J(q) q̇
```

v = [v_x, v_y, v_z, ω_x, ω_y, ω_z]^T（6×1），q̇为关节速度（n×1），J为6×n矩阵

### 转动关节i的雅可比列
```plain
Jᵢ = [zᵢ₋₁ × (pₙ - pᵢ₋₁)]
     [zᵢ₋₁                ]
```

### 移动关节i的雅可比列
```plain
Jᵢ = [zᵢ₋₁]
     [  0  ]
```

### 二自由度平面臂雅可比
```plain
J = [-l1 sinθ1 - l2 sin(θ1+θ2)   -l2 sin(θ1+θ2)]
    [ l1 cosθ1 + l2 cos(θ1+θ2)    l2 cos(θ1+θ2)]
    [            1                          1       ]
```

### 力域雅可比（虚功原理）
```plain
τ = Jᵀ(q) F
```

τ为关节力矩（n×1），F为末端力/力矩（6×1）

### 速度级逆运动学
```plain
q̇ = J⁺ ẋ + (I - J⁺J) q̇₀
```

J⁺为伪逆，第二项为零空间投影（冗余度机器人优化次要目标）

## 动力学
### 标准形式
```plain
M(q) q̈ + C(q, q̇) q̇ + G(q) = τ
```

+ M(q)：n×n质量矩阵（对称正定）
+ C(q,q̇)：n×n科氏力/离心力矩阵
+ G(q)：n×1重力向量
+ τ：n×1关节力矩

### 牛顿-欧拉递推
+ 向外递推：角速度、角加速度、质心加速度（基座→末端）
+ 向内递推：力、力矩、关节驱动力矩（末端→基座）
+ 复杂度：O(n)

### 拉格朗日方程
```plain
L = K - P
d/dt (∂L/∂q̇ᵢ) - ∂L/∂qᵢ = τᵢ
```

### 动能
```plain
K = (1/2) q̇ᵀ M(q) q̇
```

## 控制
### PID控制
```plain
τ = Kp e + Kd ė + Ki ∫e dt
e = qd - q
```

### 计算力矩控制
```plain
τ = M(q)[q̈d + Kd ė + Kp e] + C(q,q̇)q̇ + G(q)
```

代入动力学方程得：ë + Kd ė + Kp e = 0（线性二阶系统）

### 阻抗控制
```plain
M_d ẍ + B_d ẋ + K_d x = F_ext
```

+ M_d：期望惯性
+ B_d：期望阻尼
+ K_d：期望刚度

### 阻尼最小二乘法（DLS，逆运动学）
```plain
Δθ = Jᵀ (J Jᵀ + λ² I)⁻¹ Δx
```

λ为阻尼系数，接近奇异时增大

## 轨迹生成
### 三次多项式
```plain
θ(t) = a₀ + a₁t + a₂t² + a₃t³
边界条件：θ(0)=θ0, θ̇(0)=v0, θ(tf)=θf, θ̇(tf)=vf
```

### 五次多项式
```plain
θ(t) = a₀ + a₁t + a₂t² + a₃t³ + a₄t⁴ + a₅t⁵
边界条件：增加θ̈(0)=a0, θ̈(tf)=af
```

### 梯形速度
+ 加速段（抛物线，加速度恒定）
+ 匀速段（速度恒定）
+ 减速段（抛物线，加速度恒定）

## 差速机器人运动学
### 正运动学
```plain
v = (v_r + v_l) / 2
ω = (v_r - v_l) / B
```

v_r/v_l为右/左轮线速度，B为轮距

### 逆运动学
```plain
v_l = v - ω B/2
v_r = v + ω B/2
```

### 里程计
```plain
Δd = (Δd_l + Δd_r) / 2
Δθ = (Δd_r - Δd_l) / B
x += Δd cos(θ + Δθ/2)
y += Δd sin(θ + Δθ/2)
θ += Δθ
```

---

## 附录D GitHub开源项目精选
## ROS核心框架
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| ros2 | ROS2核心仓库，包含客户端库、DDS适配、构建工具等 | [https://github.com/ros2/ros2](https://github.com/ros2/ros2) |
| rclcpp | ROS2 C++客户端库 | [https://github.com/ros2/rclcpp](https://github.com/ros2/rclcpp) |
| rclpy | ROS2 Python客户端库 | [https://github.com/ros2/rclpy](https://github.com/ros2/rclpy) |
| examples | ROS2官方示例代码 | [https://github.com/ros2/examples](https://github.com/ros2/examples) |
| design | ROS2设计文档 | [https://github.com/ros2/design](https://github.com/ros2/design) |


## 导航与SLAM
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| navigation2 | ROS2官方导航栈，包含规划器、控制器、恢复行为、行为树 | [https://github.com/ros-navigation/navigation2](https://github.com/ros-navigation/navigation2) |
| slam_toolbox | ROS2推荐的2D SLAM工具包，支持 lifelong mapping | [https://github.com/SteveMacenski/slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) |
| cartographer | Google开源的SLAM系统，支持2D/3D，图优化 | [https://github.com/cartographer-project/cartographer](https://github.com/cartographer-project/cartographer) |
| cartographer_ros | Cartographer的ROS集成 | [https://github.com/cartographer-project/cartographer_ros](https://github.com/cartographer-project/cartographer_ros) |
| amcl | 自适应蒙特卡洛定位（ROS2版本在navigation2中） | [https://github.com/ros-planning/navigation2](https://github.com/ros-planning/navigation2) |
| robot_localization | EKF/UKF多传感器融合定位 | [https://github.com/cra-ros-pkg/robot_localization](https://github.com/cra-ros-pkg/robot_localization) |


## 机械臂与运动规划
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| moveit2 | ROS2机械臂运动规划框架，运动学/规划/碰撞/抓取 | [https://github.com/moveit/moveit2](https://github.com/moveit/moveit2) |
| moveit2_tutorials | MoveIt2官方教程 | [https://github.com/moveit/moveit2_tutorials](https://github.com/moveit/moveit2_tutorials) |
| ompl | 开放运动规划库（OMPL），MoveIt默认规划库 | [https://github.com/ompl/ompl](https://github.com/ompl/ompl) |
| trac_ik | 改进的逆运动学求解器，比KDL更鲁棒 | [https://github.com/traclabs/trac_ik](https://github.com/traclabs/trac_ik) |
| descartes | 笛卡尔路径规划器 | [https://github.com/ros-industrial-consortium/descartes](https://github.com/ros-industrial-consortium/descartes) |
| pilz_industrial_motion | 工业机器人运动规划（PTP/LIN/CIRC） | [https://github.com/PilzDE/pilz_industrial_motion](https://github.com/PilzDE/pilz_industrial_motion) |


## 控制
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| ros2_control | ROS2官方控制框架，硬件抽象+控制器管理 | [https://github.com/ros-controls/ros2_control](https://github.com/ros-controls/ros2_control) |
| ros2_controllers | ros2_control的控制器集合（位置/速度/力矩/差速/关节轨迹） | [https://github.com/ros-controls/ros2_controllers](https://github.com/ros-controls/ros2_controllers) |
| control_toolbox | 控制工具箱（PID、滤波器等） | [https://github.com/ros-controls/control_toolbox](https://github.com/ros-controls/control_toolbox) |
| eigen_stl_containers | Eigen STL容器 | [https://github.com/ros/eigen_stl_containers](https://github.com/ros/eigen_stl_containers) |


## 仿真与可视化
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| gazebo | Gazebo Classic物理仿真器 | [https://github.com/gazebosim/gazebo-classic](https://github.com/gazebosim/gazebo-classic) |
| gz-sim | Gazebo Sim（新一代，原Ignition） | [https://github.com/gazebosim/gz-sim](https://github.com/gazebosim/gz-sim) |
| gazebo_ros_pkgs | Gazebo的ROS2集成插件 | [https://github.com/ros-simulation/gazebo_ros_pkgs](https://github.com/ros-simulation/gazebo_ros_pkgs) |
| rviz | RViz三维可视化工具（ROS2版本） | [https://github.com/ros2/rviz](https://github.com/ros2/rviz) |
| webots | 开源机器人仿真器（Cyberbotics） | [https://github.com/cyberbotics/webots](https://github.com/cyberbotics/webots) |
| mujoco | MuJoCo物理引擎（Google DeepMind开源） | [https://github.com/google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) |
| Isaac Sim | NVIDIA机器人仿真平台 | [https://developer.nvidia.com/isaac-sim](https://developer.nvidia.com/isaac-sim) |


## 机器人学理论与算法
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| pinocchio | 高效刚体动力学库（C++/Python），运动学/动力学/雅可比/解析导数 | [https://github.com/stack-of-tasks/pinocchio](https://github.com/stack-of-tasks/pinocchio) |
| Drake | 机器人动力学与控制（MIT，C++/Python） | [https://github.com/RobotLocomotion/drake](https://github.com/RobotLocomotion/drake) |
| iDynTree | 机器人动力学库（IIT，多体动力学） | [https://github.com/robotology/idyntree](https://github.com/robotology/idyntree) |
| qpOASES | 二次规划求解器（用于MPC/WBC） | [https://github.com/coin-or/qpOASES](https://github.com/coin-or/qpOASES) |
| OSQP | 算子分裂二次规划求解器 | [https://github.com/osqp/osqp](https://github.com/osqp/osqp) |
| ModernRobotics | Modern Robotics教材的MATLAB/Python库 | [https://github.com/NxRLab/ModernRobotics](https://github.com/NxRLab/ModernRobotics) |
| MATLAB-For-Robotics | Craig教材的MATLAB代码（变换/运动学/动力学/轨迹/控制） | [https://github.com/SakethGG/MATLAB-For-Robotics-concepts](https://github.com/SakethGG/MATLAB-For-Robotics-concepts) |


## 感知与视觉
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| vision_opencv | OpenCV的ROS2集成（cv_bridge、image_geometry） | [https://github.com/ros-perception/vision_opencv](https://github.com/ros-perception/vision_opencv) |
| image_pipeline | 图像处理流水线（相机标定、矫正、深度处理） | [https://github.com/ros-perception/image_pipeline](https://github.com/ros-perception/image_pipeline) |
| pcl | 点云库（PCL） | [https://github.com/PointCloudLibrary/pcl](https://github.com/PointCloudLibrary/pcl) |
| perception_pcl | PCL的ROS2集成 | [https://github.com/ros-perception/perception_pcl](https://github.com/ros-perception/perception_pcl) |
| Open3D | 现代点云处理库（Python友好） | [https://github.com/isl-org/Open3D](https://github.com/isl-org/Open3D) |
| realsense-ros | Intel RealSense相机的ROS2驱动 | [https://github.com/IntelRealSense/realsense-ros](https://github.com/IntelRealSense/realsense-ros) |
| ORB-SLAM3 | 视觉SLAM（单目/双目/RGBD/IMU） | [https://github.com/UZ-SLAMLab/ORB_SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3) |
| yolov5 | YOLOv5目标检测 | [https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5) |


## 机器人平台
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| turtlebot3 | TurtleBot3官方仓库（固件/驱动/仿真/SLAM/导航/应用） | [https://github.com/ROBOTIS-GIT/turtlebot3](https://github.com/ROBOTIS-GIT/turtlebot3) |
| turtlebot3_simulations | TurtleBot3仿真（Gazebo模型/世界） | [https://github.com/ROBOTIS-GIT/turtlebot3_simulations](https://github.com/ROBOTIS-GIT/turtlebot3_simulations) |
| open_manipulator | OpenManipulator机械臂（驱动/MoveIt/仿真） | [https://github.com/ROBOTIS-GIT/open_manipulator](https://github.com/ROBOTIS-GIT/open_manipulator) |
| OpenCR | OpenCR控制板（固件/Arduino库/ROS） | [https://github.com/ROBOTIS-GIT/OpenCR](https://github.com/ROBOTIS-GIT/OpenCR) |
| DynamixelSDK | Dynamixel舵机SDK（C++/Python/Java等） | [https://github.com/ROBOTIS-GIT/DynamixelSDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) |
| universal_robot | Universal Robots机械臂驱动（UR3/5/10/e系列） | [https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver) |
| franka_ros | Franka Emika Panda机械臂（libfranka/ROS） | [https://github.com/frankaemika/franka_ros](https://github.com/frankaemika/franka_ros) |
| Husky | Clearpath Husky移动机器人 | [https://github.com/husky/husky](https://github.com/husky/husky) |


## 教程与学习资源
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| ros2_for_beginners_code | ROS2初学者代码（按章节，C++/Python，话题/服务/动作/TF/导航/MoveIt） | [https://github.com/homalozoa/ros2_for_beginners_code](https://github.com/homalozoa/ros2_for_beginners_code) |
| ROS-Theory-Practice | ROS理论与实践教程代码（建模/仿真/导航/实体） | [https://github.com/jingxuanyang/ROS-Theory-Practice](https://github.com/jingxuanyang/ROS-Theory-Practice) |
| how-to-learn-robotics | 开源机器人学学习指南（数学/运动学/动力学/控制/ROS） | [https://github.com/ysu341/how-to-learn-robotics](https://github.com/ysu341/how-to-learn-robotics) |
| Hands-On-ROS | 《ROS机器人编程实战》配套代码（GoPiGo3/SLAM/导航/视觉） | [https://github.com/PacktPublishing/Hands-On-ROS-for-Robotics-Programming](https://github.com/PacktPublishing/Hands-On-ROS-for-Robotics-Programming) |
| ros_robotics_projects | ROS机器人项目实例（人脸识别/聊天/手势/目标检测/深度学习/SLAM） | [https://github.com/qboticslabs/ros_robotics_projects](https://github.com/qboticslabs/ros_robotics_projects) |
| Mastering-ROS | 《精通ROS机器人编程》配套代码（传感器/执行器/融合/机械臂/插件） | [https://github.com/PacktPublishing/Mastering-ROS-for-Robotics-Programming-Third-edition](https://github.com/PacktPublishing/Mastering-ROS-for-Robotics-Programming-Third-edition) |
| ros2_knowledge | ROS2知识整理（概念/命令/最佳实践） | [https://github.com/zhangrelay/ros2_knowledge](https://github.com/zhangrelay/ros2_knowledge) |
| awesome-ros2 | ROS2精选资源列表 | [https://github.com/vmayoral/awesome-ros2](https://github.com/vmayoral/awesome-ros2) |


## 开发工具
| 项目 | 说明 | 链接 |
| --- | --- | --- |
| colcon | ROS2构建工具 | [https://github.com/colcon/colcon-core](https://github.com/colcon/colcon-core) |
| rosdep | ROS依赖管理工具 | [https://github.com/ros-infrastructure/rosdep](https://github.com/ros-infrastructure/rosdep) |
| vcstool | 版本控制工具（管理多个仓库） | [https://github.com/dirk-thomas/vcstool](https://github.com/dirk-thomas/vcstool) |
| catkin | ROS1构建工具（兼容） | [https://github.com/ros/catkin](https://github.com/ros/catkin) |
| plotjuggler | 数据可视化工具（ROS话题/CSV，比rqt_plot强大） | [https://github.com/facontidavide/PlotJuggler](https://github.com/facontidavide/PlotJuggler) |
| foxglove-studio | 机器人数据可视化平台（替代RViz，Web/桌面） | [https://github.com/foxglove/studio](https://github.com/foxglove/studio) |


---

> **本书完**
>
> 本书融合了《机器人学导论》（John J. Craig）的理论体系与《ROS机器人编程》（ROBOTIS）的工程实践，涵盖从空间变换、运动学、动力学、控制理论，到ROS环境搭建、通信机制、传感器、建模仿真、SLAM导航、机械臂控制，再到综合项目实战的完整知识体系。
>
> 每章均嵌入了相关的B站视频教程和GitHub开源项目，建议读者边学边练，在仿真环境中验证理论，在实体机器人上积累工程经验。
>
> 理论是实践的基础，实践是理论的验证。祝你在机器人学的学习道路上不断进步！
>
> _本书基于两本经典教材的公开目录和知识体系编写，仅供学习参考。如需深入学习，请阅读原书。_
>

---
