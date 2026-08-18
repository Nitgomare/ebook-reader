# 第10章 安保巡逻任务系统

安保巡逻任务系统是机器人实现自主安保服务的顶层应用，负责巡逻任务的组织、调度、异常事件处理以及与远程监控端的交互。本章在导航系统（第9章）的基础上，设计并实现完整的安保巡逻任务管理框架，使机器人能够按照预设策略自主执行巡逻任务，并在发现异常时及时报警。

## 10.1 任务管理框架设计

### 10.1.1 任务管理需求

安保巡逻任务系统的核心需求包括：

- **任务定义**：支持用户定义巡逻路线、巡逻区域、巡逻时间和频率。
- **任务调度**：根据时间表或外部触发启动、暂停、恢复和终止巡逻任务。
- **异常处理**：检测到异常事件后，暂停当前任务，执行报警流程，并根据策略恢复或终止巡逻。
- **远程交互**：支持远程下发任务指令、查看任务状态、手动接管控制。
- **日志记录**：记录巡逻过程中的关键事件、异常和操作，便于事后审计。

### 10.1.2 任务管理架构

任务管理系统采用分层架构：

- ┌──────────────────────────────────────┐
- │ 远程监控端（Web/上位机） │
- │ 任务配置 | 实时视频 | 状态显示 | 远程遥控 │
- └──────────────────────┬───────────────┘
- │ 网络（Wi-Fi/4G/5G）
- ┌──────────────────────▼───────────────┐
- │ 任务管理节点（ROS） │
- │ ┌──────────┐ ┌──────────┐ ┌────────┐ │
- │ │ 任务解析 │ │ 调度器 │ │ 异常处理 │ │
- │ └────┬─────┘ └────┬─────┘ └────┬───┘ │
- │ │ │ │ │
- │ ┌────▼────────────▼────────────▼───┐ │
- │ │ 巡逻执行状态机 │ │
- │ └────────────────┬─────────────────┘ │
- │ │ 目标点/速度指令 │
- │ ┌────────────────▼─────────────────┐ │
- │ │ 导航系统（move_base） │ │
- │ └────────────────┬─────────────────┘ │
- │ │ CAN │
- │ ┌────────────────▼─────────────────┐ │
- │ │ 运动控制（MCU） │ │
- │ └──────────────────────────────────┘ │
- └──────────────────────────────────────┘

任务管理节点通过服务与导航系统、感知系统、远程监控端通信。

### 10.1.3 任务定义与消息格式

巡逻任务使用JSON格式描述。一个典型的定点巡逻任务定义如下：

```json
{
  "task_id": "patrol_001",
  "task_type": "fixed_points",
  "points": [
    {"x": 1.0, "y": 2.0, "yaw": 0.0, "stay_time": 10},
    {"x": 5.0, "y": 3.0, "yaw": 1.57, "stay_time": 5},
    {"x": 8.0, "y": 1.0, "yaw": -1.57, "stay_time": 10}
  ],
  "repeat": 2,
  "interval": 60,
  "priority": 1
}
```

- task_type：巡逻类型，fixed_points（定点巡逻）或area_coverage（区域覆盖）。

- points：路径点列表，包含坐标、朝向和停留时间。

- repeat：重复次数，-1表示无限循环。

- interval：两次巡逻之间的间隔时间（秒）。

- priority：优先级，高优先级任务可中断低优先级任务。

## 10.2 定点与随机巡逻策略

### 10.2.1 定点巡逻

定点巡逻按照预设的路径点顺序依次执行。在每个路径点，机器人导航到达后停留指定时间（用于观察），然后前往下一个路径点。到达最后一个路径点后，根据`repeat`参数决定是否重复。

**定点巡逻执行流程**：

1. 解析任务定义，获取路径点列表。
2. 依次将每个路径点作为`move_base`的目标点发送。
3. 等待导航结果（成功/失败/超时）。
4. 到达后停留指定时间，期间保持感知系统运行，检测异常。
5. 所有路径点完成后，若`repeat`大于1或为-1，则间隔`interval`秒后重新开始。

**代码示例**（Python节点简化版）：

```python
#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import json

class FixedPointPatrol:
    def __init__(self):
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        rospy.loginfo("Connected to move_base")

    def execute_patrol(self, task):
        points = task['points']
        repeat = task.get('repeat', 1)
        interval = task.get('interval', 0)

        for r in range(repeat if repeat != -1 else 999999):
            for p in points:
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = p['x']
                goal.target_pose.pose.position.y = p['y']
                goal.target_pose.pose.orientation.w = 1.0  # 简化朝向
                self.client.send_goal(goal)
                self.client.wait_for_result()
                rospy.sleep(p.get('stay_time', 5))
            rospy.sleep(interval)
```

