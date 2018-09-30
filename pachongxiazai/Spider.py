# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 09:45:17 2018

@author: Administrator
"""
import redis, pickle, os, gzip
from bs4 import BeautifulSoup
from chardet import detect
from urllib import request, parse
from fake_useragent import UserAgent


class Urls(object):
    '''
    爬虫url管理器
    '''

    def __init__(self, name, host='127.0.0.1', port=6379):
        self.r = redis.Redis(host=host, port=port)
        self.spider_name = name

    def add_urls(self, *args):
        for x in args:
            if not self.r.sismember(self.spider_name + '_old', x):
                self.r.sadd(self.spider_name + '_new', x)
        return True

    def get_url(self):
        url = self.r.spop(self.spider_name + '_new')
        if url == None:
            return None
        self.r.sadd(self.spider_name + '_old', url)
        return url.decode('utf8')

    def back_url(self, url):
        self.r.smove(self.spider_name + '_old', self.spider_name + '_new', url)
        return True

    def __len__(self):
        return self.r.scard(self.spider_name + '_new')


# 代理池类
class ProxyPool(object):
    '''
    IP代理池
    该代理池地址由https://www.kuaidaili.com免费提供
    '''

    def __init__(self, max=5, check_url='http://www.baidu.com'):
        '''
        代理对象初始化时需要参数如下：
        @max 为代理池的大小
        @check_url 为代理池的检测地址【可选】默认为http://www.baidu.com
        设计思路：
        默认可以将本次的代理信息进行保存，一般在当前对象所在目录下的poxy.pickle文件中
        '''
        self.__max = max
        self.__check_url = check_url
        self.__proxy_get_url = 'https://www.kuaidaili.com/free/'
        self.__get_proxy()  # 初始化代理池

    def __get_proxy(self):
        '''
        初始化代理池地址
        '''
        if os.path.isfile('./poxy.pickle'):
            with open('./poxy.pickle', 'rb') as f:
                self.__Pool = pickle.load(f)
        else:
            self.__Pool = set()
        self.get_chack_pool()  # 检查并获取真实的代理池内容

    def get_chack_pool(self):
        '''
        检查并完整代理池
        '''
        proxys = set()
        for proxy in self.__Pool:
            if self.__check(proxy):
                proxys.add(proxy)
        self.__Pool = proxys
        if len(self.__Pool) < self.__max:
            self.__crawl_proxy()

    def __check(self, proxy):
        '''
        代理检查方法
        '''
        if isinstance(proxy, str):
            proxy = eval(proxy)
        proxy_handler = request.ProxyHandler(proxy)  # 创建代理对象
        opener = request.build_opener(proxy_handler)
        try:
            req = opener.open(self.__check_url)
        except:
            return False
        if req.status == 200:
            return True
        else:
            return False

    def __crawl_proxy(self):
        '''
        代理补全抓取方法
        '''
        pool = set()
        while True:
            proxys = self.get_proxy()
            for proxy in proxys:
                if self.__check(proxy):
                    pool.add(proxy)
            if len(pool) < self.__max - len(self.__Pool):
                continue
            else:
                for proxy in pool:
                    self.__Pool.add(proxy)
                # 代理池回写 以备下次使用
                with open('./poxy.pickle', 'wb') as f:
                    pickle.dump(self.__Pool, f)
                break

    def get_proxy(self):
        '''
        获取代理网站的代理地址
        '''
        rep = request.urlopen(self.__proxy_get_url)
        data = rep.read()
        if 'gzip' in rep.getheader('Content-Encoding'):
            data = gzip.decompress(data)
        html = data.decode(detect(data)['encoding'], errors='ignore')
        sel = BeautifulSoup(html, 'html.parser')
        proxys = set()
        items = sel.find(name='tbody').find_all(name='tr')
        for x in items:
            s = x.find_all(name='td')
            item = {}
            key = s[3].string
            value = key + '://' + s[0].string + ':' + s[1].string
            item[key] = value
            item = str(item)
            if item not in self.__Pool:
                proxys.add(item)
        if rep.url == 'https://www.kuaidaili.com/free/':
            self.__proxy_get_url = 'https://www.kuaidaili.com/free/inha/2'
        else:
            n = rep.url.spit('/')[-2]
            n = int(n) + 1
            self.__proxy_get_url = 'https://www.kuaidaili.com/free/inha/' + str(n) + '/'
        return proxys

    def getProxy(self):
        data = self.__Pool.pop()
        self.__Pool.add(data)
        return eval(data)


# ======================================
# 音乐爬取过程需要函数
# 1、下载函数
def download(url, headers, proxy):
    req = request.Request(url=url, headers=headers)
    handler_proxy = request.ProxyHandler(proxy)
    opener = request.build_opener(handler_proxy)
    rep = opener.open(req)
    data = rep.read()
    try:
        data = gzip.decompress(data)
    except:
        pass
    html = data.decode(detect(data)['encoding'], errors='ignore')
    return html


# 2、歌单页面解析函数
def index(html, url):
    sel = BeautifulSoup(html, 'html.parser')
    sel_l = sel.find(name='ul', attrs={'id': 'm-pl-container'})
    list = sel_l.find_all(name='a', attrs={'class': 'msk'})
    result = []
    for x in list:
        x = x['href']
        url_r = parse.urljoin(url, x)
        result.append(url_r)
    next_url = sel.find('a', string='下一页')
    try:
        next_url = next_url['href']
        next_url = parse.urljoin(url, next_url)
    except:
        next_url = None
    return result, next_url


# 3、列表页处理函数
def list_option(url, headers, Proxy):
    proxy = Proxy.getProxy()
    html = download(url, headers, proxy)
    urls, next_ = index(html, url)
    for url in urls:
        yield url
    if next_:
        for url in list_option(next_, headers, Proxy):
            yield url


# =======================
# 4、歌单处理逻辑
def music_list(url, headers, Proxy):
    proxy = Proxy.getProxy()
    html = download(url, headers, proxy)
    sel = BeautifulSoup(html, 'html.parser')
    result = {}
    result['music_list_name'] = sel.find('h2').string
    img_url = sel.find('img', class_='j-img')['data-src']
    result['img_url'] = downimg(img_url, url=None)
    # 获取歌单数据
    temp = sel.find('div', attrs={'id': 'content-operation'})
    result['save'] = temp.find('a', attrs={'data-res-action': 'fav'})['data-count']
    result['share'] = temp.find('a', attrs={'data-res-action': 'share'})['data-count']
    result['comment'] = temp.find('span', attrs={'id': 'cnt_comment_count'}).string
    # result['content']=''.join[temp.find('p',attrs={'id':'album-desc-more'}).strings]
    tag = temp.find_all('a', attrs={'class': 'u-tag'})
    result['tag'] = []
    for x in tag:
        result['tag'].append(x.find('li').string)
    result['music'] = []
    return result


# 5、图片下载方法
def downimg(img_url, url=None):
    filename = './image/' + img_url.split('/')[-1]
    request.urlretrieve(img_url, filename)
    return filename


if __name__ == '__main__':
    import pymongo
    db = pymongo.MongoClient().music_163
    tb1 = db.music_list
    start_url = 'https://music.163.com/discover/playlist'
    headers = {
        'User-Agent': UserAgent().random
    }
    Proxy = ProxyPool(max=15)
    # 列表页处理代码
    for url in list_option(start_url, headers, Proxy):
        # 每个歌单处理代码
        data = music_list(url, headers, Proxy)
        print(data, type(data))
        tb1.insert_one(data)














