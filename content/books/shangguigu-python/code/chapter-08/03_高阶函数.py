# 高阶函数：当一个函数的『参数是函数』或者『返回值是函数』那该函数就是『高阶函数』。

# 高阶函数的意义：
# 1. 代码复用性高：可以把行为“独立出去”，传入不同函数实现不同逻辑。
# 2. 能让函数更灵活，更通用。
# 3. 高阶函数是：装饰器、闭包的基础。（后面会讲）

def info(msg):
    return '[提示]：' + msg

def warn(msg):
    return '[警告]：' + msg

def error(msg):
    return '[错误]：' + msg

def log(func, text):
    print(func(text))

log(info, '文件保存成功！')
log(warn, '磁盘空间不足！')
log(error, '该用户不存在！')
