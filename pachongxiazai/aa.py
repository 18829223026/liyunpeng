from urllib import request
from chardet import detect
import chardet
import gzip
from bs4 import BeautifulSoup
import re

req = request.Request('http://www.sohu.com')
req = request.urlopen(req)
data = req.read()
html = data.decode(detect(data)['encoding'], errors='ignore')
html = bytes(html, encoding='utf-8')
soup = BeautifulSoup(
    html,
    'html.parser'
)
aa=soup.find_all('a')
a={}
for i in aa:
    try:
        a[i.get_text()]=i['href']
    except:
        pass
b=str(a)
b=bytes(b,encoding='utf8')
with open('sohu a链接.html','wb') as f:
    f.write(b)

