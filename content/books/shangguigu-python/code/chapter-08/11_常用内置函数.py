# 一、输入与输出
# print() ===> 输出指定内容
# 完整参数：print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
# 参数详解：
#   1.objects：要输出的内容
#   2.sep：分隔符
#   3.end：结束符
#   4.file：输出位置
#   5.flush：是否立即刷新

# f = open('a.txt', 'w', encoding='utf-8')
# print(10, 20, 30, 40, sep='-', end='!', file=f)

import time
# 第一种进度条
# print('加载中', end='')
# for index in range(5):
#     print('.', end='', flush=True)
#     time.sleep(1)
# print('完成！', end='')

# 第二种进度条
# for index in range(1, 101):
#     print(f'\r已加载{index}%', end='', flush=True)
#     time.sleep(0.1)


# input() ===> 获取用户输入

# 二、类型转换
# int() ======> 转为整数
# float() ====> 转为浮点数
# str() ======> 转为字符串
# bool() =====> 转为布尔值
# list() =====> 转为列表
# tuple() ====> 转为元组
# set() ======> 转为集合
# dict() =====> 转为字典

# 三、数学相关
# abs() =========> 取绝对值
# print(abs(-9))
# print(abs(-2.5))
# print(abs(3 - 5))


# round() =======> 四舍五入
# 注意：round函数的四舍五入，是银行家舍入法：小于5就舍，大于5就入，等于5看奇偶（奇入偶舍）
# print(round(3.4))
# print(round(4.6))
# print(round(6.5))
# print(round(7.5))
# print(round(7.543, 2))

# pow()	=========> 次方
# print(pow(2, 3))    # 2的3次方
# print(pow(2, -1))   # 2的-1次方
# print(pow(2, 0.5))  # 2的开平方
# print(pow(2, 3, 5)) # 2的3次方对5取模


# divmod() ======> 商和余数
# print(divmod(10, 3))


# max()	=========> 最大值（支持 key 函数）
# min()	=========> 最小值（支持 key 函数）
# sum()	=========> 求和
# map()	=========> 加工一组数据
# filter() ======> 按条件过滤数据（支持 key 函数）
# reduce() ======> 合并计算（需导入 functools）
# sorted() ======> 排序（支持 key 函数）

# 四、数据容器相关
# len()	==========> 获取容器中元素的个数
# range() ========> 生成一个数字序列（可用于循环）
# for index in range(0, 10, 2):
#     print(index)

# enumerate() ====> 给序列添加索引
# zip()	==========> 将多个序列一一配对
# names = ('张三', '李四', '王五')
# scores = [60, 70, 80]
# result = zip(names, scores)
# for item in result:
#     print(item)

# 五、类型判断与对象相关
# type() ==========> 查看类型
# isinstance() ====> 判断类型
# issubclass() ====> 判断两个类的继承关系
# id() ============> 查看对象的内存地址

# 六、逻辑判断相关
# all() ====> 全为真返回True
# l1 = [10, '尚硅谷', {1, 2, 3}, -9]
# print(all(l1))

# any() ====> 有一个为真即可
# l2 = [0, '', None, False, 10]
# print(any(l2))

# 七、字符串辅助相关
# ord() ====>  获取字符的 Unicode 编码值
# chr() ====>  将 Unicode 编码值转为字符