### 10.2.2 随机巡逻

随机巡逻用于提高安保的不确定性，防止被预判。本平台实现两种随机巡逻方式：

- 方式一：随机路径点选择。在预设的候选路径点中随机选择下一个目标点，保证相邻两点不同。

- 方式二：区域随机游走。在指定区域内随机生成目标点，调用导航系统前往。区域由多边形顶点定义。

随机巡逻的任务定义示例：

```json
{
  "task_id": "random_patrol_001",
  "task_type": "random_points",
  "candidate_points": [
    {"x": 1.0, "y": 2.0},
    {"x": 5.0, "y": 3.0},
    {"x": 8.0, "y": 1.0},
    {"x": 3.0, "y": 6.0}
  ],
  "repeat": -1,
  "interval": 30
}
```

随机巡逻执行逻辑：维护一个随机数发生器，每次从候选点中随机选取一个不同于当前点的目标，导航到达后停留随机时间（如5~15秒），然后继续。

## 10.3 异常事件检测与分级报警

### 10.3.1 异常事件类型

基于第8章的感知系统，本平台定义以下异常事件类型及等级：

| 事件类型 | 等级 | 触发条件 | 响应 |
| :--- | :--- | :--- | :--- |
| 人员入侵 | 高 | 检测到人员在禁入区域（预设多边形）内 | 立即报警，上传图像，原地监视 |
| 遗留物 | 中 | 非背景物体静止超过30秒 | 上报，拍照留证，继续巡逻 |
| 烟雾/火焰 | 高 | 视觉检测到烟雾或火焰 | 立即报警，原地监视，通知消防 |
| 设备异常 | 中 | 电压过低、电流过大、温度过高 | 上报，停止巡逻，返回充电点 |
| 通信丢失 | 高 | 与远程监控端心跳超时 | 本地声光报警，停止移动 |

### 10.3.2 异常事件处理流程

异常事件处理采用状态机，优先级从高到低为：通信丢失 > 烟雾/火焰 > 人员入侵 > 设备异常 > 遗留物。

处理流程：

1. **事件检测**：感知节点发布异常事件消息（自定义ROS消息`AnomalyEvent`）。
2. **事件评估**：任务管理节点接收事件，根据当前任务状态判断是否立即处理。
3. **报警响应**：发布报警消息，触发声光报警，上传现场图像。
4. **任务调整**：根据事件等级，决定暂停、终止或继续巡逻任务。
5. **恢复**：事件清除后，根据策略恢复巡逻任务。

**报警消息格式**：

```python
# AnomalyEvent.msg
string type          # 事件类型
float32 severity     # 等级1~5
float32 x            # 事件位置x
float32 y            # 事件位置y
string description   # 描述
sensor_msgs/Image image  # 现场图像
```

### 10.3.3 报警与上报实现

报警节点同时执行本地声光报警和远程上报：

```python
def handle_anomaly(event):
    # 本地声光报警
    activate_buzzer(1.0)
    activate_led('red', 0.5)
    # 远程上报
    upload_event(event)
    # 上传图像
    upload_image(event.image)
    # 根据等级调整任务
    if event.severity >= 4:
        pause_current_task()
        rospy.logwarn("High severity anomaly, pausing patrol")
    elif event.severity >= 2:
        rospy.loginfo("Medium severity anomaly, continue patrol")
```

## 10.4 视频回传与远程监控

### 10.4.1 视频回传架构

远程监控端需要实时查看机器人摄像头画面。由于巡逻机器人可能处于Wi-Fi覆盖不稳定区域，本平台采用**自适应码率**和**断线重连**机制。

视频回传使用`web_video_server`或`rosbridge`将图像话题转发为WebRTC/HTTP流，供浏览器访问。架构如下：

```
机器人端（ROS）                         远程监控端
┌────────────────┐                 ┌────────────────┐
│ 深度相机RGB    │──ROS Image────►│ web_video_server│──HTTP/WebRTC──►浏览器
│ /camera/color  │                 └────────────────┘
└────────────────┘
```

### 10.4.2 视频回传节点配置

启动`web_video_server`：

```bash
rosrun web_video_server web_video_server
```

默认情况下，访问`http://<机器人IP>:8080/stream?topic=/camera/color/image_raw`即可查看视频流。

对于带宽受限场景，可降低图像分辨率或帧率：

```yaml
# camera_node_config.yaml
color_width: 640
color_height: 480
color_fps: 15
```

### 10.4.3 远程监控界面

远程监控端基于Web实现，功能包括：

- 实时视频显示
- 机器人状态显示（位置、电量、模式）
- 任务下发与进度查看
- 报警列表与图像查看
- 远程遥控按钮

