# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 08:37:03 2018

@author: Administrator
http://www.ivsky.com/bizhi/chengshi_qiuri_he_xue_v41292/pic_663796.html
http://www.zhuoku.com/zhuomianbizhi/star-starcn/20180625153200(2).htm#turn
http://www.zhuoku.com/zhuomianbizhi/game-ctwall/20180724163809(4).htm#turn
内容
http://www.zhuoku.com/zhuomianbizhi/star-starcn/20180806002103.htm
http://www.zhuoku.com/zhuomianbizhi/movie/index-1.htm
http://www.zhuoku.com/zhuomianbizhi/design-jingmeisheji/20090504191703.htm
普通
"""
# 爬壁纸网站
from bs4 import BeautifulSoup
from lxml import etree
from chardet import  detect
from urllib import request,parse
import gzip,time
def dowmloadHtml(url):
    r=request.urlopen(url=url,timeout=1)
    if r.getcode()==200:
        data=r.read()
        if r.getheader('Content-Encoding')=='gzip':
            data=gzip.decompress(data)
    else:
        print('ERROR')
    html=data.decode(detect(data)['encoding'],errors='ignore')
    return html,r.url
def links(*args):
    if len(args)!=2:
        return
    sel=etree.HTML(str(args[0]))
    links=sel.xpath('//a/@href')
    for i in range(len(links)):
        links[i]=parse.urljoin(args[1],links[i])
    result=[]
    for x in links:
        try:
            if '.'.join(x.split('/')[2].split('.')[-2:])=='.'.join(args[1].split('/')[2].split('.')[-2:]):
                result.append(x)
        except:
            pass
    return result
def option(urls):
    if urls==None:
        return
    for x in urls:
        print(x)
        if x[-5:]=='#turn':
            html,url=dowmloadHtml(x)
            sel=etree.HTML(html)
            src=sel.xpath('//img[@id="imageview"]/@src')[0]
            filename='../imges/'+str(time.time())+'.'+src.split('.')[-1]
            print(src)
            request.urlretrieve(src,filename)
            option(links(html,url))
        else:
            option(links(dowmloadHtml(x)))

if __name__=='__main__':
    url='http://www.zhuoku.com/'
    html,url=dowmloadHtml(url)
    option(links(html,url))
    