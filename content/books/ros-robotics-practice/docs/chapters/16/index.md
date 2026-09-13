# 第16章 综合项目实战：自主巡逻机器人
<!-- 这是一张图片，ocr 内容为： -->
![181_201_353_1399_1074_0.jpg](../../images/181_201_353_1399_1074_0.jpg)
![182_184_112_1433_1099_0.jpg](../../images/182_184_112_1433_1099_0.jpg)



<!-- 这是一张图片，ocr 内容为： -->
![188_137_283_1511_1244_0.jpg](../../images/188_137_283_1511_1244_0.jpg)

_图16-1 自主巡逻机器人系统架构_

_图16-2 巡逻任务状态机_



## 16.1 项目概述
### 16.1.1 项目目标
本项目综合运用前面章节所学的机器人学理论和ROS编程知识，构建一个能够在室内环境自主巡逻的移动机器人。项目目标：

+ **自主建图**：在未知环境中通过SLAM构建二维栅格地图
+ **自主定位**：在已知地图中通过AMCL确定机器人位置
+ **路径规划与导航**：从当前位置自主导航到指定目标点，避障
+ **巡逻任务**：按预设航点循环巡逻，到达航点后停留观察
+ **异常检测**：（可选）通过相机检测人员入侵、烟雾等异常
+ **远程监控**：（可选）通过Web界面或RViz远程监控机器人状态

### 16.1.2 技术栈
+ **操作系统**：Ubuntu 22.04 LTS + ROS2 Humble Hawksbill
+ **硬件平台**：差速移动底盘（TurtleBot3 Burger或自制）+ 2D激光雷达 + 可选RGB-D相机 + IMU
+ **软件框架**：Navigation2（导航栈）+ Cartographer（SLAM）+ OpenCV（视觉，可选）
+ **仿真环境**：Gazebo Classic 11
+ **编程语言**：Python 3（主要）+ C++（性能关键部分）
+ **开发工具**：VS Code + RViz2 + rqt + rosbag2

### 16.1.3 项目参考
本项目参考《ROS机器人编程》第10-12章的TurtleBot3内容，以及《机器人学导论》的运动学和控制理论，将理论与工程实践结合。

## 16.2 系统架构设计
<!-- 这是一张图片，ocr 内容为： -->
![184_171_125_1421_1067_0.jpg](../../images/184_171_125_1421_1067_0.jpg)

_图16-3 系统启动流程与节点拓扑_

### 16.2.1 系统模块划分
系统采用分层架构，从下到上分为四层：

```plain
┌─────────────────────────────────────────────────────────┐
│                  任务调度层（Task Layer）                 │
│        巡逻任务管理 / 异常处理 / 远程交互 / 航点管理      │
├─────────────────────────────────────────────────────────┤
│                  导航层（Navigation Layer）               │
│     SLAM建图 / AMCL定位 / 全局规划(A*) / 局部规划(DWA)   │
├─────────────────────────────────────────────────────────┤
│                  感知层（Perception Layer）               │
│   激光雷达 / 相机 / IMU / 轮式里程计 / 目标检测(可选)    │
├─────────────────────────────────────────────────────────┤
│                  控制层（Control Layer）                  │
│        电机驱动 / 速度PID控制 / 电源管理 / 传感器读取     │
└─────────────────────────────────────────────────────────┘
```

### 16.2.2 话题与服务设计
系统中的主要ROS话题和服务：

| 话题/服务 | 类型 | 方向 | 说明 |
| --- | --- | --- | --- |
| /scan | sensor_msgs/LaserScan | 传感器→系统 | 激光雷达扫描数据 |
| /camera/image_raw | sensor_msgs/Image | 传感器→系统 | 相机图像（可选） |
| /imu/data | sensor_msgs/Imu | 传感器→系统 | IMU数据 |
| /odom | nav_msgs/Odometry | 底盘→系统 | 轮式里程计 |
| /cmd_vel | geometry_msgs/Twist | 系统→底盘 | 速度命令（线速度+角速度） |
| /map | nav_msgs/OccupancyGrid | SLAM→系统 | 栅格地图 |
| /tf | tf2_msgs/TFMessage | 全系统 | 坐标变换（odom→base_link等） |
| /tf_static | tf2_msgs/TFMessage | 全系统 | 静态坐标变换 |
| /patrol_waypoints | 自定义 | 任务层 | 巡逻航点（参数） |
| /patrol_state | std_msgs/String | 任务层→外部 | 巡逻状态 |


