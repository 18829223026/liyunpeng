# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import bizhiItem


class Xs2Spider(CrawlSpider):
    name = 'xs2'
    allowed_domains = ['www.23us.so']
    start_urls = ['http://www.23us.so/']

    rules = (
        Rule(LinkExtractor(allow=r'list/\d+.+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'.*'),follow=True),

    )

    def parse_item(self, response):
        i = bizhiItem()
        i['name'] = response.css('.L>a::text').extract()[::2]
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
