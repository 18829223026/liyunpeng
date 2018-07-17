import os,pickle,json

def login():    #登陆
    if os.path.exists('user.pickle'):    #判定是否有这个文件
        with open('user.pickle','rb') as f:  #打开用户信息文件
            users=pickle.load(f)            #反序列化文件内的信息
        n=0
        while n<3:
            name=input('请输入您的用户名')
            pwd=input('请输入您的密码')
            if(name,pwd) in users:
                print('登陆成功')
                return True
            else:
                n+=1
        else:
            return False
        
    else:
        print('无用户，请注册')
        if reg():
            login()
        else:
            return False
def reg():    #注册
    try:
        users,f=[],False
        f=open('user.pickle','rb')
        users_p=pickle.load(f)
        users.extend(users_p)
    except:
        users=[]
        if f:
            f.close()
    name=input('请输入您的用户名')
    pwd=input('请输入您的密码')
    with open('user.pickle','wb') as f:
        users.append((name,pwd))
        pickle.dump(users,f)
        print('注册成功')
    return True
def search():
    if os.path.exists('user.json'):
        with open('user.json','r') as f:
            data=json.load(f)
        
    else:
        data={}
        
    keyword=input('请输入关键字')
    result=data.get(keyword)
    if result:
        return result
    else:
        print('是否需要输入关键字')
        data=input('您是否需要录入，需要录入输入rec')
        if data=='rec':
            rec()
        else:
            return False
def rec():
    if os.path.exists('user.json'):
        data={}
    else:
        with open('user.json','r') as f:
            data=json.load(f)
    key=input('请输入您的用户名')
    value=input('请输入您的密码VALUE')
    with open('data.json','w') as f:
        data[key]=value
        juon.jump(data.f)
        
        print('录入成功')
    return True


if __name__=='__main__':
    option=input('请输入1登陆')
    if option=='1':
        if login():
            while True:
        
                option=input('请继续使用2,3')
                if option=='1':
                    data=search()
                    if data:print(data)
                elif option=='2':
                    rec()
        
                else:
                    exit()
    else:
        exit()
    
        






























            