### 16.2.3 TF树设计
```plain
map → odom → base_link → laser_link
                      → camera_link（可选）
                      → imu_link
                      → wheel_left_link
                      → wheel_right_link
                      → caster_front_link
                      → caster_rear_link
```

+ `map`：地图坐标系（固定，由SLAM/AMCL维护）
+ `odom`：里程计坐标系（固定，但有漂移，由底盘里程计维护）
+ `base_link`：机器人本体坐标系（随机器人运动）
+ 传感器坐标系固定在base_link上（静态TF）

注意：`map→odom`的变换由AMCL发布（校正里程计漂移），`odom→base_link`由里程计节点发布，两者不能同时由一个节点发布。

## 16.3 硬件选型与集成
### 16.3.1 硬件清单
| 组件 | 型号 | 说明 | 参考价格 |
| --- | --- | --- | --- |
| 主控 | Raspberry Pi 4B (4GB) 或 Jetson Nano | 运行ROS2和导航栈 | ¥300-800 |
| 底盘 | 差速驱动底盘（两轮+万向轮） | 机械结构，含电机和编码器 | ¥200-500 |
| 激光雷达 | RPLIDAR A1/A2 或 HLDS-LDS | 2D激光，360°，范围5-18m | ¥300-800 |
| RGB-D相机 | Intel RealSense D435i（可选） | 深度相机+IMU，用于视觉 | ¥1500 |
| 电机驱动 | Arduino Mega 或 OpenCR | 电机PID控制，读取编码器 | ¥100-300 |
| 电机 | 直流减速电机（带编码器） | 驱动轮子，PPR≥400 | ¥50×2 |
| 电池 | 11.1V 2200mAh锂电池组 | 供电，含保护板 | ¥100 |
| 降压模块 | 5V/3A降压模块 | 为树莓派和传感器供电 | ¥20 |
| 结构件 | 3D打印或铝板 | 固定各组件 | ¥50-100 |
| **总计** |  |  | **约¥1500-4000** |


也可以直接使用TurtleBot3 Burger（约¥5000），省去硬件集成的麻烦。

### 16.3.2 硬件连接图
```plain
激光雷达 ───USB───► 树莓派（主控）
RGB-D相机 ──USB───► 树莓派
Arduino ────USB───► 树莓派（发送速度命令，接收编码器/IMU数据）
     │
     ├──PWM──► 电机驱动板 ──► 左电机
     │              │
     │              └──► 右电机
     │
     └──GPIO──► 编码器（左/右）
                IMU（可选，I2C）
电池 ──► 电机驱动板（12V）
     └──► 降压模块（5V）──► 树莓派 + 激光雷达 + 相机
```

### 16.3.3 底盘运动学
差速驱动底盘的运动学模型：

```plain
已知：左轮速度v_l，右轮速度v_r，轮距B，轮半径r
计算：
  线速度 v = (v_l + v_r) / 2
  角速度 ω = (v_r - v_l) / B

逆运动学（已知v, ω，求轮速）：
  v_l = v - ω * B / 2
  v_r = v + ω * B / 2

轮速转电机转速（RPM）：
  RPM_l = v_l / (2πr) × 60
  RPM_r = v_r / (2πr) × 60
```

里程计计算（编码器增量）：

```plain
Δd_l = 2πr × Δticks_l / N
Δd_r = 2πr × Δticks_r / N
Δd = (Δd_l + Δd_r) / 2
Δθ = (Δd_r - Δd_l) / B
x += Δd × cos(θ + Δθ/2)
y += Δd × sin(θ + Δθ/2)
θ += Δθ
```

其中N是编码器每转脉冲数（含四倍频）。

## 16.4 软件系统开发
### 16.4.1 功能包结构
创建巡逻机器人功能包 `patrol_robot`：

