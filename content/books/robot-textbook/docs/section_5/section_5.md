# 第5章 嵌入式软件开发

## 5.1 嵌入式架构与RTOS任务划分

底层控制器选用STM32F405RGT6，主频168 MHz，基于FreeRTOS构建软件框架。为保证1 kHz控制环的严格实时性，控制算法不放在RTOS任务中，而是置于硬件定时器中断服务程序内执行。RTOS负责任务调度、通信和辅助功能。

### 5.1.1 软件分层

| 层次 | 内容 |
| :--- | :--- |
| 硬件抽象层 | STM32 HAL库，外设初始化与操作 |
| 驱动层 | GPIO、PWM、ADC、SPI、I2C、CAN、UART驱动封装 |
| 中间件 | FreeRTOS内核、队列、信号量、定时器 |
| 应用层 | 控制中断、通信任务、传感器任务、安全监控任务 |

### 5.1.2 任务与中断划分

| 任务/中断 | 优先级 | 周期/触发 | 功能 |
| :--- | :--- | :--- | :--- |
| TIM6中断 | 最高 | 1 kHz | 姿态估计、平衡控制、关节伺服、轮速控制、发送状态帧 |
| CAN接收任务 | 高 | 事件触发 | 解析速度指令，更新目标值 |
| 传感器采集任务 | 中 | 1 kHz | 读取IMU和编码器，滤波后传递 |
| 安全监控任务 | 中 | 100 Hz | 监测电压/电流/温度，执行保护 |
| 日志任务 | 低 | 10 Hz | 输出调试信息到UART |

- 控制中断中禁止使用阻塞函数，不与RTOS API交互，仅通过volatile变量或中断安全队列传递数据。
- 内存使用静态分配，避免动态内存碎片。

## 5.2 驱动层设计

### 5.2.1 GPIO、PWM、ADC与定时器配置

**GPIO配置**：急停输入（上拉）、LED指示、超声波TRIG/ECHO、电机使能等。使用HAL库初始化。

```c
// 急停输入初始化
void GPIO_Init_EmergencyStop(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    __HAL_RCC_GPIOB_CLK_ENABLE();
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
}
```

PWM配置：关节电机使用TIM1和TIM8产生6路互补PWM，轮毂电机使用TIM2和TIM3产生6路PWM（或通过DRV8301由MCU提供6路PWM）。PWM频率20 kHz，死区时间1 μs。

```c
// TIM1 互补PWM初始化（关节电机左腿髋/膝）
void MX_TIM1_Init(void) {
    TIM_OC_InitTypeDef sConfigOC = {0};
    TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};
    htim1.Instance = TIM1;
    htim1.Init.Prescaler = 0;
    htim1.Init.CounterMode = TIM_COUNTERMODE_CENTERALIGNED1;
    htim1.Init.Period = 8399; // 168MHz/8400 = 20kHz
    htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim1.Init.RepetitionCounter = 0;
    htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_PWM_Init(&htim1);

    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 4200;
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
    sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
    sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
    HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1);
    HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_2);
    HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_3);

    sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;
    sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;
    sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;
    sBreakDeadTimeConfig.DeadTime = 84; // 1us
    sBreakDeadTimeConfig.BreakState = TIM_BREAK_ENABLE;
    sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;
    sBreakDeadTimeConfig.BreakFilter = 0;
    sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_ENABLE;
    HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig);

    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);
    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_1);
    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_2);
    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_3);
}
```

ADC配置：ADC1配合DMA采集6路电流采样信号，采样时间3个周期，触发源为定时器TRGO，实现与PWM同步采样。

```c
// ADC1 DMA采集配置（6通道）
void MX_ADC1_Init(void) {
    ADC_ChannelConfTypeDef sConfig = {0};
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = ADC_SCAN_ENABLE;
    hadc1.Init.ContinuousConvMode = DISABLE;
    hadc1.Init.DiscontinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_RISING;
    hadc1.Init.ExternalTrigConv = ADC_EXTERNALTRIGCONV_T1_TRGO;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 6;
    hadc1.Init.DMAContinuousRequests = ENABLE;
    hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
    HAL_ADC_Init(&hadc1);

    // 配置6个通道
    uint32_t channels[6] = {ADC_CHANNEL_0, ADC_CHANNEL_1, ADC_CHANNEL_2,
                            ADC_CHANNEL_3, ADC_CHANNEL_4, ADC_CHANNEL_5};
    for (int i = 0; i < 6; i++) {
        sConfig.Channel = channels[i];
        sConfig.Rank = i + 1;
        sConfig.SamplingTime = ADC_SAMPLETIME_3CYCLES;
        HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    }

    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buffer, 6);
}
```

