# 第6章 运动学与动力学建模

## 6.1 坐标系与参数定义

### 6.1.1 坐标系定义

本平台为双足轮腿机器人，每条腿包含髋关节和膝关节两个旋转自由度，末端为驱动轮。为描述运动，建立以下坐标系：

| 坐标系 | 符号 | 定义 |
| :--- | :--- | :--- |
| 世界坐标系 | $\{W\}$ | 固定于地面，$X_W$水平向前，$Z_W$垂直向上 |
| 身体坐标系 | $\{B\}$ | 固连于身体质心，$X_B$沿身体前向，$Z_B$垂直身体向上 |
| 大腿坐标系 | $\{T_i\}$ | 固连于第$i$条腿大腿，原点在髋关节，$i=L,R$ |
| 小腿坐标系 | $\{S_i\}$ | 固连于第$i$条腿小腿，原点在膝关节 |
| 轮心坐标系 | $\{W_i\}$ | 固连于轮子，原点在轮心 |

如图6-1所示（此处以文字描述），机器人工作在矢状面（$X-Z$平面）内，所有关节旋转轴平行于$Y$轴。身体姿态由俯仰角$\theta_b$描述，定义为身体$X_B$轴与世界$X_W$轴的夹角。

### 6.1.2 几何与质量参数

| 参数 | 符号 | 数值 | 单位 |
| :--- | :--- | :--- | :--- |
| 大腿长度 | $l_1$ | 220 | mm |
| 小腿长度 | $l_2$ | 220 | mm |
| 轮子半径 | $r$ | 50 | mm |
| 身体质量 | $m_b$ | 2.5 | kg |
| 单条大腿质量 | $m_t$ | 0.5 | kg |
| 单条小腿质量 | $m_s$ | 0.35 | kg |
| 单个轮子质量 | $m_w$ | 0.45 | kg |
| 身体转动惯量 | $I_b$ | 0.02 | kg·m² |
| 大腿转动惯量（绕质心） | $I_t$ | 0.002 | kg·m² |
| 小腿转动惯量（绕质心） | $I_s$ | 0.0015 | kg·m² |
| 重力加速度 | $g$ | 9.81 | m/s² |

为简化推导，假设各连杆质心位于其几何中心，轮子为均质圆盘。

### 6.1.3 关节变量定义

每条腿定义两个关节角：

- **髋关节角** $q_{hip,i}$：大腿与身体之间的夹角。定义身体直立时$q_{hip}=0$，大腿前摆为正。
- **膝关节角** $q_{knee,i}$：小腿与大腿延长线之间的夹角。定义小腿完全伸展时$q_{knee}=0$，小腿后弯（正常站立方向）为正。

轮子滚动角为 $\phi_i$，轮心速度为 $v_i = r\dot{\phi}_i$。

## 6.2 轮腿机构运动学建模

### 6.2.1 单腿正运动学

考虑第$i$条腿，以髋关节为原点建立局部坐标系，$X$轴沿身体前向，$Z$轴垂直向上。则膝关节位置和轮心位置可表示为：

**膝关节位置**（相对髋关节）：

$$
\begin{bmatrix}
x_k \\
z_k
\end{bmatrix}
=
\begin{bmatrix}
l_1 \sin q_{hip,i} \\
-l_1 \cos q_{hip,i}
\end{bmatrix}
$$

**轮心位置**（相对髋关节）：

$$
\begin{bmatrix}
x_w \\
z_w
\end{bmatrix}
=
\begin{bmatrix}
l_1 \sin q_{hip,i} + l_2 \sin(q_{hip,i} - q_{knee,i}) \\
-l_1 \cos q_{hip,i} - l_2 \cos(q_{hip,i} - q_{knee,i})
\end{bmatrix}
$$

