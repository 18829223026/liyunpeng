from threading import current_thread,Thread,local

import os,time


def worker_1(tg):
    print('我特别喜欢听%s，进程ID%d'%(tg,os.getppid()))
    time.sleep(3)
    print('结束1')
    

def worker_2(dq):
    print('%s特别有意思，进程ID%d'%(dq,os.getppid()))
    time.sleep(5)
    print('结束2')
    

if __name__=='__main__':
    p1=Thread(target=worker_1, args=('Rssen',))
    p2=Thread(target=worker_2, args=('打球',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
