import os
import shutil

# 1️⃣os.mkdir(path)：创建“单级”目录（如果目录已经存在，则会抛出异常）
# os.mkdir('D:/demo')

# 2️⃣os.makedirs(path)：创建“多级”目录（如果路径中的所有目录都已经存在，则会抛出异常）
# os.makedirs('D:/demo/aa/bb')

# 3️⃣os.rmdir(path)：删除空目录（如果目录不存在，或目录非空，都会抛出异常）
# os.rmdir('D:/demo/aa/bb')

# 4️⃣os.removedirs(path)：递归删除空目录，在成功删除末尾一级目录后，会“向上”尝试把父级目录也删除（直到父目录不是空目录）
# os.removedirs('D:/demo/aa/bb')

# 5️⃣os.path.exists(path)：判断路径是否存在（文件/目录都算）
# result = os.path.exists('D:/demo/aa/bb')
# print(result)

# 6️⃣os.path.isdir(path)：用于判断路径，具体规则如下：
#   1.路径不存在 ==================> 返回 False
#   2.路径存在，但指向的是文件 =====> 返回 False
#   3.路径存在，并且是目录 =======> 返回 True
# result = os.path.isdir('D:/demo/aa/bb')
# print(result)

# 7️⃣os.path.isfile(path)：判断是否为文件
# result = os.path.isfile('D:/demo/aa/bb')
# print(result)

# 8️⃣os.scandir(path)：扫描指定目录
# result = os.scandir('D:/demo')
# for item in result:
#     print('目录' if item.is_dir() else '文件', item.name)

# 9️⃣os.walk(path)：按层级，递归地遍历指定目录下，所有的子目录和文件
# result = os.walk('D:/demo')
# for item in result:
#     print(item)

# ⚠️危险操作：删除有内容的目录
# shutil.rmtree('D:/demo')
