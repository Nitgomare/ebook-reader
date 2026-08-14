"""第7章：Pandas 数据清洗（Pandas 3.x，纯新手注释版）。

对应原书 7.1～7.5：缺失值、重复值、异常值、字符串清洗和数据转换。
教材覆盖地图：7.1.1～7.1.3 缺失值概念、查看与处理；7.2 重复值；
7.3 业务范围、标准差和 IQR 异常检测；7.4.1～7.4.4 字符串常用函数、
replace、split、contains；7.5.1～7.5.3 map、cut 和 get_dummies。
现代补充：
- 不存在适用于所有项目的“缺失率超过 30% 就删除”规则；处理方法取决于业务含义、
  缺失机制和后续分析目标。
- Pandas 3 默认使用新的字符串 dtype 和 Copy-on-Write。
- 字符串 contains/replace 若只是查找普通文字，明确写 regex=False 更安全。
"""

import argparse

import numpy as np
import pandas as pd


SCRIPT_NAME = "chapter07_pandas_cleaning_tutorial.py"
LEARNING_OBJECTIVES = (
    "先量化缺失、重复、异常和脏字符串，再选择有依据的处理策略",
    "区分业务规则、统计规则与数据录入错误，避免机械删除异常值",
    "使用字符串向量化方法完成规范化、拆分、替换与筛选",
    "根据类别是否有顺序，正确选择映射、分箱、有序类别或 one-hot",
)
SECTION_LABELS = ("7.1", "7.2", "7.3", "7.4", "7.5", "exercises")
OUTLINE_LABELS = (
    "7.1.1 了解数据中的缺失值", "7.1.2 查看缺失值", "7.1.3 处理缺失值",
    "7.2 处理数据中的重复值", "7.3 数据中异常值的检测与处理",
    "7.4.1 字符串对象中的常见函数", "7.4.2 替换字符串—replace()函数",
    "7.4.3 数据切分—split()函数", "7.4.4 判断字符串—contains()函数",
    "7.5.1 通过字典映射—map()函数", "7.5.2 数据分割—cut()函数",
    "7.5.3 数据分类—get_dummies()函数",
)
SELF_CHECKS = (
    "能说明每个缺失值代表‘未知’、‘不适用’还是‘采集失败’吗？",
    "删除重复记录前，能先定义判断重复所需的业务键吗？",
    "发现异常值时，能先保留原值并记录处理原因吗？",
    "能解释有序编码与 one-hot 分别适合哪类变量吗？",
)

def title(text: str) -> None:
    """打印章节标题。"""

    print(f"\n{'=' * 15} {text} {'=' * 15}")


def learning_guide() -> None:
    """打印以审计为核心的数据清洗学习路线。"""

    title("学习导航")
    print("本章完成后，你应该能够：")
    # enumerate(..., start=1) 同时产生从 1 开始的编号和每条目标文字。
    for number, objective in enumerate(LEARNING_OBJECTIVES, start=1):
        print(f"  {number}. {objective}")
    print("\n清洗原则：先保留原始数据，再诊断原因；每一步记录规则，并比较清洗前后质量。")
    print("\n教材学习单元：")
    for label in OUTLINE_LABELS:
        print(f"  - {label}")
    print("命令行运行组：", "、".join(SECTION_LABELS))
    print(f"示例：python {SCRIPT_NAME} --section 7.3")


def final_self_check() -> None:
    """打印章末数据质量检查。"""

    title("学习成果自检")
    for question in SELF_CHECKS:
        print(f"  [ ] {question}")
    print("下一步：为自己的数据生成清洗前后行数、缺失率、重复数和异常数对照表。")


def make_messy_data() -> pd.DataFrame:
    """创建包含缺失、重复、异常和脏字符串的教学数据。"""

    # 每个 pd.Series(data, dtype=...) 都先锁定一列的数据类型：
    # - dtype="str" 是 Pandas 可空字符串类型，None 会显示为缺失值 NaN/NA；
    # - dtype="Int64"（大写 I）是可空整数，可同时保存整数和 pd.NA；
    # - dtype="Float64"（大写 F）是 Pandas 可空浮点类型。
    # A002 整行重复；商品名称含多余空格；数量 -3、500 是待审计异常；多列故意含缺失值。
    return pd.DataFrame(
        {
            "订单号": pd.Series(["A001", "A002", "A002", "A003", "A004", "A005"], dtype="str"),
            "商品名称": pd.Series(
                [" Python 入门 ", "Pandas指南", "Pandas指南", "C++实战", None, "NumPy 入门"],
                dtype="str",
            ),
            "数量": pd.Series([2, 1, 1, -3, pd.NA, 500], dtype="Int64"),
            "单价": pd.Series([79.0, 88.0, 88.0, 99.0, 65.0, pd.NA], dtype="Float64"),
            "城市": pd.Series(["北京", "上海", "上海", "广州", None, "北京"], dtype="str"),
        }
    )


