"""第3章：NumPy 模块之数组计算（适配 NumPy 2.x）。

最外层这一对三个双引号叫“模块文档字符串”（module docstring）。
它用于说明整个 Python 文件的用途，不会像普通代码那样执行计算。

使用方法：
1. 在 PyCharm 中右键本文件，选择“运行”。
2. 先观察每一节的输入、shape 和输出，再修改数据重新运行。
3. 学完后完成文件末尾的三个练习。

本文件对应教材第 3 章的 3.1～3.7，并补充 NumPy 2.x 的推荐写法。

教材覆盖地图：
- 3.1：模块、安装、dtype、ndarray 属性。
- 3.2.1～3.2.4：array/copy/ndmin、empty/zeros/ones/full、
  arange/linspace/logspace、随机数组。
- 3.2.5：asarray、frombuffer、fromiter、empty_like、zeros_like、
  ones_like、full_like。
- 3.3：数组运算、索引切片、reshape/转置、增删改查。
- 3.4：矩阵创建、元素运算、矩阵乘法、转置、逆矩阵和方程求解。
- 3.5：算术、倒数、幂、取余、舍入、三角与反三角函数。
- 3.6：sum/mean/max/min/median/average/var/std 与 axis。
- 3.7：sort/argsort/lexsort。

阅读代码前先认识几种符号：
- 以 # 开头的内容是单行注释，Python 不会执行它。
- = 是“赋值”，把右边的结果交给左边的变量保存，不是数学中的等于。
- () 常用于调用函数；括号里放传给函数的数据，叫“参数”。
- [] 可以表示列表，也可以用于数组索引和切片。
- . 表示访问一个对象所属的属性或方法，例如 sales.shape、sales.sum()。
- 英文逗号 , 用于分隔多个元素或参数。
- 英文冒号 : 在 def 行末表示接下来开始一个缩进代码块，也用于切片。
- Python 依靠四个空格的缩进判断哪些代码属于同一个函数。
"""

# argparse 是 Python 标准库，用来提供 --list、--section 等命令行学习选项。
import argparse

# import 的意思是“导入”，让当前文件可以使用其他模块提供的工具。
# numpy 是模块的原名；as np 给它起了一个更短的别名。
# 导入后，np.array 就表示 numpy 模块中的 array 函数。
import numpy as np


