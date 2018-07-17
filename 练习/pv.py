#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 10:44:13 2018

@author: 3gosc_ai
"""
class Pv(list):
    def __init__(self,*args):    #创建一个函数，包括数组
        self.__value=[]          #给VALUE赋值[]
        for x in args:           #循环遍历这个数组
            if not isinstance(x,int) and not isinstance(x,float):    #如果x不是整型和不是浮点型，则输出错误，如果是，则给新建的空列表后面加X
                print(' shu ru de value ERROR')
                break
            else:
                self.__value.append(x)
    def __add__(self,other):             #创建一个函数，包括另外一个输入向量
        if not isinstance(other,Pv):    #如果不是Pv，则报错
            print('ERROR')
            return False
        if len(self.__value)>len(other._Pv__value):   #取长度大的那个向量
            s=len(self.__value)
            other._Pv__value.extend([int(x) for x in '0'*(s-len(other._Pv__value))])    #则给长度短的那个向量后面用0填补
        else:
            s=len(other._Pv__value)                                                     # 哪个向量短，则用0填补
            self.__value.extend([int(x) for x in '0'*(s-len(self.__value))])
        s=[]                                          #创建一个空列表
        for x,y in zip(self.__value,other._Pv__value):#然后循环遍历 两个向量，是他们以对应位置形成一个数组， 然后让他们对应位置相加
            s.append(x+y)
        return Pv(*s)                  #把每次加好的值放在S列表中
    def __len__(self):                 
        return len(self.__value)
    def __str__(self):
        return str(self.__value)
    def __repr__(self):
        return self.__str__()      # 加法运算
        
class matrix(object):                      #创建一个乘法函数
    def __init__(self,*args):              #创建一个数组
        self.__value=[]                    #创建一个为空的值
        for x in args:
            if not isinstance(x,Pv) :       #如果x不是整数或者浮点
                x=Pv(*x)
                self.__value.append(x)
            else:
                self.__value.append(x)
    def __add__(self,other):                #创建另外一个函数
        if not isinstance(other,matrix):    #如果不是矩阵，则报错
            print('ERROR')
            return False
        self.__value,other._matrix__value=self.__same(other)
        MC=[]
        for x,y in zip(self.__value,other._matrix__value):
            mc=[]
            for i,j in zip(x._Pv__value,y._Pv__value):
                mc.append(i+j)
            MC.append(mc)
        return matrix(*MC)
    def __len__(self):
        return len(self.__value)
    # jiang liang ge juzhen  yuansu jinxin duiqi
    def __same(self,other):
        M1,M2=self.__value,other._matrix__value
        clom_s=0
        rows_s=0
        if len(M1[0])>len(M2[0]):clom_s=len(M1[0])
        else:clom_s=len(M2[0])
        if len(M1)>len(M2):rows_s=len(M1)
        else:rows_s=len(M2)
        if clom_s>len(M2[0]):
            seq=[int(x) for x in (clom_s-len(M2[0]))*'0']
            for i in range(len(M2)):
                M2[i]._Pv__value.extend(seq)
        else:
            seq=[int(x) for x in (clom_s-len(M1[0]))*'0']
            for i in range(len(M1)):
                M1[i]._Pv__value.extend(seq)
        if rows_s>len(M2):
            for i in range(rows_s-len(M2)):
                M2.append(Pv(*[int(x) for x in '0'*clom_s]))
        else:
            for i in range(rows_s-len(M1)):
                M1.append(Pv(*[int(x) for x in '0'*clom_s]))
        return M1,M2
    def __str__(self):
        value='['
        for x in self.__value:
            value+=str(x)+'\n'
        return value[:-1]+']'
    def __repr__(self):
        return self.__str__()
    
if __name__=="__main__":
    a=[[1,1,1,1],[1,1,1,1]]
    b=[[2,2],[2,2],[2,2]]
    a=matrix(*a)
    b=matrix(*b)
    print(a+b)
    
    
    
    
    
    
    
