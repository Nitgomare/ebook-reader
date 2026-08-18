# 定义一个Person类
class Person:
    # max_age、planet 他们都是类属性，类属性是保存在类身上的
    # 类属性可以通过类访问，也可以通过实例访问
    # 类属性通常用于保存：公共数据
    max_age = 120
    planet = '地球'

    # 初始化方法
    def __init__(self, name, age, gender):
        # 给实例添加属性
        self.name = name
        self.gender = gender
        # 限制age的最大值
        if age <= Person.max_age:
            self.age = age
        else:
            print(f'年龄超出范围了，已经将年龄设置为最大值：{Person.max_age}')
            self.age = Person.max_age

# 验证一下：类属性是保存在类身上的
# print(Person.__dict__)

# 创建Person类的实例对象
p1 = Person('张三', 18, '男')
p2 = Person('李四', 22, '女')

# 验证一下：实例身上是没有类属性的
# print(p1.__dict__)
# print(p2.__dict__)


# 验证一下：类属性可以通过类访问，也可以通过实例访问
# print(Person.max_age)
# print(p1.max_age)  # 查找max_age的过程：1.实例自身(p1)  => 2.实例的“缔造者”(Person)
# print(p2.planet)

# 测试一下年龄超出范围
# p3 = Person('王五', 170, '女')
# print(p3.__dict__)

# 注意点：进行【实例.属性名 = 值】操作时，只会对实例自身的属性起作用，不会影响类属性
p1.planet = '火星'
print(Person.__dict__)
print(p1.__dict__)
print(p2.__dict__)
print(p1.planet)
print(p2.planet)
