def order(num, dish):
    print(f'您点的是：{num}份 {dish}')
    print(f'{dish}可是很好吃的！')
    print(f'你只点了{num}份，够吃吗？\n')

# 函数的形参：num，dish 只能在函数内去使用
# print(num)

order(1, '辣椒炒肉')
order(2, '辣子鸡')

# 以下是错误示范
# order(3)
# order(4, '宫保鸡丁', 7)
