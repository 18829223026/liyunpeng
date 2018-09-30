# -*- coding: utf-8 -*-
import scrapy
from ..items import XiaoshuoItem
from scrapy_redis.spiders import RedisSpider 
class XiaoshuoSpider(RedisSpider):
    name = 'xiaoshuo'
    # allowed_domains = ['www.xiashu.la']
    start_urls = ['https://www.xiashu.la/']
    redis_key='xiaoshuo:start_url'
    def parse(self, response):
        links= response.css('.subMenu a::attr("href")').extract()[1:3]
        for url in links:
            url=response.urljoin(url)
            yield scrapy.Request(url=url,callback=self.next1)
            
    def next1(self, response):
        links= response.css('.selecttype')[0].css('a::attr("href")').extract()[1:]
        for url in links:
            url=response.urljoin(url)
            yield scrapy.Request(url=url,callback=self.next2)
    
    def next2(self, response):
        type_=response.css('.hottext strong::text').extract_first()
        links= response.css('.item h3>a::attr("href")').extract()
        for url in links:
            url=response.urljoin(url)
            yield scrapy.Request(url=url,callback=self.next3,meta={'type_':type_})
        next_= response.css('.next::attr("href")').extract_first()
        if next_:
            yield scrapy.Request(url=response.urljoin(next_),callback=self.next2)
    
    def next3(self, response):
        url= response.css('.orangeBtn::attr("href")').extract_first()
        image_urls=response.css('.img_in img::attr("data-original")').extract()
        meta={'number':1,'image_urls':image_urls}
        meta.update(response.meta)
        if url:

            yield scrapy.Request(url=response.urljoin(url),callback=self.next4,meta=meta)
        
    def next4(self, response):
        item=XiaoshuoItem()
        item['image_urls']=response.meta['image_urls']
        item['type_']=response.meta['type_']
        item['book_name'] =response.css('.info a::text').extract()[0] 
        item['author'] = response.css('.info a::text').extract()[1]
        item['number'] =response.meta['number']
        item['chpter_name'] = response.css('h1 a::text').extract_first().split(' ',1)[-1]
        item['chpter_content'] = ''.join(response.css('#chaptercontent::text').extract()).replace('\u3000\u3000','\r\n').strip()
        yield item
        response.meta['number']+=1
        next_= response.css('.btn-primary::attr("href")')[1].extract()
        print(next_,'nextnextnextnext')
        if next_:
            yield scrapy.Request(url=response.urljoin(next_),callback=self.next4,meta=response.meta)








