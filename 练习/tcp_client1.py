#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 09:28:39 2018

@author: 3gosc_ai
"""
import socket                                        #客户端
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #创建为socket绑定IP和端口号，指定IPV4和协议类型是TCP
s.connect(('127.0.0.1',8000))      #连接到计算机指定的端口
print(s.recv(1024).decode('utf8')) #接受子接1024，并且转码
while True:
    data=input('Please input:')    #输入你要输入的内容
    print(data,type(data))         #打印你输入的内容并且指出什么类型的
    s.send(data.encode('utf8'))    #客户端向socket写入信息
    print(s.recv(1024).decode('utf8'))#打印