定时器配置：TIM6用于1 kHz控制中断，TIM4/TIM5配置为编码器模式读取轮速。

```c
// TIM6 1kHz中断
void MX_TIM6_Init(void) {
    htim6.Instance = TIM6;
    htim6.Init.Prescaler = 167; // 1MHz
    htim6.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim6.Init.Period = 999; // 1kHz
    HAL_TIM_Base_Init(&htim6);
    HAL_TIM_Base_Start_IT(&htim6);
    HAL_NVIC_SetPriority(TIM6_DAC_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(TIM6_DAC_IRQn);
}

// TIM4编码器模式（左轮）
void MX_TIM4_Encoder_Init(void) {
    TIM_Encoder_InitTypeDef sConfig = {0};
    TIM_MasterConfigTypeDef sMasterConfig = {0};
    htim4.Instance = TIM4;
    htim4.Init.Prescaler = 0;
    htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim4.Init.Period = 65535;
    htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    sConfig.EncoderMode = TIM_ENCODERMODE_TI12;
    sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
    sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
    sConfig.IC1Prescaler = TIM_ICPSC_DIV1;
    sConfig.IC1Filter = 0;
    sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
    sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
    sConfig.IC2Prescaler = TIM_ICPSC_DIV1;
    sConfig.IC2Filter = 0;
    HAL_TIM_Encoder_Init(&htim4, &sConfig);
    HAL_TIM_Encoder_Start(&htim4, TIM_CHANNEL_ALL);
}
```

### 5.2.2 CAN/RS485驱动实现

CAN外设配置为1 Mbps，使用FIFO0接收所有帧。发送采用轮询或中断方式。

```c
// CAN初始化
void MX_CAN_Init(void) {
    CAN_FilterTypeDef sFilterConfig;
    hcan1.Instance = CAN1;
    hcan1.Init.Prescaler = 7; // 42MHz/(7+1)/5=1.05Mbps? 调整使为1Mbps
    hcan1.Init.Mode = CAN_MODE_NORMAL;
    hcan1.Init.SyncJumpWidth = CAN_SJW_1TQ;
    hcan1.Init.TimeSeg1 = CAN_BS1_11TQ;
    hcan1.Init.TimeSeg2 = CAN_BS2_4TQ;
    hcan1.Init.TimeTriggeredMode = DISABLE;
    hcan1.Init.AutoBusOff = ENABLE;
    hcan1.Init.AutoWakeUp = DISABLE;
    hcan1.Init.AutoRetransmission = ENABLE;
    hcan1.Init.ReceiveFifoLocked = DISABLE;
    hcan1.Init.TransmitFifoPriority = DISABLE;
    HAL_CAN_Init(&hcan1);

    sFilterConfig.FilterActivation = ENABLE;
    sFilterConfig.FilterMode = CAN_FILTERMODE_IDMASK;
    sFilterConfig.FilterScale = CAN_FILTERSCALE_32BIT;
    sFilterConfig.FilterIdHigh = 0x0000;
    sFilterConfig.FilterIdLow = 0x0000;
    sFilterConfig.FilterMaskIdHigh = 0x0000;
    sFilterConfig.FilterMaskIdLow = 0x0000;
    sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO0;
    sFilterConfig.FilterBank = 0;
    sFilterConfig.SlaveStartFilterBank = 14;
    HAL_CAN_ConfigFilter(&hcan1, &sFilterConfig);
    HAL_CAN_Start(&hcan1);
    HAL_CAN_ActivateNotification(&hcan1, CAN_IT_RX_FIFO0_MSG_PENDING);
}

// CAN发送函数
uint8_t can_send(uint32_t id, uint8_t *data, uint8_t len) {
    CAN_TxHeaderTypeDef tx_header;
    uint32_t tx_mailbox;
    tx_header.StdId = id;
    tx_header.IDE = CAN_ID_STD;
    tx_header.RTR = CAN_RTR_DATA;
    tx_header.DLC = len;
    tx_header.TransmitGlobalTime = DISABLE;
    return HAL_CAN_AddTxMessage(&hcan1, &tx_header, data, &tx_mailbox);
}

// CAN接收中断回调：将帧放入FreeRTOS队列
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan) {
    CAN_RxHeaderTypeDef rx_header;
    uint8_t data[8];
    HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &rx_header, data);
    can_frame_t frame;
    frame.id = rx_header.StdId;
    frame.len = rx_header.DLC;
    memcpy(frame.data, data, rx_header.DLC);
    xQueueSendFromISR(can_rx_queue, &frame, NULL);
}
```

