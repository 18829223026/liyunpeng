# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TongchengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    car_name = scrapy.Field()   #车名
    price = scrapy.Field()
    lucheng = scrapy.Field()
    guige = scrapy.Field()   #规格
    where_ = scrapy.Field()
    addr = scrapy.Field()
    url_ = scrapy.Field()

class LuntanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type_name = scrapy.Field()   #车名
    clinck = scrapy.Field()
    huifu = scrapy.Field()
    anthor = scrapy.Field()
