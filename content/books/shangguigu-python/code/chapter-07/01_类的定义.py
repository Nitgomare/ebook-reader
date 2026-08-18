# 定义一个Person类（类名通常使用：大驼峰写法）
class Person:
    # 说明：当一个函数被定义在了类中时，那这个函数就被称为：方法。
    # __init__方法：初始化方法，主要作用：给当前正在创建的实例对象添加属性
    # __init__方法收到的参数：当前正在创建的实例对象（self）、其它的自定义参数
    # 当我们以后编写代码去创建Person类实例的时候，Python会自动调用__init__方法
    def __init__(self, name, age, gender):
        # 给实例添加属性（语法为：self.属性名 = 值）
        self.name = name
        self.age = age
        self.gender = gender
