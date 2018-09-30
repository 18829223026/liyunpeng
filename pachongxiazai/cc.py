# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 09:01:38 2018

@author: Administrator
"""
from urllib import request,parse
from chardet import detect
from fake_useragent import UserAgent
import lxml,re
import gzip,time
from bs4 import BeautifulSoup
from Spader import Urls
from multiprocessing import Pool
def download(url,u):
    req=Request(url)
    try:
        response=request.urlopen(req)
        if response.status==200:
            data=response.read()
            if 'gzip' == response.getheader('Content-Encoding'):
                data=gzip.decompress(data)
            html=data.decode(detect(data)['encoding'],errors='ignore')
        else:
            html=''
    except:
        u.back_url(url)
    return html,response.url
def Request(url,ref=''):
    ua=UserAgent()
    headers={
            'User-Agent':ua.random,
            'Referer':ref,
            }
    req=request.Request(url=url,headers=headers)
    return req
def get_links(html,url):
    #sel=lxml.etree.HTML(html)
    sel=BeautifulSoup(html,'html.parser')
    #links=sel.xpath('//a/@href')
    urls=sel.find_all(name='a')
    links=[]
    for i in range(len(urls)):
        try:
            links.append(urls[i]['href'])
        except:
            pass
    for i in range(len(links)):
        links[i]=parse.urljoin(url,links[i])
    ls=[]
    ru=url.split('/')[2]
    for x in links:
        try:
            if ru==x.split('/')[2]:
                ls.append(x)
        except:
            pass
    return ls
#========================================
def saveData(html,url):
    sel=re.match(r'.+(/book/\d+)',url) 
    if sel:
        sel=lxml.etree.HTML(html)
        name=sel.xpath('//div[@class="book-information cf"]/div/h1/em/text()')
        print(name,'++++')
'''
class Urls(object):
    def __init__(self,name):
        self.name=name
        self.__new=set()
        self.__old=set()
    def add_urls(self,*args):
        for x in args:
            if x not in self.__old:
                self.__new.add(x)
        return True
    def get_url(self):
        url=self.__new.pop()
        self.__old.add(url)
        return url
    def __len__(self):
        return len(self.__new)
'''
def crawl(url,spider_name):
    u=Urls(spider_name)

    result=download(url,u)

    links=get_links(result[0],result[1])

    u.add_urls(*links)
    saveData(result[0],result[1])
if __name__=='__main__':
    spider_name='myspidr22'
    url=Urls(spider_name)
    url.add_urls('https://www.xs8.cn/')
    pool=Pool(5)
    exit_stat=0
    while True:
        u=url.get_url()
        if u:
            pool.apply_async(crawl,args=(u,spider_name)) 
            #crawl(u,url)
        else:
            exit_stat+=1
            time.sleep(2)
        if exit_stat>8:
            break
    pool.close()
    pool.join()