# 第2章 系统总体设计

## 2.1 安保巡逻场景与功能需求分析

### 2.1.1 典型应用场景

本平台面向以下四类典型场景：

| 场景 | 环境特征 | 核心需求 |
| :--- | :--- | :--- |
| 园区/厂区 | 平整路面、减速带、路缘石、坡道 | 高速轮式移动，越障能力≥80 mm |
| 楼宇/场馆 | 室内地面、门槛、电梯、窄走廊 | 结构紧凑，可通过≥600 mm宽通道 |
| 校园/公共区域 | 人流密集、动态障碍多 | 实时避障，远程视频监控 |
| 地下车库/通道 | 低照度、排水沟、减速带 | 低照度感知，越障与爬坡能力 |

### 2.1.2 功能需求分解

| 功能域 | 需求内容 | 优先级 |
| :--- | :--- | :--- |
| 移动能力 | 轮式高速移动、原地转向、腿式越障、姿态调整 | 高 |
| 平衡控制 | 站立、移动、越障中动态平衡 | 高 |
| 环境感知 | 障碍物检测、地形感知、低照度成像 | 高 |
| 自主导航 | 建图、定位、全局/局部规划、动态避障 | 高 |
| 任务管理 | 定点巡逻、随机巡逻、区域覆盖、任务调度 | 中 |
| 异常检测 | 入侵检测、遗留物识别、烟雾/火焰识别 | 中 |
| 远程交互 | 视频回传、双向语音、遥控接管 | 中 |
| 安全保护 | 急停、低压/过流保护、失稳保护、看门狗 | 高 |

### 2.1.3 性能指标分解

- **机械**：整备质量≤5 kg，腿2自由度×2，轮径100 mm，动态变形<1 mm
- **驱动**：髋关节峰值≥12 N·m，膝≥8 N·m，轮端速度≥2.5 m/s，爬坡≥15°
- **感知**：IMU零偏≤0.1°/h，编码器≥4096线，激光雷达≥12 m，深度相机近距≤0.15 m
- **计算**：底层控制1 kHz，导航10 Hz，视觉≥15 fps
- **电源**：24 V，持续放电≥5 A，峰值≥15 A，带监测保护

## 2.2 系统总体架构设计

### 2.2.1 分层架构
- ┌─────────────────────────────
- │   感知：雷达/相机/IMU采集、目标检测
- │  决策：SLAM、定位、路径规划、任务调度
- │          通信：网络通信
- └────────────────┬────────────
-                  │
- ┌────────────────┴────────────
- │  底层实时控制单元（Cortex-M4 MCU）
- │  控制：平衡控制器、关节伺服、轮速控制
- │执行：PWM、编码器采集、IMU读取、安全保护
- └────────────────┬────────────
-                  │ 功率级
-         电机、编码器、IMU、传感器

MCU运行1 kHz实时控制环，采用STM32F405RGT6，主频168 MHz。

### 2.2.2 数据流与控制流

**数据流**：传感器 → 采集 → 预处理 → 状态估计 → 决策控制 → 执行指令 → 电机

**控制流**：任务层 → 导航层（速度指令）→ 运动控制层（平衡+关节/轮力矩）→ 驱动层（电流环）→ 电机

轮腿式机器人的关键：上层速度指令不能直接驱动轮子，必须经底层平衡控制器协调腿部与轮端力矩，保持动态平衡。底层以1 kHz频率运行状态估计与控制，上层以10 Hz频率进行路径规划与决策。

### 2.2.3 工作模式

| 模式 | 说明 | 切换条件 |
| :--- | :--- | :--- |
| 待机 | 关节/轮使能，不执行运动，用于自检 | 系统上电默认 |
| 轮式 | 轮驱动为主，腿保持姿态，适合平坦高速 | 平坦地面，速度要求高 |
| 腿式 | 腿协调越障、爬坡、上下台阶，轮锁死或支撑 | 检测到台阶/坡度 |
| 自主巡逻 | 轮式基础上，导航系统自主控制 | 任务启动 |
| 遥控 | 操作员通过上位机或遥控器控制 | 人工接管 |

