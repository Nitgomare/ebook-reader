## 附录C 代码仓库结构与关键代码索引

### C.1 仓库目录结构

- wheel_legged_robot/
- ├── mechanical/
- │ ├── cad/ # 三维模型（STEP/FCStd）
- │ └── drawings/ # 二维图纸（PDF/DXF）
- ├── hardware/
- │ ├── schematic/ # 原理图
- │ ├── pcb/ # PCB文件（Gerber）
- │ ├── bom/ # 物料清单
- │ └── datasheet/ # 器件数据手册
- ├── firmware/
- │ ├── core/ # 实时控制核心（1 kHz中断）
- │ │ ├── balance_control.c # LQR平衡控制器
- │ │ ├── gait_control.c # 步态规划
- │ │ └── attitude_est.c # 姿态估计
- │ ├── drivers/ # 外设驱动
- │ │ ├── spi_driver.c # SPI驱动
- │ │ ├── imu_driver.c # IMU驱动
- │ │ └── encoder_driver.c # 编码器驱动
- │ ├── control/ # 电机控制
- │ │ ├── foc.c # FOC算法
- │ │ ├── speed_pi.c # 速度环PI
- │ │ └── position_pi.c # 位置环PI
- │ └── main.c # 主程序入口
- ├── software/
- │ ├── launch/ # 启动文件
- │ └── config/ # 参数配置
- ├── docs/ # 设计文档、测试报告
- └── README.md

### C.2 关键代码索引

| 模块      | 文件 | 功能说明 |
|:--------| :--- | :--- |
| 控制中断    | `firmware/core/main.c` | 1 kHz控制环，调用各控制器 |
| LQR平衡控制 | `firmware/core/balance_control.c` | 状态反馈计算轮端力矩 |
| 摆线步态轨迹  | `firmware/core/gait_control.c` | 摆动腿足端轨迹生成 |
| 互补滤波    | `firmware/core/attitude_est.c` | IMU姿态估计 |
| FOC电流环  | `firmware/control/foc.c` | Clarke/Park变换，SVPWM |
| 目标检测    | `software/ros_ws/src/perception/yolo_detector.py` | YOLOv5行人检测 |
| 任务管理器   | `software/ros_ws/src/task_manager/task_manager.py` | 巡逻任务调度 |
| 模式切换    | `software/ros_ws/src/task_manager/mode_manager.py` | 自主/遥控切换 |
| 数据记录    | `software/ros_ws/src/data_logger/data_logger.py` | 状态与事件记录 |