SCRIPT_NAME = "chapter03_numpy_tutorial.py"
LEARNING_OBJECTIVES = (
    "解释 ndarray 的 shape、ndim、size 与 dtype，而不只会背函数名",
    "能根据任务选择数组创建、索引、广播、重塑和矩阵运算方法",
    "能用 axis 说明统计方向，并用排序索引解决多条件排序问题",
    "能把三个小型业务问题改写成可验证的 NumPy 向量化计算",
)
SECTION_LABELS = ("3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "exercises")
OUTLINE_LABELS = (
    "3.1.1 什么是NumPy模块", "3.1.2 安装NumPy模块", "3.1.3 NumPy的数据类型",
    "3.1.4 ndarray()数组对象", "3.1.5 dtype数据类型对象",
    "3.2.1 创建简单的数组", "3.2.2 多种创建数组的方式", "3.2.3 根据数值范围创建数组",
    "3.2.4 生成随机数组", "3.2.5 在已有的数组中创建数组",
    "3.3.1 数组的多种运算方式", "3.3.2 数组的索引和切片", "3.3.3 数组的重塑",
    "3.3.4 数组的增、删、改、查",
    "3.4.1 创建矩阵", "3.4.2 矩阵的运算", "3.4.3 矩阵的转换",
    "3.5.1 算术函数", "3.5.2 舍入函数", "3.5.3 三角函数",
    "3.6.1 求和函数sum()", "3.6.2 平均值函数mean()",
    "3.6.3 最大值与最小值函数max()、min()", "3.6.4 中位数函数median()",
    "3.6.5 加权平均函数average()", "3.6.6 方差与标准差函数var()、std()",
    "3.7.1 sort()函数", "3.7.2 argsort()函数", "3.7.3 lexsort()函数",
)
SELF_CHECKS = (
    "看到 shape=(2, 3) 时，能说出数组有几维、多少个元素吗？",
    "能解释 axis=0 与 axis=1 分别沿哪个方向汇总吗？",
    "能在不用 Python 循环的情况下完成筛选、变形和批量计算吗？",
    "能说明 @、np.dot 和逐元素 * 的区别吗？",
)


# def 是 define（定义）的缩写，用来创建一个函数。
# title 是函数名，以后写 title(...) 就能调用它。
# text 是调用函数时需要传入的参数名。
# text: str 是类型标注，表示希望 text 是字符串；它主要帮助人和 PyCharm 阅读，
# Python 通常不会仅因为传入了其他类型就自动阻止程序运行。
# -> None 表示这个函数只负责做事，不用 return 返回计算结果。
# 行末冒号 : 表示下面缩进的代码都属于这个函数。
def title(text: str) -> None:
    # 函数内部的三个双引号字符串叫“函数文档字符串”，用于说明函数用途。
    # 注意：文档字符串外面不能添加 *。*"""文字"""* 不是合法的 Python 写法。
    """打印醒目的章节标题。"""

    # print(...) 是 Python 内置的输出函数，会把内容显示在“运行”窗口。
    # 字符串前面的 f 表示这是 f-string（格式化字符串）。
    # \n 是换行符，表示先换到下一行。
    # f-string 中的一对 {} 会执行里面的表达式，并把结果放进字符串。
    # '=' * 18 表示把字符串 "=" 重复 18 次。
    # {text} 会插入调用 title 时收到的文字。
    print(f"\n{'=' * 18} {text} {'=' * 18}")


def learning_guide() -> None:
    """打印本章目标、学习方法和分节运行说明。"""

    title("学习导航")
    print("本章完成后，你应该能够：")
    # enumerate(iterable, start=1) 同时给出编号和元素；start=1 让编号从 1 开始，默认则从 0 开始。
    for number, objective in enumerate(LEARNING_OBJECTIVES, start=1):
        print(f"  {number}. {objective}")
    print("\n推荐学习法：先预测输出，再运行验证；修改一个参数后重跑；最后独立完成练习。")
    print("\n教材学习单元：")
    for label in OUTLINE_LABELS:
        print(f"  - {label}")
    print("命令行运行组：", "、".join(SECTION_LABELS))
    print(f"示例：python {SCRIPT_NAME} --section 3.3")
    print(f"只查看导航：python {SCRIPT_NAME} --list")


def final_self_check() -> None:
    """给出可以口头回答或重新编码验证的章末问题。"""

    title("学习成果自检")
    for question in SELF_CHECKS:
        print(f"  [ ] {question}")
    print("若有一项答不清，使用 --section 只重跑对应小节，再修改示例数据验证。")


# 这里定义第 3.1 节的函数。函数名使用下划线连接单词，这是 Python 常见命名方式。
# () 中没有参数，表示调用它时不用提供数据。
def section_31_array_basics() -> None:
    """3.1 NumPy 模块、ndarray 与 dtype 基础。"""
    title("3.1 NumPy 基础")

    # [3.1.1] 什么是NumPy模块
    # NumPy 的核心价值是用同一数据类型的多维数组完成高效批量计算。
    print("NumPy 版本：", np.__version__)
    print("核心数组类型：", np.ndarray)

    # [3.1.2] 安装NumPy模块
    # 请在终端执行下一行显示的命令，不要把 pip 命令当作 Python 语句运行。
    print("安装/升级命令：python -m pip install --upgrade numpy")

    # [3.1.3] NumPy的数据类型
    # bool_ 保存真假；有符号整数可保存负数；无符号整数只保存 0 和正数。
    common_types = {
        "布尔": np.dtype(np.bool_),
        "32位整数": np.dtype(np.int32),
        "64位无符号整数": np.dtype(np.uint64),
        "64位浮点数": np.dtype(np.float64),
        "128位复数": np.dtype(np.complex128),
    }
    print("常见 dtype：", common_types)

    # [3.1.4] ndarray()数组对象
    # array(data, dtype=np.int64)：data 是销售量列表；dtype 指定每个元素用 64 位有符号整数保存。
    # ndarray 的 shape 是各维长度，ndim 是维数，size 是总元素数，itemsize 是单元素字节数。
    sales = np.array([120, 135, 98, 160], dtype=np.int64)
    print("数组：", sales)
    print("shape / ndim / size：", sales.shape, sales.ndim, sales.size)
    print("dtype / itemsize：", sales.dtype, sales.itemsize)
    mixed = np.array([1, 2.5, 3])
    print("整数和小数混合后：", mixed, mixed.dtype)

    # [3.1.5] dtype数据类型对象
    # np.dtype 描述存储类型；astype 返回转换后的新数组，不会原地修改输入数组。
    dtype_object = np.dtype("<i8")
    print("dtype 对象：", dtype_object, "字节数：", dtype_object.itemsize)
    converted = np.array([1.2, 2.8, 3.5]).astype(np.int64)
    print("astype 转为整数：", converted)


# 定义第 3.2 节函数。这里只是定义；程序执行到 main() 调用它时才运行函数体。
def section_32_create_arrays() -> None:
    """3.2.1～3.2.5：集中学习 NumPy 的全部数组创建方式。"""

    title("3.2 创建数组（3.2.1～3.2.5）")

    # [3.2.1] 创建简单的数组
    print("\n--- 3.2.1 创建简单数组 ---")

    # np.array(object, dtype=...) 把 Python 对象转换成 ndarray：
    # - 第 1 个位置参数 object 是待转换的数据；这里是 2 行 2 列的嵌套列表。
    # - dtype=np.float64 要求每个元素以 64 位浮点数保存，所以输出会显示小数点。
    # 若省略 dtype，NumPy 会根据输入推断类型；显式指定可避免后续除法或缺失值处理时类型意外变化。
    print("array：", np.array([[1, 2], [3, 4]], dtype=np.float64))

    # copy() 创建独立副本，修改副本不会影响原数组。
    original = np.array([1, 2, 3])
    copied = original.copy()
    copied[0] = 99
    print("原数组：", original, "独立副本：", copied)

    # ndmin=3 指定“结果至少三维”；原数据只有一维，NumPy 会在左侧补长度为 1 的轴，
    # 因而 [1, 2, 3] 变成 shape=(1, 1, 3)，但元素个数和值都没有改变。
    minimum_3d = np.array([1, 2, 3], ndmin=3)
    print("ndmin=3：", minimum_3d, "shape=", minimum_3d.shape)

    # [3.2.2] 多种创建数组的方式
    print("\n--- 3.2.2 多种创建数组的方式 ---")

    # np.empty(shape, dtype=...) 只分配内存而不初始化：
    # - shape=(2, 3) 表示 2 行 3 列；元组中的两个数依次是各轴长度。
    # - dtype=np.float64 表示每格用 64 位浮点数保存。
    # empty 的初始内容来自旧内存，可能每次不同，必须先写入再读取；fill(0.0) 会把所有格统一填 0。
    uninitialized = np.empty((2, 3), dtype=np.float64)
    uninitialized.fill(0.0)
    print("empty 创建后立即填充：\n", uninitialized)
    # zeros(shape, dtype) 创建全 0 数组；这里明确用 int64，所以输出为整数 0。
    print("zeros：\n", np.zeros((2, 3), dtype=np.int64))
    # ones(4) 的整数 4 是一维 shape，表示 4 个元素；省略 dtype 时默认是浮点数。
    print("ones：", np.ones(4))
    # full(shape, fill_value) 的第 2 个参数是填充值；这里得到 2×3 的全 8 数组。
    print("full：\n", np.full((2, 3), 8))

    # [3.2.3] 根据数值范围创建数组
    print("\n--- 3.2.3 根据数值范围创建数组 ---")

    # arange(start, stop, step) 类似 Python range：从 start=1 开始，每次加 step=2，
    # 到 stop=12 之前停止，因此得到 1、3、5、7、9、11；stop 永远不包含。
    print("arange：", np.arange(1, 12, 2))

    # linspace(start, stop, num) 把闭区间 [7500, 10000] 等分成 num=6 个点。
    # 它的第 3 个参数是“元素数量”而不是步长，默认同时包含 start 和 stop。
    print("linspace：", np.linspace(7500, 10000, 6))

    # logspace(start, stop, num=..., base=...) 在指数尺度上均匀取点：
    # - start=0、stop=5 是指数的起止值，不是最终数组的起止值；
    # - num=6 表示生成 6 个数；base=2 表示底数为 2；
    # 因而结果是 2**0、2**1、...、2**5。若 base=10，则会生成 10 的幂。
    geometric = np.logspace(0, 5, num=6, base=2)
    print("logspace：", geometric)

    # 棋盘 64 格用 uint64 和整数位移精确表示，避免浮点 logspace 的舍入误差。
    powers = np.arange(64, dtype=np.uint64)
    grains = np.left_shift(np.uint64(1), powers)
    print("棋盘最后 4 格麦粒数：", grains[-4:])

    # [3.2.4] 生成随机数组
    print("\n--- 3.2.4 生成随机数组 ---")

    # 现代 NumPy 用 Generator 对应教材的 rand、randn、randint。
    # default_rng(seed=42) 创建随机数生成器；seed 是“随机种子”。种子相同，随机序列可复现，
    # 便于教材、测试和调试得到相同结果；真实抽样若不要求复现，可以不传 seed。
    rng = np.random.default_rng(seed=42)
    # random(5) 从左闭右开区间 [0, 1) 的均匀分布抽 5 个数；区间内各位置机会相同。
    print("均匀分布 random：", rng.random(5))
    # normal(loc=0, scale=1, size=5) 从正态分布抽样：
    # - loc=0 是分布中心（均值 μ），改变它会让整条分布左右平移；
    # - scale=1 是标准差 σ，必须非负；越大数据越分散，越小越集中；它不是方差；
    # - size=5 是输出形状，这里表示一维 5 个数；size=(2, 3) 则会得到 2×3 数组。
    print("正态分布 normal：", rng.normal(loc=0, scale=1, size=5))
    # integers(low, high, size=...) 抽随机整数：low=1 包含，high=10 不包含，
    # 所以可能值是 1～9；size=(2, 4) 指定输出为 2 行 4 列。
    print("随机整数 integers：", rng.integers(1, 10, size=(2, 4)))

    # [3.2.5] 在已有的数组中创建数组
    print("\n--- 3.2.5 在已有对象或数组中创建数组 ---")

    # 1. asarray：输入已是合适的 ndarray 时，可能复用内存而不复制。
    source = np.array([1, 2, 3], dtype=np.int64)
    reused = np.asarray(source)
    print("asarray：", reused)
    print("asarray 是否共享内存：", np.shares_memory(source, reused))
    print("copy 是否共享内存：", np.shares_memory(source, source.copy()))

    # asarray(a, dtype=...) 也接受列表、元组和嵌套序列：a 是输入对象；
    # dtype=np.float64 会把整数转换为浮点数。输入类型不匹配时必须创建新数组，不能复用内存。
    print("列表转数组：", np.asarray([1, 2, 3], dtype=np.float64))
    print("嵌套元组转数组：\n", np.asarray(((1, 1), (1, 2), (1, 3))))

    # 2. frombuffer(buffer, dtype, count, offset)：不逐个解析文本，而是按指定格式解释原始字节。
    # - buffer 是 bytes 等缓冲区；b 前缀表示 bytes；dtype="S1" 表示每 1 字节作为一个字节字符串；
    # - count=3 只读取 3 个元素；offset=2 先跳过开头 2 字节，所以 ABCDEFGH 得到 C、D、E。
    # dtype 或 offset 写错会得到错误数值；处理二进制文件时还需确认字节序。
    byte_array = np.frombuffer(b"mingrisoft", dtype="S1")
    partial_bytes = np.frombuffer(b"ABCDEFGH", dtype="S1", count=3, offset=2)
    print("frombuffer：", byte_array)
    print("frombuffer count/offset：", partial_bytes)

    raw_numbers = np.array([100, 200, 300], dtype=np.int32).tobytes()
    print("整数转字节再还原：", np.frombuffer(raw_numbers, dtype=np.int32))

    # 3. fromiter(iterable, dtype, count)：从只能依次读取的可迭代对象创建“一维”数组。
    # iterable 是生成器；dtype=np.int64 是必填的目标类型；count=5 告诉 NumPy 预先分配 5 个位置。
    # count=-1 可读到迭代器结束，但已知长度时写出 count 通常更高效。
    iterable = (x * 2 for x in range(5))
    print("fromiter：", np.fromiter(iterable, dtype=np.int64, count=5))

    # 4～7. *_like(prototype, ...)：把 prototype 当模板，默认复制它的 shape 和 dtype，
    # 但不复制其中的值。empty_like 仍须先填充；zeros_like/ones_like/full_like 分别填 0、1、指定值。
    prototype = np.array([[1, 2], [3, 4]], dtype=np.int64)
    same_empty = np.empty_like(prototype)
    same_empty.fill(-1)
    print("empty_like 后填 -1：\n", same_empty)
    print("zeros_like：\n", np.zeros_like(prototype))
    print("ones_like：\n", np.ones_like(prototype))
    print("full_like 填 8：\n", np.full_like(prototype, 8))

    # prototype 是整数数组，直接填 0.2 会截成 0；指定浮点 dtype 才能保留小数。
    print("整数 dtype 填 0.2：\n", np.full_like(prototype, 0.2))
    print("显式指定浮点 dtype：\n", np.full_like(prototype, 0.2, dtype=np.float64))


def section_33_operations_and_indexing() -> None:
    """3.3 向量化、广播、索引、切片、重塑、拼接和条件筛选。"""
    title("3.3 数组基本操作")

    # [3.3.1] 数组的多种运算方式
    # 创建数量数组和价格数组。相同位置的数据描述同一种商品。
    quantity = np.array([2, 3, 5])
    price = np.array([10.0, 20.0, 8.0])

    # * 对两个同形状数组进行“对应元素相乘”：2*10、3*20、5*8。
    # 行尾 # 后面的文字也是注释，不参与运行。
    amount = quantity * price  # 对应元素相乘，不需要 Python for 循环
    print("各商品销售额：", amount)

    # amount.sum 中的 .sum 是数组的方法；后面的 () 表示调用该方法。
    # sum() 不指定 axis 时，会把数组中全部元素相加。
    print("销售总额：", amount.sum())

    # 教材 3.3.1 的完整运算符：+、-、*、/、** 以及比较运算。
    first = np.array([1, 2])
    second = np.array([3, 4])
    print("对应元素相加：", first + second)
    print("对应元素相减：", first - second)
    print("对应元素相乘：", first * second)
    print("对应元素相除：", first / second)
    print("对应元素求幂：", first**second)
    print("大于等于比较：", first >= second)
    print("不等于比较：", first != second)

    # 数组与单个标量运算也会广播到每个元素。
    metres = np.linspace(7500, 10000, 6)
    print("米转换成千米：", metres / 1000)

    # 广播：形状 (2, 3) 与 (3,) 从最右侧维度比较，3 与 3 相容。
    # daily_sales 有 2 行 3 列；growth 有 3 个数，恰好可以对应三列。
    daily_sales = np.array([[10, 20, 30], [40, 50, 60]])
    growth = np.array([1.10, 1.05, 1.20])

    # NumPy 自动把 growth 应用到 daily_sales 的每一行，这叫广播。
    print("按列应用不同增长率（广播）：\n", daily_sales * growth)

    # broadcast_shapes 接收两个形状元组，计算广播后会得到什么形状。
    print("广播后的结果形状：", np.broadcast_shapes(daily_sales.shape, growth.shape))

    # [3.3.2] 数组的索引和切片
    # np.arange(12) 先得到 0～11 的一维数组。
    # .reshape(3, 4) 紧接着把它改变为 3 行 4 列；元素数量仍必须是 12。
    # 这种“一个调用紧接另一个调用”的写法叫方法链式调用。
    data = np.arange(12).reshape(3, 4)
    print("二维数组：\n", data)

    # data[行索引, 列索引] 读取二维数组元素。
    # Python 索引从 0 开始，所以 [1, 2] 表示第 2 行、第 3 列。
    print("第 2 行第 3 列 data[1, 2]：", data[1, 2])

    # data[:2, 2:] 中逗号左边选择行，右边选择列。
    # :2 表示从开头取到索引 2 之前，即第 1、2 行。
    # 2: 表示从索引 2 取到末尾，即第 3 列及后面的列。
    print("前两行、后两列 data[:2, 2:]：\n", data[:2, 2:])

    # % 是取余运算符。data % 2 计算每个元素除以 2 的余数。
    # == 是比较“是否相等”，不同于赋值用的单个 =。
    # data % 2 == 0 会得到 True/False 数组，再用它筛出所有偶数。
    print("偶数（布尔索引）：", data[data % 2 == 0])

    # 一维切片完整形式是 [start:stop:step]，stop 不包含。
    line = np.arange(10)
    print("索引 3～5：", line[3:6])
    print("每隔一个取数：", line[::2])
    print("倒序：", line[::-1])

    # 关键知识：基本切片通常是视图，修改它会影响原数组。
    original = np.array([10, 20, 30, 40])

    # [1:3] 包含索引 1，不包含索引 3，所以得到原数组中的 20 和 30。
    # view 没有复制底层数据，而是“看向”original 的同一块数据。
    view = original[1:3]

    # 给数组的索引位置赋新值。由于 view 是视图，original[1] 也会变成 999。
    view[0] = 999
    print("修改切片视图后，原数组也改变：", original)

    # 明确调用 copy() 才获得独立副本。
    # 先切片，再用 .copy() 复制数据；之后两边互不影响。
    independent = original[1:3].copy()

    # -1 前面的 - 是负号，把正整数 1 变成负整数 -1。
    independent[0] = -1
    print("修改 copy 后，原数组不再改变：", original)

    # [3.3.3] 数组的重塑
    # reshape 只改变观察形状，元素总数必须保持一致。
    reshaped = np.arange(6).reshape(2, 3)
    print("一维重塑为 2×3：\n", reshaped)
    print("再重塑为 3×2：\n", reshaped.reshape(3, 2))
    print("数组转置：\n", reshaped.T)

    # [3.3.4] 数组的增、删、改、查
    # upper 是 2 行 2 列，lower 是 1 行 2 列；它们的列数相同，可以上下拼接。
    upper = np.array([[1, 2], [3, 4]])
    lower = np.array([[5, 6]])

    # (upper, lower) 是一个元组，用来把两个待拼接数组一起传给 concatenate。
    # axis=0 表示沿第 0 轴（行方向）拼接，最终得到 3 行 2 列。
    print("按行拼接 concatenate(axis=0)：\n", np.concatenate((upper, lower), axis=0))

    # hstack 水平拼接（增加列），vstack 垂直拼接（增加行）。
    left = np.array([[1, 2], [3, 4]])
    right = np.array([[10], [20]])
    print("hstack 水平拼接：\n", np.hstack((left, right)))
    print("vstack 垂直拼接：\n", np.vstack((left, np.array([[5, 6]]))))

    # np.delete(arr, obj, axis) 返回删除后的新数组，不会缩小原数组本身：
    # obj=1、axis=0 删除索引 1（第 2 行）；obj=0、axis=1 删除索引 0（第 1 列）。
    # 若省略 axis，NumPy 会先把数组展平再删除，二维结构会丢失。
    print("删除第 2 行：\n", np.delete(data, 1, axis=0))
    print("删除第 1 列：\n", np.delete(data, 0, axis=1))

    # 直接索引赋值完成“修改”。
    modified = data.copy()
    modified[1] = [40, 50, 60, 70]
    modified[2, 1] = 999
    print("修改行和单个元素：\n", modified)

    # > 是“大于”比较。np.where(条件, 条件为真时的值, 条件为假时的值)。
    # data > 5 的位置保留 data 原值，其余位置用 0 替代。
    print("where 替换（大于 5 保留，否则置 0）：", np.where(data > 5, data, 0))


def section_34_linear_algebra() -> None:
    """3.4 现代 NumPy 线性代数：二维 ndarray、@、solve。"""
    title("3.4 矩阵与线性代数")

    # [3.4.1] 创建矩阵
    # a 和 b 都是 2 行 2 列的浮点数组，可把它们看作数学中的矩阵。
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[2.0, 0.0], [1.0, 2.0]])

    print("单位矩阵：\n", np.eye(3))
    print("对角矩阵：\n", np.diag([1, 2, 3]))

    # [3.4.2] 矩阵的运算
    # 对 ndarray 来说，* 永远表示对应位置的元素相乘。
    print("对应元素相乘 a * b：\n", a * b)
    print("矩阵对应元素相加：\n", a + b)
    print("矩阵对应元素相减：\n", a - b)
    # divide(a, b, out=..., where=...) 逐元素相除：where=b!=0 是布尔掩码，仅在除数非 0 处计算；
    # out 指定结果容器，先用 full_like(a, np.nan) 填 NaN，使未计算位置有明确值。
    # 若只写 where 不提供已初始化的 out，掩码为 False 的位置可能保留未初始化内存，结果不可依赖。
    safe_division = np.divide(a, b, out=np.full_like(a, np.nan), where=b != 0)
    print("矩阵对应元素安全相除：\n", safe_division)

    # @ 是 Python 的矩阵乘法运算符；它和 * 的含义不同。
    print("矩阵乘法 a @ b：\n", a @ b)
    print("np.matmul(a, b) 等价结果：\n", np.matmul(a, b))

    # 对二维数组，np.dot(a, b) 也执行矩阵乘法；现代代码用 @ 更容易辨认。
    print("np.dot(a, b)：\n", np.dot(a, b))

    # [3.4.3] 矩阵的转换
    # a.T 访问转置属性，把原来的行变成列、列变成行。
    print("转置 a.T：\n", a.T)

    # 教材使用 np.mat 创建 matrix 对象；该类已不推荐使用，NumPy 2.x 还移除了 np.mat。
    # 因此本教程用通用的二维 ndarray 表示所有矩阵，且用 @ 明确表示矩阵乘法。

    # inv 计算逆矩阵。它用于学习矩阵概念；实际求 Ax=y 通常优先用 solve。
    inverse = np.linalg.inv(a)
    print("a 的逆矩阵：\n", inverse)
    print("a @ inv(a) 约等于单位矩阵：\n", a @ inverse)

    # allclose 用允许的浮点误差判断两个数组是否近似相等。
    print("逆矩阵验算是否通过：", np.allclose(a @ inverse, np.eye(2)))

    # 解方程 Ax = y。实际分析中，solve(A, y) 通常比 inv(A) @ y 更稳、更直接。
    # coefficients 保存方程中未知数前面的系数，targets 保存等号右边的目标值。
    coefficients = np.array([[2.0, 1.0], [1.0, 3.0]])
    targets = np.array([8.0, 13.0])

    # np.linalg 表示 NumPy 的 linear algebra（线性代数）子模块。
    # solve(系数矩阵, 目标值) 求解 Ax=y，并把答案数组赋给 solution。
    solution = np.linalg.solve(coefficients, targets)
    print("方程组解 x：", solution)

    # 把系数矩阵乘以求出的答案；若结果接近 targets，说明求解正确。
    print("验算 A @ x：", coefficients @ solution)


