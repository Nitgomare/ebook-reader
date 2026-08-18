# 第9章 自主导航与路径规划

自主导航是安保巡逻机器人实现无人化巡逻的核心能力。对于双足轮腿式平台，导航系统不仅需要解决常规移动机器人的建图、定位、规划问题，还需要结合轮腿复合运动的特点，在路径规划与执行过程中合理利用轮式模式的高效性和腿式模式的越障能力。本章将围绕这一主线展开。

## 9.1 环境建图与SLAM

### 9.1.1 地图表示与选择

本平台采用二维栅格地图（Occupancy Grid Map）作为导航的基础地图。栅格地图将环境划分为一系列固定大小的网格，每个网格存储该位置被障碍物占据的概率。对于安保巡逻场景，栅格地图足以描述走廊、园区道路、障碍物等主要结构，且计算量小、便于路径规划。

栅格分辨率取0.05 m，兼顾地图精度与存储开销。地图由单线激光雷达扫描数据通过SLAM算法构建。

### 9.1.2 基于激光雷达的SLAM

本平台使用Cartographer作为SLAM算法。Cartographer是基于图优化的2D/3D SLAM方法，能够融合激光雷达、IMU和轮式里程计数据，生成全局一致的栅格地图，并输出机器人实时位姿。

Cartographer配置要点：

- **轨迹构建**：使用2D模式，订阅`/scan`话题和`/imu/data`话题，提供轮式里程计作为初始位姿估计。
- **回环检测**：启用回环检测，提高大范围环境下的建图一致性。
- **参数调整**：根据机器人运动速度和激光雷达特性调整`TRAJECTORY_BUILDER_2D`中的扫描匹配和子图参数。

运行Cartographer的launch文件：

```xml
<launch>
  <node name="cartographer_node" pkg="cartographer_ros" type="cartographer_node" args="-configuration_directory $(find wheel_legged_robot)/config -configuration_basename cartographer.lua" output="screen"/>
  <node name="cartographer_occupancy_grid_node" pkg="cartographer_ros" type="cartographer_occupancy_grid_node" args="-resolution 0.05"/>
</launch>
```

### 9.1.3 建图过程中的轮腿模式

在建图阶段，机器人以轮式模式运动，腿部保持站立姿态，确保激光雷达扫描平面稳定。如果遇到轮式无法通过的障碍（如台阶），可以手动切换至腿式模式越过，但建图期间尽量保持平稳，避免剧烈姿态变化导致地图畸变。

## 9.2 定位与位姿估计

### 9.2.1 里程计与位姿估计

第8章已经介绍了基于轮式编码器和IMU的EKF融合里程计，输出高频的位姿估计。但里程计存在累积漂移，长时间运行后误差增大。因此，需要结合地图进行绝对定位。

### 9.2.2 基于AMCL的定位

本平台采用自适应蒙特卡洛定位（AMCL）算法，将激光雷达扫描数据与已知栅格地图进行匹配，估计机器人在地图中的全局位姿。AMCL输出`/amcl_pose`话题，频率约10 Hz。

AMCL配置关键参数：

- **粒子数**：初始粒子数设为2000，最小粒子数500，最大5000。
- **更新模型**：使用`likelihood_field`模型，适用于非高斯噪声的激光雷达。
- **初始位姿**：巡逻机器人通常在已知起点启动，可设置初始位姿估计，加快收敛。

```yaml
# amcl.yaml
use_map_topic: true
odom_model_type: diff
odom_alpha1: 0.2
odom_alpha2: 0.2
odom_alpha3: 0.2
odom_alpha4: 0.2
laser_model_type: likelihood_field
laser_likelihood_max_dist: 2.0
laser_max_beams: 60
min_particles: 500
max_particles: 5000
```

### 9.2.3 定位与轮腿模式的关系

在腿式越障过程中，机器人身体姿态会发生明显变化，激光雷达扫描平面倾斜，可能导致AMCL定位误差增大。因此，本平台在腿式模式下暂停AMCL更新，仅依靠里程计和IMU进行短时位姿递推；越障结束恢复轮式模式后，再重新启用AMCL进行全局定位校正。

## 9.3 全局路径规划

### 9.3.1 代价地图

导航使用全局代价地图和局部代价地图。全局代价地图由静态地图层和障碍物层组成，分辨率0.05 m，用于全局路径规划。局部代价地图以机器人为中心，范围3 m×3 m，分辨率0.05 m，用于局部避障。

对于轮腿式机器人，需要额外考虑以下因素：

- **不可通行区域**：在全局代价地图中，将高度超过腿式越障能力（80 mm）的台阶、楼梯等标记为不可通行。
- **可通过的越障区域**：对于高度在30~80 mm的台阶、减速带等，标记为“可越障但需切换腿式模式”的特殊区域。本平台简化处理：在全局路径规划时将这类区域设为高成本区域，路径规划器会尽量绕开；如果必须通过，则触发腿式模式。

