# 在windows操作系统中，查看：进程名、父进程pid、进程pid、 的命令如下：
# wmic process get Name,ParentProcessId,ProcessId

import os
import time

print(f'当前进程的pid是：{os.getpid()}')
print(f'当前进程的父进程pid是：{os.getppid()}')
time.sleep(10000)
