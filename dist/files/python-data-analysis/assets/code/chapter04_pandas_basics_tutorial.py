"""第4章：Pandas 模块基础（适配 Pandas 3.x，纯新手注释版）。

本章对应原书 4.1～4.4：
1. 检查 Pandas 环境。
2. 认识 Series（一列带索引的数据）。
3. 认识 DataFrame（带行列标签的二维表格）。
4. 学习索引、数据对齐、loc、iloc、reindex 和 reset_index。

教材覆盖地图：4.1 安装；4.2 初识 Pandas；4.3.1 Series；
4.3.2 DataFrame；4.4.1 索引概念与自动对齐；4.4.2 Series 索引、
重建索引和切片；4.4.3 DataFrame 设置、重建与重置索引。

阅读提示：
- 以 # 开头的文字是注释，只用于解释，Python 不会执行。
- = 表示赋值，把右边结果保存到左边变量。
- () 通常表示调用函数，[] 可以表示列表或索引。
- . 用来访问对象的属性或方法，例如 df.shape、df.head()。
"""

import argparse

# import 表示导入模块；as pd 给 pandas 起一个通用简称 pd。
import pandas as pd


SCRIPT_NAME = "chapter04_pandas_basics_tutorial.py"
LEARNING_OBJECTIVES = (
    "区分 Series、DataFrame、索引和普通数据列的角色",
    "能用标签与位置两套方式准确选择行、列和单元格",
    "解释 Pandas 自动对齐的结果，并识别由标签不一致产生的缺失值",
    "能安全地设置、重建和重置索引",
)
SECTION_LABELS = (
    "4.1",
    "4.2",
    "4.3-series",
    "4.3-dataframe",
    "4.4-selection",
    "4.4-alignment",
    "exercises",
)
OUTLINE_LABELS = (
    "4.1 安装Pandas模块", "4.2 了解Pandas模块", "4.3.1 Series()对象",
    "4.3.2 DataFrame()对象", "4.4.1 什么是索引", "4.4.2 Series()对象的索引",
    "4.4.3 DataFrame()对象的索引",
)
SELF_CHECKS = (
    "能解释 Series 与一维 NumPy 数组最重要的差别吗？",
    "能不试错就判断 loc 与 iloc 应该使用标签还是位置吗？",
    "两个索引不同的 Series 相加时，能预测结果索引与缺失值吗？",
    "知道什么时候应使用 set_index、reindex 和 reset_index 吗？",
)


def title(text: str) -> None:
    """输出章节标题；-> None 表示函数不返回计算结果。"""

    # f-string 允许在字符串的 {} 中放变量或表达式。
    # "=" * 16 会把等号重复 16 次；\n 表示换行。
    print(f"\n{'=' * 16} {text} {'=' * 16}")


def learning_guide() -> None:
    """打印本章目标和分节学习方法。"""

    title("学习导航")
    print("本章完成后，你应该能够：")
    # enumerate(..., start=1) 同时获得从 1 开始的序号与每条目标文字。
    for number, objective in enumerate(LEARNING_OBJECTIVES, start=1):
        print(f"  {number}. {objective}")
    print("\n推荐学习法：先看对象的 index/columns/dtype，再预测选择结果，最后运行验证。")
    print("\n教材学习单元：")
    for label in OUTLINE_LABELS:
        print(f"  - {label}")
    print("命令行运行组：", "、".join(SECTION_LABELS))
    print(f"示例：python {SCRIPT_NAME} --section 4.4-selection")


def final_self_check() -> None:
    """打印章末理解检查。"""

    title("学习成果自检")
    for question in SELF_CHECKS:
        print(f"  [ ] {question}")
    print("建议把 make_scores() 中的一行姓名或一列顺序改掉，再验证自己的判断。")


def section_41_environment() -> None:
    """4.1 检查 Pandas 是否安装成功。"""

    title("4.1 Pandas 环境")
    # [4.1] 安装Pandas模块

    # pd.__version__ 是 Pandas 自己记录的版本号。
    print("Pandas 版本：", pd.__version__)

    # 现代 Pandas 可用下面的命令安装；命令应在 PyCharm Terminal 中执行，
    # 不要把它直接当作 Python 代码写在脚本中：
    # python -m pip install pandas openpyxl lxml


