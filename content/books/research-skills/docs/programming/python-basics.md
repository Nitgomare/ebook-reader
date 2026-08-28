---
title: Python 基础与数据处理
---

# Python 基础与数据处理：从数组到图表

实验记录、传感器测量、问卷、时间序列和图像看起来各不相同，进入 Python 后都需要先回答相同的问题：数据是什么形状、每列代表什么、单位是什么、是否存在缺失或异常。下面用一段连续测量信号作为贯穿示例，练习数组、统计和作图。

## 先守住四条底线

1. 明确每个轴：`(n_samples, n_channels)` 还是 `(n_channels, n_samples)`。
2. 变量名或注释中保留单位；画图坐标必须写单位。
3. 采样率 `fs` 是数据的一部分，不能只保存幅值。
4. 原始数据只读，清洗与特征结果写入新的目录。

```python
sampling_rate_hz = 12_800
acceleration_m_s2 = np.asarray(raw_signal, dtype=np.float64)

assert acceleration_m_s2.ndim == 1
assert np.isfinite(acceleration_m_s2).all()
```

## 一个完整的连续信号例子

下面的例子模拟两个周期成分和随机噪声，再计算统计指标与单边频谱。它既可以代表声音、振动，也可以代表其他等间隔采样的连续信号。整段代码可以直接复制运行。

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)
fs = 2_000
duration_s = 2.0
t = np.arange(0, duration_s, 1 / fs)

# 假设：信号含 25 Hz 和 75 Hz 两个周期成分
signal = (
    0.9 * np.sin(2 * np.pi * 25 * t)
    + 0.35 * np.sin(2 * np.pi * 75 * t + 0.4)
    + 0.12 * rng.normal(size=t.size)
)

signal = signal - signal.mean()
rms = np.sqrt(np.mean(signal**2))
peak_to_peak = np.ptp(signal)
crest_factor = np.max(np.abs(signal)) / rms

window = np.hanning(signal.size)
spectrum = np.fft.rfft(signal * window)
frequency_hz = np.fft.rfftfreq(signal.size, d=1 / fs)
# 除以窗函数相干增益，非直流/奈奎斯特频点再乘 2
amplitude = np.abs(spectrum) / window.sum()
amplitude[1:-1] *= 2

dominant_idx = np.argmax(amplitude[1:]) + 1
print(
    f"RMS={rms:.3f}, P2P={peak_to_peak:.3f}, "
    f"crest={crest_factor:.2f}, dominant={frequency_hz[dominant_idx]:.1f} Hz"
)

fig, axes = plt.subplots(2, 1, figsize=(9, 6))
axes[0].plot(t[:800], signal[:800], linewidth=0.8)
axes[0].set(xlabel="Time [s]", ylabel="Acceleration [m/s²]", title="Time domain")
axes[1].plot(frequency_hz, amplitude, linewidth=0.9)
axes[1].set(xlim=(0, 150), xlabel="Frequency [Hz]", ylabel="Amplitude [m/s²]", title="Spectrum")
fig.tight_layout()
Path("outputs").mkdir(exist_ok=True)
fig.savefig("outputs/rotor_signal.png", dpi=180)
```

### 为什么要乘窗

截取的信号通常不恰好包含整数个周期，首尾不连续会造成频谱泄漏。Hann 窗降低旁瓣，但也改变幅值，因此示例用 `window.sum()` 做了相干增益修正。写论文时要说明窗函数、采样率、窗长、重叠比例和频率分辨率：

$$\Delta f = \frac{f_s}{N}$$

当前例子的 $\Delta f = 0.5\ \text{Hz}$。如果要分辨相距 0.2 Hz 的两个峰，2 秒数据显然不够。

## 从循环思维切换到数组思维

假设 `signals.shape == (200, 4096)`，代表 200 个样本、每个样本 4096 个采样点：

```python
# 不推荐：慢，而且容易把轴写错
rms_loop = np.array([np.sqrt(np.mean(row**2)) for row in signals])

# 推荐：明确沿采样点轴聚合
rms = np.sqrt(np.mean(signals**2, axis=1))
peak_to_peak = np.ptp(signals, axis=1)

assert rms.shape == (200,)
```

`axis=1` 的含义是“对每一行的时间点进行聚合，保留样本轴”。不要背结论；每次都问：**我要消掉哪个轴？**

## 连续测量数据的常用统计量

| 特征 | 计算 | 常见解释 | 注意 |
|---|---|---|---|
| 均方根 RMS | $\sqrt{\frac{1}{N}\sum x_i^2}$ | 总体能量/强度 | 受量程与单位影响 |
| 峰峰值 | $\max(x)-\min(x)$ | 冲击范围 | 对单个异常点敏感 |
| 峭度 | 标准化四阶矩 | 冲击性 | 小样本时不稳定 |
| 峰值因子 | 峰值 / RMS | 冲击相对强度 | RMS 很小时要防止除零 |
| 带宽能量 | 频带内 $|X(f)|^2$ 求和 | 特征频带强度 | 频率分辨率必须一致 |
| 谱质心 | $\sum fA(f)/\sum A(f)$ | 能量的频率重心 | 去直流、统一频带 |

!!! warning "不要一开始就生成几百个特征"
    特征数量大于独立样本数量时，很容易在测试集上“碰巧有效”。先用少量有明确含义的特征建立基线，再通过对照实验决定是否增加。

## 从 CSV 安全读取

```python
from pathlib import Path
import pandas as pd

data_path = Path(__file__).parent / "data" / "run_001.csv"
df = pd.read_csv(data_path)

required = {"time_s", "acc_x_m_s2", "speed_rpm"}
missing = required.difference(df.columns)
if missing:
    raise ValueError(f"缺少列: {sorted(missing)}")

df = df.sort_values("time_s").drop_duplicates("time_s")
if df[list(required)].isna().any().any():
    raise ValueError("关键列含缺失值，请先确认采集过程，不能静默填充")
```

这段代码的重点不是 Pandas 语法，而是“输入契约”：列名、单位、排序、重复值和缺失值都要显式检查。

## 练习：把图变成结论

1. 把 75 Hz 分量从 `0.35` 改为 `0.7`，比较 RMS、峰值因子和频谱。
2. 把时长改为 0.5 秒，观察频率分辨率变化。
3. 不乘窗函数重新画图，解释 25 Hz 附近的差异。
4. 将 200 段信号批量计算 RMS，确认结果形状为 `(200,)`。

完成后，不要只保存图。写三句话：**观察到什么、为什么、还不能证明什么。** 然后进入 [从零读懂机器学习](ml-from-scratch.md)。
