from multiprocessing import Process
import os, time

class SpeakProcess(Process):
    def __init__(self, a, b, **kwargs):
        super().__init__(**kwargs)
        self.a = a
        self.b = b

    def run(self):
        for index in range(10):
            print(f'{self.a}--{self.b}--我在说话{index}, 进程pid是:{os.getpid()}, 我的父进程是:{os.getppid()}')
            time.sleep(1)

class StudyProcess(Process):
    def run(self):
        for index in range(15):
            print(f'我在学习{index}, 进程pid是:{os.getpid()}, 我的父进程是:{os.getppid()}')
            time.sleep(1)

if __name__ == '__main__':
    print('我是主进程中的【第一行】打印')
    p1 = SpeakProcess(100, 200)
    p2 = StudyProcess()

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print('我是主进程中的【最后一行】打印')
