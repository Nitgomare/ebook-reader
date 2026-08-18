# 定义函数
def add(n1, n2):
    print(f'我收到了：{n1}、{n2}，二者相加是：{n1 + n2}')
    print('add函数执行完毕了')
    return n1 + n2

# 调用函数
result = add(100, 200)
print(result)

# print函数是没有返回值的
# res = print('hello')
# print(res)
