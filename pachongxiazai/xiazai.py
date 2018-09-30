# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 09:41:22 2018

@author: Administrator
"""
from urllib import request
from chardet import detect
import chardet
import gzip
from  bs4 import BeautifulSoup
import re
def download(url):
    req=Request(url)
    response=request.urlopen(req)
    if response.status==200:
        data=response.read()
        try:
            if 'gzip' in response.getheader('Content-Encoding'):
                data=gzip.decompress(data)
        except Exception:
            html=data.decode(detect(data)['encoding'],errors='ignore')
    else:
        html=''
    return html
def Request(url):
    req=request.Request(url=url)
    return req

if __name__ == "__main__":
    req = download("http://www.sohu.com/")
    req = bytes(req,encoding='utf-8')
	# charset = chardet.detect(html)
with open('sohu.html','wb') as f:
    f.write(req)



