# 概念：多重继承指一个类同时继承多个父类，从而拥有多个父类的属性和方法。
# 举例：就像孩子不仅继承爸爸的长相，也能继承妈妈的性格。
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    def speak(self):
        print(f'我叫{self.name}， 年龄是{self.age}， 性别是{self.gender}')

class Worker:
    def __init__(self, company):
        self.company = company
    def do_work(self):
        print(f'我在{self.company}做兼职')

class Student(Worker, Person):
    def __init__(self, name, age, gender, company, stu_id, grade):
        Person.__init__(self, name, age, gender)
        Worker.__init__(self, company)
        self.stu_id = stu_id
        self.grade = grade
    def study(self):
        print(f'我在努力的学习，争取做{self.grade}年级的第一名')

s1 = Student('张三', 18, '男', '麦当劳', '2025001', '初二')
print(s1.__dict__)
s1.speak()
s1.do_work()
s1.study()

# 类的__mro__属性：用于记录属性和方法的查找顺序
# 通过实例去查找属性或方法时，会先在实例自身上去查找，如果没有，就按照__mro__记录的顺序去查找
print(Student.__mro__)
