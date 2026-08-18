# 新增操作
# 方式一：通过列表的append方法，在列表尾部追加一个元素
nums = [10, 20, 30, 40]
nums.append(50)
print(nums)

# 方式二：通过列表的insert方法，在列表的指定下标处添加一个元素
# nums = [10, 20, 30, 40]
# nums.insert(2, 666)
# print(nums)

# 方式三：通过列表的extend方法，将可迭代对象中的内容依次取出，追加到列表尾部
# nums = [10, 20, 30, 40]
# nums.extend('尚硅谷')
# nums.extend(range(1, 4))
# nums.extend([70, 80, 90])
# print(nums)

# 删除操作
# 方式一：通过列表的pop方法，删除指定位置的元素，并返回该元素
# nums = [10, 20, 10, 40, 50]
# result = nums.pop(1)
# print(nums)
# print(result)

# 方式二：通过列表的remove方法，删除列表中第一次出现的指定值
# nums = [10, 20, 10, 40, 50]
# nums.remove(10)
# print(nums)

# 方式三：通过列表的clear方法，删除列表中所有的元素（清空列表）
# nums = [10, 20, 10, 40, 50]
# nums.clear()
# print(nums)

# 方式四：通过del关键字，删除指定元素
# nums = [10, 20, 10, 40, 50]
# del nums[3]
# print(nums)

# 修改操作
# nums = [10, 20, 10, 40, 50]
# nums[2] = 66
# print(nums)

# 查询操作
# nums = [10, 20, 10, 40, 50]
# print(nums[3])
