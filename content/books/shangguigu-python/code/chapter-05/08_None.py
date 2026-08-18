# None是一个特殊的字面量，它表示：空值 / 无值 / 无意义。
msg = None

# None 的类型是 NoneType。
print(type(msg))

# None 转为布尔值是 False。
print(bool(msg))
if not msg:
    print('你好')

# 不能参与数学运算，也不能与字符串拼接。
# result1 = msg + 1
# result1 = msg + 'hello'
