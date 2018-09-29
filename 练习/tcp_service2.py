#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jul  7 13:32:07 2018

@author: 3gosc_ai   服务端
"""
import socket,json
from threading import Thread
user_list={}                                #创建一个字典
def recv(conn):                             #创建一个接收函数
    global user_list
    while True:
        data=conn.recv(1024)                #接收函数
        print(data,addr)                    #输出接受到客户端的信息
        data1=json.loads(data.decode('utf8'))  #把数据反序列化和编码以后生成     
        if data1['stat']=='msg':
            if user_list.get(data1['to']):
                user_list.get(data1['to']).send(data)   #发送data
            else:
                data1['stat']=='error'
                conn.send(json.dumps(data1).encode('utf8'))
        elif data1['stat']=='login':
            data={'stat':'login','users':list(user_list.keys())}
            user_list[data1['from']]=conn
            for x in user_list.values():
                x.send(json.dumps(data).encode('utf8'))   #注册
        elif data1['stat']=='out':
            user_list[data1['from']].close()
            del user_list[data1['from']]
            data={'stat':'login','users':user_list.keys()}
            for x in user_list.values():
                x.send(json.dumps(data).encode('utf8'))
		conn.close()
                return False
    
if __name__=='__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #创建socket
    s.bind(('127.0.0.1',8989))  #为cocket绑定IP和端口号
    s.listen(5)            #设置监听消息等待序列
    while True:
        conn,addr=s.accept()   #accept方法，每接受一次生成conn，addr
        t=Thread(target=recv,args=(conn,))  #开启多线程模式
        t.start()
        
