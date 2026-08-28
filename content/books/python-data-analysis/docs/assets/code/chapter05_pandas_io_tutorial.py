"""第5章：Pandas 数据读取与写入（Pandas 3.x，纯新手注释版）。

对应原书 5.1～5.5：文本、CSV、Excel、HTML 和数据库。
教材覆盖地图：5.1 文本；5.2.1～5.2.4 Excel 读取、Sheet、行列和写入；
5.3.1～5.3.2 CSV 读取与写入；5.4 HTML；5.5.1 MySQL；5.5.2 MongoDB。
为保证示例离线也能重复运行，本脚本会在项目中自动创建 chapter05_demo_data
文件夹以及少量教学数据，不会依赖书中未附带的外部数据文件或已失效网页。
"""

# argparse 用于选择只运行某一种文件格式，避免初学者一次面对过多输出。
import argparse

# sqlite3 是 Python 标准库，用来演示关系型数据库，不需要另外安装 MySQL。
import sqlite3

# StringIO 把字符串包装成“像文件一样的对象”，供 read_html 读取。
from io import StringIO

# Path 是现代 Python 推荐的路径工具，比手写 Windows 反斜杠更安全、清晰。
from pathlib import Path

import pandas as pd


SCRIPT_NAME = "chapter05_pandas_io_tutorial.py"
LEARNING_OBJECTIVES = (
    "根据分隔符、编码、工作表和数据源类型选择正确的读写函数",
    "在读取时明确日期、缺失值和标识符的数据类型，避免静默误判",
    "把 CSV、Excel、HTML 与 SQL 读取结果统一为可检查的 DataFrame",
    "安全处理数据库连接信息，并在写出后验证行数、列名和关键字段",
)
SECTION_LABELS = ("5.1", "5.2", "5.3", "5.4", "5.5", "exercises")
OUTLINE_LABELS = (
    "5.1 读取文本文件中的数据", "5.2.1 读取Excel文件中的数据",
    "5.2.2 读取指定Sheet页中的数据", "5.2.3 通过行列索引读取指定数据",
    "5.2.4 将数据写入Excel文件中", "5.3.1 读取CSV文件中的数据",
    "5.3.2 将数据写入CSV文件中", "5.4 读取HTML网页",
    "5.5.1 读取MySQL数据库中的数据", "5.5.2 读取MongoDB数据库中的数据",
)
SELF_CHECKS = (
    "能说明订单号为什么通常应读成字符串而不是整数吗？",
    "遇到中文乱码时，能从文件编码而不是显示设置入手排查吗？",
    "能在读取后检查 shape、columns、dtypes 和缺失值数量吗？",
    "能解释为什么数据库密码不应直接写进 Python 文件吗？",
)


# __file__ 是当前脚本文件的路径；resolve() 得到绝对路径；parent 得到所在文件夹。
PROJECT_DIR = Path(__file__).resolve().parent

# / 在 Path 对象之间表示拼接路径，不是数学除法。
DATA_DIR = PROJECT_DIR / "chapter05_demo_data"


def title(text: str) -> None:
    """打印章节标题。"""

    print(f"\n{'=' * 15} {text} {'=' * 15}")


def learning_guide() -> None:
    """打印本章目标和可靠的数据读取工作流。"""

    title("学习导航")
    print("本章完成后，你应该能够：")
    # enumerate(..., start=1) 让目标编号从 1 开始，并在每轮同时得到编号和文字。
    for number, objective in enumerate(LEARNING_OBJECTIVES, start=1):
        print(f"  {number}. {objective}")
    print("\n可靠读取四步：确认来源 → 明确参数 → 检查结构与类型 → 写出后重新读回验证。")
    print("\n教材学习单元：")
    for label in OUTLINE_LABELS:
        print(f"  - {label}")
    print("命令行运行组：", "、".join(SECTION_LABELS))
    print(f"示例：python {SCRIPT_NAME} --section 5.3")


def final_self_check() -> None:
    """打印章末数据导入质量检查。"""

    title("学习成果自检")
    for question in SELF_CHECKS:
        print(f"  [ ] {question}")
    print("下一步：选择自己的一个 CSV 或 Excel，写下数据字典后再读入。")


