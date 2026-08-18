# keys方法：用于获取字典中所有的键
# d1 = {'张三': 72, '李四': 60, '王五': 85}

# keys方法的返回值不是list，而是一种叫做dict_keys的类型
# result = d1.keys()
# print(result)
# print(type(result))

# dict_keys和列表类似，可以被遍历，但要注意的是：它不能通过下标访问元素
# for item in result:
#     print(item)
# print(result[0])

# 借助内置的list函数，可以将dict_keys转换成list
# l1 = list(result)
# print(l1)
# print(type(l1))

# values方法：获取字典中所有的值
# d1 = {'张三': 72, '李四': 60, '王五': 85}
# values方法的返回值类型是：dict_values，它的特点和dict_keys一样
# result = d1.values()
# print(result)
# print(type(result))

# items方法：获取字典中所有的键值对（每组键值对以元组的形式呈现）
d1 = {'张三': 72, '李四': 60, '王五': 85}
# items方法返回的类型是：dict_items，它的特点也和dict_keys一样
result = d1.items()
print(result)
print(type(result))
