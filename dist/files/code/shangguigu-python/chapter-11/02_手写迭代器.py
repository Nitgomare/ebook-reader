# 迭代器是一次性的，状态只会向前推进，且不会自动重置（迭代器在遍历的过程中会被“消耗”）。
# region
# names = ['张三', '李四', '王五']
# it1 = iter(names)
# it2 = iter(names)

# print(it1)
# print(it2)

# print(next(it1))
# print(next(it1))
# print(next(it1))

# print(next(it2))
# print(next(it2))
# print(next(it2))

# for item in it1:
#     print(item)
#
# for item in it2:
#     print(item)
# endregion

# 需求：让for循环可以遍历Person的实例对象
# 实现方式1️⃣
# region
# class Person:
#     def __init__(self, name, age, gender, address):
#         self.name = name
#         self.age = age
#         self.gender = gender
#         self.address = address
#
#     def __iter__(self):
#         return PersonIterator(self)
#
# class PersonIterator:
#     def __init__(self, p):
#         # 将外部传进来的数据保存好
#         self.p = p
#         # 设置迭代器的初始化状态（指针位置）
#         self.index = 0
#         # 配置好要遍历的内容
#         self.attrs = [p.name, p.age, p.gender, p.address]
#
#     # 迭代器的__iter__方法会返回迭代器自身
#     def __iter__(self):
#         return self
#
#     # 每次调用__next__方法，会根据当前的状态，返回下一个元素
#     def __next__(self):
#         # 如果指针的位置超出范围，那就抛出StopIteration异常
#         if self.index >= len(self.attrs):
#             raise StopIteration
#         # 获取要返回的内容
#         value = self.attrs[self.index]
#         # 更新迭代器状态（指针位置）
#         self.index += 1
#         # 返回value
#         return value
#
# # 目标：
# p1 = Person('张三', 18, '男', '北京昌平')
#
# for item in p1:
#     print(item)
#
# for item in p1:
#     print(item)
# endregion

# 实现方式2️⃣
# region
# class Person:
#     def __init__(self, name, age, gender, address):
#         self.name = name
#         self.age = age
#         self.gender = gender
#         self.address = address
#         # 设置迭代器的初始化状态（指针位置）
#         self.__index = 0
#         # 配置好要遍历的内容
#         self.__attrs = [name, age, gender, address]
#
#     def __iter__(self):
#         self.__index = 0
#         return self
#
#     def __next__(self):
#         # 如果指针的位置超出范围，那就抛出StopIteration异常
#         if self.__index >= len(self.__attrs):
#             raise StopIteration
#         # 获取要返回的内容
#         value = self.__attrs[self.__index]
#         # 更新迭代器状态（指针位置）
#         self.__index += 1
#         # 返回value
#         return value
#
# # 目标：
# # 下面的p1既是可迭代对象，又是迭代器
# p1 = Person('张三', 18, '男', '北京昌平')
#
# for item in p1:
#     print(item)
#
# for item in p1:
#     print(item)
# endregion

# 进阶：迭代器玩的就是__next__
from cn2an import an2cn
class Person:
    def __init__(self, name, age, gender, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address
        # 设置迭代器的初始化状态（指针位置）
        self.__index = 0
        # 配置好要遍历的内容
        self.__attrs = [name, age, gender, address]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        # 如果指针的位置超出范围，那就抛出StopIteration异常
        if self.__index >= len(self.__attrs):
            raise StopIteration
        # 获取要返回的内容
        value = self.__attrs[self.__index]
        # 将字符串转为大写
        if isinstance(value, str):
            value = value.upper()
        # 将数字转为汉语形式
        if isinstance(value, int):
            value = an2cn(value)
        # 更新迭代器状态（指针位置）
        self.__index += 1
        # 返回value
        return value

# 目标：
# 下面的p1既是可迭代对象，又是迭代器
p1 = Person('zhangsan', 18, '男', '北京昌平')

for item in p1:
    print(item)
