"""第6章：Pandas 数据处理（Pandas 3.x，纯新手注释版）。

对应原书 6.1～6.3：数据抽取，增、删、改、查，排序与排名。
教材覆盖地图：6.1.1～6.1.4 单行、多行、列和行列联合抽取；
6.2.1～6.2.5 增行列、删除、修改、比较/query/isin/between 查询；
6.3.1～6.3.2 单列/多列/统计结果/按行排序，以及各种并列排名规则。
新版重点：Pandas 3 默认使用 Copy-on-Write，链式赋值不再可靠。
修改数据时应使用一次完整的 .loc[行条件, 列名] = 新值。
"""

import argparse

import pandas as pd


SCRIPT_NAME = "chapter06_pandas_processing_tutorial.py"
LEARNING_OBJECTIVES = (
    "根据标签或位置选择合适的 loc/iloc 数据抽取方式",
    "使用 assign、insert、concat、drop 和 loc 完成可读的增删改操作",
    "把业务条件翻译成布尔筛选、query、isin 与 between 查询",
    "能解释多列排序和不同并列排名规则对结果的影响",
)
SECTION_LABELS = ("6.1", "6.2-add", "6.2-modify", "6.2-query", "6.3", "exercises")
OUTLINE_LABELS = (
    "6.1.1 抽取指定行数据", "6.1.2 抽取多行数据", "6.1.3 抽取指定列数据",
    "6.1.4 抽取指定的行、列数据", "6.2.1 增加数据", "6.2.2 按行增加数据",
    "6.2.3 删除数据", "6.2.4 修改数据", "6.2.5 查询数据",
    "6.3.1 数据的排序", "6.3.2 数据排名",
)
SELF_CHECKS = (
    "能在写代码前说清楚筛选条件中的‘并且’与‘或者’吗？",
    "能避免链式赋值，并用一次完整的 loc 完成修改吗？",
    "能在合并或追加数据后检查行数、索引和数据类型吗？",
    "能根据业务规则选择 first、dense、min 或 average 排名吗？",
)


def title(text: str) -> None:
    """打印章节标题。"""

    print(f"\n{'=' * 15} {text} {'=' * 15}")


def learning_guide() -> None:
    """打印从业务问题到 Pandas 操作的学习路线。"""

    title("学习导航")
    print("本章完成后，你应该能够：")
    # enumerate(..., start=1) 同时产生 1、2、3…编号和对应学习目标。
    for number, objective in enumerate(LEARNING_OBJECTIVES, start=1):
        print(f"  {number}. {objective}")
    print("\n推荐学习法：先用一句中文写出目标行、目标列和业务条件，再翻译成 Pandas。")
    print("\n教材学习单元：")
    for label in OUTLINE_LABELS:
        print(f"  - {label}")
    print("命令行运行组：", "、".join(SECTION_LABELS))
    print(f"示例：python {SCRIPT_NAME} --section 6.2-query")


def final_self_check() -> None:
    """打印章末操作安全检查。"""

    title("学习成果自检")
    for question in SELF_CHECKS:
        print(f"  [ ] {question}")
    print("下一步：把 make_scores() 换成自己的小表，并为每一步写行数与关键列断言。")


def make_scores() -> pd.DataFrame:
    """创建本章共用的学生成绩表。"""

    # DataFrame(data, index=...) 中 data 字典的键是列名、列表是列数据；各列长度必须一致。
    # index 参数直接指定每一行的标签。pd.Index(values, name="姓名") 中 values 是标签列表，
    # name 是索引轴名称；它会显示在表格左上角，也便于 reset_index() 后恢复成“姓名”列。
    return pd.DataFrame(
        {
            "语文": [110, 105, 109, 99],
            "数学": [105, 88, 120, 90],
            "英语": [99, 115, 130, 120],
        },
        index=pd.Index(["甲", "乙", "丙", "丁"], name="姓名"),
    )


