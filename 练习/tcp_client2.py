#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 14:02:35 2018

@author: 3gosc_ai    客户端
"""
import socket,json
from threading import Thread
user_list=''
user_name=''
def send(conn):
    global user_name
    while True:
        stat=input('Please input option(1-login,2-loginout,other-send msg):\n')#输入
        if stat=='1':
            user_name=input('Please your name:\n').strip()
            data={'stat':'login','from':user_name}
        elif stat=='2':
            if user_name:
                data={'stat':'out','from':user_name}
        else:
            if not user_name:
                continue
            name=input('Please input to name:\n')
            msg=input('Please input Message:\n')
            data={'to':name.strip(),'from':user_name,'msg':msg,'stat':'msg'}
        data=json.dumps(data).encode('utf8')
        conn.send(data)         #接服务端第七行
     	if stat==2:
            return
def recv1(conn):
    while True:
        data=conn.recv(1024)
        data=json.loads(data.decode('utf8'))
        print(data)
        if data['stat']=='error':
            print('Your sendto %s  msg %s is ERROR')
        elif data['stat']=='out':
            conn.close()
            print('EXIT success')
            return
        elif data['stat']=='login':
            print(data['users'])
        elif data['stat']=='msg':
            print('Your recv %s is msg %s'%(data['from'],data['msg']))

if __name__=='__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('127.0.0.1',8989))
    t1=Thread(target=send,args=(s,))
    t2=Thread(target=recv1,args=(s,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
        
        
        
        
        
        
        
        
        
        
        
        