### 9.3.2 A*全局路径规划

全局路径规划采用A*算法，在代价地图中搜索从起点到目标点的最短路径。A*算法结合Dijkstra算法的最短路径保证和启发式搜索的效率，适合栅格地图。

代价函数：

$$
f(n) = g(n) + h(n)
$$

其中 $g(n)$ 为从起点到节点 $n$ 的实际代价，$h(n)$ 为节点 $n$ 到目标点的启发式估计（采用欧氏距离或曼哈顿距离）。

ROS中`global_planner`包提供了A*和Dijkstra实现，配置为A*：

```yaml
# global_planner_params.yaml
GlobalPlanner:
  use_dijkstra: false
  use_astar: true
  allow_unknown: false
```

路径规划结果发布为`/plan`话题，包含一系列位姿点。

### 9.3.3 轮腿特性在全局规划中的处理

对于必须经过的越障区域（如通往目标点的唯一路径上有减速带），全局规划器输出路径后，导航系统根据路径点所在区域属性，在接近该区域时自动切换至腿式模式。这一逻辑在导航状态机中实现：

```
轮式模式行驶 → 检测到前方路径点位于越障区域 → 减速并切换腿式模式 → 越障 → 恢复轮式模式 → 继续行驶
```

## 9.4 局部避障与动态窗口法

### 9.4.1 DWA算法原理

局部避障采用动态窗口法（Dynamic Window Approach，DWA）。DWA在速度空间中搜索一组可行的速度指令，通过评价函数选择最优速度，使机器人在避开动态障碍物的同时朝目标前进。

速度空间受以下约束：

- **运动学约束**：轮式差速驱动模型下的速度范围。
- **动态约束**：最大加速度限制。
- **安全约束**：在预测轨迹内不与障碍物碰撞。

评价函数：

$$
G(v, \omega) = \alpha \cdot \text{heading}(v, \omega) + \beta \cdot \text{dist}(v, \omega) + \gamma \cdot \text{velocity}(v, \omega)
$$

其中：

- $\text{heading}$：朝向目标的程度；
- $\text{dist}$：与最近障碍物的距离；
- $\text{velocity}$：速度大小；
- $\alpha, \beta, \gamma$ 为权重系数。

本平台DWA参数调整如下：

| 参数 | 值 | 说明 |
| :--- | :--- | :--- |
| 最大线速度 | 2.0 m/s | 轮式模式 |
| 最大角速度 | 3.0 rad/s | 轮式模式 |
| 最大线加速度 | 1.5 m/s² | 保证平稳 |
| 最大角加速度 | 2.0 rad/s² | 保证平稳 |
| 前向模拟时间 | 1.5 s | 预测轨迹长度 |
| 障碍物安全距离 | 0.3 m | 保持安全裕量 |

### 9.4.2 腿式模式下的局部避障

在腿式模式下，机器人移动速度低（≤0.3 m/s），且轮子锁死，不能使用DWA进行速度规划。本平台在腿式模式下采用**定点越障策略**：当局部代价地图检测到前方障碍物时，先停止，然后执行第7章的越障步态。越障过程中，超声波传感器提供近距离避障冗余，防止与障碍物碰撞。

## 9.5 巡逻路径优化与任务分配

### 9.5.1 巡逻路径优化

安保巡逻通常要求机器人按照预设路线或覆盖指定区域。巡逻路径优化目标是最小化巡逻时间或最大化覆盖率。本平台支持两种巡逻模式：

1. **定点巡逻**：机器人按照预设的路径点列表依次巡逻，路径点由用户在地图上标记。
2. **区域覆盖巡逻**：机器人采用“弓”字形覆盖路径，遍历指定区域内的所有可达位置。

对于定点巡逻，路径规划采用A*算法依次规划相邻路径点之间的最短路径，并连接成完整巡逻路线。如果路径中存在高成本区域（越障区域），导航系统会优先绕行；如果绕行代价过大，则接受越障方案。

### 9.5.2 任务分配

在多机器人系统中，巡逻任务需要分配给多个机器人。本平台为单机器人系统，但预留了多机器人任务分配接口。任务分配采用简单的“最近优先”策略：将巡逻区域划分为若干子区域，每个机器人负责距离自己最近的子区域。

单机器人巡逻时，任务管理模块（第10章）负责根据时间表或事件触发巡逻任务，调用导航系统执行。

## 9.6 导航系统代码实现

### 9.6.1 导航启动文件