def section_61_extract() -> None:
    """6.1 使用 loc 和 iloc 抽取行列。"""

    title("6.1 数据抽取")
    df = make_scores()
    print("原始成绩表：\n", df, sep="")

    # [6.1.1] 抽取指定行数据
    # loc 使用标签。df.loc["甲"] 只写一个行标签，返回一维 Series；
    # Series 的索引是原 DataFrame 的列名。若要保持二维表，可写 df.loc[["甲"]]。
    print("loc 取甲这一行：\n", df.loc["甲"], sep="")

    # iloc 使用整数位置。位置从 0 开始，所以 iloc[0] 是第一行；即使行标签不是数字也不受影响。
    print("iloc 取第一行：\n", df.iloc[0], sep="")

    # [6.1.2] 抽取多行数据
    # 用标签列表选择不连续的多行；双层 [] 的内层是一个 Python 列表。
    print("甲和丙两行：\n", df.loc[["甲", "丙"]], sep="")

    # loc["甲":"丙"] 是标签切片，通常包含起止两端且依赖索引顺序；
    # iloc[:3] 是位置切片，遵循 Python 规则，包含位置 0、1、2，不包含 stop=3。
    print("标签切片甲到丙：\n", df.loc["甲":"丙"], sep="")
    print("位置切片前 3 行：\n", df.iloc[:3], sep="")

    # [6.1.3] 抽取指定列数据
    # df[["语文", "数学"]] 使用列名列表取多列，结果保持 DataFrame。
    print("两列：\n", df[["语文", "数学"]], sep="")

    # [6.1.4] 抽取指定的行、列数据
    # loc[行选择, 列选择]：冒号 : 表示所有行，列标签列表只保留“语文、数学”并维持二维结构。
    print("所有行的语文和数学：\n", df.loc[:, ["语文", "数学"]], sep="")

    # iloc[:2, 1:] 的逗号左侧选行、右侧选列：前两行，从位置 1（第 2 列）取到最后。
    print("前两行、后两列：\n", df.iloc[:2, 1:], sep="")

    # 不加列表时得到一个标量；标量就是单独的一个值。
    print("乙的英语成绩：", df.loc["乙", "英语"])


def section_62_add() -> None:
    """6.2.1～6.2.2 增加列和行。"""

    title("6.2.1 增加数据")
    df = make_scores()

    # [6.2.1] 增加数据
    # 给尚不存在的列名赋值会在末尾创建新列。右侧列表有 4 个值，按“位置”对应 4 行；
    # 长度不等于行数会报错。若右侧是带索引 Series，Pandas 会按标签对齐而非按位置硬塞。
    df["物理"] = [88, 79, 60, 50]
    print("增加物理列：\n", df, sep="")

    # loc[:, "化学"] 中 : 选择所有行；列标签“化学”原先不存在，所以赋值时创建它。
    # copy() 先建立教学副本，避免修改前一步的 df；Pandas 3 的 Copy-on-Write 仍建议明确表达复制意图。
    with_chemistry = df.copy()
    with_chemistry.loc[:, "化学"] = [90, 85, 95, 80]
    print("使用 loc 增加化学列：\n", with_chemistry, sep="")

    # assign(新列名=表达式) 返回新 DataFrame，不修改原 df。这里的 lambda 接收“整张 table”，
    # 取三科列后 mean(axis=1)：axis=1 表示横向跨列计算，因此每行得到一个学生的平均分；
    # 若 axis=0，则会纵向跨行计算，得到每门学科的平均值，无法直接作为逐学生新列。
    with_average = df.assign(
        三科平均=lambda table: table[["语文", "数学", "英语"]].mean(axis=1)
    )
    print("增加计算列：\n", with_average, sep="")

    # insert(loc, column, value) 会原地修改对象：loc=1 是插入位置（第 2 列），
    # column="化学" 是新列名，value 列表是逐行数据；同名列默认不允许重复。
    inserted = df.copy()
    inserted.insert(1, "化学", [90, 85, 95, 80])
    print("指定位置插列：\n", inserted, sep="")

    # [6.2.2] 按行增加数据
    # loc[新行标签] = 列表可增加一行；"戊" 是新索引标签，右侧 4 个值必须严格按当前列顺序排列。
    # 为减少列顺序变化导致的错位，真实项目也可赋值一个以列名为索引的 Series。
    one_more = df.copy()
    one_more.loc["戊"] = [100, 120, 99, 75]
    print("增加一行：\n", one_more, sep="")

    # 原书使用 df.append(...)，该方法已经移除。
    # 现代 Pandas 使用 pd.concat(objs, axis=0) 纵向连接多行；objs=[df, newcomers] 是待拼接对象列表。
    # 默认 axis=0 表示增加行，并按列标签对齐；两张表若缺少某列，对应位置会产生缺失值。
    # newcomers 与 df 使用相同 4 列；index 的 name="姓名" 保持拼接后索引轴名称一致。
    newcomers = pd.DataFrame(
        {"语文": [123, 138], "数学": [142, 60], "英语": [139, 99], "物理": [91, 84]},
        index=pd.Index(["己", "庚"], name="姓名"),
    )
    combined = pd.concat([df, newcomers])
    print("concat 增加多行：\n", combined, sep="")