模式切换由上层决策，底层切换控制策略并保证平稳过渡。

## 2.3 机械、硬件、软件功能模块划分

### 2.3.1 机械模块

1. **主体框架**：碳纤维板+铝合金，上身板、腿部基座、传感器支架
2. **腿部运动模块**：髋、膝各1自由度，无刷电机+行星减速器，关节轴线重合
3. **轮端驱动模块**：100 mm轮毂电机一体轮，集成编码器
4. **外壳与附件**：电池仓、传感器罩、走线槽
5. **连接与紧固**：碳纤维管夹座、轴承、标准件

设计要点：驱动单元靠近关节轴减小惯量；轮端轻量化；腿杆中空走线。腿部采用串联结构，髋关节驱动大腿，膝关节驱动小腿，末端安装轮毂电机。每条腿2个自由度，共4个关节电机，加上2个轮毂电机，共6个执行器。

### 2.3.2 硬件模块

1. **电源管理**：24 V/2.5 Ah锂电池、DC-DC转换、保护电路、监测
2. **计算模块**：STM32F405（Cortex-M4）
3. **驱动电路**：4路关节FOC驱动 + 2路轮毂驱动，均支持电流/速度/位置闭环
4. **传感器接口**：IMU（SPI）、编码器（ABZ）、雷达（UART/USB）、相机（USB3）、超声波（GPIO）
5. **通信接口**：UART、Ethernet、USB Hub
6. **保护电路**：急停、过流、过温、防反接

### 2.3.3 软件模块

| 层次 | 内容 |
| :--- | :--- |
| 底层驱动 | GPIO/PWM/ADC/TIM/SPI/I2C/CAN/UART，电机驱动配置 |
| 实时控制 | 姿态估计（互补/卡尔曼）、平衡控制器（LQR）、关节伺服（位置/速度/力矩）、轮速控制、安全逻辑 |
| 感知与状态估计 | IMU预处理、雷达点云、视觉检测、多传感器融合（EKF） |
| 导航与决策 | SLAM、定位（AMCL/ICP）、全局规划（A*）、局部避障（DWA）、任务调度 |
| 应用与交互 | Rviz、Web监控、日志、参数配置 |

MCU裸机运行，保证1 kHz控制周期。

## 2.4 开发流程与工具链选择

### 2.4.1 开发流程

需求分析 → 总体设计 → 机械设计 → 硬件设计 → 软件实现 → 系统集成 → 测试验证 → 部署运维

### 2.4.2 工具链

| 环节 | 工具 |
| :--- | :--- |
| 机械设计 | FreeCAD / SolidWorks / Fusion 360 |
| 硬件设计 | Altium Designer / KiCad |
| 底层软件 | STM32CubeIDE / Keil MDK |
| 上层软件 | VS Code / CLion（C++/Python） |
| 版本控制 | Git + GitHub/Gitea |
| 调试工具 | CANalyzer / 逻辑分析仪 / 示波器 |

推荐MCU使用STM32F405RGT6。

## 2.5 项目文件管理与版本控制

### 2.5.1 目录结构
- wheel_legged_robot/
- ├── mechanical/
- │ ├── cad/ # 三维模型（STEP/FCStd）
- │ └── drawings/ # 二维图纸（PDF/DXF）
- ├── hardware/
- │ ├── schematic/ # 原理图
- │ ├── pcb/ # PCB文件
- │ ├── bom/ # BOM表
- │ └── datasheet/ # 数据手册
- ├── firmware/
- │ ├── core/ # 实时控制核心
- │ ├── drivers/ # 外设驱动
- │ └── control/ # 控制算法
- ├── software/
- │ ├── launch/ # 启动文件
- │ └── config/ # 参数配置
- ├── docs/ # 文档
- └── README.md

### 2.5.2 Git规范

