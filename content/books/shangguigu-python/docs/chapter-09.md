# 第 9 章 错误与异常

<a id="irG93"></a>

## 错误与异常

**错误**：代码本身有语法错误，解释器无法执行代码。———— **无法**通过异常处理机制解决。

```python
age = 18
if age >= 18
    print('成年人')
```

**异常：**代码在语法上没问题，但执行过程中出现了问题。———— **可以**通过异常处理机制解决。

```python
# 1.ZeroDivisionError：当除数为 0 时触发。
num1 = 100
num2 = 0
result = num1 / num2

# 2.TypeError：当操作的数据类型不正确或不兼容时触发。
result = '10' + 5

# 3.AttributeError: 当对象没有指定的属性或方法时触发。
# 演示1
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person('张三', 18)
print(p1.name)
print(p1.age)
print(p1.gender)

# 演示2
nums = [10, 20, 30]
nums.add(40)

# 4.IndexError：当索引超出范围（索引越界）时触发。
nums = [10, 20, 30, 40]
print(nums[4])

# 5.NameError：当使用了不存在的变量时触发。
print(school)

# 6.KeyError：当访问字典中不存在的 key 时触发。
person = {'name':'张三', 'age':18}
print(person['gender'])

# 7.ValueError：当值不合法，但类型正确时触发。
int('hello')
```

Python 中异常类的继承关系（层级关系）如下（了解即可）：

