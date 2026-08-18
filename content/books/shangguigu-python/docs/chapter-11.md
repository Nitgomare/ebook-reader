# 第 11 章 迭代器 vs 生成器

<a id="CAnpo"></a>

## 迭代器

先区分两个概念：可迭代对象（iterable）、迭代器（iterator）

<a id="rPSwZ"></a>

### 1️⃣可迭代对象（iterable）

概念：能被 for 循环遍历的对象，就是可迭代对象（iterable）

如下这些都是可迭代对象（iterable）：

```python
names = ['张三', '李四', '王五']
citys = ('北京', '上海', '深圳')
msg = 'hello'

for item in names:
    print(item)
```

如下这些不是可迭代对象（iterable）：

```python
age = 10
def test():
    pass

for item in test:
    print(item)
endregion
```

可迭代对象都拥有`__iter__`方法。

```python
names = ['张三', '李四', '王五']
citys = ('北京', '上海', '深圳')
msg = 'hello'
age = 10
def test():
    pass

names.__iter__()
citys.__iter__()
msg.__iter__()

print(hasattr(names, '__iter__'))
print(hasattr(citys, '__iter__'))
print(hasattr(msg, '__iter__'))
print(hasattr(age, '__iter__'))
print(hasattr(test, '__iter__'))
```

<a id="Q1sjt"></a>

### 2️⃣迭代器（iterator）

调用`__iter__`方法会得到：迭代器(iterator)

- 备注1：`__iter__`是一个魔法方法，当调用`iter`函数时，`__iter__`会自动调用。
- 备注2：`可迭代对象.__iter__()` 等价于： `iter(可迭代对象)`。
- 备注3：如果`iter(obj)`能得到一个迭代器(iterator)，那`obj`就是可迭代对象。

```python
names = ['张三', '李四', '王五']
citys = ('北京', '上海', '深圳')
msg = 'hello'

print(names.__iter__())
print(citys.__iter__())
print(msg.__iter__())

print(iter(names))
print(iter(citys))
print(iter(msg))
```

迭代器（iterator）拥有`__next__`方法，每次调用都会根据当前的状态，返回下一个元素。

- 备注1：`迭代器.__next__()` 等价于 `next(迭代器)`。
- 备注2：当所有元素全都取出后，若继续调用`__next__`，Python会抛出`StopIteration`异常。

```python
names = ['张三', '李四', '王五']
it = iter(names)
print(it.__next__())
print(it.__next__())
print(it.__next__())
print(it.__next__())

print(next(it))
print(next(it))
print(next(it))
print(next(it))
```

编写`for`循环遍历`names`列表

```python
names = ['张三', '李四', '王五']
for item in names:
    print(item)
```

`for`循环背后的逻辑

```python
names = ['张三', '李四', '王五']
# 1️⃣调用【可迭代对象的__iter__方法】获取到一个迭代器(iterator)
it = iter(names)
# 2️⃣开启一个无限循环
while True:
    try:
        # 3️⃣调用__next__方法，获取下一个元素
        item = next(it)
        print(item)
    except StopIteration:
        # 4️⃣捕获 StopIteration 异常，随后结束循环
        break
```

迭代器（iterator）也拥有`__iter__`方法，并且其返回值是迭代器自身。

> 这么设计的原因：让 for 循环也能遍历迭代器（即：为了让 iter(迭代器) 不出错）。

```python
names = ['张三', '李四', '王五']

it = iter(names)
print(it)

result = iter(it)
print(result)

x = iter(result)
print(x)

it = iter(names)
for item in it:
    print(item)
```

> 迭代器协议：一个对象如果同时满足如下规范，那该对象就是一个迭代器：
>
> 1. 能被`iter()`接受。
> 2. 能被`next()`一步一步取值。

迭代器是一次性的，状态只会向前推进，且不会自动重置（迭代器在遍历的过程中会被“消耗”）。

```python
names = ['张三', '李四', '王五']
it1 = iter(names)
it2 = iter(names)

print(it1)
print(it2)

print(next(it1))
print(next(it1))
print(next(it1))
print(next(it1)) # 此行代码会抛出异常，因为此时迭代器已经被耗尽了

# 如想重新依次获取元素，需要使用新的迭代器it2
print(next(it2))
print(next(it2))
print(next(it2))
```

<a id="spJnC"></a>

### 3️⃣迭代器的应用

需求：让`for`循环可以遍历`Person`的实例对象。

实现方式1️⃣：

