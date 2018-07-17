user={'zhangsan':'123456'}
n=0
while n<3:
    name=input('please input Your name:').strip()
    pwd=input('please input Your pwd:').strip()
    try:
        if user[name]==pwd:
            print('Login Success')
            break
        else:
            print('PASSWOD ERROR')
            n+=1
            
    except KeyError:
            print('Your name is not defined')
            n+=1
    except PassError as e:
        print(e.m)

else:
    print('###########33333333')




    '''
1.用字典创建一个用户名和密码数列
2.初始设置输入次数为0次
3.当输入错误次数小于3次的时候，执行语句，首先输入用户名和密码
4.用TRY语句验证，如果用户名和密码正确，抛出成功。否则跑出密码错误，抛出错误的同时
    错误次数+1次。
5.如果密码和用户名都错误的时候，抛出没有被找到。并且错误次数+1次。
6.操作三次则执行else语句，输出####333.程序结束。
    '''
