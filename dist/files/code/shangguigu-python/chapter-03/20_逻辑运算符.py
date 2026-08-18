# and用于判断其两侧的值，是否都为True
# print(True and True)
# print(True and False)
# print(False and True)
# print(False and False)
# print(8 > 7 and 8 > 7)
# print(8 > 7 and 2 > 3)
# print(2 > 3 and 8 > 7)
# print(2 > 3 and 2 > 3)

# and具备“逻辑短路”能力
# print(False and 3 / 0)
# print(3 > 9 and 3 / 0)

# and返回的不一定是布尔值，它返回的是某个参与计算的值本身
# 规则：and会先看左边，如果左边是“假”，就直接返回左边，否则返回右边
# 备注：若参与and运算的值不是布尔值，那Python会自动转为布尔值，然后再进行逻辑操作
# print(2 - 2 and True)
# print('' and True)
# print(True and 8 / 2)
# print(3 + 3 and 3 * 4)

# or用于判断其两侧，是否至少有一个为True（只要有一个是True，那就返回True）
# print(True or True)
# print(True or False)
# print(False or True)
# print(False or False)
# print(9 > 2 or 9 > 2)
# print(9 > 2 or 3 < 1)
# print(3 < 1 or 9 > 2)
# print(3 < 1 or 3 < 1)

# or同样具备“逻辑短路”的能力
# print(True or 3 / 0)
# print(9 > 3 or 3 / 0)

# or返回的也不一定是布尔值，它返回的是参与计算的值本身
# 规则：or会先看左边，如果左边为“真”，就直接返回左边，否则返回右边
# 备注：若参与or运算的值不是布尔值，那Python会自动转为布尔值，然后再进行逻辑操作
# print(7 - 2 or False)
# print('你好' or '尚硅谷')
# print(False or 8 / 2)
# print(2 - 2 or 3 * 4)

# not用于取反
# 备注：若参与not运算的值不是布尔值，那Python会自动转为布尔值，然后再进行逻辑操作
# print(not True)
# print(not False)
# print(not 3 > 2)
# print(not 3 < 2)

# not返回的值，一定是布尔值！
print(not 0)
print(not 3 > 2)
print(not 9 // 4)
print(not 'abc')
print(9 //4)
