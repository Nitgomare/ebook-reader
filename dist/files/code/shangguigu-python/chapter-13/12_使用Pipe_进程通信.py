import time
from multiprocessing import Process, Pipe

def test1(con1):
    time.sleep(2)
    con1.send(100)
    print('test1发送了100')

def test2(con2):
    data = con2.recv()
    print(f'test2接收了{data}')


if __name__ == '__main__':
    con1, con2 = Pipe(duplex=False)
    p1 = Process(target=test1, args=(con1,))
    p2 = Process(target=test2, args=(con2,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