```plain
patrol_robot/
├── CMakeLists.txt
├── package.xml
├── launch/
│   ├── simulation.launch.py       # 仿真启动（Gazebo+导航+巡逻）
│   ├── robot_bringup.launch.py    # 实体机器人启动
│   ├── slam.launch.py             # SLAM建图
│   └── navigation.launch.py       # 导航
├── config/
│   ├── nav2_params.yaml           # Nav2参数配置
│   ├── cartographer.lua           # Cartographer配置
│   ├── waypoints.yaml             # 巡逻航点
│   └── robot.rviz                 # RViz配置
├── maps/
│   ├── my_map.pgm                 # 地图图像
│   └── my_map.yaml                # 地图配置
├── urdf/
│   ├── patrol_robot.urdf.xacro    # 机器人URDF模型
│   └── gazebo.xacro               # Gazebo插件配置
├── patrol_robot/                   # Python节点（ament_python）
│   ├── __init__.py
│   ├── patrol_node.py             # 巡逻任务节点
│   ├── base_driver.py             # 底盘驱动节点（串口通信）
│   └── odometry_publisher.py      # 里程计发布节点
├── scripts/
│   └── save_map.sh                # 保存地图脚本
└── README.md                       # 项目说明
```

### 16.4.2 巡逻任务节点（Python）
巡逻节点是任务层的核心，负责管理巡逻航点、调用导航、处理异常：

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import yaml
import math
import time

class PatrolNode(Node):
    def __init__(self):
        super().__init__('patrol_node')
        
        # 声明参数
        self.declare_parameter('waypoints_file', 'waypoints.yaml')
        self.declare_parameter('wait_time_at_waypoint', 5.0)
        self.declare_parameter('loop', True)
        
        # 加载航点
        waypoints_file = self.get_parameter('waypoints_file').value
        self.waypoints = self.load_waypoints(waypoints_file)
        self.wait_time = self.get_parameter('wait_time_at_waypoint').value
        self.loop = self.get_parameter('loop').value
        
        # 初始化导航器
        self.navigator = BasicNavigator()
        self.navigator.waitUntilNav2Active()
        
        self.get_logger().info(f'巡逻节点已启动，共{len(self.waypoints)}个航点')
    
    def load_waypoints(self, filename):
        """从YAML文件加载航点"""
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        return data['waypoints']
    
    def create_pose(self, x, y, theta):
        """创建PoseStamped消息"""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        # 航向角转四元数（简化：绕Z轴旋转theta）
        pose.pose.orientation.z = math.sin(theta / 2.0)
        pose.pose.orientation.w = math.cos(theta / 2.0)
        return pose
    
    def run(self):
        """主巡逻循环"""
        current_index = 0
        while rclpy.ok():
            if current_index >= len(self.waypoints):
                if self.loop:
                    current_index = 0
                else:
                    self.get_logger().info('巡逻完成')
                    break
            
            wp = self.waypoints[current_index]
            self.get_logger().info(f'前往航点 {current_index+1}/{len(self.waypoints)}: '
                                    f'({wp["x"]:.2f}, {wp["y"]:.2f}), 朝向{wp["theta"]:.2f}rad')
            
            # 创建目标位姿并导航
            goal = self.create_pose(wp['x'], wp['y'], wp['theta'])
            self.navigator.goToPose(goal)
            
            # 等待导航完成
            while not self.navigator.isTaskComplete():
                rclpy.spin_once(self, timeout_sec=0.1)
                # 检查取消或异常
                if self.navigator.isTaskCanceled():
                    self.get_logger().warn('导航被取消')
                    break
            
            # 检查导航结果
            result = self.navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                self.get_logger().info(f'到达航点 {current_index+1}，停留{self.wait_time}秒')
                time.sleep(self.wait_time)
            elif result == TaskResult.CANCELED:
                self.get_logger().warn('导航被取消，跳过此航点')
            elif result == TaskResult.FAILED:
                self.get_logger().error(f'导航到航点{current_index+1}失败，跳过')
            
            current_index += 1

def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 16.4.3 航点配置文件
`waypoints.yaml`：

```yaml
waypoints:
  - {x: 1.0, y: 0.0, theta: 0.0}      # 航点1：起点
  - {x: 3.0, y: 0.0, theta: 1.57}     # 航点2：右转
  - {x: 3.0, y: 2.0, theta: 3.14}     # 航点3：向上
  - {x: 1.0, y: 2.0, theta: -1.57}    # 航点4：左转
  - {x: 1.0, y: 0.0, theta: 0.0}       # 航点5：回到起点
```

### 16.4.4 Launch文件
`simulation.launch.py`：

