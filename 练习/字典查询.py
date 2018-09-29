d={}
while True:
    suc=input('请输入您要翻译的内容，推出请按88：')
    suc=suc.strip()
    if suc=='88':
        print('您已推出程序')
        break
    opt=d.get(suc,404)
    for x in d.items():
        
        if suc in x and suc in d.keys():
            opt=x[1]
            
        elif suc in x:
            opt=x[0]
    if opt==404:
        opt=input('请输入内容')
        d[suc]=opt.strip()
    else:
        print('结果：%s'%(opt,))

'''
1.使用while循环，当用户输入88时候 直接退出循环。
2.输入的值储存在d函数里面，然后我们从函数里面遍历键-值出来，然后给条件，同时满足第一个
    这个值是key的时候，取出他的Value的值，当他不是的时候，则去key值
3.最后输出这个值
            