> 官方地址：[https://docs.python.org/zh-cn/3.13/library/exceptions.html#exception-hierarchy](https://docs.python.org/zh-cn/3.13/library/exceptions.html#exception-hierarchy)

其中：`BaseException`是所有异常类的父类，`Exception`中包含的是开发中常见的业务异常。

```plain
BaseException
├── BaseExceptionGroup
├── GeneratorExit
├── KeyboardInterrupt
├── SystemExit
└── Exception
├── ArithmeticError
│    ├── FloatingPointError
│    ├── OverflowError
│    └── ZeroDivisionError
├── AssertionError
├── AttributeError
├── BufferError
├── EOFError
├── ExceptionGroup [BaseExceptionGroup]
├── ImportError
│    └── ModuleNotFoundError
├── LookupError
│    ├── IndexError
│    └── KeyError
├── MemoryError
├── NameErrorburu
│    └── UnboundLocalError
├── OSError
│    ├── BlockingIOError
│    ├── ChildProcessError
│    ├── ConnectionError
│    │    ├── BrokenPipeError
│    │    ├── ConnectionAbortedError
│    │    ├── ConnectionRefusedError
│    │    └── ConnectionResetError
│    ├── FileExistsError
│    ├── FileNotFoundError
│    ├── InterruptedError
│    ├── IsADirectoryError
│    ├── NotADirectoryError
│    ├── PermissionError
│    ├── ProcessLookupError
│    └── TimeoutError
├── ReferenceError
├── RuntimeError
│    ├── NotImplementedError
│    ├── PythonFinalizationError
│    └── RecursionError
├── StopAsyncIteration
├── StopIteration
├── SyntaxError
│    └── IndentationError
│         └── TabError
├── SystemError
├── TypeError
├── ValueError
│    └── UnicodeError
│         ├── UnicodeDecodeError
│         ├── UnicodeEncodeError
│         └── UnicodeTranslateError
└── Warning
├── BytesWarning
├── DeprecationWarning
├── EncodingWarning
├── FutureWarning
├── ImportWarning
├── PendingDeprecationWarning
├── ResourceWarning
├── RuntimeWarning
├── SyntaxWarning
├── UnicodeWarning
└── UserWarning
```

<a id="Ji9d6"></a>

## 异常处理

<a id="szsU8"></a>

### 1️⃣为什么要进行异常处理

- 程序运行过程中出现的异常，如果得不到处理，那程序就会立即崩溃，导致后续代码无法执行。
- 异常处理不是让异常消失，而是将异常捕获到，随后根据异常的具体情况，来执行指定的逻辑。

```python
print('欢迎使用本程序')
a = int(input('请输入第一个数：'))
b = int(input('请输入第二个数：'))
result = a / b
print(f'{a}除以{b}的结果是：{result}')
print('***我是后续的其它逻辑1***')
print('***我是后续的其它逻辑2***')
```

<a id="aAiEd"></a>

### 2️⃣异常处理（初级）

核心规则如下：

> 1. 将可能出现异常的代码放在`try`中，出现异常后的处理代码写在`except`中。
> 2. 如果`try`中的代码出现异常，那`try`中的后续代码不会执行，并自动跳转到`except`中。
> 3. 如果`try`中的代码没有异常，那`except`中的代码就不会执行。
> 4. 无论是否发生异常，`try-except`后面的代码都会继续执行。
> 5. 直接写`except`捕获到`Python`中所有的异常 ———— 实际开发中不推荐这样做。

```python
print('欢迎使用本程序')
try:
    a = int(input('请输入第一个数：'))
    b = int(input('请输入第二个数：'))
    result = a / b
    print(f'{a}除以{b}的结果是：{result}')
except:
    print('抱歉，程序出现了异常！')
print('***我是后续的其它逻辑1***')
print('***我是后续的其它逻辑2***')
```

<a id="n9u1y"></a>

### 3️⃣捕获指定的类型的异常

```python
print('欢迎使用本程序')
try:
    a = int(input('请输入第一个数：'))
    b = int(input('请输入第二个数：'))
    result = a / b
    print(f'{a}除以{b}的结果是：{result}')
except ZeroDivisionError:
    print('程序异常：0不能作为除数！')
except ValueError:
    print('程序异常：您输入的必须是数字！')
print('***我是后续的其它逻辑1***')
print('***我是后续的其它逻辑2***')
```

<a id="ay4A5"></a>

### 4️⃣验证异常类之间的继承关系

```python
print(issubclass(ZeroDivisionError, ArithmeticError))
print(issubclass(ZeroDivisionError, Exception))
print(issubclass(ValueError, Exception))
print(issubclass(KeyboardInterrupt, Exception))
print(issubclass(KeyboardInterrupt, BaseException))
```

<a id="ZmvRS"></a>

### ️5️⃣多个 except

多个`except`从上往下匹配，匹配成功后不再向下匹配。

```python
print('欢迎使用本程序')
try:
    a = int(input('请输入第一个数：'))
    b = int(input('请输入第二个数：'))
    print(x)
    result = a / b
    print(f'{a}除以{b}的结果是：{result}')
except ZeroDivisionError:
    print('程序异常：0不能作为除数！')
except ValueError:
    print('程序异常：您输入的必须是数字！')
except Exception:
    print('程序异常!')
print('***我是后续的其它逻辑1***')
print('***我是后续的其它逻辑2***')
```

<a id="iLCt7"></a>

### 6️⃣获取异常的具体信息

> 备注：通过`e`变量，可以获取异常相关的信息，也可以借助`traceback`去格式化异常信息。

```python
print('欢迎使用本程序')
try:
    a = int(input('请输入第一个数：'))
    b = int(input('请输入第二个数：'))
    print(x)
    result = a / b
    print(f'{a}除以{b}的结果是：{result}')
except ZeroDivisionError:
    print('程序异常：0不能作为除数！')
except ValueError:
    print('程序异常：您输入的必须是数字！')
except Exception as e:
    print(f'⚠程序异常，异常信息：{e}')
    print(f'⚠程序异常，异常类型：{type(e)}')
    print(f'⚠程序异常，异常参数：{e.args}')
    print(f'⚠程序异常，异常的文件：{e.__traceback__.tb_frame.f_code.co_filename}')
    print(f'⚠程序异常，异常的具体行数：{e.__traceback__.tb_lineno}')
    # 通过 traceback 来回溯异常
    # import traceback
    # print(traceback.format_exc())
print('***我是后续的其它逻辑1***')
print('***我是后续的其它逻辑2***')
```

<a id="pZOJl"></a>

### 7️⃣一个 except 捕获不同的异常

```python
print('欢迎使用本程序')
try:
    a = int(input('请输入第一个数：'))
    b = int(input('请输入第二个数：'))
    print(x)
    result = a / b
    print(f'{a}除以{b}的结果是：{result}')
except (ZeroDivisionError, ValueError, Exception) as e:
    if isinstance(e, ZeroDivisionError):
        print('程序异常：0不能作为除数！')
    elif isinstance(e, ValueError):
        print('程序异常：您输入的必须是数字！')
    else:
        print(f'程序异常：{e}')
print('***我是后续的其它逻辑1***')
print('***我是后续的其它逻辑2***')
```

<a id="vCMzZ"></a>

### 8️⃣完整写法

> 1. `try`：尝试去做可能会出现异常的事情。
> 2. `except`：出现异常时的处理（出现异常时怎么补救）。
> 3. `else`：如果一切顺利（没有异常出现）要做的事。
> 4. `finall`：无论有没有异常，都要做的事。

```python
print('欢迎使用本程序')
try:
    a = int(input('请输入第一个数：'))
    b = int(input('请输入第二个数：'))
    result = a / b
    print(f'{a}除以{b}的结果是：{result}')
except (ZeroDivisionError, ValueError, Exception) as e:
    if isinstance(e, ZeroDivisionError):
        print('程序异常：0不能作为除数！')
    elif isinstance(e, ValueError):
        print('程序异常：您输入的必须是数字！')
    else:
        print(f'程序异常：{e}')
else:
    print('挺好的，try中的代码没有任何异常！')
finally:
    print('无论有没有异常，我的计算都结束了！')
print('***我是后续的其它逻辑1***')
print('***我是后续的其它逻辑2***')
```

<a id="pocZM"></a>

## 手动抛出异常

当程序遇到不符合预期情况时，可以使用`raise`语句手动触发（抛出）异常。

```python
print('欢迎使用年龄判断系统')
try:
    age = int(input('请输入你的年龄：'))
    if 18 <= age <= 120:
        print('成年')
    elif 0 <= age < 18:
        print('未成年')
    else:
        # print('输入的年龄有误！（年龄应该为0~120的整数）')
        raise ValueError('年龄应该为0~120的整数')
except Exception as e:
    print(f'程序异常：{e}')
```

<a id="JuGBl"></a>

## 异常的传递机制

1. 如果异常没有被当前代码块所捕获处理，那该异常就会沿着调用链，逐层传递给其调用者。
2. 如果所有调用者，都没有捕获该异常，那最终程序将因【未处理异常】而意外终止。

```python
def test1():
    print('**test1开始**')
    result = '100' + 100
    print('**test1结束**')

def test2():
    print('**test2开始**')
    try:
        test1()
    except Exception as e:
        print(f'程序异常：{e}')
    print('**test2结束**')

def test3():
    print('**test3开始**')
    test2()
    print('**test3结束**')

test3()
```

执行以上代码，控制最终会输出

```plain
**test3开始**
**test2开始**
**test1开始**
程序异常：can only concatenate str (not "int") to str
**test2结束**
**test3结束**
```

<a id="UGV0N"></a>

## 自定义异常类

1. 由开发人员自己定义一个异常类，用来表示代码中“更具体、更有业务含义”的异常。
2. 具体规则：定义一个类（类名通常以`Error`结尾），继承`Exception`类或它的子类。

```python
class SchoolNameError(Exception):
    def __init__(self, msg):
        super().__init__('【校名异常】' + msg)

def check_school_name(name):
    if len(name) > 10:
        raise SchoolNameError('学校名过长')
    else:
        print('学校名是合法的')

try:
    check_school_name('atguiguuuuuuuuuuuuuuu')
except SchoolNameError as e:
    print(f'程序异常：{e}')
```

<a id="e37ef"></a>
