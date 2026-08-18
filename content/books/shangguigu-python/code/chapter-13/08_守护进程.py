# 什么是守护进程？
#   1.一种 “依附于主进程存在的子进程”，一旦主进程结束，它就会被自动终止。
#   2.简言之：主进程一死，守护进程必跟着死。
#
# 守护进程的使用场景：
#   1.后台监控类任务
#   2.日志 / 统计 / 采样 类任务
#   3.辅助型“陪跑任务”
#
# 注意点：
#   1.守护进程必须是 子进程。
#   2.主进程结束，守护进程也会随之结束。
#   3.守护进程中，不允许再创建新的子进程。
#   4.必须在 start 之前，start() 之后，不能再设置 daemon

import os
import time
from multiprocessing import Process

def monitor():
    while True:
        try:
            with open('log.txt', 'r', encoding='utf-8') as file:
                lines = sum(1 for _ in file)
        except FileNotFoundError:
            lines = 0
        print(f'我是【守护进程({os.getpid()})】，log.txt 共有{lines}行')
        time.sleep(1)

def test():
    for index in range(30):
        print(f'我是test({os.getpid()})')
        time.sleep(1)

if __name__ == '__main__':
    print(f'我是主进程({os.getpid()})中的【第一行】代码')

    p1 = Process(target=monitor, daemon=True)
    p2 = Process(target=test)

    p1.start()
    p2.start()

    # 向文件中写入数据
    with open('log.txt', 'a', encoding='utf-8') as file:
        for index in range(10):
            file.write(f'尚硅谷{index}\n')
            file.flush()
            time.sleep(1)

    print(f'我是主进程({os.getpid()})中的【最后一行】代码')
