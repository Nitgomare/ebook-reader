# 定义函数（接收位置参数）
def greet(name, gender, age, height):
    print(f'我叫{name}，性别{gender}，年龄是{age}，身高是{height}cm')
    print(f'我的身高是{height}，今年{age}岁了，我叫{name}')

# 调用函数
greet('张三', '男', 18, 172)

# 错误示例
# greet('张三', 18, 172)
# greet('男', '张三', 172, 18)
