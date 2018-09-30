from urllib import request
from chardet import detect
from lxml import etree
from fake_useragent import UserAgent
import chardet
import gzip
from  bs4 import BeautifulSoup
import re
def download(url):
    response=request.urlopen(url)
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

#获取网页里面的文字

a = download('https://xa.fang.anjuke.com')
b = etree.HTML(a)
con =b.xpath('//span[@class="items-name"]/text()')
print(con)


with open('楼房名字.txt','a',encoding='utf-8') as f:
    f.write(con)
