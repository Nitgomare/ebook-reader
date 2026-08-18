# 1️⃣为什么要进行异常处理？
# 程序运行过程中出现的异常，如果得不到处理，那程序就会立即崩溃，导致后续代码无法执行。
# 异常处理不是让异常消失，而是将异常捕获到，随后根据异常的具体情况，来执行指定的逻辑。
# print('欢迎使用本程序')
# a = int(input('请输入第一个数：'))
# b = int(input('请输入第二个数：'))
# result = a / b
# print(f'{a}除以{b}的结果是：{result}')
# print('*******我是后续的其它逻辑1*******')
# print('*******我是后续的其它逻辑2*******')


# 2️⃣异常处理（初级）：
# 1.将可能出现异常的代码放在 try 中，出现异常后的处理代码写在 except 中。
# 2.如果 try 中的代码出现异常，那 try 中的后续代码将不会执行，并自动跳转到 except 中处理异常。
# 3.如果 try 中的代码没有异常，那 except 中的代码就不会执行。
# 4.无论是否发生异常，try-except 后面的代码都会继续执行。
# 5.直接写 except 会捕获到 Python 中所有的异常 ———— 实际开发中不推荐这样做。
# print('欢迎使用本程序')
# try:
#     a = int(input('请输入第一个数：'))
#     b = int(input('请输入第二个数：'))
#     result = a / b
#     print(f'{a}除以{b}的结果是：{result}')
# except:
#     print('抱歉，程序出现了异常！')
# print('*******我是后续的其它逻辑1*******')
# print('*******我是后续的其它逻辑2*******')


# 3️⃣异常处理（捕获指定的类型的异常）
# print('欢迎使用本程序')
# try:
#     a = int(input('请输入第一个数：'))
#     b = int(input('请输入第二个数：'))
#     result = a / b
#     print(f'{a}除以{b}的结果是：{result}')
# except ZeroDivisionError:
#     print('程序异常：0不能作为除数！')
# except ValueError:
#     print('程序异常：您输入的必须是数字！')
# print('*******我是后续的其它逻辑1*******')
# print('*******我是后续的其它逻辑2*******')


# 4️⃣验证一下异常类之间的继承关系
# print(issubclass(ZeroDivisionError, ArithmeticError))
# print(issubclass(ZeroDivisionError, Exception))
# print(issubclass(ValueError, Exception))
# print(issubclass(KeyboardInterrupt, Exception))
# print(issubclass(KeyboardInterrupt, BaseException))


# 5️⃣多个 except 从上往下匹配，匹配成功后不再向下匹配。
# print('欢迎使用本程序')
# try:
#     a = int(input('请输入第一个数：'))
#     b = int(input('请输入第二个数：'))
#     print(x)
#     result = a / b
#     print(f'{a}除以{b}的结果是：{result}')
# except ZeroDivisionError:
#     print('程序异常：0不能作为除数！')
# except ValueError:
#     print('程序异常：您输入的必须是数字！')
# except Exception:
#     print('程序异常!')
# print('*******我是后续的其它逻辑1*******')
# print('*******我是后续的其它逻辑2*******')


# 6️⃣获取异常的具体信息
# print('欢迎使用本程序')
# try:
#     a = int(input('请输入第一个数：'))
#     b = int(input('请输入第二个数：'))
#     print(x)
#     result = a / b
#     print(f'{a}除以{b}的结果是：{result}')
# except ZeroDivisionError:
#     print('程序异常：0不能作为除数！')
# except ValueError:
#     print('程序异常：您输入的必须是数字！')
# except Exception as e:
#     print(f'⚠程序异常，异常信息：{e}')
#     print(f'⚠程序异常，异常类型：{type(e)}')
#     print(f'⚠程序异常，异常参数：{e.args}')
#     print(f'⚠程序异常，异常的文件：{e.__traceback__.tb_frame.f_code.co_filename}')
#     print(f'⚠程序异常，异常的具体行数：{e.__traceback__.tb_lineno}')
#     # 通过 traceback 来回溯异常
#     # import traceback
#     # print(traceback.format_exc())
# print('*******我是后续的其它逻辑1*******')
# print('*******我是后续的其它逻辑2*******')


# 7️⃣一个 except，也可以捕获不同的异常
# print('欢迎使用本程序')
# try:
#     a = int(input('请输入第一个数：'))
#     b = int(input('请输入第二个数：'))
#     print(x)
#     result = a / b
#     print(f'{a}除以{b}的结果是：{result}')
# except (ZeroDivisionError, ValueError, Exception) as e:
#     if isinstance(e, ZeroDivisionError):
#         print('程序异常：0不能作为除数！')
#     elif isinstance(e, ValueError):
#         print('程序异常：您输入的必须是数字！')
#     else:
#         print(f'程序异常：{e}')
# print('*******我是后续的其它逻辑1*******')
# print('*******我是后续的其它逻辑2*******')


# 8️⃣异常处理的完整写法：
#   1.try：    尝试去做可能会出现异常的事情
#   2.except： 出现异常时的处理（出现异常时怎么补救）
#   3.else：   如果一切顺利（没有异常出现）要做的事
#   4.finally：无论有没有异常，都要做的事
# print('欢迎使用本程序')
# try:
#     a = int(input('请输入第一个数：'))
#     b = int(input('请输入第二个数：'))
#     result = a / b
#     print(f'{a}除以{b}的结果是：{result}')
# except (ZeroDivisionError, ValueError, Exception) as e:
#     if isinstance(e, ZeroDivisionError):
#         print('程序异常：0不能作为除数！')
#     elif isinstance(e, ValueError):
#         print('程序异常：您输入的必须是数字！')
#     else:
#         print(f'程序异常：{e}')
# else:
#     print('挺好的，try中的代码没有任何异常！')
# finally:
#     print('无论有没有异常，我的计算都结束了！')
# print('*******我是后续的其它逻辑1*******')
# print('*******我是后续的其它逻辑2*******')