本平台使用`rosbridge_suite`和`roslibjs`实现通信。

## 10.5 远程遥控与自主模式切换

### 10.5.1 模式定义与切换逻辑

机器人具有自主巡逻模式和远程遥控模式。模式切换由远程监控端请求，任务管理节点执行。

- **自主巡逻模式**：机器人按照任务定义自主导航，无需人工干预。
- **远程遥控模式**：操作员通过上位机或Web界面手动控制机器人移动，可使用键盘、手柄或点击地图目标点。

模式切换流程：

1. 远程端发送模式切换请求（`/switch_mode`）。
2. 任务管理节点校验权限（如需密码或令牌）。
3. 若当前处于巡逻任务中，先暂停任务，保存现场状态。
4. 切换模式，发布模式状态。
5. 在遥控模式下，`move_base`被挂起，速度指令直接下发到底层。

### 10.5.2 遥控实现

键盘遥控节点（`teleop_twist_keyboard`）发布`/cmd_vel`，底层接收后执行。在自主模式下，`move_base`也发布`/cmd_vel`。为避免冲突，使用`mux`节点选择速度指令源：

```xml
<node name="cmd_vel_mux" pkg="twist_mux" type="twist_mux">
  <rosparam>
    topics:
      - name: 'teleop'
        topic: 'teleop/cmd_vel'
        timeout: 0.5
      - name: 'nav'
        topic: 'move_base/cmd_vel'
        timeout: 0.5
    default: 'nav'
  </rosparam>
</node>
```

在遥控模式下，切换`cmd_vel_mux`的默认源为`teleop`。

### 10.5.3 模式切换节点代码

```python
#!/usr/bin/env python3
import rospy
from std_srvs.srv import SetBool, SetBoolResponse
from std_msgs.msg import String

class ModeManager:
    def __init__(self):
        self.current_mode = 'autonomous'
        self.mode_pub = rospy.Publisher('/robot_mode', String, queue_size=10)
        self.switch_srv = rospy.Service('/switch_mode', SetBool, self.handle_switch)
        # 初始化twist_mux选择器
        self.mux_pub = rospy.Publisher('/cmd_vel_mux/selected', String, queue_size=10)

    def handle_switch(self, req):
        # req.data=True表示遥控模式，False表示自主模式
        if req.data:
            self.current_mode = 'remote'
            self.mux_pub.publish('teleop')
            self.mode_pub.publish('remote')
        else:
            self.current_mode = 'autonomous'
            self.mux_pub.publish('nav')
            self.mode_pub.publish('autonomous')
        rospy.loginfo(f"Mode switched to {self.current_mode}")
        return SetBoolResponse(success=True, message=f"Mode: {self.current_mode}")

if __name__ == '__main__':
    rospy.init_node('mode_manager')
    ModeManager()
    rospy.spin()
```

## 10.6 任务系统代码实现

### 10.6.1 任务管理节点结构

任务管理节点包含以下主要模块：

- **任务解析器**：解析JSON任务定义。
- **任务调度器**：根据时间和优先级调度任务。
- **巡逻执行器**：调用导航系统执行巡逻。
- **异常处理器**：处理异常事件。
- **状态发布器**：发布任务状态和机器人状态。

### 10.6.2 任务管理核心代码（Python）

```python
#!/usr/bin/env python3
import rospy
import json
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String, Float32MultiArray
from sensor_msgs.msg import Image
import threading

class TaskManager:
    def __init__(self):
        self.current_task = None
        self.task_thread = None
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()

        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

        rospy.Subscriber('/anomaly_events', String, self.anomaly_cb)
        self.status_pub = rospy.Publisher('/task_status', String, queue_size=10)
        rospy.Service('/start_task', Trigger, self.start_task_cb)
        rospy.Service('/pause_task', Trigger, self.pause_task_cb)
        rospy.Service('/resume_task', Trigger, self.resume_task_cb)
        rospy.Service('/stop_task', Trigger, self.stop_task_cb)

    def start_task_cb(self, req):
        if self.current_task is None:
            # 从参数服务器或文件加载任务
            task = rospy.get_param('/current_task')
            self.current_task = task
            self.task_thread = threading.Thread(target=self.execute_task, args=(task,))
            self.task_thread.start()
            return TriggerResponse(True, "Task started")
        else:
            return TriggerResponse(False, "Task already running")

    def execute_task(self, task):
        points = task['points']
        while not self.stop_event.is_set():
            if self.pause_event.is_set():
                rospy.sleep(0.1)
                continue
            for p in points:
                if self.stop_event.is_set() or self.pause_event.is_set():
                    break
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = p['x']
                goal.target_pose.pose.position.y = p['y']
                goal.target_pose.pose.orientation.w = 1.0
                self.client.send_goal(goal)
                self.client.wait_for_result()
                rospy.sleep(p.get('stay_time', 5))
            rospy.sleep(task.get('interval', 60))
            if task.get('repeat', 1) != -1:
                task['repeat'] -= 1
                if task['repeat'] <= 0:
                    break
        rospy.loginfo("Task completed")
        self.current_task = None

    def anomaly_cb(self, msg):
        # 解析异常消息，执行报警
        rospy.logwarn(f"Anomaly detected: {msg.data}")
        self.pause_event.set()
        # 触发报警（简化）
        self.status_pub.publish(f"anomaly:{msg.data}")
        # 高等级异常停止任务
        if 'fire' in msg.data or 'intrusion' in msg.data:
            self.stop_event.set()

    def pause_task_cb(self, req):
        self.pause_event.set()
        return TriggerResponse(True, "Task paused")

    def resume_task_cb(self, req):
        self.pause_event.clear()
        return TriggerResponse(True, "Task resumed")

    def stop_task_cb(self, req):
        self.stop_event.set()
        self.pause_event.clear()
        return TriggerResponse(True, "Task stopped")

if __name__ == '__main__':
    rospy.init_node('task_manager')
    TaskManager()
    rospy.spin()
```

