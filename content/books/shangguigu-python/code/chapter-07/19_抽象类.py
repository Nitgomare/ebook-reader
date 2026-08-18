from abc import ABC, abstractmethod

#【抽象类】是一种不能直接实例化的类，它通常作为“规范”，让子类去继承，并实现其中定义的【抽象方法】。
# MustRun类一旦继承了ABC类，那么MustRun类就是抽象类了
class MustRun(ABC):
    @abstractmethod
    def run(self):
        pass

    def speak(self):
        print(f'你好，我叫{self.name}')

class Person(MustRun):
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def run(self):
        print(f'我叫{self.name}，我在努力的奔跑')

p1 = Person('张三', 18, '男')
p1.run()
p1.speak()
