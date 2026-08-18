# 1.函数也是对象
# a1 = 100            # int类的实例对象
# a2 = 'hello'        # str类的实例对象
# a3 = [10, 20, 30]   # list类的实例对象
#
# def welcome():      # welcome函数function类的实例对象
#     print('你好啊')
#
# print(type(a1))
# print(type(a2))
# print(type(a3))
# print(type(welcome))

# 2.函数可以动态添加属性
# def welcome():
#     print('你好啊')
# welcome.desc = '这是一个打招呼的函数'
# welcome.version = 1.0
# print(welcome.desc)
# print(welcome.version)


# 3.函数可以赋值给变量
# def welcome():
#     print('你好啊')
# welcome.desc = '这是一个打招呼的函数'
# welcome.version = 1.0
#
# say_hello = welcome
# say_hello()
# print(say_hello.desc)
# print(say_hello.version)


# 4.可变参数 vs 不可变参数
# 不可变参数
# a = 666
# def welcome(data):
#     print('data修改前', data, id(data))
#     data = 888
#     print('data修改后', data, id(data))
#
# print('函数调用前', a, id(a))
# welcome(a)
# print('函数调用后', a, id(a))

# 可变参数
# a = [10, 20, 30]
# def welcome(data):
#     print('data修改前', data, id(data))
#     data[2] = 99
#     print('data修改后', data, id(data))
#
# print('函数调用前', a, id(a))
# welcome(a)
# print('函数调用后', a, id(a))


# 5.函数也可以作为参数
# def welcome():
#     print('你好啊')
#
# def caller(f):
#     print('caller函数调用了')
#     f()
#
# caller(welcome)

# 6.函数也可以作为返回值
def welcome():
    print('你好啊')
    def show_msg(msg):
        print(msg)
    return show_msg

# result = welcome()
# result('尚硅谷')
welcome()('尚硅谷')
