from urllib import request,parse
from chardet import detect
from fake_useragent import UserAgent
import lxml,re
import gzip
from  lxml import etree
'''
爬取某小说网页标题
'''
def download(req):
    response=request.urlopen(req)
    if response.status==200:
        data=response.read()
        if 'gzip' == response.getheader('Content-Encoding'):
            data=gzip.decompress(data)
        html=data.decode(detect(data)['encoding'],errors='ignore')
    else:
        html=''
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
    sel=lxml.etree.HTML(html)
    links=sel.xpath('//a/@href')
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
        # name=sel.xpath('//div[@class="book-information cf"]/div/h1/em/text()')
        name = sel.xpath('//*[@id="j-catalogWrap"]/div[2]/div[1]/ul/li/a/text()')
        print(name,'++++')
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
if __name__=='__main__':
    url=Urls('myspidr')
    url.add_urls('https://www.xs8.cn')
    while True:
        u=url.get_url()
        if u:
            result=download(u)
        else:
            break
        links=get_links(result[0],result[1])
        url.add_urls(*links)
        saveData(result[0],result[1])
