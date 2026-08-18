# 使用for循环遍历range()所指定的数字范围
n = 0
for n in range(1, 11):
    print(f'第{n}次你好啊')
print(f'我是for循环以外的代码，执行到这里时，循环已经结束了，此时的n是：{n}')

# 使用for循环遍历字符串
for m in 'abcdef':
    print(m)

# 演示由于误操作造成的死循环（下面代码中，用到了列表，我们后面会讲解）
# 备注：for循环还能遍历很多我们没有讲到的东西，比如：元组、列表、对象......
nums = [1,2,3]
for i in nums:
    # nums.append(4)
    print(i)
