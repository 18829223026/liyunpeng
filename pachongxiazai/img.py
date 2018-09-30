# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 16:57:21 2018

@author: Administrator
"""
# 拔取网站图片
from chardet import  detect
from urllib import request,parse
import gzip,time,os
from lxml import etree
r=request.urlopen('http://www.58pic.com/')
data=r.read()
html=data.decode(detect(data)['encoding'],errors='ignore')
sel=etree.HTML(html)
imgs=sel.xpath('//img/@data-url')
for x in imgs:
    url=parse.urljoin(r.url,x)
    try:
        filename='./imges/'+str(time.time())+'.jpeg'
        request.urlretrieve(url=url,filename=filename)
    except FileNotFoundError:
        os.mkdir('./imges')
        request.urlretrieve(url=url, filename=filename)