def make_source_data() -> pd.DataFrame:
    """创建本章所有文件格式共用的订单数据。"""

    # 订单号看起来像数字，但不会参与数学运算，应明确保存为字符串。
    # 每个 pd.Series 的 dtype 逐列锁定类型：str 是可空字符串；Int64 是可空整数；
    # Float64 是可空浮点。pd.NA 表示缺失值；大写扩展类型可避免有缺失时被迫转成普通 object。
    return pd.DataFrame(
        {
            "订单号": pd.Series(["A001", "A002", "A003", "A004"], dtype="str"),
            "商品": pd.Series(["Python入门", "NumPy实战", "Pandas指南", "数据可视化"], dtype="str"),
            "数量": pd.Series([2, 1, 3, 2], dtype="Int64"),
            "实付金额": pd.Series([158.0, 89.5, pd.NA, 126.0], dtype="Float64"),
            "付款时间": pd.to_datetime(["2026-08-01", "2026-08-02", "2026-08-02", "2026-08-03"]),
        }
    )


def prepare_demo_files() -> dict[str, Path]:
    """写出 CSV、TSV、Excel 和 HTML，并返回它们的路径字典。"""

    # mkdir 创建文件夹。parents=True 允许创建缺失的上级文件夹；
    # exist_ok=True 表示文件夹已存在也不报错。
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    orders = make_source_data()

    csv_path = DATA_DIR / "orders.csv"
    tsv_path = DATA_DIR / "orders.tsv"
    excel_path = DATA_DIR / "orders.xlsx"
    html_path = DATA_DIR / "orders.html"

    # to_csv(path, ...) 把 DataFrame 写为分隔文本：
    # - path 是目标路径；index=False 不把 0、1、2 的行索引写成额外一列；
    # - encoding="utf-8-sig" 在 UTF-8 开头增加 BOM，很多 Windows Excel 可据此识别中文；
    # - na_rep="缺失" 指定缺失值在文件中的文字，否则通常写成空字段。
    orders.to_csv(csv_path, index=False, encoding="utf-8-sig", na_rep="缺失")

    # sep="\t" 把列分隔符改为制表符，因此得到 TSV；encoding="utf-8" 不写 BOM；
    # na_rep="NA" 与稍后的 na_values=["NA"] 配套，实现“写出 NA、读回缺失值”。
    orders.to_csv(tsv_path, index=False, sep="\t", encoding="utf-8", na_rep="NA")

    # ExcelWriter(path, engine="openpyxl") 管理一个可写入多个 Sheet 的工作簿：
    # engine 指定 .xlsx 的读写引擎；with 是上下文管理器，代码块结束时自动保存并关闭文件。
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        # 第 1 个参数 writer 指定写入哪个工作簿；sheet_name 指定页签名称；index=False 不写行索引。
        orders.to_excel(writer, sheet_name="订单", index=False)
        # groupby("商品", as_index=False) 按商品分组；as_index=False 让商品仍是普通列，
        # ["数量"].sum() 只对数量列求和，得到每种商品的数量汇总。
        summary = orders.groupby("商品", as_index=False)["数量"].sum()
        summary.to_excel(writer, sheet_name="商品汇总", index=False)

    # to_html 把表格写成含 <table> 标签的网页；encoding 指定文件编码。
    orders.to_html(html_path, index=False, encoding="utf-8")

    # dict[str, Path] 表示“键是字符串、值是 Path”的字典类型。
    return {
        "csv": csv_path,
        "tsv": tsv_path,
        "excel": excel_path,
        "html": html_path,
    }


def section_51_text(paths: dict[str, Path]) -> None:
    """5.1 读取带分隔符的文本文件。"""

    title("5.1 文本文件")
    # [5.1] 读取文本文件中的数据

    # read_table(filepath, encoding, na_values) 读取表格文本：
    # - filepath=paths["tsv"] 是文件路径；read_table 默认 sep="\t"；
    # - encoding="utf-8" 必须与写出编码一致；na_values=["NA"] 把文本 NA 转成真正缺失值 NaN/NA。
    table = pd.read_table(paths["tsv"], encoding="utf-8", na_values=["NA"])
    print("读取 TSV：\n", table, sep="")

    # sep 可以指定任意分隔符。真实日志若用多个空白，可考虑 sep=r"\s+"。
    # r 前缀创建原始字符串，使反斜杠不被 Python 当作转义符处理。
    print("行列数：", table.shape)

    # read_csv 不只读取 .csv；sep="\t" 明确告诉解析器按制表符拆列。
    # encoding 和 na_values 与上面相同，因此两个读取结果应完全一致；assert_frame_equal 负责验证。
    same_table = pd.read_csv(paths["tsv"], sep="\t", encoding="utf-8", na_values=["NA"])
    pd.testing.assert_frame_equal(table, same_table)
    print("read_table 与 read_csv(sep='\\t') 结果一致")

    # 同时含空格和制表符时，可用正则 sep=r"\s+" 匹配一个或多个空白字符。
    # engine="python" 选择支持正则分隔符的 Python 解析引擎；它通常比默认 C 引擎慢，但语法更灵活。
    irregular_text = "姓名  语文\t数学\n甲  110\t105\n乙  105\t88"
    irregular = pd.read_csv(StringIO(irregular_text), sep=r"\s+", engine="python")
    print("正则分隔符读取：\n", irregular, sep="")


