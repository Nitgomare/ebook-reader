# 多态的概念：同一个方法名，在不同的对象上调用时，能呈现出不同的行为。
# Python中支持：标准多态、鸭子多态
class Animal:
    def speak(self):
        print('动物正在发出声音！')

class Dog(Animal):
    def speak(self):
        print('汪汪汪！')

class Cat(Animal):
    def speak(self):
        print('喵喵喵！')

class Pig:
    def speak(self):
        print('哼哼哼！')

def make_sound(animal:Animal):  # 类型注解
    # 多态的体现
    animal.speak()

# 创建实例对象
a1 = Animal()
d1 = Dog()
c1 = Cat()
p1 = Pig()

make_sound(a1)
make_sound(d1)
make_sound(c1)
make_sound(p1) # 此行代码如果在其它语言中会报错，Python不会报错，不推荐这样写
