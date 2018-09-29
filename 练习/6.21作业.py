mun=input("请输入一个三位数")


a=int(mun[0])
b=int(mun[1])
c=int(mun[2])

d=a**len(mun)+b**len(mun)+c**len(mun)
if d==int(mun):
    print("水仙花数")
else:
    print("不是水仙花数")
  
        
