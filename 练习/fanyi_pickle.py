#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 13:34:09 2018

@author: 3gosc_ai
"""
import os,pickle,json 
def login():            #登陆
    if os.path.exists('user.pickle'):                       #查找是否文件是否存在
        with open('user.pickle','rb') as f:                 #打开文件
            users=pickle.load(f)                            #把文件内容反序列化出来
        n=0
        while n<3:                                          #当输入次数小于三次的时候可以继续输入
            name=input('Please input your name:')
            pwd=input('Please input your password:')
            if (name,pwd) in users:                         #如果用户名和密码都在里面，则登陆成功              
                print('Login success')
                return True
            else:                                           #如果不存在，则次数加一次
                n+=1
        else:
            return False                                    #如果登陆次数大于三次，则报错
    else:                                                   #如果文件中没有用户名和密码，则
        print('is not users,please reg user')
        if reg():
            login()
        else:
            return False
        
def reg():                                                  #注册
    try:
        users,f=[],False
        f=open('user.pickle','rb')                          #打开文件
        users_p=pickle.load(f)                              #反序列化
        users.extend(users_p)                               #把值赋值给users
    except:
        users=[]                                            #如果try里面报错，则说里面没有值
        if f:                                               #如果文件里面有内容，则关闭文件
            f.close()
    name=input('Please input your name:')                   #输入用户名
    pwd=input('Please input your password:')                #输入密码
    with open('user.pickle','wb') as f:                     #打开文件
        users.append((name,pwd))                            #把输入的用户名和密码放到users里面
        pickle.dump(users,f)                                #把users保存到f并且序列化
        print('REG success')
    return True
def search():                                               #搜索
    if os.path.exists('data.json'):                         #查看是否有这个文件
        with open('data.json','r') as f:                    #打开文件
            data=json.load(f)
    else:
        data={}
    keyword=input('Please input you will search key:')
    result=data.get(keyword)
    if result:
        return result
    else:
        print('it is not your search key')
        data=input('if you will rec,please input "rec"')
        if data=='rec':
            rec()
        else:
            return False
def rec():
    if os.path.exists('data.json'):
        with open('data.json','r') as f:
            data=json.load(f)
    else:
        data={}
    key=input('Please input KEY:')
    value=input('Please input your password VALUE:')
    with open('data.json','w') as f:
        data[key]=value
        json.dump(data,f)
        print('REC success')
    return True

if __name__=='__main__':
    option=input('login Please input 1 exit input 88')
    if option=='1':
        login()
        while True:
            option=input('Please input 1 search 2 rec 3 quite')
            if option=='1':
                data=search()
                if data:print(data)
            elif option=='2':
                rec()
            else:
                exit()
    else:
        exit()
    elif option=='88':
        exit()
    else:
        rec()
        if login():
            while True:
                option=input('Please input 1 search 2 rec 3 quite')
                if option=='1':
                    search()
                elif option=='2':
                    rec()
                else:
                    exit()
        else:
            exit()
    
    
    
    
    
    
    
    
    
    
