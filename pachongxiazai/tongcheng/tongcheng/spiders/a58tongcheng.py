# -*- coding: utf-8 -*-
import scrapy
from ..items import TongchengItem
from selenium import webdriver
from time import sleep
from lxml import etree

class A58tongchengSpider(scrapy.Spider):
    name = 'ershouche'
    # allowed_domains = ['www.che168.com']
    start_urls = ['https://www.che168.com/china/list/#pvareaid=100945']


    # cookies
    # def start_requests(self):#用start_requests()方法,代替start_urls
    #     start_urls = 'http://xa.58.com/'
    #     cookies = [{}]
    #     for i in range(1,len(cookies)+1):
    #         yield scrapy.Request(url=start_urls,cookies=cookies[i-1],meta={'cookiejar':i},callback=self.login)

    # def login(self,response):
    #     data = {                               #设置用户登陆信息
    #         'name':'18829223026',
    #         'passwd':'lyp3621625',
    #
    #     }
    #     webdriver.Chrome()
    # #     cookie1 = response.headers.getlist('set-Cookie') #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
    # #     print(cookie1,'++++++++++++++++++')
    #     yield scrapy.FormRequest.from_response(response=response,formname='submitForm_new',format=(data),callback=self.longin)#模拟表单请求
    #     print(response.headers,'++++++++++++')
    #
    # def parse(self,response):
    #     dr = webdriver.Chrome()
    #     dr.get('https://passport.58.com/login')
    #     sleep(2)
    #     dr.switch_to.frame(0)
    #     dr.find_element_by_id('scanCode').click()
    #     sleep(2)
    #     dr.find_element_by_id('usernameUser').send_keys('18829223026')
    #     sleep(2)
    #     dr.find_element_by_id('passwordUserText').send_keys('lyp3621625')
    #     sleep(2)
    #     dr.find_element_by_id('btnSubmitUser').click()
    #     cookies = dr.get_cookies()
    #     # dr.close()
    #     print(cookies,'@@@@@@@@@@@@@@@@@@@@@')
    #     return cookies
    # def parse_1(self,response):
    #     links = response.css('.header-container>img::attr("href")')
    #     yield scrapy.Request(url=links,callback=self.parse_)

    # def parse(self, response):#进去西安58同城分类，获取二手车链接地址
    #     links = response.css('.t>a::attr("href")').extract()
    #     url = response.urljoin(links)
    #     yield scrapy.Request(url=url, callback=self.next1)

    def parse(self, rp):
        # print(rp.url,'+========================+')
        # print(rp.request.readers,'***************')
        links = rp.css('.carinfo::attr("href")').extract()#获
        # 取页面所有二手车链接
        for x in links:
            # 利用response对象的urljoin方法补全url1
            url = rp.urljoin(x)
            meta = {'url_':url}
            yield scrapy.Request(url=url, callback=self.next2,meta=meta)
        next_ = rp.css('.page-item-next::attr("href")').extract()
        if next_:
            next_ = rp.urljoin(next_[0])
            # print(next_,'++++++++++++++++++++++++++++++++')
            yield scrapy.Request(url=next_, callback=self.parse)
    def next2(self, rp):
        item = TongchengItem()
        # item['image_urls'] = rp.xpath('//*[@id="img1div"]/img[1]/@src').extract()
        item['car_name'] = rp.xpath('/html/body/div[5]/div[2]/div[1]/h2/text()').extract_first()
        try:
            item['price'] = rp.css('.car-price>ins::text').extract_first()
        except TypeError:
            item['price'] ='未知'
        item['lucheng'] = rp.css('.details>ul>li>span::text').extract_first()
        item['where_'] = rp.css('.breadnav>a::text').extract()[1]
        item['guige'] = rp.css('.details>ul>li>span::text').extract()[2]
        item['url_'] =rp.meta['url_']

        # item['car_type'] = rp.xpath('/html/body/div[4]/a[3]/text()').extract()[0]
        item['addr'] = rp.css('.car-address::text').extract_first().replace('地址:\xa0','')
        yield item

