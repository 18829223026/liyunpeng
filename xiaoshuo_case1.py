# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:34:51 2018

@author: Administrator
"""
from urllib import request,parse
from chardet import detect
from fake_useragent import UserAgent
from lxml import etree
import gzip
def download(url,callback):
    print('download:%s'%url)
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
        pass
    return callback(html,response.url)
def Request(url,ref=''):
    ua=UserAgent()
    headers={
            'User-Agent':ua.random,
            'Referer':ref,
            }
    req=request.Request(url=url,headers=headers)
    return req
#=================================================
def get_index(html,url):
    sel=etree.HTML(html)
    links=sel.xpath('//div[@class="subnav"]/ul/li/a/@href')
    for i in range(len(links)):
        links[i]=parse.urljoin(url,links[i])
    return links
def get_book_list(html,url):
    sel=etree.HTML(html)
    links=sel.xpath('//div[@id="catalog"]/div/span/a/@href')
    for i in range(len(links)):
        links[i]=parse.urljoin(url,links[i])
    next_url=sel.xpath('//a[text()="下一页"]/@href')
    if next_url:
        next_url=next_url[0]
        next_url=parse.urljoin(url,next_url)
    else:
        next_url=None
    return links,next_url
def get_content_link(html,url):
    sel=etree.HTML(html)
    link=sel.xpath('//li[@class="yuedu"]/a/@href')
    if link:
        link=link[0]
        link=parse.urljoin(url,link)
    else:
        link=None
    return link
def get_content(html,url):
    content={}
    sel=etree.HTML(html)
    next_=sel.xpath('//a[text()="下一页"]/@href')
    if next_:
        next_=next_[0]
        next_=parse.urljoin(url,next_)
    else:
        next_=None
    content['title']=sel.xpath('//div[@class="view_t"]/text()')[0]
    content['content']=str(sel.xpath('//div[@id="view_content_txt"]')[0])
    return content,next_
#==============================================
links=download('http://www.jjxsw.com/',get_index)
for url in links:
    #获取分类列表页书籍地址
    urls,next_=download(url,get_book_list)
    while True:
        if not next_:
            break
        u,next_=download(next_,get_book_list)
        urls+=u
    #书记首页处理        
    for u in urls:
        boo_u=download(u,get_content_link)
        #获取内容
        content,next_=download(boo_u,get_content)
        print(next_)
        while True:
            if not next_:
                break
            content,next_=download(next_,get_content)
            print(next_)
    
    
    
    
    
    
    
    