def section_52_excel(paths: dict[str, Path]) -> None:
    """5.2 Excel 文件读取与写入。"""

    title("5.2 Excel")

    # [5.2.1] 读取Excel文件中的数据
    # read_excel(io, ...) 中 io 是工作簿路径，其余参数控制“读哪一页、哪些列、用什么类型”：
    # - sheet_name="订单" 只读名为“订单”的 Sheet，也可用整数 0 表示第 1 页；
    # - usecols=[...] 只加载列名列表中的 4 列，可减少大文件的内存和读取时间；
    # - parse_dates=["付款时间"] 把该列解析为 datetime，而不是普通字符串；
    # - dtype={"订单号": "str"} 防止标识符被误判为数字而丢失前导零；
    # - engine="openpyxl" 明确使用 .xlsx 引擎，运行前需安装 openpyxl。
    orders = pd.read_excel(
        paths["excel"],
        sheet_name="订单",
        usecols=["订单号", "商品", "实付金额", "付款时间"],
        parse_dates=["付款时间"],
        dtype={"订单号": "str"},
        engine="openpyxl",
    )
    print("指定工作表和列：\n", orders, sep="")

    # [5.2.2] 读取指定Sheet页中的数据
    # sheet_name=None 表示读取全部 Sheet，返回 dict[str, DataFrame]；
    # 键是页签名，值是对应 DataFrame。注意这可能一次占用较多内存，大文件宜按需读取。
    all_sheets = pd.read_excel(paths["excel"], sheet_name=None, engine="openpyxl")
    print("全部工作表名称：", list(all_sheets))
    print("商品汇总页：\n", all_sheets["商品汇总"], sep="")

    # [5.2.3] 通过行列索引读取指定数据
    # index_col="订单号" 指定读入后把该列作为行索引；它不再作为普通数据列显示。
    # 按列名比写 index_col=0 更能表达意图，也不怕源文件调整列顺序。
    indexed_orders = pd.read_excel(
        paths["excel"], sheet_name="订单", index_col="订单号", engine="openpyxl"
    )
    print("订单号作为索引：\n", indexed_orders.head(), sep="")

    # header=None 表示“文件没有列名行”，所以原文件第 1 行“订单号、商品……”也会当普通数据；
    # nrows=3 限制只读取最前面 3 行，适合低成本预览。真实无表头文件可再用 names=[...] 指定列名。
    no_header_demo = pd.read_excel(paths["excel"], sheet_name="订单", header=None, nrows=3)
    print("header=None 后前 3 行：\n", no_header_demo, sep="")

    # Path 既可表示相对路径也可表示绝对路径；resolve() 显示完整绝对路径。
    print("Excel 绝对路径：", paths["excel"].resolve())

    # .xlsx 通常使用 openpyxl；老式 .xls 通常需要 xlrd。
    # 教材提到的 xlwt 面向老式 .xls 写入，现代项目通常优先采用 .xlsx。

    # [5.2.4] 将数据写入Excel文件中
    # to_excel(path, ...) 写出工作簿：sheet_name 是目标页签；index=False 不写行索引；
    # float_format="%.2f" 将浮点数显示为两位小数（影响写出格式）；
    # freeze_panes=(1, 0) 冻结第 1 行上方/左侧区域，即滚动时保留标题行；元组是“行数, 列数”。
    output_path = DATA_DIR / "selected_orders.xlsx"
    orders.to_excel(
        output_path,
        sheet_name="筛选结果",
        index=False,
        float_format="%.2f",
        freeze_panes=(1, 0),
    )
    print("已写出：", output_path.name)