### 10.6.3 任务配置文件

任务定义存储在YAML或JSON文件中，通过`rosparam`加载：

```yaml
current_task:
  task_id: "patrol_001"
  task_type: "fixed_points"
  points:
    - {x: 1.0, y: 2.0, stay_time: 10}
    - {x: 5.0, y: 3.0, stay_time: 5}
    - {x: 8.0, y: 1.0, stay_time: 10}
  repeat: -1
  interval: 30
```

## 10.7 实战：多场景安保演练

### 10.7.1 演练目标

在模拟环境中进行多场景安保演练，验证任务系统的完整性和可靠性。演练场景包括：

1. **定点巡逻**：在办公区域进行定点巡逻，覆盖所有关键位置。
2. **随机巡逻**：在园区进行随机路径点巡逻。
3. **入侵报警**：模拟人员进入禁入区域，触发报警并上传图像。
4. **模式切换**：在巡逻过程中远程切换至遥控模式，完成手动检查后切回自主模式。

### 10.7.2 演练步骤

**场景一：定点巡逻**

1. 准备地图和巡逻路径点。
2. 启动导航系统和任务管理节点。
3. 下发定点巡逻任务。
4. 观察机器人依次到达各路径点，停留时间符合要求。
5. 检查任务状态话题，确认任务进度。

**场景二：随机巡逻**

1. 配置候选路径点和随机巡逻参数。
2. 启动随机巡逻任务。
3. 记录机器人实际路径，确认随机性和覆盖性。

**场景三：入侵报警**

1. 在地图中设置禁入区域（多边形）。
2. 机器人执行巡逻任务，人员进入禁入区域。
3. 确认感知系统检测到人员并触发入侵报警。
4. 远程监控端收到报警信息和图像。
5. 机器人暂停巡逻，原地监视。
6. 人员离开后，任务恢复。

**场景四：模式切换**

1. 机器人正在自主巡逻。
2. 远程端发送切换遥控模式请求。
3. 确认机器人停止自主导航，响应遥控指令。
4. 遥控机器人移动一段距离后，切回自主模式。
5. 确认机器人重新接续巡逻任务。

### 10.7.3 演练评估指标

| 指标 | 通过标准 |
| :--- | :--- |
| 路径点到达率 | ≥95% |
| 报警响应时间 | ≤2秒 |
| 图像上传成功率 | ≥90% |
| 模式切换时间 | ≤3秒 |
| 任务恢复成功率 | 100% |

### 10.7.4 常见问题与排查

| 问题 | 可能原因 | 排查方法 |
| :--- | :--- | :--- |
| 任务无法启动 | 任务配置文件格式错误 | 检查JSON/YAML语法，查看ROS参数 |
| 巡逻途中停止 | 导航目标点不可达 | 检查地图和路径点坐标，调整目标 |
| 报警不触发 | 感知节点未发布事件 | 检查感知系统话题，确认检测算法运行 |
| 视频回传卡顿 | 带宽不足 | 降低图像分辨率和帧率 |
| 模式切换失败 | twist_mux配置错误 | 检查`/cmd_vel_mux/selected`话题 |

完成本章实战后，读者应能够为轮腿式安保巡逻机器人部署完整的任务系统，实现定点/随机巡逻、异常报警、远程监控和模式切换等核心功能，具备在实际场景中开展安保巡逻的能力。