def section_62_delete_and_modify() -> None:
    """6.2.3～6.2.4 删除与修改。"""

    title("6.2.3～6.2.4 删除与修改")
    df = make_scores()

    # [6.2.3] 删除数据
    # drop(columns=[...]) 按列标签删除并返回新表，原 df 不变；不存在的标签默认引发 KeyError，
    # 可用 errors="ignore" 忽略，但教学中保留报错更容易发现列名拼错。
    without_math = df.drop(columns=["数学"])
    print("删除数学列：\n", without_math, sep="")

    # drop(index=[...]) 按行索引标签删除；columns 与 index 两个参数让删除轴向一目了然。
    without_students = df.drop(index=["甲", "乙"])
    print("删除甲和乙：\n", without_students, sep="")

    # df["语文"] >= 105 逐行产生 True/False；df.loc[布尔条件] 只保留 True 行。
    # 末尾 copy() 让 kept 成为明确独立表，后续修改不会与原表共享逻辑状态。
    kept = df.loc[df["语文"] >= 105].copy()
    print("只保留语文不少于 105：\n", kept, sep="")

    # [6.2.4] 修改数据
    # rename(columns=列映射, index=行映射) 用“旧名称: 新名称”字典同时修改两个轴标签；
    # 未出现在映射中的标签保持不变，默认返回新表而不修改 df。
    renamed = df.rename(columns={"数学": "数学（上）"}, index={"甲": "学生甲"})
    print("修改行列标签：\n", renamed, sep="")

    # 用一次 .loc[行标签, 列标签] = 新值修改单元格，这是 Pandas 3 推荐方式。
    changed = df.copy()
    changed.loc["甲", "语文"] = 115

    # 下面这种链式赋值在 Pandas 3 中不会可靠修改原表，不要使用：
    # changed["语文"]["甲"] = 115

    # changed.loc["乙", ["数学", "英语"]] 同时选一个行标签和两个列标签；
    # 右侧 [95, 118] 按列标签列表的顺序配对，数量不一致会报错。
    changed.loc["乙", ["数学", "英语"]] = [95, 118]

    # changed.loc[行条件, "英语"] = 100 用一次完整索引完成条件更新；标量 100 会广播到全部命中行。
    # 不要写 changed["英语"][条件] = 100：这是链式赋值，在 Pandas 3 中不能可靠修改原表。
    changed.loc[changed["英语"] < 100, "英语"] = 100
    print("修改后的数据：\n", changed, sep="")

    # 整行与整列也能一次修改。iloc 使用位置，下面在副本上演示。
    position_changed = df.copy()
    position_changed.iloc[0, :] = [120, 115, 109]  # 修改第一整行
    position_changed.iloc[:, 0] = [115, 108, 112, 118]  # 修改第一整列
    position_changed.iloc[1, 2] = 125  # 修改第二行第三列
    print("iloc 修改行、列和单元格：\n", position_changed, sep="")


