# 概念：所谓『匿名函数』，就是没有名字的函数，它无需使用 def 关键字去定义。
# 语法：Python 中使用 lambda 关键字来定义『匿名函数』，格式为：lambda 参数: 表达式
# 使用场景： 当一个函数只用一次、只做一点点小事，使用匿名函数会更简洁。

# 使用普通函数实现计算效果
# def add(x, y):
#     return x + y
#
# def sub(x, y):
#     return x - y
#
# def calculate(func, a, b):
#     print(f'计算结果为：{func(a, b)}')
#
# calculate(add, 30, 10)
# calculate(sub, 30, 10)

# 匿名函数
# add1 = lambda x, y: x + y
# add2 = lambda x: x + x
# add3 = lambda: '我是add3函数'
#
# result1 = add1(30, 10)
# result2 = add2(30)
# result3 = add3()
# print(result1, result2, result3)

# 使用匿名函数实现计算效果
# def calculate(func, a, b):
#     print(f'计算结果为：{func(a, b)}')
#
# calculate(lambda x, y: x + y, 30, 10)
# calculate(lambda x, y: x - y, 30, 10)

# 注意点
# 1. 只能写一行，不能写多行代码。
# 2. 不能写代码块（if、for、while）
# 3. 冒号右边必须是表达式，且只能写一个表达式。
# 4. 表达式结果自动作为返回值。

is_adult = lambda age: '成年' if age >= 18 else '未成年'
print(is_adult(18))
print(is_adult(13))
