# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from nayang.items import NayangJobItem

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['www.nybai.com']
    start_urls = ['https://www.nybai.com/job/']

    def parse(self, response):
        links=response.css('#tg_main_nav>ul>li a::attr("href")').extract()
        for x in links:
            #利用response对象的urljoin方法补全url
            url=response.urljoin(x)
            yield scrapy.Request(url=url,callback=self.work_list)
    def work_list(self,rp):
        links=rp.css('h3>a::attr("href")').extract()
        for x in links:
            #利用response对象的urljoin方法补全url
            url=rp.urljoin(x)
            yield scrapy.Request(url=url,callback=self.work)
    def work(self,rp):
        print(rp.request.headers,'+++++++++')
        i=ItemLoader(item=NayangJobItem(),response=rp)
        i.add_css('name','.f_left>h2::text')
        i.add_css('company','.gs_name2 a::text')
        i.add_css('education','.clearfix em:nth-child(7)::text')
        i.add_css('money','.clearfix em:nth-child(-2)::text')
        i.add_css('discript','.bd')
        i.add_css('job_addr','.clearfix em:nth-child(5)::text')
        yield i.load_item()
        
        
        
        
        
        
        
        
        
        