def section_62_query() -> None:
    """6.2.5 使用比较、isin、between 和 query 查询。"""

    title("6.2.5 查询数据")
    # [6.2.5] 查询数据
    df = make_scores().reset_index()

    # df["语文"] > 105 得到布尔 Series，再放入 df[...] 筛选 True 行。
    print("语文大于 105：\n", df[df["语文"] > 105], sep="")

    # & 表示逐元素“并且”，| 表示逐元素“或者”，不能用 Python 的 and/or 处理整列。
    # 每个比较条件必须加圆括号，因为 & 和 | 与比较运算符的优先级容易产生错误解释。
    both = df[(df["语文"] > 105) & (df["数学"] > 88)]
    either = df[(df["语文"] > 105) | (df["数学"] > 100)]
    print("两个条件都满足：\n", both, sep="")
    print("至少满足一个条件：\n", either, sep="")

    # Series.isin(values) 对每个姓名检查是否属于 values=["甲", "丙"]，返回布尔 Series；
    # 再放入 df[...] 才完成整行筛选。它比多个 == 再用 | 连接更简洁。
    print("姓名属于甲或丙：\n", df[df["姓名"].isin(["甲", "丙"])], sep="")

    # 对整个 DataFrame 调用 isin，会逐单元格判断是否属于给定集合；
    # 不匹配位置显示 NaN，适合检查某些值出现在哪些列，而不是筛选整行。
    print("全表中值为 88 或 120 的位置：\n", df[df.isin([88, 120])], sep="")

    # 用一张“学生信息表”的姓名列表筛选另一张“成绩表”，演示跨表 isin。
    student_info = pd.DataFrame({"姓名": ["甲", "乙", "丙", "丁"], "性别": ["男", "女", "女", "男"]})
    female_names = student_info.loc[student_info["性别"] == "女", "姓名"]
    female_scores = df[df["姓名"].isin(female_names)]
    print("利用信息表筛选女生成绩：\n", female_scores, sep="")

    # between(left, right, inclusive="both") 判断闭区间；默认包含 100 和 110 两端。
    # 可用 inclusive="left"、"right" 或 "neither" 调整边界是否包含。
    print("语文在 100～110：\n", df[df["语文"].between(100, 110)], sep="")

    # query(expr) 把筛选条件写成字符串；列名可直接引用，包含空格/符号的列名需用反引号包住。
    # @minimum 表示引用字符串外的 Python 变量，而非查找名为 minimum 的列。
    minimum = 105
    queried = df.query("语文 > @minimum and 数学 > 88")
    # @minimum 表示引用 query 字符串外部的 Python 变量 minimum。
    print("query 查询：\n", queried, sep="")


