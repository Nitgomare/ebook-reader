# 一、函数的多返回值
# def calculate(x, y):
#     res1 = x + y
#     res2 = x - y
#     return res1, res2
#
# result = calculate(30, 10)
# print(result)
#
# r1, r2 = calculate(30, 10)
# print(r1, r2)


# 二、参数的打包与解包

# 1.打包接收参数：
# *args    ：打包所有的位置参数（会形成一个元组）
# **kwargs ：打包所有的关键字参数（会形成一个字典）
# def show_info(*args, **kwargs):
#     print(args)
#     print(kwargs)
#
# show_info(10, 20, 30, name='张三', age=18, gender='男')


# 2.解包传递参数
# *变量名  ：将元组拆解成一个一个独立的位置参数
# **变量名 ：将字典拆解一个一个 key=value 形式的关键字参数
# def show_info(num1, num2, num3, name, age, gender):
#     print(num1, num2, num3)
#     print(name, age, gender)
#
# nums = (10, 20, 30)
# person = {'name':'张三', 'age':18, 'gender':'男'}
#
# show_info(*nums, **person)


# 3.打包接收参数 和 解包传递参数 一起使用
# def show_info(*args, **kwargs):
#     print(args)
#     print(kwargs)
#
# nums = (10, 20, 30)
# person = {'name':'张三', 'age':18, 'gender':'男'}
#
# show_info(*nums, **person)