**轮心相对身体坐标系**：设髋关节在身体坐标系中的位置为 $(x_{hip,i}, z_{hip,i})$（对于本平台，$x_{hip,L}=0, z_{hip,L}=-h_b$；$x_{hip,R}=0, z_{hip,R}=-h_b$，因为双腿对称安装在身体两侧，矢状面内重合，但实际有宽度偏移，在二维模型中忽略）。则轮心在身体坐标系中的位置：

$$
\begin{bmatrix}
x_{w,i}^B \\
z_{w,i}^B
\end{bmatrix}
=
\begin{bmatrix}
x_{hip,i}^B \\
z_{hip,i}^B
\end{bmatrix}
+
\begin{bmatrix}
l_1 \sin q_{hip,i} + l_2 \sin(q_{hip,i} - q_{knee,i}) \\
-l_1 \cos q_{hip,i} - l_2 \cos(q_{hip,i} - q_{knee,i})
\end{bmatrix}
$$

### 6.2.2 身体正运动学

世界坐标系中，身体位姿由质心位置 $(x_b, z_b)$ 和俯仰角 $\theta_b$ 确定。则髋关节世界坐标：

$$
\begin{bmatrix}
x_{hip,i}^W \\
z_{hip,i}^W
\end{bmatrix}
=
\begin{bmatrix}
x_b \\
z_b
\end{bmatrix}
+
R(\theta_b)
\begin{bmatrix}
x_{hip,i}^B \\
z_{hip,i}^B
\end{bmatrix}
$$

其中 $R(\theta_b) = \begin{bmatrix} \cos\theta_b & -\sin\theta_b \\ \sin\theta_b & \cos\theta_b \end{bmatrix}$。

轮心世界坐标：

$$
\begin{bmatrix}
x_{w,i}^W \\
z_{w,i}^W
\end{bmatrix}
=
\begin{bmatrix}
x_b \\
z_b
\end{bmatrix}
+
R(\theta_b)
\begin{bmatrix}
x_{w,i}^B \\
z_{w,i}^B
\end{bmatrix}
$$

### 6.2.3 轮地接触约束

在轮式模式下，轮子与地面接触，轮心高度恒等于轮子半径：

$$
z_{w,i}^W = r
$$

同时，轮子在地面纯滚动，无滑动约束为：

$$
\dot{x}_{w,i}^W = r\dot{\phi}_i
$$

以上约束用于求解轮式模式下的闭链运动学。

## 6.3 正逆运动学求解

### 6.3.1 正运动学函数实现

正运动学用于给定关节角和身体位姿，计算轮心位置和足端轨迹。以下为C语言实现：

```c
#include <math.h>

typedef struct {
    float l1, l2;          // 腿节长度
    float x_hip, z_hip;    // 髋关节在身体坐标系中的位置
    float theta_b;         // 身体俯仰角
    float x_b, z_b;        // 身体质心世界坐标
} leg_params_t;

void forward_kinematics(float q_hip, float q_knee, leg_params_t *p, float *x_w, float *z_w) {
    float c_b = cosf(p->theta_b);
    float s_b = sinf(p->theta_b);

    // 轮心在身体坐标系
    float x_leg = p->l1 * sinf(q_hip) + p->l2 * sinf(q_hip - q_knee);
    float z_leg = -p->l1 * cosf(q_hip) - p->l2 * cosf(q_hip - q_knee);
    float x_b_local = p->x_hip + x_leg;
    float z_b_local = p->z_hip + z_leg;

    // 变换到世界坐标
    *x_w = p->x_b + c_b * x_b_local - s_b * z_b_local;
    *z_w = p->z_b + s_b * x_b_local + c_b * z_b_local;
}
```

### 6.3.2 逆运动学求解

已知轮心相对髋关节的位置 $(x_d, z_d)$，求解髋、膝关节角。由单腿几何关系：

$$
x_d = l_1 \sin q_{hip} + l_2 \sin(q_{hip} - q_{knee})
$$
$$
z_d = -l_1 \cos q_{hip} - l_2 \cos(q_{hip} - q_{knee})
$$