- 分支：`main`稳定、`develop`开发、`feature/xxx`、`fix/xxx`
- 提交信息：`feat:`、`fix:`、`docs:`、`test:` 等前缀
- 文档、硬件设计文件纳入版本管理，PDF导出并标注版本号

## 2.6 搭建项目开发环境

**步骤1：创建工程并配置CAN**

在STM32CubeMX中选择STM32F405RGT6，启用CAN1（PA11/PA12），波特率1 Mbps，使能接收中断，时钟168 MHz。

**步骤2：CAN初始化代码（生成后修改）**

```c
// main.c 中 CAN 初始化
CAN_FilterTypeDef can_filter;
can_filter.FilterActivation = ENABLE;
can_filter.FilterMode = CAN_FILTERMODE_IDMASK;
can_filter.FilterScale = CAN_FILTERSCALE_32BIT;
can_filter.FilterIdHigh = 0x0000;
can_filter.FilterIdLow = 0x0000;
can_filter.FilterMaskIdHigh = 0x0000;
can_filter.FilterMaskIdLow = 0x0000;
can_filter.FilterFIFOAssignment = CAN_RX_FIFO0;
can_filter.FilterBank = 0;
can_filter.SlaveStartFilterBank = 14;
HAL_CAN_ConfigFilter(&hcan1, &can_filter);
HAL_CAN_Start(&hcan1);
HAL_CAN_ActivateNotification(&hcan1, CAN_IT_RX_FIFO0_MSG_PENDING);
```

**步骤3：创建工程并配置CAN**

```c
// 发送状态帧（周期1 ms，在定时器中断中调用）
void send_robot_state(void) {
    CAN_TxHeaderTypeDef tx_header;
    uint8_t data[8];
    uint32_t tx_mailbox;

    tx_header.StdId = 0x100;               // 状态帧ID
    tx_header.IDE = CAN_ID_STD;
    tx_header.RTR = CAN_RTR_DATA;
    tx_header.DLC = 8;
    tx_header.TransmitGlobalTime = DISABLE;

    // 填充数据：姿态角(2字节)、关节角(2字节)、轮速(2字节)、故障码(2字节)
    int16_t pitch = (int16_t)(attitude.pitch * 1000);   // 0.001 rad
    int16_t hip_pos = (int16_t)(joint_pos[0] * 100);    // 0.01 rad
    int16_t wheel_speed = (int16_t)(wheel_rpm * 10);    // 0.1 rpm
    uint16_t fault_code = fault_status;

    data[0] = pitch >> 8; data[1] = pitch & 0xFF;
    data[2] = hip_pos >> 8; data[3] = hip_pos & 0xFF;
    data[4] = wheel_speed >> 8; data[5] = wheel_speed & 0xFF;
    data[6] = fault_code >> 8; data[7] = fault_code & 0xFF;

    HAL_CAN_AddTxMessage(&hcan1, &tx_header, data, &tx_mailbox);
}

// 接收速度指令（CAN中断回调）
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan) {
    CAN_RxHeaderTypeDef rx_header;
    uint8_t data[8];
    HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &rx_header, data);

    if (rx_header.StdId == 0x200) {        // 速度指令帧
        float vx = (int16_t)((data[0] << 8) | data[1]) / 1000.0f;   // m/s
        float wz = (int16_t)((data[2] << 8) | data[3]) / 1000.0f;   // rad/s
        float height = (int16_t)((data[4] << 8) | data[5]) / 100.0f; // cm
        set_target_velocity(vx, wz, height);
    }
}
```
验证：用USB-CAN工具在PC端收/发CAN帧，确保通信正常。

联调步骤：

1. USB-CAN连接PC，启动`can_comm`节点。
2. 底层开发板烧录测试固件，连接CAN总线。
3. 验证PC与底层通信。

**常见问题与排查**：

| 问题 | 原因 | 排查 |
| :--- | :--- | :--- |
| CAN无数据 | 终端电阻未加、波特率不一致 | 检查120Ω电阻、波特率、示波器看波形 |
| MCU烧录失败 | 调试接口、芯片型号 | 检查连接，确认STM32F405 |
