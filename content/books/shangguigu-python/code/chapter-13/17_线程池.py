import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import get_native_id, RLock

# 1️⃣ 创建『线程池执行器』、使用 submit 方法提交任务、使用 shutdown 方法等待任务完成。
# def work(n, lock):
#     with lock:
#         print(f'work正在执行任务{n}.........{get_native_id()}')
#     time.sleep(1)
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个线程池执行器
#     executor = ThreadPoolExecutor(3)
#     # 创建线程锁
#     lock = RLock()
#     # 使用 submit 方法提交任务（submit 只负责“提交任务”，不会阻塞主线程）
#     executor.submit(work, 1, lock)
#     executor.submit(work, 2, lock)
#     executor.submit(work, 3, lock)
#     executor.submit(work, 4, lock)
#     executor.submit(work, 5, lock)
#     executor.submit(work, 6, lock)
#     executor.submit(work, 7, lock)
#     # shutdown 的作用：不再接收新的任务。
#     # wait=True 的作用：阻塞主线程，等待线程池中所有任务执行完毕。
#     executor.shutdown(wait=True)
#     print('---------end-------------')


# 2️⃣ 获取子线程执行后的返回结果（Future类的实例对象 + result方法）
# def work(n, lock):
#     with lock:
#         print(f'work正在执行任务{n}.........{get_native_id()}')
#     time.sleep(1)
#     return f'任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个线程池执行器
#     executor = ThreadPoolExecutor(3)
#     # 创建线程锁
#     lock = RLock()
#     # 使用 submit 方法提交任务（submit 只负责“提交任务”，不会阻塞主线程）
#     futures = [executor.submit(work, index, lock) for index in range(1, 8)]
#     # 阻塞主线程，等待线程池中所有任务执行完毕。
#     executor.shutdown(wait=True)
#     # 打印结果
#     for f in futures:
#         print(f.result())
#     print('---------end-------------')

# 3️⃣ 使用 as_completed：按“完成顺序”获取结果
# def work(n, lock):
#     with lock:
#         print(f'work正在执行任务{n}.........{get_native_id()}')
#     if n == 1:
#         time.sleep(15)
#     elif n == 2:
#         time.sleep(10)
#     else:
#         time.sleep(1)
#     return f'任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个线程池执行器
#     executor = ThreadPoolExecutor(3)
#     # 创建线程锁
#     lock = RLock()
#     # 使用 submit 方法提交任务（submit 只负责“提交任务”，不会阻塞主线程）
#     futures = [executor.submit(work, index, lock) for index in range(1, 8)]
#     # 收集每个线程返回的结果
#     result_list = []
#     # 将每个线程返回的结果，存入result_list
#     for f in as_completed(futures):
#         result_list.append(f.result())
#     # 阻塞主线程，等待线程池中所有任务执行完毕。
#     executor.shutdown(wait=True)
#     # 打印最终的结果
#     print(result_list)
#     print('---------end-------------')


# 4️⃣使用 add_done_callback 方法，为任务添加完成时的回调函数
# def work(n, lock):
#     with lock:
#         print(f'work正在执行任务{n}.........{get_native_id()}')
#     if n == 1:
#         time.sleep(15)
#     elif n == 2:
#         time.sleep(10)
#     else:
#         time.sleep(1)
#     return f'任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个线程池执行器
#     executor = ThreadPoolExecutor(3)
#     # 创建线程锁
#     lock = RLock()
#     # 收集每个线程的执行结果
#     result_list = []
#     # 定义一个线程执行成功后的回调函数
#     def done_func(f):
#         result_list.append(f.result())
#     # 使用submit提交任务，并指定回调函数
#     for index in range(1, 8):
#         f = executor.submit(work, index, lock)
#         f.add_done_callback(done_func)
#     # 阻塞主线程，等待线程池中所有任务执行完毕。
#     executor.shutdown(wait=True)
#     # 打印最终的结果
#     print(result_list)
#     print('---------end-------------')


# 5️⃣使用 map 方法批量提交任务（注意：map方法本身不阻塞，但读取其返回的生成器对象是阻塞的，并且得到结果的顺序，与任务分配的顺序是一致的）
#  换一种说法：map方法会把这一批任务提交到线程池里执行，它会立刻返回一个生成器，真正的阻塞发生在：生成器取结果时（如 list(result)

# def work(n, lock):
#     with lock:
#         print(f'work正在执行任务{n}.........{get_native_id()}')
#     if n == 1:
#         time.sleep(15)
#     elif n == 2:
#         time.sleep(10)
#     else:
#         time.sleep(1)
#     return f'任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个线程池执行器
#     executor = ThreadPoolExecutor(3)
#     # 创建线程锁
#     lock = RLock()
#     # 使用map方法批量提交任务
#     result = executor.map(work, [1, 2, 3, 4, 5, 6, 7], [lock]*7)
#     # 打印最终的结果
#     print(list(result))
#     # 阻塞主线程，等待线程池中所有任务执行完毕。
#     executor.shutdown(wait=True)
#     print('---------end-------------')


# 6️⃣使用 with：线程池的“自动回收”写法，离开 with 代码块时自动执行 shutdown(wait=True)
def work(n, lock):
    with lock:
        print(f'work正在执行任务{n}.........{get_native_id()}')
    if n == 1:
        time.sleep(15)
    elif n == 2:
        time.sleep(10)
    else:
        time.sleep(1)
    return f'任务{n}的结果'

if __name__ == '__main__':
    print('---------start-------------')
    with ThreadPoolExecutor(3) as executor:
        # 创建线程锁
        lock = RLock()
        # 使用map方法批量提交任务
        result = executor.map(work, [1, 2, 3, 4, 5, 6, 7], [lock]*7)
        # 打印最终的结果
        print(list(result))
    print('---------end-------------')