def section_42_first_series() -> None:
    """4.2 用一个小例子认识 Pandas。"""

    title("4.2 第一个 Series")
    # [4.2] 了解Pandas模块

    # pd.Series(data, index=..., dtype=..., name=...) 创建“一维带标签数据”：
    # data 是真正的数据；index 是每个值对应的行标签；dtype 控制存储类型；name 是整列名称。
    # 此处只传 data 和 dtype，未传 index，因此 Pandas 自动生成 0～8 的 RangeIndex。
    # pd.NA 是 Pandas 的通用缺失值标记。
    # dtype="Int64" 中的大写 I 很重要，它是允许缺失值的“可空整数类型”。
    numbers = pd.Series([1, 3, 5, 7, 9, pd.NA, 2, 4, 6], dtype="Int64")
    print(numbers)

    # isna() 对每个位置判断是否缺失，返回同长度的布尔 Series。
    # 再调用 sum() 时 True 按 1、False 按 0 相加，因此结果是缺失值个数，而不是原数值之和。
    print("缺失值数量：", numbers.isna().sum())


def section_43_series() -> None:
    """4.3.1 Series：值、索引、名称和数据类型。"""

    title("4.3.1 Series 对象")
    # [4.3.1] Series()对象

    # 列表创建 Series：第 1 个位置参数是 data；name="物理" 给整列命名，
    # 便于转成 DataFrame、合并或输出时识别；若不写 index，自动使用 0、1、2。
    physics_default = pd.Series([88, 60, 75], name="物理")
    print("默认整数索引：\n", physics_default, sep="")

    # 这次逐项指定构造参数：
    # - data=[88, 60, 75] 是 3 个值；index 必须也有 3 个标签，否则长度不一致会报错；
    # - name="物理" 是 Series 自身名称；dtype="int64" 是不允许缺失值的普通 64 位整数。
    # 若数据中可能出现 pd.NA，应使用可空整数 dtype="Int64"（大写 I）。
    physics = pd.Series(
        [88, 60, 75],
        index=["甲", "乙", "丙"],
        name="物理",
        dtype="int64",
    )
    print("姓名标签索引：\n", physics, sep="")

    # 字典使用 {键: 值} 形式；键会成为 Series 索引，值成为数据。
    # 代码分成多行时，只要仍在圆括号内，Python 就知道语句还没结束。
    chinese = pd.Series({"甲": 110, "乙": 105, "丙": 109}, name="语文")
    print("由字典创建：\n", chinese, sep="")

    # .index、.name、.dtype 都是属性，不加 ()。
    # 属性用来描述对象；方法（例如 .sum()）则需要加 () 才会执行。
    print("索引：", physics.index)
    print("列名：", physics.name)
    print("数据类型：", physics.dtype)


def make_scores() -> pd.DataFrame:
    """创建后续示例共用的成绩表，并把它作为函数结果返回。"""

    # 字典的键成为列名，每个列表成为一列；所有列表长度必须相同。
    scores = pd.DataFrame(
        {
            "姓名": ["甲", "乙", "丙"],
            "语文": [110, 105, 109],
            "数学": [105, 88, 120],
            "英语": [99, 115, 130],
        }
    )

    # return 把创建好的 DataFrame 交还给调用这个函数的位置。
    return scores


def section_43_dataframe() -> None:
    """4.3.2 DataFrame：行、列、形状和类型。"""

    title("4.3.2 DataFrame 对象")
    # [4.3.2] DataFrame()对象

    # 调用 make_scores()，把返回的表格保存到 df 变量。
    df = make_scores()
    print(df)

    # 教材 4.3.2 还演示“列表创建 DataFrame”。
    # pd.DataFrame(data, columns=...)：data 的外层列表表示整张表，每个内层列表表示一行；
    # columns 按位置给 4 列命名，列名数量必须等于每行元素数量。
    from_rows = pd.DataFrame(
        [["甲", 110, 105, 99], ["乙", 105, 88, 115], ["丙", 109, 120, 130]],
        columns=["姓名", "语文", "数学", "英语"],
    )
    print("由行列表创建：\n", from_rows, sep="")

    # shape 是 (行数, 列数) 元组；ndim 是维数；size 是单元格总数。
    print("形状 (行数, 列数)：", df.shape)
    print("维数：", df.ndim)
    print("单元格总数：", df.size)
    print("行索引：", df.index)
    print("列标签：", df.columns.tolist())

    # dtypes 是每一列的数据类型。字符串列在 Pandas 3 中通常显示为 str。
    print("各列数据类型：\n", df.dtypes, sep="")

    # head(n) 返回前 n 行的新 DataFrame；n=2 只用于预览，不会删除原表其余行。
    print("前两行：\n", df.head(2), sep="")


