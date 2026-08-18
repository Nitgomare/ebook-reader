import os
import time
from multiprocessing import Process

def speak():
    try:
        for index in range(10):
            print(f'我在说话{index}, 进程pid是:{os.getpid()}, 我的父进程是:{os.getppid()}')
            time.sleep(1)
    # 注意：使用 terminate 终止进程，不会引起 finally 执行！
    finally:
        print('我是finally里的逻辑')

def study():
    for index in range(15):
        print(f'我在学习{index}, 进程pid是:{os.getpid()}, 我的父进程是:{os.getppid()}')
        time.sleep(1)

if __name__ == '__main__':
    print('我是主进程中的【第一行】打印')
    p1 = Process(target=speak)
    p2 = Process(target=study)
    p1.start()
    p2.start()

    time.sleep(3)
    print('我是主进程，我准备强制终止p1进程........')
    # 向操作系统申请强制终止p1进程
    p1.terminate()
    # 等操作系统彻底终止掉了p1进程
    p1.join()
    # 看一下p1进程是否“活着”
    print(p1.is_alive())

    print('我是主进程中的【最后一行】打印')
