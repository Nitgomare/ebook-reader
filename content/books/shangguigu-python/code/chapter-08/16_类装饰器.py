# 类装饰器：
# 1.包含 __call__ 方法的类，就是类装饰器。
# 2.像调用函数一样，去调用类装饰器的实例对象，就会触发 __call__ 方法的调用。
# 3.__call__ 方法通常接收一个函数作为参数，并且会返回一个新函数。

# class SayHello:
#     def __call__(self, func):
#         def wrapper(*args, **kwargs):
#             print('你好，我要开始计算了')
#             return func(*args, **kwargs)
#         return wrapper

# 使用@语法糖使用类装饰器
# @SayHello()
# def add(x, y):
#     res = x + y
#     print(f'{x}和{y}相加的结果是{res}')
#     return res

# 正常调用add函数
# result = add(10, 20)
# print(result)

# 使用 SayHello 去装饰 add 函数（手动装饰）
# say = SayHello()
# add = say(add)
# result = add(10, 20)
# print(result)

# 带参数的类装饰器
# class SayHello:
#     def __init__(self, msg):
#         self.msg = msg
#
#     def __call__(self, func):
#         def wrapper(*args, **kwargs):
#             print(f'你好，我要开始{self.msg}计算了')
#             return func(*args, **kwargs)
#         return wrapper
#
# @SayHello('加法')
# def add(x, y):
#     res = x + y
#     print(f'{x}和{y}相加的结果是{res}')
#     return res
#
# result = add(10, 20)
# print(result)


# 多个类装饰器的使用
class Test1:
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print('我是Test1追加的逻辑')
            return func(*args, **kwargs)
        return wrapper

class Test2:
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print('我是Test2追加的逻辑')
            return func(*args, **kwargs)
        return wrapper

@Test1()
@Test2()
def add(x, y):
    res = x + y
    print(f'{x}和{y}相加的结果是{res}')
    return res

result = add(10, 20)
print(result)