RS485驱动预留，使用UART4 + 方向控制引脚，协议为Modbus RTU简化版，本章不展开。

### 5.2.3 SPI/I2C传感器驱动实现

SPI读IMU：ICM-20948通过SPI连接，使用DMA读取加速度计和陀螺仪数据。每次读取12字节（ACCEL_XOUT_H~GYRO_ZOUT_L）。

```c
void imu_read(float *accel, float *gyro) {
    uint8_t tx[13] = {0x80 | 0x2D}; // 读取ACCEL_XOUT_H起12字节，保留位设1
    uint8_t rx[13] = {0};
    HAL_GPIO_WritePin(IMU_CS_GPIO_Port, IMU_CS_Pin, GPIO_PIN_RESET);
    HAL_SPI_TransmitReceive(&hspi1, tx, rx, 13, 100);
    HAL_GPIO_WritePin(IMU_CS_GPIO_Port, IMU_CS_Pin, GPIO_PIN_SET);

    int16_t raw_ax = (rx[2] << 8) | rx[1]; // 根据寄存器顺序调整
    int16_t raw_ay = (rx[4] << 8) | rx[3];
    int16_t raw_az = (rx[6] << 8) | rx[5];
    int16_t raw_gx = (rx[8] << 8) | rx[7];
    int16_t raw_gy = (rx[10] << 8) | rx[9];
    int16_t raw_gz = (rx[12] << 8) | rx[11];

    accel[0] = raw_ax * ACCEL_SCALE; // ACCEL_SCALE = 2g/32768
    accel[1] = raw_ay * ACCEL_SCALE;
    accel[2] = raw_az * ACCEL_SCALE;
    gyro[0] = raw_gx * GYRO_SCALE;   // GYRO_SCALE = 2000dps/32768
    gyro[1] = raw_gy * GYRO_SCALE;
    gyro[2] = raw_gz * GYRO_SCALE;
}
```

SPI读关节编码器：AS5047P通过SPI读取14位绝对角度。

```c
uint16_t as5047p_read_angle(SPI_HandleTypeDef *hspi, GPIO_TypeDef *cs_port, uint16_t cs_pin) {
    uint16_t tx_data = 0xFFFF; // 读取角度命令
    uint16_t rx_data = 0;
    HAL_GPIO_WritePin(cs_port, cs_pin, GPIO_PIN_RESET);
    HAL_SPI_TransmitReceive(hspi, (uint8_t*)&tx_data, (uint8_t*)&rx_data, 1, 100);
    HAL_GPIO_WritePin(cs_port, cs_pin, GPIO_PIN_SET);
    return rx_data & 0x3FFF;
}
```

I2C读电流监测芯片INA226：读取总线电压和电流。

```c
void ina226_read(float *voltage, float *current) {
    uint8_t data[2];
    uint16_t raw;
    // 读总线电压寄存器（地址0x02）
    HAL_I2C_Mem_Read(&hi2c1, INA226_ADDR, 0x02, I2C_MEMADD_SIZE_8BIT, data, 2, 100);
    raw = (data[0] << 8) | data[1];
    *voltage = raw * 1.25e-3; // LSB = 1.25mV
    // 读电流寄存器（地址0x04）
    HAL_I2C_Mem_Read(&hi2c1, INA226_ADDR, 0x04, I2C_MEMADD_SIZE_8BIT, data, 2, 100);
    raw = (data[0] << 8) | data[1];
    *current = (int16_t)raw * 0.5e-3; // LSB = 0.5mA
}
```

