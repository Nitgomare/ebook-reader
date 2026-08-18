# IO密集型任务，更适合用多线程。
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 拷贝文件
def copy_file(index):
    with open('a.zip', 'rb') as src, open(f'a_副本{index}.zip', 'wb') as dst:
        while True:
            data = src.read(1024 * 1024)  # 每次读 1MB
            if not data:
                break
            dst.write(data)

if __name__ == '__main__':
    # print('===== 使用多进程完成【IO密集型任务】 =====')
    # start = time.time()
    # with ProcessPoolExecutor(4) as executor:
    #     for i in range(4):
    #         executor.submit(copy_file, i)
    # end = time.time() - start
    # print(f'多进程耗时：{end} 秒')

    print('===== 使用多线程完成【IO密集型任务】 =====')
    start = time.time()
    with ThreadPoolExecutor(4) as executor:
        for i in range(4):
            executor.submit(copy_file, i)
    end = time.time() - start
    print(f'多线程耗时：{end} 秒')
