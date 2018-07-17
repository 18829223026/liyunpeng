class PwdError(Exception):
    def __init__(self,msg):
        self.msg=msg

    def __repr__(self):
        return str(self.msg)

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
         
            raise PwdError('Your Passworld Error')
            n+1
    
    except KeyError:
            print('Your name is not defined')
            n+=1
    except PwdError as e:
        print(e.msg)
        n+1

else:
    print('###########33333333')