## 5.3 电机控制底层代码

### 5.3.1 轮式电机速度环/电流环

轮毂电机采用FOC控制，驱动芯片DRV8301。电流环周期50 μs（20 kHz），速度环周期1 ms。代码结构如下：

```c
// FOC核心结构
typedef struct {
    float ia, ib, ic;        // 相电流
    float i_alpha, i_beta;   // Clarke变换结果
    float id, iq;            // Park变换结果
    float vd, vq;            // 电压参考
    float v_alpha, v_beta;   // 反Park变换结果
    float theta;             // 电角度
    float speed_ref;         // 速度参考
    float speed_fb;          // 速度反馈
} foc_t;

// 电流环PI控制器
typedef struct {
    float kp, ki;
    float integral;
    float output_max;
} pi_controller_t;

float pi_update(pi_controller_t *pi, float error) {
    pi->integral += error;
    // 积分限幅
    if (pi->integral > pi->output_max) pi->integral = pi->output_max;
    if (pi->integral < -pi->output_max) pi->integral = -pi->output_max;
    float output = pi->kp * error + pi->ki * pi->integral;
    if (output > pi->output_max) output = pi->output_max;
    if (output < -pi->output_max) output = -pi->output_max;
    return output;
}

// 速度环（1ms调用）
void speed_loop(void) {
    float speed_error = wheel.speed_ref - wheel.speed_fb;
    float iq_ref = pi_update(&speed_pi, speed_error);
    wheel.iq_ref = iq_ref;
}

// 电流环（50us中断调用）
void current_loop(void) {
    // Clarke变换
    foc.i_alpha = foc.ia;
    foc.i_beta = (foc.ia + 2*foc.ib) / 1.732f;
    // Park变换
    float sin_theta = arm_sin_f32(foc.theta);
    float cos_theta = arm_cos_f32(foc.theta);
    foc.id = foc.i_alpha * cos_theta + foc.i_beta * sin_theta;
    foc.iq = -foc.i_alpha * sin_theta + foc.i_beta * cos_theta;
    // PI控制
    foc.vd = pi_update(&id_pi, 0 - foc.id); // d轴目标0
    foc.vq = pi_update(&iq_pi, wheel.iq_ref - foc.iq);
    // 反Park变换
    foc.v_alpha = foc.vd * cos_theta - foc.vq * sin_theta;
    foc.v_beta = foc.vd * sin_theta + foc.vq * cos_theta;
    // SVPWM生成占空比并更新PWM
    svpwm_update(foc.v_alpha, foc.v_beta);
}
```

### 5.3.2 关节电机位置/力矩控制

关节电机同样基于FOC，控制模式分为位置环和力矩环。位置环周期1 ms，力矩环周期50 μs。

位置环：外环位置PI输出速度参考，内环速度PI输出力矩参考。

```c
// 关节位置环（1ms）
void joint_position_loop(void) {
    float pos_error = joint.target_angle - joint.current_angle;
    float speed_ref = pi_update(&joint_pos_pi, pos_error);
    joint.speed_ref = speed_ref;
    // 速度环
    float speed_error = joint.speed_ref - joint.current_speed;
    float iq_ref = pi_update(&joint_speed_pi, speed_error);
    joint.iq_ref = iq_ref;
}
```

力矩环：直接设置joint.iq_ref，实现力矩控制。在平衡控制中，上层平衡控制器计算关节期望力矩，直接作为iq_ref。

```c
// 力矩控制接口
void joint_set_torque(float torque) {
    joint.iq_ref = torque * TORQUE_TO_IQ; // 换算系数
}
```

## 5.4 传感器数据采集与预处理代码

IMU预处理：零偏校准和滑动平均滤波。

