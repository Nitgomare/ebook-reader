# 变量类型注解：给变量加上类型说明，可增强代码的可读性、让 IDE 的提示更友好。
num: int = 100
prcie: float = 12.5
message: str = '你好啊'
is_vip: bool = True
result: None = None  # 语法上没有问题，但这么写没有意义

# 注意：可以先写变量的类型注解，以后再赋值
# school: str
# print('*******', school)
# school = '尚硅谷'

# hobby 是列表，并且列表中的所有元素必须是 str 类型
hobby: list[str] = ['抽烟', '喝酒', '烫头']

# hobby 是列表，并且列表中的元素，可以是：str 或 int 类型
hobby: list[str | int] = ['抽烟', '喝酒', '烫头']
# 上面这行代码的旧写法如下：
from typing import Union
hobby: list[Union[str, int]] = ['抽烟', '喝酒', '烫头']

# citys 是集合，并且集合中所有元素必须是 str 类型
citys: set[str] = {'北京', '上海', '深圳'}

# citys 是集合，并且集合中所有元素可以是：str 或 float 或 bool 类型
citys: set[str | float | bool] = {'北京', '上海', '深圳'}

# persons 是字典，键是 str 类型，值是 int 类型
persons: dict[str, int] = {'张三': 18, '李四': 19, '王五': 20}

# persons 是字典，键是 str 或 int 类型，值是 int 类型
persons: dict[str | int, int] = {'张三': 18, '李四': 19, '王五': 20}

# 元组的类型声明有点特殊，各位要留意一下：
# scores 是元组，并且元组中仅包含1个int类型的元素
scores: tuple[int] = (60,)

# scores 是元组，并且元组中包含3个int类型的元素
scores: tuple[int, int, int] = (60, 70, 80)

# scores 是元组，并且元组中包含任意个数的元素，但每个元素的类型必须是int
scores: tuple[int, ...] = (60, 70, 80, 90, 100)

# scores 是元组，并且元组中包含任意个数的元素，每个元素的类型可以是：int 或 str
scores: tuple[int | str, ...] = (60, '70', 80, '90', 100)

# Python 会根据初始赋值推导变量的类型：
# 1. 对于普通变量：后续如果改变类型，不会警告。
# 2. 对于容器变量：要求内部元素类型必须与推导出来的一致，否则就会警告。
x = 100
x = '尚硅谷'

y = [10, 20, 30]
y.append('40')
