def fuc(*gao):       #求一个数的平均和
    s=0
    for x in gao:
        s+=x
    pj=s/len(gao)
    print(pj)
    print(s)
fuc(1,2,3,4,5,6,7,8)



def fuc(hangshu):               #输入三角形，行数任意
    for x in range(hangshu+1):
        print(x*'*')
fuc(10)


 
def fuc(**tezheng):           #取出个人信息     
    for x,y in tezheng.items(): 
        print(y)
fuc(a='nihao',b='danteng')
        