def section_71_missing_values() -> None:
    """7.1 查看、删除和填充缺失值。"""

    title("7.1 缺失值")
    # [7.1.1] 了解数据中的缺失值
    df = make_messy_data()
    print("原始数据：\n", df, sep="")

    # info() 输出行数、各列非空数量、dtype 和大致内存占用，适合作为清洗前第一张“体检表”。
    # 它直接把报告写到终端并返回 None，所以不要写 print(df.info())，否则末尾会多打印一个 None。
    print("\n数据概况：")
    df.info()

    # [7.1.2] 查看缺失值
    # isna() 与 isnull() 含义相同：逐单元格返回 True/False DataFrame；
    # 后接 sum() 默认 axis=0，沿行方向汇总，因此得到“每一列”的缺失个数。
    print("\n每列缺失数量：\n", df.isna().sum(), sep="")

    # notna()/notnull() 与 isna()/isnull() 相反：非缺失为 True。
    # df.loc[布尔条件] 只保留“数量”不缺失的整行，而不是只返回数量列。
    print("数量列非缺失记录：\n", df.loc[df["数量"].notna()], sep="")

    # mean() 对布尔值求平均：True 当 1、False 当 0，因此得到 0～1 的缺失比例；
    # mul(100) 乘 100 变成百分比；round(1) 保留 1 位小数。方法链按从左到右顺序执行。
    missing_rate = df.isna().mean().mul(100).round(1)
    print("每列缺失百分比：\n", missing_rate.astype("str") + "%", sep="")

    # [7.1.3] 处理缺失值
    # dropna(subset=["商品名称"]) 中 subset 指定判定列：只在商品名称缺失时删除该行，
    # 数量、单价或城市缺失不会触发这次删除。方法返回新表，原 df 不变。
    complete_products = df.dropna(subset=["商品名称"])
    print("删除商品名称缺失的行：\n", complete_products, sep="")

    # concat([df, 新行], ignore_index=True) 沿默认 axis=0 追加行，并重建连续索引。
    # 字典推导式为每列构造 pd.NA，得到一条“整行为空”的记录。
    # dropna(how="all") 仅当一行所有列都缺失时删除；how="any" 则任一列缺失就删，通常更激进。
    with_empty_row = pd.concat([df, pd.DataFrame([{column: pd.NA for column in df.columns}])], ignore_index=True)
    without_empty_row = with_empty_row.dropna(how="all")
    print("dropna(how='all') 删除的行数：", len(with_empty_row) - len(without_empty_row))

    # 数量缺失是否应填 0 必须由业务定义决定。
    # 若“缺失”确实代表“没有购买”，才适合填 0；否则可能应保留未知或进行估算。
    filled = df.copy()
    filled["数量"] = filled["数量"].fillna(0)

    # mode() 返回所有并列众数的 Series，可能不止一个；iloc[0] 取第一个。
    # fillna(city_mode) 只替换缺失位置，已有城市不会改变。众数填充会增加主流类别占比，需记录决策。
    city_mode = filled["城市"].mode().iloc[0]
    filled["城市"] = filled["城市"].fillna(city_mode)

    # median() 忽略缺失值求中位数，通常比均值更不受极端值影响；
    # fillna(计算结果) 用这个单一标量填所有单价缺失位置，但不代表它适合所有业务场景。
    filled["单价"] = filled["单价"].fillna(filled["单价"].median())
    print("按不同策略填充：\n", filled, sep="")

    # 对有可靠先后顺序的数据，ffill() 用前一个有效值向后填，bfill() 用后一个有效值向前填。
    # 它们不会跨 DataFrame 自动理解“用户/设备”分组，真实面板数据通常应先 groupby 再填充。
    sequence = pd.Series([10, pd.NA, pd.NA, 40], dtype="Int64")
    print("向前填充：", sequence.ffill().tolist())
    print("向后填充：", sequence.bfill().tolist())


