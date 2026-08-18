# 1.使用内置的 sorted 函数，返回一个排序后的新容器（不改变原容器，默认顺序：从小到大）
# 1.1 若列容器中的元素：都是数字，则按照数字的大小顺序进行排序。
# nums = [23, 11, 32, 30, 17]
# result = sorted(nums, reverse=True)
# print(nums)
# print(result)

# 1.2 若列容器中的元素：既有数字，又有字符串，那就会报错。
# nums = [23, 11, 32, 30, 17, '尚硅谷']
# sorted(nums)

# 1.3 若列容器中的元素：都是字符串，则按照字符串的 Unicode 编码大小进行排序。
# msg_list = ['北京', '尚硅谷', '你好']
# result = sorted(msg_list)
# print(msg_list)
# print(result)

# 2.使用内置的 len 函数，获取容器中元素的总数量，返回值是：元素总数量。
# nums = [10, 20, 10, 30, 10, 40, [50, 60, 70]]
# result = len(nums)
# print(result)


# 3.使用内置的 max 函数，获取容器中的最大值，返回值是：最大值。
# 3.1 如果容器中的元素：都是数字，那 max 返回的是最大的数。
# nums = [23, 11, 32, 30, 17]
# result = max(nums)
# print(nums)
# print(result)

# 3.2 如果容器中的元素：既有数字又有字符串，那 max 会报错。
# nums = [23, 11, 32, 30, 17, '尚硅谷']
# max(nums)

# 3.3 如果容器中的元素：都是字符串，那 max 会返回：Unicode 编码最大的字符。
# msg_list = ['北京', '尚硅谷', '你好']
# result = max(msg_list)
# print(msg_list)
# print(result)

# 3.4 max 函数也可以接收多个值，并筛选出最大值
# result = max(33, 45, 12, 78, 99)
# print(result)

# 4.使用内置的 min 函数，获取容器中的最小值，返回值是：最小值。
# 备注：min 函数的使用方式与注意点与 max 函数一样，只不过 min 函数返回的是最小值
# nums = [23, 11, 32, 30, 17]
# result = min(nums)
# print(result)

# 5.使用内置的 sum 函数，对容器中的数据进行求和（元素只能是数值）。
# nums = [10, 20, 30, 40, 50]
# result = sum(nums)
# print(result)