```python
class Person:
    def __init__(self, name, age, gender, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    def __iter__(self):
        return PersonIterator(self)

class PersonIterator:
    def __init__(self, p):
        # 将外部传进来的数据保存好
        self.p = p
        # 设置迭代器的初始化状态（指针位置）
        self.index = 0
        # 配置好要遍历的内容
        self.attrs = [p.name, p.age, p.gender, p.address]

    # 迭代器的__iter__方法会返回迭代器自身
    def __iter__(self):
        return self

    # 每次调用__next__方法，会根据当前的状态，返回下一个元素
    def __next__(self):
        # 如果指针的位置超出范围，那就抛出StopIteration异常
        if self.index >= len(self.attrs):
            raise StopIteration
        # 获取要返回的内容
        value = self.attrs[self.index]
        # 更新迭代器状态（指针位置）
        self.index += 1
        # 返回value
        return value

# 目标：
p1 = Person('张三', 18, '男', '北京昌平')

for item in p1:
    print(item)

for item in p1:
    print(item)
```

实现方式2️⃣

```python
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
        # 更新迭代器状态（指针位置）
        self.__index += 1
        # 返回value
        return value

# 目标：
# 下面的p1既是可迭代对象，又是迭代器
p1 = Person('张三', 18, '男', '北京昌平')

for item in p1:
    print(item)

for item in p1:
    print(item)
```

进阶：迭代器玩的就是`__next__`

```python
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
```

<a id="fXuI6"></a>

### 4️⃣迭代器的优势

1. 迭代器是惰性计算，不会一次性生成所有结果，所以能显著降低内存占用。
2. 当数据量很大，不确定要用多少结果时，推荐使用迭代器。

使用迭代器实现【斐波那契数列】：

```python
class Fibo:
    def __init__(self, total):
        # 要生成多少个数
        self.total = total
        # 当前生成到第几个了（计数器，指针）
        self.index = 0
        # 初始的两个值
        self.pre = 1
        self.cur = 1

    def __iter__(self):
        return self

    def __next__(self):
        # 当生成足够数量后，抛出StopIteration异常
        if self.index >= self.total:
            raise StopIteration
        # 前两项都是1
        if self.index < 2:
            value = 1
        else:
            # 新的结果等于前两项的和
            value = self.pre + self.cur
            # 更新一下pre和cur
            self.pre = self.cur
            self.cur = value
        # 计数器+1
        self.index += 1
        # 返回value
        return value
```

不使用迭代器实现【斐波那契数列】：

```python
def fibo(total):
    if total <= 0:
        return []
    if total == 1:
        return [1]
    nums = [1, 1]
    for i in range(2, total):
        nums.append(nums[-1] + nums[-2])
    return  nums
```

分析内存占用情况：

> 分别运行如下两段代码后，会发现迭代器实现明显节约内存。

```python
tracemalloc.start()
f1 = Fibo(0)
m = tracemalloc.get_traced_memory()[1]
print(f'内存占用是：{m / 1024 / 1024}MB')
```

```python
tracemalloc.start()
f1 = fibo(0)
m = tracemalloc.get_traced_memory()[1]
print(f'内存占用是：{m / 1024 / 1024}MB')
```

<a id="rufbh"></a>

## 生成器

<a id="KEbkX"></a>

### 1️⃣两个概念

1. 生成器函数：函数体中如果出现了`yield`关键字，那该函数是『生成器函数』。
2. 生成器对象：调用『生成器函数』时，其函数体不会立刻执行，而是返回一个『生成器对象』。

> 备注：不管能否执行到`yield`所在的位置，只要函数中有`yield`，那该函数就是『生成器函数』。

```python
def demo():
    print('demo函数开始执行了')
    print(100)
    yield
    a = 200
    print(a)

d = demo()
print(d)
```

<a id="DttrE"></a>

### 2️⃣几个细节

写在『生成器函数』中的代码，需要通过『生成器对象』来执行：

> 1. 调用『生成器对象』的`__next__`方法，会让『生成器函数』中的代码开始执行。
> 2. 当『生成器函数』中的代码开始执行后，遇到`yield`会“暂停”，并会记录“暂停”的位置。
> 3. 后续调用`__next__`方法时，都会从上一次“暂停”的位置，继续运行，直到再次遇到 yield。
> 4. 遇到`return`会抛出`StopIteration`异常，并将`return`后面的表达式，作为异常信息。
> 5. `yield`后面所写的表达式，会作为本次`__next__`方法的返回值。

