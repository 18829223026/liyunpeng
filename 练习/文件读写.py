


while True:
    a=input('请输入用户名,输入88结束：')
    if a=='88':
        break
        
        
    b=input('请输入密码')
        
    with open('C:\\Users\\LI\\Desktop\\write.txt','a') as f:            
        f.write('用户名%s,密码%s\n'%(a,b))
    
        f.close()
   

    
with open('C:\\Users\\LI\\Desktop\\write.txt','r') as f:
    print(f.read())






    