def section_72_duplicates() -> None:
    """7.2 判断和删除重复数据。"""

    title("7.2 重复值")
    # [7.2] 处理数据中的重复值
    df = make_messy_data()

    # duplicated(subset=None, keep="first") 默认比较全部列，并把第一次出现保留为 False，
    # 后续相同记录标为 True；返回布尔 Series，不会直接删除数据。
    print("整行是否重复：", df.duplicated().tolist())

    # subset=["订单号"] 把业务主键作为重复依据；其他列即使不同，只要订单号相同也会判为重复。
    print("订单号是否重复：", df.duplicated(subset=["订单号"]).tolist())

    # drop_duplicates(subset, keep, ignore_index)：subset 指定业务键；keep="last" 保留最后一条；
    # ignore_index=True 丢弃原索引并生成连续索引。keep="first" 保留首条，keep=False 一条也不留。
    deduplicated = df.drop_duplicates(subset=["订单号"], keep="last", ignore_index=True)
    print("按订单号去重并保留最后一条：\n", deduplicated, sep="")

    # keep=False 不保留任何重复订单号；A002 的两条记录都会被删除。
    no_repeated_keys = df.drop_duplicates(subset=["订单号"], keep=False, ignore_index=True)
    print("完全移除所有重复订单号：\n", no_repeated_keys, sep="")

    # 去重前应先确定“重复”的业务含义。相同用户多次下单不一定是脏数据。


def section_73_outliers() -> None:
    """7.3 用业务范围和 IQR 检测异常值。"""

    title("7.3 异常值")
    # [7.3] 数据中异常值的检测与处理

    # name="销量" 为 Series 命名；dtype="Float64" 允许后续真实数据出现缺失并进行浮点边界计算。
    quantities = pd.Series([10, 12, 11, 13, 500, 12], name="销量", dtype="Float64")

    # 方法一：业务规则。between(left=0, right=100) 默认包含两个边界，返回“是否合法”的布尔值；
    # 前面的 ~ 对布尔值取反，因而筛出小于 0 或大于 100 的异常值。
    domain_outliers = quantities[~quantities.between(0, 100)]
    # ~ 是布尔取反运算符：合法 True 变成 False，从而筛出不合法值。
    print("超出业务范围：\n", domain_outliers, sep="")

    # 方法二：IQR（四分位距）规则。quantile(0.25/0.75) 分别求第 1、3 四分位数；
    # IQR=Q3-Q1，再把低于 Q1-1.5×IQR 或高于 Q3+1.5×IQR 的值标记为候选异常。
    # 1.5 是常用经验系数，不是自然定律；小样本、分组数据应结合业务判断。
    q1 = quantities.quantile(0.25)
    q3 = quantities.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    iqr_mask = ~quantities.between(lower_bound, upper_bound)
    print(f"IQR 下界={lower_bound:.2f}，上界={upper_bound:.2f}")
    print("IQR 检测结果：\n", quantities[iqr_mask], sep="")

    # 方法三：教材的均值/标准差规则。接近正态分布时，常把均值 ± 3 个标准差外标记为异常。
    # 但极端值本身会拉高均值和标准差，偏态分布也不适合机械使用该规则。
    sigma_values = pd.Series([10, 11, 12, 10, 11, 12, 13, 9, 10, 11, 12, 10, 11, 12, 100])
    mean = sigma_values.mean()
    # std(ddof=0) 把现有数据视为完整总体，分母使用 n；若视为总体样本，常用 ddof=1，分母为 n-1。
    standard_deviation = sigma_values.std(ddof=0)
    z_score = (sigma_values - mean) / standard_deviation
    three_sigma_mask = z_score.abs() > 3
    print("每个值的 z-score：", z_score.round(2).tolist())
    print("3σ 检出的异常：", sigma_values[three_sigma_mask].tolist())

    # 异常不等于错误。处理前应回查来源；可选择标记、截尾、单独分析或删除。
    result = pd.DataFrame({"销量": quantities, "是否异常": iqr_mask})

    # clip(lower=..., upper=...) 把低于下界的值抬到 lower、高于上界的值压到 upper，
    # 区间内数据不变。这是截尾/Winsorize 风格处理，会改变原始数值，应保留原列和异常标记供审计。
    result["截尾后销量"] = quantities.clip(lower=lower_bound, upper=upper_bound)
    print("保留异常标记并演示截尾：\n", result, sep="")


