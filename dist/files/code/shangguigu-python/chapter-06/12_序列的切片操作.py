# 对列表进行切片
# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[0:5:1]
# print(list2)

# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[1:8:2]
# print(list2)

# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[1:8:3]
# print(list2)

# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[::]
# print(list2)

# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[:999:]
# print(list2)

# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[3::]
# print(list2)

# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[:5:]
# print(list2)

# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[::4]
# print(list2)

# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[7:2:-1]
# print(list2)

# 一个特殊情况：当同时省略起始索引和结束索引时，如果步长为负数，那Python会自动对调：起始位置和结束位置
# list1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# list2 = list1[::-1]
# print(list2)

# 对元组进行切片
# tuple1 = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
# tuple2 = tuple1[0:5:1]
# print(tuple2)

# 对字符串进行切片
msg1 = 'welcome to atguigu'
msg2 = msg1[2:9:2]
print(msg2)
