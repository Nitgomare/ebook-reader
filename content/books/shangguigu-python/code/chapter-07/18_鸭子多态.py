# 核心理念：如果一个东西看起来像鸭子，叫起来也像鸭子，那它就是鸭子。
# 鸭子类型是一种编程风格，它不检查对象的类型，只关注对象能否“做某件事”（是否有对应的方法）。

# 鸭子多态
class Dog:
    def speak(self):
        print('汪汪汪！')

class Cat:
    def speak(self):
        print('喵喵喵！')

class Pig:
    def speak(self):
        print('哼哼哼！')

class Fish:
    def speak(self):
        print('咕噜噜！')

class Computer:
    def speak(self):
        print('滋滋滋！')

def make_sound(animal):
    animal.speak()

# 创建实例对象
d1 = Dog()
c1 = Cat()
p1 = Pig()
f1 = Fish()
cm1 = Computer()

make_sound(d1)
make_sound(c1)
make_sound(p1)
make_sound(f1)
make_sound(cm1)
