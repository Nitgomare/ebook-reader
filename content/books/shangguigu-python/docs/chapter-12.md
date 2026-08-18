# 第 12 章 文件操作

<!-- bilibili-playlist:start -->
<details class="chapter-videos" markdown="1">
<summary><strong>本章配套视频 · P136–P141（6 集）</strong></summary>

视频来自尚硅谷 Python 零基础教程；点击分 P 标题可直接播放对应内容。

- [P136 · 136_文件操作_前序知识](https://www.bilibili.com/video/BV1tDsgzxECr?p=136)
- [P137 · 137_文件操作_读取文件](https://www.bilibili.com/video/BV1tDsgzxECr?p=137)
- [P138 · 138_关于with](https://www.bilibili.com/video/BV1tDsgzxECr?p=138)
- [P139 · 139_文件操作_写入文件](https://www.bilibili.com/video/BV1tDsgzxECr?p=139)
- [P140 · 140_目录操作](https://www.bilibili.com/video/BV1tDsgzxECr?p=140)
- [P141 · 141_文件操作_小练习](https://www.bilibili.com/video/BV1tDsgzxECr?p=141)

</details>
<!-- bilibili-playlist:end -->

<a id="QwQAx"></a>

## 文件的分类

<a id="mphfQ"></a>

### 1️⃣**纯文本文件**

> 1. 读取和存储时，要遵循某种『字符编码』规范（如：UTF-8 等）进行编码和解码，最终以『二进制』的形式存储。
> 2. 『纯文本文件』最终会呈现为：可以直接阅读的文本信息。
> 3. 常见的『纯文本文件』有：`.txt` `.py` `.md` `.html` 等。

<a id="BJY8H"></a>

### 2️⃣**二进制文件**

> 1. 读取和存储时，不涉及字符编码，会按照某种『文件格式规范』把内容转为『二进制』进行存储。
> 2. 二进制文件需要由『能够识别其格式的软件』进行解析，最终的呈现形式多种多样（音频、视频、图像、幻灯片等）。
> 3. 常见的二进制文件有：`.mp3` `.mp4` `.doc` `.ppt` `.jpg` `.png` 等。

<a id="jyIm4"></a>

## 绝对路径 vs 相对路径

<a id="RA5Rg"></a>

### 1️⃣**绝对路径：**

从文件系统的『根目录』开始，完整描述文件或目录所在的位置。

> 举例：`D:/demo/test/a.txt`​

<a id="N2gX0"></a>

### **2️⃣相对路径：**

以当前『工作目录』为参照，描述目标文件或目录相对于它的位置。

> 举例：`../../a.txt`（其中`..`表示上一级目录）

<a id="T7TXe"></a>

## Python 中操作文件的标准流程

标准流程成如下：

> 1. 创建『文件对象』
> 2. 操作文件（读取、写入 等）
> 3. 关闭文件

文件操作的核心 —— `open`函数

> `open`函数最常用的三个参数如下：
>
> 1. `file`：要操作的文件路径
> 2. `mode`：文件的打开模式
>
>
>
> `r` ：读取（默认值）
>
>
>
> `w` ：写入，并先截断文件
>
>
>
> `x` ：排它性创建，如果文件已存在，则创建失败
>
>
>
> `a` ：打开文件用于写入，如果文件存在，则在文件末尾追加内容
>
>
>
> `b` ：二进制模式
>
>
>
> `t` ：文本模式（默认值）
>
>
>
> `+` ：打开用于更新（读取与写入）
>
> 1. `encoding`：字符编码

<a id="vjhSJ"></a>

## 读取文件

<a id="ibyzs"></a>

### 1️⃣`read`方法

- **概述：**使用『文件对象』的`read`方法，读取文件中的内容。
- **方法说明：**

> 1. `read(size)`中的`size`是可选参数。
>
>
>
> 🔸若不传递`size`参数，表示：读取文件中所有的内容（注意内存占用！）。
>
>
>
> 🔸若传递了`size`参数，表示：读取文件中指定个数的字符，或指定大小的字节。
>
> 1. `read`会从上一次`read`的位置继续读取，若到达文件末尾后继续读取，将返回空字符串。

- **示例代码：**

```python
# 第一步：创建『文件对象』
# 完整写法
# file = open(file='a.txt', mode='rt', encoding='utf-8')

# 简写
file = open('a.txt', 'rt', encoding='utf-8')

# 使用绝对路径读取
# file = open('D:/test/atguigu.txt', 'rt', encoding='utf-8')

# 读取二进制文件
# file = open('D:/test/girl.jpg', 'rb')

# 第二步：操作文件（读取）
# 多次调用read去逐步读取文件
r1 = file.read(2)
r2 = file.read(3)
r3 = file.read(4)
r4 = file.read()
print(r1, end='')
print(r2, end='')
print(r3, end='')
print(r4, end='')

# 用循环配合多次read（对内存友好）
while True:
    result = file.read(10)
    if result == '':
        break
    print(result, end='')

# 第三步：关闭文件
file.close()
```

<a id="jl3JY"></a>

### 2️⃣`readline`方法

- **概述：**使用文件对象的`readline`方法，读取文件中的一行。
- **方法说明：**

> 1. `readline(size)`中的`size`是可选参数。
>
>
>
> 🔸若不传递`size`参数，表示：读取当前这一行所有的内容。
>
>
>
> 🔸若传递了`size`参数，表示：表示读取当前行时，最多能读取的字符数，或字节数
>
>
>
> 🔸注意：`size`不是行数。
>
> 1. `readline`方法，也是从上一次位置继续读取，若到达文件末尾后继续读取，返回空字符串。

- **示例代码：**

```python
# 第一步：创建『文件对象』
file = open('a.txt', 'rt', encoding='utf-8')

# 第二步：操作文件（读取）
# 依次调用readline逐行读取
r1 = file.readline()
r2 = file.readline()
r3 = file.readline()
r4 = file.readline()
print(r1.strip())
print(r2.strip())
print(r3.strip())
print(r4.strip())

# 通过循环配合readline逐行读取
while True:
    line = file.readline()
    if line == '':
        break
    # print(line.strip())
    print(line, end='')

# 第三步：关闭文件
file.close()
```

<a id="N2Sf8"></a>

### 3️⃣for 循环遍历文件对象

- **概述：**可以使用`for`循环直接遍历文件对象（逐行遍历）。
- **示例代码：**

```python
# 第一步：创建『文件对象』
file = open('a.txt', 'rt', encoding='utf-8')

# 第二步：操作文件（读取）
for line in file:
    print(line, end='')

# 第三步：关闭文件
file.close()
```

<a id="EAe1b"></a>

### 4️⃣`readlines`方法

- **概述：**使用文件对象的`readlines`方法，一次性按“行”读完，返回一个列表。
- **方法说明：**

> 1. `readlines(hint)` 中的`hint`是可选参数。
>
>
>
> 🔸若不传递`hint`参数，表示：读取当前文件的所有行。
>
>
>
> 🔸若传递了`hint`参数，表示：期望读取的【字符个数 或 字节数】（`hint`不是行数）。
>
> 1. 注意：由于`readlines`是一次性读取文件的所有内容，所以不适合读取体积较大的文件。

- **示例代码：**

```python
# 第一步：创建『文件对象』
file = open('a.txt', 'rt', encoding='utf-8')

# 第二步：操作文件（读取）
result = file.readlines()
print(result)

# 第三步：关闭文件
file.close()
```

<a id="X285v"></a>

### ⭐️最佳实践

- **概述：**更推荐使用`with`上下文管理器，结合`for`循环遍历，逐行读取文件。

```python
with open('a.txt', 'rt', encoding='utf-8') as file:
    for line in file:
        print(line, end='')
```

<a id="sCHie"></a>

## 关于`with`

- **概述：**Python 中的`with`主要用于管理程序中“需要成对出现的操作”，例如：

🔸上锁 / 解锁

🔸打开 / 关闭

🔸借用 / 归还

- **使用**`with`**的目标：**编码者只管做具体的事，“进入”和“离开”的事，让 Python 自动处理。
- **语法格式：**

```python
with 能得到一个上下文管理器的表达式 as 变量:
    具体的事1
    具体的事2
    具体的事3
```

- **上下文管理器协议：**

> 1. `__enter__` 方法：`with`中的代码执行【之前】调用，其返回值会赋值给`as`后的变量。
> 2. `__exit__` 方法：`with`中的代码执行【结束后】调用（无论是`with`中否出现异常都会调用）。

- **测试代码：**

```python
# 定义一个 Person 类，让其实例对象遵循：上下文管理器协议
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f'我叫{self.name}，年龄是{self.age}')

    def __enter__(self):
        print('-----我是进入的逻辑-----')
        return self

    # 当 with 中的代码发生异常时，__exit__ 方法的返回值规则如下：
    #   🔸返回“真”：表示异常【已经】被处理，异常【不会】被继续抛出。
    #   🔸返回“假”：表示异常【没有】被处理，异常【会】被继续抛出。
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('-----我是离开的逻辑-----')
        # exc_type  : 异常类型
        # exc_val   : 异常对象
        # exc_tb    : 异常追踪信息
        if exc_type:
            print(f'异常类型：{exc_type}')
            print(f'异常对象：{exc_val}')
            print(f'异常追踪信息：{exc_tb}')
        return True

# 1.计算 with 后面的表达式，得到一个『上下文管理器』。
# 2.调用『上下文管理器』的 __enter__() 方法，并将其返回值赋给 as 后面的变量。
# 3.执行 with 所管理的代码。
# 4.无论代 with 中的代码，是正常结束，还是发生异常，都会自动调用『上下文管理器』的 __exit__ 方法。

with Person('张三', 18) as p1:
    p1.speak()
    # p1.study()
    print(666)
```

<a id="Kse2f"></a>

## 写入文件

<a id="DU0ja"></a>

### 1️⃣`w`模式

- **概述**：`w`模式是写入模式，写入前会先截断文件（清空文件）。
- **代码：**

```python
with open('b.txt', 'wt', encoding='utf-8') as file:
    file.write('你好')
```

<a id="YmG6V"></a>

### 2️⃣`x`模式

- **概述：**`x`模式是排它性创建，如果文件已存在，则创建失败。
- **代码：**

```python
with open('demo.txt', 'xt', encoding='utf-8') as file:
    file.write('你好')
```

<a id="cNYmh"></a>

### 3️⃣`a`模式

- **概述：**打开文件用于写入，如果文件存在，则在文件末尾追加内容。
- **代码：**

```python
with open('a.txt', 'at', encoding='utf-8') as file:
    file.write('你好')
```

<a id="Axgsy"></a>

## `flush`方法

- **概述：**Python 写入文件时，并不是每写一次就立刻落盘，而是：先写到“缓冲区”里。
- `flush`**方法：**把缓冲区中的数据，立刻写入到文件中。
- **测试代码**：

```python
import time
with open('demo.txt', 'at', encoding='utf-8') as file:
    file.write('你好1')
    file.write('你好2')
    file.flush()
    time.sleep(10000)
    file.write('你好3')
    file.write('你好4')
```

<a id="Yxxu4"></a>

## 组合模式

<a id="IlfwF"></a>

### 1️⃣`rt+`模式

- **概述：**`r`模式可以读取，`+`模式可以更新（读取或写入），所以`rt+`模式可读可写。
- **注意：**`r`模式打开文件后，文件指针在起始位置。
- **备注：**由于`t`是默认值，所以`rt+`中的`t`可以省略。
- **代码：**

```python
with open('a.txt', 'rt+', encoding='utf-8') as file:
    # seek(offset, whence)方法：用于改变文件对象指针的位置，参数说明如下：
    #   offset：偏移量，要移动多少距离
    #   whence：参考点，从哪里开始计算偏移，有三种取值：
    #       0：从文件开头计算（默认值）
    #       1：从当前位置计算
    #       2：从文件末尾计算
    #  注意：在文本模式下，不要随意去定位中文字符位置，否则可能破坏文件编码。
    file.seek(0, 0)
    file.write('你好')
```

<a id="GczP1"></a>

### 2️⃣`wt+`模式

- **概述：**`w`模式可以写入，`+`模式可以用于更新（读取或写入），所以`wt+`模式可读可写。
- **注意：**`w`模式打开文件后，文件指针在起始位置，但`write`方法执行完后，指针在文件结束位置。
- **备注：**由于`t`是默认值，所以`wt+`中的`t`可以省略。
- **代码：**

```python
with open('a.txt', 'wt+', encoding='utf-8') as file:
    file.write('你好')
    file.seek(0, 0)
    result = file.read()
    print(result)
```

<a id="yudgb"></a>

### 3️⃣`xt+`模式

- **概述：**`x`模式可以写入，`+`模式可以用于更新（读取或写入），所以`xt+`模式可读可写。
- **注意：**`x`模式打开文件后，文件指针在起始位置。
- **备注：**由于`t`是默认值，所以`xt+`中的`t`可以省略。
- **代码：**

```python
with open('demo3.txt', 'xt+', encoding='utf-8') as file:
    file.write('你好')
    file.seek(0, 0)
    result = file.read()
    print(result)
```

<a id="NBad2"></a>

### 3️⃣`at+`模式

- **概述：**`a`模式可以追加内容，`+`模式可以用于更新（读取或写入），所以`at+`模式可读可写。
- **注意：**`a`模式打开文件后，文件指针在结束位置。
- **备注：**由于`t`是默认值，所以`at+`中的`t`可以省略。
- **代码：**

```python
with open('a.txt', 'at+', encoding='utf-8') as file:
    file.write('你好')
    file.seek(0, 0)
    result = file.read()
    print(result)
```

<a id="uX04y"></a>

## 目录操作

Python 中常见的目录操作如下：

```python
import os
import shutil

# 1️⃣os.mkdir(path)：创建“单级”目录（如果目录已经存在，则会抛出异常）
os.mkdir('D:/demo')

# 2️⃣os.makedirs(path)：创建“多级”目录（如果路径中的所有目录都已经存在，则会抛出异常）
os.makedirs('D:/demo/aa/bb')

# 3️⃣os.rmdir(path)：删除空目录（如果目录不存在，或目录非空，都会抛出异常）
os.rmdir('D:/demo/aa/bb')

# 4️⃣os.removedirs(path)：递归删除空目录，在成功删除末尾一级目录后，会“向上”尝试把父级目录也删除
#	（直到父目录不是空目录）
os.removedirs('D:/demo/aa/bb')

# 5️⃣os.path.exists(path)：判断路径是否存在（文件/目录都算）
result = os.path.exists('D:/demo/aa/bb')
print(result)

# 6️⃣os.path.isdir(path)：用于判断路径，具体规则如下：
#   1.路径不存在 ==================> 返回 False
#   2.路径存在，但指向的是文件 =====> 返回 False
#   3.路径存在，并且是目录 =======> 返回 True
result = os.path.isdir('D:/demo/aa/bb')
print(result)

# 7️⃣os.path.isfile(path)：判断是否为文件
result = os.path.isfile('D:/demo/aa/bb')
print(result)

# 8️⃣os.scandir(path)：扫描指定目录
result = os.scandir('D:/demo')
for item in result:
    print('目录' if item.is_dir() else '文件', item.name)

# 9️⃣os.walk(path)：按层级，递归地遍历指定目录下，所有的子目录和文件
result = os.walk('D:/demo')
for item in result:
    print(item)

# ⚠️危险操作：删除有内容的目录
shutil.rmtree('D:/demo')
```

<a id="czb4D"></a>

## 两个小练习

**练习 1：**将一个二进制文件复制到指定位置。

```python
import os
# 源文件
source = 'music.mp3'
# 目标目录
target = 'D:/media'

# 如果目标目录不存在，那就去创建
if not os.path.isdir(target):
    os.makedirs(target)

with open(source, 'rb') as f1, open(target + '/' + 'my_music.mp3', 'wb') as f2:
    while True:
        # 每次只读取1KB
        data = f1.read(1024)
        # 如果文件读取完毕了，就跳出循环
        if not data:
            break
        # 向目标文件中写入数据
        f2.write(data)
    print('复制完毕')
```

**练习 2：**日志记录，需求如下：

> 1. 用户输入用户名和密码后，程序进行校验：
> 2. 用户名不存在，提示“用户名未注册”，并记录日志。
> 3. 用户名存在，但密码错误，提示“密码错误”，并记录日志。
> 4. 用户名和密码均正确，提示“登录成功”，并记录日志。

```python
import time
# 准备一些用户
users = {
    '张三': '123456',
    '李四': '888888',
    '王五': 'abc123'
}

# 提示输入信息
username = input('请输入用户名：')
password = input('请输入密码：')

# 获取当前的时间
now = time.strftime('%Y-%m-%d %H:%M:%S')

# 如果用户名不在users中
if username not in users:
    print('用户名未注册')
    with open('log.txt', 'at', encoding='utf-8') as file:
        file.write(f'{now}  {username}  登录失败（用户未注册）\n')

# 如果密码不正确
elif users[username] != password:
    print('密码不正确')
    with open('log.txt', 'at', encoding='utf-8') as file:
        file.write(f'{now}  {username}  密码错误 \n')

# 登录成功
else:
    print('登录成功！')
    with open('log.txt', 'at', encoding='utf-8') as file:
        file.write(f'{now}  {username}  登录成功 \n')
```

<a id="v4DYR"></a>
