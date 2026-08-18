import os
import time
from multiprocessing import Process
print(100, __name__, os.getpid())

# 定义一个 speak 函数，功能是：每隔一秒说话一次（一共说话10次）
def speak():
    for index in range(10):
        print(f'我在说话{index}, 进程pid是:{os.getpid()}, 我的父进程是:{os.getppid()}')
        time.sleep(1)

# 定义一个 study 函数，功能是：每隔一秒学习一次（一共学习15次）
def study():
    for index in range(15):
        print(f'我在学习{index}, 进程pid是:{os.getpid()}, 我的父进程是:{os.getppid()}')
        time.sleep(1)

# 注意：一定要写 if __name__ == '__main__' 这个判断，原因如下：
#   1.当创建子进程时，Python 并不会把父进程内存里的 speak 函数直接交给子进程。
#   2.Python会启动一个全新的 Python 解释器进程，重新执行当前的 .py 文件（作为模块）。
#   3.在执行过程中，重新定义出一个 speak 函数，交给子进程。
if __name__ == '__main__':
    print('我是主进程中的【第一行】打印')
    # 创建两个 Process 类的实例对象（进程对象），分别是 p1 和 p2。
    # 注意点1：p1 和 p2 就对应着以后的两个子进程，在创建它们的时候，就要指定好他们要执行的任务。
    # 注意点2：此时的 p1 和 p2 只是代码层面的两个进程对象，操作系统还没有真的创建 p1 和 p2 两个进程。
    p1 = Process(target=speak)
    p2 = Process(target=study)

    # 调用进程对象的 start 方法，会立刻向操作系统申请一个进程，并且会将该进程交由操作系统进行调度。
    p1.start()
    p2.start()

    print('我是主进程中的【最后一行】打印')