def section_44_index_and_selection() -> None:
    """4.4.1～4.4.2：索引概念与 Series 索引。"""

    title("4.4 索引基础与 Series 索引")

    # [4.4.1] 什么是索引
    df = make_scores()
    # set_index(keys, drop=True) 把普通列转换成行索引：keys="姓名" 指定来源列；
    # 默认 drop=True，所以“姓名”不再同时出现在普通列中。方法返回新表，原 df 不变。
    indexed = df.set_index("姓名")
    print("姓名作为行索引：\n", indexed, sep="")
    print("索引对象：", indexed.index)
    print("索引是否唯一：", indexed.index.is_unique)
    # drop=False 表示建立索引后仍保留“姓名”普通列，适合后续既要按姓名定位又要导出姓名列的场景。
    kept_name_column = df.set_index("姓名", drop=False)
    print("drop=False 同时保留姓名列：\n", kept_name_column, sep="")

    # [4.4.2] Series()对象的索引
    # loc 使用“标签”，iloc 使用从 0 开始的“位置”，二者都可写成 [行选择, 列选择]。
    # 明确写出 loc/iloc 可避免 Series 拥有整数标签时，series[0] 究竟代表标签还是位置的歧义。
    physics = pd.Series([88, 60, 75, 66, 34], index=["甲", "乙", "丙", "丁", "戊"])
    print("Series 标签取值：", physics.loc["甲"])
    print("Series 位置取值：", physics.iloc[0])
    # 外层 [] 是索引语法，内层 ["甲", "丙"] 是标签列表；列表选择返回 Series，而非单个标量。
    print("Series 多标签：\n", physics.loc[["甲", "丙"]], sep="")
    # loc 的标签切片通常“包含 stop”；iloc 与普通 Python 切片相同，“不包含 stop”。
    print("Series 标签切片包含戊：\n", physics.loc["甲":"戊"], sep="")
    print("Series 位置切片不含位置 4：\n", physics.iloc[0:4], sep="")


def section_44_alignment_and_reindex() -> None:
    """4.4.3 DataFrame 的标签/位置索引、自动对齐与重建索引。"""

    title("4.4.3 DataFrame 对象的索引")

    # [4.4.3] DataFrame()对象的索引
    indexed = make_scores().set_index("姓名")
    # loc[行标签, 列标签]：单个行标签通常返回 Series，单个行列交点返回标量；
    # 行、列都传列表时返回 DataFrame。双层方括号的内层方括号正是在构造标签列表。
    print("甲的全部成绩：\n", indexed.loc["甲"], sep="")
    print("乙的英语成绩：", indexed.loc["乙", "英语"])
    print("甲和丙的语文、数学：\n", indexed.loc[["甲", "丙"], ["语文", "数学"]], sep="")
    # iloc[行位置, 列位置] 只接受整数位置、整数列表或位置切片；:2 表示位置 0、1，不含 2。
    print("前两行、前两列：\n", indexed.iloc[:2, :2], sep="")
    print("loc 标签切片包含末端：\n", indexed.loc["甲":"丙"], sep="")
    print("iloc 位置切片不含末端：\n", indexed.iloc[0:2], sep="")

    # 两个 Series 的标签不完全相同，运算时会先按标签自动对齐。
    first = pd.Series([10, 20, 30], index=list("abc"), dtype="Int64")
    second = pd.Series([2, 3, 4], index=list("bcd"), dtype="Int64")

    # Pandas 按标签对齐后相加，不是单纯按位置相加。
    # 只有 b、c 同时存在；a、d 缺少另一边的值，所以得到 <NA>。
    print("按标签对齐相加：\n", first + second, sep="")

    # add(other, fill_value=0)：other 是另一个 Series；Pandas 先按标签对齐，
    # 某标签仅一侧缺值时用 fill_value=0 补齐再相加。若两侧同一位置都缺失，结果仍缺失。
    print("缺少一侧时按 0 计算：\n", first.add(second, fill_value=0), sep="")

    # Series 的 index/name/dtype 与前文相同：index 建立标签，name 给整列命名；
    # 下方 reindex 示例未显式 dtype，是为了让新增缺失值自然提升为可容纳缺失的类型。
    physics = pd.Series([88, 60, 75], index=["甲", "乙", "丙"], name="物理")

    # reindex(labels) 按给定标签集合和顺序生成新对象：已有标签被重排，
    # 新标签“丁”没有来源数据，因而产生缺失；原对象不会被原地修改。
    expanded = physics.reindex(["甲", "乙", "丙", "丁"])
    print("扩展索引：\n", expanded, sep="")

    # fill_value=0 只填“reindex 新增出来”的空位，不会替换原数据中本来就存在的缺失值。
    print("扩展时填 0：\n", physics.reindex(["甲", "乙", "丙", "丁"], fill_value=0), sep="")

    # 对单调有序索引，method="ffill" 用前一个有效标签的值填新位置，
    # method="bfill" 用后一个有效标签的值；无序索引使用这两种方法可能报错或得到非预期结果。
    # index=[1,3,5] 是单调递增的有序标签；dtype="Int64" 允许填充过程中仍保持可空整数。
    timed = pd.Series([10, 30, 50], index=[1, 3, 5], dtype="Int64")
    print("reindex 向前填充：\n", timed.reindex([1, 2, 3, 4, 5], method="ffill"), sep="")
    print("reindex 向后填充：\n", timed.reindex([1, 2, 3, 4, 5], method="bfill"), sep="")

    # reset_index(drop=False) 把旧索引恢复为普通列，并生成 0、1、2 的 RangeIndex；
    # 默认 drop=False。若 drop=True，则直接丢弃旧索引值，不生成“姓名”列。
    restored = indexed.reset_index()
    print("恢复默认索引：\n", restored, sep="")

    # DataFrame.reindex(index=..., columns=...) 可同时调整两个轴：
    # index 指定目标行标签及顺序，columns 指定目标列标签及顺序；
    # 原表没有“丁”行和“物理”列，所以对应位置产生 NaN。
    expanded_table = indexed.reindex(
        index=["甲", "乙", "丙", "丁"],
        columns=["语文", "物理", "数学", "英语"],
    )
    print("同时重新设置行列索引：\n", expanded_table, sep="")

    # drop=True 表示丢弃旧索引，不把旧索引保存成一列。
    filtered = indexed.loc[["甲", "丙"]].reset_index(drop=True)
    print("筛选后生成连续索引：\n", filtered, sep="")

    # dropna(subset=["英语"]) 只检查“英语”列：该列缺失才删行，其他列缺失不参与本次判断。
    # 随后 reset_index(drop=True) 丢弃不连续旧索引，建立从 0 开始的连续索引。
    dirty = make_scores()
    dirty.loc[1, "英语"] = pd.NA
    cleaned = dirty.dropna(subset=["英语"]).reset_index(drop=True)
    print("dropna 后重置连续索引：\n", cleaned, sep="")