def section_35_math_functions() -> None:
    """3.5 通用函数 ufunc：算术、舍入和三角函数。"""
    title("3.5 数学运算函数")

    # [3.5.1] 算术函数
    # 创建一个包含四个浮点数的一维数组。
    values = np.array([0.25, 1.75, 2.0, 100.0])

    # add/subtract/multiply/divide 是运算符 +、-、*、/ 对应的 NumPy 函数。
    left = np.array([10.0, 20.0, 30.0])
    right = np.array([2.0, 5.0, 6.0])
    print("add：", np.add(left, right))
    print("subtract：", np.subtract(left, right))
    print("multiply：", np.multiply(left, right))
    print("divide：", np.divide(left, right))

    # reciprocal 对每个元素求倒数，即计算 1/x。
    print("倒数：", np.reciprocal(values))

    # power(values, 2) 对每个元素做二次方，等价于 values ** 2。
    print("平方：", np.power(values, 2))

    # mod 计算余数。Python/NumPy 的余数符号跟随除数，负数情形要特别留意。
    print("mod 取余：", np.mod(np.array([10, 20, 30]), np.array([4, 5, -8])))

    # [3.5.2] 舍入函数
    decimals = np.array([-1.8, 1.55, 1.66, -0.2])

    # round(数组, 1) 把每个元素保留 1 位小数。
    # NumPy 在正好位于中间时通常舍入到最近偶数，不保证是日常口语中的“四舍五入”。
    print("round/around（采用舍入到最近偶数规则）：", np.round(decimals, 1))

    # ceil 向正无穷方向取整，例如 -1.8 变为 -1；“向上”不等于远离 0。
    print("ceil 向正无穷方向取整：", np.ceil(decimals))

    # floor 向负无穷方向取整，例如 -0.2 变为 -1。
    print("floor 向负无穷方向取整：", np.floor(decimals))

    # [3.5.3] 三角函数
    # degrees 只是变量名，这里保存用“度”表示的角度。
    degrees = np.array([0, 30, 45, 60, 90])

    # NumPy 三角函数使用弧度；deg2rad 把 degree（度）转换为 radian（弧度）。
    radians = np.deg2rad(degrees)

    # sin 对数组中每个弧度值计算正弦。
    print("角度对应的正弦值：", np.sin(radians))

    # rad2deg 做相反转换，把弧度重新转换成度。
    print("弧度再转回角度：", np.rad2deg(radians))

    # arcsin 是 sin 的反函数，结果单位是弧度；degrees 再把弧度转成角度。
    sine_values = np.sin(radians)
    inverse_radians = np.arcsin(sine_values)
    print("反正弦得到的弧度：", inverse_radians)
    print("反正弦结果转回角度：", np.degrees(inverse_radians))

    # arccos 和 arctan 分别是余弦、正切的反函数。
    print("arccos(cos(角度))：", np.degrees(np.arccos(np.cos(radians))))
    print("arctan(tan(0/30/45度))：", np.degrees(np.arctan(np.tan(radians[:3]))))


