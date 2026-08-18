# open 函数最常用的三个参数如下：
#   1.file：要操作的文件路径
#   2.mode：文件的打开模式
#       r ：读取（默认值）
#       w ：写入，并先截断文件
#       x ：排它性创建，如果文件已存在，则创建失败
#       a ：打开文件用于写入，如果文件存在，则在文件末尾追加内容
#       b ：二进制模式
#       t ：文本模式（默认值）
#       + ：打开用于更新（读取与写入）
#   3.encoding：字符编码
import time

# 测试 w 模式
# with open('b.txt', 'wt', encoding='utf-8') as file:
#     file.write('你好')

# 测试 x 模式
# with open('demo.txt', 'xt', encoding='utf-8') as file:
#     file.write('你好')

# 测试 a 模式
# with open('a.txt', 'at', encoding='utf-8') as file:
#     file.write('你好')

# 在 Python 中文件写入时，并不是每写一次就立刻落盘，而是：先写到“缓冲区”里。
# 文件对象的 flush 方法：把缓冲区中的数据，立刻写入到文件中。
# with open('demo.txt', 'at', encoding='utf-8') as file:
#     file.write('你好1')
#     file.write('你好2')
#     file.flush()
#     time.sleep(10000)
#     file.write('你好3')
#     file.write('你好4')

# 测试 rt+
# with open('a.txt', 'rt+', encoding='utf-8') as file:
#     # seek(offset, whence)方法：用于改变文件对象指针的位置，参数说明如下：
#     #   offset：偏移量，要移动多少距离
#     #   whence：参考点，从哪里开始计算偏移，有三种取值：
#     #       0：从文件开头计算（默认值）
#     #       1：从当前位置计算
#     #       2：从文件末尾计算
#     #  注意：在文本模式下，不要随意去定位中文字符位置，否则可能破坏文件编码。
#     file.seek(0, 0)
#     file.write('你好')

# 测试 wt+
# with open('a.txt', 'wt+', encoding='utf-8') as file:
#     file.write('你好')
#     file.seek(0, 0)
#     result = file.read()
#     print(result)

# 测试 xt+
# with open('demo3.txt', 'xt+', encoding='utf-8') as file:
#     file.write('你好')
#     file.seek(0, 0)
#     result = file.read()
#     print(result)

# 测试 at+
# with open('a.txt', 'at+', encoding='utf-8') as file:
#     file.write('你好')
#     file.seek(0, 0)
#     result = file.read()
#     print(result)