```python
def demo():
    print('demo函数开始执行了')
    print(100)
    yield '我是第1个yield所返回的数据'
    a = 200
    print(a)
    yield '我是第2个yield所返回的数据'
    b = 300
    print(b)
    return '尚硅谷'

d = demo()
r1 = next(d)
print(r1)
r2 = next(d)
print(r2)
try:
    next(d)
except StopIteration as e:
    print(e)
```

生成器对象是一种特殊的迭代器（本质是通过`yield`自动实现了迭代器协议）

```python
def demo():
    print('demo函数开始执行了')
    print(100)
    yield '我是第1个yield所返回的数据'
    a = 200
    print(a)
    yield '我是第2个yield所返回的数据'
    b = 300
    print(b)
    return '尚硅谷'

d = demo()
# 验证：生成器对象d，和迭代器一样，也拥有：__iter__  和 __next__ 方法
print(hasattr(d, '__iter__'))
print(hasattr(d, '__next__'))

# 验证：生成器对象的__iter__方法，和迭代器一样，返回的也是自身
result = iter(d)
print(result == d)

# for循环遍历生成器
for item in d:
    print(item)

# for循环背后的逻辑
gen = iter(d)
while True:
    try:
        value = next(gen)
        print(value)
    except StopIteration:
        break
```

`yield`也能写在循环里

```python
region
def create_car(total):
    for index in range(1, total + 1):
        yield f'我是第{index}台车'

# cars是生成器对象
cars = create_car(5)

# 调用一次cars的__next__方法，就会得到一台车
c1 = next(cars)
print(c1)
c2 = next(cars)
print(c2)
c3 = next(cars)
print(c3)
c4 = next(cars)
print(c4)
c5 = next(cars)
print(c5)

for car in cars:
    print(car)
endregion
```

`yield from`能把一个『可迭代对象』里的东西依次`yield`出去。(替代：`for + yield`)

```python
def demo():
    nums = [10, 20, 30, 40]
    yield from nums

d = demo()
r1 = next(d)
print(r1)
r2 = next(d)
print(r2)
r3 = next(d)
print(r3)
r4 = next(d)
print(r4)

for item in d:
    print(item)
```

使用：`生成器.send(值)` 可以让生成器继续执行的同时，给上一次`yield`传值。

> 备注1：`next`只能取值，`send`既能取值，也能送值。
>
>
>
> 备注2：第一次启动生成器，不能传值！（或者说只能传 None 值）

```python
def demo():
    print('demo函数开始执行了')
    print(100)
    a = yield '我是第1个yield所返回的数据'
    print(a)
    b = yield '我是第2个yield所返回的数据'
    print(b)
    return '尚硅谷'

d = demo()
r1 = next(d) # 此处等价于 d.send(None)
print(r1)
r2 = d.send(666)
print(r2)
try:
    d.send(888)
except StopIteration as e:
    print(e)
```

<a id="si9o9"></a>

### 3️⃣生成器的应用

用生成器实现遍历`Person`类的实例对象：

```python
class Person:
    def __init__(self, name, age, gender, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address
        self.__attr = [name, age, gender, address]

    def __iter__(self):
        # yield self.name
        # yield self.age
        # yield self.gender
        # yield self.address
        yield from self.__attr

p1 = Person('张三', 18, '男', '北京昌平')
# 目标：
for attr in p1:
    print(attr)
```

用生成器实现斐波那契数列：

```python
def fibo(total):
    pre = 1
    cur = 1

    for index in range(total):
        if index < 2:
            yield 1
        else:
            value = pre + cur
            pre = cur
            cur = value
            yield value

f1 = fibo(10)

for item in f1:
    print(item)
```

无论是迭代器，还是生成器对象，都可以用`list`、`tuple`、`set`等直接拿到其里面的所有内容（注意：如果数据量很大，可能会挤爆内存）

```python
def fibo(total):
    pre = 1
    cur = 1

    for index in range(total):
        if index < 2:
            yield 1
        else:
            value = pre + cur
            pre = cur
            cur = value
            yield value

f1 = fibo(10)

result = set(f1)
print(result)
```

<a id="Uzwx3"></a>

### 4️⃣生成器表达式

生成器表达式：一种用类似列表推导式的语法，快速创建生成器对象的方式。

语法格式：`(表达式 for 变量 in 可迭代对象)`。

什么时候适合用生成器表达式？———— 当“每个结果，只依赖当前这一个元素”时。

```python
nums = [10, 20, 30, 40]

# 列表推导式
result1 = [n * 2 for n in nums]
print(result1)

# 生成器表达式（和列表推导式很像，不要搞混）
result2 = (n * 2 for n in nums)

for item in result2:
    print(item)
```

<a id="m78zI"></a>
