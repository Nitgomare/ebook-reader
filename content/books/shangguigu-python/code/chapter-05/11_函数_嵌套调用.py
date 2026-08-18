# 函数嵌套调用测试1
# def greet(name, msg):
#     print(f'我叫{name}，我想说的话在下面：')
#     speak(msg)
#     print('嗯，我想说的结束了')
#
# def speak(msg):
#     print('----------')
#     print(msg)
#     print('----------')
#
# greet('张三', '你好啊')

# 函数嵌套调用测试2
def test1():
    print('进入 test1 函数')
    test2()
    print('退出 test1 函数')

def test2():
    print('进入 test2 函数')
    test3()
    print('退出 test2 函数')

def test3():
    print('进入 test3 函数')
    print('***正在执行 test3 函数')
    print('退出 test3 函数')

test1()
