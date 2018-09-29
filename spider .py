# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 08:14:45 2018

@author: Administrator
"""
import sys
import argparse
import logging
import sqlite3
import requests
import jieba
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from urllib import parse as Parse
#import jieba

#数据库存储类
class Response(object):
    pass
#爬虫类
class Crawl(object):
    def __init__(self,start_url,deep,dbname=None,t_num=2):
        logger.info('Create Crawl ...')
        self.__start_url=start_url
        self.__deep=deep
        self.__urls={}
        self.__t_num=t_num
        if dbname:
            try:
                self.__conn=sqlite3.connect()
                self.cu=self.__conn.cursor()
            except Exception as e:
                logger.error('Failed to request', exc_info=True)
    def start_request(self,key):
        '''爬虫启动方法'''
        logger.info('Start Crawl with %s'%self.__start_url)
        try:
            rep=Response()
            rep.response=requests.get(self.__start_url)
            rep.deep=1
            rep.text=rep.response.text
            #获取页面链接
            links=self.__getLinks(rep)
            #页面链接压入url管理器
            self.__addUrls(links)
        except Exception as e:
            logger.critical('Failed to request', exc_info=True)
        #构造线程池
        pool = ThreadPoolExecutor(self.__t_num)
        for url in self.get_url():
            pool.submit(self.get_content,url,key)
    def __addUrls(self,links):
        '''爬虫url去重管理方法'''
        for link in links:
            if link[0] not in self.__urls.keys():
                self.__urls[link[0]]=link[1]
    def __getLinks(self,rep):
        '''页面链接提取方法'''
        sel=etree.HTML(rep.text)
        links=sel.xpath('//a/@href')
        for i in range(len(links)):
            links[i]=Parse.urljoin(rep.response.url,links[i])
        links=[(x,rep.deep+1) for x in links]
        return links
    def __dataSave(self,rep,key):
        '''数据存储方法'''
        seg_list = jieba.cut(rep.text)
        logger.info('Get keys %s from %s'%(seg_list,rep.response.url))
        if key in seg_list:
            self.cu.execute('insert into info (url,key,html)values(%s,%s,%s)',(rep.response.url,key,rep.text))
            logger.warning('Save Data from %s is %s with %s'%(rep.response.url,key,seg_list))
    def get_content(self,url,key):
        
        rep=Response()
        try:
            logger.info('Start Crawl %s',url)
            rep.response=requests.get(url[0])
            rep.deep=url[1]
            rep.text=rep.response.text
            logger.info('Crawl %s is ok [%s].'%(url,rep.response.status_code))
            #获取页面链接
            links=self.__getLinks(rep)
            #页面链接压入url管理器
            self.__addUrls(links)
            self.__dataSave(rep,key)
        except Exception as e:
            logger.error('Failed to request', exc_info=True)
    def get_url(self):
        '''
        url调度管理
        '''
        while True:
            for x,y in self.__urls.items():
                if y!=0 and y<=self.__deep:
                    yield x,y
                    break
            else:
                raise StopIteration
'''
接受参数设定
@-u 请求url
@-d 抓取深度
@-f 日志文件
@-l 日志等级（1-5|info-error）
@--thread 线程数
@--dbfile 数据文件
@--key 检索关键字
'''
parse=argparse.ArgumentParser(prog='my - program', usage='%(prog)s [options] usage',description = 'my - description',epilog = 'my - epilog')
parse.add_argument('-u',help='请输入要抓取的网站入口url',type=str)
parse.add_argument('-d',help='抓取深度默认为5',type=int,default=5)
parse.add_argument('-f',help='请输入日志文件路径',type=str,default='./spider_loggin.log')
parse.add_argument('-l',help='日志级别1-5默认为5',type=int,default=5,choices=range(1,6))
parse.add_argument('--thread',help='线程默认为10',type=int,default=10)
parse.add_argument('--dbfile',help='请输入您要存储的sqllite数据库名称',type=str)
parse.add_argument('--key',help='请输入您要检索的关键字',type=str)
#获取参数空间
if __name__=='__main__':
    level=(0,50,40,30,20,10)
    args = parse.parse_args()
    #设定日志级别
    logging.basicConfig(level=level[args.l])
    logger = logging.getLogger(__name__)
    #设定日志输出位置
    filehandler = logging.FileHandler(filename=args.f,encoding="utf-8")
    streamhandler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    #获取爬虫实例
    crawl=Crawl(start_url=args.u,deep=args.d,dbname=args.dbfile,t_num=args.thread)
    #爬虫启动
    crawl.start_request(args.key)







#https://blog.csdn.net/lis_12/article/details/54618868 argsparse参考
#https://www.cnblogs.com/yunche/p/9041052.html sqllite参考
#https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p07_creating_thread_pool.html #线程池参考
#https://www.jianshu.com/p/cdea68108cbf #分词参考资料
#https://www.cnblogs.com/MrFiona/p/5978898.html 
#https://www.jb51.net/article/126681.htm  logging参考