def section_74_strings() -> None:
    """7.4 使用 Series.str 清洗字符串。"""

    title("7.4 字符串清洗")

    # [7.4.1] 字符串对象中的常见函数
    text = pd.Series([" Python ", "PANDAS", None, " NumPy入门 "], dtype="str")

    # .str 是 Pandas 的向量化字符串访问器：strip() 去两端空白，lower() 转小写；
    # 方法逐元素执行并保留缺失值，不需要手写 for 循环。连续点号调用称为方法链。
    cleaned = text.str.strip().str.lower()
    print("去除两端空格并转小写：\n", cleaned, sep="")

    # upper 转大写，len 计算字符数，lstrip/rstrip 分别只去左/右两端空白。
    print("转大写：", text.str.upper().tolist())
    print("原始字符串长度：", text.str.len().tolist())
    print("只去左侧空格：", text.str.lstrip().tolist())
    print("只去右侧空格：", text.str.rstrip().tolist())

    # [7.4.2] 替换字符串—replace()函数
    housing = pd.DataFrame(
        {
            "总价": pd.Series(["120万", "95万"], dtype="str"),
            "建筑面积": pd.Series(["80平米", "65平米"], dtype="str"),
        }
    )

    # str.replace(pat, repl, regex=False)：pat 是待查文字，repl="" 是替换为空字符串，
    # regex=False 表示按字面文本处理，不把 +、.、| 等字符解释成正则语法。
    # 去掉单位后仍是字符串，astype("float64") 再转换为可计算数值；无法解析的脏文本会报错。
    housing["总价"] = housing["总价"].str.replace("万", "", regex=False).astype("float64")
    housing["建筑面积"] = (
        housing["建筑面积"].str.replace("平米", "", regex=False).astype("float64")
    )
    print("去单位并转为数值：\n", housing, sep="")

    # Index 也提供 .str。下面清除列标题两侧空格，并把内部空格换成下划线。
    # columns 故意含首尾/内部空格；Index.str.replace 的 regex=False 同样表示按普通空格替换。
    messy_columns = pd.DataFrame([[1, 2]], columns=[" 总价 ", "建筑 面积"])
    messy_columns.columns = messy_columns.columns.str.strip().str.replace(" ", "_", regex=False)
    print("清洗后的列标题：", messy_columns.columns.tolist())

    # [7.4.3] 数据切分—split()函数
    # name 是整列名称，dtype="str" 启用可空字符串操作；两个地址使用相同竖线结构。
    addresses = pd.Series(
        ["广东省|深圳市|南山区", "浙江省|杭州市|西湖区"], name="收货地址", dtype="str"
    )

    # str.split(pat="|", expand=True)：pat 是分隔文字；expand=True 把每段展开为 DataFrame 多列，
    # 若为 False，结果会是“每格一个列表”的 Series。随后列名列表长度必须与拆出的列数一致。
    address_parts = addresses.str.split("|", expand=True)
    address_parts.columns = ["省", "市", "区"]
    print("地址切分：\n", address_parts, sep="")

    # [7.4.4] 判断字符串—contains()函数
    books = pd.Series(["Python入门", "C++实战", None, "Java核心"], dtype="str")

    # str.contains(pat, regex=False, na=False) 返回布尔 Series：pat="C++" 是查询文字；
    # regex=False 按字面匹配，避免 C++ 中 + 被当正则量词；na=False 把缺失位置当“不匹配”，
    # 这样布尔结果可直接用于 books[has_cpp]，不会因 NA 布尔值无法筛选而报错。
    has_cpp = books.str.contains("C++", regex=False, na=False)
    print("包含 C++ 的书：", books[has_cpp].tolist())

    # np.select(conditions, choices, default)：conditions 是等长布尔数组列表；choices 与其逐项对应；
    # 同一行若命中多个条件，只采用第一个 True 对应的类别；全部不命中或名称缺失时使用 default="其他"。
    products = pd.DataFrame(
        {"商品名称": pd.Series(["Python数据分析", "Java核心", "C++实战", None], dtype="str")}
    )
    # 三次 contains 都使用 regex=False 和 na=False，含义与上例一致：字面匹配且缺失视为不匹配。
    conditions = [
        products["商品名称"].str.contains("Python", regex=False, na=False),
        products["商品名称"].str.contains("Java", regex=False, na=False),
        products["商品名称"].str.contains("C++", regex=False, na=False),
    ]
    products["类别"] = np.select(conditions, ["Python", "Java", "C++"], default="其他")
    print("contains 分类：\n", products, sep="")


