# 第8章 环境感知系统

## 8.1 感知系统总体设计

环境感知系统是安保巡逻机器人的“眼睛”，负责实时获取周围环境信息，为自主导航、避障和异常检测提供数据支撑。本平台感知系统由以下传感器组成：

| 传感器 | 类型 | 数据 | 主要用途 |
| :--- | :--- | :--- | :--- |
| 单线激光雷达 | RPLIDAR A1 | 2D点云（距离、角度） | 建图、定位、障碍物检测 |
| 深度相机 | Intel RealSense D435i | 深度图、RGB图、IMU | 目标检测、近距避障、夜间感知 |
| IMU | ICM-20948 | 加速度、角速度 | 姿态估计、运动补偿 |
| 轮速编码器 | 霍尔编码器×2 | 轮速 | 里程计、速度反馈 |
| 超声波传感器 | HC-SR04×2 | 距离 | 近程避障冗余 |

话题与消息定义

| 话题名 | 消息类型 | 频率 | 内容 |
| :--- | :--- | :--- | :--- |
| `/scan` | `sensor_msgs/LaserScan` | 10 Hz | 激光雷达扫描数据 |
| `/camera/color/image_raw` | `sensor_msgs/Image` | 30 Hz | RGB图像 |
| `/camera/depth/image_rect_raw` | `sensor_msgs/Image` | 30 Hz | 深度图像 |
| `/camera/imu` | `sensor_msgs/Imu` | 200 Hz | 相机内置IMU |
| `/imu/data` | `sensor_msgs/Imu` | 1 kHz | 底层IMU（经CAN上传） |
| `/ultrasonic` | `std_msgs/Float32MultiArray` | 20 Hz | 超声波距离 |
| `/wheel_odom` | `nav_msgs/Odometry` | 50 Hz | 轮式里程计 |
| `/detections` | `vision_msgs/Detection2DArray` | 15 Hz | 目标检测结果 |
| `/anomaly_events` | `std_msgs/String` | 事件触发 | 异常事件上报 |

## 8.2 激光雷达点云处理

### 8.2.1 数据获取与转换

RPLIDAR A1输出2D扫描数据，通过`rplidar_ros`驱动包发布`/scan`话题。`LaserScan`消息包含距离数组和角度信息。为便于处理，需转换为点云格式（`PointCloud2`）或直接使用距离数组。

```python
#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

class LaserProcessor:
    def __init__(self):
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan_cb)
        self.points_2d = []

    def scan_cb(self, scan):
        angles = np.arange(scan.angle_min, scan.angle_max, scan.angle_increment)
        ranges = np.array(scan.ranges)
        # 过滤无效值
        valid = (ranges > scan.range_min) & (ranges < scan.range_max)
        angles = angles[valid]
        ranges = ranges[valid]
        # 极坐标转笛卡尔坐标
        x = ranges * np.cos(angles)
        y = ranges * np.sin(angles)
        self.points_2d = np.column_stack((x, y))
```

### 8.2.2 点云滤波与分割

原始点云包含噪声和地面反射，需进行滤波。使用PCL库或自定义算法：

```python
# 基于距离的离群点滤波（简化）
def filter_outliers(points, radius=0.1, min_neighbors=3):
    filtered = []
    for p in points:
        dist = np.linalg.norm(points - p, axis=1)
        if np.sum(dist < radius) >= min_neighbors:
            filtered.append(p)
    return np.array(filtered)
```

### 8.2.3 障碍物聚类

将点云聚类为独立障碍物，用于避障和建图。采用欧氏聚类：

```python
// C++ 欧氏聚类（简化）
#include <pcl/point_cloud.h>
#include <pcl/segmentation/extract_clusters.h>

pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
// 填充cloud...

pcl::search::KdTree<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>);
tree->setInputCloud(cloud);

std::vector<pcl::PointIndices> cluster_indices;
pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
ec.setClusterTolerance(0.1);  // 10cm
ec.setMinClusterSize(5);
ec.setMaxClusterSize(1000);
ec.setSearchMethod(tree);
ec.setInputCloud(cloud);
ec.extract(cluster_indices);
```

## 8.3 视觉传感器与图像处理

### 8.3.1 深度相机驱动与标定

Intel RealSense D435i通过`realsense2_camera`包驱动，发布RGB、深度和IMU话题。使用前需进行内参标定和深度对齐。

```bash
# 启动相机节点
roslaunch realsense2_camera rs_camera.launch \
    enable_infra1:=true enable_infra2:=true \
    enable_depth:=true enable_color:=true
```