def exercises() -> None:
    """第4章练习及自动检查。"""

    title("第4章练习")

    # 练习 1：创建以商品编号为索引、销量为值的 Series。
    # data 是销量值，index 是商品编号，name="销量" 是整列名称；三者长度需一致。
    sales = pd.Series([12, 20, 15], index=["A01", "A02", "A03"], name="销量")
    print("练习 1：\n", sales, sep="")

    # 练习 2：从成绩表中取出“丙”的数学成绩。
    scores = make_scores().set_index("姓名")
    answer_2 = scores.loc["丙", "数学"]
    print("练习 2：", answer_2)

    # 练习 3：用 iloc 取前两名学生的数学和英语两列。
    answer_3 = scores.iloc[:2, 1:3]
    print("练习 3：\n", answer_3, sep="")

    # assert 是断言：条件为 False 时程序报错，适合自动检查答案。
    assert answer_2 == 120
    pd.testing.assert_frame_equal(answer_3, scores.loc[["甲", "乙"], ["数学", "英语"]])
    print("第4章练习全部通过！")


def main() -> None:
    """运行整章或指定的学习单元。"""

    # description 是 `python 文件名.py --help` 中显示的程序简介。
    parser = argparse.ArgumentParser(description="第4章 Pandas 基础分节学习脚本")
    # action="store_true" 把无取值开关转换为布尔值；help 提供用户可读说明。
    parser.add_argument("--list", action="store_true", help="只显示学习导航")
    # choices 限制合法小节；default="all" 是未指定时的默认值。
    parser.add_argument("--section", choices=("all", *SECTION_LABELS), default="all")
    parser.add_argument("--skip-exercises", action="store_true", help="整章运行时暂不执行练习")
    args = parser.parse_args()

    print("Pandas 版本：", pd.__version__)
    learning_guide()
    if args.list:
        return

    section_runners = {
        "4.1": section_41_environment,
        "4.2": section_42_first_series,
        "4.3-series": section_43_series,
        "4.3-dataframe": section_43_dataframe,
        "4.4-selection": section_44_index_and_selection,
        "4.4-alignment": section_44_alignment_and_reindex,
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


# 只有直接运行本文件时才调用 main；被其他文件导入时不会自动运行全部示例。
if __name__ == "__main__":
    main()