def section_53_csv(paths: dict[str, Path]) -> None:
    """5.3 CSV 文件读取、类型控制、分块和写入。"""

    title("5.3 CSV")

    # [5.3.1] 读取CSV文件中的数据
    # read_csv(filepath, ...) 是最常用的数据读取函数：
    # - encoding="utf-8-sig" 与写出文件编码对应；
    # - na_values=["缺失"] 把指定文字识别成缺失值，而不是普通字符串；
    # - parse_dates 指定日期列；dtype 字典逐列锁定类型，特别保护订单号和可空整数数量。
    orders = pd.read_csv(
        paths["csv"],
        encoding="utf-8-sig",
        na_values=["缺失"],
        parse_dates=["付款时间"],
        dtype={"订单号": "str", "商品": "str", "数量": "Int64"},
    )
    print(orders)
    print("各列类型：\n", orders.dtypes, sep="")

    # usecols 只读取指定列；nrows=2 只读前 2 条数据记录（不含表头），适合先侦察大文件结构。
    preview = pd.read_csv(paths["csv"], usecols=["订单号", "商品"], nrows=2)
    print("只读两列、两行：\n", preview, sep="")

    # chunksize=2 不立即返回 DataFrame，而返回 TextFileReader 迭代器；每轮产生最多 2 行，
    # 适合内存放不下的大文件。enumerate(..., start=1) 让块编号从 1 而非 0 开始。
    chunk_reader = pd.read_csv(paths["csv"], chunksize=2)
    for number, chunk in enumerate(chunk_reader, start=1):
        print(f"第 {number} 块有 {len(chunk)} 行")

    # [5.3.2] 将数据写入CSV文件中
    output_path = DATA_DIR / "orders_clean.csv"
    orders.to_csv(output_path, index=False, encoding="utf-8-sig", float_format="%.2f")
    print("已写出：", output_path.name)

    # to_csv 的写出参数逐项说明：sep="?" 用问号分列；na_rep="NA" 写出缺失值；
    # float_format="%.2f" 写两位小数；columns 只输出列名列表中的列且保持该顺序；
    # header=True 写列名；index=False 不写行索引；encoding="utf-8" 决定字节编码。
    custom_path = DATA_DIR / "orders_custom.txt"
    orders.to_csv(
        custom_path,
        sep="?",
        na_rep="NA",
        float_format="%.2f",
        columns=["订单号", "商品", "实付金额"],
        header=True,
        index=False,
        encoding="utf-8",
    )
    # 读回时 sep 必须与写出相同，na_values=["NA"] 将写出的缺失标记还原为真正缺失值。
    custom = pd.read_csv(custom_path, sep="?", na_values=["NA"])
    print("自定义问号分隔文件：\n", custom, sep="")


def section_54_html(paths: dict[str, Path]) -> None:
    """5.4 读取 HTML 的 table 表格。"""

    title("5.4 HTML 表格")
    # [5.4] 读取HTML网页

    # read_html(io, match, encoding) 解析 HTML 中的 <table>：
    # io 是本地路径或网址；match="商品" 只保留含该文字的表格；encoding="utf-8" 指定解码方式。
    # 一个页面可能有多张表，所以返回 list[DataFrame]，即使只匹配到一张也要用 tables[0] 取出。
    tables = pd.read_html(paths["html"], match="商品", encoding="utf-8")
    print("找到表格数量：", len(tables))
    print("第一个表格：\n", tables[0].head(), sep="")

    # 也可以读取已有 HTML 字符串。Pandas 3 推荐用 StringIO 包装字面 HTML。
    html_text = """
    <table>
      <tr><th>城市</th><th>销量</th></tr>
      <tr><td>北京</td><td>120</td></tr>
      <tr><td>上海</td><td>135</td></tr>
    </table>
    """
    city_table = pd.read_html(StringIO(html_text), match="城市")[0]
    print("字符串中的表格：\n", city_table, sep="")

    # 读取互联网网页时要遵守网站条款与 robots 规则；网页还可能发生变化。
    # 不要照抄书中多年以前的网址作为稳定生产数据源。


