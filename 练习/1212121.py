class Myclass():
    def __init__(self,name,age):#定义构造方法
        
        self.name=name
        self.age=age
        
    def aaa(self):
        print(self.name,self.age)
    def bbb(self):
        self.sex=5
        print(self.name,self.sex)

       
    
a=Myclass('liyunpeng',20)
a.bbb
a.aaa()
a.bbb()



