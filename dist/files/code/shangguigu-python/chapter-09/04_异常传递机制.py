# 异常的传递机制：
# 1.如果异常没有被当前代码块所捕获处理，那该异常就会沿着调用链，逐层传递给其调用者。
# 2.如果所有调用者，都没有捕获该异常，那最终程序将因【未处理异常】而意外终止。
def test1():
    print('******test1开始******')
    result = '100' + 100
    print('******test1结束******')

def test2():
    print('******test2开始******')
    try:
        test1()
    except Exception as e:
        print(f'程序异常：{e}')
    print('******test2结束******')

def test3():
    print('******test3开始******')
    test2()
    print('******test3结束******')

test3()