```c
// IMU零偏校准（上电静止500ms采集均值）
void imu_calibrate(void) {
    float sum[6] = {0};
    int n = 500;
    for (int i = 0; i < n; i++) {
        float acc[3], gyr[3];
        imu_read(acc, gyr);
        for (int j = 0; j < 3; j++) {
            sum[j] += acc[j];
            sum[j+3] += gyr[j];
        }
        HAL_Delay(1);
    }
    for (int j = 0; j < 3; j++) {
        imu_offset.acc[j] = sum[j] / n;
        imu_offset.gyr[j] = sum[j+3] / n;
    }
}

// 滑动平均滤波（窗口大小10）
float moving_average(float *buf, float new_val) {
    buf[0] = new_val; // 简单示例，实际使用环形缓冲
    float sum = 0;
    for (int i = 0; i < 10; i++) sum += buf[i];
    return sum / 10;
}
```

编码器预处理：关节角度采用AS5047P绝对角度，直接读取；轮速通过定时器编码器计数差分计算。

```c
// 轮速计算（1kHz调用）
float wheel_speed = (float)(encoder_count - last_count) * SPEED_FACTOR;
last_count = encoder_count;
```

超声波测距：

```c
float ultrasonic_read(ultrasonic_t *sonar) {
    // 发送10us触发脉冲
    HAL_GPIO_WritePin(sonar->trig_port, sonar->trig_pin, GPIO_PIN_SET);
    delay_us(10);
    HAL_GPIO_WritePin(sonar->trig_port, sonar->trig_pin, GPIO_PIN_RESET);
    // 等待回声
    uint32_t start = 0, end = 0;
    while (HAL_GPIO_ReadPin(sonar->echo_port, sonar->echo_pin) == GPIO_PIN_RESET);
    start = micros();
    while (HAL_GPIO_ReadPin(sonar->echo_port, sonar->echo_pin) == GPIO_PIN_SET);
    end = micros();
    float distance = (end - start) * 0.034 / 2; // cm
    return distance;
}
```

## 5.5 通信协议设计与实现

### 5.5.1 自定义数据帧格式

CAN帧采用标准帧，ID 11位，数据长度固定8字节（不足补0）。帧ID分配如下：

| 帧ID | 方向 | 名称 | 数据内容 |
| :--- | :--- | :--- | :--- |
| 0x100 | 底层→上层 | 状态帧 | 姿态角、关节角、轮速、故障码 |
| 0x200 | 上层→底层 | 速度指令帧 | vx, wz, 身体高度 |
| 0x300 | 上层→底层 | 参数配置帧 | PID参数、模式切换 |
| 0x400 | 双向 | 心跳帧 | 计数器、状态 |

数据编码采用定点数，缩放因子定义如下：

| 数据 | 缩放因子 | 单位 |
| :--- | :--- | :--- |
| 姿态角 | 1000 | rad |
| 关节角 | 100 | rad |
| 轮速 | 10 | rpm |
| 速度 | 1000 | m/s |
| 角速度 | 1000 | rad/s |
| 高度 | 100 | cm |
| 电流 | 100 | A |
| 电压 | 100 | V |

状态帧示例：

```c
void send_status_frame(void) {
    uint8_t data[8];
    int16_t pitch = (int16_t)(attitude.pitch * 1000);
    int16_t hip_pos = (int16_t)(joint[0].position * 100);
    int16_t wheel_speed = (int16_t)(wheel_speed_rpm * 10);
    uint16_t fault = fault_code;
    data[0] = pitch >> 8; data[1] = pitch & 0xFF;
    data[2] = hip_pos >> 8; data[3] = hip_pos & 0xFF;
    data[4] = wheel_speed >> 8; data[5] = wheel_speed & 0xFF;
    data[6] = fault >> 8; data[7] = fault & 0xFF;
    can_send(0x100, data, 8);
}
```

### 5.5.2 心跳、校验与超时处理

心跳：底层每100 ms发送心跳帧（0x400），数据包含递增计数器。上层监控，若1 s未收到心跳则报警并进入安全模式。上层每500 ms发送心跳帧，底层若2 s未收到则自动停车。

```c
// 底层心跳发送（100ms周期）
void heartbeat_task(void *arg) {
    static uint8_t counter = 0;
    uint8_t data[8] = {counter++, 0};
    can_send(0x400, data, 2);
    vTaskDelay(pdMS_TO_TICKS(100));
}
```

