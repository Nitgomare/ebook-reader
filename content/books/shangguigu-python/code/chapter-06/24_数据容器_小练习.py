# 练习一：水果清单
fruits = {
    '苹果': 4.5,
    '香蕉': 3.2,
    '橙子': 5.8,
    '草莓': 12.0,
    '哈密瓜': 8.8
}

# 需求1：打印所有的水果
# for key in fruits:
#     print(f'{key}：{fruits[key]} 元/斤')

# 需求2：找到最贵水果
# key = max(fruits, key=fruits.get)
# print(f'最贵的水果是{key}，价格是{fruits[key]} 元/斤')

# --------------------------------------------------------------------

# 练习二：学生成绩表
students = [
    {
        'name': '张三',
        'scores': {'语文': 88, '数学': 92, '英语': 95}
    },
    {
        'name': '李四',
        'scores': {'语文': 75, '数学': 83, '英语': 80}
    },
    {
        'name': '王五',
        'scores': {'语文': 92, '数学': 95, '英语': 88}
    }
]

# 需求1：计算每位学生的平均分
# for stu in students:
#     # 获取当前学生的成绩列表
#     score_list = stu['scores'].values()
#     # 计算平均值
#     avg = sum(score_list) / len(score_list)
#     print(f'{stu['name']}的平均成绩是：{avg:.1f}')


# 需求2：找到总分最高的学生
# def find_best():
#     # 记录分数最高的学生
#     best_students = []
#     # 记录最高分
#     best_score = 0
#     # 循环遍历
#     for stu in students:
#         # 获取当前学生的总成绩
#         total = sum(stu['scores'].values())
#         # 当前学生的成绩，如果大于best_score，就会更新数据
#         if total > best_score:
#             best_students = [stu['name']]
#             best_score = total
#         # 当前学生的成绩与最高分相同，就加入列表
#         elif total == best_score:
#             best_students.append(stu['name'])
#     print(f'最高分为{best_score}，取得最高分的学生有：{best_students}')
# find_best()

# --------------------------------------------------------------------

# 练习三：评论内容
comment = '这家奶茶真好喝，环境也不错，就是价格有点贵，好喝好喝好喝！强烈推荐！'

# 需求1：统计“好喝”出现次数
print(comment.count('好喝'))

# 需求2：将字符串中的“贵”替换为“略高”
comment2 = comment.replace('贵', '略高')
print(comment2)

# 需求3：是否包含“推荐”两个字
print('推荐' in comment)
