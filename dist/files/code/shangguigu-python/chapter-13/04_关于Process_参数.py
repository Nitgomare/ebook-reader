import os
import time
from multiprocessing import Process, current_process

def speak(a, b, msg):
    for index in range(10):
        print(f'{msg}--{a}--{b}--{current_process().name}--我在说话{index}, 进程pid是:{os.getpid()}, 我的父进程是:{os.getppid()}')
        time.sleep(1)

def study():
    for index in range(15):
        print(f'我在学习{index}, 进程pid是:{os.getpid()}, 我的父进程是:{os.getppid()}')
        time.sleep(1)

if __name__ == '__main__':
    print('我是主进程中的【第一行】打印')
    # Process的参数：
    #   🔸group： 默认值为None（应当始终为None）。
    #   🔸target：子进程要执行的可调用对象，默认值为 None。
    #   🔸name：  进程名称，默认为 None ，如果设置为 None，Python 会自动分配名字。
    #   🔸args：  给 target 传的位置参数（元组）
    #   🔸kwargs：给 target 传的关键字参数（字典）。
    #   🔸daemon：标记进程是否为守护进程，取值为布尔值（默认为 None，表示从创建方进程继承）。
    p1 = Process(target=speak, name='说话进程', args=(666, 888), kwargs={'msg':'尚硅谷'})
    p2 = Process(target=study)
    # print(p1.name)
    # print(p2.name)
    p1.start()
    p2.start()
    print('我是主进程中的【最后一行】打印')