def section_63_sort_and_rank() -> None:
    """6.3 sort_values 排序和 rank 排名。"""

    title("6.3 排序与排名")

    books = pd.DataFrame(
        {
            "图书名称": ["Python", "Pandas", "NumPy", "Excel", "SQL"],
            "类别": ["编程", "编程", "编程", "办公", "数据库"],
            "销量": [120, 150, 150, 90, 110],
        }
    )

    # [6.3.1] 数据的排序
    # sort_values(by, ascending, ignore_index)：by="销量" 是排序键；ascending=False 从大到小；
    # ignore_index=True 丢弃原行索引并生成 0～n-1，结果是新表，原 books 顺序不变。
    sorted_books = books.sort_values("销量", ascending=False, ignore_index=True)
    print("销量降序：\n", sorted_books, sep="")

    # 多列排序时 by 与 ascending 两个列表按位置配对：先按“类别”升序 True，
    # 类别相同再按“销量”降序 False；两个列表长度必须一致。
    multi_sorted = books.sort_values(
        by=["类别", "销量"], ascending=[True, False], ignore_index=True
    )
    print("多列排序：\n", multi_sorted, sep="")

    # 教材的“统计结果排序”：先按类别分组求销量和，再按销量降序。
    # groupby("类别", as_index=False) 按类别分组且把类别保留为普通列；sum() 汇总销量；
    # 最后的 sort_values(ascending=False, ignore_index=True) 降序并重建连续索引。
    category_sales = (
        books.groupby("类别", as_index=False)["销量"]
        .sum()
        .sort_values("销量", ascending=False, ignore_index=True)
    )
    print("分组统计后排序：\n", category_sales, sep="")

    # sort_values(by=0, axis=1)：axis=1 表示重新排列“列”，by=0 表示根据行标签 0 的值判断列顺序。
    # 它不是给每一行内部的数单独排序，而是整列一起移动，实际项目较少使用。
    # columns 为三列指定 A/B/C 标签；每个内层列表是一行，长度必须与 columns 一致。
    numeric = pd.DataFrame([[3, 1, 2], [30, 10, 20]], columns=["A", "B", "C"])
    columns_sorted_by_first_row = numeric.sort_values(by=0, axis=1)
    print("按第 1 行的值重排列：\n", columns_sorted_by_first_row, sep="")

    # [6.3.2] 数据排名
    # rank(method=..., ascending=False) 中 ascending=False 表示销量越大名次数字越小。
    # method 决定并列规则：first 按原出现顺序拆开并列；dense 并列后不跳号；
    # average 取并列名次平均值；min 取并列可占名次中的最小值；max 取最大值。
    # astype("Int64") 把本来是浮点的整数名次转为可空整数；average 可能出现 1.5，所以保留浮点。
    ranked = books.assign(
        顺序排名=books["销量"].rank(method="first", ascending=False).astype("Int64"),
        密集排名=books["销量"].rank(method="dense", ascending=False).astype("Int64"),
        平均排名=books["销量"].rank(method="average", ascending=False),
        最小值排名=books["销量"].rank(method="min", ascending=False).astype("Int64"),
        最大值排名=books["销量"].rank(method="max", ascending=False).astype("Int64"),
    )
    print("排名：\n", ranked, sep="")


def exercises() -> None:
    """第6章练习及自动检查。"""

    title("第6章练习")
    df = make_scores()

    # 练习 1：筛选数学至少 100 且英语至少 100 的学生。
    answer_1 = df[(df["数学"] >= 100) & (df["英语"] >= 100)]

    # 练习 2：增加总分列。
    # sum(axis=1) 横向汇总每个学生三科；assign(总分=...) 返回增加总分列的新表。
    answer_2 = df.assign(总分=df.sum(axis=1))

    # 练习 3：按总分降序排列。
    answer_3 = answer_2.sort_values("总分", ascending=False)

    assert answer_1.index.tolist() == ["丙"]
    assert answer_2.loc["甲", "总分"] == 314
    assert answer_3.index[0] == "丙"
    print("第6章练习全部通过！")


def main() -> None:
    """运行整章或指定的数据处理单元。"""

    # description 是 --help 页面中的程序简介；add_argument 定义支持的选项及规则。
    parser = argparse.ArgumentParser(description="第6章 Pandas 数据处理分节学习脚本")
    # action="store_true" 表示开关出现即为 True；choices 限制小节；default 是省略时的值。
    parser.add_argument("--list", action="store_true", help="只显示学习导航")
    parser.add_argument("--section", choices=("all", *SECTION_LABELS), default="all")
    parser.add_argument("--skip-exercises", action="store_true", help="整章运行时暂不执行练习")
    args = parser.parse_args()

    print("Pandas 版本：", pd.__version__)
    learning_guide()
    if args.list:
        return

    section_runners = {
        "6.1": section_61_extract,
        "6.2-add": section_62_add,
        "6.2-modify": section_62_delete_and_modify,
        "6.2-query": section_62_query,
        "6.3": section_63_sort_and_rank,
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


if __name__ == "__main__":
    main()
