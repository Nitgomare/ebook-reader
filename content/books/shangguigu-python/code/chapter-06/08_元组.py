# 定义元组
# t1 = (28, 67, 21, 67, 11)
# t2 = ('北京', '尚硅谷', '你好')
# t3 = (100, True, '你好', None)
# t4 = (100, True, '你好', None, (50, 60, 70))
# print(type(t1), t1)
# print(type(t2), t2)
# print(type(t3), t3)
# print(type(t4), t4)

# 元组的下标
# t1 = (28, 67, 21, 67, 11)
# print(t1[3])
# print(t1[-1])

# 元组中的元素，不可修改
# t1 = (28, 67, 21, 67, 11)
# t1[0] = 100

# 元组中的元素，不可修改，但元组中如果存放了可变类型（列表），那可变类型中的内容仍可修改
# t2 = (28, 67, 21, 67, 11, [100, 200, 300, ('你好', '尚硅谷')])
# # t2[5] = 400
# t2[5][2] = 400
# t2[5][3][0] = 'hello'
# print(t2)

# 定义空元组
# t1 = ()
# t2 = tuple()
# print(type(t1), t1)
# print(type(t2), t2)

# 定义只有一个元素的元组
# t1 = ('你好',)
# t2 = (18,)
# print(type(t1), t1)
# print(type(t2), t2)

# 常用方法：
# index 方法：获取指定元素在元组中第一次出现的下标。
# t1 = (28, 67, 21, 67, 11)
# result = t1.index(67)
# print(result)

# count 方法：统计指定元素在元组中出现的次数。
# t1 = (28, 67, 21, 67, 11)
# result = t1.count(67)
# print(result)

# 常用内置函数
# max 函数，返回元组中的最大值
# t1 = (23, 11, 32, 30, 17)
# result = max(t1)
# print(result)

# min 函数，返回元组中的最小值
# t1 = (23, 11, 32, 30, 17)
# result = min(t1)
# print(result)

# len 函数，返回元组中元素的个数（元组长度）
# t1 = (23, 11, 32, 30, 17)
# result = len(t1)
# print(result)

# sorted 函数，对元组进行排序（不修改原元组，返回一个新的列表）
# t1 = (23, 11, 32, 30, 17)
# result = sorted(t1, reverse=True)
# print(tuple(result))

# sum 函数，统计元组中所有元素的和（元素必须是纯数字）
# t1 = (23, 11, 32, 30, 17)
# result = sum(t1)
# print(result)

# 实际开发中的元组，不一定是我们自己定义的，比如函数的可变参数*args就是一个元组
# def demo(*args):
#     return sum(args)
# result = demo(100, 200, 300)
# print(result)

# 元组的循环遍历
t1 = (23, 11, 32, 30, 17)

# while循环遍历
# index = 0
# while index < len(t1):
#     print(t1[index])
#     index += 1

# for循环遍历
for item in t1:
    print(item)