def section_36_statistics() -> None:
    """3.6 聚合、axis、稳健统计、加权平均、总体/样本标准差。"""
    title("3.6 统计分析")

    # [3.6.1] 求和函数sum()
    # 行代表日期，列代表商品。
    # dtype=np.float64 让销量用浮点数保存，方便后续计算平均数等结果。
    sales = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]], dtype=np.float64)

    # 不传参数的 sum() 会对全部 9 个元素求和。
    print("全部元素总和：", sales.sum())

    # axis 可以理解为“计算后被消掉的方向”。
    # axis=0 消掉行：沿着上到下的方向计算，结果为每一列的和。
    print("axis=0 消去行，得到每列/每种商品之和：", sales.sum(axis=0))

    # axis=1 消掉列：沿着左到右的方向计算，结果为每一行的和。
    print("axis=1 消去列，得到每行/每天之和：", sales.sum(axis=1))

    # [3.6.2] 平均值函数mean()
    # mean 是平均值方法。axis=0 得到三种商品各自跨日期的平均销量。
    print("每种商品平均销量：", sales.mean(axis=0))

    # [3.6.3] 最大值与最小值函数max()、min()
    # max 是最大值方法。axis=1 得到每一天三种商品中的最大销量。
    print("每一天最大销量：", sales.max(axis=1))

    # min 与 max 相反，返回指定轴上的最小值。
    print("每一天最小销量：", sales.min(axis=1))

    # [3.6.4] 中位数函数median()
    # 300.0 相比其他价格特别大，可以把它视为异常值。
    prices = np.array([34.5, 36.0, 37.8, 39.0, 39.8, 300.0])

    # mean() 求算术平均数，异常大的 300 会明显拉高结果。
    print("含异常值的均值：", prices.mean())

    # median 求中位数：排序后取中间位置，通常比均值更不容易受极端值影响。
    print("含异常值的中位数（更稳健）：", np.median(prices))

    # quantile(数据, 分位点) 计算分位数。
    # [0.25, 0.5, 0.75] 分别代表 25%、50% 和 75% 的位置；0.5 分位数就是中位数。
    print("25%、50%、75% 分位数：", np.quantile(prices, [0.25, 0.5, 0.75]))

    # [3.6.5] 加权平均函数average()
    # normal_prices 与 quantities 中相同索引的元素相互对应：一个是价格，一个是销量。
    normal_prices = np.array([34.5, 36, 37.8, 39, 39.8, 33.6])
    quantities = np.array([900, 580, 230, 150, 120, 1800])

    # average 在提供 weights（权重）后计算加权平均数。
    # 销量越大的价格对最终平均价影响越大。
    print("按销量加权的平均价：", np.average(normal_prices, weights=quantities))

    # [3.6.6] 方差与标准差函数var()、std()
    # var 是 variance（方差）；correction=0/1 分别演示总体和样本口径。
    print("总体方差 correction=0：", np.var(normal_prices, correction=0))
    print("样本方差 correction=1：", np.var(normal_prices, correction=1))

    # std 是 standard deviation（标准差），用于衡量数据的分散程度。
    # correction=0 把现有数据当成完整总体；这也等价于旧参数 ddof=0。
    print("总体标准差 correction=0：", np.std(normal_prices, correction=0))

    # correction=1 把数据当作总体的一份样本，分母会做贝塞尔校正；等价于 ddof=1。
    print("样本标准差 correction=1：", np.std(normal_prices, correction=1))

    # 真实数据常含 NaN；普通 mean 会得到 NaN，nanmean 会忽略缺失值。
    # np.nan 是特殊浮点值 NaN（Not a Number），常用来表示缺失数据。
    temperatures = np.array([20.1, np.nan, 21.3, 19.8])

    # nanmean 会忽略 NaN 后再计算均值；普通 np.mean 不会自动忽略它。
    print("忽略 NaN 后的均值：", np.nanmean(temperatures))


