# -*- coding: utf-8 -*-
import scrapy
from ..items import YqxsItem
from scrapy_redis.spiders import RedisSpider
from lxml import etree

class XsSpider(RedisSpider):
    name = 'xs'
    allowed_domains = ['www.23us.so']
    start_urls = ['https://www.23us.so/']
    # redis_key = 'xs:start_url'
    def parse(self, response):
        links = response.css('li a::attr("href")').extract()[1:11]
        for x in links:
            # 利用response对象的urljoin方法补全url
            url = response.urljoin(x)
            yield scrapy.Request(url=url, callback=self.next1)


    def next1(self,rp):
        bb = rp.css('#content>dd>table>tr')[1:]
        for x in bb:#传入下页内容
            links = x.css('.L>a::attr("href")').extract()[0]
            cc = x.css('.L>a::text').extract()[0]
            links = rp.urljoin(links)
            meta = {'wenben':cc}
            yield scrapy.Request(url=links,callback=self.next2,meta=meta)


        # links = rp.css('.L>a::attr("href")').extract()[::2]
        next_ = rp.xpath('//*[@id="pagelink"]/a[8]/@href').extract_first()

        if next_:
            next_ = rp.urljoin(next_)
            yield scrapy.Request(url=next_, callback=self.next1)

        # for x in links:
        #     # 利用response对象的urljoin方法补全url
        #     url = rp.urljoin(x)
        #     yield scrapy.Request(url=url, callback=self.next2)

    def next2(self, rp):
        item = YqxsItem()
        item['image_urls'] = rp.css('.hst>img::attr("src")').extract()
        item['book_name'] = rp.meta['wenben']
        # item['book_name'] = rp.css('h1::text').extract()[0].split(' ')[0]
        item['type_'] = rp.css('td>a::text').extract()
        item['anthor'] = rp.css('td::text').extract()[1]
        item['num_zishu'] = rp.css('tr')[1].css('td::text')[1].extract().replace('\xa0','')
        yield item


