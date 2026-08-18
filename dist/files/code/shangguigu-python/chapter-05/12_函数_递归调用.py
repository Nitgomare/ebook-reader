# 使用递归打印n次“你好啊”（从大到小）
def welcome(n):
    print(f'你好啊{n}')
    if n > 1:
        welcome(n - 1)
# 调用函数
welcome(5)

# 使用递归打印n次“你好啊”（从小到大）
def welcome(n):
    if n > 1:
        welcome(n - 1)
    print(f'你好啊{n}')
# 调用函数
welcome(5)
