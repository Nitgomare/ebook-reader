# 进程之间不共享内存，因此也就不共享任何变量。
from multiprocessing import Process

def test1(num, names):
    num += 10
    names.append('张三')
    print(f'我是 test1 进程，操作之后的num是{num}，操作之后的names是{names}')

def test2(num, names):
    num -= 10
    names.append('李四')
    print(f'我是 test2 进程，操作之后的num是{num}，操作之后的names是{names}')

if __name__ == "__main__":
    num = 100
    names = []

    print('主进程中的【第一行】代码')
    p1 = Process(target=test1, args=(num, names))
    p2 = Process(target=test2, args=(num, names))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    print('主进程中的【最后一行】代码', num, names)