```python
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_patrol = get_package_share_directory('patrol_robot')
    pkg_tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    pkg_tb3_nav = get_package_share_directory('turtlebot3_navigation2')
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_file = LaunchConfiguration('map', default=os.path.join(pkg_patrol, 'maps', 'my_map.yaml'))
    
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('map', default_value=map_file),
        
        # 1. 启动Gazebo仿真（TurtleBot3世界）
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_tb3_gazebo, 'launch', 'turtlebot3_world.launch.py')
            ),
        ),
        
        # 2. 延迟5秒后启动导航（等待Gazebo和机器人就绪）
        TimerAction(
            period=5.0,
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(pkg_tb3_nav, 'launch', 'navigation2.launch.py')
                    ),
                    launch_arguments={'use_sim_time': use_sim_time, 'map': map_file}.items(),
                ),
            ],
        ),
        
        # 3. 延迟10秒后启动巡逻节点（等待导航就绪）
        TimerAction(
            period=10.0,
            actions=[
                Node(
                    package='patrol_robot',
                    executable='patrol_node',
                    name='patrol_node',
                    output='screen',
                    parameters=[{
                        'waypoints_file': os.path.join(pkg_patrol, 'config', 'waypoints.yaml'),
                        'wait_time_at_waypoint': 5.0,
                        'loop': True,
                    }],
                ),
            ],
        ),
    ])
```

## 16.5 测试与部署
### 16.5.1 仿真测试流程
**第一步：Gazebo仿真环境测试**

```bash
# 终端1：启动仿真环境
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 终端2：键盘遥控，验证机器人运动
ros2 run turtlebot3_teleop teleop_keyboard

# 终端3：检查话题和TF
ros2 topic list
ros2 topic echo /odom
ros2 run tf2_tools view_frames
```

**第二步：SLAM建图测试**

```bash
# 终端1：仿真
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 终端2：启动Cartographer SLAM
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True

# 终端3：遥控探索环境（缓慢移动，覆盖整个环境）
ros2 run turtlebot3_teleop teleop_keyboard

# 终端4：建图完成后保存地图
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/patrol_robot/maps/my_map
```

**第三步：导航测试**

```bash
# 终端1：仿真
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 终端2：启动导航（加载地图）
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=maps/my_map.yaml

# 在RViz中：
# 1. 用"2D Pose Estimate"指定初始位姿（在地图上机器人实际位置点击并拖动朝向）
# 2. 用"Nav2 Goal"指定目标点，观察机器人是否能自主导航
# 3. 在路径中添加动态障碍物（Gazebo中插入物体），观察避障效果
```

**第四步：巡逻任务测试**

```bash
# 终端1：仿真+导航（用前面的launch文件）
# 终端2：启动巡逻节点
ros2 run patrol_robot patrol_node --ros-args -p waypoints_file:=config/waypoints.yaml

# 观察机器人是否按航点顺序巡逻，到达后停留，然后继续下一个
```

### 16.5.2 实体机器人部署
**第一步：系统镜像制作**

+ 在Raspberry Pi上安装Ubuntu Server 22.04（64位）
+ 安装ROS2 Humble（基础版ros-base，不需要桌面工具）
+ 安装TurtleBot3或自定义底盘的驱动包
+ 配置WiFi自动连接（netplan）
+ 配置SSH远程登录
+ 设置主机名（如patrol-bot）

**第二步：开机自启（systemd服务）**

创建 `/etc/systemd/system/patrol_robot.service`：

```properties
[Unit]
Description=Patrol Robot ROS2 System
After=network.target
Wants=network.target

[Service]
Type=simple
User=ubuntu
Environment="ROS_DOMAIN_ID=0"
Environment="ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET"
ExecStart=/bin/bash -c 'source /opt/ros/humble/setup.bash && source /home/ubuntu/ros2_ws/install/setup.bash && ros2 launch patrol_robot robot_bringup.launch.py'
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable patrol_robot.service
sudo systemctl start patrol_robot.service
sudo systemctl status patrol_robot.service  # 查看状态
journalctl -u patrol_robot.service -f       # 查看日志
```

**第三步：远程访问与多机通信**

+ 确保机器人和远程电脑在同一WiFi网络
+ 设置相同的ROS_DOMAIN_ID（如0）
+ 在远程电脑上运行RViz，可视化机器人状态和地图
+ 远程电脑不需要运行导航节点，只需要订阅话题（话题自动发现）