定义 $D = \sqrt{x_d^2 + z_d^2}$，由余弦定理：

$$
\cos q_{knee} = \frac{l_1^2 + l_2^2 - D^2}{2 l_1 l_2}
$$

因此：

$$
q_{knee} = \arccos\left( \frac{l_1^2 + l_2^2 - D^2}{2 l_1 l_2} \right)
$$

注意：该公式给出的 $q_{knee}$ 为正值（后弯），且需检查 $D$ 是否在可达范围内（$|l_1 - l_2| \le D \le l_1 + l_2$）。

髋关节角由下式求解：

$$
q_{hip} = \operatorname{atan2}(x_d, -z_d) - \operatorname{atan2}(l_2 \sin q_{knee}, l_1 + l_2 \cos q_{knee})
$$

但注意这里的 $q_{knee}$ 是正值，代入时应注意方向。我们重新推导：

由几何关系可得：

$$
q_{hip} = \operatorname{atan2}(x_d, -z_d) - \alpha
$$

其中 $\alpha$ 是 $l_1$ 与 $D$ 之间的夹角，$\alpha = \operatorname{atan2}(l_2 \sin q_{knee}, l_1 + l_2 \cos q_{knee})$。

C语言实现：

```c
int inverse_kinematics(float x_d, float z_d, leg_params_t *p, float *q_hip, float *q_knee) {
    float D = sqrtf(x_d*x_d + z_d*z_d);
    float cos_knee = (p->l1*p->l1 + p->l2*p->l2 - D*D) / (2 * p->l1 * p->l2);
    if (cos_knee < -1.0f || cos_knee > 1.0f) return -1; // 不可达
    *q_knee = acosf(cos_knee);  // 正值，后弯
    float alpha = atan2f(p->l2 * sinf(*q_knee), p->l1 + p->l2 * cosf(*q_knee));
    *q_hip = atan2f(x_d, -z_d) - alpha;
    return 0;
}
```

### 6.3.3 轮式模式闭链运动学

在轮式模式下，身体质心高度 $z_b$ 和俯仰角 $\theta_b$ 由关节角决定。若双腿对称站立，则 $q_{hip,L}=q_{hip,R}=q_h$，$q_{knee,L}=q_{knee,R}=q_k$。由轮地约束 $z_w = r$，可推导身体质心高度：

$$
z_b = r - \left[ \sin\theta_b \cdot x_{w}^B + \cos\theta_b \cdot z_{w}^B \right]
$$

当 $\theta_b=0$ 时：

$$
z_b = r - z_w^B = r + l_1 \cos q_h + l_2 \cos(q_h - q_k)
$$

可见，通过调节 $q_h$ 和 $q_k$ 可以改变身体高度，这就是蹲起动作的基础。

## 6.4 轮腿状态切换约束分析

### 6.4.1 支撑与摩擦约束

在腿式模式下，轮子锁死作为支撑点，需要满足以下约束：

**摩擦锥约束**：地面提供的水平力 $F_x$ 和垂直力 $F_z$ 必须满足 $|F_x| \le \mu F_z$，其中 $\mu$ 为地面摩擦系数（橡胶轮胎与硬质地面 $\mu \approx 0.8$）。

**单腿支撑稳定性**：在单腿支撑相，质心投影必须位于支撑腿轮子与地面接触点附近，否则机器人将倾倒。可通过调节身体姿态和另一条摆动腿的加速度来维持动态平衡。

**切换条件**：从轮式切换到腿式需满足：
1. 轮子锁死，电磁制动器施加。
2. 身体速度降低到安全阈值（$v < 0.5$ m/s）。
3. 目标障碍物高度在腿式越障范围内（$h_{obs} \le 80$ mm）。

从腿式切换回轮式需满足：
1. 轮子解锁。
2. 身体姿态恢复水平（$\theta_b \approx 0$）。
3. 轮地接触确认。

### 6.4.2 可达工作空间