def section_75_transform() -> None:
    """7.5 map、cut、类别类型与 one-hot 编码。"""

    title("7.5 数据转换")

    # [7.5.1] 通过字典映射—map()函数
    people = pd.DataFrame(
        {
            "性别": pd.Series(["男", "女", "女", "未知"], dtype="str"),
            "年龄": [18, 25, 42, 70],
        }
    )

    # Series.map(mapping) 逐值查字典："男"→1、"女"→2；字典没有“未知”，结果自动变缺失。
    # astype("Int64") 使用可空整数，既保存 1/2 整数又允许未知值为 NA。无序类别的数字编码不代表大小。
    mapping = {"男": 1, "女": 2}
    people["性别编码"] = people["性别"].map(mapping).astype("Int64")
    print("字典映射：\n", people, sep="")

    # [7.5.2] 数据分割—cut()函数
    scores = pd.Series([59, 60, 69, 70, 100], name="得分")

    # cut(x, bins, labels, right, include_lowest) 把连续数值分箱：
    # - x=scores 是待分箱数据；bins 的 4 个边界产生 3 个区间，labels 必须恰有 3 个；
    # - right=False 创建左闭右开区间 [0,60)、[60,70)、[70,101)；
    # - include_lowest=True 保证最小边界 0 被纳入。这里 59=一般、60=良好、70/100=优秀；
    # 超出所有边界的值会变成缺失类别，所以最高边界写 101 才能在右开区间中包含 100。
    levels = pd.cut(
        scores,
        bins=[0, 60, 70, 101],
        labels=["一般", "良好", "优秀"],
        right=False,
        include_lowest=True,
    )
    print("成绩分箱：\n", pd.DataFrame({"得分": scores, "等级": levels}), sep="")

    # [7.5.3] 数据分类—get_dummies()函数
    products = pd.DataFrame(
        {
            "颜色": pd.Series(["黑色", "浅灰", "粉色", "浅灰"], dtype="str"),
            "尺码": pd.Series(["M", "S", "L", "XS"], dtype="str"),
        }
    )

    # CategoricalDtype(categories, ordered=True) 定义有序类别：categories 给出完整合法值及顺序，
    # ordered=True 允许 XS<S<M<L<XL 的排序比较；输入若有不在 categories 中的值会转为缺失。
    size_type = pd.CategoricalDtype(categories=["XS", "S", "M", "L", "XL"], ordered=True)
    products["尺码"] = products["尺码"].astype(size_type)

    # get_dummies(data, columns, dtype) 做 one-hot：columns=["颜色"] 只展开颜色列，尺码保留；
    # 每种颜色生成一个 0/1 指示列；dtype="int8" 用 8 位整数减少内存。one-hot 不人为制造类别大小关系。
    encoded = pd.get_dummies(products, columns=["颜色"], dtype="int8")
    print("颜色 one-hot 编码：\n", encoded, sep="")


def exercises() -> None:
    """第7章练习及自动检查。"""

    title("第7章练习")
    df = make_messy_data()

    # 练习 1：统计全表缺失值总数。
    answer_1 = int(df.isna().sum().sum())

    # 练习 2：按订单号去重，保留第一条。
    # 第 1 个位置参数等价于 subset="订单号"；keep="first" 保留每个订单号首次出现记录。
    answer_2 = df.drop_duplicates("订单号", keep="first")

    # 练习 3：清理商品名称两端空格，并筛选含 Python 的商品。
    cleaned_names = df["商品名称"].str.strip()
    # regex=False 做字面查找；na=False 让缺失名称生成 False，从而可直接用于布尔筛选。
    answer_3 = cleaned_names[cleaned_names.str.contains("Python", regex=False, na=False)]

    # 四个缺失值分别位于：商品名称、数量、单价、城市。
    assert answer_1 == 4
    assert len(answer_2) == 5
    assert answer_3.tolist() == ["Python 入门"]
    print("第7章练习全部通过！")


def main() -> None:
    """运行整章或指定的数据清洗单元。"""

    # description 会出现在 --help 中；以下 add_argument 定义开关、小节合法值和默认行为。
    parser = argparse.ArgumentParser(description="第7章 Pandas 数据清洗分节学习脚本")
    # store_true 把开关转为布尔值；choices 防止拼错小节；default="all" 默认运行整章。
    parser.add_argument("--list", action="store_true", help="只显示学习导航")
    parser.add_argument("--section", choices=("all", *SECTION_LABELS), default="all")
    parser.add_argument("--skip-exercises", action="store_true", help="整章运行时暂不执行练习")
    args = parser.parse_args()

    print("Pandas 版本：", pd.__version__)
    learning_guide()
    if args.list:
        return

    section_runners = {
        "7.1": section_71_missing_values,
        "7.2": section_72_duplicates,
        "7.3": section_73_outliers,
        "7.4": section_74_strings,
        "7.5": section_75_transform,
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
