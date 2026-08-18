# Python 中，所有的类都继承了 object 类，即：object 类是所有类的顶层父类。
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

# 验证一下：所有的类继承了object类
# print(issubclass(Person, object))
# print(issubclass(int, object))
# print(issubclass(str, object))
# print(issubclass(list, object))
# print(issubclass(bool, object))
# print(issubclass(tuple, object))

# 因为 object 是所有类的父类，所以 Python 中的所有对象，都间接是 object 类的实例。
# p1 = Person('张三', 18, '男')
# print(isinstance(p1, object))
# print(isinstance(100, object))
# print(isinstance('hello', object))
# print(isinstance(True, object))
# print(isinstance(None, object))
# print(isinstance([10, 20, 30], object))
# print(isinstance({'吃饭','睡觉'}, object))

# 所有对象都继承了object类所提供的：各种属性和方法，从而保证了每个对象都具备统一的基本能力
# for key in object.__dict__:
#     print(key)

p1 = Person('张三', 18, '男')
print(p1.__dict__)  # 对象身上自己的东西
print(dir(p1))      # 对象可以访问到的东西（自己的、继承过来的）

print(p1.__str__())
print(p1)
