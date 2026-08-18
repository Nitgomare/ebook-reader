# 定义一个成绩列表
score_list = [62, 50, 60, 48, 80, 20, 95]

# 使用while循环遍历列表
index = 0
while index < len(score_list):
    print(score_list[index])
    index += 1

# 使用for循环遍历列表
# for item in score_list:
#     print(item)

# 使用for循环遍历列表（通过range函数 和 len函数按照索引遍历）
# for index in range(len(score_list)):
#     print(score_list[index])

# 使用for循环遍历列表（通过enumerate函数，同时获取下标（索引值）和元素）
# enumerate 的 start 参数，可以让计数从指定值开始（改变的是循环时的“编号”，不是真正的索引值）
# for index, item in enumerate(score_list, start=5):
#     print(index, item, score_list[0])
# print('最后的打印', score_list[0])
