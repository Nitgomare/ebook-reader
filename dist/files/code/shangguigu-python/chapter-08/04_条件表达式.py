# 表达式：执行后能得到值的代码，就是表达式（表达式最终会形成一个值，可以写在任何需要值的地方）。
# a1 = 3 + 5
# a2 = 'abc' * 3
# print(5 > 3)
# int('y' in 'python')
# a5 = len('hello')

# 条件表达式：根据条件的真假，在两个值中二选一的表达式（又称：三元表达式、三目运算符）。
age = 21

# 传统的if-else去写：
# if age >= 18:
#     text = '成年'
# else:
#     text = '未成年'
# print(text)

# 条件表达式去写：值1 if 条件 else 值2
# text = '成年' if age >= 18 else '未成年'
# print(text)

# 条件表达式的使用场景：简单的二选一场景
rain = True
eat = '外卖' if rain else '出去吃'

is_vip = False
disscount = 0.8 if is_vip else 1.0

is_login = False
msg = '欢迎回来！' if is_login else print('哈哈哈')

print(eat)
print(disscount)
print(msg)
