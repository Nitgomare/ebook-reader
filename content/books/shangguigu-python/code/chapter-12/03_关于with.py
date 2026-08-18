# 1.Python 中的 with 主要用于管理程序中“需要成对出现的操作”，例如：
#    🔸上锁 / 解锁
#    🔸打开 / 关闭
#    🔸借用 / 归还

# 2.最终目标：编码者只管做具体的事，“进入”和“离开”的事，让 Python 自动处理。

# 3.语法格式如下：
#   with 能得到一个上下文管理器的表达式 as 变量:
#       具体的事1
#       具体的事2
#       具体的事3

# 4.上下文管理器协议：
#    (1). __enter__ 方法：with 中的代码执行【之前】调用，其返回值会赋值给 as 后的变量。
#    (2). __exit__  方法：with 中的代码执行【结束后】调用（无论是 with 中否出现异常都会调用）。

# 定义一个 Person 类，让其实例对象遵循：上下文管理器协议
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f'我叫{self.name}，年龄是{self.age}')

    def __enter__(self):
        print('-----我是进入的逻辑-----')
        return self

    # 当 with 中的代码发生异常时，__exit__ 方法的返回值规则如下：
    #   🔸返回“真”：表示异常【已经】被处理，异常【不会】被继续抛出。
    #   🔸返回“假”：表示异常【没有】被处理，异常【会】被继续抛出。
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('-----我是离开的逻辑-----')
        # exc_type  : 异常类型
        # exc_val   : 异常对象
        # exc_tb    : 异常追踪信息
        if exc_type:
            print(f'异常类型：{exc_type}')
            print(f'异常对象：{exc_val}')
            print(f'异常追踪信息：{exc_tb}')
        return True

# 1.计算 with 后面的表达式，得到一个『上下文管理器』。
# 2.调用『上下文管理器』的 __enter__() 方法，并将其返回值赋给 as 后面的变量。
# 3.执行 with 所管理的代码。
# 4.无论代 with 中的代码，是正常结束，还是发生异常，都会自动调用『上下文管理器』的 __exit__ 方法。

with Person('张三', 18) as p1:
    p1.speak()
    # p1.study()
    print(666)
