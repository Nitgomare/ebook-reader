# 我们之前学过 list、tuple、dict，它们的特点是：数据想怎么拿数据，就怎么拿。
# 队列(Queue)是：一种“先进先出”的数据结构（先放进去的数据，一定会先取出来）
import time
from multiprocessing import Queue, Process

# 创建一个队列（不限制大小，即：不设置容量上限）
# q1 = Queue()

# 创建一个队列（最多能保存3个元素）
# q2 = Queue(3)

# 1️⃣put方法：往队列里放数据（入队）
# q1.put(10)
# q1.put(20)
# q1.put(30)

# 2️⃣get方法：从队列里取数据（出队）
# value1 = q1.get()
# value2 = q1.get()
# value3 = q1.get()
# print(value1)
# print(value2)
# print(value3)

# 3️⃣empty方法：判断队列是否为空
# result = q1.empty()
# print(result)

# 4️⃣full方法：判断队列是否已满
# q1.put(10)
# q1.put(20)
# q1.put(30)
# result = q1.full()
# print(result)

# q2.put(100)
# q2.put(200)
# q2.put(300)
# result = q2.full()
# print(result)

# 5️⃣qsize方法：获取队列长度
# q1.put(10)
# q1.put(20)
# q1.put(30)
# result = q1.qsize()
# print(result)

# 6️⃣队列具备等待模式
# q2.put(100)
# q2.put(200)
# q2.put(300)

# (1).当队列已满，继续 put，就会进入等待模式，等别人调用get方法，取走一个元素
# q2.put(400)
# print('放入完毕')

# (2).当队列已满，执行：put(元素, timeout=秒数)，就会等待指定秒数。
# q2.put(400, timeout=3)
# print('放入完毕')

# (3).put_nowait 方法，会直接向队列中添加元素，不会进入等待模式，若队列已满，会抛出异常。
# 备注：put_nowait 等价于 put(元素, block=False)，block的默认值为 True
# q2.put_nowait(400)
# q2.put(400, block=False)

# get读多了，也会进入等待模式
# q2.get()
# q2.get()
# q2.get()

# (1).当队列已空，继续 get，就会进入等待模式。x
# q2.get()

# (2).当队列已空，执行 get(timeout=秒数)，就会等待指定秒数。
# q2.get(timeout=3)

# (3).get_nowait 方法，会直接读取队列中的元素，不会进入等待模式，若队列已空，会抛出异常
# 备注：get_nowait 等价于 get(block=False)
# q2.get_nowait()
# q2.get(block=False)

def test(q):
    time.sleep(3)
    result = q.get()
    print('我从队列中取出了一个元素：',result)


# 通过多进程，演示一下：当队列满了以后，再次put会等待，当有人从队列中取出元素后，put会继续。
if __name__ == '__main__':
    # 创建一个队列，让其最多能保存2个元素
    q = Queue(2)
    # put两次，把队列填满
    q.put('尚硅谷')
    q.put('atguigu')
    print(f'队列是否已满：{q.full()}')

    # 创建子进程p1
    p1 = Process(target=test, args=(q, ))
    # 开启子进程p1，让其3秒钟后，从队列中取出一个元素
    p1.start()

    print('即将向已满的队列中添加一个元素........')
    q.put('hello')

    print('目前队列中有的元素是：')
    print(q.get())
    print(q.get())
