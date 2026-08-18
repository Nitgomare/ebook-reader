# 使用str()将指定数据转换为字符串。
# result1 = str(18)
# result2 = str(75.6)
# result3 = str(1.8e3)
# result4 = str(12_000)
#
# print(type(result1),result1)
# print(type(result2),result2)
# print(type(result3),result3)
# print(type(result4),result4)

# 使用int()将指定数据转换为整型。
# result1 = int(15.6)
# result2 = int('79')
# result3 = int('   79   ')
# result4 = int(48)

# 以下是错误示例
# int('   7 9   ')
# int('你好')
# int('79个')
# int('15.6')

# print(type(result1),result1)
# print(type(result2),result2)
# print(type(result3),result3)
# print(type(result4),result4)

# 使用float()将指定数据转换为浮点型。
result1 = float(18)
result2 = float('15.6')
result3 = float('   5.7   ')
result4 = float(14.8)
result5 = float('48')

# 以下是反例
# float('   5.  7   ')
# float('你好')
# float('5.7元')
# float('5.23.12')

print(type(result1), result1)
print(type(result2), result2)
print(type(result3), result3)
print(type(result4), result4)
print(type(result5), result5)