单腿轮心相对髋关节的可达工作空间为一个圆环区域，外径 $l_1+l_2$，内径 $|l_1-l_2|$（但受关节限位限制）。本平台关节限位：

- 髋关节：$q_{hip} \in [-60^\circ, 60^\circ]$
- 膝关节：$q_{knee} \in [0^\circ, 130^\circ]$

有效工作空间为一扇形区域，可用于越障时的足端轨迹规划。

## 6.5 动力学模型

### 6.5.1 轮式模式简化动力学

在轮式模式下，将机器人简化为一个倒立摆模型。身体和腿部的质量集中到质心，质心位于髋关节上方。设等效质量 $M$，质心高度 $h_c$，身体俯仰角 $\theta$，轮子驱动提供水平力 $F$。忽略腿部细节，动力学方程为：

$$
M \ddot{x} = F - M g \theta
$$
$$
I_c \ddot{\theta} = M g h_c \theta - F h_c
$$

其中 $I_c$ 为质心绕轮轴的转动惯量。该模型用于平衡控制器设计（第7章）。

### 6.5.2 完整拉格朗日动力学

对于腿式模式，需要建立包含4个关节角度的完整动力学方程。采用拉格朗日方法，系统动能和势能分别为：

$$
T = \frac{1}{2} m_b (\dot{x}_b^2 + \dot{z}_b^2) + \frac{1}{2} I_b \dot{\theta}_b^2 + \sum_{i} \left[ \frac{1}{2} m_t \| \mathbf{v}_{t,i} \|^2 + \frac{1}{2} I_t \dot{q}_{hip,i}^2 + \frac{1}{2} m_s \| \mathbf{v}_{s,i} \|^2 + \frac{1}{2} I_s (\dot{q}_{hip,i} - \dot{q}_{knee,i})^2 + \frac{1}{2} m_w \| \mathbf{v}_{w,i} \|^2 + \frac{1}{2} I_w \dot{\phi}_i^2 \right]
$$
$$
V = m_b g z_b + \sum_{i} \left( m_t g z_{t,i} + m_s g z_{s,i} + m_w g z_{w,i} \right)
$$

拉格朗日方程：

$$
\frac{d}{dt} \frac{\partial L}{\partial \dot{\mathbf{q}}} - \frac{\partial L}{\partial \mathbf{q}} = \mathbf{Q}
$$

其中 $L = T - V$，$\mathbf{q} = [x_b, z_b, \theta_b, q_{hip,L}, q_{knee,L}, q_{hip,R}, q_{knee,R}, \phi_L, \phi_R]^T$，$\mathbf{Q}$ 为广义力。

由于推导过程冗长，本书推荐使用符号计算工具（如SymPy）自动生成动力学方程。以下为Python示例：

```python
import sympy as sp

# 定义符号变量
l1, l2, r = sp.symbols('l1 l2 r')
theta_b = sp.symbols('theta_b')
q_hip, q_knee = sp.symbols('q_hip q_knee')
x_b, z_b = sp.symbols('x_b z_b')
m_b, m_t, m_s, m_w, I_b, I_t, I_s, I_w = sp.symbols('m_b m_t m_s m_w I_b I_t I_s I_w')
g = sp.symbols('g')

# 轮心位置（相对身体）
x_w = l1*sp.sin(q_hip) + l2*sp.sin(q_hip - q_knee)
z_w = -l1*sp.cos(q_hip) - l2*sp.cos(q_hip - q_knee)

# 世界坐标
x_w_w = x_b + sp.cos(theta_b)*x_w - sp.sin(theta_b)*z_w
z_w_w = z_b + sp.sin(theta_b)*x_w + sp.cos(theta_b)*z_w

# 速度
x_w_dot = sp.diff(x_w_w, sp.Symbol('t'))
# ... 后续自动生成动能、势能和动力学方程
```

学习本章后，读者应能够利用运动学模型控制机器人的腿部姿态，并为第7章的运动控制算法提供基础。
