# -*- coding: utf-8 -*-
import scrapy
from ..items import tongchengItem
from selenium import webdriver
from time import sleep

class A58tongchengSpider(scrapy.Spider):
    name = '58tongcheng'
    allowed_domains = ['xa.58.com']
    start_urls = ['https://passport.58.com/login']
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

    def parse(self,response):
        dr = webdriver.Chrome()
        dr.get('https://passport.58.com/login')
        sleep(2)


        dr.find_element_by_link_text('扫码登录').click()
        sleep(2)
        dr.switch_to.frame(0)
        dr.find_element_by_id('usernameUser').send_keys('18829223026')
        sleep(2)
        dr.find_element_by_id('passwordUserText').send_keys('lyp3621625')
        sleep(2)
        dr.find_element_by_id('btnSubmitUser').click()
        cookies = dr.get_cookies()
        # dr.close()
        print(cookies,'@@@@@@@@@@@@@@@@@@@@@')
        return cookies
    def parse_1(self,response):
        links = response.css('.header-container>img::attr("href")')
        yield scrapy.Request(url=links,callback=self.parse_)

    def parse_(self, response):#进去西安58同城分类，获取二手车链接地址
        links = response.css('.topIco::attr("href")').extract()[2]
        url = response.urljoin(links)
        yield scrapy.Request(url=url, callback=self.next1)

    def next1(self, rp):
        # print(rp.request.readers,'***************')
        links = rp.css('.col2>a::attr("href")').extract()#获
        # 取页面所有二手车链接
        next_ = rp.css('.next::attr("href")').extract()[0]
        # print(next_, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        if next_:
            next_ = rp.urljoin(next_)
            # print(next_, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            yield scrapy.Request(url=next_, callback=self.next1)

        for x in links:
            # 利用response对象的urljoin方法补全url
            url = rp.urljoin(x)
            yield scrapy.Request(url=url, callback=self.next2)

    def next2(self, rp):
        item = tongchengItem()
        item['image_urls'] = rp.xpath('//*[@id="img1div"]/img[1]/@src').extract()
        item['car_name'] = rp.css('.content_title>p::text').extract_first()
        item['price'] = rp.css('.price_span>span::text').extract_first()+'万'
        item['lucheng'] = rp.css('.lcsp_info>ul>li>span::text').extract()[0]
        item['guige'] = rp.css('.lcsp_info>ul>li>span::text').extract()[4]
        yield item