def section_37_sorting() -> None:
    """3.7 排序、排序索引、多关键字排序。"""
    title("3.7 数组排序")

    # [3.7.1] sort()函数
    # 创建一个成绩数组。
    scores = np.array([88, 95, 76, 95, 82])

    # np.sort 默认从小到大排序，并返回一个新数组；scores 本身不会被改变。
    print("np.sort 返回排序后的副本：", np.sort(scores))

    # [3.7.2] argsort()函数
    # np.argsort(scores) 返回“从小到大排列时应该使用的原索引”，而不是返回成绩。
    # [::-1] 是切片：start 和 stop 都省略，step=-1，因此把索引顺序完全反转。
    # 反转升序索引后，就得到从高分到低分的索引。
    order = np.argsort(scores)[::-1]
    print("从高到低的索引：", order)

    # scores[order] 是整数数组高级索引：按照 order 指定的顺序取出成绩。
    print("按索引重排：", scores[order])

    # [3.7.3] lexsort()函数
    # 三个数组的相同索引代表同一个学生的三项成绩。
    total = np.array([621, 623, 620, 620, 615, 615])
    math = np.array([101, 109, 115, 108, 118, 118])
    english = np.array([117, 105, 118, 108, 98, 109])

    # lexsort 最后一个键是主键；负号把升序变成分数从高到低。
    # (-english, -math, -total) 是包含三个数组的元组。
    # lexsort 默认升序，而分数前加负号后，较高分数会变成更小的负数，从而排在前面。
    # 最后一个 -total 是第一排序条件，-math 是总分相同时的第二条件，
    # -english 是总分和数学都相同时的第三条件。
    admission_order = np.lexsort((-english, -math, -total))

    # column_stack 把三个一维数组作为三列并排放置，得到二维成绩表。
    # 紧接着的 [admission_order] 按刚才算出的学生顺序重排行。
    result = np.column_stack((total, math, english))[admission_order]
    print("按总分、数学、英语依次从高到低：\n", result)


