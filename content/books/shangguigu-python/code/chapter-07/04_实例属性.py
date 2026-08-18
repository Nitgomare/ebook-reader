# 定义一个Person类
class Person:
    # 初始化方法
    def __init__(self, name, age, gender):
        # 通过【实例.属性名 = 值】给实例添加的属性，就叫实例属性
        # 实例属性只能通过实例访问，不能通过类访问
        # 每个实例都有自己【独一份的】实例属性，各个实例之间是互不干扰的
        self.name = name
        self.age = age
        self.gender = gender

# 创建Person类的实例对象
p1 = Person('张三', 18, '男')
p2 = Person('李四', 22, '女')

# 实例属性只能通过实例访问，不能通过类访问
# print(p1.name)
# print(Person.name)