```xml
<!-- navigation.launch -->
<launch>
  <!-- 地图服务器 -->
  <node name="map_server" pkg="map_server" type="map_server" args="$(find wheel_legged_robot)/maps/patrol_map.yaml"/>

  <!-- AMCL定位 -->
  <node name="amcl" pkg="amcl" type="amcl" output="screen">
    <rosparam file="$(find wheel_legged_robot)/config/amcl.yaml"/>
  </node>

  <!-- 全局规划器 -->
  <node name="global_planner" pkg="global_planner" type="planner" output="screen">
    <rosparam file="$(find wheel_legged_robot)/config/global_planner_params.yaml"/>
  </node>

  <!-- 局部规划器（DWA） -->
  <node name="local_planner" pkg="dwa_local_planner" type="dwa_local_planner" output="screen">
    <rosparam file="$(find wheel_legged_robot)/config/dwa_params.yaml"/>
  </node>

  <!-- move_base -->
  <node name="move_base" pkg="move_base" type="move_base" output="screen">
    <rosparam file="$(find wheel_legged_robot)/config/costmap_common_params.yaml"/>
    <rosparam file="$(find wheel_legged_robot)/config/costmap_global_params.yaml"/>
    <rosparam file="$(find wheel_legged_robot)/config/costmap_local_params.yaml"/>
    <rosparam file="$(find wheel_legged_robot)/config/move_base_params.yaml"/>
  </node>
</launch>
```

### 9.6.2 轮腿模式切换节点

```python
#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

class ModeSwitchNode:
    def __init__(self):
        self.path_sub = rospy.Subscriber('/move_base/TrajectoryPlannerROS/global_plan', Path, self.path_cb)
        self.mode_pub = rospy.Publisher('/robot_mode', String, queue_size=10)
        self.current_mode = 'wheel'
        self.obstacle_threshold = 0.03  # 30mm

    def path_cb(self, path):
        # 检查路径中是否有越障区域（简化：由上层标记）
        for pose in path.poses:
            if self.is_obstacle_area(pose):
                self.switch_to_leg()
                return
        self.switch_to_wheel()

    def is_obstacle_area(self, pose):
        # 查询代价地图中该点的代价值，高于阈值认为是越障区域
        # 此处简化，实际需调用costmap服务
        return False

    def switch_to_leg(self):
        if self.current_mode != 'leg':
            self.mode_pub.publish('leg')
            self.current_mode = 'leg'
            rospy.loginfo('Switch to leg mode for obstacle crossing')

    def switch_to_wheel(self):
        if self.current_mode != 'wheel':
            self.mode_pub.publish('wheel')
            self.current_mode = 'wheel'
            rospy.loginfo('Switch to wheel mode')

if __name__ == '__main__':
    rospy.init_node('mode_switch_node')
    ModeSwitchNode()
    rospy.spin()
```

### 9.6.3 底盘接口适配

`move_base`输出的速度指令为`geometry_msgs/Twist`，底层通过CAN通信接收。在轮式模式下，底层直接解析速度指令并执行。在腿式模式下，`move_base`被挂起，由底层步态控制器接管，此时速度指令被忽略。

## 9.7 实战：园区环境自主巡逻

### 9.7.1 任务目标

在园区环境中完成一次完整的自主巡逻任务：加载地图、定位、路径规划、避障、越障，最终返回起点。

### 9.7.2 测试步骤

1. **准备地图**：在园区内使用遥控模式驱动机器人，运行Cartographer建图，保存栅格地图。
2. **设置巡逻路线**：在地图上标记至少4个巡逻路径点，包括一段含有减速带或台阶的越障区域。
3. **启动导航系统**：运行`navigation.launch`，加载地图和AMCL。
4. **发送巡逻指令**：通过任务系统（第10章）发送巡逻路径点列表。
5. **观察与记录**：观察机器人的行驶轨迹、避障行为和越障过程，记录完成时间。
6. **评估**：对比期望路径与实际轨迹，评估导航精度和越障成功率。

### 9.7.3 常见问题与排查

| 问题 | 可能原因 | 排查方法 |
| :--- | :--- | :--- |
| 定位漂移 | 里程计误差累积、激光雷达被遮挡 | 检查IMU融合参数，清洁激光雷达 |
| 路径规划失败 | 代价地图中起点或终点被占据 | 检查地图，清理临时障碍物 |
| DWA速度振荡 | 评价函数权重不当 | 调整heading和dist权重 |
| 越障时定位丢失 | 姿态变化导致雷达扫描异常 | 腿式模式下暂停AMCL，增加IMU权重 |
| 巡逻路线偏离 | 全局路径跟踪精度不足 | 调整move_base的xy_goal_tolerance |

完成本章实战后，读者应能够为轮腿式机器人部署完整的自主导航系统，实现园区环境下的自主巡逻，并具备处理轮腿模式切换和越障导航的能力。
