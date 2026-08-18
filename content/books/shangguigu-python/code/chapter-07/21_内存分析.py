# a = 666
# print(id(a))
# b = a
# print(id(b))
# print(a)
# print(b)
# a = 888
# print(a)
# print(b)
# print(id(a))
# print(id(b))

stu_list = ['张三', '李四', '王五']
print(id(stu_list))
print(id(stu_list[0]))
stu_list[0] = '阿三'
print(id(stu_list))
print(id(stu_list[0]))