标定文件存储在config/camera.yaml，包含相机内参矩阵和畸变系数。

### 8.3.2 深度图像处理

深度图像用于近距避障和地形检测。将深度图转换为点云或直接分析距离。

```python
# 深度图转点云并分析前方障碍
import cv2
import numpy as np

def depth_to_pointcloud(depth_img, fx, fy, cx, cy):
    h, w = depth_img.shape
    u, v = np.meshgrid(np.arange(w), np.arange(h))
    z = depth_img / 1000.0  # mm转m
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy
    return np.stack((x, y, z), axis=-1)

# 分析前方区域障碍距离
def front_obstacle_distance(depth_img, roi=(0.3, 0.4, 0.6, 0.6)):
    h, w = depth_img.shape
    x1 = int(roi[0]*w); x2 = int(roi[1]*w)
    y1 = int(roi[2]*h); y2 = int(roi[3]*h)
    roi_depth = depth_img[y1:y2, x1:x2]
    valid = roi_depth[roi_depth > 100]  # 过滤过近
    return np.min(valid) if len(valid) > 0 else -1
```

## 8.4 目标检测、跟踪与异常识别

### 8.4.1 基于深度学习的行人检测

目标检测采用YOLOv5轻量模型。模型输入RGB图像，输出目标类别和边界框。

```python
# 使用PyTorch和YOLOv5进行检测
import torch
import cv2
import rospy
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose

class YoloDetector:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.classes = [0]  # 只检测行人
        self.pub = rospy.Publisher('/detections', Detection2DArray, queue_size=10)
        self.sub = rospy.Subscriber('/camera/color/image_raw', Image, self.image_cb)

    def image_cb(self, msg):
        # 转换ROS Image为OpenCV
        img = bridge.imgmsg_to_cv2(msg, 'bgr8')
        results = self.model(img)
        detections = Detection2DArray()
        for det in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = det.tolist()
            d = Detection2D()
            d.bbox.center.x = (x1+x2)/2
            d.bbox.center.y = (y1+y2)/2
            d.bbox.size_x = x2-x1
            d.bbox.size_y = y2-y1
            d.results.append(ObjectHypothesisWithPose(id=int(cls), score=conf))
            detections.detections.append(d)
        self.pub.publish(detections)
```

### 8.4.2 目标跟踪

采用简单的交并比（IoU）匹配进行多目标跟踪，避免重复计数。

```python
def iou(box1, box2):
    x1 = max(box1[0], box2[0]); y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2]); y2 = min(box1[3], box2[3])
    inter = max(0, x2-x1) * max(0, y2-y1)
    area1 = (box1[2]-box1[0])*(box1[3]-box1[1])
    area2 = (box2[2]-box2[0])*(box2[3]-box2[1])
    return inter / (area1 + area2 - inter + 1e-6)
```

### 8.4.3 异常事件识别

安保巡逻中需要检测的异常事件包括：人员入侵（在禁入区域检测到人）、遗留物检测（静态物体长时间存在）、烟雾/火焰识别。本平台基于视觉实现：

入侵检测：将检测框与预设禁区多边形进行几何判断。

遗留物检测：持续观察场景，检测到非背景物体且30 s内未移动判定为遗留物。

烟雾火焰：使用轻量分类网络或颜色特征。

```python
def check_intrusion(bbox, forbidden_zone):
    # forbidden_zone为多边形顶点列表
    center_x = (bbox[0] + bbox[2]) / 2
    center_y = (bbox[1] + bbox[3]) / 2
    return point_in_polygon(center_x, center_y, forbidden_zone)
```

## 8.5 多传感器融合与时空同步

### 8.5.1 时间同步

激光雷达、相机、IMU和编码器数据具有不同时间戳，需进行同步。本平台采用以下策略：

- **硬件同步**：D435i相机内置IMU与图像硬件同步。
- **软件同步**：ROS中使用`message_filters`进行时间戳近似匹配。
- **统一时间基准**：所有节点使用ROS时间，通过`rospy.Time.now()`获取。

```python
from message_filters import Subscriber, ApproximateTimeSynchronizer

scan_sub = Subscriber('/scan', LaserScan)
image_sub = Subscriber('/camera/color/image_raw', Image)
imu_sub = Subscriber('/imu/data', Imu)

ts = ApproximateTimeSynchronizer([scan_sub, image_sub, imu_sub], 10, 0.1)
ts.registerCallback(sync_callback)
```

### 8.5.2 传感器融合里程计

轮式编码器提供高频里程计，但存在打滑和漂移；IMU提供姿态角，但积分漂移；激光雷达提供绝对位置观测。采用扩展卡尔曼滤波（EKF）融合三者。