def exercises() -> None:
    """动手练习：先读题并自己写，再参考注释下方的答案。"""
    title("章末练习")

    # 练习 1：把一周销售额转换成 2 行 3 列，并求每一列的平均值。
    # 右侧列表共有 6 个元素，创建后是一维数组，shape 为 (6,)。
    weekly_sales = np.array([120, 150, 180, 110, 170, 190])

    # reshape(2, 3) 把 6 个元素重新排成 2 行 3 列，没有增删数据。
    table = weekly_sales.reshape(2, 3)

    # axis=0 沿行方向计算，得到三列各自的平均数。
    answer_1 = table.mean(axis=0)
    print("练习 1 答案：", answer_1)

    # 练习 2：筛出温度在 [20, 25] 闭区间内的记录。
    # “闭区间”表示 20 和 25 两个端点都可以保留。
    temperature = np.array([18.5, 20.0, 23.4, 25.0, 27.2])

    # >= 表示大于等于，<= 表示小于等于，各自都会生成布尔数组。
    # & 对两个布尔数组逐元素执行“并且”：两个条件都是 True 才保留。
    # 每个比较条件必须分别放在括号中；不能对 NumPy 数组直接使用 Python 的 and。
    answer_2 = temperature[(temperature >= 20) & (temperature <= 25)]
    print("练习 2 答案：", answer_2)

    # 练习 3：10 件商品打八折，但最低价不能低于 50 元。
    # arange(20, 220, 20) 从 20 开始每次增加 20，生成到 220 之前。
    price = np.arange(20, 220, 20)

    # price * 0.8 对所有原价打八折。
    # maximum(数组, 50) 逐元素比较，取折后价和 50 中较大的那个。
    answer_3 = np.maximum(price * 0.8, 50)
    print("练习 3 原价：", price)
    print("练习 3 折后价：", answer_3)

    # 自动检查：若你改写答案但计算错了，程序会在这里报错。
    # np.testing 是 NumPy 的测试工具子模块。
    # assert_allclose 检查实际结果和预期结果是否在允许的浮点误差内近似相等。
    np.testing.assert_allclose(answer_1, [115, 160, 185])

    # assert_array_equal 要求两个数组的形状和元素完全相等。
    np.testing.assert_array_equal(answer_2, [20.0, 23.4, 25.0])
    np.testing.assert_allclose(answer_3, [50, 50, 50, 64, 80, 96, 112, 128, 144, 160])

    # 只有前三行检查均未报错，程序才会执行到这里。
    print("三个练习全部通过！")


