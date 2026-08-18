import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# 1️⃣ 创建『进程池执行器』、使用 submit 方法提交任务、使用 shutdown 方法等待任务完成。
# def work(n):
#     print(f'work正在执行任务{n}.........{os.getpid()}')
#     time.sleep(1)
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个进程池执行器
#     executor = ProcessPoolExecutor(3)
#     # 使用 submit 方法提交任务（submit 只负责“提交任务”，不会阻塞主进程）
#     executor.submit(work, 1)
#     executor.submit(work, 2)
#     executor.submit(work, 3)
#     executor.submit(work, 4)
#     executor.submit(work, 5)
#     executor.submit(work, 6)
#     executor.submit(work, 7)
#     # shutdown 的作用：不再接收新的任务。
#     # wait=True 的作用：阻塞主进程，等待进程池中所有任务执行完毕。
#     executor.shutdown(wait=True)
#     print('---------end-------------')


# 2️⃣ 获取子进程执行后的返回结果（Future类的实例对象 + result方法）
# def work(n):
#     print(f'work正在执行任务{n}.........{os.getpid()}')
#     time.sleep(1)
#     return f'我是任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个进程池执行器
#     executor = ProcessPoolExecutor(3)
#     # 使用 submit 方法提交任务（submit 只负责“提交任务”，不会阻塞主进程）
#     # f1 = executor.submit(work, 1)
#     # f2 = executor.submit(work, 2)
#     # f3 = executor.submit(work, 3)
#     # f4 = executor.submit(work, 4)
#     # f5 = executor.submit(work, 5)
#     # f6 = executor.submit(work, 6)
#     # f7 = executor.submit(work, 7)
#     futures = [executor.submit(work, index) for index in range(1, 8)]
#     # 阻塞主进程，等待进程池中所有任务执行完毕。
#     executor.shutdown(wait=True)
#     # print(f1.result())
#     # print(f2.result())
#     # print(f3.result())
#     # print(f4.result())
#     # print(f5.result())
#     # print(f6.result())
#     # print(f7.result())
#     for f in futures:
#         print(f.result())
#     print('---------end-------------')


# 3️⃣ 使用 as_completed：按“完成顺序”获取结果
# def work(n):
#     print(f'work正在执行任务{n}.........{os.getpid()}')
#     if n == 1:
#         time.sleep(15)
#     elif n == 2:
#         time.sleep(10)
#     else:
#         time.sleep(1)
#     return f'我是任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个进程池执行器
#     executor = ProcessPoolExecutor(3)
#     # 使用 submit 方法提交任务（submit 只负责“提交任务”，不会阻塞主进程）
#     futures = [executor.submit(work, index) for index in range(1, 8)]
#     # 准备一个 result_list 去收集任务的具体结果
#     result_list = []
#     # 收集每个任务的结果
#     for f in as_completed(futures):
#         result_list.append(f.result())
#     # 阻塞主进程，等待进程池中所有任务执行完毕。
#     executor.shutdown(wait=True)
#     # 打印最终的结
#     print(result_list)
#     print('---------end-------------')


# 4️⃣使用 add_done_callback 方法，为任务添加完成时的回调函数
# def work(n):
#     print(f'work正在执行任务{n}.........{os.getpid()}')
#     if n == 1:
#         time.sleep(15)
#     elif n == 2:
#         time.sleep(10)
#     else:
#         time.sleep(1)
#     return f'我是任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个进程池执行器
#     executor = ProcessPoolExecutor(3)
#     # 准备一个 result_list 列表去收集任务的结果
#     result_list = []
#     # 任务完成后的回调函数
#     def done_func(futrue):
#         result_list.append(futrue.result())
#     # 开启7个任务，并指定回调函数
#     for index in range(1, 8):
#         f = executor.submit(work, index)
#         f.add_done_callback(done_func)
#     # 等所有任务都完成
#     executor.shutdown(wait=True)
#     # 打印最终的结果（按“完成的顺序”获取）
#     print(result_list)
#     print('---------end-------------')


# 5️⃣使用 map 方法批量提交任务（注意：map方法本身不阻塞，但读取其返回的生成器对象是阻塞的，并且得到结果的顺序，与任务分配的顺序是一致的）
#  换一种说法：map方法会把这一批任务提交到进程池里执行，它会立刻返回一个生成器，真正的阻塞发生在：生成器取结果时（如 list(result)
# def work(n):
#     print(f'work正在执行任务{n}.........{os.getpid()}')
#     if n == 1:
#         time.sleep(15)
#     elif n == 2:
#         time.sleep(10)
#     else:
#         time.sleep(1)
#     return f'我是任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个进程池执行器
#     executor = ProcessPoolExecutor(3)
#     # 通过 map 方法批量提交任务（结果按照提交的顺序来）
#     results = executor.map(work, [1, 2, 3, 4, 5, 6, 7])
#     # 获取 results 生成器中的内容
#     print(list(results))
#     # 等所有任务都完成
#     executor.shutdown(wait=True)
#     print('---------end-------------')


# 6️⃣使用 with：进程池的“自动回收”写法，离开 with 代码块时自动执行 shutdown(wait=True)
# def work(n):
#     print(f'work正在执行任务{n}.........{os.getpid()}')
#     if n == 1:
#         time.sleep(15)
#     elif n == 2:
#         time.sleep(10)
#     else:
#         time.sleep(1)
#     return f'我是任务{n}的结果'
#
# if __name__ == '__main__':
#     print('---------start-------------')
#     # 创建一个进程池执行器
#     with ProcessPoolExecutor(3) as executor:
#         # 通过 map 方法批量提交任务（结果按照提交的顺序来）
#         results = executor.map(work, [1, 2, 3, 4, 5, 6, 7])
#         # 获取 results 生成器中的内容
#         print(list(results))
#     print('---------end-------------')