```bash
# 远程电脑上运行RViz（可视化机器人状态）
rviz2 -d config/robot.rviz

# 远程遥控
ros2 run turtlebot3_teleop teleop_keyboard
```

### 16.5.3 常见问题与调试
| 问题 | 可能原因 | 解决方法 |
| --- | --- | --- |
| 建图漂移严重 | 里程计不准、激光雷达安装歪斜、运动过快 | 校准轮子直径和轮距、检查TF（laser_link→base_link）、降低建图速度 |
| 导航迷路/定位失败 | AMCL初始位姿不准、地图不匹配、激光数据质量差 | 在RViz中重新指定初始位姿、检查地图分辨率和原点、清洁激光雷达窗口 |
| 撞墙/不避障 | 局部规划参数不当、激光盲区、代价地图更新慢 | 调整DWA参数（增大障碍物权重）、检查激光安装高度、提高局部代价地图更新频率 |
| 电机抖动/异响 | PID参数不当、编码器噪声、齿轮间隙 | 调整PID（减小P、增大D）、滤波编码器数据、检查机械结构 |
| 通信延迟/丢包 | WiFi信号弱、CPU过载、话题频率过高 | 改善WiFi（5GHz/靠近路由器）、降低非关键话题频率、优化代码（减少计算量） |
| 导航到目标后不停止 | 目标容差设置过小、定位抖动 | 增大xy_goal_tolerance和yaw_goal_tolerance |
| 路径规划失败 | 目标在障碍物内、机器人被包围 | 检查目标点是否在自由空间、触发恢复行为（旋转/清图） |


### 16.5.4 性能优化建议
+ **计算优化**：将SLAM和导航的CPU占用控制在可接受范围，树莓派4上建议降低激光采样数（laser_max_beams=30）
+ **通信优化**：非关键话题（如相机图像）降低频率或仅在需要时启动
+ **电源优化**：使用高效降压模块，避免电压不稳导致重启
+ **散热优化**：树莓派加装散热片，避免高温降频
+ **代码优化**：Python节点中避免在回调中做耗时计算，使用多线程或异步处理

## 16.6 项目扩展方向
完成基础巡逻功能后，可以进一步扩展：

1. **视觉异常检测**：集成YOLO/OpenCV，检测人员入侵、烟雾、火焰等异常，发现异常时报警并拍照
2. **语音交互**：集成语音识别和合成，支持语音指令（"开始巡逻"、"回充电桩"）
3. **自动回充**：在电量低时自主导航到充电桩，对接充电
4. **多机器人协作**：多台巡逻机器人分工协作，覆盖更大区域
5. **云端监控**：将机器人状态和视频流传到云端，远程Web监控
6. **3D SLAM与导航**：使用3D激光雷达或深度相机，构建3D地图，实现更复杂的导航
7. **机械臂操作**：在移动底盘上加装机械臂（如OpenManipulator），实现移动操作（移动物体、按电梯按钮）

### 📺 推荐视频
> **ROS2机器人开发实战：从仿真到实体的完整项目流程**  
演示自主巡逻机器人从URDF建模、Gazebo仿真、SLAM建图（Cartographer）、Nav2导航调优，到实体部署（systemd自启）和调试的完整项目流程，是移动机器人项目实战的优秀参考。  
🔗 [B站观看](https://www.bilibili.com/video/BV1bzSSBCETQ/)
>

### 💻 推荐GitHub项目
> **Hands-On-ROS-for-Robotics-Programming：完整项目代码**  
《ROS机器人编程实战》配套的完整项目，包含GoPiGo3机器人的SLAM、导航、视觉、巡逻等功能实现，代码结构清晰，注释详细，可作为移动机器人项目的参考模板。  
🔗 [GitHub仓库](https://github.com/PacktPublishing/Hands-On-ROS-for-Robotics-Programming)
>

> **turtlebot3 — TurtleBot3官方仓库**  
TurtleBot3的官方软件仓库，包含固件、驱动、仿真、SLAM、导航、应用等完整代码，是学习移动机器人ROS开发的最佳参考。  
🔗 [GitHub仓库](https://github.com/ROBOTIS-GIT/turtlebot3)
>

---
