def input_num():
    while True:
        num=input('请输入数字')
        try:
            num=int(num)
            break
        except ValueError:
            try:
                num=float(num)
                break
            except:
                print('you input error')
            return num
        except:
            print('error')

a=input_num()
b=input_num()
print(a+b)


'''
    1.创建一个函数
2.设置一个无限循环，设置用户输入一个数字并且赋值给num,但是我们不确定用户输入的到底是不是
   整型，浮点或者其他字母，所以我们需要设置其他条件来满足
3.利用try关键字函数，对结果进行异常检测
4.如果是整型，直接跳出，程序结束。如果用户输入不是整型，则会抛出一个错误。
5.如果是浮点类型，则跳出程序，否则则抛出error错误
6.如果所有错误都找不到，则抛出error错误

'''           
