#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 09:18:28 2018

@author: 3gosc_ai
"""
import socket                           #服务端
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建为socket绑定IP和端口号，指定IPV4和协议类型是TCP
s.bind(('127.0.0.1',8000))  #为socket绑定IP和端口号
s.listen(1)             #监听，赋值为1，说明只能有一个任务给监听
while True:
    conn,addr=s.accept()#Accept阻塞，知道有客户端连接进来
    conn.send(b'Please speak')#连接发送内容
    data=conn.recv(1024).decode('utf8')#服务器读取信息
    print(addr,data)   #打印地址，和你输入的内容
    conn.send(('You send is:'+data).encode('utf8'))#发送相关内容
    conn.close()     #关闭