def section_55_database() -> None:
    """5.5 使用 SQLite 演示 SQL 数据库读写。"""

    title("5.5 SQL 数据库")
    # [5.5.1] 读取MySQL数据库中的数据

    # ":memory:" 表示创建只存在于内存中的临时 SQLite 数据库。
    connection = sqlite3.connect(":memory:")

    try:
        source = make_source_data()

        # to_sql(name, con, if_exists, index)：name="orders" 是表名，con 是数据库连接；
        # if_exists="replace" 会删除并重建同名表（生产环境须谨慎）；index=False 不写 DataFrame 行索引。
        source.to_sql("orders", connection, if_exists="replace", index=False)

        # read_sql_query(sql, con, params) 执行查询并返回 DataFrame。
        # SQL 中的 ? 是 SQLite 参数占位符；params=(100,) 是单元素元组，把 100 安全绑定进去。
        # 参数化查询可避免引号转义错误和 SQL 注入，不要用 f-string 拼接用户输入。
        query = "SELECT 订单号, 商品, 实付金额 FROM orders WHERE 实付金额 >= ?"
        result = pd.read_sql_query(query, connection, params=(100,))
        print("金额不少于 100 的订单：\n", result, sep="")

        # chunksize=2 使 read_sql_query 返回迭代器，每次最多 2 行；适合结果集很大时逐块处理。
        chunks = pd.read_sql_query("SELECT * FROM orders", connection, chunksize=2)
        print("数据库分块行数：", [len(chunk) for chunk in chunks])
    finally:
        # finally 中的代码无论前面是否出错都会执行，确保数据库连接关闭。
        connection.close()

    title("5.5.1 MySQL 阅读模板")

    # 下方是可阅读但不自动执行的 MySQL 模板。
    # 真正运行前需安装 sqlalchemy 和 pymysql，并在环境变量中提供账号密码。
    # 不要像旧示例那样把 root 密码直接写进源代码。
    mysql_template = '''
import os
import pandas as pd
from sqlalchemy import URL, create_engine, text

url = URL.create(
    "mysql+pymysql",
    username=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    host=os.environ.get("MYSQL_HOST", "localhost"),
    database="test",
)
engine = create_engine(url)
with engine.connect() as connection:
    query = text("SELECT * FROM user WHERE id > :minimum_id")
    mysql_df = pd.read_sql_query(query, connection, params={"minimum_id": 0})
'''
    print(mysql_template)

    # [5.5.2] 读取MongoDB数据库中的数据
    title("5.5.2 MongoDB 阅读模板")

    # MongoDB 不是 SQL 数据库，Pandas 没有 read_mongodb 函数。
    # 通常用 pymongo 查询文档，再用 DataFrame.from_records 转成表格。
    mongodb_template = '''
import os
import pandas as pd
from pymongo import MongoClient

with MongoClient(os.environ["MONGODB_URI"]) as client:
    collection = client["mrbooks"]["books"]
    documents = list(collection.find({}, {"_id": 0}))
    mongo_df = pd.DataFrame.from_records(documents)
'''
    print(mongodb_template)


def exercises(paths: dict[str, Path]) -> None:
    """第5章练习及自动检查。"""

    title("第5章练习")

    # 练习 1：从 CSV 只读取商品和数量两列。
    # usecols 只加载两列；它检查的是“读取列集合”，源 CSV 仍保持完整不变。
    answer_1 = pd.read_csv(paths["csv"], usecols=["商品", "数量"])

    # 练习 2：读取 Excel 的商品汇总页。
    # sheet_name 精确选择商品汇总页，返回单个 DataFrame；若写 None 则返回全部页字典。
    answer_2 = pd.read_excel(paths["excel"], sheet_name="商品汇总")

    # 练习 3：检查 HTML 中读取到的表格数量。
    # 本地 HTML 是 UTF-8 编码；明确写 encoding，避免解析器按系统编码误判中文。
    answer_3 = len(pd.read_html(paths["html"], match="商品", encoding="utf-8"))

    assert answer_1.columns.tolist() == ["商品", "数量"]
    assert answer_2["数量"].sum() == 8
    assert answer_3 == 1
    print("第5章练习全部通过！")


def main() -> None:
    """创建演示数据，并运行整章或指定的数据源单元。"""

    # 命令行参数让一个教学脚本既可跑整章，也可只练单一数据源；description 显示在 --help 中。
    parser = argparse.ArgumentParser(description="第5章 Pandas 数据读写分节学习脚本")
    # store_true 处理无取值开关；choices 拒绝未知小节；default 指定省略 --section 时运行 all。
    parser.add_argument("--list", action="store_true", help="只显示学习导航，不创建演示文件")
    parser.add_argument("--section", choices=("all", *SECTION_LABELS), default="all")
    parser.add_argument("--skip-exercises", action="store_true", help="整章运行时暂不执行练习")
    args = parser.parse_args()

    print("Pandas 版本：", pd.__version__)
    learning_guide()
    if args.list:
        return

    paths = prepare_demo_files()
    print("教学数据目录：", DATA_DIR)
    section_runners = {
        "5.1": lambda: section_51_text(paths),
        "5.2": lambda: section_52_excel(paths),
        "5.3": lambda: section_53_csv(paths),
        "5.4": lambda: section_54_html(paths),
        "5.5": section_55_database,
        "exercises": lambda: exercises(paths),
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