校验：CAN硬件自带CRC，应用层不再重复校验，但在参数配置帧中加入累加和校验，防止配置错误。

```c
uint8_t checksum(uint8_t *data, uint8_t len) {
    uint8_t sum = 0;
    for (int i = 0; i < len; i++) sum += data[i];
    return sum;
}
```

超时处理：底层检测速度指令超时（500 ms无更新），自动将目标速度置零，切换待机模式。

```c
void check_timeout(void) {
    if (HAL_GetTick() - last_cmd_time > 500) {
        target_vx = 0;
        target_wz = 0;
        mode = MODE_STANDBY;
    }
}
```

## 5.6 日志、看门狗与异常保护

日志：使用环形缓冲区存储日志信息，通过UART输出。日志任务优先级最低，每10 ms输出一条。

```c
void log_task(void *arg) {
    char log_buf[128];
    while (1) {
        if (log_queue != NULL && xQueueReceive(log_queue, log_buf, portMAX_DELAY) == pdPASS) {
            HAL_UART_Transmit(&huart1, (uint8_t*)log_buf, strlen(log_buf), 100);
        }
    }
}
```

看门狗：启用独立看门狗IWDG，超时时间1 s。在TIM6控制中断中喂狗。若程序死机，复位MCU。

```c
void IWDG_Init(void) {
    hiwdg.Instance = IWDG;
    hiwdg.Init.Prescaler = IWDG_PRESCALER_64; // 32kHz/64=500Hz
    hiwdg.Init.Reload = 500; // 1s
    HAL_IWDG_Init(&hiwdg);
}
// 在TIM6中断中调用 HAL_IWDG_Refresh(&hiwdg);
```

异常保护：安全监控任务检测电压、电流、温度。

```c
void safety_task(void *arg) {
    while (1) {
        float voltage, current;
        ina226_read(&voltage, &current);
        if (voltage < 18.0f || current > 15.0f || temp > 80.0f) {
            emergency_stop();
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void emergency_stop(void) {
    // 关闭电机使能，设置故障码
    HAL_GPIO_WritePin(EN_GPIO_Port, EN_Pin, GPIO_PIN_RESET);
    fault_code = FAULT_EMERGENCY;
    mode = MODE_STANDBY;
}
```

## 5.7 实战：底层驱动代码走读与调试

### 5.7.1 任务目标

完成底层驱动代码编写与调试，实现：GPIO/PWM/ADC正常、CAN通信、电机转动、传感器数据读取、安全保护。

### 5.7.2 调试步骤

- 编译与烧录：使用STM32CubeIDE编译代码，通过ST-Link烧录。

- 单步调试：在关键函数设置断点，观察变量值。

- PWM输出验证：示波器测量TIM1输出引脚，确认波形和死区。

- CAN通信验证：USB-CAN工具收发测试。

- 电机开环测试：给定固定PWM占空比，确认电机转动。

- 闭环测试：逐步调试电流环、速度环、位置环。

- 传感器验证：读取IMU和编码器，检查数据合理性。

- 安全功能测试：模拟过流、欠压，验证保护动作。

### 5.7.3 常见问题与排查

| 问题 | 可能原因 | 排查方法 |
| :--- | :--- | :--- |
| PWM无输出 | 定时器未启动、通道配置错误 | 检查HAL_TIM_PWM_Start是否调用，示波器测量 |
| CAN通信失败 | 终端电阻、波特率、收发器 | 检查硬件，用示波器看CAN波形 |
| 电机不转 | 使能未打开、驱动芯片故障、PWM极性 | 检查EN引脚，测量栅极波形 |
| 电流采样异常 | ADC通道错误、运放增益错误 | 检查ADC通道映射，校准运放 |
| IMU数据为零 | SPI通信失败、CS引脚错误 | 逻辑分析仪抓取SPI波形 |
| 编码器角度跳变 | 接触不良、磁场干扰 | 检查连接，调整磁铁与芯片间距 |
| 看门狗复位 | 控制中断超时、死循环 | 检查中断执行时间，优化代码 |

完成本章实战后，底层嵌入式软件应能稳定运行，为第6章运动学建模和第7章运动控制提供可靠的执行基础。
