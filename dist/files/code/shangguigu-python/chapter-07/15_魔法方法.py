# 概念：以 __xxx__ 命名的特殊方法（双下划线开头和结尾）。
# 特点：不需要我们手动调，我们只要准备好这些方法，Python会在特定场景下，去自动调用。

class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    # 当执行print(Person的实例对象) 或 str(Person的实例对象) 时调用
    def __str__(self):
        return f'{self.name}-{self.age}-{self.gender}'

    # 当执行len(Person的实例对象) 时调用
    def __len__(self):
        return len(p1.__dict__)

    # 当执行 Person实例对象1 < Person实例对象2 时调用
    def __lt__(self, other):
        return self.age < other.age

    # 当执行 Person实例对象1 > Person实例对象2 时调用
    def __gt__(self, other):
        return self.age > other.age

    # 当执行 Person实例对象1 == Person实例对象2 时调用
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # 当访问Person实例对象身上不存在的属性时调用
    def __getattr__(self, item):
        return f'您访问的{item}属性不存在'

p1 = Person('张三', 22, '男')
p2 = Person('李四', 22, '男')
# print(p1)
# print(p2)
# res = len(p1)
# print(res)
# print(p1 < p2)
# print(p1 > p2)
# print(p1 == p2)
print(p1.address)