def main() -> None:
    """运行整章或按命令行参数只运行一个学习单元。"""

    # ArgumentParser(description=...) 创建命令行解析器；description 会显示在 --help 帮助页中。
    parser = argparse.ArgumentParser(description="第3章 NumPy 分节学习脚本")
    # add_argument 增加命令行选项：action="store_true" 表示出现该开关时保存 True，
    # 未出现时为 False；help 是 --help 中的说明文字。
    parser.add_argument("--list", action="store_true", help="只显示学习目标与可选单元")
    # choices 限制允许值，输入其他文字会直接提示错误；*SECTION_LABELS 把元组元素展开；
    # default="all" 表示用户未提供 --section 时运行整章。
    parser.add_argument(
        "--section",
        choices=("all", *SECTION_LABELS),
        default="all",
        help="只运行指定小节；默认运行整章",
    )
    parser.add_argument("--skip-exercises", action="store_true", help="整章运行时暂不执行练习")
    # parse_args() 读取当前命令行并返回 Namespace；之后用 args.list、args.section 访问结果。
    args = parser.parse_args()

    # np.__version__ 是 NumPy 模块记录自身版本号的特殊属性。
    # 前后双下划线的名称常由 Python 或库预先定义，不建议初学者随意创造。
    print("NumPy 版本：", np.__version__)
    learning_guide()
    if args.list:
        return

    # 字典把学习单元名称映射到函数。选择单节时，只调用对应函数。
    section_runners = {
        "3.1": section_31_array_basics,
        "3.2": section_32_create_arrays,
        "3.3": section_33_operations_and_indexing,
        "3.4": section_34_linear_algebra,
        "3.5": section_35_math_functions,
        "3.6": section_36_statistics,
        "3.7": section_37_sorting,
        "exercises": exercises,
    }
    if args.section == "all":
        for name, runner in section_runners.items():
            if name == "exercises" and args.skip_exercises:
                continue
            runner()
    else:
        section_runners[args.section]()
    final_self_check()


# __name__ 是 Python 自动提供的特殊变量。
# 当你直接在 PyCharm 中运行本文件时，__name__ 的值就是字符串 "__main__"。
# == 用于比较左右两边是否相等；比较结果是布尔值 True 或 False。
# if 表示“如果”：只有条件为 True，下面缩进的代码才会执行。
# 这样写可以保证：直接运行本文件时会执行 main()；
# 将本文件 import 到其他程序时，则只提供函数，不会自动把整章示例都运行一遍。
if __name__ == "__main__":
    # 调用总入口函数 main，正式开始本章演示。
    main()