机器人状态向量：

$$
\mathbf{x} = [x, y, \theta, v, \omega]^T
$$

状态预测由轮式编码器和IMU提供：

$$
\begin{bmatrix}
x_{k+1} \\ y_{k+1} \\ \theta_{k+1}
\end{bmatrix}
=
\begin{bmatrix}
x_k + v_k \Delta t \cos\theta_k \\
y_k + v_k \Delta t \sin\theta_k \\
\theta_k + \omega_k \Delta t
\end{bmatrix}
$$

激光雷达定位结果作为观测更新EKF,使用`robot_localization`包实现：

```yaml
# ekf.yaml
frequency: 50
odom0: /wheel_odom
odom0_config: [true, true, false, false, false, true, true, false, false, false, false, false, false, false, false]
imu0: /imu/data
imu0_config: [false, false, false, true, true, true, false, false, false, false, false, true, false, false, false]
```

## 8.6 感知软件代码实现

### 8.6.1 节点启动文件

```xml
<!-- perception.launch -->
<launch>
  <!-- 激光雷达 -->
  <include file="$(find rplidar_ros)/launch/rplidar.launch"/>
  <!-- 深度相机 -->
  <include file="$(find realsense2_camera)/launch/rs_camera.launch"/>
  <!-- 超声波 -->
  <node name="ultrasonic_node" pkg="wheel_legged_robot" type="ultrasonic_node.py"/>
  <!-- 感知融合 -->
  <node name="perception_fusion" pkg="wheel_legged_robot" type="perception_fusion.py"/>
  <!-- 目标检测 -->
  <node name="yolo_detector" pkg="wheel_legged_robot" type="yolo_detector.py"/>
</launch>
```

### 8.6.2 超声波节点

```python
#!/usr/bin/env python3
import rospy
import serial
from std_msgs.msg import Float32MultiArray

ser = serial.Serial('/dev/ttyUSB0', 115200)

def read_ultrasonic():
    # 发送读取指令，解析返回数据
    ser.write(b'\x22')
    data = ser.read(10)
    # 解析两个超声波距离
    dist1 = (data[1] << 8) | data[2]
    dist2 = (data[3] << 8) | data[4]
    return dist1, dist2

def ultrasonic_node():
    rospy.init_node('ultrasonic_node')
    pub = rospy.Publisher('/ultrasonic', Float32MultiArray, queue_size=10)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        d1, d2 = read_ultrasonic()
        msg = Float32MultiArray(data=[d1, d2])
        pub.publish(msg)
        rate.sleep()
```

## 8.7 实战：夜间巡逻感知测试

### 8.7.1 任务目标

在低照度环境下测试感知系统的可靠性，验证激光雷达、深度相机和目标检测算法在夜间的工作效果。

### 8.7.2 测试场景

选择地下车库或室外无路灯区域，光照强度<10 lux。设置以下测试项：

| 测试项 | 方法 | 通过标准 |
| :--- | :--- | :--- |
| 激光雷达建图 | 在测试区域移动，运行SLAM | 地图轮廓清晰，无严重畸变 |
| 深度相机避障 | 放置障碍物，观察点云 | 障碍物被准确检测 |
| 行人检测 | 人员在机器人前方10 m处行走 | 检测框持续跟踪 |
| 入侵报警 | 人员进入预设禁区 | 触发报警并上报 |

### 8.7.3 测试步骤

1. 启动感知系统：`roslaunch wheel_legged_robot perception.launch`
2. 运行目标检测节点，确认模型加载成功。
3. 手动控制机器人在测试区域行驶，录制传感器数据。
4. 分析录制的数据包，评估检测准确率和延迟。
5. 切换照明条件（开/关灯），重复测试。

### 8.7.4 常见问题与排查

| 问题 | 可能原因 | 排查方法 |
| :--- | :--- | :--- |
| 夜间图像噪声大 | 深度相机RGB增益过高 | 调整相机曝光参数，增加补光 |
| 激光雷达受环境光干扰 | 强光或反射面 | 调整安装角度，滤除异常点 |
| 目标检测漏检 | 模型训练数据不足、光照变化 | 收集夜间数据微调模型 |
| 时间同步误差 | 节点负载过高、网络延迟 | 降低相机分辨率，优化回调函数 |
| 超声波误报 | 声波反射、串扰 | 调整安装位置，增加滤波 |

完成本章实战后，读者应能搭建完整的机器人环境感知系统，并在实际场景中验证其性能，为后续自主导航和安保任务提供可靠的环境信息。
