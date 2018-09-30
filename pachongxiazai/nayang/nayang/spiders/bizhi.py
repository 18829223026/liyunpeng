# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nayang.items import BizhiItem

class BizhiSpider(CrawlSpider):
    name = 'bizhi'
    allowed_domains = ['www.win4000.com']
    start_urls = ['http://www.win4000.com/']

    rules = (
        Rule(LinkExtractor(allow=r'wallpaper_detail_\d+.+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'.*'), follow=True),
    )

    def parse_item(self, response):
        i = BizhiItem()
        i['image_urls']=response.css('.pic-large::attr("src")').extract()
        return i
