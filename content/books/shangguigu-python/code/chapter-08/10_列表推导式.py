# 列表推导式：用一条简洁语句，从可迭代对象中，生成新列表的语法结构。
# 备注：列表推导式本质上是对 for循环 + append() 的一种简写形式。
# 语法格式：[表达式 for 变量 in 可迭代对象]

# 需求：让列表中每个元素，都变为原来的2倍，得到是一个新的列表

# 方式一：用map函数
# nums = [10, 20, 30, 40]
# result = list(map(lambda n: n * 2, nums))
# print(result)

# 方式二：用 for循环 + append()
# nums = [10, 20, 30, 40]
# result = []
# for n in nums:
#     result.append(n * 2)
# print(result)

# 方式三：用列表推导式
# nums = [10, 20, 30, 40]
# result = [n * 2 for n in nums]
# print(result)

# 带条件的列表推导式
# nums = [10, 20, 30, 40]
# result = [n * 2 for n in nums if n > 20]
# print(result)

# 字典推导式
# names = ['张三', '李四', '王五']
# scores = [60, 70, 80]
# result = {names[i]: scores[i] for i in range(len(names))}
# print(result)

# 集合推导式
# names = ['张三', '李四', '王五']
# result = {n + '！' for n in names}
# print(result)

names = ['张三', '李四', '王五']
# Python中没有元组推导式，下面这种写法叫：生成器（后面会仔细讲）
result = (n + '！' for n in names)
print(result)
